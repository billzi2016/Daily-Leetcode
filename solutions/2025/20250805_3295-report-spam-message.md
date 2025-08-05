# #3295. 报告垃圾消息 / Report Spam Message

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/report-spam-message/)

---

## 题目（英文原版）

**Description**

You are given an array of strings message and an array of strings bannedWords.
An array of words is considered spam if there are at least two words in it that exactly match any word in bannedWords.
Return true if the array message is spam, and false otherwise.

**Examples**

**Example 1:**

```
Input: message = ["hello","world","leetcode"], bannedWords = ["world","hello"]
Output: true
Explanation:
The words "hello" and "world" from the message array both appear in the bannedWords array.
```

**Example 2:**

```
Input: message = ["hello","programming","fun"], bannedWords = ["world","programming","leetcode"]
Output: false
Explanation:
Only one word from the message array ( "programming" ) appears in the bannedWords array.
```

**Constraints**

- 1 <= message.length, bannedWords.length <= 105
- 1 <= message[i].length, bannedWords[i].length <= 15
- message[i] and bannedWords[i] consist only of lowercase English letters.

---

## 题目（中文翻译）

你将得到一个字符串数组 `message` 和一个字符串数组 `bannedWords`。  
如果一个词语数组（array of words）中至少有两个词恰好匹配 `bannedWords` 中的任意词，则该数组被视为垃圾信息（spam）。  
返回 `true` 表示 `message` 是垃圾信息，返回 `false` 表示不是。

**示例 1**  
**输入**: `message = ["hello","world","leetcode"]`, `bannedWords = ["world","hello"]`  
**输出**: `true`  
**解释**:  
`message` 数组中的单词 `"hello"` 和 `"world"` 都出现在 `bannedWords` 数组中。

**示例 2**  
**输入**: `message = ["hello","programming","fun"]`, `bannedWords = ["world","programming","leetcode"]`  
**输出**: `false`  
**解释**:  
只有 `message` 数组中的单词 `"programming"` 出现在 `bannedWords` 数组中，未达到两个的条件。

**约束条件**  
- `1 <= message.length, bannedWords.length <= 10^5`  
- `1 <= message[i].length, bannedWords[i].length <= 15`  
- `message[i]` 和 `bannedWords[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **message** 和 **bannedWords** 两个列表逐个比较：  
- 对 **message** 中的每个单词，遍历 **bannedWords**，看它们是否相等。  
- 只要找到了两个相同的单词，就可以返回 `True`，否则遍历结束返回 `False`。  

这里用到的唯一数据结构是 **列表**（array），类似于我们平时在纸上写的单词表，一行一行地查找。  
这种方法之所以 **正确**，是因为我们把所有可能的配对都检查了一遍，保证不漏掉任何一次匹配。

**时间复杂度** 用大白话解释：  
- 假设 **message** 长度为 `n`，**bannedWords** 长度为 `m`。  
- 每个 `message` 的单词都要和 `m` 个 banned 单词比较，最坏情况要比较 `n × m` 次。  
- 用 **O(n·m)** 表示，就是“数量级是 n 乘以 m”，如果 n、m 都是 10⁵，运算次数会是 10¹⁰，几乎不可能在几秒内跑完。

**空间复杂度**：只用了原来的两个列表，没有额外的大结构，用 **O(1)**（常数级）空间。

#### 代码（Python）

```python
def is_spam_brute(message, bannedWords):
    """
    暴力解：两层循环逐个比较
    :param message: List[str]，待检测的消息数组
    :param bannedWords: List[str]，禁用词数组
    :return: bool，是否为 Spam
    """
    count = 0                     # 记录已经匹配到的禁用词个数
    for w in message:             # 外层遍历消息中的每个单词
        for b in bannedWords:     # 内层遍历所有禁用词
            if w == b:            # 完全相等则算一次匹配
                count += 1
                if count >= 2:    # 找到两次或以上即可直接返回 True
                    return True
    return False                  # 循环结束仍未达到两次匹配
