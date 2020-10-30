# #1035. **不相交的直线** / Uncrossed Lines

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/uncrossed-lines/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2. We write the integers of nums1 and nums2 (in the order they are given) on two separate horizontal lines.
We may draw connecting lines: a straight line connecting two numbers nums1[i] and nums2[j] such that:
Note that a connecting line cannot intersect even at the endpoints (i.e., each number can only belong to one connecting line).
Return the maximum number of connecting lines we can draw in this way.

**Examples**

**Example 1:**

```
Input: nums1 = [1,4,2], nums2 = [1,2,4]
Output: 2
Explanation: We can draw 2 uncrossed lines as in the diagram.
We cannot draw 3 uncrossed lines, because the line from nums1[1] = 4 to nums2[2] = 4 will intersect the line from nums1[2]=2 to nums2[1]=2.
```

**Example 2:**

```
Input: nums1 = [2,5,1,2,5], nums2 = [10,5,2,1,5,2]
Output: 3
```

**Example 3:**

```
Input: nums1 = [1,3,7,1,7,5], nums2 = [1,9,2,5,1]
Output: 2
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 500
- 1 <= nums1[i], nums2[j] <= 2000

---

## 题目（中文翻译）

给定两个整数数组（integer array）`nums1` 和 `nums2`。我们按照给定顺序把 `nums1` 与 `nums2` 的整数分别写在两条水平线（horizontal line）上。  

我们可以画连接线（connecting line）：一条直线连接 `nums1[i]` 与 `nums2[j]`，且满足两个数相等。  

注意，连接线不能相交，即使在端点（endpoint）处也不能相交（即每个数字至多只能属于一条连接线）。  

返回能够画出的最大不相交连接线的数量。

**示例 1**  
**输入**: `nums1 = [1,4,2]`, `nums2 = [1,2,4]`  
**输出**: `2`  
**解释**: 如图所示，我们可以画出 2 条不相交的连接线。无法画出 3 条不相交的连接线，因为 `nums1[1] = 4` 与 `nums2[2] = 4` 之间的线会与 `nums1[2] = 2` 与 `nums2[1] = 2` 之间的线相交。

**示例 2**  
**输入**: `nums1 = [2,5,1,2,5]`, `nums2 = [10,5,2,1,5,2]`  
**输出**: `3`

**示例 3**  
**输入**: `nums1 = [1,3,7,1,7,5]`, `nums2 = [1,9,2,5,1]`  
**输出**: `2`

**约束条件**  
- `1 <= nums1.length, nums2.length <= 500`  
- `1 <= nums1[i], nums2[j] <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种可能的连线方式都枚举一遍，找出最多的合法连线数**。  
可以把它想象成两排小球（`nums1` 与 `nums2`），我们要在两排球之间挑选若干对相同数字的球并用线连起来，要求这些线不相交。  
暴力做法就是：

1. 从 `nums1` 的第一个元素开始，决定是否和 `nums2` 中某个相同的元素连线。  
2. 如果连了，就把这两个位置“锁定”，后面的连线只能在它们右侧继续。  
3. 如果不连，就直接跳到 `nums1` 的下一个元素。  
4. 对所有可能的选择递归搜索，记录最大的连线数量。

这相当于在两条序列上做 **“是否取这个配对”** 的二叉选择树，每一次选择都会把搜索空间分成两块：取或不取。  

> **数据结构类比**：递归的调用栈就像一本“记录每一步决定的笔记本”，每进入一次递归就往笔记本里写一行，回溯时把这行擦掉。

**为什么能得到正确答案**：递归会遍历所有合法的配对组合（即不相交的线），所以最大值必然会被搜到。

**时间/空间复杂度**  
- **时间**：每个元素都有“取 / 不取”两种决定，最坏情况下会产生 `2^{(m+n)}` 条分支（`m = len(nums1), n = len(nums2)`），所以时间复杂度是 **指数级**，记作 `O(2^{m+n})`。用大白话说，就是 **“几乎每增加一个数字，计算量就翻倍”**，在实际运行中会很快卡死。  
- **空间**：递归调用栈的深度最多是 `m + n`，所以空间复杂度是 **`O(m+n)`**，这部分相对来说比较小。

