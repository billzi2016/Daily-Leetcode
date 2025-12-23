# #3465. 查找具有有效序列号的产品 / Find Products with Valid Serial Numbers

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-products-with-valid-serial-numbers/)

---

## 题目（英文原版）

**Description**

Table: products
Write a solution to find all products whose description contains a valid serial number pattern. A valid serial number follows these rules:
Return the result table ordered by product_id in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+--------------+------------+
| Column Name  | Type       |
+--------------+------------+
| product_id   | int        |
| product_name | varchar    |
| description  | varchar    |
+--------------+------------+
(product_id) is the unique key for this table.
Each row in the table represents a product with its unique ID, name, and description.
```

**Example 2:**

```
+------------+--------------+------------------------------------------------------+
| product_id | product_name | description                                          |
+------------+--------------+------------------------------------------------------+
| 1          | Widget A     | This is a sample product with SN1234-5678            |
| 2          | Widget B     | A product with serial SN9876-1234 in the description |
| 3          | Widget C     | Product SN1234-56789 is available now                |
| 4          | Widget D     | No serial number here                                |
| 5          | Widget E     | Check out SN4321-8765 in this description            |
+------------+--------------+------------------------------------------------------+
```

**Example 3:**

```
+------------+--------------+------------------------------------------------------+
| product_id | product_name | description                                          |
+------------+--------------+------------------------------------------------------+
| 1          | Widget A     | This is a sample product with SN1234-5678            |
| 2          | Widget B     | A product with serial SN9876-1234 in the description |
| 5          | Widget E     | Check out SN4321-8765 in this description            |
+------------+--------------+------------------------------------------------------+
```

---

## 题目（中文翻译）

**描述**  
表（table）: `products`  
编写一个查询，找出所有描述（description）中包含有效序列号（serial number）模式的产品。有效序列号遵循下列规则：  
（此处应列出规则，原题未给出，保持原样）  

返回的 **结果表（result table）** 按 `product_id` 升序排列。  
结果格式参见下方示例。

**示例**  

示例 1:  
```
+--------------+------------+
| Column Name  | Type       |
+--------------+------------+
| product_id   | int        |
| product_name | varchar    |
| description  | varchar    |
+--------------+------------+
```
`product_id` 为该表的唯一键。每一行代表一个产品，包含唯一的 ID、名称和描述。

示例 2:  
```
+------------+--------------+--------------------------------------------------------+
| product_id | product_name | description                                            |
+------------+--------------+--------------------------------------------------------+
| 1          | Widget A     | This is a sample product with SN1234-5678            |
| 2          | Widget B     | A product with serial SN9876-1                         |
... (已截断)
```

示例 3:  
```
+------------+--------------+--------------------------------------------------------+
| product_id | product_name | description                                            |
+------------+--------------+--------------------------------------------------------+
| 1          | Widget A     | This is a sample product with SN1234-5678            |
| 2          | Widget B     | A product with serial SN9876-1                         |
... (已截断)
```

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把每一行描述都完整读一遍**，在文字里寻找符合“序列号”格式的子串。  
- **数据结构**：把表中的每一行当作一个普通的 Python `dict`（或 `tuple`），所有行放进一个 `list`。这就像把一本电话簿的每一页放进一个装有多页纸的文件夹，遍历文件夹就能看到每一页。  
- **序列号的模式**：题目说「有效的序列号」形如 `SN` 开头，后面接数字、连字符 `-`，再接数字。用正则表达式可以把这种“文字规则”写成 `r'\bSN\d+-\d+\b'`（`\b` 表示单词边界，`\d+` 表示一段或多段数字）。正则表达式就像一本 **查字典**，我们把 “SN1234-5678” 当成词，字典里记录的就是它的结构规则。  
- **为什么正确**：只要描述里出现了满足正则的子串，就说明它包含了一个合法的序列号；否则就不符合要求。遍历全部行并检查每行，必然能找出所有符合条件的产品。  

#### 代码（Python）

```python
import re
from typing import List, Dict

