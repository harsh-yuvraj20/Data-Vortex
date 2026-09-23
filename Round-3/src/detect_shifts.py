from __future__ import annotations
import pandas as pd
from utils import RESULTS, save_csv
def detect_shifts(df: pd.DataFrame) -> pd.DataFrame:
    x=df.copy(); x['month']=pd.to_datetime(x.timestamp,utc=True).dt.to_period('M').astype(str)
    all_months=x.groupby('month').size().rename('record_count').to_frame()
    p=x.pivot_table(index='month',columns='predicted_sentiment',values='id',aggfunc='count',fill_value=0).reindex(all_months.index,fill_value=0).join(all_months)
    for label in ['Positive','Negative','Neutral']:
        if label not in p: p[label]=0
    # Only class counts belong in the denominator. `record_count` duplicates their sum.
    sentiment_total = p[['Positive', 'Negative', 'Neutral']].sum(axis=1)
    p['sentiment_index']=(p.Positive-p.Negative)/sentiment_total
    p['delta']=p.sentiment_index.diff()
    # Both adjacent windows must have a minimally interpretable sample; no tiny-month shifts.
    eligible = p.record_count.ge(3) & p.record_count.shift(1).ge(3)
    candidates=p[eligible].dropna(subset=['delta']).reindex(p.loc[eligible,'delta'].abs().sort_values(ascending=False).head(2).index)
    rows=[]
    for n,(month,row) in enumerate(candidates.iterrows(),1):
        prev=p.index[p.index.get_loc(month)-1]; evidence=x[x.month.eq(month)].nlargest(3,'engagement_score')
        rows.append({'shift_id':f'SS{n}','start_time':prev,'end_time':month,'before_sentiment':float(p.loc[prev,'sentiment_index']),'after_sentiment':float(row.sentiment_index),'magnitude':float(row.delta),'record_count_before':int(p.loc[prev,'record_count']),'record_count_after':int(row.record_count),'evidence_posts':' | '.join(evidence.url.tolist()),'possible_trigger':'Observed temporal association only; evidence URLs/titles supplied for review.'})
    out=pd.DataFrame(rows); save_csv(out,RESULTS/'detected_sentiment_shifts.csv'); save_csv(p.reset_index(),RESULTS/'sentiment_by_month.csv'); return out
