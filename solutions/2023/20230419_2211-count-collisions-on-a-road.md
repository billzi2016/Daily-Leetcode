# #2211. 道路上的碰撞计数 / Count Collisions on a Road

> 难度：中等 · 标签：String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-collisions-on-a-road/)

---

## 题目（英文原版）

**Description**

There are n cars on an infinitely long road. The cars are numbered from 0 to n - 1 from left to right and each car is present at a unique point.
You are given a 0-indexed string directions of length n. directions[i] can be either 'L', 'R', or 'S' denoting whether the ith car is moving towards the left, towards the right, or staying at its current point respectively. Each moving car has the same speed.
The number of collisions can be calculated as follows:
After a collision, the cars involved can no longer move and will stay at the point where they collided. Other than that, cars cannot change their state or direction of motion.
Return the total number of collisions that will happen on the road.

**Examples**

**Example 1:**

```
Input: directions = "RLRSLL"
Output: 5
Explanation:
The collisions that will happen on the road are:
- Cars 0 and 1 will collide with each other. Since they are moving in opposite directions, the number of collisions becomes 0 + 2 = 2.
- Cars 2 and 3 will collide with each other. Since car 3 is stationary, the number of collisions becomes 2 + 1 = 3.
- Cars 3 and 4 will collide with each other. Since car 3 is stationary, the number of collisions becomes 3 + 1 = 4.
- Cars 4 and 5 will collide with each other. After car 4 collides with car 3, it will stay at the point of collision and get hit by car 5. The number of collisions becomes 4 + 1 = 5.
Thus, the total number of collisions that will happen on the road is 5.
```

**Example 2:**

```
Input: directions = "LLRR"
Output: 0
Explanation:
No cars will collide with each other. Thus, the total number of collisions that will happen on the road is 0.
```

**Constraints**

- 1 <= directions.length <= 105
- directions[i] is either 'L', 'R', or 'S'.

---

## 题目（中文翻译）

**描述**  
在一条无限长的道路 (road) 上共有 `n` 辆汽车。汽车从左到右依次编号为 `0` 到 `n-1`，每辆汽车都位于唯一的位置。  
给定一个下标从 `0` 开始、长度为 `n` 的字符串 `directions`，其中 `directions[i]` 可能为 `'L'`、`'R'` 或 `'S'`，分别表示第 `i` 辆汽车向左移动、向右移动或保持静止。所有移动的汽车具有相同的速度 (speed)。  

**碰撞计数** 的规则如下：  
- 当两辆或多辆汽车相遇时会发生碰撞 (collision)。碰撞后，涉及的所有汽车将不再移动，并停留在碰撞发生的点上。  
- 除此之外，汽车不能改变其状态或运动方向 (direction)。  

返回道路上最终会发生的 **碰撞次数** 的总和。

---

### 示例

**示例 1**  
```text
Input: directions = "RLRSLL"
Output: 5
Explanation:
道路上会发生的碰撞如下：
- 汽车 0 与汽车 1 碰撞。它们的运动方向相反，产生 2 次碰撞 → 总计 0 + 2 = 2。
- 汽车 2 与汽车 3 碰撞。汽车 3 本来是静止的，产生 1 次碰撞 → 总计 2 + 1 = 3。
- 汽车 3 与汽车 4 碰撞。由于汽车 3 已在前一次碰撞后停住，产生 1 次碰撞 → 总计 3 + 1 = 4。
- 汽车 4 与汽车 5 碰撞。汽车 4 已停住，产生 1 次碰撞 → 总计 4 + 1 = 5。

因此最终的碰撞次数为 5。
```

**示例 2**  
```text
Input: directions = "LLRR"
Output: 0
Explanation:
没有任何汽车会相互碰撞，故道路上发生的碰撞次数为 0。
```

---

### 约束条件
- `1 <= directions.length <= 10^5`
- `directions[i]` 只能是 `'L'`、`'R'` 或 `'S'`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每辆车当成一个小人，按照它们的方向一步步走**，每走一步检查相邻的两辆车是否会在同一点相遇。  
- 如果左边的车向右 (`R`) 而右边的车向左 (`L`)，它们会在中间相撞，两辆车都停下来，碰撞次数加 **2**。  
- 如果一辆车向右 (`R`) 碰到一辆已经停住的车（原本是 `S` 或者之前已经相撞），只会把自己撞停，碰撞次数加 **1**（因为停住的车已经算过了）。  

在实现时可以把每辆车的**当前位置**和**是否已经停住**存到数组里，循环模拟时间的推移，直到所有车都不再移动。  
> 类比：这就像在玩“踩格子”游戏，每一步都要检查左右两格是否有人，若有人就“踩”住他。

#### 代码（Python）

