# #2034. 股票价格波动 / Stock Price Fluctuation 

> 难度：中等 · 标签：Hash Table、Design、Heap (Priority Queue)、Data Stream、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/stock-price-fluctuation/)

---

## 题目（英文原版）

**Description**

You are given a stream of records about a particular stock. Each record contains a timestamp and the corresponding price of the stock at that timestamp.
Unfortunately due to the volatile nature of the stock market, the records do not come in order. Even worse, some records may be incorrect. Another record with the same timestamp may appear later in the stream correcting the price of the previous wrong record.
Design an algorithm that:
Implement the StockPrice class:

**Examples**

**Example 1:**

```
Input
["StockPrice", "update", "update", "current", "maximum", "update", "maximum", "update", "minimum"]
[[], [1, 10], [2, 5], [], [], [1, 3], [], [4, 2], []]
Output
[null, null, null, 5, 10, null, 5, null, 2]

Explanation
StockPrice stockPrice = new StockPrice();
stockPrice.update(1, 10); // Timestamps are [1] with corresponding prices [10].
stockPrice.update(2, 5);  // Timestamps are [1,2] with corresponding prices [10,5].
stockPrice.current();     // return 5, the latest timestamp is 2 with the price being 5.
stockPrice.maximum();     // return 10, the maximum price is 10 at timestamp 1.
stockPrice.update(1, 3);  // The previous timestamp 1 had the wrong price, so it is updated to 3.
                          // Timestamps are [1,2] with corresponding prices [3,5].
stockPrice.maximum();     // return 5, the maximum price is 5 after the correction.
stockPrice.update(4, 2);  // Timestamps are [1,2,4] with corresponding prices [3,5,2].
stockPrice.minimum();     // return 2, the minimum price is 2 at timestamp 4.
```

**Constraints**

- 1 <= timestamp, price <= 109
- At most 105 calls will be made in total to update, current, maximum, and minimum.
- current, maximum, and minimum will be called only after update has been called at least once.

---

## 题目（中文翻译）

你将会收到一系列关于某只股票的记录（record），每条记录包含一个时间戳（timestamp）以及该时间戳对应的股票价格（price）。  
由于股市的波动，这些记录**不一定按时间顺序**到达。更糟的是，某些记录可能是错误的，随后会出现 **相同时间戳的记录** 来更正之前的错误价格。

请设计一个算法实现 `StockPrice` 类，使其能够高效地处理以下操作：

* `StockPrice()`  
  初始化对象。

* `void update(int timestamp, int price)`  
  将时间戳 `timestamp` 对应的价格更新为 `price`。如果该时间戳之前已经存在记录，则用新的价格覆盖旧的价格。

* `int current()`  
  返回 **最新时间戳**（即出现的最大 `timestamp`）对应的股票价格。

* `int maximum()`  
  返回所有记录中 **最高的价格**。

* `int minimum()`  
  返回所有记录中 **最低的价格**。

---

### 示例

```json
["StockPrice", "update", "update", "current", "maximum", "update", "maximum", "update", "minimum"]
[[], [1, 10], [2, 5], [], [], [1, 3], [], [4, 2], []]
```

**输出**

```
[null, null, null, 5, 10, null, 5, null, 2]
```

**解释**

```java
StockPrice stockPrice = new StockPrice();
stockPrice.update(1, 10); // 时间戳为 [1]，对应的价格为 [10]。
stockPrice.update(2, 5);  // 时间戳为 [1, 2]，对应的价格为 [10, 5]。
stockPrice.current();    // 返回最新时间戳 2 的价格，结果是 5。
stockPrice.maximum();    // 价格中最大的为 10，返回 10。
stockPrice.update(1, 3); // 时间戳 1 的价格被更正为 3，价格列表变为 [3, 5]。
stockPrice.maximum();    // 现在最大的价格是 5，返回 5。
stockPrice.update(4, 2); // 新增时间戳 4，价格为 2，价格列表为 [3, 5, 2]。
stockPrice.minimum();    // 最低的价格是 2，返回 2。
```

---

### 约束

