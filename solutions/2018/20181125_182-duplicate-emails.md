# #182. 重复的电子邮件 / Duplicate Emails

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/duplicate-emails/)

---

## 题目（英文原版）

**Description**

Table: Person
Write a solution to report all the duplicate emails. Note that it's guaranteed that the email field is not NULL.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains an email. The emails will not contain uppercase letters.
```

**Example 2:**

```
Input: 
Person table:
+----+---------+
| id | email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
Output: 
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
Explanation: a@b.com is repeated two times.
```

---

## 题目（中文翻译）

表（Table）: Person  
编写一个查询，报告所有出现重复的电子邮件（email）。请注意，已保证 **email** 字段（field）不为 **NULL**。  
返回的结果表可以任意顺序。结果格式见下方示例。

**示例 1**

示例表结构：

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| email       | varchar |

- **id** 是该表的主键（primary key），即唯一值的列（column）。  
- 每行记录包含一个电子邮件地址（email），且电子邮件中不含大写字母。

**示例 2**

**输入**  
Person 表：

| id | email   |
|----|---------|
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |

**输出**  

| Email   |
|---------|
| a@b.com |

**解释**：a@b.com 出现了两次。

约束条件：  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把每一行的 `email` 都和后面的每一行比较一遍，只要出现相同的 `email` 就记下来。  
- **使用的数据结构**：我们把整张表当成一个普通的 Python 列表，每条记录用字典 `{'id':..., 'email':...}` 表示。列表就像一排排的信件，遍历它们就像一个人一次检查一封信。  
- **为什么正确**：因为我们把所有可能的两两组合都检查了一遍，只要有重复就一定会被发现。  
- **时间/空间复杂度**：  
  - **时间**：外层循环遍历 `n` 条记录，内层循环最多再遍历 `n‑1` 条记录，整体是 `n × n ≈ n²`，即 **O(n²)**。这里的 “O” 只是一种上限的表示，意思是“随着记录数增多，运行时间会像平方一样快”。  
  - **空间**：我们只额外用了一个 `set`（或列表）来保存已经找到的重复邮箱，最坏情况下最多保存 `n` 条，故是 **O(n)**。  

#### 代码（Python）  

```python
from typing import List, Dict

def duplicate_emails_brute(person: List[Dict[str, str]]) -> List[str]:
    """
    暴力解：两层循环检查每两个 email 是否相同
    :param person: 表示 Person 表的记录列表，每条记录形如 {'id': 1, 'email': 'a@b.com'}
    :return: 重复出现的 email 列表（去重后返回）
    """
    n = len(person)
    seen = set()          # 已经确认出现过重复的邮箱
    result = set()        # 用 set 自动去重

    for i in range(n):
        email_i = person[i]['email']
        # 如果已经在 seen 里，说明之前已经找到了它的重复，就不必再比较了
        if email_i in seen:
            continue
        for j in range(i + 1, n):
            if email_i == person[j]['email']:
                result.add(email_i)   # 记录下来
                break                  # 该邮箱已确认重复，跳出内层循环
        else:
            # 内层循环正常结束（没有 break），说明 i 位置的邮箱没有重复
            seen.add(email_i)

    return list(result)
```

#### 复杂度  

- **时间复杂度**：O(n²) —— 随着记录数 n 增加，比较次数大约是 n 的平方。  
- **空间复杂度**：O(n) —— 需要额外的集合来存放最多 n 条邮箱（最坏情况所有邮箱都不重复）。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈**在于我们不停地把同一个邮箱和后面的所有邮箱比较，导致了二次遍历。  
要把这个过程改成一次遍历，只需要在遍历的同时记住每个邮箱出现的次数。  
- **核心数据结构**：**哈希表**（Python 中的 `dict` 或 `collections.Counter`）。哈希表就像一本**查字典**，我们把 **email** 当成“单词”，把出现次数当成“页码”。查找、插入、更新的时间都是 **O(1)**，也就是说几乎不花时间。  
- **一步步的推导**：  
  1. **第一次遍历**：把所有记录的 `email` 统计出现次数。  
  2. **第二次遍历**（或直接在第一遍结束后筛选）：把出现次数大于 1 的邮箱挑出来，就是我们要的重复邮箱。  
- **为什么正确**：如果一个邮箱出现两次或更多次，它在统计表里的计数一定会大于 1；反之，计数为 1 的邮箱一定没有重复。  
- **类比**：想象你在超市结账时，收银员会把每种商品的条码记录在一个表格里，最后把数量大于 1 的商品挑出来，这正是我们现在做的事。  

#### 代码（Python）  

```python
from collections import Counter
from typing import List, Dict

def duplicate_emails_opt(person: List[Dict[str, str]]) -> List[str]:
    """
    最优解：利用哈希表一次遍历统计出现次数，再筛选出重复的 email
    :param person: 同上
    :return: 重复出现的 email 列表（去重后返回）
    """
    # 第一步：统计每个 email 出现了多少次
    email_counter = Counter(row['email'] for row in person)   # O(n) 时间

    # 第二步：挑选出现次数 > 1 的 email
    duplicates = [email for email, cnt in email_counter.items() if cnt > 1]  # O(k) 时间，k 为不同 email 数量

    return duplicates
```

#### 复杂度  

- **时间复杂度**：O(n) —— 只需要一次遍历（`Counter`）和一次遍历哈希表（通常比 n 小），线性增长。相比暴力的 O(n²) 快很多。  
- **空间复杂度**：O(m) —— 需要存放哈希表，`m` 是不同邮箱的数量，最坏情况 `m = n`，所以也是 O(n)。  

---  

## 心得  

- **核心技巧**：使用哈希表（字典 / Counter）统计出现次数，快速定位重复元素。  
- **适用的题型**：  
  1. “找出出现次数超过 k 次的元素” （如 LeetCode 347: 前 K 个高频元素）  
  2. “数组/字符串中出现次数唯一的元素” （如 LeetCode 169: 多数元素）  
  3. “两数组交集并去重” （利用集合或计数）  
- **一句话总结**：**把“比较”变成“计数”，用哈希表把 O(n²) 的暴力遍历压缩到 O(n)。**  

## 反思  

- **第一反应**：看到“重复”二字，立刻想到两层循环逐个比较——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记去重返回结果，直接把所有出现的记录输出会导致重复行。  
  - 对于大数据集，暴力解会超时；一定要意识到可以用哈希表“一遍搞定”。  
  - 在实际数据库环境中，需要注意 `email` 列不为空且不含大写，这让我们可以直接用字符串比较，不必做大小写统一。  
- **下次第一步**：先问自己“有没有可以一次遍历就统计的信息？”——如果答案是“有”，立刻上哈希表；如果没有，再考虑排序或双指针等别的技巧。