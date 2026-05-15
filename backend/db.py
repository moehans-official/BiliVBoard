import sqlite3
import os
from contextlib import contextmanager
from typing import Optional

CHARTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'charts')


def get_latest_chart_db():
    if not os.path.exists(CHARTS_DIR):
        return None
    charts = sorted([f for f in os.listdir(CHARTS_DIR) if f.startswith('chart_') and f.endswith('.db')])
    if not charts:
        return None
    return os.path.join(CHARTS_DIR, charts[-1])


DB_PATH = get_latest_chart_db() or os.path.join(os.path.dirname(__file__), '..', 'DataCollector', 'bilibili_video_data.db')


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_rankings(limit: int = 20, offset: int = 0) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute('''
            SELECT rank, bvid, title, name, view, danmaku, reply, favorite,
                   coin, share, like_count, score, cover_url, bilibili_url
            FROM videos
            ORDER BY rank ASC
            LIMIT ? OFFSET ?
        ''', (limit, offset)).fetchall()
        return [dict(r) for r in rows]


def get_video_detail(bvid: str) -> Optional[dict]:
    with get_db() as conn:
        row = conn.execute('''
            SELECT rank, bvid, title, pubdate, name, view, danmaku, reply,
                   favorite, coin, share, like_count, score, cover_url, bilibili_url
            FROM videos WHERE bvid = ?
        ''', (bvid,)).fetchone()
        return dict(row) if row else None


def get_period_info() -> Optional[dict]:
    with get_db() as conn:
        try:
            row = conn.execute('''
                SELECT key, value FROM meta
            ''').fetchall()
            if row:
                meta = {r['key']: r['value'] for r in row}
                return {
                    'formula': meta.get('formula', 'unknown'),
                    'total_videos': conn.execute('SELECT COUNT(*) FROM videos').fetchone()[0],
                }
        except:
            pass
        try:
            row = conn.execute('''
                SELECT id, formula, total_videos, created_at
                FROM periods ORDER BY id DESC LIMIT 1
            ''').fetchone()
            return dict(row) if row else None
        except:
            return None


def get_total_count() -> int:
    with get_db() as conn:
        row = conn.execute('SELECT COUNT(*) as cnt FROM videos').fetchone()
        return row['cnt']
