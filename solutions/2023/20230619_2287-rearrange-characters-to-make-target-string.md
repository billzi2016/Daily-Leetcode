# #2287. 重新排列字符以构造目标字符串 / Rearrange Characters to Make Target String

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/rearrange-characters-to-make-target-string/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed strings s and target. You can take some letters from s and rearrange them to form new strings.
Return the maximum number of copies of target that can be formed by taking letters from s and rearranging them.
Note: This question is the same as  1189: Maximum Number of Balloons.

**Examples**

**Example 1:**

```
Input: s = "ilovecodingonleetcode", target = "code"
Output: 2
Explanation:
For the first copy of "code", take the letters at indices 4, 5, 6, and 7.
For the second copy of "code", take the letters at indices 17, 18, 19, and 20.
The strings that are formed are "ecod" and "code" which can both be rearranged into "code".
We can make at most two copies of "code", so we return 2.
```

**Example 2:**

```
Input: s = "abcba", target = "abc"
Output: 1
Explanation:
We can make one copy of "abc" by taking the letters at indices 0, 1, and 2.
We can make at most one copy of "abc", so we return 1.
Note that while there is an extra 'a' and 'b' at indices 3 and 4, we cannot reuse the letter 'c' at index 2, so we cannot make a second copy of "abc".
```

**Example 3:**

```
Input: s = "abbaccaddaeea", target = "aaaaa"
Output: 1
Explanation:
We can make one copy of "aaaaa" by taking the letters at indices 0, 3, 6, 9, and 12.
We can make at most one copy of "aaaaa", so we return 1.
```

**Constraints**

- 1 <= s.length <= 100
- 1 <= target.length <= 10
- s and target consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的字符串 `s` 和 `target`。你可以从 `s` 中取出若干字符并重新排列它们，形成新的字符串。返回通过从 `s` 中取字母并重新排列后，能够构造的 `target` 的最大拷贝（copy）数。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- 1 ≤ s.length ≤ 100  
- 1 ≤ target.length ≤ 10  
- `s` 和 `target` 只包含小写英文字母。  

> **注意**：本题等价于 1189: Maximum Number of Balloons。

---

### 示例

#### 示例 1
**输入**  
```txt
s = "ilovecodingonleetcode", target = "code"
```
**输出**  
```txt
2
```
**解释**：  
- 对于第一份 `"code"`，取下标为 4、5、6、7 的字符。  
- 对于第二份 `"code"`，取下标为 17、18、19、20 的字符。  
形成的字符串分别为 `"ecod"` 和 `"code"`，它们都可以重新排列成 `"code"`。  
最多可以得到两份 `"code"`，因此返回 `2`。

#### 示例 2
**输入**  
```txt
s = "abcba", target = "abc"
```
**输出**  
```txt
1
```
**解释**：  
我们可以取下标 0、1、2 的字符，得到一份 `"abc"`。  
虽然下标 3、4 处还有额外的 `'a'` 和 `'b'`，但下标 2 处的 `'c'` 已经被使用，无法再组成第二份 `"abc"`，所以最多只能得到一份，返回 `1`。

#### 示例 3
**输入**  
```txt
s = "abbaccaddaeea", target = "aaaaa"
```
**输出**  
```txt
1
```
**解释**：  
取下标 0、3、6、9、12 的字符即可得到一份 `"aaaaa"`。  
最多只能得到一份，返回 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**一边遍历 `s`，一边尝试把 `target` 的字母一个个拼起来**。  
具体做法：

1. 把 `target` 当成一个“配方”，需要多少个 `'a'`、多少个 `'b'` ……  
2. 从 `s` 的左边开始取字符，看到的字符如果正好是配方里还缺的，就把它填进去。  
3. 当配方全部填满时，说明已经成功拼出了一份 `target`，计数器 `ans` 加 1，随后把配方重新恢复到初始状态，继续往后走，尝试再拼下一份。  
4. 当遍历完 `s`，再也找不到完整的配方时，返回 `ans`。

> **类比**：把 `target` 想成一道菜的配方，需要的食材是特定数量的字母。`s` 就是一篮子散落的食材，我们一个一个往锅里倒，凑齐配方就能做出一道菜。做完一道后再把配方重新摆好，继续挑食材。

这种方法一定能得到正确答案，因为我们**不遗漏任何可能的字母**，每次只要配方满足就计数一次。

#### 代码（Python）

