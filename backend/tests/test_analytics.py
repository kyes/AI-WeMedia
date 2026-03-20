"""Tests for analytics endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_dashboard(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/analytics/dashboard", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_followers" in data
    assert "weekly_views" in data
    assert "health_score" in data
    assert "growth_trend" in data
    assert "alerts" in data
    assert isinstance(data["platform_breakdown"], list)


@pytest.mark.asyncio
async def test_create_alert_rule(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/analytics/alerts", json={
        "name": "粉丝流失预警",
        "metric": "followers",
        "operator": "<",
        "threshold": 1000.0,
        "notification_channels": ["email"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "粉丝流失预警"
    assert data["metric"] == "followers"
    assert data["operator"] == "<"
    assert data["threshold"] == 1000.0
    return data["id"]


@pytest.mark.asyncio
async def test_list_alert_rules(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/analytics/alerts", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_delete_alert_rule(client: AsyncClient, auth_headers):
    # Create then delete
    create_resp = await client.post("/api/v1/analytics/alerts", json={
        "name": "临时预警",
        "metric": "views",
        "operator": ">",
        "threshold": 100000.0,
    }, headers=auth_headers)
    rule_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/analytics/alerts/{rule_id}", headers=auth_headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "预警规则已删除"


@pytest.mark.asyncio
async def test_alert_rule_invalid_operator(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/analytics/alerts", json={
        "name": "无效操作符",
        "metric": "followers",
        "operator": "INVALID",
        "threshold": 100.0,
    }, headers=auth_headers)
    assert resp.status_code == 422  # validation error
