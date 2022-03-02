# #1687. 从仓库运送箱子到港口 / Delivering Boxes from Storage to Ports

> 难度：困难 · 标签：Array、Dynamic Programming、Segment Tree、Queue、Heap (Priority Queue)、Prefix Sum、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/delivering-boxes-from-storage-to-ports/)

---

## 题目（英文原版）

**Description**

You have the task of delivering some boxes from storage to their ports using only one ship. However, this ship has a limit on the number of boxes and the total weight that it can carry.
You are given an array boxes, where boxes[i] = [ports​​i​, weighti], and three integers portsCount, maxBoxes, and maxWeight.
The boxes need to be delivered in the order they are given. The ship will follow these steps:
The ship must end at storage after all the boxes have been delivered.
Return the minimum number of trips the ship needs to make to deliver all boxes to their respective ports.

**Examples**

**Example 1:**

```
Input: boxes = [[1,1],[2,1],[1,1]], portsCount = 2, maxBoxes = 3, maxWeight = 3
Output: 4
Explanation: The optimal strategy is as follows: 
- The ship takes all the boxes in the queue, goes to port 1, then port 2, then port 1 again, then returns to storage. 4 trips.
So the total number of trips is 4.
Note that the first and third boxes cannot be delivered together because the boxes need to be delivered in order (i.e. the second box needs to be delivered at port 2 before the third box).
```

**Example 2:**

```
Input: boxes = [[1,2],[3,3],[3,1],[3,1],[2,4]], portsCount = 3, maxBoxes = 3, maxWeight = 6
Output: 6
Explanation: The optimal strategy is as follows: 
- The ship takes the first box, goes to port 1, then returns to storage. 2 trips.
- The ship takes the second, third and fourth boxes, goes to port 3, then returns to storage. 2 trips.
- The ship takes the fifth box, goes to port 2, then returns to storage. 2 trips.
So the total number of trips is 2 + 2 + 2 = 6.
```

**Example 3:**

```
Input: boxes = [[1,4],[1,2],[2,1],[2,1],[3,2],[3,4]], portsCount = 3, maxBoxes = 6, maxWeight = 7
Output: 6
Explanation: The optimal strategy is as follows:
- The ship takes the first and second boxes, goes to port 1, then returns to storage. 2 trips.
- The ship takes the third and fourth boxes, goes to port 2, then returns to storage. 2 trips.
- The ship takes the fifth and sixth boxes, goes to port 3, then returns to storage. 2 trips.
So the total number of trips is 2 + 2 + 2 = 6.
```

**Constraints**

- 1 <= boxes.length <= 105
- 1 <= portsCount, maxBoxes, maxWeight <= 105
- 1 <= ports​​i <= portsCount
- 1 <= weightsi <= maxWeight

---

## 题目（中文翻译）

**题目描述**

你需要使用一艘船将若干箱子从仓库运送到对应的港口。船一次只能装载不超过 `maxBoxes` 个箱子，且总重量不超过 `maxWeight`。

给定数组 `boxes`，其中 `boxes[i] = [ports_i, weight_i]` 表示第 `i` 个箱子的目的港口编号 `ports_i`（`1 ≤ ports_i ≤ portsCount`）以及重量 `weight_i`。同时给定三个整数 `portsCount`（港口总数）、`maxBoxes`、`maxWeight`。

箱子必须按照在数组中出现的顺序进行装运。船的每一次航程遵循以下步骤：

1. 从仓库依次装载 **连续** 的若干箱子，装载的箱子数量 ≤ `maxBoxes`，总重量 ≤ `maxWeight`。  
2. 按装载顺序依次前往这些箱子对应的港口 `ports_i`，到达对应港口后卸下该箱子。  
3. 若连续的多个箱子目的地相同，船只需要在该港口停留一次即可卸完所有这些箱子。  
4. 完成当前航程的所有卸货后，船返回仓库准备下一次装载。  
5. 所有箱子全部送达后，船必须回到仓库。

返回将所有箱子送达各自港口所需的**最少航程次数**（一次航程包括装载、送达以及返回仓库）。

---

### 示例

