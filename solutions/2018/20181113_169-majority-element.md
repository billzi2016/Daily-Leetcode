# #169. 多数元素 / Majority Element

> 难度：简单 · 标签：Array、Hash Table、Divide and Conquer、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/majority-element/)

---

## 题目（英文原版）

**Description**

Given an array nums of size n, return the majority element.
The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

**Examples**

**Example 1:**

```
Input: nums = [3,2,3]
Output: 3
```

**Example 2:**

```
Input: nums = [2,2,1,1,1,2,2]
Output: 2
```

**Constraints**

- n == nums.length
- 1 <= n <= 5 * 104
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个大小为 `n` 的整数数组 `nums`，返回多数元素（majority element）。  
多数元素是指在数组中出现次数严格大于 ⌊n / 2⌋ 次的元素。你可以假设数组中一定存在多数元素。

示例 1:
```
Input: nums = [3,2,3]
Output: 3
```

示例 2:
```
Input: nums = [2,2,1,1,1,2,2]
Output: 2
```

约束条件：
- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里每一个数字都“数一遍”，看它出现了多少次，哪个次数超过了 `⌊n/2⌋`，那就是多数元素。  

- **使用的数据结构**：我们可以用 **哈希表**（在 Python 里是 `dict`）来记录每个数字出现的次数。哈希表就像一本字典，**key** 是单词（这里是数组中的数字），**value** 是对应的页码（这里是出现次数），查找、插入的速度都很快。  
- **为什么正确**：题目保证一定存在多数元素，只要我们把所有元素的出现次数都算出来，必然会有一个计数大于 `n/2`，直接返回它即可。  

#### 代码（Python）

```python
from typing import List

def majorityElement(nums: List[int]) -> int:
    # 用字典统计每个数出现的次数
    count = {}                     # key: 数字，value: 出现次数
    for num in nums:
        if num in count:
            count[num] += 1        # 已经出现过，次数加一
        else:
            count[num] = 1         # 第一次出现，次数设为 1

    # 遍历字典，找到出现次数超过 n//2 的数字
    n = len(nums)
    for num, freq in count.items():
        if freq > n // 2:          # 大于数组长度的一半
            return num
    # 题目保证一定有答案，这里永远不会走到下面
    raise ValueError("No majority element")
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历数组一次（`O(n)`）再遍历哈希表一次（最多也是 `O(n)`），所以整体是线性时间。  
- **空间复杂度**：`O(k)`，`k` 为不同数字的种类数。最坏情况下每个数字都不相同，`k = n`，因此最坏空间是 `O(n)`。  

---

### 2. 最优解

#### 思路  

虽然上面的哈希表解已经是线性时间，但它用了额外的 `O(n)` 空间。我们可以进一步压缩空间，做到 **O(1) 额外空间**。  

**慢在哪里？**  
- 统计次数需要保存每个数字的计数，这本身就占用了额外的内存。  
- 实际上我们不需要知道每个数字具体出现了多少次，只要找到「多数」这个「占多数」的特性即可。  

**核心算法：Boyer–Moore 投票算法**  
- 把数组想象成一场选举，**候选人**（candidate）是当前可能的多数元素，**票数**（vote）表示我们对候选人的信心。  
- 初始没有候选人，票数为 0。遍历数组：
  - 如果票数为 0，就把当前元素设为新的候选人，并把票数设为 1。  
  - 否则，比较当前元素和候选人是否相同：相同则票数加 1，不同则票数减 1。  
- 为什么会得到正确答案？因为多数元素出现的次数 > 其余所有元素之和。即使我们把多数元素和非多数元素两两抵消，最后剩下的仍然是多数元素。  

**类比**：想象一堆红球和蓝球，红球数量超过蓝球。我们每次拿出两球，如果颜色相同就保留一球（相当于票数加），如果不同就把两球都扔掉（相当于票数减）。最终剩下的球一定是红球，即多数元素。  

#### 代码（Python）

```python
from typing import List

def majorityElement(nums: List[int]) -> int:
    # 第一步：寻找候选人
    candidate = None   # 暂时的多数候选人
    vote = 0           # 对候选人的信任票数

    for num in nums:
        if vote == 0:          # 没有候选人，选当前元素
            candidate = num
            vote = 1
        elif num == candidate:  # 与候选人相同，票数加一
            vote += 1
        else:                    # 与候选人不同，票数减一
            vote -= 1

    # 由于题目保证一定有多数元素，这里直接返回 candidate
    return candidate
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每一步都是常数时间操作。  
- **空间复杂度**：`O(1)`  
  只使用了几个额外变量（`candidate`、`vote`），不随输入规模增长。

---

## 心得

- **核心技巧**：**Boyer–Moore 投票算法**——利用「多数」的定义，通过抵消消除非多数元素，只保留可能的多数候选人。  
- **适用的题型**：  
  1. **多数元素 II**（出现超过 ⌊n/3⌋ 次的元素）——需要稍微改进投票算法。  
  2. **寻找出现次数超过 n/2 的字符**（字符串版的多数元素）。  
  3. **找出数组中出现次数超过 ⌊n/k⌋ 的元素**（更一般化的多数问题）。  
- **一句话总结**：多数元素题的解题钥匙是“**抵消法**”，把相互抵消的不同元素剔除，剩下的必是多数。

---

## 反思

- **第一反应**：直接想到用哈希表计数，因为这最直观、最容易实现。  
- **最容易踩的坑**：  
  - 忘记题目已经保证存在多数元素，导致在投票算法后还要再遍历一次验证（其实可以省略）。  
  - 在实现哈希表时误把 `>` 写成 `>=`，会在出现恰好 `n/2` 次的元素时错误返回。  
- **下次遇到同类题的第一步**：先问自己“是否只需要出现次数超过一半？”如果是，直接考虑 **Boyer–Moore 投票算法**，把空间压到常数级；如果阈值不是 `n/2`，再考虑哈希表或排序等其他方法。