# -*- coding: utf-8 -*-
"""
格式检查器测试
"""

import pytest
from pathlib import Path
import tempfile
import os

from paper_pilot.checker.format_checker import FormatChecker


def make_tex(content: str) -> Path:
    """创建临时 .tex 文件"""
    tmp = tempfile.NamedTemporaryFile(suffix=".tex", mode="w", encoding="utf-8", delete=False)
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


def make_bib(content: str) -> Path:
    """创建临时 .bib 文件"""
    tmp = tempfile.NamedTemporaryFile(suffix=".bib", mode="w", encoding="utf-8", delete=False)
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


class TestFormatChecker:

    def test_clean_tex_no_issues(self, tmp_path):
        """干净的 .tex 文件不应有任何问题"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
\begin{document}
摘要：这是中文摘要。
\begin{abstract}
This is the English abstract.
\end{abstract}
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        errors = [r for r in results if r["level"] == "error"]
        assert len(errors) == 0

    def test_mismatched_begin_end(self, tmp_path):
        """\\begin 和 \\end 不匹配应报错"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
摘要：中文摘要
\begin{abstract}English abstract\end{abstract}
\begin{document}
\begin{figure}
此处缺少 figure 环境的结束标签
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        # figure 环境缺少 \end{figure}
        assert any("figure" in r["message"].lower() for r in results)

    def test_empty_label(self, tmp_path):
        """空的 \\label{} 应报警告"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
\begin{document}
摘要：中文摘要
\begin{abstract}English abstract\end{abstract}
\label{}
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        warnings = [r for r in results if r["level"] == "warning" and "label" in r["message"]]
        assert len(warnings) >= 1

    def test_empty_ref(self, tmp_path):
        """空的 \\ref{} 应报错"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
\begin{document}
摘要：中文摘要
\begin{abstract}English abstract\end{abstract}
见图~\ref{}所示
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        errors = [r for r in results if r["level"] == "error" and "ref" in r["message"]]
        assert len(errors) >= 1

    def test_missing_chinese_abstract(self, tmp_path):
        """缺少中文摘要应报警告"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
\begin{document}
\begin{abstract}
Only English abstract here.
\end{abstract}
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        warnings = [r for r in results if "中文摘要" in r["message"]]
        assert len(warnings) >= 1

    def test_missing_english_abstract(self, tmp_path):
        """缺少英文摘要应报警告"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            r"""
\begin{document}
摘要：这是中文摘要内容。
\end{document}
""",
            encoding="utf-8",
        )
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        warnings = [r for r in results if "Abstract" in r["message"]]
        assert len(warnings) >= 1

    def test_empty_bib_file(self, tmp_path):
        """空的 .bib 文件应报警告"""
        bib = tmp_path / "refs.bib"
        bib.write_text("", encoding="utf-8")
        checker = FormatChecker(tmp_path)
        results = checker.run_all_checks()
        warnings = [r for r in results if r["level"] == "warning" and ".bib" in r["message"]]
        assert len(warnings) >= 1
