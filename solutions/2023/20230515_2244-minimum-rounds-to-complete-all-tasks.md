# #2244. **完成所有任务的最少轮数** / Minimum Rounds to Complete All Tasks

> 难度：中等 · 标签：Array、Hash Table、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-rounds-to-complete-all-tasks/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array tasks, where tasks[i] represents the difficulty level of a task. In each round, you can complete either 2 or 3 tasks of the same difficulty level.
Return the minimum rounds required to complete all the tasks, or -1 if it is not possible to complete all the tasks.
Note: This question is the same as 2870: Minimum Number of Operations to Make Array Empty.

**Examples**

**Example 1:**

```
Input: tasks = [2,2,3,3,2,4,4,4,4,4]
Output: 4
Explanation: To complete all the tasks, a possible plan is:
- In the first round, you complete 3 tasks of difficulty level 2. 
- In the second round, you complete 2 tasks of difficulty level 3. 
- In the third round, you complete 3 tasks of difficulty level 4. 
- In the fourth round, you complete 2 tasks of difficulty level 4.  
It can be shown that all the tasks cannot be completed in fewer than 4 rounds, so the answer is 4.
```

**Example 2:**

```
Input: tasks = [2,3,3]
Output: -1
Explanation: There is only 1 task of difficulty level 2, but in each round, you can only complete either 2 or 3 tasks of the same difficulty level. Hence, you cannot complete all the tasks, and the answer is -1.
```

**Constraints**

