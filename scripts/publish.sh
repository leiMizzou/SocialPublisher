#!/bin/bash
# 社交媒体发布工具 - 快捷命令

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
    echo "  publish.sh status              - 查看登录状态"
    echo "  publish.sh track <命令>        - 内容追踪命令"
    echo ""
    echo "追踪命令:"
    echo "  publish.sh track init -t <主题>     - 初始化新会话"
    echo "  publish.sh track report             - 查看报告"
    echo "  publish.sh track verify             - 执行核查"
    echo "  publish.sh track list               - 列出会话"
    echo ""
    echo "示例:"
    echo "  publish.sh status                   # 检查登录状态"
    echo "  publish.sh track init -t 'AI Agent' # 初始化追踪"
    echo "  publish.sh track verify             # 核查发布状态"
}

# 检查 Python 依赖
check_deps() {
    if ! python3 -c "import json" 2>/dev/null; then
        echo -e "${RED}❌ Python3 未安装${NC}"
        exit 1
    fi
}

case "$1" in
    status)
        check_deps
        python3 "$SCRIPT_DIR/check_login.py"
        ;;
    track)
        check_deps
        shift
        python3 "$SCRIPT_DIR/content_tracker.py" "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac
