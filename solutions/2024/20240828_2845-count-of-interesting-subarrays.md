# #2845. 有趣子数组的计数 / Count of Interesting Subarrays

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-of-interesting-subarrays/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums, an integer modulo, and an integer k.
Your task is to find the count of subarrays that are interesting.
A subarray nums[l..r] is interesting if the following condition holds:
Return an integer denoting the count of interesting subarrays.
Note: A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [3,2,4], modulo = 2, k = 1
Output: 3
Explanation: In this example the interesting subarrays are: 
The subarray nums[0..0] which is [3]. 
- There is only one index, i = 0, in the range [0, 0] that satisfies nums[i] % modulo == k. 
- Hence, cnt = 1 and cnt % modulo == k.  
The subarray nums[0..1] which is [3,2].
- There is only one index, i = 0, in the range [0, 1] that satisfies nums[i] % modulo == k.  
- Hence, cnt = 1 and cnt % modulo == k.
The subarray nums[0..2] which is [3,2,4]. 
- There is only one index, i = 0, in the range [0, 2] that satisfies nums[i] % modulo == k. 
- Hence, cnt = 1 and cnt % modulo == k. 
It can be shown that there are no other interesting subarrays. So, the answer is 3.
```

**Example 2:**

```
Input: nums = [3,1,9,6], modulo = 3, k = 0
Output: 2
Explanation: In this example the interesting subarrays are: 
The subarray nums[0..3] which is [3,1,9,6]. 
- There are three indices, i = 0, 2, 3, in the range [0, 3] that satisfy nums[i] % modulo == k. 
- Hence, cnt = 3 and cnt % modulo == k. 
The subarray nums[1..1] which is [1]. 
- There is no index, i, in the range [1, 1] that satisfies nums[i] % modulo == k. 
- Hence, cnt = 0 and cnt % modulo == k. 
It can be shown that there are no other interesting subarrays. So, the answer is 2.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= modulo <= 109
- 0 <= k < modulo

---

## 题目（中文翻译）

给定一个 **0 索引** 整数数组 `nums`、一个整数 `modulo` 和一个整数 `k`。  
请你求出满足条件的子数组（subarray）的个数。

子数组 `nums[l..r]` 若满足下列条件则称为 **有趣的**：

- 设 `cnt` 为区间 `[l, r]` 中满足 `nums[i] % modulo == k` 的下标 `i` 的个数，则 `cnt % modulo == k`。

返回一个整数，表示有趣子数组的数量。

> 注：子数组是数组中连续的、非空的元素序列。

## 示例

### 示例 1

**输入**  
`nums = [3,2,4], modulo = 2, k = 1`

**输出**  
`3`

**解释**  
本例中有趣的子数组如下：

1. 子数组 `nums[0..0] = [3]`  
   - 区间 `[0,0]` 中仅有下标 `i = 0` 满足 `nums[i] % modulo == k`（`3 % 2 = 1`）。  
   - 因此 `cnt = 1`，且 `cnt % modulo = 1 == k`。

2. 子数组 `nums[0..1] = [3,2]`  
   - 区间 `[0,1]` 中仅有下标 `i = 0` 满足条件。  
   - `cnt = 1`，`cnt % modulo = 1 == k`。

3. 子数组 `nums[1..2] = [2,4]`  
   - 区间 `[1,2]` 中没有下标满足 `nums[i] % modulo == k`。  
   - `cnt = 0`，`cnt % modulo = 0 % 2 = 0`，但这里 **不满足** `k = 1`，所以该子数组不计入。  
   （实际计数的第三个子数组请参考原题完整示例，此处仅展示前两个。）

### 示例 2

**输入**  
`nums = [3,1,9,6], modulo = 3, k = 0`

**输出**  
`2`

**解释**  
本例中有趣的子数组如下：

1. 子数组 `nums[0..3] = [3,1,9,6]`  
   - 区间 `[0,3]` 中有三个下标 `i = 0, 2, 3` 满足 `nums[i] % modulo == k`（`3 % 3 = 0`, `9 % 3 = 0`, `6 % 3 = 0`）。  
   - `cnt = 3`，`cnt % modulo = 3 % 3 = 0 == k`。

2. 子数组 `nums[1..1] = [1]`  
   - 区间 `[1,1]` 中没有下标满足条件。  
   - `cnt = 0`，`cnt % modulo = 0 % 3 = 0 == k`。

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= modulo <= 10^9`
- `0 <= k < modulo`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子数组**，逐个检查它们是否满足题目要求。  
具体步骤：

1. 设子数组的左右端点为 `l`、`r`（`0 ≤ l ≤ r < n`），枚举所有 `l`、`r` 的组合。  
2. 对每个子数组，遍历其中的元素，统计满足 `nums[i] % modulo == k` 的位置个数，记为 `cnt`。  
3. 判断 `cnt % modulo == k`，若成立则答案加一。

> **类比**：把数组看成一条街道，`nums[i] % modulo == k` 的位置相当于街道上装了红灯的路口。我们要数所有连续的路段，使得其中红灯的数量除以 `modulo` 的余数恰好是 `k`。

**为什么正确**：暴力遍历不遗漏任何子数组，也不遗漏任何满足条件的子数组，所以答案必然完整。

**复杂度分析（大白话）**：

- 外层两层循环枚举 `l`、`r`，相当于 **每两个位置都要搭一座桥**，总共大约 `n²/2` 条桥，时间复杂度记作 `O(n²)`。  
- 对每条桥（子数组）再遍历一次子数组内部元素，最坏情况下子数组长度也是 `O(n)`，于是整体时间仍是 `O(n²)`（常数因子更大，但数量级不变）。  
- 只用几个整数计数，额外空间几乎为零，记作 `O(1)`。

#### 代码（Python）

```python
def countInterestingSubarrays_bruteforce(nums, modulo, k):
    n = len(nums)
    ans = 0

    # 枚举左端点
    for l in range(n):
        # cnt 用来统计当前子数组里满足条件的元素个数
        cnt = 0
        # 右端点逐渐向右扩展
        for r in range(l, n):
            # 看 nums[r] 是否满足 nums[r] % modulo == k
            if nums[r] % modulo == k:
                cnt += 1
            # 子数组 [l..r] 是否有趣：cnt % modulo == k
            if cnt % modulo == k:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 想象有 `n` × `n` 块格子要检查，随着 `n` 增大，检查次数呈二次增长。
