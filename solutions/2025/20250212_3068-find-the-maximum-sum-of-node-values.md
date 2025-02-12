# #3068. 求节点值的最大和 / Find the Maximum Sum of Node Values

> 难度：困难 · 标签：Array、Dynamic Programming、Greedy、Bit Manipulation、Tree、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-sum-of-node-values/)

---

## 题目（英文原版）

**Description**

There exists an undirected tree with n nodes numbered 0 to n - 1. You are given a 0-indexed 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the tree. You are also given a positive integer k, and a 0-indexed array of non-negative integers nums of length n, where nums[i] represents the value of the node numbered i.
Alice wants the sum of values of tree nodes to be maximum, for which Alice can perform the following operation any number of times (including zero) on the tree:
Return the maximum possible sum of the values Alice can achieve by performing the operation any number of times.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1], k = 3, edges = [[0,1],[0,2]]
Output: 6
Explanation: Alice can achieve the maximum sum of 6 using a single operation:
- Choose the edge [0,2]. nums[0] and nums[2] become: 1 XOR 3 = 2, and the array nums becomes: [1,2,1] -> [2,2,2].
The total sum of values is 2 + 2 + 2 = 6.
It can be shown that 6 is the maximum achievable sum of values.
```

**Example 2:**

```
Input: nums = [2,3], k = 7, edges = [[0,1]]
Output: 9
Explanation: Alice can achieve the maximum sum of 9 using a single operation:
- Choose the edge [0,1]. nums[0] becomes: 2 XOR 7 = 5 and nums[1] become: 3 XOR 7 = 4, and the array nums becomes: [2,3] -> [5,4].
The total sum of values is 5 + 4 = 9.
It can be shown that 9 is the maximum achievable sum of values.
```

**Example 3:**

```
Input: nums = [7,7,7,7,7,7], k = 3, edges = [[0,1],[0,2],[0,3],[0,4],[0,5]]
Output: 42
Explanation: The maximum achievable sum is 42 which can be achieved by Alice performing no operations.
```

**Constraints**

- 2 <= n == nums.length <= 2 * 104
- 1 <= k <= 109
- 0 <= nums[i] <= 109
- edges.length == n - 1
- edges[i].length == 2
- 0 <= edges[i][0], edges[i][1] <= n - 1
- The input is generated such that edges represent a valid tree.

---

## 题目（中文翻译）

存在一棵无向树，包含 n 个节点，编号为 0 到 n‑1。给定一个长度为 n‑1 的二维整数数组 edges（0‑索引），其中 `edges[i] = [ui, vi]` 表示节点 ui 与节点 vi 之间有一条边。还给定一个正整数 k 以及长度为 n 的非负整数数组 nums（0‑索引），其中 `nums[i]` 表示编号为 i 的节点的值。

Alice 可以对树执行以下操作任意次数（包括零次）：

- 选择一条边 `[u, v]`，对该边的两个端点的值同时执行异或（XOR）操作：  
  `nums[u] = nums[u] XOR k`，`nums[v] = nums[v] XOR k`。

Alice 希望使所有节点值的总和最大化。返回 Alice 通过执行上述操作任意次数后能够得到的最大可能总和。

---

### 示例

**示例 1**

```
Input: nums = [1,2,1], k = 3, edges = [[0,1],[0,2]]
Output: 6
Explanation: Alice 只需执行一次操作即可得到最大和：
- 选择边 [0,2]。此时 `nums[0]` 与 `nums[2]` 变为：`1 XOR 3 = 2`，数组 `nums` 由 `[1,2,1]` 变为 `[2,2,2]`。
总和为 2 + 2 + 2 = 6，且可以证明 6 已是能够达到的最大和。
```

**示例 2**

```
Input: nums = [2,3], k = 7, edges = [[0,1]]
Output: 9
Explanation: Alice 只需执行一次操作即可得到最大和：
- 选择边 [0,1]。此时 `nums[0]` 变为 `2 XOR 7 = 5`，`nums[1]` 变为 `3 XOR 7 = 4`，数组 `nums` 由 `[2,3]` 变为 `[5,4]`。
总和为 5 + 4 = 9，且可以证明 9 已是能够达到的最大和。
```

**示例 3**

```
Input: nums = [7,7,7,7,7,7], k = 3, edges = [[0,1],[0,2],[0,3],[0,4],[0,5]]
Output: 42
Explanation: 最大和为 42，Alice 通过不执行任何操作即可得到该结果。
```

---

### 约束条件

- 2 ≤ n = `nums.length` ≤ 2 × 10⁴  
- 1 ≤ k ≤ 10⁹  
- 0 ≤ `nums[i]` ≤ 10⁹  
- `edges.length` = n - 1  
- `edges[i].length` = 2  
- 0 ≤ `edges[i][0]`, `edges[i][1]` ≤ n - 1  
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每一条边** 当成“开关”。  
- 选中这条边，就把它两端的节点的值都做一次 `xor k`（相当于把原来的数字换成 `nums[i] ^ k`）。  
- 不选这条边，两个端点保持不变。  

于是我们只需要遍历 **所有可能的选边集合**，算出每种情况下所有节点最终的值，再取最大和。  

> **类比**：把树看成一串灯泡，边是控制灯泡开关的按钮。我们要尝试所有按钮的开/关组合，找出亮度（节点值）最高的情况。

> **正确性**：因为题目允许任意次数地对任意边执行操作，枚举所有选边集合就覆盖了所有可能的最终状态。  

> **为什么慢**：树有 `n‑1` 条边，选/不选各有两种可能，组合数是 `2^(n‑1)`，随着 `n` 增大呈指数增长，根本不可接受。  

#### 代码（Python）  

```python
from itertools import product
from collections import defaultdict

