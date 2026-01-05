# #3480. 最大化子数组数量（删除一个冲突对后） / Maximize Subarrays After Removing One Conflicting Pair

> 难度：困难 · 标签：Array、Segment Tree、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximize-subarrays-after-removing-one-conflicting-pair/)

---

## 题目（英文原版）

**Description**

You are given an integer n which represents an array nums containing the numbers from 1 to n in order. Additionally, you are given a 2D array conflictingPairs, where conflictingPairs[i] = [a, b] indicates that a and b form a conflicting pair.
Remove exactly one element from conflictingPairs. Afterward, count the number of non-empty subarrays of nums which do not contain both a and b for any remaining conflicting pair [a, b].
Return the maximum number of subarrays possible after removing exactly one conflicting pair.

**Examples**

**Example 1:**

```
Input: n = 4, conflictingPairs = [[2,3],[1,4]]
Output: 9
Explanation:
```

**Example 2:**

```
Input: n = 5, conflictingPairs = [[1,2],[2,5],[3,5]]
Output: 12
Explanation:
```

**Constraints**

- 2 <= n <= 105
- 1 <= conflictingPairs.length <= 2 * n
- conflictingPairs[i].length == 2
- 1 <= conflictingPairs[i][j] <= n
- conflictingPairs[i][0] != conflictingPairs[i][1]

---

## 题目（中文翻译）

给定一个整数 `n`，它表示数组 `nums`，该数组按顺序包含从 `1` 到 `n` 的所有整数。同时，给定一个二维数组 `conflictingPairs`，其中 `conflictingPairs[i] = [a, b]` 表示 `a` 与 `b` 构成一个冲突对（conflicting pair）。  
从 `conflictingPairs` 中**恰好删除一个**元素。随后，统计 `nums` 的所有非空子数组（subarray），要求这些子数组中不同时包含任意剩余冲突对 `[a, b]` 的两个元素 `a` 与 `b`。  
返回在恰好删除一个冲突对后，能够得到的子数组数量的最大值。

### 示例

#### 示例 1
**输入**: `n = 4, conflictingPairs = [[2,3],[1,4]]`  
**输出**: `9`  
**解释**：

#### 示例 2
**输入**: `n = 5, conflictingPairs = [[1,2],[2,5],[3,5]]`  
**输出**: `12`  
**解释**：

### 约束条件
- `2 <= n <= 10^5`
- `1 <= conflictingPairs.length <= 2 * n`
- `conflictingPairs[i].length == 2`
- `1 <= conflictingPairs[i][j] <= n`
- `conflictingPairs[i][0] != conflictingPairs[i][1]`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

> **题目再说一遍**  
> - 给定 `n`，数组 `nums = [1,2,…,n]`（自然递增）  
> - `conflictingPairs` 中的每一对 `[a,b]` 表示子数组 **不能同时** 包含 `a` 与 `b`（顺序不重要）  
> - 必须**恰好**删除 `conflictingPairs` 中的一对，然后统计在剩余冲突对约束下，`nums` 中所有**非空**子数组的个数。  
> - 求最大可能的子数组数量。

最直接的想法是：**枚举要删掉的那一对**，对每一种情况都算一次合法子数组的数量，最后取最大值。

实现时，我们把剩下的冲突对放进一个集合 `S`。遍历数组的每个左端点 `l`，用一个指针 `r` 向右扩展，只要当前窗口 `[l,r]` 不包含任意冲突对中的两个元素，就继续扩大；一旦出现冲突，就停止。此时 `l` 为左端点，`r-1` 为该左端点能够到达的最右位置，合法子数组数为 `r-l`（因为 `[l,l] , [l,l+1] , … , [l,r-1]` 都合法）。把所有左端点的贡献相加即可。

> **类比**  
> - **哈希表** 就像一本字典，`key` 是数字，`value` 是它在窗口里出现的次数。  
> - 当窗口里出现冲突对的两个 `key` 时，就相当于在字典里找到了同一页的两个词，必须把窗口收回。

> **为什么正确**  
> - 每个左端点 `l` 都只统计一次最长合法右端点 `r-1`，所有以 `l` 为左端点的子数组正好是 `r-l` 个，且没有遗漏或重复。

