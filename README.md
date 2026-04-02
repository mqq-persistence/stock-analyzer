# Stock Analyzer - 涨停股分析工具

基于 AKShare 数据源的涨停股筛选与分析工具，帮助投资者识别高质量涨停标的。

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 功能特性

- **涨停股池获取** - 调用 AKShare 接口获取指定交易日所有涨停股
- **封板强度筛选** - 剔除成交额≤1 亿的股票，按封板成交比取前 25 只
- **换手率过滤** - 保留换手率在 10%-20% 之间的股票
- **板块强度评估** - 剔除板块下跌或活跃度低的股票
- **格式化输出** - 返回 JSON 格式的分析结果

## 快速开始

### 方式 1: 本地安装使用

```bash
# 克隆仓库
git clone https://github.com/mqq-persistence/stock-analyzer.git
cd stock-analyzer

# 安装依赖
pip install -e ".[dev]"

# 运行分析
python -m src.stock_analyzer.cli                    # 分析最新交易日
python -m src.stock_analyzer.cli 20260403           # 分析指定日期
```

### 方式 2: 作为 Claude Code Skill 使用

#### 安装 Skill

```bash
# 在 Claude Code 中，使用 /install 命令
/install your-username/stock-analyzer

# 或者手动克隆后启用
git clone https://github.com/mqq-persistence/stock-analyzer.git ~/.claude/skills/stock-analyzer
```

#### 使用 Skill

安装后，在 Claude Code 对话中直接说：

- "分析今天的涨停股"
- "筛选封板强度高的股票"
- "涨停股池分析"

## 筛选标准

| 指标       | 阈值      | 说明           |
| ---------- | --------- | -------------- |
| 成交额     | > 1 亿    | 确保流动性充足 |
| 封板成交比 | 前 25     | 封板强度排名   |
| 换手率     | 10% - 20% | 适中活跃度     |
| 板块涨跌幅 | ≥ 0%      | 板块不拖后腿   |

## 输出字段

```json
[
  {
    "code": "000001",
    "name": "股票名称",
    "amount": 15.5,
    "order_amount": 3.2,
    "ratio": 0.206,
    "turnover": 12.5,
    "sector": "所属板块"
  }
]
```

| 字段         | 说明       | 单位 |
| ------------ | ---------- | ---- |
| code         | 股票代码   | -    |
| name         | 股票名称   | -    |
| amount       | 成交额     | 亿元 |
| order_amount | 封单金额   | 亿元 |
| ratio        | 封板成交比 | -    |
| turnover     | 换手率     | %    |
| sector       | 所属板块   | -    |

## 技术栈

- **Python 3.10+**
- **AKShare** - 股票数据源（东方财富网）
- **Pandas** - 数据处理
- **NumPy** - 数值计算
- **pytest** - 单元测试

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/ tests/

# 代码检查
ruff check src/ tests/
```

## 项目结构

```
stock-analyzer/
├── src/stock_analyzer/
│   ├── __init__.py         # 包初始化
│   ├── __main__.py         # python -m 入口
│   ├── cli.py              # 命令行入口
│   └── limit_up.py         # 涨停分析核心模块
├── tests/
│   └── test_limit_up.py    # 单元测试
├── skills/
│   └── limit-up-analysis.md  # Claude Code Skill 文档
├── skill.json              # Skill 元数据配置
├── pyproject.toml          # 项目配置
└── README.md
```

## 作为 Skill 分发

本项目设计为可作为 Claude Code Skill 分发：

1. **skill.json** - 包含 Skill 元数据（名称、版本、触发词、依赖等）
2. **skills/\*.md** - Skill 说明文档，描述功能和使用方式
3. **install.sh** - 一键安装脚本

### 发布到 GitHub

```bash
# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库并推送
git remote add origin https://github.com/mqq-persistence/stock-analyzer.git
git push -u origin main
```

### 安装使用

```bash
# 方法 1: 使用 /install 命令（如果 Claude Code 支持）
/install your-username/stock-analyzer

# 方法 2: 手动克隆到 skills 目录
git clone https://github.com/your-username/stock-analyzer.git ~/.claude/skills/stock-analyzer

# 方法 3: 下载后复制
# 下载 ZIP 解压，将 skills 目录复制到 ~/.claude/skills/
```

## 许可证

MIT License
