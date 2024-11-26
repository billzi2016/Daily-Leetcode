# #2952. 最少需要添加的硬币数量 / Minimum Number of Coins to be Added

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-coins-to-be-added/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array coins, representing the values of the coins available, and an integer target.
An integer x is obtainable if there exists a subsequence of coins that sums to x.
Return the minimum number of coins of any value that need to be added to the array so that every integer in the range [1, target] is obtainable.
A subsequence of an array is a new non-empty array that is formed from the original array by deleting some (possibly none) of the elements without disturbing the relative positions of the remaining elements.

**Examples**

**Example 1:**

```
Input: coins = [1,4,10], target = 19
Output: 2
Explanation: We need to add coins 2 and 8. The resulting array will be [1,2,4,8,10].
It can be shown that all integers from 1 to 19 are obtainable from the resulting array, and that 2 is the minimum number of coins that need to be added to the array.
```

**Example 2:**

```
Input: coins = [1,4,10,5,7,19], target = 19
Output: 1
Explanation: We only need to add the coin 2. The resulting array will be [1,2,4,5,7,10,19].
It can be shown that all integers from 1 to 19 are obtainable from the resulting array, and that 1 is the minimum number of coins that need to be added to the array.
```

**Example 3:**

```
Input: coins = [1,1,1], target = 20
Output: 3
Explanation: We need to add coins 4, 8, and 16. The resulting array will be [1,1,1,4,8,16].
It can be shown that all integers from 1 to 20 are obtainable from the resulting array, and that 3 is the minimum number of coins that need to be added to the array.
```

**Constraints**

- 1 <= target <= 105
- 1 <= coins.length <= 105
- 1 <= coins[i] <= target

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `coins`，表示可用硬币的面值，以及一个整数 `target`。  
如果存在 `coins` 的一个子序列（subsequence）其元素和等于 `x`，则称整数 `x` 是可获得的（obtainable）。  
返回需要向数组中添加的任意面值硬币的最少数量，使得区间 `[1, target]` 内的每个整数都可获得。  

**子序列的定义**  
数组的子序列是通过删除（可能不删除）若干元素后得到的一个新的非空数组，删除操作不改变剩余元素的相对顺序。

**示例**  

*示例 1*  
```
Input: coins = [1,4,10], target = 19
Output: 2
Explanation: 需要添加硬币 2 和 8。得到的数组为 [1,2,4,8,10]。  
可以证明，在该数组中可以获得 1 到 19 的所有整数，且添加的硬币数量的最小值为 2。
```

*示例 2*  
```
Input: coins = [1,4,10,5,7,19], target = 19
Output: 1
Explanation: 只需添加硬币 2。得到的数组为 [1,2,4,5,7,10,19]。  
可以证明，在该数组中可以获得 1 到 19 的所有整数，且添加的硬币数量的最小值为 1。
```

*示例 3*  
```
Input: coins = [1,1,1], target = 20
Output: 3
Explanation: 需要添加硬币 4、8 和 16。得到的数组为 [1,1,1,4,8,16]。  
可以证明，在该数组中可以获得 1 到 20 的所有整数，且添加的硬币数量的最小值为 3。
```

**约束条件**  

- `1 <= target <= 10^5`  
- `1 <= coins.length <= 10^5`  
- `1 <= coins[i] <= target`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的子序列**，看它们能否凑出 `[1, target]` 区间内的每一个整数。  
- **子序列**：就像把原数组的若干个硬币挑出来（保持原来的顺序），不挑的直接丢掉。  
- **暴力做法**：先把原数组 `coins` 复制一份，然后**尝试在它后面添加 0、1、2、… 个硬币**（硬币的面值可以随意取 1~target），每种添加方式都枚举所有子序列，看能否覆盖 `[1, target]`。  

为什么这能得到正确答案？因为我们把**所有可能的添加方案**都穷举了一遍，只要有一种方案能满足要求，就一定会被检查到，最小的添加数自然会被记录下来。  

显然，这种方法在 **时间和空间** 上都不可接受：  
- `coins` 长度最多 10⁵，子序列的组合数是 `2ⁿ`（指数级），根本算不完。  
- 再加上要尝试不同的添加硬币数量，搜索空间更是天文数字。  

