# #1707. 数组中元素的最大异或 / Maximum XOR With an Element From Array

> 难度：困难 · 标签：Array、Bit Manipulation、Trie · [LeetCode 链接](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of non-negative integers. You are also given a queries array, where queries[i] = [xi, mi].
The answer to the ith query is the maximum bitwise XOR value of xi and any element of nums that does not exceed mi. In other words, the answer is max(nums[j] XOR xi) for all j such that nums[j] <= mi. If all elements in nums are larger than mi, then the answer is -1.
Return an integer array answer where answer.length == queries.length and answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
Output: [3,3,7]
Explanation:
1) 0 and 1 are the only two integers not greater than 1. 0 XOR 3 = 3 and 1 XOR 3 = 2. The larger of the two is 3.
2) 1 XOR 2 = 3.
3) 5 XOR 2 = 7.
```

**Example 2:**

```
Input: nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
Output: [15,-1,5]
```

**Constraints**

- 1 <= nums.length, queries.length <= 105
- queries[i].length == 2
- 0 <= nums[j], xi, mi <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个仅包含非负整数的数组 `nums`。同时给定一个查询数组 `queries`，其中 `queries[i] = [xi, mi]`。  

第 `i` 个查询的答案是 `xi` 与 `nums` 中所有不超过 `mi` 的元素的按位异或（bitwise XOR）值的最大值。换句话说，答案为  

\[
\max_{j \;:\; nums[j] \le mi} (nums[j] \; \text{XOR} \; xi)
\]

如果 `nums` 中没有任何元素满足 `nums[j] ≤ mi`，则答案为 `-1`。  

返回一个整数数组 `answer`，其中 `answer.length == queries.length`，且 `answer[i]` 为第 `i` 个查询的答案。

---

**示例 1**

```text
Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
Output: [3,3,7]
Explanation:
1) 不大于 1 的元素只有 0 和 1。0 XOR 3 = 3，1 XOR 3 = 2，较大的值为 3。
2) 不大于 3 的元素有 0、1、2、3。1 XOR 2 = 3，得到的最大值为 3。
3) 不大于 6 的元素有 0、1、2、3、4，5 XOR 2 = 7，得到的最大值为 7。
```

**示例 2**

```text
Input: nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
Output: [15,-1,5]
```

---

**约束条件**

- `1 <= nums.length, queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= nums[j], xi, mi <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个查询都枚举一遍**：

1. 对于第 `i` 个查询 `[xi, mi]`，遍历整个数组 `nums`。  
2. 只保留满足 `nums[j] ≤ mi` 的元素。  
3. 对这些合法的元素计算 `nums[j] XOR xi`，取最大值。  
4. 如果根本没有合法元素，就把答案记成 `-1`。

> **类比**：把 `nums` 看成一本厚厚的电话簿，`mi` 像是“只能查到某个编号之前的号码”。我们逐行检查，找出所有符合条件的号码，再用 `xi`（相当于想要拨的目标号码）去和它们做异或，挑出最大的那一个。

**为什么能得到正确答案**  
因为我们没有漏掉任何可能的 `nums[j]`（只要它 ≤ `mi`），并且把所有合法的异或值都算了一遍，取最大自然就是答案。

**时间/空间分析**  

- 对每个查询我们要遍历 `nums`，`nums` 长度记为 `n`，查询数记为 `q`。  
- 时间复杂度就是 `O(q * n)`，在最坏情况下是 **10⁵ × 10⁵ = 10¹⁰**，远远超出 1 秒能接受的范围。  
- 只用了几个临时变量，空间复杂度是 `O(1)`（不计输出数组）。

> **大白话**：`O(q * n)` 就像让 10 万个人每人都检查 10 万本书，显然不可能在几秒内完成。

#### 代码（Python）

```python
from typing import List

def maximumXor_bruteforce(nums: List[int], queries: List[List[int]]) -> List[int]:
    ans = []
    for xi, mi in queries:               # 逐个处理查询
        best = -1                         # 记录当前查询的最大异或值，默认 -1
        for v in nums:                    # 暴力遍历所有 nums
            if v <= mi:                   # 只考虑不超过 mi 的数
                cur = v ^ xi              # 计算异或
                if cur > best:            # 维护最大值
                    best = cur
        ans.append(best)                  # 把答案加入结果列表
    return ans
```

