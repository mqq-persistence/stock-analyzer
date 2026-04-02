# GitHub Skill 发布清单

## 发布前准备

### 1. 更新 skill.json

修改以下字段为你的实际信息：

```json
{
  "name": "limit-up-analysis",
  "version": "1.0.0",
  "author": "Your Name",
  "repository": "https://github.com/your-username/stock-analyzer",
  "homepage": "https://github.com/your-username/stock-analyzer#readme"
}
```

### 2. 更新 README.md

替换所有 `your-username` 为你的 GitHub 用户名。

### 3. 更新 INSTALL.md

替换所有 `your-username` 为你的 GitHub 用户名。

---

## 发布步骤

### 步骤 1: 初始化 Git 仓库（如果还没有）

```bash
cd /Users/qiaozhuangzhu/companyProjects/claude-code-stock-analyzer
git init
git add .
git commit -m "Initial commit: 涨停股分析 Skill"
```

### 步骤 2: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名：`stock-analyzer`
3. 描述：`涨停股分析工具 - Claude Code Skill`
4. 设为 Public（公开）
5. 创建仓库

### 步骤 3: 推送代码

```bash
git remote add origin https://github.com/your-username/stock-analyzer.git
git branch -M main
git push -u origin main
```

---

## 安装测试

### 方式 1: 使用全局安装脚本

```bash
# 下载安装脚本
curl -o ~/bin/install-skill https://raw.githubusercontent.com/your-username/stock-analyzer/main/scripts/install_skill.py
chmod +x ~/bin/install-skill

# 安装 Skill
install-skill your-username/stock-analyzer
```

### 方式 2: 手动克隆

```bash
git clone https://github.com/your-username/stock-analyzer.git ~/.claude/skills/stock-analyzer
cd ~/.claude/skills/stock-analyzer
pip install -e .
```

### 方式 3: 使用项目安装脚本

```bash
git clone https://github.com/your-username/stock-analyzer.git
cd stock-analyzer
./install.sh
```

---

## 验证安装

在 Claude Code 中输入：

```
/skills
```

应该能看到 `limit-up-analysis.md`。

然后测试：

```
分析今天的涨停股
```

---

## 项目结构

```
stock-analyzer/
├── .github/workflows/ci.yml    # GitHub Actions CI
├── .gitignore                   # Git 忽略配置
├── .claude/index.json           # AI 上下文索引
├── src/stock_analyzer/          # 核心模块
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── limit_up.py
├── tests/
│   └── test_limit_up.py
├── skills/
│   └── limit-up-analysis.md     # Skill 说明文档
├── scripts/
│   ├── install-skill.sh         # Bash 安装器
│   └── install_skill.py         # Python 安装器
├── skill.json                   # Skill 元数据
├── pyproject.toml               # Python 项目配置
├── install.sh                   # 项目安装脚本
├── README.md                    # GitHub 主页说明
├── INSTALL.md                   # 详细安装指南
└── CLAUDE.md                    # AI 上下文文档
```

---

## 维护说明

### 更新 Skill

1. 修改代码或文档
2. 更新 `skill.json` 版本号
3. 提交并推送：

```bash
git add .
git commit -m "fix: 描述改动"
git push
```

### 用户更新已安装的 Skill

```bash
cd ~/.claude/skills/stock-analyzer
git pull
pip install -e .
```

---

## 常见问题

### Q: 安装后 Claude Code 找不到 Skill？

A: 确保 skill 文件在正确位置：
```bash
ls ~/.claude/skills/limit-up-analysis.md
```

### Q: 依赖安装失败？

A: 尝试使用 Python 3.10+ 并更新 pip：
```bash
python3 -m pip install --upgrade pip
pip install -e .
```

### Q: AKShare 数据获取失败？

A: 检查网络连接，AKShare 从东方财富网获取数据，可能需要稳定的网络环境。

---

## 许可证

MIT License - 详见 LICENSE 文件（可选添加）
