# #1705. 最多能吃掉的苹果数 / Maximum Number of Eaten Apples

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-eaten-apples/)

---

## 题目（英文原版）

**Description**

There is a special kind of apple tree that grows apples every day for n days. On the ith day, the tree grows apples[i] apples that will rot after days[i] days, that is on day i + days[i] the apples will be rotten and cannot be eaten. On some days, the apple tree does not grow any apples, which are denoted by apples[i] == 0 and days[i] == 0.
You decided to eat at most one apple a day (to keep the doctors away). Note that you can keep eating after the first n days.
Given two integer arrays days and apples of length n, return the maximum number of apples you can eat.

**Examples**

**Example 1:**

```
Input: apples = [1,2,3,5,2], days = [3,2,1,4,2]
Output: 7
Explanation: You can eat 7 apples:
- On the first day, you eat an apple that grew on the first day.
- On the second day, you eat an apple that grew on the second day.
- On the third day, you eat an apple that grew on the second day. After this day, the apples that grew on the third day rot.
- On the fourth to the seventh days, you eat apples that grew on the fourth day.
```

**Example 2:**

```
Input: apples = [3,0,0,0,0,2], days = [3,0,0,0,0,2]
Output: 5
Explanation: You can eat 5 apples:
- On the first to the third day you eat apples that grew on the first day.
- Do nothing on the fouth and fifth days.
- On the sixth and seventh days you eat apples that grew on the sixth day.
```

**Constraints**

- n == apples.length == days.length
- 1 <= n <= 2 * 104
- 0 <= apples[i], days[i] <= 2 * 104
- days[i] = 0 if and only if apples[i] = 0.

---

## 题目（中文翻译）

**题目描述**  
有一种特殊的苹果树会在连续 **n** 天内每天结果。第 `i` 天，树会长出 `apples[i]` 个苹果，这些苹果会在 `days[i]` 天后腐烂，即在第 `i + days[i]` 天这些苹果会变质，无法再被吃掉。某些天树可能不结果，此时 `apples[i] == 0` 且 `days[i] == 0`。  
你决定每天最多吃掉 **一个** 苹果（保持身体健康）。注意，你可以在前 `n` 天结束后继续吃苹果。  
给定长度为 `n` 的整数数组 `apples` 与 `days`，返回你能吃掉的苹果的最大数量。

**示例 1**  
```
Input: apples = [1,2,3,5,2], days = [3,2,1,4,2]
Output: 7
Explanation: 你可以吃掉 7 个苹果：
- 第一天，吃掉第一天长出的苹果。
- 第二天，吃掉第二天长出的苹果。
- 第三天，吃掉第二天长出的另一个苹果。此时，第三天长出的苹果已腐烂。
- 第四天到第七天，分别吃掉第四天至第七天长出的苹果（具体顺序可自行安排，只要不吃到已腐烂的苹果）。
```

**示例 2**  
```
Input: apples = [3,0,0,0,0,2], days = [3,0,0,0,0,2]
Output: 5
Explanation: 你可以吃掉 5 个苹果：
- 第一天到第三天，吃掉第一天长出的苹果（因为它们在第 4 天会腐烂）。
- 第四天和第五天不吃任何苹果（此时树上没有可吃的苹果）。
- 第六天和第七天，吃掉第六天长出的苹果。
```

**约束条件**  
- `n == apples.length == days.length`
- `1 <= n <= 2 * 10^4`
- `0 <= apples[i], days[i] <= 2 * 10^4`
- `days[i] = 0` 当且仅当 `apples[i] = 0`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每天产生的苹果全部记下来，然后每天挑一颗可以吃的苹果**。  
我们可以用一个二维列表 `store[day] = [(expire_day, cnt)]` 来保存第 `day` 天出现的苹果，其中：

* `expire_day = day + days[day]` —— 这批苹果什么时候会腐烂（不再能吃）。
* `cnt` —— 这批苹果的数量。

每天的吃法：

1. 把当天产生的苹果（如果有）加入 `store[day]`。
2. 遍历 `store[day]` 中所有未腐烂的批次，挑选**剩余数量最多**的一批吃一颗（因为我们只想保证能吃到最多的苹果，随便挑一颗都可以，只要不让苹果浪费）。
3. 吃完后把对应批次的 `cnt` 减 1；如果 `cnt` 变成 0 或者已经到了 `expire_day`，就把这批从列表中移除。

