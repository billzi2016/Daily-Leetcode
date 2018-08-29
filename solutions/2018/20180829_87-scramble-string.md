# #87. 扰乱字符串 / Scramble String

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/scramble-string/)

---

## 题目（英文原版）

**Description**

We can scramble a string s to get a string t using the following algorithm:
Given two strings s1 and s2 of the same length, return true if s2 is a scrambled string of s1, otherwise, return false.

**Examples**

**Example 1:**

```
Input: s1 = "great", s2 = "rgeat"
Output: true
Explanation: One possible scenario applied on s1 is:
"great" --> "gr/eat" // divide at random index.
"gr/eat" --> "gr/eat" // random decision is not to swap the two substrings and keep them in order.
"gr/eat" --> "g/r / e/at" // apply the same algorithm recursively on both substrings. divide at random index each of them.
"g/r / e/at" --> "r/g / e/at" // random decision was to swap the first substring and to keep the second substring in the same order.
"r/g / e/at" --> "r/g / e/ a/t" // again apply the algorithm recursively, divide "at" to "a/t".
"r/g / e/ a/t" --> "r/g / e/ a/t" // random decision is to keep both substrings in the same order.
The algorithm stops now, and the result string is "rgeat" which is s2.
As one possible scenario led s1 to be scrambled to s2, we return true.
```

**Example 2:**

```
Input: s1 = "abcde", s2 = "caebd"
Output: false
```

**Example 3:**

```
Input: s1 = "a", s2 = "a"
Output: true
```

**Constraints**

- s1.length == s2.length
- 1 <= s1.length <= 30
- s1 and s2 consist of lowercase English letters.

---

## 题目（中文翻译）

我们可以使用如下算法对字符串 `s` 进行扰乱（scramble），得到字符串 `t`。  
给定两个等长字符串 `s1` 和 `s2`，如果 `s2` 是 `s1` 的扰乱字符串，则返回 `true`；否则返回 `false`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `s1.length == s2.length`
- `1 <= s1.length <= 30`
- `s1` 和 `s2` 仅由小写英文字母组成。

---

### 示例

#### 示例 1
```
Input: s1 = "great", s2 = "rgeat"
Output: true
Explanation: 对 `s1` 可能的扰乱过程如下：
"great" → "gr/eat"               // 在任意位置划分为两个子串（substrings）。
"gr/eat" → "gr/eat"               // 随机决定不交换两个子串，保持顺序不变。
"gr/eat" → "g/r / e/at"           // 对两个子串递归应用相同的算法，各自再随意划分。
"g/r / e/at" → "r/g / e/at"       // 随机决定交换第一个子串，第二个子串保持顺序不变。
"r/g / e/at" → "r/g / e/a/t"      // 再次递归，对 "at" 划分为 "a/t"。
"r/g / e/a/t" → "r/g / e/a/t"     // 随机决定两个子串都保持原顺序。
此时算法结束，得到的结果字符串为 "rgeat"，即 `s2`。  
因为存在一种可能的情形使 `s1` 被扰乱得到 `s2`，所以返回 `true`。
```

#### 示例 2
```
Input: s1 = "abcde", s2 = "caebd"
Output: false
```

