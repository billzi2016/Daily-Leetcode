# #2997. **使数组的 XOR 等于 K 的最少操作次数** / Minimum Number of Operations to Make Array XOR Equal to K

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-xor-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and a positive integer k.
You can apply the following operation on the array any number of times:
Return the minimum number of operations required to make the bitwise XOR of all elements of the final array equal to k.
Note that you can flip leading zero bits in the binary representation of elements. For example, for the number (101)2 you can flip the fourth bit and obtain (1101)2.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,4], k = 1
Output: 2
Explanation: We can do the following operations:
- Choose element 2 which is 3 == (011)2, we flip the first bit and we obtain (010)2 == 2. nums becomes [2,1,2,4].
- Choose element 0 which is 2 == (010)2, we flip the third bit and we obtain (110)2 = 6. nums becomes [6,1,2,4].
The XOR of elements of the final array is (6 XOR 1 XOR 2 XOR 4) == 1 == k.
It can be shown that we cannot make the XOR equal to k in less than 2 operations.
```

**Example 2:**

```
Input: nums = [2,0,2,0], k = 0
Output: 0
Explanation: The XOR of elements of the array is (2 XOR 0 XOR 2 XOR 0) == 0 == k. So no operation is needed.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 106
- 0 <= k <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个正整数 `k`。  
你可以对数组执行以下操作任意次：

- 选择数组中的任意一个元素，将其二进制表示中的任意一位取反（即 **翻转**）。注意，你可以翻转元素二进制表示中**前导零**所在的位。例如，对数 `(101)_2` 翻转第四位后得到 `(1101)_2`。

返回使得最终数组中所有元素的按位异或（bitwise XOR）结果等于 `k` 所需的**最少操作次数**。

---

### 示例

**示例 1**

```text
Input: nums = [2,1,3,4], k = 1
Output: 2
Explanation:
我们可以按如下方式操作：
- 选中下标为 2 的元素 3，即 `(011)_2`，翻转最高位得到 `(010)_2`，即 2。此时 nums 变为 [2,1,2,4]。
- 选中下标为 0 的元素 2，即 `(010)_2`，翻转最低位得到 `(110)_2`，即 6。此时 nums 变为 [6,1,2,4]。
最终数组的 XOR 为 `6 XOR 1 XOR 2 XOR 4 = 1 = k`，共用了 2 次操作。
```

**示例 2**

```text
Input: nums = [2,0,2,0], k = 0
Output: 0
Explanation:
数组的 XOR 为 `2 XOR 0 XOR 2 XOR 0 = 0 = k`，无需任何操作。
```

---

### 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^6`
- `0 <= k <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次一次地去尝试所有可能的翻转**，直到数组的整体 XOR 等于 `k` 为止。  
可以这么做：

1. 先算出当前数组所有元素的 XOR，记作 `curXor`。  
2. 随机挑选数组中的某个元素，随机挑选它的某一位（包括高位的前导零），把这位 **翻转**（0→1 或 1→0）。  
3. 再重新计算整个数组的 XOR，检查是否已经等于 `k`。  
4. 如果不等，就继续第 2 步，直到成功。

> **类比**：把每个整数想象成一本书的页码，翻转某一位就像在这本书的某一页上改一个字母。我们不停地改字母，直到所有书的内容（所有页码的 XOR）拼在一起恰好得到目标 `k`。

**为什么能对**：只要我们不停地尝试所有可能的翻转，最终必然会出现一种组合使得整体 XOR = `k`（因为可以把每一位都调到想要的状态）。

**为什么慢**：  
- 每次翻转后都要 **重新遍历整个数组** 去求 XOR，时间是 `O(n)`。  
- 可能要翻转 **很多次**（最坏情况每一位都要改），位数大约是 20（因为 `nums[i] ≤ 10⁶`），所以总时间会是 `O(翻转次数 × n)`，在最坏情况下接近 `O(n·logC)`，但实现时如果盲目穷举所有位的组合，时间会爆炸。  
- 空间上只需要保存数组本身，`O(1)` 额外空间。

#### 代码（Python）

```python
def min_operations_bruteforce(nums, k):
    # 计算当前 XOR
    cur = 0
    for v in nums:
        cur ^= v

    ops = 0
    # 暴力尝试：只要 cur != k，就随便翻转一位
    while cur != k:
        # 找到第一个不同的二进制位（从低位往高位）
        diff = cur ^ k               # diff 中 1 的位置就是 cur 与 k 不同的位
        low_bit = diff & -diff       # 取最低位的 1
        # 把数组中任意一个数的对应位翻转，这里随便选第 0 个数
        nums[0] ^= low_bit            # 只翻转一位
        cur ^= low_bit                # 整体 XOR 也随之翻转该位
        ops += 1
    return ops
