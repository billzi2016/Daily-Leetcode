# #706. **设计哈希映射** / Design HashMap

> 难度：简单 · 标签：Array、Hash Table、Linked List、Design、Hash Function · [LeetCode 链接](https://leetcode.com/problems/design-hashmap/)

---

## 题目（英文原版）

**Description**

Design a HashMap without using any built-in hash table libraries.
Implement the MyHashMap class:

**Examples**

**Example 1:**

```
Input
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
Output
[null, null, null, 1, -1, null, 1, null, -1]

Explanation
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // The map is now [[1,1]]
myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]
```

**Constraints**

- 0 <= key, value <= 106
- At most 104 calls will be made to put, get, and remove.

---

## 题目（中文翻译）

设计一个哈希映射（HashMap），禁止使用任何内置的哈希表（hash table）库。

实现 `MyHashMap` 类，使其支持以下操作：

- `put(key, value)`：插入键值对 `(key, value)`。如果 `key` 已存在，则更新对应的 `value`。
- `get(key)`：返回 `key` 对应的 `value`；如果 `key` 不存在，则返回 `-1`。
- `remove(key)`：删除 `key` 以及对应的 `value`，如果 `key` 不存在则不做任何操作。

**示例 1**

```text
Input
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]

Output
[null, null, null, 1, -1, null, 1, null, -1]
```

**解释**
```java
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // 哈希映射现在为 [[1,1]]
myHashMap.put(2, 2); // 哈希映射现在为 [[1,1], [2,2]]
myHashMap.get(1);    // 返回 1，哈希映射仍为 [[1,1], [2,2]]
myHashMap.get(3);    // 返回 -1（即未找到），哈希映射仍为 [[1,1], [2,2]]
myHashMap.put(2, 1); // 哈希映射更新为 [[1,1], [2,1]]（即更新已有的值）
myHashMap.get(2);    // 返回 1，哈希映射仍为 [[1,1], [2,1]]
myHashMap.remove(2); // 删除键 2 对应的映射，哈希映射现在为 [[1,1]]
myHashMap.get(2);    // 返回 -1（即未找到），哈希映射仍为 [[1,1]]
```

**约束条件**

- `0 <= key, value <= 10^6`
- 最多会调用 `put、get、remove` 共计 `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有的 `(key, value)` 对都放进一个普通的 Python 列表里，  
每次 `put / get / remove` 都在这个列表里 **线性遍历**，找到对应的键再进行操作。

- **数据结构**：列表（`list`）相当于一排装着小盒子的抽屉，每个抽屉里装 `(key, value)`。  
  查找时只能从左到右一个一个打开抽屉，就像在字典里找词，却没有索引，只能逐页翻。

- **正确性**：只要遍历到的 `key` 与要操作的键相同，就能得到（或修改、删除）对应的 `value`。  
  因为题目只要求实现 `put、get、remove`，不要求排序或其他高级操作，这种线性搜索完全可以满足功能。

#### 代码（Python）

```python
class MyHashMap:
    def __init__(self):
        # 用一个列表保存所有的 (key, value) 对
        self.data = []                     # [] 表示空的抽屉

    def put(self, key: int, value: int) -> None:
        """如果 key 已经存在就更新，否则在末尾新增一对"""
        for i, (k, _) in enumerate(self.data):
            if k == key:                   # 找到相同的钥匙
                self.data[i] = (key, value)   # 替换旧的 value
                return
        self.data.append((key, value))     # 没找到，新增一对

    def get(self, key: int) -> int:
        """遍历查找 key，找到就返回对应的 value，找不到返回 -1"""
        for k, v in self.data:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        """遍历找到后把对应的 (key, value) 删除"""
        for i, (k, _) in enumerate(self.data):
            if k == key:
                self.data.pop(i)           # 删除抽屉
                return
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每次 `put / get / remove` 最坏都要遍历完整个列表，`n` 是当前已存放的键值对数量。  
  用大白话说，就是“如果有 1000 条记录，最差情况下要看 1000 次”。

- **空间复杂度**：`O(n)`  
  需要保存所有键值对，列表的大小正好等于键值对的数量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **线性遍历**——每次操作都要把所有抽屉都打开一次。  
我们可以借鉴现实中 **哈希表** 的做法：先把钥匙（`key`）通过**哈希函数**映射到固定数量的**桶**（bucket）上，再在对应的桶里做局部搜索。这样每个桶只会存少量元素，平均时间就会变成常数级。

**关键步骤**  

1. **选取桶的数量** `BASE`（如 1000）。把所有键均匀分配到这 1000 个桶里。  
2. **哈希函数**：`idx = key % BASE`，相当于把钥匙除以 1000，余数决定它落在哪个抽屉里。  
3. **桶的内部结构**：每个桶仍然用一个小列表保存冲突的 `(key, value)` 对（称为**链表法**）。因为同一个桶里最多只有少量元素，线性搜索已经足够快。  
4. **操作实现**：  
   - `put` → 先算出桶索引，再在该桶里找键是否已存在，存在则更新，不存在则追加。  
   - `get` → 同理，只返回找到的值或 `-1`。  
   - `remove` → 在桶里找到后删除对应的元素。  

> **为什么这样快？**  
> 把 10⁴ 次操作均匀分布到 1000 个桶后，平均每个桶只有约 10 条记录。  
> 查找、插入、删除只需要遍历这 10 条记录，时间大约是 `O(10)`，即 **常数时间** `O(1)`（在大多数情况下如此）。

#### 代码（Python）

```python
class MyHashMap:
    """使用固定大小的桶 + 链表实现的简易哈希表"""

    def __init__(self):
        self.BASE = 1000                     # 桶的数量，类似抽屉的总数
        # 每个桶都是一个列表，初始为空列表 []，共 self.BASE 个
        self.buckets = [[] for _ in range(self.BASE)]

    def _hash(self, key: int) -> int:
        """哈希函数：把 key 映射到 [0, BASE-1] 的桶编号"""
        return key % self.BASE

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)                 # 找到属于哪个桶
        bucket = self.buckets[idx]            # 取出该桶（一个小列表）

        for i, (k, _) in enumerate(bucket):
            if k == key:                       # 桶里已经有这个键
                bucket[i] = (key, value)       # 直接更新对应的值
                return
        bucket.append((key, value))            # 没有则在桶尾部新增

    def get(self, key: int) -> int:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v                       # 找到直接返回
        return -1                              # 没有找到返回 -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)                  # 删除该键值对
                return
        # 若不存在什么也不做
```

#### 复杂度  

- **时间复杂度**：`O(1)`（均摊）  
  解释：因为键被均匀分配到 1000 个桶里，平均每个桶只会有极少数元素（约 10 条），遍历它们的代价可以视为常数。  
  与暴力解相比，原来的 `O(n)` 变成了几乎不随 `n` 增长的 `O(1)`。

- **空间复杂度**：`O(n + BASE)` → `O(n)`  
  需要存放所有键值对 `n` 条，加上固定的 `BASE` 个空桶（常数级），总体随输入规模线性增长。

---

## 心得

- **核心技巧**：**哈希函数 + 桶（链表）**，即“把大问题拆成很多小问题，各自快速解决”。  
- **适用的题型**：  
  1. **Design HashSet / Design HashMap**（本题）。  
  2. **Two Sum - 使用哈希表快速查找配对**。  
  3. **LRU Cache**（需要 O(1) 的查找和删除，常用哈希表+双向链表实现）。  
- **一句话总结**：把键通过取余映射到固定数量的桶里，再在每个桶内部做线性搜索，即可在常数时间内完成 `put/get/remove`。

---

## 反思

- **第一反应**：直接用列表保存所有键值对，想到“遍历查找”。这就是暴力解的自然想法。  
- **最容易踩的坑**：  
  - **哈希冲突**：不同的键可能映射到同一个桶，需要在桶内部再做区分（用链表或其他结构）。  
  - **边界条件**：`key` 可能为 `0`，`value` 也可能为 `0`，不能把 `0` 当作“未找到”的标记。  
  - **桶的大小**：若选太小会导致冲突多，性能退化到 `O(n)`；太大则浪费空间。这里 `1000` 对题目约束已经足够。  
- **下次类似题**：第一步先**思考哈希**——把键映射到固定桶，再决定桶内部如何存储（链表、红黑树等）。这一步往往能把原本的线性遍历直接提升到常数时间。