# #3040. 相同分数的最大操作次数 II / Maximum Number of Operations With the Same Score II

> 难度：中等 · 标签：Array、Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-operations-with-the-same-score-ii/)

---

## 题目（英文原版）

**Description**

Given an array of integers called nums, you can perform any of the following operation while nums contains at least 2 elements:
The score of the operation is the sum of the deleted elements.
Your task is to find the maximum number of operations that can be performed, such that all operations have the same score.
Return the maximum number of operations possible that satisfy the condition mentioned above.

**Examples**

**Example 1:**

```
Input: nums = [3,2,1,2,3,4]
Output: 3
Explanation: We perform the following operations:
- Delete the first two elements, with score 3 + 2 = 5, nums = [1,2,3,4].
- Delete the first and the last elements, with score 1 + 4 = 5, nums = [2,3].
- Delete the first and the last elements, with score 2 + 3 = 5, nums = [].
We are unable to perform any more operations as nums is empty.
```

**Example 2:**

```
Input: nums = [3,2,6,1,4]
Output: 2
Explanation: We perform the following operations:
- Delete the first two elements, with score 3 + 2 = 5, nums = [6,1,4].
- Delete the last two elements, with score 1 + 4 = 5, nums = [6].
It can be proven that we can perform at most 2 operations.
```

**Constraints**

- 2 <= nums.length <= 2000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组（array）`nums`，只要 `nums` 中至少还有 2 个元素，就可以执行以下任意一种操作：

- 删除 `nums` 中的任意两个元素，记为 `a` 和 `b`。  
- 本次操作的分数（score）为被删除元素之和 `a + b`。

你的任务是找出能够执行的最大操作次数，使得所有操作的分数都相同。返回满足上述条件的最大操作次数。

**示例 1**  
```
输入: nums = [3,2,1,2,3,4]
输出: 3
解释:
我们可以按如下顺序进行操作：
- 删除前两个元素，分数为 3 + 2 = 5，剩余 nums = [1,2,3,4]。
- 删除首尾两个元素，分数为 1 + 4 = 5，剩余 nums = [2,3]。
- 删除首尾两个元素，分数为 2 + 3 = 5，剩余 nums = []。
此时数组已空，无法再进行操作。
```

**示例 2**  
```
输入: nums = [3,2,6,1,4]
输出: 2
解释:
我们可以按如下顺序进行操作：
- 删除前两个元素，分数为 3 + 2 = 5，剩余 nums = [6,1,4]。
- 删除最后两个元素，分数为 1 + 4 = 5，剩余 nums = [6]。
可以证明最多只能进行 2 次操作。
```

**约束条件**  

- `2 <= nums.length <= 2000`  
- `1 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的操作顺序**，看能否得到一组分数相同的操作并统计其个数。

- 先随便挑选数组中的任意两个元素删掉，得到第一步的分数 `S`。  
- 接下来把剩下的元素继续两两配对，只要配对的两个数之和仍然是 `S` 就可以继续，否则这条路径就死掉了。  
- 把所有可能的配对顺序都遍历一遍，记录能够完成的最大操作次数。

这里用到的唯一数据结构是 **递归的调用栈**（想象成一层层的“选择-回溯”），相当于我们在玩一个“找配对”的游戏，每一步都要在当前剩余的数组里挑两个数。

> **为什么能得到正确答案？**  
> 因为我们把 **所有** 合法的配对顺序都枚举了，只要有一种方式能完成 `k` 次操作，递归一定会走到这条路径并更新答案。

> **时间/空间复杂度**  
> - 每一次配对都会把数组长度减 2，最坏情况下我们要尝试 `n/2` 步。  
> - 在第 `i` 步时，有 `C(len,2)` 种可能的两数选择，整体相当于 **指数级** 的搜索树。  
> - 用大白话说，时间复杂度大约是 `O( (n!!) )`（超级大），在 `n=2000` 时根本跑不完。  
> - 空间上只需要保存递归的调用栈，最深 `n/2` 层，`O(n)`。

#### 代码（Python）

```python
from typing import List

