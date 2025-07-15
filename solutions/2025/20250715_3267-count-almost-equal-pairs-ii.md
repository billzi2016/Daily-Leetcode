# #3267. 几乎相等数对计数 II / Count Almost Equal Pairs II

> 难度：困难 · 标签：Array、Hash Table、Sorting、Counting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-almost-equal-pairs-ii/)

---

## 题目（英文原版）

**Description**

Attention: In this version, the number of operations that can be performed, has been increased to twice.
You are given an array nums consisting of positive integers.
We call two integers x and y almost equal if both integers can become equal after performing the following operation at most twice:
Return the number of indices i and j in nums where i < j such that nums[i] and nums[j] are almost equal.
Note that it is allowed for an integer to have leading zeros after performing an operation.

**Examples**

**Example 1:**

```
Input: nums = [1023,2310,2130,213]
Output: 4
Explanation:
The almost equal pairs of elements are:
```

**Example 2:**

```
Input: nums = [1,10,100]
Output: 3
Explanation:
The almost equal pairs of elements are:
```

**Constraints**

- 2 <= nums.length <= 5000
- 1 <= nums[i] < 107

---

## 题目（中文翻译）

**注意**：在本版本中，允许执行的操作次数增加至 **两次**。

给定一个由正整数构成的数组（array）`nums`。

我们称两个整数 `x` 和 `y` 为**几乎相等**（almost equal），如果在至多 **两次**（at most twice）执行以下操作后，它们可以变得相等：

> **操作**：任选一个整数的任意一位，将该位的数字替换为 `0`，并且可以在结果前面补上任意数量的前导零（leading zeros）。

返回满足 `i < j` 且 `nums[i]` 与 `nums[j]` **几乎相等** 的索引对 `(i, j)` 的数量。

> 注意：执行操作后，整数可以出现前导零。

### 示例

**示例 1**

```
Input: nums = [1023,2310,2130,213]
Output: 4
Explanation:
几乎相等的元素对为：
```

**示例 2**

```
Input: nums = [1,10,100]
Output: 3
Explanation:
几乎相等的元素对为：
```

### 约束条件

- `2 <= nums.length <= 5000`
- `1 <= nums[i] < 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有下标对 `(i, j)` 都枚举一遍**，把 `nums[i]` 和 `nums[j]` 分别做**不超过两次的交换操作**，看看能否得到相同的整数。

- **数据结构**：我们只需要普通的 `list`（保存数字的字符数组）和 `set`（去重）。  
  - `set` 就像一本字典，里面的每一页（元素）都是唯一的；我们把每一次交换得到的整数都放进去，保证不把同一个结果算两次。

- **为什么正确**：  
  1. 对每一对 `(i, j)`，我们把 `nums[i]` 能在 ≤2 次交换后得到的所有整数全部列举出来（记作 `S_i`），同理得到 `S_j`。  
  2. 只要 `S_i ∩ S_j` 非空，说明这两个数可以通过 ≤2 次交换变成同一个数，题目要求的 “almost equal” 就成立。  
  3. 把所有满足条件的对计数，即得到答案。

- **复杂度分析**（大白话）  
  - 枚举所有下标对需要 `n·(n‑1)/2` 次，大约是 `n²/2`，如果 `n=5000` 那就是 **约 1.25×10⁷** 次。  
  - 对每个数我们要生成 **所有可能的交换结果**。一个整数最多有 7 位（因为 `nums[i] < 10⁷`），一次交换可以选 `C(7,2)=21` 种方式，**两次交换**最多是 `21²≈441` 种（实际会更少，因为有些交换会得到相同的结果）。  
  - 所以暴力的总时间大约是 `O(n²·d⁴)`（`d` 为位数），在最坏情况下会超过 10¹¹ 步，**完全跑不动**。  
  - 空间上只需要保存几个临时集合，`O(1)`。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def all_after_two_swaps(x: int) -> set[int]:
    """返回整数 x 经过至多两次任意位置交换后可以得到的所有整数（含原数）。"""
    s = str(x)                     # 把数字变成字符序列，方便交换
    d = len(s)
    res = {x}                      # 零次交换的情况
    # ---------- 一次交换 ----------
    for i, j in combinations(range(d), 2):
        lst = list(s)
        lst[i], lst[j] = lst[j], lst[i]          # 交换两位
        res.add(int(''.join(lst)))               # 加入集合去重
    # ---------- 两次交换 ----------
    # 把一次交换的结果再进行一次交换
    one_swap_vals = list(res)                    # 已经包含所有一次交换的数
    for val in one_swap_vals:
        ss = str(val)
        dd = len(ss)
        for i, j in combinations(range(dd), 2):
            lst = list(ss)
            lst[i], lst[j] = lst[j], lst[i]
            res.add(int(''.join(lst)))
    return res

def count_almost_equal_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    for i in range(n):
        set_i = all_after_two_swaps(nums[i])
        for j in range(i + 1, n):
            # 只要两集合有交集即满足条件
            if any(v in set_i for v in all_after_two_swaps(nums[j])):
                ans += 1
    return ans
```

