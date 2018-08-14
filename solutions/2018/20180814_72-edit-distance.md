# #72. 编辑距离 / Edit Distance

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/edit-distance/)

---

## 题目（英文原版）

**Description**

Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.
You have the following three operations permitted on a word:

**Examples**

**Example 1:**

```
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
```

**Example 2:**

```
Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation: 
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')
```

**Constraints**

- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`，返回将 `word1` 转换成 `word2` 所需的最少操作次数。  
在字符串上你可以使用以下三种操作（operations）：

- 插入（insert）一个字符  
- 删除（delete）一个字符  
- 替换（replace）一个字符为另一个字符  

---

### 示例

**示例 1**  
**输入**: `word1 = "horse", word2 = "ros"`  
**输出**: `3`  
**解释**:  
```
horse  -> rorse   （replace 将 'h' 替换为 'r'）
rorse  -> rose    （delete 删除 'r'）
rose   -> ros     （delete 删除 'e'）
```

**示例 2**  
**输入**: `word1 = "intention", word2 = "execution"`  
**输出**: `5`  
**解释**:  
```
intention -> inention   （delete 删除 't'）
inention  -> enention   （replace 将 'i' 替换为 'e'）
enention  -> exention   （replace 将 'n' 替换为 'x'）
exention  -> exection   （replace 将 'n' 替换为 'c'）
exection  -> execution  （insert 插入 'u'）
```

---

### 约束条件

- `0 <= word1.length, word2.length <= 500`
- `word1` 和 `word2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `word1` 的每一种可能的编辑序列都枚举出来，看看哪一种恰好能得到 `word2`，并记录最少的操作次数。  
- **数据结构**：我们可以把一次编辑过程看成一棵搜索树的路径。树的每个节点保存当前的字符串，往下的三条边分别对应**插入**、**删除**、**替换**三种操作。  
- **生活化类比**：把字符串想象成一本书的内容，编辑操作就像在写稿子时的“增删改”。暴力法相当于把所有可能的稿件改动都写下来，再逐一检查哪一个最短。  
- **正确性**：只要把**所有**合法的编辑序列都遍历完，就一定能找到最少步数的那条路径，所以答案一定在遍历的结果里。  

然而，这种穷举的代价极其高。设 `n = len(word1)`, `m = len(word2)`，每一步都有最多 3 种选择，搜索深度大约是 `n + m`，总的可能序列数是 `3^{n+m}`，即使 `n,m` 只有 5，也会产生几千条路径，远超计算机的承受范围。

#### 代码（Python）

```python
from collections import deque

def minDistance_bruteforce(word1: str, word2: str) -> int:
    """暴力 BFS（广度优先搜索）实现，仅作概念演示，超时不建议使用"""
    # BFS 保证第一次到达 word2 时的步数即为最小值
    queue = deque()
    queue.append((word1, 0))          # (当前字符串, 已使用的编辑次数)
    visited = {word1}                 # 防止重复访问同一个状态

    while queue:
        cur, steps = queue.popleft()
        if cur == word2:              # 找到目标，返回步数
            return steps

        # 1. 删除任意一个字符
        for i in range(len(cur)):
            nxt = cur[:i] + cur[i+1:]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, steps + 1))

        # 2. 插入任意字符（这里遍历所有 'a'~'z'，实际实现会更慢）
        for i in range(len(cur) + 1):
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                nxt = cur[:i] + ch + cur[i:]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))

        # 3. 替换任意字符
        for i in range(len(cur)):
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                if cur[i] == ch:      # 替换成相同字符等于不操作，跳过
                    continue
                nxt = cur[:i] + ch + cur[i+1:]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))

    return -1   # 理论上不会走到这里
```

> **提示**：上述代码仅用于说明“把所有可能的编辑序列枚举”的思路。实际跑 LeetCode 会因为状态爆炸而 **TLE**（超时）。

#### 复杂度

- **时间复杂度**：`O(3^{n+m})`（指数级）  
  大白话：当字符串长度稍微大一点（比如 10），所需的操作次数就会像 3 的 20 次方那样庞大，根本不可能在电脑里算完。
- **空间复杂度**：`O(3^{n+m})`（同样是指数级）  
  因为要把所有中间状态都放进队列/集合里，空间占用会和时间一样快地增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“重复子问题”**是导致指数爆炸的根本原因。  
比如在搜索树里，`word1 = "ab"`，`word2 = "ac"`，我们既可以先把 `"ab"` 删除 `'b'` 再插入 `'c'`，也可以直接把 `'b'` 替换成 `'c'`。这两条路径在后面都会进入同一个子状态 `"a"`，于是大量的计算被重复做了。

**动态规划（Dynamic Programming, DP）** 正是用来消除这种重复子问题的技术。  
我们把**“把 `word1` 的前 i 个字符变成 `word2` 的前 j 个字符所需的最少操作数”**记作 `dp[i][j]`。从这个定义出发，可以一步步写出状态转移方程：

1. **边界**  
   - `dp[0][j]`：把空串变成 `word2` 的前 `j` 个字符，只能插入 `j` 次。  
   - `dp[i][0]`：把 `word1` 的前 `i` 个字符变成空串，只能删除 `i` 次。