def max_sum_bruteforce(nums, k, edges):
    n = len(nums)
    best = sum(nums)                     # 不选任何边的情况
    # 把边编号，方便遍历所有 0/1 组合
    m = len(edges)

    for mask in product([0, 1], repeat=m):   # 0 表示不选，1 表示选
        cur = nums[:]                         # 复制一份
        for bit, (u, v) in zip(mask, edges):
            if bit:                            # 选中这条边
                cur[u] ^= k
                cur[v] ^= k
        best = max(best, sum(cur))

    return best
```

> **关键行注释**  
> - `product([0, 1], repeat=m)`：生成所有 `2^(n‑1)` 种选边方式。  
> - `cur[u] ^= k`：对选中的边的两个端点执行一次 `xor k`。  

#### 复杂度  

- **时间复杂度**：`O(2^{n})`（指数级）——因为要枚举每条边的两种状态。  
  大白话：如果树有 20 条边，可能的组合就有 `2^20 ≈ 1,048,576` 种；如果是 30 条边，就会超过十亿，根本跑不完。  
- **空间复杂度**：`O(n)`——保存一份当前节点值的数组。  

> 暴力解只能用来验证思路或在极小的样例上跑通，正式解题必须寻找 **多项式**（线性）算法。  

---  

### 2. 最优解  

#### 思路  

观察操作的本质：  
- 每条边被选中一次会让 **两个** 端点的值都 `xor k`。  
- 同一条边如果被选两次，`xor k` 两次会抵消，恢复原值。  

因此 **每个节点最终是否被 `xor k` 只取决于它 incident（相邻）被选中的边的奇偶性**：  

| 选中相邻边的次数 | 最终值                     |
|----------------|---------------------------|
| 偶数           | `nums[i]`（不变）         |
| 奇数           | `nums[i] ^ k`（翻转一次） |

把“选中相邻边的次数的奇偶性”记作 **parity[i] ∈ {0,1}**。  
我们要在满足 **所有 parity 的和是偶数**（因为每条边贡献 2 次奇数，整个树的奇数节点数必须是偶数） 的前提下，使  

\[
\text{total} = \sum_i \bigl[\, parity[i]==0 ? nums[i] : (nums[i]\,\mathbf{xor}\,k) \,\bigr]
\]

最大。

---

#### 关键一步：把每个节点的“翻转收益”抽出来  

对节点 `i` 定义  

\[
\Delta_i = (nums[i] \mathbf{xor} k) - nums[i]
\]

- `Δ_i > 0`：把这个节点翻转一次会让总和 **增加** `Δ_i`。  
- `Δ_i ≤ 0`：翻转会让总和 **不增**，甚至下降。  

如果没有奇偶约束，我们显然会把所有 `Δ_i > 0` 的节点都翻转。  
唯一的约束是 **翻转的节点数必须是偶数**（因为奇数个翻转节点无法由边的配对产生）。

于是问题简化为：

> 在所有正收益的节点集合 `P = { i | Δ_i > 0 }` 中，挑选一个子集，使其大小为 **偶数**，且 `Δ` 的和最大。

- **如果 |P| 本身是偶数** → 直接全部翻转，得到最大和。  
- **如果 |P| 是奇数** → 必须舍弃（或“补”）一个节点，使总数变为偶数。  
  - 舍弃一个正收益节点的代价是失去最小的正 `Δ`（即最小的 `Δ_i`）。  
  - 或者把一个负收益节点也翻转，使奇偶性恢复（这会让总和下降 `|Δ_j|`，其中 `Δ_j ≤ 0`），我们取两者中 **损失最小** 的方案。

这一步只需要一次遍历即可得到：

1. `pos_sum` = sum of all positive `Δ_i`  
2. `min_pos` = smallest positive `Δ_i` (如果有)  
3. `max_neg` = largest (即最接近 0) 非正 `Δ_i` (如果有)  

若 `|P|` 为奇数，答案 = `base_sum + pos_sum - min(min_pos, -max_neg)`。  
其中 `base_sum = sum(nums)` 是不做任何翻转的总和。

> **为什么在树上一定可行**  
> 给定任意满足偶数个奇节点的集合，树中总可以找到一组边，使得恰好这些节点的 incident 选边次数为奇数（把这些节点两两配对，沿唯一路径选边，路径上的每条边会被计入两端的奇偶）。因此只要满足奇偶约束，就一定能实现对应的翻转方案。

---

#### 代码（Python）  

```python
def max_sum_optimal(nums, k, edges):
    """
    树的结构在本解法里其实不需要显式使用，只要知道它是一棵连通无环图，
    因为只要翻转节点数为偶数，就一定可以通过若干条边实现。
    """
    n = len(nums)
    base_sum = sum(nums)                     # 全部不翻转时的和

    # 计算每个节点翻转后的增益 Δ_i
    deltas = [(num ^ k) - num for num in nums]

    pos_sum = 0          # 所有正 Δ 的总和
    cnt_pos = 0          # 正 Δ 的个数
    min_pos = float('inf')   # 最小的正 Δ
    max_neg = -float('inf')   # 最大的非正 Δ（即最接近 0 的负数或 0）

    for d in deltas:
        if d > 0:
            pos_sum += d
            cnt_pos += 1
            if d < min_pos:
                min_pos = d
        else:
            if d > max_neg:          # d ≤ 0
                max_neg = d

    # 若正收益节点数为偶数，直接全部翻转
    if cnt_pos % 2 == 0:
        return base_sum + pos_sum

    # 正收益节点数为奇数，需要“补齐”一次奇偶
    # 两种补齐方式：舍弃最小的正收益，或者额外翻转一个负收益（损失 -max_neg）
    # 取损失最小的那种
    loss_if_drop_pos = min_pos                     # 舍弃一个正收益的损失
    loss_if_add_neg = -max_neg if max_neg != -float('inf') else float('inf')
    min_loss = min(loss_if_drop_pos, loss_if_add_neg)

    return base_sum + pos_sum - min_loss
