from __future__ import annotations
import numpy as np, pandas as pd
from utils import RESULTS, save_csv

def activity_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    x=df.copy(); x['month']=pd.to_datetime(x.timestamp,utc=True).dt.to_period('M').astype(str)
    x['engagement_score']=pd.to_numeric(x.engagement_score,errors='coerce')
    activity=x.groupby('month').agg(activity_count=('id','size'), score_record_count=('engagement_score','count'), total_engagement=('engagement_score','sum'), average_engagement=('engagement_score','mean'), median_engagement=('engagement_score','median'), maximum_engagement=('engagement_score','max')).reset_index()
    # A sparse archive has many comment-only months. Use the median across *observed
    # scored months* (rather than treating score-missing months as zero) as a clear,
    # source-appropriate descriptive reference. This is not a statistical test.
    observed_scores = activity.loc[activity.score_record_count.gt(0), 'total_engagement']
    baseline = float(observed_scores.median()) if len(observed_scores) else float('nan')
    activity['engagement_baseline_median'] = baseline
    activity['engagement_ratio'] = activity.total_engagement / baseline if baseline > 0 else float('nan')
    candidates=activity[(activity.score_record_count.gt(0)) & (activity.activity_count.ge(3))].sort_values('total_engagement',ascending=False).head(3).copy()
    spikes=[]
    for n,row in enumerate(candidates.itertuples(),1):
        evidence=x[x.month.eq(row.month)].nlargest(3,'engagement_score')
        spikes.append({'spike_id':f'ES{n}', 'timestamp_time_window':row.month, 'activity_count':int(row.activity_count), 'engagement_value':float(row.total_engagement), 'baseline':float(row.engagement_baseline_median), 'spike_ratio_or_zscore_or_percentile':float(row.engagement_ratio), 'evidence_records':' | '.join(evidence.url.tolist()), 'associated_topic':'See data-derived TF-IDF topics; correlation only.', 'possible_trigger':'No causal assertion; inspect contemporaneous record titles/URLs.'})
    spikes=pd.DataFrame(spikes); save_csv(activity,RESULTS/'activity_results.csv'); save_csv(spikes,RESULTS/'detected_engagement_spikes.csv')
    return activity, spikes
