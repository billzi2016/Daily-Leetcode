# #2284. 单词数最多的发送者 / Sender With Largest Word Count

> 难度：中等 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/sender-with-largest-word-count/)

---

## 题目（英文原版）

**Description**

You have a chat log of n messages. You are given two string arrays messages and senders where messages[i] is a message sent by senders[i].
A message is list of words that are separated by a single space with no leading or trailing spaces. The word count of a sender is the total number of words sent by the sender. Note that a sender may send more than one message.
Return the sender with the largest word count. If there is more than one sender with the largest word count, return the one with the lexicographically largest name.
Note:

**Examples**

**Example 1:**

```
Input: messages = ["Hello userTwooo","Hi userThree","Wonderful day Alice","Nice day userThree"], senders = ["Alice","userTwo","userThree","Alice"]
Output: "Alice"
Explanation: Alice sends a total of 2 + 3 = 5 words.
userTwo sends a total of 2 words.
userThree sends a total of 3 words.
Since Alice has the largest word count, we return "Alice".
```

**Example 2:**

```
Input: messages = ["How is leetcode for everyone","Leetcode is useful for practice"], senders = ["Bob","Charlie"]
Output: "Charlie"
Explanation: Bob sends a total of 5 words.
Charlie sends a total of 5 words.
Since there is a tie for the largest word count, we return the sender with the lexicographically larger name, Charlie.
```

**Constraints**

- n == messages.length == senders.length
- 1 <= n <= 104
- 1 <= messages[i].length <= 100
- 1 <= senders[i].length <= 10
- messages[i] consists of uppercase and lowercase English letters and ' '.
- All the words in messages[i] are separated by a single space.
- messages[i] does not have leading or trailing spaces.
- senders[i] consists of uppercase and lowercase English letters only.

---

## 题目（中文翻译）

**题目描述**  
给定一段包含 `n` 条信息的聊天记录。你会得到两个字符串数组 `messages` 和 `senders`，其中 `messages[i]` 是由 `senders[i]` 发送的一条信息。  
一条信息是由单个空格分隔的单词序列，且不存在首尾空格。**发送者的单词数**（word count）是该发送者发送的所有信息中单词的总数。注意，同一个发送者可能会发送多条信息。  

返回单词数最多的发送者。如果出现多个发送者的单词数并列最多，返回字典序（lexicographically）最大的名字。

**示例**

示例 1  
```
Input: messages = ["Hello userTwooo","Hi userThree","Wonderful day Alice","Nice day userThree"], 
       senders = ["Alice","userTwo","userThree","Alice"]
Output: "Alice"
Explanation: Alice 总共发送了 2 + 3 = 5 个单词。  
userTwo 发送了 2 个单词。  
userThree 发送了 3 个单词。  
因为 Alice 的单词数最多，返回 "Alice"。
```

示例 2  
```
Input: messages = ["How is leetcode for everyone","Leetcode is useful for practice"], 
       senders = ["Bob","Charlie"]
Output: "Charlie"
Explanation: Bob 总共发送了 5 个单词。  
Charlie 也发送了 5 个单词。  
出现并列，返回字典序更大的名字，即 "Charlie"。
```

**约束条件**
- `n == messages.length == senders.length`
- `1 <= n <= 10^4`
- `1 <= messages[i].length <= 100`
- `1 <= senders[i].length <= 10`
- `messages[i]` 只包含大小写英文字母和空格 `' '`。
- `messages[i]` 中的所有单词均由单个空格分隔，且不存在首尾空格。
- `senders[i]` 只包含大小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次遇到一条消息，就把它拆成单词，统计单词数，然后把这个数加到对应发送者的总计里**。  
实现上可以：

1. 逐条遍历 `messages`（相当于把聊天记录从头到尾翻一遍）。
2. 对当前的 `messages[i]`，用 `split(' ')` 把句子切成单词列表，列表的长度就是该消息的单词数。  
   - 这里的 `split` 就像把一句话的每个词“摘下来”，把它们装进一个小盒子，盒子里有多少词，答案就出来了。
3. 用一个 **哈希表**（在 Python 中用 `dict`）记录每个发送者累计的单词数。  
   - 哈希表可以类比为一本**查字典**：词（key）是发送者的名字，页码（value）是该发送者已经说过的单词总数。查找、插入、更新都在 **常数时间**（≈ O(1)）完成。
