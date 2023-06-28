# #2300. 成功的咒语与药水配对 / Successful Pairs of Spells and Potions

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/)

---

## 题目（英文原版）

**Description**

You are given two positive integer arrays spells and potions, of length n and m respectively, where spells[i] represents the strength of the ith spell and potions[j] represents the strength of the jth potion.
You are also given an integer success. A spell and potion pair is considered successful if the product of their strengths is at least success.
Return an integer array pairs of length n where pairs[i] is the number of potions that will form a successful pair with the ith spell.

**Examples**

**Example 1:**

```
Input: spells = [5,1,3], potions = [1,2,3,4,5], success = 7
Output: [4,0,3]
Explanation:
- 0th spell: 5 * [1,2,3,4,5] = [5,10,15,20,25]. 4 pairs are successful.
- 1st spell: 1 * [1,2,3,4,5] = [1,2,3,4,5]. 0 pairs are successful.
- 2nd spell: 3 * [1,2,3,4,5] = [3,6,9,12,15]. 3 pairs are successful.
Thus, [4,0,3] is returned.
```

**Example 2:**

```
Input: spells = [3,1,2], potions = [8,5,8], success = 16
Output: [2,0,2]
Explanation:
- 0th spell: 3 * [8,5,8] = [24,15,24]. 2 pairs are successful.
- 1st spell: 1 * [8,5,8] = [8,5,8]. 0 pairs are successful. 
- 2nd spell: 2 * [8,5,8] = [16,10,16]. 2 pairs are successful. 
Thus, [2,0,2] is returned.
```

**Constraints**

- n == spells.length
- m == potions.length
- 1 <= n, m <= 105
- 1 <= spells[i], potions[i] <= 105
- 1 <= success <= 1010

---

## 题目（中文翻译）

你得到两个正整数数组 **spells** 和 **potions**，长度分别为 *n* 和 *m*，其中 `spells[i]` 表示第 *i* 个咒语的强度，`potions[j]` 表示第 *j* 个药水的强度。  
另外给定一个整数 `success`。如果一对咒语与药水的强度乘积（product）不少于 `success`，则该配对被视为成功（successful pair）。  
返回一个长度为 *n* 的整数数组 `pairs`，其中 `pairs[i]` 表示能够与第 *i* 个咒语形成成功配对的药水数量。

**示例 1**  
**输入**: `spells = [5,1,3]`, `potions = [1,2,3,4,5]`, `success = 7`  
**输出**: `[4,0,3]`  
**解释**:  
- 第 0 个咒语: `5 * [1,2,3,4,5] = [5,10,15,20,25]`，其中 4 对的乘积 ≥ `success`，因此成功配对数为 4。  
- 第 1 个咒语: `1 * [1,2,3,4,5] = [1,2,3,4,5]`，没有乘积达到 `success`，成功配对数为 0。  
- 第 2 个咒语: `3 * [1,2,3,4,5] = [3,6,9,12,15]`，其中 3 对的乘积 ≥ `success`，成功配对数为 3。  
返回 `[4,0,3]`。

**示例 2**  
**输入**: `spells = [3,1,2]`, `potions = [8,5,8]`, `success = 16`  
**输出**: `[2,0,2]`  
**解释**:  
- 第 0 个咒语: `3 * [8,5,8] = [24,15,24]`，其中 2 对的乘积 ≥ `success`。  
- 第 1 个咒语: `1 * [8,5,8] = [8,5,8]`，没有配对满足条件。  
- 第 2 个咒语: `2 * [8,5,8] = [16,10,16]`，其中 2 对的乘积 ≥ `success`。  
返回 `[2,0,2]`。

**约束条件**  
- `n == spells.length`  
- `m == potions.length`  
- `1 <= n, m <= 10^5`  
- `1 <= spells[i], potions[i] <= 10^5`  
- `1 <= success <= 10^10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把每一条 **spell** 都和 **所有 potion** 两两相乘，看看乘积是否大于等于 `success`，满足的就计数。  

- **使用的数据结构**：两个普通的列表（`spells`、`potions`），遍历时会产生一个计数器 `cnt`。可以把列表想象成超市的货架，`spells[i]` 是第 *i* 件商品的重量，`potions[j]` 是第 *j* 种包装盒的承重。我们要把每件商品尝试放进每个包装盒，看看能否“装得下”（乘积 ≥ success）。  
- **为什么正确**：因为我们枚举了所有可能的配对，凡是符合条件的都会被统计到。没有遗漏，也没有多余的判断。  

#### 代码（Python）  

```python
from typing import List

