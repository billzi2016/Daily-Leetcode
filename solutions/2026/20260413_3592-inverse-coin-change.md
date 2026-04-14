# #3592. 逆向硬币兑换 / Inverse Coin Change

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/inverse-coin-change/)

---

## 题目（英文原版）

**Description**

You are given a 1-indexed integer array numWays, where numWays[i] represents the number of ways to select a total amount i using an infinite supply of some fixed coin denominations. Each denomination is a positive integer with value at most numWays.length.
However, the exact coin denominations have been lost. Your task is to recover the set of denominations that could have resulted in the given numWays array.
Return a sorted array containing unique integers which represents this set of denominations.
If no such set exists, return an empty array.

**Examples**

**Example 1:**

```
Input: numWays = [0,1,0,2,0,3,0,4,0,5]
Output: [2,4,6]
Explanation:
Input: numWays = [1,2,2,3,4]
Output: [1,2,5]
Explanation:
Example 3:
Input: numWays = [1,2,3,4,15]
Output: []
Explanation:
No set of denomination satisfies this array.
```

**Example 2:**

```
Input: numWays = [1,2,2,3,4]
Output: [1,2,5]
Explanation:
```

**Example 3:**

```
Input: numWays = [1,2,3,4,15]
Output: []
Explanation:
No set of denomination satisfies this array.
```

**Constraints**

- 1 <= numWays.length <= 100
- 0 <= numWays[i] <= 2 * 108

---

## 题目（中文翻译）

给定一个 **1‑索引** 的整数数组 `numWays`，其中 `numWays[i]` 表示使用若干固定面额的硬币（每种面额的硬币数量无限）能够凑出总金额 `i` 的不同组合数。每个面额都是不超过 `numWays.length` 的正整数。  
然而，这些具体的硬币面额已经遗失。请你恢复出所有可能导致给定 `numWays` 数组的面额集合。

返回一个 **已排序且唯一** 的整数数组，表示该面额集合。  
如果不存在任何满足条件的面额集合，返回空数组。

## 示例

### 示例 1
**输入**  
```
numWays = [0,1,0,2,0,3,0,4,0,5]
```
**输出**  
```
[2,4,6]
```
**解释**  
`numWays` 中的奇数下标均为 0，说明只能使用偶数面额的硬币。面额集合 `[2,4,6]` 能够产生对应的组合数。

### 示例 2
**输入**  
```
numWays = [1,2,2,3,4]
```
**输出**  
```
[1,2,5]
```
**解释**  
面额集合 `[1,2,5]` 可以得到 `numWays` 中的每个计数。

### 示例 3
**输入**  
```
numWays = [1,2,3,4,15]
```
**输出**  
```
[]
```
**解释**  
不存在任何硬币面额集合能够产生该 `numWays` 数组。

## 约束

- `1 <= numWays.length <= 100`
- `0 <= numWays[i] <= 2 * 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的硬币面额集合**，把每一种集合都带入「普通的零钱兑换」动态规划中，算出对应的 `numWays` 数组，看是否和题目给出的完全相同。  

- **枚举集合**：面额的取值范围是 `1 … n`（`n = len(numWays)`），于是我们可以把每个数看成“是否在硬币集合里”。这相当于把 `n` 个开关全部摆出来，所有的开关组合（`2ⁿ` 种）就是所有可能的硬币集合。  
- **模拟计算**：对于每个候选集合，用经典的「无穷硬币背包」DP 计算出 `ways[i]`（选出总额 `i` 的方案数），这一步和求零钱兑换的「有多少种方式」完全一样。  
- **比对**：如果得到的 `ways` 完全等于题目给出的 `numWays`，说明这套面额是合法的，直接返回。

> **生活化类比**：把硬币集合想成一本词典的“词表”。我们要尝试所有可能的词表，然后用词表去查每个单词出现的次数，看看是否和老师给的统计表一模一样。

这种方法 **一定能找到答案**（如果答案存在），因为它把所有可能的硬币集合都穷举了一遍。  

但是它的时间和空间代价非常大：

- **时间复杂度**：枚举 `2ⁿ` 种集合，每种集合要跑一次 DP，DP 本身是 `O(n·k)`（`k` 为硬币种类数，最坏 `k=n`），所以整体是 `O(2ⁿ·n²)`，对于 `n=100` 完全不可接受。  
- **空间复杂度**：存 DP 表需要 `O(n)` 的额外数组。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def brute_inverse_coin_change(numWays: List[int]) -> List[int]:
    n = len(numWays) - 1               # numWays 是 1-indexed，长度为 n+1
    # 所有可能的硬币面额 1..n
    candidates = list(range(1, n + 1))

    # 枚举硬币个数，从 1 到 n
    for k in range(1, n + 1):
        # 取出所有长度为 k 的组合
        for comb in combinations(candidates, k):
            # ----- 动态规划：计算该组合对应的方案数 -----
            ways = [0] * (n + 1)
            ways[0] = 1                 # 金额 0 的方案只有一种：不选硬币
            for coin in comb:          # 每一种硬币都可以无限使用
                for s in range(coin, n + 1):
                    ways[s] += ways[s - coin]

            # ----- 与题目给出的 numWays 对比 -----
            if ways == numWays:
                return sorted(comb)    # 找到合法集合，直接返回

    # 没有任何组合匹配
    return []
```

