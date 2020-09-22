# #996. 可平方数组的数目 / Number of Squareful Arrays

> 难度：困难 · 标签：Array、Hash Table、Math、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/number-of-squareful-arrays/)

---

## 题目（英文原版）

**Description**

An array is squareful if the sum of every pair of adjacent elements is a perfect square.
Given an integer array nums, return the number of permutations of nums that are squareful.
Two permutations perm1 and perm2 are different if there is some index i such that perm1[i] != perm2[i].

**Examples**

**Example 1:**

```
Input: nums = [1,17,8]
Output: 2
Explanation: [1,8,17] and [17,8,1] are the valid permutations.
```

**Example 2:**

```
Input: nums = [2,2,2]
Output: 1
```

**Constraints**

- 1 <= nums.length <= 12
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

一个数组如果每一对相邻元素的和是完全平方数（perfect square），则称该数组为可平方的。给定整数数组 `nums`，返回 `nums` 的所有排列（permutations）中可平方的排列个数。两个排列 `perm1` 和 `perm2` 不同，当且仅当存在某个下标 `i` 使得 `perm1[i] != perm2[i]`。

**示例 1**  
Input: nums = [1,17,8]  
Output: 2  
Explanation: `[1,8,17]` 和 `[17,8,1]` 是满足条件的排列。

**示例 2**  
Input: nums = [2,2,2]  
Output: 1  

**约束条件**  
- 1 ≤ nums.length ≤ 12  
- 0 ≤ nums[i] ≤ 10^9

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有排列都列出来**，然后逐个检查相邻两数之和是否是完全平方数（比如 1、4、9、16…）。  
这一步可以拆成两部分：

1. **产生全排列**  
   - 用递归的方式把 `nums` 中的每个元素依次放到当前排列的下一个位置。  
   - 类比：就像把一堆不同颜色的球依次排成一行，先选第一个球，再选第二个，直到全部排好。

2. **检查平方和**  
   - 对已经排好的序列，从左到右看相邻两个数的和 `a+b`，判断 `a+b` 是否是完全平方数。  
   - 判断方法：取整数平方根 `int(sqrt(a+b))`，如果 `root * root == a+b` 就说明是完全平方数。  
   - 类比：把两本书的页码相加，看是否恰好是某本书的章节数（正好是一个完整的平方）。

因为题目要求 **不同的排列**（即使有相同的数，只要下标位置不同也算不同），我们在产生全排列时不需要去重。

> **为什么这个方法一定能得到答案？**  
> 只要把所有可能的排列都枚举完，并且每个排列都做了合法性检查，就不会漏掉任何一个满足条件的排列，也不会误计不合法的排列。

#### 代码（Python）

```python
import math
from itertools import permutations

def is_perfect_square(x: int) -> bool:
    """判断 x 是否为完全平方数"""
    root = int(math.isqrt(x))          # math.isqrt 返回整数平方根
    return root * root == x

def num_squareful_permutations_bruteforce(nums):
    cnt = 0
    # itertools.permutations 会产生所有排列（包括相同数的不同下标排列）
    for perm in permutations(nums):
        ok = True
        # 检查相邻两数之和是否为完全平方数
        for i in range(len(perm) - 1):
            if not is_perfect_square(perm[i] + perm[i + 1]):
                ok = False
                break
        if ok:
            cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的个数（比如 5 个数就有 120 种），每个排列要检查 `n-1` 对相邻元素，所以乘以 `n`。  
  - 用大白话说，就是“先把所有可能的排法列出来（这一步已经非常慢），再逐个检查”。  
- **空间复杂度**：`O(n)`  
  - 递归或 `permutations` 只需要保存当前排列的长度 `n`，其余都是常数空间。  

> 对于 `n ≤ 12` 的限制，`12! ≈ 4.79e8`，暴力枚举显然不可接受——即使只做一次检查也会超时。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**。我们可以利用下面两点来大幅剪枝：

1. **相邻关系是局部的**  
   - 只要知道当前数字 `x`，下一个数字只能是满足 `x + y` 为完全平方数的 `y`。  
   - 换句话说，整个排列可以看成在一个**无向图**上走哈密尔顿路径：  
     - **节点**：数组中的每个下标（因为相同的数可能出现多次，需要区分下标）。  
     - **边**：若 `nums[i] + nums[j]` 为完全平方数，则在 `i`、`j` 之间连一条边。

2. **状态压缩 + 记忆化搜索**  
   - 由于 `n ≤ 12`，我们可以用 **位掩码**（bitmask）记录哪些下标已经被使用。  
   - `mask` 的第 `i` 位为 `1` 表示下标 `i` 已经放进排列里。  
   - 用 **DP + 回溯**（也叫记忆化搜索）求解：  
     - `dp[last][mask]` = 以 `last` 为最后一个元素、已经使用了 `mask` 中的下标的合法排列数。  
   - 递推公式：  
     ```
     dp[last][mask] = sum( dp[next][mask | (1 << next)] )
                     for all next not in mask
                     and nums[last] + nums[next] is a perfect square
     ```
   - 递归结束条件是 `mask` 已经包含全部 `n` 个下标，此时计 1 条完整排列。

3. **预处理相邻合法列表**  
   - 为了在递归时快速找“可以接在 `last` 后面的 `next`”，先把每个下标的合法邻居存进列表 `adj[i]`。  
   - 这一步相当于把“是否是完全平方数”这件事提前算好，后面只需要 O(1) 查询。

4. **去重（可选）**  
   - 如果数组里有相同的数，直接使用下标已经天然区分了，不会出现重复计数的问题。  
   - 若想进一步压缩状态（比如把相同数合并），实现会更复杂，这里保持最直观的下标版即可。

> **核心算法**：**记忆化深度优先搜索 + 位掩码**（DP on subsets），常用于「排列计数」且约束 `n ≤ 12` 时非常高效。

#### 代码（Python）

```python
import math
from functools import lru_cache

