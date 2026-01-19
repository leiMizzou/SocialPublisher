# SocialPublisher

English | **[中文](./README.md)**

> 🚀 Social Media Content Automation: Search → Engage → Distill → Multi-Platform Publish

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Features

- ✅ **Smart Search** - Search trending content on Twitter/X for any topic
- ✅ **Auto Engagement** - Like posts, generate valuable replies
- ✅ **Content Distillation** - Extract key insights from multiple posts
- ✅ **Multi-Platform Publishing** - Twitter Thread, Xiaohongshu (RED), WeChat Official Account
- ✅ **Content Tracking** - Full workflow tracking, automatic verification
- ✅ **Claude Code Integration** - Use as a Skill, AI-powered workflow

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. Search  │ ──▶ │  2. Engage  │ ──▶ │  3. Distill │ ──▶ │  4. Publish │ ──▶ │  5. Verify  │
│   Trending  │     │  Like/Reply │     │   Insights  │     │ Multi-Plat  │     │   Auto QA   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
        │                  │                  │                  │                  │
        └──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                   Content Tracker Records Everything
```

## Platform Style Guide

| Aspect | Twitter Thread | Xiaohongshu (RED) | WeChat Article |
|--------|---------------|-------------------|----------------|
| **Tone** | Professional info | Casual chat | In-depth report |
| **Address Reader** | None/Devs | Sisters/Friends | Dear readers |
| **Emoji** | Minimal 🧵📌🔗 | Heavy use | Rare/None |
| **Length** | ≤280 chars/tweet | 300-800 chars | 1000-2500 chars |
| **Technical Terms** | Use directly | Explain casually | Use with context |
| **Ending** | Links/Discussion | Q&A + Hashtags | Summary + Reading |

## Installation

```bash
# Clone the project
git clone https://github.com/leiMizzou/SocialPublisher.git
cd SocialPublisher

# Install dependencies
pip install playwright
playwright install chromium
```

## Usage

### 1. Claude Code Skill (Recommended)

```bash
# Full workflow example
/social-media-publisher Search 10 hottest AI Agent posts today, like and reply, create Twitter thread, Xiaohongshu note, and WeChat article

# Search only, no engagement
/social-media-publisher Check what's trending about Claude Skill today

# Specific platform
/social-media-publisher Search LLM content, only publish to Xiaohongshu

# Natural language support
/social-media-publisher Write a Xiaohongshu note about React 19 based on Twitter discussions
```

### 2. Command Line Tools

```bash
# Check login status for all platforms
./scripts/publish.sh status

# Content tracking commands
./scripts/publish.sh track init -t "AI Agent"    # Initialize tracking session
./scripts/publish.sh track report                 # View tracking report
./scripts/publish.sh track verify                 # Execute publish verification
./scripts/publish.sh track list                   # List all sessions
```

### 3. Python Scripts

```bash
# Check login status
python scripts/check_login.py              # Check all platforms
python scripts/check_login.py -p twitter   # Check Twitter only
python scripts/check_login.py --json       # JSON format output

# Content tracking
python scripts/content_tracker.py init --topic "Claude Skill"
python scripts/content_tracker.py search --query "Claude Skill" --posts '[...]'
python scripts/content_tracker.py engage --action like --post-id "xxx"
python scripts/content_tracker.py generate --platform twitter --thread '[...]'
python scripts/content_tracker.py publish --platform twitter --status published --count 5
python scripts/content_tracker.py verify
```

## File Structure

```
SocialPublisher/
├── README.md                 # Chinese documentation
├── README_EN.md              # English documentation
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── check_login.py        # Login status checker
│   ├── content_tracker.py    # Content tracking and verification
│   └── publish.sh            # Shell command shortcuts
├── .claude/
│   └── skills/
│       └── social-media-publisher/
│           └── SKILL.md      # Claude Code Skill definition
└── .social_publisher/        # Auto-generated at runtime (in .gitignore)
    ├── cookies/              # Cookie storage
    └── sessions/             # Session tracking records
