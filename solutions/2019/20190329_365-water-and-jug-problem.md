# #365. 水壶问题 / Water and Jug Problem

> 难度：中等 · 标签：Math、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/water-and-jug-problem/)

---

## 题目（英文原版）

**Description**

You are given two jugs with capacities x liters and y liters. You have an infinite water supply. Return whether the total amount of water in both jugs may reach target using the following operations:

**Examples**

**Example 1:**

```
Input: x = 3, y = 5, target = 4
Output: true
Explanation:
Follow these steps to reach a total of 4 liters:
Reference: The Die Hard example.
```

**Example 2:**

```
Input: x = 2, y = 6, target = 5
Output: false
```

**Example 3:**

```
Input: x = 1, y = 2, target = 3
Output: true
Explanation: Fill both jugs. The total amount of water in both jugs is equal to 3 now.
```

**Constraints**

- 1 <= x, y, target <= 103

---

## 题目（中文翻译）

You are given two jugs with capacities `x` liters and `y` liters. You have an infinite water supply. Return whether the total amount of water in both jugs may reach `target` using the following operations.

### 示例

#### 示例 1
**Input:** `x = 3, y = 5, target = 4`  
**Output:** `true`  
**Explanation:**  
按照以下步骤即可得到 4 升的总量：  
（参考《虎胆龙威》中的示例）

#### 示例 2
**Input:** `x = 2, y = 6, target = 5`  
**Output:** `false`

#### 示例 3
**Input:** `x = 1, y = 2, target = 3`  
**Output:** `true`  
**Explanation:**  
把两个壶都装满。此时两个壶中水的总量等于 3 升。

### 约束条件
- `1 <= x, y, target <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把**所有可能的状态**都枚举一遍，然后看有没有哪一种状态的两壶水量之和恰好等于 `target`。  
- **状态**可以用一个二元组 `(a, b)` 表示，`a` 表示壶 x 里当前的水量，`b` 表示壶 y 里当前的水量。  
- 每一次操作都可以把我们从一个状态转移到另一个状态，常见的 6 种操作如下（把它们想成「游戏的按钮」）  
  1. 把壶 x 装满 → `(x, b)`  
  2. 把壶 y 装满 → `(a, y)`  
  3. 把壶 x 倒空 → `(0, b)`  
  4. 把壶 y 倒空 → `(a, 0)`  
  5. 把壶 x 的水倒进壶 y ，直到壶 x 空或壶 y 满 → `(max(0, a - (y-b)), min(y, b+a))`  
  6. 把壶 y 的水倒进壶 x ，直到壶 y 空或壶 x 满 → `(min(x, a+b), max(0, b - (x-a)))`  

把这些按钮一次次按下，就会遍历出所有 **可达** 的 `(a, b)`。  
我们只要在遍历的过程中检查 `a + b == target`，如果出现一次就返回 `True`，遍历完都没有则返回 `False`。

> **类比**：把状态看成城市，用 `a+b` 看成城市的“海拔”。我们在地图上跑来跑去，只要爬到海拔恰好等于 `target` 的山顶，就算成功。

为什么一定能找对答案？因为 BFS（广度优先搜索）会把 **所有** 能够通过合法操作得到的状态都访问一次，漏掉的状态不存在。

#### 代码（Python）

```python
from collections import deque

def can_measure_bruteforce(x: int, y: int, target: int) -> bool:
    # 特殊情况：直接装满两壶就已经等于 target
    if x + y == target:
        return True
    # BFS 用队列存放待探索的状态
    queue = deque()
    queue.append((0, 0))               # 初始状态，两壶都空
    visited = set()                    # 记录已经访问过的状态，防止死循环
    visited.add((0, 0))

    while queue:
        a, b = queue.popleft()
        # 如果当前两壶水量之和等于目标，成功
        if a + b == target:
            return True

        # 生成所有可能的下一步状态
        next_states = [
            (x, b),                     # 把壶 x 装满
            (a, y),                     # 把壶 y 装满
            (0, b),                     # 把壶 x 倒空
            (a, 0),                     # 把壶 y 倒空
            (max(0, a - (y - b)), min(y, b + a)),   # 把 x 倒进 y
            (min(x, a + b), max(0, b - (x - a)))    # 把 y 倒进 x
        ]

        for na, nb in next_states:
            if (na, nb) not in visited:
                visited.add((na, nb))
                queue.append((na, nb))

    # 所有可达状态遍历完仍未找到目标
    return False
