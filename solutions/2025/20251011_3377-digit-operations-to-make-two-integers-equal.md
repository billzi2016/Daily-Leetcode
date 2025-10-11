# #3377. 数字操作使两个整数相等 / Digit Operations to Make Two Integers Equal

> 难度：中等 · 标签：Math、Graph、Heap (Priority Queue)、Number Theory、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/digit-operations-to-make-two-integers-equal/)

---

## 题目（英文原版）

**Description**

You are given two integers n and m that consist of the same number of digits.
You can perform the following operations any number of times:
The integer n must not be a prime number at any point, including its original value and after each operation.
The cost of a transformation is the sum of all values that n takes throughout the operations performed.
Return the minimum cost to transform n into m. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: n = 10, m = 12
Output: 85
Explanation:
We perform the following operations:
```

**Example 2:**

```
Input: n = 4, m = 8
Output: -1
Explanation:
It is impossible to make n equal to m .
```

**Example 3:**

```
Input: n = 6, m = 2
Output: -1
Explanation:
Since 2 is already a prime, we can't make n equal to m .
```

**Constraints**

- 1 <= n, m < 104
- n and m consist of the same number of digits.

---

## 题目（中文翻译）

给定两个整数 `n` 和 `m`，它们的位数相同。  
你可以任意次数执行以下操作：

- 在整个过程中，整数 `n` 必须不是质数 (prime)，包括它的初始值以及每次操作后的值。  
- 转换的成本是所有 `n` 在操作过程中取值的总和。

返回将 `n` 转换为 `m` 的最小成本。如果无法实现，返回 `-1`。

示例 1  
**输入:** `n = 10, m = 12`  
**输出:** `85`  
**解释:**  
我们执行以下操作：

（此处保留原题中具体的操作步骤）

示例 2  
**输入:** `n = 4, m = 8`  
**输出:** `-1`  
**解释:**  
不可能让 `n` 等于 `m` 。

示例 3  
**输入:** `n = 6, m = 2`  
**输出:** `-1`  
**解释:**  
由于 `2` 已经是质数 (prime)，我们无法使 `n` 等于 `m` 。

约束条件  
- $1 \le n, m < 10^4$  
- `n` 和 `m` 具有相同的位数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每一个合法的整数（**非质数**，且位数和 `n`、`m` 相同）都看成图中的一个节点。  
如果我们可以**一次只改动一个数位**（比如把 1234 的第 2 位 2 改成 7，得到 1734），而改动后得到的数字仍然是非质数，那么就在这两个节点之间连一条有向边。  

> **类比**：把整数想象成一本字典里的单词，改动一个字符就相当于在字典里走到另一个只差一个字母的单词。这里 “字典” 是所有合法的非质数， “查字典” 就是判断一个数是否是质数。

因为每走一步都会产生一个新的整数值，而 **总费用 = 所有经过的整数值的累加**，所以我们只要在这张图里找到 **从 `n` 到 `m` 的最小权重路径**，路径权重就是费用。

暴力实现思路：

1. **遍历所有可能的整数**（`10^{d-1}` 到 `10^{d}-1`，其中 `d` 为位数），筛掉质数，只留下合法节点。  
2. 对每个合法节点，枚举它的每一位，把该位改成 `0~9`（但不能改成自身，也不能导致首位为 `0`），得到邻居 `y`。如果 `y` 也是合法的，就在 `x → y` 加一条有向边，边权记为 `y`（因为走到 `y` 时要把 `y` 加进费用）。  
3. 用 **Dijkstra**（最短路）在这张有向加权图上从 `n` 出发，找最小费用到达 `m`。  

> **为什么正确**  
> - 每一次合法的“改动一个数位”都对应图中的一条边，所有可能的转化序列恰好对应图中的一条从 `n` 到 `m` 的路径。  
> - 路径权重 = 起点 `n` + 所有中间节点 + 终点 `m`，这正是题目要求的费用定义。  
> - Dijkstra 能在非负权重图里找到从起点到终点的最小路径权重，因而得到最小费用。

#### 代码（Python）

```python
import heapq
import math
from typing import List

