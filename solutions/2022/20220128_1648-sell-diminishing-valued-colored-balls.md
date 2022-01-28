# #1648. 出售递减价值的彩球 / Sell Diminishing-Valued Colored Balls

> 难度：中等 · 标签：Array、Math、Binary Search、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/sell-diminishing-valued-colored-balls/)

---

## 题目（英文原版）

**Description**

You have an inventory of different colored balls, and there is a customer that wants orders balls of any color.
The customer weirdly values the colored balls. Each colored ball's value is the number of balls of that color you currently have in your inventory. For example, if you own 6 yellow balls, the customer would pay 6 for the first yellow ball. After the transaction, there are only 5 yellow balls left, so the next yellow ball is then valued at 5 (i.e., the value of the balls decreases as you sell more to the customer).
You are given an integer array, inventory, where inventory[i] represents the number of balls of the ith color that you initially own. You are also given an integer orders, which represents the total number of balls that the customer wants. You can sell the balls in any order.
Return the maximum total value that you can attain after selling orders colored balls. As the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: inventory = [2,5], orders = 4
Output: 14
Explanation: Sell the 1st color 1 time (2) and the 2nd color 3 times (5 + 4 + 3).
The maximum total value is 2 + 5 + 4 + 3 = 14.
```

**Example 2:**

```
Input: inventory = [3,5], orders = 6
Output: 19
Explanation: Sell the 1st color 2 times (3 + 2) and the 2nd color 4 times (5 + 4 + 3 + 2).
The maximum total value is 3 + 2 + 5 + 4 + 3 + 2 = 19.
```

**Constraints**

- 1 <= inventory.length <= 105
- 1 <= inventory[i] <= 109
- 1 <= orders <= min(sum(inventory[i]), 109)

---

## 题目（中文翻译）

你有一个包含不同颜色球的库存（inventory），且有一位顾客想要购买任意颜色的球。  
该顾客对彩球的价值评估方式很特殊。每个颜色球的价值等于你当前库存中该颜色球的数量。例如，如果你拥有 6 个黄色球，则顾客会为第一个黄色球支付 **6**。交易后，黄色球只剩下 5 个，此时下一个黄色球的价值为 **5**（即随着你向顾客出售更多球，同一种颜色球的价值会递减）。

给定一个整数数组 **inventory**，其中 `inventory[i]` 表示你最初拥有的第 *i* 种颜色球的数量。还给定一个整数 **orders**，表示顾客想要购买的球的总数量。你可以以任意顺序出售这些球。

返回在出售恰好 **orders** 个球后能够获得的最大总价值。由于答案可能非常大，请返回结果对 `10^9 + 7` 取模后的值。

**示例 1**  
输入: `inventory = [2,5]`, `orders = 4`  
输出: `14`  
解释: 先卖出第一种颜色 1 次（价值 2），再卖出第二种颜色 3 次（价值 5 + 4 + 3）。  
最大总价值为 **2 + 5 + 4 + 3 = 14**。

**示例 2**  
输入: `inventory = [3,5]`, `orders = 6`  
输出: `19`  
解释: 先卖出第一种颜色 2 次（价值 3 + 2），再卖出第二种颜色 4 次（价值 5 + 4 + 3 + 2）。  
最大总价值为 **3 + 2 + 5 + 4 + 3 + 2 = 19**。

**约束条件**  
- `1 <= inventory.length <= 10^5`  
- `1 <= inventory[i] <= 10^9`  
- `1 <= orders <= min( sum(inventory[i]), 10^9 )`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是每次都把「当前价值最高」的球卖掉。  
- **数据结构**：我们可以把每种颜色的剩余球数放进一个最大堆（`heapq` 的负数实现），相当于把「价值」当作「字典里单词的页码」，堆顶就是价值最大的那颗球。  
- **为什么正确**：因为每卖出一颗球，只会让该颜色的价值下降 1，其他颜色的价值不变。若我们不把当前价值最高的球先卖，就会把一个价值更低的球卖掉，导致总收益不可能更大。  
- **时间/空间复杂度**：  
  - 每卖出一颗球，需要把堆顶弹出、价值减 1 再放回堆中，这一步是 **O(log n)**（`n` 为颜色种类数）。如果要卖 `orders` 颗球，总时间是 **O(orders · log n)**。  
  - 当 `orders` 接近 `10⁹` 时，这个复杂度完全不可接受。  
  - 空间上我们只保存一个大小为 `n` 的堆，**O(n)**。

> **大白话**：`O(orders·log n)` 就像你要买 `orders` 本书，每本书都要去图书馆排队找一本最贵的，这样排队的次数会跟你买的书本数成正比，甚至还有额外的“排队时间”(log n)。当书本很多时，排队次数会爆炸。

#### 代码（Python）

```python
import heapq

