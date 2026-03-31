# -*- coding: utf-8 -*-
"""
Paper Pilot CLI 主入口
使用 Click 库实现命令行界面
"""

import click
from rich.console import Console

from paper_pilot.commands.init import init
from paper_pilot.commands.check import check
from paper_pilot.commands.refs import refs

console = Console()


@click.group(
    name="pp",
    help="🎓 Paper Pilot - 中国研究生论文写作助手\n\n"
         "帮助研究生快速创建、检查和管理 LaTeX 论文项目。\n\n"
         "常用命令:\n"
         "  pp init . --title \"我的论文\" --author \"张三\"\n"
         "  pp check\n"
         "  pp refs --stats",
    invoke_without_command=True,
)
@click.version_option(
    version="0.1.0",
    prog_name="paper-pilot",
    message="%(prog)s 版本 %(version)s - 中国研究生论文写作助手"
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Paper Pilot 主命令组"""
    if ctx.invoked_subcommand is None:
        # 没有子命令时显示帮助信息
        click.echo(ctx.get_help())


# 注册子命令
cli.add_command(init)
cli.add_command(check)
cli.add_command(refs)


def main() -> None:
    """CLI 主入口函数"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]操作已取消[/yellow]")
        raise SystemExit(130)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()