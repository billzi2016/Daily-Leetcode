# #3551. 按数字和排序的最少交换次数 / Minimum Swaps to Sort by Digit Sum

> 难度：中等 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-swaps-to-sort-by-digit-sum/)

---

## 题目（英文原版）

**Description**

You are given an array nums of distinct positive integers. You need to sort the array in increasing order based on the sum of the digits of each number. If two numbers have the same digit sum, the smaller number appears first in the sorted order.
Return the minimum number of swaps required to rearrange nums into this sorted order.
A swap is defined as exchanging the values at two distinct positions in the array.

**Examples**

**Example 1:**

```
Input: nums = [37,100]
Output: 1
Explanation:
```

**Example 2:**

```
Input: nums = [22,14,33,7]
Output: 0
Explanation:
```

**Example 3:**

```
Input: nums = [18,43,34,16]
Output: 2
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- nums consists of distinct positive integers.

---

## 题目（中文翻译）

**题目描述**  
给定一个由互不相同的正整数构成的数组 `nums`。需要按照每个数字的数字和（digit sum）从小到大对数组进行排序；若两个数字的数字和相同，则数值较小的数字排在前面。返回将 `nums` 重排为上述顺序所需的最少交换次数。  
交换（swap）指的是将数组中两个不同位置的值互换。

**示例**

**示例 1**  
Input: `nums = [37,100]`  
Output: `1`  
解释：

**示例 2**  
Input: `nums = [22,14,33,7]`  
Output: `0`  
解释：

**示例 3**  
Input: `nums = [18,43,34,16]`  
Output: `2`  
解释：

**约束条件**  

- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `nums` 由互不相同的正整数构成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次遍历一次**，把数组里每个数的**数位和**算出来，然后**直接对整个数组进行排序**（把数位和当作第一关键字，数值本身当作第二关键字），得到目标排列。  
随后我们可以**模拟**一次次的交换：每次把当前位置的元素和它在目标位置应该出现的元素交换，直到整个数组和目标数组完全相同为止。

- **使用的数据结构**  
  - `list`（列表）保存原数组。  
  - `list` 保存排好序的目标数组。  
  - `dict`（哈希表）把「数值 → 目标下标」存起来，哈希表就像一本**词典**，单词是键（这里是数字），页码是值（这里是它在排好序后应该出现的下标），查找是 **O(1)** 的。

- **为什么正确**  
  只要我们把每个位置的元素换到它在目标数组里的位置，最终一定会得到目标数组。因为所有数字都是**互不相同**，每个数字只有唯一的目标下标。

- **时间/空间复杂度**  
  - 计算每个数的数位和需要遍历每个数字的每一位，最坏情况是 `log10(10^9) ≈ 9` 位，算作常数。  
  - 对 `n` 个元素进行**一次完整的排序**，排序的时间复杂度是 `O(n log n)`。  
  - 然后我们用**两层循环**模拟交换：外层遍历 `n` 次，内层在最坏情况下也可能遍历 `n` 次（因为每次都要在哈希表里找目标位置），所以**暴力模拟的时间复杂度是 `O(n^2)`**。  
  - 空间上我们额外用了一个目标数组和一个哈希表，都是 `O(n)` 的大小。

> **大白话**：  
> - `O(n log n)` 就像把 `n` 本书排好顺序需要 `log n` 轮比较，每轮比较 `n` 本书。  
> - `O(n^2)` 就像每本书都要找一次它的正确位置，最坏情况下要找 `n` 次，整体就是 `n` 乘 `n`。

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """计算整数 x 的各位数字之和，例如 37 -> 3+7=10"""
    s = 0
    while x:
        s += x % 10          # 取最右边一位
        x //= 10             # 去掉最右边一位
    return s


def min_swaps_bruteforce(nums):
    n = len(nums)

    # 1. 生成目标数组：先按数位和升序，再按数值升序
    target = sorted(nums, key=lambda x: (digit_sum(x), x))

    # 2. 建立「数值 → 目标下标」的映射，类似查字典
    pos_in_target = {val: idx for idx, val in enumerate(target)}

    swaps = 0
    nums = nums[:]                 # 复制一份，防止修改原数组
    for i in range(n):
        # 当前元素已经在正确位置，继续
        if nums[i] == target[i]:
            continue

        # 需要把 nums[i] 换到它的目标位置
        correct_val = target[i]               # 当前位置应该出现的值
        j = pos_in_target[nums[i]]             # nums[i] 在目标数组里的下标

        # 交换 nums[i] 与 nums[j]
        nums[i], nums[j] = nums[j], nums[i]
        swaps += 1

    return swaps
```

#### 复杂度

- **时间复杂度**：`O(n^2)`  
  - 解释：外层遍历 `n` 次，最坏情况下每次都要在哈希表里找一次目标下标（`O(1)`），但因为我们每次只做一次交换，整体仍然是 `O(n^2)`（两层遍历的乘积）。
- **空间复杂度**：`O(n)`  
  - 解释：额外存放目标数组 `target`（`n` 个元素）和映射表 `pos_in_target`（同样 `n` 条键值对），再加上复制的原数组。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于：我们一次次地“把错误的元素搬到正确位置”，但每搬一次只能纠正 **一个** 错误，而实际上**很多错误是互相交织在一起的**，形成了**环（cycle）**。  
