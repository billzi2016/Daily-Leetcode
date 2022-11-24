# #2025. 划分数组的最大方式数 / Maximum Number of Ways to Partition an Array

> 难度：困难 · 标签：Array、Hash Table、Counting、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-ways-to-partition-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n. The number of ways to partition nums is the number of pivot indices that satisfy both conditions:
You are also given an integer k. You can choose to change the value of one element of nums to k, or to leave the array unchanged.
Return the maximum possible number of ways to partition nums to satisfy both conditions after changing at most one element.

**Examples**

**Example 1:**

```
Input: nums = [2,-1,2], k = 3
Output: 1
Explanation: One optimal approach is to change nums[0] to k. The array becomes [3,-1,2].
There is one way to partition the array:
- For pivot = 2, we have the partition [3,-1 | 2]: 3 + -1 == 2.
```

**Example 2:**

```
Input: nums = [0,0,0], k = 1
Output: 2
Explanation: The optimal approach is to leave the array unchanged.
There are two ways to partition the array:
- For pivot = 1, we have the partition [0 | 0,0]: 0 == 0 + 0.
- For pivot = 2, we have the partition [0,0 | 0]: 0 + 0 == 0.
```

**Example 3:**

```
Input: nums = [22,4,-25,-20,-15,15,-16,7,19,-10,0,-13,-14], k = -33
Output: 4
Explanation: One optimal approach is to change nums[2] to k. The array becomes [22,4,-33,-20,-15,15,-16,7,19,-10,0,-13,-14].
There are four ways to partition the array.
```

**Constraints**

- n == nums.length
- 2 <= n <= 105
- -105 <= k, nums[i] <= 105

---

## 题目（中文翻译）

给定一个长度为 `n` 的 **0 索引整数数组**（0-indexed integer array）`nums`。  
**划分数组的方式数**定义为满足以下两个条件的枢轴索引（pivot index）的个数：

1. 枢轴索引 `i` 必须满足 `0 < i < n`（即左右两侧均非空）。  
2. 左侧子数组 `nums[0 .. i-1]` 的元素和等于右侧子数组 `nums[i .. n-1]` 的元素和。

此外，还给定一个整数 `k`。你可以选择将 `nums` 中**至多**一个元素的值改为 `k`，也可以保持数组不变。  
求在最多更改一个元素后，`nums` 能拥有的**最大**划分方式数，并返回该最大值。

---

### 示例

#### 示例 1
``` 
Input: nums = [2,-1,2], k = 3
Output: 1
```
**解释**：一种最优做法是把 `nums[0]` 改为 `k`，数组变为 `[3,-1,2]`。此时只有一种划分方式：
- 枢轴 `i = 2`，划分为 `[3,-1 | 2]`，左侧和 `3 + (-1) = 2` 等于右侧和 `2`。

#### 示例 2
``` 
Input: nums = [0,0,0], k = 1
Output: 2
```
**解释**：最优做法是保持数组不变。共有两种划分方式：
- 枢轴 `i = 1`，划分为 `[0 | 0,0]`，左侧和 `0` 等于右侧和 `0 + 0`。  
- 枢轴 `i = 2`，划分为 `[0,0 | 0]`，左侧和 `0 + 0` 等于右侧和 `0`。

#### 示例 3
``` 
Input: nums = [22,4,-25,-20,-15,15,-16,7,19,-10,0,-13,-14], k = -33
Output: 4
```
**解释**：一种最优做法是把 `nums[2]` 改为 `k`，数组变为 `[22,4,-33,-20,-15,15,-16,7,19,-10,0,-13,-14]`。此时共有四种划分方式。

---

### 约束条件

- `n == nums.length`
- `2 <= n <= 10^5`
- `-10^5 <= k, nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「把一个元素改成 `k`」和「找满足划分条件的 pivot」这两件事都枚举一遍：

1. **枚举要改的下标** `i`（`i = -1` 代表不改任何元素）。  
2. 把 `nums[i]`（如果 `i != -1`）改成 `k`，得到新数组 `arr`。  
3. **枚举所有可能的 pivot** `p`（`1 ≤ p ≤ n‑1`），计算左侧和 `sum(arr[0 … p‑1])` 与右侧和 `sum(arr[p … n‑1])`，看它们是否相等。  
4. 把所有满足条件的 `p` 计数，取最大的那个计数即为答案。

> **生活化类比**：  
> 把数组想成一排装有糖果的盒子，pivot 就是把盒子从某个位置切开，左边盒子里糖果的总重量要和右边盒子里糖果的总重量相同。暴力解相当于把每一种「把哪颗糖果换成新口味」的可能性都尝一遍，然后再把每一种「从哪儿切」的可能性都尝一遍。

这种做法一定能得到正确答案，因为它把所有合法的「改动 + 切点」都遍历到了。只是不够高效。

#### 代码（Python）

```python
from typing import List

