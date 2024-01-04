# #2537. 统计好子数组的数量 / Count the Number of Good Subarrays

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-good-subarrays/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the number of good subarrays of nums.
A subarray arr is good if there are at least k pairs of indices (i, j) such that i < j and arr[i] == arr[j].
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,1,1,1,1], k = 10
Output: 1
Explanation: The only good subarray is the array nums itself.
```

**Example 2:**

```
Input: nums = [3,1,4,3,2,2,4], k = 2
Output: 4
Explanation: There are 4 different good subarrays:
- [3,1,4,3,2,2] that has 2 pairs.
- [3,1,4,3,2,2,4] that has 3 pairs.
- [1,4,3,2,2,4] that has 2 pairs.
- [4,3,2,2,4] that has 2 pairs.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i], k <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回 `nums` 中 **好子数组（good subarray）** 的数量。

如果一个子数组 `arr` 至少存在 `k` 对满足 `i < j` 且 `arr[i] == arr[j]` 的索引 `(i, j)`，则称该子数组为 **好子数组**。  
子数组（subarray）是数组中连续的、非空的元素序列。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**

示例 1：  
Input: `nums = [1,1,1,1,1]`, `k = 10`  
Output: `1`  
Explanation: 唯一的好子数组就是整个数组 `nums` 本身。

示例 2：  
Input: `nums = [3,1,4,3,2,2,4]`, `k = 2`  
Output: `4`  
Explanation: 有 4 个不同的好子数组：
- `[3,1,4,3,2,2]`，其中恰好有 2 对相等元素。
- `[3,1,4,3,2,2,4]`，其中有 3 对相等元素。
- `[1,4,3,2,2,4]`，其中有 2 对相等元素。
- `[4,3,2,2,4]`，其中有 2 对相等元素。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i], k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子数组**，对每一个子数组统计其中相等元素对的数量，看是否 ≥ k，满足条件的就计数。  

- **枚举子数组**：用两个循环 `left`、`right`（`left ≤ right`）确定子数组的左右端点。  
- **统计相等对**：对子数组里的每个元素，用另一个循环与它后面的元素比较，若相等则计数 + 1。  
- **数据结构**：这里不需要额外的结构，直接用数组和整数计数。可以把“遍历所有可能的组合”想象成 **把所有可能的拼图块都搬出来逐个检查**，虽然很费力，但一定能找到答案。

**为什么正确**：因为我们把**每一种可能的子数组**都检查了一遍，符合条件的自然会被统计，漏掉的不存在。

**时间/空间复杂度**  
- 外层两层循环产生 `O(n²)` 个子数组。  
- 对每个子数组再用两层循环去比较元素，最坏情况下是 `O(length²)`，整体时间复杂度是 `O(n³)`（这里的 `n` 是数组长度）。  
- 空间上只用到常数个变量，`O(1)`。

> **大白话**：  
> - `O(n³)` 就像把一座 1000 层的大楼每层的每个房间都检查三遍，根本不可能在几秒内完成。  
> - `O(1)` 空间意味着我们只需要一张纸记几个数字，不会占用额外的“大箱子”。

#### 代码（Python）

