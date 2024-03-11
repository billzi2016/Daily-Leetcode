# #2610. 将数组转换为满足条件的二维数组 / Convert an Array Into a 2D Array With Conditions

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/convert-an-array-into-a-2d-array-with-conditions/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. You need to create a 2D array from nums satisfying the following conditions:
Return the resulting array. If there are multiple answers, return any of them.
Note that the 2D array can have a different number of elements on each row.

**Examples**

**Example 1:**

```
Input: nums = [1,3,4,1,2,3,1]
Output: [[1,3,4,2],[1,3],[1]]
Explanation: We can create a 2D array that contains the following rows:
- 1,3,4,2
- 1,3
- 1
All elements of nums were used, and each row of the 2D array contains distinct integers, so it is a valid answer.
It can be shown that we cannot have less than 3 rows in a valid array.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: [[4,3,2,1]]
Explanation: All elements of the array are distinct, so we can keep all of them in the first row of the 2D array.
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums`。请将 `nums` 重构为一个二维数组，使其满足以下条件：

- 每一行（row）中的元素互不相同，即行内元素唯一（distinct）。
- 同一个整数在不同的行中可以出现多次，但同一行中不能出现重复。
- 允许各行的元素个数不同。

返回满足条件的二维数组。如果存在多个答案，返回任意一个即可。

**示例 1**  
**输入**: `nums = [1,3,4,1,2,3,1]`  
**输出**: `[[1,3,4,2],[1,3],[1]]`  
**解释**: 我们可以构造如下的二维数组：  
- 行 1: `1,3,4,2`  
- 行 2: `1,3`  
- 行 3: `1`  

所有 `nums` 中的元素均被使用，并且每一行的元素均互不相同，满足要求。可以证明，在满足条件的数组中，行数最少为 3。

**示例 2**  
**输入**: `nums = [1,2,3,4]`  
**输出**: `[[4,3,2,1]]`  
**解释**: 数组中的所有元素均互不相同，故可以全部放在二维数组的第一行。

**约束条件**

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把元素一个一个放进已经建好的行**，如果当前行里已经有相同的数字，就换到下一行，直到找到可以放的行。  
- **数据结构**：我们用一个二维列表 `matrix` 保存所有行。`matrix[i]` 就相当于第 `i` 行的“抽屉”。  
- **类比**：把每一行想象成一本笔记本的页面，页面里不能出现重复的单词。我们手里有一串单词（数组），要把它们依次贴到页面上，若当前页面已经有这个单词，就换到别的页面继续贴。  
- **正确性**：只要我们遍历 **所有已有的行** 并把元素放到第一个不冲突的行里，就一定能得到一个满足“每行元素互不相同”的二维数组。因为我们只要保证不把同一个数放进同一行，题目就没有别的限制。  

这个办法的 **瓶颈** 在于每放一个数，都要遍历已有的所有行去检查是否冲突，最坏情况下行数会很多，导致整体运行慢。

#### 代码（Python）

```python
def find_matrix_bruteforce(nums):
    # 用来存放最终的二维数组，每个子列表是一行
    matrix = []

    for x in nums:                     # 逐个处理数组中的元素
        placed = False                 # 标记当前元素是否已经放进某行
        # 依次尝试把 x 放进已有的每一行
        for row in matrix:
            if x not in row:           # 行里没有出现过 x，说明可以放
                row.append(x)          # 把 x 加到这行的末尾
                placed = True
                break                  # 放好后直接退出内层循环
        # 如果所有已有的行都已经有 x，说明必须新建一行
        if not placed:
            matrix.append([x])          # 开辟新行，只放当前的 x

    return matrix
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`，其中 `n = len(nums)`，`m` 为最终行数的上界（最坏情况下等于 `n`），所以最坏会是 `O(n²)`。通俗地说，假如数组里全是相同的数字，我们每插入一个数字都要检查所有已经存在的行，行数会逐渐增多，导致检查次数呈二次增长。  
- **空间复杂度**：`O(n)`，因为最终的二维数组里恰好存放了所有 `n` 个元素，没有额外的辅助空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**行数的多少是决定性能的关键**。  
- **慢点在哪**：每插入一个元素都要遍历所有已有行，行数越多，检查越慢。  
- **观察**：如果一个数在原数组中出现了 `k` 次，那么**无论如何**，这 `k` 次必须分布在 **不同的行**，否则同一行会出现重复。于是**最少需要的行数**就是出现次数最多的那个数的出现次数，记作 `maxFreq`。  

