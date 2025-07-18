# #3271. 哈希划分字符串 / Hash Divided String

> 难度：中等 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/hash-divided-string/)

---

## 题目（英文原版）

**Description**

You are given a string s of length n and an integer k, where n is a multiple of k. Your task is to hash the string s into a new string called result, which has a length of n / k.
First, divide s into n / k substrings, each with a length of k. Then, initialize result as an empty string.
For each substring in order from the beginning:
Return result.

**Examples**

**Example 1:**

```
Input: s = "abcd", k = 2
Output: "bf"
Explanation:
First substring: "ab" , 0 + 1 = 1 , 1 % 26 = 1 , result[0] = 'b' .
Second substring: "cd" , 2 + 3 = 5 , 5 % 26 = 5 , result[1] = 'f' .
```

**Example 2:**

```
Input: s = "mxz", k = 3
Output: "i"
Explanation:
The only substring: "mxz" , 12 + 23 + 25 = 60 , 60 % 26 = 8 , result[0] = 'i' .
```

**Constraints**

- 1 <= k <= 100
- k <= s.length <= 1000
- s.length is divisible by k.
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串 `s` 与整数 `k`，且 `n` 能被 `k` 整除。需要将字符串 `s` 哈希为一个新字符串 `result`，其长度为 `n / k`。

**操作步骤**  

1. 将 `s` 按顺序划分为 `n / k` 个子串（substring），每个子串的长度均为 `k`。  
2. 初始化 `result` 为一个空字符串。  
3. 依次遍历每个子串，执行以下操作：  
   - 计算子串中每个字符在字母表中的下标（`'a'` 对应 `0`，`'b'` 对应 `1`，...，`'z'` 对应 `25`）之和。  
   - 对该和取模 `26`，得到值 `v`。  
   - 将 `v` 转换回对应的字母（`0 → 'a'`，`1 → 'b'`，...，`25 → 'z'`），并将该字母追加到 `result` 的末尾。  
4. 最终返回 `result`。

---

### 示例

**示例 1**

```text
Input: s = "abcd", k = 2
Output: "bf"
Explanation:
第一个子串: "ab" ，0 + 1 = 1 ，1 % 26 = 1 ，result[0] = 'b' 。
第二个子串: "cd" ，2 + 3 = 5 ，5 % 26 = 5 ，result[1] = 'f' 。
```

**示例 2**

```text
Input: s = "mxz", k = 3
Output: "i"
Explanation:
唯一的子串: "mxz" ，12 + 23 + 25 = 60 ，60 % 26 = 8 ，result[0] = 'i' 。
```

---

### 约束条件

- `1 <= k <= 100`
- `k <= s.length <= 1000`
- `s.length` 能被 `k` 整除
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把原字符串 `s` 按照长度 `k` 划分成若干子串，每个子串算出 **所有字符在字母表中的序号之和**（`a → 0, b → 1, …, z → 25`），再对 26 取模，得到的数值再映射回字母，拼接成最终的 `result`。

> **类比**：  
> 把每个子串看成一本小字典，字典里每个词（字符）都有对应的页码（序号）。我们把这本小字典里所有词的页码加在一起，然后把总页码除以 26 取余，得到的余数就是新词（字符）所在的页码。

**为什么这样可以得到答案**：  
题目明确说明了“把每个子串的字符序号相加、模 26、再映射回字母”。只要我们严格按照这个步骤逐个子串地执行，就一定会得到题目要求的 `result`。

**时间/空间分析（大白话版）**  
- 外层循环遍历所有子串，子串的个数是 `n/k`（`n` 为字符串长度）。  
- 内层循环遍历子串内部的每个字符，长度恰好是 `k`。  
- 所以总共会访问 ` (n/k) * k = n` 次字符。  
- 用大 O 记法写就是 **O(n)**，也就是说时间随输入长度线性增长。  
- 我们只用到几个整数变量和最终的结果字符串，额外空间不随 `n` 增长，只是 **O(1)**（常数级）。

#### 代码（Python）

```python
def hashDividedString(s: str, k: int) -> str:
    """
    暴力实现：逐个子串、逐个字符求和
    """
    n = len(s)
    result = []                     # 用列表收集字符，最后 join 成字符串

    # 依次取出每个长度为 k 的子串
    for start in range(0, n, k):    # start = 0, k, 2k, ...
        sub = s[start:start + k]    # 当前子串，例如 "ab"

        # 计算子串里所有字符的字母序号之和
        total = 0
        for ch in sub:
            total += ord(ch) - ord('a')   # 'a' 的序号是 0，'b' 是 1，...

        # 对 26 取模，得到新字符的序号
        hashed_idx = total % 26

        # 把序号映射回字母并加入结果
        result.append(chr(hashed_idx + ord('a')))

    return ''.join(result)
```

#### 复杂度

