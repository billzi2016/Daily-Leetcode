# #1787. 使所有子段的异或等于零 / Make the XOR of All Segments Equal to Zero

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/make-the-xor-of-all-segments-equal-to-zero/)

---

## 题目（英文原版）

**Description**

You are given an array nums​​​ and an integer k​​​​​. The XOR of a segment [left, right] where left <= right is the XOR of all the elements with indices between left and right, inclusive: nums[left] XOR nums[left+1] XOR ... XOR nums[right].
Return the minimum number of elements to change in the array such that the XOR of all segments of size k​​​​​​ is equal to zero.

**Examples**

**Example 1:**

```
Input: nums = [1,2,0,3,0], k = 1
Output: 3
Explanation: Modify the array from [1,2,0,3,0] to from [0,0,0,0,0].
```

**Example 2:**

```
Input: nums = [3,4,5,2,1,7,3,4,7], k = 3
Output: 3
Explanation: Modify the array from [3,4,5,2,1,7,3,4,7] to [3,4,7,3,4,7,3,4,7].
```

**Example 3:**

```
Input: nums = [1,2,4,1,2,5,1,2,6], k = 3
Output: 3
Explanation: Modify the array from [1,2,4,1,2,5,1,2,6] to [1,2,3,1,2,3,1,2,3].
```

**Constraints**

- 1 <= k <= nums.length <= 2000
- ​​​​​​0 <= nums[i] < 210

---

## 题目（中文翻译）

**题目描述**

给定一个数组 `nums` 和一个整数 `k`。长度为 `k` 的子段（segment）`[left, right]`（其中 `right - left + 1 = k` 且 `left ≤ right`）的异或（XOR）定义为下标从 `left` 到 `right` 的所有元素的异或值：

```
nums[left] XOR nums[left+1] XOR ... XOR nums[right]
```

返回要修改数组中最少的元素个数，使得 **所有长度为 `k` 的子段的异或均等于 0**。

**示例**

*示例 1*

```
输入: nums = [1,2,0,3,0], k = 1
输出: 3
解释: 将数组从 [1,2,0,3,0] 改为 [0,0,0,0,0]，共修改 3 个元素，使得每个长度为 1 的子段的异或为 0。
```

*示例 2*

```
输入: nums = [3,4,5,2,1,7,3,4,7], k = 3
输出: 3
解释: 将数组从 [3,4,5,2,1,7,3,4,7] 改为 [3,4,7,3,4,7,3,4,7]，共修改 3 个元素，使得所有长度为 3 的子段的异或为 0。
```

*示例 3*

```
输入: nums = [1,2,4,1,2,5,1,2,6], k = 3
输出: 3
解释: 将数组从 [1,2,4,1,2,5,1,2,6] 改为 [1,2,3,1,2,3,1,2,3]，共修改 3 个元素，使得所有长度为 3 的子段的异或为 0。
```

**约束条件**

- `1 ≤ k ≤ nums.length ≤ 2000`
- `0 ≤ nums[i] < 2^10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的修改方案都枚举一遍**，然后挑出改动最少且满足“所有长度为 `k` 的子段的 XOR 为 0” 的方案。  

- **枚举方式**：对数组中的每一个位置 `i`，我们可以把 `nums[i]` 改成 `0~2¹⁰‑1`（因为题目限制 `nums[i] < 2¹⁰`）中的任意一个数。  
- **检验条件**：枚举完以后，遍历所有长度为 `k` 的子段，计算它们的 XOR，检查是否全部为 `0`。  

> **类比**：这相当于把每个位置想象成一本字典里的词条，字典里有 `2¹⁰`（约 1024）个可能的解释。我们把每个词条的解释全部列出来，然后检查整本书的每一段话读出来的意思（XOR）是否全是“空”。  

**为什么它是正确的**：因为我们把**所有**合法的改法都穷举了，答案自然会在其中。  

**时间/空间复杂度**：  
- 对每个位置有 `2¹⁰` 种选择，数组长度最多 `2000`，所以枚举的总数是 `(2¹⁰)ⁿ`，即 `1024ⁿ`，这在任何实际数据下都是 **指数级** 的，根本不可接受。  
- 检查每一种方案需要遍历 `O(n·k)`（每个长度为 `k` 的子段），所以总时间是 `O( (2¹⁰)ⁿ · n·k )`。  
- 只需要保存当前枚举的数组，空间是 `O(n)`。  

> **大白话**：`O(1024ⁿ)` 就好比让 10 个人每人挑选 1024 种衣服穿一天，要算出所有人穿什么才能让大家的颜色都相同，根本不可能手算完。

#### 代码（Python）

```python
# 暴力枚举（仅作思想展示，实际会超时）
import itertools

