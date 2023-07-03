# #2305. 公平分配饼干 / Fair Distribution of Cookies

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/fair-distribution-of-cookies/)

---

## 题目（英文原版）

**Description**

You are given an integer array cookies, where cookies[i] denotes the number of cookies in the ith bag. You are also given an integer k that denotes the number of children to distribute all the bags of cookies to. All the cookies in the same bag must go to the same child and cannot be split up.
The unfairness of a distribution is defined as the maximum total cookies obtained by a single child in the distribution.
Return the minimum unfairness of all distributions.

**Examples**

**Example 1:**

```
Input: cookies = [8,15,10,20,8], k = 2
Output: 31
Explanation: One optimal distribution is [8,15,8] and [10,20]
- The 1st child receives [8,15,8] which has a total of 8 + 15 + 8 = 31 cookies.
- The 2nd child receives [10,20] which has a total of 10 + 20 = 30 cookies.
The unfairness of the distribution is max(31,30) = 31.
It can be shown that there is no distribution with an unfairness less than 31.
```

**Example 2:**

```
Input: cookies = [6,1,3,2,2,4,1,2], k = 3
Output: 7
Explanation: One optimal distribution is [6,1], [3,2,2], and [4,1,2]
- The 1st child receives [6,1] which has a total of 6 + 1 = 7 cookies.
- The 2nd child receives [3,2,2] which has a total of 3 + 2 + 2 = 7 cookies.
- The 3rd child receives [4,1,2] which has a total of 4 + 1 + 2 = 7 cookies.
The unfairness of the distribution is max(7,7,7) = 7.
It can be shown that there is no distribution with an unfairness less than 7.
```

**Constraints**

- 2 <= cookies.length <= 8
- 1 <= cookies[i] <= 105
- 2 <= k <= cookies.length

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `cookies`，其中 `cookies[i]` 表示第 `i` 包饼干的数量。再给定一个整数 `k`，表示要将所有饼干包分配给 `k` 个孩子。 同一包饼干必须完整地分配给同一个孩子，不能拆分。  

分配方案的 **unfairness（不公平度）** 定义为该方案中单个孩子获得的饼干总数的最大值。  
返回所有可能分配方案中最小的 **unfairness（不公平度）**。

**示例 1**  
```
Input: cookies = [8,15,10,20,8], k = 2
Output: 31
Explanation: 一种最优的分配方式是 [8,15,8] 和 [10,20]  
- 第 1 个孩子得到 [8,15,8]，总共 8 + 15 + 8 = 31 块饼干。  
- 第 2 个孩子得到 [10,20]，总共 10 + 20 = 30 块饼干。  
该分配的不公平度为 max(31,30) = 31。  
可以证明不存在不公平度小于 31 的分配方案。
```

**示例 2**  
```
Input: cookies = [6,1,3,2,2,4,1,2], k = 3
Output: 7
Explanation: 一种最优的分配方式是 [6,1]、[3,2,2] 和 [4,1,2]  
- 第 1 个孩子得到 [6,1]，总共 6 + 1 = 7 块饼干。  
- 第 2 个孩子得到 [3,2,2]，总共 3 + 2 + 2 = 7 块饼干。  
- 第 3 个孩子得到 [4,1,2]，总共 4 + 1 + 2 = 7 块饼干。  
该分配的不公平度为 max(7,7,7) = 7。
```

