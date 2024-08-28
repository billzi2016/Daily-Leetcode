# #2844. 使数字特殊的最少操作次数 / Minimum Operations to Make a Special Number

> 难度：中等 · 标签：Math、String、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-a-special-number/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string num representing a non-negative integer.
In one operation, you can pick any digit of num and delete it. Note that if you delete all the digits of num, num becomes 0.
Return the minimum number of operations required to make num special.
An integer x is considered special if it is divisible by 25.

**Examples**

**Example 1:**

```
Input: num = "2245047"
Output: 2
Explanation: Delete digits num[5] and num[6]. The resulting number is "22450" which is special since it is divisible by 25.
It can be shown that 2 is the minimum number of operations required to get a special number.
```

**Example 2:**

```
Input: num = "2908305"
Output: 3
Explanation: Delete digits num[3], num[4], and num[6]. The resulting number is "2900" which is special since it is divisible by 25.
It can be shown that 3 is the minimum number of operations required to get a special number.
```

**Example 3:**

```
Input: num = "10"
Output: 1
Explanation: Delete digit num[0]. The resulting number is "0" which is special since it is divisible by 25.
It can be shown that 1 is the minimum number of operations required to get a special number.
```

**Constraints**

- 1 <= num.length <= 100
- num only consists of digits '0' through '9'.
- num does not contain any leading zeros.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的字符串 `num`，它表示一个非负整数 (non-negative integer)。  
在一次操作中，你可以选择 `num` 中的任意一个数字并将其删除。注意，如果你删除了 `num` 的所有数字，则 `num` 变为 `0`。  
返回使 `num` 变为特殊数所需的最少操作次数。  

如果一个整数 `x` 能被 `25` 整除，则称其为特殊数 (special)。

---

### 示例

#### 示例 1
**输入:** `num = "2245047"`  
**输出:** `2`  
**解释:** 删除下标为 `5` 和 `6` 的数字，得到的数字是 `"22450"`，它是特殊的，因为它能被 `25` 整除。可以证明，得到特殊数的最少操作次数是 `2`。

#### 示例 2
**输入:** `num = "2908305"`  
**输出:** `3`  
**解释:** 删除下标为 `3`、`4` 和 `6` 的数字，得到的数字是 `"2900"`，它是特殊的，因为它能被 `25` 整除。可以证明，得到特殊数的最少操作次数是 `3`。

#### 示例 3
**输入:** `num = "10"`  
**输出:** `1`  
**解释:** 删除下标为 `0` 的数字，得到的数字是 `"0"`，它是特殊的，因为它能被 `25` 整除。可以证明，得到特殊数的最少操作次数是 `1`。

---

### 约束条件
- `1 <= num.length <= 100`
- `num` 只包含字符 `'0'` 到 `'9'`。
- `num` 不含任何前导零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的删除方式都穷举一遍**，看看哪一种能得到一个能被 25 整除的数，取其中最少的删除次数。

- **数据结构**：我们只需要把字符串 `num` 当作字符数组来遍历。可以把“删掉某些下标的字符”想象成在一本书里划掉几页，剩下的文字顺序不变。
- **正确性**：只要遍历了**所有**删法，就一定能找到最优解，因为最优解本身也是一种删法，必然会被枚举到。
- **复杂度分析**：  
  - 对于长度为 `n`（最多 100）的字符串，所有可能的删法数量是 `2^n`（每个位置保留或删除），这在 `n=100` 时已经是天文数字，根本不可能在电脑里跑完。  
  - 用大白话说，`O(2^n)` 就像把 100 条线每条都决定要不要剪掉，组合数太多了，计算机会卡死。

> 所以暴力枚举所有子序列虽然思路最直观，却不可行。

#### 代码（Python）

```python
def minOperations_bruteforce(num: str) -> int:
    n = len(num)
    best = n          # 最多删掉全部字符，得到 0
    # 用位掩码遍历所有子序列（仅作演示，实际不可用）
    for mask in range(1 << n):
        # 生成删除后的数字字符串
        kept = []
        for i in range(n):
            if mask >> i & 1:          # 保留第 i 位
                kept.append(num[i])
        if not kept:                   # 全部删掉，视作 "0"
            cur = "0"
        else:
            cur = "".join(kept)
        # 判断是否能被 25 整除
        if int(cur) % 25 == 0:
            deletions = n - len(kept)  # 删除的字符数
            best = min(best, deletions)
    return best
```

> **注**：上面代码只用于说明暴力思路，`n` 甚至为 20 都会非常慢，更别说题目上最高 100。

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 每个位都有保留/删除两种选择，组合数呈指数增长。  
  实际上，这意味着当 `n=30` 时就已经需要约 10⁹ 次操作，远远超出一秒的计算上限。
- **空间复杂度**：`O(n)` —— 用来存放当前子序列的临时列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于枚举所有子序列**。我们需要找出只要**关注数字的末两位**就能判断是否能被 25 整除的规律，从而大幅缩小搜索空间。

> **关键数学事实**  
> 一个整数能被 25 整除，当且仅当它的**最后两位**是 `00、25、50、75`（因为 25 = 5²，只有这四种组合的十位和个位能被 25 整除）。

所以我们只要**把原字符串删到只剩下这四种结尾之一**，其余的高位可以随意保留。问题转化为：

