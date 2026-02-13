# #3525. 数组的 X 值 II / Find X Value of Array II

> 难度：困难 · 标签：Array、Math、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/find-x-value-of-array-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums and a positive integer k. You are also given a 2D array queries, where queries[i] = [indexi, valuei, starti, xi].
You are allowed to perform an operation once on nums, where you can remove any suffix from nums such that nums remains non-empty.
The x-value of nums for a given x is defined as the number of ways to perform this operation so that the product of the remaining elements leaves a remainder of x modulo k.
For each query in queries you need to determine the x-value of nums for xi after performing the following actions:
Return an array result of size queries.length where result[i] is the answer for the ith query.
A prefix of an array is a subarray that starts from the beginning of the array and extends to any point within it.
A suffix of an array is a subarray that starts at any point within the array and extends to the end of the array.
Note that the prefix and suffix to be chosen for the operation can be empty.
Note that x-value has a different definition in this version.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], k = 3, queries = [[2,2,0,2],[3,3,3,0],[0,1,0,1]]
Output: [2,2,2]
Explanation:
```

**Example 2:**

```
Input: nums = [1,2,4,8,16,32], k = 4, queries = [[0,2,0,2],[0,2,0,1]]
Output: [1,0]
Explanation:
```

**Example 3:**

```
Input: nums = [1,1,2,1,1], k = 2, queries = [[2,1,0,1]]
Output: [5]
```

**Constraints**

- 1 <= nums[i] <= 109
- 1 <= nums.length <= 105
- 1 <= k <= 5
- 1 <= queries.length <= 2 * 104
- queries[i] == [indexi, valuei, starti, xi]
- 0 <= indexi <= nums.length - 1
- 1 <= valuei <= 109
- 0 <= starti <= nums.length - 1
- 0 <= xi <= k - 1

---

## 题目（中文翻译）

你得到一个由正整数构成的数组 `nums` 和一个正整数 `k`。同时还有一个二维数组 `queries`，其中 `queries[i] = [index_i, value_i, start_i, x_i]`。  

你可以对 `nums` **仅执行一次** 操作：删除 `nums` 的任意后缀（suffix），要求删除后 `nums` 仍保持非空。  

**x‑value**（x 值）对给定的 `x` 定义为：在满足上述操作的前提下，使剩余元素的乘积 **模** `k` 的余数等于 `x` 的不同操作方式的数量。  

对于 `queries` 中的每个查询，需要在执行以下动作后求出对应的 `x_i` 的 **x‑value**：  

* 返回一个长度为 `queries.length` 的数组 `result`，其中 `result[i]` 为第 `i` 个查询的答案。  

数组的 **前缀**（prefix）是指从数组起始位置开始，延伸到任意位置的子数组（subarray）。  
数组的 **后缀**（suffix）是指从数组任意位置开始，延伸到数组末尾的子数组。  

> 注意，选择的前缀和后缀都可以为空。  
> 本题中的 **x‑value** 与其他版本的定义不同。

---

### 示例

**Example 1:**  
``` 
Input: nums = [1,2,3,4,5], k = 3, queries = [[2,2,0,2],[3,3,3,0],[0,1,0,1]]
Output: [2,2,2]
Explanation:
```

**Example 2:**  
``` 
Input: nums = [1,2,4,8,16,32], k = 4, queries = [[0,2,0,2],[0,2,0,1]]
Output: [1,0]
Explanation:
```

**Example 3:**  
``` 
Input: nums = [1,1,2,1,1], k = 2, queries = [[2,1,0,1]]
Output: [5]
Explanation:
```

---

### 约束条件

- `1 <= nums[i] <= 10^9`
- `1 <= nums.length <= 10^5`
- `1 <= k <= 5`
- `1 <= queries.length <= 2 * 10^4`
- `queries[i] == [index_i, value_i, start_i, x_i]`
- `0 <= index_i <= nums.length - 1`
- `1 <= value_i <= 10^9`
- `0 <= start_i <= nums.length - 1`
- `0 <= x_i <= k - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要我们 **在每次查询后**，先把 `nums[index]` 改成 `value`，随后在子数组 `nums[start … n-1]` 中统计：

