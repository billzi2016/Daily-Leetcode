# #46. 全排列 / Permutations

> 难度：中等 · 标签：Array、Backtracking · [LeetCode 链接](https://leetcode.com/problems/permutations/)

---

## 题目（英文原版）

**Description**

Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Example 2:**

```
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

**Example 3:**

```
Input: nums = [1]
Output: [[1]]
```

**Constraints**

- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

---

## 题目（中文翻译）

给定一个由互不相同的整数构成的数组（array）`nums`，返回所有可能的排列（permutations）。答案可以以任意顺序返回。

示例 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

示例 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]

示例 3:
Input: nums = [1]
Output: [[1]]

约束条件：
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- `nums` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有数字一个一个挑出来，放进当前的排列里，等把所有数字都挑完就得到一种完整的排列。  
这其实就是**回溯（Backtracking）**的雏形——我们在一棵“选择树”里深度优先搜索。

- **用到的数据结构**  
  - `list path`：记录当前已经挑好的数字，类似于我们在做菜时已经放进锅里的材料。  
  - `list used`（布尔数组）或 `set`：标记哪些数字已经被挑过，像是字典里的“是否已经翻到这一页”。  

- **为什么正确**  
  对于每一步，我们都尝试把 **所有** 还没有用过的数字放进去。递归结束时，`path` 长度等于原数组长度，说明已经把每个数字恰好用了一次，这正是一种合法的排列。遍历完所有分支后，所有可能的排列自然都会被枚举出来。

- **复杂度大白话**  
  - **时间复杂度**：`O(n! * n)`  
    - `n!` 表示排列的总数，像是把 3 本书全部排成不同顺序有 `3! = 6` 种。  
    - 每产生一个排列都要复制 `path`（长度 `n`），所以整体是 `n!` 次乘以 `n`。  
  - **空间复杂度**：`O(n)`（递归栈 + `path`）  
    - 递归最多会嵌套 `n` 层，每层只保存常数信息，加上 `path` 长度为 `n`，整体随 `n` 线性增长。

#### 代码（Python）

```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    res: List[List[int]] = []          # 最终要返回的所有排列
    used = [False] * len(nums)         # 标记每个位置的数字是否已经被使用
    path: List[int] = []               # 当前递归层已经选好的数字

    def backtrack():
        # 递归终止条件：path 长度已经和原数组相同，得到一个完整的排列
        if len(path) == len(nums):
            # 把当前排列拷贝一份加入结果集中（拷贝很重要！）
            res.append(path.copy())
            return

        # 遍历所有数字，尝试把「未使用」的数字放到下一个位置
        for i in range(len(nums)):
            if used[i]:
                continue                  # 这个数字已经在当前路径里，跳过
            # 做选择
            used[i] = True
            path.append(nums[i])
            # 进入下一层搜索
            backtrack()
            # 撤销选择（回溯），为后面的分支腾出位置
            path.pop()
            used[i] = False

    backtrack()      # 开始递归
    return res
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  解释：所有合法排列的数量是 `n!`，每生成一个排列都要复制长度为 `n` 的列表，所以总工作量约等于 `n!` 乘 `n`。

- **空间复杂度**：`O(n)`  
  解释：递归栈最多 `n` 层，加上 `path` 列表最多存 `n` 个元素，都是随 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每次递归都要遍历整个 `used` 数组（`O(n)`）以及复制 `path`（`O(n)`）。  
其实我们可以把“是否已使用”这个信息直接编码进 **原数组本身**，通过**原地交换**来完成“挑选”和“撤销”。这样：

1. 把第 `i` 位的数字和当前层对应的数字交换，等价于把它挑进当前排列。  
2. 递归结束后再把两者换回来，完成撤销（回溯）。  
3. 当递归层数等于数组长度时，`nums` 本身已经被排列成一种合法顺序，直接把它拷贝进答案即可。

这样做的好处是：

- **不需要额外的 `used` 数组**，因为已经通过交换把「已使用」的数字放到了前面。  
- **只在递归结束时复制一次完整的排列**，而不是每一步都拷贝 `path`，减少了常数因子。  

这就是**经典的原地回溯（in‑place backtracking）**，在排列、组合这类“全排列”题目中最常用、最简洁的实现。

#### 代码（Python）

```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    res: List[List[int]] = []

    def backtrack(first: int):
        """
        first 表示当前要固定的位置（从 0 开始）。
        把 nums[first:] 中的每个元素依次放到位置 first 上，递归生成后面的排列。
        """
        # 当 first 指向最后一个位置的下一格，说明所有位置都已经确定
        if first == len(nums):
            res.append(nums.copy())   # 把当前完整的排列拷贝进结果
            return

        # 依次把第 first 位之后的每个元素（包括自己）放到 first 位
        for i in range(first, len(nums)):
            # 交换，把 nums[i] 挑到当前层的“第一位”
            nums[first], nums[i] = nums[i], nums[first]
            # 继续固定下一位
            backtrack(first + 1)
            # 撤销交换，恢复原数组，为后续循环做准备
            nums[first], nums[i] = nums[i], nums[first]

    backtrack(0)   # 从第 0 位开始固定
    return res
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  解释：虽然我们省掉了每层 `used` 检查和 `path` 复制，但最终仍然要输出 `n!` 个长度为 `n` 的排列，所以总体工作量仍是 `n! * n`。与暴力解的时间复杂度相同，只是常数更小，实际运行更快。

- **空间复杂度**：`O(n)`  
  解释：递归栈深度为 `n`，另外只使用了原数组 `nums`（原地操作）和结果列表 `res`（存放所有排列，不计入额外空间）。因此额外空间随 `n` 线性增长。

---

## 心得

- **核心技巧**：原地回溯（利用交换把「已使用」信息直接写进数组），这是处理全排列、全组合时的「省时省力」钥匙。  
- **适用的题型**  
  1. **全排列**（LeetCode 46）  
  2. **全排列 II**（含重复元素，需要去重）  
  3. **组合**（LeetCode 77）——虽然不需要交换，但同样使用回溯框架。  
- **一句话总结**：把「挑选」和「撤销」用一次元素交换来完成，既省空间又省复制。

## 反思

- **第一反应**：看到“返回所有可能的排列”，立刻想到递归遍历每一种选法——也就是回溯。  
- **最容易踩的坑**  
  - 忘记在递归结束时复制当前排列（直接把 `nums` 加进 `res` 会导致后面修改影响已保存的答案）。  
  - 交换后没有及时撤销，导致后面的分支基于错误的数组状态。  
  - 对长度为 0 的输入没有做好防御（本题约束 `len >= 1`，但写通用代码时要考虑）。  
- **下次第一步**：先确认「是否需要原地操作」——如果题目只要求返回所有排列且数组元素唯一，原地回溯是最直接且高效的思路。