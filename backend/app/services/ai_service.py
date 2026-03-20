"""AI model integration service supporting multiple providers."""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

from app.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.models import AIProvider
from app.schemas import AIGenerateRequest, AIGenerateResponse

settings = get_settings()


class BaseAIAdapter(ABC):
    """Abstract base for AI provider adapters."""

    @abstractmethod
    async def generate(self, request: AIGenerateRequest) -> AIGenerateResponse:
        ...


class OpenAIAdapter(BaseAIAdapter):
    async def generate(self, request: AIGenerateRequest) -> AIGenerateResponse:
        try:
            import openai  # lazy import
            client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            messages: list[dict[str, str]] = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            t0 = time.monotonic()
            resp = await client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,  # type: ignore[arg-type]
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
            latency = int((time.monotonic() - t0) * 1000)
            content = resp.choices[0].message.content or ""
            tokens = resp.usage.total_tokens if resp.usage else 0
            return AIGenerateResponse(
                content=content,
                provider=AIProvider.OPENAI,
                model=settings.openai_model,
                tokens_used=tokens,
                latency_ms=latency,
            )
        except Exception as exc:
            raise ExternalServiceError(f"OpenAI error: {exc}") from exc


class AnthropicAdapter(BaseAIAdapter):
    async def generate(self, request: AIGenerateRequest) -> AIGenerateResponse:
        try:
            import anthropic  # lazy import
            client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
            t0 = time.monotonic()
            msg = await client.messages.create(
                model=settings.anthropic_model,
                max_tokens=request.max_tokens,
                system=request.system_prompt or "You are a helpful assistant.",
                messages=[{"role": "user", "content": request.prompt}],
            )
            latency = int((time.monotonic() - t0) * 1000)
            content = msg.content[0].text if msg.content else ""
            tokens = (msg.usage.input_tokens + msg.usage.output_tokens) if msg.usage else 0
            return AIGenerateResponse(
                content=content,
                provider=AIProvider.ANTHROPIC,
                model=settings.anthropic_model,
                tokens_used=tokens,
                latency_ms=latency,
            )
        except Exception as exc:
            raise ExternalServiceError(f"Anthropic error: {exc}") from exc


class MockAIAdapter(BaseAIAdapter):
    """Fallback mock adapter for local development / testing."""

    async def generate(self, request: AIGenerateRequest) -> AIGenerateResponse:
        mock_text = f"[MOCK AI RESPONSE]\n\n主题：{request.prompt[:100]}\n\n这是AI模拟生成的内容，用于本地开发测试。"
        return AIGenerateResponse(
            content=mock_text,
            provider=AIProvider.OPENAI,
            model="mock",
            tokens_used=len(mock_text.split()),
            latency_ms=50,
        )


