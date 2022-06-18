# #1823. 环形游戏的获胜者 / Find the Winner of the Circular Game

> 难度：中等 · 标签：Array、Math、Recursion、Queue、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-winner-of-the-circular-game/)

---

## 题目（英文原版）

**Description**

There are n friends that are playing a game. The friends are sitting in a circle and are numbered from 1 to n in clockwise order. More formally, moving clockwise from the ith friend brings you to the (i+1)th friend for 1 <= i < n, and moving clockwise from the nth friend brings you to the 1st friend.
The rules of the game are as follows:
Given the number of friends, n, and an integer k, return the winner of the game.
Follow up:
Could you solve this problem in linear time with constant space?

**Examples**

**Example 1:**

```
Input: n = 5, k = 2
Output: 3
Explanation: Here are the steps of the game:
1) Start at friend 1.
2) Count 2 friends clockwise, which are friends 1 and 2.
3) Friend 2 leaves the circle. Next start is friend 3.
4) Count 2 friends clockwise, which are friends 3 and 4.
5) Friend 4 leaves the circle. Next start is friend 5.
6) Count 2 friends clockwise, which are friends 5 and 1.
7) Friend 1 leaves the circle. Next start is friend 3.
8) Count 2 friends clockwise, which are friends 3 and 5.
9) Friend 5 leaves the circle. Only friend 3 is left, so they are the winner.
```

**Example 2:**

```
Input: n = 6, k = 5
Output: 1
Explanation: The friends leave in this order: 5, 4, 6, 2, 3. The winner is friend 1.
```

**Constraints**

- 1 <= k <= n <= 500

---

## 题目（中文翻译）

有 **n** 位朋友在玩一个游戏。朋友们围成一个圆圈，按顺时针顺序编号为 `1` 到 `n`。更形式化地说，顺时针从第 `i` 位朋友移动会到第 `i+1` 位朋友（`1 <= i < n`），而顺时针从第 `n` 位朋友移动会回到第 `1` 位朋友。

游戏规则如下：

给定朋友的数量 `n` 和一个整数 `k`，返回游戏的获胜者编号。

## 示例 1

**输入**: `n = 5, k = 2`  
**输出**: `3`  
**解释**: 游戏进行过程如下：

1. 从朋友 `1` 开始。  
2. 顺时针数 `2` 位朋友，分别是朋友 `1` 和朋友 `2`。  
3. 朋友 `2` 离开圆圈。下一个起始点是朋友 `3`。  
4. 顺时针数 `2` 位朋友，分别是朋友 `3` 和朋友 `4`。  
5. 朋友 `4` 离开圆圈。下一个起始点是朋友 `5`。  
6. 顺时针数 `2` 位朋友，分别是朋友 `5` 和朋友 `1`。  
7. 朋友 `1` 离开圆圈。...（后续过程省略）  

最终剩下的朋友是编号 `3`，因此获胜者为 `3`。

## 示例 2

**输入**: `n = 6, k = 5`  
**输出**: `1`  
**解释**: 朋友离开的顺序为 `5, 4, 6, 2, 3`，最后剩下的朋友是 `1`，所以获胜者为 `1`。

## 约束条件

- `1 <= k <= n <= 500`

## 进阶

是否可以在 **O(n)** 的线性时间且 **O(1)** 的常数空间内完成此题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有朋友按顺序放进一个**循环列表**（可以用 Python 的 `list` 或 `deque` 来模拟），然后按照题目规则一次一次地“数 k 个人”，把第 k 个人踢出圈。

- **数据结构类比**：  
  - `list` 就像一本顺序排好的通讯录，里面的每一项是一个朋友的编号。  
  - `deque`（双端队列）可以看作是一条可以从两端取出或放入元素的传送带，取出首位元素的速度非常快。  

- **正确性说明**：  
  每次我们从当前所在位置开始，顺时针数 `k` 个人（包括当前这位），正好把第 `k` 位朋友标记为“出局”。把他从列表中删除后，游戏的下一轮自然从他的下一个朋友开始。如此循环，直到只剩下最后一位朋友，他就是胜者。

- **复杂度大白话**：  
  - **时间复杂度**：每次删除一个元素都要把后面的元素往前搬一次（`list.pop(idx)` 的时间是 O(长度)），最坏会进行 `n-1` 次删除，所以整体大概是 `1 + 2 + … + (n-1) = n·(n-1)/2`，用大写的 **O(n²)** 表示。可以把 O(n²) 想成“随着人数 n 增大，耗时会像 n 的平方那样快速增长”。  
  - **空间复杂度**：我们需要保存所有人的编号，最多是 `n` 个，用 **O(n)** 的额外空间。

#### 代码（Python）

```python
from collections import deque

def find_the_winner_bruteforce(n: int, k: int) -> int:
    # 把 1~n 的编号放进循环队列
    q = deque(range(1, n + 1))

    # 当前指向的朋友默认是队首
    while len(q) > 1:                     # 只剩一个人时结束
        # 把前 (k-1) 个人依次搬到队尾，相当于顺时针数 k 个人
        q.rotate(-(k - 1))                # rotate 负数向左转，相当于把前面的人搬到后面
        q.popleft()                       # 第 k 个人出局，直接弹出队首
        # 下一轮自然从当前队首开始（已经是第 k+1 个人）

    return q[0]                           # 唯一剩下的就是赢家
```