2. **转移**  
   - 如果 `word1[i-1] == word2[j-1]`（注意下标偏移），最后一个字符已经相同，不需要额外操作，直接继承 `dp[i-1][j-1]`。  
   - 否则，需要在 **插入**、**删除**、**替换** 三种操作中选最小的那一个，再加一次操作：
     - 插入：`dp[i][j-1] + 1`（在 `word1` 前 i 个字符后面插入 `word2[j-1]`）
     - 删除：`dp[i-1][j] + 1`（把 `word1[i-1]` 删除）
     - 替换：`dp[i-1][j-1] + 1`（把 `word1[i-1]` 替换成 `word2[j-1]`）

   所以总体公式为：

   ```
   if word1[i-1] == word2[j-1]:
       dp[i][j] = dp[i-1][j-1]
   else:
       dp[i][j] = 1 + min(dp[i][j-1],    # 插入
                          dp[i-1][j],    # 删除
                          dp[i-1][j-1])  # 替换
   ```

3. **答案**  
   `dp[len(word1)][len(word2)]` 即为整个字符串的编辑距离。

**空间优化**  
观察公式可以发现，计算第 `i` 行只依赖第 `i-1` 行和当前行的左侧元素。于是可以只保留两行（或甚至一行滚动）来降低空间到 `O(min(n,m))`。这里先给出最直观的二维 DP 实现，随后展示一维滚动写法。

#### 代码（Python）

##### 2.1 完整二维 DP（易于理解）

```python
def minDistance_dp(word1: str, word2: str) -> int:
    """二维动态规划实现编辑距离"""
    n, m = len(word1), len(word2)

    # dp[i][j] 表示 word1 前 i 个字符 → word2 前 j 个字符的最少编辑数
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # 初始化第一行和第一列（空串的情况）
    for i in range(n + 1):
        dp[i][0] = i          # 只需要 i 次删除
    for j in range(m + 1):
        dp[0][j] = j          # 只需要 j 次插入

    # 填表
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                # 最后一个字符相同，不需要额外操作
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # 取插入、删除、替换三者的最小值再加 1
                dp[i][j] = 1 + min(dp[i][j - 1],    # 插入
                                   dp[i - 1][j],    # 删除
                                   dp[i - 1][j - 1])# 替换

    return dp[n][m]
```

##### 2.2 一维滚动数组（空间优化）

```python
def minDistance_dp_optimized(word1: str, word2: str) -> int:
    """只用 O(min(n,m)) 空间的一维 DP"""
    # 为了使用更少的空间，始终让 word2 是较短的那个
    if len(word1) < len(word2):
        word1, word2 = word2, word1   # 交换，使 word2 更短

    n, m = len(word1), len(word2)

    # prev 保存上一行的值，cur 保存当前行
    prev = list(range(m + 1))          # dp[0][j] = j
    cur = [0] * (m + 1)

    for i in range(1, n + 1):
        cur[0] = i                     # dp[i][0] = i
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1]   # 相同字符，直接继承左上角
            else:
                cur[j] = 1 + min(cur[j - 1],   # 插入（左边）
                                 prev[j],      # 删除（上面）
                                 prev[j - 1])  # 替换（左上角）
        # 交换引用，准备进入下一行
        prev, cur = cur, prev

    # 循环结束后，prev 保存的是最后一行的结果
    return prev[m]
```

#### 复杂度

- **时间复杂度**：`O(n * m)`  
  大白话：我们要填一个 `n+1` 行、`m+1` 列的表格，每个格子只算一次常数时间的比较和取最小值。若两个字符串各有 500 个字符，最多算 250,000 次，电脑几毫秒就能搞定。

- **空间复杂度**：  
  - 二维 DP：`O(n * m)`（表格本身占的空间）。  
  - 一维滚动：`O(min(n, m))`，只保存两行，最多 501 个整数，几乎可以忽略不计。  
  与暴力解的指数级空间相比，简直是“天壤之别”。

---

## 心得

- **核心技巧**：把“把前 i 个字符变成前 j 个字符的最少操作数”抽象为状态 `dp[i][j]`，通过**子问题的最优子结构**递推得到答案。  
- **适用题型**：  
  1. **最小编辑距离**（本题）  
  2. **最长公共子序列（LCS）** – 也是在两个序列上找子问题的最优解  
  3. **最小路径和（网格 DP）** – 把二维网格看成字符匹配的状态转移表  

- **一句话总结**：**“把大问题拆成‘前缀到前缀’的子问题，用表格记忆每一步的最优解，最后表格右下角的数就是答案。”**

---

## 反思

- **第一反应**：看到“插入、删除、替换”三个操作，就想到要把每一步的选择枚举出来，甚至联想到 BFS/DFS 的搜索树。  
- **最容易踩的坑**：  
  - **下标偏移**：`dp` 表格从 0 开始，实际字符对应的是 `i-1`、`j-1`，容易写错导致越界或逻辑错误。  
  - **初始化**：忘记把第一行/列填成 `0..n`、`0..m`，会导致后面的最小值计算不准确。  
  - **空间优化时的行交换**：忘记在每轮结束后把 `prev` 与 `cur` 交换，导致后面的循环使用了错误的旧数据。  

- **下次遇到同类题的第一步**：先问自己“有没有‘前缀到前缀’的最优子结构”，如果答案是肯定的，就立刻写出 DP 状态定义和转移公式，再考虑是否需要空间压缩。