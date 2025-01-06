# #3011. 判断数组是否可排序 / Find if Array Can Be Sorted

> 难度：中等 · 标签：Array、Bit Manipulation、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-if-array-can-be-sorted/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers nums.
In one operation, you can swap any two adjacent elements if they have the same number of set bits. You are allowed to do this operation any number of times (including zero).
Return true if you can sort the array in ascending order, else return false.

**Examples**

**Example 1:**

```
Input: nums = [8,4,2,30,15]
Output: true
Explanation: Let's look at the binary representation of every element. The numbers 2, 4, and 8 have one set bit each with binary representation "10", "100", and "1000" respectively. The numbers 15 and 30 have four set bits each with binary representation "1111" and "11110".
We can sort the array using 4 operations:
- Swap nums[0] with nums[1]. This operation is valid because 8 and 4 have one set bit each. The array becomes [4,8,2,30,15].
- Swap nums[1] with nums[2]. This operation is valid because 8 and 2 have one set bit each. The array becomes [4,2,8,30,15].
- Swap nums[0] with nums[1]. This operation is valid because 4 and 2 have one set bit each. The array becomes [2,4,8,30,15].
- Swap nums[3] with nums[4]. This operation is valid because 30 and 15 have four set bits each. The array becomes [2,4,8,15,30].
The array has become sorted, hence we return true.
Note that there may be other sequences of operations which also sort the array.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: true
Explanation: The array is already sorted, hence we return true.
```

**Example 3:**

```
Input: nums = [3,16,8,4,2]
Output: false
Explanation: It can be shown that it is not possible to sort the input array using any number of operations.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 28

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的正整数数组 `nums`。  
一次操作可以交换任意两个**相邻元素**，前提是这两个元素的**置位（set bits）**数相同。你可以执行任意次数（包括 0 次）此操作。  
如果可以通过上述操作将数组按升序排序，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入**: `nums = [8,4,2,30,15]`  
**输出**: `true`  
**解释**: 先看每个元素的二进制表示。数字 2、4、8 的置位数各为 1，二进制分别为 `"10"`、`"100"`、`"1000"`。数字 15、30 的置位数各为 4，二进制分别为 `"1111"`、`"11110"`。  
我们可以通过 4 次操作将数组排序:
- 交换 `nums[0]` 与 `nums[1]`。此操作…

（后续过程省略）

### 示例 2
**输入**: `nums = [1,2,3,4,5]`  
**输出**: `true`  
**解释**: 数组已经是升序的，直接返回 `true`。

### 示例 3
**输入**: `nums = [3,16,8,4,2]`  
**输出**: `false`  
**解释**: 可以证明，无论进行多少次上述操作，都无法将该数组排序。

## 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 28`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有能做的交换都枚举一遍**，看能否把数组变成递增序列。  
具体做法可以把数组看成一棵“状态树”：

* 每个节点是当前数组的一个排列。  
* 从一个节点出发，如果相邻两个数的 **二进制 1 的个数（即 set bits）相同**，就可以交换它们，得到子节点。  

我们可以用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）** 把这棵树遍历完，  
只要在遍历过程中碰到已经排好序的数组，就返回 `True`，否则遍历完所有可能的排列后返回 `False`。

> **为什么这个方法能得到正确答案？**  
> 因为搜索过程穷举了 **所有** 通过合法交换能够到达的排列，只要有一种能得到有序数组，搜索一定会发现它。

> **为什么它不适合大输入？**  
> 每一次合法交换都可能产生新的排列，排列的数量在最坏情况下是 `n!`（全排列的个数），  
> 对于 `n = 100` 的情况下，根本不可能在合理时间内遍历完。

#### 代码（Python）

```python
from collections import deque

def popcount(x: int) -> int:
    """返回整数 x 的二进制中 1 的个数"""
    return bin(x).count('1')

def can_sort_bruteforce(nums):
    """暴力 BFS 版，适用于长度很小的测试（如 n <= 6）"""
    start = tuple(nums)                     # 用 tuple 方便放进集合
    target = tuple(sorted(nums))
    if start == target:
        return True

    visited = {start}
    q = deque([start])

    while q:
        cur = q.popleft()
        # 枚举所有相邻且 popcount 相同的位置进行交换
        for i in range(len(cur) - 1):
            if popcount(cur[i]) == popcount(cur[i + 1]):
                nxt = list(cur)
                nxt[i], nxt[i + 1] = nxt[i + 1], nxt[i]   # 交换
                nxt = tuple(nxt)
                if nxt == target:
                    return True
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
    return False
```

> **关键行注释**  
> - `popcount`：把整数的二进制表示转成字符串，统计 `'1'` 的个数，类似“查字典”里找词的出现次数。  
> - `visited`：记录已经遍历过的排列，防止无限循环，就像在迷宫里已经走过的路不再回头。  

#### 复杂度  

