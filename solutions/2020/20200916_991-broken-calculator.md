# #991. **破损计算器** / Broken Calculator

> 难度：中等 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/broken-calculator/)

---

## 题目（英文原版）

**Description**

There is a broken calculator that has the integer startValue on its display initially. In one operation, you can:
Given two integers startValue and target, return the minimum number of operations needed to display target on the calculator.

**Examples**

**Example 1:**

```
Input: startValue = 2, target = 3
Output: 2
Explanation: Use double operation and then decrement operation {2 -> 4 -> 3}.
```

**Example 2:**

```
Input: startValue = 5, target = 8
Output: 2
Explanation: Use decrement and then double {5 -> 4 -> 8}.
```

**Example 3:**

```
Input: startValue = 3, target = 10
Output: 3
Explanation: Use double, decrement and double {3 -> 6 -> 5 -> 10}.
```

**Constraints**

- 1 <= startValue, target <= 109

---

## 题目（中文翻译）

有一台损坏的计算器，最初显示屏上显示整数 `startValue`。一次操作（operation）中，你可以：

给定两个整数 `startValue` 和 `target`，返回在计算器上显示 `target` 所需的最少操作次数（operations）。

约束条件：

- 1 ≤ `startValue`, `target` ≤ 10^9  

---

### 示例

#### 示例 1
**输入:** `startValue = 2, target = 3`  
**输出:** `2`  
**解释:** 先使用倍增操作（double），再使用递减操作（decrement），过程为 `{2 → 4 → 3}`。

#### 示例 2
**输入:** `startValue = 5, target = 8`  
**输出:** `2`  
**解释:** 先使用递减操作（decrement），再使用倍增操作（double），过程为 `{5 → 4 → 8}`。

#### 示例 3
**输入:** `startValue = 3, target = 10`  
**输出:** `3`  
**解释:** 先使用倍增操作（double），再递减操作（decrement），随后再倍增操作（double），过程为 `{3 → 6 → 5 → 10}`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从 `startValue` 出发**，一步步尝试所有可能的操作，直到等于 `target` 为止。  
可以把这看成在一棵无限大的树上搜索：

- 树的根节点是 `startValue`  
- 每个节点有两条向下的边：  
  1. ***双倍*（`x → 2*x`）**，相当于把数字“翻倍”，像把水杯里装的水再倒满一倍。  
  2. ***减一*（`x → x-1`）**，相当于把数字往左退一步，就像在数字轴上往左走一步。

把所有可能的路径都遍历一遍，找到最短的那条，就是答案。  

实现上常用 **广度优先搜索（BFS）**：  
- 用一个队列保存当前层的所有数值。  
- 每弹出一个数，就产生它的两个后继，放进队列的下一层。  
- 当弹出的数等于 `target` 时，当前层数就是最少操作次数。

> **为什么正确？**  
> BFS 按层次展开，先访问的都是操作次数最少的状态，碰到目标值时必然是最短路径。

#### 代码（Python）

```python
from collections import deque

def broken_calculator_brute(startValue: int, target: int) -> int:
    # 特例：如果起点已经是目标，直接返回 0
    if startValue == target:
        return 0

    # 队列里保存 (当前数值, 已使用的操作次数)
    q = deque()
    q.append((startValue, 0))
    # 为了防止无限循环，需要记住已经访问过的数值
    visited = set([startValue])

    while q:
        cur, steps = q.popleft()
        # 生成两种可能的下一步
        nxt1 = cur * 2          # 双倍
        nxt2 = cur - 1          # 减一

        for nxt in (nxt1, nxt2):
            if nxt == target:               # 找到目标，返回答案
                return steps + 1
            # 只把合理且未访问过的状态压入队列
            if nxt > 0 and nxt not in visited and nxt <= 2 * target:
                visited.add(nxt)
                q.append((nxt, steps + 1))

    # 理论上永远不会走到这里，因为一定能到达 target
    return -1
```

- `visited` 防止重复搜索，避免无限循环。  
- `nxt <= 2 * target` 是一个**剪枝**：因为如果已经超过两倍的目标，再继续双倍只会让距离更远。

#### 复杂度

