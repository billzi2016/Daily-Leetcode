# #497. **非重叠矩形中的随机点** / Random Point in Non-overlapping Rectangles

> 难度：中等 · 标签：Array、Math、Binary Search、Reservoir Sampling、Prefix Sum、Ordered Set、Randomized · [LeetCode 链接](https://leetcode.com/problems/random-point-in-non-overlapping-rectangles/)

---

## 题目（英文原版）

**Description**

You are given an array of non-overlapping axis-aligned rectangles rects where rects[i] = [ai, bi, xi, yi] indicates that (ai, bi) is the bottom-left corner point of the ith rectangle and (xi, yi) is the top-right corner point of the ith rectangle. Design an algorithm to pick a random integer point inside the space covered by one of the given rectangles. A point on the perimeter of a rectangle is included in the space covered by the rectangle.
Any integer point inside the space covered by one of the given rectangles should be equally likely to be returned.
Note that an integer point is a point that has integer coordinates.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "pick", "pick", "pick", "pick", "pick"]
[[[[-2, -2, 1, 1], [2, 2, 4, 6]]], [], [], [], [], []]
Output
[null, [1, -2], [1, -1], [-1, -2], [-2, -2], [0, 0]]

Explanation
Solution solution = new Solution([[-2, -2, 1, 1], [2, 2, 4, 6]]);
solution.pick(); // return [1, -2]
solution.pick(); // return [1, -1]
solution.pick(); // return [-1, -2]
solution.pick(); // return [-2, -2]
solution.pick(); // return [0, 0]
```

**Constraints**

- 1 <= rects.length <= 100
- rects[i].length == 4
- -109 <= ai < xi <= 109
- -109 <= bi < yi <= 109
- xi - ai <= 2000
- yi - bi <= 2000
- All the rectangles do not overlap.
- At most 104 calls will be made to pick.

---

## 题目（中文翻译）

给定一个由非重叠的轴对齐矩形（axis-aligned rectangles）组成的数组 `rects`，其中 `rects[i] = [a_i, b_i, x_i, y_i]` 表示第 `i` 个矩形的左下角点为 `(a_i, b_i)`，右上角点为 `(x_i, y_i)`。请设计一种算法，从这些矩形覆盖的空间中随机挑选一个整数点（integer point）。矩形的边界上的点也视为属于该矩形覆盖的空间。

- 所有可能的整数点出现的概率必须相同。
- 整数点指的是坐标均为整数的点。
- 实现 `Solution` 类，使其能够多次调用 `pick` 方法返回满足上述条件的随机点。

**示例 1**

```json
["Solution", "pick", "pick", "pick", "pick", "pick"]
[[[[-2, -2, 1, 1], [2, 2, 4, 6]]], [], [], [], [], []]
```

输出

```json
[null, [1, -2], [1, -1], [-1, -2], [-2, -2], [0, 0]]
```

**解释**

```java
Solution solution = new Solution([[-2, -2, 1, 1], [2, 2, 4, 6]]);
solution.pick(); // 返回 [1, -2]
solution.pick(); // 返回 [1, -1]
solution.pick(); // 返回 [-1, -2]
solution.pick(); // 返回 [-2, -2]
solution.pick(); // 返回 [0, 0]
```

**约束条件**

- `1 <= rects.length <= 100`
- `rects[i].length == 4`
- `-10^9 <= a_i < x_i <= 10^9`
- `-10^9 <= b_i < y_i <= 10^9`
- `x_i - a_i <= 2000`
- `y_i - b_i <= 2000`
- 所有矩形互不重叠。
- 最多会调用 `pick` 方法 `10^4` 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **所有** 整数格点都列出来，放进一个大列表，然后让 Python 的 `random.choice` 随机挑一个。  
- **数据结构**：把每个格点当成列表的一个元素。可以把列表想象成一本**电话号码簿**，每一行记载一个坐标 (x, y)。  
- **正确性**：因为我们把所有合法格点都放进列表，并且 `choice` 是均匀随机的，所以每个格点被选中的概率相同。  

> **注意**：题目保证每个矩形的宽高 ≤ 2000，单个矩形最多有 (2000+1)·(2000+1) ≈ 4 000 001 个格点。若有 100 个矩形，最坏情况下会有 **4·10⁸** 条记录，显然会爆内存。这就是暴力解的瓶颈，但在概念层面它是最容易理解的。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, rects: List[List[int]]):
        """把所有整数格点展开成一个大列表"""
        self.points = []
        for a, b, x, y in rects:                # a,b 为左下角，x,y 为右上角（含边界）
            for xi in range(a, x + 1):          # x 坐标从 a 到 x（包括两端）
                for yi in range(b, y + 1):      # y 坐标从 b 到 y（包括两端）
                    self.points.append([xi, yi])   # 把坐标加入列表

    def pick(self) -> List[int]:
        """随机返回列表中的一个坐标"""
        return random.choice(self.points)   # Python 自带的均匀随机抽取
```

