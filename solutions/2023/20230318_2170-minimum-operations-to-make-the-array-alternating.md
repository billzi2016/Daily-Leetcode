# #2170. 最少操作使数组交替 / Minimum Operations to Make the Array Alternating

> 难度：中等 · 标签：Array、Hash Table、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-the-array-alternating/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of n positive integers.
The array nums is called alternating if:
In one operation, you can choose an index i and change nums[i] into any positive integer.
Return the minimum number of operations required to make the array alternating.

**Examples**

**Example 1:**

```
Input: nums = [3,1,3,2,4,3]
Output: 3
Explanation:
One way to make the array alternating is by converting it to [3,1,3,1,3,1].
The number of operations required in this case is 3.
It can be proven that it is not possible to make the array alternating in less than 3 operations.
```

**Example 2:**

```
Input: nums = [1,2,2,2,2]
Output: 2
Explanation:
One way to make the array alternating is by converting it to [1,2,1,2,1].
The number of operations required in this case is 2.
Note that the array cannot be converted to [2,2,2,2,2] because in this case nums[0] == nums[1] which violates the conditions of an alternating array.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的数组 `nums`，其中包含 `n` 个正整数（positive integer）。  
如果满足以下条件，则称数组 `nums` 为 **交替**（alternating）：

* 在所有偶数下标 `i`（即 `i % 2 == 0`）处的元素两两不同；
* 在所有奇数下标 `i`（即 `i % 2 == 1`）处的元素两两不同；
* 任意偶数下标 `i` 与任意奇数下标 `j` 处的元素也不同。

一次 **操作**（operation）中，你可以选择一个 **索引** `i`，并将 `nums[i]` 改为任意正整数。  
返回使数组变为交替所需的最少操作次数。

**示例 1**  
```
Input: nums = [3,1,3,2,4,3]
Output: 3
Explanation:
一种使数组交替的方法是将其转换为 [3,1,3,1,3,1]。
此时需要的操作次数为 3。
可以证明，少于 3 次操作无法使数组交替。
```

**示例 2**  
```
Input: nums = [1,2,2,2,2]
Output: 2
Explanation:
一种使数组交替的方法是将其转换为 [1,2,1,2,1]。
此时需要的操作次数为 2。
需要注意的是，数组不能转换为 [2,2,2,2,2]，因为此时 nums[0] == nums[1]，违反了交替数组的条件。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的交替数组**，然后计算把原数组改成它需要多少次操作，取最小值。  
- 交替数组的定义是：相邻两个数不相等，并且下标奇偶位置上的数可以相同，只要相邻不相同即可。  
- 为了遍历所有可能的交替数组，我们可以先决定奇数下标（0、2、4…）上的数，再决定偶数下标（1、3、5…）上的数。  
- 每一种决定都是从「所有正整数」中任选一个。因为正整数的范围是 `1 … 10^5`（题目限制），理论上要遍历 `10^5 × 10^5` 种组合，显然不可行。  

**为什么暴力是对的？**  
只要我们把所有可能的交替数组都列举出来，必然会包含最优的那个。只要把每个候选数组和原数组逐位比较，统计不同位置的个数（即需要改动的次数），最小的就是答案。

**时间/空间复杂度**  
- 时间复杂度：`O(V^2 * n)`，其中 `V = 10^5` 是数值的取值范围，`n` 是数组长度。想象一下，遍历十万乘十万的组合，每个组合还要遍历整个数组，这几乎是 **天文数字**，在实际运行中根本跑不完。  
- 空间复杂度：`O(1)`（只用了常数级的临时变量），但这点不重要，因为时间已经炸裂。

> **大白话**：`O(V^2 * n)` 就像让一千个人每人去遍历一万本书再统计一次，显然不可能在一天内完成。

#### 代码（Python）

```python
def min_operations_bruteforce(nums):
    # 这里的实现只是为了说明思路，实际运行会超时
    MAX_VAL = 10 ** 5
    n = len(nums)
    best = n  # 最多需要改动 n 次

    for odd_val in range(1, MAX_VAL + 1):          # 奇数下标填的数
        for even_val in range(1, MAX_VAL + 1):     # 偶数下标填的数
            if odd_val == even_val:                # 相邻位置不能相同
                continue
            ops = 0
            for i, x in enumerate(nums):
                # i 为奇数下标时应该是 odd_val，偶数下标时应该是 even_val
                target = odd_val if i % 2 == 0 else even_val
                if x != target:
                    ops += 1
            best = min(best, ops)                  # 取最小
    return best
```

#### 复杂度

- **时间复杂度**：`O(10^5 × 10^5 × n)` → 实际不可接受。  
- **空间复杂度**：`O(1)` → 只用了几个计数器。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正决定改动次数的关键是奇数位和偶数位各自保留多少原来的数字**。  
如果我们把奇数下标的所有元素视为一组，偶数下标的所有元素视为另一组：

| 位置 | 0 | 1 | 2 | 3 | 4 | 5 | … |
|------|---|---|---|---|---|---|---|
| 组别 | 奇 | 偶 | 奇 | 偶 | 奇 | 偶 | … |

要让数组交替，只需要满足 **奇组选的数 ≠ 偶组选的数**。  
因此，我们只要找出：

1. **奇组出现频率最高的数**（记作 `odd_max1`），以及它出现的次数 `cnt_odd_max1`。  
2. **奇组出现频率第二高的数**（`odd_max2`），出现次数 `cnt_odd_max2`（如果不存在则记 0）。  
3. 同理，**偶组出现频率最高的数**（`even_max1`），出现次数 `cnt_even_max1`，以及第二高的 `even_max2`、`cnt_even_max2`。

