# #1722. 交换操作后最小化汉明距离 / Minimize Hamming Distance After Swap Operations

> 难度：中等 · 标签：Array、Depth-First Search、Union Find · [LeetCode 链接](https://leetcode.com/problems/minimize-hamming-distance-after-swap-operations/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays, source and target, both of length n. You are also given an array allowedSwaps where each allowedSwaps[i] = [ai, bi] indicates that you are allowed to swap the elements at index ai and index bi (0-indexed) of array source. Note that you can swap elements at a specific pair of indices multiple times and in any order.
The Hamming distance of two arrays of the same length, source and target, is the number of positions where the elements are different. Formally, it is the number of indices i for 0 <= i <= n-1 where source[i] != target[i] (0-indexed).
Return the minimum Hamming distance of source and target after performing any amount of swap operations on array source.

**Examples**

**Example 1:**

```
Input: source = [1,2,3,4], target = [2,1,4,5], allowedSwaps = [[0,1],[2,3]]
Output: 1
Explanation: source can be transformed the following way:
- Swap indices 0 and 1: source = [2,1,3,4]
- Swap indices 2 and 3: source = [2,1,4,3]
The Hamming distance of source and target is 1 as they differ in 1 position: index 3.
```

**Example 2:**

```
Input: source = [1,2,3,4], target = [1,3,2,4], allowedSwaps = []
Output: 2
Explanation: There are no allowed swaps.
The Hamming distance of source and target is 2 as they differ in 2 positions: index 1 and index 2.
```

**Example 3:**

```
Input: source = [5,1,2,4,3], target = [1,5,4,2,3], allowedSwaps = [[0,4],[4,2],[1,3],[1,4]]
Output: 0
```

**Constraints**

- n == source.length == target.length
- 1 <= n <= 105
- 1 <= source[i], target[i] <= 105
- 0 <= allowedSwaps.length <= 105
- allowedSwaps[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi

---

## 题目（中文翻译）

给定两个整数数组 `source` 和 `target`，两者长度均为 `n`。另有数组 `allowedSwaps`，其中每个 `allowedSwaps[i] = [a_i, b_i]` 表示 **允许交换（allowed swap）** `source` 中下标 `a_i` 与下标 `b_i`（0‑基）的元素。注意，同一对下标可以交换任意次数，且顺序不限。

两个等长数组 `source` 与 `target` 的 **汉明距离（Hamming distance）** 定义为两数组在对应位置不同的元素个数。形式化地，汉明距离等于满足 `source[i] != target[i]` 的下标 `i`（`0 <= i <= n-1`）的数量。

返回对数组 `source` 进行任意次数的 **交换操作（swap operations）** 后，`source` 与 `target` 的最小可能汉明距离。

---

### 示例

**示例 1**  
```
Input: source = [1,2,3,4], target = [2,1,4,5], allowedSwaps = [[0,1],[2,3]]
Output: 1
Explanation: 可以按如下方式变换 source：
- 交换下标 0 与 1：source = [2,1,3,4]
- 交换下标 2 与 3：source = [2,1,4,3]
此时 source 与 target 的汉明距离为 1，仅在下标 3 处不同。
```

**示例 2**  
```
Input: source = [1,2,3,4], target = [1,3,2,4], allowedSwaps = []
Output: 2
Explanation: 没有任何允许的交换。
source 与 target 的汉明距离为 2，分别在下标 1 与下标 2 处不同。
```

**示例 3**  
```
Input: source = [5,1,2,4,3], target = [1,5,4,2,3], allowedSwaps = [[0,4],[4,2],[1,3],[1,4]]
Output: 0
```

---

### 约束

- `n == source.length == target.length`
- `1 <= n <= 10^5`
- `1 <= source[i], target[i] <= 10^5`
- `0 <= allowedSwaps.length <= 10^5`
- `allowedSwaps[i].length == 2`
- `0 <= a_i, b_i <= n - 1`
- `a_i != b_i`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**如果根本不做任何交换**，直接比较 `source` 与 `target` 在每个下标上的值是否相同，统计不同的下标个数，这就是 Hamming 距离。  

- **用到的数据结构**：只需要遍历两个列表，用普通的计数器就行。可以把计数器想象成“统计表”，每看到一个不相等的下标，就往表里加一。  
- **为什么正确**：因为在没有任何交换的前提下，数组的顺序是固定的，唯一能判断两数组是否相等的方式就是逐位比较。  
- **时间/空间复杂度**：我们只遍历一次长度为 `n` 的数组，时间是 **O(n)**，这里的 `O(n)` 就是“随着元素个数线性增长”。额外使用的空间只有常数个变量，记作 **O(1)**（常数空间），也就是不随 `n` 增大而增长的空间。

> 这一步虽然不能得到题目要求的最小距离，但它帮助我们明确：**只有在允许交换的下标之间才能改变 Hamming 距离**，这为后面的优化奠定思路。

#### 代码（Python）  

```python
def min_hamming_bruteforce(source, target):
    """
    暴力思路：不做任何交换，直接统计两数组不同的位置个数
    """
    n = len(source)
    diff = 0                       # 记录不同下标的数量
    for i in range(n):
        if source[i] != target[i]: # 只要对应位置的数不相等，就+1
            diff += 1
    return diff
```

#### 复杂度  

- **时间复杂度**：O(n) —— 需要遍历 `source`（或 `target`）一次，`n` 越大，花的时间就线性增长。  
- **空间复杂度**：O(1) —— 只用了几个整数变量，不会随 `n` 增大而占用更多内存。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **没有利用题目给出的 “allowedSwaps”**。  
如果两个下标在同一个 *连通分量*（component）里，意味着我们可以在这些下标之间任意交换元素，等价于这些位置的元素可以被 **自由排列**。于是，**只要在同一连通分量内部的 multiset（元素出现次数的集合）相同，就可以把它们全部配对成功**，不产生 Hamming 距离。  

下面一步步把思路展开：  

1. **把下标看成图的节点**，每个 `allowedSwaps[i] = [a, b]` 是一条无向边。  
2. 使用 **并查集（Union‑Find）** 把所有相连的节点合并成一个集合，得到若干连通分量。并查集可以在几乎常数时间（α(n)，反阿克曼函数）完成合并和查询。  
3. 对每个连通分量，统计它内部 `source` 中每个数出现的次数（用哈希表 `cnt`），再遍历同一分量的 `target`，如果 `target` 的某个数在 `cnt` 中出现过，就把对应的计数减 1（相当于配对成功），否则这一次配对失败，必须计入 Hamming 距离。  
4. 所有分量的配对失败次数累加，就是 **最小可能的 Hamming 距离**。  

> **类比**：把每个连通分量想象成一个装有若干球的口袋，`source` 的球放进去后可以随意摇晃（交换位置），我们再把 `target` 的球逐个放进口袋，能对应上口袋里已有的球就算配对成功，剩下的就是无法匹配的球，正好对应 Hamming 距离。  

#### 代码（Python）  

```python
class UnionFind:
    """并查集实现，支持路径压缩和按秩合并"""
    def __init__(self, n):
        self.parent = list(range(n))   # 初始时每个节点是自己的根
        self.rank = [0] * n            # 用来控制合并时的高度

    def find(self, x):
        """寻找根节点，顺带路径压缩，使后续查询更快"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 递归压缩路径
        return self.parent[x]

    def union(self, x, y):
        """把 x, y 所在的集合合并"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:                     # 已经在同一个集合，无需合并
            return
        # 按秩合并：高度小的挂在高度大的下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1


def minHammingDistance(source, target, allowedSwaps):
    """
    最优解：利用并查集找连通分量，然后在每个分量内部统计元素出现次数，
    计算无法匹配的数量即为最小 Hamming 距离。
    """
    n = len(source)
    uf = UnionFind(n)

    # 1️⃣ 合并所有允许交换的下标
    for a, b in allowedSwaps:
        uf.union(a, b)

    # 2️⃣ 根据根节点把下标分组，得到每个连通分量的下标列表
    from collections import defaultdict
    groups = defaultdict(list)   # key: root, value: 该连通分量内的所有下标
    for i in range(n):
        root = uf.find(i)
        groups[root].append(i)

    # 3️⃣ 对每个分量统计 source 中的元素出现次数
    answer = 0  # 最终的最小 Hamming 距离
    for idx_list in groups.values():
        cnt = defaultdict(int)   # 统计 source 中的数出现次数
        for i in idx_list:
            cnt[source[i]] += 1   # 把 source 的元素放进口袋

        # 4️⃣ 再遍历同一分量的 target，尝试配对
        for i in idx_list:
            val = target[i]
            if cnt[val] > 0:      # 口袋里还有相同的球，配对成功
                cnt[val] -= 1
            else:                 # 配对失败，这个位置必然贡献 1 到 Hamming 距离
                answer += 1

    return answer
```

#### 复杂度  

- **时间复杂度**：  
  - 并查集的 `union`/`find` 操作近似 **O(α(n))**，对 `m = len(allowedSwaps)` 条边共计 **O(m α(n))**。  
  - 再遍历一次数组把下标分组、统计、配对，总共 **O(n)**。  
  - 综合起来是 **O(n + m α(n))**，其中 α(n) 极其缓慢（几乎可以当作常数），所以实际运行时几乎是线性时间。  
- **空间复杂度**：  
  - 并查集需要 `parent`、`rank` 两个长度为 `n` 的数组 → **O(n)**。  
  - 额外的哈希表 `groups`、`cnt` 也最多存储 `n` 个下标或元素计数 → **O(n)**。  
  - 整体 **O(n)**，即随输入规模线性增长的内存。  

与暴力解相比，最优解把 **只看位置** 的 O(n) 计算提升为 **利用可交换关系** 的 O(n + m) 计算，显著降低了在大规模 `allowedSwaps` 场景下的时间成本。  

---  

## 心得  

- **核心技巧**：把“可以交换的下标”抽象成图的连通分量，利用 **并查集** 快速划分组件，然后在每个组件内部用 **哈希计数**（多重集合）匹配 `source` 与 `target`。  
- **适用的题型**：  
  1. **“可以在同一连通分量内部自由排列”** 的数组/字符串题，如 “Reachable Nodes With Subdivided Edges”。  
  2. **基于等价关系** 的分组统计问题，如 “Largest Component Size by Common Factor”。  
  3. **需要最小化不匹配** 的配对类问题，例如 “Minimum Swaps To Make Sequences Increasing”。  
- **一句话总结解题钥匙**：**“同一连通分量内元素可以任意调换，统计每个分量内部的多重集合差异即可得到最小 Hamming 距离”。**  

---  

## 反思  

- **第一反应**：看到 `allowedSwaps`，立刻把下标想成图的节点，想到“连通分量”可以自由交换。  
- **最容易踩的坑**：  
  1. **忘记在同一分量内部统计 `source` 的次数**，直接把 `target` 的每个元素和 `source` 同位置比较，导致错误。  
  2. **计数时使用普通字典忘记初始化为 0**，导致 `KeyError`。  
  3. **忽视空的 `allowedSwaps`**（此时答案就是普通 Hamming 距离），代码要在没有任何合并的情况下仍能正常工作。  
- **下次遇到同类题的第一步**：先把“可操作的关系”抽象成 **图/并查集**，快速得到连通分量，再在每个分量内部做**计数配对**。这样可以把复杂的全局排列问题拆解成若干局部的“多重集合匹配”。