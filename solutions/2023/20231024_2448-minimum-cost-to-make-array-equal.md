# #2448. 最小代价使数组相等 / Minimum Cost to Make Array Equal

> 难度：困难 · 标签：Array、Binary Search、Greedy、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-make-array-equal/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed arrays nums and cost consisting each of n positive integers.
You can do the following operation any number of times:
The cost of doing one operation on the ith element is cost[i].
Return the minimum total cost such that all the elements of the array nums become equal.

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,2], cost = [2,3,1,14]
Output: 8
Explanation: We can make all the elements equal to 2 in the following way:
- Increase the 0th element one time. The cost is 2.
- Decrease the 1st element one time. The cost is 3.
- Decrease the 2nd element three times. The cost is 1 + 1 + 1 = 3.
The total cost is 2 + 3 + 3 = 8.
It can be shown that we cannot make the array equal with a smaller cost.
```

**Example 2:**

```
Input: nums = [2,2,2,2,2], cost = [4,2,8,1,3]
Output: 0
Explanation: All the elements are already equal, so no operations are needed.
```

**Constraints**

- n == nums.length == cost.length
- 1 <= n <= 105
- 1 <= nums[i], cost[i] <= 106
- Test cases are generated in a way that the output doesn't exceed 253-1

---

## 题目（中文翻译）

给定两个下标从 0 开始的数组 `nums` 和 `cost`，两者均包含 **n** 个正整数。  
你可以对第 **i** 个元素执行任意次数的以下操作：

- 将 `nums[i]` 增加或减少 1。执行一次该操作的代价为 `cost[i]`。

返回使得数组 `nums` 中所有元素相等的最小总代价。

**示例 1**

```text
Input: nums = [1,3,5,2], cost = [2,3,1,14]
Output: 8
Explanation: 我们可以将所有元素都变为 2，过程如下：
- 将下标 0 的元素增加一次，代价为 2。
- 将下标 1 的元素减少一次，代价为 3。
- 将下标 2 的元素减少三次，代价为 1 + 1 + 1 = 3。
总代价为 2 + 3 + 3 = 8。
可以证明不存在更小的代价使数组相等。
```

**示例 2**

```text
Input: nums = [2,2,2,2,2], cost = [4,2,8,1,3]
Output: 0
Explanation: 所有元素已经相等，无需任何操作。
```

**约束条件**

- `n == nums.length == cost.length`
- `1 <= n <= 10^5`
- `1 <= nums[i], cost[i] <= 10^6`
- 测试用例保证输出不超过 `2^53 - 1`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有元素都改成数组 `nums` 中的某一个值**，然后把每一种可能的目标值的代价算出来，取最小的那一个。  

- **数据结构**：只需要遍历两个同长的列表 `nums` 与 `cost`。可以把 `cost[i]` 想象成“每次把第 `i` 个元素改动一次要付的价钱”，就像去超市买东西，每件商品都有单价。  
- **为什么正确**：  
  1. 题目要求所有元素最终相等，而我们只考虑把它们改成已有的 `nums` 中的某个数。  
  2. 设最终相等的值为 `x`，如果 `x` 不是原数组里出现的数，那么把它向最近的已有数（左或右）移动一步，整体代价只会 **不增**（因为移动一步的代价是所有对应 `cost[i]` 的加权和的正数）。所以最优解一定是某个原始的 `nums[i]`。  
- **暴力做法**：对每个可能的目标值 `t = nums[j]`，遍历全部元素，累计 `cost[i] * |nums[i] - t|`。  

**时间/空间复杂度**：  
- 外层遍历 `n` 次，内层也遍历 `n` 次，故总共是 `n × n = n²` 次基本操作。用大白话说，就是如果有 10,000 个数，算法要跑 **一亿** 次循环，显然太慢。  
- 只用了常数级别的额外空间（几个临时变量），记作 **O(1)**。

#### 代码（Python）

```python
def min_cost_bruteforce(nums, cost):
    """
    暴力解：尝试把所有元素改成 nums 中的每一个值，求最小代价
    时间复杂度 O(n^2)，空间复杂度 O(1)
    """
    n = len(nums)
    ans = float('inf')                     # 记录最小费用

    for target in nums:                    # 每个可能的目标值
        total = 0
        for i in range(n):                 # 计算把所有元素改成 target 的费用
            total += cost[i] * abs(nums[i] - target)
        ans = min(ans, total)              # 取最小

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环，每层都是 `n` 次。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解我们知道：  
1. **目标值一定是 `nums` 中的一个元素**（因为把目标往最近的已有数移动代价不会增大）。  
2. 代价公式是 `∑ cost[i] * |nums[i] - target|`，这是一种 **加权绝对偏差**，它的形状是 **凸函数**（先下降后上升），所以最小点一定在**拐点**处。  

**拐点** 对应的是 **加权中位数**（weighted median）：

