import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CHARTS_DIR = os.path.join(DATA_DIR, 'charts')


def init_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)


def get_all_songs_db():
    return os.path.join(DATA_DIR, 'AllSongsList.db')


def get_cache_db():
    return os.path.join(DATA_DIR, 'cache.db')


def get_chart_db(chart_id: int):
    return os.path.join(CHARTS_DIR, f'chart_{chart_id:03d}.db')


def get_nominations_db():
    return os.path.join(DATA_DIR, 'nominations.db')


def get_announcements_db():
    return os.path.join(DATA_DIR, 'announcements.db')


def create_all_songs_db(songs: list[dict]):
    db_path = get_all_songs_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS songs')
    c.execute('''
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY,
            bvid TEXT UNIQUE,
            pubtime INTEGER,
            title TEXT,
            title_cn TEXT,
            first_recorded_at INTEGER,
            producers TEXT,
            vocalists TEXT,
            peak_rank INTEGER,
            best_score INTEGER,
            latest_rank INTEGER,
            weeks_on_board INTEGER,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0,
            favorites INTEGER DEFAULT 0
        )
    ''')

    for song in songs:
        c.execute('''
            INSERT OR REPLACE INTO songs (id, bvid, pubtime, title, title_cn,
                first_recorded_at, producers, vocalists, peak_rank, best_score,
                latest_rank, weeks_on_board, views, likes, coins, favorites)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            song['id'], song.get('bvid', ''), song.get('pubtime', 0),
            song.get('title', ''), song.get('title_cn', ''),
            song.get('first_recorded_at', 0),
            ', '.join(p['name'] for p in song.get('producers', [])),
            ', '.join(v['name'] for v in song.get('vocalists', [])),
            song.get('peak_rank'), song.get('best_score'),
            song.get('latest_rank'), song.get('weeks_on_board'),
            song.get('views', 0), song.get('likes', 0),
            song.get('coins', 0), song.get('favorites', 0)
        ))

    conn.commit()
    conn.close()
    return db_path


def create_cache_db():
    db_path = get_cache_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS cache')
    c.execute('''
        CREATE TABLE cache (
            bvid TEXT PRIMARY KEY,
            title TEXT,
            name TEXT,
            cover_url TEXT,
            best_rank INTEGER,
            best_score INTEGER,
            times_in_top20 INTEGER DEFAULT 0,
            last_chart_id INTEGER,
            last_rank INTEGER,
            view INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            coin INTEGER DEFAULT 0,
            favorite INTEGER DEFAULT 0,
            danmaku INTEGER DEFAULT 0,
            reply INTEGER DEFAULT 0,
            share INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    return db_path


def update_cache_from_chart(chart_id: int, videos: list[dict]):
    cache_path = get_cache_db()
    conn = sqlite3.connect(cache_path)
    c = conn.cursor()

    for i, v in enumerate(videos):
        rank = i + 1
        bvid = v['bvid']
        existing = c.execute('SELECT best_rank, times_in_top20 FROM cache WHERE bvid = ?', (bvid,)).fetchone()

        if existing:
            best_rank = min(existing[0] or 999, rank)
            times = existing[1] + (1 if rank <= 20 else 0)
            c.execute('''
                UPDATE cache SET title=?, name=?, cover_url=?,
                    best_rank=?, best_score=MAX(best_score, ?),
                    times_in_top20=?, last_chart_id=?, last_rank=?,
                    view=?, like_count=?, coin=?, favorite=?,
                    danmaku=?, reply=?, share=?, updated_at=CURRENT_TIMESTAMP
                WHERE bvid=?
            ''', (v['title'], v['name'], v.get('cover_url', ''),
                  best_rank, v['score'], times, chart_id, rank,
                  v.get('view', 0), v.get('like_count', 0), v.get('coin', 0),
                  v.get('favorite', 0), v.get('danmaku', 0), v.get('reply', 0),
                  v.get('share', 0), bvid))
        else:
            times = 1 if rank <= 20 else 0
            c.execute('''
                INSERT INTO cache (bvid, title, name, cover_url, best_rank,
                    best_score, times_in_top20, last_chart_id, last_rank,
                    view, like_count, coin, favorite, danmaku, reply, share)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bvid, v['title'], v['name'], v.get('cover_url', ''),
                  rank, v['score'], times, chart_id, rank,
                  v.get('view', 0), v.get('like_count', 0), v.get('coin', 0),
                  v.get('favorite', 0), v.get('danmaku', 0), v.get('reply', 0),
                  v.get('share', 0)))

    conn.commit()
    conn.close()


def create_chart_db(chart_id: int, formula: str = 'normal'):
    db_path = get_chart_db(chart_id)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS videos')
    c.execute('''
        CREATE TABLE videos (
            rank INTEGER PRIMARY KEY,
            bvid TEXT,
            title TEXT,
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
            bilibili_url TEXT,
            pubdate TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('DROP TABLE IF EXISTS meta')
    c.execute('''
        CREATE TABLE meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute("INSERT INTO meta (key, value) VALUES ('formula', ?)", (formula,))
    c.execute("INSERT INTO meta (key, value) VALUES ('chart_id', ?)", (str(chart_id),))

    conn.commit()
    conn.close()
    return db_path


def insert_video_to_chart(chart_id: int, rank: int, video: dict):
    db_path = get_chart_db(chart_id)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    bilibili_url = f"https://www.bilibili.com/video/{video['bvid']}"
    c.execute('''
        INSERT OR REPLACE INTO videos (rank, bvid, title, name, view, danmaku,
            reply, favorite, coin, share, like_count, score, cover_url,
            bilibili_url, pubdate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        rank, video['bvid'], video['title'], video['name'],
        video.get('view', 0), video.get('danmaku', 0), video.get('reply', 0),
        video.get('favorite', 0), video.get('coin', 0), video.get('share', 0),
        video.get('like_count', 0), video.get('score', 0),
        video.get('cover_url', ''), bilibili_url, video.get('pubdate', '')
    ))

    conn.commit()
    conn.close()


def create_nominations_db():
    db_path = get_nominations_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS nominations')
    c.execute('''
        CREATE TABLE nominations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bvid TEXT UNIQUE,
            title TEXT,
            name TEXT,
            cover_url TEXT,
            status TEXT DEFAULT 'pending',
            score INTEGER,
            view INTEGER,
            like_count INTEGER,
            coin INTEGER,
            favorite INTEGER,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            reviewed_at TEXT
        )
    ''')

    conn.commit()
    conn.close()
    return db_path


def create_announcements_db():
    db_path = get_announcements_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS announcements')
    c.execute('''
        CREATE TABLE announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    return db_path


def get_list_of_charts():
    init_data_dir()
    charts = []
    if os.path.exists(CHARTS_DIR):
        for f in sorted(os.listdir(CHARTS_DIR)):
            if f.startswith('chart_') and f.endswith('.db'):
                chart_id = int(f.replace('chart_', '').replace('.db', ''))
                conn = sqlite3.connect(os.path.join(CHARTS_DIR, f))
                conn.row_factory = sqlite3.Row
                meta = {}
                for row in conn.execute('SELECT key, value FROM meta'):
                    meta[row['key']] = row['value']
                count = conn.execute('SELECT COUNT(*) FROM videos').fetchone()[0]
                conn.close()
                charts.append({
                    'id': chart_id,
                    'formula': meta.get('formula', 'unknown'),
                    'video_count': count
                })
    return charts