def maxProfit_bruteforce(inventory, orders):
    # 把每种颜色的球数取负，构造最大堆（heapq 只能做最小堆）
    max_heap = [-cnt for cnt in inventory]
    heapq.heapify(max_heap)

    MOD = 10**9 + 7
    profit = 0

    for _ in range(orders):
        # 取出价值最高的颜色（负数转正）
        cur = -heapq.heappop(max_heap)          # cur 为当前最大价值
        profit = (profit + cur) % MOD           # 累计收益
        cur -= 1                                # 卖掉一颗后价值减 1
        heapq.heappush(max_heap, -cur)          # 重新放回堆

    return profit
```

#### 复杂度

- **时间复杂度**：`O(orders · log n)`  
  - `orders` 次循环，每次堆操作 `log n`。  
  - 当 `orders` 接近 `10⁹`，这几乎是不可能在一秒内完成的。

- **空间复杂度**：`O(n)`  
  - 只用了一个大小等于颜色种类数的堆。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于逐颗出售，循环次数等于 `orders`。  
我们需要一次性算出「卖掉一段连续价值」能得到多少收益。

观察价值随出售的变化：

| 颜色 | 初始数量 `c` | 第 1 颗价值 `c` | 第 2 颗价值 `c‑1` | … | 第 `k` 颗价值 `c‑k+1` |
|------|--------------|-----------------|-------------------|---|----------------------|

对同一种颜色，若我们一次卖掉从 `c` 到 `t+1`（`t` 为卖完后剩下的数量），收益等于等差数列求和：

\[
\text{gain} = \frac{(c + (t+1)) \times (c - t)}{2}
\]

**关键想法**：在所有颜色中，价值最高的若干球会先被卖完，形成一个「阈值」`k`，所有价值 > `k` 的球全部卖掉，价值恰好等于 `k` 的球可能只卖一部分。

于是任务转化为：**找出这个阈值 `k`**，使得卖掉所有 >`k` 的球恰好（或不超过）`orders` 个。

> **二分搜索**  
> `k` 的取值范围在 `[0, max(inventory)]`。  
> 对每个候选 `k`，我们可以在 O(n) 时间内统计「卖掉价值 > k」的球数：

\[
\text{cnt}(k) = \sum_{c\in inventory} \max(0, c - k)
\]

如果 `cnt(k) >= orders`，说明阈值太低（卖的球太多），需要把 `k` 调高；否则 `k` 太高，需要调低。二分即可定位最接近的 `k`。

**算收益**  
二分得到的 `k` 可能导致卖出的球数多于 `orders`。我们先把所有 >`k` 的球全部卖掉，得到的收益：

\[
\text{profit} = \sum_{c\in inventory} \text{sum\_range}(c, k+1)
\]

其中 `sum_range(c, low)` 计算从 `c` down到 `low`（不含 `low`）的等差和：

\[
\text{sum\_range}(c, low) = \frac{(c + low) \times (c - low + 1)}{2}
\]

此时已经卖出的球数是 `cnt(k)`，如果 `cnt(k) > orders`，说明我们多卖了 `extra = cnt(k) - orders` 球，这些多卖的球的价值恰好都是 `k`（因为我们已经把所有 >k 的球卖完，只剩价值为 `k` 的球）。只需要把 `extra * k` 从总收益中减去即可。

**取模**：因为答案可能很大，需要对 `10⁹+7` 取模。等差和公式中涉及乘法，先对每一步取模防止溢出。

#### 代码（Python）

```python
MOD = 10**9 + 7