def is_perfect_square(x: int) -> bool:
    """判断 x 是否为完全平方数（整数根法）"""
    root = int(math.isqrt(x))
    return root * root == x

def num_squareful_arrays(nums):
    n = len(nums)
    # 1. 预处理每个下标的合法邻居
    adj = [[] for _ in range(n)]            # adj[i] 保存可以接在 i 后面的下标 j
    for i in range(n):
        for j in range(n):
            if i != j and is_perfect_square(nums[i] + nums[j]):
                adj[i].append(j)

    # 2. 记忆化搜索（DP on subsets）
    @lru_cache(maxsize=None)
    def dfs(last, mask):
        """
        last : 上一个放进排列的下标
        mask : 已经使用的下标集合，用二进制表示，例如 mask = 0b1011 表示下标 0、1、3 已使用
        返回：从当前状态继续往后填完剩余元素的合法排列数
        """
        if mask == (1 << n) - 1:           # 所有下标都已使用，形成完整排列
            return 1

        total = 0
        for nxt in adj[last]:              # 只遍历合法的下一个候选
            if not (mask >> nxt) & 1:      # nxt 还没被使用
                total += dfs(nxt, mask | (1 << nxt))
        return total

    # 3. 任选一个下标作为起点，累加所有可能的排列数
    answer = 0
    for start in range(n):
        answer += dfs(start, 1 << start)

    return answer
```

> 代码要点（带中文注释）：
> - `adj` 把“是否能相邻”这件事提前算好，后面只需要遍历 `adj[last]`。
> - `mask` 用位运算记录已使用的元素，`(1 << n) - 1` 表示全部 `n` 位都是 `1`（即全选）。
> - `lru_cache` 自动帮我们把已经算过的 `(last, mask)` 记住，避免重复递归——相当于 DP 表。

#### 复杂度

- **时间复杂度**：`O(n^2 * 2^n)`  
  - 状态数目：`n * 2^n`（每个 `last`（`n` 种）配合每个 `mask`（`2^n` 种））。  
  - 对每个状态我们遍历 `adj[last]`，最坏情况是 `O(n)`，于是总共 `O(n * n * 2^n)`。  
  - 用大白话说，就是“因为我们只枚举合法的相邻关系，而不是所有排列，所以复杂度从 `n!` 降到了 `n * 2^n`，在 `n ≤ 12` 时大约几千次，轻松跑完”。

- **空间复杂度**：`O(n * 2^n)`  
  - 递归栈深度最多 `n`，`lru_cache` 保存的表格大小同状态数 `n * 2^n`。  
  - 对于 `n = 12`，约为 `12 * 4096 ≈ 5e4`，只占几百 KB，完全可以接受。

> 与暴力解相比，时间从 **指数级的 `n!`** 降到 **`n * 2^n`**，快了几个数量级，完全符合题目要求。

---

## 心得

- **核心技巧**：**记忆化深度优先搜索 + 位掩码（DP on subsets）**，用来统计满足局部约束的全排列数。  
- **适用的题型**（类似思路）：
  1. “Permutation with Adjacent Condition” 系列，如 **“Number of Permutations with Given Hamming Distance”**。  
  2. “Hamiltonian Path / Cycle Count in Small Graph”——用位掩码枚举子集。  
  3. “Count Different Palindromic Substrings” 中的 “状态压缩 DP” 变体。  
- **一句话总结解题钥匙**：  
  > 把“相邻必须是完全平方数”抽象成图的边，利用位掩码记住已经走过的节点，记忆化搜索即可在指数时间内枚举所有合法排列。

---

## 反思

- **拿到题目第一反应**：先写全排列暴力检查，确认思路是否正确。  
- **最容易踩的坑**  
  - **重复元素**：如果直接用 `set(permutations)` 去重，会把下标不同但数值相同的排列错误合并，导致计数错误。应当基于下标区分。  
  - **完全平方数判断**：直接使用 `int(sqrt(x))**2 == x` 可能因为浮点误差出错，建议使用 `math.isqrt`（整数平方根）安全可靠。  
  - **位运算细节**：`mask >> nxt & 1` 与 `(mask & (1 << nxt)) == 0` 两种写法都可以，记得加括号防止优先级错误。  
- **下次遇到同类题**，第一步应该：  
  1. 把“相邻关系”抽象成**邻接表**（图），  
  2. 判断是否可以用**位掩码 + DP** 进行状态压缩。  

这样就能快速从暴力思路转向高效的记忆化搜索，避免超时。