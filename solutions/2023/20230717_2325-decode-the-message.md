# #2325. 解码信息 / Decode the Message

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/decode-the-message/)

---

## 题目（英文原版）

**Description**

You are given the strings key and message, which represent a cipher key and a secret message, respectively. The steps to decode message are as follows:
Return the decoded message.

**Examples**

**Example 1:**

```
Input: key = "the quick brown fox jumps over the lazy dog", message = "vkbs bs t suepuv"
Output: "this is a secret"
Explanation: The diagram above shows the substitution table.
It is obtained by taking the first appearance of each letter in "the quick brown fox jumps over the lazy dog".
```

**Example 2:**

```
Input: key = "eljuxhpwnyrdgtqkviszcfmabo", message = "zwx hnfx lqantp mnoeius ycgk vcnjrdb"
Output: "the five boxing wizards jump quickly"
Explanation: The diagram above shows the substitution table.
It is obtained by taking the first appearance of each letter in "eljuxhpwnyrdgtqkviszcfmabo".
```

**Constraints**

- 26 <= key.length <= 2000
- key consists of lowercase English letters and ' '.
- key contains every letter in the English alphabet ('a' to 'z') at least once.
- 1 <= message.length <= 2000
- message consists of lowercase English letters and ' '.

---

## 题目（中文翻译）

给定字符串 **key** 和 **message**，它们分别表示密码键（cipher key）和密文（secret message）。解码 **message** 的步骤如下：

1. 根据 **key** 构建一个替换表（substitution table）。该表通过依次取 **key** 中每个字母第一次出现的顺序来建立，空格被忽略。
2. 使用替换表将 **message** 中的每个字母替换为对应的原始字母。空格保持不变。
3. 返回解码后的字符串。

### 示例

#### 示例 1
**输入**  
``` 
key = "the quick brown fox jumps over the lazy dog"
message = "vkbs bs t suepuv"
```  
**输出**  
```
this is a secret
```  
**解释**  
上图展示了替换表（substitution table）。该表是通过取 `"the quick brown fox jumps over the lazy dog"` 中每个字母第一次出现的顺序得到的。

#### 示例 2
**输入**  
``` 
key = "eljuxhpwnyrdgtqkviszcfmabo"
message = "zwx hnfx lqantp mnoeius ycgk vcnjrdb"
```  
**输出**  
```
the five boxing wizards jump quickly
```  
**解释**  
上图展示了替换表（substitution table）。该表是通过取 `"eljuxhpwnyrdgtqkviszcfmabo"` 中每个字母第一次出现的顺序得到的。

### 约束条件
- `26 <= key.length <= 2000`
- `key` 只包含小写英文字母和空格 `' '`。
- `key` 至少包含英文字母表中的每个字母（`'a'` 到 `'z'`）一次。
- `1 <= message.length <= 2000`
- `message` 只包含小写英文字母和空格 `' '`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个要翻译的字符，都去钥匙 `key` 里找它对应的原始字母**。  
可以把 `key` 看成一本“密码字典”，但我们不提前把它整理成表，而是**每次都线性扫描**：

1. **遍历 `message` 中的每个字符**  
2. 如果是空格，直接保留。  
3. 否则，从 `key` 的左到右依次检查字符 `c`，把第一次出现的 `c` 对应的英文字母（`a、b、c…`）记下来。  
   - 这一步类似于在一本字典里**顺序查词**，每找一次都要从头到尾翻一遍。  
4. 把找到的原始字母加入答案字符串。

因为 `key` 中每个字母至少出现一次，最终一定能找到对应关系。

> **为什么能对上**：题目说明“取 `key` 中每个字母第一次出现的顺序，映射到 `'a'~'z'`”。我们每次都重新遍历 `key`，自然会得到相同的映射。

#### 代码（Python）

```python
def decodeMessage_bruteforce(key: str, message: str) -> str:
    # 记录答案字符
    decoded_chars = []

    # 遍历密文中的每个字符
    for ch in message:
        if ch == ' ':                     # 空格直接保留
            decoded_chars.append(' ')
            continue

        # 暴力在 key 中找第一次出现的位置
        # 这里的 i 表示第 i 个出现的不同字母，对应的原始字母是 chr(ord('a') + i)
        seen = set()                      # 已经出现过的字符集合，防止重复计数
        idx = 0                           # 计数器，表示已经遇到第几个不同字母
        for kch in key:                   # 线性扫描 key
            if kch == ' ':                # 跳过空格
                continue
            if kch not in seen:           # 第一次出现
                seen.add(kch)
                if kch == ch:              # 找到要翻译的字符
                    # 用 idx 对应的英文字母填入答案
                    decoded_chars.append(chr(ord('a') + idx))
                    break
                idx += 1                   # 继续往后找下一个不同字母

    return ''.join(decoded_chars)
```

