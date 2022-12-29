# #2070. 最美商品查询 / Most Beautiful Item for Each Query

> 难度：中等 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/most-beautiful-item-for-each-query/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array items where items[i] = [pricei, beautyi] denotes the price and beauty of an item respectively.
You are also given a 0-indexed integer array queries. For each queries[j], you want to determine the maximum beauty of an item whose price is less than or equal to queries[j]. If no such item exists, then the answer to this query is 0.
Return an array answer of the same length as queries where answer[j] is the answer to the jth query.

**Examples**

**Example 1:**

```
Input: items = [[1,2],[3,2],[2,4],[5,6],[3,5]], queries = [1,2,3,4,5,6]
Output: [2,4,5,5,6,6]
Explanation:
- For queries[0]=1, [1,2] is the only item which has price <= 1. Hence, the answer for this query is 2.
- For queries[1]=2, the items which can be considered are [1,2] and [2,4]. 
  The maximum beauty among them is 4.
- For queries[2]=3 and queries[3]=4, the items which can be considered are [1,2], [3,2], [2,4], and [3,5].
  The maximum beauty among them is 5.
- For queries[4]=5 and queries[5]=6, all items can be considered.
  Hence, the answer for them is the maximum beauty of all items, i.e., 6.
```

**Example 2:**

```
Input: items = [[1,2],[1,2],[1,3],[1,4]], queries = [1]
Output: [4]
Explanation: 
The price of every item is equal to 1, so we choose the item with the maximum beauty 4. 
Note that multiple items can have the same price and/or beauty.
```

**Example 3:**

```
Input: items = [[10,1000]], queries = [5]
Output: [0]
Explanation:
No item has a price less than or equal to 5, so no item can be chosen.
Hence, the answer to the query is 0.
```

**Constraints**

- 1 <= items.length, queries.length <= 105
- items[i].length == 2
- 1 <= pricei, beautyi, queries[j] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个二维整数数组 `items`，其中 `items[i] = [priceᵢ, beautyᵢ]` 分别表示第 *i* 件商品的价格（price）和美丽度（beauty）。  
另给定一个 **0-indexed** 整数数组 `queries`。对于每个 `queries[j]`，需要找出价格 **小于等于** `queries[j]` 的商品中，美丽度（beauty）最大的商品的美丽度。如果不存在满足条件的商品，则该查询的答案为 `0`。  

返回一个与 `queries` 等长的数组 `answer`，其中 `answer[j]` 为第 *j* 个查询的答案。

**示例**  

*示例 1*  
```
Input: items = [[1,2],[3,2],[2,4],[5,6],[3,5]], queries = [1,2,3,4,5,6]
Output: [2,4,5,5,6,6]
Explanation:
- 对于 queries[0]=1，只有商品 [1,2] 的价格 ≤ 1，故答案为 2。
- 对于 queries[1]=2，可考虑的商品有 [1,2] 和 [2,4]，其中最大美丽度为 4。
- 对于 queries[2]=3 和 queries[3]=4，可考虑的商品为 ...（此处省略其余过程）。
```

*示例 2*  
```
Input: items = [[1,2],[1,2],[1,3],[1,4]], queries = [1]
Output: [4]
Explanation:
所有商品的价格均为 1，故选择美丽度最大的商品，答案为 4。注意，多个商品可以拥有相同的价格和/或美丽度。
```

*示例 3*  
```
Input: items = [[10,1000]], queries = [5]
Output: [0]
Explanation:
没有商品的价格 ≤ 5，无法选取商品，答案为 0。
```

**约束条件**  
- `1 <= items.length, queries.length <= 10⁵`  
- `items[i].length == 2`  
- `1 <= priceᵢ, beautyᵢ, queries[j] <= 10⁹`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**对每一个查询** `queries[j]`，把 `items` 中所有 **价格 ≤ queries[j]** 的商品挑出来，找出它们的最大美观度 `beauty`。  
- **数据结构**：只需要遍历 `items`，不需要额外的结构。可以把 `items` 想象成超市里的一排商品，**遍历一次** 就像把所有商品都检查一遍，看有没有符合“价钱不超过预算”的要求。  
- **正确性**：因为我们把所有可能的商品都考虑到了，取最大美观度自然就是答案。  

#### 代码（Python）

```python
from typing import List

def maximumBeauty_bruteforce(items: List[List[int]], queries: List[int]) -> List[int]:
    ans = []
    # 对每一个查询逐个处理
    for q in queries:                     # q = 当前预算
        best = 0                           # 记录当前预算下的最大美观度，默认 0
        for price, beauty in items:        # 遍历所有商品
            if price <= q:                 # 只看价钱不超过预算的商品
                if beauty > best:          # 找到更大的美观度就更新
                    best = beauty
        ans.append(best)                   # 把答案放进结果数组
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`，其中 `m = len(queries)`，`n = len(items)`。  
  直观解释：如果查询有 10 万条，商品也有 10 万件，那么最坏情况下需要 **一亿次** 比较，计算机会非常慢。  
