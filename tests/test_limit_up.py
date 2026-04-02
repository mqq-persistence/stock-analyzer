"""
涨停股分析模块测试
"""

import pytest
import pandas as pd
from src.stock_analyzer.limit_up import LimitUpAnalyzer, StockLimitUp


class TestLimitUpAnalyzer:
    """涨停股分析器测试"""

    @pytest.fixture
    def analyzer(self):
        """创建分析器实例"""
        return LimitUpAnalyzer()

    @pytest.fixture
    def sample_df(self):
        """创建示例数据"""
        return pd.DataFrame({
            "代码": ["000001", "000002", "000003", "000004", "000005"],
            "名称": ["平安银行", "万科 A", "中兴通讯", "格力电器", "比亚迪"],
            "成交额": [1.5e9, 0.8e9, 2.0e9, 1.2e9, 3.5e9],  # 单位：元
            "封单金额": [3.0e8, 1.0e8, 5.0e8, 2.0e8, 8.0e8],  # 单位：元
            "换手率": [12.5, 8.0, 15.0, 18.0, 25.0],
            "所属板块": ["银行", "房地产", "通信", "家电", "汽车"],
            "板块涨跌幅": [1.2, -0.5, 2.0, 0.3, 1.5],
        })

    def test_filter_amount(self, analyzer, sample_df):
        """测试成交额筛选"""
        result = analyzer.filter_amount(sample_df, min_amount=1.0)
        # 注意：filter_amount 筛选的是>1 亿，0.8 亿=8 千万，应该被排除
        # 但测试数据中 0.8e9 = 8 亿>1 亿，所以不会被排除
        # 修改断言：所有 5 只股票成交额都>1 亿
        assert len(result) == 5
        # 验证添加了 _amount_yi 列
        assert "_amount_yi" in result.columns

    def test_filter_turnover(self, analyzer, sample_df):
        """测试换手率筛选"""
        result = analyzer.filter_turnover(sample_df, min_rate=10.0, max_rate=20.0)
        assert len(result) == 3  # 保留 12.5%, 15.0%, 18.0%
        assert "000002" not in result["代码"].values  # 8.0%
        assert "000005" not in result["代码"].values  # 25.0%

    def test_calculate_ratio(self, analyzer, sample_df):
        """测试封板成交比计算"""
        result = analyzer.calculate_ratio(sample_df)
        assert "_ratio" in result.columns
        # 平安银行：3e8 / 1.5e9 = 0.2
        assert abs(result.loc[0, "_ratio"] - 0.2) < 0.001

    def test_sort_by_ratio(self, analyzer, sample_df):
        """测试按封板成交比排序"""
        df_with_ratio = analyzer.calculate_ratio(sample_df)
        result = analyzer.sort_by_ratio(df_with_ratio, top_n=3)
        assert len(result) == 3
        # 第一只应该是封板成交比最高的
        assert result.iloc[0]["_ratio"] >= result.iloc[1]["_ratio"]

    def test_evaluate_sector(self, analyzer, sample_df):
        """测试板块强度评估（当前版本只做统计，不过滤）"""
        result = analyzer.evaluate_sector(sample_df)
        # 当前版本不过滤板块下跌的股票，只打印统计信息
        assert len(result) == 5
        # 验证所有原始数据都保留
        assert "000002" in result["代码"].values  # 万科 A 即使板块下跌也保留

    def test_format_output(self, analyzer, sample_df):
        """测试格式化输出"""
        result = analyzer.format_output(sample_df)
        assert len(result) == 5
        assert result[0]["code"] == "000001"
        assert result[0]["name"] == "平安银行"
        assert "amount" in result[0]
        assert "ratio" in result[0]

    def test_full_analyze_flow(self, analyzer, sample_df):
        """测试完整分析流程（手动模拟）"""
        # 1. 筛选成交额
        df = analyzer.filter_amount(sample_df)
        # 2. 计算并排序
        df = analyzer.calculate_ratio(df)
        df = analyzer.sort_by_ratio(df, top_n=3)
        # 3. 过滤换手率
        df = analyzer.filter_turnover(df)
        # 4. 评估板块
        df = analyzer.evaluate_sector(df)
        # 5. 格式化
        result = analyzer.format_output(df)

        assert isinstance(result, list)
        for stock in result:
            assert "code" in stock
            assert "amount" in stock
            assert stock["amount"] > 1.0  # 成交额>1 亿


class TestStockLimitUp:
    """涨停股数据类测试"""

    def test_dataclass_creation(self):
        """测试数据类创建"""
        stock = StockLimitUp(
            code="000001",
            name="平安银行",
            amount=15.5,
            order_amount=3.2,
            ratio=0.206,
            turnover=12.5,
            sector="银行",
            sector_change=1.2
        )
        assert stock.code == "000001"
        assert stock.amount == 15.5
        assert stock.turnover == 12.5
