# #2786. 访问数组位置以最大化得分 / Visit Array Positions to Maximize Score

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/visit-array-positions-to-maximize-score/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and a positive integer x.
You are initially at position 0 in the array and you can visit other positions according to the following rules:
Return the maximum total score you can get.
Note that initially you have nums[0] points.

**Examples**

**Example 1:**

```
Input: nums = [2,3,6,1,9,2], x = 5
Output: 13
Explanation: We can visit the following positions in the array: 0 -> 2 -> 3 -> 4.
The corresponding values are 2, 6, 1 and 9. Since the integers 6 and 1 have different parities, the move 2 -> 3 will make you lose a score of x = 5.
The total score will be: 2 + 6 + 1 + 9 - 5 = 13.
```

**Example 2:**

```
Input: nums = [2,4,6,8], x = 3
Output: 20
Explanation: All the integers in the array have the same parities, so we can visit all of them without losing any score.
The total score is: 2 + 4 + 6 + 8 = 20.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i], x <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个正整数 `x`。  
你最初位于数组下标 `0` 处，可以按照以下规则访问其他位置：

返回你能够获得的最大总得分。  
注意，初始时你已经拥有 `nums[0]` 分。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [2,3,6,1,9,2], x = 5
```  
**输出**  
```
13
```  
**解释**  
我们可以按顺序访问数组中的位置：`0 -> 2 -> 3 -> 4`。  
对应的数值分别是 `2, 6, 1, 9`。由于整数 `6` 与 `1` 的奇偶性不同，移动 `2 -> 3` 会让你损失 `x = 5` 分。  
总得分为：`2 + 6 + 1 + 9 - 5 = 13`。

#### 示例 2
**输入**  
``` 
nums = [2,4,6,8], x = 3
```  
**输出**  
```
20
```  
**解释**  
数组中的所有整数奇偶性相同，因此我们可以依次访问全部位置而不会损失任何分数。  
总得分为：`2 + 4 + 6 + 8 = 20`。

---

### 约束条件
- `2 <= nums.length <= 10^5`
- `1 <= nums[i], x <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直观的想法是：**枚举所有合法的访问顺序**，把每一种顺序算出得分，取最大值。  
因为只能向右走（下标只能增大），我们可以把问题看成“从下标 0 出发，挑选一个递增的下标序列”。  

- **数据结构**：我们用一个一维数组 `dp[i]` 表示**走到位置 i（一定会访问 i）时的最高得分**。  
  这跟查字典差不多，键是下标 `i`，值是对应的最高分数。  
- **转移**：要得到 `dp[i]`，我们可以从任意之前的下标 `j (0 ≤ j < i)` 跳到 `i`。  
  - 访问 `i` 能得到 `nums[i]` 分。  
  - 如果 `nums[j]` 与 `nums[i]` 奇偶性不同（一个偶数一个奇数），就要扣除 `x` 分。  
  所以  
  ```text
  dp[i] = max over j<i ( dp[j] + nums[i] - (parity different ? x : 0) )
  ```  

- **为什么正确**：`dp[i]` 考虑了所有可能的前一步 `j`，取最大值自然就是到 `i` 的最优得分。  
  最后答案是所有 `dp[i]`（或 `dp[n‑1]`）中的最大值。

- **复杂度分析**：  
  - 外层遍历 `i` 一次，内层要遍历所有 `j < i`，所以总共要做大约 `1 + 2 + … + (n‑1) = n·(n‑1)/2` 次比较。  
  - 用大白话说，这就是 **O(n²)**，当 `n = 10⁵` 时，大约会有 **10⁹** 次操作，电脑根本跑不完。  
  - 额外的数组 `dp` 长度为 `n`，占用 **O(n)** 的空间。

#### 代码（Python）

```python
from typing import List

