# #1172. **餐盘栈** / Dinner Plate Stacks

> 难度：困难 · 标签：Hash Table、Stack、Design、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/dinner-plate-stacks/)

---

## 题目（英文原版）

**Description**

You have an infinite number of stacks arranged in a row and numbered (left to right) from 0, each of the stacks has the same maximum capacity.
Implement the DinnerPlates class:

**Examples**

**Example 1:**

```
Input
["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop", "pop"]
[[2], [1], [2], [3], [4], [5], [0], [20], [21], [0], [2], [], [], [], [], []]
Output
[null, null, null, null, null, null, 2, null, null, 20, 21, 5, 4, 3, 1, -1]

Explanation: 
DinnerPlates D = DinnerPlates(2);  // Initialize with capacity = 2
D.push(1);
D.push(2);
D.push(3);
D.push(4);
D.push(5);         // The stacks are now:  2  4
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.popAtStack(0);   // Returns 2.  The stacks are now:     4
                                                       1  3  5
                                                       ﹈ ﹈ ﹈
D.push(20);        // The stacks are now: 20  4
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.push(21);        // The stacks are now: 20  4 21
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.popAtStack(0);   // Returns 20.  The stacks are now:     4 21
                                                        1  3  5
                                                        ﹈ ﹈ ﹈
D.popAtStack(2);   // Returns 21.  The stacks are now:     4
                                                        1  3  5
                                                        ﹈ ﹈ ﹈ 
D.pop()            // Returns 5.  The stacks are now:      4
                                                        1  3 
                                                        ﹈ ﹈  
D.pop()            // Returns 4.  The stacks are now:   1  3 
                                                        ﹈ ﹈   
D.pop()            // Returns 3.  The stacks are now:   1 
                                                        ﹈   
D.pop()            // Returns 1.  There are no stacks.
D.pop()            // Returns -1.  There are still no stacks.
```

**Constraints**

- 1 <= capacity <= 2 * 104
- 1 <= val <= 2 * 104
- 0 <= index <= 105
- At most 2 * 105 calls will be made to push, pop, and popAtStack.

---

## 题目（中文翻译）

你有无限数量的栈（stack）排成一行，编号（从左到右）为 0、1、2 …，每个栈的容量（capacity）相同。请实现 `DinnerPlates` 类：

- `DinnerPlates(int capacity)`：使用给定的 `capacity` 初始化对象。
- `void push(int val)`：将 `val` 推入（push）左侧最近的、未满的栈中。如果所有已有的栈都已满，则在最右侧新建一个栈并将 `val` 放入其中。
- `int pop()`：从右侧最近的、非空的栈中弹出（pop）并返回栈顶元素。如果所有栈均为空，则返回 `-1`。
- `int popAtStack(int index)`：从编号为 `index` 的栈中弹出并返回栈顶元素。如果该栈为空，则返回 `-1`。

---

**示例**

```text
示例 1:
Input
["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop", "pop"]
[[2], [1], [2], [3], [4], [5], [0], [20], [21], [0], [2], [], [], [], [], []]
Output
[null, null, null, null, null, null, 2, null, null, 20, 21, 5, 4, 3, 1, -1]

Explanation: 
DinnerPlates D = DinnerPlates(2);  // 使用容量 = 2 初始化
D.push(1);    // 栈 0 -> [1]
D.push(2);    // 栈 0 -> [1,2]（已满）
D.push(3);    // 栈 1 -> [3]
D.push(4);    // 栈 1 -> [3,4]（已满）
D.push(5);    // 栈 2 -> [5]
D.popAtStack(0); // 从栈 0 弹出 2，返回 2
D.push(20);   // 栈 0 还有空间，放入 20 → 栈 0 -> [1,20]
D.push(21);   // 栈 3 -> [21]
D.popAtStack(0); // 从栈 0 弹出 20，返回 20
D.popAtStack(2); // 从栈 2 弹出 5，返回 5
D.pop();      // 从最右侧非空的栈弹出 21，返回 21
D.pop();      // 从栈 1 弹出 4，返回 4
D.pop();      // 从栈 1 弹出 3，返回 3
D.pop();      // 从栈 0 弹出 1，返回 1
D.pop();      // 所有栈均为空，返回 -1
```

