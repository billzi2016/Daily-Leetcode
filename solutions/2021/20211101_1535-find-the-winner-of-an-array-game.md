# #1535. 数组游戏的获胜者 / Find the Winner of an Array Game

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-winner-of-an-array-game/)

---

## 题目（英文原版）

**Description**

Given an integer array arr of distinct integers and an integer k.
A game will be played between the first two elements of the array (i.e. arr[0] and arr[1]). In each round of the game, we compare arr[0] with arr[1], the larger integer wins and remains at position 0, and the smaller integer moves to the end of the array. The game ends when an integer wins k consecutive rounds.
Return the integer which will win the game.
It is guaranteed that there will be a winner of the game.

**Examples**

**Example 1:**

```
Input: arr = [2,1,3,5,4,6,7], k = 2
Output: 5
Explanation: Let's see the rounds of the game:
Round |       arr       | winner | win_count
  1   | [2,1,3,5,4,6,7] | 2      | 1
  2   | [2,3,5,4,6,7,1] | 3      | 1
  3   | [3,5,4,6,7,1,2] | 5      | 1
  4   | [5,4,6,7,1,2,3] | 5      | 2
So we can see that 4 rounds will be played and 5 is the winner because it wins 2 consecutive games.
```

**Example 2:**

```
Input: arr = [3,2,1], k = 10
Output: 3
Explanation: 3 will win the first 10 rounds consecutively.
```

**Constraints**

- 2 <= arr.length <= 105
- 1 <= arr[i] <= 106
- arr contains distinct integers.
- 1 <= k <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个由互不相同的整数构成的整数数组 `arr` 和一个整数 `k`。  
游戏在数组的前两个元素（即 `arr[0]` 与 `arr[1]`）之间进行。每一回合（round），比较 `arr[0]` 与 `arr[1]` 的大小，较大的整数获胜并保持在下标 `0` 位置，较小的整数被移到数组末尾。游戏在同一个整数连续获胜 `k` 回合后结束。  
返回最终获胜的整数。题目保证一定会出现获胜者。

**示例**  

*示例 1*  
```text
Input: arr = [2,1,3,5,4,6,7], k = 2
Output: 5
Explanation: 下面展示游戏的每一回合：
Round |       arr       | winner | win_count
  1   | [2,1,3,5,4,6,7] | 2      | 1
  2   | [2,3,5,4,6,7,1] | 3      | 1
  3   | [3,5,4,6,7,1,2] | 5      | 1
  4   | [5,4,6,7,1,2,3] | 5      | 2
可以看到共进行 4 回合，整数 5 连续赢得 2 回合，因此成为获胜者。
```

*示例 2*  
```text
Input: arr = [3,2,1], k = 10
Output: 3
Explanation: 整数 3 连续赢得前 10 回合，直接成为获胜者。
```

**约束条件**  
- `2 <= arr.length <= 10^5`  
- `1 <= arr[i] <= 10^6`  
- `arr` 中的整数互不相同  
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
游戏的规则非常直接：  
1. 取数组最前面的两个数 `a = arr[0]`、`b = arr[1]` 比大小。  
2. 大的数留在最前面（位置 0），小的数搬到数组的最末端。  
3. 连续获胜的次数累计，一旦某个数连续赢了 `k` 场，游戏结束，返回它。

最直观的做法就是**一步步模拟**这个过程，直到出现连续 `k` 次胜利的数。  
- **使用的数据结构**：我们只需要在数组头部取两个元素、在尾部插入一个元素。用 Python 的 `collections.deque`（双端队列）非常合适——它就像一条可以随意在两端进出人的排队队伍，`popleft()` 把最前面的元素取走，`append()` 把元素放到队尾，时间都是 O(1)。  
- **为什么一定能得到正确答案**：因为每一轮的操作都是题目规定的唯一操作，模拟完整个过程自然就会得到最终的赢家。  

#### 代码（Python）  

```python
from collections import deque

def get_winner_bruteforce(arr, k):
    """
    直接模拟游戏过程，直到出现连续 k 胜利的数
    """
    dq = deque(arr)                 # 把列表变成双端队列，方便头尾操作
    cur_winner = dq[0]              # 当前在位置 0 的数（第一次是 arr[0]）
    win_cnt = 0                     # 连续赢的次数

    while True:                     # 无限循环，题目保证一定会终止
        first = dq.popleft()        # 取出最前面的两个数
        second = dq.popleft()

        if first > second:          # first 赢
            cur_winner = first
            win_cnt += 1
            dq.appendleft(first)    # 胜者继续留在位置 0
            dq.append(second)       # 败者搬到队尾
        else:                       # second 赢
            cur_winner = second
            win_cnt = 1             # 连胜计数重新开始，因为换了赢家
            dq.appendleft(second)
            dq.append(first)

        if win_cnt == k:            # 达到 k 连胜，返回赢家
            return cur_winner
```

