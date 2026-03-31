# 🤝 贡献指南

感谢你对 Paper Pilot 的关注！欢迎贡献代码、文档或提出建议。

## 快速开始

1. Fork 本仓库
2. Clone 到本地：`git clone https://github.com/你的用户名/paper-pilot.git`
3. 安装开发依赖：`pip install -e ".[dev]"`
4. 运行测试：`pytest`

## 开发流程

1. 从 `main` 创建新分支：`git checkout -b feature/your-feature`
2. 编写代码和测试
3. 确保所有测试通过：`pytest -v`
4. 提交 PR，描述你的改动

## 代码规范

- Python 3.8+ 兼容
- 使用 Click 作为 CLI 框架
- 使用 Rich 进行终端输出美化
- 文件头加 `# -*- coding: utf-8 -*-`
- 中文注释
- 测试使用 pytest

## 提交 Issue

- 🐛 Bug：请描述复现步骤和期望行为
- 💡 新功能：请描述使用场景和预期效果
- 📄 文档：指出需要改进的部分

## 模板贡献

如果你有某个学校的 LaTeX 论文模板，欢迎贡献！请将模板放到 `src/paper_pilot/templates/` 下，并更新 `pp init` 命令支持选择不同模板。
