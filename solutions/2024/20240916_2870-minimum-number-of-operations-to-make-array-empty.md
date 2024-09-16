# #2870. **使数组为空的最少操作次数** / Minimum Number of Operations to Make Array Empty

> 难度：中等 · 标签：Array、Hash Table、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-empty/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of positive integers.
There are two types of operations that you can apply on the array any number of times:
Return the minimum number of operations required to make the array empty, or -1 if it is not possible.
Note: This question is the same as 2244: Minimum Rounds to Complete All Tasks.

**Examples**

**Example 1:**

```
Input: nums = [2,3,3,2,2,4,2,3,4]
Output: 4
Explanation: We can apply the following operations to make the array empty:
- Apply the first operation on the elements at indices 0 and 3. The resulting array is nums = [3,3,2,4,2,3,4].
- Apply the first operation on the elements at indices 2 and 4. The resulting array is nums = [3,3,4,3,4].
- Apply the second operation on the elements at indices 0, 1, and 3. The resulting array is nums = [4,4].
- Apply the first operation on the elements at indices 0 and 1. The resulting array is nums = [].
It can be shown that we cannot make the array empty in less than 4 operations.
```

**Example 2:**

```
Input: nums = [2,1,2,2,3,3]
Output: -1
Explanation: It is impossible to empty the array.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的数组 `nums`，其中所有元素都是正整数。  
你可以无限次地对数组执行以下两种操作之一：

1. 选取两个数值相同的元素并将它们从数组中删除；
2. 选取三个数值相同的元素并将它们从数组中删除。

返回使数组为空所需的最少操作次数；如果无法将数组清空，则返回 `-1`。

---

### 示例

**示例 1**

```text
Input: nums = [2,3,3,2,2,4,2,3,4]
Output: 4
Explanation: 可以按如下方式完成清空：
- 对下标 0 和 3 处的元素执行第一次操作，数组变为 [3,3,2,4,2,3,4]；
- 对下标 2 和 4 处的元素执行第一次操作，数组变为 [3,3,4,3,4]；
- 对下标 0、1、3 处的元素执行第二次操作，数组变为 [4,4]；
- 对下标 0、1 处的元素执行第一次操作，数组为空。
```

**示例 2**

```text
Input: nums = [2,1,2,2,3,3]
Output: -1
Explanation: 无法通过上述操作将数组清空。
```

---

### 约束

- `2 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

> 注意：本题与 2244 题 *Minimum Rounds to Complete All Tasks* 完全相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求把数组中的所有元素全部删掉，每次操作只能选择 **两个相同的数** 或 **三个相同的数** 并一次性把它们从数组中移除。  
最直接的想法是：  

1. 统计数组里每一种数字出现了多少次（比如 `2` 出现 5 次，`3` 出现 3 次 …）。  
2. 对每一种数字，**枚举** 所有可能的删除组合：  
   - 先删 2 个，再删 3 个，或者先删 3 个，再删 2 个……  
   - 只要把这一次数字的所有出现次数凑成若干个 “2” 或 “3”，就算一种合法的方案。  
3. 把所有数字的方案相加，取最小的那个。  

可以把第 2 步想象成把一堆相同的水果（比如 7 颗苹果）分装进 **装 2 颗的盒子** 或 **装 3 颗的盒子**，把装满的盒子数加起来就是操作次数。  

> **为什么暴力能得到正确答案？**  
> 因为只要我们遍历了 **所有** 可能的分装方式，就一定能找到最少的盒子数（即最少的操作次数）。  

不过，这种“全枚举”会非常慢。假设一种数字出现了 `n` 次，枚举所有可能的 2‑和‑3 的组合相当于在 `0..n` 之间遍历，最坏情况要尝试 `O(n)` 种分法；而整个数组长度可能高达 `10⁵`，如果每种数字都这样枚举，时间会爆炸。

#### 代码（Python）

```python
from collections import Counter
import math

def min_operations_bruteforce(nums):
    """
    暴力枚举每个数字的所有 2/3 分配方式，返回最小操作数或 -1。
    只适合极小规模测试，真实数据会超时。
    """
    cnt = Counter(nums)                     # 统计每个数字出现次数
    total_ops = 0

    for val, times in cnt.items():
        best = math.inf                      # 保存当前数字的最少操作数

        # 枚举使用 k 次 “3个一组” 的情况，剩下的用 “2个一组”
        # k 的取值范围是 0 ~ times//3
        for k in range(times // 3 + 1):
            left = times - 3 * k              # 剩下的要用 2 的组合
            if left % 2 == 0:                 # 必须能被 2 整除才能完成
                ops = k + left // 2
                best = min(best, ops)

        if best == math.inf:                  # 没有合法的划分，说明出现次数为 1
            return -1
        total_ops += best

    return total_ops
```

> **关键行解释**  
> - `cnt = Counter(nums)`：把数组看成一本“字典”，`key` 是数字，`value` 是它在数组里出现的次数。  
> - `for k in range(times // 3 + 1)`：枚举把多少组 “3 个” 用掉。  
> - `if left % 2 == 0`：剩下的必须能被 2 整除，否则无法全部删光。  

#### 复杂度  

