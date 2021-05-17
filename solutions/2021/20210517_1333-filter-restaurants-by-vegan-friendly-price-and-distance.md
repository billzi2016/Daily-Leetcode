# #1333. 按素食友好度、价格和距离过滤餐厅 / Filter Restaurants by Vegan-Friendly, Price and Distance

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/filter-restaurants-by-vegan-friendly-price-and-distance/)

---

## 题目（英文原版）

**Description**

Given the array restaurants where  restaurants[i] = [idi, ratingi, veganFriendlyi, pricei, distancei]. You have to filter the restaurants using three filters.
The veganFriendly filter will be either true (meaning you should only include restaurants with veganFriendlyi set to true) or false (meaning you can include any restaurant). In addition, you have the filters maxPrice and maxDistance which are the maximum value for price and distance of restaurants you should consider respectively.
Return the array of restaurant IDs after filtering, ordered by rating from highest to lowest. For restaurants with the same rating, order them by id from highest to lowest. For simplicity veganFriendlyi and veganFriendly take value 1 when it is true, and 0 when it is false.

**Examples**

**Example 1:**

```
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]], veganFriendly = 1, maxPrice = 50, maxDistance = 10
Output: [3,1,5] 
Explanation: 
The restaurants are:
Restaurant 1 [id=1, rating=4, veganFriendly=1, price=40, distance=10]
Restaurant 2 [id=2, rating=8, veganFriendly=0, price=50, distance=5]
Restaurant 3 [id=3, rating=8, veganFriendly=1, price=30, distance=4]
Restaurant 4 [id=4, rating=10, veganFriendly=0, price=10, distance=3]
Restaurant 5 [id=5, rating=1, veganFriendly=1, price=15, distance=1] 
After filter restaurants with veganFriendly = 1, maxPrice = 50 and maxDistance = 10 we have restaurant 3, restaurant 1 and restaurant 5 (ordered by rating from highest to lowest).
```

**Example 2:**

```
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]], veganFriendly = 0, maxPrice = 50, maxDistance = 10
Output: [4,3,2,1,5]
Explanation: The restaurants are the same as in example 1, but in this case the filter veganFriendly = 0, therefore all restaurants are considered.
```

**Example 3:**

```
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]], veganFriendly = 0, maxPrice = 30, maxDistance = 3
Output: [4,5]
```

**Constraints**

- 1 <= restaurants.length <= 10^4
- restaurants[i].length == 5
- 1 <= idi, ratingi, pricei, distancei <= 10^5
- 1 <= maxPrice, maxDistance <= 10^5
- veganFriendlyi and veganFriendly are 0 or 1.
- All idi are distinct.

---

## 题目（中文翻译）

**题目描述**  
给定数组 `restaurants`，其中 `restaurants[i] = [idi, ratingi, veganFriendlyi, pricei, distancei]`。请使用以下三个过滤条件对餐厅进行筛选：

1. **veganFriendly** 过滤器的取值为 `true`（表示只保留 `veganFriendlyi` 为 `true` 的餐厅）或 `false`（表示可以保留任意餐厅）。  
2. `maxPrice` 为价格上限，只保留 `pricei ≤ maxPrice` 的餐厅。  
3. `maxDistance` 为距离上限，只保留 `distancei ≤ maxDistance` 的餐厅。

返回筛选后餐厅的 **id** 列表，排序规则为：
- 先按 `rating` 从高到低排序；
- 若 `rating` 相同，则按 `id` 从高到低排序。

为简化起见，`veganFriendlyi` 与 `veganFriendly` 为 `true` 时取值 `1`，为 `false` 时取值 `0`。

**示例 1**  
```text
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]],
       veganFriendly = 1, maxPrice = 50, maxDistance = 10
Output: [3,1,5]
```
**解释**  
餐厅信息如下：
- 餐厅 1: `[id=1, rating=4, veganFriendly=1, price=40, distance=10]`
- 餐厅 2: `[id=2, rating=8, veganFriendly=0, price=50, distance=5]`
- 餐厅 3: `[id=3, rating=8, veganFriendly=1, price=30, distance=4]`
- 餐厅 4: `[id=4, rating=10, veganFriendly=0, price=10, distance=3]`
- 餐厅 5: `[id=5, rating=1, veganFriendly=1, price=15, distance=1]`

