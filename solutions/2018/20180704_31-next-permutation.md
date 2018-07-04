# #31. 下一个排列 / Next Permutation

> 难度：中等 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/next-permutation/)

---

## 题目（英文原版）

**Description**

A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).
Given an array of integers nums, find the next permutation of nums.
The replacement must be in place and use only constant extra memory.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: [1,3,2]
```

**Example 2:**

```
Input: nums = [3,2,1]
Output: [1,2,3]
```

**Example 3:**

```
Input: nums = [1,1,5]
Output: [1,5,1]
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

---

## 题目（中文翻译）

一个整数数组的**排列（permutation）**是指将其成员重新组织成一个序列或线性顺序。  
数组的**下一个排列**是指该数组在字典序（lexicographical order）上紧随当前排列的下一个更大的排列。更形式化地说，如果把所有可能的排列按照字典序排序，那么该数组的下一个排列就是在已排序序列中紧跟在它后面的那个排列。如果不存在这样的更大排列，则需要将数组重新排列成字典序最小的顺序（即升序排列）。

给定整数数组 `nums`，求 `nums` 的下一个排列。要求**原地**修改数组，且只能使用 **O(1)** 的额外空间。

**示例**

```text
示例 1:
输入: nums = [1,2,3]
输出: [1,3,2]

示例 2:
输入: nums = [3,2,1]
输出: [1,2,3]

示例 3:
输入: nums = [1,1,5]
输出: [1,5,1]
```

**约束条件**

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的排列** 都列举出来，按照字典序（词典顺序）排序，然后在排序后的序列里找到当前数组所在的位置，返回它后面的那个排列。如果已经是最后一个排列（即字典序最大的），就返回最小的排列（升序排列）。

- **数据结构**：  
  - **列表** 用来存放每一种排列，就像我们把所有单词写在纸上。  
  - **集合/哈希表**（可选）可以帮助我们快速判断是否已经产生过某个排列，类似于查字典：单词是 key，出现过与否是 value。  

- **为什么正确**：  
  按照题意，“下一个排列”就是在全部排列按字典序排好后，紧跟在当前排列后面的那个。因此只要完整列举并排序，就一定能得到正确答案。

- **时间/空间复杂度**：  
  - 对长度为 `n` 的数组，所有排列的数量是 `n!`（阶乘），这会导致 **时间复杂度 O(n!·n)**（每个排列还要拷贝一次），可以把 `n!` 想象成“从 1 到 n 连乘的结果”，即使 `n=10` 也已经是 3,628,800 种可能，远远超过普通电脑能在一秒内完成的操作数。  
  - **空间复杂度 O(n!·n)**，因为要把所有排列都存到内存里，就像把每本书的每一页都复印一遍，纸张会用爆。

显然，这种暴力做法只能用于学习和验证思路，实际面试或在线评测中会因为超时或内存超限而不被接受。

#### 代码（Python）

```python
import itertools

def next_permutation_bruteforce(nums):
    """暴力解：生成所有排列并排序，返回下一个排列（原地修改）"""
    # 1. 生成所有排列（itertools.permutations 会返回元组）
    all_perm = list(itertools.permutations(nums))
    # 2. 按字典序排序（元组本身支持比较）
    all_perm.sort()
    # 3. 找到当前排列所在的位置
    cur = tuple(nums)
    idx = all_perm.index(cur)
    # 4. 若已经是最后一个，返回最小的排列（升序）
    if idx == len(all_perm) - 1:
        next_perm = list(all_perm[0])
    else:
        next_perm = list(all_perm[idx + 1])
    # 5. 原地修改输入列表
    nums[:] = next_perm
    return nums
```

#### 复杂度

- **时间复杂度**：`O(n!·n)`  
  - `n!` 是所有排列的数量，`n` 是把元组转回列表的开销。可以把它想成“先把所有可能的钥匙都做一遍，再一个个试”。  
- **空间复杂度**：`O(n!·n)`  
  - 需要把每一种排列都存下来，类似于把所有钥匙的复制品都放进抽屉。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**，这一步根本不需要做。我们只要在 **局部** 找到可以让字典序变大的最小改动即可。下面一步步推导出 O(n) 的原地算法：

