"""四柱排盘：年、月、日、时干支。

依赖 sxtwl（寿星天文历）处理立春换年、节令换月、农历转换。
时柱使用「五鼠遁日起时」公式由日干推出。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

import sxtwl

from .elements import BRANCHES, STEMS

Gender = Literal["M", "F"]


@dataclass(frozen=True)
class Pillar:
    """单柱：天干 + 地支。"""

    stem: str
    branch: str

    def __str__(self) -> str:
        return f"{self.stem}{self.branch}"


@dataclass
class BaziChart:
    """完整命盘。"""

    solar_datetime: datetime
    gender: Gender
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    lunar: dict = field(default_factory=dict)

    @property
    def day_master(self) -> str:
        """日主 = 日柱天干。"""
        return self.day.stem

    @property
    def pillars(self) -> tuple[Pillar, Pillar, Pillar, Pillar]:
        return (self.year, self.month, self.day, self.hour)

    def to_dict(self) -> dict:
        return {
            "solar": self.solar_datetime.isoformat(),
            "gender": self.gender,
            "year": str(self.year),
            "month": str(self.month),
            "day": str(self.day),
            "hour": str(self.hour),
            "day_master": self.day_master,
            "lunar": self.lunar,
        }


# 时支：23-1 子, 1-3 丑, 3-5 寅 ...
def _hour_branch(hour: int) -> str:
    # 子时跨夜：23-0:59 与 0-0:59 一并算 0 索引
    idx = ((hour + 1) // 2) % 12
    return BRANCHES[idx]


# 五鼠遁日起时：日干→子时天干索引
# 甲己→甲(0), 乙庚→丙(2), 丙辛→戊(4), 丁壬→庚(6), 戊癸→壬(8)
_DAY_TO_ZI_STEM_IDX = {
    "甲": 0, "己": 0,
    "乙": 2, "庚": 2,
    "丙": 4, "辛": 4,
    "丁": 6, "壬": 6,
    "戊": 8, "癸": 8,
}


def _hour_stem(day_stem: str, hour: int) -> str:
    """五鼠遁：由日干与小时数推时干。"""
    zi_idx = _DAY_TO_ZI_STEM_IDX[day_stem]
    branch_idx = ((hour + 1) // 2) % 12  # 子=0, 丑=1 ...
    return STEMS[(zi_idx + branch_idx) % 10]


def compute_chart(
    solar_dt: datetime,
    gender: Gender,
    *,
    late_zi_crosses_day: bool = True,
) -> BaziChart:
    """从公历出生时间计算四柱命盘。

    Args:
        solar_dt: 公历出生时间（本地时间，已是真太阳时则更精确）。
        gender: ``"M"`` 男 / ``"F"`` 女。
        late_zi_crosses_day: 23:00–23:59 的「晚子时」是否归入次日日柱。默认 True。
    """
    if gender not in ("M", "F"):
        raise ValueError("gender must be 'M' or 'F'")

    y, m, d, hh = solar_dt.year, solar_dt.month, solar_dt.day, solar_dt.hour

    # 晚子时换日：日柱用次日干支，但年/月柱仍按当下时间界定
    day_for_pillar = solar_dt
    if late_zi_crosses_day and hh == 23:
        from datetime import timedelta
        day_for_pillar = solar_dt + timedelta(days=1)

    yd, md, dd = day_for_pillar.year, day_for_pillar.month, day_for_pillar.day

    # sxtwl: 用当下时刻取年/月柱（节气分界由库内部处理）
    cur = sxtwl.fromSolar(y, m, d)
    year_gz = cur.getYearGZ()    # 立春换年
    month_gz = cur.getMonthGZ()  # 节令换月

    # 日柱用（可能换日后的）日期
    day_obj = sxtwl.fromSolar(yd, md, dd)
    day_gz = day_obj.getDayGZ()

    year = Pillar(STEMS[year_gz.tg], BRANCHES[year_gz.dz])
    month = Pillar(STEMS[month_gz.tg], BRANCHES[month_gz.dz])
    day = Pillar(STEMS[day_gz.tg], BRANCHES[day_gz.dz])

    hour_branch = _hour_branch(hh)
    hour_stem = _hour_stem(day.stem, hh)
    hour = Pillar(hour_stem, hour_branch)

    lunar = {
        "lunar_year": cur.getLunarYear(),
        "lunar_month": cur.getLunarMonth(),
        "lunar_day": cur.getLunarDay(),
        "is_leap_month": bool(cur.isLunarLeap()),
    }

    return BaziChart(
        solar_datetime=solar_dt,
        gender=gender,
        year=year,
        month=month,
        day=day,
        hour=hour,
        lunar=lunar,
    )
