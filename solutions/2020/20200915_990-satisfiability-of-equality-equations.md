# #990. 等式可满足性 / Satisfiability of Equality Equations

> 难度：中等 · 标签：Array、String、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/satisfiability-of-equality-equations/)

---

## 题目（英文原版）

**Description**

You are given an array of strings equations that represent relationships between variables where each string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi".Here, xi and yi are lowercase letters (not necessarily different) that represent one-letter variable names.
Return true if it is possible to assign integers to variable names so as to satisfy all the given equations, or false otherwise.

**Examples**

**Example 1:**

```
Input: equations = ["a==b","b!=a"]
Output: false
Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
There is no way to assign the variables to satisfy both equations.
```

**Example 2:**

```
Input: equations = ["b==a","a==b"]
Output: true
Explanation: We could assign a = 1 and b = 1 to satisfy both equations.
```

**Constraints**

- 1 <= equations.length <= 500
- equations[i].length == 4
- equations[i][0] is a lowercase letter.
- equations[i][1] is either '=' or '!'.
- equations[i][2] is '='.
- equations[i][3] is a lowercase letter.

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`equations`，其中每个字符串 `equations[i]` 的长度为 4，且仅有两种形式之一：`"xi==yi"` 或 `"xi!=yi"`。这里，`xi` 和 `yi` 是小写字母（不一定不同），表示单字符变量名。

如果可以为这些变量分配整数，使得所有给出的等式（equations）都得到满足，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入**: `equations = ["a==b","b!=a"]`  
**输出**: `false`  
**解释**: 若将 `a = 1`、`b = 1`，则第一条等式成立，但第二条不成立。没有任何方式能够同时满足这两条等式。

### 示例 2
**输入**: `equations = ["b==a","a==b"]`  
**输出**: `true`  
**解释**: 可以将 `a = 1`、`b = 1`，从而使两条等式都成立。

## 约束条件
- `1 <= equations.length <= 500`
- `equations[i].length == 4`
- `equations[i][0]` 为小写字母
- `equations[i][1]` 为 `'='` 或 `'!'`
- `equations[i][2]` 为 `'='`
- `equations[i][3]` 为小写字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有等式先算出来，再去验证所有不等式**。  
我们可以把 26 个小写字母想象成 26 本小册子，  
每本册子上记录它“等于”哪些其他册子。如果 `a==b`，就在 `a` 与 `b` 之间画一条双向的线，表示它们在同一本“等价册子”里。

把所有 `==` 的线画完后，还要把**传递关系**也算进去：  
如果 `a==b` 且 `b==c`，那么 `a` 必然也等于 `c`。  
这一步可以用**弗洛伊德‑沃沙尔（Floyd‑Warshall）**算法来完成——它会遍历所有三元组 `(i, j, k)`，把 “如果 i 能到 k，k 能到 j，那么 i 也能到 j” 的规则全部执行。

得到完整的等价关系后，只需要检查每条 `!=`：  
- 若 `x != y` 的两字母已经在同一个等价集合里（即我们之前算出的 “相等” 为 True），说明冲突，返回 `False`。  
- 否则所有不等式都满足，返回 `True`。

> **类比**：把每个字母想成城市，`==` 是两座城市之间的高速公路，`!=` 是“这两座城市绝不能在同一个州”。先把高速路网连通起来（包括间接连通），再看“不在同州”的要求是否被高速路网违背。

#### 代码（Python）

```python
def equationsPossible_bruteforce(equations):
    # 26 个字母对应 0~25 的下标
    N = 26
    # eq[i][j] 为 True 表示字母 i 与 j 已知相等
    eq = [[False] * N for _ in range(N)]

    # 每个字母显然与自己相等
    for i in range(N):
        eq[i][i] = True

    # 先处理所有 “==” 的等式
    for exp in equations:
        if exp[1] == '=':               # "a==b"
            x = ord(exp[0]) - ord('a')
            y = ord(exp[3]) - ord('a')
            eq[x][y] = eq[y][x] = True   # 双向标记相等

    # 传递闭包：如果 x==k 且 k==y，则 x==y
    # 这里的三层循环正是 Floyd‑Warshall
    for k in range(N):
        for i in range(N):
            if eq[i][k]:                # 只在 i 能到 k 时才继续
                for j in range(N):
                    if eq[k][j]:
                        eq[i][j] = True

    # 检查所有 “!=” 的不等式
    for exp in equations:
        if exp[1] == '!':               # "a!=b"
            x = ord(exp[0]) - ord('a')
            y = ord(exp[3]) - ord('a')
            if eq[x][y]:                # 已经相等，冲突
                return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(26³)`，即 `O(1)`（因为字母个数固定为 26）。  
  用大白话说，就是我们用了三层循环，每层最多跑 26 次，最多跑 26×26×26 ≈ 1.7 万次，计算机跑得飞快。  
