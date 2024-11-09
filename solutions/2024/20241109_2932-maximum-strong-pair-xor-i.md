# #2932. 最大强配对异或 I / Maximum Strong Pair XOR I

> 难度：简单 · 标签：Array、Hash Table、Bit Manipulation、Trie、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-strong-pair-xor-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. A pair of integers x and y is called a strong pair if it satisfies the condition:
You need to select two integers from nums such that they form a strong pair and their bitwise XOR is the maximum among all strong pairs in the array.
Return the maximum XOR value out of all possible strong pairs in the array nums.
Note that you can pick the same integer twice to form a pair.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: 7
Explanation: There are 11 strong pairs in the array nums: (1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4), (3, 5), (4, 4), (4, 5) and (5, 5).
The maximum XOR possible from these pairs is 3 XOR 4 = 7.
```

**Example 2:**

```
Input: nums = [10,100]
Output: 0
Explanation: There are 2 strong pairs in the array nums: (10, 10) and (100, 100).
The maximum XOR possible from these pairs is 10 XOR 10 = 0 since the pair (100, 100) also gives 100 XOR 100 = 0.
```

**Example 3:**

```
Input: nums = [5,6,25,30]
Output: 7
Explanation: There are 6 strong pairs in the array nums: (5, 5), (5, 6), (6, 6), (25, 25), (25, 30) and (30, 30).
The maximum XOR possible from these pairs is 25 XOR 30 = 7 since the only other non-zero XOR value is 5 XOR 6 = 3.
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。如果一对整数 `x` 和 `y` 满足以下条件，则称它们为 **强配对（strong pair）**：  

（此处应填写具体的条件描述）

你需要从 `nums` 中挑选两个整数，使它们构成强配对，并且它们的按位异或（bitwise XOR）在所有强配对中取得最大值。返回数组 `nums` 中所有可能的强配对所能得到的最大 XOR 值。  

注意，你可以选取同一个整数两次来组成配对。

## 示例

### 示例 1  
**输入**  
```text
nums = [1,2,3,4,5]
```  
**输出**  
```text
7
```  
**解释**  
数组 `nums` 中共有 11 对强配对：`(1,1)`, `(1,2)`, `(2,2)`, `(2,3)`, `(2,4)`, `(3,3)`, `(3,4)`, `(3,5)`, `(4,4)`, `(4,5)` 和 `(5,5)`。  
这些配对中能够得到的最大 XOR 为 `3 XOR 4 = 7`。

### 示例 2  
**输入**  
```text
nums = [10,100]
```  
**输出**  
```text
0
```  
**解释**  
数组 `nums` 中共有 2 对强配对：`(10,10)` 和 `(100,100)`。  
这些配对中能够得到的最大 XOR 为 `10 XOR 10 = 0`（`(100,100)` 也得到 `100 XOR 100 = 0`）。

### 示例 3  
**输入**  
```text
nums = [5,6,25,30]
```  
**输出**  
```text
7
```  
**解释**  
数组 `nums` 中共有 6 对强配对：`(5,5)`, `(5,6)`, `(6,6)`, `(25,25)`, `(25,30)` 和 `(30,30)`。  
这些配对中能够得到的最大 XOR 为 `25 XOR 30 = 7`，因为唯一的其他非零 XOR 值是 `5 XOR 6 = 3`。

## 约束条件

- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的办法就是把数组里所有可能的两两组合都枚举一遍，判断它们是否满足 **强对** 的条件，再把满足条件的组合的 `x ^ y`（按位异或）取最大即可。  

- **强对的定义**：`(x, y)` 是强对当且仅当  
  `max(x, y) ≤ 2 * min(x, y)`。  
  把它想象成“两个数的大小差距不超过它们的最小值的两倍”。  
- **数据结构**：只需要普通的 **列表**（array）和 **两层循环**，不需要额外的数据结构。  
- **为什么正确**：我们把**所有**合法的配对都检查了一遍，最大值自然不会错过。  