def min_changes_bruteforce(nums, k):
    n = len(nums)
    INF = float('inf')
    best = INF

    # 所有可能的取值范围 0~1023
    candidates = list(range(1 << 10))

    # 对每一个位置的取值进行笛卡尔积枚举（指数级！）
    for new_vals in itertools.product(candidates, repeat=n):
        # 统计改动次数
        changes = sum(1 for i in range(n) if new_vals[i] != nums[i])

        # 若已经不比当前最优好，就直接跳过
        if changes >= best:
            continue

        # 检查所有长度为 k 的子段 XOR 是否为 0
        ok = True
        for left in range(n - k + 1):
            xr = 0
            for j in range(k):
                xr ^= new_vals[left + j]
            if xr != 0:
                ok = False
                break

        if ok:
            best = changes

    return best if best != INF else -1
```

> **关键行注释**：  
> - `itertools.product(..., repeat=n)` 产生所有可能的改法（指数级）。  
> - `xr ^= new_vals[left + j]` 用异或把子段的所有元素“合并”。  

#### 复杂度  

- **时间复杂度**：`O( (2¹⁰)ⁿ · n·k )` —— 指数级，根本不可行。  
- **空间复杂度**：`O(n)` —— 只保存一套枚举出来的数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **“每个位置可以任选 0~1023 中的值”** 这一步是导致指数爆炸的根源。我们需要利用题目给出的 **结构性约束** 来把搜索空间大幅压缩。

**关键观察 1**：  
如果所有长度为 `k` 的子段的 XOR 都为 `0`，那么相邻两个子段的 XOR 相等：

```
XOR(nums[i .. i+k-1]) = 0
XOR(nums[i+1 .. i+k]) = 0
```

两式相异（把相同的部分约掉）得到  

```
nums[i] XOR nums[i+k] = 0   →   nums[i] = nums[i+k]
```

> **类比**：把每个长度为 `k` 的子段想成一段“密码”。两个相邻的密码都是“全 0”，所以它们唯一的区别只能是首位和尾位相同——这就要求首位等于尾位。

**结论**：数组必须 **周期为 `k`**，即下标同余 `k` 的位置上必须相等。  

**关键观察 2**：  
设 `group[g] = { i | i % k == g }`（共 `k` 组），每组内部的所有元素必须统一成同一个数 `val[g]`。  
另外，**首 `k` 个数的 XOR 必须为 0**，即  

```
val[0] XOR val[1] XOR … XOR val[k-1] = 0
```

于是问题转化为：

> 为每个组 `g` 选一个数 `val[g]`（可以是 0~1023 中的任意值），  
> 使得 `val[0] ^ … ^ val[k-1] = 0`，且 **改动的元素总数最少**。

**如何计数改动**  
对第 `g` 组，记它的大小为 `size[g]`，以及每个数出现的次数 `freq[g][x]`（即该组里值为 `x` 的元素有多少个）。  
如果我们决定把整组改成 `x`，需要改动 `size[g] - freq[g][x]` 个元素（保留已经是 `x` 的那些）。  

**转化为 DP**  
我们把 “选了前 `i` 组后得到的 XOR 值” 当作状态：

```
dp[i][xor] = 前 i 组已经决定好，各自的值的 XOR = xor 时的最少改动次数
```

- 初始：`dp[0][0] = 0`（还没选任何组，XOR 为 0，改动 0 次），其他均为 INF。  
- 转移：遍历第 `i` 组的所有可能取值 `x`（只需要遍历出现过的 `x`，因为不存在的取值改动代价是 `size[i]`，等价于把 `freq=0` 的情况）。  

```
new_xor = xor ^ x
dp[i+1][new_xor] = min(dp[i+1][new_xor],
                       dp[i][xor] + size[i] - freq[i].get(x, 0))
```

- 最终答案：`dp[k][0]`（所有 `k` 组的 XOR 为 0 时的最少改动次数）。

**为什么时间可接受**  

- `k ≤ 2000`，`nums[i] < 2¹⁰`，所以 XOR 的取值范围只有 `0 … 1023`（共 1024 种）。  
- 对每一组，我们只遍历 **出现过的不同数**，而所有组出现的不同数之和 ≤ `n`（每个元素至多贡献一次）。  
- 因此总的状态转移次数 ≈ `1024 * n` ≤ `2·10⁶`，在一秒内轻松跑完。  

**空间优化**：只需要前一行 DP，使用一维数组滚动更新。

#### 代码（Python）

```python
from collections import Counter
from math import inf