#### 示例 1
```
Input: boxes = [[1,1],[2,1],[1,1]], portsCount = 2, maxBoxes = 3, maxWeight = 3
Output: 4
Explanation: 最优方案如下：
- 第一次航程装载所有三个箱子，依次前往港口 1、港口 2、港口 1，最后返回仓库。共 4 次航程（装载‑>港口1‑>港口2‑>港口1‑>返回）。
因此总航程次数为 4。
注意，箱子 1 与箱子 3 不能在同一次装载后一起送达，因为它们的目的港口顺序不同，需要分别到达两次港口 1。
```

#### 示例 2
```
Input: boxes = [[1,2],[3,3],[3,1],[3,1],[2,4]], portsCount = 3, maxBoxes = 3, maxWeight = 6
Output: 6
Explanation: 最优方案如下：
- 第一次航程装载第 1 个箱子，前往港口 1 并返回仓库。2 次航程。
- 第二次航程装载第 2、3、4 个箱子，前往港口 3 并返回仓库。2 次航程。
- 第三次航程装载第 5 个箱子，前往港口 2 并返回仓库。2 次航程。
总计 6 次航程。
```

#### 示例 3
```
Input: boxes = [[1,4],[1,2],[2,1],[2,1],[3,2],[3,4]], portsCount = 3, maxBoxes = 6, maxWeight = 7
Output: 6
Explanation: 最优方案如下：
- 第一次航程装载第 1、2 个箱子，前往港口 1 并返回仓库。2 次航程。
- 第二次航程装载第 3、4 个箱子，前往港口 2 并返回仓库。2 次航程。
- 第三次航程装载第 5、6 个箱子，前往港口 3 并返回仓库。2 次航程。
总计 6 次航程。
```

---

### 约束条件

- `1 ≤ boxes.length ≤ 10^5`
- `1 ≤ portsCount, maxBoxes, maxWeight ≤ 10^5`
- `1 ≤ ports_i ≤ portsCount`
- `1 ≤ weight_i ≤ maxWeight`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的装箱方式枚举一遍**，然后挑出需要最少航次的那一种。  
具体做法可以用递归或动态规划：

1. 从第 `0` 个箱子开始，尝试把 **第 1、2、…、k** 个箱子装进船，只要满足  
   - 装的箱子数量 ≤ `maxBoxes`  
   - 装的总重量 ≤ `maxWeight`  
2. 这一次装完后，船会按照装进来的顺序依次访问对应的港口，途中如果连续两个箱子的目的港不一样，就要额外一次“换港”操作。  
3. 船把这批箱子送完后回到仓库，这算 **1 次航程**（去往各港口 + 回仓库）。  
4. 然后递归地处理剩下的箱子，累计航程次数，取最小值。

> **类比**：把箱子想象成排队买票的顾客，船是一辆只能一次装 `maxBoxes` 人、总重量不超 `maxWeight` 的巴士。我们想把所有顾客送到他们对应的站点，要求巴士往返次数最少。最笨的办法就是：从队首开始，尝试让巴士一次装 1 人、2 人、3 人…，每种装法都算一次来回，然后递归处理剩下的人。

**为什么这个方法一定能得到答案？**  
因为它穷举了 **所有** 合法的装箱方式（每一步都尝试所有可能的装箱数），其中必然包含最优的装箱方案。只要我们把每一种方案的航次数算对了，取最小值自然就是答案。

#### 代码（Python）

```python
from functools import lru_cache

def minTrips_bruteforce(boxes, maxBoxes, maxWeight):
    n = len(boxes)

    # 前缀和帮助快速计算区间重量
    pref_weight = [0] * (n + 1)
    for i in range(n):
        pref_weight[i + 1] = pref_weight[i] + boxes[i][1]

    @lru_cache(None)          # 记忆化递归，防止重复计算
    def dfs(idx):             # idx 表示下一个要装的箱子下标
        if idx == n:          # 所有箱子都送完了
            return 0
        best = float('inf')
        # 尝试一次装 i~j-1（左闭右开）这些箱子
        for j in range(idx + 1, n + 1):
            cnt = j - idx                     # 装的箱子数量
            total_w = pref_weight[j] - pref_weight[idx]
            if cnt > maxBoxes or total_w > maxWeight:
                break                         # 已经超出限制，后面的 j 只会更大，直接退出

            # 计算这一趟需要的“换港次数”
            trips = 1                         # 去仓库 → 第一个港口算一次
            for k in range(idx, j - 1):
                if boxes[k][0] != boxes[k + 1][0]:
                    trips += 1                # 相邻两个箱子目的港不一样，需要再去一次新港口
            trips += 1                         # 最后一定要回到仓库

            best = min(best, trips + dfs(j))  # 当前这趟 + 递归后面的最优

        return best

    return dfs(0)
```

