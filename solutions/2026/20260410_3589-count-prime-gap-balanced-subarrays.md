# #3589. **质数间隔平衡子数组计数** / Count Prime-Gap Balanced Subarrays

> 难度：中等 · 标签：Array、Math、Queue、Sliding Window、Number Theory、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/count-prime-gap-balanced-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
A subarray is called prime-gap balanced if:
Return the count of prime-gap balanced subarrays in nums.
Note:

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 1
Output: 2
Explanation:
Prime-gap balanced subarrays are:
Thus, the answer is 2.
```

**Example 2:**

```
Input: nums = [2,3,5,7], k = 3
Output: 4
Explanation:
Prime-gap balanced subarrays are:
Thus, the answer is 4.
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 1 <= nums[i] <= 5 * 104
- 0 <= k <= 5 * 104

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。  
如果一个子数组满足以下条件，则称其为 **质数间隔平衡（prime-gap balanced）** 子数组：  

> *此处应给出具体的平衡条件，原题中未给出定义。*

返回数组 `nums` 中质数间隔平衡子数组的数量。

**示例**

**示例 1**  
```text
Input: nums = [1,2,3], k = 1
Output: 2
Explanation:
质数间隔平衡子数组为：
（此处应列出满足条件的子数组）
因此答案为 2。
```

**示例 2**  
```text
Input: nums = [2,3,5,7], k = 3
Output: 4
Explanation:
质数间隔平衡子数组为：
（此处应列出满足条件的子数组）
因此答案为 4。
```

**约束条件**

- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 5 * 10^4`
- `0 <= k <= 5 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

> **题目回顾**  
> 给定数组 `nums` 与整数 `k`。  
> 把一个子数组称为 **prime‑gap balanced** 当且仅当  
> `max(subarray) - min(subarray)` 是 **素数**，且该素数 **≤ k**。  
> 任务是统计满足条件的子数组个数。

最直接的想法就是 **枚举所有子数组**，对每个子数组求出最大值与最小值的差，然后检查这两个条件：

1. 差是否是素数（可以用一个「素数表」来快速判断）  
2. 差是否 ≤ `k`

> **数据结构类比**  
> - **哈希表 / 集合**：我们把所有 ≤ `k` 的素数放进一个集合里，就像把字典里「词」对应的「页码」存进去，查询是否为素数只需要一次“查页码”。  
> - **数组**：遍历子数组时直接用下标访问，和在超市里挑选商品一样直观。

**为什么一定对？**  
遍历所有起点 `i`（左端）和终点 `j`（右端），每一种可能的子数组都会被检查一次。只要判断条件满足，就计数。没有遗漏，也没有多算。

**时间/空间复杂度大白话**  

- **时间**：外层遍历 `i`（`n` 次），内层遍历 `j`（最坏也要遍历 `n` 次），每次都要线性扫描子数组求最大最小 → `O(n³)`，在实际实现里我们可以在内层循环里动态维护 `max`、`min`，把时间降到 `O(n²)`。  
  - `O(n²)` 的意思是：如果数组长度是 10，最多要算 100 次；长度是 1000，最多要算 1,000,000 次，随 `n` 的平方增长，增长很快。