```

> **关键行中文注释**  
> - `deltas = [(num ^ k) - num for num in nums]`：计算每个节点翻转一次后相对原来的增益。  
> - `if cnt_pos % 2 == 0:`：奇偶性检查，偶数直接使用全部正增益。  
> - `loss_if_add_neg = -max_neg`：把一个负增益节点也翻转，实际会让总和 **减少** `|max_neg|`。  
> - `return base_sum + pos_sum - min_loss`：在必须牺牲的情况下，选取最小的损失。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次 `nums`（`n ≤ 2·10⁴`），不需要递归或 DP。  
  - 大白话：即使有两万节点，也只需要几万次简单的算术运算，几乎是瞬间完成。  

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只用了若干个整型变量来保存累计和、最小/最大值。  

> 与暴力解相比，时间从指数级降到了线性，几乎可以在所有合法输入下毫秒通过。  

---  

## 心得  

- **核心技巧**：  
  1. **奇偶约束**——每条边同时影响两个端点，导致“翻转的节点数必须为偶数”。  
  2. **增益拆分**——把每个节点的翻转收益 `Δ_i` 单独算出来，问题转化为在满足偶数个正收益的前提下取最大和。  
  3. **贪心/数学化**——当正收益节点数为奇数时，只需要比较“舍弃最小正收益”和“补进最大负收益”两种选择，取更小的损失即可。  

- **适用的题型**（类似思路）：  
  1. “在图/树上选若干条边，使得某些节点状态翻转”，如 **LeetCode 1625. Lexicographically Smallest String After Applying Operations**（同样利用奇偶配对）。  
  2. “在数组上任选若干次相同操作，每次改变两个元素”，如 **Maximum Sum After Two Operations**（利用配对奇偶）。  
  3. “把每个元素翻转或不翻转，但总翻转次数受限制”，如 **Maximum XOR Sum of Subset**（需要考虑奇偶或模 2 的约束）。  

- **一句话总结解题钥匙**：  
  > “把每个节点的翻转收益抽出来，利用‘翻转节点数必须为偶数’的全局奇偶约束，只在正收益奇数时做一次最小代价的补偿”。  

---  

## 反思  

- **拿到题目第一反应**：  
  “这是一棵树，操作是对相邻两个节点同时做 `xor k`，我先想到用树形 DP，记录子树在父边选或不选时的最优值”。  

- **最容易踩的坑**  
  1. **忘记奇偶约束**：直接把所有 `Δ_i > 0` 的节点翻转，结果在正数个时会得到非法状态（无法通过边的配对实现）。  
  2. **误以为需要完整的 DP**：其实只要把增益拆分就能得到 O(n) 的贪心解，写出复杂的 DP 会浪费时间且容易出错。  
  3. **边界情况**：  
     - `k = 0` 时 `nums[i] ^ k == nums[i]`，所有 `Δ_i = 0`，答案就是原始和。  
     - 所有 `Δ_i ≤ 0`，此时 `cnt_pos = 0`（偶数），直接返回原始和。  
     - 只有一个正收益且没有负收益可补偿时，需要 **舍弃** 这个正收益。  

- **下次遇到同类题的第一步**：  
  **先把每个元素的“单独操作收益”算出来，观察全局约束（如奇偶、模数、总次数上限），再决定是 DP、贪心还是配对/匹配**。  

这样一步步抽象、化简，就能把看似复杂的树上操作问题转化为一次线性遍历即可求解的简单模型。祝学习愉快！