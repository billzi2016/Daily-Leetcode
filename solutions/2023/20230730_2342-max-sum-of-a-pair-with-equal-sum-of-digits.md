# #2342. 相同数位和的数对的最大和 / Max Sum of a Pair With Equal Sum of Digits

> 难度：中等 · 标签：Array、Hash Table、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/max-sum-of-a-pair-with-equal-sum-of-digits/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of positive integers. You can choose two indices i and j, such that i != j, and the sum of digits of the number nums[i] is equal to that of nums[j].
Return the maximum value of nums[i] + nums[j] that you can obtain over all possible indices i and j that satisfy the conditions. If no such pair of indices exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [18,43,36,13,7]
Output: 54
Explanation: The pairs (i, j) that satisfy the conditions are:
- (0, 2), both numbers have a sum of digits equal to 9, and their sum is 18 + 36 = 54.
- (1, 4), both numbers have a sum of digits equal to 7, and their sum is 43 + 7 = 50.
So the maximum sum that we can obtain is 54.
```

**Example 2:**

```
Input: nums = [10,12,19,14]
Output: -1
Explanation: There are no two numbers that satisfy the conditions, so we return -1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的正整数数组（array）`nums`。你可以选择两个下标 `i` 和 `j`（`i != j`），要求 `nums[i]` 与 `nums[j]` 的各位数字之和（sum of digits）相等。返回在所有满足条件的下标对 `(i, j)` 中，`nums[i] + nums[j]` 的最大可能值。如果不存在满足条件的下标对，返回 `-1`。

**示例 1**  
**Input:** `nums = [18,43,36,13,7]`  
**Output:** `54`  
**Explanation:** 满足条件的下标对有：  
- `(0, 2)`，两个数的数位和均为 `9`，它们的和为 `18 + 36 = 54`。  
- `(1, 4)`，两个数的数位和均为 `7`，它们的和为 `43 + 7 = 50`。  
因此能够得到的最大和为 `54`。

**示例 2**  
**Input:** `nums = [10,12,19,14]`  
**Output:** `-1`  
**Explanation:** 没有任意两数的数位和相等，故返回 `-1`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组里每两个不同下标的数都拿出来检查：

1. 计算 `nums[i]` 的各位数字之和（把数字想象成一本书，求它的“字数”）。  
2. 再计算 `nums[j]` 的各位数字之和。  
3. 如果这两个“字数”相同，就把 `nums[i] + nums[j]` 记下来，最后取最大的那个。

> **数据结构**：只需要一个普通的整数变量来保存当前最大和。  
> **生活化类比**：把 `哈希表` 想成查字典——键是“字数”，值是对应的数字。暴力解根本不需要字典，只是逐个比较，像是两个人手拉手逐个检查是否生日相同。

**为什么这个方法一定能得到答案**  
因为我们把所有可能的 `(i, j)`（i ≠ j）都遍历了一遍，只要有满足条件的配对，必然会被比较到并记录其和。于是最大值必然被找出来。

**时间/空间复杂度**  
- **时间**：我们要检查每一对数，数组长度记为 `n`，所以检查次数是 `C(n,2) = n·(n‑1)/2`，数量级为 `O(n²)`。  
  - **大白话**：如果 `n = 10⁴`，那么需要比较大约 5 × 10⁷ 次，明显会超时。
- **空间**：只用了常数个额外变量，`O(1)`。

#### 代码（Python）

