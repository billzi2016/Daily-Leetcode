# #40. 组合总和 II / Combination Sum II

> 难度：中等 · 标签：Array、Backtracking · [LeetCode 链接](https://leetcode.com/problems/combination-sum-ii/)

---

## 题目（英文原版）

**Description**

Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.
Each number in candidates may only be used once in the combination.
Note: The solution set must not contain duplicate combinations.

**Examples**

**Example 1:**

```
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: 
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]
```

**Example 2:**

```
Input: candidates = [2,5,2,1,2], target = 5
Output: 
[
[1,2,2],
[5]
]
```

**Constraints**

- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30

---

## 题目（中文翻译）

给定一个候选数字集合 `candidates`（数组）和一个目标数字 `target`，找出所有 **唯一** 的组合，使得组合中数字的和等于 `target`。  
每个数字在一次组合中只能使用 **一次**。  
注意：答案集合中不能出现重复的组合。

**示例 1**  
```text
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: 
[
  [1,1,6],
  [1,2,5],
  [1,7],
  [2,6]
]
```

**示例 2**  
```text
Input: candidates = [2,5,2,1,2], target = 5
Output: 
[
  [1,2,2],
  [5]
]
```

**约束条件**

- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子集**，把每个子集里数字的和算出来，等于 `target` 的就保存。  
这和我们在超市挑选商品的过程类似：把所有商品（`candidates`）都列出来，然后**随意挑选任意数量的商品**，看看挑完的总价是否正好是我们想要的金额。  

- **用到的数据结构**  
  - `list`（列表）保存当前正在尝试的组合。可以把它想象成手里装的购物篮。  
  - `list`（结果列表）保存所有满足条件的组合。相当于记账本，记录每一次成功的购物方案。  

- **为什么正确**  
  - 我们遍历了**所有**可能的挑选方式（包括不挑、只挑一个、挑两个、…），只要有一种方式的和恰好等于 `target`，就一定会被我们找到并加入结果。  

- **时间/空间复杂度**  
  - 对 `n` 个元素，子集的数量是 `2ⁿ`（因为每个元素有“选”或“不选”两种状态），所以最坏情况下我们要检查 `2ⁿ` 种组合。  
  - 计算每个组合的和需要遍历该组合的长度，平均大约是 `n/2`，所以整体时间复杂度约为 **O( n·2ⁿ )**。  
    - 大白话：如果有 20 个数字，2ⁿ≈1,048,576，基本上是**指数级**增长，算起来会非常慢。  
  - 递归调用的栈深度最深是 `n`，再加上保存当前组合的列表，空间复杂度是 **O(n)**（不计结果集的空间）。

#### 代码（Python）

```python
from typing import List

def combination_sum2_brute(candidates: List[int], target: int) -> List[List[int]]:
    res: List[List[int]] = []          # 最终答案

    n = len(candidates)

    # dfs(idx, cur_sum, path) 递归遍历所有子集
    def dfs(idx: int, cur_sum: int, path: List[int]) -> None:
        # 1. 到达叶子节点（遍历完所有元素）
        if idx == n:
            if cur_sum == target:      # 和恰好等于目标
                res.append(path.copy())
            return

        # 2. 不选当前元素，直接跳到下一个
        dfs(idx + 1, cur_sum, path)

        # 3. 选当前元素（注意题目要求每个数字只能用一次）
        dfs(idx + 1, cur_sum + candidates[idx], path + [candidates[idx]])

    dfs(0, 0, [])
    return res
```

#### 复杂度

- **时间复杂度**：O(n·2ⁿ)  
  - 解释：指数级的子集数 `2ⁿ` 再乘上每次计算和的代价，等价于遍历所有可能的挑选方式。  
- **空间复杂度**：O(n)  
  - 解释：递归栈最深 `n` 层，加上临时保存当前组合的列表（最多 `n` 长），不计最终答案的存储。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**盲目枚举所有子集**，其中大量组合的和早已超出 `target`，但我们仍然继续递归下去，浪费时间。  
要优化，需要在**搜索的过程中及时剪枝**，并且**避免产生相同的组合**（题目要求唯一解）。思路如下：

1. **先排序**  
   将 `candidates` 按升序排列。排序后相同的数字会相邻，这为去重提供便利，也能让我们在遍历时提前判断后面的数字是否会导致和超标。

2. **回溯（Backtracking）**  
   与暴力解类似，我们仍然采用深度优先搜索，但每一步都检查两个条件：
   - **剪枝**：如果当前累计的和 `cur_sum + candidates[i] > target`，因为数组已排序，后面的数字更大，只要当前已经超了，后面的都不可能满足，直接 `break`。
   - **去重**：在同一层递归中，如果 `i > start` 且 `candidates[i] == candidates[i-1]`，说明这个数字在本层已经尝试过一次，继续使用会产生重复组合，直接 `skip`（`continue`）。

3. **使用“起始索引”**  
   为了保证每个数字**只能使用一次**，递归时的下一个起始位置是 `i + 1`，而不是 `i`（后者会导致同一个元素被多次选取）。

4. **路径保存**  
   当 `cur_sum == target` 时，把当前路径的拷贝加入结果。

> 类比：想象我们在超市里挑商品，**先把商品从便宜到贵排好**。挑的时候，如果已经挑的总价超过预算，就不必继续往后挑更贵的商品了；如果发现前面已经挑过同样价位的商品，且这次挑的方式和上一次完全一样，就直接跳过，防止出现重复的购物清单。

#### 代码（Python）

```python
from typing import List

def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    candidates.sort()                 # 1️⃣ 排序，便于剪枝和去重
    res: List[List[int]] = []        # 最终答案

    def backtrack(start: int, cur_sum: int, path: List[int]) -> None:
        # 2️⃣ 达到目标，保存结果
        if cur_sum == target:
            res.append(path.copy())
            return
        # 3️⃣ 遍历候选数字
        for i in range(start, len(candidates)):
            # 3.1 剪枝：后面的数字更大，只要当前和已经超了，就可以直接退出循环
            if cur_sum + candidates[i] > target:
                break
            # 3.2 去重：同一层中，跳过与前一个相同的数字
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            # 3.3 选取当前数字，进入下一层（下一个起点是 i+1，保证每个数字只能用一次）
            path.append(candidates[i])
            backtrack(i + 1, cur_sum + candidates[i], path)
            path.pop()                 # 回溯，撤销选择

    backtrack(0, 0, [])
    return res
```

#### 复杂度

- **时间复杂度**：O(2ⁿ)（最坏情况）  
  - 解释：虽然仍然是指数级搜索，但剪枝和去重大幅削减了实际遍历的分支。对多数输入，实际运行时间远低于暴力解。  
- **空间复杂度**：O(n)  
  - 解释：递归栈深度最多为 `n`，加上当前路径的存储，仍然是线性空间。

---

## 心得

- **核心技巧**：**排序 + 回溯 + 剪枝 + 同层去重**。  
- **适用题型**：  
  1. 组合求和类（如 *Combination Sum I/II*、*Combination Sum III*）  
  2. 子集去重类（如 *Subsets II*）  
  3. 产生所有唯一排列/组合的题目（如 *Permutations II*）  
- **一句话总结解题钥匙**：**先把数据排好序，再用回溯逐层尝试，遇到“已经超出目标”或“本层已出现相同数字”时立刻停下或跳过。**

## 反思

- **第一反应**：想到“枚举所有子集”，直接写递归遍历。  
- **最容易踩的坑**  
  - **重复组合**：没有去重会得到大量相同的答案。  
  - **使用同一数字多次**：忘记在递归时把起始索引设为 `i+1`。  
  - **剪枝时机**：如果不在排序后进行 `break`，会继续遍历无意义的分支，导致超时。  
- **下次类似题的第一步**：**先对输入进行排序**，再决定是否可以通过“当前和 > 目标”提前剪枝。这样既能防止重复，又能大幅提升效率。