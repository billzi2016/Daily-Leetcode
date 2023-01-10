# #2086. 喂养仓鼠所需的最少食物桶数量 / Minimum Number of Food Buckets to Feed the Hamsters

> 难度：中等 · 标签：String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-food-buckets-to-feed-the-hamsters/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string hamsters where hamsters[i] is either:
You will add some number of food buckets at the empty indices in order to feed the hamsters. A hamster can be fed if there is at least one food bucket to its left or to its right. More formally, a hamster at index i can be fed if you place a food bucket at index i - 1 and/or at index i + 1.
Return the minimum number of food buckets you should place at empty indices to feed all the hamsters or -1 if it is impossible to feed all of them.

**Examples**

**Example 1:**

```
Input: hamsters = "H..H"
Output: 2
Explanation: We place two food buckets at indices 1 and 2.
It can be shown that if we place only one food bucket, one of the hamsters will not be fed.
```

**Example 2:**

```
Input: hamsters = ".H.H."
Output: 1
Explanation: We place one food bucket at index 2.
```

**Example 3:**

```
Input: hamsters = ".HHH."
Output: -1
Explanation: If we place a food bucket at every empty index as shown, the hamster at index 2 will not be able to eat.
```

**Constraints**

- 1 <= hamsters.length <= 105
- hamsters[i] is either'H' or '.'.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串 `hamsters`，其中 `hamsters[i]` 只能是 `'H'`（仓鼠）或 `'.'`（空位）。  
你可以在空位上放置若干食物桶（food bucket）。如果某只仓鼠左侧或右侧（即下标 `i-1` 或 `i+1`）至少有一个食物桶，则该仓鼠可以进食。  
返回为使所有仓鼠都能进食而需要放置的最少食物桶数量；如果无法让所有仓鼠进食，返回 `-1`。

**示例**  

示例 1  
```
Input: hamsters = "H..H"
Output: 2
Explanation: 我们在下标 1 和 2 处各放置一个食物桶。
可以证明，只放置一个食物桶的话，必有一只仓鼠得不到食物。
```

示例 2  
```
Input: hamsters = ".H.H."
Output: 1
Explanation: 我们在下标 2 处放置一个食物桶。
```

示例 3  
```
Input: hamsters = ".HHH."
Output: -1
Explanation: 即使在所有空位上都放置食物桶，位于下标 2 的仓鼠仍然无法进食。
```

**约束条件**  
- `1 <= hamsters.length <= 10^5`  
- `hamsters[i]` 只能是 `'H'` 或 `'.'`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有可以放食物桶的位置（即字符 `'.'`）全部列举出来，然后**枚举**每一种放置或不放置的组合，检查每种组合是否能让所有仓鼠都有左侧或右侧的桶。  

- **数据结构**：  
  - 用一个列表 `empty_idx` 保存所有空位的下标，类似把字典的“词表”收集起来，只是这里的“词”是位置。  
  - 用二进制掩码（`mask`）来表示一种放置方案：第 `k` 位是 1 表示在 `empty_idx[k]` 放桶，0 表示不放。  

- **为什么正确**：  
  枚举了**所有**可能的放置方式，只要有一种满足条件，就能得到答案。因为我们检查了每一种情况，必然不会漏掉最优解（即最少桶数的那种组合）。  

- **时间/空间复杂度**：  
  - 空位的个数记为 `m`，则一共有 `2^m` 种放置方式。对每一种方式我们要遍历整个字符串检查是否所有仓鼠都被喂到。  
  - **时间复杂度**：`O( 2^m * n )`，其中 `n` 是字符串长度。对大多数输入（`n` 可达 10⁵）来说，这几乎是不可能完成的任务。  
  - **空间复杂度**：`O(m)` 用来存放空位下标，最多和 `n` 同阶。  

> **大白话**：  
> “指数级”`2^m` 就像每次把钱翻倍一样，几秒钟能做到的事，放到 30 个空位后就需要几千万年的计算时间了。  

#### 代码（Python）  

```python
from itertools import product
from typing import List

def min_buckets_bruteforce(hamsters: str) -> int:
    n = len(hamsters)
    empty_idx: List[int] = [i for i, ch in enumerate(hamsters) if ch == '.']

    # m 为空位数量
    m = len(empty_idx)
    best = float('inf')                     # 记录最少桶数

    # 逐一枚举 0/1 的组合（相当于二进制掩码）
    for mask in range(1 << m):               # 0 ~ 2^m-1
        # 生成当前放置方案对应的集合，便于 O(1) 查询
        bucket = set()
        for k in range(m):
            if mask >> k & 1:                # 第 k 位为 1 → 放桶
                bucket.add(empty_idx[k])

        # 检查所有仓鼠是否都有左或右相邻的桶
        ok = True
        for i, ch in enumerate(hamsters):
            if ch == 'H':
                if (i - 1 not in bucket) and (i + 1 not in bucket):
                    ok = False
                    break
        if ok:
            best = min(best, len(bucket))

    return -1 if best == float('inf') else best
```

> 这段代码只适合 **非常小** 的输入（比如 `len(hamsters) ≤ 12`），用来帮助大家理解最朴素的思路。  

#### 复杂度  

- **时间复杂度**：`O(2^m * n)`，指数级增长，几乎不可接受。  
- **空间复杂度**：`O(m)`，只存放空位下标。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**枚举所有可能**显然太慢。我们要找出 **决定桶放在哪里的关键规则**，从而一次遍历就能得到答案。  

