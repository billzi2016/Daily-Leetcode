# #1502. 能否通过重新排列得到等差数列 / Can Make Arithmetic Progression From Sequence

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence/)

---

## 题目（英文原版）

**Description**

A sequence of numbers is called an arithmetic progression if the difference between any two consecutive elements is the same.
Given an array of numbers arr, return true if the array can be rearranged to form an arithmetic progression. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: arr = [3,5,1]
Output: true
Explanation: We can reorder the elements as [1,3,5] or [5,3,1] with differences 2 and -2 respectively, between each consecutive elements.
```

**Example 2:**

```
Input: arr = [1,2,4]
Output: false
Explanation: There is no way to reorder the elements to obtain an arithmetic progression.
```

**Constraints**

- 2 <= arr.length <= 1000
- -106 <= arr[i] <= 106

---

## 题目（中文翻译）

**描述**  
如果一个数列中任意两个相邻元素的差值相同，则称该数列为等差数列（arithmetic progression）。  
给定一个整数数组 `arr`，如果可以对其元素进行重新排列，使其形成等差数列，则返回 `true`；否则返回 `false`。

**示例**  

**示例 1**  
```text
Input: arr = [3,5,1]
Output: true
Explanation: 我们可以将元素重新排列为 [1,3,5]（差值为 2）或 [5,3,1]（差值为 -2），相邻元素的差值均相同。
```

**示例 2**  
```text
Input: arr = [1,2,4]
Output: false
Explanation: 无法通过任何排列方式使其成为等差数列。
```

**约束条件**  

- `2 <= arr.length <= 1000`
- `-10^6 <= arr[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组的所有排列全部枚举出来，逐个检查每个排列是否满足“相邻两个数的差相等”。  
- **数据结构**：我们可以把数组的每一种排列看成一本“字典”，每一页（即一种排列）记录了数字的顺序。枚举排列的过程类似于把所有单词都查一遍字典。
- **正确性**：如果数组真的可以被重新排列成等差数列，那么在所有可能的排列中必然会出现这样一个排列。遍历所有排列自然能找到它。
- **复杂度**：  
  - 枚举排列的数量是 `n!`（n 的阶乘），因为第一个位置有 n 种选择，第二个位置有 n‑1 种，依此类推。  
  - 对每一种排列，我们要遍历一次数组来比较相邻差值，耗时 O(n)。  
  - 所以总时间是 O(n! × n)，对任何稍大的 n（比如 10 以上）都不可接受。  
  - 额外空间只需要保存当前排列，最多 O(n)。

> **大白话**：`O(n! )` 可以想象成“把所有可能的排队方式都试一遍”，即使是 6 个人排队也有 720 种可能，人数再多就像天文数字一样，根本不可能在电脑里跑完。

#### 代码（Python）

```python
import itertools
from typing import List

def can_make_arith_seq_brute(arr: List[int]) -> bool:
    """
    暴力枚举所有排列，检查是否存在等差数列
    """
    # itertools.permutations 会产生所有可能的排列，类似把每一种排队方式拿出来
    for perm in itertools.permutations(arr):
        # 计算首两个数的差值，作为等差数列的公差
        diff = perm[1] - perm[0]
        # 检查后面的每一对相邻元素差是否都等于 diff
        ok = True
        for i in range(2, len(perm)):
            if perm[i] - perm[i - 1] != diff:
                ok = False
                break
        if ok:                     # 找到一组满足条件的排列，直接返回 True
            return True
    return False                  # 所有排列都不符合，返回 False
```

#### 复杂度  

- **时间复杂度**：`O(n! × n)`  
  - “n!” 表示所有排列的数量，乘以 `n` 是因为每个排列要遍历一次。对 n=10 已经是 3.6 百万 × 10 ≈ 3.6 千万次操作，已经很慢了。
- **空间复杂度**：`O(n)`  
  - 只保存当前遍历到的排列，最多占用与原数组等长的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有排列是最耗时的**，因为我们把“所有可能”都尝试了一遍。其实我们可以利用等差数列本身的一个重要特性：**只要把数列排好序（升序或降序），相邻差就一定相等**。  

**为什么排序就足够？**  
- 假设有一组数能够组成等差数列，记公差为 `d`。把这组数从小到大排好序后，仍然是同样的数，只是顺序变成了递增。递增顺序下相邻两个数的差仍然是 `d`（如果原来是递减，则差是 `-d`，但我们只关心绝对值是否相等）。  
- 因此，只要把数组排序好，只需要检查一次相邻差是否相等，就能判断是否可以排列成等差数列。

**实现步骤**  
1. **排序**：使用 Python 内置的 `sorted`（时间 O(n log n)），把数组从小到大排好序。可以把它想象成把所有数字排成一列，从左到右依次增大，就像把书按页码从小到大摆放。  
2. **计算公差**：`diff = sorted_arr[1] - sorted_arr[0]`，即前两个数的差。  
3. **遍历检查**：从下标 2 开始，依次比较 `sorted_arr[i] - sorted_arr[i-1]` 是否等于 `diff`。如果有任何一次不相等，就说明不能形成等差数列。  
4. **返回结果**：全部相等则返回 `True`，否则 `False`。

**核心算法/数据结构**  
- **排序**（Sorting）：一种把数据按大小顺序重新排列的操作，时间复杂度是 `O(n log n)`，在大多数语言里都有高度优化的实现。  
- **遍历**（Linear Scan）：一次线性遍历，用来检查相邻差是否相等，时间是 `O(n)`。

**类比**：把等差数列想象成一条“等间距的楼梯”。只要把所有楼梯的高度（数字）排好序，检查每一步的高度差是否相同，就能确认这条楼梯是否真的等间距。

#### 代码（Python）

```python
from typing import List

def can_make_arith_seq(arr: List[int]) -> bool:
    """
    最优解：先排序，再检查相邻差是否相等
    """
    # 1. 排序，O(n log n)
    arr_sorted = sorted(arr)          # 把数组从小到大排成一列

    # 2. 计算公差（前两个数的差），如果数组只有两个元素，这一步已经足够
    diff = arr_sorted[1] - arr_sorted[0]

    # 3. 线性遍历检查后面的每一对相邻元素
    for i in range(2, len(arr_sorted)):
        # 如果发现任意一对相邻元素的差不等于 diff，就直接返回 False
        if arr_sorted[i] - arr_sorted[i - 1] != diff:
            return False

    # 4. 所有相邻差都相等，说明可以组成等差数列
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `sorted` 需要 `n log n` 次比较（类似把 n 本书按照字母顺序排好需要的时间），随后一次线性遍历 `O(n)`，整体仍是 `O(n log n)`。相比暴力的 `n!`，这已经是天壤之别，几乎在所有合法输入范围内都能毫秒级完成。  
- **空间复杂度**：`O(n)`（或 `O(1)` 视实现而定）  
  - `sorted` 会创建一个新列表，长度为 `n`，所以需要额外的 `O(n)` 空间。如果使用原地排序（如 `arr.sort()`），则可以把空间降到 `O(1)`（只用常数级的临时变量）。

---

## 心得

- **核心技巧**：**先排序再检查等差**。等差数列的“相邻差相等”在排序后只需要一次遍历即可验证。  
- **适用的题型**：  
  1. 判断一组数能否构成等差数列（本题）。  
  2. 判断一组数能否构成等比数列（思路类似，检查相邻比值是否相等）。  
  3. 检查数组是否已经是等差/等比序列（直接遍历，无需排序）。  
- **一句话总结解题钥匙**：*“等差数列在有序状态下最容易看出规律”*。

---

## 反思

- **第一反应**：看到“可以重新排列”，立刻想到要尝试所有排列（暴力搜索），因为没有立刻想到“有序”会简化问题。  
- **最容易踩的坑**：  
  - 忘记对数组进行排序直接比较相邻差，导致错误的 `False` 结果（例如 `[5,1,3]`）。  
  - 当数组长度只有 2 时，任何两个数都能构成等差数列，需直接返回 `True`（实现中自然满足）。  
  - 负数和大数的范围不会影响算法，但要注意 Python 整数不会溢出。  
- **下次遇到同类题**：第一步就想“是否有一种自然的顺序（排序）可以把问题转化为线性检查”，再决定是否需要排序或其他预处理。这样可以立刻跳过指数级的暴力搜索，直接走向 `O(n log n)` 或更优的解法。