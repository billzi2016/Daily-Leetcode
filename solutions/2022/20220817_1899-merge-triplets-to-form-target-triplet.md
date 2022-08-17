# #1899. 合并三元组以形成目标三元组 / Merge Triplets to Form Target Triplet

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)

---

## 题目（英文原版）

**Description**

A triplet is an array of three integers. You are given a 2D integer array triplets, where triplets[i] = [ai, bi, ci] describes the ith triplet. You are also given an integer array target = [x, y, z] that describes the triplet you want to obtain.
To obtain target, you may apply the following operation on triplets any number of times (possibly zero):
Return true if it is possible to obtain the target triplet [x, y, z] as an element of triplets, or false otherwise.

**Examples**

**Example 1:**

```
Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
Output: true
Explanation: Perform the following operations:
- Choose the first and last triplets [[2,5,3],[1,8,4],[1,7,5]]. Update the last triplet to be [max(2,1), max(5,7), max(3,5)] = [2,7,5]. triplets = [[2,5,3],[1,8,4],[2,7,5]]
The target triplet [2,7,5] is now an element of triplets.
```

**Example 2:**

```
Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
Output: false
Explanation: It is impossible to have [3,2,5] as an element because there is no 2 in any of the triplets.
```

**Example 3:**

```
Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
Output: true
Explanation: Perform the following operations:
- Choose the first and third triplets [[2,5,3],[2,3,4],[1,2,5],[5,2,3]]. Update the third triplet to be [max(2,1), max(5,2), max(3,5)] = [2,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,2,3]].
- Choose the third and fourth triplets [[2,5,3],[2,3,4],[2,5,5],[5,2,3]]. Update the fourth triplet to be [max(2,5), max(5,2), max(5,3)] = [5,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,5,5]].
The target triplet [5,5,5] is now an element of triplets.
```

**Constraints**

- 1 <= triplets.length <= 105
- triplets[i].length == target.length == 3
- 1 <= ai, bi, ci, x, y, z <= 1000

---

## 题目（中文翻译）

**描述**  
三元组（triplet）是长度为 3 的整数数组。给定一个二维整数数组 `triplets`，其中 `triplets[i] = [a_i, b_i, c_i]` 表示第 *i* 个三元组。同时给定一个整数数组 `target = [x, y, z]`，表示你希望得到的目标三元组。

为了得到 `target`，可以对 `triplets` 任意次（可能为零次）执行以下操作：  
选取两个不同下标 `i` 与 `j`（`i ≠ j`），用元素逐位取最大值的结果替换下标为 `i` 的三元组，即  
`triplets[i] = [max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)]`。

如果能够让目标三元组 `[x, y, z]` 成为 `triplets` 中的某个元素，则返回 `true`；否则返回 `false`。

---

**示例**

**示例 1**  
```text
Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
Output: true
Explanation: 执行如下操作：
- 选取第一个和最后一个三元组，更新最后一个三元组为
  [max(2,1), max(5,7), max(3,5)] = [2,7,5]。
  此时 triplets = [[2,5,3],[1,8,4],[2,7,5]]。
目标三元组 [2,7,5] 已经出现在数组中。
```

**示例 2**  
```text
Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
Output: false
Explanation: 无法得到 [3,2,5]，因为所有三元组中都不存在数值 2。
```

**示例 3**  
```text
Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
Output: true
Explanation: 执行如下操作：
- 选取第一个和第三个三元组，更新第三个三元组为
  [max(2,1), max(5,2), max(3,5)] = [2,5,5]。
  此时 triplets = [[2,5,3],[2,3,4],[2,5,5],[5,2,3]]。
- 再选取第三个和第四个三元组，更新第三个三元组为
  [max(2,5), max(5,2), max(5,3)] = [5,5,5]。
  此时 triplets 包含目标三元组 [5,5,5]，返回 true。
```

---

**约束条件**  
- `1 <= triplets.length <= 10^5`  
- `triplets[i].length == target.length == 3`  
- `1 <= a_i, b_i, c_i, x, y, z <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把所有可能的合并顺序都枚举一遍**，只要有一种合并方式能够得到目标三元组 `[x, y, z]`，答案就返回 `True`。  

- **合并操作**：任选两条三元组 `a = [a1, a2, a3]`、`b = [b1, b2, b3]`，把其中一条（比如 `a`）替换成 `max(a, b)`，即  
  `a' = [max(a1, b1), max(a2, b2), max(a3, b3)]`。  
- 这就好像我们有 **一堆颜色卡**，每次可以把两张卡的颜色取“更深的那种”，最终想得到一张恰好是目标颜色的卡。  

**暴力做法**：  
1. 把所有三元组的子集（即任意挑选若干条）列出来。  
2. 对每个子集，依次把里面的三元组两两合并（顺序随意），得到的最终三元组记为 `cur`。  
3. 检查 `cur` 是否等于目标 `[x, y, z]`。  

因为我们把 **所有子集** 都尝试了一遍，所以一定不会漏掉任何可能的合并方式，答案的正确性是显而易见的。  

> **时间/空间复杂度**  
> - 子集的数量是 `2ⁿ`（`n` 为三元组的个数），每个子集内部最多要合并 `n` 次，所以时间复杂度大约是 `O(n·2ⁿ)`，这在 `n` 甚至稍大时都会爆炸。  
> - 为了保存子集我们需要额外的 `O(2ⁿ)` 空间（实际实现时可以用递归回溯省一点空间），但总体上这已经不是可接受的算法了。  

#### 代码（Python）  

