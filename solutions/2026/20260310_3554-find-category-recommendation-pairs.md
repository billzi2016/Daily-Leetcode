# #3554. 查找类别推荐对 / Find Category Recommendation Pairs

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-category-recommendation-pairs/)

---

## 题目（英文原版）

**Description**

Table: ProductPurchases
Table: ProductInfo
Amazon wants to understand shopping patterns across product categories. Write a solution to:
A category pair is considered reportable if at least 3 different customers have purchased products from both categories.
Return the result table of reportable category pairs ordered by customer_count in descending order, and in case of a tie, by category1 in ascending order lexicographically, and then by category2 in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type | 
+-------------+------+
| user_id     | int  |
| product_id  | int  |
| quantity    | int  |
+-------------+------+
(user_id, product_id) is the unique identifier for this table. 
Each row represents a purchase of a product by a user in a specific quantity.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    | 
+-------------+---------+
| product_id  | int     |
| category    | varchar |
| price       | decimal |
+-------------+---------+
product_id is the unique identifier for this table.
Each row assigns a category and price to a product.
```

**Example 3:**

```
+---------+------------+----------+
| user_id | product_id | quantity |
+---------+------------+----------+
| 1       | 101        | 2        |
| 1       | 102        | 1        |
| 1       | 201        | 3        |
| 1       | 301        | 1        |
| 2       | 101        | 1        |
| 2       | 102        | 2        |
| 2       | 103        | 1        |
| 2       | 201        | 5        |
| 3       | 101        | 2        |
| 3       | 103        | 1        |
| 3       | 301        | 4        |
| 3       | 401        | 2        |
| 4       | 101        | 1        |
| 4       | 201        | 3        |
| 4       | 301        | 1        |
| 4       | 401        | 2        |
| 5       | 102        | 2        |
| 5       | 103        | 1        |
| 5       | 201        | 2        |
| 5       | 202        | 3        |
+---------+------------+----------+
```

**Example 4:**

```
+------------+-------------+-------+
| product_id | category    | price |
+------------+-------------+-------+
| 101        | Electronics | 100   |
| 102        | Books       | 20    |
| 103        | Books       | 35    |
| 201        | Clothing    | 45    |
| 202        | Clothing    | 60    |
| 301        | Sports      | 75    |
| 401        | Kitchen     | 50    |
+------------+-------------+-------+
```

**Example 5:**

```
+-------------+-------------+----------------+
| category1   | category2   | customer_count |
+-------------+-------------+----------------+
| Books       | Clothing    | 3              |
| Books       | Electronics | 3              |
| Clothing    | Electronics | 3              |
| Electronics | Sports      | 3              |
+-------------+-------------+----------------+
```

---

## 题目（中文翻译）

Amazon 希望了解不同商品类别之间的购物模式。请编写 SQL 语句实现以下需求：

- 若至少有 **3** 位不同的用户（customer）购买了 **两个类别**（category）的商品，则这两个类别构成一个**可报告的类别对**（category pair）。
- 返回所有可报告的类别对，并按照 `customer_count` 降序排列；若计数相同，则按 `category1` 的字典序升序排列；再者按 `category2` 的字典序升序排列。

结果表结构如下所示（参见示例 5）：

```sql
+-------------+-------------+----------------+
| category1   | category2   | customer_count |
+-------------+-------------+----------------+
| ...         | ...         | ...            |
+-------------+-------------+----------------+
```

**表结构**

`ProductPurchases` 表记录用户购买信息：

| Column Name | Type |
|-------------|------|
| user_id     | int  |
| product_id  | int  |
| quantity    | int  |

`(user_id, product_id)` 为唯一标识。每行表示用户对某商品的购买数量。

`ProductInfo` 表记录商品的类别和价格信息：

| Column Name | Type    |
|-------------|---------|
| product_id  | int     |
| category    | varchar |
| price       | decimal |

`product_id` 为唯一标识。每行给出商品对应的类别（category）和价格。

**示例数据**

```sql
-- ProductPurchases
+---------+------------+----------+
| user_id | product_id | quantity |
+---------+------------+----------+
| 1       | 101        | 2        |
| 1       | 102        | 1        |
| 1       | 201        | 3        |
| 1       | 301        | 1        |
| 2       | 101        | 1        |
| 2       | 102        | 2        |
| 2       | 103        | 1        |
| 2       | 201        | 5        |
| 3       | ...        | ...      |
... (已截断)

