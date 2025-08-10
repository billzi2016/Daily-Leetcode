# #3300. 替换为各位数字之和后的最小元素 / Minimum Element After Replacement With Digit Sum

> 难度：简单 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/minimum-element-after-replacement-with-digit-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
You replace each element in nums with the sum of its digits.
Return the minimum element in nums after all replacements.

**Examples**

**Example 1:**

```
Input: nums = [10,12,13,14]
Output: 1
Explanation:
nums becomes [1, 3, 4, 5] after all replacements, with minimum element 1.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 1
Explanation:
nums becomes [1, 2, 3, 4] after all replacements, with minimum element 1.
```

**Example 3:**

```
Input: nums = [999,19,199]
Output: 10
Explanation:
nums becomes [27, 10, 19] after all replacements, with minimum element 10.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你需要将 `nums` 中的每个元素替换为其**各位数字之和**（digit sum）。  
返回所有替换完成后 `nums` 中的**最小元素**（minimum element）。

示例 1  
示例 2  
示例 3  

#### 示例

**示例 1**  
输入: `nums = [10,12,13,14]`  
输出: `1`  
**解释:**  
所有元素替换后，`nums` 变为 `[1, 3, 4, 5]`，其中最小元素为 `1`。

**示例 2**  
输入: `nums = [1,2,3,4]`  
输出: `1`  
**解释:**  
所有元素替换后，`nums` 仍为 `[1, 2, 3, 4]`，最小元素为 `1`。

**示例 3**  
输入: `nums = [999,19,199]`  
输出: `10`  
**解释:**  
所有元素替换后，`nums` 变为 `[27, 10, 19]`，最小元素为 `10`。

#### 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把数组里的每个整数 **逐个** 换成它的 **各位数字之和**，再在新数组里找最小值。  

- **数据结构**：只需要原数组 `nums` 本身和一个临时变量保存“各位和”。可以把 “各位和” 想象成 **查字典**：字典的键是数字本身，值是它的位数之和。这里我们不必真的建字典，只是每次 **算一次**。  
- **为什么正确**：题目要求“把每个元素替换为它的数字和”，这一步是必不可少且唯一的。替换完后，数组里每个位置的值都是题目规定的值，直接取最小值即为答案。  
- **时间/空间复杂度**：  
  - 对每个元素，我们需要把它的每一位相加。假设数字最大是 `10^4`，最多 5 位，所以每次求和的时间是 **与位数成正比**，记作 `O(d)`（d≈5）。遍历 `n` 个元素，总时间 `O(n·d)`，在本题里可以写成 `O(n)`（因为 d 是常数）。  
  - 只用了几个额外的整数变量，空间是 `O(1)`，即**常数级**。  

#### 代码（Python）  

```python
def digit_sum(x: int) -> int:
    """
    计算整数 x 的各位数字之和。
    思路：不断取出最低位 (x % 10)，累加后把 x 整除 10。
    """
    s = 0
    while x:               # 当 x 不为 0 时循环
        s += x % 10        # 取出最低位并加到 s
        x //= 10           # 去掉最低位
    return s               # 返回累计的和


def min_after_replacement(nums):
    """
    暴力实现：遍历每个元素，求位和后更新最小值。
    """
    min_val = float('inf')          # 初始设为正无穷，保证第一个元素会被替换
    for num in nums:
        replaced = digit_sum(num)   # 把当前元素换成位和
        if replaced < min_val:      # 更新最小值
            min_val = replaced
    return min_val
```

#### 复杂度  

- **时间复杂度**：`O(n·d)` → 实际上 `O(n)`，因为每个数的位数 `d` 最多 5（`nums[i] ≤ 10⁴`），可以视作常数。  
  - 大白话：如果数组有 100 个数，最多只需要算 500 次“取余+除以 10”，非常快。  
- **空间复杂度**：`O(1)`，只用了几个临时整数，不会随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
从暴力解来看，唯一的耗时来源是 **逐位相加**。  
- **瓶颈**：每次都要对同一个数重复做相同的除余操作。  
- **优化方向**：如果同一个数会出现多次，可以把它的位和记下来，下次直接查表。这里题目规模很小（`len(nums) ≤ 100`），且每个数最多出现一次，所以 **不需要额外的优化**，原来的 O(n) 已经是最优的。  

不过，为了演示「记忆化」的思想（在更大规模时会有帮助），我们可以使用 **哈希表**（字典）把已经算过的位和缓存下来。字典的工作方式可以类比 **查字典**：  
- **key**：原始整数  
- **value**：它的位和  

这样，每个不同的数只会计算一次，后续出现时直接 O(1) 取值。  

#### 代码（Python）  

```python
def digit_sum(x: int) -> int:
    """同上，只是保留在这里供后面使用。"""
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def min_after_replacement_opt(nums):
    """
    使用哈希表缓存已经计算过的位和。
    对于本题规模，这种做法和暴力解几乎一样快，
    但在数值重复很多、数组很大的情况下可以显著降低计算量。
    """
    cache = {}                # key: 原数, value: 位和
    min_val = float('inf')
    for num in nums:
        if num not in cache:          # 只在第一次遇到时计算
            cache[num] = digit_sum(num)
        replaced = cache[num]         # 直接拿缓存值
        if replaced < min_val:
            min_val = replaced
    return min_val
```

#### 复杂度  

- **时间复杂度**：`O(n·d)` → `O(n)`（每个不同的数只算一次位和，查表是 O(1)）。  
  - 与暴力解相比，**最坏情况相同**（所有数都不相同），**最好情况更好**（大量重复时只算一次）。  
- **空间复杂度**：`O(k)`，`k` 为不同数字的个数，最多不超过 `n`，即 `O(n)`。  
  - 大白话：如果数组里全是相同的数，只需要存一个结果；如果全不相同，就相当于用了一个额外的同等大小的数组来记忆。  

---  

## 心得  

- **核心技巧**：**求整数的各位数字之和**（digit sum）以及**使用哈希表缓存**。  
- **适用的题型**：  
  1. “把每个数转换成某种函数值后统计/比较”——例如把数转成二进制中 `1` 的个数后求最小值。  
  2. “对数组每个元素做相同的耗时操作，且可能出现重复”——比如把数转成其 **因子个数**、**素数判定** 等。  
- **解题钥匙**：**先把每个元素映射到目标值（这里是位和），再在映射结果上做最简操作（取最小/最大/计数）**。  

---  

## 反思  

- **第一反应**：看到“把每个元素替换为它的数字和”，自然想到遍历数组、对每个数做位运算或字符串转换。  
- **最容易踩的坑**：  
  - **遗漏 0**：`while x:` 在 `x = 0` 时循环不会进入，需单独返回 0（本题 `nums[i] ≥ 1` 不会出现）。  
  - **使用字符串**时忘记把字符转成整数 `int(ch)`，导致拼接错误。  
  - **边界条件**：数组长度可能为 1，确保代码在单元素时也能正常返回。  
- **下次遇到同类题**，第一步应该想到 **“把每个数映射为一个新值（位和、位数、某函数）”，然后在新值上直接求答案”。如果映射过程可能重复，立刻考虑 **哈希表缓存**。