# #1023. **驼峰式匹配** / Camelcase Matching

> 难度：中等 · 标签：Array、Two Pointers、String、Trie、String Matching · [LeetCode 链接](https://leetcode.com/problems/camelcase-matching/)

---

## 题目（英文原版）

**Description**

Given an array of strings queries and a string pattern, return a boolean array answer where answer[i] is true if queries[i] matches pattern, and false otherwise.
A query word queries[i] matches pattern if you can insert lowercase English letters into the pattern so that it equals the query. You may insert a character at any position in pattern or you may choose not to insert any characters at all.

**Examples**

**Example 1:**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FB"
Output: [true,false,true,true,false]
Explanation: "FooBar" can be generated like this "F" + "oo" + "B" + "ar".
"FootBall" can be generated like this "F" + "oot" + "B" + "all".
"FrameBuffer" can be generated like this "F" + "rame" + "B" + "uffer".
```

**Example 2:**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBa"
Output: [true,false,true,false,false]
Explanation: "FooBar" can be generated like this "Fo" + "o" + "Ba" + "r".
"FootBall" can be generated like this "Fo" + "ot" + "Ba" + "ll".
```

**Example 3:**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBaT"
Output: [false,true,false,false,false]
Explanation: "FooBarTest" can be generated like this "Fo" + "o" + "Ba" + "r" + "T" + "est".
```

**Constraints**

- 1 <= pattern.length, queries.length <= 100
- 1 <= queries[i].length <= 100
- queries[i] and pattern consist of English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `queries` 和一个字符串 `pattern`，返回一个布尔数组 `answer`，其中 `answer[i]` 为 `true` 当且仅当 `queries[i]` 能匹配 `pattern`，否则为 `false`。

若可以在 `pattern` 的任意位置插入小写英文字母（lowercase English letters）使其等于查询单词 `queries[i]`，则 `queries[i]` 匹配 `pattern`。插入字符的数量可以为零，也可以在多个位置插入。

---

### 示例

**示例 1**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FB"
Output: [true,false,true,true,false]
Explanation: 
"FooBar" 可以这样生成： "F" + "oo" + "B" + "ar"。  
"FootBall" 可以这样生成： "F" + "oot" + "B" + "all"。  
"FrameBuffer" 可以这样生成： "F" + "rame" + "B" + "uffer"。
```

**示例 2**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBa"
Output: [true,false,true,false,false]
Explanation: 
"FooBar" 可以这样生成： "Fo" + "o" + "Ba" + "r"。  
"FootBall" 可以这样生成： "Fo" + "ot" + "Ba" + "ll"。
```

**示例 3**

```
Input: queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FoBaT"
Output: [false,true,false,false,false]
Explanation: 
"FooBarTest" 可以这样生成： "Fo" + "o" + "Ba" + "r" + "T" + "est"。
```

---

### 约束条件

- `1 <= pattern.length, queries.length <= 100`
- `1 <= queries[i].length <= 100`
- `queries[i]` 与 `pattern` 只包含英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把匹配过程当成一次“选择”**：  
- 读取 `query` 的每个字符 `c`，看它能不能和 `pattern` 当前指向的字符配对。  
- 如果 `c` 与 `pattern` 的字符相同，就把两者都往后走一步（相当于“使用”这个字符）。  
- 如果 `c` 是小写且 **不** 与 `pattern` 的字符相同，我们可以把它“插入”到 `pattern` 中，也就是说直接跳过 `c`，只把 `query` 往后走一步。  
- 关键是：**大写字母只能用来匹配 `pattern`，不能随便跳过**。如果在 `query` 中遇到大写字母却找不到对应的 `pattern` 字母，就直接判为不匹配。

把上面的规则直接写成递归，就得到一个**暴力搜索**的解法：

```
match(i, j)  表示 query[i:] 能否匹配 pattern[j:]
```

- 当 `i` 到达 `query` 末尾且 `j` 到达 `pattern` 末尾时，返回 `True`（全部匹配完了）。
- 当 `i` 到达 `query` 末尾但 `j` 还没到时，返回 `False`（还有未匹配的 pattern）。
- 当 `query[i] == pattern[j]` 时，必须把两者都向后走一步：`match(i+1, j+1)`。
- 当 `query[i]` 是小写且不等于 `pattern[j]` 时，可以“插入”它，继续匹配 `query[i+1:]` 与 `pattern[j:]`：`match(i+1, j)`。
- 其余情况（大写字母不匹配）直接返回 `False`。

因为每一步最多会产生 **两条递归分支**，最坏情况下会遍历所有可能的子序列，时间会呈指数级增长（类似“找子集”的复杂度），所以这是一种**暴力**解法。

> **类比**：把 `pattern` 看成一本只有大写字母的“手册”，`query` 是一本“加了很多小写装饰的手册”。我们要检查能否把装饰（小写）去掉后，得到的手册正好是 `pattern`。暴力解法相当于把所有可能的去装饰方式都枚举一遍。

#### 代码（Python）

```python
def camel_match_bruteforce(queries, pattern):
    """
    暴力递归解法（不使用记忆化），时间会指数级增长。
    """
    def match(word, i, pat, j):
        # i, j 分别是 word 和 pat 的指针
        # 当两个指针都到达字符串末尾，说明完全匹配
        if i == len(word) and j == len(pat):
            return True
        # word 用完了但 pat 还有剩余，匹配失败
        if i == len(word):
            return False

        # 当前字符相等，必须一起向后走
        if j < len(pat) and word[i] == pat[j]:
            return match(word, i + 1, pat, j + 1)

        # word[i] 是小写字母，且不需要匹配 pattern 中的字符
        if word[i].islower():
            # “插入”这个小写字母，相当于直接跳过它
            return match(word, i + 1, pat, j)

        # 其余情况：大写字母不匹配，直接返回 False
        return False

    return [match(q, 0, pattern, 0) for q in queries]
```

#### 复杂度

- **时间复杂度**：`O(2^{L})`（指数级），其中 `L` 为 `query` 的长度。因为每遇到一个可以“跳过”的小写字母，就会产生两条递归分支。用大白话说，就是“最坏情况下要尝试所有可能的删除组合”，会非常慢。
- **空间复杂度**：`O(L)`，递归栈的深度最多等于 `query` 的长度。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于递归产生的分支**。其实我们不需要把所有可能都尝试一遍，只要**顺序地一次遍历 `query` 与 `pattern`**，就能判断是否匹配。因为：

- 小写字母可以随意“插入”，所以遇到小写且不匹配时，直接跳过它即可，不需要回溯。
- 大写字母必须严格对应 `pattern` 中的下一个字符，否则匹配失败。

这正好对应 **双指针**（Two Pointers）技巧：  
- `i` 指向 `query`，`j` 指向 `pattern`。  
- 当 `query[i]` 与 `pattern[j]` 相同（无论大小写），两指针都向前走。  
- 当 `query[i]` 是小写且不等于 `pattern[j]` 时，只移动 `i`（相当于把这个小写字母“插入”到 pattern 中）。  
- 其余情况（`query[i]` 为大写且不匹配）直接返回 `False`。  

遍历结束后，只要 `j` 已经走到 `pattern` 末尾，说明所有必须匹配的大写字母都找到了；如果还有未匹配的 `pattern`，则返回 `False`。

> **类比**：想象你在读一本混有装饰的小写字母的手册（`query`），手里还有一本只写大写字母的原稿（`pattern`）。你一边读 `query`，一边在原稿上找对应的大写字母。遇到装饰（小写）就直接略过，遇到不相符的大写就立刻知道这本手册不是原稿的“加装版”。整个过程只需要一次线性扫描。

#### 代码（Python）

```python
def camel_match_optimal(queries, pattern):
    """
    双指针线性扫描解法，时间复杂度 O(N * L)，其中
    N = len(queries)，L = 平均 query 长度（<=100），非常快。
    """
    def matches(word, pat):
        i = j = 0                     # i -> word, j -> pat
        while i < len(word):
            if j < len(pat) and word[i] == pat[j]:
                # 当前字符匹配，两个指针都前进
                i += 1
                j += 1
            elif word[i].islower():
                # 小写字母可以“插入”，只跳过 word 中的它
                i += 1
            else:
                # 大写字母不匹配，直接失败
                return False
        # 循环结束后，只有当 pat 也全部匹配完才算成功
        return j == len(pat)

    return [matches(q, pattern) for q in queries]
```

#### 复杂度

- **时间复杂度**：`O(N * L)`，其中 `N` 为 `queries` 的数量（≤100），`L` 为每个字符串的长度（≤100）。用大白话说，就是“每个查询只需要一次从头到尾的扫描”，所以最多 10,000 次字符比较，几乎是瞬间完成。
- **空间复杂度**：`O(1)`，只用了常数个指针变量，不会随输入规模增长。

与暴力解相比，时间从指数级降到了线性级，速度提升非常明显。

---

## 心得

- **核心技巧**：双指针（Two Pointers）在**顺序匹配**类问题中的强大威力。只要能把“可以跳过的字符”定义清楚，就能一次遍历完成判断。
- **适用题型**：
  1. **字母序列匹配**（如 “Is Subsequence”）  
  2. **带有可选字符的模式匹配**（如 “Wildcard Matching” 的简化版）  
  3. **字符串压缩/展开的验证**（如 “Valid Parentheses” 中的字符过滤）
- **一句话总结**：**大写字母必须逐一对应，小写字母随意跳过 → 用双指针一次线性扫描即可完成匹配**。

---

## 反思

- **第一反应**：看到“可以在 pattern 中插入小写字母”，立刻想到“递归穷举所有插入方式”。这会导致指数级的搜索。
- **最容易踩的坑**：
  - 忽略 **大写字母必须严格匹配**，导致把 `query` 中多余的大写字母误判为可跳过。  
  - 结束循环后忘记检查 `pattern` 是否全部匹配完（`j == len(pattern)`），会把 `"FB"` 匹配 `"FooBarTest"` 错误地判为 `True`。  
  - 边界条件：空字符串或全小写的 `query`，以及 `pattern` 全大写的情况，都要通过指针的边界检查。
- **下次遇到同类题**：第一步就**明确哪些字符是“必须匹配”，哪些是“可以跳过”，然后尝试 **双指针一次遍历**；如果仍然不确定，再考虑 DP 或回溯。