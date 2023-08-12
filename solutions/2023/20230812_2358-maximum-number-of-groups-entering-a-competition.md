# #2358. 比赛中可形成的最大组数 / Maximum Number of Groups Entering a Competition

> 难度：中等 · 标签：Array、Math、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-groups-entering-a-competition/)

---

## 题目（英文原版）

**Description**

You are given a positive integer array grades which represents the grades of students in a university. You would like to enter all these students into a competition in ordered non-empty groups, such that the ordering meets the following conditions:
Return the maximum number of groups that can be formed.

**Examples**

**Example 1:**

```
Input: grades = [10,6,12,7,3,5]
Output: 3
Explanation: The following is a possible way to form 3 groups of students:
- 1st group has the students with grades = [12]. Sum of grades: 12. Student count: 1
- 2nd group has the students with grades = [6,7]. Sum of grades: 6 + 7 = 13. Student count: 2
- 3rd group has the students with grades = [10,3,5]. Sum of grades: 10 + 3 + 5 = 18. Student count: 3
It can be shown that it is not possible to form more than 3 groups.
```

**Example 2:**

```
Input: grades = [8,8]
Output: 1
Explanation: We can only form 1 group, since forming 2 groups would lead to an equal number of students in both groups.
```

**Constraints**

- 1 <= grades.length <= 105
- 1 <= grades[i] <= 105

---

## 题目（中文翻译）

给定一个正整数数组 `grades`，其中 `grades[i]` 表示大学中第 i 名学生的成绩。你需要把所有学生按照 **有序的非空组**（ordered non‑empty groups）进行划分，使得组的顺序满足以下条件：

- 第 k 组的学生人数严格大于第 k‑1 组的学生人数；
- 第 k 组的成绩总和（sum of grades）严格大于第 k‑1 组的成绩总和。

返回可以形成的 **最大组数**（maximum number of groups）。

**示例 1**  
**输入**: `grades = [10,6,12,7,3,5]`  
**输出**: `3`  
**解释**: 以下是一种可能的划分方式，形成了 3 组学生：

- 第 1 组: 成绩为 `[12]`，成绩总和 = 12，学生人数 = 1  
- 第 2 组: 成绩为 `[6,7]`，成绩总和 = 6 + 7 = 13，学生人数 = 2  
- 第 3 组: 成绩为 `[10,3,5]`，成绩总和 = 10 + 3 + 5 = 18，学生人数 = 3  

（后续内容已截断）

**示例 2**  
**输入**: `grades = [8,8]`  
**输出**: `1`  
**解释**: 只能形成 1 组，因为若划分为 2 组，两组的学生人数会相等，违反了“学生人数严格递增”的要求。

**约束条件**  

- $1 \leq \text{grades.length} \leq 10^5$
- $1 \leq \text{grades}[i] \leq 10^5$

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的分组方式都枚举一遍**，然后挑选出满足题目条件且组数最多的那一种。  
- **枚举方式**：可以使用递归（或回溯）把数组从左到右切分，每次决定当前组的长度（从 1 到剩余元素个数），计算该组的成绩总和，检查它是否严格大于前一组的总和。  
- **使用的数据结构**：递归调用栈相当于一条“路线”，类似于我们在找字典里单词时的“查字典”。这里 `key` 是已经决定好的前几组，`value` 是对应的成绩和与已经形成的组数。  

**为什么这个方法正确**  
因为我们把**所有**合法的分割方式都尝试了一遍，只要有一种方式可以得到更大的组数，就一定会被遍历到，最终取最大值自然就是答案。

**为什么不推荐**  
- 组合数会爆炸：数组长度 `n` 最高可达 `10⁵`，即使 `n=20`，所有切分方式也有 `2^{n-1}` 种（每两个相邻元素之间可以选择“断开”或“不断开”），远远超出计算机的承受范围。  
- 时间复杂度呈指数级增长，实际运行会在几秒钟内超时甚至直接卡死。

#### 代码（Python）

```python
from typing import List

def brute_max_groups(grades: List[int]) -> int:
    # 递归枚举所有切分方式，返回合法的最大组数
    def dfs(idx: int, prev_sum: int, groups: int) -> int:
        # idx：当前处理到的下标
        # prev_sum：前一组的成绩和
        # groups：已经形成的组数
        if idx == len(grades):
            return groups                     # 所有学生都已经分完组

        best = groups                         # 先把“不再分组”的情况记下来
        cur_sum = 0
        # 尝试把从 idx 开始的前 k（k≥1）个学生组成下一组
        for j in range(idx, len(grades)):
            cur_sum += grades[j]
            # 只有当新组的成绩和严格大于前一组时才合法
            if cur_sum > prev_sum:
                best = max(best, dfs(j + 1, cur_sum, groups + 1))
        return best

    # 暴力搜索在 n 较大时会非常慢，仅作概念展示
    return dfs(0, 0, 0)
```

> **注意**：上述代码仅用于说明思路，**在实际提交时会因超时而失效**。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级），因为每两个相邻学生之间都有“切或不切”两种选择。  
- **空间复杂度**：`O(n)`，递归栈最深会达到 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于我们每次都要尝试所有可能的组大小**。实际上，题目只要求“**尽可能多的组**”，因此**每次都应该尽量让当前组尽可能小**，只要满足“成绩总和严格递增”的条件即可。  

**关键观察**  

1. **把学生成绩从小到大排序**  
   - 类比：把字典里的词条按字母顺序排好，这样查找会更有规律。  
   - 排序后，若我们从左到右依次取学生，后面的学生成绩只会更大，**更容易让后面的组的总和大于前面的组**。

