# #3121. 统计特殊字符的数量 II / Count the Number of Special Characters II

> 难度：中等 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-special-characters-ii/)

---

## 题目（英文原版）

**Description**

You are given a string word. A letter c is called special if it appears both in lowercase and uppercase in word, and every lowercase occurrence of c appears before the first uppercase occurrence of c.
Return the number of special letters in word.

**Examples**

**Example 1:**

```
Input: word = "aaAbcBC"
Output: 3
Explanation:
The special characters are 'a' , 'b' , and 'c' .
```

**Example 2:**

```
Input: word = "abc"
Output: 0
Explanation:
There are no special characters in word .
```

**Example 3:**

```
Input: word = "AbBCab"
Output: 0
Explanation:
There are no special characters in word .
```

**Constraints**

- 1 <= word.length <= 2 * 105
- word consists of only lowercase and uppercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `word`。如果某个字母 `c` 同时以小写形式和大写形式出现在 `word` 中，并且所有小写形式的 `c` 都出现在该字母的第一个大写形式之前，则称 `c` 为特殊字符（special character）。返回 `word` 中特殊字符的数量。

**示例 1：**

```text
Input: word = "aaAbcBC"
Output: 3
Explanation:
特殊字符为 'a'、'b' 和 'c'。
```

**示例 2：**

```text
Input: word = "abc"
Output: 0
Explanation:
`word` 中不存在特殊字符。
```

**示例 3：**

```text
Input: word = "AbBCab"
Output: 0
Explanation:
`word` 中不存在特殊字符。
```

**约束条件**

- `1 <= word.length <= 2 * 10^5`
- `word` 仅由英文小写字母和大写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个可能的字母（a~z）都单独检查一遍**。  
具体步骤：

1. 取出字母 `c`（比如 `'a'`），在整个字符串 `word` 中**遍历两次**  
   * 第一次从左到右找到 `c` 第一次出现的大写形式 `'A'`（如果根本没有大写则记为 `∞`）。  
   * 第二次从左到右记录 `c` 最后一次出现的小写形式 `'a'`（如果根本没有小写则记为 `-1`）。  
