# #3531. 统计被覆盖的建筑 / Count Covered Buildings

> 难度：中等 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-covered-buildings/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n, representing an n x n city. You are also given a 2D grid buildings, where buildings[i] = [x, y] denotes a unique building located at coordinates [x, y].
A building is covered if there is at least one building in all four directions: left, right, above, and below.
Return the number of covered buildings.

**Examples**

**Example 1:**

```
Input: n = 3, buildings = [[1,2],[2,2],[3,2],[2,1],[2,3]]
Output: 1
Explanation:
```

**Example 2:**

```
Input: n = 3, buildings = [[1,1],[1,2],[2,1],[2,2]]
Output: 0
Explanation:
```

**Example 3:**

```
Input: n = 5, buildings = [[1,3],[3,2],[3,3],[3,5],[5,3]]
Output: 1
Explanation:
```

**Constraints**

- 2 <= n <= 105
- 1 <= buildings.length <= 105
- buildings[i] = [x, y]
- 1 <= x, y <= n
- All coordinates of buildings are unique.

---

## 题目（中文翻译）

你得到一个正整数 n，表示一个 n × n 的城市。还有一个二维数组 buildings，其中 buildings[i] = [x, y] 表示一座坐标为 [x, y] 的唯一建筑。  
如果一座建筑在 **左 (left)**、**右 (right)**、**上 (above)**、**下 (below)** 四个方向上各至少存在另一座建筑，则该建筑被视为已覆盖。  
返回被覆盖的建筑数量。

**示例 1**  
**输入**: `n = 3, buildings = [[1,2],[2,2],[3,2],[2,1],[2,3]]`  
**输出**: `1`  
**解释**:  

**示例 2**  
**输入**: `n = 3, buildings = [[1,1],[1,2],[2,1],[2,2]]`  
**输出**: `0`  
**解释**:  

**示例 3**  
**输入**: `n = 5, buildings = [[1,3],[3,2],[3,3],[3,5],[5,3]]`  
**输出**: `1`  
**解释**:  

**约束条件**  
- 2 ≤ n ≤ 10^5  
- 1 ≤ buildings.length ≤ 10^5  
- buildings[i] = [x, y]  
- 1 ≤ x, y ≤ n  
- 所有建筑坐标互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是对每一座建筑都去检查四个方向是否都有别的建筑：

1. **左**：在同一行（`y` 相同）且 `x` 更小的建筑是否存在。  
2. **右**：同一行且 `x` 更大的建筑是否存在。  
3. **上**：同一列（`x` 相同）且 `y` 更大的建筑是否存在。  
4. **下**：同一列且 `y` 更小的建筑是否存在。

如果四个方向都满足，则这座建筑算作“被覆盖”。  

> **类比**：把每一行想象成一本字典，`x` 是单词的字母顺序。要判断一个单词是否在字典的“中间”，只需要看它左边和右边是否还有单词。同理，列也是一本字典，只是按照 `y` 排序。

**正确性**：只要遍历所有建筑，逐一检查四个方向的存在性，满足题目定义的建筑必然会被计数，未满足的不会计数，故算法正确。

**复杂度分析**（大白话）：

- 对每座建筑我们要在所有其他建筑中找左、右、上、下四个方向的“邻居”。最坏情况下要比较 `m-1`（`m = buildings.length`）次。  
- 于是时间是 `m`（建筑数）乘以 `m`，记作 **O(m²)**，即如果建筑有 10,000 座，程序要做 100,000,000 次比较，显然会很慢。  
- 我们只用到一个存放所有坐标的列表，空间是 **O(m)**。

#### 代码（Python）

```python
from typing import List

def count_covered_bruteforce(n: int, buildings: List[List[int]]) -> int:
    # 把坐标转成集合，查找是否存在会更快（O(1)）
    s = set((x, y) for x, y in buildings)

    covered = 0
    for x, y in buildings:
        # 检查四个方向是否都有建筑
        left  = any((lx, y) in s for lx in range(1, x))          # 同行左边
        right = any((rx, y) in s for rx in range(x + 1, n + 1))  # 同行右边
        down  = any((x, dy) in s for dy in range(1, y))          # 同列下边
        up    = any((x, uy) in s for uy in range(y + 1, n + 1))  # 同列上边

        if left and right and up and down:
            covered += 1
    return covered
```

> 关键行解释  
> - `s = set(...)`：把所有建筑放进哈希表（像查字典一样）方便 O(1) 判断是否存在。  
> - `any(... for ...)`：遍历可能的坐标，一旦找到满足条件的即返回 `True`。

#### 复杂度

- **时间复杂度**：**O(m²)**  
  - “平方”意味着如果建筑数量翻倍，运行时间会变成原来的四倍。  
- **空间复杂度**：**O(m)**  
  - 只用了一个集合存放所有建筑坐标。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每座建筑都要遍历整条行或列**，导致大量重复检查。我们可以把同一行（`y` 相同）或同一列（`x` 相同）的建筑提前收集、排序，然后一次性得出哪些建筑在该方向上是“内部”的（既有左也有右，或既有上也有下）。

