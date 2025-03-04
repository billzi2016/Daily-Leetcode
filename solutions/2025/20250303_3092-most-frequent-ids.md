# #3092. 最常出现的 ID / Most Frequent IDs

> 难度：中等 · 标签：Array、Hash Table、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/most-frequent-ids/)

---

## 题目（英文原版）

**Description**

The problem involves tracking the frequency of IDs in a collection that changes over time. You have two integer arrays, nums and freq, of equal length n. Each element in nums represents an ID, and the corresponding element in freq indicates how many times that ID should be added to or removed from the collection at each step.
Return an array ans of length n, where ans[i] represents the count of the most frequent ID in the collection after the ith step. If the collection is empty at any step, ans[i] should be 0 for that step.

**Examples**

**Example 1:**

```
Input: nums = [2,3,2,1], freq = [3,2,-3,1]
Output: [3,3,2,2]
Explanation:
After step 0, we have 3 IDs with the value of 2. So ans[0] = 3 . After step 1, we have 3 IDs with the value of 2 and 2 IDs with the value of 3. So ans[1] = 3 . After step 2, we have 2 IDs with the value of 3. So ans[2] = 2 . After step 3, we have 2 IDs with the value of 3 and 1 ID with the value of 1. So ans[3] = 2 .
```

**Example 2:**

```
Input: nums = [5,5,3], freq = [2,-2,1]
Output: [2,0,1]
Explanation:
After step 0, we have 2 IDs with the value of 5. So ans[0] = 2 . After step 1, there are no IDs. So ans[1] = 0 . After step 2, we have 1 ID with the value of 3. So ans[2] = 1 .
```

**Constraints**

- 1 <= nums.length == freq.length <= 105
- 1 <= nums[i] <= 105
- -105 <= freq[i] <= 105
- freq[i] != 0
- The input is generated such that the occurrences of an ID will not be negative in any step.

---

## 题目（中文翻译）

**描述**  
本题涉及在随时间变化的集合中跟踪 ID 的出现频率。给定两个等长整数数组 `nums` 和 `freq`，长度均为 `n`。`nums` 中的每个元素表示一个 ID，`freq` 中对应位置的元素表示在每一步中该 ID 应该被加入或移除的次数（正数表示加入，负数表示移除）。

返回一个长度为 `n` 的数组 `ans`，其中 `ans[i]` 表示第 `i` 步之后集合中出现次数最多的 ID 的数量。如果在某一步集合为空，则 `ans[i]` 为 `0`。

**示例 1**  
输入: `nums = [2,3,2,1]`, `freq = [3,2,-3,1]`  
输出: `[3,3,2,2]`  
解释:  
- 第 0 步后，集合中有 3 个值为 `2` 的 ID，所以 `ans[0] = 3`。  
- 第 1 步后，集合中有 3 个值为 `2` 的 ID 和 2 个值为 `3` 的 ID，所以 `ans[1] = 3`。  
- 第 2 步后，集合中只剩下 2 个值为 `3` 的 ID，所以 `ans[2] = 2`。  
- 第 3 步后，集合中有 2 个值为 `3` 的 ID 和 1 个值为 `1` 的 ID，所以 `ans[3] = 2`。

**示例 2**  
输入: `nums = [5,5,3]`, `freq = [2,-2,1]`  
输出: `[2,0,1]`  
解释:  
- 第 0 步后，集合中有 2 个值为 `5` 的 ID，所以 `ans[0] = 2`。  
- 第 1 步后，集合为空，所以 `ans[1] = 0`。  
- 第 2 步后，集合中有 1 个值为 `3` 的 ID，所以 `ans[2] = 1`。

**约束条件**  
- `1 <= nums.length == freq.length <= 10^5`  
- `1 <= nums[i] <= 10^5`  
- `-10^5 <= freq[i] <= 10^5`  
- `freq[i] != 0`  
- 输入保证在任何一步中某个 ID 的出现次数不会为负。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步一步模拟**题目描述的过程：