> 关键行已用中文注释说明。

#### 复杂度  

- **时间复杂度**：`O(T)`，其中 `T` 为所有矩形中格点的总数。构造阶段需要遍历每个格点一次，`pick` 只需 `O(1)`。  
  > “O(T)” 可以理解为“和格点数量成正比”。如果格点有 1000 万个，构造就要跑 1000 万次循环。  
- **空间复杂度**：`O(T)`，因为我们把每个格点都存进了列表。  

> 对于本题的最大输入，这种做法会导致数百 MB 甚至 GB 级别的内存占用，显然不可行。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到两个关键点：

1. **每个格点出现的概率相同** → 只要把格点总数 `total` 看成一个大“抽屉”，先随机抽出一个编号 `k`（0 ≤ k < total），再把这个编号映射回具体的坐标即可。  
2. **我们不必真的把所有格点写出来** → 只要知道每个矩形里有多少格点，就可以在「抽屉」层面先决定落在哪个矩形，再在该矩形内部随机取点。

于是我们把 **“格点数量”** 这个信息压缩成一个 **前缀和数组**（Prefix Sum），再用 **二分查找**（Binary Search）把随机编号定位到对应的矩形。

下面逐步解释这些概念：

- **前缀和**：把每个矩形的格点数累加起来，得到一个递增的序列 `pref[i]`，它的意义是“前 i 个矩形（包括第 i‑1 个）一共有多少格点”。可以把它想象成一本**目录**，目录的第 i 条记录说“到第 i 本书为止，一共 12345 页”。  
- **二分查找**：给定一个随机编号 `k`，我们在递增的 `pref` 中找第一个 **大于 k** 的位置，这个位置对应的矩形就是我们要选的矩形。二分查找的时间是 `O(log n)`（n 为矩形数量），相当于把一本 100 页的目录，用折半查找只需要最多 7 次比较就能定位到目标页。  

**在确定了矩形以后**，只需要在该矩形的整数坐标范围内各自随机一次即可。因为矩形内部的格点是均匀分布的，直接使用 `random.randint` 就能保证每个格点等概率。

#### 步骤概览  

1. **预处理**（构造函数）  
   - 对每个矩形计算格点数 `cnt = (x - a + 1) * (y - b + 1)`。  
   - 把 `cnt` 加到前缀和列表 `pref` 中。  
   - 同时把矩形本身保存下来备用。  

2. **pick()**  
   - 生成 `k = random.randint(0, total-1)`，其中 `total = pref[-1]`。  
   - 用 `bisect_left(pref, k+1)` 找到对应的矩形下标 `idx`（`bisect` 是 Python 标准库的二分实现）。  
   - 在矩形 `rects[idx] = [a,b,x,y]` 内分别随机生成 `rx = random.randint(a, x)`、`ry = random.randint(b, y)`。  
   - 返回 `[rx, ry]`。  

