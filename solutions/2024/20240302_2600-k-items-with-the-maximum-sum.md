# #2600. 最大和的 K 件物品 / K Items With the Maximum Sum

> 难度：简单 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/k-items-with-the-maximum-sum/)

---

## 题目（英文原版）

**Description**

There is a bag that consists of items, each item has a number 1, 0, or -1 written on it.
You are given four non-negative integers numOnes, numZeros, numNegOnes, and k.
The bag initially contains:
We want to pick exactly k items among the available items. Return the maximum possible sum of numbers written on the items.

**Examples**

**Example 1:**

```
Input: numOnes = 3, numZeros = 2, numNegOnes = 0, k = 2
Output: 2
Explanation: We have a bag of items with numbers written on them {1, 1, 1, 0, 0}. We take 2 items with 1 written on them and get a sum in a total of 2.
It can be proven that 2 is the maximum possible sum.
```

**Example 2:**

```
Input: numOnes = 3, numZeros = 2, numNegOnes = 0, k = 4
Output: 3
Explanation: We have a bag of items with numbers written on them {1, 1, 1, 0, 0}. We take 3 items with 1 written on them, and 1 item with 0 written on it, and get a sum in a total of 3.
It can be proven that 3 is the maximum possible sum.
```

**Constraints**

- 0 <= numOnes, numZeros, numNegOnes <= 50
- 0 <= k <= numOnes + numZeros + numNegOnes

---

## 题目（中文翻译）

有一个装有物品（item）的袋子（bag），每件物品上写有数字 1、0 或 -1。  
给定四个非负整数 `numOnes`、`numZeros`、`numNegOnes` 和 `k`。  

初始时，袋子中包含：

- `numOnes` 个写有 1 的物品  
- `numZeros` 个写有 0 的物品  
- `numNegOnes` 个写有 -1 的物品  

我们需要恰好挑选 `k` 件物品，返回这些被挑选物品上数字的最大可能和（sum）。

---

### 示例

**示例 1**

```text
Input: numOnes = 3, numZeros = 2, numNegOnes = 0, k = 2
Output: 2
Explanation: 袋子中物品的数字为 {1, 1, 1, 0, 0}。我们挑选了两件数字为 1 的物品，得到的总和为 2。可以证明 2 是最大的可能和。
```

**示例 2**

```text
Input: numOnes = 3, numZeros = 2, numNegOnes = 0, k = 4
Output: 3
Explanation: 袋子中物品的数字为 {1, 1, 1, 0, 0}。我们挑选了三件数字为 1 的物品和一件数字为 0 的物品，得到的总和为 3。可以证明 3 是最大的可能和。
```

---

### 约束条件

- `0 <= numOnes, numZeros, numNegOnes <= 50`
- `0 <= k <= numOnes + numZeros + numNegOnes`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把所有物品的数值展开成一个列表，例如  

```
numOnes = 3, numZeros = 2, numNegOnes = 1
列表 = [1, 1, 1, 0, 0, -1]
```

我们要从这 6 个数里挑 **恰好 k** 个，使得它们的和最大。  
最直接的想法是：**把所有合法的挑法都枚举一遍，算出每种挑法的和，取最大的那个**。  

- **数据结构**：这里用到的最基本的结构是**计数**（`for` 循环）和**列表**。可以把挑选的过程看成“从三种颜色的球中取球”，  
  - 1️⃣ 球的数量 = `numOnes`，  
  - 0️⃣ 球的数量 = `numZeros`，  
  - -1️⃣ 球的数量 = `numNegOnes`。  
  只要遍历所有可能的“取多少个 1、取多少个 0、剩下的自然是 -1”，就覆盖了所有挑法。

- **正确性**：因为我们枚举了 **每一种** 可能的取法（只要满足总数为 k），必然会找到最大和的那一种。

- **复杂度**：  
  - 外层循环遍历 `take_one`（0 到 `min(numOnes, k)`），  
  - 内层循环遍历 `take_zero`（0 到 `min(numZeros, k - take_one)`），  
  - 剩下的 `take_neg = k - take_one - take_zero` 自动确定。  
  最坏情况下 `k ≤ 150`，所以循环次数大约是 `O(k²)`（大约几千次），对这道题完全够用。  
  空间只用了几个整数，`O(1)`。

#### 代码（Python）

