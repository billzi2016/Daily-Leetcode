# #3517. 最小回文重排 I / Smallest Palindromic Rearrangement I

> 难度：中等 · 标签：String、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/smallest-palindromic-rearrangement-i/)

---

## 题目（英文原版）

**Description**

You are given a palindromic string s.
Return the lexicographically smallest palindromic permutation of s.

**Examples**

**Example 1:**

```
Input: s = "z"
Output: "z"
Explanation:
A string of only one character is already the lexicographically smallest palindrome.
```

**Example 2:**

```
Input: s = "babab"
Output: "abbba"
Explanation:
Rearranging "babab" → "abbba" gives the smallest lexicographic palindrome.
```

**Example 3:**

```
Input: s = "daccad"
Output: "acddca"
Explanation:
Rearranging "daccad" → "acddca" gives the smallest lexicographic palindrome.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.
- s is guaranteed to be palindromic.

---

## 题目（中文翻译）

你得到一个回文（palindromic）字符串 `s`。  
返回 `s` 所有可能的回文排列（palindromic permutation）中，字典序（lexicographically）最小的那个。

**示例 1**  
**输入**: `s = "z"`  
**输出**: `"z"`  
**解释**: 仅有一个字符的字符串本身已经是字典序最小的回文。

**示例 2**  
**输入**: `s = "babab"`  
**输出**: `"abbba"`  
**解释**: 将 `"babab"` 重新排列为 `"abbba"` 可得到字典序最小的回文。

**示例 3**  
**输入**: `s = "daccad"`  
**输出**: `"acddca"`  
**解释**: 将 `"daccad"` 重新排列为 `"acddca"` 可得到字典序最小的回文。

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。  
- `s` 已保证是回文。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接、最笨的想法是**把所有可能的排列都列出来**，然后挑出其中既是回文又字典序最小的那个。  
- **数据结构**：我们可以把字符串当成一个字符数组，使用 `itertools.permutations` 生成全排列。  
- **类比**：把字符看成一副扑克牌，暴力解相当于把这副牌所有的洗牌方式都尝试一次，再检查每一种洗出来的牌面是否满足“左半边和右半边相同”（回文），以及它在字典序上是否最靠前。  
- **正确性**：因为我们枚举了**所有**合法的排列，答案必然在其中；只要我们把符合回文条件的排列挑出来，再取字典序最小的那一个，就是题目的要求。  

显然，这种方法只适合长度非常小的字符串（比如 `n ≤ 8`），因为全排列的数量是 `n!`，会非常爆炸。  

#### 代码（Python）  

```python
import itertools

def smallest_palindrome_bruteforce(s: str) -> str:
    # 1. 生成所有排列（会产生大量重复，需要去重）
    perms = set(itertools.permutations(s))          # set 去掉相同排列
    best = None

    for p in perms:
        cand = ''.join(p)                           # 把元组转回字符串
        # 2. 判断是否是回文
        if cand == cand[::-1]:                      # 字符串翻转后相等即为回文
            # 3. 更新字典序最小的答案
            if best is None or cand < best:
                best = cand
    return best
```

> **注意**：上述代码只能在极小规模的测试里跑通，实际提交会超时甚至内存炸掉。

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是全排列的个数，`n` 是每次检查回文和比较字典序时需要遍历字符串的长度。  
  - 用大白话说，就是“先把所有可能的洗牌方式都尝试一次（爆炸性增长），每次都要把整副牌翻一遍”。  
- **空间复杂度**：`O(n! * n)` 用于存放所有不同的排列，同样是爆炸性的。

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们发现 **瓶颈** 在于**枚举所有排列**，而实际上我们只需要 **构造一个满足条件的排列**，不必穷举。  
回文字符串的结构非常特殊：  
```
left_half + middle? + reverse(left_half)
```
- `left_half` 是左侧的字符序列（长度为 `len(s)//2`），  
- `middle?` 只在字符总数为奇数时出现，它是唯一可以单独放在中间的字符。  

因为题目保证原字符串本身已经是回文的，所以字符的出现次数一定满足：  
- **偶数个**的字符可以全部成对出现，分别放在左右两侧。  
- **奇数个**的字符至多只有 **一个**（因为总长度为奇数时才会出现），它必须位于中间。  

