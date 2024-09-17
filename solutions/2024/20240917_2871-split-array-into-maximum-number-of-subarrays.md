# #2871. 划分数组为最多子数组数 / Split Array Into Maximum Number of Subarrays

> 难度：中等 · 标签：Array、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/split-array-into-maximum-number-of-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of non-negative integers.
We define the score of subarray nums[l..r] such that l <= r as nums[l] AND nums[l + 1] AND ... AND nums[r] where AND is the bitwise AND operation.
Consider splitting the array into one or more subarrays such that the following conditions are satisfied:
Return the maximum number of subarrays in a split that satisfies the conditions above.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [1,0,2,0,1,2]
Output: 3
Explanation: We can split the array into the following subarrays:
- [1,0]. The score of this subarray is 1 AND 0 = 0.
- [2,0]. The score of this subarray is 2 AND 0 = 0.
- [1,2]. The score of this subarray is 1 AND 2 = 0.
The sum of scores is 0 + 0 + 0 = 0, which is the minimum possible score that we can obtain.
It can be shown that we cannot split the array into more than 3 subarrays with a total score of 0. So we return 3.
```

**Example 2:**

```
Input: nums = [5,7,1,3]
Output: 1
Explanation: We can split the array into one subarray: [5,7,1,3] with a score of 1, which is the minimum possible score that we can obtain.
It can be shown that we cannot split the array into more than 1 subarray with a total score of 1. So we return 1.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 106

---

## 题目（中文翻译）

你得到一个由非负整数构成的数组 `nums`。  
我们将子数组（subarray）`nums[l..r]`（其中 `l ≤ r`）的 **分数** 定义为 `nums[l] AND nums[l + 1] AND ... AND nums[r]`，其中 `AND` 为按位与（bitwise AND）运算。

考虑将整个数组划分为一个或多个子数组，使得满足以下条件：

* 所有子数组的 **分数之和** 为所有可能划分方式中能够得到的 **最小可能总分**；
* 在满足上述总分最小的前提下，划分得到的子数组数量尽可能多。

返回满足条件的划分方案中 **子数组的最大数量**。

> 子数组是数组中连续的一段。

### 示例

#### 示例 1
```
Input: nums = [1,0,2,0,1,2]
Output: 3
Explanation: 我们可以将数组划分为以下子数组：
- [1,0]，其分数为 1 AND 0 = 0。
- [2,0]，其分数为 2 AND 0 = 0。
- [1,2]，其分数为 1 AND 2 = 0。
三个子数组的分数之和为 0 + 0 + 0 = 0，这是能够得到的最小总分。
可以证明，无法在保持总分为 0 的情况下得到更多的子数组，因此答案为 3。
```

#### 示例 2
```
Input: nums = [5,7,1,3]
Output: 1
Explanation: 我们只能将数组划分为一个子数组 [5,7,1,3]，其分数为 5 AND 7 AND 1 AND 3 = 1，这是能够得到的最小总分。
可以证明，无法在保持总分为 1 的情况下将数组划分为超过 1 个子数组。因此返回 1。
```

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的切分方式**，计算每段子数组的 AND 值，然后把这些 AND 值相加，找出总和最小且子数组个数最多的方案。  

- **数据结构**：我们只需要普通的数组 `nums`，以及在枚举时用到的临时变量 `cur_and`（记录当前子数组的按位与）。可以把 `cur_and` 想象成 **“累积的口袋”**：每往里放一个数字，就把口袋里已有的数字全部做一次 AND，得到新的口袋内容。  
- **正确性**：因为我们遍历了**所有**合法的切分（从左到右每次都可以选择在当前位置结束子数组），必然会覆盖最优答案。  

> 这里的暴力实际上是 **指数级**（每个位置都有“切”或“不切”两种选择），在最坏情况下会有 `2^(n-1)` 种切法，显然不可行。但先写出这种思路，有助于我们发现瓶颈所在。

#### 代码（Python）

```python
from typing import List

def max_subarrays_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best_cnt = 0                     # 记录满足最小总分的最大子数组个数

    # dfs(idx, cur_and, cur_sum, cnt)  - 从 idx 开始往后走
    def dfs(idx: int, cur_and: int, cur_sum: int, cnt: int):
        nonlocal best_cnt
        if idx == n:                  # 到达数组末尾，算一次完整的切分
            # 这里的最小总分其实就是所有元素的整体 AND
            # 因为题目已知最小总分一定是 overall_and，故只要 cur_sum == overall_and 即可
            if cur_sum == overall_and:
                best_cnt = max(best_cnt, cnt)
            return

        # 把 nums[idx] 加入当前子数组
        new_and = cur_and & nums[idx] if cur_and is not None else nums[idx]
        # 继续往后，不在这里切
        dfs(idx + 1, new_and, cur_sum, cnt)

        # 在 idx 位置结束当前子数组（前提是已经有子数组在进行中）
        if cur_and is not None:
            dfs(idx + 1, None, cur_sum + cur_and, cnt + 1)

    overall_and = nums[0]
    for x in nums[1:]:
        overall_and &= x               # 整体 AND，题目已说明它是最小可能的总分

    dfs(0, None, 0, 0)
    return best_cnt
```

