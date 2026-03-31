# -*- coding: utf-8 -*-
"""
论文格式检查器 - 检查 .tex 和 .bib 文件的常见问题
"""

import re
from pathlib import Path
from typing import List, Dict


class FormatChecker:
    """格式检查器"""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.results: List[Dict] = []

    def run_all_checks(self) -> List[Dict]:
        """运行所有检查"""
        self.results.clear()

        tex_files = list(self.root.rglob("*.tex"))
        bib_files = list(self.root.rglob("*.bib"))

        for f in tex_files:
            self._check_tex(f)

        for f in bib_files:
            self._check_bib(f)

        return self.results

    def _add(self, level: str, filepath: str, line: int, message: str) -> None:
        self.results.append({
            "level": level,
            "file": filepath,
            "line": line,
            "message": message,
        })

    # ── .tex 检查 ──────────────────────────────────────────────

    def _check_tex(self, path: Path) -> None:
        rel = path.relative_to(self.root) if path.is_relative_to(self.root) else path.name

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self._add("error", str(rel), 0, "文件编码不是 UTF-8，请转换编码")
            return

        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # 检查空 label
            for m in re.finditer(r"\\label\{(\s*)\}", line):
                if m.group(1).strip() == "":
                    self._add("warning", str(rel), i, "空的 \\label{}")

            # 检查空 ref
            for m in re.finditer(r"\\ref\{(\s*)\}", line):
                if m.group(1).strip() == "":
                    self._add("error", str(rel), i, "空的 \\ref{}，引用未指定目标")

            # 检查 \cite 中空引用
            for m in re.finditer(r"\\cite\{(\s*)\}", line):
                if m.group(1).strip() == "":
                    self._add("warning", str(rel), i, "空的 \\cite{}")

        # 检查 \begin / \end 配对
        self._check_brace_pairs(content, rel)

        # 检查中英文摘要
        self._check_abstracts(content, rel)

    def _check_brace_pairs(self, content: str, rel: str) -> None:
        """检查 \\begin 和 \\end 是否配对"""
        begins: Dict[str, int] = {}
        ends: Dict[str, int] = {}

        for m in re.finditer(r"\\begin\{(\w+\*?)\}", content):
            env = m.group(1)
            begins[env] = begins.get(env, 0) + 1
        for m in re.finditer(r"\\end\{(\w+\*?)\}", content):
            env = m.group(1)
            ends[env] = ends.get(env, 0) + 1

        all_envs = set(begins.keys()) | set(ends.keys())
        for env in all_envs:
            b = begins.get(env, 0)
            e = ends.get(env, 0)
            if b > e:
                self._add("error", rel, 0, f"\\begin{{{env}}} 出现 {b} 次，但 \\end{{{env}}} 只有 {e} 次")
            elif e > b:
                self._add("error", rel, 0, f"\\end{{{env}}} 出现 {e} 次，但 \\begin{{{env}}} 只有 {b} 次")

    def _check_abstracts(self, content: str, rel: str) -> None:
        """检查是否有中英文摘要"""
        has_cn = bool(re.search(r"摘要|abstractcn|cnabstract", content, re.IGNORECASE))
        has_en = bool(re.search(r"\\begin\{abstract\}|Abstract|ABSTRACT", content, re.IGNORECASE))

        if not has_cn:
            self._add("warning", rel, 0, "未检测到中文摘要部分")
        if not has_en:
            self._add("warning", rel, 0, "未检测到英文 Abstract 部分")

    # ── .bib 检查 ──────────────────────────────────────────────

    def _check_bib(self, path: Path) -> None:
        rel = path.relative_to(self.root) if path.is_relative_to(self.root) else path.name

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self._add("error", str(rel), 0, "文件编码不是 UTF-8，请转换编码")
            return

        # 检查空的大括号条目
        entries = re.findall(r"@\w+\{([^,]+),", content)
        for key in entries:
            key = key.strip()
            if not key:
                self._add("error", str(rel), 0, "发现空的参考文献条目键")

        # 检查是否有任何条目
        if not entries:
            self._add("warning", str(rel), 0, ".bib 文件为空或格式不正确")
