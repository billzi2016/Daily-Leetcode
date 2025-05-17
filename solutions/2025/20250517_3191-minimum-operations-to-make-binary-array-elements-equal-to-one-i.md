# #3191. 使二进制数组元素全部等于1的最少操作次数 I / Minimum Operations to Make Binary Array Elements Equal to One I

> 难度：中等 · 标签：Array、Bit Manipulation、Queue、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/)

---

## 题目（英文原版）

**Description**

You are given a binary array nums.
You can do the following operation on the array any number of times (possibly zero):
Flipping an element means changing its value from 0 to 1, and from 1 to 0.
Return the minimum number of operations required to make all elements in nums equal to 1. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: nums = [0,1,1,1,0,0]
Output: 3
Explanation: We can do the following operations:
```

**Example 2:**

```
Input: nums = [0,1,1,1]
Output: -1
Explanation: It is impossible to make all elements equal to 1.
```

**Constraints**

- 3 <= nums.length <= 105
- 0 <= nums[i] <= 1

---

## 题目（中文翻译）

给定一个二进制数组 `nums`（binary array）。
你可以对数组执行以下操作任意次（包括零次）：

- 翻转（Flipping）一个元素，即将其值从 `0` 变为 `1`，或从 `1` 变为 `0`。

返回使 `nums` 中所有元素都等于 `1` 所需的最小操作次数。如果无法实现，返回 `-1`。

### 示例

**示例 1**  
输入: `nums = [0,1,1,1,0,0]`  
输出: `3`  
解释: 我们可以执行以下操作：

**示例 2**  
输入: `nums = [0,1,1,1]`  
输出: `-1`  
解释: 无法将所有元素变为 `1`。

### 约束条件

- `3 <= nums.length <= 10^5`
- `0 <= nums[i] <= 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的翻转序列全部穷举**，看哪一种能把数组全部变成 `1`，并记录最少的翻转次数。

- **操作是什么？**  
  题目说明一次操作可以把 **连续的 3 个元素** 同时翻转（`0↔1`）。可以把它想象成手里有一把 **3 位“开关”**，每次把这把开关对准数组的某个位置，三盏灯一起切换状态。  
- **暴力枚举**  
  对于长度为 `n` 的数组，任意位置 `i (0 ≤ i ≤ n‑3)` 都可以选择“开关”或不选择。于是每个位置有两种状态（翻还是不翻），总共会出现 `2^{n-2}`（因为最后两个位置不能再发起新的 3‑翻）种组合。我们可以用递归（或 BFS）遍历这些组合，模拟每一次翻转后数组的变化，最后检查是否全是 `1`，若是则更新最小操作数。  
- **为什么一定对？**  
  因为我们把 **所有可能的翻转序列** 都尝试了一遍，必然不会漏掉最优解。  

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy

def min_operations_bruteforce(nums):
    """
    暴力 BFS：每一次把「可以翻转的起始下标」入队，
    同时记录已经使用过的状态，防止重复搜索。
    """
    n = len(nums)
    start = tuple(nums)                 # 把列表变成不可变的 tuple，方便哈希
    if all(x == 1 for x in start):      # 已经全是 1
        return 0

    q = deque()
    q.append((start, 0))                # (当前数组, 已经用了几次操作)
    visited = {start}

    while q:
        cur, step = q.popleft()
        # 尝试在每个可以翻转的起始位置 i 进行一次操作
        for i in range(n - 2):
            nxt = list(cur)              # 复制一份，准备翻转
            # 翻转 i、i+1、i+2 三个位置
            nxt[i]   ^= 1                # ^=1 等价于 0↔1
            nxt[i+1] ^= 1
            nxt[i+2] ^= 1
            nxt_t = tuple(nxt)
            if nxt_t in visited:         # 已经遍历过的状态直接跳过
                continue
            if all(x == 1 for x in nxt): # 全部变成 1，返回答案
                return step + 1
            visited.add(nxt_t)
            q.append((nxt_t, step + 1))
    # BFS 结束仍未找到全 1 的状态，说明无解
    return -1