```python
from itertools import combinations
from copy import deepcopy
from typing import List

def merge(a: List[int], b: List[int]) -> List[int]:
    """返回两条三元组的逐位最大值"""
    return [max(a[i], b[i]) for i in range(3)]

def brute_force(triplets: List[List[int]], target: List[int]) -> bool:
    n = len(triplets)

    # 枚举所有非空子集（大小从 1 到 n）
    for sz in range(1, n + 1):
        for idxs in combinations(range(n), sz):
            # 复制子集中所有三元组，准备合并
            cur = deepcopy([triplets[i] for i in idxs])

            # 任意顺序两两合并，这里简单地一次性把所有元素
            # 合并到第一个位置上（顺序不影响 max 的结果）
            merged = cur[0]
            for i in range(1, len(cur)):
                merged = merge(merged, cur[i])

            if merged == target:          # 找到目标
                return True
    return False                         # 所有子集都不行
```

> **关键行解释**  
> - `combinations(range(n), sz)`: 类比“从 n 本书里挑 sz 本”，遍历所有可能的挑选方式。  
> - `merge(merged, cur[i])`: 把两本书的页码取“大的一页”，对应题目中的逐位取最大。  

#### 复杂度  

- **时间复杂度**：`O(n·2ⁿ)` —— 因为要遍历所有子集，指数级增长。  
- **空间复杂度**：`O(n)`（递归版会更高），主要用于保存临时的合并结果。  

> 大白话：`2ⁿ` 相当于“把所有可能的选法都列出来”，当 `n = 20` 时已经是 **一百万** 种，远远超出一秒能处理的范围。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正决定能否得到目标的，是每个坐标上的最大值**。  
观察 `max` 的两个重要特性：

1. **单调性**：如果 `a ≤ x` 且 `b ≤ x`，那么 `max(a, b) ≤ x`。换句话说，只要所有参与合并的数都不超过目标对应的坐标，合并后的结果也一定不会超过目标。  
2. **覆盖性**：如果我们能找到若干条三元组，使得它们在每个坐标上都 **恰好** 达到目标值（其余坐标不超过目标），那么把这些三元组依次合并，最终必然得到 `[x, y, z]`。  

于是可以把注意力 **只放在“合法的三元组”** 上：  
- 对于目标 `[x, y, z]`，只关心那些 **每个元素都不大于对应目标** 的三元组（`a ≤ x && b ≤ y && c ≤ z`）。  
- 其余的三元组即使参与合并，也会把某个坐标“推过头”，导致最终结果超出目标，永远不可能得到目标。  

在这些合法三元组里，我们只需要检查：

- 是否至少有一条三元组的第一位等于 `x`（其它两位 ≤ 对应目标），  
- 是否至少有一条三元组的第二位等于 `y`（其它两位 ≤ 对应目标），  
- 是否至少有一条三元组的第三位等于 `z`（其它两位 ≤ 对应目标）。

只要这三个条件同时满足，就可以把它们（可能是同一条，也可能是三条不同的）合并得到目标；否则无论怎么合并都不行。

> **类比**：把目标看成“一把钥匙”，每个坐标是钥匙的一个齿。我们只需要找到能恰好卡住每个齿的钥匙片段（不超过目标），把它们拼在一起就能打开锁。

#### 代码（Python）  

```python
from typing import List

def can_form_target(triplets: List[List[int]], target: List[int]) -> bool:
    x, y, z = target
    # 用三个布尔变量记录是否已经找到对应坐标的“恰好等于目标”的合法三元组
    has_x = has_y = has_z = False

    for a, b, c in triplets:
        # 只考虑“每个坐标都不超过目标”的三元组
        if a <= x and b <= y and c <= z:
            if a == x:   # 第一位已经达到目标
                has_x = True
            if b == y:   # 第二位已经达到目标
                has_y = True
            if c == z:   # 第三位已经达到目标
                has_z = True

    # 三个坐标都被覆盖了，说明可以合并得到目标
    return has_x and has_y and has_z
```

> **关键行解释**  
> - `if a <= x and b <= y and c <= z:`：相当于“把不合格的三元组踢出筛子”，只留下不会把坐标推过头的。  
> - `has_x = True` 等：记录“已经找到一个可以提供第一位 x 的合法片段”。  

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次 `triplets`，每条记录做常数次比较。  
- **空间复杂度**：`O(1)`，只用三个布尔变量，和输入规模无关。  

> 与暴力解相比：我们从 **指数级** 降到了 **线性**，在 `n = 10⁵` 时也能在毫秒级完成。

---

## 心得  

- **核心技巧**：利用 `max` 的单调性，只保留“每个维度都不超过目标”的候选，随后检查每个维度是否至少出现一次等于目标的值。  
- **适用题型**（类似思路）：  
  1. *Maximum Top Row of a Matrix*（逐位取最大，需要每列都满足条件）。  
  2. *Make Array Strictly Increasing*（每个位置的值只能在一定范围内递增）。  
  3. *Check If All Elements Are Positive*（只关心是否所有元素满足上界/下界）。  
- **一句话总结**：**只要在不超限的前提下，找到每个坐标恰好等于目标的“拼图块”，就一定能拼出目标。**

---

## 反思  

- **第一反应**：看到“取 max”就想到把所有三元组都合并一次，检查结果是否等于目标。  
- **最容易踩的坑**：  
  - 忽略了“不能超过目标”的限制，导致错误地认为只要有一条三元组的某个坐标等于目标就行。  
  - 没有考虑到同一条三元组可能同时满足多个坐标，需要同时检查三个维度。  
- **下次类似题目第一步**：先**筛选合法元素**（不超过/不低于目标），再**检查每个维度的覆盖情况**，看能否通过“贪心”或“组合”得到目标。