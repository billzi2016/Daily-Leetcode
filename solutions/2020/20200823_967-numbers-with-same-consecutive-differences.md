# #967. **相同连续差的数字** / Numbers With Same Consecutive Differences

> 难度：中等 · 标签：Backtracking、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/numbers-with-same-consecutive-differences/)

---

## 题目（英文原版）

**Description**

Given two integers n and k, return an array of all the integers of length n where the difference between every two consecutive digits is k. You may return the answer in any order.
Note that the integers should not have leading zeros. Integers as 02 and 043 are not allowed.

**Examples**

**Example 1:**

```
Input: n = 3, k = 7
Output: [181,292,707,818,929]
Explanation: Note that 070 is not a valid number, because it has leading zeroes.
```

**Example 2:**

```
Input: n = 2, k = 1
Output: [10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98]
```

**Constraints**

- 2 <= n <= 9
- 0 <= k <= 9

---

## 题目（中文翻译）

给定两个整数 `n` 和 `k`，返回所有长度为 `n` 的整数数组，使得每两个相邻数字之间的差的绝对值为 `k`。答案可以以任意顺序返回。  
请注意，整数不能有前导零。例如 `02`、`043` 都是不合法的。

**示例 1**  

**示例 2**  

**约束条件**  

**示例**  
**示例 1:**  
```
Input: n = 3, k = 7
Output: [181,292,707,818,929]
```
**解释:** 需要注意 `070` 不是合法的数字，因为它有前导零。

**示例 2:**  
```
Input: n = 2, k = 1
Output: [10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98]
```

**约束条件:**  
- `2 <= n <= 9`  
- `0 <= k <= 9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 n 位整数都枚举出来**，然后逐个检查相邻两位数字的差是否等于 k。

- **枚举**：从 10^(n‑1) 到 10^n‑1（因为不能出现前导零），把每个整数拆成字符数组或数字列表，逐位比较。
- **数据结构类比**：把每个整数想象成一本书的章节编号，遍历所有章节就像“翻遍整本字典”。  
- **正确性**：我们把**所有合法的 n 位数**都检查了一遍，只要相邻差为 k，就把它加入答案，必然不会漏掉，也不会多加不符合条件的数。

#### 代码（Python）

```python
def numsSameConsecDiff_bruteforce(n: int, k: int):
    ans = []
    # 10^(n-1) 是最小的 n 位数（不含前导零），10^n-1 是最大 n 位数
    start = 10 ** (n - 1)
    end = 10 ** n
    for num in range(start, end):
        s = str(num)                 # 把整数转成字符串，方便逐位访问
        ok = True
        for i in range(1, n):
            # 前后两位数字的差的绝对值
            if abs(int(s[i]) - int(s[i - 1])) != k:
                ok = False
                break
        if ok:
            ans.append(num)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(10^{n})`  
  解释：我们遍历了从 10^{n‑1} 到 10^{n}‑1 共 9·10^{n‑1} ≈ 10^{n} 个数，每个数最多检查 n‑1 次相邻差。因此整体是指数级的，`n` 增大时会很快失去实用性。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了常数级的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**遍历了大量不可能满足条件的数**。实际上，满足相邻差为 k 的数可以**一步步构造**出来：

1. **首位**只能是 1~9（不能为 0）。
2. 对于已经构造好的前缀 `prefix`，我们只需要在最后一位 `last` 的基础上尝试两种可能的下一位：
   - `next = last + k`
   - `next = last - k`
3. 只要 `next` 落在 0~9 之间，就可以把它接在 `prefix` 后面，形成更长的前缀。  
4. 重复上述过程，直到前缀长度达到 n，得到完整的答案。

这就是典型的**回溯（Backtracking）**或**广度优先搜索（BFS）**。这里用 **DFS（递归）** 实现更直观：

- **递归树的每一层**对应数位的位置。  
- **分支**数目最多为 2（`+k` 与 `-k`），所以整体节点数为 `9 * 2^{(n-1)}`，远小于 `10^{n}`。

> **关键概念解释**  
> - **回溯**：像在迷宫里走一步，如果走不通就“回头”撤销这一步，尝试另一条路。这里的“撤销”就是把最后加的数字弹出来。  
> - **前缀**：已经确定好的左侧数字序列。我们只关心它的最后一位，因为下一位只能由它决定。

#### 代码（Python）

```python
def numsSameConsecDiff(n: int, k: int):
    """
    使用深度优先搜索（递归）构造所有满足条件的 n 位数。
    """
    if n == 1:                     # 题目保证 n >= 2，但保留这个分支以防万一
        return list(range(10))

    ans = []

    def dfs(pos: int, cur: int):
        """
        pos  : 已经构造好的位数（从 1 开始计数）
        cur  : 当前的整数（前缀），例如 pos=3, cur=181 表示已经有 "181"
        """
        if pos == n:               # 前缀已经够长，收集答案
            ans.append(cur)
            return

        last_digit = cur % 10      # 取出当前整数的最后一位
        # 计算可能的下一位
        next_digits = set()
        next_digits.add(last_digit + k)
        next_digits.add(last_digit - k)

        for nd in next_digits:
            if 0 <= nd <= 9:        # 下一位必须是合法的十进制数字
                dfs(pos + 1, cur * 10 + nd)   # 把 nd 接在后面，继续往下走

    # 首位只能是 1~9（不能是 0），因为不允许前导零
    for first in range(1, 10):
        dfs(1, first)

    return ans
