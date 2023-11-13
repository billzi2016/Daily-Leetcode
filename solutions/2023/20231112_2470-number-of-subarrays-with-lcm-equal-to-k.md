# #2470. 最小公倍数等于 K 的子数组数量 / Number of Subarrays With LCM Equal to K

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-subarrays-with-lcm-equal-to-k/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the number of subarrays of nums where the least common multiple of the subarray's elements is k.
A subarray is a contiguous non-empty sequence of elements within an array.
The least common multiple of an array is the smallest positive integer that is divisible by all the array elements.

**Examples**

**Example 1:**

```
Input: nums = [3,6,2,7,1], k = 6
Output: 4
Explanation: The subarrays of nums where 6 is the least common multiple of all the subarray's elements are:
- [3,6,2,7,1]
- [3,6,2,7,1]
- [3,6,2,7,1]
- [3,6,2,7,1]
```

**Example 2:**

```
Input: nums = [3], k = 2
Output: 0
Explanation: There are no subarrays of nums where 2 is the least common multiple of all the subarray's elements.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i], k <= 1000

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回 `nums` 中 **子数组（subarray）** 的数量，使得该子数组所有元素的 **最小公倍数（LCM）** 等于 `k`。  
子数组是数组中连续的、非空的元素序列。  
数组的最小公倍数是能够被数组中所有元素整除的最小的正整数。

**示例 1**  
**输入**: `nums = [3,6,2,7,1]`, `k = 6`  
**输出**: `4`  
**解释**: `nums` 中最小公倍数为 `6` 的子数组有：  
- `[3,6,2,7,1]`  
- `[3,6,2,7,1]`  
- `[3,6,2,7,1]`  
- `[3,6,2,7,1]`

**示例 2**  
**输入**: `nums = [3]`, `k = 2`  
**输出**: `0`  
**解释**: `nums` 中不存在最小公倍数为 `2` 的子数组。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i], k <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有子数组**，逐个算出它们的最小公倍数（LCM），看是否等于 `k`。  

- **子数组**：连续的一段元素，就像把一根绳子从第 `i` 根结点剪到第 `j` 根结点，中间的所有结点都是子数组的成员。  
- **LCM**：把若干个整数想象成齿轮，LCM 就是让所有齿轮转几圈后第一次恰好全部对齐的最小转数。  
- **哈希表类比**：我们这里不需要哈希表，只需要 **`gcd`（最大公约数）**，因为两数的 LCM 有公式  

\[
\text{lcm}(a,b)=\frac{a\times b}{\gcd(a,b)}
\]

  `gcd` 就像查字典一样：给出两个单词（数字），返回它们的共同根（最大公约数），再用公式算出 LCM。

枚举过程：

1. 外层循环挑选子数组的左端点 `i`（从 0 到 `n-1`）。  
2. 内层循环把右端点 `j` 从 `i` 向右扩展，每加入一个新元素就用公式把当前 LCM 与新元素合并得到新的 LCM。  
3. 每次得到的 LCM 与 `k` 比较，若相等计数器 `ans` 加一。

**为什么正确**：我们把所有可能的连续区间都遍历了一遍，且每个区间的 LCM 都算对了，符合题目“所有子数组”。  

**复杂度分析（大白话）**：

- 外层 `n` 次，内层最坏也要跑 `n` 次，两个循环相乘得到 **`O(n²)`**，也就是 **“平方级”**。如果 `n = 1000`，大约要做 1,000,000 次运算，电脑跑得很快。  
- 只用了常数级的额外变量（`gcd`、`lcm`、计数器），所以 **空间是 `O(1)`**，即 **“不占额外空间”**。

#### 代码（Python）

```python
import math
from typing import List

