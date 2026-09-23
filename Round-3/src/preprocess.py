from __future__ import annotations
import pandas as pd
from utils import PROCESSED, RESULTS, clean_text, save_csv

# A second, stricter screen applied to the already collected HN archive export.
# It requires both recommendation/feed context and a concrete change, reaction, or
# user-control/quality signal. Generic ranking mentions, jobs, and broad platform
# policy discussions are therefore excluded with an auditable reason.
CHANGE_OR_REACTION = [
    'change', 'changed', 'changing', 'update', 'updated', 'new feed', 'new algorithm',
    'open source', 'open-source', 'release', 'released', 'rollout', 'removed', 'remove',
    'opt out', 'opt-out', 'chronological', 'for you', 'what is happening', 'broken',
    'worse', 'better', 'pushed to me', 'recommendation quality', 'user control',
    'emphasized', 'de-emphasized', 'personalized feed', 'algorithmic feed'
]
RECOMMENDER = ['recommend', 'ranking', 'feed algorithm', 'algorithmic feed', 'for you', 'suggested content']

def relevance_reason(title: object, text: object, source_type: object) -> str | None:
    value = f'{title or ""} {text or ""}'.lower()
    if not any(term in value for term in RECOMMENDER):
        return None
    # A public story explicitly titled as a platform recommendation-algorithm
    # discussion is retained even when its short title omits a change verb. This
    # preserves direct announcement/discussion threads such as the March 2023
    # Twitter source-code discussion, while not admitting generic comments.
    if source_type == 'public_story' and 'recommendation algorithm' in value:
        return 'direct public story about a platform recommendation algorithm'
    if any(term in value for term in CHANGE_OR_REACTION):
        return 'recommendation/feed context plus documented change, reaction, quality, or user-control signal'
    return None

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy(); out['cleaned_text'] = out.text.map(clean_text)
    out['relevance_filter_reason'] = [relevance_reason(t, z, s) for t, z, s in zip(out.title, out.text, out.source_type)]
    audit = pd.DataFrame([{
        'initial_screened_records': int(len(out)),
        'excluded_empty_or_short_text': int(out.cleaned_text.str.len().le(2).sum()),
        'excluded_not_specific_to_change_or_reaction': int(out.relevance_filter_reason.isna().sum()),
        'excluded_duplicate_cleaned_text': int(out.cleaned_text.duplicated().sum()),
    }])
    out = out[out.cleaned_text.str.len().gt(2) & out.relevance_filter_reason.notna()].drop_duplicates(subset=['cleaned_text']).copy()
    audit['final_retained_records'] = int(len(out))
    save_csv(audit, RESULTS/'relevance_filter_audit.csv')
    save_csv(out, PROCESSED/'recommendation_algorithm_reactions_cleaned.csv')
    return out
