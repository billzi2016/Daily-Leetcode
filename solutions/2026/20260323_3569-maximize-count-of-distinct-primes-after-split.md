# #3569. **最大化拆分后不同质数的数量** / Maximize Count of Distinct Primes After Split

> 难度：困难 · 标签：Array、Math、Segment Tree、Number Theory · [LeetCode 链接](https://leetcode.com/problems/maximize-count-of-distinct-primes-after-split/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums having length n and a 2D integer array queries where queries[i] = [idx, val].
For each query:
Note: The changes made to the array in one query persist into the next query.
Return an array containing the result for each query, in the order they are given.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,1,2], queries = [[1,2],[3,3]]
Output: [3,4]
Explanation:
```

**Example 2:**

```
Input: nums = [2,1,4], queries = [[0,1]]
Output: [0]
Explanation:
```

**Constraints**

- 2 <= n == nums.length <= 5 * 104
- 1 <= queries.length <= 5 * 104
- 1 <= nums[i] <= 105
- 0 <= queries[i][0] < nums.length
- 1 <= queries[i][1] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，长度为 `n`，以及一个二维整数数组 `queries`，其中 `queries[i] = [idx, val]`。  

对每个查询执行以下操作：

> **注意**：一次查询对数组的修改会保留到下一次查询。

返回一个数组，按照查询的顺序依次存放每次查询的结果。

---

### 示例 1

**输入**  
```text
nums = [2,1,3,1,2], queries = [[1,2],[3,3]]
```

**输出**  
```text
[3,4]
```

**解释**  
（此处填写解释）

---

### 示例 2

**输入**  
```text
nums = [2,1,4], queries = [[0,1]]
```

**输出**  
```text
[0]
```

**解释**  
（此处填写解释）

---

### 约束条件

- `2 <= n == nums.length <= 5 * 10^4`
- `1 <= queries.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^5`
- `0 <= queries[i][0] < nums.length`
- `1 <= queries[i][1] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **枚举所有可能的切分位置** `k`（`0 ≤ k < n‑1`），把数组分成左段 `nums[0…k]` 与右段 `nums[k+1…n‑1]`。  
2. 分别把左段、右段里出现的**质数**收集到集合 `L`、`R` 中，集合的大小就是左侧/右侧的**不同质数个数**。  
3. 计算 `|L| + |R|`，取所有 `k` 中的最大值即为答案。  

> **类比**：把数组想成一条街道，质数就像街上不同颜色的灯泡。我们把街道在某个位置 `k` 切开，左边看到的灯泡颜色放进箱子 `L`，右边的放进箱子 `R`，最后把两个箱子里灯泡的种类数相加，找出哪个切点让灯泡种类最多。

**为什么对**：  
- `|L|` 正好是左边不同质数的个数，`|R|` 同理。  
- 求最大值自然就是我们要的答案。

**时间/空间复杂度**  
- 枚举 `k` 需要 `O(n)` 次。  
- 对每个 `k`，收集左、右两段的质数需要遍历整段，最坏是 `O(n)`。  
- 所以总时间是 `O(n²)`（比如 `n = 5·10⁴` 时会慢到爆炸）。  
- 只用了几个集合，空间是 `O(n)`（存放数组本身）。

> **大白话解释**：`O(n²)` 就像把 5 万个人两两配对检查，需要 2.5 × 10⁹ 次操作，普通电脑根本跑不完。

#### 代码（Python）

```python
from math import isqrt

def is_prime(x: int) -> bool:
    """判断 x 是否为质数（暴力版）"""
    if x < 2:
        return False
    for d in range(2, isqrt(x) + 1):
        if x % d == 0:
            return False
    return True


def brute(nums):
    n = len(nums)
    # 预处理每个位置左侧出现的不同质数
    left_sets = [set() for _ in range(n)]
    cur = set()
    for i, v in enumerate(nums):
        if is_prime(v):
            cur.add(v)
        left_sets[i] = cur.copy()

    # 预处理每个位置右侧出现的不同质数
    right_sets = [set() for _ in range(n)]
    cur = set()
    for i in range(n - 1, -1, -1):
        if is_prime(nums[i]):
            cur.add(nums[i])
        right_sets[i] = cur.copy()

    best = 0
    for k in range(n - 1):
        left_cnt = len(left_sets[k])
        right_cnt = len(right_sets[k + 1])
        best = max(best, left_cnt + right_cnt)
    return best
```

