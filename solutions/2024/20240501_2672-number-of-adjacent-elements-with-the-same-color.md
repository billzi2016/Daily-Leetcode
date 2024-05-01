# #2672. 相同颜色的相邻元素数量 / Number of Adjacent Elements With the Same Color

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/number-of-adjacent-elements-with-the-same-color/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing an array colors of length n where all elements are set to 0's meaning uncolored. You are also given a 2D integer array queries where queries[i] = [indexi, colori]. For the ith query:
Return an array answer of the same length as queries where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: n = 4, queries = [[0,2],[1,2],[3,1],[1,1],[2,1]]
Output: [0,1,1,0,2]
Explanation:
```

**Example 2:**

```
Input: n = 1, queries = [[0,100000]]
Output: [0]
Explanation:
After the 1 st query colors = [100000]. The count of adjacent pairs with the same color is 0.
```

**Constraints**

- 1 <= n <= 105
- 1 <= queries.length <= 105
- queries[i].length == 2
- 0 <= indexi <= n - 1
- 1 <=  colori <= 105

---

## 题目（中文翻译）

**题目描述**

给定一个整数 `n`，表示长度为 `n` 的数组 `colors`，初始时所有元素均为 `0`，表示未上色。  
同时给定一个二维整数数组 `queries`，其中 `queries[i] = [index_i, color_i]` 表示第 `i` 条查询。

对第 `i` 条查询执行以下操作：

1. 将 `colors[index_i]` 设为 `color_i`（即对位置 `index_i` 上色为 `color_i`）。  
2. 统计数组中相邻位置 `(j, j+1)`（`0 ≤ j < n‑1`）满足 `colors[j] == colors[j+1]` 且该颜色不为 `0` 的对数。

返回一个数组 `answer`，`answer[i]` 为第 `i` 条查询执行完毕后的统计结果，`answer` 的长度与 `queries` 相同。

---

**示例**

**示例 1**

```
输入: n = 4, queries = [[0,2],[1,2],[3,1],[1,1],[2,1]]
输出: [0,1,1,0,2]
解释:
- 查询 0: 将 colors[0] 设为 2 → colors = [2,0,0,0]，相邻相同颜色对数为 0。
- 查询 1: 将 colors[1] 设为 2 → colors = [2,2,0,0]，相邻相同颜色对数为 1（下标 0 与 1）。
- 查询 2: 将 colors[3] 设为 1 → colors = [2,2,0,1]，相邻相同颜色对数仍为 1。
- 查询 3: 将 colors[1] 设为 1 → colors = [2,1,0,1]，相邻相同颜色对数为 0。
- 查询 4: 将 colors[2] 设为 1 → colors = [2,1,1,1]，相邻相同颜色对数为 2（下标 1 与 2，2 与 3）。
```

**示例 2**

```
输入: n = 1, queries = [[0,100000]]
输出: [0]
解释:
执行第 1 条查询后 colors = [100000]。数组中没有相邻位置，故相同颜色相邻对数为 0。
```

---

**约束条件**

- `1 <= n <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= index_i <= n - 1`
- `1 <= color_i <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次查询后**把整个数组 `colors` 重新遍历一遍，统计相邻两个位置颜色相同的对数。  
- **数据结构**：只需要一个普通的 Python 列表 `colors` 来存颜色。  
- **为什么正确**：遍历一次就能把所有相邻位置 `(i,i+1)` 的颜色是否相同全部检查完，计数自然就是答案。  
- **复杂度分析**：  
  - 对于每一次查询，我们都要 **完整遍历** 长度为 `n` 的数组，时间是 `O(n)`。  
  - 查询总数记为 `m = len(queries)`，所以整体时间是 `O(m·n)`。  
  - 只用了一个数组 `colors`（长度 `n`）和几个计数变量，空间是 `O(n)`。  

> 大白话解释：`O(n)` 就像“每次都把整条街的房子都走一遍”，如果街道很长（`n` 大），而且要走很多次（`m` 次查询），显然会很慢。

#### 代码（Python）

