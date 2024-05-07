# #2681. 英雄的力量 / Power of Heroes

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/power-of-heroes/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums representing the strength of some heroes. The power of a group of heroes is defined as follows:
Return the sum of the power of all non-empty groups of heroes possible. Since the sum could be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,1,4]
Output: 141
Explanation: 
1st group: [2] has power = 22 * 2 = 8.
2nd group: [1] has power = 12 * 1 = 1. 
3rd group: [4] has power = 42 * 4 = 64. 
4th group: [2,1] has power = 22 * 1 = 4. 
5th group: [2,4] has power = 42 * 2 = 32. 
6th group: [1,4] has power = 42 * 1 = 16. 
​​​​​​​7th group: [2,1,4] has power = 42​​​​​​​ * 1 = 16. 
The sum of powers of all groups is 8 + 1 + 64 + 4 + 32 + 16 + 16 = 141.
```

**Example 2:**

```
Input: nums = [1,1,1]
Output: 7
Explanation: A total of 7 groups are possible, and the power of each group will be 1. Therefore, the sum of the powers of all groups is 7.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`，其中 `nums[i]` 表示第 i 位英雄的 **strength**（力量）。  
一个英雄组的 **power**（力量）定义如下：

- 设该组中力量的最大值为 `max`，最小值为 `min`。  
- 该组的力量为 `max² * min`。

求所有 **非空** 英雄组的力量之和。由于结果可能非常大，返回结果对 `10⁹ + 7` 取模后的值。

---

### 示例

#### 示例 1  
**输入**  
```json
nums = [2,1,4]
```  

**输出**  
```
141
```  

**解释**  

1. 组 `[2]` 的力量 = `2² * 2 = 8`。  
2. 组 `[1]` 的力量 = `1² * 1 = 1`。  
3. 组 `[4]` 的力量 = `4² * 4 = 64`。  
4. 组 `[2,1]` 的力量 = `2² * 1 = 4`。  
5. 组 `[2,4]` 的力量 = `4² * 2 = 32`。  
6. 组 `[1,4]` 的力量 = `4² * 1 = 16`。  
7. 组 `[2,1,4]` 的力量 = `4² * 1 = 16`。  

所有组的力量之和为 `8 + 1 + 64 + 4 + 32 + 16 + 16 = 141`。

#### 示例 2  
**输入**  
```json
nums = [1,1,1]
```  

**输出**  
```
7
```  

**解释**  
共计 7 种非空组，每组的力量均为 `1`，因此总和为 `7`。

---

### 约束

- `1 <= nums.length <= 10⁵`
- `1 <= nums[i] <= 10⁹`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有非空子集**，对每个子集计算  

```
power = (子集中的最大值)² × (子集中的最小值)
```

然后把所有 `power` 加起来。  

- **数据结构**：只需要用 Python 的列表（list）来保存原数组，枚举子集时可以用 `itertools.combinations` 或者二进制枚举。  
- **为什么正确**：因为题目要求把**每一种可能的组合**都算上，而暴力枚举正好把所有组合都遍历到了。  

> **类比**：把所有组合想成一本《英雄手册》，我们把每一页（每个子集）都翻一遍，记下它的“力量”，最后把这些力量相加。

#### 代码（Python）

```python
from itertools import combinations

MOD = 10**9 + 7

def power_of_group(sub):
    """返回一个子集的 power = (max)^2 * min"""
    mx = max(sub)
    mn = min(sub)
    return (mx * mx % MOD) * mn % MOD

def brute(nums):
    n = len(nums)
    ans = 0
    # 1~n 长度的所有子集
    for sz in range(1, n + 1):
        for comb in combinations(nums, sz):
            ans = (ans + power_of_group(comb)) % MOD
    return ans

