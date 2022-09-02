# #1916. 统计蚂蚁巢穴中建造房间的方案数 / Count Ways to Build Rooms in an Ant Colony

> 难度：困难 · 标签：Math、Dynamic Programming、Tree、Graph、Topological Sort、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-ways-to-build-rooms-in-an-ant-colony/)

---

## 题目（英文原版）

**Description**

You are an ant tasked with adding n new rooms numbered 0 to n-1 to your colony. You are given the expansion plan as a 0-indexed integer array of length n, prevRoom, where prevRoom[i] indicates that you must build room prevRoom[i] before building room i, and these two rooms must be connected directly. Room 0 is already built, so prevRoom[0] = -1. The expansion plan is given such that once all the rooms are built, every room will be reachable from room 0.
You can only build one room at a time, and you can travel freely between rooms you have already built only if they are connected. You can choose to build any room as long as its previous room is already built.
Return the number of different orders you can build all the rooms in. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: prevRoom = [-1,0,1]
Output: 1
Explanation: There is only one way to build the additional rooms: 0 → 1 → 2
```

**Example 2:**

```
Input: prevRoom = [-1,0,0,1,2]
Output: 6
Explanation:
The 6 ways are:
0 → 1 → 3 → 2 → 4
0 → 2 → 4 → 1 → 3
0 → 1 → 2 → 3 → 4
0 → 1 → 2 → 4 → 3
0 → 2 → 1 → 3 → 4
0 → 2 → 1 → 4 → 3
```

**Constraints**

- n == prevRoom.length
- 2 <= n <= 105
- prevRoom[0] == -1
- 0 <= prevRoom[i] < n for all 1 <= i < n
- Every room is reachable from room 0 once all the rooms are built.

---

## 题目（中文翻译）

你是一只蚂蚁，需要向你的巢穴中添加 n 个新房间，编号为 0 到 n‑1。你得到了一份扩展计划，它是一个长度为 n 的 0 索引整数数组（integer array）`prevRoom`，其中 `prevRoom[i]` 表示在建造房间 i 之前必须先建造房间 `prevRoom[i]`，并且这两个房间必须直接相连。房间 0 已经建好，所以 `prevRoom[0] = -1`。该扩展计划保证当所有房间都建成后，每个房间都可以从房间 0 到达。

一次只能建造一个房间，并且只能在已经建好的且相互连通的房间之间自由移动。只要其前置房间已经建好，你就可以选择建造任意房间。

返回可以建造所有房间的不同顺序的数量。由于答案可能很大，请返回对 10^9 + 7 取模后的结果。

**示例 1**  
输入: `prevRoom = [-1,0,1]`  
输出: `1`  
解释: 只有唯一一种建造额外房间的方式：0 → 1 → 2  

**示例 2**  
输入: `prevRoom = [-1,0,0,1,2]`  
输出: `6`  
解释: 这 6 种方式为：  
- 0 → 1 → 3 → 2 → 4  
- 0 → 2 → 4 → 1 → 3  
- 0 → 1 → 2 → 3 → 4  
- 0 → 1 → 2 → 4 → 3  
- 0 → 2 → 1 → 3 → 4  
- 0 → 2 → 1 → 4 → 3  

**约束条件**  
- `n == prevRoom.length`  
- `2 <= n <= 10^5`  
- `prevRoom[0] == -1`  
- `0 <= prevRoom[i] < n`，对于所有 `1 <= i < n`  
- 当所有房间建成后，每个房间都能从房间 0 到达

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题本质上让我们在一棵 **有向树**（根为房间 0）上，按照“父节点先建，子节点后建”的规则，枚举所有可能的建造顺序。  

最直接的想法就是**把所有房间的排列全枚举一遍**，然后检查每一种排列是否满足：  
- 对于每个房间 i（i > 0），它的前置房间 `prevRoom[i]` 必须出现在它前面。  

这就像在排队买票：每个人都有一个必须站在他前面的“前辈”，只要所有前辈都排在前面，这个顺序就是合法的。  

**用到的数据结构**  
- **数组** `perm`：保存一种排列（相当于排队的顺序）。  
- **集合 / 哈希表**（Python 的 `set`）：快速判断一个房间是否已经建好。  

> 哈希表可以想象成一本**字典**，我们把已经建好的房间号当作“单词”，只要字典里出现了，就说明这间房间已经可以使用了。

**为什么暴力法是正确的**  
因为我们遍历了 **所有** 可能的排列，只要检查出满足所有前置关系的排列，就把它计数。没有漏掉任何合法情况，也没有把非法情况算进去。

#### 代码（Python）  

```python
import itertools