def find_products_bruteforce(products: List[Dict]) -> List[Dict]:
    """
    暴力实现：逐行检查 description 是否包含符合规则的序列号。
    参数 products 是形如 [{'product_id': 1, 'product_name': 'A', 'description': '...'}, ...] 的列表。
    返回满足条件的行，按 product_id 升序排列。
    """
    # 正则：SN + 至少一个数字 + - + 至少一个数字，单词边界保证不会匹配到 SN1234-5678abc 之类
    pattern = re.compile(r'\bSN\d+-\d+\b')

    ans = []
    for row in products:                     # ⬅️ 逐行遍历（相当于遍历数据库的每一条记录）
        desc = row['description']
        if pattern.search(desc):             # ⬅️ 在描述里找一次，若找到则说明有合法序列号
            ans.append(row)                  # ⬅️ 把符合条件的记录保存下来

    # 按 product_id 升序返回
    ans.sort(key=lambda x: x['product_id'])
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 为表的行数（产品数量），`L` 为每条描述的平均长度。我们对每一行都要在字符串里跑一次正则匹配，最坏情况下要检查全部字符。用大白话说，就是“如果表里有 10 万行，每行描述有 100 个字符，那么大约要检查 1000 万个字符”。  
- **空间复杂度**：`O(K)`  
  - `K` 为最终返回的符合条件的记录数（最坏情况下 K=N）。我们只额外保存满足条件的行和正则对象本身。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每条记录都要执行一次正则匹配，而正则的内部实现本身已经是线性扫描，基本没有进一步加速的空间。真正可以提升的是 **把正则的编译工作提前**，避免在每次循环里都重新解释正则表达式。  

优化步骤：

1. **一次性编译正则**：`re.compile` 会把模式转换成内部的状态机，只需要做一次，后面直接复用。相当于把“查字典”这本字典先印好，之后每查一个词只需要翻页，而不是每次都重新印一本。  
2. **一次遍历即可**：仍然需要遍历所有行，因为题目要求找出 **所有** 符合条件的产品，无法跳过任何记录。  
3. **使用生成器 + `sorted`**：如果数据量非常大，可以先用生成器筛选，再一次性排序，省掉额外的列表拷贝。  

核心概念 **正则表达式**：把文字模式抽象成机器可以直接执行的“指令”。对初学者来说，只要记住 `\d` 代表数字，`+` 代表“一次或多次”，`-` 直接匹配字符本身，`\b` 保证是完整的单词，就能写出我们需要的模式。  

#### 代码（Python）

```python
import re
from typing import List, Dict, Iterable

def find_products_optimal(products: Iterable[Dict]) -> List[Dict]:
    """
    最优实现：预编译正则、一次遍历、一次排序。
    参数 products 可以是 list，也可以是任何可迭代的对象（如文件读取器）。
    """
    # 预编译正则，只做一次
    serial_pat = re.compile(r'\bSN\d+-\d+\b')

    # 使用生成器表达式筛选符合条件的记录，省掉中间列表的临时空间
    filtered = (row for row in products if serial_pat.search(row['description']))

    # 把筛选后的记录一次性收集到列表并排序（按 product_id 升序）
    result = sorted(filtered, key=lambda x: x['product_id'])
    return result
```

#### 复杂度

- **时间复杂度**：`O(N * L)`（与暴力解相同）  
  - 由于正则匹配本身已经是最优的线性扫描，提前编译只把常数因子降低了。可以把它想象成“跑同样的路程，但每一步的准备工作更少”。  
- **空间复杂度**：`O(K)`（与暴力解相同）  
  - 只存放符合条件的记录以及正则对象本身，正则对象大小固定，不随输入规模增长。

---

## 心得

- **核心技巧**：正则表达式（Regex）——把“文字模式”抽象成机器可直接匹配的规则。  
- **适用的题型**  
  1. **字符串过滤**：如 “找出所有邮箱地址符合 `xxx@yyy.com` 格式的用户”。  
  2. **日志分析**：从服务器日志里提取符合 IP 地址或时间戳格式的行。  
  3. **文本清洗**：在自然语言处理前，先把不符合规则的噪声字符剔除。  
- **解题钥匙**：**先把规则写成正则，再一次性编译并遍历**。

---

## 反思

- **第一反应**：看到 “序列号” 这种固定格式的字符，就想到用 **正则** 去匹配。  
- **最容易踩的坑**  
  - **漏掉单词边界**：如果不加 `\b`，像 `SN1234-5678abc` 也会被误判为合法。  
  - **大小写问题**：题目未说明大小写敏感，默认大小写匹配；若需不区分大小写，需要在 `compile` 时加 `re.IGNORECASE`。  
  - **描述为空或缺失字段**：在真实数据库里可能出现 `NULL`，代码里要先判断 `desc` 是否为字符串。  
- **下次第一步**：**把题目给出的格式抽象成正则**，确认好每个字符的意义后，再决定是否需要预编译或其他优化手段。