> **复杂度分析（大白话）**  
> - 枚举要删的冲突对：`m = len(conflictingPairs)` 次。  
> - 对每一次枚举，双指针遍历整个数组一次（左指针 `l` 走 `n` 步，右指针 `r` 只向右走最多 `n` 步），所以是 `O(n)`。  
> - 总体时间复杂度 `O(m·n)`。  
> - 额外使用的哈希表只存当前窗口里出现的数字，最多 `n` 个，空间 `O(n)`。

> **在实际数据里**：`n` 可达 `10⁵`，`m` 也可能接近 `2·n`，`m·n` 会是 `10¹⁰` 级，根本跑不完——所以我们需要更快的办法。

#### 代码（Python）

```python
from collections import defaultdict

def brute_max_subarrays(n: int, pairs):
    """暴力实现，仅用于说明思路，实际会超时。"""
    # 预处理：把每对转成 (min, max) 方便后面使用
    norm = [(min(a, b), max(a, b)) for a, b in pairs]
    m = len(norm)
    best = 0

    for rm in range(m):                     # 枚举要删掉的那一对
        # 把剩余冲突对放进集合，使用字典统计出现次数
        bad = set()
        for i, (x, y) in enumerate(norm):
            if i != rm:
                bad.add((x, y))

        cnt = 0
        freq = defaultdict(int)            # 窗口里每个数字出现次数
        r = 1                               # 右指针（1-indexed）

        for l in range(1, n + 1):          # 左指针从 1 到 n
            # 把左端点 l 加入窗口
            freq[l] += 1

            # 如果加入后出现冲突，就一直收缩左端点，直到冲突消失
            while True:
                conflict = False
                # 检查窗口里是否出现任意冲突对的两个数字
                for x, y in bad:
                    if freq[x] > 0 and freq[y] > 0:
                        conflict = True
                        break
                if not conflict:
                    break
                # 收缩左端点：把 l 从窗口里移除
                freq[l] -= 1
                l += 1
                if l > n:        # 已经走完
                    break

            # 此时窗口 [l, r]（r 尚未移动）是合法的，尝试把 r 往右扩
            while r <= n:
                freq[r] += 1
                # 检查新增的 r 是否导致冲突
                conflict = any(freq[x] > 0 and freq[y] > 0 for x, y in bad)
                if conflict:
                    freq[r] -= 1          # 把 r 再踢出窗口
                    break
                r += 1

            # 以当前左端点 l 为起点的合法子数组个数是 r - l
            cnt += r - l

        best = max(best, cnt)

    return best
```

> **代码要点注释**（已在代码中用中文解释）

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - `m` 是冲突对的数量，`n` 是数组长度。  
  - 对每个被删的冲突对，都要完整遍历一次数组。

- **空间复杂度**：`O(n)`  
  - 只用了一个哈希表 `freq` 来记录窗口里出现的数字，最多 `n` 个键。

---

### 2. 最优解

#### 思路

暴力解的瓶颈在于**每次枚举删除的冲突对都要重新遍历整个数组**。我们要把“遍历数组”这一步**复用**，让所有 `m` 种删除方案在 **一次** 或 **少数几次** 的遍历里就能得到答案。

下面分几步推导出高效算法。

---

##### 2.1 把子数组合法性转化为「起点的最远右端点」

对固定的冲突对集合（不删任何对），记  

> `f[i]` = **以 i 为左端点的最长合法子数组的右端点**（含），  
> 若没有任何冲突限制，则 `f[i] = n`。

只要知道所有 `f[i]`，合法子数组总数很容易求：

```
以 i 为左端点的合法子数组数 = f[i] - i + 1
答案 = Σ (f[i] - i + 1)   (i = 1 … n)
      = Σ f[i] - n·(n+1)/2 + n
```

所以核心任务是**维护 `f[i]`**。

---

##### 2.2 只看「左端点 ≥ i」的冲突对

设冲突对为 `(l, r)` 且 `l < r`（若相反则换序）。  
如果子数组左端点 `i ≤ l`，一旦右端点 `≥ r`，子数组里就同时出现 `l` 与 `r`，冲突成立。  
因此：

```
对所有左端点 i，f[i] = min_{ (l,r) 且 l ≥ i } (r-1)
如果不存在满足条件的冲突对，则 f[i] = n
```

换句话说，**只要把每个左端点 `l` 关联一个 “限制右端点 ≤ r-1”**，  
`f[i]` 就是 **从 i 开始往右看，所有限制值的最小值**。

这正好是**后缀最小**的结构：  
- 设 `best[l] = min_{pair with left = l} (r-1)`（如果没有则记作 `∞`）  
- `f[i] = min( best[i], best[i+1], … , best[n] )`  

