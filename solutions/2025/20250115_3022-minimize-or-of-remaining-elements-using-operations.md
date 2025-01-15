# #3022. **使用操作最小化剩余元素的按位或** / Minimize OR of Remaining Elements Using Operations

> 难度：困难 · 标签：Array、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimize-or-of-remaining-elements-using-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k.
In one operation, you can pick any index i of nums such that 0 <= i < nums.length - 1 and replace nums[i] and nums[i + 1] with a single occurrence of nums[i] & nums[i + 1], where & represents the bitwise AND operator.
Return the minimum possible value of the bitwise OR of the remaining elements of nums after applying at most k operations.

**Examples**

**Example 1:**

```
Input: nums = [3,5,3,2,7], k = 2
Output: 3
Explanation: Let's do the following operations:
1. Replace nums[0] and nums[1] with (nums[0] & nums[1]) so that nums becomes equal to [1,3,2,7].
2. Replace nums[2] and nums[3] with (nums[2] & nums[3]) so that nums becomes equal to [1,3,2].
The bitwise-or of the final array is 3.
It can be shown that 3 is the minimum possible value of the bitwise OR of the remaining elements of nums after applying at most k operations.
```

**Example 2:**

```
Input: nums = [7,3,15,14,2,8], k = 4
Output: 2
Explanation: Let's do the following operations:
1. Replace nums[0] and nums[1] with (nums[0] & nums[1]) so that nums becomes equal to [3,15,14,2,8]. 
2. Replace nums[0] and nums[1] with (nums[0] & nums[1]) so that nums becomes equal to [3,14,2,8].
3. Replace nums[0] and nums[1] with (nums[0] & nums[1]) so that nums becomes equal to [2,2,8].
4. Replace nums[1] and nums[2] with (nums[1] & nums[2]) so that nums becomes equal to [2,0].
The bitwise-or of the final array is 2.
It can be shown that 2 is the minimum possible value of the bitwise OR of the remaining elements of nums after applying at most k operations.
```

**Example 3:**

```
Input: nums = [10,7,10,3,9,14,9,4], k = 1
Output: 15
Explanation: Without applying any operations, the bitwise-or of nums is 15.
It can be shown that 15 is the minimum possible value of the bitwise OR of the remaining elements of nums after applying at most k operations.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] < 230
- 0 <= k < nums.length

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个整数 `k`。  
在一次操作中，你可以选择任意满足 `0 <= i < nums.length - 1` 的下标 `i`，并用 `nums[i] & nums[i + 1]`（`&` 表示按位与（bitwise AND）运算）替换掉 `nums[i]` 与 `nums[i + 1]`，即将这两个相邻元素合并为它们的按位与结果。  
在至多进行 `k` 次操作后，返回剩余元素的按位或（bitwise OR）可能的最小值。

---

### 示例

#### 示例 1
**输入**: `nums = [3,5,3,2,7]`, `k = 2`  
**输出**: `3`  
**解释**: 进行如下操作:
1. 用 `nums[0] & nums[1]` 替换 `nums[0]` 与 `nums[1]`，得到 `[1,3,2,7]`。  
2. 用 `nums[2] & nums[3]` 替换 `nums[2]` 与 `nums[3]`，得到 `[1,3,2]`。  
最终数组的按位或为 `3`。可以证明 `3` 是在至多 `k` 次操作后按位或的最小可能值。

#### 示例 2
**输入**: `nums = [7,3,15,14,2,8]`, `k = 4`  
**输出**: `2`  
**解释**: 进行如下操作:
1. 用 `nums[0] & nums[1]` 替换 `nums[0]` 与 `nums[1]`，得到 `[3,15,14,2,8]`。  
2. 再次用 `nums[0] & nums[1]` 替换前两个元素，得到 `[3,14,2,8]`。  
3. 再次用 `nums[0] & nums[1]` 替换前两个元素，得到 `[2,2,8]`。  
4. …（后续操作略）  
最终可以得到按位或为 `2`，且这是最小可能值。

#### 示例 3
**输入**: `nums = [10,7,10,3,9,14,9,4]`, `k = 1`  
**输出**: `15`  
**解释**: 若不进行任何操作，`nums` 的按位或为 `15`。可以证明，即使最多进行一次操作，按位或的最小值仍为 `15`。

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] < 2^30`
- `0 <= k < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的操作都穷举一遍**，把每一种操作序列执行完后，计算剩余数组的 `OR`，取最小值。

- **数据结构**  
  - 使用 **列表**（list）保存当前的数组，列表就像我们平时的“书架”，每个位置放一个数字。  
  - 递归函数 `dfs(arr, ops_left)` 表示“现在的数组是 `arr`，还能再做 `ops_left` 次操作”。递归就像在树形图里不断往下走，每一次分支都代表一次“挑选相邻两个位置并把它们的 `AND` 合并”。

- **为什么正确**  
  - 递归会遍历 **所有** 可能的挑选顺序（从左到右任选任意相邻位置），以及 **所有** 可能的操作次数（0~k 次）。只要遍历完了，就一定能找到最小的 `OR`。

- **时间 / 空间复杂度**  

  - 假设数组长度是 `n`，最多可以做 `k` 次操作。每一次操作把数组长度减 1，递归树的深度最多是 `k`，每层的分支数大约是 `n`（因为可以在 `n-1` 个相邻位置中任选一个），所以总的状态数大致是 `O(n^k)`。  
  - `O(n^k)` 在最坏情况下会非常大（比如 `n=20, k=10`），这就是“暴力”解法的瓶颈——**指数级**增长。  
  - 空间上需要保存递归栈，最深 `k` 层，空间 `O(k)`。

> **大白话**：  
> 如果你把每一步都想象成“把两个相邻的盒子合并成一个盒子”，暴力解就是把所有可能的合并顺序都列出来尝试一遍。随着盒子多、合并次数多，组合的可能性会像树枝一样快速增长，根本算不过来。

#### 代码（Python）

```python
from copy import deepcopy
from typing import List

