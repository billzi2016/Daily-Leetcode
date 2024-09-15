# #2869. 收集元素的最少操作次数 / Minimum Operations to Collect Elements

> 难度：简单 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-collect-elements/)

---

## 题目（英文原版）

**Description**

You are given an array nums of positive integers and an integer k.
In one operation, you can remove the last element of the array and add it to your collection.
Return the minimum number of operations needed to collect elements 1, 2, ..., k.

**Examples**

**Example 1:**

```
Input: nums = [3,1,5,4,2], k = 2
Output: 4
Explanation: After 4 operations, we collect elements 2, 4, 5, and 1, in this order. Our collection contains elements 1 and 2. Hence, the answer is 4.
```

**Example 2:**

```
Input: nums = [3,1,5,4,2], k = 5
Output: 5
Explanation: After 5 operations, we collect elements 2, 4, 5, 1, and 3, in this order. Our collection contains elements 1 through 5. Hence, the answer is 5.
```

**Example 3:**

```
Input: nums = [3,2,5,3,1], k = 3
Output: 4
Explanation: After 4 operations, we collect elements 1, 3, 5, and 2, in this order. Our collection contains elements 1 through 3. Hence, the answer is 4.
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= nums.length
- 1 <= k <= nums.length
- The input is generated such that you can collect elements 1, 2, ..., k.

---

## 题目（中文翻译）

**描述**  
给定一个由正整数构成的数组 `nums` 和一个整数 `k`。  
在一次操作中，你可以移除数组的最后一个元素并将其加入你的收集集合。  
返回收集到元素 `1, 2, ..., k` 所需的最少操作次数。

**示例**

**示例 1**  
输入: `nums = [3,1,5,4,2]`, `k = 2`  
输出: `4`  
解释: 经过 4 次操作后，我们依次收集到的元素是 `2, 4, 5, 1`。此时集合中包含元素 `1` 和 `2`，因此答案为 `4`。

**示例 2**  
输入: `nums = [3,1,5,4,2]`, `k = 5`  
输出: `5`  
解释: 经过 5 次操作后，我们依次收集到的元素是 `2, 4, 5, 1, 3`。此时集合中包含元素 `1` 到 `5`，因此答案为 `5`。

**示例 3**  
输入: `nums = [3,2,5,3,1]`, `k = 3`  
输出: `4`  
解释: 经过 4 次操作后，我们依次收集到的元素是 `1, 3, 5, 2`。此时集合中包含元素 `1` 到 `3`，因此答案为 `4`。

**约束条件**  
- `1 <= nums.length <= 50`  
- `1 <= nums[i] <= nums.length`  
- `1 <= k <= nums.length`  
- 输入保证可以收集到元素 `1, 2, ..., k`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**一步一步地把数组最后一个元素弹出来**，把它放进自己的收藏袋，然后检查目前已经收集到了多少个目标数字 `1…k`。  
- **数据结构**：我们可以用 Python 的 `list`（相当于购物车）来模拟“收藏”。  
- **检查是否全部收齐**：每次弹出后，遍历 `1…k`，看这 `k` 个数字是否全部出现在收藏里。可以把收藏当成一本“字典”，`key` 是数字，`value` 是是否已经收到了（类似查字典时，词是 key，页码是 value）。  

为什么这样能得到正确答案？因为题目规定只能从数组的**尾部**取元素，按照这个顺序取完若干次后，若恰好已经收齐 `1…k`，那么这就是一种合法的操作序列。我们只要找出最早出现“全部收齐”的那一步，即是最少操作数。

**时间/空间复杂度**  
- 每弹出一次，就要检查一次 `k` 个目标数字是否都在收藏里，这一步是 `O(k)`。最坏情况下需要弹出全部 `n` 个元素，所以总时间是 `O(n·k)`。  
- 需要的额外空间只有收藏列表，最多保存 `n` 个元素，空间复杂度是 `O(n)`。  

> 大白话解释：如果 `n=50，k=50`，暴力解大约要做 2500 次“小检查”，在电脑里跑几毫秒都能搞定，但从算法的角度来看，这不是最省力的办法。

#### 代码（Python）

```python
def minOperations_bruteforce(nums, k):
    """
    暴力解：每次弹出最后一个元素后，遍历 1~k 检查是否全部已收集。
    """
    collected = []                 # 用列表模拟收藏袋
    n = len(nums)

    for ops in range(1, n + 1):    # ops 表示已经做了多少次弹出
        # 把当前数组的最后一个元素弹出放进收藏
        collected.append(nums[-ops])

        # 检查 1~k 是否全部在 collected 中
        ok = True
        for target in range(1, k + 1):
            if target not in collected:   # 线性查找，最坏 O(k)
                ok = False
                break
        if ok:                      # 已经收齐，返回当前操作次数
            return ops

    # 按题意一定能收齐，这行理论上不会被执行
    return n
