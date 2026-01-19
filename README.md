# SocialPublisher

> 🚀 一键发布内容到多个社交媒体平台，内容自动适配各平台风格

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)](https://playwright.dev)

## 特性

- ✅ **多平台支持** - Twitter/X、微信公众号、小红书
- ✅ **Cookie 持久化** - 首次扫码登录，之后自动登录
- ✅ **内容自动适配** - 根据平台特点调整风格和格式
- ✅ **Claude Code 集成** - 可作为 Skill 使用，AI 生成内容

## 平台适配策略

| 平台 | 风格 | 特点 |
|------|------|------|
| **Twitter/X** | 简洁 | Thread 串联、280字符限制 |
| **微信公众号** | 正式 | 长文章、封面图、摘要 |
| **小红书** | 活泼 | Emoji、话题标签、文字配图 |

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

### 1. 命令行工具

```bash
# 首次使用：登录并保存 cookies
./scripts/publish.sh login

# 查看登录状态
./scripts/publish.sh status

# 发布到所有平台
./scripts/publish.sh post "标题" "内容"

# 只发布到指定平台
./scripts/publish.sh post "标题" "内容" xiaohongshu
./scripts/publish.sh post "标题" "内容" wechat
```

### 2. Python API

```python
import asyncio
from scripts.social_publisher import publish_content, login_platform

# 登录（首次需要）
asyncio.run(login_platform("xiaohongshu"))

# 发布内容
content = {
    "title": "今日AI热点",
    "content": "内容正文...",
    "summary": "摘要（微信公众号用）"
}
asyncio.run(publish_content(content, platforms=["xiaohongshu", "wechat"]))
```

### 3. Claude Code Skill

将 `.claude/skills/social-media-publisher.md` 复制到你的项目，然后：

```
/social-media-publisher AI热点
/social-media-publisher "今天学到的Python技巧" xiaohongshu
```

## 文件结构

```
SocialPublisher/
├── README.md
├── scripts/
│   ├── social_publisher.py    # Python 主程序
│   └── publish.sh             # Shell 快捷命令
├── .claude/
│   └── skills/
│       └── social-media-publisher.md  # Claude Code Skill
└── .social_publisher/         # (运行后自动生成)
    └── cookies/               # Cookie 存储
```

## Cookie 说明

- Cookies 保存在 `.social_publisher/cookies/` 目录
- 首次使用需扫码登录，之后自动加载
- 登录状态通常可保持几天到几周
- 如果 cookies 过期，会提示重新登录

## 内容适配示例

**原始内容：**
```
今日AI热点：Claude预言成真，AI将编写所有代码
```

**微信公众号：**
```
标题：今日AI热点汇总 (2026.1.19)
正文：[正式的文章格式，完整段落]
```

**小红书：**
```
标题：刷X看到的AI热点｜码住！
正文：姐妹们！今天AI圈超热闘🔥
💡 Claude预言成真...
#AI #人工智能 #科技热点
```

## 依赖

- Python 3.8+
- Playwright
- Chromium (通过 playwright install 安装)

## 注意事项

- 微信公众号和小红书需要通过浏览器操作，无法完全 headless
- 发布前请确认内容符合各平台规范
- 请勿用于发布违规内容

## License

MIT License
