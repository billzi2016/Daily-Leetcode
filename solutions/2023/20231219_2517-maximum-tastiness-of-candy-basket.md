# #2517. 糖果篮的最大美味度 / Maximum Tastiness of Candy Basket

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-tastiness-of-candy-basket/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers price where price[i] denotes the price of the ith candy and a positive integer k.
The store sells baskets of k distinct candies. The tastiness of a candy basket is the smallest absolute difference of the prices of any two candies in the basket.
Return the maximum tastiness of a candy basket.

**Examples**

**Example 1:**

```
Input: price = [13,5,1,8,21,2], k = 3
Output: 8
Explanation: Choose the candies with the prices [13,5,21].
The tastiness of the candy basket is: min(|13 - 5|, |13 - 21|, |5 - 21|) = min(8, 8, 16) = 8.
It can be proven that 8 is the maximum tastiness that can be achieved.
```

**Example 2:**

```
Input: price = [1,3,1], k = 2
Output: 2
Explanation: Choose the candies with the prices [1,3].
The tastiness of the candy basket is: min(|1 - 3|) = min(2) = 2.
It can be proven that 2 is the maximum tastiness that can be achieved.
```

**Example 3:**

```
Input: price = [7,7,7,7], k = 2
Output: 0
Explanation: Choosing any two distinct candies from the candies we have will result in a tastiness of 0.
```

**Constraints**

- 2 <= k <= price.length <= 105
- 1 <= price[i] <= 109

---

## 题目（中文翻译）

给定一个正整数数组 `price`，其中 `price[i]` 表示第 `i` 颗糖果的价格，以及一个正整数 `k`。  
商店出售由 **k** 种不同糖果组成的篮子。  
糖果篮的 **美味度**（tastiness）定义为篮子中任意两颗糖果价格的绝对差的最小值。  
返回能够得到的最大美味度。

## 示例

### 示例 1
**输入**  
```
price = [13,5,1,8,21,2], k = 3
```
**输出**  
```
8
```
**解释**  
选择价格为 `[13,5,21]` 的三颗糖果。  
糖果篮的美味度为：`min(|13 - 5|, |13 - 21|, |5 - 21|) = min(8, 8, 16) = 8`。  
可以证明，8 是能够达到的最大美味度。

### 示例 2
**输入**  
```
price = [1,3,1], k = 2
```
**输出**  
```
2
```
**解释**  
选择价格为 `[1,3]` 的两颗糖果。  
糖果篮的美味度为：`min(|1 - 3|) = 2`。  
可以证明，2 是能够达到的最大美味度。

### 示例 3
**输入**  
```
price = [7,7,7,7], k = 2
```
**输出**  
```
0
```
**解释**  
任意挑选两颗不同的糖果，它们的价格相同，导致美味度为 `0`。

## 约束条件
- `2 <= k <= price.length <= 10^5`
- `1 <= price[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的 k 只糖果组合枚举出来**，计算每个组合的“可口度”（tastiness），取最大值。

- **枚举组合**：可以使用 `itertools.combinations` 把 `price` 列表中任意挑选 `k` 个位置的所有组合列出来。  
- **计算可口度**：对每个组合，遍历所有两两之间的价格差，取最小的那个差值（因为可口度定义为“任意两只糖果价格差的最小值”）。  
- **取最大**：把所有组合得到的可口度放进一个列表，最后返回最大的那个。

> **类比**：把每种挑选方式想成一次“聚会”，每次聚会里大家的“亲密度”取最远的两个人之间的距离（最小差），我们想找一次最“热闹”的聚会（最大最小距离）。

这个办法**一定正确**，因为我们遍历了所有合法的挑选方式，最大值自然就是答案。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maximum_tastiness_brute(price: List[int], k: int) -> int:
    # 记录全局最大可口度
    best = 0
    # 遍历所有挑选 k 只糖果的组合
    for combo in combinations(price, k):
        # 计算当前组合的可口度：所有两两差值的最小值
        min_diff = float('inf')
        # 两层循环遍历组合中的每一对糖果
        for i in range(k):
            for j in range(i + 1, k):
                diff = abs(combo[i] - combo[j])
                if diff < min_diff:
                    min_diff = diff
        # 更新全局最大值
        if min_diff > best:
            best = min_diff
    return best
```

> **关键行中文注释**已写在代码里，方便阅读。

#### 复杂度

- **时间复杂度**：  
  枚举所有 `C(n, k)`（即从 `n` 个糖果中挑 `k` 个的组合数）种可能，每个组合内部要遍历 `k·(k-1)/2` 对糖果求差。  
  用大白话说，就是“**组合数乘以 k²**”。在最坏情况下（比如 `n=10⁵, k≈n/2`）这根本不可行，实际会超时。  
  用符号写就是 `O( C(n, k) * k² )`，这远远大于 `10⁸`，所以不可接受。

- **空间复杂度**：  
  只用了常数级别的额外空间（存放几个临时变量），即 `O(1)`。  

> 暴力解虽然概念最清晰，但在数据量大时会“卡死”，所以我们需要更聪明的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有组合是瓶颈**。我们需要一种方式，在不枚举的前提下判断是否能得到“可口度 ≥ X”。如果能判断，那么就可以用**二分搜索**去找最大的 X。

**核心观察**：

