# #3074. 苹果重新分配到箱子中 / Apple Redistribution into Boxes

> 难度：简单 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/apple-redistribution-into-boxes/)

---

## 题目（英文原版）

**Description**

You are given an array apple of size n and an array capacity of size m.
There are n packs where the ith pack contains apple[i] apples. There are m boxes as well, and the ith box has a capacity of capacity[i] apples.
Return the minimum number of boxes you need to select to redistribute these n packs of apples into boxes.
Note that, apples from the same pack can be distributed into different boxes.

**Examples**

**Example 1:**

```
Input: apple = [1,3,2], capacity = [4,3,1,5,2]
Output: 2
Explanation: We will use boxes with capacities 4 and 5.
It is possible to distribute the apples as the total capacity is greater than or equal to the total number of apples.
```

**Example 2:**

```
Input: apple = [5,5,5], capacity = [2,4,2,7]
Output: 4
Explanation: We will need to use all the boxes.
```

**Constraints**

- 1 <= n == apple.length <= 50
- 1 <= m == capacity.length <= 50
- 1 <= apple[i], capacity[i] <= 50
- The input is generated such that it's possible to redistribute packs of apples into boxes.

---

## 题目（中文翻译）

你得到一个大小为 `n` 的数组 `apple` 和一个大小为 `m` 的数组 `capacity`。  
其中有 `n` 包苹果，第 `i` 包包含 `apple[i]` 个苹果；同样有 `m` 个箱子，第 `i` 个箱子的容量为 `capacity[i]`（即最多能装 `capacity[i]` 个苹果）。  

返回需要选取的最少箱子数量，使得这 `n` 包苹果能够全部重新分配到所选箱子中。  
注意，同一包中的苹果可以分散到不同的箱子里。

## 示例

### 示例 1
**输入**  
```text
apple = [1,3,2], capacity = [4,3,1,5,2]
```
**输出**  
```text
2
```
**解释**  
我们选用容量为 `4` 和 `5` 的两个箱子。由于总容量 `4 + 5 = 9` 大于等于苹果总数 `1 + 3 + 2 = 6`，因此可以完成分配。

### 示例 2
**输入**  
```text
apple = [5,5,5], capacity = [2,4,2,7]
```
**输出**  
```text
4
```
**解释**  
必须使用所有箱子才能满足容量需求。

## 约束条件

- `1 <= n == apple.length <= 50`
- `1 <= m == capacity.length <= 50`
- `1 <= apple[i], capacity[i] <= 50`
- 输入保证一定可以将所有苹果重新分配到箱子中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有盒子都列出来，尝试每一种可能的选盒子组合**，看哪一种的总容量刚好（或刚好大于等于）能装下所有苹果，并且盒子数量最少。

- **数据结构**  
  - `apple` 和 `capacity` 本身就是普通的 Python 列表（list），相当于我们平时装东西的“篮子”。  
  - 为了枚举所有盒子组合，我们可以用 **位掩码**（bit mask）来表示每个盒子是否被选中。把每个盒子看成一本字典，`1` 表示这本字典被抽出来查，`0` 表示不抽。这样 `m` 本字典（盒子）就可以用一个长度为 `m` 的二进制数来描述。

- **为什么正确**  
  - 只要遍历了 **所有** 可能的选盒子子集，就一定会碰到最优的那一种。因为题目保证一定可以装下苹果，所以一定会有至少一个子集满足「总容量 ≥ 所有苹果之和」。

- **时间/空间复杂度**  
  - `m ≤ 50`，遍历所有子集的数量是 `2^m`（2 的 m 次方），这在最坏情况下会是天文数字（约 `1.12e15`），显然不可接受。但因为是「暴力」思路，只是用来帮助我们认识问题的本质。  
  - **时间复杂度**：`O(2^m * m)`，每个子集需要遍历一次盒子求和。  
  - **空间复杂度**：`O(1)`（只用常数级的额外变量），因为我们直接在循环里算和，不需要额外的数组。

> **大白话解释**：  
> - `O(2^m)` 就像让你把 50 本书每本都决定「要不要拿出来」——所有决定的组合一共有 2 的 50 次方种，想象一下有多少种可能！  
> - `O(m)` 表示对每一种决定，我们还要把选中的盒子容量加起来，最多检查 50 次。

#### 代码（Python）

