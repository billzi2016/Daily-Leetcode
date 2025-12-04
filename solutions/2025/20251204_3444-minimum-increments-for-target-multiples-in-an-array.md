# #3444. 数组中使每个目标数拥有倍数的最少增量次数 / Minimum Increments for Target Multiples in an Array

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Bit Manipulation、Number Theory、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-increments-for-target-multiples-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given two arrays, nums and target.
In a single operation, you may increment any element of nums by 1.
Return the minimum number of operations required so that each element in target has at least one multiple in nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], target = [4]
Output: 1
Explanation:
The minimum number of operations required to satisfy the condition is 1.
```

**Example 2:**

```
Input: nums = [8,4], target = [10,5]
Output: 2
Explanation:
The minimum number of operations required to satisfy the condition is 2.
```

**Example 3:**

```
Input: nums = [7,9,10], target = [7]
Output: 0
Explanation:
Target 7 already has a multiple in nums, so no additional operations are needed.
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 1 <= target.length <= 4
- target.length <= nums.length
- 1 <= nums[i], target[i] <= 104

---

## 题目（中文翻译）

**描述**  
给定两个数组 `nums` 和 `target`。一次操作可以将 `nums` 中的任意元素加 `1`。返回满足 `target` 中每个元素在 `nums` 中至少存在一个它的倍数（multiple）所需的最少操作次数。

**示例 1**  
**输入**: `nums = [1,2,3]`, `target = [4]`  
**输出**: `1`  
**解释**:  
只需要对 `nums` 中的元素进行一次增量，使其出现 `4` 的倍数（如 `4`），即可满足条件，最少操作次数为 `1`。

**示例 2**  
**输入**: `nums = [8,4]`, `target = [10,5]`  
**输出**: `2`  
**解释**:  
对 `8` 增加 `2` 得到 `10`（满足 `10` 的倍数），对 `4` 增加 `1` 得到 `5`（满足 `5` 的倍数），共需 `2` 次操作。

**示例 3**  
**输入**: `nums = [7,9,10]`, `target = [7]`  
**输出**: `0`  
**解释**:  
`7` 已经是 `nums` 中的一个元素，本身即为 `7` 的倍数（multiple），因此不需要任何操作。

**约束条件**  
- `1 <= nums.length <= 5 * 10^4`  
- `1 <= target.length <= 4`  
- `target.length <= nums.length`  
- `1 <= nums[i], target[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个 `target` 分别找一个 `nums` 元素，让它变成 `target` 的倍数**。  
我们可以遍历所有 `nums`，对每个 `target` 计算把该元素增到最近的倍数需要多少次加 1：

```
need = (target - nums[i] % target) % target
```

- 如果 `nums[i]` 本身已经是 `target` 的倍数，`need` 为 0。  
- 否则把它加到下一个 `target` 的整数倍即可。

把每个 `target` 找到各自的“最近倍数”后，把所有 `need` 加起来，就是一种合法的操作次数。

> **生活化类比**：  
> 把 `nums` 看成一排书架上的书本，`target` 是我们希望看到的书的页码。每本书的页码可以往后翻（只能加不能减），我们要把每本书翻到恰好是某个目标页码的整数倍，这样就能“满足”该目标。

这个办法一定能得到答案，因为我们把每个目标都单独满足了。  
但它 **没有利用** 同一本 `nums` 同时满足多个 `target` 的可能性——如果一条书架可以一次性翻到同时是 3 和 5 的倍数（即 15 的倍数），我们就能省掉很多翻页次数。

#### 代码（Python）

```python
import math
from typing import List

def min_operations_bruteforce(nums: List[int], target: List[int]) -> int:
    m = len(target)
    total = 0
    # 对每个 target，找 nums 中增幅最小的那一个
    for t in target:
        best = float('inf')
        for x in nums:
            # 把 x 增到下一个 t 的倍数需要的次数
            inc = (t - x % t) % t
            best = min(best, inc)
        total += best
    return total
