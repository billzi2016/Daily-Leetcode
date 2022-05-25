# #1792. 最大平均通过率 / Maximum Average Pass Ratio

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-average-pass-ratio/)

---

## 题目（英文原版）

**Description**

There is a school that has classes of students and each class will be having a final exam. You are given a 2D integer array classes, where classes[i] = [passi, totali]. You know beforehand that in the ith class, there are totali total students, but only passi number of students will pass the exam.
You are also given an integer extraStudents. There are another extraStudents brilliant students that are guaranteed to pass the exam of any class they are assigned to. You want to assign each of the extraStudents students to a class in a way that maximizes the average pass ratio across all the classes.
The pass ratio of a class is equal to the number of students of the class that will pass the exam divided by the total number of students of the class. The average pass ratio is the sum of pass ratios of all the classes divided by the number of the classes.
Return the maximum possible average pass ratio after assigning the extraStudents students. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: classes = [[1,2],[3,5],[2,2]], extraStudents = 2
Output: 0.78333
Explanation: You can assign the two extra students to the first class. The average pass ratio will be equal to (3/4 + 3/5 + 2/2) / 3 = 0.78333.
```

**Example 2:**

```
Input: classes = [[2,4],[3,9],[4,5],[2,10]], extraStudents = 4
Output: 0.53485
```

**Constraints**

- 1 <= classes.length <= 105
- classes[i].length == 2
- 1 <= passi <= totali <= 105
- 1 <= extraStudents <= 105

---

## 题目（中文翻译）

描述  
学校有若干班级（class），每个班级都要进行期末考试。给定一个二维整数数组 `classes`，其中 `classes[i] = [passi, totali]` 表示第 `i` 个班级共有 `totali` 名学生，其中有 `passi` 名学生能够通过（pass）考试。  
另给定一个整数 `extraStudents`，表示还有 `extraStudents` 名优秀学生可以被分配到任意班级，这些学生一定会通过他们所在班级的考试。  
你的目标是将这 `extraStudents` 名学生分配到各班级，使所有班级的 **平均通过率（average pass ratio）** 最大化。  

班级的通过率（pass ratio）等于该班级能够通过的学生数除以该班级的总学生数。平均通过率是所有班级的通过率之和除以班级数量。  
返回分配完 `extraStudents` 后可能得到的最大平均通过率。答案误差在 `10^-5` 以内均视为正确。

示例  
**示例 1**  
```text
Input: classes = [[1,2],[3,5],[2,2]], extraStudents = 2
Output: 0.78333
Explanation: 你可以把两个额外学生分配到第一班级。此时的平均通过率为 (3/4 + 3/5 + 2/2) / 3 = 0.78333.
```

**示例 2**  
```text
Input: classes = [[2,4],[3,9],[4,5],[2,10]], extraStudents = 4
Output: 0.53485
```

约束条件  
- `1 <= classes.length <= 10^5`  
- `classes[i].length == 2`  
- `1 <= passi <= totali <= 10^5`  
- `1 <= extraStudents <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把每个额外的学生都尝试分配到所有可能的班级**，然后算出每种分配方式对应的平均通过率，最后取最大的那个。  
- **数据结构**：我们可以用一个一维数组 `add[i]` 表示第 `i` 个班级额外分配了多少名优秀学生。整个 `add` 数组的和必须等于 `extraStudents`。这类似于把若干颗糖果分到若干个小碗里，求所有可能的分配方式。  
- **为什么正确**：因为我们枚举了**所有**合法的分配情况，答案一定会在这些情况里出现，所以取最大值必然得到最优解。  

不过，这种做法的计算量非常大。假设有 `n` 个班级，`extraStudents = k`，则等价于在 `k` 个相同的球中找 `n-1` 条分隔线——组合数为  

\[
C(k+n-1, n-1)
\]

即“**星号与竖线**”的组合数，随着 `k`、`n` 增大会呈指数级爆炸。  

#### 代码（Python）  
下面的实现使用深度优先搜索（DFS）递归枚举所有分配方式，仅用于演示思路，**在真实测试里会超时**。

