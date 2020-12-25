# #1125. 最小足够团队 / Smallest Sufficient Team

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/smallest-sufficient-team/)

---

## 题目（英文原版）

**Description**

In a project, you have a list of required skills req_skills, and a list of people. The ith person people[i] contains a list of skills that the person has.
Consider a sufficient team: a set of people such that for every required skill in req_skills, there is at least one person in the team who has that skill. We can represent these teams by the index of each person.
Return any sufficient team of the smallest possible size, represented by the index of each person. You may return the answer in any order.
It is guaranteed an answer exists.

**Examples**

**Example 1:**

```
Input: req_skills = ["java","nodejs","reactjs"], people = [["java"],["nodejs"],["nodejs","reactjs"]]
Output: [0,2]
```

**Example 2:**

```
Input: req_skills = ["algorithms","math","java","reactjs","csharp","aws"], people = [["algorithms","math","java"],["algorithms","math","reactjs"],["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],["aws","java"]]
Output: [1,2]
```

**Constraints**

- 1 <= req_skills.length <= 16
- 1 <= req_skills[i].length <= 16
- req_skills[i] consists of lowercase English letters.
- All the strings of req_skills are unique.
- 1 <= people.length <= 60
- 0 <= people[i].length <= 16
- 1 <= people[i][j].length <= 16
- people[i][j] consists of lowercase English letters.
- All the strings of people[i] are unique.
- Every skill in people[i] is a skill in req_skills.
- It is guaranteed a sufficient team exists.

---

## 题目（中文翻译）

在一个项目中，你有一个必需技能列表 `req_skills`，以及一个人员列表。第 `i` 个人 `people[i]` 包含该人拥有的技能列表。

考虑 **足够团队**（sufficient team）：一组人员，使得 `req_skills` 中的每一项必需技能至少有团队中的一名成员具备。我们可以用每个人的下标来表示这些团队。

返回任意一个 **最小足够团队**（size 最小的 sufficient team），用其成员的下标数组表示。答案的下标顺序不限。

保证一定存在答案。

**示例 1**  
**示例 2**  

**约束条件**

- `1 <= req_skills.length <= 16`
- `1 <= req_skills[i].length <= 16`
- `req_skills[i]` 只包含小写英文字母。
- `req_skills` 中的所有字符串互不相同。
- `1 <= people.length <= 60`
- `0 <= people[i].length <= 16`
- `1 <= people[i][j].length <= 16`
- `people[i][j]` 只包含小写英文字母。
- `people[i]` 中的所有字符串互不相同。
- `people[i]` 中的每个技能必定出现在 `req_skills` 中。
- 必然存在一个足够团队。

**示例**

示例 1:  
Input: `req_skills = ["java","nodejs","reactjs"], people = [["java"],["nodejs"],["nodejs","reactjs"]]`  
Output: `[0,2]`

示例 2:  
Input: `req_skills = ["algorithms","math","java","reactjs","csharp","aws"], people = [["algorithms","math","java"],["algorithms","math","reactjs"],["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],["aws","java"]]`  
Output: `[1,2]`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有可能的人员组合**，看哪个组合能够覆盖所有必需技能，并且人数最少。  
- **数据结构**：我们可以把每个人的技能看成一个集合（`set`），把所有必需技能也看成一个集合。判断一个组合是否足够，只需要把组合里所有人的技能集合`union`起来，看看是否等于必需技能集合。  
- **生活化类比**：把必需技能想象成一张“任务清单”，每个人是一本“工具书”，书里列出的技能就是这本书的“章节”。我们要挑选最少的几本书，使得所有章节都有对应的书提供。  
- **正确性**：只要遍历到的每一种人员子集都检查一次，必然能找到满足条件的最小子集（因为题目保证至少有解）。  

#### 代码（Python）  

