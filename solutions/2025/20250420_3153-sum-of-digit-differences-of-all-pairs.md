# #3153. 所有数对的位差之和 / Sum of Digit Differences of All Pairs

> 难度：中等 · 标签：Array、Hash Table、Math、Counting · [LeetCode 链接](https://leetcode.com/problems/sum-of-digit-differences-of-all-pairs/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers where all integers have the same number of digits.
The digit difference between two integers is the count of different digits that are in the same position in the two integers.
Return the sum of the digit differences between all pairs of integers in nums.

**Examples**

**Example 1:**

```
Input: nums = [13,23,12]
Output: 4
Explanation: We have the following: - The digit difference between 1 3 and 2 3 is 1. - The digit difference between 1 3 and 1 2 is 1. - The digit difference between 23 and 12 is 2. So the total sum of digit differences between all pairs of integers is 1 + 1 + 2 = 4 .
```

**Example 2:**

```
Input: nums = [10,10,10,10]
Output: 0
Explanation: All the integers in the array are the same. So the total sum of digit differences between all pairs of integers will be 0.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] < 109
- All integers in nums have the same number of digits.

---

## 题目（中文翻译）

**题目描述**  
给定一个只包含正整数的数组 `nums`，且数组中的所有整数均具有相同的位数。  
两个整数之间的 **位差（digit difference）** 定义为：在相同位置上不同的数字的个数。  
请返回 `nums` 中所有整数对之间位差的总和。

**示例 1**  
输入: `nums = [13,23,12]`  
输出: `4`  
解释: 我们有以下配对：  
- `13` 与 `23` 的位差为 `1`（个位相同，十位不同）。  
- `13` 与 `12` 的位差为 `1`（十位相同，个位不同）。  
- `23` 与 `12` 的位差为 `2`（十位和个位均不同）。  
因此所有整数对的位差之和为 `1 + 1 + 2 = 4`。

**示例 2**  
输入: `nums = [10,10,10,10]`  
输出: `0`  
解释: 数组中的所有整数都相同，任意两数之间的位差为 `0`，故总和为 `0`。

**约束条件**  
- `2 <= nums.length <= 10^5`  
- `1 <= nums[i] < 10^9`  
- `nums` 中的所有整数具有相同的位数。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**把每一对数字都枚举出来，逐位比较它们的每个数字是否相同**，相同则计 0，不同则计 1，最后把所有对的计数加在一起。  

- **数据结构**：我们只需要把数组 `nums` 按顺序放进列表里，遍历时用两层 `for` 循环取出每一对 `(i, j)`。  
- **生活化类比**：把每个整数想成一排相同长度的“卡片”。比较两张卡片时，把每个位置的数字当作“字母”，如果字母不一样，就记一分。就像两本同页数的书，对应页码的文字不相同时计数。  
- **正确性**：因为我们把 **所有** 可能的配对都算了一遍，且每个配对的差异都是逐位比较得到的，求和自然就是题目要求的“所有配对的数字差的总和”。  

#### 代码（Python）

```python
from typing import List

def sumDigitDifferences_brute(nums: List[int]) -> int:
    n = len(nums)
    # 先把所有数字统一转成字符串，方便逐位比较
    strs = [str(x) for x in nums]          # 例如 13 -> "13"
    total = 0

    # 双层循环枚举所有 unordered pair (i < j)
    for i in range(n):
        for j in range(i + 1, n):
            diff = 0
            # 同一位置逐位比较，长度相同所以可以直接 zip
            for a, b in zip(strs[i], strs[j]):
                if a != b:                 # 不相同则计 1
                    diff += 1
            total += diff                  # 把这对的差加入答案
    return total
```

#### 复杂度  

- **时间复杂度**：`O(n² * d)`  
  - `n` 是数组长度，`d` 是每个整数的位数（题目保证相同）。  
  - “平方” `n²` 表示我们要遍历所有配对，`d` 表示每对要逐位比较。  
  - 用大白话说，就是如果数组有 10,000 个数，配对数大约是 50,000,000（10,000 选 2），每对再比较几位，算起来会很慢。  

- **空间复杂度**：`O(n * d)`（存放所有数字的字符串）  
  - 这里的额外空间主要是把整数转成字符串占的内存，`d` 很小（最多 9），所以可以视作 `O(n)`。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历所有配对**。实际上，**不同配对之间的比较是可以“合并”**的。  

观察每一位（比如个位、十位、百位……）：

- 对于同一位上的所有数字，我们只关心 **有多少个 0、多少个 1、…、多少个 9**。  
- 假设在第 `k` 位上，数字 `d` 出现了 `c` 次。  
  - 那么这 `c` 个数字会和其余 `n - c` 个不等于 `d` 的数字产生差异，每对差 1。  
  - 所以第 `k` 位对答案的贡献是 `c * (n - c)`。  

把每一位的贡献都算出来再相加，就是所有配对的总差。  

**关键点**：

1. **把问题拆成“每一位独立求和”**。因为不同位之间互不影响，求和后再相加即可。  
2. **计数**：对每一位，用长度为 10 的数组 `cnt[0..9]` 统计出现次数。这里的数组相当于 **哈希表**（字典），只不过键是固定的 0~9，查询和写入都是 O(1)。可以把它想象成一本**数字手册**，第 `i` 页记着数字 `i` 出现了多少次。  
3. **公式**：对于一位的所有数字，`c * (n - c)` 实际上是 **每对不同数字计 1** 的总和。把所有 `c` 加起来就等于 `n * (n - 1) / 2`（配对总数），但我们只想要不同数字的配对数，于是用 `c * (n - c)` 把每种数字贡献的不同配对挑出来。  

#### 代码（Python）

```python
from typing import List

def sumDigitDifferences(nums: List[int]) -> int:
    n = len(nums)
    # 所有整数位数相同，取第一个的长度即可
    d = len(str(nums[0]))
    total = 0

    # 逐位处理，从最低位（个位）到最高位
    for pos in range(d):
        # cnt[i] 记录第 pos 位上数字 i 出现的次数，i∈[0,9]
        cnt = [0] * 10

        # 统计这一位的数字出现次数
        for num in nums:
            # 取出第 pos 位的数字
            # 例如 pos=0 → 个位, pos=1 → 十位 ...
            digit = (num // (10 ** pos)) % 10
            cnt[digit] += 1

        # 根据计数公式累计贡献
        for c in cnt:                     # c 是出现次数
            total += c * (n - c)          # 不同数字配对数 * 1（每对差 1）

    return total
```

**代码要点说明**  

- `digit = (num // (10 ** pos)) % 10`：先把整数右移 `pos` 位，再取模 10，得到对应位的数字。  
- `cnt = [0] * 10`：长度为 10 的列表相当于 **哈希表**，键固定为 0~9，查询、更新都是 O(1)。  
- `total += c * (n - c)`：这里每对不同数字计 1，`c` 与 `n-c` 的乘积恰好是所有以该数字为一方、另一方为不同数字的配对数。  

#### 复杂度  

- **时间复杂度**：`O(n * d)`  
  - 只遍历一次数组 `n` 次，每次要取出 `d` 位数字（`d ≤ 9`），所以整体是线性时间。  
  - 与暴力解的 `O(n² * d)` 相比，省掉了配对的二次循环，快了一个数量级。  

- **空间复杂度**：`O(1)`（常数空间）  
  - 只用了长度为 10 的计数数组 `cnt`，不随 `n` 增长。  

---

## 心得  

- **核心技巧**：**逐位计数 + 组合数学**（`c * (n - c)`）。  
- **适用的题型**  
  1. “所有配对的某种逐位差值求和” 例如 **Sum of Digit Differences of All Pairs**（本题）。  
  2. “所有配对的位异或和” 例如 **Sum of Pairwise Hamming Distance**（二进制位异或计数）。  
  3. “每一列/行的不同元素配对计数” 例如 **Count Nice Pairs in an Array**（使用哈希计数）。  
- **一句话总结**：把“大对小”的暴力配对拆成“每一位独立计数”，用 `c * (n - c)` 把不同元素配对一次性算完，就是解题钥匙。  

---

## 反思  

- **第一反应**：直接写双层循环逐对比较，想到要把每个数字转成字符串。  
- **最容易踩的坑**  
  1. **位数不统一**：虽然题目保证相同，但如果忘记验证，直接取 `(num // 10**pos) % 10` 仍然安全，因为高位会自动得到 0。  
  2. **整数溢出**：在 Python 中不存在，但在语言如 C++/Java 需要注意 `c * (n - c)` 可能超过 32 位整数范围。  
  3. **忘记除以 2**：有的同学会把 `c * (n - c)` 再除以 2，实际上已经算好了每对一次，不需要再除。  
- **下次遇到同类题**：第一步先问自己“是否可以把问题拆成每一位/每一列独立计数？”如果答案是 Yes，马上转向计数+组合公式的思路。