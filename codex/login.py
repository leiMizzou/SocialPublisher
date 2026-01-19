#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
COOKIES_DIR = ROOT_DIR / ".social_publisher" / "cookies"

PLATFORMS = {
    "twitter": {
        "url": "https://x.com/login",
        "cookie_file": "twitter_cookies.json",
    },
    "wechat": {
        "url": "https://mp.weixin.qq.com",
        "cookie_file": "wechat_cookies.json",
    },
    "xiaohongshu": {
        "url": "https://creator.xiaohongshu.com",
        "cookie_file": "xiaohongshu_cookies.json",
    },
}


def login_platform(platform: str, headless: bool) -> Path:
    config = PLATFORMS[platform]
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)
    cookie_path = COOKIES_DIR / config["cookie_file"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(config["url"], wait_until="domcontentloaded")

        print(f"Login in the browser window: {config['url']}")
        input("Press Enter after login completes to save cookies...")

        cookies = context.cookies()
        with open(cookie_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=True, indent=2)

        context.close()
        browser.close()

    return cookie_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Codex login helper (isolated from Claude Skill).")
    parser.add_argument(
        "--platform",
        "-p",
        choices=sorted(PLATFORMS.keys()) + ["all"],
        default="all",
        help="Which platform to login",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser headless (not recommended for QR logins)",
    )
    args = parser.parse_args()

    platforms = list(PLATFORMS.keys()) if args.platform == "all" else [args.platform]
    for platform in platforms:
        path = login_platform(platform, headless=args.headless)
        print(f"Saved cookies: {path}")


if __name__ == "__main__":
    main()
