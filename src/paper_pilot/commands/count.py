# -*- coding: utf-8 -*-
"""
pp count — 论文字数统计命令

统计 LaTeX 论文中英文字符数，适用于中文研究生论文字数要求检查。
例如硕士学位论文通常要求 30000+ 中文字符。

使用方法：
    pp count                # 统计当前目录
    pp count --path ./thesis  # 统计指定目录
"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from paper_pilot.utils.counter import (
    count_chinese,
    count_english,
    find_tex_files,
    strip_latex,
)

console = Console()


@click.command(name="count", help="📊 统计论文字数（中文字符 + 英文单词）")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="要统计的目录路径，默认为当前目录",
)
def count(path: Path | None) -> None:
    """
    统计指定目录中所有 .tex 文件的字数。

    分别统计中文字符数和英文单词数，并显示按文件分布的明细表。
    """
    target = path or Path.cwd()

    # 查找所有 .tex 文件
    tex_files = find_tex_files(target)

    if not tex_files:
        console.print(
            f"[yellow]未在 {target} 下找到任何 .tex 文件。[/yellow]\n"
            "提示：请在论文根目录下运行此命令，或使用 --path 指定目录。"
        )
        return

    # 逐文件统计
    table = Table(
        title=f"📝 论文字数统计 — {target}",
        show_header=True,
        header_style="bold cyan",
        show_lines=False,
    )
    table.add_column("文件", style="white", no_wrap=False)
    table.add_column("中文字符", justify="right", style="green")
    table.add_column("英文单词", justify="right", style="blue")
    table.add_column("总字数*", justify="right", style="bold magenta")

    total_cn = 0
    total_en = 0

    for f in tex_files:
        try:
            raw = f.read_text(encoding="utf-8")
        except Exception as exc:
            console.print(f"[red]读取文件失败: {f} ({exc})[/red]")
            continue

        clean = strip_latex(raw)
        cn = count_chinese(clean)
        en = count_english(clean)
        total_cn += cn
        total_en += en

        # 显示相对于搜索根目录的路径，更简洁
        rel = f.relative_to(target)
        table.add_row(str(rel), f"{cn:,}", f"{en:,}", f"{cn + en:,}")

    # 添加汇总行
    table.add_section()
    table.add_row(
        "[bold]合计[/bold]",
        f"[bold green]{total_cn:,}[/bold green]",
        f"[bold blue]{total_en:,}[/bold blue]",
        f"[bold magenta]{total_cn + total_en:,}[/bold magenta]",
    )

    console.print(table)

    # 字数要求提示
    console.print()
    console.print(
        "[dim]* 总字数 = 中文字符数 + 英文单词数（中文研究生论文通常只计中文字符）[/dim]"
    )

    # 常见字数要求参考
    typical_thresholds = [
        (10000, "本科毕业论文（部分学校）"),
        (20000, "本科毕业论文（多数学校）"),
        (30000, "硕士学位论文"),
        (50000, "博士学位论文（部分）"),
        (80000, "博士学位论文（多数）"),
    ]

    for threshold, label in typical_thresholds:
        if total_cn < threshold:
            remaining = threshold - total_cn
            console.print(
                f"  [yellow]⚠ 还差约 [bold]{remaining:,}[/bold] 个中文字符可达 {label} 要求 ({threshold:,})[/yellow]"
            )
            break
    else:
        console.print(
            f"  [green]✅ 中文字符数 ({total_cn:,}) 已达到博士学位论文一般要求！[/green]"
        )

    console.print()
    console.print(
        f"[dim]共扫描 {len(tex_files)} 个 .tex 文件[/dim]"
    )
