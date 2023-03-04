# #2151. 最大可能的好人数量（基于陈述） / Maximum Good People Based on Statements

> 难度：困难 · 标签：Array、Backtracking、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-good-people-based-on-statements/)

---

## 题目（英文原版）

**Description**

There are two types of persons:
You are given a 0-indexed 2D integer array statements of size n x n that represents the statements made by n people about each other. More specifically, statements[i][j] could be one of the following:
Additionally, no person ever makes a statement about themselves. Formally, we have that statements[i][i] = 2 for all 0 <= i < n.
Return the maximum number of people who can be good based on the statements made by the n people.

**Examples**

**Example 1:**

```
Input: statements = [[2,1,2],[1,2,2],[2,0,2]]
Output: 2
Explanation: Each person makes a single statement.
- Person 0 states that person 1 is good.
- Person 1 states that person 0 is good.
- Person 2 states that person 1 is bad.
Let's take person 2 as the key.
- Assuming that person 2 is a good person:
    - Based on the statement made by person 2, person 1 is a bad person.
    - Now we know for sure that person 1 is bad and person 2 is good.
    - Based on the statement made by person 1, and since person 1 is bad, they could be:
        - telling the truth. There will be a contradiction in this case and this assumption is invalid.
        - lying. In this case, person 0 is also a bad person and lied in their statement.
    - Following that person 2 is a good person, there will be only one good person in the group.
- Assuming that person 2 is a bad person:
    - Based on the statement made by person 2, and since person 2 is bad, they could be:
        - telling the truth. Following this scenario, person 0 and 1 are both bad as explained before.
            - Following that person 2 is bad but told the truth, there will be no good persons in the group.
        - lying. In this case person 1 is a good person.
            - Since person 1 is a good person, person 0 is also a good person.
            - Following that person 2 is bad and lied, there will be two good persons in the group.
We can see that at most 2 persons are good in the best case, so we return 2.
Note that there is more than one way to arrive at this conclusion.
```

**Example 2:**

```
Input: statements = [[2,0],[0,2]]
Output: 1
Explanation: Each person makes a single statement.
- Person 0 states that person 1 is bad.
- Person 1 states that person 0 is bad.
Let's take person 0 as the key.
- Assuming that person 0 is a good person:
    - Based on the statement made by person 0, person 1 is a bad person and was lying.
    - Following that person 0 is a good person, there will be only one good person in the group.
- Assuming that person 0 is a bad person:
    - Based on the statement made by person 0, and since person 0 is bad, they could be:
        - telling the truth. Following this scenario, person 0 and 1 are both bad.
            - Following that person 0 is bad but told the truth, there will be no good persons in the group.
        - lying. In this case person 1 is a good person.
            - Following that person 0 is bad and lied, there will be only one good person in the group.
We can see that at most, one person is good in the best case, so we return 1.
Note that there is more than one way to arrive at this conclusion.
```

**Constraints**

- n == statements.length == statements[i].length
- 2 <= n <= 15
- statements[i][j] is either 0, 1, or 2.
- statements[i][i] == 2

---

## 题目（中文翻译）

**题目描述**

有两类人：好人（good person）和坏人（bad person）。  
好人总是说实话，坏人可以说真话也可以说假话。

给定一个下标从 0 开始的 `n × n` 二维整数数组（2D integer array）`statements`，它记录了 `n` 个人相互之间的陈述（statement）。具体而言，`statements[i][j]` 可能取以下三种值：

- `0` 表示第 `i` 个人说第 `j` 个人是坏人；
- `1` 表示第 `i` 个人说第 `j` 个人是好人；
- `2` 表示第 `i` 个人没有对第 `j` 个人作出陈述。

此外，任何人都不会对自己作出陈述，即对所有 `0 ≤ i < n` 都有 `statements[i][i] = 2`。

请根据所有人的陈述，返回可能的最大好人数。

---

**示例 1**

