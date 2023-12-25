# #2523. 区间内最近的素数对 / Closest Prime Numbers in Range

> 难度：中等 · 标签：Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/closest-prime-numbers-in-range/)

---

## 题目（英文原版）

**Description**

Given two positive integers left and right, find the two integers num1 and num2 such that:
Return the positive integer array ans = [num1, num2]. If there are multiple pairs satisfying these conditions, return the one with the smallest num1 value. If no such numbers exist, return [-1, -1].

**Examples**

**Example 1:**

```
Input: left = 10, right = 19
Output: [11,13]
Explanation: The prime numbers between 10 and 19 are 11, 13, 17, and 19.
The closest gap between any pair is 2, which can be achieved by [11,13] or [17,19].
Since 11 is smaller than 17, we return the first pair.
```

**Example 2:**

```
Input: left = 4, right = 6
Output: [-1,-1]
Explanation: There exists only one prime number in the given range, so the conditions cannot be satisfied.
```

**Constraints**

- 1 <= left <= right <= 106

---

## 题目（中文翻译）

**题目描述**  
给定两个正整数 `left` 和 `right`，在区间 `[left, right]`（两端点均包含）中找到一对整数 `num1` 和 `num2`，满足：

- `num1` 与 `num2` 均为素数（prime）；
- `num1 < num2`；
- `num2 - num1` 为所有满足条件的素数对中最小的差值。

返回正整数数组 `ans = [num1, num2]`。如果存在多对满足上述条件的素数对，返回 `num1` 最小的那一对。如果区间内不存在满足条件的两素数对，返回 `[-1, -1]`。

**示例 1**  
```
Input: left = 10, right = 19
Output: [11,13]
Explanation: 区间 [10,19] 内的素数为 11、13、17、19。任意相邻素数的差值最小为 2，可由 [11,13] 或 [17,19] 达成。由于 11 < 17，返回前者。
```

**示例 2**  
```
Input: left = 4, right = 6
Output: [-1,-1]
Explanation: 区间内仅有唯一的素数 5，无法形成满足条件的素数对。
```

**约束条件**  
- `1 <= left <= right <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **把区间 `[left, right]` 里的每个数都检查一遍，判断它是不是素数**。  
   - 判断素数最常用的办法是“试除法”：把 `n` 除以 `2,3,4,…,√n`，只要有一个能整除，就说明 `n` 不是素数。  
   - 这一步可以把 **素数看成“合格的学生”，我们要给每个学生逐一检查成绩**，虽然慢但最容易想到。

2. **把所有找到的素数放进一个列表**（比如 `primes = [11,13,17,19]`）。

3. **遍历这个列表的所有两两组合，计算它们的差值**，找出差值最小的那一对。  
   - 这里的组合就像“让每两个学生两两比身高”，找出身高差最小的一对。

4. **如果有多对差值相同，返回 `num1` 最小的那一对**（因为我们是从左到右遍历，先出现的就是 `num1` 最小的）。

**为什么这个方法一定能得到答案？**  
因为我们把区间里所有的素数都列举出来了，随后检查每一种可能的配对，必然不会漏掉最优的那一对。

**时间/空间分析（用大白话解释 O 记号）**  

- **时间复杂度**  
  - 判断一个数 `n` 是否为素数，需要最多除到 `√n`，所以每个数的检查时间大约是 `√n`。  
  - 区间长度记作 `m = right - left + 1`（最多 `10⁶`），所以总的检查时间约为 `m * √right`。  
  - 再加上遍历所有素数配对的时间，最坏情况下素数数目接近 `m`，配对数是 `m²/2`，这会让时间爆炸。  
  - 综合来看，**时间复杂度是 O(m·√right + m²)**，在最坏情况下会非常慢（几秒甚至几分钟）。

- **空间复杂度**  
  - 只需要一个列表存素数，最多 `m` 个整数，**空间是 O(m)**。  

> **大白话**：如果把 `O(m·√right)` 想成“一辆车每分钟只能检查 √right 辆车”，而 `m²` 就像“把所有车都两两比一遍”，显然会非常慢。

#### 代码（Python）

```python
import math
from typing import List