**约束条件**  
- `2 <= cookies.length <= 8`  
- `1 <= cookies[i] <= 10^5`  
- `2 <= k <= cookies.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个饼干袋子都尝试分给每一个孩子**，把所有可能的分配列举出来，最后挑选出“不公平度”（即某个孩子拿到的饼干总数的最大值）最小的那种。  

- **数据结构**：我们用一个长度为 `k` 的数组 `load` 来记录每个孩子当前已经得到的饼干数量。把 `load[i]` 想象成 **孩子 i 的背包**，往背包里放东西就相当于把一袋饼干交给这个孩子。  
- **为什么正确**：只要把所有 `cookies` 中的每一袋都分配完毕，就得到一种合法的分配方式。遍历 **所有** 合法方式后，必然能找到最小的不公平度。  
- **时间/空间复杂度**：  
  - 每一袋饼干有 `k` 种选择，`n = len(cookies)`，所以总的尝试次数是 `k^n`（指数级）。这就是我们常说的 **O(kⁿ)**，意思是当 `n` 增加时，运算次数会像 `k` 的 `n` 次方一样快速增长。  
  - 递归栈最多保存 `n` 层调用，外加 `load` 数组大小为 `k`，所以空间是 **O(n + k)**，对我们这道题几乎可以忽略不计。

#### 代码（Python）

```python
from typing import List

def distribute_cookies_bruteforce(cookies: List[int], k: int) -> int:
    n = len(cookies)
    load = [0] * k                 # load[i] 表示第 i 个孩子当前的饼干总数
    best = float('inf')            # 记录目前找到的最小不公平度

    def dfs(idx: int):
        """把第 idx 袋饼干分配给某个孩子"""
        nonlocal best
        if idx == n:                # 所有袋子都已经分配完
            cur_unfair = max(load) # 当前分配的不公平度
            best = min(best, cur_unfair)
            return

        # 把第 idx 袋饼干尝试分给每一个孩子
        for i in range(k):
            load[i] += cookies[idx]    # 把这袋饼干放进孩子 i 的背包
            dfs(idx + 1)               # 继续分配下一袋
            load[i] -= cookies[idx]    # 回溯，撤销这次选择

    dfs(0)
    return best
```

> **关键行注释**  
> - `load = [0] * k`：把每个孩子的背包先清空。  
> - `if idx == n:`：递归终止条件，所有袋子都已经分完。  
> - `cur_unfair = max(load)`：求当前分配中最大的背包容量，即“不公平度”。  
> - `load[i] += cookies[idx] / load[i] -= cookies[idx]`：典型的**回溯**写法，先做选择，递归后再撤销。

#### 复杂度

- **时间复杂度**：`O(kⁿ)` —— 例如 `k=3, n=8` 时，需要尝试 `3⁸ = 6561` 种可能，随 `n` 增大很快爆炸。  
- **空间复杂度**：`O(n + k)` —— 递归栈深度 `n`，加上 `k` 大小的 `load` 数组。对本题几乎可以忽略。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **大量重复的搜索**：很多分配在中途已经明显比当前最好的答案更差，却仍然继续往下搜索。我们可以在搜索过程中**提前剪枝**，把这种“注定不会更好”的分支直接扔掉。

优化思路分三步：

1. **先把大袋子先安排**  
   - 把 `cookies` 按从大到小排序。这样在搜索时，先放“大块”会更快让某个孩子的背包“爆炸”，从而更早触发剪枝。  
   - 类比：装箱时先装大箱子，能更快发现装不下的情况。

2. **使用分支限界（Branch & Bound）**  
   - 在递归的每一步，计算当前所有孩子的最大背包 `cur_max = max(load)`。  
   - 如果 `cur_max` 已经 **不小于** 当前已经找到的最优答案 `best`，说明继续往下分配只会让最大值更大或保持不变，**没有必要继续**，直接返回。

3. **对称剪枝**  
   - 当我们把一袋饼干放进一个空背包（`load[i] == 0`）时，后面的空背包与它是等价的，不需要再尝试把同一袋放进其他空背包。这样可以把搜索空间再缩小约 `k!`（阶乘）倍。

综合以上三点，搜索树的规模会大幅下降，能够在极短时间内得到最优答案。由于题目本身 `n ≤ 8`，即使是最坏情况也能轻松跑完。

**核心算法**：**回溯 + 剪枝**（不需要额外的 DP 表或位运算），但在实现时要注意**排序**、**提前返回**和**对称剪枝**这三个技巧。

#### 代码（Python）

```python
from typing import List

