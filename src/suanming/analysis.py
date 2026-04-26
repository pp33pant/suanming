"""命盘分析：五行强弱、十神分布、日主旺衰粗判。"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .elements import (
    HIDDEN_STEMS,
    branch_element,
    stem_element,
    ten_god,
)
from .pillars import BaziChart

# 藏干权重（本气、中气、余气）
_HIDDEN_WEIGHTS = [1.0, 0.5, 0.3]
# 天干在柱中权重 vs 地支本气权重
_STEM_WEIGHT = 1.0
_BRANCH_WEIGHT = 1.2  # 地支力量略大于天干


@dataclass
class Analysis:
    element_strength: dict[str, float]
    ten_god_distribution: dict[str, int]
    day_master: str
    day_master_element: str
    strong_weak: str  # 旺 / 中和 / 弱

    def to_dict(self) -> dict:
        return {
            "element_strength": self.element_strength,
            "ten_god_distribution": self.ten_god_distribution,
            "day_master": self.day_master,
            "day_master_element": self.day_master_element,
            "strong_weak": self.strong_weak,
        }


def analyze(chart: BaziChart) -> Analysis:
    """对命盘做基础量化分析。"""
    elem_score: Counter[str] = Counter()
    ten_god_count: Counter[str] = Counter()
    day_master = chart.day_master

    for pillar in chart.pillars:
        # 天干
        elem_score[stem_element(pillar.stem)] += _STEM_WEIGHT
        # 地支本气
        elem_score[branch_element(pillar.branch)] += _BRANCH_WEIGHT
        # 藏干带权
        for i, hs in enumerate(HIDDEN_STEMS[pillar.branch]):
            w = _HIDDEN_WEIGHTS[i] if i < len(_HIDDEN_WEIGHTS) else 0.2
            elem_score[stem_element(hs)] += w * 0.5  # 藏干折半计入

        # 十神（仅以天干计；日柱本身不算）
        if pillar is not chart.day:
            ten_god_count[ten_god(day_master, pillar.stem)] += 1

    me_e = stem_element(day_master)
    same_or_gen = elem_score[me_e]
    # 生我 + 同我 视为帮扶
    from .elements import _GENERATES  # type: ignore[attr-defined]
    gen_me = next(k for k, v in _GENERATES.items() if v == me_e)
    support = elem_score[me_e] + elem_score[gen_me]
    total = sum(elem_score.values()) or 1.0
    ratio = support / total

    if ratio > 0.55:
        strong_weak = "旺"
    elif ratio < 0.35:
        strong_weak = "弱"
    else:
        strong_weak = "中和"

    return Analysis(
        element_strength={k: round(v, 2) for k, v in elem_score.items()},
        ten_god_distribution=dict(ten_god_count),
        day_master=day_master,
        day_master_element=me_e,
        strong_weak=strong_weak,
    )