def is_prime(n: int) -> bool:
    """试除法判断 n 是否为素数。"""
    if n < 2:
        return False
    # 只需要除到 sqrt(n) 即可
    limit = int(math.isqrt(n))
    for d in range(2, limit + 1):
        if n % d == 0:          # 能被整除说明不是素数
            return False
    return True                # 没有发现因子，说明是素数

def closest_primes_brute(left: int, right: int) -> List[int]:
    # 1️⃣ 收集区间内所有素数
    primes = []
    for num in range(left, right + 1):
        if is_prime(num):
            primes.append(num)

    # 2️⃣ 若不足两个素数，直接返回 [-1, -1]
    if len(primes) < 2:
        return [-1, -1]

    # 3️⃣ 暴力遍历所有两两配对，找最小间距
    best_pair = [-1, -1]
    best_gap = float('inf')   # 初始设为无限大，后面会被更小的间距替代

    for i in range(len(primes)):
        for j in range(i + 1, len(primes)):
            gap = primes[j] - primes[i]   # 两个素数的差值
            if gap < best_gap:            # 发现更小的间距
                best_gap = gap
                best_pair = [primes[i], primes[j]]
            # 如果间距相等，题目要求 num1 最小，而这里 i 从小到大遍历
            # 所以第一次出现的配对已经满足条件，无需额外处理

    return best_pair
```

#### 复杂度

- **时间复杂度**：`O(m·√right + m²)`  
  - `m·√right` 来自每个数的试除法，`m²` 来自两两配对的遍历。  
  - 在最坏情况下（`right = 10⁶`，`left = 1`），这几乎不可接受。

- **空间复杂度**：`O(m)`  
  - 只用了一个列表保存区间内的素数，最多存 `10⁶` 个整数（约 8 MB）。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因在于：

1. **每个数都要做 `√n` 次除法**——重复检查了很多不必要的合数。  
2. **两两配对是 `O(m²)`**——实际上只需要相邻的素数就能得到最小间距，因为如果有三位数 `a < b < c`，则 `c-a` 肯定不小于 `b-a` 或 `c-b`。

**优化方向**：

- **一次性找出所有素数**，而不是对每个数单独判断。  
  - 这里可以使用 **埃拉托斯特尼筛法（Sieve of Eratosthenes）**，它可以在 `O(N log log N)` 的时间内把 `1 … N` 的素数全部标记出来。  
  - 把筛子想象成“一把大筛子”，把所有合数一次性筛掉，只留下“合格的颗粒（素数）”。  
  - 对于本题，`N = right ≤ 10⁶`，非常容易在内存里放下。

- **只遍历相邻素数**，计算它们的差值。  
  - 想象把所有素数排成一条直线，最近的两个点一定是相邻的两个点。  
  - 因此只需要一次线性扫描，就能找到最小间距。

**完整步骤**：

1. **使用筛法生成 `is_prime[0…right]`**（布尔数组，`True` 表示是素数）。  
   - 初始化时把所有大于 `1` 的位置设为 `True`。  
   - 从 `2` 开始，若当前位置是 `True`，就把它的所有倍数标记为 `False`（合数）。  
   - 只需要遍历到 `√right`，因为更大的因子对应的另一因子已经在前面筛掉了。

2. **在 `[left, right]` 区间里把所有素数依次放进列表 `primes_in_range`**。  
   - 这一步是一次线性扫描，时间和区间长度 `m` 成正比。

3. **如果素数数量不足 2，直接返回 `[-1, -1]`**。

4. **一次遍历 `primes_in_range`，计算相邻两个素数的差值**，保存最小的差值以及对应的配对。  
   - 因为我们是从左到右遍历的，遇到相同的最小差值时，第一个配对的 `num1` 已经是最小的，直接返回即可。

**为什么这样更快？**  

- 筛法一次性把所有合数剔除，避免了对每个数都做 `√n` 次除法。  
- 只比较相邻素数，省掉了 `O(m²)` 的配对检查。  
- 整体时间是 `O(right log log right)`（筛法） + `O(m)`（收集与扫描），在 `right ≤ 10⁶` 的范围内几乎是瞬间完成。

#### 代码（Python）

```python
import math
from typing import List

