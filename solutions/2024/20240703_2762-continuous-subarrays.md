# #2762. 连续子数组 / Continuous Subarrays

> 难度：中等 · 标签：Array、Queue、Sliding Window、Heap (Priority Queue)、Ordered Set、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/continuous-subarrays/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. A subarray of nums is called continuous if:
Return the total number of continuous subarrays.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [5,4,2,4]
Output: 8
Explanation: 
Continuous subarray of size 1: [5], [4], [2], [4].
Continuous subarray of size 2: [5,4], [4,2], [2,4].
Continuous subarray of size 3: [4,2,4].
There are no subarrys of size 4.
Total continuous subarrays = 4 + 3 + 1 = 8.
It can be shown that there are no more continuous subarrays.
```

**Example 2:**

```
Input: nums = [1,2,3]
Output: 6
Explanation: 
Continuous subarray of size 1: [1], [2], [3].
Continuous subarray of size 2: [1,2], [2,3].
Continuous subarray of size 3: [1,2,3].
Total continuous subarrays = 3 + 2 + 1 = 6.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`。若子数组（subarray）满足以下条件，则称其为 **连续**（continuous）子数组：

- 子数组中的最大值与最小值之差等于子数组长度减一，即 `max - min = length - 1`。

返回连续子数组的总数。

> **子数组** 是数组中一个连续的、非空的元素序列。

---

## 示例

### 示例 1

**输入**  
`nums = [5,4,2,4]`

**输出**  
`8`

**解释**  
连续子数组按长度划分如下：

- 长度为 1 的连续子数组: `[5]`, `[4]`, `[2]`, `[4]`。  
- 长度为 2 的连续子数组: `[5,4]`, `[4,2]`, `[2,4]`。  
- 长度为 3 的连续子数组: `[4,2,4]`。  

不存在长度为 4 的连续子数组。  
总连续子数组数 = `4 + 3 + 1 = 8`。可以证明不存在其他连续子数组。

### 示例 2

**输入**  
`nums = [1,2,3]`

**输出**  
`6`

**解释**  
连续子数组按长度划分如下：

- 长度为 1 的连续子数组: `[1]`, `[2]`, `[3]`。  
- 长度为 2 的连续子数组: `[1,2]`, `[2,3]`。  
- 长度为 3 的连续子数组: `[1,2,3]`。  

总连续子数组数 = `3 + 2 + 1 = 6`。

---

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把所有可能的子数组枚举出来，逐个检查它们是否满足 “连续” 的定义。  
这里的“连续”指的是 **子数组中的最大值和最小值之差不超过 2**（`max - min ≤ 2`）。  

- **枚举子数组**：我们可以固定左端点 `i`，然后让右端点 `j` 从 `i` 向右移动，形成子数组 `nums[i:j+1]`。  
- **检查条件**：遍历子数组内部，找出最大值 `mx` 与最小值 `mn`，判断 `mx - mn ≤ 2` 是否成立。  

> **类比**：把数组想成一本书的章节，左端点是书的起始页，右端点是结束页。我们把每一段章节都读一遍，记录这段章节里最高的字数和最少的字数，只要它们相差不超过 2，就算这段章节是“连续的”。

- **为什么一定对**：因为我们穷举了所有可能的 `[i, j]`，只要满足条件就计数，漏掉的情况不存在。  

- **时间/空间复杂度**：  
  - 对每一对 `(i, j)` 都要遍历子数组内部找最大最小，最坏情况下会是 `O(n)` 的扫描。  
  - 一共有 `O(n²)` 对左右端点，所以总时间是 `O(n³)`（实际实现时可以在内部遍历时同步更新最大最小，时间会降到 `O(n²)`）。  
  - 只使用了常数级别的额外空间 `O(1)`。

#### 代码（Python）

```python
def count_continuous_subarrays_bruteforce(nums):
    n = len(nums)
    ans = 0
    # i 为子数组左端点
    for i in range(n):
        cur_max = cur_min = nums[i]      # 当前子数组的最大值、最小值
        # j 为子数组右端点，向右扩展
        for j in range(i, n):
            # 同步更新最大最小值（只需要 O(1)）
            cur_max = max(cur_max, nums[j])
            cur_min = min(cur_min, nums[j])
            # 判断是否满足连续的条件
            if cur_max - cur_min <= 2:
                ans += 1
            else:
                # 已经不满足，继续往右扩展只会让范围更大，必然仍不满足
                # 可以提前结束内部循环，稍微优化一点
                break
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历左端点 `i`，内层最多向右扫描到数组末尾。每次移动右端点只做常数次比较更新最大最小，所以整体是二次遍历。  
  - 大白话：如果数组有 10,000 个元素，最多要检查约 `10,000 × 10,000 / 2 ≈ 5×10⁷` 次，这在实际运行中会很慢。

- **空间复杂度**：`O(1)`  
  - 只用了几个变量来保存当前的最大、最小值和计数器，和数组大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要重新遍历子数组来找最大最小**。  
