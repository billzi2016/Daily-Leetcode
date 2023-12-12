# #2509. **树上的环长度查询** / Cycle Length Queries in a Tree

> 难度：困难 · 标签：Array、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/cycle-length-queries-in-a-tree/)

---

## 题目（英文原版）

**Description**

You are given an integer n. There is a complete binary tree with 2n - 1 nodes. The root of that tree is the node with the value 1, and every node with a value val in the range [1, 2n - 1 - 1] has two children where:
You are also given a 2D integer array queries of length m, where queries[i] = [ai, bi]. For each query, solve the following problem:
Note that:
Return an array answer of length m where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: n = 3, queries = [[5,3],[4,7],[2,3]]
Output: [4,5,3]
Explanation: The diagrams above show the tree of 23 - 1 nodes. Nodes colored in red describe the nodes in the cycle after adding the edge.
- After adding the edge between nodes 3 and 5, the graph contains a cycle of nodes [5,2,1,3]. Thus answer to the first query is 4. We delete the added edge and process the next query.
- After adding the edge between nodes 4 and 7, the graph contains a cycle of nodes [4,2,1,3,7]. Thus answer to the second query is 5. We delete the added edge and process the next query.
- After adding the edge between nodes 2 and 3, the graph contains a cycle of nodes [2,1,3]. Thus answer to the third query is 3. We delete the added edge.
```

**Example 2:**

```
Input: n = 2, queries = [[1,2]]
Output: [2]
Explanation: The diagram above shows the tree of 22 - 1 nodes. Nodes colored in red describe the nodes in the cycle after adding the edge.
- After adding the edge between nodes 1 and 2, the graph contains a cycle of nodes [2,1]. Thus answer for the first query is 2. We delete the added edge.
```

**Constraints**

- 2 <= n <= 30
- m == queries.length
- 1 <= m <= 105
- queries[i].length == 2
- 1 <= ai, bi <= 2n - 1
- ai != bi

---

## 题目（中文翻译）

你被给定一个整数 `n`。  
存在一棵包含 `2^n - 1` 个节点的**完全二叉树**（complete binary tree），根节点的编号为 `1`。对于所有编号在 `[1, 2^n - 2]` 区间内的节点 `val`，它有两棵子树：

- 左子节点编号为 `2 * val`  
- 右子节点编号为 `2 * val + 1`

同时，你还得到一个长度为 `m` 的二维整数数组 `queries`，其中 `queries[i] = [a_i, b_i]`。对每个查询，需要解决如下问题：

- 在原始树上**额外添加一条无向边** `(a_i, b_i)`（`a_i ≠ b_i`），此时图中恰好会出现唯一的一条**环**（cycle）。  
- 求该环包含的节点个数（即环的长度）。

**注意**：

- 对每个查询，都应在 **添加边后** 计算环的长度，然后 **删除这条新增的边**，再处理下一个查询，互不影响。

返回一个长度为 `m` 的数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的答案。

---

### 示例

**示例 1**

> 输入: `n = 3, queries = [[5,3],[4,7],[2,3]]`  
> 输出: `[4,5,3]`  
> 解释: 下图展示了 `2^3 - 1 = 7` 个节点的完全二叉树。红色节点表示在添加对应边后形成的环中的节点。  
> - 在节点 `3` 与 `5` 之间添加一条边后，图中出现环 `[5,2,1,3]`，长度为 `4`。随后删除这条边，继续处理下一个查询。  
> - 在节点 `4` 与 `7` 之间添加边后，环为 `[7,3,1,2,4]`，长度为 `5`。  
> - 在节点 `2` 与 `3` 之间添加边后，环为 `[3,1,2]`，长度为 `3`。

**示例 2**

> 输入: `n = 2, queries = [[1,2]]`  
> 输出: `[2]`  
> 解释: 下图展示了 `2^2 - 1 = 3` 个节点的完全二叉树。红色节点表示环中的节点。  
> - 在节点 `1` 与 `2` 之间添加一条边后，环为 `[2,1]`，长度为 `2`。

---

### 约束条件

- `2 ≤ n ≤ 30`
- `m = queries.length`
- `1 ≤ m ≤ 10^5`
- `queries[i].length = 2`
- `1 ≤ a_i, b_i ≤ 2^n - 1`
- `a_i ≠ b_i`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
树是一棵 **完全二叉树**，节点的编号恰好和 **堆**（heap）里的下标一样：

```
父节点   = 当前节点 // 2
左孩子   = 当前节点 * 2
右孩子   = 当前节点 * 2 + 1
```

题目让我们 **在树上再加一条边 (a, b)**，这条新边把原本唯一的 `a‑b` 路径闭合，形成一个环。  
环里包含的节点正好是 **从 a 到 b 的路径上的所有节点**，所以环的长度 =  
`路径上边的条数 + 1`（因为路径本身已经把所有节点串起来，新增的那条边只让它闭合）。

**暴力做法**：

1. 从 `a` 往上一直走到根（记录所有经过的节点）。  
2. 同样从 `b` 往上走到根。  
3. 把第一条路径的节点放进集合 `S`，再遍历第二条路径，找到第一个同时在 `S` 中的节点——这就是 **最近公共祖先 (LCA)**。  
4. 设 `depth(x)` 为节点 `x` 到根的边数（即深度），则  
   `distance(a, b) = depth(a) + depth(b) - 2 * depth(LCA)`  
   环的节点数 = `distance(a, b) + 1`。

> **类比**：  
> 想象每个节点是一张纸条，纸条上写着它的编号。把 `a` 的纸条一路往上贴，形成一串；同理把 `b` 的纸条贴成另一串。两串第一次相遇的纸条，就是它们最近的共同祖先。

#### 代码（Python）

```python
def brute_cycle_len(a: int, b: int) -> int:
    # ---------- 第一步：收集 a 到根的所有祖先 ----------
    ancestors_a = set()
    cur = a
    depth_a = 0          # 记录 a 的深度
    while cur:
        ancestors_a.add(cur)
        cur //= 2        # 往父节点走
        depth_a += 1

    # ---------- 第二步：从 b 往上找最近的公共祖先 ----------
    cur = b
    depth_b = 0
    lca = 1               # 必然有根 1 是公共祖先
    while cur:
        if cur in ancestors_a:   # 第一次碰到就一定是最近公共祖先
            lca = cur
            break
        cur //= 2
        depth_b += 1

    # ---------- 第三步：算距离 + 环长度 ----------
    # depth 包含了根本身，多算了一层，需要减 1
    depth_a -= 1
    depth_b -= 1
    # LCA 的深度同样可以通过不断除以 2 求得
    depth_lca = 0
    cur = lca
    while cur:
        cur //= 2
        depth_lca += 1
    depth_lca -= 1

    distance = depth_a + depth_b - 2 * depth_lca
    return distance + 1          # 环的节点数
