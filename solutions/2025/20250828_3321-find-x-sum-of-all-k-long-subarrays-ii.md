# #3321. 求所有长度为 K 的子数组的 X‑和 II / Find X-Sum of All K-Long Subarrays II

> 难度：困难 · 标签：Array、Hash Table、Sliding Window、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-ii/)

---

## 题目（英文原版）

**Description**

You are given an array nums of n integers and two integers k and x.
The x-sum of an array is calculated by the following procedure:
Note that if an array has less than x distinct elements, its x-sum is the sum of the array.
Return an integer array answer of length n - k + 1 where answer[i] is the x-sum of the subarray nums[i..i + k - 1].

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,2,3,4,2,3], k = 6, x = 2
Output: [6,10,12]
Explanation:
```

**Example 2:**

```
Input: nums = [3,8,7,8,7,5], k = 2, x = 2
Output: [11,15,15,15,12]
Explanation:
Since k == x , answer[i] is equal to the sum of the subarray nums[i..i + k - 1] .
```

**Constraints**

- nums.length == n
- 1 <= n <= 105
- 1 <= nums[i] <= 109
- 1 <= x <= k <= nums.length

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，以及两个整数 `k` 和 `x`。  
数组的 **x‑和** 按如下步骤计算：

1. 取数组中所有不同的元素（distinct elements），并按升序排列。  
2. 若不同元素的数量 **小于** `x`，则 x‑和 等于数组中所有元素的总和（包括重复的元素）。  
3. 否则，取排好序的前 `x` 个不同元素，将这 `x` 个元素的值相加，即得到 x‑和。

返回一个长度为 `n - k + 1` 的整数数组 `answer`，其中 `answer[i]` 为子数组 `nums[i .. i + k - 1]` 的 x‑和。

---

**示例 1**

> **输入**  
> `nums = [1,1,2,2,3,4,2,3], k = 6, x = 2`  
> **输出**  
> `[6,10,12]`  
> **解释**  
> - 子数组 `[1,1,2,2,3,4]` 的不同元素为 `{1,2,3,4}`，取最小的 2 个 distinct 元素 `1` 与 `2`，其和为 `1 + 2 = 3`。由于不同元素不少于 `x`，再加上窗口中其余元素的值（重复的 `1`、`2`、`3`、`4`）得到最终的 x‑和 `6`。  
> - 其余窗口同理计算得到 `10` 与 `12`。

**示例 2**

> **输入**  
> `nums = [3,8,7,8,7,5], k = 2, x = 2`  
> **输出**  
> `[11,15,15,15,12]`  
> **解释**  
> 当 `k == x` 时，窗口中的不同元素恰好等于 `k`，因此 x‑和 等价于窗口所有元素的和。  

---

**约束条件**

- `nums.length == n`
- `1 ≤ n ≤ 10^5`
- `1 ≤ nums[i] ≤ 10^9`
- `1 ≤ x ≤ k ≤ nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是把每一个长度为 `k` 的子数组都单独拿出来，统计它里面每个不同数字出现了多少次，然后挑出出现次数最多的 `x` 个不同数字（出现次数相同的情况下取**数字更大的**），把这些数字出现的所有次数对应的值相加，得到该子数组的 **x‑sum**。  

这里涉及到的主要数据结构只有 **哈希表**（`dict`），它的作用可以类比成一本词典：  
- **key**（词）是子数组里出现的数字  
- **value**（页码）是这个数字出现的次数  

因为每个子数组都要重新统计一次频率，时间上会非常慢——相当于我们每次都重新打开一本新词典去查。

**正确性**：  
- 统计完整的频率信息后，挑出出现次数最多的 `x` 种数字（并在出现次数相同的情况下挑更大的数字），正好符合题目对 “x‑sum” 的定义。  
- 把这 `x` 种数字对应的所有出现值相加，就得到答案。

