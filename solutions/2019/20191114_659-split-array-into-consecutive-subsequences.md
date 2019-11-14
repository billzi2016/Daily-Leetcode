# #659. 分割数组为连续子序列 / Split Array into Consecutive Subsequences

> 难度：中等 · 标签：Array、Hash Table、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/split-array-into-consecutive-subsequences/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums that is sorted in non-decreasing order.
Determine if it is possible to split nums into one or more subsequences such that both of the following conditions are true:
Return true if you can split nums according to the above conditions, or false otherwise.
A subsequence of an array is a new array that is formed from the original array by deleting some (can be none) of the elements without disturbing the relative positions of the remaining elements. (i.e., [1,3,5] is a subsequence of [1,2,3,4,5] while [1,3,2] is not).

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,3,4,5]
Output: true
Explanation: nums can be split into the following subsequences:
[1,2,3,3,4,5] --> 1, 2, 3
[1,2,3,3,4,5] --> 3, 4, 5
```

**Example 2:**

```
Input: nums = [1,2,3,3,4,4,5,5]
Output: true
Explanation: nums can be split into the following subsequences:
[1,2,3,3,4,4,5,5] --> 1, 2, 3, 4, 5
[1,2,3,3,4,4,5,5] --> 3, 4, 5
```

**Example 3:**

```
Input: nums = [1,2,3,4,4,5]
Output: false
Explanation: It is impossible to split nums into consecutive increasing subsequences of length 3 or more.
```

**Constraints**

- 1 <= nums.length <= 104
- -1000 <= nums[i] <= 1000
- nums is sorted in non-decreasing order.

---

## 题目（中文翻译）

给定一个按非递减顺序排序的整数数组 `nums`。  
判断是否可以将 `nums` 拆分成一个或多个子序列（subsequence），使得以下两个条件同时成立：

1. 每个子序列都是严格递增且连续的，即子序列中的每个元素与前一个元素的差值恰好为 1。  
2. 每个子序列的长度至少为 3。

如果能够按照上述条件拆分 `nums`，返回 `true`；否则返回 `false`。

**子序列** 是指从原数组中删除若干（可以为零）元素后得到的新数组，且不改变剩余元素的相对顺序。（例如 `[1,3,5]` 是 `[1,2,3,4,5]` 的子序列，而 `[1,3,2]` 不是）。

---

### 示例

#### 示例 1
**输入**  
`nums = [1,2,3,3,4,5]`  

**输出**  
`true`  

**解释**  
`nums` 可以拆分为以下两个子序列：  
- `[1,2,3]`  
- `[3,4,5]`

#### 示例 2
**输入**  
`nums = [1,2,3,3,4,4,5,5]`  

**输出**  
`true`  

**解释**  
`nums` 可以拆分为以下两个子序列：  
- `[1,2,3,4,5]`  
- `[3,4,5]`

#### 示例 3
**输入**  
`nums = [1,2,3,4,4,5]`  

**输出**  
`false`  

**解释**  
无法将 `nums` 拆分成长度至少为 3 且连续递增的子序列。

---

### 约束条件

- `1 <= nums.length <= 10^4`
- `-1000 <= nums[i] <= 1000`
- `nums` 已按非递减顺序排序。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每一个** 元素都决定到底放到哪条子序列里，然后检查所有子序列的长度是否都≥3、且元素是否连续。  
这相当于 **枚举所有可能的划分**，就像把一串珠子用剪刀随意剪开，所有剪法都尝试一遍。

- **数据结构**：我们可以用一个 `list` 保存当前已经形成的若干子序列，每条子序列本身也是 `list`。  
  - 把哈希表想象成一本“词典”，键（key）是单词，值（value）是对应的页码；这里的 `list` 就是把珠子放进不同的盒子里，盒子编号就是子序列的下标。  
- **递归/回溯**：对数组 `nums` 按顺序遍历，当前处理的数字 `x` 有两种选择  
  1. **放到已有的子序列**：只要该子序列的最后一个元素恰好是 `x-1`（保持连续），我们就可以把 `x` 加进去。  
  2. **新开一条子序列**：把 `x` 当作新子序列的第一个元素。  

  对每一种选择继续递归处理下一个数字。递归到底（所有数字都放完）后，检查每条子序列的长度是否≥3，若全部满足则返回 `True`。  

- **为什么正确**：因为我们把 **所有** 合法的放置方式都遍历了一遍，只要有一种满足题目条件，就一定能在递归树的某个叶子节点发现。  

- **时间/空间复杂度**：  
  - 每个数字有 **“放到已有序列”** 或 **“新建序列”** 两种分支，最坏情况下分支数会呈指数增长。大概是 `O(2^n)`（指数级），也就是说当 `n=20` 时就已经非常慢了。  
  - 递归需要保存当前的子序列集合，最坏需要保存 `n` 条子序列，每条长度最多 `n`，空间大约是 `O(n^2)`。  

> **大白话**：指数时间就像不停地在森林里分岔走路，树枝越分越多，走到尽头的时间会炸裂；而平方空间就像在纸上画 `n` 行 `n` 列的格子，格子数会随 `n` 的增大而快速增长。

#### 代码（Python）  

```python
from typing import List

