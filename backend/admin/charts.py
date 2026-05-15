import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_schema import get_chart_db, get_list_of_charts, get_cache_db


def list_charts():
    return get_list_of_charts()


def get_chart(chart_id: int):
    db_path = get_chart_db(chart_id)
    if not os.path.exists(db_path):
        return None

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    meta = {}
    for row in conn.execute('SELECT key, value FROM meta'):
        meta[row['key']] = row['value']

    videos = [dict(r) for r in conn.execute(
        'SELECT * FROM videos ORDER BY rank ASC'
    ).fetchall()]
    conn.close()

    return {'chart_id': chart_id, 'meta': meta, 'videos': videos}


def get_cache_top(limit: int = 1000):
    db_path = get_cache_db()
    if not os.path.exists(db_path):
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('''
        SELECT * FROM cache
        WHERE best_score IS NOT NULL
        ORDER BY best_score DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
