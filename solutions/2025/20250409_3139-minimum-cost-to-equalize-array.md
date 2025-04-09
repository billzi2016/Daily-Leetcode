# #3139. 数组相等的最小代价 / Minimum Cost to Equalize Array

> 难度：困难 · 标签：Array、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-equalize-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers cost1 and cost2. You are allowed to perform either of the following operations any number of times:
Return the minimum cost required to make all elements in the array equal.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [4,1], cost1 = 5, cost2 = 2
Output: 15
Explanation:
The following operations can be performed to make the values equal:
The total cost is 15.
```

**Example 2:**

```
Input: nums = [2,3,3,3,5], cost1 = 2, cost2 = 1
Output: 6
Explanation:
The following operations can be performed to make the values equal:
The total cost is 6.
```

**Example 3:**

```
Input: nums = [3,5,3], cost1 = 1, cost2 = 3
Output: 4
Explanation:
The following operations can be performed to make the values equal:
The total cost is 4.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106
- 1 <= cost1 <= 106
- 1 <= cost2 <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums` 以及两个整数 `cost1` 和 `cost2`。你可以任意次数地执行以下任意一种操作：

返回使数组中所有元素相等所需的最小代价。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

**示例 1**  
**输入**: `nums = [4,1]`, `cost1 = 5`, `cost2 = 2`  
**输出**: `15`  
**解释**:  
可以执行以下操作使所有数值相等，累计花费为 15。

**示例 2**  
**输入**: `nums = [2,3,3,3,5]`, `cost1 = 2`, `cost2 = 1`  
**输出**: `6`  
**解释**:  
可以执行以下操作使所有数值相等，累计花费为 6。

**示例 3**  
**输入**: `nums = [3,5,3]`, `cost1 = 1`, `cost2 = 3`  
**输出**: `4`  
**解释**:  
可以执行以下操作使所有数值相等，累计花费为 4。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^6`  
- `1 <= cost1 <= 10^6`  
- `1 <= cost2 <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目给了我们两种“加一”操作：

| 操作 | 作用 | 费用 |
|------|------|------|
| **单增** | 任选 **一个** 元素 `+1` | `cost1` |
| **双增** | 任选 **两个**（可以是同一个元素两次，也可以是两个不同元素）各 `+1`，一次完成 | `cost2` |

> **类比**：  
> *单增* 就像去字典里查一个单词的解释，查一次要花 `cost1` 分钟。  
> *双增* 就像一次性查两个单词的解释，只要 `cost2` 分钟。显然如果一次查两个的费用比两次单查的费用还贵（`cost2 > 2*cost1`），我们根本不会用“双增”。

**最直接的想法**是：先把所有元素提升到同一个数值 `T`（`T` 必须不小于数组的最大值），然后把 **需要的总加一次数** 用单增和双增的组合凑出来，算出费用，取最小即可。

具体步骤：

1. 任选一个目标值 `T`（`T ≥ max(nums)`）。  
2. 计算每个元素到 `T` 需要加多少次：`diff_i = T - nums[i]`。  
3. 把所有 `diff_i` 加起来得到 **总增次数** `S = Σ diff_i`。  
4. 用 `S` 次单增或双增凑出最小费用：  
   * 如果 `cost2 ≤ 2*cost1`，双增更划算，就尽量多用双增：  
     `pair = S // 2`（成对的次数），`single = S % 2`（剩下的单个），费用 `pair*cost2 + single*cost1`。  
   * 否则双增比两次单增还贵，直接全部用单增：费用 `S * cost1`。  

> **为什么这样一定对？**  
> 我们只关心“加一的次数”。无论把哪两个元素配成一对，都只消耗两次加一，而且费用只取决于 **使用了多少对** 和 **用了多少单次**。所以只要把总次数 `S` 拆分成 `2*pair + single = S`，费用最小的拆法就是上面那种：在双增更划算时尽量配对，在不划算时全部单增。

**时间/空间复杂度**（暴力枚举所有 `T`）：

- 对每个候选 `T` 需要遍历数组一次，时间 `O(n)`。如果把所有可能的 `T`（从 `max(nums)` 到 `max(nums)+something`）都枚举，最坏会是 `O(n * range)`，这里 `range` 可能非常大，根本不可接受。  
- 只用几个整数变量，空间 `O(1)`。

> **大白话解释**：  
> `O(n)` 就是“随数组长度线性增长”，比如数组有 10 万个数，代码会跑大约 10 万次循环；`O(1)` 表示不管数组多大，用的额外内存始终是固定的几百字节。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def minCost_bruteforce(nums, cost1, cost2):
    """
    暴力思路：尝试所有可能的目标值 T（这里仅示意，实际不可行）。
    """
    max_val = max(nums)
    # 为了演示，这里只尝试 T = max_val（真实暴力会枚举更大的 T）
    T = max_val

    # 1. 计算总需要的加一次数 S
    total_inc = sum(T - x for x in nums)   # S

    # 2. 根据费用关系决定怎么组合单增/双增
    if cost2 <= 2 * cost1:          # 双增更划算，尽量配对
        pair = total_inc // 2      # 成对的次数
        single = total_inc % 2     # 剩余的单次
        cost = pair * cost2 + single * cost1
    else:                           # 双增太贵，全部用单增
        cost = total_inc * cost1

    return cost % MOD
