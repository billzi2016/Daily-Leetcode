# #1833. 最大冰淇淋棒数量 / Maximum Ice Cream Bars

> 难度：中等 · 标签：Array、Greedy、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/maximum-ice-cream-bars/)

---

## 题目（英文原版）

**Description**

It is a sweltering summer day, and a boy wants to buy some ice cream bars.
At the store, there are n ice cream bars. You are given an array costs of length n, where costs[i] is the price of the ith ice cream bar in coins. The boy initially has coins coins to spend, and he wants to buy as many ice cream bars as possible.
Note: The boy can buy the ice cream bars in any order.
Return the maximum number of ice cream bars the boy can buy with coins coins.
You must solve the problem by counting sort.

**Examples**

**Example 1:**

```
Input: costs = [1,3,2,4,1], coins = 7
Output: 4
Explanation: The boy can buy ice cream bars at indices 0,1,2,4 for a total price of 1 + 3 + 2 + 1 = 7.
```

**Example 2:**

```
Input: costs = [10,6,8,7,7,8], coins = 5
Output: 0
Explanation: The boy cannot afford any of the ice cream bars.
```

**Example 3:**

```
Input: costs = [1,6,3,1,2,5], coins = 20
Output: 6
Explanation: The boy can buy all the ice cream bars for a total price of 1 + 6 + 3 + 1 + 2 + 5 = 18.
```

**Constraints**

- costs.length == n
- 1 <= n <= 105
- 1 <= costs[i] <= 105
- 1 <= coins <= 108

---

## 题目（中文翻译）

炎热的夏天，一个男孩想要购买冰淇淋棒。  
商店里共有 `n` 根冰淇淋棒。给定一个长度为 `n` 的数组 `costs`，其中 `costs[i]` 表示第 `i` 根冰淇淋棒的价格（单位：硬币）。男孩初始拥有 `coins` 枚硬币，他希望在不超过预算的前提下尽可能多地购买冰淇淋棒。  

> 注意：男孩可以以任意顺序购买冰淇淋棒。  

返回男孩在拥有 `coins` 枚硬币的情况下，能够购买的冰淇淋棒的最大数量。  
**必须使用计数排序（counting sort）来求解此问题。**

## 示例

### 示例 1
**输入**  
`costs = [1,3,2,4,1], coins = 7`  

**输出**  
`4`  

**解释**  
男孩可以购买下标为 0、1、2、4 的冰淇淋棒，总花费为 `1 + 3 + 2 + 1 = 7`。

### 示例 2
**输入**  
`costs = [10,6,8,7,7,8], coins = 5`  

**输出**  
`0`  

**解释**  
男孩没有足够的硬币购买任何一根冰淇淋棒。

### 示例 3
**输入**  
`costs = [1,6,3,1,2,5], coins = 20`  

**输出**  
`6`  

**解释**  
男孩可以购买所有冰淇淋棒，总花费为 `1 + 6 + 3 + 1 + 2 + 5 = 18`。

## 约束条件

- `costs.length == n`
- `1 <= n <= 10^5`
- `1 <= costs[i] <= 10^5`
- `1 <= coins <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有冰淇淋的价格都列出来，尝试所有可能的购买顺序，看看哪一种能买到最多的冰淇淋。  
- **数据结构**：我们只需要一个普通的 Python 列表 `costs` 来保存每根冰淇淋的价格。可以把它想象成超市里摆放的商品价格标签，标签上写的数字就是 “价格”。  
- **为什么正确**：只要遍历到一种合法的购买顺序（总花费不超过 `coins`），我们就能得到这一次能买到的冰淇淋数量。把所有顺序都尝试完后，最大值必然就是答案。  
- **时间/空间复杂度**：遍历所有排列的时间是 `O(n!)`（阶乘），这在 n=10⁵ 时根本不可能完成。空间只用了原数组 `O(1)`，但时间远远超出限制。这里用大白话解释：`O(n!)` 就像把 10⁵ 根冰棍全部排成每一种可能的顺序，根本不可能在地球上完成。

#### 代码（Python）

```python
import itertools

def maxIceCream_bruteforce(costs, coins):
    """
    暴力遍历所有购买顺序（仅作思想展示，实际不可用）。
    """
    n = len(costs)
    best = 0
    # itertools.permutations 会产生所有排列
    for order in itertools.permutations(range(n)):
        spent = 0          # 已经花掉的硬币数
        cnt   = 0          # 已买的冰棍数量
        for idx in order:
            if spent + costs[idx] > coins:   # 超预算，停止当前排列
                break
            spent += costs[idx]
            cnt   += 1
        best = max(best, cnt)   # 更新最大值
    return best
