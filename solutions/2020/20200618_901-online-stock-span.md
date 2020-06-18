# #901. 股票价格跨度 / Online Stock Span

> 难度：中等 · 标签：Stack、Design、Monotonic Stack、Data Stream · [LeetCode 链接](https://leetcode.com/problems/online-stock-span/)

---

## 题目（英文原版）

**Description**

Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.
The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.
Implement the StockSpanner class:

**Examples**

**Example 1:**

```
Input
["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
[[], [100], [80], [60], [70], [60], [75], [85]]
Output
[null, 1, 1, 1, 2, 1, 4, 6]

Explanation
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // return 1
stockSpanner.next(80);  // return 1
stockSpanner.next(60);  // return 1
stockSpanner.next(70);  // return 2
stockSpanner.next(60);  // return 1
stockSpanner.next(75);  // return 4, because the last 4 prices (including today's price of 75) were less than or equal to today's price.
stockSpanner.next(85);  // return 6
```

**Constraints**

- 1 <= price <= 105
- At most 104 calls will be made to next.

---

## 题目（中文翻译）

设计一种算法，用于收集某只股票的每日价格报价（daily price quotes），并返回该股票在当前日期的价格跨度（span）。  
某一天的价格跨度是指从该天开始向前（即往过去）连续的天数的最大值，这些天的股票价格均 **小于或等于** 当天的价格。

实现 `StockSpanner` 类，使其能够高效地处理上述查询。

## 示例

```text
输入
["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
[[], [100], [80], [60], [70], [60], [75], [85]]
输出
[null, 1, 1, 1, 2, 1, 4, 6]
```

**解释**

```java
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // 返回 1
stockSpanner.next(80);  // 返回 1
stockSpanner.next(60);  // 返回 1
stockSpanner.next(70);  // 返回 2
stockSpanner.next(60);  // 返回 1
stockSpanner.next(75);  // 返回 4，因为最近 4 天（包括当天价格 75）的价格都 ≤ 当天价格。
stockSpanner.next(85);  // 返回 6
```

## 约束

- `1 <= price <= 10^5`
- 最多会调用 `next` 方法 `10^4` 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：  
- 用一个列表 `prices` 按顺序记录每一天的股价。  
- 当调用 `next(price)` 时，先把当天的股价加入 `prices`。  
- 然后从列表的最后一个元素（今天）往前遍历，遇到 **股价 ≤ 今天的价格** 时计数，遇到 **股价 > 今天的价格** 时停止。计数的天数就是今天的 **span**。  

这就像在日历上往回数，遇到更贵的那天就停下来。  

**为什么正确**  
题目要求的 span 正是“从今天往前连续的、股价 ≤ 今天的天数”。我们逐天向后检查，恰好把所有满足条件的天数全部算进来，一旦出现更贵的天，说明再往前的天已经不连续了，应该停止。  

**复杂度分析（大白话）**  
- 对每一次 `next`，我们最坏要把已经记录的所有股价都遍历一遍。  
- 假设第 `i` 次调用时已经有 `i‑1` 天的价格，那么这一次最坏需要检查 `i‑1` 天。  
- 把所有调用加在一起，就是 1 + 2 + … + N ≈ N²/2，时间复杂度记作 **O(N²)**（N 为总调用次数）。  
- 我们只用了一个列表保存所有价格，空间随调用次数线性增长，记作 **O(N)**。  

#### 代码（Python）  

```python
class StockSpanner:
    def __init__(self):
        # 用列表保存所有历史股价，类似一本“股价日记”
        self.prices = []

    def next(self, price: int) -> int:
        """
        返回今天的 span，同时把 price 加入历史记录
        """
        self.prices.append(price)          # 记录今天的价格
        span = 1                           # 至少包括今天自己

        # 从今天往前检查，直到遇到更高的价格为止
        idx = len(self.prices) - 2         # 前一天的下标
        while idx >= 0 and self.prices[idx] <= price:
            span += 1                      # 满足条件，span 加 1
            idx -= 1                       # 继续往前看

        return span
```

#### 复杂度  

- **时间复杂度：O(N)**（单次调用），累计 O(N²)。  
  *大白话*：每次都要把已经写好的“日记”往回翻，翻的页数会越来越多。  
- **空间复杂度：O(N)**。  
  *大白话*：我们把所有出现过的价格都保存在一个列表里，列表会随调用次数增长。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每次都要往回遍历**，当价格连续上升时会产生大量重复工作。  
我们可以把“已经不可能再被后面的更大价格覆盖的天” **提前剔除**，这样每一次只处理**真正需要比较的**天数。  

这正好可以用 **单调栈（Monotonic Stack）** 来实现：  

1. **栈里保存的是「递减」的价格**，即栈底的价格最大，栈顶的价格最小。  
2. 每当来一个新价格 `price`，我们把栈顶所有 **≤ price** 的元素全部弹出。因为这些天的价格都不比今天高，今天的 span 一定会把它们“合并进来”。  
3. 弹出的同时，把它们对应的 span 累加到今天的 span。  
4. 最后把 `(price, span)` 这对信息压入栈中，供以后更大的价格使用。  

> **类比**：想象把每一天的价格装进一个盒子，盒子里只能放比下面的盒子更小（或相等）的价格。新来的盒子如果比栈顶的盒子大，就把栈顶的盒子全部搬走（因为它们已经被新盒子“覆盖”），把它们的大小（span）累加到新盒子上，然后把新盒子放进去。这样栈始终保持递减顺序，查询时只需要看栈顶，省掉了大量遍历。

**为什么正确**  
- 当我们弹出所有 ≤ 当前价格的栈顶元素时，等价于把这些天的 span 合并到今天，因为它们之间没有更大的价格阻断。  
- 栈中留下的元素一定都是 **> 当前价格**，这正是今天的 span 结束的地方（第一个更贵的过去的天）。  
- 每个价格只会被 **压入一次、弹出一次**，所以整体上只遍历了 O(N) 次。  

#### 代码（Python）  

```python
class StockSpanner:
    def __init__(self):
        # 栈中保存 (price, span) 元组，price 为当天股价，span 为该价格的跨度
        self.stack = []   # 类似“一叠递减的盒子”

    def next(self, price: int) -> int:
        """
        返回今天的 span，同时维护单调递减栈
        """
        span = 1  # 今天本身算 1 天

        # 弹出所有价格 <= 当前价格的盒子，累加它们的 span
        while self.stack and self.stack[-1][0] <= price:
            # stack[-1][1] 是被弹出盒子的跨度
            span += self.stack[-1][1]
            self.stack.pop()          # 把它们“搬走”

        # 把当前价格和它的跨度压入栈中，供以后使用
        self.stack.append((price, span))
        return span
```

#### 复杂度  

- **时间复杂度：O(1)（摊销）**。  
  *大白话*：虽然在一次调用里可能会弹出多个元素，但每个元素一旦弹出以后就再也不会出现了。所有弹出操作加起来最多也是 N 次，所以平均到每次调用上就是常数时间。  
- **空间复杂度：O(N)**。  
  *大白话*：栈里最多保存所有历史价格的副本（每个价格只会在栈中出现一次），最坏情况是价格严格递减，此时栈的大小等于调用次数。  

---

## 心得  

- **核心技巧**：**单调栈**（Monotonic Stack），把“递减”或“递增”的约束直接体现在数据结构上，能够在一次遍历中完成本来需要多次遍历的工作。  
- **适用的题型**（类似思路）：  
  1. **每日温度**（739. Daily Temperatures）——寻找右侧第一个更高的温度。  
  2. **柱状图中最大的矩形**（84. Largest Rectangle in Histogram）——利用单调栈求每根柱子的左右边界。  
  3. **接雨水**（42. Trapping Rain Water）——也可以用单调栈求每个位置的左右最高柱子。  
- **一句话总结**：  
  “把“向左/向右寻找更大（或更小）元素”的过程，用递减（递增）栈一次性搞定，既省时又省力。”  

---

## 反思  

- **第一反应**：直接把所有历史价格保存下来，遇到新价格就往回遍历——这就是暴力思路。  
- **最容易踩的坑**：  
  - **边界条件**：第一次调用时栈为空，需要返回 1。  
  - **相等价格的处理**：题目要求 “≤”，所以在弹出时要使用 `<=` 而不是 `<`，否则会少算相同价格的天数。  
  - **摊销分析**：虽然单次 `while` 循环看起来可能很长，但要记住每个元素最多只弹出一次，才能得出 O(1) 摊销时间。  
- **下次遇到同类题**：第一步先问自己 “有没有一种单调性（递增/递减）可以利用？”——如果答案是肯定的，立刻想到 **单调栈**，再去设计压入/弹出的规则。