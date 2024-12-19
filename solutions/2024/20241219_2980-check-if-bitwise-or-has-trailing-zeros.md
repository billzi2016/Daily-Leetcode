# #2980. 检查按位或是否有尾随零 / Check if Bitwise OR Has Trailing Zeros

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/check-if-bitwise-or-has-trailing-zeros/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums.
You have to check if it is possible to select two or more elements in the array such that the bitwise OR of the selected elements has at least one trailing zero in its binary representation.
For example, the binary representation of 5, which is "101", does not have any trailing zeros, whereas the binary representation of 4, which is "100", has two trailing zeros.
Return true if it is possible to select two or more elements whose bitwise OR has trailing zeros, return false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: true
Explanation: If we select the elements 2 and 4, their bitwise OR is 6, which has the binary representation "110" with one trailing zero.
```

**Example 2:**

```
Input: nums = [2,4,8,16]
Output: true
Explanation: If we select the elements 2 and 4, their bitwise OR is 6, which has the binary representation "110" with one trailing zero.
Other possible ways to select elements to have trailing zeroes in the binary representation of their bitwise OR are: (2, 8), (2, 16), (4, 8), (4, 16), (8, 16), (2, 4, 8), (2, 4, 16), (2, 8, 16), (4, 8, 16), and (2, 4, 8, 16).
```

**Example 3:**

```
Input: nums = [1,3,5,7,9]
Output: false
Explanation: There is no possible way to select two or more elements to have trailing zeros in the binary representation of their bitwise OR.
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个正整数（positive integers）数组 `nums`。  
需要判断是否可以选取数组中的两个或更多元素，使得这些选取元素的按位或（bitwise OR）的二进制表示中至少包含一个尾随零（trailing zero）。  

例如，数字 5 的二进制表示为 `101`，没有尾随零；而数字 4 的二进制表示为 `100`，有两个尾随零。  

如果存在一种选取方式使得按位或（bitwise OR）结果含有尾随零，返回 `true`；否则返回 `false`。  

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `2 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`  

---

### 示例

**示例 1**  
```
Input: nums = [1,2,3,4,5]
Output: true
```
**解释**：若选取元素 `2` 和 `4`，它们的按位或（bitwise OR）为 `6`，其二进制表示为 `110`，包含一个尾随零（trailing zero）。

**示例 2**  
```
Input: nums = [2,4,8,16]
Output: true
```
**解释**：若选取元素 `2` 和 `4`，它们的按位或（bitwise OR）为 `6`，二进制为 `110`，有一个尾随零（trailing zero）。  
其他满足条件的选取方式还有：`(2, 8)`、`(2, 16)`、`(4, 8)`、`(4, 16)`、`(8, 16)`、`(2, 4, 8)`、`(2, 4, 16)`、`(2, 8, 16)`、`(4, 8, 16)`、以及 `(2, 4, 8, 16)`。

**示例 3**  
```
Input: nums = [1,3,5,7,9]
Output: false
```
**解释**：不存在任何选取两个或更多元素，使得它们的按位或（bitwise OR）的二进制表示中含有尾随零（trailing zero）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有**可能的组合**都枚举一遍，只要找到一种组合的按位或（bitwise OR）在二进制表示里以 `0` 结尾（即**最低位是 0**），就返回 `True`。  

- **数据结构**：我们只需要数组本身和两个循环的下标，根本不需要额外的容器。可以把数组想象成一排 **盒子**，我们把每两个盒子里放的数字取出来做 OR 运算，就像把两块拼图拼在一起看看拼出的图案是否在最右边留了空白（0）。
- **为什么正确**：遍历所有两两组合（或更多元素的组合）能够覆盖题目要求的“任意选取两个或两个以上元素”。如果真的存在一种合法的选取方式，暴力遍历必然会在某一次检查时发现它。
- **复杂度分析**：  
  - **时间**：外层遍历 `i`，内层遍历 `j > i`，总共要检查 `C(n,2) = n·(n-1)/2` 对。用大写的 **O** 表示，这相当于 **O(n²)**，意思是当数组长度翻倍时，检查的次数会 **大约增加四倍**。  
  - **空间**：只用了几个计数器和临时变量，和数组本身无关，属于 **O(1)**（常数级）空间。

