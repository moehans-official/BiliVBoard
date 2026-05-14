import asyncio
import math
import os
import time
from datetime import datetime, timezone
from bilibili_api import video
import httpx
from .formulas import get_score_calculator
from .utils import truncate_score


async def get_video_data(bvid, formula='normal'):
    v = video.Video(bvid=bvid)
    info = await v.get_info()
    stat = info['stat']
    pubdate = datetime.fromtimestamp(info['pubdate'], tz=timezone.utc)

    score_calculator = get_score_calculator(formula)
    score = score_calculator(stat, pubdate)

    return {
        'bvid': bvid,
        'title': info['title'],
        'pubdate': pubdate.strftime('%Y-%m-%d %H:%M:%S'),
        'mid': info['owner']['mid'],
        'name': info['owner']['name'],
        'view': stat['view'],
        'danmaku': stat['danmaku'],
        'reply': stat['reply'],
        'favorite': stat['favorite'],
        'coin': stat['coin'],
        'share': stat['share'],
        'like': stat['like'],
        'score': truncate_score(score),
        'cover_url': info.get('pic', '')
    }


async def download_cover(cover_url, bvid, covers_dir='covers'):
    if not cover_url:
        return None

    os.makedirs(covers_dir, exist_ok=True)
    file_path = os.path.join(covers_dir, f'{bvid}.jpg')

    if os.path.exists(file_path):
        return file_path

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(cover_url, timeout=30)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
    except Exception as e:
        print(f'下载封面失败 {bvid}: {e}')
        return None


async def collect_one(bvid, formula, semaphore, stats, total):
    async with semaphore:
        try:
            data = await get_video_data(bvid, formula)
            cover_path = await download_cover(data['cover_url'], data['bvid'])
            data['cover_path'] = cover_path
            stats['done'] += 1
            print(f"[{stats['done']}/{total}] {data['bvid']}: {data['title'][:30]}... score={data['score']}", flush=True)
            return data
        except Exception as e:
            stats['failed'] += 1
            stats['failed_bvids'].append(bvid)
            print(f"[{stats['done'] + stats['failed']}/{total}] FAILED {bvid}: {e}", flush=True)
            return None
        finally:
            await asyncio.sleep(1)


async def collect_all_data(bvids, formula='normal', concurrency=3):
    semaphore = asyncio.Semaphore(concurrency)
    stats = {'done': 0, 'failed': 0, 'failed_bvids': []}
    total = len(bvids)

    tasks = [collect_one(bvid, formula, semaphore, stats, total) for bvid in bvids]
    results = await asyncio.gather(*tasks)

    valid = [r for r in results if r is not None]
    print(f'\n完成: {len(valid)} 成功, {stats["failed"]} 失败', flush=True)
    if stats['failed_bvids']:
        print(f'失败的 BV号: {stats["failed_bvids"][:20]}...', flush=True)

    return valid, stats