- **时间复杂度：O(n)** — 这里的 `n` 是原字符串长度。我们遍历了每个字符一次，像走路一样一步不漏。
- **空间复杂度：O(1)** — 只用了常数个额外变量（`total`、`hashed_idx` 等），结果字符串本身是题目必须返回的，不算额外空间。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 **O(n)**，但它在每次处理子串时都要重新遍历 `k` 个字符。我们可以把“子串内部的字符和”看成一种**滑动窗口**的累计值：

1. **先算出第一个子串的字符和**（一次完整遍历 `k` 个字符）。
2. 当窗口向右移动一个字符时，**移出左边的字符、移入右边的字符**，这样可以在 **O(1)** 时间内得到下一个子串的和，而不必再次遍历整个子串。

这样做的好处是把每个字符的“加入”和“移除”操作只做一次，整体仍是 **O(n)**，但常数更小、更贴近线性扫描的思想。

> **类比**：  
> 想象你在走一条长长的走廊，走廊两端各放一个称。第一次称完你记下重量（子串和），以后每走一步，就把左边的箱子放下称、把右边的箱子放上称，称一次就知道新重量——不需要重新把整条走廊的箱子都搬到称上。

**核心技巧**：滑动窗口（Sliding Window）  
- 维护一个长度为 `k` 的窗口的字符和 `window_sum`。  
- 初始时遍历前 `k` 个字符得到 `window_sum`。  
- 每次窗口右移一步：`window_sum += new_char - old_char`（这里的 `new_char`、`old_char` 是对应的字母序号）。  
- 对 `window_sum` 取模并映射回字符。

**为什么正确**：  
窗口每次仅改变最左和最右的两个字符，其他字符保持不变，窗口内的字符和自然等于 **前一次的和** 加上 **新加入字符的序号** 减去 **移出字符的序号**。这正是我们在数学上对 “子串之和” 的递推关系。

#### 代码（Python）

```python
def hashDividedString(s: str, k: int) -> str:
    """
    最优实现：使用滑动窗口把每个子串的求和从 O(k) 降到 O(1)
    """
    n = len(s)
    result = []

    # 把字符转成对应的序号，便于后面直接相加/相减
    nums = [ord(ch) - ord('a') for ch in s]   # 例如 "ab" -> [0, 1]

    # 计算第一个窗口的和（前 k 个字符）
    window_sum = sum(nums[:k])

    # 第一个子串对应的字符
    result.append(chr((window_sum % 26) + ord('a')))

    # 从第二个子串开始，窗口每次右移一位
    for i in range(k, n, k):
        # 移出左边的字符（i - k），移入右边的字符（i + k - 1）
        window_sum += nums[i] - nums[i - k]   # O(1) 更新窗口和
        result.append(chr((window_sum % 26) + ord('a')))

    return ''.join(result)
```

> **关键行解释**  
> - `nums = [ord(ch) - ord('a') for ch in s]`：把字符串一次性转成整数列表，后面加减更快。  
> - `window_sum = sum(nums[:k])`：一次性算出第一个子串的和。  
> - `window_sum += nums[i] - nums[i - k]`：窗口右移一步的递推公式。  
> - `chr((window_sum % 26) + ord('a'))`：把模 26 的结果映射回字母。

#### 复杂度

- **时间复杂度：O(n)** — 只遍历一次字符列表，窗口的每一次移动都是常数时间。相较于“每个子串都重新遍历 `k` 次”，这里的常数更小。  
- **空间复杂度：O(n)**（**可优化到 O(1)**）——我们额外用了一个整数列表 `nums` 长度为 `n`，如果不想额外空间，也可以在遍历时直接使用 `ord`，这样空间降为 **O(1)**。这里保留列表是为了代码更易读。

---

## 心得

- **核心技巧**：滑动窗口（把子串的和从每次全遍历压缩到增量更新）。  
- **适用题型**：  
  1. “固定长度子数组/子串的和” 类问题（例如 LeetCode 209. Minimum Size Subarray Sum 的固定窗口变体）。  
  2. “滑动窗口求最大/最小值” 系列（如 3️⃣ 最大子数组和、最长无重复子串）。  
  3. “字符频率滑窗” 题目（如 438. Find All Anagrams in a String）。  
- **一句话总结**：**“把重复的工作搬到窗口的两端，只在两端加减，就能一次遍历搞定所有子串”。**

---

## 反思

- **第一反应**：看到“把字符串切成长度为 k 的块，求每块的字符序号和”，立刻想到最直接的“双层循环”实现。  
- **最容易踩的坑**：  
  - **字符序号的起点**：要记住 `a → 0`，否则会导致结果偏移一个字母。  
  - **取模位置**：先把总和取 `% 26` 再映射回字符，不能在映射后再取模。  
  - **边界条件**：`k` 可能等于 `1`（每个字符单独处理）或等于 `len(s)`（只有一个子串），代码需要兼容。  
- **下次类似题的第一步**：先确认“子串/子数组的长度是固定的”，然后思考是否可以用**滑动窗口**把“每次重新遍历”改成“增量更新”。这样往往能直接从暴力 O(n·k) 降到 O(n)。