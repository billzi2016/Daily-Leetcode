# #1869. 连续 1 段比 0 段更长 / Longer Contiguous Segments of Ones than Zeros

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/longer-contiguous-segments-of-ones-than-zeros/)

---

## 题目（英文原版）

**Description**

Given a binary string s, return true if the longest contiguous segment of 1's is strictly longer than the longest contiguous segment of 0's in s, or return false otherwise.
Note that if there are no 0's, then the longest continuous segment of 0's is considered to have a length 0. The same applies if there is no 1's.

**Examples**

**Example 1:**

```
Input: s = "1101"
Output: true
Explanation:
The longest contiguous segment of 1s has length 2: "1101"
The longest contiguous segment of 0s has length 1: "1101"
The segment of 1s is longer, so return true.
```

**Example 2:**

```
Input: s = "111000"
Output: false
Explanation:
The longest contiguous segment of 1s has length 3: "111000"
The longest contiguous segment of 0s has length 3: "111000"
The segment of 1s is not longer, so return false.
```

**Example 3:**

```
Input: s = "110100010"
Output: false
Explanation:
The longest contiguous segment of 1s has length 2: "110100010"
The longest contiguous segment of 0s has length 3: "110100010"
The segment of 1s is not longer, so return false.
```

**Constraints**

- 1 <= s.length <= 100
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个二进制字符串（binary string）`s`，如果 `s` 中最长的连续 1 子串（contiguous segment of 1's）的长度严格大于最长的连续 0 子串（contiguous segment of 0's）的长度，则返回 `true`；否则返回 `false`。

**注意**：如果字符串中没有 `0`，则最长的连续 0 子串的长度视为 `0`。同理，如果没有 `1`，则最长的连续 1 子串的长度视为 `0`。

## 示例

### 示例 1
**输入**：`s = "1101"`  
**输出**：`true`  
**解释**：  
最长的连续 1 子串长度为 `2`（子串 `"11"`），最长的连续 0 子串长度为 `1`（子串 `"0"`）。  
1 的子串更长，返回 `true`。

### 示例 2
**输入**：`s = "111000"`  
**输出**：`false`  
**解释**：  
最长的连续 1 子串长度为 `3`（子串 `"111"`），最长的连续 0 子串长度也为 `3`（子串 `"000"`）。  
1 的子串并不更长，返回 `false`。

### 示例 3
**输入**：`s = "110100010"`  
**输出**：`false`  
**解释**：  
最长的连续 1 子串长度为 `2`（子串 `"11"`），最长的连续 0 子串长度为 `3`（子串 `"000"`）。  
1 的子串不比 0 的子串长，返回 `false`。

