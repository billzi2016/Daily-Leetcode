# #1665. 最小初始能量完成任务 / Minimum Initial Energy to Finish Tasks

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/)

---

## 题目（英文原版）

**Description**

You are given an array tasks where tasks[i] = [actuali, minimumi]:
For example, if the task is [10, 12] and your current energy is 11, you cannot start this task. However, if your current energy is 13, you can complete this task, and your energy will be 3 after finishing it.
You can finish the tasks in any order you like.
Return the minimum initial amount of energy you will need to finish all the tasks.

**Examples**

**Example 1:**

```
Input: tasks = [[1,2],[2,4],[4,8]]
Output: 8
Explanation:
Starting with 8 energy, we finish the tasks in the following order:
    - 3rd task. Now energy = 8 - 4 = 4.
    - 2nd task. Now energy = 4 - 2 = 2.
    - 1st task. Now energy = 2 - 1 = 1.
Notice that even though we have leftover energy, starting with 7 energy does not work because we cannot do the 3rd task.
```

**Example 2:**

```
Input: tasks = [[1,3],[2,4],[10,11],[10,12],[8,9]]
Output: 32
Explanation:
Starting with 32 energy, we finish the tasks in the following order:
    - 1st task. Now energy = 32 - 1 = 31.
    - 2nd task. Now energy = 31 - 2 = 29.
    - 3rd task. Now energy = 29 - 10 = 19.
    - 4th task. Now energy = 19 - 10 = 9.
    - 5th task. Now energy = 9 - 8 = 1.
```

**Example 3:**

```
Input: tasks = [[1,7],[2,8],[3,9],[4,10],[5,11],[6,12]]
Output: 27
Explanation:
Starting with 27 energy, we finish the tasks in the following order:
    - 5th task. Now energy = 27 - 5 = 22.
    - 2nd task. Now energy = 22 - 2 = 20.
    - 3rd task. Now energy = 20 - 3 = 17.
    - 1st task. Now energy = 17 - 1 = 16.
    - 4th task. Now energy = 16 - 4 = 12.
    - 6th task. Now energy = 12 - 6 = 6.
```

**Constraints**

- 1 <= tasks.length <= 105
- 1 <= actual​i <= minimumi <= 104

---

## 题目（中文翻译）

**描述**  
给定一个数组 `tasks`，其中 `tasks[i] = [actual_i, minimum_i]`：

- `actual_i` 表示完成第 *i* 项任务后会消耗的能量。  
- `minimum_i` 表示开始第 *i* 项任务前所需的最小能量。

例如，任务 `[10, 12]` 表示如果你当前的能量为 11，则无法开始该任务；但如果当前能量为 13，则可以完成该任务，完成后剩余能量为 `13 - 10 = 3`。

你可以按照任意顺序完成所有任务。返回完成所有任务所需的**最小初始能量**。

**示例 1**  
```
Input: tasks = [[1,2],[2,4],[4,8]]
Output: 8
Explanation:
从 8 能量开始，我们按以下顺序完成任务：
- 第 3 项任务。此时能量 = 8 - 4 = 4。
- 第 2 项任务。此时能量 = 4 - 2 = 2。
- 第 1 项任务。此时能量 = 2 - 1 = 1。

即使还有剩余能量，若从 7 能量开始也无法完成第 3 项任务，因此 8 为最小答案。
```

**示例 2**  
```
Input: tasks = [[1,3],[2,4],[10,11],[10,12],[8,9]]
Output: 32
Explanation:
从 32 能量开始，我们按以下顺序完成任务：
- 第 1 项任务。此时能量 = 32 - 1 = 31。
- 第 2 项任务。此时能量 = 31 - 2 = 29。
- 第 3 项任务。此时能量 = 29 - 10 = 19。
- 第 4 项任务。此时能量 = 19 - 10 = 9。
- 第 5 项任务。此时能量 = 9 - 8 = 1。
```

**示例 3**  
```
Input: tasks = [[1,7],[2,8],[3,9],[4,10],[5,11],[6,12]]
Output: 27
Explanation:
从 27 能量开始，我们按以下顺序完成任务：
- 第 5 项任务。此时能量 = 27 - 5 = 22。
- 第 2 项任务。此时能量 = 22 - 2 = 20。
- 第 3 项任务。此时能量 = 20 - 3 = 17。
- 第 1 项任务。此时能量 = 17 - 1 = 16。
- 第 4 项任务。此时能量 = 16 - 4 = 12。
- 第 6 项任务。此时能量 = 12 - 6 = 6。
```

