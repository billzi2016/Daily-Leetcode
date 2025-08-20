# #3312. 排序的 GCD 配对查询 / Sorted GCD Pair Queries

> 难度：困难 · 标签：Array、Hash Table、Math、Binary Search、Combinatorics、Counting、Number Theory、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sorted-gcd-pair-queries/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and an integer array queries.
Let gcdPairs denote an array obtained by calculating the GCD of all possible pairs (nums[i], nums[j]), where 0 <= i < j < n, and then sorting these values in ascending order.
For each query queries[i], you need to find the element at index queries[i] in gcdPairs.
Return an integer array answer, where answer[i] is the value at gcdPairs[queries[i]] for each query.
The term gcd(a, b) denotes the greatest common divisor of a and b.

**Examples**

**Example 1:**

```
Input: nums = [2,3,4], queries = [0,2,2]
Output: [1,2,2]
Explanation:
gcdPairs = [gcd(nums[0], nums[1]), gcd(nums[0], nums[2]), gcd(nums[1], nums[2])] = [1, 2, 1] .
After sorting in ascending order, gcdPairs = [1, 1, 2] .
So, the answer is [gcdPairs[queries[0]], gcdPairs[queries[1]], gcdPairs[queries[2]]] = [1, 2, 2] .
```

**Example 2:**

```
Input: nums = [4,4,2,1], queries = [5,3,1,0]
Output: [4,2,1,1]
Explanation:
gcdPairs sorted in ascending order is [1, 1, 1, 2, 2, 4] .
```

**Example 3:**

```
Input: nums = [2,2], queries = [0,0]
Output: [2,2]
Explanation:
gcdPairs = [2] .
```

**Constraints**

- 2 <= n == nums.length <= 105
- 1 <= nums[i] <= 5 * 104
- 1 <= queries.length <= 105
- 0 <= queries[i] < n * (n - 1) / 2

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 和一个整数数组 `queries`。  
设 `gcdPairs` 为一个数组，先计算所有可能的配对 `(nums[i], nums[j])` 的最大公约数（gcd），其中 `0 ≤ i < j < n`，然后将得到的值按升序排序得到 `gcdPairs`。  

对于每个查询 `queries[i]`，需要找到 `gcdPairs` 中下标为 `queries[i]` 的元素。  
返回一个整数数组 `answer`，其中 `answer[i]` 为 `gcdPairs[queries[i]]` 的值。  

**术语说明**  
- `gcd(a, b)` 表示 `a` 与 `b` 的最大公约数（greatest common divisor）。

---

## 示例

### 示例 1
**输入**  
`nums = [2,3,4], queries = [0,2,2]`

**输出**  
`[1,2,2]`

**解释**  
`gcdPairs = [gcd(nums[0], nums[1]), gcd(nums[0], nums[2]), gcd(nums[1], nums[2])] = [1, 2, 1]`。  
按升序排序后，`gcdPairs = [1, 1, 2]`。  
因此答案为 `[gcdPairs[queries[0]], gcdPairs[queries[1]], gcdPairs[queries[2]]] = [1, 2, 2]`。

### 示例 2
**输入**  
`nums = [4,4,2,1], queries = [5,3,1,0]`

**输出**  
`[4,2,1,1]`

**解释**  
所有配对的 GCD 排序后得到 `[1, 1, 1, 2, 2, 4]`。

### 示例 3
**输入**  
`nums = [2,2], queries = [0,0]`

**输出**  
`[2,2]`

**解释**  
`gcdPairs = [2]`。

---

## 约束条件

- `2 ≤ n == nums.length ≤ 10^5`
- `1 ≤ nums[i] ≤ 5 * 10^4`
- `1 ≤ queries.length ≤ 10^5`
- `0 ≤ queries[i] < n * (n - 1) / 2`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有合法的数对 `(nums[i], nums[j]) (i < j)` 都枚举出来，逐个求它们的 **最大公约数（GCD）**，得到一个长度为  

\[
\frac{n\,(n-1)}{2}
\]

的数组 `gcdPairs`，随后把它排序。查询 `queries[i]` 时，只要取 `gcdPairs[queries[i]]` 即可。

> **类比**：  
> 把 `nums` 看成一堆水果，暴力做法就是把每两个水果配对，算出它们的“相似度”（这里是 GCD），再把所有相似度排成一列，按顺序取第 k 个。

**为什么正确**：  
因为题目要求的正是「所有两两 GCD 的升序排列」，暴力枚举显然能得到完整集合，排序后自然满足要求。

#### 代码（Python）

```python
import math
from typing import List

def sorted_gcd_pair_queries_bruteforce(nums: List[int], queries: List[int]) -> List[int]:
    n = len(nums)
    # 1. 枚举所有 i < j 的数对，计算 GCD
    gcd_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            g = math.gcd(nums[i], nums[j])   # 计算最大公约数
            gcd_pairs.append(g)

    # 2. 升序排序
    gcd_pairs.sort()

    # 3. 根据查询下标直接取值
    return [gcd_pairs[q] for q in queries]
```

