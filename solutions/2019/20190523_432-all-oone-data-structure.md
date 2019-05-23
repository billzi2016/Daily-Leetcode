# #432. All O`one 数据结构 / All O`one Data Structure

> 难度：困难 · 标签：Hash Table、Linked List、Design、Doubly-Linked List · [LeetCode 链接](https://leetcode.com/problems/all-oone-data-structure/)

---

## 题目（英文原版）

**Description**

Design a data structure to store the strings' count with the ability to return the strings with minimum and maximum counts.
Implement the AllOne class:
Note that each function must run in O(1) average time complexity.

**Examples**

**Example 1:**

```
Input
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["leet"], [], []]
Output
[null, null, null, "hello", "hello", null, "hello", "leet"]

Explanation
AllOne allOne = new AllOne();
allOne.inc("hello");
allOne.inc("hello");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "hello"
allOne.inc("leet");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "leet"
```

**Constraints**

- 1 <= key.length <= 10
- key consists of lowercase English letters.
- It is guaranteed that for each call to dec, key is existing in the data structure.
- At most 5 * 104 calls will be made to inc, dec, getMaxKey, and getMinKey.

---

## 题目（中文翻译）

设计一个数据结构来存储字符串的计数，并能够返回计数最小和计数最大的字符串。  
实现 **AllOne** 类，使其中的每个函数的平均时间复杂度均为 **O(1)**。

**AllOne** 类需要实现以下方法：

- `inc(key)`: 将字符串 `key` 的计数增加 1；如果 `key` 不存在，则将其计数设为 1。  
- `dec(key)`: 将字符串 `key` 的计数减少 1；如果计数变为 0，则从数据结构中删除 `key`。  
- `getMaxKey()`: 返回任意一个计数最大的字符串。如果数据结构为空，返回空字符串 `""`。  
- `getMinKey()`: 返回任意一个计数最小的字符串。如果数据结构为空，返回空字符串 `""`。

### 示例

**示例 1**

```text
Input
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["leet"], [], []]

Output
[null, null, null, "hello", "hello", null, "hello", "leet"]
```

**解释**
```java
AllOne allOne = new AllOne();
allOne.inc("hello");          // "hello" 的计数变为 1
allOne.inc("hello");          // "hello" 的计数变为 2
allOne.getMaxKey();           // 返回 "hello"
allOne.getMinKey();           // 返回 "hello"
allOne.inc("leet");           // "leet" 的计数变为 1
allOne.getMaxKey();           // 返回 "hello"
allOne.getMinKey();           // 返回 "leet"
```

### 约束条件

- `1 <= key.length <= 10`
- `key` 只包含小写英文字母。
- 保证每次调用 `dec` 时，`key` 必定存在于数据结构中。
- 最多会有 `5 * 10^4` 次对 `inc`、`dec`、`getMaxKey`、`getMinKey` 的调用。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **key 与它的计数** 用一个哈希表（`dict`）存起来，另外再准备一个 **计数到所有拥有该计数的 key 集合** 的哈希表。  

- `cnt[key]` → 这个 key 当前出现了多少次。  
- `group[count]` → 所有计数等于 `count` 的 key 放在一个 `set` 里。  

这样 `inc` / `dec` 只需要在两个哈希表之间搬家，时间是 **O(1)**。  
但是 `getMaxKey` / `getMinKey` 需要在 `group` 的所有计数上遍历一次，找出最大的/最小的计数，再随便返回其中一个 key。遍历所有计数的时间是 **O(m)**，其中 `m` 是不同计数的种类数，最坏情况下相当于 **O(n)**（`n` 为当前的 key 数量）。

> **类比**：  
> - 哈希表就像一本词典，**key** 是单词，**value** 是页码，查找非常快。  
> - `group` 里的 `set` 像是把同一页码的单词都写在同一张纸上，方便搬家。

#### 代码（Python）

```python
class AllOne:
    def __init__(self):
        # key -> count
        self.cnt = {}                     # 哈希表：记录每个 key 的计数
        # count -> set of keys
        self.group = {}                   # 哈希表：同一计数的 key 放在同一个集合

    def inc(self, key: str) -> None:
        old = self.cnt.get(key, 0)        # 之前的计数，若不存在则为 0
        new = old + 1
        self.cnt[key] = new               # 更新 cnt

        # 把 key 从 old 对应的集合移走（若 old 为 0 则不需要移走）
        if old > 0:
            self.group[old].remove(key)
            if not self.group[old]:       # 集合空了就删掉，防止遍历时出现无用的计数
                del self.group[old]

        # 把 key 加入 new 对应的集合
        self.group.setdefault(new, set()).add(key)

    def dec(self, key: str) -> None:
        old = self.cnt[key]                # 题目保证 key 必定存在
        new = old - 1

        # 从 old 集合中移除
        self.group[old].remove(key)
        if not self.group[old]:
            del self.group[old]

        if new == 0:                       # 计数降到 0，直接删除 key
            del self.cnt[key]
        else:
            self.cnt[key] = new
            self.group.setdefault(new, set()).add(key)

    def getMaxKey(self) -> str:
        if not self.group:
            return ""
        max_cnt = max(self.group.keys())   # O(m) 遍历所有计数
        # 任取一个键返回即可
        return next(iter(self.group[max_cnt]))

    def getMinKey(self) -> str:
        if not self.group:
            return ""
        min_cnt = min(self.group.keys())   # O(m) 遍历所有计数
        return next(iter(self.group[min_cnt]))
```

#### 复杂度

- **时间复杂度**  
  - `inc` / `dec`：`O(1)`，因为只在哈希表里做常数次插入/删除。  
  - `getMaxKey` / `getMinKey`：`O(m)`，需要遍历所有不同的计数。最坏情况下 `m ≈ n`，相当于 `O(n)`。  
  > **大白话**：`O(n)` 就像你把所有同学的成绩排个序再找最高分，需要看每个人一次。

- **空间复杂度**  
  - 两个哈希表共保存每个 key 一份信息，最坏 `O(n)`（`n` 为当前键的数量）。

---

### 2. 最优解

#### 思路  
要让 **所有操作都在 O(1) 平均时间** 完成，关键是把「找最大计数」和「找最小计数」这一步也做到常数时间。  
我们可以把 **计数本身** 组织成一个 **双向链表**（doubly linked list），链表的每个节点保存：

- `count`：该节点代表的计数值  
- `keys`：所有计数等于 `count` 的 key，放在一个 `set`（或 `OrderedDict`）里

链表按照计数从小到大排列，**头节点** 的计数最小，**尾节点** 的计数最大。这样：

- `getMinKey` → 直接返回头节点的任意 key（`O(1)`）  
- `getMaxKey` → 直接返回尾节点的任意 key（`O(1)`）

要让 `inc` / `dec` 也保持 `O(1)`，我们再维护一个 **key → 节点** 的哈希表 `node_of[key]`，这样可以在常数时间定位到某个 key 所在的计数节点，然后：

- **增加** (`inc`)：把 key 从当前节点搬到“计数+1”对应的下一个节点；如果下一个节点的计数不是 `cur+1`，就**在链表中间新建一个节点**。搬家后，如果原节点的 `keys` 为空，就把该节点删掉。
- **减少** (`dec`)：类似，只是搬到“计数-1”对应的前一个节点；计数降到 0 时直接删除 key。

> **类比**：  
> - 双向链表像是一条有序的火车轨道，每个车厢（节点）装的都是同一票数的乘客（key）。我们可以在任意车厢前后快速插入或删除车厢。  
> - `node_of` 哈希表像是每位乘客的身份证，告诉我们他正坐在哪个车厢，省去遍历找车厢的时间。

#### 代码（Python）

```python
class Node:
    """双向链表的节点，表示一种计数值"""
    __slots__ = ('cnt', 'keys', 'prev', 'next')
    def __init__(self, cnt: int):
        self.cnt = cnt                # 计数值
        self.keys = set()             # 所有拥有该计数的 key
        self.prev = None              # 前一个节点
        self.next = None              # 后一个节点


class AllOne:
    def __init__(self):
        # 哨兵节点，防止空链表时的边界判断
        self.head = Node(float('-inf'))   # 最左侧哨兵，计数无限小
        self.tail = Node(float('inf'))    # 最右侧哨兵，计数无限大
        self.head.next = self.tail
        self.tail.prev = self.head

        self.key_node = {}                # key -> 所在的节点

    # ---------- 链表操作 ----------
    def _add_node_after(self, new_node: Node, prev_node: Node) -> None:
        """在 prev_node 之后插入 new_node（时间 O(1)）"""
        nxt = prev_node.next
        new_node.prev, new_node.next = prev_node, nxt
        prev_node.next = new_node
        nxt.prev = new_node

    def _remove_node(self, node: Node) -> None:
        """把 node 从链表中摘除（时间 O(1)）"""
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev
        # 断开引用帮助 GC
        node.prev = node.next = None

    # ---------- inc ----------
    def inc(self, key: str) -> None:
        if key not in self.key_node:               # 第一次出现
            # 确保在计数为 1 的节点上
            if self.head.next.cnt != 1:            # 没有计数为 1 的节点，需要新建
                node1 = Node(1)
                self._add_node_after(node1, self.head)
            else:
                node1 = self.head.next
            node1.keys.add(key)
            self.key_node[key] = node1
            return

        cur = self.key_node[key]                    # 当前所在节点
        nxt_cnt = cur.cnt + 1

        # 判断后继节点是否已经是 nxt_cnt
        if cur.next.cnt != nxt_cnt:
            new_node = Node(nxt_cnt)
            self._add_node_after(new_node, cur)
        else:
            new_node = cur.next

        # 把 key 移动到新节点
        new_node.keys.add(key)
        self.key_node[key] = new_node

        # 从旧节点删掉
        cur.keys.remove(key)
        if not cur.keys:                            # 旧节点空了就删掉
            self._remove_node(cur)

    # ---------- dec ----------
    def dec(self, key: str) -> None:
        cur = self.key_node[key]                    # 必然存在
        if cur.cnt == 1:                            # 删除 key
            cur.keys.remove(key)
            del self.key_node[key]
            if not cur.keys:
                self._remove_node(cur)
            return

        prev_cnt = cur.cnt - 1
        # 判断前驱节点是否已经是 prev_cnt
        if cur.prev.cnt != prev_cnt:
            new_node = Node(prev_cnt)
            self._add_node_after(new_node, cur.prev)
        else:
            new_node = cur.prev

        # 把 key 移动到前驱节点
        new_node.keys.add(key)
        self.key_node[key] = new_node

        # 从旧节点删掉
        cur.keys.remove(key)
        if not cur.keys:
            self._remove_node(cur)

    # ---------- getMaxKey ----------
    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:             # 链表为空
            return ""
        # tail.prev 是计数最大的真实节点
        return next(iter(self.tail.prev.keys))

    # ---------- getMinKey ----------
    def getMinKey(self) -> str:
        if self.head.next == self.tail:             # 链表为空
            return ""
        # head.next 是计数最小的真实节点
        return next(iter(self.head.next.keys))
```

#### 复杂度

- **时间复杂度**  
  - `inc` / `dec` / `getMaxKey` / `getMinKey`：全部都是 **O(1)**（常数时间），因为所有操作只涉及哈希表查找、集合增删、以及链表的相邻节点插入/删除。  
  > 与暴力解相比，最大/最小查询不再需要遍历所有计数，瞬间就能拿到答案。

- **空间复杂度**  
  - 每个不同的 key 只会在链表中出现一次，链表节点的数量最多等于不同计数的种类数，合计仍是 **O(n)**（`n` 为当前键的数量）。  
  - 额外的哈希表 `key_node` 也占 `O(n)`，总体空间仍是线性。

---

## 心得

- **核心技巧**：用 **双向链表 + 哈希表** 把“计数”这一维度变成有序的结构，使得最值查询可以在常数时间完成。  
- **适用的题型**：  
  1. 需要在 **O(1)** 时间内获取「最大/最小」或「前驱/后继」的结构（如 LFU 缓存、设计 O(1) 计数器）。  
  2. 「分组」并保持分组顺序的场景（如「数据流的中位数」可以用两堆堆实现类似思路）。  
  3. 需要在 **O(1)** 删除/插入任意元素并快速定位的场景（如随机集合 `Insert Delete GetRandom O(1)`）。
- **一句话总结**：**把计数抽象成链表节点，用哈希表把 key 快速映射到对应节点，链表的首尾天然提供最小/最大键**。

---

## 反思

- **第一反应**：直接想到「两个哈希表」来分别记录 `key→count` 与 `count→keys`，但忽视了最值查询的线性代价。  
- **最容易踩的坑**  
  - **链表空状态**：需要哨兵节点或额外判断，防止在删除最后一个计数节点后访问空指针。  
  - **计数为 0 的处理**：`dec` 时若计数降到 0 必须彻底把 key 从所有结构中移除，否则会导致 `getMinKey` 误返回已删除的 key。  
  - **集合的迭代**：`next(iter(...))` 只取任意一个 key，若集合为空一定要先检查，否则会抛异常。  
- **下次思路**：一看到「需要 O(1) 取最大/最小」且数据会不断增删，就先考虑 **有序的链表/双端队列 + 哈希映射**，把「顺序」交给链表，把「定位」交给哈希表。这样常数时间往往可以实现。