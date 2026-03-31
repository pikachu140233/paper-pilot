# -*- coding: utf-8 -*-
"""
LaTeX 文本统计工具模块

提供从中英混排 LaTeX 源码中提取纯文本、
分别统计中文字符数和英文单词数等功能。
"""

import re
from pathlib import Path


def strip_latex(text: str) -> str:
    """
    去除 LaTeX 命令和注释，提取纯文本内容。

    处理内容：
    - 移除以 % 开头的行注释
    - 移除 \\command{...} 形式的命令
    - 移除 \\command 形式的命令（后面不跟 { 的）
    - 移除花括号 { }
    - 保留中英文正文内容

    Args:
        text: 原始 LaTeX 文本

    Returns:
        清理后的纯文本
    """
    # 移除行注释（% 到行尾），但保留 \% 转义
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)

    # 移除 \\command{...}{...}... 形式（包括嵌套花括号参数）
    # 先处理带参数的命令: \\command{...}
    # 简化处理：匹配 \字母序列{...} （一层花括号）
    text = re.sub(r'\\[a-zA-Z]+\{[^{}]*\}', '', text)

    # 反复清理直到没有变化，处理多层嵌套
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'\\[a-zA-Z]+\{[^{}]*\}', '', text)

    # 移除 \\command 形式（无参数的命令，如 \\par, \\\\
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # 移除特殊字符命令 \\, \\ 等
    text = re.sub(r'\\[^a-zA-Z\s]', '', text)

    # 移除剩余的花括号
    text = text.replace('{', '').replace('}', '')

    # 移除方括号内的可选参数（如 \\section[短标题]{长标题} 的短标题部分）
    # 注意：上面的正则已经移除了 \\section，这里处理残留的方括号
    text = re.sub(r'\[[^\]]*\]', '', text)

    # 将多个空白合并为单个空格
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def count_chinese(text: str) -> int:
    """
    统计中文字符数量。

    匹配 CJK 统一汉字区间 U+4E00..U+9FFF，
    以及 CJK 扩展 A 区间 U+3400..U+4DBF，
    覆盖绝大多数常用汉字。

    Args:
        text: 已清理的纯文本

    Returns:
        中文字符数
    """
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))


def count_english(text: str) -> int:
    """
    统计英文单词数量。

    通过提取连续的 ASCII 字母序列来识别英文单词，
    自动忽略数字、标点和空白字符。

    Args:
        text: 已清理的纯文本

    Returns:
        英文单词数
    """
    return len(re.findall(r'[a-zA-Z]+', text))


def find_tex_files(path: Path) -> list[Path]:
    """
    递归查找指定目录下的所有 .tex 文件。

    Args:
        path: 搜索根目录

    Returns:
        按文件名排序的 .tex 文件列表
    """
    if not path.exists():
        return []
    files = sorted(path.rglob('*.tex'))
    return [f for f in files if f.is_file()]