2. **贪心地构造每一组**  
   - 第 1 组最小可以是 1 人；第 2 组至少需要 2 人；第 3 组至少需要 3 人……（因为若第 `k` 组人数少于 `k`，则必然导致前面的组人数更少，整体组数也会受限）。  
   - 这相当于在“**最小可能的组大小**”上做贪心：每当我们已经取到了 `cnt+1`（`cnt` 为已经形成的组数）个学生，并且这 `cnt+1` 个学生的成绩和 `cur_sum` **严格大于** 前一组的总和 `prev_sum`，我们就可以确认形成了第 `cnt+1` 组。

3. **为什么这种贪心一定最优**  
   - 我们总是**先尝试最小的合法组**。如果此时已经满足条件，那么把更多的学生塞进同一组只会**浪费**后面可以用来开启新组的学生，从而导致组数下降。  
   - 反之，如果当前的最小组（`cnt+1` 人）还不够大（`cur_sum ≤ prev_sum`），我们只能继续往里加学生，**直到满足**。这一步是不可避免的，因为无论怎么切，都必须让该组的总和大于前一组。

**算法步骤（伪代码）**

```
sort grades 升序
prev_sum = 0            // 前一组的成绩总和
cnt      = 0            // 已经形成的组数
cur_sum  = 0            // 正在累积的当前组成绩和
cur_len  = 0            // 当前组的学生人数

遍历每个 grade:
    cur_sum += grade
    cur_len += 1
    // 需要的最小人数是 cnt+1，且总和必须大于 prev_sum
    if cur_len > cnt and cur_sum > prev_sum:
        cnt      += 1          // 完成一组
        prev_sum = cur_sum     // 更新前一组的总和
        cur_sum  = 0           // 重置，准备下一组
        cur_len  = 0
返回 cnt
```

#### 代码（Python）

```python
from typing import List

def max_groups(grades: List[int]) -> int:
    """
    贪心算法：先把成绩排序，然后尽可能用最小的合法组数来分组。
    时间复杂度 O(n log n)（排序），空间复杂度 O(1)（原地操作）。
    """
    grades.sort()               # 1. 按成绩升序排列
    prev_sum = 0                # 前一组的成绩总和，初始为 0（因为不存在前组）
    cnt = 0                     # 已经形成的组数
    cur_sum = 0                 # 正在累积的当前组成绩和
    cur_len = 0                 # 当前组的学生人数

    for g in grades:
        cur_sum += g            # 累加当前学生的成绩
        cur_len += 1            # 当前组人数加 1
        # 当当前组人数已经超过已有组数 (cnt) 且成绩和大于前一组时，确定形成新组
        if cur_len > cnt and cur_sum > prev_sum:
            cnt += 1            # 组数加一
            prev_sum = cur_sum  # 更新前一组的成绩和
            cur_sum = 0         # 清空，为下一组做准备
            cur_len = 0

    return cnt
```

> **代码解释**  
> - `cur_len > cnt` 保证第 `k` 组至少有 `k` 人（因为已经有 `cnt` 组，下一组的最小人数是 `cnt+1`）。  
> - `cur_sum > prev_sum` 正是题目要求的“每组成绩总和严格递增”。  
> - 一旦两条条件同时满足，就可以**立刻封闭当前组**，因为继续往里加只会让后面的组更难满足条件。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `n` 为学生人数。主要耗时在排序（`log n` 是排序的对数因子），遍历一次数组的过程是线性的 `O(n)`。  
  - 与暴力解的指数级 `O(2^n)` 相比，几乎可以在毫秒级完成，即使 `n = 10⁵` 也毫无压力。  

- **空间复杂度**：`O(1)`（不计入输入数组本身）  
  - 除了若干整数变量外，只使用了常数级的额外空间。  
  - 如果语言的排序实现需要额外的临时数组（如 Python 的 Timsort），也只是 `O(n)` 的临时空间，仍然符合题目对“额外空间”较宽松的要求。

---

## 心得

- **核心技巧**：**贪心 + 排序**。先把数据排好序，再一次遍历中“最小合法组”即可得到最大组数。  
- **适用的题型**（类似思路）  
  1. **分割数组使每段和递增**（如 LeetCode 2415 “Stepping Numbers” 的思路）。  
  2. **最小子序列个数**（如“分割数组使子数组和大于等于 K”）。  
  3. **按大小顺序装箱**（如“最少的堆叠数”或“最少的船只数”）。  
- **一句话总结解题钥匙**：**“把学生按成绩从小到大排列，始终用最小可能的合法组把他们装进去”。**

---

## 反思

- **第一反应**：看到“分组且每组成绩和递增”，立刻想到**枚举所有切分**（回溯），因为这样最能确保不漏掉任何合法方案。  
- **最容易踩的坑**  
  1. **忽视“每组人数至少递增 1”**：如果只检查总和递增而不限制组大小，可能会出现“把很多学生塞进同一组”，导致组数不是最大。  
  2. **边界条件**：当数组只有 1 或 2 个元素时，代码必须仍能正确返回 1（因为无法形成 2 组且满足递增）。  
  3. **整数溢出**（在某些语言中）——虽然 Python 没问题，但在 C++/Java 中要注意使用 `long long`。  
- **下次遇到同类题**：第一步先**排序**，然后**思考最小合法单位**（最小子集、最小长度、最小重量等），再用**一次遍历的贪心**来“尽可能多地”完成目标。这样往往能把指数级的搜索压缩到 `O(n log n)`。