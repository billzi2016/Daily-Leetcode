# #1122. 相对排序数组 / Relative Sort Array

> 难度：简单 · 标签：Array、Hash Table、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/relative-sort-array/)

---

## 题目（英文原版）

**Description**

Given two arrays arr1 and arr2, the elements of arr2 are distinct, and all elements in arr2 are also in arr1.
Sort the elements of arr1 such that the relative ordering of items in arr1 are the same as in arr2. Elements that do not appear in arr2 should be placed at the end of arr1 in ascending order.

**Examples**

**Example 1:**

```
Input: arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]
Output: [2,2,2,1,4,3,3,9,6,7,19]
```

**Example 2:**

```
Input: arr1 = [28,6,22,8,44,17], arr2 = [22,28,8,6]
Output: [22,28,8,6,17,44]
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 1000
- 0 <= arr1[i], arr2[i] <= 1000
- All the elements of arr2 are distinct.
- Each arr2[i] is in arr1.

---

## 题目（中文翻译）

给定两个数组 `arr1` 和 `arr2`，其中 `arr2` 的元素互不相同（distinct），且 `arr2` 中的所有元素都出现在 `arr1` 中。  
请对 `arr1` 进行排序，使得 `arr1` 中元素的相对顺序（relative ordering）与 `arr2` 中出现的顺序相同。未出现在 `arr2` 中的元素需放在 `arr1` 的末尾，并按升序排列。

**示例 1**  

**输入**  
```text
arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]
```
**输出**  
```text
[2,2,2,1,4,3,3,9,6,7,19]
```

**示例 2**  

**输入**  
```text
arr1 = [28,6,22,8,44,17], arr2 = [22,28,8,6]
```
**输出**  
```text
[22,28,8,6,17,44]
```

**约束条件**

- `1 <= arr1.length, arr2.length <= 1000`
- `0 <= arr1[i], arr2[i] <= 1000`
- `arr2` 的所有元素互不相同（distinct）。
- `arr2` 中的每个元素都在 `arr1` 中出现。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**按照 `arr2` 的顺序把 `arr1` 中对应的元素挑出来**，剩下的再排序放到后面。  
实现思路可以分三步：

1. **遍历 `arr2`**，对每个数在 `arr1` 中**线性搜索**所有出现的位置，把它们依次放进结果列表。  
2. 把已经取走的元素从 `arr1` 中删除（或标记为已使用），剩下的就是 **不在 `arr2` 中的元素**。  
3. 对剩下的元素直接使用 Python 自带的 `sort()`（升序），再接到结果后面。

> **类比**：把 `arr2` 想成一本“菜谱”，每道菜的名字在 `arr1` 这堆原材料里出现多次。我们逐本菜谱查找对应的原材料，找完菜谱后，把剩余的原材料按字母顺序（升序）排好。

这种方法**一定能得到正确答案**，因为我们严格遵循了题目要求的相对顺序，且把所有未出现的元素按照升序放在最后。

#### 代码（Python）
```python
def relativeSortArray_bruteforce(arr1, arr2):
    # 复制一份 arr1，避免在遍历时修改原数组
    remaining = arr1[:]          # 还未被挑选的元素
    result = []                  # 最终排序结果

    # 1. 按 arr2 的顺序把对应的元素全部取出
    for val in arr2:             # 遍历菜谱
        i = 0
        while i < len(remaining):
            if remaining[i] == val:
                result.append(val)   # 取出一个符合顺序的元素
                remaining.pop(i)     # 删除，后面的元素会左移
                # 删除后 i 不需要 +1，因为下一个元素已经移动到了当前位置
            else:
                i += 1                # 继续检查下一个位置

    # 2. 剩余的元素全部升序排列
    remaining.sort()               # Python 内置的快速排序（Timsort）
    result.extend(remaining)       # 把升序的剩余元素接在后面

    return result
