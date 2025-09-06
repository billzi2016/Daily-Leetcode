# #3334. 求数组的最大因子分数 / Find the Maximum Factor Score of Array

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-factor-score-of-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
The factor score of an array is defined as the product of the LCM and GCD of all elements of that array.
Return the maximum factor score of nums after removing at most one element from it.
Note that both the LCM and GCD of a single number are the number itself, and the factor score of an empty array is 0.

**Examples**

**Example 1:**

```
Input: nums = [2,4,8,16]
Output: 64
Explanation:
On removing 2, the GCD of the rest of the elements is 4 while the LCM is 16, which gives a maximum factor score of 4 * 16 = 64 .
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: 60
Explanation:
The maximum factor score of 60 can be obtained without removing any elements.
```

**Example 3:**

```
Input: nums = [3]
Output: 9
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 30

---

## 题目（中文翻译）

你得到一个整数数组 `nums`。  
数组的因子分数定义为该数组所有元素的最小公倍数（LCM）与最大公约数（GCD）的乘积。  
返回在最多删除一个元素后，`nums` 能得到的最大因子分数。  

注意：
- 单个数字的 LCM 与 GCD 都是该数字本身；
- 空数组的因子分数为 0。

**示例 1**  
Input: `nums = [2,4,8,16]`  
Output: `64`  
Explanation:  
删除 `2` 后，其余元素的 GCD 为 `4`，LCM 为 `16`，因子分数为 `4 * 16 = 64`，为最大值。

**示例 2**  
Input: `nums = [1,2,3,4,5]`  
Output: `60`  
Explanation:  
不删除任何元素即可得到最大因子分数 `60`。

**示例 3**  
Input: `nums = [3]`  
Output: `9`  
Explanation:  
数组仅有一个元素 `3`，其 GCD 与 LCM 均为 `3`，因子分数为 `3 * 3 = 9`。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 30`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「枚举」我们到底要不要删掉哪个元素，然后把剩下的数全部算出 **GCD**（最大公约数） 和 **LCM**（最小公倍数），把两者相乘得到 **factor score**，取最大的即可。

- **枚举**：把数组的每一个位置都当成「可能被删掉的」元素，同时也别忘了「什么都不删」的情况。  
- **求 GCD**：把所有剩余数字两两取 `gcd`，类似把一堆绳子一起拉，最短的那根长度就是最大公约数。Python 的 `math.gcd` 就像查字典一样，`key` 是两个数，`value` 是它们的最大公约数。  
- **求 LCM**：先算两数的 GCD，再用公式 `lcm(a,b) = a // gcd(a,b) * b`。这相当于先把两根绳子「对齐」在它们的公共长度上，再把它们「拼接」成一根最短能同时容纳两根绳子的长绳。  

因为数组长度最多只有 100，枚举每一种删除方式（最多 `n+1` 种）并对每种方式遍历一次数组求 GCD、LCM，时间复杂度大约是 `O(n²)`，在本题的约束下完全可以接受。

**为什么一定对？**  
枚举覆盖了所有合法的「删掉至多一个元素」的情形，求得的 GCD、LCM 正是题目定义的那两个值，乘积自然就是对应的 factor score。遍历完所有情况后取最大，就是答案。

#### 代码（Python）

```python
import math
from typing import List

def lcm(a: int, b: int) -> int:
    """返回 a 与 b 的最小公倍数。"""
    return a // math.gcd(a, b) * b

def max_factor_score_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # 先算「不删」的情况
    best = 0

    # 枚举要删除的下标 i，i == n 表示「不删除任何元素」
    for i in range(n + 1):
        cur_gcd = None   # 当前子数组的 GCD
        cur_lcm = None   # 当前子数组的 LCM

        for j in range(n):
            if j == i:               # 跳过被删除的元素
                continue
            if cur_gcd is None:      # 第一个保留下来的数，直接初始化
                cur_gcd = nums[j]
                cur_lcm = nums[j]
            else:
                cur_gcd = math.gcd(cur_gcd, nums[j])
                cur_lcm = lcm(cur_lcm, nums[j])

        # 处理空数组的特殊情况（只能在 n==1 且删除唯一元素时出现）
        if cur_gcd is None:          # 没有留下任何元素
            score = 0
        else:
            score = cur_gcd * cur_lcm
        best = max(best, score)

    return best

# 示例测试
print(max_factor_score_bruteforce([2, 4, 8, 16]))   # 64
print(max_factor_score_bruteforce([1, 2, 3, 4, 5]))# 60
print(max_factor_score_bruteforce([3]))           # 9
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  *为什么叫 O(n²)？* 想象有 `n` 行 `n` 列的格子，每个格子都要访问一次，总共访问 `n × n` 次，数量级就是「n 的平方」。
- **空间复杂度**：`O(1)`（不计输出变量）  
  只用了常数个额外变量（`cur_gcd、cur_lcm、best`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于：**每次删除一个元素时，都要重新遍历整条数组来求 GCD 和 LCM**，这一步是 `O(n)`，而我们要做 `n+1` 次，导致 `O(n²)`。

我们可以把「遍历一次求全部」的过程提前，保存下来，后面只需要 **常数时间** 就能得到「删掉第 i 个元素后」的 GCD 与 LCM。  

**关键技巧：前缀‑后缀数组**  

- **前缀 GCD / LCM**：`pre_gcd[i]` 表示 `nums[0..i]`（左边到 i）的 GCD；`pre_lcm[i]` 表示同区间的 LCM。  
- **后缀 GCD / LCM**：`suf_gcd[i]` 表示 `nums[i..n-1]`（从 i 到右边）的 GCD；`suf_lcm[i]` 表示同区间的 LCM。  

这样，对于「删掉第 i 个元素」的剩余数组，它其实是「左侧区间」`[0, i-1]` 与「右侧区间」`[i+1, n-1]` 的并集。  
- **剩余 GCD** = `gcd(pre_gcd[i-1], suf_gcd[i+1])`  
- **剩余 LCM** = `lcm(pre_lcm[i-1], suf_lcm[i+1])`  

边界情况（i 为 0 或 n‑1）只需要取对应的前缀或后缀即可。  
再把「不删」的情况（直接使用 `pre_gcd[n-1]` 与 `pre_lcm[n-1]`）一起考虑，遍历一次 `i`，每次只做 O(1) 的计算，整体时间降到 `O(n)`。

**为什么前缀/后缀能做到 O(1) 合并？**  
- GCD 的合并公式：`gcd(a, b)` 只需要把两数直接带入 `math.gcd`，不依赖于它们内部的元素。  
- LCM 的合并公式同理：`lcm(a, b) = a // gcd(a, b) * b`，只要知道两段的 LCM 与 GCD，就能算出整体 LCM。  