```python
def count_good_subarrays_bruteforce(nums, k):
    n = len(nums)
    ans = 0

    # 枚举左端点
    for left in range(n):
        # 枚举右端点
        for right in range(left, n):
            # 统计子数组 nums[left:right+1] 中相等元素对的数量
            pairs = 0
            # 双层循环比较每一对 (i, j)
            for i in range(left, right + 1):
                for j in range(i + 1, right + 1):
                    if nums[i] == nums[j]:
                        pairs += 1
            # 如果达到 k 对，就算一个好子数组
            if pairs >= k:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - `n` 为数组长度。三层循环的意思是“遍历所有子数组的所有元素对”。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量，没有额外的随 `n` 增长的存储。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**每次都重新统计子数组里的相等对**。  
观察一下：

- 当我们往子数组右侧加入一个新元素 `x` 时，**只会新增** `cnt[x]`（`x` 在当前子数组中已经出现的次数） 对，因为新加入的 `x` 与之前出现的每一个 `x` 都形成一对。  
- 当我们把左侧的元素 `y` 移出子数组时，**会减少** `cnt[y] - 1` 对（`y` 与子数组里其余的 `y` 形成的对数），因为这些对不再属于子数组。

于是我们可以**用滑动窗口（双指针）**维护一个 **“当前窗口中的相等对数”**，并随时更新它。

具体步骤：

1. 用两个指针 `left`、`right`（均从 0 开始）表示当前窗口 `[left, right)`（左闭右开）。  
2. `freq` 为哈希表（字典），记录窗口内每个数出现的次数。  
3. `pairs` 为窗口内相等对的总数。  
4. **扩张右指针**：把 `nums[right]` 加入窗口，`pairs += freq[nums[right]]`（因为它与已经出现的相同数字形成这么多新对），然后 `freq[nums[right]] += 1`，`right += 1`。  
5. **收缩左指针**：只要 `pairs >= k`（窗口已经 **不再好**，即已经包含至少 `k` 对），我们就把左端点向右移动，统计以当前 `left` 为左端点的所有**好子数组**的数量。  
   - 当 `pairs >= k` 时，**以 `left` 为左端点的所有子数组** `[left, right-1]、[left, right]、...`（只要右端点不小于当前 `right`）都是好子数组。因为右端点再往右只会让对数不减。于是贡献 `len(nums) - right + 1`（因为右端点可以取 `right-1, right, …, n-1`）。  
   - 然后把 `nums[left]` 移出窗口，`freq[nums[left]] -= 1`，`pairs -= freq[nums[left]]`（因为它原来与窗口里其余相同元素形成 `freq[nums[left]]` 对），`left += 1`。  
6. 重复 4、5，直至右指针遍历完整个数组。

> **类比**：  
> 想象有一条流水线，左边是入口，右边是出口。我们不断往右边放新商品（扩张窗口），同时在左边把旧商品搬走（收缩窗口），只用记住每种商品现在有多少件，以及因为新商品加入产生了多少“配对”。这样就能在 **O(n)** 的时间内完成统计。

#### 代码（Python）

```python
def count_good_subarrays(nums, k):
    """
    使用滑动窗口 + 哈希表统计满足「至少 k 对相等元素」的子数组个数。
    """
    n = len(nums)
    freq = {}          # 哈希表：元素 -> 在当前窗口中的出现次数
    left = 0           # 窗口左端点（闭）
    right = 0          # 窗口右端点（开），初始窗口为空 []
    pairs = 0          # 窗口内相等元素对的数量
    ans = 0

    while right < n:
        # --------- 把 nums[right] 加入窗口 ----------
        x = nums[right]
        cnt_x = freq.get(x, 0)          # x 之前出现了多少次
        pairs += cnt_x                  # 新加入的 x 与每个已有的 x 形成一对
        freq[x] = cnt_x + 1
        right += 1

        # --------- 当窗口已经「不再好」时，统计并收缩 ----------
        # 只要 pairs >= k，说明以 left 为左端点的子数组
        # 只要右端点不小于当前 right，就一定满足条件
        while pairs >= k:
            # 以当前 left 为左端点的好子数组数量 = n - right + 1
            ans += n - right + 1

            # 把左端点的元素移出窗口
            y = nums[left]
            freq[y] -= 1
            # 移除 y 会失去它与窗口中其余 y 形成的配对数
            pairs -= freq[y]   # 因为剩下的 freq[y] 个 y 仍在窗口，它们之间已经计数，移除的 y 只会失去这 freq[y] 对
            left += 1

    return ans
```

> **关键注释解释**  
> - `pairs += cnt_x`：把新元素加入窗口时，它会与已经出现的相同元素每一个配成一对。  
> - `pairs -= freq[y]`：把左端点的元素移出时，它原本与窗口里其余相同元素形成 `freq[y]` 对，这些对都要删掉。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个元素最多被右指针加入一次、左指针移出一次，所有操作都是 **常数时间**（字典查询/更新）。  
  - 与暴力解的 `O(n³)` 相比，简直是 **天壤之别**，相当于把“遍历所有可能的拼图块”压缩成“一遍线性扫描”。  
- **空间复杂度**：`O(m)`，`m` 为不同数字的种类数（最坏 `m = n`），因为我们用哈希表记录每个数的出现次数。  
  - 对于本题的约束 `n ≤ 10⁵`，这在内存上是完全可以接受的。

---

## 心得

- **核心技巧**：**滑动窗口 + 计数哈希表**，通过增删元素的局部贡献来维护全局“相等对数”。  
- **适用题型**：  
  1. “子数组满足某种计数条件” 如 **“子数组中不超过 K 个不同整数”**（LeetCode 340. Longest Substring with At Most K Distinct Characters）。  
  2. “子数组中满足累计和/累计次数的阈值” 如 **“子数组和 ≥ K 的个数”**（前缀和 + 二分/哈希）。  
  3. “子数组中出现次数超过阈值的元素个数” 如 **“最多包含 K 个重复元素的最长子数组”**（LeetCode 1004. Max Consecutive Ones III）。  
- **一句话总结**：  
  > 把“整体统计”拆成“每次加入/删除一个元素的局部增量”，配合双指针，就能把指数级暴力降到线性。

---

## 反思

- **第一反应**：看到“子数组”“至少 k 对相等元素”，我第一时间想到**枚举子数组**并逐个计数——这正是暴力思路。  
- **最容易踩的坑**：  
  - **计数更新错误**：加入元素时应加上 **已有出现次数**，而不是 `+1`；移除元素时应减去 **移除后仍在窗口中的出现次数**（即 `freq[value]`，而不是 `freq[value] - 1`）。  
  - **右指针的边界**：在 `while pairs >= k` 循环里统计答案时，`right` 已经指向“窗口外的下一个位置”，所以贡献的子数组数是 `n - right + 1`（而不是 `n - right`）。  
  - **大数溢出**：答案可能达到 `O(n²)`（约 `10¹⁰`），在 Python 中整数不会溢出，但在有些语言需要使用 64 位整数。  
- **下次思路**：遇到“子数组满足某种累计条件”时，第一步先思考**“增量如何更新”**，进而尝试**滑动窗口**或**前缀和 + 哈希**的线性/对数解法。