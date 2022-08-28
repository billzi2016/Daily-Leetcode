# #1912. 电影租赁系统设计 / Design Movie Rental System

> 难度：困难 · 标签：Array、Hash Table、Design、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/design-movie-rental-system/)

---

## 题目（英文原版）

**Description**

You have a movie renting company consisting of n shops. You want to implement a renting system that supports searching for, booking, and returning movies. The system should also support generating a report of the currently rented movies.
Each movie is given as a 2D integer array entries where entries[i] = [shopi, moviei, pricei] indicates that there is a copy of movie moviei at shop shopi with a rental price of pricei. Each shop carries at most one copy of a movie moviei.
The system should support the following functions:
Implement the MovieRentingSystem class:
Note: The test cases will be generated such that rent will only be called if the shop has an unrented copy of the movie, and drop will only be called if the shop had previously rented out the movie.

**Examples**

**Example 1:**

```
Input
["MovieRentingSystem", "search", "rent", "rent", "report", "drop", "search"]
[[3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]]], [1], [0, 1], [1, 2], [], [1, 2], [2]]
Output
[null, [1, 0, 2], null, null, [[0, 1], [1, 2]], null, [0, 1]]

Explanation
MovieRentingSystem movieRentingSystem = new MovieRentingSystem(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]]);
movieRentingSystem.search(1);  // return [1, 0, 2], Movies of ID 1 are unrented at shops 1, 0, and 2. Shop 1 is cheapest; shop 0 and 2 are the same price, so order by shop number.
movieRentingSystem.rent(0, 1); // Rent movie 1 from shop 0. Unrented movies at shop 0 are now [2,3].
movieRentingSystem.rent(1, 2); // Rent movie 2 from shop 1. Unrented movies at shop 1 are now [1].
movieRentingSystem.report();   // return [[0, 1], [1, 2]]. Movie 1 from shop 0 is cheapest, followed by movie 2 from shop 1.
movieRentingSystem.drop(1, 2); // Drop off movie 2 at shop 1. Unrented movies at shop 1 are now [1,2].
movieRentingSystem.search(2);  // return [0, 1]. Movies of ID 2 are unrented at shops 0 and 1. Shop 0 is cheapest, followed by shop 1.
```

**Constraints**

- 1 <= n <= 3 * 105
- 1 <= entries.length <= 105
- 0 <= shopi < n
- 1 <= moviei, pricei <= 104
- Each shop carries at most one copy of a movie moviei.
- At most 105 calls in total will be made to search, rent, drop and report.

---

## 题目（中文翻译）

**描述**  
你拥有一家拥有 `n` 家门店的电影租赁公司。需要实现一个租赁系统，支持以下操作：

* **search**：查询某部电影在未被租出的门店中，租金最低的 **3** 家门店编号（若不足 3 家则返回全部），并按租金从低到高排序；若租金相同，则按门店编号升序排列。  
* **rent**：在指定的门店租出一部电影。  
* **drop**：归还在指定门店租出的电影，使其再次可供租赁。  
* **report**：返回当前所有已被租出的电影信息，按租金从低到高排序；若租金相同，则先按门店编号升序，再按电影编号升序。每条信息为 `[shop, movie]`。

系统的初始化由 `MovieRentingSystem` 类完成，构造函数接收：

* `n`：门店数量  
* `entries`：二维整数数组，其中 `entries[i] = [shop_i, movie_i, price_i]` 表示门店 `shop_i` 有一部电影 `movie_i`，租金为 `price_i`。每家门店对同一部电影至多只有一份拷贝。

> **注意**：测试用例保证 `rent` 只会在该门店拥有未被租出的该电影拷贝时调用，`drop` 只会在该门店之前已经租出该电影时调用。

---

### 示例

**输入**  

```json
["MovieRentingSystem", "search", "rent", "rent", "report", "drop", "search"]
[[3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]]], [1], [0, 1], [1, 2], [], [1, 2], [2]]
```

**输出**  

```json
[null, [1, 0, 2], null, null, [[0, 1], [1, 2]], null, [0, 1]]
```

**解释**  