```python
from typing import List

def brute_force(classes: List[List[int]], extra: int) -> float:
    """
    暴力枚举每一种 extraStudents 的分配方式
    返回最大可能的平均通过率
    """
    n = len(classes)
    best = 0.0                     # 用来保存遍历过程中的最大平均值

    def dfs(idx: int, remain: int, adds: List[int]):
        """
        idx   : 当前正在处理的班级编号
        remain: 还剩多少额外学生未分配
        adds  : 前 idx 个班级各自得到的额外学生数量
        """
        nonlocal best
        if idx == n:               # 所有班级都已决定额外学生数
            # 计算当前分配方案的平均通过率
            total = 0.0
            for (p, t), add in zip(classes, adds):
                total += (p + add) / (t + add)
            avg = total / n
            best = max(best, avg)
            return

        # 把剩余的学生全部或者部分分配给当前班级
        for extra_here in range(remain + 1):
            adds.append(extra_here)
            dfs(idx + 1, remain - extra_here, adds)
            adds.pop()

    dfs(0, extra, [])
    return best
```

#### 复杂度  
- **时间复杂度**：`O(C(extra + n - 1, n - 1))`，即所有可能的分配方式数，随着 `extra`、`n` 增大呈指数级增长。可以把它想象成“**把 100 块糖果放进 5 个盒子**”，组合数已经是上千甚至上万，远远超出一秒能算完的范围。  
- **空间复杂度**：`O(n)`，递归栈深度最多 `n`，以及保存每个班级额外学生数的 `adds` 列表。  

> **结论**：暴力解虽然概念最简单，却在本题的约束（`n、extra ≤ 10⁵`）下根本不可行。下面我们来寻找更聪明的办法。  

---  

### 2. 最优解  

#### 思路  

**从暴力解出发，找出瓶颈**：  
- 暴力解的慢点在于**每一次都要遍历所有可能的分配**，而实际上我们只需要关心“把一个学生放到哪儿能让平均通过率提升最多”。  
- 关键观察：**给某个班级再加一个优秀学生后，班级的通过率提升幅度是递减的**。也就是说，第一次加人的收益最大，第二次加人的收益比第一次小，依此类推。  

**数学推导**：  
对第 `i` 班级，原始通过人数 `p_i`、总人数 `t_i`，若再加一个学生，新的通过率为  

\[
\frac{p_i+1}{t_i+1}
\]

提升幅度（记作 `gain_i`）为  

\[
gain_i = \frac{p_i+1}{t_i+1} - \frac{p_i}{t_i}
      = \frac{t_i - p_i}{t_i(t_i+1)}
\]

当该班级已经额外得到 `k` 名学生后，`p_i`、`t_i` 分别变成 `p_i+k`、`t_i+k`，对应的提升幅度为  

\[
gain_i(k) = \frac{(p_i+k+1)}{(t_i+k+1)} - \frac{(p_i+k)}{(t_i+k)}
\]

**重要性质**：`gain_i(k)` 随着 `k` 增大而单调递减。直观类比：把糖果放进已经很满的瓶子，瓶子涨高的幅度会越来越小。  

**贪心策略**：因为每一次我们只想拿到“**当前所有班级中提升幅度最大的那一个**”，于是可以把每个班级当前的 `gain` 放进一个**最大堆（Priority Queue）**，每次弹出堆顶（最大提升），把该班级的 `p`、`t` 都加一，再把新的 `gain` 放回堆。循环 `extraStudents` 次后，所有额外学生都已经“最值分配”。  

**为什么贪心是最优的**：  
- 每一次选择的都是当前**局部最优**（最大增益）。  
- 由于 `gain_i(k)` 随 `k` 单调递减，**以后**再对同一个班级加人时的收益只会更小，不会因为现在“错过”而在后面得到更大的补偿。  
- 这正好满足**贪心选择性**的充分条件：**子问题的最优解能够合并成全局最优解**。  

#### 代码（Python）  

