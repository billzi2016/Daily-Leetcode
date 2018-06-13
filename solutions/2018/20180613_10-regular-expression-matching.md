# #10. 正则表达式匹配 / Regular Expression Matching

> 难度：困难 · 标签：String、Dynamic Programming、Recursion · [LeetCode 链接](https://leetcode.com/problems/regular-expression-matching/)

---

## 题目（英文原版）

**Description**

Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
The matching should cover the entire input string (not partial).

**Examples**

**Example 1:**

```
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
```

**Example 2:**

```
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
```

**Example 3:**

```
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".
```

**Constraints**

- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

---

## 题目（中文翻译）

给定一个输入字符串 `s` 和一个模式 `p`，实现支持 `.` 和 `*` 的正则表达式匹配，使得：

- `.` 匹配任意单个字符（single character）。
- `*` 匹配零个或多个前面的元素（preceding element）。
- 匹配必须覆盖整个输入字符串（而不是部分匹配）。

## 示例

### 示例 1
**输入**: `s = "aa", p = "a"`  
**输出**: `false`  
**解释**: `"a"` 不能匹配完整的字符串 `"aa"`。

### 示例 2
**输入**: `s = "aa", p = "a*"`  
**输出**: `true`  
**解释**: `'*'` 表示前面的元素 `'a'` 可以出现零次或多次。因此将 `'a'` 重复一次即可得到 `"aa"`。

### 示例 3
**输入**: `s = "ab", p = ".*"`  
**输出**: `true`  
**解释**: `".*"` 表示任意字符 `.` 出现零次或多次 `*`，可以匹配 `"ab"`。

## 约束条件

- `1 <= s.length <= 20`
- `1 <= p.length <= 20`
- `s` 只包含小写英文字母。
- `p` 只包含小写英文字母、`.` 和 `*`。
- 对于每个出现的 `*`，一定有一个合法的前置字符与之匹配。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把正则表达式当成一棵决策树**，逐字符尝试所有可能的匹配方式。  
- `.` 可以匹配 **任意一个字符**，相当于我们在字典里随便挑一个词对应的页码。  
- `*` 表示**前面的字符可以出现 0 次、1 次、2 次……**，这就像在购物时可以选择不买、买一件、买两件……  
因此我们可以用递归来枚举：

1. 看模式的第一个字符 `p[0]` 是否是普通字符或 `.`。如果匹配，就把 `s` 和 `p` 都向后走一步继续比较。  
2. 如果模式的第二个字符是 `*`（即 `p[1] == '*'`），我们有两种选择：  
   - **不使用 `*`**：把 `*` 连同它前面的字符一起丢掉，直接比较 `s` 与 `p[2:]`。  
   - **使用 `*`**：只要 `s` 的首字符和 `p[0]` 匹配（包括 `.`），就把 `s` 向后走一步，`p` 仍然保持不变（因为 `*` 还能再匹配一次）。  
递归到底的情况是：  
- 当 `p` 为空时，只有 `s` 也为空才算匹配成功。  
- 当 `s` 为空但 `p` 还有字符时，只能在 `*` 能把前面的字符“消掉”的情况下才可能匹配。

这套递归（回溯）思路保证了**穷举所有合法匹配**，所以一定正确。

#### 代码（Python）

```python
def is_match_brute(s: str, p: str) -> bool:
    """
    递归暴力解法
    """
    # 当模式为空时，只有字符串也为空才匹配
    if not p:
        return not s

    # 第一个字符是否匹配（考虑 '.' 的通配）
    first_match = bool(s) and (p[0] == s[0] or p[0] == '.')

    # 如果模式的第二个字符是 '*'
    if len(p) >= 2 and p[1] == '*':
        # 1）* 代表出现 0 次：直接跳过这两个字符
        # 2）* 代表出现 >=1 次：要求首字符匹配，然后让 s 前进一位，模式保持不变
        return (is_match_brute(s, p[2:]) or
                (first_match and is_match_brute(s[1:], p)))
    else:
        # 普通匹配，两个字符串都向后走一步
        return first_match and is_match_brute(s[1:], p[1:])
```

#### 复杂度

- **时间复杂度：** `O(2^{m+n})`（指数级）  
  这里的 `m = len(s)`, `n = len(p)`。因为每遇到一个 `*`，我们会产生两条递归分支：使用或不使用 `*`，最坏情况下会出现指数级的递归树。可以把它想象成“每次都要在两条路中选”，路数会翻倍。

- **空间复杂度：** `O(m+n)`  
  递归调用的栈深度最多是 `m + n`（每次最多消耗一个字符），所以只占用线性空间。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**大量重复子问题**：相同的 `(i, j)`（即 `s[i:]` 与 `p[j:]`）会被多次递归计算。  
我们可以把“从下标 i 开始的 s 与从下标 j 开始的 p 是否匹配”记下来，**避免重复计算**。这正是**动态规划（DP）**的核心思想。

##### 状态定义  

`dp[i][j]` 表示 **`s[i:]` 与 `p[j:]` 是否匹配**（后缀匹配）。  
- `i` 取值 `0 … len(s)`，`j` 取值 `0 … len(p)`。  
- 当 `i == len(s)` 时，`s[i:]` 是空串；同理 `j == len(p)`。

##### 初始化  

- `dp[len(s)][len(p)] = True` —— 空串对空模式自然匹配。  
- 对于 `i = len(s)`（即 s 已经耗尽），如果剩余的模式能匹配空串，只可能是形如 `a*`、`a*b*`… 的组合。我们遍历 `p`，如果 `p[j+1] == '*'`，则 `dp[len(s)][j] = dp[len(s)][j+2]`，否则为 `False`。

##### 转移方程  

设 `first_match = (i < len(s)) and (p[j] == s[i] or p[j] == '.')`  

1. **如果 `p[j+1]` 是 `*`**（即 `j+1 < len(p)` 且 `p[j+1] == '*'`）  
   - **不使用 `*`**：直接跳过这两个字符 → `dp[i][j] = dp[i][j+2]`  
   - **使用 `*`**：要求当前字符匹配且把 `s` 向后一步 → `dp[i][j] = dp[i][j] or (first_match and dp[i+1][j])`  
   两者取 **或**（只要有一种方式成功即为匹配）。

2. **普通字符或 `.`**  
   - 必须当前字符匹配且后面的子问题也匹配 → `dp[i][j] = first_match and dp[i+1][j+1]`

##### 计算顺序  

因为 `dp[i][j]` 依赖于 `dp[i][j+2]`、`dp[i+1][j]`、`dp[i+1][j+1]`，我们从右下角往左上角填表即可（逆序遍历 `i`、`j`）。

##### 代码（Python）

```python
def is_match_dp(s: str, p: str) -> bool:
    """
    动态规划（自底向上）实现正则匹配
    """
    m, n = len(s), len(p)
    # 多建一行一列，方便表示空后缀的情况
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # 空串对空模式匹配
    dp[m][n] = True

    # 只剩空串 s，处理形如 a*b*c* 的尾部模式
    for j in range(n - 1, -1, -1):
        if j + 1 < n and p[j + 1] == '*':
            dp[m][j] = dp[m][j + 2]   # 把 a* 当作空出现
        else:
            dp[m][j] = False          # 其余情况只能匹配失败

    # 逆序遍历 s 的所有位置
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # 当前字符是否匹配（考虑 '.'）
            first_match = (p[j] == s[i] or p[j] == '.')

            if j + 1 < n and p[j + 1] == '*':
                # 1) * 当作 0 次出现，直接跳过这两个字符
                # 2) * 当作 >=1 次出现，要求当前匹配并继续匹配 s[i+1:] 与 p[j:]
                dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
            else:
                # 普通匹配，两个后缀都要向后一步
                dp[i][j] = first_match and dp[i + 1][j + 1]

    return dp[0][0]
```

#### 复杂度

- **时间复杂度：** `O(m * n)`  
  只遍历了一遍二维表，`m = len(s)`, `n = len(p)`。相比指数级的暴力解快了很多。可以把它想成“每个字符组合只算一次”，不再翻倍。

- **空间复杂度：** `O(m * n)`  
  需要一个 ` (m+1) × (n+1) ` 的表来存放子问题的答案。若进一步优化（只保留当前行和下一行），空间可以降到 `O(n)`，但这里保持完整表便于理解。

---

## 心得

- 这道题的核心技巧是 **把递归的子问题记忆化**，即**动态规划**。  
- 适用这种技巧的题型还有：  
  1. **编辑距离（Edit Distance）** – 计算两个字符串的最小编辑步数。  
  2. **通配符匹配（Wildcard Matching）** – 类似正则，但只支持 `?` 与 `*`。  
  3. **拆分数组的最大子数组和（Maximum Subarray Sum）** – 通过 DP 把局部最优转化为全局最优。  
- **一句话总结解题钥匙：**「把“从当前位置往后匹配”抽象成状态，用表格记住每个状态的答案，避免重复计算。」

---

## 反思

- **第一反应**：直接写递归回溯，想把 `*` 的两种含义写成两个分支。  
- **最容易踩的坑**：  
  - 忘记处理 `*` 可以匹配 **零次** 的情况，导致在模式尾部出现 `a*` 时出错。  
  - 边界条件不完整：空字符串与只剩 `*` 的模式匹配，需要单独初始化 DP 表的最后一行。  
  - 在 DP 转移时把 `dp[i][j+2]`（跳过 `*`）和 `dp[i+1][j]`（使用 `*`）的逻辑混淆。  
- **下次遇到同类题**，第一步应该：**先写出递归/回溯的状态定义**（`i, j`），再思考哪些子状态会被重复计算，最后把它们写进 DP 表或记忆化搜索。这样既保证正确性，又能快速得到最优解。