```

> **关键行中文注释**  
> - `total_inc = sum(T - x for x in nums)`：把每个数提升到 `T` 需要多少次 `+1`，全部加起来得到总次数 `S`。  
> - `if cost2 <= 2 * cost1:`：判断“双增”是否比“两个单增”更便宜。  
> - `pair = total_inc // 2`：可以组成多少完整的 “两个一起加 1” 的配对。  
> - `single = total_inc % 2`：如果次数是奇数，还剩下一个只能单独加。  

#### 复杂度

- **时间复杂度**：`O(n)`（遍历一次数组计算 `total_inc`）。  
  > 实际暴力枚举所有 `T` 会更慢，这里只展示核心计算的复杂度。  
- **空间复杂度**：`O(1)`（只用了常数个整数变量）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**唯一真正影响费用的因素**是：

1. 目标值 `T` 必须不小于数组的最大值 `max(nums)`。  
2. 所有元素提升到 `T` 需要的 **总加一次数** `S = Σ (T - nums[i])`。  

费用公式：

```
if cost2 <= 2*cost1:
    cost = (S // 2) * cost2 + (S % 2) * cost1
else:
    cost = S * cost1
```

注意到 `S` 与 `T` 的关系非常简单：

```
S = n * T - Σ nums[i]      (n = len(nums))
```

这是一条 **一次函数**（随 `T` 线性增长）。  
而费用 `cost` 也是 `S` 的线性函数（只涉及 `S` 的整数除法与取余），因此 `cost` 随 `T` 也是 **单调递增** 的——`T` 越大，需要加的次数越多，费用只能不减。

> **结论**：要想让费用最小，**一定取最小可能的目标值**，也就是数组的最大元素 `max_val`。再往上提升只会多加不必要的次数，费用只会更高。

所以最优解只需要一次遍历：

1. 找出数组最大值 `max_val`。  
2. 计算所有元素提升到 `max_val` 所需的总次数 `S`。  
3. 根据 `cost1`、`cost2` 的大小关系，用上面的公式算费用。  

整个过程只需要 **O(n)** 的时间和 **O(1)** 的额外空间。

> **为什么不需要枚举“所有可能的最大值”**  
> 题目提示里说“最大值已知”，事实上只要把所有数提升到当前的最大值就已经满足“所有元素相等”。如果再往上提升，等价于在已经相等的数组上再统一加一，这只会额外产生费用，显然不是最小的。

#### 代码（Python）

```python
MOD = 10**9 + 7

def minCost(nums, cost1, cost2):
    """
    最优解：只把所有元素提升到当前的最大值。
    """
    n = len(nums)
    max_val = max(nums)                     # 目标值 T
    total_inc = 0                           # Σ (max_val - nums[i])
    for x in nums:
        total_inc += max_val - x

    # 根据费用关系选择最优的单增/双增组合
    if cost2 <= 2 * cost1:                  # 双增更划算
        pair = total_inc // 2
        single = total_inc % 2
        ans = pair * cost2 + single * cost1
    else:                                   # 双增太贵，只用单增
        ans = total_inc * cost1

    return ans % MOD
```

> **关键行中文注释**  
> - `max_val = max(nums)`：找出已经存在的最大数，它就是我们要统一到的目标值。  
> - `total_inc += max_val - x`：累计每个元素提升到 `max_val` 需要的次数。  
> - `if cost2 <= 2 * cost1:`：判断是否值得使用“双增”。  
> - `pair = total_inc // 2`、`single = total_inc % 2`：把总次数尽可能拆成成对的“双增”。  

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  > 与暴力解相比，去掉了“枚举所有可能的 T”这一步，真正做到线性时间。  
- **空间复杂度**：`O(1)`，只用常数个变量。

---

## 心得

- **核心技巧**：把“把所有数变成同一个数”的问题转化为**总增次数**，再用**贪心配对**（尽量使用更便宜的双增）求最小费用。  
- **适用的题型**  
  1. “把数组所有元素统一到同一数值”类问题（如最小移动次数、最小加减成本）。  
  2. “两种操作的费用比较”类的贪心优化（如单次增/减 vs 成对增/减）。  
- **一句话总结**：**先把目标定在当前最大值，再把需要的增量尽可能配对使用最便宜的“双增”。**

---

## 反思

- **第一反应**：把每个元素都逐个加到最大值，用循环模拟，记下每一次使用的操作。  
- **最容易踩的坑**  
  1. 忘记判断 `cost2` 与 `2*cost1` 的大小，导致把“双增”当成必然更好，出现不必要的高费用。  
  2. 只考虑把所有数提升到 **某个更大的** 值，而没有意识到已经最大值就是最小可行目标。  
  3. 大数取模忘记在最终答案上取模，而不是在中间每一步都取模（会导致错误的结果）。  
- **下次类似题的第一步**：先**确定目标值的范围**（往往是数组的最大或最小），再**把所有操作的费用映射为对“总需求量”的线性函数**，最后用**贪心/数学公式**直接求最小费用。