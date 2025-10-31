# #3404. **计数特殊子序列** / Count Special Subsequences

> 难度：中等 · 标签：Array、Hash Table、Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-special-subsequences/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
A special subsequence is defined as a subsequence of length 4, represented by indices (p, q, r, s), where p < q < r < s. This subsequence must satisfy the following conditions:
Return the number of different special subsequences in nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,3,6,1]
Output: 1
Explanation:
There is one special subsequence in nums .
```

**Example 2:**

```
Input: nums = [3,4,3,4,3,4,3,4]
Output: 3
Explanation:
There are three special subsequences in nums .
```

**Constraints**

- 7 <= nums.length <= 1000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个仅包含正整数的数组 `nums`。

定义 **特殊子序列** 为长度为 4 的子序列，记为索引四元组 `(p, q, r, s)`，其中 `p < q < r < s`，并且满足以下关系：

```
nums[p] < nums[q] > nums[r] < nums[s]
```

返回数组 `nums` 中不同的特殊子序列的个数。

**示例**

**示例 1**

```
输入：nums = [1,2,3,4,3,6,1]
输出：1
解释：
唯一满足条件的特殊子序列是下标 (2,3,4,5)，对应的元素为 [3,4,3,6]，满足 3 < 4 > 3 < 6。
```

**示例 2**

```
输入：nums = [3,4,3,4,3,4,3,4]
输出：3
解释：
满足条件的特殊子序列分别是：
- (0,1,2,3) -> [3,4,3,4]
- (2,3,4,5) -> [3,4,3,4]
- (4,5,6,7) -> [3,4,3,4]
```

**约束条件**

- `7 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的四元组 `(p, q, r, s)` 都枚举一遍，然后检查它们是否满足  
```
p < q < r < s
nums[p] / nums[q] == nums[s] / nums[r]
```
把等式两边同时乘以分母，得到等价条件  

```
nums[p] * nums[r] == nums[q] * nums[s]
```

> **数据结构**：这里只需要普通的 **数组**，因为我们只是在数组上遍历。  
> **类比**：把四个下标想成四个人排成一列，只有当左边两个人的“速度比”恰好等于右边两个人的“速度比”时，这四个人才算是一组“特殊”组合。

只要遍历完所有四元组，计数器加一，就能得到答案。  

#### 代码（Python）

```python
from math import gcd
from typing import List

def count_special_subsequences_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    # 枚举四个下标 p < q < r < s
    for p in range(n):
        for q in range(p + 1, n):
            for r in range(q + 1, n):
                for s in range(r + 1, n):
                    # 检查比例是否相等：nums[p] / nums[q] == nums[s] / nums[r]
                    if nums[p] * nums[r] == nums[q] * nums[s]:
                        ans += 1
    return ans
```

> 关键行的中文注释已经写在代码里。  

#### 复杂度  

- **时间复杂度**：`O(n⁴)`  
  四层循环，每层最多遍历 `n` 次，整体就是 `n * n * n * n`。  
  “O(n⁴)” 可以想象成“如果数组有 10 000 个元素，运行时间会是 10 000⁴ ≈ 10¹⁶ 次基本操作”，显然不可接受。

- **空间复杂度**：`O(1)`  
  只用了常数级的额外变量（计数器 `ans`）。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **重复计算**：  
- 对于同一个 `q`，我们会在不同的 `r`、`s` 中一次又一次地去检查所有 `p`。  
- 对于同一个 `r`，我们会在不同的 `p、q` 中一次又一次地去检查所有 `s`。

如果能够把 **左边的配对** `(p, q)` 和 **右边的配对** `(s, r)` 分别提前统计起来，后面只需要把对应的计数相乘，就可以省掉大量的循环。

**核心想法**  
1. 把满足 `p < q < r < s` 的四元组，先把左边的两个下标 `(p, q)` 看成 **左配对**，右边的两个下标 `(s, r)` 看成 **右配对**。  
2. 对每一个 `r`（作为左配对的 “第三个” 下标），把所有已经出现的左配对 `(p, q)`（其中 `q = r‑1`）的比例 **累计** 到一个哈希表 `left_cnt` 中。  
3. 同时，对于固定的 `r`，遍历所有 `s > r`，计算右配对 `(s, r)` 的比例。如果这个比例在 `left_cnt` 中出现过，就说明找到了若干个合法的 `(p, q)` 与当前 `(s, r)` 匹配，直接把对应计数加到答案里。  

