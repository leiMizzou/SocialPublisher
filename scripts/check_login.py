#!/usr/bin/env python3
"""
登录状态检查工具
快速检查各社交平台的 Cookie 状态
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

# 配置目录
CONFIG_DIR = Path(__file__).parent.parent / ".social_publisher"
COOKIES_DIR = CONFIG_DIR / "cookies"

# 平台配置
PLATFORMS = {
    "twitter": {
        "name": "Twitter/X",
        "cookie_file": "twitter_cookies.json",
        "key_cookies": ["auth_token", "ct0"],  # 关键 cookie 名称
        "max_age_days": 30,
    },
    "wechat": {
        "name": "微信公众号",
        "cookie_file": "wechat_cookies.json",
        "key_cookies": ["slave_sid", "slave_user"],
        "max_age_days": 7,
    },
    "xiaohongshu": {
        "name": "小红书",
        "cookie_file": "xiaohongshu_cookies.json",
        "key_cookies": ["customer-sso-sid", "access-token-creator"],
        "max_age_days": 7,
    }
}


def check_cookie_file(platform: str) -> dict:
    """检查单个平台的 Cookie 状态"""
    config = PLATFORMS[platform]
    cookie_file = COOKIES_DIR / config["cookie_file"]

    result = {
        "platform": platform,
        "name": config["name"],
        "status": "unknown",
        "message": "",
        "file_exists": False,
        "cookie_count": 0,
        "has_key_cookies": False,
        "file_age_days": None,
    }

    # 检查文件是否存在
    if not cookie_file.exists():
        result["status"] = "missing"
        result["message"] = "Cookie 文件不存在，需要登录"
        return result

    result["file_exists"] = True

    # 检查文件年龄
    file_mtime = datetime.fromtimestamp(cookie_file.stat().st_mtime)
    age = datetime.now() - file_mtime
    result["file_age_days"] = age.days

    # 读取 Cookie 内容
    try:
        with open(cookie_file, "r") as f:
            cookies = json.load(f)
        result["cookie_count"] = len(cookies)
    except (json.JSONDecodeError, IOError) as e:
        result["status"] = "error"
        result["message"] = f"Cookie 文件损坏: {e}"
        return result

    # 检查关键 Cookie 是否存在
    cookie_names = {c.get("name", "") for c in cookies}
    key_cookies = set(config["key_cookies"])
    found_keys = cookie_names & key_cookies
    result["has_key_cookies"] = len(found_keys) > 0

    # 判断状态
    max_age = config["max_age_days"]

    if not result["has_key_cookies"]:
        result["status"] = "invalid"
        result["message"] = "缺少关键 Cookie，需要重新登录"
    elif age.days > max_age:
        result["status"] = "expired"
        result["message"] = f"Cookie 已过期 ({age.days} 天前更新，建议 {max_age} 天内刷新)"
    elif age.days > max_age * 0.7:
        result["status"] = "warning"
        result["message"] = f"Cookie 即将过期 ({age.days} 天前更新)"
    else:
        result["status"] = "ok"
        result["message"] = f"正常 ({age.days} 天前更新)"

    return result


def check_all() -> list:
    """检查所有平台"""
    results = []
    for platform in PLATFORMS:
        results.append(check_cookie_file(platform))
    return results


def print_status(results: list):
    """打印状态报告"""
    print("\n" + "=" * 50)
    print("🔐 社交平台登录状态检查")
    print("=" * 50 + "\n")

    status_icons = {
        "ok": "✅",
        "warning": "⚠️",
        "expired": "❌",
        "invalid": "❌",
        "missing": "❌",
        "error": "❌",
        "unknown": "❓",
    }

    for r in results:
        icon = status_icons.get(r["status"], "❓")
        print(f"{icon} {r['name']}: {r['message']}")

        if r["file_exists"] and r["status"] not in ["missing", "error"]:
            print(f"   Cookie 数量: {r['cookie_count']}")

    print("\n" + "-" * 50)

    # 统计
    ok_count = sum(1 for r in results if r["status"] == "ok")
    warning_count = sum(1 for r in results if r["status"] == "warning")
    bad_count = sum(1 for r in results if r["status"] in ["expired", "invalid", "missing", "error"])

    if bad_count > 0:
        print(f"⚠️  {bad_count} 个平台需要重新登录")
        print("\n使用 Playwright MCP 访问对应平台进行登录：")
        for r in results:
            if r["status"] in ["expired", "invalid", "missing"]:
                if r["platform"] == "twitter":
                    print(f"   • Twitter: https://x.com/login")
                elif r["platform"] == "wechat":
                    print(f"   • 微信公众号: https://mp.weixin.qq.com")
                elif r["platform"] == "xiaohongshu":
                    print(f"   • 小红书: https://creator.xiaohongshu.com")
    elif warning_count > 0:
        print(f"⚠️  {warning_count} 个平台 Cookie 即将过期，建议刷新")
    else:
        print("✅ 所有平台登录状态正常")

    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="检查社交平台登录状态")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--platform", "-p", choices=list(PLATFORMS.keys()), help="只检查指定平台")

    args = parser.parse_args()

    # 确保目录存在
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)

    if args.platform:
        results = [check_cookie_file(args.platform)]
    else:
        results = check_all()

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_status(results)


if __name__ == "__main__":
    main()