def sieve(limit: int) -> List[bool]:
    """
    埃拉托斯特尼筛法，返回长度为 limit+1 的布尔数组 is_prime，
    其中 is_prime[n] 为 True 表示 n 是素数。
    """
    # 0、1 不是素数，其他先默认是素数
    is_prime = [False, False] + [True] * (limit - 1)

    # 只需要筛到 sqrt(limit)
    for p in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[p]:                     # p 本身是素数
            # 把 p 的所有倍数标记为合数，从 p*p 开始可以省去很多重复操作
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return is_prime

def closest_primes_opt(left: int, right: int) -> List[int]:
    # 1️⃣ 先把 [2, right] 区间的所有素数筛出来
    is_prime = sieve(right)

    # 2️⃣ 收集区间 [left, right] 内的素数（保持从小到大顺序）
    primes = [num for num in range(left, right + 1) if is_prime[num]]

    # 3️⃣ 若不足两个素数，返回 [-1, -1]
    if len(primes) < 2:
        return [-1, -1]

    # 4️⃣ 扫一遍相邻素数，找最小间距
    best_pair = [primes[0], primes[1]]
    best_gap = best_pair[1] - best_pair[0]

    for i in range(1, len(primes) - 1):
        gap = primes[i + 1] - primes[i]
        if gap < best_gap:                # 发现更小的间距
            best_gap = gap
            best_pair = [primes[i], primes[i + 1]]
        # 若 gap == best_gap，题目要求返回 num1 最小的配对，
        # 由于我们是从左到右遍历，第一次出现的配对已经满足该条件

    return best_pair
```

#### 复杂度

- **时间复杂度**：`O(right log log right + m)`  
  - `right log log right` 来自筛法（大约 `10⁶ * log log 10⁶`，极快）。  
  - `m = right - left + 1` 来自一次线性遍历收集素数和一次相邻比较。  
  - 与暴力解的 `O(m·√right + m²)` 相比，提升了几个数量级。

- **空间复杂度**：`O(right)`  
  - 需要一个长度为 `right+1` 的布尔数组来存“是否为素数”。  
  - 对于 `right ≤ 10⁶`，约占 1 MB（因为 Python 的 `bool` 实际是一个字节），在普通机器上完全可以接受。

---

## 心得

- **核心技巧**：**埃拉托斯特尼筛法 + 相邻比较**  
  - 筛法一次性找出所有素数，避免重复的试除。  
  - 相邻比较利用了“最近的两个素数一定是相邻的”这一数学性质。

- **适用的题型**（类似思路）  
  1. “区间内的第 K 大素数” → 先筛出所有素数，再直接索引。  
  2. “寻找两个素数之间的最大间距” → 同样先筛，然后遍历相邻素数求最大差。  
  3. “判断区间内是否存在连续的两个素数（素数对）” → 只要相邻差为 2 即可。

- **一句话总结解题钥匙**：**先把所有素数一次性列出来，再只比较相邻的两个——既省时又省力。**

---

## 反思

- **拿到题目第一反应**：直接遍历每个数，用 trial division 检查素数，然后两两比较差值。  
  - 这是一种“暴力但直观”的思路，适合快速写出可运行的代码。

- **最容易踩的坑**  
  1. **边界条件**：`left` 可能为 `1`，而 `1` 不是素数，需要在筛或判断时排除。  
  2. **只有一个素数的情况**：必须在收集完素数后检查数量，防止在后面的相邻比较中出现索引错误。  
  3. **时间超限**：若直接用 trial division，会在 `right = 10⁶` 时超时，需要换成筛法。

- **下次遇到同类题，第一步该想到**：  
  **“这是一道数论/素数的区间查询”，先考虑是否可以用筛法一次性预处理所有素数”。**  
  这样可以把“判断是否为素数”的重复工作一次性完成，后面的逻辑往往就会大幅简化。