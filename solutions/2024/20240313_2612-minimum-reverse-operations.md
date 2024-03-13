# #2612. 最小反转操作 / Minimum Reverse Operations

> 难度：困难 · 标签：Array、Breadth-First Search、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimum-reverse-operations/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an integer p representing an array arr of length n where all elements are set to 0's, except position p which is set to 1. You are also given an integer array banned containing restricted positions. Perform the following operation on arr:
Return an integer array answer with n results where the ith result is the minimum number of operations needed to bring the single 1 to position i in arr, or -1 if it is impossible.

**Examples**

**Example 1:**

```
Input: n = 4, p = 0, banned = [1,2], k = 4
Output: [0,-1,-1,1]
Explanation:
```

**Example 2:**

```
Input: n = 5, p = 0, banned = [2,4], k = 3
Output: [0,-1,-1,-1,-1]
Explanation:
```

**Example 3:**

```
Input: n = 4, p = 2, banned = [0,1,3], k = 1
Output: [-1,-1,0,-1]
Explanation:
Perform operations of size 1 and 1 never changes its position.
```

**Constraints**

- 1 <= n <= 105
- 0 <= p <= n - 1
- 0 <= banned.length <= n - 1
- 0 <= banned[i] <= n - 1
- 1 <= k <= n
- banned[i] != p
- all values in banned are unique

---

## 题目（中文翻译）

**描述**  
给定整数 `n` 与整数 `p`，表示一个长度为 `n` 的数组 `arr`，其中所有元素均为 `0`，只有下标 `p` 处的元素为 `1`。另给定整数数组 `banned`，其中的下标为受限位置。对 `arr` 执行以下 **operation（操作）**：

返回一个长度为 `n` 的整数数组 `answer`，其中第 `i` 项是将唯一的 `1` 移动到下标 `i` 所需的最少 **operation（操作）** 次数，若无法到达则返回 `-1`。

**示例**

**示例 1**  
```
Input: n = 4, p = 0, banned = [1,2], k = 4
Output: [0,-1,-1,1]
Explanation:
```

**示例 2**  
```
Input: n = 5, p = 0, banned = [2,4], k = 3
Output: [0,-1,-1,-1,-1]
Explanation:
```

**示例 3**  
```
Input: n = 4, p = 2, banned = [0,1,3], k = 1
Output: [-1,-1,0,-1]
Explanation:
执行大小为 1 的 operation（操作）永远不会改变其位置。
```

**约束条件**  
- `1 <= n <= 10^5`  
- `0 <= p <= n - 1`  
- `0 <= banned.length <= n - 1`  
- `0 <= banned[i] <= n - 1`  
- `1 <= k <= n`  
- `banned[i] != p`  
- `banned` 中的所有值互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一次操作都枚举出来**，然后用**广度优先搜索 (BFS)** 找到从起点 `p` 到所有其他位置的最短步数。

- **数组**：我们把数组想象成一排格子，格子里只有一个 `1`，其它都是 `0`。  
- **一次操作**：选取长度恰好为 `k` 的连续子数组，把它整体翻转。翻转后，`1` 所在格子会搬到子数组的对称位置。  
- **遍历所有可能的翻转**：对于当前格子 `cur`，我们把所有合法的子数组左端点 `l`（`0 ≤ l ≤ n‑k` 且 `l ≤ cur ≤ l+k‑1`）都枚举一次，算出翻转后 `1` 会落到的位置 `new = 2*l + k‑1 – cur`，把它加入 BFS 队列。

只要把 **禁止位置 `banned`** 直接排除掉，就可以得到每个格子最少需要的操作次数。

> **为什么这个方法一定能得到答案？**  
> BFS 按层次展开，第一次碰到某个格子时使用的步数就是从起点到该格子的最短路径长度（这就是 BFS 的核心属性）。只要我们把所有合法的翻转都考虑进去，就不会漏掉任何可能的路径。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minimum_reverse_operations_bruteforce(
    n: int, p: int, banned: List[int], k: int
) -> List[int]:
    # ---------- 初始化 ----------
    banned_set = set(banned)               # 查字典：判断一个位置是否被禁止，O(1)
    ans = [-1] * n                         # 最终答案，默认 -1 表示不可达
    ans[p] = 0                             # 起点本身需要 0 步

    q = deque([p])                         # BFS 队列
    visited = {p} | banned_set             # 已访问或禁止的格子都不再入队

    # ---------- BFS ----------
    while q:
        cur = q.popleft()
        # 所有可能的子数组左端点 l，使得 cur 落在子数组内部
        left_min = max(0, cur - k + 1)      # 子数组左端点的最小合法值
        left_max = min(cur, n - k)          # 子数组左端点的最大合法值
        for l in range(left_min, left_max + 1):
            new = 2 * l + k - 1 - cur       # 翻转后 1 的新位置
            if new in visited:             # 已访问或被禁，直接跳过
                continue
            visited.add(new)
            ans[new] = ans[cur] + 1         # 步数+1
            q.append(new)

    return ans