#### 代码（Python）

```python
def max_uncrossed_lines_bruteforce(nums1, nums2):
    """
    暴力递归搜索所有可能的配对方式
    返回可以画的最大不相交直线条数
    """
    m, n = len(nums1), len(nums2)

    # 递归函数：从 i 开始看 nums1，从 j 开始看 nums2，返回最多能连多少条线
    def dfs(i, j):
        # 如果任意一条线已经遍历完，后面就没有可能的连线了
        if i == m or j == n:
            return 0

        # 情况一：不把 nums1[i] 与任何 nums2 的元素连，直接跳到下一个 i
        skip_i = dfs(i + 1, j)

        # 情况二：尝试把 nums1[i] 与后面的每一个相同值的 nums2[k] 连
        take_i = 0
        for k in range(j, n):
            if nums1[i] == nums2[k]:
                # 选中这对后，后面的连线只能在 i+1、k+1 之后继续
                take_i = max(take_i, 1 + dfs(i + 1, k + 1))
        # 两种情况取最大值
        return max(skip_i, take_i)

    return dfs(0, 0)
```

> **代码说明**  
> - `dfs(i, j)` 负责计算子序列 `nums1[i:]` 与 `nums2[j:]` 的最优解。  
> - `skip_i` 表示“放弃当前 `nums1[i]`”，继续向后。  
> - `take_i` 用 `for k in range(j, n)` 找到所有可以配对的 `nums2[k]`，并递归求子问题。  
> - 最终返回两者的最大值。

#### 复杂度

- **时间复杂度**：`O(2^{m+n})`（指数级），因为每个元素都有取或不取两种选择，搜索树会指数增长。  
- **空间复杂度**：`O(m+n)`，递归栈的最大深度等于两数组长度之和。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一次递归只和当前位置的下标 `(i, j)` 有关**，也就是说，`dfs(i, j)` 的返回值只取决于 `i` 和 `j`。这正好符合**动态规划**（DP）的特征：把大问题拆成子问题，并用表格记住子问题的答案，避免重复计算。

把题目抽象一下：  
- 我们要在两条序列中挑选相同的数字，且挑选的顺序必须保持原来的相对顺序（不交叉）。  
- 这正是**最长公共子序列（Longest Common Subsequence, LCS）**的问题。  
- LCS 的标准 DP 公式是：

```
dp[i][j] =  # 以 nums1 前 i 个元素和 nums2 前 j 个元素为子序列的最大不交叉连线数
    if nums1[i-1] == nums2[j-1]:
        dp[i-1][j-1] + 1          # 两个当前位置相等，必然可以连一条线
    else:
        max(dp[i-1][j], dp[i][j-1])  # 当前位置不能连，取左上或上方的较大值
```

**为什么这个公式成立**：

- **相等时**：如果 `nums1[i-1]` 与 `nums2[j-1]` 相等，我们一定可以把它们配成一条线。此时之前的最优解只能来源于去掉这两个元素的子问题 `dp[i-1][j-1]`，再加上这条新线。
- **不相等时**：我们只能放弃其中一个元素（因为它们不能配对），于是有两种选择：  
  1. 把 `nums1[i-1]` 丢掉，答案是 `dp[i-1][j]`。  
  2. 把 `nums2[j-1]` 丢掉，答案是 `dp[i][j-1]`。  
  取两者的最大值即可。

> **类比**：想象两条绳子上各挂一排珠子，想把颜色相同的珠子用线连起来且线不交叉。我们从左到右逐步检查两条绳子当前的珠子颜色，如果颜色相同，就把这对珠子连起来（相当于把两个珠子“吃掉”，再继续往后看）；如果颜色不同，就只能把左边或上边的珠子先“丢掉”，继续比较后面的珠子。