```

#### 复杂度

- **时间复杂度**：`O(n!)` —— 随着冰棍数量的增加，排列数呈指数级增长，根本不可接受。  
- **空间复杂度**：`O(1)` —— 只用了常数级别的额外空间（不计递归栈和 `itertools` 的内部实现）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**“先买最便宜的”** 永远不会让我们错过更好的解。因为如果我们把一根贵的冰棍提前买了，必然会浪费更多的硬币，导致后面能买的数量变少。于是我们把问题转化为：

> 在所有价格中，按从小到大依次挑选，直到钱花光为止，挑了多少根？

这一步只需要把价格从小到大排序，然后线性扫描即可。**但是** 题目要求使用**计数排序**（Counting Sort）来实现 O(n + max(cost)) 的时间。

**计数排序的核心思想**：

- 把所有可能的价格（这里最高不超过 10⁵）看成“桶”，每个桶记录该价格出现的次数。想象成一本超市的“价格目录”，第 `i` 页上写着价格为 `i` 的商品有多少个。
- 先遍历 `costs` 把每个价格放进对应的桶（`cnt[price] += 1`），这一步是 O(n)。
- 再从最小的价格开始，尽可能多地买同价位的冰棍：如果当前价位的冰棍数量 `cnt[p]` 大于我们还能买的数量 `coins // p`，只买够钱的那几根就可以结束；否则把这一价位的所有冰棍都买掉，扣除相应的硬币，继续检查更贵的价位。

这样我们只遍历了一遍价格区间（最多 10⁵），时间是 **O(n + max(cost))**，空间是 **O(max(cost))**（用来存桶）。

#### 代码（Python）

```python
def maxIceCream(costs, coins):
    """
    计数排序 + 贪心
    1. 统计每个价格出现的次数（桶）
    2. 从最小价格开始，尽可能多买
    """
    MAX_COST = 100000               # 题目给出的价格上限
    cnt = [0] * (MAX_COST + 1)      # 桶数组，cnt[p] 表示价格为 p 的冰棍有多少根

    # 统计出现次数，等价于把每根冰棍放进对应的“价格页”
    for c in costs:
        cnt[c] += 1

    bought = 0                      # 已经买的冰棍数量
    # 从最便宜的价格（1）遍历到最贵的价格（MAX_COST）
    for price in range(1, MAX_COST + 1):
        if cnt[price] == 0:
            continue                # 该价格没有冰棍，跳过
        if coins < price:           # 钱已经不足以买当前价位的第一根，直接结束
            break

        # 能买的最多根数 = min(该价位数量, 还能买的根数)
        # 还能买的根数 = coins // price （整除得到还能买几根同价位的）
        max_can_buy = coins // price
        take = min(cnt[price], max_can_buy)

        bought += take               # 累加买到的根数
        coins -= take * price        # 扣除相应的硬币

        # 如果已经把当前价位的所有冰棍都买完，继续往后走；
        # 如果钱已经花光（coins == 0），后面的循环自然会因为 coins < price 而提前结束
    return bought
```

#### 复杂度

- **时间复杂度**：`O(n + C)`，其中 `n` 是冰棍数量，`C = max(costs) ≤ 10⁵` 是价格上限。  
  - 大白话：我们只需要一次遍历所有冰棍（把它们放进“价格目录”），再一次遍历所有可能的价格（最多十万次），两次线性扫描，速度非常快。
- **空间复杂度**：`O(C)`，即额外使用一个大小为 `max(costs)+1` 的数组作桶。  
  - 大白话：这相当于在超市里准备了十万页的价格目录，页数固定不随冰棍数量变化。

---

## 心得

- **核心技巧**：先排序（这里用计数排序）再贪心，从最小价格开始购买。  
- **适用题型**：  
  1. “买最多的物品” 类题，如 **Maximum Number of Toys**、**Maximum Dungeons**（在可排序的资源上使用贪心）。  
  2. 需要在 **O(n + maxVal)** 时间内完成的计数排序场景，如 **Sort Colors**（颜色计数）或 **Frequency Sort**。  
- **一句话总结**：**“先把最便宜的装进购物车，钱用光为止”**。

---

## 反思

- **第一反应**：看到“买尽可能多的冰棍”，立刻想到把价格从小到大排序，然后逐个累加。  
- **最容易踩的坑**：  
  - 忘记检查 **硬币不足以买当前价位的第一根** 时要提前结束，否则会出现无限循环或错误计数。  
  - 计数排序的桶大小一定要覆盖所有可能的价格（这里是 10⁵），否则会出现索引越界。  
- **下次类似题的第一步**：先判断是否可以用 **计数排序**（即数值范围不大）把 “排序” 步骤压到 O(n)；随后直接 **贪心** 选最小的子集。