> 有多少个前缀（即从 `start` 开始一直取到某个位置）使得这些元素的乘积对 `k` 取模等于 `xi`。

最直接的想法就是 **遍历所有前缀**，把乘积一步步算出来，看到余数就记个数。

- **用到的数据结构**：只需要一个普通的 Python 列表来存 `nums`，以及几个整型变量保存“当前乘积”。  
  把 `nums` 看成一本账本，**前缀乘积** 就像每天把账本里前面的数相乘，得到当天的累计余额。我们只要把每一天的余额对 `k` 求余，然后统计出现多少次 `xi` 即可。

- **为什么正确**：因为题目本身就是在问“有多少个前缀的乘积满足条件”，我们把每个前缀的乘积都算一遍，肯定不会漏掉任何一种可能。

- **时间/空间复杂度**  
  - 对每一次查询，我们需要 **从 `start` 到数组末尾** 逐个遍历，计算前缀乘积。最坏情况下遍历整个数组，记作 `n`。  
    因此 **时间复杂度** 为 **`O(n)`**。  
    用“大白话”说：如果数组有 10 万个元素，单次查询就要算 10 万次乘法，查询 2 万次的话，算下来就是 2 × 10⁴ × 10⁵ ≈ 2 × 10⁹ 次乘法，显然会超时。
  - 只用了常数个额外变量（乘积、计数器），**空间复杂度** 为 **`O(1)`**（不计输入数组本身）。

#### 代码（Python）

```python
def brute_force(nums, k, queries):
    """暴力解：每次查询 O(n)"""
    res = []
    for index, value, start, xi in queries:
        # 1️⃣ 更新数组
        nums[index] = value

        # 2️⃣ 统计满足条件的前缀个数
        cnt = 0
        prod = 1          # 前缀乘积，初始为 1（空前缀的乘积）
        for i in range(start, len(nums)):
            prod = (prod * nums[i]) % k   # 只保留余数，防止数值爆炸
            if prod == xi:
                cnt += 1
        res.append(cnt)
    return res
```

#### 复杂度

- **时间复杂度**：`O(q * n)`（`q` 为查询数，`n` 为数组长度）。  
  `O(n)` 表示“线性增长”，数组越长，花的时间就像排队买咖啡的人数越多，排队时间会等比例变长。
- **空间复杂度**：`O(1)`（只用了常数级的额外变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次查询都要从头遍历一次**。我们需要一种结构，能够 **快速合并区间信息**，从而在 `log n` 的时间内得到任意后缀（`start … n-1`）的答案。

**关键观察**：

1. 对于一个区间 `[l, r]`，如果我们已经知道：
   - 区间内所有 **前缀**（从 `l` 开始到某个位置）的乘积余数出现次数（即频率数组 `freq[0 … k-1]`），
   - 整个区间的乘积余数 `total = product(l … r) % k`，
   
   那么 **左区间 + 右区间** 的信息可以 **通过一次合并** 计算出来。

2. 合并方式  
   - 左子区间的前缀直接保留下来。  
   - 右子区间的前缀如果要放在左子区间后面，它们的余数要 **先乘以左区间的整体余数** 再取模。  
   - 因此右子区间的频率数组需要 **“平移”**：`new_r = (left_total * r) % k`。

这正是 **线段树（Segment Tree）** 擅长的事情：把区间信息存进树的节点，支持 **点更新**（修改 `nums[index]`）和 **区间查询**（合并 `[start, n-1]`），每次只需要 `O(log n)` 个节点。

> **类比**：想象每个节点是一家小卖部，里面记录了从这家店开门到任意时刻（前缀）的销售额余数以及当天的总销售额。两家相邻的小卖部合并成一家大店时，只需要把右边店的销售额先乘以左边店的总额，再重新统计余数，整个过程就像把两段账单拼在一起。

**数据结构设计（每个节点保存）**：

