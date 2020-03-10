# #801. 最小交换次数使序列递增 / Minimum Swaps To Make Sequences Increasing

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-swaps-to-make-sequences-increasing/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays of the same length nums1 and nums2. In one operation, you are allowed to swap nums1[i] with nums2[i].
Return the minimum number of needed operations to make nums1 and nums2 strictly increasing. The test cases are generated so that the given input always makes it possible.
An array arr is strictly increasing if and only if arr[0] < arr[1] < arr[2] < ... < arr[arr.length - 1].

**Examples**

**Example 1:**

```
Input: nums1 = [1,3,5,4], nums2 = [1,2,3,7]
Output: 1
Explanation: 
Swap nums1[3] and nums2[3]. Then the sequences are:
nums1 = [1, 3, 5, 7] and nums2 = [1, 2, 3, 4]
which are both strictly increasing.
```

**Example 2:**

```
Input: nums1 = [0,3,5,8,9], nums2 = [2,1,4,6,9]
Output: 1
```

**Constraints**

- 2 <= nums1.length <= 105
- nums2.length == nums1.length
- 0 <= nums1[i], nums2[i] <= 2 * 105

---

## 题目（中文翻译）

给定两个长度相同的整数数组（integer arrays）`nums1` 和 `nums2`。在一次操作（operation）中，你可以将 `nums1[i]` 与 `nums2[i]` 进行交换（swap）。  
返回使 `nums1` 和 `nums2` 均严格递增（strictly increasing）所需的最少操作次数。题目保证给定的输入一定可以实现。

如果一个数组（array）`arr` 满足 `arr[0] < arr[1] < arr[2] < ... < arr[arr.length - 1]`，则称其为严格递增。

**示例 1**  
```text
输入: nums1 = [1,3,5,4], nums2 = [1,2,3,7]
输出: 1
解释:
交换 nums1[3] 和 nums2[3]。此时序列为:
nums1 = [1, 3, 5, 7] 和 nums2 = [1, 2, 3, 4]
两者均严格递增。
```

**示例 2**  
```text
输入: nums1 = [0,3,5,8,9], nums2 = [2,1,4,6,9]
输出: 1
```

**约束条件**
- `2 <= nums1.length <= 10^5`
- `nums2.length == nums1.length`
- `0 <= nums1[i], nums2[i] <= 2 * 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个位置 `i` 的「是否交换」当成一个二进制位**，遍历所有可能的 0/1 组合，找到满足「两个序列严格递增」且交换次数最少的那一种。

- **数据结构**：只需要一个 `for` 循环和若干整数变量。可以把「是否交换」想象成一本字典的 **页码**：第 `i` 页写的是 0（不换）还是 1（换），我们要把所有页码排成合法的顺序。
- **正确性**：因为我们枚举了 **所有** 可能的交换方式，只要其中有一种方式能让两条序列严格递增，就一定会被检查到，最小的交换次数自然会被记录下来。

> 这就是典型的「暴力穷举」思路，保证正确，却往往慢到不忍直视。

#### 代码（Python）

```python
from itertools import product
from typing import List

def minSwap_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    ans = float('inf')                     # 记录最小交换次数

    # 所有 0/1 长度为 n 的组合，0 表示不换，1 表示换
    for mask in product([0, 1], repeat=n):
        a, b = nums1[:], nums2[:]          # 复制两条序列
        swaps = 0

        # 按照当前的 mask 进行交换
        for i, flag in enumerate(mask):
            if flag:                        # 需要交换
                a[i], b[i] = b[i], a[i]
                swaps += 1

        # 检查两条序列是否严格递增
        ok = all(a[i] < a[i + 1] for i in range(n - 1)) and \
             all(b[i] < b[i + 1] for i in range(n - 1))

        if ok:
            ans = min(ans, swaps)          # 取最小值

    return ans
