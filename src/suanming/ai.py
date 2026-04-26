"""可选：调用 LLM 给出命局白话解读。"""

from __future__ import annotations

import os
from typing import Iterable

from .analysis import Analysis
from .luck import LuckPillar
from .pillars import BaziChart

_SYSTEM_PROMPT = (
    "你是一位中文命理顾问。给定客观的八字命盘事实（四柱、五行强弱、十神分布、大运），"
    "用温和、克制、负责任的口吻给出白话解读：性格倾向、事业财运参考方向、需注意的健康/人际议题、"
    "近年（大运/流年）建议。请避免绝对化断言，提醒读者命理仅供参考，最终决策应结合现实情况。"
    "用简体中文输出，分小标题。"
)


def _format_facts(chart: BaziChart, analysis: Analysis, luck: Iterable[LuckPillar]) -> str:
    luck_str = "\n".join(
        f"  - {lp.pillar} 起 {lp.start_age:.1f} 岁（约 {lp.start_year} 年）" for lp in luck
    )
    return (
        f"出生：{chart.solar_datetime.isoformat()} 性别：{chart.gender}\n"
        f"四柱：年 {chart.year}  月 {chart.month}  日 {chart.day}  时 {chart.hour}\n"
        f"日主：{analysis.day_master}（{analysis.day_master_element}）  旺衰：{analysis.strong_weak}\n"
        f"五行强弱：{analysis.element_strength}\n"
        f"十神分布：{analysis.ten_god_distribution}\n"
        f"大运：\n{luck_str}\n"
    )


def reading(
    chart: BaziChart,
    analysis: Analysis,
    luck: Iterable[LuckPillar],
    *,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    base_url: str | None = None,
) -> str:
    """调用 OpenAI 兼容接口给出解读。需要安装 ``openai`` 并设置 ``OPENAI_API_KEY``。"""
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("需要安装 openai：pip install 'suanming[ai]'") from e

    client = OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
        base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
    )
    facts = _format_facts(chart, analysis, luck)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": facts},
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content or ""
