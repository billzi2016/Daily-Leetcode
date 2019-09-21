# #587. 围栏 / Erect the Fence

> 难度：困难 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/erect-the-fence/)

---

## 题目（英文原版）

**Description**

You are given an array trees where trees[i] = [xi, yi] represents the location of a tree in the garden.
Fence the entire garden using the minimum length of rope, as it is expensive. The garden is well-fenced only if all the trees are enclosed.
Return the coordinates of trees that are exactly located on the fence perimeter. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: trees = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]
Output: [[1,1],[2,0],[4,2],[3,3],[2,4]]
Explanation: All the trees will be on the perimeter of the fence except the tree at [2, 2], which will be inside the fence.
```

**Example 2:**

```
Input: trees = [[1,2],[2,2],[4,2]]
Output: [[4,2],[2,2],[1,2]]
Explanation: The fence forms a line that passes through all the trees.
```

**Constraints**

- 1 <= trees.length <= 3000
- trees[i].length == 2
- 0 <= xi, yi <= 100
- All the given positions are unique.

---

## 题目（中文翻译）

你得到一个数组 `trees`，其中 `trees[i] = [xi, yi]` 表示花园中一棵树的位置坐标。  
请使用最短长度的绳子将整个花园围住，因为绳子很贵。只有当所有的树都被围栏（fence）包围时，花园才算是完整围住的。  
返回恰好位于围栏（fence）边界上的树的坐标。答案的顺序可以任意。

**示例 1：**  
（此处原题仅列出标题，无具体内容）

**示例 2：**  
（此处原题仅列出标题，无具体内容）

**约束条件：**
- `1 <= trees.length <= 3000`
- `trees[i].length == 2`
- `0 <= xi, yi <= 100`
- 所有给出的坐标互不相同

**示例：**

示例 1:  
```
Input: trees = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]
Output: [[1,1],[2,0],[4,2],[3,3],[2,4]]
Explanation: 除了坐标为 [2, 2] 的树外，所有树都位于围栏的边界上，坐标为 [2, 2] 的树在围栏内部。
```

示例 2:  
```
Input: trees = [[1,2],[2,2],[4,2]]
Output: [[4,2],[2,2],[1,2]]
Explanation: 围栏形成一条直线，所有树都在这条直线上。
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一条可能的线段都当成“围栏的边”，看看它是不是在凸包的边上**。  

- **数据结构**：我们只需要一个二维列表 `points` 来存放所有树的坐标。  
- **生活化类比**：把每棵树想成一张贴在平面纸上的贴纸，围栏就像一根根用细线拉起的绳子。我们要找出哪些绳子（即哪些点对）能够把所有贴纸全部包在它的左侧（或右侧），这根绳子就一定在围栏的边上。  
- **为什么正确**：如果一条线段的两端点是凸包上的相邻点，那么所有其它点必然全部位于这条线段的同一侧（或者恰好在同一直线上）。因此只要遍历所有点对，检验“所有点是否都在同侧”，就能把所有凸包的边找出来，进而得到凸包上的所有点。  

**步骤**  

1. 对每一对不同的点 `i, j`（`i < j`），把它们当成一条候选边。  
2. 计算向量 `AB = (xj‑xi, yj‑yi)`。  
3. 对所有其它点 `k`，计算向量 `AC = (xk‑xi, yk‑yi)`，求 **叉积** `cross = AB.x * AC.y - AB.y * AC.x`。  
   - 如果 `cross > 0`，点 `k` 在 `AB` 的左侧；  
   - 如果 `cross < 0`，点 `k` 在右侧；  
   - 如果 `cross == 0`，点 `k` 在同一直线上。  
4. 只要出现了左侧和右侧两种情况（即 `cross` 既有正又有负），说明这条线段 **不可能** 是凸包的边。  
5. 若所有 `cross` 的符号只出现一种（全正、全负或全为 0），则这条线段一定在凸包上。把它的两个端点加入答案集合。  
6. 最后把答案集合去重，即得到所有在围栏上的树。

> **注意**：如果所有点都在同一直线上，围栏退化成一条直线，这种情况下每两个端点之间的连线都满足“同侧”条件，答案就是所有点本身。

