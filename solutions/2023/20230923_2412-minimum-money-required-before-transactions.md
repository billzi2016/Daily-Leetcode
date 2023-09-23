# #2412. **交易前所需的最小金额** / Minimum Money Required Before Transactions

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-money-required-before-transactions/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array transactions, where transactions[i] = [costi, cashbacki].
The array describes transactions, where each transaction must be completed exactly once in some order. At any given moment, you have a certain amount of money. In order to complete transaction i, money >= costi must hold true. After performing a transaction, money becomes money - costi + cashbacki.
Return the minimum amount of money required before any transaction so that all of the transactions can be completed regardless of the order of the transactions.

**Examples**

**Example 1:**

```
Input: transactions = [[2,1],[5,0],[4,2]]
Output: 10
Explanation:
Starting with money = 10, the transactions can be performed in any order.
It can be shown that starting with money < 10 will fail to complete all transactions in some order.
```

**Example 2:**

```
Input: transactions = [[3,0],[0,3]]
Output: 3
Explanation:
- If transactions are in the order [[3,0],[0,3]], the minimum money required to complete the transactions is 3.
- If transactions are in the order [[0,3],[3,0]], the minimum money required to complete the transactions is 0.
Thus, starting with money = 3, the transactions can be performed in any order.
```

**Constraints**

- 1 <= transactions.length <= 105
- transactions[i].length == 2
- 0 <= costi, cashbacki <= 109

---

## 题目（中文翻译）

你得到一个下标从 0 开始的 **2D 整数数组（2D integer array）** `transactions`，其中 `transactions[i] = [costi, cashbacki]`。  
该数组描述了一系列交易，每笔交易必须恰好执行一次，执行顺序可以自行决定。此时你拥有一定的 **money**（金钱）。要完成第 `i` 笔交易，需要满足 `money >= costi`。完成交易后，`money` 会变为 `money - costi + cashbacki`。

返回在 **任何** 交易顺序下，都能够完成所有交易所需的 **最少初始金钱**（即在进行任何交易之前必须拥有的最小 `money`）。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  
**示例 1**  
```text
Input: transactions = [[2,1],[5,0],[4,2]]
Output: 10
Explanation:
从 money = 10 开始，所有交易可以按任意顺序完成。
可以证明，若初始 money < 10，则在某些顺序下无法完成全部交易。
```

**示例 2**  
```text
Input: transactions = [[3,0],[0,3]]
Output: 3
Explanation:
- 若交易顺序为 [[3,0],[0,3]]，完成所有交易所需的最小 money 为 3。
- 若交易顺序为 [[0,3],[3,0]]，完成所有交易所需的最小 money 为 0。
因此，初始 money = 3 时，任意顺序都能完成所有交易。
```

**约束条件**  
- `1 <= transactions.length <= 10^5`
- `transactions[i].length == 2`
- `0 <= costi, cashbacki <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有交易的执行顺序全部枚举**，然后对每一种顺序模拟实际需要的初始金钱。  
- 把 `transactions` 看成一张“任务表”，每一行是一笔交易 `[costi, cashbacki]`。  
- 枚举所有可能的排列（Permutation），就像把这张任务表的行重新排个序。  
- 对于固定的顺序，模拟执行：  
  1. 记录当前手里有多少钱 `money`（一开始是 `0`），  
  2. 在执行第 `i` 笔交易前，如果 `money < costi`，就需要额外的 `costi - money` 来补足，这部分钱就是**必须提前准备的**。  
  3. 交易结束后 `money = money - costi + cashbacki`。  
- 把所有交易完成后，所有补足的钱的最大值就是这条顺序需要的最少初始金钱。  
- 把所有顺序得到的最小值再取 **最小**，就是题目要求的答案。

> **类比**：把每笔交易想象成一次“买东西并得到返现”。如果你想把所有东西都买完，最保守的办法就是先把所有可能的买买顺序都写下来，看看哪一种顺序需要的零花钱最少。

> **为什么正确**：因为我们穷举了所有合法的执行顺序，必然会覆盖最优顺序。对每个顺序我们都算出了恰好能完成它所需的最小初始金钱，所以在所有顺序里取最小就得到全局最优。

> **缺点**：排列数随 `n`（交易数）呈阶乘增长，`n` 稍大就根本算不完。

#### 代码（Python）

```python
import itertools
from typing import List