> **关键注释**  
> - `pref_weight` 是**前缀重量和**，可以在 O(1) 时间内得到任意区间的总重量。  
> - `dfs(idx)` 用**记忆化搜索**（`lru_cache`）避免对同一个起点重复递归。  
> - 循环里 `cnt > maxBoxes or total_w > maxWeight` 一旦不满足，就可以直接 `break`，因为后面的区间只会更大。

#### 复杂度  

- **时间复杂度**：最坏情况下会尝试每个起点 `i` 与每个终点 `j` 的组合，约为 `O(n²)`（n 是箱子数量）。  
  - 大白话：如果有 10,000 个箱子，暴力解大概要检查 10,000 × 10,000 = 1 亿次，远远超过一秒能完成的次数。  
- **空间复杂度**：递归栈深度最多 `O(n)`，加上记忆化表需要 `O(n)`，整体 `O(n)`。

> 这已经远远超出题目要求（`n ≤ 10⁵`），所以我们必须继续优化。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于枚举每一次装箱的起点 `i` 与终点 `j`（即 `O(n²)` 的双层循环）。  
我们需要一种方式 **快速求出**：

```
dp[j] = min{ dp[i-1] + cost(i, j) }   (i ≤ j, 区间 i~j 合法)
```

- `dp[k]` 表示 **送完前 k 个箱子所需的最少航次**（不包括最后回仓库的那一次，稍后会统一加上）。  
- `cost(i, j)` 是 **第 i~j 这批箱子一次装载所需要的航次**，等于  
  `1`（从仓库出发） + `portChanges(i, j)`（中途换港的次数） + `1`（返回仓库）。  
  其中 `portChanges(i, j)` = 区间内相邻箱子目的港不相同的次数。

所以我们只要快速得到 `dp[i-1] - portChanges(1, i-1)` 的最小值，就能在 **O(1)** 时间内算出 `dp[j]`。  
这正好可以用 **单调队列（Monotonic Queue）** 来维护滑动窗口中的最小值。

##### 关键预处理  

1. **前缀重量** `preW[i]`：第 `i` 个箱子之前（不含第 `i`）的总重量。  
   - 用来判断区间 `[i, j]` 是否满足重量 ≤ `maxWeight`。  
2. **前缀箱子数** `preC[i] = i`（因为每个箱子计数 1），用来判断箱子数量 ≤ `maxBoxes`。  
3. **前缀港口变化** `preDiff[i]`：从第 1 个箱子到第 `i` 个箱子（包含第 `i`）的 **换港次数**。  
   - 计算方式：`preDiff[i] = preDiff[i-1] + (ports[i-1] != ports[i-2])`（下标从 1 开始）。  

有了这些前缀数组，我们可以在 **O(1)** 时间得到：

- 区间重量 `weight(i, j) = preW[j] - preW[i-1]`  
- 区间箱子数 `cnt(i, j) = j - i + 1`  
- 区间换港次数 `portChanges(i, j) = preDiff[j] - preDiff[i] + (ports[i-1] != ports[i])`  
  这里的 `+ (ports[i-1] != ports[i])` 用来补上区间左端点与前一个箱子是否同港的差异。

##### 动态规划转移  

设 `dp[0] = 0`（送完 0 个箱子不需要航次）。  
对于每个 `j (1 … n)`，我们想找到最左的合法 `i`（满足 `cnt(i, j) ≤ maxBoxes` 且 `weight(i, j) ≤ maxWeight`），记为 `left`。  
在窗口 `[left, j]` 内，转移公式可以写成：

```
dp[j] = min_{i∈[left, j]} ( dp[i-1] + 1 + portChanges(i, j) + 1 )
      = 1 + 1 + min_{i∈[left, j]} ( dp[i-1] + portChanges(i, j) )
```

