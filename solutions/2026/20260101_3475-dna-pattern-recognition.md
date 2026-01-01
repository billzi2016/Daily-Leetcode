# #3475. DNA 模式识别 / DNA Pattern Recognition 

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/dna-pattern-recognition/)

---

## 题目（英文原版）

**Description**

Table: Samples
Biologists are studying basic patterns in DNA sequences. Write a solution to identify sample_id with the following patterns:
Return the result table ordered by sample_id in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    | 
+----------------+---------+
| sample_id      | int     |
| dna_sequence   | varchar |
| species        | varchar |
+----------------+---------+
sample_id is the unique key for this table.
Each row contains a DNA sequence represented as a string of characters (A, T, G, C) and the species it was collected from.
```

**Example 2:**

```
+-----------+------------------+-----------+
| sample_id | dna_sequence     | species   |
+-----------+------------------+-----------+
| 1         | ATGCTAGCTAGCTAA  | Human     |
| 2         | GGGTCAATCATC     | Human     |
| 3         | ATATATCGTAGCTA   | Human     |
| 4         | ATGGGGTCATCATAA  | Mouse     |
| 5         | TCAGTCAGTCAG     | Mouse     |
| 6         | ATATCGCGCTAG     | Zebrafish |
| 7         | CGTATGCGTCGTA    | Zebrafish |
+-----------+------------------+-----------+
```

**Example 3:**

```
+-----------+------------------+-------------+-------------+------------+------------+------------+
| sample_id | dna_sequence     | species     | has_start   | has_stop   | has_atat   | has_ggg    |
+-----------+------------------+-------------+-------------+------------+------------+------------+
| 1         | ATGCTAGCTAGCTAA  | Human       | 1           | 1          | 0          | 0          |
| 2         | GGGTCAATCATC     | Human       | 0           | 0          | 0          | 1          |
| 3         | ATATATCGTAGCTA   | Human       | 0           | 0          | 1          | 0          |
| 4         | ATGGGGTCATCATAA  | Mouse       | 1           | 1          | 0          | 1          |
| 5         | TCAGTCAGTCAG     | Mouse       | 0           | 0          | 0          | 0          |
| 6         | ATATCGCGCTAG     | Zebrafish   | 0           | 1          | 1          | 0          |
| 7         | CGTATGCGTCGTA    | Zebrafish   | 0           | 0          | 0          | 0          |
+-----------+------------------+-------------+-------------+------------+------------+------------+
```

---

## 题目（中文翻译）

表: Samples  
生物学家正在研究 DNA 序列中的基本模式。编写一个查询，找出满足以下模式的 `sample_id`：  
返回结果表按 `sample_id` **升序** 排序。  
结果格式见下例。

示例：

示例 1:
```sql
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| sample_id      | int     |
| dna_sequence   | varchar |
| species        | varchar |
+----------------+---------+
```
`sample_id` 为该表的唯一键。每行包含一个用字符 (A, T, G, C) 表示的 DNA 序列以及其采集自的物种。

示例 2:
```sql
+-----------+----------------+-----------+
| sample_id | dna_sequence   | species   |
+-----------+----------------+-----------+
| 1         | ATGCTAGCTAGCTAA| Human     |
| 2         | GGGTCAATCATC   | Human     |
| 3         | ATATATCGTAGCTA | Human     |
| 4         | ATGGGGTCATCATAA| Mouse     |
| 5         | TCAGTCAGTCAG   | Mouse     |
| 6         | ATATCGCGCTAG   | Zebrafi
... (已截断)
```

示例 3:
```sql
+-----------+----------------+-----------+-----------+-----------+-----------+-----------+
| sample_id | dna_sequence   | species   | has_start | has_stop  | has_atat  | has_ggg   |
+-----------+----------------+-----------+-----------+-----------+-----------+-----------+
| 1         | ATGCTAGCTAGCTAA| Human     | 1         | 1         | 0         | 0         |
... (已截断)
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目给出一张 `Samples` 表，每行包含 DNA 序列 `dna_sequence`（只由 `A,T,G,C` 四个字符组成）。我们需要为每条记录生成四个布尔字段：

| 字段 | 含义 |
|------|------|
| `has_start` | 序列中是否出现 **ATG**（起始密码子） |
| `has_stop`  | 序列中是否出现 **TAA**（终止密码子，题目示例里用了 TAA） |
| `has_atat` | 序列中是否出现 **ATAT** |
| `has_ggg`  | 序列中是否出现 **GGG** |

