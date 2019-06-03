# #446. 等差子序列 II - 子序列 / Arithmetic Slices II - Subsequence

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/arithmetic-slices-ii-subsequence/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the number of all the arithmetic subsequences of nums.
A sequence of numbers is called arithmetic if it consists of at least three elements and if the difference between any two consecutive elements is the same.
A subsequence of an array is a sequence that can be formed by removing some elements (possibly none) of the array.
The test cases are generated so that the answer fits in 32-bit integer.

**Examples**

**Example 1:**

```
Input: nums = [2,4,6,8,10]
Output: 7
Explanation: All arithmetic subsequence slices are:
[2,4,6]
[4,6,8]
[6,8,10]
[2,4,6,8]
[4,6,8,10]
[2,4,6,8,10]
[2,6,10]
```

**Example 2:**

```
Input: nums = [7,7,7,7,7]
Output: 16
Explanation: Any subsequence of this array is arithmetic.
```

**Constraints**

- 1  <= nums.length <= 1000
- -231 <= nums[i] <= 231 - 1

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回 `nums` 中所有 **等差子序列**（arithmetic subsequence）的数量。  

如果一个数列包含至少三个元素且任意相邻两个元素的差值相同，则该数列称为 **等差数列**（arithmetic sequence）。  

数组的 **子序列**（subsequence）是通过删除数组中的若干（可能为零）元素而得到的序列。  

测试用例保证答案可以放入 32 位整数。

**示例 1**  
**输入**: `nums = [2,4,6,8,10]`  
**输出**: `7`  
**解释**: 所有的等差子序列切片如下:
- `[2,4,6]`
- `[4,6,8]`
- `[6,8,10]`
- `[2,4,6,8]`
- `[4,6,8,10]`
- `[2,4,6,8,10]`
- `[2,6,10]`

**示例 2**  
**输入**: `nums = [7,7,7,7,7]`  
**输出**: `16`  
**解释**: 该数组的任意子序列都是等差的。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `-2^31 <= nums[i] <= 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组的 **所有子序列**（不要求连续）都枚举出来，  
然后把每个子序列的长度 ≥ 3 的部分检查一下：相邻两数的差值是否相同。  

- **子序列**可以想象成“从一排水果中挑选一些”，挑不挑都可以，只要保持原来的顺序。  
- 为了枚举子序列，我们可以用 **位掩码**（mask）来表示是否保留第 `i` 个元素：  
  `mask` 的第 `i` 位为 `1` → 取 `nums[i]`，为 `0` → 丢掉它。  
- 检查是否为等差数列时，只要遍历一次子序列，记录第一次出现的差 `d`，随后每一对相邻数的差都要等于 `d`。

**为什么这个方法一定能得到答案**  
因为它把 **所有可能的子序列** 都遍历了一遍，凡是满足等差条件且长度≥3 的子序列，都一定会被计数。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def numberOfArithmeticSlices_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 2^n - 1 种非空子集（这里用二进制枚举）
    for mask in range(1 << n):
        # 只保留长度 >= 3 的子序列
        if bin(mask).count('1') < 3:
            continue

        seq = []
        for i in range(n):
            if mask & (1 << i):          # 第 i 位为 1 → 取这个元素
                seq.append(nums[i])

        # 判断 seq 是否为等差数列
        diff = seq[1] - seq[0]           # 第一个差值
        ok = True
        for i in range(2, len(seq)):
            if seq[i] - seq[i-1] != diff:
                ok = False
                break
        if ok:
            ans += 1

    return ans
```

> **关键行中文注释** 已写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度：** `O(2^n * n)`  
  - 解释：我们要遍历 `2^n` 种子集，每个子集最多要遍历 `n` 次来收集元素并检查等差性。  
  - 对于 `n = 20` 已经是几百万次，`n = 1000` 则根本不可行。

- **空间复杂度：** `O(n)`  
  - 只用到临时的 `seq` 列表，最多存 `n` 个元素。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于 **“枚举所有子序列”**，这一步导致指数级时间。  
其实我们不需要一次性生成完整的子序列，只要 **在遍历数组的过程中，记录以当前元素结尾的等差子序列数量**，就可以把问题拆成若干个 **子问题**，进而使用 **动态规划**（DP）来合并。

**核心想法**  
- 对每个位置 `i`，维护一个哈希表 `dp[i]`：  
  `dp[i][d] =` 以 `nums[i]` 为结尾、公共差为 `d` 的等差子序列（**长度 ≥ 2**）的个数。  
  - “长度 ≥ 2” 是因为当我们只看两个数时，差 `d` 总是确定的，后面再加入第三个数才算真正的等差子序列。  