#### 示例 3
```
Input: s1 = "a", s2 = "a"
Output: true
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目描述的“递归分割、可交换”过程直接翻译成代码：

1. **把字符串 s1 在任意位置切成两段**（切分点 `i` 可以是 `1 … len-1`）。  
2. 对这两段分别继续判断是否能变成对应的 s2 的两段。  
3. 有两种可能的对应方式  
   * **不交换**：左边对应左边，右边对应右边。  
   * **交换**：左边对应右边，右边对应左边。  

如果任意一次切分下，上面的两种对应方式有一种全部成立，就说明 s2 是 s1 的 scramble。

> **类比**：把字符串想象成一根绳子，你可以在任意位置把它剪成两段，然后把这两段再继续剪，最后可以把两段的顺序调换。只要有一种剪法和调换方式可以得到目标绳子，就算成功。

递归的 **终止条件** 很简单：  
- 长度为 1 时，只要两个字符相等就返回 `True`，不相等返回 `False`。  
- 两个字符串整体字符种类不一样（比如出现的字母频次不同），直接返回 `False`，因为无论怎么切都不可能匹配。

> 这个检查相当于先把 “字典” 拿出来查一下：如果两段的字母集合不相同，就不用继续深挖了。

#### 代码（Python）

```python
def isScramble_brute(s1: str, s2: str) -> bool:
    # 递归函数，判断 s1[l1:r1] 是否可以 scramble 成 s2[l2:r2]
    def helper(l1: int, r1: int, l2: int, r2: int) -> bool:
        # 取子串
        sub1 = s1[l1:r1]
        sub2 = s2[l2:r2]

        # 1）长度为 1，直接比较字符
        if r1 - l1 == 1:
            return sub1 == sub2

        # 2）字母频次不同，提前剪枝
        if sorted(sub1) != sorted(sub2):   # 这里用 sorted 代替哈希表统计
            return False

        length = r1 - l1
        # 3）尝试所有可能的切分点
        for cut in range(1, length):      # cut 为左子串的长度
            # 不交换的情况
            if (helper(l1, l1 + cut, l2, l2 + cut) and
                helper(l1 + cut, r1, l2 + cut, r2)):
                return True
            # 交换的情况
            if (helper(l1, l1 + cut, r2 - cut, r2) and
                helper(l1 + cut, r1, l2, r2 - cut)):
                return True
        return False

    return helper(0, len(s1), 0, len(s2))
```

> **关键行中文注释**  
> - `sorted(sub1) != sorted(sub2)`：把子串的字母排好序后比较，相当于把字典（哈希表）里的“词条”对应起来，若不相同直接返回 `False`。  
> - `for cut in range(1, length)`: 逐个尝试所有可能的切分点。  
> - 两个 `if` 分别对应“**不交换**”和“**交换**”两种情况。

#### 复杂度

- **时间复杂度**：`O(2^n * n)`（指数级）  
  - 解释：每一次递归都要在 `n-1` 个切点里挑一个，且每个切点有“不交换 / 交换”两种分支，导致递归树的节点数呈指数增长。再乘上每层做的 `sorted`（`O(n log n)`）或字符计数，整体大概是指数级的。  
  - 用大白话说，就是 **“每增加一个字符，可能的情况几乎翻倍”**，所以会很快变慢。

- **空间复杂度**：`O(n)`（递归栈深度）  
  - 递归最多会把字符串切到长度为 1，深度为 `n`，每层保存常数个局部变量，所以空间随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于大量的重复计算：  
- 同样的子串组合会被递归多次检查。  
- 例如 `isScramble("great", "rgeat")` 中会出现多次对 `"ea"` 与 `"ae"` 的比较。

**优化思路**：把已经算过的子问题结果记下来，下次直接拿来用——这就是**记忆化搜索（Memoization）**或**动态规划**的核心思想。

我们可以把子问题抽象为：

> **子问题**：`dp[i][j][len]` 表示 `s1[i : i+len]` 是否可以 scramble 成 `s2[j : j+len]`。

- `i`：在 `s1` 中的起始下标  
- `j`：在 `s2` 中的起始下标  
- `len`：子串的长度  

**转移**（递推公式）：

对每一个可能的切分长度 `k (1 ≤ k < len)`，只要下面两种情况之一成立，就说明 `dp[i][j][len] = True`：

1. **不交换**  
   - 左半段匹配：`dp[i][j][k]`  
   - 右半段匹配：`dp[i+k][j+k][len-k]`

2. **交换**  
   - 左半段匹配右半段：`dp[i][j+len-k][k]`  
   - 右半段匹配左半段：`dp[i+k][j][len-k]`

如果所有 `k` 都不满足，则 `dp[i][j][len] = False`。

**初始化**：

- 当 `len = 1` 时，只要对应字符相等即为 `True`，否则 `False`。  
- 还可以提前做一次**字符频次检查**（和暴力版一样），如果整体字符集合不同直接返回 `False`，可以省掉后面的 DP。

**实现方式**：

- **自顶向下**（递归 + 记忆化）  
  - 用字典 `memo[(i, j, len)]` 保存已经算过的结果。  
  - 代码简洁，易于理解。

- **自底向上**（三维 DP 表）  
  - 先填长度为 1 的情况，然后逐步增长长度。  
  - 空间占用 `O(n³)`（因为 `n ≤ 30`，完全可以接受），时间 `O(n⁴)`（每个状态遍历所有切分点）。  

这里给出 **自顶向下记忆化** 的实现，因为它保留了递归的直观思路，同时避免了重复计算，代码更短。

> **类比**：记忆化相当于给递归的“查字典”装上了“缓存”。第一次查到某个词条（子问题）时把答案记下来，第二次再需要时直接拿，不必重新查。

#### 代码（Python）

```python
def isScramble(s1: str, s2: str) -> bool:
    n = len(s1)
    if n != len(s2):
        return False

    # 1）整体字符频次不一致，直接返回 False
    if sorted(s1) != sorted(s2):
        return False

    # 记忆化表：键是 (i, j, length)，值是 bool
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(i: int, j: int, length: int) -> bool:
        """
        判断 s1[i:i+length] 是否可以 scramble 成 s2[j:j+length]
        """
        # 1) 长度为 1 时直接比较字符
        if length == 1:
            return s1[i] == s2[j]

        # 2) 再做一次局部字符频次检查（剪枝）
        if sorted(s1[i:i+length]) != sorted(s2[j:j+length]):
            return False

        # 3) 尝试所有可能的切分点
        for k in range(1, length):            # k 为左子串的长度
            # 不交换的情况
            if (dfs(i, j, k) and
                dfs(i + k, j + k, length - k)):
                return True
            # 交换的情况
            if (dfs(i, j + length - k, k) and
                dfs(i + k, j, length - k)):
                return True
        # 没有任何切法成立
        return False

    # 从整体开始检查
    return dfs(0, 0, n)