> **注释**  
> - `combinations(range(d), 2)` 就像在字典里挑两页，页码的组合数就是 `C(d,2)`。  
> - `int(''.join(lst))` 把字符列表重新拼成整数，允许出现前导零（比如 `'0123'` → `123`，在 Python 中自动去掉前导零）。

#### 复杂度

- **时间复杂度**：`O(n² · d⁴)`，其中 `d ≤ 7`。  
  - “`n²`” 表示我们遍历所有下标对；“`d⁴`” 代表每个数最多要尝试两次交换的所有组合。  
  - 对于 `n=5000`、`d=7`，这已经是 **上百亿次**的计算，根本不可接受。

- **空间复杂度**：`O(1)`（不计输入数组），只用了几个临时集合，大小与位数 `d` 成正比，几乎可以忽略不计。

---

### 2. 最优解

#### 思路  

暴力的**瓶颈**在于**两层循环遍历所有下标对**。我们可以把这一步换成“**一遍扫描，实时查询**”。核心思想是：

> 当我们从左到右遍历数组时，**把已经出现过的数字的所有“可达形态”**记在哈希表里。  
> 对当前数字 `x`，只要把它 **自身的所有可达形态**（≤2 次交换后得到的整数）逐个查表，累计之前出现过的次数，就得到以 `x` 为右端点的合法对数。

这样，每个元素只会被 **处理一次**，而不是与所有后面的元素比较。

关键点：

1. **生成可达形态**  
   - 与暴力相同，我们仍然要枚举一次、两次交换的所有结果。  
   - 由于位数最多 7，最多产生约 `1 + 21 + 441 ≈ 463` 个不同整数，**常数级**，可以直接生成并放入 `set`。

2. **哈希表的意义**  
   - 把每一个“可达形态”看成 **字典的键**，对应的值是**已经出现过的原始数字的数量**。  
   - 这相当于“把所有可能的结果映射回原始下标”，查询时只要 O(1)（平均）时间。

3. **计数过程**  

   ```text
   ans = 0
   freq = {}   # 哈希表：key = 可达整数，value = 已出现的次数
   for x in nums:
       S = all_after_two_swaps(x)   # 生成集合
       for v in S:                  # 查表
           ans += freq.get(v, 0)   # 之前出现过多少个能变成 v
       for v in S:                  # 把当前的可达形态加入表中，供后面的数使用
           freq[v] = freq.get(v, 0) + 1
   ```

4. **为什么只加一次**  
   - 当我们遍历到 `x` 时，只统计左侧已经出现的数（`i < j`），所以不会出现重复计数。  
   - 每对 `(i, j)` 正好在遍历到 `j` 时被统计一次。

5. **时间空间对比**  
   - **时间**：对每个元素我们生成至多 `≈ 463` 个形态，随后做两遍哈希表遍历（查询 + 更新），总计 `O(n · d⁴)`，但去掉了 `n` 的平方因子。  
     对 `n = 5000`、`d = 7`，大约是 `5000 × 463 ≈ 2.3×10⁶` 次操作，轻松在 1 秒以内完成。  
   - **空间**：哈希表最多存 `n × 463` 条记录（最坏情况每个数的形态互不相同），约 `2.3×10⁶` 条键值对，**在 Python 中大约几百 MB**，仍在题目限制内（LeetCode 常给 256 MB，实际键值是整数，压缩后更小）。如果担心空间，可以在插入时使用 `defaultdict(int)`，并在遍历结束后直接丢弃。

#### 代码（Python）

