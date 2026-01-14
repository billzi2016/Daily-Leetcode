# #3489. 零数组转换 IV / Zero Array Transformation IV

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/zero-array-transformation-iv/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and a 2D array queries, where queries[i] = [li, ri, vali].
Each queries[i] represents the following action on nums:
A Zero Array is an array with all its elements equal to 0.
Return the minimum possible non-negative value of k, such that after processing the first k queries in sequence, nums becomes a Zero Array. If no such k exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]
Output: 2
Explanation:
```

**Example 2:**

```
Input: nums = [4,3,2,1], queries = [[1,3,2],[0,2,1]]
Output: -1
Explanation:
It is impossible to make nums a Zero Array even after all the queries.
```

**Example 3:**

```
Input: nums = [1,2,3,2,1], queries = [[0,1,1],[1,2,1],[2,3,2],[3,4,1],[4,4,1]]
Output: 4
Explanation:
```

**Example 4:**

```
Input: nums = [1,2,3,2,6], queries = [[0,1,1],[0,2,1],[1,4,2],[4,4,4],[3,4,1],[4,4,5]]
Output: 4
```

**Constraints**

- 1 <= nums.length <= 10
- 0 <= nums[i] <= 1000
- 1 <= queries.length <= 1000
- queries[i] = [li, ri, vali]
- 0 <= li <= ri < nums.length
- 1 <= vali <= 10

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 和一个二维数组 `queries`，其中 `queries[i] = [l_i, r_i, v_i]`。  
每个 `queries[i]` 表示对 `nums` 执行如下操作：

- 将下标区间 `[l_i, r_i]`（包括两端）内的每个元素 **加** 上 `v_i`。

> **零数组（Zero Array）** 指所有元素均为 `0` 的数组。

返回最小的非负整数 `k`，使得按顺序处理前 `k` 条查询后，`nums` 变成零数组。如果不存在这样的 `k`，返回 `-1`。

---

### 示例

**示例 1**  
```text
Input: nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]
Output: 2
Explanation:
```
（此处解释略）

**示例 2**  
```text
Input: nums = [4,3,2,1], queries = [[1,3,2],[0,2,1]]
Output: -1
Explanation:
即使执行完所有查询，也无法将 `nums` 变为零数组。
```

**示例 3**  
```text
Input: nums = [1,2,3,2,1], queries = [[0,1,1],[1,2,1],[2,3,2],[3,4,1],[4,4,1]]
Output: 4
Explanation:
```
（此处解释略）

**示例 4**  
```text
Input: nums = [1,2,3,2,6], queries = [[0,1,1],[0,2,1],[1,4,2],[4,4,4],[3,4,1],[4,4,5]]
Output: 4
```

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 1000`
- `1 <= queries.length <= 10^5`
- `queries[i] = [l_i, r_i, v_i]`
- `0 <= l_i <= r_i < nums.length`
- `1 <= v_i <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有查询一次性全部执行**，得到每个位置最终被加（或减）的总和，然后和原数组 `nums` 对比，看看是否全为 0。  
如果要找最小的前缀 `k`，我们可以**枚举 `k = 1 … m`（`m = len(queries)`）**，每次把前 `k` 条查询重新算一遍，看数组是否已经全部归零。

> **类比**：想象你在厨房里一次加盐，每加一次都记下来。要知道第几次加完后味道刚好合适，就只能把每一次的加盐量重新算一遍，看看什么时候恰好等于目标味道。

**为什么正确**：  
- 查询的执行顺序是固定的，前 `k` 条查询的效果就是把这 `k` 条的 `vali` 加到它们覆盖的区间上。  
- 只要我们把这些加法全部算出来，得到的数组一定是**唯一**的。  
- 检查它是否全为 0，就是在判断“这 `k` 条查询的累计加法正好抵消了 `nums`”。  

**复杂度分析（大白话版）**  
- 对每个可能的 `k`（最多 `m` 次），我们都要**从头遍历所有查询**（最多 `k` 条），并且对每条查询再遍历它覆盖的区间（最多 `n` 个元素）。  
- 于是总的工作量大约是 `1 + 2 + … + m` 次遍历区间，等价于 `m·(m+1)/2`，再乘以 `n`。  
- 用大 O 记号写就是 **O(m²·n)**。  
- 这里的 “平方” 并不是说程序会跑几百亿次（因为 `m ≤ 1000`），而是说**运行时间随查询数量的平方增长**。  
- 额外的空间只需要保存一个长度为 `n` 的临时数组，**O(n)**。

#### 代码（Python）

```python
def zeroArrayTransformation(nums, queries):
    n = len(nums)               # 元素个数，最多 10
    m = len(queries)            # 查询个数，最多 1000

    # 暴力：枚举前缀长度 k
    for k in range(1, m + 1):
        cur = [0] * n           # 本次前 k 条查询的累计加法

        # 把前 k 条查询全部重新算一遍
        for i in range(k):
            l, r, v = queries[i]    # 区间左端、右端、加的数值
            for idx in range(l, r + 1):
                cur[idx] += v        # 把 v 加到区间里的每个位置

        # 检查是否已经全部归零
        ok = True
        for i in range(n):
            if nums[i] - cur[i] != 0:   # 需要恰好抵消
                ok = False
                break
        if ok:
            return k                # 找到最小的前缀长度

    return -1                       # 所有查询都执行完也没法归零