```

#### 复杂度  

- **时间复杂度**：`O(log N)`，这里 `N = 2^n - 1`，树的高度最多 `n ≤ 30`，所以每次循环最多走 30 步。  
  大白话：我们只需要爬到根节点，树有多高我们就走多少步，最多 30 步，几乎可以忽略不计。  
- **空间复杂度**：`O(log N)`，因为要把 `a` 的所有祖先放进集合，最多也只有树的高度这么多。

---

### 2. 最优解  

#### 思路  

暴力解已经是 `O(log N)`，已经很快了。但我们可以 **去掉集合**，只用常数级的额外空间，把 “找最近公共祖先” 的过程写得更简洁、更高效。

**关键观察**：

- 两个节点的深度可以直接用 **位数**（二进制长度）得到。  
  `depth(x) = x.bit_length() - 1`（根 1 的深度是 0）。  
- 只要把较深的那个节点 **抬高**（不断除以 2）到和另一节点同深度，然后两边同步上移，第一次相等的节点就是 LCA。  

这样只需要 **两次循环**，每次最多 `log N` 步，空间只用 `O(1)`。

**步骤**：

1. 计算 `depth_a`、`depth_b`（使用 `bit_length`）。  
2. 若 `depth_a > depth_b`，把 `a` 往上移动 `depth_a - depth_b` 步，使两者同层；反之亦然。  
3. 同时把 `a`、`b` 向上（`//=2`）移动，直到相等，得到 LCA。  
4. 用公式 `distance = depth_a + depth_b - 2 * depth_lca`，环长 = `distance + 1`。