def max_ops_bruteforce(nums: List[int]) -> int:
    """
    暴力递归实现，仅用于说明思路。
    对于 n>20 已经不可用，仅作教学示例。
    """
    n = len(nums)
    if n < 2:
        return 0

    best = 0

    # 递归尝试所有配对
    def dfs(arr: List[int], cur_score: int, cnt: int):
        nonlocal best
        # 没有剩余元素或只剩一个，结束当前路径
        if len(arr) < 2:
            best = max(best, cnt)
            return

        # 如果已经确定了分数，则只能配对和为 cur_score 的两个数
        if cur_score != -1:
            # 逐个寻找合法配对
            for i in range(len(arr)):
                for j in range(i + 1, len(arr)):
                    if arr[i] + arr[j] == cur_score:
                        nxt = arr[:i] + arr[i+1:j] + arr[j+1:]   # 删除 i、j
                        dfs(nxt, cur_score, cnt + 1)
            # 没有合法配对，结束
            best = max(best, cnt)
            return

        # 第一次配对：随便挑两个数，确定分数
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                score = arr[i] + arr[j]
                nxt = arr[:i] + arr[i+1:j] + arr[j+1:]
                dfs(nxt, score, cnt + 1)

    dfs(nums, -1, 0)
    return best
```

> **关键行中文注释**  
> - `cur_score == -1` 表示还没有确定统一的分数。  
> - `arr[:i] + arr[i+1:j] + arr[j+1:]` 就像把数组里第 `i`、`j` 两本书取走，剩下的书重新排成一排。  

#### 复杂度

- **时间复杂度**：`O( (n!!) )`（指数级），实际运行会在 `n≈20` 时就爆炸。  
- **空间复杂度**：`O(n)`，递归栈的最大深度为 `n/2`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于我们把每一步的所有配对都枚举了**。实际上，题目只要求“**所有操作的分数相同**”，这意味着：

1. **第一次配对决定了统一的分数 `S`**。  
2. 之后我们只需要在原序列里找尽可能多的 **不相交的配对**，每对的和必须等于 `S`。  

> 换句话说：给定 `S`，问题等价于“在保持原来顺序的前提下，最多能挑出多少对 `(i, j)`（`i<j`），使得 `nums[i] + nums[j] = S`，且每个位置至多被使用一次”。  

这正是 **最长不相交配对子序列** 的经典 DP 形式。

---

#### 2.1 先把所有可能的分数 `S` 列出来  

- `nums[i]` 的取值范围是 `[1, 1000]`，所以两数之和 `S` 的取值范围是 `[2, 2000]`。  
- 实际上只需要遍历 **出现过的和**，但即使遍历全部 `2…2000`，也只有 1999 种，数量极小。

---

#### 2.2 对固定的 `S` 求最大配对数  

设 `dp[i]` 为 **考虑前 `i`（0‑based）个元素，最多能完成的配对次数**。  

转移方式：

- **不把第 `i` 个元素配对** → `dp[i] = dp[i-1]`  
- **把第 `i` 个元素配对** → 必须找一个更早的下标 `j`（`j < i`），满足 `nums[j] + nums[i] = S`。  
  此时我们可以在 `j` 之前再配对 `dp[j-1]` 次，然后再加上这一次配对，得到 `dp[j-1] + 1`。  
  为了让这一步 O(1) 完成，我们维护一个哈希表 `best[val]`，记录 **截至当前下标前，值为 `val` 的位置 `j` 能得到的最大 `dp[j-1]`**。

具体步骤（对每个 `S`）：

```
best = defaultdict(lambda: -inf)   # key: 数值，value: 在该数出现前的最大 dp
dp_prev = 0                         # dp[i-1]，滚动更新，省掉整个 dp 数组
for i, x in enumerate(nums):
    # 先尝试把 x 当作右端点配对
    complement = S - x
    cand = best[complement] + 1 if best[complement] != -inf else -inf
    dp_cur = max(dp_prev, cand)    # 两种选择取最大

    # 更新 best，使得 x 以后可以作为左端点参与配对
    # 注意这里使用的是 dp_prev（即不包括当前元素的配对数）
    best[x] = max(best[x], dp_prev)

    dp_prev = dp_cur                # 为下一个 i 做准备