只要一次从右往左的遍历，就能得到全部 `f[i]`（**O(n + m)**）。

---

##### 2.3 删除一对会产生的变化

删除 `(l, r)` 后，**只影响左端点 `i ≤ l`** 的 `f[i]`，因为只有这些起点会把 `l` 纳入子数组。  
如果 `(l, r)` 是这些 `i` 中**最严格的限制**（即最小的 `r-1`），删除它会让 `f[i]` **上升** 到**第二小**的限制值；否则 `f[i]` 完全不变。

于是我们只需要知道：

1. 对每个起点 `i`，**最小限制** `min1[i]`（即 `f[i]`）  
2. 对每个起点 `i`，**第二小限制** `min2[i]`（如果不存在第二小，则视为 `n`）  

如果我们能快速得到这两列数组，就可以在 **O(1)** 时间算出删除任意冲突对后的答案：

```
total = Σ min1[i]                     # 所有冲突对都保留时的 Σ f[i]
删除对 (l,r) 影响的起点集合 = [L , R]   （见下节如何求）
答案 = total - Σ_{i∈[L,R]} min1[i] + Σ_{i∈[L,R]} min2[i]
```

所以任务变成**两件事**：

- **(A)** 计算 `min1[i]`、`min2[i]`（一次扫线即可）  
- **(B)** 对每条冲突对，找出它在 `min1` 中“掌权”的那段连续区间 `[L,R]`（即它是 **唯一最小** 的那段）

下面分别说明这两件事的实现细节。

---

##### 2.4 (A) 计算 `min1`、`min2` —— 使用多集合（堆 + 计数）

从右往左遍历 `i = n … 1`：

| 步骤 | 说明 |
|------|------|
| 1. 把所有左端点恰好等于 `i` 的冲突对的值 `v = r-1` 插入**多集合**（可以用 `heapq` + `Counter`）| 多集合能在 `O(log m)` 取到最小值和次小值 |
| 2. 读取当前集合的最小值 `min1[i]`（若集合为空记 `n`）| 这就是 `f[i]` |
| 3. 再读取第二小的值 `min2[i]`（若集合大小 < 2 记 `n`）| 这就是删掉唯一最小后 `i` 能达到的最右端点 |

整个过程只涉及 **插入** 和 **取最小/次小** 两种堆操作，时间 `O((n+m)·log m)`，空间 `O(m)`（存所有冲突对的值）。

---

##### 2.5 (B) 找到每对冲突对的“掌权区间”

观察 `min1[i]` 的形成过程：  
当我们从右往左扫描时，**集合的最小值只能单调不增**（因为我们只往集合里加入新元素，永远不会删掉）。  
因此，当出现一个更小的值 `v`（来自某对 `(l, r)`），它会立即成为 **所有更左的起点**（即 `i ≤ l`）的最小值，直到再出现更小的值覆盖它为止。  

这说明 **每条冲突对在 `min1` 中的最小区间是一段连续的左端点区间**，形如 `[L , R]`，且：

- `R` 正好是这条冲突对的左端点 `l`（因为左端点大于 `l` 看不到这条限制）。
- `L` 是**下一个更小的限制**的左端点 `+1`，如果再没有更小的限制，则 `L = 1`。

我们可以用**单调栈**一次性求出所有区间：

1. 按左端点 `l` **降序**（从大到小）遍历所有冲突对。  
2. 栈中维护 **递增的限制值 `v = r-1`**。  
3. 对当前冲突对 `(l, v)`：  
   - 弹出栈顶所有 `v_top ≥ v`（因为它们被更小的 `v` 覆盖，区间结束在 `l-1`）。  
   - 被弹出的每条记录得到它的左区间下界 `L = l + 1`（因为当前更小的限制出现在 `l`），上界 `R = l_top`（它自己的左端点）。  
   - 把当前 `(l, v)` 推入栈。  
4. 扫描结束后，栈里剩下的记录的下界全部是 `1`，上界仍是各自的左端点。

这样我们在 **O(m)** 时间得到每条冲突对对应的区间 `[L,R]`（如果该对从未成为最小，则区间长度为 0）。

---

##### 2.6 综合答案

准备好以下前缀和：

```
pref1[i] = Σ_{k=1..i} min1[k]
pref2[i] = Σ_{k=1..i} min2[k]
total    = pref1[n]
```

对每条冲突对：

