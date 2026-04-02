# 涨停股分析技能

分析指定交易日的涨停股，筛选出封板强度高、换手率适中的优质标的。

## 触发条件

当用户需要：
- 分析涨停股数据
- 筛选强势涨停股票
- 获取涨停股池并进行过滤
- 评估板块强度和封板质量

## 执行流程

### 1. 获取涨停股池
调用 AKShare 接口获取指定交易日所有涨停股数据。

### 2. 筛选封板强度
- 剔除成交额 ≤ 1 亿元的股票（排除流动性不足的标的）
- 计算封板成交比（封单金额 / 成交额）
- 按封板成交比取前 25 只股票

### 3. 过滤换手率
保留换手率在 10% - 20% 之间的股票：
- < 10%：交投不够活跃
- > 20%：可能存在过度投机

### 4. 评估板块强度
- 剔除板块下跌的股票
- 评估板块活跃度

### 5. 格式化输出
返回包含以下字段的 JSON 列表：
- `code`: 股票代码
- `name`: 股票名称
- `amount`: 成交额（亿元）
- `order_amount`: 封单金额（亿元）
- `ratio`: 封板成交比
- `turnover`: 换手率（%）
- `sector`: 所属板块

## 技术实现

```python
# 使用示例
from src.stock_analyzer.limit_up import LimitUpAnalyzer

analyzer = LimitUpAnalyzer()
result = analyzer.analyze(date="20260402")  # 指定日期或留空使用最新数据
```

## 依赖配置

- `akshare>=1.12.0` - 股票数据源（东方财富网）
- `pandas>=2.0.0` - 数据处理
- `numpy>=1.24.0` - 数值计算

## 筛选标准说明

| 指标 | 阈值 | 说明 |
|------|------|------|
| 成交额 | > 1 亿 | 确保流动性充足 |
| 封板成交比 | 前 25 | 封板强度排名 |
| 换手率 | 10% - 20% | 适中活跃度 |
| 板块涨跌幅 | ≥ 0% | 板块不拖后腿 |

## 输出示例

```json
[
  {
    "code": "000001",
    "name": "平安银行",
    "amount": 15.5,
    "order_amount": 3.2,
    "ratio": 0.206,
    "turnover": 12.5,
    "sector": "银行"
  }
]
```

## 使用方式

### 方式 1：命令行运行
```bash
# 分析最新交易日
python -m src.stock_analyzer.cli

# 分析指定日期
python -m src.stock_analyzer.cli 20260402
```

### 方式 2：Python 代码调用
```python
from src.stock_analyzer.limit_up import LimitUpAnalyzer

analyzer = LimitUpAnalyzer()

# 完整分析流程
result = analyzer.analyze()  # 最新交易日
result = analyzer.analyze(date="20260402")  # 指定日期

# 分步调用
df = analyzer.get_limit_up_pool("20260402")
df = analyzer.filter_amount(df)
df = analyzer.calculate_ratio(df)
df = analyzer.sort_by_ratio(df, top_n=25)
df = analyzer.filter_turnover(df)
df = analyzer.evaluate_sector(df)
result = analyzer.format_output(df)
```

### 方式 3：Skill 触发
在对话中描述以下需求时自动触发此技能：
- "分析今天的涨停股"
- "筛选封板强度高的股票"
- "获取涨停股池并过滤"
- "看看哪些涨停股值得关注和打板"
