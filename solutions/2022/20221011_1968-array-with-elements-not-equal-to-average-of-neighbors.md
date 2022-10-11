# #1968. 数组中元素不等于相邻元素的平均值 / Array With Elements Not Equal to Average of Neighbors

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/array-with-elements-not-equal-to-average-of-neighbors/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of distinct integers. You want to rearrange the elements in the array such that every element in the rearranged array is not equal to the average of its neighbors.
More formally, the rearranged array should have the property such that for every i in the range 1 <= i < nums.length - 1, (nums[i-1] + nums[i+1]) / 2 is not equal to nums[i].
Return any rearrangement of nums that meets the requirements.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: [1,2,4,5,3]
Explanation:
When i=1, nums[i] = 2, and the average of its neighbors is (1+4) / 2 = 2.5.
When i=2, nums[i] = 4, and the average of its neighbors is (2+5) / 2 = 3.5.
When i=3, nums[i] = 5, and the average of its neighbors is (4+3) / 2 = 3.5.
```

**Example 2:**

```
Input: nums = [6,2,0,9,7]
Output: [9,7,6,2,0]
Explanation:
When i=1, nums[i] = 7, and the average of its neighbors is (9+6) / 2 = 7.5.
When i=2, nums[i] = 6, and the average of its neighbors is (7+2) / 2 = 4.5.
When i=3, nums[i] = 2, and the average of its neighbors is (6+0) / 2 = 3.
Note that the original array [6,2,0,9,7] also satisfies the conditions.
```

**Constraints**

- 3 <= nums.length <= 105
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始、元素互不相同的整数数组 `nums`。请重新排列数组中的元素，使得重新排列后的数组中每个元素都不等于其相邻两个元素的平均值（average）。

更形式化地，对于所有满足 `1 <= i < nums.length - 1` 的下标 `i`，都有：

\[
\frac{nums[i-1] + nums[i+1]}{2} \neq nums[i]
\]

返回任意一个满足上述要求的 `nums` 的重新排列。

---

## 示例

### 示例 1
**输入**  
`nums = [1,2,3,4,5]`

**输出**  
`[1,2,4,5,3]`

**解释**  
- 当 `i = 1` 时，`nums[i] = 2`，其相邻元素的平均值为 `(1 + 4) / 2 = 2.5`，不等于 `2`。  
- 当 `i = 2` 时，`nums[i] = 4`，其相邻元素的平均值为 `(2 + 5) / 2 = 3.5`，不等于 `4`。  
- 当 `i = 3` 时，`nums[i] = 5`，其相邻元素的平均值为 `(4 + 3) / 2 = 3.5`，不等于 `5`。

### 示例 2
**输入**  
`nums = [6,2,0,9,7]`

**输出**  
`[9,7,6,2,0]`

**解释**  
- 当 `i = 1` 时，`nums[i] = 7`，其相邻元素的平均值为 `(9 + 6) / 2 = 7.5`，不等于 `7`。  
- 当 `i = 2` 时，`nums[i] = 6`，其相邻元素的平均值为 `(7 + 2) / 2 = 4.5`，不等于 `6`。  
- 当 `i = 3` 时，`nums[i] = 2`，其相邻元素的平均值为 `(6 + 0) / 2 = 3`，不等于 `2`。  

注意，原数组 `[6,2,0,9,7]` 本身也满足条件。

---

## 约束条件

- `3 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `nums` 中的所有元素互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的排列全部枚举出来**，然后把每一种排列都检验一遍，看看是否满足  

```
对于所有 1 ≤ i < n‑1 ：
    (arr[i‑1] + arr[i+1]) / 2 ≠ arr[i]
```

- **用到的数据结构**  
  - **数组**：用来存放当前的排列。  
  - **哈希表（字典）**（可选）：记录哪些元素已经被使用，类似于查字典，键是数字，值是“已用/未用”。  

- **为什么它是正确的**  
  把所有排列都尝试一遍，肯定不会漏掉任何满足条件的答案。只要遍历到一个合法的排列，就可以直接返回。

- **时间/空间复杂度的大白话解释**  
  - **时间**：枚举 `n!`（n 的阶乘）种排列，每种排列要检查 `n` 次，所以大约是 `n! × n` 次操作。  
    用大白话说，就是 **“随便多少个数字都要尝遍所有顺序，根本不可行”**，尤其是 `n` 可能高达 `10⁵`。  
  - **空间**：递归或回溯的栈深度是 `n`，再加上保存一个排列的数组，也是 `O(n)`，也就是 **“和原数组一样大的额外空间”**。

#### 代码（Python）

```python
from typing import List

def rearrange_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    used = [False] * n                 # 标记哪些位置的数字已经被放进了当前排列
    cur = [0] * n                      # 正在构造的排列

    # 检查当前已经放好的前缀是否已经违背条件
    def ok_prefix(idx: int) -> bool:
        # 只需要检查 idx-1 位置，因为它的左右邻居已经确定
        if idx >= 2:
            left, mid, right = cur[idx-2], cur[idx-1], cur[idx]
            if (left + right) / 2 == mid:
                return False
        return True

    # 深度优先搜索所有排列
    def dfs(pos: int) -> List[int] | None:
        if pos == n:                    # 已经排满
            return cur.copy()
        for i in range(n):
            if not used[i]:
                cur[pos] = nums[i]
                used[i] = True
                # 只在前缀合法时继续深入
                if pos < 2 or ok_prefix(pos):
                    res = dfs(pos + 1)
                    if res:               # 找到合法解，直接返回
                        return res
                used[i] = False          # 回溯
        return None

    return dfs(0)   # 可能返回 None（理论上题目保证一定有解）
```

