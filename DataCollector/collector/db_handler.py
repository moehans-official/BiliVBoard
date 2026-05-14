import sqlite3
from datetime import datetime


def create_database(results, db_file='bilibili_video_data.db'):
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS videos')
    c.execute('''
        CREATE TABLE videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bvid TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            pubdate TEXT,
            mid INTEGER,
            name TEXT,
            view INTEGER DEFAULT 0,
            danmaku INTEGER DEFAULT 0,
            reply INTEGER DEFAULT 0,
            favorite INTEGER DEFAULT 0,
            coin INTEGER DEFAULT 0,
            share INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            cover_url TEXT,
            cover_path TEXT,
            bilibili_url TEXT,
            rank INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    for i, data in enumerate(sorted_results, start=1):
        bilibili_url = f"https://www.bilibili.com/video/{data['bvid']}"
        c.execute('''
            INSERT INTO videos (bvid, title, pubdate, mid, name, view, danmaku, reply,
                              favorite, coin, share, like_count, score, cover_url, cover_path,
                              bilibili_url, rank)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['bvid'], data['title'], data['pubdate'], data['mid'], data['name'],
            data['view'], data['danmaku'], data['reply'], data['favorite'],
            data['coin'], data['share'], data['like'], data['score'],
            data.get('cover_url', ''), data.get('cover_path', ''),
            bilibili_url, i
        ))

    c.execute('DROP TABLE IF EXISTS periods')
    c.execute('''
        CREATE TABLE periods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            formula TEXT NOT NULL,
            total_videos INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute("INSERT INTO periods (formula, total_videos) VALUES (?, ?)",
              ('normal', len(sorted_results)))

    conn.commit()
    conn.close()
    return db_file
