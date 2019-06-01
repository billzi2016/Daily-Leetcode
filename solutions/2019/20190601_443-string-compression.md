# #443. 字符串压缩 / String Compression

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/string-compression/)

---

## 题目（英文原版）

**Description**

Given an array of characters chars, compress it using the following algorithm:
Begin with an empty string s. For each group of consecutive repeating characters in chars:
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.
After you are done modifying the input array, return the new length of the array.
You must write an algorithm that uses only constant extra space.

**Examples**

**Example 1:**

```
Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
```

**Example 2:**

```
Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.
```

**Example 3:**

```
Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
```

**Constraints**

- 1 <= chars.length <= 2000
- chars[i] is a lowercase English letter, uppercase English letter, digit, or symbol.

---

## 题目（中文翻译）

给定一个字符数组 `chars`，请使用以下算法对其进行压缩：

- 从空字符串 `s` 开始。对于 `chars` 中每一组连续重复的字符（consecutive repeating characters）：
- 将压缩后的结果 **不** 另行返回，而是直接写回到输入的字符数组 `chars` 中。注意，长度大于等于 `10` 的组需要拆分为多个字符写入 `chars`。
- 完成对输入数组的修改后，返回数组的新长度。

要求使用 **常数额外空间**（constant extra space）实现该算法。

---

### 示例

**示例 1**  
**输入**：`chars = ["a","a","b","b","c","c","c"]`  
**输出**：返回 `6`，且数组前 `6` 个字符应为 `["a","2","b","2","c","3"]`  
**解释**：分组为 `"aa"`、`"bb"`、`"ccc"`，压缩后得到 `"a2b2c3"`。

**示例 2**  
**输入**：`chars = ["a"]`  
**输出**：返回 `1`，且数组前 `1` 个字符应为 `["a"]`  
**解释**：唯一的分组是 `"a"`，因为只有单个字符，不需要压缩。

**示例 3**  
**输入**：`chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]`  
**输出**：返回 `4`，且数组前 `4` 个字符应为 `["a","b","1","2"]`  
**解释**：分组为 `"a"` 和 `"bbbbbbbbbbbb"`，压缩后得到 `"ab12"`。

---

### 约束条件

- `1 <= chars.length <= 2000`
- `chars[i]` 为小写英文字母、大写英文字母、数字或符号。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**先把压缩后的结果完整地生成出来**，再把它一次性拷贝回原数组 `chars`。  
- **遍历**：从左到右扫描 `chars`，统计每一段连续相同字符的长度（比如 `"aaa"` 长度是 3）。  
- **生成**：把字符本身写进去，如果长度大于 1，就把长度拆成每位数字（`3 → "3"`，`12 → "1","2"`）依次写进去。  
- **拷贝回原数组**：把生成的列表直接赋值给 `chars[:len(result)]`，返回结果长度。  

> 类比：把一段文字先抄到新的纸上（这一步用的是“额外的纸”，相当于额外的数组），等抄完了再把新纸上的内容搬回原来的本子。

这种办法显然是 **正确** 的，因为我们完全按照题目要求把每一组字符及其计数写出来了，只是多用了一个临时的存储空间。

#### 代码（Python）  
```python
def compress(chars):
    """
    暴力实现：先用额外列表生成压缩结果，再拷贝回原数组
    """
    n = len(chars)
    i = 0               # 读取指针，遍历原数组
    compressed = []    # 临时存放压缩后的字符（额外空间）

    while i < n:
        cur = chars[i]          # 当前字符
        count = 0               # 统计该字符连续出现的次数
        while i < n and chars[i] == cur:
            i += 1
            count += 1

        # 写入字符本身
        compressed.append(cur)
        # 若出现次数 > 1，需要把次数拆成单个数字写入
        if count > 1:
            for d in str(count):    # 把整数转成字符串，再逐位取字符
                compressed.append(d)

    # 把压缩结果拷贝回原数组
    chars[:len(compressed)] = compressed
    return len(compressed)
```

