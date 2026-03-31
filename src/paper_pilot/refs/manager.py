# -*- coding: utf-8 -*-
"""
参考文献管理器 - 解析和操作 .bib 文件
"""

import re
from pathlib import Path
from typing import List, Dict


class RefManager:
    """BibTeX 参考文献管理器"""

    def __init__(self, root: Path) -> None:
        self.root = root

    def find_bib_files(self) -> List[Path]:
        """查找项目中的所有 .bib 文件"""
        return list(self.root.rglob("*.bib"))

    def parse_bib(self, path: Path) -> List[Dict]:
        """解析 .bib 文件，返回条目列表"""
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            return []

        entries = []
        # 匹配 @type{key, ... } 块
        pattern = r"@\s*(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}"
        for m in re.finditer(pattern, content, re.DOTALL):
            entry_type = m.group(1).lower()
            key = m.group(2).strip()
            body = m.group(3)

            fields = self._parse_fields(body)
            fields["type"] = entry_type
            fields["key"] = key
            entries.append(fields)

        return entries

    @staticmethod
    def _parse_fields(body: str) -> Dict[str, str]:
        """解析条目字段"""
        fields: Dict[str, str] = {}
        # 匹配 field = {value} 或 field = "value" 或 field = value
        field_pattern = r'(\w+)\s*=\s*(?:\{([^}]*)\}|"([^"]*)"|(\S+))'
        for m in re.finditer(field_pattern, body):
            key = m.group(1).lower()
            value = m.group(2) or m.group(3) or m.group(4) or ""
            value = value.strip().rstrip(",")
            fields[key] = value
        return fields
