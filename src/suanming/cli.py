"""Typer CLI 入口。"""

from __future__ import annotations

from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from .analysis import analyze
from .luck import compute_luck
from .pillars import compute_chart

app = typer.Typer(add_completion=False, help="算命 · Suanming：八字排盘与命理分析")
console = Console()


def _parse_dt(date: str, time: str) -> datetime:
    return datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")


def _print_chart(chart, analysis) -> None:
    t = Table(title="四柱命盘", show_header=True, header_style="bold magenta")
    for col in ("年柱", "月柱", "日柱", "时柱"):
        t.add_column(col)
    t.add_row(str(chart.year), str(chart.month), str(chart.day), str(chart.hour))
    console.print(t)
    console.print(f"[bold]日主[/bold]：{analysis.day_master}（{analysis.day_master_element}）  "
                  f"[bold]旺衰[/bold]：{analysis.strong_weak}")
    console.print(f"[bold]五行强弱[/bold]：{analysis.element_strength}")
    console.print(f"[bold]十神分布[/bold]：{analysis.ten_god_distribution}")


@app.command()
def bazi(
    date: str = typer.Option(..., help="公历出生日期 YYYY-MM-DD"),
    time: str = typer.Option("12:00", help="出生时间 HH:MM (24h)"),
    gender: str = typer.Option("M", help="性别 M/F"),
):
    """排盘并打印四柱、五行、十神。"""
    dt = _parse_dt(date, time)
    chart = compute_chart(dt, gender=gender)  # type: ignore[arg-type]
    analysis = analyze(chart)
    _print_chart(chart, analysis)


@app.command()
def luck(
    date: str = typer.Option(...),
    time: str = typer.Option("12:00"),
    gender: str = typer.Option("M"),
    count: int = typer.Option(8, help="输出几步大运"),
):
    """显示前 N 步大运。"""
    dt = _parse_dt(date, time)
    chart = compute_chart(dt, gender=gender)  # type: ignore[arg-type]
    analysis = analyze(chart)
    _print_chart(chart, analysis)
    luck_pillars = compute_luck(chart, count=count)
    t = Table(title="大运", header_style="bold cyan")
    for col in ("步数", "干支", "起运岁", "起运年"):
        t.add_column(col)
    for i, lp in enumerate(luck_pillars, 1):
        t.add_row(str(i), str(lp.pillar), f"{lp.start_age:.1f}", str(lp.start_year))
    console.print(t)


@app.command()
def reading(
    date: str = typer.Option(...),
    time: str = typer.Option("12:00"),
    gender: str = typer.Option("M"),
    model: str = typer.Option("gpt-4o-mini"),
):
    """生成 AI 命局白话解读（需要 OPENAI_API_KEY）。"""
    from .ai import reading as ai_reading

    dt = _parse_dt(date, time)
    chart = compute_chart(dt, gender=gender)  # type: ignore[arg-type]
    analysis = analyze(chart)
    luck_pillars = compute_luck(chart)
    _print_chart(chart, analysis)
    console.rule("AI 解读")
    console.print(ai_reading(chart, analysis, luck_pillars, model=model))


if __name__ == "__main__":
    app()
