# #2401. 最长优雅子数组 / Longest Nice Subarray

> 难度：中等 · 标签：Array、Bit Manipulation、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-nice-subarray/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
We call a subarray of nums nice if the bitwise AND of every pair of elements that are in different positions in the subarray is equal to 0.
Return the length of the longest nice subarray.
A subarray is a contiguous part of an array.
Note that subarrays of length 1 are always considered nice.

**Examples**

**Example 1:**

```
Input: nums = [1,3,8,48,10]
Output: 3
Explanation: The longest nice subarray is [3,8,48]. This subarray satisfies the conditions:
- 3 AND 8 = 0.
- 3 AND 48 = 0.
- 8 AND 48 = 0.
It can be proven that no longer nice subarray can be obtained, so we return 3.
```

**Example 2:**

```
Input: nums = [3,1,5,11,13]
Output: 1
Explanation: The length of the longest nice subarray is 1. Any subarray of length 1 can be chosen.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个只包含正整数的数组 `nums`。  
我们称 `nums` 的一个子数组（subarray）为 **优雅的**，如果该子数组中任意两项位于不同位置的元素的位与（bitwise AND）均等于 `0`。  
返回最长优雅子数组的长度。

> 子数组是数组的连续片段。  
> 注意，长度为 `1` 的子数组始终被视为优雅的。

### 示例

#### 示例 1
```
Input: nums = [1,3,8,48,10]
Output: 3
```
**解释**：最长的优雅子数组是 `[3,8,48]`。该子数组满足以下条件：
- `3 AND 8 = 0`
- `3 AND 48 = 0`
- `8 AND 48 = 0`

可以证明不存在更长的优雅子数组，所以返回 `3`。

#### 示例 2
```
Input: nums = [3,1,5,11,13]
Output: 1
```
**解释**：最长的优雅子数组长度为 `1`。任意一个长度为 `1` 的子数组都符合要求。

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是枚举所有可能的子数组，逐个检查它们是否满足 “任意两数的按位与为 0”。  

- **枚举子数组**：双层循环，外层 `i` 表示子数组左端点，内层 `j` 表示右端点，子数组为 `nums[i..j]`。  
- **检查子数组是否 nice**：对子数组里的每一对不同位置的元素做 `a & b`，只要出现不为 0 的情况，就立刻判为不 nice。  
- **记录最长长度**：每次发现一个 nice 子数组，就更新答案 `max_len = max(max_len, j-i+1)`。

> **类比**：把数组想成一排坐在长凳上的小朋友，老师要挑出一段连续的同学，让这段同学之间的“手势”（二进制位）没有任何交叉（即按位与为 0）。暴力做法就是把每一种可能的坐姿全部尝试一次，然后逐对检查手势是否冲突。

这种做法显然是 **正确** 的，因为它遍历了所有合法的子数组并且严格按照题目定义检验。

#### 代码（Python）

```python
from typing import List

def longestNiceSubarray_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 1                     # 长度为 1 的子数组一定满足条件
    for i in range(n):          # 左端点
        for j in range(i + 1, n):   # 右端点（至少两元素才需要检查）
            ok = True
            # 检查子数组 nums[i..j] 中任意两数的 AND 是否为 0
            for p in range(i, j):
                for q in range(p + 1, j + 1):
                    if nums[p] & nums[q]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                ans = max(ans, j - i + 1)
    return ans
```

> 关键行解释  
> - `if nums[p] & nums[q]:` —— 如果这两个数有任何相同的「1」位，则它们的按位与不为 0，子数组不满足条件。  
> - `ans = max(ans, j - i + 1)` —— 记录当前找到的最长 nice 子数组长度。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层两层循环产生 `O(n²)` 个子数组。  
  - 对每个子数组最坏要检查 `O(k²)`（`k` 为子数组长度）对元素，整体上等价于 `O(n³)`。  
  - **大白话**：如果数组有 1000 个元素，暴力解大约要做 1000³ ≈ 10⁹ 次比较，明显不可接受。

- **空间复杂度**：`O(1)`  
  - 只使用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查相同的位冲突**。我们注意到：

1. **位的数量有限**  
   - `nums[i] ≤ 10⁹`，二进制最多只有 30 位（因为 2³⁰ > 10⁹）。  
   - 一个子数组若要满足 “任意两数的 AND 为 0”，意味着子数组中所有数的 **已出现的 1 位集合** 必须互不重叠。换句话说，子数组里所有数的 **位集合的并集** 中每一位至多出现一次。

2. **滑动窗口（双指针）**  
   - 我们可以用两个指针 `left`、`right` 维护一个**当前合法的子数组**（窗口）。  
   - 同时维护一个整数 `mask`，它的二进制位表示当前窗口里已经出现的 1 位集合。  
   - 当我们准备把 `nums[right]` 加入窗口时，只要 `mask & nums[right] == 0`（即没有共同的 1 位），就可以安全加入，更新 `mask |= nums[right]`，窗口右移。  
   - 否则，说明 `nums[right]` 与窗口中的某些数冲突。我们只能**收缩左端**，不断把 `nums[left]` 移出窗口并用 `mask ^= nums[left]` 清除对应的位，直到冲突消失为止。此时再把 `nums[right]` 加入。

3. **最长长度**  
   - 每次窗口合法后，用 `ans = max(ans, right - left + 1)` 更新答案。

> **类比**：把每个数的「1 位」想象成一把钥匙。窗口里的钥匙不能重复出现（同一把钥匙只能在同一时刻被一把锁使用）。我们把钥匙放进盒子（窗口），如果新钥匙与盒子里已有钥匙冲突，就把最左边的钥匙先取出来，直到冲突消失。

4. **为什么最长子数组不会超过 30**  
   - 因为每加入一个新数，至少会占用它的一个「1 位」，而总共只有 30 种不同的位。若窗口长度已经超过 30，必然会出现位重复，冲突必然出现。  
   - 这也可以帮助我们在实现时不必担心无限增长的 `mask`，但算法本身已经自然限制了窗口大小。

#### 代码（Python）

```python
from typing import List

