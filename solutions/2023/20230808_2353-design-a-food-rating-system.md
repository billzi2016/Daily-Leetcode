# #2353. **食物评分系统** / Design a Food Rating System

> 难度：中等 · 标签：Array、Hash Table、String、Design、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/design-a-food-rating-system/)

---

## 题目（英文原版）

**Description**

Design a food rating system that can do the following:
Implement the FoodRatings class:
Note that a string x is lexicographically smaller than string y if x comes before y in dictionary order, that is, either x is a prefix of y, or if i is the first position such that x[i] != y[i], then x[i] comes before y[i] in alphabetic order.

**Examples**

**Example 1:**

```
Input
["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", "changeRating", "highestRated"]
[[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]], ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], ["japanese"]]
Output
[null, "kimchi", "ramen", null, "sushi", null, "ramen"]

Explanation
FoodRatings foodRatings = new FoodRatings(["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]);
foodRatings.highestRated("korean"); // return "kimchi"
                                    // "kimchi" is the highest rated korean food with a rating of 9.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // "ramen" is the highest rated japanese food with a rating of 14.
foodRatings.changeRating("sushi", 16); // "sushi" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "sushi"
                                      // "sushi" is the highest rated japanese food with a rating of 16.
foodRatings.changeRating("ramen", 16); // "ramen" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // Both "sushi" and "ramen" have a rating of 16.
                                      // However, "ramen" is lexicographically smaller than "sushi".
```

**Constraints**

- 1 <= n <= 2 * 104
- n == foods.length == cuisines.length == ratings.length
- 1 <= foods[i].length, cuisines[i].length <= 10
- foods[i], cuisines[i] consist of lowercase English letters.
- 1 <= ratings[i] <= 108
- All the strings in foods are distinct.
- food will be the name of a food item in the system across all calls to changeRating.
- cuisine will be a type of cuisine of at least one food item in the system across all calls to highestRated.
- At most 2 * 104 calls in total will be made to changeRating and highestRated.

---

## 题目（中文翻译）

设计一个食物评分系统，使其能够完成以下操作：

实现 `FoodRatings` 类：

- `FoodRatings(String[] foods, String[] cuisines, int[] ratings)`  
  初始化系统。`foods[i]` 是第 `i` 种食物的名称，`cuisines[i]` 是该食物所属的料理类型，`ratings[i]` 是该食物的初始评分。

- `void changeRating(String food, int newRating)`  
  将名称为 `food` 的食物的评分更改为 `newRating`。题目保证 `food` 必定已存在于系统中。

- `String highestRated(String cuisine)`  
  返回指定料理类型 `cuisine` 中评分最高的食物名称。若存在多个食物拥有相同的最高评分，则返回字典序（lexicographically）最小的那个。字典序的定义：字符串 `x` 在字典序上小于字符串 `y`，当且仅当 `x` 是 `y` 的前缀，或在第一次出现不同字符的位置 `i` 上，`x[i]` 在字母表中位于 `y[i]` 前面。

---

### 示例

```text
输入
["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", "changeRating", "highestRated"]
[[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
  ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
  [9, 12, 8, 15, 14, 7]],
 ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], ["japanese"]]
输出
[null, "kimchi", "ramen", null, "sushi", null, "ramen"]
```

**解释**

1. 初始化系统后，`korean` 料理中评分最高的食物是 `"kimchi"`（评分 9），`japanese` 料理中最高的是 `"ramen"`（评分 14）。
2. 调用 `changeRating("sushi", 16)` 后，`sushi` 的评分提升到 16，成为 `japanese` 料理中评分最高的食物。
3. 再次查询 `highestRated("japanese")`，返回 `"sushi"`。
4. 调用 `changeRating("ramen", 16)` 后，`ramen` 与 `sushi` 并列最高评分 16。因为在字典序上 `"ramen"` 小于 `"sushi"`，所以 `highestRated("japanese")` 返回 `"ramen"`。

---

### 约束