```
输入: statements = [[2,1,2],[1,2,2],[2,0,2]]
输出: 2
解释:
每个人只作出了一条陈述。
- 人 0 说人 1 是好人。
- 人 1 说人 0 是好人。
- 人 2 说人 1 是坏人。

我们以人 2 为基准进行假设。
- 假设人 2 是好人:
    - 根据人 2 的陈述，人 1 是坏人。
    - 于是人 1 的所有陈述都不可信。
    - 人 1 说人 0 是好人，但因为人 1 是坏人，这条陈述可以是谎言，也可以是实话；此时不影响人 0 的状态。
    - 人 0 说人 1 是好人，但已知人 1 是坏人，所以人 0 必须是坏人（因为好人不可能说错）。
    - 综上，只有人 2 为好人，人数为 1。

- 假设人 2 是坏人:
    - 人 2 的陈述可以真假不定，此时不对其他人产生约束。
    - 只要满足人 0 与人 1 之间的相互陈述即可。
    - 若设人 0 为好人，则人 1 必须是好人（因为人 0 说人 1 是好人）。
    - 此时人 1 说人 0 是好人，与人 0 为好人不冲突。
    - 因此可以得到 2 个好人（人 0 与人 1），这已经是最大可能。

所以答案为 `2`。
```

**示例 2**

```
输入: statements = [[2,0],[0,2]]
输出: 1
解释:
每个人只作出了一条陈述。
- 人 0 说人 1 是坏人。
- 人 1 说人 0 是坏人。

以人 0 为基准进行假设。
- 假设人 0 是好人:
    - 根据人 0 的陈述，人 1 是坏人。
    - 那么人 1 的陈述（“人 0 是坏人”）可以是谎言，也可以是实话，但不影响已知的好人数量。
    - 此时只有人 0 为好人，人数为 1。

- 假设人 0 是坏人:
    - 人 0 的陈述可以真假不定，此时人 1 的状态不受限制。
    - 若再设人 1 为好人，则根据人 1 的陈述，人 0 必须是坏人，这与假设不冲突。
    - 于是可以得到 1 个好人（人 1），同样为 1。

因此最大好人数为 `1`。
```

---

**约束条件**

- `n == statements.length == statements[i].length`
- `2 ≤ n ≤ 15`
- `statements[i][j]` 只可能是 `0`, `1` 或 `2`
- `statements[i][i] == 2`（所有人对自己都没有陈述）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把每个人「好」或「坏」的状态全部列举出来，逐一验证哪些组合与所有人的陈述相容，最后取相容组合中「好」的人数最多的那个。  

- **用到的数据结构**  
  - **位掩码（bitmask）**：把 `n` 个人的好坏状态压在一个整数的二进制位里。第 `i` 位为 `1` 表示第 `i` 个人是「好」；为 `0` 表示「坏」。这就像把「是否通过」这件事记在一本 0/1 记录本上，翻开一本就能一次看到所有人的状态。  
  - **二维数组 `statements`**：原题给出的「每个人对每个人的声明」矩阵。`statements[i][j] = 1` 代表「i 说 j 是好」，`0` 代表「i 说 j 是坏」，`2` 代表「i 没说（或者说自己）」。可以把它想象成「每个人的证词表」。

- **为什么正确**  
  - 所有可能的好坏分配只有 `2ⁿ` 种（因为每个人只有两种可能）。只要遍历这 `2ⁿ` 种情况，并且对每一种情况检查「若某人是好的人，他的话必须全部成立」这条规则，就一定能找出所有合法的分配。合法分配中好人的数量的最大值就是答案。

- **复杂度分析（大白话）**  
  - **时间**：我们要检查 `2ⁿ` 种状态。对每一种状态，最多要看 `n × n` 条陈述（因为要检查每个人对每个人的说法）。所以总体是 `O(2ⁿ · n²)`。  
    - `2ⁿ`：如果 `n=15`，就是 32768 种，数量不大，电脑可以在毫秒级遍历完。  
    - `n²`：比如 `n=15`，最多 225 条陈述，算得很快。  
  - **空间**：只需要保存原始矩阵 `statements`（`n²`）和一个整数的位掩码（常数空间），所以是 `O(n²)`，其实可以写成 `O(1)`（不计输入）。

#### 代码（Python）

