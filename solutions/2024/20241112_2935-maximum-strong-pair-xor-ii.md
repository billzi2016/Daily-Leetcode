# #2935. Maximum Strong Pair XOR II / Maximum Strong Pair XOR II

> 难度：困难 · 标签：Array、Hash Table、Bit Manipulation、Trie、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-strong-pair-xor-ii/)

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
Input: nums = [500,520,2500,3000]
Output: 1020
Explanation: There are 6 strong pairs in the array nums: (500, 500), (500, 520), (520, 520), (2500, 2500), (2500, 3000) and (3000, 3000).
The maximum XOR possible from these pairs is 500 XOR 520 = 1020 since the only other non-zero XOR value is 2500 XOR 3000 = 636.
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 1 <= nums[i] <= 220 - 1

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。如果一对整数 `x` 和 `y` 满足  
**max(x, y) ≤ 2 × min(x, y)**，则称它们为 **强配对（strong pair）**。  

你需要从 `nums` 中挑选两个整数，使它们构成强配对，并且它们的按位异或（bitwise XOR）在所有强配对中取得最大值。返回该最大 XOR 值。  

注意，构成配对的两个整数可以是同一个元素（即可以选择同一个整数两次）。

**示例 1**  
输入: `nums = [1,2,3,4,5]`  
输出: `7`  
解释: 数组中共有 11 对强配对：  
`(1,1)`, `(1,2)`, `(2,2)`, `(2,3)`, `(2,4)`, `(3,3)`, `(3,4)`, `(3,5)`, `(4,4)`, `(4,5)`, `(5,5)`。  
这些配对中最大的异或值为 `3 XOR 4 = 7`。

**示例 2**  
输入: `nums = [10,100]`  
输出: `0`  
解释: 数组中只有 2 对强配对：`(10,10)` 与 `(100,100)`。  
它们的异或均为 `0`，所以答案为 `0`。

**示例 3**  
输入: `nums = [500,520,2500,3000]`  
输出: `1020`  
解释: 数组中共有 6 对强配对：  
`(500,500)`, `(500,520)`, `(520,520)`, `(2500,2500)`, `(2500,3000)`, `(3000,3000)`。  
最大异或值为 `500 XOR 520 = 1020`（另一个非零异或为 `2500 XOR 3000 = 636`）。

**约束条件**  
- `1 ≤ nums.length ≤ 5 * 10^4`  
- `1 ≤ nums[i] ≤ 2^20 - 1`   (即 `220 - 1` 的正确写法)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求找 **强对**（strong pair） 中 **异或**（XOR） 最大的那一对。  
先把“强对”这件事说清楚：

> 对任意两个数 `x`、`y`（不论顺序），只要满足  
> `|x - y| ≤ min(x, y)`  
> 就叫 **强对**。  

把它稍微变形一下会更直观。设 `x ≤ y`，则 `|x - y| = y - x`，条件变成  

```
y - x ≤ x   →   y ≤ 2·x
```

所以 **只要较大的数不超过较小数的两倍**，这对数就是强对。

**暴力做法**：

1. 两层循环遍历所有 `i, j (0 ≤ i, j < n)`，把 `nums[i]` 当作 `x`，`nums[j]` 当作 `y`（可以相同）。
2. 检查 `max(nums[i], nums[j]) ≤ 2 * min(nums[i], nums[j])` 是否成立。
3. 成立就计算 `nums[i] ^ nums[j]`，维护一个全局最大值。

> **类比**：把数组想成一排小朋友，两个小朋友要手拉手玩游戏，只有当“身高差不超过较矮的两倍”时才可以。我们把每一对小朋友都尝试一次，记录下最开心（XOR 最大）的那对。

**为什么正确**：我们遍历了所有可能的配对，凡是符合强对条件的都会被检查，最大值自然被找出来。

**复杂度**：

- **时间**：外层 `n` 次，内层也 `n` 次，整体是 `O(n²)`。  
  - **大白话**：如果数组有 10,000 个数，暴力需要跑 100,000,000 次检查，明显会慢到不行。
- **空间**：只用了常数个额外变量，`O(1)`。

#### 代码（Python）