def longestNiceSubarray(nums: List[int]) -> int:
    """
    使用滑动窗口 + 位掩码（mask）实现 O(n) 时间解法
    """
    left = 0               # 窗口左端点
    mask = 0               # 当前窗口中出现的 1 位的并集
    ans = 0                # 最长 nice 子数组的长度

    for right, val in enumerate(nums):
        # 若出现位冲突，收缩左端直到冲突消失
        while mask & val:                 # 与运算不为 0 表示有公共的 1 位
            mask ^= nums[left]            # 移除左端元素对应的位
            left += 1                     # 左端右移

        # 加入当前元素
        mask |= val
        # 更新答案
        ans = max(ans, right - left + 1)

    return ans
```

> 关键行解释  
> - `while mask & val:` —— 检查新数 `val` 与当前窗口已有的位集合是否有交叉。只要有交叉，就必须收缩左端。  
> - `mask ^= nums[left]` —— 把左端元素对应的位从 `mask` 中移除（异或相当于“撤销”刚才的 `|=` 操作）。  
> - `mask |= val` —— 把新数的位加入到窗口的位集合中。  
> - `ans = max(ans, right - left + 1)` —— 当前窗口合法，更新最长长度。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个元素至多被右指针访问一次，又可能被左指针弹出一次。左、右指针的总移动次数不超过 `2n`，所以整体线性。  
  - 与暴力 `O(n³)` 相比，效率提升了 **指数级**（几乎可以在 10⁵ 长度的数组上毫秒通过）。

- **空间复杂度**：`O(1)`  
  - 只使用了常数个整数变量（`mask`, `left`, `ans` 等），不随输入规模增长。

---

## 心得

- **核心技巧**：**滑动窗口 + 位掩码**，利用位运算快速判断“是否有公共的 1 位”。  
- **适用的题型**  
  1. 「子数组/子串不含重复字符」类（LeetCode 3. Longest Substring Without Repeating Characters）——本质是检查字符是否重复，这里换成「位是否重复」。  
  2. 「子数组的按位或/按位与」限制的题目，例如「最长子数组使按位或 ≤ K」等。  
  3. 「最长子数组满足某种集合不冲突」的题目（如区间调度、颜色冲突等），只要能用位集合或哈希集合快速判断冲突，都可以套用同样的滑动窗口思路。  

- **一句话总结**：**把“是否冲突”抽象成“位是否重复”，用 mask 记录窗口状态，左指针负责“把冲突的钥匙先搬走”，右指针负责“把新钥匙放进来”。**

---

## 反思

- **第一反应**：看到“任意两数的 AND 为 0”，第一时间想到**位的互斥**，于是想检查每一对是否有公共 1 位。  
- **最容易踩的坑**  
  1. **忘记把左端元素的位撤销**：仅仅移动左指针而不更新 `mask` 会导致后续判断出现假阳性冲突。  
  2. **位数误判**：`nums[i] ≤ 10⁹` 实际上最多 30 位（而不是 31），但即使算多一点也不会影响正确性，只是会让人误以为最长子数组可以更长。  
  3. **边界情况**：空数组（题目保证至少 1 个元素）或全部元素都相同（如全是 1），窗口会始终只能容纳一个元素，需确保 `ans` 初始为 0 或 1 都能得到正确答案。  

- **下次遇到同类题**：第一步先**思考冲突的本质**（是重复字符、重复位、还是其他属性），然后**用一个全局状态（哈希表 / 位掩码）记录窗口内已出现的属性**，再用**滑动窗口**在冲突出现时收缩左端。这样几乎可以把大多数 “最长子数组/子串满足某种唯一性” 的问题一次性搞定。