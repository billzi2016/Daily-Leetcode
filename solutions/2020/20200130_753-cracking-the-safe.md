# #753. 破解保险箱 / Cracking the Safe

> 难度：困难 · 标签：Depth-First Search、Graph、Eulerian Circuit · [LeetCode 链接](https://leetcode.com/problems/cracking-the-safe/)

---

## 题目（英文原版）

**Description**

There is a safe protected by a password. The password is a sequence of n digits where each digit can be in the range [0, k - 1].
The safe has a peculiar way of checking the password. When you enter in a sequence, it checks the most recent n digits that were entered each time you type a digit.
Return any string of minimum length that will unlock the safe at some point of entering it.

**Examples**

**Example 1:**

```
Input: n = 1, k = 2
Output: "10"
Explanation: The password is a single digit, so enter each digit. "01" would also unlock the safe.
```

**Example 2:**

```
Input: n = 2, k = 2
Output: "01100"
Explanation: For each possible password:
- "00" is typed in starting from the 4th digit.
- "01" is typed in starting from the 1st digit.
- "10" is typed in starting from the 3rd digit.
- "11" is typed in starting from the 2nd digit.
Thus "01100" will unlock the safe. "10011", and "11001" would also unlock the safe.
```

**Constraints**

- 1 <= n <= 4
- 1 <= k <= 10
- 1 <= kn <= 4096

---

## 题目（中文翻译）

有一个保险箱受密码保护。密码是长度为 **n** 的数字序列，每个数字的取值范围为 **[0, k‑1]**。  
保险箱检查密码的方式很特殊：每当你输入一个数字时，它会检查最近输入的 **n** 个数字是否与密码匹配。  
返回任意一个 **最短** 的字符串，使得在输入该字符串的过程中，某一时刻能够解锁保险箱。

**示例 1**  
**输入**: `n = 1, k = 2`  
**输出**: `"10"`  
**解释**: 密码只有一位，因此只需依次输入每个可能的数字。`"01"` 同样能够解锁保险箱。

**示例 2**  
**输入**: `n = 2, k = 2`  
**输出**: `"01100"`  
**解释**: 对于所有可能的密码：  
- `"00"` 在第 4 位开始输入时出现。  
- `"01"` 在第 1 位开始输入时出现。  
- `"10"` 在第 3 位开始输入时出现。  
- `"11"` 在第 2 位开始输入时出现。  
因此 `"01100"` 能够解锁保险箱。`"10011"` 和 `"11001"` 也同样可行。

**约束条件**  
- `1 <= n <= 4`  
- `1 <= k <= 10`  
- `1 <= k^n <= 4096`   (即 `kn` 在原题中表示 `k^n`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的密码都列出来，然后把它们一个接一个地拼在一起**，只要在拼的过程中保证每个长度为 `n` 的子串恰好出现一次，就能得到一个可行的答案。

- **数据结构**  
  - `set seen`：像字典一样存已经出现过的 `n` 位子串。把它想成“记事本”，每记下一条就往里面写，查找时像查字典一样 O(1)。  
  - `string path`：当前已经输入的字符序列。我们不断往后追加字符，就像在纸上写字一样。

- **为什么正确**  
  只要最终的 `path` 包含了 **所有** `kⁿ` 种长度为 `n` 的组合（不管顺序），安全箱在某个时刻一定会看到正确的密码。因此，只要我们在回溯搜索中保证每一次新增的字符能够形成一个此前未出现的 `n` 位子串，最终的 `path` 必然满足题目要求。

- **时间/空间复杂度**  
  - 暴力搜索会尝试每一种可能的字符序列。每一步我们要检查新产生的子串是否已出现，检查是 O(1)（集合查找），但搜索树的深度是 `kⁿ + n - 1`，分支数是 `k`，所以最坏情况下的时间是 **指数级**，记作 `O(k^{k^n})`（实际会更小，但仍然是指数增长）。  
  - 需要保存所有已出现的子串，最多 `kⁿ` 个，空间是 `O(kⁿ)`。

> **大白话**：  
> `O(kⁿ)` 就是“和所有可能密码的数量成正比”。比如 `k=2,n=3` 时，`kⁿ=8`，所以我们要记 8 条子串。指数级 `O(k^{k^n})` 可以想象成“把每一种可能的输入顺序都尝试一次”，根本不可能在合理时间内完成。

#### 代码（Python）

```python
def crackSafe_brute(n: int, k: int) -> str:
    """暴力回溯求最短序列（仅用于理解，实际会超时）"""
    total = k ** n                     # 所有密码的数量
    seen = set()                       # 已出现的 n 位子串
    path = []                          # 当前拼好的字符列表

    # 初始时把前 n-1 位都填成 0，后面的搜索只负责补足最后一位
    path.extend(['0'] * (n - 1))

    def dfs() -> bool:
        """尝试继续往后写字符，返回是否已收集完全部子串"""
        if len(seen) == total:         # 已经见到所有密码
            return True

        # 依次尝试添加 0..k-1
        for digit in map(str, range(k)):
            path.append(digit)                         # 写下一个字符
            cur = ''.join(path[-n:])                   # 最近的 n 位子串
            if cur not in seen:                        # 这个子串是新出现的
                seen.add(cur)                          # 记下来
                if dfs():                              # 继续深入
                    return True
                seen.remove(cur)                      # 回溯：撤销记录
            path.pop()                                 # 回溯：把字符删掉
        return False

    dfs()
    return ''.join(path)
```

> 关键行解释  
> - `path.extend(['0'] * (n - 1))`：先把前 `n‑1` 位固定为 `'0'`，这样后面的搜索只需要关注每次加入的第 `n` 位子串。  
> - `cur = ''.join(path[-n:])`：取最近的 `n` 位，类似“刚才你敲的最后 n 键”。  
> - `if cur not in seen:`：如果这个子串以前没出现过，就可以接受这一步。  

#### 复杂度

- **时间复杂度**：`O(k^{k^n})`（指数级）——因为会遍历几乎所有可能的字符序列。  
- **空间复杂度**：`O(k^n)`——需要保存所有已经出现的长度为 `n` 的子串。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**不断回溯**，每一次尝试都要重新走很多已经走过的路。我们可以把问题抽象成一张**有向图**，把“已经访问过的子串”视作**边**，而“子串的前缀”视作**节点**。在这张图上找一条**欧拉回路**（Eulerian circuit）——一次走遍每条边且只走一次的回路，恰好对应我们要的最短序列。

**构造图**  

- 每个节点表示一个长度为 `n‑1` 的字符串。比如 `n=3` 时，节点有 `"00"、"01"、"10"、"11"`（共 `k^{n-1}` 个）。  
- 对于任意节点 `u`，我们可以向它**添加**任意一个数字 `d∈[0,k-1]`，形成新字符串 `u+d`（把 `d` 拼在后面）。取它的后 `n‑1` 位作为下一个节点 `v`。这条从 `u` 到 `v` 的有向边就对应**密码** `u+d`（长度为 `n` 的子串）。  

这样，每条边恰好对应一种可能的密码，边的总数是 `kⁿ`，正好是我们必须覆盖的子串数。

**欧拉回路的存在性**  

- 每个节点的**出度**（离开的边数）都是 `k`，**入度**（进入的边数）也都是 `k`，因为可以任意在前面补 `k` 种数字。  
- 当每个节点的入度等于出度且图是连通的时，欧拉回路必然存在。这里的图正好满足这些条件。

**如何求欧拉回路**  

使用 **Hierholzer 算法**（递归版 DFS）：

1. 从任意起点（这里取全 0 的节点）开始深度优先遍历。  
2. 对当前节点的每一条未使用的边 `digit`：  
   - 标记这条边已用（可以直接在循环里弹出）。  
   - 递归进入下一个节点 `next = (cur + digit)[1:]`（即去掉最左边的字符，只保留后 `n‑1` 位）。  
3. 当一个节点的所有出边都走完后，把 **走过的数字**加入答案序列。因为是递归后加入的，实际上得到的是**逆序**的欧拉回路。  
4. 最后在答案前面补上起点的 `n‑1` 个 `0`，得到完整的密码序列。

> **类比**：  
> 想象你在一座城镇的每条道路上都贴了编号（对应数字 `d`），你要走遍每条道路且不重复。你可以把城镇抽象成图，**一次走完所有道路**的路线就是欧拉回路。Hierholzer 就像你随手挑一条未走的路走到底，走不下去时回头把路标记下来，最后把所有路标倒着拼起来，就是完整的路线。

**为什么是最短**  

欧拉回路恰好走了 `kⁿ` 条边，每条边对应一个长度为 `n` 的子串。把路径转成字符序列时，只需要在最前面补 `n‑1` 个字符，其余每走一条边只多加 **一个** 字符。因此最终长度是 `kⁿ + n - 1`，这是已知的**De Bruijn 序列**的最短长度，下界不可再小。

#### 代码（Python）

```python
def crackSafe(n: int, k: int) -> str:
    """
    最优解：构造 De Bruijn 序列（欧拉回路）
    时间 O(k^n)   空间 O(k^{n-1})
    """
    if n == 1:                     # 特殊情况：只有一位密码，直接遍历 0..k-1
        return ''.join(str(i) for i in range(k))

    # 记录每个节点剩余未使用的出边，使用列表模拟栈，pop() 取最后一个
    # 节点用字符串表示，例如 "00"、"01"...
    edges = {''.join(p): list(map(str, range(k))) for p in
             __import__('itertools').product('0123456789'[:k], repeat=n-1)}

    circuit = []                   # 存放逆序的边（数字字符）

    def dfs(node: str):
        """Hierholzer 递归：遍历 node 的所有出边"""
        while edges[node]:         # 只要还有未使用的边
            digit = edges[node].pop()          # 取出一条边
            next_node = (node + digit)[1:]      # 形成下一个节点
            dfs(next_node)                     # 继续深搜
            circuit.append(digit)              # 回溯时记录走过的数字

    start = '0' * (n - 1)          # 任意起点，这里选全 0
    dfs(start)

    # circuit 现在是逆序的，把它反转并在前面补上起点的 n-1 位
    return start + ''.join(reversed(circuit))
```

> 关键行解释  
> - `edges = {...}`：为每个长度为 `n‑1` 的节点准备一份「未走的数字列表」，就像为每条路标记了「是否已走」的状态。  
> - `digit = edges[node].pop()`：取走一条未使用的路，`pop()` 同时把它从「未使用」集合里删掉。  
> - `next_node = (node + digit)[1:]`：把新加的数字拼进去，再去掉最左边的字符，得到下一个节点的名称。  
> - `circuit.append(digit)`：在回溯阶段把走过的数字加入答案，这一步会产生逆序，需要最后 `reversed`。  

#### 复杂度

- **时间复杂度**：`O(k^n)` —— 每条边（即每种密码）只被遍历一次，`k^n` 最多 4096，完全可接受。  
- **空间复杂度**：`O(k^{n-1})` —— 需要保存每个节点的出边列表，节点数是 `k^{n-1}`（最多 1000 左右），以及递归栈深度同样不超过 `k^n`。

> 与暴力解对比：  
> - 暴力解在搜索树上会重复走很多已经遍历过的路径，时间呈指数级增长。  
> - 最优解一次性走遍所有边，时间线性于答案规模，快得多。

---

## 心得

- **核心技巧**：把“遍历所有长度为 `n` 的子串”抽象成 **欧拉回路 / De Bruijn 序列**，用 **Hierholzer（递归 DFS）** 求解。  
- **适用的题型**  
  1. **Cracking the Safe**（本题）  
  2. **Construct Binary String With Substrings**（要求每个子串出现一次）  
  3. **Find the Shortest Superstring**（在特定限制下可转化为欧拉回路）  
- **一句话总结**：  
  *把密码看成图的边，走一次遍历所有边的欧拉回路，就是最短的解锁序列。*

---

## 反思

- **第一反应**：直接想 “枚举所有密码，然后拼起来”。这导致了指数级的回溯，效率太低。  
- **最容易踩的坑**  
  - **边界条件**：`n = 1` 时，图的节点数为 `k⁰ = 1`，需要单独处理，否则 `edges` 会出现空字符串的键。  
  - **递归深度**：Python 默认递归深度约 1000，`kⁿ` 最多 4096，仍在安全范围，但如果改用迭代版 `stack` 更稳妥。  
  - **字符类型**：`digit` 必须是字符串，拼接时不能混用整数，否则会报类型错误。  
- **下次遇到同类题**：第一步先**思考能否把问题映射成图**（节点/边），检查入度/出度是否相等，判断是否存在欧拉回路；如果符合，就直接上 Hierholzer。这样可以立刻把指数级搜索降到线性。