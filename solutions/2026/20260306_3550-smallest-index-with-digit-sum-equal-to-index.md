# #3550. 数字和等于下标的最小索引 / Smallest Index With Digit Sum Equal to Index

> 难度：简单 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/smallest-index-with-digit-sum-equal-to-index/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Return the smallest index i such that the sum of the digits of nums[i] is equal to i.
If no such index exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2]
Output: 2
Explanation:
```

**Example 2:**

```
Input: nums = [1,10,11]
Output: 1
Explanation:
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: -1
Explanation:
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`。  
返回满足 `nums[i]` 的各位数字之和（digit sum）等于下标 `i` 的最小下标 `i`。  
如果不存在这样的下标，返回 `-1`。

示例 1:
``` 
Input: nums = [1,3,2]
Output: 2
解释：
```

示例 2:
``` 
Input: nums = [1,10,11]
Output: 1
解释：
```

示例 3:
``` 
Input: nums = [1,2,3]
Output: -1
解释：
```

约束条件：
- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的要求非常直接：**遍历数组**，找出第一个下标 `i`，使得 `nums[i]` 的各位数字之和等于 `i`。  
我们可以把它想象成在一本电话号码簿里查找：“第几页（下标 i）对应的电话号码（nums[i]）的数字之和恰好等于页码”。  
实现时只需要两件事：

1. **遍历**：从下标 `0` 开始逐个检查，最先满足条件的就是答案（因为要最小的下标）。  
2. **计算数字和**：把一个整数拆成个位、十位、百位…逐个相加。可以用 `while n > 0: sum += n % 10; n //= 10`，这就像把数字拆成“每一块砖”，一块块累加。

只要遍历完都没有找到，就返回 `-1`。

> 为什么这个方法一定对？  
> 因为我们把**所有可能的下标**（即 `0 … len(nums)-1`）都检查了一遍，且检查顺序是从小到大，一旦找到就一定是最小的符合条件的下标。

#### 代码（Python）

```python
from typing import List

def digit_sum(x: int) -> int:
    """返回整数 x 的各位数字之和。"""
    s = 0
    while x:               # 当 x 不为 0 时循环
        s += x % 10        # 取最低位加入和
        x //= 10           # 去掉最低位
    return s

def smallest_index(nums: List[int]) -> int:
    """
    返回最小的下标 i，使得 nums[i] 的各位数字之和等于 i；
    若不存在则返回 -1。
    """
    for i, val in enumerate(nums):   # 按下标顺序遍历
        if digit_sum(val) == i:      # 判断数字和是否等于下标
            return i                 # 找到首个满足条件的下标，直接返回
    return -1                         # 全部遍历完也没找到
```

#### 复杂度

- **时间复杂度**：`O(n * d)`，其中 `n = len(nums)`，`d` 是 `nums[i]` 的位数（最多 4 位，因为 `0 ≤ nums[i] ≤ 1000`）。  
  用大白话说，就是“遍历数组一次，每个数最多看四次（因为最多四位）”。在本题的约束下，最坏也只有 `100 * 4 = 400` 次基本操作，几乎可以忽略不计。

- **空间复杂度**：`O(1)`——只用了常数个额外变量 (`s, i, val`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

对于本题，**暴力解已经是最优的**。  
唯一可以改进的地方是**把“计算数字和”这一步写得更简洁**，比如直接使用 Python 的字符串特性：

```python
digit_sum = lambda x: sum(int(ch) for ch in str(x))
```

这相当于把数字转换成字符数组，再把每个字符转回整数求和。时间复杂度仍是 `O(d)`，实现更短、更易读。  
因此我们把“最优解”写成 **一次遍历 + O(1) 额外空间** 的形式。

#### 代码（Python）

```python
from typing import List

def smallest_index_opt(nums: List[int]) -> int:
    """
    最优实现：一次遍历，使用 Python 的字符串技巧求数字和。
    """
    for i, val in enumerate(nums):
        # 将整数转成字符串，再把每个字符转成整数求和
        if sum(int(ch) for ch in str(val)) == i:
            return i
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n * d)`，和暴力解完全相同，只是实现更简洁。  
  这里的 `d` 仍然是数字的位数（最多 4），所以整体仍是线性时间。

- **空间复杂度**：`O(1)`（不计入 `str(val)` 临时字符串的常数空间），同样只用了常数级别的额外变量。

---

## 心得

- **核心技巧**：一次遍历 + 计算数字和。  
- **适用场景**：  
  1. “下标/位置 与 元素的某种属性相等” 的线性搜索题（如“找下标等于元素本身的下标”）。  
  2. 需要**对每个元素做 O(位数) 小计算** 的题目（如“判断数组中是否有元素的各位数字之和为奇数”）。  
  3. 任何**数组/列表的线性扫描**，只要判断条件不依赖于全局信息，都可以用类似思路。

- **一句话总结**：  
  “遍历 + 简单的局部计算”，是数组线性搜索题的万能钥匙。

---

## 反思

- **第一反应**：看到“下标 i”和“数字和相等”，立刻想到**逐个检查**，因为数组长度只有 100，直接遍历根本不会超时。  
- **最容易踩的坑**：  
  - 忘记 **下标从 0 开始**，导致把答案错位。  
  - 对 `0` 的数字和处理不当（`0` 的各位和应该是 `0`，而 `while x:` 会直接跳过循环，需要特别处理或使用 `str` 方法）。  
  - 没有考虑 **空数组**（本题约束 `len ≥ 1`，但实际写代码时最好防御性检查）。  
- **下次类似题的第一步**：  
  “先把题目条件写成‘遍历每个下标 i，检查某个函数 f(nums[i]) 是否等于 i’，然后实现 f 的计算”。这样思路清晰，代码也自然简洁。