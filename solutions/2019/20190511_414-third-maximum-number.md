# #414. 第三大数 / Third Maximum Number

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/third-maximum-number/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the third distinct maximum number in this array. If the third maximum does not exist, return the maximum number.

**Examples**

**Example 1:**

```
Input: nums = [3,2,1]
Output: 1
Explanation:
The first distinct maximum is 3.
The second distinct maximum is 2.
The third distinct maximum is 1.
```

**Example 2:**

```
Input: nums = [1,2]
Output: 2
Explanation:
The first distinct maximum is 2.
The second distinct maximum is 1.
The third distinct maximum does not exist, so the maximum (2) is returned instead.
```

**Example 3:**

```
Input: nums = [2,2,3,1]
Output: 1
Explanation:
The first distinct maximum is 3.
The second distinct maximum is 2 (both 2's are counted together since they have the same value).
The third distinct maximum is 1.
```

**Constraints**

- 1 <= nums.length <= 104
- -231 <= nums[i] <= 231 - 1

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，返回该数组中第三大的 **不同** 最大数（third distinct maximum number）。如果不存在第三大的数，则返回最大的数。

**示例 1：**  
**示例 2：**  
**示例 3：**  

**约束条件：**

- `1 <= nums.length <= 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`

**示例：**

**示例 1:**  
```text
Input: nums = [3,2,1]
Output: 1
Explanation:
第一个不同的最大数是 3。
第二个不同的最大数是 2。
第三个不同的最大数是 1。
```

**示例 2:**  
```text
Input: nums = [1,2]
Output: 2
Explanation:
第一个不同的最大数是 2。
第二个不同的最大数是 1。
不存在第三个不同的最大数，因此返回最大数（2）。
```

**示例 3:**  
```text
Input: nums = [2,2,3,1]
Output: 1
Explanation:
第一个不同的最大数是 3。
第二个不同的最大数是 2（两个 2 视为同一个值）。
第三个不同的最大数是 1。
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把数组全部拿出来，**去重**后再从大到小排个序，排好序后第 3 位（如果有的话）就是答案。  

- **去重**：我们可以用 Python 的 `set`，它的工作方式类似于查字典——把每个数字当成“词”，对应的“页码”就是它本身。相同的词只会留下一个，天然实现了去重。  
- **排序**：把去重后的集合转成列表，用 `sorted` 按从大到小的顺序排好。`sorted` 的实现类似于把所有数字排成一条长队，从最高的往后排，时间上会比手动比较要快很多。  
- **取第 3 大**：排好序后，如果长度 ≥ 3，直接返回下标为 2 的元素；否则说明不存在第 3 大，直接返回最大的那个（下标 0 的元素）。

这个方法**一定正确**：  
1. `set` 保证了每个不同的数只出现一次，满足“distinct”。  
2. 排序保证了我们可以按照大小顺序依次访问。  
3. 按顺序取第 3 个，恰好对应题目要求的“第三大”。  

#### 代码（Python）  

```python
def thirdMax(nums: list[int]) -> int:
    # 1️⃣ 用 set 去重，像查字典一样，只保留不同的数字
    distinct = set(nums)               # {3, 2, 1, ...}
    
    # 2️⃣ 把去重后的集合转成列表并从大到小排序
    sorted_desc = sorted(distinct, reverse=True)   # 例: [3, 2, 1]
    
    # 3️⃣ 判断是否有第三个元素
    if len(sorted_desc) >= 3:          # 长度够 3，说明第三大存在
        return sorted_desc[2]          # 第 3 大的下标是 2
    else:                              # 不够 3，直接返回最大值（下标 0）
        return sorted_desc[0]
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `set(nums)` 需要遍历全部 `n` 个元素，时间是 `O(n)`。  
  - `sorted(..., reverse=True)` 对去重后的 `m`（`m ≤ n`）个数进行排序，排序的时间是 `O(m log m)`，最坏情况 `m = n`，所以整体是 `O(n log n)`。  
  - 大白话：如果数组有 10 000 个数，排序大概会比直接遍历慢几百倍，但在 10⁴ 规模下仍然很快。  