> 关键行说明  
> - `math.gcd`：Python 标准库提供的求两数最大公约数的函数，底层是欧几里得算法。  
> - 双层 `for` 循环产生所有 `(i, j)`，时间随 `n` 的平方增长。  

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - `n²` 来自枚举所有数对。  
  - `log n` 来自对 `≈ n²/2` 个元素的排序（排序的时间是 `O(m log m)`，这里 `m ≈ n²/2`）。  
  - 大白话：如果 `n = 10⁴`，那就要进行约 5·10⁷ 次 GCD 计算，再把这么多数字排个序，几乎不可能在 1 秒内跑完。  

- **空间复杂度**：`O(n²)` 用于存放所有 GCD。  
  - 这在 `n = 10⁵` 时根本装不下（需要 5·10⁹ 个整数），所以只能当作思路演示，不能直接提交。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：

1. **枚举所有数对**——数量是 `n·(n‑1)/2`，随 `n` 的平方增长。  
2. **对巨大的 GCD 列表排序**——即使不枚举，若要得到第 `k` 小的值仍需要把所有值排好序。

我们需要 **跳过枚举**，直接统计“有多少对的 GCD 等于某个值”。有了每个可能 GCD 的出现次数，就可以在 **累加**（前缀和）后用二分查找定位第 `k` 小的 GCD。

---

#### 2.1 统计 GCD = g 的对数  

设 `cnt[x]` 为数组 `nums` 中等于 `x` 的出现次数（`x ≤ 5·10⁴`），我们先把所有数的出现频次记下来。  

> **类比**：`cnt` 像一本词典，单词是数字，页码是出现次数。  

若把所有 **能被 g 整除** 的数挑出来，记它们的总个数为 `mult[g]`。  
显然，任选其中的任意两数（顺序不重要）就得到一对 **“都能被 g 整除”** 的数对，数量是组合数  

\[
C(mult[g], 2) = \frac{mult[g]\,(mult[g]-1)}{2}
\]

这正是 **GCD 至少为 g**（即 `≥ g`）的数对数量。  

但是我们真正想要的是 **恰好等于 g** 的数对。  
可以用 **包含‑排除**（或莫比乌斯反演）把“大于 g 的情况”剔除掉：

\[
exact[g] = C(mult[g], 2) \;-\; \sum_{k=2}^{\lfloor maxV/g \rfloor} exact[k\cdot g]
\]

从 **大到小** 依次计算 `exact[g]`，因为在计算 `exact[g]` 时，所有更大的倍数 `k·g` 已经算好（递推的方向保证了这一点）。

---

#### 2.2 计算 `mult[g]`  

`mult[g]` 需要把所有 `cnt[x]` 中 `x` 为 `g` 的倍数的频次加起来。  
直接遍历每个 `g` 的所有倍数的做法：

```python
for g in range(1, maxV + 1):
    for m in range(g, maxV + 1, g):
        mult[g] += cnt[m]
```

时间复杂度是  

\[
\sum_{g=1}^{maxV} \frac{maxV}{g} = maxV \cdot H_{maxV} \approx maxV \log maxV
\]

`maxV = 5·10⁴`，所以约 `5·10⁴·log(5·10⁴) ≈ 6·10⁵` 次循环，轻松通过。

---

#### 2.3 由 `exact[g]` 得到前缀累计  

把所有可能的 GCD（从小到大）出现次数累加：

```python
pref[g] = pref[g-1] + exact[g]   # 0 <= g <= maxV
```

`pref[g]` 表示 **“GCD ≤ g 的数对总数”**。  
对于查询 `k`（0‑基），我们要找最小的 `g` 使得 `pref[g] > k`，这正是 **二分查找** 的典型场景。

---

#### 2.4 复杂度对比  

| 步骤 | 时间 | 空间 | 解释 |
|------|------|------|------|
| 统计 `cnt` | `O(n)` | `O(maxV)` | 只遍历一次原数组 |
| 计算 `mult[g]` | `O(maxV log maxV)` | 同上 | 类似筛法 |
| 计算 `exact[g]`（倒序） | `O(maxV log maxV)` | 同上 | 包含‑排除 |
| 前缀和 `pref` | `O(maxV)` | 同上 | 线性遍历 |
| 每个查询二分 | `O(log maxV)` | - | `maxV ≤ 5·10⁴`，二分极快 |
| **总计** | `O((n + maxV) log maxV + Q log maxV)` | `O(maxV)` | 对 `n, Q ≤ 10⁵` 完全可接受 |

与暴力 `O(n²)` 相比，时间从 **平方级** 降到 **近线性级**，空间也从 `O(n²)` 降到只需要 `maxV`（≈ 5·10⁴）的几个整数数组。

---

#### 代码（Python）

