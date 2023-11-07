# #2465. 不同平均值的数量 / Number of Distinct Averages

> 难度：简单 · 标签：Array、Hash Table、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/number-of-distinct-averages/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of even length.
As long as nums is not empty, you must repetitively:
The average of two numbers a and b is (a + b) / 2.
Return the number of distinct averages calculated using the above process.
Note that when there is a tie for a minimum or maximum number, any can be removed.

**Examples**

**Example 1:**

```
Input: nums = [4,1,4,0,3,5]
Output: 2
Explanation:
1. Remove 0 and 5, and the average is (0 + 5) / 2 = 2.5. Now, nums = [4,1,4,3].
2. Remove 1 and 4. The average is (1 + 4) / 2 = 2.5, and nums = [4,3].
3. Remove 3 and 4, and the average is (3 + 4) / 2 = 3.5.
Since there are 2 distinct numbers among 2.5, 2.5, and 3.5, we return 2.
```

**Example 2:**

```
Input: nums = [1,100]
Output: 1
Explanation:
There is only one average to be calculated after removing 1 and 100, so we return 1.
```

**Constraints**

- 2 <= nums.length <= 100
- nums.length is even.
- 0 <= nums[i] <= 100

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的整数数组 `nums`，且数组长度为偶数。只要 `nums` 不为空，你必须重复以下步骤：

1. 取出数组中的最小元素 `a` 与最大元素 `b`（如果最小值或最大值出现多次，任意取出一个）。
2. 计算这两个数的平均值，公式为 `(a + b) / 2`（平均值（average））。
3. 将 `a` 与 `b` 从数组中删除，记录下得到的平均值。

返回在整个过程结束后得到的**不同平均值的数量**。  

**说明**  
- 当出现最小值或最大值的平局时，任意一个都可以被移除。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [4,1,4,0,3,5]
```  
**输出**  
```
2
```  
**解释**  
1. 移除 `0` 和 `5`，平均值为 `(0 + 5) / 2 = 2.5`，此时 `nums = [4,1,4,3]`。  
2. 移除 `1` 和 `4`，平均值为 `(1 + 4) / 2 = 2.5`，此时 `nums = [4,3]`。  
3. 移除 `3` 和 `4`，平均值为 `(3 + 4) / 2 = 3.5`。  

得到的平均值为 `2.5, 2.5, 3.5`，其中不同的数有 `2.5` 与 `3.5` 两个，故返回 `2`。

#### 示例 2
**输入**  
``` 
nums = [1,100]
```  
**输出**  
```
1
```  
**解释**  
只需移除 `1` 与 `100`，得到唯一的平均值 `(1 + 100) / 2 = 50.5`，因此返回 `1`。

---

### 约束条件
- `2 <= nums.length <= 100`
- `nums.length` 为偶数
- `0 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步步模拟题目描述的过程**：

1. 在当前数组 `nums` 中，找出最小的数 `min` 和最大的数 `max`（如果有多个相同的最小/最大，随便挑一个都行）。  
2. 计算它们的平均值 `(min + max) / 2`，把这个平均值放进一个集合里，用来去重。  
3. 把 `min` 与 `max` 从数组中删除，数组长度会减少 2。  
4. 重复上述步骤，直到数组为空。  

> **类比**：把数组想成一本书的章节目录，最小的章节号像是书的封面，最大的像是封底。我们每次把封面和封底一起拿走，记录下它们的“平均页码”。这个过程一直进行到书里没有章节为止。

**为什么能得到正确答案**：  
题目规定“只要数组不为空，就一直这么取”，而且**取最小和最大**的顺序不影响最终的所有平均值集合（因为每次我们都把当前最小和最大配对），所以只要严格按照上述规则模拟，就一定会得到题目要求的所有平均值。

**时间/空间分析**：  
- 找最小、最大需要遍历一次数组 → `O(k)`（`k` 为当前数组长度）。  
- 由于我们会进行 `n/2` 次配对（`n` 为原数组长度），总时间是 `O(n + (n-2) + (n-4) + … + 2) = O(n²)`。  
- 为了去重，我们使用一个集合 `set`，最坏情况下会存 `n/2` 个平均值 → `O(n)` 的额外空间。

> **大白话**：`O(n²)` 就像把 100 本书的每一本都和其他 99 本书比较一次，工作量会变成 10,000 次。这里的 `n` 只有最多 100，虽然还能跑，但不是最省力的办法。

#### 代码（Python）

