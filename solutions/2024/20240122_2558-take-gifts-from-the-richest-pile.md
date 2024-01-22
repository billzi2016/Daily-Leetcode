# #2558. 从最富有的堆中取礼物 / Take Gifts From the Richest Pile

> 难度：简单 · 标签：Array、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/take-gifts-from-the-richest-pile/)

---

## 题目（英文原版）

**Description**

You are given an integer array gifts denoting the number of gifts in various piles. Every second, you do the following:
Return the number of gifts remaining after k seconds.

**Examples**

**Example 1:**

```
Input: gifts = [25,64,9,4,100], k = 4
Output: 29
Explanation: 
The gifts are taken in the following way:
- In the first second, the last pile is chosen and 10 gifts are left behind.
- Then the second pile is chosen and 8 gifts are left behind.
- After that the first pile is chosen and 5 gifts are left behind.
- Finally, the last pile is chosen again and 3 gifts are left behind.
The final remaining gifts are [5,8,9,4,3], so the total number of gifts remaining is 29.
```

**Example 2:**

```
Input: gifts = [1,1,1,1], k = 4
Output: 4
Explanation: 
In this case, regardless which pile you choose, you have to leave behind 1 gift in each pile. 
That is, you can't take any pile with you. 
So, the total gifts remaining are 4.
```

**Constraints**

- 1 <= gifts.length <= 103
- 1 <= gifts[i] <= 109
- 1 <= k <= 103

---

## 题目（中文翻译）

给定一个整数数组 `gifts`，其中 `gifts[i]` 表示第 `i` 堆礼物的数量。每秒，你执行以下操作：

- 选择当前礼物数量**最多**的那一堆（如果有多堆数量相同，任选其一），
- 将该堆的礼物数量替换为 `⌊√gifts[i]⌋`（即该堆原始数量的平方根向下取整），
- 其余堆的礼物数量保持不变。

在进行完 `k` 秒后，返回所有堆中剩余礼物的总数。

## 示例

### 示例 1
**输入**  
``` 
gifts = [25,64,9,4,100], k = 4
```
**输出**  
```
29
```
**解释**  
礼物的取走过程如下：
- 第 1 秒，选择数量最多的堆（100），取走后剩下 `⌊√100⌋ = 10`。
- 第 2 秒，选择数量最多的堆（64），取走后剩下 `⌊√64⌋ = 8`。
- 第 3 秒，选择数量最多的堆（25），取走后剩下 `⌊√25⌋ = 5`。
- 第 4 秒，选择数量最多的堆（10），取走后剩下 `⌊√10⌋ = 3`。

此时各堆的礼物数量为 `[5,8,9,4,3]`，总和为 `5 + 8 + 9 + 4 + 3 = 29`。

### 示例 2
**输入**  
```
gifts = [1,1,1,1], k = 4
```
**输出**  
```
4
```
**解释**  
每堆礼物数量都是 1，`⌊√1⌋ = 1`，因此无论选择哪一堆，都不会减少礼物数量。最终所有堆的礼物总数仍为 4。

## 约束条件
- `1 <= gifts.length <= 10^3`
- `1 <= gifts[i] <= 10^9`
- `1 <= k <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每秒钟都要找出 **当前礼物堆中数量最多的那一堆**，把它的数量改成 `⌊√x⌋`（即取平方根后向下取整），其余堆保持不变，重复 `k` 次。  

- **使用的数据结构**：普通的 Python 列表 `gifts`。把它想象成一排装满礼物的箱子，我们每次都要在这排箱子里挑出最“重”的那一个。  
- **为什么正确**：题目要求每秒都必须选择**当前最大的**堆并执行同样的操作，暴力实现正是逐秒模拟这个过程，完全符合题意。  
- **复杂度分析**：  
  - 找最大堆需要遍历整个数组，时间是 `O(n)`（`n` 为礼物堆的数量）。  
  - 这一步会进行 `k` 次，所以总时间是 `O(n·k)`。如果把 `O(n·k)` 用大白话解释，就是“每秒要检查所有箱子一次，最多检查 `k` 秒”。  
  - 只用了原数组本身，没有额外的存储，空间复杂度是 `O(1)`（常数级），也就是“几乎不占额外空间”。  

#### 代码（Python）

```python
import math
from typing import List

def pick_gifts_bruteforce(gifts: List[int], k: int) -> int:
    """
    暴力模拟：每秒遍历一次数组找到最大值并替换为 sqrt 后的整数部分。
    """
    n = len(gifts)
    for _ in range(k):
        # 1️⃣ 找到当前最大的堆的下标
        max_idx = 0
        for i in range(1, n):
            if gifts[i] > gifts[max_idx]:
                max_idx = i

        # 2️⃣ 用 sqrt 结果（向下取整）覆盖原来的值
        gifts[max_idx] = int(math.isqrt(gifts[max_idx]))   # math.isqrt 直接返回整数平方根

    # 3️⃣ 所有秒数结束后，返回剩余礼物的总数
    return sum(gifts)