-- ProductInfo
+------------+-------------+-------+
| product_id | category    | price |
+------------+-------------+-------+
| 101        | Electronics | 100   |
| 102        | Books       | 20    |
| 103        | Books       | 35    |
| 201        | Clothing    | 45    |
| 202        | Clothing    | 60    |
| 301        | Sports      | 75    |
| 401        | Kitchen     | 50    |
+------------+-------------+-------+
... (已截断)

-- 期望输出
+-------------+-------------+----------------+
| category1   | category2   | customer_count |
+-------------+-------------+----------------+
| Books       | Clothing    | 3              |
| Books       | Electronics | 3              |
| Clothing    | Electronics | 3              |
| Electronics | Sports      | 3              |
+-------------+-------------+----------------+
```

**约束条件**

- 无特定约束。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把两张表合并**  
   - `ProductPurchases` 记录每个用户买了哪些 `product_id`。  
   - `ProductInfo` 把每个 `product_id` 对应到具体的 `category`。  
   - 把它们 **JOIN**（相当于把两本书的目录拼在一起），得到 **用户‑类别** 的记录。  

2. **统计每个用户买过哪些类别**  
   - 把同一个用户出现的所有 `category` 收集到一个 **集合**（就像把一个人买过的所有水果装进篮子，篮子里不允许出现相同的水果）。  

3. **在每个用户的篮子里生成所有两两组合**  
   - 对每个用户的类别集合，枚举所有 **不重复的两两配对**（`category1 < category2`），这一步相当于让用户把手里的水果两两配对，看看配对了哪些水果。  

4. **把配对出现的次数累加**  
   - 用一个全局的哈希表 `pair_cnt`（键是 `(cat1, cat2)`，值是出现的用户数）来统计有多少不同用户产生了同一配对。  

5. **筛选并排序**  
   - 只保留出现次数 **≥ 3** 的配对。  
   - 按 `customer_count` 降序；若相同，再按 `category1`、`category2` 的字典序升序排列。  

> **哈希表的类比**：把它想象成一本 **查字典**，`key` 是要查的单词（这里是类别配对），`value` 是对应的页码（这里是买过这对类别的用户数）。查一次就是 O(1) 时间。

#### 代码（Python）

```python
from collections import defaultdict
from itertools import combinations
from typing import List, Tuple

# -------------------------------------------------
# 模拟数据库表：列表套字典，实际使用时可以直接读 csv / sql
# -------------------------------------------------
ProductPurchases = [
    # user_id, product_id, quantity
    {"user_id": 1, "product_id": 101, "quantity": 2},
    {"user_id": 1, "product_id": 102, "quantity": 1},
    {"user_id": 1, "product_id": 201, "quantity": 3},
    {"user_id": 1, "product_id": 301, "quantity": 1},
    {"user_id": 2, "product_id": 101, "quantity": 1},
    {"user_id": 2, "product_id": 102, "quantity": 2},
    {"user_id": 2, "product_id": 103, "quantity": 1},
    {"user_id": 2, "product_id": 201, "quantity": 5},
    {"user_id": 3, "product_id": 101, "quantity": 1},
    {"user_id": 3, "product_id": 103, "quantity": 2},
    {"user_id": 3, "product_id": 202, "quantity": 1},
    {"user_id": 3, "product_id": 301, "quantity": 1},
    # ... 这里可以继续添加更多数据
]

ProductInfo = [
    # product_id, category, price
    {"product_id": 101, "category": "Electronics", "price": 100},
    {"product_id": 102, "category": "Books",       "price": 20},
    {"product_id": 103, "category": "Books",       "price": 35},
    {"product_id": 201, "category": "Clothing",    "price": 45},
    {"product_id": 202, "category": "Clothing",    "price": 60},
    {"product_id": 301, "category": "Sports",      "price": 75},
    {"product_id": 401, "category": "Kitchen",     "price": 50},
]

