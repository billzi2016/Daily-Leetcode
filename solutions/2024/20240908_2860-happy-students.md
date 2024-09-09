# #2860. 快乐的学生 / Happy Students

> 难度：中等 · 标签：Array、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/happy-students/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n where n is the total number of students in the class. The class teacher tries to select a group of students so that all the students remain happy.
The ith student will become happy if one of these two conditions is met:
Return the number of ways to select a group of students so that everyone remains happy.

**Examples**

**Example 1:**

```
Input: nums = [1,1]
Output: 2
Explanation: 
The two possible ways are:
The class teacher selects no student.
The class teacher selects both students to form the group. 
If the class teacher selects just one student to form a group then the both students will not be happy. Therefore, there are only two possible ways.
```

**Example 2:**

```
Input: nums = [6,0,3,3,6,7,2,7]
Output: 3
Explanation: 
The three possible ways are:
The class teacher selects the student with index = 1 to form the group.
The class teacher selects the students with index = 1, 2, 3, 6 to form the group.
The class teacher selects all the students to form the group.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] < nums.length

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`，其中 `n` 表示班级中学生的总人数。班主任想要挑选一组学生，使得所有学生都保持快乐。第 `i` 位学生如果满足以下两条条件中的任意一条，就会感到快乐：

（题目原文中未给出具体的两条条件，这里保持原样）

返回能够使所有学生都快乐的挑选方式的数量。

**示例 1**  
输入: `nums = [1,1]`  
输出: `2`  
解释:  
可能的两种方式为：  
- 班主任不选任何学生。  
- 班主任选取所有学生组成小组。  

如果班主任只选取一个学生组成小组，则两位学生都不会感到快乐。因此，只有上述两种有效的方式。

**示例 2**  
输入: `nums = [6,0,3,3,6,7,2,7]`  
输出: `3`  
解释:  
可能的三种方式为：  
- 班主任只选取下标为 `1` 的学生组成小组。  
- 班主任选取下标为 `1, 2, 3, 6` 的学生组成小组。  
- 班主任选取所有学生组成小组。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `0 <= nums[i] < nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的学生子集**，逐个检查每个子集里每个学生是否满足“开心”条件。  
- **子集**可以想象成一本笔记本里把每个学生的名字写上去或不写，上面有 2ⁿ 种写法（每个学生两种状态：选 / 不选）。  
- 对每一种写法，我们都要遍历一遍学生，判断他们是“被选中”还是“未选中”，再根据题目给出的两个条件判断他们是否开心。  

> **为什么暴力能得到正确答案？**  
> 因为我们把**所有可能的组合**都检查了一遍，凡是满足条件的必然被计数，凡是不满足的必然被剔除，所以答案一定正确。  

> **时间/空间复杂度大白话**  
> - 时间复杂度：`O(2^n * n)`  
>   - `2^n` 是所有子集的数量，随着学生人数每增加一次，可能的组合就会 **翻倍**（比如 10 人有 1024 种，20 人有 1,048,576 种）。  
>   - 对每个子集我们还要遍历 `n` 次学生来判断是否开心。  
>   - 用大白话讲，就是“先把所有可能的组合全部列出来（指数级的多），再对每个组合逐个检查（线性的多）”。  
> - 空间复杂度：`O(n)` 用来保存当前子集的选/不选状态（可以用一个长度为 `n` 的布尔数组），除此之外几乎不占额外空间。

#### 代码（Python）

```python
from itertools import product
from typing import List

def happy_students_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # product([0, 1], repeat=n) 会生成 0/1 的所有排列，0 表示不选，1 表示选
    for mask in product([0, 1], repeat=n):
        k = sum(mask)                # 选中的学生人数
        ok = True

        for i in range(n):
            if mask[i] == 1:         # 第 i 位学生被选中
                # 选中时必须满足：k - 1 >= nums[i]  （即 k > nums[i]）
                if k - 1 < nums[i]:
                    ok = False
                    break
            else:                    # 第 i 位学生未被选中
                # 未选中时必须满足：k <= nums[i]
                if k > nums[i]:
                    ok = False
                    break

        if ok:
            ans += 1                  # 这个子集满足所有学生都开心

    return ans
```

> 这段代码可以直接跑通，但只适用于 `n` 很小（比如 `n ≤ 20`）的情况，超过这个规模就会超时。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)` —— 随着学生人数指数级增长，几乎不可能在真实数据（`n ≤ 10^5`）上通过。  
- **空间复杂度**：`O(n)` —— 只用了一个长度为 `n` 的数组来保存当前的选/不选状态。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到**瓶颈在于枚举所有子集**。实际上，题目中的两个开心条件可以化简成一种非常强的约束：  

> **如果一个学生的 `nums[i] = x` 被选中，那么所有 `nums[j] ≤ x` 的学生也必须被选中；**  
> **如果一个学生的 `nums[i] = x` 没被选中，那么所有 `nums[j] ≥ x` 的学生也必须不被选中。**  