def brute_min_or(nums: List[int], k: int) -> int:
    """
    暴力递归搜索所有最多 k 次的相邻 AND 合并，返回最小的 OR。
    只适用于 n、k 都很小的情况（比如 n <= 12）。
    """
    n = len(nums)

    # 递归函数：当前数组 arr，剩余可用操作次数 ops
    def dfs(arr: List[int], ops: int) -> int:
        # 计算当前数组的 OR，作为一种可能的答案
        cur_or = 0
        for v in arr:
            cur_or |= v
        # 如果已经没有操作次数可用了，直接返回当前 OR
        if ops == 0:
            return cur_or

        best = cur_or                     # 至少可以不再操作，保持这个 OR
        # 枚举所有可以合并的相邻位置 i,i+1
        for i in range(len(arr) - 1):
            # 生成一次操作后的新数组
            new_arr = arr[:i] + [arr[i] & arr[i + 1]] + arr[i + 2:]
            # 递归求子问题的最小 OR
            best = min(best, dfs(new_arr, ops - 1))
        return best

    return dfs(nums, k)

# -------------------------------------------------
# 示例（仅用于验证，实际使用时请确保 n、k 很小）
if __name__ == "__main__":
    print(brute_min_or([3, 5, 3, 2, 7], 2))   # 输出 3
    print(brute_min_or([7, 3, 15, 14, 2, 8], 4))  # 输出 2