```

> 关键行解释  
> - `product([0, 1], repeat=n)`：产生所有长度为 `n` 的 0/1 序列，相当于「遍历所有可能的交换方案」。  
> - `a[i], b[i] = b[i], a[i]`：如果当前位为 1，就把两条数组对应位置的元素互换。  
> - `all(a[i] < a[i + 1] ...)`：判断序列是否严格递增。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 来自所有可能的交换组合（每个位置有 2 种选择），每一种组合我们都要遍历一次数组检查递增性，耗时 `O(n)`。  
  - 用大白话说，就是「如果数组有 20 个元素，可能的方案多到 1,048,576 种，几乎不可能在一秒内算完」。
- **空间复杂度**：`O(n)`  
  - 需要复制两遍原数组 `a, b`，以及递归产生的 `mask`（在 Python 中 `product` 会逐个生成），所以最多占用与输入等长的额外空间。

> 暴力解虽然能「保证」找到答案，但在 LeetCode 给出的 `n ≤ 10^5` 时根本不可行，只能作为思考的起点。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：**每个位置的决策只与前一个位置的状态有关**。换句话说，决定第 `i` 位是否要换，只需要知道第 `i‑1` 位是「换」还是「不换」时的最小交换次数。于是可以用**动态规划（DP）**把指数级的搜索压缩到线性时间。

我们维护两个变量：

| 状态 | 含义 |
|------|------|
| `keep[i]` | 前 i+1 个元素（下标 0…i）已经严格递增，且第 i 位**不换**的最少交换次数 |
| `swap[i]` | 前 i+1 个元素已经严格递增，且第 i 位**换**的最少交换次数 |

初始时（i = 0）：

- `keep[0] = 0`（第 0 位不换，当然不需要操作）  
- `swap[0] = 1`（第 0 位换，需要一次交换）

对于后面的每个位置 `i (1 ≤ i < n)`，我们考虑两种可能的前驱状态：

1. **不换 i** (`keep[i]`)  
   - 若 `nums1[i] > nums1[i-1]` **且** `nums2[i] > nums2[i-1]`，说明即使第 `i-1` 位不换，第 `i` 位也可以保持不换。此时 `keep[i] = keep[i-1]`。  
   - 若 `nums1[i] > nums2[i-1]` **且** `nums2[i] > nums1[i-1]`，说明第 `i-1` 位如果**换了**，第 `i` 位仍然可以**不换**。此时 `keep[i] = min(keep[i], swap[i-1])`。

2. **换 i** (`swap[i]`)  
   - 若 `nums1[i] > nums2[i-1]` **且** `nums2[i] > nums1[i-1]`，说明前一个位置不换时，第 i 位可以换。此时 `swap[i] = keep[i-1] + 1`（因为第 i 位多一次交换）。  
   - 若 `nums1[i] > nums1[i-1]` **且** `nums2[i] > nums2[i-1]`，说明前一个位置已经换了，第 i 位仍然可以换。此时 `swap[i] = min(swap[i], swap[i-1] + 1)`。

每一步只需要前一次的 `keep`、`swap`，所以可以把数组压缩成 **两个变量**，实现 `O(1)` 的空间。

> **类比**：想象两条相邻的楼梯，每一步我们可以「不换」保持原来的踏板，也可以「换」把两条楼梯的踏板互换。只要前一步的踏板高度满足递增条件，后一步就可以决定是否换。我们记录「不换」和「换」两种情况下的最少换梯次数，逐步向前走。

#### 代码（Python）

```python
from typing import List

def minSwap(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    # keep 表示当前位不换的最小次数，swap 表示当前位换的最小次数
    keep = 0          # i = 0 时不换，次数为 0
    swap = 1          # i = 0 时换，次数为 1

    for i in range(1, n):
        # 先把本轮的两个状态设成一个很大的数，后面取最小值
        new_keep = new_swap = float('inf')

        # 情形 1：前后都不换，仍保持递增
        if nums1[i] > nums1[i - 1] and nums2[i] > nums2[i - 1]:
            new_keep = min(new_keep, keep)          # 不换 i，前面也不换
            new_swap = min(new_swap, swap + 1)      # 换 i，前面也换（再多一次交换）

        # 情形 2：前后交叉换位，仍保持递增
        if nums1[i] > nums2[i - 1] and nums2[i] > nums1[i - 1]:
            new_keep = min(new_keep, swap)          # 不换 i，前面换了
            new_swap = min(new_swap, keep + 1)      # 换 i，前面不换（多一次交换）

        # 更新为本轮的结果，准备进入下一位
        keep, swap = new_keep, new_swap

    # 最终答案是两种状态的最小值
    return min(keep, swap)
```

> 关键行解释  
> - `keep, swap = 0, 1`：第 0 位的两种初始状态。  
> - `new_keep = new_swap = float('inf')`：先设为「无限大」，后面取「最小」保证只保留合法转移。  
> - 两个 `if` 条件分别对应「同向递增」和「交叉递增」两种可能。  
> - `new_swap = min(new_swap, swap + 1)`：如果前一步已经换了，而当前也换，需要在已有交换次数上再加 1。  
> - 最后返回 `min(keep, swap)`：最后一位可以是换也可以是不换，取最少的即可。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每一步做常数次比较和赋值。对比暴力解的 `2^n`，这相当于把「指数级」的搜索压缩成「线性级」——在 `n = 10^5` 时依旧能在毫秒级完成。  
- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量 (`keep, swap, new_keep, new_swap`) 与输入数组无关，常数级额外空间。

> 与暴力解相比，时间从「天文数字」降到「线性」，空间也从 `O(n)` 降到 `O(1)`，是典型的 DP 优化案例。

---

## 心得

- **核心技巧**：**状态压缩的动态规划**（每个位置只保留「换」和「不换」两种最优子结构）。  
- **适用的题型**  
  1. 「两个序列或两条路径的同步约束」——如 *"Minimum Swaps To Make Sequences Increasing"*。  
  2. 「只能在相邻位置做决定」的 DP——如 *"House Robber"*（偷盗）或 *"Jump Game"*（跳跃）。  
  3. 「每一步有两种状态」的优化——如 *"Two City Scheduling"*（两城调度）中的「分配/不分配」状态。  
- **一句话总结解题钥匙**：**只要能用「上一步的状态」唯一决定「当前步的最优」就可以用 DP 把指数爆炸压到线性**。

---

## 反思

- **拿到题目第一反应**：先想「遍历所有换不换的组合」——暴力枚举，确保思路正确。  
- **最容易踩的坑**  
  1. **忘记交叉递增的情况**：只检查 `nums1[i] > nums1[i-1]` 和 `nums2[i] > nums2[i-1]` 会漏掉「前一位换了、当前位不换」的合法方案。  
  2. **边界条件**：`i = 0` 的初始化必须是 `keep = 0, swap = 1`，否则后续转移会出错。  
  3. **整数溢出/负数**：本题数值范围不大，但在写 `float('inf')` 时要确保后续比较正确。  
- **下次遇到同类题，第一步该想到**：**「每个位置只有两种可能的状态（换 / 不换），尝试用 DP 把状态压缩」**。先画出状态转移图，再写出递推公式，最后再考虑空间优化。