> **类比**：把 DNA 序列想象成一本书的文字，`ATG`、`TAA`… 就是我们要找的特定词。  
> 在 Python 中，`sub in s` 的操作就像在书的目录里查词——**哈希表**（字典）把每个词映射到它出现的页码，查找是 *O(1)* 的。但这里我们直接用字符串的 `in` 操作，底层会遍历一次序列来判断是否包含子串，最直观的实现就是 **暴力搜索**。  

实现思路非常直接：对每一行记录，分别用 `if "ATG" in seq`、`if "TAA" in seq` … 判断子串是否出现，出现就记 `1`，否则记 `0`。  

为什么这个方法一定能得到正确答案？因为我们检查的就是题目要求的“是否出现”。只要序列中出现一次对应的子串，`in` 运算就会返回 `True`，对应的标记就为 `1`。  

**时间/空间复杂度**（大白话）  
- 对每条记录，`in` 操作会遍历一次序列，最坏情况下要看完整个序列（长度记作 `L`）。我们要检查 4 个子串，所以每条记录的时间是 `4 × O(L)` → `O(L)`。  
- 若表中有 `n` 条记录，总时间就是 `O(n·L)`。如果把 `L` 看成“平均序列长度”，可以写成 `O(n·m)`（`m` 代表序列长度）。  
- 额外空间只用来存放结果的几列，和输入规模无关，记作 `O(1)`。  

#### 代码（Python）  

```python
# -------------------------------------------------
# 直觉解：逐行检查子串是否出现
# -------------------------------------------------
from typing import List, Dict

def flag_patterns_brute(samples: List[Dict]) -> List[Dict]:
    """
    参数 samples：每条记录是一个 dict，至少包含
        - 'sample_id' (int)
        - 'dna_sequence' (str)
    返回值：每条记录增加四个标记字段，值为 0/1
    """
    result = []
    for row in samples:
        seq = row["dna_sequence"]          # 取出 DNA 序列
        # 下面四行分别判断子串是否出现，出现记 1，否则记 0
        has_start = 1 if "ATG" in seq else 0   # 起始密码子
        has_stop  = 1 if "TAA" in seq else 0   # 终止密码子（示例使用 TAA）
        has_atat  = 1 if "ATAT" in seq else 0  # 连续的 ATAT
        has_ggg   = 1 if "GGG"  in seq else 0  # 连续的 GGG

        # 生成新记录（保留原始字段 + 四个标记）
        new_row = {
            "sample_id": row["sample_id"],
            "has_start": has_start,
            "has_stop":  has_stop,
            "has_atat":  has_atat,
            "has_ggg":   has_ggg,
        }
        result.append(new_row)

    # 按 sample_id 升序返回（符合题目要求）
    return sorted(result, key=lambda x: x["sample_id"])
```

**使用示例**

```python
samples = [
    {"sample_id": 1, "dna_sequence": "ATGCTAGCTAGCTAA"},
    {"sample_id": 2, "dna_sequence": "GGGTCAATCATC"},
    {"sample_id": 3, "dna_sequence": "ATATATCGTAGCTA"},
    {"sample_id": 4, "dna_sequence": "ATGGGGTCATCATAA"},
]

print(flag_patterns_brute(samples))
# 输出：
# [{'sample_id': 1, 'has_start': 1, 'has_stop': 1, 'has_atat': 0, 'has_ggg': 0},
#  {'sample_id': 2, 'has_start': 0, 'has_stop': 0, 'has_atat': 0, 'has_ggg': 1},
#  {'sample_id': 3, 'has_start': 0, 'has_stop': 0, 'has_atat': 1, 'has_ggg': 0},
#  {'sample_id': 4, 'has_start': 1, 'has_stop': 1, 'has_atat': 0, 'has_ggg': 1}]
```

#### 复杂度  

- **时间复杂度**：`O(n·L)`（`n` 为记录数，`L` 为序列平均长度）。可以理解为“对每条记录，我们要走一遍它的 DNA”。  
- **空间复杂度**：`O(1)`（不计返回结果本身的空间，只用了常数个临时变量）。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们的 **瓶颈** 在于每条记录对同一个序列做了 4 次独立的遍历（`"ATG" in seq`、`"TAA" in seq` …），实际上一次遍历就能把四个子串的出现情况全部判断出来。  

**优化思路**：

1. **一次扫描**：用滑动窗口遍历序列的每个位置，窗口大小取最长模式的长度（这里是 4，因为 `ATAT`、`GGG` 最长为 4）。  
2. **同时匹配**：在每个窗口中检查它是否等于任意目标模式。如果相等，就把对应的标记设为 `1`。  
3. **提前结束**：当四个标记全部为 `1` 时，后面的字符再也不需要检查，直接退出本条记录的循环。  

这样，每条记录只遍历一次序列，时间从 `4·L` 降到 `L`，即 **线性时间**。  