> 在原字符串 `num` 中，找出一对下标 `(i, j)`（`i < j`），使得 `num[i]` 为十位、`num[j]` 为个位，且这两个字符组成的两位数是 `00、25、50、75`。  
> 删除所有位于 `j` 右侧的字符（它们会变成尾部之后的多余位），以及 `i` 与 `j` 之间、`i` 左侧不需要保留的字符。  
> 删除的总数 = `n - (保留下来的字符数)` = `n - (i 前面的保留 + 2)` = `n - i - 2`（因为我们必定保留 `i` 与 `j` 两位，且 `i` 前面的字符都可以保留，最少只要这两位）。

因此，只要遍历所有可能的 `(i, j)`，找出满足条件的最小 `n - i - 2` 即可。

**步骤细化**：

1. 预定义合法的结尾集合 `targets = ["00","25","50","75"]`。  
2. 对每一种目标结尾 `t`（两字符），在字符串从右往左寻找匹配的**个位** `t[1]`，记为位置 `j`。  
3. 在 `j` 左侧继续向左寻找匹配的**十位** `t[0]`，记为位置 `i`。  
4. 若成功找到 `i` 与 `j`，则需要删除的字符数为 `n - i - 2`，更新答案的最小值。  
5. 特殊情况：如果字符串本身已经是 `0`（即只有一个字符 `'0'`），只需要删除 `n-1` 次即可得到 `0`（因为 `0` 本身已经是特殊数）。

> **为什么从右往左找更快？**  
> 因为我们关心的是“最后两位”，自然应该先锁定最右边的个位，再往左找十位，这样可以一次遍历完成，时间是线性的 `O(n)`。

#### 代码（Python）

```python
def minOperations(num: str) -> int:
    n = len(num)
    # 只要有一个 '0'，最坏情况可以把全部删成 "0"
    answer = n - 1          # 初始答案：删掉除一个字符外的所有字符

    targets = ["00", "25", "50", "75"]   # 能被 25 整除的两位结尾

    for t in targets:        # 枚举四种合法结尾
        last = t[1]           # 个位字符
        second = t[0]         # 十位字符

        # 从右往左找个位
        j = n - 1
        while j >= 0 and num[j] != last:
            j -= 1
        if j < 0:             # 没找到对应的个位，直接进入下一个目标
            continue

        # 在个位左侧继续找十位
        i = j - 1
        while i >= 0 and num[i] != second:
            i -= 1
        if i < 0:             # 十位找不到，同样跳过
            continue

        # 此时 i、j 满足目标结尾，删除次数 = 总长度 - 已保留的字符数
        deletions = n - i - 2
        answer = min(answer, deletions)

    return answer
```

> **代码注释**  
> - `answer = n - 1`：如果只剩下一个 `'0'`，我们最多只需要删掉 `n-1` 位（题目保证没有前导零）。  
> - `while j >= 0 and num[j] != last:`：从最右侧开始找匹配的个位，直到找到或遍历完。  
> - `deletions = n - i - 2`：保留 `i` 前面的所有字符（不需要删除），再加上必保留的 `i` 与 `j` 两位，剩余的字符都要删。

#### 复杂度

- **时间复杂度**：`O(n)` —— 我们只遍历字符串几次（最多 4 × 2 ≈ 8 次遍历），与 `n` 成线性关系。相较于暴力的指数级 `O(2^n)`，快得多。  
  - 用生活化的比喻：找出符合条件的两位数就像在一本书里从后往前找两个特定的词，只要一次扫描就能定位，不需要把每一种删法都列出来。
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`answer、i、j`），不随输入规模增长。

---

## 心得

- **核心技巧**：利用 **“只需关注末两位”** 的数学性质，把原本的子序列枚举压缩到 **固定的四种目标结尾**，再用 **一次线性扫描** 找到最近的匹配位置。
- **适用题型**  
  1. “使数字满足某个末尾条件”——如 `Divisible by 6`（需要判断末两位是否为偶数且能被 3 整除）。  
  2. “删除最少字符使字符串满足特定模式”——如 `Make Number Palindrome`（把数字变成回文）。  
  3. “最少操作使字符串成为某种合法形式”——如 `Minimum Deletions to Make String Balanced`（删除字符使左括号数不超过右括号数）。
- **一句话总结**：**把问题从“删多少种可能”转化为“找最近的合法结尾”，从指数降到线性**。

---

## 反思

- **第一反应**：看到“删除字符”，自然想到枚举所有子序列或动态规划，结果忽略了题目给出的数学线索（能被 25 整除的末两位特性），导致思路走得太宽。
- **最容易踩的坑**  
  - **漏掉单独的 `0`**：题目说明如果把所有字符都删掉，数值变成 `0`，所以答案上限是 `n-1`（而不是 `n`）。  
  - **下标顺序**：必须保证十位下标 `<` 个位下标，否则删除顺序不对，会误算需要删除的字符数。  
  - **前导零**：虽然原字符串没有前导零，但删后得到的子序列可能出现前导零，只要保留的末两位正确，前导零不影响能否被 25 整除。
- **下次遇到同类题**：第一步先**找出“只关心最后几位”的数学规律**，再**从右往左定位匹配**，把搜索空间压到常数或线性级别。这样可以快速锁定最优解，避免暴力枚举的陷阱。