# ------------------- 示例 -------------------
print(brute([2, 1, 4]))   # 141
print(brute([1, 1, 1]))   # 7
```

> 关键行中文注释  
> - `combinations(nums, sz)`：把数组里挑出 `sz` 个元素的所有组合。  
> - `power_of_group`：先找最大值 `mx`、最小值 `mn`，再算 `mx² * mn`（取模防止溢出）。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（每个元素可以选或不选，所有非空子集共 `2^n‑1` 个）。  
  - 大白话：如果数组有 20 个人，暴力要检查 `2^20 ≈ 1,048,576` 种组合，人数多了指数就爆炸。  
- **空间复杂度**：`O(n)`（递归/迭代时保存当前子集的临时空间），主要是存放组合本身。

> 暴力解只适合 **n 很小**（比如 `n ≤ 20`）的情况，面对题目给出的 `n ≤ 10⁵` 完全不可行。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**枚举所有子集**。我们要想办法**不逐个子集去算**，而是直接把同类子集的贡献合并。

1. **先把数组排序**  
   把英雄的力量从小到大排好，这样子集的 **最小值** 一定在左边，**最大值** 一定在右边。  
   > 类比：把英雄排成一条队伍，左边的永远是“最弱”，右边的永远是“最强”。

2. **固定最大值**  
   假设 `nums[j]` 是子集的最大值（`j` 为下标）。子集的最小值只能是 `nums[i]`（`i ≤ j`）。  
   - 当 `i < j` 时，介于 `i` 与 `j` 的元素 **可以自由选或不选**，每个位置有 2 种可能，故共有 `2^{j-i-1}` 种子集。  
   - 当 `i = j`（子集只有一个元素）时，子集数是 1。  

   因此，以 `nums[j]` 为最大值的所有子集贡献为  

   \[
   \text{contrib}_j = nums[j]^2 \times
   \Big( nums[j] \;+\; \sum_{i=0}^{j-1} nums[i]\times 2^{\,j-i-1}\Big)
   \]

   这里的大括号就是“所有可能的最小值 + 对应的子集数量”。

3. **把求和改成前缀累计**  
   定义  

   \[
   S_j = nums[j] + \sum_{i=0}^{j-1} nums[i]\times 2^{\,j-i-1}
   \]

   我们希望在一次遍历中得到 `S_j`。观察 `S_{j-1}`：

   \[
   S_{j-1}=nums[j-1] + \sum_{i=0}^{j-2} nums[i]\times 2^{\,j-1-i-1}
   \]

   两边同时乘以 2：

   \[
   2S_{j-1}=2\,nums[j-1] + \sum_{i=0}^{j-2} nums[i]\times 2^{\,j-i-1}
   \]

   与 `S_j` 对比可得递推式  

   \[
   S_j = nums[j] + 2S_{j-1} - nums[j-1]
   \]

   （`- nums[j-1]` 是因为 `2S_{j-1}` 把 `nums[j-1]` 的系数变成了 2，而我们只需要系数 1）

   用这个式子我们只要维护一个变量 `pref`（即 `S_{j-1}`），就能 **O(1)** 时间得到 `S_j`。

4. **整体流程**  

   - 把 `nums` 按升序排序。  
   - 预计算 `pow2[k] = 2^k mod MOD`（虽然递推里已经隐式用了 2 的幂，但有时直接取模会更安全）。  
   - 依次遍历 `j = 0 … n-1`：  
     - 更新 `pref = (2*pref - nums[j-1] + MOD) % MOD`（注意 `j=0` 时没有 `j-1`）。  
     - `pref = (pref + nums[j]) % MOD` 得到 `S_j`。  
     - 累加答案 `ans = (ans + nums[j] * nums[j] % MOD * pref) % MOD`。  

   这样只用了 **一次线性遍历**，时间 `O(n)`（加上排序的 `O(n log n)`），空间 `O(1)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def power_of_heroes(nums):
    """
    返回所有非空子集的 power 和，power = (max)^2 * min
    采用排序 + 前缀累计的 O(n log n) 解法。
    """
    nums.sort()                     # 让最小值在左，最大值在右
    n = len(nums)

    ans = 0          # 最终答案
    pref = 0         # 对应 S_{j-1}，即上一次的前缀累计

    for j in range(n):
        # 1) 计算当前的 S_j
        #   S_j = nums[j] + 2 * S_{j-1} - nums[j-1]（j>0 时）
        if j == 0:
            pref = nums[0]               # S_0 = nums[0]
        else:
            pref = (2 * pref - nums[j-1]) % MOD   # 2*S_{j-1} - nums[j-1]
            pref = (pref + nums[j]) % MOD         # + nums[j]

        # 2) 累加以 nums[j] 为最大值的所有子集贡献
        ans = (ans + (nums[j] * nums[j] % MOD) * pref) % MOD

    return ans

# ------------------- 示例 -------------------
print(power_of_heroes([2, 1, 4]))   # 141
print(power_of_heroes([1, 1, 1]))   # 7
```

> **关键行中文注释**  
> - `nums.sort()`：把英雄按力量从弱到强排好，方便后面固定最大值。  
> - `pref = (2 * pref - nums[j-1]) % MOD`：利用递推式一次性得到新的前缀和。  
> - `ans = (ans + (nums[j] * nums[j] % MOD) * pref) % MOD`：把 “当前最大值的平方 × 所有可能的最小值加权和” 加进答案。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`，遍历一次 `O(n)`。  
  - 与暴力的 `O(2^n)` 相比，指数级下降，几乎可以处理 `n = 10⁵` 的极限输入。  
- **空间复杂度**：`O(1)`（不计排序本身的原地修改）  
  - 只用了几个整数变量 `ans、pref`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**把子集的贡献拆成“最大值 ×（所有可能的最小值的加权和）”，并利用排序 + 前缀累计把加权和在一次遍历中算完**。  
- **适用的题型**：  
  1. 需要统计所有子集中**最大/最小**组合的题目（如 “子集的最大值最小值乘积”）。  
  2. 需要对每个子集的**某个元素的幂次**做累计的题目（如 “子集的最大值的平方乘以最小值”）。  
  3. 任何可以把子集贡献写成 `f(max) * g(min)` 并且 `max/min` 在排序后有单调性的题目。  
- **一句话总结解题钥匙**：**“先排序，让最大值固定，再用前缀累计把所有最小值的加权和一次算完”。**

---

## 反思

- **第一反应**：看到 “所有非空子集”立刻想到 **枚举**，写出 `2^n` 暴力解。  
- **最容易踩的坑**：  
  - **模运算**：在递推式里出现负数，需要加 `MOD` 再取模，防止 Python 的负模结果错误。  
  - **溢出**：`nums[j]^2` 可能超过 64 位整数，必须在乘法后立刻 `% MOD`。  
  - **边界条件**：`j = 0` 时没有 `nums[j-1]`，递推式要单独处理。  
- **下次遇到同类题**，第一步应该思考：**“能否把子集的贡献拆成只和最大值、最小值有关的乘积？”**，如果能，尝试 **排序 + 前缀累计** 或 **单调栈** 等线性技巧。