# #2535. 数组的元素和与数字和之差 / Difference Between Element Sum and Digit Sum of an Array

> 难度：简单 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/difference-between-element-sum-and-digit-sum-of-an-array/)

---

## 题目（英文原版）

**Description**

You are given a positive integer array nums.
Return the absolute difference between the element sum and digit sum of nums.
Note that the absolute difference between two integers x and y is defined as |x - y|.

**Examples**

**Example 1:**

```
Input: nums = [1,15,6,3]
Output: 9
Explanation: 
The element sum of nums is 1 + 15 + 6 + 3 = 25.
The digit sum of nums is 1 + 1 + 5 + 6 + 3 = 16.
The absolute difference between the element sum and digit sum is |25 - 16| = 9.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 0
Explanation:
The element sum of nums is 1 + 2 + 3 + 4 = 10.
The digit sum of nums is 1 + 2 + 3 + 4 = 10.
The absolute difference between the element sum and digit sum is |10 - 10| = 0.
```

**Constraints**

- 1 <= nums.length <= 2000
- 1 <= nums[i] <= 2000

---

## 题目（中文翻译）

给定一个正整数数组 `nums`。

返回 `nums` 的元素和（element sum）与数字和（digit sum）之间的绝对差（absolute difference）。

**注意**，两个整数 `x` 与 `y` 的绝对差定义为 `|x - y|`。

## 示例

### 示例 1

**输入**  
`nums = [1,15,6,3]`

**输出**  
`9`

**解释**  
`nums` 的元素和为 `1 + 15 + 6 + 3 = 25`。  
`nums` 的数字和为 `1 + 1 + 5 + 6 + 3 = 16`（将每个整数的各位数字相加）。  
元素和与数字和的绝对差为 `|25 - 16| = 9`。

### 示例 2

**输入**  
`nums = [1,2,3,4]`

**输出**  
`0`

**解释**  
`nums` 的元素和为 `1 + 2 + 3 + 4 = 10`。  
`nums` 的数字和为 `1 + 2 + 3 + 4 = 10`。  
元素和与数字和的绝对差为 `|10 - 10| = 0`。

## 约束条件

- `1 <= nums.length <= 2000`
- `1 <= nums[i] <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题最直接的想法其实只有两件事：

1. **求元素和**（element sum）：把数组里每个整数直接相加。  
   - 用的结构就是普通的 `list`（数组），遍历一次把每个数累加即可。  
   - 这一步可以类比为把购物车里的商品价格全部加起来，得到总价。

2. **求数字和**（digit sum）：把数组里每个整数拆成**每一位数字**再相加。  
   - 拆位可以想象成把一本书的页码拆成每一位数字，然后把所有位数相加。  
   - 实现方式有两种常见的“字典”类比：  
     - 把整数转成字符串，像查字典一样逐字符取出每位数字。  
     - 或者用数学的“取模除法”，不断 `num % 10` 取出最低位，再 `num //= 10` 去掉最低位。  

这两步算完后，用 `abs(element_sum - digit_sum)` 计算绝对差即可。  

**为什么正确？**  
- 元素和是题目要求的“element sum”。  
- 拆位后把所有数字相加，恰好是题目定义的“digit sum”。  
- 两者相减后取绝对值，符合题目对 “absolute difference” 的定义。

#### 代码（Python）

```python
from typing import List

def differenceOfSum(nums: List[int]) -> int:
    # ---------- 1. 计算元素和 ----------
    element_sum = 0
    for num in nums:
        element_sum += num               # 把每个整数累加进 element_sum

    # ---------- 2. 计算数字和 ----------
    digit_sum = 0
    for num in nums:
        # 方法一：把整数转成字符串，再逐字符转回整数
        # for ch in str(num):
        #     digit_sum += int(ch)

        # 方法二：数学取模除法（更高效一点）
        while num > 0:
            digit_sum += num % 10        # 取出最低位数字
            num //= 10                   # 去掉最低位

    # ---------- 3. 绝对差 ----------
    return abs(element_sum - digit_sum)
```

#### 复杂度

- **时间复杂度**：`O(N * D)`  
  - `N` 是数组长度（最多 2000），`D` 是每个数的位数（`nums[i] ≤ 2000`，最多 4 位）。  
  - 大白话：我们要遍历每个数一次（`N` 次），对每个数再把它的每一位数字看一遍（最多 `D` 次），所以总工作量是两者的乘积。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量来累计和，没有额外随 `N` 增长的存储。  
  - 大白话：不管数组多大，程序占用的额外内存几乎不变。

---

### 2. 最优解

#### 思路  

对这道题来说，**暴力解已经是最优的**，因为：

- 计算元素和只能遍历一次，无法再快；  
- 计算数字和必须检查每一位数字，位数的上限是常数（4 位），也没有更快的办法。  

唯一可以“优化”的点是**实现方式**的细节：

| 方式 | 代码可读性 | 实际运行速度 |
|------|-----------|--------------|
| 把整数转成字符串再遍历字符 | ★★★★★（直观） | ★★☆☆☆（会产生额外的字符串对象） |
| 数学取模除法 (`% 10`, `// 10`) | ★★★★☆（稍微晦涩） | ★★★★★（只用整数运算） |

因此我们把 **最优解** 定义为 **仅使用整数运算的实现**，它在时间上与暴力思路等价，但在常数因子上更好。

#### 代码（Python）

```python
from typing import List

def differenceOfSum(nums: List[int]) -> int:
    element_sum = 0
    digit_sum = 0

    for num in nums:
        element_sum += num          # 累加元素本身

        # 只用整数运算把每位数字拆出来并累计
        tmp = num
        while tmp > 0:
            digit_sum += tmp % 10   # 取最低位
            tmp //= 10              # 去掉最低位

    return abs(element_sum - digit_sum)
```

#### 复杂度

- **时间复杂度**：`O(N * D)`（同上）  
  - 与暴力解的时间复杂度相同，只是内部的常数更小。  
  - 对于本题的约束（`D ≤ 4`），实际运行几乎是线性 `O(N)`。

- **空间复杂度**：`O(1)`（同上）  
  - 只使用常数个额外变量。

---

## 心得

- **核心技巧**：**位数拆分**（digit extraction）——通过 `% 10` 与 `// 10` 把整数逐位拆开。  
- **适用的题型**：  
  1. 统计数组中所有数字的**数字和**（如 LeetCode 1977）。  
  2. 判断一个数是否满足“**各位数字之和**”的某种条件（如 2585. 子数组和分离）。  
  3. 需要把数值转化为**每位字符**进行统计或比较的题目（如回文数判断）。  
- **一句话总结解题钥匙**：**“遍历数组 + 整数取模拆位”**，简单直接、永远不会错。

## 反思

- **第一反应**：直接把题目要求拆成两步——求元素和、求数字和，再相减。  
- **最容易踩的坑**：  
  - **忘记处理数字 0**：虽然本题 `nums[i] ≥ 1`，但如果出现 0，需要在 `while` 循环外单独加一次 `0`（或直接 `while tmp:`）。  
  - **溢出**：Python 的整数不溢出，但在某些语言需要注意累计和的范围。  
  - **字符串方法的额外开销**：把整数转成字符串会产生临时对象，虽然不影响正确性，却会让运行时间略增。  
- **下次遇到同类题**，第一步应该想到：**“我要把每个数的每一位拿出来”**，于是立刻决定使用 `% 10` 与 `// 10` 的位拆分技巧。