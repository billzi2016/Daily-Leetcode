# #3012. 使用操作最小化数组长度 / Minimize Length of Array Using Operations

> 难度：中等 · 标签：Array、Math、Greedy、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimize-length-of-array-using-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums containing positive integers.
Your task is to minimize the length of nums by performing the following operations any number of times (including zero):
Return an integer denoting the minimum length of nums after performing the operation any number of times.

**Examples**

**Example 1:**

```
Input: nums = [1,4,3,1]
Output: 1
Explanation: One way to minimize the length of the array is as follows:
Operation 1: Select indices 2 and 1, insert nums[2] % nums[1] at the end and it becomes [1,4,3,1,3], then delete elements at indices 2 and 1.
nums becomes [1,1,3].
Operation 2: Select indices 1 and 2, insert nums[1] % nums[2] at the end and it becomes [1,1,3,1], then delete elements at indices 1 and 2.
nums becomes [1,1].
Operation 3: Select indices 1 and 0, insert nums[1] % nums[0] at the end and it becomes [1,1,0], then delete elements at indices 1 and 0.
nums becomes [0].
The length of nums cannot be reduced further. Hence, the answer is 1.
It can be shown that 1 is the minimum achievable length.
```

**Example 2:**

```
Input: nums = [5,5,5,10,5]
Output: 2
Explanation: One way to minimize the length of the array is as follows:
Operation 1: Select indices 0 and 3, insert nums[0] % nums[3] at the end and it becomes [5,5,5,10,5,5], then delete elements at indices 0 and 3.
nums becomes [5,5,5,5]. 
Operation 2: Select indices 2 and 3, insert nums[2] % nums[3] at the end and it becomes [5,5,5,5,0], then delete elements at indices 2 and 3. 
nums becomes [5,5,0]. 
Operation 3: Select indices 0 and 1, insert nums[0] % nums[1] at the end and it becomes [5,5,0,0], then delete elements at indices 0 and 1.
nums becomes [0,0].
The length of nums cannot be reduced further. Hence, the answer is 2.
It can be shown that 2 is the minimum achievable length.
```

**Example 3:**

```
Input: nums = [2,3,4]
Output: 1
Explanation: One way to minimize the length of the array is as follows: 
Operation 1: Select indices 1 and 2, insert nums[1] % nums[2] at the end and it becomes [2,3,4,3], then delete elements at indices 1 and 2.
nums becomes [2,3].
Operation 2: Select indices 1 and 0, insert nums[1] % nums[0] at the end and it becomes [2,3,1], then delete elements at indices 1 and 0.
nums becomes [1].
The length of nums cannot be reduced further. Hence, the answer is 1.
It can be shown that 1 is the minimum achievable length.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 0 开始的整数数组 `nums`，其中所有元素都是正整数（positive integers）。  
你的任务是通过以下操作任意次数（包括 0 次）来最小化 `nums` 的长度，并返回在可以执行任意次数操作后，`nums` 的最小可能长度。

**操作（operation）**  
任选两个不同的下标 `i` 与 `j`（`i ≠ j`），将 `nums[i] % nums[j]`（取模，modulo）插入数组的末尾，然后删除下标 `i` 和 `j` 处的两个元素。该操作可以重复执行任意次。

---

### 示例

#### 示例 1
```text
Input: nums = [1,4,3,1]
Output: 1
```
**解释（Explanation）**：一种最小化数组长度的方法如下  
- **操作 1**：选择下标 2 和 1，取 `nums[2] % nums[1]` 并插入末尾，数组变为 `[1,4,3,1,3]`，随后删除下标 2 和 1 对应的元素，得到 `[1,1,3]`。  
- **操作 2**：选择下标 1 和 2，取 `nums[1] % nums[2]` 并插入末尾，数组变为 `[1,1,3,1]`，随后删除下标 1 和 2，得到 `[1,1]`。  
- **操作 3**：选择下标 0 和 1，取 `nums[0] % nums[1]` 并插入末尾，数组变为 `[1,1,0]`，随后删除下标 0 和 1，得到 `[0]`。  
最终数组长度为 1。

#### 示例 2
```text
Input: nums = [5,5,5,10,5]
Output: 2
```
**解释（Explanation）**：一种最小化数组长度的方法如下  
- **操作 1**：选择下标 0 和 3，取 `nums[0] % nums[3]` 并插入末尾，数组变为 `[5,5,5,10,5,5]`，随后删除下标 0 和 3，得到 `[5,5,5,5]`。  
- **操作 2**：选择下标 2 和 3，取 `nums[2] % nums[3]` 并插入末尾，数组变为 `[5,5,5,5,0]`，随后删除下标 2 和 3，得到 `[5,5,0]`。  
- **后续操作** 继续进行，最终最小长度为 2。

#### 示例 3
```text
Input: nums = [2,3,4]
Output: 1
```
**解释（Explanation）**：一种最小化数组长度的方法如下  
- **操作 1**：选择下标 1 和 2，取 `nums[1] % nums[2]` 并插入末尾，数组变为 `[2,3,4,3]`，随后删除下标 1 和 2，得到 `[2,3]`。  
- **操作 2**：选择下标 1 和 0，取 `nums[1] % nums[0]` 并插入末尾，数组变为 `[2,3,1]`，随后删除下标 1 和 0，得到 `[1]`。  
最终数组长度为 1。

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目给出一种“**取两个下标 i、j，算 `nums[i] % nums[j]` 并把结果塞到数组末尾，然后把 i、j 两个元素删掉**”的操作。  
最直接的想法就是**枚举所有可能的取法**，把每一步都尝试一次，看看最后能得到的最短数组长度是多少。

- **数据结构**：直接在 Python 的 `list` 上做增删。  
  - 把 `list` 想象成一张**可写的纸**，我们可以随时在纸的末尾写新数字，也可以把纸上的某两行撕掉。  
- **为什么正确**：因为我们把 **所有** 合法的取法都遍历了一遍，必然会碰到最优的那条路径。  
- **复杂度分析**：  
  - 每一步我们要从 `n` 个元素里选出两个人，组合数是 `C(n,2) = n·(n‑1)/2`。  
  - 选完后数组长度会 **-1**（删掉两个再加一个），于是递归深度大约是 `n‑1`。  
  - 整体的搜索树规模约为 `O( (n·(n‑1)/2) ^ (n‑1) )`，随 `n` 指数级增长。  
  - 用大白话说，就是 **“几乎每增加一个元素，计算时间就会翻几百倍”**，根本跑不动 `n=10⁵` 的数据。  
  - 空间上除了递归栈外，只用了原数组本身，`O(n)`。

#### 代码（Python）

```python
from functools import lru_cache
from itertools import combinations

