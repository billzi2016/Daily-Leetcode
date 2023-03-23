# #2178. **正偶数的最大拆分** / Maximum Split of Positive Even Integers

> 难度：中等 · 标签：Math、Backtracking、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-split-of-positive-even-integers/)

---

## 题目（英文原版）

**Description**

You are given an integer finalSum. Split it into a sum of a maximum number of unique positive even integers.
Return a list of integers that represent a valid split containing a maximum number of integers. If no valid split exists for finalSum, return an empty list. You may return the integers in any order.

**Examples**

**Example 1:**

```
Input: finalSum = 12
Output: [2,4,6]
Explanation: The following are valid splits: (12), (2 + 10), (2 + 4 + 6), and (4 + 8).
(2 + 4 + 6) has the maximum number of integers, which is 3. Thus, we return [2,4,6].
Note that [2,6,4], [6,2,4], etc. are also accepted.
```

**Example 2:**

```
Input: finalSum = 7
Output: []
Explanation: There are no valid splits for the given finalSum.
Thus, we return an empty array.
```

**Example 3:**

```
Input: finalSum = 28
Output: [6,8,2,12]
Explanation: The following are valid splits: (2 + 26), (6 + 8 + 2 + 12), and (4 + 24). 
(6 + 8 + 2 + 12) has the maximum number of integers, which is 4. Thus, we return [6,8,2,12].
Note that [10,2,4,12], [6,2,4,16], etc. are also accepted.
```

**Constraints**

- 1 <= finalSum <= 1010

---

## 题目（中文翻译）

给定一个整数 `finalSum`，将其拆分为若干个**唯一的正偶整数**（unique positive even integers）的和，使得拆分得到的整数个数尽可能多。  
返回一个整数数组，表示一种包含最大数量整数的合法拆分方案。若不存在合法拆分，则返回空数组。数组中整数的顺序不限。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件**  
- `1 <= finalSum <= 10^10`

---

### 示例

**示例 1**  
```
Input: finalSum = 12
Output: [2,4,6]
```
**解释:** 合法的拆分方式有 `(12)`, `(2 + 10)`, `(2 + 4 + 6)`, `(4 + 8)`。  
其中 `(2 + 4 + 6)` 包含的整数个数最多，为 3，所以返回 `[2,4,6]`。  
`[2,6,4]`, `[6,2,4]` 等顺序不同的数组同样被接受。

**示例 2**  
```
Input: finalSum = 7
Output: []
```
**解释:** 对于给定的 `finalSum` 没有合法的拆分方式，故返回空数组。

**示例 3**  
```
Input: finalSum = 28
Output: [6,8,2,12]
```
**解释:** 合法的拆分方式有 `(2 + 26)`, `(6 + 8 + 2 + 12)`, `(4 + 24)`。  
其中 `(6 + 8 + 2 + 12)` 包含的整数个数最多，为 4，所以返回 `[6,8,2,12]`。  
`[10,2,4,12]`, `[6,2,4,16]` 等顺序不同的数组同样被接受。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的偶数**（2, 4, 6, …）枚举出来，然后尝试 **每一种子集**，看它们的和是否恰好等于 `finalSum`，并且记录下子集大小最大的那一个。

- **数据结构**：  
  - `list` 用来存放候选的偶数，就像我们把一堆不同面值的硬币排成一列。  
  - `set`（或 `list`）用来保存当前尝试的子集，就像我们从硬币堆里挑出几枚放进口袋。

- **为什么正确**：  
  只要把所有偶数都遍历一遍，并且检查所有子集，就一定能找到满足条件的最大子集（如果存在的话），因为没有任何组合会被漏掉。

- **时间/空间复杂度**：  
  - 枚举所有子集的时间是指数级的，记作 **O(2^m)**（这里的 `m` 是候选偶数的个数）。  
    - 用大白话说，就是如果候选偶数有 10 个，就要检查 2^10 = 1024 种组合；如果有 20 个，就要检查 2^20 ≈ 100 万种组合，明显不可接受。  
  - 空间上需要保存候选偶数列表和递归栈，最多 **O(m)**。

> **结论**：暴力搜索可以帮助我们理清问题，但在实际运行时会因为指数级的时间开销而超时。

#### 代码（Python）

```python
def maximum_split_bruteforce(finalSum: int):
    # 1. 只能分割成偶数，若 finalSum 本身是奇数直接返回空列表
    if finalSum % 2 == 1:
        return []

    # 2. 生成所有可能的偶数（2, 4, 6, ...）直至不超过 finalSum
    candidates = [i for i in range(2, finalSum + 1, 2)]

    best = []                     # 用来保存找到的最大合法拆分

    # 3. 深度优先搜索所有子集
    def dfs(idx: int, cur_sum: int, cur_list: list):
        nonlocal best
        # 已经凑到目标和，更新答案
        if cur_sum == finalSum:
            if len(cur_list) > len(best):
                best = cur_list[:]
            return
        # 超过目标和或遍历完所有候选数，直接返回
        if cur_sum > finalSum or idx == len(candidates):
            return

        # 选择当前偶数
        dfs(idx + 1, cur_sum + candidates[idx], cur_list + [candidates[idx]])
        # 不选当前偶数
        dfs(idx + 1, cur_sum, cur_list)

    dfs(0, 0, [])
    return best
```

#### 复杂度