- **空间复杂度**：`O(1)`（不计答案数组）。只用了常数级别的额外变量 `best`、`q`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个查询都要重新遍历全部商品**。实际上，**查询之间是有联系的**：如果我们已经知道预算 `5` 能买到的最大美观度是 `7`，那么预算 `6` 的答案一定 **不小于** `7`（因为可以把预算 `5` 能买的商品也买了）。  
利用这一点，我们可以把商品和查询都 **按价格从小到大排序**，然后一次线性扫描即可得到所有答案。

具体步骤如下：

1. **按价格升序排序商品** `items`。  
   - 同一个价格可能有多件商品，只保留**最高美观度**即可（后面会用前缀最大处理）。  
2. **构造前缀最大数组** `max_beauty_up_to[i]`，表示**价格 ≤ items[i][0]** 时的最大美观度。  
   - 这一步类似“跑步时记录最高分”，遍历一次即可。  
3. **把查询也排序**，但要记住原来的下标，以便最后恢复顺序。  
4. **双指针扫描**：  
   - 用指针 `i` 遍历排序后的商品列表，指针 `j` 遍历排序后的查询。  
   - 对每个查询 `q`，把 `i` 向前推进，直到 `items[i][0] > q`（即商品价格已经超过预算）。此时 `i-1` 就是**所有价钱 ≤ q 的商品**的最后一个位置，答案就是 `max_beauty_up_to[i-1]`（如果 `i==0` 则答案为 `0`）。  
5. 把答案写回原始查询下标位置，返回结果。

> **类比**：想象你在图书馆排队借书，**排好序的书架**（商品）从左到右依次放，**排好序的读者**（查询）从左到右来。每当一个读者的预算够借左边的书时，你把指针往右移动，记录下当前能借到的最高评分的书。这样每本书只会被检查一次，效率大幅提升。

#### 代码（Python）

```python
from typing import List

def maximumBeauty(items: List[List[int]], queries: List[int]) -> List[int]:
    # 1️⃣ 先把商品按价格升序排列
    items.sort(key=lambda x: x[0])          # x[0] = price

    # 2️⃣ 构造前缀最大美观度数组
    #   max_beauty[i] 表示 price <= items[i][0] 时的最大 beauty
    max_beauty = []
    cur_max = 0
    for price, beauty in items:
        cur_max = max(cur_max, beauty)      # 维护到目前为止的最大美观度
        max_beauty.append(cur_max)          # 对应位置保存

    # 3️⃣ 把查询排序，同时记住原始下标
    #   queries_with_idx = [(budget, original_index), ...]
    queries_with_idx = sorted(
        [(q, idx) for idx, q in enumerate(queries)],
        key=lambda x: x[0]
    )

    # 4️⃣ 双指针扫描
    ans = [0] * len(queries)                # 最终答案数组
    i = 0                                    # 商品指针
    n = len(items)

    for budget, original_idx in queries_with_idx:
        # 把商品指针向右移动，直到 price > budget
        while i < n and items[i][0] <= budget:
            i += 1
        # 此时 i 是第一个 price > budget 的位置，i-1 是符合条件的最后一个
        if i == 0:                           # 没有任何商品价格 ≤ budget
            ans[original_idx] = 0
        else:
            ans[original_idx] = max_beauty[i-1]

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n + m log m)`  
  - `n = len(items)`，`m = len(queries)`。  
  - 解释：我们分别对商品和查询进行一次排序（各自 `log` 级别），随后只做线性扫描 `O(n + m)`。整体比暴力的 `O(n·m)` 快很多。  
- **空间复杂度**：`O(n + m)`  
  - 需要存储排序后的商品列表、前缀最大数组以及带下标的查询列表。  
  - 与输入规模同阶，属于线性额外空间。

---

## 心得

- **核心技巧**：**先排序 + 前缀最大 + 双指针**。  
  这是一种常见的“**离线查询**”思路：把所有查询先收集起来，按照某个属性（这里是预算）排序后一次性处理，避免重复工作。  
- **适用的题型**  
  1. “区间最大/最小查询” 类似 **“查询小于等于某值的最大/最小”**（如 LeetCode 1847. Closest Room）。  
  2. “每个查询对应前缀/后缀统计” 如 **“每个查询求前缀和的最大值”**（Prefix Sum + offline）。  
  3. “两组数据的配对统计” 如 **“两个数组的配对满足某种不等式”**（Two‑Pointer on sorted arrays）。  
- **一句话总结**：**把查询和数据一起排序，利用单调性一次扫完，答案自然随指针移动得到**。

---

## 反思

- **第一反应**：看到“对每个查询找 price ≤ q 的最大 beauty”，本能想到**遍历所有商品**。这导致了 `O(n·m)` 的暴力思路。  
- **最容易踩的坑**  
  1. **同价商品的处理**：如果不取最大 beauty，前缀最大数组会被较小的 beauty 覆盖，导致错误答案。  
  2. **边界情况**：查询的预算比所有商品都小，需要返回 `0`；代码中 `i == 0` 的判断不能忘。  
  3. **整数范围**：价格、beauty、查询值都可能高达 `10^9`，不能用数组直接按值索引（会爆内存），只能靠排序。  
- **下次遇到同类题**：第一步先**思考是否可以把所有查询离线**，把查询和数据一起排序，然后用**单调指针/前缀信息**一次遍历得到答案。这样常能把指数级的暴力降到 `O(N log N)`。