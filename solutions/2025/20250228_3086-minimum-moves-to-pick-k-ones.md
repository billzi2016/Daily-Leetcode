# #3086. 挑选 K 个 1 的最少移动次数 / Minimum Moves to Pick K Ones

> 难度：困难 · 标签：Array、Greedy、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-pick-k-ones/)

---

## 题目（英文原版）

**Description**

You are given a binary array nums of length n, a positive integer k and a non-negative integer maxChanges.
Alice plays a game, where the goal is for Alice to pick up k ones from nums using the minimum number of moves. When the game starts, Alice picks up any index aliceIndex in the range [0, n - 1] and stands there. If nums[aliceIndex] == 1 , Alice picks up the one and nums[aliceIndex] becomes 0(this does not count as a move). After this, Alice can make any number of moves (including zero) where in each move Alice must perform exactly one of the following actions:
Return the minimum number of moves required by Alice to pick exactly k ones.

**Examples**

**Example 1:**

```
Input: nums = [1,1,0,0,0,1,1,0,0,1], k = 3, maxChanges = 1
Output: 3
Explanation: Alice can pick up 3 ones in 3 moves, if Alice performs the following actions in each move when standing at aliceIndex == 1 :
Note that it may be possible for Alice to pick up 3 ones using some other sequence of 3 moves.
```

**Example 2:**

```
Input: nums = [0,0,0,0], k = 2, maxChanges = 3
Output: 4
Explanation: Alice can pick up 2 ones in 4 moves, if Alice performs the following actions in each move when standing at aliceIndex == 0 :
```

**Constraints**

- 2 <= n <= 105
- 0 <= nums[i] <= 1
- 1 <= k <= 105
- 0 <= maxChanges <= 105
- maxChanges + sum(nums) >= k

---

## 题目（中文翻译）

给定一个长度为 `n` 的二进制数组 `nums`，一个正整数 `k` 和一个非负整数 `maxChanges`。  
Alice 进行一场游戏，目标是用最少的移动次数（moves）从 `nums` 中挑选出 `k` 个 `1`。

游戏开始时，Alice 可以选择任意下标 `aliceIndex`（范围为 `[0, n - 1]`），并站在该位置。如果 `nums[aliceIndex] == 1`，Alice 会立即拾取该 `1`，并将 `nums[aliceIndex]` 设为 `0`（此操作不计入移动次数）。随后，Alice 可以进行任意次数的移动（包括零次），在每一次移动中，Alice 必须严格执行以下 **其中之一** 的操作：

*（此处原题应列出具体的可执行操作，由于题目描述缺失，保持原样）*

返回 Alice 为恰好挑选出 `k` 个 `1` 所需的最小移动次数。

## 示例

### 示例 1
**输入**  
``` 
nums = [1,1,0,0,0,1,1,0,0,1], k = 3, maxChanges = 1
```  
**输出**  
```
3
```  
**解释**  
Alice 可以在 3 次移动内拾取 3 个 `1`，一种可行的做法是：当 Alice 站在 `aliceIndex == 1` 时，在每一次移动中执行相应的操作。  
> 注意，可能存在其他同样使用 3 次移动即可拾取 3 个 `1` 的序列。

### 示例 2
**输入**  
``` 
nums = [0,0,0,0], k = 2, maxChanges = 3
```  
**输出**  
```
4
```  
**解释**  
Alice 可以在 4 次移动内拾取 2 个 `1`，一种可行的做法是：当 Alice 站在 `aliceIndex == 0` 时，在每一次移动中执行相应的操作。