其实我们只需要在 **滑动窗口** 中维护当前窗口的最大值和最小值，随窗口的左、右边界移动，能够 **在 O(1) 时间** 内得到最新的 `max` 与 `min`。  

实现思路如下：

1. **使用双端队列（Monotonic Queue）**  
   - `max_q`：单调递减队列，队首始终是当前窗口的最大值。  
   - `min_q`：单调递增队列，队首始终是当前窗口的最小值。  
   - 当右指针 `right` 向右扩张时，把 `nums[right]` 插入两个队列，同时弹出队尾不再保持单调性的元素。  
2. **窗口合法性判定**  
   - 只要 `max_q[0] - min_q[0] > 2`，说明窗口已经不满足 “连续” 条件，需要把左指针 `left` 向右收缩，直到差值 ≤ 2 为止。收缩时如果左端点正好等于队首元素，就把它弹出。  
3. **计数**  
   - 每次右指针移动到位置 `right`，窗口 `[left, right]` 已经是满足条件的最长窗口。以 `right` 为右端点的所有合法子数组的左端点只能是 `left, left+1, …, right`，共有 `right - left + 1` 个。把这个数累加到答案中即可。  

> **类比**：把数组看成一条河，左指针和右指针是两只船。我们让右船不停前进，同时用两根尺子（单调队列）实时记录船之间最高的水位和最低的水位。当水位差超过 2 时，左船就得往前划，直到水位差恢复到安全范围。每一次右船停下来，都能直接算出从左船到右船之间有多少段安全的河段（即连续子数组）。

#### 代码（Python）

```python
from collections import deque

def count_continuous_subarrays(nums):
    """
    使用滑动窗口 + 单调队列统计满足 max - min <= 2 的子数组个数
    """
    max_q = deque()   # 递减队列，保存候选的最大值
    min_q = deque()   # 递增队列，保存候选的最小值
    left = 0
    ans = 0

    for right, x in enumerate(nums):
        # ----- 维护 max_q -----
        while max_q and max_q[-1] < x:      # 弹出比 x 小的，保持递减
            max_q.pop()
        max_q.append(x)

        # ----- 维护 min_q -----
        while min_q and min_q[-1] > x:      # 弹出比 x 大的，保持递增
            min_q.pop()
        min_q.append(x)

        # ----- 收缩窗口，直到 max - min <= 2 -----
        while max_q[0] - min_q[0] > 2:
            # 如果左端点正好是队首，需要把它弹出
            if nums[left] == max_q[0]:
                max_q.popleft()
            if nums[left] == min_q[0]:
                min_q.popleft()
            left += 1                     # 左指针右移，窗口变小

        # 此时窗口 [left, right] 合法，所有以 right 为结尾的子数组数目为 (right-left+1)
        ans += right - left + 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个元素最多进入两次队列（一次加入，一次弹出），所以整体操作是线性的。  
  - 大白话：如果数组有 100,000 个元素，算法只会走大约 200,000 步，瞬间就能得到答案。

- **空间复杂度**：`O(k)`（这里的 `k` 为窗口大小的上限，最坏情况下是 `O(n)`）  
  - 需要两个双端队列来保存窗口内的最大、最小候选值。  
  - 实际上队列中元素的数量不会超过窗口长度，最坏是整个数组全部在窗口里时占 `O(n)` 空间。

---

## 心得

- **核心技巧**：**滑动窗口 + 单调队列**（也叫 **Monotonic Queue**）用来在 O(1) 时间获取窗口的最大值和最小值。  
- **适用题型**  
  1. “子数组最大值/最小值 ≤ K” 之类的区间约束（如 LeetCode 2398、2399）。  
  2. “滑动窗口最大值/最小值” 经典题目（LeetCode 239）。  
  3. “子数组满足某种单调性或范围限制” 的计数问题（如 “子数组中最大最小差不超过 K”）。
- **一句话总结**：  
  *“把窗口的极值实时维护起来，窗口非法就收缩，合法就直接计数”。*

---

## 反思

- **第一反应**：看到“最大值和最小值之差 ≤ 2”，立刻想到滑动窗口配合维护极值的结构，而不是直接枚举。  
- **最容易踩的坑**  
  1. **忘记在收缩窗口时同步弹出队首**，导致队列中残留已经离开窗口的元素，进而产生错误的极值。  
  2. **边界条件**：窗口收缩到只剩一个元素时仍需检查 `max_q[0] - min_q[0]`，否则会出现空队列访问错误。  
  3. **计数公式**：答案是 `right - left + 1`（以当前右端点为结尾的合法子数组个数），容易误写成 `right - left`。  
- **下次思路**：  
  1. **先写出窗口合法性的判定**（`max - min ≤ 2`）。  
  2. **挑选合适的数据结构**：单调队列 → O(1) 取极值。  
  3. **在循环里同步移动左指针，确保队列始终只保存窗口内元素**。这样就能一步到位得到答案。