```java
MovieRentingSystem movieRentingSystem = new MovieRentingSystem(
    3,
    [[0, 1, 5], [0, 2, 6], [0, 3, 7],
     [1, 1, 4], [1, 2, 7],
     [2, 1, 5]]
);
movieRentingSystem.search(1); // 返回 [1, 0, 2]
movieRentingSystem.rent(0, 1); // 租出门店 0 的电影 1
movieRentingSystem.rent(1, 2); // 租出门店 1 的电影 2
movieRentingSystem.report();   // 返回 [[0, 1], [1, 2]]
movieRentingSystem.drop(1, 2); // 归还门店 1 的电影 2
movieRentingSystem.search(2); // 返回 [0, 1]
```

---

### 约束条件

* `1 <= n <= 3 * 10^5`
* `1 <= entries.length <= 10^5`
* `0 <= shop_i < n`
* `1 <= movie_i, price_i <= 10^4`
* 每家门店对同一部电影至多只有一份拷贝
* `search`、`rent`、`drop`、`report` 四类函数的调用总次数不超过 `10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有电影拷贝 **一次性** 存在一个大列表里，后面的每一次操作都在这份列表上遍历：

* **search(movie)**  
  - 逐个检查列表，找出 `movie` 且 **未被租出的** 拷贝。  
  - 把它们按 `price`（价格）升序、`shop`（店铺编号）升序排好序，取前 5 个店铺编号返回。

* **rent(shop, movie)**  
  - 再次遍历列表，找到对应的 `(shop, movie)`，把它的状态标记为 “已租出”。  

* **drop(shop, movie)**  
  - 同上，把状态改回 “未租出”。  

* **report()**  
  - 遍历列表，收集所有 **已租出** 的拷贝，按 `price → shop → movie` 的顺序排序，返回前 5 条 `[shop, movie]`。

> **类比**：把所有拷贝想象成一本巨大的电话簿，想找某部电影就得把整本电话簿翻一遍，找不到的记录也要逐页翻过去。

#### 代码（Python）

```python
import collections

class MovieRentingSystem:
    def __init__(self, n, entries):
        """
        n      : 店铺数量（本解法不需要用到）
        entries: [[shop, movie, price], ...]
        """
        # 把所有拷贝放进一个大列表，每条记录用字典保存状态
        self.all = []                     # 存放所有拷贝
        self.idx = {}                     # (shop, movie) -> 在 self.all 中的下标，便于快速定位
        for i, (shop, movie, price) in enumerate(entries):
            rec = {"shop": shop, "movie": movie, "price": price, "rented": False}
            self.all.append(rec)
            self.idx[(shop, movie)] = i

    def search(self, movie):
        """返回未租出的、价格最便宜的最多 5 家店铺编号"""
        candidates = []
        for rec in self.all:
            if rec["movie"] == movie and not rec["rented"]:
                candidates.append((rec["price"], rec["shop"]))
        # 按价格、店铺编号排序
        candidates.sort()
        # 只取前 5 家
        return [shop for _, shop in candidates[:5]]

    def rent(self, shop, movie):
        """把 (shop, movie) 标记为已租出"""
        i = self.idx[(shop, movie)]
        self.all[i]["rented"] = True

    def drop(self, shop, movie):
        """把 (shop, movie) 标记为未租出"""
        i = self.idx[(shop, movie)]
        self.all[i]["rented"] = False

    def report(self):
        """返回已租出的、价格最便宜的最多 5 条 [shop, movie]"""
        rented = []
        for rec in self.all:
            if rec["rented"]:
                rented.append((rec["price"], rec["shop"], rec["movie"]))
        rented.sort()
        return [[shop, movie] for _, shop, movie in rented[:5]]
