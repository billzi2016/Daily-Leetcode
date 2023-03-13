# #2164. 分别独立排序奇偶索引 / Sort Even and Odd Indices Independently

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/sort-even-and-odd-indices-independently/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. Rearrange the values of nums according to the following rules:
Return the array formed after rearranging the values of nums.

**Examples**

**Example 1:**

```
Input: nums = [4,1,2,3]
Output: [2,3,4,1]
Explanation: 
First, we sort the values present at odd indices (1 and 3) in non-increasing order.
So, nums changes from [4,1,2,3] to [4,3,2,1].
Next, we sort the values present at even indices (0 and 2) in non-decreasing order.
So, nums changes from [4,1,2,3] to [2,3,4,1].
Thus, the array formed after rearranging the values is [2,3,4,1].
```

**Example 2:**

```
Input: nums = [2,1]
Output: [2,1]
Explanation: 
Since there is exactly one odd index and one even index, no rearrangement of values takes place.
The resultant array formed is [2,1], which is the same as the initial array.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个 **0 索引的** 整数数组 `nums`。请按照以下规则重新排列 `nums` 中的值，并返回重新排列后的数组。

**规则**  
1. 将所有 **奇数索引 (odd indices)** 处的值按 **非递增顺序**（从大到小）排序。  
2. 将所有 **偶数索引 (even indices)** 处的值按 **非递减顺序**（从小到大）排序。  

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [4,1,2,3]
```  
**输出**  
```
[2,3,4,1]
```  
**解释**  
首先，对奇数索引（1 和 3）上的值按非递增顺序排序，数组由 `[4,1,2,3]` 变为 `[4,3,2,1]`。  
接着，对偶数索引（0 和 2）上的值按非递减顺序排序，数组由 `[4,3,2,1]` 变为 `[2,3,4,1]`。  
最终得到的数组为 `[2,3,4,1]`。

#### 示例 2
**输入**  
``` 
nums = [2,1]
```  
**输出**  
```
[2,1]
```  
**解释**  
因为恰好只有一个奇数索引和一个偶数索引，数组无需重新排列，结果仍为 `[2,1]`。

---

### 约束条件
- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组 **分成两堆**：

* **偶数下标**（0、2、4…）的元素放在一起  
* **奇数下标**（1、3、5…）的元素放在一起  

就像我们把书架上的书按左边和右边的格子分别摆放一样。  
把这两堆取出来后：

* 偶数下标的这堆用 **升序** 排序（从小到大）  
* 奇数下标的这堆用 **降序** 排序（从大到小）  

排序好后，再把它们“拼回去”。把排好序的第 0 个偶数元素放回原来的 0 号位，第 1 个奇数元素放回原来的 1 号位，依次类推。

为什么这样一定对？

* 题目只要求 **偶数位** 的数 **非递减**（升序），**奇数位** 的数 **非递增**（降序）。  
* 把对应位置的所有数分别排好序后，再放回原位，必然满足这两个要求。

#### 代码（Python）

```python
def sortEvenOdd(nums):
    # 1️⃣ 把偶数位和奇数位的元素分别取出来
    even_vals = [nums[i] for i in range(0, len(nums), 2)]   # 0,2,4,...
    odd_vals  = [nums[i] for i in range(1, len(nums), 2)]   # 1,3,5,...

    # 2️⃣ 对两堆分别排序
    even_vals.sort()                # 升序
    odd_vals.sort(reverse=True)    # 降序

    # 3️⃣ 把排好序的数“塞回”原数组
    res = nums[:]                   # 复制一份结果数组
    even_idx, odd_idx = 0, 0
    for i in range(len(nums)):
        if i % 2 == 0:              # 偶数下标
            res[i] = even_vals[even_idx]
            even_idx += 1
        else:                       # 奇数下标
            res[i] = odd_vals[odd_idx]
            odd_idx += 1
    return res
```

> **关键行中文注释** 已写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度：** `O(n log n)`  
  - 解释：我们对两个子数组各做一次排序，排序的时间是 `O(k log k)`，其中 `k`≈`n/2`。两次加起来仍是 `O(n log n)`。  
  - “`log n`” 可以理解为把 `n` 个数字一次次“分成两半”再合并的过程，次数大约是 7 （因为 2⁷≈128 > 100），所以实际运行很快。

