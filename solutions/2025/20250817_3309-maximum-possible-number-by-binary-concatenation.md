# #3309. 通过二进制拼接得到的最大可能数 / Maximum Possible Number by Binary Concatenation

> 难度：中等 · 标签：Array、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-possible-number-by-binary-concatenation/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums of size 3.
Return the maximum possible number whose binary representation can be formed by concatenating the binary representation of all elements in nums in some order.
Note that the binary representation of any number does not contain leading zeros.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: 30
Explanation:
Concatenate the numbers in the order [3, 1, 2] to get the result "11110" , which is the binary representation of 30.
```

**Example 2:**

```
Input: nums = [2,8,16]
Output: 1296
Explanation:
Concatenate the numbers in the order [2, 8, 16] to get the result "10100010000" , which is the binary representation of 1296.
```

**Constraints**

- nums.length == 3
- 1 <= nums[i] <= 127

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 3 的整数数组 `nums`。返回可以通过将 `nums` 中所有元素的二进制表示（binary representation）按某种顺序拼接（concatenating）得到的二进制字符串对应的最大十进制数。  
注意，任意数的二进制表示中不包含前导零。

**示例 1**  
```text
输入: nums = [1,2,3]
输出: 30
解释:
按顺序 [3, 1, 2] 拼接得到二进制字符串 "11110"，其十进制值为 30。
```

**示例 2**  
```text
输入: nums = [2,8,16]
输出: 1296
解释:
按顺序 [2, 8, 16] 拼接得到二进制字符串 "10100010000"，其十进制值为 1296。
```

**约束条件**  
- `nums.length == 3`
- `1 <= nums[i] <= 127`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
- **最直接的想法**：把三个数的二进制字符串全部列出来，然后把这三段二进制按照**所有可能的排列顺序**拼接，算出每一种拼接得到的十进制值，取最大的那个。  
- **用到的数据结构**：  
  - `list` 保存三个数的二进制字符串。  
  - `itertools.permutations` 能一次性产生 **全排列**，相当于把“所有可能的拼接顺序”全部列出来。可以把它想象成一次次把三本不同颜色的书随意排成一排，看看哪种排法拼出的标题最长、最大。  
- **为什么一定能得到正确答案**：  
  - 题目只要求把**三个**数的二进制拼接，所有合法的顺序只有 `3! = 6` 种。我们把这 6 种全部尝试一次，必然会覆盖真正的最优顺序。  
- **时间/空间复杂度**：  
  - **时间**：遍历 6 种排列，每种都要把三个二进制字符串拼接一次，再把拼好的二进制转成十进制。拼接和转数的代价与数字位数成正比，最大位数不超过 `7+7+7 = 21`（因为 `nums[i] ≤ 127`），可以视作常数。因此整体是 **O(6) ≈ O(1)**，即常数时间。  
  - **空间**：只需要保存原数组的 3 条二进制字符串和临时的拼接结果，最多 O(1) 的额外空间。  

#### 代码（Python）  

```python
import itertools

def max_binary_concatenation_bruteforce(nums):
    """
    暴力枚举所有排列，返回最大可能的十进制数
    """
    # 把每个整数转成二进制字符串（去掉前面的 '0b'）
    bin_strs = [bin(x)[2:] for x in nums]          # 例如 5 -> '101'
    
    max_val = 0
    # itertools.permutations 会产生所有可能的排列（这里恰好是 3! = 6 种）
    for perm in itertools.permutations(bin_strs):
        # 把当前排列的二进制字符串拼接在一起
        merged = ''.join(perm)                     # 例如 ('111', '1', '10') -> '111110'
        # 把拼好的二进制串转成十进制整数
        cur_val = int(merged, 2)                   # int('111110', 2) = 62
        max_val = max(max_val, cur_val)            # 维护最大值
    return max_val
