# #1475. 商店中带有特殊折扣的最终价格 / Final Prices With a Special Discount in a Shop

> 难度：简单 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/)

---

## 题目（英文原版）

**Description**

You are given an integer array prices where prices[i] is the price of the ith item in a shop.
There is a special discount for items in the shop. If you buy the ith item, then you will receive a discount equivalent to prices[j] where j is the minimum index such that j > i and prices[j] <= prices[i]. Otherwise, you will not receive any discount at all.
Return an integer array answer where answer[i] is the final price you will pay for the ith item of the shop, considering the special discount.

**Examples**

**Example 1:**

```
Input: prices = [8,4,6,2,3]
Output: [4,2,4,2,3]
Explanation: 
For item 0 with price[0]=8 you will receive a discount equivalent to prices[1]=4, therefore, the final price you will pay is 8 - 4 = 4.
For item 1 with price[1]=4 you will receive a discount equivalent to prices[3]=2, therefore, the final price you will pay is 4 - 2 = 2.
For item 2 with price[2]=6 you will receive a discount equivalent to prices[3]=2, therefore, the final price you will pay is 6 - 2 = 4.
For items 3 and 4 you will not receive any discount at all.
```

**Example 2:**

```
Input: prices = [1,2,3,4,5]
Output: [1,2,3,4,5]
Explanation: In this case, for all items, you will not receive any discount at all.
```

**Example 3:**

```
Input: prices = [10,1,1,6]
Output: [9,0,1,6]
```

**Constraints**

- 1 <= prices.length <= 500
- 1 <= prices[i] <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 (integer array) `prices`，其中 `prices[i]` 表示商店中第 `i` 件商品的原价。  
商店对商品提供一种特殊折扣：如果你购买第 `i` 件商品，则可以获得等同于 `prices[j]` 的折扣，其中 `j` 是满足 `j > i` 且 `prices[j] <= prices[i]` 的 **最小下标** (minimum index)。如果不存在这样的 `j`，则你无法获得任何折扣。  
返回一个整数数组 `answer`，其中 `answer[i]` 为考虑上述特殊折扣后你需要支付的第 `i` 件商品的最终价格。

**示例**  

*示例 1*  
```
输入: prices = [8,4,6,2,3]
输出: [4,2,4,2,3]
解释:
- 对于商品 0，price[0]=8，你将获得等同于 price[1]=4 的折扣，最终支付 8 - 4 = 4。
- 对于商品 1，price[1]=4，你将获得等同于 price[3]=2 的折扣，最终支付 4 - 2 = 2。
- 对于商品 2，price[2]=6，你将获得等同于 price[3]=2 的折扣，最终支付 6 - 2 = 4。
- 对于商品 3，price[3]=2，没有满足条件的后续商品，故不受折扣，最终支付 2。
- 对于商品 4，price[4]=3，同上，最终支付 3。
```

*示例 2*  
```
输入: prices = [1,2,3,4,5]
输出: [1,2,3,4,5]
解释: 对所有商品均不存在满足条件的后续商品，因此均不受折扣，最终价格保持不变。
```

*示例 3*  
```
输入: prices = [10,1,1,6]
输出: [9,0,1,6]
解释:
- 商品 0 的折扣为 price[1]=1，最终支付 10 - 1 = 9。
- 商品 1 的折扣为 price[2]=1，最终支付 1 - 1 = 0。
- 商品 2 没有后续更小或相等的商品，最终支付 1。
- 商品 3 同理，最终支付 6。
```

**约束条件**  
- `1 <= prices.length <= 500`  
- `1 <= prices[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**对每个商品 i，顺着后面的商品找第一个满足 `prices[j] ≤ prices[i]` 的 j**，然后把 `prices[j]` 当作折扣减掉。如果后面再也找不到满足条件的商品，就不打折，直接把原价保留下来。

- **用到的数据结构**：只需要一个普通的 Python 列表 `prices`，以及遍历时产生的临时变量 `j`。可以把它想象成在超市里**从左往右排队的商品**，我们站在第 i 件商品前面，往后面看，直到看到一个“不贵于”当前商品的商品，就把它的价格当作优惠券。  
- **为什么正确**：题目要求的折扣恰好是**最近的、价格不高于当前商品的后续商品**。暴力遍历恰好逐一检查了所有后面的商品，必然能找到满足条件的最小下标 j（如果有的话），于是得到的折扣必然是题目要求的折扣。  
- **时间/空间复杂度**：  
  - 对每个 `i`（最多 `n` 次）都要向后遍历一次，最坏情况下会遍历到数组末尾（大约 `n/2` 次平均），所以总共大约是 `n × n = n²` 次比较。  
  - 空间上只用了常数个额外变量（结果数组除外），所以是 **O(1)**（不计答案数组）。

> **大白话解释**：  
> - **O(n²)** 就像你让每个人都去检查后面所有人一次，人数多了检查的次数会呈“平方”增长。  
> - **O(1)** 则是说除了输入和输出外，你几乎不需要额外的存储空间。

#### 代码（Python）

```python
def finalPrices(prices):
    """
    暴力解：对每个商品 i，向后找第一个满足条件的商品 j
    """
    n = len(prices)
    ans = prices[:]                     # 先把原价复制一遍作为初始答案
    for i in range(n):                  # 遍历每件商品
        discount = 0                     # 默认没有折扣
        for j in range(i + 1, n):        # 在 i 之后的商品里寻找
            if prices[j] <= prices[i]:   # 找到第一个不贵于 i 的商品
                discount = prices[j]     # 折扣就是它的价格
                break                    # 只要找到第一个就可以停了
        ans[i] = prices[i] - discount    # 原价减去折扣（若 discount 为 0 则不变）
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 意味着如果商品数量是 100，最坏情况下要检查约 10,000 次；如果是 500（题目上限），则约 250,000 次。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了几个临时变量 `i, j, discount`，不随 `n` 增长而增长。

