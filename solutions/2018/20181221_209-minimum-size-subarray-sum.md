# #209. 最小长度子数组和 / Minimum Size Subarray Sum

> 难度：中等 · 标签：Array、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-size-subarray-sum/)

---

## 题目（英文原版）

**Description**

Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

**Examples**

**Example 1:**

```
Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: The subarray [4,3] has the minimal length under the problem constraint.
```

**Example 2:**

```
Input: target = 4, nums = [1,4,4]
Output: 1
```

**Example 3:**

```
Input: target = 11, nums = [1,1,1,1,1,1,1,1]
Output: 0
```

**Constraints**

- 1 <= target <= 109
- 1 <= nums.length <= 105
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums` 和一个正整数 `target`，返回满足子数组（subarray）之和 **大于等于** `target` 的最小长度。如果不存在这样的子数组，返回 `0`。

**示例 1**  
**输入**: `target = 7, nums = [2,3,1,2,4,3]`  
**输出**: `2`  
**解释**: 子数组 `[4,3]` 在满足题目条件的所有子数组中长度最小。

**示例 2**  
**输入**: `target = 4, nums = [1,4,4]`  
**输出**: `1`  
**解释**: 子数组 `[4]`（任选一个 `4`）的长度为 `1`，已经满足和 ≥ `target`。

**示例 3**  
**输入**: `target = 11, nums = [1,1,1,1,1,1,1,1]`  
**输出**: `0`  
**解释**: 没有任何子数组的和能够达到 `11`，因此返回 `0`。

**约束条件**

- `1 <= target <= 10^9`
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把所有可能的子数组都枚举一遍，算出它们的和，看看哪些子数组的和 `≥ target`，然后在这些符合条件的子数组中挑出最短的长度。

- **枚举子数组**：我们可以用两个循环，第一个循环决定子数组的左端点 `left`，第二个循环把右端点 `right` 从 `left` 往后推，一直加到数组末尾。  
- **求和**：在每一次把 `right` 向右移动时，把新加入的元素加到当前的累计和 `curr_sum` 上。  
- **更新答案**：只要 `curr_sum ≥ target`，说明 `[left, right]` 这段子数组已经满足要求，此时记录下它的长度 `right-left+1`，并尝试更新全局最小长度 `ans`。  

> **类比**：想象你在一本厚厚的书里找连续的页码，使得这些页码对应的字数总和不小于某个目标。暴力法就像是把每一页都当作起点，然后逐页往后翻，累计字数，直到满足目标，再记下用了多少页。这样遍历所有起点，最终得到最少的页数。

这个方法一定能得到正确答案，因为我们把**所有**可能的连续子数组都检查了一遍。

#### 代码（Python）

```python
def min_subarray_len_brute(target: int, nums: list[int]) -> int:
    n = len(nums)
    ans = float('inf')                 # 用正无穷表示“目前还没有找到合法子数组”

    for left in range(n):              # 枚举子数组的左端点
        curr_sum = 0                    # 累计和从 0 开始
        for right in range(left, n):   # 右端点不断向右扩展
            curr_sum += nums[right]    # 把新加入的元素加进累计和
            if curr_sum >= target:     # 一旦满足 “和 ≥ target”
                ans = min(ans, right - left + 1)  # 更新最小长度
                break                  # 对当前 left，已经找到了最短的 right，后面再往右只会更长

    return 0 if ans == float('inf') else ans   # 如果 ans 仍是正无穷，说明不存在合法子数组
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环遍历 `n` 次，内层最坏情况下也要遍历 `n` 次（比如目标非常大，必须遍历到数组末尾才能达到），于是大约要做 `n × n` 次加法和比较。用大白话说，就是如果数组有 10,000 个元素，最坏会进行约 1 亿 次操作，明显太慢了。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`ans、curr_sum、left、right`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在“双层循环”——我们对每一个左端点都重新累加一次右端点的和，导致大量重复计算。事实上，**连续子数组的和** 有一个非常好的性质：**如果我们把左端点向右移动，累计和只会减去左端点对应的数值**，而右端点向右扩展则只会**加上新元素**。这正好符合“窗口”在数组上滑动的过程。

