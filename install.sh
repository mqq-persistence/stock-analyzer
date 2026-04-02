#!/bin/bash
# 股票分析工具 - 安装脚本
# 支持多种安装方式

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}✓${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# 检查 Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        error "未找到 Python，请安装 Python 3.10+"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    info "Python 版本：$PYTHON_VERSION"
}

# 检查 pip
check_pip() {
    if $PYTHON_CMD -m pip --version &> /dev/null; then
        PIP_CMD="$PYTHON_CMD -m pip"
    elif command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        error "未找到 pip"
        exit 1
    fi

    info "pip: $($PIP_CMD --version)"
}

# 创建虚拟环境（可选）
create_venv() {
    if [ "$USE_VENV" = "true" ]; then
        if [ ! -d "venv" ]; then
            info "创建虚拟环境..."
            $PYTHON_CMD -m venv venv
            source venv/bin/activate
            info "虚拟环境已创建并激活"
        else
            info "虚拟环境已存在，激活..."
            source venv/bin/activate
        fi
    fi
}

# 安装依赖
install_deps() {
    info "安装项目依赖..."
    $PIP_CMD install -e ".[dev]" --quiet

    if [ $? -eq 0 ]; then
        info "依赖安装成功"
    else
        error "依赖安装失败"
        exit 1
    fi
}

# 验证安装
verify_install() {
    info "验证安装..."
    if $PYTHON_CMD -c "import src.stock_analyzer" 2>/dev/null; then
        info "模块导入成功"
    else
        error "模块导入失败"
        exit 1
    fi
}

# 显示使用说明
show_usage() {
    echo ""
    echo "========================================"
    echo "  安装完成！"
    echo "========================================"
    echo ""
    echo "使用方式:"
    echo "  python -m src.stock_analyzer.cli                    # 分析最新交易日"
    echo "  python -m src.stock_analyzer.cli 20260403           # 分析指定日期"
    echo "  pytest                                              # 运行测试"
    echo ""
    echo "作为 Claude Code Skill 使用:"
    echo "  1. 在 Claude Code 中：/install your-username/stock-analyzer"
    echo "  2. 或使用：/skill enable limit-up-analysis"
    echo "  3. 然后说：'分析今天的涨停股'"
    echo ""
}

# 解析参数
USE_VENV="false"
SKIP_VERIFY="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --venv)
            USE_VENV="true"
            shift
            ;;
        --skip-verify)
            SKIP_VERIFY="true"
            shift
            ;;
        -h|--help)
            echo "用法：$0 [选项]"
            echo ""
            echo "选项:"
            echo "  --venv       创建并使用虚拟环境"
            echo "  --skip-verify 跳过安装验证"
            echo "  -h, --help   显示帮助"
            exit 0
            ;;
        *)
            error "未知选项：$1"
            exit 1
            ;;
    esac
done

# 主流程
echo "========================================"
echo "  股票分析工具 - 安装程序"
echo "========================================"
echo ""

check_python
check_pip
create_venv
install_deps

if [ "$SKIP_VERIFY" != "true" ]; then
    verify_install
fi

show_usage