#### 代码（Python）  

```python
from typing import List, Set, Tuple

def outer_trees_bruteforce(trees: List[List[int]]) -> List[List[int]]:
    n = len(trees)
    # 用集合保存结果，自动去重
    hull: Set[Tuple[int, int]] = set()

    # 遍历所有点对 (i, j)
    for i in range(n):
        xi, yi = trees[i]
        for j in range(i + 1, n):
            xj, yj = trees[j]

            # 向量 AB
            dx = xj - xi
            dy = yj - yi

            pos = neg = False   # 记录是否出现左侧/右侧

            # 检查所有其它点相对 AB 的位置
            for k in range(n):
                if k == i or k == j:
                    continue
                xk, yk = trees[k]
                # 向量 AC
                cross = dx * (yk - yi) - dy * (xk - xi)

                if cross > 0:
                    pos = True
                elif cross < 0:
                    neg = True

                # 同时出现左右两侧，说明这条边不在凸包上，直接退出
                if pos and neg:
                    break

            # 若没有同时出现左右两侧，则 (i, j) 是凸包边
            if not (pos and neg):
                hull.add((xi, yi))
                hull.add((xj, yj))

    # 把集合转换成题目要求的列表形式
    return [list(p) for p in hull]
```

> 关键行解释（中文注释已在代码中）  
> - `cross = dx * (yk - yi) - dy * (xk - xi)`：这就是**叉积**，它的符号告诉我们点 `k` 在直线 `ij` 的哪一侧。  
> - `if not (pos and neg):`：只要没有出现“左侧”和“右侧”并存的情况，这条线段就一定在凸包上。  

#### 复杂度  

- **时间复杂度**：`O(n³)`。  
  - 外层两层循环遍历所有点对，数量是 `C(n,2) ≈ n²/2`；  
  - 内层再遍历其余点检查方向，最坏情况是 `O(n)`。  
  - 所以总体是 `n² * n = n³`。  
  - 用大白话说，就是如果树有 1000 棵，程序会做大约 **10⁹** 次基本运算，明显太慢。  

- **空间复杂度**：`O(n)`。  
  - 只用了一个集合保存答案，最多存 `n` 个点的坐标。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每条候选边都要遍历全部点**，导致 `O(n³)`。  
事实上，求“所有在围栏上的点”本质上是**求平面点集的凸包（Convex Hull）**，而凸包可以在 `O(n log n)` 时间内完成。  

下面采用 **单调栈（Monotone Chain）**（又叫 Andrew’s algorithm）实现凸包：

1. **先排序**  
   - 按 **x 坐标升序** 排序；若 x 相同，再按 **y 坐标升序**。  
   - 类比：把所有树排成一列，从左到右、从下到上，这样我们只需要一次遍历就能把“下边缘”和“上边缘”分别挑出来。  
   - 排序的时间是 `O(n log n)`（因为比较排序的下界就是 `log n`）。

2. **构造下半凸包**（左到右）  
   - 使用一个栈 `lower`，依次把排序后的点压进去。  
   - 每压入一个新点 `p`，检查栈顶的最后两个点 `q, r`（`r` 是栈顶，`q` 是次顶），看 `q → r → p` 是否 **左转**（即叉积 > 0）。  
   - **左转** 表示当前路径仍然在凸包的下边缘，保留；  
   - **右转或共线**（叉积 ≤ 0）说明 `r` 已经不是下半凸包的一部分，需要弹出 `r`。  
   - 重复弹出直到形成左转，再把 `p` 放进去。  

3. **构造上半凸包**（右到左）  
   - 同理，只是遍历排序后的点的逆序，得到上半凸包 `upper`。  

4. **合并**  
   - 把 `lower` 和 `upper` 合在一起（去掉首尾重复的点），得到完整的凸包。  
   - 为了满足题目要求“所有在围栏上的点”，我们必须 **保留所有共线的点**（即在同一直线上的点也算在围栏上）。  
   - 在上述弹出条件中，把 “叉积 < 0” 当作右转弹出，而把 “叉积 = 0”（共线）**不弹出**，这样所有在边界上的点都会保留下来。  