```

> **关键行中文注释**  
> - `inc = (t - x % t) % t`：先算出 `x` 除以 `t` 的余数，若余数为 0 则不需要增；否则补足到下一个倍数。  
> - `best = min(best, inc)`：在所有 `nums` 中挑出增幅最少的那一本。

#### 复杂度

- **时间复杂度**：`O(n * m)`，其中 `n = len(nums)`，`m = len(target)`。  
  直白来说，就是把每本书（`n` 本）和每个目标（`m` 个）都配对一次，最多做 `n*m` 次加法/取余运算。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于我们把每个 `target` 都单独配一条 `nums`，没有利用“一条书可以同时满足多个目标”。  
因为 `target` 的数量最多只有 **4**，我们可以把它们的组合用 **位掩码（bitmask）** 表示，枚举所有可能的子集，然后把每条 `nums` 变成对应子集所有目标的 **公共倍数**。

**核心概念**  

1. **子集的公共倍数**  
   - 若一条 `nums` 同时要满足目标集合 `{t1, t2, …}`，它必须是这些目标的 **最小公倍数（LCM）** 的倍数。  
   - 例如要同时满足 `3` 和 `5`，只要把它变成 `15`（或 `30、45…）的倍数即可。  

2. **把 “把 nums[i] 变成子集的倍数” 的代价算出来**  
   - 设子集对应的 LCM 为 `L`，把 `nums[i]` 增到最近的 `L` 的倍数需要的次数同样是  
     `inc = (L - nums[i] % L) % L`。

3. **位掩码 DP**  
   - `mask`（0~(1<<m)-1）表示已经被覆盖的目标集合。  
   - `dp[mask]` = 使用已经遍历过的 `nums`，最小的操作次数，使得 `mask` 对应的目标全部被满足。  
   - 初始 `dp[0] = 0`（什么都不覆盖，代价 0），其余设为 `∞`。  
   - 对每个 `nums[i]`，我们尝试让它负责 **任意非空子集 `sub`**（子集对应的位掩码），得到新状态 `new_mask = mask | sub`，更新  
     `dp[new_mask] = min(dp[new_mask], dp[mask] + inc(i, sub))`。  
   - 由于 `m ≤ 4`，子集总数只有 `2^4 = 16`，遍历所有 `sub` 非常快。

4. **答案**  
   - 最终我们需要覆盖全部目标，即 `full_mask = (1<<m)-1`。答案是 `dp[full_mask]`。

**为什么正确**  

- 对每条 `nums[i]`，我们穷举它可能承担的目标子集（包括只负责一个目标的情况），并记录最小代价。  
- DP 的状态转移保证了 **每条 `nums` 只使用一次**（因为我们在遍历 `nums` 时只能基于之前的状态来更新），而 **子集可以共享同一条 `nums`**（因为子集本身可能包含多个目标）。  
- 所有可能的覆盖方式都在 DP 中被枚举，最小值自然就是全局最优。

> **类比**：  
> 想象有几位老师（`target`）需要监督学生（`nums`）。每位老师只要求学生的成绩是自己的整数倍。我们可以把几位老师的要求合并成“一位老师要求成绩是 12 的倍数”，这样只需要让一个学生达到 12 的倍数即可同时满足这几位老师的要求。DP 就是在找 **哪几位老师合并**、**哪个学生负责**，从而让整体加分次数最少。

#### 代码（Python）

```python
import math
from typing import List

INF = 10 ** 18

def lcm(a: int, b: int) -> int:
    """返回 a 与 b 的最小公倍数"""
    return a // math.gcd(a, b) * b

def min_operations(nums: List[int], target: List[int]) -> int:
    m = len(target)                     # target 最多 4 个
    full_mask = (1 << m) - 1            # 需要覆盖的全部位

    # 1. 预处理每个子集对应的 LCM
    subset_lcm = [1] * (1 << m)         # 0 号子集不使用，保持 1（不会被取模）
    for mask in range(1, 1 << m):
        # 取出子集的最低位，递归合并 LCM
        low_bit = mask & -mask                     # 例如 1010 -> 0010
        idx = (low_bit.bit_length() - 1)           # 该位对应的目标下标
        prev = mask ^ low_bit                      # 去掉最低位后的子集
        subset_lcm[mask] = lcm(subset_lcm[prev], target[idx])

    # 2. DP 初始化
    dp = [INF] * (1 << m)
    dp[0] = 0

    # 3. 枚举每个 nums[i]，尝试让它负责任意非空子集
    for x in nums:
        # 对当前的 dp 复制一份，防止同一条 nums 在本轮中被使用多次
        ndp = dp[:]          # 深拷贝当前状态
        for mask in range(1 << m):
            if dp[mask] == INF:
                continue     # 这个状态不可达，直接跳过
            # 遍历所有非空子集 sub
            sub = 1
            while sub < (1 << m):
                # 只考虑 sub 与已覆盖的 mask 没有交集的情况
                if (sub & mask) == 0:
                    L = subset_lcm[sub]            # 子集对应的 LCM
                    inc = (L - x % L) % L          # 把 x 增到最近的 L 的倍数
                    new_mask = mask | sub
                    ndp[new_mask] = min(ndp[new_mask], dp[mask] + inc)
                sub += 1
        dp = ndp  # 用新状态替换旧状态，进入下一个 nums

    return dp[full_mask]
```