- `1 <= timestamp, price <= 10^9`
- 最多会调用 `update`、`current`、`maximum`、`minimum` 共计 `10^5` 次。
- `current`、`maximum`、`minimum` 的调用 **只会在至少调用一次 `update` 之后** 进行。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有收到的记录全部保存下来，然后每次要回答 `current`、`maximum`、`minimum` 时都遍历一次所有记录，找出最新的时间戳对应的价格、最高价和最低价。  

- **保存记录的容器**：可以用一个普通的字典 `ts2price`（相当于查字典，`timestamp` 是单词，`price` 是页码）把每个时间戳对应的最新价格存进去。  
- **当前价格**：遍历字典的键找到最大的时间戳，即为最新的记录。  
- **最大 / 最小价格**：遍历字典的所有值，分别取最大值和最小值。  

这样做一定能得到正确答案，因为我们每次都把所有可能的候选值检查了一遍。  

#### 代码（Python）  
```python
class StockPrice:
    def __init__(self):
        # timestamp -> latest price
        self.ts2price = {}          # 哈希表，查字典速度快

    def update(self, timestamp: int, price: int) -> None:
        # 直接覆盖，同一个时间戳后面的记录会把前面的纠正掉
        self.ts2price[timestamp] = price

    def current(self) -> int:
        # 找到最大的时间戳（最新的记录）
        latest_ts = max(self.ts2price.keys())   # O(n)遍历所有时间戳
        return self.ts2price[latest_ts]

    def maximum(self) -> int:
        # 在所有价格里挑出最大的
        return max(self.ts2price.values())      # O(n)遍历所有价格

    def minimum(self) -> int:
        # 在所有价格里挑出最小的
        return min(self.ts2price.values())      # O(n)遍历所有价格
```

#### 复杂度  
- **时间复杂度**  
  - `update`：O(1)（直接写进哈希表）  
  - `current`、`maximum`、`minimum`：O(n)（需要遍历全部 n 条记录）  
  - 这里的 **O(n)** 可以理解为“随着记录数线性增长”，如果有 10⁵ 条记录，查询一次大概要检查 10⁵ 次。  
- **空间复杂度**  
  - O(n) 用来存放所有时间戳和对应的价格。  

> 这种实现虽然思路最直观，但在最坏情况下每一次查询都要遍历整个数据集合，随着调用次数增多会非常慢，不能满足题目要求的 **10⁵ 次调用**。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每次查询都要 O(n) 扫描所有记录**。我们需要一种数据结构，使得：

1. **插入/更新** 能够在对数时间完成。  
2. **获取当前最新的价格** 能在常数时间完成（只需要记住最新的时间戳）。  
3. **获取最大值 / 最小值** 也能在对数时间完成。  

实现思路如下：

1. **哈希表 `ts2price`** 仍然保留，用来快速定位某个时间戳的最新价格。  
2. **记录最新时间戳** 用一个变量 `latest_ts`，每次 `update` 时比较并更新它。这样 `current` 只要直接读取 `ts2price[latest_ts]`，时间复杂度 O(1)。  
3. **最大值** 用一个**最大堆**（Python `heapq` 只支持最小堆，最大堆可以把价格取负数）保存 `(price, timestamp)`。  
4. **最小值** 用一个**最小堆**保存 `(price, timestamp)`。  

> **惰性删除（lazy deletion）**：  
> 当我们对同一个时间戳多次 `update`，旧的 `(price, timestamp)` 仍然留在堆里。我们不在 `update` 时去遍历堆把旧元素删掉（那会是 O(n)），而是在查询 `maximum`/`minimum` 时“弹出”堆顶，检查它是否仍然和哈希表里对应的最新价格一致。如果不一致，说明它是过期的，直接丢弃，继续弹出下一个，直到堆顶是有效的。这样每个元素最多被弹出一次，总体仍是 O(log n) 的摊销复杂度。  

**类比**：想象堆是一个装满了“旧报纸”的箱子，我们只在需要最新新闻时才把箱子顶上的报纸取出来检查，如果是旧报纸就扔掉，继续取，直到拿到最新的。  

