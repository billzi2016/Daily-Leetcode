# Daily LeetCode — 产品需求文档 (PRD)

## 一、项目概述

读取 `leetcode_problems.json` 中的 2913 道 LeetCode 题目，为每道题生成双语 Markdown 解析文档，并以题目对应的历史日期正向提交 git（oldest commit first），形成一份从 2018-06-04 到 2026-05-25 跨越 8 年的 LeetCode 刷题记录。

**刷题语言：Python（全部题目统一使用 Python，不涉及其他语言）。**

---

## 二、日期映射（核心）

```
题目索引 i（0-based） → commit 日期 = 2018-06-04 + i 天

索引 0    → #1   Two Sum                → 2018-06-04
索引 1    → #2   Add Two Numbers        → 2018-06-05
...
索引 2912 → #3640 Trionic Array II      → 2026-05-25
```

**提交顺序：从索引 0 到 2912，正向提交（oldest first）。**

git 历史效果：

```
* 2026-05-25  solve #3640: Trionic Array II         ← HEAD（最新）
* 2026-05-24  solve #3639: ...
...
* 2018-06-04  solve #1: Two Sum                     ← 最早
```

---

## 三、数据源

| 字段 | 说明 |
|------|------|
| 文件 | `leetcode_problems.json` |
| 结构 | `{ "questions": [...] }` |
| 题目总数 | 2913 题 |
| 英文原版 | 直接从 JSON 字段拼装，**不经过 LLM** |
| 传给 LLM | 按字段提取后结构化注入 prompt，**不做整体序列化** |

---

## 四、技术栈

| 组件 | 选型 |
|------|------|
| 语言 | Python 3.10+ |
| LLM | Ollama 本地，模型 `gpt-oss:120b` |
| Ollama API | `http://localhost:11434/api/generate` |
| git 日期设定 | `GIT_AUTHOR_DATE` + `GIT_COMMITTER_DATE` 环境变量 |
| LLM 调用次数 | 每道题**恰好 2 次**：翻译 1 次 + 题解 1 次 |
| 进度显示 | `tqdm`，`--all` 模式及单题内部步骤均显示进度条 |

---

## 五、目录结构（扁平）

```
Daily-Leetcode/
├── leetcode_problems.json   # 原始题库（只读）
├── config.py                # 全局配置
├── llm.py                   # Ollama 调用封装
├── prompts.py               # Prompt 模板
├── committer.py             # git commit 封装（专职提交）
├── main.py                  # 入口，串联全流程
└── solutions/
    ├── 2018/
    │   └── 20180604_1-two-sum.md
    ├── ...
    └── 2026/
        └── 20260525_3640-trionic-array-ii.md
```

> 无子包，无嵌套模块，5 个 `.py` 文件平铺在根目录。

---

## 六、输出文件规范

### 6.1 路径

```
solutions/{YYYY}/{YYYYMMDD}_{frontend_id}-{problem_slug}.md
```

### 6.2 Markdown 拼装流程

最终 Markdown 由三段**字符串拼接**而成，分隔符为 `\n\n---\n\n`：

```
段 A（英文原版）  ← 由 main.py 直接从 JSON 字段拼装，不调用 LLM
段 B（中文翻译）  ← Ollama 第 1 次调用结果
段 C（题解文档）  ← Ollama 第 2 次调用结果
```

完整结构：

```markdown
# #{frontend_id}. {中文题目名} / {英文题目名}

> 难度：{难度中文} · 标签：{topics} · [LeetCode 链接](https://leetcode.com/problems/{problem_slug}/)

---

## 题目（英文原版）

<!-- ↓ 以下全部由 JSON 字段直接拼装，不经过 LLM -->

**Description**

{description 字段，去除末尾的 "Example N:" / "Constraints:" 占位行}

**Examples**

Example 1:

```
{examples[0].example_text}
```

Example 2:

```
{examples[1].example_text}
```

...

**Constraints**

- {constraints[0]}
- {constraints[1]}
...

---

## 题目（中文翻译）

<!-- ↓ Ollama 第 1 次调用输出（translation_prompt） -->
<!-- 响应第一行为中文题目名，main.py 提取后用于顶部标题，其余为正文 -->

{中文描述正文（含示例翻译、约束翻译）}

---

<!-- ↓ Ollama 第 2 次调用输出（solution_prompt），直接追加，不加额外标题 -->

## 解题过程

### 1. 直觉解（暴力）
...

### 2. 最优解
...

## 心得
...

## 反思
...
```