```

#### 复杂度

- **时间复杂度**：`O(n·k)`  
  - 解释：`n` 次弹出 × 每次检查 `k` 个目标数字 → 乘法关系就像“买 10 本书，每本书要翻 5 页”，总页数是 50 页。
- **空间复杂度**：`O(n)`  
  - 解释：最坏情况下我们把全部 `n` 个元素都弹进收藏袋，收藏袋的大小随之线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历 `1…k` 去判断是否已经全部收齐**。其实我们不需要每次都去“找”。只要在弹出元素的同时**记住已经收到了哪些目标数字**，就能在 **O(1)** 时间内判断是否已经收齐。

**关键点**：

1. **出现数组（occurrence array）**  
   - 把 `1…k` 的出现情况记录在一个长度为 `k+1` 的布尔数组 `seen` 中。  
   - `seen[x] = True` 表示数字 `x` 已经被弹出并收进了收藏。  
   - 这相当于一本“查字典”，词（key）是数字，页码（value）是“是否已经在字典里”。查一次只需要看一个格子，时间是 `O(1)`。

2. **逆序遍历**  
   - 因为只能从数组尾部弹出，实际操作顺序就是 **从右往左** 读取数组。  
   - 所以我们直接从 `nums` 的最后一个元素向前遍历，模拟一次次的弹出。

3. **计数已收集的目标数字**  
   - 用一个计数器 `cnt` 记录已经标记（收集）的目标数字个数。  
   - 当 `cnt == k` 时，说明 `1…k` 全部出现，当前遍历到的位置（从 1 开始计数）就是最少操作数。

**为什么一定能得到最小操作数**？  
我们是**按实际操作的顺序**（从数组末尾往前）逐个检查的，一旦发现已经收齐 `k` 个目标数字，就立刻返回。这是“最早”出现完整集合的时刻，必然是最少的弹出次数。

#### 代码（Python）

```python
def minOperations(nums, k):
    """
    最优解：使用出现数组 + 逆序遍历，只需要 O(n) 时间。
    """
    seen = [False] * (k + 1)   # seen[0] 虚位，真正关心 1~k
    cnt = 0                    # 已经收集到的目标数字个数

    # 从数组末尾向前遍历，ops 表示已经弹出的次数（从 1 开始计数）
    for ops, val in enumerate(reversed(nums), start=1):
        # 只关心 <= k 的数字，且之前未出现过
        if 1 <= val <= k and not seen[val]:
            seen[val] = True    # 标记为已收集
            cnt += 1            # 计数器加一

            # 当已经收齐 1~k 时，当前 ops 就是答案
            if cnt == k:
                return ops

    # 题目保证一定能收齐，这里理论上不会执行
    return len(nums)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：只遍历一次数组，**每个元素只看一次**，相当于“只走一趟路”。相比暴力的 `O(n·k)`，这是一大提升。  
- **空间复杂度**：`O(k)`  
  - 解释：我们只用一个长度为 `k+1` 的布尔数组来记录出现情况，最多占用 `k` 个格子。若 `k` 接近 `n`，空间仍然是线性级别，但比起保存整个 `collected` 列表的 `O(n)` 更小。

---

## 心得

- **核心技巧**：**出现数组 + 逆序遍历**（相当于“一边走路一边在纸上记笔记”），可以在一次扫描中快速判断“所有目标是否出现”。  
- **适用的题型**  
  1. “从数组尾部取元素，直到满足某些条件”——如 *“Collect Elements”* 系列。  
  2. “在序列中找最早出现全部指定元素的窗口”——如 *“Shortest Subarray with All Unique Elements”*。  
  3. “统计子数组或前缀中出现次数”——如 *“Maximum Number of Consecutive Ones”*（使用布尔数组记录状态）。  
- **一句话总结**：**把“是否出现”用一个布尔表记下来，边走边标记，第一时间发现全部出现时即是最优答案**。

---

## 反思

- **第一反应**：看到只能从尾部弹出，立刻想到“倒着遍历”。这一步把操作顺序和数组顺序对应起来，思路更清晰。  
- **最容易踩的坑**  
  - **忘记限制 `val <= k`**：如果不判断，只标记所有数字，计数器可能提前达到 `k`，导致错误答案。  
  - **重复计数**：同一个目标数字出现多次时，只能计数一次，需要 `if not seen[val]` 的判断。  
  - **边界条件**：`k = 1` 或 `k = len(nums)` 时，代码仍然要正常返回，使用 `enumerate(..., start=1)` 防止返回 `0`。  
- **下次遇到同类题**：**第一步先确定遍历方向（正序还是逆序），然后考虑用哈希表或布尔数组记录“已出现”。** 只要能“一遍遍历 + 常数时间检查”，往往就能得到最优解。