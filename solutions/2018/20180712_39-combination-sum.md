# #39. **组合总和** / Combination Sum

> 难度：中等 · 标签：Array、Backtracking · [LeetCode 链接](https://leetcode.com/problems/combination-sum/)

---

## 题目（英文原版）

**Description**

Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.
The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.
The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.

**Examples**

**Example 1:**

```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
```

**Example 2:**

```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

**Example 3:**

```
Input: candidates = [2], target = 1
Output: []
```

**Constraints**

- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 40

---

## 题目（中文翻译）

给定一个由互不相同的整数构成的数组 `candidates` 和一个目标整数 `target`，返回所有 **唯一组合**（unique combinations），使得组合中选取的数字之和等于 `target`。你可以以任意顺序返回这些组合。

同一个数字可以在 `candidates` 中被选择 **无限次**（unlimited number of times）。如果至少有一种数字在两个组合中的出现次数不同，则这两个组合被视为不同的唯一组合。

测试用例保证，对于给定的输入，满足条件的唯一组合数量少于 150 条。

---

#### 示例

**示例 1**  
**输入**: `candidates = [2,3,6,7]`, `target = 7`  
**输出**: `[[2,2,3],[7]]`  
**解释**:  
- `2` 和 `3` 都是候选数，且 `2 + 2 + 3 = 7`。注意 `2` 可以被多次使用。  
- `7` 本身也是候选数，且 `7 = 7`。  
这就是唯一的两种组合。

**示例 2**  
**输入**: `candidates = [2,3,5]`, `target = 8`  
**输出**: `[[2,2,2,2],[2,3,3],[3,5]]`

**示例 3**  
**输入**: `candidates = [2]`, `target = 1`  
**输出**: `[]`

---

#### 约束条件

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- `candidates` 中的所有元素互不相同。
- `1 <= target <= 40`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把「所有可能的取法」全部枚举一遍，只要把每一种取法的和算出来，等于 `target` 的就留下。  
可以把它想象成「在超市里挑商品」：

- **candidates** 就像超市里不同种类的商品（每种商品的价格是它的数值）。
- 我们可以无限次挑选同一种商品（题目允许同一个数重复使用）。
- 目标是让挑选的商品总价恰好等于 `target`。

最暴力的做法是：

1. 维护一个列表 `path` 记录当前已经挑选的商品（即当前的组合）。
2. 从 `candidates` 中任选一个商品加入 `path`，继续递归尝试加入更多商品。
3. 每次递归结束时检查 `path` 的和是否等于 `target`，如果相等就把这条 `path` 保存下来。
4. 递归的终止条件有两种：  
   - 和已经超过 `target` → 这条路走不通，直接返回。  
   - 已经遍历完所有商品 → 没有更多选择，返回。

**为什么正确**  
因为我们把「所有可能的挑选顺序」都走了一遍（每一次都可以把同一个商品再挑一次），所以只要有满足条件的组合，它一定会在某一次递归里被完整构造出来并被记录。

**复杂度分析（大白话）**  
- 时间复杂度：最坏情况下，我们会尝试所有长度 ≤ `target/min(candidates)` 的组合。每一步都有 `len(candidates)` 种选择，形成一棵 `len(candidates)` 分支的递归树，深度约为 `target / min(candidates)`。所以时间复杂度大约是 `O(k^n)`（指数级），这里的 `k = len(candidates)`，`n = target/min`。用大白话说，就是「可能的组合数会随目标值和候选数的增多而指数爆炸」。
- 空间复杂度：递归调用栈的深度等于组合的最大长度，最多 `target / min(candidates)`，再加上保存答案的空间（答案本身的大小）。所以是 `O(target/min + answer)`。

#### 代码（Python）

```python
from typing import List

def combinationSum_bruteforce(candidates: List[int], target: int) -> List[List[int]]:
    res: List[List[int]] = []          # 用来装所有满足条件的组合

    def backtrack(start: int, cur_sum: int, path: List[int]) -> None:
        """
        start   : 本层递归可以从哪一个下标开始取数
                  （因为可以重复使用同一个数，所以这里可以继续从 start 开始）
        cur_sum : 当前路径里所有数的和
        path    : 已经选好的数的列表（组合）
        """
        # 1️⃣ 递归终止条件——和已经等于 target，保存答案
        if cur_sum == target:
            res.append(path.copy())    # 复制一份防止后面改动影响已保存的答案
            return
        # 2️⃣ 和已经超过 target，说明这条路不可能成功，直接剪枝返回
        if cur_sum > target:
            return

        # 3️⃣ 继续尝试把后面的每一个数加入组合
        for i in range(start, len(candidates)):
            # 把 candidates[i] 加入当前路径
            path.append(candidates[i])
            # 递归：因为可以重复使用同一个数，start 仍然是 i
            backtrack(i, cur_sum + candidates[i], path)
            # 回溯：把刚才加入的数弹出来，尝试下一个数
            path.pop()

    # 从下标 0 开始搜索，当前和为 0，路径为空
    backtrack(0, 0, [])
    return res
```

#### 复杂度

- **时间复杂度**：`O(k^n)`，其中 `k = len(candidates)`，`n = target / min(candidates)`。这表示随着目标值变大或候选数增多，搜索空间会呈指数增长。
- **空间复杂度**：`O(n + m)`，`n` 为递归深度（即当前组合的最大长度），`m` 为答案列表本身占用的空间（因为必须把所有合法组合都保存下来）。

---

### 2. 最优解

#### 思路  

暴力解已经是「枚举」的思路，只是没有利用**剪枝**（提前把不可能成功的分支剔除）。  
要把搜索空间压得更小，需要在递归的每一步做两件事：

1. **排序 + 剪枝**  
   - 把 `candidates` 从小到大排序。这样在递归时，如果当前数已经让和超过 `target`，后面的数（更大）一定也会超过，直接停止循环即可。
2. **避免无效的重复搜索**  
   - 在每一层递归里，只从当前下标 `i` 开始往后取数（即 `for i in range(start, len(candidates))`），这样可以防止「同一组合只出现不同顺序的多次」。
   - 仍然允许同一个数多次使用，因为递归时 `start` 仍然是 `i`（不向后移动）。

把这两点加进去后，搜索树的宽度会大幅下降，尤其当 `target` 较大时，很多“已经超出目标”的分支会在第一时间被剪掉。

**核心技巧：回溯 + 剪枝**  
- **回溯**：在搜索过程中不断尝试、撤销（`path.append` / `path.pop`），类似于在迷宫里走一步、回头再走另一条路。
- **剪枝**：提前判断「这条路不可能成功」就不继续往下走，节省时间。

下面的代码把排序和剪枝写进去，就是本题的「最优」实现（在题目约束下已经足够高效）。

#### 代码（Python）

```python
from typing import List

def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    # 1️⃣ 先把候选数从小到大排好序，便于后面的剪枝
    candidates.sort()
    res: List[List[int]] = []

    def dfs(start: int, cur_sum: int, path: List[int]) -> None:
        """
        start   : 本层搜索可以使用的最小下标（保证组合不出现不同顺序的重复）
        cur_sum : 当前组合的总和
        path    : 已经选好的数
        """
        # 2️⃣ 达到目标，保存答案
        if cur_sum == target:
            res.append(path.copy())
            return
        # 3️⃣ 如果已经超过目标，直接返回（剪枝）
        if cur_sum > target:
            return

        # 4️⃣ 从 start 开始尝试每一个候选数
        for i in range(start, len(candidates)):
            # 因为数组已经排好序，如果加上 candidates[i] 已经超过 target，
            # 说明后面的数（更大）一定也会超过，直接 break
            if cur_sum + candidates[i] > target:
                break
            # 选取 candidates[i]
            path.append(candidates[i])
            # 递归：仍然可以继续使用 i（因为同一个数可以重复使用）
            dfs(i, cur_sum + candidates[i], path)
            # 撤销选择，尝试下一个数
            path.pop()

    dfs(0, 0, [])
    return res
```

#### 复杂度

- **时间复杂度**：`O(k^n)` 的上界仍然成立（因为最坏情况下仍可能遍历所有组合），但实际运行时因为**排序 + 提前剪枝**，搜索的节点数会大幅减少。用大白话说，就是「我们只走那些有希望成功的路，浪费的时间比暴力解少很多」。
- **空间复杂度**：`O(n + m)`，和暴力解相同。`n` 为递归深度（最多 `target / min(candidates)`），`m` 为保存答案的空间。

---

## 心得

- **核心技巧**：**回溯 + 剪枝**（排序后提前结束循环）。回溯负责枚举所有可能的组合，剪枝负责把不可能成功的分支及时砍掉。
- **适用题型**  
  1. **组合求和类**：`Combination Sum II`（每个数只能使用一次，需要去重），`Combination Sum III`（找出 k 个数相加为 n 的所有组合）。  
  2. **子集/排列类**：`Subsets`、`Permutations`（同样用回溯，只是剪枝条件不同）。  
  3. **棋盘/路径类**：`Word Search`、`N-Queens`（需要在搜索过程中提前判断冲突）。
- **一句话总结**：**“先把搜索空间排序，再在递归时用当前和判断是否已经超标，超标就立即止步”。**

---

## 反思

- **第一反应**：直接写一个深度优先搜索，遍历所有可能的取法，然后把满足条件的组合收集起来。  
- **最容易踩的坑**  
  1. **重复组合**：如果不控制每层递归的起始下标，`[2,3]` 与 `[3,2]` 会被算两次。  
  2. **无限递归**：忘记在 `cur_sum > target` 时返回，导致递归永远向下进行。  
  3. **剪枝遗漏**：没有对已排序的数组使用 `break`，会继续遍历已经确定不可能成功的更大数。  
- **下次类似题目第一步**：**先把数组排序，然后写回溯框架并在递归入口加上“和超出目标就返回”的剪枝条件**。这样可以快速定位搜索的边界，避免不必要的遍历。