**滑动窗口（Two‑Pointer）** 技巧：

1. 维护一个窗口 `[left, right]`，窗口内的元素之和记为 `window_sum`。  
2. 初始时 `left = 0, right = 0, window_sum = 0`（窗口为空）。  
3. **右指针**不断右移（`right += 1`），把新元素加入 `window_sum`。  
4. 每当 `window_sum ≥ target`，说明当前窗口已经满足要求，此时可以**尝试收缩左端点**（`left += 1`），同时把离开的元素从 `window_sum` 中减去，以期得到更短的合法窗口。每一次收缩后，都更新最小长度 `ans`。  
5. 当右指针遍历完数组后，过程结束。

> **类比**：把数组想象成一条装满水的管子，`right` 是水流的入口，`left` 是出口。我们不断往管子里倒水（右指针），当管子里水量 ≥ 目标时，就尝试把出口往前移（左指针），把多余的水倒掉，记录下管子最短的“够水”长度。

**为什么有效**：  
- 每个元素最多只会被左指针和右指针各访问一次，整个过程是线性的。  
- 当 `window_sum` 小于目标时，唯一的办法是继续往右扩张；当 `window_sum` 大于等于目标时，唯一的办法是尝试把左端点往右收缩，以期更短的长度。这样不会遗漏任何可能的最短子数组。

#### 代码（Python）

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    n = len(nums)
    ans = n + 1                 # 用一个大于可能答案的初始值，方便后面比较
    left = 0
    window_sum = 0

    for right in range(n):      # 右指针一次遍历整个数组
        window_sum += nums[right]   # 把新加入的元素加到窗口和里

        # 当窗口和已经满足要求时，尝试收缩左端点
        while window_sum >= target:
            # 更新最小长度
            ans = min(ans, right - left + 1)
            # 把左端点元素移出窗口，并左指针右移
            window_sum -= nums[left]
            left += 1

    # 如果 ans 仍然是初始值，说明不存在合法子数组
    return 0 if ans == n + 1 else ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：`right` 指针遍历一次数组，`left` 指针最多也只会向右移动 `n` 步（每一步都对应一次 `while` 循环体的执行），所以总的操作次数不超过 `2n`，即线性时间。与暴力解的 `n²` 相比，速度提升了一个数量级。
- **空间复杂度**：`O(1)`  
  - 只用了若干个整数变量（`left、right、window_sum、ans`），不随 `n` 增长。

---

## 心得

- **核心技巧**：**滑动窗口（Two‑Pointer）**。它适用于“求满足某种累计条件的最短/最长连续子数组”这类问题。  
- **类似题目**：
  1. *Longest Substring Without Repeating Characters*（求最长不含重复字符的子串）——使用哈希表+滑动窗口。  
  2. *Maximum Size Subarray Sum Equals k*（求和等于 k 的最长子数组）——使用前缀和+哈希表（思路类似窗口）。  
  3. *Minimum Window Substring*（最小覆盖子串）——也是滑动窗口的经典变形。  
- **一句话总结**：**“把数组看成一条可伸缩的绳子，右指针拉长，左指针收紧，随时记录最短满足条件的长度”。**

---

## 反思

- **第一反应**：看到“子数组”和“最小长度”，自然想到枚举所有子数组（暴力），但很快会意识到会超时。  
- **最容易踩的坑**：
  1. **边界条件**：当数组中没有任何子数组满足条件时，需要返回 `0`，而不是默认的 `inf` 或者 `n+1`。  
  2. **窗口收缩**：在 `while window_sum >= target` 循环里一定要先更新答案，再把左端点元素移出，否则会错过当前窗口的长度。  
  3. **整数溢出**：本题 `target` 可达 `10⁹`，`nums[i]` 最高 `10⁴`，累计和可能超过 32 位整数范围，使用 Python 的大整数不会有问题，但在其他语言要注意使用 64 位整数。  
- **下次类似题的第一步**：**先判断是否可以使用滑动窗口**——检查“子数组是连续的”“所有元素为正数（或非负）”这两个条件是否满足；如果满足，就立刻尝试构建左、右指针的线性遍历框架。