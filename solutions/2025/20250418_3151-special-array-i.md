# #3151. 特殊数组 I / Special Array I

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/special-array-i/)

---

## 题目（英文原版）

**Description**

An array is considered special if the parity of every pair of adjacent elements is different. In other words, one element in each pair must be even, and the other must be odd.
You are given an array of integers nums. Return true if nums is a special array, otherwise, return false.

**Examples**

**Example 1:**

```
Input: nums = [1]
Output: true
Explanation:
There is only one element. So the answer is true .
```

**Example 2:**

```
Input: nums = [2,1,4]
Output: true
Explanation:
There is only two pairs: (2,1) and (1,4) , and both of them contain numbers with different parity. So the answer is true .
```

**Example 3:**

```
Input: nums = [4,3,1,6]
Output: false
Explanation:
nums[1] and nums[2] are both odd. So the answer is false .
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

一个数组（array）如果每一对相邻元素（adjacent element）的奇偶性（parity）都不同，则称该数组为特殊数组（special array）。换句话说，在每一对相邻元素中必须有一个是偶数（even），另一个是奇数（odd）。

给定一个整数数组（integer array）`nums`，如果 `nums` 是特殊数组则返回 `true`，否则返回 `false`。

**示例 1**  
**输入**: `nums = [1]`  
**输出**: `true`  
**解释**: 只有一个元素，所以答案为 `true`。

**示例 2**  
**输入**: `nums = [2,1,4]`  
**输出**: `true`  
**解释**: 仅有两对相邻元素：`(2,1)` 和 `(1,4)`，它们都包含奇偶性不同的数字。因此答案为 `true`。

**示例 3**  
**输入**: `nums = [4,3,1,6]`  
**输出**: `false`  
**解释**: `nums[1]` 与 `nums[2]` 均为奇数（odd），所以答案为 `false`。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把数组里每两个相邻的元素都拿出来比较一次**，只要发现有一对的奇偶性相同（即都是偶数或都是奇数），就立刻返回 `false`；如果所有相邻对的奇偶性都不相同，最后返回 `true`。  

- **用到的数据结构**：普通的 Python 列表（list），我们只需要遍历它，不需要额外的结构。可以把列表想象成一排排座位，**相邻的两个人** 就是我们要检查的“邻居”。  
- **为什么正确**：题目要求“每一对相邻元素的奇偶性必须不同”。只要把所有相邻的对全部检查一遍，确保每对都满足要求，整个数组自然就满足要求。  

**暴力实现的细节**：  
1. 用两层循环，外层遍历下标 `i`（从 `0` 到 `len(nums)-2`），内层固定比较 `nums[i]` 与 `nums[i+1]`。  
2. 判断奇偶性可以用取模运算 `x % 2`：余数为 `0` 表示偶数，余数为 `1` 表示奇数。  

#### 代码（Python）  

```python
def isSpecialArray_brute(nums):
    """
    暴力版：双层循环检查每一对相邻元素的奇偶性是否不同
    """
    n = len(nums)
    # 外层遍历每一个位置 i（除了最后一个，因为它没有右侧邻居）
    for i in range(n - 1):
        # 内层直接比较 i 与 i+1 的奇偶性
        # nums[i] % 2 得到 0（偶） 或 1（奇），相同则说明奇偶性相同
        if (nums[i] % 2) == (nums[i + 1] % 2):
            return False          # 只要有一对不符合，立刻返回 False
    return True                   # 全部检查完都符合，返回 True
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（因为用了两层循环，外层 `n` 次，内层常数次，严格来说是 `O(n)`，但如果把“比较每一对”写成嵌套循环，最坏会是 `O(n²)`，这里用来说明最直观的思路）。  
  - 大白话：如果数组有 1000 个元素，最多要检查 1000 × 1000 = 100 万次。  
- **空间复杂度**：`O(1)`，只用了几个临时变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解来看，**真正耗时的地方在于不必要的重复检查**。我们每次只需要比较相邻的两个人一次，根本不需要两层循环。于是可以把 **外层循环** 保留下来，**去掉内层循环**，一次遍历即可完成全部检查。  

- **瓶颈**：双层循环导致每对相邻元素被比较了很多次（虽然在本题里内层其实只比较一次，但从思考角度把它视作“可能的冗余”）。  
- **优化思路**：一次遍历（单指针）从左到右，**每走一步就比较当前元素和它左边的元素**。如果发现奇偶相同，立即返回 `false`，否则继续。遍历结束后仍未发现冲突，说明数组满足条件，返回 `true`。  

**核心概念——奇偶性**：  
- 偶数：能被 2 整除，`x % 2 == 0`。  
- 奇数：除以 2 余 1，`x % 2 == 1`。  
把奇偶性看成 “灯的开关”，偶数是红灯，奇数是绿灯，只要相邻两个灯颜色不同，整个道路就安全。

#### 代码（Python）  

```python
def isSpecialArray(nums):
    """
    最优解：单指针一次遍历检查相邻元素的奇偶性是否不同
    """
    # 从第二个元素开始（下标 1），因为要和前一个元素比较
    for i in range(1, len(nums)):
        # 如果当前元素和前一个元素奇偶性相同，直接返回 False
        if (nums[i] % 2) == (nums[i - 1] % 2):
            return False
    # 循环结束都没有冲突，说明数组是 special 的
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 大白话：数组长度是 10，就最多比较 9 次；长度是 100，就最多比较 99 次，随数组长度线性增长。  
- **空间复杂度**：`O(1)`。只用了常数个变量（循环计数器 `i`），不随输入大小变化。

---

## 心得  

- **核心技巧**：**一次遍历检查相邻元素的奇偶性**。这类“相邻关系”题目几乎都可以用线性扫描解决。  
- **适用的题型**：  
  1. 判断数组是否交替出现正负数（正负交替）。  
  2. 判断字符串是否交替出现元音和辅音。  
  3. 判断链表节点值是否交替升序/降序。  
- **解题钥匙**：**把“相邻”转化为“前后比较”，用单指针一次遍历**。

---

## 反思  

- **第一反应**：看到“相邻元素奇偶不同”，立刻想到逐对检查。  
- **最容易踩的坑**：  
  - 忘记处理只有一个元素的情况（此时应直接返回 `True`）。  
  - 使用 `==` 判断奇偶性时写反了（比如写成 `!=`）。  
  - 对空数组没有考虑（虽然题目保证长度 ≥ 1）。  
- **下次第一步**：先确认“相邻关系”是否可以用一次线性扫描解决，如果可以，就直接写出“遍历 + 前后比较”的框架。