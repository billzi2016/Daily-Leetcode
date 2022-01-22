# #1640. 检查数组能否通过拼接形成 / Check Array Formation Through Concatenation

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/check-array-formation-through-concatenation/)

---

## 题目（英文原版）

**Description**

You are given an array of distinct integers arr and an array of integer arrays pieces, where the integers in pieces are distinct. Your goal is to form arr by concatenating the arrays in pieces in any order. However, you are not allowed to reorder the integers in each array pieces[i].
Return true if it is possible to form the array arr from pieces. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: arr = [15,88], pieces = [[88],[15]]
Output: true
Explanation: Concatenate [15] then [88]
```

**Example 2:**

```
Input: arr = [49,18,16], pieces = [[16,18,49]]
Output: false
Explanation: Even though the numbers match, we cannot reorder pieces[0].
```

**Example 3:**

```
Input: arr = [91,4,64,78], pieces = [[78],[4,64],[91]]
Output: true
Explanation: Concatenate [91] then [4,64] then [78]
```

**Constraints**

- 1 <= pieces.length <= arr.length <= 100
- sum(pieces[i].length) == arr.length
- 1 <= pieces[i].length <= arr.length
- 1 <= arr[i], pieces[i][j] <= 100
- The integers in arr are distinct.
- The integers in pieces are distinct (i.e., If we flatten pieces in a 1D array, all the integers in this array are distinct).

---

## 题目（中文翻译）

给定一个由互不相同的整数组成的数组 `arr` 和一个整数子数组（array of integer arrays）`pieces`，其中 `pieces` 中的整数也是互不相同的。你的目标是通过按任意顺序拼接 `pieces` 中的子数组来形成 `arr`，但 **不允许** 在每个子数组 `pieces[i]` 内重新排列整数。若能够通过 `pieces` 形成数组 `arr` 则返回 `true`，否则返回 `false`。

### 示例

**示例 1**  
Input: `arr = [15,88]`, `pieces = [[88],[15]]`  
Output: `true`  
**解释**: 先拼接 `[15]` 再拼接 `[88]`。

**示例 2**  
Input: `arr = [49,18,16]`, `pieces = [[16,18,49]]`  
Output: `false`  
**解释**: 虽然数字相同，但不能重新排列 `pieces[0]` 中的顺序。

**示例 3**  
Input: `arr = [91,4,64,78]`, `pieces = [[78],[4,64],[91]]`  
Output: `true`  
**解释**: 先拼接 `[91]`，再拼接 `[4,64]`，最后拼接 `[78]`。

### 约束条件

- `1 <= pieces.length <= arr.length <= 100`
- `sum(pieces[i].length) == arr.length`
- `1 <= pieces[i].length <= arr.length`
- `1 <= arr[i], pieces[i][j] <= 100`
- `arr` 中的整数互不相同。
- `pieces` 中的整数互不相同（即将 `pieces` 展平成一维数组后，所有整数互不相同）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **pieces** 中的所有子数组全部排列组合，尝试每一种排列方式把它们拼接起来，看得到的完整数组是否和 **arr** 完全相同。  

- **数据结构**：我们只需要普通的 `list`（列表）来保存每一种排列后的拼接结果。可以把排列想象成把一堆积木（每块积木是一段子数组）随意摆放顺序，然后把它们“黏”在一起形成一条长线。  
- **正确性**：只要枚举了 **所有** 可能的排列，必然会包含一种正确的排列（如果存在的话），因此只要在遍历过程中找到了等于 **arr** 的结果，就可以返回 `True`；遍历完仍未匹配则返回 `False`。  

#### 代码（Python）  

```python
import itertools
from typing import List

def canFormArray_bruteforce(arr: List[int], pieces: List[List[int]]) -> bool:
    """
    暴力枚举 pieces 的所有排列，然后逐一拼接检查是否等于 arr。
    """
    # 1) 生成 pieces 的所有排列（每一种排列都是一个 tuple）
    for perm in itertools.permutations(pieces):
        # 2) 把当前排列的子数组依次拼接成一个新列表
        merged = []                         # 用来保存拼接后的结果
        for piece in perm:                  # 逐块加入
            merged.extend(piece)            # extend 相当于把 piece 的所有元素一次性加进去
        # 3) 检查拼接结果是否和目标 arr 完全相同
        if merged == arr:                   # 完全相等则说明找到了合法的拼接顺序
            return True
    # 4) 所有排列都试过了，仍未匹配成功
    return False