#### 复杂度  
- **时间复杂度：** `O(n)` —— 只遍历了一遍原数组（`n` 为字符个数），每个字符最多被访问两次（一次计数，一次拷贝），所以时间随 `n` 成线性关系。  
- **空间复杂度：** `O(n)` —— 需要额外的列表 `compressed` 最坏情况下会和原数组等长（比如所有字符都不相同时），这违背了 “常数额外空间” 的要求。  

---  

### 2. 最优解  

#### 思路  
暴力解的 **瓶颈** 在于使用了额外的数组。  
我们可以 **原地** 完成压缩：在同一个数组里用两个指针交替工作——  

1. **读取指针 `read`**：负责遍历整个 `chars`，找到每一段相同字符的结束位置，统计出现次数。  
2. **写入指针 `write`**：负责把压缩后的字符和计数写回 `chars` 的前面位置。  

关键点在于**计数的写法**：如果出现次数大于 1，需要把它拆成单个字符（例如 `12 → '1','2'`），这可以通过 `str(count)` 再逐字符写入实现。  

整个过程只使用了常数级别的额外变量（几个整数指针），符合 “O(1) 额外空间” 的要求。

> 类比：把一串珠子（字符）排好后，用两只手 **同步** 前进。左手（`read`）负责数珠子，右手（`write`）负责把数好的结果放到左边的空位里。左手跑得快，右手只在需要写东西时才动。

#### 代码（Python）  
```python
def compress(chars):
    """
    双指针原地压缩：只使用 O(1) 额外空间
    """
    n = len(chars)
    read = 0      # 读取指针，遍历原数组
    write = 0     # 写入指针，负责把压缩结果写回前面

    while read < n:
        cur = chars[read]   # 当前字符
        count = 0

        # 统计连续相同字符的数量
        while read < n and chars[read] == cur:
            read += 1
            count += 1

        # ① 写入字符本身
        chars[write] = cur
        write += 1

        # ② 若出现次数 > 1，写入计数的每一位
        if count > 1:
            for digit in str(count):   # 把整数转成字符串，再逐位写入
                chars[write] = digit
                write += 1

    # 最终压缩后的长度就是 write 指针所在的位置
    return write
```

#### 复杂度  
- **时间复杂度：** `O(n)` —— 每个字符至多被 `read` 指针访问一次，计数转换为字符串的过程总共也只会产生不超过 `log10(n)` 位的额外字符，整体仍然是线性时间。  
- **空间复杂度：** `O(1)` —— 只用了几个整数变量 `read、write、count`，不随输入规模增长而增加，符合常数额外空间的要求。  
- 与暴力解对比：**时间相同**（都是线性），但**空间从 O(n) 降到了 O(1)**，这是面试中常考的优化点。

---  

## 心得  

- **核心技巧**：**双指针（Two Pointers）原地操作**。一个指针负责读取，另一个负责写入，能够在同一数组里完成压缩或去重等任务。  
- **适用题型**：  
  1. **字符串/数组原地压缩**（如本题 `String Compression`）。  
  2. **有序数组去重**（LeetCode 26 `Remove Duplicates from Sorted Array`）。  
  3. **移动零**（LeetCode 283 `Move Zeroes`）。  
- **一句话总结解题钥匙**：**“让读指针跑遍全场，写指针只在需要留下痕迹时才动”。**  

---  

## 反思  

- **第一反应**：看到“压缩”“原地”关键词，马上想到 **双指针** 或者 **快慢指针**，但最开始可能会犹豫计数怎么写回。  
- **最容易踩的坑**：  
  - **计数为 1 时不写数字**（只写字符本身）。  
  - **计数大于 9 需要拆位**，直接把整数写进去会出错，需要逐位写入。  
  - **返回值要是写指针的位置**，而不是原数组长度。  
- **下次类似题的第一步**：**先明确“读取一次、写入一次”的两指针框架，再考虑特殊情况（计数为 1、计数多位等）**。这样可以迅速搭建出 O(1) 空间的解法。