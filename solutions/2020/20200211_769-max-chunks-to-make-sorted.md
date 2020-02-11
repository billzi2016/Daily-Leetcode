# #769. 最大分块使数组有序 / Max Chunks To Make Sorted

> 难度：中等 · 标签：Array、Stack、Greedy、Sorting、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/max-chunks-to-make-sorted/)

---

## 题目（英文原版）

**Description**

You are given an integer array arr of length n that represents a permutation of the integers in the range [0, n - 1].
We split arr into some number of chunks (i.e., partitions), and individually sort each chunk. After concatenating them, the result should equal the sorted array.
Return the largest number of chunks we can make to sort the array.

**Examples**

**Example 1:**

```
Input: arr = [4,3,2,1,0]
Output: 1
Explanation:
Splitting into two or more chunks will not return the required result.
For example, splitting into [4, 3], [2, 1, 0] will result in [3, 4, 0, 1, 2], which isn't sorted.
```

**Example 2:**

```
Input: arr = [1,0,2,3,4]
Output: 4
Explanation:
We can split into two chunks, such as [1, 0], [2, 3, 4].
However, splitting into [1, 0], [2], [3], [4] is the highest number of chunks possible.
```

**Constraints**

- n == arr.length
- 1 <= n <= 10
- 0 <= arr[i] < n
- All the elements of arr are unique.

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的整数数组 `arr`，它是区间 `[0, n - 1]` 内所有整数的一个排列（permutation）。  
我们可以将 `arr` 划分为若干块（chunks），对每一块分别进行排序，然后按块的顺序拼接起来。拼接后的结果应当等于整体有序的数组。  
返回能够使数组有序的最大块数。

**示例 1**  
```text
Input: arr = [4,3,2,1,0]
Output: 1
Explanation:
将数组划分为两个或更多块都无法得到要求的结果。例如，将其划分为 [4, 3], [2, 1, 0]，分别排序后得到 [3, 4, 0, 1, 2]，这不是有序的。
```

**示例 2**  
```text
Input: arr = [1,0,2,3,4]
Output: 4
Explanation:
我们可以划分为两块，例如 [1, 0], [2, 3, 4]。  
但若划分为 [1, 0], [2], [3], [4]，则得到了可能的最大块数。
```

**约束条件**  
- `n == arr.length`  
- `1 <= n <= 10`  
- `0 <= arr[i] < n`  
- `arr` 中的所有元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都枚举一遍**，然后检查每一种切分在各块内部分别排序后，拼接起来是否等于 `[0,1,2,…,n‑1]`。  

- **数据结构**：我们可以用 **递归 + 列表** 来生成切分。递归相当于在“切分点”上做选择，就像在一本书里把每一页都决定是单独成章还是和后面的页一起成章。  
- **正确性**：只要遍历了**所有**合法的切分方式，就不会错过最优解。因为题目要求返回“最多能分成多少块”，只要把每一种切分都算一遍，取最大块数即可。  

#### 代码（Python）

```python
from typing import List

def max_chunks_to_make_sorted_bruteforce(arr: List[int]) -> int:
    n = len(arr)

    # 递归枚举所有切分方式
    def dfs(idx: int, cur_chunks: int) -> int:
        """从下标 idx 开始继续切分，cur_chunks 为已经形成的块数，返回最大块数"""
        if idx == n:                      # 已经走到数组末尾，合法切分结束
            return cur_chunks

        best = 0
        # 尝试把 arr[idx:next_idx] 作为下一块
        for next_idx in range(idx + 1, n + 1):
            # 取出当前块
            chunk = arr[idx:next_idx]
            # 把块内部排序后放回原位，观察拼接后是否仍然是递增的
            # 为了不破坏原数组，这里拷贝一份临时数组做检查
            tmp = arr[:idx] + sorted(chunk) + arr[next_idx:]
            # 检查 tmp 前缀是否已经是 0..next_idx-1（因为前面已经保证有序）
            if tmp[:next_idx] == list(range(next_idx)):
                # 如果前缀合法，就可以在这里划块，继续往后找
                best = max(best, dfs(next_idx, cur_chunks + 1))
        return best

    return dfs(0, 0)
```