- 1 <= tasks.length <= 105
- 1 <= tasks[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `tasks`，其中 `tasks[i]` 表示第 `i` 项任务的难度等级。每一轮，你只能完成 **2 或 3** 个难度相同的任务。返回完成所有任务所需的最少轮数，如果无法完成所有任务则返回 **-1**。

**示例 1**  
**输入**: `tasks = [2,2,3,3,2,4,4,4,4,4]`  
**输出**: `4`  
**解释**: 完成所有任务的一种可行方案如下：  
- 第 1 轮，完成 3 个难度为 2 的任务。  
- 第 2 轮，完成 2 个难度为 3 的任务。  
- 第 3 轮，完成 3 个难度为 4 的任务。  
- 第 4 轮，完成 2 个难度为 4 的任务。  
可以证明不存在使用更少轮数完成所有任务的方案。

**示例 2**  
**输入**: `tasks = [2,3,3]`  
**输出**: `-1`  
**解释**: 只有 1 个难度为 2 的任务，而每轮只能完成 2 或 3 个同一难度的任务。因此无法完成所有任务，答案为 `-1`。

**约束条件**  
- `1 <= tasks.length <= 10^5`  
- `1 <= tasks[i] <= 10^9`

**提示**: 本题与 2870 题 “Minimum Number of Operations to Make Array Empty” 完全相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接、最笨的想法是：**把所有任务逐个挑出来，尝试每一种可能的分组方式**，看哪一种能把所有任务全部完成且使用的回合最少。  
实现上可以这样想：

1. 先统计每一种难度出现了多少次（相当于把任务“分类”），这一步可以用**哈希表**（dictionary）来完成。哈希表就像一本“查字典”，键（key）是难度值，值（value）是该难度出现的次数。
2. 对每一种难度，枚举所有可能的「2 任务一组」和「3 任务一组」的组合。比如出现 `7` 次，就要遍历 `x`（2 任务的组数）从 `0` 到 `7//2`，看是否存在 `y`（3 任务的组数）使得 `2*x + 3*y = 7`，并记录 `x+y`（回合数）的最小值。
3. 把所有难度的最小回合数相加，就是答案；如果某一种难度根本找不到合法的 `x、y`，直接返回 `-1`。

> **为什么这个方法正确？**  
> 因为我们把「每一轮只能完成 2 或 3 个相同难度的任务」的约束全部写进了等式 `2*x + 3*y = cnt`（`cnt` 为该难度的任务数），遍历所有满足等式的 `(x, y)` 必然能找到最少的 `x+y`，也就是最少回合数。

> **时间/空间复杂度大白话**  
> - 对每一种不同的难度，我们都要尝试所有可能的 `x`（最多 `cnt/2` 次）。如果任务数很多（比如 `cnt = 10⁵`），这个循环会非常慢，几乎是「把所有可能的组合都算一遍」——这就是 **暴力**。  
> - 用大 O 记号表示，这种做法的时间复杂度大约是 `O( Σ cnt_i / 2 ) ≈ O(n²)`（最坏情况下所有任务都是同一种难度，`cnt = n`，循环次数是 `n/2`，再乘以 `n` 种可能的 `cnt`，得到二次方量级）。  
> - 空间上我们只需要保存哈希表，最多保存 `n` 个不同的难度，空间复杂度是 `O(n)`。

#### 代码（Python）

```python
from collections import Counter
from math import inf
from typing import List

def minimumRounds_bruteforce(tasks: List[int]) -> int:
    # 1. 统计每个难度出现了多少次
    freq = Counter(tasks)               # 哈希表：难度 → 次数

    total_rounds = 0                     # 最终答案

    # 2. 对每一种难度，枚举所有可能的 2‑组 和 3‑组
    for diff, cnt in freq.items():
        best = inf                       # 用一个很大的数表示“目前还没有合法方案”

        # x 表示使用多少个「2 个任务」的回合，最多 cnt//2 次
        for x in range(cnt // 2 + 1):
            # 剩下的任务必须能被 3 整除
            remain = cnt - 2 * x
            if remain % 3 == 0:          # 找到合法的 y
                y = remain // 3
                best = min(best, x + y) # 记录最少回合数

        if best == inf:                  # 该难度根本无法完成
            return -1
        total_rounds += best

    return total_rounds
```

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况下，所有任务同一种难度，需要遍历约 `n/2` 次的循环，整体是二次方量级）。  
  大白话：如果任务有 10⁵ 个，程序会跑上 **上亿次**的循环，显然会超时。
- **空间复杂度**：`O(n)`，只用了一个哈希表来保存每种难度的计数。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道，**关键在于每一种难度的任务数 `cnt`**，只要找出最少的回合数即可。  
暴力解慢的原因是 **枚举所有可能的 2‑组数**，其实我们可以用数学观察直接算出最优方案，根本不需要遍历。

**观察 1：**  
`cnt` 只可能被 `2` 或 `3` 整除才能完成全部任务。  
- 当 `cnt % 2 == 0` 时，全部用「2 个」的回合就能完成，回合数是 `cnt / 2`。  
- 当 `cnt % 3 == 0` 时，全部用「3 个」的回合就能完成，回合数是 `cnt / 3`。

**观察 2：**  
如果 `cnt` 既不能被 2 整除，也不能被 3 整除，仍然有可能通过混合「2」和「3」来凑齐。  
实际上，**只要 `cnt >= 2` 且 `cnt != 1`**，必定可以用若干个 3 再加上若干个 2 完成。  
原因是：
- 用尽可能多的「3」可以最大程度减少回合数，因为每回合完成的任务更多。
- 只要剩余的任务数是 1（比如 `cnt = 4` → 3 + 1），我们就把一组「3」改成两组「2」：`3+1 → 2+2`。这样仍然合法且回合数只会增加 **1**。

**由此得到最优策略：**  
1. 先把 `cnt` 用 `3` 整除，得到 `cnt // 3` 个「3」的回合。  
2. 看剩余 `r = cnt % 3`：  
   - `r == 0` → 正好全部用 3，回合数 = `cnt // 3`。  
   - `r == 1` → 需要把一组「3」换成两组「2」：回合数 = `cnt // 3 - 1 + 2`（即 `cnt // 3 + 1`）。等价于 `cnt // 3 + 1`。  
   - `r == 2` → 再加一组「2」即可，回合数 = `cnt // 3 + 1`。  

**特殊情况**：如果 `cnt == 1`，根本无法完成，直接返回 `-1`。

**整体算法**：

1. 用哈希表统计每种难度的出现次数（同暴力解的第一步）。  
2. 对每一种难度的计数 `cnt`，按照上面的公式直接算出最少回合数；若 `cnt == 1` 则返回 `-1`。  
3. 把所有难度的回合数相加，即得到答案。

**为什么是最优？**  
- 采用「尽可能多的 3」是贪心的核心，因为 3 能一次完成更多任务，回合数自然更少。  
- 唯一需要「退让」的情况是余数为 1 时，这时把一组 3 替换成两组 2 是唯一的可行且最少回合的办法（不能再把 1 拆成更小的合法组合）。  
- 这套规则对所有 `cnt ≥ 2` 都成立，因而整体最优。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def minimumRounds(tasks: List[int]) -> int:
    """
    返回完成所有任务的最少回合数，若不可能则返回 -1。
    思路：先统计每种难度的出现次数，再对每个计数使用贪心公式。
    """
    freq = Counter(tasks)          # 哈希表：难度 → 次数
    total = 0                      # 最终答案

    for diff, cnt in freq.items():
        if cnt == 1:                # 只能单独出现一次，根本无法组成 2 或 3
            return -1

        # 使用最多的 3，余数决定是否需要额外的 2
        rounds = cnt // 3           # 先算可以完整使用多少个「3」的回合
        remainder = cnt % 3

        if remainder == 0:
            # 余数为 0，全部用 3 即可
            total += rounds
        elif remainder == 1:
            # 余数为 1，需要把一组 3 换成两组 2
            # 这里保证 cnt >= 4（因为 cnt != 1），所以 rounds >= 1
            total += rounds - 1 + 2   # = rounds + 1
        else:  # remainder == 2
            # 直接再加一组 2
            total += rounds + 1

    return total
```

#### 复杂度

- **时间复杂度**：`O(n)`。  
  - 只遍历一次数组统计次数 `O(n)`，随后对每种不同的难度（至多 `n` 种）做 **常数时间** 的计算。  
  - 大白话：不管有多少任务，只要遍历一次就搞定，十万条数据也只会跑十万次循环，极快。

- **空间复杂度**：`O(k)`，`k` 为不同难度的种类数，最坏情况下 `k = n`（所有任务难度都不相同），仍然是线性空间。  
  - 实际上只存放计数，远比暴力解的额外循环空间要小。

---

## 心得

- **核心技巧**：**贪心 + 计数**（把相同难度的任务先聚合，用尽可能多的 “3” 来最小化回合数）。
- **适用的题型**  
  1. 需要把元素分成固定大小的组（如「每组 2/3」）并求最少组数的题目。  
  2. “把数组清空” 或 “把所有相同元素消除” 类的贪心计数题。  
  3. 类似的还有「将数组分割成若干子数组，每个子数组长度为 2 或 3」的变形。
- **一句话总结解题钥匙**：**先统计，再用「尽可能多的 3」的贪心规则处理余数**。

---

## 反思

- **第一反应**：看到“每回合只能完成 2 或 3 个相同难度的任务”，自然想到先把相同难度的任务聚在一起，然后尝试各种组合——这就是暴力枚举的思路。
- **最容易踩的坑**  
  1. 忽略了 `cnt == 1` 的特殊情况，会导致错误的正数答案。  
  2. 对余数为 1 时没有进行 “把一组 3 换成两组 2” 的处理，导致错误的回合数。  
  3. 在实现时忘记检查 `cnt // 3 - 1` 是否会出现负数（当 `cnt = 2` 时不会进入该分支）。
- **下次类似题的第一步**：**先做频数统计**，把同类元素聚合；随后**思考每个聚合后的计数如何最少拆分**（通常是找最大可用的组大小，再处理余数）。这样可以迅速从暴力转向贪心或数学公式，避免枚举爆炸。