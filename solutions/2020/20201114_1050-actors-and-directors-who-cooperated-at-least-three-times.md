# #1050. 合作至少三次的演员和导演 / Actors and Directors Who Cooperated At Least Three Times

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/)

---

## 题目（英文原版）

**Description**

Table: ActorDirector
Write a solution to find all the pairs (actor_id, director_id) where the actor has cooperated with the director at least three times.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| actor_id    | int     |
| director_id | int     |
| timestamp   | int     |
+-------------+---------+
timestamp is the primary key (column with unique values) for this table.
```

**Example 2:**

```
Input: 
ActorDirector table:
+-------------+-------------+-------------+
| actor_id    | director_id | timestamp   |
+-------------+-------------+-------------+
| 1           | 1           | 0           |
| 1           | 1           | 1           |
| 1           | 1           | 2           |
| 1           | 2           | 3           |
| 1           | 2           | 4           |
| 2           | 1           | 5           |
| 2           | 1           | 6           |
+-------------+-------------+-------------+
Output: 
+-------------+-------------+
| actor_id    | director_id |
+-------------+-------------+
| 1           | 1           |
+-------------+-------------+
Explanation: The only pair is (1, 1) where they cooperated exactly 3 times.
```

---

## 题目（中文翻译）

**表（Table）**：`ActorDirector`  

编写一个查询，找出所有 `(actor_id, director_id)` 对，使得该演员与该导演的合作次数 **至少** 为三次。返回结果表，顺序不限。结果格式请参考下例。

**示例 1**  

| Column Name | Type |
|-------------|------|
| actor_id    | int  |
| director_id | int  |
| timestamp   | int  |

`timestamp` 为该表的 **主键（primary key）**，即唯一值的列。

**示例 2**  

**输入**  

`ActorDirector` 表：

| actor_id | director_id | timestamp |
|----------|-------------|-----------|
| 1        | 1           | 0         |
| 1        | 1           | 1         |
| 1        | 1           | 2         |
| 1        | 2           | 3         |
| 1        | 2           | 4         |
| 2        | 1           | 5         |
| 2        | 1           | 6         |

**输出**

| actor_id | director_id |
|----------|-------------|
| 1        | 1           |

**解释**：唯一满足条件的配对是 `(1, 1)`，他们恰好合作了 3 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把表中的每一行都拿出来，两两比较，看它们的 `(actor_id, director_id)` 是否相同。如果相同，就把这对组合的出现次数加一。  
- **用到的数据结构**：只用最原始的 `list`（相当于一摞纸条），把每一行当作一张卡片。  
- **生活化类比**：把表想象成一堆信件，每封信上写着“演员‑导演”。暴力做法就是把所有信件两两配对，看看有没有写着同样的名字。  
- **为什么正确**：只要把所有可能的配对都检查一遍，就不会漏掉任何一次合作，自然也能统计出每对出现了多少次。  

但是，这种做法会让我们不停地比较同一张卡片，导致大量重复工作。

#### 代码（Python）

```python
from typing import List, Tuple

def brute_force(actor_director: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """
    暴力解：两层循环遍历所有行，统计每对 (actor_id, director_id) 出现的次数。
    参数 actor_director 是表中的所有记录，每条记录是 (actor_id, director_id, timestamp)。
    返回满足出现次数 >= 3 的 (actor_id, director_id) 列表，顺序不要求。
    """
    n = len(actor_director)
    # 用一个字典暂存计数，key 为 (actor_id, director_id)
    cnt = {}

    # 双层遍历，比较每两条记录
    for i in range(n):
        a1, d1, _ = actor_director[i]
        for j in range(i + 1, n):          # 只比较一次，避免 i 与 i 自己比较
            a2, d2, _ = actor_director[j]
            if a1 == a2 and d1 == d2:       # 同一个演员和导演
                pair = (a1, d1)
                cnt[pair] = cnt.get(pair, 0) + 2   # 两条记录一起算两次出现

    # 上面的循环把每一次配对都算了两次（i,j）和 (j,i) 会各算一次，
    # 为了得到真实的出现次数，需要再除以 2。
    result = []
    for pair, times in cnt.items():
        real_times = times // 2
        if real_times >= 3:
            result.append(pair)

    return result
```

> **注意**：这里的实现仅作演示，实际运行会非常慢，尤其当记录数上万甚至更多时。

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 如果表里有 `n` 条记录，双层循环要检查 `n × (n‑1) / 2` 对组合，换句话说，记录数翻倍，比较次数会成 **平方** 增长。  
- **空间复杂度**：`O(k)` —— `k` 为不同 `(actor_id, director_id)` 对的数量，最坏情况下每条记录都是唯一的，这时 `k = n`，需要额外的字典来存放计数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复比较**：我们每次都要把两条记录拿出来比较，而其实只需要**一次遍历**就能知道每对演员‑导演出现了多少次。  
- 把每条记录的 `(actor_id, director_id)` 当作字典的 **key**，出现一次就把对应的计数 **+1**。  
- 这相当于把“查字典”比作“查电话本”：我们直接把演员‑导演的组合当成电话号码，出现一次就记下来，不用去找别的记录来验证。  

这样只需要 **一次** 线性遍历表格，时间从 `O(n²)` 降到 `O(n)`，空间只用保存每个不同组合的计数。

#### 代码（Python）

```python
from typing import List, Tuple

def optimal(actor_director: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """
    最优解：使用哈希表（Python 的 dict）一次遍历统计每对出现次数。
    返回出现次数 >= 3 的 (actor_id, director_id) 列表，顺序不要求。
    """
    # step1: 计数
    count = {}                         # key: (actor_id, director_id) , value: 出现次数
    for actor_id, director_id, _ in actor_director:
        pair = (actor_id, director_id)
        count[pair] = count.get(pair, 0) + 1   # 字典的 get 方法相当于“查字典”，不存在时返回 0

    # step2: 过滤满足条件的 pair
    result = [pair for pair, times in count.items() if times >= 3]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次表格，每条记录的计数操作是 **常数时间**（字典查找/插入），所以总体随记录数线性增长。  
- **空间复杂度**：`O(k)` —— 需要额外的字典保存每个不同的 `(actor_id, director_id)`，`k` 是不同组合的数量，最坏情况下 `k = n`，但仍比 `O(n²)` 小很多。

---

## 心得

- **核心技巧**：**哈希表（字典）计数**。把需要统计的对象直接映射成键，在遍历时把出现次数累加。  
- **适用的题型**  
  1. “找出出现次数≥k的元素”类（如 LeetCode 1087. 将数组划分为和相等的子数组）。  
  2. “统计配对出现次数”类（如 1651. 计算所有好对数目）。  
  3. “统计字符/单词频率”类（如 208. 实现 Trie 树的前缀计数）。  
- **一句话总结**：**把“比较”变成“计数”，用字典一次遍历完成所有统计**。

---

## 反思

- **第一反应**：看到“合作次数至少三次”，立刻想到要 **计数**，于是想到用字典把每对 `(actor, director)` 的出现次数记录下来。  
- **最容易踩的坑**  
  - 忘记把 `timestamp`（唯一键）排除在计数之外，只需要关注 `actor_id` 与 `director_id`。  
  - 统计时误把每条记录算两次（如暴力解中出现的 `+2`），导致结果偏大。  
  - 对空表或所有组合出现次数都小于 3 的情况，需要返回空列表而不是 `None`。  
- **下次遇到同类题**：第一步就要 **确定统计的维度**（本题是 `(actor_id, director_id)`），随后 **选用哈希表一次遍历**，最后 **根据阈值过滤**。这样可以快速得到正确且高效的答案。