# #393. UTF-8 验证 / UTF-8 Validation

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/utf-8-validation/)

---

## 题目（英文原版）

**Description**

Given an integer array data representing the data, return whether it is a valid UTF-8 encoding (i.e. it translates to a sequence of valid UTF-8 encoded characters).
A character in UTF8 can be from 1 to 4 bytes long, subjected to the following rules:
This is how the UTF-8 encoding would work:
x denotes a bit in the binary form of a byte that may be either 0 or 1.
Note: The input is an array of integers. Only the least significant 8 bits of each integer is used to store the data. This means each integer represents only 1 byte of data.

**Examples**

**Example 1:**

```
Number of Bytes   |        UTF-8 Octet Sequence
                       |              (binary)
   --------------------+-----------------------------------------
            1          |   0xxxxxxx
            2          |   110xxxxx 10xxxxxx
            3          |   1110xxxx 10xxxxxx 10xxxxxx
            4          |   11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
```

**Example 2:**

```
Input: data = [197,130,1]
Output: true
Explanation: data represents the octet sequence: 11000101 10000010 00000001.
It is a valid utf-8 encoding for a 2-bytes character followed by a 1-byte character.
```

**Example 3:**

```
Input: data = [235,140,4]
Output: false
Explanation: data represented the octet sequence: 11101011 10001100 00000100.
The first 3 bits are all one's and the 4th bit is 0 means it is a 3-bytes character.
The next byte is a continuation byte which starts with 10 and that's correct.
But the second continuation byte does not start with 10, so it is invalid.
```

**Constraints**

- 1 <= data.length <= 2 * 104
- 0 <= data[i] <= 255

---

## 题目（中文翻译）

给定一个整数数组 `data` 表示字节序列，返回它是否是一个有效的 UTF-8 编码（即它能被翻译为一系列合法的 UTF-8 编码字符）。

UTF-8 中的一个字符可以由 1 到 4 个字节（byte）组成，需满足以下规则：

- **1 字节字符**：首位为 `0`，其余 7 位为字符的二进制表示。  
  格式：`0xxxxxxx`

- **2 字节字符**：首字节以 `110` 开头，后面紧跟 **1 个** 以 `10` 开头的后续字节（continuation byte）。  
  格式：`110xxxxx 10xxxxxx`

- **3 字节字符**：首字节以 `1110` 开头，后面紧跟 **2 个** 以 `10` 开头的后续字节。  
  格式：`1110xxxx 10xxxxxx 10xxxxxx`

- **4 字节字符**：首字节以 `11110` 开头，后面紧跟 **3 个** 以 `10` 开头的后续字节。  
  格式：`11110xxx 10xxxxxx 10xxxxxx 10xxxxxx`

> **注意**：输入是一个整数数组。每个整数的最低有效 8 位用于存储数据，也就是说每个整数只表示 1 个字节（byte）。

---

### 示例

#### 示例 1：UTF-8 字节模式表

| 字节数 | UTF-8 八位字节序列（二进制） |
|-------|----------------------------|
| 1     | `0xxxxxxx`                 |
| 2     | `110xxxxx 10xxxxxx`        |
| 3     | `1110xxxx 10xxxxxx 10xxxxxx` |
| 4     | `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx` |

#### 示例 2
```text
Input: data = [197,130,1]
Output: true
Explanation: data 表示的八位字节序列为 11000101 10000010 00000001。  
这是一段合法的 UTF-8 编码：前两个字节构成一个 2 字节字符，最后一个字节构成一个 1 字节字符。
```

#### 示例 3
```text
Input: data = [235,140,4]
Output: false
Explanation: data 表示的八位字节序列为 11101011 10001100 00000100。  
前 3 位都是 `1`，第 4 位是 `0`，说明它应该是一个 3 字节字符。  
第二个字节以 `10` 开头，是合法的后续字节。但第三个字节不是以 `10` 开头，因而整个序列无效。
```

---

### 约束条件
- `1 <= data.length <= 2 * 10^4`
- `0 <= data[i] <= 255`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
我们把 `data` 看成一串 **字节**（每个整数只保留最低 8 位），按照 UTF‑8 的规则逐个检查。  
最直接的做法是：

1. **从左到右遍历** 每个字节。  
2. 先看当前字节的最高几位，统计连续的 `1` 有多少个（这叫 *前导 1*）。  
   - `0` 开头 → 说明这是 **单字节**（长度 1）。  
   - `110` 开头 → 说明这是 **双字节**（长度 2）。  
   - `1110` 开头 → 说明是 **三字节**（长度 3）。  
   - `11110` 开头 → 说明是 **四字节**（长度 4）。  
   - 其它情况（比如前导 1 的数量是 5 或者 0 但不是 `0xxxxxxx`）直接返回 `False`。  
3. 依据前导 1 的数量，**检查后面的 continuation bytes** 是否全部以 `10` 开头。  
   - `10xxxxxx` 用十进制掩码 `0b10000000`（128）判断最高位是否为 1，且 `0b01000000`（64）判断次高位是否为 0。  
4. 如果所有字节都符合规则，返回 `True`。

> **类比**：把字节想成一本书的每一页，前导 1 告诉我们这页是独立章节（单字节）还是需要后面几页一起才能完整（多字节）。后面的 `10xxxxxx` 就像“续页”，必须按顺序出现，否则章节不完整。

这个方法 **必然** 正确，因为我们把 UTF‑8 的每一条规范都逐条检查了一遍。

#### 代码（Python）  