#### 代码（Python）  

```python
from itertools import combinations

def brute_min_add(coins, target):
    """
    暴力解：尝试添加 0~target 个硬币（面值 1~target），
    检查所有子序列能否覆盖 [1, target]。
    只用于演示思路，实际数据会超时。
    """
    # 先把原数组排序，方便后面子序列枚举（不影响正确性）
    coins = list(coins)

    # helper：判断在当前硬币集合下，能否得到所有 1~target
    def can_cover(arr):
        n = len(arr)
        # 用位运算枚举子序列（仅适用于 n 小于 20 的情况）
        for mask in range(1, 1 << n):
            s = 0
            for i in range(n):
                if mask >> i & 1:          # 选第 i 枚硬币
                    s += arr[i]
            if s <= target:
                reachable.add(s)

        # 检查是否全部覆盖
        return all(x in reachable for x in range(1, target + 1))

    # 暴力尝试添加的数量
    for add_cnt in range(target + 1):          # 最多加 target 个 1 元硬币
        # 生成所有可能的添加组合（这里仅示例，实际不可行）
        for added in combinations(range(1, target + 1), add_cnt):
            new_arr = coins + list(added)
            reachable = set()
            if can_cover(new_arr):
                return add_cnt
    return -1  # 理论上不会到这里
```

> **注意**：上述代码仅为“思路展示”。在真实数据（`coins` 长度、`target` up to 10⁵）下会 **超时**，甚至 **内存爆炸**。  

#### 复杂度  

- **时间复杂度**：`O(2^n * target)`（指数级），因为我们枚举了所有子序列并对每个子序列求和。  
  - 大白话：如果你有 20 枚硬币，子序列就有约 `1,048,576` 种，已经很慢了；如果是 30 枚，子序列数会到 `≈ 10⁹`，根本不可能在电脑里跑完。  
- **空间复杂度**：`O(target)` 用来保存可以得到的和集合。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于：我们不需要真的去枚举子序列，只要知道**当前能够凑出的最大连续区间** `[1, x]`，就可以判断下一个硬币是否能继续扩展这个区间。  

**关键观察**（来源于提示）：

1. **已知**：我们已经可以用若干硬币凑出所有整数 `1 … x`（`x` 初始为 `0`，表示什么都凑不出来）。  
2. **如果** 下一枚未使用的硬币 `c` **恰好等于 `x+1`**，那么把它加入后，我们可以继续凑出 `1 … x + c`，也就是 `1 … x + (x+1) = 1 … 2x+1`。  
3. **如果** `c > x+1`，说明在没有新硬币的情况下，`x+1` 这个数**永远凑不出来**。唯一的办法是**主动在数组里加一枚面值为 `x+1` 的硬币**。加入后，同理可以把可覆盖区间扩大到 `1 … 2x+1`。  

这就形成了**贪心**的过程：**始终保持区间 `[1, x]` 连续可得**，每次看下一个最小的硬币：

- 若它 ≤ `x+1`，直接使用它，`x ← x + coin`。  
- 否则，**必须补一个硬币 `x+1`**，计数加一，`x ← 2*x + 1`（因为我们相当于把 `x+1` 加进来后，又能把原来的所有组合再加上它）。  

继续上述步骤，直到 `x ≥ target`，此时 `[1, target]` 已经全部可得，返回添加硬币的次数。  

**为什么贪心是最优的？**  
- 我们每次都**尽可能少地添加硬币**：只有在真的缺 `x+1` 时才补。  
- 添加更大的硬币（比如 `> x+1`）永远不能帮助我们凑出 `x+1`，所以一定是多余的。  
- 只要把 `x+1` 加进去，就能把可达上限立刻翻倍（`2x+1`），这已经是**最大化一次添加的收益**。因此没有别的添加方案能用更少的硬币覆盖同样的范围。  

#### 代码（Python）  

