# #2749. 使整数变为零的最少操作次数 / Minimum Operations to Make the Integer Zero

> 难度：中等 · 标签：Bit Manipulation、Brainteaser、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-the-integer-zero/)

---

## 题目（英文原版）

**Description**

You are given two integers num1 and num2.
In one operation, you can choose integer i in the range [0, 60] and subtract 2i + num2 from num1.
Return the integer denoting the minimum number of operations needed to make num1 equal to 0.
If it is impossible to make num1 equal to 0, return -1.

**Examples**

**Example 1:**

```
Input: num1 = 3, num2 = -2
Output: 3
Explanation: We can make 3 equal to 0 with the following operations:
- We choose i = 2 and subtract 22 + (-2) from 3, 3 - (4 + (-2)) = 1.
- We choose i = 2 and subtract 22 + (-2) from 1, 1 - (4 + (-2)) = -1.
- We choose i = 0 and subtract 20 + (-2) from -1, (-1) - (1 + (-2)) = 0.
It can be proven, that 3 is the minimum number of operations that we need to perform.
```

**Example 2:**

```
Input: num1 = 5, num2 = 7
Output: -1
Explanation: It can be proven, that it is impossible to make 5 equal to 0 with the given operation.
```

**Constraints**

- 1 <= num1 <= 109
- -109 <= num2 <= 109

---

## 题目（中文翻译）

**描述**  
给定两个整数 `num1` 和 `num2`。  
在一次操作中，你可以选择整数 `i`（范围为 \[0, 60\]），并从 `num1` 中减去 `2^i + num2`。  
返回使 `num1` 等于 0 所需的最少操作次数。如果无法使 `num1` 等于 0，返回 `-1`。

**示例 1**  
```
Input: num1 = 3, num2 = -2
Output: 3
```
**解释**：我们可以通过以下操作将 3 变为 0：  
- 选择 `i = 2`，从 3 中减去 `2^2 + (-2)`，即 `3 - (4 + (-2)) = 1`。  
- 再次选择 `i = 2`，从 1 中减去 `2^2 + (-2)`，即 `1 - (4 + (-2)) = -1`。  
- 选择 `i = 0`，从 -1 中减去 `2^0 + (-2)`，即 `(-1) - (1 + (-2)) = 0`。  
可以证明，3 是完成此过程的最少操作次数。

**示例 2**  
```
Input: num1 = 5, num2 = 7
Output: -1
```
**解释**：可以证明，使用给定的操作无法将 5 变为 0。

**约束条件**  
- \(1 \leq \text{num1} \leq 10^9\)  
- \(-10^9 \leq \text{num2} \leq 10^9\)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把“每一次操作”都列举出来，然后尝试所有可能的 `i`（0~60）组合，看看能否把 `num1` 变成 0。  
具体做法：

1. 从 `num1` 开始，递归（或 BFS）尝试把它减去 `2^i + num2`（`i` 从 0 到 60 任意取）。  
2. 每走一步记录已经用了几次操作，若某一步恰好把 `num1` 变成 0，就得到一种可行解。  
3. 把所有可行解的操作次数取最小值。

**生活化类比**：把这道题想成“在一堆不同面额的硬币（每个面额是 `2^i + num2`）中，挑选若干硬币凑出正好 `num1` 的金额”。暴力做法就是把每一种挑硬币的顺序都尝试一次。

**为什么能得到正确答案**：只要遍历了**所有**可能的操作序列，就一定能找到最少次数的那一个（如果存在的话）。

**时间/空间复杂度**：  
- 每一步有 61 种选择（`i = 0 … 60`），如果我们把搜索深度设为 `k`（最少的操作次数），则总的搜索树节点数大约是 `61^k`。  
- 这相当于 **指数级**（指数随 `k` 指数增长），在最坏情况下会爆炸。  
- 空间上需要保存递归栈或 BFS 队列，深度为 `k`，即 **O(k)**。

> **大白话**：`O(61^k)` 就像是把一棵每层都有 61 条枝桠的树往下爬 `k` 层，树的叶子会非常非常多，根本跑不完。

#### 代码（Python）

```python
from collections import deque

def min_operations_bruteforce(num1: int, num2: int) -> int:
    """
    暴力 BFS，尝试所有 i∈[0,60] 的操作序列。
    只用于演示思路，实际会超时。
    """
    MAX_I = 60
    # BFS 队列保存 (当前值, 已使用的操作次数)
    q = deque()
    q.append((num1, 0))
    # 为了防止无限循环，用集合记住已经访问过的值
    visited = {num1}

    while q:
        cur, steps = q.popleft()
        if cur == 0:               # 找到答案
            return steps
        if steps >= 60:            # 根据题目提示，最少不可能超过 60 步
            continue
        for i in range(MAX_I + 1):
            nxt = cur - (1 << i) - num2   # cur - (2^i + num2)
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, steps + 1))
    return -1    # 遍历完都没找到
```

#### 复杂度  

- **时间复杂度**：`O(61^k)`（指数级），即使 `k` 只有 10，`61^10` 也超过 `10^18`，根本跑不完。  
- **空间复杂度**：`O(61^k)`（最坏情况下要把整棵搜索树都放进队列），同样不可接受。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有操作序列**太慢，关键是要 **把问题抽象成数学等式**，然后只在一个很小的范围内（最多 60 次）枚举 **操作次数** `k`，而不是每一次的 `i`。

---

#### 2.1 把操作写成等式

一次操作把 `num1` 减去 `2^i + num2`，如果我们做了 `k` 次操作，分别选了 `i₁, i₂, …, i_k`，则：

```
num1 - Σ (2^{i_t} + num2) = 0
⇔ Σ 2^{i_t} + k * num2 = num1
```

