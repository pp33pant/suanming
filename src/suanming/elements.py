"""天干地支 · 五行 · 藏干 · 十神 基础数据与映射。"""

from __future__ import annotations

from typing import Literal

# 天干
STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

Element = Literal["木", "火", "土", "金", "水"]
Polarity = Literal["阳", "阴"]

# 天干 → 五行
_STEM_ELEMENT: dict[str, Element] = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 天干阴阳：甲丙戊庚壬阳，乙丁己辛癸阴
_STEM_POLARITY: dict[str, Polarity] = {
    s: ("阳" if i % 2 == 0 else "阴") for i, s in enumerate(STEMS)
}

# 地支 → 五行
_BRANCH_ELEMENT: dict[str, Element] = {
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "亥": "水", "子": "水",
    "辰": "土", "戌": "土", "丑": "土", "未": "土",
}

# 地支阴阳：子寅辰午申戌阳，丑卯巳未酉亥阴
_BRANCH_POLARITY: dict[str, Polarity] = {
    b: ("阳" if i % 2 == 0 else "阴") for i, b in enumerate(BRANCHES)
}

# 地支藏干（本气在前）
HIDDEN_STEMS: dict[str, list[str]] = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 五行相生：木→火→土→金→水→木
_GENERATES: dict[Element, Element] = {
    "木": "火", "火": "土", "土": "金", "金": "水", "水": "木",
}
# 五行相克：木→土→水→火→金→木
_OVERCOMES: dict[Element, Element] = {
    "木": "土", "土": "水", "水": "火", "火": "金", "金": "木",
}

TEN_GODS = (
    "比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印",
)


def stem_element(stem: str) -> Element:
    """返回天干对应五行。"""
    return _STEM_ELEMENT[stem]


def branch_element(branch: str) -> Element:
    """返回地支对应五行。"""
    return _BRANCH_ELEMENT[branch]


def stem_polarity(stem: str) -> Polarity:
    return _STEM_POLARITY[stem]


def branch_polarity(branch: str) -> Polarity:
    return _BRANCH_POLARITY[branch]


def ten_god(day_master: str, other: str) -> str:
    """根据日主天干，判定另一天干与日主的十神关系。

    规则：
        同五行同性 → 比肩；同五行异性 → 劫财
        我生（日主→他）同性 → 食神；异性 → 伤官
        我克同性 → 偏财；异性 → 正财
        克我同性 → 七杀；异性 → 正官
        生我同性 → 偏印；异性 → 正印
    """
    me_e = stem_element(day_master)
    me_p = stem_polarity(day_master)
    o_e = stem_element(other)
    o_p = stem_polarity(other)
    same_polarity = me_p == o_p

    if o_e == me_e:
        return "比肩" if same_polarity else "劫财"
    if _GENERATES[me_e] == o_e:
        return "食神" if same_polarity else "伤官"
    if _OVERCOMES[me_e] == o_e:
        return "偏财" if same_polarity else "正财"
    if _OVERCOMES[o_e] == me_e:
        return "七杀" if same_polarity else "正官"
    if _GENERATES[o_e] == me_e:
        return "偏印" if same_polarity else "正印"
    raise ValueError(f"无法判定十神：{day_master} vs {other}")


def generates(a: Element, b: Element) -> bool:
    """a 是否生 b。"""
    return _GENERATES[a] == b


def overcomes(a: Element, b: Element) -> bool:
    """a 是否克 b。"""
    return _OVERCOMES[a] == b
