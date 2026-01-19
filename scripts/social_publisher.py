#!/usr/bin/env python3
"""
社交媒体多平台发布工具
支持: Twitter/X, 微信公众号, 小红书
特性: Cookie持久化，只需首次扫码登录
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext

# 配置目录
CONFIG_DIR = Path(__file__).parent.parent / ".social_publisher"
COOKIES_DIR = CONFIG_DIR / "cookies"
CONTENT_DIR = CONFIG_DIR / "content"

# 平台配置
PLATFORMS = {
    "wechat": {
        "name": "微信公众号",
        "url": "https://mp.weixin.qq.com",
        "login_url": "https://mp.weixin.qq.com",
        "cookie_file": "wechat_cookies.json",
    },
    "xiaohongshu": {
        "name": "小红书",
        "url": "https://creator.xiaohongshu.com",
        "login_url": "https://creator.xiaohongshu.com/login",
        "cookie_file": "xiaohongshu_cookies.json",
    }
}


def ensure_dirs():
    """确保配置目录存在"""
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)


async def save_cookies(context: BrowserContext, platform: str):
    """保存 cookies 到文件"""
    cookies = await context.cookies()
    cookie_file = COOKIES_DIR / PLATFORMS[platform]["cookie_file"]
    with open(cookie_file, "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"✅ {PLATFORMS[platform]['name']} cookies 已保存")


async def load_cookies(context: BrowserContext, platform: str) -> bool:
    """从文件加载 cookies"""
    cookie_file = COOKIES_DIR / PLATFORMS[platform]["cookie_file"]
    if cookie_file.exists():
        with open(cookie_file, "r") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        print(f"✅ {PLATFORMS[platform]['name']} cookies 已加载")
        return True
    return False


async def check_login_status(page, platform: str) -> bool:
    """检查登录状态"""
    if platform == "wechat":
        # 微信公众号：检查是否在登录页面
        await page.goto(PLATFORMS[platform]["url"])
        await page.wait_for_load_state("networkidle")
        return "login" not in page.url.lower()

    elif platform == "xiaohongshu":
        # 小红书：检查是否在登录页面
        await page.goto(PLATFORMS[platform]["url"])
        await page.wait_for_load_state("networkidle")
        return "login" not in page.url.lower()

    return False


async def wait_for_login(page, platform: str):
    """等待用户扫码登录"""
    print(f"\n🔐 请扫码登录 {PLATFORMS[platform]['name']}...")
    print("   登录成功后会自动继续")

    # 等待URL变化（离开登录页面）
    while "login" in page.url.lower():
        await asyncio.sleep(1)

    # 等待页面加载完成
    await page.wait_for_load_state("networkidle")
    print(f"✅ {PLATFORMS[platform]['name']} 登录成功!")


async def publish_to_wechat(page, title: str, content: str, summary: str):
    """发布到微信公众号"""
    print("\n📝 正在发布到微信公众号...")

    # 点击创建文章
    await page.click('text=文章')
    await page.wait_for_load_state("networkidle")

    # 切换到新标签页
    pages = page.context.pages
    if len(pages) > 1:
        page = pages[-1]

    await asyncio.sleep(2)

    # 关闭可能的弹窗
    try:
        await page.click('text=我知道了', timeout=3000)
    except:
        pass

    # 填写标题
    await page.fill('input[placeholder*="标题"]', title)

    # 填写正文
    editor = page.locator('.edui-body-container, .ProseMirror, [contenteditable="true"]').first
    await editor.click()
    await editor.fill(content)

    # 填写摘要
    try:
        summary_input = page.locator('textarea[placeholder*="摘要"]').first
        await summary_input.fill(summary)
    except:
        pass

    print("✅ 微信公众号内容已填写，请手动检查并发布")


async def publish_to_xiaohongshu(page, title: str, content: str):
    """发布到小红书"""
    print("\n📝 正在发布到小红书...")

    # 导航到首页
    await page.goto("https://creator.xiaohongshu.com/new/home")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(2)

    # 点击发布图文笔记 -> 文字配图
    try:
        await page.click('text=发布图文笔记')
        await asyncio.sleep(1)
    except:
        pass

    # 取消文件选择对话框（如果出现）
    page.on("filechooser", lambda fc: fc.set_files([]))

    # 点击文字配图
    await page.click('text=文字配图')
    await asyncio.sleep(1)

    # 输入文字内容
    text_input = page.locator('textarea, [contenteditable="true"]').first
    await text_input.fill(content[:500])  # 小红书文字配图有字数限制

    # 点击生成图片
    await page.click('text=生成图片')
    await asyncio.sleep(3)

    # 选择科技风格
    try:
        await page.click('text=科技')
    except:
        pass

    # 点击下一步
    await page.click('text=下一步')
    await asyncio.sleep(2)

    # 填写标题
    title_input = page.locator('input[placeholder*="标题"]').first
    await title_input.fill(title)

    # 填写正文（带话题标签）
    content_input = page.locator('textarea, [contenteditable="true"]').first
    await content_input.fill(content)

    print("✅ 小红书内容已填写，请手动检查并发布")


def adapt_content_for_platform(base_content: dict, platform: str) -> dict:
    """根据平台特点调整内容"""
    title = base_content.get("title", "")
    content = base_content.get("content", "")
    summary = base_content.get("summary", "")

    if platform == "wechat":
        # 微信公众号：正式风格
        return {
            "title": title,
            "content": content,
            "summary": summary[:120] if summary else content[:120]
        }

    elif platform == "xiaohongshu":
        # 小红书：活泼风格 + 话题标签
        xhs_title = title.replace("汇总", "｜码住！")
        xhs_content = content
        if "#" not in xhs_content:
            xhs_content += "\n\n#AI #人工智能 #科技热点 #AI工具 #程序员"
        return {
            "title": xhs_title,
            "content": xhs_content
        }

    return base_content


async def login_platform(platform: str, headless: bool = False):
    """登录指定平台并保存 cookies"""
    ensure_dirs()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        # 尝试加载已有 cookies
        has_cookies = await load_cookies(context, platform)

        # 检查登录状态
        is_logged_in = await check_login_status(page, platform)

        if not is_logged_in:
            # 需要登录
            await page.goto(PLATFORMS[platform]["login_url"])
            await wait_for_login(page, platform)

        # 保存 cookies
        await save_cookies(context, platform)

        await browser.close()
        print(f"\n✅ {PLATFORMS[platform]['name']} 登录完成，cookies 已保存")


async def publish_content(content: dict, platforms: list = None, headless: bool = False):
    """发布内容到指定平台"""
    ensure_dirs()

    if platforms is None:
        platforms = ["wechat", "xiaohongshu"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)

        for platform in platforms:
            if platform not in PLATFORMS:
                print(f"⚠️ 未知平台: {platform}")
                continue

            print(f"\n{'='*50}")
            print(f"📱 处理平台: {PLATFORMS[platform]['name']}")
            print('='*50)

            context = await browser.new_context()
            page = await context.new_page()

            # 加载 cookies
            has_cookies = await load_cookies(context, platform)

            # 检查登录状态
            is_logged_in = await check_login_status(page, platform)

            if not is_logged_in:
                print(f"⚠️ {PLATFORMS[platform]['name']} 未登录")
                await page.goto(PLATFORMS[platform]["login_url"])
                await wait_for_login(page, platform)
                await save_cookies(context, platform)

            # 适配内容
            adapted_content = adapt_content_for_platform(content, platform)

            # 发布
            if platform == "wechat":
                await publish_to_wechat(
                    page,
                    adapted_content["title"],
                    adapted_content["content"],
                    adapted_content.get("summary", "")
                )
            elif platform == "xiaohongshu":
                await publish_to_xiaohongshu(
                    page,
                    adapted_content["title"],
                    adapted_content["content"]
                )

            # 保存 cookies（更新）
            await save_cookies(context, platform)

            # 等待用户操作
            input(f"\n按 Enter 继续处理下一个平台...")

            await context.close()

        await browser.close()


# ============ CLI 接口 ============

def cmd_login(args):
    """登录命令"""
    platform = args.platform if hasattr(args, 'platform') else None

    if platform:
        asyncio.run(login_platform(platform, headless=False))
    else:
        # 登录所有平台
        for p in PLATFORMS:
            asyncio.run(login_platform(p, headless=False))


def cmd_publish(args):
    """发布命令"""
    content = {
        "title": args.title,
        "content": args.content,
        "summary": args.summary if hasattr(args, 'summary') else ""
    }

    platforms = args.platforms.split(",") if hasattr(args, 'platforms') and args.platforms else None

    asyncio.run(publish_content(content, platforms, headless=False))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="社交媒体多平台发布工具")
    subparsers = parser.add_subparsers(dest="command")

    # login 命令
    login_parser = subparsers.add_parser("login", help="登录平台并保存 cookies")
    login_parser.add_argument("-p", "--platform", choices=list(PLATFORMS.keys()), help="指定平台")

    # publish 命令
    publish_parser = subparsers.add_parser("publish", help="发布内容")
    publish_parser.add_argument("-t", "--title", required=True, help="标题")
    publish_parser.add_argument("-c", "--content", required=True, help="内容")
    publish_parser.add_argument("-s", "--summary", help="摘要")
    publish_parser.add_argument("-p", "--platforms", help="平台列表，逗号分隔 (wechat,xiaohongshu)")

    # status 命令
    status_parser = subparsers.add_parser("status", help="查看登录状态")

    args = parser.parse_args()

    if args.command == "login":
        cmd_login(args)
    elif args.command == "publish":
        cmd_publish(args)
    elif args.command == "status":
        for platform, config in PLATFORMS.items():
            cookie_file = COOKIES_DIR / config["cookie_file"]
            status = "✅ 已登录" if cookie_file.exists() else "❌ 未登录"
            print(f"{config['name']}: {status}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
