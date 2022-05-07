# #1769. **最小移动次数使所有球聚集到每个盒子** / Minimum Number of Operations to Move All Balls to Each Box

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/)

---

## 题目（英文原版）

**Description**

You have n boxes. You are given a binary string boxes of length n, where boxes[i] is '0' if the ith box is empty, and '1' if it contains one ball.
In one operation, you can move one ball from a box to an adjacent box. Box i is adjacent to box j if abs(i - j) == 1. Note that after doing so, there may be more than one ball in some boxes.
Return an array answer of size n, where answer[i] is the minimum number of operations needed to move all the balls to the ith box.
Each answer[i] is calculated considering the initial state of the boxes.

**Examples**

**Example 1:**

```
Input: boxes = "110"
Output: [1,1,3]
Explanation: The answer for each box is as follows:
1) First box: you will have to move one ball from the second box to the first box in one operation.
2) Second box: you will have to move one ball from the first box to the second box in one operation.
3) Third box: you will have to move one ball from the first box to the third box in two operations, and move one ball from the second box to the third box in one operation.
```

**Example 2:**

```
Input: boxes = "001011"
Output: [11,8,5,4,3,4]
```

**Constraints**

- n == boxes.length
- 1 <= n <= 2000
- boxes[i] is either '0' or '1'.

---

## 题目（中文翻译）

你有 `n` 个盒子。给定一个长度为 `n` 的二进制字符串 `boxes`，其中 `boxes[i]` 为 `'0'` 表示第 `i` 个盒子为空，`'1'` 表示其中有一个球。  

一次操作中，你可以将一个球从某个盒子移动到相邻的盒子。盒子 `i` 与盒子 `j` 相邻当且仅当 `abs(i - j) == 1`。注意，执行操作后，某些盒子里可能会出现多个球。  

返回一个长度为 `n` 的数组 `answer`，其中 `answer[i]` 表示将所有球移动到第 `i` 个盒子所需的最少操作次数。  
每个 `answer[i]` 的计算都基于盒子的初始状态。

---

### 示例

**示例 1**

```text
Input: boxes = "110"
Output: [1,1,3]
Explanation:
1) 第 1 个盒子：需要将第 2 个盒子里的球向左移动一次，耗费 1 次操作。
2) 第 2 个盒子：需要将第 1 个盒子里的球向右移动一次，耗费 1 次操作。
3) 第 3 个盒子：需要将第 1 个盒子里的球向右移动两次，另外将第 2 个盒子里的球向右移动一次，总计 3 次操作。
```

**示例 2**

```text
Input: boxes = "001011"
Output: [11,8,5,4,3,4]
```

---

### 约束条件

- `n == boxes.length`
- `1 <= n <= 2000`
- `boxes[i]` 只能是 `'0'` 或 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**对每一个目标盒子 i，遍历所有盒子 j，如果 j 里有球（`boxes[j]=='1'`），就把这颗球搬到 i 所需要的步数是 `abs(i-j)`，把所有这些步数相加，就是 `answer[i]`。**  

- **使用的数据结构**：只需要一个字符串（相当于一排盒子）和一个长度为 `n` 的整数数组 `answer` 来保存结果。可以把字符串想象成一本“盒子目录”，下标就是盒子的位置，字符 `'1'` 表示这本目录里有球这本“书”，`'0'` 表示空的。
- **为什么正确**：搬球的规则只和距离有关，且每颗球的搬动互不影响（可以先搬完一颗再搬另一颗），所以把每颗球的距离逐个相加，正好等于把所有球都搬到同一个盒子所需要的最少操作次数。
- **时间/空间复杂度**：  
  - 外层遍历 `i`（`n` 次），内层遍历 `j`（`n` 次），每次只做 O(1) 的加法，所以总共是 `n × n = n²` 次操作，时间复杂度是 **O(n²)**。  
    - **大白话**：如果盒子有 1000 个，暴力解要检查 1000 × 1000 = 1,000,000 次，这在电脑里算是“慢一点”。  
  - 只用了一个长度为 `n` 的答案数组，空间复杂度是 **O(n)**（不算输入字符串本身）。

#### 代码（Python）

```python
def minOperations_bruteforce(boxes: str) -> list[int]:
    n = len(boxes)
    answer = [0] * n                     # 用来保存每个盒子的答案

    # 对每一个目标盒子 i
    for i in range(n):
        ops = 0                           # 累计把所有球搬到 i 需要的步数
        # 遍历所有盒子 j，找出里面的球
        for j in range(n):
            if boxes[j] == '1':           # 盒子 j 有球
                ops += abs(i - j)         # 这颗球搬到 i 需要的步数
        answer[i] = ops                   # 把累计的步数写入答案
    return answer
```

#### 复杂度

