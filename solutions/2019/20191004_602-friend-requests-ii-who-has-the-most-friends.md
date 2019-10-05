# #602. 好友请求 II：谁拥有最多的朋友 / Friend Requests II: Who Has the Most Friends

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/)

---

## 题目（英文原版）

**Description**

Table: RequestAccepted
Write a solution to find the people who have the most friends and the most friends number.
The test cases are generated so that only one person has the most friends.
The result format is in the following example.
Follow up: In the real world, multiple people could have the same most number of friends. Could you find all these people in this case?

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| requester_id   | int     |
| accepter_id    | int     |
| accept_date    | date    |
+----------------+---------+
(requester_id, accepter_id) is the primary key (combination of columns with unique values) for this table.
This table contains the ID of the user who sent the request, the ID of the user who received the request, and the date when the request was accepted.
```

**Example 2:**

```
Input: 
RequestAccepted table:
+--------------+-------------+-------------+
| requester_id | accepter_id | accept_date |
+--------------+-------------+-------------+
| 1            | 2           | 2016/06/03  |
| 1            | 3           | 2016/06/08  |
| 2            | 3           | 2016/06/08  |
| 3            | 4           | 2016/06/09  |
+--------------+-------------+-------------+
Output: 
+----+-----+
| id | num |
+----+-----+
| 3  | 3   |
+----+-----+
Explanation: 
The person with id 3 is a friend of people 1, 2, and 4, so he has three friends in total, which is the most number than any others.
```

---

## 题目（中文翻译）

描述  
表（Table）：`RequestAccepted`  
编写一个解决方案，找出拥有最多朋友的人以及对应的朋友数量。测试用例保证只有一个人拥有最多的朋友。结果格式参照下面的示例。

后续问题：在真实世界中，可能会有多个人拥有相同的最多朋友数。请在这种情况下找出所有这些人。

示例 1  
+----------------+---------+  
| Column Name    | Type    |  
+----------------+---------+  
| requester_id   | int     |  
| accepter_id    | int     |  
| accept_date    | date    |  
+----------------+---------+  
`(requester_id, accepter_id)` 是该表的主键（primary key），即唯一值组合的列。该表记录了发送请求的用户 ID、接受请求的用户 ID，以及请求被接受的日期。

示例 2  
Input:  
RequestAccepted table:  
+--------------+-------------+-------------+  
| requester_id | accepter_id | accept_date |  
+--------------+-------------+-------------+  
| 1            | 2           | 2016/06/03  |  
| 1            | 3           | 2016/06/08  |  
| 2            | 3           | 2016/06/08  |  
| 3            | 4           | 2016/06/09  |  
+--------------+-------------+-------------+  

Output:  
+----+-----+  
| id | num |  
+----+-----+  
| 3  | 3   |  
+----+-----+  

Explanation:  
ID 为 3 的人是 1、2、4 的朋友，因此他总共有 3 位朋友，是所有人中最多的。

约束条件  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

- **数据结构**：用一个 Python 字典 `cnt`（键是用户 ID，值是该用户的朋友数）来记录每个人拥有的朋友数量。  
  - 这里的字典可以类比成生活中的**查字典**：你把朋友的 ID 当成“单词”，对应的朋友数量当成“页码”。  
- **为什么正确**：题目说“朋友是双向的”，也就是说一条记录 `(requester_id, accepter_id)` 同时意味着 `requester_id` 与 `accepter_id` 互为朋友。遍历表中的每一行，分别把 `requester_id` 和 `accepter_id` 的计数各加 1，最后字典里保存的就是每个人的朋友数。  
- **找出最多的朋友**：遍历字典一次，记录出现的最大值 `max_num`，以及对应的用户 ID `max_id`（题目保证唯一）。  

> **时间/空间复杂度大白话**  
> - **时间复杂度 O(n)**：如果表里有 `n` 条记录，我们只需要一次遍历，每条记录做常数次（两个字典增值）操作，所以耗时跟记录条数成正比。想象一下你把所有记录排成一条长队，逐个检查一次，花的时间就是队长 * 1。  
> - **空间复杂度 O(m)**：`m` 是不同用户的数量（最坏情况下每条记录的两个人都是新的人），我们需要一个字典来存放每个人的计数。相当于我们在桌面上摆放了 `m` 张小卡片，每张卡片记一个人的朋友数。

#### 代码（Python）  

```python
from typing import List, Tuple

def most_friends_bruteforce(requests: List[Tuple[int, int, str]]) -> Tuple[int, int]:
    """
    暴力（直觉）解法
    :param requests: 每条记录为 (requester_id, accepter_id, accept_date)
    :return: (id, num)——拥有最多朋友的用户 id 以及朋友数量
    """
    # 用字典统计每个人的朋友数，键是用户 id，值是朋友数量
    cnt = {}                               # 初始化空字典
    for requester, accepter, _ in requests:
        # requester 与 accepter 互为朋友，计数各加 1
        cnt[requester] = cnt.get(requester, 0) + 1
        cnt[accepter] = cnt.get(accepter, 0) + 1

    # 找出朋友数最多的那个人
    max_id, max_num = None, -1
    for uid, num in cnt.items():
        if num > max_num:                  # 只要出现更大的，就更新
            max_id, max_num = uid, num

    return max_id, max_num