#### 代码（Python）  
```python
import heapq

class StockPrice:
    def __init__(self):
        # timestamp -> latest price
        self.ts2price = {}

        # 记录出现过的最大时间戳，方便 O(1) 取 current
        self.latest_ts = -1

        # 最大堆：存 ( -price , timestamp )
        self.max_heap = []          # Python 没有原生最大堆，用负数模拟

        # 最小堆：存 ( price , timestamp )
        self.min_heap = []

    def update(self, timestamp: int, price: int) -> None:
        """更新或插入一条记录"""
        self.ts2price[timestamp] = price          # 哈希表直接覆盖

        # 维护最新时间戳
        if timestamp > self.latest_ts:
            self.latest_ts = timestamp

        # 把新记录压入两个堆
        heapq.heappush(self.max_heap, (-price, timestamp))  # 负号实现最大堆
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self) -> int:
        """返回最新时间戳对应的价格，时间 O(1)"""
        return self.ts2price[self.latest_ts]

    def maximum(self) -> int:
        """堆顶可能是过期的，需要惰性删除"""
        while self.max_heap:
            neg_price, ts = self.max_heap[0]       # 看堆顶但不弹出
            price = -neg_price
            # 如果堆顶记录仍然是最新的 price，则返回
            if self.ts2price.get(ts) == price:
                return price
            # 否则说明是旧记录，弹出丢弃
            heapq.heappop(self.max_heap)
        # 按题意这里不会到达
        return -1

    def minimum(self) -> int:
        """同 maximum，只是最小堆"""
        while self.min_heap:
            price, ts = self.min_heap[0]
            if self.ts2price.get(ts) == price:
                return price
            heapq.heappop(self.min_heap)
        return -1
```

#### 复杂度  
- **时间复杂度**  
  - `update`：向两个堆各插入一次，都是 `O(log n)`，哈希表写入是 `O(1)`，整体 `O(log n)`。  
  - `current`：直接读取 `latest_ts`，`O(1)`。  
  - `maximum` / `minimum`：每次最多弹出几个已经过期的元素。每个元素只会被弹出一次，摊销下来仍是 `O(log n)`。  
  - 与暴力解相比，查询不再是 `O(n)`，而是对数级别，几乎可以忽略不计。  

- **空间复杂度**  
  - 哈希表保存每个时间戳最新的价格：`O(n)`。  
  - 两个堆中会保留所有插入过的记录（包括过期的），最坏情况下也是 `O(n)`。  
  - 总体 `O(n)`，与暴力解相同，但时间效率大幅提升。  

---  

## 心得  

- **核心技巧**：**哈希表 + 双堆 + 惰性删除**。  
- 这种组合特别适合“**需要快速查询最大/最小且会有更新**”的场景。  

**类似题目**（可以练习相同思路）：  
1. **设计一个支持插入、删除、获取中位数的数据结构**（LeetCode 295）——使用两个堆。  
2. **滑动窗口最大值**（LeetCode 239）——使用单调双端队列（也是一种“堆化”思路）。  
3. **设计推文存储系统**（LeetCode 355）——需要维护时间戳的最大值，思路类似。  

**一句话总结**：  
> “把所有历史记录都放进堆里，只在查询时把‘旧报纸’扔掉，即可在对数时间得到最新的最大/最小价格”。  

---  

## 反思  

- **第一反应**：直接把所有记录保存下来，查询时遍历，想到 “暴力” 方案。  
- **最容易踩的坑**  
  1. **重复时间戳的覆盖**：后来的记录必须覆盖前面的价格，否则会导致错误的最大/最小值。  
  2. **堆的过期元素**：忘记在 `maximum` / `minimum` 时进行惰性删除，会返回已经被更新的旧价格。  
  3. **最新时间戳的维护**：如果只在 `update` 时更新 `latest_ts`，而不比较大小，`current` 会出错。  

- **下次遇到同类题**，第一步应该思考：  
  - “哪些操作需要**快速查询**（最大/最小/中位数）？”  
  - “数据会被**修改**吗？如果会，能否用**懒删**的方式避免每次都遍历？”  
  - 然后挑选合适的 **堆**（或平衡树）配合 **哈希表** 实现。