# #349. 两个数组的交集 / Intersection of Two Arrays

> 难度：简单 · 标签：Array、Hash Table、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/intersection-of-two-arrays/)

---

## 题目（英文原版）

**Description**

Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]
```

**Example 2:**

```
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4]
Explanation: [4,9] is also accepted.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 1000

---

## 题目（中文翻译）

**描述**  
给定两个整数数组（integer arrays）`nums1` 和 `nums2`，返回它们的交集（intersection）构成的数组（array）。结果中的每个元素必须是唯一的，返回结果的顺序可以任意。

**示例 1**  
```text
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]
```

**示例 2**  
```text
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4]
Explanation: 同样接受 [4,9]。
```

**约束条件**  
- `1 <= nums1.length, nums2.length <= 1000`  
- `0 <= nums1[i], nums2[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 `nums1` 里每一个数都去和 `nums2` 里所有的数比较一遍，  
只要发现相同的就把它放进答案里。  
这里用到的唯一数据结构是 **列表**（Python 的 `list`），相当于我们手里的一摞纸条，  
我们一张一张往下翻查找。

- **正确性**：只要遍历了 `nums1` 的每个元素并且把它和 `nums2` 的每个元素都比较一次，  
  那么所有可能的相同元素一定会被发现。  
- **唯一性**：为了保证答案里没有重复元素，发现相同后再检查一下答案里是否已经有了这个数。

#### 代码（Python）  
```python
def intersection_brute(nums1, nums2):
    result = []                     # 用来存放交集，类似装答案的盒子
    for a in nums1:                 # 把 nums1 的每个数拿出来
        for b in nums2:             # 与 nums2 的每个数逐一比对
            if a == b:              # 找到相同的数
                if a not in result:    # 盒子里还没有这个数才放进去（保证唯一）
                    result.append(a)
                break                # 已经找到对应的 b，后面的就不用再比了
    return result
```

#### 复杂度  
- **时间复杂度**：`O(n * m)`（这里的 `n`、`m` 分别是两个数组的长度）。  
  用大白话说，就是如果 `nums1` 长 1000，`nums2` 也长 1000，程序会跑 **一百万** 次比较，  
  随着数组变长，比较次数会呈 **乘法** 增长，像两条路交叉形成的格子数。  
- **空间复杂度**：`O(k)`，`k` 是交集的大小。除了存放答案外，几乎不需要额外空间。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 在于每次都要把 `nums2` 的所有元素遍历一遍去找匹配，  
这相当于每次都在“大海捞针”。  
如果我们事先把其中一个数组的所有元素记下来，后面只需要 **快速查找** 是否出现过，就能省掉大量遍历。

这里可以利用 **哈希表**（在 Python 中用 `set` 实现），它的查找速度是 **常数级** `O(1)`，  
就像一本 **字典**，我们直接翻到对应的页码就能知道某个单词是否存在，而不必逐页翻。

优化步骤：

1. 把 `nums1` 放进一个集合 `set1`，自动去重。  
   - 这一步相当于把所有可能的答案装进“查字典的词典”。  
2. 再遍历 `nums2`，每遇到一个数就去 `set1` 里查一查：  
   - 若在，就说明这个数是交集，把它放进答案集合 `ans`（同样用 `set` 去重）。  
3. 最后把答案集合转成列表返回即可。

如果想再省空间，也可以把较短的数组先放进集合，这样构造的集合更小，查找仍然是 `O(1)`。

#### 代码（Python）  
```python
def intersection(nums1, nums2):
    # 1. 把较短的数组放进集合，自动去重
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1   # 交换，让 nums1 更短

    set1 = set(nums1)                 # 哈希表：查找速度是 O(1)
    ans = set()                       # 用集合保存答案，自动去重

    # 2. 遍历另一个数组，快速判断是否在 set1 中
    for num in nums2:
        if num in set1:               # O(1) 判断
            ans.add(num)              # 加进答案集合

    # 3. 把集合转成列表返回（顺序不限）
    return list(ans)
```

#### 复杂度  
- **时间复杂度**：`O(n + m)`。  
  - 把 `nums1` 放进集合是 `O(n)`，遍历 `nums2` 并做常数时间查找是 `O(m)`，  
    两部分相加就是线性时间。用大白话说，数组多长我们只需要走一遍，**不再出现乘法的格子**。  
- **空间复杂度**：`O(n)`（或 `O(min(n, m))`），因为我们只需要存放较短数组的集合和答案集合。  

---  

## 心得  

- **核心技巧**：利用哈希集合（`set`）实现**常数时间查找**，把“遍历找匹配”转化为“查询是否存在”。  
- **适用的题型**：  
  1. 两个数组的交集 / 并集 / 差集（如 “Intersection of Two Arrays II”）。  
  2. 判断两个集合是否有交叉元素（如 “Contains Duplicate”）。  
  3. 统计数组中出现次数超过一次的元素（如 “Majority Element” 的变形）。  
- **一句话总结**：**把一个数组变成字典（集合），把“遍历找”变成“查字典”。**  

## 反思  

- **第一反应**：看到“交集”，自然会想到逐个比较——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记去重，导致答案里出现重复元素。  
  - 没有考虑数组长度差异，导致不必要的大集合占用额外空间。  
- **下次的第一步**：先问自己“有没有可以一次性记住所有元素的结构？”——答案往往是哈希表（集合）或排序后双指针。这样就能立刻把暴力的**O(n·m)** 降到 **O(n+m)**。