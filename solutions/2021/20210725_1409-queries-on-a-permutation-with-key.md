# #1409. 查询置换中的键 / Queries on a Permutation With Key

> 难度：中等 · 标签：Array、Binary Indexed Tree、Simulation · [LeetCode 链接](https://leetcode.com/problems/queries-on-a-permutation-with-key/)

---

## 题目（英文原版）

**Description**

Given the array queries of positive integers between 1 and m, you have to process all queries[i] (from i=0 to i=queries.length-1) according to the following rules:
Return an array containing the result for the given queries.

**Examples**

**Example 1:**

```
Input: queries = [3,1,2,1], m = 5
Output: [2,1,2,1] 
Explanation: The queries are processed as follow: 
For i=0: queries[i]=3, P=[1,2,3,4,5], position of 3 in P is 2, then we move 3 to the beginning of P resulting in P=[3,1,2,4,5]. 
For i=1: queries[i]=1, P=[3,1,2,4,5], position of 1 in P is 1, then we move 1 to the beginning of P resulting in P=[1,3,2,4,5]. 
For i=2: queries[i]=2, P=[1,3,2,4,5], position of 2 in P is 2, then we move 2 to the beginning of P resulting in P=[2,1,3,4,5]. 
For i=3: queries[i]=1, P=[2,1,3,4,5], position of 1 in P is 1, then we move 1 to the beginning of P resulting in P=[1,2,3,4,5]. 
Therefore, the array containing the result is [2,1,2,1].
```

**Example 2:**

```
Input: queries = [4,1,2,2], m = 4
Output: [3,1,2,0]
```

**Example 3:**

```
Input: queries = [7,5,5,8,3], m = 8
Output: [6,5,0,7,5]
```

**Constraints**

- 1 <= m <= 10^3
- 1 <= queries.length <= m
- 1 <= queries[i] <= m

---

## 题目（中文翻译）

给定一个正整数数组 `queries`（元素取值在 `1` 到 `m` 之间），以及一个整数 `m`。  
初始时，构造一个排列（permutation）`P = [1, 2, 3, …, m]`。  
随后依次处理 `queries[i]`（`i` 从 `0` 到 `queries.length‑1`），遵循以下规则：

1. 找到 `queries[i]` 在当前排列 `P` 中的位置（下标从 `0` 开始），记为 `pos`。  
2. 将 `pos` 加入答案数组。  
3. 将 `queries[i]` 移动到 `P` 的开头，使得 `P` 变为 `[queries[i]] + P`（去掉原来的该元素后再拼接）。

返回包含所有查询结果的数组。

**示例 1**  
``` 
Input: queries = [3,1,2,1], m = 5
Output: [2,1,2,1] 
Explanation: 
- i = 0: queries[i] = 3, P = [1,2,3,4,5]，3 在 P 中的位置是 2，随后把 3 移到开头，得到 P = [3,1,2,4,5]。  
- i = 1: queries[i] = 1, P = [3,1,2,4,5]，1 在 P 中的位置是 1，随后把 1 移到开头，得到 P = [1,3,2,4,5]。  
- i = 2: queries[i] = 2, P = [1,3,2,4,5]，2 在 P 中的位置是 2，随后把 2 移到开头，得到 P = [2,1,3,4,5]。  
- i = 3: queries[i] = 1, P = [2,1,3,4,5]，1 在 P 中的位置是 1，随后把 1 移到开头，得到 P = [1,2,3,4,5]。  
答案数组即为 [2,1,2,1]。 
```

**示例 2**  
```
Input: queries = [4,1,2,2], m = 4
Output: [3,1,2,0]
```

**示例 3**  
```
Input: queries = [7,5,5,8,3], m = 8
Output: [6,5,0,7,5]
```

**约束条件**  

- `1 <= m <= 10^3`  
- `1 <= queries.length <= m`  
- `1 <= queries[i] <= m`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的做法就是把整个排列 **P = [1,2,…,m]** 用一个普通的 Python 列表保存。  
对于每一次查询 `queries[i]`：

1. **顺序扫描** `P`，找到 `queries[i]` 所在的下标 `pos`（下标从 0 开始）。这一步就像在一本电话本里**从头到尾找名字**，最慢但最直观。  
2. 把 `pos` 加 1（因为题目要求返回的是**位置**，从 1 开始计数），记入答案数组。  
3. 将找到的元素 **移动到列表最前面**，其余元素向后挪一位。实现上可以先 `pop(pos)` 再 `insert(0, x)`，相当于把这个元素“提到前面”。  

> **数据结构类比**  
> - Python 列表就像一排排座位，`pop` 相当于把坐在第 `pos` 位的同学请出教室，`insert(0, x)` 就是把他重新安排坐到第一排的最左边。  

**为什么正确**  
因为我们每一步都严格按照题目描述的“找到位置 → 记录位置 → 把该数字移到最前面”来操作，整个过程完全模拟了题目中的规则，自然会得到正确答案。

**复杂度分析（大白话）**  
- **时间**：每一次查询我们都要 **遍历整个列表** 来找位置，最坏情况下要看 `m` 个数。查询总数是 `len(queries)`，记作 `n`。于是时间复杂度是 `O(n * m)`。如果把 `n` 当成和 `m` 同级（题目里 `n ≤ m`），最坏大约是 `O(m²)`，也就是“把 `m` 张纸每张都看 `m` 次”。  
- **空间**：我们只保存原始排列和答案数组，都是长度 `m` 和 `n`，所以是 `O(m + n)`，在本题里可以看作 `O(m)`。

#### 代码（Python）  

```python
def processQueries(queries, m):
    # 初始化排列 P = [1,2,...,m]
    perm = list(range(1, m + 1))
    ans = []                       # 用来存放每一次查询的结果

    for q in queries:              # 逐个处理查询
        # 线性扫描找位置（下标从 0 开始），相当于在列表里“找字典”
        pos = perm.index(q)        # .index 会返回第一次出现的下标
        ans.append(pos + 1)        # 题目要求位置从 1 开始计数

        # 把找到的元素搬到最前面
        perm.pop(pos)              # 把 q 从原来的位置摘下来
        perm.insert(0, q)          # 插到列表最前面

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`（最坏约 `O(m²)`）——每次查询都要遍历整个列表。  
- **空间复杂度**：`O(m)`——保存排列 `perm`（长度 `m`）和答案 `ans`（长度 `n ≤ m`）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“线性扫描寻找位置”**，这一步需要 `O(m)`，导致整体 `O(n·m)`。  
我们需要一种 **更快的“查位置”** 方法。  

观察题目：  
- 初始排列是 `[1,2,…,m]`，每次把某个元素移动到最前面。  
- 这相当于在一个 **动态序列** 中维护每个数字的 **相对顺序**，并且我们只关心 **它在序列中的第几位**（即前缀长度）。  

这正好可以用 **树状数组（Binary Indexed Tree，Fenwick Tree）** 来实现：  

1. **把每个数字映射到一个“位置编号”**。我们不直接把数字放在列表里，而是把它们放在一条“坐标轴”上。  
   - 为了方便把新搬到最前面的数字插在 **坐标轴的最左边**，我们预留出足够的空位。设 `offset = len(queries)`，则第一次查询的元素可以放在坐标 `offset`，第二次查询的元素放在 `offset-1`，依此类推。这样每次“搬到最前面”只需要把该数字的坐标改成当前最左侧的空位。  
2. **树状数组维护每个坐标上是否有数字**（1 表示有，0 表示空）。前缀和 `sum(i)` 就等于坐标 `1..i` 之间的元素个数，也就是该坐标左边有多少个数字。  
3. **查询位置**：要知道数字 `x` 当前在序列中的第几位，只需要求 **它坐标左侧已有多少元素**，即 `sum(pos[x] - 1)`，再加 1 即为答案。树状数组可以在 `O(log m)` 时间内得到前缀和。  
4. **搬到最前面**：把旧坐标的值设为 0（从树上删除），把 `offset`（当前最左空位）设为 1 并更新 `pos[x] = offset`，然后 `offset -= 1` 为下次腾出更左的空位。  

> **类比**  
> - 树状数组就像一个**电子记分牌**，每个格子记录“这位置上有没有人”。我们可以**快速累计**前面所有格子的总人数（前缀和），而不需要一个个数过去。  

**步骤概览**  
1. 初始化：`size = m + len(queries)`（保证有足够左侧空位），`BIT` 长度为 `size`，所有位置从 `len(queries)+1` 开始放置原始排列。  
2. 对每个查询 `q`：  
   - `idx = pos[q]`（当前坐标）  
   - `ans.append(bit.query(idx - 1) + 1)`（前缀和 + 1）  
   - `bit.update(idx, -1)`（把旧位置清掉）  
   - `bit.update(cur_left, 1)`（在最左空位插入）  
   - `pos[q] = cur_left`，`cur_left -= 1`  

这样每一步只用了 `O(log (m+len(queries)))`，整体 `O(n log m)`，足以轻松通过所有约束。

#### 代码（Python）  

```python
class BIT:
    """树状数组（Fenwick Tree），支持单点增减和前缀和查询"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)          # 1-indexed

    def update(self, i, delta):
        """把第 i 位的值加 delta（i 从 1 开始）"""
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i                  # lowbit，跳到下一个负责的区间

    def query(self, i):
        """返回前缀和 sum[1..i]"""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s


def processQueries(queries, m):
    n = len(queries)                      # 查询次数
    size = m + n + 2                       # 预留足够左侧空位，+2 防止越界
    bit = BIT(size)

    # pos[x] 记录数字 x 当前所在的坐标（1-indexed）
    pos = [0] * (m + 1)

    # 初始时把 1..m 放在坐标 n+1 .. n+m
    start = n + 1
    for x in range(1, m + 1):
        idx = start + x - 1
        pos[x] = idx
        bit.update(idx, 1)                 # 该坐标上有一个元素

    cur_left = n                           # 第一次搬到最前面的坐标
    ans = []

    for q in queries:
        # 1. 计算 q 在当前排列中的位置（前缀和 + 1）
        rank = bit.query(pos[q] - 1) + 1
        ans.append(rank)

        # 2. 把 q 从旧位置移除
        bit.update(pos[q], -1)

        # 3. 把 q 插入到最左侧空位
        bit.update(cur_left, 1)
        pos[q] = cur_left                  # 更新坐标映射
        cur_left -= 1                      # 为下一次腾出更左的位置

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log (m + n))`。  
  - 每一次查询我们做了两次 `update`（删除旧位、插入新位）和一次 `query`，每个操作都是 `O(log size)`。  
  - 与暴力解的 `O(n·m)` 相比，`log` 只在几十层，几乎是瞬间完成。  
- **空间复杂度**：`O(m + n)`。  
  - `BIT`、`pos`、以及答案数组共用了线性空间。  
  - 与暴力解的 `O(m)` 相当，但多了 `n` 的额外映射，仍然在可接受范围内。

---

## 心得  

- **核心技巧**：利用 **树状数组（Fenwick Tree）** 维护“当前位置上是否有元素”，从而在 **对数时间** 内完成“查询排名 + 移动到最前面”。  
- **适用场景**：  
  1. **动态序列的顺序统计**（如 LeetCode 1802 – 有序数组查询）  
  2. **频率/前缀和的在线更新**（如 303. 区域和检索 - 数组可修改）  
  3. **离线处理的逆序对计数**（如 493. 翻转对）  
- **一句话总结**：  
  > 把“在序列里找第几位”转化为“前缀和查询”，用树状数组把每次搬动的代价压到 `O(log n)`。

---

## 反思  

- **第一反应**：直接用列表模拟搬动，代码写起来很直观，但很快会发现时间会超。  
- **最容易踩的坑**：  
  - **坐标偏移**：忘记给左侧预留足够的空位，会导致插入时坐标冲突或越界。  
  - **下标从 1 开始**：树状数组实现必须使用 1‑indexed，`pos` 与 `BIT` 的下标要保持一致。  
  - **更新顺序**：先删除旧位置再插入新位置，否则会出现重复计数。  
- **下次遇到同类题**：  
  1. 先问自己“我需要快速得到某个元素在当前序列中的排名吗？”  
  2. 如果是，立刻想到 **前缀和数据结构**（BIT 或线段树）来把 **线性扫描** 替换成 **对数查询**。