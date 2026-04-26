# 算命 · Suanming

> 基于天干地支的八字（四柱）排盘与命理分析工具：四柱计算 → 五行十神 → 大运流年 → 道家视角解读。

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![ci](https://github.com/pp33pant/suanming/actions/workflows/ci.yml/badge.svg)

## ✨ 功能

- **四柱排盘**：年/月/日/时柱，基于 [`sxtwl`](https://github.com/yuttie/sxtwl_cpp) 寿星天文历，立春换年、节令换月精准
- **五行十神**：天干地支五行、地支藏干、十神映射、五行强弱量化
- **大运流年**：阳男阴女顺排 / 阴男阳女逆排，按节气距离 / 3 折算起运岁
- **AI 解读**（可选）：调用 OpenAI 兼容接口，结合下方 4 个 Copilot skills 给出道家视角分析
- **CLI**：`suanming bazi --date 1995-08-15 --time 14:30 --gender M`

> 前端 / Web UI 为下一阶段计划，当前只提供 CLI 与 Python API。

## 🧠 命理分析 Skill 体系

`.github/skills/` 下定义了 4 个 Copilot skill，由 AI 按顺序调用，构成完整命理报告。完整调用规则见 [`skill_index.md`](.github/skills/skill_index.md)：

| 顺序 | Skill | 角度 | 输出 |
|------|-------|------|------|
| 1 | [`wuxing-shengke`](.github/skills/wuxing-shengke/SKILL.md) | 五行生克制化 | 日主旺衰、喜用忌神、补救方向 |
| 2 | [`zhongnan-daoist`](.github/skills/zhongnan-daoist/SKILL.md) | 终南道家义理 | 命之气象、道分、性命双修 |
| 3 | [`dayun-liunian`](.github/skills/dayun-liunian/SKILL.md) | 大运流年 | 每步大运评判、近 5-10 年节点 |
| 4 | [`daoist-summary`](.github/skills/daoist-summary/SKILL.md) | 道家眼中此命 | 五段式综合总结 + 经典箴言 |

四个 skill 的红线（不预言寿命 / 不指认姻缘 / 不渲染凶煞 / 经典必有真出处）写在各自 SKILL.md 中。

## 🚀 快速上手

```bash
git clone git@github.com:pp33pant/suanming.git
cd suanming
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/Mac: source .venv/bin/activate
pip install -e ".[ai,dev]"

# 排盘
suanming bazi --date 1995-08-15 --time 14:30 --gender M

# 大运
suanming luck --date 1995-08-15 --time 14:30 --gender M --count 8

# AI 解读（需要 OPENAI_API_KEY）
export OPENAI_API_KEY=sk-...
suanming reading --date 1995-08-15 --time 14:30 --gender M
```

## 🗂️ 目录结构

```
suanming/
├── src/suanming/
│   ├── pillars.py     # 四柱：年/月/日/时干支
│   ├── elements.py    # 天干地支五行、藏干、十神映射
│   ├── analysis.py    # 五行强弱、十神分布
│   ├── luck.py        # 大运、流年
│   ├── ai.py          # LLM 解读
│   └── cli.py         # Typer CLI
├── scripts/           # 一次性脚本（如 calc_bazi.py 批量排盘）
├── tests/             # pytest 用例
└── .github/
    ├── copilot-instructions.md   # 总入口：skill 调用顺序与红线
    ├── skills/                   # 4 个命理分析 skill
    └── workflows/ci.yml          # GitHub Actions CI
```

## 🧪 开发

```bash
pytest                      # 跑测试
ruff check src tests        # lint
```

## 📚 命理基础（速览）

- **天干**：甲乙丙丁戊己庚辛壬癸
- **地支**：子丑寅卯辰巳午未申酉戌亥
- **五行生克**：木→火→土→金→水→木；木克土、土克水、水克火、火克金、金克木
- **节气换月**：立春→寅、惊蛰→卯、清明→辰…；月柱以**节**为界，非农历初一
- **晚子时**：23:00–23:59 是否过日，依门派而定，本工具默认**过日**（可关闭）

## 🪐 PR 工作流

默认开发分支 `copilot/pr-workflow-archive-v1`：在该分支提交改动 → 推送后开 PR → 合并到 `main`。**不直接向 `main` 推送。**

## ⚠️ 免责声明

本项目仅供文化研究与个人兴趣，**不构成医疗、法律、投资、婚恋决策建议**。命理仅供参考，路在自己脚下。

## 📄 许可证

MIT © pp33pant