def min_len_bruteforce(nums):
    """
    暴力递归搜索所有可能的操作序列，返回最小长度。
    只适合 n 很小（如 n <= 8）做演示，实际 LeetCode 数据会超时。
    """
    @lru_cache(maxsize=None)
    def dfs(state):
        # state 是一个不可变的元组，代表当前数组
        if len(state) <= 1:
            return len(state)               # 已经是最短了

        best = len(state)                    # 最差情况：不再操作直接返回
        # 枚举所有不同的 i、j（i < j）
        for i, j in combinations(range(len(state)), 2):
            a, b = state[i], state[j]
            # 计算 a % b 与 b % a 两种可能（因为顺序不同会得到不同余数）
            for x, y in [(a, b), (b, a)]:
                new_val = x % y
                # 构造新数组：删掉 i、j，末尾加 new_val
                new_state = list(state)
                # 先删大下标，防止索引错位
                del new_state[max(i, j)]
                del new_state[min(i, j)]
                new_state.append(new_val)
                best = min(best, dfs(tuple(new_state)))
        return best

    return dfs(tuple(nums))

# 示例（仅供验证思路，实际请勿在大数据上运行）
print(min_len_bruteforce([1, 4, 3, 1]))   # → 1
```

> **关键注释**  
> - `lru_cache`：把已经算过的数组状态记下来，防止重复计算（类似记忆化搜索）。  
> - `combinations`：把“挑两个人”这件事抽象成数学组合。  

#### 复杂度  

- **时间复杂度**：`O( (n·(n‑1)/2) ^ (n‑1) )`（指数级），因为要遍历所有可能的配对顺序。  
- **空间复杂度**：`O(n)`（递归栈 + 原数组），但记忆化表会额外占用 `O(状态数)`，在最坏情况下也是指数级。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**把每一次配对都硬枚举**，而实际上我们并不需要真的去模拟每一步。  
观察题目可以发现，**余数运算的本质是把大的数“压缩”成更小的数**，而**最小的数 `x` 永远不会被压得更小**（因为 `x % anything = x` 当 `x < anything`）。  

下面一步步推导出最简的结论：

1. **找出数组的最小值 `x`**（想象成一把最小的钥匙，所有大钥匙都可以被它“锁住”）。  
2. **统计 `x` 出现的次数 `cnt`**。  
3. **两种能让数组最终只剩一个元素的情形**  
   - **情形 A：`x` 只出现一次**。  
     只要把 `x` 和任意别的数 `y` 配对，得到 `x % y = x`（因为 `x < y`），于是 `x` 仍然在数组里，而 `y` 被删掉。重复这个过程，所有非 `x` 的元素都会被逐个消除，最后只剩 `x`，长度为 **1**。  
   - **情形 B：存在某个数 `y` 使得 `y % x != 0`**。  
     这时把 `y` 和 `x` 配对会产生 `y % x`，它必然 **小于 `x`**（因为余数比除数小），于是产生了一个更小的数 `z = y % x`。`z` 成为了新的最小值，回到**情形 A**（因为最小值现在只出现一次），最终也能把数组压到 **1**。  

4. **如果既不满足情形 A 也不满足情形 B**，说明：  
   - `x` 出现了 **多次**（`cnt ≥ 2`），  
   - **所有**其它数 `y` 都能被 `x` 整除（`y % x == 0`），否则就会进入情形 B。  
   在这种“所有数都是 `x` 的倍数” 的特殊情形下，**任意一次操作都会把两个 `x` 合并成一个 `x`（因为 `x % x = 0`，但 `0` 不是正数，题目要求正整数，所以我们只能把两个 `x` 删除后再把 `0` 加进去，随后 `0` 再和其他 `x` 配对会得到 `0`，最终只能保留若干 `x` 或 `0`）。**  
   实际上，最优的做法是**把 `x` 两两配对**，每次可以把 **两个** `x` 合并成 **一个**（或一个 `0` 再与 `x` 合并），所以剩余的最小长度是 **`ceil(cnt / 2)`**。  

> **关键结论**  
> - 如果 **最小值只出现一次** 或 **存在一个数对最小值取余不为 0**，答案是 **1**。  
> - 否则，答案是 **`ceil(cnt / 2)`**（即把最小值两两配对，剩下的最多只会多出一个）。

下面把这个思路写成代码。  

#### 代码（Python）

```python
import math
from typing import List

