# #2654. 使所有数组元素等于 1 的最少操作次数 / Minimum Number of Operations to Make All Array Elements Equal to 1

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisiting of positive integers. You can do the following operation on the array any number of times:
Return the minimum number of operations to make all elements of nums equal to 1. If it is impossible, return -1.
The gcd of two integers is the greatest common divisor of the two integers.

**Examples**

**Example 1:**

```
Input: nums = [2,6,3,4]
Output: 4
Explanation: We can do the following operations:
- Choose index i = 2 and replace nums[2] with gcd(3,4) = 1. Now we have nums = [2,6,1,4].
- Choose index i = 1 and replace nums[1] with gcd(6,1) = 1. Now we have nums = [2,1,1,4].
- Choose index i = 0 and replace nums[0] with gcd(2,1) = 1. Now we have nums = [1,1,1,4].
- Choose index i = 2 and replace nums[3] with gcd(1,4) = 1. Now we have nums = [1,1,1,1].
```

**Example 2:**

```
Input: nums = [2,10,6,14]
Output: -1
Explanation: It can be shown that it is impossible to make all the elements equal to 1.
```

**Constraints**

- 2 <= nums.length <= 50
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

**题目描述**

给定一个下标从 0 开始的数组 `nums`，其中所有元素都是正整数。你可以对数组执行以下操作任意次：

- 选择任意下标 `i`（`0 ≤ i < nums.length - 1`），用 `gcd(nums[i], nums[i+1])` 替换 `nums[i]` 或 `nums[i+1]` 中的一个元素，其中 **gcd（greatest common divisor）** 表示两个整数的最大公约数。

返回使 `nums` 中所有元素都等于 1 的最小操作次数。如果无法做到，返回 `-1`。

**示例**

**示例 1**

```
输入: nums = [2,6,3,4]
输出: 4
解释:
我们可以按以下顺序进行操作:
- 选择下标 i = 2，将 nums[2] 替换为 gcd(3,4) = 1，得到 nums = [2,6,1,4]。
- 选择下标 i = 1，将 nums[1] 替换为 gcd(6,1) = 1，得到 nums = [2,1,1,4]。
- 选择下标 i = 0，将 nums[0] 替换为 gcd(2,1) = 1，得到 nums = [1,1,1,4]。
- 选择下标 i = 3，将 nums[3] 替换为 gcd(1,4) = 1，得到 nums = [1,1,1,1]。
共计 4 次操作。
```

**示例 2**

```
输入: nums = [2,10,6,14]
输出: -1
解释: 可以证明，无论如何操作，都无法让所有元素变为 1。
```

**约束条件**

- `2 ≤ nums.length ≤ 50`
- `1 ≤ nums[i] ≤ 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们要把数组 `nums` 中的所有数都变成 **1**，唯一允许的操作是：

> 任选下标 `i (0 ≤ i < n-1)`，用 `gcd(nums[i], nums[i+1])` 替换 `nums[i]`（或 `nums[i+1]`，两者等价）。

把这个过程想象成 **“两个相邻的数相互‘融合’，只保留它们的最大公约数”**。  
如果两个数本来就互质（最大公约数是 1），融合一次就能得到 1；否则融合后得到的仍然是大于 1 的数，需要继续和别的数融合。

**最直接的想法**：

1. **先检查数组里有没有 1**。  
   - 1 的作用类似字典里已经有的“页码”，只要出现一次，就可以把它左边或右边的数一次一次“擦掉”变成 1。  
   - 因此如果已经有 `cnt1` 个 1，剩下的 `n - cnt1` 个非 1 只需要各 **一次** 操作就能变成 1，答案就是 `n - cnt1`。

2. **如果数组里没有 1**，我们只能靠“融合”产生第一个 1。  
   - 只要找到一个 **最短的连续子数组**，其所有元素的 gcd 为 1，就可以在这个子数组内部通过 `len-1` 次融合得到一个 1（把子数组从左到右依次融合）。  
   - 之后我们手里就有了一个 1，接下来把剩下的 `n-1` 个元素都变成 1，每个只需要一次操作。  
   - 所以总操作数 = `(len-1)   // 产生第一个 1`  + ` (n-1)   // 把其它元素变成 1` = `len + n - 2`。

