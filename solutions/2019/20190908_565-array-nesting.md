# #565. 数组嵌套 / Array Nesting

> 难度：中等 · 标签：Array、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/array-nesting/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n where nums is a permutation of the numbers in the range [0, n - 1].
You should build a set s[k] = {nums[k], nums[nums[k]], nums[nums[nums[k]]], ... } subjected to the following rule:
Return the longest length of a set s[k].

**Examples**

**Example 1:**

```
Input: nums = [5,4,0,3,1,6,2]
Output: 4
Explanation: 
nums[0] = 5, nums[1] = 4, nums[2] = 0, nums[3] = 3, nums[4] = 1, nums[5] = 6, nums[6] = 2.
One of the longest sets s[k]:
s[0] = {nums[0], nums[5], nums[6], nums[2]} = {5, 6, 2, 0}
```

**Example 2:**

```
Input: nums = [0,1,2]
Output: 1
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] < nums.length
- All the values of nums are unique.

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，且 `nums` 是区间 `[0, n - 1]` 内所有数字的一个排列（permutation）。  
你需要构造一个 **集合** `s[k] = {nums[k], nums[nums[k]], nums[nums[nums[k]]], …}`，满足如下规则：  

- 从下标 `k` 开始，不断取当前元素的值作为下一个下标，直至出现已访问过的下标为止，形成集合 `s[k]`。  

返回任意集合 `s[k]` 的最大可能长度。

## 示例

### 示例 1

**输入**  
```json
nums = [5,4,0,3,1,6,2]
```

**输出**  
```
4
```

**解释**  
`nums[0] = 5, nums[1] = 4, nums[2] = 0, nums[3] = 3, nums[4] = 1, nums[5] = 6, nums[6] = 2.`  
其中一个最长的集合 `s[k]` 为：  

`s[0] = {nums[0], nums[5], nums[6], nums[2]} = {5, 6, 2, 0}`

### 示例 2

**输入**  
```json
nums = [0,1,2]
```

**输出**  
```
1
```

## 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] < nums.length`
- `nums` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从每一个下标 `k` 出发，沿着 `nums[k] → nums[nums[k]] → …` 一直走，直到出现已经出现过的数字为止**。  
走的过程把遇到的数字放进一个集合 `cur_set`，走完后记录 `cur_set` 的大小，所有 `k` 的结果取最大值。

- **用到的数据结构**  
  - **集合（set）**：像查字典一样，存放已经出现的数字，判断“我已经见过这个数字了吗？”只需要 O(1) 时间。  
  - **列表（list）**：原始数组 `nums`，每个位置只会出现一次（题目保证是 `[0, n‑1]` 的全排列），所以我们可以放心地把 `nums[i]` 当作下一个下标。

- **为什么正确**  
  题目要求的集合 `s[k]` 正是从 `k` 开始沿着数组指向形成的**环**（循环链）。只要把环走完，集合里的元素就是 `s[k]`，长度即为环的大小。遍历所有起点并取最大值，自然得到答案。

- **时间/空间复杂度的大白话**  
  - **时间复杂度**：对每个起点我们都要“走”一遍，最坏情况下每次都要走 `n` 步，`n` 次起点 ⇒ `n × n = n²` 步。`O(n²)` 就是说“步数会随数组长度的平方增长”，比如 `n=10⁴` 时大概要 1 亿步，明显会超时。  
  - **空间复杂度**：每次遍历都要一个临时集合保存已经访问的数字，最多存 `n` 个元素 ⇒ `O(n)`。

#### 代码（Python）

