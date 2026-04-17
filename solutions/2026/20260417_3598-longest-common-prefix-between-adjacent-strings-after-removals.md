# #3598. 最长公共前缀（longest common prefix）在删除元素后的相邻字符串 / Longest Common Prefix Between Adjacent Strings After Removals

> 难度：中等 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/longest-common-prefix-between-adjacent-strings-after-removals/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words. For each index i in the range [0, words.length - 1], perform the following steps:
Return an array answer, where answer[i] is the length of the longest common prefix between the adjacent pairs after removing the element at index i. If no adjacent pairs remain or if none share a common prefix, then answer[i] should be 0.

**Examples**

**Example 1:**

```
Input: words = ["jump","run","run","jump","run"]
Output: [3,0,0,3,3]
Explanation:
```

**Example 2:**

```
Input: words = ["dog","racer","car"]
Output: [0,0,0]
Explanation:
```

**Constraints**

- 1 <= words.length <= 105
- 1 <= words[i].length <= 104
- words[i] consists of lowercase English letters.
- The sum of words[i].length is smaller than or equal 105.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组（array）`words`。对于每个下标 `i`（范围为 `[0, words.length - 1]`），执行以下操作：  

返回一个整数数组 `answer`，其中 `answer[i]` 表示在删除下标为 `i` 的元素后，剩余相邻对（adjacent pairs）之间的最长公共前缀的长度。如果不存在相邻对，或所有相邻对的公共前缀长度均为 0，则 `answer[i]` 设为 0。

---

**示例 1**  
```text
Input: words = ["jump","run","run","jump","run"]
Output: [3,0,0,3,3]
Explanation:
删除下标 0 的 "jump" 后，剩余字符串为 ["run","run","jump","run"]，相邻对为 ("run","run")、("run","jump")、("jump","run")，最长公共前缀长度为 3（"run" 与 "run" 的公共前缀）。
删除下标 1 的 "run" 后，剩余字符串为 ["jump","run","jump","run"]，相邻对的公共前缀均为 0，故 answer[1] = 0。
其余下标依此类推，得到最终数组 [3,0,0,3,3]。
```

**示例 2**  
```text
Input: words = ["dog","racer","car"]
Output: [0,0,0]
Explanation:
无论删除哪个元素，剩余的相邻字符串之间都没有公共前缀，故所有答案均为 0。
```

**约束条件**  
- `1 <= words.length <= 10^5`  
- `1 <= words[i].length <= 10^4`  
- `words[i]` 仅由小写英文字母组成。  
- 所有 `words[i]` 的长度之和 ≤ `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次遍历** 所有可能的删除位置 `i`，对每个 `i`：

1. 把 `words[i]` 从数组里拿掉，得到一个新数组 `new_words`。  
2. 依次检查 `new_words` 中所有相邻的两个字符串，计算它们的 **最长公共前缀**（Longest Common Prefix，简称 LCP）。  
3. 取这些 LCP 长度的最大值作为 `answer[i]`（如果没有相邻对或者所有 LCP 为 0，就返回 0）。

> **哈希表的类比**：如果我们把“相邻对的 LCP 长度”看作是“字典里词对应的页码”，暴力解相当于把每一本书都拆开、重新排版，再一个一个查字典——非常费时。

**为什么能得到正确答案**  
因为我们枚举了**所有**可能的删除位置，并且在每种情况下遍历了**所有**相邻对，计算了它们的真实公共前缀长度，最后取最大值，自然就是题目要求的答案。

**复杂度分析（大白话）**  

- 假设数组长度为 `n`，每个字符串的长度平均为 `L`。  
- 对每个 `i`（共 `n` 次）我们都要重新遍历一次剩余的数组，最多要比较 `n-1` 对相邻字符串，每对最多比较 `L` 个字符。  
- 所以总共要做大约 `n × (n-1) × L` 次字符比较，时间复杂度记作 **O(n²·L)**。  
- 只用了几个额外的列表来保存答案，空间上只需要 **O(n)**。

> **O(n²·L) 的意义**：如果 `n=10⁴`，`L=10`，那么比较次数大约是 `10⁸`，在 Python 里会非常慢，几乎会超时。

#### 代码（Python）

```python
def longest_common_prefix(a: str, b: str) -> int:
    """返回两个字符串的最长公共前缀长度"""
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return i