```
seg_sum_min1 = pref1[R] - pref1[L-1]   # 区间内原来的贡献
seg_sum_min2 = pref2[R] - pref2[L-1]   # 删除后提升到第二小的贡献
candidate    = total - seg_sum_min1 + seg_sum_min2
answer       = max(answer, candidate)
```

如果某对的区间为空（`L > R`），`seg_sum_min1 = seg_sum_min2 = 0`，候选值就是 `total`（不影响答案）。

整体时间复杂度：

- 构建 `min1/min2`：`O((n+m)·log m)`（堆）  
- 单调栈求区间：`O(m)`  
- 前缀和 + 遍历求最大值：`O(n + m)`  

**总计 `O((n+m)·log m)`，在 `n ≤ 10⁵`、`m ≤ 2·n` 的限制下轻松 AC。**  
空间使用 `O(n + m)`。

---

#### 代码（Python）

```python
import sys
import heapq
from collections import defaultdict

def maxSubarraysAfterRemovingOnePair(n: int, conflictingPairs):
    """
    返回在恰好删除一条冲突对后，能够得到的最大合法子数组数量。
    时间复杂度 O((n+m)·log m)，空间复杂度 O(n+m)。
    """

    # --------------------------------------------------------------
    # 1️⃣ 预处理：保证每对 (l,r) 满足 l < r，记 val = r-1
    # --------------------------------------------------------------
    m = len(conflictingPairs)
    pairs = []                     # (l, r, val, id)
    by_left = defaultdict(list)   # left -> list of (val, id)
    for idx, (a, b) in enumerate(conflictingPairs):
        l, r = (a, b) if a < b else (b, a)
        val = r - 1
        pairs.append((l, r, val, idx))
        by_left[l].append((val, idx))

    # --------------------------------------------------------------
    # 2️⃣ 计算 min1[i]（最长合法右端点） 与 min2[i]（次小限制）
    #    使用多集合（堆 + Counter）从右往左扫
    # --------------------------------------------------------------
    INF = n                      # 没有限制时相当于 n
    min1 = [0] * (n + 2)         # 1-indexed, min1[i] = f[i]
    min2 = [0] * (n + 2)

    # 小根堆存所有当前限制值，cnt 记录每个值出现次数
    heap = []
    cnt = defaultdict(int)

    def push(v):
        heapq.heappush(heap, v)
        cnt[v] += 1

    def clean_top():
        # 删除已经被弹出的（计数为 0）的堆顶
        while heap and cnt[heap[0]] == 0:
            heapq.heappop(heap)

    for i in range(n, 0, -1):
        # 把左端点恰好为 i 的所有限制加入集合
        for v, _ in by_left[i]:
            push(v)

        clean_top()
        # 取最小值
        if heap:
            min1[i] = heap[0]
        else:
            min1[i] = INF

        # 取次小值：临时弹出一个最小再看下一个
        if heap:
            first = heap[0]
            cnt[first] -= 1          # 暂时把它移除
            clean_top()
            if heap:
                min2[i] = heap[0]
            else:
                min2[i] = INF
            cnt[first] += 1           # 恢复计数
        else:
            min2[i] = INF

    # --------------------------------------------------------------
    # 3️⃣ 前缀和，方便区间求和
    # --------------------------------------------------------------
    pref1 = [0] * (n + 1)   # pref1[i] = Σ_{k=1..i} min1[k]
    pref2 = [0] * (n + 1)
    for i in range(1, n + 1):
        pref1[i] = pref1[i - 1] + min1[i]
        pref2[i] = pref2[i - 1] + min2[i]

    total = pref1[n]                     # Σ min1[i]，即全部冲突对保留时的 Σ f[i]

    # --------------------------------------------------------------
    # 4️⃣ 求每条冲突对的“掌权区间” [L, R]（单调栈）
    # --------------------------------------------------------------
    # 按左端点降序遍历
    pairs_sorted = sorted(pairs, key=lambda x: -x[0])   # -l => 降序
    stack = []                                          # (val, left, id, L) ; L 待填
    segL = [0] * m                                     # 每条冲突对的左区间下界
    segR = [0] * m                                     # 上界 = left

    for l, r, val, pid in pairs_sorted:
        # 弹出所有不比当前更小的（val_top >= val）
        while stack and stack[-1][0] >= val:
            v_top, left_top, id_top, _ = stack.pop()
            # 当前 l 成为它的左区间下界（+1）
            segL[id_top] = l + 1
            segR[id_top] = left_top

        # 把当前压栈，暂时不知道它的下界，等以后被更小值弹出时再填
        stack.append((val, l, pid, None))

    # 栈里剩余的元素没有更小的限制，它们的下界是 1
    while stack:
        v_top, left_top, id_top, _ = stack.pop()
        segL[id_top] = 1
        segR[id_top] = left_top

    # --------------------------------------------------------------
    # 5️⃣ 逐条计算删除该对后的答案，取最大值
    # --------------------------------------------------------------
    answer = total          # 至少等于不删任何限制的情况（题目要求恰好删一对，所以会被覆盖）

    for pid in range(m):
        L, R = segL[pid], segR[pid]
        if L > R:                     # 该对从未是最小限制，删除不影响答案
            candidate = total
        else:
            sum_min1 = pref1[R] - pref1[L - 1]
            sum_min2 = pref2[R] - pref2[L - 1]
            candidate = total - sum_min1 + sum_min2
        if candidate > answer:
            answer = candidate

    # 把 Σ f[i] 转回子数组数量公式
    #   answer_subarrays = Σ f[i] - n·(n+1)/2 + n
    return answer - n * (n + 1) // 2 + n


# --------------------------------------------------------------
# 示例（题目示例已省略具体输入，仅作演示）
# --------------------------------------------------------------
if __name__ == "__main__":
    # 示例 1
    n1 = 4
    pairs1 = [[2, 3], [1, 4]]
    print(maxSubarraysAfterRemovingOnePair(n1, pairs1))   # 期待 9

    # 示例 2
    n2 = 5
    pairs2 = [[1, 2], [2, 5], [3, 5]]
    print(maxSubarraysAfterRemovingOnePair(n2, pairs2))   # 期待 12
```

