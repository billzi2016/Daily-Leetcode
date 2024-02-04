# #2570. 合并两个二维数组并对值求和 / Merge Two 2D Arrays by Summing Values

> 难度：简单 · 标签：Array、Hash Table、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/merge-two-2d-arrays-by-summing-values/)

---

## 题目（英文原版）

**Description**

You are given two 2D integer arrays nums1 and nums2.
Each array contains unique ids and is sorted in ascending order by id.
Merge the two arrays into one array that is sorted in ascending order by id, respecting the following conditions:
Return the resulting array. The returned array must be sorted in ascending order by id.

**Examples**

**Example 1:**

```
Input: nums1 = [[1,2],[2,3],[4,5]], nums2 = [[1,4],[3,2],[4,1]]
Output: [[1,6],[2,3],[3,2],[4,6]]
Explanation: The resulting array contains the following:
- id = 1, the value of this id is 2 + 4 = 6.
- id = 2, the value of this id is 3.
- id = 3, the value of this id is 2.
- id = 4, the value of this id is 5 + 1 = 6.
```

**Example 2:**

```
Input: nums1 = [[2,4],[3,6],[5,5]], nums2 = [[1,3],[4,3]]
Output: [[1,3],[2,4],[3,6],[4,3],[5,5]]
Explanation: There are no common ids, so we just include each id with its value in the resulting list.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 200
- nums1[i].length == nums2[j].length == 2
- 1 <= idi, vali <= 1000
- Both arrays contain unique ids.
- Both arrays are in strictly ascending order by id.

---

## 题目（中文翻译）

**描述**  
给定两个二维整数数组（2D integer arrays）`nums1` 和 `nums2`。  
每个数组都只包含唯一的 `id`，并且已按照 `id` 的升序（ascending order）排序。  
请将这两个数组合并为一个新的数组，要求新数组仍然按 `id` 的升序排列，并满足以下条件：

- 若同一个 `id` 在两个数组中都出现，则在结果中该 `id` 对应的值为两个原始值之和。  
- 若某个 `id` 只出现在其中一个数组中，则在结果中保留该 `id` 以及它对应的原始值。  

返回合并后的数组，结果数组必须按 `id` 的升序排列。

**示例**  

示例 1:  
Input: `nums1 = [[1,2],[2,3],[4,5]], nums2 = [[1,4],[3,2],[4,1]]`  
Output: `[[1,6],[2,3],[3,2],[4,6]]`  
Explanation: 结果数组包含以下内容：  
- `id = 1`，该 `id` 的值为 `2 + 4 = 6`。  
- `id = 2`，该 `id` 的值为 `3`（仅在 `nums1` 中出现）。  
- `id = 3`，该 `id` 的值为 `2`（仅在 `nums2` 中出现）。  
- `id = 4`，该 `id` 的值为 `5 + 1 = 6`。

示例 2:  
Input: `nums1 = [[2,4],[3,6],[5,5]], nums2 = [[1,3],[4,3]]`  
Output: `[[1,3],[2,4],[3,6],[4,3],[5,5]]`  
Explanation: 两个数组中没有共同的 `id`，因此结果中直接保留每个 `id` 及其对应的值。

**约束条件**  

- `1 <= nums1.length, nums2.length <= 200`  
- `nums1[i].length == nums2[j].length == 2`  
- `1 <= id_i, val_i <= 1000`  
- 两个数组均只包含唯一的 `id`。  
- 两个数组均严格按 `id` 的升序排列。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把 `nums1` 的每一条记录都和 `nums2` 的每一条记录逐一比较。  
- **数据结构**：直接使用 **列表**（list）来存放结果。  
- **生活化类比**：把 `nums1` 想成一本通讯录，`nums2` 也是一本。我们要把两本通讯录里所有的“名字”（id）都列出来，如果同名则把对应的“电话号码”（value）相加。暴力做法相当于把两本通讯录一本一本地翻，对每个名字都去另一册里找一遍，像是“逐页对照”。  
- **正确性**：因为我们遍历了 `nums1` 的每个 id，并在 `nums2` 中寻找相同的 id（如果有），再把两边的 value 加起来；随后把 `nums2` 中没有出现在 `nums1` 里的 id 直接加入结果。所有可能出现的 id 都被处理到了，所以答案必然正确。  

#### 代码（Python）  

```python
def merge_bruteforce(nums1, nums2):
    # 先把 nums1 的所有记录放进结果列表
    res = []
    for id1, val1 in nums1:               # 对 nums1 的每一行
        found = False
        for id2, val2 in nums2:           # 在 nums2 里逐行查找相同的 id
            if id1 == id2:                # 找到相同 id
                res.append([id1, val1 + val2])  # 把两个值相加
                found = True
                break
        if not found:                     # 如果在 nums2 中没有相同的 id
            res.append([id1, val1])       # 直接把 nums1 的这条记录加入

    # 处理只出现在 nums2 里的 id
    for id2, val2 in nums2:
        # 检查这个 id 是否已经在结果里出现过
        if not any(id2 == x[0] for x in res):
            res.append([id2, val2])

    # 结果需要按照 id 的升序排列
    res.sort(key=lambda x: x[0])
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - 这里的 `n = len(nums1)`，`m = len(nums2)`。  
  - “O(n·m)” 可以理解为“如果 `nums1` 有 100 条，`nums2` 也有 100 条，就要做 100 × 100 = 10,000 次比较”。  
