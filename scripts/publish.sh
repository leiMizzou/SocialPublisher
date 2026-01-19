#!/bin/bash
# 社交媒体发布工具 - 快捷命令

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/social_publisher.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    echo "社交媒体多平台发布工具"
    echo ""
    echo "用法:"
    echo "  publish.sh login [平台]       - 登录并保存 cookies"
    echo "  publish.sh status             - 查看登录状态"
    echo "  publish.sh post \"标题\" \"内容\" [平台]  - 发布内容"
    echo ""
    echo "平台选项:"
    echo "  wechat      - 微信公众号"
    echo "  xiaohongshu - 小红书"
    echo "  all         - 所有平台 (默认)"
    echo ""
    echo "示例:"
    echo "  publish.sh login                    # 登录所有平台"
    echo "  publish.sh login xiaohongshu        # 只登录小红书"
    echo "  publish.sh status                   # 查看登录状态"
    echo "  publish.sh post \"标题\" \"内容\"        # 发布到所有平台"
    echo "  publish.sh post \"标题\" \"内容\" wechat # 只发到微信公众号"
}

# 检查 Python 依赖
check_deps() {
    if ! python3 -c "import playwright" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  需要安装 playwright${NC}"
        echo "运行: pip install playwright && playwright install chromium"
        exit 1
    fi
}

case "$1" in
    login)
        check_deps
        if [ -n "$2" ]; then
            python3 "$PYTHON_SCRIPT" login -p "$2"
        else
            python3 "$PYTHON_SCRIPT" login
        fi
        ;;
    status)
        python3 "$PYTHON_SCRIPT" status
        ;;
    post|publish)
        check_deps
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}❌ 缺少参数${NC}"
            echo "用法: publish.sh post \"标题\" \"内容\" [平台]"
            exit 1
        fi

        TITLE="$2"
        CONTENT="$3"
        PLATFORM="${4:-all}"

        if [ "$PLATFORM" = "all" ]; then
            python3 "$PYTHON_SCRIPT" publish -t "$TITLE" -c "$CONTENT"
        else
            python3 "$PYTHON_SCRIPT" publish -t "$TITLE" -c "$CONTENT" -p "$PLATFORM"
        fi
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac
