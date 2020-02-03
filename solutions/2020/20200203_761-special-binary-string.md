# #761. 特殊二进制字符串 / Special Binary String

> 难度：困难 · 标签：String、Recursion · [LeetCode 链接](https://leetcode.com/problems/special-binary-string/)

---

## 题目（英文原版）

**Description**

Special binary strings are binary strings with the following two properties:
You are given a special binary string s.
A move consists of choosing two consecutive, non-empty, special substrings of s, and swapping them. Two strings are consecutive if the last character of the first string is exactly one index before the first character of the second string.
Return the lexicographically largest resulting string possible after applying the mentioned operations on the string.

**Examples**

**Example 1:**

```
Input: s = "11011000"
Output: "11100100"
Explanation: The strings "10" [occuring at s[1]] and "1100" [at s[3]] are swapped.
This is the lexicographically largest string possible after some number of swaps.
```

**Example 2:**

```
Input: s = "10"
Output: "10"
```

**Constraints**

- 1 <= s.length <= 50
- s[i] is either '0' or '1'.
- s is a special binary string.

---

## 题目（中文翻译）

特殊二进制字符串（special binary strings）是满足以下两个性质的二进制字符串：

给定一个特殊二进制字符串 `s`。

一次操作指选择 `s` 中两个相邻的、非空的特殊子字符串（special substrings），并交换它们。若第一个字符串的最后一个字符恰好位于第二个字符串的第一个字符的前一个位置，则这两个字符串是相邻的。

返回在对字符串进行任意次数上述操作后，能够得到的字典序（lexicographically）最大的字符串。

**示例 1**  
**输入**: `s = "11011000"`  
**输出**: `"11100100"`  
**解释**: 将位于 `s[1]` 的子字符串 `"10"` 与位于 `s[3]` 的子字符串 `"1100"` 交换。经过若干次交换后得到的字符串已经是字典序最大的。

**示例 2**  
**输入**: `s = "10"`  
**输出**: `"10"`

**约束条件**

- `1 <= s.length <= 50`
- `s[i]` 仅为 `'0'` 或 `'1'`。
- `s` 是一个特殊二进制字符串。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目描述的“把两个相邻的特殊子串交换”当成**暴力枚举**：  
1. 先找出字符串 `s` 中所有**相邻的、非空的特殊子串**。  
   - 判断一个子串 `s[l:r]` 是否是特殊的，只要满足：  
     * 子串中 `1` 的个数等于 `0` 的个数（即平衡），  
     * 任意前缀的 `1` 数量都不少于 `0` 的数量（左括号永远不多于右括号），这正好和“合法的括号序列”一一对应。  
   - 为了判断，我们可以在遍历子串时维护一个计数器 `balance`，遇到 `1` 加 1，遇到 `0` 减 1；如果遍历结束时 `balance==0` 且中途从未出现负值，则该子串是特殊的。  
2. 对每一对相邻的特殊子串，**交换**它们得到一个新字符串，然后继续对这个新字符串递归尝试所有可能的交换。  
3. 记录所有能够得到的字符串，返回字典序（lexicographically）最大的那个。

> **生活化类比**：把特殊子串想成“装在盒子里的玩具”。我们要做的就是找出相邻的两个盒子，然后把它们的位置互换。只要盒子里的玩具符合“左手永远不比右手多”的规则（即特殊），我们就可以交换。

这个方法一定能得到答案，因为它遍历了**所有**合法的交换序列，最终的最大字符串必然在其中。

#### 代码（Python）

```python
def is_special(sub: str) -> bool:
    """判断子串是否是 special binary string"""
    bal = 0
    for ch in sub:
        bal += 1 if ch == '1' else -1
        if bal < 0:          # 前缀出现了更多的 0，非法
            return False
    return bal == 0         # 整体平衡才算 special

def brute_max(s: str) -> str:
    """暴力递归搜索所有可能的交换，返回字典序最大的字符串"""
    n = len(s)
    best = s                # 至少可以不做任何交换
    # 枚举所有可能的相邻特殊子串
    for i in range(1, n):
        # 第一个子串是 s[0:i]，第二个子串是 s[i:j]
        for j in range(i + 1, n + 1):
            left, right = s[:i], s[i:j]
            if is_special(left) and is_special(right):
                # 交换后得到的新字符串
                new_s = s[:0] + right + left + s[j:]
                # 继续对 new_s 做递归搜索
                cand = brute_max(new_s)
                if cand > best:      # 字典序比较，'>' 表示更大
                    best = cand
    return best
```

> **注意**：这段代码仅用于演示思路，实际运行会非常慢（指数级），因为会产生大量重复子问题。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）  
  - 解释：每次我们都要在所有可能的切分点上尝试交换，而每一次交换又会产生一个新的子问题。对于长度 `n` 的字符串，可能的子串切分数是 `O(n^2)`，而递归深度最坏情况下是 `O(n)`，于是整体呈指数增长。可以把它想象成“每走一步都有好几条路可以选”，路数会快速翻倍。

- **空间复杂度**：`O(n)`（递归栈）  
  - 只需要保存递归调用的栈帧，最多 `n` 层深度。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈**在于我们对每一次交换都重新遍历整串并递归，导致大量重复计算。其实这道题有一个非常关键的结构特性：**特殊二进制字符串本质上是嵌套的“山峰”（mountain）**，类似合法的括号序列。

**关键观察**  

1. **山峰（mountain）**  
   - 把 `1` 当作向上走一步，`0` 当作向下走一步。  
   - 整个字符串从 `(0,0)` 开始，最终回到 `y=0`，且在除起点终点外从不低于 `0`。  
   - 第一次回到 `y=0` 的位置把字符串划分成一个 **完整的山峰**，它内部可能再嵌套若干子山峰。  

2. **山峰的递归结构**  
   - 一个山峰的形式一定是 `1  (内部) 0`，其中 `内部` 本身仍然是若干**相邻的山峰**的拼接。  
   - 例如 `"11011000"` 可以分解为  
     ```
     1  ( 10 ) 1 ( 10 ) 0 0
     ^  ^^^^  ^  ^^^^  ^ ^
     山峰1   山峰2   山峰3
     ```
     这里最外层是 `1 … 0`，内部是三个山峰 `10、1100、10`（实际划分时会递归处理）。  

3. **交换等价于对相邻山峰重新排序**  
   - 题目允许我们**交换任意相邻的特殊子串**，而相邻的特殊子串恰好对应**相邻的山峰**。  
   - 因此，经过任意次数的交换后，所有山峰的相对顺序可以变成**任意排列**，只要我们保持每个山峰内部的结构不变。  

4. **字典序最大化的策略**  
   - 在字典序比较中，`'1'` 大于 `'0'`，所以我们希望**把“更大的山峰”放在前面**。  
   - “更大的山峰”可以递归地用同样的规则来判断：先把山峰内部再做最大化，然后把得到的结果当作一个整体字符串比较大小。  
   - 因此：**对每个山峰递归求解其最大形式，然后把所有山峰按字典序降序排列**，最后把它们拼接起来，即得到整体的最大字符串。  

5. **递归实现**  
   - 写一个函数 `makeLargest(s)`：  
     1. 用一个计数器 `balance` 找到最外层的每个山峰的结束位置（`balance` 再次回到 `0` 时）。  
     2. 对每个山峰 `segment = s[l:r]`（包括首尾的 `1` 与 `0`），递归求 `makeLargest(segment[1:-1])`（去掉首尾后处理内部），得到 `inner`。  
     3. 当前山峰的最大形式为 `"1" + inner + "0"`。  
     4. 把所有山峰的最大形式放入列表 `parts`，对 `parts` 按字典序逆序（降序）排序。  
     5. 返回 `''.join(parts)`。  

这就是 LeetCode 官方解法的核心思路——**递归 + 排序**。

#### 代码（Python）

```python
def makeLargestSpecial(s: str) -> str:
    """
    返回对特殊二进制字符串 s 进行任意合法交换后能够得到的字典序最大的字符串。
    思路：把 s 分解为若干相邻的“山峰”，递归处理每个山峰内部，再把山峰整体按字典序降序排列。
    """
    parts = []          # 用来存放每个山峰的最大形式
    balance = 0         # balance == 0 时表示回到了当前层的起点
    last = 0            # 上一个山峰的起始下标

    # 扫描整个字符串，找到所有最外层山峰的区间
    for i, ch in enumerate(s):
        balance += 1 if ch == '1' else -1
        # 当 balance 再次回到 0，说明从 last 到 i 形成了一个完整的山峰
        if balance == 0:
            # s[last:i+1] 形如 1 …… 0
            # 去掉首尾的 1、0，对内部递归求解
            inner = makeLargestSpecial(s[last + 1:i])
            # 当前山峰的最大形式是 1 + inner + 0
            parts.append('1' + inner + '0')
            last = i + 1   # 下一段山峰从 i+1 开始

    # 把所有山峰按字典序降序排列，较大的山峰排前面
    parts.sort(reverse=True)
    # 拼接得到整体的最大字符串
    return ''.join(parts)
```

> **代码注释解释**  
> - `balance` 就像在山路上爬坡（`1`）和下坡（`0`），每次回到同一海拔（`0`）就意味着完成了一座山。  
> - `inner = makeLargestSpecial(s[last + 1:i])` 把山峰内部再次拆分、排序，保证内部已经是最大形式。  
> - `parts.sort(reverse=True)` 相当于把“更高的山”搬到左边，字典序自然更大。

#### 复杂度

- **时间复杂度**：`O(n log n)`（其中 `n = len(s)`）  
  - 解释：每一次递归遍历字符串一次来找到山峰的分界，总共遍历的字符数是 `n`。在每层递归结束时，我们对当前层得到的山峰列表 `parts` 进行排序，排序的代价是 `O(k log k)`，`k` 是当前层的山峰数量，且 `k ≤ n/2`。整个递归树的总排序代价累计仍然是 `O(n log n)`。  
  - 与暴力解的指数级不同，这里只需要对每层的子问题做一次线性扫描和一次排序，速度快得多。

- **空间复杂度**：`O(n)`（递归调用栈 + 结果字符串）  
  - 递归的最大深度等于嵌套的层数，最坏情况下是 `n/2`（形如 `"111...000"`），因此使用的栈空间是线性的。返回的字符串本身也占 `O(n)` 空间。

---

## 心得

- **核心技巧**：把特殊二进制字符串看成**嵌套的山峰（合法括号序列）**，利用**递归拆分 + 局部排序**得到全局最优。  
- **适用题型**  
  1. “Make The String Great” 之类的**括号序列重排**问题。  
  2. “Remove Outermost Parentheses” 需要把嵌套结构拆解。  
  3. 任何**递归分治**可以把整体划分为若干相邻子块并对块进行排序的问题（例如 “Largest Number” 按自定义比较排序）。  
- **一句话总结解题钥匙**：**把每个最外层的特殊子串（山峰）先内部最大化，再按字典序逆序排列**。

---

## 反思

- **第一反应**：看到“相邻的特殊子串可以交换”，本能想到**暴力枚举所有交换**，但很快意识到会爆炸。  
- **最容易踩的坑**  
  - **分割山峰的边界**：必须在 `balance` 恰好回到 `0` 时截断，错误的截断会产生非法子串。  
  - **递归的基准情况**：空字符串应直接返回空，否则会导致无限递归。  
  - **排序的方向**：忘记逆序（`reverse=True`）会得到字典序最小的结果。  
- **下次类似题的第一步**：先**把结构抽象成递归的“块”（如括号、山峰）**，判断块之间是否可以自由调换，再**在块内部递归求解**，最后**对块进行合适的排序**。这样往往能把指数级的搜索压缩到线性或 `n log n` 的复杂度。