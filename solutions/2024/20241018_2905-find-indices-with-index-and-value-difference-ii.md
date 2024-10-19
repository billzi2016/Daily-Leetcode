# #2905. 寻找满足索引差和值差的下标 II / Find Indices With Index and Value Difference II

> 难度：中等 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/find-indices-with-index-and-value-difference-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums having length n, an integer indexDifference, and an integer valueDifference.
Your task is to find two indices i and j, both in the range [0, n - 1], that satisfy the following conditions:
Return an integer array answer, where answer = [i, j] if there are two such indices, and answer = [-1, -1] otherwise. If there are multiple choices for the two indices, return any of them.
Note: i and j may be equal.

**Examples**

**Example 1:**

```
Input: nums = [5,1,4,1], indexDifference = 2, valueDifference = 4
Output: [0,3]
Explanation: In this example, i = 0 and j = 3 can be selected.
abs(0 - 3) >= 2 and abs(nums[0] - nums[3]) >= 4.
Hence, a valid answer is [0,3].
[3,0] is also a valid answer.
```

**Example 2:**

```
Input: nums = [2,1], indexDifference = 0, valueDifference = 0
Output: [0,0]
Explanation: In this example, i = 0 and j = 0 can be selected.
abs(0 - 0) >= 0 and abs(nums[0] - nums[0]) >= 0.
Hence, a valid answer is [0,0].
Other valid answers are [0,1], [1,0], and [1,1].
```

**Example 3:**

```
Input: nums = [1,2,3], indexDifference = 2, valueDifference = 4
Output: [-1,-1]
Explanation: In this example, it can be shown that it is impossible to find two indices that satisfy both conditions.
Hence, [-1,-1] is returned.
```

**Constraints**

- 1 <= n == nums.length <= 105
- 0 <= nums[i] <= 109
- 0 <= indexDifference <= 105
- 0 <= valueDifference <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`（长度为 `n`），以及整数 `indexDifference` 与 `valueDifference`。  
请找出两个下标 `i` 与 `j`（均在区间 `[0, n - 1]`）使得它们满足以下条件：

- `abs(i - j) >= indexDifference`，即下标之差的绝对值不少于 `indexDifference`；
- `abs(nums[i] - nums[j]) >= valueDifference`，即对应元素值之差的绝对值不少于 `valueDifference`。

返回一个整数数组 `answer`：

- 若存在满足条件的下标对，则 `answer = [i, j]`（任意一组即可）；
- 若不存在，则返回 `answer = [-1, -1]`。

**注意**：`i` 与 `j` 可以相等。

---

### 示例

**示例 1**  
输入: `nums = [5,1,4,1]`, `indexDifference = 2`, `valueDifference = 4`  
输出: `[0,3]`  
解释: 在此示例中，可选下标 `i = 0` 与 `j = 3`。  
`abs(0 - 3) >= 2` 且 `abs(nums[0] - nums[3]) >= 4`，因此 `[0,3]` 为合法答案。  
`[3,0]` 也是合法答案。

**示例 2**  
输入: `nums = [2,1]`, `indexDifference = 0`, `valueDifference = 0`  
输出: `[0,0]`  
解释: 此例中可以选取 `i = 0` 与 `j = 0`。  
`abs(0 - 0) >= 0` 且 `abs(nums[0] - nums[0]) >= 0`，故 `[0,0]` 为合法答案。  
其他合法答案还有 `[0,1]`, `[1,0]`, `[1,1]`。

**示例 3**  
输入: `nums = [1,2,3]`, `indexDifference = 2`, `valueDifference = 4`  
输出: `[-1,-1]`  
解释: 在此例中可以证明不存在同时满足两条条件的下标对。  
因此返回 `[-1,-1]`。

---

### 约束条件

- `1 <= n == nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`
- `0 <= indexDifference <= 10^5`
- `0 <= valueDifference <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 **所有可能的下标对 (i, j)** 都枚举一遍，看看它们是否满足  
```
|i - j| >= indexDifference   且   |nums[i] - nums[j]| >= valueDifference
```
- 这里用到的唯一数据结构是 **两个嵌套的 for 循环**，相当于把数组看成一本厚厚的“字典”，我们把每一页 (i) 都和每一页 (j) 对比一次。  
- 为什么能得到正确答案？因为我们没有遗漏任何一对下标，满足条件的必然会被检查到。  

#### 代码（Python）  