---

**约束条件**

- `1 <= capacity <= 2 * 10^4`
- `1 <= val <= 2 * 10^4`
- `0 <= index <= 10^5`
- 最多会调用 `push`、`pop` 和 `popAtStack` 共计 `2 * 10^5` 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求模拟 **无限排排坐的盘子堆**（每个堆容量相同），并实现三个操作：

1. `push(val)` 把 `val` 放到最左边**还有空位**的堆里。  
2. `pop()` 弹出**最右边**非空堆的栈顶元素。  
3. `popAtStack(index)` 弹出第 `index` 个堆的栈顶元素（若该堆为空返回 `-1`）。  

最直接的想法就是 **把所有堆都存到一个 Python 列表 `stacks` 中**，每个堆本身用 `list`（当作栈）实现。  

- **`push`**：从左到右遍历 `stacks`，找到第一个长度 < `capacity` 的堆，直接 `append`。如果所有已有堆都满了，就在列表末尾新建一个堆再放入。  
- **`pop`**：从右到左遍历 `stacks`，找到第一个非空堆，`pop` 栈顶。弹完后如果该堆变空且它是最右边的堆，就把它从 `stacks` 删除（以免列表无限增长）。  
- **`popAtStack(index)`**：直接检查 `index` 是否在 `stacks` 范围内且对应堆非空，若是则 `pop`，否则返回 `-1`。  

> **类比**：`stacks` 就像一本“堆的目录”，每一页（`list`）记录该堆里放了哪些盘子。遍历目录找空位或找最后一本有内容的页，就是我们平时在图书馆找书的过程——最笨但最直观。

**为什么正确**：我们每一次都严格按照题目定义的“左边最近的空位”或“右边最近的非空堆”进行搜索，所以答案必然符合要求。  

**时间/空间复杂度**（大白话）：

- `push` 最坏要遍历所有堆，堆的数量记作 `m`，所以 **O(m)**。  
- `pop` 也需要从右往左遍历，最坏 **O(m)**。  
- `popAtStack` 直接定位到 `index`，只要检查是否空即可，**O(1)**。  
- 空间上我们要存每个盘子，盘子总数记作 `n`，所以 **O(n)**（加上一点额外的列表指针）。  

当调用次数达到 `2·10⁵`，而堆的数量 `m` 可能也接近 `10⁵`，**O(m)** 的线性搜索会导致超时。

#### 代码（Python）

```python
class DinnerPlates:
    def __init__(self, capacity: int):
        self.capacity = capacity          # 每个堆最多放 capacity 个盘子
        self.stacks = []                  # 用 list 保存所有堆，每个堆本身也是 list

    # 把 val 放到最左边还有空位的堆
    def push(self, val: int) -> None:
        # 从左到右找第一个没有满的堆
        for stack in self.stacks:
            if len(stack) < self.capacity:   # 还有空位
                stack.append(val)
                return
        # 所有已有堆都满了，创建新堆
        self.stacks.append([val])

    # 弹出最右边非空堆的栈顶元素
    def pop(self) -> int:
        # 从右往左找第一个非空堆
        while self.stacks:
            stack = self.stacks[-1]
            if stack:                         # 非空
                return stack.pop()
            else:                             # 空堆，直接删除，防止列表无限增长
                self.stacks.pop()
        return -1

    # 弹出第 index 个堆的栈顶元素
    def popAtStack(self, index: int) -> int:
        if 0 <= index < len(self.stacks) and self.stacks[index]:
            return self.stacks[index].pop()
        return -1
```

#### 复杂度  

- **时间复杂度**  
  - `push`：最坏 **O(m)**（遍历所有堆）  
  - `pop`：最坏 **O(m)**（遍历所有堆）  
  - `popAtStack`：**O(1)**（直接定位）  
  解释：`m` 代表当前已创建的堆的数量。线性遍历在数据规模大时会很慢。  

- **空间复杂度**：**O(n)**，`n` 为所有压入的盘子总数。我们只保存每个盘子一次，没有额外的结构。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈在于每次都要线性扫描堆**。  
要把这一步降到对数甚至常数级，需要一种**能快速定位左侧空位堆**和**右侧非空堆**的数据结构。

