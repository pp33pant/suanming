"""一次性脚本：批量从 CSV 排盘并输出 JSON。

用法：
    python scripts/calc_bazi.py input.csv > out.jsonl

CSV 列：name,date(YYYY-MM-DD),time(HH:MM),gender(M/F)
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime

from suanming.analysis import analyze
from suanming.luck import compute_luck
from suanming.pillars import compute_chart


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M")
            chart = compute_chart(dt, gender=row["gender"])  # type: ignore[arg-type]
            analysis = analyze(chart)
            luck = [lp.to_dict() for lp in compute_luck(chart)]
            print(json.dumps({
                "name": row.get("name"),
                "chart": chart.to_dict(),
                "analysis": analysis.to_dict(),
                "luck": luck,
            }, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: calc_bazi.py <csv>")
    main(sys.argv[1])
