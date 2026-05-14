import json
import sqlite3
import os

API_URL = 'https://wwe.ldmkc.cn/api/o/736579'
DB_PATH = os.path.join(os.path.dirname(__file__), 'DataCollector', 'bilibili_video_data.db')
SONGS_JSON = 'songs.json'


def fetch_songs():
    import urllib.request
    print('Fetching songs from API...', flush=True)
    req = urllib.request.Request(API_URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    print(f'Fetched {len(data)} songs', flush=True)
    return data


def save_json(songs, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print(f'Saved to {path}', flush=True)


def create_db(songs, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS songs')
    c.execute('''
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY,
            bvid TEXT,
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

    c.execute('DROP TABLE IF EXISTS rank_history')
    c.execute('''
        CREATE TABLE rank_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER,
            board_id INTEGER,
            board_name TEXT,
            issue_id INTEGER,
            issue_year INTEGER,
            issue_week INTEGER,
            rank INTEGER,
            bvid TEXT,
            title TEXT,
            title_cn TEXT,
            pubtime INTEGER,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0,
            favorites INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            last_rank INTEGER,
            weeks_on_board INTEGER,
            peak_rank INTEGER,
            score_ratio_text TEXT,
            special_status TEXT,
            time_correction REAL,
            is_annual INTEGER,
            issue_end_date INTEGER,
            FOREIGN KEY (song_id) REFERENCES songs(id)
        )
    ''')

    for song in songs:
        producers_str = ', '.join(p['name'] for p in song.get('producers', []))
        vocalists_str = ', '.join(v['name'] for v in song.get('vocalists', []))

        rank_history = song.get('rank_history', [])
        peak_rank = None
        best_score = None
        latest_rank = None
        total_weeks = 0
        total_views = 0
        total_likes = 0
        total_coins = 0
        total_favorites = 0

        for rh in rank_history:
            stats = rh.get('stats', {})
            r = rh.get('rank')
            s = stats.get('score', 0)
            if r is not None:
                if peak_rank is None or r < peak_rank:
                    peak_rank = r
            if s > 0:
                if best_score is None or s > best_score:
                    best_score = s
            if rh.get('weeks_on_board'):
                total_weeks = max(total_weeks, rh['weeks_on_board'])
            total_views = max(total_views, stats.get('views', 0))
            total_likes = max(total_likes, stats.get('likes', 0))
            total_coins = max(total_coins, stats.get('coins', 0))
            total_favorites = max(total_favorites, stats.get('favorites', 0))

        if rank_history:
            latest = rank_history[-1]
            latest_rank = latest.get('rank')

        c.execute('''
            INSERT INTO songs (id, bvid, pubtime, title, title_cn, first_recorded_at,
                             producers, vocalists, peak_rank, best_score, latest_rank,
                             weeks_on_board, views, likes, coins, favorites)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            song['id'], song.get('bvid', ''), song.get('pubtime', 0),
            song.get('title', ''), song.get('title_cn', ''), song.get('first_recorded_at', 0),
            producers_str, vocalists_str, peak_rank, best_score, latest_rank,
            total_weeks, total_views, total_likes, total_coins, total_favorites
        ))

        for rh in rank_history:
            stats = rh.get('stats', {})
            c.execute('''
                INSERT INTO rank_history (song_id, board_id, board_name, issue_id, issue_year,
                                        issue_week, rank, bvid, title, title_cn, pubtime,
                                        views, likes, coins, favorites, score,
                                        last_rank, weeks_on_board, peak_rank,
                                        score_ratio_text, special_status, time_correction,
                                        is_annual, issue_end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                song['id'], rh.get('board_id'), rh.get('board_name'),
                rh.get('issue_id'), rh.get('issue_year'), rh.get('issue_week'),
                rh.get('rank'), rh.get('bvid', ''), rh.get('title', ''),
                rh.get('title_cn', ''), rh.get('pubtime', 0),
                stats.get('views', 0), stats.get('likes', 0),
                stats.get('coins', 0), stats.get('favorites', 0), stats.get('score', 0),
                rh.get('last_rank'), rh.get('weeks_on_board'), rh.get('peak_rank'),
                rh.get('score_ratio_text'), rh.get('special_status'),
                rh.get('time_correction', 1.0), rh.get('is_annual', False),
                rh.get('issue_end_date')
            ))

    conn.commit()
    conn.close()
    print(f'Database created at {db_path}', flush=True)


def main():
    songs = fetch_songs()
    save_json(songs, SONGS_JSON)
    create_db(songs, DB_PATH)
    print('Done!', flush=True)


if __name__ == '__main__':
    main()