```python
from itertools import combinations
from collections import defaultdict
from typing import List

def reachable_vals(x: int) -> list[int]:
    """
    返回整数 x 在至多两次任意位置交换后能得到的所有不同整数（包括 x 本身）。
    由于位数 ≤7，直接枚举即可。
    """
    s = str(x)
    d = len(s)
    results = {x}                         # 零次交换

    # ---------- 一次交换 ----------
    for i, j in combinations(range(d), 2):
        lst = list(s)
        lst[i], lst[j] = lst[j], lst[i]
        results.add(int(''.join(lst)))

    # ---------- 两次交换 ----------
    # 对已经得到的每个数再做一次交换
    one_swap = list(results)              # 把一次交换的结果保存下来
    for val in one_swap:
        ss = str(val)
        dd = len(ss)
        for i, j in combinations(range(dd), 2):
            lst = list(ss)
            lst[i], lst[j] = lst[j], lst[i]
            results.add(int(''.join(lst)))

    return list(results)                  # 返回列表，便于遍历

def count_almost_equal(nums: List[int]) -> int:
    """
    主函数：一次遍历 + 哈希表计数
    """
    freq = defaultdict(int)   # key: 可达整数，value: 出现次数
    ans = 0

    for x in nums:
        vals = reachable_vals(x)            # 所有 ≤2 次交换后的形态
        # 统计左侧已经出现的、可以和 x 变成同一个数的下标数量
        for v in vals:
            ans += freq[v]                  # freq[v] 若不存在则默认 0
        # 把当前数字的所有形态加入哈希表，供后面的元素使用
        for v in vals:
            freq[v] += 1

    return ans
```

> **代码要点**  
> - `defaultdict(int)` 相当于一本“自动补零的字典”，查不到键时直接返回 `0`，省去 `if` 判断。  
> - `reachable_vals` 使用 **集合去重**，保证同一个整数不会被多次计入 `freq`，防止同一对被重复计数。  
> - 允许前导零：比如 `1023` 交换后得到 `'0123'`，`int('0123')` 自动变成 `123`，这正是题目所允许的。

#### 复杂度

- **时间复杂度**：`O(n · d⁴)`（`d ≤ 7` 为位数）。  
  - 实际常数约为 `463`，所以整体约 `2.3·10⁶` 次基本操作，远快于暴力的 `n²` 级别。  
  - 与暴力相比，**把 `n²` 的瓶颈降到了线性**，因此在最坏输入下也能在毫秒级完成。

- **空间复杂度**：`O(n · d⁴)`（哈希表存储所有出现过的可达整数）。  
  - 最多约 `2.3·10⁶` 条记录，约几百 MB，符合题目限制。  
  - 如果想进一步压缩空间，可以在遍历完后直接 `freq.clear()`，因为只在一次遍历中使用。

---

## 心得

- **核心技巧**：**把“所有可能的结果”预先映射到哈希表**，利用“一遍遍历 + 计数”替代二重循环。  
- **适用场景**（类似题目）  
  1. **Count Pairs With Same Frequency After One Operation**（如「Count Almost Equal Pairs I」）  
  2. **Pairs of Numbers With Same Digit Multiset**（把数字的数字集合映射到哈希表）  
  3. **Subarrays With Same Sum After At Most K Modifications**（把所有可达的前缀和映射到哈希表）  
- **一句话总结**：把每个元素的“可达集合”写进字典，遍历时直接查询，省去两层循环。

---

## 反思

- **第一反应**：直接枚举所有下标对，写一个函数把数字做 ≤2 次交换后得到的所有整数列举出来。  
- **最容易踩的坑**  
  1. **重复计数**：同一个可达整数如果在同一个数的两次不同交换路径中出现，需要去重（使用 `set`）。  
  2. **前导零**：交换后可能产生 `'0xxx'`，转换成整数时会自动去掉零，这在比较时必须保持一致。  
  3. **哈希表冲突**：在统计时一定要先 **查询** 再 **写入**，否则会把自己算进去，导致 `i == j` 的错误计数。  
- **下次类似题目第一步**：先思考**“能产生多少种不同的状态”**，如果状态数是常数级（如位数 ≤7），就可以**把所有状态写进哈希表**，再用一次遍历完成计数。这样往往能把原本的 `O(n²)` 降到 `O(n)`。