**代码要点说明（已在代码中用中文注释）**

- 第 2 步的堆实现了**多集合**，能够在 `O(log m)` 取最小/次小值。  
- 第 4 步的单调栈保证每条冲突对只会被弹出一次，得到它在 `min1` 中“统治”的连续区间。  
- 前缀和把区间求和化为 `O(1)`，最终遍历每条冲突对得到答案。

#### 复杂度

- **时间复杂度**：`O((n + m)·log m)`  
  - 堆操作 `O((n+m)·log m)`  
  - 单调栈 `O(m)`  
  - 其余线性遍历 `O(n+m)`

- **空间复杂度**：`O(n + m)`  
  - `min1/min2/prefix` 长度 `n`  
  - 堆、计数、以及保存冲突对的数组 `O(m)`

---

## 心得

- **核心技巧**：把“子数组不能同时出现两点”转化为“每个起点的最远右端点是所有限制的最小值”。  
- **关键数据结构**：  
  1. **多集合（堆 + Counter）** 用来实时得到最小值和次小值。  
  2. **单调栈** 用来一次性找出每条限制在 `min1` 中的统治区间。  
- **适用场景**：  
  - 任意“**左端点受右端点的约束集合的最小值**”的问题（例如“给定若干禁止区间，求每个起点的最右可达位置”）。  
  - “**删除/加入一条约束后，整体最小值如何变化**”的离线求解（可用单调栈或线段树）。  
- **一句话总结**：把所有约束压缩为“每个起点的最小右界”，再用**最小 / 次小** 两层信息快速模拟“删掉唯一最小约束”即可。

---

## 反思

- **第一反应**：直接枚举删除的冲突对，然后用双指针重新统计子数组——这在脑子里最直观，却忽视了 `n`、`m` 的规模。  
- **最容易踩的坑**  
  1. **左/右端点顺序**：一定要把冲突对统一为 `l < r`，否则 `r-1` 可能出现负数。  
  2. **次小值的处理**：如果当前集合只有一个元素，次小值应视为 `n`（相当于没有第二约束），否则会出现 “次小为 INF” 导致答案错误。  
  3. **区间下界的计算**：单调栈弹出时下界应是 “当前更小的左端点 + 1”，容易写成 `+0` 或者忘记 `+1`，导致区间错位。  
- **下次遇到类似题目**：第一步先**抽象出“每个左端点的限制集合的最小值”**，看能否用后缀最小或前缀最小快速得到；如果要求“删掉/加入一条约束”，就考虑**最小与次小**两层信息以及**单调栈**或**线段树**来维护。这样往往能把原本 `O(n·m)` 的暴力降到 `O((n+m)·log)`。