# #2002. 两个回文子序列长度乘积的最大值 / Maximum Product of the Length of Two Palindromic Subsequences

> 难度：中等 · 标签：String、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/)

---

## 题目（英文原版）

**Description**

Given a string s, find two disjoint palindromic subsequences of s such that the product of their lengths is maximized. The two subsequences are disjoint if they do not both pick a character at the same index.
Return the maximum possible product of the lengths of the two palindromic subsequences.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters. A string is palindromic if it reads the same forward and backward.

**Examples**

**Example 1:**

```
Input: s = "leetcodecom"
Output: 9
Explanation: An optimal solution is to choose "ete" for the 1st subsequence and "cdc" for the 2nd subsequence.
The product of their lengths is: 3 * 3 = 9.
```

**Example 2:**

```
Input: s = "bb"
Output: 1
Explanation: An optimal solution is to choose "b" (the first character) for the 1st subsequence and "b" (the second character) for the 2nd subsequence.
The product of their lengths is: 1 * 1 = 1.
```

**Example 3:**

```
Input: s = "accbcaxxcxx"
Output: 25
Explanation: An optimal solution is to choose "accca" for the 1st subsequence and "xxcxx" for the 2nd subsequence.
The product of their lengths is: 5 * 5 = 25.
```

**Constraints**

- 2 <= s.length <= 12
- s consists of lowercase English letters only.

---

## 题目（中文翻译）

给定一个字符串 `s`，请找出两个互不相交的回文子序列（palindromic subsequence），使得它们长度的乘积最大。若两个子序列没有在同一索引处选取字符，则称它们是互不相交的（disjoint）。返回两个回文子序列长度乘积的最大可能值。

子序列（subsequence）是指可以通过删除原字符串中的若干字符（也可以不删除）而得到的字符串，且剩余字符的相对顺序保持不变。若一个字符串正读和反读相同，则称其为回文（palindromic）。

**示例 1**  
**输入**: `s = "leetcodecom"`  
**输出**: `9`  
**解释**: 一种最优方案是选取第一个子序列为 `"ete"`，第二个子序列为 `"cdc"`。它们长度的乘积为 `3 * 3 = 9`。

**示例 2**  
**输入**: `s = "bb"`  
**输出**: `1`  
**解释**: 最优方案是将第一个子序列选为第一个字符 `"b"`，第二个子序列选为第二个字符 `"b"`，乘积为 `1 * 1 = 1`。

**示例 3**  
**输入**: `s = "accbcaxxcxx"`  
**输出**: `25`  
**解释**: 最优方案是选取第一个子序列为 `"accca"`，第二个子序列为 `"xxcxx"`，乘积为 `5 * 5 = 25`。

**约束条件**  
- `2 <= s.length <= 12`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的子序列都列举出来**，然后从中挑出两条互不重叠且都是回文的子序列，计算它们长度的乘积，取最大值。

- **子序列的表示**：  
  给定字符串 `s` 长度为 `n`（本题 `n ≤ 12`），我们可以用一个 **位掩码**（bitmask）来表示一个子序列。  
  位掩码是一个二进制整数，长度恰好为 `n` 位。第 `i` 位为 `1` 表示我们 **选取** `s[i]`，为 `0` 则不选。  
  这就好像我们在一本字典里做记号：每一页（字符位置）上贴一个小贴纸（1）或不贴（0），记下我们挑了哪些字符。

- **枚举所有子序列**：  
  对于 `n` 个字符，一共有 `2^n` 种不同的选取方式（每个字符要么选要么不选），所以我们可以把 `0 … (1<<n)-1` 这 `2^n` 个整数全部遍历。

- **判断是否是回文**：  
  把对应的字符取出来形成一个新字符串 `t`，然后检查 `t` 是否等于它的逆序 `t[::-1]`。如果相等，则 `t` 是回文。

- **两两配对**：  
  对于每一个回文子序列 `mask1`，再遍历一次所有回文子序列 `mask2`，如果 `mask1` 与 `mask2` **不重叠**（即 `mask1 & mask2 == 0`），说明它们在原串中使用的字符位置互不冲突。此时计算 `len1 * len2`，更新最大乘积。

**为什么这个方法一定能得到答案？**  
因为我们穷举了**所有**可能的子序列组合，只要答案对应的两条回文子序列存在，它们一定会在我们的遍历中被检测到，最终的最大乘积必然被记录。

#### 代码（Python）

