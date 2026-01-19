---
name: social-media-publisher
description: 社交媒体内容运营工具。搜索 Twitter 热门帖子、点赞回复互动、提炼核心观点、发布到多平台（Twitter Thread、小红书、微信公众号）。支持自然语言输入如"搜索 10 个今天最热的 AI 帖子，点赞并整理成小红书笔记"。
---

# Social Media Publisher Skill

## Usage
```
/social-media-publisher <自然语言描述你的需求>
```

## Examples
```
/social-media-publisher 搜索 10 个今天最热的 Claude Skill 帖子，点赞并回复，然后整理成 Twitter 串和小红书笔记

/social-media-publisher 找 5 个最有价值的 AI Agent 讨论，只看不互动，整理成微信公众号文章

/social-media-publisher 搜索 20 个关于 LLM 的帖子，按评论数排序，提炼观点发到所有平台

/social-media-publisher 看看今天 Cursor 相关有什么热门讨论

/social-media-publisher 帮我写一篇关于 React 19 的小红书笔记，基于 Twitter 上的热门讨论
```

---

## Instructions

### Step 0: 登录状态检查 (必须执行!)

**在开始任何操作之前，必须先检查登录状态：**

```bash
python3 scripts/check_login.py
```

**根据检查结果处理：**
- ✅ 所有平台正常 → 继续 Step 1
- ⚠️ 有平台需要登录 → 使用 Playwright MCP 访问对应平台完成登录，然后重新检查
- ❌ 检查失败 → 停止并告知用户

**如果用户只需要发布到部分平台，只需确保目标平台登录正常即可。**

---

### Step 1: 解析用户意图

从用户的自然语言输入中提取以下参数：

```yaml
主题: <关键词，如 "Claude Skill", "AI Agent", "LLM">
数量: <帖子数量，默认 10>
排序: <最热/最新/最有价值/评论最多/转发最多，默认 最热>
时间: <今天/本周/本月/不限，默认 今天>
互动: <是否点赞回复，默认 是>
平台: <twitter/xiaohongshu/wechat/all，默认 all>
操作: <仅搜索/仅互动/仅发布/完整流程，默认 完整流程>
```

**解析示例：**

| 用户输入 | 解析结果 |
|---------|---------|
| "搜索 10 个今天最热的 Claude Skill 帖子" | 主题=Claude Skill, 数量=10, 排序=最热, 时间=今天 |
| "找 5 个最有价值的 AI 讨论，只看不互动" | 主题=AI, 数量=5, 排序=最有价值, 互动=否 |
| "本周关于 Rust 的热门帖子，发到小红书" | 主题=Rust, 时间=本周, 平台=xiaohongshu |
| "看看 Cursor 有什么讨论" | 主题=Cursor, 操作=仅搜索 |

### Step 2: 确认理解并初始化追踪

向用户展示解析结果，确认后继续：

```
📋 我理解你的需求是：

🔍 搜索: "Claude Skill" 相关内容
📊 数量: 10 条
📈 排序: 按热度（点赞+转发）
📅 时间: 最近 24 小时
💬 互动: 点赞并回复有价值的帖子
📱 发布: Twitter Thread + 小红书 + 微信公众号

确认开始？(可以说"调整为 5 条"或"不要互动"等)
```

**确认后，必须执行 - 初始化内容追踪：**
```bash
python3 scripts/content_tracker.py init --topic "{主题}"
```
⚠️ **此命令必须成功执行后才能继续，它会创建追踪会话用于记录整个流程。**

### Step 3: 执行搜索

**构建搜索 URL：**
```
Twitter: x.com/search?q={主题}&f=top (最热) 或 &f=live (最新)
时间过滤: 添加 since:2026-01-18 until:2026-01-19
```

**使用 Playwright MCP：**
```
1. browser_navigate: 构建的搜索 URL
2. browser_snapshot: 获取结果
3. 滚动加载更多，直到收集够 {数量} 条
4. 提取每条帖子信息
```

