# #3583. 计数特殊三元组 / Count Special Triplets

> 难度：中等 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/count-special-triplets/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
A special triplet is defined as a triplet of indices (i, j, k) such that:
Return the total number of special triplets in the array.
Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [6,3,6]
Output: 1
Explanation:
The only special triplet is (i, j, k) = (0, 1, 2) , where:
```

**Example 2:**

```
Input: nums = [0,1,0,0]
Output: 1
Explanation:
The only special triplet is (i, j, k) = (0, 2, 3) , where:
```

**Example 3:**

```
Input: nums = [8,4,2,8,4]
Output: 2
Explanation:
There are exactly two special triplets:
```

**Constraints**

- 3 <= n == nums.length <= 105
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`。  
若一组三元索引 `(i, j, k)` 满足以下条件，则称其为 **特殊三元组（special triplet）**：  

（题目原文中此处缺少具体条件，保持原样）

请返回数组中所有特殊三元组的总数。由于答案可能很大，请返回其对 `10^9 + 7` 取模后的结果。

**示例**  

*示例 1*  
```
Input: nums = [6,3,6]
Output: 1
Explanation:
唯一的特殊三元组是 (i, j, k) = (0, 1, 2) ，其中：
```

*示例 2*  
```
Input: nums = [0,1,0,0]
Output: 1
Explanation:
唯一的特殊三元组是 (i, j, k) = (0, 2, 3) ，其中：
```

*示例 3*  
```
Input: nums = [8,4,2,8,4]
Output: 2
Explanation:
恰好存在两个特殊三元组：
```

**约束条件**  

- `3 <= n == nums.length <= 10^5`  
- `0 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有可能的下标三元组 `(i, j, k)` 都枚举一遍，然后检查它们是否满足“特殊三元组”的定义：  

* `i < j < k`  
* `nums[i] == nums[k]`（左右两端的数相等）  
* `nums[i] == 2 * nums[j]`（左右两端的数恰好是中间数的两倍）  

可以把数组想象成一排座位，`i、j、k` 分别是坐在左、中、右的三个人。我们要找的正好是左边和右边的人的身高相同，而且恰好是中间那个人身高的两倍。  

把所有三元组都列出来，就像把所有可能的三个人组合都排一遍，检查每一组合是否满足条件。只要有一组满足，就把计数器加一。

> **为什么正确？**  
> 暴力枚举不遗漏任何下标组合，所有满足条件的三元组都会被检测到，自然得到正确答案。

> **时间/空间复杂度**  
> - 外层有 `n`（数组长度）个位置可以当 `i`，  
> - 中层还有 `n` 个位置可以当 `j`，  
> - 内层再有 `n` 个位置可以当 `k`。  
> 所以总共要检查大约 `n³` 次。  
> 大写的 **O(n³)** 其实就是 “n 的三次方”，比如 `n = 10⁵` 时，`10⁵³ = 10¹⁵`，这在电脑里根本跑不完。  
> - 空间上只用了常数个额外变量，**O(1)**。

#### 代码（Python）

```python
from typing import List

