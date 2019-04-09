# #380. 插入、删除、获取随机数 O(1) / Insert Delete GetRandom O(1)

> 难度：中等 · 标签：Array、Hash Table、Math、Design、Randomized · [LeetCode 链接](https://leetcode.com/problems/insert-delete-getrandom-o1/)

---

## 题目（英文原版）

**Description**

Implement the RandomizedSet class:
You must implement the functions of the class such that each function works in average O(1) time complexity.

**Examples**

**Example 1:**

```
Input
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]
Output
[null, true, false, true, 2, true, false, 2]

Explanation
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
randomizedSet.insert(2); // 2 was already in the set, so return false.
randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.
```

**Constraints**

- -231 <= val <= 231 - 1
- At most 2 * 105 calls will be made to insert, remove, and getRandom.
- There will be at least one element in the data structure when getRandom is called.

---

## 题目（中文翻译）

实现 `RandomizedSet` 类，使其所有成员函数的**平均**时间复杂度均为 O(1)。

---

**示例 1**

```text
Input
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]
Output
[null, true, false, true, 2, true, false, 2]
```

**解释**
```java
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1);    // 将 1 插入集合，返回 true 表示插入成功。
randomizedSet.remove(2);    // 2 不在集合中，返回 false。
randomizedSet.insert(2);    // 将 2 插入集合，返回 true。集合现在为 [1,2]。
randomizedSet.getRandom(); // 随机返回 1 或 2 中的任意一个。
randomizedSet.remove(1);    // 删除 1，返回 true。集合现在为 [2]。
randomizedSet.insert(2);    // 2 已经在集合中，返回 false。
randomizedSet.getRandom(); // 由于集合中只有 2，必定返回 2。
```

---

### 约束条件

- `-2^31 <= val <= 2^31 - 1`
- 最多会调用 `insert`、`remove`、`getRandom` 共计 `2 * 10^5` 次。
- 调用 `getRandom` 时，数据结构中必定至少存在一个元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有元素存放在 **列表（list）** 或 **集合（set）** 里：

- `insert(val)`：直接把 `val` 加入集合，如果已经存在则返回 `False`。
- `remove(val)`：直接把 `val` 从集合中删掉，如果不存在返回 `False`。
- `getRandom()`：从集合里随机抽取一个元素。  

这里的 **集合** 可以类比成“词典的抽屉”，每个抽屉里只放一种单词（不允许重复），我们只需要把抽屉打开或关上即可。  

**为什么正确**：集合天然满足“不重复”的特性，插入、删除都可以直接操作；`random.choice`（或 `random.sample`）可以在已有元素中随机挑选一个，满足题目要求的随机性。

**复杂度分析**（用大白话解释）：

| 操作 | 时间 | 空间 |
|------|------|------|
| insert | 在最坏情况下，需要先检查元素是否在集合里，这一步是 **O(1)**（集合的“查字典”操作非常快） | 只多存了一个整数，**O(1)** |
| remove | 同理，集合的删除也是 **O(1)** | 删除后空间相应减少，仍是 **O(1)** |
| getRandom | 这里我们要把集合转成列表再随机取值，转列表是 **O(n)**（遍历全部元素），随机取值是 **O(1)**，所以整体 **O(n)** | 需要临时的列表，**O(n)** 额外空间 |

可以看到，**`getRandom` 成了瓶颈**，因为每次都要把所有元素搬运一遍。

#### 代码（Python）

```python
import random

class RandomizedSetBrute:
    """ 仅作演示的暴力实现 """
    def __init__(self):
        self.data = set()                     # 用 set 保存元素，不允许重复

    def insert(self, val: int) -> bool:
        if val in self.data:                  # 已经有了，返回 False
            return False
        self.data.add(val)                    # 向集合里放进一个新元素
        return True

    def remove(self, val: int) -> bool:
        if val not in self.data:              # 不存在，返回 False
            return False
        self.data.remove(val)                 # 把元素删掉
        return True

    def getRandom(self) -> int:
        # 把集合转成列表，再随机抽取一个元素
        # 这里的 O(n) 来自于 list(self.data) 这一步遍历全部元素
        lst = list(self.data)
        return random.choice(lst)            # 从列表里随机挑一个
```

#### 复杂度

- **时间复杂度**  
  - `insert` / `remove`：**O(1)**，因为集合的“查字典”和“删字典”操作都是常数时间。  
  - `getRandom`：**O(n)**，因为需要把所有元素复制到列表中（遍历一次），相当于要花 `n` 步。

- **空间复杂度**  
  - `insert` / `remove`：**O(1)** 额外空间，只是存一个整数。  
  - `getRandom`：**O(n)** 额外空间，用于临时的列表复制。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**`getRandom` 的慢点在于把集合转成列表**。如果我们能够 **同时拥有**：

1. **能够 O(1) 取任意位置元素的结构**（数组 / list），用于 `getRandom`。
2. **能够 O(1) 判断元素是否存在并定位它在数组中的下标**（哈希表 / dict），用于 `insert` / `remove`。

我们就可以把三种操作都做到 **平均 O(1)**。

实现思路如下：

- 用 **list `nums`** 按顺序存放所有元素。`getRandom` 只需要 `random.choice(nums)`，时间就是 **O(1)**（直接随机访问下标）。
- 用 **dict `pos`** 记录每个元素在 `nums` 中的下标：`pos[val] = index`。这相当于“词典”，key 是元素本身，value 是它在数组里的位置。
- **插入**：先检查 `val` 是否在 `pos` 中，若不存在，把它 **追加**到 `nums` 尾部，并在 `pos` 记录下新下标。追加是 **O(1)**。
- **删除**：要把 `val` 从数组中移除，但直接删会导致数组中间出现空洞（时间 O(n)）。我们采用 “**把最后一个元素搬到要删除的位置**” 的技巧：
  1. 取出 `val` 在数组中的下标 `idx`（通过 `pos`）。
  2. 取出数组最后一个元素 `last`。
  3. 把 `last` 写进 `nums[idx]`（覆盖要删的位子），并更新 `pos[last] = idx`。
  4. 把数组尾部弹出（`pop()`），并删除 `pos[val]`。
  这样只用了常数次赋值和弹出，时间是 **O(1)**。

**类比**：想象你在一个抽屉里放了若干球（list），每个球上都有编号（value）。抽屉外面有一本“球号→抽屉位置”的目录（dict）。当要拿走某个球时，你把抽屉最底下的球搬到它的位置，然后把最底下的空位封闭，这样抽屉的内容始终紧凑，不需要搬动很多球。

#### 代码（Python）

```python
import random

class RandomizedSet:
    """
    支持 insert、remove、getRandom，所有操作平均 O(1)。
    - nums : list，存放当前集合的所有元素，支持随机下标访问。
    - pos  : dict，映射元素 -> 它在 nums 中的下标，支持 O(1) 判断是否存在以及定位。
    """
    def __init__(self):
        self.nums = []          # 动态数组，存放元素
        self.pos = {}           # 哈希表，key 是元素，value 是在 nums 中的下标

    def insert(self, val: int) -> bool:
        """
        将 val 加入集合。
        若 val 已经存在返回 False，否则加入并返回 True。
        """
        if val in self.pos:          # 哈希表已经有这个键，说明集合里已有该元素
            return False

        # 把 val 放到数组尾部，记录下标
        self.nums.append(val)        # O(1) 追加
        self.pos[val] = len(self.nums) - 1   # 记录新元素的下标
        return True

    def remove(self, val: int) -> bool:
        """
        删除集合中的 val。
        若 val 不存在返回 False，否则删除并返回 True。
        """
        if val not in self.pos:      # 不存在直接返回
            return False

        # 需要删除的下标
        idx = self.pos[val]
        # 数组最后一个元素
        last = self.nums[-1]

        # 把最后一个元素搬到 idx 位置（覆盖要删的元素）
        self.nums[idx] = last
        self.pos[last] = idx         # 更新最后一个元素的新下标

        # 删除数组尾部（已经搬走的元素）和哈希表中 val 的记录
        self.nums.pop()              # O(1) 删除尾部
        del self.pos[val]            # O(1) 删除键值对

        return True

    def getRandom(self) -> int:
        """
        随机返回集合中的一个元素，所有元素被选中的概率相等。
        由于 nums 是紧凑数组，直接随机下标即可。
        """
        return random.choice(self.nums)   # O(1) 随机访问列表元素
```

#### 复杂度

- **时间复杂度**  
  - `insert`：**O(1)**，因为只做一次哈希查询 + 追加。  
  - `remove`：**O(1)**，只做几次哈希查询、一次元素覆盖、一次弹出。  
  - `getRandom`：**O(1)**，`random.choice` 直接在列表中随机取下标。  
  与暴力解相比，所有操作都保持常数时间，没有任何遍历。

- **空间复杂度**  
  - 额外使用了两个结构：`nums`（存放所有元素）和 `pos`（每个元素对应一个下标）。两者大小都是集合中元素的数量 `n`，所以 **O(n)**。这与只用集合的空间相同，只是把信息拆成了两份以换取时间效率。

---

## 心得

- **核心技巧**：**“数组 + 哈希表” 双向映射 + “把最后一个元素搬到删除位置”** 的思路。  
- **适用的题型**（常见的 O(1) 设计题）：
  1. **Insert Delete GetRandom O(1) – 变体**（比如支持 `getRandomUnique` 等）。
  2. **LRU Cache**（用双向链表 + 哈希表实现 O(1) 的缓存淘汰）。
  3. **All O(1) Data Structure**（同样利用哈希表和链表的组合实现 O(1) 的增删改查）。
- **一句话总结解题钥匙**：  
  > “让每个元素同时拥有‘位置编号’（数组下标）和‘查找入口’（哈希表），删除时用最后一个元素填补空位。”

---

## 反思

- **第一反应**：直接用 `set` 实现，忘记 `getRandom` 需要遍历，导致时间不符合要求。  
- **最容易踩的坑**：  
  - 删除时忘记同时更新 **被搬走元素** 在哈希表中的下标，导致后续 `getRandom` 或 `remove` 出错。  
  - `getRandom` 调用前集合可能为空（题目保证不会），实际代码里若自行测试，需要加 guard 防止 `IndexError`。  
- **下次遇到同类题**：第一步就思考“哪个操作最慢”，然后寻找 **可以把慢操作换成常数时间的辅助结构**（如数组、哈希表、链表）并设计 **如何同步更新两者**。这样往往能快速定位到类似的 “双结构 + 位置交换” 的解法。