# #2560. **打家劫舍 IV** / House Robber IV

> 难度：中等 · 标签：Array、Binary Search、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/house-robber-iv/)

---

## 题目（英文原版）

**Description**

There are several consecutive houses along a street, each of which has some money inside. There is also a robber, who wants to steal money from the homes, but he refuses to steal from adjacent homes.
The capability of the robber is the maximum amount of money he steals from one house of all the houses he robbed.
You are given an integer array nums representing how much money is stashed in each house. More formally, the ith house from the left has nums[i] dollars.
You are also given an integer k, representing the minimum number of houses the robber will steal from. It is always possible to steal at least k houses.
Return the minimum capability of the robber out of all the possible ways to steal at least k houses.

**Examples**

**Example 1:**

```
Input: nums = [2,3,5,9], k = 2
Output: 5
Explanation: 
There are three ways to rob at least 2 houses:
- Rob the houses at indices 0 and 2. Capability is max(nums[0], nums[2]) = 5.
- Rob the houses at indices 0 and 3. Capability is max(nums[0], nums[3]) = 9.
- Rob the houses at indices 1 and 3. Capability is max(nums[1], nums[3]) = 9.
Therefore, we return min(5, 9, 9) = 5.
```

**Example 2:**

```
Input: nums = [2,7,9,3,1], k = 2
Output: 2
Explanation: There are 7 ways to rob the houses. The way which leads to minimum capability is to rob the house at index 0 and 4. Return max(nums[0], nums[4]) = 2.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= (nums.length + 1)/2

---

## 题目（中文翻译）

有若干连续的房子沿街排列，每栋房子里都有一定金额。还有一个小偷，他想要偷取这些房子里的钱，但他不会偷相邻的两栋房子。  
小偷的 **能力值 (capability)** 定义为他在所有被偷的房子中，单个房子所偷金额的最大值。  

给定整数数组 `nums`，其中 `nums[i]` 表示从左起第 `i` 栋房子里存放的金额。还给定整数 `k`，表示小偷至少要偷取的房子数量。题目保证至少可以偷取 `k` 栋房子。  

返回在所有满足至少偷取 `k` 栋房子的方案中，能够得到的最小 **能力值**。

---

**示例 1**

```text
Input: nums = [2,3,5,9], k = 2
Output: 5
Explanation: 
有三种方式可以偷取至少 2 栋房子：
- 偷取下标 0 和 2 的房子。能力值为 max(nums[0], nums[2]) = 5。
- 偷取下标 0 和 3 的房子。能力值为 max(nums[0], nums[3]) = 9。
- 偷取下标 1 和 3 的房子。能力值为 max(nums[1], nums[3]) = 9。
因此返回 min(5, 9, 9) = 5。
```

**示例 2**

```text
Input: nums = [2,7,9,3,1], k = 2
Output: 2
Explanation: 有 7 种偷取方式。能够得到最小能力值的方式是偷取下标 0 和 4 的房子。返回 max(nums[0], nums[4]) = 2。
```

---

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= (nums.length + 1) / 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有满足「不偷相邻房子」的组合都枚举出来**，然后在每个组合里找出最大偷取金额（即能力值），最后取这些能力值的最小值。

- **数据结构**：我们只需要用**列表**来保存当前枚举到的房子下标。可以把它想象成“挑选水果的篮子”，每次往篮子里放一个房子的下标，放之前要检查这个房子和篮子里已有的房子是否相邻（相邻就像是两颗相邻的葡萄，挑了一个就不能挑另一个）。
- **正确性**：因为我们遍历了**所有**合法的挑选方式，必然会包含最优的那一种，所以最终取到的最小能力值一定是答案。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def minCapability_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = float('inf')                     # 记录当前找到的最小能力值

    # 所有可能的挑选下标组合（不要求不相邻，后面再过滤）
    for comb in combinations(range(n), k):
        # 检查是否有相邻的下标
        ok = True
        for i in range(1, k):
            if comb[i] - comb[i-1] == 1:    # 相邻了，非法
                ok = False
                break
        if not ok:
            continue                         # 直接跳过这个非法组合

        # 计算该组合的能力值：挑的房子里金额的最大值
        capability = max(nums[i] for i in comb)
        best = min(best, capability)        # 保留更小的答案

    return best
```

> **关键行解释**  
> - `combinations(range(n), k)`：枚举所有挑 `k` 个下标的方式，像把所有可能的“挑水果的方式”列出来。  
> - `if comb[i] - comb[i-1] == 1`：判断两个挑的下标是否相邻，若相邻则这套方案不合法。  
> - `max(nums[i] for i in comb)`：在当前合法方案里找出最大金额，即该方案的“能力”。  

#### 复杂度

- **时间复杂度**：`O(C(n, k) * k)`  
  - `C(n, k)` 是组合数，表示所有挑 `k` 个房子的方式。即使 `k` 很小，组合数也会随着 `n` 指数级增长。可以把它想象成“你要在 1000 本书里挑 5 本，每本书都有可能被挑”，枚举的次数非常多。  
- **空间复杂度**：`O(k)`  
  - 只保存当前枚举的 `k` 个下标，最多占用 `k` 个整数的空间。

> 暴力解虽然思路最直观，但在 `n` 达到 `10⁵` 时根本跑不完，需要寻找更快的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有组合**。我们实际上并不需要知道具体挑了哪些房子，只要判断**是否存在一种合法的挑选方式，使得每栋被偷的房子金额都 ≤ 某个阈值**。如果能判断这个“可行性”，我们就可以用**二分搜索**在答案空间里快速定位最小的阈值。

