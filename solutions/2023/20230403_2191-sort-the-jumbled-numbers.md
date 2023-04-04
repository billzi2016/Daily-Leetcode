# #2191. 排序扰乱数字 / Sort the Jumbled Numbers

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/sort-the-jumbled-numbers/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array mapping which represents the mapping rule of a shuffled decimal system. mapping[i] = j means digit i should be mapped to digit j in this system.
The mapped value of an integer is the new integer obtained by replacing each occurrence of digit i in the integer with mapping[i] for all 0 <= i <= 9.
You are also given another integer array nums. Return the array nums sorted in non-decreasing order based on the mapped values of its elements.
Notes:

**Examples**

**Example 1:**

```
Input: mapping = [8,9,4,0,2,1,3,5,7,6], nums = [991,338,38]
Output: [338,38,991]
Explanation: 
Map the number 991 as follows:
1. mapping[9] = 6, so all occurrences of the digit 9 will become 6.
2. mapping[1] = 9, so all occurrences of the digit 1 will become 9.
Therefore, the mapped value of 991 is 669.
338 maps to 007, or 7 after removing the leading zeros.
38 maps to 07, which is also 7 after removing leading zeros.
Since 338 and 38 share the same mapped value, they should remain in the same relative order, so 338 comes before 38.
Thus, the sorted array is [338,38,991].
```

**Example 2:**

```
Input: mapping = [0,1,2,3,4,5,6,7,8,9], nums = [789,456,123]
Output: [123,456,789]
Explanation: 789 maps to 789, 456 maps to 456, and 123 maps to 123. Thus, the sorted array is [123,456,789].
```

**Constraints**

- mapping.length == 10
- 0 <= mapping[i] <= 9
- All the values of mapping[i] are unique.
- 1 <= nums.length <= 3 * 104
- 0 <= nums[i] < 109

---

## 题目（中文翻译）

给定一个 **0 索引** 整数数组 `mapping`，它表示一种 **打乱的十进制系统** 的映射规则。`mapping[i] = j` 表示数字 `i` 应该映射为数字 `j`（`0 ≤ i ≤ 9`）。

整数的 **映射值**（mapped value）是将该整数中每个出现的数字 `i` 替换为 `mapping[i]` 后得到的新整数。

同时给定另一个整数数组 `nums`。返回 `nums` 按 **映射值的非递减顺序**（non‑decreasing order）排序后的数组。

### 示例

**示例 1**

```text
Input: mapping = [8,9,4,0,2,1,3,5,7,6], nums = [991,338,38]
Output: [338,38,991]
Explanation:
- 将数字 991 进行映射：
  1. `mapping[9] = 6`，所以所有出现的数字 9 都变成 6；
  2. `mapping[1] = 9`，所以所有出现的数字 1 都变成 9。
  因此，991 的映射值为 669。
- 338 映射为 007，去掉前导零后得到 7。
- 38 映射为 07，同样去掉前导零后得到 7。

由于 338 与 38 的映射值相同，保持原来的相对顺序（稳定排序），最终得到 `[338,38,991]`。

**示例 2**

```text
Input: mapping = [0,1,2,3,4,5,6,7,8,9], nums = [789,456,123]
Output: [123,456,789]
Explanation:
映射规则未改变数字本身，789 → 789，456 → 456，123 → 123。按照映射值的非递减顺序排序后得到 `[123,456,789]`。
```

### 约束

- `mapping.length == 10`
- `0 <= mapping[i] <= 9`
- `mapping` 中的所有值互不相同
- `1 <= nums.length <= 3 * 10^4`
- `0 <= nums[i] < 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **把每个数字都“翻译”一次**。  
   - `mapping` 数组就像一本**查字典**：左边是原来的数字（0~9），右边是对应的“新”数字。  
   - 例如 `mapping[3] = 0`，就相当于把所有出现的 `3` 都换成 `0`。

2. **得到翻译后的整数**。  
   - 把原整数的每一位都查表换成新数字，拼成一个新字符串，再把它转成 `int`，这样自然会把前导的 `0` 去掉（`"007"` → `7`）。

3. **把原数组按照这些新整数的大小排序**。  
   - 若两个原整数的翻译结果相同，保持它们在原数组中的相对顺序（**稳定排序**），最简单的办法是把原下标也一起放进排序键里。

**为什么能得到正确答案**  
- 每个原整数只会产生唯一的翻译结果（因为映射是确定的且每个数字只映射一次），所以比较翻译结果的大小就等价于比较题目要求的“映射值”大小。  
- 稳定排序保证了相同映射值的数字保持原来的先后顺序，正好满足题目要求。

**复杂度分析（大白话）**  

- 设 `n = len(nums)`，`d` 为单个整数的位数（`nums[i] ≤ 10^9`，最多 10 位）。  
- **时间**：  
  - 对每个数字我们要遍历它的每一位并查表 → `O(d)`。  
  - 计算完所有映射后再排序，排序本身是 `O(n log n)`（比较次数会乘上每次比较的键长度，但键已经算好，是常数时间）。  
  - 合在一起是 `O(n·d + n log n)`，在最坏情况下 `d ≤ 10`，可以简化为 `O(n log n)`。  
- **空间**：我们额外存了 `n` 个三元组 `(mapped, index, original)` → `O(n)` 的额外空间。  

