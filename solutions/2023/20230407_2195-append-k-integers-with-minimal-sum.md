# #2195. 追加 K 个整数以获得最小总和 / Append K Integers With Minimal Sum

> 难度：中等 · 标签：Array、Math、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/append-k-integers-with-minimal-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. Append k unique positive integers that do not appear in nums to nums such that the resulting total sum is minimum.
Return the sum of the k integers appended to nums.

**Examples**

**Example 1:**

```
Input: nums = [1,4,25,10,25], k = 2
Output: 5
Explanation: The two unique positive integers that do not appear in nums which we append are 2 and 3.
The resulting sum of nums is 1 + 4 + 25 + 10 + 25 + 2 + 3 = 70, which is the minimum.
The sum of the two integers appended is 2 + 3 = 5, so we return 5.
```

**Example 2:**

```
Input: nums = [5,6], k = 6
Output: 25
Explanation: The six unique positive integers that do not appear in nums which we append are 1, 2, 3, 4, 7, and 8.
The resulting sum of nums is 5 + 6 + 1 + 2 + 3 + 4 + 7 + 8 = 36, which is the minimum. 
The sum of the six integers appended is 1 + 2 + 3 + 4 + 7 + 8 = 25, so we return 25.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 108

---

## 题目（中文翻译）

给定一个整数数组 (array) `nums` 和一个整数 `k`。向 `nums` 中追加 `k` 个**唯一的 (unique) 正整数 (positive integer)**，且这些整数在 `nums` 中不存在，使得追加后的总体和最小。返回这 `k` 个追加整数的和。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1:**  
Input: nums = [1,4,25,10,25], k = 2  
Output: 5  
Explanation: 我们在 `nums` 中追加的两个**唯一的**且**不在** `nums` 中的**正整数**是 2 和 3。  
追加后的 `nums` 和为 1 + 4 + 25 + 10 + 25 + 2 + 3 = 70，是最小可能值。  
追加的两个整数之和为 2 + 3 = 5，故返回 5。

**示例 2:**  
Input: nums = [5,6], k = 6  
Output: 25  
Explanation: 我们在 `nums` 中追加的六个**唯一的**且**不在** `nums` 中的**正整数**是 1、2、3、4、7、8。  
追加后的 `nums` 和为 5 + 6 + 1 + 2 + 3 + 4 + 7 + 8 = 36，是最小可能值。  
追加的六个整数之和为 1 + 2 + 3 + 4 + 7 + 8 = 25，故返回 25。

**约束条件**  
- 1 ≤ `nums.length` ≤ 10^5  
- 1 ≤ `nums[i]` ≤ 10^9  
- 1 ≤ `k` ≤ 10^8

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**从 1 开始逐个检查**，看它是否已经出现在 `nums` 中。如果没有，就把它当作要“追加”的数，累计到答案里，直到找到 `k` 个为止。

- **数据结构**：我们需要能够**快速判断一个数是否在原数组**。  
  使用 **哈希表（Python 的 `set`）**，它的工作方式类似于**查字典**：把单词当作 `key`，对应的页码当作 `value`，查找时只需要看字典里有没有这个单词，时间几乎是常数 `O(1)`。

- **为什么正确**：  
  题目要求“把 `k` 个不在 `nums` 中的正整数加入，使得它们的和最小”。显然，**越小的正整数越有利于让和变小**。所以只要从最小的正整数 1 开始，依次挑选那些不在 `nums` 里的数，恰好得到最小的 `k` 个。

- **复杂度分析（大白话）**：  
  - 每检查一个数，我们只做一次哈希表查找，几乎是瞬间完成的（常数时间）。  
  - 但如果 `nums` 前面占了很多小数字（比如 `nums = [1,2,3,…,10⁵]`），我们就要跳过它们，实际检查的数字会远大于 `k`。最坏情况下我们可能要检查到 `k + max(nums)`。  
  - **时间复杂度** 记作 `O(k + m)`，其中 `m` 是我们在检查过程中遇到的、已经在 `nums` 中的数字个数。  
  - **空间复杂度** 只用了一个集合来存 `nums`，大小是 `O(n)`（`n` 为 `nums` 长度），相当于把原数组“搬进字典”去查。

#### 代码（Python）

```python
def minimalKSum_bruteforce(nums, k):
    # 把 nums 放进哈希表，查找 O(1)
    exist = set(nums)          # 哈希表：像字典一样，key 是出现的数

    added = 0                  # 已经追加的个数
    cur = 1                    # 当前检查的正整数
    ans = 0                    # 需要返回的 sum

    # 循环直到找到 k 个不在 nums 里的数
    while added < k:
        if cur not in exist:   # 如果 cur 没出现过，就可以追加
            ans += cur
            added += 1
        cur += 1               # 检查下一个正整数

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k + m)`  
  - `k` 是必须追加的个数，`m` 是在检查过程中跳过的、已经在 `nums` 中的数。  
  - 用大白话说，就是“我们可能会检查比需要的多一些的数字”。

- **空间复杂度**：`O(n)`  
  - 需要额外的集合来存放 `nums` 中的所有不同元素，大小随 `nums` 长度线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **逐个检查**：当 `nums` 包含很多小数字时，我们会浪费大量时间在“已经被占用”的数上。  
我们可以 **一次性跳过这些占用的区间**，只在缺口（gap）里取数。

关键思路：

1. **去重并排序**  
   - 把 `nums` 变成 **唯一且有序** 的序列 `arr`。  
   - 去重是必要的，因为重复的数字不影响我们“缺口”的位置。  
   - 排序后，相邻两个数之间的差值就能直接告诉我们这两个数之间还有多少**未被占用的正整数**。

2. **遍历每个缺口**  
   - 设 `prev` 为上一个已经处理好的数字（初始为 0，代表 0 之前的所有正整数都可以使用）。  
   - 对每个 `x`（按升序）：
     - 区间 `(prev, x)` 之间的整数都是 **合法且未出现** 的。  
     - 该区间长度 `gap = x - prev - 1`（因为两端都不算）。  
     - 如果 `k` 小于等于 `gap`，说明我们只需要从这段区间里取前 `k` 个数，**直接用等差数列求和公式**得到答案后结束。  
     - 否则，把整个区间的和全部加进去，`k -= gap`，继续向后检查。

3. **处理完所有数组元素后仍有剩余**  
   - 如果遍历完 `arr` 仍然没有取够 `k` 个数，说明剩下的数全在 `arr` 最大值之后。此时我们只需要从 `arr[-1] + 1` 开始取连续的 `k` 个数，同样用等差数列求和。

**等差数列求和**：  
前 `n` 个正整数的和是 `n * (n + 1) // 2`。  
如果我们从 `a` 开始取 `cnt` 个连续整数，和为  