```python
from typing import List

def distinctAverages_brute(nums: List[int]) -> int:
    # 用 set 自动去重，存放所有出现过的平均值
    avgs = set()
    # 复制一份，防止修改原数组
    arr = nums[:]

    # 只要数组里还有元素就继续
    while arr:
        # 找最小值和最大值的下标
        min_idx = arr.index(min(arr))   # O(k) 查找最小
        max_idx = arr.index(max(arr))   # O(k) 查找最大

        # 取出对应的数值
        a = arr[min_idx]
        b = arr[max_idx]

        # 计算平均值，放进集合
        avgs.add((a + b) / 2)

        # 为了删除不影响下标，先把大的下标删掉，再删小的下标
        # （否则删除后，另一个下标会因为数组收缩而改变）
        for idx in sorted([min_idx, max_idx], reverse=True):
            arr.pop(idx)   # O(k) 删除

    # 集合的大小就是不同的平均值数量
    return len(avgs)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：每一次配对都要遍历一次当前数组找最小/最大，配对次数是 `n/2`，于是工作量大约是 `n + (n-2) + … ≈ n² / 2`，量级是平方级。  

- **空间复杂度**：`O(n)`  
  解释：我们额外用了一个集合保存至多 `n/2` 个平均值，以及一个复制的数组 `arr`（大小为 `n`），所以空间随 `n` 线性增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“每次都取当前最小和最大”** 是关键。  
如果我们事先把数组**排好序**，最小元素一定在左端，最大元素一定在右端。于是：

1. 将 `nums` 从小到大排序（一次 `O(n log n)`）。  
2. 用两个指针：`left` 从最左边向右移动，`right` 从最右边向左移动。每一步配对 `nums[left]` 与 `nums[right]`。  
3. 计算平均值并放进集合 `set` 去重。  
4. `left` 加 1，`right` 减 1，继续配对，直到 `left > right`（恰好配完 `n/2` 对）。

> **类比**：把一串排好序的珠子摆成一条直线，左手抓最左边的珠子，右手抓最右边的珠子，一起算它们的平均颜色。每次把这两个珠子取走，继续向中间靠拢。

**为什么更快**：  
排序把“找最小/最大”这一步从每轮 `O(k)` 降到了 `O(1)`（只需要指针位置），只需要一次 `O(n log n)` 的排序开销。配对本身是线性 `O(n)`，所以整体是 `O(n log n)`，远快于 `O(n²)`。

**核心数据结构**：  
- **数组**（已排序）  
- **双指针**：左指针 `l`、右指针 `r`，每次向中间收敛。  
- **集合（哈希表）**：用来自动去重，查找/插入都是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def distinctAverages(nums: List[int]) -> int:
    # 1. 先把数组排好序，最小在左，最大在右
    nums.sort()                     # O(n log n)

    # 2. 用集合存放所有出现过的平均值（自动去重）
    avgs = set()

    # 3. 双指针配对
    left, right = 0, len(nums) - 1
    while left < right:             # 只要还有未配对的元素
        a, b = nums[left], nums[right]
        avgs.add((a + b) / 2)       # 计算平均值并加入集合
        left += 1                   # 左指针右移
        right -= 1                  # 右指针左移

    # 4. 集合的大小即为不同平均值的数量
    return len(avgs)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  解释：排序是 `O(n log n)`，后面的双指针遍历只需一次线性扫描 `O(n)`，两者相加仍是 `O(n log n)`。这比暴力的 `O(n²)` 快很多，尤其当 `n` 变大时优势更明显。  

- **空间复杂度**：`O(n)`（或 `O(1)` 视实现而定）  
  解释：如果把排序原地进行，额外的指针和集合只占 `O(n/2)`（即最多 `n/2` 个平均值），因此总体是线性空间。若不计集合，指针本身是常数空间 `O(1)`。  

---  

## 心得  

- **核心技巧**：先排序 + 双指针配对，配合哈希集合去重。  
- **适用的类似题型**：  
  1. “最大化最小配对和” 类似的 **两数配对** 题（如 LeetCode 1679 `Max Number of K-Sum Pairs`）。  
  2. “找出所有不同的中位数/平均数” 需要先排序再配对的题目（如 1672 `Richest Customer Wealth` 中的配对思路）。  
- **一句话总结**：**“先把乱序的东西排好序，再用左右指针一次性配对，配对结果放进集合去重”。**  

---  

## 反思  

- **第一反应**：看到“每次取最小和最大”，立刻想到要**排序**，因为排序后最小/最大位置固定，配对会变得非常简单。  
- **最容易踩的坑**：  
  1. **平均值是小数**：在 Python 中 `(a + b) / 2` 会得到浮点数，需要直接放进集合，不能用整数除法 `//`（会丢失小数部分）。  
  2. **边界条件**：数组长度一定是偶数，配对循环的结束条件要写成 `left < right`，否则会出现 `left == right` 时多算一次。  
  3. **集合去重**：若误用了列表或直接计数，会把相同的平均值算多次。  
- **下次类似题的第一步**：**先把数据排序**，判断是否可以用**双指针**一次遍历完成配对或统计，这往往能把原本的 `O(n²)` 降到 `O(n log n)` 或 `O(n)`。