- 当我们固定右端点 `i`，枚举左端点 `j < i`：  
  1. 计算差值 `d = nums[i] - nums[j]`（可能是负数或很大的数，哈希表可以直接存）。  
  2. `cnt_j = dp[j].get(d, 0)` → 以 `j` 为结尾、差为 `d` 的子序列数。  
  3. 这些 `cnt_j` 条序列每条都可以 **在末尾加上 `nums[i]`**，形成长度 ≥ 3 的等差子序列，**立即计入答案**。  
  4. 同时，`(nums[j], nums[i])` 这对两数也构成一个长度为 2 的等差序列，应该放进 `dp[i][d]`，为以后更右侧的元素提供扩展的可能。  
- 最后把所有 `cnt_j` 加到答案中，就得到了 **所有长度≥3 的等差子序列** 的数量。

**为什么这样能算对**  
- 每条合法的等差子序列必然有唯一的“最后两个元素”。  
  当我们在遍历到这两个元素时（左端点 `j`，右端点 `i`），恰好会把这条序列计一次。  
- 由于我们只在 **右端点** `i` 时把对应的 `cnt_j` 加到答案，**不会重复计数**。  

**类比**  
把每个 `dp[i]` 想象成一本“小账本”，记录“我（`nums[i]`）和之前的谁配对，差是多少，配对了多少次”。  
当新同学 `nums[i]` 来到时，他会去翻前面的账本，找所有和自己差相同的配对，**把这些配对的数量直接算进总成绩**，并把自己和这些同学的配对记录下来，供以后更后面的同学继续使用。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def numberOfArithmeticSlices(nums: List[int]) -> int:
    n = len(nums)
    # dp[i] 是一个字典，key 为差值 d，value 为以 nums[i] 结尾、差为 d 的等差子序列（长度 >= 2）的个数
    dp = [defaultdict(int) for _ in range(n)]
    ans = 0

    for i in range(n):
        for j in range(i):
            d = nums[i] - nums[j]                # 公共差

            # 以 j 为结尾、差为 d 的序列数（可能为 0）
            cnt_j = dp[j][d]

            # 这些序列每条加上 nums[i] 后，长度 >= 3，计入答案
            ans += cnt_j

            # (nums[j], nums[i]) 本身是一条长度为 2 的等差序列，放进 dp[i] 为以后扩展做准备
            dp[i][d] += cnt_j + 1   # +1 表示新建的这条两元素序列

    return ans
```

> 代码中的每一行都配有中文注释，直接运行即可得到答案。

#### 复杂度

- **时间复杂度：** `O(n^2)`  
  - 解释：外层遍历 `i`（`n` 次），内层遍历 `j < i`（平均约 `n/2` 次），每次只做 `O(1)` 的哈希表查/增操作。  
  - 与暴力解的 `2^n` 相比，`n` 最多只有 1000，`n^2 = 10⁶` 完全可以接受。

- **空间复杂度：** `O(n^2)`（最坏情况）  
  - 每个 `dp[i]` 最多可能存 `i` 条不同的差值，全部加起来最多 `n*(n-1)/2` 条记录。  
  - 实际上差值的种类往往远小于 `n^2`，但在最坏情况下仍需 `O(n^2)` 空间。

---

## 心得

- **核心技巧**：**以「差值」为键的动态规划 + 哈希表**，把「所有子序列」的枚举转化为「每个元素的局部贡献」的累加。  
- **适用的题型**（类似思路）  
  1. **LeetCode 1027 – Longest Arithmetic Subsequence**（求最长等差子序列长度）  
  2. **LeetCode 873 – Length of Longest Fibonacci Subsequence**（用差值/和做状态）  
  3. **LeetCode 698 – Partition to K Equal Sum Subsets**（利用子集状态转移的 DP 思路）  
- **一句话总结解题钥匙**：  
  “把等差子序列的 **最后两个元素** 当成决定因素，使用哈希表记录每个差值的出现次数，逐步累加即得全部答案。”

---

## 反思

- **第一反应**：直接想到「枚举所有子序列」——最直观但不可行。  
- **最容易踩的坑**  
  - **整数差值溢出**：在 C/C++ 中需要使用 `long long`，但 Python 的整数无限大，直接使用即可。  
  - **计数重复**：如果把长度为 2 的序列也直接加入答案，会把不满足“至少 3 个元素”的情况算进去。必须只把**已有长度≥2 的序列**扩展后计数。  
  - **负差值和零差值**：差值可以为负或 0，哈希表必须能够接受任意整数键。  
- **下次遇到同类题**，第一步应该思考：  
  “这类子序列/子集问题，能否把 **局部信息（如差值、和、长度）** 用哈希表/数组记录下来，进而在遍历时逐步累加？”  
  这种「**状态压缩 + 动态规划**」的思路往往能把指数级暴力降到多项式时间。