```python
from typing import List

def findIndices(nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
    n = len(nums)

    # 特殊情况：如果 indexDifference==0 且 valueDifference==0，任意 (i,i) 都合法
    if indexDifference == 0 and valueDifference == 0:
        return [0, 0]

    # 暴力枚举所有 i、j
    for i in range(n):
        for j in range(n):
            # 先检查下标差是否够大
            if abs(i - j) >= indexDifference:
                # 再检查数值差是否够大
                if abs(nums[i] - nums[j]) >= valueDifference:
                    return [i, j]        # 找到第一组合法解直接返回
    # 没有任何合法组合
    return [-1, -1]
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - “平方”是什么意思？如果数组有 10 000 个元素，暴力会比较 10 000 × 10 000 = 1 亿 次，这在实际运行时会非常慢。  
- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量，和数组长度无关。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **每次都要把所有之前的下标重新遍历一遍**。  
我们注意到条件里有两个独立的约束：

1. **下标差**：`|i - j| >= indexDifference`  
   - 只要把 *i* 固定，合法的 *j* 必须在区间 `[0, i - indexDifference]`（如果 *j* 在左边）或 `[i + indexDifference, n-1]`（如果 *j* 在右边）。  
2. **数值差**：`|nums[i] - nums[j]| >= valueDifference`  
   - 只要我们知道在合法的 *j* 区间里 **最小的数** 和 **最大的数** 分别是多少，就能立刻判断是否满足数值差。  
   - 因为如果 `nums[i]` 与区间最小值的差已经 ≥ `valueDifference`，那么它必然也与所有更小的数（不存在）满足；同理，和最大值的差也一样。

所以关键是**快速获取区间 `[0, i-indexDifference]` 的最小值、最大值以及对应的下标**。  
这可以用 **前缀最小/最大** 来实现：

- `pref_min_val[i]` = `min(nums[0..i])`，`pref_min_idx[i]` = 产生该最小值的下标。  
- `pref_max_val[i]` = `max(nums[0..i])`，`pref_max_idx[i]` = 产生该最大值的下标。  

有了这两个数组，遍历 `i` 时，只要 `i-indexDifference >= 0`，我们就能在 **O(1)** 时间拿到合法左侧区间的最小/最大信息，随后检查两条数值差条件即可。

如果遍历完仍未找到合法对，则返回 `[-1,-1]`。  
（右侧区间的检查不必单独实现，因为当 `j` 在右侧时，最终会在遍历到那个 `j` 时变成 “左侧区间的 `i`”。）

**类比**：想象你在一本字典里找两个词的页码差和词长差。前缀最小/最大就像你事先把每一页之前的“最短词”和“最长词”记下来，查询时只要翻开当前页的前一页的记录就能立刻知道答案。

#### 代码（Python）  

```python
from typing import List

def findIndices(nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
    n = len(nums)

    # 0/0 的特殊情况，任意 (i,i) 都合法，直接返回最小下标即可
    if indexDifference == 0 and valueDifference == 0:
        return [0, 0]

    # ---------- 预处理前缀最小 / 最大 ----------
    pref_min_val = [0] * n          # 前缀最小值
    pref_min_idx = [0] * n          # 对应的下标
    pref_max_val = [0] * n          # 前缀最大值
    pref_max_idx = [0] * n          # 对应的下标

    cur_min = nums[0]
    cur_min_idx = 0
    cur_max = nums[0]
    cur_max_idx = 0

    for i in range(n):
        # 更新前缀最小
        if nums[i] < cur_min:
            cur_min = nums[i]
            cur_min_idx = i
        pref_min_val[i] = cur_min
        pref_min_idx[i] = cur_min_idx

        # 更新前缀最大
        if nums[i] > cur_max:
            cur_max = nums[i]
            cur_max_idx = i
        pref_max_val[i] = cur_max
        pref_max_idx[i] = cur_max_idx
    # -----------------------------------------

    # ---------- 主循环：遍历 i ----------
    for i in range(n):
        # 必须保证左侧有足够的距离
        left = i - indexDifference
        if left < 0:
            continue          # 还没有到可以配对的 i

        # 取左侧区间的最小/最大及其下标
        min_val = pref_min_val[left]
        min_idx = pref_min_idx[left]
        max_val = pref_max_val[left]
        max_idx = pref_max_idx[left]

        # 检查与最小值的差
        if abs(nums[i] - min_val) >= valueDifference:
            return [min_idx, i]      # (min_idx, i) 满足所有条件

        # 检查与最大值的差
        if abs(nums[i] - max_val) >= valueDifference:
            return [max_idx, i]      # (max_idx, i) 同样合法
    # -----------------------------------------

    # 没有任何合法组合
    return [-1, -1]
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历两遍数组：一次构造前缀最小/最大，第二次检查每个 `i`。相比暴力的 `n²`，即使 `n=10⁵` 也能在毫秒级完成。  
- **空间复杂度：** `O(n)`（也可以优化到 `O(1)`）  
  - 我们用了四个长度为 `n` 的数组来保存前缀信息。若只想要 `O(1)`，可以在遍历时维护当前窗口的最小/最大以及对应下标——思路相同，只是实现稍微繁琐。  

---

## 心得  

- **核心技巧**：利用**前缀最小/最大**（或滑动窗口的最值维护）把“在一定范围内找最大/最小”从 `O(k)` 降到 `O(1)`。  
- **适用的题型**  
  1. “在满足下标距离的前提下，判断数值差是否足够”——如本题、LeetCode 2391 *“Minimize Maximum of Two Numbers”* 的变形。  
  2. “区间内的极值查询”——比如 “Maximum Subarray Sum with Length Constraint”。  
  3. “滑动窗口最大/最小值”——经典题目 *239. Sliding Window Maximum*。  
- **一句话总结解题钥匙**：**把“在某段区间里找最大/最小”提前预处理（前缀或单调队列），每次查询就能 O(1) 完成。**

---

## 反思  

- **第一反应**：看到两个 `abs` 条件，立刻想到“双层循环遍历所有下标”。这虽然正确，却极慢。  
- **最容易踩的坑**  
  1. **下标差为 0** 时需要允许 `i == j`，否则会错过合法答案（如示例 2）。  
  2. **valueDifference 为 0** 时，只要满足下标差即可，同样要记得 `i == j` 的情况。  
  3. **边界检查**：在遍历 `i` 时必须先确认 `i - indexDifference >= 0`，否则会访问负下标。  
- **下次遇到类似题**：第一步先思考 **“能否把区间极值提前算好”**，如果可以，就立刻转向前缀/单调队列等 **O(1) 查询** 的方案，而不是直接暴力。