---

## 七、模块职责

### 7.1 `config.py`

```python
OLLAMA_MODEL  = "gpt-oss:120b"
OLLAMA_URL    = "http://localhost:11434/api/generate"
DATA_FILE     = "leetcode_problems.json"
SOLUTIONS_DIR = "solutions"
START_DATE    = "2018-06-04"   # 索引 0（Two Sum）对应的日期
TIMEOUT       = 300            # Ollama 请求超时（秒）
```

---

### 7.2 `llm.py` — Ollama 调用封装

- `generate(prompt: str) -> str`：POST 请求，`stream: false`，返回完整文本
- 失败时打印错误并退出，不静默吞错

---

### 7.3 `prompts.py` — Prompt 模板

两个函数，均接收 `problem: dict`，返回 `str`。内部从字段提取并格式化后注入。

---

**`translation_prompt(problem: dict) -> str`**

```
你是一位专业的 LeetCode 题目中文翻译专家。

请将以下题目翻译为流畅、准确的简体中文。

要求：
- 第一行仅输出中文题目名称（不含序号），例如：两数之和
- 第二行起开始正文翻译
- 技术术语首次出现时保留英文括号注释，如：子数组（subarray）
- 数学符号保持原样（如 10^9）
- 示例的输入/输出保留原样，只翻译 Explanation 部分
- 直接输出 Markdown，不要任何前言，不要解题

题目标题：{title}

描述：
{description}

示例：
{examples_text}

约束条件：
{constraints_text}
```

> `main.py` 读取响应后，将**第一行**作为中文题目名写入顶部标题，**第二行起**作为 § B 翻译正文。

---

**`solution_prompt(problem: dict) -> str`**

```
你是一位耐心、专业的算法导师。你的读者是编程初学者——他们懂基础 Python 语法，但对算法和数据结构还很陌生。

请针对以下 LeetCode 题目，用简体中文写出一份面向初学者的解题文档。
代码统一使用 Python，不提供其他语言版本。
直接输出 Markdown，不要任何前言，不要开头的 "---" 分隔线。文档结构如下：

## 解题过程

### 1. 直觉解（暴力）

#### 思路

描述"最直接、最笨"的想法：
- 解释用到的数据结构，用生活化类比（如：哈希表就像查字典，key 是词，value 是页码）
- 说明为什么这个方法正确
- 分析时间/空间复杂度，用大白话解释 O(n²) 等符号的实际含义

#### 代码（Python）

（可运行代码，每个关键行有中文注释）

#### 复杂度

- 时间复杂度：O(?) — 含义解释
- 空间复杂度：O(?) — 含义解释

---

### 2. 最优解

#### 思路

从暴力解出发：
- 指出慢在哪里（瓶颈）
- 一步步推导优化思路
- 核心算法/数据结构（动态规划、双指针、单调栈、前缀和等）必须从零解释，不能假设读者已知
- 用类比或图示文字辅助理解关键步骤

#### 代码（Python）

（可运行代码，每个关键行有中文注释）

#### 复杂度

- 时间复杂度：O(?) — 含义解释，与暴力解对比
- 空间复杂度：O(?) — 含义解释

---

## 心得

- 这道题考察的核心技巧
- 该技巧适用的题型（列举 2-3 个类似题）
- 一句话总结"解题钥匙"

## 反思

- 拿到题目第一反应是什么
- 最容易踩的坑（边界条件、溢出、特殊情况等）
- 下次遇到同类题，第一步该想到什么

---

题目信息：

标题：{title}
难度：{difficulty}
标签：{topics}

描述：
{description}

示例：
{examples_text}

约束条件：
{constraints_text}

提示（hints）：
{hints_text}
```

---

### 7.4 `committer.py` — git commit 封装（专职）

**职责**：所有 git 操作集中在此模块，`main.py` 不直接调用 `subprocess`。

**对外接口**：

```python
def commit_file(file_path: str, frontend_id: str, title: str, date_str: str) -> None:
    """
    git add <file_path>，然后以 date_str 当天随机时间（08:00–23:30）提交。
    commit message 格式：solve #{frontend_id}: {title}
    """
```