```python
from typing import List

class Solution:
    def maximumGood(self, statements: List[List[int]]) -> int:
        n = len(statements)               # 人数
        ans = 0                            # 最佳的好人数量

        # 用 0 ~ (1<<n)-1 表示所有可能的好坏分配
        for mask in range(1 << n):        # 枚举每一种位掩码
            ok = True                     # 用来标记当前 mask 是否自洽
            # 检查每个人 i 是否为好人
            for i in range(n):
                if not (mask >> i) & 1:   # 第 i 位是 0，说明 i 是坏人，无需验证他的陈述
                    continue
                # i 是好人，需要验证他所有的陈述
                for j in range(n):
                    if statements[i][j] == 2:   # i 没对 j 说话，跳过
                        continue
                    # i 说 j 是好 (1) 还是坏 (0)
                    expected = statements[i][j]
                    actual = (mask >> j) & 1    # mask 中第 j 位的实际好坏
                    if expected != actual:      # 矛盾！此 mask 不合法
                        ok = False
                        break
                if not ok:               # 提前退出内层循环
                    break

            if ok:                       # 该 mask 合法，统计好人数量
                good_cnt = bin(mask).count('1')
                ans = max(ans, good_cnt)

        return ans
```

> **关键行中文注释**  
> - `for mask in range(1 << n)`: 用 `1 << n` 表示 `2ⁿ`，遍历所有可能的好坏组合。  
> - `if not (mask >> i) & 1`: 右移 `i` 位后与 `1` 与操作，判断第 `i` 位是否为 `1`（好人）。  
> - `expected != actual`: 如果好人的陈述与实际状态不一致，就说明该组合不可能成立。

#### 复杂度

- **时间复杂度**：`O(2ⁿ · n²)`  
  - `2ⁿ` 表示所有可能的好坏分配数量，`n²` 表示每次验证需要遍历的陈述条数。  
  - 对于本题的上限 `n ≤ 15`，最多约 `3.3 万 × 225 ≈ 7.5 百万` 次基本操作，完全在毫秒级可接受。

- **空间复杂度**：`O(1)`（不计输入矩阵）  
  - 只使用了常数个额外变量和一个整数的位掩码。

---

### 2. 最优解

#### 思路  

暴力解已经能在题目限制下跑完，但我们仍可以在枚举的过程中 **提前剪枝**，避免无意义的完整遍历，从而把常数因子降到更低。思路如下：

1. **从左到右逐人决定好坏**（回溯 / 深度优先搜索）。  
2. 当决定某个人为「好」时，立刻检查他已经说出的所有陈述是否与当前已确定的状态冲突。  
   - 如果冲突，说明这条分支不可能产生合法解，直接回溯，省去后面所有的检查。  
3. 当决定某个人为「坏」时，他的话可以不管，因为坏人的话不需要满足任何条件。  
4. 记录当前已经确定为「好」的人数，上限 `n`，在搜索结束后更新答案。  

这相当于在 **位掩码枚举** 的基础上加了 **冲突提前检测**，在最坏情况下仍是 `O(2ⁿ·n²)`，但平均会快很多，尤其当陈述之间矛盾较多时，很多不合法的分支会提前被剪掉。

核心概念——**回溯**（Backtracking）  
- 想象我们在给每个人贴「好」或「坏」的标签，先给第 0 个人贴上，检查是否与之前的标签冲突，若冲突就撤销（回溯）并尝试另一种颜色。这个过程像在画图时不断尝试不同的颜色，碰到冲突就换颜色。

#### 代码（Python）

