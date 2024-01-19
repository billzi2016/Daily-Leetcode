# #2554. 从区间中选择的最大整数个数 I / Maximum Number of Integers to Choose From a Range I

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-integers-to-choose-from-a-range-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array banned and two integers n and maxSum. You are choosing some number of integers following the below rules:
Return the maximum number of integers you can choose following the mentioned rules.

**Examples**

**Example 1:**

```
Input: banned = [1,6,5], n = 5, maxSum = 6
Output: 2
Explanation: You can choose the integers 2 and 4.
2 and 4 are from the range [1, 5], both did not appear in banned, and their sum is 6, which did not exceed maxSum.
```

**Example 2:**

```
Input: banned = [1,2,3,4,5,6,7], n = 8, maxSum = 1
Output: 0
Explanation: You cannot choose any integer while following the mentioned conditions.
```

**Example 3:**

```
Input: banned = [11], n = 7, maxSum = 50
Output: 7
Explanation: You can choose the integers 1, 2, 3, 4, 5, 6, and 7.
They are from the range [1, 7], all did not appear in banned, and their sum is 28, which did not exceed maxSum.
```

**Constraints**

- 1 <= banned.length <= 104
- 1 <= banned[i], n <= 104
- 1 <= maxSum <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `banned`，以及两个整数 `n` 和 `maxSum`。你需要从区间 `[1, n]` 中挑选若干整数，满足以下条件：

1. 选中的整数 **不能** 出现在 `banned` 中。  
2. 选中的整数的总和 **不超过** `maxSum`。  

返回在满足上述条件的前提下，最多可以挑选的整数个数。

**示例 1**  
```
Input: banned = [1,6,5], n = 5, maxSum = 6
Output: 2
Explanation: 你可以选择整数 2 和 4。它们都在区间 [1, 5] 内，且不在 banned 中，和为 6，未超过 maxSum。
```

**示例 2**  
```
Input: banned = [1,2,3,4,5,6,7], n = 8, maxSum = 1
Output: 0
Explanation: 在满足条件的情况下，你无法选择任何整数。
```

**示例 3**  
```
Input: banned = [11], n = 7, maxSum = 50
Output: 7
Explanation: 你可以选择整数 1, 2, 3, 4, 5, 6, 7。它们全部在区间 [1, 7] 内，且不在 banned 中，和为 28，未超过 maxSum。
```

**约束条件**  

- `1 <= banned.length <= 10^4`  
- `1 <= banned[i], n <= 10^4`  
- `1 <= maxSum <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有满足条件的整数都列出来**，然后把它们的子集一个一个枚举，看看哪个子集的元素之和 ≤ `maxSum`，且元素个数最多。  

- **把合法整数列出来**  
  - 先把 `banned` 中 ≤ `n` 的数字放进一个集合（哈希表），哈希表就像一本“查字典”，把词（数字）当成 `key`，对应的页码（是否被禁）当成 `value`，查找是 O(1) 的速度。  
  - 再遍历 `1 … n`，只要不在禁用集合里，就把这个数字放进 `candidates` 列表。  

- **枚举子集**  
  - 对 `candidates` 中的每个数字，都有两种选择：**取** 或 **不取**。于是所有可能的取法就是二叉树的每一条路径，路径数是 `2^{len(candidates)}`，即指数级。  
  - 对每个子集，计算它们的和，如果和 ≤ `maxSum`，就更新答案为子集大小的最大值。  

> **为什么这个方法一定能得到正确答案？**  
> 因为它穷举了所有可能的取法，哪怕是最不直观的组合也会被检查到，所以答案一定在其中。  

> **时间/空间复杂度**  
> - 时间复杂度：`O(2^m * m)`，其中 `m = len(candidates)`，因为要遍历 `2^m` 个子集，每个子集要算一次和（最坏需要遍历 `m` 个数）。这在 `m` 较大时几乎不可用。  
> - 空间复杂度：`O(m)` 用来存放 `candidates`，以及递归/栈的深度 `O(m)`。  

#### 代码（Python）

```python
from typing import List

def maxCount_brute(banned: List[int], n: int, maxSum: int) -> int:
    # 1. 把禁用的数字放进哈希表（集合），查找 O(1)
    banned_set = set(x for x in banned if x <= n)

    # 2. 生成所有合法的候选数字
    candidates = [i for i in range(1, n + 1) if i not in banned_set]

    best = 0                     # 当前找到的最大数量

    # 3. 深度优先搜索枚举子集
    def dfs(idx: int, cur_sum: int, cur_cnt: int):
        nonlocal best
        # 如果已经超过上限，直接剪枝
        if cur_sum > maxSum:
            return
        # 更新答案
        best = max(best, cur_cnt)

        # 从 idx 开始尝试把后面的数字加入子集
        for i in range(idx, len(candidates)):
            dfs(i + 1, cur_sum + candidates[i], cur_cnt + 1)

    dfs(0, 0, 0)
    return best
