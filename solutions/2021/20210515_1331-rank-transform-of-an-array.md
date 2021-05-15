# #1331. 数组的秩变换 / Rank Transform of an Array

> 难度：简单 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/rank-transform-of-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr, replace each element with its rank.
The rank represents how large the element is. The rank has the following rules:

**Examples**

**Example 1:**

```
Input: arr = [40,10,20,30]
Output: [4,1,2,3]
Explanation: 40 is the largest element. 10 is the smallest. 20 is the second smallest. 30 is the third smallest.
```

**Example 2:**

```
Input: arr = [100,100,100]
Output: [1,1,1]
Explanation: Same elements share the same rank.
```

**Example 3:**

```
Input: arr = [37,12,28,9,100,56,80,5,12]
Output: [5,3,4,2,8,6,7,1,3]
```

**Constraints**

- 0 <= arr.length <= 105
- -109 <= arr[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `arr`，用每个元素的秩（rank）替换该元素。  
秩（rank）表示元素的大小顺序，满足以下规则：

- 数组中数值越大，其秩越大。  
- 相同的数值拥有相同的秩。  
- 最小的数值的秩为 1，之后依次递增。

**示例**

**示例 1**  
```
Input: arr = [40,10,20,30]
Output: [4,1,2,3]
```
**解释**：40 是最大的元素，秩为 4。10 是最小的元素，秩为 1。20 是第二小的元素，秩为 2。30 是第三小的元素，秩为 3。

**示例 2**  
```
Input: arr = [100,100,100]
Output: [1,1,1]
```
**解释**：相同的元素共享相同的秩，均为 1。

**示例 3**  
```
Input: arr = [37,12,28,9,100,56,80,5,12]
Output: [5,3,4,2,8,6,7,1,3]
```

**约束条件**  
- `0 <= arr.length <= 10^5`  
- `-10^9 <= arr[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对数组里的每一个元素 `arr[i]`，都去遍历一遍整个数组，统计有多少个 **不同的** 元素比它小。  
- **统计方式**：把比 `arr[i]` 小的数全部记下来，用 `set` 去重后计数。  
- **类比**：想象你在课堂上点名，老师要给每个同学排座位号（rank），你只能逐个询问每位同学：“请问你前面有几位同学坐得比你靠前？”这就需要一次一次地去数。

这种方法一定能得到正确的 rank，因为我们真的把所有比它小的不同元素全部数了一遍。

#### 代码（Python）

```python
def array_rank_transform_brute(arr):
    """
    暴力解：对每个元素统计比它小的不同元素个数 → rank = count + 1
    时间复杂度 O(n^2)，空间复杂度 O(1)
    """
    n = len(arr)
    res = [0] * n               # 用来存放最终的 rank
    for i in range(n):
        smaller = set()         # 用 set 自动去重
        for j in range(n):
            if arr[j] < arr[i]:
                smaller.add(arr[j])
        # 小于它的不同元素有多少，就加一得到 rank
        res[i] = len(smaller) + 1
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  “n²” 表示如果数组有 10 000 个元素，程序大约要执行 10 000 × 10 000 = 1 亿次比较。随着 `n` 增大，耗时会呈二次方增长，算得很慢。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  只用了常数级别的额外变量 `smaller`（最坏情况下也只会装不超过 `n` 个元素），不随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每次都要遍历整个数组去找比当前元素小的数。  
如果我们能够一次性把所有元素的相对大小关系整理好，就不需要重复遍历。

**关键观察**：  
- 排序后，数组中相同的数会聚在一起。  
- 对于每一个 **不同的** 数，它的 rank 正好等于它在排好序的 **唯一值列表** 中的位置（从 1 开始计数）。

于是我们可以这样做：

1. **复制并排序**：把原数组复制一份 `sorted_arr`，对它进行升序排序。  
2. **去重**：遍历排好序的数组，遇到新值就给它分配下一个 rank，使用哈希表（字典）记录 `value → rank`。  
   - 哈希表就像一本“查字典”：单词是 `value`，对应的页码是 `rank`，查找时间是 O(1)。  
3. **映射回原数组**：再次遍历原数组，用哈希表把每个元素直接替换成它的 rank。

整个过程只需要两次线性遍历（一次排序除外），时间大幅降低。

#### 代码（Python）

```python
def array_rank_transform(arr):
    """
    最优解：排序 + 哈希表映射
    时间复杂度 O(n log n)（排序），空间复杂度 O(n)（哈希表 + 排序副本）
    """
    # 1. 复制并排序
    sorted_arr = sorted(arr)                 # O(n log n)

    # 2. 为每个唯一值分配 rank，保存到字典
    rank_map = {}                            # 哈希表：value -> rank
    rank = 1                                 # rank 从 1 开始
    for val in sorted_arr:
        # 只在第一次遇到该值时分配 rank，后面相同的值直接跳过
        if val not in rank_map:
            rank_map[val] = rank
            rank += 1

    # 3. 把原数组映射为对应的 rank
    return [rank_map[x] for x in arr]        # O(n)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  主要花在排序上，`log n` 是把 `n` 个数“层层拆分、合并”的代价。相较于暴力的 `O(n²)`，即使 `n` 达到 10⁵，`n log n` 仍然在几百万次级别，能够在一秒左右跑完。  
- **空间复杂度**：`O(n)`  
  需要额外的数组 `sorted_arr`（存放 `n` 个元素的拷贝）和哈希表 `rank_map`（最多存放 `n` 个唯一值）。这在题目允许的 10⁵ 规模内是可以接受的。

---

## 心得

- **核心技巧**：先排序再利用哈希表把“值 ↔ rank”映射起来。  
- **适用场景**：  
  1. “离散化”或“坐标压缩”——把任意大小的数映射到连续的 1~k 区间（如离线查询、线段树）。  
  2. “相对大小排序”——需要给每个元素标记它在整体中的顺序（如排行榜、分数排名）。  
  3. “去重后计数”——统计不同元素的出现顺序或频次。  
- **一句话总结**：**先把所有数排好序，再用哈希表一次性记住每个数的排名**。

---

## 反思

- **第一反应**：直接遍历统计每个数比多少其他数小——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记对相同的元素 **共享同一个 rank**，导致输出不符合题目要求。  
  - 在排序后直接使用下标作为 rank，未去重，会把相同的数算成不同的排名。  
- **下次遇到类似题**：第一步先 **思考是否可以把整个集合一次性整理（排序 / 哈希）**，再利用 **映射** 把结果快速写回原数组。这样可以把 “重复遍历” 的时间浪费降到最低。