# #2073. 买票所需的时间 / Time Needed to Buy Tickets

> 难度：简单 · 标签：Array、Queue、Simulation · [LeetCode 链接](https://leetcode.com/problems/time-needed-to-buy-tickets/)

---

## 题目（英文原版）

**Description**

There are n people in a line queuing to buy tickets, where the 0th person is at the front of the line and the (n - 1)th person is at the back of the line.
You are given a 0-indexed integer array tickets of length n where the number of tickets that the ith person would like to buy is tickets[i].
Each person takes exactly 1 second to buy a ticket. A person can only buy 1 ticket at a time and has to go back to the end of the line (which happens instantaneously) in order to buy more tickets. If a person does not have any tickets left to buy, the person will leave the line.
Return the time taken for the person initially at position k (0-indexed) to finish buying tickets.

**Examples**

**Example 1:**

```
Input: tickets = [2,3,2], k = 2
Output: 6
Explanation:
```

**Example 2:**

```
Input: tickets = [5,1,1,1], k = 0
Output: 8
Explanation:
```

**Constraints**

- n == tickets.length
- 1 <= n <= 100
- 1 <= tickets[i] <= 100
- 0 <= k < n

---

## 题目（中文翻译）

有 **n** 个人排队（queue）买票，编号为 **0** 的人在队首，编号为 **(n‑1)** 的人在队尾。  
给定一个下标从 **0** 开始的整数数组 **tickets**，长度为 **n**，其中 **tickets[i]** 表示第 **i** 个人想购买的票数。  
每购买一张票需要恰好 **1 秒**。一个人一次只能买 **1 张票**，买完后需要立刻（瞬间）回到队尾继续排队购买剩余的票。若某人已无票可买，则立即离开队列。  

返回最初位于下标 **k** 的人完成全部购票所需要的时间。

**示例 1**  
**输入**: `tickets = [2,3,2]`, `k = 2`  
**输出**: `6`  
**解释**:  
- 第 0 个人买第一张票 → 时间 +1（剩余票数 `[1,3,2]`），回到队尾。  
- 第 1 个人买第一张票 → 时间 +1（`[1,2,2]`），回到队尾。  
- 第 2 个人（即 k）买第一张票 → 时间 +1（`[1,2,1]`），回到队尾。  
- 第 0 个人买第二张票 → 时间 +1（`[0,2,1]`），离开队列。  
- 第 1 个人买第二张票 → 时间 +1（`[0,1,1]`），回到队尾。  
- 第 2 个人买第二张票 → 时间 +1（`[0,1,0]`），离开队列。  
共计 **6 秒**。

**示例 2**  
**输入**: `tickets = [5,1,1,1]`, `k = 0`  
**输出**: `8`  
**解释**:  
- 第 0 个人买第一张票 → 时间 +1（`[4,1,1,1]`），回到队尾。  
- 第 1、2、3 个人各买一张票 → 时间 +3（分别变为 `[4,0,0,0]`），他们全部离开队列。  
- 第 0 个人继续买剩余的 4 张票 → 时间 +4（`[0,0,0,0]`），离开队列。  
总时间 **8 秒**。

**约束条件**  
- `n == tickets.length`  
- `1 <= n <= 100`  
- `1 <= tickets[i] <= 100`  
- `0 <= k < n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把排队的过程 **完整地模拟** 一遍：

1. 用一个**队列**（可以把 Python 列表当作队列）存放每个人还剩多少票要买。  
   - 队列就像超市的排队收银：最前面的顾客先服务，买完一张票后如果还有需求，就回到队尾继续排队。  
2. 每一次循环，取出队首的 `person`（即 `pop(0)`），他买一张票，所需时间 `+1 秒`。  
   - 买完后把 `person-1`（剩余票数减 1）放回队尾；如果已经买完（`person-1 == 0`），则直接丢掉，不再放回。  
3. 同时记录我们关心的 **k 号人物**（原始位置）是否已经买完。只要他买完，就可以停止模拟，返回已经累计的时间。

> **为什么这样一定对？**  
> 题目说每个人只能一次买一张票，然后立刻回到队尾继续排队，这正好和我们对队列的操作一致。只要我们按照“取首、买票、若还有需求再进尾”的顺序执行，模拟的过程就完全等价于真实的排队过程。

#### 代码（Python）

```python
from collections import deque

def timeRequiredToBuy(tickets, k):
    """
    暴力模拟排队买票的全过程
    :param tickets: List[int] 每个人想买的票数
    :param k: int        我们关心的人的原始下标
    :return: int        完成买票所需的秒数
    """
    # 把每个人的剩余票数放进队列，队列里保存 (剩余票数, 是否是 k 号人物)
    q = deque([(t, i == k) for i, t in enumerate(tickets)])
    time = 0                     # 已经过去的时间（秒）

    while q:
        cur_tickets, is_target = q.popleft()   # 取出队首
        cur_tickets -= 1                        # 买一张票
        time += 1                               # 用时 1 秒

        # 如果这一次买完后已经没有票要买了
        if cur_tickets == 0:
            if is_target:                       # 正好是我们关心的 k 号
                return time                    # 直接返回答案
            # 其他人已经离开，继续循环
        else:
            # 还有票要买，放回队尾继续排队
            q.append((cur_tickets, is_target))

    return time   # 理论上不会走到这里
```

#### 复杂度

- **时间复杂度**：`O(total)`，其中 `total = sum(tickets)` 为所有人要买的票的总数。  
  - 用大白话说，就是**每卖出一张票**我们都要做一次循环，所以时间等价于“卖了多少票”。  
- **空间复杂度**：`O(n)`，需要把 `n` 个人的剩余票数以及是否是 k 号的标记全部放进队列。  
  - 类比成把所有人都站在一条线里，线的长度正好是人数。

---

### 2. 最优解

#### 思路  

虽然上面的模拟已经能够通过所有约束（`n ≤ 100, tickets[i] ≤ 100`），但我们可以 **省掉队列的额外空间**，只用原数组和一个指针来完成同样的过程：

1. 维护一个指针 `i`，从 `0` 循环到 `n-1`，再回到 `0`（即 `i = (i + 1) % n`），模拟“轮流”让每个人买票的顺序。  
2. 每次 `i` 指向的人买一张票，时间 `+1`。  
3. 当 `i == k` 且该人的票数已经买完（`tickets[k] == 0`）时，直接返回累计的时间。  
4. 如果某个人的票数已经为 `0`，我们仍然会让指针经过他，但不会再做任何操作（相当于他已经离开队列）。

> **瓶颈在哪？**  
> 暴力解用了 `deque` 来不断弹出/插入元素，这会产生额外的 **O(n)** 空间开销。我们只需要记录每个人还剩多少票，而不必真的把“离开”的人从结构里删除。直接在原数组上减计数即可。

> **核心技巧：循环遍历 + 原地修改**  
> 把“队列”抽象成“指针在环形数组上走”。环形遍历在很多排队、轮转调度的问题里都非常常见。

#### 代码（Python）

```python
def timeRequiredToBuy(tickets, k):
    """
    最优解：不使用额外的队列，仅用原数组和一个循环指针
    """
    n = len(tickets)
    time = 0          # 已经过去的秒数
    i = 0             # 当前轮到的下标

    while True:
        if tickets[i] > 0:          # 还有票要买，才会消耗时间
            tickets[i] -= 1
            time += 1

            # 如果正好是我们关心的 k 号，并且已经买完
            if i == k and tickets[i] == 0:
                return time

        # 移动指针到下一个人，形成环形遍历
        i = (i + 1) % n
```

#### 复杂度

- **时间复杂度**：`O(total)`，同样是“每卖出一张票”就走一次循环。  
  - 与暴力解的时间相同，只是常数更小（没有队列的出入操作）。  
- **空间复杂度**：`O(1)`，只使用了常数级的额外变量（`time、i、n`），不再需要额外的队列。  
  - 用大白话说，就是**只占用了几块内存**，和人数无关。

---

## 心得

- **核心技巧**：**循环遍历（环形指针） + 原地计数**，相当于“轮流服务”模型。  
- **适用场景**：  
  1. **轮转调度**（如 CPU 时间片轮转）  
  2. **循环队列模拟**（如 “Circular Elimination” 题）  
  3. **按顺序递减资源**（如 “Number of Steps to Reduce a Number to Zero”）  
- **一句话总结解题钥匙**：把排队过程抽象成“指针在环形数组上走，每次让指针所在位置的计数减 1”，当目标位置计数归零时即得到答案。

---

## 反思

- **第一反应**：直接把排队过程写成 `deque`，把每个人买票的动作逐一模拟。  
- **最容易踩的坑**：  
  - 忘记在买完票后把已经为 0 的人**不再放回队尾**，会导致死循环。  
  - 边界条件：当 `k` 为 0 且他买的票数最多时，需要确保循环能正确回到他自己。  
- **下次遇到同类题**：第一步先思考**“是否真的需要额外的数据结构”**，如果可以用**指针/下标**在原数组上直接模拟，那就直接走环形遍历。这样既省空间，又更易实现。