5. **返回结果**  
   - 把合并后的点集合转成列表返回即可，顺序无要求。  

#### 代码（Python）  

```python
from typing import List

def cross(o: List[int], a: List[int], b: List[int]) -> int:
    """
    计算向量 OA × OB 的叉积
    >0 : o->a 到 o->b 为左转
    <0 : 为右转
    =0 : 共线
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def outer_trees(trees: List[List[int]]) -> List[List[int]]:
    # 1. 特殊情况：点数 ≤ 2 时全部返回
    if len(trees) <= 2:
        return trees[:]

    # 2. 按 x 再 y 排序
    points = sorted(trees, key=lambda p: (p[0], p[1]))

    lower: List[List[int]] = []   # 下半凸包
    for p in points:
        # 当出现右转时弹出栈顶点；共线时不弹，保留在边界上
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
            lower.pop()
        lower.append(p)

    upper: List[List[int]] = []   # 上半凸包
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:
            upper.pop()
        upper.append(p)

    # 3. 合并上下半凸包（去掉首尾重复点）
    # lower[-1] == upper[-1] == 最右侧点，lower[0] == upper[0] == 最左侧点
    hull = lower[:-1] + upper[:-1]

    # 4. 去重（因为共线点可能在上下两条链里都出现）
    unique = []
    seen = set()
    for p in hull:
        tup = (p[0], p[1])
        if tup not in seen:
            seen.add(tup)
            unique.append(p)

    return unique
```

> **关键行中文解释**  
> - `cross(lower[-2], lower[-1], p) < 0`：如果最近的两个点加上新点形成**右转**，说明栈顶点不在下半凸包上，需要弹出。  
> - `while len(lower) >= 2 ...`：循环弹出，直到栈顶形成左转或共线。  
> - `lower[:-1] + upper[:-1]`：把下半和上半拼起来，去掉两端重复的端点（最左/最右的点各出现两次）。  
> - `if tup not in seen:`：再次去重，确保每个边界点只出现一次。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`。  
  - 排序耗时 `O(n log n)`，是主导因素。  
  - 构造上下凸包各遍历一次点集，弹出操作总体也是线性 `O(n)`。  
  - 与暴力解 `O(n³)` 相比，提升了 **指数级**，即使 3000 棵树也能在毫秒级完成。  

- **空间复杂度**：`O(n)`。  
  - 需要额外的列表 `lower、upper、hull`，最坏情况每个列表都可能存 `n` 个点。  

---

## 心得  

- **核心技巧**：**单调栈求凸包（Monotone Chain）**，配合**叉积判断转向**。  
- **适用题型**：  
  1. “外接凸包”类（如 LeetCode 587 – Erect the Fence、218 – The Skyline Problem 的几何变形）。  
  2. “最小包围矩形”或 “最远点对” 等需要先求凸包的几何问题。  
  3. “寻找所有极值点”——比如求二维点集的上凸包或下凸包。  
- **一句话总结**：**先把点排好序，用栈把左转的路径保留下来，右转的点统统弹出，就能在 O(n log n) 内得到围栏的全部边界点。**  

---

## 反思  

- **第一反应**：看到“返回所有在围栏上的树”，立刻联想到“凸包”。如果不熟悉凸包，可能会想遍历所有组合的线段——这就是暴力思路。  
- **最容易踩的坑**：  
  - **共线点**：题目要求把所有在边界上的点都返回，不能像普通凸包那样只保留端点。实现时要把 “叉积 = 0” 当作 **左转**（不弹出），否则会遗漏边上的树。  
  - **全线性情况**：所有点在同一直线上时，凸包退化为一条线，仍需返回所有点。单调栈实现天然支持，只要不要把共线点弹掉即可。  
  - **去重**：上、下半凸包拼接时端点会出现两次，需要手动去重。  
- **下次遇到同类题**，第一步应该思考：**这是不是在求点集的最小/最大几何包围**？如果是，就直接把目光投向 **凸包算法**（Graham scan、Monotone chain、Jarvis march），并记得处理共线点的特殊要求。