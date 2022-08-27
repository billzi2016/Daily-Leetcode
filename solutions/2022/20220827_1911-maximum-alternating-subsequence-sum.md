# #1911. 最大交替子序列和 / Maximum Alternating Subsequence Sum

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-alternating-subsequence-sum/)

---

## 题目（英文原版）

**Description**

The alternating sum of a 0-indexed array is defined as the sum of the elements at even indices minus the sum of the elements at odd indices.
Given an array nums, return the maximum alternating sum of any subsequence of nums (after reindexing the elements of the subsequence).
A subsequence of an array is a new array generated from the original array by deleting some elements (possibly none) without changing the remaining elements' relative order. For example, [2,7,4] is a subsequence of [4,2,3,7,2,1,4] (the underlined elements), while [2,4,2] is not.

**Examples**

**Example 1:**

```
Input: nums = [4,2,5,3]
Output: 7
Explanation: It is optimal to choose the subsequence [4,2,5] with alternating sum (4 + 5) - 2 = 7.
```

**Example 2:**

```
Input: nums = [5,6,7,8]
Output: 8
Explanation: It is optimal to choose the subsequence [8] with alternating sum 8.
```

**Example 3:**

```
Input: nums = [6,2,1,2,4,5]
Output: 10
Explanation: It is optimal to choose the subsequence [6,1,5] with alternating sum (6 + 5) - 1 = 10.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

交替和（alternating sum）指的是对一个 **0 索引** 的数组，将偶数下标的元素求和后减去奇数下标的元素求和得到的值。  
给定数组 `nums`，返回 `nums` 中 **任意子序列**（subsequence）在重新编号（即按照子序列出现的顺序重新从 0 开始索引）后的最大交替和。

**子序列** 是指从原数组中删除若干元素（可以不删），但保持剩余元素相对顺序不变得到的新数组。例如，`[2,7,4]` 是 `[4,2,3,7,2,1,4]` 的子序列（下划线标出的元素），而 `[2,4,2]` 不是。

---

### 示例

**示例 1**  
```
Input: nums = [4,2,5,3]
Output: 7
Explanation: 选择子序列 [4,2,5]，其交替和为 (4 + 5) - 2 = 7，达到最大值。
```

**示例 2**  
```
Input: nums = [5,6,7,8]
Output: 8
Explanation: 选择子序列 [8]，交替和为 8，为最大可能值。
```

**示例 3**  
```
Input: nums = [6,2,1,2,4,5]
Output: 10
Explanation: 选择子序列 [6,1,5]，其交替和为 (6 + 5) - 1 = 10，取得最大值。
```

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有可能的子序列枚举出来，逐个计算它们的“交替和”，最后取最大值。

- **子序列**：就像从一串珠子里挑出若干颗（可以不挑），挑出来的顺序不能变。  
- **交替和**：把挑出来的第 0、2、4… 个珠子加起来，再减去第 1、3、5… 个珠子。相当于把子序列重新编号后，偶数下标“正”，奇数下标“负”。

枚举子序列可以用**递归**（或二进制掩码）实现：  
对每个位置 `i`，我们有两种选择——**取** `nums[i]` 放进子序列，或**不取**。递归到底部时得到一个完整的子序列，计算它的交替和并更新全局最大值。

这种方法一定能得到正确答案，因为它遍历了**全部**合法子序列，最大值必然在其中。

**时间/空间分析（大白话）**  
- 对长度为 `n` 的数组，每个位置都有“取”或“不取”两种决定，所有可能的子序列数是 `2^n`（指数级）。所以时间复杂度是 `O(2^n)`，意思是“随着元素增多，耗时会像翻倍一样飞快增长”。  
- 递归深度最多 `n`，需要保存每层的状态，空间复杂度是 `O(n)`（栈空间）。

#### 代码（Python）

```python
def maxAlternatingSum_bruteforce(nums):
    n = len(nums)
    best = 0                     # 保存全局最大交替和

    def dfs(idx, seq):
        """递归遍历 idx 之后的所有子序列，seq 保存当前已经选的元素"""
        nonlocal best
        if idx == n:              # 递归到底，计算交替和
            alt_sum = 0
            for i, v in enumerate(seq):
                if i % 2 == 0:    # 偶数下标加
                    alt_sum += v
                else:             # 奇数下标减
                    alt_sum -= v
            best = max(best, alt_sum)
            return

        # 1) 不取 nums[idx]
        dfs(idx + 1, seq)

        # 2) 取 nums[idx]，放进子序列末尾
        dfs(idx + 1, seq + [nums[idx]])

    dfs(0, [])
    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 随着 `n` 增加，耗时会呈指数级增长，实际只能跑几十个元素以内的测试。  
