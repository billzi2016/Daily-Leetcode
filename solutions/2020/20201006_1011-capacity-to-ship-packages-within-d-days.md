# #1011. 在 D 天内运送包裹的船舶容量 / Capacity To Ship Packages Within D Days

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

---

## 题目（英文原版）

**Description**

A conveyor belt has packages that must be shipped from one port to another within days days.
The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

**Examples**

**Example 1:**

```
Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.
```

**Example 2:**

```
Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4
```

**Example 3:**

```
Input: weights = [1,2,3,1,1], days = 4
Output: 3
Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1
```

**Constraints**

- 1 <= days <= weights.length <= 5 * 104
- 1 <= weights[i] <= 500

---

## 题目（中文翻译）

**题目描述**  
传送带（conveyor belt）上有若干包裹需要在 `days` 天内从一个港口运送到另一个港口。第 `i` 个包裹的重量为 `weights[i]`。每天我们按照 `weights` 中给出的顺序将若干包裹装上船，但装载的总重量不能超过船的最大承载重量（capacity）。  

返回能够在 `days` 天内将所有包裹全部运完的 **最小** 最大承载重量（capacity）。

**示例**  

*示例 1*  
```text
输入: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
输出: 15
解释: 最大承载重量为 15 时可以在 5 天内完成运输，具体安排如下:
第 1 天: 1, 2, 3, 4, 5
第 2 天: 6, 7
第 3 天: 8
第 4 天: 9
第 5 天: 10

注意必须保持原始顺序，不能像 (2,3,4,5), (1,6,7), (8), (9), (10) 这样重新分割包裹。
```

*示例 2*  
```text
输入: weights = [3,2,2,4,1,4], days = 3
输出: 6
解释: 最大承载重量为 6 时可以在 3 天内完成运输，具体安排如下:
第 1 天: 3, 2
第 2 天: 2, 4
第 3 天: 1, 4
```

*示例 3*  
```text
输入: weights = [1,2,3,1,1], days = 4
输出: 3
解释:
第 1 天: 1
第 2 天: 2
第 3 天: 3
第 4 天: 1, 1
```

**约束条件**  

- `1 <= days <= weights.length <= 5 * 10^4`
- `1 <= weights[i] <= 500`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的船舱容量都枚举一遍**，然后看哪一个容量能够在 `days` 天内把所有包裹运完，取最小的那个。  

- **枚举范围**：  
  - **下界**：船的容量不可能小于单个最重的包裹，否则这件包根本装不下。下界就是 `max(weights)`，就像字典里查单词时，最短的词长度是下限。  
  - **上界**：如果船一次能装下所有包裹，那只需要一天就能完成。上界就是所有重量的总和 `sum(weights)`，相当于把整个字典一次性背完。  

- **验证一个容量**：  
  按顺序把包裹装上船，每天装的重量累计不超过当前容量；一旦再装下一个包会超重，就**结束这一天**，换到第二天继续装。这样模拟完所有包裹后，看用了多少天。如果天数 ≤ `days`，说明这个容量是可行的。  

- **为什么正确**：  
  我们把**所有可能的容量**都检查了一遍，只要找到一个可行的，就说明它真的可以在 `days` 天内完成。最小的可行容量自然就是答案。  

- **复杂度大概是**：  
  - 枚举的容量数目 ≈ `sum(weights) - max(weights) + 1`（可能非常大）。  
  - 每次验证需要遍历一次数组 `weights`（长度 `n`）。  
  所以总时间复杂度是 **O(n · range)**，在最坏情况下相当于 **O(n · sum(weights))**。  
  空间上只用了常数级的变量，**O(1)**。  

> **大白话解释**：  
> 如果把 `O(n²)` 想成“把 n 本书每本都和每本书比较一次”，那么这里的 `O(n · sum)` 就像“把 n 本书分别和一大堆不同的背包容量（可能上万次）比较一次”。显然会很慢。  

#### 代码（Python）  

```python
def shipWithinDays_bruteforce(weights, days):
    """
    暴力枚举所有可能的船舱容量，返回最小可行容量
    """
    lo = max(weights)               # 下界：最重的包
    hi = sum(weights)               # 上界：全部装在一起

    # ---------- 判断容量 capacity 是否可行 ----------
    def can_ship(capacity):
        used_days = 1                # 从第 1 天开始
        cur_load = 0                # 当天已经装的重量

        for w in weights:           # 按顺序装每个包
            if cur_load + w > capacity:   # 超重了，换天
                used_days += 1
                cur_load = 0
            cur_load += w            # 把当前包装上船
        return used_days <= days    # 用的天数不超过限制即可

    # ---------- 暴力枚举 ----------
    ans = hi
    for cap in range(lo, hi + 1):   # 从最小可能容量一直往上试
        if can_ship(cap):
            ans = cap
            break                    # 第一个可行的就是最小的
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n · (range))`，其中 `range = sum(weights) - max(weights) + 1`。  
  换句话说，遍历一次数组的代价是 `n`，我们要对每一个可能的容量都做一次这样的遍历。  

- **空间复杂度**：`O(1)`，只用了几个整型变量，没有额外的数组或递归栈。  



---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有可能的容量**。实际上，容量和「能否在 `days` 天内完成」之间存在**单调性**：  