```

#### 复杂度  

- **时间复杂度**：`O(x * y)`  
  每个壶的水量只能是 `0 … x`（或 `0 … y`）之间的整数，总状态数上限是 `(x+1)*(y+1)`，即大约 `x*y`。我们最多遍历一次所有状态，所以时间和状态数成正比。  
  用大白话说，如果 `x=1000, y=1000`，最坏情况下要检查约 **一百万** 种可能。

- **空间复杂度**：`O(x * y)`  
  `visited` 集合需要保存所有已经遍历的状态，同样是最多 `x*y` 条记录。队列的最大长度也不会超过这个数量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有状态**，当 `x`、`y` 较大时会非常慢。其实我们并不需要真的模拟倒水的过程，只要利用一点数学知识就能直接判断是否可行。

观察操作的本质：  
- 每一次倒水、倒空、装满，实际上都是在 **把水量加上或减去** 壶的容量 `x`、`y` 的整数倍。  
- 这与**“把两个数的线性组合”**非常相似：我们可以得到的任意水量 `k` 必须满足  

\[
k = m \times x + n \times y
\]

其中 `m、n` 为整数（可以为负，负数对应倒空或倒回去的操作）。  
根据**数论中的 Bézout 定理**，所有可以表示成 `m·x + n·y` 的整数，恰好是 `gcd(x, y)`（`x` 与 `y` 的最大公约数）的整数倍。

因此，要想让 **两壶水量之和** 能等于 `target`，必须满足两个必要条件：

1. **目标不能超过两壶的总容量**  
   \[
   target \le x + y
   \]
   （因为我们只能装满两壶，最多拥有 `x+y` 升水）

2. **目标必须是 `gcd(x, y)` 的倍数**  
   \[
   target \bmod \text{gcd}(x, y) = 0
   \]

这两个条件同时成立时，必定存在一系列合法操作让两壶的水量之和恰好等于 `target`。不需要真的去找具体的倒水步骤。

> **类比**：把 `x`、`y` 想成两根尺子，只有它们的最小公因子（gcd）才能“拼出”其他长度。只要目标长度不超过两根尺子相加的总长，并且能被那根最小公因子整除，就一定能拼出来。

#### 代码（Python）

```python
import math

def can_measure_optimal(x: int, y: int, target: int) -> bool:
    """
    使用数论快速判断是否能得到 target 升水。
    1. target 不能超过两壶的总容量 x + y
    2. target 必须是 gcd(x, y) 的倍数
    """
    # 目标大于两壶总容量，显然不可能
    if target > x + y:
        return False

    # 计算 x 与 y 的最大公约数
    g = math.gcd(x, y)

    # 判断 target 是否能被 g 整除
    return target % g == 0
```

#### 复杂度  

- **时间复杂度**：`O(log min(x, y))`  
  计算最大公约数 `gcd` 使用欧几里得算法，其复杂度是对数级的。相较于暴力的 `O(x*y)`，这几乎是瞬间完成的。

- **空间复杂度**：`O(1)`  
  只用了常数个变量，没有额外的数组或集合。

---

## 心得

- **核心技巧**：**Bézout 定理 + 最大公约数**。只要把问题抽象成“能否用两个数的整数线性组合得到目标”，就可以用 gcd 判定。
- **适用的题型**  
  1. “水壶问题”系列（测量指定体积）  
  2. “是否能用若干硬币凑出指定金额”——本质也是检查金额是否是硬币面额的 gcd 的倍数（在只有两种硬币且可以正负使用时）  
  3. “能否把两根绳子剪成相同长度”——涉及 gcd 的划分。
- **一句话总结**：只要目标 ≤ 两壶容量之和且能被 `gcd(x, y)` 整除，答案必为 `True`。

---

## 反思

- **第一反应**：直接想到模拟倒水的六种操作，用 BFS 或 DFS 把所有状态遍历一遍。  
- **最容易踩的坑**  
  1. **忘记检查上限**：`target` 大于 `x+y` 时即使满足 gcd 条件也不可能，因为水总量不够。  
  2. **边界情况**：当 `x` 或 `y` 为 `0`（虽然题目约束不允许）时，需要单独处理。  
  3. **整数溢出**：在某些语言里 `m·x + n·y` 可能超出范围，但我们用数学判定根本不需要实际计算大数。  
- **下次类似题的第一步**：先把问题抽象为“是否能用两个数的整数线性组合得到目标”，立即检查 `target ≤ x+y` 和 `target % gcd(x, y) == 0`，若不满足直接返回 `False`，否则返回 `True`。这样既快速又可靠。