# #2861. **最大合金数量** / Maximum Number of Alloys

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-alloys/)

---

## 题目（英文原版）

**Description**

You are the owner of a company that creates alloys using various types of metals. There are n different types of metals available, and you have access to k machines that can be used to create alloys. Each machine requires a specific amount of each metal type to create an alloy.
For the ith machine to create an alloy, it needs composition[i][j] units of metal of type j. Initially, you have stock[i] units of metal type i, and purchasing one unit of metal type i costs cost[i] coins.
Given integers n, k, budget, a 1-indexed 2D array composition, and 1-indexed arrays stock and cost, your goal is to maximize the number of alloys the company can create while staying within the budget of budget coins.
All alloys must be created with the same machine.
Return the maximum number of alloys that the company can create.

**Examples**

**Example 1:**

```
Input: n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,0], cost = [1,2,3]
Output: 2
Explanation: It is optimal to use the 1st machine to create alloys.
To create 2 alloys we need to buy the:
- 2 units of metal of the 1st type.
- 2 units of metal of the 2nd type.
- 2 units of metal of the 3rd type.
In total, we need 2 * 1 + 2 * 2 + 2 * 3 = 12 coins, which is smaller than or equal to budget = 15.
Notice that we have 0 units of metal of each type and we have to buy all the required units of metal.
It can be proven that we can create at most 2 alloys.
```

**Example 2:**

```
Input: n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,100], cost = [1,2,3]
Output: 5
Explanation: It is optimal to use the 2nd machine to create alloys.
To create 5 alloys we need to buy:
- 5 units of metal of the 1st type.
- 5 units of metal of the 2nd type.
- 0 units of metal of the 3rd type.
In total, we need 5 * 1 + 5 * 2 + 0 * 3 = 15 coins, which is smaller than or equal to budget = 15.
It can be proven that we can create at most 5 alloys.
```

**Example 3:**

```
Input: n = 2, k = 3, budget = 10, composition = [[2,1],[1,2],[1,1]], stock = [1,1], cost = [5,5]
Output: 2
Explanation: It is optimal to use the 3rd machine to create alloys.
To create 2 alloys we need to buy the:
- 1 unit of metal of the 1st type.
- 1 unit of metal of the 2nd type.
In total, we need 1 * 5 + 1 * 5 = 10 coins, which is smaller than or equal to budget = 10.
It can be proven that we can create at most 2 alloys.
```

**Constraints**

- 1 <= n, k <= 100
- 0 <= budget <= 108
- composition.length == k
- composition[i].length == n
- 1 <= composition[i][j] <= 100
- stock.length == cost.length == n
- 0 <= stock[i] <= 108
- 1 <= cost[i] <= 100

---

## 题目（中文翻译）

你是一个生产合金的公司的所有者，合金是由多种金属混合而成的。现有 `n` 种不同的金属可供使用，并且你拥有 `k` 台机器可以用来制造合金。每台机器在制造一个合金时都需要固定数量的每种金属。

对于第 `i` 台机器，要制造一个合金需要 `composition[i][j]` 单位的第 `j` 种金属。最初，你拥有 `stock[j]` 单位的第 `j` 种金属，购买一单位第 `j` 种金属需要花费 `cost[j]` 枚硬币。

已知整数 `n、k、budget`，以及 **1‑索引** 的二维数组 `composition`、**1‑索引** 的数组 `stock` 与 `cost`，你的目标是在不超过 `budget` 硬币的前提下，最大化公司能够制造的合金数量。所有合金必须使用同一台机器制造。

返回公司能够制造的最大合金数量。

---

### 示例

**示例 1**

```
Input: n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,0], cost = [1,2,3]
Output: 2
Explanation: 最优选择是使用第 1 台机器制造合金。
要制造 2 个合金，需要购买：
- 第 1 种金属 2 单位
- 第 2 种金属 2 单位
- 第 3 种金属 2 单位
总共花费 2*1 + 2*2 + 2*3 = 12 枚硬币，小于预算 15。
```

**示例 2**

