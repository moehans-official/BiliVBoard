import sqlite3
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_schema import get_nominations_db


def _get_conn():
    db_path = get_nominations_db()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def list_nominations(status: str = None):
    conn = _get_conn()
    if status:
        rows = conn.execute(
            'SELECT * FROM nominations WHERE status = ? ORDER BY created_at DESC',
            (status,)
        ).fetchall()
    else:
        rows = conn.execute('SELECT * FROM nominations ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_nomination(nom_id: int):
    conn = _get_conn()
    row = conn.execute('SELECT * FROM nominations WHERE id = ?', (nom_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def add_nomination(bvid: str, reason: str = ''):
    conn = _get_conn()
    try:
        conn.execute(
            'INSERT INTO nominations (bvid, reason, status) VALUES (?, ?, ?)',
            (bvid, reason, 'pending')
        )
        conn.commit()
        nom_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return nom_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def parse_nomination(nom_id: int):
    conn = _get_conn()
    row = conn.execute('SELECT bvid FROM nominations WHERE id = ?', (nom_id,)).fetchone()
    if not row:
        conn.close()
        return None

    bvid = row['bvid']
    try:
        import httpx
        url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        resp = httpx.get(url, headers=headers, timeout=10)
        result = resp.json()
        if result.get('code') != 0:
            print(f'parse failed {bvid}: API error {result.get("message")}')
            return None
        data = result['data']
        stat = data['stat']

        conn.execute('''
            UPDATE nominations SET
                title = ?, name = ?, cover_url = ?,
                score = 0, view = ?, like_count = ?,
                coin = ?, favorite = ?
            WHERE id = ?
        ''', (
            data['title'], data['owner']['name'], data.get('pic', ''),
            stat['view'], stat['like'], stat['coin'],
            stat['favorite'], nom_id
        ))
        conn.commit()
    except Exception as e:
        print(f'parse failed {bvid}: {e}')
    finally:
        conn.close()


def review_nomination(nom_id: int, status: str, reason: str = ''):
    if status not in ('approved', 'rejected'):
        return False

    conn = _get_conn()
    conn.execute('''
        UPDATE nominations SET status = ?, reason = ?, reviewed_at = ?
        WHERE id = ?
    ''', (status, reason, datetime.now().isoformat(), nom_id))
    conn.commit()
    conn.close()
    return True


def delete_nomination(nom_id: int):
    conn = _get_conn()
    conn.execute('DELETE FROM nominations WHERE id = ?', (nom_id,))
    conn.commit()
    conn.close()