def successfulPairs_bruteforce(spells: List[int],
                               potions: List[int],
                               success: int) -> List[int]:
    n = len(spells)
    m = len(potions)
    ans = [0] * n                     # 用来保存每个 spell 的答案

    for i in range(n):                # 对每个 spell
        cnt = 0
        for j in range(m):            # 与每个 potion 配对
            if spells[i] * potions[j] >= success:   # 判断是否成功
                cnt += 1
        ans[i] = cnt                  # 把计数写入答案数组
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`。  
  - 这里的 `n` 是 spells 的长度，`m` 是 potions 的长度。  
  - “O(n*m)” 可以理解为：如果 `n = 10⁵`，`m = 10⁵`，那么最坏情况下要做 10⁵ × 10⁵ = 10¹⁰ 次乘法和比较，计算量是天文数字，几乎不可能在几秒内跑完。  
- **空间复杂度**：`O(1)`（不计返回数组的空间）。  
  - 只用了常数个额外变量 `cnt`、`ans`（答案数组本身是必须的），不随输入规模增长而增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每个 spell 都要遍历所有 potion**，导致 `n*m` 次乘法。我们需要把 “遍历所有 potion” 这一步变得更快。  

观察题目提示：  

> 如果某个 potion 与当前 spell 配对成功，那么 **所有更强的 potion**（数值更大的）也一定成功。  

这说明 **成功的 potion 在有序数组中是一个连续的后缀**。因此，对每个 spell，只要找到 **最小的满足条件的 potion**，其右侧的所有 potion 都一定成功。  

要利用这个性质，我们可以：

1. **先把 potions 排序**（升序）。排序一次，时间 `O(m log m)`。  
2. 对每个 spell，**二分查找**（binary search）在已排序的 potions 中找到第一个满足 `spell * potion >= success` 的位置 `idx`。  
   - 二分查找的时间是 `O(log m)`。  
   - 找到 `idx` 后，成功的 potion 数量就是 `m - idx`（因为从 `idx` 到数组末尾都是成功的）。  
3. 把每个 spell 的答案存入返回数组。  

二分查找的核心是 “在有序数组里快速定位”。可以把它类比成在字典里查单词：字典是排好序的，先看中间的页码，如果目标在左边就往左继续，一直把范围缩小到只剩下目标所在的那一页。

**为什么正确**：  
- 排序后，所有 potion 按强度从小到大排列。  
- 对于固定的 `spell`，乘积随 potion 增大而单调不降。  
- 因此满足 `spell * potion >= success` 的 potion 集合是一个后缀区间，二分一定能找到左端点。  

#### 代码（Python）  

```python
from bisect import bisect_left
from typing import List

def successfulPairs(spells: List[int],
                    potions: List[int],
                    success: int) -> List[int]:
    # 1. 把 potions 排序，后面会用二分查找
    potions.sort()                       # O(m log m)

    m = len(potions)
    ans = []

    for s in spells:                     # 对每个 spell
        # 2. 计算使乘积 >= success 所需的最小 potion 值
        #    即: potion >= ceil(success / s)
        #    为了避免浮点数，使用整数除法 + 判断余数
        need = (success + s - 1) // s    # 向上取整，等价于 math.ceil(success / s)

        # 3. 在已排序的 potions 中二分找第一个 >= need 的位置
        idx = bisect_left(potions, need) # O(log m)

        # 4. 成功的 potion 数量是后缀长度
        ans.append(m - idx)               # O(1)

    return ans
```

> **代码说明**  
> - `potions.sort()`：把药水从弱到强排好，类似把字典按字母顺序排好。  
> - `need = (success + s - 1) // s`：求 `ceil(success / s)`，即**至少**需要多大的 potion 才能让乘积达标。  
> - `bisect_left(potions, need)`：二分查找第一个 **不小于** `need` 的位置。  
> - `m - idx`：从该位置到数组末尾的药水全都满足条件。

#### 复杂度  

- **时间复杂度**：`O(m log m + n log m)`。  
  - `m log m` 用于一次性排序。  
  - 对每个 `spell`（共 `n` 个）做一次二分查找，`log m` 次比较。  
  - 相比暴力的 `O(n*m)`，这里的 `log m` 只是一位数的几次比较，极大降低了运算量。  
- **空间复杂度**：`O(1)`（不计排序时原地修改列表的额外空间）。  
  - 只用了常数个额外变量 `need`、`idx`、`ans`（答案数组本身必须返回）。  

---

## 心得  

- **核心技巧**：利用单调性 + 排序 + 二分查找，把 “遍历全部” 转化为 “定位左端点”。  
- **适用的题型**：  
  1. “统计满足某个阈值的元素个数”——如 **Number of Pairs With Absolute Difference K**（利用排序+二分）  
  2. “最小/最大满足条件的子数组”——如 **Minimum Size Subarray Sum**（滑动窗口）  
  3. “每个查询求 >= 某值的元素数量”——如 **K-Query**（离线排序+树状数组）  
- **一句话总结**：**把“所有”压缩成“最左边的一个”，其右侧自然全部满足**。

---

## 反思  

- **第一反应**：看到“乘积 >= success”，立刻想到枚举所有配对（暴力）。  
- **最容易踩的坑**：  
  - **整数除法取整**：直接用 `success // s` 会把阈值向下取整，导致漏掉恰好等于 `success` 的情况，需要使用向上取整 `(success + s - 1) // s`。  
  - **溢出**：在某些语言中 `spell * potion` 可能超过 32 位整数范围，但 Python 的整数是大数，故不必担心。  
  - **边界**：当 `need` 大于所有 potion 时，`bisect_left` 返回 `m`，此时答案应为 `0`（`m - m = 0`），代码已正确处理。  
- **下次类似题**，第一步应该先 **检查单调性**（乘积随 potion 增大是否单调），如果成立，就考虑 **排序 + 二分**（或滑动窗口）来快速定位阈值。