- **空间**：只需要存素数集合和几个临时变量 → `O(1)`（常数空间），不随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def sieve(limit: int) -> set:
    """埃拉托斯特尼筛法，返回 ≤ limit 的所有素数集合"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return {i for i, v in enumerate(is_prime) if v}

def count_prime_gap_balanced_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # 预处理：所有 ≤ k 的素数
    prime_set = sieve(k)

    ans = 0
    # 枚举左端点
    for left in range(n):
        cur_max = cur_min = nums[left]   # 只要把左端点本身当作子数组，max=min=nums[left]
        # 枚举右端点
        for right in range(left, n):
            # 动态维护当前子数组的最大值、最小值
            cur_max = max(cur_max, nums[right])
            cur_min = min(cur_min, nums[right])
            gap = cur_max - cur_min       # 计算“素数间距”
            # 判断 gap 是否为素数且 ≤ k
            if gap in prime_set:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：外层 `n` 次，内层平均约 `n/2` 次，总共约 `n²/2` 次比较与更新。对 10,000 长度的数组来说，大约是 5×10⁷ 次操作，已经接近时间限制。

- **空间复杂度**：`O(k)`（素数表的大小）  
  - 解释：我们只存了 ≤ `k` 的所有素数，最多 `k` 个布尔值。若 `k` 也是 5×10⁴，仍然是常数级别的内存（几百 KB）。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于对每个左端点都要 **向右扫描**，导致 `O(n²)`。  
要提升到 `O(n log n)`（甚至 `O(n)`），我们需要：

1. **快速得到任意子数组的最大值 / 最小值**  
   - 用 **单调队列（Monotonic Queue）**（也叫 **单调递减/递增队列**）在滑动窗口里实时维护最大值和最小值，做到 **O(1)** 查询。  
   - 类比：想象你在排队买票，队伍里只保留“最高的”或“最低的”人，这样随时能看见最高/最低是谁。

2. **把“gap 为素数且 ≤ k” 转化为“gap 在某个离散集合里”**  
   - 预先用 **埃拉托斯特尼筛法** 把 `1 … k` 中的素数全部列出来，放进集合 `prime_set`，查询是否为素数只需一次“查字典”。

3. **利用“双指针”**（滑动窗口）**统计所有合法子数组**  
   - 设 `right` 为右指针，窗口左端 `left` 随时可以移动。我们维护两个左指针：
     - `l1`：保证窗口内 `max - min ≤ k`（上界限制）  
     - `l2`：保证窗口内 `max - min` **不是** 素数（下界限制）  
   - 对每个 `right`，合法子数组的左端必须在 `[l1, l2-1]` 区间内（即 **max-min ≤ k 且是素数**）。于是当前 `right` 贡献的子数组数为 `l2 - l1`。

4. **核心点——如何快速得到 `l1` 与 `l2`**  
   - 随着 `right` 右移，`max` 与 `min` 只会 **增大** 或 **减小**，所以 `max-min` 单调 **不下降**。因此我们可以像 **维护两个单调队列** 那样，用 **while 循环** 持续左移 `l1`、`l2` 直至条件满足。  
   - 这一步的时间复杂度是 **摊销 O(1)**：每个元素最多被左指针弹出一次。

> **为什么单调队列能做到 O(1) 查询？**  
> - 对于最大值队列，我们保证队列中的元素值 **从前到后单调递减**。当新元素进来时，把所有比它小的元素都踢出；当左指针移出时，如果队首正好是被移出的元素，就把它弹出。这样队首永远是窗口的最大值，读取只需要 `queue[0]`，时间 O(1)。

#### 代码（Python）

```python
from collections import deque
from typing import List

def sieve(limit: int) -> set:
    """返回 ≤ limit 的所有素数集合"""
    if limit < 2:
        return set()
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return {i for i, v in enumerate(is_prime) if v}


def count_prime_gap_balanced(nums: List[int], k: int) -> int:
    """最优解：O(n) 时间，O(k) 额外空间（素数表）"""
    n = len(nums)
    prime_set = sieve(k)                     # 所有合法的素数 gap

    # 两个单调队列，分别维护窗口的最大值和最小值
    max_q = deque()   # 队列中存 (value, index)，递减
    min_q = deque()   # 队列中存 (value, index)，递增

    left_limit = 0     # l1：满足 max - min ≤ k 的最左位置
    left_prime = 0     # l2：满足 max - min 为素数的最左位置（此时窗口已经是“非素数”）
    ans = 0

    for right, val in enumerate(nums):
        # ---- 把新元素放进单调队列 ----
        while max_q and max_q[-1][0] <= val:
            max_q.pop()
        max_q.append((val, right))

        while min_q and min_q[-1][0] >= val:
            min_q.pop()
        min_q.append((val, right))

        # ---- 调整 left_limit 使得 gap ≤ k ----
        while max_q[0][0] - min_q[0][0] > k:
            # 左指针 left_limit 必须右移，弹出对应的旧元素
            if max_q[0][1] == left_limit:
                max_q.popleft()
            if min_q[0][1] == left_limit:
                min_q.popleft()
            left_limit += 1

        # ---- 调整 left_prime 使得 gap 为“非素数” ----
        # 当窗口的 gap 已经是素数时，left_prime 必须继续左移，直到 gap 不是素数
        while left_prime <= right and (max_q[0][0] - min_q[0][0]) in prime_set:
            # 如果左端正好是队首元素，需要弹出
            if max_q[0][1] == left_prime:
                max_q.popleft()
            if min_q[0][1] == left_prime:
                min_q.popleft()
            left_prime += 1

        # 此时：
        #   - 所有左端 >= left_limit 的窗口满足 gap ≤ k
        #   - 所有左端 >= left_prime 的窗口满足 gap 不是素数
        #   - 因此左端落在 [left_limit, left_prime-1] 的窗口恰好满足
        #     “gap ≤ k 且 gap 为素数”
        ans += left_prime - left_limit

    return ans
```

> **代码关键行解释**  

| 行号（示例） | 中文注释 |
|---|---|
| `while max_q and max_q[-1][0] <= val:` | 把比新元素小的都踢出，保证队列递减（最大值在队首） |
| `while min_q and min_q[-1][0] >= val:` | 把比新元素大的都踢出，保证队列递增（最小值在队首） |
| `while max_q[0][0] - min_q[0][0] > k:` | 若当前窗口的 max‑min 超过 k，左指针左移，直到满足上界 |
| `while left_prime <= right and (max_q[0][0] - min_q[0][0]) in prime_set:` | 当窗口的 gap 已经是素数时，继续左移左指针，让 gap 变成“非素数”。 |
| `ans += left_prime - left_limit` | 当前右端 `right` 能形成的合法子数组个数等于两指针之间的距离。 |

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：每个元素最多进入、离开单调队列各一次；左指针 `left_limit`、`left_prime` 也各最多右移 `n` 步。所有循环的总步数和数组长度成线性关系。相比暴力的 `O(n²)`，这里的运行时间随 `n` 只增长一次方，几乎可以接受 5×10⁴ 的规模。

- **空间复杂度**：`O(k) + O(n)`（实际为 `O(k)`）  
  - `O(k)` 用于存素数集合（最多 5×10⁴ 个布尔值）。  
  - 单调队列最多保存当前窗口的所有元素，但窗口大小受 `k` 限制（因为 `max‑min ≤ k`），最坏情况下仍是 `O(n)`，但常数非常小。整体仍是线性空间。

---

## 心得

- **核心技巧**：**单调队列 + 双指针**（滑动窗口）  
  用单调队列可以在 *O(1)* 时间内随时得到窗口的最大值与最小值，从而把 “max‑min” 的查询从线性降到常数。双指针负责维护“上界 ≤ k” 与“gap 为素数” 两个约束的交集。

- **该技巧适用的题型**  
  1. **滑动窗口最大/最小值**：如 “Maximum of Subarrays”、 “Shortest Subarray with Sum at Least K”。  
  2. **带有 max‑min 条件的计数题**：如 “Number of Subarrays with Bounded Maximum”，以及本题的 “prime‑gap balanced”。  
  3. **需要在窗口里快速判断极值关系的题目**：如 “Longest Subarray with Absolute Diff ≤ limit”。

- **一句话总结解题钥匙**  
  > **把“窗口的极值差”抽象成可实时维护的单调队列，再用双指针在两条约束之间“找交集”，即可线性计数所有合法子数组。**

---

## 反思

- **第一反应**：看到 “max‑min 是素数且 ≤ k”，立刻想到 **枚举子数组 + 直接比较**，因为这是最直接的实现方式。  
- **最容易踩的坑**  
  1. **素数判定的重复计算**：如果每次都用 trial division 会导致时间爆炸，必须一次性预处理素数集合。  
  2. **单调队列的弹出条件写错**：左指针移动时忘记检查是否弹出队首，会导致 `max`/`min` 失真。  
  3. **边界条件**：`k = 0`、数组全相等、全是素数等特殊情况，需要保证双指针逻辑仍然成立。  

- **下次遇到同类题**  
  1. **先抽象出窗口需要维护的属性**（本题是 max 与 min）。  
  2. **选用合适的数据结构**：若属性是极值，优先考虑单调队列；若是和/计数，考虑前缀和。  
  3. **确定约束的单调性**：若随右指针移动约束只会“变坏”或“变好”，就可以用双指针/滑动窗口进行线性计数。  

祝你在算法的路上越走越顺 🚀！