```python
from typing import List

def maxStrongPairXor_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                     # 记录最大的 XOR
    for i in range(n):
        for j in range(n):
            x, y = nums[i], nums[j]
            # 判断是否为强对：较大数 ≤ 2 * 较小数
            if max(x, y) <= 2 * min(x, y):
                cur = x ^ y      # 计算 XOR
                if cur > ans:
                    ans = cur
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要比较每一对数，随 `n` 的平方增长。  
- **空间复杂度**：`O(1)` — 只用了几个临时变量。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在 **两层循环**，导致 `n²` 次检查。  
我们要利用 **“y ≤ 2·x”** 这个不等式，让每个 `x` 只去比较 **有限且相对较少** 的 `y`。

思路分两步：

1. **排序 + 滑动窗口**  
   - 把数组从小到大排好序。  
   - 对于固定的左指针 `l`（对应较小的数 `x`），右指针 `r` 往右移动，只要 `nums[r] ≤ 2 * nums[l]` 就保持在窗口里。  
   - 当 `r` 超过 `2 * nums[l]` 时，左指针左移，窗口左边界收缩。  
   - 这样对于每个 `x`，窗口中恰好是所有满足 `y ≤ 2·x` 的 `y`（包括 `x` 本身），且窗口大小 **均摊下来是 O(1)**，因为每个元素最多进出窗口一次。

2. **在窗口内找最大 XOR**  
   - 只要能在 “当前窗口的所有数” 中快速找出 **与 x 异或最大的 y**，整体就能在 `O(n·logC)` 时间内完成（`C` 为数的最大位数，这里 ≤ 2^20，logC = 20）。  
   - 这正是 **Trie（二进制字典树）** 的强项：  
     - 每个数的二进制从最高位（第 19 位）到最低位插入 Trie。  
     - 查询时，从最高位往下走，尽量往 **相反的位**（如果当前位是 0，就去 1 那条路）走，这样得到的数与 `x` 的异或在该位上为 1，贡献最大。  
   - 当左指针左移时，需要把对应的数 **从 Trie 中删除**，否则它会误导后面的查询。删除可以在 Trie 上把计数 `cnt` 减 1，若计数为 0 再把节点回收（这里用计数即可，不必真的删掉节点）。

**整体流程**：

```
sort nums
init empty binary trie
l = 0, r = 0, ans = 0
while l < n:
    # 扩大右边界，使所有满足 y ≤ 2*nums[l] 的数进入窗口
    while r < n and nums[r] <= 2 * nums[l]:
        trie.insert(nums[r])
        r += 1

    # 此时窗口里所有数都可以和 nums[l] 配对
    best = trie.max_xor(nums[l])      # 在 Trie 中找与 nums[l] XOR 最大的数
    ans = max(ans, best)

    # 移出左端点，准备 l+1
    trie.delete(nums[l])
    l += 1
return ans
```

**关键点解释**：

- **为什么排序后窗口合法**？  
  排序保证 `nums[l] ≤ nums[l+1] ≤ …`。当 `r` 移动到第一个不满足 `nums[r] ≤ 2·nums[l]` 的位置时，后面的所有数更大，必然也不满足 `y ≤ 2·x`，所以不必再检查。

- **Trie 的工作原理**（从零解释）  
  - 想象每个二进制位是一次 “左/右” 的选择，根节点是第 19 位，往左走代表该位是 0，往右走代表 1。  
  - 插入一个数，就是沿着它的二进制路径走下去，路过的每个节点的计数 `cnt` 加一。  
  - 查询最大 XOR：从最高位开始，若当前位 `x` 为 0，我们希望选 1（因为 0 xor 1 = 1），若对应的子树还有数（`cnt > 0`），就走那条路；否则只能走相同位的路。这样得到的数在每一位都尽量让 XOR 为 1，最终得到最大可能的异或值。

- **删除**：同样沿路径走下去，把每个节点的 `cnt` 减一即可。计数为 0 的节点在后续查询时自然会被视作不存在。

#### 代码（Python）

```python
from typing import List

BIT = 20                 # 因为 nums[i] < 2^20

class TrieNode:
    __slots__ = ("child", "cnt")
    def __init__(self):
        # child[0] 为位 0 的子节点，child[1] 为位 1 的子节点
        self.child = [None, None]
        self.cnt = 0     # 经过此节点的数的个数