## 约束条件
- `1 <= s.length <= 100`
- `s[i]` 只能是 `'0'` 或 `'1'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串里 **所有** 连续子段都列举出来，分别统计它们是 `0` 还是 `1`，然后找出最长的 `0` 子段和最长的 `1` 子段，比较两者的长度。

- **遍历所有子段**：可以用两层循环，外层决定子段的起始位置 `i`，内层把结束位置 `j` 从 `i` 往后推进，一直检查 `s[i:j+1]` 是否全是相同字符。如果相同，就记录它的长度；如果不相同，就停止内层循环，因为再往后肯定已经不是同一字符的连续段了。
- **用到的数据结构**：这里只需要几个整数变量来保存当前子段的长度、最大 `0` 长度、最大 `1` 长度。可以把它想象成 **记事本**，我们在纸上不停地写“这段有多少个相同的字符”，然后把最长的记下来。  
  （如果你熟悉哈希表，可以把它比作“查字典”：键是字符 `'0'` 或 `'1'`，值是对应的最长长度。不过在暴力解里我们直接用两个变量就够了。）

这个方法一定能得到正确答案，因为我们枚举了**所有可能的连续子段**，不可能漏掉最长的那段。

#### 代码（Python）

```python
def checkLongestSegment_bruteforce(s: str) -> bool:
    n = len(s)
    max_zero = 0   # 记录出现过的最长 0 段长度
    max_one  = 0   # 记录出现过的最长 1 段长度

    # i 是子段的起始位置
    for i in range(n):
        # 当前子段的字符（先假设它是 s[i]）
        cur_char = s[i]
        # j 从 i 开始向后扩展
        for j in range(i, n):
            # 如果扩展到的位置字符和起始字符不一样，就停止这一次的扩展
            if s[j] != cur_char:
                break
            # 否则说明 s[i:j+1] 是一个全相同字符的连续段，长度为 j-i+1
            length = j - i + 1
            if cur_char == '0':
                max_zero = max(max_zero, length)   # 更新最长 0 段
            else:  # cur_char == '1'
                max_one = max(max_one, length)     # 更新最长 1 段

    # 最后比较两者长度
    return max_one > max_zero
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n` 是字符串长度。两层循环相当于把每个位置当作起点，然后向后检查每一个可能的结束点，最坏情况下要检查 `1 + 2 + … + n ≈ n²/2` 次。用大白话说，就是“如果字符串有 100 个字符，最多要检查大概 10 000 次”。  
- **空间复杂度**：`O(1)`  
  只用了常数个整数变量，和字符串长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于重复检查相同的字符**。例如在 `"1111"` 中，暴力解会把 `i=0` 时检查 `1、11、111、1111`，`i=1` 时又检查 `1、11、111`，其实这些子段的内容已经在前一次遍历中知道了。

我们只需要一次遍历，就能把每个 **连续相同字符的段** 的长度算出来：

1. 用两个变量 `cur_len`、`cur_char` 记录**当前正在统计的段**的字符和长度。  
   想象我们在看一条路，路上有红灯（`0`）和绿灯（`1`），我们手里拿着一个计数器，一直数到灯的颜色变了才把这个计数器的数记下来。
2. 当遍历到下一个字符 `c` 时：
   - 如果 `c` 与 `cur_char` 相同，说明仍在同一段，`cur_len += 1`；
   - 否则，当前段结束，把 `cur_len` 用于更新对应的最大长度（`max_zero` 或 `max_one`），然后把 `cur_char` 换成 `c`，`cur_len` 重置为 `1`。
3. 循环结束后别忘了把**最后一段**的长度也更新一次（因为循环里只有在颜色变化时才会更新）。
4. 最后比较 `max_one` 与 `max_zero`，返回 `max_one > max_zero`。

核心数据结构只有几个整数，**不需要额外的数组或哈希表**，所以时间是线性的，空间是常数。

#### 代码（Python）

```python
def checkLongestSegment(s: str) -> bool:
    # 最大的 0 段、1 段长度，初始为 0（题目说没有对应字符时长度算 0）
    max_zero, max_one = 0, 0

    # 当前段的字符和长度
    cur_char = s[0]      # 第一个字符一定存在，因为长度 >= 1
    cur_len  = 1

    # 从第二个字符开始遍历
    for c in s[1:]:
        if c == cur_char:               # 仍然在同一段
            cur_len += 1
        else:                           # 段结束，先更新对应的最大值
            if cur_char == '0':
                max_zero = max(max_zero, cur_len)
            else:  # cur_char == '1'
                max_one = max(max_one, cur_len)

            # 开启新段
            cur_char = c
            cur_len = 1

    # 循环结束后，需要把最后一段的长度也更新进去
    if cur_char == '0':
        max_zero = max(max_zero, cur_len)
    else:
        max_one = max(max_one, cur_len)

    # 判断 1 段是否严格更长
    return max_one > max_zero
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，每个字符做 **常数** 次操作。换句话说，长度是 100 时，只需要大约 100 次检查，远比 10 000 次快得多。
- **空间复杂度**：`O(1)`  
  只用了固定数量的整数变量，和字符串长度没有关系。

---

## 心得

- 这道题考察的核心技巧是 **一次遍历统计连续段长度（滑动窗口/计数法）**。  
- 该技巧适用于类似的“最长连续子串”题型，例如  
  1. “最长连续 1 的子数组”  
  2. “找出字符串中最长的相同字符子段”  
  3. “二进制数组中最长的连续 0/1”  
- **一句话总结解题钥匙**：用一个计数器在遍历中“记录当前段”，在颜色/字符切换时把计数器的值保存为对应的最大长度。

---

## 反思

- **第一反应**：看到“最长连续段”，立刻想到要 **遍历一次**，在遍历过程中记录当前段的长度并更新最大值。
- **最容易踩的坑**  
  - 忘记在循环结束后更新最后一段的最大长度（因为循环里只有在字符变化时才会更新）。  
  - 把 `max_one > max_zero` 写成 `>=`，导致在长度相等时错误返回 `True`。  
  - 没考虑只有 `0` 或只有 `1` 的极端情况，但题目已经说明此时另一段长度为 `0`，代码中自然会得到正确结果。
- **下次遇到同类题**，第一步应该想到：**“用一个变量记录当前连续字符的计数，遇到不同字符时刷新计数并更新最大值”。**这样就能把时间从平方级降到线性级。