```

> **关键行中文注释**  
> - `cnt = {}`：创建一个空的“查字典”。  
> - `cnt.get(key, 0)`：如果字典里没有这个键，就返回默认值 0，类似于字典里没有这本书时返回第 0 页。  
> - `if num > max_num`：不断刷新“最高分”，最后留下最高分对应的学生（用户）。

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次表，`n` 为记录数。  
- **空间复杂度**：`O(m)` —— 需要保存所有不同用户的计数，`m` 为用户数。  

---  

### 2. 最优解  

#### 思路  

从暴力解看，它已经是 **线性** 的，几乎没有可以再“提速”的空间。  
真正的“最优”在 **代码简洁度** 与 **利用语言内置高效实现** 上：

1. **一次性把所有用户 ID 拉平**：每条记录里有两个人，我们可以把所有 `requester_id` 与 `accepter_id` 放进同一个列表。想象把所有朋友关系的两端拆开，排成一条长长的数字串。  
2. **使用 `collections.Counter` 直接计数**：`Counter` 是 Python 为统计出现次数专门优化的数据结构，内部实现用了哈希表，速度比手写的 `dict.get` 更快。  
3. **一次 `max` 操作找出最大值**：`max(counter.items(), key=lambda x: x[1])` 能在 O(m) 时间内直接得到拥有最多朋友的用户和数量。  

> **为什么比暴力更好**  
> - **代码量更少**：把“遍历两次、手动更新计数”压缩成“一行拉平 + 一行计数”。  
> - **底层优化**：`Counter` 在 C 实现的内部循环里完成计数，常数因子更小。  

> **如果出现多人并列最多**（题目 Follow‑up），只需要遍历一次计数结果，收集所有 `num == max_num` 的 `id` 即可。

#### 代码（Python）  

```python
from collections import Counter
from typing import List, Tuple

def most_friends_optimal(requests: List[Tuple[int, int, str]]) -> Tuple[int, int]:
    """
    最优解：利用 Counter 一次统计所有用户出现次数
    :param requests: (requester_id, accepter_id, accept_date) 列表
    :return: (id, num)——拥有最多朋友的用户 id 以及朋友数量
    """
    # 把每条记录的两端都取出来，形成一个“一维”列表
    # 例如 [(1,2,_), (1,3,_)] -> [1,2,1,3]
    all_ids = [uid for r in requests for uid in (r[0], r[1])]
    # Counter 会把相同的 id 自动计数，等价于手写的 dict 计数
    cnt = Counter(all_ids)

    # 找出出现次数最多的 (id, num) 元组
    max_id, max_num = max(cnt.items(), key=lambda x: x[1])
    return max_id, max_num


def most_friends_all_max(requests: List[Tuple[int, int, str]]) -> List[Tuple[int, int]]:
    """
    Follow‑up：返回所有拥有相同最大朋友数的用户
    :return: [(id1, max), (id2, max), ...]（题目保证至少有一个）
    """
    all_ids = [uid for r in requests for uid in (r[0], r[1])]
    cnt = Counter(all_ids)

    max_num = max(cnt.values())                     # 最大朋友数
    # 收集所有朋友数等于 max_num 的用户
    result = [(uid, max_num) for uid, num in cnt.items() if num == max_num]
    return result
```

> **关键行中文注释**  
> - `all_ids = [uid for r in requests for uid in (r[0], r[1])]`：把每条记录的两个人“摊平”。  
> - `cnt = Counter(all_ids)`：交给专业的“计数员”。  
> - `max(cnt.items(), key=lambda x: x[1])`：一次遍历找出最大值。  

#### 复杂度  

- **时间复杂度**：`O(n)`（拉平列表 + Counter 计数 + 一次 max），仍然是线性，和暴力解一样快，只是常数更小。  
- **空间复杂度**：`O(m)`（存放所有不同用户的计数），与暴力解相同。  

---  

## 心得  

- **核心技巧**：把“双向关系”拆成两次单向计数，再用哈希表（字典 / Counter）快速统计出现次数。  
- **适用的题型**  
  1. **社交网络**：如 “统计每个人的粉丝数 / 关注数”。  
  2. **交易日志**：如 “统计每个商品的买卖次数”。  
  3. **日志分析**：如 “统计每个 IP 的访问次数”。  
- **一句话总结解题钥匙**：**把所有涉及计数的对象一次性展平，再交给哈希表或 Counter 完成 O(n) 计数**。  

---  

## 反思  

- **第一反应**：看到“朋友是双向的”，马上想到要为两个人各加 1，随后想到用字典记录计数。  
- **最容易踩的坑**  
  - **忘记双向计数**：只给 `requester_id` 加 1，会把朋友数减半。  
  - **忽略唯一性**：题目保证唯一最大值，但 Follow‑up 需要处理并列情况，必须遍历全部计数而不是只取 `max`。  
  - **数据类型**：`accept_date` 对本题没有影响，误把它当成关键字段会导致不必要的复杂度。  
- **下次遇到同类题**：第一步先 **把所有需要计数的对象展平成一个大列表**，再决定使用 **字典 / Counter** 进行一次遍历计数。这样既保证正确，又能直接得到最优的 O(n) 解法。