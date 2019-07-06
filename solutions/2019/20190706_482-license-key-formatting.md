# #482. 许可证密钥格式化 / License Key Formatting

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/license-key-formatting/)

---

## 题目（英文原版）

**Description**

You are given a license key represented as a string s that consists of only alphanumeric characters and dashes. The string is separated into n + 1 groups by n dashes. You are also given an integer k.
We want to reformat the string s such that each group contains exactly k characters, except for the first group, which could be shorter than k but still must contain at least one character. Furthermore, there must be a dash inserted between two groups, and you should convert all lowercase letters to uppercase.
Return the reformatted license key.

**Examples**

**Example 1:**

```
Input: s = "5F3Z-2e-9-w", k = 4
Output: "5F3Z-2E9W"
Explanation: The string s has been split into two parts, each part has 4 characters.
Note that the two extra dashes are not needed and can be removed.
```

**Example 2:**

```
Input: s = "2-5g-3-J", k = 2
Output: "2-5G-3J"
Explanation: The string s has been split into three parts, each part has 2 characters except the first part as it could be shorter as mentioned above.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of English letters, digits, and dashes '-'.
- 1 <= k <= 104

---

## 题目（中文翻译）

给定一个只包含字母数字字符（alphanumeric characters）和破折号（dash）的字符串 `s`，该字符串被 `n` 个破折号分成了 `n + 1` 组。另给定一个整数 `k`。  

请重新格式化字符串 `s`，使得每一组恰好包含 `k` 个字符，**除第一组外**，第一组可以少于 `k` 个字符，但必须至少包含一个字符。组与组之间需要插入破折号，并且所有小写字母都要转换为大写字母。  

返回重新格式化后的许可证密钥。

## 示例

### 示例 1
**输入**  
` s = "5F3Z-2e-9-w", k = 4 `  

**输出**  
`"5F3Z-2E9W"`  

**解释**  
字符串 `s` 被重新划分为两部分，每部分恰好有 4 个字符。原本多余的两个破折号不再需要，已被移除。

### 示例 2
**输入**  
` s = "2-5g-3-J", k = 2 `  

**输出**  
`"2-5G-3J"`  

**解释**  
字符串 `s` 被重新划分为三部分，每部分恰好有 2 个字符，唯一例外是第一部分可以短于 `k`（如本例所示）。

## 约束条件

- `1 <= s.length <= 10^5`
- `s` 只包含英文字母、数字和破折号 `'-'`。
- `1 <= k <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把原始字符串先全部清理干净**，再按照题目要求重新分组。

1. **去掉所有的破折号**  
   把字符 `'-'` 当成垃圾，把它们全部删掉。可以把字符串当成一本书，破折号就像是书页上的污渍，先把污渍擦掉再继续阅读。

2. **全部转成大写**  
   题目要求所有字母必须是大写。把每个小写字母想象成一本字典里的词条，查到后统一改成大写形式。

3. **重新分组**  
   - 先把清理好的字符放进一个列表 `clean`，长度记作 `n`。  
   - 计算第一组的长度 `first_len = n % k`（如果余数为 0，说明第一组恰好也是 `k` 长）。  
   - 从左到右依次取 `first_len`、`k`、`k`… 个字符，用 `'-'` 把每组连接起来。  

这样得到的就是符合要求的 license key。

> **为什么这个方法一定对？**  
> - 去掉破折号后，所有剩余字符的相对顺序没有改变，题目只要求保持字符顺序不变。  
> - 按照 `first_len` 再每 `k` 个字符切分，恰好满足“第一组可以短，后面每组恰好 `k` 个”的规则。  

#### 代码（Python）