```

> 代码里每次只翻转 **最低位不同的那一位**，这样能保证最终一定收敛，但仍然是逐步模拟的过程，效率不高。

#### 复杂度

- 时间复杂度：`O(ops × n)`，其中 `ops` 最多是二进制位数（≈20），所以最坏约 `O(n·logC)`，但常数大，实际运行慢。  
- 空间复杂度：`O(1)`（只用了几个额外变量）。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**唯一影响整体 XOR 的是每一位是否被翻转**。  
更进一步思考：

- 当我们把数组中某个元素的第 `i` 位翻转时，**整个数组的 XOR 第 `i` 位也会翻转**，因为 XOR 本质上是“所有位的奇偶性”。  
- 也就是说，**一次操作只能改变整体 XOR 的 **一个** 位**，而不会影响其他位。  

因此，要把整体 XOR 从 `curXor` 变成目标 `k`，**每一位上如果两者相同，就不需要动；如果不同，就必须恰好翻转一次**。  
这就把问题转化为：**统计 `curXor` 与 `k` 在二进制表示下有多少位不同**，也叫 **汉明距离**（Hamming distance）。

计算方法非常简洁：

1. `curXor = XOR of all nums`（一次遍历 O(n)）。  
2. `diff = curXor ^ k`。在二进制里，`diff` 的每个 `1` 表示对应位不同。  
3. **统计 `diff` 中 `1` 的个数**，这就是最少需要的翻转次数。  
   - 常用技巧：`while diff: diff &= diff - 1`（每次去掉最低的 1），时间是 `O(number of 1)`，最多是二进制位数（≈20），可以视为常数。  
   - 也可以使用 Python 内置 `bit_count()`（Python 3.8+）直接得到。

> **类比**：把 `curXor` 看成一本书的原始章节，`k` 是目标章节。我们只需要把两本书不一样的章节 **对应地改一页**，每改一页就是一次操作，改多少页就要多少次。

#### 代码（Python）

```python
def minOperations(nums, k):
    """
    返回使整个数组的 XOR 等于 k 所需的最少翻转次数。
    思路：统计 curXor 与 k 的二进制不同位数。
    """
    # 1. 计算数组整体 XOR
    cur = 0
    for v in nums:
        cur ^= v                     # 逐个异或，O(n)

    # 2. 找出不同的位
    diff = cur ^ k                   # 1 表示该位不同

    # 3. 统计 diff 中 1 的个数（即需要翻转的位数）
    # 方法一：使用 Python 3.8+ 的 int.bit_count()
    return diff.bit_count()

    # 方法二（兼容旧版 Python）：
    # cnt = 0
    # while diff:
    #     diff &= diff - 1            # 去掉最低的 1
    #     cnt += 1
    # return cnt
```

> 代码只遍历一次数组，随后用位运算一次性得到答案，既简洁又高效。

#### 复杂度

- 时间复杂度：`O(n)`。只需要一次遍历求 XOR，随后统计位数的操作最多 20 次（常数级），所以整体线性。  
  - 与暴力解相比，省去了每次重新计算 XOR 的重复工作，直接一次完成。
- 空间复杂度：`O(1)`。只用了几个整数变量，不随输入规模增长。

---

## 心得

- **核心技巧**：*位异或的线性特性* + *汉明距离*。一次翻转只影响整体 XOR 的对应位，问题等价于统计不同位的数量。  
- **适用的题型**  
  1. “把数组的 XOR 变成目标值” 类似题（如 LeetCode 1658、1659）。  
  2. “最少翻转位数使两个数相等” 的位运算题。  
  3. “把所有数的按位与/或/异或达到某个目标” 的贪心/位计数题。  
- **一句话总结解题钥匙**：*整体 XOR 与目标的异或结果的二进制 1 的个数，就是最少操作次数*。

---

## 反思

- **第一反应**：看到“翻转任意位”会想到逐位模拟，甚至尝试 BFS 搜索所有状态。  
- **最容易踩的坑**  
  - 忘记 **“翻转高位的前导零也是允许的”**，导致误以为只能在已有位范围内操作。其实位数是无限的，只要对应位不同就可以翻。  
  - 把 **整体 XOR** 当成每个元素单独考虑，导致多余的循环。  
  - 没注意到 **一次翻转只能改整体 XOR 的一位**，于是尝试一次改多位导致错误。  
- **下次遇到同类题**：第一步先 **求出整体 XOR 与目标的异或**，再 **统计 1 的个数**，这几乎是所有“最少位翻转”问题的通用模板。