如果我们把每个位置看成一个**节点**，它指向**该位置上元素在目标数组中的位置**，整个数组就构成了一个**置换（permutation）**。  
例如：

```
原数组:   [18, 43, 34, 16]
目标数组: [16, 18, 34, 43]   （按数位和排序后）
下标:      0   1   2   3
```

- 位置 0 的元素 18 在目标数组中下标是 1 → 0 → 1
- 位置 1 的元素 43 在目标数组中下标是 3 → 1 → 3
- 位置 3 的元素 16 在目标数组中下标是 0 → 3 → 0

于是我们得到一个环 **0 → 1 → 3 → 0**，环的长度是 3。**把一个环整理好只需要环长-1 次交换**（把环内的元素轮流搬到正确位置即可），而不是每次只搬一个元素。  

**关键结论**：  
- 整个置换可以分解为若干不相交的环。  
- 每个环长度为 `k`，最少需要 `k-1` 次交换。  
- 把所有环的 `(k-1)` 加起来得到答案。  

数学上，这等价于：

```
最小交换次数 = n - (环的个数)
```

因为所有环的长度之和恰好是 `n`，所以：

```
∑(k-1) = ∑k - ∑1 = n - (环的个数)
```

**实现步骤**  

1. **计算数位和并排序**，得到目标数组 `sorted_nums`（同暴力解）。  
2. **构建映射** `value -> target_index`（哈希表），方便快速定位。  
3. **把原数组映射成下标数组** `perm[i] = target_index_of(nums[i])`。此时 `perm` 是一个 **0~n-1 的排列**。  
4. **遍历 `perm`，统计环的数量**：  
   - 使用 `visited` 数组标记是否已经走过。  
   - 对每个未访问的下标 `i`，沿着 `perm` 前进直到回到起点，形成一个环。环计数 `cycles += 1`。  
5. **答案** `= n - cycles`。

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """返回整数 x 的数位和"""
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def min_swaps(nums):
    """
    返回把 nums 按「数位和升序、数值升序」排序所需的最少交换次数。
    思路：把问题转化为排列的环计数，答案 = n - 环的数量。
    """
    n = len(nums)

    # 1. 目标数组：先按数位和，再按数值
    sorted_nums = sorted(nums, key=lambda x: (digit_sum(x), x))

    # 2. 哈希表：数值 -> 目标下标
    target_index = {val: idx for idx, val in enumerate(sorted_nums)}

    # 3. 把原数组映射成「应该去的下标」的排列
    perm = [target_index[val] for val in nums]   # 例： [1,3,2,0]

    visited = [False] * n
    cycles = 0

    for i in range(n):
        if visited[i]:
            continue          # 已经属于某个已统计的环
        # 从 i 开始，沿着 perm 走一圈
        j = i
        while not visited[j]:
            visited[j] = True
            j = perm[j]       # 跳到下一个位置
        cycles += 1           # 完成一个环

    # 4. 公式：最少交换次数 = n - 环的数量
    return n - cycles
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 解释：排序占 `O(n log n)`，其余步骤（构建映射、遍历找环）都是线性 `O(n)`，所以整体受排序主导。  
  - 与暴力解相比，去掉了 `O(n^2)` 的模拟交换，速度提升显著，尤其在 `n` 接近上限 `10^5` 时尤为重要。

- **空间复杂度**：`O(n)`  
  - 解释：额外存放 `sorted_nums`、`target_index`、`perm`、`visited` 四个长度为 `n` 的数组/字典，总共 `O(n)` 的额外空间。

---

## 心得

- **核心技巧**：把“最小交换次数”问题转化为**置换的环计数**。  
- **适用场景**：  
  1. 任意需要把数组按某种顺序排列，求最少交换次数的题目（如 LeetCode 765 *Couples Holding Hands*）。  
  2. “把数组变成升序”或“变成特定排列”时，只要能得到目标下标映射，就可以用环计数。  
  3. 需要求最少 **adjacent swaps**（相邻交换）时，通常要用 **逆序对**，但若交换不要求相邻，环计数是最简洁的办法。  

- **一句话总结解题钥匙**：  
  > “把数组看成一个置换，最少交换次数 = 元素总数 - 环的个数”。  

---

## 反思

- **第一反应**：直接模拟交换，边走边改，代码容易写，但会超时。  
- **最容易踩的坑**：  
  - **数位和的计算**：忘记对每个数字都重新累加，导致错误答案。  
  - **环的计数**：遗漏已经访问的节点会导致重复计数，或者把单独已经在正确位置的元素算成环（实际上长度为 1 的环不需要交换）。  
  - **相等的数位和**：忘记再用原数值做 tiebreaker，导致排序顺序错误。  
- **下次遇到同类题**：第一步先**构造目标排列并把原数组映射成下标排列**，然后**统计置换中的环**，直接用 `n - cycles` 求答案。这样思路清晰，时间复杂度自然是 `O(n log n)`。