def min_money_bruteforce(transactions: List[List[int]]) -> int:
    """
    暴力枚举所有顺序，返回能够完成所有交易的最小初始金钱。
    只适用于交易数非常少的情况（比如 n <= 8）。
    """
    best = float('inf')                     # 记录全局最小值
    for order in itertools.permutations(transactions):
        need = 0      # 需要提前准备的金钱（答案候选）
        money = 0     # 当前手里拥有的金钱
        for cost, cash in order:
            if money < cost:                # 手里不够付钱
                need = max(need, cost - money)  # 需要在一开始多准备这些
            money = money - cost + cash      # 完成交易后的余额
        best = min(best, need)              # 更新最小答案
    return best
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  `n!` 表示所有排列的数量，`* n` 是对每条排列模拟 `n` 笔交易的代价。  
  用大白话说，就是“随交易数的增加，时间会呈指数级爆炸”，所以只能在非常小的 `n` 下使用。

- **空间复杂度**：`O(n)`  
  主要是递归/迭代产生的排列对象以及几个临时变量，和 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举顺序** 上。我们要想办法 **直接构造** 那个“最安全的顺序”，不需要遍历所有可能。  
观察每笔交易的 **净收益**：

```
net = cashbacki - costi
```

- 若 `net >= 0`（返现不少于花费），这笔交易 **不会让你失钱**，甚至还能赚钱。我们把这类交易叫 **赚钱交易**。
- 若 `net < 0`，这笔交易 **会让你亏钱**，叫 **亏钱交易**。

**关键观察 1**：  
对赚钱交易来说，执行顺序只影响 **“在真正需要钱之前，先把钱塞进口袋”** 的程度。  
- 如果先做 **费用大的** 赚钱交易，虽然一开始需要的 `cost` 可能更大，但随后马上会把 `cashback`（不少于 `cost`）放回，手里的钱不降。  
- 把费用大的放在前面，能够 **降低整个过程的最高资金缺口**。  
> 因此，把所有赚钱交易 **按 cost 降序** 排序（大到小），先做费用最大的。

**关键观察 2**：  
对亏钱交易来说，每做完一笔，你的手里钱会 **净下降** `|net|`。  
- 为了让后面的交易 **更容易完成**，我们希望 **先把“亏得少”的交易做掉**，把大亏的留到最后（因为此时手里已经有了前面赚到的“缓冲”）。  
- 亏钱交易的 “亏得少” 可以用 **cashback**（返现）来衡量——返现越大，净亏越小。  
> 所以，把所有亏钱交易 **按 cashback 升序** 排序（小到大），先做返现最少的。

**关键观察 3**（为什么两类分开排序后整体顺序安全）  
- 先完成所有赚钱交易（大费用在前），此时手里的钱 **不会下降**，只会等于或高于开始时的 `need`。  
- 再完成所有亏钱交易（小返现在前），每一步的资金缺口都已经被前面的赚钱交易提供的“缓冲”所覆盖。  
- 这样，无论把这两大块顺序调换（先亏后赚），**最差的情况** 就是我们上面构造的顺序。因此，这个顺序保证了 **在任意顺序下都能完成**，而我们只需要计算这条顺序的最小初始金钱即可。

**实现细节**  
1. 把交易分成两组 `good`（`cashback >= cost`）和 `bad`（`cashback < cost`）。  
2. 对 `good` 按 `cost` **降序** 排序；对 `bad` 按 `cashback` **升序** 排序。  
3. 按 `good` → `bad` 的顺序遍历，每一次记录当前手里已有的钱 `money`，以及为满足 `cost` 所需的额外准备 `need`：  