> **注释**  
> - `dfs` 是深度优先搜索，每一次递归都尝试在当前位置放置一个“切分点”。  
> - `tmp[:next_idx] == list(range(next_idx))` 用来判断**到目前为止**（包括当前块）拼接后是否已经是 `[0,1,…,next_idx‑1]`，只有满足这个条件，后面的块才有可能继续保持整体有序。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。因为每个位置都有“切/不切”两种选择，等价于遍历所有子集。对 `n=10` 还能接受，但 `n` 稍大就会炸掉。  
- **空间复杂度**：`O(n)`，递归栈的深度最坏是 `n`，再加上临时拷贝的数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量无效的切分**：我们在很多不可能形成合法块的地方仍然尝试划分，导致指数级搜索。  
观察题目有两大关键点：

1. **数组是 `0..n‑1` 的一个排列**，也就是说若我们已经把前 `k+1` 个数排好序，它们一定恰好是 `[0,1,…,k]`。  
2. 在一个块内部，无论怎么排列，只要**块内的最大值恰好等于块的右边界下标**，那么把这个块单独排序后，左边的所有数就已经是 `[0..k]`，右边的数仍然保持相对顺序，不会影响后面的块。

基于这点，只需要一次遍历，**记录到当前位置的最大值** `max_sofar`。当 `max_sofar == i`（`i` 为当前下标）时，说明 `0..i` 这段已经可以独立成块——因为所有出现的数都不大于 `i`，而且由于是排列，恰好包含了 `0..i`。此时我们可以把块数加一，继续往后走。

这就是 **贪心 + 前缀最大** 的思路，时间只需要一次线性扫描。

> **类比**：想象一条河上有若干座桥，每座桥的编号是河两岸的石头编号。我们从左往右走，手里拿着最大的石头编号 `max_sofar`。当手里最大的编号正好等于我们站的那块石头的编号时，说明左边的所有石头已经完整收集（从 `0` 到 `i`），可以在这里“建一座桥”，把左边和右边分开。

#### 代码（Python）

```python
from typing import List

def max_chunks_to_make_sorted(arr: List[int]) -> int:
    """
    贪心算法：遍历数组，维护当前前缀的最大值 max_sofar。
    当 max_sofar == 当前下标 i 时，说明可以在 i 位置切块。
    """
    chunks = 0          # 已经形成的块数
    max_sofar = -1      # 前缀最大值，初始为 -1（因为数组最小值是 0）

    for i, v in enumerate(arr):
        # 更新前缀最大值
        if v > max_sofar:
            max_sofar = v          # 关键行：保持到目前为止出现的最大数

        # 若最大值恰好等于下标 i，说明 0..i 已经完整出现
        if max_sofar == i:
            chunks += 1            # 可以在这里切块
            # 这里不需要重置 max_sofar，因为后面的块仍然基于全局最大值判断

    return chunks
```

> **关键行解释**  
> - `max_sofar = max(max_sofar, v)`：相当于在“背包”里记录最重的石头。  
> - `if max_sofar == i:`：只有当背包里最重的石头恰好是我们站的这块石头的编号时，左边的石头才齐全，才能安全建桥。

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  - 与暴力解的 `O(2^n)` 对比，**线性**时间在任何规模的输入下都能轻松跑完。  
- **空间复杂度**：`O(1)`，只用了常数个变量 (`chunks`, `max_sofar`)。  

---

## 心得

- **核心技巧**：**前缀最大 + 贪心**。只要在遍历时维护到当前位置的最大值，就能立刻判断是否可以在此处分块。  
- **适用场景**：  
  1. **Max Chunks To Make Sorted II**（数组可能有重复元素，需要用前缀最大 + 后缀最小）。  
  2. **Partition Array Into Disjoint Intervals**（求最小的左侧区间，使左侧最大 ≤ 右侧最小）。  
  3. **Split Array Largest Sum**（二分+前缀和的思想，同样是把数组按条件切分）。  
- **一句话总结**：只要**左边的最大值不超过当前下标**，左边就已经完整，可以立即切块。

---

## 反思

- **第一反应**：看到“把数组分块后各自排序，整体有序”，自然会想到**枚举所有切分**——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记利用“排列”这一重要信息，导致把问题当成一般的数组来做，错失 O(n) 的简化。  
  - 在实现贪心时误以为需要在每次切块后把 `max_sofar` 重新置零，其实不需要——因为后面的块仍然只看**整体**的最大值是否已满足条件。  
- **下次遇到同类题**：第一步先**思考能否用“前缀/后缀信息”一次遍历得到答案**，尤其是涉及“所有元素都已出现”或“最大 ≤ 某值”的条件时。这样往往能直接推出 O(n) 的贪心或双指针解法。