#### 代码（Python）

```python
from typing import List

def maximumStrongPairXor(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                     # 先把“同一个数配自己” 的情况记为 0
    for i in range(n):
        for j in range(i, n):   # i <= j 让每对只算一次，i==j 表示配自己
            x, y = nums[i], nums[j]
            # 判断是否是强对
            if max(x, y) <= 2 * min(x, y):
                ans = max(ans, x ^ y)   # 计算 XOR 并取最大
    return ans
```

> **关键行注释**  
> - `for j in range(i, n)`: 只遍历下三角矩阵，避免重复计数。  
> - `if max(x, y) <= 2 * min(x, y)`: 正是强对的判定条件。  
> - `ans = max(ans, x ^ y)`: 记录当前最大的异或值。  

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  大白话：如果数组里有 50 个数，我们最多要比较 50×50/2≈1250 次，这在本题的约束（n ≤ 50）里完全可以接受。  
- **空间复杂度**：`O(1)`。只用了几个额外的变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两层循环**——每次都要遍历已经检查过的所有元素。  
观察强对的条件 `max ≤ 2·min`，如果把数组 **先排个序**，则对每个数 `nums[r]`，只会和 **左边** 那些不超过 `2·nums[r]` 的数形成强对。  

这正好可以用 **滑动窗口** + **二进制 Trie（前缀树）** 来优化：

1. **排序**：把 `nums` 从小到大排好序。  
2. **滑动窗口**：维护一个左指针 `l`，保证窗口 `[l, r)` 中的所有数都满足 `nums[r] ≤ 2·nums[l]`（即窗口里的每个数和 `nums[r]` 都是强对）。  
   - 当 `nums[r]` 超出窗口左端的两倍时，左端的数就不再可能和后面的数构成强对，需要 **从 Trie 中删除** 并左移 `l`。  
3. **Trie**：在窗口里存放所有候选数的二进制表示。  
   - 对当前数 `nums[r]`，在 Trie 中“贪心”寻找能够让异或值最大的数（每一位尽量选相反的比特）。  
   - 这样得到的 `max_xor` 就是 `nums[r]` 与窗口中任意合法数的最大异或。  
4. **更新答案**：`ans = max(ans, max_xor)`。  
5. **插入当前数**：把 `nums[r]` 加入 Trie，供后面的数使用。  

> **为什么快**：每个数只会被 **插入一次、删除一次、查询一次**，每次操作的代价是遍历它的二进制位（最多 31 位），总体是 `O(n·L)`，其中 `L` 是整数的位数。对本题的 `n ≤ 50` 来说，这几乎是瞬间完成。  

#### 代码（Python）