```

> **关键行注释**  
> - `arr[i] & arr[i + 1]`：把相邻两个数做 **按位与**，相当于“把两本书的内容交叉，只留下共同的章节”。  
> - `new_arr = arr[:i] + [...] + arr[i + 2:]`：把原来的两个位置替换成一个新元素，数组长度减 1。  

#### 复杂度

- **时间复杂度**：`O(n^k)`（指数级）——因为每一次操作都有约 `n` 种选择，最多进行 `k` 次。  
- **空间复杂度**：`O(k)`——递归栈的深度最多 `k`，每层只存几条临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有合并顺序**。观察题目可以发现：

1. **我们关心的只有 OR 的每一位是否为 1**。  
   - 高位（比如第 29 位）对答案的影响远大于低位。  
   - 如果我们能够保证某一位在最终 OR 中一定是 0，那么答案就一定小于等于把这位去掉的数。

2. **从高位到低位逐位尝试“能否把它消掉”**。  
   - 设 `mask` 为已经确认可以**去掉**的位的集合（用 1 表示“这位我们已经成功让它在最终 OR 中为 0”）。  
   - 逐位尝试把当前位加入 `mask`（即希望这位也能被消掉），检查 **是否存在一种合并方式，使得所有剩余元素的 AND 在 `mask` 中的位全部为 0，且所需的合并次数 ≤ k**。  
   - 如果可以，则把该位保留在 `mask`；否则说明这位必须保留在最终答案中，`mask` 不加这位。

3. **如何判定“是否可以在 ≤k 次操作下把 mask 中的位全部消掉”**？

   - 把 `mask` 看成“禁区”。我们希望把数组划分成若干段，使得每段内部全部合并后（即取段内所有数的 **按位与**），得到的值在 `mask` 中的位全为 0。  
   - 每合并一次相邻元素，数组长度减 1；把一段合并成一个元素需要 **段长‑1 次操作**。  
   - 如果把数组划分成 `segments` 段，则最少需要的操作次数是 `segments‑1`（因为每段内部合并完后，只剩下每段的代表元素，这些元素已经满足 `AND & mask == 0`，再把段与段之间合并不需要，因为我们已经可以直接停止）。  
   - 因此 **判定只要看能否用 ≤k 次操作把数组划分成 ≤k+1 段**，且每段的 `AND` 与 `mask` 为 0。

4. **贪心划分**  
   - 从左到右遍历数组，维护当前段的累计 `AND`（记作 `cur_and`）。  
   - 如果 `cur_and & mask == 0`，说明当前段已经满足要求，可以继续往后扩展（因为再加元素只会让 `AND` 变得更小，仍然满足）。  
   - 当 `cur_and & mask != 0` 时，说明仅靠当前段无法消掉 `mask` 中的位，需要 **把段结束在前一个位置**，开启新段，从当前元素重新开始累计 `AND`。  
   - 这样得到的段数是 **最少的**（因为每次我们都尽可能把段弄得最长），对应的最小操作次数 `segments‑1`。

5. **特殊情况**  
   - 如果所有元素的整体 `AND` 本身在 `mask` 中已经有 1（即 `total_and & mask != 0`），即使把数组合并成 **唯一一个元素**（最多 `n‑1` 次操作）也无法消掉这些位，答案一定不可能把这些位去掉，直接返回 `False`。

6. **整体算法**  

   ```text
   mask = 0
   for bit from 29 down to 0:
       try_mask = mask | (1 << bit)          # 希望把这位也去掉
       if can_erase(try_mask):                # 检查所需操作次数 ≤ k
           mask = try_mask                    # 成功，保留在 mask 中
   answer = (~mask) & ((1 << 30) - 1)          # 剩下的位即为最小可能的 OR
   ```

   `can_erase(mask)` 的实现就是上面描述的 **贪心划分**，返回 `True` 当且仅当 `segments‑1 ≤ k`。

#### 代码（Python）

```python
from typing import List

def min_or_after_operations(nums: List[int], k: int) -> int:
    """
    最优解：按位贪心 + 贪心分段判定
    时间复杂度 O(30 * n) ≈ O(n)，空间复杂度 O(1)
    """
    n = len(nums)

    # 判断在给定的 mask 下，是否可以用 ≤k 次操作把所有 mask 位消掉
    def can_erase(mask: int) -> bool:
        # 1. 如果整体 AND 本身在 mask 位上有 1，根本消不掉
        total_and = nums[0]
        for v in nums[1:]:
            total_and &= v
        if total_and & mask:
            return False

        # 2. 贪心划分段
        segments = 0          # 已经完成的段数
        cur_and = None        # 当前段的累计 AND
        i = 0
        while i < n:
            if cur_and is None:
                cur_and = nums[i]
            else:
                cur_and &= nums[i]

            # 当前段已经满足 “AND & mask == 0”，可以继续往后扩展
            if cur_and & mask == 0:
                i += 1
                continue

            # 否则当前段无法满足，需要在前一个位置结束段
            segments += 1      # 完成一个段
            cur_and = None     # 开启新段，从当前位置重新开始
            # 注意这里不移动 i，下一轮循环会把 nums[i] 作为新段的第一个元素
        # 处理最后一个段（如果还有未计数的段）
        if cur_and is not None:
            segments += 1

        # 最少需要的操作次数 = segments - 1
        return (segments - 1) <= k

    # 最高位到最低位依次尝试加入 mask
    mask = 0
    for bit in range(29, -1, -1):          # 因为 nums[i] < 2^30
        trial = mask | (1 << bit)
        if can_erase(trial):
            mask = trial                  # 这位可以被消掉，加入 mask

    # 最小的 OR 就是除去 mask 中的位后剩下的位
    full_bits = (1 << 30) - 1
    answer = full_bits ^ mask   # 等价于 full_bits & ~mask
    return answer


