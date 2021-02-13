# #1206. 设计跳表 / Design Skiplist

> 难度：困难 · 标签：Linked List、Design · [LeetCode 链接](https://leetcode.com/problems/design-skiplist/)

---

## 题目（英文原版）

**Description**

Design a Skiplist without using any built-in libraries.
A skiplist is a data structure that takes O(log(n)) time to add, erase and search. Comparing with treap and red-black tree which has the same function and performance, the code length of Skiplist can be comparatively short and the idea behind Skiplists is just simple linked lists.
For example, we have a Skiplist containing [30,40,50,60,70,90] and we want to add 80 and 45 into it. The Skiplist works this way:
Artyom Kalinin [CC BY-SA 3.0], via Wikimedia Commons
You can see there are many layers in the Skiplist. Each layer is a sorted linked list. With the help of the top layers, add, erase and search can be faster than O(n). It can be proven that the average time complexity for each operation is O(log(n)) and space complexity is O(n).
See more about Skiplist: https://en.wikipedia.org/wiki/Skip_list
Implement the Skiplist class:
Note that duplicates may exist in the Skiplist, your code needs to handle this situation.

**Examples**

**Example 1:**

```
Input
["Skiplist", "add", "add", "add", "search", "add", "search", "erase", "erase", "search"]
[[], [1], [2], [3], [0], [4], [1], [0], [1], [1]]
Output
[null, null, null, null, false, null, true, false, true, false]

Explanation
Skiplist skiplist = new Skiplist();
skiplist.add(1);
skiplist.add(2);
skiplist.add(3);
skiplist.search(0); // return False
skiplist.add(4);
skiplist.search(1); // return True
skiplist.erase(0);  // return False, 0 is not in skiplist.
skiplist.erase(1);  // return True
skiplist.search(1); // return False, 1 has already been erased.
```

**Constraints**

- 0 <= num, target <= 2 * 104
- At most 5 * 104 calls will be made to search, add, and erase.

---

## 题目（中文翻译）

设计一个 **跳表（Skiplist）**，不使用任何内置库。  
跳表是一种数据结构，能够在添加、删除和搜索时达到 **O(log n)** 的时间复杂度。与具有相同功能和性能的 **Treap**、**红黑树（Red‑Black Tree）** 相比，跳表的代码量相对较少，其背后的思想仅仅是若干层有序链表（linked list）。

例如，已有一个包含 `[30,40,50,60,70,90]` 的跳表，我们想要插入 `80` 和 `45`。跳表的工作方式如下图所示：

![跳表示意图](https://upload.wikimedia.org/wikipedia/commons/6/6b/Skiplist_add.png)  
*图片来源：Artyom Kalinin，CC BY‑SA 3.0，via Wikimedia Commons*

可以看到，跳表由多层组成，每一层都是一个有序链表。借助上层的“快路径”，**添加（add）**、**删除（erase）** 和 **搜索（search）** 的时间复杂度可以优于 **O(n)**。理论上可以证明，每种操作的平均时间复杂度为 **O(log n)**，空间复杂度为 **O(n)**。

更多关于跳表的原理，请参考维基百科：https://en.wikipedia.org/wiki/Skip_list

实现 `Skiplist` 类时需注意：跳表中可能出现重复元素，代码必须能够正确处理这种情况。

---

## 示例

```json
["Skiplist", "add", "add", "add", "search", "add", "search", "erase", "erase", "search"]
[[], [1], [2], [3], [0], [4], [1], [0], [1], [1]]
```

**输出**

```json
[null, null, null, null, false, null, true, false, true, false]
```

**解释**

```java
Skiplist skiplist = new Skiplist();
skiplist.add(1);
skiplist.add(2);
skiplist.add(3);
skiplist.search(0); // 返回 false
skiplist.add(4);
skiplist.search(1); // 返回 true
... (已截断)
```

---

## 约束条件

- `0 <= num, target <= 2 * 10^4`
- 最多会有 `5 * 10^4` 次对 `search`、`add`、`erase` 的调用。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有数放在一个普通的 Python 列表里，保持 **有序**。  
- **数据结构**：有序列表（`list`），可以把它想象成一本排好序的电话号码簿。  
- **为什么正确**：因为题目只要求实现 `add`、`search`、`erase` 三个基本操作，只要我们在列表里把元素放对位置，查找时遍历或二分，就一定能得到正确答案。  
- **复杂度**：  
  - 插入时需要把新元素放到正确的位置，最坏要把后面的所有元素往后搬一次，时间是 **O(n)**（`n` 为当前元素个数）。  
  - 查找如果用线性遍历也是 **O(n)**，如果用二分查找是 **O(log n)**，但二分查找只能判断是否存在，真正的插入仍然要搬位，整体仍是 **O(n)**。  
  - 删除同样需要搬位，时间也是 **O(n)**。  
  - 额外空间只用来存放列表本身，和元素个数成正比，即 **O(n)**。

> **大白话**：`O(n)` 就像把一箱子 1000 本书从左到右排好序，你最多可能要检查（或者搬动）每一本书——也就是和书的数量成正比。

#### 代码（Python）

```python
import bisect

class Skiplist:
    def __init__(self):
        # 用一个有序列表保存所有数字，类似排好序的电话本
        self.data = []

    def search(self, target: int) -> bool:
        # 二分查找：bisect_left 返回第一个 >= target 的位置
        idx = bisect.bisect_left(self.data, target)
        # 检查该位置是否正好等于 target
        return idx < len(self.data) and self.data[idx] == target

    def add(self, num: int) -> None:
        # bisect.insort 在保持有序的前提下插入元素
        bisect.insort(self.data, num)

    def erase(self, num: int) -> bool:
        # 先二分定位，再删除；如果不存在返回 False
        idx = bisect.bisect_left(self.data, num)
        if idx < len(self.data) and self.data[idx] == num:
            self.data.pop(idx)          # 删除对应位置的元素
            return True
        return False
```

#### 复杂度

- **时间复杂度**：  
  - `search`：`O(log n)`（二分查找）  
  - `add`：`O(n)`（插入需要搬位）  
  - `erase`：`O(n)`（同样需要搬位）  
- **空间复杂度**：`O(n)`——只存放了 `n` 个整数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **搬位**：每次插入或删除都要把后面的元素整体向后/向前移动，导致线性时间。  
要把时间压到对数级，需要 **跳过** 大量不相关的元素，这正是 **Skiplist**（跳表）要做的事。

**核心思想**：  
- 把普通的单向链表想象成一条“慢车道”。  
- 在它之上再建几条“快车道”，每条快车道只保留一部分节点（类似高速公路的出入口），这样在查找时可以先在高层快速前进，跳过很多节点，再逐层下沉到最底层完成精确定位。  
- 每个节点在 **多少层** 上出现是随机决定的，常用的办法是 **掷硬币**：每掷一次正面就上升一层，直到出现反面或达到最大层数。这样每层的节点数大约是下一层的 **1/2**，整体期望高度是 `log₂ n`，从而保证 **平均 O(log n)** 的操作时间。

**关键数据结构**：  
- **节点 (Node)**：保存一个数值 `val`，以及一个列表 `forward`，`forward[i]` 指向该节点在第 `i` 层的下一个节点。可以把 `forward` 想象成“每层的指向下一站的指针”。  
- **头结点 (head)**：所有层的起点，`forward` 长度等于当前最高层数。  
- **最大层数 (MAX_LEVEL)**：为了防止层数无限增长，设一个上限（如 16），足以满足题目限制 (`num ≤ 2·10⁴`)。  

**实现步骤**  

1. **随机层数**：`random_level()` 用 1/2 的概率继续往上升，最多到 `MAX_LEVEL`。  
2. **搜索路径**：在 `search`、`add`、`erase` 时，都需要先从最高层向下遍历，记录每一层上**最后一个小于等于目标值的节点**（称为 `update[i]`），这一步相当于在每层“找最近的站”。  
3. **插入**：  
   - 先得到新节点的层数 `lvl`。  
   - 如果 `lvl` 超过当前层数，扩充 `head.forward`，并把新层的 `update` 都指向 `head`（相当于在最高层直接插入）。  
   - 对每层 `i < lvl`，把新节点插入到 `update[i]` 与其原来的 `forward[i]` 之间。  
4. **删除**：  
   - 同样先找到每层的 `update`。  
   - 如果在最底层找到了要删的节点，则把每层的指针都跳过它。  
   - 删除后如果最高层已经没有节点了，就把层数降下来，保持结构紧凑。  

> **类比**：想象你在一座多层的楼梯上找房间号。底层是每个房间都标记，走一层只能前进一个房间；而高层的指示牌只标记每 2、4、8… 个房间一次。找房间时，你先站在最高层的指示牌快速跳过去，发现已经超过目标后，就往下一层继续细分，最后在底层定位到具体房间。这样步数大大减少。

#### 代码（Python）

```python
import random

class Node:
    """跳表的节点，val 为保存的数值，forward[i] 为第 i 层的后继指针"""
    __slots__ = ('val', 'forward')
    def __init__(self, val: int, level: int):
        self.val = val
        # forward 长度等于层数，每个元素初始为 None（相当于指向空）
        self.forward = [None] * level

class Skiplist:
    MAX_LEVEL = 16          # 经验值，足够容纳 2*10^4 个元素
    P = 0.5                 # 抛硬币正面概率

    def __init__(self):
        # 头结点不存数值，只负责保存每层的入口
        self.head = Node(-1, Skiplist.MAX_LEVEL)
        self.level = 1       # 当前跳表的最高层数（至少有第 0 层）

    def _random_level(self) -> int:
        """随机生成节点层数，概率 1/2 上升一层，最多 MAX_LEVEL"""
        lvl = 1
        while random.random() < Skiplist.P and lvl < Skiplist.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        """从最高层向下查找，若找到返回 True，否则 False"""
        cur = self.head
        # 从最高层往下遍历
        for i in reversed(range(self.level)):
            # 在当前层前进，只要下一个节点的值小于 target
            while cur.forward[i] and cur.forward[i].val < target:
                cur = cur.forward[i]
        # 下降到第 0 层后，检查下一个节点是否正好等于 target
        cur = cur.forward[0]
        return cur is not None and cur.val == target

    def add(self, num: int) -> None:
        """插入一个新数，可能在多层出现"""
        update = [None] * Skiplist.MAX_LEVEL   # 保存每层的前驱节点
        cur = self.head

        # 与 search 类似，先找到每层的前驱节点
        for i in reversed(range(self.level)):
            while cur.forward[i] and cur.forward[i].val < num:
                cur = cur.forward[i]
            update[i] = cur   # 第 i 层最后一个小于 num 的节点

        # 产生新节点的层数
        lvl = self._random_level()
        if lvl > self.level:          # 若新层数超过当前层，需要扩充 head
            for i in range(self.level, lvl):
                update[i] = self.head
            self.level = lvl

        # 创建新节点并插入到每层
        new_node = Node(num, lvl)
        for i in range(lvl):
            new_node.forward[i] = update[i].forward[i]   # 新节点的后继指向原来的后继
            update[i].forward[i] = new_node              # 前驱的后继指向新节点

    def erase(self, num: int) -> bool:
        """删除一个数，若不存在返回 False"""
        update = [None] * Skiplist.MAX_LEVEL
        cur = self.head
        found = False

        # 同样先定位每层的前驱节点
        for i in reversed(range(self.level)):
            while cur.forward[i] and cur.forward[i].val < num:
                cur = cur.forward[i]
            update[i] = cur

        # 第 0 层的下一个节点才是可能要删的目标
        cur = cur.forward[0]
        if cur and cur.val == num:
            found = True
            # 在每一层把指针绕过要删除的节点
            for i in range(self.level):
                if update[i].forward[i] != cur:
                    break
                update[i].forward[i] = cur.forward[i]

            # 删除后检查是否需要降低层数（最高层可能已经没有节点了）
            while self.level > 1 and self.head.forward[self.level - 1] is None:
                self.level -= 1

        return found
```

#### 复杂度

- **时间复杂度**：  
  - `search`：`O(log n)` —— 只在每层前进一次，层数约为 `log₂ n`。  
  - `add`：`O(log n)` —— 找前驱的过程是 `O(log n)`，插入本身只改指针，层数也是 `log n`。  
  - `erase`：`O(log n)` —— 同理，需要先定位前驱，然后把指针跳过。  
  与暴力解相比，所有操作都从线性下降到对数级，速度快很多。

- **空间复杂度**：`O(n)` —— 每个元素平均会出现在 `1 / (1-P) = 2` 层（因为 `P=0.5`），总指针数约为 `2n`，仍然是线性空间。

---

## 心得

- **核心技巧**：利用多层链表（跳表）把“逐个检查”变成“先跨大段再细分”，实现 `O(log n)` 的查询/插入/删除。  
- **适用题型**：  
  1. 需要动态维护有序集合且要求对数级别的增删查（如 `Design Skiplist`、`Design Ordered Stream`）。  
  2. 替代平衡二叉树的场景，例如实现 `SortedMap`、`Priority Queue`（带删除功能）时。  
- **一句话总结**：**“让指针跨层跳跃，层层递进定位”** 是解这类有序集合问题的钥匙。

---

## 反思

- **第一反应**：直接用有序数组或列表实现，担心会超时。  
- **最容易踩的坑**：  
  - 随机层数的实现不当会导致层数过高或过低，破坏对数期望。  
  - 删除后忘记收缩最高层，导致后续搜索在空层上浪费时间。  
  - 处理重复元素时，需要在每层都插入新节点（不覆盖），否则会误删。  
- **下次思路**：看到 “需要在有序集合上高效增删查” 时，第一步就想到 **使用跳表或平衡树**；若实现复杂度不想太高，优先尝试 **跳表**，因为代码相对简洁且易于调试。