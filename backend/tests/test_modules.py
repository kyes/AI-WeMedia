"""Tests for monetization, distribution, AI, and workflow endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


# ─── Monetization ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_revenue_summary(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/monetization/revenue", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_channel" in data
    assert "monthly_trend" in data


@pytest.mark.asyncio
async def test_create_commercial_order(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/monetization/orders", json={
        "brand_name": "某护肤品牌",
        "order_type": "种草",
        "amount": 5000.0,
        "platform": "xiaohongshu",
        "requirements": "发布一篇护肤成分种草笔记",
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["brand_name"] == "某护肤品牌"
    assert data["status"] == "matched"
    return data["id"]


@pytest.mark.asyncio
async def test_update_order_status(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/monetization/orders", json={
        "brand_name": "测试品牌",
        "order_type": "广告",
    }, headers=auth_headers)
    order_id = create_resp.json()["id"]

    resp = await client.put(f"/api/v1/monetization/orders/{order_id}", json={
        "status": "in_progress",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_list_orders(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/monetization/orders", headers=auth_headers)
    assert resp.status_code == 200
    assert "items" in resp.json()


# ─── Distribution ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_best_publish_time(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/distribution/best-time", json={
        "account_id": "dummy-account-id",
        "platform": "douyin",
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["platform"] == "douyin"
    assert len(data["recommended_times"]) > 0
    assert len(data["heat_scores"]) == len(data["recommended_times"])


@pytest.mark.asyncio
async def test_list_publish_tasks(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/distribution/tasks", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ─── AI Support ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_prompts(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/ai/prompts", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_prompt_template(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/ai/prompts", json={
        "name": "小红书种草文案模板",
        "scene": "content",
        "template": "请为{product}写一篇{style}风格的小红书种草笔记，字数{word_count}字左右。",
        "variables": [
            {"name": "product", "description": "商品名称"},
            {"name": "style", "description": "内容风格"},
            {"name": "word_count", "description": "字数", "default": "500"},
        ],
        "is_public": True,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "小红书种草文案模板"
    assert data["scene"] == "content"
    return data["id"]


@pytest.mark.asyncio
async def test_delete_prompt_template(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/ai/prompts", json={
        "name": "临时模板",
        "scene": "topic",
        "template": "请为{domain}生成选题",
    }, headers=auth_headers)
    tmpl_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/ai/prompts/{tmpl_id}", headers=auth_headers)
    assert del_resp.status_code == 200


# ─── Workflow ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_workflow(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/workflows", json={
        "name": "新粉欢迎私信",
        "description": "粉丝新增时自动发送欢迎私信",
        "trigger_type": "event",
        "trigger_config": {"event": "new_follower"},
        "action_type": "send_dm",
        "action_config": {
            "template": "欢迎关注！我是{account_name}，专注分享平价护肤干货。",
        },
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "新粉欢迎私信"
    assert data["is_active"] is True
    return data["id"]


@pytest.mark.asyncio
async def test_toggle_workflow(client: AsyncClient, auth_headers):
    create_resp = await client.post("/api/v1/workflows", json={
        "name": "切换测试工作流",
        "trigger_type": "schedule",
        "trigger_config": {"cron": "0 9 * * 1"},
        "action_type": "generate_report",
        "action_config": {"report_type": "weekly"},
    }, headers=auth_headers)
    rule_id = create_resp.json()["id"]

    resp = await client.patch(f"/api/v1/workflows/{rule_id}/toggle", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False  # toggled off


@pytest.mark.asyncio
async def test_list_workflows(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/workflows", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