1. **从右往左寻找“下降点”**  
   - 从数组最右侧开始往左走，找到第一个 `nums[i] < nums[i+1]` 的位置 `i`。  
   - 这一步的意义：`i` 右侧的子数组已经是 **非递增**（从大到小）了，换句话说它已经是当前字典序的最大排列，不能再让它更大，只能在左侧寻找可以提升的地方。  
   - 如果整个数组都是非递增的（比如 `[3,2,1]`），说明已经是最大排列，需要整体翻转成最小排列（升序）。

2. **在右侧找到比 `nums[i]` 稍大的数**  
   - 再次从右侧往左走，找到第一个满足 `nums[j] > nums[i]` 的 `j`。因为右侧是从大到小的，这个 `j` 正好是 **最小的比 `nums[i]` 大的数**，换成它后，字典序的提升幅度最小。

3. **交换 `i` 与 `j`**  
   - 交换后，左侧保持不变，`i` 位置的数变大，整体字典序已经比原来大了。

4. **把 `i` 右侧的子数组翻转（逆序）**  
   - 交换后，`i` 右侧仍然是非递增的，但我们需要让它变成 **最小的排列**，才能得到 “下一个” 而不是 “更大的”。把它逆序（即升序）即可。

> **类比**：想象你手里有一串递增的数字牌（从左到右），要找出比当前组合稍大的下一个组合。先在右边找第一个可以“向上升级”的牌（下降点），再在右侧找最接近的更大的牌换过去，最后把右侧的牌重新排成最小的顺序，就像把右边的牌重新整理成最紧凑的排列。

整个过程只遍历了数组几次，时间是线性的，且只用了常数级的额外变量（`i, j, temp`），满足“原地、常数额外空间”的要求。

#### 代码（Python）

```python
def next_permutation(nums):
    """
    O(n) 原地算法，求数组的下一个字典序排列。
    只使用常数额外空间。
    """
    n = len(nums)
    if n <= 1:
        return  # 长度为 0/1 时本身就是唯一排列

    # 1. 从右往左找第一个 nums[i] < nums[i+1] 的位置
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:                     # 说明存在可以提升的位置
        # 2. 再次从右往左找第一个比 nums[i] 大的数
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # 3. 交换 nums[i] 与 nums[j]
        nums[i], nums[j] = nums[j], nums[i]

    # 4. 逆转 i 右侧的子数组，使其成为最小排列
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    # 函数直接修改 nums，无需返回值
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只需要最多两次线性遍历（一次找下降点，一次逆序子数组），相当于“看一遍数组”。与暴力解的 `n!` 相比，几乎是 **指数级** 的提升。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量 `i, j, left, right`，不随输入规模增长，正好满足“常数额外内存”。

---

## 心得

- **核心技巧**：**从右往左寻找下降点 + 逆序子数组**，这是一种“局部最小改动”策略，常用于求字典序下一个排列或下一个更大的数。  
- **适用的题型**：  
  1. **下一个排列**（本题）  
  2. **寻找字典序第 K 小的排列**（需要多次使用相同的思路）  
  3. **把数字拆成下一个更大的数**（如把整数 `123` 看作数组 `[1,2,3]`）  
- **一句话总结**：  
  “在右侧找到第一个可以让整体升高的位，换成最接近的更大数，然后把右侧最小化。”

## 反思

- **第一反应**：直接想到“枚举全部排列”。这虽然正确但不实际，说明对 “字典序” 的本质理解还不够深入。  
- **最容易踩的坑**：  
  - 忘记在整个数组都是非递增时要整体逆序（如 `[3,2,1]` → `[1,2,3]`）。  
  - 在寻找 `j` 时写成 `nums[j] < nums[i]`，导致换成更小的数，字典序不增。  
  - 逆序子数组时写成 “左移右移” 错位，导致数组不完整翻转。  
- **下次第一步**：先 **检查是否已经是最大排列**（即从右往左是否全是递减），如果是直接逆序；否则定位下降点 `i`，再继续后面的步骤。这样思路更清晰，也更不容易遗漏特殊情况。