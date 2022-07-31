# #1879. 两个数组的最小异或和 / Minimum XOR Sum of Two Arrays

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-xor-sum-of-two-arrays/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 of length n.
The XOR sum of the two integer arrays is (nums1[0] XOR nums2[0]) + (nums1[1] XOR nums2[1]) + ... + (nums1[n - 1] XOR nums2[n - 1]) (0-indexed).
Rearrange the elements of nums2 such that the resulting XOR sum is minimized.
Return the XOR sum after the rearrangement.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2], nums2 = [2,3]
Output: 2
Explanation: Rearrange nums2 so that it becomes [3,2].
The XOR sum is (1 XOR 3) + (2 XOR 2) = 2 + 0 = 2.
```

**Example 2:**

```
Input: nums1 = [1,0,3], nums2 = [5,3,4]
Output: 8
Explanation: Rearrange nums2 so that it becomes [5,4,3]. 
The XOR sum is (1 XOR 5) + (0 XOR 4) + (3 XOR 3) = 4 + 4 + 0 = 8.
```

**Constraints**

- n == nums1.length
- n == nums2.length
- 1 <= n <= 14
- 0 <= nums1[i], nums2[i] <= 107

---

## 题目（中文翻译）

你得到两个长度均为 n 的整数数组（integer arrays）`nums1` 和 `nums2`。  
两个整数数组的异或和（XOR sum）定义为：

\[
(nums1[0] \; \text{XOR} \; nums2[0]) + (nums1[1] \; \text{XOR} \; nums2[1]) + \dots + (nums1[n-1] \; \text{XOR} \; nums2[n-1])
\]

（0‑索引）。  
请重新排列 `nums2` 中的元素，使得得到的异或和最小。返回排列后的最小异或和。

**示例 1**  
输入: `nums1 = [1,2]`, `nums2 = [2,3]`  
输出: `2`  
解释: 将 `nums2` 重新排列为 `[3,2]`。  
异或和为 \((1 \; \text{XOR} \; 3) + (2 \; \text{XOR} \; 2) = 2 + 0 = 2\)。

**示例 2**  
输入: `nums1 = [1,0,3]`, `nums2 = [5,3,4]`  
输出: `8`  
解释: 将 `nums2` 重新排列为 `[5,4,3]`。  
异或和为 \((1 \; \text{XOR} \; 5) + (0 \; \text{XOR} \; 4) + (3 \; \text{XOR} \; 3) = 4 + 4 + 0 = 8\)。

**约束条件**  
- `n == nums1.length`  
- `n == nums2.length`  
- `1 ≤ n ≤ 14`  
- `0 ≤ nums1[i], nums2[i] ≤ 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `nums2` 的所有可能排列都枚举一遍，和 `nums1` 按顺序配对后算出 XOR 和，取最小值。

- **用到的数据结构**：  
  - **数组**：存放两个序列。  
  - **排列（permutation）**：就像把一副牌洗牌后重新摆放，所有可能的摆法就是所有排列。  
  - **回溯 / 递归**：把“从第 0 位开始依次挑选一个未使用的元素”想象成在一棵树上走，每走一步就确定了 `nums2` 的一个位置。

- **为什么正确**：  
  我们把 **所有** 合法的重新排列都尝试了一遍，必然能找到使 XOR 和最小的那一种。

- **时间/空间复杂度**：  
  - **时间**：`n` 个数的全排列有 `n!`（n 的阶乘）种。对每一种排列我们都要遍历 `n` 次计算 XOR，故时间复杂度是 `O(n! * n)`。  
    - 大白话：`n=14` 时，`14! ≈ 87,178,291,200`，远远超过一秒能跑完的次数，所以这种方法只适合 `n` 很小的情况（比如 `n≤8`）。  
  - **空间**：递归栈深度为 `n`，外加保存 `nums2` 的副本，故 `O(n)`。  

#### 代码（Python）

