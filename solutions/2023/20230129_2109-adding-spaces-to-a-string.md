# #2109. 在字符串中添加空格 / Adding Spaces to a String

> 难度：中等 · 标签：Array、Two Pointers、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/adding-spaces-to-a-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s and a 0-indexed integer array spaces that describes the indices in the original string where spaces will be added. Each space should be inserted before the character at the given index.
Return the modified string after the spaces have been added.

**Examples**

**Example 1:**

```
Input: s = "LeetcodeHelpsMeLearn", spaces = [8,13,15]
Output: "Leetcode Helps Me Learn"
Explanation: 
The indices 8, 13, and 15 correspond to the underlined characters in "LeetcodeHelpsMeLearn".
We then place spaces before those characters.
```

**Example 2:**

```
Input: s = "icodeinpython", spaces = [1,5,7,9]
Output: "i code in py thon"
Explanation:
The indices 1, 5, 7, and 9 correspond to the underlined characters in "icodeinpython".
We then place spaces before those characters.
```

**Example 3:**

```
Input: s = "spacing", spaces = [0,1,2,3,4,5,6]
Output: " s p a c i n g"
Explanation:
We are also able to place spaces before the first character of the string.
```

**Constraints**

- 1 <= s.length <= 3 * 105
- s consists only of lowercase and uppercase English letters.
- 1 <= spaces.length <= 3 * 105
- 0 <= spaces[i] <= s.length - 1
- All the values of spaces are strictly increasing.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 **0** 开始的字符串 `s` 和一个下标从 **0** 开始的整数数组 `spaces`，该数组描述了在原始字符串中需要插入空格的位置索引。每个空格应当在给定索引对应的字符之前插入。  
返回在所有空格插入完成后的 **修改后字符串**（modified string）。

**示例 1**  
**输入**: `s = "LeetcodeHelpsMeLearn", spaces = [8,13,15]`  
**输出**: `"Leetcode Helps Me Learn"`  
**解释**:  
索引 8、13、15 对应于 `"LeetcodeHelpsMeLearn"` 中下划线标记的字符。我们在这些字符之前分别插入空格。

**示例 2**  
**输入**: `s = "icodeinpython", spaces = [1,5,7,9]`  
**输出**: `"i code in py thon"`  
**解释**:  
索引 1、5、7、9 对应于 `"icodeinpython"` 中下划线标记的字符。我们在这些字符之前分别插入空格。

**示例 3**  
**输入**: `s = "spacing", spaces = [0,1,2,3,4,5,6]`  
**输出**: `" s p a c i n g"`  
**解释**:  
我们也可以在字符串的第一个字符之前插入空格。

**约束条件**  
- `1 <= s.length <= 3 * 10^5`  
- `s` 仅由大小写英文字母组成。  
- `1 <= spaces.length <= 3 * 10^5`  
- `0 <= spaces[i] <= s.length - 1`  
- `spaces` 中的所有值严格递增。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把原字符串的每个字符都一个一个取出来，遇到需要在前面插入空格的位置就先把空格加进来**。  
- **数据结构**：我们只需要一个「可变」的字符串容器。Python 中 `list` 的 `append` 操作是 O(1) 的，把所有字符和空格先放进列表，最后 `''.join(list)` 得到结果。可以把 `list` 想象成 **一本空白笔记本**，每写一个字符或空格就翻到下一页，写完后把所有页拼在一起就是最终的字符串。  
- **正确性**：题目保证 `spaces` 已经是严格递增的（从小到大），所以只要我们按照原字符串的顺序遍历，并且用一个指针 `p` 记录下一个要插入空格的下标 `spaces[p]`，当遍历到的下标 `i` 与 `spaces[p]` 相等时，就先往结果里放一个空格，再放字符 `s[i]`，随后把 `p` 往后移动一位。这样每个需要插入空格的位置都恰好插入一次，其他位置保持不变，最终得到的字符串必然符合要求。  

#### 代码（Python）

```python
def addSpaces(s: str, spaces: list[int]) -> str:
    # 用 list 收集字符，最后一次性 join 成字符串，效率高
    res = []                     # 结果容器，相当于一本空白笔记本
    p = 0                        # 指向 spaces 中下一个要插入空格的下标
    n = len(spaces)              # spaces 的长度，方便后面判断是否已用完

    for i, ch in enumerate(s):   # 依次遍历原字符串的每个字符，i 是字符下标
        # 如果当前下标正好是需要插入空格的位置，就先放一个空格
        if p < n and i == spaces[p]:
            res.append(' ')      # 插入空格
            p += 1                # 移动指针，指向下一个空格位置

        res.append(ch)           # 再放原字符

    return ''.join(res)           # 把列表拼成最终字符串
```

#### 复杂度  

