# #3201. 最长有效子序列 I / Find the Maximum Length of Valid Subsequence I

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-i/)

---

## 题目（英文原版）

**Description**

A subsequence sub of nums with length x is called valid if it satisfies:
Return the length of the longest valid subsequence of nums.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 4
Explanation:
The longest valid subsequence is [1, 2, 3, 4] .
```

**Example 2:**

```
Input: nums = [1,2,1,1,2,1,2]
Output: 6
Explanation:
The longest valid subsequence is [1, 2, 1, 2, 1, 2] .
```

**Example 3:**

```
Input: nums = [1,3]
Output: 2
Explanation:
The longest valid subsequence is [1, 3] .
```

**Constraints**

- 2 <= nums.length <= 2 * 105
- 1 <= nums[i] <= 107

---

## 题目（中文翻译）

一个长度为 `x` 的子序列（subsequence） `sub` 若满足以下条件，则称其为 **有效**（valid）：

>（题目原文中缺失具体条件，保持原样）

返回 `nums` 中最长有效子序列的长度。  

子序列是指可以通过删除原数组中的若干（或不删除）元素而得到的数组，且删除后剩余元素的相对顺序保持不变。

## 示例

### 示例 1
**输入**  
```json
nums = [1,2,3,4]
```
**输出**  
```
4
```
**解释**  
最长的有效子序列是 `[1, 2, 3, 4]`。

### 示例 2
**输入**  
```json
nums = [1,2,1,1,2,1,2]
```
**输出**  
```
6
```
**解释**  
最长的有效子序列是 `[1, 2, 1, 2, 1, 2]`。

### 示例 3
**输入**  
```json
nums = [1,3]
```
**输出**  
```
2
```
**解释**  
最长的有效子序列是 `[1, 3]`。

## 约束条件
- `2 <= nums.length <= 2 * 10^5`
- `1 <= nums[i] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子序列**，检查每个子序列是否满足“合法”的要求，记录最长的长度。  

- **子序列**：把原数组里不需要的元素删掉，剩下的顺序不变。可以把它想象成从一串珠子中挑选出若干颗珠子，挑选的顺序不能倒置。  
- **合法条件**：根据题目提示，合法的子序列只能是以下四种形式之一  
  1. 全部是偶数  
  2. 全部是奇数  
  3. 偶‑奇‑偶‑奇…（交替，且第一个是偶数）  
  4. 奇‑偶‑奇‑偶…（交替，且第一个是奇数）  

暴力做法就是：  
1. 生成 **所有** 子序列（这一步的复杂度是 2ⁿ，几乎不可能直接实现，但我们用一个更“可行”的 DP 方式来近似）  
2. 对每个子序列判断它属于哪一种合法形式  
3. 记录最长的合法长度  

下面给出一种 **O(n²)** 的动态规划实现，它不需要真的枚举 2ⁿ 个子序列，只是对每个位置 `i` 检查它能否接在之前的合法子序列后面。  

> **为什么这种做法是正确的？**  
> 对每个元素 `nums[i]`，我们只关心它能否接在前面已经得到的合法子序列后面。如果能接上，就把长度加 1；否则保持原来的最长长度。遍历完所有元素后，最大的 DP 值就是答案。

#### 代码（Python）

```python
from typing import List

def longestValidSubsequence_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # dp[i] 表示以 nums[i] 结尾的最长合法子序列长度
    dp = [1] * n                     # 每个单独的元素本身就是长度为 1 的合法子序列
    ans = 1

    for i in range(n):
        for j in range(i):
            # 判断 nums[j] → nums[i] 这一步是否满足合法的转移
            # 1) 同奇同偶：两者奇偶相同，且之前已经是“全奇”或“全偶”
            # 2) 交替：奇偶不同，且之前是交替序列（这里用 parity[j] 判断）
            if (nums[j] % 2 == nums[i] % 2) or (nums[j] % 2 != nums[i] % 2):
                # 只要两数能接在一起，就可以把 dp[i] 更新为更长的值
                dp[i] = max(dp[i], dp[j] + 1)
        ans = max(ans, dp[i])

    return ans
```

> **关键注释**  
> - `dp[i] = 1` 表示最小合法子序列只能是自己。  
> - 两层循环 `i`、`j` 相当于“把每个元素尝试接在所有前面的合法子序列后面”，所以时间是 **平方级**。  
> - `ans` 用来记录全局最大长度。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - “平方级”意思是如果数组长度是 10,000，算法大约要跑 10,000 × 10,000 = 1 亿次循环，明显会超时。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的数组 `dp`，相当于存了每个位置的中间结果。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于两层循环**：我们每次都要遍历所有前面的元素去判断能否接上。实际上，合法子序列的形态只有 **4 种**（全偶、全奇、偶‑奇交替、奇‑偶交替），不需要对每个前缀都检查，只要**一次遍历**即可统计每种形态能得到的最长长度。

**一步步推导**：

1. **只关心奇偶**  
   题目只在意数字的奇偶性（是奇数还是偶数），数字本身的大小并不影响合法性。于是把每个数映射为 `0`（偶）或 `1`（奇），相当于把原数组压缩成一串 “偶/奇” 标记。

