# #2746. 递减字符串拼接 / Decremental String Concatenation

> 难度：中等 · 标签：Array、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/decremental-string-concatenation/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array words containing n strings.
Let's define a join operation join(x, y) between two strings x and y as concatenating them into xy. However, if the last character of x is equal to the first character of y, one of them is deleted.
For example join("ab", "ba") = "aba" and join("ab", "cde") = "abcde".
You are to perform n - 1 join operations. Let str0 = words[0]. Starting from i = 1 up to i = n - 1, for the ith operation, you can do one of the following:
Your task is to minimize the length of strn - 1.
Return an integer denoting the minimum possible length of strn - 1.

**Examples**

**Example 1:**

```
Input: words = ["aa","ab","bc"]
Output: 4
Explanation: In this example, we can perform join operations in the following order to minimize the length of str2: 
str0 = "aa"
str1 = join(str0, "ab") = "aab"
str2 = join(str1, "bc") = "aabc" 
It can be shown that the minimum possible length of str2 is 4.
```

**Example 2:**

```
Input: words = ["ab","b"]
Output: 2
Explanation: In this example, str0 = "ab", there are two ways to get str1: 
join(str0, "b") = "ab" or join("b", str0) = "bab". 
The first string, "ab", has the minimum length. Hence, the answer is 2.
```

**Example 3:**

```
Input: words = ["aaa","c","aba"]
Output: 6
Explanation: In this example, we can perform join operations in the following order to minimize the length of str2: 
str0 = "aaa"
str1 = join(str0, "c") = "aaac"
str2 = join("aba", str1) = "abaaac"
It can be shown that the minimum possible length of str2 is 6.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 50
- Each character in words[i] is an English lowercase letter

---

## 题目（中文翻译）

你得到一个下标从 0 开始的字符串数组 `words`，长度为 `n`。  
我们定义一种连接操作 `join(x, y)`，它把两个字符串 `x` 与 `y` 连接成 `xy`。但如果 `x` 的最后一个字符恰好等于 `y` 的第一个字符，则会删除其中的一个该字符，只保留一次。  

例如 `join("ab", "ba") = "aba"`，而 `join("ab", "cde") = "abcde"`。  

接下来需要进行 `n‑1` 次 `join` 操作。记 `str₀ = words[0]`。从 `i = 1` 到 `i = n‑1`，第 `i` 次操作可以任选以下两种方式之一：

* `strᵢ = join(strᵢ₋₁, words[i])`  
* `strᵢ = join(words[i], strᵢ₋₁)`

你的目标是使最终得到的 `str_{n‑1}` 的长度最小。返回一个整数，表示 `str_{n‑1}` 的最小可能长度。

---

### 示例

#### 示例 1  
**输入**: `words = ["aa","ab","bc"]`  
**输出**: `4`  
**解释**:  
可以按如下顺序进行连接，以最小化 `str₂` 的长度：  
```
str₀ = "aa"
str₁ = join(str₀, "ab") = "aab"
str₂ = join(str₁, "bc") = "aabc"
```  
可以证明 `str₂` 的最小可能长度是 `4`。

#### 示例 2  
**输入**: `words = ["ab","b"]`  
**输出**: `2`  
**解释**:  
此时 `str₀ = "ab"`，得到 `str₁` 有两种方式：  
* `join(str₀, "b") = "ab"`  
* `join("b", str₀) = "bab"`  

长度最短的是 `"ab"`，因此答案为 `2`。

#### 示例 3  
**输入**: `words = ["aaa","c","aba"]`  
**输出**: `6`  
**解释**:  
可以按如下顺序进行连接，以最小化 `str₂` 的长度：  
```
str₀ = "aaa"
str₁ = join(str₀, "c") = "aaac"
str₂ = join("aba", str₁) = "abaaac"
```  
可以证明 `str₂` 的最小可能长度是 `6`。

---

### 约束条件
- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 50`
- `words[i]` 中的每个字符都是英文小写字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举每一次加入时是把新单词放在左边还是右边**。  
- 第 `0` 步，`str0 = words[0]` 固定。  
- 第 `i (≥1)` 步，有两种选择：  

