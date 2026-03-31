# 🎓 Paper Pilot — 中国研究生论文写作助手

<div align="center">

**Paper Pilot** 是一个命令行工具，帮助中国研究生快速创建、检查和管理 LaTeX 学位论文。

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

[快速开始](#-快速开始) · [功能特性](#-功能特性) · [示例](#-使用示例) · [常见问题](#-常见问题)

</div>

---

## ✨ 功能特性

| 命令 | 功能 | 说明 |
|------|------|------|
| `pp init` | 📄 初始化论文项目 | 一键生成完整的 LaTeX 论文框架 |
| `pp check` | 🔍 格式检查 | 自动检查引用、标签、环境配对等 |
| `pp refs` | 📚 参考文献管理 | 查看、验证、统计 .bib 参考文献 |

### 为什么选择 Paper Pilot？

- 🇨🇳 **专为中文论文设计** — 内置符合中国高校学位论文规范的 LaTeX 模板
- ⚡ **零配置起步** — 一条命令生成完整论文结构
- 🔍 **智能检查** — 自动发现常见格式问题（未配对环境、空引用、缺失摘要等）
- 📚 **文献管理** — 一键查看、验证、统计参考文献
- 🎯 **多学位支持** — 学士、硕士、博士学位论文模板

## 🚀 快速开始

### 安装

```bash
pip install paper-pilot
```

> 需要 Python 3.8+ 和 LaTeX 环境（推荐 TeX Live 或 MiKTeX）

### 三步创建论文

```bash
# 1. 初始化论文项目
pp init my-thesis --title "基于深度学习的图像识别研究" --author "张三" --degree master

# 2. 进入项目目录，用 LaTeX 编译
cd my-thesis
xelatex main.tex

# 3. 检查格式
pp check
```

就这么简单！

## 📖 使用示例

### 初始化论文

```bash
# 默认硕士论文
pp init . --title "论文题目" --author "张三"

# 博士论文
pp init . --title "博士论文" --author "李四" --degree doctor

# 学士论文
pp init ./thesis --title "本科毕业论文" --author "王五" --degree bachelor
```

初始化后会生成完整的论文结构：

```
my-thesis/
├── main.tex           # 主文件（自动填入标题、作者）
├── references.bib     # 参考文献
└── chapters/
    ├── introduction.tex       # 绪论
    ├── literature_review.tex  # 文献综述
    ├── methodology.tex        # 研究方法
    ├── results.tex            # 实验结果
    └── conclusion.tex         # 总结与展望
```

### 格式检查

```bash
# 检查当前目录
pp check

# 检查指定目录（严格模式）
pp check --path ./thesis --strict
```

检查内容包括：
- ✅ `\begin{}` / `\end{}` 环境配对
- ✅ 空 `\label{}` 和 `\ref{}`
- ✅ 中英文摘要是否齐全
- ✅ 文件编码是否为 UTF-8
- ✅ `.bib` 文件完整性

### 参考文献管理

```bash
# 列出所有文献
pp refs

# 验证文献完整性
pp refs --check

# 查看统计信息
pp refs --stats
```

## 🎯 论文模板特点

Paper Pilot 内置的 LaTeX 模板包含：

- 📐 **标准页面布局** — A4 纸，符合高校要求的页边距
- 🏫 **完整封面页** — 包含学校、学院、专业、姓名等信息
- 📝 **中英文摘要** — 标准的中英文摘要与关键词格式
- 📑 **自动目录** — 目录、图目录、表目录
- 📊 **标准章节** — 绪论、文献综述、方法、结果、结论
- 📐 **图表示例** — 三线表、浮动图、公式编号
- 📚 **参考文献** — GB/T 7714 参考文献格式
- 🙏 **致谢** — 标准致谢页面

## 🛠️ 开发

```bash
git clone https://github.com/pikachu140233/paper-pilot.git
cd paper-pilot
pip install -e ".[dev]"
pytest
```

## 🤝 贡献

欢迎贡献！无论是：

- 🐛 提交 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📜 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果 Paper Pilot 对你有帮助，请给一个 ⭐ Star！**

Made with ❤️ by [pikachu140233](https://github.com/pikachu140233)

</div>
