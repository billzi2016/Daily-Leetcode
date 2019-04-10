# #381. 插入、删除、随机获取 O(1) - 允许重复 / Insert Delete GetRandom O(1) - Duplicates allowed

> 难度：困难 · 标签：Array、Hash Table、Math、Design、Randomized · [LeetCode 链接](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/)

---

## 题目（英文原版）

**Description**

RandomizedCollection is a data structure that contains a collection of numbers, possibly duplicates (i.e., a multiset). It should support inserting and removing specific elements and also reporting a random element.
Implement the RandomizedCollection class:
You must implement the functions of the class such that each function works on average O(1) time complexity.
Note: The test cases are generated such that getRandom will only be called if there is at least one item in the RandomizedCollection.

**Examples**

**Example 1:**

```
Input
["RandomizedCollection", "insert", "insert", "insert", "getRandom", "remove", "getRandom"]
[[], [1], [1], [2], [], [1], []]
Output
[null, true, false, true, 2, true, 1]

Explanation
RandomizedCollection randomizedCollection = new RandomizedCollection();
randomizedCollection.insert(1);   // return true since the collection does not contain 1.
                                  // Inserts 1 into the collection.
randomizedCollection.insert(1);   // return false since the collection contains 1.
                                  // Inserts another 1 into the collection. Collection now contains [1,1].
randomizedCollection.insert(2);   // return true since the collection does not contain 2.
                                  // Inserts 2 into the collection. Collection now contains [1,1,2].
randomizedCollection.getRandom(); // getRandom should:
                                  // - return 1 with probability 2/3, or
                                  // - return 2 with probability 1/3.
randomizedCollection.remove(1);   // return true since the collection contains 1.
                                  // Removes 1 from the collection. Collection now contains [1,2].
randomizedCollection.getRandom(); // getRandom should return 1 or 2, both equally likely.
```

**Constraints**

- -231 <= val <= 231 - 1
- At most 2 * 105 calls in total will be made to insert, remove, and getRandom.
- There will be at least one element in the data structure when getRandom is called.

---

## 题目（中文翻译）

RandomizedCollection（随机集合）是一种数据结构，用于存放一组数字，允许出现重复元素（即多重集合（multiset））。它需要支持插入指定元素、删除指定元素以及随机返回一个元素的操作。

实现 RandomizedCollection 类：
- 需要实现类中的各函数，使每个函数的平均时间复杂度为 **O(1)**。
- 注意：测试用例会保证只有在 RandomizedCollection 至少包含一个元素时才会调用 `getRandom`。

**示例 1**

```text
Input
["RandomizedCollection", "insert", "insert", "insert", "getRandom", "remove", "getRandom"]
[[], [1], [1], [2], [], [1], []]
Output
[null, true, false, true, 2, true, 1]
```

**解释**
```java
RandomizedCollection randomizedCollection = new RandomizedCollection();
randomizedCollection.insert(1);   // 返回 true，因为集合中原本不包含 1。
                                  // 将 1 插入集合。
randomizedCollection.insert(1);   // 返回 false，因为集合中已经包含 1。
                                  // 再插入一个 1。此时集合为 [1,1]。
randomizedCollection.insert(2);   // 返回 true，因为集合中不包含 2。
                                  // 将 2 插入集合。此时集合为 [1,1,2]。
randomizedCollection.getRandom(); // getRandom 应该：
                                  // - 以 2/3 的概率返回 1，或
                                  // - 以 1/3 的概率返回 2。
randomizedCollection.remove(1);   // 返回 true，因为集合中包含 1。
                                  // 移除一个 1。此时集合为 [1,2]。
randomizedCollection.getRandom(); // getRandom 应该等概率返回 1 或 2。
```

**约束条件**
- `-2^31 <= val <= 2^31 - 1`
- 最多会有 `2 * 10^5` 次 `insert`、`remove` 和 `getRandom` 的调用。
- 调用 `getRandom` 时，数据结构中必定至少有一个元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有数字放进一个普通的 **列表**（`list`），  
- **插入**：直接 `list.append(val)`，时间 O(1)。  
- **删除**：要把指定的 `val` 从列表中去掉，必须遍历列表找到它的下标，然后用 `list.pop(idx)`（或者 `del list[idx]`），这一步是 **线性搜索**，最坏情况要检查全部元素，时间 O(n)。  
- **随机取值**：Python 的 `random.choice(list)` 能在 O(1) 时间内均匀抽取一个下标，返回对应的值。

