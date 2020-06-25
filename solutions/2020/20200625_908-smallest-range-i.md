# #908. 最小范围 I / Smallest Range I

> 难度：简单 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/smallest-range-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
In one operation, you can choose any index i where 0 <= i < nums.length and change nums[i] to nums[i] + x where x is an integer from the range [-k, k]. You can apply this operation at most once for each index i.
The score of nums is the difference between the maximum and minimum elements in nums.
Return the minimum score of nums after applying the mentioned operation at most once for each index in it.

**Examples**

**Example 1:**

```
Input: nums = [1], k = 0
Output: 0
Explanation: The score is max(nums) - min(nums) = 1 - 1 = 0.
```

**Example 2:**

```
Input: nums = [0,10], k = 2
Output: 6
Explanation: Change nums to be [2, 8]. The score is max(nums) - min(nums) = 8 - 2 = 6.
```

**Example 3:**

```
Input: nums = [1,3,6], k = 3
Output: 0
Explanation: Change nums to be [4, 4, 4]. The score is max(nums) - min(nums) = 4 - 4 = 0.
```

**Constraints**

- 1 <= nums.length <= 104
- 0 <= nums[i] <= 104
- 0 <= k <= 104

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个整数 `k`。  
在一次操作中，你可以选择任意下标 `i`（`0 <= i < nums.length`），并将 `nums[i]` 改为 `nums[i] + x`，其中 `x` 为区间 `[-k, k]` 中的任意整数。每个下标至多只能进行一次此类操作。  

数组 `nums` 的得分定义为数组中最大元素与最小元素的差值。  
返回对每个下标最多进行一次上述操作后，`nums` 的最小可能得分。

**示例**  

*示例 1*  
```
Input: nums = [1], k = 0
Output: 0
Explanation: 得分为 max(nums) - min(nums) = 1 - 1 = 0。
```

*示例 2*  
```
Input: nums = [0,10], k = 2
Output: 6
Explanation: 将数组改为 [2, 8]。得分为 max(nums) - min(nums) = 8 - 2 = 6。
```

*示例 3*  
```
Input: nums = [1,3,6], k = 3
Output: 0
Explanation: 将数组改为 [4, 4, 4]。得分为 max(nums) - min(nums) = 4 - 4 = 0。
```

**约束条件**  

- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^4`
- `0 <= k <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直观的想法是**把每个元素都枚举所有可能的修改值**，再从所有得到的数组里挑选分数（最大值‑最小值）最小的那一个。  

- **数据结构**：我们只需要一个普通的 Python 列表 `nums`，以及几个整数变量来保存当前的最大值、最小值和最小的分数。  
- **生活化类比**：把每个数组元素想象成一块可以自由滑动的木块，滑动的距离只能在 `[-k, k]` 之间。暴力做法就是把每块木块 **全部试遍** 所有可能的位置，然后看看整体宽度（最右‑最左）最小是多少。  
- **为什么正确**：因为我们真的把**所有合法的**修改方式都尝试了一遍，答案自然不会错。  

显然，这种做法的时间复杂度会非常糟糕。  
假设每个元素可以取 `2k+1`（即 `-k … 0 … +k`）个不同的值，数组长度为 `n`，那么要遍历的组合数是 `(2k+1)^n`，即指数级增长，根本不可接受。  

#### 代码（Python）  
```python
from itertools import product
from typing import List

def smallestRangeI_bruteforce(nums: List[int], k: int) -> int:
    # 1. 为每个位置生成所有可能的取值列表
    #    例如 nums[i]=5, k=2 -> [3,4,5,6,7]
    candidates = [list(range(v - k, v + k + 1)) for v in nums]

    best = float('inf')                     # 保存目前找到的最小分数
    # 2. 使用笛卡尔积枚举所有组合（指数级！）
    for combo in product(*candidates):      # combo 是一个可能的完整数组
        cur_range = max(combo) - min(combo)  # 计算当前分数
        best = min(best, cur_range)         # 更新最小分数

    return best
```
> **注意**：上述代码仅用于说明思路，**在 LeetCode 真题中会因为超时而无法通过**。  