# -------------------------------------------------
# 示例
if __name__ == "__main__":
    print(min_or_after_operations([3, 5, 3, 2, 7], 2))          # 3
    print(min_or_after_operations([7, 3, 15, 14, 2, 8], 4))    # 2
    print(min_or_after_operations([10, 7, 10, 3, 9, 14, 9, 4], 1))  # 15
```

> **代码要点注释**  
> - `mask`：记录已经确认可以**消掉**的位（用 1 表示）。  
> - `can_erase(mask)`：核心检查函数。  
>   - 第一步利用整体 `AND` 的性质快速排除不可能的 `mask`。  
>   - 第二步用 **贪心划分**：遍历数组，累计 `cur_and`，一旦 `cur_and & mask != 0`，就必须把当前段结束，开启新段。  
>   - `segments - 1` 正好是把每段内部合并成一个元素所需的最小操作次数。  
> - 最后 `answer = full_bits ^ mask` 把所有可以去掉的位全部清零，剩下的就是**最小可能的 OR**。

#### 复杂度

- **时间复杂度**：`O(30 * n)` ≈ `O(n)`  
  - 最高位到最低位共 30 次（因为 `nums[i] < 2^30`），每次遍历数组一次。  
  - 与暴力解的指数级相比，线性遍历是**天壤之别**，即使 `n = 10^5` 也能轻松跑完。

- **空间复杂度**：`O(1)`  
  - 只使用了常数个整型变量和指针，没有额外的数组或递归栈。

> **对比**：暴力解需要 `O(n^k)` 的时间，几乎不可能在大数据上运行；最优解只要 `O(n)`，几乎是线性的，能在 10⁵ 规模的数据里秒杀。

---

## 心得

- **核心技巧**：**按位贪心 + 贪心分段**。  
  通过逐位尝试能否消除最高位，结合“每段的 AND 必须在 mask 位上为 0” 的判定，把原本的“任意合并顺序”转化为“最少段数”这一容易判断的条件。

- **该技巧适用的题型**  
  1. **按位消除类**：如 “最小化数组的 OR/AND”，需要决定哪些位可以被“擦除”。  
  2. **区间合并最少次数**：比如 “把数组分成若干段，使每段满足某个性质，求最少段数”。  
  3. **二进制位独立决策**：如 “在满足某些位约束的情况下，最大化/最小化某个数”，常用从高位到低位的贪心。

- **一句话总结解题钥匙**  
  > **“把每一位看成独立的‘能否被清零’问题，用贪心划分段来计数所需最少操作，逐位构造答案”。**

---

## 反思

- **第一反应**：看到“相邻 AND 合并”和“求最终 OR”，本能想到**枚举合并顺序**（即暴力递归），因为这是一种最直接的把操作模型实现出来的办法。

- **最容易踩的坑**  
  1. **忽视整体 AND 的限制**：即使可以无限次合并，某些位在所有元素的 AND 中始终为 1，根本无法消掉。忘记这点会导致在 `can_erase` 中出现无限循环或错误的判断。  
  2. **段划分的细节**：在贪心划分时，需要在 “当前段的 AND 已经不含 mask 位” 时继续扩展，而不是立即结束段，否则会产生不必要的额外段，导致误判 `segments-1 > k`。  
  3. **位数范围**：题目给出 `nums[i] < 2^30`，所以循环的最高位是 29（从 0 开始计数），写成 31 位会多算无意义的高位。  

- **下次遇到同类题的第一步**  
  > **“先把位视作独立约束，尝试从最高位往下逐位消除；随后把‘能否消除’转化为最小段数/最小操作次数的判定”。**  

这样一步步把原本看似复杂的全局操作，拆解成“位‑层面” + “区间‑层面”的两个简单子问题，就能轻松得到最优解。