MOD = 10**9 + 7

def countOrders_bruteforce(prevRoom):
    n = len(prevRoom)
    rooms = list(range(1, n))                     # 0 已经建好，只需要排列其余房间
    ans = 0

    # 枚举所有可能的排列（相当于所有建造顺序）
    for perm in itertools.permutations(rooms):
        built = {0}                               # 已经建好的房间集合，先放进根节点 0
        ok = True
        for r in perm:                           # 按照当前排列依次建造
            if prevRoom[r] not in built:         # 前置房间还没建好，非法
                ok = False
                break
            built.add(r)                         # 建好后加入集合
        if ok:
            ans = (ans + 1) % MOD                 # 合法顺序计数
    return ans
```

> 关键行解释  
> - `rooms = list(range(1, n))`：因为 0 已经在最开始建好，只需要排列 1~n‑1。  
> - `built = {0}`：用集合记录已经建好的房间，查询是否已建是 **O(1)**。  
> - `if prevRoom[r] not in built`：判断当前房间的前置房间是否已经在集合里。

#### 复杂度  

- **时间复杂度**：`O(n! )`（阶乘），因为我们要遍历所有 `n‑1` 个房间的全排列。  
  - 用大白话说，就是随着房间数量的增加，可能的建造顺序会像“炸弹”一样迅速爆炸，根本不可接受。  
- **空间复杂度**：`O(n)`，主要是保存排列和集合的开销。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**。  
实际上，这棵树的结构决定了合法顺序的计数可以用 **组合数学** 与 **动态规划** 一起算出来，根本不需要枚举。

**核心观察**  

- 对于任意节点 `i`，它的子树（所有后代）之间的相对顺序是可以随意交叉的，只要每个子树内部保持自己的合法顺序即可。  
- 换句话说，若节点 `i` 有 `k` 个孩子，分别拥有子树大小 `sz1, sz2, …, szk`，并且子树 `j` 内部有 `dp[child_j]` 种合法建造方式，则把这些子树“插入”到整体序列中的方式数等于：

```
C( sz1 + sz2 + … + szk , sz1 ) *
C( sz2 + … + szk , sz2 ) * … *
C( szk , szk )
```

这其实是 **多项式系数**（multinomial coefficient），可以写成：

```
 ( total_sz )! / ( sz1! * sz2! * … * szk! )
```

其中 `total_sz = sz1 + sz2 + … + szk` 是 `i` 的所有子树节点数之和（不包括 `i` 本身）。

- 对每个子树内部的合法方式数 `dp[child]` 也要乘进去，因为子树内部的建造顺序是独立的。

于是我们可以 **自底向上**（后序遍历）计算：

```
size[i] = 1 + sum( size[child] )                # 子树节点总数（包括自己）
dp[i]    = ( total_sz )! / ( product( size[child]! ) )  * product( dp[child] )
```

最后答案就是 `dp[0]`（根节点 0 的子树就是整棵树）。

**需要的工具**  

- **阶乘** 与 **逆元**（模 1e9+7 下的除法）。  
  - 由于除法在模运算里要转成乘以 **逆元**，我们预先计算 `fac[i] = i! % MOD` 和 `invFac[i] = (i!)^{-1} % MOD`（使用费马小定理：`a^{MOD-2} % MOD`）。  
- **树的构建**：把 `prevRoom` 转成邻接表（子节点列表），方便遍历。  

**一步步推导**  

1. **预处理阶乘**  
   - 计算 `fac[0…n]`，`fac[i] = fac[i‑1] * i % MOD`。  
   - 计算 `invFac[n] = fac[n]^{MOD‑2} % MOD`，再逆推得到所有 `invFac[i‑1] = invFac[i] * i % MOD`。  

2. **建立子树列表**  
   - 对每个 `i > 0`，把 `i` 加入 `children[prevRoom[i]]`。  

3. **后序 DFS**（递归或显式栈）  
   - 对每个节点 `u`，先遍历它的所有孩子得到 `size[child]` 与 `dp[child]`。  
   - 计算 `total = sum( size[child] )`。  
   - 用公式  
     ```
     ways = fac[total]                     # total!  
     for child in children[u]:
         ways = ways * invFac[size[child]] % MOD   # 除以 child!  
         ways = ways * dp[child] % MOD            # 乘上子树内部方式数
     dp[u] = ways
     size[u] = total + 1
     ```
4. **返回 `dp[0]`**。

> **类比**：把每个子树想象成一本“独立的书”，我们要把这些书的页码混排进一本大书里，只要保持每本书内部页码顺序不变，混排的方式就是多项式系数。

#### 代码（Python）  

```python
MOD = 10**9 + 7

