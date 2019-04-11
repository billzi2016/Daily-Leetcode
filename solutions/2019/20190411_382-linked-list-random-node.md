# #382. 链表随机节点 / Linked List Random Node

> 难度：中等 · 标签：Linked List、Math、Reservoir Sampling、Randomized · [LeetCode 链接](https://leetcode.com/problems/linked-list-random-node/)

---

## 题目（英文原版）

**Description**

Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.
Implement the Solution class:
Follow up:

**Examples**

**Example 1:**

```
Input
["Solution", "getRandom", "getRandom", "getRandom", "getRandom", "getRandom"]
[[[1, 2, 3]], [], [], [], [], []]
Output
[null, 1, 3, 2, 2, 3]

Explanation
Solution solution = new Solution([1, 2, 3]);
solution.getRandom(); // return 1
solution.getRandom(); // return 3
solution.getRandom(); // return 2
solution.getRandom(); // return 2
solution.getRandom(); // return 3
// getRandom() should return either 1, 2, or 3 randomly. Each element should have equal probability of returning.
```

**Constraints**

- The number of nodes in the linked list will be in the range [1, 104].
- -104 <= Node.val <= 104
- At most 104 calls will be made to getRandom.

---

## 题目（中文翻译）

给定一个单链表（singly linked list），返回链表中一个随机节点的值。每个节点被选中的概率必须相同。

实现 `Solution` 类：

**示例 1**

**Input**  
```
["Solution", "getRandom", "getRandom", "getRandom", "getRandom", "getRandom"]
[[[1, 2, 3]], [], [], [], [], []]
```

**Output**  
```
[null, 1, 3, 2, 2, 3]
```

**解释**  
```java
Solution solution = new Solution([1, 2, 3]);
solution.getRandom(); // 返回 1
solution.getRandom(); // 返回 3
solution.getRandom(); // 返回 2
solution.getRandom(); // 返回 2
solution.getRandom(); // 返回 3
// getRandom() 应该随机返回 1、2 或 3 中的任意一个。每个元素被返回的概率应相等。
```

**约束条件**  
- 链表中的节点数在区间 `[1, 10^4]` 内。  
- `-10^4 <= Node.val <= 10^4`  
- 对 `getRandom` 的调用次数至多为 `10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把链表里的所有节点值先全部取出来，放进一个 **数组**（列表）里。  
- **数组**可以把每个节点的值顺序存储，类似于把所有商品装进一个箱子，想要取哪个商品，只要看箱子里的下标就行了。  
- 取随机节点时，只需要在 `[0, len(array)-1]` 之间随机生成一个下标，然后返回对应的值。

> **为什么正确？**  
> 只要每个下标被选中的概率相同（`1 / n`），对应的节点值自然也就等概率被选中了。  

**复杂度分析（大白话）**  
- **时间**：把链表遍历一遍放进数组需要 `O(n)`，每次 `getRandom` 只做一次随机下标查找是 `O(1)`，所以整体是 `O(n)`（一次性建表）+ `O(1)`（每次查询）。  
- **空间**：额外用了一个长度为 `n` 的数组，空间是 `O(n)`，也就是“和链表一样大的额外记忆”。

#### 代码（Python）

```python
import random
from typing import Optional

# 链表节点的定义（LeetCode 会自带，这里写出来方便运行）
class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


class Solution:
    def __init__(self, head: ListNode):
        """
        构造函数：把链表所有节点的值存进列表 self.arr
        """
        self.arr = []               # 用来装所有值的“箱子”
        cur = head
        while cur:                  # 一次遍历链表
            self.arr.append(cur.val)   # 把当前节点的值放进箱子
            cur = cur.next

    def getRandom(self) -> int:
        """
        随机返回一个节点的值
        """
        # random.randint(a, b) 会返回 [a, b] 之间的整数，等概率
        idx = random.randint(0, len(self.arr) - 1)   # 随机抽一个下标
        return self.arr[idx]                         # 返回对应的值
```

#### 复杂度

- **时间复杂度**：`O(n)`（构造时遍历一次链表）  
  - 这里的 `n` 就是链表的节点数。构造完以后每次 `getRandom` 只需要 `O(1)`，相当于“瞬间抽奖”。
- **空间复杂度**：`O(n)`（额外存了一个大小为 n 的数组）  
  - 需要额外的记忆来保存所有节点值，像把链表复制了一遍。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **空间**：如果链表很长（题目允许 `10⁴`），我们不想再额外占用同样大小的内存。  
我们需要一种 **在遍历一次链表的过程中就能直接抽奖** 的方法，这正是 **Reservoir Sampling（水塘抽样）** 的核心思想。

**水塘抽样**可以在一次遍历中，以等概率抽取第 `k` 个元素（这里 `k=1`）。  
思路可以用“抽签”来类比：

1. 第 1 个节点出现时，我们先把它放进“水塘”（即候选答案）。  
2. 当第 2 个节点出现时，我们掷一枚硬币（随机数），有 `1/2` 的概率把它换掉；否则保留原来的。  
3. 当第 3 个节点出现时，我们再掷硬币，有 `1/3` 的概率把它换掉……  
4. 第 `i` 个节点出现时，以概率 `1/i` 把它换进去，剩下的 `1 - 1/i` 保留原来的。

这样做的结果是：每个节点最终被保留下来的概率恰好是 `1/n`（等概率），而只用了 **常数级的额外空间**。

> **为什么正确？**  
> 归纳法可以证明：在遍历到第 `i` 个节点时，水塘里保存的节点是前 `i` 个节点中任意一个的概率都是 `1/i`。当遍历结束（`i = n`）时，概率自然变成 `1/n`。

**关键点**  
- 只需要一次遍历链表，不需要额外数组。  
- 每次 `getRandom` 都重新遍历链表一次，时间是 `O(n)`，但空间是 `O(1)`。  
- 对于本题的约束（最多 `10⁴` 次调用），这已经足够快。

#### 代码（Python）

```python
import random
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


class Solution:
    def __init__(self, head: ListNode):
        """
        只需要保存链表的头结点，后面每次抽奖都从这里开始遍历。
        """
        self.head = head

    def getRandom(self) -> int:
        """
        使用 Reservoir Sampling（水塘抽样）在一次遍历中等概率抽取节点值。
        """
        reservoir = None          # 候选答案，初始为空
        cur = self.head
        i = 0                     # 已经遍历过的节点数量

        while cur:
            i += 1                # 第 i 个节点到了
            # random.random() 返回 [0.0, 1.0) 的小数，< 1/i 的概率正好是 1/i
            if random.random() < 1 / i:
                reservoir = cur.val   # 以 1/i 的概率把当前值放进水塘
            cur = cur.next

        return reservoir
```

#### 复杂度

- **时间复杂度**：`O(n)`（每次 `getRandom` 需要遍历整个链表一次）  
  - 这里的 `n` 是链表长度。对每个节点只做了常数次操作，所以整体是线性时间。  
  - 与暴力解相比，**查询时间相同**，但我们省掉了事先的 `O(n)` 建表时间。

- **空间复杂度**：`O(1)`（只用了几个额外变量）  
  - 不再需要额外的数组，内存使用几乎不随链表长度增长。  
  - 这正是我们优化的核心：**常数空间**。

---

## 心得

- **核心技巧**：Reservoir Sampling（水塘抽样），一种在未知长度或太大数据流中实现等概率抽样的算法。  
- **适用题型**：
  1. 从数据流中随机抽取一个元素（LeetCode 382. 链表随机节点即本题）。  
  2. 从巨大的数组或文件中随机抽取 `k` 个元素（LeetCode 398. 随机数取样）。  
  3. 在线算法场景下，需要在单遍遍历中保持等概率抽样的统计任务。  
- **一句话总结解题钥匙**：**“遍历一次，保留候选，用 1/当前下标 的概率换掉它”。**

---

## 反思

- **第一反应**：先把链表全部存进数组再随机取值，想到“先把所有东西都装好再抽”，因为这最直观。  
- **最容易踩的坑**：
  - **概率写错**：`1/i` 必须是 **当前已遍历的节点数**，而不是总节点数，否则不等概率。  
  - **随机函数的使用**：`random.random() < 1/i` 与 `random.randint(1, i) == 1` 等价，任选其一即可，但要注意 `i` 为整数。  
  - **空链表**：题目保证至少有一个节点，但实际实现时仍需防止 `head` 为 `None` 的情况。  
- **下次类似题的第一步**：**先问自己“是否可以在一次遍历中直接抽样？”**，如果答案是“可以”，就立刻想到水塘抽样；如果不行，再考虑预处理（如构建数组）来换取查询速度。