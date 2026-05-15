import re
import sqlite3
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import get_rankings, get_video_detail, get_period_info, get_total_count
from db_schema import (
    init_data_dir, get_cache_db, get_chart_db, get_nominations_db,
    get_announcements_db, create_cache_db, create_chart_db,
    create_nominations_db, create_announcements_db, get_list_of_charts
)
from admin.charts import list_charts, get_chart, get_cache_top
from admin.nominations import (
    list_nominations, get_nomination, add_nomination,
    parse_nomination, review_nomination, delete_nomination
)
from admin.announcements import (
    list_announcements, get_announcement, add_announcement,
    update_announcement, delete_announcement
)

app = FastAPI(title='BiliVBoard API', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup():
    init_data_dir()
    create_cache_db()
    create_nominations_db()
    create_announcements_db()


BV_PATTERN = re.compile(r'^BV[a-zA-Z0-9]{10,}$')


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
    reason: str = ''


class NominationResponse(BaseModel):
    success: bool
    message: str
    id: int | None = None


class AnnouncementItem(BaseModel):
    id: int
    title: str
    content: str
    is_active: int
    created_at: str


class AnnouncementCreate(BaseModel):
    title: str
    content: str = ''


class AnnouncementUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_active: int | None = None


class ChartItem(BaseModel):
    id: int
    formula: str
    video_count: int


class NominationItem(BaseModel):
    id: int
    bvid: str
    title: str | None = None
    name: str | None = None
    cover_url: str | None = None
    status: str
    score: int | None = None
    view: int | None = None
    like_count: int | None = None
    coin: int | None = None
    favorite: int | None = None
    reason: str | None = None
    created_at: str
    reviewed_at: str | None = None


class ReviewRequest(BaseModel):
    status: str
    reason: str = ''


# ── Public API ──


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
    if not BV_PATTERN.match(bvid):
        raise HTTPException(status_code=400, detail='无效的BV号格式')
    nom_id = add_nomination(bvid, req.reason)
    if nom_id is None:
        raise HTTPException(status_code=409, detail='该BV号已被提名过')
    return NominationResponse(success=True, message='提名已提交，等待审核', id=nom_id)


@app.get('/api/announcements', response_model=list[AnnouncementItem])
async def get_active_announcements():
    return list_announcements(active_only=True)


@app.get('/api/health')
async def health():
    return {'status': 'ok'}


# ── Admin: Charts ──


@app.get('/api/admin/charts', response_model=list[ChartItem])
async def admin_list_charts():
    return list_charts()


@app.get('/api/admin/charts/{chart_id}')
async def admin_get_chart(chart_id: int):
    data = get_chart(chart_id)
    if data is None:
        raise HTTPException(status_code=404, detail='榜单不存在')
    return data


@app.get('/api/admin/cache/top')
async def admin_cache_top(limit: int = Query(default=1000, ge=1, le=5000)):
    return get_cache_top(limit)


# ── Admin: Announcements ──


@app.get('/api/admin/announcements', response_model=list[AnnouncementItem])
async def admin_list_announcements():
    return list_announcements(active_only=False)


@app.post('/api/admin/announcements', response_model=AnnouncementItem)
async def admin_create_announcement(req: AnnouncementCreate):
    ann_id = add_announcement(req.title, req.content)
    return get_announcement(ann_id)


@app.put('/api/admin/announcements/{ann_id}')
async def admin_update_announcement(ann_id: int, req: AnnouncementUpdate):
    existing = get_announcement(ann_id)
    if not existing:
        raise HTTPException(status_code=404, detail='公告不存在')
    update_announcement(ann_id, title=req.title, content=req.content, is_active=req.is_active)
    return get_announcement(ann_id)


@app.delete('/api/admin/announcements/{ann_id}')
async def admin_delete_announcement(ann_id: int):
    existing = get_announcement(ann_id)
    if not existing:
        raise HTTPException(status_code=404, detail='公告不存在')
    delete_announcement(ann_id)
    return {'success': True}


# ── Admin: Nominations ──


@app.get('/api/admin/nominations', response_model=list[NominationItem])
async def admin_list_nominations(status: str = Query(default=None)):
    return list_nominations(status=status)


@app.get('/api/admin/nominations/{nom_id}', response_model=NominationItem)
async def admin_get_nomination(nom_id: int):
    item = get_nomination(nom_id)
    if not item:
        raise HTTPException(status_code=404, detail='提名不存在')
    return item


@app.post('/api/admin/nominations/{nom_id}/parse')
async def admin_parse_nomination(nom_id: int):
    item = get_nomination(nom_id)
    if not item:
        raise HTTPException(status_code=404, detail='提名不存在')
    parse_nomination(nom_id)
    return get_nomination(nom_id)


@app.put('/api/admin/nominations/{nom_id}/review')
async def admin_review_nomination(nom_id: int, req: ReviewRequest):
    item = get_nomination(nom_id)
    if not item:
        raise HTTPException(status_code=404, detail='提名不存在')
    if req.status not in ('approved', 'rejected'):
        raise HTTPException(status_code=400, detail='status 必须是 approved 或 rejected')
    review_nomination(nom_id, req.status, req.reason)
    return get_nomination(nom_id)


@app.delete('/api/admin/nominations/{nom_id}')
async def admin_delete_nomination(nom_id: int):
    item = get_nomination(nom_id)
    if not item:
        raise HTTPException(status_code=404, detail='提名不存在')
    delete_nomination(nom_id)
    return {'success': True}