def maxWays_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = 0                       # 记录最大划分方式数

    # i == -1 表示不改任何元素，其余 i 表示把 nums[i] 改成 k
    for i in range(-1, n):
        # 复制一份数组，避免在循环中修改原数组
        arr = nums[:]              
        if i != -1:                 # 进行一次改动
            arr[i] = k

        # 枚举所有可能的 pivot（左、右两边都必须非空）
        cnt = 0
        for p in range(1, n):      # p 为切分点的下标
            left_sum = sum(arr[:p])          # 左侧和
            right_sum = sum(arr[p:])         # 右侧和
            if left_sum == right_sum:
                cnt += 1
        best = max(best, cnt)      # 取最大值

    return best
```

> 关键行中文注释已写在代码里，直接复制即可运行。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 次（每个可能的改动），内层遍历 `n‑1` 次（每个可能的 pivot），每次还要 `O(n)` 去求左/右和（这里用了 `sum`），最坏情况下是 `n × n × n`，但因为 `sum` 可以在前缀和的帮助下降到 `O(1)`，所以我们把主要的遍历层数算作 `n²`。用大白话说，就是「如果数组有 10 000 个元素，程序大概要跑 100 000 000 次」——对 10⁵ 规模的输入会超时。

- **空间复杂度**：`O(1)`（不计输入数组本身的空间）  
  - 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **两层枚举**：  
1. 对每个可能的改动 `i`，我们都要重新遍历所有 pivot。  
2. 对每个 pivot，我们都要重新计算左、右和。

我们需要把这些重复的工作 **合并**，利用前缀和与哈希表，让每一次遍历只做 `O(1)` 的查询。

---

#### 2.1 关键观察

1. **不改动时的条件**  
   设原数组总和为 `S`，下标 `p` 的左侧前缀和记为 `pref[p] = sum(nums[0 … p‑1])`（`p` 从 `1` 到 `n‑1`）。  
   划分成立当且仅当  

   ```
   pref[p] == S - pref[p]   ⇔   2 * pref[p] == S   ⇔   pref[p] == S / 2
   ```

   也就是说，**pivot 只和前缀和的数值有关**，不需要遍历左右两段。

2. **改动一个元素的影响**  
   设我们把下标 `i` 的元素改成 `k`，改动量为  

   ```
   delta = k - nums[i]
   ```

   - **总和** 变成 `S' = S + delta`。  
   - **前缀和**：若 pivot `p` 位于 `i` 的右侧（`i < p`），左侧会多加 `delta`；若在左侧或恰好在 `i`（`i ≥ p`），左侧保持不变。

   对于某个固定 `i`，pivot `p` 的新条件：

   - **i < p（pivot 在改动右侧）**  
     ```
     pref[p] + delta == (S + delta) - (pref[p] + delta)
     ⇔ 2 * (pref[p] + delta) == S + delta
     ⇔ 2 * pref[p] == S - delta
     ⇔ pref[p] == (S - delta) / 2
     ```
   - **i ≥ p（pivot 在改动左侧或正好在 i）**  
     ```
     pref[p] == (S + delta) / 2
     ```

   关键是：**只需要知道有多少个前缀和等于某个特定值**，而不必逐个检查。

3. **把所有前缀和统计进哈希表**  
   - `cntAll[value]`：所有 `p`（`1 … n‑1`）的前缀和等于 `value` 的次数。  
   - 在遍历 `i` 时，我们把 pivot 分成两组：
     - **左组**：`p ≤ i`（左侧），对应的前缀和计数保存在 `cntLeft`。  
     - **右组**：`p > i`（右侧），对应的前缀和计数保存在 `cntRight`（初始等于 `cntAll`，随后逐步把当前 `p = i+1` 从右组移到左组）。

   这样，对于每个 `i`，我们只需要 O(1) 时间去查询：

   ```
   answer_i = cntRight[(S - delta) / 2]   (如果 (S - delta) 为偶数)
            + cntLeft[(S + delta) / 2]    (如果 (S + delta) 为偶数)
   ```

   再取所有 `i`（包括不改动的情况）的最大值即为答案。

---

#### 2.2 算法步骤

1. 计算原数组的前缀和列表 `pref[1 … n‑1]` 与总和 `S`。  
2. 用 `Counter`（哈希表）统计所有前缀和出现的次数，得到 `cntRight`。`cntLeft` 初始化为空。  
3. **不改动的基线答案**：如果 `S` 为偶数，则 `cntAll[S/2]` 即为不改动时的划分数。  
4. 从左到右遍历每个下标 `i`（`0 … n‑1`）：
   - `delta = k - nums[i]`。  
   - 计算目标值  
     ```
     targetRight = (S - delta) / 2   (仅在 S - delta 为偶数时有效)
     targetLeft  = (S + delta) / 2   (仅在 S + delta 为偶数时有效)
     ```
   - 用哈希表查询对应计数并相加得到 `cur`。  
   - 更新全局最大答案 `ans = max(ans, cur)`。  
   - **移动 pivot**：把 `p = i+1`（对应的前缀和 `pref[i]`）从 `cntRight` 移到 `cntLeft`，为下一次迭代做好准备。  
5. 返回 `ans`。

