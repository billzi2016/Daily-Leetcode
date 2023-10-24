# #2447. GCD 等于 K 的子数组数量 / Number of Subarrays With GCD Equal to K

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-subarrays-with-gcd-equal-to-k/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the number of subarrays of nums where the greatest common divisor of the subarray's elements is k.
A subarray is a contiguous non-empty sequence of elements within an array.
The greatest common divisor of an array is the largest integer that evenly divides all the array elements.

**Examples**

**Example 1:**

```
Input: nums = [9,3,1,2,6,3], k = 3
Output: 4
Explanation: The subarrays of nums where 3 is the greatest common divisor of all the subarray's elements are:
- [9,3,1,2,6,3]
- [9,3,1,2,6,3]
- [9,3,1,2,6,3]
- [9,3,1,2,6,3]
```

**Example 2:**

```
Input: nums = [4], k = 7
Output: 0
Explanation: There are no subarrays of nums where 7 is the greatest common divisor of all the subarray's elements.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i], k <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回 `nums` 中子数组（subarray）的数量，使得该子数组所有元素的最大公约数（greatest common divisor，GCD）恰好等于 `k`。

子数组（subarray）是数组中连续的、非空的元素序列。

数组的最大公约数（GCD）是能够整除数组中所有元素的最大整数。

**示例 1：**  
**输入:** `nums = [9,3,1,2,6,3]`, `k = 3`  
**输出:** `4`  
**解释:** `nums` 中满足最大公约数为 `3` 的子数组有：  
- `[9,3]`  
- `[3]`  
- `[3,1,2,6,3]`  
- `[6,3]`

**示例 2：**  
**输入:** `nums = [4]`, `k = 7`  
**输出:** `0`  
**解释:** 不存在最大公约数为 `7` 的子数组。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i], k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的子数组都枚举出来**，然后逐个求它们的最大公约数（GCD），看是否等于 `k`。  

- **枚举子数组**：数组长度记作 `n`，子数组的左端点可以是 `0 … n‑1`，右端点可以是左端点所在位置往后一直到 `n‑1`，所以总共有 `n·(n+1)/2` 种子数组。  
- **求 GCD**：可以使用 Python 标准库 `math.gcd`（实现了欧几里得算法），把子数组里的元素两两取 GCD，最终得到整个子数组的 GCD。  
- **统计**：如果得到的 GCD 正好等于 `k`，计数器 `ans` 加一。

> **类比**：把哈希表想象成一本词典，`key` 是单词，`value` 是对应的解释。这里我们不需要哈希表，只是把每个子数组当成一本“小书”，把它的所有数字“翻一遍”，算出它们的“共同语言”（GCD），看是不是我们想要的 `k`。

这种方法一定能得到正确答案，因为我们把 **所有** 子数组都检查了一遍。

#### 代码（Python）

```python
import math
from typing import List

def subarrayGCD_brute(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0                     # 统计满足条件的子数组个数
    # 枚举左端点
    for i in range(n):
        cur_gcd = 0              # 当前子数组的 GCD，初始为 0（与任意数 gcd 为该数本身）
        # 枚举右端点
        for j in range(i, n):
            cur_gcd = math.gcd(cur_gcd, nums[j])   # 逐个加入元素，更新 GCD
            if cur_gcd == k:       # 若 GCD 已经等于 k，就可以计数
                ans += 1
            # 如果 GCD 已经小于 k 且 k 不是它的因数，则后面再加入元素也不可能回到 k
            # 这里不做剪枝，保持最朴素的实现
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²·logM)`  
  - `n²` 来自双层循环枚举所有子数组。  
  - `logM`（`M` 为数组中最大元素）是求一次 GCD 的代价，欧几里得算法的时间与数的大小的对数成正比。  
  - **大白话**：如果数组长度是 1000，最坏情况下要检查大约 500,000 条子数组，每条子数组再算几次 GCD，整体算力仍在可接受范围（约几千万次基本运算）。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都从头重新计算子数组的 GCD**，这导致大量重复工作。  
观察如下：

- 当我们把子数组 `[i … j]` 的 GCD 已经算出来后，想要得到 `[i … j+1]` 的 GCD，只需要把 `nums[j+1]` 与已有的 GCD 再做一次 `gcd` 运算。  
- 对于固定的右端点 `j`，所有以 `j` 结尾的子数组的 GCD 只会出现 **有限且递减** 的不同值（因为加入新元素只能让 GCD 不增），而且这些不同值的个数最多是 `O(log M)`（每次至少除以一个质因子）。

基于这个观察，我们可以 **动态维护** “以当前位置结尾的所有子数组的 GCD 及其出现次数”。实现思路：

1. 用一个字典 `cnt`（`gcd → 出现次数`）记录 **以当前元素为右端点** 的所有子数组的 GCD。
2. 处理第 `i` 个元素时：
   - 先把 `nums[i]` 自己形成的子数组加入：`new_cnt[nums[i]] += 1`。
   - 再遍历前一步的 `cnt`，把每个旧的 GCD 与 `nums[i]` 取 GCD，得到新的 GCD，并把对应的出现次数累加到 `new_cnt`。
3. 把 `new_cnt` 设为下一轮的 `cnt`。
4. 每次更新后，只要 `new_cnt` 中有键等于 `k`，就把对应的次数加到答案里。

这相当于 **滑动窗口 + 状态压缩**，每一步只处理少量（对数级）状态，整体时间大幅下降。

> **类比**：想象你在玩拼图，每块拼图只能和左边已经拼好的图块拼接。我们不必每次都从头重新检查所有拼图，而是只看最新加入的那块和已经拼好的 “局部形状” 会产生什么新的形状。这里的 “形状” 就是 GCD。

#### 代码（Python）

```python
import math
from collections import defaultdict
from typing import List