```

> **关键行注释**  
> - `cur = [0] * n`：相当于一张空白的白纸，记录每个位置累计被加了多少。  
> - `cur[idx] += v`：把这条查询的 “加 v” 写到对应的格子里。  
> - `nums[i] - cur[i] != 0`：原来的数字要被加的总量恰好抵消才行。

#### 复杂度

- **时间复杂度**：`O(m²·n)`  
  - 想象 `m = 1000`，`n = 10`，最坏情况大约是 `1000·1000·10 = 10⁷` 次基本操作，仍能在一秒左右跑完，但不是最优的。  
- **空间复杂度**：`O(n)`  
  - 只用到一个长度为 `n` 的临时数组 `cur`，跟 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每次重新遍历前 `k` 条查询是多余的**。  
我们其实可以**在一次遍历中顺序执行查询**，并在执行完每条查询后**立即判断**当前数组是否已经全部归零。  

> **瓶颈在哪里**：暴力解每次都要把前面的查询重新算一遍，这相当于在“重复写同一本日记”。  
> **优化的关键**：把日记写成 **增量式**，每写一条新记录，就直接更新当前状态，而不是把所有记录都翻出来重新写。

因为 `vali` 均为正数，**每个位置的累计加法只会单调递增**。  
所以如果某个位置的累计加法已经超过了 `nums[i]`，说明以后再加只会更大，**永远不可能再回到恰好等于 `nums[i]`**，此时直接返回 `-1`（因为已经不可逆了）。  

整体思路：

1. 初始化一个长度为 `n` 的数组 `cur` 为全 0，表示目前已经加了多少。  
2. 按顺序遍历 `queries`（记第 `i` 条查询为第 `i+1` 步）。  
3. 对当前查询 `[l, r, v]`，把 `v` 加到 `cur[l … r]`。  
4. 检查 **所有位置** 是否已经满足 `cur[j] == nums[j]`。  
   - 若全部满足，返回当前步数 `i+1`（因为步数从 1 开始计数）。  
   - 若某个位置已经 `cur[j] > nums[j]`，直接返回 `-1`（再也不可能归零）。  
5. 循环结束后仍未归零，说明所有查询用完也不行，返回 `-1`。

> **类比**：想象你在给一排水槽注水，每次灌水量固定且只能往右或左扩展。  
> - 暴力做法是每次都把前面所有的水倒出来再重新倒一遍。  
> - 最优做法是直接把新水倒进去，顺便检查水位是否正好达到目标。  

#### 代码（Python）

```python
def zeroArrayTransformation(nums, queries):
    n = len(nums)
    cur = [0] * n               # 已经累计加的数，初始全 0

    # 依次执行每条查询
    for step, (l, r, v) in enumerate(queries, start=1):
        # 把 v 加到区间 [l, r]
        for idx in range(l, r + 1):
            cur[idx] += v

        # 检查是否已经全部恰好等于 nums
        all_zero = True
        for i in range(n):
            if cur[i] > nums[i]:          # 已经超过，后面只能更大
                return -1
            if cur[i] != nums[i]:         # 只要有一个不等，就不是全零
                all_zero = False

        if all_zero:                       # 所有位置恰好等于 nums
            return step

    # 所有查询执行完仍未归零
    return -1
```

> **关键行解释**  
> - `enumerate(queries, start=1)`：把遍历的下标直接当作“已经执行了多少条查询”。  
> - `cur[idx] += v`：增量更新，等价于把新的一笔“加 v”写到对应格子。  
> - `if cur[i] > nums[i]: return -1`：一旦超额，就相当于往已经满的杯子里继续倒水，永远倒不回去。  

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 每条查询只遍历一次它覆盖的区间（最坏 `n`），总共 `m` 条查询。  
  - 相比暴力的 `O(m²·n)`，这里 **查询数量只线性增长**，即“翻一本日记只写一次”。  
- **空间复杂度**：`O(n)`  
  - 只需要保存当前累计加法的 `cur` 数组。

---

## 心得  

- **核心技巧**：**增量模拟 + 单调性提前剪枝**。  
- **适用的题型**：  
  1. **区间加法模拟**（如 “Range Addition” 系列、Difference Array）  
  2. **单调累计检查**（如 “Running Sum” 需要提前判断是否超出阈值）  
  3. **前缀任务完成时间**（如 “Minimum Number of Operations to Make Array Zero”）  
- **一句话总结解题钥匙**：**把每一次操作的结果保留下来，实时更新并立即检查——只要一次遍历，所有信息都在手**。

---

## 反思  

- **第一反应**：直接把每个前缀重新算一遍（暴力），因为最直观的想法是“先算再比较”。  
- **最容易踩的坑**：  
  - **忘记提前剪枝**：一旦某个位置的累计值已经大于 `nums[i]`，如果继续循环会浪费时间，甚至错过返回 `-1` 的时机。  
  - **边界条件**：`li`、`ri` 可能相等（单点更新），需要保证循环 `range(l, r+1)` 正确覆盖。  
  - **返回的步数**：题目要求的是“最小的非负 `k`”，所以返回的应该是 **已经执行的查询数量**，而不是数组下标。  
- **下次类似题**：第一步想到 **“是否可以用一次增量遍历把状态维护下来？”**，如果可以，就立刻写出 O(m·n) 的模拟；否则再考虑更复杂的 DP 或差分技巧。