**关键行中文注释**  

| 行号 | 说明 |
|------|------|
| `subset_lcm[mask] = lcm(subset_lcm[prev], target[idx])` | 递归合并子集的 LCM：先算除去最低位的子集 LCM，再与该位对应的目标取 LCM。 |
| `ndp = dp[:]` | 为了保证每条 `nums` 只使用一次，先把上一次的 DP 结果复制出来，再基于它更新。 |
| `if (sub & mask) == 0:` | 只有当子集 `sub` 中的目标尚未被覆盖时才考虑，让当前 `nums` 负责这部分新目标。 |
| `inc = (L - x % L) % L` | 计算把 `x` 增到最近的 `L`（子集 LCM）的倍数需要的操作次数。 |
| `ndp[new_mask] = min(ndp[new_mask], dp[mask] + inc)` | DP 转移：把已有代价 `dp[mask]` 加上本次增幅 `inc`，得到覆盖 `new_mask` 的更小代价。 |

#### 复杂度

- **时间复杂度**：`O(n * 2^m * 2^m)` 里实际常数非常小。  
  - `2^m`（最多 16）是子集的总数；  
  - 对每个 `nums[i]` 我们遍历所有 `mask`（16）并在内部遍历所有 `sub`（16），所以每条 `nums` 最多做 `16 * 16 = 256` 次简单算术。  
  - 整体约 `256 * n ≤ 1.3 * 10^7`，在 5·10⁴ 的规模下毫秒级运行。  

- **空间复杂度**：`O(2^m)`（约 16）用于 DP 表和子集 LCM，几乎可以忽略不计。

相较于暴力 `O(n*m)`，这里的 **时间提升不在于大幅度降低数量级**（本身已经很小），而在于**正确地利用多个目标可以共享同一条 `nums`**，从而在最坏情况下可以把操作次数从数十次降到个位数。

---

## 心得

- **核心技巧**：**位掩码动态规划 + 最小公倍数**。  
  把少量目标的组合抽象成子集，用 LCM 表示“同时满足这些目标的最低要求”，再用 DP 在每个数组元素上决定它承担哪个子集。

- **适用题型**（类似思路）  
  1. “让数组中的若干数分别覆盖若干要求，每个数可以一次性满足多个要求”——如 *Minimum Number of Operations to Make Array Good*（子集覆盖）。  
  2. “给定若干颜色，需要最少的笔刷次数把每个颜色的格子染成同色”——可以把颜色集合用位掩码表示。  
  3. “把若干机器的工作时间对齐到共同的周期”——使用 LCM + DP。

- **一句话总结解题钥匙**：**把多个目标合并为它们的 LCM，用位掩码 DP 枚举每条数组元素负责的目标子集，取最小增幅即可**。

---

## 反思

- **第一反应**：直接为每个 `target` 找最近的倍数，忽视了不同目标可以共享同一条 `nums` 的可能性。  
- **最容易踩的坑**  
  1. **LCM 可能溢出**：在 Python 中整数无限大，但实际题目数据 `target[i] ≤ 10⁴`，最多四个数的 LCM 仍在可接受范围。若出现更大范围，需要提前检查是否超过 `10+7` 等限制。  
  2. **子集遍历重复**：在 DP 中必须保证同一条 `nums` 只使用一次，故需要在每轮使用 `ndp = dp[:]` 再更新，否则同一元素可能被多次计入导致错误的更小代价。  
  3. **空子集的处理**：`mask = 0`（什么都不覆盖）不需要增幅，保持 LCM 为 1 即可，防止除以 0。  

- **下次遇到同类题**：第一步先**判断目标数量是否足够小**（通常 ≤ 20），若是则考虑**位掩码 DP**；随后**把“同时满足多个目标”转化为“满足它们的公共约束（如 LCM、最大公约数、最大值等）**，再在 DP 中枚举每个元素负责的子集。这样既能保证完整性，又能得到最优解。