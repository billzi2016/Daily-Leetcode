# #3638. 最大平衡装运 / Maximum Balanced Shipments

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/maximum-balanced-shipments/)

---

## 题目（英文原版）

**Description**

You are given an integer array weight of length n, representing the weights of n parcels arranged in a straight line. A shipment is defined as a contiguous subarray of parcels. A shipment is considered balanced if the weight of the last parcel is strictly less than the maximum weight among all parcels in that shipment.
Select a set of non-overlapping, contiguous, balanced shipments such that each parcel appears in at most one shipment (parcels may remain unshipped).
Return the maximum possible number of balanced shipments that can be formed.

**Examples**

**Example 1:**

```
Input: weight = [2,5,1,4,3]
Output: 2
Explanation:
We can form the maximum of two balanced shipments as follows:
It is impossible to partition the parcels to achieve more than two balanced shipments, so the answer is 2.
```

**Example 2:**

```
Input: weight = [4,4]
Output: 0
Explanation:
No balanced shipment can be formed in this case:
As there is no way to form even one balanced shipment, the answer is 0.
```

**Constraints**

- 2 <= n <= 105
- 1 <= weight[i] <= 109

---

## 题目（中文翻译）

你得到一个整数数组 weight（array）长度为 n，表示按直线排列的 n 件包裹的重量。  
装运（shipment）被定义为一个连续的子数组（subarray）中的包裹。  
如果该装运中最后一个包裹的重量 **严格小于** 该装运所有包裹的最大重量，则称该装运为平衡的（balanced）。

请选择一组互不重叠、连续且平衡的装运，使得每个包裹至多出现在一个装运中（未被装运的包裹可以留下）。  
返回能够形成的平衡装运的最大数量。

**示例 1**  
输入: `weight = [2,5,1,4,3]`  
输出: `2`  
说明:  
我们可以形成至多两个平衡装运，例如  
- 第一个装运选择子数组 `[2,5,1]`（最后一个包裹重量 1 < 最大重量 5）  
- 第二个装运选择子数组 `[4,3]`（最后一个包裹重量 3 < 最大重量 4）  

不可能把包裹划分出多于两个平衡装运，所以答案为 2。

**示例 2**  
输入: `weight = [4,4]`  
输出: `0`  
说明:  
在这种情况下无法形成任何平衡装运，因为没有子数组满足“最后一个包裹的重量严格小于最大重量”。  
由于连一个平衡装运都无法形成，答案为 0。

**约束条件**  
- `2 <= n <= 10^5`  
- `1 <= weight[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的发货区间**，检查每个区间是否满足「平衡」的条件，然后在这些平衡区间里挑选出不相交且数量最多的集合。  

- **数据结构**：我们只需要**列表**来保存数组 `weight`，以及**两个嵌套循环**来遍历所有子数组。  
- **生活化类比**：把 `weight` 想象成一排货柜，暴力解相当于把每一只手伸进去，**把所有可能的连续货柜组合都尝试一次**，看它们是不是「最后一件货的重量比这段货里最重的货轻」。
- **为什么正确**：只要遍历了**所有**连续子数组，就一定不会漏掉任何一个合法的平衡发货；随后在这些合法区间中挑选最多的不相交区间，显然得到的就是最优解（因为没有更好的组合能超过我们遍历得到的最大数量）。

#### 代码（Python）

```python
from typing import List

def maxBalancedShipments_bruteforce(weight: List[int]) -> int:
    n = len(weight)
    # 用 dp[i] 表示考虑前 i（0~i-1）个包时，最多能得到多少平衡发货
    dp = [0] * (n + 1)          # dp[0] = 0，表示空序列时答案是 0

    # 枚举右端点 r（1 基），左端点 l 从 0 开始往左扫
    for r in range(1, n + 1):
        best = dp[r - 1]        # 不选以 r-1 为结尾的任何区间，直接继承前面的答案
        cur_max = weight[r - 1] # 区间的最大值，先放右端点本身
        # 向左扩展区间 [l, r-1]
        for l in range(r - 1, -1, -1):
            cur_max = max(cur_max, weight[l])   # 更新区间最大值
            # 判断区间 [l, r-1] 是否平衡：最后一个元素 weight[r-1] 必须 < 区间最大值
            if weight[r - 1] < cur_max:
                # 若平衡，则可以在 l 前面的最优解 dp[l] 基础上加 1
                best = max(best, dp[l] + 1)
        dp[r] = best            # 保存考虑前 r 个元素的最优答案
    return dp[n]