**步骤**  

1. **统计每个数字出现的次数**（哈希表），同时记录出现次数的最大值 `maxFreq`。  
   - 哈希表就像一本“词典”，`key` 是数字，`value` 是它出现的次数。  
2. 创建 `maxFreq` 行的空列表 `rows = [[] for _ in range(maxFreq)]`。  
3. 再遍历一次哈希表，对每个数字 `num`，把它的每一次出现分别放到不同行里。  
   - 具体做法是：`for i in range(cnt): rows[i].append(num)`，这里的 `i` 正好是 0、1、…、`cnt-1`，保证同一个数字的不同拷贝落在不同的行。  
4. 最终 `rows` 即为满足条件且行数最少的二维数组。  

**为什么正确**  
- 每个数字的所有拷贝被分配到 **不同的行**（因为下标 `i` 不会重复），所以每行内部一定没有重复。  
- 行数正好是 `maxFreq`，而我们已经证明 **不可能用更少的行**（因为出现次数最多的数字需要这么多行），因此得到的是 **最少行数的解**。  

**类比**：想象你有若干种颜色的球，每种颜色的球数量不一样。你要把球放进若干个盒子，每个盒子里不能有相同颜色的球。最少需要多少盒子？答案就是出现最多的颜色的球的数量，因为那种颜色的球必须分到不同的盒子里。接下来，把每种颜色的球依次放进盒子，先把第一颗放进第 1 盒，第二颗放进第 2 盒……循环下去，就能把所有球装好且盒子最少。

#### 代码（Python）

```python
from collections import Counter

def find_matrix_optimal(nums):
    """
    将 nums 拆分成若干行，使每行元素互不相同，且行数最少。
    """
    # 1. 统计每个数出现的次数，同时得到最大出现次数
    freq = Counter(nums)          # 哈希表：key 为数字，value 为出现次数
    max_freq = max(freq.values()) # 需要的最少行数

    # 2. 初始化 max_freq 行的空列表
    rows = [[] for _ in range(max_freq)]

    # 3. 把每个数字的出现分配到不同的行
    for num, cnt in freq.items():       # 遍历每个不同的数字及其出现次数
        for i in range(cnt):            # 把它的第 i 次出现放到第 i 行
            rows[i].append(num)         # 这里保证同一数字不会落在同一行

    return rows
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 统计出现次数遍历一次数组 `O(n)`；  
  - 再遍历哈希表把元素分配到行里，总共仍然只处理每个元素一次（虽然是“出现次数”层面的遍历，但所有出现次数之和等于 `n`），所以整体线性。  
  - 与暴力解的二次时间相比，提升明显。  
- **空间复杂度**：`O(n)`。  
  - 哈希表需要存放每种不同数字的计数，最坏情况（所有数字都不相同）会有 `n` 条记录；  
  - 最终的二维数组同样保存了 `n` 个元素，没有额外的空间开销。

---

## 心得

- **核心技巧**：**利用出现次数的最大值决定最少行数**，并使用 **哈希表（计数） + 按出现次数分配到行** 的思路。  
- **适用的题型**：  
  1. “把数组拆分成若干子数组，使每个子数组满足某种唯一性条件”——例如 LeetCode 2610（本题）。  
  2. “把字符分配到若干行，使每行字符不重复”——如把字符串分配到多行打印的题目。  
  3. “最少多少组能把相同元素分开”——如安排课程表、会议室等冲突调度问题。  
- **一句话总结**：**行数 = 最大出现次数，按出现次数轮流填行**。

---

## 反思

- **第一反应**：看到“每行元素互不相同”，立刻想到逐行检查、冲突检测的暴力做法。  
- **最容易踩的坑**：  
  - 忽略了 **行数的下界**（必须不少于出现次数最多的元素的次数），导致写出只能“尽量放进去”但不一定最少行的算法。  
  - 在分配时没有保证同一数字的不同拷贝分到不同的行，可能出现同一行出现重复。  
- **下次思路**：  
  1. **先找下界**：思考题目中有什么硬性限制（如最大出现次数决定最少行数）。  
  2. **用计数**：快速统计出现次数，用哈希表把信息结构化。  
  3. **按下界构造**：直接构造满足下界的结构（这里是 `maxFreq` 行），再把元素均匀填进去。  

这样就能在保证正确性的前提下，直接得到最优解。