# #1663. 具有给定数值的最小字符串 / Smallest String With A Given Numeric Value

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/smallest-string-with-a-given-numeric-value/)

---

## 题目（英文原版）

**Description**

The numeric value of a lowercase character is defined as its position (1-indexed) in the alphabet, so the numeric value of a is 1, the numeric value of b is 2, the numeric value of c is 3, and so on.
The numeric value of a string consisting of lowercase characters is defined as the sum of its characters' numeric values. For example, the numeric value of the string "abe" is equal to 1 + 2 + 5 = 8.
You are given two integers n and k. Return the lexicographically smallest string with length equal to n and numeric value equal to k.
Note that a string x is lexicographically smaller than string y if x comes before y in dictionary order, that is, either x is a prefix of y, or if i is the first position such that x[i] != y[i], then x[i] comes before y[i] in alphabetic order.

**Examples**

**Example 1:**

```
Input: n = 3, k = 27
Output: "aay"
Explanation: The numeric value of the string is 1 + 1 + 25 = 27, and it is the smallest string with such a value and length equal to 3.
```

**Example 2:**

```
Input: n = 5, k = 73
Output: "aaszz"
```

**Constraints**

- 1 <= n <= 105
- n <= k <= 26 * n

---

## 题目（中文翻译）

字符的数值（numeric value）定义为其在字母表中的位置（从 1 开始计数），因此字符 `'a'` 的数值为 1，`'b'` 为 2，`'c'` 为 3，依此类推。  
由小写字符组成的字符串的数值（numeric value）定义为其所有字符数值的和。例如，字符串 `"abe"` 的数值为 `1 + 2 + 5 = 8`。  

给定两个整数 `n` 和 `k`。返回长度恰好为 `n`、数值等于 `k` 的字典序（lexicographically）最小的字符串。  

注意：如果字符串 `x` 在字典序上先于字符串 `y`，则称 `x` 小于 `y`。具体而言，要么 `x` 是 `y` 的前缀，或者在第一个不同的位置 `i` 上，`x[i]` 在字母表中的顺序早于 `y[i]`。  

---

### 示例

#### 示例 1
**输入**: `n = 3, k = 27`  
**输出**: `"aay"`  
**解释**: 字符串的数值为 `1 + 1 + 25 = 27`，且它是满足该数值和长度为 3 的字典序最小的字符串。

#### 示例 2
**输入**: `n = 5, k = 73`  
**输出**: `"aaszz"`  
**解释**: 字符串的数值为 `1 + 1 + 19 + 26 + 26 = 73`，且在所有满足条件的长度为 5 的字符串中，它的字典序最小。

---

### 约束条件
- `1 <= n <= 10^5`
- `n <= k <= 26 * n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有长度为 `n` 的小写字母组合**，计算每个组合的数值和，找出数值等于 `k` 且字典序最小的那一个。  
- **数据结构**：我们可以把字符串看作一个长度为 `n` 的数组，每个位置放 1~26 之间的整数（对应字符 `'a'`~`'z'`），相当于在 **进制 26** 的数系里遍历所有可能。  
- **正确性**：只要遍历了所有可能的组合，必然能找到满足条件的最小字典序字符串。  

不过，这种做法在最坏情况下需要遍历 `26^n` 种组合，`n` 甚至可能是 `10⁵`，根本不可行。

#### 代码（Python）

```python
import itertools

def smallestString_bruteforce(n: int, k: int) -> str:
    # 生成所有可能的字符序列（仅作演示，实际 n 很小才可跑通）
    for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=n):
        # 计算数值和
        total = sum(ord(c) - ord('a') + 1 for c in combo)
        if total == k:                     # 找到满足数值的组合
            return ''.join(combo)          # 第一次出现即是字典序最小
    return ""                               # 若不存在（题目保证一定存在）