```python
from typing import List

class TrieNode:
    __slots__ = ("child", "cnt")
    def __init__(self):
        # child[0] 为比特 0 的子树，child[1] 为比特 1 的子树
        self.child = [None, None]
        # cnt 统计经过该节点的数的个数，方便删除
        self.cnt = 0

class BinaryTrie:
    def __init__(self, max_bit: int = 31):
        self.root = TrieNode()
        self.max_bit = max_bit                # 处理到哪一位（0-index）

    def insert(self, num: int) -> None:
        node = self.root
        node.cnt += 1
        for k in range(self.max_bit, -1, -1):
            b = (num >> k) & 1
            if not node.child[b]:
                node.child[b] = TrieNode()
            node = node.child[b]
            node.cnt += 1

    def erase(self, num: int) -> None:
        """从 Trie 中删除一次出现的 num（保证一定存在）"""
        node = self.root
        node.cnt -= 1
        for k in range(self.max_bit, -1, -1):
            b = (num >> k) & 1
            nxt = node.child[b]
            nxt.cnt -= 1
            # 若子节点计数归零，直接回收（省空间）
            if nxt.cnt == 0:
                node.child[b] = None
                return
            node = nxt

    def max_xor(self, num: int) -> int:
        """在 Trie 中找出与 num 异或值最大的数"""
        node = self.root
        if node.cnt == 0:          # Trie 为空时返回 0（不会出现，但防御性写法）
            return 0
        ans = 0
        for k in range(self.max_bit, -1, -1):
            b = (num >> k) & 1
            # 想让异或位为 1，就尽量走相反的比特
            want = 1 - b
            if node.child[want] and node.child[want].cnt > 0:
                ans |= (1 << k)          # 该位异或成功，记 1
                node = node.child[want]
            else:
                node = node.child[b]     # 只能走相同的比特，异或该位为 0
        return ans

def maximumStrongPairXor(nums: List[int]) -> int:
    nums.sort()                         # 先排序，方便滑动窗口
    trie = BinaryTrie(max_bit=7)        # 100 < 2^7，7 位足够；也可以用 31 位
    ans = 0
    l = 0                               # 窗口左端

    for r, val in enumerate(nums):
        # 确保窗口内的最左边元素满足强对条件：val <= 2 * nums[l]
        while l < r and val > 2 * nums[l]:
            trie.erase(nums[l])         # 左端元素不再可能与后面的数配对，删掉
            l += 1

        # 此时窗口 [l, r) 中的每个数都能和 val 组成强对
        if trie.root.cnt > 0:           # 窗口非空，才需要查询
            cur = trie.max_xor(val)    # 在窗口里找与 val 异或最大的数
            ans = max(ans, cur)

        trie.insert(val)                # 把当前数加入窗口，供后面的数使用

    return ans
```

> **关键行中文注释**  
> - `while l < r and val > 2 * nums[l]:` 确保左端的数仍然满足 “不超过两倍” 的限制。  
> - `trie.max_xor(val)` 在当前窗口里挑出能让异或最大的一位数。  
> - `trie.insert(val)` 把当前数加入窗口，后面的数就可以和它配对。  

#### 复杂度  

- **时间复杂度**：`O(n · L)`，其中 `L` 是整数的二进制位数（本题 `L ≤ 7`，实际更快）。  
  相比暴力的 `O(n²)`，这里把“每次遍历所有已出现的数” 换成了 “遍历固定的 7~31 位”，大幅提升。  
- **空间复杂度**：`O(n · L)` 用于存放 Trie。因为每插入一个数至多会创建 `L` 个节点，最多 `n·L` 个节点。  

---  

## 心得  

- **核心技巧**：**利用数值大小的比例限制**（`max ≤ 2·min`）把问题转化为 “在有序数组中，左端指针只会单调右移”，进而配合 **二进制 Trie** 快速求最大异或。  
- **适用场景**：  
  1. “在满足某种区间/比例约束的数对中求最大 XOR”。  
  2. “给定一个窗口大小或范围，要求窗口内两数的最大异或”。  
  3. “在一组数里寻找满足条件的两数，使得某个位运算（如 XOR、AND、OR）值最大”。  
- **一句话总结解题钥匙**：**先把 “合法范围” 用滑动窗口限制，再用 Trie 把 “最大异或” 的贪心搜索抽象出来**。  

---  

## 反思  

- **第一反应**：看到 “强对” 只涉及数值大小，立刻想到 **枚举所有组合**（暴力）是最直接的验证方法。  
- **最容易踩的坑**：  
  - 漏掉 **同一个数配自己** 的情况（它的 XOR 为 0，必须作为基准）。  
  - 误把条件写成 `abs(x - y) ≤ 1` 或 `x & y == x`，导致错误的合法集合。  
  - 在实现 Trie 删除时忘记维护计数，导致后续查询出现已经被“踢出”窗口的数。  
- **下次类似题目**：第一步先 **明确数值约束能否转化为有序区间**（如 `max ≤ k·min`），随后考虑 **滑动窗口 + 高效位运算结构**（Trie）来做 “最大/最小” 的查询。