```
need = max(need, cost - money)   # 若手里钱不够，就把差额记到 need
money = money - cost + cashback  # 完成交易后的余额
```

4. 最终 `need` 就是答案。

> **类比**：  
想象你在玩“先赚后花”的游戏。先挑选那些“赚钱的宝箱”（赚钱交易），把价值最大的宝箱先打开，这样一开始就能把“大钱袋”装满。接下来再去打开“会掉钱的陷阱”（亏钱交易），先挑最不掉钱的陷阱，这样手里的钱还能撑得更久。整个过程只需要一次遍历，就能算出你一开始最少得准备多少钱才能保证不被卡住。

#### 代码（Python）

```python
from typing import List

def min_money(transactions: List[List[int]]) -> int:
    """
    贪心+排序：在任意顺序下都能完成所有交易所需的最小初始金钱。
    时间复杂度 O(n log n)，空间复杂度 O(n)。
    """
    good, bad = [], []               # 分别存放赚钱和亏钱的交易

    for cost, cash in transactions:
        if cash >= cost:
            good.append((cost, cash))
        else:
            bad.append((cost, cash))

    # 赚钱交易：费用大的先做
    good.sort(key=lambda x: -x[0])   # 按 cost 降序
    # 亏钱交易：返现少的先做
    bad.sort(key=lambda x: x[1])     # 按 cashback 升序

    need = 0      # 需要提前准备的最小金钱
    money = 0     # 当前手里拥有的金钱（从 0 开始累计）

    # 先执行赚钱交易
    for cost, cash in good + bad:    # 按顺序遍历
        if money < cost:             # 手里钱不够付 cost
            need = max(need, cost - money)  # 把差额记入 need
        money = money - cost + cash   # 完成交易后的余额

    return need
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  两次排序各占 `O(k log k)`（`k` 是各自组的大小），总体不超过 `O(n log n)`。遍历一次 `O(n)`，所以总的时间主要是排序的成本。  
  与暴力解的 `O(n! * n)` 相比，**从指数级降到了对数线性级**，即使 `n=10^5` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  需要额外的两个列表 `good`、`bad` 来保存划分后的交易，规模和原数组相同。其余变量都是常数级。

---

## 心得

- **核心技巧**：把交易按照 “赚不赚钱” 两类分组，并对每类使用不同的排序准则（`cost` 降序 / `cashback` 升序），再一次线性扫描求最大缺口。  
- **适用的题型**  
  1. “先赚后花” 类的资源调度问题（如 LeetCode 1745 “Palindrome Permutation” 的贪心思路）。  
  2. 需要在 **任意顺序** 下保证安全的任务序列（比如 “任务调度的最小初始能量” 系列）。  
  3. “正负效应混合” 的优化问题（如 “项目完成的最小初始资本”）。  
- **一句话总结解题钥匙**：**把正收益的放前面、负收益的按“亏得最少”排前，顺序一次遍历即可得到最小起始金钱**。

---

## 反思

- **拿到题目第一反应**：先想到枚举所有顺序，然后计算每种顺序的资金缺口——这自然是最直接的暴力思路。  
- **最容易踩的坑**  
  1. **忽略“任意顺序”**：题目要求 *无论怎么排列* 都能完成，直接求一种最优顺序的最小金钱是不够的，需要保证所有排列都安全。  
  2. **边界条件**：`cost` 或 `cashback` 为 `0` 时仍然要正确分类，尤其 `cashback == cost` 属于 “不亏不赚”，应放入 `good` 并按 `cost` 降序处理。  
  3. **大数溢出**：`cost`、`cashback` 最大到 `10^9`，累计时可能达到 `10^14`，在 Python 中整数无限长不成问题，但在某些语言要用 `long long`。  
- **下次遇到同类题**：第一步先 **看收益符号**（正/负），把正收益的任务提前、负收益的任务按“亏得最少”排序，再一次遍历求最大缺口。这样就能快速得到最优的贪心方案。