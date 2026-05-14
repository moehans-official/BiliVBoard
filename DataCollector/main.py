import asyncio
import sys
import time
import httpx
from collector.utils import load_bvids
from collector.data_collector import collect_all_data
from collector.excel_handler import create_excel_report
from collector.db_handler import create_database

SERVERCHAN_URL = 'https://7487.push.ft07.com/send/sctp7487t1oar49wlwkey1s7owymazc.send'


def send_serverchan(title, desp):
    try:
        resp = httpx.post(SERVERCHAN_URL, data={'title': title, 'desp': desp}, timeout=10)
        print(f'ServerChan: {resp.json()}', flush=True)
    except Exception as e:
        print(f'ServerChan push failed: {e}', flush=True)


async def main():
    formula = 'normal'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['normal', 'radical', 'e_sp']:
            formula = sys.argv[1]

    print(f'使用公式: {formula}', flush=True)

    bvids = load_bvids()
    if not bvids:
        print('bvid.txt 中没有有效的 BV 号')
        return

    print(f'共 {len(bvids)} 个 BV 号待采集', flush=True)

    start_time = time.time()
    send_serverchan('BiliVBoard 采集开始', f'开始采集 {len(bvids)} 个视频\n公式: {formula}\n并发: 3\n延迟: 1s')

    results, stats = await collect_all_data(bvids, formula, concurrency=3)

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    if results:
        output_file = create_excel_report(results)
        db_file = create_database(results)
        print(f'\nExcel: {output_file}', flush=True)
        print(f'Database: {db_file}', flush=True)

    title = 'BiliVBoard 采集完成'
    desp = f"""## 采集结果

- **总数**: {len(bvids)}
- **成功**: {len(results)}
- **失败**: {stats['failed']}
- **耗时**: {minutes}分{seconds}秒
- **公式**: {formula}

### 数据库
- 路径: bilibili_video_data.db
- TOP1: {results[0]['title'] if results else 'N/A'} (score: {results[0]['score'] if results else 0})

### 失败列表
{chr(10).join(stats['failed_bvids'][:10]) if stats['failed_bvids'] else '无'}
"""

    send_serverchan(title, desp)
    print(f'\n总耗时: {minutes}分{seconds}秒', flush=True)


if __name__ == '__main__':
    asyncio.run(main())
