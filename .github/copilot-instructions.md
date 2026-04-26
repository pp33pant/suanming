# GitHub Copilot 项目说明

本仓库为「算命 · Suanming」八字排盘与分析工具。请在生成命理分析内容时，按以下顺序加载并应用 `.github/skills/` 下的 skill（详细索引见 [`.github/skills/skill_index.md`](skills/skill_index.md)）：

1. **`wuxing-shengke`** —— 五行生克制化角度的事实层分析
2. **`zhongnan-daoist`** —— 终南道家视角的义理层补充
3. **`dayun-liunian`** —— 大运流年的时间应期层
4. **`daoist-summary`** —— 道家眼中此命的综合总结（终章）

## 通用红线

- 命理仅供文化参考，**不构成医疗、法律、投资、婚恋决策建议**
- 不预言寿命、不指认姻缘对象、不预言子女细节
- 不使用「必」「定」「凶」「克」「煞」等绝对化或恐吓性词汇
- 引用经典必须真实出处（《道德经》《庄子》《清静经》《阴符经》《抱朴子》《悟真篇》《张三丰全集》等），**不得伪造**
- 输出语言：**简体中文**

## 代码风格

- Python 3.10+，类型注解齐备
- 模块化：`pillars.py`（排盘）/`elements.py`（基础数据）/`analysis.py`（分析）/`luck.py`（大运）/`ai.py`（LLM 解读）/`cli.py`/`web.py`
- 测试用 `pytest`，新增功能必须配单元测试
- 提交前 `ruff check` 通过

## PR 工作流

默认开发分支：`copilot/pr-workflow-archive-v1`
- 在该分支提交改动
- 推送后开 PR 合并到 `main`
- 不直接向 `main` 推送
