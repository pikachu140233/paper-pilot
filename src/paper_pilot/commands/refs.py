# -*- coding: utf-8 -*-
"""
pp refs - 参考文献管理
"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from paper_pilot.refs.manager import RefManager

console = Console()


@click.command(name="refs", help="管理参考文献")
@click.option("--path", "-p", "target_path", default=".", type=click.Path(), help="项目路径")
@click.option("--check", "do_check", is_flag=True, default=False, help="验证参考文献完整性")
@click.option("--stats", "do_stats", is_flag=True, default=False, help="显示参考文献统计")
def refs(target_path: str, do_check: bool, do_stats: bool) -> None:
    """管理 .bib 参考文献文件"""
    target = Path(target_path).resolve()
    manager = RefManager(target)

    bib_files = manager.find_bib_files()
    if not bib_files:
        console.print("[yellow]未找到 .bib 文件[/yellow]")
        return

    for bib_file in bib_files:
        entries = manager.parse_bib(bib_file)

        if do_stats:
            _show_stats(entries, bib_file.name)

        elif do_check:
            _show_check(entries, bib_file.name)

        else:
            _show_list(entries, bib_file.name)


def _show_list(entries: list, filename: str) -> None:
    """列出所有参考文献"""
    console.print(f"\n[bold]📚 {filename}[/bold] ({len(entries)} 条文献)\n")

    table = Table(show_lines=True)
    table.add_column("类型", width=12)
    table.add_column("引用键", style="cyan", width=25)
    table.add_column("标题", width=50)
    table.add_column("年份", width=6, justify="right")

    for entry in entries:
        table.add_row(
            entry.get("type", "unknown"),
            entry.get("key", ""),
            entry.get("title", "(无标题)")[:50],
            entry.get("year", ""),
        )

    console.print(table)


def _show_check(entries: list, filename: str) -> None:
    """检查参考文献完整性"""
    console.print(f"\n[bold]🔍 检查 {filename}[/bold]\n")

    required_fields = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "title", "publisher", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "phdthesis": ["author", "title", "school", "year"],
        "mastersthesis": ["author", "title", "school", "year"],
        "misc": ["author", "title"],
    }

    issues = 0
    for entry in entries:
        entry_type = entry.get("type", "unknown")
        needed = required_fields.get(entry_type, ["author", "title", "year"])
        missing = [f for f in needed if not entry.get(f)]

        if missing:
            issues += 1
            console.print(
                f"  [yellow]⚠️[/yellow] [cyan]{entry.get('key', '?')}[/cyan] "
                f"({entry_type}) 缺少: {', '.join(missing)}"
            )

    if issues == 0:
        console.print("[bold green]✅ 所有文献字段完整[/bold green]")
    else:
        console.print(f"\n[yellow]发现 {issues} 个问题[/yellow]")


def _show_stats(entries: list, filename: str) -> None:
    """显示统计信息"""
    console.print(f"\n[bold]📊 {filename} 统计[/bold]\n")

    # 按类型统计
    type_counts: dict[str, int] = {}
    year_counts: dict[str, int] = {}

    for entry in entries:
        t = entry.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

        y = entry.get("year", "未知")
        year_counts[y] = year_counts.get(y, 0) + 1

    # 类型表格
    table = Table(title="按类型统计")
    table.add_column("类型", style="cyan")
    table.add_column("数量", justify="right")

    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        table.add_row(t, str(count))

    console.print(table)

    # 年份表格
    if year_counts:
        ytable = Table(title="按年份统计")
        ytable.add_column("年份", style="cyan")
        ytable.add_column("数量", justify="right")

        for y, count in sorted(year_counts.items()):
            ytable.add_row(y, str(count))

        console.print(ytable)

    console.print(f"\n[bold]总计: {len(entries)} 条文献[/bold]")
