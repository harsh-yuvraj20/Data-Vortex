from __future__ import annotations
import json, shutil, sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from preprocess import preprocess
from analyze_sentiment import predict_sentiment
from analyze_activity import activity_analysis
from analyze_topics import topic_analysis
from detect_shifts import detect_shifts
from utils import ROOT, RESULTS, FIGURES, PROCESSED, save_csv

def graph(df, activity, topics, entities, evo, shifts, spikes):
    plt.style.use('seaborn-v0_8-whitegrid')
    x=df.copy(); x['month']=pd.to_datetime(x.timestamp,utc=True).dt.to_period('M').astype(str)
    def save(name): plt.tight_layout(); plt.savefig(FIGURES/name,dpi=160,bbox_inches='tight'); plt.close()
    monthly=x.groupby('month').size(); plt.figure(figsize=(10,4)); monthly.plot(color='#1f77b4'); plt.title('Relevant public records over time (Hacker News)'); plt.xlabel('Month'); plt.ylabel('Records'); plt.xticks(rotation=45); save('data_collection_overview.png'); shutil.copy2(FIGURES/'data_collection_overview.png',FIGURES/'activity_over_time.png')
    plt.figure(figsize=(10,4)); activity.set_index('month').total_engagement.plot(color='#e67e22'); plt.title('Available HN score total over time'); plt.xlabel('Month'); plt.ylabel('Score points (missing values excluded)'); plt.xticks(rotation=45); save('engagement_over_time.png')
    counts=x.predicted_sentiment.value_counts().reindex(['Positive','Negative','Neutral'],fill_value=0); plt.figure(figsize=(6,4)); counts.plot.bar(color=['#2ca02c','#d62728','#7f7f7f']); plt.title('Round 2 model sentiment distribution'); plt.xlabel('Predicted sentiment'); plt.ylabel('Records'); save('sentiment_distribution.png')
    sentiment=pd.crosstab(x.month,x.predicted_sentiment,normalize='index').reindex(columns=['Positive','Negative','Neutral'],fill_value=0); plt.figure(figsize=(10,4)); sentiment.plot(ax=plt.gca()); plt.title('Predicted sentiment proportions by month'); plt.xlabel('Month'); plt.ylabel('Proportion'); plt.xticks(rotation=45); save('sentiment_over_time.png')
    for i, row in shifts.reset_index(drop=True).iterrows():
        months=[row.start_time,row.end_time]; vals=[row.before_sentiment,row.after_sentiment]; plt.figure(figsize=(6,4)); plt.plot(months,vals,marker='o',color='#9467bd'); plt.axhline(0,color='grey',lw=.8); plt.title(f"Sentiment shift {row.shift_id}: index change {row.magnitude:+.2f}"); plt.xlabel('Month'); plt.ylabel('Positive share − negative share'); save(f'sentiment_shift_{i+1}.png')
    while len(shifts)<2:
        i=len(shifts); plt.figure(figsize=(6,4)); plt.text(.1,.5,'No second qualified shift beyond\nalgorithmically selected observations.',fontsize=12); plt.axis('off'); save(f'sentiment_shift_{i+1}.png'); shifts=pd.concat([shifts,pd.DataFrame([{}])],ignore_index=True)
    if len(spikes):
        r=spikes.iloc[0]; plt.figure(figsize=(6,4)); plt.bar(['Baseline median',r.timestamp_time_window],[r.baseline,r.engagement_value],color=['#999999','#e67e22']); plt.title(f"Engagement candidate {r.spike_id}: {r.timestamp_time_window}"); plt.ylabel('Total HN score points'); save('engagement_spike.png')
    else: plt.figure(figsize=(6,4)); plt.text(.1,.5,'No eligible engagement baseline.'); plt.axis('off'); save('engagement_spike.png')
    if not evo.empty:
        pivot=evo.pivot(index='month',columns='term',values='mentions').fillna(0); plt.figure(figsize=(10,5)); pivot.plot(ax=plt.gca()); plt.title('Top TF-IDF terms: monthly mention evolution'); plt.xlabel('Month'); plt.ylabel('Mentions'); plt.xticks(rotation=45); save('topic_evolution.png')
    if not entities.empty: plt.figure(figsize=(8,4)); entities.head(12).set_index('entity').frequency.sort_values().plot.barh(color='#17becf'); plt.title('Documented platform/product entity frequency'); plt.xlabel('Records mentioning entity'); save('entity_frequency.png')
    else: plt.figure(figsize=(6,4)); plt.text(.1,.5,'No gazetteer entities found.'); plt.axis('off'); save('entity_frequency.png')
    events=[]
    for r in shifts.dropna(subset=['end_time']).itertuples(): events.append((r.end_time,f'{r.shift_id}: sentiment shift'))
    for r in spikes.itertuples(): events.append((r.timestamp_time_window,f'{r.spike_id}: engagement candidate'))
    plt.figure(figsize=(10,3));
    for i,(date,label) in enumerate(events): plt.scatter(date,1); plt.annotate(label,(date,1),xytext=(0,15+20*(i%2)),textcoords='offset points',ha='center')
    plt.title('Algorithmically detected observation timeline'); plt.yticks([]); plt.xlabel('Month'); plt.xticks(rotation=45); save('trigger_timeline.png')