```

> **注意**：上述代码只能在 `n ≤ 5` 左右的小测试中跑通，真正的 LeetCode 数据规模会直接把它卡死。

#### 复杂度  

- **时间复杂度**：`O(26^n)` —— 每个位置有 26 种选择，需要遍历所有组合，指数级增长。  
- **空间复杂度**：`O(n)` —— 递归/迭代过程中保存当前组合的长度为 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **遍历所有组合是不可取的**，我们必须**直接构造**出答案。  
观察题目要求的“字典序最小”，意味着**左边的字符尽量小**（越靠前越重要），而“数值和等于 `k`”则限制了整体的“重量”。  

**关键观察**  

1. 若所有字符都取最小值 `'a'`（数值 1），整个字符串的数值为 `n`。  
2. 题目保证 `k ≥ n`，所以我们只需要在这些 `'a'` 的基础上**把一些位置的字符往后调**，把它们的数值从 1 提高到更大的值。  
3. 为了让左侧字符尽可能小，我们**从字符串的最右侧开始加值**。每次把当前位置的字符尽可能调到 `'z'`（数值 26），因为右侧字符对字典序的影响最小。  

**贪心策略**  

- 先把所有字符设为 `'a'`，此时总和为 `n`。  
- 计算还需要补多少值：`remain = k - n`（剩余要分配的“额外”数值）。  
- 从右往左遍历每个位置 `i`（0‑based），  
  - 本位置最多还能提升的值是 `25`（因为已经有 1，需要加到最多 26），记作 `add = min(25, remain)`。  
  - 把字符提升 `add`，即 `chr(ord('a') + add)`。  
  - 更新 `remain -= add`。  
  - 若 `remain == 0`，提前结束。  

这样得到的字符串必然是字典序最小的，因为我们**只在最不重要的右侧位置使用最大可能的提升**，左侧尽可能保持 `'a'`。

#### 代码（Python）

```python
def smallestString(n: int, k: int) -> str:
    # 1. 初始化为全部 'a'，此时总和为 n
    chars = ['a'] * n
    # 2. 需要额外增加的数值
    remain = k - n                # remain >= 0，且 <= 25 * n

    # 3. 从右向左贪心分配
    i = n - 1                     # 从最后一个位置开始
    while remain > 0 and i >= 0:
        # 本位最多还能提升 25（从 1 提升到 26）
        add = min(25, remain)     # 本次真正加多少
        # 把字符提升 add 位，例如 add=2 => 'a' -> 'c'
        chars[i] = chr(ord('a') + add)
        remain -= add
        i -= 1                     # 移动到左侧下一个位置

    # 4. 合并成字符串返回
    return ''.join(chars)
```

> **关键行解释**  
> - `chars = ['a'] * n`：把每个位置都看作一个最小的“砖块”。  
> - `add = min(25, remain)`：相当于“把当前砖块往上堆最多 25 层”，但不能超过剩余需要的层数。  
> - `chr(ord('a') + add)`：把 `'a'` 往后移动 `add` 位得到对应字符。

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串（最坏遍历全部 `n`），即使 `n = 10⁵` 也非常快。  
- **空间复杂度**：`O(n)` —— 用一个字符数组保存结果，返回时再转成字符串。  

相较于暴力的指数级时间，贪心把复杂度降到了线性。

---

## 心得

- **核心技巧**：**从右往左的贪心分配**——把“剩余价值”尽可能放在对字典序影响最小的位置。  
- **适用的题型**：  
  1. “给定长度和数值，求字典序最小/最大字符串”类（如本题）。  
  2. “分配资源使得序列字典序最小”类（如把 `k` 分配到 `n` 位数字，使数值和固定且数值最小）。  
  3. “构造满足约束的最小/最大序列”类（如 LeetCode 1840 “Maximum Building Height” 的类似思路）。  
- **一句话总结**：**把尽可能大的字符放在最右侧，左侧保持最小**，即可得到字典序最小的合法字符串。

---

## 反思

- **第一反应**：直接想到枚举所有可能（暴力），但很快意识到规模太大。  
- **最容易踩的坑**：  
  - 忘记把所有字符先设为 `'a'`，导致剩余值计算错误。  
  - 在计算 `add` 时写成 `min(26, remain)`，实际上每位最多只能再加 25（因为已经有 1）。  
  - 边界条件：`k == n` 时应该全部是 `'a'`，`k == 26*n` 时全部是 `'z'`，代码需要自然覆盖。  
- **下次遇到同类题**：第一步先**确定最小基准（全 `'a'`）**，再**从最不重要的方向（右侧）逐步填充剩余需求**，这几乎是通用的贪心思路。