**收集的信息：**
```yaml
- 链接: https://x.com/user/status/123
- 作者: @username
- 内容: 帖子全文
- 点赞数: 1234
- 转发数: 567
- 评论数: 89
- 发布时间: 2小时前
```

**排序逻辑：**
- 最热 = 点赞 + 转发
- 最有价值 = (点赞 + 转发×2 + 评论×3) / 粉丝数（归一化）
- 评论最多 = 评论数
- 最新 = 发布时间

**必须执行 - 搜索完成后记录结果：**
```bash
python3 scripts/content_tracker.py search \
  --query "{主题}" \
  --time-range "24h" \
  --posts '[{"id": "xxx", "author": "@user", "content": "...", "likes": 100}]'
```
⚠️ **必须在展示结果给用户之前执行此命令，将搜索结果记录到追踪系统。**

### Step 4: 展示搜索结果

```
🔍 搜索主题: Claude Skill
📅 时间范围: 最近 24 小时
📊 找到 {数量} 条热门帖子:

1. @anthropic (❤️ 2.1k 🔄 500 💬 120) ⭐ 价值分
   Claude's new skill system enables...
   🔗 https://x.com/anthropic/status/...

2. @aidev (❤️ 1.5k 🔄 300 💬 80) ⭐ 价值分
   Just built my first Claude Skill and...
   🔗 https://x.com/aidev/status/...

...

选择要互动的帖子 (输入编号如 1,2,5 或 "全部" 或 "跳过"):
```

### Step 5: 执行互动 (如果需要)

**点赞：**
```
browser_navigate: 帖子链接
browser_click: [data-testid="like"]
```

**生成回复：**
根据帖子内容生成有价值的回复，风格：
- 补充观点或数据
- 提出有深度的问题
- 分享相关经验
- 不要: "Great post!", "Thanks for sharing!"

```
示例回复:
"这个观点很有启发！我在实际使用中发现 Skill 的 xxx 特性特别有用，
尤其是在处理 yyy 场景时。想问下你有没有试过 zzz 的用法？"
```

**发送回复前确认：**
```
💬 准备回复 @anthropic:

"这个观点很有启发！..."

发送？(y/n/修改内容)
```

**必须执行 - 互动过程中实时记录：**
```bash
# 用户选择互动帖子后，立即记录
python3 scripts/content_tracker.py engage --action select --post-ids "id1,id2,id3"

# 每次点赞成功后，立即记录
python3 scripts/content_tracker.py engage --action like --post-id "xxx"

# 每次回复成功后，立即记录
python3 scripts/content_tracker.py engage --action reply --post-id "xxx" --reply-text "回复内容"
```
⚠️ **每次互动操作后必须立即执行对应的记录命令，确保追踪数据实时更新。**

### Step 6: 内容提炼

**分析收集的帖子，提取：**
```yaml
核心趋势:
  - 趋势1: xxx
  - 趋势2: yyy

关键观点:
  - 观点1 (来源: @user1)
  - 观点2 (来源: @user2)
  - 观点3 (来源: @user3)

有价值的引用:
  - "原文引用..." - @author

我的总结:
  - 总结1
  - 总结2
```

**必须执行 - 提炼完成后记录：**
```bash
python3 scripts/content_tracker.py distill \
  --trends '["趋势1", "趋势2"]' \
  --points '["要点1", "要点2", "要点3"]' \
  --quotes '[{"text": "引用内容", "author": "@user"}]' \
  --summary "总结内容"
```
⚠️ **必须在生成各平台内容之前执行此命令，记录提炼的核心内容。**

### Step 7: 生成各平台内容

---

## ⚠️ 平台风格差异化指南（重要！必读！）

**三个平台风格完全不同，生成内容时必须严格区分：**

