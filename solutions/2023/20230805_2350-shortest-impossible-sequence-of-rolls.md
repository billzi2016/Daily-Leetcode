# #2350. 最短不可实现的投掷序列 / Shortest Impossible Sequence of Rolls

> 难度：困难 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/shortest-impossible-sequence-of-rolls/)

---

## 题目（英文原版）

**Description**

You are given an integer array rolls of length n and an integer k. You roll a k sided dice numbered from 1 to k, n times, where the result of the ith roll is rolls[i].
Return the length of the shortest sequence of rolls so that there's no such subsequence in rolls.
A sequence of rolls of length len is the result of rolling a k sided dice len times.

**Examples**

**Example 1:**

```
Input: rolls = [4,2,1,2,3,3,2,4,1], k = 4
Output: 3
Explanation: Every sequence of rolls of length 1, [1], [2], [3], [4], can be taken from rolls.
Every sequence of rolls of length 2, [1, 1], [1, 2], ..., [4, 4], can be taken from rolls.
The sequence [1, 4, 2] cannot be taken from rolls, so we return 3.
Note that there are other sequences that cannot be taken from rolls.
```

**Example 2:**

```
Input: rolls = [1,1,2,2], k = 2
Output: 2
Explanation: Every sequence of rolls of length 1, [1], [2], can be taken from rolls.
The sequence [2, 1] cannot be taken from rolls, so we return 2.
Note that there are other sequences that cannot be taken from rolls but [2, 1] is the shortest.
```

**Example 3:**

```
Input: rolls = [1,1,3,2,2,2,3,3], k = 4
Output: 1
Explanation: The sequence [4] cannot be taken from rolls, so we return 1.
Note that there are other sequences that cannot be taken from rolls but [4] is the shortest.
```

**Constraints**

- n == rolls.length
- 1 <= n <= 105
- 1 <= rolls[i] <= k <= 105

---

## 题目（中文翻译）

你得到一个长度为 `n` 的整数数组 `rolls` 和一个整数 `k`。你会掷一颗编号为 `1` 到 `k` 的 `k` 面骰子（k‑sided dice）共 `n` 次，第 `i` 次掷出的结果为 `rolls[i]`。  

返回 **最短不可实现的投掷序列** 的长度，即不存在于 `rolls` 中的最短子序列（subsequence）长度。  
投掷序列（sequence of rolls）指的是掷 `k` 面骰子若干次得到的结果序列，其长度为 `len` 表示掷了 `len` 次。

**示例 1**  

**示例 2**  

**示例 3**  

**约束条件**

- `n == rolls.length`
- `1 <= n <= 10^5`
- `1 <= rolls[i] <= k <= 10^5`

**示例**

**示例 1:**  
输入: `rolls = [4,2,1,2,3,3,2,4,1]`, `k = 4`  
输出: `3`  
解释: 长度为 `1` 的所有投掷序列 `[1]`, `[2]`, `[3]`, `[4]` 都可以在 `rolls` 中找到。  
长度为 `2` 的所有投掷序列 `[1,1]`, `[1,2]`, …, `[4,4]` 也都可以在 `rolls` 中找到。  
序列 `[1,4,2]` 无法在 `rolls` 中出现，因此返回 `3`。注意还有其他序列也无法出现，但 `[1,4,2]` 是最短的之一。

**示例 2:**  
输入: `rolls = [1,1,2,2]`, `k = 2`  
输出: `2`  
解释: 长度为 `1` 的所有投掷序列 `[1]`, `[2]` 都可以在 `rolls` 中找到。  
序列 `[2,1]` 无法在 `rolls` 中出现，因此返回 `2`。还有其他不可出现的序列，但 `[2,1]` 是最短的。

**示例 3:**  
输入: `rolls = [1,1,3,2,2,2,3,3]`, `k = 4`  
输出: `1`  
解释: 序列 `[4]` 无法在 `rolls` 中出现，因此返回 `1`。虽然还有其他不可出现的序列，但 `[4]` 是最短的。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的序列都枚举一遍**，检查每个序列是否能在 `rolls` 中找到对应的子序列（subsequence）。  
- **子序列**：可以把 `rolls` 看成一串字符，我们可以随意跳过中间的字符，只要保持顺序不变，就算找到了子序列。  
- **所有可能的序列**：长度为 `len` 的序列一共有 `k^len` 种（因为每个位置可以是 `1 … k` 中的任意一个），这跟 **哈希表** 类似：把每一种序列当成 “词”，把它是否出现当成 “页码”。  

如果我们把所有 `k^len` 种序列都检查一遍，一旦发现有一种找不到，就可以返回当前的 `len`。  

> **为什么暴力一定能得到正确答案？**  
> 因为我们枚举了**全部**可能的序列，必然会包含第一条“不可出现”的序列，找到它的长度自然就是答案。

