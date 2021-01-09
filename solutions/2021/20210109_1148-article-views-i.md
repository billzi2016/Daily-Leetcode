# #1148. 文章浏览 I / Article Views I

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/article-views-i/)

---

## 题目（英文原版）

**Description**

Table: Views
Write a solution to find all the authors that viewed at least one of their own articles.
Return the result table sorted by id in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| article_id    | int     |
| author_id     | int     |
| viewer_id     | int     |
| view_date     | date    |
+---------------+---------+
There is no primary key (column with unique values) for this table, the table may have duplicate rows.
Each row of this table indicates that some viewer viewed an article (written by some author) on some date. 
Note that equal author_id and viewer_id indicate the same person.
```

**Example 2:**

```
Input: 
Views table:
+------------+-----------+-----------+------------+
| article_id | author_id | viewer_id | view_date  |
+------------+-----------+-----------+------------+
| 1          | 3         | 5         | 2019-08-01 |
| 1          | 3         | 6         | 2019-08-02 |
| 2          | 7         | 7         | 2019-08-01 |
| 2          | 7         | 6         | 2019-08-02 |
| 4          | 7         | 1         | 2019-07-22 |
| 3          | 4         | 4         | 2019-07-21 |
| 3          | 4         | 4         | 2019-07-21 |
+------------+-----------+-----------+------------+
Output: 
+------+
| id   |
+------+
| 4    |
| 7    |
+------+
```

---

## 题目（中文翻译）

**描述：**  
表：Views  

编写一个查询，找出所有至少浏览过自己撰写的文章的作者（author）。返回的结果表按 `author_id` 升序排列。结果格式参见下方示例。

**示例 1：**  

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| article_id    | int     |
| author_id     | int     |
| viewer_id     | int     |
| view_date     | date    |
+---------------+---------+
```

该表没有主键（唯一值列），可能存在重复行。表中的每一行表示某位浏览者（viewer_id）在某天（view_date）浏览了某篇文章（article_id），该文章的作者为 author_id。

**示例 2：**  

输入：  
Views 表：

```
+------------+-----------+-----------+------------+
| article_id | author_id | viewer_id | view_date  |
+------------+-----------+-----------+------------+
| 1          | 3         | 5         | 2019-08-01 |
| 1          | 3         | 6         | 2019-08-02 |
| 2          | 7         | 7         | 2019-08-01 |
| 2          | 7         | 6         | 2019-08-02 |
| 4          | 8         | 8         | 2019-08-01 |
| 4          | 8         | 5         | 2019-08-01 |
+------------+-----------+-----------+------------+
```

输出：

```
+-----------+
| author_id |
+-----------+
| 7         |
| 8         |
+-----------+
```

**解释：**  
- 作者 7 在 2019‑08‑01 浏览了自己撰写的文章 2。  
- 作者 8 在 2019‑08‑01 浏览了自己撰写的文章 4。  
因此，这两位作者满足条件，结果按 `author_id` 升序返回。

**约束条件：**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题本质上是把 **Views** 表（每一行代表一次阅读记录）遍历一遍，找出 `author_id` 与 `viewer_id` 相等的行。  
只要出现一次这种情况，就说明这位作者看过自己的文章。  

- **使用的数据结构**：  
  - `list`（或 `tuple`）来保存原始的阅读记录，想象成一本“阅读日志本”。  
  - `set`（集合）来保存满足条件的作者编号，集合就像一个“去重的收件箱”，同一个作者只会出现一次。  

- **为什么这个方法正确**：  
  - 我们检查每一条记录，**只要** 有一条记录满足 `author_id == viewer_id`，就把该作者加入答案集合。  
  - 最后把集合里的作者编号全部取出来并排序，正好符合题目要求。

- **时间/空间复杂度**（大白话版）  
  - **时间复杂度 O(n)**：我们只需要 **一次** 线性扫描 `n` 条记录，`n` 越大，耗时就线性增长。  
  - **空间复杂度 O(k)**：只需要额外存放满足条件的作者编号，最多不超过所有不同作者的数量 `k`（`k ≤ n`），所以是线性空间。

