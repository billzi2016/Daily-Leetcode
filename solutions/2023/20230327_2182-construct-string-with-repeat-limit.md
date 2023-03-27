# #2182. 构造受限重复次数的字符串 / Construct String With Repeat Limit

> 难度：中等 · 标签：Hash Table、String、Greedy、Heap (Priority Queue)、Counting · [LeetCode 链接](https://leetcode.com/problems/construct-string-with-repeat-limit/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer repeatLimit. Construct a new string repeatLimitedString using the characters of s such that no letter appears more than repeatLimit times in a row. You do not have to use all characters from s.
Return the lexicographically largest repeatLimitedString possible.
A string a is lexicographically larger than a string b if in the first position where a and b differ, string a has a letter that appears later in the alphabet than the corresponding letter in b. If the first min(a.length, b.length) characters do not differ, then the longer string is the lexicographically larger one.

**Examples**

**Example 1:**

```
Input: s = "cczazcc", repeatLimit = 3
Output: "zzcccac"
Explanation: We use all of the characters from s to construct the repeatLimitedString "zzcccac".
The letter 'a' appears at most 1 time in a row.
The letter 'c' appears at most 3 times in a row.
The letter 'z' appears at most 2 times in a row.
Hence, no letter appears more than repeatLimit times in a row and the string is a valid repeatLimitedString.
The string is the lexicographically largest repeatLimitedString possible so we return "zzcccac".
Note that the string "zzcccca" is lexicographically larger but the letter 'c' appears more than 3 times in a row, so it is not a valid repeatLimitedString.
```

**Example 2:**

```
Input: s = "aababab", repeatLimit = 2
Output: "bbabaa"
Explanation: We use only some of the characters from s to construct the repeatLimitedString "bbabaa". 
The letter 'a' appears at most 2 times in a row.
The letter 'b' appears at most 2 times in a row.
Hence, no letter appears more than repeatLimit times in a row and the string is a valid repeatLimitedString.
The string is the lexicographically largest repeatLimitedString possible so we return "bbabaa".
Note that the string "bbabaaa" is lexicographically larger but the letter 'a' appears more than 2 times in a row, so it is not a valid repeatLimitedString.
```

**Constraints**

- 1 <= repeatLimit <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `repeatLimit`。使用 `s` 中的字符构造一个新字符串 **受限重复字符串（repeatLimitedString）**，要求同一字母连续出现的次数不能超过 `repeatLimit`。你不必使用 `s` 中的所有字符。返回字典序（lexicographically）最大的可能的 **受限重复字符串（repeatLimitedString）**。

**字典序的比较**  
若字符串 `a` 与字符串 `b` 在首次不同的位置上，`a` 对应的字符在字母表中出现得更靠后，则 `a` 的字典序大于 `b`。若前 `min(a.length, b.length)` 个字符全部相同，则较长的字符串字典序更大。

### 示例

#### 示例 1
**输入**  
``` 
s = "cczazcc", repeatLimit = 3
```  
**输出**  
```
"zzcccac"
```  
**解释**  
我们使用 `s` 中的所有字符构造出受限重复字符串 `zzcccac`。  
- 字母 `'a'` 连续出现至多 **1** 次。  
- 字母 `'c'` 连续出现至多 **3** 次。  
- 字母 `'z'` 连续出现至多 **2** 次。  

因此没有字母的连续出现次数超过 `repeatLimit`，该字符串合法且字典序最大。

#### 示例 2
**输入**  
``` 
s = "aababab", repeatLimit = 2
```  
**输出**  
```
"bbabaa"
```  
**解释**  
我们仅使用 `s` 中的部分字符构造出受限重复字符串 `bbabaa`。  
- 字母 `'a'` 连续出现至多 **2** 次。  
- 字母 `'b'` 连续出现至多 **2** 次。  

同样没有字母的连续出现次数超过 `repeatLimit`，且该字符串在满足条件的所有可能结果中字典序最大。

### 约束条件
- `1 <= repeatLimit <= s.length <= 10^5`
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的排列**，然后挑出满足“相同字符连续出现不超过 `repeatLimit` 次”的子序列，最后取字典序最大的那个。  

- **数据结构**：我们可以把字符放进一个列表 `arr`，用 `itertools.permutations` 生成所有排列。  
- **类比**：把所有字符想象成一副牌，暴力解就是把这副牌的每一种洗牌方式都试一遍，看看哪一种符合规则且最大。  

为什么正确？因为我们遍历了**全部**合法的排列，必然不会错过最优解。  

但这显然不可行——字符个数最多 `10⁵`，全排列的数量是 `n!`，根本不可能在电脑里跑完。

#### 代码（Python）

```python
import itertools

def repeatLimitedString_bruteforce(s: str, repeatLimit: int) -> str:
    best = ""                         # 记录当前找到的字典序最大的合法串
    # 将字符列表化，方便生成排列
    chars = list(s)
    # itertools.permutations 会生成所有 n! 种排列（这里仅作演示，实际会超时）
    for perm in itertools.permutations(chars):
        cur = []
        cnt = 0                       # 当前字符连续出现的次数
        prev = ''                     # 前一个字符
        ok = True
        for ch in perm:
            if ch == prev:
                cnt += 1
            else:
                cnt = 1
                prev = ch
            if cnt > repeatLimit:     # 超过限制，直接放弃这个排列
                ok = False
                break
            cur.append(ch)
        if ok:
            cand = ''.join(cur)
            # 字典序比较，Python 中字符串直接 > 就是字典序比较
            if cand > best:
                best = cand
    return best
```

> **注意**：上述代码仅用于阐明思路，实际运行会因为 `n!` 的爆炸性增长而 **超时** 或 **内存溢出**。

#### 复杂度  

- 时间复杂度：`O(n!)` —— 必须遍历所有排列，随着 `n` 增长极其迅速。  
- 空间复杂度：`O(n)` —— 保存一个排列需要 `n` 的空间。

> **大白话**：`O(n!)` 就像把 10 个球全排列要 3,628,800 种可能，`n=20` 时已经是天文数字，根本不可能在电脑上跑完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**关键瓶颈**在于“每次都要遍历所有字符的所有排列”。  
其实我们只需要**按照字典序从大到小**依次挑选字符，尽量让大字符出现在前面，同时保证同一个字符的连续出现次数不超过 `repeatLimit`。

**核心想法**：

1. 统计每个字符出现的次数（哈希表/数组），这相当于“查字典”，`key` 是字符，`value` 是它的剩余数量。  
2. 从 `'z'` → `'a'` 依次尝试放字符。  
3. 对于当前最大的字符 `c`：  
   - 若它的剩余次数 `cnt[c]` 小于等于 `repeatLimit`，可以一次性全部放入答案。  
   - 若 `cnt[c] > repeatLimit`，我们只能先放 `repeatLimit` 次 `c`，然后**必须插入**一个**次序比 `c` 小的字符**（称为 “调剂字符”）来打断连续。  
   - 插入完调剂字符后，`c` 的剩余次数会继续被放入，循环重复上述过程。  
4. 当没有任何比 `c` 小且还有剩余的字符可供调剂时，**结束**（因为再也无法继续放 `c`，否则会违背限制），此时得到的字符串已经是字典序最大的合法串。

**为什么贪心有效？**  
- 我们总是**先用最大的字符**，因为字典序的比较本质上是“从左到右，看哪个字符更大”。  
- 只在必须打断时才使用次大的字符，**不提前浪费**次大字符的机会。  
- 这种“尽可能多放大字符 → 必要时插入次大字符”的策略保证了局部最优，同时不会影响后面的更小字符的使用，因此可以得到全局最优。

**实现细节**：

- 使用长度为 26 的数组 `cnt[0..25]` 记录每个字母的出现次数（`ord(ch)-ord('a')` 为下标）。  
- 用 **while 循环** 从 `i = 25`（对应 `'z'`）向下遍历。  
- 当 `cnt[i] == 0` 时直接 `i -= 1`，继续找下一个有剩余的字符。  
- 当需要调剂字符时，再从 `j = i-1` 向下寻找第一个 `cnt[j] > 0` 的字符。若找不到（`j < 0`），说明已经无法继续构造，直接退出。

#### 代码（Python）

```python
def repeatLimitedString(s: str, repeatLimit: int) -> str:
    # 1. 统计每个字符出现次数，cnt[0] 对应 'a', cnt[25] 对应 'z'
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    res = []                     # 用列表收集字符，最后 join 成字符串

    i = 25                       # 从最大的字符 'z' 开始尝试
    while i >= 0:
        if cnt[i] == 0:          # 当前字符已经用光，往左找更小的字符
            i -= 1
            continue

        # 这一步决定本轮最多可以连续放多少个当前字符 i
        use = min(cnt[i], repeatLimit)   # 不能超过 repeatLimit，也不能超过剩余次数
        # 把字符 i 放入答案 use 次
        res.append(chr(ord('a') + i) * use)
        cnt[i] -= use

        # 如果已经把所有 i 用完，继续循环即可
        if cnt[i] == 0:
            continue

        # 否则 cnt[i] > 0 且已经达到 repeatLimit，需要插入一个“调剂字符”
        # 在 i 的左侧（字典序更小）寻找第一个还有剩余的字符
        j = i - 1
        while j >= 0 and cnt[j] == 0:
            j -= 1

        if j < 0:                # 没有可以调剂的字符，构造结束
            break

        # 放一个字符 j，打断连续
        res.append(chr(ord('a') + j))
        cnt[j] -= 1

        # 继续下一轮循环，此时 i 仍然指向原来的字符，可能会再放一批
        # （因为已经插入调剂字符，连续限制重新算起）
    return ''.join(res)
```

> **关键注释**  
> - `cnt` 像一本“字典”，`key` 是字母，`value` 是还有多少页（剩余次数）。  
> - `use = min(cnt[i], repeatLimit)` 就是“这本书一次最多只能翻这么多页”。  
> - 当找不到调剂字符 (`j < 0`) 时，相当于“没有更小的字典可以借来填空”，只能提前结束。

#### 复杂度  

- 时间复杂度：`O(26 + n)` ≈ `O(n)`  
  - 统计字符是 `O(n)`，随后最多遍历 26 次字符的循环，每次可能多次插入调剂字符，但每插入一次都消耗掉至少一个字符的计数，整体仍是线性。  
- 空间复杂度：`O(26)` ≈ `O(1)`  
  - 只用了一个固定大小的计数数组和结果列表（结果本身必须占 `O(n)`，不计入额外空间）。

> 与暴力解相比，**从 `O(n!)` 降到了 `O(n)`**，在 10⁵ 长度的输入下也能在毫秒级完成。

---

## 心得

- **核心技巧**：**贪心 + 计数 + “调剂”思路**（把最大的字符尽可能多放，必要时用次大字符打断）。  
- **适用的题型**：  
  1. “构造满足局部约束的最大/最小字典序字符串”——如 *Largest Number After Removing Digits*。  
  2. “在一定次数限制下排列字符”——如 *Rearrange String k Distance Apart*（需要间隔 k）。  
  3. “使用字符计数构造特定模式”——如 *Arrange Characters By Frequency*。  
- **一句话总结**：**把最大的字符尽量往前排，遇到连续上限就“借”下一个可用的次大字符来解闷**。

---

## 反思

- **第一反应**：直接想到“把字符从大到小排”，但忘了连续出现的限制，导致最初的实现会产生非法串。  
- **最容易踩的坑**：  
  - 没有正确处理 **调剂字符用完** 的情况，会导致无限循环或错误结果。  
  - 忽略了 **repeatLimit 可能大于字符总数**，此时直接输出全部字符即可。  
  - 计数数组下标与字符之间的转换错误（`ord('a')` 与 `ord('z')` 的偏移）。  
- **下次类似题目**：第一步先 **统计字符出现次数**，然后 **从字典序最大的字符开始贪心尝试**，一旦触发局部约束，就 **立刻寻找最近的次大字符** 作为“调剂”。如果调剂找不到，就可以直接结束。这样思路清晰，代码实现也更稳健。