> **时间/空间分析（大白话版）**  
> - 时间复杂度：`O(k^len * n)`  
>   - `k^len` 表示我们要检查多少种序列。  
>   - 对每一种序列，我们在 `rolls` 中线性扫描一次（最坏情况要走完整个数组 `n`），所以乘在一起。  
>   - 当 `k = 2, len = 20` 时，`k^len = 1,048,576`，已经远远超过题目给的上限 `10^5`，根本跑不完。  
> - 空间复杂度：`O(1)`（只用常数级别的额外变量）。

显然，这个办法在 **数据量稍大** 时就会爆炸，不能直接使用。

#### 代码（Python）

```python
from itertools import product

def shortest_impossible_bruteforce(rolls, k):
    n = len(rolls)
    # 暴力检查长度从 1 开始递增
    length = 1
    while True:
        # 产生所有可能的序列，使用 product 生成笛卡尔积
        for seq in product(range(1, k + 1), repeat=length):
            # 检查 seq 是否是 rolls 的子序列
            i = 0                 # rolls 的指针
            for num in seq:       # seq 的每个字符依次匹配
                while i < n and rolls[i] != num:
                    i += 1
                if i == n:        # 已经遍历完 rolls 仍未匹配成功
                    return length
                i += 1             # 匹配成功，继续向后找下一个字符
        length += 1                # 所有长度为 length 的序列都能匹配，继续尝试更长的
```

> 代码里每一行都写了中文注释，帮助你快速定位每一步的意义。  

#### 复杂度  

- **时间复杂度**：`O(k^len * n)`  
  - `k^len` 是序列的总数，`n` 是每次检查子序列时最坏需要遍历的长度。  
  - 对于稍大的 `k` 或 `len`，这个乘积会非常大，实际运行会超时。  
- **空间复杂度**：`O(1)`  
  - 只使用了几个整数指针和循环变量，没有额外的数组或哈希表。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有可能的序列**。  
观察题目：我们只需要找出 **第一条找不到的序列**，而不是列举全部。  
从 **长度 1** 开始逐层检查：

1. **长度 1**  
   - 只要 `rolls` 中出现了 `1…k` 中的每一个数字，就说明所有长度为 1 的序列都可以取到。  
   - 若有数字根本没出现，答案立刻是 `1`。  

2. **长度 2**  
   - 对于任意首位 `a (1…k)`，我们必须能够在它之后再找到 **任意** 的第二个数字 `b`。  
   - 换句话说：**在每个数字的第一次出现之后，后面的子数组必须已经包含了全部 `1…k`**。  
   - 只要找不到这样的位置（即某个数字的第一次出现后面缺少某个数字），答案就是 `2`。  

3. **长度 3、4 …**  
   - 继续类推：  
     - 先把所有 **长度为 (len‑1) 的合法前缀** 看成 “起点”。  
     - 对每个起点，检查在它之后是否还能找到 **所有** `k` 种数字。  
     - 如果对 **所有** 起点都能找到，则长度 `len` 的所有序列都可以取到；否则答案就是 `len`。  

关键在于 **“最坏的起点”**。  
- 对于某一层 `len`，所有合法前缀中，**最靠后的那个起点**决定了我们能否继续向下。  
- 因为只要有一个前缀把我们逼得太靠后，后面就可能缺少某些数字。  

**如何快速得到最靠后的起点？**  

对每个数字 `v`，记它在 `rolls` 中出现的位置列表 `pos[v]`（从左到右递增）。  
在遍历层数时，我们维护一个指针 `ptr[v]`，指向 `pos[v]` 中 **第一个大于当前起点** 的位置。  

- 若 `ptr[v]` 已经越界，说明在当前起点之后再也找不到 `v`，此时答案就是当前层 `len`。  
- 否则，`pos[v][ptr[v]]` 就是 **在当前起点之后** 能够匹配到 `v` 的最近位置。  

把所有 `v` 的这些最近位置取最大值 `max_next`，这就是**最靠后的合法起点**（因为要兼容所有 `v`，我们必须走到最远的那个位置）。  
然后把起点更新为 `max_next`，层数加一，继续下一轮。

**为什么这样是最优的？**  

- 每一次循环我们只遍历一次 `rolls`（每个位置最多被各自的指针扫过一次），所以总时间是 `O(n)`。  
- 只用了 `pos`（总长度等于 `n`）和指针数组 `ptr`（长度 `k`），空间是 `O(n + k)`。  
- 由于每一步都在“最坏的前缀”上取最大位置，**只要还有一次完整的循环，就说明所有长度为当前层的序列都可以构造**。一旦循环失败，得到的层数恰好是**最短的不可构造序列长度**。