左边的第一项 `Σ 2^{i_t}` 就是 **k 个 2 的幂的和**（可以重复）。  
记

```
target = num1 - k * num2
```

于是问题化为：

> 能否用 **恰好 k 个**（可以相同）`2^i (i≥0)` 的和等于 `target`？

---

#### 2.2 何时能用 k 个 2 的幂表示一个整数？

*每个 2 的幂最小是 1（2⁰），最大是 2⁶⁰。*

- **最小可能的和**：把所有 k 个数都取最小的 1，得到 `k`。所以必须满足 `target ≥ k`。
- **最大可能的“拆分程度”**：把一个大的 2 的幂拆成两个更小的幂（例如 `8 = 4 + 4 = 2 + 2 + 2 + 2`），这样可以 **增大项数**，但**不会改变二进制中 1 的个数**的下界。  
  - 二进制里 `1` 的个数（记作 `popcount(target)`）是 **最少需要的项数**。  
  - 通过不断拆分，你可以把项数从 `popcount(target)` 增加到任意不超过 `target`（把所有 1 拆成 1+1+…）。

因此，**恰好 k 项的表示条件**为：

```
popcount(target) ≤ k ≤ target
```

（`popcount` = 二进制中 1 的个数）

---

#### 2.3 只需要枚举 k=1…60

提示已经说明：**如果能做到，最多只需要 60 步**。所以我们只在 `k = 1 … 60` 中寻找满足上面不等式的最小 `k`。

具体步骤：

1. 对 `k` 从 1 到 60 循环  
   - 计算 `target = num1 - k * num2`  
   - 若 `target ≤ 0`，直接跳过（因为每个 2 的幂都是正数）  
   - 计算 `bits = target.bit_count()`（Python 3.8+ 用 `bin(target).count('1')`）  
   - 检查 `bits ≤ k ≤ target`  
   - 第一次满足的 `k` 即为答案（因为我们是从小到大枚举的）  
2. 若循环结束都没有满足的 `k`，返回 `-1`。

**类比**：把 `target` 看成一堆糖果，`popcount(target)` 是糖果最少必须的包装盒数（每盒只能装 2ⁱ 粒），而 `target` 本身是糖果总数，`k` 就是我们准备的盒子数。只要盒子数不小于最少需要的盒子数，也不大于糖果总数（每盒最少装 1 粒），我们就能把糖果恰好装满。

---

#### 代码（Python）

```python
def minOperations(num1: int, num2: int) -> int:
    """
    最优解：只枚举操作次数 k（1~60），利用
    target = num1 - k * num2
    检查 popcount(target) ≤ k ≤ target
    """
    MAX_K = 60                     # 题目提示的上界
    for k in range(1, MAX_K + 1):
        target = num1 - k * num2   # 需要用 k 个 2 的幂凑出的数
        if target <= 0:            # 2 的幂都是正数，target 必须正
            continue
        bits = target.bit_count()  # 二进制中 1 的个数
        # 判断是否可以恰好用 k 个 2 的幂表示 target
        if bits <= k <= target:
            return k               # 第一个满足的 k 即为最小操作数
    return -1                      # 没有任何 k 能满足条件
```

**关键行中文注释**：

- `target = num1 - k * num2` # 目标和：把 k 次减去 `num2` 的贡献先算掉，剩下的要用 k 个 2 的幂凑
- `if target <= 0: continue` # 2 的幂都是正数，目标若 ≤0 不可能
- `bits = target.bit_count()` # 统计 target 二进制里有多少个 1，最少需要这么多幂
- `if bits <= k <= target:` # 同时满足“最少不小于 bits”和“最多不大于 target”即可

#### 复杂度  

- **时间复杂度**：`O(60)`，只循环 60 次，每次做 O(1) 的整数运算。  
  - 与暴力的 `O(61^k)` 相比，**从指数级降到了常数级**，几乎瞬间完成。  
- **空间复杂度**：`O(1)`，只用几个整数变量。

---

## 心得

- **核心技巧**：把“每一步减去 `2^i + num2`”转化为**等式** `Σ 2^{i_t} + k·num2 = num1`，再把问题归结为**“能否用恰好 k 个 2 的幂表示某个整数”**。  
- **相同技巧的题型**  
  1. *“把一个数拆成若干个 2 的幂”*（例如 LeetCode 1689: **Partitioning Into Minimum Number Of Subsets With Equal Sum** 的子问题）  
  2. *“给定一个数，最少多少次加/减 2 的幂可以得到目标”*（类似 1658: **Minimum Operations to Reduce X to Zero**）  
  3. *“把一个数写成若干个 1 的和，允许拆分”*（如 1405: **Longest Happy String** 中的计数拆分思路）  
- **一句话总结解题钥匙**：  
  **“把每次操作的固定部分先算掉，剩下的只需要检查能否用 k 个 2 的幂恰好拼出目标”。**

---

## 反思

- **第一反应**：直接去搜索所有可能的 `i`，想把题目当作普通的 BFS/DFS。  
- **最容易踩的坑**  
  - 忘记 `target` 必须是 **正数**（因为 2 的幂永远非负）  
  - 误以为 `k` 最大是 `num1`，其实提示已经说明最多 60 步（因为 `i` 只到 60）  
  - 没有考虑 **重复使用同一个 2 的幂**，导致把 `popcount` 误当成唯一解  
- **下次遇到同类题**：  
  1. 先把每一步的“固定增量”抽离出来，得到一个 **只和 2 的幂相关的等式**。  
  2. 再用 **二进制的 1 的个数**（popcount）和 **范围约束**（k ≤ target）快速判定可行性。  

这样就能把看似需要暴力枚举的题目，转化为 O(常数) 的数学判断。祝学习愉快！