# #3591. 检查是否存在出现次数为素数的元素 / Check if Any Element Has Prime Frequency

> 难度：简单 · 标签：Array、Hash Table、Math、Counting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/check-if-any-element-has-prime-frequency/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Return true if the frequency of any element of the array is prime, otherwise, return false.
The frequency of an element x is the number of times it occurs in the array.
A prime number is a natural number greater than 1 with only two factors, 1 and itself.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5,4]
Output: true
Explanation:
4 has a frequency of two, which is a prime number.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: false
Explanation:
All elements have a frequency of one.
```

**Example 3:**

```
Input: nums = [2,2,2,4,4]
Output: true
Explanation:
Both 2 and 4 have a prime frequency.
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`。

如果数组中任意元素的出现次数（frequency）是素数（prime），返回 `true`；否则返回 `false`。

元素 `x` 的出现次数是指它在数组中出现的次数。

素数（prime number）是大于 1 的自然数，且仅有两个因子：1 和它本身。

**示例 1**  
Input: `nums = [1,2,3,4,5,4]`  
Output: `true`  
**Explanation**:  
4 的出现次数为 2，2 是素数。

**示例 2**  
Input: `nums = [1,2,3,4,5]`  
Output: `false`  
**Explanation**:  
所有元素的出现次数都是 1。

**示例 3**  
Input: `nums = [2,2,2,4,4]`  
Output: `true`  
**Explanation**:  
2 和 4 的出现次数都是素数。

**约束条件**  
- `1 <= nums.length <= 100`  
- `0 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **对每个元素都去遍历整个数组，统计它出现了多少次**，得到每个元素的出现次数（频率）后，再判断这些频率里是否有质数。

- **数据结构**：这里我们不使用额外的哈希表，而是直接用两个循环。可以把第一个循环想象成“把每个人的名字叫出来”，第二个循环则是“在全班里找有多少人和他同名”。  
- **为什么正确**：因为我们把每个不同的数都完整地计数了一遍，所有频率都被算出来了，只要其中有一个是质数，就返回 `True`，否则返回 `False`。  
- **复杂度**：  
  - 外层遍历 `n` 次，内层每次最坏也要遍历 `n` 次，所以总共大约是 `n × n = n²` 次操作。用大白话说，就是如果数组长度是 10，最多要比较 100 次；如果是 100，则要比较 10,000 次。  
  - 额外空间只用了几个计数变量，和数组大小无关，记作 **O(1)**（常数空间）。

#### 代码（Python）

```python
def is_prime(num: int) -> bool:
    """判断一个整数是否为质数（>1且只能被1和它本身整除）"""
    if num <= 1:
        return False          # 1 及以下都不是质数
    # 只需要检查到 sqrt(num) 就够了
    i = 2
    while i * i <= num:
        if num % i == 0:       # 能被整除说明不是质数
            return False
        i += 1
    return True                # 没有发现因子，说明是质数

def prime_frequency_brute(nums):
    n = len(nums)
    # 对每个位置的元素统计它出现的次数
    for i in range(n):
        cnt = 0
        for j in range(n):
            if nums[j] == nums[i]:   # 和第 i 个元素相同就计数
                cnt += 1
        # 只要出现次数是质数，就直接返回 True
        if is_prime(cnt):
            return True
    # 所有元素的出现次数都不是质数
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 两层循环每层最多遍历 `n` 次，整体是 `n` 的平方。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，没有随输入规模增长的额外存储。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于重复遍历数组**：每次统计频率都要把整个数组扫一遍。  
我们可以把“统计每个数出现了多少次”这件事 **一次性完成**，这正是 **哈希表（在 Python 里叫 dict）** 的擅长之处：把“数”当作 **key**，出现次数当作 **value**，一遍遍历就把所有频率记下来。

优化步骤：

1. **一次遍历**：用 `dict` 把每个数的出现次数累计。可以把 `dict` 想象成“字典”，查找某个单词的解释只需要一次翻页，和遍历整个书本相比快得多。  
2. **检查质数**：遍历 `dict` 中所有的频率，只要有一个是质数就返回 `True`。这里的质数判断仍然使用前面写的 `is_prime`，因为 `nums` 长度最多 100，频率最多也是 100，直接用 **试除法到 √freq** 完全足够。  
3. **提前结束**：一旦找到质数频率就可以立刻返回，省掉后面的检查。

#### 代码（Python）

```python
def is_prime(num: int) -> bool:
    """判断正整数 num 是否为质数（>1且只能被1和它本身整除）"""
    if num <= 1:
        return False
    i = 2
    while i * i <= num:          # 只需检查到 sqrt(num)
        if num % i == 0:
            return False
        i += 1
    return True

def prime_frequency_opt(nums):
    """最优解：利用哈希表一次遍历统计频率，再检查是否有质数频率"""
    freq = {}                     # key: 元素值，value: 出现次数
    for x in nums:                # O(n) 只遍历一次
        freq[x] = freq.get(x, 0) + 1   # 字典的 get 方法类似查字典，找不到返回默认 0

    # 遍历所有频率，只要出现一次质数就返回 True
    for count in freq.values():   # O(k)，k 为不同元素的个数，k ≤ n
        if is_prime(count):
            return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n + m√m)`，其中 `n` 是数组长度（这里最多 100），`m` 是出现次数的最大值（同样 ≤ 100）。实际上 `m√m` 远小于 `n²`，在本题的约束下几乎可以视作 `O(n)`。  
  - 解释：一次遍历 `O(n)`，随后遍历哈希表的所有频率（最多 `n` 项），每个频率的质数检查最多到 `√m`（不超过 10），所以整体仍是线性级别。  
- **空间复杂度**：`O(k)`，需要额外的哈希表来保存不同元素的计数，`k` 是不同元素的数量，最坏情况 `k = n`，即 `O(n)`。在本题中最多 100，属于常数级别的额外空间。

---

## 心得

- **核心技巧**：利用哈希表（字典）一次遍历完成“计数”，再配合**质数判定**。  
- **适用的题型**  
  1. “出现次数是否满足某种条件”——如 **“出现次数是否为偶数”**、**“出现次数是否为 3 的倍数”** 等。  
  2. “找出出现次数最多/最少的元素”。  
  3. “判断是否存在出现次数相同的两个不同元素”（使用计数的哈希表再比较）。  
- **一句话总结解题钥匙**：**用字典把每个数的出现次数一次性记下来，再检查这些次数中是否出现质数**。

---

## 反思

- **第一反应**：看到“频率”和“质数”，立刻想到“先统计频率”。很多人会直接写两层循环，这也是最自然的想法。  
- **最容易踩的坑**  
  - **质数的定义**：1 不是质数，忘记这点会导致错误的 `True`。  
  - **频率为 0 的情况**：不存在，但在写 `is_prime` 时要确保只在大于 1 时返回 `True`。  
  - **边界条件**：数组长度为 1 时频率都是 1，答案应为 `False`。  
- **下次类似题的第一步**：**先思考能否用哈希表一次遍历把所有需要的统计信息收集完**，再在这些统计结果上做进一步检查或计算。这样往往能把 `O(n²)` 的暴力思路压缩到 `O(n)`。