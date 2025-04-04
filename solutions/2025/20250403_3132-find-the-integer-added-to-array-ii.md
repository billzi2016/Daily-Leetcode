# #3132. 找到添加到数组 II 的整数 / Find the Integer Added to Array II

> 难度：中等 · 标签：Array、Two Pointers、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-the-integer-added-to-array-ii/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2.
From nums1 two elements have been removed, and all other elements have been increased (or decreased in the case of negative) by an integer, represented by the variable x.
As a result, nums1 becomes equal to nums2. Two arrays are considered equal when they contain the same integers with the same frequencies.
Return the minimum possible integer x that achieves this equivalence.

**Examples**

**Example 1:**

```
Input: nums1 = [4,20,16,12,8], nums2 = [14,18,10]
Output: -2
Explanation:
After removing elements at indices [0,4] and adding -2, nums1 becomes [18,14,10] .
```

**Example 2:**

```
Input: nums1 = [3,5,5,3], nums2 = [7,7]
Output: 2
Explanation:
After removing elements at indices [0,3] and adding 2, nums1 becomes [7,7] .
```

**Constraints**

- 3 <= nums1.length <= 200
- nums2.length == nums1.length - 2
- 0 <= nums1[i], nums2[i] <= 1000
- The test cases are generated in a way that there is an integer x such that nums1 can become equal to nums2 by removing two elements and adding x to each element of nums1.

---

## 题目（中文翻译）

给定两个整数数组（integer array）`nums1` 和 `nums2`。  
从 `nums1` 中移除两个元素，其余所有元素都统一加上（或在 `x` 为负时减去）一个整数 `x`。  
这样操作后，`nums1` 与 `nums2` 相等。两个数组在包含相同整数且出现次数相同的情况下视为相等。  

返回能够实现上述等价关系的 **最小可能整数** `x`。

## 示例

### 示例 1
**输入**  
`nums1 = [4,20,16,12,8]`, `nums2 = [14,18,10]`  

**输出**  
`-2`  

**解释**  
先移除下标为 `[0,4]` 的元素，然后对剩余元素全部加上 `-2`，`nums1` 变为 `[18,14,10]`，此时与 `nums2` 相等。

### 示例 2
**输入**  
`nums1 = [3,5,5,3]`, `nums2 = [7,7]`  

**输出**  
`2`  

**解释**  
先移除下标为 `[0,3]` 的元素，然后对剩余元素全部加上 `2`，`nums1` 变为 `[7,7]`，此时与 `nums2` 相等。

## 约束条件
- `3 <= nums1.length <= 200`
- `nums2.length == nums1.length - 2`
- `0 <= nums1[i], nums2[i] <= 1000`
- 测试用例保证存在一个整数 `x`，使得通过移除两个元素并对 `nums1` 的每个元素加上 `x`，可以使 `nums1` 与 `nums2` 相等。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的两个人偷走的元素全部枚举出来」，然后看剩下的 `n‑2` 个数能不能通过同一个整数 `x` 平移得到 `nums2`。  
具体步骤如下：

1. **枚举要删掉的两下标** `i < j`（就像挑选两本要从书架上搬走的书）。  
2. 把这两个元素从 `nums1` 中删除，得到一个长度为 `n‑2` 的子数组 `rest`。  
3. 为了比较两个数组是否「相同」——即相同的数出现相同的次数——我们把 `rest` 与 `nums2` **都排序**（把书按字母顺序排好，方便一一对应）。  
4. 现在 `rest[k] + x` 必须等于 `nums2[k]`（对应位置的书名相差同一个常数），于是 `x = nums2[0] - rest[0]`。  
5. 用这个 `x` 检查所有位置的差值是否都相等，如果相等说明这一次删掉的两本书是可行的。  
6. 把所有可行的 `x` 收集起来，取最小的那个（最小指数值最小，负数更小）。

