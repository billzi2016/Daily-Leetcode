# #301. 删除无效括号 / Remove Invalid Parentheses

> 难度：困难 · 标签：String、Backtracking、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/remove-invalid-parentheses/)

---

## 题目（英文原版）

**Description**

Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.
Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: s = "()())()"
Output: ["(())()","()()()"]
```

**Example 2:**

```
Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]
```

**Example 3:**

```
Input: s = ")("
Output: [""]
```

**Constraints**

- 1 <= s.length <= 25
- s consists of lowercase English letters and parentheses '(' and ')'.
- There will be at most 20 parentheses in s.

---

## 题目（中文翻译）

给定一个只包含括号 (parentheses) 和字母的字符串 `s`，删除最少数量的无效括号，使得得到的字符串有效。  
返回所有在删除最少括号后仍然有效的唯一字符串列表。答案可以以任意顺序返回。

约束条件：

- `1 <= s.length <= 25`
- `s` 仅由小写英文字母和括号 `'('`、`')'` 组成。
- `s` 中至多包含 20 个括号。

示例 1:
Input: s = "()())()"
Output: ["(())()","()()()"]

示例 2:
Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]

示例 3:
Input: s = ")("
Output: [""]

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的删法都枚举一遍」，然后挑出合法且删除字符最少的结果。  
- **枚举方式**：把字符串里每个字符（只考虑 '('、')'）视作「保留」或「删除」两种选择，用递归或二进制位表示所有子集。  
- **合法性检查**：遍历生成的子串，维护一个计数器 `balance`，遇到 '(' → `balance+=1`，遇到 ')' → `balance-=1`，只要 `balance` 途中不为负且最后等于 0，说明括号配对合法。  
- **记录最少删除数**：在遍历所有子集的过程中，记录当前子串删除的字符数 `removed = original_len - len(candidate)`，只保留删除数等于全局最小值的子串，使用 `set` 去重。

> **类比**：把括号看成「要配对的鞋子」——我们把每只鞋子都可能「不穿」或「穿上」，最后只留下「左右鞋子数量相等且顺序正确」的组合。

#### 代码（Python）

```python
from typing import List

def removeInvalidParentheses_bruteforce(s: str) -> List[str]:
    n = len(s)
    results = set()          # 用集合自动去重
    min_removed = n + 1      # 记录最少删掉的字符数，初始设为一个很大的数

    # ---------- 判断字符串是否合法 ----------
    def is_valid(t: str) -> bool:
        balance = 0
        for ch in t:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
                if balance < 0:          # 右括号比左括号多，直接非法
                    return False
        return balance == 0              # 左右括号数量相等才合法

    # ---------- 深度优先遍历所有子集 ----------
    def dfs(idx: int, path: List[str], removed: int):
        nonlocal min_removed, results
        if idx == n:                      # 已处理完所有字符
            candidate = ''.join(path)
            if is_valid(candidate):
                if removed < min_removed:
                    min_removed = removed
                    results.clear()       # 找到更少删除数，清空旧结果
                if removed == min_removed:
                    results.add(candidate)
            return

        ch = s[idx]
        # ① 删除当前字符（只对括号考虑删除，字母直接保留）
        if ch in '()':
            dfs(idx + 1, path, removed + 1)

        # ② 保留当前字符
        path.append(ch)
        dfs(idx + 1, path, removed)
        path.pop()                        # 回溯

    dfs(0, [], 0)
    return list(results)
