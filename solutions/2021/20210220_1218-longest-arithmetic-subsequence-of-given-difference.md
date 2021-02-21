# #1218. 给定差值的最长等差子序列 / Longest Arithmetic Subsequence of Given Difference

> 难度：中等 · 标签：Array、Hash Table、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/)

---

## 题目（英文原版）

**Description**

Given an integer array arr and an integer difference, return the length of the longest subsequence in arr which is an arithmetic sequence such that the difference between adjacent elements in the subsequence equals difference.
A subsequence is a sequence that can be derived from arr by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,4], difference = 1
Output: 4
Explanation: The longest arithmetic subsequence is [1,2,3,4].
```

**Example 2:**

```
Input: arr = [1,3,5,7], difference = 1
Output: 1
Explanation: The longest arithmetic subsequence is any single element.
```

**Example 3:**

```
Input: arr = [1,5,7,8,5,3,4,2,1], difference = -2
Output: 4
Explanation: The longest arithmetic subsequence is [7,5,3,1].
```

**Constraints**

- 1 <= arr.length <= 105
- -104 <= arr[i], difference <= 104

---

## 题目（中文翻译）

给定一个整数数组 `arr` 和一个整数 `difference`，返回 `arr` 中满足以下条件的最长子序列（subsequence）的长度：该子序列是等差数列（arithmetic sequence），并且子序列中相邻元素的差恰好等于 `difference`。

子序列（subsequence）是指通过删除 `arr` 中的若干（也可以不删）元素而得到的序列，删除元素后剩余元素的相对顺序保持不变。

### 示例

**示例 1**  
输入: `arr = [1,2,3,4]`, `difference = 1`  
输出: `4`  
解释: 最长的等差子序列是 `[1,2,3,4]`。

**示例 2**  
输入: `arr = [1,3,5,7]`, `difference = 1`  
输出: `1`  
解释: 最长的等差子序列只能是任意单个元素。

**示例 3**  
输入: `arr = [1,5,7,8,5,3,4,2,1]`, `difference = -2`  
输出: `4`  
解释: 最长的等差子序列是 `[7,5,3,1]`。

### 约束条件

- `1 <= arr.length <= 10^5`
- `-10^4 <= arr[i], difference <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的子序列都枚举出来，检查每一个子序列是否满足相邻元素之差等于 `difference`，然后记录最长的长度。

- **枚举子序列**：可以把数组的每个元素看成“要不要保留”。如果把 `arr` 长度记为 `n`，每个位置有两种选择（保留或删除），于是一共有 `2ⁿ` 种子序列。  
- **检查等差**：遍历子序列中的元素，判断相邻两数之差是否都是 `difference`。如果是，就把它的长度和当前答案比较，取最大。

> **类比**：想象你有一堆不同颜色的珠子，要挑出颜色相邻差为固定值的最长串。最笨的办法就是把所有可能的挑选方式都列出来，再逐个检查。

**为什么这个方法正确**  
因为我们遍历了**全部**合法的子序列，只要其中有最长的等差子序列，就一定会被检测到。只要检查过程没有漏掉，就一定能得到正确答案。

**复杂度分析**  
- 时间复杂度：枚举 `2ⁿ` 种子序列，每种子序列最坏要遍历 `n` 次检查等差，整体是 `O(n·2ⁿ)`。这在实际中几乎不可接受，尤其 `n` 达到 10⁵ 时根本跑不完。  
- 空间复杂度：递归或位掩码实现时需要 `O(n)` 的栈空间或临时数组来保存当前子序列。

> **大白话**：`O(n·2ⁿ)` 就像在一条无限长的路上不停地分叉，每次分叉都要把所有可能的路径都走一遍，根本不可能在合理时间内走完。

#### 代码（Python）

```python
from itertools import combinations

def longest_arith_seq_bruteforce(arr, difference):
    n = len(arr)
    best = 0

    # 枚举所有长度 >= 1 的子序列（使用组合生成器）
    for length in range(1, n + 1):
        for idxs in combinations(range(n), length):   # idxs 是子序列在原数组中的下标
            seq = [arr[i] for i in idxs]                # 还原子序列的真实数值
            # 检查是否是等差序列
            ok = True
            for i in range(1, len(seq)):
                if seq[i] - seq[i - 1] != difference:
                    ok = False
                    break
            if ok:
                best = max(best, len(seq))

    return best
```

