import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_schema import get_announcements_db


def _get_conn():
    db_path = get_announcements_db()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def list_announcements(active_only: bool = False):
    conn = _get_conn()
    if active_only:
        rows = conn.execute(
            'SELECT * FROM announcements WHERE is_active = 1 ORDER BY created_at DESC'
        ).fetchall()
    else:
        rows = conn.execute('SELECT * FROM announcements ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_announcement(ann_id: int):
    conn = _get_conn()
    row = conn.execute('SELECT * FROM announcements WHERE id = ?', (ann_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def add_announcement(title: str, content: str = ''):
    conn = _get_conn()
    conn.execute(
        'INSERT INTO announcements (title, content) VALUES (?, ?)',
        (title, content)
    )
    conn.commit()
    ann_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return ann_id


def update_announcement(ann_id: int, title: str = None, content: str = None, is_active: int = None):
    conn = _get_conn()
    updates = []
    params = []
    if title is not None:
        updates.append('title = ?')
        params.append(title)
    if content is not None:
        updates.append('content = ?')
        params.append(content)
    if is_active is not None:
        updates.append('is_active = ?')
        params.append(is_active)
    if updates:
        params.append(ann_id)
        conn.execute(f'UPDATE announcements SET {", ".join(updates)} WHERE id = ?', params)
        conn.commit()
    conn.close()


def delete_announcement(ann_id: int):
    conn = _get_conn()
    conn.execute('DELETE FROM announcements WHERE id = ?', (ann_id,))
    conn.commit()
    conn.close()
