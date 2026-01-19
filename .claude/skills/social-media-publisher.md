# Social Media Publisher Skill

## Description
自动将内容发布到多个社交媒体平台（Twitter/X、微信公众号、小红书），并根据各平台特点优化内容格式。

**特性：Cookie 持久化，只需首次扫码登录！**

## Usage
```
/social-media-publisher [话题/内容来源] [目标平台]
```

## Parameters
- **话题/内容来源**: 可以是：
  - "AI热点" - 自动从X上搜索AI相关热门话题
  - "科技新闻" - 搜索科技相关内容
  - 自定义话题关键词
  - 或直接提供要发布的内容

- **目标平台** (可选，默认全部):
  - `twitter` - 仅发布到 Twitter/X
  - `wechat` - 仅发布到微信公众号
  - `xiaohongshu` - 仅发布到小红书
  - `all` - 发布到所有平台

## Examples
```
/social-media-publisher AI热点
/social-media-publisher AI热点 xiaohongshu
/social-media-publisher "今天学到的Python技巧" wechat
```

## 配套工具

### Python 脚本 (带 Cookie 持久化)
位置: `scripts/social_publisher.py`

```bash
# 首次使用：登录并保存 cookies
python scripts/social_publisher.py login

# 查看登录状态
python scripts/social_publisher.py status

# 发布内容
python scripts/social_publisher.py publish -t "标题" -c "内容"
```

### Shell 快捷命令
位置: `scripts/publish.sh`

```bash
# 登录所有平台
./scripts/publish.sh login

# 只登录小红书
./scripts/publish.sh login xiaohongshu

# 发布到所有平台
./scripts/publish.sh post "标题" "内容"

# 只发布到微信公众号
./scripts/publish.sh post "标题" "内容" wechat
```

## Workflow

### Step 1: 内容收集与生成
1. 根据话题在X/Twitter上搜索热门内容（如需要）
2. 使用AI整理和总结内容
3. 生成基础内容框架

### Step 2: 平台适配
根据目标平台特点优化内容：

**Twitter/X:**
- 拆分为多条推文的thread
- 每条控制在280字符内
- 简洁有力的表达

**微信公众号:**
- 正式的文章格式
- 完整的标题和摘要
- 结构化的段落
- 需要封面图（可用AI配图）

**小红书:**
- 活泼亲切的口吻（"姐妹们"、"码住"等）
- 大量使用emoji
- 添加热门话题标签 #AI #科技热点 等
- 使用"文字配图"功能生成图片

### Step 3: 发布流程
1. **Twitter**: 直接发布thread
2. **微信公众号**:
   - 打开 mp.weixin.qq.com
   - 自动加载 cookies（如已登录过）
   - 创建文章并发布
3. **小红书**:
   - 打开 creator.xiaohongshu.com
   - 自动加载 cookies（如已登录过）
   - 使用文字配图功能创建笔记并发布

## Cookie 持久化说明
- Cookies 保存在 `.social_publisher/cookies/` 目录
- 首次使用需要扫码登录，之后会自动加载
- 如果 cookies 过期，会提示重新登录
- 登录状态通常可以保持几天到几周

## Notes
- 首次使用需要扫码登录，之后自动登录
- 发布前会显示预览，确认后再发布
- 所有平台的内容会自动保存为草稿，发布失败可以手动重试

## Dependencies
- Playwright MCP (browser automation)
- WebSearch (for content discovery)
- Python 3.8+ & playwright (for cookie persistence)