#### 复杂度  
- **时间复杂度**：`O((2k+1)^n)` —— 这里的 `(2k+1)^n` 表示“每个元素有 `2k+1` 种取法，全部组合在一起”。随着 `n`（数组长度）稍微大一点，时间就会呈指数级爆炸。  
- **空间复杂度**：`O(n·k)` 用来保存每个元素的候选取值列表，实际运行时还会有递归栈（`product` 实现）导致额外空间开销。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看出，**真正影响最终分数的只有数组的最大值和最小值**。  
我们不必关心中间的每个元素怎么取，只要把**最大值尽量往左移动**（减小），**最小值尽量往右移动**（增大），两者之间的距离就会变小。  

**关键观察**：  
- 对任意一个元素 `x`，我们最多可以把它向左移动 `k`，向右移动 `k`。  
- 所以 **所有元素的最左可能位置** 是 `min(nums) - k`，**所有元素的最右可能位置** 是 `max(nums) + k`。  
- 为了让整体宽度最小，我们会把原来的 **最小值** 提高 `k`，把 **最大值** 降低 `k`。  
- 于是最小可能的宽度 = `max(0, (max(nums) - k) - (min(nums) + k))`。  
  - 如果 `max - min ≤ 2k`，两端可以相互“碰撞”，甚至交叉，最终可以把所有数调到同一个值，分数为 `0`。  
  - 否则，两端仍有距离，距离就是 `max - min - 2k`。  

**数学表达**：  
```
answer = max(0, max(nums) - min(nums) - 2 * k)
```

**为什么正确**：  
- **上界**：我们展示了一种具体的修改方案（把最小值加 `k`，最大值减 `k`），得到的分数正好是上式的值。  
- **下界**：任意修改后，所有数的最大值至少不小于 `max(nums) - k`（因为即使把原最大数往左移动 `k`，仍不能低于这个值），最小值至多不大于 `min(nums) + k`。于是任意合法数组的分数 **≥** `(max(nums) - k) - (min(nums) + k) = max - min - 2k`。若该值为负，则最小分数只能是 `0`（因为分数不可能为负）。  

两者相等，说明我们得到的值就是最小可能的分数。  

#### 代码（Python）  
```python
from typing import List

def smallestRangeI(nums: List[int], k: int) -> int:
    """
    只需要一次遍历得到数组的最大值和最小值，
    再套用公式 answer = max(0, max - min - 2*k)
    """
    # 1. 找到最小值和最大值（O(n)）
    mn = min(nums)          # 最小元素
    mx = max(nums)          # 最大元素

    # 2. 计算最小可能的范围
    #    若 mx - mn <= 2*k，则可以全部调到同一个数，答案为 0；
    #    否则答案为 (mx - mn - 2*k)。
    ans = max(0, mx - mn - 2 * k)

    return ans
```
> 代码只用了 `min`、`max` 两次遍历，**时间几乎为常数**（`O(n)`），空间只用了若干个整数变量，**`O(1)`**。  

#### 复杂度  
- **时间复杂度**：`O(n)` —— 只需要一次线性扫描即可得到数组的最大值和最小值。对比暴力解的指数级，这几乎是瞬间完成。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`mn、mx、ans`），不随 `n` 增长。  

---

## 心得  

- **核心技巧**：**把问题抽象为“最大值向左、最小值向右各移动 k”**，利用 **区间交叉** 的概念直接得出答案。  
- **适用的题型**：  
  1. **范围压缩** 类问题（如「把数组所有数压到同一段」）。  
  2. **单调区间** 问题（如「把数组的最大最小差距最小化」）。  
  3. **允许一次固定幅度调整** 的题目（如「最多可以加/减 k」的变形）。  
- **一句话总结**：**只要知道原数组的最大值和最小值，答案就是 `max(0, max‑min‑2k)`，不需要枚举每一种修改方式。**  

---

## 反思  

- **第一反应**：看到“每个元素可以加上或减去一个范围内的整数”，我会想到**枚举所有组合**，于是写出指数级的暴力解。  
- **最容易踩的坑**：  
  - 忘记 `k` 可能为 `0`，此时答案应该是原数组的 `max‑min`。  
  - 忽视 **负数返回** 的情况，直接返回 `max‑min‑2k` 会出现负数，需要用 `max(0, …)` 把它夹到非负。  
  - 对边界情况（长度为 1 的数组）不加以区分，实际上公式已经能覆盖，但要确保代码不出现除零等错误。  
- **下次遇到同类题**：第一步先**找出最关键的极值（最大、最小）**，思考“把它们往中心靠拢的极限”能得到的最小/最大值，而不是盲目遍历全部元素的所有可能取值。这样往往能直接得到 O(n) 或 O(1) 的简洁解法。