# #3304. 字符串游戏 I 中的第 K 个字符 / Find the K-th Character in String Game I

> 难度：简单 · 标签：Math、Bit Manipulation、Recursion、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-k-th-character-in-string-game-i/)

---

## 题目（英文原版）

**Description**

Alice and Bob are playing a game. Initially, Alice has a string word = "a".
You are given a positive integer k.
Now Bob will ask Alice to perform the following operation forever:
For example, performing the operation on "c" generates "cd" and performing the operation on "zb" generates "zbac".
Return the value of the kth character in word, after enough operations have been done for word to have at least k characters.

**Examples**

**Example 1:**

```
Input: k = 5
Output: "b"
Explanation:
Initially, word = "a" . We need to do the operation three times:
```

**Example 2:**

```
Input: k = 10
Output: "c"
```

**Constraints**

- 1 <= k <= 500

---

## 题目（中文翻译）

Alice 和 Bob 正在玩一个游戏。最初，Alice 拥有字符串 `word = "a"`。  
给定一个正整数 `k`。  

接下来，Bob 会让 Alice 永久地执行以下 **操作（operation）**：

- 对当前的 `word`，将每个字符的后继字符（即字母表中的下一个字符，`'z'` 的后继是 `'a'`）依次拼接在 `word` 的末尾，形成新的 `word`。

例如，对 `"c"` 执行一次操作会得到 `"cd"`；对 `"zb"` 执行一次操作会得到 `"zbac"`（因为 `"z"` 的后继是 `'a'`，`"b"` 的后继是 `'c'`，于是得到 `"zb"` + `"ac"`）。

在 `word` 的长度至少达到 `k` 之后，返回第 `k` 个 **字符（character）** 的值。

**示例 1**  
```
Input: k = 5
Output: "b"
Explanation:
最初 word = "a"。我们需要进行三次操作：
1 次后: "ab"
2 次后: "abac"
3 次后: "abacaba"
此时第 5 个字符是 'b'，因此返回 "b"。
```

**示例 2**  
```
Input: k = 10
Output: "c"
Explanation:
经过足够次数的操作后，得到的字符串前 10 个字符为 "abacabadab"，第 10 个字符是 'c'，因此返回 "c"。
```

**约束条件**  
- `1 <= k <= 500`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出的“操作”可以这样理解：

1. **把当前字符串**记为 `s`。  
2. **生成 `next(s)`**：把 `s` 中的每个字符都往后推一个字母（`z → a`），得到一个新串。  
3. **新字符串 = 旧字符串 + `next(s)`**。  

> **类比**：把 `s` 看成一本词典的“词”，`next(s)` 就像在词典后面附加了一页“相邻词”。我们把旧页和新页拼在一起，得到更长的书。

举例  
- `s = "c"` → `next(s) = "d"` → 新串 `"cd"`  
- `s = "zb"` → `next(s) = "ac"` → 新串 `"zbac"`

从 `"a"` 开始不断做这个操作，字符串的长度每次都会 **翻倍**（`1 → 2 → 4 → 8 …`），所以只要把它模拟到长度 ≥ k，就能直接取第 k 个字符。

**为什么一定对？**  
因为每一步的定义都是唯一的，模拟的过程恰好就是题目描述的“足够多次操作”。当长度已经够大时，后面的字符不会再影响前 k 位，所以直接读取即可。

#### 代码（Python）

```python
def kth_character_bruteforce(k: int) -> str:
    # 初始字符串
    s = "a"

    # 辅助函数：把字符往后推一位，z→a
    def nxt(ch: str) -> str:
        return 'a' if ch == 'z' else chr(ord(ch) + 1)

    # 只要长度不够，就继续做“操作”
    while len(s) < k:                     # 循环直到长度 ≥ k
        # 生成 next(s)
        next_part = "".join(nxt(c) for c in s)  # 把每个字符都向后推
        s = s + next_part                       # 旧串 + 新串

    # Python 的索引从 0 开始，k 是第几位（从 1 开始），所以要 -1
    return s[k - 1]
```

#### 复杂度

- **时间复杂度**：`O(k)`  
  - 每一次扩展把字符串长度翻倍，最终长度会稍微超过 `k`，所以总共拼接的字符数大约是 `k`（比如 `k=500` 时最多拼接 511 个字符），即线性时间。  