```python
def max_sum_bruteforce(numOnes: int, numZeros: int, numNegOnes: int, k: int) -> int:
    """
    暴力枚举所有合法的挑选方案，返回最大可能的和。
    """
    best = -10**9                     # 先设一个很小的值，后面会被更新
    # 先决定挑多少个写着 1 的物品
    for take_one in range(0, min(numOnes, k) + 1):
        # 再决定挑多少个写着 0 的物品
        max_zero = min(numZeros, k - take_one)
        for take_zero in range(0, max_zero + 1):
            # 剩下的必须是 -1
            take_neg = k - take_one - take_zero
            if take_neg > numNegOnes:        # -1 不够取，跳过这个组合
                continue
            # 计算当前组合的总和
            cur_sum = take_one * 1 + take_zero * 0 + take_neg * (-1)
            # 更新答案
            best = max(best, cur_sum)
    return best
```

#### 复杂度

- **时间复杂度**：`O(k²)`  
  - “O(k²)” 的意思是：当 `k` 变大时，运行时间大约会随 `k` 的平方增长。比如 `k=100` 时，循环大约进行 `10,000` 次，仍然很快。

- **空间复杂度**：`O(1)`  
  - 只用了常数个整数变量，不会随输入规模增长而占用更多内存。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**挑选的顺序其实很明显**：

1. **先把所有的 1 拿走**，因为 1 对和的贡献最大。  
2. 如果 1 已经拿完了，但我们还没拿够 `k`，**再拿 0**。0 不会让和变小，也不会变大，等于是“填坑”。  
3. 当 1 和 0 都拿完了，仍然不足 `k` 时，只能**被迫拿 -1**，这会把和拉低，但没有别的选择。

这三个步骤正好对应 **贪心**（Greedy）思想：在每一步都做对当前局部最有利的选择，最终得到全局最优。  
因为每一种数值的贡献是固定的（1 > 0 > -1），没有“取了某个 0 会让以后更容易取到 1”之类的相互影响，所以贪心一定能得到最优解。

实现上只需要**计算**我们到底能拿多少个 1、0、-1，而不需要真正遍历所有组合：

```
take_one = min(numOnes, k)
remaining = k - take_one
take_zero = min(numZeros, remaining)
remaining -= take_zero
take_neg = remaining          # 此时只能是 -1
answer = take_one*1 + take_zero*0 + take_neg*(-1)
```

#### 代码（Python）

```python
def max_sum_greedy(numOnes: int, numZeros: int, numNegOnes: int, k: int) -> int:
    """
    贪心解：先取尽可能多的 1，再取 0，最后才是 -1。
    时间 O(1)，空间 O(1)。
    """
    # 第一步：尽量多拿 1
    take_one = min(numOnes, k)
    k -= take_one                     # 剩下还要拿的数量

    # 第二步：尽量多拿 0（因为 0 不会降低和）
    take_zero = min(numZeros, k)
    k -= take_zero                    # 再次更新剩余需要的数量

    # 第三步：只能拿 -1 了
    take_neg = k                      # 此时 k 已经是 “还需要多少个 -1”

    # 计算总和
    return take_one * 1 + take_zero * 0 + take_neg * (-1)
```

#### 复杂度

- **时间复杂度**：`O(1)`  
  - “O(1)” 表示不管 `k` 多大，代码执行的步骤数都是固定的几行，几乎瞬间完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：**贪心**——在每一步都选择当前最有利的项（这里是先取 1，再取 0，最后取 -1），因为各项之间没有相互制约，局部最优即全局最优。  
- **适用的题型**：  
  1. “取最大/最小和”类题目，例如 **"Maximum Sum of K Items"**、**"Maximum Points You Can Obtain from Cards"**。  
  2. “先取价值最高的资源”类题目，例如 **"Maximum Profit After Buying and Selling Stock I"**（先买低后卖高的思想）。  
- **一句话总结**：**只要把价值最高的物品尽可能多地拿走，剩下的再填平常数值，答案就是最大和**。

## 反思

- **第一反应**：看到只有三种固定数值（1、0、-1），马上想到“把大的先拿”。  
- **最容易踩的坑**：  
  - 忘记 `k` 可能为 0，直接返回 0；  
  - 当 `k` 大于 `numOnes + numZeros` 时，必须确保取到的 `-1` 不会超过 `numNegOnes`（但题目保证 `k` 不会超过总数量）。  
- **下次类似题的第一步**：**先把“价值最高的那类”数量算出来，看能不能全部拿完；剩余的再按价值递减的顺序处理**。这样可以快速判断是否需要继续贪心或直接返回答案。