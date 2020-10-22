# #1027. **最长算术子序列** / Longest Arithmetic Subsequence

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-arithmetic-subsequence/)

---

## 题目（英文原版）

**Description**

Given an array nums of integers, return the length of the longest arithmetic subsequence in nums.
Note that:

**Examples**

**Example 1:**

```
Input: nums = [3,6,9,12]
Output: 4
Explanation:  The whole array is an arithmetic sequence with steps of length = 3.
```

**Example 2:**

```
Input: nums = [9,4,7,2,10]
Output: 3
Explanation:  The longest arithmetic subsequence is [4,7,10].
```

**Example 3:**

```
Input: nums = [20,1,15,3,10,5,8]
Output: 4
Explanation:  The longest arithmetic subsequence is [20,15,10,5].
```

**Constraints**

- 2 <= nums.length <= 1000
- 0 <= nums[i] <= 500

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回其中最长算术子序列（arithmetic subsequence）的长度。

> **算术子序列**：在原数组中按照下标递增的顺序挑选若干元素形成的序列，若相邻元素的差值相同，则该序列为算术子序列。

---

### 示例

**示例 1**  
**输入**: `nums = [3,6,9,12]`  
**输出**: `4`  
**解释**: 整个数组本身就是步长（step）为 `3` 的算术子序列。

**示例 2**  
**输入**: `nums = [9,4,7,2,10]`  
**输出**: `3`  
**解释**: 最长的算术子序列是 `[4,7,10]`。

**示例 3**  
**输入**: `nums = [20,1,15,3,10,5,8]`  
**输出**: `4`  
**解释**: 最长的算术子序列是 `[20,15,10,5]`。

---

### 约束条件

- `2 <= nums.length <= 1000`
- `0 <= nums[i] <= 500`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举每一种可能的等差数列**，然后看看它到底能有多长。  
具体做法：

1. 先选两个下标 `i < j`，把 `nums[i]` 和 `nums[j]` 当作等差数列的前两项。  
2. 由这两项可以算出公差 `diff = nums[j] - nums[i]`。  
3. 从下标 `j+1` 开始往后遍历，如果后面的元素恰好等于 `前一项 + diff`，就把它接到序列里。  
4. 记录下遍历得到的最长长度。

可以把 **哈希表** 想象成一本“查字典”，`key` 是“公差”，`value` 是“已经找到的等差序列的长度”。在暴力解里我们不需要这个字典，只是把每一次枚举的过程写成循环。

这种做法一定能得到正确答案，因为我们把**所有可能的起点和公差**都尝试了一遍，遗漏的情况不可能出现。

> **为什么会慢**  
> 这里有三层循环：  
> - 第一层遍历 `i`（≈ n 次）  
> - 第二层遍历 `j`（≈ n 次）  
> - 第三层再遍历一次数组去找后面的符合公差的数（≈ n 次）  
> 所以总的操作次数大约是 `n³`，当 `n` 达到 1000 时会非常慢。

#### 代码（Python）
```python
def longestArithSeqLength_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 枚举前两项的下标 i、j
    for i in range(n):
        for j in range(i + 1, n):
            diff = nums[j] - nums[i]          # 公差
            length = 2                         # 已经有两项
            prev = nums[j]                     # 当前序列的最后一项

            # 从 j 之后继续找满足等差的数
            for k in range(j + 1, n):
                if nums[k] - prev == diff:     # 符合公差
                    length += 1
                    prev = nums[k]

            ans = max(ans, length)             # 更新全局最长

    return ans
```

#### 复杂度
- **时间复杂度：** `O(n³)`  
  “立方”意思是如果把 `n` 想成 10，执行次数大概是 10 × 10 × 10 = 1000；`n` 越大，耗时会呈指数级增长。
- **空间复杂度：** `O(1)`  
  只用了常数级别的额外变量（计数器、差值等），不随 `n` 增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**重复遍历**：相同的子问题会被多次计算。我们可以把“以某个位置结尾、且公差为 diff 的最长等差子序列长度”记下来，下次需要时直接取，用**动态规划 + 哈希表**来实现。

核心想法：

1. **状态定义**  
   `dp[i][diff]` 表示「以 `nums[i]` 为结尾，公差为 `diff` 的最长等差子序列的长度」。

