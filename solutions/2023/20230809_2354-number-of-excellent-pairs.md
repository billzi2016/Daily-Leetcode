# #2354. **优秀数对的数量** / Number of Excellent Pairs

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-excellent-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed positive integer array nums and a positive integer k.
A pair of numbers (num1, num2) is called excellent if the following conditions are satisfied:
Return the number of distinct excellent pairs.
Two pairs (a, b) and (c, d) are considered distinct if either a != c or b != d. For example, (1, 2) and (2, 1) are distinct.
Note that a pair (num1, num2) such that num1 == num2 can also be excellent if you have at least one occurrence of num1 in the array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,1], k = 3
Output: 5
Explanation: The excellent pairs are the following:
- (3, 3). (3 AND 3) and (3 OR 3) are both equal to (11) in binary. The total number of set bits is 2 + 2 = 4, which is greater than or equal to k = 3.
- (2, 3) and (3, 2). (2 AND 3) is equal to (10) in binary, and (2 OR 3) is equal to (11) in binary. The total number of set bits is 1 + 2 = 3.
- (1, 3) and (3, 1). (1 AND 3) is equal to (01) in binary, and (1 OR 3) is equal to (11) in binary. The total number of set bits is 1 + 2 = 3.
So the number of excellent pairs is 5.
```

**Example 2:**

```
Input: nums = [5,1,1], k = 10
Output: 0
Explanation: There are no excellent pairs for this array.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 60

---

## 题目（中文翻译）

给定一个下标从 0 开始的正整数数组 `nums` 和一个正整数 `k`。  
如果一对数字 `(num1, num2)` 满足以下条件，则称其为 **优秀数对**（excellent pair）：

- `popcount(num1 & num2) + popcount(num1 | num2) >= k`  
  其中 `&` 表示按位与（AND），`|` 表示按位或（OR），`popcount(x)` 表示整数 `x` 的二进制表示中 1 的个数。

返回不同的优秀数对的数量。

两个数对 `(a, b)` 与 `(c, d)` 被认为是不同的，只要 `a != c` 或 `b != d`。例如，`(1, 2)` 与 `(2, 1)` 被视为不同的数对。  
需要注意的是，如果数组中至少出现一次 `num1`，则数对 `(num1, num1)` 也可能是优秀数对。

---

### 示例

**示例 1**

```text
Input: nums = [1,2,3,1], k = 3
Output: 5
Explanation: 满足条件的优秀数对如下：
- (3, 3)：`3 & 3 = 3`，`3 | 3 = 3`，二进制均为 `11`，`popcount` 为 2，2 + 2 = 4 ≥ k。
- (2, 3) 与 (3, 2)：`2 & 3 = 2`（二进制 `10`，popcount = 1），`2 | 3 = 3`（二进制 `11`，popcount = 2），1 + 2 = 3。
- (1, 3) 与 (3, 1)：同理满足条件。
```

**示例 2**

```text
Input: nums = [5,1,1], k = 10
Output: 0
Explanation: 该数组中不存在优秀数对。
```

---

### 约束

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 60`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把数组里 **所有** 可能的数对都枚举一遍，逐个检查它们是否满足 “优秀” 条件。  
具体步骤如下：

1. 先把 `nums` 中出现的数去重（因为题目只要求 **数值** 组合，而不是下标），这一步可以用 **哈希表** 完成。  
   - 哈希表就像一本词典，单词是 `key`，对应的解释是 `value`。这里我们只关心 `key`（出现过的数字），不需要 `value`。  
2. 对去重后的每一对 `(a, b)`（包括 `a == b`），计算  
   - `popcount(a)`：二进制里 `1` 的个数。  
   - `popcount(b)` 同理。  
   - 根据题目给出的等价关系，`popcount(a) + popcount(b) >= k` 即为 “优秀”。  
3. 只要满足条件，就把这对计入答案。  

这种做法 **一定能得到正确答案**，因为我们把所有合法的数对都检查了一遍，没漏也没错。  

> **为什么会对**  
> - “去重”保证每个不同的数只出现一次，避免把同一个数值的不同下标算成不同的数对（题目不这么要求）。  
> - 暴力枚举把所有可能的 `(a, b)` 都遍历到，自然不会错过任何优秀对。  

**时间/空间分析（大白话）**  

- 假设去重后有 `m` 个不同的数。  
- 暴力枚举需要两层循环，**每层遍历 `m` 次**，总共要检查 `m × m = m²` 对。  
- `m` 最坏可以和原数组长度 `n` 相等（如果所有数都不相同），所以时间复杂度是 **O(n²)**。  
  - 用大白话说，就是如果 `n = 10⁵`，程序得跑 **一万亿** 次，这在电脑里根本跑不完。  
- 需要额外的哈希表来存放去重后的数，最多保存 `n` 个整数，空间是 **O(n)**。  

#### 代码（Python）  

```python
from typing import List

