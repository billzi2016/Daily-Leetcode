# #1817. 查找用户活跃分钟数 / Finding the Users Active Minutes

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/finding-the-users-active-minutes/)

---

## 题目（英文原版）

**Description**

You are given the logs for users' actions on LeetCode, and an integer k. The logs are represented by a 2D integer array logs where each logs[i] = [IDi, timei] indicates that the user with IDi performed an action at the minute timei.
Multiple users can perform actions simultaneously, and a single user can perform multiple actions in the same minute.
The user active minutes (UAM) for a given user is defined as the number of unique minutes in which the user performed an action on LeetCode. A minute can only be counted once, even if multiple actions occur during it.
You are to calculate a 1-indexed array answer of size k such that, for each j (1 <= j <= k), answer[j] is the number of users whose UAM equals j.
Return the array answer as described above.

**Examples**

**Example 1:**

```
Input: logs = [[0,5],[1,2],[0,2],[0,5],[1,3]], k = 5
Output: [0,2,0,0,0]
Explanation:
The user with ID=0 performed actions at minutes 5, 2, and 5 again. Hence, they have a UAM of 2 (minute 5 is only counted once).
The user with ID=1 performed actions at minutes 2 and 3. Hence, they have a UAM of 2.
Since both users have a UAM of 2, answer[2] is 2, and the remaining answer[j] values are 0.
```

**Example 2:**

```
Input: logs = [[1,1],[2,2],[2,3]], k = 4
Output: [1,1,0,0]
Explanation:
The user with ID=1 performed a single action at minute 1. Hence, they have a UAM of 1.
The user with ID=2 performed actions at minutes 2 and 3. Hence, they have a UAM of 2.
There is one user with a UAM of 1 and one with a UAM of 2.
Hence, answer[1] = 1, answer[2] = 1, and the remaining values are 0.
```

**Constraints**

- 1 <= logs.length <= 104
- 0 <= IDi <= 109
- 1 <= timei <= 105
- k is in the range [The maximum UAM for a user, 105].

---

## 题目（中文翻译）

**描述**  
给定 LeetCode 上用户行为的日志（logs）以及一个整数 `k`。日志用二维整数数组 `logs` 表示，其中 `logs[i] = [ID_i, time_i]` 表示 ID 为 `ID_i` 的用户在第 `time_i` 分钟执行了一次操作。  
- 多个用户可以在同一时间执行操作。  
- 同一个用户在同一分钟内可以执行多次操作。

某个用户的 **用户活跃分钟数（UAM，User Active Minutes）** 定义为该用户在 LeetCode 上执行操作的 **不同分钟数**。即使在同一分钟内有多次操作，该分钟也只算一次。

请计算一个大小为 `k` 的 **1 索引** 数组 `answer`，使得对于每个 `j`（`1 ≤ j ≤ k`），`answer[j]` 为 **UAM 等于 `j` 的用户数**。返回上述数组 `answer`。

**示例 1**  
```text
Input: logs = [[0,5],[1,2],[0,2],[0,5],[1,3]], k = 5
Output: [0,2,0,0,0]
Explanation:
ID 为 0 的用户在第 5、2、5 分钟分别执行了操作。因此其 UAM 为 2（第 5 分钟只算一次）。
ID 为 1 的用户在第 2、3 分钟执行了操作，其 UAM 也为 2。
由于两位用户的 UAM 都是 2，`answer[2] = 2`，其余 `answer[j]` 均为 0。
```

**示例 2**  
```text
Input: logs = [[1,1],[2,2],[2,3]], k = 4
Output: [1,1,0,0]
Explanation:
ID 为 1 的用户仅在第 1 分钟执行一次操作，UAM 为 1。
ID 为 2 的用户在第 2、3 分钟各执行一次操作，UAM 为 2。
因此，UAM 为 1 的用户有 1 位，UAM 为 2 的用户也有 1 位。
`answer[1] = 1`，`answer[2] = 1`，其余值为 0。
```