def can_split_bruteforce(nums: List[int]) -> bool:
    """
    暴力回溯：尝试把每个数放进已有子序列或新建子序列。
    由于指数时间，这里只用于演示思路，实际 LeetCode 会 TLE。
    """
    def backtrack(idx: int, seqs: List[List[int]]) -> bool:
        # idx 为当前要处理的 nums 下标
        if idx == len(nums):
            # 所有数字都放完，检查每条子序列长度是否 ≥ 3
            return all(len(s) >= 3 for s in seqs)

        cur = nums[idx]

        # 1️⃣ 试着放到已有的、可以接上的子序列
        for i, s in enumerate(seqs):
            if s[-1] == cur - 1:               # 必须连续
                s.append(cur)                  # 放进去
                if backtrack(idx + 1, seqs):
                    return True
                s.pop()                         # 回溯，撤销

        # 2️⃣ 如果没有放进去的可能，或者放进去都不行，尝试新建子序列
        seqs.append([cur])                     # 开一条新序列
        if backtrack(idx + 1, seqs):
            return True
        seqs.pop()                             # 回溯，撤销新建的序列

        return False

    return backtrack(0, [])
```

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 每个元素都有两种选择，导致递归树呈指数增长。  
- **空间复杂度**：`O(n^2)` —— 最坏情况下需要保存 `n` 条子序列，每条长度最多 `n`（即 `n × n` 的格子）。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“把每个数都尽量接到已有的序列上”** 是关键。  
如果我们每次都把当前数字接到 **最短** 的、可以接上的序列，剩下的数字就更容易组成长度 ≥ 3 的新序列。  

**瓶颈**  
- 暴力解每次都遍历所有已有序列去判断能否接上，导致大量重复检查。  
- 还要记住每条序列的全部元素，实际上我们只关心 **序列的最后一个元素** 和 **序列的长度**。

**优化思路**  
1. **统计每个数字出现的次数**：用哈希表 `cnt`（相当于一本“数字词典”，键是数字，值是剩余可用次数）。  
2. **记录以某个数字结尾的序列有多少条**：再用一个哈希表 `tails`，键是序列的最后一个数字，值是以它结尾的序列数量。  
3. **遍历 nums（从小到大）**，对每个数字 `x`：
   - 如果 `cnt[x] == 0`，说明这个数字已经全部被前面的步骤用了，直接跳过。  
   - **优先尝试把 `x` 接到已有序列**：检查 `tails[x-1]` 是否大于 0。  
     - 若可以，则把一条以 `x-1` 结尾的序列延长到 `x`，于是 `tails[x-1]--`，`tails[x]++`，并且 `cnt[x]--`。  
   - **如果不能接**，只能尝试新建长度为 3 的序列 `[x, x+1, x+2]`：  
     - 检查 `cnt[x+1]` 与 `cnt[x+2]` 是否都 ≥ 1。  
     - 若可以，则把这三个数字的计数各减 1，并在 `tails` 中记录一条以 `x+2` 结尾的序列（`tails[x+2]++`）。  
   - **若两种方式都不行**，说明无论怎么划分都无法满足题目条件，直接返回 `False`。  

4. 遍历结束后，若没有提前返回 `False`，说明所有数字都成功放进了合法序列，返回 `True`。  

**核心算法**：**贪心 + 哈希表**。  
- “贪心” 在这里指的是**尽可能把当前数字接到已有序列**，因为这样可以让已有序列更快变长，避免以后出现“短序列卡死”。  
- 哈希表的作用类似于**查字典**：我们只需要 O(1) 时间就能知道某个数字还有多少剩余，以及有多少序列期待这个数字。  

**类比**：想象你在排队买电影票，手里有若干张不同编号的票（数字）。  
- `cnt` 告诉你每种票还有几张没用。  
- `tails` 告诉你已经开始的观影组合里，哪种编号的票是最后一张（等着后面的票继续）。  
每来一张票，你先看看有没有已经开的组合正好缺这张票（`tails[x-1]`），如果有，就把它接进去；否则，你必须自己凑够三张连续的票才能开新组合。  

#### 代码（Python）  

```python
from collections import Counter, defaultdict
from typing import List

