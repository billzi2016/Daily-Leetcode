# #1187. **使数组严格递增** / Make Array Strictly Increasing

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/make-array-strictly-increasing/)

---

## 题目（英文原版）

**Description**

Given two integer arrays arr1 and arr2, return the minimum number of operations (possibly zero) needed to make arr1 strictly increasing.
In one operation, you can choose two indices 0 <= i < arr1.length and 0 <= j < arr2.length and do the assignment arr1[i] = arr2[j].
If there is no way to make arr1 strictly increasing, return -1.

**Examples**

**Example 1:**

```
Input: arr1 = [1,5,3,6,7], arr2 = [1,3,2,4]
Output: 1
Explanation: Replace 5 with 2, then arr1 = [1, 2, 3, 6, 7].
```

**Example 2:**

```
Input: arr1 = [1,5,3,6,7], arr2 = [4,3,1]
Output: 2
Explanation: Replace 5 with 3 and then replace 3 with 4. arr1 = [1, 3, 4, 6, 7].
```

**Example 3:**

```
Input: arr1 = [1,5,3,6,7], arr2 = [1,6,3,3]
Output: -1
Explanation: You can't make arr1 strictly increasing.
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 2000
- 0 <= arr1[i], arr2[i] <= 10^9

---

## 题目（中文翻译）

给定两个整数数组 `arr1` 和 `arr2`，返回使 `arr1` 严格递增（strictly increasing）所需的最少操作次数（可能为 0）。  
一次操作可以选择下标 `0 <= i < arr1.length` 和 `0 <= j < arr2.length`，并执行赋值 `arr1[i] = arr2[j]`。  
如果无法使 `arr1` 严格递增，返回 `-1`。

---

### 示例

**示例 1**

```text
Input: arr1 = [1,5,3,6,7], arr2 = [1,3,2,4]
Output: 1
Explanation: 将 5 替换为 2，得到 arr1 = [1, 2, 3, 6, 7]。
```

**示例 2**

```text
Input: arr1 = [1,5,3,6,7], arr2 = [4,3,1]
Output: 2
Explanation: 先将 5 替换为 3，再将 3 替换为 4，得到 arr1 = [1, 3, 4, 6, 7]。
```

**示例 3**

```text
Input: arr1 = [1,5,3,6,7], arr2 = [1,6,3,3]
Output: -1
Explanation: 无法使 arr1 严格递增。
```

---

### 约束条件

- `1 <= arr1.length, arr2.length <= 2000`
- `0 <= arr1[i], arr2[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的替换方案**，把 `arr1` 的每一个位置要么保持原值，要么换成 `arr2` 中的某个数。  
- 把 `arr2` 看成一本“字典”，键（key）是下标，值（value）是具体的数字。我们可以随意挑选字典里的词来替换 `arr1` 中的词。  
- 替换完以后检查 `arr1` 是否严格递增（即每个元素都比左边的元素大）。如果是，就记录这次用了多少次替换，最后取最小值。

**为什么正确**：  
因为我们遍历了**所有**可能的替换组合，凡是能让数组严格递增的方案一定会在枚举过程中出现，所以最小的替换次数一定能被找到。

**复杂度分析**：  
- 对每个位置我们都有 `|arr2| + 1` 种选择（保持不变或换成 `arr2` 的任意一个元素），所以总的组合数是  
  \[
  (|arr2|+1)^{|arr1|}
  \]
  这在最坏情况下是指数级的，随数组长度稍微增长就会爆炸。  
- 检查一次数组是否递增只需要线性遍历 `O(|arr1|)`。

> **大白话**：如果把 `O(n²)` 想象成“走十字路口每次要检查两条路”，那么 `O((m+1)^n)` 就像“每走一步都要打开成千上万的门”。显然不可接受。

#### 代码（Python）

```python
from itertools import product

def min_operations_bruteforce(arr1, arr2):
    n, m = len(arr1), len(arr2)
    best = float('inf')

    # 对每个位置 i，choices[i] = [保持原值] + arr2 中所有可能的值
    choices = [[arr1[i]] + arr2 for i in range(n)]

    # product 会生成所有可能的“选哪个值”的组合
    for cand in product(*choices):
        # 统计替换次数
        ops = sum(1 for i in range(n) if cand[i] != arr1[i])

        # 检查是否严格递增
        ok = True
        for i in range(1, n):
            if cand[i] <= cand[i-1]:
                ok = False
                break

        if ok:
            best = min(best, ops)

    return -1 if best == float('inf') else best
```

> 代码只为说明思路，实际运行会在 `n=5, m=4` 这样的极小规模时才会在合理时间内结束。

#### 复杂度

- **时间复杂度**：`O((m+1)^n * n)` —— 指数级别，随 `n`、`m` 增长非常快，几乎不可能在真实数据（`n,m ≤ 2000`）上通过。  
- **空间复杂度**：`O(n)` —— 只保存一次候选数组 `cand`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**：同样的“前缀已经处理成某个值”会被多次枚举。我们可以把**状态**压缩，只记住**到当前位置为止，前一个元素的最小可能值**以及**已经用了多少次替换**，其余信息不必再记录。

关键点：

1. **把 `arr2` 排序并去重**  
   - 替换时我们只关心**比前一个元素大的最小值**，有序数组配合二分查找可以在 `O(log m)` 时间内找到它。  
   - 去重是为了避免在二分时出现相同值导致的冗余状态。

2. **动态规划 + 二分**  
   - 设 `dp[i]` 为一种**可能的前一个值**（即处理完 `arr1[:i]` 后的最后一个数），对应的**最少替换次数**。  
   - 初始时只有一种状态：`prev = -inf`（比所有数都小），`ops = 0`。  
   - 逐个遍历 `arr1` 的位置 `i`，对每个已有的 `prev`，尝试两种操作：  
     a. **不替换**：如果 `arr1[i] > prev`，则可以保留 `arr1[i]`，得到新的状态 `prev' = arr1[i]`，`ops` 不变。  
     b. **替换**：在已排序好的 `arr2` 中，用二分找到**第一个大于 `prev` 的元素** `x`（`x` 必须比前一个元素大），把 `arr1[i]` 换成 `x`，得到状态 `prev' = x`，`ops+1`。  
   - 对同一个 `prev'`，我们只保留最小的 `ops`（因为后面的计算只关心次数最少的路径）。

3. **状态压缩**  
   - 由于 `prev` 只会取 `arr1` 中的原始值或 `arr2` 中的元素，最多 `n + m` 种可能。我们用字典 `cur_dp` 把 `prev` → 最少操作数 保存下来。  
   - 每遍历一次 `arr1`，都生成一个新的字典 `next_dp`，随后用 `next_dp` 替换 `cur_dp`。

4. **答案**  
   - 最后遍历完所有位置后，`cur_dp` 中所有状态的 `ops` 中的最小值即为答案。若字典为空（没有任何合法状态），返回 `-1`。

**为什么快**：  
- 每个位置只遍历当前字典的键数，键的数量始终被限制在 `O(n + m)`。  
- 二分查找让“找下一个更大的数”从线性 `O(m)` 降到 `O(log m)`。  
- 因此总体时间复杂度是 `O(n * (n + m) * log m)`，在本题约 `2000 * 4000 * log2000` 仍然可以轻松通过。

#### 代码（Python）

```python
import bisect
from collections import defaultdict

def min_operations(arr1, arr2):
    """
    动态规划 + 二分
    返回使 arr1 严格递增所需的最少替换次数，若不可行返回 -1
    """
    # 1. 预处理 arr2：排序并去重（相当于一本“查字典”，键是数值本身）
    arr2 = sorted(set(arr2))

    # 2. dp: key = 当前已经确定的最后一个数，value = 已经用了多少次替换
    # 初始时「前一个数」比所有可能的数都小，用 -inf 表示（这里用 -1 因为题目数 >= 0）
    cur_dp = {-1: 0}

    for idx, a in enumerate(arr1):
        next_dp = defaultdict(lambda: float('inf'))  # 默认值设为无穷大

        for prev_val, ops in cur_dp.items():
            # 2.1. 不替换的情况：只有当 a > prev_val 时才合法
            if a > prev_val:
                # 更新状态：最后一个数变成 a，操作次数不变
                if ops < next_dp[a]:
                    next_dp[a] = ops

            # 2.2. 替换的情况：在 arr2 中找第一个 > prev_val 的数
            # bisect_right 返回第一个大于 prev_val 的位置
            pos = bisect.bisect_right(arr2, prev_val)
            if pos < len(arr2):          # 说明还有可以使用的数
                new_val = arr2[pos]      # 选最小的合法数
                # 替换一次，操作次数 +1
                if ops + 1 < next_dp[new_val]:
                    next_dp[new_val] = ops + 1

        # 若没有任何合法状态，直接返回 -1
        if not next_dp:
            return -1

        cur_dp = next_dp   # 进入下一轮

    # 所有位置处理完后，答案是所有状态中 ops 的最小值
    return min(cur_dp.values())
```

> 关键行解释  
> - `arr2 = sorted(set(arr2))`：把 `arr2` 当作一本“查字典”，去掉重复的页码，方便二分。  
> - `bisect.bisect_right(arr2, prev_val)`：在有序的 `arr2` 中，快速定位**第一个比前一个元素大的数**。相当于在字典里“顺手翻到下一个更大的词”。  
> - `defaultdict(lambda: float('inf'))`：把“没有记录过的状态”视为无限大的操作次数，后面取最小值时自然会被淘汰。

#### 复杂度

- **时间复杂度**：`O(n * (k) * log m)`，其中 `k` 为每一步 DP 中的状态数，最坏 `k ≤ n + m`。对本题来说约为 `O(n * (n+m) * log m)`，在 2000 规模下毫秒级。  
  - 与暴力解的指数级 `O((m+1)^n)` 相比，**每一步只看一次前缀的“最小代价”，不再重复遍历所有组合**，所以快得多。  
- **空间复杂度**：`O(k)`，即保存当前 DP 状态的字典，最多 `O(n+m)`，远小于暴力解的指数空间。

---

## 心得

- **核心技巧**：**动态规划 + 有序数组二分**，把“前一个元素的大小”压缩成状态，再用二分快速寻找可替换的最小值。  
- **适用题型**：  
  1. “把数组变成递增/递减序列，需要最少操作次数”——如 *Make Array Strictly Increasing*、*Minimum Operations to Make Array Non‑decreasing*。  
  2. “在序列中插入/替换元素，使得满足某种单调约束”，常用 **DP + 二分**（或 **单调栈**）来加速。  
- **一句话总结解题钥匙**：**把“已经处理好的前缀”抽象成“最后一个数 + 已用最少操作数”，用有序集合二分找下一个合法数，动态规划把指数搜索压缩成线性状态**。

---

## 反思

- **第一反应**：看到“可以把任意位置换成 `arr2` 中的数”，立刻想到“遍历所有替换组合”。这就是暴力思路。  
- **最容易踩的坑**：  
  - **去重**：如果不把 `arr2` 去重，二分仍能工作，但会产生大量冗余状态，导致时间和空间爆炸。  
  - **边界**：`prev` 需要比所有可能的数都小，选 `-1`（或 `-inf`）是安全的，因为题目数值≥0。  
  - **状态剪枝**：同一个 `prev` 可能出现多次，只保留最小的操作次数，否则 DP 会膨胀。  
- **下次第一步**：先**把可替换的集合排序去重**，再思考“每一步只关心前一个数的大小”，即尝试 **DP + 二分** 的思路，而不是直接枚举。这样能把问题从指数级转化为多项式级。