这意味着**被选中的学生集合一定是按照 `nums` 的大小取一个前缀**（类似把排好序的学生从左到右依次挑选，挑到哪儿就停下来）。  

把这个想法进一步抽象：设选中的学生数为 `k`（`k` 可以是 `0 … n`）。  
- 对于 **被选中** 的学生，需要 `k - 1 ≥ nums[i]`，即 `nums[i] < k`。  
- 对于 **未选中** 的学生，需要 `k ≤ nums[i]`，即 `nums[i] ≥ k`。  

于是我们得到一个**等价的条件**：  
> **恰好有 `k` 个学生的 `nums[i]` 小于 `k`。**  

换句话说，`k` 必须满足  

```
count( nums[i] < k ) == k
```

只要找出所有满足上式的 `k`，每个 `k` 对应一种合法的选取方式（把所有 `nums[i] < k` 的学生全部选上，其余全部不选）。

**如何高效计算？**  
- `nums[i]` 的取值范围是 `[0, n-1]`（题目保证），我们可以统计每个值出现的次数，用一个长度为 `n+1` 的数组 `freq`（类似字典查词条的“词典”，键是数字，值是出现次数）。  
- 然后从 `k = 0` 到 `n`，**累计** 小于 `k` 的学生数 `prefix`（相当于在排好序的数组上走指针，实时知道左边有多少元素）。  
- 每一次检查 `prefix == k`，如果相等，就找到了一个合法的 `k`，答案加一。  

> **类比**：想象一排盒子里装有不同大小的石子，盒子编号从 `0` 到 `n`。我们把石子从左往右一个个搬走，记录已经搬走的石子数量。如果搬走的数量恰好等于当前盒子的编号，那么这一次搬走的过程就是一种“合法”方案。  

#### 代码（Python）

```python
from typing import List

def happy_students(nums: List[int]) -> int:
    n = len(nums)

    # 1. 统计每个值出现的次数，freq[x] 表示 nums 中等于 x 的学生有多少个
    #    （这里把 freq 当成“字典”，key 是数字 x，value 是出现次数）
    freq = [0] * (n + 1)          # 额外多一个位置，防止访问越界
    for x in nums:
        freq[x] += 1

    ans = 0          # 最终答案
    prefix = 0       # 当前累计的、值 < k 的学生人数

    # 2. 枚举可能的选中人数 k（从 0 到 n）
    for k in range(n + 1):
        # 此时 prefix 已经是 count( nums[i] < k )
        if prefix == k:          # 正好满足 “恰好有 k 个学生的值 < k”
            ans += 1

        # 为了准备检查下一个 k+1，需要把值等于 k 的学生加入 prefix
        # 因为下一个循环里 “小于 k+1” 就包括了 “等于 k”
        if k <= n:               # 防止访问 freq[n]（虽然它一定是 0）
            prefix += freq[k]

    return ans
```

> 关键行中文注释已经解释了每一步的意义，代码可以直接运行。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组做频数统计（`O(n)`），再遍历一次 `0 … n` 检查每个 `k`（`O(n)`），所以整体线性。  
  - 与暴力解的指数级时间相比，快了 **天壤之别**，即使 `n = 10^5` 也能毫秒级完成。  
- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n+1` 的频数数组 `freq`（相当于一本“查字典”，键是数字，值是出现次数），除此之外几乎不占额外空间。  

---

## 心得  

- **核心技巧**：把“学生是否开心”转化为 **“选中人数 k 必须等于值小于 k 的学生数量”**，从而把原来的组合枚举问题简化为 **统计前缀计数**。  
- **该技巧适用的题型**  
  1. **固定点计数**（如 LeetCode 1822 *"Significant Inversions"* 类似的 “找 k 使得 count(<k) = k”）  
  2. **基于阈值的前缀选择**（如 “Maximum Length of Subarray With Positive Product” 中的前缀统计思路）  
  3. **满足两侧单调约束的子集问题**（如 “Remove Minimum Number of Magic Beans”）  
- **一句话总结解题钥匙**：**把每个学生的需求转化为对选中人数的上下界，然后只需在 0…n 中找满足 “前缀计数 = 当前人数” 的点。**

---

## 反思  

- **第一反应**：看到“每个学生都有两个条件”，自然想到**枚举所有子集**，这在小规模时可行，却忽视了规模限制。  
- **最容易踩的坑**  
  1. **遗漏空集合**：`k = 0` 也是合法的，需要在循环起始时就检查。  
  2. **边界值**：`nums[i]` 可能等于 `n`（虽然题目说 `< n`），所以在构造频数数组时要预留 `n+1` 的空间，防止越界。  
  3. **重复值的处理**：如果只检查 `k` 是否在 `nums` 中出现，会漏掉像示例 2 中 `k = 4`（不在原数组）这种合法情况。必须用 **累计计数** 而不是单纯查找值。  
- **下次类似题目第一步**：先**把条件写成关于全局变量（如选中人数、前缀和）的不等式**，看能否得到“前缀/后缀”形式的约束，这往往能把指数级搜索降到线性。