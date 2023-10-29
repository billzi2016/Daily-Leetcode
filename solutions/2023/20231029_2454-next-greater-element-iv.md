# #2454. Next Greater Element IV / Next Greater Element IV

> 难度：困难 · 标签：Array、Binary Search、Stack、Sorting、Heap (Priority Queue)、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/next-greater-element-iv/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of non-negative integers nums. For each integer in nums, you must find its respective second greater integer.
The second greater integer of nums[i] is nums[j] such that:
If there is no such nums[j], the second greater integer is considered to be -1.
Return an integer array answer, where answer[i] is the second greater integer of nums[i].

**Examples**

**Example 1:**

```
Input: nums = [2,4,0,9,6]
Output: [9,6,6,-1,-1]
Explanation:
0th index: 4 is the first integer greater than 2, and 9 is the second integer greater than 2, to the right of 2.
1st index: 9 is the first, and 6 is the second integer greater than 4, to the right of 4.
2nd index: 9 is the first, and 6 is the second integer greater than 0, to the right of 0.
3rd index: There is no integer greater than 9 to its right, so the second greater integer is considered to be -1.
4th index: There is no integer greater than 6 to its right, so the second greater integer is considered to be -1.
Thus, we return [9,6,6,-1,-1].
```

**Example 2:**

```
Input: nums = [3,3]
Output: [-1,-1]
Explanation:
We return [-1,-1] since neither integer has any integer greater than it.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的非负整数数组 `nums`。对于数组中的每个元素，需要找到它的 **第二大于它的整数**（second greater integer）。  

**第二大于它的整数** 定义为满足以下条件的 `nums[j]`：  

- `j > i`（在 `nums[i]` 的右侧）；  
- `nums[j] > nums[i]`（比 `nums[i]` 大）；  
- 在 `i` 与 `j` 之间（即 `i < k < j`）至少存在 **一个** 元素 `nums[k]` 使得 `nums[k] > nums[i]`（即已经出现过一次更大的元素）；  
- `j` 是满足上述条件的最小下标。  

如果不存在这样的 `nums[j]`，则该位置的第二大于它的整数记为 **-1**。  

返回一个整数数组 `answer`，其中 `answer[i]` 为 `nums[i]` 的第二大于它的整数。

## 示例

### 示例 1  
**输入**  
```
nums = [2,4,0,9,6]
```  
**输出**  
```
[9,6,6,-1,-1]
```  
**解释**  
- 下标 0：`4` 是第一个大于 `2` 的整数，`9` 是第二个大于 `2` 的整数，位于 `2` 的右侧。  
- 下标 1：`9` 是第一个大于 `4` 的整数，`6` 是第二个大于 `4` 的整数，位于 `4` 的右侧。  
- 下标 2：`9` 是第一个大于 `0` 的整数，`6` 是第二个大于 `0` 的整数，位于 `0` 的右侧。  
- 下标 3：右侧不存在大于 `9` 的整数，故为 `-1`。  
- 下标 4：右侧不存在大于 `6` 的整数，故为 `-1`。  

### 示例 2  
**输入**  
```
nums = [3,3]
```  
**输出**  
```
[-1,-1]
```  
**解释**  
两个元素左侧都没有任何更大的整数，因此均返回 `-1`。

## 约束条件
- `1 <= nums.length <= 10^5`  
- `0 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对每一个位置 `i`，从 `i+1` 开始往右看，先找到**第一个**比 `nums[i]` 大的数 `first`，再继续往右找**第二个**比 `nums[i]` 大的数 `second`。  
- 如果在遍历的过程中找不到第一个更大的数，直接把答案记成 `-1`（因为连第一个都没有，更不可能有第二个）。  
- 如果只找到了第一个，却再也找不到第二个，同样记 `-1`。  

这相当于把每个元素的“右侧更大数”当成一张“查字典”。我们把 `i` 看成单词，`first`、`second` 看成词义的第 1、2 条解释。  
因为我们是从左到右、逐个检查的，必然能找到所有符合条件的 `second`，所以方法是 **一定正确** 的。

**为什么会慢？**  
对每个 `i` 都要向右遍历最坏 `n‑1` 次，整体是 `n` 次 * `n` 次 → `O(n²)`。当 `n` 达到 10⁵ 时，计算量会非常大，几乎不可能在 1 秒内跑完。

#### 代码（Python）

