# #923. 带重复计数的三数之和 / 3Sum With Multiplicity

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/3sum-with-multiplicity/)

---

## 题目（英文原版）

**Description**

Given an integer array arr, and an integer target, return the number of tuples i, j, k such that i < j < k and arr[i] + arr[j] + arr[k] == target.
As the answer can be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: arr = [1,1,2,2,3,3,4,4,5,5], target = 8
Output: 20
Explanation: 
Enumerating by the values (arr[i], arr[j], arr[k]):
(1, 2, 5) occurs 8 times;
(1, 3, 4) occurs 8 times;
(2, 2, 4) occurs 2 times;
(2, 3, 3) occurs 2 times.
```

**Example 2:**

```
Input: arr = [1,1,2,2,2,2], target = 5
Output: 12
Explanation: 
arr[i] = 1, arr[j] = arr[k] = 2 occurs 12 times:
We choose one 1 from [1,1] in 2 ways,
and two 2s from [2,2,2,2] in 6 ways.
```

**Example 3:**

```
Input: arr = [2,1,3], target = 6
Output: 1
Explanation: (1, 2, 3) occured one time in the array so we return 1.
```

**Constraints**

- 3 <= arr.length <= 3000
- 0 <= arr[i] <= 100
- 0 <= target <= 300

---

## 题目（中文翻译）

给定一个整数数组 `arr` 和一个整数 `target`，返回满足 `i < j < k` 且 `arr[i] + arr[j] + arr[k] == target` 的元组 (i, j, k) 的数量。  
由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**Example 1:**  
Input: `arr = [1,1,2,2,3,3,4,4,5,5]`, `target = 8`  
Output: `20`  
解释：  
按数值枚举 `(arr[i], arr[j], arr[k])`：  
- `(1, 2, 5)` 出现了 8 次；  
- `(1, 3, 4)` 出现了 8 次；  
- `(2, 2, 4)` 出现了 2 次；  
- `(2, 3, 3)` 出现了 2 次。

**Example 2:**  
Input: `arr = [1,1,2,2,2,2]`, `target = 5`  
Output: `12`  
解释：  
`arr[i] = 1, arr[j] = arr[k] = 2` 这种组合出现了 12 次：  
- 从 `[1,1]` 中选取一个 `1` 有 2 种方式；  
- 从 `[2,2,2,2]` 中选取两个 `2` 有 6 种方式。

**Example 3:**  
Input: `arr = [2,1,3]`, `target = 6`  
Output: `1`  
解释：`(1, 2, 3)` 在数组中出现一次，所以返回 1。

约束条件：  
- `3 <= arr.length <= 3000`  
- `0 <= arr[i] <= 100`  
- `0 <= target <= 300`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有满足 `i < j < k` 的三元组枚举一遍，检查它们的和是否等于 `target`。  
这相当于在数组里找 3 张不同的牌，顺序必须保持（先拿第 i 张，再拿第 j 张，最后第 k 张），看这三张牌的点数之和能不能恰好等于目标分数。

- **用到的数据结构**：只需要遍历数组本身，不需要额外的数据结构。  
- **为什么正确**：因为我们把所有合法的三元组都检查了一遍，只要有满足条件的，就一定会被统计到。  
- **时间/空间复杂度**：  
  - 需要三个嵌套的循环，每个循环最多遍历 `n`（数组长度）次，所以总共大约是 `n × n × n = n³` 次操作。  
  - 空间上只用了常数个变量，和 `n` 无关，记作 **O(1)**。  

> **大白话解释**：  
> `O(n³)` 可以想象成“把 3000 本书里每本书的每一页都和每一页的每一页比一次”。当 `n` 只有几百时还能接受，`n` 达到几千甚至上万就会非常慢了。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def threeSumMulti_bruteforce(arr: List[int], target: int) -> int:
    n = len(arr)
    ans = 0
    # 第一个循环挑 i
    for i in range(n):
        # 第二个循环挑 j，必须大于 i
        for j in range(i + 1, n):
            # 第三个循环挑 k，必须大于 j
            for k in range(j + 1, n):
                if arr[i] + arr[j] + arr[k] == target:   # 检查三数之和
                    ans += 1
    return ans % MOD
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 意味着如果 `n = 3000`，循环次数大约是 `27,000,000,000`，在实际运行时会超时。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量，和数组大小无关。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**瓶颈** 在于三个嵌套循环导致的 `n³` 复杂度。  
观察题目限制：

- `arr[i]` 的取值范围只有 `0 … 100`（共 101 种可能），非常小。  
- `target` 最大是 `300`，也是一个小常数。

利用「取值范围小」的特点，我们可以先统计每个数出现了多少次（相当于把数组压缩成「字典」），再在 **值的层面** 上枚举三元组，而不是在 **下标的层面** 上枚举。

##### 步骤 1：统计频率（哈希表）

把数组中每个数出现的次数记下来。  
这一步可以把原来的长度 `n`（最多 3000）压缩成最多 101 条记录。  
哈希表在这里就像一本「数字词典」：`key` 是数字本身，`value` 是它在数组里出现的次数。

```python
cnt = [0] * 101          # cnt[x] 表示数字 x 出现的次数
for x in arr:
    cnt[x] += 1
