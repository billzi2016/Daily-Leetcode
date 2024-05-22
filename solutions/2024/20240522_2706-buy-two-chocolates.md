# #2706. 购买两块巧克力 / Buy Two Chocolates

> 难度：简单 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/buy-two-chocolates/)

---

## 题目（英文原版）

**Description**

You are given an integer array prices representing the prices of various chocolates in a store. You are also given a single integer money, which represents your initial amount of money.
You must buy exactly two chocolates in such a way that you still have some non-negative leftover money. You would like to minimize the sum of the prices of the two chocolates you buy.
Return the amount of money you will have leftover after buying the two chocolates. If there is no way for you to buy two chocolates without ending up in debt, return money. Note that the leftover must be non-negative.

**Examples**

**Example 1:**

```
Input: prices = [1,2,2], money = 3
Output: 0
Explanation: Purchase the chocolates priced at 1 and 2 units respectively. You will have 3 - 3 = 0 units of money afterwards. Thus, we return 0.
```

**Example 2:**

```
Input: prices = [3,2,3], money = 3
Output: 3
Explanation: You cannot buy 2 chocolates without going in debt, so we return 3.
```

**Constraints**

- 2 <= prices.length <= 50
- 1 <= prices[i] <= 100
- 1 <= money <= 100

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `prices`，表示商店中各种巧克力的价格。另给定一个整数 `money`，表示你最初拥有的金额。  
你必须恰好购买两块巧克力，并且购买后仍需保留非负的剩余金额。你希望所购买的两块巧克力的价格之和最小。  
返回购买这两块巧克力后你剩余的金额。如果没有任何方式能够在不欠债的情况下购买两块巧克力，则返回 `money`（即不进行购买）。请注意，剩余金额必须为非负数。

**示例 1**  
```text
Input: prices = [1,2,2], money = 3
Output: 0
Explanation: 购买价格分别为 1 和 2 的两块巧克力。购买后剩余金额为 3 - 3 = 0。因此返回 0。
```

**示例 2**  
```text
Input: prices = [3,2,3], money = 3
Output: 3
Explanation: 无法在不产生负债的情况下购买两块巧克力，所以返回 3。
```

**约束条件**  
- `2 <= prices.length <= 50`  
- `1 <= prices[i] <= 100`  
- `1 <= money <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把所有可能的两块巧克力组合都枚举一遍，算出它们的总价，看哪个总价 **不超过** `money` 且 **最小**。  

- **数据结构**：我们只需要用到 Python 的列表（list），把每一次组合的价格放进一个变量里。可以把列表想象成装糖果的盒子，里面的每个位置放着一种巧克力的价格。  
- **为什么正确**：因为我们遍历了**所有**两两组合，必然能找到满足条件的最小总价（如果有的话），不遗漏任何可能。  
- **复杂度分析**：  
  - 外层循环遍历第一个巧克力 `i`（最多 `n` 次），内层循环遍历第二个巧克力 `j`（最多 `n-1` 次），所以总共检查大约 `n·(n-1)/2` 种组合，数量级记作 **O(n²)**。  
  - 这里的 `O(n²)` 可以理解为“如果 `n` 是 10，运算次数大约是 10×10=100；如果 `n` 是 100，运算次数大约是 100×100=10,000”。  
  - 额外使用的空间只有几个整数变量，记作 **O(1)**（常数空间）。

#### 代码（Python）  

```python
def buy_chocolate_bruteforce(prices, money):
    n = len(prices)
    # 初始化为一个“无限大”的值，表示目前还没有找到可行的组合
    best_sum = float('inf')

    # 枚举所有两两组合
    for i in range(n):
        for j in range(i + 1, n):
            cur_sum = prices[i] + prices[j]          # 当前两块巧克力的总价
            if cur_sum <= money and cur_sum < best_sum:
                best_sum = cur_sum                    # 发现更小的可行总价

    # 如果 best_sum 仍然是初始的无限大，说明没有任何组合满足条件
    if best_sum == float('inf'):
        return money                                 # 只能把钱全留着
    else:
        return money - best_sum                      # 余下的钱
```

#### 复杂度  

- **时间复杂度**：**O(n²)** —— 需要检查所有 `n*(n-1)/2` 对巧克力。  
- **空间复杂度**：**O(1)** —— 只用到常数个临时变量，没有额外的随 `n` 增长的存储。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 在于我们把所有组合都算了一遍。实际上我们只需要关心 **最小的两块巧克力**：

1. 把价格从小到大排好序（就像把糖果按重量从轻到重排好放在架子上）。  
2. 取排好序后的前两块巧克力，它们的总价是所有可能组合中 **最小的**。  
3. 只要这两个最小的价格之和 **不超过** `money`，我们就可以买它们；如果超过了，说明**任何**其他组合的总价都会更大，也一定买不起。  

所以只需要一次排序（`O(n log n)`），或者更快的线性扫描找出最小的两个数（`O(n)`）。这里按照提示使用排序，思路更直观。

> **关键概念——排序**  
> 把一个数组排好序，就像把一堆乱放的书籍按照页码从小到大摆好。这样最左边的两本书（最小的两个数）一定是最便宜的两块巧克力。

#### 代码（Python）  

```python
def buy_chocolate_optimal(prices, money):
    # 1. 把价格从小到大排序
    prices.sort()                     # 排序后，prices[0]、prices[1] 是最小的两个

    # 2. 计算最小两块的总价
    min_pair_sum = prices[0] + prices[1]

    # 3. 判断是否能够负担得起
    if min_pair_sum > money:          # 甚至最便宜的两块都买不起
        return money                  # 只能把钱全留着
    else:
        return money - min_pair_sum   # 余下的钱
```

> 如果想把时间进一步压到 **O(n)**，可以在一次遍历中记录最小的两个数，而不进行完整的排序。思路相同，只是实现方式略有不同。

#### 复杂度  

- **时间复杂度**：**O(n log n)** —— 排序需要 `n log n` 的比较次数。相较于暴力的 `O(n²)`，当 `n` 较大时会快很多。  
- **空间复杂度**：**O(1)** （如果使用原地排序）—— 只用常数级的额外变量。  

---

## 心得  

- **核心技巧**：**贪心 + 排序**——先把数据排好序，再利用“最小的两个数一定给出最小的可行和”这一贪心思想。  
- **适用的题型**  
  1. “买两件商品，花费不超过预算，剩余最少” 类似题（如 LeetCode 2035 – Minimum Two‑Sum）。  
  2. “从数组中找出满足某种约束的最小/最大两元组” 题目（如配对和、配对差）。  
- **一句话总结解题钥匙**：**先把问题的搜索空间压到最小（排序），再直接检查最有可能的答案**。

---

## 反思  

- **第一反应**：把所有两两组合都列出来，直接算最小可行和。  
- **最容易踩的坑**  
  - 忘记返回原始 `money` 当没有任何可行组合时。  
  - 只检查第一个元素和第二个元素后忘记比较大小，导致误以为只要 `prices[0] + prices[1] <= money` 就一定是最优解（其实这里是对的，但要先确保数组已排好序）。  
  - 边界条件：数组长度最小是 2，代码必须保证 `prices[0]` 与 `prices[1]` 必定存在。  
- **下次遇到同类题**：第一步先思考“**有没有一种自然的顺序（排序）能让最优解出现在前面**”。如果能，就先排序，再用 O(1) 或 O(n) 的方式直接得到答案。