```

## Skill Workflow Details

### Phase 1: Search Trending Content
- Search specified topic on Twitter/X
- Filter by popularity within last 24 hours
- Collect specified number of posts (links, authors, content, engagement data)
- **→ Tracker: Record search results**

### Phase 2: Engagement
- Like valuable posts
- Generate insightful replies (not generic "Great post!" responses)
- User confirms before sending
- **→ Tracker: Record likes and replies**

### Phase 3: Content Distillation
- Identify common themes and trends
- Extract 3-5 key points
- Note important quotes with sources
- **→ Tracker: Record trends and key points**

### Phase 4: Multi-Platform Publishing
- **Twitter**: Generate Thread (search count + 2 tweets)
- **Xiaohongshu**: Casual style + hashtags
- **WeChat**: Long-form article + structured
- **→ Tracker: Record generated content and publish status**

### Phase 5: Verification
- Auto-check if Twitter Thread is fully published
- Verify publish status across platforms
- Prompt for incomplete content and support re-publishing
- **→ Tracker: Execute `verify` command**

## Content Tracking System

Full workflow tracking to prevent missed publications:

### Tracking Stages

| Stage | Records | CLI Command |
|-------|---------|-------------|
| Init | Topic, Session ID | `init --topic "topic"` |
| Search | Query, Posts list | `search --query "..." --posts '[...]'` |
| Engage | Likes, Replies | `engage --action like/reply` |
| Distill | Trends, Key points | `distill --trends '[...]'` |
| Generate | Platform content | `generate --platform xxx` |
| Publish | Status, URL, Count | `publish --platform xxx --status xxx` |
| Verify | Results, Suggestions | `verify` |

### Verification Report Example

```
============================================================
📋 Content Tracking Report
   Session ID: 20260119_143052
   Topic: Claude Skill
============================================================

🔍 Search Phase:
   Query: Claude Skill
   Posts found: 10

💬 Engagement Phase:
   Liked: 5 posts
   Replied: 3 posts

📝 Generated Content:
   Twitter Thread: 12 tweets
   Xiaohongshu: Claude Skill Daily Highlights
   WeChat: Claude Skill Deep Dive

📤 Publish Status:
   ⚠️ Twitter: partial (8/12 tweets)
   ✅ Xiaohongshu: published
   ✅ WeChat: draft

🔎 Verification Results:
   ⚠️ Twitter Thread incomplete: Expected 12, Actual 8

💡 Suggested Actions:
   Need to publish 4 more tweets:
   1. 9/ Hot Post #8: @author8...
   2. 10/ Hot Post #9: @author9...
============================================================
```

## Login Status Check

```bash
$ python scripts/check_login.py

==================================================
🔐 Social Platform Login Status Check
==================================================

✅ Twitter/X: OK (updated 2 days ago)
   Cookies: 15
⚠️  WeChat: Cookies expiring soon (updated 5 days ago)
   Cookies: 23
❌ Xiaohongshu: Cookies expired (updated 10 days ago, recommend refresh within 7 days)
   Cookies: 18

--------------------------------------------------
⚠️  1 platform needs re-login

Use Playwright MCP to visit the platform for login:
   • Xiaohongshu: https://creator.xiaohongshu.com
```

## Cookie Management

Storage location: `.social_publisher/cookies/`

| Platform | File | Login Method | Recommended Refresh |
|----------|------|--------------|---------------------|
| Twitter/X | `twitter_cookies.json` | Username/Password or Google | 30 days |
| WeChat | `wechat_cookies.json` | QR Code Scan | 7 days |
| Xiaohongshu | `xiaohongshu_cookies.json` | QR Code Scan | 7 days |

**Login Method**: Use Playwright MCP to visit the platform login page. Cookies are saved automatically.

## Example Output

### Search Results
```
🔍 Search Topic: AI Agent
📅 Time Range: Last 24 hours
📊 Found 10 trending posts:

1. @DBVolkov (❤️ 1.8k 🔄 310 💬 48)
   A senior Google engineer just dropped a 424-page doc...
   🔗 https://x.com/DBVolkov/status/...

2. @recap_david (❤️ 6.5k 🔄 1.6k 💬 2.4k)
   I built an AI marketing agent to run my $100K media company...
   🔗 https://x.com/recap_david/status/...
```

### Publish Results
```
✅ Complete!

📊 Session Statistics:
- 🔍 Search: 10 "AI Agent" related posts
- ❤️ Liked: 5 posts
- 💬 Replied: 3 posts
- 📱 Published: Twitter Thread (12 tweets) + Xiaohongshu + WeChat

🔗 Published Links:
- Twitter: https://x.com/yourname/status/...
- Xiaohongshu: https://www.xiaohongshu.com/explore/...
- WeChat: https://mp.weixin.qq.com/s/...
```

## Dependencies

- Python 3.8+
- Playwright
- Chromium
- Claude Code (recommended, for Skill functionality)

## Important Notes

- Use engagement features cautiously to avoid platform restrictions
- Confirm content complies with each platform's guidelines before publishing
- Recommend testing with "search only, no engagement" mode first
- Check login status regularly: `./scripts/publish.sh status`

## License

MIT License
