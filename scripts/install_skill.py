#!/usr/bin/env python3
"""
Claude Code Skill 安装器

用法:
    python install_skill.py <github-repo>
    python install_skill.py your-username/stock-analyzer
    python install_skill.py https://github.com/your-username/stock-analyzer
"""

import os
import sys
import subprocess
import json
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

def green(text):
    return f"\033[0;32m✓\033[0m {text}"

def yellow(text):
    return f"\033[1;33m⚠\033[0m {text}"

def red(text):
    return f"\033[0;31m✗\033[0m {text}"

def run_cmd(cmd, cwd=None):
    """运行 shell 命令"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def parse_repo_url(repo_input):
    """解析仓库输入为完整 GitHub URL"""
    if repo_input.startswith("http"):
        return repo_input
    elif "/" in repo_input and "." not in repo_input.split("/")[0]:
        # 格式：username/repo
        return f"https://github.com/{repo_input}.git"
    else:
        return None

def install_skill(repo_url, local_name=None):
    """安装 Skill"""
    # 解析 URL
    full_url = parse_repo_url(repo_url)
    if not full_url:
        print(red(f"无效的仓库地址：{repo_url}"))
        print("请使用格式：username/repo 或 https://github.com/username/repo")
        return False

    # 提取本地名称
    if not local_name:
        local_name = full_url.rstrip(".git").split("/")[-1]

    target_dir = SKILLS_DIR / local_name

    # 创建 skills 目录
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # 检查是否已存在
    if target_dir.exists():
        print(yellow(f"目录已存在：{target_dir}"))
        response = input("是否删除并重新安装？[y/N]: ")
        if response.lower() != 'y':
            print("安装取消")
            return False
        import shutil
        shutil.rmtree(target_dir)

    # 克隆仓库
    print(green(f"克隆仓库：{full_url}"))
    success, stdout, stderr = run_cmd(f"git clone --depth 1 {full_url} {target_dir}")

    if not success:
        print(red(f"克隆失败：{stderr}"))
        return False

    # 检查并运行安装脚本
    install_script = target_dir / "install.sh"
    if install_script.exists():
        print(green("运行安装脚本..."))
        os.chmod(install_script, 0o755)
        success, _, stderr = run_cmd(f"bash {install_script} --skip-verify", cwd=target_dir)
        if not success:
            print(yellow(f"安装脚本警告：{stderr}"))

    # 检查 skill.json
    skill_json = target_dir / "skill.json"
    if skill_json.exists():
        print(green("检测到 skill.json，Skill 已就绪"))
        try:
            with open(skill_json) as f:
                skill_data = json.load(f)
            print(f"  名称：{skill_data.get('name', 'N/A')}")
            print(f"  版本：{skill_data.get('version', 'N/A')}")
            print(f"  描述：{skill_data.get('description', 'N/A')}")
        except:
            pass

    # 复制 skills 目录到全局
    skills_src = target_dir / "skills"
    if skills_src.exists():
        print(green("注册 Skill 文件..."))
        for skill_file in skills_src.glob("*.md"):
            dest = SKILLS_DIR / skill_file.name
            import shutil
            shutil.copy2(skill_file, dest)
            print(f"  已注册：{skill_file.name}")

    # 安装 Python 依赖
    pyproject = target_dir / "pyproject.toml"
    if pyproject.exists():
        print(green("安装 Python 依赖..."))
        success, stdout, stderr = run_cmd(f"pip install -e {target_dir}", cwd=target_dir)
        if not success:
            print(yellow(f"依赖安装警告：{stderr}"))

    print("\n" + "=" * 50)
    print(green("Skill 安装完成！"))
    print("=" * 50)
    print(f"\n安装位置：{target_dir}")
    print(f"Skill 文件：{SKILLS_DIR}/*.md")
    print("\n使用方法:")
    print("  在 Claude Code 中直接说：'分析今天的涨停股'")
    print()

    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例:")
        print("  python install_skill.py your-username/stock-analyzer")
        print("  python install_skill.py https://github.com/your-username/stock-analyzer")
        sys.exit(1)

    repo_url = sys.argv[1]
    local_name = sys.argv[2] if len(sys.argv) > 2 else None

    success = install_skill(repo_url, local_name)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