```

#### 复杂度

- **时间复杂度**：`O(n·m)` — 需要把每个消息单词和所有禁用词逐个比较，数量级是两者的乘积。
- **空间复杂度**：`O(1)` — 只用了计数器 `count`，不依赖额外随输入规模增长的存储。

---

### 2. 最优解

#### 思路  
从暴力解可以看到 **瓶颈** 在于每次都要遍历完整个 `bannedWords`，导致 `n·m` 的时间。  
如果我们能把“查找是否在 bannedWords 中”这一步 **加速**，就可以把整体时间降下来。  

**哈希表（Hash Set）** 正好可以把“是否出现过”这类查询的时间从线性 `O(m)` 降到常数 `O(1)`。  
可以把 `bannedWords` 先放进一个集合（相当于把它们装进一本“字典”，查询词义只需要翻一页），随后遍历 `message`，每遇到一个单词就去集合里“查字典”。  

具体步骤：

1. **构建集合** `ban_set = set(bannedWords)`。  
   - 集合内部会把每个单词的 **哈希值** 作为索引，查询时直接定位到对应位置，几乎不需要遍历。  
2. 初始化计数器 `cnt = 0`。  
3. **遍历** `message`，如果当前单词在 `ban_set` 中，`cnt += 1`。  
4. 当 `cnt` 达到 2 时立刻返回 `True`（提前结束），遍历完仍未达到 2 则返回 `False`。  

这就是 **单遍**（一次遍历）加 **哈希集合** 的典型做法，时间从 `O(n·m)` 降到 `O(n + m)`，空间多用了 `O(m)` 用来存放集合。

> **类比**：想象你有一本词典，里面列出所有禁止词的页码。如果要判断一个单词是否在词典里，你只要翻到对应的页码（哈希），而不是从头到尾逐页查找（线性遍历）。

#### 代码（Python）

```python
def is_spam_optimal(message, bannedWords):
    """
    最优解：使用哈希集合实现 O(n+m) 时间
    :param message: List[str]
    :param bannedWords: List[str]
    :return: bool
    """
    # 把所有禁止词放进集合，等价于“快速查字典”
    ban_set = set(bannedWords)   # O(m) 时间，O(m) 额外空间

    cnt = 0                      # 已匹配的禁止词数量
    for w in message:           # O(n) 遍历每个消息单词
        if w in ban_set:        # O(1) 哈希查询：单词是否在集合里
            cnt += 1
            if cnt >= 2:        # 找到两次即可提前返回
                return True
    return False                 # 遍历结束仍未达到两次
```

#### 复杂度

- **时间复杂度**：`O(n + m)` —  
  - `O(m)` 用来把 `bannedWords` 放进集合（一次遍历），  
  - `O(n)` 用来遍历 `message` 并做常数时间的查找。  
  与暴力解的 `O(n·m)` 相比，规模大时几乎快 **指数级**（比如 10⁵ × 10⁵ → 2×10⁵）。
- **空间复杂度**：`O(m)` — 需要额外存放 `bannedWords` 的集合，大小随 `bannedWords` 长度线性增长。

---

## 心得

- **核心技巧**：利用 **哈希集合**（Hash Set）实现 **常数时间查找**，把两层遍历降为一次遍历。  
- **适用的题型**：  
  1. 判断两个数组是否有交集（如 “Intersection of Two Arrays”）。  
  2. 统计数组中出现次数大于等于 k 的元素（如 “Majority Element” 变形）。  
  3. 检查字符串中是否包含任意敏感词（如 “Censoring Bad Words”）。  
- **一句话总结**：**“把需要频繁‘是否在集合里’的查询，用哈希集合一次搞定。”**

---

## 反思

- **第一反应**：直接写双层循环，想到要逐个比较。  
- **最容易踩的坑**：  
  - **提前返回**：忘记在计数达到 2 时立刻返回，导致仍然遍历完所有元素，失去提前结束的优势。  
  - **集合的构造**：若把 `message` 放进集合再遍历 `bannedWords`，会导致计数方式错误（会漏掉同一个禁用词出现多次的情况）。  
  - **边界情况**：当 `message` 或 `bannedWords` 只有一个元素时，代码仍需正常工作，不能因为数组太小而产生 IndexError。  
- **下次第一步**：先思考“是否存在需要快速查询的子问题”，如果有，就立刻考虑 **哈希表/集合** 来把查询从线性降到常数。这样往往能把大多数 **O(n·m)** 的暴力思路直接优化到 **O(n+m)**。