- **空间复杂度**：`O(26²)`，即 `O(1)`。需要一个 26×26 的布尔矩阵来存相等关系，大小固定。

---

### 2. 最优解

#### 思路  

暴力解的“慢点”在于 **三层循环的传递闭包**，虽然对 26 个字母来说仍然可接受，但如果把字母换成更大的集合，这种 `O(n³)` 的做法就会超时。  
我们可以把 “把相等的变量合并到同一个集合” 这件事交给 **并查集（Union‑Find）** 来完成。

并查集是一种**快速合并与查询所在集合**的数据结构，核心思想是：

1. **每个元素都有一个 “父节点”**（`parent[x]`），最初自己指向自己。  
2. **`find(x)`**：沿着父节点一路向上，找到最终的根节点（集合的代表），并在路径上做压缩，让以后查找更快。  
3. **`union(x, y)`**：把 `x` 和 `y` 所在的两个集合合并，让其中一个根指向另一个根（可用秩/大小平衡，防止树太高）。

对本题的应用步骤：

1. **第一遍遍历**所有 `==` 公式，使用 `union` 把等式两边的变量合并到同一集合。  
2. **第二遍遍历**所有 `!=` 公式，检查两边的变量是否已经在同一集合（即 `find(x) == find(y)`）。如果是，则说明冲突，返回 `False`。  
3. 若所有不等式都不冲突，返回 `True`。

> **类比**：把每个字母看成学生，`==` 表示“他们是同一个社团的”。并查集就是学校的“社团登记系统”，能快速把两个学生拉进同一个社团，也能立刻告诉你两个学生是否已经在同一个社团里。

#### 代码（Python）

```python
def equationsPossible_unionfind(equations):
    # 26 个字母 → 0~25
    parent = list(range(26))      # 父节点数组，初始每个字母自己是根
    rank   = [0] * 26             # 秩（近似树的高度），用于平衡

    # 查找根节点并路径压缩
    def find(x):
        if parent[x] != x:        # 不是根，就递归找根
            parent[x] = find(parent[x])   # 递归返回时把路径上的节点直接挂到根上
        return parent[x]

    # 合并两个集合
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:              # 已经在同一个集合，啥也不干
            return
        # 按秩合并：低秩挂到高秩下，保持树矮一点
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:                     # 秩相同，随便挂一边，同时把秩加 1
            parent[ry] = rx
            rank[rx] += 1

    # 第一次遍历：处理所有 “==”
    for exp in equations:
        if exp[1] == '=':                 # "a==b"
            x = ord(exp[0]) - ord('a')
            y = ord(exp[3]) - ord('a')
            union(x, y)

    # 第二次遍历：处理所有 “!=”
    for exp in equations:
        if exp[1] == '!':                 # "a!=b"
            x = ord(exp[0]) - ord('a')
            y = ord(exp[3]) - ord('a')
            if find(x) == find(y):       # 同一个集合，冲突
                return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(N·α(26)) ≈ O(N)`，其中 `N` 为公式的数量，`α` 为阿克曼函数的反函数，增长极其缓慢，几乎可以当作常数。  
  用通俗的话说：我们只遍历两遍公式，且每次查找或合并几乎都是“一步到位”，所以整体是线性时间。  
- **空间复杂度**：`O(26)`，只需要保存 26 个父节点和秩数组，常数级别的额外空间。

---

## 心得

- **核心技巧**：并查集（Union‑Find）用于处理“等价关系”或“连通性”问题。  
- **适用题型**（类似思路）  
  1. **Friend Circles / Number of Provinces**（计算连通分量）  
  2. **Graph Valid Tree**（判断是否为树）  
  3. **Redundant Connection**（找出多余的边）  
- **一句话总结**：先把所有“相等”合并成集合，再用同一个集合的查询来验证“不等式”，这就是解这类等价约束的钥匙。

---

## 反思

- **第一反应**：看到等式和不等式，我立刻想到要把相等的变量放在一起，检查冲突。  
- **最容易踩的坑**  
  - 忘记先处理所有 `==` 再检查 `!=`，顺序搞错会导致误判。  
  - 把 `!=` 当成普通的“不相连”去 union，实际上不应该合并。  
  - 边界情况：变量可以是同一个字母（如 `a!=a`），必须直接返回 `False`。  
- **下次类似题目**：第一步先思考“这是一种等价关系吗？能否用并查集把相等的元素归类？”——如果答案是肯定的，马上进入并查集的解法。