```python
from itertools import combinations
from math import inf

def minBoxes_bruteforce(apple, capacity):
    # 1. 先算出所有苹果的总数
    total_apples = sum(apple)

    m = len(capacity)
    best = inf                     # 用一个很大的数记录当前找到的最小盒子数

    # 2. 枚举子集大小 k，从 1 到 m
    for k in range(1, m + 1):
        #   对每一种选 k 个盒子的方式（组合），检查总容量是否足够
        for idx_tuple in combinations(range(m), k):
            cur_sum = sum(capacity[i] for i in idx_tuple)
            if cur_sum >= total_apples:   # 容量够装下所有苹果
                best = k                 # 记录下最少的盒子数
                break                    # 已经找到当前 k 的答案，没必要继续同样大小的组合
        if best != inf:                    # 找到答案后直接退出外层循环
            break

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^m * m)` ——遍历所有子集（指数级）并在每个子集里求和（线性）。  
- **空间复杂度**：`O(1)` ——只用了若干计数器和临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正的难点在于“挑选盒子”**。我们不需要考虑每一种组合，只要**尽可能少的盒子、且容量总和足够**即可。

- **慢在哪里？**  
  暴力枚举所有子集的过程让我们遍历了大量不必要的组合。实际上，**只要把容量大的盒子先挑出来，就能最快达到“容量≥总苹果数”**。因为大盒子贡献的容量更多，选的数量自然更少。

- **一步步推导**  
  1. 先算出所有苹果的总数 `total = sum(apple)`。  
  2. 把 `capacity` 从大到小排序（降序）。  
  3. 从排好序的列表左侧（最大的）依次累计容量，直到累计值 `cur >= total`。  
  4. 此时累计的盒子数量就是答案。

- **核心算法/数据结构**  
  - **排序（Sorting）**：把盒子的容量从大到小排好顺序，类似于把装水的桶按照容量从大到小摆好，先用大桶装，能更快装满。Python 的 `sorted` 或 `list.sort` 都是基于 **Timsort**，时间复杂度为 `O(m log m)`。  
  - **贪心（Greedy）**：每一步都做局部最优（挑最大的盒子），全局也最优，因为如果我们把一个容量较小的盒子换成容量更大的盒子，装苹果的盒子数只会不增反减。

- **类比**  
  想象你要搬家，需要把所有家具装进卡车。卡车的载重不同，你显然会先挑载重最大的卡车来装，这样卡车数量最少，搬家最快。

#### 代码（Python）

```python
def minBoxes_greedy(apple, capacity):
    """
    贪心解：先挑容量最大的盒子，累计到足够装下所有苹果为止。
    """
    total_apples = sum(apple)          # 1. 计算所有苹果总数
    capacity.sort(reverse=True)       # 2. 按容量从大到小排序（原地修改）

    cur = 0            # 已经选的盒子累计容量
    cnt = 0            # 已经选的盒子数量
    for cap in capacity:               # 3. 依次取最大的盒子
        cur += cap
        cnt += 1
        if cur >= total_apples:         # 4. 容量已经足够，直接返回
            return cnt

    # 根据题目保证一定可以装下，这里理论上不会到达
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(m log m)` ——主要耗时在对 `capacity` 排序（`log m` 是对数，代表排序的层数）。相较于暴力的指数级，这已经快得多。  
- **空间复杂度**：`O(1)`（如果使用原地排序）或 `O(m)`（如果使用 `sorted` 产生新列表）。这里我们用了原地排序，所以只用了常数级额外空间。

> **对比**：  
> - 暴力解需要检查所有子集，时间随盒子数呈指数增长。  
> - 贪心解只需要一次排序和一次线性遍历，时间随盒子数呈对数＋线性增长，几乎瞬间完成。

---

## 心得

- **核心技巧**：**贪心 + 排序**。先把资源（盒子容量）从大到小排好序，然后一次取最大值，直到满足需求。
- **适用的题型**  
  1. **最少硬币找零**（在硬币面额满足“每种面额都是前一种的倍数”时，贪心可行）。  
  2. **分配任务到机器**（机器处理能力从大到小分配，最少机器数）。  
  3. **背包容量最小化**（在只关心“是否能装下全部物品”，不关心价值时，使用最大容量优先）。
- **一句话总结**：**把最大的盒子先挑出来，累计容量，一旦够了就停——这就是最少盒子数的钥匙。**

---

## 反思

- **第一反应**：看到“总容量 ≥ 总苹果数”，自然会想到先算总和，然后想办法选最少的盒子来满足这个总和。
- **最容易踩的坑**  
  - **忘记对容量排序**：直接从原数组顺序挑盒子会导致选的盒子不是最优的。  
  - **遗漏“容量相等的盒子”**：即使有多个容量相同的盒子，贪心仍然有效，只要按任意顺序取即可。  
  - **边界条件**：当所有盒子都必须使用时（如示例 2），循环会遍历完所有盒子才返回，这时 `cnt == m`，代码仍然正确。
- **下次遇到同类题**，第一步应该问自己：**“有没有一种资源（容量、价值、速度）可以排序，使得取最大的/最小的就能最快满足需求？”**如果答案是肯定的，贪心往往是最直接、最高效的解法。