def find_reportable_pairs_bruteforce(
    purchases: List[dict],
    infos: List[dict],
    threshold: int = 3
) -> List[Tuple[str, str, int]]:
    """
    暴力实现：先把用户对应的购买类别收集起来，再枚举配对计数。
    返回形如 (category1, category2, customer_count) 的列表，已排序。
    """
    # 1️⃣ 把 product_id -> category 建立映射（相当于字典查词典）
    pid_to_cat = {info["product_id"]: info["category"] for info in infos}

    # 2️⃣ 为每个用户收集购买过的类别集合
    user_to_cats = defaultdict(set)          # key: user_id, value: set of categories
    for rec in purchases:
        uid = rec["user_id"]
        pid = rec["product_id"]
        # 只要买过就算一次，quantity 不影响配对计数
        cat = pid_to_cat.get(pid)
        if cat:                               # 防止出现找不到类别的脏数据
            user_to_cats[uid].add(cat)

    # 3️⃣ 统计所有用户产生的类别配对出现次数
    pair_cnt = defaultdict(int)              # key: (cat1, cat2), value: number of distinct users
    for uid, cat_set in user_to_cats.items():
        # 同一个用户内部的配对只计一次
        for cat1, cat2 in combinations(sorted(cat_set), 2):   # 只取 (小, 大) 防止重复
            pair_cnt[(cat1, cat2)] += 1

    # 4️⃣ 过滤出满足阈值的配对并排序
    result = [
        (c1, c2, cnt)
        for (c1, c2), cnt in pair_cnt.items()
        if cnt >= threshold
    ]

    # 排序规则：customer_count 降序 → category1 升序 → category2 升序
    result.sort(key=lambda x: (-x[2], x[0], x[1]))
    return result


# ------------------- 演示 -------------------
if __name__ == "__main__":
    pairs = find_reportable_pairs_bruteforce(ProductPurchases, ProductInfo, 3)
    for c1, c2, cnt in pairs:
        print(f"{c1:<12} {c2:<12} {cnt}")
```

> **关键行中文注释**  
> - 第 9 行：把 `product_id` 映射成 `category`，相当于查字典得到页码。  
> - 第 16 行：`defaultdict(set)` 自动创建空集合，省去判断键是否存在的代码。  
> - 第 24 行：`combinations(sorted(cat_set), 2)` 生成所有不重复的两两配对，并且保证配对顺序固定（小的在前），防止 `(A,B)` 与 `(B,A)` 被算成两条。  
> - 第 31 行：用 `defaultdict(int)` 统计每个配对出现的用户数。  

#### 复杂度  

- **时间复杂度**：  
  - 建立映射 O(*p*)，`p` 为商品数量。  
  - 收集用户‑类别集合遍历所有购买记录 O(*n*)，`n` 为购买记录条数。  
  - 对每个用户的类别集合枚举配对，最坏情况是某个用户买了 `c` 种不同类别，需要枚举 `C(c,2) = c·(c-1)/2` 对。设所有用户的类别总数为 `S`，则这一步是 O(*S²*) 的上界（极端情况下每个用户买了所有类别）。实际数据中 `c` 通常很小。  
  - 整体时间大约是 **O(n + S²)**，在最坏情况下可以视作 **O(n·k²)**（`k` 为每个用户可能的最大类别数）。  
  - 对初学者来说，只要记住**遍历一次表 + 对每个用户做两两组合**，就是暴力解的全部工作量。  

- **空间复杂度**：  
  - `pid_to_cat` 需要存放所有商品的类别，大小为 O(*p*)。  
  - `user_to_cats` 保存每个用户的类别集合，最多 O(*U·k*)，`U` 为用户数。  
  - `pair_cnt` 保存所有出现过的配对，最多 O(*C²*)，其中 `C` 为所有不同类别的数量。  
  - 因此总体空间是 **O(p + U·k + C²)**，在真实业务里这些数字都在可接受范围内。  

---

### 2. 最优解

#### 思路  

暴力解已经很直观，但我们可以把 **“为每个用户产生配对再计数”** 这一步合并进一次 **全局遍历**，从而只需要一次遍历 `ProductPurchases` 表，而不必先把所有用户的类别收集完再二次遍历。

核心思想：

1. **一次遍历构造用户‑类别集合**  
   - 用 `defaultdict(set)` 同时把每条购买记录映射到对应的 `category`，并立即把它加入用户的集合。  

2. **在用户集合** **完成后立即** 统计配对，而不是等所有用户都处理完后再统一遍历。  
   - 当我们 **第一次** 完成某个用户的全部类别（即所有该用户的购买记录都已读取完），立刻对该用户的集合生成配对并累加到全局计数器。  
   - 为了在一次遍历中“知道何时结束一个用户”，我们可以先对 `ProductPurchases` 按 `user_id` 排序（或使用 `groupby`），这样相同用户的记录会连续出现。  

3. **使用整数编码代替字符串配对**（可选）  
   - 若类别数量很多，字符串拼接会带来额外的哈希开销。我们可以给每个类别分配一个 **整数 id**（类似给字典里每个词编号），配对用 `(id1, id2)` 这个元组作为键。  
   - 这种方式在大数据量时会更快、更省内存。  

4. **一次计数后直接筛选**  
   - 在累计配对计数的过程中，一旦某个配对的计数达到阈值 `3`，我们可以标记它为 “已满足”，但仍需继续统计，以免后面出现更多用户导致计数继续增长（对排序没有影响）。  

5. **最终排序**  
   - 与暴力解相同，只是这里的 `pair_cnt` 已经在一次遍历中完成。  

> **为什么会更快？**  
> - 暴力解先把所有用户的集合保存下来，然后再遍历这些集合生成配对，这相当于 **两遍遍历**。  
> - 最优解把 “生成配对” 与 “收集集合” 合并到同一次遍历中，**只遍历一次** 表，减少了内存占用（不需要保存所有用户的完整集合），在数据量很大时优势明显。  

#### 代码（Python）

```python
from collections import defaultdict
from itertools import combinations
from typing import List, Tuple