```python
def countCollisions_bruteforce(directions: str) -> int:
    n = len(directions)
    # 记录每辆车的当前位置（这里用下标表示），以及是否已经停住
    pos = list(range(n))               # 初始位置就是下标
    stopped = [c == 'S' for c in directions]   # S 的车一开始就停住
    dir_map = {'L': -1, 'R': 1, 'S': 0}
    dirs = [dir_map[c] for c in directions]

    collisions = 0
    # 最坏情况下，最多需要走 n 步（每一步都可能让一辆车停下）
    for _ in range(n):
        # 先把所有还能动的车往前一步
        for i in range(n):
            if not stopped[i]:
                pos[i] += dirs[i]

        # 检查是否有车在同一位置相遇
        # 用一个哈希表把位置映射到出现的车下标，类似“查字典”
        location = {}
        for i, p in enumerate(pos):
            if p not in location:
                location[p] = [i]
            else:
                location[p].append(i)

        # 处理碰撞
        for cars in location.values():
            if len(cars) >= 2:                     # 同一点上有 >=2 辆车
                # 只要有一辆是已经停住的，碰撞次数只加上移动的车数
                moving = [i for i in cars if not stopped[i]]
                if moving:
                    collisions += len(moving)      # 每辆移动的车都算一次
                    for i in moving:
                        stopped[i] = True          # 碰到后立刻停住
                else:
                    # 全都是移动的车（必然是相向而行），两辆车都停
                    collisions += len(cars)        # 每辆车都算一次
                    for i in cars:
                        stopped[i] = True

        # 所有车都停住了，提前结束
        if all(stopped):
            break

    return collisions
```

> **注意**：这段代码只用于说明思路，实际运行时间会随 `n` 的增大而急剧增长，`n` 达到 10⁵ 时会超时。

#### 复杂度  

- **时间复杂度**：`O(n²)`。每一步都要遍历全部车辆并检查碰撞，最坏情况下需要 `n` 步，每步 `O(n)`，所以是二次方。可以把 `O(n²)` 想象成“每辆车要和所有其他车“约会”一次”。  
- **空间复杂度**：`O(n)`。我们保存了位置、是否停住等信息，和输入长度成线性关系。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到**瓶颈在于逐步模拟**——每一步都遍历全部车辆。其实我们并不需要真的去“跑”。  
观察题目可以得到以下关键事实：

1. **永远不会相撞的车**  
   - 最左边连续出现的 `L`（一直向左走）永远跑向无穷左侧，不会碰到别的车。  
   - 最右边连续出现的 `R`（一直向右走）永远跑向无穷右侧，也不会碰撞。  

2. **其它位置的车必然会碰撞**  
   - 只要一辆车不是上面两类“安全”车，它最终都会停下来（因为左边或右边一定有阻挡它前进的车）。  
   - 碰撞次数只统计**移动的车**（`L`、`R`），原本就是 `S` 的车不计数。  

于是我们只要 **把左端的连续 `L`、右端的连续 `R` 剔除**，其余区间里所有的 `L`、`R` 都会贡献一次碰撞。  

> 类比：把道路想象成一条长长的跑道，左边的 “左走小孩” 永远跑向左边的围墙，右边的 “右走小孩” 永远跑向右边的围墙，只有站在围墙之间的孩子们会相互碰撞。  

**实现步骤**  

1. 用两个指针 `i`、`j` 分别从左、右扫描，跳过所有连续的 `L`（左端）和 `R`（右端）。  
2. 剩下的区间是 `[i, j]`（如果 `i > j` 说明整条路都是安全车，答案为 0）。  
3. 在区间 `[i, j]` 中统计字符不是 `'S'` 的个数，即为答案。  

#### 代码（Python）

```python
def countCollisions(directions: str) -> int:
    """
    返回所有会发生的碰撞次数。
    思路：剔除左端的连续 L 和右端的连续 R，其余位置的 L/R 必然会碰撞。
    """
    n = len(directions)
    i = 0
    # 跳过最左边一直向左的车，它们永远不会相撞
    while i < n and directions[i] == 'L':
        i += 1

    j = n - 1
    # 跳过最右边一直向右的车，它们也永远不会相撞
    while j >= 0 and directions[j] == 'R':
        j -= 1

    # 如果 i > j，说明整个字符串都是安全的车，直接返回 0
    if i > j:
        return 0

    # 在剩余区间统计非 'S' 的字符个数，即为会碰撞的移动车数
    collisions = 0
    for k in range(i, j + 1):
        if directions[k] != 'S':
            collisions += 1
    return collisions
```

> **代码解释**（每行中文注释已写在代码里），核心只用了两次线性遍历，**时间 O(n)**，**额外空间 O(1)**。

#### 复杂度  

- **时间复杂度**：`O(n)`。只需要一次从左到右和一次从右到左的扫描，`n` 最高 10⁵，完全可接受。  
- **空间复杂度**：`O(1)`。只用了若干指针和计数器，与输入规模无关。

---

## 心得  

- **核心技巧**：**排除永远不会相撞的车**（左端的 `L`、右端的 `R`），其余所有移动的车必然会停下。  
- **适用的题型**  
  1. “**只需要统计会发生的事件**”而不必真正模拟的题目（例如 LeetCode 2210 “Count Hills and Valleys in an Array”）。  
  2. **一次性剔除两端安全元素**的线性扫描问题（如 “Number of Cars That Can Reach the Destination”）。  
- **一句话总结解题钥匙**：**左端的左走、右端的右走永不碰撞，其余全部碰撞**。

---

## 反思  

- **第一反应**：直接想把所有车逐步移动、碰撞，写一个完整的模拟器。  
- **最容易踩的坑**  
  - 忽略了原本停住的 `S` 车不计入碰撞次数，只是“撞”它们的移动车才算。  
  - 没有考虑到 **全部是安全车** 的极端情况（如 `"LLL"` 或 `"RRR"`），会导致 `i > j`，需要单独返回 0。  
- **下次遇到同类题**：第一步先思考**哪些元素永远不参与交互**（两端的单向元素），然后把问题转化为**区间统计**，避免完整的模拟。