- 如果容量 `C` 能完成，那么任何更大的容量 `C' > C` 也一定能完成（因为更大只会让装货更容易）。  
- 反之，如果容量 `C` 不能完成，则所有更小的容量都不可能完成。  

这正好满足二分搜索（Binary Search）可以使用的**单调判定函数**的条件。我们把「是否可行」抽象成一个函数 `possible(capacity)`，然后在 `[lo, hi]` 区间上二分查找最小的满足 `possible` 为真的容量。

**二分搜索步骤**  

1. **确定搜索区间**  
   - `lo = max(weights)`（最小可能容量）  
   - `hi = sum(weights)`（最大可能容量）  

2. **循环二分**  
   - `mid = (lo + hi) // 2` 取中间值作为当前尝试的容量。  
   - 调用 `possible(mid)`：用同暴力解中「模拟装货」的方式，计算需要多少天。  
   - 如果 `possible(mid)` 为 **True**（能在 `days` 天内完成），说明答案 **不大于** `mid`，于是把上界收紧 `hi = mid`。  
   - 否则说明容量太小，需要更大的船，`lo = mid + 1`。  

3. 当 `lo == hi` 时，搜索结束，`lo`（或 `hi`）就是最小可行容量。  

**核心数据结构**：这里只用到了**普通整数变量**和**一次遍历的数组**。  
**核心算法**：**二分搜索**（Binary Search）+ **线性模拟**（判断函数）。  

> **类比**：  
> 想象你在找一本书的最小页码，使得从这页开始往后阅读能够在规定的时间内读完。你知道如果从第 10 页可以读完，那么从第 11 页肯定也可以读完；于是你可以用二分法快速定位那本「刚好读完」的页码。  

#### 代码（Python）  

```python
def shipWithinDays(weights, days):
    """
    二分搜索答案，返回最小的船舱容量，使得在 days 天内可以把所有包裹运完
    """
    lo = max(weights)          # 任何答案都不能小于最重的包
    hi = sum(weights)          # 把所有包一次装完的极限上界

    # ---------- 判定函数 ----------
    def possible(capacity):
        """
        给定船舱容量 capacity，返回是否能在 days 天内装完所有包
        """
        used_days = 1          # 从第 1 天开始计数
        cur_load = 0           # 当天已经装的重量

        for w in weights:
            # 若加入当前包会超载，则换到新的一天
            if cur_load + w > capacity:
                used_days += 1
                cur_load = 0
            cur_load += w
        # 用的天数不超过限制即为可行
        return used_days <= days

    # ---------- 二分搜索 ----------
    while lo < hi:                     # 区间还有长度时继续收敛
        mid = (lo + hi) // 2           # 取中点尝试
        if possible(mid):              # 能在 days 天内完成
            hi = mid                    # 说明答案不大于 mid，收紧上界
        else:
            lo = mid + 1                # 不能完成，容量需要更大，收紧下界

    return lo                          # lo == hi，即最小可行容量
```

#### 复杂度  

- **时间复杂度**：`O(n · log(sum(weights) - max(weights)))`  
  - 每次判定 `possible` 只需要一次线性遍历 `O(n)`。  
  - 二分搜索的迭代次数是对容量区间取对数（大约 `log2(范围)` 次），范围最多是 `sum - max ≤ 5·10⁴·500 ≈ 2.5×10⁷`，对数约为 25。  
  - 所以整体比暴力快很多，实际运行非常快。  

- **空间复杂度**：`O(1)`，只用了若干整数变量，没有额外的数据结构。  



---  

## 心得  

- **核心技巧**：**二分搜索答案**（Binary Search on the answer） + **单调性判定函数**。  
- **适用的题型**（类似思路）  
  1. *Split Array Largest Sum*（分割数组使最大子数组和最小）  
  2. *Find Minimum Speed to Arrive on Time*（在限定时间内的最小速度）  
  3. *Koko Eating Bananas*（吃香蕉的最小速度）  
- **一句话总结解题钥匙**：  
  “先把问题转化为‘容量够不够’，利用容量随增大而更容易满足的单调性，用二分搜索快速定位最小可行的容量”。  



---  

## 反思  

- **拿到题目第一反应**：  
  “这不就是把重量分配到几天里吗？先尝试从最小可能容量一直往上试，找到第一个能装完的”。  

- **最容易踩的坑**  
  - **下界选错**：如果把下界设为 1，会导致二分搜索很多不必要的无效区间，因为任何小于 `max(weights)` 的容量必然不可能装下最重的包。  
  - **判定函数写错**：忘记在超重时先 **结束当前天** 再把当前包装到新一天，导致天数计算少了。  
  - **边界条件**：当 `days` 等于 `len(weights)` 时，每天只能装一个包，答案就是 `max(weights)`；当 `days` 为 1 时，答案就是 `sum(weights)`，代码要能够覆盖这两个极端。  

- **下次遇到同类题的第一步**  
  1. **确认是否存在单调性**（容量/速度/阈值增大 → 可行性不变或更好）。  
  2. **写出判定函数**，确保它在 `O(n)` 或更低时间内完成。  
  3. 用二分搜索在合理的上下界范围内查找最小/最大满足条件的值。  



祝你在算法的旅程中一路顺风 🚀!