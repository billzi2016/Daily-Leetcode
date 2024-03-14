# #2614. **Prime In Diagonal** / Prime In Diagonal

> 难度：简单 · 标签：Array、Math、Matrix、Number Theory · [LeetCode 链接](https://leetcode.com/problems/prime-in-diagonal/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed two-dimensional integer array nums.
Return the largest prime number that lies on at least one of the diagonals of nums. In case, no prime is present on any of the diagonals, return 0.
Note that:
In the above diagram, one diagonal is [1,5,9] and another diagonal is [3,5,7].

**Examples**

**Example 1:**

```
Input: nums = [[1,2,3],[5,6,7],[9,10,11]]
Output: 11
Explanation: The numbers 1, 3, 6, 9, and 11 are the only numbers present on at least one of the diagonals. Since 11 is the largest prime, we return 11.
```

**Example 2:**

```
Input: nums = [[1,2,3],[5,17,7],[9,11,10]]
Output: 17
Explanation: The numbers 1, 3, 9, 10, and 17 are all present on at least one of the diagonals. 17 is the largest prime, so we return 17.
```

**Constraints**

- 1 <= nums.length <= 300
- nums.length == numsi.length
- 1 <= nums[i][j] <= 4*106

---

## 题目（中文翻译）

给定一个下标从 0 开始的二维整数数组 `nums`（two-dimensional integer array）。  
返回位于 `nums` 至少一条对角线（diagonal）上的最大素数（prime）。如果所有对角线上都不存在素数，返回 `0`。

**注意**  
- 对角线指的是从左上到右下的主对角线以及从右上到左下的次对角线。例如图中对角线 `[1,5,9]` 与 `[3,5,7]`。

### 示例

**示例 1**  
> **输入** `nums = [[1,2,3],[5,6,7],[9,10,11]]`  
> **输出** `11`  
> **解释** 位于任意对角线上的数字只有 `1, 3, 6, 9, 11`。其中 `11` 是最大的素数，故返回 `11`。

**示例 2**  
> **输入** `nums = [[1,2,3],[5,17,7],[9,11,10]]`  
> **输出** `17`  
> **解释** 对角线上出现的数字有 `1, 3, 9, 10, 17`。`17` 为最大的素数，返回 `17`。

### 约束条件

- `1 <= nums.length <= 300`
- `nums.length == nums[i].length`（矩阵为方阵）
- `1 <= nums[i][j] <= 4 * 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把对角线上的所有元素都找出来**，然后逐个判断它们是不是素数，最后取最大的素数返回。  

- **哪些元素属于对角线**  
  - 主对角线：下标满足 `i == j`（左上 → 右下）。  
  - 副对角线：下标满足 `i + j == n - 1`（右上 → 左下）。  
  两条对角线会在中心位置相交，中心元素会出现两次，但我们只需要统计一次即可。  

- **素数怎么判断**  
  素数的定义是：只能被 1 和它本身整除的自然数（>1）。  
  判断一个数 `x` 是否为素数，只需要尝试除以 `2 … √x`（即 `x` 的平方根）即可——如果都不能整除，说明 `x` 是素数。  
  这里的 **“查字典”** 类比是：我们在字典里找词的页码，`√x` 就像是我们只需要翻到字典的前半页就能确定是否有对应的词。

- **为什么正确**  
  我们遍历了**所有**在任意一条对角线上出现的元素，并对每个元素做了完整的素数判定。只要在这些元素中存在素数，最大素数一定会被找到。

#### 代码（Python）

```python
import math
from typing import List

def is_prime(x: int) -> bool:
    """判断 x 是否为素数，时间复杂度约 O(√x)"""
    if x < 2:                     # 0、1 不是素数
        return False
    if x == 2:                    # 2 是唯一的偶数素数
        return True
    if x % 2 == 0:                # 其余偶数直接判为非素数
        return False
    # 只需要检查奇数因子，范围到 √x
    limit = int(math.isqrt(x))    # math.isqrt 返回整数的平方根
    for d in range(3, limit + 1, 2):
        if x % d == 0:
            return False
    return True


def prime_in_diagonal(nums: List[List[int]]) -> int:
    n = len(nums)                 # 矩阵是 n×n
    max_prime = 0                 # 用来保存目前找到的最大素数

    for i in range(n):
        # 主对角线元素 (i, i)
        val = nums[i][i]
        if is_prime(val):
            max_prime = max(max_prime, val)

        # 副对角线元素 (i, n-1-i)
        # 注意：当 n 为奇数且 i 正好是中心位置时，这两个位置相同，避免重复判断
        j = n - 1 - i
        if i != j:                # 防止中心元素重复检查
            val = nums[i][j]
            if is_prime(val):
                max_prime = max(max_prime, val)

    return max_prime               # 若没有素数，仍然是初始值 0
```

#### 复杂度  

- **时间复杂度**：`O(n * √M)`  
  - `n` 是矩阵的行数（对角线上最多 `2n-1` 个元素），每个元素的素数判定最坏需要遍历到它的平方根 `√M`（`M` 为矩阵中元素的最大值，题目给的上限是 `4·10⁶`）。  
  - 用大白话说，就是“我们要检查大约 `2n` 次，每次最多要除到 `√M` 次”。  

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量 (`max_prime、i、j、val` 等)，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次判断素数都要做 `√x` 次除法，虽然对 `n ≤ 300` 影响不大，但如果矩阵更大或要多次查询，这一步会成为性能热点。  

我们可以把**所有可能的素数**一次性预先算好，这样判断一个数是否为素数的时间就可以降到 **O(1)**。  
常用的预处理方法是 **埃拉托斯特尼筛法（Sieve of Eratosthenes）**：

1. **构造筛子**  
   - 创建长度为 `max_val + 1`（`max_val` 为矩阵中出现的最大数）的布尔数组 `is_prime`，初始全部设为 `True`，表示“假设都是素数”。  
   - 从 `2` 开始遍历，如果 `is_prime[p]` 为真，则 `p` 是素数，随后把 `p` 的所有倍数（`p*p, p*p+p, …`）标记为 `False`（不是素数）。  

2. **遍历对角线**  
   - 与暴力解相同，遍历主、辅对角线的元素。  
   - 直接通过 `is_prime[value]` 判断是否为素数，若是则更新最大素数。  

**为什么这样更快**  
- 筛法的时间复杂度是 `O(max_val log log max_val)`，只和矩阵中最大数的大小有关，和矩阵的维度无关。  
- 完成筛子后，每次素数查询只需要一次数组下标访问，时间几乎是常数（`O(1)`），所以遍历对角线的整体时间变为 `O(n)`。

#### 代码（Python）

```python
from typing import List

def sieve(limit: int) -> List[bool]:
    """返回长度为 limit+1 的布尔数组，True 表示对应下标是素数"""
    if limit < 2:
        return [False] * (limit + 1)

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False  # 0、1 不是素数

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            # 把 p 的所有倍数标记为非素数，从 p*p 开始可以省掉很多重复标记
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1
    return is_prime


def prime_in_diagonal_opt(nums: List[List[int]]) -> int:
    n = len(nums)

    # 1️⃣ 找出矩阵中出现的最大值，决定筛子的上界
    max_val = max(max(row) for row in nums)

    # 2️⃣ 预处理所有素数
    prime_table = sieve(max_val)

    max_prime = 0
    for i in range(n):
        # 主对角线
        val = nums[i][i]
        if prime_table[val]:
            max_prime = max(max_prime, val)

        # 副对角线
        j = n - 1 - i
        if i != j:                     # 防止中心元素重复
            val = nums[i][j]
            if prime_table[val]:
                max_prime = max(max_prime, val)

    return max_prime
```

#### 复杂度  

- **时间复杂度**：`O(max_val log log max_val + n)`  
  - `max_val ≤ 4·10⁶`，筛法的时间大约是 `4·10⁶ * log log 4·10⁶`，在实际运行中非常快（几毫秒级）。  
  - 再加上遍历对角线的 `O(n)`，整体仍然是线性级别。相比暴力解的 `O(n·√M)`，这里的 `√M`（约 2000）被消除了，速度提升显著。  

- **空间复杂度**：`O(max_val)`  
  - 需要额外的布尔数组保存所有数的素数信息，大小与最大元素值成正比（约 4 MB），在本题限制下完全可以接受。  

---

## 心得

- **核心技巧**：**埃拉托斯特尼筛法** 用一次预处理把“是否为素数”的查询从 `O(√x)` 降到 `O(1)`。  
- **适用的题型**  
  1. **大量重复的素数判断**（例如判断数组中所有元素是否为素数、统计区间素数个数）。  
  2. **需要在固定范围内快速判断质数**（如“质数矩阵”或“质数路径”类题）。  
  3. **求最大/最小素数**（本题）或 **统计素数出现次数**。  
- **一句话总结**：*把所有可能的答案一次算好，查询时直接“看表”就行了。*

---

## 反思

- **第一反应**：看到“对角线”和“最大素数”，马上想到遍历对角线、逐个判断素数。  
- **最容易踩的坑**  
  - **中心元素重复计数**：当矩阵尺寸为奇数时，主、副对角线会在中心相交，需要手动去重。  
  - **素数判定的边界**：0、1 不是素数，2 是唯一的偶数素数，忘记这些会导致错误答案。  
  - **最大值的上界**：如果直接使用 `√x` 判断，可能会因 `x` 很大而超时；提前获取矩阵最大值用于筛子上界是关键。  
- **下次类似题的第一步**：先**确定需要检查的元素集合**（是整行、整列、对角线还是子矩阵），然后**评估是否会出现大量重复的判定**——如果是，就考虑一次性预处理（如筛法、前缀和、哈希表等）再进行查询。