因为我们已经在预处理阶段把每段的 GCD 与 LCM 存下来，后面合并时只需要「查表」加一次 `gcd`/`lcm`，时间就是常数。

#### 代码（Python）

```python
import math
from typing import List

def lcm(a: int, b: int) -> int:
    """返回 a 与 b 的最小公倍数。"""
    return a // math.gcd(a, b) * b

def max_factor_score_opt(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0

    # ---------- 前缀 ----------
    pre_gcd = [0] * n
    pre_lcm = [0] * n
    cur_g = nums[0]
    cur_l = nums[0]
    pre_gcd[0] = cur_g
    pre_lcm[0] = cur_l
    for i in range(1, n):
        cur_g = math.gcd(cur_g, nums[i])
        cur_l = lcm(cur_l, nums[i])
        pre_gcd[i] = cur_g
        pre_lcm[i] = cur_l

    # ---------- 后缀 ----------
    suf_gcd = [0] * n
    suf_lcm = [0] * n
    cur_g = nums[-1]
    cur_l = nums[-1]
    suf_gcd[-1] = cur_g
    suf_lcm[-1] = cur_l
    for i in range(n - 2, -1, -1):
        cur_g = math.gcd(cur_g, nums[i])
        cur_l = lcm(cur_l, nums[i])
        suf_gcd[i] = cur_g
        suf_lcm[i] = cur_l

    # ---------- 计算答案 ----------
    best = 0

    # 1) 不删除任何元素
    best = max(best, pre_gcd[-1] * pre_lcm[-1])

    # 2) 删除第 i 个元素（0 <= i < n）
    for i in range(n):
        # 左侧区间是否存在
        if i == 0:
            left_gcd = None
            left_lcm = None
        else:
            left_gcd = pre_gcd[i - 1]
            left_lcm = pre_lcm[i - 1]

        # 右侧区间是否存在
        if i == n - 1:
            right_gcd = None
            right_lcm = None
        else:
            right_gcd = suf_gcd[i + 1]
            right_lcm = suf_lcm[i + 1]

        # 合并 GCD
        if left_gcd is None:
            cur_gcd = right_gcd
        elif right_gcd is None:
            cur_gcd = left_gcd
        else:
            cur_gcd = math.gcd(left_gcd, right_gcd)

        # 合并 LCM
        if left_lcm is None:
            cur_lcm = right_lcm
        elif right_lcm is None:
            cur_lcm = left_lcm
        else:
            cur_lcm = lcm(left_lcm, right_lcm)

        # 处理空数组（只能在 n==1 且删除唯一元素时出现）
        if cur_gcd is None:
            score = 0
        else:
            score = cur_gcd * cur_lcm
        best = max(best, score)

    return best

# 示例测试
print(max_factor_score_opt([2, 4, 8, 16]))   # 64
print(max_factor_score_opt([1, 2, 3, 4, 5]))# 60
print(max_factor_score_opt([3]))           # 9
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历三遍数组（一次前缀、一次后缀、一次枚举），每一步都是「常数时间」的计算。相较于暴力的「每次都要再遍历一次」的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(n)`  
  需要四个长度为 `n` 的辅助数组来存前缀/后缀的 GCD 与 LCM。若只在意空间，还可以把 LCM 用同一个数组滚动存，但在本题规模下 `O(n)` 完全可以接受。

---

## 心得  

- **核心技巧**：前缀/后缀数组的「区间合并”。**  
- **适用场景**：  
  1. “删除至多一个元素后求某种区间属性”——如「最大子数组和」的前后缀最大/最小和。  
  2. “固定分割点求左右区间的 GCD/LCM/最小值/最大值”等。  
  3. “数组中插入或删除一次后仍要快速查询整体属性”的题目。  
- **一句话总结**：把「整条数组的属性」拆成「左半段」+「右半段」的组合，预先算好每段的属性，删掉一个元素后只需要 O(1) 合并。

---

## 反思  

- **第一反应**：直接写两层循环枚举删除位置，逐个算 GCD、LCM。虽然能跑通，但会觉得不够「优雅」。
- **最容易踩的坑**：  
  - 处理 **空数组** 的情况（全部元素被删除时 factor score 为 0）。  
  - LCM 计算时可能出现 **整数溢出**（在其他语言需要注意），在 Python 中整数任意大但仍要防止除零错误。  
  - 前缀/后缀合并时要记得 **边界**（删除第一个或最后一个元素时，只剩单侧区间）。  
- **下次遇到同类题**：第一步先问自己「如果不删除任何元素，整个数组的属性怎么快速算？」然后思考「把数组切成左/右两段，分别算属性，删掉中间一个元素后如何把两段的结果合并」。这样就能立刻想到前缀‑后缀的套路。