```

> **关键行中文注释**  
> - `banned_set = set(...)`：把禁用数字放进集合，类似查字典，能在常数时间判断一个数是否被禁。  
> - `candidates = [...]`：把所有可以选择的数字收集起来。  
> - `dfs`：递归枚举每一种取或不取的可能。  

#### 复杂度  

- **时间复杂度**：`O(2^m * m)`，`m` 是合法数字的个数。`2^m` 表示所有子集的数量，`m` 是每次计算子集和时最坏需要遍历的元素数。对大输入几乎不可接受。  
- **空间复杂度**：`O(m)`，主要是保存 `candidates` 列表和递归栈的深度。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举所有子集是最耗时的地方**。  
事实上，这道题的目标是“在和不超过 `maxSum` 的前提下，选出尽可能多的整数”。所有整数都是 **正数**，所以 **先选小的、后选大的** 能让我们在相同的和限制下容纳更多的数。  

**核心优化思路**：  
1. **只关心是否被禁**，不需要真正枚举子集。把 `banned` 中 ≤ `n` 的数字放进集合，随后**从 1 开始顺序遍历**。  
2. **贪心**：遍历到的每个合法数字 `x`，只要 `cur_sum + x ≤ maxSum` 就立刻选它，因为它是当前剩余范围里最小的数，选了它一定不会妨碍以后选更大的数（更大的数只会让和更快超过上限）。  
3. 一旦 `cur_sum + x` 超过 `maxSum`，后面的所有更大的数也必然超过（因为它们更大），此时直接结束循环。  

这样只需要一次线性扫描，时间复杂度是 `O(n)`，空间只用来存放禁用集合 `O(banned.length)`。  

**类比**：想象你在超市买零食，预算是 `maxSum`，每件零食都有价格（正整数），而且你只能买每种零食 **一次**，还有一些零食是“禁买”的（`banned`）。如果你想买的零食种类最多，最聪明的办法就是先挑最便宜的（从 1 元开始），一直买到预算用完为止。  

#### 代码（Python）

```python
from typing import List

def maxCount(banned: List[int], n: int, maxSum: int) -> int:
    # 1. 把禁用的数字（且 <= n）放进集合，查询 O(1)
    banned_set = set(num for num in banned if num <= n)

    cur_sum = 0          # 已经选的数字之和
    cnt = 0              # 已经选的数字个数

    # 2. 从 1 到 n 按顺序尝试选取
    for x in range(1, n + 1):
        # 跳过禁用的数字
        if x in banned_set:
            continue
        # 若加入 x 后总和仍然 ≤ maxSum，说明可以选
        if cur_sum + x <= maxSum:
            cur_sum += x
            cnt += 1
        else:
            # 已经超过预算，后面的更大数字也不可能再选
            break

    return cnt
```

> **关键行中文注释**  
> - `banned_set = set(...)`：把需要排除的数字放进哈希表，类似字典查词，快速判断。  
> - `if x in banned_set: continue`：如果当前数字被禁，用 `continue` 跳过。  
> - `if cur_sum + x <= maxSum:`：贪心判断，若加上它仍在预算内，就选它。  
> - `else: break`：一旦超预算，后面的更大数字必然也会超，直接结束循环。  

#### 复杂度  

- **时间复杂度**：`O(n)`。我们只遍历一次 `1 … n`，每一步的判断都是常数时间（集合查找 O(1)）。这比暴力的指数时间快了很多。  
- **空间复杂度**：`O(b)`，其中 `b` 是 `banned` 中 ≤ `n` 的元素个数。只需要存放一个哈希集合，其余变量都是常数级别。  

---

## 心得  

- **核心技巧**：**贪心 + 哈希集合**。先把禁用的数字过滤掉，然后从最小的合法数字开始逐个尝试，只要不超预算就立刻选。  
- **适用的题型**  
  1. “在和不超过某个值的前提下，尽可能多选元素”——如 **Maximum Number of Integers to Choose From a Range II**（进阶版）。  
  2. “选取尽可能多的任务/活动，使总耗时 ≤ 给定上限”——如 **Maximum Number of Events That Can Be Attended**（活动安排类）。  
  3. “在预算内购买尽可能多的商品”——如 **Buy Two Chocolates**（预算购买类）。  

- **一句话总结解题钥匙**：**先挑最小的、合法的数，遇到预算上限立即停止**。  

---

## 反思  

- **拿到题目第一反应**：想到“枚举所有子集检查”——这是一种最直观、最安全的思路，但很快会发现会超时。  
- **最容易踩的坑**  
  1. **忘记只把 ≤ `n` 的 banned 数字放进集合**——若 `banned` 中有大于 `n` 的数，直接加入集合会导致不必要的查找（虽然不影响正确性，但浪费时间）。  
  2. **没有提前退出循环**——如果一直遍历到 `n` 即使已经超预算，会多做很多无用比较。  
  3. **整数溢出**（在某些语言中）——`cur_sum + x` 可能超过 32 位整数范围，Python 自动大数，但在其他语言需要注意。  
- **下次遇到同类题，第一步该想到**：**“所有数都是正的，先排序（或天然递增），贪心地从最小的开始选，直到预算/上限被触发”。**这样往往能直接得到最优解。