**关键观察**：

1. **左侧空位堆**：只要记录所有**还有空位的堆的下标**，每次 `push` 只取最小的下标即可。  
2. **右侧非空堆**：只要记录所有**非空堆的下标**，每次 `pop` 只取最大的下标即可。  

这正好可以用 **小根堆（min‑heap）** 保存左侧空位的下标，用 **大根堆（max‑heap）**（或者把负数放进小根堆）保存右侧非空堆的下标。  

**具体实现**：

- `stacks`：仍然是 `list`，下标对应堆。  
- `min_heap`（左侧空位堆）：存所有 **还有空位** 的堆下标。  
  - 当某堆从 **满** 变成 **未满**（`popAtStack` 或 `pop`），把它的下标加入 `min_heap`。  
  - 当某堆被 **填满**（`push` 后达到 `capacity`），我们不必立刻删除它的下标，只在取堆时**懒删**（如果堆已满就弹出堆顶继续）。  
- `max_heap`（右侧非空堆）：存所有 **非空** 的堆下标（存负数以实现最大堆）。  
  - 当某堆从 **空** 变成 **非空**（`push`），把它的下标加入 `max_heap`。  
  - 当某堆被 **弹空**（`pop` 或 `popAtStack`），同样**懒删**：取堆顶时若对应堆已空就继续弹出。  

**懒删除**的思想：堆里可能会残留已经失效的下标（例如一个堆已经满了，但它的下标仍在 `min_heap`），我们在真正使用堆顶时检查一下，如果失效就把它弹掉，直到找到合法的下标。这避免了在每次状态变化时去遍历整个堆去删元素，保持 `O(log m)` 的时间。

**操作细节**：

- `push(val)`  
  1. 通过 `while min_heap` 且对应堆已满，弹出无效下标。  
  2. 若 `min_heap` 为空，说明所有已有堆都满了，直接在 `stacks` 末尾新建堆（下标 = `len(stacks)`）。  
  3. 把 `val` 放进该堆。  
  4. 若堆刚满（`len == capacity`），不必再把它放进 `min_heap`（下次会被懒删）。  
  5. 把该堆的下标加入 `max_heap`（因为它现在肯定非空）。  

- `pop()`  
  1. 通过 `while max_heap` 且对应堆为空，弹出无效下标。  
  2. 若 `max_heap` 为空，返回 `-1`（所有堆都空）。  
  3. 取堆顶下标 `i`，弹出 `stacks[i].pop()`。  
  4. 若弹出后堆不再满，将 `i` 加入 `min_heap`（它变成了有空位的堆）。  
  5. 若弹出后堆仍非空，`max_heap` 中的 `i` 已经在（但可能已被懒删），不必额外处理。  

- `popAtStack(index)`  
  1. 若 `index` 超出 `stacks` 范围或对应堆为空，返回 `-1`。  
  2. 否则弹出该堆的栈顶。  
  3. 同 `pop()`，弹后若堆不满就加入 `min_heap`，若堆为空则不必手动删除 `max_heap`（懒删即可）。  

**为什么对数时间**：  
- 堆的插入、弹出都是 `O(log m)`。  
- 其余的列表操作都是 `O(1)`。  
- 因此每个接口的最坏时间都是 `O(log m)`，在 `2·10⁵` 次调用内完全可以接受。

#### 代码（Python）