- **时间复杂度**：`O( Σ (freq_i) )`，即所有数字出现次数之和的数量级。最坏情况下等价于 `O(n²)`（因为对每个出现次数 `freq_i` 进行 `freq_i/3` 次枚举），对 `10⁵` 的数据会超时。  
- **空间复杂度**：`O(m)`，`m` 为不同数字的种类数（哈希表 `Counter` 需要存放每种数字的计数），最多 `O(n)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于对每个数字的出现次数进行枚举。实际上，这个枚举过程有规律可循：  
- 我们只能使用 “2 个” 或 “3 个” 把全部出现次数凑齐。  
- 对任意正整数 `c`（出现次数），只要 `c` 不是 **1**，就一定可以用若干个 2 和 3 表示出来。  

下面用 **数学推导** 来直接得到最少操作数，而不需要枚举。

1. **先尽可能多用 3**  
   因为一次操作能删掉更多元素，使用 3 能让操作次数更少。  
   所以把 `c // 3` 作为初始的 3‑组数。  

2. **看余数** `r = c % 3`  
   - `r == 0`：恰好全部用 3 填满，操作次数就是 `c // 3`。  
   - `r == 2`：剩下 2 个，用一组 2 完成，次数是 `c // 3 + 1`。  
   - `r == 1`：此时直接把 1 加进去会不合法，因为没有 “1 个” 的操作。  
     解决办法是**把一组已经的 3 拆成两个 2**：  
     - 把 `c // 3` 减 1（拿走一组 3），剩下的元素变成 `c - 3`。  
     - 这时 `c - 3` 的余数是 `1 + 3 = 4`，恰好可以用 **两个 2** 把它填满。  
     - 所以操作次数 = `(c // 3 - 1) + 2 = (c - 4) // 3 + 2`。  

3. **特殊情况**：如果某个数字只出现一次（`c == 1`），上述公式都不可用，说明根本不可能把它删掉，直接返回 `-1`。  

> **类比**：把出现次数想成一根棍子，你可以一次切掉 **2** 长或 **3** 长的段。目标是用最少的刀切完全部棍子。显然，先用长刀（3）切能减少刀数；只有最后剩下的长度不合适时才换成短刀（2），而 “余 1” 的情况只能把前面的一段长刀拆成两段短刀。

#### 代码（Python）

```python
from collections import Counter

def minimum_operations(nums):
    """
    返回把数组全部删掉所需的最少操作次数，若不可能返回 -1。
    思路：统计每个数字出现次数，根据出现次数除以 3 的余数直接算出最少操作数。
    时间 O(n) ，空间 O(m)（m 为不同数字个数）。
    """
    cnt = Counter(nums)          # 哈希表：数字 -> 出现次数
    ops = 0

    for val, c in cnt.items():
        if c == 1:                # 单独出现一次，无法组成 2 或 3
            return -1

        # 根据余数决定如何安排 2 与 3
        if c % 3 == 0:
            ops += c // 3                     # 全部用 3
        elif c % 3 == 1:
            # 把一组 3 拆成两个 2，等价于 (c-4)//3 + 2
            ops += (c - 4) // 3 + 2
        else:  # c % 3 == 2
            ops += c // 3 + 1                 # 用尽可能多的 3，剩下的 2 直接加一组

    return ops
```

> **关键行解释**  
> - `cnt = Counter(nums)`：把数组看成一本“词典”，每个数字对应它出现的页码数。  
> - `if c == 1: return -1`：出现一次的数字没有配对对象，直接判负。  
> - `c % 3 == 1` 分支里 `(c - 4) // 3 + 2`：把一组 3（长度 3）换成两个 2（长度 4），确保全部被覆盖。  

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历一次数组进行计数，再遍历哈希表（最多 `n` 项）计算公式。对 `10⁵` 的数据毫无压力。  
- **空间复杂度**：`O(m)`，`m` 为不同数字的种类数。最坏情况下每个元素都不相同，`m = n`，仍然是线性空间。  

与暴力解相比，时间从 **指数级/平方级** 降到了 **线性级**，大幅提升。

---

## 心得  

- **核心技巧**：**把“只能删 2 或 3 个相同元素”的约束转化为“用 2 与 3 组合表示出现次数”，再用数学余数直接求最少组合数**。  
- **适用的题型**：  
  1. LeetCode 2244 *Minimum Rounds to Complete All Tasks*（本题的原始版本）。  
  2. “把所有石子分成若干堆，每堆只能是 2 或 3” 类似的装箱/分割问题。  
  3. “最少硬币找零” 中硬币面额只有 2 与 3 的特例。  
- **一句话总结解题钥匙**：**先尽量用最大的“3”，余数为 1 时把一组 3 拆成两个 2**。

---

## 反思  

- **第一反应**：看到只能删除 2 或 3 个相同元素，立刻想到 “统计频率” 再 “枚举所有可能的 2/3 组合”。  
- **最容易踩的坑**：  
  - 忽视出现次数为 **1** 的情况，导致错误地返回一个正数。  
  - 余数为 **1** 时不做特殊处理，直接算 `c//3 + 1` 会得到错误的操作数（例如 `c = 4` 会得到 `2`，实际应为 `2` 但来源不同，需要把 4 看成 `2+2`）。  
  - 对大数据忘记使用哈希表统计，导致超时。  
- **下次遇到同类题**：第一步先 **统计每种元素出现次数**，再检查 **是否有出现一次的元素**，随后依据 **余数** 用 “先用最大单位、余数调节” 的思路快速算出最优答案。