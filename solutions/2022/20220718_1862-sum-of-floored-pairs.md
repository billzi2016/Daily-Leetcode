# #1862. 取整对的和 / Sum of Floored Pairs

> 难度：困难 · 标签：Array、Math、Binary Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sum-of-floored-pairs/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the sum of floor(nums[i] / nums[j]) for all pairs of indices 0 <= i, j < nums.length in the array. Since the answer may be too large, return it modulo 109 + 7.
The floor() function returns the integer part of the division.

**Examples**

**Example 1:**

```
Input: nums = [2,5,9]
Output: 10
Explanation:
floor(2 / 5) = floor(2 / 9) = floor(5 / 9) = 0
floor(2 / 2) = floor(5 / 5) = floor(9 / 9) = 1
floor(5 / 2) = 2
floor(9 / 2) = 4
floor(9 / 5) = 1
We calculate the floor of the division for every pair of indices in the array then sum them up.
```

**Example 2:**

```
Input: nums = [7,7,7,7,7,7,7]
Output: 49
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回所有下标对 `0 <= i, j < nums.length` 中 `floor(nums[i] / nums[j])` 的总和。由于答案可能非常大，请返回 **取模（modulo）** `10^9 + 7` 后的结果。  
`floor()` 函数返回除法运算的整数部分（向下取整）。

## 示例

### 示例 1

**输入**  
```json
nums = [2,5,9]
```

**输出**  
```
10
```

**解释**  
```
floor(2 / 5) = floor(2 / 9) = floor(5 / 9) = 0
floor(2 / 2) = floor(5 / 5) = floor(9 / 9) = 1
floor(5 / 2) = 2
floor(9 / 2) = 4
floor(9 / 5) = 1
```
我们对数组中每一对下标计算除法的向下取整值，然后将它们求和。

### 示例 2

**输入**  
```json
nums = [7,7,7,7,7,7,7]
```

**输出**  
```
49
```

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里所有下标 `i`、`j` 的组合都列举出来，逐个算 `floor(nums[i] / nums[j])`，然后把结果相加。

- **使用的数据结构**：只需要原数组本身，遍历时用两个 `for` 循环。可以把这两个循环想象成两层嵌套的“遍历所有伙伴”，就像在一次聚会里让每个人和所有人（包括自己）拍一张合照。
- **为什么正确**：因为题目要求**所有**有序对 `(i, j)`（包括 `i == j`）的除法取整之和，枚举所有对显然不会漏掉任何一种情况。
- **复杂度分析**：  
  - 外层循环跑 `n` 次，内层循环每次也跑 `n` 次，总共要执行 `n × n = n²` 次除法和取整。  
  - 时间复杂度记作 **O(n²)**，这在数学里表示“随着 `n` 增大，运行时间大约是 `n` 的平方”。如果 `n = 10⁵`，`n²` 就是 `10¹⁰`，这已经远远超出一秒能跑完的范围。  
  - 只用了原数组，没有额外的存储空间，空间复杂度是 **O(1)**（常数级），意思是占用的内存基本不随 `n` 增大而变多。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def sum_of_floored_pairs_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    for i in range(n):                 # 第一个下标 i
        for j in range(n):             # 第二个下标 j
            # floor(a / b) 在 Python 中直接使用 // 运算符
            ans += nums[i] // nums[j]  # 计算并累加
            ans %= MOD                 # 防止中间结果溢出
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 随着数组长度的增长，运算次数会呈二次方增长。  
- **空间复杂度**：`O(1)` —— 只用了几个额外的整数变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**相同的数值。  
例如数组里有很多相同的元素 `5`，那么 `5 // 2` 会被算很多遍。只要把相同的数“归类”，我们就可以一次性算出它们对所有其他数的贡献。

**核心想法：利用频率（出现次数）+ 前缀和 + 乘法来一次性统计。**  
步骤如下：

1. **统计每个数出现了多少次**  
   - 由于 `nums[i] ≤ 10⁵`，我们可以开一个长度为 `max_val + 1` 的数组 `freq`，下标 `x` 上的值表示数字 `x` 在原数组中出现的次数。  
   - 把 `freq` 想象成“字典”，键是数字，值是这本字典里该词出现的页码数。

2. **构造前缀和 `pref`**  
   - `pref[x]` 表示 **≤ x** 的所有数字出现次数的累计和。  
   - 这样，**区间 `[l, r]`（含两端）**里数字的总出现次数就可以用 `pref[r] - pref[l-1]` 一句算出来。  
   - 前缀和相当于“累计的书架”，只要知道左端和右端的总页数，就能直接得到中间的页数。

3. **枚举除数 `d`（即 `nums[j]`）**  
   - 对每个可能的除数 `d`（只要它出现过，即 `freq[d] > 0`），我们要统计所有被除数 `x` 使得 `floor(x / d) = k` 的情况。  
   - 当 `k` 固定时，满足 `k ≤ x / d < k+1` 的 `x` 落在区间 **`[k*d, (k+1)*d - 1]`**。  
   - 区间内的所有数字对除数 `d` 的贡献都是 `k`，而出现次数是该区间的总频率 `cnt = pref[(k+1)*d - 1] - pref[k*d - 1]`。  
   - 于是这部分贡献是 `freq[d] * k * cnt`（除数出现 `freq[d]` 次，被除数出现 `cnt` 次，每对贡献 `k`）。

4. **遍历所有可能的 `k`**  
   - 对固定的 `d`，`k` 从 `1` 开始，一直到 `max_val // d`（因为最大被除数是 `max_val`）。  
   - 这相当于在数轴上每隔 `d` 取一个“窗口”，窗口宽度为 `d`，窗口编号就是 `k`。