> **O(n log n) 的意义**：如果 `n = 10,000`，`log n`（以 2 为底）大约是 14，也就是说排序大约要比较 140,000 次，比起直接两两比较 (`O(n²) = 100,000,000`) 要快很多。

#### 代码（Python）

```python
from typing import List

def sortJumbled(mapping: List[int], nums: List[int]) -> List[int]:
    # ---------- 第一步：把每个数字翻译成新的整数 ----------
    def translate(x: int) -> int:
        # 把整数拆成每一位，查表后重新拼接成字符串
        # 这里用列表推导式把每位数字映射后转成字符
        mapped_str = ''.join(str(mapping[int(ch)]) for ch in str(x))
        # int() 会自动去掉前导的 0，例如 "007" -> 7
        return int(mapped_str)

    # 用一个列表保存 (映射值, 原下标, 原数字)
    transformed = []
    for idx, num in enumerate(nums):
        mapped_val = translate(num)
        transformed.append((mapped_val, idx, num))

    # ---------- 第二步：按照映射值升序排序 ----------
    # Python 的 sort 是稳定的，若映射值相同会保持原下标的顺序
    transformed.sort(key=lambda t: (t[0], t[1]))

    # ---------- 第三步：把排好序的原数字取出来 ----------
    return [t[2] for t in transformed]
```

#### 复杂度

- **时间复杂度**：`O(n·d + n log n)` → 实际上可视为 `O(n log n)`。  
  - `n·d` 用来把每个数字翻译一次，`d ≤ 10`，几乎可以忽略。  
- **空间复杂度**：`O(n)`。我们额外保存了和原数组等长的三元组列表。

---

### 2. 最优解

#### 思路  

暴力解已经是 **最自然** 的实现，只要把映射过程提前算好，就不需要在排序比较时重复计算。  
所以“最优解”实际上是 **在暴力思路上做一次小小的优化**：

1. **一次性预计算所有映射值**（把每个 `num` → `mapped` 存到数组里），避免排序时再去遍历每一位。  
2. **利用 Python 自带的稳定排序**，只需要把 `(mapped, index)` 作为排序键即可。  
3. 由于 `mapping` 是 **全排列**（每个 0~9 恰好出现一次），所以映射过程不会产生冲突，直接使用查表即可。

这一步的时间复杂度仍是 `O(n log n)`（排序是不可避免的），但常数更小，因为每个数字只翻译一次，而不是在比较时反复翻译。

#### 代码（Python）

```python
from typing import List

def sortJumbled(mapping: List[int], nums: List[int]) -> List[int]:
    # 预处理：把每个数字映射一次，结果存入列表
    mapped_vals = []
    for num in nums:
        # 将每位数字映射后拼接，再转成整数去掉前导0
        mapped = int(''.join(str(mapping[int(ch)]) for ch in str(num)))
        mapped_vals.append(mapped)

    # 使用 Python 的 zip 把 (mapped, original index, original number) 绑定在一起
    combined = list(zip(mapped_vals, range(len(nums)), nums))

    # 稳定排序：先按映射值升序；若相同则按原下标升序（保证相等时相对顺序不变）
    combined.sort(key=lambda x: (x[0], x[1]))

    # 取出排好序的原数字返回
    return [x[2] for x in combined]
```

#### 复杂度

- **时间复杂度**：`O(n·d + n log n)` → 仍然是 `O(n log n)`，但只遍历每个数字一次，常数更低。  
- **空间复杂度**：`O(n)`，需要额外保存映射值和下标的组合列表。

> **与暴力解对比**：  
> - 暴力解在排序时每次比较都要重新“翻译”数字，最坏情况下会是 `O(n·d·log n)`（因为比较次数乘以翻译成本）。  
> - 优化后把翻译提前，只需要 `O(n·d)` 的一次性成本，随后排序只比较整数和下标，省掉了重复的字符拼接。

---

## 心得

- **核心技巧**：把“映射”过程抽象为 **查表 + 字符拼接**，并利用 **稳定排序** 保证相同映射值的相对顺序。  
- **适用的题型**：  
  1. **自定义排序**（根据派生属性排序），如 “按字母顺序排序字符串的逆序字符”。  
  2. **映射/转换后排序**，例如 “把每个单词的字母映射成另一个字母表后排序”。  
  3. **保持原有相对顺序的排序**（需要稳定排序），如 “按出现频率排序，频率相同保持原顺序”。  
- **一句话总结解题钥匙**：**先把所有元素转换成可以直接比较的“键”，再用稳定排序一次搞定**。

---

## 反思

- **第一反应**：看到 “mapping” 与 “nums”，立刻想到把每个数字逐位替换后再排序。  
- **最容易踩的坑**：  
  - **前导零**：`"007"` 必须转成整数 `7`，否则比较时会把 `"007"` 当成更大的字符串。  
  - **稳定性**：如果直接用 `sorted(nums, key=func)`，Python 的 `sorted` 已经是稳定的，但如果自行实现比较函数（如 `cmp_to_key`），要注意在映射值相同的情况下返回 0，才能保持原顺序。  
  - **数字 0 的特殊情况**：`0` 也要经过映射，不能直接跳过。  
- **下次类似题的第一步**：**明确“比较键”是什么**——先把原始数据映射/转换成一个可以直接比较的值（整数、字符串等），再交给排序算法处理。这样思路清晰，代码也会自然简洁。