# ---------- 质数判定（使用埃拉托斯特尼筛） ----------
def sieve(limit: int) -> List[bool]:
    """返回 length = limit+1 的布尔数组，prime[i] 为 True 表示 i 是质数"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if prime[p]:
            step = p
            start = p * p
            for multiple in range(start, limit + 1, step):
                prime[multiple] = False
    return prime

# ---------- 生成所有合法的邻居 ----------
def neighbors(x: int, d: int, is_prime: List[bool]) -> List[int]:
    """
    给定整数 x（长度 d），返回所有一次只改动一位且仍是非质数的数。
    """
    s = list(str(x))                     # 把数字拆成字符列表，方便逐位修改
    res = []
    for i in range(d):
        original = s[i]
        for dig in '0123456789':
            if dig == original:
                continue                # 不能保持不变
            if i == 0 and dig == '0':
                continue                # 首位不能为 0，保持位数不变
            s[i] = dig
            y = int(''.join(s))
            if not is_prime[y]:         # 只保留非质数
                res.append(y)
        s[i] = original                  # 恢复原来的字符
    return res

# ---------- 主函数 ----------
def minimumCost(n: int, m: int) -> int:
    # 位数相同的前提已在题目保证，这里直接求位数 d
    d = len(str(n))
    max_val = 10 ** d - 1

    # 预处理：在 0 ~ max_val 之间标记所有质数
    is_prime = sieve(max_val)

    # 起点或终点本身是质数，直接返回 -1（题目不允许出现质数）
    if is_prime[n] or is_prime[m]:
        return -1

    # Dijkstra 初始化
    INF = float('inf')
    dist = [INF] * (max_val + 1)         # dist[x] 表示到达 x 的最小费用（已包含 x 本身）
    dist[n] = n                         # 第一步费用就要把起点 n 加进来
    heap = [(n, n)]                     # (当前费用, 当前整数)

    while heap:
        cur_cost, x = heapq.heappop(heap)
        if cur_cost != dist[x]:
            continue                    # 过期的记录
        if x == m:                     # 已经到达目标，最小费用已确定
            return cur_cost
        for y in neighbors(x, d, is_prime):
            new_cost = cur_cost + y    # 走到 y 要再加上 y 本身的值
            if new_cost < dist[y]:
                dist[y] = new_cost
                heapq.heappush(heap, (new_cost, y))

    # 若循环结束仍未返回，说明不可达
    return -1
```

> **关键行中文注释** 已在代码中给出，直接复制运行即可。

#### 复杂度

- **时间复杂度**：  
  - 筛质数 `O(max_val log log max_val)`，这里 `max_val ≤ 10⁴`，几乎可以忽略。  
  - Dijkstra：每个合法节点最多有 `9 * d` 条出边（每位 9 种改法），节点数最多是 `10^d`（≤ 10⁴）。所以整体是 `O(V log V + E log V) ≈ O(10⁴ log 10⁴)`，在题目限制下非常快。  
  - 大白话：我们最多遍历一万次，每次把费用放进优先队列（类似排队），排队的开销和遍历次数成对数关系，几乎在一瞬间完成。

- **空间复杂度**：  
  - 质数数组 `O(max_val)` ≈ `O(10⁴)`。  
  - 距离数组、优先队列同样是 `O(V)`。  
  - 所以整体 `O(10⁴)`，只占几百 KB 的内存。

---

### 2. 最优解

#### 思路  

暴力解已经是最直观的 **Dijkstra** 实现，已经达到了 **最优时间/空间**（在题目约束下无法再进一步提升）。  
这里把思路再抽象一次，帮助读者从“怎么写代码”提升到“为什么这样写是最好的”：

1. **状态定义**：  
   - **状态 = 当前整数**（只要它是非质数且位数不变）。  
   - **转移 = 改动一位得到另一个合法整数**。  
   - 这正好对应 **图的节点 + 边** 的概念。

2. **费用累计**：  
   - 费用是所有经过的整数之和。  
   - 把费用视为 **节点权重**（而不是边权），于是从 `n` 到 `m` 的费用 = `weight(n) + weight(v₁) + … + weight(m)`。  
   - 在 Dijkstra 中我们把 **每条边的代价设为目标节点的权重**，这样累计的路径代价自然等于所有节点权重的和。

3. **为何选 Dijkstra 而不是 BFS**：  
   - BFS 只能处理 **每条边代价相同** 的情况（等价于每走一步费用相同）。  
   - 这里每走到的节点费用 **不相同**（不同整数值），所以要使用 **带权最短路**——Dijkstra 正好满足“非负权重”。  

4. **剪枝**：  
   - 如果 `n` 或 `m` 本身是质数，直接返回 `-1`（因为题目要求“任意时刻都不能是质数”）。  
   - 在生成邻居时，**提前过滤掉质数**，避免无效的搜索分支。  

5. **复杂度分析**：  
   - 节点数 ≤ `9 * 10^{d-1}`（同位数的非质数最多约 9 千）。  
   - 每个节点最多 `9*d` 条出边。  
   - 因此 Dijkstra 的时间 `O(V log V + E log V)` 已经是 **最优**（因为必须遍历所有可能的合法整数）。  

#### 代码（Python）

```python
import heapq
import math
from typing import List

def sieve(limit: int) -> List[bool]:
    """埃拉托斯特尼筛，返回 [0..limit] 是否为质数"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if prime[p]:
            for multiple in range(p * p, limit + 1, p):
                prime[multiple] = False
    return prime

