from datetime import datetime

from suanming.analysis import analyze
from suanming.pillars import compute_chart


def test_compute_chart_basic():
    chart = compute_chart(datetime(1995, 8, 15, 14, 30), gender="M")
    # 1995-08-15 是乙亥年、甲申月、戊寅日（60 甲子顺推验证）
    assert str(chart.year) == "乙亥"
    assert str(chart.month) == "甲申"
    assert str(chart.day) == "戊寅"
    # 14:30 → 未时；戊日未时：戊癸起壬子，未为第8 → (8+7)%10=5 → 己未
    assert str(chart.hour) == "己未"
    assert chart.day_master == "戊"


def test_analysis_outputs_keys():
    chart = compute_chart(datetime(1990, 5, 1, 8, 0), gender="F")
    a = analyze(chart)
    assert a.day_master_element in {"木", "火", "土", "金", "水"}
    assert a.strong_weak in {"旺", "中和", "弱"}
    assert sum(a.element_strength.values()) > 0


def test_late_zi_crosses_day():
    # 23:30 出生默认归入次日日柱
    chart = compute_chart(datetime(2000, 1, 1, 23, 30), gender="M")
    chart_no = compute_chart(
        datetime(2000, 1, 1, 23, 30), gender="M", late_zi_crosses_day=False
    )
    assert chart.day != chart_no.day