def excellentPairs_bruteforce(nums: List[int], k: int) -> int:
    # 1️⃣ 去重：用集合（哈希表）把相同的数字合并，只保留唯一值
    uniq = list(set(nums))               # 相当于把“词典”里只留下不同的单词
    m = len(uniq)

    # 2️⃣ 统计每个数的二进制 1 的个数（popcount）
    pop = [bin(x).count('1') for x in uniq]   # bin(x) 把整数变成二进制字符串，count('1') 计数

    ans = 0
    # 3️⃣ 暴力枚举所有有序数对 (a, b)
    for i in range(m):
        for j in range(m):
            # 条件：pop[i] + pop[j] >= k
            if pop[i] + pop[j] >= k:
                ans += 1                  # (uniq[i], uniq[j]) 是优秀的
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m²)` → 最坏情况 `O(n²)`，即平方级别的时间，实际会超时。  
- **空间复杂度**：`O(m)` → 最坏 `O(n)`，用于存放去重后的数组和对应的 popcount。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于两层循环导致的 `m²` 检查。  
要提升效率，需要 **快速找出满足 `pop[a] + pop[b] >= k` 的配对数目**，而不是逐个比较。

下面一步步推导优化思路：

1. **利用提示化简条件**  
   - 题目提示：`popcount(a OR b) + popcount(a AND b) = popcount(a) + popcount(b)`。  
   - 因此“优秀”条件等价于 `popcount(a) + popcount(b) >= k`。  
   - 这把原本看起来和位运算相关的条件，简化成了 **只看两个数的 1 的个数**。

2. **只关心 1 的个数**  
   - 对每个不同的数字，只需要它的 `popcount`，不需要原始的数值。  
   - 把所有不同数字的 `popcount` 收集到一个数组 `bits[]` 中。

3. **排序 + 二分 / 双指针**  
   - 将 `bits` 按升序排好。  
   - 对于固定的 `bits[i]`，我们想知道有多少 `bits[j]` 满足 `bits[i] + bits[j] >= k`。  
   - 因为数组有序，`bits[j]` 只要 **大于等于** `k - bits[i]` 就行。  
   - 用 **二分查找**（`bisect_left`）找出第一个满足 `bits[j] >= k - bits[i]` 的位置 `pos`，随后所有位置在 `pos … m-1` 都合法。  
   - 对每个 `i`，合法配对数 = `m - pos`（包括 `i` 本身），把它们累加即可得到答案。  

4. **为什么是有序 + 二分**  
   - 想象一排排好序的书，想找所有厚度≥`X` 的书。只要在排好序的书架上**快速定位**第一本满足厚度的书（用二分），后面的书自然全部满足。  
   - 这里的“厚度”对应 `bits[j]`，`X = k - bits[i]`。  

5. **有序 + 双指针的另一种写法**  
   - 也可以使用左指针 `l`（指向最小的 `bits`）和右指针 `r`（指向最大），从两端向中间收敛，统计满足条件的配对数。  
   - 但二分实现更直观，代码更短。  

**核心技巧**：  
- **位计数的等价转化** → 把复杂的位运算条件化简为两个整数的和。  
- **排序 + 二分** → 在有序序列上快速统计满足 “≥ 某值” 的元素个数。  

#### 代码（Python）  

```python
from typing import List
import bisect