```python
def minAddedCoins(coins, target):
    """
    贪心解：维护当前能够凑出的最大连续区间 [1, reachable]。
    只要下一个硬币的面值大于 reachable+1，就必须补一个硬币 reachable+1。
    时间 O(n log n)（排序），空间 O(1)。
    """
    coins.sort()                 # 先把硬币从小到大排好序
    added = 0                    # 记录补的硬币数量
    reachable = 0                # 当前可以连续凑出的最大数，初始为 0（即 [1,0] 为空）

    i = 0                        # 遍历已排序的 coins
    n = len(coins)

    while reachable < target:
        # 1）如果还有未使用的硬币且它的面值 ≤ reachable+1，直接使用它
        if i < n and coins[i] <= reachable + 1:
            reachable += coins[i]   # 扩大可达区间
            i += 1                  # 移动指针
        else:
            # 2）否则必须补一个硬币 reachable+1
            added += 1
            # 加入后可达区间翻倍：原来可以得到 [1, reachable]，
            # 再加上这个新硬币，就能得到 [reachable+1, 2*reachable+1]
            reachable = reachable * 2 + 1

    return added
```

**代码解释（逐行注释）**  

| 行号 | 代码 | 中文解释 |
|------|------|----------|
| 1 | `coins.sort()` | 把已有硬币从小到大排好，就像把钱包里的零钱从面值最小的排到最大的，方便逐个检查。 |
| 2 | `added = 0` | 记录我们补了多少枚新硬币。 |
| 3 | `reachable = 0` | 当前已经可以连续凑出的最大整数。`0` 表示还什么都凑不出来。 |
| 5‑6 | `i = 0; n = len(coins)` | 用指针 `i` 遍历已排序的硬币。 |
| 8 | `while reachable < target:` | 只要还没有覆盖到 `target`，就继续循环。 |
| 10‑13 | `if i < n and coins[i] <= reachable + 1:` … | 如果还有硬币且它的面值不大于 `reachable+1`，直接使用这枚硬币，把可达上限加上它的面值。 |
| 15‑18 | `else:` … | 否则说明缺少恰好是 `reachable+1` 的硬币，我们只能**补**它。补完后可达上限会变成 `2*reachable+1`（相当于把原来的所有组合都再加上这枚新硬币）。 |
| 20 | `return added` | 循环结束时，`added` 就是最少需要补的硬币数量。 |

#### 复杂度  

- **时间复杂度**：`O(n log n)`，主要是排序 `coins` 的开销。遍历一次数组和若干次补硬币的循环都是线性的。  
  - 大白话：如果有 10⁵ 枚硬币，排序大约需要 10⁵ × log₂10⁵ ≈ 1.7 百万次比较，完全可以在一秒以内完成。  
- **空间复杂度**：`O(1)`（不计排序本身的原地实现），只用了几个整数变量。  

---

## 心得  

- **核心技巧**：**维护“当前可达的最小缺口”**（即 `reachable+1`），并用**贪心**方式在缺口出现时立即补齐。  
- **适用场景**：  
  1. **最小补全硬币/分数** 类题目（如 LeetCode 330. Patching Array）。  
  2. **区间覆盖** 需要连续可达的情况（如构造最小集合使所有数都能被表示）。  
  3. **背包类的变体**，当我们只关心**连续**可达范围时的优化。  
- **一句话总结**：**只在缺少“下一个最小不可得数”时补它，补完后区间会立刻翻倍，这就是最少硬币的钥匙。**  

---

## 反思  

- **第一反应**：看到“每个整数都必须可由子序列得到”，立刻想到**枚举子序列**或**动态规划**。但这会忽视题目中“连续可得”这一关键结构。  
- **最容易踩的坑**：  
  - 忽略 **排序**，直接用原序列会导致错误的判断，因为我们必须按照从小到大的顺序检查缺口。  
  - 误以为只需要补 `target - sum(coins)` 那么多硬币，实际上补的硬币面值决定了覆盖效率。  
  - 边界条件：当 `coins` 已经可以覆盖 `[1, target]` 时，循环应该直接结束，返回 `0`。  
- **下次遇到同类题**，第一步应该：**把已有元素从小到大排列，确定当前连续可达的最大值 `x`，然后检查下一个元素是否正好是 `x+1`**——这一步往往能直接揭示贪心策略。