2. **状态转移**  
   对于每一对下标 `(j, i)`（`j < i`），设 `diff = nums[i] - nums[j]`。  
   - 如果在 `j` 位置已经有以相同 `diff` 的序列（即 `dp[j][diff]` 存在），我们可以在它的基础上把 `nums[i]` 接在后面，长度加 1。  
   - 否则，`nums[j]` 和 `nums[i]` 本身就可以构成长度为 2 的等差序列。  

   用公式写就是  
   `dp[i][diff] = dp[j].get(diff, 1) + 1`  
   这里的 `1` 表示「只算 `nums[j]` 本身」，再加上 `nums[i]` 就是长度 2。

3. **哈希表的作用**  
   对每个下标 `i`，我们维护一个 **字典**（相当于“查字典”），`key` 是公差 `diff`，`value` 是对应的最长长度。这样查、写都是 `O(1)`。

4. **遍历顺序**  
   外层遍历 `i`（从左到右），内层遍历所有 `j < i`。因为我们只需要已经处理好的 `j` 的信息，所以这种顺序是合法的。

5. **答案收集**  
   在更新 `dp[i][diff]` 的同时，维护一个全局最大值 `ans`，最后返回它即可。

> **为什么快**  
> 只用了两层循环（`O(n²)`），每次只做 `O(1)` 的哈希表查找/写入，避免了第三层遍历。

#### 代码（Python）
```python
from collections import defaultdict

def longestArithSeqLength(nums):
    n = len(nums)
    # dp[i] 是一个字典：diff -> 以 i 为结尾的等差子序列最长长度
    dp = [defaultdict(int) for _ in range(n)]
    ans = 0

    for i in range(n):
        for j in range(i):
            diff = nums[i] - nums[j]                     # 公差

            # dp[j][diff] 若不存在则默认为 1（只算 nums[j] 本身）
            # 加上 nums[i] 后长度加 1
            dp[i][diff] = dp[j].get(diff, 1) + 1

            ans = max(ans, dp[i][diff])                 # 更新全局最大

    return ans
```

#### 复杂度
- **时间复杂度：** `O(n²)`  
  两层循环，每层最多遍历 `n` 次，`n=1000` 时大约是 1 000 000 次操作，能够在毫秒级完成。  
- **空间复杂度：** `O(n²)`（最坏情况）  
  每个 `dp[i]` 最多会存放 `i` 个不同的 `diff`，总数约为 `n(n‑1)/2`。在本题的数值范围（`0 ≤ nums[i] ≤ 500`）下，实际占用会更少。

---

## 心得

- **核心技巧**：用「以当前位置 + 公差」为键的哈希表记录子序列长度，属于「状态压缩」的动态规划思路。  
- **适用的题型**  
  1. **最长斐波那契子序列**（Longest Fibonacci Subsequence）——同样用 `dp[i][j]` 记录以 `i, j` 为结尾的最长长度。  
  2. **最长等差子数组**（Longest Arithmetic Subarray）——虽然是连续的，但可以用类似的差值映射思路快速判断。  
  3. **最长递增子序列**（Longest Increasing Subsequence）——也可以用「以 i 为结尾」的 DP 思路，只是状态转移不同。  
- **一句话总结**：**把“以某个位置、某个公差”作为状态，用字典记住最长长度，避免重复枚举。**

---

## 反思

- **第一反应**：看到“等差子序列”，立刻想到枚举公差并逐个检查，结果是暴力三层循环。  
- **最容易踩的坑**  
  1. **公差的范围**：`diff` 可能为负数，需要在字典里允许负键。  
  2. **长度的初始值**：如果直接写 `dp[i][diff] = dp[j][diff] + 1`，在 `dp[j][diff]` 不存在时会报错或得到错误结果，需要使用 `get(..., 1)` 或手动判断。  
  3. **返回值**：即使所有子序列长度都只有 2，答案也应该是 2，不能忘记在遍历结束后返回 `ans`（而不是默认的 0）。  
- **下次第一步**：先思考「能否把子问题抽象成‘以某个位置结束’的状态」；如果可以，就尝试用哈希表把不同的公差分开记录，从而把三层循环压到两层。