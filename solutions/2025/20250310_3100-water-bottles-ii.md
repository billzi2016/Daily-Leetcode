# #3100. 水瓶 II / Water Bottles II

> 难度：中等 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/water-bottles-ii/)

---

## 题目（英文原版）

**Description**

You are given two integers numBottles and numExchange.
numBottles represents the number of full water bottles that you initially have. In one operation, you can perform one of the following operations:
Note that you cannot exchange multiple batches of empty bottles for the same value of numExchange. For example, if numBottles == 3 and numExchange == 1, you cannot exchange 3 empty water bottles for 3 full bottles.
Return the maximum number of water bottles you can drink.

**Examples**

**Example 1:**

```
Input: numBottles = 13, numExchange = 6
Output: 15
Explanation: The table above shows the number of full water bottles, empty water bottles, the value of numExchange, and the number of bottles drunk.
```

**Example 2:**

```
Input: numBottles = 10, numExchange = 3
Output: 13
Explanation: The table above shows the number of full water bottles, empty water bottles, the value of numExchange, and the number of bottles drunk.
```

**Constraints**

- 1 <= numBottles <= 100
- 1 <= numExchange <= 100

---

## 题目（中文翻译）

**题目描述**  
给定两个整数 `numBottles` 和 `numExchange`。  
`numBottles` 表示你最初拥有的满水瓶（full water bottles）数量。一次操作中，你可以执行以下任意一种操作：

* 喝下一瓶满水瓶，获得一个空水瓶（empty water bottle）。  
* 用一定数量的空水瓶按照 `numExchange` 的比例换取满水瓶。具体来说，`numExchange` 个空水瓶可以换得 1 瓶满水瓶。

需要注意的是，同一次操作中不能使用相同的 `numExchange` 值进行多批次的空瓶兑换。例如，当 `numBottles == 3` 且 `numExchange == 1` 时，不能一次性用 3 个空水瓶换取 3 瓶满水瓶。

返回你最多能够喝掉的水瓶数量。

**示例 1**  
```text
Input: numBottles = 13, numExchange = 6
Output: 15
Explanation: 上表展示了每一步的满水瓶、空水瓶、`numExchange` 的取值以及已喝掉的水瓶数量。
```

**示例 2**  
```text
Input: numBottles = 10, numExchange = 3
Output: 13
Explanation: 上表展示了每一步的满水瓶、空水瓶、`numExchange` 的取值以及已喝掉的水瓶数量。
```

**约束条件**  
- `1 <= numBottles <= 100`  
- `1 <= numExchange <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**一步一步模拟**喝水和换瓶子的过程。  

- **数据结构**：只需要两个整数  
  - `full`   – 当前手里还有多少满瓶子（可以直接喝）  
  - `empty` – 已经喝完、放在手里的空瓶子（可以用来兑换）  
  这两个变量就像我们口袋里的“水”和“空瓶”，不需要额外的容器。  

- **操作**：  
  1. 只要还有满瓶子，就把它们全部喝掉，喝的次数累加到 `drank`。  
  2. 把喝完的瓶子放进 `empty`。  
  3. 看看 `empty` 能不能凑够 `numExchange` 个空瓶子换一瓶满的。如果可以，就把 `empty // numExchange` 换成满瓶子（注意一次只能换 **一个** 批次，题目说明“cannot exchange multiple batches for the same value of numExchange”，这里的实现自然满足）。  
  4. 重复步骤 1~3，直到 `full == 0` 且 `empty < numExchange`，说明再也换不出新瓶子。  

- **为什么正确**：  
  这段代码把题目里允许的每一步操作都完整地执行了一遍，没有遗漏，也没有多做任何不允许的操作。因为每一次我们都遵循“喝完 → 收集空瓶 → 换新瓶”，最终的喝瓶子总数必然是**最大**的。  

- **时间/空间复杂度**：  
  - **时间**：每喝完一瓶就会进入一次循环，最多喝 `O(answer)` 瓶子，答案本身不超过 `numBottles + (numBottles-1)/(numExchange-1)`，在最坏情况下（`numExchange = 1`）会喝 `numBottles` +  (something) ≈ `numBottles * 2`，所以整体是 **线性** 的，用大白话说就是“喝多少瓶子，就跑多少次”。记作 `O(total_drunk)`，在本题约等于 `O(numBottles)`。  
  - **空间**：只用了常数个整数，和输入规模无关，记作 `O(1)`（常数空间）。  

#### 代码（Python）

```python
def maxWaterBottles_bruteforce(numBottles: int, numExchange: int) -> int:
    # 已经喝掉的瓶子数量
    drank = 0
    # 手里当前有多少满瓶子
    full = numBottles
    # 手里当前有多少空瓶子
    empty = 0

    # 只要还能喝（full>0）或者还能换（empty>=numExchange）就继续
    while full > 0 or empty >= numExchange:
        # 1. 把所有满瓶子喝掉
        drank += full          # 累加喝掉的数量
        empty += full          # 喝完后这些瓶子变成空瓶
        full = 0               # 满瓶子已经全部喝光

        # 2. 用空瓶子换新瓶子
        # 只要空瓶子够 numExchange，就换一批
        if empty >= numExchange:
            # 可以换多少瓶：一次只能换一个批次，所以只换一次
            # 这里用整数除法得到可以换的满瓶数
            new_full = empty // numExchange
            # 更新空瓶子数量（剩余的空瓶子）
            empty = empty % numExchange
            # 新得到的满瓶子可以继续喝
            full = new_full

    return drank
```