def excellentPairs(nums: List[int], k: int) -> int:
    """
    返回不同数值之间（有序）满足 popcount(a) + popcount(b) >= k 的配对数目。
    """
    # 1️⃣ 去重：只保留不同的数字（哈希表/集合）
    uniq = set(nums)                     # 类似词典的 key 集合
    # 2️⃣ 统计每个数的 1 的个数
    bits = [bin(x).count('1') for x in uniq]   # 只需要 popcount
    # 3️⃣ 排序，方便二分
    bits.sort()                          # 从小到大排好序

    m = len(bits)
    ans = 0

    # 4️⃣ 对每个 popcount[i]，二分找出第一个 >= (k - bits[i]) 的位置
    for i in range(m):
        need = k - bits[i]                # 另一个数至少需要多少个 1
        # 如果 need <= 0，说明当前 bits[i] 已经足够大，所有剩余的数都可以配对
        if need <= 0:
            ans += m                      # 与所有 m 个数配对（包括自己）
            continue

        # bisect_left 在有序列表中找第一个 >= need 的下标
        pos = bisect.bisect_left(bits, need)
        # pos 右侧（包括 pos）都是合法的配对对象
        ans += m - pos

    return ans
```

> **代码要点注释**  
> - `set(nums)`：像把所有单词放进一本词典，只保留唯一的词条。  
> - `bin(x).count('1')`：把整数转成二进制字符串，再数其中的 `'1'`。  
> - `bits.sort()`：把书按照厚度（1 的个数）从薄到厚排好，后面二分才能快。  
> - `bisect_left(bits, need)`：在排好序的书架上，快速定位第一本厚度≥`need` 的书。  

#### 复杂度  

- **时间复杂度**：`O(m log m)`  
  - 去重 `O(n)`，统计 popcount `O(m)`，排序 `O(m log m)`，遍历 `m` 次并二分 `O(log m)` → 总体 `O(m log m)`。  
  - 相比暴力的 `O(m²)`，把平方级别降到了 **对数级别**，即使 `m = 10⁵` 也能在毫秒级完成。  

- **空间复杂度**：`O(m)`  
  - 需要存放去重后的数和对应的 `bits`，最多 `m` 个整数。  

---

## 心得  

- **核心技巧**：把 “`popcount(a OR b) + popcount(a AND b)`” 通过位运算的等价关系化简为 **`popcount(a) + popcount(b)`**，然后利用 **排序 + 二分**（或双指针）快速统计满足阈值的配对数。  
- **适用的题型**  
  1. 需要统计满足 “两个数的某种单调函数之和 ≥ k” 的配对，例如 “两个数的位数之和” 或 “两个数的绝对差 ≤ k”。  
  2. “数对满足条件” 且 **只与单个数的属性**（如位数、长度、出现次数）有关的题目。  
  3. 类似 “Number of Pairs With Sum At Least K” 这类求和阈值的配对计数。  
- **一句话总结解题钥匙**：**先把位运算条件化简成单值求和，再用排序+二分把配对计数从 O(n²) 降到 O(n log n)。**  

---

## 反思  

- **第一反应**：看到 “AND / OR 的二进制位数” 直接想到遍历每一对做位运算，导致想到暴力枚举。  
- **最容易踩的坑**  
  1. **忘记去重**：如果直接在原数组上枚举，会把同一个数值的不同下标算成不同的配对，答案会被高估。  
  2. **误解条件**：没有利用提示把 `OR` 与 `AND` 的位数和转化为单纯的 `popcount` 之和，会错失关键的简化步骤。  
  3. **二分边界**：当 `need <= 0` 时，二分会返回 `0`，但实际上所有数都合法，需要单独处理。  
- **下次遇到同类题的第一步**：**先思考是否可以把题目给出的复杂表达式转化为只涉及单个元素的属性**（如长度、位数、出现次数），再决定使用排序 + 二分/双指针来做配对计数。