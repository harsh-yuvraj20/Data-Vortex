"""Collect real, public Hacker News discussions about recommendation-algorithm changes.

The public Algolia API is used without credentials.  Reddit and Bluesky were tested
on 2026-09-22 but returned HTTP 403 in this environment; no bypass was attempted.
HN records are public archive records, so `collected_at` is distinct from `timestamp`.
"""
from __future__ import annotations
import json, time, html, re
from datetime import datetime, timezone
from pathlib import Path
import requests, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'

def clean_html(value: object) -> str:
    s = html.unescape(str(value or ''))
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()

def relevant(title: str, text: str) -> bool:
    s = (title + ' ' + text).lower()
    recommender = any(x in s for x in ['recommend', 'algorithmic feed', 'for you', 'ranking', 'timeline', 'suggested content', 'feed algorithm'])
    change = any(x in s for x in ['change', 'changed', 'update', 'launch', 'release', 'removed', 'remove', 'open source', 'rollout', 'new algorithm', 'switch'])
    platform = any(x in s for x in ['twitter', ' x ', 'youtube', 'instagram', 'facebook', 'tiktok', 'github', 'google', 'reddit'])
    return recommender and (change or platform)

def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')

API = 'https://hn.algolia.com/api/v1/search'
QUERIES = ['Twitter recommendation algorithm', 'YouTube recommendation algorithm',
           'Instagram algorithm change', 'feed algorithm', 'recommendation algorithm',
           'recommendation ranking', 'Facebook news feed algorithm', 'algorithmic feed']
HEADERS = {'User-Agent': 'DataVortexRound3/1.0 research collection'}

def collect() -> pd.DataFrame:
    started = datetime.now(timezone.utc)
    rows, failures = [], []
    for query in QUERIES:
        try:
            response = requests.get(API, params={'query': query, 'tags': '(comment,story)', 'hitsPerPage': 100}, headers=HEADERS, timeout=30)
            response.raise_for_status()
            for hit in response.json().get('hits', []):
                title = clean_html(hit.get('story_title') or hit.get('title') or '')
                body = clean_html(hit.get('comment_text') or '')
                text = body or title
                if not text or not relevant(title, text):
                    continue
                object_id = str(hit.get('objectID'))
                is_comment = hit.get('_tags') and 'comment' in hit['_tags']
                parent = hit.get('story_id') or object_id
                rows.append({'id': 'hn_' + object_id, 'source': 'Hacker News',
                    'source_type': 'public_comment' if is_comment else 'public_story',
                    'timestamp': hit.get('created_at'), 'date': str(hit.get('created_at',''))[:10],
                    'text': text, 'title': title, 'url': f'https://news.ycombinator.com/item?id={object_id}',
                    'author_or_author_id_if_appropriate': hit.get('author'),
                    'engagement_score': hit.get('points'), 'comment_count': hit.get('num_comments'),
                    'upvote_count_if_available': hit.get('points'), 'query_term': query,
                    'topic_relevance': 'Conservative keyword/context screen: recommendation/ranking/feed plus change/platform context.',
                    'story_id': parent, 'story_url': hit.get('story_url'),
                    'collected_at': started.isoformat(), 'collection_timezone': 'UTC'})
            time.sleep(0.5)
        except Exception as exc:
            failures.append({'query': query, 'error': str(exc)})
    df = pd.DataFrame(rows)
    if df.empty: raise RuntimeError('No source records returned; do not create an empty synthetic dataset.')
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df = df.dropna(subset=['timestamp']).drop_duplicates(subset=['id']).sort_values('timestamp').reset_index(drop=True)
    df['date'] = df.timestamp.dt.date.astype(str)
    save_csv(df, RAW/'hn_recommendation_algorithm_reactions_raw.csv')
    save_csv(df, ROOT/'data'/'round3_recommendation_algorithm_reactions.csv')
    (RAW/'collection_metadata.json').write_text(json.dumps({'collection_start_timestamp': started.isoformat(), 'collection_end_timestamp': datetime.now(timezone.utc).isoformat(), 'timezone': 'UTC', 'source': 'Hacker News public Algolia archive API', 'endpoint': API, 'query_terms': QUERIES, 'records_after_topic_screen_and_deduplication': int(len(df)), 'failed_queries': failures, 'access_notes': 'Reddit and Bluesky public endpoints returned HTTP 403 from this environment on 2026-09-22; no bypass attempted.'}, indent=2), encoding='utf-8')
    return df

if __name__ == '__main__':
    out = collect(); print(f'Collected {len(out)} real public records: {out.timestamp.min()} to {out.timestamp.max()}')