因为 `veganFriendly = 1`，只保留 `veganFriendlyi = 1` 的餐厅 → {1,3,5}。  
再依据 `price ≤ 50` 与 `distance ≤ 10`，这三家都满足条件。  
按照 `rating` 降序排列，若相同则 `id` 降序，得到 `[3,1,5]`。

**示例 2**  
```text
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]],
       veganFriendly = 0, maxPrice = 50, maxDistance = 10
Output: [4,3,2,1,5]
```
**解释**  
`veganFriendly = 0` 表示不进行素食友好度过滤，所有餐厅均被考虑。  
在满足 `price ≤ 50` 且 `distance ≤ 10` 的前提下，按照 `rating`（10、8、8、4、1）以及 `id`（相同 rating 时 id 降序）排序，得到 `[4,3,2,1,5]`。

**示例 3**  
```text
Input: restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]],
       veganFriendly = 0, maxPrice = 30, maxDistance = 3
Output: [4,5]
```
**解释**  
此时只保留 `price ≤ 30` 且 `distance ≤ 3` 的餐厅 → 餐厅 4 与餐厅 5。  
按照 `rating` 降序得到 `[4,5]`。

**约束条件**  
- `1 ≤ restaurants.length ≤ 10^4`  
- `restaurants[i].length == 5`  
- `1 ≤ idi, ratingi, pricei, distancei ≤ 10^5`  
- `1 ≤ maxPrice, maxDistance ≤ 10^5`  
- `veganFriendlyi` 与 `veganFriendly` 只能取 `0` 或 `1`  
- 所有 `idi` 均互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **遍历所有餐厅**，把每一家都拿出来检查它是否满足三个条件：  
   - `veganFriendly` 是否等于题目给出的 `veganFriendly`（如果要求只能是素食友好，则只保留 `veganFriendly==1` 的餐厅）。  
   - `price` ≤ `maxPrice`。  
   - `distance` ≤ `maxDistance`。  
   这一步类似于在超市里 **逐个检查商品标签**，看它们是不是我们想要的。

2. 把所有满足条件的餐厅 **放进一个新列表**，每个元素仍然是 `[id, rating, ...]`。

3. 对这个新列表 **手动排序**：  
   - 先比较 `rating`（评分），大的排在前面。  
   - 如果评分相同，再比较 `id`，大的排在前面。  

   这里可以使用最容易想到的 **冒泡排序**（两两比较、不断交换），因为它实现最简单，完全符合“暴力”二字。  
   冒泡排序可以想象成 **把最重的箱子不停地往上“冒”**，直到整个队列从大到小。

4. 最后把排好序的餐厅的 `id` 按顺序取出来返回。

> **为什么这样一定对？**  
> - 第 1 步把所有满足筛选条件的餐厅全部收集，没有遗漏。  
> - 第 2 步的冒泡排序会把列表按照我们要求的顺序（先 rating 再 id）彻底排好。冒泡排序的原理保证了所有元素最终都会按照比较规则从大到小排列。

#### 代码（Python）

