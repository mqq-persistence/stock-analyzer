#!/bin/bash
# Claude Code Skill 安装器
# 用于从 GitHub 安装 Skill

set -e

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SKILLS_DIR="$HOME/.claude/skills"

usage() {
    echo "用法：$0 <github-repo-url> [local-name]"
    echo ""
    echo "示例:"
    echo "  $0 https://github.com/your-username/stock-analyzer"
    echo "  $0 https://github.com/your-username/stock-analyzer stock-analyzer"
    echo ""
    echo "或者使用 repo 简写:"
    echo "  $0 your-username/stock-analyzer"
    exit 1
}

info() {
    echo -e "${GREEN}✓${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

# 检查参数
if [ $# -lt 1 ]; then
    usage
fi

REPO_URL="$1"
LOCAL_NAME="${2:-}"

# 转换简写格式为完整 URL
if [[ "$REPO_URL" != "http*" ]]; then
    # 格式：username/repo
    REPO_URL="https://github.com/${REPO_URL}.git"
fi

# 提取 repo 名称作为本地目录名
if [ -z "$LOCAL_NAME" ]; then
    LOCAL_NAME=$(basename "$REPO_URL" .git)
fi

# 创建 skills 目录
if [ ! -d "$SKILLS_DIR" ]; then
    info "创建 skills 目录：$SKILLS_DIR"
    mkdir -p "$SKILLS_DIR"
fi

# 检查是否已存在
TARGET_DIR="$SKILLS_DIR/$LOCAL_NAME"
if [ -d "$TARGET_DIR" ]; then
    warn "目录已存在：$TARGET_DIR"
    read -p "是否删除并重新安装？[y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$TARGET_DIR"
    else
        error "安装取消"
    fi
fi

# 克隆仓库
info "克隆仓库：$REPO_URL"
git clone --depth 1 "$REPO_URL" "$TARGET_DIR"

# 检查是否有 skill.json 或 install.sh
cd "$TARGET_DIR"

if [ -f "install.sh" ]; then
    info "运行安装脚本..."
    chmod +x install.sh
    ./install.sh --skip-verify
fi

if [ -f "skill.json" ]; then
    info "检测到 skill.json，Skill 已就绪"
fi

# 复制 skills 目录到全局（如果存在）
if [ -d "skills" ]; then
    info "注册 Skill 文件..."
    # 复制每个 skill 文件
    for skill_file in skills/*.md; do
        if [ -f "$skill_file" ]; then
            skill_name=$(basename "$skill_file")
            cp "$skill_file" "$SKILLS_DIR/$skill_name"
            info "  已注册：$skill_name"
        fi
    done
fi

echo ""
echo "========================================"
info "Skill 安装完成！"
echo "========================================"
echo ""
echo "安装位置：$TARGET_DIR"
echo "Skill 文件：$SKILLS_DIR/*.md"
echo ""
echo "使用方法:"
echo "  在 Claude Code 中直接说：'分析今天的涨停股'"
echo ""