4. 遍历完所有消息后，再遍历哈希表一次，找到 **单词数最大的发送者**；如果出现相同的最大值，则比较名字的字典序（lexicographically），取更大的那个。

**为什么这个方法一定能得到正确答案**  
因为我们对每一条消息都 **准确地统计了单词数**，并且 **把它完整地累加到对应的发送者**。最终的累计数正好等于题目定义的“发送者的单词总数”。再挑选最大值（并在平局时按字典序比较）自然得到答案。

**时间/空间复杂度的大白话**  
- **时间复杂度**：  
  - 第一步遍历所有 `n` 条消息，**每条消息**我们要把字符串切成单词，最坏情况（每条消息长度 100）切一次需要 O(L)（L 为该条消息长度），整体是 O(∑L) ≈ O(n·100) → **O(n)**。  
  - 第二步遍历哈希表，哈希表里最多有 `n` 个不同的发送者，复杂度也是 O(n)。  
  - 所以总时间是 **O(n)**，线性增长，和消息条数成正比。  
- **空间复杂度**：  
  - 需要一个哈希表来保存每个发送者的累计单词数，最坏情况每条消息的发送者都不相同，哈希表会有 `n` 条记录。  
  - 因此空间是 **O(n)**（额外的存储随输入规模线性增长）。

> **注意**：虽然这里的实现已经是线性时间，但如果把 “统计单词数” 这一步写成 **每次都遍历整个字符串并计数空格**，仍然是 O(L)；如果把它写成 **对每个发送者都重新遍历所有消息**（即两层循环），时间会升到 O(n²)，这就是下面「暴力」写法的示例。

#### 代码（Python）

```python
from typing import List

def countWords(message: str) -> int:
    """
    把一句话切成单词，返回单词数。
    split(' ') 会把每个空格分开的子串放进列表，列表长度即为单词数。
    """
    # 这里直接使用 split，省去手动遍历字符计数空格的过程
    return len(message.split(' '))

def largestWordCount_bruteforce(messages: List[str], senders: List[str]) -> str:
    """
    暴力实现：对每个发送者，都遍历所有消息统计单词数。
    时间复杂度 O(n²)（两层循环），空间 O(1)（不使用额外哈希表）。
    """
    n = len(messages)
    max_sender = ""
    max_cnt = -1

    # 对每个可能的发送者（这里直接遍历 senders 列表，可能会重复统计同一个人多次）
    for i in range(n):
        sender_i = senders[i]

        # 统计该发送者的总单词数，需要遍历所有消息
        total = 0
        for j in range(n):
            if senders[j] == sender_i:
                total += countWords(messages[j])

        # 更新答案：先比较单词数，若相同再比较字典序
        if total > max_cnt or (total == max_cnt and sender_i > max_sender):
            max_cnt = total
            max_sender = sender_i

    return max_sender
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 两层循环：外层遍历 `n` 条消息，内层又遍历 `n` 条消息统计同一发送者的单词数。  
  - 用大白话说，就是 **“每条消息都要看 `n` 次”**，当 `n` 增大时，耗时会呈二次方增长，明显慢。

- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了常数个额外变量 `max_sender、max_cnt、total`，没有额外的数据结构随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **慢点** 在于：  
- 对同一个发送者，我们 **重复遍历所有消息**，导致二次循环。  
- 实际上，每条消息只需要 **统计一次**，然后把结果直接加到对应发送者的累计里即可。

**优化的关键** 是使用 **哈希表（字典）** 来**一次遍历**完成所有统计：

1. 初始化空字典 `cnt = {}`，键是发送者名字，值是该发送者已经说过的单词总数。  
2. 只遍历一次 `messages`（下标 `i` 同时对应 `senders[i]`）：
   - 计算当前消息的单词数 `words = countWords(messages[i])`。  
   - 用 `cnt[senders[i]] = cnt.get(senders[i], 0) + words` 把单词数累加到该发送者的记录里。  
   - 这里的 `get` 方法相当于“查字典”，如果发送者还没有出现过，就返回默认值 `0`，再加上本条消息的单词数。
3. 遍历完后，字典里已经保存了 **每个发送者的完整单词总数**。  
4. 再遍历字典一次，找出 **最大单词数** 的发送者；如果出现相同的最大值，比较名字的字典序（`sender > best_sender`），取更大的那个。

**核心算法/数据结构解释**  

- **哈希表（字典）**：像一本**查字典**，可以在 **常数时间**（≈ O(1)）完成“找名字 → 看对应的单词数”。这比每次都遍历所有消息快得多。  
- **字典序比较**：在 Python 中，字符串直接用 `>`、`<` 比较时，会按照字典序（先比较首字符，若相同再比较下一位）进行。这正好满足题目要求“字典序更大的名字获胜”。  

**一步步推导**  
- 先想：**只要把每条消息的单词数加到对应发送者的累计里，就不需要再回头找**。  
- 再想：**怎样快速把“发送者 → 累计数”存下来？** 用字典！  
- 最后：**遍历完后，怎么挑选最大者？** 再遍历一次字典，用 “单词数更大或单词数相同且名字更大” 的规则更新答案。

#### 代码（Python）

```python
from typing import List

