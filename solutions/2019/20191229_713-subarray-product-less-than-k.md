# #713. 子数组乘积小于 K / Subarray Product Less Than K

> 难度：中等 · 标签：Array、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/subarray-product-less-than-k/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer k, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.

**Examples**

**Example 1:**

```
Input: nums = [10,5,2,6], k = 100
Output: 8
Explanation: The 8 subarrays that have product less than 100 are:
[10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6]
Note that [10, 5, 2] is not included as the product of 100 is not strictly less than k.
```

**Example 2:**

```
Input: nums = [1,2,3], k = 0
Output: 0
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- 1 <= nums[i] <= 1000
- 0 <= k <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回满足以下条件的连续子数组（subarray）数量：该子数组中所有元素的乘积（product）**严格小于** `k`。

### 示例

#### 示例 1
**输入**  
```json
nums = [10,5,2,6], k = 100
```
**输出**  
```
8
```
**解释**  
乘积小于 `100` 的 8 个子数组为：  
`[10]`, `[5]`, `[2]`, `[6]`, `[10, 5]`, `[5, 2]`, `[2, 6]`, `[5, 2, 6]`  
注意 `[10, 5, 2]` 不计入答案，因为其乘积等于 `100`，并非严格小于 `k`。

#### 示例 2
**输入**  
```json
nums = [1,2,3], k = 0
```
**输出**  
```
0
```

### 约束条件
- `1 <= nums.length <= 3 * 10^4`
- `1 <= nums[i] <= 1000`
- `0 <= k <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有连续子数组**，计算它们的乘积，看是否 `< k`。  
- 这里的“连续子数组”可以想象成一根绳子，从数组的某个位置开始往后拉，拉多长就是子数组的长度。  
- 为了遍历所有可能的绳子起点 `i`（左端点）和终点 `j`（右端点），我们可以使用两层循环：外层固定左端点 `i`，内层让右端点 `j` 从 `i` 向右移动，每移动一步就把新的元素乘进来。  
- 只要乘积 `< k`，计数器 `ans` 加一；如果乘积已经 `>= k`，后面的子数组只会更大（因为所有数字都是正数），于是可以直接结束内层循环，继续下一个左端点。

> **为什么正确？**  
> 每一个子数组都有唯一的左端点 `i` 与右端点 `j`，两层循环恰好遍历了所有 `(i, j)` 的组合。只要在遍历过程中对每个组合计算真实乘积并比较，就不会漏掉也不会多计。

#### 代码（Python）

```python
from typing import List

def numSubarrayProductLessThanK_brute(nums: List[int], k: int) -> int:
    # 如果 k <= 1，任何正数乘积都不可能小于 k，直接返回 0
    if k <= 1:
        return 0

    n = len(nums)
    ans = 0

    # 枚举左端点 i
    for i in range(n):
        prod = 1                     # prod 用来保存当前子数组的乘积
        # 枚举右端点 j，逐步向右扩展子数组
        for j in range(i, n):
            prod *= nums[j]          # 把新加入的元素乘进去
            if prod < k:
                ans += 1            # 满足条件，计数
            else:
                # 乘积已经不小于 k，后面的子数组乘积只会更大，直接退出内层循环
                break
    return ans
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  - “平方”在这里的直观意义是：我们用两层循环，最坏情况下（比如 `k` 很大）每个左端点都要遍历到数组末尾，导致大约 `n * n / 2` 次乘法运算。对 `n = 10⁴` 的数组来说，这已经会超时。
- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量（`prod`、`ans`、循环计数器），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算乘积**：每次左端点移动时，我们都要重新从头乘一次。实际上，乘积是可以**“滑动”**的——当左端点右移时，只需要把左端点对应的数除掉，而右端点右移时，只需要把新数乘进去。

这正好对应**滑动窗口（Sliding Window）**的思想：

1. **维护一个窗口** `[left, right]`，窗口内的所有元素乘积 `prod` 始终满足 `prod < k`。  
2. `right` 从左到右遍历数组，每加入一个新元素 `nums[right]`，把它乘到 `prod` 中。  
3. 如果此时 `prod >= k`，说明窗口太“大”了，需要**收缩左边界**：不断把 `nums[left]` 从 `prod` 中除掉，并把 `left` 向右移动，直到 `prod < k` 为止。  
4. 此时窗口 `[left, right]` 已经是**以 `right` 为右端点的最长合法子数组**。以 `right` 为右端点的所有合法子数组数量恰好等于窗口长度 `right - left + 1`（因为左端点可以取 `left, left+1, …, right`）。把这个数量累加到答案中。

> **为什么正确？**  
> - `prod` 始终保持为窗口内所有元素的乘积，窗口的左、右边界只会单向移动（不回溯），所以每个元素最多被乘一次、除一次，保证了乘积的实时准确性。  
> - 当 `prod < k` 时，窗口内的所有子数组（左端点从 `left` 到 `right`）必然满足条件，因为乘积只会变小或保持不变（去掉左端点的数会让乘积更小）。  
> - 当 `prod >= k` 时，唯一的解决办法就是把左端点右移，去掉最左边的数；这一步是**必要且充分**的，因为只有这样才能让乘积重新下降到 `< k`。

> **类比**  
> 想象你在一条河上划船，河面上有若干浮标（数组元素），每个浮标的“重量”是它的数值。船上只能承受总重量 `< k`。你从左往右推进（`right`），每上一个浮标就增加重量；如果超重了，就把船头最早上的浮标（`left`）扔掉，直到船重新轻于限制。此时船上所有浮标的组合就是合法的连续子数组。

#### 代码（Python）

```python
from typing import List

