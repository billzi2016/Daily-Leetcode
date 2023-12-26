# #2526. 从数据流中找出连续整数 / Find Consecutive Integers from a Data Stream

> 难度：中等 · 标签：Hash Table、Design、Queue、Counting、Data Stream · [LeetCode 链接](https://leetcode.com/problems/find-consecutive-integers-from-a-data-stream/)

---

## 题目（英文原版）

**Description**

For a stream of integers, implement a data structure that checks if the last k integers parsed in the stream are equal to value.
Implement the DataStream class:

**Examples**

**Example 1:**

```
Input
["DataStream", "consec", "consec", "consec", "consec"]
[[4, 3], [4], [4], [4], [3]]
Output
[null, false, false, true, false]

Explanation
DataStream dataStream = new DataStream(4, 3); //value = 4, k = 3 
dataStream.consec(4); // Only 1 integer is parsed, so returns False. 
dataStream.consec(4); // Only 2 integers are parsed.
                      // Since 2 is less than k, returns False. 
dataStream.consec(4); // The 3 integers parsed are all equal to value, so returns True. 
dataStream.consec(3); // The last k integers parsed in the stream are [4,4,3].
                      // Since 3 is not equal to value, it returns False.
```

**Constraints**

- 1 <= value, num <= 109
- 1 <= k <= 105
- At most 105 calls will be made to consec.

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数据流，实现一个数据结构，用于判断最近解析的 **k** 个整数是否全部等于给定的 **value**。

实现 **DataStream** 类（class）：

- `DataStream(int value, int k)`：构造函数，初始化目标整数 **value** 与窗口大小 **k**。  
- `bool consec(int num)`：向数据流中添加整数 **num**，并返回最近的 **k** 个整数（包括当前加入的 **num**）是否全部等于 **value**。如果已解析的整数少于 **k**，始终返回 `false`。

**示例**  

```text
输入
["DataStream", "consec", "consec", "consec", "consec"]
[[4, 3], [4], [4], [4], [3]]
输出
[null, false, false, true, false]
```

**解释**  
```java
DataStream dataStream = new DataStream(4, 3); // value = 4, k = 3
dataStream.consec(4); // 仅解析了 1 个整数，返回 false
dataStream.consec(4); // 仅解析了 2 个整数，仍少于 k，返回 false
dataStream.consec(4); // 现在最近的 3 个整数均为 4，返回 true
dataStream.consec(3); // 最近的 3 个整数为 [4,4,3]，不全等于 4，返回 false
```

**约束条件**  

- `1 <= value, num <= 10^9`
- `1 <= k <= 10^5`
- 最多调用 `consec` 方法 `10^5` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每次出现的整数全部记下来**，等到要判断时，直接去看最近的 `k` 个数是不是全部等于 `value`。  

- **使用的数据结构**：普通的 Python `list`（相当于一本顺序的“记录本”，把每个数字依次写进去）。  
- **为什么正确**：因为我们把所有出现的数字都保存了，随时可以把“最近的 k 条记录”拿出来比对，只要全部相等就返回 `True`，否则返回 `False`。  
- **复杂度分析**：  
  - **时间**：每调用一次 `consec`，我们都要检查最近的 `k` 条记录。检查一次要遍历 `k` 个元素，时间是 **O(k)**。如果一共调用 `n` 次（`n ≤ 10⁵`），最坏情况是 `n·k`，这在 `k` 也可能是 `10⁵` 时会变成 `10¹⁰`，根本跑不完。  
  - **空间**：我们把所有出现的数字都存下来，最多会有 `n` 条记录，空间是 **O(n)**。  

> **大白话**：  
> - `O(k)` 就像说“每次都要跑 `k` 步”。如果 `k` 很大，这一步会很慢。  
> - `O(n)` 就是“我们要记住所有走过的路”。如果走了很多次（`n` 很大），记忆会占很多空间。

#### 代码（Python）

```python
from typing import List

class DataStream:
    def __init__(self, value: int, k: int):
        self.value = value          # 要匹配的目标值
        self.k = k                  # 连续的长度要求
        self.history: List[int] = []  # 记录所有出现的整数

    def consec(self, num: int) -> bool:
        # 把新来的数字放进记录本
        self.history.append(num)          # O(1)

        # 如果记录本还没满 k，直接返回 False
        if len(self.history) < self.k:
            return False

        # 取出最近的 k 条记录，逐个检查是否都等于 value
        for i in range(1, self.k + 1):    # 最多遍历 k 次 → O(k)
            if self.history[-i] != self.value:
                return False
        return True
```

#### 复杂度

- **时间复杂度**：`O(k)`  
  每次调用都要遍历最近的 `k` 条记录，等价于“跑 `k` 步”。  
- **空间复杂度**：`O(n)`  
  需要保存所有已经出现的整数，最坏情况下会存 `n` 条数据。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要遍历 `k` 条记录**。我们需要把这一步压到 **O(1)**（常数时间）：

1. **只关心最近的 k 条**，更老的数字根本不影响答案。  
   → 用「队列」这种「只保留最近的」数据结构，满了就把最旧的踢出去。  
   （在 Python 里用 `collections.deque`，它像一条排队的长龙，左边进左边出，右边进右边出，都是 O(1)。）

2. **只要知道这 k 条里有多少个等于 `value`**，就能判断是否全部相等。  
   → 维护一个计数器 `cnt_eq`，每加入一个新数字如果等于 `value` 就 `+1`，如果踢出一个旧数字且它等于 `value` 就 `-1`。  

3. **什么时候返回 True**？  
   - 队列已经满了（长度恰好是 `k`），并且 `cnt_eq == k`（说明这 k 条全都是 `value`）。

这样，每次 `consec` 只做 **常数次** 的操作：加入、可能弹出、更新计数器、检查条件。时间 **O(1)**，空间只保存最多 `k` 条数字，**O(k)**。

> **类比**：  
> - `deque` 就像超市的收银队列，只保留最近的 `k` 位顾客，最早进来的顾客会被叫走。  
> - `cnt_eq` 像是「统计站」的计数器，实时记录队列里有多少位是想要的「VIP」顾客（value）。

#### 代码（Python）

```python
from collections import deque

class DataStream:
    def __init__(self, value: int, k: int):
        self.value = value          # 目标值
        self.k = k                  # 连续长度要求
        self.q = deque()            # 保存最近的最多 k 条数字
        self.cnt_eq = 0             # 队列里等于 value 的个数

    def consec(self, num: int) -> bool:
        # ① 把新数字加入队列
        self.q.append(num)                       # O(1)
        if num == self.value:
            self.cnt_eq += 1                     # 计数器加一

        # ② 如果队列长度超过 k，弹出最左边的老数字
        if len(self.q) > self.k:
            left = self.q.popleft()               # O(1)
            if left == self.value:
                self.cnt_eq -= 1                  # 计数器减一

        # ③ 检查是否已经满 k 且全部等于 value
        #    - len(self.q) == self.k 表示已经收集了 k 条
        #    - self.cnt_eq == self.k 表示这 k 条全是目标值
        return len(self.q) == self.k and self.cnt_eq == self.k
```

#### 复杂度

- **时间复杂度**：`O(1)`  
  每次调用只做几次常数时间的入队、出队、计数更新和比较，和 `k` 大小无关。比暴力的 `O(k)` 快很多。

- **空间复杂度**：`O(k)`  
  只保存最近的 `k` 条数字，最坏情况下占用 `k` 个位置。相比暴力的 `O(n)`，省了很多内存。

---

## 心得

- **核心技巧**：**滑动窗口 + 计数器**  
  用固定长度的窗口（这里用队列实现）只关注最近的 `k` 条数据，实时维护窗口内部满足条件的数量。

- **适用的题型**  
  1. 「找连续子数组/子串满足某种计数条件」——如 LeetCode 992. **K‑th Smallest in a Stream**（计数滑动窗口）  
  2. 「固定窗口内的最大/最小」——如 239. **Sliding Window Maximum**（单调队列）  
  3. 「流式数据连续出现次数」——如 1812. **Determine Color of a Chessboard Square**（记录最近状态）

- **一句话总结**：**把“只看最近 k 条”用队列实现，配合一个等于目标值的计数器，所有操作都能在常数时间完成。**

---

## 反思

- **拿到题目第一反应**：  
  “先把所有数字记下来，然后每次检查最近的 k 条”。这就是暴力解的雏形。

- **最容易踩的坑**  
  1. **忘记限制队列长度**：如果不在超过 `k` 时弹出老元素，计数器会一直累加，导致错误的判断。  
  2. **边界条件**：当总元素数少于 `k` 时，答案一定是 `False`，需要显式判断。  
  3. **计数器同步**：弹出元素时忘记如果它是 `value` 也要把计数器减一。

- **下次遇到同类题，第一步该想到**：  
  “这道题只关心最近的固定长度窗口吗？如果是，先考虑用 **队列/双指针** 实现滑动窗口，再思考在窗口内部需要维护的统计信息（计数、最大值、最小值等）”。这样可以快速把时间复杂度从 `O(k·n)` 降到 `O(n)` 或 `O(1)`。