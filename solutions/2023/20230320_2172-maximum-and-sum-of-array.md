# #2172. 最大 AND 和 / Maximum AND Sum of Array

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-and-sum-of-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and an integer numSlots such that 2 * numSlots >= n. There are numSlots slots numbered from 1 to numSlots.
You have to place all n integers into the slots such that each slot contains at most two numbers. The AND sum of a given placement is the sum of the bitwise AND of every number with its respective slot number.
Return the maximum possible AND sum of nums given numSlots slots.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5,6], numSlots = 3
Output: 9
Explanation: One possible placement is [1, 4] into slot 1, [2, 6] into slot 2, and [3, 5] into slot 3. 
This gives the maximum AND sum of (1 AND 1) + (4 AND 1) + (2 AND 2) + (6 AND 2) + (3 AND 3) + (5 AND 3) = 1 + 0 + 2 + 2 + 3 + 1 = 9.
```

**Example 2:**

```
Input: nums = [1,3,10,4,7,1], numSlots = 9
Output: 24
Explanation: One possible placement is [1, 1] into slot 1, [3] into slot 3, [4] into slot 4, [7] into slot 7, and [10] into slot 9.
This gives the maximum AND sum of (1 AND 1) + (1 AND 1) + (3 AND 3) + (4 AND 4) + (7 AND 7) + (10 AND 9) = 1 + 1 + 3 + 4 + 7 + 8 = 24.
Note that slots 2, 5, 6, and 8 are empty which is permitted.
```

**Constraints**

- n == nums.length
- 1 <= numSlots <= 9
- 1 <= n <= 2 * numSlots
- 1 <= nums[i] <= 15

---

## 题目（中文翻译）

**描述**  
给定一个长度为 `n` 的整数数组 `nums` 和一个整数 `numSlots`，满足 `2 * numSlots >= n`。有 `numSlots` 个槽位，编号从 `1` 到 `numSlots`。  
你需要将所有 `n` 个整数放入这些槽位中，使得每个槽位至多容纳两个数字。某种放置方式的 **AND 和** 定义为：每个数字与其所在槽位编号进行按位与（bitwise AND）运算的结果之和。  
返回在 `numSlots` 个槽位下，`nums` 能得到的最大可能的 **AND 和**。

**示例**

**示例 1**  
输入: `nums = [1,2,3,4,5,6]`, `numSlots = 3`  
输出: `9`  
解释: 一种可能的放置方式是将 `[1, 4]` 放入槽位 `1`，`[2, 6]` 放入槽位 `2`，`[3, 5]` 放入槽位 `3`。  
这得到的最大 AND 和为  
`(1 AND 1) + (4 AND 1) + (2 AND 2) + (6 AND 2) + (3 AND 3) + (5 AND 3) = 1 + 0 + 2 + 2 + 3 + 1 = 9`。

**示例 2**  
输入: `nums = [1,3,10,4,7,1]`, `numSlots = 9`  
输出: `24`  
解释: 一种可能的放置方式是将 `[1, 1]` 放入槽位 `1`，`[3]` 放入槽位 `3`，`[4]` 放入槽位 `4`，`[7]` 放入槽位 `7`，`[10]` 放入槽位 `9`。  
这得到的最大 AND 和为  
`(1 AND 1) + (1 AND 1) + (3 AND 3) + (4 AND 4) + (7 AND 7) + (10 AND 9) = 1 + 1 + 3 + 4 + 7 + 8 = 24`。  
注意，槽位 `2、5、6、8` 为空是允许的。

**约束条件**  
- `n == nums.length`  
- `1 <= numSlots <= 9`  
- `1 <= n <= 2 * numSlots`  
- `1 <= nums[i] <= 15`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每个数字** 按顺序尝试放进 **每个槽位**（槽位编号 1~numSlots），并记录每个槽位已经放了几个数（最多 2 个）。  
这其实是一次「全排列」加「选位」的过程：  

1. 依次取出 `nums` 中的第 `i` 个数。  
2. 在所有还能再放一个数的槽位（即当前放了 0 或 1 个数的槽）中挑一个放进去。  
3. 继续放下一个数，直到所有 `n` 个数都放完。  

**用到的数据结构**  

| 数据结构 | 类比 | 作用 |
|----------|------|------|
| `cnt[slot]`（长度 `numSlots+1` 的数组） | 像一本笔记本，每一页记录该槽已经放了几本书 | 记录每个槽位当前已放的数字个数，确保不超过 2 |
| `ans`（全局最大值） | 像比赛的最高分 | 保存遍历过程中出现的最大 AND 和 |

**为什么正确**  

因为我们把所有可能的放置方式都遍历一遍，必然会找到最优的那一种。只要在递归结束时计算当前的 AND 和并和全局答案比较，就能得到最大值。

**时间/空间复杂度**  

- **时间复杂度**：每个数字最多有 `numSlots` 种放法（实际上只有还能放的槽），所以最坏情况是 `O(numSlots^n)`。  
  - 这里的 `O` 符号可以理解为“数量级”。如果 `numSlots=3、n=6`，则大约是 `3^6 = 729` 种尝试；如果 `numSlots=9、n=18`，则是 `9^18`，天文数字，根本跑不完。  
- **空间复杂度**：递归栈深度为 `n`，再加上 `cnt` 数组，都是 `O(n + numSlots)`，对本题来说几乎可以忽略不计。

#### 代码（Python）

```python
from typing import List