1. 把糖果价格从小到大排序。  
2. 假设我们已经决定了目标可口度 `x`（即每两只糖果的价格差至少要 `x`），我们能否挑出 `k` 只糖果？  
3. 采用**贪心**：从左到右扫描，第一次把最左边的糖果放进篮子（记作 `last`），随后只要当前糖果的价格与 `last` 的差 ≥ `x`，就把它也放进篮子，并把 `last` 更新为当前糖果。这样挑出来的每两个相邻糖果之间的差都 ≥ `x`，所以任意两只之间的差也 ≥ `x`（因为它们的价格是递增的）。  
4. 如果最终挑到的糖果数量 ≥ `k`，说明“可口度 ≥ x”是可行的；否则不可行。

有了“可行性检查”函数 `can(x)`，我们就可以在答案的取值范围 `[0, max(price)-min(price)]` 上二分搜索最大满足 `can(x)` 的 `x`。

**为什么二分搜索有效？**  
可口度的取值是单调的：如果 `x` 可行，那么所有小于 `x` 的值也必然可行（因为放宽要求更容易实现）。这正好符合二分搜索的前提——**单调性**。

#### 具体步骤

1. **排序** `price` → `sorted_price`（O(n log n)）。  
2. **二分搜索**  
   - `low = 0`（最小可能的可口度）  
   - `high = sorted_price[-1] - sorted_price[0]`（最大可能的差）  
   - while `low < high`：取中点 `mid = (low + high + 1) // 2`（上取整防止死循环）。  
   - 调用 `can(mid)`：如果可以挑到 `k` 只，则 `low = mid`（尝试更大），否则 `high = mid - 1`。  
3. 循环结束后 `low` 即为答案。

#### 代码（Python）

```python
from typing import List

def maximum_tastiness(price: List[int], k: int) -> int:
    # 1️⃣ 先把价格从小到大排好序
    price.sort()
    
    # 2️⃣ 定义检查函数：给定阈值 x，能否挑到 k 只糖果？
    def can(x: int) -> bool:
        # 已经挑进去的最后一只糖果的价格
        last = price[0]          # 先把最左边的糖果放进篮子
        cnt = 1                  # 已经挑了 1 只
        # 从第二只开始遍历
        for p in price[1:]:
            if p - last >= x:    # 与上一次挑的差够大，就可以再挑一个
                cnt += 1
                last = p
                if cnt >= k:    # 提前返回，省时间
                    return True
        return cnt >= k

    # 3️⃣ 二分搜索最大可行的 x
    low, high = 0, price[-1] - price[0]   # 差值的可能范围
    while low < high:
        mid = (low + high + 1) // 2       # 取上中点，防止死循环
        if can(mid):
            low = mid                     # mid 可行，尝试更大
        else:
            high = mid - 1                # mid 不行，缩小上界
    return low
```

**代码要点解释**：

- `price.sort()`：把糖果价格排成从小到大的“队列”，相邻的差最小，方便贪心。  
- `can(x)`：只要两次挑选的价格差 ≥ `x`，后面的糖果自然也满足（因为顺序递增）。  
- `while low < high` + `mid = (low + high + 1)//2`：使用上取整可以保证 `low` 能够向右移动，防止出现 `low` 永远不变的死循环。  
- `if cnt >= k: return True`：一旦满足 k，只要返回即可，不必继续遍历全部数组，提升效率。

#### 复杂度

- **时间复杂度**：  
  - 排序 `O(n log n)`（`n = len(price)`）。  
  - 二分搜索的循环次数是 `log₂(range)`，这里的 `range` 最多是 `10⁹`（价格最大差），约 `30` 次。每次检查 `can(x)` 只需要一次线性扫描 `O(n)`。  
  - 综合起来是 `O(n log n + n log MaxDiff)`，在最坏情况下约等于 `O(n log n)`（因为 `log MaxDiff` 只有常数级别的 30）。对 `n=10⁵` 完全可接受。  

- **空间复杂度**：  
  - 只用了原数组的排序（原地）和若干常数级变量，`O(1)` 额外空间。  

> 与暴力解相比，时间从指数级降到了 **线性对数级**，大幅提升。

---

## 心得

- **核心技巧**：**单调性 + 二分搜索 + 贪心检查**。  
- **适用场景**：  
  1. “在满足某个最小/最大条件的前提下，求最大的/最小的数值”。例如  
     - *Maximum Distance Between Same Elements*（求最大距离）  
     - *Find the Smallest Divisor Given a Threshold*（阈值下的最小除数）  
  2. “在排序后，用间隔约束挑选子集”。例如  
     - *Aggressive Cows*（放牛）  
     - *Maximum Number of K-Adjacent Intervals*（间隔选择）  

- **一句话总结解题钥匙**：**把“可口度 ≥ x”转化为“能否在排序后按间隔 ≥ x 选到 k 个”，再用二分搜索找最大的 x**。

---

## 反思

- **第一反应**：直接想遍历所有组合，没意识到可以把“最小差”转化为“间隔约束”。  
- **最容易踩的坑**：  
  - 忘记先排序，导致贪心检查不成立。  
  - 二分搜索的边界写错（上取整 vs 下取整），会出现无限循环或错失答案。  
  - `can(x)` 中忘记提前返回 `True`，导致不必要的完整遍历，影响性能。  
- **下次类似题目**：第一步先判断**是否有单调性**，如果有，就立刻考虑**二分搜索 + 可行性检查**，检查函数往往可以用**排序 + 贪心**来实现。