**复杂度**：  
- **时间**：对每一个窗口都要遍历 `k` 个元素并统计频率，窗口的个数是 `n‑k+1`，所以总时间是 `O((n‑k+1)·k) ≈ O(n·k)`。如果 `k` 接近 `n`，最坏会是 `O(n²)`，这在 `n ≤ 10⁵` 时根本跑不完。  
- **空间**：每个窗口最多有 `k` 个不同数字，需要一个哈希表保存频率，空间是 `O(k)`，最坏 `O(n)`。

---

#### 代码（Python）

```python
from collections import Counter
from typing import List

def x_sum_bruteforce(nums: List[int], k: int, x: int) -> List[int]:
    n = len(nums)
    ans = []
    for i in range(n - k + 1):
        window = nums[i:i + k]                     # 取出长度为 k 的子数组
        cnt = Counter(window)                     # 统计每个数字出现的次数
        # 把 (freq, value) 按 freq 降序、value 降序 排序
        # 注意：freq 越大越靠前，freq 相同则 value 越大越靠前
        sorted_items = sorted(cnt.items(),
                              key=lambda kv: (kv[1], kv[0]),
                              reverse=True)
        # 取前 x 种不同数字（如果种类不足则全部取）
        top_x = sorted_items[:x]
        # 把这些数字出现的所有值相加：value * freq
        cur_sum = sum(val * freq for val, freq in top_x)
        ans.append(cur_sum)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·k)`（最坏 `O(n²)`），因为对每个窗口都要遍历 `k` 次。  
