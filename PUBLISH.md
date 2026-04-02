# GitHub Skill 发布清单

## 发布状态 ✅

- [x] 更新 skill.json
- [x] 更新 README.md
- [x] 更新 INSTALL.md
- [x] 推送到 GitHub: https://github.com/mqq-persistence/stock-analyzer

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

## 安装方式

### 方式 1: 使用全局安装脚本

```bash
# 下载安装脚本
curl -o ~/bin/install-skill https://raw.githubusercontent.com/mqq-persistence/stock-analyzer/main/scripts/install_skill.py
chmod +x ~/bin/install-skill

# 安装 Skill
install-skill mqq-persistence/stock-analyzer
```

### 方式 2: 手动克隆

```bash
git clone https://github.com/mqq-persistence/stock-analyzer.git ~/.claude/skills/stock-analyzer
cd ~/.claude/skills/stock-analyzer
pip install -e .
```

### 方式 3: 使用项目安装脚本

```bash
git clone https://github.com/mqq-persistence/stock-analyzer.git
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

MIT License
