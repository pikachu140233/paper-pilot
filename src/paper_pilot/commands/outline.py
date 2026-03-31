# -*- coding: utf-8 -*-
"""
pp outline — 论文大纲提取命令

从 LaTeX 源码中解析章节标题，生成可视化的目录树结构。
方便快速了解论文整体框架和章节安排。

使用方法：
    pp outline                # 提取当前目录大纲
    pp outline --path ./thesis  # 提取指定目录大纲
"""

import re
from pathlib import Path

import click
from rich.console import Console
from rich.tree import Tree

console = Console()

# 章节层级与对应 LaTeX 命令的映射
HEADING_PATTERNS: list[tuple[str, re.Pattern, int]] = [
    ("chapter", re.compile(r'\\chapter\{([^}]*)\}'), 0),
    ("section", re.compile(r'\\section\{([^}]*)\}'), 1),
    ("subsection", re.compile(r'\\subsection\{([^}]*)\}'), 2),
    ("subsubsection", re.compile(r'\\subsubsection\{([^}]*)\}'), 3),
]

# 树节点样式
STYLES = {
    0: "bold magenta",      # chapter
    1: "bold cyan",         # section
    2: "green",             # subsection
    3: "dim",               # subsubsection
}


@click.command(name="outline", help="🌳 提取并展示论文大纲（章节目录树）")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="论文目录路径，默认为当前目录",
)
def outline(path: Path | None) -> None:
    """
    从 .tex 文件中提取章节结构并展示为目录树。
    """
    target = path or Path.cwd()

    # 查找所有 .tex 文件，按文件名排序确保章节顺序一致
    tex_files = sorted(target.rglob("*.tex"))
    tex_files = [f for f in tex_files if f.is_file()]

    if not tex_files:
        console.print(
            f"[yellow]未在 {target} 下找到任何 .tex 文件。[/yellow]\n"
            "提示：请在论文根目录下运行此命令，或使用 --path 指定目录。"
        )
        return

    # 解析所有文件的章节标题
    # 每项: (level, title, source_file)
    headings: list[tuple[int, str, str]] = []

    for f in tex_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as exc:
            console.print(f"[red]读取文件失败: {f} ({exc})[/red]")
            continue

        for line in content.splitlines():
            line = line.strip()
            for name, pattern, level in HEADING_PATTERNS:
                m = pattern.search(line)
                if m:
                    title = m.group(1).strip()
                    # 清理标题中的 LaTeX 命令残留
                    title = _clean_title(title)
                    rel = f.relative_to(target)
                    headings.append((level, title, str(rel)))
                    break  # 每行只匹配一个层级

    if not headings:
        console.print(
            "[yellow]未在任何 .tex 文件中找到章节命令（\\chapter / \\section 等）。[/yellow]"
        )
        return

    # 构建树
    tree = Tree(f"📖 [bold]{target.name}[/bold] 论文大纲")

    # 用栈维护当前各层级的父节点
    # stack[i] = 第 i 层最新的 Tree 节点
    stack: dict[int, Tree] = {}

    for level, title, source in headings:
        style = STYLES.get(level, "white")

        # 找到合适的父节点：栈中比当前层级小的最大层级
        parent = tree
        for l in range(level - 1, -1, -1):
            if l in stack:
                parent = stack[l]
                break

        node_label = f"[{style}]{title}[/{style}]"
        if len(tex_files) > 1:
            node_label += f"  [dim]({source})[/dim]"

        node = parent.add(node_label)
        stack[level] = node

        # 清除当前层级以下的所有子层级节点
        # （因为新节点会开启新的子树）
        for l in list(stack.keys()):
            if l > level:
                del stack[l]

    console.print(tree)
    console.print()
    console.print(
        f"[dim]共 {len(headings)} 个章节，来自 {len(tex_files)} 个 .tex 文件[/dim]"
    )


def _clean_title(title: str) -> str:
    """
    清理章节标题中的 LaTeX 命令残留。

    例如将 "基于\\textbf{深度学习}的方法" 清理为 "基于深度学习的方法"。

    Args:
        title: 原始标题字符串

    Returns:
        清理后的标题
    """
    # 移除 \command{...} 形式，保留花括号内的内容
    prev = None
    while prev != title:
        prev = title
        title = re.sub(r'\\[a-zA-Z]+\{([^{}]*)\}', r'\1', title)
    # 移除残留的 \command 形式
    title = re.sub(r'\\[a-zA-Z]+', '', title)
    return title.strip()