```

> **关键行中文注释**已经写在代码里，帮助你快速定位每一步的意义。

#### 复杂度

- **时间复杂度**：  
  对每个被访问的格子 `cur`，我们要遍历所有可能的左端点 `l`，数量最多是 `k`。最坏情况下会访问 `n` 个格子，故总体是 **`O(n·k)`**。如果 `k` 接近 `n`，这会达到 `10^10` 级别，远远超出限制。  
  > 大白话：想象每走一步都要把整条街的每家店都跑一遍，街很长（`n`）店也很多（`k`），自然慢。

- **空间复杂度**：  
  需要存 `ans`、`visited`、队列等，都是 **`O(n)`**。  
  > 大白话：只要把每个格子的信息记下来，空间就跟格子数成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都枚举所有左端点 `l`**，导致 `O(k)` 的额外因子。我们需要**一次性把同一层所有可以到达的格子算出来**，而不是逐个枚举。

观察翻转的数学规律：

1. 设子数组左端点为 `l`，长度为 `k`，则右端点是 `r = l + k – 1`。  
2. `cur` 位于 `[l, r]` 之间，翻转后它会落到对称位置  
   ```
   new = l + (r - cur) = 2*l + k - 1 - cur
   ```
3. 当 `l` 从 `left_min` 增加到 `left_max` 时，`new` 也会 **等差递增**，增量恰好是 **2**（因为 `new` 随 `l` 线性变化，系数为 2）。  
   换句话说，**从 `cur` 能到达的所有位置组成一个等差数列**，公差是 `2`，且所有位置的 **奇偶性**（parity）是固定的。

   - 当 `k` 为奇数，`k-1` 为偶数，`new = cur + (k-1) - 2*offset`，这里的 `offset` 为 `cur - l`，所以 `new` 与 `cur` 同奇偶。  
   - 当 `k` 为偶数，`k-1` 为奇数，`new` 与 `cur` **相反**奇偶。

4. 因此，从 `cur` 能到达的格子 **只在一个连续区间 `[low, high]` 内**，并且只保留与 `cur`（或相反）奇偶相同的格子。  

   - `low = max(cur - (k-1), 0)`  
   - `high = min(cur + (k-1), n-1)`  

   这两个端点已经把 “子数组必须完全在数组内部” 的限制考虑进来了。

5. 为了在 **`O(log n)`** 时间内找出区间内未访问且未被禁的格子，我们使用 **有序集合（Ordered Set）**。在 Python 中可以用 **`bisect`** 在一个排好序的列表里快速定位区间的起始下标，然后一次性弹出所有满足条件的元素。

   - 我们把所有未被禁且未访问的奇数位置放在 `odd = sorted([...])`，偶数位置放在 `even = sorted([...])`。  
   - 在 BFS 中处理 `cur` 时，根据 `k` 的奇偶决定我们要查询 `odd` 还是 `even`（即奇偶相同或相反的集合）。  
   - 用 `bisect_left` 找到 `low` 在集合中的第一个位置，用循环向右遍历直到超过 `high`，每访问一个位置就把它从集合中删除（`pop(idx)`），并加入 BFS 队列。

这样，每个格子只会被弹出一次，整个过程的时间复杂度降到 **`O(n log n)`**（`log n` 来自二分查找），空间仍是 **`O(n)`**。

> **类比**：把所有格子想象成排好队的学生，奇数站在左侧，偶数站在右侧。老师（BFS）一次只能叫出一段连续的学生（区间），并且只能叫出奇数或偶数。用二分快速定位这段学生的起点，然后把他们一个一个叫走（弹出），再继续下一轮。

#### 代码（Python）

```python
import bisect
from collections import deque
from typing import List