```

#### 复杂度  

- **时间复杂度**：`O(6) ≈ O(1)`  
  - 解释：只需要遍历 6 种排列，每次操作的工作量与二进制位数有关，而位数上限是 21（因为每个数最多 7 位），所以可以看成常数时间。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了固定数量的额外变量（几个字符串和整数），不随输入规模增长。  

---

### 2. 最优解  

#### 思路  

虽然暴力已经是 **常数时间**，但我们仍可以从“比较两两拼接的大小”出发，得到一种**排序**的思路，这在 **元素个数更大** 时尤为有用。  

1. **慢在哪里？**  
   - 暴力把所有排列都列出来，思路清晰但如果题目改成 “`n` 个数” ，枚举 `n!` 的代价会瞬间爆炸。  
2. **优化的关键**：  
   - 对于任意两个数 `a`、`b`，我们只需要判断把 `a` 放在前面还是 `b` 放在前面会得到更大的二进制数。  
   - 这正好可以用**自定义比较函数**来实现：  
     - 若 `a+b`（二进制字符串拼接） > `b+a`，则 `a` 应该排在 `b` 前面。  
   - 这和 “组成最大数” 题目（把整数视为字符串拼接）是同一个原理，只是这里的基数是 2（二进制）。  
3. **核心算法**：  
   - 将每个整数转成二进制字符串。  
   - 用 `sorted` + `functools.cmp_to_key` 按照上面的比较规则排序。  
   - 排好序后一次性把所有字符串拼接，最后转成十进制。  
4. **为什么正确**：  
   - 设排序后得到的序列为 `s1, s2, …, sk`（这里 `k = 3`）。  
   - 对任意相邻的两项 `si, si+1`，比较函数保证 `si+si+1` ≥ `si+1+si`（二进制字符串的字典序）。  
   - 通过“交换相邻逆序对不减小整体值”的归纳，可证明整个序列是 **全局最优** 的。  

#### 代码（Python）  

```python
import functools

def max_binary_concatenation_optimal(nums):
    """
    通过自定义排序，使二进制拼接得到的十进制数最大
    """
    # 1️⃣ 把每个整数转成二进制字符串（不带前缀 0b）
    bin_strs = [bin(x)[2:] for x in nums]

    # 2️⃣ 定义比较函数：若 a+b 的二进制值更大，则 a 排在前面
    def cmp(a, b):
        # a+b 与 b+a 实际上是字符串比较，等价于比较对应的二进制数大小
        if a + b > b + a:      # 字典序大的二进制串对应的十进制数也更大
            return -1         # -1 表示 a 应排在前面
        elif a + b < b + a:
            return 1          # 1 表示 b 应排在前面
        else:
            return 0          # 完全相同，顺序无所谓

    # 3️⃣ 使用 cmp_to_key 把比较函数转换成 key 函数进行排序
    sorted_bins = sorted(bin_strs, key=functools.cmp_to_key(cmp))

    # 4️⃣ 把排好序的二进制串一次性拼接，再转成十进制整数
    merged = ''.join(sorted_bins)
    return int(merged, 2)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`（这里 `n = 3`，所以仍然是常数）  
  - 排序需要比较 `O(n log n)` 次，每次比较拼接两段二进制字符串，长度最多 21，视作常数。相比暴力的 `O(n!)`（若 `n` 更大）有明显提升。  
- **空间复杂度**：`O(n)`  
  - 需要存储 `n` 条二进制字符串以及排序过程中的临时列表，随 `n` 线性增长。  

---

## 心得  

- **核心技巧**：**自定义比较排序**（把“哪个先拼接更大”转化为两两比较）。  
- **适用的题型**：  
  1. **Largest Number**（把整数视为字符串拼接得到最大数）。  
  2. **Form Minimum Number**（把整数拼接得到最小数，比较方向相反）。  
  3. **按自定义规则排序的字符/字符串拼接**（如把单词按字典序或特定规则拼接）。  
- **一句话总结**：**把“哪个先放”转化为“拼接后哪个二进制字符串更大”，用排序一次性决定顺序**。  

---

## 反思  

- **第一反应**：看到“3 个数”，立刻想到**枚举全排列**，因为 3! 只有 6 种，写起来最直观。  
- **最容易踩的坑**：  
  - 忘记二进制表示**不能有前导零**，所以直接使用 `bin(x)[2:]`（去掉 `0b`）即可。  
  - 在自定义比较时，如果用整数比较 `int(a+b) vs int(b+a)`，会因位数不同导致溢出或额外的进位，**直接比较字符串**更安全且更快。  
- **下次遇到同类题**：第一步先**思考是否可以用排序代替枚举**——把“顺序决定最终值”抽象为两两比较函数，如果可以，立刻写出比较规则并用 `sorted` 实现。