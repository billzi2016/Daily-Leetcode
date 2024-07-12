# #2772. 通过操作使所有数组元素变为零 / Apply Operations to Make All Array Elements Equal to Zero

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-make-all-array-elements-equal-to-zero/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and a positive integer k.
You can apply the following operation on the array any number of times:
Return true if you can make all the array elements equal to 0, or false otherwise.
A subarray is a contiguous non-empty part of an array.

**Examples**

**Example 1:**

```
Input: nums = [2,2,3,1,1,0], k = 3
Output: true
Explanation: We can do the following operations:
- Choose the subarray [2,2,3]. The resulting array will be nums = [1,1,2,1,1,0].
- Choose the subarray [2,1,1]. The resulting array will be nums = [1,1,1,0,0,0].
- Choose the subarray [1,1,1]. The resulting array will be nums = [0,0,0,0,0,0].
```

**Example 2:**

```
Input: nums = [1,3,1,1], k = 2
Output: false
Explanation: It is not possible to make all the array elements equal to 0.
```

**Constraints**

- 1 <= k <= nums.length <= 105
- 0 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个正整数 `k`。你可以对数组任意次数地执行以下操作：

返回 `true` 若可以将所有数组元素全部变为 `0`，否则返回 `false`。

子数组（subarray）是数组中连续且非空的一段。

**示例 1**

```text
Input: nums = [2,2,3,1,1,0], k = 3
Output: true
Explanation: 我们可以按以下步骤进行操作：
- 选择子数组 [2,2,3]，得到的数组为 nums = [1,1,2,1,1,0]。
- 选择子数组 [2,1,1]，得到的数组为 nums = [1,1,1,0,0,0]。
- 选择子数组 [1,1,1]，得到的数组为 nums = [0,0,0,0,0,0]。
```

**示例 2**

```text
Input: nums = [1,3,1,1], k = 2
Output: false
Explanation: 无法通过上述操作使所有数组元素全部变为 0。
```

**约束条件**

- $1 \le k \le \text{nums.length} \le 10^{5}$
- $0 \le \text{nums}[i] \le 10^{6}$

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目给出的操作是：**任选一个长度恰好为 `k` 的连续子数组**，把子数组里的每个元素都减 1（前提是减完后仍然是非负的）。  
最直接的想法就是**一直遍历整个数组**，只要发现还有非零的元素，就随便挑一个长度为 `k` 的子数组，把它们全部减 1，重复这个过程直到所有元素都变成 0，或者找不到可以继续减的子数组就停下来。

可以把这个过程想象成 **“用水桶把水舀走”**：  
- 数组每个位置的数值是盛在小桶里的水量。  
- 一次操作就是把 **相邻 `k` 桶** 的水一起舀掉 1 升。  
- 暴力解就是不停地找一堆相邻的 `k` 桶，只要还有水，就一直舀，直到所有桶空了。

> **为什么这个方法能得到答案？**  
> 因为我们没有对操作做任何限制，只要能把所有水舀光，就一定可以实现；而暴力枚举所有可能的舀水顺序，必然包含一种可行的顺序（如果真的存在的话）。  

> **它的缺点是什么？**  
> - 每一次减 1 都要遍历一次数组，寻找一个合法的子数组。  
> - 如果某个位置的数值很大（比如 10⁶），我们可能需要对同一个位置执行上百万次减 1。  
> - 最坏情况下会把每个元素都减到 0，需要 **`max(nums) * n`** 次遍历，时间会爆炸。

#### 代码（Python）