```python
from typing import List

def arrayNesting_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    max_len = 0                     # 记录最大的集合长度

    for i in range(n):              # 从每个下标 i 出发
        cur_set = set()              # 用 set 保存本次遍历看到的数字
        j = i
        while j not in cur_set:      # 只要没有出现过，就继续往下走
            cur_set.add(j)           # 把当前下标加入集合
            j = nums[j]              # 跳到下一个下标
        max_len = max(max_len, len(cur_set))

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每个起点最多遍历 `n` 步，起点有 `n` 个。  
- **空间复杂度**：`O(n)` —— 最坏情况下 `cur_set` 会保存全部 `n` 个下标。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**同一个环会被重复遍历多次**。比如示例 `[5,4,0,3,1,6,2]` 中的环 `{0,5,6,2}`，如果我们从 `0、5、6、2` 四个起点都去走一遍，就会把同样的四条边走四遍，浪费了大量时间。

**优化的关键**：一旦我们已经知道某个下标属于某个环，就不必再从它出发重新走一遍。我们可以用一个「已访问」标记数组 `visited`（或者直接把 `nums[i]` 设为 `-1`）来记住哪些下标已经被处理过。遍历数组时：

1. **如果 `i` 已经被访问**，说明它所在的环已经算过，直接跳过。  
2. **否则**，从 `i` 开始走下去，沿途把每个经过的下标标记为已访问，并计数当前走了多少步（即当前环的大小）。  
3. 用 `max_len` 保存最大的环大小。

因为每个下标只会被标记一次，**整个过程只遍历一次数组**，时间是线性的。

> **为什么一定会形成环？**  
> 题目保证 `nums` 是 `[0, n‑1]` 的全排列，也就是说每个下标都有且仅有唯一的「指向」`nums[i]`，且指向的值仍在 `[0, n‑1]` 范围。把所有下标当作图的节点、`i → nums[i]` 当作有向边，这就是一个 **每个节点出度为 1 的有向图**，必然由若干**互不相交的环**组成（没有入口、也没有出口），所以从任意未访问的节点出发必定能走到环的起点并回到起点。

#### 代码（Python）

```python
from typing import List

def arrayNesting(nums: List[int]) -> int:
    n = len(nums)
    visited = [False] * n          # visited[i] 表示下标 i 是否已经被遍历过
    max_len = 0

    for i in range(n):
        if visited[i]:              # 已经算过的下标直接跳过
            continue

        cur = i
        cur_len = 0                 # 记录当前环的长度
        while not visited[cur]:     # 只要没走过，就继续往下
            visited[cur] = True     # 标记为已访问
            cur = nums[cur]         # 跳到下一个下标
            cur_len += 1            # 环长加一

        max_len = max(max_len, cur_len)

    return max_len
```

> **代码要点解释**  
> - `visited` 像一本「已走过的路标册」，查一次就知道这条路是否已经走过，时间 O(1)。  
> - `while not visited[cur]` 保证每个下标只会进入循环一次。  
> - `cur_len` 正是我们沿着环走的步数，也就是集合 `s[i]` 的大小。

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个下标只会被访问一次，整体步数随 `n` 成线性关系。  
- **空间复杂度**：`O(n)`（或 `O(1)` 进阶写法）—— 需要一个长度为 `n` 的布尔数组记录访问情况；如果允许原地修改 `nums`（把已访问的元素设为 `-1`），则额外空间可降到 `O(1)`。

---

## 心得

- **核心技巧**：**遍历并标记已访问**（相当于在有向图中寻找互不相交的环），避免重复计算。  
- **该技巧适用的题型**：  
  1. **数组嵌套**（本题）  
  2. **寻找数组中的循环链**（如 LeetCode 287. Find the Duplicate Number）  
  3. **图的连通分量计数**（如 LeetCode 200. Number of Islands 的 DFS/BFS 变体）  
- **一句话总结解题钥匙**：**一次遍历，走过的节点全部打上“已走过”标记，后面的起点直接跳过**。

---

## 反思

- **第一反应**：看到“`nums[nums[...]]`”的嵌套下标，就想把它写成循环，一步步把数字收集进集合，逐个起点尝试。  
- **最容易踩的坑**  
  - **忘记去重**：直接把数字放进列表会出现重复计数，必须用集合或 `visited` 防止重复。  
  - **遗漏环的结束条件**：如果只用 `while True` 而不判断是否回到起点或已访问，会导致无限循环。  
  - **边界条件**：数组长度为 `1` 时仍然要返回 `1`，代码里 `while not visited[cur]` 能正确处理。  
- **下次遇到同类题**：第一步先思考**“这是一张每个节点只有一条出边的图吗？如果是，是否会形成环？”**，然后立刻考虑用**访问标记**一次遍历解决。