| 维度 | Twitter Thread | 小红书 | 微信公众号 |
|------|---------------|--------|-----------|
| **整体调性** | 专业信息流 | 闺蜜聊天 | 深度报告 |
| **人称** | 第三人称/客观 | 第一人称"我" | 第一人称"笔者" |
| **称呼读者** | 无/Devs/Folks | 姐妹们/家人们/宝子们 | 各位读者/朋友们 |
| **emoji 使用** | 少量(🧵📌🔗) | 大量丰富 | 极少/不用 |
| **每段长度** | ≤280字/条 | 2-4句话换行 | 完整段落 |
| **总字数** | 每条精炼 | 300-800字 | 1000-2500字 |
| **专业术语** | 直接使用 | 需解释/口语化 | 可用但需背景 |
| **引用格式** | @username | "某位博主说..." | >"原文" —— @作者 |
| **结尾** | 链接/讨论邀请 | 互动提问+标签 | 总结+延伸阅读 |

---

### 7.1 Twitter Thread 风格

**特点：信息密集、编号清晰、专业表达、@ 引用原作者**

**重要：Thread 条数 = 搜索数量 + 2**（开头总结 + 结尾观点 + 每条搜索结果一条推文）

例如：搜索 10 条 → 生成 12 条推文的 Thread

**风格要求：**
- ✅ 每条推文独立成句，信息完整
- ✅ 使用 @ 引用原作者
- ✅ 专业术语可直接使用
- ✅ 数据和事实优先
- ❌ 不要用"姐妹们""家人们"
- ❌ 不要过多 emoji
- ❌ 不要口语化表达

```
🧵 {主题} 今日热点整理 (1/{Thread条数})

1/ 核心发现：
• {趋势1}
• {趋势2}
今天刷了上百条推文，这些是最值得关注的讨论 👇

2/ @{author1} 的观点引发热议：
"{核心内容摘要}"
→ 这说明 {简短分析}
🔗 {链接}

3/ @{author2} 分享了实战经验：
"{要点摘要}"
关键数据：{具体数字}
🔗 {链接}

... (每条搜索结果一条推文，保持简洁专业)

{n+1}/ 我的观察：
{2-3句个人见解，保持客观专业}

{n+2}/ 总结：
{主题} 正在 {趋势判断}。
相关资源和讨论见评论区 👇
```

---

### 7.2 小红书风格

**特点：活泼亲切、口语化、emoji 丰富、像朋友分享**

**风格要求：**
- ✅ 用"我"开头，像在跟朋友聊天
- ✅ 大量使用 emoji 增加可读性
- ✅ 每 2-4 句话换行，避免大段文字
- ✅ 专业术语要用口语解释
- ✅ 结尾要有互动提问
- ✅ 标签放在最后
- ❌ 不要用"笔者""综上所述"
- ❌ 不要学术化表达
- ❌ 不要长段落

```
标题选项（任选风格）：
- {主题}今日热点｜刷完X我整个人都不好了！
- 姐妹们！{主题}又有大瓜了🍉
- 码住！{主题}最新动态整理｜建议收藏⭐
- 啊啊啊！关于{主题}我有话说！

正文:
姐妹们/家人们！👋

今天刷 X(推特) 看到好多关于 {主题} 的讨论
我整理了最有价值的几条，分享给你们！

💡 发现一：{用口语重新表述要点1}
简单说就是 {大白话解释}
这对我们意味着 {实际影响}

💡 发现二：{口语化要点2}
有个博主说得特别好 👉 "{简短引用}"
我觉得 {个人感受}

💡 发现三：{口语化要点3}
这个真的绝了！{为什么绝}

📌 我的感受：
说实话 {真实想法}
{主题} 确实 {判断}
以后还会持续关注分享给大家～

---
💬 你们怎么看？评论区聊聊！
📣 觉得有用的话点赞收藏支持一下～

#{主题} #科技圈 #AI干货 #程序员日常 #涨知识
```

---

### 7.3 微信公众号风格

