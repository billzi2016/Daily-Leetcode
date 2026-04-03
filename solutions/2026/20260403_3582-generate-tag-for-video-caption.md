# #3582. Generate Tag for Video Caption / Generate Tag for Video Caption

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/generate-tag-for-video-caption/)

---

## 题目（英文原版）

**Description**

You are given a string caption representing the caption for a video.
The following actions must be performed in order to generate a valid tag for the video:
Return the tag after performing the actions on caption.

**Examples**

**Example 1:**

```
Input: caption = "Leetcode daily streak achieved"
Output: "#leetcodeDailyStreakAchieved"
Explanation:
The first letter for all words except "leetcode" should be capitalized.
```

**Example 2:**

```
Input: caption = "can I Go There"
Output: "#canIGoThere"
Explanation:
The first letter for all words except "can" should be capitalized.
```

**Example 3:**

```
Input: caption = "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
Output: "#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
Explanation:
Since the first word has length 101, we need to truncate the last two letters from the word.
```

**Constraints**

- 1 <= caption.length <= 150
- caption consists only of English letters and ' '.

---

## 题目（中文翻译）

给定一个字符串 `caption`，表示视频的字幕（caption）。需要按照以下步骤生成该视频的合法标签（tag）：

- 在处理后的字符串前添加字符 `#`。
- 第一个单词保持原样（全部小写），其余单词的首字母全部大写，其余字母保持原样，形成驼峰式（CamelCase）风格。
- 若第一个单词的长度超过 **100**，需要截掉其最后的两个字符，使其长度不超过 100。

返回对 `caption` 执行上述操作后得到的标签。

**示例 1**  
输入: `caption = "Leetcode daily streak achieved"`  
输出: `"#leetcodeDailyStreakAchieved"`  
解释: 除了第一个单词 `"leetcode"`，其余单词的首字母均需大写。

**示例 2**  
输入: `caption = "can I Go There"`  
输出: `"#canIGoThere"`  
解释: 除了第一个单词 `"can"`，其余单词的首字母均需大写。

**示例 3**  
输入: `caption = "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"`  
输出: `"#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"`  
解释: 第一个单词长度为 101，需要截去最后两个字符。

**约束条件**  
- `1 <= caption.length <= 150`  
- `caption` 仅由英文字母和空格 `' '` 构成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把句子拆成单词**  
   `caption` 只由英文字母和空格组成，用 `split()` 按空格切分即可。把每个单词想象成一段文字，就像把一本书拆成一页页的纸。

2. **按照要求处理每个单词**  
   - 第一个单词保持原样（不管大小写）。  
   - 其余单词的首字母要大写，后面的字符保持不变。  
   大写操作类似“查字典”，把字母 `'a'~'z'` 映射到 `'A'~'Z'`，Python 用 `word[0].upper()` 就可以做到。

3. **把所有单词连在一起，再在最前面加 `#`**  
   这一步相当于把一张张纸贴在一起，形成一条长长的标签。

4. **如果标签太长就截断**  
   题目要求 **标签的总长度（包括 `#`）不能超过 100**。  
   - 先得到完整标签 `full = "#" + processed_string`。  
   - 如果 `len(full) > 100`，只保留前 100 个字符：`full[:100]`。  
   这相当于把标签剪刀裁到规定的长度，只保留最前面的部分。

> **为什么这个方法一定对？**  
> - 拆词、大小写转换、拼接、截断都是**确定性的**操作，按照题目描述一步步执行，必然得到满足所有要求的结果。

#### 代码（Python）

```python
def generateTag(caption: str) -> str:
    # 1. 按空格拆词，自动去掉多余空格
    words = caption.split()

    # 2. 处理每个词
    processed = []
    for i, w in enumerate(words):
        if i == 0:                         # 第一个词保持原样
            processed.append(w)
        else:                              # 其余词首字母大写
            # w[0].upper() 把首字母变成大写，w[1:] 直接保留剩余部分
            processed.append(w[0].upper() + w[1:])

    # 3. 拼接成标签并加上 '#'
    tag = "#" + "".join(processed)

    # 4. 长度限制：若超过 100，就截取前 100 个字符
    if len(tag) > 100:
        tag = tag[:100]

    return tag
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  `n` 为 `caption` 的字符数。我们只遍历一次字符串（拆词、遍历单词、拼接），每一步都是线性操作。  
  大白话：如果字符数翻倍，程序跑的时间也大概会翻倍。

- **空间复杂度：** `O(n)`  
  需要额外的存储来保存拆开的单词和最终的标签，最坏情况和原字符串等长。

---

### 2. 最优解

#### 思路  

从暴力解出发，唯一的“慢”点其实是 **没有**——所有操作本身都是线性的。  
唯一需要注意的是 **一次性截断**：我们不必在每次拼接后都检查长度，只在最终得到完整标签后一次性裁剪即可，这样代码更简洁，性能也不受影响。

因此，**最优解** 与暴力解在算法上是同一个，只是把实现写得更紧凑、一步到位。

核心技巧：

- **字符串拼接**：使用 `join` 而不是 `+` 在循环里逐个累加，能避免 Python 中的 `O(n²)` 隐患（每次 `+` 都会创建新字符串）。
- **一次性截断**：`tag[:100]` 是 O(1) 的切片操作（底层只记录起止位置），不会复制整个字符串。

#### 代码（Python）

```python
def generateTag(caption: str) -> str:
    # 拆词
    words = caption.split()

    # 首词原样，后面的词首字母大写
    # 使用列表推导式 + join，避免循环中频繁的字符串拼接
    transformed = [words[0]] + [w[0].upper() + w[1:] for w in words[1:]]

    # 合并并加 '#'
    tag = "#" + "".join(transformed)

    # 超过 100 长度则截断
    return tag[:100]        # 切片本身会自动返回完整字符串（若不足 100 则不截断）
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  只遍历一次 `caption`，所有操作均为线性。

- **空间复杂度：** `O(n)`  
  需要存放拆开的单词以及最终标签。

与暴力解的对比：时间、空间都是同阶的 `O(n)`，但实现更简洁、常数因子更小。

---

## 心得

- **核心技巧**：**字符串的统一处理 + 一次性截断**。  
- **适用场景**：  
  1. 把句子转换为驼峰式（camelCase）或 PascalCase 的标签。  
  2. 对生成的文本做统一长度限制（如社交媒体的字符上限）。  
  3. 把多段文字拼接成单行摘要并截断。  
- **解题钥匙**：**先把任务拆成小步骤（拆词 → 变形 → 拼接 → 截断），每一步都可以单独验证**。

---

## 反思

- **第一反应**：把句子按空格拆开，然后逐词处理，再拼在一起，最后检查长度。  
- **最容易踩的坑**：  
  - **多余空格**：连续空格会产生空字符串，需要 `split()` 自动过滤。  
  - **长度截断位置**：一定是整体截断，而不是只在单词内部截断，否则会破坏已经完成的大小写转换。  
  - **首字母已经是大写**：直接 `upper()` 不会产生错误，保持原样即可。  
- **下次类似题**：**先确定“每一步的独立规则”，再把规则按顺序串起来；最后统一处理全局约束（如长度上限）**。这样思路清晰，代码也更不容易出错。