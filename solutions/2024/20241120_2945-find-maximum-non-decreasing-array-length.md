# #2945. 寻找最大非递减数组长度 / Find Maximum Non-decreasing Array Length

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Stack、Queue、Monotonic Stack、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/find-maximum-non-decreasing-array-length/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
You can perform any number of operations, where each operation involves selecting a subarray of the array and replacing it with the sum of its elements. For example, if the given array is [1,3,5,6] and you select subarray [3,5] the array will convert to [1,8,6].
Return the maximum length of a non-decreasing array that can be made after applying operations.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [5,2,2]
Output: 1
Explanation: This array with length 3 is not non-decreasing.
We have two ways to make the array length two.
First, choosing subarray [2,2] converts the array to [5,4].
Second, choosing subarray [5,2] converts the array to [7,2].
In these two ways the array is not non-decreasing.
And if we choose subarray [5,2,2] and replace it with [9] it becomes non-decreasing. 
So the answer is 1.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 4
Explanation: The array is non-decreasing. So the answer is 4.
```

**Example 3:**

```
Input: nums = [4,3,2,6]
Output: 3
Explanation: Replacing [3,2] with [5] converts the given array to [4,5,6] that is non-decreasing.
Because the given array is not non-decreasing, the maximum possible answer is 3.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。  

你可以执行任意次数的操作，每次操作选择数组的一个子数组（subarray），并用该子数组所有元素的和来替换它。例如，若数组为 `[1,3,5,6]`，选择子数组 `[3,5]` 后，数组会变为 `[1,8,6]`。  

返回在进行任意次数操作后，能够得到的非递减数组（non-decreasing array）的最大长度。  

**子数组** 是数组中连续的、非空的元素序列。

---

### 示例

#### 示例 1
> **Input:** `nums = [5,2,2]`  
> **Output:** `1`  
> **Explanation:**  
> 原数组长度为 3，但不是非递减的。我们可以将数组长度缩减到 2 的两种方式如下：  
> 1. 选择子数组 `[2,2]`，数组变为 `[5,4]`。  
> 2. 选择子数组 `[5,2]`，数组变为 `[7,2]`。  
> 这两种情况下数组仍然不是非递减的。  
> 若选择子数组 `[5,2,2]` 并用其和 `[9]` 替换，数组变为 `[9]`，此时已经是非递减的。  

#### 示例 2
> **Input:** `nums = [1,2,3,4]`  
> **Output:** `4`  
> **Explanation:**  
> 原数组已经是非递减的，因此答案为 4。  

#### 示例 3
> **Input:** `nums = [4,3,2,6]`  
> **Output:** `3`  
> **Explanation:**  
> 将子数组 `[3,2]` 替换为其和 `[5]` 后，数组变为 `[4,5,6]`，此时是非递减的。由于原数组不是非递减的，能够得到的最大长度为 3。  

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把「把一个子数组替换成它的和」想象成「把相邻的几块砖砸在一起，变成一块重量等于它们重量之和的砖」。  
砸完以后，剩下的砖（即数组元素）必须从左到右重量 **不减**，我们想保留尽可能多的砖。  

于是这道题可以等价地描述为：

> 把原数组 **划分成若干个连续的区间**（每个区间代表一次砸砖），  
> 要求这些区间的 **区间和** 按出现顺序是非递减的，  
> 求能得到的 **最多区间数**（即保留下来的元素个数）。

最直接的做法就是 **枚举所有可能的划分**，检查哪一种满足「区间和非递减」且区间数最多。  

- **数据结构**：我们只需要数组本身和前缀和（`pref[i] = nums[0] + … + nums[i‑1]`），前缀和相当于一本「累计重量表」，可以在 `O(1)` 时间内算出任意区间的和。  
  前缀和就像查字典：**key** 是区间的左端点，**value** 是从数组开头到左端点前的累计和。

- **正确性**：遍历所有划分肯定能找到最优的那一种，因为「最优」本身是所有可能划分中的一个。

- **时间/空间复杂度**：  
  - 枚举划分的过程相当于在 `n‑1` 条「切割线」中挑选若干条，组合数是指数级的 `2^(n‑1)`（每条切割线要么保留要么删掉）。  
  - 这相当于 **O(2ⁿ)**，在最坏情况下大约是 `2^100000`，根本不可能跑完。  
  - 空间只用了前缀和数组 `O(n)`。