\[
\text{sum} = \frac{(a + a + cnt - 1) \times cnt}{2}
\]

这就是 **首项 + 末项** 再乘以 **项数** 再除以 2。

#### 代码（Python）

```python
def minimalKSum(nums, k):
    # 1️⃣ 去重并排序
    arr = sorted(set(nums))          # 去掉重复并升序排列，像把所有“已占用的房间号”排好队

    ans = 0                           # 最终要返回的和
    prev = 0                          # 上一个已经处理好的数字，初始为 0（因为正整数从 1 开始）

    for x in arr:                     # 依次检查每个已占用的数字
        gap = x - prev - 1            # (prev, x) 之间的空位数量
        if gap > 0:                   # 只有真正有空位时才考虑
            if k <= gap:              # 需要的数量在当前空位里就能凑齐
                # 直接取从 prev+1 开始的 k 个连续整数的和
                start = prev + 1
                ans += (start + start + k - 1) * k // 2
                return ans
            else:                     # 把整个空位都拿走
                start = prev + 1
                ans += (start + start + gap - 1) * gap // 2
                k -= gap               # 还差多少个
        prev = x                       # 更新已处理的最大数字

    # 2️⃣ 走完所有已占用数字后，如果 k 仍然大于 0，说明剩下的数都在最后一个元素之后
    #    从 prev+1 开始取连续的 k 个数
    start = prev + 1
    ans += (start + start + k - 1) * k // 2
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 主要开销是对 `nums` 去重并排序（`n` 为 `nums` 长度）。排序像把一堆乱七八糟的书摆进书架，需要 `n log n` 的时间。  
  - 之后的遍历是线性 `O(n)`，远小于排序的代价。  
  - 与暴力解相比，我们不再逐个检查每个正整数，而是一次性跳过大段已占用的区间，速度快很多。

- **空间复杂度**：`O(n)`  
  - 需要额外的集合存放去重后的元素，再把它们转成列表排序，整体空间与原数组大小同阶。

---

## 心得

- **核心技巧**：**利用排序后的“缺口”一次性取连续区间**，并用 **等差数列求和公式** 把区间求和的工作压缩到常数时间。  
- **适用的题型**：  
  1. “找最小/最大 k 个不在集合中的数” —— 如本题、LeetCode 2336 “Maximum Sum of a Subarray After One Operation”。  
  2. “在已占用的区间中插入最少的数” —— 如 “Missing Positive Number” 系列。  
  3. “区间补全” 需要一次性跳过已占用段的场景。  
- **一句话总结**：**先把已有数字排好序，然后在每段空隙里直接算和，省掉逐个检查的时间**。

---

## 反思

- **第一反应**：立刻想到“从 1 开始枚举，遇到不在 `nums` 的就加”。这其实已经是对题意的直觉理解，但忽视了 `nums` 可能很大、导致枚举过慢。  
- **最容易踩的坑**：  
  - 忘记去重，导致同一个数字占用了多个空位，错误地缩小了可选范围。  
  - 计算区间和时写错等差数列公式（尤其是首项和末项的计算）。  
  - `k` 可能非常大（最高 10⁸），直接循环 `k` 次会超时，需要一次性算和。  
- **下次类似题的第一步**：**把已有元素去重并排序**，这样可以直接看到“哪里有空位”，再决定是一次性跳过还是逐个枚举。