**约束条件**  
- `1 <= tasks.length <= 10^5`  
- `1 <= actual_i <= minimum_i <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有任务的执行顺序枚举出来**，逐个尝试，看哪一种顺序能够在最小的初始能量下把所有任务都做完。  
- **数据结构**：我们可以把任务看成一张“任务卡片”。枚举顺序就像把这些卡片全部排成一条线，所有可能的排法就是所有**排列**（permutation）。  
- **为什么可行**：只要遍历到所有排列，就一定能找到一种最优的执行顺序（如果它真的存在的话），因为我们没有对顺序做任何限制。  
- **时间/空间复杂度**：  
  - 枚举 `n` 张卡片的全部排列，需要 `n!`（n 的阶乘）种可能。对每一种排列我们都要模拟一次任务执行，模拟过程是 `O(n)`。所以总时间是 `O(n! * n)`，这在 `n` 稍大（比如 10 以上）时就几乎不可能跑完。  
  - 只需要保存当前排列以及一点临时变量，空间是 `O(n)`（保存排列本身），不算额外开销。

> **大白话**：`O(n!)` 就像把所有可能的钥匙都试一遍才能打开门，钥匙多了根本没时间一个个试。

#### 代码（Python）

```python
import itertools
from typing import List

def min_initial_energy_bruteforce(tasks: List[List[int]]) -> int:
    """
    暴力枚举所有执行顺序，返回最小的初始能量。
    只适合任务数很少的情况（例如 n <= 8）。
    """
    n = len(tasks)
    ans = float('inf')                       # 记录全局最小的初始能量
    for order in itertools.permutations(range(n)):   # 所有排列
        # 先猜一个足够大的初始能量，随后逐步减小
        # 这里用二分法求最小可行值会更快，但为了演示暴力，这里直接线性递增
        need = 0
        cur = 0                               # 当前能量
        # 先把所有任务的 minimum 累加，得到一个上界
        upper = sum(m for _, m in tasks) + 1
        for init in range(upper):             # 逐个尝试初始能量
            cur = init
            ok = True
            for idx in order:
                actual, minimum = tasks[idx]
                if cur < minimum:             # 能量不足，任务无法开始
                    ok = False
                    break
                cur -= actual                 # 完成任务后能量下降
            if ok:                             # 找到第一个能完成所有任务的 init
                need = init
                break
        ans = min(ans, need)                  # 更新全局最小值
    return ans
```

> **关键注释**  
> - `itertools.permutations` 把任务下标排成所有可能的顺序。  
> - `init` 从 0 开始递增，直到找到能完成全部任务的最小初始能量。  
> - 这种实现只能在 `tasks` 很少（比如 ≤ 8）时跑得完。

#### 复杂度

- **时间复杂度**：`O(n! * n * E)`，其中 `E` 是尝试的初始能量上界（约等于所有 `minimum` 的和）。对实际数据几乎不可接受。  
- **空间复杂度**：`O(n)`，只存储当前排列和几个临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于“枚举所有顺序”。我们需要找到一种**贪心**的顺序，使得只要按这个顺序执行，**只用一次遍历就能判断是否可行**，从而直接算出最小初始能量。

**关键观察**  

1. 对于某个任务 `i = [actual_i, minimum_i]`，如果我们在完成它之前已经拥有的能量是 `cur`，则必须满足 `cur ≥ minimum_i`，完成后能量变成 `cur - actual_i`。  
2. 设想把所有任务排成一条线，**前面的任务会把能量消耗掉**，所以**后面的任务要求的 `minimum` 越大越不容易满足**。于是我们倾向把 **“要求高” 的任务放在** ****前面** **。  
3. 但是只看 `minimum` 本身并不够。假设有两个任务  
   - A: `[actual=5, minimum=7]`  
   - B: `[actual=1, minimum=3]`  
   把 A 放前面需要的初始能量是 `7`，完成后剩 `2`，再做 B 需要的 `minimum=3` 已经不够；而把 B 放前面只需要 `3`，完成后剩 `2`，再做 A 仍然不够。这里我们看到 **`minimum - actual`（即任务完成后还能剩下多少“余量”）** 也很重要。  
4. **贪心原则**：把 **“余量小（甚至负）”** 的任务放在前面，因为它们会把能量消耗得更厉害，必须提前满足它们的 `minimum`。这等价于把 **`(minimum - actual)` 从大到小** 排序（即余量大的在后，余量小的在前）。  

**为什么这种排序是最优的？**  

- 设两任务 `i`、`j`，且 `i` 在前、`j` 在后。若我们把顺序调换，只有两种可能影响：  
  - 若 `minimum_i - actual_i ≥ minimum_j - actual_j`，则把 `i` 放前面不会让后面的 `j` 更难完成。  
  - 反之，把余量更小的任务提前可以降低对初始能量的要求。  
- 通过**交换相邻逆序对**（类似冒泡排序的思想）可以逐步把数组变成 “余量从大到小” 的顺序，而每一次交换都不会增加完成所有任务所需的最小初始能量。于是最终的顺序一定是最优的。

**得到最小初始能量的计算方式**  

按照上述排序后，从左到右依次执行任务：

- 设 `need` 为当前已经确定的**最小初始能量**，`cur` 为已经消耗掉的 `actual` 总和（即已完成任务后剩余的能量相对初始值的变化）。  
- 对于每个任务 `[a, m]`：  
  - 在执行它之前，我们的实际能量是 `need - cur`（因为初始能量是 `need`，已经消耗了 `cur`）。  
  - 为了满足 `need - cur ≥ m`，我们必须让 `need` 至少等于 `m + cur`。于是 `need = max(need, m + cur)`。  
  - 完成任务后，`cur += a`（累计消耗的实际能量）。  

遍历完所有任务后，`need` 就是**最小的初始能量**。

> **类比**：把 `cur` 想象成“已经走过的路程”，`need` 是“一开始准备的汽油”。每到一个加油站（任务），站的要求是“你至少要有 `minimum` 升油”。如果你已经走了 `cur` 距离（消耗了 `cur` 升），就要检查一开始准备的汽油是否足够大，保证“到达站点时油量 ≥ minimum”。如果不够，就提前在一开始多加点油（增大 `need`）。

**复杂度**  

- 排序：`O(n log n)`（`n` 最多 10⁵，完全可以接受）。  
- 单次遍历：`O(n)`。  
- 总空间：只需要常数级额外空间 `O(1)`（除去存任务本身的数组）。

#### 代码（Python）

```python
from typing import List