def find_reportable_pairs_optimal(
    purchases: List[dict],
    infos: List[dict],
    threshold: int = 3
) -> List[Tuple[str, str, int]]:
    """
    最优实现：一次遍历完成用户‑类别收集 + 配对计数。
    """
    # 1️⃣ 建立 product_id → category 的映射（一次性完成）
    pid_to_cat = {info["product_id"]: info["category"] for info in infos}

    # 2️⃣ 为每个类别分配一个整数 id（可选，提升哈希效率）
    #    这里用字典把 category -> idx 记录下来
    cat_to_idx = {}
    idx_to_cat = []                     # idx → category，逆向映射
    for cat in set(pid_to_cat.values()):
        cat_to_idx[cat] = len(idx_to_cat)
        idx_to_cat.append(cat)

    # 3️⃣ 先按 user_id 排序，保证同一用户的记录相邻
    purchases_sorted = sorted(purchases, key=lambda x: x["user_id"])

    pair_cnt = defaultdict(int)        # (idx1, idx2) -> distinct user count
    cur_user = None
    cur_cats = set()                    # 当前用户的类别集合（整数 id）

    for rec in purchases_sorted:
        uid = rec["user_id"]
        pid = rec["product_id"]
        cat = pid_to_cat.get(pid)
        if not cat:                     # 跳过没有对应类别的商品
            continue
        cid = cat_to_idx[cat]           # 把类别转成整数 id

        if uid != cur_user:
            # ---- 旧用户的配对统计结束，计入全局 ----
            if cur_user is not None and len(cur_cats) >= 2:
                for i, j in combinations(sorted(cur_cats), 2):
                    pair_cnt[(i, j)] += 1
            # ---- 开始处理新用户 ----
            cur_user = uid
            cur_cats = set()
        # 把当前商品的类别加入当前用户集合
        cur_cats.add(cid)

    # 循环结束后记得处理最后一个用户
    if cur_user is not None and len(cur_cats) >= 2:
        for i, j in combinations(sorted(cur_cats), 2):
            pair_cnt[(i, j)] += 1

    # 4️⃣ 把满足阈值的配对转换回字符串形式并排序
    result = []
    for (i, j), cnt in pair_cnt.items():
        if cnt >= threshold:
            result.append((idx_to_cat[i], idx_to_cat[j], cnt))

    result.sort(key=lambda x: (-x[2], x[0], x[1]))
    return result


