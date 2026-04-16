# #3597. **划分字符串** / Partition String 

> 难度：中等 · 标签：Hash Table、String、Trie、Simulation · [LeetCode 链接](https://leetcode.com/problems/partition-string/)

---

## 题目（英文原版）

**Description**

Given a string s, partition it into unique segments according to the following procedure:
Return an array of strings segments, where segments[i] is the ith segment created.

**Examples**

**Example 1:**

```
Input: s = "abbccccd"
Output: ["a","b","bc","c","cc","d"]
Explanation:
Hence, the final output is ["a", "b", "bc", "c", "cc", "d"] .
```

**Example 2:**

```
Input: s = "aaaa"
Output: ["a","aa"]
Explanation:
Hence, the final output is ["a", "aa"] .
```

**Constraints**

- 1 <= s.length <= 105
- s contains only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，按照以下过程将其划分为唯一的段（segment）：

返回一个字符串数组 `segments`，其中 `segments[i]` 为第 `i` 个创建的段。

---

### 示例 1

**输入**  
` s = "abbccccd" `  

**输出**  
`["a","b","bc","c","cc","d"]`  

**解释**  
因此，最终输出为 `["a", "b", "bc", "c", "cc", "d"]` 。

---

### 示例 2

**输入**  
` s = "aaaa" `  

**输出**  
`["a","aa"]`  

**解释**  
因此，最终输出为 `["a", "aa"]` 。

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都枚举出来**，然后挑出满足“每个子串内部字符不重复”的那一组。  
可以把字符串看成一串珠子，每一颗珠子上写着一个字母。我们要把这些珠子分成若干段，使得同一段里没有两颗写着相同字母的珠子。

暴力做法：

1. 用两层循环枚举所有切分点 `(i, j)`，`i` 为当前段的左边界，`j` 为右边界（不含 `j`）。  
2. 对每个 `[i, j)` 检查这段字符是否全部不同（可以用一个临时的哈希表 `set` 来判断）。  
3. 如果这段合法，就继续递归/动态规划去处理后面的字符；否则直接丢弃。  

这样会遍历 **指数级** 的切分方案，但思路最清晰，适合作为第一步的“穷举”。

#### 代码（Python）

```python
def partition_bruteforce(s: str):
    """
    暴力递归枚举所有合法的切分方式，返回其中一种（题目只要求返回切分结果）。
    """
    n = len(s)

    def helper(start):
        # 当已经走到字符串末尾，返回空列表表示成功切分完毕
        if start == n:
            return []

        # 从 start 开始尝试所有可能的右边界
        for end in range(start + 1, n + 1):
            segment = s[start:end]

            # 检查 segment 是否所有字符唯一
            if len(set(segment)) == len(segment):          # O(end-start) 的检查
                # 递归处理剩余部分
                rest = helper(end)
                if rest is not None:                      # 找到合法切分
                    return [segment] + rest

        # 没有任何合法的切分方式，返回 None 表示失败
        return None

    return helper(0)
```

> 关键行解释  
> - `len(set(segment)) == len(segment)`：把当前子串放进集合（哈希表），如果集合的大小等于子串长度，说明没有重复字符。  
> - `for end in range(start + 1, n + 1)`：枚举所有可能的切分点。  
> - 递归 `helper(end)`：把已经确定好的子串后面的部分继续切分。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）  
  每个位置都有“切或不切”两种选择，最坏情况下会遍历所有可能的切分方案。  
- **空间复杂度**：`O(n)`  
  递归深度最多 `n`，加上返回的切分列表共占用线性空间。

> **大白话**：  
> 想象把一根绳子上的每个结点都可能是“剪刀”出现的地方，暴力解相当于把所有可能的剪刀位置全部尝试一次，数量会非常庞大，像把所有可能的二进制数列列出来一样。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查同一个子串是否有重复字符**，以及**对所有切分点的穷举**。  
实际上，只要我们**从左到右一次遍历**，并用一个哈希表记录“当前子串已经出现过的字符”，就能即时决定何时必须结束当前子串：

1. **维护一个集合 `cur`**，存放当前子串已经出现的字符。  
2. 逐字符遍历 `s`：  
   - 如果当前字符 `c` **不在 `cur`**，说明把它加入当前子串仍然满足“字符唯一”，于是 `cur.add(c)`，继续往后走。  
   - 如果 `c` **已经在 `cur`**，则**必须在这里结束当前子串**（因为继续往下会出现重复），把已收集的子串加入答案列表 `segments`，**并重新开启一个新子串**，此时 `cur` 只保留 `c`（新子串的第一个字符）。  
3. 循环结束后，别忘了把最后一个正在构建的子串也加入答案。

这就是 **一次遍历 O(n)** 的贪心/模拟方案。  
这里用到的 **哈希表（Python 的 `set`）** 可以类比成“字典”，`key` 是字符，`value` 只是一张“该字符已经出现过”的标记。

#### 代码（Python）

```python
def partition_optimal(s: str):
    """
    贪心模拟：一次遍历，把字符唯一的子串依次切下来。
    返回所有子串组成的列表。
    """
    segments = []          # 用来保存最终的切分结果
    cur_set = set()        # 当前子串已经出现的字符集合
    start = 0              # 当前子串的起始下标

    for i, ch in enumerate(s):
        if ch in cur_set:                     # 遇到重复字符，需要结束当前子串
            # 把[start, i) 这段加入结果
            segments.append(s[start:i])
            # 重新开始新子串，重置集合，只保留当前字符
            cur_set.clear()
            cur_set.add(ch)
            start = i                         # 新子串的起点移动到当前字符
        else:
            cur_set.add(ch)                    # 继续往后收集字符

    # 循环结束后，剩余的最后一个子串（如果有）加入答案
    segments.append(s[start:])

    return segments
```

> 关键行解释  
> - `if ch in cur_set:`：判断当前字符是否已经在当前子串出现过。  
> - `segments.append(s[start:i])`：把不包含当前重复字符的子串切下来。  
> - `cur_set.clear(); cur_set.add(ch)`：新子串从当前字符重新开始。  
> - 循环结束后 `segments.append(s[start:])`：把最后剩余的子串加入答案。

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个字符只会被访问一次，集合的查找/插入都是 **摊销 O(1)**，所以整体线性。  
- **空间复杂度**：`O(k)`，`k` 为当前子串的长度，最坏情况下等于 `O(n)`（整条字符串全都是不重复字符）。  
  额外的答案列表 `segments` 也需要 `O(n)` 的存储，因为最终要把所有字符全部返回。

> **对比暴力**：  
> 暴力要把每一段都重新检查是否有重复，导致指数级时间；而最优解只用一个集合“记住”已经出现的字符，一次遍历即可决定切点，快得多。

---

## 心得

- **核心技巧**：**贪心 + 哈希集合**，在遍历过程中实时判断是否出现重复，从而决定切分位置。  
- **适用场景**：  
  1. “把字符串切成字符唯一的子串”——如本题、LeetCode 2405 “Partition String”。  
  2. “在序列中找最长无重复子段”——滑动窗口问题（LeetCode 3 “Longest Substring Without Repeating Characters”）。  
  3. “在数组/字符串中检测窗口内是否出现重复元素”——常用的 **滑动窗口 + 哈希表** 模式。  
- **一句话总结**：**只要能在一次遍历中用集合快速判断“已出现”，就能把“重复”转化为切分点，实现线性时间的最优解。**

---

## 反思

- **第一反应**：看到“唯一段”这几个字，我立刻想到“集合去重”。于是想到了用 `set` 来记录已经出现的字符。  
- **最容易踩的坑**：  
  - **忘记把最后一个子串加入答案**（循环结束时集合里还有字符）。  
  - **误把 `set` 清空后直接继续**，导致当前字符被遗漏；正确做法是在清空后把当前字符重新加入集合并更新起始下标。  
  - **边界条件**：字符串全是不同字符时只会产生一个子串；全是相同字符时会产生 `n`/`2`（视实现）个子串，需要验证。  
- **下次遇到同类题**：第一步先思考“是否可以在一次遍历中记录已经出现的元素”，如果可以，就立刻用 **哈希集合 + 贪心**（或滑动窗口）来决定切分或移动窗口。这样往往能直接得到 O(n) 的最优解。