要得到**字典序最小**的回文，只需要让 `left_half` **尽可能从小到大排**。这相当于：

1. 统计每个字符出现的次数（类似查字典，字符是“词”，出现次数是“页码”）。  
2. 对每个字符 `c`：  
   - 把 `cnt[c] // 2` 个 `c` 放进 `left_half`（因为每对字符各占左、右各一个）。  
   - 如果 `cnt[c]` 是奇数且我们还没有确定 `middle`，把剩下的一个 `c` 设为 `middle`。  
3. `left_half` 按字符 **升序** 拼接得到最小的左半边。  
4. 最终答案 = `left_half` + `middle`（可能为空） + `reverse(left_half)`。  

这一步只遍历一次字符串计数，随后遍历 26 个英文字母（固定常数），所以时间线性且非常快。  

**核心算法**：计数 + 构造（相当于一种“计数排序”），不涉及复杂的数据结构。  

#### 代码（Python）  

```python
def smallest_palindrome(s: str) -> str:
    # 1. 统计每个字符出现次数（哈希表像查字典，key 是字符，value 是出现次数）
    cnt = [0] * 26                     # 只包含小写英文字母，长度固定 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1   # ord('a') 是基准，把字符映射到 0~25

    left_half = []                     # 用列表收集左半边字符，后面会 join 成字符串
    middle = ''                        # 中间字符，默认空字符串

    # 2. 按字母顺序遍历，确保 left_half 从小到大
    for i in range(26):
        c = chr(ord('a') + i)          # 当前字符，例如 i=0 时是 'a'
        times = cnt[i]

        # 2.1 把成对的字符放进左半边
        pairs = times // 2
        if pairs:
            left_half.append(c * pairs)   # 例如 'b' 出现 4 次，则 pairs=2，放入 "bb"

        # 2.2 处理可能的奇数个字符（只会出现一次）
        if times % 2 == 1 and middle == '':
            middle = c                    # 第一个出现奇数次的字符就是中间字符

    # 3. 把左半边拼成字符串（已经是升序），再拼出完整回文
    left = ''.join(left_half)            # 例如 ['a', 'bb'] -> "abb"
    right = left[::-1]                   # 右半边是左半边的逆序
    return left + middle + right
```

> **运行示例**  
> ```python
> print(smallest_palindrome("z"))        # z
> print(smallest_palindrome("babab"))    # abbba
> print(smallest_palindrome("daccad"))   # acddca
> ```

#### 复杂度  

- **时间复杂度**：`O(n + 26)` → 简写为 `O(n)`  
  - 第一次遍历字符串计数是 `O(n)`，`n` 是字符串长度（最多 10⁵）。  
  - 后面遍历 26 个字母是常数时间。  
  - 用大白话说，就是“只需要走一遍字符串，随后再看一遍字母表”。  
- **空间复杂度**：`O(26)` → 简写为 `O(1)`（常数空间）  
  - 只用了一个长度为 26 的计数数组和若干临时字符串，和输入规模无关。

---

## 心得  

- **核心技巧**：利用回文的对称结构，把问题转化为“如何把字符按字典序排好左半边”。  
- **适用的题型**：  
  1. “最小字典序的回文重排”系列（如本题、`Smallest Palindromic Rearrangement II`）。  
  2. “能否重排成回文”类问题（只需检查奇数次数字符的个数）。  
  3. “字符计数 + 排序” 的字符串重排问题（如按字典序输出所有可能的排列的第一种）。  
- **一句话总结**：**把所有字符配对，左半边从小到大排，剩下的唯一奇数字符放中间**，即可得到字典序最小的回文。

---

## 反思  

- **第一反应**：看到“回文”二字，我马上想到“左右对称”。于是想到把字符计数后配对，这比直接枚举要省很多力气。  
- **最容易踩的坑**：  
  - 忘记处理 **奇数长度** 时的中间字符，导致生成的字符串不是合法回文。  
  - 在构造左半边时没有保证升序，导致得到的回文不是字典序最小。  
  - 计数数组越界或字符映射错误（如 `ord(ch) - ord('a')` 写错）。  
- **下次遇到同类题**，第一步应该**统计字符出现次数**，并思考**回文的对称配对**如何决定每个字符应该放在哪个位置。这样可以快速定位最优构造方案，避免盲目枚举。