```

> **代码要点**  
> - `cur % 10` 取出当前整数的**最后一位**，相当于“看前缀的最右边”。  
> - `set()` 去重：当 `k == 0` 时，`last_digit + k` 与 `last_digit - k` 相同，只需要走一次分支。  
> - `cur * 10 + nd` 把新数字 `nd` 加到整数的末尾，类似“在左边已经写好的数字后面继续写”。  

#### 复杂度  

- **时间复杂度**：`O(9 * 2^{(n-1)})`  
  解释：首位有 9 种选择（1~9），之后每一位最多产生 2 条分支，所以总节点数不超过 `9·2^{n-1}`。对比暴力的 `10^{n}`，指数底数从 10 降到了 2，明显更快。  
- **空间复杂度**：`O(n)`（递归栈深度）  
  递归最多深入 n 层，每层保存少量局部变量，空间随 n 线性增长。答案本身的存储不计入额外空间。

---

## 心得

- **核心技巧**：**利用相邻位的约束进行逐位构造**（回溯 / BFS），把全局搜索空间从 `10^n` 大幅压缩到 `9·2^{n-1}`。  
- **适用的题型**  
  1. “数字的每一位满足某种关系”——如 **`N-Queens`** 中每行只能放一个皇后的约束（回溯）。  
  2. “路径上每一步只能走特定步长”——如 **`Word Ladder`**（BFS）。  
  3. “从左到右递增/递减的序列”——如 **`Combination Sum`**（回溯）。  
- **一句话总结**：**把“检查”变成“生成”，让搜索只在可能的分支上进行**。

---

## 反思

- **第一反应**：直接枚举所有 n 位数，检查相邻差是否为 k。  
- **最容易踩的坑**  
  1. **前导零**：首位不能是 0，需要单独处理。  
  2. **k = 0** 时会产生重复分支，需要去重（使用 `set` 或判断 `+k` 与 `-k` 是否相等）。  
  3. **边界条件**：n = 2、k = 9 等极端情况仍然要产生合法答案（如 `90`、`09`（非法））。  
- **下次遇到同类题**：第一步先思考**是否可以从左到右逐位构造**，把约束转化为“下一位只能是哪些值”，再决定使用 **DFS（回溯）** 还是 **BFS**。这样往往能立刻把搜索空间压到指数底数 2 左右。