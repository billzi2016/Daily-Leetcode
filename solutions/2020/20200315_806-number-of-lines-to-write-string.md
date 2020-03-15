# #806. 写字符串所需的行数 / Number of Lines To Write String

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/number-of-lines-to-write-string/)

---

## 题目（英文原版）

**Description**

You are given a string s of lowercase English letters and an array widths denoting how many pixels wide each lowercase English letter is. Specifically, widths[0] is the width of 'a', widths[1] is the width of 'b', and so on.
You are trying to write s across several lines, where each line is no longer than 100 pixels. Starting at the beginning of s, write as many letters on the first line such that the total width does not exceed 100 pixels. Then, from where you stopped in s, continue writing as many letters as you can on the second line. Continue this process until you have written all of s.
Return an array result of length 2 where:

**Examples**

**Example 1:**

```
Input: widths = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], s = "abcdefghijklmnopqrstuvwxyz"
Output: [3,60]
Explanation: You can write s as follows:
abcdefghij  // 100 pixels wide
klmnopqrst  // 100 pixels wide
uvwxyz      // 60 pixels wide
There are a total of 3 lines, and the last line is 60 pixels wide.
```

**Example 2:**

```
Input: widths = [4,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], s = "bbbcccdddaaa"
Output: [2,4]
Explanation: You can write s as follows:
bbbcccdddaa  // 98 pixels wide
a            // 4 pixels wide
There are a total of 2 lines, and the last line is 4 pixels wide.
```

**Constraints**

- widths.length == 26
- 2 <= widths[i] <= 10
- 1 <= s.length <= 1000
- s contains only lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`，以及一个数组 `widths`，表示每个小写英文字母的像素宽度。具体地，`widths[0]` 表示字符 `'a'` 的宽度，`widths[1]` 表示字符 `'b'` 的宽度，依此类推。

需要将 `s` 按顺序写在若干行中，每行的总宽度不能超过 **100 像素**。首先从 `s` 的开头开始，在第一行写入尽可能多的字符，使得该行的累计宽度不超过 100 像素。随后在第二行继续从上一次停止的位置写入尽可能多的字符，依此类推，直到全部字符写完。

**返回** 一个长度为 2 的数组 `result`，其中  
- `result[0]` 为使用的行数；  
- `result[1]` 为最后一行的像素宽度。

## 示例

### 示例 1
**输入**  
```text
widths = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], 
s = "abcdefghijklmnopqrstuvwxyz"
```
**输出**  
```text
[3,60]
```
**解释**  
你可以这样写 `s`：  

```
abcdefghij  // 100 像素宽
klmnopqrst  // 100 像素宽
uvwxyz      // 60 像素宽
```  

共计 3 行，最后一行宽度为 60 像素。

### 示例 2
**输入**  
```text
widths = [4,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], 
s = "bbbcccdddaaa"
```
**输出**  
```text
[2,4]
```
**解释**  
你可以这样写 `s`：  

```
bbbcccdddaa  // 98 像素宽
a            // 4 像素宽
```  

共计 2 行，最后一行宽度为 4 像素。

## 约束条件
- `widths.length == 26`
- `2 <= widths[i] <= 10`
- `1 <= s.length <= 1000`
- `s` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从左到右一次遍历字符串**，每读一个字符就把它对应的宽度加到当前行的累计宽度 `cur` 上。  
如果加入这个字符后累计宽度已经超过 100 像素，就说明这行已经写不下了，需要**新开一行**，把累计宽度重新设为该字符的宽度（因为它必须写在新行的最左侧），行数 `lines` 加一。

> **类比**：想象你在纸上写字，每写完一个字就量一下这行已经用了多少厘米。如果再写下一个字会让这行超出 10 厘米的限制，就把笔移到下一行继续写。

这就是**贪心**的思想：每次尽可能把字符放进当前行，只要不违背“行宽 ≤ 100”。  
因为我们从左到右顺序写，**没有别的放置方式**可以让同样的字符占用更少的行数，所以这个方法一定是正确的。

下面给出一种**“暴力”**的实现：每次判断是否需要换行时，都重新遍历已经写好的字符，重新计算当前行的总宽度。虽然逻辑上可以工作，但会导致大量重复计算，时间复杂度会是 `O(n²)`（`n` 为字符串长度）。

#### 代码（Python）

```python
def number_of_lines_bruteforce(widths, s):
    # 把每个字符对应的宽度预先存到字典里，类似查字典
    w = {chr(ord('a') + i): widths[i] for i in range(26)}

    lines = 1          # 至少要有一行
    cur_width = 0      # 当前行已经使用的像素

    for ch in s:       # 逐个字符处理
        # 暴力做法：每次都把前面所有字符的宽度重新加一遍
        # 这里用一个临时列表模拟“已经写在当前行的字符”
        # （实际实现中可以直接用累加，但这里故意写成 O(n²) 形式）
        temp = []       # 保存当前行的字符
        for c in s:     # 重新遍历整条字符串（不优化）
            if c == ch:        # 只到达当前字符位置才停
                break
            if c in temp:      # 已经在当前行的字符不再重复计数
                continue
            temp.append(c)

        # 计算当前行的宽度（每次都重新算，故意慢）
        cur_width = sum(w[c] for c in temp)

        # 看加上当前字符后是否超过 100
        if cur_width + w[ch] > 100:
            lines += 1          # 换行
            cur_width = w[ch]   # 当前字符单独占新行
        else:
            cur_width += w[ch]  # 仍然写在当前行

    return [lines, cur_width]