```python
def maxProduct(s: str) -> int:
    n = len(s)
    # 用字典保存每个子序列掩码对应的回文长度（若不是回文则不保存）
    pal_len = {}

    # 1️⃣ 枚举所有子序列（2^n 种）
    for mask in range(1, 1 << n):          # mask = 0 表示空子序列，直接跳过
        # 把 mask 对应的字符取出来组成子序列 t
        t = []
        for i in range(n):
            if mask >> i & 1:              # 第 i 位是 1，说明选了 s[i]
                t.append(s[i])
        # 检查 t 是否回文
        if t == t[::-1]:
            pal_len[mask] = len(t)        # 记录回文子序列的长度

    # 2️⃣ 两两配对，找最大乘积
    ans = 0
    masks = list(pal_len.keys())
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            m1, m2 = masks[i], masks[j]
            if m1 & m2 == 0:               # 位与为 0，说明不重叠
                prod = pal_len[m1] * pal_len[m2]
                if prod > ans:
                    ans = prod
    return ans
```

**关键行中文注释**已经写在代码里，直接可以运行。

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有子序列需要 `O(2^n)` 次循环。  
  - 对每个子序列我们遍历 `n` 位来收集字符并检查回文，最坏是 `O(n)`。  
  - 两两配对的数量是 `O(k^2)`，其中 `k` 是回文子序列的数量，最坏情况下 `k ≤ 2^n`。  
  综合来看整体是 **`O( n * 2^n + (2^n)^2 ) = O(3^n)`**（因为 `2^n * 2^n = 4^n`，但实际 `n ≤ 12`，`3^n` 已经是一个保守的上界）。  
  用大白话说：如果字符串长度是 12，最多要检查大约 **531,441** 种组合，对电脑来说还是可以接受的。

- **空间复杂度**：  
  - 需要一个字典保存最多 `2^n` 条记录，每条只保存一个整数长度，空间是 **`O(2^n)`**。  
  - 额外的临时列表 `t` 最长也不会超过 `n`，算作常数级别。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经能在本题的约束下跑通，但我们可以把“**两两配对**”的步骤进一步简化，使代码更清晰、常数更小。

**瓶颈在哪里？**  
- 暴力解在配对时每次都要检查 `mask1 & mask2 == 0`。如果我们已经把所有**回文子序列的最长长度**预先算好，只需要在一次遍历中寻找两条不冲突的子序列即可。

**优化思路**：

1. **先遍历所有子序列，记录每个掩码对应的回文长度**（同上），这一步是必须的。
2. **对每个掩码**，我们只关心它对应的**最长回文子序列的长度**。因为如果同一个掩码对应多个回文子序列，显然取最长的就最有价值。
3. **遍历所有掩码对**（仍然是 `2^n` 个），但我们可以把它们的组合写成“双层循环”。  
   - 对每个 `mask1`，只需要在 **`mask2 = complement of mask1` 的子集** 中寻找最大长度。  
   - 这里的 “补集” 指的是所有不和 `mask1` 重叠的位，即 `(~mask1) & ((1<<n)-1)`。  
   - 对这个补集的所有子集（子掩码）进行遍历，找出其中的最大回文长度 `best[mask2]`，然后更新答案 `best[mask1] * best[mask2]`。

4. 为了让 “在补集子集中找最大长度” 变得 **O(1)**，我们可以在 **预处理阶段** 用 **DP（子集 DP）** 把每个掩码的 **最大回文长度** 推广到它的所有超集。具体做法：

   - 初始化 `max_len[mask] = pal_len.get(mask, 0)`（如果 `mask` 本身是回文，则是它的长度，否则 0）。
   - 对每一位 `i`（0~n-1），遍历所有 `mask`，如果第 `i` 位是 0，则 `max_len[mask | (1<<i)] = max(max_len[mask | (1<<i)], max_len[mask])`。  
   - 这样遍历完后，**每个掩码的 `max_len[mask]` 就是它所有子集（即更小的掩码）中回文长度的最大值**。

5. 最后只需要一次双层循环：

   ```python
   for mask in range(1, 1<<n):
       other = ((1<<n)-1) ^ mask          # 与 mask 不重叠的位
       ans = max(ans, max_len[mask] * max_len[other])
   ```

   这里 `max_len[other]` 已经是 **在 `other` 的所有子集里** 能得到的最长回文长度，保证不冲突。

**核心概念解释**：