> **类比**：把每批苹果想象成超市里的保质期商品，`expire_day` 就是商品的“有效期”。我们每天都去超市挑选一种还没到期且数量最多的商品来吃。

这种做法一定能得到正确答案，因为我们把所有可能的苹果都列举出来，并且在每一天都真实地模拟了“吃一颗”的过程。

#### 代码（Python）

```python
def eatenApples_bruteforce(apples, days):
    n = len(apples)
    # store[day] 保存当天产生的所有批次 (expire_day, remaining_cnt)
    store = [[] for _ in range(n + max(days) + 1)]   # 最多会吃到的最后一天
    ans = 0

    for cur_day in range(len(store)):
        # ① 把今天新长出的苹果加入 store
        if cur_day < n and apples[cur_day] > 0:
            expire = cur_day + days[cur_day]          # 腐烂的那一天
            store[cur_day].append([expire, apples[cur_day]])

        # ② 在所有未腐烂的批次中挑选数量最多的吃一颗
        best_idx = -1
        best_cnt = 0
        for i, batch in enumerate(store[cur_day]):
            expire, cnt = batch
            # 只考虑还没腐烂且还有剩余的批次
            if expire > cur_day and cnt > 0:
                if cnt > best_cnt:
                    best_cnt = cnt
                    best_idx = i

        # ③ 吃掉一颗
        if best_idx != -1:                # 找到可吃的批次
            store[cur_day][best_idx][1] -= 1   # 剩余数量减一
            ans += 1

        # ④ 清理当天已经腐烂或已吃完的批次，避免后面遍历浪费时间
        store[cur_day] = [b for b in store[cur_day] if b[0] > cur_day and b[1] > 0]

    return ans
```

> **关键注释**  
> - `store` 用二维列表模拟“每一天的所有苹果批次”。  
> - `expire > cur_day` 保证苹果还没腐烂。  
> - 每天只遍历当天的批次，时间会随天数线性增长。

#### 复杂度  

- **时间复杂度**：`O(T * B)`，其中 `T` 是我们可能吃到的最后一天（≈ `n + max(days)`），`B` 是当天最多的批次数。最坏情况下，每天都有 `O(n)` 批次，导致 `O(n²)`，即“平方级”。  
  - 大白话：如果天数是 10 000，最坏需要检查 10 000 × 10 000 = 1 亿 次，显然太慢。
- **空间复杂度**：`O(T + total_batches)`，主要是存放所有批次的列表，最坏也是 `O(n²)`（因为每一天都可能产生新批次）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出现在每天遍历所有批次去找“最合适的”那一批。我们需要一种**能快速取出** **“最近会腐烂且数量>0的批次”** 的数据结构。

> **关键观察**  
> - 为了不让苹果浪费，**先吃掉最早会腐烂的那批** 是最优的（题目提示）。因为如果我们把早到期的苹果留到以后，可能已经腐烂，而后面更久才到期的苹果仍然可以吃。

这正好对应 **“最小堆（优先队列）”**：  
- 堆中每个元素是 `(expire_day, remaining_cnt)`。  
- 堆会把 `expire_day` 最小的批次放在堆顶，**O(log k)**（k 为堆中批次数）取出/插入。

**算法步骤**（逐日模拟）：

1. **遍历日期 `day = 0, 1, 2, …`**，直到没有批次可以吃（即堆空且已遍历完原数组）。  
2. **加入新批次**：如果 `apples[day] > 0`，把 `(day + days[day], apples[day])` 推入堆。  
3. **删除已腐烂的批次**：堆顶的 `expire_day` ≤ `day` 表示这批已经烂了，弹出并继续检查堆顶。  
4. **吃苹果**：如果堆不为空，堆顶就是**最早会腐烂**且还有剩余的批次。我们吃一颗，`remaining_cnt -= 1`，并把它重新放回堆（如果还有剩余的话）。计数 `ans += 1`。  
5. **继续下一天**。