**随机时间**：

```python
def random_commit_time(date_str: str) -> str:
    base = datetime.strptime(date_str, "%Y-%m-%d")
    minutes = random.randint(8 * 60, 23 * 60 + 30)
    dt = base + timedelta(minutes=minutes)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")
```

**Commit 命令**（通过 `subprocess` 执行）：

```bash
GIT_AUTHOR_DATE="{datetime}" GIT_COMMITTER_DATE="{datetime}" \
  git commit -m "solve #{frontend_id}: {title}"
```

**CLI 用法**（可单独运行）：

```bash
python committer.py <file_path> <frontend_id> <title> <date_YYYY-MM-DD>
```

---

### 7.5 `main.py` — 主入口

**CLI 用法**：

```
python main.py               # 处理下一道未完成的题目（自动续接）
python main.py --all         # 批量处理所有未完成的题目
python main.py --index 0     # 强制处理指定索引的题目
python main.py --dry-run     # 只打印题目信息，不调用 LLM，不写文件
```

**单题处理流程**：

```
1. 扫描 solutions/ 中的 .md 文件数量 N，确定下一题索引 N
2. 加载 questions[N]
3. commit_date = 2018-06-04 + N 天

── 段 A：英文原版（不调用 LLM）──────────────────────────────────
4. 从 description 字段去除末尾 "Example N:" / "Constraints:" 占位行
5. 将 examples 数组逐条格式化为 Markdown 代码块
6. 将 constraints 数组格式化为列表
7. 拼装 "## 题目（英文原版）" 段落 → english_md

── 段 B：中文翻译（Ollama 第 1 次调用）────────────────────────────
8. 调用 llm.generate(translation_prompt(problem))
9. 响应第一行 → chinese_title（用于顶部标题）
   响应第二行起 → translation_body → "## 题目（中文翻译）\n\n{translation_body}"

── 段 C：题解（Ollama 第 2 次调用）─────────────────────────────────
10. 调用 llm.generate(solution_prompt(problem)) → solution_md

── 拼装 & 写入 ────────────────────────────────────────────────────
11. header = "# #{id}. {chinese_title} / {title}\n\n> 难度：... · ..."
12. final_md = header + "\n\n---\n\n" + english_md
                       + "\n\n---\n\n" + chinese_section
                       + "\n\n---\n\n" + solution_md
13. 写入 solutions/{YYYY}/{YYYYMMDD}_{id}-{slug}.md

── 提交 ────────────────────────────────────────────────────────────
14. committer.commit_file(path, frontend_id, title, commit_date)
```

**`--all` 模式**：从 N 开始循环，用 `tqdm` 进度条显示总进度（已完成/总数），直到所有 2913 题处理完毕。单题内部步骤（翻译→题解→写入→提交）在进度条描述字段中实时更新。

---

## 八、Git 提交规范

### Commit Message 格式

```
solve #1: Two Sum
solve #2: Add Two Numbers
...
solve #3640: Trionic Array II
```

无 AI 署名，无 emoji，纯净专业。

---

## 九、运行示例

```bash
# 每天运行一次（自动处理下一题）
python main.py
# → #1 Two Sum   → solutions/2018/20180604_1-two-sum.md
#   commit date: 2018-06-04T14:37:22（随机时间）

# 或一次性批量生成全部 2913 题
python main.py --all
```

---

## 十、异常处理

| 场景 | 处理方式 |
|------|----------|
| Ollama 未启动 | 打印 `[ERROR] 请先运行 ollama serve`，退出码 1 |
| 模型响应超时 | 超 TIMEOUT 秒后报错并提示检查模型是否加载 |
| 文件已存在 | 跳过，打印 `[SKIP] 已存在: ...` |
| JSON 解析失败 | 直接抛出，不静默 |

---

## 十一、依赖

```
requests
tqdm
```

安装：`pip install requests tqdm`

---

## 十二、不做的事

- 不做 Web UI，不做数据库
- 不自动推送远程（用户手动 `git push`）
- 不做题目筛选（按顺序，一题不漏）
- 不支持多语言代码（统一 Python，不提供其他语言版本）
- 不做断点续传文件锁（靠 solutions/ 文件数量自动续接即可）
