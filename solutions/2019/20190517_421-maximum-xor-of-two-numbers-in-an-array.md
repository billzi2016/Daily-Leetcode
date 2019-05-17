# #421. 两数之间的最大异或 / Maximum XOR of Two Numbers in an Array

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation、Trie · [LeetCode 链接](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.

**Examples**

**Example 1:**

```
Input: nums = [3,10,5,25,2,8]
Output: 28
Explanation: The maximum result is 5 XOR 25 = 28.
```

**Example 2:**

```
Input: nums = [14,70,53,83,49,91,36,80,92,51,66,70]
Output: 127
```

**Constraints**

- 1 <= nums.length <= 2 * 105
- 0 <= nums[i] <= 231 - 1

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回 `nums[i] XOR nums[j]` 的最大结果，其中 `0 <= i <= j < n`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例：**  

**示例 1:**  
输入: `nums = [3,10,5,25,2,8]`  
输出: `28`  
解释: 最大的结果是 `5 XOR 25 = 28`。

**示例 2:**  
输入: `nums = [14,70,53,83,49,91,36,80,92,51,66,70]`  
输出: `127`

**约束条件：**  
- `1 <= nums.length <= 2 * 10^5`  
- `0 <= nums[i] <= 2^31 - 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组里每两个数都算一次 XOR，记录最大的那个。  
- **数据结构**：只需要一个普通的 Python `list`，因为我们只遍历元素，不需要额外的结构。  
- **生活化类比**：把数组想成一排小灯泡，每两个灯泡之间可以点亮一种“特殊颜色”（XOR 结果），我们把所有可能的颜色都试一遍，挑出最亮的那种。  
- **正确性**：因为我们把所有合法的 (i, j) 对都枚举了，最大的 XOR 必然出现在枚举的结果里。  

#### 代码（Python）  

```python
from typing import List

def findMaximumXOR_bruteforce(nums: List[int]) -> int:
    """
    暴力枚举所有 i、j（i <= j），返回最大的 XOR 值
    """
    n = len(nums)
    max_xor = 0                     # 用来保存当前最大的 XOR
    for i in range(n):
        for j in range(i, n):       # 只需要 i <= j，避免重复计算
            cur = nums[i] ^ nums[j] # ^ 是 Python 中的按位异或
            if cur > max_xor:       # 如果这一次的结果更大，就更新
                max_xor = cur
    return max_xor
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - “O” 读作“大写欧”，表示**数量级**。`n²` 意味着如果数组长度翻倍，运算次数会变成原来的 **四倍**，因此在 `n` 很大时会非常慢。  
- **空间复杂度**：`O(1)`。只用了几个额外的变量，和数组大小无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于两层循环**——我们在重复比较同一个数的高位信息。  
我们可以利用**位运算的特性**，从最高位（第 31 位）往低位逐步确定答案的每一位。  

1. **最高位先确定**：如果我们已经知道答案的前几位（从高到低），那么在第 `k` 位上，答案要么是 `0` 要么是 `1`。我们先假设它是 `1`，看看是否真的能做到。  
2. **前缀集合**：遍历数组，把每个数的 **前 k 位**（即把低于第 k 位的全部清零）保存到一个集合（类似查字典的哈希表，key 是前缀，value 是“出现过”。）  
3. **配对检查**：设当前假设的答案前缀为 `candidate`（最高位已经确定好），我们想知道是否存在两个数 `a`、`b`，使得 `a ^ b` 的前 `k` 位正好等于 `candidate`。  
   - 这等价于：在集合中找 `a_prefix`，使得 `a_prefix ^ candidate` 也在集合里（因为 `b_prefix = a_prefix ^ candidate`）。  
   - 如果能找到这样的一对前缀，说明第 `k` 位可以是 `1`，否则只能是 `0`。  

把上述过程从第 31 位一直做到第 0 位，就得到最大 XOR。  

**核心数据结构**：  
- **哈希集合（set）**：像查字典一样，`O(1)` 时间判断一个前缀是否出现过。  
- **Trie（字典树）**：另一种实现思路是把每个数的二进制位插入 Trie，遍历时总是尝试走与当前位相反的分支，以期得到更大的 XOR。这里我们用集合实现，代码更简洁，思路更易懂。  

**类比**：把每个数的前缀想成一本“电话本”，我们在找“两个电话号码的前几位互为补码”。如果找得到，就说明可以把这几位都设成 `1`（更亮的颜色）。

#### 代码（Python）  

```python
from typing import List

def findMaximumXOR(nums: List[int]) -> int:
    """
    使用前缀集合的贪心 + 位运算，时间 O(31 * n) ≈ O(n)
    """
    max_xor = 0          # 当前已经确定的最大 XOR（从高位往低位逐步填充）
    mask = 0             # 用来取前缀的掩码，例如 mask=111...1000 表示保留高位

    # 从最高位（第31位）到最低位（第0位）依次尝试
    for k in range(31, -1, -1):
        mask |= (1 << k)                 # 把第 k 位加入掩码，mask 逐渐变宽
        prefixes = set()                 # 存放所有数的前 k 位前缀
        for num in nums:
            prefixes.add(num & mask)     # 只保留高于 k 位的部分

        # 假设第 k 位可以是 1，构造一个候选答案
        candidate = max_xor | (1 << k)

        # 检查是否存在两个前缀 a、b，使得 a ^ b == candidate
        found = False
        for p in prefixes:
            if (p ^ candidate) in prefixes:   # 如果 b = p ^ candidate 也在集合中
                found = True
                break

        if found:                         # 能实现，则把第 k 位定为 1
            max_xor = candidate
        # 否则第 k 位只能是 0，max_xor 保持不变

    return max_xor
```

#### 复杂度  

- **时间复杂度**：`O(31 * n) ≈ O(n)`。  
  - 我们遍历 31 次（因为整数最多到第 31 位），每次遍历整个数组并做 `O(1)` 的哈希操作，整体与 `n` 成线性关系。  
- **空间复杂度**：`O(n)`。  
  - 每一轮需要存储所有数的前缀，最坏情况下前缀数量等于数组长度 `n`。  

相比暴力的 `O(n²)`，线性时间在 `n` 达到 2×10⁵ 时可以在毫秒级完成。

---

## 心得  

- **核心技巧**：**位前缀贪心 + 哈希集合**（或 Trie）能够在不枚举所有对的情况下，逐位确定最大异或。  
- **适用题型**：  
  1. “Maximum XOR of Two Numbers in an Array”（本题）  
  2. “Maximum XOR With an Element From Array” （LeetCode 1707）  
  3. “Maximum XOR Subarray” （LeetCode 1803）  
- **解题钥匙**：**从高位往低位贪心**，每一步都只判断“是否有可能把这一位设为 1”。  

---

## 反思  

- **第一反应**：直接写两层循环枚举所有配对，得到答案。  
- **最容易踩的坑**：  
  - **位数范围**：题目说 `0 <= nums[i] <= 2³¹‑1`，所以最高位是第 31 位（从 0 开始计数），不能漏掉。  
  - **前缀集合的更新**：每轮都要重新建立集合，不能把前一轮的前缀直接复用，因为掩码已经变宽了。  
  - **整数溢出**：在 Python 中整数不溢出，但在其他语言（如 C/C++）需要注意使用 64 位或无符号整数。  
- **下次思路**：看到 “求最大 XOR” 时，立刻想到 **按位贪心 + 前缀哈希 / Trie**，先确定最高位能否为 1，再往低位推进。这样可以把指数级的枚举压到线性时间。