> **类比**：想象有很多盒子装着苹果，每个盒子上贴着“保质期”。我们每天只挑**保质期最近**的盒子吃一颗，吃完后如果盒子里还有苹果就放回去继续使用。这个过程就像把盒子放进一个“保质期最小优先”的抽屉（堆）里。

**为什么最优**  
- 若我们不先吃最早腐烂的批次，而是吃了保质期更长的批次，那么最早的批次可能会在后面某天被迫丢掉，导致总吃的苹果数减少。  
- 采用堆保证每一步都**贪心**选择最安全（最先会坏）的苹果，整个过程不会产生冲突，故全局最优。

#### 代码（Python）

```python
import heapq
from typing import List

def eatenApples(apples: List[int], days: List[int]) -> int:
    """
    使用最小堆（优先队列）贪心模拟每天吃苹果的过程
    """
    n = len(apples)
    heap = []                # 堆中元素为 (expire_day, remaining_cnt)
    day = 0                  # 当前模拟的天数
    eaten = 0                # 已吃的苹果数

    # 只要还有未遍历的天数 或者 堆里还有未吃完的批次，就继续循环
    while day < n or heap:
        # 1️⃣ 把当天新长出的苹果加入堆
        if day < n and apples[day] > 0:
            expire = day + days[day]          # 这批苹果的腐烂日
            heapq.heappush(heap, (expire, apples[day]))

        # 2️⃣ 弹出所有已经腐烂的批次（expire <= day）
        while heap and heap[0][0] <= day:
            heapq.heappop(heap)

        # 3️⃣ 吃掉堆顶批次的一个苹果（如果还有可吃的批次）
        if heap:
            expire, cnt = heapq.heappop(heap)   # 取出最早会腐烂的批次
            cnt -= 1                            # 吃掉一颗
            eaten += 1
            # 如果这批还有剩余且还没到期，放回堆中继续使用
            if cnt > 0 and expire > day:
                heapq.heappush(heap, (expire, cnt))

        # 进入下一天
        day += 1

    return eaten
```

> **关键注释**  
> - `heapq.heappush` / `heappop` 为 **O(log k)** 的插入/删除操作。  
> - `while heap and heap[0][0] <= day:` 用来**清理已经烂掉的批次**，防止误吃。  
> - `day < n or heap` 循环条件保证即使原数组遍历完后，堆里仍有未腐烂的苹果时还能继续吃。

#### 复杂度  

- **时间复杂度**：`O(T log K)`，其中 `T` 是实际模拟的天数（≤ `n + max(days)`），`K` 是堆中最多的批次数。每一天最多进行一次 `push`、一次 `pop`（以及可能的再次 `push`），每次操作是 `log K`。  
  - 大白话：如果最多有 20 000 天，每次只需要几次 “找最小值” 的操作，整体大约是 **几万次乘以 log(几千)**，远远快于平方级的暴力法。
- **空间复杂度**：`O(K)`，堆里最多保存同一天产生且未吃完的批次数，最坏情况下是 `O(n)`。

---

## 心得

- **核心技巧**：**贪心 + 最小堆**，始终优先吃掉**最近会腐烂**的苹果。  
- **该技巧适用的题型**：  
  1. “最早截止日期任务调度”（如 LeetCode 1834 `Maximum Population Year`）  
  2. “处理有有效期的资源”（如 LeetCode 2072 `The Maximum Number of Jobs You Can Accept`）  
  3. “需要按时间顺序取最小/最大值的滑动窗口问题”。  
- **一句话总结**：**先吃最早会坏的苹果，使用最小堆快速找到它**。

## 反思

- **第一反应**：看到“每一天只能吃一颗，苹果有保质期”，直觉是**模拟每一天**，把所有苹果列出来，然后挑一颗吃。  
- **最容易踩的坑**：  
  - **忘记删除已经腐烂的批次**，导致误吃已经烂的苹果。  
  - **边界天数**：原数组遍历完后，堆里仍可能有未到期的苹果，需要继续模拟后续的天数。  
  - **days[i] = 0** 时对应的 `apples[i]` 必然为 0，若不处理会产生无效的批次。  
- **下次类似题目第一步**：先**确定“先做什么”**（如“先吃最早到期的”，或“先处理最短期限的任务”），然后**选用合适的数据结构**（堆、队列、前缀和等）来**高效实现**这个“先做”。