> **类比**：把集合想成一本“装满数字的书”。插入相当于在书的最后加一页（直接写下去），删除相当于要在书里翻到某一页把它撕掉——必须先把书翻完才能找到那一页。

这种实现虽然很容易写，但删除的线性代价在数据量大时会让整体性能失去 **常数时间** 的保证。

#### 代码（Python）

```python
import random
from typing import List

class RandomizedCollectionBrute:
    """暴力实现，仅用于说明思路"""
    def __init__(self):
        self.nums: List[int] = []          # 用列表保存所有元素

    def insert(self, val: int) -> bool:
        """把 val 加到末尾，返回集合里原本是否没有该值"""
        existed = val in self.nums          # O(n) 的线性查找，只是为了返回 true/false
        self.nums.append(val)               # O(1) 插入
        return not existed

    def remove(self, val: int) -> bool:
        """线性搜索第一个出现的 val 并删除，返回是否成功"""
        for i, x in enumerate(self.nums):
            if x == val:                     # 找到要删除的下标
                self.nums.pop(i)             # O(n)（因为要把后面的元素左移）
                return True
        return False                        # 没找到

    def getRandom(self) -> int:
        """随机返回列表中的一个元素，前提是列表非空"""
        return random.choice(self.nums)     # O(1)
```

#### 复杂度

- **时间复杂度**  
  - `insert`：O(1)（实际返回值需要一次 O(n) 的 `in` 检查，这里只关注核心操作）。  
  - `remove`：**O(n)**，因为必须遍历列表找到要删的元素并且左移后面的元素。  
  - `getRandom`：O(1)。  
  > “O(n)” 的意思是：如果集合里有 10 000 条数据，最坏情况下要检查 10 000 次才能完成删除，耗时随数据规模线性增长。

- **空间复杂度**  
  - 只用一个列表保存所有元素，**O(n)**（n 为当前元素个数）。

---

### 2. 最优解

#### 思路  

要让 **插入、删除、随机取值** 都保持 **常数时间**，关键在于：

1. **随机取值** 仍然使用列表 `nums`，因为列表可以让我们在 O(1) 时间内根据下标直接访问元素。  
2. **删除** 时，如果直接把要删的元素从中间移走会导致 O(n) 左移。我们可以把 **要删的元素和列表最后一个元素互换位置**，然后把最后一个元素弹出，这样只涉及常数次下标操作。  
3. 交换后，需要快速知道每个数在列表中的哪些下标。这里使用 **哈希表**（`dict`）把「数值」映射到「下标集合」：`idx_map[val] = set(indices)`。  
   - **哈希表类比**：就像一本字典，`val` 是单词，`set(indices)` 是这本字典里该单词出现的所有页码。查找、插入、删除页码都只需要 O(1)。  

**完整流程**（以 `remove(val)` 为例）：

- 取出 `val` 在 `idx_map` 中的任意一个下标 `remove_idx`（集合的 `pop()`）。
- 取列表最后一个元素 `last_val` 与其下标 `last_idx = len(nums) - 1`。
- 把 `last_val` 移到 `remove_idx` 位置：`nums[remove_idx] = last_val`。
- 更新 `idx_map[last_val]`：把 `last_idx` 从集合中删掉，加入 `remove_idx`（如果 `last_val` 正好是 `val`，这一步会把同一个下标重新加回去，仍然正确）。
- 最后弹出列表最后一个元素：`nums.pop()`。
- 若 `val` 的下标集合已经为空，删掉对应的键，保持哈希表整洁。

插入时只需要把新值追加到列表尾部，然后把新下标加入 `idx_map[val]` 的集合即可。

> **为什么常数时间？**  
> - 取任意下标、集合的 `add/remove/pop` 都是 O(1)。  
> - 列表的 `append` 与 `pop()`（最后一个元素）也是 O(1)。  
> - 只进行几次哈希表查找/更新和几次列表下标写入，都是常数操作。

#### 代码（Python）

