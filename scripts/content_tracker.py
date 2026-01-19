#!/usr/bin/env python3
"""
内容追踪和核查系统
用于记录社交媒体运营全流程的内容，并在发布后进行验证
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 配置目录
CONFIG_DIR = Path(__file__).parent.parent / ".social_publisher"
SESSIONS_DIR = CONFIG_DIR / "sessions"


def ensure_dirs():
    """确保目录存在"""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


class ContentTracker:
    """内容追踪器"""

    def __init__(self, topic: str):
        ensure_dirs()
        self.topic = topic
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = SESSIONS_DIR / f"session_{self.session_id}.json"

        self.data = {
            "session_id": self.session_id,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "status": "initialized",

            # Phase 1: 搜索结果
            "search": {
                "query": "",
                "time_range": "",
                "total_found": 0,
                "posts": []  # 所有找到的帖子
            },

            # Phase 2: 选定互动的帖子
            "engagement": {
                "selected_posts": [],  # 选定要互动的帖子ID
                "liked": [],           # 已点赞的帖子ID
                "replied": [],         # 已回复的帖子ID
                "replies_content": {}  # 回复内容 {post_id: reply_text}
            },

            # Phase 3: 提炼的内容
            "distilled": {
                "trends": [],
                "key_points": [],
                "quotes": [],
                "summary": ""
            },

            # Phase 4: 各平台生成的内容
            "generated_content": {
                "twitter": {
                    "thread": [],  # 每条推文
                    "total_tweets": 0
                },
                "xiaohongshu": {
                    "title": "",
                    "content": "",
                    "hashtags": []
                },
                "wechat": {
                    "title": "",
                    "content": "",
                    "summary": ""
                }
            },

            # Phase 5: 发布状态
            "publish_status": {
                "twitter": {
                    "status": "pending",  # pending, published, failed, partial
                    "published_count": 0,
                    "expected_count": 0,
                    "urls": [],
                    "errors": []
                },
                "xiaohongshu": {
                    "status": "pending",
                    "url": "",
                    "errors": []
                },
                "wechat": {
                    "status": "pending",
                    "url": "",
                    "errors": []
                }
            },

            # Phase 6: 核查结果
            "verification": {
                "verified_at": "",
                "twitter_verified": False,
                "xiaohongshu_verified": False,
                "wechat_verified": False,
                "issues": [],
                "notes": ""
            }
        }

        self._save()

    def _save(self):
        """保存会话数据"""
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, session_id: str) -> "ContentTracker":
        """加载已有会话"""
        session_file = SESSIONS_DIR / f"session_{session_id}.json"
        if not session_file.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        with open(session_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tracker = cls.__new__(cls)
        tracker.topic = data["topic"]
        tracker.session_id = session_id
        tracker.session_file = session_file
        tracker.data = data
        return tracker

    @classmethod
    def get_latest_session(cls) -> Optional["ContentTracker"]:
        """获取最新的会话"""
        ensure_dirs()
        sessions = list(SESSIONS_DIR.glob("session_*.json"))
        if not sessions:
            return None
        latest = max(sessions, key=lambda p: p.stat().st_mtime)
        session_id = latest.stem.replace("session_", "")
        return cls.load(session_id)

    # ========== Phase 1: 搜索 ==========

    def record_search(self, query: str, time_range: str, posts: List[Dict]):
        """记录搜索结果"""
        self.data["search"]["query"] = query
        self.data["search"]["time_range"] = time_range
        self.data["search"]["total_found"] = len(posts)
        self.data["search"]["posts"] = posts
        self.data["status"] = "searched"
        self._save()
        print(f"📝 已记录 {len(posts)} 条搜索结果")

    # ========== Phase 2: 互动 ==========

    def record_selected_for_engagement(self, post_ids: List[str]):
        """记录选定要互动的帖子"""
        self.data["engagement"]["selected_posts"] = post_ids
        self._save()
        print(f"📝 已记录 {len(post_ids)} 条选定互动的帖子")

    def record_like(self, post_id: str):
        """记录点赞"""
        if post_id not in self.data["engagement"]["liked"]:
            self.data["engagement"]["liked"].append(post_id)
            self._save()

    def record_reply(self, post_id: str, reply_text: str):
        """记录回复"""
        if post_id not in self.data["engagement"]["replied"]:
            self.data["engagement"]["replied"].append(post_id)
        self.data["engagement"]["replies_content"][post_id] = reply_text
        self._save()

    # ========== Phase 3: 提炼 ==========

    def record_distilled_content(self, trends: List[str], key_points: List[str],
                                  quotes: List[Dict], summary: str):
        """记录提炼的内容"""
        self.data["distilled"] = {
            "trends": trends,
            "key_points": key_points,
            "quotes": quotes,
            "summary": summary
        }
        self.data["status"] = "distilled"
        self._save()
        print(f"📝 已记录提炼内容: {len(trends)} 个趋势, {len(key_points)} 个要点")

    # ========== Phase 4: 生成内容 ==========

    def record_twitter_content(self, thread: List[str]):
        """记录 Twitter Thread 内容"""
        self.data["generated_content"]["twitter"]["thread"] = thread
        self.data["generated_content"]["twitter"]["total_tweets"] = len(thread)
        self.data["publish_status"]["twitter"]["expected_count"] = len(thread)
        self._save()
        print(f"📝 已记录 Twitter Thread: {len(thread)} 条推文")

    def record_xiaohongshu_content(self, title: str, content: str, hashtags: List[str] = None):
        """记录小红书内容"""
        self.data["generated_content"]["xiaohongshu"] = {
            "title": title,
            "content": content,
            "hashtags": hashtags or []
        }
        self._save()
        print(f"📝 已记录小红书内容: {title}")

    def record_wechat_content(self, title: str, content: str, summary: str = ""):
        """记录微信公众号内容"""
        self.data["generated_content"]["wechat"] = {
            "title": title,
            "content": content,
            "summary": summary
        }
        self._save()
        print(f"📝 已记录微信公众号内容: {title}")

    # ========== Phase 5: 发布状态 ==========

    def record_twitter_publish(self, published_count: int, urls: List[str] = None,
                                status: str = "published", error: str = None):
        """记录 Twitter 发布状态"""
        self.data["publish_status"]["twitter"]["published_count"] = published_count
        self.data["publish_status"]["twitter"]["status"] = status
        if urls:
            self.data["publish_status"]["twitter"]["urls"] = urls
        if error:
            self.data["publish_status"]["twitter"]["errors"].append(error)
        self._save()

    def record_xiaohongshu_publish(self, url: str = "", status: str = "published",
                                    error: str = None):
        """记录小红书发布状态"""
        self.data["publish_status"]["xiaohongshu"]["status"] = status
        self.data["publish_status"]["xiaohongshu"]["url"] = url
        if error:
            self.data["publish_status"]["xiaohongshu"]["errors"].append(error)
        self._save()

    def record_wechat_publish(self, url: str = "", status: str = "published",
                               error: str = None):
        """记录微信发布状态"""
        self.data["publish_status"]["wechat"]["status"] = status
        self.data["publish_status"]["wechat"]["url"] = url
        if error:
            self.data["publish_status"]["wechat"]["errors"].append(error)
        self._save()

    # ========== Phase 6: 核查 ==========

    def verify(self) -> Dict:
        """执行核查并返回结果"""
        issues = []

        # 检查 Twitter
        twitter_status = self.data["publish_status"]["twitter"]
        twitter_content = self.data["generated_content"]["twitter"]

        if twitter_status["expected_count"] > 0:
            if twitter_status["published_count"] < twitter_status["expected_count"]:
                issues.append({
                    "platform": "twitter",
                    "type": "incomplete",
                    "expected": twitter_status["expected_count"],
                    "actual": twitter_status["published_count"],
                    "message": f"Twitter Thread 未发完: 预期 {twitter_status['expected_count']} 条, 实际 {twitter_status['published_count']} 条"
                })
            elif twitter_status["status"] != "published":
                issues.append({
                    "platform": "twitter",
                    "type": "status",
                    "message": f"Twitter 状态异常: {twitter_status['status']}"
                })

        # 检查小红书
        xhs_status = self.data["publish_status"]["xiaohongshu"]
        if self.data["generated_content"]["xiaohongshu"]["title"]:
            if xhs_status["status"] != "published":
                issues.append({
                    "platform": "xiaohongshu",
                    "type": "status",
                    "message": f"小红书状态: {xhs_status['status']}"
                })

        # 检查微信
        wechat_status = self.data["publish_status"]["wechat"]
        if self.data["generated_content"]["wechat"]["title"]:
            if wechat_status["status"] not in ["published", "draft"]:
                issues.append({
                    "platform": "wechat",
                    "type": "status",
                    "message": f"微信公众号状态: {wechat_status['status']}"
                })

        # 更新核查结果
        self.data["verification"] = {
            "verified_at": datetime.now().isoformat(),
            "twitter_verified": len([i for i in issues if i["platform"] == "twitter"]) == 0,
            "xiaohongshu_verified": len([i for i in issues if i["platform"] == "xiaohongshu"]) == 0,
            "wechat_verified": len([i for i in issues if i["platform"] == "wechat"]) == 0,
            "issues": issues,
            "notes": ""
        }
        self.data["status"] = "verified"
        self._save()

        return self.data["verification"]

    def get_report(self) -> str:
        """生成核查报告"""
        report = []
        report.append("=" * 60)
        report.append(f"📋 内容追踪报告")
        report.append(f"   会话ID: {self.session_id}")
        report.append(f"   主题: {self.topic}")
        report.append(f"   时间: {self.data['created_at']}")
        report.append("=" * 60)

        # 搜索阶段
        search = self.data["search"]
        report.append(f"\n🔍 搜索阶段:")
        report.append(f"   查询: {search['query']}")
        report.append(f"   时间范围: {search['time_range']}")
        report.append(f"   找到帖子: {search['total_found']} 条")

        # 互动阶段
        engagement = self.data["engagement"]
        report.append(f"\n💬 互动阶段:")
        report.append(f"   选定互动: {len(engagement['selected_posts'])} 条")
        report.append(f"   已点赞: {len(engagement['liked'])} 条")
        report.append(f"   已回复: {len(engagement['replied'])} 条")

        # 生成内容
        generated = self.data["generated_content"]
        report.append(f"\n📝 生成内容:")
        report.append(f"   Twitter Thread: {generated['twitter']['total_tweets']} 条推文")
        report.append(f"   小红书: {generated['xiaohongshu']['title'] or '(无)'}")
        report.append(f"   微信公众号: {generated['wechat']['title'] or '(无)'}")

        # 发布状态
        publish = self.data["publish_status"]
        report.append(f"\n📤 发布状态:")

        # Twitter
        tw = publish["twitter"]
        tw_emoji = "✅" if tw["status"] == "published" and tw["published_count"] == tw["expected_count"] else "⚠️"
        report.append(f"   {tw_emoji} Twitter: {tw['status']} ({tw['published_count']}/{tw['expected_count']} 条)")

        # 小红书
        xhs = publish["xiaohongshu"]
        xhs_emoji = "✅" if xhs["status"] == "published" else "⚠️"
        report.append(f"   {xhs_emoji} 小红书: {xhs['status']}")

        # 微信
        wc = publish["wechat"]
        wc_emoji = "✅" if wc["status"] in ["published", "draft"] else "⚠️"
        report.append(f"   {wc_emoji} 微信公众号: {wc['status']}")

        # 核查结果
        if self.data["verification"]["verified_at"]:
            verification = self.data["verification"]
            report.append(f"\n🔎 核查结果:")

            if verification["issues"]:
                for issue in verification["issues"]:
                    report.append(f"   ⚠️ {issue['message']}")
            else:
                report.append("   ✅ 所有内容发布完整")

        report.append("\n" + "=" * 60)

        return "\n".join(report)

    def get_unpublished_twitter_content(self) -> List[str]:
        """获取未发布的 Twitter 内容"""
        twitter = self.data["generated_content"]["twitter"]
        publish = self.data["publish_status"]["twitter"]

        published_count = publish["published_count"]
        all_tweets = twitter["thread"]

        if published_count < len(all_tweets):
            return all_tweets[published_count:]
        return []


# ========== CLI ==========

def main():
    import argparse

    parser = argparse.ArgumentParser(description="内容追踪和核查系统")
    subparsers = parser.add_subparsers(dest="command")

    # init 命令 - 初始化新会话
    init_parser = subparsers.add_parser("init", help="初始化新会话")
    init_parser.add_argument("--topic", "-t", required=True, help="主题关键词")

    # search 命令 - 记录搜索结果
    search_parser = subparsers.add_parser("search", help="记录搜索结果")
    search_parser.add_argument("--session", "-s", help="会话ID，默认最新")
    search_parser.add_argument("--query", "-q", required=True, help="搜索查询词")
    search_parser.add_argument("--time-range", "-r", default="24h", help="时间范围")
    search_parser.add_argument("--posts", "-p", help="帖子JSON数组（或从stdin读取）")

    # engage 命令 - 记录互动
    engage_parser = subparsers.add_parser("engage", help="记录互动")
    engage_parser.add_argument("--session", "-s", help="会话ID，默认最新")
    engage_parser.add_argument("--action", "-a", choices=["select", "like", "reply"], required=True)
    engage_parser.add_argument("--post-id", "-p", help="帖子ID")
    engage_parser.add_argument("--post-ids", help="多个帖子ID，逗号分隔")
    engage_parser.add_argument("--reply-text", help="回复内容")

    # distill 命令 - 记录提炼内容
    distill_parser = subparsers.add_parser("distill", help="记录提炼内容")
    distill_parser.add_argument("--session", "-s", help="会话ID，默认最新")
    distill_parser.add_argument("--trends", help="趋势JSON数组")
    distill_parser.add_argument("--points", help="要点JSON数组")
    distill_parser.add_argument("--quotes", help="引用JSON数组")
    distill_parser.add_argument("--summary", help="总结")

    # generate 命令 - 记录生成的内容
    generate_parser = subparsers.add_parser("generate", help="记录生成的内容")
    generate_parser.add_argument("--session", "-s", help="会话ID，默认最新")
    generate_parser.add_argument("--platform", "-p", choices=["twitter", "xiaohongshu", "wechat"], required=True)
    generate_parser.add_argument("--title", "-t", help="标题")
    generate_parser.add_argument("--content", "-c", help="内容")
    generate_parser.add_argument("--thread", help="Twitter Thread JSON数组")
    generate_parser.add_argument("--hashtags", help="话题标签，逗号分隔")

    # publish 命令 - 记录发布状态
    publish_parser = subparsers.add_parser("publish", help="记录发布状态")
    publish_parser.add_argument("--session", "-s", help="会话ID，默认最新")
    publish_parser.add_argument("--platform", "-p", choices=["twitter", "xiaohongshu", "wechat"], required=True)
    publish_parser.add_argument("--status", choices=["pending", "published", "partial", "failed", "draft"], default="published")
    publish_parser.add_argument("--url", "-u", help="发布URL")
    publish_parser.add_argument("--count", "-n", type=int, help="已发布数量（Twitter用）")
    publish_parser.add_argument("--error", "-e", help="错误信息")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有会话")

    # report 命令
    report_parser = subparsers.add_parser("report", help="查看核查报告")
    report_parser.add_argument("--session", "-s", help="指定会话ID，默认最新")

    # verify 命令
    verify_parser = subparsers.add_parser("verify", help="执行核查")
    verify_parser.add_argument("--session", "-s", help="指定会话ID，默认最新")

    # session-id 命令 - 获取当前会话ID
    session_parser = subparsers.add_parser("session-id", help="获取最新会话ID")

    args = parser.parse_args()

    # ========== init ==========
    if args.command == "init":
        tracker = ContentTracker(args.topic)
        print(f"✅ 新会话已创建: {tracker.session_id}")
        print(tracker.session_id)  # 输出ID供脚本捕获

    # ========== search ==========
    elif args.command == "search":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if not tracker:
            print("❌ 未找到会话，请先运行 init")
            return

        posts = []
        if args.posts:
            posts = json.loads(args.posts)
        else:
            # 从 stdin 读取
            import sys
            if not sys.stdin.isatty():
                posts = json.load(sys.stdin)

        tracker.record_search(args.query, args.time_range, posts)

    # ========== engage ==========
    elif args.command == "engage":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if not tracker:
            print("❌ 未找到会话")
            return

        if args.action == "select":
            post_ids = args.post_ids.split(",") if args.post_ids else [args.post_id]
            tracker.record_selected_for_engagement(post_ids)
        elif args.action == "like":
            tracker.record_like(args.post_id)
            print(f"✅ 已记录点赞: {args.post_id}")
        elif args.action == "reply":
            tracker.record_reply(args.post_id, args.reply_text or "")
            print(f"✅ 已记录回复: {args.post_id}")

    # ========== distill ==========
    elif args.command == "distill":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if not tracker:
            print("❌ 未找到会话")
            return

        trends = json.loads(args.trends) if args.trends else []
        points = json.loads(args.points) if args.points else []
        quotes = json.loads(args.quotes) if args.quotes else []
        summary = args.summary or ""

        tracker.record_distilled_content(trends, points, quotes, summary)

    # ========== generate ==========
    elif args.command == "generate":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if not tracker:
            print("❌ 未找到会话")
            return

        if args.platform == "twitter":
            thread = json.loads(args.thread) if args.thread else []
            tracker.record_twitter_content(thread)
        elif args.platform == "xiaohongshu":
            hashtags = args.hashtags.split(",") if args.hashtags else []
            tracker.record_xiaohongshu_content(args.title or "", args.content or "", hashtags)
        elif args.platform == "wechat":
            tracker.record_wechat_content(args.title or "", args.content or "", "")

    # ========== publish ==========
    elif args.command == "publish":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if not tracker:
            print("❌ 未找到会话")
            return

        if args.platform == "twitter":
            tracker.record_twitter_publish(
                published_count=args.count or 0,
                urls=[args.url] if args.url else [],
                status=args.status,
                error=args.error
            )
        elif args.platform == "xiaohongshu":
            tracker.record_xiaohongshu_publish(
                url=args.url or "",
                status=args.status,
                error=args.error
            )
        elif args.platform == "wechat":
            tracker.record_wechat_publish(
                url=args.url or "",
                status=args.status,
                error=args.error
            )
        print(f"✅ 已记录 {args.platform} 发布状态: {args.status}")

    # ========== list ==========
    elif args.command == "list":
        ensure_dirs()
        sessions = list(SESSIONS_DIR.glob("session_*.json"))
        if not sessions:
            print("暂无会话记录")
            return

        print("📁 会话列表:")
        for session_file in sorted(sessions, reverse=True)[:10]:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"   {data['session_id']} - {data['topic']} ({data['status']})")

    # ========== report ==========
    elif args.command == "report":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if tracker:
            print(tracker.get_report())
        else:
            print("未找到会话记录")

    # ========== verify ==========
    elif args.command == "verify":
        tracker = ContentTracker.load(args.session) if args.session else ContentTracker.get_latest_session()
        if tracker:
            result = tracker.verify()
            print(tracker.get_report())

            if result["issues"]:
                print("\n💡 建议操作:")
                for issue in result["issues"]:
                    if issue["type"] == "incomplete" and issue["platform"] == "twitter":
                        unpublished = tracker.get_unpublished_twitter_content()
                        if unpublished:
                            print(f"   需要补发 {len(unpublished)} 条推文:")
                            for i, tweet in enumerate(unpublished, 1):
                                print(f"   {i}. {tweet[:50]}...")
        else:
            print("未找到会话记录")

    # ========== session-id ==========
    elif args.command == "session-id":
        tracker = ContentTracker.get_latest_session()
        if tracker:
            print(tracker.session_id)
        else:
            print("")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