```python
from itertools import combinations
from typing import List

def smallestSufficientTeam(req_skills: List[str], people: List[List[str]]) -> List[int]:
    # 把必需技能转成集合，方便后面比较
    need = set(req_skills)
    n = len(people)

    # 先把每个人的技能集合化，去掉与需求无关的（题目保证全有关，这里仅作演示）
    skill_sets = [set(p) for p in people]

    # 从人数最少的子集开始枚举，找到第一个满足条件的即为答案
    for r in range(1, n + 1):                     # r 表示子集大小
        for idxs in combinations(range(n), r):    # 生成所有 r 人的组合
            combined = set()
            for i in idxs:
                combined |= skill_sets[i]         # 合并技能
            if combined >= need:                  # 是否覆盖全部必需技能
                return list(idxs)                 # 找到最小团队，直接返回
    return []   # 题目保证一定有解，这行不会被执行
```

*关键行解释*  
- `for r in range(1, n + 1)`: 从 1 人的组合开始，逐渐增加人数，保证第一次找到的就是最小的。  
- `combinations(range(n), r)`: Python 标准库生成所有不重复的 `r` 人组合。  
- `combined |= skill_sets[i]`: “并集”操作，等价于把这个人的技能加入已有的技能集合。  

#### 复杂度  

- **时间复杂度**：  
  暴力枚举所有子集，最坏情况下要检查 `2^n`（`n` 为人数）个组合。每个组合合并技能的代价是 `O(k)`（`k` 为技能总数），所以总体是 **O( n·2ⁿ )**。  
  大白话：如果有 20 个人，组合数大约是 1,048,576（约一百万），算起来会很慢。  

- **空间复杂度**：  
  只用了常数级额外空间（存放几个集合和递归栈），所以是 **O(1)**（不计输入本身的空间）。  



---  

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于枚举所有人员子集，人数稍多就会指数爆炸。  
观察题目约束：  

- 必需技能数量 `|req_skills| ≤ 16`（很小）  
- 人数 `|people| ≤ 60`（相对大一些）  

因为技能数目小，我们可以**把技能集合编码成二进制位**（位掩码），每一位表示一种技能是否已被覆盖。这样，**状态空间从指数 `2^n` 降到 `2^m`（`m = |req_skills| ≤ 16`）**，只有最多 65536 种可能的技能覆盖情况。  

**核心思路：动态规划 + 位运算**  

1. 为每个必需技能分配一个唯一的编号 `0 … m-1`，并把每个人的技能集合转换成一个整数 `mask`，第 `i` 位为 `1` 表示该人会第 `i` 种技能。  
2. 用 DP 数组 `dp[mask]` 记录**得到技能集合 `mask` 所需的最小团队**（用人员下标列表表示）。  
   - 初始时 `dp[0] = []`（不需要任何技能，团队为空），其他 `dp` 为 `None`（未达成）。  
3. 对每个人的 `person_mask`，遍历已有的 `dp` 状态 `old_mask`（可以用 `list(dp.items())` 复制一遍防止遍历时被覆盖），  
   - 新的技能集合 `new_mask = old_mask | person_mask`（把此人的技能加入已有技能）。  
   - 如果 `dp[new_mask]` 为空或 `len(dp[old_mask]) + 1 < len(dp[new_mask])`，说明使用此人可以得到更小的团队，就更新 `dp[new_mask]` 为 `dp[old_mask] + [person_index]`。  
4. 最后 `dp[full_mask]`（`full_mask = (1 << m) - 1`）即为覆盖全部技能的最小团队。  

**为什么这一步是对的？**  
DP 的每一步都在记录**“已经覆盖的技能集合对应的最优团队”**，而更新时只会把团队人数更少的方案保留下来。因为每个人只会被考虑一次（可以多次加入不同的状态），所有可能的组合都会在某个 `mask` 中出现，最终的 `full_mask` 必然得到最小人数的团队。  

**类比**：把每一种“已完成的任务集合”想象成一张“进度表”，我们在每一步尝试“派一个新成员加入”，如果这样可以让进度表更快完成（用更少人），就把进度表更新为更优解。  

#### 代码（Python）  