**特点：深度专业、结构清晰、引用规范、适合深度阅读**

**风格要求：**
- ✅ 正式书面语
- ✅ 完整的段落结构
- ✅ 引用需标注来源
- ✅ 数据需注明出处
- ✅ 包含背景介绍和延伸阅读
- ❌ 不要用 emoji（可少量用于分隔）
- ❌ 不要口语化
- ❌ 不要碎片化表达

```
标题: {主题}深度观察：Twitter 上的 {数量} 条热门讨论

今天在 Twitter 上关于 {主题} 的讨论非常热烈，我整理了 {数量} 条最有价值的内容，分享给大家。

一、核心趋势

{主题} 正在经历 {阶段/变化}。从今天的热门讨论可以看出 {数字} 个关键趋势：

1. {趋势1标题} - {详细阐述，2-3句话}

2. {趋势2标题} - {详细阐述，2-3句话}

3. {趋势3标题} - {详细阐述，2-3句话}

二、值得关注的观点

1. {观点1标题}

"@{author1} {原文引用}"

{解读和分析，3-5句话}

2. {观点2标题}

"@{author2} {原文引用}"

{解读和分析}

（依次列出核心观点...）

三、深度思考

{个人见解和思考，完整段落，200-300字}

{对未来的展望或建议}

四、延伸阅读

• {资源1名称及简介}
• {资源2名称及简介}
• {资源3名称及简介}

---
数据来源：Twitter/X，采集时间：{日期}
```

---

**必须执行 - 每个平台内容生成后立即记录：**
```bash
# Twitter Thread 生成后立即记录（JSON 数组格式）
python3 scripts/content_tracker.py generate \
  --platform twitter \
  --thread '["1/ 第一条推文内容", "2/ 第二条推文内容", "3/ 第三条推文内容"]'

# 小红书内容生成后立即记录
python3 scripts/content_tracker.py generate \
  --platform xiaohongshu \
  --title "标题" \
  --content "正文内容" \
  --hashtags "AI,科技,程序员"

# 微信公众号内容生成后立即记录
python3 scripts/content_tracker.py generate \
  --platform wechat \
  --title "标题" \
  --content "正文内容"
```
⚠️ **每生成一个平台的内容后必须立即执行对应命令记录。这样核查时才能比对预期内容与实际发布内容。**

### Step 8: 预览确认

```
📝 内容预览:

=== Twitter Thread ({Thread条数}条，基于{数量}条搜索结果) ===
[预览内容]

=== 小红书 ===
[预览内容]

=== 微信公众号 ===
[预览内容]

确认发布？(可以说"修改 Twitter 的第3条"或"小红书加个 emoji")
```

### Step 9: 执行发布

**使用 Playwright MCP 发布到各平台。**

**必须执行 - 每个平台发布后立即记录状态：**
```bash
# Twitter Thread 发布成功后
python3 scripts/content_tracker.py publish \
  --platform twitter \
  --status published \
  --count 12 \
  --url "https://x.com/user/status/xxx"

# 如果 Thread 未发完（部分发布）
python3 scripts/content_tracker.py publish \
  --platform twitter \
  --status partial \
  --count 8 \
  --error "发布中断"

# 小红书发布成功后
python3 scripts/content_tracker.py publish \
  --platform xiaohongshu \
  --status published \
  --url "https://www.xiaohongshu.com/explore/xxx"

# 微信公众号发布成功后
python3 scripts/content_tracker.py publish \
  --platform wechat \
  --status published \
  --url "https://mp.weixin.qq.com/s/xxx"

# 如果只保存为草稿
python3 scripts/content_tracker.py publish \
  --platform wechat \
  --status draft
```
⚠️ **每个平台发布完成后必须立即执行对应命令。记录实际发布状态（published/partial/draft/failed）和数量，用于最终核查。**

### Step 10: 报告结果

