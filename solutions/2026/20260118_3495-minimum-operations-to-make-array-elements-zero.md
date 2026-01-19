# #3495. 将数组元素全部变为零的最少操作次数 / Minimum Operations to Make Array Elements Zero

> 难度：困难 · 标签：Array、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/)

---

## 题目（英文原版）

**Description**

You are given a 2D array queries, where queries[i] is of the form [l, r]. Each queries[i] defines an array of integers nums consisting of elements ranging from l to r, both inclusive.
In one operation, you can:
Your task is to determine the minimum number of operations required to reduce all elements of the array to zero for each query. Return the sum of the results for all queries.

**Examples**

**Example 1:**

```
Input: queries = [[1,2],[2,4]]
Output: 3
Explanation:
For queries[0] :
For queries[1] :
The output is 1 + 2 = 3 .
```

**Example 2:**

```
Input: queries = [[2,6]]
Output: 4
Explanation:
For queries[0] :
The output is 4.
```

**Constraints**

- 1 <= queries.length <= 105
- queries[i].length == 2
- queries[i] == [l, r]
- 1 <= l < r <= 109

---

## 题目（中文翻译）

给定一个二维数组 `queries`，其中 `queries[i]` 的形式为 `[l, r]`。每个 `queries[i]` 定义了一个整数数组 `nums`，包含从 `l` 到 `r`（两端均含）的所有元素。  
在一次操作中，你可以：  
你的任务是求出对每个查询，将该数组的所有元素降低至 `0` 所需的最少操作次数。返回所有查询结果的总和。

### 示例

#### 示例 1
**输入:** `queries = [[1,2],[2,4]]`  
**输出:** `3`  
**解释:**  
对于 `queries[0]` ：  
对于 `queries[1]` ：  
输出为 `1 + 2 = 3` 。

#### 示例 2
**输入:** `queries = [[2,6]]`  
**输出:** `4`  
**解释:**  
对于 `queries[0]` ：  
输出为 `4` 。

### 约束条件
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `queries[i] == [l, r]`
- `1 <= l < r <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目把每个查询 `[l, r]` 看成一个 **连续整数数组** `nums = [l, l+1, … , r]`。  
对数组里的每个元素，我们可以不断做“除以 4（向下取整）”的操作，直到它变成 `0`。  

> **类比**：把除以 4 想成把一本厚厚的书每次撕掉 1/4 页，直到书页全被撕完。

如果只考虑单个数字 `x`，要把它变成 `0` 需要的操作次数等于  
```
t(x) = floor(log4(x)) + 1
```
- `log4(x)` 告诉我们 `x` 大约是 `4` 的几次方；
- `floor` 取整后得到最大的完整 “除以 4” 步数；
- 再加 `1` 是因为即使 `x` 已经小于 `4`，再除一次仍然会得到 `0`。

> **正确性**：  
> 每一次除以 4 都把数值缩小到原来的四分之一。  
> 只要把 `x` 不断除到 `0`，恰好需要 `⌊log4 x⌋ + 1` 次，既没有多余也没有缺少。

现在考虑 **一次操作可以同时对两个数字除以 4**（题目暗示要“配对”两个数）。  
把所有数字的 `t(x)` 看成一堆需要 “减 1” 的计数器，每次我们可以把 **两个** 正数计数器各减 1。  
这相当于：

- 把所有 `t(x)` 加起来得到总的“单独需要的次数” `total = Σ t(x)`；
- 每一次操作可以处理 **两个** 计数器，所以最少需要的操作次数就是把 `total` “两两配对”后剩下的最大配对数：

```
answer = ceil(total / 2)
```

> **为什么是 `ceil(total/2)`**：  
> - 如果 `total` 是偶数，恰好可以把所有计数器两两配对，每配对一次完成一次操作，操作数 = `total/2`。  
> - 如果 `total` 是奇数，最后会剩下一个计数器只能单独处理，需要再多一次操作，所以向上取整 `ceil(total/2)`。

**时间/空间复杂度**（暴力实现）  
- **时间**：对每个查询遍历 `[l, r]` 中的每个数，计算 `t(x)` 再求和 → `O(r‑l+1)`。  
  对大范围（比如 `1~10^9`）根本不可行。  
- **空间**：只用几个整型变量 → `O(1)`。

> **大白话**：  
> `O(n)` 就像排队买饭，排的人越多，等的时间越长；`O(1)` 则像只买一杯饮料，时间固定不变。

---

### 2. 最优解

#### 思路  

**瓶颈**：暴力解必须逐个枚举区间里的每个整数，区间长度可能高达 `10^9`，根本做不到。

**关键观察**：  
` t(x) = floor(log4 x) + 1 ` 只和 `x` 所在的 **4 的幂次区间** 有关。  
所有在 `[4^k , 4^{k+1}-1]`（即第 `k` 层）里的数，它们的 `t(x)` 都相等，都是 `k+1`。

因此，只需要统计区间 `[l, r]` 与这些 **层** 的交集大小，就能一次性算出 `Σ t(x)`，而不必逐个数。

**步骤**：

1. **预计算 4 的幂**  
   `pow4 = [1, 4, 16, 64, …]`，一直到超过 `10^9`（最多 15 项）。  

2. **前缀和函数 `pref(x)`**  
   返回 `Σ_{i=1}^{x} t(i)`。  
   - 从最小的幂次 `k = 0` 开始，找到当前层的右端 `right = min(x, 4^{k+1}-1)`。  
   - 本层包含的元素数 `cnt = right - 4^{k} + 1`。  
   - 本层对前缀和的贡献 `cnt * (k+1)`。  
   - 累加后继续处理更大的 `k`，直到 `right == x`。  
   这一步只循环 `O(log_4 x)` 次（≤ 15），非常快。

3. **单个查询答案**  
   ```
   total = pref(r) - pref(l-1)          # Σ t(x) for x in [l, r]
   ops   = (total + 1) // 2             # 等价于 ceil(total/2)
   ```

4. **所有查询求和**  
   对每个查询算出 `ops`，累加得到最终答案。

**核心算法**：**分段计数 + 前缀和**。  
不涉及动态规划、双指针或单调栈，只是把“相同需求的数放在一起”，一次性算完。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
"""
Minimum Operations to Make Array Elements Zero
思路：利用 /4 操作次数只与所在的 4 的幂次区间有关，构造前缀和快速求区间总次数，
再用 ceil(total/2) 得到最少操作数。
"""

from typing import List

# --------------------------------------------------------------
# 1️⃣ 预计算 4 的幂次（直到超过 1e9）
POW4 = [1]                       # 4^0
while POW4[-1] <= 10**9:
    POW4.append(POW4[-1] * 4)    # 依次乘以 4
# 此时 POW4 = [1, 4, 16, ..., 4^15]，长度约 16
# --------------------------------------------------------------

def prefix_sum(x: int) -> int:
    """
    返回 Σ_{i=1}^{x} ( floor(log4(i)) + 1 )
    只遍历 4 的幂次区间，时间 O(log_4 x)。
    """
    if x <= 0:
        return 0

    total = 0          # 累计答案
    k = 0              # 当前层的幂次（0 表示 [1, 3]）
    while True:
        left = POW4[k]                     # 本层左端点 = 4^k
        right = min(x, POW4[k + 1] - 1)    # 本层右端点（受 x 限制）
        cnt = right - left + 1             # 本层元素个数
        total += cnt * (k + 1)             # 每个元素需要 (k+1) 次 /4

        if right == x:                     # 已覆盖到 x，结束
            break
        k += 1

    return total


def minimum_operations(queries: List[List[int]]) -> int:
    """
    对所有查询求最少操作数之和。
    """
    ans = 0
    for l, r in queries:
        total_ops_needed = prefix_sum(r) - prefix_sum(l - 1)   # Σ t(i)
        # ceil(total/2) = (total + 1) // 2（整数除法）
        ans += (total_ops_needed + 1) // 2
    return ans


# --------------------------------------------------------------
# 示例运行（可自行取消注释测试）
if __name__ == "__main__":
    # 示例 1
    q1 = [[1, 2], [2, 4]]
    print(minimum_operations(q1))   # 输出 3

    # 示例 2
    q2 = [[2, 6]]
    print(minimum_operations(q2))   # 输出 4
# --------------------------------------------------------------
```

