# SocialPublisher

> 🚀 社交媒体内容运营自动化：搜索 → 互动 → 提炼 → 多平台发布

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)](https://playwright.dev)

## 特性

- ✅ **智能搜索** - 在 Twitter/X 搜索任意主题的热门内容
- ✅ **自动互动** - 点赞、生成有价值的回复
- ✅ **内容提炼** - 从多条帖子中提取核心观点
- ✅ **多平台发布** - Twitter Thread、小红书、微信公众号
- ✅ **Cookie 持久化** - 首次登录后自动保持
- ✅ **Claude Code 集成** - 作为 Skill 使用，AI 驱动全流程

## 工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. 搜索    │ ──▶ │  2. 互动    │ ──▶ │  3. 提炼    │ ──▶ │  4. 发布    │
│  热门内容   │     │  点赞/回复  │     │  核心观点   │     │  多平台     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## 平台适配策略

| 平台 | 风格 | 长度 | 特点 |
|------|------|------|------|
| **Twitter Thread** | 信息密集 | 每条≤280字 | 编号串联、@引用、精炼表达 |
| **小红书** | 活泼亲切 | ≤500字 | 口语化、emoji、话题标签 |
| **微信公众号** | 深度专业 | 1000-2000字 | 结构化、引用来源、延伸阅读 |

## 安装

```bash
# 克隆项目
git clone https://github.com/yourname/SocialPublisher.git
cd SocialPublisher

# 安装依赖
pip install playwright
playwright install chromium
```

## 使用方式

### 1. Claude Code Skill (推荐)

```bash
# 完整流程：搜索 + 互动 + 提炼 + 发布
/social-media-publisher "Claude Skill"

# 仅搜索
/social-media-publisher "AI Agent" search

# 搜索 + 互动
/social-media-publisher "LLM" engage

# 搜索 + 发布（跳过互动）
/social-media-publisher "React 19" publish

# 指定平台
/social-media-publisher "Claude" full twitter
```

### 2. 命令行工具

```bash
# 首次使用：登录平台
./scripts/publish.sh login
./scripts/publish.sh login twitter

# 查看登录状态
./scripts/publish.sh status

# 发布内容
./scripts/publish.sh post "标题" "内容"
./scripts/publish.sh post "标题" "内容" twitter
```

### 3. Python API

```python
import asyncio
from scripts.social_publisher import publish_content, login_platform

# 登录
asyncio.run(login_platform("twitter"))

# 发布
content = {
    "title": "Claude Skill 今日热点",
    "content": "内容正文...",
    "summary": "摘要"
}
asyncio.run(publish_content(content, platforms=["twitter", "xiaohongshu", "wechat"]))
```

## 文件结构

```
SocialPublisher/
├── README.md
├── requirements.txt
├── scripts/
│   ├── social_publisher.py    # Python 主程序
│   ├── content_tracker.py     # 内容追踪和核查系统
│   └── publish.sh             # Shell 快捷命令
├── .claude/
│   └── skills/
│       └── social-media-publisher/
│           └── SKILL.md       # Claude Code Skill (核心)
└── .social_publisher/         # (运行后自动生成)
    ├── cookies/               # Cookie 存储
    └── sessions/              # 会话追踪记录
```

## Skill 工作流详解

### Phase 1: 搜索热门内容
- 在 Twitter/X 搜索指定主题
- 按热度筛选最近 24 小时内容
- 收集 10 条最热帖子（链接、作者、内容、互动数据）

### Phase 2: 互动
- 对有价值的帖子点赞
- 生成有见地的回复（非 "Great post!" 式敷衍）
- 用户确认后发送

### Phase 3: 内容提炼
- 识别共同主题和趋势
- 提取 3-5 个核心要点
- 标注重要引用来源

### Phase 4: 多平台发布
- **Twitter**: 生成 Thread 串 (5-10 条)
- **小红书**: 活泼风格 + 话题标签
- **微信公众号**: 深度长文 + 结构化

### Phase 5: 核查验证
- 检查 Twitter Thread 是否完整发布
- 验证各平台发布状态
- 提示未完成的内容并支持补发

## 内容追踪系统

为确保内容完整发布，新增了 `ContentTracker` 追踪系统：

```bash
# 查看最新会话报告
python scripts/content_tracker.py report

# 执行核查验证
python scripts/content_tracker.py verify

# 列出所有会话
python scripts/content_tracker.py list
```

### 追踪功能
- 记录搜索到的所有帖子
- 记录互动状态（点赞、回复）
- 记录各平台生成的完整内容
- 记录发布状态（预期数量 vs 实际数量）
- 发布后自动核查，提示未完成项

### 核查报告示例
```
📋 内容追踪报告
   主题: Claude Skill

📤 发布状态:
   ⚠️ Twitter: partial (3/5 条)
   ✅ 小红书: published
   ✅ 微信公众号: draft

🔎 核查结果:
   ⚠️ Twitter Thread 未发完: 预期 5 条, 实际 3 条
```

## Cookie 说明

存储位置: `.social_publisher/cookies/`

| 平台 | 文件 | 登录方式 |
|------|------|----------|
| Twitter/X | `twitter_cookies.json` | 账号密码 / Google |
| 微信公众号 | `wechat_cookies.json` | 扫码 |
| 小红书 | `xiaohongshu_cookies.json` | 扫码 |

## 示例输出

### 搜索结果
```
🔍 搜索主题: Claude Skill
📅 时间范围: 最近24小时
📊 找到 10 条热门帖子:

1. @anthropic (❤️ 2.1k 🔄 500 💬 120)
   Claude's new skill system is amazing...
   🔗 https://x.com/...

2. @aidev (❤️ 1.5k 🔄 300 💬 80)
   Just built my first Claude Skill...
```

### 发布结果
```
✅ 完成！

📊 本次运营:
- 搜索: 10 条热门帖子
- 互动: 点赞 8 条，回复 5 条
- 发布: Twitter Thread (5条) + 小红书 + 微信公众号

🔗 发布链接:
- Twitter: https://x.com/yourname/status/...
- 小红书: https://...
- 微信: https://mp.weixin.qq.com/...
```

## 依赖

- Python 3.8+
- Playwright
- Chromium
- Claude Code (推荐，使用 Skill 功能)

## 注意事项

- 互动功能需谨慎使用，避免被平台限制
- 发布前请确认内容符合各平台规范
- 建议先用 `search` 模式测试

## License

MIT License
