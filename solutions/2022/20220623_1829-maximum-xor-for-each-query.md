# #1829. 每个查询的最大异或 / Maximum XOR for Each Query

> 难度：中等 · 标签：Array、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-xor-for-each-query/)

---

## 题目（英文原版）

**Description**

You are given a sorted array nums of n non-negative integers and an integer maximumBit. You want to perform the following query n times:
Return an array answer, where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: nums = [0,1,1,3], maximumBit = 2
Output: [0,3,2,3]
Explanation: The queries are answered as follows:
1st query: nums = [0,1,1,3], k = 0 since 0 XOR 1 XOR 1 XOR 3 XOR 0 = 3.
2nd query: nums = [0,1,1], k = 3 since 0 XOR 1 XOR 1 XOR 3 = 3.
3rd query: nums = [0,1], k = 2 since 0 XOR 1 XOR 2 = 3.
4th query: nums = [0], k = 3 since 0 XOR 3 = 3.
```

**Example 2:**

```
Input: nums = [2,3,4,7], maximumBit = 3
Output: [5,2,6,5]
Explanation: The queries are answered as follows:
1st query: nums = [2,3,4,7], k = 5 since 2 XOR 3 XOR 4 XOR 7 XOR 5 = 7.
2nd query: nums = [2,3,4], k = 2 since 2 XOR 3 XOR 4 XOR 2 = 7.
3rd query: nums = [2,3], k = 6 since 2 XOR 3 XOR 6 = 7.
4th query: nums = [2], k = 5 since 2 XOR 5 = 7.
```

**Example 3:**

```
Input: nums = [0,1,2,2,5,7], maximumBit = 3
Output: [4,3,6,4,6,7]
```

**Constraints**

- nums.length == n
- 1 <= n <= 105
- 1 <= maximumBit <= 20
- 0 <= nums[i] < 2maximumBit
- nums​​​ is sorted in ascending order.

---

## 题目（中文翻译）

给定一个长度为 n 的已排序数组 nums，数组中的元素为非负整数，以及一个整数 maximumBit。你需要对该数组执行 n 次查询：

返回一个数组 answer，其中 answer[i] 是第 i 次查询的答案。

---

**示例 1**

```text
Input: nums = [0,1,1,3], maximumBit = 2
Output: [0,3,2,3]
```

**解释**：查询的求解过程如下：
- 第 1 次查询：nums = [0,1,1,3]，k = 0，因为 0 XOR 1 XOR 1 XOR 3 XOR 0 = 3。  
- 第 2 次查询：nums = [0,1,1]，k = 3，因为 0 XOR 1 XOR 1 XOR 3 = 3。  
- 第 3 次查询：nums = [0,1]，k = 2，因为 0 XOR 1 XOR 2 = 3。  
- 第 4 次查询：nums = [0]，k = 3，因为 0 XOR 3 = 3。

---

**示例 2**

```text
Input: nums = [2,3,4,7], maximumBit = 3
Output: [5,2,6,5]
```

**解释**：查询的求解过程如下：
- 第 1 次查询：nums = [2,3,4,7]，k = 5，因为 2 XOR 3 XOR 4 XOR 7 XOR 5 = 7。  
- 第 2 次查询：nums = [2,3,4]，k = 2，因为 2 XOR 3 XOR 4 XOR 2 = 7。  
- 第 3 次查询：nums = [2,3]，k = 6，因为 2 XOR 3 XOR 6 = 7。  
- 第 4 次查询：nums = [2]，k = 5，因为 2 XOR 5 = 7。

---

**示例 3**

```text
Input: nums = [0,1,2,2,5,7], maximumBit = 3
Output: [4,3,6,4,6,7]
```

---

**约束条件**

- `nums.length == n`
- `1 <= n <= 10^5`
- `1 <= maximumBit <= 20`
- `0 <= nums[i] < 2^maximumBit`
- `nums` 按升序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **每一次查询**都把当前数组里所有元素做一次异或（XOR），记为 `curXor`。  
2. 题目要求我们找一个 `k`（`0 ≤ k < 2^maximumBit`），使得  

```
curXor XOR k = 111…111 (maximumBit 位全是 1)
```

   这相当于让 `k` 把 `curXor` 的每一位都“翻转”。  
3. 因为 `111…111` 的十进制值是 `2^maximumBit - 1`，我们只要把 `curXor` 和它异或，就得到答案 `k`：

```
k = curXor XOR (2^maximumBit - 1)
```

暴力实现就是 **每次都重新遍历数组** 求 `curXor`，然后计算 `k`，最后把数组最后一个元素删掉，进入下一轮查询。

> **类比**：把数组想象成一本厚厚的书，想要知道整本书的“总密码” (`curXor`) 时，我们每次都要把所有页面的密码一次读完，显然很慢。

> **为什么正确**：  
> - `curXor XOR k` 的结果正好是全 1（因为 `a XOR b = c` → `b = a XOR c`），满足题目要求的“最大可能 XOR”。  
> - `k` 必然在 `[0, 2^maximumBit)` 范围，因为我们只对 `maximumBit` 位做异或，超出的高位始终是 0。

#### 代码（Python）

```python
from typing import List