**空间优化**  
公式只需要前一行 `dp[i-1][*]` 和当前行 `dp[i][*]`，所以可以把二维数组压缩成一维 `prev` 与 `cur` 两行，甚至只用一行滚动更新。

#### 代码（Python）

```python
def max_uncrossed_lines(nums1, nums2):
    """
    动态规划（等价于最长公共子序列）求最大不相交连线数
    时间 O(m * n)   空间 O(min(m, n))（这里用 O(n)）
    """
    m, n = len(nums1), len(nums2)

    # 为了节省空间，始终让 dp 长度等于较短的数组
    if n > m:                     # 让 nums2 成为较短的那条
        nums1, nums2 = nums2, nums1
        m, n = n, m

    dp = [0] * (n + 1)            # dp[j] 表示当前处理的 nums1 前 i 个元素 与 nums2 前 j 个元素的答案

    for i in range(1, m + 1):
        prev = 0                  # prev 保存 dp[j-1]（即左上角的值），因为 dp[j] 已经被更新为本行的值
        for j in range(1, n + 1):
            temp = dp[j]          # 先把旧的 dp[j]（即左侧的值）存起来，待下次循环作为 prev 使用
            if nums1[i - 1] == nums2[j - 1]:
                dp[j] = prev + 1   # 对角线相等，取左上角 + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])  # 取左侧或上方的最大值
            prev = temp           # 更新 prev 为左侧旧值，进入下一个 j
    return dp[n]
```

> **代码要点**  
> - `dp` 只占 `O(n)` 空间（`n` 为较短数组长度），每次遍历 `i` 时用 `prev` 保存左上角的值。  
> - `if nums1[i - 1] == nums2[j - 1]` 对应“相等可以连线”，`dp[j] = prev + 1` 把这条线计入答案。  
> - 否则 `dp[j] = max(dp[j], dp[j - 1])` 取“丢掉左边或上边”的更优解。

#### 复杂度

- **时间复杂度**：`O(m * n)`，这里的 `m`、`n` 分别是两数组长度（最多 500），即最多 25 万次循环，算得快。  
  - 与暴力解的指数级时间相比，**把“每增加一个元素只会多乘一次”**的增长变成了“每增加一个元素只会多乘另一个元素的长度”，大幅降低。
- **空间复杂度**：`O(min(m, n))`，只用了一个长度为较短数组的 1‑维 DP 表。相比于二维表的 `O(m*n)`，节省了大量内存。

---

## 心得

- **核心技巧**：把 “不相交连线” 转化为 **最长公共子序列（LCS）**，使用 **动态规划** 求解。  
- **适用的题型**  
  1. **LeetCode 1143 – Longest Common Subsequence**（直接的 LCS 题目）。  
  2. **LeetCode 1035 – Uncrossed Lines**（本题的变体，甚至可以换成字符数组）。  
  3. **LeetCode 1155 – Number of Dice Rolls With Target Sum**（也是二维 DP，思路相似）。  
- **一句话总结解题钥匙**：**“把不交叉的约束转化为保持顺序的子序列问题，使用 DP 把子问题记忆化”**。

---

## 反思

- **第一反应**：看到“不能相交的连线”，自然会想到“顺序必须保持”，于是联想到 **最长公共子序列**。  
- **最容易踩的坑**  
  1. **下标混淆**：DP 中 `dp[i][j]` 对应的是前 `i`、`j` 个元素（而不是第 `i`、`j` 个），容易写错 `i-1`、`j-1` 的索引。  
  2. **空间压缩时的左上角值**：在一维 DP 中，需要额外保存左上角的 `prev`，否则会把已经被覆盖的值误用。  
  3. **数组长度不一致**：若直接使用 `dp = [0] * (len(nums2)+1)` 而不把较短数组放在 `dp` 上，会导致不必要的空间浪费。  
- **下次遇到同类题**：第一步先判断是否可以把“不能相交 / 不能逆序”转化为“保持相对顺序的子序列”，随后尝试 **二维 DP**（或空间压缩的 DP）求解。