def distribute_cookies_optimal(cookies: List[int], k: int) -> int:
    # 1. 先把大袋子排在前面，方便早剪枝
    cookies.sort(reverse=True)

    load = [0] * k               # 每个孩子的当前背包容量
    best = float('inf')          # 记录目前找到的最小不公平度

    def dfs(idx: int):
        """把第 idx 袋饼干分配给某个孩子，使用剪枝优化"""
        nonlocal best

        # 所有袋子已经分配完，更新答案
        if idx == len(cookies):
            best = min(best, max(load))
            return

        cur_cookie = cookies[idx]

        # 为了避免对称情况：只在第一次遇到空背包时尝试放入
        visited = set()          # 记录已经尝试过的背包容量，防止相同容量的背包重复尝试

        for i in range(k):
            # ① 对称剪枝：如果这个孩子的背包容量已经在本层尝试过，跳过
            if load[i] in visited:
                continue
            visited.add(load[i])

            # ② 分支限界：如果放进去后最大背包已经 >= best，直接剪枝
            load[i] += cur_cookie
            if load[i] < best:    # 只有潜在会更好时才继续往下搜索
                dfs(idx + 1)
            # ③ 回溯
            load[i] -= cur_cookie

            # 如果当前孩子本来是空的，放完后又回到空，说明后面的空孩子与它等价，直接结束循环
            if load[i] == 0:
                break

    dfs(0)
    return best
```

> **关键行解释**  
> - `cookies.sort(reverse=True)`：把大袋子先处理，提升剪枝概率。  
> - `visited` 集合：同一层中，如果两个孩子的当前背包容量相同，后者的尝试没有意义（对称剪枝）。  
> - `if load[i] < best:`：只有在当前最大背包仍然小于已知最优解时才继续递归，否则直接剪掉这条枝。  
> - `if load[i] == 0: break`：第一次把饼干放进一个空背包后，后面的空背包不需要再尝试，避免重复。

#### 复杂度

- **时间复杂度**：最坏情况下仍是 `O(kⁿ)`，但实际搜索的节点数因为剪枝会大幅减少。对于本题的约束（`n ≤ 8, k ≤ n`），实际运行时间在毫秒级。可以把它理解为 **“指数级但常数因子很小”**。  
- **空间复杂度**：`O(n + k)`，递归栈深度 `n`，加上 `load` 数组大小 `k`。与暴力解相同，但因为搜索更快结束，实际占用的栈空间更少。

---

## 心得

- **核心技巧**：**回溯 + 剪枝**（包括先排序、分支限界、对称剪枝）。  
- **适用题型**：  
  1. **分配类**问题，如 “分配糖果”“任务分配”“工作分配” 需要最小化最大负荷。  
  2. **背包类**的 “枚举所有放置方式” 场景，尤其当元素个数 ≤ 15 时。  
  3. **组合优化** 中需要搜索全部组合但可以提前判断“这条路走不通”的情况。  
- **一句话总结**：**把“大块先放”，用“当前最差 ≥ 已知最优”时立刻停下来，就是解这类最小最大分配题的钥匙。**

---

## 反思

- **第一反应**：看到“把所有袋子分给 k 个人”，立刻想到“枚举所有可能的分配”，于是写出暴力递归。  
- **最容易踩的坑**：  
  - 忘记 **对称剪枝**（空背包的重复尝试），导致搜索时间指数级爆炸。  
  - 没有 **提前排序**，大袋子放在后面会让剪枝失效，运行慢很多。  
  - 在剪枝时只比较 **当前最大** 而不是 **可能的最小**，会误剪掉合法解。  
- **下次类似题**，第一步应该想到：**“先把大东西处理，再用‘当前最差 >= 已知最优’的界限剪枝”**，这样搜索空间会立刻大幅缩小。