#### 复杂度

- **时间复杂度**：`O(q * n)`  
  - `q` 是查询数量，`n` 是数组长度。每个查询都要遍历整个 `nums`。
- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只用了几个整型变量来保存临时值。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次查询都要重新遍历 `nums`**。  
如果我们能让每个查询只“看到”已经满足 `≤ mi` 条件的数字，而不必每次都遍历全部，就可以把时间降下来。  

**关键观察**  

- 对于固定的 `xi`，要让 `xi XOR y` 最大，需要在最高位就把两者的位相反（因为 1 > 0）。于是我们希望在 **每一位** 都能挑选一个与 `xi` 对应位相反的数。  
- 这正好可以用 **Trie（前缀树）** 来实现：把所有合法的 `nums` 按二进制位从最高位到最低位插入 Trie。查询时，沿着与 `xi` 位相反的方向走（如果有分支），否则只能走相同方向。这样走完 31（或 30）位后得到的就是最大可能的异或值。

**如何保证 Trie 里只放合法的数字**  

1. **先把 `nums` 排序**（升序）。  
2. **把查询也排序**，但排序的依据是 `mi`（上限），即把 `mi` 小的查询放前面。  
3. 维护一个指针 `pos`，指向 `nums` 中还未加入 Trie 的位置。  
4. 当处理某个查询 `[xi, mi]` 时，**把所有 `nums[pos] ≤ mi` 的元素全部插入 Trie**，并把 `pos` 向后移动。  
5. 这样，当前查询对应的 Trie 正好只包含 **不超过 `mi` 的数**，后面的查询只会往里继续加入更大的数，永不删除。

> **类比**：想象有一排装满水果的盒子（`nums` 已排好序），我们有一只篮子（Trie）。每次来一个顾客（查询），他只想挑 **重量 ≤ mi** 的水果。我们把所有符合重量的水果从盒子里倒进篮子，之后再让顾客挑选能让味道（异或）最好的水果。下一个顾客的重量上限更大时，只需要把新符合的水果再倒进篮子即可，之前的水果自然仍然在篮子里。

**Trie 结构**  

- 每个节点有两个子节点，分别对应二进制位 `0` 和 `1`。  
- 为了省空间，我们只存 **指针**（`None` 或子节点对象），不必记录出现次数，因为只要有路径就说明有对应的数。

**查询过程**（找最大异或）  

- 从最高位（这里取 30 位，因为 `10⁹ < 2³⁰`）开始。  
- 设 `bit = (xi >> k) & 1` 为当前位的值。我们希望走向 `1-bit`（相反位），因为 `1 XOR 0 = 1` 能让该位贡献 1。  
- 如果相反位的子节点存在，就往那边走，并把答案的该位设为 1（`ans |= 1 << k`）。  
- 否则只能走相同位的子节点，答案该位为 0。  
- 最终累计的 `ans` 就是 `xi` 与 Trie 中某个数的最大异或值。

**整体时间**  

- 排序：`O(n log n + q log q)`。  
- 插入每个 `nums` 元素到 Trie：每个元素最多 31 次节点创建，整体 `O(n * 31)`。  
- 每个查询在 Trie 中走 31 步，整体 `O(q * 31)`。  
- 常数 31 可以看成常数，故总体是 `O((n + q) log (n + q))`，足够快。

#### 代码（Python）