def subarrayGCD_opt(nums: List[int], k: int) -> int:
    ans = 0                     # 最终答案
    cnt = {}                    # cnt[g] = 以当前元素结尾且 GCD 为 g 的子数组个数

    for x in nums:              # 逐个遍历数组元素，x 是当前右端点的值
        new_cnt = defaultdict(int)

        # 1. 只包含当前元素的子数组
        new_cnt[x] += 1

        # 2. 把之前所有以 i-1 为右端点的子数组，延伸到当前元素
        for g, c in cnt.items():
            ng = math.gcd(g, x)   # 旧 GCD 与新元素取 GCD
            new_cnt[ng] += c      # 这些子数组的数量保持不变，只是 GCD 变了

        # 3. 统计本轮出现的 GCD 为 k 的子数组数目
        ans += new_cnt.get(k, 0)

        # 4. 为下一轮准备
        cnt = new_cnt

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·logM)`  
  - 对每个位置，只遍历 `cnt` 中的键。`cnt` 的大小最多是 `O(logM)`（因为 GCD 只能不断被约掉），所以整体是 `n` 乘以对数级的常数。  
  - **对比**：暴力是 `n²·logM`，这里把平方降到了线性，速度提升大约是 `n` 倍（对 `n=1000` 来说约 1000 倍）。

- **空间复杂度**：`O(logM)`  
  - 只需要保存当前右端点的所有不同 GCD 及其计数，数量同样是对数级。

---

## 心得

- **核心技巧**：利用 **前缀状态压缩**（或叫“以右端点为中心的动态规划”）把所有以当前元素结尾的子数组的 GCD 合并，用哈希表记录不同 GCD 出现的次数。  
- **适用的题型**  
  1. “子数组的 GCD / LCM / 最大值 / 最小值” 需要在 **所有子数组** 中统计某种属性的题目（如 LeetCode 1735 `Count Subarrays With Max Difference`）。  
  2. “子数组的异或 / 和 / 乘积” 类似的计数题，常用前缀哈希或前缀和/乘积的技巧。  
- **一句话总结**：**把以右端点为中心的子数组状态压缩成少量的 GCD 键值对，就能线性时间完成计数**。

---

## 反思

- **第一反应**：看到 “子数组”和 “GCD”，立刻想到枚举所有子数组并逐个求 GCD——这是最自然的暴力思路。  
- **最容易踩的坑**  
  - **溢出/大数**：GCD 本身不会产生溢出，但要避免在 `cnt` 中存入过多不同的键，否则会导致时间爆炸。  
  - **边界条件**：当 `k` 本身不在数组中，仍然可能出现子数组 GCD 为 `k`（因为多个数的 GCD 可能更小），所以不能仅检查单个元素。  
  - **重复计数**：在压缩状态时必须把相同 GCD 的子数组计数累加，否则会漏掉很多子数组。  
- **下次类似题的第一步**：先思考 **“是否可以把子数组的状态随右端点递推”**，如果可以，就尝试用哈希表/字典记录状态，避免全局枚举。这样往往能把 `O(n²)` 降到 `O(n·log)` 或 `O(n)`。