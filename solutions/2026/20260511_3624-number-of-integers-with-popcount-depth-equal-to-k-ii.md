# #3624. Popcount 深度等于 K 的整数个数 II / Number of Integers With Popcount-Depth Equal to K II

> 难度：困难 · 标签：Array、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/number-of-integers-with-popcount-depth-equal-to-k-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
For any positive integer x, define the following sequence:
This sequence will eventually reach the value 1.
The popcount-depth of x is defined as the smallest integer d >= 0 such that pd = 1.
For example, if x = 7 (binary representation "111"). Then, the sequence is: 7 → 3 → 2 → 1, so the popcount-depth of 7 is 3.
You are also given a 2D integer array queries, where each queries[i] is either:
Return an integer array answer, where answer[i] is the number of indices for the ith query of type [1, l, r, k].

**Examples**

**Example 1:**

```
Input: nums = [2,4], queries = [[1,0,1,1],[2,1,1],[1,0,1,0]]
Output: [2,1]
Explanation:
Thus, the final answer is [2, 1] .
```

**Example 2:**

```
Input: nums = [3,5,6], queries = [[1,0,2,2],[2,1,4],[1,1,2,1],[1,0,1,0]]
Output: [3,1,0]
Explanation:
Thus, the final answer is [3, 1, 0] .
```

**Example 3:**

```
Input: nums = [1,2], queries = [[1,0,1,1],[2,0,3],[1,0,0,1],[1,0,0,2]]
Output: [1,0,1]
Explanation:
Thus, the final answer is [1, 0, 1] .
```

**Constraints**

- 1 <= n == nums.length <= 105
- 1 <= nums[i] <= 1015
- 1 <= queries.length <= 105
- queries[i].length == 3 or 4

queries[i] == [1, l, r, k] or,
queries[i] == [2, idx, val]
0 <= l <= r <= n - 1
0 <= k <= 5
0 <= idx <= n - 1
1 <= val <= 1015
- queries[i] == [1, l, r, k] or,
- queries[i] == [2, idx, val]
- 0 <= l <= r <= n - 1
- 0 <= k <= 5
- 0 <= idx <= n - 1
- 1 <= val <= 1015

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
对于任意正整数 `x`，定义如下序列：

该序列最终会收敛到值 `1`。  
`x` 的 **popcount 深度**（popcount 表示二进制中 `1` 的个数）定义为最小的整数 `d ≥ 0`，使得 `p^d = 1`。  

例如，若 `x = 7`（二进制表示为 `"111"`），则序列为 `7 → 3 → 2 → 1`，因此 `7` 的 popcount 深度为 `3`。  

同时给定一个二维整数数组 `queries`，其中每个 `queries[i]` 为以下两种形式之一：

* `[1, l, r, k]`：统计下标 `i`（`l ≤ i ≤ r`）满足 `nums[i]` 的 popcount 深度等于 `k` 的个数。  
* `[2, idx, val]`：将 `nums[idx]` 的值更新为 `val`。  

返回一个整数数组 `answer`，其中 `answer[i]` 为第 `i` 个类型为 `[1, l, r, k]` 的查询的答案。  

---

### 示例

#### 示例 1  
**输入**  
```
nums = [2,4], queries = [[1,0,1,1],[2,1,1],[1,0,1,0]]
```
**输出**  
```
[2,1]
```
**解释**  
第一个查询 `[1,0,1,1]` 要求统计区间 `[0,1]` 中 popcount 深度等于 `1` 的整数个数，答案为 `2`。  
第二个查询是更新操作，将下标 `1` 的值改为 `1`。  
第三个查询 `[1,0,1,0]` 统计区间 `[0,1]` 中 popcount 深度等于 `0` 的整数个数，答案为 `1`。  
因此最终返回 `[2, 1]`。

#### 示例 2  
**输入**  
```
nums = [3,5,6], queries = [[1,0,2,2],[2,1,4],[1,1,2,1],[1,0,1,0]]
```
**输出**  
```
[3,1,0]
```
**解释**  
- 第一个查询 `[1,0,2,2]` 的答案为 `3`。  
- 第二个查询将下标 `1` 的值更新为 `4`。  
- 第三个查询 `[1,1,2,1]` 的答案为 `1`。  
- 第四个查询 `[1,0,1,0]` 的答案为 `0`。  
最终返回 `[3, 1, 0]`。

#### 示例 3  
**输入**  
```
nums = [1,2], queries = [[1,0,1,1],[2,0,3],[1,0,0,1],[1,0,0,2]]
```
**输出**  
```
[1,0,1]
```
**解释**  
- 第一个查询 `[1,0,1,1]` 的答案为 `1`。  
- 第二个查询将下标 `0` 的值更新为 `3`。  
- 第三个查询 `[1,0,0,1]` 的答案为 `0`。  
- 第四个查询 `[1,0,0,2]` 的答案为 `1`。  
最终返回 `[1, 0, 1]`。