# ------------------- 演示 -------------------
if __name__ == "__main__":
    pairs = find_reportable_pairs_optimal(ProductPurchases, ProductInfo, 3)
    for c1, c2, cnt in pairs:
        print(f"{c1:<12} {c2:<12} {cnt}")
```

> **代码要点解释**  
> - 第 9‑12 行：把所有 `category` 编号，**整数比字符串更轻量**，在后面做哈希时更快。  
> - 第 15 行：`sorted(..., key=lambda x: x["user_id"])` 确保同一用户的记录相邻，类似把同学的成绩单按学号排好序，方便一次遍历完结算。  
> - 第 24‑32 行：当检测到 **用户切换** 时，说明前一个用户的所有购买记录已经收集完毕，于是立刻对其集合生成配对并计数。  
> - 第 38‑40 行：循环结束后别忘了对最后一个用户做同样的配对统计。  
> - 第 45‑48 行：把整数配对重新映射回原始的 `category` 名称，方便阅读。  

#### 复杂度  

- **时间复杂度**  
  - 建立 `product_id → category` 映射 O(*p*)。  
  - 对 `purchases` 进行一次排序 O(*n* log *n*)（如果原始表已经按照 `user_id` 排好序，这一步可以省掉）。  
  - 单次遍历 `purchases`，对每条记录做 O(1) 的映射与集合加入操作，总计 O(*n*)。  
  - 对每个用户的类别集合生成配对的总工作量仍是所有用户配对数的和，记作 *P*。因此整体时间是 **O(p + n log n + P)**。在大多数实际场景下，`P` 远小于 `n²`，所以比暴力解快很多。  

- **空间复杂度**  
  - `pid_to_cat` O(*p*)。  
  - `cat_to_idx / idx_to_cat` O(*C*)，`C` 为不同类别数。  
  - `pair_cnt` 最多保存所有可能的配对，即 O(*C²*)。  
  - 额外只保留 **当前用户的类别集合**，大小最多 O(*k*)（单个用户的类别数）。  
  - 因此总体空间是 **O(p + C + C²)**，与暴力解相比省去了 `user_to_cats` 那块可能很大的内存。  

> **对比**：暴力解需要两次遍历（一次收集集合，一次枚举配对），且在内存中保存所有用户的完整集合；最优解只遍历一次，且只在内存中保留当前用户的临时集合，显著降低了空间使用，并在大数据下拥有更好的时间表现。

---

## 心得

- **核心技巧**：**对每个用户的类别集合做两两配对并计数**（本质是 **集合配对计数**）。  
- **适用场景**  
  1. “找出共同出现的标签对”——如社交平台用户共同喜欢的两种兴趣标签。  
  2. “商品篮子中经常一起出现的两类商品”——购物篮分析（Market‑Basket Analysis）。  
  3. “同一作者的文章中出现的关键词对”——文本共现分析。  

> **一句话总结解题钥匙**：把 **“同一实体的多属性集合”** 转化为 **“两两配对”**，用哈希表累计出现次数，再按阈值筛选。

---

## 反思

- **第一反应**：看到“两个类别配对出现至少 3 次”，立刻想到 **先把每个用户的类别收集成集合，再枚举配对**。  
- **最容易踩的坑**  
  1. **重复计数**：同一个用户如果购买同一类别多次，不能把它算作多次配对。必须先 **去重**（用集合）。  
  2. **配对顺序**：`(A,B)` 与 `(B,A)` 必须视为同一配对，需统一顺序（如字典序或 id 小在前）。  
  3. **边界条件**：用户只买了 0 或 1 种类别时不产生配对，需要过滤。  
  4. **排序规则**：`customer_count` 降序、`category1` 升序、`category2` 升序，三层排序一定要写对。  

- **下次遇到类似题目**，第一步应该：  
  **“把每个实体的属性集合化为去重的集合，然后在集合内部做两两组合计数”**。这一步几乎是所有“共现配对”题的通用模板。