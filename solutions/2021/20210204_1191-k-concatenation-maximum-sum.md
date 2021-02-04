# #1191. K 次拼接的最大子数组和 / K-Concatenation Maximum Sum

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/k-concatenation-maximum-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array arr and an integer k, modify the array by repeating it k times.
For example, if arr = [1, 2] and k = 3 then the modified array will be [1, 2, 1, 2, 1, 2].
Return the maximum sub-array sum in the modified array. Note that the length of the sub-array can be 0 and its sum in that case is 0.
As the answer can be very large, return the answer modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: arr = [1,2], k = 3
Output: 9
```

**Example 2:**

```
Input: arr = [1,-2,1], k = 5
Output: 2
```

**Example 3:**

```
Input: arr = [-1,-2], k = 7
Output: 0
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= k <= 105
- -104 <= arr[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `arr` 和一个整数 `k`，将数组重复 `k` 次后得到修改后的数组。  
例如，若 `arr = [1, 2]` 且 `k = 3`，则修改后的数组为 `[1, 2, 1, 2, 1, 2]`。  

返回修改后数组中**最大子数组和**（subarray），注意子数组的长度可以为 `0`，此时其和为 `0`。  

由于答案可能非常大，返回答案对 `10^9 + 7` 取模后的结果。

**示例 1**  
Input: `arr = [1,2]`, `k = 3`  
Output: `9`

**示例 2**  
Input: `arr = [1,-2,1]`, `k = 5`  
Output: `2`

**示例 3**  
Input: `arr = [-1,-2]`, `k = 7`  
Output: `0`

**约束条件**  
- `1 <= arr.length <= 10^5`  
- `1 <= k <= 10^5`  
- `-10^4 <= arr[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把原数组 **arr** 按题目要求复制 **k** 次，得到一个长度为 `n * k` 的新数组，然后在这个新数组上求“最大子数组和”。  
这里的“最大子数组和”可以使用 **Kadane 算法**——它的工作原理类似于在一条路上走，随时记录当前这段路的累计收益，如果累计收益变负了，就把起点搬到下一格，重新开始累计。  

- **数据结构**：我们只需要一个普通的 Python 列表来存放复制后的数组。可以把它想象成把一本书的章节 **arr** 连续复印 **k** 份，排成一本更长的书。  
- **正确性**：因为我们把题目要求的完整序列都显式写出来了，随后在这完整序列上跑 Kadane，必然会得到所有可能子数组的最大和。  

#### 代码（Python）

```python
def maxSubArray_bruteforce(arr, k):
    MOD = 10**9 + 7

    # 1️⃣ 把数组复制 k 次 → 长度为 n * k 的新数组
    repeated = arr * k                     # python 的 * 会把列表复制多份

    # 2️⃣ Kadane 算法求最大子数组和
    max_ending_here = 0        # 当前子数组的累计和
    max_so_far = 0            # 记录到目前为止的最大和，初始为 0（允许空子数组）

    for num in repeated:
        max_ending_here = max(0, max_ending_here + num)   # 累计和若为负则重置为 0
        max_so_far = max(max_so_far, max_ending_here)    # 更新全局最大

    return max_so_far % MOD
```

> **关键行中文注释**  
> - `repeated = arr * k` 把原数组复印 `k` 份。  
> - `max_ending_here = max(0, max_ending_here + num)` 如果累计和变负，就把“起点”搬到下一位（相当于丢弃之前的负贡献）。  
> - `max_so_far = max(max_so_far, max_ending_here)` 记录遍历过程中出现的最高累计和。  

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 解释：我们遍历了 `n*k` 个元素（`n` 为原数组长度），如果 `n = 10⁵，k = 10⁵`，这会达到 `10¹⁰` 步，根本跑不完。  
- **空间复杂度**：`O(n * k)`（存放复制后的数组）  
  - 实际上我们只需要一个临时列表，最坏情况下也要占用 `n*k` 的内存，同样不可接受。  

> 暴力解只能用来验证思路或在极小的测试数据上跑通，实际提交时会因超时/内存超限而被拒绝。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **复制整个数组** 这一步——当 `k` 很大时，复制会产生巨大的时间和空间开销。我们要 **在不显式构造完整数组的前提下**，直接算出最大子数组和。  

从 Kadane 的角度看，最大子数组只会出现在以下三种“形态”中（`k > 1` 时）：

1. **只在单个拷贝里**：答案等同于 `k = 1` 时的最大子数组和。  
2. **跨越多个拷贝的完整数组**：如果整个数组的总和 `S = sum(arr)` 为正，那么把整个数组重复多次会让和线性增长，最大子数组可以是 **全部 k 份** 的和，即 `S * k`。  
3. **跨越首尾但不完整覆盖中间**：子数组从某一次拷贝的**后缀**开始，经过若干完整拷贝（可能为 0），再在最后一次拷贝的**前缀**结束。此时最大和 =  
   `max_suffix + max_prefix + (k-2) * S`（`k-2` 份完整数组的贡献），其中  
   - `max_prefix` = 第一次拷贝中，以 **开头** 为起点的最大前缀和。  
   - `max_suffix` = 最后一次拷贝中，以 **结尾** 为终点的最大后缀和。  

> 这里的 “前缀 / 后缀” 可以想象成一根绳子：我们把数组首部的若干元素当作绳子的一段，尾部的若干元素当作另一段，连接在一起形成更长的子数组。

因此，只要我们能在 **一次遍历** 中算出以下三个值，就能得到答案：

| 变量 | 含义 | 计算方式 |
|------|------|----------|
| `max_kadane` | `k = 1` 时的最大子数组和 | Kadane |
| `total_sum` | 整个原数组的和 `S` | 累加 |
| `max_prefix` | 最大前缀和 | 从左到右累加，记录最大值 |
| `max_suffix` | 最大后缀和 | 从右到左累加，记录最大值 |

接下来分情况讨论：

- **全部为负数**：`max_kadane` 已经是 `0`（因为空子数组允许），其余两种情况也不会超过 `0`，答案为 `0`。  
- **`total_sum <= 0`**：完整复制的贡献不再增加，答案只能是 `max_kadane` 或 “前缀 + 后缀”。取二者最大。  
- **`total_sum > 0`**：完整复制会带来正向增长，答案可能是 `max_kadane`、`total_sum * k`、或 `max_prefix + max_suffix + (k-2)*total_sum`。取三者最大。

最后记得对 `10⁹+7` 取模。

#### 代码（Python）

```python
def kConcatenationMaxSum(arr, k):
    MOD = 10**9 + 7

    # ---------- 1️⃣ 计算一次遍历所需的四个值 ----------
    total_sum = 0          # 整个数组的和 S
    max_kadane = 0         # Kadane（k=1 时的最大子数组和），空子数组允许所以初始 0
    cur = 0                # Kadane 过程中的当前累计和

    max_prefix = float('-inf')   # 最大前缀和
    prefix_sum = 0

    for num in arr:
        # 累加得到 total_sum
        total_sum += num

        # Kadane 更新
        cur = max(0, cur + num)   # 若累计和为负则重置为 0
        max_kadane = max(max_kadane, cur)

        # 前缀和更新
        prefix_sum += num
        max_prefix = max(max_prefix, prefix_sum)

    # ---------- 2️⃣ 计算最大后缀和 ----------
    max_suffix = float('-inf')
    suffix_sum = 0
    for num in reversed(arr):
        suffix_sum += num
        max_suffix = max(max_suffix, suffix_sum)

    # ---------- 3️⃣ 根据不同情况取最大 ----------
    if k == 1:
        ans = max_kadane
    else:
        # 情形 A：仅在单个拷贝里
        ans = max_kadane

        # 情形 B：跨越多个完整拷贝（只在 total_sum 为正时才有意义）
        if total_sum > 0:
            ans = max(ans, total_sum * k)

        # 情形 C：首尾相接 + 中间若干完整拷贝
        # (k-2) 份完整拷贝的贡献可能为负，此时不取它（因为 max_prefix+max_suffix 已经包含了单拷贝的情况）
        ans = max(ans, max_prefix + max_suffix + max(0, total_sum) * (k - 2))

    # ---------- 4️⃣ 取模 ----------
    return ans % MOD
```

> **关键行中文注释**  
> - `cur = max(0, cur + num)` Kadane：累计和若为负则放弃，重新开始。  
> - `max_prefix = max(max_prefix, prefix_sum)` 记录从数组左端开始的最大累计和。  
> - `for num in reversed(arr):` 从右往左遍历得到后缀和。  
> - `max_prefix + max_suffix + max(0, total_sum) * (k - 2)` “前缀 + 后缀 + 中间完整拷贝的正贡献”。  
> - `if total_sum > 0: ans = max(ans, total_sum * k)` 只有整体和为正时，完整复制才会提升答案。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历原数组两遍（一次正向一次逆向），不随 `k` 增长。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干标量变量，和 `n` 无关。  

> 与暴力解相比，时间从 `O(n*k)` 降到了 `O(n)`，空间也从 `O(n*k)` 降到常数，完全满足题目最大 `10⁵` 的约束。

---  

## 心得  

- **核心技巧**：把“最大子数组和”拆成三类情况，利用 **前缀和、后缀和、整体和** 的组合，避免显式拼接数组。  
- **适用场景**：  
  1. **重复数组**（如 K-Concatenation、循环数组的最大子段）。  
  2. **需要跨区间的最大和**（如两段子数组最大和、环形数组最大子数组）。  
  3. **整体正负判断影响整体结构**（如求多次重复的最大收益）。  
- **一句话总结**：**先算出单拷贝的最大子数组、整体和、最大前缀、最大后缀，再根据整体和的正负在三种可能的组合中取最大**。

## 反思  

- **第一反应**：把数组复制 `k` 次后直接跑 Kadane。  
- **最容易踩的坑**：  
  - 忘记考虑 **空子数组**（答案可以为 0），导致在全负数时返回负值。  
  - 当 `k = 1` 时仍使用 “前缀+后缀+(k-2)*S” 公式，会出现 `k-2 = -1` 的错误。  
  - 对 **大数取模** 时忘记在乘法前先做模，可能导致 Python 整数溢出（虽然 Python 自动大整数，但会影响性能）。  
- **下次第一步**：先思考 “是否真的需要构造完整的重复序列？” 如果答案是 “不需要”，就立刻列出 **单拷贝的 Kadane、总和、前缀、后缀**，再依据整体和的正负划分情况求解。