---

### 约束条件

- `1 ≤ n == nums.length ≤ 10^5`
- `1 ≤ nums[i] ≤ 10^15`
- `1 ≤ queries.length ≤ 10^5`
- `queries[i].length == 3` 或 `4`
- `queries[i]` 为 `[1, l, r, k]` 或 `[2, idx, val]`
- `0 ≤ l ≤ r ≤ n - 1`
- `0 ≤ k ≤ 5`
- `0 ≤ idx ≤ n - 1`
- `1 ≤ val ≤ 10^15`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是 **把每一次查询都完整地跑一遍**：

1. **求深度**：对数组 `nums[i]` 计算它的 *popcount‑depth*（把数字不断换成二进制中 `1` 的个数，直到等于 1，记录换了几次）。  
2. **查询**：遇到类型为 `[1, l, r, k]` 的询问时，遍历下标 `l … r`，把深度等于 `k` 的元素计数。  
3. **更新**：遇到类型为 `[2, idx, val]` 的修改时，直接把 `nums[idx]` 改成 `val`，并重新计算该位置的深度。

> **类比**：把数组想象成一本书的每一页，`popcount-depth` 就是每页的“章节数”。查询相当于让你在某几页之间数出章节数恰好等于 `k` 的页数。暴力解法就是一本一本翻，逐页检查。

这个方法**一定能得到正确答案**，因为我们没有遗漏任何下标，也没有对深度的计算做近似。

#### 代码（Python）

```python
def popcount(x: int) -> int:
    """返回 x 的二进制中 1 的个数，等价于 bin(x).count('1')"""
    return bin(x).count('1')

def depth(x: int) -> int:
    """返回 x 的 popcount-depth（直到等于 1 为止的步数）"""
    d = 0
    while x != 1:          # 当 x 不是 1 时继续循环
        x = popcount(x)    # 把 x 换成它的 1 的个数
        d += 1
    return d                # 最终返回步数

def solve_bruteforce(nums, queries):
    # 预先算一次深度，后面更新时再重新算
    dep = [depth(v) for v in nums]

    ans = []
    for q in queries:
        if q[0] == 1:                     # 查询 [1, l, r, k]
            _, l, r, k = q
            cnt = 0
            for i in range(l, r + 1):    # 暴力遍历区间
                if dep[i] == k:
                    cnt += 1
            ans.append(cnt)

        else:                             # 更新 [2, idx, val]
            _, idx, val = q
            nums[idx] = val               # 改数组
            dep[idx] = depth(val)         # 重新计算该位置的深度
    return ans
```

#### 复杂度  

- **时间复杂度**  
  - 计算深度本身是 `O(log value)`（因为每次 popcount 至少把数字减半），这里可以近似记作 `O(60)`，即常数。  
  - 对每个查询 `[1, l, r, k]`，我们要遍历 `r‑l+1` 个元素，最坏情况下是遍历整个数组 `n`，所以 **每次查询 O(n)**。  
  - 对每个更新 `[2, idx, val]`，只需要重新算一次深度，**O(1)**（常数）。  
  - 总体来说，若有 `q` 条查询，最坏时间是 **O(q·n)**，在 `n, q ≤ 10⁵` 时会超时。

- **空间复杂度**  
  - 只用了原数组和深度数组，都是 `O(n)` 的额外空间。  

> **大白话**：`O(n)` 就像“一次要检查 n 本书”，如果查询很多，就相当于要翻好几遍整本书，时间会爆炸。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次查询都要线性遍历区间**。我们需要一种**能够快速统计区间内某个属性出现次数**的数据结构。常见的有：

- **前缀和**：适用于“固定属性”，但这里属性是 **深度**，而深度的取值只有 0‒5（题目限制 `k ≤ 5`），因此可以为每一种深度单独维护一个前缀和结构。
- **树状数组（Fenwick Tree）** 或 **线段树**：同样支持“区间求和 + 单点修改”，且实现更简洁。

这里使用 **6 棵 Fenwick 树**（编号 0‒5），第 `d` 棵树记录下标 `i` 上 **深度恰好等于 `d`** 的信息：

- 当 `depth[i] == d` 时，`fenw[d].add(i, 1)`，否则不加。
- **查询** `[1, l, r, k]` 只需要在第 `k` 棵树上求区间和：`fenw[k].sum(r) - fenw[k].sum(l-1)`，时间 `O(log n)`。
- **更新** `[2, idx, val]`  
  1. 先把原来的深度从对应的树中减掉：`fenw[old].add(idx, -1)`。  
  2. 计算新值的深度 `new = depth(val)`，再加进去：`fenw[new].add(idx, 1)`。  
  这两次都是 `O(log n)`。