> 关键行解释  
> - `combinations(candidates, k)`：相当于把 `k` 把钥匙挑出来，尝试只用这几把钥匙开锁。  
> - `ways[s] += ways[s - coin]`：把「选到 `s‑coin`」的所有方案，延伸一枚面额为 `coin` 的硬币，得到「选到 `s`」的方案。

#### 复杂度

- **时间复杂度**：`O(2ⁿ · n²)` —— 先把所有子集枚举完（指数级），每套子集再跑一次 `O(n²)` 的 DP。对 `n=100` 来说，几乎不可能在合理时间内跑完。  
- **空间复杂度**：`O(n)` —— DP 表只需要长度为 `n+1` 的一维数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有可能的硬币集合**，这一步是指数级的。  
观察题目给出的 **提示**（下面会再次解释），我们可以 **逆向推导** 出硬币集合，而不必枚举。

**核心观察**  

1. **最小面额一定对应 `numWays[c] = 1`**  
   - 想象只使用一种硬币 `c`，那么只能凑出 `c, 2c, 3c …`。其中最小的正数 `c` 只能用 **一枚** 硬币得到，方案数自然是 `1`。  
   - 因此在整个 `numWays` 中，最左边（最小下标）且等于 `1` 的位置必然是 **最小硬币面额**。

2. **把已知硬币的贡献「剔除」**  
   - 假设我们已经确认硬币 `c` 存在。对于任意金额 `s (≥ c)`，所有使用这枚硬币的方案数恰好等于 **`numWays[s‑c]`**（把一枚 `c` 放在最前面，剩下的方案数就是凑 `s‑c` 的方式）。  
   - 所以我们可以 **从后往前** 把这些贡献从 `numWays` 中减掉：`numWays[s] -= numWays[s‑c]`。减完后，`numWays` 只保留 **未使用硬币 `c` 的方案数**。

3. **循环上述步骤**  
   - 再次寻找最小的 `numWays[i] == 1`（此时的 `1` 已经是「只用剩余硬币」的方案数），它就是下一个硬币面额。  
   - 重复「剔除贡献」的过程，直至数组全为 `0`（说明所有方案都被解释完），或者再也找不到 `1`（说明输入不合法）。

**为什么这样就能得到唯一答案**  

- 每次我们都取 **当前最小的** 能产生唯一方案的金额 `c`，这一定是剩余硬币集合里的最小面额。因为如果有更小的硬币 `d < c`，它的方案数也会在对应位置出现 `1`（只用 `d` 本身），冲突。  
- 通过「剔除」我们实际上在做「逆向的背包 DP」——把已经确定的硬币的贡献逐层消除，剩下的数组始终保持「仅由未确定硬币产生的方案数」。

