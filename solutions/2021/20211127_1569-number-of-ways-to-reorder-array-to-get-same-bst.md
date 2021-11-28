# #1569. 重新排列数组以得到相同二叉搜索树的方案数 / Number of Ways to Reorder Array to Get Same BST

> 难度：困难 · 标签：Array、Math、Divide and Conquer、Dynamic Programming、Tree、Union Find、Binary Search Tree、Memoization、Combinatorics、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/)

---

## 题目（英文原版）

**Description**

Given an array nums that represents a permutation of integers from 1 to n. We are going to construct a binary search tree (BST) by inserting the elements of nums in order into an initially empty BST. Find the number of different ways to reorder nums so that the constructed BST is identical to that formed from the original array nums.
Return the number of ways to reorder nums such that the BST formed is identical to the original BST formed from nums.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3]
Output: 1
Explanation: We can reorder nums to be [2,3,1] which will yield the same BST. There are no other ways to reorder nums which will yield the same BST.
```

**Example 2:**

```
Input: nums = [3,4,5,1,2]
Output: 5
Explanation: The following 5 arrays will yield the same BST: 
[3,1,2,4,5]
[3,1,4,2,5]
[3,1,4,5,2]
[3,4,1,2,5]
[3,4,1,5,2]
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 0
Explanation: There are no other orderings of nums that will yield the same BST.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= nums.length
- All integers in nums are distinct.

---

## 题目（中文翻译）

给定一个数组 `nums`，它是整数集合 `[1, n]` 的一个排列。我们将按照 `nums` 中的顺序依次将元素插入到一棵初始为空的二叉搜索树（BST）中。求有多少种不同的排列方式能够使得构造出的 BST 与使用原数组 `nums` 构造得到的 BST 完全相同。

返回满足上述条件的排列数目。由于答案可能非常大，请返回结果对 `10^9 + 7` 取模后的值。

**示例 1**

**输入**: `nums = [2,1,3]`  
**输出**: `1`  
**解释**: 我们可以将 `nums` 重新排列为 `[2,3,1]`，这样得到的 BST 与原来的完全相同。除此之外不存在其他能够得到相同 BST 的排列。

**示例 2**

**输入**: `nums = [3,4,5,1,2]`  
**输出**: `5`  
**解释**: 以下 5 种排列会得到相同的 BST：  
`[3,1,2,4,5]`  
`[3,1,4,2,5]`  
`[3,1,4,5,2]`  
`[3,4,1,2,5]`  
`[3,4,1,5,2]`

**示例 3**

**输入**: `nums = [1,2,3]`  
**输出**: `0`  
**解释**: 没有其他排列方式能够得到与原始数组相同的 BST。

**约束条件**

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= nums.length`
- `nums` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的排列都枚举出来**，把每一种排列依次插入空的二叉搜索树（BST），看得到的树是否和原来的树完全相同，统计满足条件的排列个数。

- **数据结构**  
  - **列表（list）**：用来存放当前枚举的排列。  
  - **二叉树节点**（`TreeNode`）：模拟 BST 的插入过程。可以把它想象成一本“字典”，每插入一个数字，就在对应的页码上写下这个数字的位置，左子树对应比根小的页码，右子树对应比根大的页码。  
- **为什么正确**  
  - 我们遍历了**全部**合法的排列（即 `nums` 的全排列），只要有一种排列能得到相同的 BST，就会被计数。因为没有漏掉任何一种可能，统计的结果必然是准确的。  
- **时间/空间复杂度**  
  - 全排列的数量是 `n!`（n 的阶乘），对每一种排列我们都要模拟一次插入，插入过程最坏是 O(n)。于是总时间复杂度是 **O(n!·n)**，这在实际中几乎不可接受。  
  - 空间上我们需要保存当前排列（O(n)）和一棵临时的 BST（最多 O(n)），所以 **O(n)** 的额外空间。

> **大白话解释**：  
> `n!` 就像把 `n` 本不同的书随意排成一排的方式，哪怕 `n=10`，也有 3,628,800 种排法，想把每一种都尝试一次，显然太慢了。

#### 代码（Python）

```python
from itertools import permutations
from typing import List

# ---------- 辅助：构造 BST ----------
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None

def insert(root: TreeNode, val: int) -> TreeNode:
    """把 val 插入到 BST 中，返回根节点（保持不变）"""
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:                     # val > root.val，因为所有值互不相同
        root.right = insert(root.right, val)
    return root