如果模式数量更大、长度更不统一，常用的**多模式匹配**算法是 **Aho‑Corasick 自动机**，它可以在一次遍历中匹配上百甚至上千个子串。这里为了保持代码简洁、易懂，手写一个“手工版”滑动窗口即可达到最优。  

**核心概念解释**  

- **滑动窗口**：把一根尺子（窗口）放在序列上，从左到右依次移动，每次读取窗口内的字符组合。想象你在阅读 DNA 时，用一只放大镜只看 4 个字符，往后滑动一格再看下一个 4‑字符组合。  
- **提前结束**：相当于在找宝藏的过程中，一旦已经找到所有宝藏，就不必继续挖掘。  

#### 代码（Python）  

```python
# -------------------------------------------------
# 最优解：一次遍历同时匹配所有模式
# -------------------------------------------------
from typing import List, Dict

def flag_patterns_one_pass(samples: List[Dict]) -> List[Dict]:
    """
    用一次线性扫描判断四个子串是否出现。
    """
    # 需要匹配的模式及其对应的标记字段名
    patterns = {
        "ATG": "has_start",
        "TAA": "has_stop",
        "ATAT": "has_atat",
        "GGG": "has_ggg",
    }
    # 记录每个模式的长度，方便滑动窗口
    max_len = max(len(p) for p in patterns)   # 本题是 4

    result = []
    for row in samples:
        seq = row["dna_sequence"]
        n = len(seq)

        # 初始化标记为 0
        flags = {field: 0 for field in patterns.values()}

        # 只要还有未被置 1 的标记，就继续遍历
        for i in range(n):
            # 为了不越界，只检查窗口长度不超过剩余字符数的情况
            # 同时只需要检查最长窗口 max_len
            for length in range(1, max_len + 1):
                if i + length > n:
                    break
                sub = seq[i:i+length]          # 当前子串（窗口）

                # 若子串正好是我们要找的模式，就把对应标记置 1
                if sub in patterns:
                    flags[patterns[sub]] = 1

            # 所有标记已经全部为 1，直接结束本条记录的循环
            if all(v == 1 for v in flags.values()):
                break

        # 组装结果行
        new_row = {
            "sample_id": row["sample_id"],
            "has_start": flags["has_start"],
            "has_stop":  flags["has_stop"],
            "has_atat":  flags["has_atat"],
            "has_ggg":   flags["has_ggg"],
        }
        result.append(new_row)

    # 按 sample_id 升序返回
    return sorted(result, key=lambda x: x["sample_id"])
```

**使用示例**

```python
samples = [
    {"sample_id": 1, "dna_sequence": "ATGCTAGCTAGCTAA"},
    {"sample_id": 2, "dna_sequence": "GGGTCAATCATC"},
    {"sample_id": 3, "dna_sequence": "ATATATCGTAGCTA"},
    {"sample_id": 4, "dna_sequence": "ATGGGGTCATCATAA"},
]

print(flag_patterns_one_pass(samples))
# 与暴力解得到的结果完全相同，但遍历次数更少
```

#### 复杂度  

- **时间复杂度**：`O(n·L)`（每条记录只遍历一次序列），比暴力解的 `4·n·L` 少了常数因子 4。可以把它想象成“只走一次路”。  
- **空间复杂度**：`O(1)`（只用常数个变量保存标记），同样不随输入规模增长。  

---

## 心得  

- **核心技巧**：**一次遍历多模式匹配**（滑动窗口 + 提前结束）。  
- **适用的题型**  
  1. 给定字符串列表，需要判断每个字符串是否包含若干子串（如 DNA、日志、URL 等）。  
  2. “在一段文本里找多个关键字是否出现”——如搜索引擎的关键词预筛选。  
  3. 多模式匹配的进阶版：字符流实时检测多个模式（可使用 Aho‑Corasick）。  

> **解题钥匙**：把“检查多个子串”视作“一次遍历所有字符”，用窗口一次性比较，避免重复遍历。  

---

## 反思  

- **第一反应**：看到四个子串，直接写四条 `if sub in seq`，这就是最直接的暴力思路。  
- **最容易踩的坑**  
  - 忘记区分大小写（DNA 只有大写，代码里也要保持一致）。  
  - 子串长度不统一时，窗口的上限必须取 **最长模式的长度**，否则会出现 `IndexError`。  
  - 当序列很短（长度小于某些模式）时，`in` 检查仍然返回 `False`，不需要额外的边界处理。  
- **下次遇到同类题**：第一步先问自己——“是否可以在一次遍历里把所有需要的判断都完成？”如果答案是 **是**，就立刻考虑滑动窗口或 Aho‑Corasick；如果 **否**，再回到暴力实现。