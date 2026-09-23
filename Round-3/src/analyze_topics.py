from __future__ import annotations
from collections import Counter
import re, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from utils import RESULTS, save_csv

STOP={'algorithm','algorithms','recommendation','recommendations','change','changed','new','using','like','just','would','people','really','also','content','use','user','users','things','way','time','good','think','don','url','news','want','doesn','ve','make','social','media'}
ENTITIES=['Twitter','YouTube','Instagram','Facebook','TikTok','Google','GitHub','Reddit','Spotify','Netflix','Meta']
def topic_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    vec=TfidfVectorizer(stop_words=sorted(ENGLISH_STOP_WORDS | STOP),ngram_range=(1,2),min_df=2,max_features=40)
    matrix=vec.fit_transform(df.cleaned_text); scores=matrix.sum(axis=0).A1; words=vec.get_feature_names_out()
    topics=pd.DataFrame({'term':words,'tfidf_total':scores}).sort_values('tfidf_total',ascending=False)
    x=df.copy(); x['month']=pd.to_datetime(x.timestamp,utc=True).dt.to_period('M').astype(str)
    top=topics.term.head(8).tolist(); evolution=[]
    for month, group in x.groupby('month'):
        content=' '.join(group.cleaned_text.str.lower())
        for term in top: evolution.append({'month':month,'term':term,'record_count':len(group),'mentions':len(re.findall(r'(?<!\w)'+re.escape(term)+r'(?!\w)',content))})
    entities=[]
    for entity in ENTITIES:
        count=x.cleaned_text.str.contains(r'(?i)(?<!\w)'+re.escape(entity)+r'(?!\w)',regex=True).sum()
        if count: entities.append({'entity':entity,'frequency':int(count),'method':'case-insensitive gazetteer, documented platform/product list'})
    # A bare, case-insensitive `x` is not reliable. Count X only in explicit platform contexts.
    x_pattern = r'(?i)(?:\btwitter\s*/\s*x\b|\bx\s*\(formerly\s+twitter\)|\bon\s+x\b|\bx[’\']s\s+(?:recommendation|feed|algorithm))'
    x_count = x.cleaned_text.str.contains(x_pattern, regex=True).sum()
    if x_count:
        entities.append({'entity':'X','frequency':int(x_count),'method':'explicit X/Twitter platform-context regex; bare X excluded'})
    entity_df=pd.DataFrame(entities).sort_values('frequency',ascending=False) if entities else pd.DataFrame(columns=['entity','frequency','method'])
    save_csv(topics,RESULTS/'topic_results.csv'); save_csv(entity_df,RESULTS/'entity_results.csv'); save_csv(pd.DataFrame(evolution),RESULTS/'topic_evolution_results.csv')
    return topics,entity_df,pd.DataFrame(evolution)