> 关键行解释  
> - `overall_and`：相当于 **“全局字典”**，记录所有数字的 AND，答案的最小总分一定是它。  
> - `dfs`：深度优先搜索，尝试在每个位置“切”或“不切”。  
> - `cur_and is None`：用 `None` 表示当前没有正在构建的子数组，相当于 “口袋是空的”。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级），因为每个位置都有两种选择，实际运行只能处理 `n` 很小的情况。  
- **空间复杂度**：`O(n)`，递归栈的深度最多 `n`。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于“枚举所有切法”。我们需要 **一次遍历** 就能决定在哪里切。观察题目提示：

1. **最小总分** 必然等于所有元素的整体 AND（记作 `overall_and`）。  
2. 如果 `overall_and != 0`，则不可能把总分降到更小，只能把整个数组当作一个子数组，答案只能是 `1`。  
3. 当 `overall_and == 0` 时，**每个子数组的分数都必须为 0**（否则总分就会大于 0），这时我们希望把子数组 **尽可能多**。  

**如何让子数组的 AND 为 0？**  
- 按位与的性质是：只要子数组中出现 **任意一个 0 位**（即对应位上有 0），整个 AND 就会在该位上变成 0。  
- 更直观的说：只要子数组里出现 **一个元素本身为 0**，或者 **某几个元素的 AND 结果已经是 0**，再往后加入元素也不会把 0 “变回” 正数，AND 仍然是 0。  

因此，我们可以 **从左到右累积 AND**，一旦累计结果变成 0，就立刻把这个子数组切掉（因为再往后加只会让它仍然是 0，切得更早可以让后面的元素有机会再形成新的 0），然后重新开始累计。  

**贪心策略**：  
- 维护一个变量 `cur_and`，初始为全 1（即 `~0`，在 Python 用 `-1` 表示所有位都是 1）。  
- 遍历数组，对每个 `num` 做 `cur_and &= num`。  
- 若 `cur_and == 0`，说明当前子数组已经满足分数为 0，计数 `ans += 1`，并把 `cur_and` 重置为全 1，准备开始下一个子数组。  

这就是 **一次遍历的贪心**，时间线性，空间常数。

> **类比**：把 `cur_and` 想成“装满水的杯子”。每次往杯子里倒水（`&=`），只要杯子里出现了“干” (0) 的位置，整杯水就变得“干”。一旦杯子完全干了（`cur_and == 0`），我们立刻把这杯水倒掉，重新装满，继续装下一杯。

#### 代码（Python）

```python
from typing import List

def max_subarrays(nums: List[int]) -> int:
    """
    返回满足题目条件的最大子数组个数
    """
    # 1️⃣ 先算出整体 AND（最小可能的总分）
    overall_and = nums[0]
    for x in nums[1:]:
        overall_and &= x

    # 2️⃣ 如果整体 AND 不为 0，只能整段放在一起
    if overall_and != 0:
        return 1

    # 3️⃣ 否则整体 AND 为 0，贪心切分
    ans = 0
    cur_and = -1          # -1 的二进制全部为 1（相当于“全满的杯子”）
    for num in nums:
        cur_and &= num   # 往当前子数组里“倒水”
        if cur_and == 0: # 已经变成 0，子数组得分为 0
            ans += 1      # 计数一个子数组
            cur_and = -1  # 重置，准备下一段

    return ans
```

> 关键行解释  
> - `overall_and`：全局 AND，题目已说明它是最小总分。  
> - `cur_and = -1`：在 Python 中 `-1` 的二进制是全 1，等价于 “所有位都还没被清零”。  
> - `cur_and &= num`：把当前元素的位与到累计结果中。  
> - `if cur_and == 0:`：一旦累计结果为 0，说明当前子数组已经满足要求，立即计数并重置。  

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  - 对比暴力的 `O(2^n)`，线性时间几乎可以处理 `10^5` 的规模。  
- **空间复杂度**：`O(1)`，只使用了若干个整型变量，和输入规模无关。  

---

## 心得  

- **核心技巧**：利用 **整体 AND 为最小总分**，并在整体 AND 为 0 时使用 **一次遍历的贪心**（累计 AND 并在为 0 时立即切分）。  
- **适用的题型**  
  1. “把数组划分，使每段满足某种位运算条件”——如 *Split Array With Same Average*（按均值划分）等。  
  2. “要求子数组的某个累计属性达到阈值后立即结束”——如 *Maximum Number of Non-Overlapping Subarrays with Sum = 0*（累计和为 0）。  
  3. “整体属性决定最优解的上界”，比如整体最大值/最小值决定是否可以进一步划分。  
- **一句话总结**：**整体 AND 为 0 时，尽可能早地让局部 AND 变 0，就能得到最多子数组。**  

---

## 反思  

- **第一反应**：看到“AND”“最小分数”，立刻想到“整体 AND”。于是尝试枚举所有切法验证。  
- **最容易踩的坑**  
  - 忽略了 **整体 AND 为非零** 的特殊情况，导致在某些输入上错误地返回大于 1 的答案。  
  - 在贪心实现时，如果把 `cur_and` 初始化为 `0` 而不是全 1，会导致一开始就认为已经满足条件，答案错误。  
  - 边界：数组全为 0 时，每个元素都可以单独成段，答案应等于 `len(nums)`，代码的重置逻辑必须正确。  
- **下次遇到同类题**：  
  1. 先 **计算整体属性**（AND、OR、sum、max 等），看它是否已经决定答案的上限/下限。  
  2. 判断是否需要 **全局唯一解**（如整体非零只能整体），否则考虑 **贪心累计** 并在满足条件时立即切分。  

这样一步步抽象出通用思路，就能在类似的“划分 + 位运算”题目中快速找到最优解。