> **核心算法**：  
> 1. 统计每个数字的出现位置（哈希表 / 列表）。  
> 2. 检查是否有数字根本不存在 → `return 1`。  
> 3. `cur = -1`（当前已匹配的最后位置），`ans = 0`。  
> 4. 循环：  
>    - 对每个 `v = 1 … k`  
>        - 使用二分搜索（`bisect_right`）在 `pos[v]` 中找第一个 > `cur` 的位置。  
>        - 若找不到 → `return ans + 1`（长度 `ans+1` 的序列不可得）。  
>        - 记录该位置的最大值 `max_next`。  
>    - `cur = max_next`，`ans += 1`，继续。  

因为 `ans` 最多只会增长到 **约 20**（在最极端的 `k = 2` 情况下），整体运行时间远在限制之内。

#### 代码（Python）

```python
from bisect import bisect_right
from collections import defaultdict

def shortestImpossibleSequence(rolls, k):
    """
    返回最短的、在 rolls 中找不到的掷骰子序列长度
    思路：逐层检查，每层只保留“在当前起点之后，各数字最近出现的位置”，
          取这些位置的最大值作为下一层的起点。如果某个数字已经没有
          出现位置，则当前层+1 即为答案。
    """
    n = len(rolls)

    # 1️⃣ 统计每个数字出现的下标列表（下标从 0 开始）
    pos = defaultdict(list)          # pos[v] = [i1, i2, ...]（升序）
    for idx, val in enumerate(rolls):
        pos[val].append(idx)

    # 2️⃣ 若有数字根本未出现，答案就是 1
    for v in range(1, k + 1):
        if not pos[v]:               # 空列表说明该数字从未出现
            return 1

    cur = -1          # 已经匹配的最后一个位置，-1 表示“在最左侧”
    ans = 0           # 已经成功构造的序列长度

    while True:
        max_next = -1   # 本层所有数字最近出现位置的最大值

        # 3️⃣ 对每个可能的数字，找出它在 cur 之后的第一个出现位置
        for v in range(1, k + 1):
            # 使用二分查找，第一个大于 cur 的下标
            i = bisect_right(pos[v], cur)
            if i == len(pos[v]):      # 已经没有位置可以继续匹配 v
                return ans + 1        # 当前层的序列已经构造不出来
            nxt = pos[v][i]           # v 在 cur 之后最近的出现位置
            if nxt > max_next:
                max_next = nxt

        # 4️⃣ 所有数字都能在 max_next 之前出现，说明本层长度 ans+1 的
        #    所有序列都可以构造。继续向下一层尝试。
        cur = max_next
        ans += 1
```

**代码要点注释**（已在代码中给出）：

- `defaultdict(list)` 类比 **字典里的词典**，每个数字对应一个“出现页码列表”。  
- `bisect_right` 相当于 **在有序目录里快速定位**，时间是 `O(log m)`（`m` 为该数字出现次数）。  
- `max_next` 就是 **最靠后的合法起点**，只有它足够靠后，所有数字才能在它之后各自出现一次。  

#### 复杂度  

- **时间复杂度**：`O(answer * k * log average_occurrence)`  
  - `answer` 为最终返回的长度，实际在题目限制下最多约 20（因为 `k^answer` 很快超过所有可能的子序列数）。  
  - 每一层遍历全部 `k` 个数字，二分查找每次 `O(log occurrence)`，`occurrence` 平均约 `n/k`。  
  - 整体远小于 `10^6` 次基本运算，轻松通过 1 s 限制。  
- **空间复杂度**：`O(n + k)`  
  - `pos` 保存所有出现位置，总数恰好是 `n`。  
  - 额外的指针、变量只占 `O(k)`。

---

## 心得  

- **核心技巧**：**把“所有可能的序列”转化为“每个数字最近出现的位置”，并只关注最靠后的那个位置**。这是一种**贪心 + 二分**的思路。  
- **适用场景**：  
  1. **最短不可出现子序列**（Shortest Absent Subsequence）问题。  
  2. **判断所有长度为 L 的子序列是否齐全**的场景，例如 “给定字符序列，最短缺失的长度”。  
  3. **基于字典序的序列覆盖**问题，如 “最短无法覆盖的密码”。  
- **一句话总结**：*把每一次“最坏的起点”往右推进，直到某个字符再也找不到为止，推进的次数就是答案。*

---

## 反思  

- **第一反应**：立刻想到枚举所有 `k^len` 种序列，写出暴力检查。  
- **最容易踩的坑**：  
  - 忘记检查 **单个数字是否出现**，导致在 `len = 1` 时直接崩溃。  
  - 在实现贪心时，只比较**最大**出现位置，却忽略了**有的数字已经在当前起点之后找不到**的情况（如示例 2），会导致错误的结果。  
  - 二分查找时使用了错误的左/右界，导致无限循环。  
- **下次类似题目第一步**：先判断 **“长度 1 是否缺失”**，再把 **“每个字符的下一次出现位置”** 建成列表，准备好 **二分定位**，然后按照“最靠后起点”逐层推进。这样可以避免盲目枚举，直接走向最优解。