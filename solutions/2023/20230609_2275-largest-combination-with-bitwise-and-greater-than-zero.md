# #2275. 最大组合使按位与大于零 / Largest Combination With Bitwise AND Greater Than Zero

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation、Counting · [LeetCode 链接](https://leetcode.com/problems/largest-combination-with-bitwise-and-greater-than-zero/)

---

## 题目（英文原版）

**Description**

The bitwise AND of an array nums is the bitwise AND of all integers in nums.
You are given an array of positive integers candidates. Compute the bitwise AND for all possible combinations of elements in the candidates array.
Return the size of the largest combination of candidates with a bitwise AND greater than 0.

**Examples**

**Example 1:**

```
Input: candidates = [16,17,71,62,12,24,14]
Output: 4
Explanation: The combination [16,17,62,24] has a bitwise AND of 16 & 17 & 62 & 24 = 16 > 0.
The size of the combination is 4.
It can be shown that no combination with a size greater than 4 has a bitwise AND greater than 0.
Note that more than one combination may have the largest size.
For example, the combination [62,12,24,14] has a bitwise AND of 62 & 12 & 24 & 14 = 8 > 0.
```

**Example 2:**

```
Input: candidates = [8,8]
Output: 2
Explanation: The largest combination [8,8] has a bitwise AND of 8 & 8 = 8 > 0.
The size of the combination is 2, so we return 2.
```

**Constraints**

- 1 <= candidates.length <= 105
- 1 <= candidates[i] <= 107

---

## 题目（中文翻译）

**题目描述**  
数组 `nums` 的按位与（bitwise AND）是 `nums` 中所有整数的按位与。  
给定一个正整数数组 `candidates`。请计算 `candidates` 中所有可能的元素组合的按位与。  
返回按位与大于 `0` 的最大组合的大小。

**示例 1**  
```
Input: candidates = [16,17,71,62,12,24,14]
Output: 4
Explanation: 组合 [16,17,62,24] 的按位与为 16 & 17 & 62 & 24 = 16 > 0。  
该组合的大小为 4。  
可以证明不存在大小大于 4 且按位与大于 0 的组合。  
注意可能有不止一个组合拥有相同的最大大小，例如组合 [62,12,24,14] 的按位与也满足条件。
```

**示例 2**  
```
Input: candidates = [8,8]
Output: 2
Explanation: 最大组合 [8,8] 的按位与为 8 & 8 = 8 > 0。  
该组合的大小为 2，故返回 2。
```

**约束条件**  
- `1 <= candidates.length <= 10^5`  
- `1 <= candidates[i] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的子集合都枚举一遍，计算它们的 **位与**（bitwise AND），看哪些子集合的结果大于 0，记录下最大的子集合大小。

- **数据结构**：我们只需要一个列表 `candidates`，以及在遍历时用到的临时变量 `cur_and`（保存当前子集合的位与）。可以把「子集合」想象成「从超市里挑选若干件商品」的所有可能挑选方式，枚举的过程就像把每一种挑选方式都写下来检查一次。
- **为什么正确**：因为我们把 **所有** 子集合都检查了一遍，任何满足「位与 > 0」的组合都会被发现，最大的自然也就找到了。

> 但是这相当于「把每本书的每一页都读一遍」——时间会爆炸。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def largestCombination_bruteforce(candidates: List[int]) -> int:
    n = len(candidates)
    best = 0                               # 记录目前找到的最大组合大小

    # 枚举子集合的大小 1 … n
    for size in range(1, n + 1):
        # itertools.combinations 会生成所有 size 个元素的子集合
        for subset in combinations(candidates, size):
            cur_and = subset[0]             # 先把第一个数放进 cur_and
            for num in subset[1:]:          # 依次与后面的数做 AND
                cur_and &= num
                if cur_and == 0:            # 只要出现 0，就不可能 >0，提前退出
                    break
            if cur_and > 0:                 # 位与大于 0，说明这是合法组合
                best = max(best, size)      # 更新最大大小
    return best
```

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  解释：子集合的总数是 `2^n`（每个元素选或不选），对每个子集合我们最多要遍历 `n` 次来计算位与。对 n=20 以上已经不可接受，等价于「指数级」增长。
- **空间复杂度**：`O(n)`（递归栈/迭代时保存的临时子集合）  
  只需要存放当前子集合的元素，和输入数组大小同阶。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「枚举所有子集合」。  
观察位与的性质：

> **位与 > 0** 当且仅当 **存在至少一个二进制位** 在组合里所有数的该位都是 `1`。  

也就是说，只要我们找到一个二进制位 `k`，使得 **所有选中的数在第 k 位都是 1**，整个组合的位与就一定大于 0（该位的 AND 为 1，其他位随便）。

所以我们不必枚举子集合，只要统计「在同一位上都是 1」的数有多少个，就能得到一个合法组合的最大可能大小。

具体步骤：

1. **遍历所有数字**，对每个二进制位（最多到 24 位，因为 `candidates[i] ≤ 10^7 < 2^24`）检查该位是否为 1。  
   - 如果是，就把该位对应的计数器 `cnt[bit]` 加 1。  
   - 把「计数器」想象成「字典」或「查字典」：键是位的位置，值是出现 1 的次数。
2. 最后答案就是 **所有计数器的最大值**。因为对应的那一位上出现 1 的数字集合本身已经满足「每个数的该位都是 1」，它们的位与必定大于 0，且不可能再加入其他不满足该位为 1 的数而保持位与 > 0。

> 这样我们把原来「指数」的问题压缩成了「线性」的统计问题，只需一次遍历数组、一次遍历位数。

#### 代码（Python）

```python
from typing import List

def largestCombination(candidates: List[int]) -> int:
    """
    返回能够得到位与 > 0 的最大组合大小。
    思路：统计每一位上为 1 的数字个数，最大值即为答案。
    """
    # 由于 candidates[i] <= 10^7 < 2^24，最多只需要看 0~23 位
    MAX_BITS = 24
    cnt = [0] * MAX_BITS          # cnt[i] 记录第 i 位为 1 的数字有多少个

    for num in candidates:
        # 只检查到最高位即可，使用位运算快速判断每一位是否为 1
        bit = 0
        while num:                # 当 num 为 0 时，后面的高位必然都是 0，直接结束
            if num & 1:           # 当前最低位是 1 吗？(num & 1) 为 1 表示是
                cnt[bit] += 1
            num >>= 1             # 右移一位，检查下一位
            bit += 1

    # 最大的计数即为能够组成的最大合法组合大小
    return max(cnt)
```

#### 复杂度  

- **时间复杂度**：`O(n * B)`，其中 `n = len(candidates)`，`B = 24` 为位数常数。  
  解释：我们遍历每个数字，对每个数字最多检查 24 次（因为数字 ≤ 2^24），相当于「线性」时间。对普通人来说，这相当于「一次走遍所有商品」的速度。
- **空间复杂度**：`O(B)`，只用了一个长度为 24 的数组存计数。  
  相当于「只需要一张小纸条」来记录每一位的出现次数，几乎不占内存。

---

## 心得

- **核心技巧**：**位与 > 0 等价于“某一位全为 1”，因此只需统计每个位出现 1 的次数**。  
- **适用题型**  
  1. “Maximum Subset Size With Bitwise AND > 0” 这类直接涉及位与的最大子集问题。  
  2. “Maximum Subset Size With Bitwise OR < K” 类似的位运算统计题（把注意力放在特定位的分布上）。  
  3. “Largest Subset With Common Bit” 这类要求子集在某个位上保持相同的题目。
- **一句话总结**：**把位运算的全局约束转化为“每个位独立计数”，最大计数即为答案**。

---

## 反思

- **第一反应**：直接想到枚举子集合，想要穷举检查所有组合是否满足位与 > 0。  
- **最容易踩的坑**  
  - 忽视 **位数上限**：若不限制位数，上述计数会遍历到 31 位甚至 64 位，仍然是 O(n·bits) 但会浪费时间。  
  - **边界条件**：当所有数字都是 0（题目保证正整数，但若改为非负）时，所有计数均为 0，需要返回 0 而不是错误。  
  - **重复数字**：计数自然会把重复的数字算进去，这正是我们想要的，不需要额外去重。  
- **下次类似题**：第一步先 **思考位运算的全局约束能否拆成“每个位独立统计”**，如果能，就立刻转向计数/哈希表方案，而不是暴力枚举。