```python
def licenseKeyFormatting_bruteforce(s: str, k: int) -> str:
    # 1. 删除所有破折号，并转成大写
    # 类比：把破折号当成垃圾，全部清理掉；把字母当成单词，统一变成大写的词条
    clean = [ch.upper() for ch in s if ch != '-']

    n = len(clean)                     # 剩余字符的总数
    if n == 0:                         # 特殊情况：全是破折号
        return ""

    first_len = n % k                  # 第一组的长度，可能为 0（表示恰好 k）
    parts = []                         # 用来存放每一组

    # 2. 处理第一组（如果 first_len 为 0，则第一组也取 k 个）
    idx = 0
    if first_len != 0:
        parts.append(''.join(clean[idx:idx + first_len]))
        idx += first_len

    # 3. 之后每次取 k 个字符
    while idx < n:
        parts.append(''.join(clean[idx:idx + k]))
        idx += k

    # 4. 用破折号把所有组拼起来
    return '-'.join(parts)
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  这里的 `n` 是字符串 `s` 的长度。我们只遍历了一遍字符串（去掉破折号、转大写），再遍历一次 `clean` 列表来切分，整体是线性时间。  
  大白话：如果 `s` 有 1000 个字符，程序大约会做 1000 次“看一眼并处理”，不会出现指数级的爆炸。

- **空间复杂度：** `O(n)`  
  需要额外的列表 `clean` 来保存去掉破折号后的字符，以及 `parts` 保存每组子串，最坏情况下占用和原字符串等量的空间。

---

### 2. 最优解

#### 思路  

暴力解已经是线性的时间，但它在**处理第一组**时需要先算出 `first_len`，代码稍显繁琐。  
我们可以把**从后往前**构造每组的思路运用进来，省去对第一组特殊处理的步骤。

核心想法：

1. **同样先清理字符**（去掉破折号、转大写），得到 `clean`。
2. **从右往左遍历** `clean`，每读取 `k` 个字符就往结果里插入一个破折号。  
   - 想象把字符倒着排成一条线，左手每抓满 `k` 个就打一个记号（破折号），最后再把整条线翻过来。  
   - 这样做的好处是**不需要事先知道第一组的长度**，因为最后翻转后，第一组自然会是剩余的那一小段（可能不足 `k`）。
3. **把构造好的字符序列翻转**，得到最终的 license key。

这就是常见的“逆序分组”技巧，能够让代码更简洁且只用一次遍历。

#### 代码（Python）

```python
def licenseKeyFormatting_optimal(s: str, k: int) -> str:
    # 1. 清理字符：去掉破折号并转成大写
    clean = [ch.upper() for ch in s if ch != '-']

    # 2. 从后往前每 k 个字符插入一次破折号
    res = []            # 用列表收集字符，最后一次性转成字符串
    count = 0           # 当前已经放进当前组的字符数

    for ch in reversed(clean):   # 逆序遍历
        res.append(ch)           # 先放字符
        count += 1
        if count == k:           # 当前组已经满 k 个
            res.append('-')      # 插入破折号作为组间分隔
            count = 0            # 重新计数，开始新的一组

    # 3. 可能最后多加了一个破折号，去掉它
    if res and res[-1] == '-':
        res.pop()

    # 4. 逆序回来并拼成字符串
    return ''.join(reversed(res))
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  仍然只遍历一次原字符串（去除破折号），再一次逆序遍历 `clean`，整体线性。相比暴力解，**没有额外的“计算第一组长度”这一步**，但数量级相同，只是常数更小。

- **空间复杂度：** `O(n)`  
  需要保存清理后的字符 `clean`（`O(n)`），以及结果列表 `res`（同样最多 `n + n/k` 个元素），总体仍是线性空间。

---

## 心得

- **核心技巧**：逆序分组（从后往前每 `k` 个字符插入分隔符），可以省去对“第一组可能不足 `k`”的特殊处理，让代码更简洁。
- **适用场景**  
  1. **License Key Formatting**（本题）  
  2. **分割字符串为固定长度的子串**（如把一串数字每 3 位加逗号）  
  3. **逆序遍历实现的滑动窗口**（如把二进制数每 4 位加空格）
- **一句话总结**：把“从左到右先算第一组长度”换成“从右往左直接每 k 个加分隔符”，自然得到符合要求的第一组。

---

## 反思

- **拿到题目第一反应**：先把所有破折号删掉，剩下的字符直接分组。于是想到先算出第一组的长度，然后顺序切分。
- **最容易踩的坑**  
  - **全部是破折号**：清理后可能为空，需要提前返回空串。  
  - **最后多余的破折号**：逆序构造时如果恰好在末尾插入了 `'-'`，要记得删除。  
  - **大小写转换**：忘记把小写字母统一转成大写会导致答案错误。  
- **下次遇到同类题**：第一步想到“先把无关字符（破折号、空格等）全部去掉”，第二步考虑“是否可以逆序处理，省去首组特殊情况”。这样可以快速得到简洁且高效的解法。