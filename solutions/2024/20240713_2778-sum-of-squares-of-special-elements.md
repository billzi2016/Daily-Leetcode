# #2778. 特殊元素平方和 / Sum of Squares of Special Elements 

> 难度：简单 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/sum-of-squares-of-special-elements/)

---

## 题目（英文原版）

**Description**

You are given a 1-indexed integer array nums of length n.
An element nums[i] of nums is called special if i divides n, i.e. n % i == 0.
Return the sum of the squares of all special elements of nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 21
Explanation: There are exactly 3 special elements in nums: nums[1] since 1 divides 4, nums[2] since 2 divides 4, and nums[4] since 4 divides 4. 
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[4] * nums[4] = 1 * 1 + 2 * 2 + 4 * 4 = 21.
```

**Example 2:**

```
Input: nums = [2,7,1,19,18,3]
Output: 63
Explanation: There are exactly 4 special elements in nums: nums[1] since 1 divides 6, nums[2] since 2 divides 6, nums[3] since 3 divides 6, and nums[6] since 6 divides 6. 
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[3] * nums[3] + nums[6] * nums[6] = 2 * 2 + 7 * 7 + 1 * 1 + 3 * 3 = 63.
```

**Constraints**

- 1 <= nums.length == n <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个 **1-indexed** 整数数组 `nums`，长度为 `n`。  
如果下标 `i` 能整除 `n`（即 `n % i == 0`），则元素 `nums[i]` 被称为 **特殊元素**（special element）。  
返回所有特殊元素的平方和。

## 示例

### 示例 1
**输入**：`nums = [1,2,3,4]`  
**输出**：`21`  
**解释**：`nums` 中恰好有 3 个特殊元素：`nums[1]`（因为 `1` 整除 `4`）、`nums[2]`（因为 `2` 整除 `4`）以及 `nums[4]`（因为 `4` 整除 `4`）。  
因此，所有特殊元素的平方和为 `nums[1] * nums[1] + nums[2] * nums[2] + nums[4] * nums[4] = 1 * 1 + 2 * 2 + 4 * 4 = 21`。

### 示例 2
**输入**：`nums = [2,7,1,19,18,3]`  
**输出**：`63`  
**解释**：`nums` 中恰好有 4 个特殊元素：`nums[1]`（因为 `1` 整除 `6`）、`nums[2]`（因为 `2` 整除 `6`）、`nums[3]`（因为 `3` 整除 `6`）以及 `nums[6]`（因为 `6` 整除 `6`）。  
因此，所有特殊元素的平方和为 `nums[1] * nums[1] + nums[2] * nums[2] + nums[3] * nums[3] + nums[6] * nums[6] = 2 * 2 + 7 * 7 + 1 * 1 + 3 * 3 = 63`。

## 约束条件
- `1 <= nums.length == n <= 50`
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组 **全部遍历一遍**，每遍历到一个位置 `i`（注意题目是 1‑索引），判断它是不是“特殊”。  
- 判断方法：`n % i == 0`（`n` 是数组长度）。如果余数为 0，说明 `i` 能整除 `n`，即 `i` 是特殊下标。  
- 把对应的元素 `nums[i-1]`（因为 Python 的列表是 0‑索引）平方后累加到答案里。

> **类比**：把数组想成一本书的章节目录，`i` 就是章节号。只有章节号能整除总章节数（`n`）的章节，才算是“特殊章节”。我们把这些章节的页码（`nums[i]`）的平方加起来。

这个方法一定能得到正确答案，因为我们没有遗漏任何可能的下标，也没有多加不该加的下标。

#### 代码（Python）

```python
def sum_of_squares_special(nums):
    """
    暴力遍历全部下标，找出能整除 n 的下标并累计平方和
    :param nums: List[int]，题目给出的 1 索引数组（实际是 Python 的 0 索引列表）
    :return: int，所有特殊元素的平方和
    """
    n = len(nums)                     # 数组长度 n
    total = 0                         # 累计答案
    for i in range(1, n + 1):         # i 从 1 遍历到 n（因为是 1 索引）
        if n % i == 0:                # 判断 i 是否能整除 n
            val = nums[i - 1]         # Python 列表是 0 索引，需要减 1
            total += val * val        # 累加该元素的平方
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `O(n)` 表示我们最多遍历一次数组，`n` 最高只能是 50，几乎可以忽略不计。  
- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量（`total、i、val`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 `O(n)`，在本题的约束下已经足够快，但我们仍可以从 **“只遍历真正需要的下标”** 出发，进一步减少循环次数。

