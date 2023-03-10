# #2161. 根据给定枢轴划分数组 / Partition Array According to Given Pivot

> 难度：中等 · 标签：Array、Two Pointers、Simulation · [LeetCode 链接](https://leetcode.com/problems/partition-array-according-to-given-pivot/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer pivot. Rearrange nums such that the following conditions are satisfied:
Return nums after the rearrangement.

**Examples**

**Example 1:**

```
Input: nums = [9,12,5,10,14,3,10], pivot = 10
Output: [9,5,3,10,10,12,14]
Explanation: 
The elements 9, 5, and 3 are less than the pivot so they are on the left side of the array.
The elements 12 and 14 are greater than the pivot so they are on the right side of the array.
The relative ordering of the elements less than and greater than pivot is also maintained. [9, 5, 3] and [12, 14] are the respective orderings.
```

**Example 2:**

```
Input: nums = [-3,4,3,2], pivot = 2
Output: [-3,2,4,3]
Explanation: 
The element -3 is less than the pivot so it is on the left side of the array.
The elements 4 and 3 are greater than the pivot so they are on the right side of the array.
The relative ordering of the elements less than and greater than pivot is also maintained. [-3] and [4, 3] are the respective orderings.
```

**Constraints**

- 1 <= nums.length <= 105
- -106 <= nums[i] <= 106
- pivot equals to an element of nums.

---

## 题目（中文翻译）

给定一个 **0 索引** 整数数组 `nums` 和一个整数 `pivot`。请重新排列 `nums` 使得满足以下条件：

1. 所有 **小于** `pivot` 的元素位于数组的左侧；
2. 所有 **等于** `pivot` 的元素位于数组的中间；
3. 所有 **大于** `pivot` 的元素位于数组的右侧；
4. 在左侧和右侧内部，**相对顺序**（relative ordering）保持不变。

返回重新排列后的数组 `nums`。

## 示例

### 示例 1
**输入**  
```
nums = [9,12,5,10,14,3,10], pivot = 10
```
**输出**  
```
[9,5,3,10,10,12,14]
```
**解释**  
- 元素 `9、5、3` 都小于 `pivot`，因此位于数组左侧。  
- 元素 `12、14` 都大于 `pivot`，因此位于数组右侧。  
- 小于 `pivot` 的元素 `[9,5,3]` 与大于 `pivot` 的元素 `[12,14]` 的**相对顺序**均得到保留。

### 示例 2
**输入**  
```
nums = [-3,4,3,2], pivot = 2
```
**输出**  
```
[-3,2,4,3]
```
**解释**  
- 元素 `-3` 小于 `pivot`，位于左侧。  
- 元素 `4、3` 大于 `pivot`，位于右侧。  
- 小于 `pivot` 的子数组 `[-3]` 与大于 `pivot` 的子数组 `[4,3]` 的**相对顺序**均保持不变。

## 约束条件

- `1 <= nums.length <= 10^5`
- `-10^6 <= nums[i] <= 10^6`
- `pivot` 必然等于 `nums` 中的某个元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次遍历** 把满足条件的元素直接搬到目标位置。  
因为题目要求「相对顺序要保持不变」——比如原来 `9,5,3` 在数组里出现的先后顺序，最终也要保持 `9,5,3` 的顺序。  

如果我们在原数组上 **原地** 进行搬移，就需要把「小于 pivot」的元素一个个 **插入** 到左边合适的位置；这会导致后面的元素整体向右搬动，最坏情况下每插入一次都要搬动 `O(n)` 个元素，整体时间会是 `O(n²)`。

> **类比**：想象你在一本字典里把所有「小于某个字母」的单词搬到前面，却要保持它们原来的顺序。若每次搬动都把后面的页码整体往后推，工作量会非常大。

下面给出这种「暴力」实现（采用列表的 `insert` 方法），代码里每一步都有中文注释，便于理解。

#### 代码（Python）

```python
def partitionArray_bruteforce(nums, pivot):
    """
    暴力实现：在原数组上逐个插入
    时间复杂度会达到 O(n^2)，仅作演示
    """
    n = len(nums)
    i = 0  # i 用来遍历原数组
    while i < n:
        if nums[i] < pivot:                 # 需要移动到左边
            # 把当前元素插入到最左边（索引 0）后面的第一个位置
            # 这里会把前面的所有元素整体右移一位
            nums.insert(0, nums.pop(i))
            # 插入后，左边已经有一个新元素，i 需要往后走一位才能继续检查
            i += 1
        elif nums[i] == pivot:              # 与 pivot 相等的元素保持原位
            i += 1
        else:                               # 大于 pivot 的元素留在右边
            i += 1
    return nums
```

> **注意**：`list.pop(i)` 会把下标 `i` 的元素取出来并删除，随后 `insert(0, x)` 把它放到最左边。因为 `pop` 已经把数组长度减 1，`insert` 再把长度恢复，所以 `n` 不变。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  想象有 `n` 个元素，每次把一个「小于 pivot」的元素搬到左边，都要把它左侧的所有元素整体向右搬动，最坏情况相当于 `1 + 2 + … + (n-1) = O(n²)`。  
  用大白话说，就是「每搬一次，可能要搬很多次」。
- **空间复杂度**：`O(1)`（原地操作，只用了常数级别的临时变量）。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈** 在于「每次搬动都要把后面的元素整体右移」。  
如果我们把「左边」和「右边」的元素**提前**准备好，再一次性拼接，就可以 **避免重复搬移**，从而把时间降到线性 `O(n)`。

实现思路：

1. **遍历一次原数组**，把元素按三类分别放进三个临时列表  
   - `less`：所有 `< pivot` 的元素（保持出现顺序）  
   - `equal`：所有 `== pivot` 的元素（因为题目保证 pivot 至少出现一次，这里会有至少一个）  
   - `greater`：所有 `> pivot` 的元素（保持出现顺序）  
   这一步相当于「把小于、等于、大于的元素分别装进不同的盒子」。
2. **合并** 三个列表得到最终答案：`less + equal + greater`。  
   合并本身是 O(n) 的操作，因为只需要把每个元素拷贝一次到新的数组里。

> **类比**：想象你在超市排队结账，先把所有「买的水果」的购物篮放在左边，「买的蔬菜」放在右边，最后统一排成一列。你不需要在排队的过程中不停地换位，只要事先分好类，最后再把三段排好即可。

这种做法使用了 **额外的线性空间**（三个列表），但时间是线性的，已经是本题的最优解法（因为必须至少遍历一次数组）。

#### 代码（Python）

```python
def partitionArray(nums, pivot):
    """
    最优实现：一次遍历 + 三个临时列表（保持相对顺序）
    时间复杂度 O(n)，空间复杂度 O(n)
    """
    less = []      # 小于 pivot 的元素，保持原顺序
    equal = []     # 等于 pivot 的元素（至少有一个）
    greater = []   # 大于 pivot 的元素，保持原顺序

    for num in nums:               # 只遍历一次
        if num < pivot:
            less.append(num)       # 放进 less
        elif num == pivot:
            equal.append(num)      # 放进 equal
        else:
            greater.append(num)    # 放进 greater

    # 直接把三个列表拼接起来返回
    return less + equal + greater
```

> **关键行解释**  
> - `less.append(num)` / `greater.append(num)`: 把当前元素放进对应的“盒子”，相当于记下它出现的顺序。  
> - `return less + equal + greater`: Python 中列表相加会产生一个新列表，内部实现是一次性拷贝所有元素，时间仍是线性。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，后面的拼接也是线性操作。比暴力的 `O(n²)` 快了很多，尤其当 `n` 达到 `10⁵` 时差距尤为明显。  
- **空间复杂度**：`O(n)` — 需要额外存放 `less、equal、greater` 三个列表，总长度等于原数组长度。若不计输出数组本身，这算是额外的线性空间。

---

## 心得

- **核心技巧**：**一次遍历分桶（stable partition）**——把满足不同条件的元素分别收集到不同的容器里，再按需求合并。  
- **适用的题型**  
  1. **颜色分类**（如 LeetCode 75. 颜色分类）——把 0、1、2 三种颜色分别放进不同列表后合并。  
  2. **分组排序**（如 LeetCode 1122. 数组的相对排序）——根据另一个数组的顺序把元素分组。  
  3. **奇偶排序**（如 LeetCode 905. 按奇偶排序数组）——把奇数、偶数分别收集后拼接。  
- **一句话总结**：**先把不同类别的元素各自收集好，再一次性拼接，既保持顺序又线性完成。**

---

## 反思

- **第一反应**：看到「保持相对顺序」会想到「稳定」的划分，马上想到「用额外数组收集」而不是原地交换。  
- **最容易踩的坑**  
  1. **忘记保留等于 pivot 的元素**：只收集 `<` 与 `>`，导致答案缺少 pivot。  
  2. **错误地使用 `pop`/`insert` 原地搬移**：会破坏相对顺序或产生 `O(n²)` 的时间。  
  3. **边界条件**：数组全为 `< pivot` 或全为 `> pivot`，此时 `equal` 仍然需要保留（因为题目保证 pivot 出现），代码要能处理空的 `less/greater`。  
- **下次遇到同类题**：第一步先 **判断是否需要保持相对顺序**；如果需要，立刻考虑 **“一次遍历分桶”** 的思路；如果不需要，再思考 **双指针原地交换** 能否做到。