```python
def maxCopies_bruteforce(s: str, target: str) -> int:
    # 统计 target 中每个字符需要的数量，形成配方 dict
    need = {}
    for ch in target:
        need[ch] = need.get(ch, 0) + 1

    ans = 0                     # 已经成功拼出的 target 副本数
    cur = need.copy()           # 当前还缺的字符数量

    for ch in s:                # 依次取 s 中的字符
        if ch in cur:           # 只有配方里需要这种字符才考虑
            cur[ch] -= 1        # 用掉一个
            if cur[ch] == 0:    # 这种字符已经全部满足
                del cur[ch]     # 从缺的列表里移除，方便判断是否完成

        # 当配方全部被满足（cur 为空），说明成功拼出一份 target
        if not cur:
            ans += 1
            cur = need.copy()   # 重新准备下一份的配方

    return ans
```

#### 复杂度

- **时间复杂度**：`O(|s| * |target|)`  
  实际上遍历一次 `s`（长度记为 `n`），每次对字典的增删查都是 `O(1)`，所以整体是线性 `O(n)`。这里写成 `O(|s| * |target|)` 只是一种保守的写法，强调我们在每一步都在对照配方（配方大小 ≤ 10）。
- **空间复杂度**：`O(|target|)`  
  只用了一个保存配方的哈希表，最多存放目标字符串中不同字母的数量，最多 10 个。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐字符模拟**，虽然已经是 `O(|s|)`，但我们完全可以用**计数**一次性算出答案，省去逐字符匹配的过程。

关键观察：

- 对每一种字母 `c`，如果 `s` 中出现了 `cnt_s[c]` 次，`target` 中需要 `cnt_t[c]` 次，那么**只能用 `cnt_s[c] // cnt_t[c]`（整数除法）**份 `target` 来使用这些 `c`。
- 整体能拼出的 `target` 副本数受**最稀缺的字母**限制。换句话说，答案是所有字母 `c` 的 `cnt_s[c] // cnt_t[c]` 中的最小值。

实现步骤：

1. 用哈希表（字典）分别统计 `s` 和 `target` 中每个字符的出现次数。  
   - 哈希表就像一本**字典**，`key` 是字母，`value` 是它出现的次数。
2. 对 `target` 中出现的每个字母，计算 `cnt_s[c] // cnt_t[c]`。如果 `s` 中根本没有某个必需字母，则该除法结果为 `0`，答案直接是 `0`。  
3. 取所有除法结果的最小值，即为最大可以拼出的 `target` 副本数。

#### 代码（Python）

```python
from collections import Counter
from math import inf

def maxCopies_optimal(s: str, target: str) -> int:
    # 统计每个字符出现的次数
    cnt_s = Counter(s)          # s 中的字母频率表
    cnt_t = Counter(target)     # target 中的字母频率表

    # 设一个很大的初始值，后面会取最小值
    ans = inf

    # 只需要遍历 target 中出现过的字母
    for ch, need in cnt_t.items():
        have = cnt_s.get(ch, 0)          # s 中该字母的数量，若不存在则为 0
        ans = min(ans, have // need)     # 取最小的可复制次数

    return ans if ans != inf else 0      # 防止 target 为空（题目保证非空）
```

#### 复杂度

- **时间复杂度**：`O(|s| + |target|)`  
  - 统计频率各遍历一次字符串，线性时间。后面遍历 `target` 中的不同字母（最多 10 种），常数时间。整体就是 `O(n + m)`，其中 `n = |s|，m = |target|`。
- **空间复杂度**：`O(Σ)`，这里的 Σ 为字母表大小（固定 26），即 `O(1)` 实际常数空间。我们只用了两个字典来保存字符计数。

> 与暴力解相比，最优解省去了逐字符匹配的过程，直接用数学公式算出答案，时间更快且代码更简洁。

---

## 心得

- **核心技巧**：**字符计数 + 取最小值**。  
  通过统计每个字符出现的次数，利用整数除法求出每种字符能支撑的目标副本数，再取最小值得到最终答案。

- **适用的题型**  
  1. *Maximum Number of Balloons*（1189）——统计气球所需字母的最小可复制次数。  
  2. *Find the Longest Word in Dictionary through Deleting*——统计字符出现次数以判断子序列关系。  
  3. *Construct the Longest Palindrome*——统计字符出现次数决定可以使用的对称字符数量。

- **一句话总结解题钥匙**：**“把目标当配方，算每种材料能做几份，最少的那种决定最终能做多少份”。**

---

## 反思

- **第一反应**：看到“取字母并重新排列”，立刻想到**字母计数**，因为顺序不重要，只要数量足够即可。  
- **最容易踩的坑**  
  - 忘记对 `target` 中不存在于 `s` 的字符返回 `0`（因为 `0 // anything = 0`）。  
  - 忽视整数除法的取整行为，直接用除法得到浮点数会出错。  
  - 当 `target` 包含重复字母（如示例 3 中的 `'a'`）时，必须用 **出现次数** 而不是 **是否出现** 来判断。

- **下次遇到同类题**，第一步应想到：**先统计两边字符出现频率，再用除法求每种字符能支撑的副本数，最后取最小值**。这样可以迅速得到最优解。