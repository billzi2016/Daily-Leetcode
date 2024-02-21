# #2588. 统计美丽子数组的数量 / Count the Number of Beautiful Subarrays

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-beautiful-subarrays/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. In one operation, you can:
A subarray is beautiful if it is possible to make all of its elements equal to 0 after applying the above operation any number of times (including zero).
Return the number of beautiful subarrays in the array nums.
A subarray is a contiguous non-empty sequence of elements within an array.
Note: Subarrays where all elements are initially 0 are considered beautiful, as no operation is needed.

**Examples**

**Example 1:**

```
Input: nums = [4,3,1,2,4]
Output: 2
Explanation: There are 2 beautiful subarrays in nums: [4,3,1,2,4] and [4,3,1,2,4].
- We can make all elements in the subarray [3,1,2] equal to 0 in the following way:
  - Choose [3, 1, 2] and k = 1. Subtract 21 from both numbers. The subarray becomes [1, 1, 0].
  - Choose [1, 1, 0] and k = 0. Subtract 20 from both numbers. The subarray becomes [0, 0, 0].
- We can make all elements in the subarray [4,3,1,2,4] equal to 0 in the following way:
  - Choose [4, 3, 1, 2, 4] and k = 2. Subtract 22 from both numbers. The subarray becomes [0, 3, 1, 2, 0].
  - Choose [0, 3, 1, 2, 0] and k = 0. Subtract 20 from both numbers. The subarray becomes [0, 2, 0, 2, 0].
  - Choose [0, 2, 0, 2, 0] and k = 1. Subtract 21 from both numbers. The subarray becomes [0, 0, 0, 0, 0].
```

**Example 2:**

```
Input: nums = [1,10,4]
Output: 0
Explanation: There are no beautiful subarrays in nums.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 106

---

## 题目（中文翻译）

你得到一个下标从 0 开始的整数数组 `nums`。在一次操作中，你可以：

子数组（subarray）如果能够在任意次数（包括零次）重复上述操作后，使其所有元素都变为 0，则称其为**美丽子数组**（beautiful subarray）。返回数组 `nums` 中美丽子数组的数量。

子数组是数组中连续的、非空的元素序列。

> 注意：所有元素初始即为 0 的子数组也被视为美丽子数组，因为不需要进行任何操作。

### 示例

**示例 1**

> **输入**  
> `nums = [4,3,1,2,4]`  
> **输出**  
> `2`  
> **解释**  
> `nums` 中共有 2 个美丽子数组：`[4,3,1,2,4]` 和 `[4,3,1,2,4]`。  
> - 我们可以通过以下方式使子数组 `[3,1,2]` 中的所有元素变为 0：  
>   1. 选择子数组 `[3,1,2]` 并取 `k = 1`，从每个数中减去 `2^1`，子数组变为 `[1,1,0]`。  
>   2. 再选择子数组 `[1,1,0]` 并取 `k = 0`，从每个数中减去 `2^0`，子数组最终变为 `[0,0,0]`。  
> - （后续步骤省略）

**示例 2**

> **输入**  
> `nums = [1,10,4]`  
> **输出**  
> `0`  
> **解释**  
> `nums` 中不存在美丽子数组。

### 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有子数组**，把每个子数组里的元素依次做异或（XOR），看结果是否为 `0`。  

- **数据结构**：只需要一个普通的整数变量 `cur_xor` 来保存当前子数组的异或值。  
- **生活化类比**：把数组想象成一串灯泡，每盏灯的亮暗状态用二进制表示。把若干盏灯连在一起（子数组），把它们的状态“异或”起来，就像把每盏灯的开关一次次按下，最终如果所有灯都熄灭（结果是 `0`），说明这段灯串是“美丽的”。  

**为什么正确**  
- 异或的性质：`a ^ a = 0`，`a ^ 0 = a`，且满足结合律、交换律。  
- 子数组 `[l, r]` 的异或值等于 `nums[l] ^ nums[l+1] ^ … ^ nums[r]`。如果这个值恰好为 `0`，说明可以通过题目给出的操作把所有元素变成 `0`（提示已经说明：**美丽子数组 ↔ 子数组异或为 0**），因此直接判断异或是否为 `0` 就能得到答案。

#### 代码（Python）

```python
def count_beautiful_subarrays_bruteforce(nums):
    n = len(nums)
    ans = 0
    # 枚举左端点
    for left in range(n):
        cur_xor = 0               # 当前子数组的异或值
        # 枚举右端点
        for right in range(left, n):
            cur_xor ^= nums[right]    # 把右边新加入的元素异或进来
            if cur_xor == 0:          # 若异或结果为 0，则子数组[left, right] 美丽
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n` 是数组长度。外层循环 `n` 次，内层平均也要遍历 `≈ n/2` 次，总共约 `n²/2` 次操作。  
  - 大白话：如果数组有 10,000 个元素，暴力解要检查大约一亿次子数组，显然会超时。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，不随 `n` 增长。  

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要从左端点重新遍历到右端点，导致二次循环。我们可以利用 **前缀异或** 的性质把子数组的异或值在 **O(1)** 时间内算出来，从而把整体时间降到 **线性**。

**关键观察**  

- 定义 `pre[i]` 为前 `i` 个元素的异或（`pre[0] = 0`，`pre[i] = nums[0] ^ nums[1] ^ … ^ nums[i-1]`）。  
- 子数组 `[l, r]`（左闭右闭）的异或等于 `pre[l] ^ pre[r+1]`。  
  - 解释：`pre[r+1]` 包含了 `0 … r` 的全部异或，`pre[l]` 包含了 `0 … l-1` 的异或，两者相异（^）就把前面多余的部分抵消，只剩下 `l … r`。  
- 要让子数组异或为 `0`，只需满足 `pre[l] ^ pre[r+1] = 0`，即 **`pre[l] == pre[r+1]`**。  

于是问题转化为：**在前缀异或数组中，有多少对相同的值**（下标 `i < j`），每对对应一个美丽子数组。

**如何快速计数**  

- 从左到右遍历数组，实时维护 **哈希表**（字典）`cnt`，记录每个前缀异或出现的次数。  
- 当我们计算到第 `i` 个元素后得到当前前缀异或 `cur`，如果 `cnt[cur]` 之前已经出现了 `k` 次，说明有 `k` 个左端点使得子数组异或为 `0`，所以答案累加 `k`。  
- 最后把当前 `cur` 的出现次数加一，继续向右推进。  

**类比**：哈希表就像一本“词典”，`key` 是“前缀异或的值”，`value` 是“这个值出现了几次”。每次我们看到一个已经在词典里的词，就可以立刻把它对应的次数加到答案上。

#### 代码（Python）

```python
def count_beautiful_subarrays(nums):
    """
    返回 nums 中异或为 0 的子数组个数
    """
    from collections import defaultdict

    cnt = defaultdict(int)   # 哈希表：前缀异或 -> 出现次数
    cnt[0] = 1                # 前缀异或为 0 的空前缀，方便统计以第一个元素起始的子数组
    cur = 0                   # 当前前缀异或
    ans = 0

    for x in nums:
        cur ^= x              # 更新前缀异或，等价于 pre[i+1]
        # 如果之前出现过相同的前缀异或，那么每一次出现都对应一个美丽子数组
        ans += cnt[cur]       # 累加已有的相同前缀异或的次数
        cnt[cur] += 1         # 把当前前缀异或计数加一，供后续使用

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每一步的哈希表查询/插入都是 **均摊 O(1)**。  
  - 与暴力 `O(n²)` 相比，速度提升了一个量级：如果 `n = 10⁵`，只需要约 `10⁵` 次操作，轻松跑完。

