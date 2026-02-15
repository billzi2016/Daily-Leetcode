# #3527. 找出最常见的回答 / Find the Most Common Response

> 难度：中等 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/find-the-most-common-response/)

---

## 题目（英文原版）

**Description**

You are given a 2D string array responses where each responses[i] is an array of strings representing survey responses from the ith day.
Return the most common response across all days after removing duplicate responses within each responses[i]. If there is a tie, return the lexicographically smallest response.

**Examples**

**Example 1:**

```
Input: responses = [["good","ok","good","ok"],["ok","bad","good","ok","ok"],["good"],["bad"]]
Output: "good"
Explanation:
```

**Example 2:**

```
Input: responses = [["good","ok","good"],["ok","bad"],["bad","notsure"],["great","good"]]
Output: "bad"
Explanation:
```

**Constraints**

- 1 <= responses.length <= 1000
- 1 <= responses[i].length <= 1000
- 1 <= responses[i][j].length <= 10
- responses[i][j] consists of only lowercase English letters

---

## 题目（中文翻译）

**描述：**  
给定一个二维字符串数组 (2D string array) `responses`，其中 `responses[i]` 是一个字符串数组，表示第 `i` 天的调查回答。  
在对每个 `responses[i]` 内部先去除重复的回答后，返回所有天中出现次数最多的回答。如果出现次数相同，则返回字典序 (lexicographically) 最小的回答。

**示例 1：**  
输入: `responses = [["good","ok","good","ok"],["ok","bad","good","ok","ok"],["good"],["bad"]]`  
输出: `"good"`  
解释：

**示例 2：**  
输入: `responses = [["good","ok","good"],["ok","bad"],["bad","notsure"],["great","good"]]`  
输出: `"bad"`  
解释：

**约束条件：**  
- `1 <= responses.length <= 1000`  
- `1 <= responses[i].length <= 1000`  
- `1 <= responses[i][j].length <= 10`  
- `responses[i][j]` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把所有天的答案直接拼成一个大列表，然后把**出现次数最多的**答案挑出来。  
但是题目要求 **“每一天内部的重复要先去掉”**，也就是说同一天里出现多次的同一个答案只能算 **一次**。  

如果不事先去重，直接对整个大列表计数，就会把同一天的重复算进去，结果会不正确。  
一种“暴力”做法是：遍历每一天的每个答案，在全局计数之前，先检查这一天里之前是否已经统计过这个答案。  
我们可以用一个 **列表** 来保存已经统计过的答案（因为是暴力解，不追求效率），每次判断都用 `in` 线性搜索。  

- **数据结构**：  
  - `global_counts`：字典（哈希表），key 是答案字符串，value 是出现的天数。  
  - `seen_today`：列表，用来记录当前天已经统计过的答案，类似“手写的字典”。  

- **正确性**：  
  - 对每一天，只有第一次遇到的答案会进入 `global_counts`，后面的重复因为在 `seen_today` 中被发现而被跳过，符合题意。  
  - 最后遍历 `global_counts`，找出出现次数最多的答案；若出现次数相同，取字典序最小的，即可得到答案。  

- **复杂度分析（大白话）**：  
  - 假设总共有 `N` 条答案（所有天的答案数量之和）。  
  - 对每条答案我们都要在 `seen_today` 里线性查找，最坏情况下 `seen_today` 长度会和当天的答案数成正比。于是总的时间大约是 **O(N²)**（想象每条答案都要检查前面所有答案）。  
  - 额外空间只用了两个字典/列表，规模和不同答案的数量 `U` 成正比，记作 **O(U)**。  

#### 代码（Python）  

```python
from typing import List

def most_common_response_bruteforce(responses: List[List[str]]) -> str:
    # 全局计数：每个答案出现了多少天
    global_counts = {}          # 哈希表，key 是答案，value 是出现的天数

    # 遍历每一天
    for day in responses:
        # 用列表记录今天已经统计过的答案（暴力做法）
        seen_today = []         # 类似手写的“已经出现过的集合”

        # 遍历今天的每个答案
        for ans in day:
            # 如果今天已经统计过了，就跳过（避免同一天重复计数）
            if ans in seen_today:          # 线性搜索，最坏 O(len(seen_today))
                continue

            # 标记今天已经看到过这个答案
            seen_today.append(ans)

            # 更新全局计数
            if ans in global_counts:
                global_counts[ans] += 1
            else:
                global_counts[ans] = 1

    # 在全局计数里找出现次数最多的答案
    # 如果出现次数相同，取字典序最小的（Python 的 min 会比较字符串的字典序）
    best = None
    best_cnt = -1
    for ans, cnt in global_counts.items():
        if cnt > best_cnt or (cnt == best_cnt and ans < best):
            best = ans
            best_cnt = cnt

    return best
```

