# #1803. 区间异或计数 / Count Pairs With XOR in a Range

> 难度：困难 · 标签：Array、Bit Manipulation、Trie · [LeetCode 链接](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/)

---

## 题目（英文原版）

**Description**

Given a (0-indexed) integer array nums and two integers low and high, return the number of nice pairs.
A nice pair is a pair (i, j) where 0 <= i < j < nums.length and low <= (nums[i] XOR nums[j]) <= high.

**Examples**

**Example 1:**

```
Input: nums = [1,4,2,7], low = 2, high = 6
Output: 6
Explanation: All nice pairs (i, j) are as follows:
    - (0, 1): nums[0] XOR nums[1] = 5 
    - (0, 2): nums[0] XOR nums[2] = 3
    - (0, 3): nums[0] XOR nums[3] = 6
    - (1, 2): nums[1] XOR nums[2] = 6
    - (1, 3): nums[1] XOR nums[3] = 3
    - (2, 3): nums[2] XOR nums[3] = 5
```

**Example 2:**

```
Input: nums = [9,8,4,2,1], low = 5, high = 14
Output: 8
Explanation: All nice pairs (i, j) are as follows:
​​​​​    - (0, 2): nums[0] XOR nums[2] = 13
    - (0, 3): nums[0] XOR nums[3] = 11
    - (0, 4): nums[0] XOR nums[4] = 8
    - (1, 2): nums[1] XOR nums[2] = 12
    - (1, 3): nums[1] XOR nums[3] = 10
    - (1, 4): nums[1] XOR nums[4] = 9
    - (2, 3): nums[2] XOR nums[3] = 6
    - (2, 4): nums[2] XOR nums[4] = 5
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= nums[i] <= 2 * 104
- 1 <= low <= high <= 2 * 104

---

## 题目（中文翻译）

给定一个 **0 起始索引** 的整数数组 `nums` 和两个整数 `low`、`high`，返回满足条件的「好对」的数量。

「好对」定义为满足 `0 <= i < j < nums.length` 且 `low <= (nums[i] XOR nums[j]) <= high` 的下标对 `(i, j)`，其中 **XOR** 为按位异或运算。

**示例 1**

```text
Input: nums = [1,4,2,7], low = 2, high = 6
Output: 6
Explanation: 所有满足条件的好对 (i, j) 如下：
    - (0, 1): nums[0] XOR nums[1] = 5 
    - (0, 2): nums[0] XOR nums[2] = 3
    - (0, 3): nums[0] XOR nums[3] = 6
    - (1, 2): nums[1] XOR nums[2] = 6
    - (1, 3): nums[1] XOR nums[3] = 3
    - (2, 3): nums[2] XOR nums[3] = 5
```

**示例 2**

```text
Input: nums = [9,8,4,2,1], low = 5, high = 14
Output: 8
Explanation: 所有满足条件的好对 (i, j) 如下：
    - (0, 2): nums[0] XOR nums[2] = 13
    - (0, 3): nums[0] XOR nums[3] = 11
    - (0, 4): nums[0] XOR nums[4] = 8
    - (1, 2): nums[1] XOR nums[2] = 12
    - (1, 3): nums[1] XOR nums[3] = 10
    - (1, 4): nums[1] XOR nums[4] = 9
    - (2, 3): nums[2] XOR nums[3] = 6
    - (2, 4): nums[2] XOR nums[4] = 5
```

**约束条件**

- `1 <= nums.length <= 2 * 10^4`
- `1 <= nums[i] <= 2 * 10^4`
- `1 <= low <= high <= 2 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的下标对** `(i, j)`，计算 `nums[i] XOR nums[j]`，检查它是否落在 `[low, high]` 区间内，满足条件就计数。