```

> **关键行解释**  
> - `nxt[i] ^= 1`：`^=` 是异或赋值，`0 ^ 1 = 1, 1 ^ 1 = 0`，恰好实现“翻转”。  
> - `visited` 集合：防止在搜索过程中重复进入同一个数组状态，避免指数级的重复工作。  

#### 复杂度

- **时间复杂度：** `O(2^{n})`（指数级）  
  因为最坏情况下我们会遍历所有可能的翻转组合。对初学者来说可以把它想象成“每个位置都有两种选择，所有选择相乘”。  
- **空间复杂度：** `O(2^{n})`  
  需要存放 BFS 队列和 `visited` 集合中的所有状态，同样是指数级增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**遍历所有组合**，而实际上我们并不需要这么多尝试。观察题目可以得到一个非常重要的**局部贪心**性质：

1. **只能用长度为 3 的窗口翻转**，因此**第 0 位只能被第 0、1、2 这三个位置的同一次操作影响**。  
2. 如果 `nums[0]` 已经是 `1`，我们完全可以不动它，直接考虑从下标 `1` 开始的子数组。  
3. 如果 `nums[0]` 是 `0`，唯一能把它变成 `1` 的办法就是**在下标 `0` 发起一次翻转**（即翻转 `[0,1,2]`）。因为没有任何其他操作会涉及到下标 `0`。  

基于以上两点，我们可以**从左到右一次扫描**数组：

- 当扫描到位置 `i` 时，若 `nums[i]` 为 `0`，立刻在 `i,i+1,i+2` 处执行一次翻转，并计数。  
- 这一步骤保证了 **在处理完位置 `i` 后，它永远不会再被后面的操作影响**（因为后面的操作起点都在 `i+1` 及以后，翻转窗口长度为 3，根本覆盖不到 `i`）。  

最终，我们只需要检查 **最后两个位置**（`n-2`、`n-1`）是否已经都是 `1`。如果是，返回计数；否则说明无解（因为没有足够的元素再发起一次 3‑翻转来修正它们）。

> **为什么贪心是对的？**  
> 由于只能用长度为 3 的窗口，**左边的元素一旦被确定为 1，就不可能再被后面的操作改变**。所以在遍历到 `i` 时，唯一的选择就是立刻把它变成 1（如果它本来就是 1，则保持不动）。这一步不会影响后面还能做的决定，因此是最优的。

#### 代码（Python）

```python
def min_operations(nums):
    """
    贪心左扫：从左到右，只要当前位置是 0 就在这里翻转
    长度为 3 的窗口。时间 O(n)，空间 O(1)。
    """
    n = len(nums)
    ops = 0                         # 记录翻转次数
    i = 0
    while i <= n - 3:               # 只要还能形成长度为 3 的窗口就继续
        if nums[i] == 0:            # 需要翻转
            # 翻转 i, i+1, i+2 三个位置
            nums[i]   ^= 1
            nums[i+1] ^= 1
            nums[i+2] ^= 1
            ops += 1
        i += 1                       # 向右移动一步，继续检查下一个位置

    # 检查最后两个位置是否全是 1
    if nums[-1] == 1 and nums[-2] == 1:
        return ops
    return -1                       # 无法全部变成 1
```

> **关键行解释**  
> - `while i <= n - 3:`：只要还能以 `i` 为起点形成 `[i,i+1,i+2]` 的窗口，就可以尝试翻转。  
> - `nums[i] ^= 1` 等价于“把 0 变成 1，或把 1 变成 0”。  

#### 复杂度

- **时间复杂度：** `O(n)` — 只遍历一次数组，`n` 是数组长度。对比暴力的指数级，这相当于把“所有可能的组合”压缩成“一条直线”。  
- **空间复杂度：** `O(1)` — 只使用了几个额外的整数变量（计数器 `ops`、索引 `i`），不随 `n` 增长。

---

## 心得

- **核心技巧**：**左到右的贪心 + 固定窗口翻转**。  
- **适用题型**  
  1. “把二进制数组全变成 1，只能翻转固定长度子数组” 类似题（如 *Minimum Operations to Make Binary Array Elements Equal to One II*）。  
  2. “灯泡开关”类问题（每次切换固定数量的灯），比如 LeetCode 995 “Minimum Number of K Consecutive Bit Flips”。  
  3. “用最少操作把数组变为单调递增/递减”，当操作只能影响局部连续区间时常能使用类似的贪心扫描。  

> **一句话总结解题钥匙**：**从左到右，只要当前位置不符合目标，就立刻在这里动手；后面的操作永远不会再影响已解决的左边。**

---

## 反思

- **第一反应**：看到“只能翻 3 个连续元素”，立刻想到**滑动窗口**或**局部贪心**。  
- **最容易踩的坑**  
  1. **忘记检查末尾两个元素**：左扫结束后可能还有未被覆盖的 `0`，必须返回 `-1`。  
  2. **数组越界**：在 `i` 接近 `n-2` 时仍尝试翻转会导致越界，记得只在 `i ≤ n-3` 时才可以操作。  
  3. **原地修改 vs. 复制**：若在函数外部还要保留原数组，需要先拷贝一份再进行原地翻转。  
- **下次遇到同类题**，第一步应该思考**“最左侧的错误元素只能被哪个最靠左的操作修正？”**，据此设计**从左到右的贪心策略**。