```python
from typing import List

class Solution:
    def maximumGood(self, statements: List[List[int]]) -> int:
        n = len(statements)
        self.ans = 0                 # 全局最大好人数
        # status[i] = -1 未决定, 0 坏, 1 好
        status = [-1] * n

        def dfs(idx: int, good_cnt: int) -> None:
            """尝试决定第 idx 个人的身份"""
            if idx == n:                         # 所有人都已决定
                self.ans = max(self.ans, good_cnt)
                return

            # 方案 1：把 idx 当成坏人（不需要检查他的陈述）
            status[idx] = 0
            dfs(idx + 1, good_cnt)               # 好人数不变
            status[idx] = -1                     # 恢复现场

            # 方案 2：把 idx 当成好人，先检查冲突
            conflict = False
            for j in range(n):
                if statements[idx][j] == 2:      # 没说
                    continue
                expected = statements[idx][j]    # 0 或 1
                if status[j] == -1:               # j 还未决定，暂时不冲突
                    continue
                if status[j] != expected:         # 已决定的 j 与陈述不符
                    conflict = True
                    break
            if conflict:
                return                            # 这条分支直接剪枝

            # 若没有冲突，则可以把 idx 设为好人并继续搜索
            # 同时把 idx 所说的「确定的」陈述同步到 status 中，以便后续检查
            saved = []                           # 记录因 idx 的陈述而被临时确定的人的原状态
            for j in range(n):
                if statements[idx][j] in (0, 1) and status[j] == -1:
                    saved.append((j, status[j]))
                    status[j] = statements[idx][j]   # 根据 idx 的话确定 j 的好坏

            status[idx] = 1
            dfs(idx + 1, good_cnt + 1)

            # 回溯：恢复被 idx 强制决定的那些人的状态
            for j, old in saved:
                status[j] = old
            status[idx] = -1

        dfs(0, 0)
        return self.ans
```

> **代码要点中文解释**  
> - `status` 用 `-1/0/1` 分别表示「未决定」「坏」「好」。  
> - 在把第 `idx` 个人设为好人时，先遍历他所有的陈述，若出现已经决定的 `j` 与陈述不符，就立刻 `return`，这一步就是**提前剪枝**。  
> - 对于尚未决定的 `j`，我们可以利用「好人说的话一定可信」的特性，直接把 `j` 的状态固定为陈述的值，这样后面的递归就能少检查一次。为避免影响其他分支，使用 `saved` 列表在回溯时恢复原状。  
> - 递归结束后（`idx == n`）更新全局最大好人数 `self.ans`。

#### 复杂度

- **时间复杂度**：最坏情况仍是 `O(2ⁿ · n²)`，因为我们可能仍需遍历所有子集。但实际运行时由于**冲突提前剪枝**，大多数不合法的分支会在较浅的递归层就被终止，常数因子大幅下降。  
  - 与纯位掩码枚举相比，这里可以把「检查」的次数从每个子集 `n²` 次降到 **只在好人出现时检查**，平均会更快。

- **空间复杂度**：`O(n)`  
  - 递归栈深度最多 `n`，以及 `status`、`saved` 等线性数组。  

---

## 心得

- **核心技巧**：**枚举 + 位掩码**（或回溯）结合「好人说的话必须成立」的约束。  
- **适用的题型**  
  1. 所有状态只有两种（0/1）且人数 ≤ 15 ~ 20 时，需要检查所有可能的组合（如「Maximum Compatibility Score」）。  
  2. 需要在「若某人可信，其言论必须自洽」的前提下求最优解的题目（如「Maximum Good People」系列、或「Friend Circle」的变体）。  
- **一句话总结解题钥匙**：**把每个人的好坏视作二进制位，用位掩码遍历所有可能，然后只保留「所有好人的陈述都不冲突」的方案**。

---

## 反思

- **第一反应**：看到「好人」与「坏人」的二元关系，以及 `n ≤ 15`，立刻想到「枚举所有 2ⁿ 种状态」——这在竞赛中是最常用的突破口。  
- **最容易踩的坑**  
  1. **忽视 `statements[i][i] = 2`**：自己对自己的陈述永远是「无意义」的，需要在代码里跳过，否则会误判冲突。  
  2. **位运算写错**：`(mask >> i) & 1` 与 `mask & (1 << i)` 两种写法要弄清楚优先级，防止把左移当成乘法。  
  3. **计数方式**：`bin(mask).count('1')` 在 Python 中很方便，但若用手动位操作要确保循环结束条件正确。  
- **下次遇到同类题**：第一步先判断「搜索空间是否足够小（2ⁿ）」，如果可以，就直接用 **位掩码枚举**；随后检查「是否可以在枚举过程中提前剪枝」——比如利用「好人的话一定可信」这一约束，尽早发现冲突。这样既保证正确性，又能提升实际运行速度。