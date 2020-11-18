# #1054. 相隔条形码 / Distant Barcodes

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting、Heap (Priority Queue)、Counting · [LeetCode 链接](https://leetcode.com/problems/distant-barcodes/)

---

## 题目（英文原版）

**Description**

In a warehouse, there is a row of barcodes, where the ith barcode is barcodes[i].
Rearrange the barcodes so that no two adjacent barcodes are equal. You may return any answer, and it is guaranteed an answer exists.

**Examples**

**Example 1:**

```
Input: barcodes = [1,1,1,2,2,2]
Output: [2,1,2,1,2,1]
```

**Example 2:**

```
Input: barcodes = [1,1,1,1,2,2,3,3]
Output: [1,3,1,3,1,2,1,2]
```

**Constraints**

- 1 <= barcodes.length <= 10000
- 1 <= barcodes[i] <= 10000

---

## 题目（中文翻译）

在一个仓库中，有一排条形码（barcode），其中第 *i* 个条形码为 `barcodes[i]`。请重新排列这些条形码，使得任意两个相邻的条形码不相等。你可以返回任意一种满足条件的排列，题目保证至少存在一种答案。

**示例 1**  
**输入**: `barcodes = [1,1,1,2,2,2]`  
**输出**: `[2,1,2,1,2,1]`

**示例 2**  
**输入**: `barcodes = [1,1,1,1,2,2,3,3]`  
**输出**: `[1,3,1,3,1,2,1,2]`

**约束条件**  
- `1 <= barcodes.length <= 10^4`  
- `1 <= barcodes[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有条形码逐个放到结果数组里，只要发现把当前条形码放到最后会和前一个相同，就把它换到别的地方。  
一种最笨的实现方式是：

1. **遍历所有排列**（全排列）或**不断尝试把元素插到不同位置**，只要出现相邻相同就回溯。  
2. 为了判断相邻是否相同，只需要看前一个元素的值。

这里用到的唯一数据结构是 **列表（list）**，它就像我们平时用的“纸条”，把条形码一个一个写上去。  
为什么这种办法能得到正确答案？因为只要遍历到所有可能的放置方式，必然会找到一个满足“相邻不相等”的排列（题目已经保证一定存在）。

不过，这种“穷举”会把**所有可能的排列**都尝遍，时间会爆炸。

#### 代码（Python）

```python
from typing import List

def rearrangeBarcodes_bruteforce(barcodes: List[int]) -> List[int]:
    n = len(barcodes)
    used = [False] * n               # 记录哪些下标已经被使用
    ans = [0] * n                     # 最终答案

    def backtrack(pos: int) -> bool:
        """尝试把第 pos 位填好，返回是否成功"""
        if pos == n:                  # 全部填完
            return True

        for i in range(n):
            if used[i]:
                continue
            # 如果不是第一个位置，且与左侧相同，就跳过
            if pos > 0 and barcodes[i] == ans[pos - 1]:
                continue

            # 选择当前条码
            used[i] = True
            ans[pos] = barcodes[i]

            # 继续填下一个位置
            if backtrack(pos + 1):
                return True

            # 回溯
            used[i] = False

        return False

    backtrack(0)
    return ans
```

> **注**：上述代码在最坏情况下会尝试 `n!`（阶乘）种排列，实际运行会非常慢，只适合 **n ≤ 8** 左右的调试用例。

#### 复杂度

- **时间复杂度**：`O(n!)` —— 这表示随着元素个数的增长，所需的时间会像“阶乘”一样疯狂增长。比如 `n=10` 时，10! = 3,628,800，已经不现实了。
- **空间复杂度**：`O(n)` —— 主要是递归栈和几个长度为 `n` 的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于不停地在所有剩余元素里寻找一个“不等于前一个”的元素**。如果我们每次都能**快速拿到出现次数最多的条码**，并且把它放到一个安全的位置，就能避免相邻相同的问题。

关键观察：

1. **出现次数最多的条码** 必须被 **尽可能均匀地分散**，否则必然会相邻。  
2. 当我们已经把出现次数最多的条码放在某些位置后，**第二多的条码** 可以填进剩余的空位。  
3. 这正好对应 **贪心**：每一步都选出**当前剩余次数最高的两种条码**，交替放置。

要实现“每次拿到出现次数最高的条码”，我们可以使用 **最大堆（priority queue）**。  
堆的工作方式类似“**抽奖箱**”：里面装满了条码的出现次数，次数大的条码会被“抢先抽出来”。  
在 Python 中，`heapq` 默认是最小堆，我们把次数取负数即可实现最大堆。

**算法步骤**

1. **统计每个条码出现的次数**（哈希表），类似查字典：`key` 是条码，`value` 是出现次数。  
2. 把所有 `(次数, 条码)` 放进最大堆。  
3. **循环取出堆顶两个元素**（次数最多和次多的条码），交替放进结果数组：  
   - 先把次数最多的条码放进去（如果它和上一个放进去的相同，则换成次多的）。  
   - 把它的次数减 1，若仍有剩余就放回堆中。  
   - 再处理次多的条码，同理。  
4. 当堆里只剩下一个元素时，直接把它的剩余次数全部放进去（此时一定不会与前一个相同，因为题目保证可行）。

这样每一步都只涉及**堆的插入/弹出**，时间是 `O(log k)`（k 为不同条码种类数），总体是 `O(n log k)`。

#### 代码（Python）

```python
import heapq
from collections import Counter
from typing import List

def rearrangeBarcodes(barcodes: List[int]) -> List[int]:
    # 1️⃣ 统计出现次数：类似查字典，key=条码，value=出现次数
    cnt = Counter(barcodes)          # Counter 本质是 dict

    # 2️⃣ 建最大堆（次数取负），堆顶就是出现次数最多的条码
    # heap 中的元素形如 (-次数, 条码)
    heap = [(-freq, num) for num, freq in cnt.items()]
    heapq.heapify(heap)              # O(k) 建堆，k 为不同条码的种类数

    res = []                         # 最终答案

    # 3️⃣ 贪心取出堆顶两个元素交替放置
    while len(heap) >= 2:
        # 取出现次数最多的两个条码
        freq1, num1 = heapq.heappop(heap)   # freq 为负数
        freq2, num2 = heapq.heappop(heap)

        # 交替放入结果列表
        res.append(num1)
        res.append(num2)

        # 计数减一（因为我们用了一个），仍有剩余则重新放回堆
        if freq1 + 1 < 0:               # 负数加一仍然小于0，说明还有剩余
            heapq.heappush(heap, (freq1 + 1, num1))
        if freq2 + 1 < 0:
            heapq.heappush(heap, (freq2 + 1, num2))

    # 4️⃣ 处理堆里剩下的最后一种条码（如果有的话）
    if heap:
        freq, num = heap[0]               # 只剩一个元素
        # freq 为负数，-freq 就是剩余次数
        res.extend([num] * (-freq))

    return res
```

> **关键注释**  
> - `Counter` 类似“统计员”，帮我们一次性算出每个条码出现了多少次。  
> - 堆里存的次数取负数是因为 `heapq` 只能取最小的，我们想要最大的，于是把“大”变成“小”。  
> - `freq + 1 < 0` 的判断等价于“还有剩余次数”。因为 `freq` 是负的，+1 实际上是 “次数减一”。  

#### 复杂度

- **时间复杂度**：`O(n log k)`  
  - `n` 是条码总数，`k` 是不同条码的种类数（`k ≤ n`）。  
  - 解释：每次弹出或推入堆都需要 `log k` 的时间，整个过程共进行 `n` 次（每个条码放一次），所以整体是 `n × log k`。这比暴力的 `n!` 快了天壤之别。  
- **空间复杂度**：`O(k)`  
  - 主要用于存放计数的哈希表和堆，最多只需要保存每种不同条码一次。即使 `k = n`（所有条码都不相同），也只用了线性空间。

---

## 心得

- **核心技巧**：**贪心 + 最大堆**（或优先队列）  
  把出现次数最多的元素先“抢出来”，交替放置，确保不会出现相邻相同。

- **适用的题型**  
  1. **重新排列字符使相邻不相同**（如 LeetCode 767 `Reorganize String`）。  
  2. **任务调度**（LeetCode 621 `Task Scheduler`），需要把高频任务分散。  
  3. **颜色填充**（如 “彩色条纹” 类似问题），也可以用相同思路。

- **一句话总结**：**每一步都把“剩余最多”的条码放出来，交替使用，堆帮你快速找出最多的那一个。**

---

## 反思

- **第一反应**：直接想遍历所有排列，或者一次遍历把相同的条码往后搬——这都是暴力思路。  
- **最容易踩的坑**  
  - 忘记处理**最后只剩一种条码**的情况，直接弹出会导致空堆错误。  
  - 计数时使用正数/负数混淆，导致次数更新错误。  
  - 结果数组的长度必须恰好等于原数组长度，别多放或少放。

- **下次遇到同类题**，第一步应该**先统计每个元素的出现次数**，然后**考虑用堆/排序把出现最多的先取出来**，再根据“相邻不相同”的约束设计交替放置的贪心策略。