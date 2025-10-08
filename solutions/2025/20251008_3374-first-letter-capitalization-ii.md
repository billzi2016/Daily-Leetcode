# #3374. First Letter Capitalization II / First Letter Capitalization II

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/first-letter-capitalization-ii/)

---

## 题目（英文原版）

**Description**

Table: user_content
Write a solution to transform the text in the content_text column by applying the following rules:
Return the result table that includes both the original content_text and the modified text following the above rules.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| content_id  | int     |
| content_text| varchar |
+-------------+---------+
content_id is the unique key for this table.
Each row contains a unique ID and the corresponding text content.
```

**Example 2:**

```
+------------+---------------------------------+
| content_id | content_text                    |
+------------+---------------------------------+
| 1          | hello world of SQL              |
| 2          | the QUICK-brown fox             |
| 3          | modern-day DATA science         |
| 4          | web-based FRONT-end development |
+------------+---------------------------------+
```

**Example 3:**

```
+------------+---------------------------------+---------------------------------+
| content_id | original_text                   | converted_text                  |
+------------+---------------------------------+---------------------------------+
| 1          | hello world of SQL              | Hello World Of Sql              |
| 2          | the QUICK-brown fox             | The Quick-Brown Fox             |
| 3          | modern-day DATA science         | Modern-Day Data Science         |
| 4          | web-based FRONT-end development | Web-Based Front-End Development |
+------------+---------------------------------+---------------------------------+
```

---

## 题目（中文翻译）

表：user_content  

编写一个查询，对 **content_text 列 (column)** 中的文本按以下规则进行转换：  
返回的结果表中同时包含原始的 **content_text** 和按照上述规则转换后的文本。  
结果格式参见下方示例。  

示例：

示例 1:  
+-------------+---------+  
| Column Name | Type    |  
+-------------+---------+  
| content_id  | int     |  
| content_text| varchar |  
+-------------+---------+  
content_id 是该表的唯一键。  
每行包含唯一的 ID 以及对应的文本内容。  

示例 2:  
+------------+---------------------------------+  
| content_id | content_text                    |  
+------------+---------------------------------+  
| 1          | hello world of SQL              |  
| 2          | the QUICK-brown fox             |  
| 3          | modern-day DATA science         |  
| 4          | web-based FRONT-end development |  
+------------+---------------------------------+  

示例 3:  
+------------+---------------------------------+-------------------------------+  
| content_id | original_text                   | converted_text                |  
+------------+---------------------------------+-------------------------------+  
| 1          | hello world of SQL              | Hello World Of Sql           |  
| 2          | the QUICK-brown fox             | The Quick-Brown Fox          |  
| …          | …                               | …                             |  
+------------+---------------------------------+-------------------------------+  

约束条件：  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一行的 `content_text` 逐字符遍历，遇到单词的第一个字符就把它变成大写，其他字符变成小写。  
这里有两个「分割点」需要注意：

1. **空格**：空格把句子切成普通单词。  
2. **连字符 `-`**：连字符把「复合词」再切一次，例如 `quick-brown` 实际上是两个子单词 `quick` 和 `brown`，每个子单词的首字母都要大写。

可以把这两个分割点看成「字典的查找键」——我们先把字符串按空格切成「单词块」，再把每个块按 `-` 再切一次。对每个最小的子单词调用 Python 的 `str.capitalize()`（把首字母大写、其余小写），然后把子单词用 `-` 拼回去，最后把所有块用空格拼回去。

这种做法的正确性来源于：

- 只要把每个「真正的单词」的首字母大写、其余字母小写，就满足题目要求。  
- 我们没有遗漏任何字符，因为每次都是完整地把原字符串分割、处理、再合并。

#### 代码（Python）

```python
def convert_brute(rows):
    """
    暴力实现：对每一行的 content_text 逐行处理。
    参数 rows: List[Tuple[int, str]]  → (content_id, content_text)
    返回值: List[Tuple[int, str, str]] → (content_id, original_text, converted_text)
    """
    result = []
    for cid, text in rows:                     # 遍历每一行
        # 1. 先按空格切分成“块”
        blocks = text.split(' ')
        new_blocks = []
        for blk in blocks:                     # 处理每个块
            # 2. 再按连字符切分成子单词
            parts = blk.split('-')
            # 3. 对每个子单词做首字母大写，其余小写
            new_parts = [p.capitalize() for p in parts]
            # 4. 用连字符把子单词拼回去
            new_blocks.append('-'.join(new_parts))
        # 5. 用空格把所有块拼成完整句子
        converted = ' '.join(new_blocks)
        result.append((cid, text, converted))
    return result
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 为表中的行数，`L` 为单行文本的字符数。我们遍历每个字符一次（切分、`capitalize` 都是线性操作），所以整体是「行数 × 文本长度」的线性时间。用大白话说，就是「如果有 1000 行、每行 200 字，总共要处理 200 000 个字符」。
- **空间复杂度**：`O(N * L)`（输出表的大小）+ `O(L)`（每行临时的分割列表）  
  - 额外的临时空间只和单行长度成正比，最坏情况下需要保存切分后的列表。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性** 的，没有明显的「慢点」可以进一步削减时间。  