def pdf(path, title, sections, figures):
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='Small',parent=styles['BodyText'],fontSize=8,leading=10)); story=[Paragraph(title,styles['Title']),Paragraph('Data Vortex A\'26 — Round 3 | Team: hy4366<br/>Assigned topic: Public Reaction to Changes in the Recommendation Algorithm',styles['BodyText']),Spacer(1,12)]
    for h, body in sections:
        story += [Paragraph(h,styles['Heading1']),Paragraph(body,styles['BodyText']),Spacer(1,6)]
    for f,caption in figures:
        if f.exists(): story += [Image(str(f),width=6.5*inch,height=3.0*inch,kind='proportional'),Paragraph(caption,styles['Small']),Spacer(1,10)]
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=.55*inch,leftMargin=.55*inch,topMargin=.55*inch,bottomMargin=.55*inch); doc.build(story)

def make_reports(df, activity, topics, entities, shifts, spikes):
    metadata=json.loads((ROOT/'data'/'raw'/'collection_metadata.json').read_text())
    dist=df.predicted_sentiment.value_counts().to_dict(); shift_text='; '.join(f"{r.shift_id}: {r.start_time}→{r.end_time}, index {r.before_sentiment:.3f}→{r.after_sentiment:.3f} ({r.magnitude:+.3f}), n={r.record_count_before}/{r.record_count_after}" for r in shifts.itertuples()) or 'No qualified shift.'
    spike_text='; '.join(f"{r.spike_id}: {r.timestamp_time_window}, engagement {r.engagement_value:.0f} vs rolling-median baseline {r.baseline:.0f} (ratio {r.spike_ratio_or_zscore_or_percentile:.2f})" for r in spikes.itertuples()) or 'No eligible spike.'
    trigger_evidence = pd.read_csv(RESULTS/'trigger_evidence.csv')
    trigger_summary = '; '.join(f"{r.event_id}: {r.event_description}" for r in trigger_evidence.itertuples())
    quality = pd.read_csv(RESULTS/'relevance_filter_audit.csv').iloc[0].to_dict()
    sections=[('Executive Summary',f"This reproducible analysis uses {len(df)} genuine, retained public Hacker News archive records. Predictions are from the preserved Round 2 TF-IDF + Logistic Regression pipeline, not hand labels. Results describe this technical-community source only."),('DATA COLLECTION METHOD',f"Source: {metadata['source']}. Endpoint: {metadata['endpoint']}. Queries: {', '.join(metadata['query_terms'])}. The existing archive export was not recollected during this correction. A second documented screen retained records with recommendation/feed context plus a concrete change, reaction, quality, or user-control signal."),('TIME WINDOW',f"Collection ran from {metadata['collection_start_timestamp']} to {metadata['collection_end_timestamp']} (UTC). Retained source observation window: {df.timestamp.min()} to {df.timestamp.max()} UTC. This is a historical public archive sample collected through the Hacker News Algolia archive API; it is not a continuous live stream."),('Dataset Overview and Data Quality',f"Initial screened records: {quality['initial_screened_records']}. Excluded as not specific to change/reaction: {quality['excluded_not_specific_to_change_or_reaction']}; duplicate cleaned text excluded: {quality['excluded_duplicate_cleaned_text']}; final retained records: {quality['final_retained_records']}. Score/comment fields are unavailable for most HN comments and remain missing."),('Round 2 NLP Model',"The exact preserved Round 2 sklearn Pipeline is loaded directly: TF-IDF word 1–2 grams plus Logistic Regression. Its labels are Negative, Neutral, and Positive. The model produces predictions and class probabilities for every retained record."),('SENTIMENT ANALYSIS',f"Predicted distribution: {dist}. Monthly sentiment index = (Positive − Negative) / (Positive + Negative + Neutral). Algorithmically selected descriptive candidate shifts: {shift_text}. Small n values mean these are not statistical significance claims."),('ACTIVITY ANALYSIS',f"Monthly record counts and available HN score totals are charted. Engagement candidate definition: the highest monthly total of available HN story scores among months with scored records and at least three retained records; reference baseline is the median total across observed scored months. {spike_text}."),('TOPIC / ENTITY ANALYSIS',f"Topics are data-derived TF-IDF terms using English plus custom domain stopwords (min document frequency 2), not semantic topic-model labels. Highest terms: {', '.join(topics.term.head(10).tolist())}. Entities use a documented platform/product gazetteer; X requires explicit platform context: {', '.join(entities.entity.head(10).tolist()) if len(entities) else 'none'}."),('TRIGGER EXPLANATIONS',f"Evidence is drawn only from collected HN records: {trigger_summary}. These observations coincide in time with the detections; they do not establish causation. All item URLs/timestamps are listed in results/trigger_evidence.csv."),('Limitations, Conclusion, and Reproducibility',"HN is a technically oriented public forum, rather than a representative population. This historical archive sample does not fulfill continuous live monitoring, and sparse month-level samples make descriptive shifts unstable. Re-run `python src/run_round3.py` from the project root to regenerate analysis from the stored raw export; requirements are listed in requirements.txt.")]
    figs=[(FIGURES/'data_collection_overview.png','Figure 1. Retained records over time.'),(FIGURES/'sentiment_distribution.png','Figure 2. Sentiment distribution.'),(FIGURES/'sentiment_over_time.png','Figure 3. Monthly predicted sentiment.'),(FIGURES/'sentiment_shift_1.png','Figure 4. Descriptive sentiment shift candidate SS1.'),(FIGURES/'sentiment_shift_2.png','Figure 5. Descriptive sentiment shift candidate SS2.'),(FIGURES/'engagement_over_time.png','Figure 6. Available HN score over time.'),(FIGURES/'engagement_spike.png','Figure 7. Engagement candidate.'),(FIGURES/'topic_evolution.png','Figure 8. Data-derived term evolution.'),(FIGURES/'entity_frequency.png','Figure 9. Entity frequency.'),(FIGURES/'trigger_timeline.png','Figure 10. Detection timeline.')]
    pdf(ROOT/'reports'/'Round3_Analytical_Report.pdf','ROUND 3 ANALYTICAL REPORT',sections,figs)

