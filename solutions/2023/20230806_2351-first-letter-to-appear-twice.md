# #2351. First Letter to Appear Twice / First Letter to Appear Twice

> 难度：简单 · 标签：Hash Table、String、Bit Manipulation、Counting · [LeetCode 链接](https://leetcode.com/problems/first-letter-to-appear-twice/)

---

## 题目（英文原版）

**Description**

Given a string s consisting of lowercase English letters, return the first letter to appear twice.
Note:

**Examples**

**Example 1:**

```
Input: s = "abccbaacz"
Output: "c"
Explanation:
The letter 'a' appears on the indexes 0, 5 and 6.
The letter 'b' appears on the indexes 1 and 4.
The letter 'c' appears on the indexes 2, 3 and 7.
The letter 'z' appears on the index 8.
The letter 'c' is the first letter to appear twice, because out of all the letters the index of its second occurrence is the smallest.
```

**Example 2:**

```
Input: s = "abcdd"
Output: "d"
Explanation:
The only letter that appears twice is 'd' so we return 'd'.
```

**Constraints**

- 2 <= s.length <= 100
- s consists of lowercase English letters.
- s has at least one repeated letter.

---

## 题目（中文翻译）

**描述**  
给定一个只包含小写英文字母（lowercase English letters）的字符串（string）`s`，返回第一个出现两次的字母。

**示例 1**  
输入: `s = "abccbaacz"`  
输出: `"c"`  
**解释:**  
- 字母 `'a'` 出现在下标（index）0、5 和 6。  
- 字母 `'b'` 出现在下标 1 和 4。  
- 字母 `'c'` 出现在下标 2、3 和 7。  
- 字母 `'z'` 出现在下标 8。  
字母 `'c'` 是第一个出现两次的字母，因为在所有出现两次的字母中，它的第二次出现的下标最小。

**示例 2**  
输入: `s = "abcdd"`  
输出: `"d"`  
**解释:**  
唯一出现两次的字母是 `'d'`，因此返回 `'d'`。

**约束条件**  
- `2 <= s.length <= 100`  
- `s` 只由小写英文字母组成。  
- `s` 至少包含一个重复的字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个字符都和后面的字符逐个比较，看看哪一个第一次出现第二次。  
可以把字符串想象成一排座位，**暴力解** 就是让每个人（字符）去依次检查自己后面所有人的名字，找出第一个被重复叫到的名字。

- **使用的数据结构**：只需要原始的字符串本身和几个临时变量（比如记录答案的字符和它第二次出现的下标），不需要额外的容器。
- **正确性**：因为我们把所有可能的“先出现的第二次”都检查了一遍，最先找到的必然就是答案。
- **时间/空间复杂度**：  
  - 时间上要遍历 `i` 从 `0` 到 `n-1`，对每个 `i` 再遍历 `j` 从 `i+1` 到 `n-1`，于是总比较次数大约是 `1 + 2 + … + (n-1) = n·(n-1)/2`，用大写的 **O(n²)** 表示。这里的 `O(n²)` 可以理解为“随着字符串长度增长，工作量会像面积一样快地增长”。  
  - 空间上只用了常数个变量，**O(1)**（常数级）空间。

#### 代码（Python）

```python
def first_letter_bruteforce(s: str) -> str:
    n = len(s)
    # best_idx 用来记录当前已知的「第二次出现」的最小下标
    best_idx = n  # 初始设为一个不可能的最大值
    answer = ''   # 最终返回的字符

    # i 表示第一次出现的位置
    for i in range(n):
        # j 从 i+1 开始寻找同样的字符，代表第二次出现
        for j in range(i + 1, n):
            if s[i] == s[j]:               # 找到一次重复
                if j < best_idx:           # 看看这次的第二次出现是不是更早
                    best_idx = j
                    answer = s[i]
                break  # 已经找到了 i 对应的最早第二次出现，没必要再往后找

    return answer
```

#### 复杂度

- **时间复杂度**：**O(n²)** —— 需要两层循环，最坏情况下会比较约 `n²/2` 次。  
- **空间复杂度**：**O(1)** —— 只使用了固定数量的变量，不随输入大小增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，慢的地方在于**重复检查**：每个字符都要和后面的所有字符比较一次。  
实际上，我们只需要**记住已经见过的字符**，当再次遇到同一个字符时，就立刻知道它是第一次“第二次出现”。  

这可以用 **集合（set）** 来实现。集合在 Python 中底层是哈希表，类似于 **查字典**：  
- “词” 是字符本身（key），  
- “页码” 只是标记这个词是否已经出现过（value 只关心是否存在）。

遍历字符串一次：

1. 若当前字符不在集合中，就把它加入集合，表示“第一次看到”。  
2. 若当前字符已经在集合里，说明这是它的第二次出现，而且因为我们是从左到右顺序遍历的，这一定是**所有字符中最早的第二次出现**，直接返回即可。

这样只需要一次遍历，时间降到 **O(n)**，空间使用一个集合，最多存放 26 个小写字母，**O(1)**（常数空间）。

#### 代码（Python）

```python
def first_letter_optimal(s: str) -> str:
    seen = set()                     # 用集合记录已经出现过的字符
    for ch in s:                     # 从左到右逐个检查字符
        if ch in seen:               # 如果已经出现过，说明是第二次出现
            return ch                # 直接返回，答案找到了
        seen.add(ch)                 # 否则把它加入集合，标记为“已见”
    # 根据题目保证一定会有重复字符，这行理论上不会被执行
    raise ValueError("No repeated character found")
```

#### 复杂度

- **时间复杂度**：**O(n)** —— 只遍历一次字符串，集合的查找和插入在均摊意义下都是常数时间。相比暴力的 **O(n²)**，速度提升了一个量级。  
- **空间复杂度**：**O(1)** —— 最多只会存 26 个小写字母，和字符串长度无关，属于常数空间。

---

## 心得

- **核心技巧**：利用哈希集合（set）一次遍历实现“第一次出现第二次”的判定。  
- **适用的题型**：  
  1. “找出第一个重复字符”类（如 LeetCode 387）。  
  2. “判断字符串是否有重复字符”类（如判断是否为异位词）。  
  3. “最小子数组包含所有字符”类（需要快速判断字符是否已出现）。  
- **一句话总结**：**“遇到字符先查集合，已在则返回，否则加入集合”** 是解这类“首次重复”题目的钥匙。

## 反思

- **第一反应**：看到“第一个出现两次的字母”，自然会想到从左到右扫描，记录已经见过的字符。  
- **最容易踩的坑**：  
  - 忘记题目保证一定有重复字符，直接返回 `None` 会导致错误。  
  - 把集合误写成列表，导致查找变成 O(n) 又回到暴力的时间。  
  - 忽视字符集只有小写字母，误以为需要更大的空间。  
- **下次遇到同类题**：第一步就应该想到**“哈希/集合 + 单遍扫描”**，因为它能在 O(n) 时间内判断“是否已经出现”。