> **类比**：把每个深度看成一种颜色的标记笔，Fenwick 树相当于每种颜色的“计数器”。查询时只打开对应颜色的计数器，立刻得到区间里有多少该颜色的标记。

**为什么只需要 0‒5**：  
`popcount-depth` 对任意正整数最多不超过 5（因为 `value ≤ 10¹⁵ < 2⁵⁰`，每次 popcount 至少把数字压缩到 ≤ 50，再几次就到 1）。所以我们只需维护 6 棵树。

#### 代码（Python）

```python
class Fenwick:
    """Fenwick 树（亦称二叉索引树），支持单点增减和前缀和查询"""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)          # 1-indexed

    def add(self, idx: int, delta: int):
        """在位置 idx（0-indexed）上加 delta"""
        i = idx + 1                       # 转成 1-indexed
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i                   # lowbit，跳到下一个负责的区间

    def sum(self, idx: int) -> int:
        """返回前缀和 sum[0..idx]（若 idx < 0 返回 0）"""
        if idx < 0:
            return 0
        i = idx + 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        """返回区间 [l, r] 的和"""
        return self.sum(r) - self.sum(l - 1)


def popcount(x: int) -> int:
    return bin(x).count('1')


def depth(x: int) -> int:
    """计算 x 的 popcount-depth，深度最多 5"""
    d = 0
    while x != 1:
        x = popcount(x)
        d += 1
    return d


def solve_optimal(nums, queries):
    n = len(nums)

    # 1️⃣ 预处理：算出每个位置的深度
    dep = [depth(v) for v in nums]

    # 2️⃣ 为每个可能的深度（0~5）建一棵 Fenwick 树
    fenw = [Fenwick(n) for _ in range(6)]
    for i, d in enumerate(dep):
        fenw[d].add(i, 1)               # 深度为 d 的位置记 1

    ans = []
    for q in queries:
        if q[0] == 1:                    # 查询类型 [1, l, r, k]
            _, l, r, k = q
            cnt = fenw[k].range_sum(l, r)   # O(log n)
            ans.append(cnt)

        else:                            # 更新类型 [2, idx, val]
            _, idx, val = q
            old = dep[idx]               # 旧的深度
            fenw[old].add(idx, -1)       # 从旧树中减去 1

            new = depth(val)             # 计算新值的深度
            dep[idx] = new               # 更新记录
            fenw[new].add(idx, 1)        # 把 1 加到对应的新树

    return ans
```

#### 复杂度  

- **时间复杂度**  
  - **预处理**：遍历 `nums` 计算深度 `O(n·log value)`，这里可以视作 `O(n)`（常数 60）。  
  - **每次查询** `[1, l, r, k]`：一次 Fenwick 前缀和差，**`O(log n)`**。  
  - **每次更新** `[2, idx, val]`：两次单点增减（旧深度、旧深度），每次 `O(log n)`，共 **`O(log n)`**。  
  - 整体 **`O((n + q)·log n)`**，在 `n, q ≤ 10⁵` 下轻松通过。

- **空间复杂度**  
  - 深度数组 `dep`：`O(n)`。  
  - 6 棵 Fenwick 树，每棵大小 `n+1`，共 `6·O(n)`，仍是 **`O(n)`**。  

> **对比**：暴力解的每次查询是 `O(n)`，相当于“一次要遍历整本书”。最优解把查询压到 `O(log n)`，只需“看几页的目录”，快了几个数量级。

---

## 心得

- **核心技巧**：**把离散的属性（深度）拆分成若干类，每类用一棵 Fenwick 树维护**，从而实现**区间计数 + 单点修改**的高效操作。  
- **适用的题型**  
  1. “区间内出现次数等于 k 的元素个数”，如本题。  
  2. “区间内最大/最小值的出现次数”，可以把每个可能的值（或离散化后）单独建树。  
  3. “区间内颜色/标签统计”，每种颜色对应一棵树（或使用线段树的懒标记）。  
- **一句话总结**：**把“属性 = k”的判定转化为“在第 k 棵树上查询区间和”，即可在对数时间完成统计**。

---

## 反思

- **第一反应**：看到“区间查询 + 单点更新”，自然想到**树状数组或线段树**；但因为属性是“深度”，一开始会尝试把深度直接存进树的节点里，结果仍需要遍历区间，没能降到 `O(log n)`。  
- **最容易踩的坑**  
  1. **深度上限**：一定要证明 `popcount-depth ≤ 5`（或 `≤ 6`），否则需要更多的树。  
  2. **下标偏移**：Fenwick 树是 1‑indexed，忘记转换会导致越界或错误的前缀和。  
  3. **更新时忘记删除旧深度**：只添加新深度会导致计数累计错误。  
- **下次遇到同类题**：第一步先检查属性的取值范围是否**离散且小**，如果是，就考虑**为每个取值建立独立的计数结构**（Fenwick/线段树），再利用“区间和 - 单点修改”完成高效解答。