```
✅ 完成！

📊 本次运营统计:
- 🔍 搜索: {数量} 条 "{主题}" 相关帖子
- ❤️ 点赞: {n} 条
- 💬 回复: {n} 条
- 📱 发布: Twitter Thread ({n}条) + 小红书 + 微信公众号

🔗 发布链接:
- Twitter: https://x.com/...
- 小红书: https://...
- 微信公众号: https://mp.weixin.qq.com/...

📈 预计曝光: 基于历史数据估算
```

### Step 11: 核查验证 (必须执行!)

**必须执行 - 使用 tracker 执行自动核查：**
```bash
python3 scripts/content_tracker.py verify
```
⚠️ **发布流程结束后必须执行核查命令！这是防止漏发的最后一道防线。**

这会输出完整的核查报告：

```
🔎 发布核查:

Twitter Thread:
  预期: {n} 条推文
  实际: {m} 条已发布
  状态: ✅ 完整 / ⚠️ 未完成 (还需发布 {n-m} 条)

小红书:
  状态: ✅ 已发布 / ⚠️ 待确认

微信公众号:
  状态: ✅ 已发布 / 📝 草稿 (待管理员审核)
```

**如果发现未完成的内容，tracker 会提示需要补发的内容：**
```
💡 建议操作:
   需要补发 4 条推文:
   1. 9/ 热帖 #8: @author8...
   2. 10/ 热帖 #9: @author9...
   ...
```

**必须执行 - 补发完成后更新并重新核查：**
```bash
# 更新发布数量
python3 scripts/content_tracker.py publish --platform twitter --status published --count 12

# 重新核查，确认全部完成
python3 scripts/content_tracker.py verify
```
⚠️ **补发后必须更新状态并重新核查，直到核查报告显示所有内容已完整发布。**

---

## 内容追踪系统

为确保内容完整发布，在整个流程中使用 `ContentTracker` 记录：

### 追踪点

| 阶段 | 记录内容 | CLI 命令 |
|------|----------|----------|
| 初始化 | 主题、会话ID | `init --topic "主题"` |
| 搜索 | 查询词、时间范围、所有找到的帖子 | `search --query "关键词" --posts '[...]'` |
| 互动 | 选定的帖子、已点赞、已回复、回复内容 | `engage --action like/reply --post-id "xxx"` |
| 提炼 | 趋势、要点、引用、总结 | `distill --trends '[...]' --points '[...]'` |
| 生成 | 各平台的完整内容（Twitter Thread 每条推文） | `generate --platform twitter --thread '[...]'` |
| 发布 | 状态、已发布数量、URL、错误信息 | `publish --platform twitter --status published` |
| 核查 | 验证结果、未完成项、补救建议 | `verify` |

### CLI 命令完整列表

```bash
# 初始化新会话
python3 scripts/content_tracker.py init --topic "Claude Skill"

# 记录搜索结果
python3 scripts/content_tracker.py search \
  --query "Claude Skill" \
  --time-range "24h" \
  --posts '[{"id": "xxx", "author": "@user", "content": "...", "likes": 100}]'

# 记录互动
python3 scripts/content_tracker.py engage --action select --post-ids "id1,id2,id3"
python3 scripts/content_tracker.py engage --action like --post-id "xxx"
python3 scripts/content_tracker.py engage --action reply --post-id "xxx" --reply-text "回复内容"

# 记录提炼内容
python3 scripts/content_tracker.py distill \
  --trends '["趋势1", "趋势2"]' \
  --points '["要点1", "要点2"]' \
  --quotes '[{"text": "引用", "author": "@user"}]' \
  --summary "总结"

# 记录生成的内容
python3 scripts/content_tracker.py generate --platform twitter --thread '["1/ ...", "2/ ..."]'
python3 scripts/content_tracker.py generate --platform xiaohongshu --title "标题" --content "内容"
python3 scripts/content_tracker.py generate --platform wechat --title "标题" --content "内容"

# 记录发布状态
python3 scripts/content_tracker.py publish --platform twitter --status published --count 12 --url "https://..."
python3 scripts/content_tracker.py publish --platform xiaohongshu --status published --url "https://..."
python3 scripts/content_tracker.py publish --platform wechat --status draft

# 查看会话
python3 scripts/content_tracker.py list              # 列出所有会话
python3 scripts/content_tracker.py report            # 查看最新报告
python3 scripts/content_tracker.py report -s xxx     # 查看指定会话报告

# 执行核查
python3 scripts/content_tracker.py verify            # 核查最新会话
python3 scripts/content_tracker.py session-id        # 获取最新会话ID
```