- **数据结构**：只需要一个普通的列表 `nums`，遍历时用两个嵌套的 `for` 循环。  
- **类比**：把数组想象成一排学生，老师要检查每两位学生的“秘密编号”（XOR）是否在规定的范围内。老师只能一个一个地让两位学生站出来比较，这就是暴力枚举。  
- **正确性**：因为我们把 **所有** `i < j` 的组合都检查了一遍，只要满足条件就计数，所以一定不会漏掉任何合法的配对。  

#### 代码（Python）

```python
from typing import List

def countPairs_bruteforce(nums: List[int], low: int, high: int) -> int:
    n = len(nums)
    ans = 0
    # 外层循环固定左边的下标 i
    for i in range(n):
        # 内层循环遍历右边的下标 j（只能比 i 大）
        for j in range(i + 1, n):
            xor_val = nums[i] ^ nums[j]          # 计算异或
            if low <= xor_val <= high:           # 判断是否在区间内
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - “`n²`” 可以想象成 **每个人要和后面所有人都比一次**，如果有 10 个人，最多要比较 45 次；如果有 10,000 人，比较次数会变成约 50,000,000 次，显然会超时。  
- **空间复杂度**：`O(1)`。只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每一次 XOR 都要遍历一次所有已经出现的数**，导致二次方时间。  
我们需要一种 **快速查询**：在遍历数组时，能够在 **对数级别**（或者常数级别）得到“已有的数中，有多少个与当前数的 XOR ≤ K”。  

这正好可以使用 **二进制前缀树（Trie）** 来实现：

1. **把整数看成二进制位的序列**（最高位到最低位）。  
2. 在 Trie 中每条路径对应一个已插入的数的二进制表示。  
3. 对于当前数 `x`，我们想统计已有数 `y` 满足 `x XOR y ≤ K`。  
   - 从最高位开始比较 `x` 的第 `b` 位和 `K` 的第 `b` 位。  
   - 若 `K` 的第 `b` 位是 **0**，则 `x XOR y` 在这一位必须也为 0，意味着 `y` 必须在 Trie 中走 **与 `x` 相同的位**；否则若 `K` 的第 `b` 位是 **1**，则有两种情况：  
        a. 让 `x XOR y` 在该位为 0（即 `y` 与 `x` 同位），此时后面的位可以随意，直接把对应子树的计数加到答案中。  
        b. 让 `x XOR y` 在该位为 1（即 `y` 与 `x` 异位），此时必须继续在对应子树里继续比较下一位。  
4. 通过上述过程，我们可以在 **O(位数)**（这里位数 ≤ 15，因为 `nums[i] ≤ 2·10⁴ < 2¹⁵`）得到满足条件的已有数的数量。  

因为题目要求 **low ≤ XOR ≤ high**，我们可以利用**计数函数**：

```
countPairs(nums, low, high) = countPairsWithXorLeq(high) - countPairsWithXorLeq(low-1)
```

即只需要实现 “**统计所有 i < j 且 XOR ≤ K**” 的函数。

**Trie 结构**：

```text
TrieNode:
    child[0] -> 指向表示当前位为 0 的子树
    child[1] -> 指向表示当前位为 1 的子树
    cnt      -> 经过此节点的数的个数（用于快速统计子树大小）
```

**类比**：把 Trie 想成一本**二进制字典**，每本书的页码就是数的二进制。要找“所有书的页码与当前页码异或不超过 K”，我们可以按位翻阅字典，利用 K 的每一位指示我们可以“跳过去”多少本书，而不必逐本检查。

#### 代码（Python）

```python
from typing import List

class TrieNode:
    __slots__ = ('child', 'cnt')
    def __init__(self):
        # child[0] 为位 0 的子节点，child[1] 为位 1 的子节点
        self.child = [None, None]
        # cnt 表示有多少个数的前缀走到这里
        self.cnt = 0