```python
from typing import List

def smallestSufficientTeam(req_skills: List[str], people: List[List[str]]) -> List[int]:
    # 1️⃣ 为每个必需技能编号，建立 skill -> index 的映射
    skill_index = {skill: i for i, skill in enumerate(req_skills)}
    m = len(req_skills)                     # 技能总数，最多 16

    # 2️⃣ 把每个人的技能集合转成位掩码（整数）
    person_masks = []
    for p in people:
        mask = 0
        for s in p:
            mask |= 1 << skill_index[s]    # 把对应位设为 1
        person_masks.append(mask)

    # 3️⃣ DP：mask -> 最小团队（下标列表）
    # 使用字典而不是列表，方便只保存已到达的状态
    dp = {0: []}                            # 0 技能需要空团队

    for i, pmask in enumerate(person_masks):
        if pmask == 0:                      # 此人不带任何必需技能，直接跳过
            continue
        # 为防止在遍历时修改 dp，先把当前的所有条目复制出来
        cur_items = list(dp.items())
        for old_mask, team in cur_items:
            new_mask = old_mask | pmask      # 把此人加入后得到的新技能集合
            # 如果新集合还没有解，或可以用更少的人数得到，则更新
            if new_mask not in dp or len(team) + 1 < len(dp[new_mask]):
                dp[new_mask] = team + [i]

    full_mask = (1 << m) - 1                # 所有技能对应的掩码，例如 111...1
    return dp[full_mask]                    # 必然存在最优解
```

*关键行解释*  
- `mask |= 1 << skill_index[s]`：把技能对应的位设为 `1`，相当于把该技能记在二进制“清单”里。  
- `new_mask = old_mask | pmask`：位或操作，表示把当前人的技能加入已有技能集合。  
- `if new_mask not in dp or len(team) + 1 < len(dp[new_mask])`：如果这条新路径更短，就用它覆盖旧的。  

#### 复杂度  

- **时间复杂度**：  
  - 人数 `n ≤ 60`，技能数 `m ≤ 16`，状态数 `2^m ≤ 65536`。  
  - 对每个人遍历已有的 DP 状态一次，最坏是 `n * 2^m` 次位运算和列表复制，故 **O(n·2^m)**。  
  - 以实际最大值算：`60 * 65536 ≈ 3.9 million` 次操作，完全可以在毫秒级完成。  

- **空间复杂度**：  
  - DP 表最多保存 `2^m` 条记录，每条记录是一段人员下标列表，最坏情况是 `O(2^m * m)`（因为每个团队最多 `m` 个人），但实际远小于这个上限。  
  - 简化记为 **O(2^m)**，即最多几万条记录，内存消耗几 MB，完全可接受。  



---  

## 心得  

- **核心技巧**：**位掩码 + 动态规划**，把「少量的技能」映射到二进制状态，用 DP 记录每个状态的最优子集。  
- **适用的题型**：  
  1. “最小覆盖集合”类问题（如 **最小集合覆盖**、**最小基因突变**等）。  
  2. 需要在 **有限种属性**（≤20）上做组合优化的题目（如 **按位与的最大子集**、**拼图游戏**）。  
- **一句话总结**：  
  > 当要覆盖的种类不多时，先把种类压缩成二进制位，再用 DP 按位转移，就能在指数级状态里快速找到最小组合。  



---  

## 反思  

- **第一反应**：先想到枚举所有人员子集，写出最直观的暴力解。  
- **最容易踩的坑**：  
  - **技能映射错误**：忘记把技能统一映射到同一编号，导致位掩码不对应。  
  - **状态更新顺序**：在遍历 DP 时直接在原字典上修改会产生“使用同一个人多次更新同一轮”的错误，需要先复制当前状态列表。  
  - **空技能人员**：有的 `people[i]` 可能不包含任何必需技能，若不跳过会导致不必要的循环。  
- **下次遇到类似题**：第一步先判断“可变维度是否小”，如果是，就**把维度压成位掩码**；随后用 **DP（或 BFS）在 2^维度 的状态空间里搜索**，而不是直接枚举所有元素的子集。