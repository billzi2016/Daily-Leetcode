# #2281. **巫师的总力量之和** / Sum of Total Strength of Wizards

> 难度：困难 · 标签：Array、Stack、Monotonic Stack、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sum-of-total-strength-of-wizards/)

---

## 题目（英文原版）

**Description**

As the ruler of a kingdom, you have an army of wizards at your command.
You are given a 0-indexed integer array strength, where strength[i] denotes the strength of the ith wizard. For a contiguous group of wizards (i.e. the wizards' strengths form a subarray of strength), the total strength is defined as the product of the following two values:
Return the sum of the total strengths of all contiguous groups of wizards. Since the answer may be very large, return it modulo 109 + 7.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: strength = [1,3,1,2]
Output: 44
Explanation: The following are all the contiguous groups of wizards:
- [1] from [1,3,1,2] has a total strength of min([1]) * sum([1]) = 1 * 1 = 1
- [3] from [1,3,1,2] has a total strength of min([3]) * sum([3]) = 3 * 3 = 9
- [1] from [1,3,1,2] has a total strength of min([1]) * sum([1]) = 1 * 1 = 1
- [2] from [1,3,1,2] has a total strength of min([2]) * sum([2]) = 2 * 2 = 4
- [1,3] from [1,3,1,2] has a total strength of min([1,3]) * sum([1,3]) = 1 * 4 = 4
- [3,1] from [1,3,1,2] has a total strength of min([3,1]) * sum([3,1]) = 1 * 4 = 4
- [1,2] from [1,3,1,2] has a total strength of min([1,2]) * sum([1,2]) = 1 * 3 = 3
- [1,3,1] from [1,3,1,2] has a total strength of min([1,3,1]) * sum([1,3,1]) = 1 * 5 = 5
- [3,1,2] from [1,3,1,2] has a total strength of min([3,1,2]) * sum([3,1,2]) = 1 * 6 = 6
- [1,3,1,2] from [1,3,1,2] has a total strength of min([1,3,1,2]) * sum([1,3,1,2]) = 1 * 7 = 7
The sum of all the total strengths is 1 + 9 + 1 + 4 + 4 + 4 + 3 + 5 + 6 + 7 = 44.
```

**Example 2:**

```
Input: strength = [5,4,6]
Output: 213
Explanation: The following are all the contiguous groups of wizards: 
- [5] from [5,4,6] has a total strength of min([5]) * sum([5]) = 5 * 5 = 25
- [4] from [5,4,6] has a total strength of min([4]) * sum([4]) = 4 * 4 = 16
- [6] from [5,4,6] has a total strength of min([6]) * sum([6]) = 6 * 6 = 36
- [5,4] from [5,4,6] has a total strength of min([5,4]) * sum([5,4]) = 4 * 9 = 36
- [4,6] from [5,4,6] has a total strength of min([4,6]) * sum([4,6]) = 4 * 10 = 40
- [5,4,6] from [5,4,6] has a total strength of min([5,4,6]) * sum([5,4,6]) = 4 * 15 = 60
The sum of all the total strengths is 25 + 16 + 36 + 36 + 40 + 60 = 213.
```

**Constraints**

- 1 <= strength.length <= 105
- 1 <= strength[i] <= 109

---

## 题目（中文翻译）

你是王国的统治者，麾下拥有一支由巫师组成的军队。  
给定一个下标从 **0** 开始的整数数组 `strength`，其中 `strength[i]` 表示第 `i` 位巫师的力量。对于任意一个连续的巫师子群（即数组 `strength` 的一个子数组（subarray）），其 **总力量** 定义为下面两项的乘积：

- 该子数组中的最小力量 `min(subarray)`
- 该子数组中所有力量的和 `sum(subarray)`

求所有可能的连续子数组的 **总力量** 之和。由于答案可能非常大，返回结果对 `10^9 + 7` 取模后的值。

> **子数组（subarray）** 是数组中一个连续且非空的元素序列。

### 示例

#### 示例 1
```text
输入: strength = [1,3,1,2]
输出: 44
解释: 所有连续子数组及其总力量如下：
- [1] → min=1, sum=1, total=1*1=1
- [3] → min=3, sum=3, total=3*3=9
- [1] → min=1, sum=1, total=1*1=1
- [2] → min=2, sum=2, total=2*2=4
- [1,3] → min=1, sum=4, total=1*4=4
- [3,1] → min=1, sum=4, total=1*4=4
- [1,2] → min=1, sum=3, total=1*3=3
- [1,3,1] → min=1, sum=5, total=1*5=5
- [3,1,2] → min=1, sum=6, total=1*6=6
- [1,3,1,2] → min=1, sum=7, total=1*7=7
所有总力量相加得到 44。
```

#### 示例 2
```text
输入: strength = [5,4,6]
输出: 213
解释: 所有连续子数组及其总力量如下：
- [5] → min=5, sum=5, total=5*5=25
- [4] → min=4, sum=4, total=4*4=16
- [6] → min=6, sum=6, total=6*6=36
- [5,4] → min=4, sum=9, total=4*9=36
- [4,6] → min=4, sum=10, total=4*10=40
- [5,4,6] → min=4, sum=15, total=4*15=60
所有总力量相加得到 213。
```

### 约束条件
- `1 <= strength.length <= 10^5`
- `1 <= strength[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

> **最直接的想法**：枚举所有连续子数组，求出每个子数组的最小值 `min` 与元素和 `sum`，把 `min * sum` 累加起来。  

- **用到的数据结构**：  
  - **数组**本身：我们只需要遍历它。  
  - **双层循环**：外层固定子数组的左端点 `l`，内层把右端点 `r` 从 `l` 向右推进，同时维护当前子数组的最小值和总和。  
- **为什么正确**：因为题目要求“所有连续子数组的 `min * sum` 的和”，只要把每一种可能的子数组都算一遍，就一定得到正确答案。  
- **时间/空间复杂度**：  
  - **时间**：外层 `l` 有 `n` 种取法，内层 `r` 最多也会遍历 `n` 次（每次右移一步），于是总共大约是 `n × n = n²` 次操作。  
    - **大白话**：如果 `n = 10⁴`，那么需要做一亿次运算，普通电脑跑几秒甚至更久就会超时。  
  - **空间**：只用了常数个额外变量（最小值、前缀和等），所以是 `O(1)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def total_strength_bruteforce(strength):
    n = len(strength)
    ans = 0
    # 枚举左端点
    for l in range(n):
        cur_min = strength[l]          # 当前子数组的最小值
        cur_sum = 0                    # 当前子数组的元素和
        # 右端点向右扩展
        for r in range(l, n):
            cur_sum += strength[r]                 # 累加新加入的元素
            cur_min = min(cur_min, strength[r])    # 更新最小值
            ans = (ans + cur_min * cur_sum) % MOD   # 累加子数组的贡献
    return ans
```

> **关键行解释**  
> - `cur_min = min(cur_min, strength[r])`：相当于在“检查这段子数组里最弱的巫师”。  
> - `ans = (ans + cur_min * cur_sum) % MOD`：把每个子数组的“力量”累加进答案，并取模防止整数爆炸。

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每对 `(l, r)` 都要访问一次。  
- **空间复杂度**：`O(1)` —— 只用了几个临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈**在于我们每次都要重新遍历子数组来求最小值。  
如果能够 **直接算出每个元素在多少个子数组里是最小值**，并把这些子数组的 `sum` 也一次性算出来，就能把 `O(n²)` 降到 `O(n)`。

**核心思路：贡献法 + 单调栈 + 前缀和**  

1. **把注意力放在单个巫师上**  
   - 假设第 `i` 位的巫师强度为 `a[i]`。  
   - 只要找出所有**以 `a[i]` 为最小值**的子数组，我们就可以把这些子数组的贡献一次性算完。  

2. **用单调栈找左右边界**  
   - 对每个位置 `i`，找出左边最近的**比 `a[i]` 更小**的下标 `L`（不存在时记作 `-1`），以及右边最近的**更小**的下标 `R`（不存在时记作 `n`）。  
   - 那么，**所有**以 `i` 为最小值的子数组的左端点只能在 `(L, i]`，右端点只能在 `[i, R)`。  
   - 这一步只需要一次 **单调递增栈**（栈里存下标），时间 `O(n)`。

3. **前缀和 & 前缀前缀和**  
   - 为了快速求子数组的元素和，我们先算普通前缀和 `pre[i] = a[0] + … + a[i]`（1‑索引更方便）。  
   - 再算 **前缀前缀和** `pre2[i] = pre[1] + … + pre[i]`。  
   - 有了这两个数组，**任意区间 `[l, r]` 的所有子数组的元素和之和** 能在 `O(1)` 内算出（推导见下面的公式）。  

4. **贡献公式**（使用 1‑索引，方便写）  

   设  
   - `i` 为当前元素（1‑索引），`L` 为左边界下标（`L < i`），`R` 为右边界下标（`R > i`）。  
   - `cntL = i - L`（左侧可以选多少种左端点）  
   - `cntR = R - i`（右侧可以选多少种右端点）  

   对于所有左端点 `l ∈ (L, i]`，右端点 `r ∈ [i, R)`，子数组的 **和** 为 `sum(l, r) = pre[r] - pre[l-1]`。  
   把 `a[i]` 乘进去得到贡献：

   \[
   \text{contrib}_i = a[i] \times
   \Big[
   cntL \times (pre2[R-1] - pre2[i-1]) \;
   -\; cntR \times (pre2[i-1] - pre2[L-1])
   \Big] \pmod{M}
   \]

   - `pre2[R-1] - pre2[i-1]` 实际上是 **所有右端点在 `[i, R-1]` 的前缀和之和**。  
   - `pre2[i-1] - pre2[L-1]` 是 **所有左端点在 `(L, i-1]` 的前缀和之和**。  

   乘上 `cntL`、`cntR` 再相减，就正好把每一种合法的 `(l, r)` 计入一次。  

5. **把所有位置的贡献加起来**，再取模即得答案。

> **为什么是 O(n)？**  
> - 单调栈遍历一次得到所有 `L、R`（`O(n)`）。  
> - 前缀和、前缀前缀和各一次线性遍历（`O(n)`）。  
> - 最后遍历每个位置计算公式（`O(n)`）。  
> 所有步骤都是线性的，整体 `O(n)`，空间只需要几倍大小的数组，`O(n)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def total_strength(strength):
    n = len(strength)
    a = [0] + strength                # 1-indexed, a[1]~a[n]

    # ---------- 1. 单调栈求左、右边界 ----------
    left = [0] * (n + 1)   # left[i] = 最近的更小元素的下标，若不存在为 0
    right = [n + 1] * (n + 1)  # right[i] = 最近的更小元素的下标，若不存在为 n+1

    stack = []
    # 求左边界（严格小于）
    for i in range(1, n + 1):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else 0
        stack.append(i)

    stack.clear()
    # 求右边界（严格小于），从右往左遍历更直观
    for i in range(n, 0, -1):
        while stack and a[stack[-1]] >= a[i]:   # 注意这里要 >=，保证右边界是第一个更小的
            stack.pop()
        right[i] = stack[-1] if stack else n + 1
        stack.append(i)

    # ---------- 2. 前缀和、前缀前缀和 ----------
    pre = [0] * (n + 1)      # pre[i] = a[1] + ... + a[i]
    for i in range(1, n + 1):
        pre[i] = (pre[i - 1] + a[i]) % MOD

    pre2 = [0] * (n + 1)     # pre2[i] = pre[1] + ... + pre[i]
    for i in range(1, n + 1):
        pre2[i] = (pre2[i - 1] + pre[i]) % MOD

    # ---------- 3. 逐个位置累计贡献 ----------
    ans = 0
    for i in range(1, n + 1):
        L = left[i]
        R = right[i]

        cntL = i - L          # 左侧可以选多少种左端点
        cntR = R - i          # 右侧可以选多少种右端点

        # 下面的式子全部取模，防止负数
        sum_right = (pre2[R - 1] - pre2[i - 1]) % MOD
        sum_left  = (pre2[i - 1] - pre2[L - 1]) % MOD

        contrib = (cntL * sum_right - cntR * sum_left) % MOD
        contrib = (contrib * a[i]) % MOD

        ans = (ans + contrib) % MOD

    return ans
```

> **关键行解释**  
> - `while stack and a[stack[-1]] > a[i]:`：栈里保持**递增**，弹出比当前大的元素，从而得到左侧最近的更小值。  
> - `right[i] = stack[-1] if stack else n + 1`：右侧的最近更小元素，如果不存在则设为 `n+1`（相当于数组右边的哨兵）。  
> - `pre2[i] = (pre2[i - 1] + pre[i]) % MOD`：这里的 `pre2` 是“前缀前缀和”，帮助我们在 O(1) 内求 **所有右端点的前缀和之和**。  
> - `contrib = (cntL * sum_right - cntR * sum_left) % MOD`：公式的核心——左侧选择数乘以右侧前缀和之和，减去右侧选择数乘以左侧前缀和之和。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 单调栈一次遍历、前缀和两次遍历、最终遍历一次，总共是线性时间。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **近 `n` 倍**（当 `n = 10⁵` 时，能在毫秒级完成）。  

- **空间复杂度**：`O(n)`  
  - 需要额外的数组 `left、right、pre、pre2`，每个长度 `n+1`。  
  - 只用了线性额外空间，符合题目对 `n ≤ 10⁵` 的要求。

---

## 心得  

- **核心技巧**：**单调栈 + 前缀前缀和的贡献法**。  
  - 单调栈帮助我们快速定位每个元素作为「最小值」的左右有效区间。  
  - 前缀前缀和把「所有子数组的元素和」转化为常数时间查询。  
- **适用的题型**（类似思路）  
  1. **子数组最小值之和**（LeetCode 907）  
  2. **子数组最大值之和**（类似的单调栈求左右界）  
  3. **子数组乘积或和的区间贡献**（需要前缀积或前缀和的二次前缀）  
- **一句话总结解题钥匙**：**把「每个元素是最小值」的所有子数组一次性算完，而不是一个子数组一个子数组地枚举。**

---

## 反思  

- **第一反应**：看到 `min * sum`，立刻想到「枚举子数组」——这就是暴力解的思路。  
- **最容易踩的坑**  
  - **边界处理**：左、右边界的哨兵要设为 `0`、`n+1`，并且在计算 `pre2` 时要防止负数取模。  
  - **单调栈的比较符号**：左边界用 `>`，右边界用 `>=`，保证每个子数组的最小值只被唯一的一个位置计数。  
  - **大数取模**：在 `cntL * sum_right - cntR * sum_left` 这一步可能出现负数，必须先 `% MOD` 再加 `MOD` 再 `% MOD`，否则 Python 会得到负数导致最终答案错误。  
- **下次类似题目第一步**：**先思考「贡献」**——哪个元素在多少个子结构里起关键作用？随后寻找 **单调栈** 或 **前缀结构** 来快速统计这些贡献。这样往往能把暴力的二次时间直接降到线性。