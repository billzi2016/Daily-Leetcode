# #1979. 数组中最小数和最大数的最大公约数 / Find Greatest Common Divisor of Array

> 难度：简单 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/find-greatest-common-divisor-of-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the greatest common divisor of the smallest number and largest number in nums.
The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.

**Examples**

**Example 1:**

```
Input: nums = [2,5,6,9,10]
Output: 2
Explanation:
The smallest number in nums is 2.
The largest number in nums is 10.
The greatest common divisor of 2 and 10 is 2.
```

**Example 2:**

```
Input: nums = [7,5,6,8,3]
Output: 1
Explanation:
The smallest number in nums is 3.
The largest number in nums is 8.
The greatest common divisor of 3 and 8 is 1.
```

**Example 3:**

```
Input: nums = [3,3]
Output: 3
Explanation:
The smallest number in nums is 3.
The largest number in nums is 3.
The greatest common divisor of 3 and 3 is 3.
```

**Constraints**

- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个整数数组 (integer array) `nums`，返回 `nums` 中最小数和最大数的最大公约数 (greatest common divisor)。  
两个数的最大公约数是能够整除这两个数的最大正整数。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**  

- `2 <= nums.length <= 1000`  
- `1 <= nums[i] <= 1000`

---

### 示例

**示例 1**  
Input: `nums = [2,5,6,9,10]`  
Output: `2`  
Explanation:  
最小的数是 `2`。  
最大的数是 `10`。  
`2` 和 `10` 的最大公约数是 `2`。

**示例 2**  
Input: `nums = [7,5,6,8,3]`  
Output: `1`  
Explanation:  
最小的数是 `3`。  
最大的数是 `8`。  
`3` 和 `8` 的最大公约数是 `1`。

**示例 3**  
Input: `nums = [3,3]`  
Output: `3`  
Explanation:  
最小的数是 `3`。  
最大的数是 `3`。  
`3` 和 `3` 的最大公约数是 `3`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：  
1. 先在数组里找出 **最小值** `mn` 和 **最大值** `mx`（这一步只要一次遍历）。  
2. 再在 **1 到 `mn`** 之间的所有整数中，找出能同时整除 `mn` 和 `mx` 的最大数。  

这里可以把 **哈希表** 想象成一本词典，`key` 是单词，`value` 是页码。  
而 **遍历 1~mn 的过程**，就像我们从第 1 页一直翻到第 `mn` 页，检查每一页的编号是否能“配得上”这两个数——如果能，就记下来，最后留下最大的那个页码。  

这种做法一定能得到正确答案，因为**最大公约数**（Greatest Common Divisor, GCD）必然是 **小于等于最小数** 的整数，只要把所有可能的整数都试一遍，最大的满足条件的那个就是答案。  

#### 代码（Python）  

```python
from typing import List

def findGCD(nums: List[int]) -> int:
    # ---------- 第一步：一次遍历找到最小值和最大值 ----------
    mn = float('inf')   # 初始设为正无穷，后面会被任何实际数值覆盖
    mx = float('-inf')  # 初始设为负无穷，同理
    for x in nums:
        if x < mn:
            mn = x
        if x > mx:
            mx = x

    # ---------- 第二步：从 mn 开始往下枚举可能的公约数 ----------
    # 从大到小枚举，这样第一个符合条件的就是最大公约数，直接返回
    for d in range(mn, 0, -1):          # d 依次是 mn, mn-1, ..., 1
        if mn % d == 0 and mx % d == 0: # 同时能整除 mn 和 mx
            return d                    # 找到最大公约数，结束函数
    # 理论上这里永远不会走到，因为 1 总是公约数
    return 1
```

#### 复杂度  
- **时间复杂度**：`O(n + mn)`  
  - 第一次遍历数组找最小/最大是 `O(n)`（`n` 是数组长度）。  
  - 第二步最多要检查 `mn` 次（`mn` ≤ 1000），所以是 `O(mn)`。  
  - 用大白话说，就是“先找一次宝藏（遍历数组），再在宝藏的大小范围里逐个尝试钥匙（枚举可能的公约数）”。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`mn`, `mx`, `d`），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  
