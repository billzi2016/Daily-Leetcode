# #1460. 通过翻转子数组使两个数组相等 / Make Two Arrays Equal by Reversing Subarrays

> 难度：简单 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/make-two-arrays-equal-by-reversing-subarrays/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays of equal length target and arr. In one step, you can select any non-empty subarray of arr and reverse it. You are allowed to make any number of steps.
Return true if you can make arr equal to target or false otherwise.

**Examples**

**Example 1:**

```
Input: target = [1,2,3,4], arr = [2,4,1,3]
Output: true
Explanation: You can follow the next steps to convert arr to target:
1- Reverse subarray [2,4,1], arr becomes [1,4,2,3]
2- Reverse subarray [4,2], arr becomes [1,2,4,3]
3- Reverse subarray [4,3], arr becomes [1,2,3,4]
There are multiple ways to convert arr to target, this is not the only way to do so.
```

**Example 2:**

```
Input: target = [7], arr = [7]
Output: true
Explanation: arr is equal to target without any reverses.
```

**Example 3:**

```
Input: target = [3,7,9], arr = [3,7,11]
Output: false
Explanation: arr does not have value 9 and it can never be converted to target.
```

**Constraints**

- target.length == arr.length
- 1 <= target.length <= 1000
- 1 <= target[i] <= 1000
- 1 <= arr[i] <= 1000

---

## 题目（中文翻译）

给定两个等长的整数数组 `target` 和 `arr`。在一次操作中，你可以选择 `arr` 的任意非空子数组（subarray）并将其翻转。可以进行任意次数的操作。

如果能够通过上述操作使 `arr` 与 `target` 相等，返回 `true`；否则返回 `false`。

### 示例

#### 示例 1
**输入:** `target = [1,2,3,4]`, `arr = [2,4,1,3]`  
**输出:** `true`  
**解释:** 你可以按以下步骤将 `arr` 转换为 `target`：  
1. 翻转子数组 `[2,4,1]`，`arr` 变为 `[1,4,2,3]`  
2. 翻转子数组 `[4,2]`，`arr` 变为 `[1,2,4,3]`  
3. 翻转子数组 `[4,3]`，`arr` 变为 `[1,2,3,4]`  

还有多种方式可以将 `arr` 转换为 `target`，这并非唯一方法。

#### 示例 2
**输入:** `target = [7]`, `arr = [7]`  
**输出:** `true`  
**解释:** `arr` 与 `target` 本来就相等，无需进行任何翻转。

#### 示例 3
**输入:** `target = [3,7,9]`, `arr = [3,7,11]`  
**输出:** `false`  
**解释:** `arr` 中不存在值 `9`，因此不可能转换为 `target`。

### 约束条件
- `target.length == arr.length`
- `1 <= target.length <= 1000`
- `1 <= target[i] <= 1000`
- `1 <= arr[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的子数组翻转全部尝试一遍**，看能否得到 `target`。  
可以把这个过程想象成在玩拼图：每一次翻转就像把一块拼图翻过去，拼出不同的图案。  

实现上可以用**宽度优先搜索（BFS）**：

1. 把初始数组 `arr` 放进队列。  
2. 每次从队列里取出一个数组 `cur`，如果 `cur == target`，返回 `True`。  
3. 否则枚举 `cur` 中所有 **非空子数组** 的左、右端点 `(i, j)`，把 `cur[i:j+1]` 翻转得到新数组 `next`，如果 `next` 之前没见过，就加入队列。  
4. 队列空了仍未找到目标，说明不可达，返回 `False`。

> **为什么会对？**  
> 只要把所有可能的翻转都枚举出来，搜索过程就会遍历所有能够通过若干次翻转得到的数组。只要目标数组在这棵搜索树里，就一定能被发现。

> **时间/空间复杂度**  
> - 数组长度记作 `n`。子数组的数量是 `n·(n+1)/2`，每一次翻转都要复制并翻转子数组，**时间复杂度是指数级**（大约 `O(n! )`），因为不同的翻转序列会产生几乎所有排列。  
> - 为了防止重复访问，需要用哈希表保存已经出现过的数组，这会占用 **指数级的空间**。

> 用大白话说，`O(n!)` 就像把所有可能的排队顺序都列出来，哪怕 `n=10`，也要考虑 **3,628,800** 种情况，根本不可行。

#### 代码（Python）

```python
from collections import deque

def can_be_equal_bruteforce(target, arr):
    """暴力 BFS 版（仅作思路演示，实际会超时）"""
    n = len(arr)
    target_tuple = tuple(target)          # 目标转成不可变的 tuple，方便哈希比较
    start = tuple(arr)

    if start == target_tuple:
        return True

    q = deque([start])
    visited = {start}

    while q:
        cur = q.popleft()
        # 枚举所有子数组的左右端点
        for i in range(n):
            for j in range(i, n):
                # 翻转子数组 [i, j]，生成新数组
                nxt = list(cur)
                nxt[i:j+1] = reversed(nxt[i:j+1])
                nxt_t = tuple(nxt)
                if nxt_t == target_tuple:
                    return True
                if nxt_t not in visited:
                    visited.add(nxt_t)
                    q.append(nxt_t)
    return False