3. **如果所有子数组的 gcd 都大于 1**，说明整个数组的所有数都有公共因子，根本不可能得到 1，返回 `-1`。

> **生活化类比**：  
> - 把数组看成一排水管，水管口径是数字本身。  
> - 两根相邻的水管接在一起后，流出的水口径只能是它们共同的最小口径（gcd）。  
> - 只要有一根口径为 1 的水管，其他水管只要和它相连一次，就都能把口径调到 1。

#### 代码（Python）

```python
import math
from typing import List

def min_operations(nums: List[int]) -> int:
    n = len(nums)

    # 1️⃣ 统计数组里已经是 1 的个数
    cnt_one = nums.count(1)
    if cnt_one:
        # 已有 cnt_one 个 1，剩下的每个只需要一次操作
        return n - cnt_one

    # 2️⃣ 没有 1，尝试寻找最短子数组，使其 gcd 为 1
    min_len = float('inf')                     # 记录最短长度
    for i in range(n):
        cur_gcd = 0
        for j in range(i, n):
            cur_gcd = math.gcd(cur_gcd, nums[j])   # 逐步累加 gcd
            if cur_gcd == 1:                       # 找到一个子数组 gcd 为 1
                min_len = min(min_len, j - i + 1)
                break                              # 这个 i 起点已经够短，结束内层循环

    # 3️⃣ 判断是否真的可以得到 1
    if min_len == float('inf'):                 # 没有任何子数组的 gcd 为 1
        return -1

    # 4️⃣ 计算总操作数：产生第一个 1 需要 (min_len-1) 次，之后把其余 n-1 个数变成 1
    return min_len + n - 2
```

- `math.gcd` 就像 **字典查词**，把两个数当作“词”，返回它们共同的“页码”（最大公约数）。
- 两层循环 `i, j` 直接遍历所有连续子数组，时间上是 **暴力** 的。

#### 复杂度  

- **时间复杂度**：`O(n² * logV)`  
  - 两层循环遍历所有子数组是 `O(n²)`，每次求 gcd 的时间是 `O(log V)`（`V` 为数字的大小，最大 `10⁶`），所以整体是二次方级别。  
  - 用大白话说，就是如果数组长度是 50，最坏要比较大约 `50*50 = 2500` 次，每次算一个小的除法，完全可以接受。

- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量，和数组大小无关。

---

### 2. 最优解  

#### 思路  

从暴力解我们已经得到核心公式：

- 若数组已有 1，答案 = `n - cnt1`。  
- 否则，找最短子数组长度 `L` 使其 gcd 为 1，答案 = `L + n - 2`。  

**瓶颈**在于 **暴力搜索子数组**，时间是 `O(n²)`。  
因为 `n ≤ 50`，暴力已经足够快，实际上不需要进一步优化。  
但为了让思路更完整，我们仍然可以把 “寻找最短 gcd 为 1 的子数组” 用 **一次遍历 + 滑动窗口** 的思想来解释——只要在遍历时实时维护当前 gcd，一旦发现为 1，就立刻记录长度并尝试缩短左端。

下面给出一种 **更简洁的实现**，仍然是 `O(n²)`（因为 gcd 不是单调的，无法用真正的 O(n) 滑动窗口），但代码结构更清晰，且把 “产生第一个 1 的代价” 与 “把其余元素变成 1 的代价” 明确分开，帮助读者快速记忆公式。

**关键算法/数据结构**：

- **欧几里得算法**（`math.gcd`）——求最大公约数的经典方法，时间复杂度是 `O(log V)`，这里我们把它当作“黑盒”使用。  
- **前缀 gcd**（可选）——如果想把子数组 gcd 计算降到 `O(1)`，可以预处理前缀和后缀 gcd，整体仍是 `O(n²)`，但常数更小。这里为了易懂，直接用双层循环。