def main():
    # Correction pass deliberately reuses the saved genuine raw archive export; no new data is collected.
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(ROOT/'data'/'raw'/'hn_recommendation_algorithm_reactions_raw.csv')
    raw['timestamp'] = pd.to_datetime(raw['timestamp'], utc=True)
    clean=preprocess(raw); df=predict_sentiment(clean); activity,spikes=activity_analysis(df); topics,entities,evo=topic_analysis(df); shifts=detect_shifts(df)
    evidence=[]
    event_specs=[]
    if len(spikes):
        event_specs.append(('ES1', spikes.iloc[0].evidence_records, f"The {spikes.iloc[0].timestamp_time_window} engagement candidate coincided with collected HN discussion of Twitter recommendation-algorithm source code."))
    for shift in shifts.itertuples():
        event_specs.append((shift.shift_id, shift.evidence_posts, f"The {shift.start_time} to {shift.end_time} descriptive candidate shift has contemporaneous collected discussion; no specific causal platform announcement is asserted from this bounded evidence."))
    for event_id, urls, description in event_specs:
        for url in str(urls).split(' | '):
            hit=df[df.url.eq(url)]
            if len(hit):
                r=hit.iloc[0]; evidence.append({'event_id':event_id,'event_description':description,'source_name':'Hacker News','article_or_post_title':r.title,'publication_timestamp':r.timestamp,'url':r.url,'reason_relevant':'Collected contemporaneous evidence record; supports temporal coincidence only.'})
    save_csv(pd.DataFrame(evidence),RESULTS/'trigger_evidence.csv')
    graph(df,activity,topics,entities,evo,shifts,spikes); make_reports(df,activity,topics,entities,shifts,spikes)
    save_csv(df,PROCESSED/'round3_recommendation_algorithm_reactions.csv')
    print(json.dumps({'records':len(df),'window':[str(df.timestamp.min()),str(df.timestamp.max())],'sentiment':df.predicted_sentiment.value_counts().to_dict(),'shifts':len(shifts),'spikes':len(spikes)},indent=2))
if __name__=='__main__': main()