def min_initial_energy(tasks: List[List[int]]) -> int:
    """
    贪心 + 排序，返回完成所有任务所需的最小初始能量。
    复杂度 O(n log n) 时间，O(1) 额外空间。
    """
    # 1. 按照 (minimum - actual) 从大到小排序
    #    余量大的任务放后面，余量小（甚至负）的任务放前面
    tasks.sort(key=lambda x: x[1] - x[0], reverse=True)

    need = 0   # 当前已知的最小初始能量
    cur = 0    # 已经消耗的 actual 总和

    for actual, minimum in tasks:
        # 需要保证：need - cur >= minimum
        # => need >= minimum + cur
        need = max(need, minimum + cur)
        cur += actual      # 完成该任务后，累计消耗的 actual
    return need
```

**关键注释**  

- `lambda x: x[1] - x[0]` 计算每个任务的 **余量**（`minimum - actual`）。  
- `reverse=True` 把余量大的放在后面（即从大到小排）。  
- `need = max(need, minimum + cur)`：如果当前的 `need` 已经足够大，就保持不变；否则把它提升到刚好满足当前任务的最低要求。  
- `cur += actual` 累计已经“消耗掉的能量”，为后面的任务提供正确的基准。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n log n` 来自排序，遍历本身是线性的 `O(n)`。相较于暴力的 `n!`，速度提升几个数量级。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个整数变量 `need`、`cur`，没有额外的数组或递归栈。

---

## 心得

- **核心技巧**：**贪心排序 + 前缀累计**。先把“余量（minimum‑actual）”从大到小排好，再用一次遍历把最小初始能量算出来。  
- **适用的题型**：  
  1. “任务/项目需要先满足最小阈值后才能执行”的问题（如 LeetCode 1665 Minimum Initial Energy to Finish Tasks）。  
  2. “先付费用后获得收益”类的调度问题（比如 “最大化完成任务的奖励”）。  
  3. “先满足最低要求后消耗资源”的游戏或工程调度（如 “游戏关卡能量”或 “机器维修”）。  
- **一句话总结**：**把“先消耗多、后剩余少”的任务提前执行，按余量降序排，遍历时实时补足最小初始能量**。

---

## 反思

- **第一反应**：想到“枚举所有顺序”，因为只有顺序会影响能否满足 `minimum`。  
- **最容易踩的坑**：  
  - 忘记把 `minimum` 与已经消耗的 `actual` 累计值一起考虑，导致只比较 `minimum` 本身而出错。  
  - 排序时方向写反（把余量大的放前面），会导致答案偏大。  
  - 任务数可达 `10⁵`，若仍使用 `O(n²)` 或 `O(n!)` 的方法会超时或内存爆炸。  
- **下次遇到同类题**：第一步先**思考能否把任务按某个单调属性排序**（如 `minimum‑actual`、`deadline`、`profit‑cost`），如果可以，再用**一次遍历+前缀累计**求解最小/最大阈值。这样往往能把指数级搜索降到 `O(n log n)`。