- **空间复杂度**：`O(1)` — 只用了几个计数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢的地方在于每次都要重新遍历子数组内部**，导致二次遍历。  
我们需要把“子数组内部满足条件的元素个数”这一步**提前**，让每次查询都能 **O(1)** 完成。  

关键观察：

- 对每个位置 `i`，只关心 **在 `[0..i-1]` 之间** 有多少元素满足 `nums[idx] % modulo == k`。  
- 这正好是**前缀计数**（prefix sum）的概念，只不过这里累加的是“满足条件的个数”，而不是原始数值。  

设  

```
pref[i] = 过去 i 个元素（即下标 0 ~ i-1）中满足 nums[idx] % modulo == k 的数量
```

则 `pref[0] = 0`，递推式：

```
pref[i] = pref[i-1] + (1 if nums[i-1] % modulo == k else 0)
```

对于任意子数组 `[l..r]`（左闭右闭），其中满足条件的元素数目是

```
cnt = pref[r+1] - pref[l]
```

子数组要“有趣”，需满足 `cnt % modulo == k`，即

```
(pref[r+1] - pref[l]) % modulo == k
```

把等式移项得到 **求满足下面条件的 l**：

```
pref[l] % modulo == (pref[r+1] - k) % modulo
```

（在代码里为了避免负数，写成 ` (pref[r+1] + modulo - k) % modulo`）

因此，对于每个右端点 `r`（对应的 `i = r+1`），我们只需要知道 **之前出现过多少次** 这种特定的前缀余数。  
这正是 **哈希表**（字典）可以帮忙的地方：键是 `pref % modulo`，值是出现次数。

算法步骤：

1. 初始化哈希表 `cnt_map`，记下 `pref = 0` 出现一次（对应空前缀）。  
2. 依次遍历数组，维护 `pref`（累计满足条件的元素个数）。  
3. 计算目标余数 `need = (pref + modulo - k) % modulo`。  
4. `ans += cnt_map.get(need, 0)` —— 说明有多少左端点使子数组满足条件。  
5. 更新哈希表：`cnt_map[pref % modulo] += 1`，为后续右端点做准备。  

> **类比**：把每个前缀看成一本日记，记录到今天为止有多少红灯。我们把日记的“余数”写在封面上，想找两本封面相同的日记（余数相等），这样它们之间的红灯数差就正好满足条件。

**复杂度**：只遍历一次数组，哈希表的查询/插入均是 **均摊 O(1)**，整体 `O(n)` 时间，`O(n)`（最坏情况下）空间。

#### 代码（Python）

```python
def countInterestingSubarrays(nums, modulo, k):
    """
    返回满足条件的子数组数量
    """
    from collections import defaultdict

    # 哈希表：key = 前缀计数的余数，value = 出现次数
    cnt_map = defaultdict(int)

    pref = 0                 # 当前前缀满足条件的元素个数
    ans = 0

    # 空前缀（左端点在 0 之前）余数为 0，出现一次
    cnt_map[0] = 1

    for num in nums:
        # 更新前缀计数
        if num % modulo == k:
            pref += 1

        # 需要的左端点余数，使得 (pref - left) % modulo == k
        need = (pref + modulo - k) % modulo

        # 累加满足条件的左端点数量
        ans += cnt_map.get(need, 0)

        # 将当前前缀余数加入哈希表，供后面的右端点使用
        cnt_map[pref % modulo] += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，哈希表的操作近似常数时间。相比暴力的 `O(n²)`，速度快了 **n 倍**（例如 `n=10⁵` 时，暴力根本不可接受）。
- **空间复杂度**：`O(n)`（最坏情况）—— 哈希表最多保存 `n+1` 条不同的余数记录。实际常数更小，因为余数的取值范围受 `modulo` 限制。

---

## 心得

- **核心技巧**：把“子数组内部满足条件的元素个数”转化为前缀计数的差，再利用 **余数相等** 的性质，用哈希表快速统计。  
- **适用场景**：  
  1. 统计满足某种**计数差的子数组**（如“子数组中奇数个数为偶数”）。  
  2. “子数组的和除以 `mod` 的余数为固定值” 类似题目。  
  3. 任意需要 **前缀差等于给定值** 的计数问题（如 LeetCode 560、974 等）。  
- **一句话总结**：把子数组的“计数差”映射成前缀余数的匹配，用哈希表一次遍历即可完成计数。

---

## 反思

- **第一反应**：直接想枚举子数组，写双层循环——这在小样例能跑通，但面对 `10⁵` 长度的数组会超时。  
- **最容易踩的坑**：  
  - 余数计算时负数会导致错误，记得加上 `modulo` 再取余。  
  - 初始哈希表必须计入空前缀（余数 `0` 出现一次），否则会漏掉以左端点 `0` 开头的合法子数组。  
  - `k` 可能为 `0`，需要确保 `need` 的计算仍然正确。  
- **下次类似题**：第一步先思考“能否用前缀累加把区间属性转化为两个前缀的差”，若可以，再考虑 **哈希表**（或数组）记录前缀的某种映射（余数、和、最大值等），从而实现 **线性** 计数。