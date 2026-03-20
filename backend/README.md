# AI智能自媒体运营平台 - 后端

Python (FastAPI) 后端服务，基于《AI智能自媒体系统功能说明书》设计实现。

## 技术栈

| 层次 | 技术 |
|------|------|
| Web 框架 | FastAPI 0.115+ |
| ORM | SQLAlchemy 2.0 (Async) |
| 数据库迁移 | Alembic |
| 关系数据库 | PostgreSQL 16 |
| 缓存 & 消息队列 | Redis 7 |
| 后台任务 | Celery 5 + Celery Beat |
| 认证 | JWT (python-jose) + BCrypt |
| AI 接入 | OpenAI / Anthropic / 文心 / 通义千问 |
| 监控 | Prometheus metrics |
| 日志 | structlog |

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
└─────────────────────────────────────────────────────────┘
                          │ HTTP REST / JSON
┌─────────────────────────────────────────────────────────┐
│                FastAPI Application                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │   Auth   │  │ Content  │  │Analytics │  │  ...   │  │
│  │  Router  │  │  Router  │  │  Router  │  │        │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Service Layer (Business Logic)         │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           SQLAlchemy ORM (Async)                    │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │                    │                  │
   ┌─────▼─────┐       ┌──────▼──────┐   ┌─────▼─────┐
   │ PostgreSQL │       │    Redis    │   │  AI APIs  │
   │   (main)  │       │(cache+queue)│   │(OpenAI/..)│
   └───────────┘       └─────────────┘   └───────────┘
         │
   ┌─────▼─────┐
   │  Celery   │
   │ Workers   │
   └───────────┘
```

## 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理 (pydantic-settings)
│   ├── database.py          # 数据库引擎 & Session
│   ├── dependencies.py      # 依赖注入 (current_user, db)
│   ├── core/
│   │   ├── security.py      # JWT 签发/验证、密码哈希
│   │   └── exceptions.py    # 自定义异常 & FastAPI 异常处理器
│   ├── models/              # SQLAlchemy ORM 模型 (15张数据表)
│   ├── schemas/             # Pydantic 请求/响应 Schema
│   ├── api/v1/              # REST API 路由 (10个子路由)
│   │   ├── auth.py          # 认证 (注册/登录/刷新/改密)
│   │   ├── accounts.py      # 社媒账号管理
│   │   ├── topics.py        # 智能选题引擎
│   │   ├── content.py       # 多模态内容生成
│   │   ├── analytics.py     # 数据分析 & 预警
│   │   ├── distribution.py  # 跨平台智能分发
│   │   ├── monetization.py  # 商业变现
│   │   ├── interaction.py   # 用户画像 & 互动
│   │   ├── ai_support.py    # AI 技术支撑 & 提示词模板
│   │   └── workflows.py     # 自动化工作流
│   ├── services/            # 业务逻辑层
│   └── tasks/               # Celery 后台任务
├── alembic/                 # 数据库迁移脚本
├── tests/                   # 测试 (pytest-asyncio)
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── requirements.txt
└── pyproject.toml
```

## 核心功能模块

| 模块 | API 前缀 | 功能说明 |
|------|----------|---------|
| 认证 | `/api/v1/auth` | 注册、登录、JWT 刷新、改密 |
| 社媒账号 | `/api/v1/accounts` | 多平台账号绑定、定位管理 |
| **智能选题** | `/api/v1/topics` | AI 批量生成选题、评分、选题日历 |
| **多模态内容** | `/api/v1/contents` | AI 内容生成、多平台适配、合规检测 |
| **数据分析** | `/api/v1/analytics` | 数据看板、预警规则、归因分析 |
| **智能分发** | `/api/v1/distribution` | 定时发布、最优发布时间 |
| **商业变现** | `/api/v1/monetization` | 商单管理、收入统计 |
| **用户互动** | `/api/v1/interaction` | 粉丝画像、自动化互动任务 |
| AI 支撑 | `/api/v1/ai` | 多模型调用、提示词模板库 |
| 工作流 | `/api/v1/workflows` | 自动化规则 (触发器-动作) |

## 快速启动

### 使用 Docker Compose（推荐）

```bash
# 1. 复制环境变量
cp .env.example .env
# 填入 OPENAI_API_KEY 等 AI 配置

# 2. 启动所有服务
cd docker && docker-compose up -d

# 3. 访问 API 文档
open http://localhost:8000/docs
```

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt -r requirements-dev.txt

# 2. 配置环境变量
cp .env.example .env

# 3. 启动 PostgreSQL & Redis (或使用 docker-compose)
docker-compose -f docker/docker-compose.yml up postgres redis -d

# 4. 运行数据库迁移
alembic upgrade head

# 5. 启动 API 服务
uvicorn app.main:app --reload

# 6. 启动 Celery Worker (另一终端)
celery -A app.tasks.celery_app worker --loglevel=info

# 7. 启动 Celery Beat 定时任务 (另一终端)
celery -A app.tasks.celery_app beat --loglevel=info
```

### 运行测试

```bash
# 无需 PostgreSQL，使用 SQLite
TEST_DATABASE_URL="sqlite+aiosqlite:///./test.db" pytest tests/ -v
```

## 数据库设计

共 **15 张数据表**，覆盖所有核心业务：

| 表名 | 说明 |
|------|------|
| `users` | 平台用户 |
| `refresh_tokens` | JWT 刷新令牌 |
| `social_accounts` | 绑定的社媒账号 |
| `topics` | 内容选题 |
| `contents` | 创作内容 |
| `materials` | 素材库 |
| `prompt_templates` | 提示词模板 |
| `fan_profiles` | 粉丝画像 |
| `interaction_tasks` | 自动化互动任务 |
| `account_analytics` | 账号数据快照 (日维度) |
| `content_analytics` | 内容数据 (日维度) |
| `alert_rules` | 数据预警规则 |
| `publish_tasks` | 定时发布任务 |
| `commercial_orders` | 商单 |
| `revenue_records` | 变现收入记录 |
| `workflow_rules` | 自动化工作流规则 |

## 后台任务调度

| 任务 | 触发频率 | 说明 |
|------|---------|------|
| `sync_all_platform_analytics` | 每小时 | 同步各平台数据 |
| `check_alert_rules` | 每15分钟 | 检查预警规则 |
| `process_due_publish_tasks` | 每分钟 | 执行到期发布任务 |

## 安全特性

- JWT Bearer Token 认证 (access + refresh token 轮换)
- BCrypt 密码哈希
- CORS 控制
- 细粒度角色权限 (admin / editor / operator / analyst / viewer)
- Prometheus 指标采集
- 敏感词 & 原创度合规检测 (AI 辅助)
