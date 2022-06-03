# #1802. 受限数组中给定下标的最大值 / Maximum Value at a Given Index in a Bounded Array

> 难度：中等 · 标签：Math、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/)

---

## 题目（英文原版）

**Description**

You are given three positive integers: n, index, and maxSum. You want to construct an array nums (0-indexed) that satisfies the following conditions:
Return nums[index] of the constructed array.
Note that abs(x) equals x if x >= 0, and -x otherwise.

**Examples**

**Example 1:**

```
Input: n = 4, index = 2,  maxSum = 6
Output: 2
Explanation: nums = [1,2,2,1] is one array that satisfies all the conditions.
There are no arrays that satisfy all the conditions and have nums[2] == 3, so 2 is the maximum nums[2].
```

**Example 2:**

```
Input: n = 6, index = 1,  maxSum = 10
Output: 3
```

**Constraints**

- 1 <= n <= maxSum <= 109
- 0 <= index < n

---

## 题目（中文翻译）

给定三个正整数 `n`、`index` 和 `maxSum`。你需要构造一个长度为 `n` 的数组 `nums`（0 索引），使其满足以下条件：

1. `nums` 中所有元素都是正整数（> 0）。
2. 任意相邻元素的绝对差不超过 1，即 `abs(nums[i] - nums[i-1]) <= 1`（`abs(x)` 等于 `x` 当 `x >= 0`，否则等于 `-x`）。
3. 整个数组的元素和不超过 `maxSum`，即 `sum(nums) <= maxSum`。
4. 在满足上述所有条件的前提下，使 `nums[index]` 取得最大可能值。

返回构造的数组中 `nums[index]` 的最大值。

---

**示例 1**  
**输入**: `n = 4, index = 2, maxSum = 6`  
**输出**: `2`  
**解释**: `nums = [1, 2, 2, 1]` 是满足所有条件的一种数组。不存在满足条件且 `nums[2] == 3` 的数组，所以答案为 `2`。

**示例 2**  
**输入**: `n = 6, index = 1, maxSum = 10`  
**输出**: `3`

---

**约束条件**  

- `1 <= n <= maxSum <= 10^9`
- `0 <= index < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**先猜一个 `nums[index]` 的值 `target`，再把数组填满，看看总和是否不超过 `maxSum`**。  
具体做法可以这样想：

1. 把 `nums[index]` 设为 `target`。  
2. 向左走一步，按照 “相邻两个数差的绝对值 ≤ 1” 的要求，最小化左边的数——于是左边第一个数是 `target‑1`，再往左是 `target‑2`，依此类推，直到降到 1 为止。  
3. 向右同理。  
4. 把所有得到的数加起来，如果 ≤ `maxSum`，说明这个 `target` 是可行的；否则不可行。  

> **类比**：把 `target` 想成山顶的高度，左边右边的坡度只能每一步降 1，坡底最低是 1（因为数组元素必须是正整数），我们在求“在给定坡度限制下，山的最小体积”。  

因为题目里 `n` 最大可以到 `10⁹`，直接把数组真的生成出来并遍历求和根本不可行——这就是暴力解的 **瓶颈**（时间和空间都会爆炸）。

#### 代码（Python）

```python
def brute_max_value(n: int, index: int, maxSum: int) -> int:
    # 暴力尝试所有可能的 target（从 1 到 maxSum）
    for target in range(1, maxSum + 1):
        # 计算左侧最小和
        left_len = index                # 左边有多少个位置
        left_sum = 0
        cur = target - 1                # 左边第一个数
        for _ in range(left_len):
            left_sum += max(cur, 1)      # 不能小于 1
            cur -= 1

        # 计算右侧最小和
        right_len = n - index - 1
        right_sum = 0
        cur = target - 1
        for _ in range(right_len):
            right_sum += max(cur, 1)
            cur -= 1

        total = left_sum + right_sum + target   # 加上 index 位置的 target
        if total > maxSum:               # 已经超过上限，后面的 target 更大肯定不行
            return target - 1
    return maxSum                         # 极端情况下全部放在 index 位置