```

#### 复杂度

- **时间复杂度**：`O(n·k)`  
  - 解释：每秒遍历 `n` 个堆，重复 `k` 秒。若 `n=1000, k=1000`，最坏情况约为 `10⁶` 次比较，仍在可接受范围。  
- **空间复杂度**：`O(1)`  
  - 解释：只在原数组上原地修改，没有额外的数组或容器，使用的额外空间是常数级的。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每秒都要 **线性扫描** 整个数组找最大值。我们可以用一种“随时能拿到最大值”的数据结构来把这一步的时间从 `O(n)` 降到 `O(log n)`。

- **数据结构**：**最大堆（Priority Queue）**。  
  - 类比：想象我们有一个“礼物箱子的大仓库”，每次想要最重的箱子，只需要在仓库的最上层（堆顶）直接拿取，而不必把所有箱子都搬出来比较。  
  - 在 Python 中的 `heapq` 实现的是 **最小堆**，所以我们把数值取负数来“伪装”成最大堆。  

- **核心步骤**（每秒）  
  1. 从堆中弹出（`heappop`）当前最大的礼物数 `x`（实际弹出的是 `-x`）。  
  2. 计算 `⌊√x⌋`，记作 `y`。  
  3. 把 `-y` 再压回堆（`heappush`），这样堆仍然保持“最大在堆顶”。  

- **为什么这样更快**：  
  - 堆的 **插入** 与 **弹出** 都是 `O(log n)`，而不是 `O(n)`。  
  - 进行 `k` 次后，总时间是 `O((n + k)·log n)`（最初把所有元素建堆是 `O(n)`），这在 `n, k ≤ 1000` 的范围内几乎是瞬间完成。  

- **细节说明**：  
  - `math.isqrt` 是 Python 3.8+ 提供的整数平方根函数，直接返回 `⌊√x⌋`，避免了浮点数误差。  
  - 最后把堆里的负数取反再求和，即可得到剩余礼物的总数。  

#### 代码（Python）

```python
import heapq
import math
from typing import List

def pick_gifts_optimal(gifts: List[int], k: int) -> int:
    """
    使用最大堆（通过取负数实现）在每秒 O(log n) 时间内获取并更新最大的礼物堆。
    """
    # 1️⃣ 把所有礼物数量取负放入堆，构造最大堆
    max_heap = [-g for g in gifts]          # 负数越大（即原数越小），堆顶越小
    heapq.heapify(max_heap)                 # O(n) 建堆

    # 2️⃣ 进行 k 次操作
    for _ in range(k):
        # 弹出当前最大的礼物数（记得取负号恢复正数）
        largest = -heapq.heappop(max_heap)  # O(log n)

        # 计算取走后的剩余礼物数（整数平方根）
        remaining = math.isqrt(largest)     # ⌊√largest⌋

        # 把新的数量再放回堆中（仍然取负）
        heapq.heappush(max_heap, -remaining) # O(log n)

    # 3️⃣ 堆中剩余的都是负数，取反后求和即为答案
    return -sum(max_heap)
```

#### 复杂度

- **时间复杂度**：`O((n + k)·log n)`  
  - 解释：建堆 `O(n)`，每次弹出 + 插入各 `O(log n)`，共 `k` 次。与暴力的 `O(n·k)` 相比，**对数级的提升**让程序在更大规模下也依然快。  
- **空间复杂度**：`O(n)`  
  - 解释：需要额外的堆来存放 `n` 个负数，空间随礼物堆的数量线性增长。  

---

## 心得

- **核心技巧**：**使用堆（优先队列）快速获取并更新最大元素**。  
- **适用的题型**：  
  1. “每次取最大/最小元素并修改后继续取”——如 LeetCode 1977 *Number of Ways to Separate a String*（使用堆模拟）  
  2. “动态维护一组数的最大/最小」——如 LeetCode 1642 *Furthest Building You Can Reach*（使用最小堆）  
  3. “每次取出最大后进行某种变换」——如 LeetCode 2462 *Maximum Sum of Distinct Elements*（使用最大堆）  
- **一句话总结解题钥匙**：**“把最大堆当作‘随时可取的最大箱子’，每秒弹出、变换再放回”。**  

---

## 反思

- **第一反应**：看到“每秒取最大堆并对它做 sqrt 操作”，立刻想到要 **模拟** 过程；随后想到直接遍历数组找最大。  
- **最容易踩的坑**：  
  - 忘记对 **平方根取整**（使用 `int(math.sqrt(x))` 可能因浮点误差导致错误，推荐 `math.isqrt`）。  
  - 没有考虑 **k 大于数组长度** 的情况，仍然可以重复取同一个堆，代码必须循环 `k` 次而不是只取 `n` 次。  
  - 在使用堆时忘记取负号导致得到最小值而非最大值。  
- **下次遇到同类题**，第一步应该想到 **“是否需要频繁获取最大/最小元素？”**，如果答案是“是”，立刻选用 **堆**（或平衡二叉搜索树）来降低时间复杂度。