```python
def filterRestaurants(restaurants, veganFriendly, maxPrice, maxDistance):
    # 1. 过滤：把符合条件的餐厅挑出来
    filtered = []
    for r in restaurants:                     # r = [id, rating, vegan, price, distance]
        id_, rating, vegan, price, dist = r
        # 判断三个过滤条件
        if (veganFriendly == 0 or vegan == 1) and price <= maxPrice and dist <= maxDistance:
            filtered.append(r)                # 符合就放进 filtered

    # 2. 暴力排序：冒泡排序（O(n^2)）
    n = len(filtered)
    for i in range(n):                         # 外层循环控制轮数
        for j in range(0, n - i - 1):          # 内层两两比较相邻元素
            # 先比较 rating，rating 大的应该在前面
            if filtered[j][1] < filtered[j + 1][1]:
                filtered[j], filtered[j + 1] = filtered[j + 1], filtered[j]
            # rating 相同再比较 id，id 大的在前面
            elif filtered[j][1] == filtered[j + 1][1] and filtered[j][0] < filtered[j + 1][0]:
                filtered[j], filtered[j + 1] = filtered[j + 1], filtered[j]

    # 3. 只返回 id
    return [r[0] for r in filtered]
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 过滤本身是一次遍历，`O(n)`。  
  - 冒泡排序最坏需要比较 `n*(n-1)/2` 次，约等于 `n²/2`，所以整体是二次方级别。  
  - 用大白话说，就是如果餐厅有 10,000 家，排序大概要做 100,000,000 次比较，显得很慢。

- **空间复杂度**：`O(n)`  
  - 额外用了一个 `filtered` 列表来存放满足条件的餐厅，最坏情况下它会装下所有 `n` 家餐厅。  
  - 其它变量都是常数级别的。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于排序：我们用了冒泡排序，时间是 `O(n²)`，这在 `n` 达到 10⁴ 时会明显超时。  
排序其实可以交给 Python 内置的 **Timsort**（实现于 `list.sort()` 与 `sorted()`），它的时间复杂度是 `O(n log n)`，在实际数据规模下非常快。

优化思路如下：

1. **过滤** 步仍然保持一次遍历 `O(n)`，因为每家餐厅只能检查一次，已经是最优的线性时间。  
2. **排序** 使用 Python 的 `sorted`，并提供 **自定义键**（key）来一次性表达 “先 rating 降序、再 id 降序”。  
   - `key=lambda x: (-x[1], -x[0])`：  
     - `-x[1]` 把 rating 变成负数，使得默认的升序变成 **降序**。  
     - 同理 `-x[0]` 把 id 也变成降序。  
   - 这就像在 **把餐厅先按照“分数高低”排好队，再在相同分数的组里按“编号大小”重新排**，一次搞定。
3. 最后 **提取 id**，返回结果。

> **为什么这样更好？**  
> - 过滤仍是一次遍历，已经最优。  
> - Python 的 Timsort 在最坏情况下是 `O(n log n)`，比冒泡的 `O(n²)` 快得多。  
> - 使用 `sorted` 的 `key` 参数可以一次表达多层排序规则，代码简洁且易读。

#### 代码（Python）

```python
def filterRestaurants(restaurants, veganFriendly, maxPrice, maxDistance):
    """
    最优解：一次遍历过滤 + 内置排序（O(n log n)）
    """
    # 1. 过滤：满足所有条件的餐厅留下
    filtered = [
        r for r in restaurants
        if (veganFriendly == 0 or r[2] == 1)      # veganFriendly 过滤
        and r[3] <= maxPrice                      # 价格过滤
        and r[4] <= maxDistance                   # 距离过滤
    ]

    # 2. 排序：先 rating 降序，再 id 降序
    # key 使用负数实现降序，sorted 默认升序
    filtered.sort(key=lambda x: (-x[1], -x[0]))

    # 3. 只返回 id 列表
    return [r[0] for r in filtered]
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 过滤一次遍历 `O(n)`。  
  - `list.sort`（或 `sorted`）的时间复杂度是 `O(m log m)`，其中 `m` 是过滤后剩余的餐厅数量，`m ≤ n`。  
  - 所以整体是线性遍历 + 排序，最耗时的部分是 `O(n log n)`，这在 10⁴ 的规模下几乎是瞬间完成。

- **空间复杂度**：`O(n)`  
  - 需要额外存放过滤后的列表 `filtered`，最坏情况仍然是 `n` 条记录。  
  - `sort` 是原地排序，只使用常数级的额外空间（Python 的 Timsort 会用到 `O(n)` 的临时空间，但仍然在同数量级）。

---

## 心得

- **核心技巧**：一次遍历完成过滤 + 利用内置排序的自定义键实现多关键字的降序排列。  
- **适用的题型**：  
  1. “按多个属性排序并返回子集”——如 LeetCode 1337. The K Weakest Rows in a Matrix（先统计再排序）。  
  2. “筛选后排序”——如 1641. Count Sorted Vowel Strings（统计后按字典序）。  
  3. “自定义排序规则”——如 1561. Maximum Number of Coins You Can Get（先按价值排序）。  
- **一句话总结**：**过滤 + O(n log n) 排序是大多数“筛选后排序”题目的通用钥匙**。

---

## 反思

- **第一反应**：看到有 “过滤” 与 “排序” 两个关键词，立刻想到先遍历筛选，再用排序函数把结果排好。  
- **最容易踩的坑**：  
  - 忘记 `veganFriendly` 为 `0` 时**不需要**筛选素食友好餐厅。  
  - 排序时把 **rating 降序** 写成 **升序**，导致输出顺序错误。  
  - 直接返回完整的餐厅信息而不是仅返回 `id`。  
- **下次遇到同类题**：第一步先 **明确过滤条件**，把它们写成列表推导式；第二步考虑 **排序键的组合**（使用负号或 `reverse=True`），最后再 **提取需要的字段**。这样思路清晰、实现也自然。