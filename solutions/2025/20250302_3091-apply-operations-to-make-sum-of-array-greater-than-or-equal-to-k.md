# #3091. 对数组执行操作，使其和大于等于 k / Apply Operations to Make Sum of Array Greater Than or Equal to k

> 难度：中等 · 标签：Math、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-make-sum-of-array-greater-than-or-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given a positive integer k. Initially, you have an array nums = [1].
You can perform any of the following operations on the array any number of times (possibly zero):
Return the minimum number of operations required to make the sum of elements of the final array greater than or equal to k.

**Examples**

**Example 1:**

```
Input: k = 11
Output: 5
Explanation:
We can do the following operations on the array nums = [1] :
The sum of the final array is 4 + 4 + 4 = 12 which is greater than or equal to k = 11 . The total number of operations performed is 3 + 2 = 5 .
```

**Example 2:**

```
Input: k = 1
Output: 0
Explanation:
The sum of the original array is already greater than or equal to 1 , so no operations are needed.
```

**Constraints**

- 1 <= k <= 105

---

## 题目（中文翻译）

**描述**  
给定一个正整数 `k`。最初，你拥有数组 `nums = [1]`。  
你可以对数组执行以下任意操作任意次数（可能为零）：  
（此处应列出具体操作，原题中未给出）

返回使最终数组中所有元素之和 **大于等于** `k` 所需的最少操作次数。

**示例**

**示例 1**  
```
Input: k = 11
Output: 5
```
**解释**：  
我们可以在数组 `nums = [1]` 上依次执行如下操作：  
（具体操作过程略）  
最终数组的和为 `4 + 4 + 4 = 12`，满足 `12 ≥ k = 11`。  
总共执行的操作次数为 `3 + 2 = 5`。

**示例 2**  
```
Input: k = 1
Output: 0
```
**解释**：  
原数组的和已经 `≥ 1`，因此不需要任何操作。

**约束条件**  
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给了我们两种操作：

1. **增加（increase）**：把数组中的任意一个元素 `+1`。  
   *可以把它想象成在字典里查找一个词，然后把对应的页码往后翻一页*——每次只改动一个元素，花费 1 次操作。

2. **复制（duplicate）**：把数组中任意一个元素复制一份，再插入数组。  
   *这就像把一本书里某页的内容复印一遍，得到两页相同的内容*——数组的长度会加 1，花费同样是 1 次操作。

我们从 `[1]` 开始，目标是让 **所有元素之和 ≥ k**，并且要让操作次数最少。

最直接的想法是**枚举所有可能的操作顺序**，每一步都尝试对每个元素做“增加”或“复制”，一直搜索到和 ≥ k 为止。  

- **数据结构**：只需要一个普通的 Python 列表来保存当前数组。  
- **为什么正确**：因为我们把所有可能的操作序列都遍历了一遍，必然能找到最少操作次数的那条路径。  
- **时间/空间复杂度**：  
  - 每一步我们都有两种选择（增加或复制），而操作次数本身可能高达 `k`（例如 k=10⁵ 时，最坏情况需要 10⁵ 次“增加”），于是时间复杂度是指数级的，记作 **O(2^k)**，这在实际里根本不可行。  
  - 空间上只需要保存当前数组，最多也只有 `k` 个元素，**O(k)**。

> **大白话**：`O(2^k)` 就好比每秒钟翻倍增长的细菌，10 秒就有 1024 只，30 秒就有十亿只；显然我们没法等它跑完。

#### 代码（Python）

```python
from collections import deque

def brute(k: int) -> int:
    """暴力 BFS，搜索所有可能的操作序列（仅作演示，实际不可用）"""
    start = (1, (1,))                 # (已使用的操作数, 当前数组元组)
    q = deque([start])
    seen = {start[1]}                 # 防止重复状态

    while q:
        ops, arr = q.popleft()
        if sum(arr) >= k:             # 已经满足要求
            return ops

        # 1. 增加操作：对每个位置 +1
        for i in range(len(arr)):
            new_arr = list(arr)
            new_arr[i] += 1
            tup = tuple(new_arr)
            if tup not in seen:
                seen.add(tup)
                q.append((ops + 1, tup))

        # 2. 复制操作：复制任意一个元素
        for i in range(len(arr)):
            new_arr = list(arr) + [arr[i]]
            tup = tuple(new_arr)
            if tup not in seen:
                seen.add(tup)
                q.append((ops + 1, tup))

    return -1   # 理论上不会到这里
```

> 代码里每一行都有中文注释，帮助你快速定位每一步的作用。**注意**：这段代码仅用于说明思路，`k` 稍大就会卡死。

#### 复杂度