def build_bst(arr: List[int]) -> TreeNode:
    """按照数组顺序依次插入，得到一棵 BST"""
    root = None
    for x in arr:
        root = insert(root, x)
    return root

def same_tree(a: TreeNode, b: TreeNode) -> bool:
    """递归比较两棵树是否结构相同、节点值相同"""
    if not a and not b:
        return True
    if not a or not b or a.val != b.val:
        return False
    return same_tree(a.left, b.left) and same_tree(a.right, b.right)

# ---------- 暴力枚举 ----------
def numOfWays_bruteforce(nums: List[int]) -> int:
    MOD = 10**9 + 7
    target = build_bst(nums)                     # 原始 BST
    cnt = 0
    for perm in permutations(nums):
        if perm[0] != nums[0]:        # 根必须是原来的根，否则一定不相同，提前剪枝
            continue
        if same_tree(build_bst(perm), target):
            cnt += 1
    # 题目要求不计入原始排列本身
    return (cnt - 1) % MOD
```

> 这段代码可以直接运行（不过对 n>8 会超时），每一行都加了中文注释帮助理解。

#### 复杂度  

- **时间复杂度**：`O(n!·n)`  
  - `n!` 表示所有排列的数量，`·n` 是每次插入/比较 BST 所需的时间。  
- **空间复杂度**：`O(n)`  
  - 只保存当前排列和临时 BST，随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有排列**。实际上，排列的顺序对 BST 的结构只有 **相对大小** 有影响。我们可以利用 BST 的**分治**特性，递归地统计每个子树的合法排列数，再利用组合数学把左右子树的排列“交叉”在一起。

**关键观察**  

1. **根节点唯一**  
   - 第一个插入的元素一定是整棵树的根。后面的元素只会在根的左子树或右子树里继续插入，**不可能跨越根**。  
2. **左右子树相互独立**  
   - 对于根左侧的所有元素（全部比根小），它们只会在左子树内部比较大小；同理右侧元素只会在右子树内部比较。  
3. **把两棵子树的插入顺序混合**  
   - 假设左子树有 `L` 个节点，右子树有 `R` 个节点。我们已经知道左子树内部可以有 `ways_left` 种插入顺序，右子树内部可以有 `ways_right` 种。  
   - 现在要把这 `L+R` 个节点的插入顺序**合并**在一起，使得左子树的相对顺序保持不变，右子树的相对顺序也保持不变。  
   - 这相当于从 `L+R` 个位置里挑出 `L` 个放左子树，剩下的放右子树，组合数为 `C(L+R, L)`（即 “从 L+R 中选 L”。）  
   - 因此，当前子树的合法排列数 = `C(L+R, L) * ways_left * ways_right`。  

4. **递归求解**  
   - 对左子树和右子树再分别使用相同的思路，递归到底（空树或只有一个节点）时返回 1。  

5. **组合数的计算**  
   - `n` 最多 1000，直接用阶乘求组合数会溢出，需要**模数** `M = 10**9+7` 下的**预计算逆元**（费马小定理）或**动态规划**。这里采用预计算阶乘 `fac[i]` 和逆阶乘 `ifac[i]`，这样 `C(n,k) = fac[n] * ifac[k] * ifac[n-k] % M`。  

6. **记忆化**  
   - 同一子数组会被多次递归访问（例如在不同父节点的左/右子树里出现相同的元素集合），可以用 `@lru_cache` 对 `(tuple(nums))` 进行记忆化，进一步提升效率。  

**整体框架**  

```
solve(nums):
    precompute fac / ifac up to n
    return (dfs(nums) - 1) % MOD   # 减去原始排列本身
```

`dfs(subarray)`：

```
if len(subarray) <= 2: return 1
root = subarray[0]
left  = [x for x in subarray if x < root]
right = [x for x in subarray if x > root]

ways_left  = dfs(left)
ways_right = dfs(right)

combine = C(len(left)+len(right), len(left))   # 交叉排列数
return combine * ways_left % MOD * ways_right % MOD
```

**类比**：  
把左子树的节点看成红球，右子树的节点看成蓝球。我们要把 `L+R` 个球排成一列，要求红球内部的相对顺序保持不变，蓝球内部的相对顺序也保持不变。把红球的位置挑出来的方式正是组合数 `C(L+R, L)`，剩下的位置自然就是蓝球的位置。

#### 代码（Python）

```python
from functools import lru_cache
from typing import List