不过我们可以把代码写得更简洁、可读性更高，同时只使用一次遍历来完成「分割 → 转换 → 合并」的全部工作，避免创建多余的中间列表。

核心技巧：

- **一次遍历 + 状态机**：用一个布尔变量 `need_cap` 标记「当前字符是否是一个单词的首字母」。  
  - 初始时 `need_cap = True`（因为文本最左边的字符是首字母）。  
  - 遇到空格或连字符后，说明下一个字符又是新单词的开始，把 `need_cap` 设回 `True`。  
  - 其他字符则保持 `need_cap = False`。  
- **字符级处理**：直接对每个字符调用 `upper()` / `lower()`，不需要 `split`、`join` 再拼。

这样做的好处：

- 只遍历一次字符串，省去 `split`/`join` 带来的额外遍历。  
- 代码更接近「手工改写」的过程，便于在面试中口头说明。

#### 代码（Python）

```python
def convert_opt(rows):
    """
    最优实现：一次遍历每个字符，使用状态机判断是否需要大写。
    参数 rows: List[Tuple[int, str]]
    返回值: List[Tuple[int, str, str]]
    """
    def transform(s: str) -> str:
        res = []                 # 用列表收集字符，最后一次性拼成字符串
        need_cap = True          # 首字符需要大写
        for ch in s:
            if ch == ' ' or ch == '-':   # 空格或连字符后，下一字符是新单词的首字母
                res.append(ch)           # 直接保留分隔符
                need_cap = True
            else:
                if need_cap:
                    res.append(ch.upper())   # 首字母大写
                else:
                    res.append(ch.lower())   # 其余字母小写
                need_cap = False            # 已经处理过首字母
        return ''.join(res)

    result = []
    for cid, txt in rows:
        result.append((cid, txt, transform(txt)))
    return result
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - 仍然是对每个字符遍历一次，只是把「分割」和「拼接」的额外遍历合并进来了。相比暴力解，常数因子更小（不需要 `split`、`join` 多次）。
- **空间复杂度**：`O(N * L)`（输出）+ `O(L)`（单行临时字符列表）  
  - 与暴力解相同的量级，但临时空间仅是一维字符列表。

---

## 心得

- **核心技巧**：**一次遍历+状态机** 判断何时需要大写。  
- **适用题型**：  
  1. **标题大小写**（Title Case）或 **首字母大写** 的字符串处理。  
  2. **自定义分隔符**（如点号、斜杠）下的单词首字母转换。  
  3. **过滤/转换** 类题目，需要在遍历时保持「前一个字符」的信息（例如去掉多余空格、压缩连续标点等）。  
- **一句话总结**：把「每个单词的首字符」看成「需要大写的状态」，用布尔标记在一次遍历中完成全部转换。

---

## 反思

- **第一反应**：看到「把每个单词的首字母大写」马上想到 `split` → `capitalize` → `join`，这在 Python 中写起来非常直观。  
- **最容易踩的坑**：  
  - **连字符**：如果只按空格切分，`quick-brown` 会被当作一个整体，导致 `b` 不会大写。  
  - **连续分隔符**（如 `"hello  world"` 两个空格）会产生空的子串，需要保证空串不被误处理。  
  - **全大写/全小写混杂**：一定要在非首字符时强制转成小写，否则会留下原来的大小写。  
- **下次思路**：面对「按某些字符分割后对每个子块做统一转换」的题目，第一步先在脑中把「分割符」抽象成「状态切换点」，然后决定是 **两次 split** 还是 **一次遍历 + 状态机**，根据数据规模选最省时的实现。