def maxScore_bruteforce(nums: List[int], x: int) -> int:
    n = len(nums)
    # dp[i] 表示到达 i 并访问 i 时的最高得分
    dp = [float('-inf')] * n
    dp[0] = nums[0]                     # 起点一定拿到 nums[0]

    for i in range(1, n):
        for j in range(i):
            # 判断奇偶是否相同
            penalty = 0 if (nums[i] % 2 == nums[j] % 2) else x
            dp[i] = max(dp[i], dp[j] + nums[i] - penalty)

    # 任意位置都可以是结束点，取最大即可
    return max(dp)
```

> **关键行中文注释**  
> - `dp = [float('-inf')] * n`：把所有位置的得分先设为负无穷，表示“还没算出来”。  
> - `penalty = 0 if (nums[i] % 2 == nums[j] % 2) else x`：奇偶相同不扣分，否者扣 `x`。  
> - `dp[i] = max(dp[i], dp[j] + nums[i] - penalty)`：把所有可能的前一步 `j` 的得分取最大。

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环导致的平方级增长。  
- **空间复杂度**：`O(n)` —— 只用了 `dp` 一个长度为 `n` 的数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**转移只和前一步的奇偶性有关**，而不是具体是哪一个下标。  
这提示我们可以把“所有已经算好的位置”按照奇偶性分成两类来维护：  

- `best_even`：截至目前（只看 **左侧**），**最后访问的数是偶数** 时的最高得分。  
- `best_odd`：截至目前，**最后访问的数是奇数** 时的最高得分。  

当我们要计算 `dp[i]`（即访问到位置 `i` 的最高得分）时，只需要看这两个“代表值”，不必遍历所有 `j`：

| 当前 `nums[i]` 的奇偶 | 需要的前一步 | 是否扣 `x` | 公式 |
|----------------------|--------------|-----------|------|
| 偶数 (`%2==0`)       | 之前也是偶数 | 不扣       | `best_even + nums[i]` |
| 偶数                 | 之前是奇数   | 扣 `x`    | `best_odd + nums[i] - x` |
| 奇数 (`%2==1`)       | 之前是奇数   | 不扣       | `best_odd + nums[i]` |
| 奇数                 | 之前是偶数   | 扣 `x`    | `best_even + nums[i] - x` |

于是：

```text
if nums[i] is even:
    dp_i = max(best_even + nums[i],          # 同 parity，不扣
               best_odd  + nums[i] - x)      # 不同 parity，扣 x
else:
    dp_i = max(best_odd  + nums[i],          # 同 parity，不扣
               best_even + nums[i] - x)      # 不同 parity，扣 x
```

计算完 `dp_i` 以后，要把它放回对应的 “best” 里，保持 **“截至当前位置的最佳”**：

- 如果 `nums[i]` 是偶数，就 `best_even = max(best_even, dp_i)`。  
- 如果是奇数，就 `best_odd  = max(best_odd , dp_i)`。

**初始化**  
- 起点 0 必须访问，得分 `nums[0]`。  
- 根据 `nums[0]` 的奇偶性，给相应的 `best_even / best_odd` 赋初值，其余设为负无穷（表示“不可能”）。

**为什么正确**  
- 任何合法的访问序列的最后一步一定是某个下标 `i`。  
- 在到达 `i` 之前，序列的得分已经是 **某个奇偶类别的最佳**（因为我们一直在维护 `best_even / best_odd`）。  
- 当我们把 `i` 加进去，只需要考虑两种可能的前一步奇偶性，取更大的即可。  
- 这与暴力 DP 的转移等价，只是把 **所有 j** 的信息压缩成了 **两个代表值**，不会遗漏任何更优的选择。

**复杂度**：只遍历一次数组，时间 **O(n)**，空间只用常数几个变量，**O(1)**。

#### 代码（Python）

```python
from typing import List

