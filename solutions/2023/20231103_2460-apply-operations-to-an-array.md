# #2460. **Apply Operations to an Array** / Apply Operations to an Array

> 难度：简单 · 标签：Array、Two Pointers、Simulation · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of size n consisting of non-negative integers.
You need to apply n - 1 operations to this array where, in the ith operation (0-indexed), you will apply the following on the ith element of nums:
After performing all the operations, shift all the 0's to the end of the array.
Return the resulting array.
Note that the operations are applied sequentially, not all at once.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,1,1,0]
Output: [1,4,2,0,0,0]
Explanation: We do the following operations:
- i = 0: nums[0] and nums[1] are not equal, so we skip this operation.
- i = 1: nums[1] and nums[2] are equal, we multiply nums[1] by 2 and change nums[2] to 0. The array becomes [1,4,0,1,1,0].
- i = 2: nums[2] and nums[3] are not equal, so we skip this operation.
- i = 3: nums[3] and nums[4] are equal, we multiply nums[3] by 2 and change nums[4] to 0. The array becomes [1,4,0,2,0,0].
- i = 4: nums[4] and nums[5] are equal, we multiply nums[4] by 2 and change nums[5] to 0. The array becomes [1,4,0,2,0,0].
After that, we shift the 0's to the end, which gives the array [1,4,2,0,0,0].
```

**Example 2:**

```
Input: nums = [0,1]
Output: [1,0]
Explanation: No operation can be applied, we just shift the 0 to the end.
```

**Constraints**

- 2 <= nums.length <= 2000
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

你得到一个下标从 0 开始、长度为 *n* 的整数数组 `nums`，其中所有元素均为非负整数。  
需要对该数组依次执行 **n‑1** 次操作。第 *i* 次操作（下标从 0 开始）针对 `nums[i]` 执行以下步骤：

- 如果 `nums[i]` 与 `nums[i+1]` 相等，则把 `nums[i]` 乘以 2（即 `nums[i] = nums[i] * 2`），并将 `nums[i+1]` 置为 0。
- 否则不做任何修改。

所有操作按顺序执行完毕后，将数组中的所有 0 移动到数组的末尾（保持非零元素的相对顺序不变），并返回得到的数组。

> 注意：上述操作是**顺序**进行的，而不是一次性并行完成。

---

### 示例

#### 示例 1  
**输入**  
```text
nums = [1,2,2,1,1,0]
```  

**输出**  
```text
[1,4,2,0,0,0]
```  

**解释**  
我们依次执行如下操作：

- `i = 0`：`nums[0]` 与 `nums[1]` 不相等，跳过此操作。  
- `i = 1`：`nums[1]` 与 `nums[2]` 相等，`nums[1]` 乘以 2 变为 4，`nums[2]` 置为 0。数组变为 `[1,4,0,1,1,0]`。  
- `i = 2`：`nums[2]` 与 `nums[3]` 不相等，跳过此操作。  
- `i = 3`：`nums[3]` 与 `nums[4]` 相等，`nums[3]` 乘以 2 变为 2，`nums[4]` 置为 0。数组变为 `[1,4,0,2,0,0]`。  
- `i = 4`：`nums[4]` 与 `nums[5]` 相等（均为 0），`nums[4]` 乘以 2 仍为 0，`nums[5]` 仍为 0。数组保持 `[1,4,0,2,0,0]`。

完成所有操作后，将所有 0 移动到末尾，得到 `[1,4,2,0,0,0]`。

---

#### 示例 2  
**输入**  
```text
nums = [0,1]
```  

**输出**  
```text
[1,0]
```  

**解释**  
没有任何相邻元素相等可以进行操作，直接把 0 移动到数组末尾，得到 `[1,0]`。

---

### 约束条件

- `2 <= nums.length <= 2000`
- `0 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步照题目描述去做**，把所有的操作都模拟一遍：

1. 从左到右遍历数组 `nums`（下标 `i` 从 `0` 到 `n‑2`）。  
2. 每次检查相邻的两个元素 `nums[i]` 和 `nums[i+1]`：  
   - 如果相等，就把左边的 `nums[i]` 乘以 `2`，把右边的 `nums[i+1]` 设成 `0`。  
   - 否则什么也不做，直接进入下一个 `i`。  
3. 所有 `n‑1` 次操作结束后，题目要求 **把所有的 0 移到数组末尾**。  
   - 最笨的办法是每次发现一个 `0`，就把它后面的所有元素左移一位，再在数组最后补一个 `0`。这相当于 “把 0 当作石子，挖掉它后让后面的石子往左滚”。  

> **类比**：哈希表像一本词典，`key` 是单词，`value` 是页码。这里的“左移”可以想象成把书页的空白页（0）撕掉，然后把后面的页码往前搬，最后在书的最后补上一页空白。

这种做法一定能得到正确答案，因为我们严格按照题目规定的顺序执行了每一步，而且最后把所有的 `0` 按要求搬到了最右侧。