```

> **关键行解释**  
> - `nxt[i:j+1] = reversed(nxt[i:j+1])`：把子数组原地翻转。  
> - `visited`：记录已经遍历过的排列，防止无休止循环。

#### 复杂度

- **时间复杂度**：`O(n! )`（指数级）——因为搜索会遍历几乎所有可能的排列。  
- **空间复杂度**：`O(n! )`——需要存放已经访问的每一个排列。

> 这两项都远远超出题目给出的 `n ≤ 1000`，所以暴力解只能用来帮助我们理解问题本质，实际代码里绝不能使用。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有翻转序列**。  
我们需要问自己：**到底有哪些数组是可以通过若干次子数组翻转互相转换的？**  

> **关键观察**  
> 任意一次翻转都等价于把一段连续的元素顺序倒置。  
> 如果我们把翻转的长度限制为 **2**（即只翻转相邻的两个元素），这正是一次 **交换（swap）**。  
> 通过不断地交换相邻元素，我们可以实现 **任意排列**（这正是冒泡排序的原理）。  

> 因此，只要两个数组 **包含完全相同的元素且出现次数相同**，我们就一定能把其中一个变成另一个——顺序不重要，**多重集合（multiset）相等** 即可。

于是问题转化为：  
> “`target` 和 `arr` 的元素出现频率是否完全相同？”  

检查方式有两种：

1. **排序后逐位比较**：把两数组都排序，若排好序后相等，则原数组多重集合相同。  
2. **计数（桶）**：因为题目限制 `1 ≤ value ≤ 1000`，可以用长度 1001 的计数数组统计每个数出现次数，比较两计数数组是否相等。计数法是 **线性 O(n)**，但实现稍繁琐；排序法 `O(n log n)` 更直观，也足够快（`n ≤ 1000`）。

下面给出排序法的实现，并在注释中解释每一步。

#### 代码（Python）

```python
def can_be_equal(target, arr):
    """
    最优解：只要两数组的元素出现次数相同，就一定能通过若干次子数组翻转相互转换。
    实现思路：先对两数组排序，再逐位比较是否相等。
    时间复杂度 O(n log n)；空间复杂度 O(1)（原地排序或使用额外的临时列表）。
    """
    # 1. 对两数组进行排序
    target_sorted = sorted(target)   # sorted 会返回一个新列表，原数组保持不变
    arr_sorted    = sorted(arr)

    # 2. 逐位比较：如果每个位置的数字都相同，说明两数组的多重集合相等
    return target_sorted == arr_sorted
```

> **关键行解释**  
> - `sorted(target)`：把 `target` 里所有数字从小到大排好序，像把一堆散乱的书按字母顺序摆放。  
> - `target_sorted == arr_sorted`：直接比较两个排好序的列表是否完全相同。

如果想进一步利用题目给出的数值范围，可以改写为计数法：

```python
def can_be_equal_count(target, arr):
    MAX_VAL = 1000
    cnt = [0] * (MAX_VAL + 1)   # 计数桶，索引对应数值

    for x in target:
        cnt[x] += 1
    for x in arr:
        cnt[x] -= 1

    # 所有计数都应回到 0，才说明两数组出现次数相同
    return all(c == 0 for c in cnt)
```

#### 复杂度

- **时间复杂度**：`O(n log n)`（排序）  
  - 对于 `n = 1000`，`log n` 约等于 `10`，所以实际运算非常快。  
  - 与暴力解的指数级时间相比，简直是天壤之别。  
- **空间复杂度**：`O(1)`（如果使用原地排序 `list.sort()`，则不需要额外的存储）或 `O(n)`（`sorted` 返回新列表）。  

> 与暴力解相比，时间从“几乎遍历所有排列”降到了“把数字排个序”，空间也从“记录所有排列”降到了“几百个整数”。这就是算法优化的本质：**找出问题的核心属性，直接判断，而不是穷举所有可能**。

---

## 心得

- **核心技巧**：把“能否通过任意子数组翻转相互转换”抽象为“两个数组的多重集合是否相同”。  
- **适用场景**：  
  1. 只关心元素出现次数而不关心顺序的题目（如 **“两个数组是否为同构”**）。  
  2. 允许任意排列操作的题目（如 **“通过任意次数的相邻交换将数组排序”**）。  
  3. 需要判断两个字符串是否为 **anagram（字母异位词）** 的情形。  
- **一句话总结**：**只要元素集合相同，子数组翻转就能把任意排列变成目标排列**。

---

## 反思

- **第一反应**：看到“可以翻转任意子数组”，第一时间想到“这类似于可以随意交换相邻元素”，于是尝试 BFS 暴力搜索。  
- **最容易踩的坑**：  
  - 误以为只能翻转**连续**子数组会限制可达的排列，其实连续翻转两两相邻已经足够产生任意排列。  
  - 忽略了 **重复元素** 的情况：即使有相同数字，只要出现次数相同仍然可达。  
- **下次思路**：遇到“任意子序列/子数组/子串的操作”时，先问自己 **“这种操作能否实现任意置换？”**，如果答案是肯定的，就把问题转化为 **“元素出现次数是否相同”**，直接用排序或计数来判断。