1. 用一个字典 `cnt` 记录每个 ID 当前在集合里出现的次数。  
   - 这就像我们在生活中记笔记：把「ID」当作「单词」，出现的次数当作「页码」——查找、增加或减少都很直观。  
2. 每处理完一步（即遍历到 `i`），把 `cnt` 里所有 ID 的出现次数全部找出来，取最大值，就是 `ans[i]`。  
3. 重复上述过程直至遍历完整个数组。

这种做法一定能得到正确答案，因为我们**完全按照题目要求**去更新集合并统计最大频次。

#### 代码（Python）

```python
from typing import List

def most_frequent_ids_bruteforce(nums: List[int], freq: List[int]) -> List[int]:
    n = len(nums)
    cnt = {}               # 记录每个 ID 当前的出现次数
    ans = [0] * n

    for i in range(n):
        id_ = nums[i]
        delta = freq[i]    # 本步要增加（正）或减少（负）的次数

        # 更新该 ID 的出现次数
        cnt[id_] = cnt.get(id_, 0) + delta
        if cnt[id_] == 0:          # 出现次数变成 0，删除键，保持字典干净
            del cnt[id_]

        # 暴力扫描得到当前最大的出现次数
        if cnt:                     # 集合非空时才有最大值
            max_freq = max(cnt.values())
            ans[i] = max_freq
        else:                       # 集合为空，答案为 0
            ans[i] = 0

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 对每一步（共 `n` 步）我们都要遍历一次 `cnt`（最坏情况下有 `O(n)` 个不同的 ID），所以总共是 `n × n`。  
  - 用大白话说，就是“如果有 10,000 步，每步都要看 10,000 次，那就要 100,000,000 次操作”，在 10⁵ 规模下会超时。

- **空间复杂度**：`O(n)`  
  - 最坏情况下每个 ID 都不同，需要在字典里保存 `n` 条记录。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每一步都要遍历所有 ID 去找最大频次。我们只需要在 **常数时间**（或均摊 O(1)）内得到当前最大的出现次数即可。

**关键观察**：

- 只会对单个 ID 的出现次数进行增减，不会一次性改变很多 ID。  
- 只关心“**有多少个 ID 的出现次数是 x**”。如果我们知道每个出现次数对应的 ID 数量，就能快速判断最大出现次数是否仍然有效。

因此我们维护两套数据结构：

| 数据结构 | 含义 | 类比 |
|---|---|---|
| `cnt[id]` | ID `id` 当前的出现次数 | “字典查词典”，key 是词（ID），value 是页码（出现次数） |
| `freq_of_cnt[f]` | 出现次数恰好为 `f` 的 ID 有多少个 | “频率的频率”，相当于把“多少个词在第 f 页”记下来 |

另外再保留一个变量 `max_freq`，始终保存 **当前集合里最大的出现次数**。每一步的更新规则如下：

1. **读取旧的出现次数** `old = cnt.get(id, 0)`。  
2. **计算新的出现次数** `new = old + delta`（`delta` 可能是正数或负数）。  
3. **更新 `cnt`**：`cnt[id] = new`（若 `new == 0` 则删掉该键）。  
4. **同步 `freq_of_cnt`**  
   - `freq_of_cnt[old] -= 1`（若 `old > 0`）  
   - `freq_of_cnt[new] += 1`（若 `new > 0`）  
5. **维护 `max_freq`**  
   - 若 `new > max_freq` → `max_freq = new`（出现了更大的频次）。  
   - 否则如果 `old == max_freq` 且 `freq_of_cnt[old] == 0`，说明之前的最大频次已经没有任何 ID 拥有了，需要把 `max_freq` 向下搜寻，直到找到一个 `freq_of_cnt[max_freq] > 0` 或者降到 `0`（集合为空）。  

这样每一步的所有操作都是 **O(1)**（字典的增删改查在均摊意义下是常数时间），因此总时间是 `O(n)`。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def most_frequent_ids(nums: List[int], freq: List[int]) -> List[int]:
    """
    最优解：使用两层哈希表 + 一个维护当前最大频次的变量
    """
    n = len(nums)
    cnt = defaultdict(int)            # id -> 当前出现次数
    freq_of_cnt = defaultdict(int)    # 出现次数 -> 拥有该次数的 id 数量
    max_freq = 0                       # 当前集合的最大出现次数
    ans = [0] * n

    for i in range(n):
        id_ = nums[i]
        delta = freq[i]

        old = cnt[id_]                 # 之前的出现次数（可能是 0）
        new = old + delta              # 更新后的出现次数

        # 1) 更新 cnt
        cnt[id_] = new
        if new == 0:                   # 出现次数变成 0，删掉键保持整洁
            del cnt[id_]

        # 2) 同步 freq_of_cnt
        if old > 0:                    # 旧的次数如果大于 0，才在 freq_of_cnt 中有记录
            freq_of_cnt[old] -= 1
            if freq_of_cnt[old] == 0:
                del freq_of_cnt[old]

        if new > 0:                    # 新的次数如果大于 0，加入记录
            freq_of_cnt[new] += 1

        # 3) 维护 max_freq
        if new > max_freq:
            max_freq = new
        else:
            # 如果原来的 max_freq 被删光了，需要向下寻找新的 max
            while max_freq > 0 and freq_of_cnt.get(max_freq, 0) == 0:
                max_freq -= 1

        ans[i] = max_freq               # 当前步骤的答案

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每一步只做常数次字典操作和一次（最坏情况下）向下搜索 `max_freq`。  
  - `max_freq` 只会整体下降最多 `n` 次（因为总出现次数的上限是所有正 `freq[i]` 的和），所以整体仍是线性时间。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **指数级**（比如 10⁵ 步时只需要几百毫秒）。

- **空间复杂度**：`O(m)`，`m` 为不同 ID 的数量（`≤ n`）。  
  - 需要存 `cnt`（每个 ID 一条）和 `freq_of_cnt`（每种出现次数一条），在最坏情况下也是 `O(n)`。  

---

## 心得

- **核心技巧**：用「出现次数的出现次数」来间接维护最大频次。相当于把「最大」这个查询转化为「有没有人拥有这个值」的检查，从而实现 O(1) 更新。  
- **适用场景**：  
  1. **All O`1` Data Structure**（LeetCode 432）——同样要求 O(1) 插入、删除、获取最大/最小键。  
  2. **Frequency Stack**（LeetCode 895）——需要快速得到出现次数最多的元素。  
  3. **Sliding Window Maximum Frequency**——窗口内维护最高出现次数时也可以使用类似思路。  
- **一句话总结**：**把「最大值」拆成「是否还有人拥有这个值」来维护，就能在常数时间内实时得到答案。**

---

## 反思

- **第一反应**：直接用字典记录每个 ID 的次数，然后每步遍历一次找最大。  
- **最容易踩的坑**  
  - **负数更新**：`freq[i]` 可能为负，需要确保不会让某个 ID 的出现次数变成负数（题目已保证不会）。  
  - **删除键**：当出现次数变为 0 时要把对应的键从字典中删掉，否则 `max(cnt.values())` 会错误地把 0 当成最大值。  
  - **max_freq 的下滑**：如果当前最大频次的拥有者全部被删除，需要向下循环寻找新的最大频次，忘记这一步会导致答案卡在已不存在的频次上。  
- **下次遇到同类题**：第一步先思考「我需要的查询是什么？」——如果是「最大/最小」且数据只会**局部增减**，就尝试使用「计数的计数」或「双向链表+哈希」等 O(1) 结构来维护。这样可以把原本的线性扫描变成常数时间。