> **类比**：把奇组想成一本“奇数字典”，把偶组想成一本“偶数字典”。字典里每个词（数字）对应的页码就是出现次数。我们想挑出两本字典里最常出现的词，然而这两个词**不能相同**（否则相邻会相等）。

**为什么只需要前两名？**  
- 如果 `odd_max1` 与 `even_max1` 不相同，那么直接让奇位全部保持 `odd_max1`，偶位全部保持 `even_max1`，两者不冲突，改动次数最少。  
- 如果它们相同（比如都是数字 3），我们就必须让其中一组换成次高的数字。换成哪一个更好？显然是把改动最少的那组换成它的第二高数字。于是只需要比较两种方案：

  - 方案 A：奇组使用 `odd_max1`，偶组使用 `even_max2` → 改动次数 = `(奇位总数 - cnt_odd_max1) + (偶位总数 - cnt_even_max2)`  
  - 方案 B：奇组使用 `odd_max2`，偶组使用 `even_max1` → 改动次数 = `(奇位总数 - cnt_odd_max2) + (偶位总数 - cnt_even_max1)`

取两者的最小值即为答案。

**核心算法**：一次遍历统计奇、偶位的频率（使用哈希表），再一次遍历哈希表找出前两名（可以直接用 `most_common(2)`，但手写更易懂）。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def min_operations(nums: List[int]) -> int:
    """
    返回使数组交替所需的最少改动次数。
    思路：统计奇、偶位各自的出现次数，挑出出现次数最多的两种数字，
          根据是否冲突决定是否使用次高数字。
    """
    n = len(nums)

    # 1. 分别收集奇位（下标偶数）和偶位（下标奇数）的出现频率
    odd_counter = Counter()   # 下标 0,2,4,...   → 这里称为 “奇位”
    even_counter = Counter()  # 下标 1,3,5,...   → 这里称为 “偶位”

    for i, val in enumerate(nums):
        if i % 2 == 0:          # 奇位
            odd_counter[val] += 1
        else:                   # 偶位
            even_counter[val] += 1

    # 2. 找出每个 Counter 中出现次数最多的两个元素
    #   most_common(k) 会返回 (元素, 次数) 的列表，按次数降序排列
    odd_top = odd_counter.most_common(2)
    even_top = even_counter.most_common(2)

    # 为了统一处理不存在第二名的情况，补齐 (None, 0)
    if len(odd_top) < 2:
        odd_top.append((None, 0))
    if len(even_top) < 2:
        even_top.append((None, 0))

    # 解包，分别得到数字和值
    odd_val1, cnt_odd1 = odd_top[0]
    odd_val2, cnt_odd2 = odd_top[1]
    even_val1, cnt_even1 = even_top[0]
    even_val2, cnt_even2 = even_top[1]

    # 3. 根据是否冲突决定最少改动次数
    if odd_val1 != even_val1:
        # 最多出现的奇位数字和偶位数字不相同，直接使用它们
        ops = (n // 2 + n % 2 - cnt_odd1) + (n // 2 - cnt_even1)
    else:
        # 出现冲突，需要让一方使用次高数字
        # 方案 A：奇位保持第一，偶位使用第二
        ops_a = (n // 2 + n % 2 - cnt_odd1) + (n // 2 - cnt_even2)
        # 方案 B：偶位保持第一，奇位使用第二
        ops_b = (n // 2 + n % 2 - cnt_odd2) + (n // 2 - cnt_even1)
        ops = min(ops_a, ops_b)

    return ops
```

**代码要点注释**  

- `Counter` 相当于“字典”，把每个数字映射到它出现的次数，像查字典一样 `counter[num]` 就能得到次数。  
- `n // 2 + n % 2` 计算奇位（下标偶数）总数，`n // 2` 计算偶位（下标奇数）总数。  
- 当最高频数字相同，需要考虑两种“让另一组退位”的方案，取最小的那一个。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组收集频率 `O(n)`，  
  - 再遍历两个哈希表（最多 `O(k)`，其中 `k ≤ n`）找前两名，整体仍是线性。  
  - 与暴力解的 `O(V²·n)` 相比，**大幅下降**，在 `n ≤ 10⁵` 时毫秒级完成。

- **空间复杂度**：`O(k)`  
  - `k` 为不同数字的种类数，最坏情况下 `k ≤ n`（每个数都不相同），  
  - 只需要存两个计数字典，空间是线性的，且常数因子很小。

---

## 心得

- **核心技巧**：把奇、偶下标分别视作两个独立的“集合”，统计各自出现频率，然后通过“最大频率 + 次高频率”消除冲突。  
- **适用的题型**  
  1. **数组交替/分组最少改动**（如 “Minimum Deletions to Make Array Alternating”）。  
  2. **分组颜色填充**（如 “Paint House” 类似的每组颜色不能相同的最小成本问题）。  
  3. **两个子序列分别统一**（如 “Make Two Arrays Equal With Minimum Operations”）。  
- **一句话总结**：**先把奇、偶位各自“保留最多”，再处理冲突——只要比较最高/次高两种组合即可得到最少改动次数**。

---

## 反思

- **第一反应**：看到“交替数组”，立刻想到**相邻不相等**，于是想到遍历所有可能的数字组合（暴力）。  
- **最容易踩的坑**  
  - **下标的奇偶概念混淆**：记得题目是 0‑索引，奇位指下标偶数，偶位指下标奇数。  
  - **边界情况**：当数组长度为 1 时，偶位数量为 0，代码仍需正常返回 0。  
  - **次高频率不存在**：如果某一组只有一种数字，次高频率的计数应视为 0，否则会出现 `None` 与数字比较的错误。  
- **下次思路**：遇到“让数组满足某种交替/分组约束”时，**先统计每个组的出现频率**，再**只比较最高/次高**，往往能把复杂度降到线性。