def subarrayLCM(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0                       # 统计满足条件的子数组个数

    # i 为子数组左端点
    for i in range(n):
        cur_lcm = 1                # 当前子数组的 LCM，先设为 1（乘法单位元）

        # j 为子数组右端点，向右扩展
        for j in range(i, n):
            # 计算加入 nums[j] 后的 LCM
            cur_lcm = cur_lcm * nums[j] // math.gcd(cur_lcm, nums[j])

            # 如果 LCM 已经超过 k，后面继续往右只会更大，直接停止本次 i 的循环
            if cur_lcm > k:
                break

            # LCM 恰好等于 k，答案加一
            if cur_lcm == k:
                ans += 1

    return ans
```

> **关键行解释**  
> - `cur_lcm = cur_lcm * nums[j] // math.gcd(cur_lcm, nums[j])`：用公式把新元素合并进 LCM。  
> - `if cur_lcm > k: break`：一旦 LCM 超过目标 `k`，再往右加只会更大，提前结束循环，省时。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子数组。  
- **空间复杂度**：`O(1)` —— 只用几个整数变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

虽然上面的实现已经是 `O(n²)`，但我们可以 **把不必要的计算提前剪掉**，让实际运行更快。  
关键观察：

1. **LCM 单调不减**：对正整数来说，往子数组里再加入一个元素，LCM **不会变小**（只能保持或增大）。这像往水桶里再倒水，水位只能上升或保持不变。  
2. **一旦超过 k，就永远不可能回到 k**：因为后面加入的数只会让 LCM 更大，永远不可能再等于 `k`。

基于这两点，我们在遍历每个左端点 `i` 时，**一旦当前 LCM 超过 `k` 就立刻停止向右扩展**，不必继续检查更长的子数组。  

这一步剪枝让我们在很多情况下大幅降低实际循环次数，尤其是当数组里出现大于 `k` 的数时，右侧的所有更长子数组都会被快速跳过。  

> **为什么仍是 `O(n²)` 的最坏情况？**  
> 在最坏情况下（比如所有元素都是 `1`，且 `k = 1`），LCM 永远等于 `1`，永远不会大于 `k`，于是我们仍然会遍历全部 `n(n+1)/2` 个子数组。但即使如此，`n ≤ 1000`，仍然可以在毫秒级完成。

#### 代码（Python）

```python
import math
from typing import List

def subarrayLCM_opt(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0

    for i in range(n):
        cur_lcm = 1
        for j in range(i, n):
            # 计算加入 nums[j] 后的 LCM
            cur_lcm = cur_lcm * nums[j] // math.gcd(cur_lcm, nums[j])

            # 剪枝：LCM 已经超过 k，后面的子数组不可能满足条件
            if cur_lcm > k:
                break

            if cur_lcm == k:
                ans += 1

    return ans
```

> 与暴力解唯一的区别是 **加入了 `if cur_lcm > k: break`** 这行，实现了“提前止步”。其余代码保持不变，便于阅读和调试。

#### 复杂度

- **时间复杂度**：**最坏 `O(n²)`**，**平均会更快**（因为提前终止）。  
  - 与暴力解相比，**实际执行的循环次数通常会少很多**，尤其当 `k` 较小或数组中出现大数时。  
- **空间复杂度**：`O(1)`——只用常数级的几个整数。

---

## 心得

- **核心技巧**：**利用 LCM 的单调性进行剪枝**。  
- **适用的题型**（类似思路）  
  1. “子数组的最大公约数（GCD）等于 K”——同样利用 GCD 单调不增的特性。  
  2. “子数组乘积小于 K”——乘积也单调递增，可用滑动窗口或提前终止。  
- **一句话总结**：**“一旦目标值被超越，后面的更长子数组就不可能再回到目标，直接停下”。**

---

## 反思

- **第一反应**：直接把所有子数组枚举一遍，逐个算 LCM。  
- **最容易踩的坑**  
  - **整数溢出**：在 Python 中整数会自动扩容，但在其他语言需要注意 `a * b` 可能会超过 64 位。使用 `a // gcd(a,b) * b` 能降低溢出概率。  
  - **边界条件**：`k = 1` 时，所有只含 `1` 的子数组都符合，需要确保循环不因 `break` 提前退出。  
  - **LCM 计算**：不要忘记先除后乘，否则 `a * b` 可能产生非常大的中间值。  
- **下次遇到同类题**：**先思考“随着区间扩展，目标量是增大还是减小”，如果是单调的，就可以考虑提前剪枝或滑动窗口**。这样往往能把朴素的 `O(n²)` 直接变成更快的实现。