- **空间复杂度**：`O(n + m)`  
  - 需要额外的列表来存放合并后的结果，最坏情况下结果的长度等于两数组长度之和。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复遍历**：每次在 `nums2` 里找匹配的 id 都要从头扫到尾，导致时间呈平方级增长。  
既然题目已经保证两个数组**都已经按 id 升序排列**，我们可以像归并两个有序列表那样，只遍历一次就把它们合并——这就是**双指针**技巧。  

1. **准备两个指针** `i`（指向 `nums1`）和 `j`（指向 `nums2`），初始都指向各自的第一个元素。  
2. 每一步比较 `nums1[i][0]` 与 `nums2[j][0]`（即两个 id）。  
   - 若相等：把两个 value 加在一起，加入结果，并让 `i`、`j` 同时向后移动一位。  
   - 若 `nums1[i][0] < nums2[j][0]`：说明 `nums1[i]` 的 id 在 `nums2` 中不存在，直接把它加入结果，`i` 前进。  
   - 若 `nums1[i][0] > nums2[j][0]`：同理，把 `nums2[j]` 加入结果，`j` 前进。  
3. 当其中一个数组遍历完后，把剩余的另一数组全部复制到结果里。  

**类比**：把两条排好队的学生（按学号）分别站在两条队列的入口处，每次比较队首的学号，决定谁先出队。这样每个人只会被检查一次，效率自然高。  

#### 代码（Python）  

```python
def merge_optimal(nums1, nums2):
    i, j = 0, 0               # 双指针初始化
    res = []                  # 用来存放合并后的结果

    while i < len(nums1) and j < len(nums2):
        id1, val1 = nums1[i]
        id2, val2 = nums2[j]

        if id1 == id2:                    # 两个 id 相同，求和值
            res.append([id1, val1 + val2])
            i += 1
            j += 1
        elif id1 < id2:                   # nums1 的 id 更小，直接加入
            res.append([id1, val1])
            i += 1
        else:                             # nums2 的 id 更小，直接加入
            res.append([id2, val2])
            j += 1

    # 把剩余的元素全部追加到结果中
    while i < len(nums1):
        res.append(nums1[i])
        i += 1
    while j < len(nums2):
        res.append(nums2[j])
        j += 1

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 每个指针只会前进一次，等价于“一次遍历”。如果把 `n`、`m` 都看成 100，最多只会进行 200 次比较，远远小于 10,000 次。  
- **空间复杂度**：`O(n + m)`  
  - 需要存放合并后的数组，长度最多等于两数组长度之和。额外的辅助空间只有几个指针，视作常数。  

---  

## 心得  

- **核心技巧**：**双指针（归并）**——利用两个已排序序列的顺序特性，只遍历一次即可完成合并。  
- **适用的题型**：  
  1. 合并两个有序数组（LeetCode 88）  
  2. 合并两个有序链表（LeetCode 21）  
  3. 统计两个有序序列的交集或并集（LeetCode 349 / 350）  
- **一句话总结解题钥匙**：**“两个排好队的列表，比较队首，谁小谁先走”**。  

## 反思  

- **第一反应**：看到“两个数组都已经按 id 排序”，立刻想到可以用“双指针”一次遍历完成合并。  
- **最容易踩的坑**：  
  - 忘记在遍历结束后把未遍历完的那一侧全部加入结果。  
  - 对相同 id 的处理要先相加后同时移动两个指针，防止只移动一个导致重复或漏掉。  
- **下次遇到同类题**：第一步先确认是否有序，若有序则直接考虑**双指针归并**；若无序再考虑使用**哈希表**记录出现次数或求和。