"""Tests for topics and content endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_topics_empty(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/topics", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 0
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_create_topic(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/topics", json={
        "title": "2026年最值得入手的平价护肤成分",
        "description": "聚焦敏感肌用户的平价护肤成分科普",
        "tags": ["护肤", "平价", "成分党"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "2026年最值得入手的平价护肤成分"
    assert data["status"] == "pending"
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_get_topic(client: AsyncClient, auth_headers):
    # Create first
    create_resp = await client.post("/api/v1/topics", json={
        "title": "春季护肤全攻略",
        "tags": ["护肤", "春季"],
    }, headers=auth_headers)
    topic_id = create_resp.json()["id"]

    # Get
    resp = await client.get(f"/api/v1/topics/{topic_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == topic_id


@pytest.mark.asyncio
async def test_update_topic_status(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/topics", json={
        "title": "状态更新测试选题",
    }, headers=auth_headers)
    topic_id = create_resp.json()["id"]

    resp = await client.patch(
        f"/api/v1/topics/{topic_id}/status",
        params={"status": "confirmed"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_topic_not_found(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/topics/nonexistent-id", headers=auth_headers)
    assert resp.status_code == 404


# ─── Content tests ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_content(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/contents", json={
        "title": "素人护肤博主必看！这6个平价护肤成分",
        "body": "大家好，今天分享护肤干货...",
        "content_type": "article",
        "platform": "xiaohongshu",
        "style": "专业干货",
        "tags": ["护肤", "成分"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"].startswith("素人护肤博主")
    assert data["status"] == "draft"
    assert data["platform"] == "xiaohongshu"


@pytest.mark.asyncio
async def test_list_contents(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/contents", headers=auth_headers)
    assert resp.status_code == 200
    assert "items" in resp.json()


@pytest.mark.asyncio
async def test_update_content(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/contents", json={
        "title": "原始标题",
        "platform": "douyin",
    }, headers=auth_headers)
    content_id = create_resp.json()["id"]

    resp = await client.put(f"/api/v1/contents/{content_id}", json={
        "title": "更新后的标题",
        "status": "in_review",
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "更新后的标题"
    assert data["status"] == "in_review"


@pytest.mark.asyncio
async def test_delete_content(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/contents", json={
        "title": "待删除内容",
        "platform": "wechat",
    }, headers=auth_headers)
    content_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/contents/{content_id}", headers=auth_headers)
    assert del_resp.status_code == 200

    get_resp = await client.get(f"/api/v1/contents/{content_id}", headers=auth_headers)
    assert get_resp.status_code == 404