```python
import math
from typing import List

def sorted_gcd_pair_queries(nums: List[int], queries: List[int]) -> List[int]:
    """
    最优解：先统计每个可能的 GCD 出现了多少次，再用前缀和 + 二分定位答案。
    """
    n = len(nums)
    max_val = max(nums)                     # 题目限定 ≤ 5*10^4
    # 1️⃣ 统计每个数出现的次数
    cnt = [0] * (max_val + 1)
    for v in nums:
        cnt[v] += 1

    # 2️⃣ 计算 mult[g] = 有多少个数是 g 的倍数
    mult = [0] * (max_val + 1)
    for g in range(1, max_val + 1):
        # 把所有 g 的倍数的频次加起来
        for m in range(g, max_val + 1, g):
            mult[g] += cnt[m]

    # 3️⃣ 由大到小求 exact[g] = GCD 恰好等于 g 的对数
    exact = [0] * (max_val + 1)          # 使用 64 位整数防止溢出
    for g in range(max_val, 0, -1):
        # 首先算出“都能被 g 整除”的对数（组合数）
        total = mult[g] * (mult[g] - 1) // 2
        # 减去已经统计过的更大的倍数的情况（包含‑排除）
        mul = 2 * g
        while mul <= max_val:
            total -= exact[mul]
            mul += g
        exact[g] = total

    # 4️⃣ 前缀和：pref[g] = GCD ≤ g 的对数
    pref = [0] * (max_val + 1)
    running = 0
    for g in range(1, max_val + 1):
        running += exact[g]
        pref[g] = running

    # 5️⃣ 对每个查询二分寻找最小的 g 使得 pref[g] > k
    def kth_gcd(k: int) -> int:
        """返回第 k 小（0-index）的 GCD 值"""
        lo, hi = 1, max_val
        while lo < hi:
            mid = (lo + hi) // 2
            if pref[mid] > k:        # 说明答案 ≤ mid
                hi = mid
            else:
                lo = mid + 1
        return lo

    # 6️⃣ 统一输出
    return [kth_gcd(q) for q in queries]
```

> **关键行解释**  
> - 第 8‑12 行：`cnt` 相当于“词典”，记录每个数出现了几次。  
> - 第 15‑18 行：通过 **筛**（类似埃拉托斯特尼筛素数）累计所有 `g` 的倍数出现次数，得到 `mult[g]`。  
> - 第 22‑30 行：倒序遍历保证在处理 `g` 时，`exact[2g]、exact[3g]…` 已经算好，直接减去即可完成包含‑排除。  
> - 第 34‑38 行：前缀和 `pref` 把 “≤ g” 的对数累计，后面二分只要看 `pref[mid]` 是否“大于查询下标”。  
> - 第 41‑49 行：二分查找的模板，时间是 `O(log max_val)`，对 10⁵ 条查询也足够快。  

---

#### 复杂度  

- **时间复杂度**：`O((n + maxV)·log maxV + Q·log maxV)`  
  - 其中 `maxV = max(nums) ≤ 5·10⁴`。  
  - 与暴力的 `O(n² log n)` 相比，下降到了 **近线性**，在最坏 `n = Q = 10⁵` 时仍在几百万次运算范围，轻松通过。

- **空间复杂度**：`O(maxV)`  
  - 只用几个长度为 `maxV+1` 的整数数组（`cnt, mult, exact, pref`），约 5·10⁴ × 4 ≈ 200 KB，远小于 `O(n²)`。

---

## 心得  

- **核心技巧**：**利用数的倍数关系统计 GCD 出现次数 + 包含‑排除（或莫比乌斯反演）**。  
- **适用题型**（相似思路）  
  1. “所有子数组的 GCD/LCM 计数”  
  2. “区间内最大公约数 ≥ K 的对数”  
  3. “求所有数对的最大公约数的第 k 大/小值”  

- **一句话总结**：**先把“有多少对的 GCD 为 g”算出来，再用前缀累计+二分直接定位第 k 小的 GCD**。

---

## 反思  

- **第一反应**：直接枚举所有数对并排序——虽然最直观，却忽略了 `n` 达到 10⁵ 时的规模爆炸。  
- **最容易踩的坑**  
  - **溢出**：对 `mult[g]` 进行组合 `C(mult,2)` 时需要 64 位整数（Python 自动大整数，但在其他语言要注意）。  
  - **边界**：`queries[i]` 是 0‑基的，第 `k` 小对应 `pref[g] > k`（而不是 `≥ k`）。  
  - **遗漏倍数**：在倒序计算 `exact[g]` 时必须完整遍历 `2g, 3g, …`，否则会高估。  
- **下次遇到同类题**：第一步先 **统计每个可能值的出现次数**（利用数的倍数或因子关系），再 **用包含‑排除/莫比乌斯** 把“至少 …”转化为“恰好 …”。这样即可把 “枚举所有对” 的二次爆炸彻底规避。