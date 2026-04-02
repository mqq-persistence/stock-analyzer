"""
涨停股分析模块

提供涨停股池获取、筛选、过滤和板块强度评估功能。
"""

import pandas as pd
import akshare as ak
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class StockLimitUp:
    """涨停股数据"""
    code: str  # 股票代码
    name: str  # 股票名称
    amount: float  # 成交额（亿元）
    order_amount: float  # 封单金额（亿元）
    ratio: float  # 封板成交比
    turnover: float  # 换手率（%）
    sector: str  # 所属板块
    sector_change: float  # 板块涨跌幅（%）


class LimitUpAnalyzer:
    """涨停股分析器"""

    # 配置常量
    MIN_AMOUNT: float = 1.0  # 最小成交额（亿元）
    MIN_TURNOVER: float = 10.0  # 最小换手率（%）
    MAX_TURNOVER: float = 20.0  # 最大换手率（%）
    TOP_N: int = 25  # 返回前 N 只股票

    def __init__(self):
        """初始化分析器"""
        pass

    def get_limit_up_pool(self, date: str | None = None) -> pd.DataFrame:
        """
        获取指定交易日的涨停股池

        Args:
            date: 交易日期，格式 YYYYMMDD，默认为最新交易日

        Returns:
            涨停股数据 DataFrame
        """
        if date is None:
            # 获取最新交易日数据
            date = datetime.now().strftime("%Y%m%d")

        try:
            # 调用 AKShare 获取涨停股池数据（东方财富网数据源）
            df = ak.stock_zt_pool_em(date=date)
            return df
        except Exception as e:
            raise RuntimeError(f"获取涨停股池失败：{e}")

    def filter_amount(self, df: pd.DataFrame, min_amount: float | None = None) -> pd.DataFrame:
        """
        筛选成交额大于指定阈值的股票

        Args:
            df: 涨停股数据
            min_amount: 最小成交额（亿元），默认为 MIN_AMOUNT

        Returns:
            筛选后的 DataFrame
        """
        threshold = min_amount if min_amount is not None else self.MIN_AMOUNT
        # 成交额列名可能是"成交额"或"amount"，需要适配
        amount_col = self._find_column(df, ["成交额", "amount", "成交金额"])
        if amount_col is None:
            raise ValueError("未找到成交额列")

        # 转换为亿元单位（如果原始数据是元）
        df_filtered = df.copy()
        if df_filtered[amount_col].max() > 1e8:  # 如果最大值大于 1 亿，说明单位是元
            df_filtered["_amount_yi"] = df_filtered[amount_col] / 1e8
        else:
            df_filtered["_amount_yi"] = df_filtered[amount_col]

        return df_filtered[df_filtered["_amount_yi"] > threshold]

    def filter_turnover(self, df: pd.DataFrame, min_rate: float | None = None,
                        max_rate: float | None = None) -> pd.DataFrame:
        """
        筛选换手率在指定范围内的股票

        Args:
            df: 涨停股数据
            min_rate: 最小换手率（%），默认为 MIN_TURNOVER
            max_rate: 最大换手率（%），默认为 MAX_TURNOVER

        Returns:
            筛选后的 DataFrame
        """
        min_turnover = min_rate if min_rate is not None else self.MIN_TURNOVER
        max_turnover = max_rate if max_rate is not None else self.MAX_TURNOVER

        turnover_col = self._find_column(df, ["换手率", "turnover", "换手"])
        if turnover_col is None:
            raise ValueError("未找到换手率列")

        mask = (df[turnover_col] >= min_turnover) & (df[turnover_col] <= max_turnover)
        return df[mask]

    def calculate_ratio(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算封板成交比

        Args:
            df: 涨停股数据

        Returns:
            添加了封板成交比列的 DataFrame
        """
        # 封单金额列
        order_col = self._find_column(df, ["封成比", "封单金额", "买一成交额", "order_amount"])
        # 成交额列
        amount_col = self._find_column(df, ["成交额", "amount", "成交金额"])

        if order_col is None or amount_col is None:
            raise ValueError("未找到封单金额或成交额列")

        # 计算封板成交比 = 封单金额 / 成交额
        df_copy = df.copy()

        # 统一单位为亿元
        if df_copy[amount_col].max() > 1e8:
            amount = df_copy[amount_col] / 1e8
        else:
            amount = df_copy[amount_col]

        if df_copy[order_col].max() > 1e8:
            order = df_copy[order_col] / 1e8
        else:
            order = df_copy[order_col]

        # 避免除以零
        df_copy["_ratio"] = order / amount.replace(0, 0.001)
        return df_copy

    def sort_by_ratio(self, df: pd.DataFrame, top_n: int | None = None) -> pd.DataFrame:
        """
        按封板成交比排序，取前 N 只股票

        Args:
            df: 涨停股数据
            top_n: 返回前 N 只，默认为 TOP_N

        Returns:
            排序后的 DataFrame
        """
        n = top_n if top_n is not None else self.TOP_N
        ratio_col = self._find_column(df, ["_ratio", "ratio", "封板成交比", "封成比"])

        if ratio_col is None:
            df = self.calculate_ratio(df)
            ratio_col = "_ratio"

        return df.sort_values(by=ratio_col, ascending=False).head(n)

    def evaluate_sector(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        评估板块强度，剔除板块下跌或活跃度低的股票

        Args:
            df: 涨停股数据

        Returns:
            筛选后的 DataFrame
        """
        # 注：AKShare 返回数据中没有直接的板块涨跌幅列
        # 所属行业列用于后续分析，此处暂不做板块涨跌幅筛选
        sector_col = self._find_column(df, ["所属行业", "sector"])

        if sector_col:
            print(f"板块分布：{df[sector_col].nunique()} 个行业")

        return df

    def format_output(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        格式化输出为 JSON 友好的字典列表

        Args:
            df: 涨停股数据

        Returns:
            字典列表
        """
        result = []

        for _, row in df.iterrows():
            # 获取成交额（转换为亿元）
            amount_col = self._find_column(pd.DataFrame([row]), ["成交额", "amount"])
            amount = row[amount_col] if amount_col else None
            if amount and amount > 1e8:
                amount = amount / 1e8

            # 获取封板资金/封单金额（转换为亿元）
            order_col = self._find_column(pd.DataFrame([row]), ["封板资金", "封单金额", "order_amount"])
            order_amount = row[order_col] if order_col else None
            # 判断单位：如果大于 1 亿，说明单位是元，转换为亿元
            if order_amount and order_amount > 1e8:
                order_amount = order_amount / 1e8
            # 如果小于 1，可能是亿元单位
            elif order_amount and order_amount < 1:
                order_amount = order_amount  # 保持原值（亿元）
            # 否则假设是元单位
            elif order_amount:
                order_amount = order_amount / 1e8

            # 获取封板成交比
            ratio = self._get_numeric_value(row, ["_ratio", "ratio", "封板成交比"])
            # 如果没有预计算的 ratio，现场计算
            if ratio is None and amount and order_amount:
                ratio = order_amount / amount if amount > 0 else 0

            stock = {
                "code": self._get_value(row, ["代码", "code", "股票代码"]),
                "name": self._get_value(row, ["名称", "name", "股票名称"]),
                "amount": round(amount, 2) if amount else None,
                "order_amount": round(order_amount, 2) if order_amount else None,
                "ratio": round(ratio, 3) if ratio else None,
                "turnover": round(self._get_numeric_value(row, ["换手率", "turnover"]), 2),
                "sector": self._get_value(row, ["所属行业", "sector", "所属板块"]),
            }
            result.append(stock)

        return result

    def analyze(self, date: str | None = None) -> List[Dict[str, Any]]:
        """
        完整分析流程：获取涨停股池 -> 筛选 -> 过滤 -> 评估 -> 输出

        Args:
            date: 交易日期，格式 YYYYMMDD

        Returns:
            分析结果列表
        """
        # 1. 获取涨停股池
        df = self.get_limit_up_pool(date)
        print(f"初始涨停股池：{len(df)} 只")

        # 2. 筛选成交额 > 1 亿
        df = self.filter_amount(df)
        print(f"成交额>1 亿：{len(df)} 只")

        # 3. 计算封板成交比并取前 25
        df = self.sort_by_ratio(df)
        print(f"封板成交比前 25: {len(df)} 只")

        # 4. 过滤换手率 10%-20%
        df = self.filter_turnover(df)
        print(f"换手率 10%-20%: {len(df)} 只")

        # 5. 评估板块强度
        df = self.evaluate_sector(df)
        print(f"板块强度评估后：{len(df)} 只")

        # 6. 格式化输出
        result = self.format_output(df)
        print(f"最终结果：{len(result)} 只股票")

        return result

    def _find_column(self, df: pd.DataFrame, candidates: List[str]) -> str | None:
        """查找匹配的列名"""
        for col in df.columns:
            if col in candidates:
                return col
        # 模糊匹配
        for candidate in candidates:
            for col in df.columns:
                if candidate in col or col in candidate:
                    return col
        return None

    def _get_value(self, row: pd.Series, candidates: List[str]) -> Any:
        """获取行的值"""
        col = self._find_column(pd.DataFrame([row]), candidates)
        return row[col] if col else None

    def _get_numeric_value(self, row: pd.Series, candidates: List[str]) -> float | None:
        """获取数值类型的值"""
        col = self._find_column(pd.DataFrame([row]), candidates)
        if col is None:
            return None
        value = row[col]
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