1. **瓶颈在哪里？**  
   - 暴力解的慢点在于“尝试所有组合”。实际上，**每只仓鼠只需要一个相邻的空位**，而且**我们可以贪心地决定把桶放在右边**（如果右边有空位），因为右边的桶还有可能帮助后面的仓鼠。  

2. **关键观察**  
   - 当我们从左到右扫描字符串时，**已经处理过的仓鼠一定已经被喂到**（我们会确保这一点）。  
   - 对于当前位置 `i`，如果 `hamsters[i] == 'H'`：  
     - **优先把桶放在 `i+1`**（右侧），前提是 `i+1` 在范围内且是 `'.'`。这样可以同时喂到后面的仓鼠，最大化利用。  
     - 如果右侧不可用（超界或已经是 `'H'`），只能把桶放在左侧 `i-1`（此时左侧必然是 `'.'`，因为如果左侧是 `'H'` 那么这只仓鼠根本没有空位，题目直接返回 `-1`）。  
     - 如果左、右都不可用，则**无法喂到这只仓鼠**，直接返回 `-1`。  

3. **为什么贪心有效？**  
   - 把桶放在右侧不会影响已经喂好的左侧仓鼠（它们已经有左/右桶），而只会帮助**后面的**仓鼠。  
   - 如果我们把桶放在左侧，可能浪费了一个本可以喂到右侧仓鼠的机会，导致后面出现 “两只相邻的仓鼠中间没有空位” 的不可喂情况。  
   - 因此**始终把桶放在右侧**是最安全、最省桶的策略。  

4. **实现细节**  
   - 用一个字符列表 `s = list(hamsters)` 便于原地修改（把放好的桶记作 `'B'`）。  
   - 维护计数器 `ans` 记录放了多少桶。  
   - 按下标 `i` 从 `0` 到 `n-1` 遍历：  
     - 若 `s[i] == 'H'`，检查 `i+1`、`i-1` 两侧。  
     - 按上面的规则放桶并更新 `ans`。  
   - 最终返回 `ans`（若中途返回 `-1` 则表示不可能）。  

5. **类比**  
   - 想象你在给排队的孩子发糖果，**只允许在空位放糖**。如果左边的孩子已经拿到糖，你应该把糖放在右边的空位，这样可以一次喂到后面排队的孩子，减少糖的浪费。  

#### 代码（Python）  

```python
def min_buckets_greedy(hamsters: str) -> int:
    """
    贪心扫描，时间 O(n)，空间 O(1)
    """
    s = list(hamsters)          # 方便修改字符
    n = len(s)
    ans = 0                     # 已放的桶数

    i = 0
    while i < n:
        if s[i] == 'H':         # 遇到仓鼠
            # 情况 1：右侧有空位，可以放桶
            if i + 1 < n and s[i + 1] == '.':
                s[i + 1] = 'B'  # 标记为已经放桶
                ans += 1
                # 右侧放桶后，当前仓鼠已经被喂到，直接跳过右侧的空位
                i += 2          # 因为 i+1 已经是桶，i+2 可能是下一个仓鼠
                continue
            # 情况 2：右侧不可放，左侧必须有空位
            if i - 1 >= 0 and s[i - 1] == '.':
                s[i - 1] = 'B'
                ans += 1
                # 左侧放桶后，当前仓鼠已经喂到，继续检查下一个位置
                i += 1
                continue
            # 两侧都没有空位 → 不可能喂到
            return -1
        # 当前不是仓鼠，直接往后走
        i += 1

    return ans
```

> 代码里每一行都写了中文注释，帮助你一步步跟上思路。  

#### 复杂度  

- **时间复杂度**：`O(n)`。我们只遍历一次字符串，**n** 最高是 10⁵，在 1 秒左右即可完成。  
  - 与暴力解的 `O(2^m * n)` 相比，指数级的爆炸被降到了线性，快了几万倍甚至更多。  
- **空间复杂度**：`O(1)`（不计输入本身）。只用了几个整数和一个可以原地修改的字符数组。  

---

## 心得  

- **核心技巧**：**贪心**——在满足当前需求的前提下，尽可能把资源（食物桶）放在对后续最有帮助的位置（右侧）。  
- **适用的题型**：  
  1. “最少灯泡点亮走廊”类问题（如 LeetCode 1991 `Find the Minimum Number of Operations to Make Array Sorted` 中的类似贪心思路）。  
  2. “覆盖区间”类问题（如放置摄像头、炸弹等，需要覆盖所有目标且每次尽量向右扩展）。  
  3. “相邻元素配对”类（如 `Minimum Number of Moves to Make Palindrome` 中的左右配对）。  
- **一句话总结解题钥匙**：**总是把资源放在右侧空位，因为它能兼顾当前和后面的需求。**  

---

## 反思  

- **拿到题目第一反应**：先想“遍历所有空位的子集”，因为我习惯先用暴力验证可行性。  
- **最容易踩的坑**：  
  - 忽略两只相邻仓鼠 `HH` 的情况，这直接导致答案是 `-1`。  
  - 边界条件：仓鼠在最左或最右端时，只能检查单侧空位。  
  - 在实现贪心时，忘记在放桶后**跳过已经处理的空位**，可能导致重复计数或错误判断。  
- **下次遇到同类题**：第一步先**判断是否有“无空位的孤立仓鼠”**（即出现 `HH` 或 `H` 在两端且相邻不是 `.`），若有直接返回 `-1`；否则就**从左到右、优先在右侧放资源**。