```

循环结束后，`dp_prev` 即为在整个数组上、分数为 `S` 时能完成的最大操作次数。

**为什么正确？**  
- `best[x]` 保存的是 “在位置 `i` 之前，若把值为 `x` 的元素当左端点配对，能得到的最大配对数”。这样在看到 `complement` 时，就能立刻得到 “把当前元素配对后，整体最多多少次”。  
- 由于我们始终只使用 **之前的 `dp` 值**，配对之间不会出现交叉，保证了“不相交”。  
- 每次只遍历一次数组，时间是线性的。

---

#### 2.3 综合所有可能的 `S`

对每一个可能的分数 `S`（最多 1999 种）执行上面的线性 DP，取最大值即为答案。

整体复杂度：

- 外层遍历 `S`：`O(M)`，`M ≤ 1999`（实际更少）。  
- 内层对数组一次扫描：`O(n)`。  
- 总计 `O(M·n) ≤ 4·10⁶`，在 2000 规模的数据下毫秒级完成。  
- 额外空间只需要哈希表 `best`（大小 ≤ 1000）和若干整数，`O(1)` 相对 `n`。

---

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def maxOperations(nums: List[int]) -> int:
    """
    最优解：遍历所有可能的统一分数 S，使用 O(n) 的线性 DP 求最大不相交配对数。
    时间复杂度：O(M * n)，M 为可能的分数种类（≤ 1999）
    空间复杂度：O(1)（不计输入数组本身）
    """
    n = len(nums)
    if n < 2:
        return 0

    # 统计所有出现过的和，减少不必要的遍历
    possible_sums = set()
    for i in range(n):
        for j in range(i + 1, n):
            possible_sums.add(nums[i] + nums[j])

    ans = 0

    # 对每一个可能的统一分数 S，跑一次线性 DP
    for S in possible_sums:
        # best[val] = max dp[j-1]  (j 为值为 val 的位置，且 j 在当前 i 左侧)
        best = defaultdict(lambda: -10**9)   # 用很小的数表示“不存在”
        dp_prev = 0                           # dp[i-1]

        for x in nums:
            complement = S - x
            # 若 complement 之前出现过，就可以尝试配对
            cand = best[complement] + 1 if best[complement] > -10**9 else -10**9

            # 选 “不配对当前元素” 或 “配对当前元素” 中的较大值
            dp_cur = dp_prev if dp_prev > cand else cand

            # 更新 best，使得当前元素以后可以作为左端点配对
            # 注意这里使用的是 dp_prev（配对不包括当前元素）
            if dp_prev > best[x]:
                best[x] = dp_prev

            dp_prev = dp_cur   # 为下一个元素准备

        if dp_prev > ans:
            ans = dp_prev

    return ans
```

> **关键行中文注释**  
> - `possible_sums` 就像把所有可能的“配对得分”先列出来，避免后面白跑。  
> - `best` 相当于“字典本子”，记录每个数字在左边出现时，已经配对好的最大次数。  
> - `cand = best[complement] + 1` 表示“把当前数字 `x` 和左边某个 `complement` 配对后，总次数”。  
> - `dp_prev` / `dp_cur` 只用两个变量滚动更新，省掉了 `O(n)` 的数组空间。  

---

#### 复杂度

- **时间复杂度**：`O(M·n)`，其中 `M` 为可能的统一分数种类（`≤ 1999`），`n ≤ 2000`。  
  用大白话说，就是最多 **四百万次**简单的整数运算，跑得飞快。  
- **空间复杂度**：`O(1)`（不计输入数组本身），只用了一个大小不超过 1000 的哈希表和若干整型变量。

---

## 心得

- **核心技巧**：把“所有操作分数相同”转化为“固定一个目标和 `S`，在原序列中找最多的不相交配对”。  
- **适用场景**：  
  1. “相同分数的配对”类问题，如 *Maximum Number of Operations With the Same Score I*（只能从两端取）。  
  2. “在序列中找最多的不相交子序列/子对”——比如 “最长上升子序列的非交叉配对” 或 “相同和的子数组配对”。  
- **一句话总结解题钥匙**：**先固定目标和，再用一次线性 DP（哈希表 + 前缀最优）求最大不交配对**。

---

## 反思

- **第一反应**：看到“所有操作的得分相同”，立刻想到“先选第一步的得分，然后所有后续操作都必须匹配”。  
- **最容易踩的坑**：  
  - 忽略了“配对必须不交叉”。若只统计出现次数会得到错误答案。  
  - 在 DP 中忘记使用 `dp[j-1]`（而是用了 `dp[j]`），导致同一个元素被重复计入两次配对。  
  - 边界情况：数组长度为奇数时最后会剩下一个元素，必须保证 DP 正确返回已配对的次数。  
- **下次思路**：遇到“相同属性的多次操作”时，先 **固定属性值**（这里是和 `S`），再把问题转化为 **在序列上找最大不冲突的子结构**，往往可以用 **前缀 DP + 哈希映射** 的线性技巧化解。