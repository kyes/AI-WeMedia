"""Content & topic business logic service."""
from __future__ import annotations

import random
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models import (
    Content,
    ContentStatus,
    PlatformType,
    SocialAccount,
    Topic,
    TopicStatus,
)
from app.schemas import (
    ContentAdaptRequest,
    ContentCreate,
    ContentGenerateRequest,
    ContentUpdate,
    TopicCreate,
    TopicGenerateRequest,
)
from app.services.ai_service import AIService

_ai = AIService()


class TopicService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_topics(
        self,
        user_id: str,
        account_id: str | None = None,
        status: TopicStatus | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Topic], int]:
        query = select(Topic).where(Topic.creator_id == user_id)
        if account_id:
            query = query.where(Topic.account_id == account_id)
        if status:
            query = query.where(Topic.status == status)
        total_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(total_q)).scalar_one()
        query = query.order_by(Topic.composite_score.desc()).offset((page - 1) * page_size).limit(page_size)
        results = await self.db.execute(query)
        return list(results.scalars()), total

    async def create_topic(self, user_id: str, data: TopicCreate) -> Topic:
        topic = Topic(
            creator_id=user_id,
            account_id=data.account_id,
            title=data.title,
            description=data.description,
            tags=data.tags,
            scheduled_date=data.scheduled_date,
        )
        self.db.add(topic)
        await self.db.flush()
        return topic

    async def generate_ai_topics(
        self, user_id: str, data: TopicGenerateRequest
    ) -> list[Topic]:
        """Generate topics using AI, persist and return them."""
        account_result = await self.db.execute(
            select(SocialAccount).where(SocialAccount.id == data.account_id)
        )
        account = account_result.scalar_one_or_none()
        positioning = account.positioning if account else {}

        raw_topics = await _ai.generate_topics(
            account_positioning=positioning or {},
            count=data.count,
            sources=data.sources,
            keywords=data.custom_keywords,
        )

        topics: list[Topic] = []
        for rt in raw_topics:
            topic = Topic(
                creator_id=user_id,
                account_id=data.account_id,
                title=rt.get("title", "未命名选题"),
                description=rt.get("description"),
                tags=rt.get("tags", []),
                source="AI生成",
                # Scores: assign weighted randoms as placeholder (real: from scoring model)
                heat_score=round(random.uniform(60, 95), 1),
                competition_score=round(random.uniform(20, 70), 1),
                match_score=round(random.uniform(70, 100), 1),
                commercial_score=round(random.uniform(60, 95), 1),
            )
            topic.composite_score = round(
                topic.heat_score * 0.35
                + (100 - topic.competition_score) * 0.20
                + topic.match_score * 0.30
                + topic.commercial_score * 0.15,
                1,
            )
            topic.predicted_views_min = int(topic.heat_score * 1500)
            topic.predicted_views_max = int(topic.heat_score * 2500)
            topic.predicted_engagement_rate = round(random.uniform(3.5, 8.5), 2)
            self.db.add(topic)
            topics.append(topic)

        await self.db.flush()
        return topics

    async def get_topic(self, topic_id: str, user_id: str) -> Topic:
        result = await self.db.execute(
            select(Topic).where(Topic.id == topic_id, Topic.creator_id == user_id)
        )
        topic = result.scalar_one_or_none()
        if not topic:
            raise NotFoundError("Topic not found")
        return topic

    async def update_status(
        self, topic_id: str, user_id: str, status: TopicStatus
    ) -> Topic:
        topic = await self.get_topic(topic_id, user_id)
        topic.status = status
        await self.db.flush()
        return topic


class ContentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_contents(
        self,
        user_id: str,
        status: ContentStatus | None = None,
        platform: PlatformType | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Content], int]:
        query = select(Content).where(Content.creator_id == user_id)
        if status:
            query = query.where(Content.status == status)
        if platform:
            query = query.where(Content.platform == platform)
        total_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(total_q)).scalar_one()
        query = query.order_by(Content.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        results = await self.db.execute(query)
        return list(results.scalars()), total

    async def create_content(self, user_id: str, data: ContentCreate) -> Content:
        content = Content(
            creator_id=user_id,
            topic_id=data.topic_id,
            account_id=data.account_id,
            title=data.title,
            body=data.body,
            content_type=data.content_type,
            platform=data.platform,
            style=data.style,
            tags=data.tags,
        )
        self.db.add(content)
        await self.db.flush()
        return content

    async def generate_ai_content(
        self, user_id: str, data: ContentGenerateRequest
    ) -> Content:
        """Generate content with AI, run compliance check, persist."""
        topic_text = ""
        if data.topic_id:
            res = await self.db.execute(select(Topic).where(Topic.id == data.topic_id))
            topic = res.scalar_one_or_none()
            topic_text = topic.title if topic else ""
        else:
            topic_text = data.custom_topic or ""

        raw = await _ai.generate_content(
            topic=topic_text,
            platform=data.platform.value,
            style=data.style,
            word_count=data.word_count,
        )
        # Parse title / body from AI output
        raw_text: str = raw.get("raw", "")
        title, body = self._parse_ai_output(raw_text, topic_text)

        # Compliance check
        compliance = await _ai.check_compliance(body)

        content = Content(
            creator_id=user_id,
            topic_id=data.topic_id,
            account_id=data.account_id,
            title=title,
            body=body,
            content_type=data.content_type,
            platform=data.platform,
            style=data.style,
            ai_provider=raw.get("ai_provider"),
            originality_score=compliance.get("originality"),
            readability_score=compliance.get("readability"),
            compliance_score=compliance.get("compliance"),
            value_score=compliance.get("value"),
        )
        self.db.add(content)
        await self.db.flush()
        return content

    def _parse_ai_output(self, text: str, fallback_title: str) -> tuple[str, str]:
        """Parse 【标题】/【正文】 sections from AI output."""
        title = fallback_title
        body = text
        if "【标题】" in text:
            parts = text.split("【标题】", 1)
            rest = parts[1]
            if "【正文】" in rest:
                title_part, body_part = rest.split("【正文】", 1)
                title = title_part.strip()
                body = body_part.split("【话题标签】")[0].strip()
            else:
                title = rest.split("\n")[0].strip()
        return title or fallback_title, body

    async def adapt_to_platforms(
        self, user_id: str, data: ContentAdaptRequest
    ) -> Content:
        """Generate platform-specific variants for a piece of content."""
        res = await self.db.execute(
            select(Content).where(Content.id == data.content_id, Content.creator_id == user_id)
        )
        content = res.scalar_one_or_none()
        if not content:
            raise NotFoundError("Content not found")

        versions = dict(content.platform_versions or {})
        for platform in data.target_platforms:
            raw = await _ai.generate_content(
                topic=content.title,
                platform=platform.value,
                style=content.style or "专业干货",
            )
            versions[platform.value] = raw.get("raw", "")

        content.platform_versions = versions
        await self.db.flush()
        return content

    async def get_content(self, content_id: str, user_id: str) -> Content:
        res = await self.db.execute(
            select(Content).where(Content.id == content_id, Content.creator_id == user_id)
        )
        content = res.scalar_one_or_none()
        if not content:
            raise NotFoundError("Content not found")
        return content

    async def update_content(
        self, content_id: str, user_id: str, data: ContentUpdate
    ) -> Content:
        content = await self.get_content(content_id, user_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(content, field, value)
        await self.db.flush()
        await self.db.refresh(content)
        return content

    async def delete_content(self, content_id: str, user_id: str) -> None:
        content = await self.get_content(content_id, user_id)
        await self.db.delete(content)
        await self.db.flush()