从暴力解可以看出，**慢的地方在第二步**：我们把 1~`mn` 的所有数都试了一遍。  
实际上，**求两个数的最大公约数** 有一个非常古老而高效的算法——**欧几里得算法**（又叫辗转相除法），它的核心思想是：

> 两个数的最大公约数等于 **较大数** 对 **较小数** 取余后的 **余数** 与 **较小数** 的最大公约数。  
> 余数为 0 时，较小数本身就是最大公约数。

把它想象成**分蛋糕**：  
- 先让大号蛋糕（`mx`）被小号蛋糕（`mn`）切分，余下的那块（`mx % mn`）再和小号蛋糕继续切，直到余下的那块正好是 0，最后一次切的那个小号蛋糕的大小就是两块蛋糕的最大公共尺寸——也就是 GCD。  

欧几里得算法的时间复杂度是 **对数级**（`O(log min(mx, mn))`），因为每一次取余都会把数字大幅“缩小”。  
因此，只要先得到最小值 `mn` 与最大值 `mx`（一次遍历），随后用欧几里得算法求 `gcd(mn, mx)`，整个过程就非常快。

#### 代码（Python）  

```python
from typing import List

def findGCD(nums: List[int]) -> int:
    # ---------- 第一步：一次遍历得到最小值和最大值 ----------
    mn = min(nums)  # Python 内置函数，一次遍历即可得到最小值
    mx = max(nums)  # 同理，得到最大值

    # ---------- 第二步：欧几里得算法求 gcd ----------
    def euclidean_gcd(a: int, b: int) -> int:
        # a、b 任意顺序均可，下面的 while 循环会自动处理
        while b != 0:          # 当余数不为 0 时继续
            a, b = b, a % b    # 让 b 成为新的“较大数”，余数成为新的“较小数”
        return a               # b 为 0 时，a 就是最大公约数

    return euclidean_gcd(mn, mx)
```

#### 复杂度  
- **时间复杂度**：`O(n + log min(mx, mn))`  
  - `O(n)` 用于一次遍历找最小/最大。  
  - `log min(mx, mn)` 是欧几里得算法的迭代次数，通常只需要几次（因为每次都把数字缩小）。  
  - 与暴力解相比，**从每次最多检查 1000 次降到几次**，快了好几倍。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级的变量，没有额外的数组或递归栈（即使用递归实现，栈深度也仅 `log` 级，仍算 `O(1)`）。

---  

## 心得  

- **核心技巧**：欧几里得算法（辗转相除）求最大公约数。  
- **适用的题型**  
  1. 给定两个数，求它们的 GCD（直接使用欧几里得）。  
  2. 多个数的 GCD：先把前两个求出 GCD，再和下一个数求 GCD，循环下去。  
  3. 与 **约数/倍数** 相关的题目，如 “判断两个数是否互质”、 “求最小公倍数（LCM）” 等（LCM 可以通过 `LCM(a,b)=a*b/GCD(a,b)` 计算）。  
- **一句话总结**：  
  > “最大公约数只要用欧几里得算法，一遍遍历找最值，两步就搞定。”  

---  

## 反思  

- **第一反应**：先想到遍历所有可能的除数（暴力），因为直觉上 “最大公约数一定在 1~最小值之间”。  
- **最容易踩的坑**  
  1. **忘记先找最小值和最大值**，直接对所有数组元素两两求 GCD，导致不必要的 O(n²) 时间。  
  2. **边界情况**：数组里只有相同的数时，最小值 = 最大值，GCD 就是这个数本身。代码必须能正确返回。  
  3. **取余为 0 的结束条件**：在实现欧几里得时，若写成 `while a != 0` 而不是 `while b != 0`，容易导致错误的返回值。  
- **下次遇到同类题**：  
  > “先把问题压缩到最关键的几个数（如最小/最大），然后把数学核心（如 GCD）用已知的高效算法直接解决。”