# #2956. 寻找两个数组的公共元素 / Find Common Elements Between Two Arrays

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-common-elements-between-two-arrays/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 of sizes n and m, respectively. Calculate the following values:
Return [answer1,answer2].

**Examples**

**Example 1:**

```
Input: nums1 = [2,3,2], nums2 = [1,2]
Output: [2,1]
Explanation:
```

**Example 2:**

```
Input: nums1 = [4,3,2,3,1], nums2 = [2,2,5,2,3,6]
Output: [3,4]
Explanation:
The elements at indices 1, 2, and 3 in nums1 exist in nums2 as well. So answer1 is 3.
The elements at indices 0, 1, 3, and 4 in nums2 exist in nums1 . So answer2 is 4.
```

**Example 3:**

```
Input: nums1 = [3,4,2,3], nums2 = [1,5]
Output: [0,0]
Explanation:
No numbers are common between nums1 and nums2 , so answer is [0,0].
```

**Constraints**

- n == nums1.length
- m == nums2.length
- 1 <= n, m <= 100
- 1 <= nums1[i], nums2[i] <= 100

---

## 题目（中文翻译）

**描述**  
给定两个整数数组（integer array）`nums1` 和 `nums2`，它们的长度分别为 `n` 和 `m`。请计算以下两个数值：

- `answer1`：`nums1` 中有多少个元素在 `nums2` 中也出现过；
- `answer2`：`nums2` 中有多少个元素在 `nums1` 中也出现过。

返回数组 `[answer1, answer2]`。

**示例 1**  
```text
Input: nums1 = [2,3,2], nums2 = [1,2]
Output: [2,1]
Explanation:
nums1 中的元素 2 和 3（下标 0、1、2）在 nums2 中都有出现，共计 2 个不同的下标对应的元素；  
而 nums2 中的元素 2（下标 1）在 nums1 中出现，计为 1。
```

**示例 2**  
```text
Input: nums1 = [4,3,2,3,1], nums2 = [2,2,5,2,3,6]
Output: [3,4]
Explanation:
`nums1` 中下标 1、2、3 对应的元素（3、2、3）在 `nums2` 中也出现，所以 answer1 为 3。  
`nums2` 中下标 0、1、3、4 对应的元素（2、2、2、3）在 `nums1` 中出现，所以 answer2 为 4。
```

**示例 3**  
```text
Input: nums1 = [3,4,2,3], nums2 = [1,5]
Output: [0,0]
Explanation:
`nums1` 与 `nums2` 没有任何公共元素，故答案为 [0,0]。
```

**约束条件**  
- `n == nums1.length`  
- `m == nums2.length`  
- `1 <= n, m <= 100`  
- `1 <= nums1[i], nums2[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
- 对 `nums1` 的每一个元素，去 `nums2` 里逐个比较，看看能不能找到相同的数。能找到就算它“在两个数组都有”。  
- 同理，再对 `nums2` 的每一个元素，遍历 `nums1` 检查是否相同。

这里用到的唯一数据结构就是 **数组** 本身。可以把数组想象成排好队的学生，**遍历** 就是把老师一个一个叫出来检查。  
为什么这种方法一定能得到正确答案？因为我们把所有可能的配对都检查了一遍，凡是相等的配对都会被计数。

时间复杂度：  
- 对 `nums1` 的每个元素，都要遍历完整个 `nums2` → `n * m` 次比较。这里的 `O(n·m)` 可以读作“数量级是 n 乘以 m”，也就是说如果 `n` 是 10、`m` 是 20，最多会做 200 次比较。  
- 再对 `nums2` 做一次同样的遍历，整体仍是 `O(n·m)`（常数因子 2 在大 O 记号里省略）。

空间复杂度：  
- 只用了几个计数变量，没有额外的数组或哈希表 → `O(1)`（常数级空间），意思是占用的内存基本不随输入规模变化。

#### 代码（Python）

```python
def find_common(nums1, nums2):
    # 计数器
    ans1 = 0  # nums1 中有多少个元素在 nums2 里出现过
    ans2 = 0  # nums2 中有多少个元素在 nums1 里出现过

    # ----- 统计 ans1 -----
    for x in nums1:                # 取出 nums1 的每个元素
        found = False               # 标记是否在 nums2 中找到相同的数
        for y in nums2:            # 在 nums2 中逐个比较
            if x == y:              # 找到相等
                found = True
                break               # 已经找到，后面不必继续遍历
        if found:                   # 只要找到一次就算一次
            ans1 += 1

    # ----- 统计 ans2 -----
    for y in nums2:
        found = False
        for x in nums1:
            if y == x:
                found = True
                break
        if found:
            ans2 += 1

    return [ans1, ans2]
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  这里的 `n` 是 `nums1` 长度，`m` 是 `nums2` 长度。因为我们对每个元素都要遍历另一个数组一次，最坏情况下会进行 `n*m` 次比较。  
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（计数器），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次比较都要遍历整个另一数组，导致 `n·m` 次重复工作。  
我们可以把“在另一个数组里出现过吗？”的查询变成 **常数时间**（`O(1)`）的操作，这就需要一种“快速查找”结构——**哈希表**（在 Python 中表现为 `set`）。