```python
from typing import List
import sys

# ---------- Trie 节点 ----------
class TrieNode:
    __slots__ = ('child',)          # 只保留 child 两个指针，节省内存

    def __init__(self):
        # child[0] 表示二进制 0 分支，child[1] 表示二进制 1 分支
        self.child = [None, None]

# ---------- 核心函数 ----------
def maximumXor(nums: List[int], queries: List[List[int]]) -> List[int]:
    # 1. 对 nums 排序
    nums.sort()
    n = len(nums)

    # 2. 把查询包装成 (mi, xi, original_index) 并按 mi 排序
    indexed_queries = [(mi, xi, idx) for idx, (xi, mi) in enumerate(queries)]
    indexed_queries.sort(key=lambda x: x[0])   # 按 mi 升序

    # 3. 初始化 Trie
    root = TrieNode()

    # 4. 辅助函数：往 Trie 插入一个数
    def insert(num: int) -> None:
        node = root
        for k in range(30, -1, -1):            # 从第 30 位遍历到第 0 位
            bit = (num >> k) & 1
            if node.child[bit] is None:
                node.child[bit] = TrieNode()
            node = node.child[bit]

    # 5. 辅助函数：在 Trie 中找和 x 最大的异或值
    def query(x: int) -> int:
        node = root
        if node.child[0] is None and node.child[1] is None:
            return -1                           # Trie 为空，说明没有合法数字
        ans = 0
        for k in range(30, -1, -1):
            bit = (x >> k) & 1
            # 我们希望走向相反的位
            want = 1 - bit
            if node.child[want] is not None:
                ans |= (1 << k)                  # 该位可以得到 1
                node = node.child[want]
            else:
                node = node.child[bit]           # 只能走相同位
        return ans

    # 6. 主循环：按 mi 递增处理查询，同时把满足条件的 nums 加入 Trie
    ans = [0] * len(queries)
    pos = 0                                    # nums 的指针
    for mi, xi, idx in indexed_queries:
        # 把所有 <= mi 的数加入 Trie
        while pos < n and nums[pos] <= mi:
            insert(nums[pos])
            pos += 1
        # 在当前 Trie 中查询最大异或
        ans[idx] = query(xi)

    return ans
```

> **代码说明**  
> - `insert` 与 `query` 都只遍历 31 位（0~30），所以时间是常数级别。  
> - `indexed_queries` 用来记录原始下标，保证答案返回顺序与输入一致。  
> - `while` 循环只会把每个 `nums` 元素插入一次，整体线性。

#### 复杂度

- **时间复杂度**：`O( (n + q) log (n + q) )`  
  - `n` 为 `nums` 长度，`q` 为查询数。主要来源是两次排序 (`O(n log n)`、`O(q log q)`) 以及线性遍历插入/查询（每次 31 步，可视为常数）。相较于暴力的 `O(n*q)`，大幅提升。
- **空间复杂度**：`O( n * 31 ) ≈ O(n)`  
  - Trie 最多会有 `n` 条路径，每条路径长 31，实际节点数 ≤ `n * 31`，但我们只保存指针，所以仍然是线性空间。额外的数组（排序后的 `queries`、答案）同样是 `O(n + q)`。

---

## 心得

- **核心技巧**：利用 **Trie（二进制前缀树）** 快速在大量数中找出与给定数的最大异或，同时结合 **离线排序**（把查询和数组都排序）保证每次查询只处理合法的子集合。
- **适用的题型**  
  1. “给定上限，求最大 XOR”——本题。  
  2. “在一组数中，求任意两数的最大 XOR”——LeetCode 421。  
  3. “求某数与集合中数的最小 XOR”——可将相反位改为相同位的选择。
- **一句话总结**：**“先把合法数字逐步塞进二进制 Trie，再用异或的位贪心在 Trie 中走遍最高位到最低位，就能在 O(1)（常数）时间得到最大异或”。**

---

## 反思

- **第一反应**：看到 “最大 XOR + 上限” 立刻想到 **枚举 + 位运算**，于是写出了暴力解。  
- **最容易踩的坑**  
  - **边界条件**：`mi` 可能小于所有 `nums`，此时答案必须是 `-1`，需要在 Trie 为空时单独返回。  
  - **位数选择**：`10⁹` 的二进制最高位是第 30 位（因为 `2³⁰ ≈ 1.07e9`），若写成 31 位或 32 位都可以，但一定要统一，否则会出现错误的路径。  
  - **排序后忘记恢复原始顺序**：因为查询被重新排序，必须用原下标把答案放回对应位置。  
- **下次遇到同类题**：  
  1. **先判断是否可以离线**（是否有上限、区间等约束）。  
  2. **考虑用 Trie 存二进制**，因为异或的“最高位尽可能不同”是贪心的本质。  
  3. **把数据结构的增删改操作对应到题目约束**（这里是“只增不删”。）