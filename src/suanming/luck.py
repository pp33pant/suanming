"""大运 / 流年推算。

规则（简化版）：
    - 阳男阴女顺排，阴男阳女逆排
    - 起运 = 出生到下一节气（顺）/ 上一节气（逆）的天数 / 3，得起运岁数（按 3 天 = 1 年）
    - 大运从月柱顺/逆排干支，每柱 10 年
    - 流年取当年年柱干支
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import sxtwl

from .elements import BRANCHES, STEMS, stem_polarity
from .pillars import BaziChart, Pillar


@dataclass
class LuckPillar:
    pillar: Pillar
    start_age: float
    start_year: int

    def to_dict(self) -> dict:
        return {
            "pillar": str(self.pillar),
            "start_age": round(self.start_age, 2),
            "start_year": self.start_year,
        }


def _next_or_prev_jieqi_seconds(solar_dt: datetime, *, forward: bool) -> float:
    """返回到最近一个 *节*（非中气）的秒数。简化：扫描 ±60 天。"""
    # sxtwl 的节气接口在不同版本差异较大，这里用每日扫描 + 节气标志判断
    from datetime import timedelta

    sign = 1 if forward else -1
    for delta in range(1, 75):
        d = solar_dt + sign * timedelta(days=delta)
        day = sxtwl.fromSolar(d.year, d.month, d.day)
        # hasJieQi(): 当日是否含节气；getJieQi(): 节气索引(0..23)
        # 节（非中气）索引为偶数：0 立春,2 惊蛰,4 清明,6 立夏,8 芒种,10 小暑,12 立秋,14 白露,16 寒露,18 立冬,20 大雪,22 小寒
        if day.hasJieQi() and day.getJieQi() % 2 == 0:
            # sxtwl 提供 getJieQiJD() 取节气精确儒略日
            jd = day.getJieQiJD()
            jq_dt = _jd_to_datetime(jd)
            return abs((jq_dt - solar_dt).total_seconds())
    raise RuntimeError("未在 75 天内找到节气，数据异常")


def _jd_to_datetime(jd: float) -> datetime:
    """儒略日 → UTC datetime（再 +8h 视为北京时间）。"""
    from datetime import timedelta
    # 标准儒略日转换
    jd0 = jd + 0.5
    z = int(jd0)
    f = jd0 - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    day_int = int(day)
    frac = day - day_int
    secs = int(frac * 86400)
    base = datetime(year, month, day_int) + timedelta(seconds=secs)
    return base + timedelta(hours=8)  # 转北京时间


def compute_luck(chart: BaziChart, count: int = 8) -> list[LuckPillar]:
    """生成前 N 步大运。"""
    yang_male = chart.gender == "M" and stem_polarity(chart.year.stem) == "阳"
    yin_female = chart.gender == "F" and stem_polarity(chart.year.stem) == "阴"
    forward = yang_male or yin_female

    secs = _next_or_prev_jieqi_seconds(chart.solar_datetime, forward=forward)
    days = secs / 86400.0
    start_age = days / 3.0  # 3 日 = 1 年

    # 月柱在 60 甲子中的位置
    s_idx = STEMS.index(chart.month.stem)
    b_idx = BRANCHES.index(chart.month.branch)

    luck: list[LuckPillar] = []
    for i in range(1, count + 1):
        step = i if forward else -i
        ns = (s_idx + step) % 10
        nb = (b_idx + step) % 12
        age = start_age + (i - 1) * 10
        year = chart.solar_datetime.year + int(age)
        luck.append(
            LuckPillar(
                pillar=Pillar(STEMS[ns], BRANCHES[nb]),
                start_age=age,
                start_year=year,
            )
        )
    return luck


def year_pillar(year: int) -> Pillar:
    """取某公历年的年柱（以立春为界，使用该年 3 月 1 日采样规避立春前后干扰；
    若需立春前精确判定，请用 ``compute_chart`` 传入具体日期）。"""
    day = sxtwl.fromSolar(year, 3, 1)
    gz = day.getYearGZ()
    return Pillar(STEMS[gz.tg], BRANCHES[gz.dz])