- `1 <= n <= 2 * 10^4`  
- `n == foods.length == cuisines.length == ratings.length`
- `1 <= foods[i].length, cuisines[i].length <= 10`
- `foods[i]`、`cuisines[i]` 只包含小写英文字母
- `1 <= ratings[i] <= 10^8`
- 所有 `foods[i]` 均互不相同
- `food` 在所有对 `changeRating` 的调用中必定是系统中已存在的食物名称
- `cuisine` 在所有对 `highestRated` 的调用中必定对应系统中至少一种食物的料理类型
- `changeRating` 与 `highestRated` 的总调用次数不超过 `2 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是把所有信息都放在一个大列表里，每次要查询 **某一类 cuisine** 里评分最高的食物时，就遍历整个列表，挑出属于该 cuisine 的所有食物，比较它们的 `rating`，如果分数相同再比较 `food` 的字典序（lexicographically），最后返回找到的食物名称。

> **数据结构类比**  
> - **列表** 就像一本电话簿，所有食物都排成一列。要找某个地区（cuisine）的电话，只能从头到尾逐行查看。  
> - **字典（哈希表）** 在这里我们暂时不使用，因为我们只想演示最“笨”的办法。

这个方法一定能得到正确答案，因为我们把 **所有可能的候选** 都检查了一遍，绝不会漏掉最高分的那一个。

#### 代码（Python）

```python
class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        """
        暴力实现：直接把所有信息存到一个列表里
        每个元素是 (food, cuisine, rating)
        """
        self.entries = []                     # 列表，存放所有食物信息
        for f, c, r in zip(foods, cuisines, ratings):
            self.entries.append([f, c, r])    # 用 list 便于后面修改 rating

    def changeRating(self, food: str, newRating: int) -> None:
        """
        把指定食物的评分改成 newRating
        只需要在列表里把对应的元素找到并改值
        """
        for entry in self.entries:            # 线性遍历寻找 food
            if entry[0] == food:              # 找到后直接修改 rating
                entry[2] = newRating
                break

    def highestRated(self, cuisine: str) -> str:
        """
        在所有属于该 cuisine 的食物中，找出 rating 最大、字典序最小的 food
        """
        best_food = None
        best_rating = -1

        for f, c, r in self.entries:         # 逐个检查
            if c != cuisine:                  # 只关注目标 cuisine
                continue
            # 先比较 rating；若相同再比较 food 的字典序
            if r > best_rating or (r == best_rating and f < best_food):
                best_food = f
                best_rating = r

        return best_food
```

#### 复杂度  

- **时间复杂度**  
  - `changeRating`：最坏情况需要遍历整个列表 → **O(n)**。  
  - `highestRated`：同样要遍历整个列表 → **O(n)**。  
  这里的 **O(n)** 只是一种“大写字母 N”的记号，表示“随食物数量线性增长”。如果有 10 000 个食物，操作大约要跑 10 000 次循环；如果是 100 000 个，就要跑 100 000 次，时间会明显变慢。  

- **空间复杂度**  
  - 只用了一个列表保存所有信息 → **O(n)**，即需要和食物数量相同的存储空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次查询 `highestRated` 都要 **遍历所有食物**，这在题目最多 2·10⁴ 次查询/修改的情况下会导致超时。我们需要把“查找最高评分的食物”这一步的成本从 **O(n)** 降到 **O(log n)** 或 **O(1)**。

**核心想法**：对每一种 cuisine，维护一个 **优先队列（堆）**，堆里保存该 cuisine 所有食物的 `(rating, food)`，堆顶永远是 rating 最大、且 rating 相同则 food 字典序最小的那一项。这样：

- `highestRated(cuisine)` 只要取对应堆的堆顶 → **O(1)**（取堆顶本身是常数时间）。
- `changeRating(food, newRating)` 需要把该食物在对应堆里“更新”。直接在堆里找并修改是困难的，于是采用 **懒删（lazy deletion）**：把新 `(newRating, food)` 再压进堆里，不立即删除旧的条目。随后在 `highestRated` 取堆顶时，如果堆顶的 rating 已经不是当前最新的（通过一个全局的 `food -> rating` 哈希表检查），就把它弹出（pop）并继续检查下一个堆顶，直到堆顶是“最新”的为止。

**所需数据结构**：

| 结构 | 作用 | 类比 |
|------|------|------|
| `food2cuisine`（字典） | 给食物名字快速找到它所属的 cuisine | 像查字典的“词条”，key 是食物名，value 是 cuisine |
| `food2rating`（字典） | 给食物名字快速找到它当前的 rating | 像查字典的“页码”，随时能得到最新分数 |
| `cuisine2heap`（字典 → 堆） | 对每个 cuisine 维护一个最大堆，元素是 `(-rating, food)`（负号让 Python 的最小堆变成最大堆） | 想象每种 cuisine 都有一个“排行榜”，最高分的食物总是排在最前面 |

**步骤细化**：

1. **构造函数**  
   - 把每个食物的信息分别填进 `food2cuisine`、`food2rating`。  
   - 同时把 `(-rating, food)` 放进对应 cuisine 的堆里。

2. **changeRating**  
   - 更新 `food2rating[food] = newRating`。  
   - 通过 `food2cuisine` 找到该食物的 cuisine，向该 cuisine 的堆再压入 `(-newRating, food)`。旧的条目仍留在堆里，稍后会在查询时被丢弃。

3. **highestRated**  
   - 取出对应 cuisine 的堆 `heap`。  
   - 循环检查堆顶 `(-r, f)`：  
     - 用 `food2rating[f]` 取最新的 rating `cur`.  
     - 若 `cur == -r`，说明堆顶是最新的，直接返回 `f`。  
     - 否则堆顶是“过时条目”，执行 `heapq.heappop(heap)` 把它弹出，继续检查下一个。  
   - 由于每次 `changeRating` 只会往堆里添加一条新记录，且每条旧记录最多被弹出一次，整个过程的摊销时间仍是 **O(log n)**。

> **为什么堆能帮我们做到 O(log n)？**  
> 堆是一棵满足“父节点总不小于子节点”（最大堆）的完全二叉树，插入或弹出堆顶只需要沿着树的高度移动，而高度正好是 `log₂(节点数)`，所以操作是对数级别的。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        """
        初始化：
        - food2cuisine: food -> cuisine
        - food2rating:  food -> current rating
        - cuisine2heap: cuisine -> max-heap[(-rating, food)]
        """
        self.food2cuisine = {}          # 哈希表：食物 -> 所属 cuisine
        self.food2rating = {}           # 哈希表：食物 -> 当前 rating
        self.cuisine2heap = defaultdict(list)   # 每个 cuisine 的堆

        for f, c, r in zip(foods, cuisines, ratings):
            self.food2cuisine[f] = c
            self.food2rating[f] = r
            # 用负号把 Python 的小根堆变成大根堆
            heapq.heappush(self.cuisine2heap[c], (-r, f))

    def changeRating(self, food: str, newRating: int) -> None:
        """
        1. 更新全局的 rating 表
        2. 把新的 (-rating, food) 再压进对应 cuisine 的堆
        （旧的条目会在 later 的 highestRated 中被懒删）
        """
        self.food2rating[food] = newRating
        cuisine = self.food2cuisine[food]
        heapq.heappush(self.cuisine2heap[cuisine], (-newRating, food))

    def highestRated(self, cuisine: str) -> str:
        """
        从对应 cuisine 的堆里不断弹出“过时条目”，
        直到堆顶是最新 rating 为止，然后返回食物名。
        """
        heap = self.cuisine2heap[cuisine]
        while heap:
            neg_rating, food = heap[0]            # 看堆顶
            # 当前最新 rating
            cur_rating = self.food2rating[food]
            if -neg_rating == cur_rating:         # 堆顶是最新的
                return food
            # 否则堆顶已经过时，弹出丢弃，继续检查下一个
            heapq.heappop(heap)

        # 题目保证每个 cuisine 至少有一个食物，不会走到这里
        return ""

```

