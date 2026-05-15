import asyncio
import os
import sqlite3
import sys
from pathlib import Path

from bilibili_api import video, Credential, HEADERS, get_client

CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'charts')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
TOP_N = 20
FFMPEG_PATH = 'ffmpeg'

SESSDATA = ''


def get_latest_chart_db():
    if not os.path.exists(CHARTS_DIR):
        print(f'Charts directory not found: {CHARTS_DIR}')
        return None
    charts = sorted([f for f in os.listdir(CHARTS_DIR) if f.startswith('chart_') and f.endswith('.db')])
    if not charts:
        print('No chart databases found')
        return None
    return os.path.join(CHARTS_DIR, charts[-1])


def get_top_videos(db_path, limit=TOP_N):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('''
        SELECT rank, bvid, title
        FROM videos
        ORDER BY rank ASC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


async def download_stream(url: str, out: str, intro: str):
    dwn_id = await get_client().download_create(url, HEADERS)
    bts = 0
    tot = get_client().download_content_length(dwn_id)
    with open(out, 'wb') as file:
        while True:
            chunk = await get_client().download_chunk(dwn_id)
            bts += file.write(chunk)
            pct = bts * 100 // tot if tot > 0 else 0
            print(f'\r  {intro}: {pct}% ({bts}/{tot})', end='', flush=True)
            if bts == tot:
                break
    print()


async def download_video(bvid: str, rank: int, output_dir: str, credential: Credential = None) -> bool:
    filename = f'#{rank}_{bvid}.mp4'
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f'  [SKIP] Already exists: {filename}')
        return True

    v = video.Video(bvid=bvid, credential=credential)

    try:
        url_data = await v.get_download_url(page_index=0)
    except Exception as e:
        print(f'  [FAIL] Cannot get download URL: {e}')
        return False

    detecter = video.VideoDownloadURLDataDetecter(data=url_data)
    streams = detecter.detect_best_streams(
        video_max_quality=video.VideoQuality._1080P,
        no_dolby_video=True,
        no_dolby_audio=True,
        no_hdr=True,
        no_hires=True,
    )

    video_temp = os.path.join(output_dir, f'_video_{bvid}.m4s')
    audio_temp = os.path.join(output_dir, f'_audio_{bvid}.m4s')

    try:
        if detecter.check_video_and_audio_stream():
            if streams[0] is None or streams[1] is None:
                print(f'  [FAIL] No suitable stream found')
                return False

            print(f'  Quality: {streams[0].video_quality}')
            await download_stream(streams[0].url, video_temp, 'Video')
            await download_stream(streams[1].url, audio_temp, 'Audio')

            cmd = [
                FFMPEG_PATH, '-y',
                '-i', video_temp,
                '-i', audio_temp,
                '-vcodec', 'copy',
                '-acodec', 'copy',
                filepath
            ]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()

            for f in [video_temp, audio_temp]:
                if os.path.exists(f):
                    os.remove(f)

            if proc.returncode == 0 and os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / 1024 / 1024
                print(f'  [OK] {filename} ({size_mb:.1f} MB)')
                return True
            else:
                print(f'  [FAIL] FFmpeg merge failed')
                return False
        else:
            flv_temp = os.path.join(output_dir, f'_flv_{bvid}.flv')
            await download_stream(streams[0].url, flv_temp, 'FLV')

            cmd = [FFMPEG_PATH, '-y', '-i', flv_temp, filepath]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()

            if os.path.exists(flv_temp):
                os.remove(flv_temp)

            if proc.returncode == 0 and os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / 1024 / 1024
                print(f'  [OK] {filename} ({size_mb:.1f} MB)')
                return True
            else:
                print(f'  [FAIL] FLV conversion failed')
                return False

    except Exception as e:
        print(f'  [ERROR] {e}')
        for f in [video_temp, audio_temp]:
            if os.path.exists(f):
                os.remove(f)
        return False


async def main():
    db_path = get_latest_chart_db()
    if not db_path:
        print('No chart database found. Run start_make.py first.')
        sys.exit(1)

    print(f'Using chart database: {db_path}')

    videos = get_top_videos(db_path, TOP_N)
    if not videos:
        print('No videos found in chart database')
        sys.exit(1)

    print(f'Found {len(videos)} videos to download')

    credential = None
    if SESSDATA:
        credential = Credential(sessdata=SESSDATA)
        print(f'Using SESSDATA: {SESSDATA[:10]}...')
    else:
        print('Warning: No SESSDATA provided, quality limited to 480P')

    print()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    success = 0
    failed = 0

    for v in videos:
        rank = v['rank']
        bvid = v['bvid']
        title = v['title'][:50]
        print(f'[{rank}/{len(videos)}] {title}')
        print(f'  BVID: {bvid}')

        if await download_video(bvid, rank, OUTPUT_DIR, credential):
            success += 1
        else:
            failed += 1
        print()

    print(f'{"="*50}')
    print(f'Done: {success} success, {failed} failed')
    print(f'Output: {OUTPUT_DIR}')


if __name__ == '__main__':
    asyncio.run(main())