class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, num: int) -> None:
        node = self.root
        node.cnt += 1
        for k in range(BIT - 1, -1, -1):   # 从最高位到最低位
            b = (num >> k) & 1
            if not node.child[b]:
                node.child[b] = TrieNode()
            node = node.child[b]
            node.cnt += 1

    def delete(self, num: int) -> None:
        node = self.root
        node.cnt -= 1
        for k in range(BIT - 1, -1, -1):
            b = (num >> k) & 1
            nxt = node.child[b]
            nxt.cnt -= 1
            # 若计数为 0，可选地把指针置空释放内存（这里不必做）
            node = nxt

    def max_xor(self, num: int) -> int:
        """在 Trie 中找与 num 异或最大的数，返回该最大 XOR 值"""
        node = self.root
        ans = 0
        for k in range(BIT - 1, -1, -1):
            b = (num >> k) & 1
            # 想走相反的位，使 XOR 该位为 1
            togg = 1 - b
            if node.child[togg] and node.child[togg].cnt > 0:
                ans |= (1 << k)          # 这一位异或得 1
                node = node.child[togg]
            else:
                node = node.child[b]     # 只能走相同位的路，异或得 0
        return ans

def maxStrongPairXor(nums: List[int]) -> int:
    n = len(nums)
    nums.sort()                     # 先排序
    trie = BinaryTrie()
    l = r = 0
    ans = 0

    while l < n:
        # 扩大右指针，加入所有满足 y ≤ 2*x 的数
        while r < n and nums[r] <= 2 * nums[l]:
            trie.insert(nums[r])
            r += 1

        # 当前窗口里所有数都可以和 nums[l] 配对
        cur = trie.max_xor(nums[l])
        if cur > ans:
            ans = cur

        # 左指针离开窗口，需要把 nums[l] 删除
        trie.delete(nums[l])
        l += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n · BIT)`，这里 `BIT = 20`，所以大约是 `O(20n) ≈ O(n)`。  
  - 排序 `O(n log n)`，在本题的约束下仍然是主导项，但 `log n`（≈ 16）同样很小。总体是 `O(n log n)`。  
  - 与暴力的 `O(n²)` 相比，提升非常明显。  
  - **大白话**：如果有 50,000 个数，算法大约只会遍历几百万次（远远小于 2.5 × 10⁹ 次）。

- **空间复杂度**：`O(n · BIT)` 用于 Trie，最坏情况每个数都占用 20 个节点 → `O(n·20) ≈ O(n)`。额外的指针、计数等都是常数级。

---

## 心得

- **核心技巧**：  
  1. **把约束转化为区间**（`y ≤ 2·x`），利用排序 + 滑动窗口把每个 `x` 能配对的 `y` 限制在一个可管理的集合里。  
  2. **二进制 Trie** 用来在动态集合中快速查询“与给定数异或最大的数”。  

- **适用的题型**（类似思路）  
  - “在满足某种数值区间关系的数对中，求最大 XOR / 和 / 差”  
  - “给定数组，要求满足 `|a[i] - a[j]| ≤ k` 的最大 XOR”  
  - “在一段区间内（滑动窗口）求最大异或”  

- **一句话总结解题钥匙**：  
  “把 `y ≤ 2·x` 转成窗口，然后在窗口里用二进制 Trie 按位挑最不同的数，即可线性时间得到最大强对 XOR”。  

---

## 反思

- **第一反应**：看到“强对”条件 `|x - y| ≤ min(x, y)`，立刻把它化简成 `y ≤ 2·x`（假设 `x ≤ y`），想到可以把数组排个序，这样左小右大的关系更好处理。  
- **最容易踩的坑**  
  - **漏掉同一个数配对**：题目允许 `x` 与自身配对，若忘记把 `x` 插入 Trie 再查询，会错失 `x ^ x = 0` 的情况（虽然不影响最大值，但会导致窗口为空时查询出错）。  
  - **删除时计数未减**：Trie 中仅删指针会导致后续查询仍把已离开的数算进去，必须维护每个节点的出现次数。  
  - **位数选择错误**：若取的 BIT 小于实际数的最高位，会把高位信息丢失，导致错误的 XOR。这里安全取 20（因为 `nums[i] < 2^20`).  
  - **窗口移动顺序**：一定要先 **插入**满足条件的右端点，再 **查询**，最后 **删除**左端点，否则会把 `x` 本身遗漏或多算。  

- **下次遇到同类题**：  
  1. **先把约束写成 “区间/倍数” 形式**，看能否用排序+双指针/滑动窗口把可选集合限定。  
  2. **判断目标函数（最大 XOR、最大和、最小差等）**适合哪种数据结构——对 XOR，二进制 Trie 是首选。  
  3. **先写出插入/查询/删除的模板**，再把滑动窗口的进出操作套进去即可。