> **类比**：把所有可能的切点想成装在两只口袋里的球，左口袋是已经走过的切点，右口袋是还没走到的切点。每次我们站在某个元素 `i`，只需要看看左口袋里有没有“价值等于 targetLeft”的球，右口袋里有没有“价值等于 targetRight”的球，计数即可。

---

#### 代码（Python）

```python
from collections import Counter
from typing import List

def maxWays(nums: List[int], k: int) -> int:
    n = len(nums)
    # ---------- 1. 前缀和 ----------
    pref = []               # pref[p] = sum(nums[0:p]) , p 从 1 到 n-1
    cur = 0
    for i in range(n - 1):  # 只需要前 n-1 个前缀，因为 pivot 不能在最右端
        cur += nums[i]
        pref.append(cur)

    total = sum(nums)       # 原数组总和 S

    # ---------- 2. 统计所有前缀和 ----------
    cnt_right = Counter(pref)   # 初始所有 pivot 都在右侧
    cnt_left = Counter()        # 左侧暂时为空

    # ---------- 3. 不改动时的答案 ----------
    ans = 0
    if total % 2 == 0:
        ans = cnt_right.get(total // 2, 0)

    # ---------- 4. 枚举要改的下标 ----------
    for i in range(n):
        delta = k - nums[i]          # 改动量

        # 目标值必须是整数，才能在哈希表里查到
        cur_cnt = 0

        # i < p 的情况：pivot 在右侧
        if (total - delta) % 2 == 0:
            target = (total - delta) // 2
            cur_cnt += cnt_right.get(target, 0)

        # i >= p 的情况：pivot 在左侧
        if (total + delta) % 2 == 0:
            target = (total + delta) // 2
            cur_cnt += cnt_left.get(target, 0)

        ans = max(ans, cur_cnt)

        # ---------- 5. 把当前的 pivot 移到左侧 ----------
        # 当前元素 i 结束后，pivot = i+1 将不再属于右侧
        if i < n - 1:                     # 最后一个元素后面已经没有 pivot
            val = pref[i]                 # 对应的前缀和
            cnt_right[val] -= 1
            if cnt_right[val] == 0:
                del cnt_right[val]        # 删除避免计数为 0 的键
            cnt_left[val] += 1

    return ans
```

**代码要点注释（已在代码中）**：

- `pref` 只保存到 `n-2` 索引，因为第 `n` 个前缀（整个数组）没有对应的 pivot。  
- `cnt_right` 与 `cnt_left` 分别维护「右侧」和「左侧」的前缀和出现次数。  
- 对每个 `i`，只要检查 `(total ± delta)` 是否为偶数，就能确定目标前缀和是否可能出现。  
- 更新哈希表时把当前的 `pref[i]` 从右侧搬到左侧，保证后面的 `i` 使用的左右划分是正确的。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 前缀和、计数表的构建各一次遍历 `O(n)`。  
  - 主循环遍历每个元素 `i`，每次只做常数次哈希查询与更新。  
  - 与暴力的 `O(n²)` 相比，提升了一个量级。可以轻松应付 `n ≤ 10⁵` 的约束。

- **空间复杂度**：`O(n)`  
  - 存放前缀和列表与两个计数表（最坏情况下每个前缀和都不相同）。  
  - 只比输入数组多用了线性额外空间，符合题目限制。

---

## 心得

- **核心技巧**：利用**前缀和 + 哈希计数**把「左/右和相等」的判定转化为「前缀和等于某个固定值」的查询。再配合一次遍历把「改动在左侧」与「改动在右侧」的情况分别统计，完成 `O(n)` 解法。  
- **适用场景**：  
  1. 需要在「改动一次」后重新满足「前缀和 = 某值」的题目（如 LeetCode 1665、2100 系列）。  
  2. 任何「划分数组」或「找平衡点」的题目，只要可以用 `2 * prefix = total` 表示，都可以尝试这种「前缀哈希」思路。  
- **一句话总结**：**把所有可能的划分点的前缀和放进哈希表，用前缀和的“等于目标值”来一次性统计改动前后能得到的划分数**。

---

## 反思

- **第一反应**：看到「可以改动一个元素」立刻想到「枚举改动位置」+「枚举划分点」的双层循环——这就是暴力解。  
- **最容易踩的坑**：  
  1. **偶数/奇数判断**：`pref == total/2` 只有在 `total` 为偶数时才有意义，忘记检查会导致浮点数或错误的哈希查询。  
  2. **边界 pivot**：pivot 不能在数组最左或最右端，必须是 `1 … n‑1`。  
  3. **计数表的同步**：在遍历 `i` 时必须把对应的 `pref[i]` 从右侧搬到左侧，否则左侧/右侧的划分会错位。  
- **下次思路**：遇到「改动一次」且「条件可以用前缀和表达」的题目时，先写出 **不改动的等式**，再分析改动对 **总和** 与 **局部前缀** 的线性影响，最后用 **哈希计数 + 单次遍历** 把所有可能合并。这样常能把 `O(n²)` 降到 `O(n)`。