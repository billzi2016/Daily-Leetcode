# #284. 可窥视迭代器 / Peeking Iterator

> 难度：中等 · 标签：Array、Design、Iterator · [LeetCode 链接](https://leetcode.com/problems/peeking-iterator/)

---

## 题目（英文原版）

**Description**

Design an iterator that supports the peek operation on an existing iterator in addition to the hasNext and the next operations.
Implement the PeekingIterator class:
Note: Each language may have a different implementation of the constructor and Iterator, but they all support the int next() and boolean hasNext() functions.

**Examples**

**Example 1:**

```
Input
["PeekingIterator", "next", "peek", "next", "next", "hasNext"]
[[[1, 2, 3]], [], [], [], [], []]
Output
[null, 1, 2, 2, 3, false]

Explanation
PeekingIterator peekingIterator = new PeekingIterator([1, 2, 3]); // [1,2,3]
peekingIterator.next();    // return 1, the pointer moves to the next element [1,2,3].
peekingIterator.peek();    // return 2, the pointer does not move [1,2,3].
peekingIterator.next();    // return 2, the pointer moves to the next element [1,2,3]
peekingIterator.next();    // return 3, the pointer moves to the next element [1,2,3]
peekingIterator.hasNext(); // return False
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- All the calls to next and peek are valid.
- At most 1000 calls will be made to next, hasNext, and peek.

---

## 题目（中文翻译）

设计一个迭代器（iterator），在原有的 `hasNext` 与 `next` 操作之外，额外支持 **窥视**（peek）操作。

实现 `PeekingIterator` 类：

> 注意：不同语言的构造函数（constructor）和迭代器实现可能不同，但均提供 `int next()` 与 `boolean hasNext()` 方法。

### 示例

**示例 1**

```json
Input
["PeekingIterator", "next", "peek", "next", "next", "hasNext"]
[[[1, 2, 3]], [], [], [], [], []]

Output
[null, 1, 2, 2, 3, false]
```

**解释**

```java
PeekingIterator peekingIterator = new PeekingIterator([1, 2, 3]); // 初始化为 [1,2,3]
peekingIterator.next();    // 返回 1，指针移动到下一个元素
peekingIterator.peek();    // 返回 2，指针 **不** 移动
peekingIterator.next();    // 返回 2，指针移动到下一个元素
peekingIterator.next();    // 返回 3，指针移动到下一个元素
peekingIterator.hasNext(); // 返回 false
```

### 约束条件

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`
- 所有对 `next` 与 `peek` 的调用都是合法的
- 最多会调用 `next`、`hasNext`、`peek` 共计 1000 次

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **原始迭代器** 里的所有元素一次性全部取出来，放进一个普通的 Python `list`，然后自己用下标来模拟 `next()`、`hasNext()` 与 `peek()` 的行为。  
- `list` 就像一本“装满数字的书”，我们可以随时翻到任意页码（下标）查看内容。  
- `next()` → 返回当前下标对应的元素并把下标往后移一位。  
- `hasNext()` → 看看下标是否已经跑到 `len(list)` 之外。  
- `peek()` → 只返回当前下标对应的元素 **但不移动下标**，相当于“把手指停在这页上先看一眼”。  

这种做法一定能得到正确答案，因为我们把所有数据都保存在了自己的容器里，随时都能直接访问。

#### 代码（Python）

```python
from typing import List

class PeekingIterator:
    def __init__(self, nums: List[int]):
        """
        把原始迭代器的所有元素一次性读进列表 self.data
        """
        self.data = list(nums)          # 把迭代器“装进书本”
        self.idx = 0                    # 当前指针，指向下一个要返回的元素

    def next(self) -> int:
        """
        返回当前元素并把指针右移一格
        """
        val = self.data[self.idx]       # 取出当前页的数字
        self.idx += 1                   # 手指向后移动
        return val

    def hasNext(self) -> bool:
        """
        判断指针是否已经越界
        """
        return self.idx < len(self.data)

    def peek(self) -> int:
        """
        只看当前元素，不移动指针
        """
        return self.data[self.idx]      # 直接返回当前页的数字
```

#### 复杂度  

- **时间复杂度**：  
  - `__init__` 需要遍历所有 `n` 个元素一次 → **O(n)**。  
  - `next`、`hasNext`、`peek` 都是 **O(1)**（只做常数次下标访问）。  
- **空间复杂度**：  
  - 额外用了一个长度为 `n` 的列表来存所有元素 → **O(n)**。  
  - 用“大白话”说就是：我们把原来的“盒子”里的东西全部搬进了自己的“大箱子”，所以占用了线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **空间**：我们把所有元素都保存下来，虽然实现简单，但不符合“迭代器本身只应该占用 O(1) 额外空间”的设计初衷。  
要优化，就要 **只在需要时保存下一个元素**，而不是一次性全部保存。  

关键观察：

1. `peek()` 只需要“提前看到”下一个元素，而 `next()` 需要把这个元素真正取出来。  
2. 原始迭代器本身已经提供了 `next()` 与 `hasNext()`，我们可以把它当成“黑盒子”，只在 **第一次调用 `peek()` 或 `next()` 前** 把下一个值缓存起来。  

实现细节：

- 用一个变量 `self._next` 保存**已缓存的下一个值**。如果这个变量为 `None`，说明缓存还没准备好，需要从原始迭代器里取一个出来。  
- `hasNext()` 的实现要同时检查两件事：  
  1. 缓存里已经有值 (`self._next is not None`) → 肯定还有下一个。  
  2. 否则，尝试让原始迭代器 `hasNext()` 再次检查。  
- `peek()`：如果缓存为空，就先把原始迭代器的下一个元素取出来放进缓存，然后直接返回缓存。  
- `next()`：如果缓存已经有值，直接弹出（并清空缓存），否则直接调用原始迭代器的 `next()`。

这样我们只用了 **一个额外的变量** 来保存“下一个”元素，空间降到 **O(1)**，每个操作仍然是常数时间。

> 类比：把原始迭代器想象成一条流水线，`peek()` 就是站在流水线前面先把下一件产品挑出来放进手里（不让它继续前进），`next()` 则是把手里的产品交给顾客（并让流水线继续前进）。

#### 代码（Python）

```python
from typing import Iterator

class PeekingIterator:
    """
    只用一个变量 _next 缓存“下一元素”，实现 O(1) 额外空间的迭代器。
    """

    def __init__(self, iterator: Iterator[int]):
        """
        参数 iterator 本身已经实现了 next() 与 hasNext()（这里用 Python 的迭代器协议）。
        """
        self._it = iterator          # 原始迭代器（像一条生产线）
        self._next = None            # 缓存的下一个元素，初始为空

    def _fill(self):
        """
        私有方法：如果缓存为空且还有元素，取出下一个放进缓存。
        """
        if self._next is None:
            try:
                self._next = next(self._it)   # 取出下一件产品放进手里
            except StopIteration:
                self._next = None            # 已经没有产品了

    def peek(self) -> int:
        """
        只看下一个元素但不移动指针。
        """
        self._fill()                # 确保缓存已准备好
        return self._next           # 直接返回手里的产品

    def next(self) -> int:
        """
        返回下一个元素并让指针前进。
        """
        self._fill()                # 若缓存为空则先取出来
        val = self._next            # 取出手里的产品
        self._next = None           # 手里清空，准备下次缓存
        return val

    def hasNext(self) -> bool:
        """
        判断是否还有剩余元素。
        """
        self._fill()                # 只要缓存有值，就说明还有元素
        return self._next is not None
```

> **说明**：在 Python 中，普通的迭代器只提供 `__next__()`（即 `next()`）和 `StopIteration`，没有显式的 `hasNext()`。这里的实现把 `hasNext()` 用 `try/except` 包装成了缓存逻辑，效果等价。

#### 复杂度  

- **时间复杂度**：  
  - `peek()`、`next()`、`hasNext()` 每次最多只调用一次原始迭代器的 `next()`，其余操作都是常数时间 → **O(1)**。  
  - 与暴力解相比，**每次操作的时间都保持不变**，而不需要遍历整个列表。  
- **空间复杂度**：  
  - 只用了一个额外的变量 `self._next` → **O(1)**（常数空间）。  
  - 用通俗的话说，就是我们只在手里抓着 **一件** 产品，而不是把整条流水线的所有产品都搬进仓库。

---

## 心得

- **核心技巧**：**提前缓存（look‑ahead）**，即在需要“预览”下一个元素时，把它暂存一份，而不是一次性全部保存。  
- **适用的题型**  
  1. **Peeking Iterator**（本题）  
  2. **实现带有 `next` 与 `prev` 的双向迭代器**（需要在前后缓存）  
  3. **滑动窗口类题目**（如求子数组最大和，需要在窗口外预取一个元素）  
- **一句话总结解题钥匙**：*只在需要时缓存下一个值，别把所有数据一次性搬走*。

---

## 反思

- **拿到题目第一反应**：把原始迭代器的内容全部装进列表，直接用下标模拟 `peek`。这是一种“先把所有东西搬到手边再操作”的直觉。  
- **最容易踩的坑**  
  - **缓存未及时更新**：连续调用 `peek()` 多次，如果不把缓存保持不变，会导致每次都向底层迭代器前进，破坏指针位置。  
  - **边界条件**：当迭代器已经耗尽时，`peek()` 或 `next()` 仍会被调用（题目保证不会出现非法调用，但实现时仍需防止 `StopIteration` 导致异常）。  
  - **一次性读取导致 O(n) 空间**：在数据规模很大时，暴力解会占用太多内存。  
- **下次遇到同类题，第一步该想到**：**“我只需要看下一项而已，能否只保存一份而不是全部？”**——即先判断是否可以用**单个缓存变量**实现“前瞻”。