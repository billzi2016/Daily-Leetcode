# #2335. 填满杯子的最少时间 / Minimum Amount of Time to Fill Cups

> 难度：简单 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-amount-of-time-to-fill-cups/)

---

## 题目（英文原版）

**Description**

You have a water dispenser that can dispense cold, warm, and hot water. Every second, you can either fill up 2 cups with different types of water, or 1 cup of any type of water.
You are given a 0-indexed integer array amount of length 3 where amount[0], amount[1], and amount[2] denote the number of cold, warm, and hot water cups you need to fill respectively. Return the minimum number of seconds needed to fill up all the cups.

**Examples**

**Example 1:**

```
Input: amount = [1,4,2]
Output: 4
Explanation: One way to fill up the cups is:
Second 1: Fill up a cold cup and a warm cup.
Second 2: Fill up a warm cup and a hot cup.
Second 3: Fill up a warm cup and a hot cup.
Second 4: Fill up a warm cup.
It can be proven that 4 is the minimum number of seconds needed.
```

**Example 2:**

```
Input: amount = [5,4,4]
Output: 7
Explanation: One way to fill up the cups is:
Second 1: Fill up a cold cup, and a hot cup.
Second 2: Fill up a cold cup, and a warm cup.
Second 3: Fill up a cold cup, and a warm cup.
Second 4: Fill up a warm cup, and a hot cup.
Second 5: Fill up a cold cup, and a hot cup.
Second 6: Fill up a cold cup, and a warm cup.
Second 7: Fill up a hot cup.
```

**Example 3:**

```
Input: amount = [5,0,0]
Output: 5
Explanation: Every second, we fill up a cold cup.
```

**Constraints**

- amount.length == 3
- 0 <= amount[i] <= 100

---

## 题目（中文翻译）

你有一台饮水机（water dispenser），它可以提供冷水（cold water）、温水（warm water）和热水（hot water）。每秒，你可以 **同时装满 2 个不同种类的杯子**，或者 **装满任意一种的 1 个杯子**。

给定一个下标从 0 开始、长度为 3 的整数数组 `amount`，其中 `amount[0]`、`amount[1]`、`amount[2]` 分别表示需要装满的冷水、温水和热水杯的数量。返回装满所有杯子所需的 **最少秒数**。

---

### 示例

**示例 1**

> Input: `amount = [1,4,2]`  
> Output: `4`  
> **解释**：一种可行的装杯方案是：  
> - 第 1 秒：装满 1 个冷水杯和 1 个温水杯。  
> - 第 2 秒：装满 1 个温水杯和 1 个热水杯。  
> - 第 3 秒：装满 1 个温水杯和 1 个热水杯。  
> - 第 4 秒：装满 1 个温水杯。  
> 可以证明，4 秒是最少需要的时间。

**示例 2**

> Input: `amount = [5,4,4]`  
> Output: `7`  
> **解释**：一种可行的装杯方案是：  
> - 第 1 秒：装满 1 个冷水杯和 1 个热水杯。  
> - 第 2 秒：装满 1 个冷水杯和 1 个温水杯。  
> - 第 3 秒：装满 1 个冷水杯和 1 个温水杯。  
> - 第 4 秒：装满 1 个温水杯和 1 个热水杯。  
> - 第 5 秒：装满 1 个冷水杯和 1 个热水杯。  
> - 第 6 秒：装满 1 个冷水杯和 1 个温水杯。  
> - 第 7 秒：装满 1 个热水杯。

**示例 3**

> Input: `amount = [5,0,0]`  
> Output: `5`  
> **解释**：每秒只装满 1 个冷水杯。

---

### 约束条件

- `amount.length == 3`
- `0 <= amount[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每秒只装一杯**。  
不管有什么水，只要还有未装的杯子，就把其中任意一杯装满。  
这样可以保证一定能把所有杯子装完，只是可能会花费很多时间。

- **用到的数据结构**：只需要一个整数数组 `amount`，保存三种水还有多少杯子待装。  
  数组就像我们手里的一张小本子，记下每种水的“剩余数量”。  
- **为什么正确**：只要每秒装一杯，最终所有杯子都会被装满，符合题目要求。  
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(total)**，这里的 `total = amount[0] + amount[1] + amount[2]`，即所有杯子的总数。  
    用大白话说，就是“装几杯，就花几秒”。  
  - 空间复杂度是 **O(1)**，只用了常数个额外变量（计数器、临时变量），不随输入规模增长。

> 虽然这种做法能得到答案，但显然不是最少时间。它相当于把每秒只能装两杯的机器“强行”只用来装一杯，浪费了很多机会。

#### 代码（Python）

```python
def fill_cups_bruteforce(amount):
    """
    直觉解：每秒只装一杯，答案就是所有杯子总数。
    """
    # total 表示所有杯子的数量，即需要的最少秒数的上界
    total = amount[0] + amount[1] + amount[2]
    return total