> 这段代码仅用于演示思路，**不要**在正式提交时使用。

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)` — 随着 `n` 增大，计算量会呈指数级爆炸。  
- **空间复杂度**：`O(n)` — 用来存放当前子序列的临时列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的**瓶颈**在于“枚举所有子序列”。我们并不需要关心子序列的具体排列，只要知道**每个数能否接在已有的等差序列后面**即可。

**关键观察**：

> 如果我们已经知道以值 `x` 结尾的最长等差子序列长度是 `len_x`，那么当遍历到元素 `y = x + difference` 时，就可以把 `y` 接在这条序列后面，得到长度 `len_x + 1`。

这正好可以用**哈希表**（Python 中的 `dict`）来保存“以某个数结尾的最长序列长度”。遍历数组一次，动态更新哈希表：

- `dp[val]` 表示**以值 `val` 为结尾**的最长等差子序列长度。  
- 对于当前元素 `num`，我们检查 `num - difference` 是否已经出现过（即 `dp` 中是否有对应的键）。  
  - 若出现，则 `dp[num] = dp[num - difference] + 1`。  
  - 若没有，则只能单独成一个序列，`dp[num] = 1`。  
- 同时维护全局最大值 `ans`。

> **类比**：把每个数字想成一本书的页码，`difference` 就是“相邻两页的距离”。我们在一本“查找表”里记录每一页可以组成的最长连续章节。看到新页码时，只要查找前一页（`页码 - distance`）的章节长度，就能快速拼接出更长的章节。

**为什么正确**  

- **局部最优等于全局最优**：对任意以 `num` 结尾的合法等差子序列，倒数第二个元素必然是 `num - difference`。所以最长的以 `num` 结尾的序列，一定是 **最长的以 `num - difference` 结尾的序列** 再加上 `num` 本身。递推关系正是 `dp[num] = dp[num - difference] + 1`。  
- **遍历顺序**：我们按数组的原始顺序遍历，保证了子序列的相对位置不被打乱——因为只有在前面出现的元素才能被当作前驱加入当前序列。

**核心数据结构**：哈希表（字典）  
- 读取/写入均是 **O(1)** 平均时间，适合处理 `10⁵` 规模的数组。

#### 代码（Python）

```python
def longest_arith_seq(arr, difference):
    """
    返回最长等差子序列的长度，等差为 difference。
    dp[val] 表示以 val 结尾的最长子序列长度。
    """
    dp = {}          # 哈希表：key = 数值，value = 最长长度
    ans = 0          # 全局最大长度

    for num in arr:
        # 前驱的值
        prev = num - difference

        # 如果前驱已经出现过，接在它后面；否则单独成序列
        if prev in dp:
            dp[num] = dp[prev] + 1
        else:
            dp[num] = 1

        # 更新答案
        if dp[num] > ans:
            ans = dp[num]

    return ans
```

> 代码仅用了几行核心逻辑，注释帮助初学者理解每一步的意义。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，每次哈希表查找/写入是常数时间。相当于“线性时间”，即使 `n = 10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(m)` — `m` 为不同数值的种类数，最坏情况下 `m = n`（所有元素互不相同），因此最多需要 `O(n)` 的额外空间来存哈希表。

---

## 心得

- **核心技巧**：利用哈希表记录“以某个数结尾的最长等差子序列长度”，实现 **动态规划** 的 O(1) 状态转移。  
- **适用题型**  
  1. “最长等差子序列”（本题的变体，difference 需要自行搜索）  
  2. “最长递增子序列的长度” → 使用 `dp[val]` 记录以 `val` 结尾的最长递增序列（可结合二分搜索实现 `O(n log n)`)  
  3. “最长同值子序列” → `dp[x]` 记录出现次数，直接统计最大频率  

- **一句话总结解题钥匙**：**“把‘以当前值结尾的最优解’存进哈希表，遇到新值只要查找前驱即可快速递推”。**

---

## 反思

- **第一反应**：看到“subsequence + fixed difference”，第一时间会想到枚举所有子序列或使用 DP。  
- **最容易踩的坑**  
  - 忘记子序列必须保持原数组的相对顺序，不能随意排序后再求等差。  
  - 负数差值会导致前驱 `num - difference` 变大，必须在哈希表中正确查找（不要写成 `num + difference`）。  
  - 大数组时若误用了 `O(n²)` 或指数级算法，会导致超时。  
- **下次遇到同类题**：第一步先思考“能否把状态压缩成‘以某个值/下标结尾’”，然后寻找 **O(1)** 的转移方式（哈希表、前缀和、单调栈等），再决定是否需要进一步优化空间。