- **瓶颈**：暴力解每次都检查所有 `1 … n`，即使只有少数下标真正能整除 `n`。  
- **优化**：先 **求出 `n` 的所有约数**（即所有能整除 `n` 的下标），约数的个数远小于 `n`（最多 `≈ √n` 个），然后只遍历这些约数对应的元素即可。

**约数的获取方法**：  
遍历 `d` 从 `1` 到 `√n`（即 `int(n**0.5) + 1`），如果 `n % d == 0`，说明 `d` 是约数，同时 `n // d` 也是约数（可能相同）。把它们收集到列表里，最后遍历这些约数即可。

> **类比**：把 `n` 看成一把锁的齿轮，只有齿数能整除锁孔（`n`）的齿轮才能进入。我们先找出所有合适的齿轮（约数），再把对应的钥匙（数组元素）取出来用。

#### 代码（Python）

```python
def sum_of_squares_special_opt(nums):
    """
    只遍历 n 的约数（特殊下标），累计对应元素的平方和
    :param nums: List[int]
    :return: int
    """
    n = len(nums)
    divisors = []                     # 用来存所有能整除 n 的下标（1 索引）
    limit = int(n ** 0.5) + 1        # 只需要检查到 sqrt(n)

    for d in range(1, limit):
        if n % d == 0:                # d 是约数
            divisors.append(d)        # 添加 d 本身
            other = n // d
            if other != d:            # 防止重复（比如 n=9 时 d=3）
                divisors.append(other)

    total = 0
    for idx in divisors:              # 只遍历约数对应的下标
        val = nums[idx - 1]           # 仍需转成 0 索引
        total += val * val
    return total
```

#### 复杂度

- **时间复杂度**：`O(√n)`  
  我们只遍历到 `√n`（约 7 次，当 `n=50` 时），再遍历约数本身（最多 `2·√n`），所以整体是 `O(√n)`，比 `O(n)` 更快。  
- **空间复杂度**：`O(√n)`（约数列表）  
  约数数量与 `√n` 成正比，使用了额外的列表来保存它们。

> 与暴力解相比，最优解在 `n` 很大的情况下（比如 `10⁵`）会有明显提升；在本题的 50 上限里，两者运行时间几乎相同，但思路的提升对以后遇到更大规模的数据很有帮助。

---

## 心得

- **核心技巧**：**约数枚举**（利用平方根遍历）  
- **适用题型**：  
  1. “求所有能整除 `n` 的下标/元素的某种聚合”  
  2. “基于数组长度的约数进行分组/统计”  
  3. “求所有约数对应的数组值的最大/最小/和”等  
- **一句话总结**：先找出 **真正需要关注的下标（约数）**，再做计算，能把遍历次数从 `n` 降到 `√n`。

---

## 反思

- **第一反应**：直接遍历全部下标，用模运算判断是否特殊。  
- **最容易踩的坑**：  
  - 忘记题目是 **1 索引**，导致在 Python 中直接用 `nums[i]` 而不是 `nums[i-1]`。  
  - 当 `n` 为完全平方数时，约数 `√n` 会出现两次，需要去重。  
- **下次思考步骤**：  
  1. 判断题目是否涉及 “能整除” 或 “约数”。  
  2. 考虑是否可以 **只枚举约数** 而不是全部元素。  
  3. 再决定具体实现细节（遍历到 `√n`、收集约数、计算）。