**步骤**：

1. 统计已有的 1 的数量 `cnt1`。  
2. 若 `cnt1 > 0`，直接返回 `n - cnt1`。  
3. 否则，遍历所有左端 `i`，从 `i` 开始向右累积 gcd，找到第一次等于 1 的右端 `j`，记录长度 `j-i+1`，更新最小长度 `L`。  
4. 若遍历结束仍未找到 `L`，说明所有数都有公共因子，返回 `-1`。  
5. 否则答案 = `L + n - 2`（`L-1` 次产生 1，`n-1` 次把其它数变成 1）。

#### 代码（Python）

```python
import math
from typing import List

def min_operations_opt(nums: List[int]) -> int:
    n = len(nums)

    # 统计已有的 1
    cnt_one = nums.count(1)
    if cnt_one:
        # 每个非 1 只需要一次操作
        return n - cnt_one

    # 没有 1，寻找最短子数组 gcd 为 1
    min_len = n + 1                 # 初始设为不可能的大值
    for i in range(n):
        cur = 0
        for j in range(i, n):
            cur = math.gcd(cur, nums[j])
            if cur == 1:
                min_len = min(min_len, j - i + 1)
                break               # 对当前 i，已经是最短的了

    # 若仍未找到，则 impossible
    if min_len == n + 1:
        return -1

    # 产生第一个 1 需要 (min_len-1) 次，随后把其余 n-1 个数变成 1
    return min_len + n - 2
```

- 代码几乎和暴力版一样，只是把 “已有 1 的情况” 单独提前判断，提升可读性。  
- `min_len` 初始化为 `n+1`（大于任何可能的子数组长度），用来判断是否找到合法子数组。

#### 复杂度  

- **时间复杂度**：`O(n² * logV)`  
  - 与暴力解相同，因为我们仍然需要检查所有子数组的 gcd。  
  - 对于本题的约束 `n ≤ 50`，这已经是 **最优** 的实际运行时间，没有必要再做更复杂的优化。

- **空间复杂度**：`O(1)`  
  - 只使用常数个额外变量。

---

## 心得  

- **核心技巧**：把“把所有数变成 1”拆成两步——  
  1. **产生第一个 1**（寻找 gcd 为 1 的最短子数组）。  
  2. **利用已有的 1**，一次操作把相邻的数变成 1。  

- **适用的题型**（类似思路）  
  1. **最短子数组的 gcd 为 1**（如 LeetCode 1979）。  
  2. **数组中出现 1 后的最小操作数**（如 “Make Array Elements Equal” 系列）。  
  3. **利用已有的“好”元素快速消除其他元素**（如 “Minimum Operations to Reduce X to Zero” 中的贪心思路）。

- **一句话总结解题钥匙**：  
  > **先造出一个 1，随后所有元素只要一次“和 1 求 gcd”就能变成 1**。

---

## 反思  

- **第一反应**：看到“gcd”和“全部变成 1”，自然想到 **“只要出现一次互质的组合，就能产生 1”**，于是把问题拆成“是否已有 1”和“怎样最快得到第一个 1”。  

- **最容易踩的坑**  
  1. **忘记统计已有的 1**，导致把已经有 1 的情况也跑进 “寻找子数组” 的循环，得到错误的更大答案。  
  2. **边界条件**：当最短子数组长度为 2 时，`L + n - 2` 正好等于 `n`，要确保公式不越界。  
  3. **返回 -1 的时机**：如果所有数的 gcd 大于 1，整个数组不可能出现 1，必须在遍历结束后统一返回 -1，而不是在某个局部判断中提前退出。

- **下次类似题的第一步**：  
  > **检查数组里是否已经存在目标状态（这里是 1），如果有，直接用线性计数得到答案；如果没有，先寻找最小的“能产生目标状态的子结构”。**  

这样一步步拆解，既能保证思路清晰，又能写出简洁且高效的代码。祝你玩得开心！