def minChanges(nums, k):
    n = len(nums)
    # 1️⃣ 把下标同余 k 的位置划为同一组
    groups = []
    for r in range(k):
        # 取出所有下标 i % k == r 的元素
        grp = [nums[i] for i in range(r, n, k)]
        groups.append(grp)

    # 2️⃣ 预处理每组的频率表和大小
    freq = []          # freq[g][value] = 出现次数
    size = []          # 每组的元素个数
    for g in groups:
        cnt = Counter(g)          # Counter 本质是哈希表，类似“查字典”
        freq.append(cnt)
        size.append(len(g))

    # 3️⃣ 动态规划
    MAX_XOR = 1 << 10            # 2^10 = 1024
    dp = [inf] * MAX_XOR
    dp[0] = 0                    # 初始状态：0 组，XOR 为 0，改动 0

    for idx in range(k):
        ndp = [inf] * MAX_XOR    # 下一行 DP
        # 该组所有可能的取值（出现过的 + “全改成一个新数”）
        # 为了统一处理，把所有 0~1023 都遍历一次也可以，只是会多一些常数
        possible_vals = list(freq[idx].keys())
        # 还要考虑把整组改成一个根本没有出现的数的情况
        # 这等价于把 freq 当成 0，代价就是 size[idx]，我们在循环里直接处理
        for cur_xor in range(MAX_XOR):
            if dp[cur_xor] == inf:
                continue
            # ① 只改成已经出现的数
            for v in possible_vals:
                new_xor = cur_xor ^ v
                cost = size[idx] - freq[idx][v]   # 需要改动的元素数
                ndp[new_xor] = min(ndp[new_xor], dp[cur_xor] + cost)
            # ② 改成一个全新数（freq = 0），代价是 size[idx]
            # 这里我们只需要一次更新，因为对所有不在 possible_vals 的数代价相同
            # 只要把 dp[cur_xor] + size[idx] 与对应 new_xor（这里取任意 v）比较即可
            # 为了写得更直观，直接遍历所有 0~1023：
            for v in range(MAX_XOR):
                if v in freq[idx]:
                    continue          # 已在上面处理过
                new_xor = cur_xor ^ v
                ndp[new_xor] = min(ndp[new_xor], dp[cur_xor] + size[idx])
        dp = ndp

    return dp[0]            # 需要的最少改动次数
```

> **代码要点解释**  
> 1. `groups` 把数组按照下标模 `k` 分成 `k` 组，**哈希表**（`Counter`）记录每组里每个数出现了多少次，类似“查字典”。  
> 2. `dp[x]` 表示“已经处理完前几组，当前 XOR 为 `x` 时的最小改动”。  
> 3. 转移时 `cur_xor ^ v` 把新加入的组的值 `v` 合并进当前的异或结果。  
> 4. `size[idx] - freq[idx][v]` 正是把该组全部改成 `v` 需要改动的元素个数。  

**空间复杂度**：`O(2¹⁰)`（两个长度为 1024 的一维数组）——只跟数值范围有关，和 `n`、`k` 无关。  

**时间复杂度**：  
- 预处理 `O(n)`（遍历一次数组）。  
- DP 主循环：对每组遍历 `size_of_group_distinct_values`（所有组的总和 ≤ `n`） × `2¹⁰`（XOR 状态） → `O(n·2¹⁰)`，约 `2·10⁶` 步。  
- 因此整体 **时间 O(n·1024) ≈ O(n)**，空间 **O(1024)**，完全可以通过所有测试。

---

## 心得  

- **核心技巧**：利用相邻子段 XOR 为 0 推导出“相距 `k` 的元素必须相等”，把原本的 **全局约束** 转化为 **每组内部统一**，再通过 **动态规划** 在 1024 种 XOR 状态上做最小化。  
- **适用场景**：  
  1. “所有长度为 `k` 的子段 XOR 为常数” 类似的题目。  
  2. “把数组划分为若干等价类，使每类内部统一，同时满足全局异或/求和约束” 的问题。  
  3. “需要在有限取值范围（如 0~2¹⁰‑1）内选值，使得若干组的异或/和为目标值”的 DP。  
- **一句话总结**：**把“每段 XOR 为 0” 先化为 “相距 k 的元素相等”，再用 DP 在 1024 种异或状态中找最小改动**。  

---

## 反思  

- **第一反应**：直接想“遍历所有子段，逐个改”，导致了指数级的暴力思路。  
- **最容易踩的坑**：  
  - 忘记 **首 `k` 个数的 XOR 必须为 0**（仅保证相距 `k` 的相等还不足）。  
  - 在 DP 转移时遗漏了“把整组改成一个全新数”的情况（虽然代价等同于 `size`），可能导致答案偏大。  
  - 没有利用 **数值范围只有 0~1023**，导致状态空间被错误地设得太大。  
- **下次类似题目**：  
  1. 先**找出可以把全局约束拆成局部等价关系**（如相等、相同余数等）。  
  2. **统计每个等价类的频率**，把“改动次数”转化为“保留已有相同值的数量”。  
  3. 再用 **DP** 或 **贪心** 在有限取值空间里满足剩余的全局约束（如 XOR 为 0、和为目标值）。