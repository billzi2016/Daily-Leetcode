# #2673. 使二叉树中路径的代价相等 / Make Costs of Paths Equal in a Binary Tree

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/make-costs-of-paths-equal-in-a-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the number of nodes in a perfect binary tree consisting of nodes numbered from 1 to n. The root of the tree is node 1 and each node i in the tree has two children where the left child is the node 2 * i and the right child is 2 * i + 1.
Each node in the tree also has a cost represented by a given 0-indexed integer array cost of size n where cost[i] is the cost of node i + 1. You are allowed to increment the cost of any node by 1 any number of times.
Return the minimum number of increments you need to make the cost of paths from the root to each leaf node equal.
Note:

**Examples**

**Example 1:**

```
Input: n = 7, cost = [1,5,2,2,3,3,1]
Output: 6
Explanation: We can do the following increments:
- Increase the cost of node 4 one time.
- Increase the cost of node 3 three times.
- Increase the cost of node 7 two times.
Each path from the root to a leaf will have a total cost of 9.
The total increments we did is 1 + 3 + 2 = 6.
It can be shown that this is the minimum answer we can achieve.
```

**Example 2:**

```
Input: n = 3, cost = [5,3,3]
Output: 0
Explanation: The two paths already have equal total costs, so no increments are needed.
```

**Constraints**

- 3 <= n <= 105
- n + 1 is a power of 2
- cost.length == n
- 1 <= cost[i] <= 104

---

## 题目（中文翻译）

给定一个整数 `n`，表示一棵 **完全二叉树**（perfect binary tree）中的节点数量，节点编号从 `1` 到 `n`。树的根节点是 `1`，每个节点 `i` 在树中都有两个子节点：左子节点为 `2 * i`，右子节点为 `2 * i + 1`。

同时给定一个长度为 `n` 的 0‑索引整数数组 `cost`，其中 `cost[i]` 表示节点 `i + 1` 的代价（cost）。你可以对任意节点的代价进行任意次数的 **递增**（increment），每次递增的幅度为 `1`。

返回使从根节点到每个 **叶子节点**（leaf node）的路径代价相等所需的最少递增次数。

## 示例

### 示例 1
**输入**: `n = 7, cost = [1,5,2,2,3,3,1]`  
**输出**: `6`  
**解释**: 我们可以进行如下递增操作:
- 将节点 `4` 的代价递增一次。
- 将节点 `3` 的代价递增三次。
- 将节点 `7` 的代价递增两次。

此时每条从根到叶子的路径的总代价均为 `9`。  
总递增次数为 `1 + 3 + 2 = 6`。可以证明这已经是最小的答案。

### 示例 2
**输入**: `n = 3, cost = [5,3,3]`  
**输出**: `0`  
**解释**: 两条路径的总代价已经相等，无需进行任何递增。

## 约束条件
- `3 <= n <= 10^5`
- `n + 1` 为 `2` 的幂（即 `n` 为完全二叉树的节点数）
- `cost.length == n`
- `1 <= cost[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每条根‑到‑叶子的路径单独算出来**，再把它们全部调成一样的值。  
具体步骤：

1. **遍历所有叶子节点**（在完全二叉树里，叶子就是编号大于 `n/2` 的节点）。  
2. 对每个叶子，**沿着父节点向上回溯**，把经过的所有节点的 `cost` 加起来，得到这条路径的总费用 `path_sum`。  
   - 这里的“父节点”可以用整数除以 2 求得：`parent = i // 2`（因为左子是 `2*i`，右子是 `2*i+1`）。  
   - 这一步可以想象成在“查字典”。我们手里有一本编号到费用的字典（`cost`），从叶子这个词往上找它的父亲词，一直找到根词，顺便把对应的费用累加。
3. 把所有路径费用放进一个列表 `sums`，取最大值 `mx`。因为只能 **增加** 费用，最省事的办法就是把所有其他路径都 **提升到 `mx`**，而 **不动** 那条已经是最大费用的路径。  
4. 最后把每条路径需要增加的量 `mx - path_sum` 累加，就是答案。

> **为什么这个方法一定对？**  
> 只能增不能减，若把一条已经是最大费用的路径再往上调，所有其它路径也必须再调一次，显然会多出不必要的增量。于是 **让最大路径保持不变，其他全部追上去** 必然是最省增量的方案。

#### 代码（Python）

```python
def minIncrementsBrute(n: int, cost: list[int]) -> int:
    # ---------- 第一步：找出所有叶子 ----------
    # 完全二叉树的叶子节点编号 >= n//2 + 1
    leaf_start = n // 2 + 1

    path_sums = []                     # 用来存每条根‑到‑叶的费用

    # ---------- 第二步：对每个叶子向上累加 ----------
    for leaf in range(leaf_start, n + 1):
        cur = leaf
        s = 0
        # 向上走到根（编号 1），一路把费用加进 s
        while cur >= 1:
            s += cost[cur - 1]         # cost 是 0‑index，节点编号是 1‑index
            cur //= 2                  # 父节点编号
        path_sums.append(s)

    # ---------- 第三步：找最大路径费用 ----------
    mx = max(path_sums)

    # ---------- 第四步：把所有路径提升到 mx ----------
    ans = sum(mx - s for s in path_sums)   # 每条路径缺少的费用相加
    return ans
```

> **关键注释**  
> - `leaf_start = n // 2 + 1`：在完全二叉树里，编号大于 `n/2` 的都是叶子。  
> - `cur //= 2`：父节点编号的“查字典”方式。  
> - `cost[cur - 1]`：因为 `cost` 列表是从 0 开始的，而题目节点是从 1 开始的，需要偏移 1。

#### 复杂度  