- **空间复杂度**：`O(k)`（哈希表存放窗口内的频率），最坏 `O(n)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次窗口滑动都要重新统计全部频率。  
其实相邻两个窗口只差一个元素——左边的元素离开，右边的元素加入。我们只需要 **增量地** 更新频率即可，这正是 **滑动窗口** 的核心思想。

但是仅仅维护频率还不够：我们还要随时知道当前窗口里 **出现次数最多的前 x 种不同数字**（出现次数相同要取更大的数字）。这需要一种能够 **快速取最小/最大**、**快速插入/删除** 的有序结构。  

思路步骤如下：

1. **维护一个全局的哈希表 `freq`**，记录每个数字在当前窗口中的出现次数。  
   - 类比词典：键是数字，值是它在窗口里出现的次数。

2. **把所有不同数字分成两组**  
   - **big**：容量最多为 `x`，保存「当前窗口里出现次数最多的前 x 种数字」。我们需要随时能够得到这组里 **出现次数最少的那一个**（因为当有更“抢手”的数字进来时，需要把最弱的踢出去），所以 **big 用最小堆**（`freq` 升序、`value` 升序）来维护。  
   - **small**：保存其余的数字，用 **最大堆**（`freq` 降序、`value` 降序）来维护，这样可以快速拿到 **出现次数最多的那一个**（准备升到 big 里）。

   堆的作用可以类比成 **排队的队列**：  
   - **big** 是“VIP 队列”，只容纳最抢手的 `x` 个人，最不抢手的站在前面，随时准备被替换。  
   - **small** 是“普通队列”，最抢手的站在前面，随时准备晋升为 VIP。

3. **维护一个变量 `sum_big`**，记录 `big` 里所有数字对应的 **value × freq** 的总和。答案正是这个值。

4. **窗口滑动时的更新**  
   - **加入新数字 `v`**：  
     - `freq[v] += 1`（如果之前不存在就当作 0）。  
     - 把 `(freq[v], v)` 这条记录加入 **big**（先假设它是 VIP），随后在 `balance()` 中根据堆的大小和顺序把多余的或不够“抢手”的元素搬到 **small**。  
   - **移除旧数字 `u`**（窗口左端即将离开）：  
     - `freq[u] -= 1`，如果减到 0 则在哈希表里删除。  
     - 把更新后的 `(freq[u], u)` 再次压入对应的堆（这里不必立即从堆里删掉旧的旧记录，只要在弹出堆顶时检查它是否已经是“过期的”，这叫 **懒删**）。  
   - **平衡（balance）**：  
     - 确保 `big` 的大小恰好是 `min(x, distinct_cnt)`（`distinct_cnt` 是当前窗口里不同数字的种类数）。  
     - 如果 `big` 里有元素 **不够抢手**（即比 `small` 堆顶的元素更弱），就把 `big` 堆顶弹出，放进 `small`；反之如果 `small` 堆顶比 `big` 最弱的更抢手，就把它弹出放进 `big`。  
     - 每一次搬迁都要同步更新 `sum_big`（加上进入 `big` 的 `value*freq`，减去离开的）。

5. **懒删（lazy deletion）**  
   - 堆里可能会残留已经“过期”的记录（因为我们只在频率变化时压入新记录，旧的记录没有立即删除）。弹出堆顶时，检查 `freq` 中对应的频率是否和堆里保存的一致，不一致则说明是旧记录，直接丢弃，继续弹出下一个。这样可以在 `O(log n)` 内保持堆的正确性，而不需要实现支持删除的平衡树。

6. **每一步窗口结束后**，`sum_big` 就是当前窗口的 **x‑sum**，把它加入答案数组。

**核心算法**：滑动窗口 + 两个堆（最小堆 + 最大堆） + 哈希表 + 懒删。  
整个过程每次窗口滑动只做 `O(log n)` 的堆操作，整体 `O(n log n)`，可以轻松应对 `n = 10⁵`。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

def x_sum(nums: List[int], k: int, x: int) -> List[int]:
    """
    返回长度为 n-k+1 的数组 ans，其中 ans[i] 为子数组 nums[i..i+k-1] 的 x‑sum
    """
    n = len(nums)
    # 记录每个数字在当前窗口的出现次数
    freq = defaultdict(int)

    # min‑heap 保存 big（最多 x 个最抢手的元素）
    # 堆中存 (freq, value)   -> freq 越小越在堆顶（因为是最小堆）
    big = []
    # max‑heap 保存 small
    # 为了用 Python 的 min‑heap 实现 max‑heap，取负数
    # 堆中存 (-freq, -value)   -> freq 越大、value 越大越在堆顶
    small = []

    # 当前 big 中所有 (value * freq) 的和
    sum_big = 0
    # 记录答案
    ans = []

    def clean_heap(heap, sign):
        """
        移除堆顶的“过期”记录。
        sign = 1  表示 min‑heap (big)   (freq, val)
        sign = -1 表示 max‑heap (small) (-freq, -val)
        """
        while heap:
            f, v = heap[0]
            # 还原真实的 freq、value
            real_f = f if sign == 1 else -f
            real_v = v if sign == 1 else -v
            # 若哈希表中已经没有该数字，或者频率不匹配，则是旧记录
            if freq.get(real_v, 0) != real_f:
                heapq.heappop(heap)          # 丢掉旧记录
            else:
                break                         # 堆顶是最新的
        # 返回堆顶的真实 (freq, value) 或 None
        if not heap:
            return None
        f, v = heap[0]
        return (f if sign == 1 else -f,
                v if sign == 1 else -v)

    def add_to_big(f, v):
        """把 (f,v) 加入 big，并更新 sum_big"""
        nonlocal sum_big
        heapq.heappush(big, (f, v))
        sum_big += f * v

    def add_to_small(f, v):
        """把 (f,v) 加入 small（使用负数实现 max‑heap）"""
        heapq.heappush(small, (-f, -v))

    def balance():
        """
        保证：
        1) big 的大小 = min(x, distinct_cnt)
        2) big 中的每个元素都“至少和 small 堆顶一样抢手”
        """
        nonlocal sum_big

        # 1) 先把堆顶的过期元素清理干净
        clean_heap(big, 1)
        clean_heap(small, -1)

        # 计算当前不同数字的种类数
        distinct = len(freq)

        # 2) 调整 big 的容量
        while len(big) > min(x, distinct):
            # 把最弱的弹到 small
            f, v = heapq.heappop(big)
            sum_big -= f * v
            add_to_small(f, v)
            clean_heap(big, 1)       # 可能弹出后又有旧记录，顺手清理

        while len(big) < min(x, distinct):
            # 从 small 里挑最抢手的放进 big
            top = clean_heap(small, -1)
            if top is None:   # small 为空，说明 distinct 已经等于 big 的容量
                break
            f, v = top
            heapq.heappop(small)   # 真正弹出
            add_to_big(f, v)

        # 3) 维持顺序：big 中最弱的不能比 small 中最抢手的弱
        while True:
            top_big = clean_heap(big, 1)
            top_small = clean_heap(small, -1)
            if top_big is None or top_small is None:
                break
            f_big, v_big = top_big
            f_small, v_small = top_small
            # 判断顺序：如果 small 的 (freq, value) 更抢手，则交换
            if (f_small > f_big) or (f_small == f_big and v_small > v_big):
                # 交换两堆的堆顶
                heapq.heappop(big)
                heapq.heappop(small)
                sum_big -= f_big * v_big          # big 弹出
                sum_big += f_small * v_small      # small 晋升
                add_to_big(f_small, v_small)
                add_to_small(f_big, v_big)
            else:
                break

    # ------------------- 初始化窗口 -------------------
    for i in range(k):
        v = nums[i]
        freq[v] += 1
    # 把所有不同数字先放进 big（随后 balance 会把多余的搬走）
    for v, f in freq.items():
        add_to_big(f, v)
    balance()
    ans.append(sum_big)

    # ------------------- 窗口滑动 -------------------
    for i in range(k, n):
        # 新进来的元素
        add = nums[i]
        freq[add] += 1
        add_to_big(freq[add], add)   # 先放进 big，后面 balance 会纠正

        # 要离开的元素
        remove = nums[i - k]
        freq[remove] -= 1
        if freq[remove] == 0:
            del freq[remove]         # 完全消失，后面的 clean 会把旧记录剔除
        else:
            # 仍然存在，放入对应的堆（这里随意放，balance 会处理）
            add_to_big(freq[remove], remove)

        # 重新平衡两堆，使 big 正好是前 x 名
        balance()
        ans.append(sum_big)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 每次窗口滑动只会对两个堆执行 `push / pop`（`log` 级别）以及若干次“懒删”检查（同样是 `log`）。  
  - 与 `n` 成线性关系，远快于暴力的 `O(n·k)`。

- **空间复杂度**：`O(m)`，其中 `m` 是窗口内不同数字的种类数，最坏 `O(n)`（所有元素都不相同）。  
  - 主要存放哈希表 `freq`、两个堆以及少量额外变量。

---

## 心得

- **核心技巧**：滑动窗口 + “双堆 + 懒删” 维护 **前 x 大频率（并在频率相同的情况下取更大数值）**。  
- **适用的题型**  
  1. “前 K 大/小元素” 类的动态窗口问题（如 “滑动窗口的中位数”）。  
  2. “维护 top‑k 频率/权重” 的流式统计（如 “数据流中的第 K 大元素”）。  
  3. 需要在窗口内实时查询 **排序后的前几名**（如 “滑动窗口内的最大子序和” 的变形）。  

> **解题钥匙**：把「窗口内的全部信息」拆成「频率表」+「两堆分别保存前 x 与其余」，用堆的「最小/最大」特性快速调整。

---

## 反思

- **第一反应**：看到“x‑sum” 立刻想到「统计频率」并「挑出前 x」——于是想到暴力遍历。  
- **最容易踩的坑**  
  1. **频率相同的取值规则**：必须在比较时把 `value` 作为第二关键字，且在堆中采用升序/降序一致的方式，否则会选错元素。  
  2. **懒删不彻底**：忘记在 `balance` 前先把堆顶的过期记录清理干净，会导致堆大小不对或 `sum_big` 错误。  
  3. **窗口种类数少于 x**：`big` 的容量应为 `min(x, distinct_cnt)`，否则会在 `sum_big` 中加入不存在的元素。  

- **下次类似题的第一步**：先确定窗口内需要维护的「排序属性」是什么（频率、大小、和等），再选用「双堆」或「有序容器」来实时维护前 k（或后 k）个元素。这样就能把「每次重新统计」的 `O(k)` 降到 `O(log n)`。