```

##### 步骤 2：枚举有序的数值组合 `(a, b, c)`

因为我们要求 `i < j < k`，对应到数值上，只需要保证 **数值的非递减顺序** `a ≤ b ≤ c`，这样每一种组合只会被统计一次。

我们用两层循环遍历 `a` 和 `b`（`a` 从 0 到 100，`b` 从 `a` 到 100），然后由目标公式算出 `c = target - a - b`。如果 `c` 落在合法范围 `[b, 100]`，说明这三个数可以组成目标和。

##### 步骤 3：根据出现次数算出具体的三元组数目

根据 `a、b、c` 是否相等，组合数的计算方式不同：

| 情形 | 说明 | 计数公式 |
|------|------|----------|
| `a = b = c` | 三个数全相同 | `C(cnt[a], 3) = cnt[a] * (cnt[a]-1) * (cnt[a]-2) / 6` |
| `a = b < c` | 前两个相同，第三个不同 | `C(cnt[a], 2) * cnt[c] = cnt[a] * (cnt[a]-1) / 2 * cnt[c]` |
| `a < b = c` | 后两个相同，前一个不同 | `cnt[a] * C(cnt[b], 2)` |
| `a < b < c` | 三个数全不同 | `cnt[a] * cnt[b] * cnt[c]` |

这里的 **C(n, k)** 是组合数，表示从 `n` 个相同元素中挑 `k` 个的不同挑选方式数。

把每种情形算出的数量加到答案里，最后对 `10⁹+7` 取模即可。

##### 为什么快？

- 统计频率只需要遍历一次数组：`O(n)`。
- 两层循环的范围是 `0 … 100`，最多 `101 × 101 ≈ 10⁴` 次，远小于 `n³`。
- 组合数的计算是 O(1) 的公式。

> **类比**：想象你在超市里挑三件商品，超市里只有 101 种商品，每种商品有一定库存。我们不需要逐个检查每件商品的具体位置，只要看每种商品有多少库存，然后用数学公式算出挑选方式。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def threeSumMulti(arr: List[int], target: int) -> int:
    # 1️⃣ 统计每个数的出现次数
    cnt = [0] * 101                # 因为 0 ≤ arr[i] ≤ 100
    for x in arr:
        cnt[x] += 1

    ans = 0

    # 2️⃣ 枚举 a ≤ b ≤ c
    for a in range(101):
        if cnt[a] == 0:            # 没出现的数字直接跳过，省时间
            continue
        for b in range(a, 101):
            if cnt[b] == 0:
                continue
            c = target - a - b
            # c 必须满足 b ≤ c ≤ 100，且出现次数大于 0
            if c < b or c > 100 or cnt[c] == 0:
                continue

            # 3️⃣ 根据 a、b、c 的相等关系计算组合数
            if a == b == c:
                # C(cnt[a], 3)
                ways = cnt[a] * (cnt[a] - 1) * (cnt[a] - 2) // 6
            elif a == b < c:
                # C(cnt[a], 2) * cnt[c]
                ways = cnt[a] * (cnt[a] - 1) // 2 * cnt[c]
            elif a < b == c:
                # cnt[a] * C(cnt[b], 2)
                ways = cnt[a] * cnt[b] * (cnt[b] - 1) // 2
            else:  # a < b < c
                ways = cnt[a] * cnt[b] * cnt[c]

            ans = (ans + ways) % MOD   # 防止中间结果溢出

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n + U²)`，其中 `U = 101` 是取值上限。  
  - `O(n)` 用于一次遍历统计频率。  
  - `U² ≈ 10⁴` 用于枚举所有可能的 `(a, b)`。  
  - 对比暴力的 `O(n³)`，这里即使 `n = 3000` 也只需要几万次循环，轻松跑完。  

- **空间复杂度**：`O(U)`，即 `101` 的整数数组，用来存放频率。  
  - 只和取值范围有关，和原数组长度 `n` 无关。

---

## 心得

- **核心技巧**：利用「数值范围小」做**频率计数 + 组合数学**，把原本的指数级枚举降到常数级别。  
- **适用的题型**  
  1. “Two Sum / Three Sum” 这类求和计数的题目，当元素取值范围受限时。  
  2. “Count Good Triplets” 或 “Number of Pairs with Given Sum” 等需要统计组合数的题目。  
  3. “Subarray Sum Equals K” 的变种，如果数组元素值域有限，同样可以先做频率统计。  

- **一句话总结**：**把“大集合”压缩成“小字典”，再用组合公式直接算答案**。

---

## 反思

- **第一反应**：立刻想到三层循环暴力遍历，因为最直接的思路总是先把所有可能列出来。  
- **最容易踩的坑**  
  - **边界条件**：`c` 计算出来后必须满足 `b ≤ c ≤ 100`，否则会出现负数或超出数组索引。  
  - **组合数除法**：使用整数除法时要保证先做乘法再除，防止出现小数或精度问题（在 Python 中 `//` 保证整数）。  
  - **取模时机**：中间累加可能会超过 64 位整数范围，最好每次加完后立即 `% MOD`。  

- **下次类似题的第一步**：检查**数值范围是否小**，如果是，就先**统计频率**，再在「值」的层面上枚举组合，而不是在「下标」层面逐一遍历。这样往往能把时间复杂度从指数级直接降到多项式甚至常数级。