# #846. 顺子 / Hand of Straights

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/hand-of-straights/)

---

## 题目（英文原版）

**Description**

Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size groupSize, and consists of groupSize consecutive cards.
Given an integer array hand where hand[i] is the value written on the ith card and an integer groupSize, return true if she can rearrange the cards, or false otherwise.
Note: This question is the same as 1296: https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/

**Examples**

**Example 1:**

```
Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
Output: true
Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]
```

**Example 2:**

```
Input: hand = [1,2,3,4,5], groupSize = 4
Output: false
Explanation: Alice's hand can not be rearranged into groups of 4.
```

**Constraints**

- 1 <= hand.length <= 104
- 0 <= hand[i] <= 109
- 1 <= groupSize <= hand.length

---

## 题目（中文翻译）

Alice 有若干张牌，她想把这些牌重新排列成若干组，使得每一组的大小为 **groupSize**，且每组内的牌是 **groupSize** 个连续的卡牌。

给定一个整数数组 **hand**，其中 `hand[i]` 表示第 *i* 张牌上的数值，以及一个整数 **groupSize**，如果可以将牌重新排列满足上述要求返回 `true`，否则返回 `false`。

> **注意**：本题与 1296 题相同：https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/

### 示例

**示例 1**  
Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3  
Output: true  
Explanation: Alice 的手牌可以重新排列为 `[1,2,3]`, `[2,3,4]`, `[6,7,8]`。

**示例 2**  
Input: hand = [1,2,3,4,5], groupSize = 4  
Output: false  
Explanation: Alice 的手牌无法重新排列成大小为 4 的连续组。

### 约束条件

- `1 <= hand.length <= 10^4`
- `0 <= hand[i] <= 10^9`
- `1 <= groupSize <= hand.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的分组方式**，只要找到一种能够把手里的牌全部划分成长度为 `groupSize`、且每组内部是连续整数的子数组，就返回 `true`。  
实现上可以：

1. 先把牌按 **从小到大** 排序（这样更容易判断“连续”）。  
2. 用递归（或回溯）把第一张牌放进一个新组，然后尝试把后面的 `groupSize‑1` 张连续的牌也放进同一个组。  
3. 把已经使用的牌标记为“已取走”，递归处理剩余的牌。  
4. 若递归走到所有牌都被使用，说明成功；若在某一步找不到连续的 `groupSize‑1` 张牌，就回溯，尝试别的组合。

> **类比**：把手里的牌想象成一堆拼图块，目标是把它们拼成若干条连续的“小河”。暴力解法相当于把每一块都尝试放进每一条河里，哪怕已经尝试过很多次也不放弃。

**为什么这个方法正确**  
递归会遍历 **所有** 合法的分组方式，只要有一种方式可以把所有牌分完，递归必然会找到。因此，只要返回 `true`，一定是可行的；若所有路径都走不通，则返回 `false`，说明根本不存在合法划分。

**时间/空间复杂度**  
- 时间复杂度：`O( (n/groupSize)! )`（阶乘级）——每次都要挑选 `groupSize` 张连续的牌，搜索树的分支数随牌数指数增长。对 10⁴ 张牌来说几乎不可接受。  
- 空间复杂度：`O(n)`——递归栈最多保存 `n/groupSize` 层，每层需要记录已经使用的牌。

> **大白话**：`O(n²)` 表示“和 n 乘以 n 差不多”，而这里的阶乘 `!` 更糟，意思是“每增加一张牌，可能的组合会翻几倍”。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canArrange_bruteforce(hand: List[int], groupSize: int) -> bool:
    # 1. 先排序，方便后面判断连续性
    hand.sort()
    n = len(hand)

    # 2. 用 Counter 记录每张牌还剩多少张（相当于“是否被用过”）
    cnt = Counter(hand)

    # 3. 递归函数：尝试把剩余的牌全部划分完
    def backtrack(remaining: int) -> bool:
        # remaining 表示还有多少张牌未分组
        if remaining == 0:                 # 所有牌都用完了
            return True

        # 取当前最小的还未使用的牌作为新组的起点
        start = min(k for k, v in cnt.items() if v > 0)

        # 试图把 start, start+1, …, start+groupSize-1 都取走
        for i in range(start, start + groupSize):
            if cnt[i] == 0:                # 中途断了，说明这条路不通
                return False
            cnt[i] -= 1                    # 把这张牌标记为已使用

        # 成功取走一整组，继续递归处理剩余的牌
        if backtrack(remaining - groupSize):
            return True

        # ------------------ 回溯 ------------------
        # 上面递归返回 False，说明这条分组方式行不通，需要恢复现场
        for i in range(start, start + groupSize):
            cnt[i] += 1                    # 把牌放回去

        return False

    # 先检查能否被 groupSize 整除，不能整除直接 false
    if n % groupSize != 0:
        return False

    return backtrack(n)
```

#### 复杂度