- **时间复杂度**：`O(2^m)`，其中 `m = finalSum // 2`（候选偶数的个数）。指数级增长，实际会超时。  
- **空间复杂度**：`O(m)`，主要是递归栈和保存候选偶数的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **枚举所有子集是不可行的**，因为组合数太多。我们需要找到 **规律**，让每一步的选择都尽可能 “贪心”——即在保证最终可以凑出 `finalSum` 的前提下，**尽量多使用小的偶数**。这样可以让拆分的数量达到最大。

**关键观察**：

1. **只能使用偶数**，所以如果 `finalSum` 是奇数，直接返回空列表。  
2. 为了让元素个数最多，我们应该让每个元素尽量 **小**，因为小的数可以放得更多。  
3. 按照从小到大的顺序依次取偶数 `2, 4, 6, …`，累计求和 `s`。  
   - 当 `s + next_even` **仍然小于** `finalSum` 时，说明我们可以安全地把 `next_even` 加入答案。  
   - 当再加下一个偶数会 **超过** `finalSum` 时，说明已经没有足够的 “余量” 再放一个新的、不同的偶数了。  
4. 此时我们把 **剩余的差值**（`finalSum - s`）加到最后一个已经选好的偶数上。  
   - 由于 `finalSum - s` 本身一定是偶数（因为 `finalSum` 与 `s` 都是偶数），并且它大于等于已经选的最后一个偶数，所以 **不会与已有的偶数重复**，仍然满足“唯一”的要求。

**步骤**：

- 初始化 `ans = []`，`cur = 2`（当前准备加入的最小偶数），`remaining = finalSum`。  
- **循环**：只要 `remaining - cur > cur`（即把 `cur` 加进去后，剩余的数仍然大于下一个可能的偶数），就把 `cur` 加入 `ans`，`remaining -= cur`，`cur += 2`。  
- 循环结束后，把 `remaining`（剩下的唯一一个数）加入 `ans`。  

这样得到的 `ans` 中的数既 **唯一**、**全是偶数**，且 **个数最多**。

> **类比**：想象你有一袋糖果，总重量是 `finalSum` 克。你只能一次拿走 **2 克、4 克、6 克…** 的糖块，且每种重量只能拿一次。为了让袋子里糖块的数量最多，你会先把最小的 2 克、4 克、6 克… 依次装进去，等到装不下更大的糖块时，把剩下的糖全部装进最后一个已经装好的糖块里（把它“升级”），这样糖块的数量就最多了。

#### 代码（Python）

```python
from typing import List

def maximumSplit(finalSum: int) -> List[int]:
    """
    贪心实现：尽可能多地使用最小的偶数，
    最后把剩余的差值加到最后一个元素上。
    """
    # 1. 奇数无法拆成偶数和，直接返回空列表
    if finalSum % 2 == 1:
        return []

    ans = []          # 用来保存最终的拆分结果
    cur = 2           # 当前准备加入的最小偶数
    remaining = finalSum

    # 2. 循环加入尽可能小的偶数
    #    条件：加入 cur 后，剩余的数仍然大于下一个偶数（cur+2），
    #    这样可以保证后面还能再加入一个不同的偶数
    while remaining - cur > cur:
        ans.append(cur)
        remaining -= cur
        cur += 2       # 下一次尝试更大的偶数

    # 3. 循环结束后，remaining 本身就是最后一个数
    #    它一定是偶数，且不会与前面的数重复
    ans.append(remaining)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k` 是答案列表的长度，约等于 `sqrt(finalSum)`。因为每次循环至少把当前最小偶数 `cur` 加到答案中，而 `cur` 按 `2,4,6,…` 递增，直到累计和接近 `finalSum`。用大白话说，就是**随着 `finalSum` 增大，循环次数只会增长到大约 √finalSum**，远远小于指数级。  
- **空间复杂度**：`O(k)`，需要保存答案列表本身，同样是最多 √finalSum 个整数。

---

## 心得

- **核心技巧**：**贪心 + 最小递增偶数**——先用最小的偶数填充，最后把剩余的差值合并到最后一个元素上，保证唯一性且元素个数最多。  
- **适用的题型**：  
  1. “把整数拆成若干唯一的**正数/偶数**，使数量最大”——如本题。  
  2. “把整数拆成若干唯一的**正整数**使数量最大”（类似 LeetCode 1849 - Splitting a String Into the Max Number of Unique Substrings）。  
  3. “在满足某种约束的情况下，使用最小的资源集合”——比如装箱、分配任务等贪心场景。  
- **一句话总结**：**“先把最小的合法单位装满，再把剩余全部合并到最后一个”。**

---

## 反思

- **第一反应**：看到“唯一的正偶数”以及“最大数量”，立刻想到“从小到大依次取”，因为小的东西能放得更多。  
- **最容易踩的坑**：  
  - 忘记判断 `finalSum` 是否为奇数，导致返回了非法的拆分。  
  - 循环条件写错（比如写成 `remaining - cur >= 0`），会导致最后两个数相同，从而违背“唯一”要求。  
  - 没考虑到 **剩余的差值** 必须是偶数并且大于等于当前的 `cur`，否则会产生重复。  
- **下次遇到同类题**，第一步应该问自己：“**能否先把最小的合法单位一次加入，直到再加入会导致冲突？**”，如果答案是“可以”，那么就可以尝试上述贪心策略。