> 这段代码仅用于说明思路，实际运行会超时。

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：`O(n)` —— 保存左、右两个前缀/后缀集合的数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定答案的不是每个子数组的全部质数，而是哪些质数跨越了切分点**。  
设质数 `p` 在数组中出现的下标集合为 `pos(p) = {i₁, i₂, …, i_m}`（已升序）。  
- 如果 `m = 1`，`p` 只能出现在左或右，**不可能被计两次**。  
- 如果 `m ≥ 2`，只要切分点 `k` 满足 `i₁ ≤ k < i_m`，`p` 同时出现在左、右两侧，**会被计两次**。

> **类比**：把每个出现两次以上的质数想成一根横跨整条街的绳子，绳子的左端挂在最早出现的位置，右端挂在最晚出现的位置。只要我们在绳子两端之间的任意位置把街道剪开，这根绳子就会被“分成两段”，于是这根绳子对应的质数会在左、右两边各出现一次，计数加 2。

因此：

- **总的不同质数个数** `distinct`（左+右各算一次）是固定的，只和数组里出现了哪些质数有关。  
- **答案 = distinct + max_overlap**，其中 `max_overlap` 是**切分点被多少根跨越的绳子覆盖**的最大值。

于是问题转化为：

> 对所有出现 ≥2 次的质数 `p`，它对应的可行切分区间是 `[first(p), last(p)‑1]`（`first`、`last` 分别是最早、最晚出现的下标）。在 `[0, n‑2]` 这条线段上，找出被**区间覆盖数最多**的点。

这正是**区间加法 + 求最大值**的典型场景，**线段树（Segment Tree）+ 懒标记** 能在 `O(log n)` 时间完成一次区间加/减以及全局最大值查询。

##### 关键数据结构

| 数据结构 | 生活化类比 | 用途 |
|----------|------------|------|
| **哈希表 + 有序列表** (`prime → sorted list of indices`) | “字典查词”——键是质数，值是它出现的所有位置（排好序的） | 快速得到 `first` 与 `last`，并支持插入/删除（`bisect`） |
| **线段树 + 懒标记** | “区间计数器”——把街道分成若干小段，每段记住有多少根绳子压在上面，懒标记相当于把一次大面积的涂色操作延迟到真正需要时才真正去涂 | 对 `[first, last‑1]` 区间做 `+1 / -1`，并随时查询整条街道的最大覆盖数 |

##### 更新细节

一次查询 `[idx, val]` 实际是把 `nums[idx]` **改成** `val`，并且这个改动会保留到后面的查询中。我们需要对 **旧质数** 与 **新质数** 分别做以下三步：

1. **撤销旧区间**（如果旧质数原本出现 ≥2 次）  
   - 对旧质数对应的 `[first, last‑1]` 区间在段树上 `-1`（因为这根绳子不再存在）。
2. **在对应的有序列表中删除/插入下标**（使用 `bisect`）  
   - 删除旧下标，插入新下标。
3. **重新加入新区间**（如果修改后质数出现 ≥2 次）  
   - 计算新的 `first`、`last`，在段树上 `+1`。

同时维护：

- `distinct`：出现次数 ≥1 的质数个数。  
  - 删除下标后如果列表为空，`distinct -= 1`。  
  - 插入下标前如果列表为空，`distinct += 1`。

最后答案：

```python
answer = distinct + segtree.query_max()
```

> 注意：若 `n == 1`（虽然题目保证 `n ≥ 2`），则没有合法切分点，答案就是 `distinct` 本身。

##### 步骤概览

| 步骤 | 操作 | 复杂度 |
|------|------|--------|
| **预处理** | 1️⃣ 用埃拉托斯特尼筛（Sieve）把 `1…10⁵` 的所有质数标记好（O(maxV log log maxV))  <br>2️⃣ 初始化哈希表 `prime → positions`，把每个元素下标加入对应质数的列表 <br>3️⃣ 对每个出现 ≥2 次的质数，在段树上 `+1` 区间 | `O(n log n)`（插入+区间更新） |
| **单次查询** | ① 处理旧质数的撤销区间 <br>② 删除旧下标 <br>③ 处理旧质数的重新加入区间（若仍 ≥2 次） <br>④ 处理新质数的撤销区间（若已有 ≥2 次） <br>⑤ 插入新下标 <br>⑥ 处理新质数的重新加入区间（若 ≥2 次） <br>⑦ 计算 `distinct + segtree.max` | `O(log n)`（段树） + `O(log m)`（列表二分） ≈ `O(log n)` |
| **整体** | `q` 次查询 | `O((n+q) log n)`，完全能通过 `5·10⁴` 规模的限制 |