MOD = 10**9 + 7

# ---------- 预计算阶乘和逆阶乘 ----------
def prepare_factorials(n: int):
    """返回 (fac, ifac) 两个列表，分别是 i! 和 (i!)^{-1} (mod MOD)"""
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    # 费马小定理：a^{p-2} ≡ a^{-1} (mod p)，p 为质数
    ifac = [1] * (n + 1)
    ifac[n] = pow(fac[n], MOD - 2, MOD)          # n! 的逆元
    for i in range(n, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD          # (i-1)! = i! / i
    return fac, ifac

def comb(n: int, k: int, fac: List[int], ifac: List[int]) -> int:
    """在模 MOD 下计算组合数 C(n,k)"""
    if k < 0 or k > n:
        return 0
    return fac[n] * ifac[k] % MOD * ifac[n - k] % MOD

# ---------- 主函数 ----------
def numOfWays(nums: List[int]) -> int:
    n = len(nums)
    fac, ifac = prepare_factorials(n)

    @lru_cache(maxsize=None)
    def dfs(arr: tuple) -> int:
        """返回 arr（以 tuple 形式传入）对应子树的合法排列数"""
        if len(arr) <= 2:               # 0、1、2 个节点的子树只有唯一的插入顺序
            return 1

        root = arr[0]
        left  = tuple(x for x in arr if x < root)
        right = tuple(x for x in arr if x > root)

        ways_left  = dfs(left)
        ways_right = dfs(right)

        # 交叉排列数：从 left+right 的位置中挑出 left 的位置
        inter = comb(len(left) + len(right), len(left), fac, ifac)

        return inter * ways_left % MOD * ways_right % MOD

    # 减去原始排列本身，因为题目要求“不同的重排”
    return (dfs(tuple(nums)) - 1) % MOD
```

> **代码要点注释**  
> - `prepare_factorials`：一次性算好所有 `i!` 与它们的逆元，后面求组合数就 O(1)。  
> - `lru_cache`：把每个子数组的结果记下来，防止重复递归。  
> - `dfs` 中把列表转成 `tuple` 作为缓存键，因为列表是不可哈希的。  
> - `comb` 使用预计算的 `fac`、`ifac`，在模数下快速得到 `C(n,k)`。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`（近似）  
  - 每个节点只会被划分到一次左子树或右子树，递归深度最多 `O(log n)`（均匀分布）或最坏 `O(n)`（完全偏斜），但每层的划分操作总共遍历所有元素一次，所以总体是 `O(n log n)` 的期望，最坏 `O(n²)`（仍然远快于 `n!`).  
- **空间复杂度**：`O(n)`  
  - 递归栈深度最坏 `O(n)`，另外保存 `fac`、`ifac` 各 `O(n)`，以及缓存的子数组（每个节点对应一个缓存条目）共 `O(n)`。  

> 与暴力解相比，时间从天文数字的 `n!` 降到了线性甚至略高的 `n log n`，可以轻松跑完 `n=1000` 的测试。

---

## 心得

- **核心技巧**：**利用 BST 的分治结构 + 组合数学的“交叉排列”**。  
- **适用的题型**  
  1. “把一棵树的节点重新排列，使得插入顺序不变”——如本题。  
  2. “统计不同的二叉搜索树形状的插入序列”——如 LeetCode 1569.  
  3. “在保持相对顺序的前提下合并两段序列的计数”——常见的组合计数问题。  
- **一句话总结**：  
  > **根确定，左/右子树独立，用 `C(L+R, L)` 把两边的合法序列交叉合并**。

---

## 反思

- **第一反应**：看到“构造 BST 再比较”立刻想到暴力枚举所有排列。  
- **最容易踩的坑**  
  1. **忘记模数**：组合数在乘法过程中会很大，需要随时 `% MOD`。  
  2. **边界条件**：只有 0、1、2 个节点的子树只有唯一排列，直接返回 1，防止除以 0 的组合数。  
  3. **缓存键的可哈希性**：列表不能直接作为 `lru_cache` 的键，必须转成 `tuple`。  
  4. **答案要减去原始排列**：题目要求“不同的重排”，所以最后要 `-1`（并再取模防负数）。  
- **下次类似题的第一步**：  
  > **先把问题抽象为“根划分左右子树”，判断子问题是否相互独立，然后寻找组合数或 DP 把子问题合并**。这样就能迅速从暴力想到分治/组合的最优解。