```python
def can_make_zero_bruteforce(nums, k):
    n = len(nums)
    # 为了避免修改原数组，拷贝一份
    a = nums[:]

    # 只要还有非零元素，就继续循环
    while any(x > 0 for x in a):
        made_progress = False          # 本轮是否真的执行了一次减 1

        # 从左到右尝试每一个长度为 k 的子数组
        for i in range(n - k + 1):
            # 检查子数组里的每个元素是否都大于 0，只有这样才能减 1
            if all(a[j] > 0 for j in range(i, i + k)):
                # 把子数组里的每个元素都减 1
                for j in range(i, i + k):
                    a[j] -= 1
                made_progress = True
                break   # 只做一次减 1，重新从头开始检查
        # 如果一次也没有减，就说明卡住了，返回 False
        if not made_progress:
            return False
    return True
```

> **关键行解释**  
> - `any(x > 0 for x in a)`: 判断数组里是否还有正数。  
> - `all(a[j] > 0 for j in range(i, i + k))`: 确保选中的子数组里每个位置都还能减 1，避免出现负数。  
> - `for j in range(i, i + k): a[j] -= 1`: 真正执行“一次操作”。  

#### 复杂度  

- **时间复杂度**：`O(max(nums) * n * k)`  
  - 最坏情况下，每次只能让左边第一个正数减 1，需要 `max(nums)` 次循环。  
  - 每一次循环我们要遍历所有可能的起始位置（`n`），并检查子数组长度 `k`。  
  - 用大白话说：如果数组里最大数是 100 万，数组长度是 10⁵，`k` 也是 10⁵，时间会是 **100 000 000 000 000** 次，根本跑不完。  

- **空间复杂度**：`O(1)`（只用了常数级别的额外变量）。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次只减 1，却要遍历整个数组去找可以减的子数组。  
实际上，如果我们在位置 `i` 看到一个正数 `v`，**唯一合理的做法**是立刻在以 `i` 为左端点的子数组 `[i, i+k-1]` 上减 `v` 次（因为以后再来减，只会更麻烦）。这是一种**贪心**策略：左到右逐个处理，每次把当前位置的剩余值一次性清零。

实现这种贪心需要记录**已经对后面的元素产生的累计减量**。常用的技巧是**差分数组（difference array）**或**滑动窗口计数**：

1. 维护一个变量 `cur`，表示截至当前位置 `i`，已经被前面操作“覆盖”了多少次减 1。  
2. 用一个长度为 `n` 的差分数组 `diff`，当我们在位置 `i` 开始一次减 `v` 的操作时，就把 `diff[i] += v`、`diff[i+k] -= v`（如果 `i+k` 在数组范围内）。这样在后续遍历时，`cur += diff[i]` 就能得到当前累计的减量。  
3. 计算 **实际剩余值**：`remain = nums[i] - cur`。  
   - 如果 `remain == 0`，说明已经被足够的操作覆盖，继续向右。  
   - 如果 `remain > 0`，我们必须在 `[i, i+k-1]` 再执行一次操作，减 `remain` 次。  
   - 如果 `i + k > n`（子数组超出边界）且 `remain > 0`，说明无法再覆盖这个位置，直接返回 `False`。  

这种做法一次遍历即可完成所有决定，时间是 **O(n)**，空间只需要额外的 `diff`（长度 `n+1`），即 **O(n)**（可以进一步把 `diff` 改成队列实现 O(1) 空间，但这里保持直观）。

**类比**：  
想象你在给一排房子供水，**每次打开阀门就会同时给连续 `k` 栋房子供 1 单位的水**。现在每栋房子已经有一定的水量（`nums[i]`），我们想把所有水抽干。我们从左边第一栋房子开始检查，如果它还有水，就把阀门从这里打开，持续 `k` 栋，抽走它全部的水（`remain` 单位）。后面的房子会记下这次抽水的“影响”，相当于在它们的水表上减去相同的量。于是我们只需要一次遍历就能决定所有阀门的开启时机。

#### 代码（Python）