#### 代码（Python）

```python
import sys
import bisect
from math import isqrt
from collections import defaultdict

# ---------- 1. 质数筛（Sieve） ----------
MAXV = 100_000  # 题目限制的上限
is_prime = [True] * (MAXV + 1)
is_prime[0] = is_prime[1] = False
for p in range(2, isqrt(MAXV) + 1):
    if is_prime[p]:
        step = p * p
        while step <= MAXV:
            is_prime[step] = False
            step += p
# 现在 is_prime[x] 能在 O(1) 判断 x 是否为质数

# ---------- 2. 线段树（区间加、全局最大） ----------
class SegTree:
    """支持区间加、查询整个区间的最大值（懒标记）"""
    __slots__ = ('n', 'tree', 'lazy')
    def __init__(self, size: int):
        self.n = 1
        while self.n < size:
            self.n <<= 1
        self.tree = [0] * (2 * self.n)   # 最大值
        self.lazy = [0] * (2 * self.n)   # 懒标记

    def _push(self, idx: int):
        """把 idx 的懒标记下传到子节点"""
        if self.lazy[idx]:
            for child in (idx << 1, idx << 1 | 1):
                self.tree[child] += self.lazy[idx]
                self.lazy[child] += self.lazy[idx]
            self.lazy[idx] = 0

    def _range_add(self, l: int, r: int, val: int, idx: int, left: int, right: int):
        if r < left or right < l:          # 完全不相交
            return
        if l <= left and right <= r:       # 完全覆盖
            self.tree[idx] += val
            self.lazy[idx] += val
            return
        self._push(idx)                    # 先把懒标记下放
        mid = (left + right) >> 1
        self._range_add(l, r, val, idx << 1, left, mid)
        self._range_add(l, r, val, idx << 1 | 1, mid + 1, right)
        self.tree[idx] = max(self.tree[idx << 1], self.tree[idx << 1 | 1])

    def add(self, l: int, r: int, val: int):
        """在闭区间 [l, r] 上加 val（如果 l>r 则什么也不做）"""
        if l > r:
            return
        self._range_add(l, r, val, 1, 0, self.n - 1)

    def query_max(self) -> int:
        """返回整个区间的最大值"""
        return self.tree[1]

# ---------- 3. 主函数 ----------
def max_distinct_primes(nums, queries):
    n = len(nums)
    # 可切分位置只有 0 … n-2
    seg = SegTree(n - 1)

    # prime -> sorted list of positions where it appears
    pos = defaultdict(list)

    distinct = 0  # 目前出现的不同质数个数

    # ----- 初始化 -----
    for idx, v in enumerate(nums):
        if not is_prime[v]:
            continue
        if not pos[v]:            # 之前还没有出现过这个质数
            distinct += 1
        bisect.insort(pos[v], idx)

    # 把每个出现 >=2 次的质数对应的区间加到线段树
    for p, lst in pos.items():
        if len(lst) >= 2:
            left = lst[0]               # first
            right = lst[-1] - 1         # last-1，切分点只能在左侧下标到 right
            seg.add(left, right, 1)

    ans = []

    # ----- 处理每个查询 -----
    for idx, new_val in queries:
        old_val = nums[idx]
        nums[idx] = new_val                     # 先把数组改掉，后面会恢复 old_val 用到

        # ---------- 处理旧质数 ----------
        if is_prime[old_val]:
            lst = pos[old_val]
            # 1) 若旧质数原本贡献了区间，先撤销
            if len(lst) >= 2:
                seg.add(lst[0], lst[-1] - 1, -1)

            # 2) 删除当前位置
            del_idx = bisect.bisect_left(lst, idx)
            lst.pop(del_idx)

            # 3) 若删除后仍有 >=2 次，重新加入新区间
            if len(lst) >= 2:
                seg.add(lst[0], lst[-1] - 1, 1)

            # 4) 若列表为空，distinct 减 1
            if not lst:
                distinct -= 1
                del pos[old_val]   # 清理，防止 dict 无限增长

        # ---------- 处理新质数 ----------
        if is_prime[new_val]:
            lst = pos[new_val]
            # 1) 若新质数之前已经有 >=2 次，先把旧区间删掉
            if len(lst) >= 2:
                seg.add(lst[0], lst[-1] - 1, -1)

            # 2) 插入新下标
            bisect.insort(lst, idx)

            # 3) 若插入后出现 >=2 次，重新加入区间
            if len(lst) >= 2:
                seg.add(lst[0], lst[-1] - 1, 1)

            # 4) 若之前列表为空（新质数第一次出现），distinct 加 1
            if len(lst) == 1:   # 刚插入后长度为 1，说明之前为空
                distinct += 1

        # ---------- 计算当前答案 ----------
        # 若 n==1（不可能）或 n==2 时，seg.n-1 == 1，仍然可以 query_max()
        cur = distinct + seg.query_max()
        ans.append(cur)

    return ans

# ---------- 4. 交互式测试 ----------
if __name__ == "__main__":
    # 示例 1
    nums1 = [2, 1, 3, 1, 2]
    queries1 = [[1, 2], [3, 3]]
    print(max_distinct_primes(nums1, queries1))   # -> [3, 4]

    # 示例 2
    nums2 = [2, 1, 4]
    queries2 = [[0, 1]]
    print(max_distinct_primes(nums2, queries2))   # -> [0]
```