class BinaryTrie:
    def __init__(self, bit_len: int = 15):
        self.root = TrieNode()
        self.bit_len = bit_len          # 最高位索引，15 够覆盖 2*10^4

    def insert(self, num: int) -> None:
        """把 num 的二进制位插入 Trie，同时更新每个节点的计数"""
        node = self.root
        for b in range(self.bit_len, -1, -1):   # 从高位到低位遍历
            cur_bit = (num >> b) & 1
            if not node.child[cur_bit]:
                node.child[cur_bit] = TrieNode()
            node = node.child[cur_bit]
            node.cnt += 1                       # 经过此节点的数增一

    def count_leq(self, num: int, limit: int) -> int:
        """
        统计已经插入的数中，有多少个 y 满足 (num XOR y) <= limit
        """
        node = self.root
        ans = 0
        for b in range(self.bit_len, -1, -1):
            if not node:
                break
            num_bit = (num >> b) & 1
            limit_bit = (limit >> b) & 1

            if limit_bit == 1:
                # 情形 a) 让 XOR 在此位为 0 -> y_bit 必须等于 num_bit
                # 对应的子树全部可以直接计入答案
                same_child = node.child[num_bit]
                if same_child:
                    ans += same_child.cnt

                # 情形 b) 让 XOR 在此位为 1 -> y_bit 必须与 num_bit 不同
                # 继续在 opposite 子树里检查更低位
                node = node.child[1 - num_bit]
            else:
                # limit_bit == 0，XOR 在此位只能为 0，必须走相同位的子树
                node = node.child[num_bit]
        return ans

def countPairs(nums: List[int], low: int, high: int) -> int:
    """
    主函数：利用 Trie 计算 XOR 在 [low, high] 区间的配对数量
    """
    # 位数取足以容纳题目上限 2*10^4 (< 2^15)
    trie = BinaryTrie(bit_len=15)
    ans = 0
    for x in nums:
        # 先统计已有数中满足条件的个数（i < 当前下标）
        ans += trie.count_leq(x, high) - trie.count_leq(x, low - 1)
        # 再把当前数插入 Trie，供后面的数使用
        trie.insert(x)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * L)`，其中 `n = len(nums)`，`L` 是整数的二进制位数（本题 `L ≤ 15`）。  
  - 对每个元素我们做两次 `count_leq`（各 `O(L)`）加一次 `insert`（`O(L)`），所以常数很小。相当于 **线性** 级别，远快于 `O(n²)`。  
- **空间复杂度**：`O(n * L)`，Trie 最多会存 `n` 个数的每一位路径，最多 `n * (L+1)` 个节点。  
  - 这里 `L` 很小，实际占用的内存约几百 KB，完全可接受。

---

## 心得

- **核心技巧**：利用 **二进制 Trie**（前缀树）快速统计满足 “XOR ≤ K” 的配对数。  
- **适用题型**：  
  1. **统计 XOR 在某区间的配对**（本题）。  
  2. **求数组中两数的最大 XOR**（LeetCode 421）。  
  3. **求子数组的前缀 XOR 满足某条件的计数**（如“子数组异或小于 K”）。  
- **一句话总结**：把 “数的异或 ≤ K” 转化为 **按位比较**，用 Trie 按位累加计数，避免枚举所有配对。

## 反思

- **第一反应**：看到“XOR 在区间”立刻想到 **枚举 + 判断**，因为 XOR 的性质不直观，容易忽略更高效的位运算结构。  
- **最容易踩的坑**：  
  - **位数选择**：若忘记把最高位设大 enough，会导致错误计数（高位被截断）。本题上限 `2·10⁴` 只需要 15 位。  
  - **low 为 0 时**：公式 `countLeq(high) - countLeq(low-1)` 中 `low-1` 可能为负数，需要在实现中保证 `count_leq(..., -1)` 返回 0（本实现自然满足，因为所有 limit 位都是 0，遍历时不会累计）。  
  - **插入顺序**：一定要先查询再插入当前数，防止把 `(i,i)` 计入答案。  
- **下次遇到同类题**：第一步想到 **“把区间计数转化为 ≤K 的计数差”**，然后搜索 **Trie / 前缀树** 这类 **按位统计** 的数据结构。