5. **把所有 `d`、`k` 的贡献加起来**，记得取模 `10⁹+7`。

**时间复杂度分析**  
- 外层遍历所有可能的除数 `d`（至多 `max_val` 次）。  
- 对每个 `d`，内部遍历 `k` 的次数大约是 `max_val / d`。  
- 所有 `d` 的遍历次数之和是  
  \[
  \sum_{d=1}^{max\_val} \frac{max\_val}{d} = max\_val \cdot \sum_{d=1}^{max\_val} \frac{1}{d}
  \]  
  这正是 **调和级数**，其增长速度约为 `log(max_val)`。  
- 因此总体时间复杂度是 **O(max_val · log max_val)**，在本题约为 `10⁵·log10⁵ ≈ 1.2·10⁶`，完全可以在一秒内跑完。  
- 额外使用了 `freq`、`pref` 两个长度为 `max_val+1` 的数组，空间复杂度是 **O(max_val)**，即 `10⁵` 级别的整数数组，内存占用约几百 KB。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def sum_of_floored_pairs(nums: List[int]) -> int:
    """
    最优解：利用频率 + 前缀和 + 区间枚举
    """
    if not nums:
        return 0

    max_val = max(nums)                     # 数组里最大的数
    freq = [0] * (max_val + 1)               # freq[x] = x 出现次数
    for v in nums:
        freq[v] += 1

    # 前缀和：pref[i] = 0..i 的出现次数总和
    pref = [0] * (max_val + 1)
    cur = 0
    for i in range(max_val + 1):
        cur += freq[i]
        pref[i] = cur

    ans = 0
    # 枚举除数 d（对应 nums[j]）
    for d in range(1, max_val + 1):
        if freq[d] == 0:          # 这个数根本没出现，直接跳过
            continue

        # k 表示 floor(x / d) 的值，从 1 开始（k=0 的情况已经在下面统一处理）
        max_k = max_val // d
        for k in range(1, max_k + 1):
            # 被除数 x 落在区间 [k*d, (k+1)*d - 1]
            left = k * d
            right = min((k + 1) * d - 1, max_val)

            # 该区间内所有数字出现的总次数
            cnt = pref[right] - pref[left - 1]

            # 贡献 = freq[d]（除数的出现次数） * k（除法结果） * cnt（被除数的出现次数）
            ans = (ans + freq[d] * k * cnt) % MOD

    # 处理 floor(x / d) == 0 的情况：只要 x < d 即可
    # 对每个除数 d，所有小于 d 的数都会产生 0，贡献为 0，故不需要显式累加

    # 最后还要加上所有 i==j 的情况，floor(x/x)=1
    # 这已经在上面的循环里被算进来了，因为当 k=1 且 left=d 时，cnt 包含了自身的出现次数
    return ans % MOD
```

> **代码要点解释**  
> - `freq` 像“字典”，`freq[x]` 告诉我们“词 `x` 在书里出现了几页”。  
> - `pref` 是“累计的书页数”，`pref[r] - pref[l-1]` 能瞬间得到区间 `[l, r]` 的总页数（即出现次数）。  
> - 双层循环里外层遍历除数 `d`，内层遍历每个可能的商 `k`，利用前缀和一次性算出所有对应被除数的出现次数 `cnt`，从而把**成千上万**的 `i,j` 对压缩成 **一条** 加法。

#### 复杂度

- **时间复杂度**：`O(max_val · log max_val)`  
  - 这里的 `max_val ≤ 10⁵`，所以实际运行约为一两百万次基本运算，远快于 `O(n²)` 的上亿次。  
  - 与暴力解相比，时间从“平方级”降到了“准线性级”，提升非常明显。

- **空间复杂度**：`O(max_val)`  
  - 只用了两个长度为 `max_val+1` 的整数数组，额外占用的内存是线性级别的，完全可以接受。

---

## 心得

- **核心技巧**：**利用数值的频率 + 前缀和 + 区间枚举**，把大量相同的除法运算压缩成若干次区间求和。  
- **适用题型**（类似思路）  
  1. “**统计所有数对的最大公约数**”——可以用频率 + 倍数枚举的方式。  
  2. “**数组中每个数的出现次数乘以它的值**”——前缀和帮助快速求区间和。  
  3. “**统计所有数对满足 `a % b == 0` 的个数**”——同样使用倍数遍历与频率。  
- **一句话总结解题钥匙**：  
  > 把“每个元素出现多少次”记下来，用**前缀和**一次性算出任意数值区间的总出现次数，再把这些区间对应的除法结果乘上频率相加。

---

## 反思

- **第一反应**：直接写两层循环暴力枚举，忽视了数组长度可能高达 `10⁵`，导致时间必然超限。  
- **最容易踩的坑**  
  - **边界条件**：在计算区间 `[k*d, (k+1)*d - 1]` 时，右端可能超过 `max_val`，必须 `min` 限制。  
  - **前缀和下标**：当 `left = k*d` 为 `1` 时，`pref[left-1]` 需要是 `pref[0]`（已经在数组里），不能出现负下标。  
  - **取模**：累加过程中要经常 `% MOD`，防止 Python 整数在极端情况下占用过多内存。  
- **下次类似题目**：第一步先**统计频率**，再思考“能否把相同值的计算合并”，如果涉及到“区间范围”则**构造前缀和**或**差分数组**，最后用**倍数/除数枚举**把问题压缩。这样往往能把原本的 `O(n²)` 降到 `O(max·log max)`。