- **空间复杂度**：`O(n)`（最坏情况）  
  - 哈希表最多会存储 `n+1` 个不同的前缀异或值。  
  - 这相当于我们为每个位置都记了一张“小票”，在本题的约束（`n ≤ 10⁵`）下完全可接受。

---

## 心得

- **核心技巧**：利用前缀异或把子数组异或转化为“两个前缀相等”，再配合哈希表计数。  
- **适用的题型**  
  1. “子数组异或为 K”——把目标异或值 `K` 移到哈希表查询中（`pre[i] ^ K`）。  
  2. “子数组和为 0 / K”——同理使用前缀和 + 哈希表。  
  3. “最长子数组满足某种前缀关系”——常用前缀 + 哈希表或单调栈。  
- **一句话总结**：**把子数组的问题抽象成前缀的等价对，用哈希表把等价对数目瞬间统计出来**。

---

## 反思

- **第一反应**：看到“子数组美丽”且提示“xor 为 0”，立刻想到“前缀异或”。  
- **最容易踩的坑**  
  - 忘记在哈希表中先放入 `0` 的计数（代表空前缀），会导致遗漏以第一个元素为左端点的子数组。  
  - 对大整数或负数的异或没有额外处理，因为 Python 的整数是无限精度，直接使用 `^` 即可。  
  - 需要注意 **计数的顺序**：先把当前前缀异或对应的已有次数加到答案，再把自身计数加一，否则会把自己算成子数组（长度为 0 的子数组是不合法的）。  
- **下次第一步**：  
  - 判断子数组的目标值是否可以通过“前缀运算 + 哈希表”转化（如异或、和、乘积的可逆操作），如果可以，就直接走前缀+哈希表的路线。