**核心想法**：

1. 把 `nums2` 的所有元素放进一个集合 `set2`。集合的特性是“查找某个元素是否在其中”，相当于一本**词典**：你给出单词（这里是数字），立刻得到“有”或“没有”。  
2. 再遍历 `nums1`，对每个元素直接用 `in set2` 判断是否出现过，若是则计数。这样每次查询只需要 `O(1)` 时间。  
3. 同理，构造 `set1`（`nums1` 的集合），遍历 `nums2` 统计 `answer2`。

这样我们把 **双层循环**（`n·m`）变成了 **两次线性遍历**（`n + m`），显著提升效率。

**为什么集合可以做到 `O(1)` 查找？**  
集合内部使用 **哈希函数** 把元素映射到一个数组的下标位置，查找时直接跳到对应位置即可，和把名字直接对应到字典的页码类似。

#### 代码（Python）

```python
def find_common(nums1, nums2):
    # 把 nums2 的所有数字放进集合，类似“查字典”
    set2 = set(nums2)          # O(m) 时间，O(m) 空间

    # 统计 nums1 中有多少元素在 set2 里
    ans1 = 0
    for x in nums1:            # O(n) 时间
        if x in set2:          # O(1) 查找
            ans1 += 1

    # 同理，把 nums1 放进集合
    set1 = set(nums1)          # O(n) 时间，O(n) 空间
    ans2 = 0
    for y in nums2:            # O(m) 时间
        if y in set1:          # O(1) 查找
            ans2 += 1

    return [ans1, ans2]
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  我们只做了两次线性遍历（构造集合和计数），不再有乘法项。相当于如果 `n = 100`、`m = 100`，最多只需要 200 次操作，而不是 10,000 次。  
- **空间复杂度**：`O(n + m)`  
  需要额外存放两个集合，分别保存 `nums1` 与 `nums2` 的所有不同元素。最坏情况下每个数组的元素都不重复，集合大小就是原数组长度之和。

---

## 心得

- **核心技巧**：利用哈希集合（`set`）实现 O(1) 的“是否出现”查询。  
- **适用的题型**  
  1. 判断两个数组是否有交集（LeetCode 349 – Intersection of Two Arrays）。  
  2. 统计数组中出现次数相同的元素（如出现次数相等的字符统计）。  
  3. 判断一个数组中是否存在某个子数组的和等于目标值（利用前缀和集合）。  
- **一句话总结解题钥匙**：把“在另一个数组里出现吗”这个问题转化为“在集合里查找”，从 O(n·m) 降到 O(n+m)。

---

## 反思

- **第一反应**：看到“统计两个数组的公共元素”，第一时间想到双层循环遍历全部配对。  
- **最容易踩的坑**  
  - **重复计数**：题目要求的是“每个位置是否有对应的数”，而不是去重后计数；所以即使同一个数字在另一数组出现多次，也只算一次。  
  - **边界条件**：数组长度可能为 1，需要确保循环不会因为空集合而出错。  
  - **数据范围**：虽然这里的数值范围小（≤100），但若改为更大范围，暴力解的性能差距会更明显。  
- **下次遇到同类题**：第一步先思考“是否可以把一个数组的元素存进哈希集合”，如果可以，就直接用集合实现 O(1) 查询；否则再考虑暴力或其他优化手段。