#### 复杂度

- **时间复杂度**：`O(n·k)`，因为每轮 `rotate` 需要移动 `k-1` 步，总共会执行约 `n` 轮。若 `k` 与 `n` 同阶，则约为 `O(n²)`。  
  - **含义**：人数越多、数的步数越大，程序跑得越慢，最坏情况下接近“人数的平方”。  
- **空间复杂度**：`O(n)`，需要保存全部 `n` 位朋友的编号。  
  - **含义**：如果 `n` 增加一倍，所占内存也会大约增加一倍。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈**在于每次都要把整个列表/队列旋转或搬移，导致大量无用的元素搬动。我们其实不需要真的“转动”圈子，只要**记录下当前的相对位置**即可。

这道题其实是著名的**约瑟夫环（Josephus）**问题。约瑟夫环有一个数学递推公式：

> 当有 `n` 个人、每数 `k` 人淘汰一次时，胜者的编号 `f(n, k)` 满足  
> `f(1, k) = 0`（只有一个人时，编号 0（从 0 开始计数）自然是胜者）  
> `f(n, k) = (f(n-1, k) + k) % n`（把人数从 `n-1` 扩展到 `n` 时，胜者位置向右平移 `k` 步，再取模防止越界）

这里的递推是**从小到大**构造答案的：先算出只有 1 个人时的胜者位置（显然是 0），然后逐步加入第 2、3、…、n 个人，每加入一个人，只需要把已有的胜者位置往右移动 `k` 步（因为每次淘汰都是数 `k`），再对当前人数取模。

- **为什么公式成立**（零基编号解释）：  
  假设已经算出在 `n-1` 个人时的胜者位置是 `x`（相对于当时的圆圈的第一个人）。现在把第 `n` 个人加入圆圈，按照规则第 `k` 个人会被淘汰。相当于把原来的圆圈整体向左“旋转” `k` 位，导致原来的编号全部向右平移 `k`。于是原来的胜者 `x` 在新圆圈中的实际位置变成 `(x + k) % n`。这正是递推式。

- **从 0 基编号转回题目要求的 1 基**：最终得到的 `f(n, k)` 是从 0 开始计数的编号，答案要加 1。

- **核心技巧**：**递推 + 取模**，只需要一个整数变量保存当前的胜者位置，循环 `n-1` 次即可得到答案，**时间 O(n)**、**空间 O(1)**。

- **类比**：把这个过程想象成在一个转盘上不断把指针顺时针转 `k` 步，指针最终指向的那个人就是胜者。我们不必真的转动转盘，只需要记录指针每次转了多少步即可。

#### 代码（Python）

```python
def find_the_winner_optimal(n: int, k: int) -> int:
    """
    约瑟夫环的递推实现，时间 O(n)，空间 O(1)。
    返回的编号是 1 基（题目要求）。
    """
    winner = 0               # f(1, k) = 0，只有一个人时胜者编号为 0（0 基）
    for cur_n in range(2, n + 1):   # 依次把人数扩展到 2、3、…、n
        winner = (winner + k) % cur_n   # 递推公式：f(cur_n, k) = (f(cur_n-1, k) + k) % cur_n
    return winner + 1        # 转换成 1 基编号
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次 `2 … n` 的整数，循环体里只有几条算数运算。  
  - **含义**：人数翻倍，耗时大约只会翻倍，远比暴力解的“平方级”快很多。  
- **空间复杂度**：`O(1)` — 只用了一个整数变量 `winner`，不随 `n` 增长而增加额外空间。  
  - **含义**：不管有多少人，程序占用的额外内存基本不变。

---

## 心得

- **核心技巧**：约瑟夫环的递推公式 `f(n, k) = (f(n-1, k) + k) % n`，即“把上一步的答案右移 k 位再取模”。  
- **适用题型**：  
  1. “圆形淘汰”类问题（如 LeetCode 1823 “Find the Winner of the Circular Game”）。  
  2. “最后剩下的数字”类问题（如 LeetCode 1382 “Balance a Binary Search Tree” 中的递归思路类比）。  
  3. “循环移位”或“轮流删除”场景（如 “Elimination Game”）。  
- **一句话总结**：**把循环淘汰过程抽象成“指针顺时针跳 k 步”，用递推公式一步步把答案推进**。

---

## 反思

- **第一反应**：直接把所有人放进列表，模拟“数 k、删人、继续”——这就是暴力解。  
- **最容易踩的坑**：  
  - **下标与编号的差异**：递推公式使用 0 基下标，最后要记得加 1。  
  - **取模位置**：`(winner + k) % cur_n` 必须在每一步都取模，否则 `winner` 会越界。  
  - **k 大于当前人数**：即使 `k` 超过 `cur_n`，取模仍然有效，不需要额外处理。  
- **下次类似题的第一步**：先问自己“是否可以用约瑟夫环的递推或数学公式”，如果答案是肯定的，就直接写 O(n) 的迭代实现；否则再考虑用队列/链表做模拟。