**代码要点注释**  

- `POW4` 类似一本 **“4 的幂次表”**，帮助我们快速定位每个数字属于哪一层。  
- `prefix_sum` 只在每层上做一次算术运算，**不遍历具体的数字**，因此即使 `x = 10^9` 也只循环 15 次。  
- ` (total + 1) // 2 ` 正是 **向上取整** 的整数实现，避免使用浮点数。

#### 复杂度

- **时间复杂度**：  
  对每个查询 `O(log_4 r)`（至多 15 次），整体 `O(Q * log_4 maxR)`，  
  其中 `Q ≤ 10^5`，`maxR ≤ 10^9` → 大约 `1.5 × 10^6` 次基本运算，轻松通过。  

- **空间复杂度**：  
  只使用常数级额外空间（`POW4` 长度固定 ≤ 16），即 `O(1)`。

> **对比暴力**：  
> 暴力是 `O(r‑l+1)`，最坏情况下是 `O(10^9)`，根本不可跑；  
> 最优解把复杂度降到 **对数级**，几乎瞬间完成。

---

## 心得

- **核心技巧**：**分段计数 + 前缀和**，把“相同属性的元素合并”来避免逐个遍历。  
- **适用场景**：  
  1. 统计在 **指数区间**（如 `2^k, 3^k`）内的数值特征（例：`floor(log2 x)`、`floor(log10 x)`）。  
  2. 需要对 **连续区间** 求和且每个数的函数值在区间内保持不变的题目（如“区间内每个数的位数”）。  
  3. 任何可以 **按块** 预先计算贡献的计数类问题。  
- **解题钥匙**：**“把相同的东西放在一起，一次性算完”**。

---

## 反思

- **第一反应**：看到“除以 4”就想到对每个数单独计数，想把所有 `t(x)` 累加后再配对。  
- **最容易踩的坑**：  
  - 忘记对 **奇数个总次数** 需要向上取整，直接除以 2 会少算一次。  
  - 直接遍历 `[l, r]` 会超时。  
  - 计算 `log4` 时使用浮点数容易产生精度误差，最好用整数区间的方式（如本解法）避免。  
- **下次遇到类似题**：第一步就思考 **“函数值是否在某些区间保持不变”**，如果是，就把区间划分好，用前缀和或数学公式一次性求和。这样可以把指数级的遍历压缩到对数级的循环。