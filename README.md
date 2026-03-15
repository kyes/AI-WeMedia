# AI-WeMedia — AI+自媒体系统

> 基于多模型 AI 的智能自媒体内容创作、分发与运营一体化平台

---

## 项目简介

AI-WeMedia 是一套面向自媒体创作者与运营团队的 **AI 驱动一体化系统**，覆盖从选题策划、内容生产、多平台分发，到运营监控、数据分析和商业变现的完整链路。系统集成 Gemini、豆包（扣子空间）、腾讯 ima、kimi 等主流大模型，并对接微信公众号、小红书、抖音、快手、B站等头部内容平台，帮助创作者以更低成本实现更高效率的内容运营。

---

## 系统功能模块

| # | 模块名称 | 简介 |
|---|---------|------|
| 1 | [智能选题与内容生成](docs/modules/01-content-creation.md) | 热点追踪、用户洞察、AI 文案/脚本生成 |
| 2 | [数据监测与智能决策](docs/modules/02-data-monitoring.md) | 实时看板、策略优化建议 |
| 3 | [跨平台智能分发](docs/modules/03-platform-distribution.md) | 多平台内容适配与自动发布 |
| 4 | [商业变现赋能](docs/modules/04-monetization.md) | 广告匹配、带货推荐、私域引流 |
| 5 | [自媒体选题分析智能体](docs/modules/05-intelligent-agent.md) | 需求沟通、选题评估、平台选择、方案制定 |
| 6 | [内容创作工作流（智能体系）](docs/modules/06-content-workflow.md) | 热点收集、图文/视频生成、AI 检测优化、自动发布 |
| 7 | [运营监控](docs/modules/07-operation-monitoring.md) | 账号合规、内容质量、用户运营监控 |
| 8 | [数据运营监控](docs/modules/08-data-analytics.md) | 日/周数据、竞品对比分析 |

---

## 快速开始

1. 阅读 [产品功能设计文档](docs/product-design.md) 了解系统全貌。
2. 按需查阅各模块详细说明（`docs/modules/` 目录）。
3. 参考 [技术架构说明](docs/tech-architecture.md) 了解集成方式与技术选型。

---

## 技术栈

| 层级 | 技术 / 平台 |
|------|------------|
| AI 大模型 | Gemini、腾讯 ima、豆包（扣子空间）、kimi |
| 内容平台 | 微信公众号、小红书、抖音、快手、B站 |
| 数据采集 | 平台原生 API、第三方热点平台、行业垂直官网 |
| 自动化发布 | 各平台自动发布接口 |
| 监控体系 | 日/周数据监控仪表盘、竞品追踪 |
| AI 检测 | AI 内容比例检测（≤70% AI 味） |

---

## 文档导航

```
docs/
├── product-design.md               # 产品功能设计文档（主文档）
├── tech-architecture.md            # 技术架构说明
└── modules/
    ├── 01-content-creation.md      # 智能选题与内容生成
    ├── 02-data-monitoring.md       # 数据监测与智能决策
    ├── 03-platform-distribution.md # 跨平台智能分发
    ├── 04-monetization.md          # 商业变现赋能
    ├── 05-intelligent-agent.md     # 自媒体选题分析智能体
    ├── 06-content-workflow.md      # 内容创作工作流
    ├── 07-operation-monitoring.md  # 运营监控
    └── 08-data-analytics.md        # 数据运营监控
```

---

## 核心 KPI 指标

| 指标 | 目标值 |
|------|--------|
| 内容产出效率提升 | ≥ 3x |
| AI 内容比例 | ≤ 70% |
| 热点响应时间 | ≤ 2 小时 |
| 多平台同步发布 | 支持 6+ 平台 |
| 数据监控维度 | ≥ 20 项核心指标 |
| 竞品追踪数量 | 3-5 个 |

---

## License

MIT