```

**关键注释**  
- `dp[r]` 保存「前 `r` 个包（下标 `0~r-1`）里，最多能组成多少个平衡发货」的答案。  
- 内层循环把区间左端点从右往左扩展，同时维护该区间的最大重量 `cur_max`。  
- 当满足 `weight[r-1] < cur_max` 时，这个区间是合法的平衡发货，可以把左侧的最优解 `dp[l]` 加 1。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历 `n` 次，内层最坏情况下也要遍历 `n` 次（相当于把所有 `n·(n+1)/2` 个子数组都检查一遍），所以整体是二次方的工作量。对 `n = 10⁵` 来说，这已经完全不可接受了——想象一下，10 万 × 10 万 ≈ 10⁹ 次操作，电脑根本跑不完。
- **空间复杂度**：`O(n)`  
  只用了一个长度为 `n+1` 的 `dp` 数组，额外空间随输入线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要向左扫描来找所有可能的左端点**，这导致 `O(n²)`。如果我们能够**快速定位**「对当前右端点 `i`，最近的左端点 `j` 满足 `weight[j] > weight[i]`」就能省去大量无效的左端点检查。  

**关键观察**  
- 对于以 `i` 为右端点的平衡区间，**只要区间里出现一个比 `weight[i]` 更大的重量，就已经满足条件**。而且，**越靠近 `i` 的那个更大的元素越好**，因为它让左端点的选择空间更大（左侧还能继续拼接其它区间）。
- 换句话说，**只需要知道最近的、比 `weight[i]` 大的左侧位置 `j`**（如果不存在则记 `j = -1`），那么所有以 `i` 为右端点且平衡的区间，左端点一定在 `j` 及其左侧。于是我们可以把 `dp[i]`（以 `i` 为右端点能够得到的最大发货数）写成：
  
  ```
  dp[i] = best[j] + 1
  ```
  这里 `best[k]` 表示「考虑前 `k`（下标 `0~k`）个包时，最多能得到多少平衡发货」的全局最优值。  
- 为了快速得到最近的更大元素 `j`，我们使用 **单调递减栈**（Monotonic Stack）：
  - 栈中保存的是**下标**，并且对应的 `weight` **严格递减**（栈顶的元素是最近的、比当前元素大的）。
  - 当遍历到 `i` 时，弹出所有 `weight[stack_top] ≤ weight[i]`，因为它们不可能成为 `i` 的最近更大元素。弹完后，栈顶（如果还有）就是我们要的 `j`。

**步骤概览**  

1. 初始化 `best[-1] = 0`（相当于「在数组左边界之前」的答案是 0）。  
2. 用单调递减栈遍历数组 `weight`，对每个位置 `i`：
   - 弹出栈中不满足 `weight[stack_top] > weight[i]` 的元素；
   - 设 `j = stack_top`（若栈空则 `j = -1`）；
   - 计算 `dp_i = best[j] + 1`（如果 `j = -1`，则 `dp_i = 1` 表示可以直接形成一个以 `i` 为右端点的平衡发货）；
   - 更新 `best[i] = max(best[i-1], dp_i)`，保证 `best` 始终保存到当前位置的全局最优；
   - 把 `i` 入栈，维护单调递减性质。
3. 最终答案是 `best[n-1]`（即考虑全部元素时的最优值）。

**类比帮助理解**  
- 想象一条河岸上放了若干块大小不一的石头（重量），我们要在河面上划出不重叠的「跳板」——每块跳板的右端必须比左端的某块石头轻。单调栈就像一位 **守门员**，只保留**比当前石头更高的石头**，因为只有它们能帮助我们「撑起」左端的跳板。

#### 代码（Python）

```python
from typing import List