- **时间复杂度：** `O(L * H)`，其中 `L = n/2` 是叶子数量，`H = log2(n+1)` 是树的高度。  
  - 直观来说，就是 **每条叶子都要走一遍从叶子到根的路径**，所以大约是 `n/2 * log n`，在最坏情况下约等于 `O(n log n)`。  
  - 用大白话解释：如果树有 1 万个节点，深度约 14，平均每条路径要看 14 个节点，叶子有 5k 条，总共要看 70k 次——比线性 `O(n)` 稍微慢一点。
- **空间复杂度：** `O(L)` 用来保存所有路径和，约 `O(n)`（因为 `L ≈ n/2`）。递归栈只用了常数空间（这里用了循环）。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于**重复遍历同一条父链**：不同叶子共享很多共同的祖先节点，却每次都重新累计一次。  
我们可以 **一次遍历整棵树**，在遍历过程中把“从根到当前节点的费用累计”保存下来，这样每个节点只被访问一次。

实现方式有两种，下面采用 **深度优先搜索（DFS）**（递归写法），思路如下：

1. **从根节点 1 开始，维护一个累计费用 `cur_sum`**，它表示“从根到当前节点的费用”。  
2. 当递归到 **叶子节点** 时，把 `cur_sum` 放进列表 `leaf_sums`。此时每条根‑到‑叶路径的费用只算了一次。  
3. 整棵树遍历完后，`leaf_sums` 中已经装好了所有路径费用。取最大值 `mx`（这条路径我们不需要动），其余路径提升到 `mx` 所需的增量就是 `mx - leaf_sum` 的总和。  

> **为什么只需要一次遍历就够了？**  
> 在 DFS 过程中，每走一步就把当前节点的费用加到 `cur_sum`，相当于“把这条路上的所有费用都背在背包里”。当我们到达叶子时，背包里正好装的是这条完整路径的费用。因为每个节点只会被访问一次（左子一次、右子一次），所以整个过程是 **线性的**。

#### 代码（Python）

```python
def minIncrements(n: int, cost: list[int]) -> int:
    # ---------- 1. DFS 收集所有根‑到‑叶路径费用 ----------
    leaf_sums = []                     # 用来保存每条叶子路径的总费用

    def dfs(node: int, cur_sum: int) -> None:
        """递归遍历二叉树，node 为当前节点编号（1‑index）"""
        cur_sum += cost[node - 1]      # 把当前节点的费用加入累计和

        left = node * 2
        right = node * 2 + 1

        # 判断是否为叶子：在完全二叉树里，编号大于 n//2 的都是叶子
        if left > n:                   # 没有左孩子，说明是叶子
            leaf_sums.append(cur_sum)
            return

        # 继续向左、右子递归
        dfs(left, cur_sum)
        dfs(right, cur_sum)

    dfs(1, 0)                          # 从根节点 1 开始，累计费用初始为 0

    # ---------- 2. 计算最少增量 ----------
    mx = max(leaf_sums)                # 最大路径费用（不需要动）
    ans = sum(mx - s for s in leaf_sums)   # 其它路径提升到 mx 所需的增量
    return ans
```

> **关键注释**  
> - `if left > n:`：如果左子编号已经超过 `n`，说明当前节点已经没有子节点，即为叶子。  
> - `cur_sum += cost[node - 1]`：把当前节点费用加入累计和，**一次就完成**。  
> - `leaf_sums.append(cur_sum)`：把完整路径费用记录下来，后面只需要一次遍历找最大值。

#### 复杂度  

- **时间复杂度：** `O(n)`。每个节点恰好被访问一次，做常数级的加法和递归调用。相比暴力的 `O(n log n)`，快了一个对数因子。  
  - 大白话：如果有 100 000 个节点，只需要走 100 000 步，和读完一本 100 000 行的书差不多快。
- **空间复杂度：** `O(h + L)`  
  - `h = log2(n+1)` 是递归栈的深度（完全二叉树高度），最大约 17（因为 `n ≤ 10⁵`），可以忽略不计。  
  - `L = n/2` 是存放叶子路径费用的数组大小，约占原数据的一半。总体仍然是 `O(n)`。

---

## 心得

- **核心技巧**：**一次遍历收集所有根‑到‑叶路径和 + 只增不减的贪心**。  
- **适用的题型**  
  1. “把所有路径的某个属性统一”——如 **把所有根‑到‑叶路径的奇数个数统一**（只增不减的变形）。  
  2. “树上每条路径的最大/最小值”——如 **把所有根‑到‑叶路径的最长长度统一**（只增不减时同理）。  
  3. “树形 DP 求路径和”——如 **最大路径和**、**最小路径和** 等。  
- **一句话总结解题钥匙**：*把所有共享的工作一次做完（一次 DFS），然后把“最贵的那条路”定为目标，所有其它路向上追赶即可*。

---

## 反思

- **第一反应**：看到“只能增加”就想到“把所有路径抬到最高的那条”。于是立刻想到要先算出每条路径的总费用。  
- **最容易踩的坑**  
  1. **叶子判定错误**：完全二叉树的叶子是 `i > n//2`，而不是 `i*2 > n`（后者在递归里也可以，但要写对）。  
  2. **下标偏移**：`cost` 是 0‑index，节点编号是 1‑index，忘记 `-1` 会导致 IndexError。  
  3. **递归深度**：虽然本题深度只有 ~17，仍建议使用递归或显式栈，避免因 `sys.setrecursionlimit` 不够导致错误。  
- **下次遇到同类题**：第一步就**想“是否可以一次遍历把所有需要的中间信息收集完”**，如果可以，就把暴力的“重复遍历同一路径”转化为 **一次 DFS/ BFS + DP**。这样往往能直接把 `O(n log n)` 降到 `O(n)`。