def maxScore(nums: List[int], x: int) -> int:
    """
    动态规划 + 按奇偶分类的最优状态压缩
    """
    n = len(nums)
    # 负无穷表示「还没有出现」的状态
    NEG = float('-inf')

    # 根据起点的奇偶性初始化
    if nums[0] % 2 == 0:          # 起点是偶数
        best_even = nums[0]       # 以偶数结尾的最高分
        best_odd  = NEG           # 还没有奇数结尾的路径
    else:                         # 起点是奇数
        best_odd  = nums[0]
        best_even = NEG

    # ans 用来记录全局最大（可以直接取 max(best_even, best_odd)）
    ans = nums[0]

    # 从下标 1 开始遍历
    for i in range(1, n):
        val = nums[i]
        if val % 2 == 0:          # 当前是偶数
            # 两种来源：前一步是偶数（不扣）或是奇数（扣 x）
            cand1 = best_even + val                # 同 parity
            cand2 = best_odd  + val - x if best_odd != NEG else NEG  # 不同 parity
            dp_i = max(cand1, cand2)
            # 更新 best_even（因为现在以偶数结尾的路径可能更好）
            best_even = max(best_even, dp_i)
        else:                     # 当前是奇数
            cand1 = best_odd  + val                # 同 parity
            cand2 = best_even + val - x if best_even != NEG else NEG
            dp_i = max(cand1, cand2)
            best_odd = max(best_odd, dp_i)

        ans = max(ans, dp_i)      # 维护全局最大

    return ans
```

> **代码要点中文注释**  
> - `NEG = float('-inf')`：表示「目前还不存在」的状态，防止误用。  
> - `cand2 = best_odd + val - x if best_odd != NEG else NEG`：只有当对应的 `best` 已经出现过才可以使用，否则视作负无穷。  
> - `best_even = max(best_even, dp_i)`：把新的以偶数结尾的路径和旧的比较，保留更大的。  
> - `ans = max(ans, dp_i)`：虽然 `best_even / best_odd` 已经保存了全局最优，但把答案单独记录更直观。

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每一步做常数次运算。  
  与暴力 `O(n²)` 相比，速度提升约 **n 倍**（对 10⁵ 的数据可以轻松在毫秒级完成）。  
- **空间复杂度**：`O(1)` —— 只用了几个标量变量 (`best_even`, `best_odd`, `ans`)。

---

## 心得  

- **核心技巧**：**状态压缩 DP**——把原本需要 `O(n²)` 的转移（所有前驱 `j`）压缩成 **奇偶两类**的最优子状态。  
- **适用题型**：  
  1. **只和前一步的「属性」有关**（如奇偶、颜色、正负号）的序列优化问题。  
  2. **转移代价只取决于两种分类**（例如「相同/不同」）的路径最大化/最小化问题。  
  3. 类似的 LeetCode 题目还有  
     - *Maximum Sum of a Subsequence With Non‑Adjacent Constraint*（利用「上一个是否选」的两状态）  
     - *Best Time to Buy and Sell Stock with Transaction Fee*（使用「持有/不持有」两状态）  

- **一句话总结解题钥匙**：  
  **把所有可能的前驱压缩成「类别」的最优值，只在类别之间转移**。

---

## 反思  

- **第一反应**：直接写「遍历所有前驱」的 DP，想到 O(n²) 的解法。  
- **最容易踩的坑**  
  - 忘记把起点 `nums[0]` 的分数计入答案。  
  - 在更新 `best_even / best_odd` 时误用了 `dp_i` 前的旧值，导致遗漏当前下标本身的贡献。  
  - 对 `best` 尚未出现的情况（仍为负无穷）直接相加，会产生 `nan` 或错误的负数，需要专门判空。  
- **下次类似题的第一步**：  
  **先问自己“转移只依赖于哪些属性？”**，如果属性种类很少（如奇偶、颜色两类），就立刻考虑 **按属性分组维护最优子状态**，从而把「遍历所有前驱」降到「遍历属性种类」的 O(1) 级别。