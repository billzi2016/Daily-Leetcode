# #1111. **两个有效括号字符串的最大嵌套深度** / Maximum Nesting Depth of Two Valid Parentheses Strings

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/)

---

## 题目（英文原版）

**Description**

A string is a valid parentheses string (denoted VPS) if and only if it consists of "(" and ")" characters only, and:
We can similarly define the nesting depth depth(S) of any VPS S as follows:
For example,  "", "()()", and "()(()())" are VPS's (with nesting depths 0, 1, and 2), and ")(" and "(()" are not VPS's.
Given a VPS seq, split it into two disjoint subsequences A and B, such that A and B are VPS's (and A.length + B.length = seq.length).
Now choose any such A and B such that max(depth(A), depth(B)) is the minimum possible value.
Return an answer array (of length seq.length) that encodes such a choice of A and B:  answer[i] = 0 if seq[i] is part of A, else answer[i] = 1.  Note that even though multiple answers may exist, you may return any of them.

**Examples**

**Example 1:**

```
Input: seq = "(()())"
Output: [0,1,1,1,1,0]
```

**Example 2:**

```
Input: seq = "()(())()"
Output: [0,0,0,1,1,0,1,1]
```

**Constraints**

- 1 <= seq.size <= 10000

---

## 题目（中文翻译）

一个字符串仅由字符 `'('` 和 `')'` 组成，且满足配对规则时，被称为合法括号字符串（valid parentheses string，VPS）。  
我们可以类似地为任意 VPS **S** 定义其**嵌套深度**（nesting depth）`depth(S)`，其含义为在 **S** 中出现的最大左括号的层数。

例如，`""`、`"()()"`、`"()(()())"` 均是 VPS，对应的嵌套深度分别为 `0、1、2`；而 `")("` 和 `"(()"` 不是 VPS。

给定一个 VPS `seq`，将其划分为两个不相交的子序列（subsequence）`A` 与 `B`，要求 `A` 与 `B` 均为 VPS，且满足 `A.length + B.length = seq.length`。  
在所有可能的划分方式中，选取使 `max(depth(A), depth(B))` 最小的那一对 `A`、`B`。  
返回一个长度等于 `seq.length` 的答案数组 `answer`，用于描述上述划分：若 `seq[i]` 属于子序列 `A`，则 `answer[i] = 0`；否则 `answer[i] = 1`。  
若存在多种最优划分，返回任意一种即可。

**示例 1**  
输入: `seq = "(()())"`  
输出: `[0,1,1,1,1,0]`

**示例 2**  
输入: `seq = "()(())()"`  
输出: `[0,0,0,1,1,0,1,1]`

**约束条件**  

- `1 <= seq.size <= 10000`  
- `seq` 只包含字符 `'('` 和 `')'`，并且是一个合法括号字符串（VPS）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个括号都尝试放进 A 或 B 两个序列**，然后检查这两个序列是否都是合法的括号串（VPS），再计算它们各自的最大嵌套深度，最后挑选出 `max(depth(A), depth(B))` 最小的那一种。  

- **数据结构**：我们只需要用 **列表** 来保存 A、B 的字符序列，用 **栈**（可以用 Python 的 list 当栈）来判断一个序列是否是合法的 VPS。栈的工作原理类似“查字典”：遇到左括号 `(` 就把它压进去，遇到右括号 `)` 就把栈顶的左括号弹出来，如果在弹出时栈已经空了，说明出现了不匹配的右括号，这个序列就不合法。  
- **正确性**：因为我们枚举了 **所有** 可能的划分（每个字符都有两种放法），只要有一种划分满足题目要求，枚举过程一定会找到它。随后比较所有合法划分的 `max(depth(A), depth(B))`，取最小值，自然得到答案。  

#### 代码（Python）

```python
def is_vps(s: str) -> bool:
    """判断字符串 s 是否是合法的括号串（VPS）"""
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)          # 左括号入栈
        else:  # ch == ')'
            if not stack:             # 栈空却遇到右括号，不合法
                return False
            stack.pop()               # 匹配成功，弹出左括号
    return not stack                  # 栈空说明全部匹配

def depth(s: str) -> int:
    """计算 VPS s 的最大嵌套深度"""
    cur = max_d = 0
    for ch in s:
        if ch == '(':
            cur += 1
            max_d = max(max_d, cur)
        else:
            cur -= 1
    return max_d

def brute(seq: str):
    n = len(seq)
    best_ans = None
    best_max_depth = float('inf')

    # 使用深度优先搜索遍历所有 2^n 种分配方式
    def dfs(idx, a, b, assign):
        nonlocal best_ans, best_max_depth
        if idx == n:
            A = ''.join(a)
            B = ''.join(b)
            if is_vps(A) and is_vps(B):
                cur_max = max(depth(A), depth(B))
                if cur_max < best_max_depth:
                    best_max_depth = cur_max
                    best_ans = assign[:]   # 复制当前的 0/1 列表
            return

        # 选 0 → 放入 A
        a.append(seq[idx])
        assign.append(0)
        dfs(idx + 1, a, b, assign)
        a.pop()
        assign.pop()

        # 选 1 → 放入 B
        b.append(seq[idx])
        assign.append(1)
        dfs(idx + 1, a, b, assign)
        b.pop()
        assign.pop()

    dfs(0, [], [], [])
    return best_ans
```

