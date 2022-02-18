# #1673. 最具竞争力的子序列 / Find the Most Competitive Subsequence

> 难度：中等 · 标签：Array、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/find-the-most-competitive-subsequence/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and a positive integer k, return the most competitive subsequence of nums of size k.
An array's subsequence is a resulting sequence obtained by erasing some (possibly zero) elements from the array.
We define that a subsequence a is more competitive than a subsequence b (of the same length) if in the first position where a and b differ, subsequence a has a number less than the corresponding number in b. For example, [1,3,4] is more competitive than [1,3,5] because the first position they differ is at the final number, and 4 is less than 5.

**Examples**

**Example 1:**

```
Input: nums = [3,5,2,6], k = 2
Output: [2,6]
Explanation: Among the set of every possible subsequence: {[3,5], [3,2], [3,6], [5,2], [5,6], [2,6]}, [2,6] is the most competitive.
```

**Example 2:**

```
Input: nums = [2,4,3,3,5,4,9,6], k = 4
Output: [2,3,3,4]
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109
- 1 <= k <= nums.length

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个正整数 `k`，返回 `nums` 中长度为 `k` 的**最具竞争力的子序列**（subsequence）。  
数组的子序列是通过删除（可能为零个）元素后得到的序列。  
我们定义：若在两个等长子序列 `a` 与 `b` 的首个不同位置上，`a` 的对应元素小于 `b` 的对应元素，则子序列 `a` **更具竞争力**（more competitive）于子序列 `b`。例如 `[1,3,4]` 比 `[1,3,5]` 更具竞争力，因为它们在最后一个位置不同，且 `4 < 5`。

**示例 1**  
输入: `nums = [3,5,2,6]`, `k = 2`  
输出: `[2,6]`  
说明: 在所有可能的子序列集合 `{[3,5], [3,2], [3,6], [5,2], [5,6], [2,6]}` 中，`[2,6]` 是最具竞争力的。

**示例 2**  
输入: `nums = [2,4,3,3,5,4,9,6]`, `k = 4`  
输出: `[2,3,3,4]`

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `0 <= nums[i] <= 10^9`  
- `1 <= k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的长度为 `k` 的子序列枚举出来**，然后在这些子序列里挑选字典序（lexicographical order）最小的那个。  
- **子序列**：相当于在原数组里挑选 `k` 个位置，保持原来的相对顺序不变，就像从一本书里挑出几页，页码顺序必须保持原来的顺序。  
- **枚举方式**：可以用组合（Combination）的思想，从 `n` 个下标中选出 `k` 个下标（`C(n,k)` 种），对应的元素顺序就是一个子序列。  
- **比较大小**：两个等长的序列，从左到右逐个比较，第一次出现不同的地方，数值更小的序列更“竞争”。这正好就是字典序的比较方式。

因为我们把**所有**合法子序列都遍历了一遍，必然能找到最小的那一个，所以方法是正确的。

**复杂度分析（大白话）**  
- 枚举组合的数量是 “从 `n` 个人里挑 `k` 个人” 的组合数，记作 `C(n,k)`，它会随 `n` 的增大而非常快地爆炸（比如 `n=30, k=15` 时已经有 155M 种）。  
- 对每一种组合，我们还要把对应的 `k` 个元素取出来并与当前最小序列比较，花费 `O(k)` 的时间。  
- 所以总时间是 `O(C(n,k) * k)`，在最坏情况下几乎等同于 **指数级**，在 `n ≤ 10^5` 时根本跑不完。  
- 空间方面，只需要保存当前遍历到的一个子序列和最小序列，最多 `O(k)`。

#### 代码（Python）

```python
import itertools
from typing import List

def mostCompetitive_bruteforce(nums: List[int], k: int) -> List[int]:
    """
    暴力枚举所有长度为 k 的子序列，返回字典序最小的那个。
    只在小规模数据上能跑通，示例演示用。
    """
    best = None                     # 用来保存目前找到的最小序列
    # itertools.combinations 会产生所有下标的组合
    for idx_tuple in itertools.combinations(range(len(nums)), k):
        # 根据下标取出对应的元素，保持原顺序
        cur = [nums[i] for i in idx_tuple]
        # 第一次直接赋值，之后做字典序比较
        if best is None or cur < best:
            best = cur
    return best
```

#### 复杂度

- **时间复杂度**：`O(C(n, k) * k)` —— 组合数乘以每次取元素的代价，几乎是指数级的。  
- **空间复杂度**：`O(k)` —— 只保存当前子序列和最小子序列，最多 `k` 长度。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能**。我们需要一种**一次遍历就能直接构造答案** 的方法。  
观察题目：