def brute_force(words):
    n = len(words)
    ans = [0] * n

    for i in range(n):                       # 枚举要删除的位置
        # 1. 把第 i 个元素去掉，得到新数组
        new_words = words[:i] + words[i + 1:]

        # 2. 计算新数组里所有相邻对的 LCP，取最大值
        max_lcp = 0
        for j in range(len(new_words) - 1):
            lcp_len = longest_common_prefix(new_words[j], new_words[j + 1])
            if lcp_len > max_lcp:
                max_lcp = lcp_len

        ans[i] = max_lcp                      # 保存答案

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²·L)` —— 两层循环 + 每次比较字符。  
  > 大白话：如果 `n` 是 1000，`L` 是 10，程序要跑大约 10⁷ 次字符比较，已经接近能接受的上限。  
- **空间复杂度**：`O(n)` —— 只用了一个和输入等长的答案数组以及临时的 `new_words`（长度 `n-1`）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次删除都要重新遍历整个数组**。  
观察可以发现：

- 删除第 `i` 个元素后，**大部分相邻对并没有改变**。  
  - 只会失去两对：`(words[i‑1], words[i])` 与 `(words[i], words[i+1])`（如果它们存在）。  
  - 会多出一对：`(words[i‑1], words[i+1])`（如果两端都有元素）。  
- 因此，只要我们预先知道 **原数组中每一对相邻字符串的 LCP 长度**，就可以在 **O(1)** 时间内得到除去这两对之外的最大 LCP。

**关键步骤**

1. **预处理相邻 LCP**  
   - 建立数组 `lcp[i] = LCP(words[i], words[i+1])`，长度为 `n‑1`。  
   - 计算每个 LCP 的时间是 `O(length_of_shorter_string)`，所有 LCP 的总时间是 **O(总字符数)**，即 ≤ `10⁵`。

2. **前缀最大 & 后缀最大**  
   - `pref_max[i]` = `max(lcp[0..i])`（从左到右的最大前缀）。  
   - `suf_max[i]` = `max(lcp[i..n‑2])`（从右到左的最大后缀）。  
   - 这两趟线性扫描各是 `O(n)`。

3. **逐个位置求答案**  
   对每个 `i`：
   - `left = pref_max[i‑2]`（如果 `i‑2 >= 0`），表示删除 `i` 前，左侧所有相邻对的最大 LCP。  
   - `right = suf_max[i+1]`（如果 `i+1 <= n‑2`），表示右侧所有相邻对的最大 LCP。  
   - `cross = LCP(words[i‑1], words[i+1])`（如果 `0 < i < n‑1`），即新产生的相邻对。  
   - `answer[i] = max(left, right, cross)`。

这样每个 `i` 只做 **常数次** 的查表和一次 LCP 计算（只针对 `i‑1` 与 `i+1`），整体时间 **O(n + total_len)**，空间 **O(n)**。

> **单调栈/前缀和的类比**：这里的 `pref_max` 与 `suf_max` 就像在求数组最大值的“前缀最大”和“后缀最大”。想象你在排队买票，前面的人已经排好序，你只需要知道排到第几个人的最高票价，而不必每次都重新遍历所有人。

#### 代码（Python）

```python
def longest_common_prefix(a: str, b: str) -> int:
    """返回两个字符串的最长公共前缀长度（一次遍历）"""
    i = 0
    # 同时遍历两串，遇到不同字符或到达任意一串结尾就停
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return i


def optimal(words):
    n = len(words)
    if n == 1:                # 只剩一个元素，删除后没有相邻对
        return [0]

    # 1. 计算相邻 LCP，长度 n-1
    lcp = [0] * (n - 1)
    for i in range(n - 1):
        lcp[i] = longest_common_prefix(words[i], words[i + 1])

    # 2. 前缀最大
    pref_max = [0] * (n - 1)
    cur = 0
    for i in range(n - 1):
        cur = max(cur, lcp[i])
        pref_max[i] = cur

    # 3. 后缀最大
    suf_max = [0] * (n - 1)
    cur = 0
    for i in range(n - 2, -1, -1):
        cur = max(cur, lcp[i])
        suf_max[i] = cur

    # 4. 逐个位置求答案
    ans = [0] * n
    for i in range(n):
        left = pref_max[i - 2] if i - 2 >= 0 else 0          # 删除 i 前的最大 LCP
        right = suf_max[i + 1] if i + 1 <= n - 2 else 0    # 删除 i 后的最大 LCP
        cross = 0
        if 0 < i < n - 1:                                   # 两端都有元素，产生新相邻对
            cross = longest_common_prefix(words[i - 1], words[i + 1])
        ans[i] = max(left, right, cross)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + total_len)`  
  - 计算所有相邻 LCP：`O(total_len)`（总字符数 ≤ 10⁵）  
  - 前缀/后缀最大扫描：`O(n)`  
  - 最后遍历一次求答案：`O(n)`  
  与暴力解的 `O(n²·L)` 相比，几乎是线性级别，能够轻松通过 10⁵ 规模的测试。

- **空间复杂度**：`O(n)`  
  - 需要存 `lcp、pref_max、suf_max、ans` 四个长度为 `n`（或 `n‑1`）的数组。  
  - 这在题目限制下是完全可以接受的。

---

## 心得

- **核心技巧**：利用 **前缀最大 / 后缀最大**（或前缀/后缀信息）把“除去某个元素后的全局最大值”转化为常数时间查询。  
- **适用场景**  
  1. **删除单个元素后求全局最大/最小**（如 “删除一个数后数组的最大差值”）。  
  2. **数组中每次屏蔽一段后求区间最大**（类似 “滑动窗口最大值” 的思路）。  
  3. **两端合并后求新属性**（如本题的跨越 `i‑1` 与 `i+1` 的 LCP）。  
- **一句话总结**：**“把所有局部信息预处理好，再用前缀/后缀合并，删除操作就能 O(1) 完成”。**

---

## 反思

- **第一反应**：直接模拟删除再遍历，想到暴力实现。  
- **最容易踩的坑**  
  - **边界条件**：`i` 在数组最左或最右时没有左/右相邻对，需要把对应的 `left`、`right`、`cross` 设为 0。  
  - **空数组或单元素数组**：删除后没有相邻对，答案全为 0。  
  - **字符总长度的限制**：虽然单个字符串最长可达 10⁴，但所有字符总和 ≤ 10⁵，必须利用这一点避免 O(n·L) 的二次遍历。  
- **下次遇到类似题**：第一步先思考 **“删除/屏蔽一个元素后，哪些局部信息会改变？”**，随后考虑 **前缀/后缀/单调结构** 预处理，把“全局查询”转化为 **O(1)** 的表格查找。