| 选择 | 结果字符串 | 说明 |
|------|------------|------|
| **左侧** `join(words[i], str{i-1})` | 把 `words[i]` 放到当前字符串的最前面 | 只要看 `words[i]` 的**最后一个字符**和 `str{i‑1}` 的**第一个字符**是否相同，就决定是否要删掉一个字符 |
| **右侧** `join(str{i-1}, words[i])` | 把 `words[i]` 放到当前字符串的最后面 | 只要看 `str{i‑1}` 的**最后一个字符**和 `words[i]` 的**第一个字符**是否相同，同理决定是否删字符 |

把所有选择列出来，一共会有 `2^(n‑1)` 种不同的拼接顺序。  
我们可以用递归（或 BFS）把每一种情况都走一遍，最后取最小的长度。

> **类比**：想象你手里有一根绳子，每次要把另一段绳子接上去，接法只有两种——左接或右接。要找出所有可能的接法并记录最终绳子的长度，就是暴力搜索。

> **为什么正确**：因为我们把 **所有** 合法的操作序列都尝试了一遍，最小值自然不会错过。

#### 代码（Python）

```python
from typing import List

def join_len(x_len: int, x_last: str, y_len: int, y_first: str) -> int:
    """返回把 x 放左边，y 放右边后的长度（只关心长度，不保存实际字符串）"""
    # 如果最后字符与首字符相同，删掉一个字符
    return x_len + y_len - (1 if x_last == y_first else 0)

def brute(words: List[str]) -> int:
    n = len(words)

    # 递归枚举第 i 步是左接还是右接
    def dfs(i: int, cur_len: int, cur_first: str, cur_last: str) -> int:
        if i == n:                     # 所有单词都已经用了
            return cur_len
        w = words[i]
        w_len, w_first, w_last = len(w), w[0], w[-1]

        # 方案 1：把 w 放到右边
        len_right = join_len(cur_len, cur_last, w_len, w_first)
        best = dfs(i + 1, len_right, cur_first, w_last)

        # 方案 2：把 w 放到左边
        len_left = join_len(w_len, w_last, cur_len, cur_first)
        best = min(best, dfs(i + 1, len_left, w_first, cur_last))
        return best

    first, last = words[0][0], words[0][-1]
    return dfs(1, len(words[0]), first, last)
```

> 代码里只记录**长度、首字符、尾字符**，而不真的拼接字符串，省掉了大量无意义的字符拷贝。  

#### 复杂度  

- **时间复杂度**：`O(2^(n-1))`  
  每一步都有两种选择，树的深度是 `n‑1`，所以总共会遍历 `2^(n-1)` 条路径。  
  对于 `n = 1000`（题目最大）根本不可行——这就是暴力解的“瓶颈”。  
- **空间复杂度**：`O(n)`（递归栈深度）  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正影响后续拼接的只有当前字符串的首字符、尾字符以及长度**，而不是完整的字符串内容。  
因此我们可以把“状态”压缩为三元组 `(first, last, length)`，并对每一步使用 **动态规划**（DP）来保存所有可能的 `(first, last)` 对应的最短长度。

**状态定义**  
`dp[i][a][b]` = 使用前 `i`（含）个单词后，得到的字符串 **首字符是 `a`、尾字符是 `b`** 时的**最小长度**。  
这里 `a、b` 取值为 `'a'..'z'`（共 26 种），可以用整数 `0..25` 代替。

**初始状态**  
`i = 0`（只用第 0 个单词）  
```
a = words[0][0]          # 首字符
b = words[0][-1]         # 尾字符
dp[0][a][b] = len(words[0])
```

**转移**  
设第 `i` 步我们要加入单词 `w = words[i]`，记  
```
f = w[0]          # w 的首字符
l = w[-1]         # w 的尾字符
len_w = len(w)
```
对于所有已经存在的状态 `(first, last)`（即 `dp[i-1][first][last]` 有值）：

1. **右侧加入** `join(str, w)`  
   - 新的首字符仍是 `first`，新的尾字符是 `l`。  
   - 长度增加 `len_w`，如果 `last == f` 则多减 1。  
   ```
   new_len = dp[i-1][first][last] + len_w - (1 if last == f else 0)
   dp[i][first][l] = min(dp[i][first][l], new_len)
   ```

2. **左侧加入** `join(w, str)`  
   - 新的首字符是 `f`，尾字符仍是 `last`。  
   - 长度增加 `len_w`，如果 `l == first` 则多减 1。  
   ```
   new_len = dp[i-1][first][last] + len_w - (1 if l == first else 0)
   dp[i][f][last] = min(dp[i][f][last], new_len)
   ```