1. 我们希望得到字典序最小的长度为 `k` 的子序列。  
2. “字典序最小”意味着**左边的元素越小越好**，因为左边的元素在比较时拥有最高优先级。  
3. 但是我们不能随意把小元素都搬到最前面，必须保证**还能凑够 `k` 个元素**。也就是说，当我们决定把某个大元素丢掉时，后面剩下的元素数量必须足够填满 `k`。

这正好可以用**单调栈（Monotonic Stack）**来实现：  
- 栈中保存已经挑选好的元素，栈底到栈顶的顺序就是当前构造的子序列的顺序。  
- 当遍历到新元素 `x` 时，如果栈顶元素 `> x`，说明把栈顶的“大”元素换成更小的 `x` 能让字典序更小。于是**弹出栈顶**。  
- 但弹出有个前提：弹完后**剩余未遍历的元素 + 栈中已有元素** 必须还能凑够 `k`（否则就会缺元素）。用公式表示就是：`len(stack) - 1 + (n - i) >= k`，其中 `i` 为当前遍历到的下标，`n` 为数组长度。  
- 当不满足弹出条件或栈顶已经不比 `x` 大时，就把 `x` **压入栈**。  
- 最后，栈的前 `k` 个元素就是答案（因为可能会多压入一些元素）。

**为什么一定对？**  
- **贪心**：每一步我们都尽可能把左边的“大”元素换成更小的，且不影响后面能否完成长度 `k`。如果有更小的序列存在，它必然在某一步可以用同样的替换策略得到，否者就违背了“左边优先”这一比较规则。  
- **单调性**：栈始终保持**递增**（从栈底到栈顶），这保证了已经确定的前缀已经是当前能做到的最小前缀。  

> 类比：想象你在排队买票，手里有一张卡片可以把排在你前面的“更贵”的人换到后面，只要后面还有足够的人可以补齐队伍长度。你总是把更贵的人让出去，让队伍的“费用”尽可能低。

#### 代码（Python）

```python
from typing import List

def mostCompetitive(nums: List[int], k: int) -> List[int]:
    """
    单调栈 + 贪心
    时间 O(n) 只遍历一次
    空间 O(k) 只保留最多 k+1 个元素在栈里
    """
    n = len(nums)
    stack = []                      # 用列表当栈，stack[0] 为栈底

    for i, x in enumerate(nums):
        # 只要栈顶比当前元素大，且弹掉后仍有足够的元素填满 k，就弹出栈顶
        while stack and stack[-1] > x and len(stack) - 1 + (n - i) >= k:
            stack.pop()            # 弹掉一个更大的元素
        # 如果栈的长度还没达到 k，就把当前元素压进去
        if len(stack) < k:
            stack.append(x)        # 记录当前元素，可能成为答案的一部分

    return stack                     # stack 长度恰好是 k
```

> 关键行解释  
> - `while stack and stack[-1] > x and len(stack) - 1 + (n - i) >= k:`  
>   *`stack[-1] > x`* 判断“栈顶更大”，可以改成更小的 `x`；  
>   *`len(stack) - 1 + (n - i) >= k`* 确保弹掉后**剩余的元素**（栈中除去即将弹出的那个，加上后面未遍历的）仍然够 `k`。  
> - `if len(stack) < k:` 只在还能容纳的情况下压入新元素，防止栈变得太长。

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个元素最多进栈一次、出栈一次，整体线性。相比暴力的指数级，快得多。  
- **空间复杂度**：`O(k)` —— 栈里最多保留 `k`（或 `k+1`）个元素，和输入规模无关。

---

## 心得

- **核心技巧**：**单调栈 + 贪心**，用于在保持相对顺序的前提下构造字典序最小（或最大）的子序列。  
- **适用的题型**  
  1. *LeetCode 402. Remove K Digits* – 删除 `k` 位数字后得到最小数。  
  2. *LeetCode 1081. Smallest Subsequence of Distinct Characters* – 在保持字符出现顺序的前提下找最小字典序子序列。  
  3. *LeetCode 316. Remove Duplicate Letters* – 与上题相似，只是要求每个字符恰好出现一次。  

> **解题钥匙**：**“左边更小更重要，弹出大元素只要后面还有足够的补位”**。

---

## 反思

- **第一反应**：直接想到“枚举所有组合”，因为字典序比较看起来像普通的排序。  
- **最容易踩的坑**  
  - **剩余元素不足**：在弹出栈顶时忘记检查后面还有多少未遍历的元素，容易导致最终栈里元素不足 `k`。  
  - **压入过多元素**：如果不限制 `len(stack) < k`，栈会超过 `k`，返回时需要再截断，容易出错。  
  - **边界情况**：`k` 等于数组长度时，答案就是原数组；`k` 为 1 时，只需要最小的单个元素。  

- **下次遇到同类题**：第一步先问自己——“如果我想让左边尽可能小，我可以把比当前元素大的已经选好的元素丢掉吗？丢掉后还能凑够所需长度吗？” 基于这个判断，就能快速构造单调栈的贪心框架。