- **空间复杂度：** `O(n)`  
  - 解释：我们额外用了两个列表 `even_vals`、`odd_vals` 来存放拆分后的元素，大小加起来等于原数组的长度 `n`，所以是线性空间。

---

### 2. 最优解

#### 思路  

上面的暴力解已经是 `O(n log n)`，在本题的约束（`nums[i] ≤ 100`）下还能再快一点。  
因为数值范围很小（只在 1~100 之间），我们可以使用 **计数排序**（Counting Sort）：

1. **统计** 偶数位和奇数位各自出现的次数（用长度为 101 的计数数组）。  
   - 计数数组就像一本“字典”，下标是数字本身，值是这个数字出现了几次。  
2. **遍历计数数组**，按需要的顺序（升序或降序）把数字“写回”到结果数组对应的下标。  

计数排序的时间是 **线性** `O(n + m)`，其中 `m` 是数值范围大小（这里 `m = 100`），对本题来说就是 `O(n)`。

#### 代码（Python）

```python
def sortEvenOdd(nums):
    max_val = 100                     # 题目保证的最大值
    # 1️⃣ 为偶数位和奇数位各准备一个计数数组，索引 0~100（0 位置不用）
    even_cnt = [0] * (max_val + 1)    # 偶数位出现次数
    odd_cnt  = [0] * (max_val + 1)    # 奇数位出现次数

    # 2️⃣ 统计出现次数
    for i, v in enumerate(nums):
        if i % 2 == 0:                # 偶数下标
            even_cnt[v] += 1
        else:                         # 奇数下标
            odd_cnt[v] += 1

    # 3️⃣ 把统计结果写回原数组
    res = [0] * len(nums)
    even_idx, odd_idx = 0, 1          # 先写偶数位，再写奇数位

    # 偶数位需要 **升序**，从小到大遍历计数数组
    for val in range(1, max_val + 1):
        while even_cnt[val] > 0:     # 还有该数字未写完
            res[even_idx] = val
            even_idx += 2            # 跳到下一个偶数下标
            even_cnt[val] -= 1

    # 奇数位需要 **降序**，从大到小遍历计数数组
    for val in range(max_val, 0, -1):
        while odd_cnt[val] > 0:
            res[odd_idx] = val
            odd_idx += 2             # 跳到下一个奇数下标
            odd_cnt[val] -= 1

    return res
```

> 计数数组的每一格就像一本“词典”，`even_cnt[5]=3` 表示在偶数下标出现了三个 5。  
> 通过一次遍历把这些“词条”按顺序写回，就完成了排序。

#### 复杂度

- **时间复杂度：** `O(n + 100)` → `O(n)`  
  - 解释：遍历原数组一次统计 (`O(n)`) + 两次遍历计数数组（固定长度 101）是常数时间。整体随 `n` 线性增长。

- **空间复杂度：** `O(n + 100)` → `O(n)`  
  - 解释：除了结果数组 `O(n)`，我们额外用了两个长度为 101 的计数数组（常数空间），所以总体仍是线性。

---

## 心得

- **核心技巧**：把不同“位置”的元素分组后分别排序。  
- **适用场景**：  
  1. “奇偶位分别排序” 类题（LeetCode 2163）  
  2. “把数组中满足某种条件的元素单独处理” 如分奇偶、正负数分组等  
  3. “计数排序” 在数值范围小且要求线性时间时的利器  

> **解题钥匙**：**先分组，再针对每组选最合适的排序方式**。

---

## 反思

- **第一反应**：看到“奇数下标”和“偶数下标”，立刻想到把它们拆开分别处理。  
- **最容易踩的坑**  
  * 忘记把奇数位排序成 **降序**（非递增），写成升序会导致答案错误。  
  * 边界情况：数组长度为 1 时只有偶数位，直接返回原数组即可。  
- **下次类似题的第一步**：**先把满足同一条件的元素收集到一起**（比如同下标同奇偶、同符号等），再决定使用普通排序还是计数排序等更高效的方法。