### 核查报告示例

```
============================================================
📋 内容追踪报告
   会话ID: 20260119_143052
   主题: Claude Skill
   时间: 2026-01-19T14:30:52
============================================================

🔍 搜索阶段:
   查询: Claude Skill
   时间范围: 最近24小时
   找到帖子: 10 条

💬 互动阶段:
   选定互动: 5 条
   已点赞: 5 条
   已回复: 3 条

📝 生成内容:
   Twitter Thread: 12 条推文 (10条搜索结果 + 开头 + 结尾)
   小红书: Claude Skill今日热点｜码住！
   微信公众号: Claude Skill 深度观察

📤 发布状态:
   ⚠️ Twitter: partial (8/12 条)
   ✅ 小红书: published
   ✅ 微信公众号: draft

🔎 核查结果:
   ⚠️ Twitter Thread 未发完: 预期 12 条, 实际 8 条

============================================================
```

---

## 自然语言理解示例

| 用户说 | 解析为 |
|-------|-------|
| "10个" / "十个" / "10条" | 数量=10 |
| "最热" / "热门" / "火爆" | 排序=热度 |
| "最有价值" / "干货" / "高质量" | 排序=价值(综合指标) |
| "今天" / "24小时" / "最近" | 时间=today |
| "本周" / "这周" / "7天" | 时间=week |
| "只看看" / "不互动" / "别点赞" | 互动=否 |
| "发小红书" / "发到小红书" | 平台=xiaohongshu |
| "所有平台" / "全发" | 平台=all |
| "整理一下" / "总结" / "提炼" | 包含提炼步骤 |

---

## 配套脚本

```bash
# 检查登录状态（Step 0 必须执行）
python3 scripts/check_login.py

# 检查单个平台
python3 scripts/check_login.py -p twitter

# JSON 格式输出（供程序调用）
python3 scripts/check_login.py --json
```

**登录方式：** 使用 Playwright MCP 访问对应平台进行登录，Cookie 会自动保存。

---

## 强制执行规则

⚠️ **以下 Python 脚本调用是强制执行的，不是可选项：**

| 时机 | 必须执行的命令 |
|------|----------------|
| 开始前 | `python3 scripts/check_login.py` |
| 确认需求后 | `python3 scripts/content_tracker.py init --topic "..."` |
| 搜索完成后 | `python3 scripts/content_tracker.py search ...` |
| 每次互动后 | `python3 scripts/content_tracker.py engage ...` |
| 提炼完成后 | `python3 scripts/content_tracker.py distill ...` |
| 每平台内容生成后 | `python3 scripts/content_tracker.py generate ...` |
| 每平台发布后 | `python3 scripts/content_tracker.py publish ...` |
| 流程结束时 | `python3 scripts/content_tracker.py verify` |

**不执行这些命令将导致：**
- 无法准确核查发布状态
- 无法检测漏发内容
- 无法生成追踪报告

---

## Cookie 持久化

存储: `.social_publisher/cookies/`

| 平台 | 登录方式 |
|------|----------|
| Twitter/X | 账号密码 / Google |
| 微信公众号 | 扫码 |
| 小红书 | 扫码 |

---

## Dependencies
- Playwright MCP (浏览器自动化)
- WebSearch (补充搜索)
- Bash (执行脚本)