def getMaximumXor(nums: List[int], maximumBit: int) -> List[int]:
    n = len(nums)
    mask = (1 << maximumBit) - 1          # 全 1 的掩码，例如 maximumBit=3 时 mask=0b111=7
    ans = []

    # 暴力：每轮都重新遍历剩余的元素求 XOR
    for i in range(n):
        cur_xor = 0
        # 计算当前数组（前 n-i 个元素）的 XOR
        for j in range(n - i):
            cur_xor ^= nums[j]

        # k = cur_xor XOR mask，即把所有位翻转得到最大可能值
        k = cur_xor ^ mask
        ans.append(k)

        # “删除”数组最后一个元素：实际上什么也不需要做，
        # 因为下一轮循环的范围已经缩小了 (n - i - 1)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层循环 `n` 次，内层每次遍历剩余的 `≈ n/2` 个元素，整体是等差求和，约等于 `n²/2`。  
  - 大白话：如果数组有 10,000 个数，最坏情况下要做 10,000 × 5,000 次异或，明显太慢。

- **空间复杂度**：`O(1)`（不计输出数组）  
  - 只用了常数个额外变量 `mask、cur_xor、k`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每轮都要重新遍历求 XOR**。  
实际上，**前缀异或**（或后缀异或）可以让我们把每轮的 `curXor` 复用起来，省去重复计算。

关键观察：

1. **异或的可逆性**：`a XOR b = c` → `a = c XOR b`。  
   当我们从数组右侧依次删除元素时，`curXor` 只需要把被删掉的元素再 **异或一次**（因为 `x XOR x = 0`）。

2. 设 `totalXor` 为原始完整数组的异或值。  
   第一次查询的 `curXor = totalXor`。  
   删除最右边的元素 `nums[-1]` 后，第二次查询的 `curXor = totalXor XOR nums[-1]`。  
   再删除 `nums[-2]`，`curXor = totalXor XOR nums[-1] XOR nums[-2]`，依此类推。

3. 因此我们只需要一次遍历把 **所有元素的异或**算出来（`totalXor`），随后再 **逆序遍历** 数组，每一步把当前元素再异或进 `curXor`，即可得到每轮的 `curXor`。

4. 与暴力解相同，答案 `k` 仍然是 `curXor XOR mask`，其中 `mask = 2^maximumBit - 1`（全 1）。

> **类比**：把数组想象成一根绳子，上面系了若干结（每个数）。一次把整根绳子拉直得到 `totalXor`，然后每次解掉最右边的结，只需要把这个结的“力量”再从总力量里减去（异或），不需要重新把所有结都拉一遍。

#### 代码（Python）

```python
from typing import List

def getMaximumXor(nums: List[int], maximumBit: int) -> List[int]:
    mask = (1 << maximumBit) - 1          # 全 1 的掩码，例如 maximumBit=3 时 mask=7
    n = len(nums)

    # 1️⃣ 先算出完整数组的异或值 total_xor
    total_xor = 0
    for num in nums:
        total_xor ^= num

    ans = []
    cur_xor = total_xor                   # 第一次查询的 cur_xor 就是 total_xor

    # 2️⃣ 逆序遍历，每一步都把当前元素再异或一次，得到本轮的 cur_xor
    for i in range(n - 1, -1, -1):
        # k = cur_xor XOR mask，使得 cur_xor XOR k = mask（全 1）
        k = cur_xor ^ mask
        ans.append(k)                     # 按查询顺序加入答案（先加入第 1 次）

        # 删除最右边的元素：相当于把它再异或进 cur_xor
        cur_xor ^= nums[i]                # 为下一轮准备

    # 逆序遍历得到的 ans 顺序恰好是查询的顺序，无需再翻转
    return ans
```

> **小技巧**：`cur_xor ^= nums[i]` 这一步的意义是“把已经被删除的元素从当前 XOR 中去掉”。因为 `a XOR a = 0`，再 XOR 一遍就相当于把它抵消。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历两遍数组（一次求总异或，一次逆序计算），线性时间。  
  - 与暴力的 `O(n²)` 相比，规模为 `10⁵` 时可以轻松在毫秒级完成。

- **空间复杂度**：`O(1)`（不计输出数组）  
  - 只用了 `mask、total_xor、cur_xor` 三个额外变量。

---

## 心得

- **核心技巧**：利用 **异或的可逆性** + **前缀/后缀异或**，把重复的求 XOR 操作压缩到一次遍历。  
- **适用的题型**：  
  1. “数组/子数组的异或” 类问题（如 “Maximum XOR of Two Numbers in an Array”、 “Subarray XOR Equals K”）。  
  2. 需要 **逐步删除/加入元素** 并实时维护累计信息的问题（如 “滑动窗口求和/异或”、 “动态前缀和”）。  
- **一句话总结**：**把“每次重新算”变成“只算一次，再用异或撤销/加入”。**

---

## 反思

- **第一反应**：看到 “每次都要对当前数组求 XOR”，立刻想到“遍历一次求 XOR”，于是写出了暴力的双层循环。  
- **最容易踩的坑**：  
  - 忘记 `k` 必须在 `[0, 2^maximumBit)` 范围，直接返回 `cur_xor` 会出错。  
  - 没有注意到 `mask = (1 << maximumBit) - 1` 才是 “全 1”。  
  - 在逆序遍历时误把答案顺序翻转，导致输出顺序错误。  
- **下次遇到同类题**，第一步应该问自己：  
  - “这一步的计算是否可以通过累计/撤销的方式在 O(1) 完成？”  
  - “是否有全 1（或全 0）这样固定目标，让我只需要一次异或就能得到答案？”  

这样思考可以迅速从 “暴力遍历” 跳到 “前缀/后缀累计” 的最优解。