# -*- coding: utf-8 -*-
"""
pp init - 初始化论文项目
"""

import os
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command(name="init", help="创建新的论文项目")
@click.argument("path", default=".", type=click.Path())
@click.option("--title", "-t", default="论文题目", help="论文标题")
@click.option("--author", "-a", default="作者姓名", help="作者姓名")
@click.option("--degree", "-d", type=click.Choice(["bachelor", "master", "doctor"]), default="master", help="学位类型")
def init(path: str, title: str, author: str, degree: str) -> None:
    """初始化一个新的论文项目目录"""
    target = Path(path).resolve()

    if target.exists() and any(target.iterdir()):
        console.print(f"[yellow]警告: 目录 {target} 不为空[/yellow]")
        if not click.confirm("是否继续？部分文件可能被覆盖"):
            return

    # 获取模板目录
    template_dir = Path(__file__).parent.parent / "templates" / "thesis"
    if not template_dir.exists():
        console.print(f"[red]错误: 找不到模板目录 {template_dir}[/red]")
        raise SystemExit(1)

    # 学位中文名映射
    degree_map = {
        "bachelor": "学士",
        "master": "硕士",
        "doctor": "博士",
    }

    # 复制模板文件
    shutil.copytree(template_dir, target, dirs_exist_ok=True)

    # 替换 main.tex 中的占位符
    main_tex = target / "main.tex"
    if main_tex.exists():
        content = main_tex.read_text(encoding="utf-8")
        content = content.replace("{{TITLE}}", title)
        content = content.replace("{{AUTHOR}}", author)
        content = content.replace("{{DEGREE}}", degree_map.get(degree, "硕士"))
        main_tex.write_text(content, encoding="utf-8")

    console.print(Panel(
        f"[bold green]论文项目创建成功！[/bold green]\n\n"
        f"  📁 路径: {target}\n"
        f"  📄 标题: {title}\n"
        f"  👤 作者: {author}\n"
        f"  🎓 学位: {degree_map.get(degree, '硕士')}\n\n"
        f"[cyan]下一步:[/cyan]\n"
        f"  cd {target}\n"
        f"  xelatex main.tex  # 编译论文\n"
        f"  pp check           # 检查格式",
        title="🎓 Paper Pilot",
        border_style="cyan",
    ))