#### 复杂度

- **时间复杂度：** `O(m * n)`  
  - `m` 为 `message` 长度，`n` 为 `key` 长度。  
  - 直观上可以理解为“每翻译一个字符，都要把钥匙整本书翻一遍”，所以时间会随两者乘积增长。  
- **空间复杂度：** `O(1)`（不计答案字符串）  
  - 只用了常数级别的额外变量 `seen`、`idx`、`decoded_chars`（答案本身不算额外空间）。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都要遍历完整个 `key`** 来找映射，导致 `O(m·n)`。  
我们可以把这一步提前做一次，**一次遍历 `key`，建立从密码字符到真实字符的映射表**（哈希表），后面翻译 `message` 时只需 O(1) 查表。

1. **构造映射表**  
   - 从左到右遍历 `key`，遇到第一次出现的字母就把它映射到当前的英文字母（`'a' + cnt`），`cnt` 从 0 开始递增。  
   - 用 Python 的字典（`dict`）实现，类似“查字典”：键是密码字符，值是对应的真实字符。  
2. **翻译 `message`**  
   - 再遍历一次 `message`，如果是空格直接保留，否则用字典快速查到对应字符。  

这样 **只需要两次线性遍历**，时间降到 `O(m + n)`，空间使用 `O(26)`（只存 26 条映射），是最优的。

#### 代码（Python）

```python
def decodeMessage(key: str, message: str) -> str:
    """
    通过一次遍历 key 构造映射表，再一次遍历 message 完成译码。
    """
    # 1. 构造映射表：密码字符 -> 原始字符
    mapping = {}                # 类似于“查字典”，key 为密文字母，value 为真实字母
    cur = ord('a')              # 当前应该映射到的英文字母，从 'a' 开始

    for ch in key:
        if ch == ' ':           # 空格不参与映射
            continue
        if ch not in mapping:   # 只记录第一次出现
            mapping[ch] = chr(cur)
            cur += 1            # 下一个真实字母
        if cur > ord('z'):      # 已经映射完 26 个字母，后面可以提前结束
            break

    # 2. 翻译 message
    decoded = []
    for ch in message:
        if ch == ' ':
            decoded.append(' ')
        else:
            decoded.append(mapping[ch])   # 字典查表，时间 O(1)

    return ''.join(decoded)
```

#### 复杂度

- **时间复杂度：** `O(m + n)`  
  - `n` 为 `key` 长度，`m` 为 `message` 长度。  
  - 可以把它想成“先把钥匙翻成一本完整的字典（一次遍历），再把密文逐字查表（再次遍历）”，总共只走两遍。  
- **空间复杂度：** `O(26) ≈ O(1)`  
  - 只保存 26 条映射关系，常数级别的额外空间。

---

## 心得

- **核心技巧**：**一次遍历构造哈希映射**，随后 O(1) 查表。  
- **适用的题型**：  
  1. 字符替换类（如“字母异位词映射”“密码解码”）。  
  2. 需要把一组唯一元素映射到另一组唯一元素的场景（如“字符统计→排名”）。  
- **解题钥匙**：**把重复的线性搜索提前为一次预处理，用哈希表一次搞定对应关系**。

---

## 反思

- **第一反应**：看到“把 key 中第一次出现的字母依次映射到 a~z”，立刻想到要把 `key` 变成一个映射表。  
- **最容易踩的坑**：  
  - 忽略 `key` 中的空格，导致映射表多出空格键。  
  - 未只记录第一次出现，导致后面的重复字母覆盖了正确映射。  
  - 翻译 `message` 时忘记保留空格，输出会全部粘在一起。  
- **下次遇到同类题**，第一步应该：**遍历一次构造唯一映射（哈希表或数组），再一次遍历原串做查表**。这样即可避免 O(n²) 的低效搜索。