```

**代码要点说明**  

| 行号 | 关键说明 |
|------|----------|
| `sorted(s1) != sorted(s2)` | 整体字符集合不同，直接返回 `False`（相当于先查一次“字典”）。 |
| `@lru_cache` | Python 内置的记忆化装饰器，会把函数的输入 `(i,j,length)` 对应的返回值缓存起来，避免重复递归。 |
| `if length == 1` | 递归终止条件：单个字符只能相等才算匹配。 |
| `if sorted(... ) != sorted(... )` | 局部剪枝：子串的字母集合不同，后面的递归必然失败，提前返回。 |
| `for k in range(1, length)` | 逐个尝试切分点 `k`（左半段长度）。 |
| 两个 `if` 分别对应 **不交换** 与 **交换** 两种组合。 |

#### 复杂度

- **时间复杂度**：`O(n⁴)`  
  - 解释：状态数为 `O(n³)`（`i`、`j`、`length` 各可取 `n`，但 `length` 只到 `n`），每个状态遍历 `k = 1 … length-1`，最坏情况下是 `O(n)`，所以整体 `O(n³ * n) = O(n⁴)`。  
  - 对于本题的约束 `n ≤ 30`，`30⁴ = 810,000`，在 Python 中运行毫秒级完成。  
  - 与暴力解相比，**指数级**下降到 **多项式**，速度提升非常明显。

- **空间复杂度**：`O(n³)`（缓存表） + `O(n)`（递归栈）  
  - 缓存最多会存储每一种 `(i, j, length)` 的结果，数量上限是 `n³`。  
  - 递归深度最多 `n`，所以额外的栈空间是线性的。

---

## 心得

- **核心技巧**：**记忆化搜索 / 动态规划** + **字符频次剪枝**。  
- **适用的题型**  
  1. “是否可以通过某种递归拆分得到目标”——如 **Valid Palindrome III**（可以删除 k 个字符使回文）。  
  2. “两个结构是否相似”——如 **Isomorphic Strings**、**Word Break**（判断能否拆分成字典单词）。  
- **一句话总结解题钥匙**：  
  > “把递归的每一步结果记下来，重复子问题只算一次，同时用字符集合提前把不可能的分支剔除。”

---

## 反思

- **第一反应**：看到“把字符串随意切、再可能交换”，立刻想到**递归枚举所有切法**，于是写了暴力版。  
- **最容易踩的坑**  
  - **剪枝不足**：没有先检查字符频次，会导致大量无意义的递归，直接超时。  
  - **边界条件**：长度为 1 时一定要返回字符相等，否则会无限递归。  
  - **缓存键的设计**：忘记把 `length` 放进键里会产生错误的记忆化结果。  
- **下次遇到同类题**：  
  1. 先判断整体可行性（字符集合、计数等）。  
  2. 把递归过程抽象成“子问题 + 状态”，思考是否可以用记忆化或 DP。  
  3. 再写递归/DP 实现，并做好剪枝。