#### 复杂度  

- **时间复杂度**：`O(N²)`  
  - `N` 是所有答案的总数。每次检查是否已经出现过都要遍历 `seen_today`，最坏情况下会导致二次遍历。  
- **空间复杂度**：`O(U)`  
  - `U` 为不同答案的数量。我们用一个字典保存每个答案出现的天数，还要在每一天保存一个 `seen_today` 列表，最多也只会存放该天的不同答案。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 出在每天用列表线性搜索已经出现的答案。  
如果我们换成 **哈希表（字典）或集合** 来保存当天已经出现的答案，查询是否出现过的时间可以降到 **O(1)**（常数时间），这样整体就只需要遍历所有答案一次。

**优化步骤**  

1. **对每一天去重**  
   - 使用 `set(day)` 把当天的答案转成集合，自动去掉重复。集合的工作原理类似“字典”，可以在常数时间判断元素是否在集合里。  

2. **全局计数**  
   - 用一个全局字典 `cnt` 记录每个答案出现了多少天。遍历每一天的集合，把每个答案的计数加一。  

3. **找出最大计数并处理平局**  
   - 一遍遍历 `cnt`，维护当前的最佳答案 `best` 与出现次数 `best_cnt`。  
   - 当出现次数相等时，用 `ans < best`（字符串的字典序比较）来挑选字典序更小的答案。  

**为什么这样是最优的？**  

- 每个答案只会被访问 **一次**（加入对应天的集合时），再加一次全局计数更新。整体时间是 **O(N)**，线性随输入规模增长。  
- 只用了两个哈希表（集合和字典），空间与不同答案的数量 `U` 成正比，记作 **O(U)**。  

**关键概念解释**  

- **哈希表 / 字典**：想象成一本“查字典”，我们把答案当作单词，字典会直接告诉我们这个单词对应的页码（这里是出现的天数），查找速度非常快，几乎是瞬间（常数时间）。  
- **集合（set）**：类似字典，只是只存“单词”，不记录对应的值。把一堆答案放进去，自动会把重复的单词删掉，就像把装有重复卡片的盒子倒进一个只能放唯一卡片的盒子。  

#### 代码（Python）  

```python
from typing import List

def most_common_response(responses: List[List[str]]) -> str:
    """
    最优解：利用集合去重 + 哈希表计数
    时间复杂度 O(N)  空间复杂度 O(U)
    """
    # 全局计数字典：key 为答案，value 为出现的天数
    cnt = {}

    # 逐天处理
    for day in responses:
        # set 会自动去掉同一天内部的重复
        unique_today = set(day)          # O(len(day))

        # 把今天出现的每个不同答案计数加一
        for ans in unique_today:         # 每个答案只遍历一次
            cnt[ans] = cnt.get(ans, 0) + 1

    # 在计数字典里找出现次数最多且字典序最小的答案
    best = None
    best_cnt = -1
    for ans, c in cnt.items():
        if c > best_cnt or (c == best_cnt and (best is None or ans < best)):
            best = ans
            best_cnt = c

    return best
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - `N` 为所有答案的总数。每个答案先放进集合去重（线性），再在全局字典里更新计数，都是一次遍历。  
- **空间复杂度**：`O(U)`  
  - `U` 为不同答案的数量。我们维护一个全局计数字典以及每一天的临时集合，最多占用 `U` 条记录的空间。  

---  

## 心得  

- **核心技巧**：利用 **集合去重** + **哈希表计数**，在 O(1) 时间内判断是否出现过以及快速累计次数。  
- **适用的题型**：  
  1. “出现次数最多的元素”类题目（如统计数组中出现频率最高的数字）。  
  2. “去重后再统计”类题目（如统计不同用户的登录天数）。  
  3. “字典序 tie‑break”类题目（需要在出现次数相同的情况下取最小的字符串）。  
- **一句话总结**：**“先用集合把同一天的重复抹掉，再用哈希表一次遍历统计出现天数”。**  

## 反思  

- **第一反应**：看到“每一天内部去重”，立刻想到用 `set`；看到“出现次数最多”，想到计数哈希表。  
- **最容易踩的坑**：  
  - 忘记在同一天内部去重，导致同一天的重复被多次计数。  
  - 平局时没有按照字典序挑选最小的答案，直接返回第一个会出错。  
  - 边界情况：只有一条答案或所有答案都不重复，需要确保代码仍能返回正确结果。  
- **下次类似题的第一步**：  
  - 明确“去重的粒度”（是整体还是局部），先用集合/字典把重复剔除，再决定计数或其他操作。