**约束条件**  
- `1 ≤ logs.length ≤ 10^4`  
- `0 ≤ ID_i ≤ 10^9`  
- `1 ≤ time_i ≤ 10^5`  
- `k` 的取值范围为 `[最大用户的 UAM, 10^5]`   (即 `k` 不小于任意用户的 UAM，且不超过 `10^5`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有日志逐条扫描，记录每个用户在每一分钟出现了多少次**，最后再把每个用户的出现次数（去重后的唯一分钟数）统计出来。  

- **使用的数据结构**  
  - **字典（哈希表）**：把用户 ID 当作键（key），把该用户所有出现的分钟放进一个**列表**（value）。字典就像一本“大词典”，我们把用户的名字写进去，想查某个人的记录时，只要翻开对应的那一页就能看到。  
  - **列表**：用来暂时存放同一个用户的所有分钟（包括重复的），相当于把同一个人一天的所有活动时间都记在纸上。  

- **为什么正确**  
  1. 把每条日志都放进对应用户的列表里，保证了**没有遗漏**。  
  2. 对每个用户的列表去重（把重复的分钟删掉），得到的就是该用户的 **UAM**（Unique Active Minutes）。  
  3. 最后把所有用户的 UAM 计数放进答案数组即可。  

- **复杂度分析（大白话）**  
  - **时间复杂度**：我们遍历 `logs` 一次（`n` 条），每条日志做一次字典查找/插入（常数时间），然后对每个用户的列表去重需要遍历列表本身。最坏情况下所有日志都属于同一个用户，列表长度为 `n`，去重要遍历 `n` 次，所以总时间是 **O(n²)**。  
    - **O(n²) 是什么意思**？如果 `n=1000`，大约要做 1,000,000 次基本操作；如果 `n` 再翻一番到 2000，操作次数会变成 4,000,000，呈平方增长，速度会明显变慢。  
  - **空间复杂度**：我们保存了所有日志的拷贝（放进列表里），所以需要 **O(n)** 的额外空间。  

#### 代码（Python）

```python
def findingUsersActiveMinutes_bruteforce(logs, k):
    # 1. 把每条日志放进对应用户的列表里
    user_minutes = {}                     # dict: key = user ID, value = list of minutes
    for uid, minute in logs:              # 遍历每一条日志
        if uid not in user_minutes:
            user_minutes[uid] = []        # 第一次看到这个用户，创建空列表
        user_minutes[uid].append(minute) # 把出现的分钟记下来（可能有重复）

    # 2. 统计每个用户的唯一分钟数（UAM）
    answer = [0] * k                      # 题目要求 1-indexed，先全 0
    for minutes in user_minutes.values():
        unique_cnt = len(set(minutes))    # 把列表转成集合，自动去重，得到唯一分钟数
        if 1 <= unique_cnt <= k:          # 只统计在 1..k 范围内的
            answer[unique_cnt - 1] += 1   # 记得转成 0-index

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 主要瓶颈在把每个用户的列表去重（`set` 操作）时，需要遍历列表本身，最坏情况下所有日志属于同一个用户，导致二次遍历。  
- **空间复杂度**：`O(n)` —— 需要保存每条日志的分钟数（列表），以及最终的答案数组 `answer`（大小为 `k`，但 `k ≤ 10⁵`，相对 `n` 可视为常数）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“把同一个用户的所有分钟都存成一个列表再去重”** 是慢的根源。我们可以在 **记录的同时就去重**，这样就不必在后面再遍历一次列表。

**关键点**：

1. **用集合（set）直接保存每个用户的唯一分钟**。  
   - 集合的特性是“元素不重复”，所以每次把一个分钟加入集合时，若已经出现过，就自动被忽略。  
   - 这相当于在记录时就把“同一分钟的多次操作”合并成一次，省掉了后面的去重工作。  

2. **一次遍历完成所有统计**。  
   - 只需要遍历 `logs` 一遍，把 `(uid, minute)` 插入对应用户的集合中。  
   - 完成后，再遍历字典的值（每个用户的集合），直接取集合的大小就是该用户的 UAM。  

3. **把 UAM 计数写入答案数组**。  
   - 因为题目要求返回长度为 `k` 的 1-indexed 数组，直接在对应位置 `answer[uam-1]` 加一即可。

**类比**：  
想象你在图书馆为每位读者准备一本“借书记录本”。每次读者借书，你就在他的本子上写下借书的日期。**如果用普通纸记录**（列表），借完后还要把重复的日期挑出来；**如果直接用记号笔在本子上划叉**（集合），同一天再借就不再写，直接保持唯一记录，省时省力。

#### 代码（Python）

```python
def findingUsersActiveMinutes(logs, k):
    """
    最优解：使用 dict + set，一遍遍历即可得到每个用户的 UAM。
    """
    # 1. 用字典把每个用户的唯一分钟收集起来
    user_minutes = {}                     # key: user ID, value: set of unique minutes
    for uid, minute in logs:              # 只遍历一次 logs
        if uid not in user_minutes:
            user_minutes[uid] = set()     # 第一次出现，创建空集合
        user_minutes[uid].add(minute)    # 往集合里加 minute，自动去重

    # 2. 根据每个用户集合的大小，填充答案数组
    answer = [0] * k                      # 初始化全 0，长度为 k
    for minutes_set in user_minutes.values():
        uam = len(minutes_set)            # 集合的大小就是该用户的 UAM
        if 1 <= uam <= k:                 # 只统计在 1..k 范围内的
            answer[uam - 1] += 1          # 1-indexed -> 0-indexed

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次 `logs`，每次向集合插入的时间是 **均摊 O(1)**（哈希表的特性），随后遍历用户数 `m`（`m ≤ n`）来统计 UAM，整体仍是线性时间。  
  - 与暴力解的 `O(n²)` 相比，**速度提升了好几个数量级**，即使 `n` 达到 10⁴ 甚至更大也能轻松跑完。  

- **空间复杂度**：`O(n)` —— 最坏情况下每条日志的分钟都不重复，需要把所有分钟存进对应用户的集合中，总空间仍然是线性级别。不过相比暴力解，我们不再保存冗余的重复分钟，实际占用会更少。

---

## 心得

- **核心技巧**：**利用哈希表（字典）配合集合（set）在记录阶段直接去重**。  
- **适用的题型**  
  1. “统计每个元素出现的不同种类数”——例如 **统计每个字符出现的不同单词数**。  
  2. “按组分组后对每组做唯一计数”——例如 **每个用户的不同访问页面数**。  
  3. “需要在一次遍历中完成去重并计数”——如 **统计数组中不同子数组的长度**。  
- **一句话总结解题钥匙**：**“在收集信息的同时去重，而不是收集完再去重”。**

---

## 反思

- **第一反应**：看到“唯一分钟数”，立刻想到 **集合去重**，于是想到用 `dict[id] = set()` 来直接记录。  
- **最容易踩的坑**  
  - **忘记 1-indexed**：答案数组是从下标 1 开始，需要把 `uam` 减一后再存入 `answer`。  
  - **UAM 超出 k**：如果某个用户的唯一分钟数大于 `k`，题目说明 `k` 至少等于最大 UAM，但防御性写代码时仍需检查范围。  
  - **空日志或单用户多次同一分钟**：集合自然会处理这些特殊情况，但若使用列表，需要手动去重。  
- **下次遇到同类题的第一步**：**先思考能否在“收集阶段”直接用集合或哈希表消除重复**，把去重和计数合并为一次遍历。这样往往能直接得到最优解。