def maxBalancedShipments(weight: List[int]) -> int:
    n = len(weight)
    # best[i] 表示考虑前 i+1（下标 0~i）个包时的最优答案
    best = [0] * n
    # monotonic stack，存下标，保证 weight[stack] 严格递减
    stack: List[int] = []

    for i in range(n):
        # 弹出所有不比 weight[i] 大的元素
        while stack and weight[stack[-1]] <= weight[i]:
            stack.pop()

        # 最近的更大元素下标
        j = stack[-1] if stack else -1

        # 以 i 为右端点可以得到的平衡发货数
        # 如果 j == -1，说明左侧没有更大的元素，直接形成 1 个区间
        cur_dp = (best[j] + 1) if j != -1 else 1

        # 更新全局最优：要么不使用以 i 为结尾的区间，沿用前一个 best，
        # 要么使用它得到的 cur_dp
        best[i] = max(best[i - 1] if i > 0 else 0, cur_dp)

        # 把当前位置压入栈，保持递减
        stack.append(i)

    return best[-1]
```

**关键注释**  

- `while stack and weight[stack[-1]] <= weight[i]: stack.pop()`  
  **弹出**所有不比当前重量大的下标，确保栈顶始终是**最近的更大元素**。  
- `j = stack[-1] if stack else -1`  
  若栈为空，说明左侧没有更大的包，`j = -1` 相当于「在数组左边界之外」的虚拟位置。  
- `cur_dp = (best[j] + 1) if j != -1 else 1`  
  把左侧的最优解 `best[j]` 加上当前新形成的平衡发货（`+1`），如果没有更大元素则只能把当前包单独算作一个区间（因为它本身已经满足「最后一个包比区间最大轻」——最大就是它自己）。  
- `best[i] = max(best[i - 1] if i > 0 else 0, cur_dp)`  
  取「不使用」或「使用」的较大值，保证 `best` 始终保存到当前位置的全局最优。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个下标最多 **入栈一次、出栈一次**，所以整个循环的操作次数线性增长。相当于「走了一遍数组」的时间。
- **空间复杂度**：`O(n)`  
  需要额外的 `best` 数组（`n` 长）和单调栈（最坏情况下也会存 `n` 个下标），均为线性空间。  

与暴力解相比，时间从二次方降到了线性，能够轻松应对 `n ≤ 10⁵` 的数据规模。

---

## 心得

- **核心技巧**：**单调栈 + 前缀最佳 DP**。单调栈帮助我们在 **O(1)** 时间内找到「最近更大的左侧位置」，而 DP 记录「到当前位置为止的最优解」让我们能够快速累加。
- **适用的题型**  
  1. 「对于每个位置，寻找最近满足某种单调关系的左/右侧元素」——如 *Nearest Greater Element*、*Maximum Width Ramp*。  
  2. 「在满足某种区间约束的情况下，最大化不相交区间数量」——如本题、*Maximum Number of Non‑Overlapping Subarrays With Sum Equals K*（使用前缀和 + 哈希表）。  
  3. 「区间最大/最小值与当前元素的关系」——如 *Maximum Subarray Min‑Product*（单调栈 + 前缀乘积）。
- **一句话总结**：**把「找最近更大」的工作交给单调栈，剩下的「最优累加」交给前缀最大 DP。**

---

## 反思

- **第一反应**：看到「最后一个包的重量要小于区间最大」就想到「只要区间里出现比最后一个更大的就行」，于是自然会想到「最近更大的左侧位置」。
- **最容易踩的坑**  
  - 忘记 **严格** 小于（`<`），导致把等重的情况也算进来，答案会偏大。  
  - 单调栈的比较方向写反（使用 `>=` 而不是 `>`），会把本应保留的更大元素错误弹出。  
  - `best[-1]` 的初始值要设为 0，避免在 `j = -1` 时出现索引错误。  
- **下次遇到类似题**：第一步先**思考能否用单调结构快速定位「最近满足条件的左/右端点」**，如果可以，再结合 **前缀最优/前缀和** 的 DP 思路完成整体最优解。