**代码要点注释（中文）**：

- **质数筛**：一次性把 `1…10⁵` 的所有质数预处理好，后面判断是否为质数只要 `O(1)`。
- **`SegTree`**：`add(l, r, val)` 在闭区间 `[l, r]` 上加 `val`，`query_max()` 返回当前所有切分点被多少根“跨越绳子”覆盖的最大值。
- **`pos`**：`defaultdict(list)` 保存每个质数出现的下标，始终保持有序（`bisect.insort` / `bisect_left`）。
- **更新流程**：先把旧质数对应的覆盖区间减 1，再在列表里删掉下标，随后如果仍然有两次以上再把新区间加 1；对新质数同理，只是顺序是“先减旧区间 → 插入 → 加新区间”。
- **`distinct`**：实时维护当前数组里出现的不同质数数量。答案 = `distinct + 最大覆盖数`。

#### 复杂度  

- **时间复杂度**  
  - 预处理筛 `O(MAXV log log MAXV)`（常数很小）  
  - 初始化 `O(n log n)`（每个元素一次二分插入 + 可能一次区间加）  
  - 每次查询：`O(log n)`（线段树区间加/删） + `O(log m)`（在有序列表中插入/删除，`m` 为该质数出现次数，最坏 `O(log n)`）  
  - 整体 `O((n + q) log n)`，在 `5·10⁴` 规模下轻松跑完。

- **空间复杂度**  
  - 质数筛 `O(MAXV)`  
  - `pos` 保存每个下标一次，合计 `O(n)`  
  - 线段树大小约 `4·(n-1)` → `O(n)`  
  - 总体 `O(n + MAXV)`，约 `1.5×10⁵` 的整数数组，完全符合限制。

---

## 心得

- **核心技巧**：把“左侧/右侧不同质数个数之和”拆解为 **“全部不同质数数目 + 跨越切分点的质数个数”**，后者恰好是 **区间覆盖的最大值**。  
- **适用的题型**  
  1. “在数组上做点更新，求某个切分点的最优值”——如 **“最大子数组和分割”**、**“最大不同元素对数”** 等。  
  2. “维护区间出现次数 ≥2 的元素”，常用 **线段树 + 哈希表**（或 **Fenwick + 离线**）解决。  
- **一句话总结**：**把“计两次的质数”抽象成跨区间的绳子，使用线段树维护绳子覆盖的最大次数**。

---

## 反思

- **第一反应**：看到“左+右的不同质数”，立刻想到**枚举切分点**，这就是暴力解的思路。  
- **最容易踩的坑**  
  1. **忘记把质数出现一次的情况排除**——一次出现的质数只能计一次，不能参与跨区间计数。  
  2. **区间端点的写法**：跨区间的合法切分点是 `[first, last‑1]`，容易写成 `[first, last]` 导致越界或多算。  
  3. **更新时的顺序**：先撤销旧区间再删除下标、再重新加入新区间，顺序搞错会导致覆盖数瞬间出现负值或遗漏。  
  4. **边界情况**：`n = 2` 时只有一个切分点，线段树仍然要建 `size = 1`，否则查询会出错。  

- **下次遇到同类题**：**先把“计两次的元素”抽象成区间”，然后寻找能快速支持**区间增删 + 全局最大/最小查询的**数据结构**（线段树、树状数组+离线等）。这样可以把“暴力 O(n²)”直接降到 “O(log n)”。