整个过程只用了 **O(n)** 的预处理空间（n ≤ 100），每次 `pick` 只做 **O(log n)** 的查找和常数次随机数生成，既快又省内存。

#### 代码（Python）

```python
import random
import bisect
from typing import List

class Solution:
    def __init__(self, rects: List[List[int]]):
        """
        预处理：为每个矩形计算格点数量并构造前缀和数组。
        rects[i] = [a, b, x, y]，左下角 (a,b)，右上角 (x,y)，坐标都是整数。
        """
        self.rects = rects                # 保存原始矩形信息，后面会用到
        self.prefix = []                  # 前缀和数组，prefix[i] 表示前 i+1 个矩形的格点总数
        cur = 0
        for a, b, x, y in rects:
            # 该矩形内部的整数格点数量 = (宽度+1) * (高度+1)
            cnt = (x - a + 1) * (y - b + 1)
            cur += cnt                    # 累加到当前总数
            self.prefix.append(cur)       # 保存当前的前缀和

    def pick(self) -> List[int]:
        """
        随机挑选一个格点，保证所有格点等概率。
        步骤：
        1）在 [0, total-1] 之间随机一个编号 k；
        2）二分定位 k 落在哪个矩形；
        3）在该矩形内部再随机一次得到具体坐标。
        """
        total = self.prefix[-1]           # 所有格点的总数
        k = random.randint(0, total - 1)  # 第一步：随机编号

        # 第二步：二分查找，第一个前缀和 > k 的位置即为目标矩形下标
        idx = bisect.bisect_left(self.prefix, k + 1)

        a, b, x, y = self.rects[idx]      # 取出对应的矩形

        # 第三步：在该矩形的整数坐标范围内各自随机一次
        rx = random.randint(a, x)
        ry = random.randint(b, y)
        return [rx, ry]
```

> 关键行已加中文注释，代码可直接运行。

#### 复杂度  

- **时间复杂度**：`O(log n)`（`n` 为矩形数量）。二分查找的代价是对数级别，其他操作（两次 `randint`）是常数时间。相比暴力的 `O(T)`（T 为格点总数），快了很多。  
  > 举例：如果有 100 个矩形，`log₂100 ≈ 7`，所以最多只需要 7 次比较就能定位矩形。  
- **空间复杂度**：`O(n)`。我们只保存矩形列表和前缀和数组，最多几百个整数，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：把离散的“点”压缩成“数量” → 前缀和 + 二分查找 + 区间随机。  
- **适用场景**  
  1. **离散概率抽样**：如「从若干盒子中随机抽球，盒子里球的数量不同」  
  2. **权重随机选择**：LeetCode 528 `Random Pick with Weight`  
  3. **区间随机**：如「从若干不相交区间中随机挑一个整数」  

> **解题钥匙**：先把“每个元素出现的次数”算出来，构造递增的累计数组，用二分定位，再在对应子集内部做一次均匀抽样。

---

## 反思  

- **第一反应**：把所有格点列出来 → 直接想到「枚举」但忽略了规模。  
- **最容易踩的坑**  
  1. **整数溢出**：坐标范围可达 ±10⁹，计算格点数时要使用 64 位整数（Python 自动处理，但在其他语言要注意 long long）。  
  2. **前缀和的下标**：二分查找时要找 `k+1`（或使用 `bisect_left` 并把 `k` 与前缀比较），否则会把编号恰好等于前缀和的情况定位错。  
  3. **矩形宽高的 +1**：因为边界点也算在内，格点数是 `(x-a+1)*(y-b+1)`，忘记 `+1` 会导致概率不均。  

- **下次类似题的第一步**：先**统计每个子集合的大小**（或权重），把它们累加成前缀和；随后**在总大小范围随机**，用二分把随机数映射回具体子集合。这样既省空间又快。