- 把 `(nums[i], cost[i])` 按 `nums[i]` 从小到大排好序。  
- 计算所有 `cost` 的总和 `W = Σ cost[i]`。  
- 从左到右累加 `cost`，找到第一个使得累计和 `≥ W/2` 的位置，这个位置对应的 `nums` 就是 **加权中位数**。  

为什么加权中位数是最优的？  
- 想象每个元素 `i` 把 `cost[i]` 份“重量”放在坐标 `nums[i]` 上。把所有重量的“平衡点”向左或向右移动会导致左边或右边的重量产生额外的距离代价。只有当左侧重量 ≤ 右侧重量时，向左移动会让左侧代价增加更多；同理向右移动也是如此。恰好在左侧累计重量刚好达到或超过一半时，左右两边的“拉力”最均衡，这就是最小代价点——加权中位数。

**实现步骤**：

1. **配对并排序**：`pairs = sorted(zip(nums, cost))`。  
2. **前缀累计**：遍历排序后的数组，维护 `prefix_cost`（左侧累计重量）和 `total_cost = sum(cost)`。  
3. 当 `prefix_cost >= total_cost / 2` 时，当前的 `num` 即为目标值 `target`。  
4. **一次遍历算总费用**：利用目标值直接计算 `∑ cost[i] * |nums[i] - target|`（仍是 O(n)），或者在排序过程中用前缀/后缀和进一步优化到 O(1) 计算每个候选点的费用（这里为了清晰，直接在第 4 步一次遍历）。  

整体复杂度是 **排序 O(n log n)** 加上 **线性遍历 O(n)**，即 `O(n log n)`，空间是存储排序后的数组 `O(n)`。

#### 代码（Python）

```python
def min_cost_optimal(nums, cost):
    """
    最优解：加权中位数 + 一次遍历求总费用
    时间复杂度 O(n log n)（排序），空间复杂度 O(n)（存放排序后的列表）
    """
    n = len(nums)

    # 1. 把数值和对应的费用配对后排序（想象把每个数放到坐标轴上，费用是重量）
    pairs = sorted(zip(nums, cost), key=lambda x: x[0])   # 按 nums 从小到大排

    # 2. 计算全部费用的总和，用来判断“重量的一半”
    total_weight = sum(cost)

    # 3. 找到加权中位数所在的数值
    prefix_weight = 0
    target = None
    for val, w in pairs:
        prefix_weight += w
        if prefix_weight * 2 >= total_weight:   # 左侧重量 >= 右侧重量（即 >= 一半）
            target = val
            break

    # 4. 计算把所有元素改成 target 的最小总费用
    ans = 0
    for i in range(n):
        ans += cost[i] * abs(nums[i] - target)

    return ans
```

> **代码要点说明**  
> - `pairs` 的排序相当于把每个数放在数轴上排好队，`cost` 就是每个人背的“背包重量”。  
> - `prefix_weight * 2 >= total_weight` 等价于 `prefix_weight >= total_weight / 2`，避免使用浮点数。  
> - 找到目标值后，只需要一次普通遍历计算代价即可，代码保持简洁易懂。

#### 复杂度  

- **时间复杂度**：`O(n log n)` —— 主要来自排序，后面的遍历都是线性。与暴力的 `O(n²)` 相比，提升非常明显。  
- **空间复杂度**：`O(n)` —— 需要额外的列表保存排序后的 `(num, cost)` 对。若在原数组上原地排序，可降到 `O(1)`（不计递归栈）。

---

## 心得  

- **核心技巧**：**加权中位数**（weighted median）——在加权绝对偏差问题里，最小化总代价的目标点就是使左侧累计权重不小于总权重一半的那个数。  
- **适用题型**：  
  1. “把数组元素统一到同一个值的最小代价” 类问题（本题）。  
  2. “最小化加权距离之和” 如 LeetCode 2963 *Minimum Number of Coins to be Added*（变形）。  
  3. “找出使得 Σ w_i * |x - a_i| 最小的 x” 的统计学问题（加权 L1 中心点）。  
- **一句话总结**：**把每个数视作有重量的点，找出重量平衡的中位数，即是最省钱的目标值**。

---

## 反思  

- **第一反应**：看到“把所有元素变成相同的数”，自然想到遍历所有可能的目标值并逐一计算代价。  
- **最容易踩的坑**：  
  - 忽略了“目标值一定可以选自原数组”这一关键优化，导致直接枚举所有整数范围（会超时）。  
  - 处理大数时忘记使用 `int`（Python 自动大整数，但在其他语言要防止溢出）。  
  - 在判断加权中位数时使用浮点除法会产生精度问题，最好用 `*2` 比较整数。  
- **下次思路**：一看到“加权绝对值求和”这种形式，就先想 **“加权中位数”** 或者 **“凸函数最小点”**，先检查是否可以通过排序 + 前缀和直接得到答案，再决定是否需要二分或单调队列等更复杂的技巧。