---

### 2. 最优解

#### 思路  
暴力解的慢点在于**每次都要向后线性扫描**，这相当于“重复劳动”。我们可以把**“寻找下一个不大于当前元素的位置”**这个过程一次性完成，利用 **单调栈（Monotonic Stack）**。

**单调栈的核心思想**  
- 栈里保存的是**下标**，且对应的 `prices` 值从栈底到栈顶 **单调递增**（即栈顶的元素是当前已看到的最小的）。  
- 当我们遍历数组时，如果当前价格 `prices[i]` 小于等于栈顶对应的价格，就说明 **栈顶的商品找到了它的折扣**（因为当前 i 是栈顶商品右侧第一个不大于它的商品）。于是可以立刻把折扣算出来并弹出栈顶。  
- 这样每个下标只会 **入栈一次、出栈一次**，总操作次数是 `2n`，时间线性。

**类比**：想象一条生产线，前面的商品如果比后面的大，就会被后面的“小商品”“抢先折扣”。我们把还没有找到折扣的商品放进一个“等待队列”（栈），当出现一个更便宜的商品时，就立即为队列里所有比它贵的商品提供折扣。

**步骤**  
1. 初始化一个空栈 `stack = []`，用来存放还未确定折扣的商品下标。  
2. 依次遍历 `prices`（下标 `i` 从左到右）：  
   - 当栈不为空且 `prices[i] <= prices[stack[-1]]` 时，说明 `i` 是栈顶商品的折扣。弹出栈顶 `idx = stack.pop()`，并把 `prices[idx] -= prices[i]`。  
   - 循环上述步骤，直到栈为空或当前价格大于栈顶对应的价格。  
   - 最后把当前下标 `i` 入栈 `stack.append(i)`，表示它自己还在等待更便宜的后续商品。  
3. 遍历结束后，栈里剩下的下标表示没有找到折扣的商品，答案已经是原价（因为我们只在找到折扣时才修改）。直接返回 `prices`（已经在原数组上就地修改）。

**为什么正确**  
- 栈的 **单调递增** 保证了栈中下标对应的价格从左到右严格递增。  
- 当出现一个更小或相等的价格 `prices[i]` 时，它必然是栈顶（最左侧、最靠近的）商品的第一个满足 `prices[j] ≤ prices[idx]` 的 `j`，因为所有在它左边且更大的商品已经在栈中排好队，且没有更小的商品介入。  
- 因此每次弹出栈顶并计算折扣，恰好满足题目对“最小下标 j”的要求。

#### 代码（Python）

```python
def finalPrices(prices):
    """
    单调栈解法：一次遍历完成所有折扣的寻找
    """
    stack = []                     # 用来存放“还未找到折扣”的商品下标
    for i, price in enumerate(prices):
        # 当前价格比栈顶对应的价格小（或相等）时，栈顶商品找到了折扣
        while stack and price <= prices[stack[-1]]:
            idx = stack.pop()                 # 弹出需要打折的商品下标
            prices[idx] -= price              # 原价减去折扣
        stack.append(i)                       # 当前商品加入等待队列
    # 栈中剩余的下标代表没有折扣的商品，prices 已经是最终答案
    return prices
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个下标最多入栈一次、出栈一次，整个过程只做了线性次数的比较和赋值。相比暴力的 `O(n²)`，即使 `n=500`，也只需要约 1,000 次操作，几乎是瞬间完成。  
- **空间复杂度**：`O(n)`（最坏情况下栈里会存全部下标）  
  - 这相当于额外用了一个长度不超过 `n` 的列表来保存“等待折扣”的商品。对 500 条数据来说也非常小。

---

## 心得

- **核心技巧**：**单调栈**（Monotonic Stack），用于快速找到每个元素右侧第一个满足 “不大于” 条件的元素。  
- **适用的题型**（类似）  
  1. *每日温度*（LeetCode 739）——找右侧第一个更高的温度。  
  2. *柱状图中最大的矩形*（LeetCode 84）——利用单调栈求每根柱子左右最近更低的柱子。  
  3. *车队*（LeetCode 853）——单调栈帮助判断何时形成车队。  
- **一句话总结解题钥匙**：**把“向后找第一个满足条件的元素”转化为“用单调栈一次遍历完成”。**

---

## 反思

- **第一反应**：直接写两层循环，逐个向后搜索。因为这最容易想到，且不需要额外的数据结构。  
- **最容易踩的坑**  
  - 忘记“≤”而写成 `<`，会导致相等的商品不被当作折扣，从而得到错误答案。  
  - 在暴力实现中忘记把 `discount` 初始化为 `0`，导致未找到折扣时仍使用了上一次的折扣值。  
  - 单调栈实现时如果把 `price < prices[stack[-1]]` 写成 `price > …`，逻辑会完全相反。  
- **下次遇到同类题的第一步**：先判断是否在“右侧”寻找“第一个满足单调关系的元素”。如果是，立刻考虑 **单调栈**（递增或递减）来把搜索过程压缩到一次遍历。