```

#### 复杂度

- **时间复杂度**：O(total) → 只要遍历一次数组求和，和杯子数成正比。  
- **空间复杂度**：O(1) → 只用了几个整数变量，不会随 `amount` 长度增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**每秒装两杯（前提是有两种不同的水）** 能显著减少总时间。  
要想让每秒都装两杯，需要每次挑选**剩余杯子最多的两种水**，因为它们最容易形成“不同种类配对”。  

**瓶颈**  
- 暴力解只装一杯，浪费了每秒可以装两杯的机会。  
- 如果我们总是优先把数量最多的两种水配对，就能让“装两杯”的机会尽可能多。

**关键观察**  
1. 每秒最多只能装两杯，所以总时间至少是 `ceil(total / 2)`（把所有杯子两两配对，偶数刚好配完，奇数会剩一杯，需要再加一秒）。  
2. 另一方面，如果某一种水的数量本身就很多，超过了其他两种之和，那么即使把其它两种全部配对完，仍然会剩下这类水只能单独装。此时最少时间就是这最多的那种水的数量。  

因此答案是两者的 **最大值**：

```
answer = max( max(amount),  ceil(total / 2) )
```

其中 `ceil(total/2)` 用整数实现可以写成 `(total + 1) // 2`。

**为什么这个公式一定成立**  
- **上界**：我们可以用一种贪心模拟：每秒取剩余最多的两种水各装一杯，直到只剩下一种或没有水。这个过程恰好需要 `max(max(amount), (total+1)//2)` 秒。  
- **下界**：任何方案都不可能少于这两个数中的较大者。  
  - 若 `max(amount)` 较大，则即使把其它两种全部配对，也仍需要单独装剩下的那种水，最少要 `max(amount)` 秒。  
  - 若 `ceil(total/2)` 较大，则说明即使每秒都装两杯，也至少需要这么多秒才能把所有杯子配完。  

两者取最大值即可得到最小可能的秒数。

**类比**  
把三种水想象成三堆不同颜色的球。每秒可以拿走**两种不同颜色**的球各一颗。我们希望把球尽快全部拿完，就要把数量最多的两堆球交叉拿走，避免只剩下一堆球而浪费配对机会。  

#### 代码（Python）

```python
def fill_cups_optimal(amount):
    """
    最优解：每秒尽可能装两杯不同种类的水。
    公式 answer = max(最大种类数量, ceil(总杯数/2))
    """
    total = sum(amount)                     # 所有杯子的总数
    max_one = max(amount)                   # 任意一种水的最大剩余杯数
    # (total + 1) // 2 等价于 math.ceil(total / 2)
    half_ceil = (total + 1) // 2
    return max(max_one, half_ceil)
```

#### 复杂度

- **时间复杂度**：O(1) → 只做了几次加法、取最大值和除法，和输入规模无关。  
- **空间复杂度**：O(1) → 只用了常数个临时变量。

---

## 心得

- **核心技巧**：利用**“配对上限”** 与 **“单种上限”** 两个下界取最大值。  
- **适用的题型**  
  1. “每次可以同时完成两件不同任务” 类的调度问题（如 LeetCode 1833 “Maximum Ice Cream Bars” 的类似思路）。  
  2. “把若干资源两两配对” 的最小时间/步数问题（如 1975 “Maximum Matrix Sum” 中的配对思路）。  
  3. “只允许一次操作处理两种不同元素” 的贪心类题目（如 2073 “Time to Buy Tickets” 的变形）。  
- **一句话总结解题钥匙**：**把“最多的那类”与“总量的一半”两者取最大，即是最少秒数**。

---

## 反思

- **第一反应**：看到“每秒可以装两杯不同种类”，立刻想到“尽量让每秒都装两杯”。于是考虑把杯子两两配对。  
- **最容易踩的坑**  
  - 忽略 **单种数量过多** 的情况，导致只用 `ceil(total/2)` 会低估答案。  
  - 边界条件：全是同一种水（如 `[5,0,0]`），此时只能每秒装一杯，需要返回该种的数量。  
- **下次遇到同类题**：第一步先判断“是否有一种类型的数量大于其余两种之和”。如果是，答案就是它的数量；否则答案就是 `ceil(total/2)`。这样可以快速得出最优解。