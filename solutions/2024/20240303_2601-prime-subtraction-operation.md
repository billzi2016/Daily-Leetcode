# #2601. **质数减法操作** / Prime Subtraction Operation

> 难度：中等 · 标签：Array、Math、Binary Search、Greedy、Number Theory · [LeetCode 链接](https://leetcode.com/problems/prime-subtraction-operation/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n.
You can perform the following operation as many times as you want:
Return true if you can make nums a strictly increasing array using the above operation and false otherwise.
A strictly increasing array is an array whose each element is strictly greater than its preceding element.

**Examples**

**Example 1:**

```
Input: nums = [4,9,6,10]
Output: true
Explanation: In the first operation: Pick i = 0 and p = 3, and then subtract 3 from nums[0], so that nums becomes [1,9,6,10].
In the second operation: i = 1, p = 7, subtract 7 from nums[1], so nums becomes equal to [1,2,6,10].
After the second operation, nums is sorted in strictly increasing order, so the answer is true.
```

**Example 2:**

```
Input: nums = [6,8,11,12]
Output: true
Explanation: Initially nums is sorted in strictly increasing order, so we don't need to make any operations.
```

**Example 3:**

```
Input: nums = [5,8,3]
Output: false
Explanation: It can be proven that there is no way to perform operations to make nums sorted in strictly increasing order, so the answer is false.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- nums.length == n

---

## 题目（中文翻译）

给定一个下标从 0 开始、长度为 `n` 的整数数组 `nums`。

你可以无限次执行以下操作：

- 任选一个下标 `i`（`0 ≤ i < n`）和一个质数 `p`（`p` 为素数且 `p ≤ nums[i]`），将 `nums[i]` 减去 `p`，即 `nums[i] = nums[i] - p`。

返回 `true`，如果可以通过上述操作使数组 `nums` 变为**严格递增数组（strictly increasing array）**；否则返回 `false`。

**严格递增数组** 是指数组中每个元素都严格大于其前一个元素。

---

### 示例

**示例 1**  
> **输入**: `nums = [4,9,6,10]`  
> **输出**: `true`  
> **解释**:  
> 第一次操作: 选择 `i = 0`，`p = 3`，`nums[0]` 减 3，数组变为 `[1,9,6,10]`。  
> 第二次操作: 选择 `i = 1`，`p = 7`，`nums[1]` 减 7，数组变为 `[1,2,6,10]`。  
> 此时数组已经是严格递增的，故答案为 `true`。

**示例 2**  
> **输入**: `nums = [6,8,11,12]`  
> **输出**: `true`  
> **解释**: 初始数组已经是严格递增的，无需进行任何操作。

**示例 3**  
> **输入**: `nums = [5,8,3]`  
> **输出**: `false`  
> **解释**: 可以证明无论怎样进行上述操作，都无法将数组变为严格递增，故答案为 `false`。

---

### 约束条件

- `1 ≤ nums.length ≤ 1000`
- `1 ≤ nums[i] ≤ 1000`
- `nums.length == n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的操作顺序**，把每个位置的数字要么保持不变，要么减去一个素数（只允许减一次），然后检查最终数组是否严格递增。  

- **数据结构**：我们可以把每个位置的所有“可达值”放进一个列表里。列表就像一本**字典**，键是原始数字，值是它可以变成的所有数字（原来的数字 + “减去的素数”）。
- **为什么正确**：只要遍历到了**所有**合法的取值组合，就一定能找到一种使数组递增的方案（如果存在的话），因为我们没有遗漏任何一种合法的减法。
- **复杂度分析**：  
  - 对于长度为 `n` 的数组，每个位置的可达值最多有 `π(1000) + 1 ≈ 168`（所有不大于 1000 的素数再加上“不减”这一个）种。  
  - 暴力枚举相当于在每个位置上做一次“多叉树”遍历，最坏情况需要遍历 `168ⁿ` 种组合，时间随 `n` **指数级**增长。  
  - 空间上只需要保存递归栈，最坏也只会达到 `O(n)`。

> **大白话**：如果你把每一步都想成“尝试所有可能”，那你会像在一个非常深、非常宽的迷宫里不停地转来转去，根本走不完。

#### 代码（Python）

```python
import math
from typing import List

# 判断一个数是否为素数（暴力写法，仅用于说明）
def is_prime(x: int) -> bool:
    if x < 2:
        return False
    for d in range(2, int(math.sqrt(x)) + 1):
        if x % d == 0:
            return False
    return True

# 递归暴力搜索
def dfs(nums: List[int], idx: int, prev: int) -> bool:
    if idx == len(nums):          # 所有位置都处理完了
        return True

    # 生成当前位置所有合法的取值
    candidates = [nums[idx]]                     # 不减
    for p in range(2, nums[idx] + 1):
        if is_prime(p) and nums[idx] - p > 0:    # 减去一个素数
            candidates.append(nums[idx] - p)

    # 逐一尝试
    for cur in sorted(candidates):               # 先尝试小的，有助于提前剪枝
        if cur > prev:                           # 必须严格大于前一个数
            if dfs(nums, idx + 1, cur):
                return True
    return False

def primeSubtractionOperation_bruteforce(nums: List[int]) -> bool:
    return dfs(nums, 0, 0)
```

> 代码中每一行都写了中文注释，直接复制即可运行（只适用于非常小的 `n`，否则会超时）。

#### 复杂度

- **时间复杂度**：`O(168ⁿ)`（指数级），因为每个位置最多有 168 种选择，全部遍历。  
  - **含义**：当 `n` 增加到 10、20…时，计算量会像“天文数字”一样迅速膨胀，普通电脑根本跑不完。
- **空间复杂度**：`O(n)`，递归栈的深度最多等于数组长度。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“枚举所有可能”** 是极其低效的。我们需要抓住题目中的关键限制：

1. **每个位置只能减一次素数**（或者不减）。  
2. **只能减去素数**，最小的素数是 2，所以**减 1 是不可能的**。  
3. 目标是让数组**严格递增**，因此我们希望每个位置的取值尽可能 **小**，只要满足大于前一个数即可。

**核心观察**  
设前一个已经确定的值为 `prev`，当前原始数字为 `x`。我们希望选一个最小的 `v`，满足：

- `v > prev`（严格递增）  
- `v == x`（不减） **或** `x - v` 是素数（减去的正好是一个素数）  

换句话说，**只要 `x - (prev+1)` 是 0 或素数，就可以把当前位置取成 `prev+1`**。如果 `prev+1` 不满足（比如差是 1，或者差不是素数），我们只能把 `v` 向上调大一点，再继续检查。

因为 `nums[i] ≤ 1000`，我们可以 **预先用埃拉托斯特尼筛法** 生成 `[0, 1000]` 区间的所有素数，随后在每一步只需 O(1) 判断 “差值是否为素数”。遍历 `v` 的次数最多也只会是 `x - prev`，而 `x ≤ 1000`，所以整体时间是 `O(n·max(nums))`，对本题完全够快。

**算法步骤（伪代码）**

```
pre = 0                                   # 前一个已经确定的值，0 相当于哨兵
for each x in nums:
    need = pre + 1                         # 最小可能的取值
    while need <= x:
        diff = x - need                    # 需要减去的量
        if diff == 0 or diff is prime:    # 0 表示不减，prime 表示只减一次素数
            break                         # 找到合法的最小值
        need += 1                          # 向上尝试更大的值
    if need > x:                           # 没有合法取值
        return False
    pre = need                             # 确定当前值，继续下一个位置
return True
```

**为什么是最优的？**  
- **贪心**：我们每一步都选 **最小** 能满足条件的值。因为后面的元素只能比当前更大，选更小的当前值永远不会妨碍后面的选择，反而给后面留出了更大的“操作空间”。  
- **只检查一次**：通过素数表的 O(1) 查找，整个过程只遍历一次数组，时间线性。

#### 代码（Python）

```python
import math
from typing import List

# 预处理：埃拉托斯特尼筛法，返回 [0, limit] 区间的素数集合
def sieve(limit: int) -> set:
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return {i for i, val in enumerate(is_prime) if val}

# 主函数
def primeSubtractionOperation(nums: List[int]) -> bool:
    # 题目限制 nums[i] ≤ 1000，提前算好所有素数
    primes = sieve(1000)

    prev = 0                     # 已确定的前一个数，初始为 0（比所有正整数都小）
    for x in nums:
        need = prev + 1          # 必须严格大于前一个数
        # 在可行区间 [need, x] 内寻找最小合法值
        while need <= x:
            diff = x - need      # 需要减去的量
            if diff == 0 or diff in primes:   # 0 表示不减，diff 为素数则只减一次素数
                break            # 找到合法的最小值，退出循环
            need += 1            # 当前值不可行，尝试更大的值
        if need > x:             # 循环结束仍未找到合法值 → 失败
            return False
        prev = need              # 确定当前位置的取值，继续检查下一个
    return True
```

**代码要点解释（中文注释）**

- `sieve`：把“找素数”这件事搬到程序一开始完成，后面只需要 O(1) 查询是否为素数。  
- `prev`：相当于“前一个已经排好序的数字”。我们把它初始化为 0，这样第一个元素只要大于 0 即可。  
- `need = prev + 1`：因为数组必须严格递增，当前数最小只能是前一个数的 **下一个整数**。  
- `diff == 0`：表示我们不需要减任何数，直接使用原始值。  
- `diff in primes`：如果差是素数，说明只需要一次操作（减去这个素数）就能得到 `need`。  
- `while need <= x`：在 `[need, x]` 区间里逐个尝试，最多尝试 `x - need + 1 ≤ 1000` 次，时间可接受。  

#### 复杂度

- **时间复杂度**：`O(n * M)`，其中 `M = max(nums) ≤ 1000`。  
  - **含义**：即使最坏情况下每个元素都要遍历 1000 次（极端情况），对于 `n ≤ 1000`，总操作不超过 `10⁶`，在毫秒级即可完成。  
  - 与暴力解的指数级 `O(168ⁿ)` 相比，**线性**的增长让程序在所有合法输入下都能快速返回。
- **空间复杂度**：`O(M)` 用于存放素数集合（最多 1000 个布尔值），即常数级别的额外空间。

---

## 心得

- **核心技巧**：**一次素数减法的可行性判定 + 贪心取最小合法值**。  
- **适用题型**：  
  1. 只能进行“单次”或“有限次”特殊操作的数组/序列问题（如“只能加/减一次奇数”“只能翻转一次子数组”）。  
  2. 需要在每一步保持严格递增/递减，同时操作受限的数论题目（如“只能加/减一个质数”）。  
  3. 需要在每个位置做“是否保留原值或做一次固定代价改变”的决策问题。  
- **解题钥匙**：**把每一步的“最小合法取值”当成贪心目标，只要能满足一次操作的条件就立即选它**。

---

## 反思

- **第一反应**：看到“减去素数”立刻想到“把每个数变成尽可能小”。于是想到枚举所有减法组合——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记**只能减一次**的限制，误以为可以任意多次相加得到任意差值。  
  - 忽略**减 1 不可能**（因为 1 不是素数），导致在 `need = prev + 1` 时直接判断失败。  
  - 没有提前把素数表算好，导致在循环里频繁判断素数，时间会超标。  
- **下次类似题目第一步**：先**明确每个元素的可选集合**（保留或一次合法变换），再**尝试贪心取最小合法值**，必要时用**预处理**（如筛素数）把判断过程降到 O(1)。