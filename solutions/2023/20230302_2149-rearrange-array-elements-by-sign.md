# #2149. 按符号重新排列数组元素 / Rearrange Array Elements by Sign

> 难度：中等 · 标签：Array、Two Pointers、Simulation · [LeetCode 链接](https://leetcode.com/problems/rearrange-array-elements-by-sign/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of even length consisting of an equal number of positive and negative integers.
You should return the array of nums such that the the array follows the given conditions:
Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

**Examples**

**Example 1:**

```
Input: nums = [3,1,-2,-5,2,-4]
Output: [3,-2,1,-5,2,-4]
Explanation:
The positive integers in nums are [3,1,2]. The negative integers are [-2,-5,-4].
The only possible way to rearrange them such that they satisfy all conditions is [3,-2,1,-5,2,-4].
Other ways such as [1,-2,2,-5,3,-4], [3,1,2,-2,-5,-4], [-2,3,-5,1,-4,2] are incorrect because they do not satisfy one or more conditions.
```

**Example 2:**

```
Input: nums = [-1,1]
Output: [1,-1]
Explanation:
1 is the only positive integer and -1 the only negative integer in nums.
So nums is rearranged to [1,-1].
```

**Constraints**

- 2 <= nums.length <= 2 * 105
- nums.length is even
- 1 <= |nums[i]| <= 105
- nums consists of equal number of positive and negative integers.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`，其长度为偶数，且正整数（positive integer）和负整数（negative integer）的数量相等。请重新排列 `nums` 中的元素，使得到的数组满足以下条件：

- 若下标 `i` 为偶数，则 `nums[i]` 为正整数；
- 若下标 `i` 为奇数，则 `nums[i]` 为负整数。

返回满足上述条件的任意排列后的数组。

---

### 示例

#### 示例 1  
**输入**  
```json
nums = [3,1,-2,-5,2,-4]
```  
**输出**  
```json
[3,-2,1,-5,2,-4]
```  
**解释**  
`nums` 中的正整数为 `[3,1,2]`，负整数为 `[-2,-5,-4]`。唯一一种能够使正负交替且从正数开始的排列是 `[3,-2,1,-5,2,-4]`。其他排列如 `[1,-2,2,-5,3,-4]`、`[3,1,2,-2,-5,-4]`、`[-2,3,-5,1,-4,2]` 均不满足所有条件。

#### 示例 2  
**输入**  
```json
nums = [-1,1]
```  
**输出**  
```json
[1,-1]
```  
**解释**  
`1` 是唯一的正整数，`-1` 是唯一的负整数。因此只能将数组重新排列为 `[1,-1]`。

---

### 约束条件
- `2 <= nums.length <= 2 * 10^5`
- `nums.length` 为偶数
- `1 <= |nums[i]| <= 10^5`
- `nums` 中正整数的数量等于负整数的数量

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：先把所有正数和负数分别挑出来，得到两个“子序列”。  
然后交叉把它们放回原数组——先放正数，再放负数，再放下一个正数……  
这一步可以直接用 **两个列表** 来保存正负数，列表就像我们平时查字典时的“纸条”，把同类的东西放在一起，取出来很方便。

为什么这样一定能得到合法答案？  
题目保证正负数数量相等且数组长度为偶数，所以正负交叉填入后必然可以恰好填满整个数组，且每个正数后面必然跟着一个负数（或者相反），满足“正负交替”的要求。

#### 代码（Python）

```python
def rearrangeArray(nums):
    # 1️⃣ 把正数和负数分别放进两个列表
    pos = []          # 正数列表，像装正数的盒子
    neg = []          # 负数列表，像装负数的盒子
    for x in nums:
        if x > 0:
            pos.append(x)   # 正数进正数盒子
        else:
            neg.append(x)   # 负数进负数盒子

    # 2️⃣ 交叉写回原数组
    i = 0               # 原数组的写指针
    while i < len(nums):
        nums[i] = pos[i // 2]   # 偶数下标放正数，i//2 把 0,2,4 → 0,1,2
        nums[i + 1] = neg[i // 2]   # 奇数下标放负数
        i += 2          # 跳过已经填好的两格

    return nums
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了一遍原数组（把正负分开），再遍历一次把它们交叉写回。`n` 是数组长度，`O(n)` 就是说“随数组大小线性增长”，比如 `n=10⁵` 时需要大约 `10⁵` 次基本操作。  

- **空间复杂度**：`O(n)`  
  需要额外的两个列表各存一半元素，总共再占用 `n` 个位置的额外空间。  

---

### 2. 最优解  

#### 思路  

暴力解已经是 `O(n)` 的时间，但用了额外的 `O(n)` 空间。  
**瓶颈** 在于我们把正负数全部搬到了新列表，再搬回去。  
如果能够在 **原地**（不额外申请大块内存）完成交叉，就可以把空间降到 `O(1)`（只用常数级别的临时变量）。

思路如下：

1. 使用 **双指针**：  
   - `i` 从左向右扫描，负责找 **错误位置**（比如应该是正数却是负数）。  
   - `j` 从左向右扫描，负责找 **可以交换的元素**（比如当前位置是负数，但我们需要正数）。  

2. 约定 **偶数下标** 必须是正数，**奇数下标** 必须是负数。  
   - 当 `i` 指向的下标是偶数且 `nums[i]` 已经是正数，说明位置正确，`i` 前进。  
   - 当 `i` 指向奇数且 `nums[i]` 已经是负数，同理前进。  
   - 只要出现 **不匹配**（比如偶数下标却是负数），我们就把 `j` 往后找，直到找到一个可以交换的元素（奇数下标的正数），随后交换两者。

3. 由于正负数数量相等，`j` 最终一定可以找到配对元素，整个过程只遍历一次数组。

这就是经典的 **双指针原地交换** 思路，类似把一堆红球和蓝球交错排放，只用两根手指去挑选错误的球并互换。

#### 代码（Python）

```python
def rearrangeArray(nums):
    n = len(nums)
    i = 0               # 扫描指针，找“错误位置”
    j = 0               # 寻找指针，找可以交换的元素

    while i < n:
        # ① 判断 i 位置是否已经符合要求
        if (i % 2 == 0 and nums[i] > 0) or (i % 2 == 1 and nums[i] < 0):
            i += 1      # 正确，无需操作，直接看下一个位置
            continue

        # ② i 位置不对，移动 j 找到一个可以交换的元素
        j = max(j, i + 1)   # j 永远在 i 的右边，避免重复比较
        while j < n:
            # j 位置必须恰好相反（奇偶相反且符号相反）才能交换
            if (i % 2 == 0 and nums[j] > 0) or (i % 2 == 1 and nums[j] < 0):
                break
            j += 1

        # ③ 交换 i 与 j 的元素
        nums[i], nums[j] = nums[j], nums[i]
        i += 1          # 处理完 i 位置后，继续往后
        j += 1          # j 已经用了，往后继续找

    return nums
```

**关键注释**  
- `i % 2 == 0` 判断是否是偶数下标（需要正数）。  
- `nums[i] > 0` 判断当前元素是否为正数。  
- `j = max(j, i + 1)` 确保 `j` 永远在 `i` 右侧，避免回头找已经检查过的元素。  
- 交换后两指针都往前（或右）走，保证线性遍历。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每个指针最多遍历一次数组，所有操作都是常数时间的比较或交换。  

- **空间复杂度**：`O(1)`  
  只用了几个整数变量 (`i`, `j`, 临时交换用的元组)，不随 `n` 增长。  

相比暴力解，**时间相同**，但**额外空间从 `O(n)` 降到 `O(1)`**，更符合“原地”要求。

---

## 心得  

- **核心技巧**：**双指针原地交换**（Two‑pointer in‑place swap）。  
- **适用场景**：  
  1. 把数组划分为两类并交替出现（如正负交错、奇偶交错）。  
  2. “颜色分类”问题，例如 LeetCode 75. 颜色分类（把 0、1、2 排序）。  
  3. 把所有奇数放左边、偶数放右边的题目（LeetCode 905. 按奇偶排序）。  
- **一句话总结**：**用两个指针分别定位“错位”和“可补位”，原地互换即可完成交错排列。**

---

## 反思  

- **第一反应**：看到“正负数数量相等、交替排列”，立刻想到把正负分别收集后交叉合并。  
- **最容易踩的坑**：  
  - 忘记 **偶数下标必须是正数**（题目并未强制，但所有示例都是这样），导致输出 `[−2,3,…]` 被判错。  
  - 边界情况：最小长度 `2` 时，直接交换或保持顺序都要符合交替规则。  
  - 在原地交换实现时，如果 `j` 没有提前 `max(j, i+1)`，可能会出现 `j` 落在已经处理好的位置，导致无限循环。  
- **下次第一步**：先确认 **每种下标的期望符号**（正/负），然后决定是 **收集再合并** 还是 **双指针原地交换**。如果空间不是关键，收集合并更直观；若要求 O(1) 空间，立刻想到双指针原地交换。