#### 代码（Python）

```python
from typing import List, Tuple

def authors_who_view_their_own_articles(views: List[Tuple[int, int, int, str]]) -> List[int]:
    """
    :param views: 每条记录是 (article_id, author_id, viewer_id, view_date)
    :return: 按 id 升序的作者列表
    """
    # 用集合收集满足条件的作者 id，集合会自动去重
    good_authors = set()                     # ← “去重的收件箱”

    for article_id, author_id, viewer_id, view_date in views:
        # 只要作者本人是观看者，就把作者 id 放进集合
        if author_id == viewer_id:           # ← 关键比较
            good_authors.add(author_id)

    # 把集合转成列表并排序，得到最终答案
    return sorted(good_authors)              # ← 按 id 升序返回
```

**关键行中文注释** 已在代码中给出，直接复制运行即可。

#### 复杂度

- **时间复杂度：O(n)**  
  只遍历一次 `views`，每条记录的比较、集合插入都是 O(1) 的操作。  
- **空间复杂度：O(k)**  
  需要额外的集合存放满足条件的作者 id，最坏情况下 `k` 等于所有不同作者的数量。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们已经发现唯一的瓶颈是 **遍历全部记录**。  
事实上，**不遍历** 是不可能的，因为我们必须检查每一条记录是否满足 `author_id == viewer_id`。  
因此 **O(n)** 已经是最优时间复杂度，无法再进一步降低。

唯一可以改进的地方是 **代码可读性** 与 **一次性完成所有工作**：

1. 使用 **列表推导式** 或 **生成器表达式** 把 “找出满足条件的作者” 与 “去重、排序” 合并在一起，使代码更简洁。  
2. 仍然使用 `set` 完成去重，这一步是必须的。

核心工具仍然是 **集合（Set）** —— 把它想象成“一本只能写一次的笔记本”，同一个作者只会被记一次。

#### 代码（Python）

```python
def authors_who_view_their_own_articles_opt(views: List[Tuple[int, int, int, str]]) -> List[int]:
    """
    更简洁的实现，时间复杂度仍是 O(n)，空间复杂度 O(k)。
    """
    # 直接用集合推导式把满足条件的 author_id 收集起来
    good_authors = {author_id for _, author_id, viewer_id, _ in views if author_id == viewer_id}
    # 把集合转为有序列表返回
    return sorted(good_authors)
```

#### 复杂度

- **时间复杂度：O(n)**  
  仍然只遍历一次 `views`，集合推导式内部的比较与插入都是常数时间。  
- **空间复杂度：O(k)**  
  只额外存放满足条件的作者 id，和暴力解使用的空间相同。

与暴力解相比，**时间上没有提升**（已经是最优），但 **代码更短、更易读**，这在实际面试或团队协作中同样重要。

---

## 心得

- **核心技巧**：利用集合去重并快速判断是否出现过目标关系（这里是 `author_id == viewer_id`）。  
- **适用的题型**：  
  1. “找出出现过某种配对关系的元素”——如 `User` 表中自我关注的用户。  
  2. “统计满足某种条件的唯一 ID”——如订单表中同一用户的多次购买。  
  3. “检查是否有交叉出现的两个字段相等的记录”。  
- **一句话总结解题钥匙**：**遍历一次，遇到符合条件的作者立即放进集合，最后排序输出**。

---

## 反思

- **第一反应**：看到 “author_id 与 viewer_id 相等” 直接想到遍历并比较，最直接的实现就是用 `if` 判断。  
- **最容易踩的坑**：  
  - **去重**：如果直接把所有满足条件的 `author_id` 放进列表，可能会出现重复，需要用 `set` 去重。  
  - **排序**：题目要求按 `id` 升序返回，忘记排序会导致答案不符合要求。  
  - **空表**：如果 `Views` 为空，返回的应该是空列表 `[]`，代码需要能够自然处理这种情况。  
- **下次遇到同类题**：第一步就思考 “是否只需要判断出现过一次的关系”，如果是，立刻决定使用 **集合** 来去重并收集答案。