- **时间复杂度**：`O(|s| + |spaces|)`  
  - 我们只遍历了一遍字符串 `s`（长度记作 `|s|`）和一次 `spaces`（长度记作 `|spaces|`），每一步的操作都是 O(1)。  
  - 用大白话说，就是如果字符串有 1000 个字符，空格数组有 200 个位置，最多做 1200 次“看一眼、写进去”的事，跟字符和空格的总数成正比。  

- **空间复杂度**：`O(|s| + |spaces|)`（输出空间）  
  - 额外的辅助空间只有 `res` 列表，最终会存放和原字符串等长（再加上空格）的字符。  
  - 这算是**必要的**空间，因为答案本身就比原字符串长。若只算**额外**的临时空间（不计输出），则是 `O(1)`，因为我们只用了常数个变量 `p、i、ch`。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈其实不在遍历本身**——我们已经只遍历了一遍字符串和一次 `spaces`，每一步都是常数时间。  
唯一可以改进的地方是**避免使用列表再 `join` 的额外拷贝**，直接在原字符串上构造新字符串。但在 Python 中，字符串是不可变的，逐字符拼接会导致 O(n²) 的时间开销（每次拼接都会拷贝已有字符），所以 `list` + `join` 已经是最优的实现方式。  

因此，这里把 **最优解**定义为 **使用双指针（遍历字符串 + 遍历 spaces）并利用列表一次性拼接**，它已经是时间上最好的 O(|s|+|spaces|) 方案。下面再用稍微不同的写法展示，同样的思路，只是把 `spaces` 转成集合，利用 O(1) 的“查找”来决定是否插入空格。  

> **为什么集合也能做到 O(1) 查找？**  
> 把 `spaces` 看成一本 **字典**，每个需要插入空格的位置都是词条的“键”，查询时只需要一次“查页码”，时间恒定，不会随 `spaces` 长度增长。  

#### 代码（Python）

```python
def addSpaces_opt(s: str, spaces: list[int]) -> str:
    space_set = set(spaces)          # 把数组变成集合，查找是否需要空格是 O(1)
    res = []                         # 结果列表

    for i, ch in enumerate(s):
        if i in space_set:           # 如果当前下标在集合里，就先放空格
            res.append(' ')
        res.append(ch)               # 再放原字符

    return ''.join(res)
```

> **提示**：本题的 `spaces` 已经是有序的，使用集合会多占用一点额外空间（约 O(|spaces|)），但查找更直接；如果想省空间且保持 O(|s|+|spaces|) 的时间，仍然推荐前面的双指针写法。

#### 复杂度  

- **时间复杂度**：`O(|s| + |spaces|)`  
  - 仍然只遍历一次字符串，集合的查找是常数时间。  
  - 与暴力解相比没有多余的循环，仍是线性时间。  

- **空间复杂度**：`O(|s| + |spaces|)`（输出空间）  
  - 额外的集合占用 `O(|spaces|)`，列表占用 `O(|s|)`（加空格后）。  
  - 若仅计输出，则同样是 `O(|s| + |spaces|)`。  

---

## 心得

- **核心技巧**：**双指针 + 列表/集合 + 一次性 `join`**。  
  - 双指针帮助我们在遍历有序的 `spaces` 时只前进一次，避免每次都在数组里搜索。  
  - 使用 `list.append` 再 `''.join'` 能把“逐字符拼接”变成 O(1) 的追加操作，极大提升效率。  

- **适用的题型**  
  1. **在有序位置插入字符或标记**（如在字符串中插入逗号、换行符等）。  
  2. **根据下标数组进行分段或合并**（如把数组分割成若干段，或在特定下标处做标记）。  
  3. **需要一次遍历完成“同步”两份有序信息**（如合并两个有序列表、两指针扫描等）。  

- **一句话总结解题钥匙**：**利用有序特性，用指针一次遍历同步处理，两端都只前进不回头**。

---

## 反思

- **第一反应**：看到“在若干下标前插入空格”，立刻想到“遍历字符串，遇到对应下标就加空格”。这就是最直接的暴力思路。  

- **最容易踩的坑**  
  - **下标从 0 开始**：要记得空格是 **在字符之前**，而不是之后。  
  - **首字符前插空格**：如果 `spaces[0] == 0`，需要在最开始就先放空格。  
  - **重复或越界**：题目保证 `spaces` 严格递增且在合法范围内，但在手写代码时仍要检查 `p < len(spaces)` 防止越界。  
  - **字符串拼接的性能**：直接用 `+` 拼接会导致 O(n²) 的时间，要改用列表 `append` + `join`。  

- **下次遇到同类题的第一步**：  
  1. **确认输入是否有序**（如果有序，就可以用双指针）。  
  2. **确定“插入点”是字符前还是字符后**，并在遍历时提前/随后处理。  
  3. **选用 O(1) 的追加结构**（列表或集合），避免逐字符拼接的低效实现。