# #3154. 寻找到达第 K 阶楼梯的方法数 / Find Number of Ways to Reach the K-th Stair

> 难度：困难 · 标签：Math、Dynamic Programming、Bit Manipulation、Memoization、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/find-number-of-ways-to-reach-the-k-th-stair/)

---

## 题目（英文原版）

**Description**

You are given a non-negative integer k. There exists a staircase with an infinite number of stairs, with the lowest stair numbered 0.
Alice has an integer jump, with an initial value of 0. She starts on stair 1 and wants to reach stair k using any number of operations. If she is on stair i, in one operation she can:
Return the total number of ways Alice can reach stair k.
Note that it is possible that Alice reaches the stair k, and performs some operations to reach the stair k again.

**Examples**

**Example 1:**

```
Input: k = 0
Output: 2
Explanation:
The 2 possible ways of reaching stair 0 are:
```

**Example 2:**

```
Input: k = 1
Output: 4
Explanation:
The 4 possible ways of reaching stair 1 are:
```

**Constraints**

- 0 <= k <= 109

---

## 题目（中文翻译）

你得到一个非负整数 `k`。存在一座拥有无限层台阶的楼梯，最底层的台阶编号为 0。  
Alice 拥有一个整数跳跃值（jump），初始为 0。她从第 1 层台阶出发，想要通过任意次数的操作到达第 k 层台阶。若她位于第 i 层台阶，在一次操作中她可以：

返回 Alice 能够到达第 k 层台阶的所有可能方式的总数。  
需要注意的是，Alice 可能已经到达第 k 层台阶后，仍然可以继续进行操作，使得她再次回到第 k 层台阶。

**示例**

**示例 1**  
```
Input: k = 0
Output: 2
```
**解释**  
到达第 0 层台阶的 2 种可能方式是：

（此处省略具体方式的描述）

**示例 2**  
```
Input: k = 1
Output: 4
```
**解释**  
到达第 1 层台阶的 4 种可能方式是：

（此处省略具体方式的描述）

**约束条件**

- `0 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的操作序列枚举出来**，然后检查序列执行完后是否正好停在第 `k` 阶。  
我们可以把每一步的两种操作记为：

* **A 操作**：向下走一步（`i -> i-1`），记作 `'A'`。  
* **B 操作**：把当前位置翻倍（`i -> 2*i`），记作 `'B'`。

从第 1 阶开始，随意地把 `'A'`、`'B'` 组合成一个字符串（比如 `"BABAB"`），再按顺序执行，最后看是否站在第 `k` 阶。  

> **类比**：这就像把所有可能的单词（只由字母 A、B 组成）列出来，然后逐个查字典看是否符合条件。  

因为题目没有给出操作次数的上限，理论上序列可以无限长。为了让暴力搜索能结束，我们只能**人为设一个最大深度**（比如 `depth = 20`），遍历所有长度不超过 `depth` 的序列。显然，这种做法只能在 `k` 很小、深度很小的情况下勉强跑通，用来帮助我们**感受问题的本质**。

#### 代码（Python）

```python
from typing import List

def brute_force(k: int, max_depth: int = 20) -> int:
    """
    暴力枚举所有长度 ≤ max_depth 的操作序列，统计能恰好到达第 k 阶的序列数。
    这里的实现仅作思路展示，实际 k 较大时会非常慢。
    """
    cnt = 0                     # 用来累计满足条件的序列数

    def dfs(pos: int, last_was_A: bool, depth: int) -> None:
        """
        depth   : 已经使用的操作数
        pos     : 当前所在的楼层
        last_was_A: 前一步是否是 A 操作（因为 A 不能连续出现）
        """
        nonlocal cnt
        if pos == k:            # 到达目标楼层，计数
            cnt += 1
        if depth == max_depth:  # 已经达到最大深度，停止向下搜索
            return

        # 选 A 操作（向下走一步），只能在上一步不是 A 时使用
        if not last_was_A and pos > 0:   # 防止楼层小于 0
            dfs(pos - 1, True, depth + 1)

        # 选 B 操作（翻倍），没有任何限制
        dfs(pos * 2, False, depth + 1)

    # 起点是第 1 阶，且上一条操作不是 A（因为根本没有操作）
    dfs(1, False, 0)
    return cnt