- **位掩码**：把字符串的每个位置当成一盏灯，灯开（1）表示选这个字符，灯关（0）表示不选。掩码就是一串 0/1，直接映射到二进制整数。
- **子集 DP**（Subset DP）：类似于在一张“状态转移表”上把信息从小集合“传递”到大集合。想象你在把小盒子里的宝贝（最长回文长度）搬到能装下它的大盒子里，确保每个大盒子里装的都是它能装的最大宝贝。

#### 代码（Python）

```python
def maxProduct(s: str) -> int:
    n = len(s)
    total = 1 << n                     # 所有可能的掩码数量

    # 1️⃣ 记录每个掩码本身是否是回文以及对应长度
    pal_len = [0] * total
    for mask in range(1, total):
        # 取出 mask 对应的子序列
        t = []
        for i in range(n):
            if mask >> i & 1:
                t.append(s[i])
        # 检查回文
        if t == t[::-1]:
            pal_len[mask] = len(t)     # 直接写入数组，省去字典的开销

    # 2️⃣ 子集 DP：把每个子集的最大回文长度向上“传播”
    max_len = pal_len[:]               # 复制一份作为 DP 表
    for i in range(n):                 # 枚举每一位
        for mask in range(total):
            if not (mask >> i & 1):    # 第 i 位是 0，意味着可以把 i 加进来形成更大的集合
                nxt = mask | (1 << i)  # 把第 i 位设为 1，得到超集
                if max_len[nxt] < max_len[mask]:
                    max_len[nxt] = max_len[mask]

    # 3️⃣ 枚举第一个子序列的掩码，直接用 complement 查第二个子序列的最佳长度
    ans = 0
    full_mask = total - 1
    for mask in range(1, total):
        other = full_mask ^ mask       # 与 mask 不重叠的所有位置
        prod = max_len[mask] * max_len[other]
        if prod > ans:
            ans = prod
    return ans
```

**代码要点**：

- `pal_len[mask]` 只在 `mask` 本身对应的子序列是回文时保存长度，其他保持 `0`。
- 子集 DP 循环的两层 `for` 把 **“子集的最大值”** 传递到 **“包含它的更大集合”**，保证 `max_len[mask]` 最终等于 `mask` 所有子集中回文长度的最大值。
- `other = full_mask ^ mask` 直接得到与 `mask` 完全不重叠的位集合（位异或），无需再遍历所有子集。

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有掩码并检查回文：`O(n * 2^n)`（每个掩码遍历 `n` 位）。  
  - 子集 DP：外层 `n`，内层 `2^n`，也是 `O(n * 2^n)`。  
  - 最后一次遍历求最大乘积：`O(2^n)`。  
  综合为 **`O(n * 2^n)`**，对 `n ≤ 12` 来说大约 `12 * 4096 ≈ 5e4` 次操作，几乎瞬间完成。  
  与暴力解的 `O(3^n)` 相比，常数更小，实际运行更快。

- **空间复杂度**：  
  - 两个长度为 `2^n` 的数组 `pal_len`、`max_len`，即 **`O(2^n)`**。  
  - 其它临时变量都是常数级别。

---

## 心得

- **核心技巧**：**位掩码 + 子集 DP**（把子集信息向上合并），在「集合之间不冲突」的组合优化题里非常有用。
- **适用的题型**  
  1. *Maximum Product of the Length of Two Palindromic Substrings*（本题的变体）  
  2. *Maximum AND Sum of Two Disjoint Subsets*（求两不相交子集的位运算最大值）  
  3. *Largest Subset with Bitwise XOR = 0*（需要在子集之间保持互斥或特定关系的题目）  
- **一句话总结解题钥匙**：**先把每个子集的“价值”算好，再用子集 DP 把价值传播到所有超集，最后配对时直接查表即可。**

---

## 反思

- **第一反应**：看到“两个不重叠的回文子序列”，立刻想到“枚举所有子序列”，因为字符串长度只有 12，暴力似乎可以接受。
- **最容易踩的坑**  
  1. **空子序列**：`mask = 0` 对应空串，它不是合法的回文子序列，需要跳过。  
  2. **位运算细节**：计算补集时一定要用 `full_mask = (1<<n)-1`，否则高位会被误算成 1。  
  3. **子集 DP 更新方向**：必须从 **低位到高位**（`mask` 的第 `i` 位为 0 时才向 `mask|1<<i` 更新），否则会出现信息未完整传播的错误。
- **下次类似题的第一步**：  
  **把“是否冲突”转化为位掩码的“与操作为 0”**，然后先把每个掩码的单独价值算出来，再考虑使用子集 DP 或直接枚举补集来组合最大值。这样可以把原本指数级的搜索压到 `O(n·2^n)`。