- **空间复杂度**：`O(k)`  
  - 需要把整条字符串保存在内存中，最坏情况下长度接近 `k`。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于把整条字符串都保存在内存里，实际上我们只关心第 k 位的字符，不需要整个序列。观察生成过程可以发现一种递归/二分的规律：

- 设第 `i` 次操作后字符串长度为 `L = 2^i`（因为每次翻倍）。
- 第 `L/2` 前半段就是上一次的完整字符串 `s`。  
- 第 `L/2` 后半段是 `next(s)`，即把前半段每个字符都往后推一位。

因此，对于任意位置 `k`（1‑based）：

| k 的奇偶性 | 该位置对应的字符来源 |
|------------|-------------------|
| **奇数**   | 与 `k` 对应的 **前一次** 位置 ` (k+1)//2` 完全相同（因为它位于前半段） |
| **偶数**   | 与 `k/2` 位置的字符相同，只是 **再往后推一位**（因为它位于后半段） |

把这个规则不断往上追溯，最终会回到最初的字符 `'a'`（第 1 位）。在追溯的过程中，每次走到 **偶数** 分支就意味着要把字符向后推一次。只要统计从根到叶子路径上走过多少次偶数分支，即可得到最终字符。

> **类比**：把这个过程想象成在一棵完全二叉树里找叶子。根节点是 `'a'`，左子树不变，右子树是“往后推一位”。沿路左转（奇数）不改变字符，右转（偶数）把字符往后推一格。最终字符 = `'a'` +（右转次数） mod 26。

**实现方式**（迭代）：

1. `cnt = 0` 用来记录走过的偶数分支次数。  
2. 当 `k > 1` 时：  
   - 若 `k` 为偶数，`cnt += 1`（需要往后推一次）。  
   - 把 `k` 整除 2，继续向上一层看。  
3. 最后字符 = `'a'` 往后推 `cnt` 步（模 26 循环）。

这样只用了 **对数次数**（因为每次都把 `k` 除以 2），时间 `O(log k)`，空间 `O(1)`。

#### 代码（Python）

```python
def kth_character_opt(k: int) -> str:
    """
    在不构造完整字符串的前提下，直接算出第 k 位字符。
    思路：每次把 k 除以 2，统计走过多少次“偶数”分支。
    """
    shift = 0                     # 需要向后推的次数

    while k > 1:                  # 只要还不是根节点，就继续向上回溯
        if k % 2 == 0:            # 偶数 → 该位在 next(s) 中，需要再往后推一次
            shift += 1
        k //= 2                   # 往上一层看（对应前一次操作的字符位置）

    # 最终字符 = 'a' 往后推 shift 步，循环 26 次回到 'a'
    base = ord('a')
    result_char = chr(base + (shift % 26))
    return result_char
```

#### 复杂度

- **时间复杂度**：`O(log k)`  
  - 每一步把 `k` 除以 2，最多需要 `log2(k)` 次循环。对比暴力的 `O(k)`，快了几个数量级。  
- **空间复杂度**：`O(1)`  
  - 只用几个整数变量，和 `k` 的大小无关。

---

## 心得

- **核心技巧**：利用字符串长度每次翻倍的特性，把查询过程转化为 **二进制递归**（或“树的路径”）的问题。  
- **适用的题型**  
  1. “Kth Symbol in Grammar”（LeetCode 779）——同样利用奇偶分支决定取值。  
  2. “Find K-th Bit in Nth Binary String”（LeetCode 1545）——字符串同样是递归拼接的。  
  3. “K-th Smallest in Infinite Sorted Array” 类似的二分/递归技巧。  
- **一句话总结**：**把“不断翻倍的序列”看成一棵二叉树，奇数左走不变，偶数右走加一，即可在对数时间内定位第 k 位字符。**

---

## 反思

- **第一反应**：看到“每次操作把字符串长度翻倍”，立刻想到可以直接模拟直到够长——这就是暴力解。  
- **最容易踩的坑**  
  - **字符循环**：`z` 往后推应回到 `a`，需要取模 26。  
  - **下标偏差**：题目使用 1‑based 下标，代码里要注意 `k-1` 与 `k` 的对应关系。  
  - **边界条件**：`k = 1` 时直接返回 `'a'`，否则递归/循环会无限。  
- **下次遇到同类题**：第一步先判断**是否真的需要完整构造**，如果字符串长度有明确的指数增长规律，就尝试**从二进制/递归视角**直接推导答案。这样往往能把时间从线性降到对数。