```python
def sum_of_digits(x: int) -> int:
    """计算整数 x 各位数字之和。"""
    s = 0
    while x:
        s += x % 10          # 取最后一位
        x //= 10             # 去掉最后一位
    return s

def maxSum(nums):
    n = len(nums)
    ans = -1                 # 记录最大和，默认 -1 表示没有合法配对
    for i in range(n):
        for j in range(i + 1, n):      # 只看 i < j，避免重复和 i == j
            if sum_of_digits(nums[i]) == sum_of_digits(nums[j]):
                cur = nums[i] + nums[j]
                if cur > ans:
                    ans = cur
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有数对，随着 `n` 增大，运行时间呈二次方增长。
- **空间复杂度**：`O(1)` —— 只用了几个临时变量，没有额外的随 `n` 增长的数据结构。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每一对都要比较一次**，而题目只关心“数字之和相同”的配对。我们可以把所有数字按照“各位和”分组，然后**只在同一组内部寻找最大的两个数**，因为只有这两个数的和才可能是该组的最大和。

**步骤拆解**：

1. **计算每个数的位和**。这一步仍然是 O(1)（因为 `nums[i] ≤ 10⁹`，最多 10 位），可以写成一个小函数。  
2. **使用哈希表（Python 的 dict）**，键是位和，值是当前已见到的**最大的两个数**（用列表保存，长度 ≤ 2）。  
   - 类比：把每个“字数”当成一本字典的条目，字典里记录这本书里最大、第二大的章节页码。  
3. **遍历数组**：对每个数 `x`  
   - 计算 `digit_sum = sum_of_digits(x)`。  
   - 取出 `hash[digit_sum]`（如果不存在则创建空列表）。  
   - 将 `x` 插入列表并保持列表从大到小排序，只保留前两名。  
   - 这样遍历完后，每个键对应的列表里就是该位和组的前两大数。  
4. **计算答案**：再次遍历哈希表，对每个键的列表  
   - 若列表长度为 2，则这两个数的和是该组的候选答案。  
   - 取所有候选答案的最大值即为最终答案。  

**为什么只保留前两大数就够了**  
因为我们只需要**两数之和的最大值**。在同一组里，任意两数的和 ≤ 最大数 + 第二大数。若我们把更小的数也放进去，它们不可能超过这个上界，所以可以安全丢弃。

**核心数据结构**：**哈希表**（字典）+ **固定大小的列表**。  
- 哈希表的查找/插入是 `O(1)`（均摊），相当于在字典里快速定位对应的“字数”。  
- 列表长度始终 ≤ 2，排序或插入的代价是常数。

**类比/图示**（文字版）：

```
位和 = 9   ->  [36, 18]   （最大的两个数）
位和 = 7   ->  [43, 7]
位和 = 5   ->  [5]        （只有一个，无法构成配对）
```

最后只看长度为 2 的组，取 `36+18 = 54`、`43+7 = 50`，最大的是 54。

#### 代码（Python）

```python
def sum_of_digits(x: int) -> int:
    """返回整数 x 各位数字之和。"""
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def maxSum(nums):
    """返回满足「位和相同」的两数之和的最大值，若不存在返回 -1。"""
    groups = {}                     # key: 位和, value: 前两大的数（降序列表）

    for x in nums:
        d = sum_of_digits(x)        # 计算位和

        # 取出当前组的列表，若不存在则创建空列表
        lst = groups.get(d)
        if lst is None:
            lst = []
            groups[d] = lst

        # 将 x 插入 lst 并保持降序，只保留前两名
        # 由于 lst 长度最多为 2，直接线性插入即可
        if len(lst) == 0:
            lst.append(x)
        elif len(lst) == 1:
            if x >= lst[0]:
                lst.insert(0, x)    # x 更大，放在前面
            else:
                lst.append(x)       # x 更小，放在后面
        else:  # len == 2
            if x > lst[0]:
                lst[1] = lst[0]     # 原最大变为第二大
                lst[0] = x          # x 成为最大
            elif x > lst[1]:
                lst[1] = x          # x 成为第二大
        # 若插入后列表长度超过 2，截断（这里不会发生）

    ans = -1
    for lst in groups.values():
        if len(lst) == 2:            # 只有两个或以上才能配对
            cur = lst[0] + lst[1]
            if cur > ans:
                ans = cur
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个数只做一次位和计算（最多 10 次除法/取余）和一次哈希表操作（均摊 O(1)），整体随 `n` 线性增长。  
  - 与暴力解的 `O(n²)` 相比，提升巨大：比如 `n = 10⁵` 时，暴力需要约 5·10⁹ 次比较，而最优解只需要约 10⁵ 次。

- **空间复杂度**：`O(m)`，其中 `m` 是不同位和的种类数。  
  - 位和的最大可能值是 `9 * 10 = 90`（因为 `nums[i] ≤ 10⁹`，最多 10 位，每位最大 9），所以 `m ≤ 91`，可以看作是常数级别的额外空间。  
  - 换句话说，哈希表最多存 91 条记录，每条记录只保存两条整数，几乎不占内存。

---

## 心得

- **核心技巧**：**把元素按某个属性分组（哈希表） + 只保留每组的前 k 大元素**。  
- **适用的题型**  
  1. “相同字符计数的最大乘积”之类的分组取最大/第二大。  
  2. “相同余数的两数之和最大”或 “相同奇偶性/相同位数”等属性分组。  
  3. “相同频率的字符最长子串”等需要分组后取极值的题目。
- **一句话总结解题钥匙**：**先把问题压缩到“同类中挑最优”，再用哈希表一次遍历完成**。

---

## 反思

- **第一反应**：看到“位和相同”，马上想到“把位和作为键分组”。但如果直接想到要排序整个数组再遍历，可能会多余地使用 `O(n log n)`。
- **最容易踩的坑**  
  - **位和的取值范围**：不要误以为是 `10⁹`，实际上最多只有 90（9 × 10 位），这保证了哈希表大小是常数。  
  - **同一数字出现多次**：即使两个相同的数下标不同，也可以配对，记得不要因为值相同就忽略。  
  - **只保留两大时的更新逻辑**：要确保在插入新数时正确维护降序，否则可能错过真正的最大和。  
- **下次遇到同类题**：第一步先**明确可以用哈希表分组的属性**，然后**思考每组只需要哪些极值（最大/最小/前 k）**，最后用一次遍历完成统计。这样既能避免 O(n²) 的暴力，又能保持代码简洁。