- **时间复杂度**：`O( (n/groupSize)! )`（指数/阶乘级），因为递归会尝试所有可能的分组组合。  
- **空间复杂度**：`O(n)`，主要是 `Counter` 保存每张牌的计数以及递归栈的深度。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于大量的回溯和重复检查。  
观察题目可以得到两个关键点：

1. **每次都应该从当前最小的未使用牌开始**。因为如果最小的牌不参与某个完整的连续序列，那么它永远也无法被使用（没有更小的牌可以“填补”它的缺口）。
2. **只要能够把最小牌所在的那一组完整取走，后面的牌顺序不会受影响**。因此我们可以一次性“贪心”地把这组牌删掉，而不必回溯。

基于这两个点，**贪心 + 哈希表**（计数）即可得到线性或 `O(n log n)` 的解法：

1. **计数**：使用 `collections.Counter` 统计每个数出现的次数。把它想象成一本“字典”，键是牌的点数，值是这张牌还有几张剩余。
2. **排序**：把所有不同的牌点数从小到大排好序（相当于把字典的“页码”从前往后翻）。
3. **遍历**：从最小的点数 `x` 开始，如果 `cnt[x]` 为 0，说明这张牌已经在之前的组里用了，直接跳过。否则，说明我们需要以 `x` 为起点，构造一组 `groupSize` 连续的牌。
   - 设 `need = cnt[x]` 为当前最小牌需要被使用的次数（因为可能有多张相同的最小牌）。
   - 对 `i = x, x+1, …, x+groupSize-1`，把 `cnt[i]` 减去 `need`。如果出现 `cnt[i] < 0`，说明在这段连续区间里某个数字不够用，直接返回 `False`。
4. **全部遍历结束**，没有出现负数，说明每张牌都成功被分配进了合法的组，返回 `True`。

> **类比**：把手里的牌想成一排排超市货架，`cnt` 是每种商品的库存。我们每次从最左边的货架开始，检查右边连续的 `groupSize` 条货架是否都有足够的商品。如果都有，就把这些商品一起“打包发货”。如果某条货架的商品不够，就说明无法满足要求，直接放弃。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canArrange(hand: List[int], groupSize: int) -> bool:
    n = len(hand)
    # 先判断能否整除，否则必然不可能全部分完
    if n % groupSize != 0:
        return False

    # 1. 统计每个数字出现的次数（哈希表）
    cnt = Counter(hand)

    # 2. 把所有不同的数字排个序，从小到大遍历
    for x in sorted(cnt):
        # 如果当前数字已经被前面的组“吃光”了，直接跳过
        if cnt[x] == 0:
            continue

        # 需要把 cnt[x] 张以 x 为起点的连续序列都取走
        need = cnt[x]

        # 3. 检查 x, x+1, …, x+groupSize-1 是否都有足够的牌
        for i in range(x, x + groupSize):
            if cnt[i] < need:          # 不足，直接返回 False
                return False
            cnt[i] -= need              # 把这些牌从库存中扣掉

    # 所有数字都顺利配对完
    return True
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `Counter` 统计是 `O(n)`。  
  - 对不同的数字进行排序需要 `O(m log m)`，其中 `m` 为不同数字的个数，`m ≤ n`，所以整体是 `O(n log n)`。  
  - 内层的遍历总共只会遍历 `n` 次（每张牌只会被减一次），不影响整体复杂度。

- **空间复杂度**：`O(m)`（哈希表的大小），最坏情况下 `m = n`，即 `O(n)`。  
  与暴力解相比，省去了递归栈，只用一个计数表保存信息。

---

## 心得

- **核心技巧**：**贪心 + 哈希计数**。先把最小的未使用元素作为起点，确保每一步都构成合法的连续序列，再一次性扣除计数，避免回溯。
- **适用的题型**  
  1. “将数组分成 k 长度的连续子数组” （本题）。  
  2. “把数组拆成若干个相同大小的子集，使每个子集满足某种顺序/相等条件” （如 LeetCode 1296 Divide Array in Sets of K Consecutive Numbers）。  
  3. “把手牌或数字序列分成若干顺子” 类似扑克牌游戏的题目。
- **一句话总结解题钥匙**：**从最小的未使用数字出发，贪心地一次性消耗完整的连续区间**。

---

## 反思

- **第一反应**：看到“连续”“分组”两个关键词，立刻想到先排序，再尝试把相邻的 `groupSize` 个数放进一组。随后想到回溯会很慢，于是寻找更直接的贪心策略。
- **最容易踩的坑**  
  1. **不能直接用列表切片**：因为同一个数字可能出现多次，需要计数而不是只检查是否存在。  
  2. **忘记先检查能否被 `groupSize` 整除**，会导致在后面的循环里出现负数的异常情况。  
  3. **边界条件**：当 `groupSize = 1` 时，答案永远是 `True`（只要数组非空），代码仍然要能正常跑通。  
- **下次遇到同类题**：第一步先 **统计频次 + 排序**，然后 **从最小值开始贪心构造连续序列**，检查是否出现“库存不足”的情况。这样可以快速判断可行性，避免暴力回溯的时间爆炸。