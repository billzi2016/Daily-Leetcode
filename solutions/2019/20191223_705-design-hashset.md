# #705. 设计哈希集合 / Design HashSet

> 难度：简单 · 标签：Array、Hash Table、Linked List、Design、Hash Function · [LeetCode 链接](https://leetcode.com/problems/design-hashset/)

---

## 题目（英文原版）

**Description**

Design a HashSet without using any built-in hash table libraries.
Implement MyHashSet class:

**Examples**

**Example 1:**

```
Input
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
Output
[null, null, null, true, false, null, true, null, false]

Explanation
MyHashSet myHashSet = new MyHashSet();
myHashSet.add(1);      // set = [1]
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(1); // return True
myHashSet.contains(3); // return False, (not found)
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(2); // return True
myHashSet.remove(2);   // set = [1]
myHashSet.contains(2); // return False, (already removed)
```

**Constraints**

- 0 <= key <= 106
- At most 104 calls will be made to add, remove, and contains.

---

## 题目（中文翻译）

设计一个哈希集合（HashSet），要求不使用任何内置的哈希表库。

实现 `MyHashSet` 类，使其支持以下操作：

- `MyHashSet()`：初始化一个空的哈希集合。  
- `void add(int key)`：向集合中插入元素 `key`。如果集合中已存在 `key`，则不进行任何操作。  
- `bool contains(int key)`：判断集合中是否存在 `key`，若存在返回 `true`，否则返回 `false`。  
- `void remove(int key)`：从集合中删除元素 `key`。如果集合中不存在 `key`，则不进行任何操作。  

## 示例

**示例 1：**

```json
Input
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]

Output
[null, null, null, true, false, null, true, null, false]
```

**解释**

```java
MyHashSet myHashSet = new MyHashSet();
myHashSet.add(1);      // set = [1]
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(1); // 返回 true
myHashSet.contains(3); // 返回 false（未找到）
myHashSet.add(2);      // set = [1, 2]（已存在，不会重复插入）
myHashSet.contains(2); // 返回 true
myHashSet.remove(2);   // set = [1]
myHashSet.contains(2); // 返回 false（已经被移除）
```

## 约束条件

- `0 <= key <= 10^6`
- 最多会调用 `add`、`remove`、`contains` 共计 `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把集合里的元素都保存在一个普通的 Python `list`（相当于一张纸条，上面写着所有已经加入的数字）。  
- **添加 (`add`)**：先遍历整张纸条，看要加入的数字是否已经在上面；如果没有，就把它写在纸条的末尾。  
- **查询 (`contains`)**：同样遍历整张纸条，看看要查的数字有没有出现。  
- **删除 (`remove`)**：遍历整张纸条找到目标数字后，把它从纸条上划掉（或者把后面的数字往前搬，保持列表紧凑）。

> **类比**：把 `list` 想象成一本“通讯录”，每次想找某个人都要从第一页翻到最后一页，这显然很慢。

这个方法之所以**正确**，是因为我们始终用线性搜索把每个操作都完整检查了一遍——只要遍历到目标，就能完成对应的增、删、查。

#### 代码（Python）

```python
class MyHashSet:
    def __init__(self):
        # 用一个普通列表保存所有已经加入的 key
        self.data = []                     # [] 表示空集合

    def add(self, key: int) -> None:
        # 只有当 key 不在集合中时才加入，防止重复
        if not self.contains(key):         # 先检查是否已经存在
            self.data.append(key)          # 把 key 加到列表尾部

    def remove(self, key: int) -> None:
        # 线性遍历找到 key 并删除
        for i, val in enumerate(self.data):
            if val == key:                  # 找到了要删除的元素
                self.data.pop(i)            # 删除它，列表会自动收拢
                break                       # 删除后直接退出循环

    def contains(self, key: int) -> bool:
        # 线性搜索判断 key 是否在列表中
        for val in self.data:
            if val == key:
                return True                # 找到了
        return False                       # 没找到
```

#### 复杂度  

- **时间复杂度**  
  - `add`、`remove`、`contains` 最坏情况都需要遍历整个列表，时间是 **O(n)**（这里的 n 是集合当前的元素个数）。  
  - 大白话：如果集合里有 1000 个数字，最坏情况下要检查 1000 次才知道答案。

- **空间复杂度**  
  - 只用了一个列表来存放元素，最多保存所有出现过的数字，空间是 **O(n)**。  
  - 大白话：集合里有多少元素，就占多少内存，没有额外的“大桶”或“额外表”。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次操作都要线性遍历。我们需要一种“快速定位”的办法。  
本题给出的约束是：

- `0 <= key <= 10^6`（键的取值范围固定且不大）  
- 最多 `10^4` 次操作  

因为键的范围是 **0~1,000,000**，我们完全可以直接为每一个可能的键准备一个“位置”，用**布尔数组**（相当于一排灯泡）来记录该键是否已经在集合中。  

- **数组的下标** 就是键的数值。  
- **数组的值** 为 `True` 表示键已经被加入，为 `False` 表示未加入。  

这样：

- `add(key)` → 把 `bucket[key] = True`（直接打开对应灯泡）  
- `remove(key)` → 把 `bucket[key] = False`（关灯）  
- `contains(key)` → 直接返回 `bucket[key]` 的真假值  

> **类比**：把键想象成一本字典的页码，每一页上都有一个小灯泡。要检查某个页码是否在集合里，只要看那一页的灯泡亮没亮，时间恒定。

如果不想一次性开 1,000,001 个灯泡（虽然内存还能接受），也可以采用**哈希桶 + 链表**的方式：  
- 取模把键分配到固定数量的桶（比如 1000 个），每个桶内部用链表存放冲突的键。  
- 这种做法更像真实的哈希表，实现上会稍微复杂一些，但仍然是 **O(1)** 均摊时间。

下面分别给出两种实现：**布尔数组**（最简）和 **哈希桶 + 链表**（更贴近真实 HashSet 的思想）。

#### 代码（Python）——布尔数组实现

```python
class MyHashSet:
    def __init__(self):
        # 因为 key 的范围是 0~10^6，直接开一个长度为 10^6+1 的布尔数组
        self.bucket = [False] * (10**6 + 1)   # 所有灯泡默认是关的

    def add(self, key: int) -> None:
        # 直接把对应位置的灯泡打开
        self.bucket[key] = True

    def remove(self, key: int) -> None:
        # 把对应位置的灯泡关掉
        self.bucket[key] = False

    def contains(self, key: int) -> bool:
        # 直接返回灯泡的状态
        return self.bucket[key]
```

#### 代码（Python）——哈希桶 + 链表实现

```python
class ListNode:
    """链表结点，用来存放冲突的 key"""
    __slots__ = ("val", "next")   # 节约内存

    def __init__(self, val: int, nxt: 'ListNode' = None):
        self.val = val
        self.next = nxt


class MyHashSet:
    def __init__(self):
        # 选取一个合适的桶数量（这里取 1000），越大冲突越少，空间稍多
        self.bucket_size = 1000
        self.buckets = [None] * self.bucket_size   # 每个元素都是链表头指针

    def _hash(self, key: int) -> int:
        """简单的取模哈希函数，返回键所在的桶下标"""
        return key % self.bucket_size

    def add(self, key: int) -> None:
        idx = self._hash(key)                     # 先算出属于哪一桶
        head = self.buckets[idx]

        # 检查链表里是否已经有该键，避免重复插入
        cur = head
        while cur:
            if cur.val == key:
                return                           # 已经存在，直接返回
            cur = cur.next

        # 没有找到，则把新结点插到链表头部（O(1)）
        new_node = ListNode(key, head)
        self.buckets[idx] = new_node

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        cur = self.buckets[idx]
        prev = None

        while cur:
            if cur.val == key:
                if prev:
                    prev.next = cur.next        # 把要删除的结点从链表中摘除
                else:
                    self.buckets[idx] = cur.next # 删除的是头结点
                return
            prev, cur = cur, cur.next

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        cur = self.buckets[idx]

        while cur:
            if cur.val == key:
                return True
            cur = cur.next
        return False
```

#### 复杂度  

- **布尔数组实现**  
  - **时间复杂度**：`add / remove / contains` 均为 **O(1)**，因为只需要一次数组下标访问。  
    - 大白话：不管集合里有多少元素，操作只需要看一盏灯，永远是常数时间。  
  - **空间复杂度**：**O(M)**，其中 `M = 10^6 + 1`（固定大小的布尔数组）。  
    - 大白话：我们一次性准备了 1,000,001 盏灯，和键的最大取值直接挂钩。

- **哈希桶 + 链表实现**  
  - **时间复杂度**：均摊 **O(1)**，最坏情况（所有键冲到同一个桶）会退化成 **O(n)**，但在均匀哈希下冲突很少。  
    - 大白话：大多数情况下，只需要检查几盏灯（链表长度很短），所以看起来也是常数时间。  
  - **空间复杂度**：**O(n + B)**，`n` 为实际存储的键数，`B` 为桶的数量（这里是 1000）。  
    - 大白话：我们只为出现过的键分配空间，另外再预留一些固定的桶。

相较于暴力的 **O(n)** 时间，最优解把每次操作的时间都压到常数级，极大提升了效率。

---

## 心得

- **核心技巧**：利用**键的取值范围**直接映射到数组（布尔数组）或使用**哈希桶 + 链表**实现近似 O(1) 的增删查。  
- **适用场景**  
  1. `Design HashMap`、`Design HashSet` 等需要自行实现哈希结构的题目。  
  2. 需要 **O(1)** 查询的“存在性判断”类题目，例如 “Two Sum - 数据结构版”。  
  3. 当键的范围已知且不大时，可直接使用 **位图 / 布尔数组**（如 “Find the Duplicate Number” 中的范围限定）。  
- **一句话总结**：把“要找的东西”直接放在“它的地址上”，不必再遍历找。

---

## 反思

- **第一反应**：直接用列表保存元素，逐个遍历检查——最自然的实现，却忽视了时间成本。  
- **最容易踩的坑**  
  - **边界**：键可能是 `0`，数组下标要从 `0` 开始；如果使用 `bucket_size`，要防止除零错误。  
  - **重复插入**：`add` 必须先判断元素是否已存在，否则会出现重复计数（虽然集合本身不关心计数，但链表实现会产生多余节点）。  
  - **空间限制**：如果键的范围更大（比如 `10^9`），布尔数组就不再可行，需要真正的哈希桶实现。  
- **下次第一步**：先检查 **键值范围**，如果范围适中就考虑“直接映射数组”，否则再设计 **哈希函数 + 桶** 的结构。