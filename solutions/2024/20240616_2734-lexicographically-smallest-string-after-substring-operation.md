# #2734. 子串操作后的字典序最小字符串 / Lexicographically Smallest String After Substring Operation

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-string-after-substring-operation/)

---

## 题目（英文原版）

**Description**

Given a string s consisting of lowercase English letters. Perform the following operation:
Return the lexicographically smallest string after performing the operation.

**Examples**

**Example 1:**

```
Input: s = "cbabc"
Output: "baabc"
Explanation:
Perform the operation on the substring starting at index 0, and ending at index 1 inclusive.
```

**Example 2:**

```
Input: s = "aa"
Output: "az"
Explanation:
Perform the operation on the last letter.
```

**Example 3:**

```
Input: s = "acbbc"
Output: "abaab"
Explanation:
Perform the operation on the substring starting at index 1, and ending at index 4 inclusive.
```

**Example 4:**

```
Input: s = "leetcode"
Output: "kddsbncd"
Explanation:
Perform the operation on the entire string.
```

**Constraints**

- 1 <= s.length <= 3 * 105
- s consists of lowercase English letters

---

## 题目（中文翻译）

给定一个只包含小写英文字母的字符串 **s**。可以对 **s** 选择任意一个非空子串（substring），并将子串中的每个字符都替换为字母表中前一个字符，若字符为 `'a'` 则替换为 `'z'`。  
请在执行一次上述操作后，返回可以得到的字典序（lexicographically）最小的字符串。

**示例 1**  
Input: `s = "cbabc"`  
Output: `"baabc"`  
**解释**：对下标 0 到 1（包含）的子串进行操作，将 `"cb"` 变为 `"ba"`。

**示例 2**  
Input: `s = "aa"`  
Output: `"az"`  
**解释**：对最后一个字符进行操作，将 `'a'` 变为 `'z'`。

**示例 3**  
Input: `s = "acbbc"`  
Output: `"abaab"`  
**解释**：对下标 1 到 4（包含）的子串进行操作，将 `"cbbc"` 变为 `"baab"`。

**示例 4**  
Input: `s = "leetcode"`  
Output: `"kddsbncd"`  
**解释**：对整个字符串进行操作，每个字符均替换为前一个字符。

**约束条件**  
- `1 <= s.length <= 3 * 10^5`  
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的子串都枚举一遍**，对每个子串执行一次“字母向前移一位”的操作（`a → z`，其余字母 `c → chr(ord(c)-1)`），得到新的字符串后和当前最好的答案比较，保留字典序最小的那个。

- **数据结构**：这里只需要用到 **字符串** 本身和 **列表**（把字符串转成列表方便原地修改）。可以把列表想象成一本笔记本，里面每一格对应一个字符，修改格子里的字母就像在本子上改字。
- **正确性**：因为我们把 **所有** 子串都尝试了一遍，必然会覆盖最优的那一次操作，所以最终选出的答案一定是字典序最小的。
- **复杂度分析**：  
  - 枚举子串的个数是 `n*(n+1)/2`（前 `n` 个数的和），每次操作要遍历子串长度，最坏情况下相当于 **O(n³)** 的时间，这在 `n ≤ 3·10⁵` 时根本不可接受。  
  - 额外空间只需要保存一个新的字符串，**O(n)**。

> **大白话**：  
> - `O(n³)` 就好比你把一本 10 万页的书每一页都抄 10 万遍再比大小，根本不现实。  

#### 代码（Python）

```python
def smallestString_bruteforce(s: str) -> str:
    n = len(s)
    best = None                       # 用来记录当前找到的最小字符串
    for i in range(n):                # 枚举子串左端点
        for j in range(i, n):         # 枚举子串右端点（包括 i、j）
            # 把 s[i..j] 中的每个字符都往前挪一位
            tmp = list(s)             # 把字符串转成列表，方便修改
            for k in range(i, j + 1):
                if tmp[k] == 'a':
                    tmp[k] = 'z'      # a 往前一位变成 z
                else:
                    tmp[k] = chr(ord(tmp[k]) - 1)
            cand = ''.join(tmp)       # 把列表再拼成字符串
            if best is None or cand < best:
                best = cand           # 更新最小值
    return best
```

> **注释**  
> - `tmp = list(s)`：把不可变的字符串变成可改的列表，就像把纸张换成可擦写的白板。  
> - `chr(ord(tmp[k]) - 1)`：把字符的 ASCII 码减 1，再转回字符，实现“往前一位”。  

#### 复杂度

- **时间复杂度**：`O(n³)` —— 需要枚举所有子串并对每个子串的每个字符做一次修改。  
  - 直观理解：如果 `n=1000`，相当于要做 10⁹ 次操作，根本跑不完。  