这样，每次 **向右移动 `r`** 时，只需要：
- 把新加入的左配对 `(p, r‑1)`（`p` 从 `0` 到 `r‑2`）加入哈希表，**O(r)** 次操作。
- 遍历所有 `s > r`，检查右配对，**O(n‑r)** 次操作。

把所有 `r` 累加起来，总操作次数是  

```
∑_{r=2}^{n-2} (r + (n - r))  =  O(n²)
```

因此整体时间是 `O(n²)`，空间只需要存放比例计数的哈希表，最坏情况也是 `O(n²)`（因为每一对 `(p, q)` 都可能产生不同的比例），在本题的 `n ≤ 1000` 范围内完全可以接受。

**比例的表示**  
直接使用浮点数会有精度误差。我们把比例化为最简分数 `(a, b)`，其中  

```
a = nums[x] / g , b = nums[y] / g , g = gcd(nums[x], nums[y])
```

这样 `(a, b)` 就是唯一的、可哈希的键。可以把它存成元组 ` (a, b) `。

> **类比**：  
> 把比例想成“两个数的配对标签”。我们把左边所有可能的标签放进左边的抽屉，用哈希表记下每个标签出现了多少次。右边遍历时，只要看到同样的标签，就知道左抽屉里有多少配对可以和它拼成完整的四元组。

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict
from typing import List

def normalize(a: int, b: int) -> tuple:
    """把分数 a / b 化为最简分数，返回 (分子, 分母) 的元组"""
    g = gcd(a, b)
    return (a // g, b // g)

def count_special_subsequences(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # left_cnt 用来统计所有已经出现的左配对 (p, q) 的比例
    # 键是 (nums[p] / nums[q]) 的最简分数，值是出现次数
    left_cnt = defaultdict(int)

    # r 从 2 开始，因为左配对至少需要两个元素 (p,q) 且 q = r-1
    for r in range(2, n - 1):
        q = r - 1                     # 新加入的左配对的第二个下标
        # 把所有以 q 为右端的左配对 (p, q) 加入统计
        for p in range(q):
            key = normalize(nums[p], nums[q])
            left_cnt[key] += 1        # 记录出现一次

        # 对当前的 r，遍历所有可能的 s（s > r），形成右配对 (s, r)
        for s in range(r + 1, n):
            key = normalize(nums[s], nums[r])
            ans += left_cnt.get(key, 0)   # 左配对中同样比例的数量直接累加

    return ans
```

> 代码中每一行都加了中文注释，帮助初学者快速定位关键操作。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个 `r`，内部两层循环分别是 `O(r)`（加入左配对）和 `O(n‑r)`（遍历右配对），两者相加再对所有 `r` 求和得到二次方级别。  
  - 与暴力的 `O(n⁴)` 相比，提升了 **两个数量级**，在 `n = 1000` 时大约只有几百万次基本操作，能够在毫秒级完成。

- **空间复杂度**：`O(n²)`（最坏情况）  
  - `left_cnt` 记录了所有左配对的比例。最坏情况下每一对 `(p, q)` 产生不同的比例，数量为 `C(n,2) ≈ n²/2`，但 `n ≤ 1000`，约为 5×10⁵ 条记录，完全在内存范围内。  
  - 与暴力解的 `O(1)` 空间相比，稍有增加，但换来了巨大的时间提升。

---

## 心得

- **核心技巧**：**把四元组拆成左右两对，利用哈希表累计左侧配对的比例**。  
- **适用的题型**  
  1. 需要比较两段子序列比例或乘积相等的题目（如 “Count Good Triplets” 中的比值问题）。  
  2. “两数之积相等” 或 “两数之和相等” 的四元组计数（可以把乘积/和转化为哈希计数的思路）。  
- **一句话总结**：**先把左边的配对计数下来，右边遍历时直接查表，就能把 O(n⁴) 降到 O(n²)。**

---

## 反思

- **拿到题目第一反应**：直接写四层循环，先验证思路能否得到正确答案。  
- **最容易踩的坑**  
  - **比例化简**：忘记使用 `gcd` 把分子分母约分，会导致同一比例被误认为不同的键，计数出错。  
  - **下标顺序**：一定要保证 `p < q < r < s`，尤其在实现“左配对”时要把 `q = r‑1` 固定，防止出现交叉的下标。  
  - **整数溢出**：虽然 Python 整数不溢出，但在某些语言里 `nums[p] * nums[r]` 可能超过 32 位，需要用长整型。  
- **下次类似题的第一步**：先思考能否把 **整体的约束拆分成两部分**（左/右、前/后），看能否用 **哈希表累计** 某种 “特征值”（比例、和、积），再在另一侧查表匹配。这样往往能把指数级搜索压到多项式级。