**类比**：想象你在玩“拆积木”游戏，先找出最小的那块积木（只能拼出唯一一种形状），把它从整体结构里拆下来，剩下的结构仍然是一座合法的积木塔。一次次拆除，最后塔子全部拆完，说明找到了所有积木的种类。

#### 代码（Python）

```python
from typing import List

def inverse_coin_change(numWays: List[int]) -> List[int]:
    """
    逆向恢复硬币面额集合。
    输入的 numWays 是 1-indexed（下标 0 位置固定为 0），
    为了方便在原数组上直接修改，这里复制一份。
    """
    n = len(numWays) - 1                # 实际的最大金额
    ways = numWays[:]                    # 深拷贝，后面会原地修改
    ans = []                             # 最终的硬币集合

    while True:
        # 1️⃣ 找最小的下标 i，使得 ways[i] == 1
        c = None
        for i in range(1, n + 1):
            if ways[i] == 1:            # 只出现一次的方案，只能是最小硬币
                c = i
                break

        # 若找不到 1，说明已经没有新硬币可以确定
        if c is None:
            break

        # 2️⃣ 记录硬币面额
        ans.append(c)

        # 3️⃣ “剔除”该硬币的贡献
        #    从 c 开始往后，所有 ways[s] 减去 ways[s-c]
        for s in range(c, n + 1):
            ways[s] -= ways[s - c]
            if ways[s] < 0:             # 负数说明输入不合法，直接返回空数组
                return []

    # 4️⃣ 检查是否所有方案数都被消掉
    if any(v != 0 for v in ways[1:]):    # 下标 0 本来就是 0，忽略
        return []                        # 仍有未解释的方案 → 不合法

    return sorted(ans)                  # 题目要求返回升序
```

> 关键行中文注释  
> - `for i in range(1, n + 1): if ways[i] == 1:`：在「剩余」的方案表里找唯一出现一次的金额，它一定是当前最小硬币。  
> - `ways[s] -= ways[s - c]`：把「使用一枚硬币 c」的所有组合从总数里减掉，相当于把这枚硬币的“贡献”剥离。  
> - `if ways[s] < 0:`：如果出现负数，说明原数组里本来就不可能由合法硬币集合产生，直接判定为无解。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每一次找到一个硬币后，需要遍历 `c … n` 更新 `ways`，最坏情况下会找出 `n` 个硬币（实际上硬币数 ≤ n），于是整体是 `1 + 2 + … + n = O(n²)`。  
  - 与暴力解的指数级相比，`n ≤ 100` 时毫秒级即可跑完。

- **空间复杂度**：`O(n)`  
  - 只用了原数组的拷贝和答案列表，均为长度 `n+1` 的一维数组。  

相比暴力解，时间从 **指数级** 降到了 **多项式级**，在本题的约束下完全可以接受。

---

## 心得

- **核心技巧**：**逆向动态规划**（把已知硬币的贡献逐层剔除），利用 `numWays[i] == 1` 这个“唯一性”特征定位最小硬币。  
- **适用场景**：  
  1. 需要从「结果」逆推出「输入」的背包/硬币类问题。  
  2. 任何「组合计数」已知、且计数数组满足「最小正数对应唯一方案」的情形。  
  3. 类似的题目还有「Recover Array from Subset Sums」「Inverse Subset Sum」等。  
- **一句话总结**：**把每枚已确定的硬币当作“已知的贡献”，从计数表中逐个扣除，剩下的就是下一枚硬币的线索**。

---

## 反思

- **第一反应**：先想「枚举所有硬币集合」再比对——这就是最直观的暴力思路。  
- **最容易踩的坑**：  
  - 忽视 `numWays` 是 **1-indexed**（下标 0 固定为 0），导致循环起点错误。  
  - 在「剔除」过程中出现负数却不立即终止，最终会得到错误的答案。  
  - 没有在全部扣除完毕后检查数组是否真的全为 0，可能会误判为合法集合。  
- **下次遇到同类题**：第一步就思考 **“是否可以从计数表里直接读出最小元素的唯一性”**，尝试把已知信息逆向消除，而不是盲目枚举。这样往往能把指数级搜索压缩到多项式时间。