- **空间复杂度**：`O(n)` —— 只保存一次临时的字符列表和当前最小答案。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于“遍历所有子串”。我们要思考：**到底哪些子串值得尝试？**  

观察题目要求的操作特点：

1. **把字母往前移一位会让字典序更小**，但 `a → z` 会让字母变大（因为 `'z'` 在字母表最后）。  
2. 因此，我们 **只想对那些不是 `'a'` 的字符** 进行“往前移”。  
3. 为了让整体字典序尽可能小，应该 **尽早（左侧）做出改变**，而且 **一次性把一段连续的非 `'a'` 字符都改掉**，这样后面的字符保持原样不会再把已经变小的前缀“抵消”。  

基于以上两点，可得最优策略：

- 从左到右找到第一个不是 `'a'` 的位置 `l`。  
- 从 `l` 开始向右一直走，直到遇到 `'a'` 为止（或者走到字符串末尾），记结束位置为 `r-1`。这段 `[l, r)` 是 **左侧第一个不含 `'a'` 的最长子串**。  
- 将这段子串里的每个字符都往前移一位（`a → z` 只会在全是 `'a'` 的特殊情况出现）。  
- **特殊情况**：如果整个字符串都是 `'a'`，我们只能把任意一个字符改成 `'z'`，最小的做法是把 **最后一个** `'a'` 变成 `'z'`（因为只改最后一个，对字典序的影响最小）。

> **类比**：  
> 想象每个字符是一个小球，`a` 是最轻的球，往前移相当于把球的重量减一。我们想让整排球的“重量序列”尽可能轻，于是从左边第一个不是最轻的球开始，把一整段连续的稍重球都轻一点；如果全都是最轻的球，只能把最右边的那颗球“倒回去”变成最重的 `z`，对整体影响最小。

#### 代码（Python）

```python
def smallestString(s: str) -> str:
    n = len(s)
    chars = list(s)                     # 转成列表，方便原地修改

    # 1️⃣ 找到左侧第一个不是 'a' 的位置
    l = 0
    while l < n and chars[l] == 'a':
        l += 1

    # 2️⃣ 全是 'a' 的情况 → 把最后一个改成 'z'
    if l == n:                          # 没找到非 'a'，说明全是 'a'
        chars[-1] = 'z'
        return ''.join(chars)

    # 3️⃣ 从 l 开始向右，直到遇到 'a' 为止
    r = l
    while r < n and chars[r] != 'a':
        # 把当前字符往前移一位
        chars[r] = chr(ord(chars[r]) - 1)   # 例如 'c' -> 'b'
        r += 1

    # 4️⃣ 其余字符保持不变，直接返回
    return ''.join(chars)
```

> **关键行注释**  
> - `while l < n and chars[l] == 'a': l += 1`：相当于在找“左侧第一颗不是最轻的球”。  
> - `if l == n:`：若遍历完都没有找到，说明所有球都是 `a`。  
> - `while r < n and chars[r] != 'a':`：把从 `l` 开始的连续非 `a` 区间全部“往前搬”。  
> - `chr(ord(chars[r]) - 1)`：把字符的 ASCII 码减 1，实现字母往前一步。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历字符串一次（最多两次指针），每个字符最多被处理一次。  
  - 与暴力解的 `O(n³)` 相比，简直是“把十万页的书一次性抄完”。  
- **空间复杂度**：`O(n)` —— 需要一个字符列表来存放结果（Python 字符串不可原地修改），相当于复制了一遍原字符串。

---

## 心得

- **核心技巧**：**一次遍历找左侧第一个非 `'a'` 的连续子串**，对这段子串统一做“字母前移”。  
- **适用题型**：  
  1. 需要对字符串做一次“局部改动”使整体字典序最小的题目（如 “Replace Substring to Minimize String”）。  
  2. “把字符往前/往后移动一次” 的贪心类题目（如 “Make String Great”）。  
  3. 需要找 **左侧第一个满足条件的连续段** 的问题（如 “最左侧非零子数组”等）。  
- **一句话总结**：**把左侧第一个连续的非 `'a'` 区间整体往前移一位，若全是 `'a'` 则把最后一个改成 `'z'`。**

---

## 反思

- **第一反应**：想到枚举所有子串——直觉上最安全，却忽视了规模限制。  
- **最容易踩的坑**：  
  - 忘记 `a` 往前会变成 `z`，导致在全是 `a` 的情况下没有正确处理。  
  - 没有考虑 “左侧第一个非 `'a'`” 之后可能出现的 `'a'`，导致把不该改的字符也改了。  
- **下次遇到同类题**：第一步先**思考**“哪些字符改动会让字典序变小”，再**定位**最左侧需要改动的连续段，尽量把改动范围限定在一次遍历能得到的区间。