**步骤拆解**：

1. **按行分组**  
   - 用哈希表 `row_map[y]` 保存所有在第 `y` 行的 `x` 坐标。  
   - 把每个列表排序后，**首位**的建筑只能看到左/右其中一个方向（因为左侧或右侧没有建筑），**中间**的建筑左、右都有建筑 → 这类建筑满足“左&右”条件。

2. **按列分组**  
   - 类似地，用 `col_map[x]` 保存所有在第 `x` 列的 `y` 坐标，排序后中间的建筑满足“上&下”条件。

3. **交集**  
   - 把满足左&右的建筑记入集合 `has_lr`，满足上&下的记入集合 `has_ud`。  
   - 同时满足四个方向的建筑就是 `has_lr ∩ has_ud` 的元素个数。

> **类比**：把每一行想成一本排好序的电话簿，首尾是“端点”，中间的号码一定可以在左边和右边各找到一个邻居。列也是一样，只是换了一本电话簿。

**为什么快**：  
- 每行/列只排序一次，总共排序的元素数等于建筑数 `m`，所以总的排序时间是 `O(m log m)`（比 `O(m²)` 小很多）。  
- 之后的遍历只是一趟线性扫描 `O(m)`，不再出现嵌套循环。

#### 代码（Python）

```python
from typing import List, Dict
from collections import defaultdict

def count_covered_optimal(n: int, buildings: List[List[int]]) -> int:
    # 1. 按行、列收集坐标
    row_map: Dict[int, List[int]] = defaultdict(list)   # y -> [x...]
    col_map: Dict[int, List[int]] = defaultdict(list)   # x -> [y...]

    for x, y in buildings:
        row_map[y].append(x)
        col_map[x].append(y)

    # 2. 记录在行内部的建筑（左&右都有）
    has_lr = set()   # (x, y) 满足左、右
    for y, xs in row_map.items():
        xs.sort()                     # 排序后首尾是端点
        # 中间的坐标都有左、右邻居
        for i in range(1, len(xs) - 1):
            has_lr.add((xs[i], y))

    # 3. 记录在列内部的建筑（上&下都有）
    has_ud = set()   # (x, y) 满足上、下
    for x, ys in col_map.items():
        ys.sort()
        for i in range(1, len(ys) - 1):
            has_ud.add((x, ys[i]))

    # 4. 同时满足四个方向的建筑 = 两个集合的交集
    covered = has_lr.intersection(has_ud)
    return len(covered)
```

> 关键行解释  
> - `defaultdict(list)`：自动创建空列表，像装箱一样把相同 `y`（或 `x`）的坐标放进同一个箱子。  
> - `xs.sort()` / `ys.sort()`：把同一行/列的坐标排好序，方便找出“中间”元素。  
> - `for i in range(1, len(xs) - 1)`：跳过首位，只遍历中间的建筑。  
> - `has_lr.intersection(has_ud)`：取两个集合的交集，得到四个方向都有建筑的点。

#### 复杂度

- **时间复杂度**：**O(m log m)**  
  - `log m` 来自对每行/列内部列表的排序。整体上相当于把 `m` 条数据整体排序一次，远快于 `m²`。  
  - 与暴力解相比，时间从“每座建筑都要遍历整条行/列”降到了“每行/列只遍历一次”。

- **空间复杂度**：**O(m)**  
  - 需要额外的哈希表保存行、列的坐标以及两个集合 `has_lr`、`has_ud`，总共不超过常数倍的建筑数。

---

## 心得

- **核心技巧**：**分组 + 排序 + 集合交集**。把同一行或同一列的建筑聚在一起，排序后中间的必然满足左右（上下）条件，再通过集合交集得到四向都有的建筑。  
- **适用的题型**  
  1. “行/列内部元素”类题目（如 LeetCode 1592 “Rearrange Spaces Between Words” 的行列处理）。  
  2. “在同一维度上有前后元素”类题目（如 2287 “Rearrange Characters to Make Target String”。）  
  3. “二维坐标统计”类题目（如 1725 “Number Of Rectangles That Can Form The Largest Square”。）  
- **一句话总结解题钥匙**：**把相同坐标的点聚在一起，排序后只关注内部元素**。

---

## 反思

- **第一反应**：看到“左、右、上、下都有建筑”，本能想到逐个检查四个方向，导致想到暴力解。  
- **最容易踩的坑**  
  - 忽略 **唯一坐标** 的前提，导致同一行/列出现重复坐标时的错误判断。  
  - 边界情况：某行或某列只有 1 或 2 座建筑时，内部集合应为空，否则会误计。  
  - 使用 `set` 交集时要确保坐标类型一致（元组而不是列表）。  
- **下次类似题**：第一步先 **把坐标按某个维度分组**，看能否通过 **排序** 一次性得到满足条件的子集，再用 **集合操作** 合并条件。这样能快速跳出暴力的思维陷阱。