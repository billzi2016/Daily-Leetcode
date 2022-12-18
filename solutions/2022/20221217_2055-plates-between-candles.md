# #2055. 烛之间的盘子 / Plates Between Candles

> 难度：中等 · 标签：Array、String、Binary Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/plates-between-candles/)

---

## 题目（英文原版）

**Description**

There is a long table with a line of plates and candles arranged on top of it. You are given a 0-indexed string s consisting of characters '*' and '|' only, where a '*' represents a plate and a '|' represents a candle.
You are also given a 0-indexed 2D integer array queries where queries[i] = [lefti, righti] denotes the substring s[lefti...righti] (inclusive). For each query, you need to find the number of plates between candles that are in the substring. A plate is considered between candles if there is at least one candle to its left and at least one candle to its right in the substring.
Return an integer array answer where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: s = "**|**|***|", queries = [[2,5],[5,9]]
Output: [2,3]
Explanation:
- queries[0] has two plates between candles.
- queries[1] has three plates between candles.
```

**Example 2:**

```
Input: s = "***|**|*****|**||**|*", queries = [[1,17],[4,5],[14,17],[5,11],[15,16]]
Output: [9,0,0,0,0]
Explanation:
- queries[0] has nine plates between candles.
- The other queries have zero plates between candles.
```

**Constraints**

- 3 <= s.length <= 105
- s consists of '*' and '|' characters.
- 1 <= queries.length <= 105
- queries[i].length == 2
- 0 <= lefti <= righti < s.length

---

## 题目（中文翻译）

**题目描述**

给定一个仅由字符 `'*'`（表示盘子）和 `'|'`（表示烛）组成的 **0 起始索引** 字符串 `s`。  
同时给定一个 **0 起始索引** 的二维整数数组 `queries`，其中 `queries[i] = [left_i, right_i]` 表示子串 `s[left_i … right_i]`（闭区间）。  

对于每个查询，需要统计该子串中 **位于两根烛之间的盘子** 的数量。若一个盘子在子串内左侧至少有一根烛且右侧至少有一根烛，则该盘子视为“位于两根烛之间”。  

返回一个整数数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的答案。

---

## 示例

### 示例 1
**输入**  
```text
s = "**|**|***|"
queries = [[2,5],[5,9]]
```
**输出**  
```text
[2,3]
```
**解释**  
- `queries[0]` 对应的子串在两根烛之间有 **2** 个盘子。  
- `queries[1]` 对应的子串在两根烛之间有 **3** 个盘子。

### 示例 2
**输入**  
```text
s = "***|**|*****|**||**|*"
queries = [[1,17],[4,5],[14,17],[5,11],[15,16]]
```
**输出**  
```text
[9,0,0,0,0]
```
**解释**  
- `queries[0]` 对应的子串在两根烛之间有 **9** 个盘子。  
- 其余查询对应的子串中没有任何位于两根烛之间的盘子，答案均为 **0**。

---

## 约束条件

- `3 <= s.length <= 10^5`
- `s` 仅由 `'*'` 和 `'|'` 组成
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= left_i <= right_i < s.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个查询** `[left, right]`，直接在子串 `s[left … right]` 里逐个检查字符。  
- 先找子串中最左边的蜡烛 `|`（记作 `first`），再找最右边的蜡烛 `|`（记作 `last`）。  
- 如果 `first` 与 `last` 都找到了且 `first < last`，则在区间 `[first, last]` 之间的所有 `*` 都算作“被两根蜡烛夹住的盘子”。  
- 直接遍历 `[first, last]`，统计 `*` 的个数，就是该查询的答案。

> **类比**：把蜡烛想象成书的章节标题，盘子是正文。我们只关心在两个标题之间的正文。所以先定位左右标题，再数正文。

该方法必然是 **正确** 的，因为我们严格按照题目定义：盘子必须左、右都有蜡烛，且这两根蜡烛必须在查询区间内。

#### 代码（Python）

```python
def platesBetweenCandles_brute(s: str, queries: list[list[int]]) -> list[int]:
    ans = []
    for left, right in queries:                     # 逐个查询
        # 1️⃣ 找左边第一个蜡烛
        first = -1
        for i in range(left, right + 1):
            if s[i] == '|':
                first = i
                break

        # 2️⃣ 找右边最后一个蜡烛
        last = -1
        for i in range(right, left - 1, -1):
            if s[i] == '|':
                last = i
                break

        # 3️⃣ 统计两根蜡烛之间的盘子
        if first != -1 and last != -1 and first < last:
            cnt = 0
            for i in range(first, last + 1):
                if s[i] == '*':
                    cnt += 1
            ans.append(cnt)
        else:                     # 区间内没有形成“夹住”的情况
            ans.append(0)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(Q * N)`（`Q` 为查询数，`N` 为字符串长度）  
  - 对每个查询我们最坏要遍历一次完整的子串 `s[left … right]`，这在最坏情况下是 `O(N)`，所以总体是 `O(Q·N)`。  
  - 大白话：如果有 10 万条查询，字符串也有 10 万长，直接跑会是 **10⁹ 次**遍历，根本跑不完。

- **空间复杂度**：`O(1)`（只用了常数个临时变量）  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每个查询都要线性扫描**。我们需要把“找左/右蜡烛”和“统计区间内盘子数”这两件事 **预处理**，让每个查询只用 **O(1)** 或 **O(log N)** 的时间即可完成。

关键点有两步：

1. **预先知道每个位置左侧最近的蜡烛**（记作 `left_candle[i]`），以及**右侧最近的蜡烛**（记作 `right_candle[i]`）。  
   - 这相当于对字符串做两遍扫描：从左到右记录最近出现的 `|`，从右到左同理。  
   - 类比：在一本书里，你提前把每一页的最近章节标题记下来，查找章节标题就不需要再翻书了。

2. **前缀和**（Prefix Sum）帮助我们在 **O(1)** 时间内求出任意区间内 `*` 的数量。  
   - `pref[i]` 表示字符串前 `i` 个字符（下标 `[0, i)`）中 `*` 的总数。  
   - 区间 `[l, r]` 内的盘子数 = `pref[r+1] - pref[l]`。

有了这两组信息，单个查询的处理流程如下：

- 用 `right_candle[left]` 找到左端最近的蜡烛（即子串左侧第一个 `|`）。  
- 用 `left_candle[right]` 找到右端最近的蜡烛（即子串右侧最后一个 `|`）。  
- 若两根蜡烛存在且 `first < last`，答案 = `pref[last] - pref[first+1]`（`first+1` 到 `last-1` 之间的 `*` 数）。否则答案为 0。

整个预处理只需要 **两次线性扫描**，时间 `O(N)`，空间 `O(N)`（存三个长度为 `N` 的数组）。每个查询只做常数次数组访问 → `O(1)`。

> **为什么二分查找也可以？**  
> 如果只存所有蜡烛的下标列表，用二分查找定位左/右蜡烛也能做到 `O(log N)`。但直接用最近蜡烛数组更简单、常数更小，故这里采用数组方式。

#### 代码（Python）

```python
def platesBetweenCandles(s: str, queries: list[list[int]]) -> list[int]:
    n = len(s)

    # 1️⃣ 前缀和：pref[i] = s[:i] 中 '*' 的数量（i 从 0 开始，pref[0] = 0）
    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (1 if ch == '*' else 0)

    # 2️⃣ left_candle[i] = i 左侧（含 i）最近的蜡烛下标，若不存在为 -1
    left_candle = [-1] * n
    last = -1
    for i in range(n):
        if s[i] == '|':
            last = i
        left_candle[i] = last

    # 3️⃣ right_candle[i] = i 右侧（含 i）最近的蜡烛下标，若不存在为 -1
    right_candle = [-1] * n
    nxt = -1
    for i in range(n - 1, -1, -1):
        if s[i] == '|':
            nxt = i
        right_candle[i] = nxt

    # 4️⃣ 处理每个查询
    ans = []
    for left, right in queries:
        # 子串左侧最近的蜡烛
        first = right_candle[left]
        # 子串右侧最近的蜡烛
        last = left_candle[right]

        # 必须保证两根蜡烛都存在且 first < last
        if first != -1 and last != -1 and first < last:
            # pref[last] 包含 last 位置之前的所有 '*'
            # pref[first + 1] 包含 first 位置之前的所有 '*'
            cnt = pref[last] - pref[first + 1]
            ans.append(cnt)
        else:
            ans.append(0)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N + Q)`  
  - 预处理遍历字符串三遍 → `O(N)`。  
  - 每个查询只做几次数组查找 → `O(1)`，累计 `O(Q)`。  
  - 与暴力解相比，时间从 `O(N·Q)` 降到了线性，能够轻松处理 `10⁵` 规模的数据。

- **空间复杂度**：`O(N)`  
  - 需要三个长度为 `N` 的数组（前缀和、左侧最近蜡烛、右侧最近蜡烛）。  
  - 对于 `N = 10⁵`，这只占几百 KB，完全可以接受。

---

## 心得  

- **核心技巧**：**前缀和 + 最近位置数组**（或二分查找）。  
- **适用的题型**：  
  1. “区间内满足某种条件的元素个数”——如 `Number of Items Between Two Objects`、`Number of Subarrays with Bounded Maximum`（需要前缀计数）。  
  2. “在区间内定位最近的某类元素”——如 `Find the Closest Stone`、`Maximum Number of Words Found in Sentences`（需要左右最近位置）。  
- **一句话总结**：先把“左/右最近的蜡烛”和“区间内盘子数量”都用一次遍历记下来，查询时只要看表格，**O(1) 即可得到答案**。

---

## 反思  

- **拿到题目第一反应**：直接遍历每个查询的子串，找左/右蜡烛再计数——也就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略子串两端没有蜡烛的情况，导致负数或错误计数。  
  - 前缀和的下标容易写错（是左闭右开区间，需要 `pref[last] - pref[first+1]`）。  
  - 大数据时忘记时间复杂度，导致超时。  
- **下次遇到同类题**：第一步先思考 **“能否把区间查询转化为数组查表？”**，尤其是是否可以利用 **前缀和** 或 **最近位置** 这类一次预处理即可复用的信息。这样往往能把原本 `O(N·Q)` 的暴力降到 `O(N+Q)`。