```python
def validUtf8(data):
    """
    :type data: List[int]
    :rtype: bool
    """
    n = len(data)
    i = 0                       # 当前处理的下标

    while i < n:
        # 取当前字节的最高 5 位，帮助判断前导 1 的个数
        first = data[i] & 0b11111000   # 只保留前 5 位

        # 统计前导 1 的数量（最多 4）
        if   first >> 3 == 0b0:   # 0xxxxxxx → 1 byte
            num_bytes = 1
        elif first >> 5 == 0b110: # 110xxxxx → 2 bytes
            num_bytes = 2
        elif first >> 4 == 0b1110:# 1110xxxx → 3 bytes
            num_bytes = 3
        elif first >> 3 == 0b11110:# 11110xxx → 4 bytes
            num_bytes = 4
        else:                     # 其他模式非法
            return False

        # 检查是否还有足够的字节供 “continuation”
        if i + num_bytes > n:
            return False

        # 对后面的 continuation bytes 做 “10xxxxxx” 检查
        for j in range(1, num_bytes):
            # 0b10xxxxxx 的二进制掩码是 0b11000000（192），
            # 且必须等于 0b10000000（128）
            if (data[i + j] & 0b11000000) != 0b10000000:
                return False

        # 跳过已经验证的这几个字节，继续往后
        i += num_bytes

    return True
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 我们只遍历一次数组，每个字节最多检查它自己和后面最多 3 个 continuation byte，常数级别的操作可以视作一次遍历。  
  - 用大白话说，就是 **线性**，数据多多少倍，耗时也会相应增加同样的倍数。  

- **空间复杂度：** `O(1)`  
  - 只用了几个整数变量（`i、first、num_bytes`），不随输入规模增长。  

---

### 2. 最优解  

#### 思路  

从暴力思路看，**慢的地方** 其实只有两点：

1. **每次都用位运算算前导 1 的个数**（虽然已经是 O(1)），但可以直接用「掩码」一次性判断。  
2. **循环检查 continuation bytes**，如果把检查过程写得更直观、更易读，也可以避免不必要的分支。

**最优解** 仍然是线性遍历，只是把「数前导 1」的过程改写成「匹配固定的掩码」：

| 字节数 | 掩码（mask） | 期望值（expected） |
|-------|--------------|-------------------|
| 1     | `0b10000000` (128) | `0b00000000` (0)   |
| 2     | `0b11100000` (224) | `0b11000000` (192) |
| 3     | `0b11110000` (240) | `0b11100000` (224) |
| 4     | `0b11111000` (248) | `0b11110000` (240) |

- 对首字节，用上述四组 **mask‑expected** 逐一匹配，找到符合的字符长度 `num_bytes`。  
- 然后检查后面的 `num_bytes‑1` 个字节是否都满足 `byte & 0b11000000 == 0b10000000`（即 `10xxxxxx`）。  

因为 UTF‑8 的规则是 **固定的四种模式**，我们不需要“数前导 1”，直接 **匹配** 即可。这种写法更简洁，也更易于把规则记下来。

#### 代码（Python）  

```python
def validUtf8(data):
    """
    最优写法：用固定的掩码直接匹配每种 UTF‑8 开头模式。
    """
    # (mask, expected, total_bytes) 的三元组
    patterns = [
        (0b10000000, 0b00000000, 1),  # 0xxxxxxx
        (0b11100000, 0b11000000, 2),  # 110xxxxx
        (0b11110000, 0b11100000, 3),  # 1110xxxx
        (0b11111000, 0b11110000, 4)   # 11110xxx
    ]

    i = 0
    n = len(data)

    while i < n:
        first = data[i]
        # 找到匹配的模式
        for mask, expect, total in patterns:
            if (first & mask) == expect:
                num_bytes = total
                break
        else:               # 循环结束也没有 break → 不合法
            return False

        # 检查后面的 continuation bytes 是否足够且满足 10xxxxxx
        if i + num_bytes > n:
            return False
        for j in range(1, num_bytes):
            if (data[i + j] & 0b11000000) != 0b10000000:
                return False

        i += num_bytes      # 跳过已经验证的字节

    return True
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 与暴力解相同的线性遍历，只是每个字节的判断常数更小。可以说是 **最简** 的线性解。  

- **空间复杂度：** `O(1)`  
  - 只用了常数个变量和一个长度为 4 的固定列表 `patterns`，不随输入规模变化。  

---

## 心得  

- **核心技巧**：利用 **位掩码**（mask）快速匹配固定的二进制模式。  
- **适用题型**：  
  1. 判断二进制协议是否合法（如网络协议帧头检查）。  
  2. 检测特定编码或压缩格式的前缀（如 UTF‑16、Morse Code）。  
  3. 判断整数数组是否满足某种位模式（如 “只出现一次的数字” 的位运算技巧）。  
- **一句话总结**：**把规则写成“掩码‑期望值”对，直接匹配即可**。  

---

## 反思  

- **第一反应**：先把每个字节转成二进制字符串，手动数前导 `1`，感觉最直观。  
- **最容易踩的坑**：  
  - 忘记检查 **字节是否足够**（越界）导致 `IndexError`。  
  - 把 `10xxxxxx` 的判断写成 `byte & 0b10000000 == 0b10000000`（只检查最高位），遗漏了第二位必须是 `0`。  
  - 处理 **单字节** 时误把 `0xxxxxxx` 当成 “前导 0 个 1” 而导致 `num_bytes = 0`。  
- **下次遇到同类题**：第一步先 **列出所有合法的位模式 + 对应的掩码**，再在遍历中直接匹配，这样既安全又高效。