- **时间复杂度**：`O(2^d)`（指数级），其中 `d` 是最少操作次数。因为每一步都可能产生两个新状态，搜索树会呈指数增长。实际运行会因为剪枝而快一些，但在最坏情况下仍然很慢。  
- **空间复杂度**：`O(2^d)`，队列和 `visited` 集合需要存储同样数量的状态。

> **大白话解释**：  
> 想象你在迷宫里每走一步都有两条路可选，想找最短出路就得把所有可能的路都走遍。路越多，走的时间和记住的路数都会指数级增长，这就是暴力搜索的“慢”。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**正向搜索会产生大量无用的分支**。  
我们换个角度：**从 `target` 往回走**，使用**逆操作**，往往能大幅度降低搜索空间。

- 正向的两种操作是  
  1. `x → 2*x`（双倍）  
  2. `x → x-1`（减一）

- 逆向思考时，这两条线对应的**逆操作**是  
  1. `y → y/2`（如果 `y` 为偶数）——因为只有偶数才能是一次“双倍”得到的。  
  2. `y → y+1`（对应正向的“减一”）

逆向的好处在于：

- 当 `target` **大于** `startValue` 时，**除以 2** 能让数字快速变小，类似把大树砍倒成小树桩。  
- 当 `target` **小于或等于** `startValue` 时，唯一的办法只能是 **正向的减一**（因为再除以 2 会让它更小），此时最少操作数就是 `startValue - target`。

因此算法如下：

1. 初始化计数器 `steps = 0`。  
2. 当 `target > startValue`：  
   - 如果 `target` 为 **偶数**，执行 `target //= 2`（逆向的双倍）。  
   - 否则（奇数），执行 `target += 1`（逆向的减一），因为奇数不可能是一次“双倍”得到的，需要先加一变成偶数再除以 2。  
   - 每执行一次逆操作，`steps += 1`。  
3. 循环结束后，`target` 已经不大于 `startValue`，此时只能正向“减一”，再加上 `startValue - target` 步即得到答案。

> **核心概念——贪心**：每一步都做“当下最好的选择”（尽可能除以 2），因为除以 2 能最大程度减少后续的操作数。  

#### 代码（Python）

```python
def broken_calculator(startValue: int, target: int) -> int:
    """
    逆向贪心：从 target 向 startValue 靠拢
    """
    steps = 0
    while target > startValue:
        if target % 2 == 0:          # 偶数可以直接逆向“双倍”
            target //= 2
        else:                        # 奇数必须先加一变偶数，再除以 2
            target += 1
        steps += 1                   # 记录一次逆操作

    # 此时 target <= startValue，只能正向“减一”
    return steps + (startValue - target)
```

- `while target > startValue` 循环的次数大约是 `log₂(target)`，因为每次除以 2 都会把数字缩小一半。  
- 当 `target` 为奇数时，加一的操作相当于把它“凑齐”到下一个偶数，这一步在正向看是一次“减一”。

#### 复杂度

- **时间复杂度**：`O(log target)`  
  - 每次循环要么把 `target` 除以 2（数字减半），要么把它加 1（随后必然会除以 2），所以循环次数最多约为二进制位数，即 `log₂(target)`。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，常数级别的额外空间。

> **对比**：暴力解需要指数级的时间和空间，而最优解只需要几步“砍树”就能把大数字砍成小数字，效率提升几个数量级。

---

## 心得

- **核心技巧**：逆向贪心 + 除以 2 / 加 1 的组合。  
- **适用场景**：  
  1. **Broken Calculator**（本题）  
  2. **Minimum Operations to Reduce X to Zero**（只能减 1 或除以 2）  
  3. **Integer Replacement**（只能加 1、减 1 或除以 2）  
- **一句话总结**：**从目标倒推，尽可能把大数除以 2，剩下的差距用减一补齐**。

---

## 反思

- **第一反应**：直接从 `startValue` 正向 BFS，想把所有可能的路径都遍历一遍。  
- **最容易踩的坑**：  
  - 正向搜索会爆炸式增长，导致超时。  
  - 忘记处理 `target <= startValue` 的情况，直接除以 2 会把数字弄得更小。  
- **下次遇到同类题**：第一步想到**“能不能逆向思考？”**，把操作倒着走，往往可以把指数级搜索压缩到对数级。