```

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 来自所有子集的枚举（每个括号都有「保留」或「删除」两种选择）。  
  - 对每个子集我们要遍历一次字符串检查合法性，耗时 `O(n)`。  
  - 对于 `n ≤ 25`（题目限制），虽然指数级，但在最坏情况下仍能跑完。

- **空间复杂度**：`O(n)`（递归栈深度 + 当前路径字符列表），再加上保存结果的集合，最坏也只会存 `O(2^n)` 条字符串，但实际只会保留最小删除数的少量解。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「把所有子集都遍历一遍」——即使已经找到了合法解，仍然继续搜索更深的层次，导致大量无用的计算。  
我们可以把搜索过程改成 **层序（BFS）**：  

1. **把每一次删除视作一次「层」**。  
   - 第 0 层：原字符串本身。  
   - 第 1 层：所有只删掉 **一个** 括号得到的字符串。  
   - 第 2 层：删掉 **两个** 括号得到的字符串，依此类推。  

2. **从第 0 层开始往下遍历**，只要在当前层找到了至少一个合法字符串，就可以停止搜索。因为 BFS 保证先找到的合法解是「删除最少括号」的。  

3. **剪枝**：  
   - 同一层可能会产生相同的子串（例如删除第 2 个 '(' 与删除第 3 个 '(' 产生相同结果），用 `visited` 集合避免重复入队。  
   - 只在当前层检查合法性，后面的层不必再继续生成子串，从而大幅降低搜索空间。  

> **类比**：把每一次「删一个括号」看作「向前走一步」。我们从原点出发，一步一步往前走，只要在某一步踩到了「合法的石头」就停下来——因为往后走只会让步数更大，根本不需要再看了。

#### 代码（Python）

```python
from collections import deque
from typing import List, Set

def removeInvalidParentheses_bfs(s: str) -> List[str]:
    # ---------- 判断合法性 ----------
    def is_valid(t: str) -> bool:
        bal = 0
        for ch in t:
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
                if bal < 0:          # 右括号太多
                    return False
        return bal == 0

    visited: Set[str] = {s}          # 已经遍历过的字符串，防止重复
    queue = deque([s])               # BFS 队列
    found: List[str] = []            # 当前层找到的所有合法解
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            cur = queue.popleft()
            if is_valid(cur):
                found.append(cur)   # 本层合法，直接加入答案
            # 如果已经在本层找到合法解，就不再产生下一层的子串
            if found:
                continue
            # 产生下一层子串（删掉一个括号）
            for i, ch in enumerate(cur):
                if ch not in '()':   # 只对括号尝试删除，字母直接保留
                    continue
                nxt = cur[:i] + cur[i+1:]   # 删除第 i 个字符
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        if found:                     # 本层已有合法解，直接结束 BFS
            break
    # 如果连合法解都没有（例如 s=")("），BFS 会遍历到空串，空串也是合法的
    return found if found else [""]

```

#### 复杂度  

- **时间复杂度**：`O(C * n)`  
  - `C` 为遍历的不同字符串个数。因为 BFS 在找到最少删除数的层后就会停止，`C` 远远小于 `2^n`（实际约为 `O( n * choose(k, n) )`，其中 `k` 为最少删除的括号数）。  
  - 每次检查合法性需要 `O(n)`，整体比暴力解快几个数量级。

- **空间复杂度**：`O(C * n)`  
  - `visited` 集合和队列中保存的都是不同的子串，总体数量同上。  
  - 由于 `n ≤ 25`，即使最坏情况也只会保存几千个短串，完全在内存范围。

---

## 心得

- **核心技巧**：**层序遍历（BFS） + 合法性剪枝**。  
  通过把「删多少括号」当作层次来搜索，保证第一批找到的合法解一定是「最少删除」的解，避免了对更深层次的无用搜索。

- **适用题型**  
  1. **最少操作数问题**：如「最少翻转使二进制数组全为 1」等，需要找最少步数的最短路径。  
  2. **状态压缩搜索**：如「单词接龙」(Word Ladder) 中的层序搜索。  
  3. **剪枝的回溯**：如「括号生成」(Generate Parentheses) 中的剪枝思路。

- **一句话总结解题钥匙**：  
  **先用 BFS 把「删除次数」变成层次，第一层出现合法解就停——最少删多少，最先找到的就是答案。**

---

## 反思

- **第一反应**：看到「最小删除」关键字，立刻想到「枚举所有子集」——这是一种直观但效率低下的做法。  
- **最容易踩的坑**  
  1. **重复子串**：在 BFS 中不去重会导致指数级膨胀，需要 `visited` 集合。  
  2. **只删除括号**：题目允许保留字母，删除时必须跳过非括号字符，否则会错误地把合法解删掉。  
  3. **空串合法**：如输入 `")("`，最少删除后得到空串，代码要能够返回 `[""]` 而不是空列表。  

- **下次遇到同类题**，第一步应该：  
  **把「最少操作」转化为「层序搜索」**，先确定搜索的层次（操作次数），在每一层检查目标条件，满足即停止。这样既保证最优，又能大幅削减搜索空间。