> **类比**：  
> 把两个人站在不同楼层的电梯口，先让高层的那个人先下几层，使两人站在同一层，然后一起坐电梯向上，第一次相遇的楼层就是他们的公共楼层。

#### 代码（Python）

```python
def fast_cycle_len(a: int, b: int) -> int:
    # ---------- 1. 计算两节点深度 ----------
    depth_a = a.bit_length() - 1      # 例如 5(101) 的深度是 2
    depth_b = b.bit_length() - 1

    # ---------- 2. 把深的节点抬高 ----------
    while depth_a > depth_b:
        a //= 2
        depth_a -= 1
    while depth_b > depth_a:
        b //= 2
        depth_b -= 1

    # ---------- 3. 同时上移，找到 LCA ----------
    while a != b:
        a //= 2
        b //= 2
        depth_a -= 1        # 同时降低深度计数
        depth_b -= 1

    lca_depth = depth_a      # 此时 a == b == LCA

    # ---------- 4. 计算距离与环长 ----------
    # 原始深度保存在变量里，下面重新算一次原始深度
    orig_depth_a = a.bit_length() - 1  # 这里 a 已经是 LCA，需用原始值
    # 为避免混淆，直接在函数入口时把原始深度记下来
    # （下面用传入时的 depth_a_original、depth_b_original）
    # 为了代码简洁，这里重新算一次：
    # (实际实现时建议在开头就保存原始深度)
    # -----------------
    # 下面的实现直接使用已保存的原始深度
    # -----------------
    # 这里假设我们在函数开头已经保存了 depth_a_orig, depth_b_orig
    # 为演示，直接把公式写成：
    distance = depth_a_original + depth_b_original - 2 * lca_depth
    return distance + 1
```

> **完整可运行版本（包含输入/输出）**：

```python
import sys
from typing import List

def cycle_length(a: int, b: int) -> int:
    # 保存原始深度，后面会用到
    depth_a_orig = a.bit_length() - 1
    depth_b_orig = b.bit_length() - 1

    # 把两者抬高到同一层
    da, db = depth_a_orig, depth_b_orig
    while da > db:
        a //= 2
        da -= 1
    while db > da:
        b //= 2
        db -= 1

    # 同时上移找到 LCA
    while a != b:
        a //= 2
        b //= 2
        da -= 1          # 此时 da == db == LCA 的深度

    lca_depth = da
    distance = depth_a_orig + depth_b_orig - 2 * lca_depth
    return distance + 1          # 环的节点数

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))                     # 只用来确认节点上限，实际不需要
    m = int(next(it))                     # queries 长度
    ans: List[int] = []
    for _ in range(m):
        a = int(next(it))
        b = int(next(it))
        ans.append(cycle_length(a, b))
    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

#### 复杂度  

- **时间复杂度**：`O(log N)`（每个查询最多走树高 `n ≤ 30` 步），与暴力解相同的数量级，但省掉了集合的哈希开销，常数更小。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，不会随查询数量增长。

---

## 心得  

- **核心技巧**：在二叉堆结构的完全二叉树里，**父子关系只用整数除以 2**，深度可以用二进制位数直接得到。利用这两个性质即可在 `O(log N)` 时间内求出任意两点的最近公共祖先（LCA），进而求距离。  
- **适用的题型**：  
  1. “树上两点距离” 类题目（如 LeetCode 2583、2360）。  
  2. “在完全二叉树中找最近公共祖先” 的变体。  
  3. “把树变成图后求环长” 这类只多加一条边的题目。  
- **一句话总结解题钥匙**：**利用整数的二进制特性快速对齐深度，再同步上移即可在常数空间内得到 LCA**。

---

## 反思  

- **第一反应**：看到“在树上再加一条边会形成环”，立刻想到环的节点数等于原路径的节点数，于是把问题转化为“求两节点距离”。  
- **最容易踩的坑**：  
  - 忘记 **+1**（新加的那条边并不增加新节点，只把路径闭合）。  
  - 深度计算错误：`bit_length()` 返回的是二进制位数，根节点 1 的深度应该是 `0`，所以要减 `1`。  
  - 输入格式中没有直接给出 `m`，需要自行读取查询的数量。  
- **下次遇到同类题**，第一步应该想到 **“把树看成堆编号，用除以 2 上移，用位数求深度”**，这样可以迅速得到 LCA 与距离，避免繁琐的显式路径存储。