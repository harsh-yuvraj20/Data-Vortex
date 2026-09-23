from __future__ import annotations
import html, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'; PROCESSED = ROOT / 'data' / 'processed'
RESULTS = ROOT / 'results'; FIGURES = ROOT / 'figures'; MODELS = ROOT.parent / 'Round-2' / 'models'
UTC = 'UTC'

def clean_html(value: object) -> str:
    s = html.unescape(str(value or ''))
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def clean_text(value: object) -> str:
    s = clean_html(value)
    s = re.sub(r'https?://\S+', ' URL ', s)
    return re.sub(r'\s+', ' ', s).strip()

def relevant(title: str, text: str) -> bool:
    """Conservative topical screen; the query context and retained wording are recorded."""
    s = (title + ' ' + text).lower()
    recommender = any(x in s for x in ['recommend', 'algorithmic feed', 'for you', 'ranking', 'timeline', 'suggested content', 'feed algorithm'])
    change = any(x in s for x in ['change', 'changed', 'update', 'launch', 'release', 'removed', 'remove', 'open source', 'rollout', 'new algorithm', 'switch'])
    platform = any(x in s for x in ['twitter', ' x ', 'youtube', 'instagram', 'facebook', 'tiktok', 'github', 'google', 'reddit'])
    return recommender and (change or platform)

def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')
