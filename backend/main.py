from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import get_rankings, get_video_detail, get_period_info, get_total_count

app = FastAPI(title='BiliVBoard API', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


class VideoItem(BaseModel):
    rank: int
    bvid: str
    title: str
    name: str
    view: int
    danmaku: int
    reply: int
    favorite: int
    coin: int
    share: int
    like_count: int
    score: int
    cover_url: str
    cover_path: str | None = None
    bilibili_url: str


class VideoDetail(VideoItem):
    pubdate: str | None = None
    mid: int | None = None


class RankingsResponse(BaseModel):
    items: list[VideoItem]
    total: int
    period: dict | None = None


class NominationRequest(BaseModel):
    bvid: str


class NominationResponse(BaseModel):
    success: bool
    message: str


@app.get('/api/rankings', response_model=RankingsResponse)
async def rankings(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = get_rankings(limit, offset)
    total = get_total_count()
    period = get_period_info()
    return RankingsResponse(items=items, total=total, period=period)


@app.get('/api/rankings/{bvid}', response_model=VideoDetail)
async def video_detail(bvid: str):
    item = get_video_detail(bvid)
    if not item:
        raise HTTPException(status_code=404, detail='视频不存在')
    return item


@app.post('/api/nominations', response_model=NominationResponse)
async def nominate(req: NominationRequest):
    bvid = req.bvid.strip()
    if not bvid:
        raise HTTPException(status_code=400, detail='BV号不能为空')
    if not bvid.startswith('BV') or len(bvid) < 10:
        raise HTTPException(status_code=400, detail='无效的BV号格式')
    return NominationResponse(success=True, message=f'{bvid} 提交成功')


@app.get('/api/health')
async def health():
    return {'status': 'ok'}