```
Input: n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,100], cost = [1,2,3]
Output: 5
Explanation: 最优选择是使用第 2 台机器制造合金。
要制造 5 个合金，需要购买：
- 第 1 种金属 5 单位
- 第 2 种金属 5 单位
- 第 3 种金属 0 单位
总共花费 5*1 + 5*2 + 0*3 = 15 枚硬币，恰好等于预算。
```

**示例 3**

```
Input: n = 2, k = 3, budget = 10, composition = [[2,1],[1,2],[1,1]], stock = [1,1], cost = [5,5]
Output: 2
Explanation: 最优选择是使用第 3 台机器制造合金。
要制造 2 个合金，需要购买：
- 第 1 种金属 1 单位
- 第 2 种金属 1 单位
总共花费 1*5 + 1*5 = 10 枚硬币，等于预算 10。
可以证明无法制造更多合金。
```

---

### 约束条件

- `1 <= n, k <= 100`
- `0 <= budget <= 10^8`
- `composition.length == k`
- `composition[i].length == n`
- `1 <= composition[i][j] <= 100`
- `stock.length == cost.length == n`
- `0 <= stock[i] <= 10^8`
- `1 <= cost[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举每一种机器**，然后**逐个尝试可以做多少合金**。  
我们可以从 `0` 开始，一次加 `1`，一直做到预算不够为止。  
- **数据结构**：  
  - `composition[i][j]`：第 `i` 台机器做一个合金需要的第 `j` 种金属数量。可以把它想象成“配方表”，类似厨房里的食谱。  
  - `stock[j]`：手里已有的第 `j` 种金属数量，就像家里现成的调料。  
  - `cost[j]`：购买一单位第 `j` 种金属需要的金币，类似“超市里每克盐的价钱”。  
- **为什么正确**：  
  - 对每一种机器，我们都尝试了所有可能的合金数量（从 `0` 到预算限制），只要预算够，就说明这个数量是可行的。取所有机器的最大可行数量，自然就是答案。  
- **时间/空间复杂度**：  
  - 假设最多能做 `M` 个合金（`M` 受预算和配方限制），每次判断需要遍历 `n` 种金属。  
  - **时间** 大约是 `O(k * M * n)`。如果把 `M` 看成“最大可能的合金数”，`O(k·M·n)` 就相当于“每台机器都穷举所有可能”。  
  - **空间** 只用了几个整数，`O(1)`（常数级别），因为我们没有额外的数组。

#### 代码（Python）

```python
def maxAlloys_bruteforce(n, k, budget, composition, stock, cost):
    # 记录全局的最大合金数
    ans = 0

    # 遍历每一台机器
    for mach in range(k):
        # 暴力尝试从 0 个合金开始往上增加
        cnt = 0
        while True:
            # 计算生产 cnt 个合金需要额外购买的金属费用
            total = 0
            for metal in range(n):
                need = composition[mach][metal] * cnt          # 需要的总量
                lack = max(0, need - stock[metal])            # 缺少的量
                total += lack * cost[metal]                   # 购买费用
                # 如果已经超出预算，提前结束内部循环
                if total > budget:
                    break
            # 预算够，cnt 合法，继续尝试更大的 cnt
            if total <= budget:
                ans = max(ans, cnt)   # 更新全局答案
                cnt += 1
            else:
                # 预算不够，当前机器已经无法再做更多合金，退出 while
                break

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k * M * n)`  
  - `M` 是答案的上界（比如 `budget / min(cost)`），实际运行时会随预算大小变化。  
  - 直观上可以把 `O(k·M·n)` 想成“每台机器都走一遍所有可能的合金数”。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量和循环索引，没有额外的数组或递归栈。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**线性枚举合金数量**。如果答案是上万甚至上亿，这种“一次加一”会非常慢。  
观察下面的事实：

1. 对于固定的机器 `i`，**判断是否能做 `x` 个合金** 是一个**单调判定**：  
   - `x` 越大，需要的金属越多，花费也只会不减。  
   - 如果 `x` 个合金已经超预算，那么更大的 `x` 一定也不行。  
2. 单调判定可以用**二分查找**（Binary Search）快速定位最大可行的 `x`。  
   - 二分的搜索范围可以设为 `[0, upper]`，其中 `upper` 取一个安全的上界，如  
     `upper = (budget + sum(stock[j] * cost[j])) // min(cost)`，或者更简单地取 `10**9`（因为题目约束保证答案不会超过这个量级）。