#### 代码（Python）

```python
def applyOperations(nums):
    n = len(nums)

    # 1️⃣ 按题目顺序模拟 n-1 次操作
    for i in range(n - 1):
        if nums[i] == nums[i + 1]:          # 相邻相等才动手
            nums[i] *= 2                    # 左边翻倍
            nums[i + 1] = 0                 # 右边归零

    # 2️⃣ 暴力把所有 0 移到末尾
    #   每遇到一个 0，就把后面的元素整体左移一格
    i = 0
    while i < n:                           # 用 while 是因为左移会改变下标
        if nums[i] == 0:
            # 把 i 位置之后的所有数往左搬一位
            for j in range(i + 1, n):
                nums[j - 1] = nums[j]
            nums[-1] = 0                    # 最后补上一个 0
            # 继续检查同一个位置，因为左移后新来的数可能也是 0
        else:
            i += 1                           # 只要不是 0，指针往前走

    return nums
```

> 关键行中文注释已经标注，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 第一次遍历本身是 `O(n)`，但把每个 `0` 往后搬的过程是 **每搬一次可能要遍历整个数组的剩余部分**，最坏情况下会出现 `1 + 2 + … + (n‑1) = O(n²)` 次元素移动。  
  - 用大白话说，就是如果数组里全是 `0`，我们每次都要把后面的所有数往左搬一次，搬的次数会像累加一样快速增长。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（循环计数器），没有额外的数组或哈希表。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于把 `0` 挪到末尾时的“逐个左移”。  
我们可以把 **所有非零元素先收集起来**，再一次性把 `0` 填到数组尾部，这样只需要一次遍历就能完成全部工作。

实现思路：

1. **双指针**（Two Pointers）  
   - `write` 指针指向“下一个该写入非零数的位置”。一开始指向 `0`。  
   - `read` 指针从左到右扫描整个数组。  
   - 当 `nums[read]` 不是 `0` 时，把它写到 `nums[write]`，随后 `write` 向右移动一格。  
   - 这样遍历结束后，`0 … write‑1` 区间保存了所有非零数且顺序不变。

2. **填充 0**  
   - 再一次遍历 `write` 到数组末尾的位置，把每个位置设为 `0`。  

整个过程只用了两次线性遍历，**没有任何元素的重复搬移**，所以时间是 `O(n)`。

> **类比**：把数组想象成一条装满水果的传送带。`read` 是检查水果的新手，`write` 是装箱员。新手把好的水果递给装箱员，装箱员把它们依次放进盒子（前面的格子），最后把空盒子（0）统一放到传送带的后面。

#### 代码（Python）

```python
def applyOperations(nums):
    n = len(nums)

    # ① 先完成题目规定的 n-1 次“相等合并”操作
    for i in range(n - 1):
        if nums[i] == nums[i + 1]:
            nums[i] *= 2
            nums[i + 1] = 0

    # ② 双指针：把所有非零数搬到左边
    write = 0                     # 下一个该写入非零数的位置
    for read in range(n):
        if nums[read] != 0:       # 只处理非零
            nums[write] = nums[read]
            write += 1            # 写入后，写指针右移

    # ③ 把剩余位置全部填成 0
    while write < n:
        nums[write] = 0
        write += 1

    return nums
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只用了两次线性遍历，和数组长度成正比。相比暴力的 `O(n²)`，速度提升了 **数倍**（尤其在 `n` 较大时差别明显）。
- **空间复杂度**：`O(1)` — 仍然只使用了常数级别的额外变量 `write`、`read`。

---

## 心得

- **核心技巧**：**双指针**（Two Pointers）用于“压缩”数组，把满足条件的元素前移、把不需要的元素（这里是 0）统一放到末尾。  
- **适用的题型**：  
  1. “移动零”类（LeetCode 283 Move Zeroes）  
  2. “删除特定元素后压缩数组”类（LeetCode 27 Remove Element）  
  3. “数组中保留奇数/偶数后压缩”类等  
- **一句话总结**：**先模拟合并，再用双指针一次性把所有非零数搬到左侧，最后补零**。

---

## 反思

- **第一反应**：看到“相等就合并、随后把 0 移到末尾”，立刻想到 **按顺序模拟**，然后手动把 0 往右搬。  
- **最容易踩的坑**：  
  - 忘记“操作是顺序进行的”，不能一次性把所有相等的对都合并后再统一搬零。  
  - 在搬零时使用 `for` 循环直接 `pop`/`insert`，会导致 **索引错位** 或 **时间复杂度升到 O(n²)**。  
  - 边界条件：数组长度为 `2` 时只会有一次检查，需要确保 `i` 的上限是 `n‑2`。  
- **下次类似题的第一步**：先 **写出原始的模拟过程**，确认操作顺序；随后思考 **是否有“压缩”或“筛选”** 的需求，决定是否使用双指针或快慢指针一次遍历完成。