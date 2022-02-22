# #1679. 最大 K 和配对数 / Max Number of K-Sum Pairs

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/max-number-of-k-sum-pairs/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array.
Return the maximum number of operations you can perform on the array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], k = 5
Output: 2
Explanation: Starting with nums = [1,2,3,4]:
- Remove numbers 1 and 4, then nums = [2,3]
- Remove numbers 2 and 3, then nums = []
There are no more pairs that sum up to 5, hence a total of 2 operations.
```

**Example 2:**

```
Input: nums = [3,1,3,4,3], k = 6
Output: 1
Explanation: Starting with nums = [3,1,3,4,3]:
- Remove the first two 3's, then nums = [1,4,3]
There are no more pairs that sum up to 6, hence a total of 1 operation.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个整数 `k`。  
在一次操作（operation）中，你可以从数组中挑选出两个数字，使它们的和等于 `k`，并将这两个数字从数组中移除。  
返回在数组上可以执行的最多操作次数。

**示例 1**  
输入：`nums = [1,2,3,4]`, `k = 5`  
输出：`2`  
解释：初始 `nums = [1,2,3,4]`：  
- 移除数字 `1` 与 `4`，此时 `nums = [2,3]`  
- 移除数字 `2` 与 `3`，此时 `nums = []`  
没有更多和为 `5` 的配对，故总共进行 `2` 次操作。

**示例 2**  
输入：`nums = [3,1,3,4,3]`, `k = 6`  
输出：`1`  
解释：初始 `nums = [3,1,3,4,3]`：  
- 移除前两个 `3`，此时 `nums = [1,4,3]`  
没有更多和为 `6` 的配对，故总共进行 `1` 次操作。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把数组里每两个数都拿出来试一试，看看它们的和是否等于 `k`。  
- **数据结构**：只需要原数组本身和一个标记数组（或直接把已经配对的数从列表中删掉），相当于在“挑水果”时，用手指在篮子里一个个挑，看两颗水果加起来的重量是否正好是 `k`。  
- **正确性**：只要遍历了所有可能的两两组合，就不会漏掉任何可以配对的情况。每找到一对满足 `a + b = k`，就把这两个数从后续的比较中移除，确保每个元素最多只被使用一次，从而得到 **最大** 的配对次数。  
- **时间/空间复杂度**：  
  - 时间上要检查 `n` 个数中的每一对，组合数是 `C(n,2) = n·(n‑1)/2`，大约是 `n²/2`，所以用大白话说就是“时间会随元素数量的平方而增长”。  
  - 空间上只需要常数级别的额外存储（比如一个布尔数组或直接在列表上做原地删除），所以是 `O(1)`。

#### 代码（Python）

```python
def maxOperations_bruteforce(nums, k):
    # 用一个列表记录哪些下标已经被配对，False 表示未使用
    used = [False] * len(nums)
    ops = 0                     # 记录成功配对的次数

    for i in range(len(nums)):
        if used[i]:             # 已经被配对的直接跳过
            continue
        for j in range(i + 1, len(nums)):
            if used[j]:
                continue
            if nums[i] + nums[j] == k:   # 找到一对满足 k 的数
                used[i] = used[j] = True # 标记为已使用
                ops += 1
                break                     # i 对应的数已经配对完，去找下一个 i
    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 需要检查所有的两两组合，`n` 越大，耗时会呈二次方增长。  
- **空间复杂度**：`O(1)` —— 只用了一个与输入等长的布尔数组（可以视作常数额外空间，因为题目只要求 **额外** 空间，不计输入本身）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们一次又一次地遍历剩余的所有元素去找配对，导致二次方的时间。  
要加速，需要**快速判断** “当前数字 `x` 的配对 `k‑x` 是否还剩余”。这正好可以用**哈希表**（字典）来实现——把每个数字出现的次数记下来，类似于“查字典”：键（key）是数字本身，值（value）是它出现的次数。  

**步骤**：

1. **统计频次**：遍历一次数组，把每个数出现的次数放进字典 `cnt`。  
2. **配对**：再次遍历字典的键 `x`。  
   - 如果 `x` 已经配对完（`cnt[x] == 0`），直接跳过。  
   - 设 `y = k - x` 为它的目标配对数。  
   - **两种情况**  
     - **x ≠ y**：可以形成的配对数是 `min(cnt[x], cnt[y])`，因为每对需要各拿走一个 `x` 和一个 `y`。配对后把这两个计数都减去对应的配对数。  
     - **x = y**（即 `x` 正好是 `k/2`）：此时只能把同一个数两两配对，配对数是 `cnt[x] // 2`（向下取整），配对后把计数减掉 `2 * 配对数`。  