#### 复杂度  

- **时间复杂度**  
  - `changeRating`：向堆插入一个元素 → **O(log m)**，其中 `m` 为该 cuisine 当前食物数（最坏可视为 O(log n)）。  
  - `highestRated`：可能要弹出若干过时条目。每条旧记录最多被弹出一次，摊销下来仍是 **O(log m)**。  
  与暴力解相比，**从 O(n) 降到 O(log n)**，即查询和修改的速度提升了数量级。

- **空间复杂度**  
  - `food2cuisine`、`food2rating` 各占 **O(n)**。  
  - `cuisine2heap` 中每次 `changeRating` 都会向堆里再插入一条记录，最坏会有 **O(k·n)** 条（k 为操作次数），但因为总操作数上限为 2·10⁴，实际空间仍在可接受范围内，仍记作 **O(n)**（常数因子略大）。

---

## 心得

- **核心技巧**：为每个类别维护**可快速取最大/最小的优先队列**（堆），配合**哈希表实现 O(1) 的定位**，并使用**懒删除**避免在堆中寻找并删除特定元素的高成本操作。  
- **适用的题型**  
  1. “每个类别的最高/最低值查询”——如 LeetCode 352 `Data Stream as Disjoint Set` 中的 **最大值维护**。  
  2. “动态排行榜”——如 LeetCode 703 `Kth Largest Element in a Stream`。  
  3. “实时最高分/最低价”——如 LeetCode 714 `Best Time to Buy and Sell Stock with Transaction Fee` 的变体。  
- **一句话总结解题钥匙**：**“用哈希表快速定位，用堆保持有序，用懒删保持堆的简洁”。**

---

## 反思

- **第一反应**：看到“查询某一 cuisine 的最高评分”，立刻想到“遍历所有食物”。这就是暴力思路。  
- **最容易踩的坑**  
  - **字典序比较**：当评分相同，需要返回字典序更小的食物，堆的比较键必须是 `(-rating, food)`，否则会出现错误的排序。  
  - **懒删除遗漏**：在 `highestRated` 时一定要检查堆顶的 rating 是否仍是最新的，否则会返回已经被改动的旧分数。  
  - **边界情况**：题目保证每个 cuisine 至少有一个食物，但实现时仍要防止堆空导致的 `IndexError`。  
- **下次遇到同类题**，第一步应该想到：**“是否可以为每个分组维护一个有序结构（堆/平衡树）？”**，然后再决定是否需要懒删除或其他技巧来保持结构的高效。