```

#### 复杂度  

- **时间复杂度**：`O(k! * n)`  
  - `k = len(pieces)`，排列的总数是 `k!`（阶乘），每一次排列都需要把所有元素（共 `n = len(arr)`）拼接一次。阶乘增长极快，即使 `k=6` 已经是 720 种排列，远远超出题目给出的 100 的规模上限。  
  - 用大白话说，这相当于“把所有可能的积木摆放顺序都尝试一次”，每一次都要重新拼装一条长线，工作量非常大。  

- **空间复杂度**：`O(n)`  
  - 主要用于存放一次拼接后的 `merged` 列表，最大长度就是 `n`（即原数组的长度）。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有排列**，这一步完全没有利用题目给出的“每个数字在所有子数组中只出现一次”的信息。实际上，我们只需要知道每个位置的数字属于哪一段子数组，就能唯一确定拼接顺序，而不必尝试所有排列。  

**关键观察**  

1. **每个数字只出现一次** → 在 **arr** 中的每个位置，只会对应唯一的一个 `piece`。  
2. **子数组内部顺序不能改变** → 只要我们在 **arr** 的遍历过程中，遇到某个数字是某个 `piece` 的第一个元素，就必须一次性把整个 `piece` 按顺序匹配进去。  

基于上述两点，我们可以：

- 用 **哈希表**（Python 中的 `dict`）把每个 `piece` 的**首元素**映射到整段子数组。哈希表就像一本“字典”，键（key）是首元素，值（value）是对应的整段子数组。查询一个键的时间是 O(1)，非常快。  
- 然后遍历 **arr**，用指针 `i` 指向当前要匹配的下标。  
  - 取 `arr[i]`，在哈希表里查找是否有以它为首的 `piece`。  
  - 若没有 → 说明 **arr** 中出现了一个不属于任何子数组的数字，直接返回 `False`。  
  - 若有 → 取出对应的子数组 `p`，依次和 **arr** 中接下来的元素比较，确保顺序完全相同。比较成功后，`i` 跳过这段子数组的长度，继续向后检查。  

这样我们只遍历一次 **arr**，每一步的查找和比较都是常数或子数组长度的线性操作，整体时间线性。  

#### 代码（Python）  

```python
from typing import List

def canFormArray(arr: List[int], pieces: List[List[int]]) -> bool:
    """
    使用哈希表把每段子数组的首元素映射到整段子数组，
    然后一次遍历 arr 完成匹配。
    """
    # 1) 建立首元素 → 子数组 的映射（哈希表）
    first_to_piece = {}                     # 键：子数组的第一个数字，值：整段子数组
    for p in pieces:
        first_to_piece[p[0]] = p             # 把每个子数组的首元素记录下来

    i = 0                                    # i 指向 arr 当前待匹配的位置
    n = len(arr)

    while i < n:
        cur = arr[i]                         # 当前要匹配的数字
        if cur not in first_to_piece:        # 哈希表里找不到对应的子数组 → 不可能拼成
            return False

        piece = first_to_piece[cur]          # 取出对应的子数组
        # 2) 逐个比较子数组中的元素与 arr 中的元素是否一致
        for num in piece:
            if i >= n or arr[i] != num:      # 越界或不相等说明匹配失败
                return False
            i += 1                           # 匹配成功，指针向后移动

    # 循环结束说明所有元素都匹配成功
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们只遍历一次 **arr**（长度为 `n`），每个元素只被检查一次。哈希表的查找是常数时间 `O(1)`，所以整体是线性时间。  
  - 用大白话讲，就是“只走一遍数组”，没有任何重复的尝试。  

- **空间复杂度**：`O(k)`（`k = len(pieces)`）  
  - 额外使用的哈希表存放每段子数组的首元素到子数组的映射，最多有 `k` 条记录。`k` 不会超过 `n`，所以空间开销是线性可接受的。  

---

## 心得  

- **核心技巧**：利用“哈希表把每段子数组的首元素快速定位”，以及“遍历一次数组完成匹配”。  
- **适用的题型**  
  1. **Check Array Formation Through Concatenation**（本题）  
  2. **Array Restoration from Pieces**（类似把碎片拼回原数组）  
  3. **Form Array from Sub‑arrays**（子数组顺序固定，只需定位首元素）  
- **一句话总结解题钥匙**：**“先定位，再一次匹配”。**先用哈希表定位每个位置属于哪块子数组，再一次遍历完成全部匹配即可。  

---

## 反思  

- **第一反应**：看到“子数组内部顺序不能变”，立刻想到要按顺序逐段匹配，而不是随意拼接。  
- **最容易踩的坑**  
  - **遗漏边界检查**：在匹配子数组时，需要确保指针没有越界（`i >= n`）。  
  - **忘记使用哈希表**：直接遍历 `pieces` 去找匹配的子数组会导致每次查找都是 O(k) ，整体变成 O(n·k)。  
  - **特殊情况**：`pieces` 中的子数组长度为 1 时仍然适用；所有子数组正好覆盖 `arr`，但顺序错乱时要返回 `False`。  
- **下次遇到同类题**：第一步就思考**“有没有唯一的标识可以快速定位每块碎片？”**（如首元素、哈希值），随后用**一次线性遍历**完成匹配。