> **类比**：  
> - **哈希表**可以想象成「字典」——`key` 是单词，`value` 是页码。这里我们不需要哈希表，只用「排序」这个工具把两个“词典”对齐。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def find_min_x_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    ans = None                     # 用来保存当前找到的最小 x
    nums2_sorted = sorted(nums2)   # 先把 nums2 排序，后面会重复使用

    # 1️⃣ 枚举要删除的两个下标 (i, j)
    for i, j in combinations(range(n), 2):
        # 2️⃣ 生成删掉 i、j 后的剩余数组
        rest = [nums1[k] for k in range(n) if k != i and k != j]
        rest.sort()                # 3️⃣ 排序，方便一一对应

        # 4️⃣ 计算候选的 x（把最小的 rest 对齐到最小的 nums2）
        x = nums2_sorted[0] - rest[0]

        # 5️⃣ 检查所有位置的差值是否相同
        ok = all(rest[idx] + x == nums2_sorted[idx] for idx in range(n - 2))
        if ok:
            # 6️⃣ 记录最小的 x
            if ans is None or x < ans:
                ans = x

    return ans                     # 题目保证一定会有答案
```

#### 复杂度

- **时间复杂度**：`O(n^3)`  
  - 枚举两下标有 `C(n,2) ≈ n²/2` 种；每次要对长度为 `n‑2` 的数组排序，`O((n‑2) log(n‑2))`，再线性检查 `O(n)`。在最坏情况下这可以近似看成 `O(n³)`（因为 `n ≤ 200`，完全能跑完）。
  - **大白话**：想象你有 200 本书，挑两本出来要尝试 20,000 种组合，每种组合还要把剩下的书排一次序，这在电脑里还能接受，但不是最优的做法。

- **空间复杂度**：`O(n)`  
  - 主要是存放排序后的 `rest` 和 `nums2_sorted`，和输入大小同量级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **对每一对删掉的元素都要重新排序**。我们可以把排序提前，只做一次，然后用「双指针」一次遍历就找出哪些元素需要被跳过（即被删掉），从而得到合法的 `x`。

关键观察：

1. **平移不改变顺序**  
   给所有剩余元素加上同一个整数 `x`，它们的相对大小不变。因此如果把 `nums1` 与 `nums2` 都排好序，两个数组在对应位置的差值必须全部相同。

2. **只能跳过两次**  
   在对齐的过程中，我们可以把 `nums1` 中的元素「跳过」最多两次——这正好对应要删除的两个数。其余所有元素都必须和 `nums2` 的当前元素匹配（差值相同）。

3. **如何求 `x`**  
   假设我们已经跳过了 `skip`（0、1 或 2）个 `nums1` 的最小元素，那么第一个匹配的 `nums1` 元素是 `nums1[skip]`，对应的 `nums2` 最小元素是 `nums2[0]`。于是  
   `x = nums2[0] - nums1[skip]`。  
   为了得到 **最小的** `x`，我们只需要尝试 `skip = 0, 1, 2` 三种情况（因为只能在最前面跳过至多两个元素），把能成功对齐的 `x` 取最小即可。

4. **双指针检查**  
   - `i` 指向排序后的 `nums1`，`j` 指向排序后的 `nums2`。  
   - 设定好的 `x` 后，如果 `nums1[i] + x == nums2[j]`，说明这两个数匹配，两个指针都右移。  
   - 否则说明 `nums1[i]` 需要被删除（跳过），只移动 `i` 并计数 `skip_cnt`。  
   - 若 `skip_cnt` 超过 `2 - skip`（已经用掉的删除次数超过允许的），则这次 `x` 不可行。  
   - 遍历结束且 `skip_cnt` 正好不超过剩余可删次数，就说明 `x` 合法。

整个过程只需要 **一次排序**（`O(n log n)`)）和 **一次线性遍历**（`O(n)`），大幅提升效率。

#### 代码（Python）

```python
from typing import List

