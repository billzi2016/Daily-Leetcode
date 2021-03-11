# #1249. 最少删除使括号有效 / Minimum Remove to Make Valid Parentheses

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/)

---

## 题目（英文原版）

**Description**

Given a string s of '(' , ')' and lowercase English characters.
Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting parentheses string is valid and return any valid string.
Formally, a parentheses string is valid if and only if:

**Examples**

**Example 1:**

```
Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.
```

**Example 2:**

```
Input: s = "a)b(c)d"
Output: "ab(c)d"
```

**Example 3:**

```
Input: s = "))(("
Output: ""
Explanation: An empty string is also valid.
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is either '(' , ')', or lowercase English letter.

---

## 题目（中文翻译）

给定一个仅由字符 `'('`、`')'` 和小写英文字母组成的字符串 `s`。  
你的任务是删除最少数量的括号（`'('` 或 `')'`，可以在任意位置），使得剩余的括号字符串（parentheses string）合法，并返回任意一个合法的结果字符串。

形式上，括号字符串 **合法** 当且仅当满足以下任意一种情况：

1. 为空字符串；
2. 它可以表示为两个合法字符串的连接；
3. 它的形式为 `'('` + **合法字符串** + `')'`。

---

### 示例

**示例 1**  
```
Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)"、"lee(t(c)ode)" 也都是合法的答案。
```

**示例 2**  
```
Input: s = "a)b(c)d"
Output: "ab(c)d"
```

**示例 3**  
```
Input: s = "))(("
Output: ""
Explanation: 空字符串也是合法的。
```

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s[i]` 只能是 `'('`、`')'` 或小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「枚举所有可能的删字符组合」，找出其中删最少字符且剩下的括号序列合法的那一个。  
实现上可以把每个字符当成「保留」或「删除」两种状态，用 **回溯（DFS）** 或 **位掩码** 暴力遍历所有子序列，然后检查该子序列的括号是否匹配。

- **数据结构**  
  - **字符串**：原始输入。  
  - **列表**：在递归过程中保存当前构造的子序列。  
  - **栈（模拟）**：检查子序列是否合法时，用栈来配对 '(' 与 ')'（栈就像“查字典”，把左括号当成词，遇到右括号时去查找对应的左括号）。

- **为什么正确**  
  只要遍历了所有可能的删字符方式，必然会碰到最少删字符且合法的那一种。随后我们只要返回其中任意一个合法子序列即可。

- **时间/空间复杂度**  
  - 对长度为 `n` 的字符串，有 `2^n` 种保留/删除的组合，遍历全部组合的时间是 **指数级**，记作 `O(2^n)`。  
  - 检查每个子序列是否合法需要线性扫描 `O(n)`，所以总时间约为 `O(n·2^n)`。  
  - 递归栈深度最坏是 `n`，加上保存子序列的列表也最多 `n`，空间 `O(n)`。

> **大白话**：  
> `O(2^n)` 就像把所有可能的钥匙都拽出来逐个尝试，钥匙的数量会随字符数指数增长，根本不可能在 10⁵ 长度的字符串上跑完。

#### 代码（Python）

```python
def minRemoveToMakeValid_bruteforce(s: str) -> str:
    n = len(s)
    best = ""                     # 记录找到的最少删除的合法串

    def is_valid(t: str) -> bool:
        """用栈检查 t 是否是合法的括号串"""
        stack = []
        for ch in t:
            if ch == '(':
                stack.append(ch)               # 左括号入栈
            elif ch == ')':
                if not stack:                  # 栈空，说明没有匹配的左括号
                    return False
                stack.pop()                    # 匹配成功，弹出左括号
        return not stack                       # 栈空才合法

    def dfs(idx: int, cur: list, removed: int):
        """在位置 idx 处决定保留还是删除当前字符"""
        nonlocal best
        # 已经遍历完全部字符
        if idx == n:
            candidate = "".join(cur)
            if is_valid(candidate):
                # 若比当前答案删得更少，直接更新
                if best == "" or len(candidate) > len(best):
                    best = candidate
            return

        # 选项 1：删除当前字符
        dfs(idx + 1, cur, removed + 1)

        # 选项 2：保留当前字符
        cur.append(s[idx])
        dfs(idx + 1, cur, removed)
        cur.pop()                               # 回溯

    dfs(0, [], 0)
    return best
```

> 这段代码在 `n` 较大时会超时，仅作思路展示。

#### 复杂度

- **时间复杂度**：`O(n·2^n)` —— 每一种保留/删除组合都要检查一次，指数级增长，实际不可用。  
- **空间复杂度**：`O(n)` —— 递归栈深度和临时字符列表最多 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「一次性枚举所有子序列」，而我们只需要 **一次线性扫描** 就能定位哪些括号必须被删。