- **空间复杂度**：`O(n)`  
  - `set` 最坏需要存放所有不同的元素，最多 `n` 个。  
  - 排序后产生的列表也占 `O(m)` 空间。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **排序**，排序本身就要 `O(n log n)`，而这道题只要求找出前三大的数，根本不需要把所有数排好序。  

我们可以 **一次遍历**，用三个变量 `first、second、third` 分别记录当前遇到的第一、第二、第三大（distinct）数。  

关键点如下：  

1. **去重**：在遍历时如果当前数字已经等于 `first、second、third` 中的任意一个，就直接跳过，防止相同的数被计数多次。  
2. **更新规则**：  
   - 如果 `x > first`，说明出现了更大的数，需要把 `first → second`，`second → third`，再把 `x` 设为新的 `first`。  
   - 否则如果 `first > x > second`，只需要把 `second → third`，`x` 设为新的 `second`。  
   - 否则如果 `second > x > third`，只把 `x` 设为新的 `third`。  
3. **返回结果**：遍历结束后，如果 `third` 仍然是初始的“哨兵值”，说明数组中不足三个不同的数，直接返回 `first`（最大值）；否则返回 `third`。  

为什么只需要三个变量就能搞定？因为我们只关心 **前三大的** 那几位，一旦这三位确定，后面的数再大也不可能影响它们的相对顺序。  

#### 代码（Python）  

```python
def thirdMax(nums: list[int]) -> int:
    # 使用三个哨兵变量，初始值设为 None，表示还没有填充
    first = second = third = None   # 分别对应第一、第二、第三大

    for x in nums:
        # 1️⃣ 去重：如果 x 已经等于前三名中的任何一个，就跳过
        if x == first or x == second or x == third:
            continue

        # 2️⃣ 更新前三名
        if first is None or x > first:          # 出现更大的数
            third = second                       # 第三名下移
            second = first                       # 第二名下移
            first = x                            # 第一次名更新为 x
        elif second is None or x > second:      # 只比第二名大
            third = second                       # 第三名下移
            second = x                           # 第二名更新为 x
        elif third is None or x > third:        # 只比第三名大
            third = x                            # 第三名更新为 x
        # else: x 小于等于 third，什么也不做

    # 3️⃣ 根据是否得到第三大返回答案
    return third if third is not None else first
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次数组，所有操作都是常数时间。  
  大白话：如果有 10 000 个数，只需要 10 000 次“比较”，几乎是瞬间完成。  

- **空间复杂度**：`O(1)`  
  只用了固定的几个变量，不随输入规模增长。  

---  

## 心得  

- 这道题的核心技巧是 **维护常数个极值**（这里是前三大），在遍历过程中即时更新。  
- 该技巧适用于类似的“第 k 大/小”问题，只要 `k` 是常数，就可以用 **常数空间 + 单次遍历** 的方式解决。常见的类似题目有：  
  1. “第二大数字”（LeetCode 414）  
  2. “数组中的最大乘积”（找出最大和次大数相乘）  
  3. “寻找数组中最大的三个数的和”。  
- 一句话总结解题钥匙：**“一次遍历，维护前 k 大（或小）的变量，遇到重复直接跳过”。**  

## 反思  

- **第一反应**：看到“第三大”立刻想到排序或集合去重后取第 3 位。  
- **最容易踩的坑**：  
  - 忽视 **去重**，导致相同的数被计入多次，从而得到错误的“第三大”。  
  - 初始化 `first、second、third` 时使用不恰当的极小值（如 `-inf`），在全负数的情况下可能导致判断错误，使用 `None` 或者专门的哨兵更安全。  
- **下次遇到同类题**：第一步先问自己“是否真的需要完整排序？”，如果只要前几名，尝试 **维护固定数量的极值**，并在遍历时做好 **去重** 与 **边界检查**。