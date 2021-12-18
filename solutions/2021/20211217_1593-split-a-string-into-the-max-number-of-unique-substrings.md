# #1593. 将字符串划分为最多唯一子串 / Split a String Into the Max Number of Unique Substrings

> 难度：中等 · 标签：Hash Table、String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/split-a-string-into-the-max-number-of-unique-substrings/)

---

## 题目（英文原版）

**Description**

Given a string s, return the maximum number of unique substrings that the given string can be split into.
You can split string s into any list of non-empty substrings, where the concatenation of the substrings forms the original string. However, you must split the substrings such that all of them are unique.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "ababccc"
Output: 5
Explanation: One way to split maximally is ['a', 'b', 'ab', 'c', 'cc']. Splitting like ['a', 'b', 'a', 'b', 'c', 'cc'] is not valid as you have 'a' and 'b' multiple times.
```

**Example 2:**

```
Input: s = "aba"
Output: 2
Explanation: One way to split maximally is ['a', 'ba'].
```

**Example 3:**

```
Input: s = "aa"
Output: 1
Explanation: It is impossible to split the string any further.
```

**Constraints**

- 1 <= s.length <= 16
- s contains only lower case English letters.

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `s`，返回可以将该字符串划分成的唯一子串（substring）的最大数量。  
你可以把字符串 `s` 划分为任意个 **非空** 子串的列表，使得这些子串的拼接（concatenation）仍然得到原始字符串。但必须保证划分得到的所有子串互不相同，即每个子串只能出现一次。  
子串是指字符串中连续的字符序列。

**示例**  

示例 1  
```
Input: s = "ababccc"
Output: 5
Explanation: 一种最大的划分方式是 ['a', 'b', 'ab', 'c', 'cc']。划分为 ['a', 'b', 'a', 'b', 'c', 'cc'] 不合法，因为出现了重复的 'a' 和 'b'。
```

示例 2  
```
Input: s = "aba"
Output: 2
Explanation: 一种最大的划分方式是 ['a', 'ba']。
```

示例 3  
```
Input: s = "aa"
Output: 1
Explanation: 已经无法再进一步划分字符串。
```

**约束条件**  
- `1 <= s.length <= 16`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串从左到右一点点切出来**，每切出一个子串就检查它之前是否出现过。如果没有出现过，就把它记下来（放进集合），继续往后切；如果出现过，就换一种切法。  
这正像我们在写笔记时，**把一段文字划分成若干段**，每段都必须是“新鲜的”，不能重复。

- **用到的数据结构**  
  - **集合（`set`）**：像一本字典，已经记住的子串就是字典里已有的词，查找是否已经出现的时间是 O(1)。  
  - **递归 + 回溯**：把“从当前位置往后切”这件事交给函数自己去完成，函数返回后再恢复现场继续尝试别的切法。

- **为什么这个方法一定能得到正确答案**  
  1. 我们枚举**所有可能的切分方式**（每个位置可以切成长度 1、2、…、剩余长度的子串）。  
  2. 对每一种切分方式，都检查是否满足“所有子串唯一”。  
  3. 在所有合法的切分方式中，记录子串个数的最大值。  
  因为没有漏掉任何一种切法，最大值自然就是答案。

- **时间/空间复杂度**  
  - **时间**：对每个位置我们都尝试所有可能的切割长度，最坏情况下会产生指数级的递归树。字符长度 ≤ 16，所有可能的切分方式总数是第 16 个**卡特兰数**的上界，大约是 `2^n`，所以时间复杂度可以记作 **O(2ⁿ)**。这里的 `2ⁿ` 只是一种形象的说法，实际运行很快，因为 n≤16。  
  - **空间**：递归深度最多是字符串长度 n，集合里最多存 n 个子串，所以 **O(n)** 的额外空间。

#### 代码（Python）

```python
def maxUniqueSplit(s: str) -> int:
    """
    暴力回溯：尝试所有切分方式，返回合法切分中子串数量的最大值。
    """
    n = len(s)
    used = set()          # 已经出现过的子串，类似“字典”
    best = 0              # 记录当前找到的最大子串数

    def backtrack(idx: int, cnt: int) -> None:
        """
        idx   : 当前要切割的起始下标
        cnt   : 已经切出多少个子串
        """
        nonlocal best
        # 已经遍历到字符串末尾，更新答案
        if idx == n:
            best = max(best, cnt)
            return

        # 剪枝：即使把剩下的每个字符都单独切成子串，得到的总数也不可能超过已有的 best
        # 剩余字符数 = n - idx
        if cnt + (n - idx) <= best:
            return

        # 从 idx 开始尝试所有可能的子串长度
        for end in range(idx + 1, n + 1):
            sub = s[idx:end]          # 当前子串 s[idx:end]
            if sub in used:           # 已经出现过，不能使用
                continue
            used.add(sub)             # 把新子串记入集合
            backtrack(end, cnt + 1)   # 递归处理后面的字符
            used.remove(sub)          # 回溯：撤销选择，尝试别的长度

    backtrack(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：O(2ⁿ)  
  - “指数级”意味着随着字符串长度的增加，可能的切分方式会快速增长。这里的 `n` 最多是 16，实际运行在毫秒级。

- **空间复杂度**：O(n)  
  - 递归栈最深为 `n`，集合最多保存 `n` 个不重复的子串。

---

### 2. 最优解

#### 思路  

对这道题目，**暴力回溯已经是最优的思路**，因为约束 `|s| ≤ 16` 本身就很小，无法再做出比指数级更快的通用算法。  
我们可以在暴力的基础上**加一点剪枝**，让搜索更快结束：

1. **剩余长度剪枝**  
   - 已经得到的子串数 `cnt` 加上剩余字符数 `(n‑idx)`（即把每个剩余字符单独切成子串的上限）如果仍然 ≤ 当前的 `best`，说明再继续搜索也不可能得到更好的答案，直接返回。

2. **提前结束**  
   - 当 `cnt` 已经等于 `n`（每个字符都单独成子串）时，直接返回，因为这是理论上的最大值。

这两点都只是在 **遍历所有切法的过程中提前停下**，不改变算法的本质，只是让“不可能更好”的分支不再浪费时间。

> **核心技巧**：**回溯 + 剪枝**。  
> 把“尝试所有可能”变成“尝试所有可能，但把明显不会产生更好答案的路径提前剪掉”。这在很多**组合搜索**类题目里都非常常见。

#### 代码（Python）

```python
def maxUniqueSplit(s: str) -> int:
    """
    回溯 + 剪枝：在暴力搜索的基础上提前剪掉不可能提升答案的分支。
    """
    n = len(s)
    used = set()
    best = 0

    def dfs(idx: int, cnt: int) -> None:
        nonlocal best
        # 到达字符串末尾，更新答案
        if idx == n:
            best = max(best, cnt)
            return

        # 剪枝：即使把剩下的每个字符都单独切，最多也只能得到 cnt + (n-idx) 个子串
        # 如果这已经不超过当前 best，后面的搜索没有意义
        if cnt + (n - idx) <= best:
            return

        # 枚举所有可能的子串
        for end in range(idx + 1, n + 1):
            sub = s[idx:end]
            if sub in used:
                continue
            used.add(sub)
            dfs(end, cnt + 1)
            used.remove(sub)

    dfs(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：仍然是 **O(2ⁿ)**，因为最坏情况下仍需遍历所有切分方式。  
  - 但由于剪枝，大多数分支会提前结束，实际运行时间往往明显快于纯暴力。

- **空间复杂度**：**O(n)**（递归栈 + 集合），和暴力解相同。

---

## 心得

- **核心技巧**：**回溯（Backtracking） + 哈希集合（Set）** 用来枚举所有可能的切分，并快速判断子串是否已经出现。  
- **适用的题型**  
  1. **分割字符串，使每段满足某种约束**（如 LeetCode 1400. 构造 K 个子数组的最大和）  
  2. **组合/排列搜索，需要“去重”**（如 LeetCode 90. 子集 II、491. 递增子序列）  
  3. **路径搜索类问题，需要记录已访问状态**（如 79. 单词搜索）

- **一句话总结解题钥匙**：**“尝试每一种切法，同时用集合记住已经出现的子串，遇到冲突就回头”**。

---

## 反思

- **第一反应**：看到“把字符串拆成若干不重复子串”，自然想到**回溯**——逐段尝试、记录、回溯。  
- **最容易踩的坑**  
  - **忘记把子串加入集合后再回溯时及时删除**，导致后面的分支误判子串已存在。  
  - **没有剪枝**，在长度为 16 的极端测试里仍能 AC，但运行时间会比预期慢很多。  
  - **边界条件**：空字符串（题目保证长度≥1）或全部相同字符时，答案只能是 1，需要保证代码能正确返回。  
- **下次遇到同类题**：**第一步先写出完整的回溯框架，再考虑用集合去重，最后再加入剪枝**，这样思路更清晰，代码更不易出错。