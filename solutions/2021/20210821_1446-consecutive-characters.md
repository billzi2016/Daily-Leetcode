# #1446. 连续字符 / Consecutive Characters

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/consecutive-characters/)

---

## 题目（英文原版）

**Description**

The power of the string is the maximum length of a non-empty substring that contains only one unique character.
Given a string s, return the power of s.

**Examples**

**Example 1:**

```
Input: s = "leetcode"
Output: 2
Explanation: The substring "ee" is of length 2 with the character 'e' only.
```

**Example 2:**

```
Input: s = "abbcccddddeeeeedcba"
Output: 5
Explanation: The substring "eeeee" is of length 5 with the character 'e' only.
```

**Constraints**

- 1 <= s.length <= 500
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

字符串的 **power**（力量）定义为只包含唯一字符的非空子字符串（substring）的最大长度。  
给定一个字符串 `s`，返回 `s` 的 **power**。

## 示例

### 示例 1
**输入**  
```
s = "leetcode"
```
**输出**  
```
2
```
**解释**：子字符串 `"ee"` 的长度为 2，且仅包含字符 `'e'`。

### 示例 2
**输入**  
```
s = "abbcccddddeeeeedcba"
```
**输出**  
```
5
```
**解释**：子字符串 `"eeeee"` 的长度为 5，且仅包含字符 `'e'`。

## 约束条件
- `1 <= s.length <= 500`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把字符串的所有 **非空子串** 都枚举一遍，检查每个子串里是否只出现了同一个字符，如果是，就记下它的长度，最后取最大的那个长度。

- **数据结构**：我们只需要遍历字符串，用两个循环分别表示子串的左端点 `i` 和右端点 `j`（`i ≤ j`）。  
  - 可以把「子串」想象成一本书里的一段文字，左端点是「起始页码」，右端点是「结束页码」。
- **正确性**：因为我们把每一种可能的子串都检查了一遍，只要有满足条件的子串，就一定会被找到，最大长度自然不会错过。
- **时间/空间复杂度**：  
  - 外层循环跑 `n` 次，内层循环最坏也跑 `n` 次（`n` 为字符串长度），所以总的比较次数大约是 `n × n = n²`。  
    - **O(n²)** 的意思是「运行时间会随输入长度的平方增长」，如果 `n=500`，最坏情况下大概要进行 250 000 次检查，对机器来说还能接受，但明显不是最优的。  
  - 只用了几个整数计数器，空间上不随 `n` 增长，记作 **O(1)**。

#### 代码（Python）

```python
def maxPower_bruteforce(s: str) -> int:
    n = len(s)
    max_len = 0                     # 记录目前找到的最大长度

    # i 是子串的左端点
    for i in range(n):
        # j 是子串的右端点（包含）
        for j in range(i, n):
            # 检查 s[i:j+1] 是否全部相同
            sub = s[i:j+1]          # 取出子串
            # 用 set 去重，若只剩一个元素说明全相同
            if len(set(sub)) == 1:
                cur_len = j - i + 1
                if cur_len > max_len:
                    max_len = cur_len
    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子串，`n` 越大，耗时呈二次方增长。
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量（`max_len、i、j、sub`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**重复检查相同字符的连续段**。实际上，我们只需要一次遍历，就能直接统计每个字符连续出现的长度：

1. 用一个指针 `i` 从左到右扫字符串。  
2. 用 `cur_len` 记录当前字符连续出现的长度。  
   - 当 `s[i]` 与前一个字符相同，`cur_len += 1`（相当于“把这页继续往后翻”。）  
   - 当不相同时，说明一个连续段结束，`cur_len` 重新置为 `1`（从新字符重新开始计数）。  
3. 每一步都把 `cur_len` 和全局最大值 `ans` 比较，保留更大的那个。

这其实就是 **双指针/滑动窗口** 的最简形式：左指针隐式地是当前连续段的起始位置，右指针是正在遍历的字符位置。我们不需要额外的数组或哈希表，只要两个整数就能完成。

> **类比**：想象你在看一串彩灯，颜色相同的灯会连在一起。你把手从左往右滑过去，手指停留的长度就是当前相同颜色灯的数量，遇到不同颜色就把手指重新放在新灯上。记录下手指最长停留的长度，就是答案。

#### 代码（Python）

```python
def maxPower(s: str) -> int:
    """
    返回字符串 s 的 power（最长相同字符连续子串的长度）。
    思路：一次遍历，统计当前连续字符的长度，用 ans 记录最大值。
    """
    ans = 1          # 至少有一个字符，power 最小为 1
    cur_len = 1      # 当前字符连续出现的长度

    # 从第二个字符开始遍历（索引 1）
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            # 与前一个字符相同，连续长度加 1
            cur_len += 1
        else:
            # 不同了，重新从 1 开始计数
            cur_len = 1
        # 更新全局最大值
        if cur_len > ans:
            ans = cur_len

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，`n` 增大时耗时线性增长。相比暴力的 `O(n²)`，快了很多。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：一次遍历统计连续相同字符的长度（滑动窗口/双指针的极简版）。  
- **适用的题型**：  
  1. “最长连续子数组/子串” 类问题（如 LeetCode 674 *Longest Continuous Increasing Subsequence*）。  
  2. “最多出现次数的字符/数字” 需要连续计数的题目（如统计二进制字符串中连续 1 的最长长度）。  
- **解题钥匙**：**把“连续”转化为“计数器”**，用一个变量记录当前段的长度，遍历时随时更新最大值。

---

## 反思

- **第一反应**：看到“最长只含一种字符的子串”，本能会想到枚举所有子串检查是否相同——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记处理字符串长度为 `1` 的特殊情况，导致 `ans` 初始化错误。  
  - 在遍历时误把 `cur_len` 重置为 `0` 而不是 `1`（因为当前字符本身已经算作长度 1）。  
- **下次第一步**：先问自己“是否可以在一次扫描中直接累计所需信息？”如果答案是“可以”，就尝试用计数器或滑动窗口来完成，而不是直接枚举所有子序列。