```

> **注释**：  
> - `w` 把字母映射到宽度，类似查字典：`w['a']` 就是 `widths[0]`。  
> - `temp` 用来收集已经写在当前行的字符，每次都重新遍历 `s`，这一步是导致 `O(n²)` 的根源。  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - “平方”是什么意思？如果 `n=1000`，算法大约要执行 1,000,000 次基本操作。  
- **空间复杂度**：`O(1)`（不计返回结果），只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于每次都重新遍历已经处理过的字符**，来计算当前行的宽度。实际上我们根本不需要重新统计，只要**维护一个累计宽度** `cur_width`，每读一个字符就把它的宽度加进去，检查是否超过 100 即可。

**关键点**：

1. **累计宽度**：`cur_width` 记录当前行已经使用的像素数。  
2. **换行判断**：如果 `cur_width + width(ch) > 100`，说明当前字符放不下，需要**新开一行**，行数 `lines` 加一，`cur_width` 重新设为该字符的宽度（因为它必须写在新行的最左边）。  
3. **结束后**：遍历完整个字符串后，`lines` 表示总行数，`cur_width` 就是最后一行的宽度。

这正是**一次遍历（单遍）**的贪心算法，时间只和字符串长度线性相关，空间只用了常数级别的变量。

> **类比**：想象你在写字时，手里有一把尺子，随时记录这行已经用了多少厘米。每写完一个字，你把尺子上的数字加上这个字的宽度。如果超过 10 厘米，就把笔移到下一行，尺子重新归零，从新字的宽度开始计数。

#### 代码（Python）

```python
def number_of_lines(widths, s):
    """
    :param widths: List[int] 长度为 26，表示 a~z 每个字母的像素宽度
    :param s: str      待写的字符串，只含小写字母
    :return: List[int] [总行数, 最后一行的宽度]
    """
    # 把字符映射到宽度，直接用下标也可以，这里保持可读性
    w = {chr(ord('a') + i): widths[i] for i in range(26)}

    lines = 1          # 至少有一行
    cur_width = 0      # 当前行已占的像素

    for ch in s:
        char_width = w[ch]               # 当前字符的宽度
        # 若加上当前字符会超过 100，则另起新行
        if cur_width + char_width > 100:
            lines += 1                   # 行数加一
            cur_width = char_width       # 新行的宽度从当前字符开始
        else:
            cur_width += char_width      # 仍写在当前行

    return [lines, cur_width]
```

> **关键行解释**  
> - `if cur_width + char_width > 100:` 判断是否需要换行。  
> - `lines += 1` 与 `cur_width = char_width` 同时完成“新起一行并写下当前字符”。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，`n` 为 `s` 的长度。比如 `n=1000`，最多执行 1000 次循环，几乎是即时完成的。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量和一个长度固定为 26 的字典（可以直接用数组下标省去字典），与输入规模无关。

---

## 心得

- **核心技巧**：一次遍历累计宽度的**贪心**思路。  
- **适用的题型**：  
  1. “把数组装进容量为 C 的箱子，求最少箱子数”——如 LeetCode 1655 *Distribute Repeating Integers*。  
  2. “分割字符串，使每段长度不超过 K”——如 文字排版、行宽限制等题目。  
  3. “在固定容量的背包里尽可能装入物品，求装入的最大数量”——类似 0‑1 背包的贪心特例。  
- **一句话总结解题钥匙**：**“逐字符累计宽度，一旦超限立刻换行”**。

---

## 反思

- **第一反应**：看到“每行不超过 100 像素”，自然会想到**模拟写字的过程**，逐字符累加宽度。  
- **最容易踩的坑**：  
  - 忘记 **初始化** 行数为 1（即使字符串为空也要算一行），导致返回 `[0,0]` 错误。  
  - 边界情况：**恰好等于 100** 时仍应留在当前行，只有**大于** 100 才换行。  
  - 宽度数组和字符的对应关系：`widths[0]` 对应 `'a'`，容易写错下标。  
- **下次遇到同类题**：第一步先**想象实际操作过程**（比如写字、装箱），判断是否可以用**累计 + 换行/换箱**的方式一次遍历完成。这样就能迅速定位到贪心/滑动窗口的解法。