> **大白话**：  
> `O(2ⁿ)` 就像在玩「从 100 个人里挑出若干人」的游戏，一次只能挑一个，所有可能的挑法数目会爆炸到天文数字，根本不可能把它们都尝试一遍。

#### 代码（Python）

```python
from itertools import product
from typing import List

def max_len_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # 前缀和，pref[i] = nums[0] + … + nums[i-1]
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + nums[i]

    best = 1                     # 至少可以把全部砸成一块
    # 在 n-1 条切割线之间枚举是否「切」：0=不切（合并），1=切
    for mask in product([0, 1], repeat=n - 1):
        seg_sums = []            # 保存每段的和
        left = 0                 # 当前段的左端点（下标）
        ok = True
        for i, cut in enumerate(mask, start=1):
            if cut:               # 在 i-1 和 i 之间切开
                seg_sums.append(pref[i] - pref[left])
                left = i
        # 最后一段
        seg_sums.append(pref[n] - pref[left])

        # 检查是否非递减
        for a, b in zip(seg_sums, seg_sums[1:]):
            if a > b:
                ok = False
                break
        if ok:
            best = max(best, len(seg_sums))
    return best
```

> 这段代码只能在 `n ≤ 15` 左右的小样例上跑通，用来帮助大家**理解除题本质**，并不是正式解法。

#### 复杂度  

- 时间复杂度：**O(2ⁿ)**（指数级）——每条切割线有两种选择，所有选择的乘积。  
- 空间复杂度：**O(n)**——前缀和数组占 `n+1` 的空间，递归/遍历本身只用常数额外空间。

---

### 2. 最优解  

#### 思路  

把问题重新表述为「**划分成最多的区间，使得每个区间的和非递减**」后，核心就变成了**动态规划 + 前缀和 + 单调性**。

设  

- `pref[i]` 为前缀和（同上），  
- `dp[i]` 为**考虑前 i 个元素（即下标 `[0, i)`）**时，能够得到的**最大区间数**。  
- 对应的**最后一个区间的和**记作 `last[i]`，我们只关心**最小可能的** `last[i]`，因为「最后的和越小」对后面继续划分越有利。

转移方程：

> 想把第 `i` 个元素（下标 `i-1`）放进一个新区间。  
> 那么我们需要找一个切点 `j < i`，使得  
> - 前 `j` 个元素已经划分好了，得到 `dp[j]` 个区间，且它们的最后一个区间和为 `last[j]`（已经是最小值），  
> - 新区间的和 `pref[i] - pref[j]` **不小于** `last[j]`（保证非递减）。  
> 在满足条件的所有 `j` 中，取 `dp[j] + 1` 的最大值，即得到 `dp[i]`。  

公式：

```
dp[i] = max{ dp[j] + 1 | 0 ≤ j < i 且 pref[i] - pref[j] ≥ last[j] }
```

#### 关键观察：单调性  

把不等式 `pref[i] - pref[j] ≥ last[j]` 移项得到  

```
pref[i] ≥ pref[j] + last[j]                (1)
```

右侧 `pref[j] + last[j]` 只和 `j` 有关，记作 `threshold[j]`。  
对每个 `j`，只要当前的前缀和 `pref[i]` **不小于** `threshold[j]`，就可以把 `j` 位置的最优划分「接”上”」到 `i`。

于是 **我们只需要在所有已经出现的 `threshold` 中，找出 ≤ `pref[i]` 的最大 `dp` 值**。  
这正好是「**前缀最大查询**」的问题：  
- 维护一组点 `(threshold, dp)`，  
- 对每个新来的 `pref[i]`，查询 `threshold ≤ pref[i]` 区间的最大 `dp`。  

这可以用**离线坐标压缩 + 树状数组（Fenwick Tree）**或**线段树**在 `O(log n)` 时间内完成。

#### 具体步骤  

1. **预处理前缀和** `pref[0…n]`（长度为 `n+1`）。  
2. **动态规划数组** `dp[0] = 0`（空前缀划分成 0 段），`last[0] = 0`（为了让式 (1) 成立，设阈值为 0）。  
3. **建立容器**  
   - 把所有可能出现的 `threshold = pref[j] + last[j]` 收集起来，和所有 `pref[i]` 一起做坐标压缩。  
   - 使用 Fenwick 树 `bit`，其中 `bit[pos]` 保存「所有阈值 ≤ 该坐标的最大 `dp` 值」。  