- **时间复杂度**：`O(k * n)`，其中 `k` 是所有可达排列的数量。最坏情况下 `k` 接近 `n!`，即**阶乘级别**，远远超出 1 秒能接受的范围。  
- **空间复杂度**：`O(k * n)` 用来保存已访问的排列，同样是指数级别。

> **大白话解释**：`O(n!)` 就像把所有可能的排队顺序都列出来，人数越多，组合数会“炸裂”——根本不可能完整遍历。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有排列**。  
其实我们并不需要真的去交换，只要判断**是否有可能**交换到有序即可。

观察交换规则：

* 只能交换 **相邻且 popcount 相同** 的元素。  
* 这意味着 **不同 popcount 的元素永远不会相互穿过**，它们的相对顺序是固定的。  

可以把数组划分成若干 **段（segment）**：

* 同一段里的所有元素 **popcount 相同**，且在原数组中是连续的。  

在同一段内部，任意两个元素都可以通过一系列合法相邻交换互换位置（相当于普通的冒泡排序），  
所以**段内的元素可以随意重新排列**，但**段与段之间的顺序永远保持不变**。

因此，判断能否排序只需要：

1. **对每个段内部进行排序**（把段内的数从小到大排好）。  
2. 把所有段拼起来，检查整体是否已经是递增的。  

如果整体有序，说明只要在每段内部做适当的交换就能得到排序；  
否则，无论怎么在段内调换，段间的相对顺序都无法改变，排序就不可能。

> **核心概念：段（segment）**  
> 把它想象成一排相同颜色的球，颜色代表 popcount。  
> 同一种颜色的球可以随意换位置，但不同颜色的球之间的顺序永远固定。

#### 代码（Python）

```python
def popcount(x: int) -> int:
    """返回整数 x 的二进制中 1 的个数"""
    return bin(x).count('1')

def can_sort(nums):
    """
    判断是否可以通过「相邻且 popcount 相同」的交换把数组排成升序。
    思路：对每个 popcount 相同的连续段内部排序，然后检查整体是否有序。
    """
    n = len(nums)
    arr = nums[:]                     # 复制一份防止修改原数组

    i = 0
    while i < n:
        # 找到当前段的右边界（不包括右边界）
        j = i + 1
        while j < n and popcount(arr[j]) == popcount(arr[j - 1]):
            j += 1

        # [i, j) 是一个段，内部可以自由排序
        segment = arr[i:j]
        segment.sort()                # 对段内元素升序排列
        arr[i:j] = segment             # 写回原数组

        i = j                         # 开始处理下一个段

    # 检查整个数组是否已经有序
    for k in range(1, n):
        if arr[k - 1] > arr[k]:
            return False
    return True
```

> **关键行注释**  
> - `while j < n and popcount(arr[j]) == popcount(arr[j - 1])`：像在走路，遇到颜色相同的球就继续往前走，颜色不同时停下来。  
> - `segment.sort()`：段内相当于把同颜色的球随意摆放，让它们从小到大排好。  
> - 最后的 `for` 循环：检查所有球排好后，是否真的从左到右递增。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 逐段遍历是 `O(n)`。  
  - 对每段内部排序，最坏情况所有元素都在同一段，需要 `O(n log n)` 的排序时间。  
  - 相比暴力的指数级别，`n ≤ 100` 完全能在毫秒级完成。  

- **空间复杂度**：`O(n)`  
  - 需要额外的列表 `segment` 来存放当前段的元素，最多占用 `n` 个整数的空间。  
  - 若使用原地排序（如 `arr[i:j] = sorted(arr[i:j])`），额外空间甚至可以降到 `O(1)`（不计递归栈）。

> **与暴力解对比**：从“枚举所有可能”降到了“只排序每个固定段”，把指数级别压到了常见的 `n log n`，速度提升几百倍以上。

---

## 心得  

- **核心技巧**：**利用不可交换的属性把数组划分成固定段**，在段内部自由排序，段间顺序保持不变。  
- **适用场景**：  
  1. 只能在满足某种**相同属性**的相邻元素之间交换的题目（如相同奇偶性、相同余数等）。  
  2. 需要判断是否可以通过局部自由排列实现全局有序的题目。  
- **一句话总结**：**只要把“同类可乱序、不同类不可交叉”这两条规则转化为段划分，排序问题就迎刃而解。**

---

## 反思  

- **第一反应**：看到“相邻且 set bits 相同才能交换”，立刻想到**模拟交换**，于是想到 BFS。  
- **最容易踩的坑**：  
  * 忘记 **段是“连续”** 的概念，只根据 popcount 分组会误把不相邻的相同 popcount 元素放在同一段，导致错误判断。  
  * 需要注意 **边界条件**：数组长度为 1 时直接返回 `True`，以及所有元素 popcount 都不相同时每个段长度为 1，排序检查仍然要进行。  
- **下次遇到同类题**，第一步应该问自己：**“哪些元素之间可以互换？哪些不可以？”**  
  * 把“可交换”关系抽象成 **连通块 / 段**，先在块内部排序，再检查全局有序性。这样往往能在 O(n log n) 时间内得到答案。