把 `portChanges(i, j)` 用前缀表示：

```
portChanges(i, j) = preDiff[j] - preDiff[i] + (ports[i-1] != ports[i])
```

把与 `j` 无关的 `preDiff[j]` 拿出来：

```
dp[j] = dpBase + preDiff[j] + 2
where dpBase = min_{i∈[left, j]} ( dp[i-1] - preDiff[i] + (ports[i-1] != ports[i]) )
```

注意 ` (ports[i-1] != ports[i]) ` 只在 **i 为区间左端点** 时才出现，等价于：

```
extra[i] = 1 if i>1 and ports[i-2] != ports[i-1] else 0
```

于是我们只需要维护 **窗口内的最小值**：

```
value[i] = dp[i-1] - preDiff[i] + extra[i]
```

随着 `j` 向右移动，`left` 只会右移（因为箱子数/重量只会增加），这正好构成一个 **滑动窗口**。  
我们可以用 **单调递增队列**（deque）：

- 队首保存当前窗口的最小 `value[i]`（即候选答案）。  
- 当 `i` 超出窗口左边界 `left` 时弹出队首。  
- 插入新的 `i = j` 时，先把队尾的所有比 `value[i]` 大的元素弹出，保证队列单调递增，队首永远是最小值。

这样每个箱子只会进入队列一次、退出一次，整体是 **O(n)**。

##### 完整步骤  

1. 预处理 `preW`、`preDiff`、`extra`（O(n)）。  
2. 初始化 `dp[0] = 0`，`deque` 里先放 `i = 1` 对应的 `value[1]`（因为 `dp[0]` 已知）。  
3. 对 `j` 从 1 到 n：  
   - 移动左边界 `left`，确保 `cnt(left, j) ≤ maxBoxes` 且 `weight(left, j) ≤ maxWeight`。  
   - 把已经不在窗口的 `i`（即 `i < left`）从队首弹出。  
   - 计算 `dp[j] = preDiff[j] + 2 + deque[0].value`。  
   - 为下一个 `j+1` 准备 `value[j+1] = dp[j] - preDiff[j+1] + extra[j+1]`，并按单调队列规则插入。  
4. 最后返回 `dp[n]`（已经把所有箱子送完并且算上回仓库的那一次）。

> **类比**：把 `dp[i]` 看成“到第 i 个箱子为止的最少航次”，而 `value[i]` 是“把第 i+1 个箱子当作新一趟的起点时，前面已经花的航次 + 一个补偿”。我们用一个排好序的队列，随时可以看到窗口里“最省钱的起点”，于是每次都能在 **常数时间** 内得到最优答案。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minTrips(boxes: List[List[int]], portsCount: int, maxBoxes: int, maxWeight: int) -> int:
    n = len(boxes)
    ports = [p for p, _ in boxes]          # 只保留港口信息，便于下标操作
    weight = [w for _, w in boxes]

    # 1️⃣ 前缀和：重量、换港次数
    preW = [0] * (n + 1)          # preW[i] = 前 i 个箱子的总重量
    preDiff = [0] * (n + 1)       # preDiff[i] = 前 i-1 个相邻箱子之间的换港次数
    for i in range(1, n + 1):
        preW[i] = preW[i - 1] + weight[i - 1]
        # 如果 i>1 且当前箱子港口 != 前一个箱子港口，换港次数 +1
        if i > 1 and ports[i - 1] != ports[i - 2]:
            preDiff[i] = preDiff[i - 1] + 1
        else:
            preDiff[i] = preDiff[i - 1]

    # 2️⃣ extra[i]：如果从第 i-1 个箱子切到第 i 个箱子会产生一次额外换港吗？
    #    这里的 i 按 1-indexed（与 dp、preDiff 对齐）
    extra = [0] * (n + 1)
    for i in range(2, n + 1):
        extra[i] = 1 if ports[i - 1] != ports[i - 2] else 0

    dp = [0] * (n + 1)           # dp[0] = 0，后面会逐步填充

    # 3️⃣ 单调队列，存放 (index i, value = dp[i-1] - preDiff[i] + extra[i])
    dq = deque()
    # 初始时，窗口左边界 left = 1（因为 i 必须 ≥ 1）
    left = 1
    # 把 i = 1 对应的 value 放进去（此时 dp[0] 已知）
    dq.append((1, dp[0] - preDiff[1] + extra[1]))

    for j in range(1, n + 1):
        # ---- 调整左边界，使得 [left, j] 满足装箱上限 ----
        while (j - left + 1) > maxBoxes or (preW[j] - preW[left - 1]) > maxWeight:
            # left 超出窗口，需要把对应的 i 弹出队首（如果在队首的话）
            if dq and dq[0][0] == left:
                dq.popleft()
            left += 1

        # ---- 现在 dq[0] 保存的是窗口内 value 的最小值 ----
        best_val = dq[0][1]                 # dp[i-1] - preDiff[i] + extra[i] 的最小值
        dp[j] = best_val + preDiff[j] + 2   # +2 = 出发一次 + 回仓库一次

        # ---- 为下一个位置 j+1 准备 value 并插入队列 ----
        if j + 1 <= n:
            new_val = dp[j] - preDiff[j + 1] + extra[j + 1]
            # 保持队列单调递增：队尾比 new_val 大的都可以踢掉
            while dq and dq[-1][1] >= new_val:
                dq.pop()
            dq.append((j + 1, new_val))

    return dp[n]
