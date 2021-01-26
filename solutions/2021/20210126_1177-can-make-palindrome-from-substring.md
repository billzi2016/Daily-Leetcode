# #1177. 能否通过子串构造回文 / Can Make Palindrome from Substring

> 难度：中等 · 标签：Array、Hash Table、String、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/can-make-palindrome-from-substring/)

---

## 题目（英文原版）

**Description**

You are given a string s and array queries where queries[i] = [lefti, righti, ki]. We may rearrange the substring s[lefti...righti] for each query and then choose up to ki of them to replace with any lowercase English letter.
If the substring is possible to be a palindrome string after the operations above, the result of the query is true. Otherwise, the result is false.
Return a boolean array answer where answer[i] is the result of the ith query queries[i].
Note that each letter is counted individually for replacement, so if, for example s[lefti...righti] = "aaa", and ki = 2, we can only replace two of the letters. Also, note that no query modifies the initial string s.
Example :

**Examples**

**Example 1:**

```
Input: s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]
Output: [true,false,false,true,true]
Explanation:
queries[0]: substring = "d", is palidrome.
queries[1]: substring = "bc", is not palidrome.
queries[2]: substring = "abcd", is not palidrome after replacing only 1 character.
queries[3]: substring = "abcd", could be changed to "abba" which is palidrome. Also this can be changed to "baab" first rearrange it "bacd" then replace "cd" with "ab".
queries[4]: substring = "abcda", could be changed to "abcba" which is palidrome.
```

**Example 2:**

```
Input: s = "lyb", queries = [[0,1,0],[2,2,1]]
Output: [false,true]
```

**Constraints**

- 1 <= s.length, queries.length <= 105
- 0 <= lefti <= righti < s.length
- 0 <= ki <= s.length
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个查询数组 `queries`，其中 `queries[i] = [left_i, right_i, k_i]`。对于每个查询，我们可以**重新排列**子串 `s[left_i...right_i]`，随后最多选择 `k_i` 个字符替换为任意小写英文字母。

如果在上述操作后，该子串能够构成**回文串**（palindrome），则该查询的结果为 `true`；否则为 `false`。返回一个布尔数组 `answer`，其中 `answer[i]` 为第 `i` 个查询 `queries[i]` 的结果。

> 注意，替换时每个字符单独计数，例如当 `s[left_i...right_i] = "aaa"` 且 `k_i = 2` 时，我们只能替换其中的两个字符。另外，所有查询均**不修改**原始字符串 `s`。

---

### 示例

**示例 1**

```text
Input: s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]
Output: [true,false,false,true,true]
Explanation:
queries[0]: 子串 = "d"，本身就是回文。
queries[1]: 子串 = "bc"，不是回文。
queries[2]: 子串 = "abcd"，仅能替换 1 个字符，仍无法构成回文。
queries[3]: 子串 = "abcd"，可以改成 "abba"，此时是回文。此时只用了 2 次替换。
queries[4]: 子串 = "abcda"，可以改成 "aacaa"（或其他形式），只需 1 次替换，即为回文。
```

**示例 2**

```text
Input: s = "lyb", queries = [[0,1,0],[2,2,1]]
Output: [false,true]
```

---

### 约束

- `1 <= s.length, queries.length <= 10^5`
- `0 <= left_i <= right_i < s.length`
- `0 <= k_i <= s.length`
- `s` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每个查询的子串真的取出来**，  
1. 统计子串里每个字母出现的次数（可以用一个长度为 26 的数组）。  
2. 根据题意，先把子串的字符随意重新排列，再最多改 `k` 个字符。  
   - 一个回文串的特征是：**至多只能有一个字符出现奇数次**（奇数次的字符只能放在回文的中间），其余字符必须出现偶数次。  
3. 统计子串里出现奇数次的字符个数 `odd_cnt`。  
   - 如果 `odd_cnt` 本身已经 ≤ 1，则不需要改动，直接返回 `True`。  
   - 否则，每改掉 **两个** 奇数次的字符（把其中一个改成另一个的配对），就能把两个奇数次数变成偶数次数。  
   - 因此需要的最小改动次数为 `(odd_cnt - 1) // 2`（向下取整），只要 `k` 不小于这个值，就可以构造回文。  

这个思路在概念上没有问题，只是**每个查询都要遍历一次子串**，在最坏情况下会导致 O(n·q) 的时间，其中 n 是字符串长度，q 是查询数量。  

#### 代码（Python）

```python
def can_make_palindrome_bruteforce(s: str, queries):
    ans = []
    for left, right, k in queries:
        # 1️⃣ 统计子串字符频率
        freq = [0] * 26                     # 26 个小写字母的计数器
        for i in range(left, right + 1):    # 把子串每个字符都遍历一遍
            freq[ord(s[i]) - ord('a')] += 1

        # 2️⃣ 统计奇数次数的字符个数
        odd_cnt = sum(cnt % 2 for cnt in freq)

        # 3️⃣ 需要的最少改动次数
        #   每改掉两个奇数次数的字符，就能让它们变偶数
        need = (odd_cnt - 1) // 2 if odd_cnt > 1 else 0

        # 4️⃣ 判断是否够 k 次改动
        ans.append(k >= need)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(q * L)`，其中 `L = right-left+1` 是子串长度。最坏情况下 `L≈n`，所以是 `O(n·q)`。  
  - 这里的 `O(n·q)` 可以想象成「每个查询都要把整条字符串重新读一遍」——如果 `n`、`q` 都是 10⁵，计算量会天文级别，根本跑不动。  
