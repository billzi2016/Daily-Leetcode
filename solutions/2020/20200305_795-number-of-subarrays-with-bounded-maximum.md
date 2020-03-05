# #795. 受限最大值的子数组数量 / Number of Subarrays with Bounded Maximum

> 难度：中等 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/number-of-subarrays-with-bounded-maximum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and two integers left and right, return the number of contiguous non-empty subarrays such that the value of the maximum array element in that subarray is in the range [left, right].
The test cases are generated so that the answer will fit in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: nums = [2,1,4,3], left = 2, right = 3
Output: 3
Explanation: There are three subarrays that meet the requirements: [2], [2, 1], [3].
```

**Example 2:**

```
Input: nums = [2,9,2,5,6], left = 2, right = 8
Output: 7
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109
- 0 <= left <= right <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和两个整数 `left`、`right`，返回满足以下条件的 **连续非空子数组（contiguous non-empty subarray）** 的数量：该子数组中 **最大数组元素（maximum array element）** 的值位于区间 `[left, right]` 内。  
测试数据保证答案可以放入 32 位整数。

**示例 1**  
**输入**: `nums = [2,1,4,3]`, `left = 2`, `right = 3`  
**输出**: `3`  
**解释**: 符合要求的子数组有三个：`[2]`、`[2, 1]`、`[3]`。

**示例 2**  
**输入**: `nums = [2,9,2,5,6]`, `left = 2`, `right = 8`  
**输出**: `7`

**约束条件**
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`
- `0 <= left <= right <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 连续子数组都枚举一遍，逐个检查它们的最大值是否落在 `[left, right]` 区间。  

- **枚举子数组**：可以用两层循环。外层 `i` 表示子数组的起始下标，内层 `j` 表示结束下标（`i ≤ j`），这样 `(i, j)` 就唯一确定了一个连续子数组 `nums[i…j]`。  
- **求子数组最大值**：在每次把 `j` 往右扩展时，维护一个变量 `cur_max`，把新加入的元素和 `cur_max` 做比较即可得到当前子数组的最大值。  
- **判断**：如果 `left ≤ cur_max ≤ right`，计数器 `ans` 加一。

> **类比**：把数组想象成一条街道，`i` 是你站在街道的某个门口，`j` 是你往前走的步数。每走一步，你都要检查这段路上最高的建筑（最大值）是否符合要求。

**正确性**：因为我们遍历了 **所有** 起始位置和结束位置的组合，且每次都准确地计算了对应子数组的最大值，所以只要最大值在区间内就一定会被计数，反之不会计数，答案必然完整。

#### 代码（Python）

```python
def count_subarrays_bruteforce(nums, left, right):
    n = len(nums)
    ans = 0                       # 计数器，记录满足条件的子数组个数
    for i in range(n):            # 子数组的左端点
        cur_max = float('-inf')   # 当前子数组的最大值，初始化为负无穷
        for j in range(i, n):     # 子数组的右端点，一直往右扩展
            cur_max = max(cur_max, nums[j])   # 更新最大值
            # 判断最大值是否在[left, right]之间
            if left <= cur_max <= right:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环遍历所有子数组，最坏情况下 `n` 为 10⁵ 时会有约 `5·10⁹` 次比较，显然会超时。  
  **大白话**：如果你把数组想象成一张 10⁵ 行的表格，暴力解相当于要检查每一格的左上到右下的所有矩形，数量会呈平方增长。

- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量 `cur_max`、`ans`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要重新遍历子数组来判断最大值**。我们可以把注意力转向“**合法子数组的划分**”。关键观察如下：

1. **大于 `right` 的元素**：一旦子数组里出现了 `> right` 的数，这个子数组就永远不可能满足条件（因为最大值已经超出上限）。因此，这些元素天然把数组切成了若干 **段**，每段内部的所有元素都 `≤ right`。我们只需要在每段内部计数即可。

2. **小于 `left` 的元素**：在一个合法段（所有元素 `≤ right`）里，如果子数组的最大值 **小于 `left`**，同样不满足要求。于是我们可以把每段再细分为两类：
   - **包含至少一个 ≥ left 的子数组** → 合法  
   - **全都 < left** 的子数组 → 不合法  

   因此，**合法子数组数 = “所有 ≤ right 的子数组数” – “所有 < left 的子数组数”。**  

3. **如何快速统计“所有 ≤ bound 的子数组数”**  
   对任意上界 `bound`（比如 `right` 或 `left-1`），只要遍历一次数组，统计连续的 **满足 ≤ bound** 的片段长度 `len`，该片段内的子数组数为 `len * (len + 1) // 2`（等差数列求和）。这一步只需要 O(n) 时间。

