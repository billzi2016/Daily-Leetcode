# #2343. 查询第 K 小的修剪数字 / Query Kth Smallest Trimmed Number

> 难度：中等 · 标签：Array、String、Divide and Conquer、Sorting、Heap (Priority Queue)、Radix Sort、Quickselect · [LeetCode 链接](https://leetcode.com/problems/query-kth-smallest-trimmed-number/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings nums, where each string is of equal length and consists of only digits.
You are also given a 0-indexed 2D integer array queries where queries[i] = [ki, trimi]. For each queries[i], you need to:
Return an array answer of the same length as queries, where answer[i] is the answer to the ith query.
Note:
Follow up: Could you use the Radix Sort Algorithm to solve this problem? What will be the complexity of that solution?

**Examples**

**Example 1:**

```
Input: nums = ["102","473","251","814"], queries = [[1,1],[2,3],[4,2],[1,2]]
Output: [2,2,1,0]
Explanation:
1. After trimming to the last digit, nums = ["2","3","1","4"]. The smallest number is 1 at index 2.
2. Trimmed to the last 3 digits, nums is unchanged. The 2nd smallest number is 251 at index 2.
3. Trimmed to the last 2 digits, nums = ["02","73","51","14"]. The 4th smallest number is 73.
4. Trimmed to the last 2 digits, the smallest number is 2 at index 0.
   Note that the trimmed number "02" is evaluated as 2.
```

**Example 2:**

```
Input: nums = ["24","37","96","04"], queries = [[2,1],[2,2]]
Output: [3,0]
Explanation:
1. Trimmed to the last digit, nums = ["4","7","6","4"]. The 2nd smallest number is 4 at index 3.
   There are two occurrences of 4, but the one at index 0 is considered smaller than the one at index 3.
2. Trimmed to the last 2 digits, nums is unchanged. The 2nd smallest number is 24.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i].length <= 100
- nums[i] consists of only digits.
- All nums[i].length are equal.
- 1 <= queries.length <= 100
- queries[i].length == 2
- 1 <= ki <= nums.length
- 1 <= trimi <= nums[i].length

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串数组 `nums`，其中每个字符串长度相同且仅由数字组成。  
同时给定一个下标从 **0** 开始的二维整数数组 `queries`，其中 `queries[i] = [k_i, trim_i]`。对于每个 `queries[i]`，需要：

- 将每个 `nums[j]` **修剪（trim）** 成仅保留其最后 `trim_i` 位的子串（如果 `trim_i` 等于字符串长度，则不发生变化）。
- 在修剪后的结果中，找出第 `k_i` 小的数字（**第 K 小**），若出现相同的数字，则下标更小的元素视为更小。
- 返回一个数组 `answer`，其长度与 `queries` 相同，`answer[i]` 为第 `i` 个查询的答案（即对应数字在原数组 `nums` 中的下标）。

**示例 1**

> **输入**  
> `nums = ["102","473","251","814"]`  
> `queries = [[1,1],[2,3],[4,2],[1,2]]`  
> **输出**  
> `[2,2,1,0]`  
> **解释**  
> 1. 修剪至最后 1 位后，`nums` 变为 `["2","3","1","4"]`。最小的数字是 `1`，其下标为 **2**。  
> 2. 修剪至最后 3 位后，`nums` 未改变。第 2 小的数字是 `251`，下标为 **2**。  
> 3. 修剪至最后 2 位后，`nums` 变为 `["02","73","51","14"]`。第 4 小的数字是 `73`，下标为 **1**。  
> 4. （后续步骤略）

**示例 2**

> **输入**  
> `nums = ["24","37","96","04"]`  
> `queries = [[2,1],[2,2]]`  
> **输出**  
> `[3,0]`  
> **解释**  
> 1. 修剪至最后 1 位后，`nums` 变为 `["4","7","6","4"]`。第 2 小的数字是 `4`，出现两次，下标更小的 **0** 视为更小，但这里第 2 小对应的是下标 **3** 的 `4`。  
> 2. 修剪至最后 2 位后，`nums` 未改变。第 2 小的数字是 `24`，下标为 **0**。

**约束条件**

- `1 <= nums.length <= 100`
- `1 <= nums[i].length <= 100`
- `nums[i]` 只包含数字字符
- 所有 `nums[i]` 的长度相等
- `1 <= queries.length <= 100`
- `queries[i].length == 2`
- `1 <= k_i <= nums.length`
- `1 <= trim_i <= nums[i].length`

**进阶**  
是否可以使用基数排序（Radix Sort）来解决此问题？该方案的时间复杂度和空间复杂度各是多少？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法是**把每一次查询都单独处理**：

1. 对于查询 `[k, trim]`，把所有字符串只保留最后 `trim` 位（相当于把数字“截短”），得到一个新的数组 `trimmed`。  
   - 这里的 **截短** 可以想象成把一本书的每一页只留下右下角的 `trim` 行文字。  
2. 把 `trimmed` 按**数值大小**排序。如果数值相同，**原下标更小的算在前面**（因为题目要求“相同数值时下标小的更小”）。这一步就像把一堆名字按字典序排好，但如果名字相同，还要看它们在原来名单里的位置。  
3. 排好序后，第 `k` 小的元素对应的原下标就是答案。

> 为什么这样一定对？因为题目本身就要求“在截短后的数组里找第 k 小”。我们完整地模拟了这个过程，所以答案必然正确。

**时间/空间复杂度**  
- 对每个查询我们都要遍历 `nums` 生成 `trimmed`（`O(n)`），再排序（`O(n log n)`），所以单次查询是 `O(n log n)`。  
- 有 `q` 条查询，总体时间是 `O(q·n log n)`。  
- 额外空间主要是保存 `trimmed` 和排序时的临时数组，都是 `O(n)`。

> 大白话解释：  
> - `O(n log n)` 可以理解为“先看每个元素一次（`n`），然后再把它们排队（`log n` 次比较）”。  
> - `O(q·n log n)` 就是把这件事重复 `q` 次。

#### 代码（Python）

```python
from typing import List

def smallestTrimmedNumbers(nums: List[str], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    ans = []

    for k, trim in queries:                     # 逐个处理查询
        # 1. 生成截短后的字符串，同时记住原下标
        trimmed = []
        for idx, s in enumerate(nums):
            # 只保留最后 trim 位，前面的直接丢掉
            trimmed.append((s[-trim:], idx))    # (截短后字符串, 原下标)

        # 2. 按数值大小排序；若数值相同则按原下标升序（Python 默认元组比较满足这个需求）
        trimmed.sort(key=lambda x: (x[0], x[1]))

        # 3. 第 k 小对应的原下标即为答案（k 是 1‑based）
        ans.append(trimmed[k - 1][1])

    return ans
```

#### 复杂度

- **时间复杂度**：`O(q·n log n)`  
  - `q` 为查询数量，`n` 为数组长度。  
  - 这里的 `log n` 来自每次对 `n` 条记录的排序。

- **空间复杂度**：`O(n)`  
  - 只需要额外存放一次 `trimmed` 列表，大小随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次查询都要重新排序。其实**同一种截短长度**会被多次使用，我们完全可以把相同 `trim` 的结果**缓存**下来，只排序一次。

**步骤概览**：

1. **收集所有出现过的 `trim` 值**。因为 `trim` 的取值范围是 `1 … L`（`L` 为数字字符串的长度），最多只有 `L ≤ 100` 种可能。  
2. 对每一种 `trim`，**一次性生成并排序**对应的 `(截短后字符串, 原下标)` 列表，保存到字典 `cache[trim]`。这一步相当于“预处理”。  
   - 排序时仍然使用 `(value, index)` 的元组，保证数值相同的情况下下标小的排在前面。  
3. 处理查询时，直接从 `cache` 里取出已经排好序的列表，返回第 `k` 小的原下标即可。  
   - 这样每条查询只需要 `O(1)` 的时间（取列表元素），整体时间只受预处理影响。

**进一步优化：使用基数排序（Radix Sort）**  

因为所有字符串只包含数字且长度相同，我们可以对每个 `trim` 采用**基数排序**来实现 `O(L·n)` 的线性时间排序（不需要比较）。基数排序的核心思想：

- 从最低位（最右边）开始，使用 **计数排序** 把数字按该位的 0‑9 分桶，保持相对顺序不变（即 **稳定**）。  
- 重复 `trim` 次后，整体就排好序了。  

基数排序的好处是**不依赖比较**，时间完全是 `O(trim·n)`，在本题的约束下非常快。

> 类比：把一堆不同颜色的球按颜色编号从 0 到 9 分到 10 个盒子里，先按最右边的颜色编号分，再按左边的，最后盒子里顺序就是从小到大。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def smallestTrimmedNumbers_opt(nums: List[str], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    L = len(nums[0])                     # 所有字符串等长
    # 1. 收集所有需要的 trim 长度
    trims = {trim for _, trim in queries}

    # 2. 为每个 trim 预处理排序结果（这里使用普通排序，代码更简洁；若想更快可改为基数排序）
    cache = {}                           # trim -> 已排好序的 (value, idx) 列表
    for t in trims:
        lst = [(s[-t:], i) for i, s in enumerate(nums)]  # 生成 (截短后, 原下标)
        lst.sort(key=lambda x: (x[0], x[1]))             # 按值、下标排序
        cache[t] = lst

    # 3. 直接回答查询
    ans = []
    for k, t in queries:
        ans.append(cache[t][k - 1][1])   # 第 k 小的原下标
    return ans
```

> 如果想使用基数排序，只需要把 `lst.sort(...)` 替换成下面的 `radix_sort(lst, t)`，实现细节已在注释中给出。

**基数排序实现（可选）**

```python
def radix_sort(arr: List[tuple], trim: int) -> List[tuple]:
    """基数排序，仅对字符串的后 trim 位进行排序，保持下标的稳定性"""
    for pos in range(trim - 1, -1, -1):          # 从最低位到最高位
        # 计数排序的 10 个桶（0-9）
        buckets = [[] for _ in range(10)]
        for val, idx in arr:
            digit = ord(val[pos]) - ord('0')    # 取当前位的数字
            buckets[digit].append((val, idx))
        # 合并桶，保持原有顺序（稳定）
        arr = [pair for bucket in buckets for pair in bucket]
    return arr
```

将 `lst = radix_sort(lst, t)` 替换原来的 `sort` 即可得到 **线性时间** 的预处理。

#### 复杂度

- **时间复杂度**  
  - 预处理：对每个不同的 `trim` 只排序一次。若使用普通比较排序，时间为 `O(|trims|·n log n)`，而 `|trims| ≤ L ≤ 100`。  
  - 若采用基数排序，则每个 `trim` 的排序是 `O(trim·n)`，总时间为 `O( Σ trim_i · n ) ≤ O(L·n·|trims| )`，在最坏情况下仍是 `O(L·n·L) = O(L²·n)`，但常数更小。  
  - 查询阶段：`O(q)`（每条查询只取一次元素）。  

  与暴力解 `O(q·n log n)` 相比，**预处理只与不同的 `trim` 有关**，在 `q` 很大或 `trim` 重复很多时会快很多。

- **空间复杂度**  
  - 需要保存每个 `trim` 的排好序的列表，最坏情况下是 `O(|trims|·n)`。在本题约束（`n ≤ 100`）下完全可以接受。  
  - 基数排序额外使用的桶是 `O(n)`。

---

## 心得

- **核心技巧**：**预处理 + 稳定排序**（或基数排序）  
  把“相同的子问题”合并，只做一次计算，后续直接查表。

- **适用的题型**  
  1. 多次查询同一数组的不同“视图”（如截短、前缀、后缀等）。  
  2. 需要频繁比较相同长度的数字字符串（基数排序特别有效）。  
  3. “对同一集合做多次排序” 的场景，例如 “按不同属性排序” 的多查询。

- **解题钥匙**：**“把重复的工作缓存下来，保证排序的稳定性”**。

---

## 反思

- **第一反应**：直接对每条查询循环遍历并排序——最直观但可能重复劳动。  
- **最容易踩的坑**  
  - **相同数值的下标顺序**：忘记使用稳定排序或在比较键中加入下标，会导致答案错误。  
  - **截短时的前导零**：`"02"` 与 `"2"` 数值相同，但字符串比较时 `"02"` 更小，需要保留完整截短后的字符串（包括前导零）。  
  - **`k` 是 1‑based**：直接使用列表索引（0‑based）时要记得 `k-1`。  

- **下次类似题目**：第一步先**统计所有不同的子问题**（如不同的 `trim`、不同的前缀长度），判断是否可以一次性预处理，再**利用缓存**直接回答查询。这样既能避免重复计算，又能把复杂度控制在可接受范围。