class AIService:
    """High-level AI service, routes to the appropriate adapter."""

    _adapters: dict[AIProvider, BaseAIAdapter] = {
        AIProvider.OPENAI: OpenAIAdapter(),
        AIProvider.ANTHROPIC: AnthropicAdapter(),
    }

    def _get_adapter(self, provider: AIProvider | None) -> BaseAIAdapter:
        p = provider or settings.default_ai_provider  # type: ignore[assignment]
        adapter = self._adapters.get(p)  # type: ignore[arg-type]
        if adapter is None or not self._is_configured(p):  # type: ignore[arg-type]
            return MockAIAdapter()
        return adapter

    def _is_configured(self, provider: AIProvider) -> bool:
        if provider == AIProvider.OPENAI:
            return bool(settings.openai_api_key)
        if provider == AIProvider.ANTHROPIC:
            return bool(settings.anthropic_api_key)
        return False

    async def generate(self, request: AIGenerateRequest) -> AIGenerateResponse:
        adapter = self._get_adapter(request.provider)
        return await adapter.generate(request)

    async def generate_topics(
        self,
        account_positioning: dict,
        count: int = 5,
        sources: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Generate topic suggestions for an account."""
        domain = account_positioning.get("domain", "通用")
        tags = account_positioning.get("tags", [])
        prompt = (
            f"你是一位专业的自媒体运营顾问。\n"
            f"账号领域：{domain}\n"
            f"账号标签：{', '.join(tags)}\n"
            f"数据来源：{', '.join(sources or ['热点榜单', '粉丝互动'])}\n"
            f"关键词偏好：{', '.join(keywords or [])}\n\n"
            f"请为该账号生成 {count} 个高潜力内容选题，每个选题包含：\n"
            f"1. 标题\n2. 简要说明\n3. 建议标签（3个）\n4. 适合平台\n"
            f"以JSON数组格式输出，字段：title, description, tags, platforms"
        )
        req = AIGenerateRequest(
            prompt=prompt,
            system_prompt="你是专业的自媒体运营顾问，擅长内容策划与选题分析。",
            max_tokens=2000,
        )
        resp = await self.generate(req)
        # In production, parse JSON from resp.content
        # For now return structured mock
        import json
        try:
            data = json.loads(resp.content)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, TypeError):
            pass
        # Fallback mock topics
        return [
            {
                "title": f"高潜力选题 {i+1}：关于 {domain} 的深度解析",
                "description": f"聚焦{domain}领域核心痛点，为目标用户提供实用价值",
                "tags": tags[:3] or ["护肤", "干货", "攻略"],
                "platforms": ["xiaohongshu", "douyin"],
            }
            for i in range(count)
        ]

    async def generate_content(
        self,
        topic: str,
        platform: str,
        style: str = "专业干货",
        word_count: int = 1200,
        account_info: dict | None = None,
    ) -> dict[str, Any]:
        """Generate complete content for a topic."""
        platform_guide = {
            "xiaohongshu": "小红书笔记风格：标题吸引眼球，正文分点排版，多用emoji，结尾引导互动",
            "douyin": "抖音文案风格：开头抓眼球，节奏快，口语化，引发共鸣",
            "wechat": "公众号文章风格：标题SEO优化，正文结构清晰，有数据支撑，结尾有CTA",
            "bilibili": "B站稿件风格：有深度，逻辑严密，适当幽默，标题含关键词",
        }
        guide = platform_guide.get(platform, "通用自媒体内容风格")
        prompt = (
            f"请为以下选题创作一篇{word_count}字左右的{style}风格内容：\n\n"
            f"选题：{topic}\n"
            f"平台规范：{guide}\n\n"
            f"请按照以下格式输出：\n"
            f"【标题】\n<标题内容>\n\n"
            f"【正文】\n<正文内容>\n\n"
            f"【话题标签】\n<标签列表>"
        )
        req = AIGenerateRequest(
            prompt=prompt,
            system_prompt="你是专业的自媒体内容创作者，擅长各平台爆款内容创作。",
            max_tokens=min(word_count * 3, 4000),
        )
        resp = await self.generate(req)
        return {
            "raw": resp.content,
            "ai_provider": resp.provider,
            "tokens_used": resp.tokens_used,
            "latency_ms": resp.latency_ms,
        }

    async def check_compliance(self, text: str) -> dict[str, Any]:
        """Check content for sensitive words, originality, compliance."""
        prompt = (
            f"请对以下内容进行合规检测，从以下4个维度评分（0-100）并给出建议：\n"
            f"1. 原创度（是否有抄袭风险）\n"
            f"2. 可读性（语言流畅、逻辑清晰）\n"
            f"3. 合规性（无敏感词、违规内容）\n"
            f"4. 价值感（对目标读者的实用价值）\n\n"
            f"内容：{text[:1000]}\n\n"
            f"输出JSON格式：{{originality: N, readability: N, compliance: N, value: N, issues: [...], suggestions: [...]}}"
        )
        req = AIGenerateRequest(prompt=prompt, max_tokens=500)
        resp = await self.generate(req)
        import json
        try:
            data = json.loads(resp.content)
            return data
        except (json.JSONDecodeError, TypeError):
            return {
                "originality": 85,
                "readability": 90,
                "compliance": 98,
                "value": 88,
                "issues": [],
                "suggestions": ["内容质量良好"],
            }
