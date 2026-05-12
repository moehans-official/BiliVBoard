import asyncio
import math
import os
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
    
    # 使用选择的公式计算评分
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
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(cover_url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
    except Exception as e:
        print(f'下载封面失败 {bvid}: {e}')
        return None


async def collect_all_data(bvids, formula='normal'):
    tasks = [get_video_data(bvid, formula) for bvid in bvids]
    results = await asyncio.gather(*tasks)
    
    cover_tasks = [download_cover(data['cover_url'], data['bvid']) for data in results]
    cover_paths = await asyncio.gather(*cover_tasks)
    
    for data, cover_path in zip(results, cover_paths):
        data['cover_path'] = cover_path
    
    return results