```python
import random
from collections import defaultdict
from typing import List, Set

class RandomizedCollection:
    """
    支持 O(1) 均摊时间的插入、删除、随机取值（允许重复元素）。
    """
    def __init__(self):
        # 用列表保存所有元素，便于 O(1) 随机访问
        self.nums: List[int] = []
        # 哈希表：val -> 出现的所有下标（使用 set 方便 O(1) 增删）
        self.idx_map: defaultdict[int, Set[int]] = defaultdict(set)

    def insert(self, val: int) -> bool:
        """
        将 val 插入集合，返回插入前集合是否不包含该值。
        """
        existed = val in self.idx_map          # 若集合中已有该值，返回 False
        self.nums.append(val)                  # 列表尾部追加，O(1)
        self.idx_map[val].add(len(self.nums) - 1)   # 记录新元素的下标，O(1)
        return not existed

    def remove(self, val: int) -> bool:
        """
        删除集合中一个 val（若存在），返回是否成功。
        """
        if not self.idx_map[val]:
            return False                       # 该值根本不在集合里

        # 1）随意取出一个待删除的下标
        remove_idx = self.idx_map[val].pop()   # O(1)

        # 2）拿到列表最后一个元素及其下标
        last_idx = len(self.nums) - 1
        last_val = self.nums[last_idx]

        # 3）把最后一个元素搬到 remove_idx 位置（若是同一个元素则相当于不动）
        self.nums[remove_idx] = last_val

        # 4）更新哈希表中 last_val 的下标集合
        self.idx_map[last_val].add(remove_idx)     # 把新位置加入
        self.idx_map[last_val].discard(last_idx)   # 删除旧的最后下标（若相同则自动忽略）

        # 5）弹出列表最后一个元素（已经搬走了）
        self.nums.pop()

        # 6）若 val 已经没有剩余下标，删除键防止哈希表膨胀
        if not self.idx_map[val]:
            del self.idx_map[val]

        return True

    def getRandom(self) -> int:
        """
        随机返回集合中的一个元素，假设集合非空。
        """
        return random.choice(self.nums)   # O(1) 随机下标访问
```

#### 复杂度

- **时间复杂度**  
  - `insert`：**O(1)**，因为只涉及一次列表 `append` 与一次哈希表 `add`。  
  - `remove`：**O(1)**，所有操作都是对哈希表或列表尾部的常数次读写。  
  - `getRandom`：**O(1)**，直接在列表上随机取下标。  
  > 与暴力解相比，删除不再随元素个数线性增长，而是始终只花几次“查字典、写纸条”的时间。

- **空间复杂度**  
  - 列表保存 `n` 个元素，哈希表的每个元素对应一个下标集合，合计 **O(n)**。  
  - 这里的 `set` 只存储整数下标，空间开销与元素个数线性相关。

---

## 心得

- **核心技巧**：利用「**数组 + 哈希表（值 → 下标集合）**」的组合，实现“**把要删的元素换到数组尾部再弹出**”的常数时间删除。  
- **适用场景**  
  1. **随机集合**（`Insert Delete GetRandom O(1)`）  
  2. **带重复的随机集合**（本题）  
  3. **需要 O(1) 删除任意元素的栈/队列**（如 LeetCode 380 `Insert Delete GetRandom O(1)` 的变体）  
- **一句话总结**：**把要删的东西和数组最后一个元素换位，然后用哈希表快速定位下标**，就能在 O(1) 时间内完成所有操作。

---

## 反思

- **第一反应**：直接用列表实现，忽视了删除的线性代价。  
- **最容易踩的坑**  
  - **下标同步错误**：在交换元素后必须同时更新两个值在哈希表中的下标集合，遗漏会导致后续 `remove` 或 `getRandom` 访问到已被删除的下标。  
  - **处理相同元素的特殊情况**：当 `val` 与 `last_val` 相同，`remove_idx` 与 `last_idx` 可能相等，更新集合时要使用 `discard` 而不是 `remove`，防止 KeyError。  
  - **空集合的清理**：删除完最后一个 `val` 后，若不把对应的键从 `idx_map` 删除，后续的 `val in idx_map` 判断仍会返回 True，导致逻辑错误。  
- **下次类似题的第一步**：先思考「**如何在数组里 O(1) 删除**」——若能把要删的元素换到数组尾部，再用哈希表记录位置，后面的实现往往就水到渠成。