3. 把所有配对数累加，就是答案。

**为什么是最优**：  
- 只遍历了两次数组/字典，时间是线性的 `O(n)`。  
- 哈希表的查询、插入、删除都是 `O(1)`（均摊），所以整体保持线性。  
- 只用了额外的字典存放计数，最坏情况下要存 `n` 个不同的数字，空间是 `O(n)`。

如果不想使用额外的哈希表，也可以先把数组排序，然后使用**双指针**（左指针指向最小，右指针指向最大），每次根据两数之和与 `k` 的关系移动指针，这样时间是 `O(n log n)`（排序），空间是 `O(1)`。这里我们先给出哈希表实现，因为思路更直观，随后再简要说明双指针的思路。

#### 代码（Python）  

```python
def maxOperations(nums, k):
    """
    使用哈希表统计每个数的出现次数，然后按配对规则计数。
    时间 O(n) ，空间 O(n)。
    """
    from collections import Counter

    cnt = Counter(nums)          # 统计频次，类似“查字典”
    ops = 0                      # 记录配对次数

    for x in list(cnt.keys()):   # 把键遍历一遍，list() 防止在循环中修改 dict
        if cnt[x] == 0:          # 已经全部配对完的直接跳过
            continue

        y = k - x                 # 目标配对数

        if x == y:                # 特殊情况：x 正好是 k/2，需要两两配对
            pair_num = cnt[x] // 2
            ops += pair_num
            cnt[x] -= pair_num * 2
        else:
            if y not in cnt:      # 字典里根本没有 y，配不了
                continue
            pair_num = min(cnt[x], cnt[y])
            ops += pair_num
            cnt[x] -= pair_num
            cnt[y] -= pair_num

    return ops
```

**双指针（排序）实现（供参考）**  

```python
def maxOperations_two_pointers(nums, k):
    nums.sort()                     # O(n log n)
    left, right = 0, len(nums) - 1
    ops = 0
    while left < right:
        s = nums[left] + nums[right]
        if s == k:                  # 找到一对
            ops += 1
            left += 1
            right -= 1
        elif s < k:                 # 和太小，左指针右移增大和
            left += 1
        else:                       # 和太大，右指针左移减小和
            right -= 1
    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只需要一次遍历统计次数，再一次遍历字典配对。相比暴力的 `O(n²)`，速度提升了 **n 倍**。  
- **空间复杂度**：`O(n)` —— 需要额外的哈希表保存每个不同数字的计数。若采用双指针排序，则空间可以降到 `O(1)`（不计排序时的递归栈），但要付出 `O(n log n)` 的时间代价。

---

## 心得  

- **核心技巧**：利用哈希表统计频次，然后根据“配对数 = `min(cnt[x], cnt[k‑x])`”（或 `cnt[x] // 2`）快速求解。  
- **适用题型**：  
  1. “两数之和 II - 输入有序数组” （双指针）  
  2. “数组中出现最多的 K 次” （计数 + 哈希表）  
  3. “相同元素的最大配对数” （同理使用 `cnt[x] // 2`）  
- **解题钥匙**：**先把“出现次数”记下来，再用“最少的那一方决定配对数”。**  

---

## 反思  

- **第一反应**：看到 “把两个数的和等于 k 且删掉” 就想遍历所有组合——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略了 `x == k - x`（即 `x` 恰好是 `k/2`）的特殊处理，导致配对次数算多或算少。  
  - 在遍历哈希表时直接修改字典，会出现 “运行时错误：字典大小改变”，所以要先把键复制到列表。  
  - 边界情况：数组只有一个元素或全部相同，需要返回 0 或 `len(nums)//2`。  
- **下次第一步**：先 **统计每个数的出现次数**（或排序），再思考 **如何用这些统计信息直接算配对数**，而不是去“一对一”地搜索。这样往往能把时间从二次方降到线性。