**核心想法**：

1. **答案一定在数组的最小值和最大值之间**。  
   - 最小值：如果把阈值设为 `min(nums)`，只能偷那些金额等于最小值的房子，可能不满足 `k`。  
   - 最大值：设为 `max(nums)`，显然一定能偷到 `k`（因为题目保证可行）。

2. **二分搜索**：在 `[low, high]` 区间取中点 `mid`，把它当作“能力上限”。  
   - 检查**是否能在不偷相邻房子的前提下，选出至少 `k` 个金额 ≤ `mid` 的房子**。  
   - 如果能，则说明答案 ≤ `mid`，把搜索区间缩小到左半边；否则答案 > `mid`，搜索右半边。

3. **可行性检查（check 函数）**：  
   - 这一步是 **贪心**：从左到右遍历房子，遇到 `nums[i] ≤ mid` 并且前一个房子没有被偷，就偷这间房子。  
   - 为什么贪心有效？因为我们只关心“能否偷到足够多的房子”，不在乎具体挑哪几间。只要当前房子满足阈值且不与上一次偷的房子相邻，立刻偷它不会影响后面的选择（后面的房子仍然可以按同样规则继续判断）。这相当于**把每一次合法的机会都利用了**，从而得到最多可能的偷取数量。  
   - 如果遍历结束后累计的偷取数量 ≥ `k`，说明 `mid` 可行。

4. **二分结束**：当 `low == high` 时，区间收敛，`low`（或 `high`）就是最小的可行阈值，即答案。

下面用类比帮助理解：  
- 想象你在走一条只能跳两格的跳格子游戏，每格子上写着数字（金额）。你只能站在数字 ≤ `mid` 的格子上，且不能连续站在相邻的两格。**贪心**相当于“一看到符合条件的格子，就立刻跳上去”，这样可以让你跳到最远的格子（最多的格子数），从而判断是否能跳到至少 `k` 次。

#### 代码（Python）

```python
from typing import List

def minCapability(nums: List[int], k: int) -> int:
    """
    二分搜索 + 贪心检查
    返回在不偷相邻房子的前提下，偷到至少 k 间房子时的最小能力值
    """

    def can_steal(limit: int) -> bool:
        """
        检查在能力上限为 limit 时，是否能偷到 >= k 间房子。
        贪心：从左到右，只要当前房子金额 ≤ limit 且上一次没有偷，就偷它。
        """
        cnt = 0          # 已经偷的房子数量
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] <= limit:
                cnt += 1          # 把这间房子偷了
                if cnt >= k:     # 已经够 k 间，提前返回 True
                    return True
                i += 2           # 因为相邻不能偷，直接跳过下一个
            else:
                i += 1           # 这间房子太贵，跳过去
        return cnt >= k

    low, high = min(nums), max(nums)   # 搜索范围
    while low < high:
        mid = (low + high) // 2
        if can_steal(mid):              # 如果能偷到 k 间，说明答案不大于 mid
            high = mid
        else:                           # 不能偷够，说明答案必须更大
            low = mid + 1
    return low
```

> **关键行解释**  
> - `while i < n:`：遍历整个街道。  
> - `if nums[i] <= limit:`：只有当当前房子的金额不超过我们假设的能力上限时，才考虑偷它。  
> - `i += 2`：偷了这间后，紧挨着的下一间不能偷，直接跳过去。  
> - `if cnt >= k: return True`：一旦偷到足够的房子，就不必继续遍历，直接返回可行。  

#### 复杂度

- **时间复杂度**：`O(n log V)`  
  - `n` 是房子数量（最多 `10⁵`），`V = max(nums) - min(nums)` 是答案搜索空间的大小。二分搜索在数值范围上进行 `log V` 次，每次检查 `can_steal` 只需线性遍历一次 `O(n)`。可以把它想象成“在 30 次（因为 `log₂10⁹≈30`）的尝试里，每次都走一遍街道”。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干整型变量，额外空间不随 `n` 增长。

> 与暴力解相比，时间从指数级下降到线性乘以对数级，完全可以在 `10⁵` 规模的数据上跑完。

---

## 心得

- **核心技巧**：**二分答案 + 贪心可行性检查**。先把「最小能力值」这个未知答案当成搜索目标，再用一个线性、贪心的子过程判断某个阈值是否可行。
- **该技巧适用的题型**：
  1. “在满足某种约束的前提下，最小化（或最大化）一个数值”——如 **分配糖果**、**最小化最大分割子数组**（Split Array Largest Sum）等。  
  2. “给定阈值，判断是否可以完成任务”——如 **K 路烧烤**、**分配工作**（Split Array Largest Sum）等。  
- **一句话总结**：把「最小可能的能力」视作搜索区间，用**二分**快速逼近，再用**贪心**一次线性遍历验证即可。

---

## 反思

- **第一反应**：直接想枚举所有合法的抢房组合，结果很快发现不可行。  
- **最容易踩的坑**：  
  - **相邻限制的处理**：在贪心检查里忘记跳过下一个房子，会导致错误计数。  
  - **二分边界**：搜索范围必须包含答案，起始 `low` 用 `min(nums)`、`high` 用 `max(nums)`，否则可能漏掉最小解。  
  - **溢出**：`mid = (low + high) // 2` 在 Python 不会溢出，但在其他语言需要注意防止 `low + high` 超过整数上限。  
- **下次类似题目第一步**：先思考「能否把答案转化为一个阈值」并用二分搜索，这往往能把指数级的搜索压缩到对数级。随后设计一个**单遍线性**的**可行性检测**（贪心或 DP），保证整体效率。