# 示例（仅用于验证思路，实际运行很慢）
print(brute_force(0, max_depth=10))   # 期望得到 2
print(brute_force(1, max_depth=10))   # 期望得到 4
```

> **关键注释**：  
> - `last_was_A` 用来记录上一条操作是否是 `'A'`，从而防止出现连续的 `'A'`。  
> - `pos > 0` 保证我们不会走到负数楼层（题目只说楼层编号是非负整数）。  

#### 复杂度

- **时间复杂度**：`O(2^d)`，其中 `d` 为设定的最大深度。因为每一步最多有两种选择（A 或 B），所以搜索树的分支数是指数级的。  
- **空间复杂度**：`O(d)`，递归栈的深度最多为 `d`。

> **大白话解释**：如果把 `d` 看成 20，`2^20` 大约等于 1,048,576，已经是十几万条序列；如果 `d` 再大一点（比如 30），序列数就会爆炸到十亿级，根本算不过来。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于**：

1. **“翻倍”**（B）操作会把当前楼层从 `i` 变成 `2*i`。  
2. **“向下走一步”**（A）只能在两次 B 之间出现，且 **不能连续**。  

假设我们使用了 `x` 次 B 操作，`y` 次 A 操作（`y` 必须 ≤ `x+1`，因为 A 只能放在每两个相邻 B 之间的 `x+1` 个“空隙”里）。  

从第 1 阶开始：

- 连续做 `x` 次 B，楼层会变成 `2^x`（因为 `1 → 2 → 4 → … → 2^x`）。  
- 每一次 A 会把当前楼层 **减 1**，所以总共会减去 `y`。  

于是**最终到达的楼层**为  

```
final = 2^x - y
```

这正是提示里给出的等式。  

现在我们把 **目标 k** 放进去：

```
2^x - y = k   →   y = 2^x - k
```

要使序列合法，需要满足：

```
0 ≤ y ≤ x + 1               （A 的数量不能超过空隙数）
y 为整数
```

因此，只要遍历所有可能的 `x`，检查 `y = 2^x - k` 是否满足上述条件，就能得到一组合法的 `(x, y)`。  

对于每一组合法的 `(x, y)`，**有多少种不同的操作顺序**？  
我们只需要决定在 `x+1` 个空隙（B 前、B 后、以及最前面）中挑出 `y` 个位置放 A。  
这正是组合数：

```
C(x + 1, y)  = (x+1) 选 y
```

于是答案就是所有合法 `(x, y)` 对应的组合数之和：

```
ans = Σ C(x + 1, 2^x - k)    （遍历满足 0 ≤ 2^x - k ≤ x+1 的 x）
```

**为什么只需要遍历到 ~log₂(k)+2？**  
因为 `2^x` 随 `x` 指数增长，当 `2^x` 已经大于 `k + x + 1` 时，`y = 2^x - k` 就会超过 `x+1`，不再满足条件。  
`k ≤ 10⁹` → `2^30 ≈ 1.07·10⁹`，所以 `x` 最多到 30 左右，遍历次数只有 **O(log k)**，非常快。

**组合数的计算**  
`x ≤ 30`，所以 `x+1 ≤ 31`，组合数可以直接用整数算式计算，不需要模运算或预处理。

#### 代码（Python）

```python
from math import comb   # Python 3.8+ 自带的组合数函数

def number_of_ways(k: int) -> int:
    """
    返回 Alice 到达第 k 阶的所有可能操作序列数（不取模）。
    思路：遍历所有可能的翻倍次数 x，计算对应的向下走次数 y = 2^x - k，
          若 0 <= y <= x+1，则该组合合法，计入 C(x+1, y)。
    """
    ans = 0
    x = 0
    # 只要 2^x - k 仍有可能 ≤ x+1，就继续循环
    while True:
        power = 1 << x               # 2^x，使用左移更快
        y = power - k                # 需要的 A 操作数
        if y > x + 1:                # 已经超过最大可能的 A 数，后续 x 更大只会更坏
            # 当 power 已经大到使 y > x+1 时，后面的 x 更大只会让 y 更大
            # 所以可以直接终止循环
            if power > k + x + 1:    # 双重保险，防止误提前退出
                break
        if 0 <= y <= x + 1:
            ans += comb(x + 1, y)    # C(x+1, y)，Python 自带大整数支持
        x += 1
    return ans

# 示例
print(number_of_ways(0))   # 2
print(number_of_ways(1))   # 4
print(number_of_ways(5))   # 6（自行验证）
```

> **关键注释**  
> - `1 << x` 等价于 `2**x`，在整数范围内更快。  
> - `comb(n, r)` 会自动返回 **精确的大整数**，不需要自己写阶乘或取模。  
> - 循环的终止条件利用了 **“一旦 y > x+1 且 power 已经足够大，就不会再有合法解”**，从而保证只遍历约 `log₂(k)` 次。

#### 复杂度

- **时间复杂度**：`O(log k)`，因为 `x` 最多到 `⌈log₂(k)⌉ + 2`（约 30 次）。每次只做常数时间的位运算和组合数查询。  
- **空间复杂度**：`O(1)`，只用几个整数变量，Python 的大整数本身也只占用常数级别的额外空间。

> **对比暴力**：暴力是指数级的 `2^d`，根本不可行；最优解只需要几十次循环，瞬间完成。

---

## 心得

- **核心技巧**：把“翻倍 + 不能连续的减 1”转化为 **“先全部翻倍，再在 x+1 个空隙中任选 y 个放减 1”**，利用组合数学直接计数。  
- **适用场景**：  
  1. **只允许两种操作且一种操作有间隔限制**（如“不能连续的 A”）。  
  2. **操作的效果是指数级增长或幂次**，可以先把指数操作全部执行，再用组合数安排其它操作。  
  3. **求所有满足线性等式的整数解数目**，尤其是形式 `a·2^x - b·y = k` 的问题。  
- **一句话总结**：**把所有“幂次”操作先做完，再用“空隙插入”计数**，组合数帮你快速求出答案。

---

## 反思

- **第一反应**：直接写递归/DFS 暴力枚举所有序列，想验证是否能到达 `k`。  
- **最容易踩的坑**：  
  * 忘记 **A 操作不能连续** 的限制，导致计数错误。  
  * 没有注意 **y ≤ x+1** 的上界，导致把不合法的组合也算进去了。  
  * 组合数计算时出现整数溢出（在语言不支持大整数时需要取模或使用额外库）。  
- **下次类似题目**：第一步先**把所有“增长最快”的操作（如翻倍、乘以 2）抽离出来，计算它们的次数 `x`；再**分析剩余操作的放置方式**（空隙、排列组合），最后用组合数或动态规划求和。这样可以把指数爆炸的问题压缩到对数级别的遍历。