```python
def can_make_zero(nums, k):
    """
    贪心 + 差分数组
    返回 True 表示可以把所有元素减到 0，反之 False
    """
    n = len(nums)
    diff = [0] * (n + 1)      # 差分数组，diff[i] 表示从 i 开始的累计增量变化
    cur = 0                    # 当前累计的减量（相当于已经被前面操作覆盖的次数）

    for i in range(n):
        cur += diff[i]         # 把 i 位置的增量变化加入累计
        # 计算在已经执行的操作之后，位置 i 还剩多少
        remain = nums[i] - cur

        if remain < 0:         # 已经被减得比原来多，说明之前的操作导致负数，不合法
            return False

        if remain == 0:        # 已经是 0，无需再操作
            continue

        # 需要在以 i 为左端点的子数组上再减 remain 次
        if i + k > n:          # 子数组会越界，说明无法完成
            return False

        cur += remain          # 立即把这次操作的效果计入当前累计
        diff[i + k] -= remain  # 在子数组右边界之后抵消掉这部分累计

    return True
```

> **关键行解释**  
> - `diff = [0] * (n + 1)`: 多开一个位置方便在 `i+k` 位置做减法，不会越界。  
> - `cur += diff[i]`: 这一步把所有在位置 `i` 之前开始、在 `i` 仍然有效的操作累计起来。  
> - `remain = nums[i] - cur`: “实际还剩多少”，如果已经是 0，直接跳过。  
> - `if i + k > n: return False`: 说明以 `i` 为左端点的长度 `k` 子数组不存在，无法再减。  
> - `diff[i + k] -= remain`: 在子数组右边界记录一次“抵消”，等到遍历到 `i+k` 时 `cur` 会自动把这部分累计减掉，保证只在 `[i, i+k-1]` 区间生效。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每一步做常数次加减操作。  
  - 与暴力解的 `O(max(nums) * n * k)` 相比，提升了几个数量级，几乎可以在 10⁵ 规模的数据上瞬间跑完。  

- **空间复杂度**：`O(n)`（差分数组）  
  - 只需要额外的一个长度为 `n+1` 的整数数组。  
  - 如果再进一步使用滑动窗口队列记录 `remain`，可以把空间压到 `O(1)`，但对初学者来说差分数组更直观。

---

## 心得  

- **核心技巧**：**贪心 + 差分数组（或滑动窗口）**。  
  - 从左到右一次性把每个位置的剩余值清零，避免重复的微小操作。  
  - 差分数组帮助我们在 **O(1)** 时间内知道当前累计的减量，而不是每次都遍历 `k` 长度的子数组。  

- **适用的题型**  
  1. “区间增/减操作后判断可行性”——如 LeetCode 1665 *`Minimum Initial Energy to Finish Tasks`*（区间前缀和）  
  2. “需要把数组全部变为 0/1 的线性操作”——如 LeetCode 2135 *`Count Words Obtained After Adding a Letter`*（前缀差分）  
  3. “每次操作影响固定长度窗口”——如 LeetCode 995 *`Minimum Number of K Consecutive Bit Flips`*（滑动窗口差分）  

- **一句话总结解题钥匙**：  
  **“左边先解决，右边只记录影响”。**  

---

## 反思  

- **第一反应**：看到“选长度为 `k` 的子数组减 1”，立刻想到**暴力遍历**，因为最直接的想法就是“一次一次地把可以减的子数组找出来”。  
- **最容易踩的坑**  
  1. **负数检查**：如果累计的减量超过了原始值，会导致负数，需要提前返回 `False`。  
  2. **边界条件**：当 `i + k > n` 时仍有剩余值，这种情况必须返回 `False`，否则会访问越界的 `diff[i+k]`。  
  3. **大数溢出**：`nums[i]` 最大可达 `10⁶`，累计的 `cur` 可能很大，使用 Python 的 `int` 没问题，但在某些语言需要注意整数溢出。  

- **下次遇到同类题的第一步**：  
  **先判断是否可以用“从左到右一次性清零”** 的贪心策略，再决定使用差分数组或滑动窗口来记录区间影响，这样往往能把时间复杂度降到线性。