2. **四种模式**  
   - **全偶**：只要是偶数就可以加入，奇数永远跳过。  
   - **全奇**：只要是奇数就可以加入，偶数永远跳过。  
   - **偶‑奇交替**：期待的奇偶序列是 `0,1,0,1,…`（从偶数开始）。每遇到符合当前期待的元素就把长度 +1，并把期待翻转。  
   - **奇‑偶交替**：期待的序列是 `1,0,1,0,…`（从奇数开始），同理。

3. **一次遍历即可求出四个答案**  
   - 维护四个计数器 `cnt_all_even, cnt_all_odd, cnt_alt_even_start, cnt_alt_odd_start`。  
   - 对每个元素 `x`（奇偶 `p = x % 2`）进行如下操作：  
     - 如果 `p == 0`（偶），`cnt_all_even += 1`。  
     - 如果 `p == 1`（奇），`cnt_all_odd += 1`。  
     - 对交替序列，需要判断当前元素是否 **恰好**是我们期待的奇偶：  
       - `expected = cnt_alt_even_start % 2`（因为交替序列的第 `k` 个位置奇偶等于 `k%2`），若 `p == expected`，则 `cnt_alt_even_start += 1`。  
       - 同理，`expected = (cnt_alt_odd_start + 1) % 2`（因为从奇数开始），若匹配则 `cnt_alt_odd_start += 1`。

4. **答案是四个计数器的最大值**。

> **类比**：想象你在排队买票，队伍里只能是全男、全女、男女交替或女男交替四种规则。只要你一次走过去，分别记录每种规则能让多少人进入队伍，最后取最大的那一个即可。

#### 代码（Python）

```python
from typing import List

def longestValidSubsequence(nums: List[int]) -> int:
    # 四种模式对应的计数器
    cnt_all_even = 0          # 只收偶数
    cnt_all_odd = 0           # 只收奇数
    cnt_alt_even_start = 0    # 偶-奇-偶-奇...（从偶数开始）
    cnt_alt_odd_start = 0     # 奇-偶-奇-偶...（从奇数开始）

    for x in nums:
        parity = x & 1  # 1 表示奇数，0 表示偶数

        # 1) 全偶
        if parity == 0:
            cnt_all_even += 1

        # 2) 全奇
        if parity == 1:
            cnt_all_odd += 1

        # 3) 偶-奇交替（先期待偶数）
        # 交替序列的第 k (0-index) 个位置应该是 k%2（0 表示偶，1 表示奇）
        expected_parity_even_start = cnt_alt_even_start % 2
        if parity == expected_parity_even_start:
            cnt_alt_even_start += 1

        # 4) 奇-偶交替（先期待奇数）
        # 这里第 0 位应该是奇数（1），所以期望是 (cnt+1)%2
        expected_parity_odd_start = (cnt_alt_odd_start + 1) % 2
        if parity == expected_parity_odd_start:
            cnt_alt_odd_start += 1

    # 四种情况取最长的那个
    return max(cnt_all_even, cnt_all_odd,
               cnt_alt_even_start, cnt_alt_odd_start)
```

> **关键注释**  
> - `parity = x & 1` 用位运算快速得到奇偶（`&` 是按位与）。  
> - `expected_parity_even_start = cnt_alt_even_start % 2`：因为我们已经收到了 `cnt_alt_even_start` 个元素，下一位的奇偶正好是 `cnt % 2`。  
> - `expected_parity_odd_start = (cnt_alt_odd_start + 1) % 2`：从奇数开始的交替序列，第 0 位应为奇（1），所以把计数再加一再取模得到期望。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，`n` 是数组长度。相比暴力的 `n²`，这里的“线性”意味着如果 `n = 200,000`，只需要大约 200,000 次操作，几乎瞬间完成。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数计数器，和 `n` 的大小无关，称为“常数级”空间。

---

## 心得

- **核心技巧**：把问题抽象成「只有 4 种可能的奇偶模式」并一次遍历统计，每种模式只需要维护一个计数器。  
- **适用的题型**  
  1. 只关心元素「属性」而非具体数值的最长子序列（如只看正负、大小关系等）。  
  2. “交替”或“全部相同”类型的约束（比如“最长交替升降序列”“全部相同颜色的子序列”）。  
  3. 需要在 O(n) 内求解的「固定模式」匹配问题（如判断字符串是否能形成交替字符序列）。  
- **一句话总结**：**把所有合法形态列举完，线性扫描一次把每种形态的最长长度都算出来，取最大即可。**

---

## 反思

- **第一反应**：看到“合法子序列”想到“枚举所有子序列”，于是写了暴力的 DP。  
- **最容易踩的坑**  
  1. **忘记只看奇偶**：如果把原始数值当成比较对象，算法会变得复杂且错误。  
  2. **交替序列的起始期望写错**：容易把 “奇‑偶‑奇‑偶” 的期望写成 `cnt % 2`，导致计数错位。  
  3. **边界情况**：数组全是偶数或全是奇数时，交替计数器会一直保持 0，不能因为 “期待奇数却永远没有” 而导致错误。  
- **下次第一步**：先把题目限制抽象成「几种固定模式」——如果模式数量很少（常数），就尝试一次遍历统计每种模式的最长长度，而不是直接枚举子序列。这样可以迅速把时间复杂度降到线性。