```python
from typing import List

def secondGreaterElement_brute(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [-1] * n                     # 默认答案是 -1
    for i in range(n):
        first_found = False            # 是否已经找到第一个更大的数
        for j in range(i + 1, n):      # 从 i 右边开始往后找
            if nums[j] > nums[i]:      # 只要比当前数大就算是更大数
                if not first_found:    # 第一次遇到更大数
                    first_found = True
                else:                  # 已经找到了第一个，这次就是第二个
                    ans[i] = nums[j]
                    break               # 找到第二个就可以停止内部循环
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  “n²” 可以想象成把一个 `n×n` 的格子全部遍历一遍。对 10⁵ 的数据来说，格子数是 10¹⁰，远远超出计算机的承受范围。  
- **空间复杂度：** `O(1)`（不计答案数组）  
  只用了常数级别的额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要线性扫描右侧**。我们需要一种“记住还没有找到第二个更大数的元素”，并且在后面出现合适的更大数时**立刻把答案填上**，而不是等到遍历结束后再去找。

下面的优化思路分三层：

1. **第一层——单调栈（First Greater Stack）**  
   - 用一个 **递减栈**（栈顶元素最小）存放**还没有找到第一个更大数**的下标。  
   - 当遍历到新元素 `x = nums[cur]` 时，只要栈顶对应的值 `< x`，说明 `x` 就是这些下标的**第一个更大数**。把这些下标弹出栈，转交给第二层处理。

2. **第二层——有序结构（堆）保存“已经找到第一个更大数，但还没找到第二个”的下标**  
   - 对每个刚刚弹出栈的下标 `idx`，把 `(nums[idx], idx)` 放进 **最小堆**。堆会把**最小的原始值**排在最前面。  
   - 这样，堆里的元素始终是“已经等到了第一个更大数，现在只等第二个更大数”。因为我们只关心 **第二个更大数**，所以只要当前遍历的 `x` 大于堆顶的 **原始值**，`x` 就是该下标的**第二个更大数**。

3. **第三层——直接写答案**  
   - 再次检查堆：只要堆不为空且 `heap[0][0] < x`，弹出堆顶 `(val, idx)`，把答案 `ans[idx] = x`。  
   - 弹出后，这个下标已经找到了第二个更大数，后面再也不用管。

整个过程只遍历一次数组，每个下标最多进出栈一次、进出堆一次，**所有操作都是 `O(log n)` 或 `O(1)`**，所以总时间是 `O(n log n)`。

> **类比**：  
> - **递减栈** 像是“排队等候的学生”，他们在找第一个比自己更高的老师。  
> - **堆** 像是“已经找到了第一位老师，但还在等第二位老师的学生”。老师出现的顺序是随时间变化的，堆帮我们快速找到“当前老师最适合的学生”。

#### 代码（Python）

```python
import heapq
from typing import List

def secondGreaterElement(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [-1] * n                     # 最终答案，默认 -1

    first_stack = []                   # 单调递减栈，存下标
    waiting_heap = []                  # 最小堆，元素形如 (original_value, index)

    for cur, cur_val in enumerate(nums):
        # ---------- 第三层：处理已经在堆里的“第二个更大数” ----------
        # 只要堆顶的原始值比当前值小，当前值就是它的第二个更大数
        while waiting_heap and waiting_heap[0][0] < cur_val:
            _, idx = heapq.heappop(waiting_heap)
            ans[idx] = cur_val          # 写答案

        # ---------- 第二层：把刚刚找到“第一个更大数”的下标放进堆 ----------
        while first_stack and nums[first_stack[-1]] < cur_val:
            idx = first_stack.pop()     # 这个下标的第一个更大数就是 cur_val
            # 把它交给堆，等后面更大的数来完成第二个更大数
            heapq.heappush(waiting_heap, (nums[idx], idx))

        # ---------- 第一层：把当前下标加入递减栈，等待它的第一个更大数 ----------
        first_stack.append(cur)

    return ans
```

> **代码要点注释**  
> - `first_stack` 保持 **递减**（栈顶最小），这样只要遇到更大的数，就能一次性弹出所有“等待第一个更大数”的下标。  
> - `heapq` 实现的最小堆可以在 `O(log n)` 时间内弹出当前最小的原始值，确保我们总是先处理最早可能得到第二个更大数的下标。  
> - 最后遍历结束后，仍然在栈或堆里的下标说明它们没有第二个更大数，答案已经保持为 `-1`。

#### 复杂度  

- **时间复杂度：** `O(n log n)`  
  - 每个元素最多 **一次** 入栈、一次出栈（`O(1)`），以及 **一次** 入堆、一次出堆（`O(log n)`）。  
  - 与暴力的 `O(n²)` 相比，`log n` 只相当于把 “十万” 级别的遍历压缩成 “十几” 次操作，跑起来非常快。  

- **空间复杂度：** `O(n)`  
  - 最坏情况下，所有下标可能同时在栈或堆里（比如严格递减的数组），需要额外线性空间来保存它们。  
  - 这与输入规模同阶，属于合理的额外空间。

---

## 心得  

- **核心技巧**：**单调栈 + 最小堆（有序结构）** 用来分两阶段“找第一更大、找第二更大”。  
- **适用的类似题型**  
  1. *Next Greater Element I/II/III*（只找第一个更大数）——单调栈即可。  
  2. *Find the K‑th Greater Element*（找第 K 大的更大数）——可以在栈的基础上加入多层有序结构或多次堆操作。  
  3. *Maximum of Subarray Minimums*（子数组最小值的最大值）——也常用单调栈配合计数。  

- **一句话总结解题钥匙**：**把“等待第一个更大数”和“已经等到第一个、正在等第二个”的元素分层管理，利用有序结构快速匹配第二个更大数**。

---

## 反思  

- **第一反应**：直接暴力遍历每个元素的右侧。  
- **最容易踩的坑**  
  - **边界条件**：数组长度只有 1 或全部相同的情况，答案全是 `-1`。  
  - **堆中存的键**必须是**原始值**（而不是下标），否则比较的对象不对。  
  - **栈的单调性**一定是递减的（`nums[stack[-1]] >= nums[i]`），否则会错误弹出不该弹出的元素。  

- **下次遇到同类题**，第一步应该想到：  
  1. **是否可以把“第一次满足条件的”过程抽象成单调栈**？  
  2. **剩下的“第二次/第 K 次”是否可以用有序结构（堆、平衡树）来维护等待队列**？  

这样就能快速从暴力转向高效的分层解法。