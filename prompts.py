def _fmt_examples(examples: list) -> str:
    parts = []
    for ex in examples:
        parts.append(f"示例 {ex['example_num']}:\n{ex['example_text'].strip()}")
    return "\n\n".join(parts) if parts else "无"


def _fmt_list(items: list) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "无"


def translation_prompt(problem: dict) -> str:
    examples_text = _fmt_examples(problem.get("examples", []))
    constraints_text = _fmt_list(problem.get("constraints", []))

    return f"""你是一位专业的 LeetCode 题目中文翻译专家。

请将以下题目翻译为流畅、准确的简体中文。

要求：
- 第一行仅输出中文题目名称（不含序号），例如：两数之和
- 第二行起开始正文翻译
- 技术术语首次出现时保留英文括号注释，如：子数组（subarray）
- 数学符号保持原样（如 10^9）
- 示例的输入/输出保留原样，只翻译 Explanation 部分
- 直接输出 Markdown，不要任何前言，不要解题

题目标题：{problem['title']}

描述：
{problem.get('description', '')}

示例：
{examples_text}

约束条件：
{constraints_text}"""


def solution_prompt(problem: dict) -> str:
    examples_text = _fmt_examples(problem.get("examples", []))
    constraints_text = _fmt_list(problem.get("constraints", []))
    hints_text = _fmt_list(problem.get("hints", []))
    topics = "、".join(problem.get("topics", []))

    return f"""你是一位耐心、专业的算法导师。你的读者是编程初学者——他们懂基础 Python 语法，但对算法和数据结构还很陌生。

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

标题：{problem['title']}
难度：{problem.get('difficulty', '')}
标签：{topics}

描述：
{problem.get('description', '')}

示例：
{examples_text}

约束条件：
{constraints_text}

提示（hints）：
{hints_text}"""