**核心观察**  
- 对于一个合法的括号串，**从左到右**的每个前缀中，左括号 '(' 的数量 **不小于** 右括号 ')' 的数量。  
- 同理，**从右到左**的每个后缀中，右括号 ')' 的数量 **不小于** 左括号 '(' 的数量。

利用这两个性质，我们可以两遍扫描：

1. **左 → 右**：  
   - 维护一个计数 `balance`，记录当前看到的左括号数量减去右括号数量。  
   - 遇到 '(' 时 `balance += 1`。  
   - 遇到 ')' 时，如果 `balance == 0`（说明左括号不够配），这时的 ')' 必须被删除；否则 `balance -= 1`（配对成功）。  
   - 把「合法」的字符（包括字母）保存到列表 `res` 中。

2. **右 → 左**（针对第一遍留下的多余 '('）：  
   - 此时 `balance` 代表剩余的未配对的左括号数量。  
   - 从 `res` 的末尾向前遍历，如果遇到 '(' 且 `balance > 0`，说明这是多余的左括号，需要删掉并 `balance -= 1`。  
   - 其他字符直接保留。

这样只用了 **两次线性遍历**，不需要额外的数据结构（栈可以看成是 `balance` 的简化版），时间 `O(n)`，空间 `O(n)`（存结果）。

**类比**  
- `balance` 像是「银行账户」的余额，存的是「未配对的左括号」。存钱（'('）会增加余额，取钱（')'）需要先确保账户有钱，否则这笔取钱是「非法」的，需要被丢掉。

#### 代码（Python）

```python
def minRemoveToMakeValid(s: str) -> str:
    # 第一次遍历：从左到右，删除多余的右括号
    res = []               # 暂存合法字符，可能还会有多余的 '('
    balance = 0            # 未配对的 '(' 数量

    for ch in s:
        if ch == '(':
            balance += 1               # 左括号进账
            res.append(ch)
        elif ch == ')':
            if balance == 0:           # 没有左括号可配，对应的 ')' 必须被删
                continue                # 跳过该字符
            balance -= 1               # 配对成功，左括号出账
            res.append(ch)
        else:                           # 小写字母直接保留
            res.append(ch)

    # 第二次遍历：从右到左，删除多余的左括号
    # 此时 balance 表示剩余未配对的 '(' 个数
    ans = []
    for ch in reversed(res):
        if ch == '(' and balance > 0:
            balance -= 1               # 删除一个多余的 '('
            continue                    # 跳过该字符
        ans.append(ch)                 # 其他字符全部保留

    # ans 是倒序的，需要再翻转回来
    return "".join(reversed(ans))
```

**代码要点注释**  

- `balance` 充当栈的作用，只记录数量，不需要真的把每个 '(' 放进栈里。  
- 第一次遍历时 `continue` 直接把非法的右括号抛掉，相当于「不让它进入银行账户」。  
- 第二次遍历使用 `reversed`，从后往前检查未配对的左括号，这一步可以把所有多余的 '(' 删掉。  
- 最终返回的字符串已经是合法的，且删掉的字符数量是最少的（因为只删了「一定非法」的括号）。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历两遍字符串，`n` 为字符串长度。相比暴力的指数级，这就是“一秒解决 10⁵ 长度”的关键。  
- **空间复杂度**：`O(n)` —— 需要额外的列表 `res` / `ans` 来保存中间结果，最坏情况下和原字符串等长。

---

## 心得

- **核心技巧**：利用括号匹配的前缀/后缀平衡性质，用计数（或栈）一次遍历剔除非法括号。  
- **适用的题型**  
  1. **删除最少字符使括号序列合法**（本题）。  
  2. **判断字符串是否为合法括号序列**（只需要一次左→右遍历检查 `balance` 是否始终非负且最终为 0）。  
  3. **最小插入使括号序列合法**（思路类似，只是记录缺少的左/右括号数量）。  
- **一句话总结**：**“左到右剔除多余的 ')'，右到左剔除多余的 '('，两遍线性扫描搞定。”**

---

## 反思

- **第一反应**：先想到用栈配对，随后想到直接记录未配对的左括号数量 `balance`，于是自然出现了两遍扫描的思路。  
- **最容易踩的坑**  
  - 忘记在第二遍遍历时只删除 **未配对的** '('，否则会把合法的 '(' 也删掉。  
  - 处理只有字母或全部是非法括号的极端情况，确保返回空字符串而不是 `None`。  
  - 在第一次遍历时，如果直接把 `balance` 设为负数会导致后续逻辑错误，必须在遇到非法 ')' 时直接 `continue`。  
- **下次遇到同类题**，第一步就要问自己：  
  - “从左到右，哪个字符会导致前缀不合法？”  
  - “从右到左，哪个字符会导致后缀不合法？”  
  只要回答这两个问题，就能快速构造出最优的线性解。