def find_min_x(nums1: List[int], nums2: List[int]) -> int:
    # 先把两数组都排序，后面只需要一次遍历
    a = sorted(nums1)
    b = sorted(nums2)
    n = len(a)          # = len(b) + 2
    best = None         # 记录当前找到的最小 x

    # 只需要尝试在最前面跳过 0、1、2 个元素的情况
    for skip_front in range(3):          # skip_front 表示在最开始就删掉的元素数
        if skip_front > 2:                # 实际上不会进入，因为 range(3) 已经限制
            break
        # 计算候选的 x：把 a[skip_front] 对齐到 b[0]
        x = b[0] - a[skip_front]

        i = skip_front       # a 的指针从 skip_front 开始
        j = 0                # b 的指针从 0 开始
        skipped = 0         # 已经跳过（删除）的元素数

        # 双指针遍历
        while i < n and j < len(b):
            if a[i] + x == b[j]:          # 匹配成功
                i += 1
                j += 1
            else:                          # a[i] 必须被删掉
                i += 1
                skipped += 1
                if skipped > 2 - skip_front:   # 超出允许的删除次数，直接放弃
                    break

        # 循环结束后，还可能剩下未遍历的 a 元素，这些也算是被删掉的
        skipped += (n - i)                 # 把尾部未使用的全部算进删除数

        if j == len(b) and skipped == 2 - skip_front:
            # 成功匹配且恰好用了完剩余的删除次数
            if best is None or x < best:
                best = x

    return best   # 题目保证一定会有答案
```

> **代码注释说明**  
> - `skip_front`：一开始就把最小的 `skip_front` 个元素当作被删除的元素。因为数组已经排好序，最小的几个元素最有可能是被删的（它们不需要参与对齐）。  
> - `skipped`：记录在遍历过程中因为不匹配而“跳过”的元素数量。  
> - `if skipped > 2 - skip_front`：一旦已经跳过的次数超过剩余可删次数，就可以提前结束本次尝试，省掉不必要的比较。  
> - 最后 `skipped += (n - i)` 把指针 `i` 之后剩下的全部算进删除，因为它们根本没有机会去匹配 `b`。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 只需要对 `nums1`、`nums2` 各自排序一次，`n ≤ 200`，排序耗时 `n log n`。  
  - 随后对每一种 `skip_front`（最多 3 次）做一次线性遍历 `O(n)`，整体仍是 `O(n log n)`。  
  - **对比**：相比暴力的 `O(n³)`，这相当于把「一次又一次的排队」变成「一次排好队后只走一趟」。

- **空间复杂度**：`O(n)`  
  - 需要额外存放排好序的两个数组（复制原数组），以及常数级的指针变量。

---

## 心得

- **核心技巧**：排序后利用双指针一次遍历，同时允许最多两次「跳过」元素（相当于删除）。  
- **适用的题型**  
  1. 两个数组只差若干个元素，需要找出删去/加入的最小/最大值（如 “Find the Integer Added to Array I”。）  
  2. 需要在保持相对顺序的前提下把一个数组平移到另一个数组（如 “Make Two Arrays Equal by Reversing Sub‑arrays”。）  
- **一句话总结**：**先排序，再用双指针把只能删两次的“跳过”次数限制住，就能一次遍历得到最小的平移值**。

---

## 反思

- **第一反应**：看到“删除两个元素 + 整体平移”，立刻想到「枚举删掉的两元素」——最直观但最慢的办法。  
- **最容易踩的坑**  
  - **边界条件**：删除的两个元素可能都在数组最前面或最末尾，必须在遍历结束后把剩余未使用的元素计入删除次数。  
  - **负数 x**：`x` 可以是负数，不能只考虑 `nums2` 大于 `nums1` 的情况。  
  - **最小 x 的定义**：题目要求「最小的整数」而不是「最小的绝对值」，因此要在所有合法 `x` 中取数值最小的（更负的更好）。  
- **下次思路**：遇到「删掉若干元素后整体变换」的题目，先**排序**，再**用指针模拟**「允许跳过」的操作，避免枚举所有组合。这样往往能把指数级的搜索压缩到线性或线性对数级。