def countWords(message: str) -> int:
    """返回一句话的单词数，等价于空格个数 + 1"""
    # 直接利用 split，省去手动计数
    return len(message.split(' '))

def largestWordCount(messages: List[str], senders: List[str]) -> str:
    """
    最优实现：一次遍历统计 + 一次遍历挑选最大者
    时间 O(n)，空间 O(k)（k 为不同发送者的数量，最坏 O(n)）
    """
    # 第一步：统计每个发送者的累计单词数
    cnt = {}                       # 哈希表：sender -> total words
    for msg, snd in zip(messages, senders):
        words = countWords(msg)    # 当前消息的单词数
        # 累加到发送者的记录里；如果发送者第一次出现，默认累计为 0
        cnt[snd] = cnt.get(snd, 0) + words

    # 第二步：挑选单词数最多且名字字典序最大的发送者
    best_sender = ""
    best_cnt = -1
    for snd, total in cnt.items():
        # 条件：更大的单词数 OR 单词数相同且名字更大
        if total > best_cnt or (total == best_cnt and snd > best_sender):
            best_cnt = total
            best_sender = snd

    return best_sender
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次 `messages`（和 `senders` 同时遍历），每条消息的单词统计是 `O(L)`，总长度受限于 `100 * n`，整体仍是线性 `O(n)`。  
  - 再遍历一次字典，最多 `k ≤ n` 条记录，也是 `O(n)`。  
  - 用大白话说，就是 **“每条消息只看一次”**，即使 `n` 增大，耗时也只会等比例增长。

- **空间复杂度**：`O(k)`（k 为不同发送者的数量）  
  - 需要一个字典保存每个发送者的累计单词数，最坏情况每条消息的发送者都不相同，字典里会有 `n` 条记录，所以是 **线性空间**。  
  - 相比暴力解的 **O(1)** 额外空间，这里多用了字典，但换来了大幅的时间提升。

---

## 心得

- **核心技巧**：利用 **哈希表**（字典）一次遍历累计统计，再一次遍历挑选最大值。  
- **适用的题型**  
  1. “出现次数最多的元素” 类似题（如 `Top K Frequent Elements`）。  
  2. “分组求和/计数” 类题（如 `Group Anagrams`、`Maximum Population Year`）。  
  3. “根据属性排序/比较” 的题目（如 `Largest Number`、`Lexicographically Smallest String`）。
- **一句话总结解题钥匙**：**“把‘求和/计数’的工作交给哈希表，让每条数据只被处理一次”。**

---

## 反思

- **第一反应**：看到“每个发送者的单词总数”，第一时间想到 **计数**，于是想到遍历一次累加。  
- **最容易踩的坑**  
  1. **单词计数错误**：忽略了消息中可能只有一个单词（此时空格数为 0），正确公式是 “空格数 + 1”，使用 `split(' ')` 更安全。  
  2. **字典序比较**：在 Python 中直接使用 `>` 比较字符串即可，但要记住是 **字典序更大的**（而不是更小的）获胜。  
  3. **同名发送者多次出现**：必须把所有出现的消息累计，而不是只取一次。  
- **下次遇到同类题的第一步**：**先确认是否可以用哈希表把属性（如出现次数、总和）一次遍历完成**，如果可以，就直接走“统计 → 取最大/最小”路线。