def is_possible_split(nums: List[int]) -> bool:
    """
    贪心 + 哈希表（Counter + defaultdict）
    时间 O(n)  空间 O(n)
    """
    # 1️⃣ 统计每个数字出现次数
    cnt = Counter(nums)                 # 相当于“数字词典”：数字 -> 剩余次数
    # 2️⃣ 记录以某个数字结尾的序列数量，默认 0
    tails = defaultdict(int)            # tails[x] 表示以 x 结尾的序列有多少条

    for x in nums:
        if cnt[x] == 0:                  # 这个数字已经全部被使用，跳过
            continue

        # 3️⃣ 先尝试接到已有序列（看是否有以 x-1 结尾的序列）
        if tails[x - 1] > 0:
            # 把一条以 x-1 结尾的序列延长到 x
            tails[x - 1] -= 1           # 原来的序列不再以 x-1 结尾
            tails[x] += 1               # 现在它以 x 结尾
            cnt[x] -= 1                 # 使用掉一个 x
        else:
            # 4️⃣ 不能接，尝试新建长度为 3 的序列 [x, x+1, x+2]
            if cnt[x + 1] > 0 and cnt[x + 2] > 0:
                cnt[x]     -= 1         # 使用 x
                cnt[x + 1] -= 1         # 使用 x+1
                cnt[x + 2] -= 1         # 使用 x+2
                tails[x + 2] += 1       # 这条新序列现在以 x+2 结尾
            else:
                # 两种方式都做不到，直接失败
                return False

    # 所有数字都成功放进合法序列
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，对每个元素的操作（哈希表查询、增删）都是 **O(1)** 常数时间。  
  - 与暴力解 `O(2^n)` 相比，指数级的递归被一次线性扫描取代，速度快了天差地别。  
- **空间复杂度**：`O(n)` —— 最坏情况下 `cnt` 与 `tails` 中会出现与 `nums` 长度相同数量的键（比如全是不重复的数字），因此使用的额外空间与 `n` 成线性关系。  

---

## 心得  

- **核心技巧**：**贪心 + 哈希表**（记录剩余次数和序列末尾）。  
- **适用的题型**（类似思路）：  
  1. *Split Array into Consecutive Subsequences*（本题）  
  2. *Divide Array in Sets of K Consecutive Numbers*（把数组划分成 K 长度的连续子序列）  
  3. *Longest Subsequence With Limited Repetitions*（利用计数哈希表做贪心）  
- **一句话总结解题钥匙**：**“把每个数尽量接到已有的最短连续序列上，否则必须立即凑齐三个连续数新开序列”。**  

---

## 反思  

- **第一反应**：看到“连续子序列、长度≥3”，本能想到**回溯**，把每个数放进不同的盒子里尝试。  
- **最容易踩的坑**：  
  - 忘记检查 `cnt[x+1]` 与 `cnt[x+2]` 是否足够，导致出现负计数错误。  
  - 只关注序列的“元素”，而忽视**序列的长度**；如果只记录末尾而不保证长度≥3，就会错误接受如 `[1,2]` 的情况。  
  - 边界条件：数组最后几位可能没有 `x+1`、`x+2`，直接访问会报 `KeyError`，所以要使用 `defaultdict(int)` 或先判断键是否存在。  
- **下次类似题的第一步**：先**统计每个数字出现次数**，再思考“**是否能把当前数字接到已有序列**”。如果接不上的话，检查**能否直接凑够最小长度的全新序列**。这样就能迅速走向贪心解。