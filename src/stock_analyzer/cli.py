"""
涨停股分析命令行入口

用法:
    python -m src.stock_analyzer.cli [日期]

示例:
    python -m src.stock_analyzer.cli          # 分析最新交易日
    python -m src.stock_analyzer.cli 20260402  # 分析指定日期
"""

import sys
import json
from datetime import datetime
from src.stock_analyzer.limit_up import LimitUpAnalyzer


def main():
    """主函数"""
    # 解析日期参数
    date = None
    if len(sys.argv) > 1:
        date = sys.argv[1]
        # 验证日期格式
        try:
            datetime.strptime(date, "%Y%m%d")
        except ValueError:
            print(f"错误：日期格式应为 YYYYMMDD，例如：20260402")
            sys.exit(1)

    print(f"开始分析涨停股{'(' + date + ')' if date else '(最新交易日)'}...")
    print("-" * 50)

    try:
        analyzer = LimitUpAnalyzer()
        result = analyzer.analyze(date)

        print("\n" + "=" * 50)
        print("分析结果:")
        print("=" * 50)

        if not result:
            print("未找到符合条件的股票")
        else:
            # 格式化输出
            output = json.dumps(result, ensure_ascii=False, indent=2)
            print(output)

            # 打印摘要
            print("\n" + "-" * 50)
            print(f"共筛选出 {len(result)} 只符合条件的股票")
            if result:
                avg_ratio = sum(s.get("ratio", 0) for s in result) / len(result)
                avg_turnover = sum(s.get("turnover", 0) for s in result) / len(result)
                print(f"平均封板成交比：{avg_ratio:.3f}")
                print(f"平均换手率：{avg_turnover:.1f}%")

        return result

    except Exception as e:
        print(f"分析失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
