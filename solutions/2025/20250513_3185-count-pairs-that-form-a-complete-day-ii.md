# #3185. 统计构成完整天的配对 II / Count Pairs That Form a Complete Day II

> 难度：中等 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/count-pairs-that-form-a-complete-day-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array hours representing times in hours, return an integer denoting the number of pairs i, j where i < j and hours[i] + hours[j] forms a complete day.
A complete day is defined as a time duration that is an exact multiple of 24 hours.
For example, 1 day is 24 hours, 2 days is 48 hours, 3 days is 72 hours, and so on.

**Examples**

**Example 1:**

```
Input: hours = [12,12,30,24,24]
Output: 2
Explanation: The pairs of indices that form a complete day are (0, 1) and (3, 4) .
```

**Example 2:**

```
Input: hours = [72,48,24,3]
Output: 3
Explanation: The pairs of indices that form a complete day are (0, 1) , (0, 2) , and (1, 2) .
```

**Constraints**

- 1 <= hours.length <= 5 * 105
- 1 <= hours[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `hours`，其中的元素表示以小时为单位的时间，返回满足 `i < j` 且 `hours[i] + hours[j]` 构成完整天（complete day）的下标对 `(i, j)` 的数量。

完整天（complete day）被定义为持续时间恰好是 24 小时的整数倍。例如，1 天是 24 小时，2 天是 48 小时，3 天是 72 小时，依此类推。

**示例 1：**

```
Input: hours = [12,12,30,24,24]
Output: 2
Explanation: 构成完整天的索引对为 (0, 1) 和 (3, 4) 。
```

**示例 2：**

```
Input: hours = [72,48,24,3]
Output: 3
Explanation: 构成完整天的索引对为 (0, 1)、(0, 2) 和 (1, 2) 。
```

**约束条件：**
- `1 <= hours.length <= 5 * 10^5`
- `1 <= hours[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的下标对 `(i, j)`（要求 `i < j`）都枚举一遍，检查它们的和是否能被 24 整除。  
- **数据结构**：只需要遍历数组本身，用两个循环分别控制 `i` 与 `j`。不需要额外的容器。  
- **为什么正确**：因为题目要求的条件是“所有满足 `i < j 且 (hours[i] + hours[j]) % 24 == 0` 的对”。只要我们把每一种可能的 `(i, j)` 都算一遍，就不会漏掉任何合法的组合，也不会把不合法的算进去。  

#### 代码（Python）

```python
from typing import List

def countPairs_bruteforce(hours: List[int]) -> int:
    n = len(hours)
    ans = 0                     # 用来累计符合条件的对数
    # 第一个循环固定左边的下标 i
    for i in range(n):
        # 第二个循环找右边的下标 j，必须保证 j > i
        for j in range(i + 1, n):
            # 判断两数之和是否是 24 的倍数
            if (hours[i] + hours[j]) % 24 == 0:
                ans += 1        # 找到一组合法的配对，计数加一
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “O(n²)” 可以想象成把 `n` 个元素排成一行，每个元素都要和后面的所有元素比较一次，形成一个 `n × n` 的格子（对角线以下的格子是我们真正遍历的），所以次数大约是 `n² / 2`，量级就是二次方。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`ans、i、j`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈**在于两层循环导致的 `O(n²)` 时间。  
观察题目条件：

```
(hours[i] + hours[j]) % 24 == 0
⇔ (hours[i] % 24 + hours[j] % 24) % 24 == 0
```

这意味着只要我们知道每个数 **模 24** 的余数，就可以把问题转化为“找两个余数之和为 24（或 0）”。  

**关键点**：  
- 余数只有 0~23 共 24 种可能，远远小于 `n`（最高可达 5·10⁵）。  
- 当我们从左到右遍历数组时，假设当前下标是 `j`，我们已经处理过 `j` 左边的所有元素 `i`。如果我们知道左边每个余数出现了多少次，就可以**直接**算出有多少个 `i` 能和 `j` 配对，使得和为 24 的整数倍。

具体做法：

1. 维护一个长度为 24 的计数数组 `cnt`（或哈希表），`cnt[r]` 表示已经遍历过的元素中，余数等于 `r` 的数量。可以把它想象成一本“余数字典”，`r` 是单词，`cnt[r]` 是这本字典里这个单词出现了几页。  
2. 对于当前元素 `hours[j]`，先算出它的余数 `r = hours[j] % 24`。  
3. 为了让两数之和是 24 的倍数，需要另一个余数 `need = (24 - r) % 24`（注意 `r = 0` 时 `need` 仍然是 0）。  
4. 已经出现的 `need` 次数就是可以和当前 `j` 组成合法对的数量，直接加到答案里。  
5. 最后把当前余数 `r` 加入计数表 `cnt[r] += 1`，为后面的元素提供配对机会。  

这样只需要一次遍历，时间是 `O(n)`，空间是固定的 24 个计数，`O(1)`。

#### 代码（Python）

```python
from typing import List

def countPairs_opt(hours: List[int]) -> int:
    # cnt[k] 表示已经遍历过的元素中，余数为 k 的出现次数
    cnt = [0] * 24          # 只需要 24 个格子，空间固定
    ans = 0                 # 最终答案

    for h in hours:         # 从左到右依次处理每个元素
        r = h % 24          # 当前元素的余数
        need = (24 - r) % 24   # 为配成完整天，需要的另一个余数
        ans += cnt[need]    # 之前出现过 need 次数的元素，都可以和当前 h 配对
        cnt[r] += 1         # 把当前余数计入统计，供后面的元素使用

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每一步的操作都是常数时间（取余、数组索引、加法），所以整体随 `n` 线性增长。相比暴力的二次方，这就像把“遍历整张表格”简化成“只走一条直线”。  
- **空间复杂度**：`O(1)`  
  - 计数数组固定大小为 24，和输入规模无关，等价于常数空间。

---

## 心得

- **核心技巧**：利用**模运算 + 计数哈希表（或固定大小数组）** 把“找两数之和能被 K 整除”转化为“一次遍历统计余数配对”。  
- **适用的类似题型**  
  1. *Count Pairs That Form a Complete Day*（第一版，只要 `hours[i] + hours[j]` 能被 24 整除）。  
  2. *Pairs of Songs With Total Durations Divisible by 60*（LeetCode 1010），求歌曲时长之和能被 60 整除的对数。  
  3. *Number of Pairs of Integers with Sum Divisible by K*（通用版），求任意 `K` 的情况。  
- **一句话总结解题钥匙**：**“把数先映射到余数，再用计数表直接找配对”**。

---

## 反思

- **第一反应**：看到“完整的一天”就是 24 的倍数，马上想到要判断 `(a + b) % 24 == 0`，于是想到了两层循环的暴力枚举。  
- **最容易踩的坑**  
  1. **余数为 0 的配对**：`need = (24 - r) % 24` 必须再取一次模，防止 `r = 0` 时得到 24（数组越界）。  
  2. **大数取余**：`hours[i]` 可达 `10⁹`，直接相加可能超出 Python 整数范围（虽然 Python 自动大整数），但仍应先取余再相加，避免不必要的开销。  
  3. **计数溢出**：答案最大可能是 `n*(n-1)/2`，在 Python 中整数无限大，但在其他语言需要使用 `long long`。  
- **下次遇到同类题**：第一步想到 **“把所有数先映射到模 K 的余数，然后用哈希表/数组统计出现次数，配对时直接查找需要的余数”**，这样就能把二次方降到线性。