```

> **注意**：上述代码仅用于说明思路，**在实际测试里会超时**，因为循环次数可能达到 `10⁹`。

#### 复杂度  

- **时间复杂度**：`O(maxSum * n)`，最坏情况下要遍历每一个 `target`，并对每个 `target` 再遍历左、右两边的所有元素。用大白话说，就是“每秒跑几万次都跑不完”。  
- **空间复杂度**：`O(1)`，只用了常数个变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到：**关键是判断某个 `target` 能否让数组的最小可能和 ≤ `maxSum`**。如果我们能在 **对数时间** 内快速算出“最小和”，就可以二分搜索 `target`，从而得到最大可行值。

**步骤拆解**：

1. **把判断过程抽象为函数** `enough(target)`，返回 `True` 表示在 `target` 为 `nums[index]` 时，满足所有约束的最小总和 ≤ `maxSum`。  
2. **如何在 O(1) 计算最小总和？**  
   - 左侧有 `left = index` 个位置。  
   - 如果 `target-1` 大于等于 `left`，说明左边可以完整下降 `left` 步，不会碰到 1。此时左侧是等差数列 `target-1, target-2, …, target-left`，和为  

\[
\text{left\_sum} = \frac{(target-1 + target-left) \times left}{2}
\]

   - 否则左边会先降到 1，然后剩下的格子只能全填 1。左侧和等于  

\[
\text{left\_sum} = \frac{(target-1 + 1) \times (target-1)}{2} \;+\; (left - (target-1)) \times 1
\]

   - 右侧同理，用 `right = n - index - 1`。  
3. **整体最小和**  

\[
\text{total} = \text{left\_sum} + \text{right\_sum} + target
\]

4. **二分搜索**  
   - `low = 1`（最小可能值），`high = maxSum`（上界，实际上不会超过 `maxSum`）。  
   - 每次取 `mid = (low + high + 1) // 2`（向上取整防止死循环），如果 `enough(mid)` 为真，说明 `mid` 可行，尝试更大；否则缩小上界。  
   - 结束时 `low` 即为答案。

> **类比**：把 `target` 看成山的高度，左/右坡的长度固定。我们用等差数列公式快速算出“坡下的土方量”，再与预算 `maxSum` 比较。二分搜索就像在一条单调递增的坡度-预算曲线上“找最高的那一点”。  

#### 代码（Python）

```python
def maxValue(n: int, index: int, maxSum: int) -> int:
    """
    二分搜索 + 等差数列求和，时间 O(log maxSum)，空间 O(1)
    """

    def min_sum(target: int) -> int:
        """
        在 nums[index] = target 的前提下，满足
        - 相邻差 <= 1
        - 所有元素 >= 1
        的最小可能总和。
        """
        # ---------- 左侧 ----------
        left_len = index               # 左边有多少个格子
        if target > left_len:
            # 左侧可以完整下降 left_len 步
            # 等差数列首项 target-1，末项 target-left_len
            left_sum = (target - 1 + target - left_len) * left_len // 2
        else:
            # 左侧会降到 1，然后剩余格子全是 1
            # 先算从 target-1 到 1 的和
            left_sum = (target - 1 + 1) * (target - 1) // 2
            # 再加上剩余的 1
            left_sum += left_len - (target - 1)

        # ---------- 右侧 ----------
        right_len = n - index - 1
        if target > right_len:
            right_sum = (target - 1 + target - right_len) * right_len // 2
        else:
            right_sum = (target - 1 + 1) * (target - 1) // 2
            right_sum += right_len - (target - 1)

        # ---------- 合计 ----------
        return left_sum + right_sum + target

    # 二分搜索目标值
    low, high = 1, maxSum
    while low < high:
        mid = (low + high + 1) // 2   # 取上中位数，防止死循环
        if min_sum(mid) <= maxSum:    # 还能接受，尝试更大
            low = mid
        else:                         # 超出预算，必须缩小
            high = mid - 1
    return low
```

> 代码里每一段都有中文注释，直接复制运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(log maxSum)`  
  - 二分搜索的迭代次数是 `log₂(maxSum)`（`maxSum ≤ 10⁹`，大约 30 次）。每次只做常数次的算术运算，算是“眨眼间”。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。

---

## 心得  

- **核心技巧**：**把“能否构造”转化为**“在给定峰值下的最小可能和”**，并用等差数列公式 O(1) 计算。随后 **二分搜索** 单调函数得到最大可行峰值。  
- **适用的类似题型**：  
  1. *Maximum Sum of a Subarray With Length Constraint*（需要在约束下求最大值）  
  2. *Find the Minimum Number of Days to Make m Bouquets*（判断可行性 + 二分）  
  3. *K-th Smallest Subset Sum*（单调性 + 二分）  
- **一句话总结解题钥匙**：**把“最大化”问题先转化为“判定某值是否可行”，利用单调性二分搜索**。

---

## 反思  

- **第一反应**：直接把数组枚举出来，尝试每个 `nums[index]`，但立刻意识到 `n` 太大，必须找更快的方式。  
- **最容易踩的坑**：  
  - **等差求和公式的边界**：当 `target` 小于左/右长度时，需要额外加上剩余的 1。容易漏掉 `+ (len - (target-1))`。  
  - **二分取中位数的写法**：如果写成 `mid = (low + high) // 2`，在 `low` 已经可行的情况下会出现死循环，应该取上中位数 `mid = (low + high + 1) // 2`。  
  - **整数溢出**（在某些语言中）：乘法后除以 2 前可能超出 64 位范围，Python 自动大整数所以不怕，但在 C++/Java 需要用 `long long`。  
- **下次遇到同类题**：第一步先 **思考“给定一个阈值，最小/最大可能值是多少”**，把问题抽象为单调判定函数，再 **二分搜索**。这样可以把看似指数级的搜索压到对数级。