def countSpecialTriplets_bruteforce(nums: List[int]) -> int:
    MOD = 10**9 + 7
    n = len(nums)
    ans = 0
    # 枚举 i, j, k（i < j < k）
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                # 检查是否满足特殊三元组的条件
                if nums[i] == nums[k] and nums[i] == 2 * nums[j]:
                    ans = (ans + 1) % MOD   # 防止答案太大
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n³)` —— 需要遍历所有三元组，随着 `n` 增大，计算量呈立方增长。  
- **空间复杂度：** `O(1)` —— 只用了几个计数器，额外的存储几乎可以忽略不计。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们把每一个可能的 `i、j、k` 都尝试了一遍，而实际只需要关注满足条件的那一小部分。  

观察条件：

1. `nums[i]` 与 `nums[k]` 必须相等，记作 `value`。  
2. `value` 必须是 `nums[j]` 的两倍，即 `value = 2 * nums[j]`。  

把 `j` 当作“中间”位置来看，**只要知道在 `j` 左侧有多少个 `value = 2 * nums[j]`，以及在 `j` 右侧有多少个相同的 `value`，两者相乘就是以 `j` 为中间时可以组成的特殊三元组数目**。  

因此我们只要在遍历数组时，实时维护：

- `freqPrev[x]`：`x` 在当前位置左侧出现的次数（相当于左边的“字典”，key 是数值，value 是出现次数）。  
- `freqNext[x]`：`x` 在当前位置右侧（包括当前位置）出现的次数。最开始 `freqNext` 包含整个数组的频次，随后在遍历过程中逐步把当前元素从右侧移到左侧。  

遍历步骤：

1. 预先统计整个数组的出现次数得到 `freqNext`。  
2. 从左到右依次把每个位置 `j` 当作中间：  
   - 先把 `nums[j]` 从 `freqNext` 中减一，因为它已经不再属于“右侧”。  
   - 计算目标外层值 `target = 2 * nums[j]`。  
   - `left = freqPrev.get(target, 0)`：左侧等于 `target` 的个数。  
   - `right = freqNext.get(target, 0)`：右侧等于 `target` 的个数。  
   - `ans += left * right`（模 `1e9+7`），这就是所有以 `j` 为中间的合法三元组。  
   - 最后把 `nums[j]` 加入 `freqPrev`，准备进入下一个 `j`。  

这整个过程只遍历一次数组，所有操作都是 **O(1)** 的哈希表查询/更新，所以总时间是 **O(n)**，空间是保存两个频次数组/字典，最多 `O(max(nums))` 或 `O(n)`（两者在本题约为 `10⁵`），属于线性空间。

> **类比**：  
> 想象你在排队买票，左边已经买好票的人数是 `freqPrev`，右边还在排队的人数是 `freqNext`。每次轮到你（中间的 `j`）时，只需要看左边和右边各有多少人拿着同样的票（即外层值），左*右 就是你能和多少对朋友凑成“三人组”。  

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

MOD = 10**9 + 7

def countSpecialTriplets(nums: List[int]) -> int:
    """
    统计满足
        i < j < k,
        nums[i] == nums[k] == 2 * nums[j]
    的三元组数量，返回结果对 1e9+7 取模。
    """
    # 1. 构造右侧频次表（包括整个数组）
    freq_next = defaultdict(int)
    for x in nums:
        freq_next[x] += 1

    freq_prev = defaultdict(int)   # 左侧频次表，开始为空
    ans = 0

    # 2. 依次把每个位置当作 j（中间）
    for j, mid in enumerate(nums):
        # 当前元素已经不再属于「右侧」，先把它从 freq_next 中移除
        freq_next[mid] -= 1

        target = mid * 2                 # 外层需要的数值
        left  = freq_prev.get(target, 0) # 左侧有多少个 target
        right = freq_next.get(target, 0) # 右侧有多少个 target

        # 以 j 为中间的合法三元组数 = left * right
        ans = (ans + left * right) % MOD

        # 把当前元素加入左侧，准备处理下一个 j
        freq_prev[mid] += 1

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)` —— 只遍历一次数组，哈希表的增删查都是常数时间。相比暴力的 `O(n³)`，速度提升了几个数量级。  
- **空间复杂度：** `O(m)`，其中 `m` 是数组中不同数值的种类数（最坏情况下等于 `n`），在本题的约束 (`nums[i] ≤ 10⁵`) 下至多是 `10⁵`，属于线性空间。  

---

## 心得  

- **核心技巧**：利用「左侧/右侧频次统计」把三元组计数转化为两次一维计数的乘积。  
- **适用题型**：  
  1. 计数满足 `i < j < k` 且两端相等或满足某种函数关系的三元组（如「左侧等于右侧」的题目）。  
  2. 「以某个位置为中心」的计数问题，例如 “Count Good Subarrays”、 “Number of Triplets With Two Equal Elements”。  
- **解题钥匙**：**把中间位置固定，分别统计左、右两侧满足条件的元素数量**，乘积即为贡献。  

---

## 反思  

- **第一反应**：看到 “三元组” 立刻想到三层循环，导致暴力思路。  
- **最容易踩的坑**：  
  - 忘记在遍历时先把当前元素从右侧频次表中减去，导致 `k` 可能取到 `j` 本身。  
  - 处理 `target = 2 * nums[j]` 时出现整数溢出（在 Python 不会，但在其他语言要注意）。  
  - 结果需要对 `10⁹+7` 取模，忘记取模会导致整数超出范围。  
- **下次思路**：遇到「左‑中‑右」结构的计数题，第一步就尝试 **固定中间**，思考如何 **快速获得左侧和右侧的满足条件的元素数量**，通常哈希表或前缀/后缀计数能把时间从 `O(n³)` 降到 `O(n)`。