| 字段 | 含义 |
|------|------|
| `freq` | 长度为 `k` 的列表，`freq[r]` 表示该区间内部**以区间左端点为起点**的所有前缀乘积余数为 `r` 的个数 |
| `total`| 区间所有元素的乘积余数 `product % k` |

**叶子节点**（单个元素 `a`）：

- `freq[a % k] = 1`（只有一种长度为 1 的前缀），其余为 0。  
- `total = a % k`。

**合并函数**（左节点 `L`、右节点 `R`）：

```python
def merge(L, R):
    node = Node()
    node.total = (L.total * R.total) % k
    # 先把左区间的前缀直接拷贝过去
    node.freq = L.freq[:]                     # copy
    # 再把右区间的前缀“平移”后累计
    for r in range(k):
        if R.freq[r]:
            new_r = (L.total * r) % k
            node.freq[new_r] += R.freq[r]
    return node
```

**查询**：

- 调用线段树的 `range_query(start, n-1)`，得到一个合并好的节点 `res_node`。  
- 所求的 **x-value** 正是 `res_node.freq[xi]`。

**复杂度**：

- 每次 **点更新**：`O(k log n)`（`k ≤ 5`，可以看作常数）。  
- 每次 **区间查询**：同样 `O(k log n)`。  
- 因此总时间为 `O((q + n) * log n)`，在本题约为 `2 × 10⁴ · log 10⁵`，完全可以通过。

#### 代码（Python）

```python
from typing import List

class Node:
    """线段树节点，保存前缀余数频率和整体乘积余数"""
    __slots__ = ('freq', 'total')
    def __init__(self, k: int):
        self.freq = [0] * k      # freq[r] = 前缀余数为 r 的个数
        self.total = 1           # 整个区间乘积 % k，默认 1（空乘积）

def build(nums: List[int], k: int) -> List[Node]:
    """自底向上构建线段树，返回树的数组（1-indexed）"""
    n = len(nums)
    size = 1
    while size < n:      # 保证 size 为 2 的幂
        size <<= 1
    tree = [Node(k) for _ in range(2 * size)]

    # 初始化叶子节点
    for i, val in enumerate(nums):
        node = tree[size + i]
        r = val % k
        node.freq[r] = 1
        node.total = r

    # 自底向上合并
    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[i << 1], tree[i << 1 | 1], k)
    return tree, size

def merge(left: Node, right: Node, k: int) -> Node:
    """合并两个相邻区间的节点"""
    node = Node(k)
    node.total = (left.total * right.total) % k

    # 左区间的前缀直接拷贝
    node.freq = left.freq[:]   # 深拷贝，防止后面修改左侧

    # 右区间的前缀需要乘以左区间的整体余数后再统计
    for r in range(k):
        cnt = right.freq[r]
        if cnt:
            new_r = (left.total * r) % k
            node.freq[new_r] += cnt
    return node

def point_update(tree: List[Node], size: int, idx: int, new_val: int, k: int):
    """把位置 idx 的值改为 new_val，并向上更新线段树"""
    pos = size + idx
    # 更新叶子节点
    leaf = tree[pos]
    leaf.freq = [0] * k
    r = new_val % k
    leaf.freq[r] = 1
    leaf.total = r

    # 向上合并
    pos >>= 1
    while pos:
        tree[pos] = merge(tree[pos << 1], tree[pos << 1 | 1], k)
        pos >>= 1

def range_query(tree: List[Node], size: int, l: int, r: int, k: int) -> Node:
    """查询闭区间 [l, r]，返回合并后的节点"""
    l += size
    r += size
    # 为了能够合并，需要分别维护左侧结果和右侧结果
    left_res = None
    right_res = None
    while l <= r:
        if l & 1:                     # l 是右子节点，直接取
            left_res = merge(left_res, tree[l], k) if left_res else tree[l]
            l += 1
        if not (r & 1):               # r 是左子节点，直接取
            right_res = merge(tree[r], right_res, k) if right_res else tree[r]
            r -= 1
        l >>= 1
        r >>= 1
    # 最终合并左右结果
    if left_res is None:
        return right_res
    if right_res is None:
        return left_res
    return merge(left_res, right_res, k)

def solve(nums: List[int], k: int, queries: List[List[int]]) -> List[int]:
    """
    主函数：返回每个查询的答案
    时间复杂度 O((n + q) * log n) ，k ≤ 5 是常数
    """
    tree, size = build(nums, k)
    ans = []
    for index, value, start, xi in queries:
        # 1️⃣ 更新
        point_update(tree, size, index, value, k)
        # 2️⃣ 查询 start … n-1
        node = range_query(tree, size, start, len(nums) - 1, k)
        ans.append(node.freq[xi])
    return ans
```