def maximumANDSum_bruteforce(nums: List[int], numSlots: int) -> int:
    n = len(nums)
    cnt = [0] * (numSlots + 1)          # cnt[i] 表示槽 i 已经放了几个数，0/1/2
    best = 0

    def dfs(idx: int, cur: int) -> None:
        """尝试把第 idx 个数放进某个槽，cur 为当前的 AND 和"""
        nonlocal best
        if idx == n:                     # 所有数都放完了
            best = max(best, cur)
            return

        # 把 nums[idx] 放进任意还能再放一个数的槽
        for slot in range(1, numSlots + 1):
            if cnt[slot] < 2:            # 槽位还能容纳
                cnt[slot] += 1
                dfs(idx + 1, cur + (nums[idx] & slot))
                cnt[slot] -= 1           # 恢复现场，回溯

    dfs(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(numSlots^n)`（指数级），因为每个数字都有 `numSlots` 种选择。  
- **空间复杂度**：`O(n + numSlots)`，主要是递归栈和计数数组。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于大量的重复搜索：  
- 同样的“已经放了哪些数”状态会被多次遍历。  
- 只要记住已经使用的槽位情况，就不必再从头搜索。

**核心想法**：用 **位掩码（bitmask）** 表示「哪些槽位已经被占用了多少次」。  
因为每个槽位最多放 **2** 个数，我们可以把每个槽位用 **两位二进制** 来记录：

| 槽位 i | 两位二进制 | 含义 |
|-------|-----------|------|
| 1     | 00        | 0 个数 |
| 1     | 01        | 1 个数 |
| 1     | 10        | 2 个数 |
| 2     | 11 01 …   | 依次类推 |

对 `numSlots ≤ 9`，最多需要 `2 * 9 = 18` 位，完全可以放进一个普通的整数（Python 的 int 没有限制）。

**状态**  
- `mask`：一个整数，二进制的第 `2*i`、`2*i+1` 位（从 0 开始计数）表示槽 `i+1` 已放了多少个数。  
- `i`：已经处理了前 `i` 个数字（`0 ≤ i ≤ n`）。

**转移**  
对第 `i` 个数字 `nums[i]`，遍历所有 **仍有空位** 的槽 `s`（即对应的两位二进制不是 `10`），把它放进去得到新掩码 `newMask`，并把贡献 `nums[i] & s` 加到当前分数上。

**动态规划（记忆化搜索）**  
因为 `mask` 的取值最多 `3^numSlots`（每个槽有 3 种状态），而 `numSlots ≤ 9`，所以状态总数 ≤ `3^9 = 19683`，非常小。我们用 **递归 + 记忆化（@lru_cache）** 来实现 DP：

```
dp(i, mask) = max   dp(i+1, mask') + (nums[i] & slot)
               slot 可放（mask 对应位 < 2）
```

递归终止条件是 `i == n`（所有数字都已放），返回 0。

**为什么只需要 mask 而不需要 cnt 数组**  
因为 mask 已经完整描述了每个槽的使用次数，cnt 只是 mask 的展开形式。

**类比**  
把每个槽位想象成 **两格的抽屉**，mask 就是记录每个抽屉里放了几件物品的「抽屉钥匙」——只要钥匙相同，抽屉的状态就相同。

#### 代码（Python）

```python
from functools import lru_cache
from typing import List

def maximumANDSum(nums: List[int], numSlots: int) -> int:
    """
    使用位掩码 + 记忆化搜索求最大 AND 和
    """
    n = len(nums)

    # 预处理：把每个槽位的两位二进制位置写成数组，方便后面快速判断/修改
    # slot_bit[i] = (低位, 高位) 在 mask 中的索引
    slot_bit = [(2 * i, 2 * i + 1) for i in range(numSlots)]

    @lru_cache(maxsize=None)
    def dp(idx: int, mask: int) -> int:
        """
        已经处理了前 idx 个数，当前的槽位使用情况用 mask 表示。
        返回从 idx 开始的最大 AND 和。
        """
        if idx == n:                     # 所有数都放完了
            return 0

        best = 0
        cur_num = nums[idx]

        # 枚举所有可能放入的槽位
        for slot in range(1, numSlots + 1):
            low, high = slot_bit[slot - 1]      # 该槽在 mask 中的两位位置
            # 取出这两位的值（0,1,2）
            used = (mask >> low) & 0b11        # 只取低两位即可
            if used < 2:                       # 还能放
                # 把这两位加 1，得到新的 mask
                new_mask = mask + (1 << low)   # 只需要在低位加 1，因为两位是 00/01/10，低位加 1 就是状态转移
                # 递归求后面的最大值，加上本次贡献
                cand = dp(idx + 1, new_mask) + (cur_num & slot)
                if cand > best:
                    best = cand

        return best

    return dp(0, 0)      # 从第 0 个数、所有槽位空开始
```

> **代码说明**  
> - `slot_bit` 把每个槽位对应的两位二进制在整数中的位置记录下来，后面取值和更新时更直观。  
> - `used = (mask >> low) & 0b11` 把 mask 右移到对应位置，再取最低两位 (`0b11`)，得到该槽已经使用的次数。  
> - `new_mask = mask + (1 << low)` 只在低位加 1，即把 `00 → 01`、`01 → 10`。因为我们保证 `used < 2`，不会出现进位到第三位。  
> - `@lru_cache` 把已经算过的 `(idx, mask)` 结果记住，避免重复计算，时间从指数级降到 `O(n * 3^numSlots)`。

#### 复杂度

- **时间复杂度**：`O(n * 3^numSlots)`  
  - `3^numSlots` 是所有可能的槽位使用状态数（每个槽有 0、1、2 三种状态）。`n ≤ 2 * numSlots ≤ 18`，所以整体最多约 `18 * 19683 ≈ 3.5e5` 次计算，完全可以在毫秒级跑完。  
  - 与暴力解相比，指数从 `numSlots^n` 降到了 `3^numSlots`，大幅提升。

- **空间复杂度**：`O(n * 3^numSlots)`（缓存表的大小）加上递归栈深度 `O(n)`，总体仍在几万级别，内存占用几 MB。

---

## 心得  

- **核心技巧**：**位掩码 + 记忆化搜索（DP）**，把「每个槽位还能放几个」压缩进一个整数，利用缓存避免重复子问题。  
- **适用的题型**  
  1. 「每个位置/对象有固定容量」的分配类问题（如 “Maximum AND Sum of Array”、 “Maximum Sum of Selected Elements with Limited Capacity”）。  
  2. 「状态只有几种」且 `状态数 ≤ 3^k`（k ≤ 9~10） 的组合优化问题（如 “Maximum Score From Performing Multiplication Operations”）。  
  3. 「需要遍历所有子集/排列」但可以用位运算压缩状态的 DP（如 “Maximum Compatibility Score Sum”）。  

- **一句话总结解题钥匙**：**把“每个槽位还能放几个人”用两位二进制压进一个整数，用记忆化搜索一次遍历所有合法放置，即可在指数级别的状态空间里快速找到最优解。**

---

## 反思  

- **第一反应**：看到“每个槽位最多放两个数”，立刻想到“枚举所有放法”，于是写出暴力递归。  
- **最容易踩的坑**  
  1. **位运算的进位**：在更新掩码时必须保证不会把 `01` 加成 `10` 再进位到第三位，正确做法是只在低位加 `1`（因为我们永远不会在已经是 `10` 时再加）。  
  2. **掩码位的对应关系**：忘记把槽位从 1 开始映射到掩码的第 `2*(slot-1)` 位，导致状态错误。  
  3. **递归终止条件**：一定要在 `idx == n` 时返回 0，防止遗漏最后一个数字的贡献。  

- **下次遇到同类题**：第一步先**判断每个位置的容量是否有限且小**，如果是，就考虑**用固定长度的位掩码表示状态**，再用**记忆化搜索/DP**在状态空间上做遍历。这样既能保证正确性，又能把指数级搜索压到可接受的规模。