```python
def number_of_adjacent_elements_bruteforce(n, queries):
    # 初始化全为 0 的颜色数组
    colors = [0] * n
    ans = []

    for idx, col in queries:
        # 1. 给指定位置重新着色
        colors[idx] = col

        # 2. 重新遍历一遍统计相邻相同颜色的对数
        cnt = 0
        for i in range(n - 1):          # 只需要检查到 n-2，i+1 才是合法下标
            if colors[i] == colors[i + 1]:
                cnt += 1
        ans.append(cnt)                 # 把本次查询的答案保存

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 每次查询遍历 `n` 个元素，`m` 次查询相乘。  
  - 当 `n`、`m` 都达到 `10⁵` 时，最坏会是 `10¹⁰` 次比较，显然会超时。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的数组来保存颜色。

---

### 2. 最优解

#### 思路  

观察暴力解的 **瓶颈**：我们每次都把整条街（整个数组）重新走一遍，只是为了更新 **一个点** 的颜色。  
事实上，改变一个位置只会影响它 **左右各一条相邻关系**（即 `(idx‑1, idx)` 和 `(idx, idx+1)`），其它相邻对的状态保持不变。  

**核心思路**：  
1. **维护一个全局计数 `same_cnt`**，它始终表示当前数组中相邻相同颜色的对数。  
2. 对每一次查询 `(idx, new_color)`：  
   - **先把旧的贡献减掉**：  
     - 如果 `idx` 左边的元素存在且颜色和 `colors[idx]` 相同，`same_cnt -= 1`。  
     - 同理，右边相同则再减 1。  
   - **执行染色**：`colors[idx] = new_color`。  
   - **再把新的贡献加上**：  
     - 检查左邻居是否和新颜色相同，若相同 `same_cnt += 1`。  
     - 检查右邻居，同理。  
3. 将 `same_cnt` 记录进答案数组。

这样每次查询只做 **常数次（最多 4 次）比较和加减**，时间是 `O(1)`，整体 `O(m)`。  

> 类比：把 `same_cnt` 想成“街道上相邻相同颜色的相邻房子对数”。当我们给某栋房子重新粉刷时，只需要检查它左边和右边的两栋房子是否颜色相同，其他房子根本不受影响。

#### 代码（Python）

```python
def number_of_adjacent_elements_optimal(n, queries):
    # 1. 初始全部未着色（颜色 0）
    colors = [0] * n
    # 2. 初始相邻相同的对数为 0（因为全是 0，实际上 n-1 对相同，但题目要求“未着色”不计数，
    #    这里我们把所有 0 当作“未染色”，所以从 0 开始计数，后面的逻辑会自行处理）
    same_cnt = 0
    ans = []

    for idx, new_col in queries:
        # ----- 1) 删除旧颜色带来的贡献 -----
        # 检查左侧相邻对 (idx-1, idx)
        if idx > 0 and colors[idx] == colors[idx - 1]:
            same_cnt -= 1               # 之前相同，现在要改颜色，先减掉
        # 检查右侧相邻对 (idx, idx+1)
        if idx < n - 1 and colors[idx] == colors[idx + 1]:
            same_cnt -= 1

        # ----- 2) 更新颜色 -----
        colors[idx] = new_col

        # ----- 3) 添加新颜色产生的贡献 -----
        if idx > 0 and colors[idx] == colors[idx - 1]:
            same_cnt += 1               # 左侧现在相同，计数加 1
        if idx < n - 1 and colors[idx] == colors[idx + 1]:
            same_cnt += 1               # 右侧现在相同，计数加 1

        # 保存本次查询的答案
        ans.append(same_cnt)

    return ans
```

> **细节说明**  
> - 初始全为 `0` 时，题目把 “未上色” 视为不计数的状态（示例 2 说明），所以我们把 `same_cnt` 初始化为 `0`，而不是 `n‑1`。  
> - 只要在 **改颜色前** 把旧的相邻贡献减掉，在 **改颜色后** 再把新的贡献加上，就能保证 `same_cnt` 始终是当前真实的答案。

#### 复杂度

- **时间复杂度**：`O(m)`  
  - 每次查询只做常数次比较/加减（最多四次），所以整体线性于查询数 `m`。  
  - 与暴力解 `O(m·n)` 相比，快了整整 `n` 倍。  
- **空间复杂度**：`O(n)`  
  - 只需要保存颜色数组 `colors`（长度 `n`）和答案列表 `ans`（长度 `m`），不需要额外的复杂结构。

---

## 心得

- **核心技巧**：**局部更新 + 全局计数**。当操作只影响相邻的常数条关系时，维护一个全局统计量并在每次修改时只局部增减，能把本来线性的遍历压到常数时间。  
- **适用的题型**  
  1. 「子数组/相邻元素」计数随单点修改而变化（如 “子数组中奇数个数” 维护）。  
  2. 「连通块数量」随点染色或删除而变化（如 “岛屿数量” 动态维护）。  
- **一句话总结**：**只看改动点的左右邻居，增减计数即可**。

---

## 反思

- **第一反应**：看到“每次都要重新统计相邻相同的对”，自然想到直接遍历全数组。  
- **最容易踩的坑**  
  - **初始状态**：所有元素为 `0`（未上色）时，是否算作相同颜色需要仔细阅读题意，避免把 `n‑1` 当作初始计数。  
  - **边界检查**：`idx` 在数组两端时，只会有左或右邻居，忘记判断 `idx > 0`、`idx < n‑1` 会导致越界错误。  
  - **重复染色**：同一个位置可能被多次染成相同颜色，仍要先减后加，否则计数会出错。  
- **下次类似**：遇到“每次只改动一个元素，求某种全局统计”时，立刻想到**维护一个全局计数并在局部增减**，而不是每次全局重新计算。