因为每一步只关心前一步的结果，我们可以把二维表 `dp` **滚动**，只保留上一轮和当前轮，进一步把空间降到 `26 × 26`。

**答案**  
遍历 `dp[n-1]` 中所有 `first、last`，取最小的长度即为答案。

**为什么快**  
- 每一步只遍历 `26 × 26 = 676` 种首尾组合，时间是 `O(n * 676) ≈ O(n)`。  
- 只保存长度，不保存完整字符串，空间是常数级 `O(26²)`。

> **类比**：把每一次“左/右”拼接看成一次“状态转移”。我们不必记住整根绳子长什么样，只要记住绳子两端的颜色（字符）以及当前的长度，就能决定下一次怎么接。

#### 代码（Python）

```python
from typing import List

INF = 10 ** 9                     # 足够大的数，表示不可达

def minLength(words: List[str]) -> int:
    # 将字符转成 0~25 的索引，方便数组下标
    def idx(ch: str) -> int:
        return ord(ch) - ord('a')

    # dp[a][b] = 当前字符串首字符为 a，尾字符为 b 时的最小长度
    dp = [[INF] * 26 for _ in range(26)]

    first = idx(words[0][0])
    last  = idx(words[0][-1])
    dp[first][last] = len(words[0])          # 初始状态

    # 逐个处理后面的单词
    for w in words[1:]:
        f = idx(w[0])          # w 的首字符索引
        l = idx(w[-1])         # w 的尾字符索引
        wl = len(w)

        # 新一轮的 dp，先全部置为 INF
        ndp = [[INF] * 26 for _ in range(26)]

        for a in range(26):          # a = 当前字符串的首字符
            for b in range(26):      # b = 当前字符串的尾字符
                cur = dp[a][b]
                if cur == INF:       # 该状态不存在，直接跳过
                    continue

                # 方案 1：把 w 加到右边 -> 新的尾字符是 l
                add_len = cur + wl - (1 if b == f else 0)
                if add_len < ndp[a][l]:
                    ndp[a][l] = add_len

                # 方案 2：把 w 加到左边 -> 新的首字符是 f
                add_len = cur + wl - (1 if l == a else 0)
                if add_len < ndp[f][b]:
                    ndp[f][b] = add_len

        dp = ndp                     # 翻到下一轮

    # 最终答案：遍历所有 (first,last) 组合取最小值
    ans = INF
    for a in range(26):
        for b in range(26):
            ans = min(ans, dp[a][b])
    return ans
```

> 代码中的每一行都有中文注释，帮助初学者快速对应到思路。

#### 复杂度  

- **时间复杂度**：`O(n * 26 * 26) = O(n)`  
  解释：对每个单词我们遍历所有可能的首尾字符组合（共 676 种），每种组合只做常数次计算。相比暴力的指数级，这相当于把 “2 的 n 次方” 降到了 “n”。  
- **空间复杂度**：`O(26 * 26) = O(1)`（常数空间）  
  只保存两张 26×26 的表，和输入规模无关。

---

## 心得

- **核心技巧**：把问题抽象为 **“只关心首字符、尾字符和长度的状态”**，并用 **动态规划** 在每一步更新最短长度。  
- **适用的题型**  
  1. 需要在序列中“左/右”拼接或插入，且拼接代价只和两端字符有关（如本题）。  
  2. “合并字符串/数组” 时只关心**边界信息**（首/尾、最大/最小）而非完整内容的 DP。  
  3. 类似的“环形/链式合并”问题，如 **字符串消除**、**字符链路合并** 等。  
- **一句话总结**：**把整个字符串压缩成 “首字符、尾字符、当前最短长度” 三元组，就能用 O(n) 的 DP 求最优**。

---

## 反思

- **第一反应**：看到可以左接或右接，立刻想到 **枚举 2^(n‑1) 种情况**，这就是暴力思路。  
- **最容易踩的坑**  
  1. **忘记更新首字符/尾字符**：左接时首字符要换成新单词的首字符，右接时尾字符要换成新单词的尾字符。  
  2. **漏掉相同字符的削减**：只有当“左端的最后字符 == 右端的首字符”时才减 1，方向要对应好。  
  3. **边界条件**：`words` 长度可能为 1，此时直接返回 `len(words[0])`。  
- **下次类似题的第一步**：先思考**哪些信息在后续操作中仍然会被使用**（本题是首、尾字符），把不必要的细节丢掉，构造一个**状态压缩**的 DP。这样往往能把指数级搜索降到多项式时间。