2. 判断 `c` 是否满足 “小写出现且全部在大写之前”  
   * 必须两种形态都出现（`first_upper != ∞` 且 `last_lower != -1`）  
   * 且 **最后一次小写** 的下标 `< **第一次大写** 的下标**。  
3. 把满足条件的字母计数。

> **数据结构类比**：这里用到的“字典”类似于 **查字典**，我们把每个字母当作“词”，对应的“页码”是它在字符串里出现的位置（第一次大写、最后一次小写）。  

> **为什么一定对**：只要把每个字母在字符串里的出现位置全部找出来，就能精确判断是否符合题目要求，暴力遍历不会漏掉任何情况。

#### 代码（Python）

```python
def countSpecialLetters_bruteforce(word: str) -> int:
    INF = len(word)            # 表示“永远找不到”
    ans = 0

    # 对 26 个英文字母逐个检查
    for i in range(26):
        lower = chr(ord('a') + i)   # 小写字母，如 'a'
        upper = chr(ord('A') + i)   # 对应的大写字母，如 'A'

        first_upper = INF   # 第一次出现的大写下标，默认“不存在”
        last_lower = -1     # 最后一次出现的小写下标，默认“不存在”

        # 遍历整个字符串，记录两个位置
        for idx, ch in enumerate(word):
            if ch == upper and first_upper == INF:
                first_upper = idx          # 记录第一次出现的大写
            if ch == lower:
                last_lower = idx           # 不断更新，最终得到最后一次小写

        # 同时出现且小写全部在大写之前 → 特殊字母
        if first_upper != INF and last_lower != -1 and last_lower < first_upper:
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(26 * n) ≈ O(n)`  
  这里的 `n` 是字符串长度。我们对每个字母都遍历一遍字符串，26 是常数，所以整体仍然是线性时间。可以把 `O(n)` 想象成“和字符串长度成正比”，长度翻倍，跑的时间也大约翻倍。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量，和字符串长度无关，算作常数空间。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于我们对每个字母都把整个字符串扫一遍，虽然常数是 26，但我们完全可以一次遍历就把所有信息收集完。

**关键观察**：

- 对每个字母，只需要知道两件事：  
  1. **第一次出现的大写下标**（`first_upper`）  
  2. **最后一次出现的小写下标**（`last_lower`）  

- 这两件事可以在 **一次遍历** 中同步完成：  
  * 当遍历到字符 `ch` 时，  
    - 若它是大写，且该字母的 `first_upper` 仍未被记录，就把当前下标写进去（只记录第一次）。  
    - 若它是小写，就把 `last_lower` 更新为当前下标（不断覆盖，最终留下最后一次）。

- 使用 **长度为 26 的数组**（或字典）来存这两个信息，数组下标 `0~25` 分别对应 `'a'~'z'`，这样查找/更新都是 `O(1)`。

- 遍历结束后，只需遍历一次这 26 条记录，统计满足 `last_lower < first_upper` 的字母即可。

> **数据结构类比**：把这 26 条记录想象成 **一本小字典**，每一页只写两个数字（第一次大写、最后一次小写），翻页（下标）是常数时间。

#### 代码（Python）

```python
def countSpecialLetters(word: str) -> int:
    n = len(word)
    INF = n          # “不存在”时使用 n 这个最大下标

    # 下面两个列表长度固定为 26，分别记录第一次大写、最后一次小写的下标
    first_upper = [INF] * 26   # 初始为 “永远找不到”
    last_lower = [-1] * 26     # 初始为 “从未出现”

    # 单次遍历收集信息
    for idx, ch in enumerate(word):
        if 'a' <= ch <= 'z':               # 小写字母
            pos = ord(ch) - ord('a')
            last_lower[pos] = idx          # 覆盖为最新下标（即最后一次出现）
        else:                              # 大写字母
            pos = ord(ch) - ord('A')
            if first_upper[pos] == INF:    # 只写入第一次出现的大写下标
                first_upper[pos] = idx

    # 统计满足条件的字母数量
    ans = 0
    for i in range(26):
        if last_lower[i] != -1 and first_upper[i] != INF and last_lower[i] < first_upper[i]:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历字符串一次，再遍历 26 条记录一次。可以把 `O(n)` 想成“和字符串长度成正比”，无论字符串多长，时间增长速度就是线性增长。

- **空间复杂度**：`O(1)`  
  使用的两个长度固定为 26 的数组占的空间不随 `n` 增长，属于常数空间。

---

## 心得

- **核心技巧**：一次遍历收集“**第一次出现**”和“**最后一次出现**”两类信息。  
- **适用的题型**  
  1. “首次出现/最后一次出现”类问题（如 LeetCode 387 *First Unique Character in a String*）  
  2. 需要比较出现顺序的字符统计（如 “字符是否全部出现在另一字符之前”）  
  3. 使用 **哈希表/数组** 记录每个字符的若干状态的题目（如 2420 *Find All Good Indices*）  
- **一句话总结**：**一次线性遍历即可把所有字母的关键位置信息全部记下来，再统一检查即可**。

---

## 反思

- **第一反应**：先想到“每个字母单独扫描”，即暴力的 26 × n 做法。  
- **最容易踩的坑**  
  1. **边界情况**：字母只出现小写或只出现大写时，需要排除，否则会误判。  
  2. **下标比较**：要确保比较的是 “最后一次小写” 与 “第一次大写”，而不是随意的出现顺序。  
  3. **字符类型判断**：要区分大小写，不能直接用 `isupper()`/`islower()`，否则会把非字母字符误算（虽然本题只给英文字母，但养成好习惯）。  
- **下次遇到同类题**，第一步应该想到 **“一次遍历收集每个字符的关键位置/状态”**，再根据这些信息进行统一判断。这样既省时又省空间。