```

> **代码要点说明**  
> 1. `preDiff[i]` 记录 **到第 i-1 对箱子之间**（即前 i-1 条相邻）需要换港的次数，故 `preDiff[1] = 0`。  
> 2. `extra[i]` 只在 **i 为窗口左端点** 时才会计入一次换港（因为左端点前面已经有一次访问）。  
> 3. `dp[j] = best_val + preDiff[j] + 2` 中的 `+2` 分别代表 “离开仓库去第一个港口” 与 “送完返回仓库”。  
> 4. 单调队列的每一次 `append/pop` 都是 **O(1)**，整个循环只遍历一次数组，时间复杂度线性。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 预处理三次遍历 `O(n)`，主循环每个箱子最多进入一次、退出一次单调队列，也是 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **从平方级到线性级**，可以轻松处理 `n = 10⁵` 的数据。  
- **空间复杂度**：`O(n)`  
  - 需要存 `preW、preDiff、extra、dp` 四个长度为 `n+1` 的数组，以及一个最多装 `n` 元素的 deque。  
  - 只用了线性额外空间，符合题目限制。

---

## 心得  

- **核心技巧**：把「区间最小值」的 DP 转移写成「`dp[i-1] - 前缀换港 + 额外补偿`」的形式，利用 **单调队列（Monotonic Queue）** 在滑动窗口内快速取得最小值。  
- **适用场景**  
  1. **区间约束的最小/最大 DP**（如「划分数组」类问题，LeetCode 714、1105）。  
  2. **带有窗口大小/重量限制的运输或装载问题**（如「船运货物」系列）。  
  3. **需要在 O(1) 或 O(log n) 时间内查询区间最值** 的动态规划，常用单调队列或单调栈来优化。  
- **一句话总结解题钥匙**：  
  > 把「前缀信息」与「窗口最小值」结合，用单调队列把 O(n²) 的枚举压到 O(n)。

---

## 反思  

- **第一反应**：看到「顺序装箱」和「重量/箱子数上限」立刻想到「滑动窗口」或「二分」来找合法区间，随后想到「最小航次」会涉及 DP。  
- **最容易踩的坑**  
  1. **换港次数的计算**：容易忘记左端点与前一个箱子是否同港导致的额外换港，需要 `extra[i]` 补齐。  
  2. **左边界的移动**：必须同时检查箱子数量和总重量，任意一个超标都要左移。  
  3. **单调队列的下标同步**：出队时要确保弹出的元素真的已经不在窗口内，否则会得到错误的最小值。  
- **下次遇到同类题**：  
  1. 先写出 **最朴素的 DP**，弄清楚转移公式里哪些量只和左端点有关。  
  2. 把这些只和左端点有关的表达式抽象成「`value[i] = dp[i-1] - 前缀 + 补偿`」形式。  
  3. 检查窗口是否只随右指针单调移动——若是，就可以尝试 **单调队列** 或 **堆** 来维护窗口最小值，从而把二重循环降到线性。