- **时间复杂度**：O(n²) — 需要两层循环，外层 `n` 次，内层 `n` 次，整体是 `n × n`。  
- **空间复杂度**：O(n) — 只额外用了一个长度为 `n` 的数组 `answer`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要遍历所有盒子**，导致二次遍历。实际上，我们可以把“搬球的距离”拆成两部分：**左侧的球向右搬** 和 **右侧的球向左搬**。如果我们已经知道了把所有左侧球搬到当前位置的总步数，那么把窗口向右移动一格，只会产生**一个很小的变化**：

- 当我们把窗口从 `i` 移动到 `i+1` 时：
  - 所有左边的球（原本在 `i` 左侧）与目标盒子的距离 **都增加 1**，因为目标盒子右移了一格。
  - 右边的球（原本在 `i+1` 右侧）与目标盒子的距离 **都减少 1**。
  - 还有一个特殊的球：如果 `boxes[i]` 本身有球，它从“左侧”变成了“目标盒子”，此时不再产生距离。

利用这个增量思路，我们可以用 **前缀和**（Prefix Sum）一次遍历得到所有答案：

1. **左到右遍历**，维护两个变量  
   - `left_count`：当前左侧（包括当前位置）已经出现了多少颗球。  
   - `left_ops`：把这些球全部搬到当前盒子所需的总步数。  
   当我们从 `i-1` 移动到 `i` 时，`left_ops` 增加 `left_count`（因为所有左侧球距离都加 1），然后如果 `boxes[i]=='1'`，`left_count` 加 1（因为新球加入左侧）。
   把每一步的 `left_ops` 记录下来，得到 `left[i]` —— 把左侧球搬到 i 所需的步数。

2. **右到左遍历**，同理得到 `right[i]` —— 把右侧球搬到 i 所需的步数。

3. 最终答案 `answer[i] = left[i] + right[i]`。

> **前缀和类比**：想象一条公路上有若干加油站（球），我们想算从某个加油站出发，到达所有其他站点的总油耗。把左边的油耗累加起来，再把右边的油耗累加起来，就是总油耗。

#### 代码（Python）

```python
def minOperations(boxes: str) -> list[int]:
    n = len(boxes)
    answer = [0] * n

    # ---------- 从左到右 ----------
    left_ops = 0      # 左侧球搬到当前位置的累计步数
    left_cnt = 0      # 左侧已经出现的球的数量
    for i in range(n):
        answer[i] += left_ops          # 先把左侧贡献加进去
        if boxes[i] == '1':            # 当前盒子有球，计入左侧计数
            left_cnt += 1
        left_ops += left_cnt           # 窗口右移一格，所有左侧球距离 +1

    # ---------- 从右到左 ----------
    right_ops = 0     # 右侧球搬到当前位置的累计步数
    right_cnt = 0     # 右侧已经出现的球的数量
    for i in range(n - 1, -1, -1):
        answer[i] += right_ops         # 加上右侧贡献
        if boxes[i] == '1':
            right_cnt += 1
        right_ops += right_cnt         # 窗口左移一格，所有右侧球距离 +1

    return answer
```

#### 复杂度

- **时间复杂度**：O(n) — 只遍历了两遍数组，每次都是 O(1) 的操作。相比暴力的 O(n²)，快了很多。  
- **空间复杂度**：O(1)（不计返回的 `answer` 数组） — 只用了常数个额外变量 `left_ops、left_cnt、right_ops、right_cnt`，没有额外的随输入规模增长的数组。

---

## 心得

- **核心技巧**：**前缀和 + 增量思路**（即把“每次移动窗口”产生的变化用 O(1) 更新）。  
- **适用的题型**：  
  1. “数组每个位置的左右累计贡献”类问题，例如 *“最小移动次数把所有 1 移到同一位置”*、*“每个位置的左侧/右侧子数组和”*。  
  2. “滑动窗口增量更新”类问题，如 *“最长子数组满足条件”* 中需要快速更新窗口统计。  
  3. “前缀和求区间和” 的变形，如 *“子数组和等于 K”*。  
- **一句话总结解题钥匙**：**把全局 O(n²) 的求和拆成两次线性扫描，每次只记录“左侧/右侧已有多少球”和“累计步数”，利用窗口移动的增量更新即可。**

---

## 反思

- **第一反应**：看到“每颗球到目标盒子的距离是 `abs(i-j)`”，立刻想到双层循环逐个相加——这就是暴力解。  
- **最容易踩的坑**：  
  - 忽略 **“每个 answer[i] 都是基于原始状态”**，如果在遍历时直接修改 `boxes` 会导致后面的计算错误。  
  - 边界条件：第一个盒子没有左侧，最后一个盒子没有右侧，需确保计数变量在进入循环前已经是 0。  
- **下次遇到同类题**：第一步先问自己：“是否可以把“对所有元素的求和”拆成“左侧贡献 + 右侧贡献”，从而用一次前缀扫描得到左侧，再一次逆序扫描得到右侧？”如果答案是肯定的，就可以立刻走向 O(n) 的最优解。