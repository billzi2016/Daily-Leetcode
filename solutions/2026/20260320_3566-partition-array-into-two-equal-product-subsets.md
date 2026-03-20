# #3566. 将数组划分为两个等积子集 / Partition Array into Two Equal Product Subsets

> 难度：中等 · 标签：Array、Bit Manipulation、Recursion、Enumeration · [LeetCode 链接](https://leetcode.com/problems/partition-array-into-two-equal-product-subsets/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums containing distinct positive integers and an integer target.
Determine if you can partition nums into two non-empty disjoint subsets, with each element belonging to exactly one subset, such that the product of the elements in each subset is equal to target.
Return true if such a partition exists and false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [3,1,6,8,4], target = 24
Output: true
Explanation: The subsets [3, 8] and [1, 6, 4] each have a product of 24. Hence, the output is true.
```

**Example 2:**

```
Input: nums = [2,5,3,7], target = 15
Output: false
Explanation: There is no way to partition nums into two non-empty disjoint subsets such that both subsets have a product of 15. Hence, the output is false.
```

**Constraints**

- 3 <= nums.length <= 12
- 1 <= target <= 1015
- 1 <= nums[i] <= 100
- All elements of nums are distinct.

---

## 题目（中文翻译）

给定一个包含互不相同的正整数（distinct positive integers）的整数数组（integer array）`nums` 和一个整数 `target`。  
判断是否可以将 `nums` 划分为两个 **非空且两两不相交的子集（non‑empty disjoint subsets）**，使得每个子集中的元素的 **乘积（product）** 都等于 `target`。  
若存在这样的划分，返回 `true`；否则返回 `false`。

**示例 1**  
**输入**: `nums = [3,1,6,8,4]`, `target = 24`  
**输出**: `true`  
**解释**: 子集 `[3, 8]` 与子集 `[1, 6, 4]` 的乘积均为 24。因此返回 `true`。

**示例 2**  
**输入**: `nums = [2,5,3,7]`, `target = 15`  
**输出**: `false`  
**解释**: 无法将 `nums` 划分为两个非空且两两不相交的子集，使得两个子集的乘积都等于 15。故返回 `false`。

**约束条件**  
- `3 <= nums.length <= 12`  
- `1 <= target <= 10^15`  
- `1 <= nums[i] <= 100`  
- `nums` 中的所有元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组 `nums` 的所有可能的子集都枚举一遍，然后检查是否存在 **两个不相交且非空** 的子集，使得它们的元素乘积都恰好等于 `target`。  

- **子集**可以用 **位掩码（bitmask）** 来表示：  
  - 把数组下标 `0 … n-1` 看成二进制的每一位，`1` 表示把对应的元素放进子集，`0` 表示不放。  
  - 例如 `nums = [3,1,6,8,4]`，掩码 `0b10101`（十进制 21）对应的子集是 `{3,6,4}`（因为第 0、2、4 位为 1）。  
  - 位掩码就像一本字典，**key** 是“哪几个位置被选中”，**value** 是对应的子集。  

- 对每一个非空子集 `mask1`，我们可以直接算出它的乘积 `prod1`。如果 `prod1 != target`，说明它根本不符合要求，直接跳过。  
- 当 `prod1 == target` 时，剩下的元素形成的集合可以用 `mask2 = full_mask ^ mask1`（异或）表示（`full_mask` 是全部元素全选的掩码）。我们只需要在 `mask2` 的子集中再找一个乘积等于 `target` 的 **非空子集** 即可。  

因为 `nums` 的长度最多只有 **12**，所有子集的数量是 `2^12 = 4096`，完全可以在毫秒级遍历完。

#### 代码（Python）

```python
from typing import List

def can_partition(nums: List[int], target: int) -> bool:
    n = len(nums)
    full_mask = (1 << n) - 1          # 全部元素对应的位掩码，例如 n=5 时为 0b11111

    # 预先把每个子集的乘积算好，存到字典 product_of_mask 中
    # product_of_mask[mask] = 子集 mask 的乘积（如果乘积已经超过 target，就记为 None，后面直接跳过）
    product_of_mask = {}
    for mask in range(1, 1 << n):      # 从 1 开始，跳过空子集
        prod = 1
        for i in range(n):
            if mask >> i & 1:          # 第 i 位为 1，说明选了 nums[i]
                prod *= nums[i]
                if prod > target:      # 超过 target 已经不可能相等，提前终止
                    prod = None
                    break
        product_of_mask[mask] = prod

    # 枚举第一个子集 mask1
    for mask1, prod1 in product_of_mask.items():
        if prod1 != target:            # 不是我们想要的乘积，直接跳过
            continue

        # 剩余元素的掩码
        remaining = full_mask ^ mask1
        # 在剩余元素的所有非空子集中寻找乘积等于 target 的子集 mask2
        sub = remaining
        while sub:
            if product_of_mask.get(sub) == target:
                # 找到两个非空且不相交的子集
                return True
            sub = (sub - 1) & remaining   # 枚举 remaining 的下一个子集（技巧：子集遍历）
    return False
```

> **关键行解释**  
> - `mask >> i & 1`：判断第 `i` 位是否为 1，相当于检查 “这件商品是否被放进购物车”。  
> - `while sub:` 循环中使用 `(sub - 1) & remaining` 能在 **O(2^k)**（k 为剩余元素个数）时间内遍历 `remaining` 的所有子集，这是一种常用的位运算技巧。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - 枚举所有子集需要 `2^n` 次；对每个子集我们最多遍历 `n` 位来计算乘积。这里的 `n ≤ 12`，所以最多约 `4096 * 12 ≈ 5·10^4` 次运算，几乎是瞬间完成。  
  - 大白话：`2^n` 就像把每件商品都决定“买”或“不买”，所有可能的组合数随商品数指数增长。因为商品最多只有 12 件，组合数仍然是几千，算得动。

- **空间复杂度**：`O(2^n)`  
  - 用一个字典保存每个子集的乘积，最多存 `2^n` 条记录。相当于为每一种组合准备了一张小卡片，记录它的总价（这里是乘积）。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经能在题目限制下跑完，但它仍然会 **重复计算**：  
- 当我们枚举 `mask1` 后，再去遍历 `remaining` 的所有子集 `mask2`，其实已经在之前的遍历里算过了。  
- 这相当于在“买东西”时，两次遍历同一批商品的所有组合，浪费了一半的时间。

**优化方向**：把所有子集的乘积一次性算好，然后把“乘积等于 target 的子集”收集起来，最后只要检查这两个集合是否 **可以互相不相交** 即可。

具体步骤：

1. **一次遍历**所有子集，记录下乘积恰好等于 `target` 的子集掩码，放进列表 `valid_masks`。  
2. 对 `valid_masks` 中的每一对掩码 `(a, b)`，判断它们是否 **不相交**（`a & b == 0`），且两者都非空。只要出现一对满足条件，就返回 `True`。  
3. 为了避免 `O(k^2)`（k 为满足乘积条件的子集数量） 的双重循环，我们可以把 `valid_masks` 按 **位数**（子集大小）分桶，或者直接使用 **哈希集合** 检查互斥性。这里因为 `n ≤ 12`，`k` 最多也只有几百，直接双层遍历仍然足够快。  

> **为什么这样更快？**  
> - 只算了一遍乘积（`O(2^n * n)`），之后的检查只涉及位运算（`O(1)`），没有再次遍历子集。整体时间仍是 `O(2^n * n)`，但常数更小，实际运行更快。

#### 代码（Python）

```python
from typing import List

def can_partition_opt(nums: List[int], target: int) -> bool:
    n = len(nums)
    full_mask = (1 << n) - 1

    # 1. 收集所有乘积恰好等于 target 的子集掩码
    valid_masks = []
    for mask in range(1, 1 << n):          # 跳过空子集
        prod = 1
        for i in range(n):
            if mask >> i & 1:
                prod *= nums[i]
                if prod > target:         # 提前剪枝
                    prod = None
                    break
        if prod == target:
            valid_masks.append(mask)

    # 2. 检查是否存在两两不相交的子集
    m = len(valid_masks)
    for i in range(m):
        for j in range(i + 1, m):
            if valid_masks[i] & valid_masks[j] == 0:   # 位与为 0 表示不相交
                # 这里已经保证两子集都非空，因为 mask 从 1 开始枚举
                return True
    return False
```

> **关键行解释**  
> - `mask >> i & 1` 同上，判断第 `i` 位是否被选中。  
> - `valid_masks[i] & valid_masks[j] == 0`：如果两套商品的选择位没有交叉，就说明它们可以分别组成两组，互不重叠。  
> - 双层循环最多 `k(k-1)/2` 次，`k` 在本题最多约 `C(12,6)=924`（所有子集都满足乘积），仍在毫秒级。

#### 复杂度  

- **时间复杂度**：`O(2^n * n + k^2)`  
  - 第一次遍历所有子集仍是 `2^n * n`，这一步不可避免。  
  - `k` 是满足乘积条件的子集数，`k ≤ 2^n`，在最坏情况下 `k^2` 也是 `2^{2n}`，但实际 `target` 的限制让 `k` 很小（尤其是乘积容易超过 `10^15`），所以整体仍是 **线性指数**，在本题约 `5·10^4 + 1e5` 级别，远低于时间限制。  
  - 相比暴力解，省掉了每次 `mask1` 再遍历 `remaining` 子集的额外 `2^{|remaining|}` 步。

- **空间复杂度**：`O(k)`（存放满足条件的掩码）  
  - 最多 `k ≤ 2^n`，在本题最多几千个整数，几乎可以忽略。

---

## 心得

- **核心技巧**：**位掩码枚举子集 + 乘积剪枝 + 检查子集不相交**。  
- 这种技巧适用于所有 **“把集合划分成若干组，使每组满足某个数值条件”** 的题目，例如：  
  1. *Partition Equal Subset Sum*（把数组划分成和相等的两组）——使用位掩码或动态规划。  
  2. *Maximum Product of Word Lengths*（找两个单词字符集合不交叉且乘积最大）——同样用位掩码判断交集。  
  3. *Subsets With Product Less Than K*（统计乘积小于 K 的子集）——位枚举结合剪枝。  

- **一句话总结**：**先把所有满足条件的子集列出来，再用位运算快速判断它们能否互不重叠**。

---

## 反思

- **第一反应**：看到“乘积 = target”，立刻想到 **枚举子集**，因为乘积不像求和那样可以用前缀和简化。  
- **最容易踩的坑**：  
  1. **乘积溢出**：在 Python 中整数不溢出，但乘积可能会非常大，导致不必要的计算。使用 `if prod > target: break` 可以提前剪枝。  
  2. **空子集**：题目要求两边都非空，记得在遍历时跳过 `mask = 0`。  
  3. **重复计数**：如果直接在遍历 `mask1` 时再次遍历 `remaining` 的子集，会产生大量重复工作，导致运行慢。  

- **下次类似题**：**第一步**先思考“是否可以把所有满足目标条件的子集一次性列出来”，然后再判断它们之间的 **相容性（是否相交）**。这样往往能把复杂度降到可接受的范围。