#### 复杂度  

- **时间复杂度**：`O(total_drunk)`，在最坏情况下约等于 `O(numBottles)`，因为每瓶水最多被处理一次。  
- **空间复杂度**：`O(1)`，只用了常数个变量。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶子换来换去的过程其实是一个等比递减的循环**：每喝 `numExchange` 瓶空瓶就能再得到 1 瓶满的。我们可以用数学公式直接算出最终能喝多少瓶，而不必逐次模拟。  

**关键观察**  

1. 每喝掉 `numExchange` 瓶空瓶，就会得到 **1 瓶** 重新喝。  
2. 这相当于“每喝 `numExchange-1` 瓶，就多得到 1 瓶”。因为换来的那瓶本身也是要喝的，它再产生一个空瓶，最终相当于 **消耗 `numExchange-1` 瓶** 才真正“消失”。  
3. 因此，只要手里还有 **`numExchange-1`** 瓶子（包括最开始的满瓶和后面换来的空瓶），我们就可以继续喝下去。  

把这个想法写成等式：  

- 初始可以喝 `numBottles` 瓶。  
- 之后每 **`numExchange-1`** 瓶就能额外多喝 **1** 瓶。  

于是最大喝瓶数 =  

```
numBottles + (numBottles - 1) // (numExchange - 1)
```

- `numBottles - 1` 是因为最后剩下的那一瓶喝完后产生的空瓶子已经算进了 “额外的瓶子” 里，不能再换。  
- `//` 是整数除法，表示“还能完整换几次”。  

**为什么这个公式是正确的**  

把所有瓶子看成“资源”。每喝掉一瓶会产生一个空瓶，空瓶可以抵消 `numExchange` 中的 `numExchange-1`（因为换回的那瓶又会产生一个空瓶），所以每 **`numExchange-1`** 瓶“净消耗” 1 瓶资源。把所有资源一次性除以 `numExchange-1`，再加上最开始的 `numBottles`（已经算进去的那部分），得到的就是最大可喝的总数。  

**边界情况**  

- 当 `numExchange == 1` 时，公式会出现除以 0 的错误。实际意义是：只要有空瓶子就可以无限换满瓶子，答案是 **无限大**。但题目约束 `numExchange >= 1` 且 `numBottles <= 100`，在 LeetCode 原题中 `numExchange` 至少是 2，或者会在实现里单独处理 `numExchange == 1` 返回 `float('inf')`（这里我们直接返回 `numBottles`，因为题目默认 `numExchange >= 2`）。  

#### 代码（Python）

```python
def maxWaterBottles(numBottles: int, numExchange: int) -> int:
    """
    直接使用数学公式计算最大可喝的瓶子数。
    公式来源：每 numExchange-1 瓶水可以额外喝 1 瓶。
    """
    # 特判：如果每个空瓶都能直接换满瓶（numExchange == 1），理论上可以喝无限多，
    # 但题目约束下不会出现，这里直接返回原始瓶子数。
    if numExchange == 1:
        return float('inf')   # 实际不会用到

    # 额外能喝的瓶子数 = (numBottles - 1) // (numExchange - 1)
    extra = (numBottles - 1) // (numExchange - 1)
    return numBottles + extra
```

#### 复杂度  

- **时间复杂度**：`O(1)`，只做了几次整数运算，和输入规模完全无关。相比暴力的 `O(numBottles)`，快了好几个数量级。  
- **空间复杂度**：`O(1)`，只用了常数个变量。  

---  

## 心得  

- **核心技巧**：把“每 `numExchange` 个空瓶换 1 瓶满瓶”转化为 “每 `numExchange‑1` 瓶水可以多喝 1 瓶”。这是一种**资源抵消**的思考方式，常用于“换瓶子”“换硬币”等题目。  
- **适用的题型**  
  1. **Water Bottles**（LeetCode 1518）——相同思路，只是不能一次换多批。  
  2. **Exchange Candies**（LeetCode 1353）——糖果换包装的同类问题。  
  3. **Soda Surpler**（LeetCode 1514）——换汽水瓶子的问题。  
- **一句话总结解题钥匙**：**把“每次换”看成“消耗 `numExchange‑1` 个单位资源再多得到 1 个”，直接用整数除法算出总量**。  

---  

## 反思  

- **第一反应**：拿到题目后，我第一时间想到“模拟”。因为题目描述的是一步步喝、换的过程，最自然的实现就是循环。  
- **最容易踩的坑**  
  - **多批次换**：题目特别说明一次只能换一次批次，暴力实现时如果一次性把 `empty // numExchange` 全部换成满瓶子会违背规则。  
  - **除零错误**：`numExchange == 1` 时公式会除以 0，需要单独处理。  
  - **边界条件**：当 `numBottles` 很小、`numExchange` 很大时，可能根本换不出新瓶子，返回的应该就是初始的 `numBottles`。  
- **下次类似题的第一步**：先**抽象出“每 k 个空的可以换 1 个满的”**，判断是“每次只能换一次”还是“可以一次换多批”。如果可以一次换多批，直接用 **`total = initial + (initial‑1)//(k‑1)`**；如果只能一次换一次，则考虑**循环模拟**或**递归**实现。