```

#### 复杂度
- **时间复杂度**：`O(n * m)`  
  - `n = len(arr1)`，`m = len(arr2)`。我们对每个 `arr2` 的元素都要在 `arr1`（剩余部分）里遍历一次，最坏情况是 `arr1` 长度每次几乎不变，所以是两层循环的乘积。  
  - 用大白话说，就是“每吃一道菜都要把厨房里的所有材料重新检查一遍”，所以会慢。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表 `remaining`（复制了 `arr1`）和 `result`，共计约 `2n` 的空间。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **每次都要遍历整个 `arr1`** 来找 `arr2` 的元素。我们可以把这一步 **一次性完成**，用哈希表（字典）记录每个数在 `arr1` 中出现的次数。

**步骤拆解**：

1. **计数**：遍历 `arr1`，把每个数出现的次数放进字典 `cnt`。  
   - 类比：把所有原材料装进 **“统计表”**，表的左边是材料名字（数字），右边是数量（出现次数）。

2. **按照 `arr2` 的顺序输出**：遍历 `arr2`，把 `cnt` 中对应的次数的元素一次写进答案。写完后把该键从字典中删除。  
   - 这样就保证了相对顺序完全匹配 `arr2`。

3. **处理剩余元素**：此时字典里只剩下 **不在 `arr2` 中的数字**。因为题目限制 `0 ≤ num ≤ 1000`，我们可以使用 **计数排序**（Counting Sort）来一次性把它们按升序输出。计数排序的核心是：  
   - 先准备一个长度为 `max_val + 1`（这里是 1001）的数组 `bucket`，下标代表数字，值代表出现次数。  
   - 再从小到大遍历 `bucket`，把对应次数的数字写进答案。

**为什么计数排序合适**？  
- 题目给出的数值范围很小（最多 1000），所以用一个固定大小的“桶”来记录频次既省时又省空间。  
- 传统的比较排序（如快速排序）需要 `O(k log k)`（k 为剩余元素个数），而计数排序是 `O(range)`，这里的 range 固定为 1001，几乎是常数时间。

#### 代码（Python）
```python
def relativeSortArray_optimal(arr1, arr2):
    # 1. 统计 arr1 中每个数字出现的次数
    cnt = {}                         # 哈希表：数字 -> 出现次数
    for num in arr1:
        cnt[num] = cnt.get(num, 0) + 1

    result = []                      # 最终答案

    # 2. 按 arr2 的顺序把对应的数字写入 result
    for num in arr2:                 # 依次看菜谱里的每道菜
        times = cnt.pop(num)         # 取出该数字出现的次数并从哈希表中删除
        result.extend([num] * times) # 把该数字重复 times 次加入答案

    # 3. 处理剩余的数字（不在 arr2 中的），使用计数排序
    # 因为数值范围 ≤ 1000，创建长度为 1001 的桶
    bucket = [0] * 1001
    for num, times in cnt.items():  # 把剩余的计数填进桶里
        bucket[num] = times

    for num in range(1001):          # 从小到大遍历桶
        if bucket[num]:              # 桶里有该数字
            result.extend([num] * bucket[num])

    return result
```

#### 复杂度
- **时间复杂度**：`O(n + k)`  
  - `n = len(arr1)`：一次遍历计数。  
  - `k = 1001`（数值上限+1）：计数排序的遍历长度是固定常数，视作 `O(1)`，所以整体近似线性 `O(n)`。  
  - 与暴力解相比，**把原来的 `n*m` 降到了 `n`**，快了很多。

- **空间复杂度**：`O(k)`  
  - 需要额外的哈希表 `cnt`（最坏存 `n` 条目）和长度为 1001 的 `bucket`。因为 `k` 是常数级别的（1001），整体空间可以视作 `O(1)`（相对于输入规模），但严格来说是 `O(k)`。

---

## 心得

- **核心技巧**：**计数 + 哈希表**（先统计，再按自定义顺序输出），以及 **计数排序** 用于处理“剩余元素的升序”。  
- **适用的类似题型**  
  1. **Sort Colors**（颜色分类）——使用计数排序把 0、1、2 三种颜色分组。  
  2. **Intersection of Two Arrays II**（求两个数组的交集，考虑重复次数）——先计数后匹配。  
  3. **Top K Frequent Elements**（出现频率前 K 的元素）——同样需要统计频次，再排序或使用桶排序。  

- **一句话总结**：**先把“每个数字出现多少次”记下来，再按题目要求的顺序把它们搬出来，剩下的用计数排序一次性排好。**  

---

## 反思

- **第一反应**：看到“相对排序”，马上想到自定义比较函数 `sorted(arr1, key=...)`，但实现起来会涉及多次查表，效率不佳。  
- **最容易踩的坑**  
  1. **忘记删除已处理的数字**：如果在步骤 2 只把数字写进结果，却不从计数表中移除，后面计数排序会把它们再次输出。  
  2. **数值范围假设错误**：题目限制在 0~1000，才可以使用计数排序；如果范围更大，需要改用其他排序方式（如基数排序或堆）。  
  3. **边界情况**：`arr2` 可能为空，或 `arr1` 全部都在 `arr2` 中，代码都要能正常返回。  

- **下次遇到同类题**，第一步应该想到：**“先统计频次，再利用题目给出的顺序或范围进行一次性输出”。** 这一步往往可以把原本的双重循环降到线性时间。