#### 代码（Python）

```python
from typing import List

def has_trailing_zero_bruteforce(nums: List[int]) -> bool:
    n = len(nums)
    # 枚举所有长度为 2 的子集（两两组合），
    # 只要其中一对满足条件就可以直接返回 True
    for i in range(n):
        for j in range(i + 1, n):
            # 按位或运算
            cur = nums[i] | nums[j]
            # 判断最低位是否为 0（即是偶数）
            if cur % 2 == 0:          # 或者写成 (cur & 1) == 0
                return True
    # 如果所有组合都不满足，说明不存在合法的选取方式
    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要检查大约 `n²/2` 对元素，数组越大，耗时增长呈二次方。
- **空间复杂度**：`O(1)` — 只使用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们枚举了所有对，实际上并不需要这么多。  
关键观察：

1. **按位或永远不会把已经是 0 的位变成 1**，只能把 0 变成 1，或者保持不变。  
2. 要让最终的 OR 结果在二进制里**以 0 结尾**，最低位（第 0 位）必须是 0。  
3. 如果选取的任意一个数的最低位是 1（奇数），那么 OR 的最低位就一定是 1，因为 1 “盖不住” 0。  
4. 因此，**所有被选中的数的最低位都必须是 0**，也就是说它们全部是 **偶数**。  

题目要求**至少选两个元素**，所以只要数组中**至少有两个偶数**，我们就可以任选这两个偶数，它们的 OR 仍然是偶数（最低位 0），满足条件。  

这把原本的二次枚举直接化简为一次线性扫描：

- 遍历数组，统计偶数的个数。  
- 若偶数个数 ≥ 2，返回 `True`；否则返回 `False`。

#### 代码（Python）

```python
from typing import List

def has_trailing_zero_opt(nums: List[int]) -> bool:
    even_cnt = 0               # 用来计数偶数（最低位为 0）的个数
    for x in nums:
        if x % 2 == 0:         # 或者写成 (x & 1) == 0，效果相同
            even_cnt += 1
            if even_cnt >= 2:  # 只要找到两个偶数就可以提前结束
                return True
    return False               # 扫描完都不到两个偶数，说明不可能
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只需要一次遍历，数组长度翻倍，检查次数也翻倍（线性增长）。相比暴力的 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(1)` — 只用了一个计数器 `even_cnt`，不随输入规模增长。

---

## 心得

- **核心技巧**：**位运算的单向性**（OR 只能把位从 0 变成 1） + **最低位（奇偶性）判断**。  
- **适用的题型**：  
  1. “是否可以通过若干数的 OR / AND / XOR 获得特定的最低位/最高位” 类问题。  
  2. “选取若干元素使得结果满足某个位为 0/1” 的组合题。  
  3. “只要满足某个局部条件（如都是偶数），全局条件自然成立” 的简化题。  
- **一句话总结**：只要找出 **两个满足最低位为 0 的数**（即偶数），就能保证 OR 结果有至少一个 trailing zero。

## 反思

- **第一反应**：直接写双层循环枚举所有组合，保证不遗漏任何可能性。  
- **最容易踩的坑**：忘记 “至少两个元素” 的限制，误把单个偶数也算作成功；或者误以为需要检查所有子集的 OR，而实际上只要检查两两组合就够了（因为 OR 的单向性）。  
- **下次遇到同类题**：第一步先**思考位运算的单向特性**，找出 **最关键的位**（本题是最低位），再判断**哪些元素本身已经满足**，从而把搜索空间从指数/二次级别压到线性。