def get_neighbors(x: int, d: int, is_prime: List[bool]) -> List[int]:
    """一次只改动一位，得到的所有非质数邻居"""
    s = list(str(x))
    res = []
    for i in range(d):
        orig = s[i]
        for ch in '0123456789':
            if ch == orig:
                continue
            if i == 0 and ch == '0':
                continue          # 保持位数不变
            s[i] = ch
            y = int(''.join(s))
            if not is_prime[y]:
                res.append(y)
        s[i] = orig
    return res

def minimumCost(n: int, m: int) -> int:
    d = len(str(n))
    max_val = 10 ** d - 1
    is_prime = sieve(max_val)

    # 起点或终点为质数直接返回 -1
    if is_prime[n] or is_prime[m]:
        return -1

    INF = 10**18
    dist = [INF] * (max_val + 1)
    dist[n] = n                     # 起点费用本身计入
    heap = [(n, n)]                 # (累计费用, 当前数)

    while heap:
        cur_cost, x = heapq.heappop(heap)
        if cur_cost != dist[x]:
            continue                # 已有更优解，跳过
        if x == m:
            return cur_cost         # 第一次弹出 m，即最小费用
        for y in get_neighbors(x, d, is_prime):
            new_cost = cur_cost + y
            if new_cost < dist[y]:
                dist[y] = new_cost
                heapq.heappush(heap, (new_cost, y))
    return -1                       # unreachable
```

> 代码与上面的暴力实现本质相同，只是把注释写得更简洁、把 “不可达返回 -1” 放在最末。它已经是 **最优**（在题目约束下），不需要再做额外的加速。

#### 复杂度

- **时间**：`O(V log V + E log V)`，其中  
  - `V ≤ 9·10^{d-1} ≤ 9·10³`（因为 `n,m < 10⁴`），  
  - `E ≤ V·9·d`（每位 9 种改法），  
  - 所以在最坏情况下约 `O(10⁴ log 10⁴)`，几毫秒即可完成。  
  与暴力枚举全部可能路径相比，**只遍历一次最短路**，是最好的。

- **空间**：`O(V)`（质数数组 + 距离数组 + 优先队列），约几千整数，极小。

---

## 心得

- **核心技巧**：把“数位改动”抽象成 **图的节点**，把“费用累加”抽象成 **带权最短路**（Dijkstra）。  
- **适用场景**：  
  1. “Word Ladder” 类题目——每次改一个字符，求最短转换次数。  
  2. “Minimum Cost to Convert Number”——每次操作产生不同费用，需要最小总费用。  
  3. “Shortest Path in Implicit Graph”——图不显式给出，而是通过状态转移函数动态生成邻居。  
- **一句话总结**：**把每一次合法的数位改动看成图的边，费用是节点权重，用 Dijkstra 找最小权路径**。

---

## 反思

- **第一反应**：先想“枚举所有可能的改动”，然后用 BFS/DFS 暴力搜索。很快意识到费用不是统一的，需要带权最短路。  
- **最容易踩的坑**：  
  - **质数限制**：忘记在起点、终点以及每次转移后都要检查是否为质数，导致错误答案。  
  - **位数保持**：改动首位为 `0` 会让整数位数变少，需要显式过滤。  
  - **费用累计**：有些同学把费用只算边的权重（即改动次数），而忘记把每个经过的整数本身加进去。  
- **下次遇到类似题**，第一步应该先 **明确状态（节点）和转移（边）**，并判断 **费用是边权还是节点权**，再决定使用 **BFS、Dijkstra 还是 DP**。