4. **遍历 i = 1 … n**  
   - **查询**：`best = bit.query(idx_of(pref[i]))`，得到满足 (1) 的最大 `dp`。  
   - **更新**：`dp[i] = best + 1`。  
   - **计算本段的最小 possible last sum**：  
     - 这里我们只需要一种「最小」的 `last[i]`，它正好是 `pref[i] - pref[pos]`，其中 `pos` 是让 `best` 成立的那个 `j`。  
     - 为了在后续仍然保持最小，我们**只记录** `last[i] = pref[i] - pref[i-1]`（即把第 i‑1 个元素单独成段）**或者**更小的值。  
       实际上，只要把 `last[i]` 设为 `pref[i] - pref[i-1]`（最小可能的单元素和），对应的 `threshold = pref[i] + last[i]` 仍然是合法的上界。  
   - **插入新阈值**：`new_thr = pref[i] + last[i]`，在 Fenwick 树对应位置写入 `dp[i]`（取最大）。  

5. 最终答案是 `max(dp)`，即 `dp[n]`（因为我们遍历到了整个数组，`dp[n]` 已经是全局最大）。

> **为什么只需要保存「最小的 last[i]」**  
> 对于同样的 `dp`，如果我们把最后一段的和记得更小，那么对应的阈值 `pref[i] + last[i]` 也更小，后面要满足 `pref[next] ≥ threshold` 的要求就更容易。因此「越小越好」是安全的贪心。

#### 数据结构细节（Fenwick 树）

Fenwick 树支持两种操作（均为 `O(log N)`）：

- `add(pos, value)`：在坐标 `pos` 上写入 `max(old, value)`（这里用「取最大」而不是「加」）。  
- `query(pos)`：返回 `[1 … pos]` 区间的最大值。

因为我们只需要「最大」而不是「求和」，把树的「合并」函数改成 `max` 即可。

#### 代码（Python）

```python
from typing import List
import bisect

class BIT:
    """Fenwick Tree for prefix maximum."""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 2)          # 1-indexed

    def update(self, idx: int, val: int) -> None:
        """在 idx 位置写入 max(old, val)"""
        while idx <= self.n:
            if val > self.bit[idx]:
                self.bit[idx] = val
            idx += idx & -idx

    def query(self, idx: int) -> int:
        """返回 [1..idx] 区间的最大值"""
        res = 0
        while idx > 0:
            if self.bit[idx] > res:
                res = self.bit[idx]
            idx -= idx & -idx
        return res


def maxLength(nums: List[int]) -> int:
    n = len(nums)
    # 1️⃣ 前缀和
    pref = [0] * (n + 1)
    for i, x in enumerate(nums, 1):
        pref[i] = pref[i - 1] + x

    # 2️⃣ 收集所有可能出现的阈值（pref[i] + last[i]）以及所有 pref[i]
    # 为了让树的坐标离散化，这里我们先把所有 pref[i] 放进去，
    # 后面在遍历时再动态插入新的阈值（因为 last[i] 只会是单元素值，已在 pref 中出现）。
    all_vals = pref[:]                     # 先把所有 pref 放进去
    # 预先把每个单元素的阈值加入：pref[i] + nums[i-1]
    for i in range(1, n + 1):
        all_vals.append(pref[i] + nums[i - 1])

    # 3️⃣ 坐标压缩
    uniq = sorted(set(all_vals))
    def get_idx(x: int) -> int:
        """返回 x 在压缩后数组中的 1-indexed 位置"""
        return bisect.bisect_left(uniq, x) + 1

    bit = BIT(len(uniq))

    # 4️⃣ 初始化：空前缀的阈值为 0，dp = 0
    # threshold = pref[0] + last[0] = 0 + 0 = 0
    bit.update(get_idx(0), 0)

    dp = [0] * (n + 1)          # dp[i]：前 i 个元素的最优划分数
    # last[i] 只需要记单元素的值即可（最小可能的）
    for i in range(1, n + 1):
        # ① 通过前缀和查询能接上的最大 dp
        cur_pref = pref[i]
        best = bit.query(get_idx(cur_pref))   # 所有阈值 ≤ cur_pref 的最大 dp
        dp[i] = best + 1

        # ② 计算本位置的最小 possible last sum（这里直接取单元素）
        last_sum = nums[i - 1]                # 最小的可能值
        threshold = cur_pref + last_sum       # 对应的阈值
        # ③ 把 (threshold, dp[i]) 写回 Fenwick
        bit.update(get_idx(threshold), dp[i])

    return dp[n]
```