> **代码说明**（关键行中文注释已在代码中标出）  
- `Node` 用来保存每个线段树节点的两类信息。  
- `build` 把数组转成完整的线段树，先填叶子再自底向上合并。  
- `merge` 实现上文的“左+右”合并规则。  
- `point_update` 负责把单个元素改成新值，并沿树向上重新合并。  
- `range_query` 采用常见的 **迭代区间查询** 写法，返回 `[l, r]` 的综合信息。  
- `solve` 按题目要求依次处理所有查询，收集答案。

#### 复杂度

- **时间复杂度**：  
  - 建树 `O(n)`（一次遍历），  
  - 每次 **点更新** `O(k log n)`，每次 **区间查询** `O(k log n)`。  
  因为 `k ≤ 5` 是常数，整体可写作 **`O((n + q) log n)`**。  
  与暴力的 `O(q·n)` 相比，`log n`（约 17）比 `n`（最高 10⁵）小得多，速度提升数千倍。

- **空间复杂度**：  
  - 线段树需要 `2 * size` 个节点，每个节点保存长度为 `k` 的数组。  
  - `size` 为最近的 2 的幂，最多 `2 * 2ⁿ ≈ 4n`。  
  - 因此 **`O(n * k)`**，在本题 `k ≤ 5`，可以视作 **`O(n)`**。  
  - 额外的递归/迭代栈空间为 `O(log n)`，同样是线性级别的常数因子。

---

## 心得

- **核心技巧**：利用线段树把「区间前缀乘积余数的频率」进行**可合并的压缩信息**存储。  
- **适用的题型**  
  1. 需要在 **区间内统计前缀/子数组的某种累计属性**（如和、乘积、异或）出现次数的题目。  
  2. **区间更新后，快速求解某种模运算统计**（如求子数组和 % k 的分布）。  
  3. 类似的 “**求区间前缀和的出现次数**” 题目（如 “Range Sum Query – Immutable” 的计数变体）。
- **一句话总结解题钥匙**：**把“前缀统计”压缩进每个节点，只要把左侧整体乘进去，就能在 O(log n) 内合并得到任意后缀的答案**。

---

## 反思

- **拿到题目第一反应**：先想到“遍历所有前缀”。因为题目只要求“前缀乘积 % k”，直觉上最容易实现的就是逐个累乘。
- **最容易踩的坑**  
  1. **乘积溢出**：`nums[i]` 可达 `10⁹`，直接相乘会超出 Python 整数的范围（虽然 Python 自动大整数，但会导致极慢）。**取模**要在每一步完成。  
  2. **空前缀的处理**：题目允许“删除空后缀”，即保留完整数组，这对应 “从 `start` 到数组末尾的全部元素” 的前缀，需要计入。  
  3. **合并时的余数平移**：忘记把右区间的余数先乘以左区间的整体余数就会得到错误的计数。  
  4. **k 的取值很小**（≤5），但如果写成 `O(k² log n)` 仍然可以接受；若忘记利用 `k` 小的特性，可能会写出不必要的复杂度。
- **下次遇到同类题，第一步该想到**：**是否可以把“前缀/子数组的累计信息”用线段树或树状数组的“可合并状态”保存**，从而把线性遍历换成对数时间的区间合并。这样可以把“每次查询都要遍历”的瓶颈直接击破。