def minimum_reverse_operations(n: int, p: int, banned: List[int], k: int) -> List[int]:
    # ---------- 初始化 ----------
    ans = [-1] * n                     # 最终答案
    ans[p] = 0                         # 起点距离 0

    # 把禁止位置和已经访问的位置都从集合里移除
    banned_set = set(banned)

    # 按奇偶划分的有序集合（用列表 + bisect 实现）
    even = [i for i in range(0, n, 2) if i not in banned_set and i != p]
    odd  = [i for i in range(1, n, 2) if i not in banned_set and i != p]

    # BFS 队列，存 (当前位置, 已使用的步数)
    q = deque([p])

    while q:
        cur = q.popleft()
        cur_dist = ans[cur]

        # 能到达的最左、最右位置（已经把子数组必须完整放进数组的限制考虑进去）
        low  = max(cur - (k - 1), 0)
        high = min(cur + (k - 1), n - 1)

        # 根据 k 的奇偶决定要在奇数集合还是偶数集合中搜索
        # 若 k 为奇数：new 与 cur 同奇偶；若 k 为偶数：new 与 cur 奇偶相反
        if k % 2 == 1:                     # k 为奇数，奇偶不变
            target = even if cur % 2 == 0 else odd
        else:                              # k 为偶数，奇偶翻转
            target = odd if cur % 2 == 0 else even

        # 用二分找到第一个 >= low 的下标
        idx = bisect.bisect_left(target, low)

        # 从 idx 开始遍历，只要位置 <= high 就是本层可达的格子
        while idx < len(target) and target[idx] <= high:
            nxt = target[idx]               # 真实的下一个位置
            ans[nxt] = cur_dist + 1         # 距离+1
            q.append(nxt)                   # 加入 BFS

            # 删除已访问的元素：pop 会把列表右移，保持有序
            target.pop(idx)                 # 删除后下一个元素仍在同 idx 位置
            # 注意：不要 idx+=1，因为 pop 后的下一个元素已经占到了 idx

    return ans
```

**代码要点解释（中文注释已在代码中）**：

- **`even / odd` 列表**：把所有「可以踩」的格子事先分类，类似字典里把单词分成两本（奇数本、偶数本），查询时只打开对应的一本。
- **`bisect_left`**：在有序列表里快速定位区间左端点，时间是 `O(log n)`，相当于在字典里查第一个以某字母开头的单词。
- **`while` 循环弹出**：一次把区间 `[low, high]` 内的所有合法格子弹出，保证每个格子只被处理一次，整体是 `O(n log n)`。
- **奇偶切换**：`k` 为奇数时奇偶不变，`k` 为偶数时奇偶翻转，这一步把「只能在奇数本里找」或「只能在偶数本里找」的规则实现出来。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 每个格子最多被弹出一次（`O(1)`），弹出前需要一次二分定位（`O(log n)`）。  
  - 与暴力解的 `O(n·k)` 相比，**把一次遍历 `k` 的代价降到了对数级**，即使 `k` 接近 `n` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 需要存 `ans`、两个有序集合以及 BFS 队列，都是和格子数量线性相关的。

> **对比**：暴力解像是“每走一步都把整条街的每家店都跑一遍”，最优解则是“一次把整条街里符合条件的店一次性叫走”，省时省力。

---

## 心得

- **核心技巧**：利用**翻转后位置的等差性质**，把一次操作的所有可能结果压缩为「同奇偶的连续区间」并用**有序集合 + 二分**一次性取出。  
- **适用的题型**  
  1. **区间翻转/移动**，如「翻转子数组后最短路径」系列。  
  2. **只能在奇偶或模 `m` 同余的格子间跳跃**，比如「跳跃游戏」的变种。  
  3. **需要频繁在区间内删除元素** 的 BFS/DFS 场景，如「最小步数到达目标」的「有序集合」版。  
- **一句话总结解题钥匙**：**把所有可达位置归纳为等差区间，用有序集合一次性抽取**。

---

## 反思

- **第一反应**：看到“翻转子数组”，立刻想到**枚举所有左端点**，于是写出了暴力 BFS。  
- **最容易踩的坑**  
  1. **子数组越界**：左端点 `l` 必须满足 `0 ≤ l ≤ n‑k`，否则翻转会超出数组。  
  2. **奇偶限制**：忽略 `k` 奇偶导致的奇偶不变/翻转，会把不合法的格子也加入答案，导致错误。  
  3. **删除已访问元素时的下标错误**：在列表中 `pop(idx)` 后，后面的元素会左移，循环中 **不要再 `idx += 1`**。  
- **下次类似题的第一步**：先**写出位置变化的公式**，看是否可以化简成等差或等比的结构；如果可以，就考虑用**有序集合**一次性处理区间，而不是逐个枚举。