> **代码说明（每行中文注释）**  
> - `BIT` 类把「求和」改成「求最大」；`update` 用 `max` 更新，`query` 返回前缀最大。  
> - `pref` 保存累计重量，`pref[i]` 就是「从左到第 i‑1 个砖的总重量」。  
> - `all_vals` 里放所有可能出现的「阈值」以及所有前缀和，随后统一压缩成 `uniq`，这样 `BIT` 的下标都是连续的整数。  
> - 主循环里：  
>   1. `best = bit.query(get_idx(cur_pref))` 找到「所有阈值 ≤ 当前累计重量」的最大划分数。  
>   2. `dp[i] = best + 1` 表示在 `i` 位置再加上一段合法的区间。  
>   3. `threshold = cur_pref + last_sum` 是以后「能否接上」的关键值，写回树中供后面查询。  
> - 最后 `dp[n]` 即为全数组的最大区间数，也就是题目要求的「最大非递减数组长度」。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 前缀和 `O(n)`。  
  - 坐标压缩 `O(n log n)`（排序）。  
  - 主循环每一步两次 Fenwick 操作，各 `O(log n)`。  
  - 整体远远小于暴力的指数级，能够轻松跑完 `n = 10⁵` 的数据。  

- **空间复杂度**：`O(n)`  
  - 前缀和、压缩数组、Fenwick 树各占线性空间。  

> **大白话**：  
> `O(n log n)` 可以想象成「把 10⁵ 件东西排成一条队，排队时每个人只需要看前面几个人的情况（log n ≈ 17），而不是去检查所有人」，所以即使是大规模数据也能在毫秒级完成。

---

## 心得  

- **核心技巧**：把「合并子数组」抽象为「把数组划分成区间，区间和必须非递减」；利用 **前缀和** 把区间和化为 `pref[i] - pref[j]`，再把不等式转化为 `pref[i] ≥ pref[j] + last[j]`，于是问题变成「在所有阈值 ≤ 当前前缀和的状态中取最大 `dp`」，这正好是 **单调性 + 树状数组（或线段树）** 的经典应用。  

- **适用的题型**（类似思路）  
  1. **最长递增子序列（LIS）**的「坐标压缩 + 树状数组」写法。  
  2. **分割数组使每段和满足单调性**（如 LeetCode 1712、1849 等）。  
  3. **区间划分 + 单调约束**的 DP（如「分割数组的最大得分」）。  

- **一句话总结解题钥匙**：  
  > 把「合并」看成「划分」，把「区间和」写成「前缀和差」后，利用 **阈值 ≤ 当前前缀和** 的单调性，用 **Fenwick 树求前缀最大** 完成 `O(n log n)` 的最优划分。

---

## 反思  

- **第一反应**：看到「可以把任意子数组替换成它的和」第一时间想到「把相邻元素砸在一起」——于是自然把问题转成「划分成区间」的形式。  

- **最容易踩的坑**  
  1. **忘记最小化最后一个区间的和**：如果只记录「任意」的 `last[i]`，后面阈值会偏大，导致 DP 过于保守，答案被低估。  
  2. **阈值与前缀和的比较顺序写反**：式子 `pref[i] ≥ pref[j] + last[j]` 必须先算 `pref[j] + last[j]` 再与 `pref[i]` 比，容易写成 `pref[i] - pref[j] ≥ last[j]` 而在代码里把两边调换导致查询方向错误。  
  3. **坐标压缩遗漏了 `threshold = 0`**（空前缀的阈值），会让第一次查询得到 `0` 而不是 `-inf`，导致 `dp[1]` 计算错误。  

- **下次类似题的第一步**：  
  > **先把「区间属性」写成「前缀和差」**，检查是否能把约束转化为「某个阈值 ≤ 当前前缀和」的形式；如果可以，考虑使用 **单调栈 / 树状数组** 进行「前缀最大」或「前缀最小」的快速查询。  

祝你在算法的道路上砸出更多「非递减」的好成绩！