```

#### 复杂度

| 操作      | 时间复杂度 | 空间复杂度 | 含义解释 |
|-----------|------------|------------|----------|
| `search`  | **O(m)**   | **O(1)**   | 需要遍历所有拷贝（`m = entries.length`），相当于“一次性把所有书都翻一遍”。 |
| `rent`/`drop` | **O(1)**   | **O(1)**   | 直接通过哈希表定位下标，改一个布尔值，像在字典里改一个键的值，时间几乎不变。 |
| `report`  | **O(m log m)**（先收集再排序）| **O(1)**   | 同样要遍历全部拷贝，然后排序，最坏情况相当于把所有电影的租金排一次序。 |

> 对于 **`entries.length ≤ 10⁵`、调用次数 ≤ 10⁵** 的限制，这种 **O(m)** 的遍历在最坏情况下会导致 **10⁵ × 10⁵ = 10¹⁰** 次操作，显然会超时。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **每一次 `search` / `report` 都要遍历全部拷贝**。  
我们需要 **按电影、按租出状态分组**，并且 **保持每组内部有序**，这样查询只在相关小集合里进行。

核心思路：

1. **每部电影维护一个“可租拷贝”小根堆**（最小堆），堆的元素是 `(price, shop)`。  
   - 堆天然保证“价格最小 → 店铺编号最小”。  
   - 堆的大小等于这部电影当前**未租出的**拷贝数，通常远小于全部拷贝数。

2. **所有已租出的拷贝统一放进另一个全局小根堆**，元素是 `(price, shop, movie)`。  
   - `report` 只需要从这堆里弹出前 5 条即可。

3. **懒删（lazy deletion）**：  
   - 当一部拷贝被租出时，我们 **不在原堆里删除**（删除堆中间元素在 Python 标准库里不方便），而是把它的状态标记为 “已租”。  
   - 以后在 `search` 或 `report` 中弹出堆顶时，若发现该拷贝已经不符合当前状态，就直接丢弃并继续弹出。  
   - 这类似“把过期的报纸撕掉”，只在需要时才清理。

4. **状态表**：用一个字典 `state[(shop, movie)] = (price, rented_flag)` 保存每个拷贝的价格和是否已租。这样可以在 O(1) 时间判断堆顶元素是否“过期”。

> **类比**：  
> - “可租拷贝堆”好比每部电影的“待售商品清单”，最便宜的商品永远排在最前面。  
> - “已租拷贝堆”好比公司的“已成交订单列表”，同样按价格从低到高排列。  
> - “懒删”就像超市的自动收银机：当商品被买走后，系统不立刻把它从货架上搬走，而是等下次顾客来挑选时再发现它已经缺货并跳过。

#### 代码（Python）

```python
import heapq
import collections

class MovieRentingSystem:
    def __init__(self, n, entries):
        """
        n      : 店铺数量（仅用于约束，不参与逻辑）
        entries: [[shop, movie, price], ...]
        """
        # ---------- 1. 记录每部电影的可租拷贝堆 ----------
        # movie_id -> min-heap of (price, shop)
        self.available = collections.defaultdict(list)

        # ---------- 2. 记录已租出的拷贝的全局堆 ----------
        # heap of (price, shop, movie)
        self.rented = []

        # ---------- 3. 状态表： (shop, movie) -> [price, rented_flag] ----------
        # 用 list 而不是 tuple，后面需要修改 rented_flag
        self.state = {}

        for shop, movie, price in entries:
            # 把拷贝加入对应电影的可租堆
            heapq.heappush(self.available[movie], (price, shop))
            # 初始化状态为 “未租出”
            self.state[(shop, movie)] = [price, False]

    # ---------- 4. 搜索未租出的最便宜店铺 ----------
    def search(self, movie):
        """
        返回未租出的、价格最便宜的最多 5 家店铺编号（升序）
        """
        res = []
        heap = self.available[movie]

        # 临时保存弹出的合法元素，后面要放回堆中
        temp = []

        while heap and len(res) < 5:
            price, shop = heapq.heappop(heap)
            # 查看当前拷贝是否真的未租出（可能已经被租走了，属于“懒删”）
            if not self.state[(shop, movie)][1]:          # 未租
                res.append(shop)
                temp.append((price, shop))                # 这条合法记录要放回堆
            # 若已经租出，则直接丢弃，不放回

        # 把合法的元素重新压回堆，保证后续操作不受影响
        for item in temp:
            heapq.heappush(heap, item)

        return res

    # ---------- 5. 租出一部电影 ----------
    def rent(self, shop, movie):
        """
        把 (shop, movie) 标记为已租出，并放入全局已租堆
        """
        price, _ = self.state[(shop, movie)]
        self.state[(shop, movie)][1] = True               # 标记为已租
        heapq.heappush(self.rented, (price, shop, movie))

    # ---------- 6. 归还一部电影 ----------
    def drop(self, shop, movie):
        """
        把 (shop, movie) 标记为未租出，并重新放回对应电影的可租堆
        """
        price, _ = self.state[(shop, movie)]
        self.state[(shop, movie)][1] = False              # 标记为未租
        heapq.heappush(self.available[movie], (price, shop))

    # ---------- 7. 报告已租出的最便宜拷贝 ----------
    def report(self):
        """
        返回已租出的、价格最便宜的最多 5 条 [shop, movie]（升序）
        """
        res = []
        temp = []

        while self.rented and len(res) < 5:
            price, shop, movie = heapq.heappop(self.rented)
            # 只保留仍然处于“已租出”状态的拷贝
            if self.state[(shop, movie)][1]:              # 仍然租着
                res.append([shop, movie])
                temp.append((price, shop, movie))
            # 否则说明这条记录已经被 drop，直接丢弃

        # 把合法的记录重新压回堆
        for item in temp:
            heapq.heappush(self.rented, item)

        return res
