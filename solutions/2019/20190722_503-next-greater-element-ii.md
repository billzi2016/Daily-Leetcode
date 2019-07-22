# #503. 下一个更大元素 II / Next Greater Element II

> 难度：中等 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/next-greater-element-ii/)

---

## 题目（英文原版）

**Description**

Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.
The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1]
Output: [2,-1,2]
Explanation: The first 1's next greater number is 2; 
The number 2 can't find next greater number. 
The second 1's next greater number needs to search circularly, which is also 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4,3]
Output: [2,3,4,-1,4]
```

**Constraints**

- 1 <= nums.length <= 104
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个循环整数数组 `nums`（即 `nums[nums.length - 1]` 的下一个元素是 `nums[0]`），返回数组中每个元素的下一个更大数字。
一个数字 `x` 的下一个更大数字是 **按遍历顺序** 在数组中紧随其后的第一个比 `x` 更大的数字，这意味着可以循环查找以找到它的下一个更大数字。如果不存在，则返回 `-1`。

## 示例

### 示例 1
**输入**: `nums = [1,2,1]`  
**输出**: `[2,-1,2]`  
**解释**:  
- 第一个 `1` 的下一个更大数字是 `2`；  
- 数字 `2` 找不到下一个更大数字，返回 `-1`；  
- 第二个 `1` 需要循环查找其下一个更大数字，结果同样是 `2`。

### 示例 2
**输入**: `nums = [1,2,3,4,3]`  
**输出**: `[2,3,4,-1,4]`

## 约束条件
- `1 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一个位置 i，都顺着数组往后走，找到第一个比 `nums[i]` 大的数**。因为数组是循环的，走到末尾后要继续从头遍历，最多遍历两遍（`2 * n` 步）才能保证每个元素都找完。  

- **使用的数据结构**：只需要一个普通的列表（数组）来存放答案。这里不需要任何高级结构，类似于我们在超市里把所有商品排成一条线，然后从左到右一个个检查是否比前面的贵——最朴素的“顺序查找”。  
- **正确性**：对每个 `i`，我们从 `i+1` 开始（模 `n` 循环），依次比较，如果找到了比 `nums[i]` 大的元素，就把它记为答案；如果遍历了一整圈仍未找到，说明不存在更大的元素，答案为 `-1`。这正是题目对“下一个更大元素”的定义。  

#### 代码（Python）  

```python
from typing import List

def nextGreaterElements_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [-1] * n                     # 先全部填 -1，后面再改成真正的答案
    for i in range(n):                 # 对每一个位置 i
        # 从 i 的下一个位置开始，最多走 2*n 步（相当于遍历两遍）
        for step in range(1, n):       # 只需要走 n-1 步，因为自己不算在内
            j = (i + step) % n         # 循环索引，超出末尾回到开头
            if nums[j] > nums[i]:      # 找到第一个更大的数
                ans[i] = nums[j]
                break                  # 结束内层循环，继续下一个 i
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个 `i`（共 `n` 次）我们最坏要检查后面的 `n‑1` 个元素，所以大约是 `n × n` 次比较。  
  - 用大白话说，就是“如果数组有 1000 个数，最坏情况要比较 1000 × 1000 = 100 万次”。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了常数个额外变量 `i、step、j`，不随 `n` 增长。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每个位置都要重复遍历后面的元素**。我们需要一种“记忆”机制，让已经遍历过的元素帮助后面的查询。  
这正是 **单调栈（Monotonic Stack）** 的用武之地：

1. **单调递减栈**  
   - 栈里保存的是**下标**，对应的数值从栈底到栈顶是严格递减的。  
   - 当我们看到一个新数 `x`，只要栈顶对应的数 `≤ x`，说明 `x` 就是这些栈顶元素的“下一个更大”。于是弹出栈顶，并把答案填上 `x`。  
2. **循环数组的处理**  
   - 题目要求“环形”，也就是从数组末尾可以继续向前看。  
   - 一个巧妙的办法是**把数组“遍历两遍”**（长度 `2n`），但**只在第一次遍历时把元素压入栈**。第二遍只负责“帮助弹栈”，不再入栈。这样每个位置最多被比较两次，却只入栈一次，保证 `O(n)`。  

> **类比**：想象你在排队买咖啡，前面的人都是“咖啡比我少”。当一个新人手里拿着更大的咖啡（数值更大）时，所有比他小的人都可以立刻得到答案（弹出）。如果队伍是环形的，你把队伍复制一遍再继续走，就能让最后几个人也看到前面的大咖啡。

#### 代码（Python）  

```python
from typing import List

def nextGreaterElements(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [-1] * n                     # 初始化答案为 -1
    stack = []                         # 单调递减栈，存放元素下标

    # 需要遍历两遍：0 .. 2*n-1
    for i in range(2 * n):
        cur = nums[i % n]              # 循环索引，取当前真实的数值

        # 栈顶元素如果比当前数小，就找到了它们的下一个更大元素
        while stack and nums[stack[-1]] < cur:
            idx = stack.pop()          # 弹出下标
            ans[idx] = cur             # 把答案填上

        # 只在第一次遍历时压栈，第二遍只负责弹栈
        if i < n:                      # i < n 表示第一次遍历
            stack.append(i)           # 把下标放进栈，保持单调递减

    return ans
```

> **代码关键点注释**  
- `i % n` 实现“环形”，把数组看成无限复制的链。  
- `while stack and nums[stack[-1]] < cur`：只要栈顶对应的数比当前数小，就可以确定当前数是它们的下一个更大。  
- `if i < n:`：第一次遍历才把下标压入栈，第二遍只用来帮助弹栈，防止重复压栈导致无限循环。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个元素最多被压栈一次、弹栈一次，总操作次数与 `n` 成线性关系。  
  - 用大白话说，如果数组有 10⁴ 个数，最多只会进行约 2×10⁴ 次基本操作，远远快于暴力的 10⁸ 次。  
- **空间复杂度**：`O(n)`  
  - 栈在最坏情况下会存放所有下标（比如严格递减的数组），所以需要 `n` 的额外空间。答案数组本身也算 `O(n)`，这里把它算在返回值里。

---  

## 心得  

- **核心技巧**：**单调栈 + 两遍遍历模拟环形**。  
- **适用的题型**  
  1. “下一个更大/更小元素”系列（如 *Next Greater Element I*、*Daily Temperatures*）。  
  2. “区间最大值”或“柱状图最大矩形”这类需要**维护递增/递减序列**的题目。  
- **一句话总结解题钥匙**：  
  > “把比当前数小的元素全部压进栈，等出现更大的数时一次性弹出，它们的答案就是这一次出现的数。”

---  

## 反思  

- **第一反应**：看到“循环数组”，直接想到把数组拼接两遍再做普通的“下一个更大元素”问题。  
- **最容易踩的坑**  
  1. **忘记只在第一次遍历时入栈**，导致无限循环或答案错误。  
  2. **边界条件**：长度为 1 的数组应该直接返回 `[-1]`，循环两遍仍能正确处理。  
  3. **比较时使用 `<` 而不是 `<=`**，因为相等的元素不算“更大”。  
- **下次第一步**：  
  > “这是不是‘下一个更大元素’的变形？先考虑单调栈，若涉及环形则把遍历次数翻倍”。