把上面的两点结合，就得到线性时间解：

```
count(≤ right) - count(< left)   // 注意 < left 等价于 ≤ (left-1)
```

> **类比**：把数组想象成一条河流，`right` 是上游的大闸门，水位超过它就会被拦住，形成独立的水池；而 `left` 是下游的最小流量阈值，只有水池里至少有一次“大浪”（≥ left）才算有价值的水流。我们先算所有不被上闸挡住的水流（≤ right），再减去那些从未出现“大浪”的水流（< left）。

#### 代码（Python）

```python
def count_subarrays_opt(nums, left, right):
    """
    统计满足 max(nums[i..j]) 在 [left, right] 区间的子数组个数
    思路：count(≤ right) - count(< left)
    """
    def count_le(bound: int) -> int:
        """
        统计所有子数组的最大值 <= bound 的个数
        只需要遍历一次，累计连续满足 condition 的段长度。
        """
        total = 0          # 累计满足条件的子数组总数
        cur_len = 0        # 当前连续段的长度
        for x in nums:
            if x <= bound:                 # 仍在合法段内
                cur_len += 1               # 段长度加 1
                total += cur_len           # 以当前元素结尾的子数组数量就是段长度
            else:                           # 超出 bound，段结束
                cur_len = 0                # 重置段长度
        return total

    # 所有子数组最大值 <= right
    le_right = count_le(right)
    # 所有子数组最大值 < left   →  等价于 <= (left-1)
    le_left_minus_one = count_le(left - 1)

    return le_right - le_left_minus_one
```

> **关键行解释**  
> - `cur_len += 1`：把当前元素加入到连续段，段长度自然加一。  
> - `total += cur_len`：以当前位置为右端点的子数组有 `cur_len` 种（从左端点往左数 1~cur_len），所以直接累计。  
> - 当遇到 `x > bound` 时，段被切断，`cur_len` 重新计数。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历数组两次（一次求 `≤ right`，一次求 `< left`），每次都是线性操作。相比于 `O(n²)` 的暴力解，速度提升了 **n 倍**（对 10⁵ 的数据轻松在毫秒级完成）。

- **空间复杂度**：`O(1)`  
  只使用了常数个计数变量，不依赖额外的数组或哈希表。

---

## 心得

- **核心技巧**：**利用上界把数组切段 + 前缀计数**（即 “计数 ≤ bound 的子数组数”），再通过差分得到目标区间的子数组数。  
- **适用的题型**  
  1. “子数组最大值/最小值在某区间” 类题目（如本题）。  
  2. “子数组和/乘积在某区间” 也可以用类似的前缀计数思路（配合滑动窗口或前缀和）。  
  3. “子数组中不出现特定元素” 或 “子数组中所有元素满足某个上界” 的计数问题。  
- **一句话总结**：**把 “在 [L,R] 之间” 拆成 “≤R” 减去 “<L”，用一次线性遍历统计每个上界的子数组数**。

---

## 反思

- **第一反应**：直接枚举子数组，写两层循环检查最大值。  
- **最容易踩的坑**  
  - 忘记排除 **全小于 `left`** 的子数组，导致计数偏大。  
  - 在统计 `≤ bound` 时误把 “以当前元素为右端点的子数组数” 当成 `cur_len`，实际应累计 `total += cur_len`。  
  - 当 `left = 0` 时，`left-1` 为 `-1`，`count_le(-1)` 必须返回 `0`（因为所有元素都 ≥0），代码实现中使用 `x <= bound` 自然满足这一点。  
- **下次类似题目**：**先问自己**——“有没有可以把条件拆成上下界的差分？”、“是否可以把数组划分为不超过上界的连续段？” 这两个问题的答案往往指向 **线性计数 + 差分** 的思路。