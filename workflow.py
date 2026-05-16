#!/usr/bin/env python3
"""
BiliVBoard 自动化视频生成工作流 v2
- 读取 chart 数据库 TOP20
- 生成排名卡片
- 用 ffmpeg 直接拼接视频（快速）
- 生成视频封面
"""

import os
import sys
import sqlite3
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from datetime import datetime

# ============================================================
# 配置
# ============================================================
DB_PATH = "data/charts/chart_001.db"
VIDEO_DIR = "output"
OUTPUT_DIR = "output_video"
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 24
CARD_DURATION = 3  # 排名卡片显示秒数

# 颜色
BG = (18, 18, 18)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLUE = (88, 166, 255)

# ============================================================
# 工具函数
# ============================================================

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def fmt_num(n):
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)

def download_cover(url):
    try:
        r = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.bilibili.com/'
        })
        if r.status_code == 200:
            return Image.open(BytesIO(r.content)).convert('RGB')
    except:
        pass
    return None

# ============================================================
# 1. 读取数据库
# ============================================================

def load_data(db_path, n=20):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT rank, bvid, title, name, view, like_count, coin, favorite, score, cover_url
        FROM videos ORDER BY rank LIMIT ?
    """, (n,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    print(f"[1/4] 读取 {len(rows)} 条数据")
    return rows

# ============================================================
# 2. 生成排名卡片
# ============================================================

def gen_cards(data, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cards = []

    for item in data:
        rank = item['rank']
        title = item['title']
        name = item['name']
        score = item['score']
        view = item['view']
        like = item['like_count']
        coin = item['coin']
        fav = item['favorite']
        cover_url = item['cover_url']

        img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG)

        cover = download_cover(cover_url)
        if cover:
            ratio = cover.width / cover.height
            h = VIDEO_HEIGHT
            w = int(h * ratio)
            cover = cover.resize((w, h), Image.LANCZOS)
            left = (w - VIDEO_WIDTH) // 2
            cover = cover.crop((left, 0, left + VIDEO_WIDTH, VIDEO_HEIGHT))
            overlay = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0))
            img = Image.blend(cover, overlay, 0.75)

        draw = ImageDraw.Draw(img)

        # 排名
        draw.text((80, 30), f"#{rank}", font=load_font(200), fill=BLUE)
        draw.rectangle([(80, 250), (VIDEO_WIDTH-80, 253)], fill=BLUE)

        # 标题
        t = title if len(title) <= 25 else title[:24] + "..."
        draw.text((80, 290), t, font=load_font(64), fill=WHITE)
        draw.text((80, 380), f"UP主: {name}", font=load_font(36), fill=GRAY)

        # 指标
        metrics = [("播放", fmt_num(view)), ("点赞", fmt_num(like)),
                   ("投币", fmt_num(coin)), ("收藏", fmt_num(fav))]
        for i, (label, val) in enumerate(metrics):
            x = 80 + i * 420
            draw.text((x, 480), val, font=load_font(40), fill=WHITE)
            draw.text((x, 530), label, font=load_font(28), fill=GRAY)

        # 得分
        draw.text((80, VIDEO_HEIGHT-180), "得分", font=load_font(28), fill=GRAY)
        draw.text((80, VIDEO_HEIGHT-140), f"{score:,}", font=load_font(72), fill=BLUE)

        path = os.path.join(out_dir, f"card_{rank:02d}.png")
        img.save(path, quality=95)
        cards.append(path)
        print(f"  卡片 #{rank}: {title[:20]}...")

    print(f"[2/4] 生成 {len(cards)} 张卡片")
    return cards

# ============================================================
# 3. 用 ffmpeg 拼接视频
# ============================================================

def build_video(data, video_dir, card_dir, output_path):
    """生成每段：卡片转视频 + 原视频，然后拼接"""
    segments = []
    concat_list = os.path.join(OUTPUT_DIR, "concat.txt")

    for item in data:
        rank = item['rank']
        bvid = item['bvid']
        title = item['title']

        video_path = os.path.join(video_dir, f"#{rank}_{bvid}.mp4")
        card_path = os.path.join(card_dir, f"card_{rank:02d}.png")

        if not os.path.exists(video_path):
            print(f"  [SKIP] 视频不存在: #{rank}")
            continue
        if not os.path.exists(card_path):
            print(f"  [SKIP] 卡片不存在: #{rank}")
            continue

        print(f"  处理 #{rank}: {title[:20]}...")

        # 1) 卡片转视频片段
        card_mp4 = os.path.join(OUTPUT_DIR, f"seg_card_{rank:02d}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", card_path,
            "-c:v", "libx264", "-t", str(CARD_DURATION),
            "-pix_fmt", "yuv420p", "-r", str(VIDEO_FPS),
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}",
            "-preset", "ultrafast", "-an",
            card_mp4
        ], capture_output=True)
        segments.append(card_mp4)

        # 2) 截取原视频前 30 秒
        clip_mp4 = os.path.join(OUTPUT_DIR, f"seg_clip_{rank:02d}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-t", "30",
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-r", str(VIDEO_FPS),
            clip_mp4
        ], capture_output=True)
        segments.append(clip_mp4)

    # 3) 拼接所有片段
    with open(concat_list, 'w') as f:
        for seg in segments:
            f.write(f"file '{os.path.abspath(seg)}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy", output_path
    ], capture_output=True)

    # 清理临时文件
    for seg in segments:
        try:
            os.remove(seg)
        except:
            pass
    try:
        os.remove(concat_list)
    except:
        pass

    print(f"[3/4] 视频生成: {output_path}")
    return output_path

# ============================================================
# 4. 生成封面
# ============================================================

def gen_cover(data, card_dir, output_path):
    top1 = data[0]
    cover = download_cover(top1['cover_url'])
    if not cover:
        cover = Image.open(os.path.join(card_dir, "card_01.png")).convert('RGB')

    cover = cover.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.LANCZOS)
    blurred = cover.filter(ImageFilter.GaussianBlur(radius=20))

    overlay = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 120))
    blurred = blurred.convert('RGBA')
    img = Image.alpha_composite(blurred, overlay)
    draw = ImageDraw.Draw(img)

    now = datetime.now().strftime("%Y年%m月%d日")
    draw.text((VIDEO_WIDTH//2-400, 100), "BiliVBoard 术力口周榜", font=load_font(80), fill=WHITE)
    draw.text((VIDEO_WIDTH//2-150, 210), now, font=load_font(40), fill=GRAY)
    draw.rectangle([(200, 280), (VIDEO_WIDTH-200, 283)], fill=BLUE)

    y = 320
    for i, item in enumerate(data[:5]):
        t = f"#{item['rank']}  {item['title']}"
        if len(t) > 40:
            t = t[:39] + "..."
        color = BLUE if i == 0 else WHITE
        draw.text((200, y), t, font=load_font(32), fill=color)
        y += 55

    draw.text((200, VIDEO_HEIGHT-120), "TOP20 完整榜单视频", font=load_font(32), fill=GRAY)

    img.convert('RGB').save(output_path, quality=95)
    print(f"[4/4] 封面: {output_path}")

# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 60)
    print("BiliVBoard 自动化视频生成 v2 (ffmpeg)")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    card_dir = os.path.join(OUTPUT_DIR, "cards")

    data = load_data(DB_PATH)
    if not data:
        print("数据库为空")
        sys.exit(1)

    gen_cards(data, card_dir)

    today = datetime.now().strftime("%Y%m%d")
    video_path = os.path.join(OUTPUT_DIR, f"BiliVBoard_TOP20_{today}.mp4")
    build_video(data, VIDEO_DIR, card_dir, video_path)

    cover_path = os.path.join(OUTPUT_DIR, f"cover_{today}.png")
    gen_cover(data, card_dir, cover_path)

    print("=" * 60)
    print("完成!")
    print(f"  视频: {video_path}")
    print(f"  封面: {cover_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