```python
import heapq
from typing import List

def maxAverageRatio(classes: List[List[int]], extraStudents: int) -> float:
    """
    使用最大堆（实际上是 Python 的最小堆，取负数模拟）实现贪心分配
    返回分配完 extraStudents 后的最大平均通过率
    """
    # ---------- 1. 计算每个班级当前的增益，并放入堆 ----------
    # 堆里存 (-gain, p, t) 负号是因为 heapq 只能实现最小堆
    heap = []
    for p, t in classes:
        # 第一次加人的增益
        gain = (p + 1) / (t + 1) - p / t
        heapq.heappush(heap, (-gain, p, t))

    # ---------- 2. 逐个分配额外的学生 ----------
    for _ in range(extraStudents):
        # 取出增益最大的班级
        neg_gain, p, t = heapq.heappop(heap)
        # 这一步相当于“把一个优秀学生塞进去”
        p += 1
        t += 1
        # 重新计算该班级下一次加人的增益
        new_gain = (p + 1) / (t + 1) - p / t
        heapq.heappush(heap, (-new_gain, p, t))

    # ---------- 3. 计算最终的平均通过率 ----------
    total_ratio = 0.0
    while heap:
        _, p, t = heapq.heappop(heap)
        total_ratio += p / t
    return total_ratio / len(classes)
```

**代码要点说明**  

| 行号 | 关键语句 | 中文解释 |
|------|----------|----------|
| 8‑11 | `gain = (p + 1) / (t + 1) - p / t` | 计算“再加一个学生”会提升多少通过率，这一步类似“测量每个瓶子再装一颗糖的体积增量”。 |
| 12   | `heapq.heappush(heap, (-gain, p, t))` | 把负的增益放进去，负号让 Python 最小堆变成**最大堆**。 |
| 16‑22| `neg_gain, p, t = heapq.heappop(heap)` … `heapq.heappush(heap, (-new_gain, p, t))` | 取出增益最大的班级，给它加一名学生，随后把新的增益再放回堆中，保证堆始终维护最新的“最大增益”。 |
| 26‑29| `total_ratio += p / t` | 把所有班级的最终通过率加起来，最后除以班级数得到平均值。 |

#### 复杂度  

- **时间复杂度**：`O(extraStudents * log n)`。  
  - 每一次分配都要弹出堆顶、更新、再插入，堆的大小始终是 `n`（班级数），所以每次操作是 `log n`。  
  - 与暴力解的指数级相比，**线性乘对数**的增长几乎可以在毫秒内完成，即使 `n、extraStudents` 都是 `10⁵`。  
- **空间复杂度**：`O(n)`。堆里存放每个班级的当前状态 `(gain, p, t)`，大小正好等于班级数。  

> **对比**：暴力解的时间是指数级的“星号与竖线”组合数，而最优解只需要 `extraStudents` 次堆操作，几乎是线性时间。  

---  

## 心得  

- **核心技巧**：**贪心 + 最大堆**（每次挑选“当前增益最大”的对象）。  
- **适用的题型**  
  1. **分配类贪心**：如 “分配 K 条额外道路使平均旅行时间最大化”。  
  2. **增益递减的优化**：如 “给机器分配额外的功率/内存，使整体效率最大”。  
  3. **最大化平均值**：如 “把 K 颗硬币放入不同罐子，使平均硬币价值最大”。  
- **一句话总结**：**每一次把学生放进“最能提升通过率的班级”，用堆把“最能提升的”始终排在前面**。  

---  

## 反思  

- **第一反应**：直接想到枚举所有可能的分配方式，甚至写了递归搜索。  
- **最容易踩的坑**  
  - **增益递减**：忘记证明或利用 `gain_i(k)` 单调递减，导致错误的贪心选择。  
  - **堆的实现**：Python 没有原生最大堆，需要用负数技巧，否则会得到最小增益。  
  - **浮点误差**：题目要求 1e‑5 精度，直接使用 `float` 足够，但要注意除法不要整除。  
  - **边界情况**：当某个班级已经满分（`p == t`）时，`gain` 为 0，仍需放入堆，否则会导致堆为空的异常。  
- **下次类似题的第一步**：**计算“再投入一个单位资源的边际收益”，并检查它是否随投入次数递减**；如果是，**用堆把最大的边际收益一次次挑出来**。