- **空间复杂度**：`O(n)` —— 递归栈最多保存 `n` 层调用。

---

### 2. 最优解

#### 思路  
暴力解慢的根本原因是**重复计算**：我们在每一步都把所有已经形成的子序列重新记下来，而其实只需要记住“到当前位置为止，最好的两种状态”即可。

**关键观察**  
把子序列的长度奇偶性放在心里：

| 状态 | 含义 |
|------|------|
| `even` | 已选的子序列长度为 **偶数**（0、2、4…），所以最后一个元素的符号是 **+**（正）。我们记下此时能得到的最大交替和。 |
| `odd`  | 已选的子序列长度为 **奇数**（1、3、5…），最后一个元素的符号是 **-**（负）。我们记下此时的最大交替和。 |

当我们看到新的数字 `x` 时，有两种可能：

1. **把 `x` 加到 `odd` 状态的子序列后**  
   原来长度是奇数，加入一个元素后长度变成偶数，`x` 的符号是 **+**。新的 `even` 值可以是 `odd + x`。

2. **把 `x` 加到 `even` 状态的子序列后**  
   原来长度是偶数，加入后变成奇数，`x` 的符号是 **-**。新的 `odd` 值可以是 `even - x`。

当然，也可以**不选** `x`，保持原来的 `even`、`odd` 不变。于是每一步的转移公式是：

```
new_even = max(old_even, old_odd + x)
new_odd  = max(old_odd,  old_even - x)
```

只需要两个变量在遍历数组时滚动更新，整个过程是 **线性** 的。

**为什么只需要两个状态就够？**  
交替和的定义只关心“当前子序列最后一个位置是正还是负”，而不在乎前面具体选了哪些数。所有满足同样奇偶性的子序列，只要它们的交替和最大即可代表这一类。于是状态压缩到 `even`、`odd` 两个数。

#### 代码（Python）

```python
def maxAlternatingSum(nums):
    """
    动态规划，时间 O(n)，空间 O(1)。
    even：已选子序列长度为偶数时的最大交替和（最后一个元素为 +）。
    odd：已选子序列长度为奇数时的最大交替和（最后一个元素为 -）。
    """
    even = 0          # 空子序列长度为 0，交替和为 0
    odd = float('-inf')   # 尚未出现奇数长度子序列，用负无穷表示“不可能”

    for x in nums:
        # 必须先算新 odd，再算新 even，防止相互覆盖
        new_odd = max(odd, even - x)   # 把 x 放在奇数位（减去 x）或保持原 odd
        new_even = max(even, odd + x)  # 把 x 放在偶数位（加上 x）或保持原 even
        odd, even = new_odd, new_even

    # 最终答案一定是偶数长度的状态，因为奇数长度会多一个负号
    return even
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 为数组长度。和暴力解相比，速度提升了 **指数级**（从 `2^n` 降到 `n`）。  
- **空间复杂度**：`O(1)` —— 只用常数个变量（`even`、`odd`、临时变量），不随 `n` 增长。

---

## 心得

- 这道题考察的核心技巧是 **状态压缩的动态规划**：只记录「奇数长度」和「偶数长度」两种状态，而不是所有子序列。  
- 该技巧适用于 **交替符号、正负切换** 的序列问题，例如  
  1. “买卖股票的最佳时机 II”（每次买入后必须卖出，收益正负交替）  
  2. “最大子序列交替和”或 “最大交替乘积” 之类的变体。  
- **一句话总结**：把子序列的“下一个符号是 + 还是 -”当成状态，滚动更新即可得到最优解。

---

## 反思

- **第一反应**：直接想枚举所有子序列，写递归或位运算。  
- **最容易踩的坑**  
  - 忘记 **重新编号**：子序列的交替和是基于子序列内部的索引，而不是原数组的索引。  
  - 初始化 `odd` 时使用 `-inf`，否则会把 “未选任何元素” 当成合法的奇数长度子序列。  
  - 更新顺序错误：如果先更新 `even` 再更新 `odd`，会使用已经被修改过的 `even`，导致错误的转移。  
- **下次类似题**：第一步先思考“当前状态只和**符号**有关吗”，如果是，尝试用 **奇/偶（或正/负）两状态**来压缩 DP。这样往往能把指数级搜索压到线性时间。