```python
import heapq

class DinnerPlates:
    def __init__(self, capacity: int):
        self.capacity = capacity          # 每个堆的最大容量
        self.stacks = []                  # 存放所有堆，stack[i] 是第 i 个堆
        self.min_heap = []                # 保存“还有空位的堆”的下标（小根堆）
        self.max_heap = []                # 保存“非空堆”的下标（存负数实现大根堆）

    # 把 val 放到最左边还有空位的堆
    def push(self, val: int) -> None:
        # 1️⃣ 找到合法的左侧空位堆
        while self.min_heap:
            i = self.min_heap[0]               # 取最小下标
            if i < len(self.stacks) and len(self.stacks[i]) < self.capacity:
                break                         # 这个堆真的还有空位
            heapq.heappop(self.min_heap)      # 否则弹掉失效的下标

        # 2️⃣ 若没有可用的堆，则新建一个堆
        if not self.min_heap:
            i = len(self.stacks)               # 新堆的下标就是当前长度
            self.stacks.append([])             # 创建空堆
        else:
            i = heapq.heappop(self.min_heap)   # 取出合法的下标

        # 3️⃣ 把值放进去
        self.stacks[i].append(val)

        # 4️⃣ 更新两个堆的状态
        if len(self.stacks[i]) < self.capacity:      # 仍有空位，放回 min_heap
            heapq.heappush(self.min_heap, i)

        # 只要栈不为空，就一定是“非空堆”，放入 max_heap（负数实现最大堆）
        heapq.heappush(self.max_heap, -i)

    # 弹出最右边非空堆的栈顶元素
    def pop(self) -> int:
        # 1️⃣ 找到合法的右侧非空堆
        while self.max_heap:
            i = -self.max_heap[0]               # 取最大下标（负数转正）
            if i < len(self.stacks) and self.stacks[i]:
                break                         # 这个堆真的非空
            heapq.heappop(self.max_heap)      # 否则弹掉失效的下标

        if not self.max_heap:
            return -1                          # 所有堆都是空的

        i = -heapq.heappop(self.max_heap)      # 真正弹出该堆的下标
        val = self.stacks[i].pop()             # 弹出栈顶

        # 2️⃣ 更新状态
        if len(self.stacks[i]) == self.capacity - 1:
            # 刚从满变成有空位，加入 min_heap
            heapq.heappush(self.min_heap, i)

        if self.stacks[i]:                     # 仍然非空，重新放回 max_heap
            heapq.heappush(self.max_heap, -i)

        return val

    # 弹出第 index 个堆的栈顶元素
    def popAtStack(self, index: int) -> int:
        if index >= len(self.stacks) or not self.stacks[index]:
            return -1

        val = self.stacks[index].pop()

        # 该堆弹出后若不再满，说明出现了空位
        if len(self.stacks[index]) < self.capacity:
            heapq.heappush(self.min_heap, index)

        # 如果弹完后堆仍非空，max_heap 中会在后续的 pop() 中懒删；若空了，就等下次 lazy‑delete。
        return val
```

#### 复杂度  

- **时间复杂度**  
  - `push`：`O(log m)`（堆的插入/弹出）  
  - `pop`：`O(log m)`（堆的弹出与可能的重新插入）  
  - `popAtStack`：`O(log m)`（只涉及一次 `min_heap` 插入）  
  解释：`m` 为当前已创建的堆的数量。对数时间意味着即使 `m` 达到几万次操作也非常快。  

- **空间复杂度**：`O(n + m)`  
  - `n` 为所有压入的盘子数量（我们必须保存它们）。  
  - `m` 为堆的数量（对应的下标会被放进两个堆中），额外的空间是 `O(m)`，远小于 `n`。  

与暴力解相比，时间从 **线性** 降到了 **对数**，大幅提升了执行效率。

---

## 心得  

- **核心技巧**：**用堆（优先队列）维护“左侧最近空位”与“右侧最近非空”**，配合**懒删除**避免频繁的线性遍历。  
- **适用的题型**：  
  1. 需要**快速定位最左/最右满足条件的下标**（如 “Design Parking System”、 “Find the Kth Smallest Sum of a Matrix”）。  
  2. **动态维护可用资源集合**（如 “Design Hit Counter”、 “All O`one Data Structure”）。  
- **一句话总结**：**把“最近的空位/非空位”抽象成两个堆，所有操作只在堆上做 `log` 级别的更新**。

---

## 反思  

- **第一反应**：直接用列表模拟所有堆，暴力遍历寻找左/右位置。  
- **最容易踩的坑**：  
  - **堆的失效下标**：忘记在取堆顶时检查是否仍然满足“空位/非空”条件，会导致错误结果。  
  - **边界条件**：当所有堆都满时需要新建堆；弹空后堆的下标仍可能残留在 `max_heap` 中，需要懒删除。  
  - **容量为 0**（题目不允许，但防御性代码要考虑）。  
- **下次类似题**：**先思考“哪个属性需要快速定位”，把它抽象成优先队列或有序集合，再用懒删除保持结构简洁**。