#### 复杂度  

- **时间复杂度**：`O(k)`。每进行一次对决就算一次循环，最坏情况下要进行 `k` 次才能出现连续 `k` 胜利。  
  - 大白话：如果 `k` 是 10⁹，那就要跑 10⁹ 次，显然太慢了。  
- **空间复杂度**：`O(1)`（不计输入数组本身）。我们只用常数个额外变量和一个双端队列，队列本身是原数组的“搬家”，不算额外空间。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“可能要模拟非常多的轮次”**（`k` 可能高达 10⁹），这在实际运行时会超时。  
我们需要找出 **什么时候一定可以提前结束**，而不是盲目模拟到 `k` 次。

观察游戏的本质：

1. **数组里最大的数永远不会输**。因为两数相比较时，较大的数会留下，较小的数被送到队尾。于是，一旦最大数跑到最前面，它在之后的每一轮都会赢。  
2. **最多 `n‑1` 轮就能让最大数上位**。设数组长度为 `n`，每轮都会把当前的输家放到队尾，最多只需要让每个非最大数都被“赶走”一次，最大数自然会坐上位置 0。  
3. 因此：
   - 如果 `k` **大于等于** `n`（或者更宽松地 `k ≥ n‑1`），**答案必然是数组的最大值**，因为在最大数登顶后，它会一直连胜，必然先达到 `k` 连胜。  
   - 如果 `k` **小于** `n`，我们只需要模拟 **至多 `k` 次**（因为一旦有数连胜 `k` 次，游戏立刻结束），而 `k` 本身也小于 `n`，所以最多只会模拟 `n` 次，时间线性 `O(n)` 完全可接受。

基于以上两点，最优算法可以写成：

1. 先找出数组的最大值 `mx`（一次遍历，`O(n)`）。  
2. 若 `k >= n`（等价于 `k >= len(arr)`），直接返回 `mx`。  
3. 否则，用同样的双端队列模拟游戏，但最多只循环 `k` 次——因为一旦出现 `k` 连胜就返回，最多也只会跑 `k < n` 步。  

#### 代码（Python）  

```python
from collections import deque

def get_winner(arr, k):
    """
    高效求解：如果 k 很大直接返回最大值；否则最多模拟 k 轮。
    """
    n = len(arr)
    mx = max(arr)                     # O(n) 找最大值

    # 情况 1：k >= n，最大值必然是最终赢家
    if k >= n:
        return mx

    # 情况 2：k < n，模拟至多 k 轮
    dq = deque(arr)
    cur_winner = dq[0]                # 初始冠军（arr[0]）
    win_cnt = 0

    while True:                       # 这里最多循环 k 次
        a = dq.popleft()
        b = dq.popleft()

        if a > b:                     # a 赢
            cur_winner = a
            win_cnt += 1
            dq.appendleft(a)          # 胜者留在最前
            dq.append(b)              # 败者去队尾
        else:                         # b 赢
            cur_winner = b
            win_cnt = 1               # 连胜计数重新开始
            dq.appendleft(b)
            dq.append(a)

        if win_cnt == k:              # 达到 k 连胜
            return cur_winner
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - **最坏情况**：`k < n` 时我们最多模拟 `k`（小于 `n`）轮；`k >= n` 时直接返回最大值，只用了一次遍历找最大值。  
  - 与暴力解的 `O(k)` 相比，**即使 `k` 为 10⁹，也只需要线性扫描数组一次**，极大提升效率。  
- **空间复杂度**：`O(1)`（不计输入数组本身）。同样只用了常数个变量和一个双端队列。

---

## 心得  

- **核心技巧**：**最大值的“不可战胜”属性** + **提前终止的边界判断**。  
- **适用的题型**：  
  1. “连续 k 次获胜”类的模拟题（如 “Find the Winner of an Array Game”）。  
  2. “在序列中出现 k 次连续相同事件”类问题（如 “找出出现次数最多的连续子串”）。  
  3. “数组中最大元素必然是最终胜者” 的情形（如 “找出最终会占据首位的元素”）。  
- **一句话总结解题钥匙**：**先判断是否可以直接用最大值回答，若不能再用有限次模拟**。

---

## 反思  

- **第一反应**：看到“连续 k 胜利”，自然想到“一次一次模拟”。  
- **最容易踩的坑**：  
  - 忽略 `k` 可能远大于数组长度，导致模拟次数爆炸（超时）。  
  - 没有正确处理 **连续胜利计数的重置**：当不同的数赢得一轮时，连胜计数必须恢复为 1（因为新冠军已经赢了一场）。  
  - 边界情况如 `k = 1`（只要一次比较的胜者即可）以及 `arr` 长度为 2 时的特殊表现。  
- **下次遇到同类题**，第一步应该问自己：“**最大元素是否会一直赢下去？**” 若答案是肯定的，先返回最大值；否则再考虑**限制循环次数的模拟**。