**核心算法**：对每台机器，二分搜索最大 `x`，每次判断的代价是遍历 `n` 种金属计算所需费用。最后在所有机器的答案中取最大值。

下面一步步解释二分判断的实现：

- 对每种金属 `j`，需要的总量是 `composition[i][j] * x`。  
- 手里已有的 `stock[j]` 可以直接使用，缺少的部分 `max(0, need - stock[j])` 必须购买。  
- 购买费用是 `缺少量 * cost[j]`，把所有金属的费用累加得到 `total_cost`。  
- 如果 `total_cost <= budget`，说明 `x` 合金可以做；否则 `x` 太大。

**类比**：想象你在超市买材料做菜，预算固定。先尝试做 **5 份**，算算花了多少钱；如果花费在预算以内，就尝试 **10 份**；如果超了，就回退到 **7 份**，如此二分逼近，最终得到最多能做多少份。

#### 代码（Python）

```python
def maxAlloys(n, k, budget, composition, stock, cost):
    """
    返回在预算 budget 内，使用同一台机器能生产的最大合金数量。
    """
    def can_make(machine_idx, x):
        """
        判定使用第 machine_idx 台机器，能否生产 x 个合金而不超预算。
        """
        total = 0
        for metal in range(n):
            need = composition[machine_idx][metal] * x          # 总需求
            lack = max(0, need - stock[metal])                  # 需要买的量
            total += lack * cost[metal]                         # 累计费用
            if total > budget:                                 # 提前剪枝
                return False
        return total <= budget

    answer = 0
    # 对每一台机器分别二分寻找最大可行的合金数
    for i in range(k):
        lo, hi = 0, 10**9          # 设一个足够大的上界
        while lo < hi:
            mid = (lo + hi + 1) // 2   # 取上中位，防止死循环
            if can_make(i, mid):
                lo = mid               # mid 可行，尝试更大
            else:
                hi = mid - 1           # mid 不可行，缩小上界
        answer = max(answer, lo)       # lo 即为机器 i 的最大合金数

    return answer
```

#### 复杂度

- **时间复杂度**：`O(k * n * log U)`  
  - `k` 台机器逐一二分。  
  - 每次二分判断遍历 `n` 种金属，计算费用。  
  - `log U` 是二分的迭代次数，`U` 为我们设定的上界（`10⁹`），`log₂10⁹ ≈ 30`，可以视为常数。  
  - 与暴力解的 `O(k * M * n)` 相比，**把线性枚举的 `M` 替换成了对数级别**，即使答案很大也能在毫秒级完成。  

- **空间复杂度**：`O(1)`  
  - 只用了若干整型变量，未开辟额外数组。

---

## 心得

- **核心技巧**：**单调性 + 二分查找**。先确认“判断是否可行”是单调的（越大越难），再用二分快速定位最大可行值。  
- **适用题型**：  
  1. “在预算/时间/容量限制下，最大可完成的任务数量”——如《Maximum Number of Dishes》《Maximum Toys With Budget》。  
  2. “最小满足条件的值”——如《Capacity To Ship Packages Within D Days》《Koko Eating Bananas》。  
- **一句话总结**：**把“能不能做”变成一个“是/否”的快速检查，然后用二分把答案从“线性枚举”提升到“对数搜索”。**

---

## 反思

- **第一反应**：直接写一个循环，从 `0` 开始逐个尝试合金数量，直到预算不够。  
- **最容易踩的坑**：  
  - **上界选取不当**：如果上界太小，二分会错过真实答案；如果上界过大，仍然安全，因为二分的迭代次数是对数级。  
  - **溢出**：`composition[i][j] * x` 可能超过 Python 整数范围（虽说 Python 自动大整数），但在其他语言需要使用 64 位整数。  
  - **提前剪枝**：在计算费用时，一旦累计超过预算就可以立刻返回 `False`，否则会导致不必要的循环，影响效率。  
- **下次类似题的第一步**：先检查“可行性判定函数”是否具备单调性——如果是，立刻考虑二分搜索；如果不是，再思考是否可以转化或使用其他优化（滑动窗口、前缀和等）。