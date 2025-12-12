# #3452. 好数之和 / Sum of Good Numbers

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/sum-of-good-numbers/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer k, an element nums[i] is considered good if it is strictly greater than the elements at indices i - k and i + k (if those indices exist). If neither of these indices exists, nums[i] is still considered good.
Return the sum of all the good elements in the array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,1,5,4], k = 2
Output: 12
Explanation:
The good numbers are nums[1] = 3 , nums[4] = 5 , and nums[5] = 4 because they are strictly greater than the numbers at indices i - k and i + k .
```

**Example 2:**

```
Input: nums = [2,1], k = 1
Output: 2
Explanation:
The only good number is nums[0] = 2 because it is strictly greater than nums[1] .
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 1000
- 1 <= k <= floor(nums.length / 2)

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，如果元素 `nums[i]` 严格大于索引 `i - k` 和 `i + k` 处的元素（前提是这些索引存在），则认为 `nums[i]` 是 **好数**（good number）。如果这两个索引都不存在，`nums[i]` 仍然视为好数。  
返回数组中所有好数的和。

**示例 1**

```
Input: nums = [1,3,2,1,5,4], k = 2
Output: 12
Explanation:
好数为 nums[1] = 3、nums[4] = 5 和 nums[5] = 4，因为它们严格大于索引 i - k 和 i + k 处的数。
```

**示例 2**

```
Input: nums = [2,1], k = 1
Output: 2
Explanation:
唯一的好数是 nums[0] = 2，因为它严格大于 nums[1]。
```

**约束条件**

- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 1000`
- `1 <= k <= floor(nums.length / 2)`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是**把每个位置的数都拿出来，分别和它左边第 `k` 个位置和右边第 `k` 个位置的数比较**。  

- **用到的数据结构**：只需要一个普通的 Python 列表 `nums`。列表就像一本装有很多格子的抽屉柜，`nums[i]` 就是第 `i` 格的东西，取值和写值都非常快。  
- **为什么这个方法正确**：题目只要求「严格大于」左/右第 `k` 个数（如果该位置存在）。只要我们把这两个数找出来并比较，就能判断 `nums[i]` 是否 “good”。  
- **时间/空间复杂度**：我们要遍历一遍数组，**每个元素只做常数次比较**（最多两次），所以时间是 `O(n)`（`n` 是数组长度）。`O(n)` 可以想象成“随数组大小线性增长”。空间只用了常数个额外变量，`O(1)`，即“几乎不占额外内存”。  

#### 代码（Python）  

```python
def sumGoodNumbers(nums, k):
    """
    返回所有 good 元素的和
    :param nums: List[int]   # 原始数组
    :param k: int           # 距离 k
    :return: int
    """
    n = len(nums)               # 数组长度
    total = 0                   # 累计答案

    for i in range(n):          # 依次检查每个下标 i
        left_ok = True          # 假设左侧满足条件
        right_ok = True         # 假设右侧满足条件

        # 检查左侧第 k 个位置是否存在且满足「严格大于」的要求
        if i - k >= 0:          # 左侧索引合法
            left_ok = nums[i] > nums[i - k]

        # 检查右侧第 k 个位置是否存在且满足「严格大于」的要求
        if i + k < n:           # 右侧索引合法
            right_ok = nums[i] > nums[i + k]

        # 同时满足左、右（或者对应方向根本不存在）即为 good
        if left_ok and right_ok:
            total += nums[i]    # 累加到答案

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 这里的 `n` 就是数组的长度。遍历一次数组，每个元素只做最多两次比较，花的时间随 `n` 成正比。  
- **空间复杂度**：`O(1)`  
  - 只用了几个额外的整型变量（`n、total、i、left_ok、right_ok`），不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
从暴力解来看，它已经是 **线性时间 `O(n)`**，这已经是最优的时间下界，因为我们必须**至少看一次每个元素**才能判断它是否 good。  

- **慢在哪里？**  
  - 这里没有真正的“慢点”。如果我们误以为要比较 `i` 左右 **所有** 距离 ≤ `k` 的元素，那会是 `O(n·k)`，会慢很多。  
- **一步步推导优化**  
  1. 认识到题目只要求比较 **恰好第 `k` 个** 左右元素，而不是全部 `k` 个。  
  2. 因此每次只需要取 `nums[i‑k]`（如果存在）和 `nums[i+k]`（如果存在）进行一次比较。  
  3. 直接在一次遍历中完成判断并累加即可。  
- **核心技巧**：**一次遍历 + 边界检查**。  
  - 边界检查可以类比为“看门人”，只有当左/右门（索引）真的开着（在数组范围内）时，才去比较。  

#### 代码（Python）  

```python
def sumGoodNumbers(nums, k):
    n = len(nums)
    ans = 0

    for i in range(n):
        # 只要左侧第 k 位存在且不满足「大于」条件，就直接跳过
        if i - k >= 0 and nums[i] <= nums[i - k]:
            continue
        # 同理，右侧第 k 位存在且不满足「大于」条件，也跳过
        if i + k < n and nums[i] <= nums[i + k]:
            continue
        # 走到这里说明 i 位置的数满足所有要求
        ans += nums[i]

    return ans
```

> **代码解释**  
> - 第 4 行 `for i in range(n):`：一次遍历所有下标。  
> - 第 6‑7 行：如果左侧第 `k` 位存在且 `nums[i]` **不** 大于它，直接 `continue`（相当于说“这肯定不是 good，下一轮”。）  
> - 第 9‑10 行：同理处理右侧。  
> - 第 12 行：只有左右都满足（或者对应方向根本不存在）才把 `nums[i]` 加到答案。  

#### 复杂度  

- **时间复杂度**：`O(n)` — 与暴力解相同，已是最优，因为必须检查每个元素一次。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量。  

---  

## 心得  

- **核心技巧**：**一次遍历 + 边界检查**（只比较恰好第 `k` 个左右元素）。  
- **适用的题型**：  
  1. “相邻/固定距离比较” 类题目，如 “检查数组中每个元素是否大于其左/右邻居”。  
  2. “窗口固定距离” 判断题，如 “数组中每个元素是否是其前后 `k` 位的最大值”。  
  3. “边界条件” 题目，例如 “只要左右都有元素且满足条件才计数”。  
- **一句话总结**：**只比较题目要求的那几个位置，别把范围扩大，时间自然线性**。  

---  

## 反思  

- **第一反应**：拿到题目后，我立刻想到“遍历数组、对每个位置检查左/右第 `k` 个数”。这就是最自然的思路。  
- **最容易踩的坑**：  
  - **越界**：`i‑k` 或 `i+k` 可能超出数组范围，需要先判断索引是否合法。  
  - **“不存在” 的情况**：如果左/右索引不存在，题目仍然视为 good，记得在代码中用 `True`（或直接跳过比较）来处理。  
- **下次遇到同类题**：第一步先**明确比较的具体位置**（是所有相邻、还是固定距离），然后**写出边界检查**，再决定是否需要更高级的数据结构。