> 这段代码可以直接运行，不过只适用于 **非常短** 的 `seq`（比如长度 ≤ 12），因为后面的搜索会非常慢。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - 解释：每个字符有 2 种放法，`2^n` 种组合。对每一种组合我们都要遍历一次整个字符串来判断合法性和计算深度，耗时 `O(n)`。所以总共是指数级别的时间，随着 `n` 增大会“炸裂”。  
- **空间复杂度**：`O(n)`  
  - 解释：递归栈最多占 `n` 层，同时我们用的临时列表 `a`、`b`、`assign` 也最多各存 `n` 个字符。

> 由于 `seq` 的长度可达 10⁴，暴力解根本不可用，只能作为思考的起点。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有划分是不可行的**。我们需要一种 **一次遍历就能决定每个括号放进 A 还是 B** 的策略。观察题目：

- 原始序列 `seq` 本身是合法的 VPS，说明它的左括号总是能在后面的右括号匹配。  
- **嵌套深度** 只和左括号出现的层数有关：第 1 层、2 层、3 层…。如果我们把 **奇数层的左括号放进 A，偶数层的左括号放进 B**（右括号同理放进对应的序列），那么 A、B 的深度就会被“平均分配”。  

直观的类比：想象把一座 **多层楼的建筑** 的楼层分配给两支施工队。每层楼只安排一支队伍，奇数层给队伍 0，偶数层给队伍 1，这样两支队伍的工作量（最高层数）相差不大，最大层数等于原来最高层数的一半（向上取整）。

实现细节：

1. **遍历 `seq`，用一个变量 `cur_depth` 记录当前的嵌套深度**（左括号 `(` 深度加 1，右括号 `)` 深度减 1）。  
2. 当遇到左括号时，先 **把深度加 1**，得到它所在的层数 `cur_depth`。把 `cur_depth % 2` 作为该左括号的分配标记（0 → A，1 → B）。  
3. 当遇到右括号时，它一定要匹配最近的左括号。此时 **先使用当前深度的奇偶性决定归属**（因为右括号对应的左括号已经在同一层），随后 **把深度减 1**。  

这样做的好处：

- **合法性保证**：左括号和对应的右括号永远分配到同一个序列，因为它们的层数相同。于是每个序列内部仍然是合法的 VPS。  
- **深度最小化**：原序列的最大深度记为 `D`。奇偶分配后，两个序列的最大深度至多是 `⌈D/2⌉`，这是可以达到的最小值（证明略，可理解为把 `D` 层尽量均分）。  

#### 代码（Python）

```python
def maxDepthAfterSplit(seq: str):
    """
    将合法的括号序列 seq 拆分成两个合法子序列，使得
    max(depth(A), depth(B)) 最小，返回划分方案（0 表示 A，1 表示 B）。
    思路：奇偶层分配。
    """
    ans = []               # 最终答案数组
    cur_depth = 0          # 当前遍历到的位置的嵌套深度

    for ch in seq:
        if ch == '(':
            cur_depth += 1                     # 进入新的一层
            ans.append(cur_depth % 2)          # 奇数层 -> 1，偶数层 -> 0（或相反都行）
        else:  # ch == ')'
            ans.append(cur_depth % 2)          # 右括号归属于当前层
            cur_depth -= 1                     # 退出这一层

    return ans
```

> 代码只遍历一次字符串，时间非常快。注释已用中文解释每一步的意义。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：只需要一次线性扫描，`n` 为字符串长度（最多 10⁴），每个字符的处理时间是常数。相比暴力的指数级别，快得多。  
- **空间复杂度**：`O(n)`  
  - 解释：返回的答案数组本身需要 `n` 个整数（0/1），除此之外只用了几个整数变量。

> 实际上，如果不需要返回完整的答案，只要知道最大深度，也可以在遍历时直接取 `max_depth = max(max_depth, cur_depth)`，但本题要求返回划分方案，所以必须保存 `ans`。

---

## 心得

- **核心技巧**：**层数的奇偶性划分**（也叫 “交替分配”）。通过把同一层的左/右括号统一分配到同一个子序列，保证子序列合法且深度均衡。  
- **适用的题型**：  
  1. **Maximum Nesting Depth of Two Valid Parentheses Strings**（本题）。  
  2. **Split a String Into the Max Number of Unique Substrings**（利用贪心分配）。  
  3. **Balanced String Split**（把字符按出现次数奇偶分配，以保持平衡）。  
- **一句话总结**：**把“层”当成“颜色”，交替上色即可最小化两支队伍的最高层数**。

---

## 反思

- **第一反应**：看到“把一个合法括号串拆成两段仍合法”，立刻想到**枚举所有划分**，因为最直接的思路总是先穷举。  
- **最容易踩的坑**：  
  - **忘记右括号的归属**：右括号必须和它对应的左括号放在同一子序列，否则子序列会出现不匹配。  
  - **深度计数顺序错误**：在处理左括号时要先 `depth += 1` 再决定归属；右括号则要先决定归属再 `depth -= 1`，否则会导致层数错位。  
  - **忽视空串**：输入可能只有一对括号，算法仍然要正确返回 `[0,0]` 或 `[1,1]`。  
- **下次遇到同类题**：第一步先**思考“层次结构”是否可以用奇偶或其他属性划分**，寻找能在一次遍历中同时保证合法性和均衡性的贪心/交替策略，而不是直接暴力枚举。