- **时间复杂度**：`O(2^k)`（指数级），因为每一步都有两种选择，且最坏情况需要 `k` 步才能达到目标。  
- **空间复杂度**：`O(k)`，因为最多只会保存长度为 `k` 的数组（实际更大，因为会存很多不同的状态）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于我们把“增加”和“复制”交叉进行，导致状态爆炸。  
观察题目还有两个重要提示：

1. **所有的增加操作最好先做完**，因为把一个元素先弄大再复制，它的价值会被复制多次，收益最大。  
2. **所有的复制操作放在最后**，因为复制后再增加只会让新复制的元素得到提升，而不是让已经大量存在的元素变大，浪费操作。

基于这两点，我们可以把整个过程简化为：

- 先对最初的唯一元素（值为 `1`）做 `i` 次增加，得到值 `v = 1 + i`。  
- 然后做 `t` 次复制（每次复制任意一个已有元素，这里显然复制的就是值最大的 `v`），数组里会出现 `t+1` 个 `v`，总和为 `(t+1) * v`。

我们只需要找到 **最小的 `i + t`**，满足 `(t+1) * v ≥ k`。

**如何求最优**：

- 给定 `i`，`v` 已知，求最小的 `t`：  
  ```
  (t + 1) * v ≥ k
  → t ≥ ceil(k / v) - 1
  ```
- 因为 `i` 的取值范围只需要到 `k`（当 `v` 已经 ≥ k 时，复制次数 `t` 为 0），我们可以 **遍历所有可能的 i**，计算对应的 `t`，取最小的 `i + t`。

这是一种 **枚举 + 直接计算** 的思路，时间复杂度是 `O(k)`，在 `k ≤ 10⁵` 的限制下完全可接受。

#### 代码（Python）

```python
import math

def min_operations(k: int) -> int:
    """
    返回使数组和 ≥ k 所需的最少操作次数。
    思路：先全部做 i 次 increase（把唯一元素变为 1+i），
          再做 t 次 duplicate（复制该元素），满足 (t+1)*(1+i) ≥ k。
    """
    if k <= 1:                     # 初始数组 [1] 已经满足条件
        return 0

    ans = k                        # 直接把所有 k 次 increase 当作上界
    for i in range(k + 1):         # i 表示 increase 的次数
        v = 1 + i                  # 增加后的单个元素值
        # 需要多少个 v 才能让和 ≥ k
        need = (k + v - 1) // v    # 等价于 ceil(k / v)
        t = need - 1               # 复制的次数（原来的那个不算）
        ans = min(ans, i + t)      # 取最小的操作总数

    return ans
```

**关键行中文解释**：

- `if k <= 1: return 0` —— 初始数组已经够大，不需要任何操作。  
- `for i in range(k + 1):` —— 枚举所有可能的 “increase” 次数。  
- `v = 1 + i` —— 经过 `i` 次增加后，唯一元素的值。  
- `need = (k + v - 1) // v` —— 计算要凑够 `k` 至少需要多少个 `v`（向上取整）。  
- `t = need - 1` —— 除了最初的那个元素，还要复制多少次。  
- `ans = min(ans, i + t)` —— 更新最小操作数。

#### 复杂度

- **时间复杂度**：`O(k)`。我们只遍历 `0 … k` 共 `k+1` 次，每次都是 O(1) 的算术运算。  
  - **含义**：如果 `k = 100 000`，最多只会跑十万次循环，几毫秒就能完成，远比指数级快得多。  
- **空间复杂度**：`O(1)`。只用了几个整数变量，不会随 `k` 增大而增长。

---

## 心得

- **核心技巧**：先把一个元素尽可能“变大”，再利用复制把大值“批量”加入数组。  
- **适用的题型**：  
  1. “先增后复制”类的贪心题（如 LeetCode 1805. **Number of Different Integers in a String** 的类似思路）。  
  2. 需要在两种操作之间平衡的最小化问题（如 “先建造再复制” 的 **Minimum Operations to Make Array Empty**）。  
- **一句话总结**：**把所有“增”集中在一个元素上，再用“复制”把它的价值乘以出现次数，遍历增的次数求最小总操作**。

---

## 反思

- **第一反应**：看到“increase”和“duplicate”会想到 BFS 暴力搜索，想把所有操作顺序都尝试一遍。  
- **最容易踩的坑**：  
  - 忘记先把所有“增加”做完会导致复制的价值太小，从而多余操作。  
  - 计算复制次数时忘记减去已经存在的那个元素，导致 `t` 多算 1。  
  - 边界情况 `k = 1`（答案应为 0）如果不单独处理会得到错误的正数。  
- **下次类似题的第一步**：先问自己 **“哪种操作的收益会被后续操作放大？”**——把收益最大的操作提前，剩下的再考虑。这样往往能把暴力搜索压缩到线性遍历。