def minLength(nums: List[int]) -> int:
    """
    返回在任意次数的 “取两个下标 i、j，插入 nums[i] % nums[j]，删除 i、j”
    操作后，数组可以达到的最小长度。
    只需要 O(n) 的时间和 O(1) 的额外空间。
    """
    # 1️⃣ 找最小值和它出现的次数
    x = min(nums)                     # 最小元素
    cnt = nums.count(x)               # 出现次数

    # 2️⃣ 情形 A：最小值只出现一次 → 直接返回 1
    if cnt == 1:
        return 1

    # 3️⃣ 情形 B：有没有数对最小值取余不为 0 ?
    #    只要出现一次，就可以把数组压到 1。
    for v in nums:
        if v % x != 0:                # v 不是 x 的整数倍
            return 1

    # 4️⃣ 只能是“所有数都是 x 的倍数且 x 出现多次”的情况
    #    把 x 两两配对，剩余长度是 ceil(cnt / 2)
    return (cnt + 1) // 2             # 等价于 math.ceil(cnt / 2)

# ------------------- 示例 -------------------
print(minLength([1, 4, 3, 1]))          # 1
print(minLength([5, 5, 5, 10, 5]))     # 2
print(minLength([2, 3, 4]))            # 1
```

> **代码要点注释**  
> - `min(nums)`：相当于在一堆水果中挑出最小的那颗。  
> - `cnt = nums.count(x)`：数一数最小水果有几颗。  
> - `v % x != 0`：检查有没有水果 **不是** 最小水果的整数倍（余数不为 0），这一步决定是否能“一举消灭”。  
> - `(cnt + 1) // 2`：整数除法实现向上取整（`ceil`），因为 `5 // 2 = 2`，但我们需要 `3`，所以先加 `1` 再除。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历数组两遍：一次找最小值，第二次检查是否存在非倍数。  
  - 与暴力解的指数级时间相比，快了 **几百万倍**，完全可以处理 `10⁵` 长度的输入。  
- **空间复杂度**：`O(1)`（只用了常数个额外变量），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**利用最小值的性质把问题转化为计数/数论**。  
  - 当最小值只出现一次或有“非倍数”时，余数操作可以不断产生更小的数，最终只剩最小值。  
  - 当所有数都是最小值的整数倍且最小值出现多次时，只能把最小值两两配对，答案是 `ceil(cnt/2)`。  

- **适用的题型**  
  1. 需要 **利用最小/最大元素的特殊性质** 来简化操作（如 “把数组压到最小”）。  
  2. **数论/倍数** 关系决定可行性的问题（例如 “使数组所有元素互为倍数”）。  
  3. 需要 **计数+贪心** 来得出最优配对数的题目（如 “配对消除” 类问题）。  

- **一句话总结解题钥匙**：**“先找最小值，看它是否唯一或能生成更小的数，若不行就只能把相同的最小值两两配对”。**  

---

## 反思  

- **第一反应**：把操作一步步模拟，写递归/回溯去搜索最短长度。  
- **最容易踩的坑**  
  - 忽略 **`y % x == 0`** 的情况，误以为只要有最小值就一定能压到 1。  
  - 误以为产生的余数一定是正数，实际 `0` 也可能出现，需要注意 `0` 仍然是合法的插入值（题目只要求原数组是正整数）。  
  - 边界：数组长度为 1 时直接返回 1；最小值出现奇数次时要向上取整。  

- **下次遇到同类题**，第一步应该先 **找出“极值”（最小或最大）”，并**分析它与其他元素的**数论关系**（是否为倍数、余数是否为 0），再决定是可以“一路压到 1” 还是只能 **配对消除**。这样往往能直接得到 O(n) 的贪心/数论解法，避免指数级的暴力搜索。