- **空间复杂度**：`O(1)`（只用了 26 长度的固定数组），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次查询都重新遍历子串**。我们需要一种**能在 O(1) 或 O(log n) 时间内得到子串的字符频率**的方法。  

**前缀计数（Prefix Sum）** 能帮助我们做到这一点。  
- 对于每个位置 `i`（0‑based），记录从字符串开头到 `i` 为止，每个字母出现的次数。记作 `pref[i][c]`（c∈0..25）。  
- 那么任意子串 `[l, r]` 的字符频率 = `pref[r] - pref[l-1]`（边界要特别处理）。  
- 只需要 O(1) 的数组相减，就能得到子串里每个字母的出现次数。

**进一步的优化**：我们其实只关心每个字母出现次数的 **奇偶性**（是奇数还是偶数），因为判断回文只需要统计奇数次数的字符个数。  
- 用 26 位的二进制整数 `mask` 来表示奇偶性：第 `c` 位为 1 表示字母 `c` 出现奇数次，为 0 表示出现偶数次。  
- 当我们遍历字符串时，遇到字符 `c` 就把 `mask` 的第 `c` 位 **异或** (`^=`) 一次，这样奇数次会变成 1，偶数次会恢复为 0。  
- 前缀异或数组 `pre[i]`（i 为下标）记录 `s[0..i]` 的奇偶性掩码。  

得到子串 `[l, r]` 的奇偶性掩码只需要 `pre[r] ^ pre[l-1]`（同样的异或原理）。  
- 该掩码的二进制中 1 的个数就是子串里出现奇数次的字符数 `odd_cnt`。  
- Python 中 `int.bit_count()`（或 `bin(x).count('1')`）可以在 O(1) 时间内算出 1 的个数（底层是硬件指令）。

**判断能否变成回文**的条件仍然是：  
- 需要的最少改动次数 `need = max(0, (odd_cnt - 1) // 2)`  
- 只要 `k >= need` 即可。

这样，每个查询只用了 **常数时间**（几次数组取值、一次异或、一次位计数），整体复杂度是 `O(n + q)`，能够轻松通过 10⁵ 规模的限制。

#### 代码（Python）

```python
def canMakePalindrome(s: str, queries):
    """
    最优解：利用前缀异或 + 位计数
    """
    n = len(s)

    # 1️⃣ 构建前缀奇偶性掩码数组
    # pre[i] 表示 s[0..i]（含 i）所有字符出现次数的奇偶性
    pre = [0] * n
    mask = 0
    for i, ch in enumerate(s):
        bit = 1 << (ord(ch) - ord('a'))   # 对应字符的位
        mask ^= bit                       # 出现一次就翻转该位
        pre[i] = mask

    # 2️⃣ 处理每个查询
    ans = []
    for left, right, k in queries:
        # 取子串的奇偶性掩码
        sub_mask = pre[right] ^ (pre[left - 1] if left > 0 else 0)

        # 统计掩码中 1 的个数 => 奇数次数字符的数量
        odd_cnt = sub_mask.bit_count()    # Python 3.8+ 可用 int.bit_count()

        # 需要的最少改动次数（每改掉两个奇数次数的字符即可让它们变偶数）
        need = (odd_cnt - 1) // 2 if odd_cnt > 1 else 0

        ans.append(k >= need)

    return ans
```

> **代码要点注释**  
> - `1 << (ord(ch)-ord('a'))` 把字符映射到 0~25 的位，类似“把字母的编号写在灯箱上”。  
> - `mask ^= bit` 用 **异或** 把该位翻转，奇数次变 1，偶数次恢复 0。  
> - `pre[right] ^ pre[left-1]` 利用异或的**抵消**特性得到子串的奇偶性。  
> - `int.bit_count()` 是 **硬件层面** 的位计数，时间几乎可以认为是 O(1)。  

#### 复杂度  

- **时间复杂度**：`O(n + q)`  
  - 前缀掩码构建遍历一次字符串 O(n)。  
  - 每个查询只做常数次数组访问、一次异或和一次位计数 O(1)，共 `q` 次 → O(q)。  
  - 相比暴力的 O(n·q)，提升巨大，能够轻松处理 10⁵ 规模。  

- **空间复杂度**：`O(n)`  
  - 需要保存前缀掩码数组 `pre`，长度为 `n`，每个元素是一个 32 位整数（足够容纳 26 位）。  
  - 其余使用的空间都是常数级别。  

---

## 心得  

- **核心技巧**：**前缀异或 + 位计数**，把“统计字符出现次数”压缩到 26 位的奇偶性掩码中。  
- **适用场景**：  
  1. 需要快速判断子串中 **奇数出现次数的字符个数**（如「回文能否构造」）。  
  2. “子串字符集合相同” 的比较（例如 **判断两个子串是否是字母异位词**）。  
  3. **子串奇偶性** 相关的问题（比如「子串能否全部配对」）。  
- **一句话总结**：**把「出现多少次」降维成「出现奇偶」并用位运算一次搞定子串统计**。

---

## 反思  

- **第一反应**：直接把子串取出来统计，写出判断奇数次数的逻辑。  
- **最容易踩的坑**：  
  - 忘记 **子串可以重新排列**，导致错误地关注字符顺序。  
  - 计算最少改动次数时遗漏了「每次改动可以消除两个奇数」的细节。  
  - 在实现前缀异或时，边界 `left = 0` 需要特殊处理，否则会出现负索引错误。  
- **下次类似题**的第一步：**先问自己「我到底关心什么信息」**——这里是每个字符的奇偶性。随后寻找 **前缀/差分** 或 **位运算** 能否在 O(1) 内得到该信息。这样就能立刻跳出暴力循环，锁定最优思路。