```python
from typing import List

def minimumXORSum_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    used = [False] * n          # 标记 nums2 中哪些下标已经被使用
    best = float('inf')         # 当前找到的最小 XOR 和

    def dfs(idx: int, cur_sum: int) -> None:
        """
        idx: 正在配对 nums1[idx]
        cur_sum: 已经累加的 XOR 和
        """
        nonlocal best
        # 剪枝：如果当前已经超过已知最小值，就不必继续往下搜索
        if cur_sum >= best:
            return
        # 所有位置都配对完毕，更新答案
        if idx == n:
            best = cur_sum
            return

        # 逐个尝试把 nums2 中未使用的元素放到当前位置
        for j in range(n):
            if not used[j]:
                used[j] = True
                dfs(idx + 1, cur_sum + (nums1[idx] ^ nums2[j]))
                used[j] = False

    dfs(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  - `n!` 表示所有排列的数量，乘上每次遍历 `n` 次求 XOR 的代价。  
- **空间复杂度**：`O(n)`  
  - 递归深度最多 `n`，再加上 `used` 标记数组。  

---

### 2. 最优解

#### 思路  

**从暴力解出发**，我们发现最慢的地方在于**枚举所有排列**（`n!`），这远远超过了题目给出的 `n ≤ 14` 的上限。  
我们需要一种**只遍历 2ⁿ（指数级但远小于 n!）**的办法。

**核心观察**：  
- `n` 最多 14，**可以用位掩码（bitmask）表示已使用的下标**。  
- 当我们已经为 `nums1` 前 `i` 个元素挑选好了对应的 `nums2` 元素后，剩下的未使用元素集合可以用一个 `mask`（二进制位）来唯一描述。  
- 于是我们可以把“把前 i‑1 个位置配好，剩下的怎么配”抽象成**子问题**，使用**动态规划（DP）+ 位掩码**来递推。

**状态定义**  
- `dp[mask]` 表示已经为 `nums1` 的前 `k`（`k = popcount(mask)`）个位置挑选了对应的 `nums2` 元素，且这些被挑选的 `nums2` 元素下标恰好对应 `mask` 中为 1 的位置时，能够得到的最小 XOR 和。  
  - `popcount(mask)` = mask 中 1 的个数，表示已经配对了多少对。

**状态转移**  
- 假设当前 `mask` 已经配对了 `k` 对（即 `k = popcount(mask)`），我们现在要为第 `k`（从 0 开始）个 `nums1` 元素挑选一个新的 `nums2` 元素。  
- 遍历所有未被使用的下标 `j`（即 `mask` 第 `j` 位为 0），形成新的掩码 `next_mask = mask | (1 << j)`。  
- 那么：
  ```
  dp[next_mask] = min(dp[next_mask],
                      dp[mask] + (nums1[k] ^ nums2[j]))
  ```
- 初始状态 `dp[0] = 0`（什么都没配，对应的 XOR 和为 0），其他全部设为无限大。

**答案**  
- 完全配对后，所有下标都被使用，即 `mask = (1 << n) - 1`。`dp[full_mask]` 就是要求的最小 XOR 和。

**为什么只需要 2ⁿ**  
- 每个 `mask` 只对应一种“已使用元素集合”，而不是所有排列的顺序。对同一集合的不同排列，它们的 `dp` 值只取最小的那一个，所以不必区分顺序，极大降低状态数。

**位掩码的类比**  
- 想象一排 14 把钥匙，每把钥匙对应 `nums2` 的一个元素。我们用 14 位的二进制数表示哪些钥匙已经拔出来（1 表示已拔），每一次配对相当于拔出一把新钥匙并记下产生的费用（XOR）。整个过程就像在玩“拔钥匙游戏”，只要记住已经拔出的钥匙集合即可。

#### 代码（Python）

```python
from typing import List

def minimumXORSum(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    full_mask = (1 << n) - 1               # 所有 n 位都为 1，表示全部配对完成

    INF = 10 ** 18
    dp = [INF] * (1 << n)                  # dp 长度为 2^n
    dp[0] = 0                              # 初始状态：没有配对，费用为 0

    # 按 mask 的二进制递增遍历，保证子状态已计算
    for mask in range(full_mask + 1):
        k = bin(mask).count('1')           # 已经配对了前 k 个 nums1 元素
        if k >= n:                         # 已经配完，后面不必再转移
            continue
        # 尝试把第 k 个 nums1 与任意未使用的 nums2[j] 配对
        for j in range(n):
            if not (mask >> j) & 1:        # 第 j 位是 0，表示 nums2[j] 还未被使用
                next_mask = mask | (1 << j)
                cost = dp[mask] + (nums1[k] ^ nums2[j])
                if cost < dp[next_mask]:
                    dp[next_mask] = cost   # 取最小值

    return dp[full_mask]
```

#### 复杂度

- **时间复杂度**：`O(n * 2^n)`  
  - 对每个 `mask`（共 `2^n` 种）我们遍历所有 `n` 个可能的 `j`，所以乘以 `n`。  
  - 大白话：当 `n=14` 时，`2^14 = 16384`，再乘以 14 大约是 2.3 万次运算，几乎可以在毫秒级完成。

- **空间复杂度**：`O(2^n)`  
  - 只需要一个长度为 `2^n` 的数组来保存每个子集的最小费用。  
  - 对于 `n=14`，数组大小为 16384，几乎不占内存。

---

## 心得

- **核心技巧**：**位掩码动态规划**（Bitmask DP），把“已使用元素集合”抽象为二进制状态，从而把指数级的排列枚举压缩到 `2^n`。
- **适用题型**：
  1. **分配/匹配类**：如 “分配工作的最小总时间” (Minimum Cost to Hire Workers)、 “按位与最小化” (Minimum XOR Sum of Two Arrays) 等。  
  2. **子集 DP**：如 “求子集的最大异或和” (Maximum XOR of Subset) 或 “旅行商问题” 的小规模版。  
  3. **状态压缩 DP**：如 “最小生成树的 DP 版” (Minimum Spanning Tree with DP) 等。
- **一句话总结**：**把“顺序”抛掉，只记“哪些已经用过”，用二进制掩码把指数爆炸降到可接受的 `2^n`。**

---

## 反思

- **第一反应**：直接想到全排列枚举，毕竟题目说“重新排列”，于是想把所有可能的排列都尝试一遍。
- **最容易踩的坑**：
  - **忘记剪枝**：在暴力递归里不加 `cur_sum >= best` 的剪枝会导致搜索空间几乎不减。  
  - **位运算错误**：在 DP 中 `mask >> j & 1`、`mask | (1 << j)` 常写错，导致状态转移不正确。  
  - **边界处理**：`full_mask = (1 << n) - 1` 必须确保 `n` 不为 0（本题 n≥1），否则会产生负数掩码。  
- **下次思路**：看到 “n ≤ 14” 或 “子集/配对” 这类约束时，第一时间想到 **位掩码 DP**，先画出状态转移图，再写代码。这样可以立刻把指数枚举压到 `2^n`，避免暴力超时。