```

#### 复杂度

| 操作      | 时间复杂度 | 空间复杂度 | 含义解释 |
|-----------|------------|------------|----------|
| `search`  | **O(k log k)**，`k` 为该电影当前未租出的拷贝数（最多弹出 5 次） | **O(1)**（不计返回列表） | 只在对应电影的堆里操作，堆的大小远小于全部拷贝数。弹出/压入一次是 `log k`，最多 5 次，几乎是常数级。 |
| `rent`    | **O(log R)**，`R` 为已租拷贝总数 | **O(1)** | 向全局已租堆插入一个元素，需要 `log R` 的时间。 |
| `drop`    | **O(log k)**，`k` 为该电影当前可租拷贝数 | **O(1)** | 向对应电影的可租堆插入一个元素，需要 `log k` 的时间。 |
| `report`  | **O(5 log R)**（最多弹出 5 次） | **O(1)** | 同 `search`，只在已租堆里操作，堆的大小为已租拷贝数 `R`，`log R` 通常也很小。 |

> 与暴力解相比，**每次查询只在相关的小集合里进行**，时间从 `O(m)` 降到了 `O(log m)` 量级，足以通过 10⁵ 次调用的时间限制。

---

## 心得

- **核心技巧**：**为每类数据维护有序的堆（或有序集合） + 懒删**。  
- **适用场景**：  
  1. “在动态集合中找最小/最大元素” 如 **Design Parking System**、**Design Food Delivery System**。  
  2. “需要频繁删除/插入并保持有序” 如 **Find the Kth Smallest Pair Distance**、**Smallest Number in Infinite Set**。  
- **一句话总结**：**把“全局遍历”拆成“局部有序堆”，用懒删把删除操作变得轻量”。**

---

## 反思

- **第一反应**：看到 `search`、`report` 要返回“价格最便宜的前 K 条”，立刻想到 **排序**，于是想每次遍历后再排序——这就是暴力解。  
- **最容易踩的坑**：  
  * **懒删忘记在 `search` / `report` 时把已经失效的堆顶弹掉**，会导致返回已被租出的拷贝。  
  * **返回的顺序必须是“先价格，再店铺/电影编号”**，堆的键要写成 `(price, shop, movie)`，否则排序会出错。  
  * **边界条件**：某部电影根本没有可租拷贝时 `search` 要返回空列表；已租拷贝为空时 `report` 也要返回空列表。  
- **下次思路**：看到“返回前 K 小/大” → **立刻考虑** “**使用堆（优先队列）**”。若还有 “状态会在两种集合之间切换”，就 **用同一个状态表+懒删** 来避免在堆里做复杂的删除操作。