# -*- coding: utf-8 -*-
"""
pp check - 论文格式检查
"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from paper_pilot.checker.format_checker import FormatChecker

console = Console()


@click.command(name="check", help="检查论文格式")
@click.option("--path", "-p", "target_path", default=".", type=click.Path(), help="检查路径")
@click.option("--strict", "-s", is_flag=True, default=False, help="严格模式（警告也视为错误）")
def check(target_path: str, strict: bool) -> None:
    """检查论文格式是否符合规范"""
    target = Path(target_path).resolve()
    checker = FormatChecker(target)
    results = checker.run_all_checks()

    # 构建结果表格
    table = Table(title="📋 论文格式检查报告", show_lines=True)
    table.add_column("级别", style="bold", width=6)
    table.add_column("文件", width=25)
    table.add_column("行号", width=6, justify="right")
    table.add_column("问题描述", width=50)

    errors = 0
    warnings = 0

    for r in results:
        style = "red" if r["level"] == "error" else "yellow"
        table.add_row(
            f"[{style}]{r['level'].upper()}[/{style}]",
            r["file"],
            str(r.get("line", "-")),
            r["message"],
        )
        if r["level"] == "error":
            errors += 1
        else:
            warnings += 1

    if results:
        console.print(table)
    else:
        console.print("[bold green]✅ 所有检查通过，未发现问题！[/bold green]")

    # 统计摘要
    console.print()
    summary_parts = []
    if errors:
        summary_parts.append(f"[red]❌ 错误: {errors}[/red]")
    if warnings:
        summary_parts.append(f"[yellow]⚠️  警告: {warnings}[/yellow]")
    if not errors and not warnings:
        summary_parts.append("[green]✅ 全部通过[/green]")

    console.print(" | ".join(summary_parts))

    if strict:
        raise SystemExit(1 if (errors + warnings) > 0 else 0)
    else:
        raise SystemExit(1 if errors > 0 else 0)