def countOrders(prevRoom):
    n = len(prevRoom)

    # 1️⃣ 预计算阶乘和逆元
    fac = [1] * (n + 1)          # fac[i] = i! % MOD
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    invFac = [1] * (n + 1)       # invFac[i] = (i!)^{-1} % MOD
    invFac[n] = pow(fac[n], MOD - 2, MOD)   # 费马小定理求逆元
    for i in range(n, 0, -1):
        invFac[i - 1] = invFac[i] * i % MOD

    # 2️⃣ 建立子节点列表（邻接表）
    children = [[] for _ in range(n)]
    for i in range(1, n):
        p = prevRoom[i]
        children[p].append(i)

    # 3️⃣ 后序遍历，计算 size 与 dp
    size = [0] * n      # 子树节点数（包括自己）
    dp   = [0] * n      # 子树合法建造方式数

    def dfs(u: int):
        """返回时已填好 size[u] 与 dp[u]"""
        total_sz = 0                 # 所有子树的节点数之和（不含 u）
        ways = 1

        for v in children[u]:
            dfs(v)                   # 先处理子节点
            total_sz += size[v]      # 累计子树大小
            # 乘上子树内部的建造方式数
            ways = ways * dp[v] % MOD
            # 除以子树大小的阶乘（使用逆元实现除法）
            ways = ways * invFac[size[v]] % MOD

        # 把子树之间交叉排列的方式：total_sz! / (Π size[child]!)
        ways = ways * fac[total_sz] % MOD

        dp[u] = ways
        size[u] = total_sz + 1       # 加上自己

    dfs(0)
    return dp[0] % MOD
```

> 关键行解释  
> - `fac[i] = fac[i - 1] * i % MOD`：递推计算阶乘，`% MOD` 保证数值不溢出。  
> - `invFac[n] = pow(fac[n], MOD - 2, MOD)`：利用 **费马小定理**（`a^{p‑1} ≡ 1 (mod p)`）求逆元。  
> - `ways = ways * invFac[size[v]] % MOD`：相当于 `ways / size[v]!`，因为在模运算里除法等价于乘逆元。  
> - `ways = ways * fac[total_sz] % MOD`：把所有子树的节点混排的总方式数乘进去。  

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 预处理阶乘是 `O(n)`，DFS 访问每个节点一次也是 `O(n)`。  
  - 与暴力解的 `n!` 完全不同，线性时间即使 `n = 10^5` 也能轻松跑完。  

- **空间复杂度**：`O(n)`。  
  - 存储邻接表、`size`、`dp`、阶乘数组等均为线性大小。  

---

## 心得  

- **核心技巧**：把树形依赖转化为“子树之间的多项式排列”，利用 **组合数**（阶乘 / 逆元）与 **动态规划** 递归计算子树的方式数。  
- **适用的题型**  
  1. **树的拓扑排序计数**（如 “Count Ways to Build Rooms in an Ant Colony”）。  
  2. **有序树的排列数**（如 “Number of Ways to Reorder Array to Get Same BST”。）  
  3. **带依赖的任务调度计数**（把任务依赖关系视作树/森林）。  
- **一句话总结解题钥匙**：  
  > “把每个子树看成一块完整的拼图，先算出块内部的合法排法，再用多项式系数把这些块自由交叉排列”。  

---

## 反思  

- **拿到题目第一反应**：这是一棵根在 0 的有向树，要求统计所有满足父在前的拓扑序列。立刻想到 **拓扑排序的计数**，但直接枚举太慢。  
- **最容易踩的坑**  
  - **模运算除法**：直接用 `/` 会出错，必须转成乘逆元。  
  - **阶乘预处理范围**：子树大小最大可能是 `n‑1`，所以要预计算到 `n`（包括根节点本身的 `n!`）。  
  - **递归深度**：树可能是链状，递归深度会达到 `10^5`，在 Python 中需要 `sys.setrecursionlimit` 或改写为显式栈。  
- **下次遇到同类题，第一步该想到**：  
  - 把结构抽象成 **树/森林**，先 **统计每个子树的节点数**，再用 **组合数** 计算子树之间的交叉排列方式，配合 **DP** 把子树内部的计数乘进去。