def numSubarrayProductLessThanK(nums: List[int], k: int) -> int:
    """
    使用滑动窗口求解，时间 O(n)，空间 O(1)
    """
    # k <= 1 时没有合法子数组（因为所有 nums[i] >= 1）
    if k <= 1:
        return 0

    prod = 1          # 当前窗口的乘积
    left = 0          # 窗口左端点
    ans = 0           # 结果计数

    # right 逐个遍历每个元素，扩大窗口
    for right, val in enumerate(nums):
        prod *= val   # 把新元素加入乘积

        # 如果乘积不满足条件，收缩左端点直到满足
        while prod >= k and left <= right:
            prod //= nums[left]   # 把左端点的数除掉（整除，因为都是正整数）
            left += 1             # 左端点右移

        # 此时 prod < k，窗口长度 = right - left + 1
        # 以 right 为结尾的合法子数组有这么多
        ans += right - left + 1

    return ans
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 每个元素至多被乘进窗口一次、除出窗口一次，整体遍历只是一次线性扫描。对 `n = 3·10⁴` 完全可以在毫秒级完成。  
- **空间复杂度：** `O(1)`  
  - 只用了几个整数变量（`prod, left, ans`），不随输入规模增长。

---

## 心得

- **核心技巧**：**滑动窗口**（保持一个满足条件的动态子数组区间），配合**乘积的前向乘、后向除**。
- **适用题型**  
  1. 子数组乘积/和小于/等于某个阈值（如 “Subarray Sum Equals K” 也可以用滑动窗口的变形）。  
  2. 最长/最短满足条件的连续子序列（如 “Longest Substring Without Repeating Characters”）。  
  3. 包含正数且需要“窗口乘积/和”单调变化的题目（如 “Maximum Size Subarray Sum Equals k”）。
- **一句话总结解题钥匙**：*把 “所有子数组” 的枚举转换为 “维护一个一直合法的窗口”，窗口左端点只在必要时收缩，右端点只向前走。*

---

## 反思

- **第一反应**：看到“所有连续子数组”，自然想到两层循环的暴力遍历。  
- **最容易踩的坑**  
  - `k <= 1` 的特殊情况：因为数组元素都是正数，乘积永远 ≥ 1，直接返回 0。忘记这一步会导致除零或死循环。  
  - 整除时使用 `//` 而不是 `/`：在 Python 中 `/` 会得到浮点数，累积误差会破坏比较。  
  - 边界条件 `left` 可能会超过 `right`（比如 `prod` 仍然 >= k 时），必须在 `while` 循环里加上 `left <= right` 防止无限循环。  
- **下次遇到同类题**：第一步先判断是否可以**单调滑动窗口**（所有元素非负/正），如果可以，就立刻尝试维护一个“合法窗口”，而不是直接写暴力枚举。这样往往能把时间复杂度从 `O(n²)` 降到 `O(n)`。