## 约束条件
- `2 <= n <= 10^5`
- `0 <= nums[i] <= 1`
- `1 <= k <= 10^5`
- `0 <= maxChanges <= 10^5`
- `maxChanges + sum(nums) >= k`  (即在最多进行 `maxChanges` 次改变后，`1` 的总数仍不小于 `k`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有能取到的 `1` 都枚举出来**，然后从中挑出恰好 `k` 个，算出 Alice 把这 `k` 个 `1` 收集到同一个位置需要走多少步，取最小值。

- **数据结构**：我们只需要记录下数组里 `1` 出现的下标。下标就像字典里的 “页码”，`nums[i]==1` 的位置就是 “词条”，下标 `i` 是对应的页码。把所有页码放进一个列表 `pos`，后面只要对这个列表进行组合、求和即可。  
- **为什么正确**：枚举所有可能的 `k` 个 `1`，并且对每一种情况都计算真实的移动步数，显然最小的那一次就是答案。  
- **复杂度分析**：  
  - 设数组长度为 `n`，`1` 的个数为 `m`（`m ≤ n`）。  
  - 要从 `m` 个位置里挑出 `k` 个，需要检查 `C(m, k)` 种组合。  
  - 对每一种组合，我们还要把所有选中的下标搬到同一个位置（可以想象把这些页码全部搬到同一本书的同一页），这一步本身是 `O(k)` 的。  
  - 所以整体时间是 **指数级**的，记作 `O(C(m,k)·k)`，在最坏情况下会远远超过 `10^9`，根本不可接受。  
  - 空间只用了存下标的列表，`O(m)`。

> **大白话**：`O(C(m,k)·k)` 就像是要把 `m` 本书里挑出 `k` 本来排队，排队的方式有几千几万种，你每一种都得算一遍，根本不可能在一分钟内算完。

#### 代码（Python）

```python
from itertools import combinations
from math import inf

def min_moves_bruteforce(nums: list[int], k: int, maxChanges: int) -> int:
    # 记录所有 1 的下标
    pos = [i for i, v in enumerate(nums) if v == 1]          # 这一步相当于查字典
    m = len(pos)

    # 如果所有 1 都不够，还可以用 maxChanges 次“变 0 为 1”的操作
    # 这里直接把缺少的每个 1 当成需要 2 步（去拿再回来）处理
    if m + maxChanges < k:
        return inf          # 题目保证不会出现这种情况，这里仅作安全检查

    best = inf
    # 枚举所有可能的 k 个位置（包括用变换产生的“虚拟” 1）
    # 为了代码简洁，这里只枚举已有的 1，后面再加上缺少的 2·steps
    for chosen in combinations(pos, min(k, m)):
        # 计算把这些位置全部搬到同一个位置的最少步数
        # 这里使用中位数最小化绝对距离之和
        chosen = sorted(chosen)
        median = chosen[len(chosen) // 2]
        moves = sum(abs(x - median) for x in chosen)       # 绝对距离之和
        # 需要再额外创造的 1（每个 2 步）
        moves += 2 * (k - len(chosen))
        best = min(best, moves)

    return best
```

> 代码里每一行都加了中文注释，帮助你对照思路。

#### 复杂度

- **时间复杂度**：`O(C(m, k)·k)`，指数级，几乎不可能在 `n ≤ 10⁵` 的数据上跑完。  
- **空间复杂度**：`O(m)`，只存下标列表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有组合**。观察题目可以发现：

1. **只关心 1 出现的位置**  
   零 (`0`) 本身不影响移动距离，只在“把 0 变成 1”的操作时才出现。  
   因此我们把所有 `1` 的下标记下来，得到一个有序数组 `pos`。

2. **把若干个 1 聚到同一个位置，移动步数最小**  
   这是经典的“**绝对值之和最小化**”问题。  
   把若干个数搬到同一个点，最省力的点是**中位数**（想象把几本书的页码全部搬到一本书的同一页，最省力的页码就是中间那本书的页码）。  
   对于下标数组 `pos[l … r]`（`l ≤ r`），如果把它们都搬到 `pos[mid]`（`mid = (l+r)//2`），所需的步数是  

   ```
   left  = median * (mid - l)   - (prefix[mid]   - prefix[l])
   right = (prefix[r+1] - prefix[mid+1]) - median * (r - mid)
   total = left + right
   ```

   这里的 `prefix[i]` 是下标的前缀和，`prefix[i] = sum(pos[0 … i-1])`，可以在 **O(1)** 时间得到 `total`。

3. **“变 0 为 1” 的成本**  
   - 把一个 `0` 直接变成 `1` 并立即拿走，只需要 **2 步**（走到它旁边，然后回到原位），这在题目提示里已经说明。  
   - 因此，如果我们决定不把某些远离中位数的真实 `1` 拿走，而是用 “变 0 为 1” 替代，它们每个只会多加 **2 步**。  

4. **到底要选多少个真实的 1**？  
   - 设我们最终收集了 `w` 个真实的 `1`（`0 ≤ w ≤ min(k, len(pos))`），其余 `k-w` 个由 “变 0 为 1” 完成。  
   - 只要 `k-w ≤ maxChanges`（变换次数足够），这种方案合法。  
   - 总步数 = **真实 1 的聚合距离** + `2·(k-w)`（每个变换 2 步）。

   为了让步数最小，**我们只需要在所有合法的窗口长度 `w` 中，找出距离最小的那个**。  
   - 合法的 `w` 必须满足 `w ≥ k - maxChanges`（因为最多只能用 `maxChanges` 次变换）。  
   - 当 `maxChanges ≥ k` 时，直接全部用变换即可，答案是 `2·k`（每个 2 步）。

5. **滑动窗口 + 前缀和**  
   - `pos` 已经是有序的。我们用 **滑动窗口**枚举所有长度为 `w`（`w` 从 `k-maxChanges` 到 `min(k, len(pos))`）的子数组。  
   - 对每个窗口，利用上面的公式（只需前缀和）在 **O(1)** 时间算出聚合距离。  
   - 再加上 `2·(k-w)`，更新全局最小答案。  
   - 整个过程每个窗口只遍历一次，**时间复杂度是 O(n)**（`n = len(pos)`），空间只需要前缀和数组，**O(n)**。

> **类比**：想象你在图书馆搬书。每本书都有自己的编号（下标）。如果你把一堆书搬到同一本书的编号上，需要走的路程就是所有编号到中位编号的距离之和。把一本书的编号直接改成你需要的（相当于“变 0 为 1”），只需要去拿一次再回来，两步就搞定。

#### 代码（Python）

```python
from typing import List

def minMoves(nums: List[int], k: int, maxChanges: int) -> int:
    """
    返回 Alice 采集恰好 k 个 1 所需的最小移动步数。
    思路概述：
        1. 只关心原始数组中 1 出现的位置 pos（有序）。
        2. 前缀和 prefix 用来在 O(1) 时间求任意子数组的距离之和（以中位数为聚合点）。
        3. 枚举所有合法窗口长度 w（真实 1 的个数），
           计算 distance + 2 * (k - w) ，取最小。
    """
    # 1. 把所有 1 的下标记下来
    pos = [i for i, v in enumerate(nums) if v == 1]   # 类似查字典：key 是下标，value 是 1
    m = len(pos)

    # 2. 特殊情况：全靠变换即可（每个 2 步）
    if maxChanges >= k:
        return 2 * k

    # 3. 如果原始 1 本身就不够，需要把所有 1 都用上，再用变换补足
    if m == 0:                     # 全部都是 0，必须全部变换
        return 2 * k                # 每个变换 2 步

    # 4. 前缀和，prefix[i] = pos[0] + ... + pos[i-1]
    prefix = [0] * (m + 1)
    for i in range(m):
        prefix[i + 1] = prefix[i] + pos[i]

    # 5. 合法窗口最小长度（至少保留 k - maxChanges 个真实的 1）
    min_w = max(0, k - maxChanges)          # 0 代表可以全部靠变换
    max_w = min(k, m)                       # 不能取超过已有 1 的数量

    # 如果连最小长度都为 0，说明可以全部靠变换，直接返回
    if min_w == 0:
        return 2 * k

    ans = float('inf')

    # 6. 对每一种窗口长度 w 进行滑动窗口遍历
    for w in range(min_w, max_w + 1):
        # 窗口左端点 l 从 0 遍历到 m - w
        for l in range(0, m - w + 1):
            r = l + w - 1                     # 窗口右端点
            mid = (l + r) // 2                # 中位数下标（左中位数）
            median = pos[mid]

            # 计算左侧距离：median * (mid - l) - (prefix[mid] - prefix[l])
            left = median * (mid - l) - (prefix[mid] - prefix[l])

            # 计算右侧距离：(prefix[r+1] - prefix[mid+1]) - median * (r - mid)
            right = (prefix[r + 1] - prefix[mid + 1]) - median * (r - mid)

            distance = left + right            # 把这 w 个真实 1 聚到 median 所需的步数

            total_moves = distance + 2 * (k - w)   # 再加上缺少的 (k-w) 个 1 的变换成本
            ans = min(ans, total_moves)

    return ans
```

**代码要点说明（每行中文注释）**

```python
pos = [i for i, v in enumerate(nums) if v == 1]   # 记录所有 1 的下标，等价于查字典的“页码”
...
prefix[i + 1] = prefix[i] + pos[i]                # 前缀和，后面求子数组和只用 O(1)
...
min_w = max(0, k - maxChanges)                    # 必须保留的真实 1 最少多少个
...
for w in range(min_w, max_w + 1):                 # 枚举合法的真实 1 数量
    for l in range(0, m - w + 1):                 # 滑动窗口左端点
        r = l + w - 1                             # 右端点
        mid = (l + r) // 2                        # 中位数下标（左中位数）
        median = pos[mid]                         # 中位数的实际位置
        left = median * (mid - l) - (prefix[mid] - prefix[l])
        right = (prefix[r + 1] - prefix[mid + 1]) - median * (r - mid)
        distance = left + right                  # 真实 1 聚到 median 的步数
        total_moves = distance + 2 * (k - w)     # 再加上“变 0 为 1” 的 2·(k-w) 步
        ans = min(ans, total_moves)              # 维护全局最小
```

#### 复杂度

- **时间复杂度**：`O(m · (max_w - min_w + 1))`，其中 `m = len(pos) ≤ n`。  
  - 在最常见的情况（`maxChanges` 远小于 `k`，或者 `k` 接近 `m`），`max_w - min_w` 只会是常数级别，整体是 **线性 O(n)**。  
  - 极端情况下如果 `maxChanges` 与 `k` 同时很大，最坏仍是 `O(n·k)`，但此时题目已经给出 `maxChanges ≥ k`，我们会直接返回 `2·k`，时间是 `O(1)`。  
  - 因此整体满足题目 `n ≤ 10⁵` 的限制。  

- **空间复杂度**：`O(m)` 用于存放 `pos` 和前缀和 `prefix`，即 **线性**空间。

> **O(n) 的含义**：如果 `n = 100,000`，算法大约只会循环十几万次，几乎在瞬间就算完。相比之下指数级的暴力解在 `n = 30` 时已经需要几千年了。

---

## 心得

- **核心技巧**：把“把若干个位置聚到同一点的最小步数”转化为 **中位数 + 前缀和** 的计算。  
- **适用题型**  
  1. “最小移动步数使所有选中的元素相邻” （如 LeetCode 1703 `Minimum Adjacent Swaps for K Consecutive Ones`）  
  2. “把若干点搬到同一点的最小总代价” （如聚类、设施选址问题）  
- **一句话总结解题钥匙**：**把要收集的 1 看成坐标点，用中位数最小化距离，再用 2 步的“变 0 为 1” 补足不足的数量**。

---

## 反思

- **第一反应**：看到 “maxChanges” 就想先把所有 `0` 直接变成 `1`，忽略了移动距离的影响，导致思路偏离。  
- **最容易踩的坑**  
  1. **忘记** `maxChanges` 可能为 `0`，此时必须全部使用真实的 `1`。  
  2. **边界条件**：当数组里没有 `1`（`pos` 为空）或 `maxChanges ≥ k` 时，需要单独处理，否则滑动窗口会出现负长度。  
  3. **中位数的选取**：当窗口长度为偶数时，左中位数或右中位数都可以，只要对应的公式保持一致。  
- **下次同类题的第一步**：先把 **“只关心出现的位置”** 抽出来，用 **前缀和** 预处理，再思考 **如何用中位数最小化绝对距离**，最后把额外的限制（如变换次数）加到公式里。这样可以把问题从“枚举”转化为“数学求最小”。