def maxProfit(inventory, orders):
    # 1. 二分寻找阈值 k
    lo, hi = 0, max(inventory)          # k 的可能范围
    while lo < hi:
        mid = (lo + hi + 1) // 2        # 取上中位数，防止死循环
        # 统计卖掉所有价值 > mid 的球数
        cnt = sum(max(0, c - mid) for c in inventory)
        if cnt <= orders:               # 已经不超过需求，mid 可以更低
            hi = mid - 1
        else:                           # 卖的太多，需要把阈值调高
            lo = mid

    k = lo                               # 最终阈值

    # 2. 计算收益
    profit = 0
    remain = orders                      # 还需要卖多少球

    for c in inventory:
        if c <= k:
            continue                     # 这类颜色的球全都不卖或只卖 k 以下的
        # 卖掉从 c down 到 k+1 的所有球
        high = c
        low = k + 1
        cnt = high - low + 1              # 卖出的球数
        # 等差和公式： (high + low) * cnt // 2
        profit += (high + low) * cnt // 2
        profit %= MOD
        remain -= cnt                     # 更新还需要卖的球数

    # 3. 处理多卖的部分（全部价值为 k）
    if remain > 0:
        profit += remain * k
        profit %= MOD

    return profit
```

**代码要点解释**  

- `while lo < hi` 用 **上取中位数** `(lo+hi+1)//2`，确保二分收敛。  
- `cnt = sum(max(0, c - mid) for c in inventory)` 统计「大于 mid」的球数。  
- `k = lo` 最后得到的阈值，使得卖掉所有 >k 的球数 **不超过** `orders`。  
- `profit += (high + low) * cnt // 2` 是等差数列求和，先算乘法再除 2，防止整数除法丢精度。  
- `remain` 记录还差多少球未卖，最后用 `remain * k` 把价值恰好为 `k` 的球补齐。  

#### 复杂度

- **时间复杂度**：`O(n · log M)`  
  - `n` 为颜色种类数（`≤ 10⁵`），`M = max(inventory)`（`≤ 10⁹`）。  
  - 二分搜索在 `[0, M]` 上进行，最多 `log₂ M`（约 30）次，每次遍历 `inventory` 统计 `cnt`。  
  - 相比暴力的 `orders` 次循环，显著降低。

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只使用了若干整数变量，常数级额外空间。

---

## 心得

- **核心技巧**：把「每次贪心卖最高价值」转化为「找价值阈值」并一次性算等差和。二分阈值 + 数学求和是本题的解题钥匙。  
- **适用场景**：  
  1. “卖掉价值递减的商品” 类题，如 **LeetCode 1648**（本题）本身。  
  2. “从多个堆中取最大的 K 个元素” 但 K 很大时，可用阈值二分代替堆。  
  3. “分配资源，价值随剩余量递减” 的贪心 + 二分模型。  
- **一句话总结**：**先确定最高价的“切线”，再用等差数列一次算完所有收益**。

---

## 反思

- **第一反应**：立刻想到「每次挑最大」并用最大堆模拟，写出能跑通小数据的代码。  
- **最容易踩的坑**：  
  - 忽略 **剩余球数可能为 0** 时仍需继续二分，导致无限循环。  
  - 在等差求和时忘记对 **模数** 进行中间取模，导致 Python 整数爆炸（虽然 Python 能自动大整数，但会极慢）。  
  - 处理 `remain`（多卖的球）时忘记乘以阈值 `k`，导致答案偏大。  
- **下次思路**：面对“价值随数量递减”且 **K 很大** 的贪心问题，第一步就要思考“是否可以一次性算完一段连续价值”，从而尝试 **二分阈值 + 数学求和** 的方案。这样可以把 O(K) 的循环压到 O(log max value)。