# #1670. **设计前中后队列** / Design Front Middle Back Queue

> 难度：中等 · 标签：Array、Linked List、Design、Queue、Data Stream · [LeetCode 链接](https://leetcode.com/problems/design-front-middle-back-queue/)

---

## 题目（英文原版）

**Description**

Design a queue that supports push and pop operations in the front, middle, and back.
Implement the FrontMiddleBack class:
Notice that when there are two middle position choices, the operation is performed on the frontmost middle position choice. For example:

**Examples**

**Example 1:**

```
Input:
["FrontMiddleBackQueue", "pushFront", "pushBack", "pushMiddle", "pushMiddle", "popFront", "popMiddle", "popMiddle", "popBack", "popFront"]
[[], [1], [2], [3], [4], [], [], [], [], []]
Output:
[null, null, null, null, null, 1, 3, 4, 2, -1]

Explanation:
FrontMiddleBackQueue q = new FrontMiddleBackQueue();
q.pushFront(1);   // [1]
q.pushBack(2);    // [1, 2]
q.pushMiddle(3);  // [1, 3, 2]
q.pushMiddle(4);  // [1, 4, 3, 2]
q.popFront();     // return 1 -> [4, 3, 2]
q.popMiddle();    // return 3 -> [4, 2]
q.popMiddle();    // return 4 -> [2]
q.popBack();      // return 2 -> []
q.popFront();     // return -1 -> [] (The queue is empty)
```

**Constraints**

- 1 <= val <= 109
- At most 1000 calls will be made to pushFront, pushMiddle, pushBack, popFront, popMiddle, and popBack.

---

## 题目（中文翻译）

设计一个队列，使其能够在队首、队中和队尾分别进行插入（push）和删除（pop）操作。

实现 `FrontMiddleBackQueue` 类，支持以下方法：

- `pushFront(int val)`：将 `val` 插入到队列的最前端。
- `pushMiddle(int val)`：将 `val` 插入到队列的中间位置。如果当前队列长度为偶数，则有两个中间位置，选取**更靠前的**中间位置进行插入。
- `pushBack(int val)`：将 `val` 插入到队列的末尾。
- `popFront()`：删除并返回队列的最前端元素。如果队列为空，返回 `-1`。
- `popMiddle()`：删除并返回队列的中间元素。如果当前队列长度为偶数，则有两个中间位置，选取**更靠前的**中间位置进行删除。如果队列为空，返回 `-1`。
- `popBack()`：删除并返回队列的末尾元素。如果队列为空，返回 `-1`。

**注意**：当队列长度为偶数时，中间位置有两个可选，所有涉及 “中间” 的操作均应作用于**更靠前的**那个位置。

### 示例

**示例 1：**

```text
Input:
["FrontMiddleBackQueue","pushFront","pushBack","pushMiddle","pushMiddle","popFront","popMiddle","popMiddle","popBack","popFront"]
[[],[1],[2],[3],[4],[],[],[],[],[]]

Output:
[null,null,null,null,null,1,3,4,2,-1]

Explanation:
FrontMiddleBackQueue q = new FrontMiddleBackQueue();
q.pushFront(1);   // 队列变为 [1]
q.pushBack(2);    // 队列变为 [1, 2]
q.pushMiddle(3);  // 队列变为 [1, 3, 2]
q.pushMiddle(4);  // 队列变为 [1, 4, 3, 2]
q.popFront();     // 返回 1，队列变为 [4, 3, 2]
q.popMiddle();    // 返回 3，队列变为 [4, 2]
q.popMiddle();    // 返回 4，队列变为 [2]
q.popBack();      // 返回 2，队列变为 []
q.popFront();     // 返回 -1，队列为空
```

### 约束条件

- `1 <= val <= 10^9`
- 最多会调用 `pushFront`、`pushMiddle`、`pushBack`、`popFront`、`popMiddle`、`popBack` 共计 **1000** 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把整个队列存到 **一个普通的 Python 列表**（`list`）里。  
- `pushFront` → 在列表最左侧插入元素，等价于 `list.insert(0, val)`。  
- `pushBack` → 在列表最右侧追加元素，等价于 `list.append(val)`。  
- `pushMiddle` → 先算出中间位置 `mid = len(lst)//2`（当长度为偶数时取左侧的中间），然后 `list.insert(mid, val)`。  
- `popFront` / `popBack` / `popMiddle` 同理，只是把对应位置的元素取出来并删除。  

> **类比**：把列表想象成一本线装书，`pushFront` 就是往书的封面前面塞一本新书，`pushBack` 是往书脊后面塞，`pushMiddle` 是把书拆开，在中间插入一本新书。  

**为什么正确**：  
所有操作都直接在列表上进行，列表本身已经保证了顺序不变。只要我们按照题目要求的“左侧中间”定位插入/删除，就一定得到正确的结果。  

**复杂度分析**（大白话解释）：

| 操作 | Python 列表内部实现 | 复杂度 |
|------|-------------------|--------|
| `pushFront`、`popFront`、`pushMiddle`、`popMiddle` | 需要把后面的元素整体向右/左移动，类似把一堆球往后推或往前拉 | **O(n)**，因为最坏情况下要搬动 `n` 个元素 |
| `pushBack`、`popBack` | 只在最右端动手，和搬动其他元素无关 | **O(1)**，常数时间 |

这里的 `n` 就是当前队列的长度。空间上，只用了一个列表来保存所有元素，**O(n)**。

#### 代码（Python）  
```python
class FrontMiddleBackQueue:
    def __init__(self):
        # 用一个普通列表保存所有元素
        self.q = []

    # ---------- 插入 ----------
    def pushFront(self, val: int) -> None:
        # 在最左侧插入
        self.q.insert(0, val)          # O(n)

    def pushBack(self, val: int) -> None:
        # 在最右侧追加
        self.q.append(val)             # O(1)

    def pushMiddle(self, val: int) -> None:
        # 计算左侧中间位置：len//2（偶数时取左边）
        mid = len(self.q) // 2
        self.q.insert(mid, val)        # O(n)

    # ---------- 删除 ----------
    def popFront(self) -> int:
        if not self.q:
            return -1
        return self.q.pop(0)           # O(n)

    def popBack(self) -> int:
        if not self.q:
            return -1
        return self.q.pop()            # O(1)

    def popMiddle(self) -> int:
        if not self.q:
            return -1
        # 左侧中间位置同样是 len//2
        mid = (len(self.q) - 1) // 2   # 当长度为偶数时取左侧
        return self.q.pop(mid)         # O(n)
```

#### 复杂度  
- **时间复杂度**  
  - `pushFront / popFront / pushMiddle / popMiddle`：**O(n)**，因为需要搬动列表中大量元素。  
  - `pushBack / popBack`：**O(1)**，只在列表尾部操作。  
- **空间复杂度**  
  - **O(n)**，保存所有元素的列表本身占用线性空间。  

> **大白话**：如果队列里有 1000 条数据，`pushMiddle` 最坏要搬动大约 500 条，这在 1000 次调用里还能接受，但如果调用次数很多或数据量更大，就会明显慢下来。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每次对中间或前端的插入/删除都要搬动大量元素**。我们需要一种数据结构，既能在两端快速操作，又能在中间“对半”快速取出。  

**关键点**：把整个队列**平分成两半**，分别用**双端队列**（`collections.deque`）保存。  
- `left` 保存前半段元素（左侧），`right` 保存后半段元素（右侧）。  
- 保持 **两段长度的平衡**：`len(left) == len(right)` 或 `len(left) == len(right) + 1`（左侧可以多一个元素），这样“左侧中间”总是位于 `left` 的最右端。  

这样，所有六个操作都可以在 **O(1)** 时间内完成，因为 `deque` 在两端的插入、删除都是常数时间。  

**具体操作**：

| 操作 | 具体实现 | 说明 |
|------|----------|------|
| `pushFront(val)` | `left.appendleft(val)`，随后 **平衡** 两段 | 把新元素直接放到左边最前面 |
| `pushBack(val)` | `right.append(val)`，随后 **平衡** | 把新元素放到右边最末尾 |
| `pushMiddle(val)` | `left.append(val)`（把它放到左段最右端），随后 **平衡** | 由于左侧可以多一个，所以直接把中间元素放到 `left` 的尾部 |
| `popFront()` | 若 `left` 非空则 `left.popleft()`，否则 `right.popleft()`，随后 **平衡** | 直接从左端弹出 |
| `popBack()` | 若 `right` 非空则 `right.pop()`，否则 `left.pop()`，随后 **平衡** | 直接从右端弹出 |
| `popMiddle()` | 若 `len(left) == len(right)`（偶数）则弹出 `left.pop()`，否则弹出 `left.pop()`（奇数时左侧多一个，仍弹左侧最右端） | 这正是“左侧中间”所在的位置 |

**平衡**（rebalance）规则：

```text
while len(left) > len(right) + 1:   # 左侧太长
    right.appendleft(left.pop())
while len(left) < len(right):       # 右侧比左侧多
    left.append(right.popleft())
```

每次插入或删除后，最多移动 **一个元素**，所以仍是 O(1)。  

**类比**：把队列想象成两条并排的传送带（左传送带、右传送带），我们随时保证左传送带不比右传送带短超过一格，这样中间的“入口”永远在左传送带的最右端，取东西只需要在对应的传送带上操作即可。

#### 代码（Python）  
```python
from collections import deque

class FrontMiddleBackQueue:
    def __init__(self):
        # left 保存前半段，right 保存后半段
        self.left = deque()   # 左侧：可以在两端 O(1) 操作
        self.right = deque()  # 右侧：同上

    # ---------- 维护平衡 ----------
    def _rebalance(self) -> None:
        """
        保证:
        len(left) == len(right)   或
        len(left) == len(right) + 1
        """
        # 左侧太长，移动最右边的元素到右侧最左边
        while len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        # 右侧比左侧多，移动右侧最左边的元素到左侧最右边
        while len(self.left) < len(self.right):
            self.left.append(self.right.popleft())

    # ---------- 插入 ----------
    def pushFront(self, val: int) -> None:
        # 把元素塞到左侧最前面
        self.left.appendleft(val)   # O(1)
        self._rebalance()           # 只会移动最多一个元素，仍是 O(1)

    def pushBack(self, val: int) -> None:
        # 把元素塞到右侧最末尾
        self.right.append(val)      # O(1)
        self._rebalance()

    def pushMiddle(self, val: int) -> None:
        # 中间位置对应左侧最右端
        self.left.append(val)       # O(1)
        self._rebalance()

    # ---------- 删除 ----------
    def popFront(self) -> int:
        if not self.left and not self.right:
            return -1
        if self.left:
            ans = self.left.popleft()
        else:               # left 为空时只能从 right 取
            ans = self.right.popleft()
        self._rebalance()
        return ans

    def popBack(self) -> int:
        if not self.left and not self.right:
            return -1
        if self.right:
            ans = self.right.pop()
        else:               # right 为空时只能从 left 取
            ans = self.left.pop()
        self._rebalance()
        return ans

    def popMiddle(self) -> int:
        if not self.left and not self.right:
            return -1
        # 无论奇偶，左侧的最右端都是“左侧中间”
        ans = self.left.pop()
        self._rebalance()
        return ans
```

#### 复杂度  
- **时间复杂度**：所有六个方法均为 **O(1)**。  
  - 解释：`deque` 在两端的插入、删除都是常数时间；`_rebalance` 最多移动 **一个** 元素，也属于常数时间。相比暴力解的 O(n)，这里的每一步都不随队列长度增长而变慢。  
- **空间复杂度**：**O(n)**，需要存放所有元素，只是把它们分布在两个 `deque` 中而已。  

> 与暴力解对比：当队列长度为 10⁵ 时，暴力解的 `pushMiddle` 可能要搬动 5×10⁴ 次，而最优解始终只搬动一次，性能提升非常明显。  

---  

## 心得  

- **核心技巧**：把一个需要“中间”操作的序列**均分**到两段，并用**双端队列**维护两段的平衡。  
- **适用的题型**  
  1. “中间插入/删除”类的设计题，如 **Design Front Middle Back Queue**（本题）  
  2. “保持中位数”类的数据结构（例如 **Median of Data Stream**）  
  3. “双端队列 + 平衡”实现的 **Sliding Window Median**、**Front Middle Back Queue** 的变体  
- **一句话总结**：**把序列拆成左右两块，左块多一格，就把“中间”锁在左块的最右端，所有操作都只在两端完成**。  

---  

## 反思  

- **第一反应**：直接用一个列表实现，想到 `insert` / `pop`，但忽略了搬动成本。  
- **最容易踩的坑**  
  - **平衡条件写错**：必须保证左侧长度≥右侧长度且差值≤1，否则“中间”位置会偏移。  
  - **空队列的边界**：`pop` 系列在两段都空时必须返回 `-1`，且不要忘记先检查 `left` 再检查 `right`。  
  - **奇偶长度的中间定位**：题目要求“左侧中间”，所以在偶数长度时仍取左侧最右端。  
- **下次类似题的第一步**：**思考是否可以把序列拆分成两块，使需要的“特殊位置”恰好落在两块的边界上**，这样往往可以把复杂的中间操作转化为两端的 O(1) 操作。