> **提示**：这段代码只适合 **极小** 的输入（比如 `n ≤ 8`）调试思路，实际提交会超时。

#### 复杂度  

- **时间复杂度**：`O(n! × n)`  
  - “阶乘”增长极快，哪怕 `n = 12` 也已经是几百亿次操作，根本跑不完。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的数组和递归栈。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于 **枚举所有排列**，我们需要 **直接构造** 一个必然合法的排列，而不是去尝试。  

观察题目条件：

> 对于某个位置 `i`，如果左邻居 `< nums[i] < 右邻居`（或相反），那么 `nums[i]` 正好是左、右两数的平均数。  
> 换句话说，**只要一个数的两个邻居分别在它的左边和右边（大小关系相反），它就会成为“中间数”**。

因此，只要我们 **把数组划分成两块**，一块全是“小数”，另一块全是“大数”，交错放置，就可以避免出现“小‑中‑大”或“大‑中‑小”的三元组，从而保证 **没有元素是其左右邻居的平均数**。

**具体做法**  

1. **先排序**：把所有数从小到大排好序。  
2. **找中位数**（或说“划分点”）  
   - 设 `mid = n // 2`（向下取整）。  
   - 前 `mid` 个是“小数”，后 `n-mid` 个是“大数”。  
3. **交错填充**  
   - **奇数下标（1,3,5,…）** 放“小数”。  
   - **偶数下标（0,2,4,…）** 放“大数”。  
   - 这样得到的序列形如 `大, 小, 大, 小, …`（如果 `n` 为奇数，最后一个位置会是“大”）。  

**为什么一定合法？**  

- 任意相邻的两数必然是 **大小相反**（大‑小 或 小‑大）。  
- 对于中间位置 `i`（既不是首也不是尾），左邻居和右邻居必然 **同属于同一组**（都是“大”或都是“小”），而 `nums[i]` 来自 **另一组**。  
- 于是左、右两数要么都 **大于** `nums[i]`，要么都 **小于** `nums[i]`，**不可能一大一小**。  
- 由于左、右两数同向（都大或都小），它们的平均数也会同向（仍然大于或小于 `nums[i]`），**不可能等于 `nums[i]`**。  

这样，**每一个内部位置都满足题目要求**，整个数组就是合法答案。

> **类比**：把数字想象成 **不同高度的砖块**。我们把高砖块放在偶数位置，低砖块放在奇数位置，任何一块砖的左右两块要么都是高的，要么都是低的，根本不可能正好在它的中间。

#### 代码（Python）

```python
from typing import List

def rearrange_optimal(nums: List[int]) -> List[int]:
    n = len(nums)
    nums.sort()                     # 1️⃣ 先排序，得到从小到大的序列
    mid = n // 2                    # 2️⃣ 分割点，左边是“小”，右边是“大”

    # 3️⃣ 创建结果数组，先全部填充占位符
    res = [0] * n

    # 下面把“大”放到偶数位（0,2,4,…），把“小”放到奇数位（1,3,5,…）
    # 大数从中位数开始往后取，保证每次取的都是当前剩余的最大数
    big_idx = mid                   # 第一个“大”在 nums[mid]
    small_idx = 0                   # 第一个“小”在 nums[0]

    for i in range(n):
        if i % 2 == 0:              # 偶数下标 → 放“大”
            res[i] = nums[big_idx]
            big_idx += 1
        else:                       # 奇数下标 → 放“小”
            res[i] = nums[small_idx]
            small_idx += 1

    return res
```

> **细节**：  
> - 当 `n` 为奇数时，`mid = n//2` 会使“大”这边的元素比“小”多一个，这正好填满最后的偶数位。  
> - 题目保证所有数字互不相同，所以不会出现“相等导致平均数相同”的特殊情况。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要花在排序上（`n log n`），后面的交错填充只需要线性遍历 `n` 次。  
  - 与暴力解相比，**从不可接受的阶乘级别降到了对数线性级别**，即使 `n = 10⁵` 也能在毫秒级完成。  

- **空间复杂度**：`O(n)`  
  - 需要额外的结果数组 `res`，大小和原数组相同。  
  - 如果允许“原地改写”，可以把 `nums` 本身当作 `res`，空间还能再降到 `O(1)`（不计递归栈）。

---

## 心得  

- **核心技巧**：**把数组分成两半交错排列**（也叫 “wiggle sort” 的一种变体），利用“大小同向”来避免出现 “左小右大” 的三元组，从而保证中间元素不可能是两端的平均数。  
- **适用的题型**（类似思路）  
  1. **摆动排序（Wiggle Sort）**：让 `nums[0] < nums[1] > nums[2] < nums[3] …`。  
  2. **避免等差数列**：把数组划分后交错，可防止连续三数形成等差。  
  3. **数组重排使相邻差最大化**：同样可以先排序再交错放置。  
- **一句话总结解题钥匙**：**把“大”和“小”交错摆放，使每个元素的左右邻居永远在同一侧（全大或全小），从而彻底堵住“平均数”这条路。**

---

## 反思  

- **第一反应**：想到 “遍历所有排列”——对所有可能都尝试一次，直观但完全不可行。  
- **最容易踩的坑**  
  - **边界**：数组长度最小是 3，必须确保奇偶交错时不会出现越界。  
  - **奇数长度**：大数会比小数多一个，需要把多出的那个大数放在最后的偶数位，代码中 `mid = n // 2` 正好处理了。  
  - **重复元素**：题目保证元素互不相同，若出现重复则需要额外处理，否则可能出现 “左小右大但相等导致平均数相等” 的情况。  
- **下次遇到同类题**，**第一步** 就是 **“把数组排序后交错放置”**，或先思考如何让相邻元素的大小关系保持一致，从而避免出现“中间值等于两端的平均数”。