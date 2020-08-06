# #950. 按递增顺序翻开卡牌 / Reveal Cards In Increasing Order

> 难度：中等 · 标签：Array、Queue、Sorting、Simulation · [LeetCode 链接](https://leetcode.com/problems/reveal-cards-in-increasing-order/)

---

## 题目（英文原版）

**Description**

You are given an integer array deck. There is a deck of cards where every card has a unique integer. The integer on the ith card is deck[i].
You can order the deck in any order you want. Initially, all the cards start face down (unrevealed) in one deck.
You will do the following steps repeatedly until all cards are revealed:
Return an ordering of the deck that would reveal the cards in increasing order.
Note that the first entry in the answer is considered to be the top of the deck.

**Examples**

**Example 1:**

```
Input: deck = [17,13,11,2,3,5,7]
Output: [2,13,3,11,5,17,7]
Explanation: 
We get the deck in the order [17,13,11,2,3,5,7] (this order does not matter), and reorder it.
After reordering, the deck starts as [2,13,3,11,5,17,7], where 2 is the top of the deck.
We reveal 2, and move 13 to the bottom.  The deck is now [3,11,5,17,7,13].
We reveal 3, and move 11 to the bottom.  The deck is now [5,17,7,13,11].
We reveal 5, and move 17 to the bottom.  The deck is now [7,13,11,17].
We reveal 7, and move 13 to the bottom.  The deck is now [11,17,13].
We reveal 11, and move 17 to the bottom.  The deck is now [13,17].
We reveal 13, and move 17 to the bottom.  The deck is now [17].
We reveal 17.
Since all the cards revealed are in increasing order, the answer is correct.
```

**Example 2:**

```
Input: deck = [1,1000]
Output: [1,1000]
```

**Constraints**

- 1 <= deck.length <= 1000
- 1 <= deck[i] <= 106
- All the values of deck are unique.

---

## 题目（中文翻译）

给定一个整数（integer）数组（array）`deck`。数组中的每个元素都是唯一的整数，`deck[i]` 表示第 `i` 张卡牌上的数字。  
你可以自行决定卡牌的初始排列顺序。最初，所有卡牌都面朝下（未翻开），并按你设定的顺序组成一副牌。  

接下来，你将重复执行以下步骤，直到所有卡牌全部翻开：

1. 翻开当前牌堆顶部的卡牌，记录其数字。  
2. 若牌堆中仍有剩余卡牌，将此时牌堆顶部的卡牌移至牌堆底部。  

请返回一种初始排列，使得按照上述过程翻开的卡牌序列恰好是递增的。  
答案中的第一个元素视为牌堆的顶部。

**示例 1**  
**输入**: `deck = [17,13,11,2,3,5,7]`  
**输出**: `[2,13,3,11,5,17,7]`  
**解释**:  
我们先得到顺序为 `[17,13,11,2,3,5,7]`（此顺序无关紧要）的牌堆，并对其重新排列。  
重新排列后，牌堆从顶部开始为 `[2,13,3,11,5,17,7]`，其中 `2` 为顶部。  
- 翻开 `2`，将 `13` 移到底部，牌堆变为 `[3,11,5,17,7,13]`。  
- 翻开 `3`，将 `11` 移到底部，牌堆变为 `[5,17,7,13,11]`。  
- 翻开 `5`，将 `17` 移到底部，牌堆变为 `[7,13,11,17]`。  
- 翻开 `7`，将 `13` 移到底部，牌堆变为 `[11,17,13]`。  
- 翻开 `11`，将 `17` 移到底部，牌堆变为 `[13,17]`。  
- 翻开 `13`，将 `17` 移到底部，牌堆变为 `[17]`。  
- 翻开 `17`。  

所有翻开的数字依次为 `2,3,5,7,11,13,17`，为递增顺序，答案正确。

**示例 2**  
**输入**: `deck = [1,1000]`  
**输出**: `[1,1000]`  

**约束条件**  
- `1 <= deck.length <= 1000`  
- `1 <= deck[i] <= 10^6`  
- `deck` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的排牌顺序都列举出来**，然后把每一种顺序按照题目描述的“揭牌+把下一张放到底部”的过程模拟一遍，检查最终揭出的序列是否是递增的。  

- **数据结构**：  
  - `list`（数组）用来保存一种可能的排牌顺序。  
  - `deque`（双端队列）用来模拟“从队首取牌、把队首牌放到队尾”的过程。`deque` 可以把左边（队首）弹出，也可以把右边（队尾）追加，类似于现实中排队的两端都可以进出的人。

- **为什么正确**：  
  把**所有**排列都尝试一遍，必然会碰到满足条件的那一种（如果有的话），于是我们一定能找到答案。

- **时间/空间复杂度**：  
  - **时间**：排出 `n` 张牌的所有排列需要 `n!`（阶乘）种可能。每种排列要模拟最多 `n` 次揭牌操作，所以总体是 `O(n!·n)`。  
    用大白话说，`n=6` 时大概要跑 `720×6≈4320` 步；`n=10` 时已经是 `3,628,800×10≈36,288,000` 步，几乎不可能在电脑上跑完。  
  - **空间**：只需要存放当前的排列和一个 `deque`，即 `O(n)`。

> **注意**：这只是教学演示，实际使用时根本不可行，只适合 **n ≤ 6** 左右的小规模测试。

#### 代码（Python）

```python
from itertools import permutations
from collections import deque

def reveal_order_bruteforce(deck):
    """
    暴力枚举所有排列，返回能够使揭牌顺序递增的那一个。
    只在极小规模（如 n <= 6）下才能接受。
    """
    # 先把 deck 排序，得到我们希望的揭牌顺序（递增）
    target = sorted(deck)

    # 枚举所有可能的排牌顺序
    for order in permutations(deck):
        q = deque(order)          # 用双端队列模拟牌堆
        revealed = []             # 记录揭出的牌

        while q:
            revealed.append(q.popleft())   # 揭出队首
            if q:                           # 如果还有牌，移动下一张到队尾
                q.append(q.popleft())

        if revealed == target:   # 与递增序列相同，说明找到了答案
            return list(order)

    return []   # 理论上不会到这里，因为一定有解
```

#### 复杂度

- **时间复杂度**：`O(n!·n)`  
  “阶乘”增长极快，实际只能在 `n ≤ 6` 时勉强跑完。

- **空间复杂度**：`O(n)`  
  只需要存放一个排列和一个 `deque`。

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**真正的难点不在于检查是否满足，而在于如何直接构造满足条件的初始顺序**。  
如果我们把**揭牌的过程倒过来**，会发现构造会非常简单。

**倒推过程**（从最后一张牌往前构造）：

1. 已知最终要揭出的顺序是递增的 `sorted_deck`（从小到大）。  
2. 想象逆向执行“揭牌+把下一张放到底部”。  
   - 正向：揭出最上面的牌 `x`，然后把新上面的牌 `y` 移到底部。  
   - 逆向：**先把最底部的牌搬到顶部**，再把原本应该最先揭出的牌 `x` 放到顶部。  
3. 从 **最大的牌** 开始逆向构造：  
   - 把当前牌（比如 17）放到结果序列的最前面。  
   - 如果此时结果序列里还有其他牌，则把**最底部的牌**（即当前序列的最后一个元素）移动到最前面。  
4. 按照从大到小的顺序依次处理所有牌，最终得到的序列就是我们要的初始排牌顺序。

**为什么正确**：  
- 逆向操作恰好是正向操作的逆过程，保证每一步都能“撤销”正向的揭牌/移动。  
- 由于我们从最大的牌开始放置，确保在正向揭牌时最先出现的正是最小的牌，递增顺序得以实现。

**关键数据结构**：  
- `deque`（双端队列）可以在 **左端**（队首）插入/弹出，也可以在 **右端**（队尾）插入/弹出，正好对应“把最底部的牌搬到最前面”这一步。

**类比**：  
想象一列排好队的人，正向过程是“让第一个人出场，然后把下一个人送到队尾”。逆向过程则是“先把队尾的人请回前面，然后再让本该第一个出场的人站到最前”。这样倒着排，正着来时就正好是我们想要的顺序。

#### 代码（Python）

```python
from collections import deque

def revealCardsInIncreasingOrder(deck):
    """
    逆向构造初始排牌顺序，使正向揭牌得到递增序列。
    时间复杂度 O(n log n)（排序），空间复杂度 O(n)。
    """
    n = len(deck)
    deck.sort()                     # 目标揭牌顺序：从小到大
    dq = deque()                    # 用双端队列逆向模拟

    # 从最大的牌开始倒着放
    for card in reversed(deck):     # 依次取  max, ..., min
        if dq:                       # 若队列非空，先把最底部的牌搬到顶部
            dq.appendleft(dq.pop())
        dq.appendleft(card)          # 把当前的最大牌放到最前面

    # deque 已经是我们要的答案，转成列表返回
    return list(dq)
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `deck.sort()` 需要 `O(n log n)`（排序的常规复杂度）。  
  - 逆向构造的循环每次只做常数时间的 `deque` 操作，累计 `O(n)`。  
  与暴力解的 `O(n!·n)` 相比，**指数级**的提升，几乎在任意 `n ≤ 1000`（题目上限）都能轻松跑完。

- **空间复杂度**：`O(n)`  
  需要额外的 `deque`（相当于一个长度为 `n` 的数组）来保存结果。

---

## 心得

- **核心技巧**：**逆向思维 + 双端队列**  
  先把最终目标（递增序列）排序，然后倒着模拟操作，把问题从“找答案”转化为“怎么把答案逆向恢复”。  
- **适用的题型**  
  1. **模拟类逆序构造**：如 LeetCode 209（长度最小子数组）里使用前缀和的逆向查找。  
  2. **排队/轮转问题**：如 轮流删除元素、约瑟夫环（Josephus problem）等。  
  3. **从结果逆推**：如 设计密码锁的逆向操作、恢复原始数组等。  
- **一句话总结**：**把过程倒过来做，往往能直接得到答案**。

---

## 反思

- **第一反应**：看到“揭牌后把下一张放到底部”，本能想到用 `deque` 按步骤模拟。  
- **最容易踩的坑**：  
  - 直接正向模拟需要遍历所有排列，时间爆炸。  
  - 逆向构造时忘记在每一步把 **最底部的牌**搬到顶部，导致最终顺序错误。  
  - 边界情况：只有一张牌时，逆向步骤中的 `if dq:` 必须判断为空，否则会出现 `pop` 错误。  
- **下次遇到类似题**：第一步先**思考是否可以倒着做**，把“最终状态”当作起点，尝试逆向一步步回到初始状态。这样往往能把指数级的搜索压缩到线性或线性对数级。