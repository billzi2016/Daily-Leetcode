# #3635. 陆上与水上游乐设施的最早完成时间 II / Earliest Finish Time for Land and Water Rides II

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-ii/)

---

## 题目（英文原版）

**Description**

You are given two categories of theme park attractions: land rides and water rides.
A tourist must experience exactly one ride from each category, in either order.
Return the earliest possible time at which the tourist can finish both rides.

**Examples**

**Example 1:**

```
Input: landStartTime = [2,8], landDuration = [4,1], waterStartTime = [6], waterDuration = [3]
Output: 9
Explanation: ​​​​​​​
Plan A gives the earliest finish time of 9.
```

**Example 2:**

```
Input: landStartTime = [5], landDuration = [3], waterStartTime = [1], waterDuration = [10]
Output: 14
Explanation: ​​​​​​​
Plan A provides the earliest finish time of 14. ​​​​​​​
```

**Constraints**

- 1 <= n, m <= 5 * 104
- landStartTime.length == landDuration.length == n
- waterStartTime.length == waterDuration.length == m
- 1 <= landStartTime[i], landDuration[i], waterStartTime[j], waterDuration[j] <= 105

---

## 题目（中文翻译）

给定两类主题乐园景点：陆上游乐设施（land rides）和水上游乐设施（water rides）。  
游客必须分别体验每类景点恰好一次，顺序可以任意。  
返回游客能够完成两次游玩所能达到的最早时间。

### 示例 1
**输入**  
`landStartTime = [2,8], landDuration = [4,1], waterStartTime = [6], waterDuration = [3]`  

**输出**  
`9`  

**解释**  
方案 A 能够在时间 9 完成，两次游玩的最早完成时间为 9。

### 示例 2
**输入**  
`landStartTime = [5], landDuration = [3], waterStartTime = [1], waterDuration = [10]`  

**输出**  
`14`  

**解释**  
方案 A 能够在时间 14 完成，两次游玩的最早完成时间为 14。

### 约束条件
- `1 <= n, m <= 5 * 10^4`
- `landStartTime.length == landDuration.length == n`
- `waterStartTime.length == waterDuration.length == m`
- `1 <= landStartTime[i], landDuration[i], waterStartTime[j], waterDuration[j] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把 **所有** 陆地设施和 **所有** 水上设施两两配对，分别算出先玩陆地后玩水上、先玩水上后玩陆地两种顺序的结束时间，取最小值。

- **配对**：遍历 `landStartTime[i] / landDuration[i]` 与 `waterStartTime[j] / waterDuration[j]` 的每一种组合。  
- **结束时间**：  
  1. 先玩陆地：  
     - 陆地结束时间 `finishL = landStartTime[i] + landDuration[i]`。  
     - 若水上设施的开放时间 `waterStartTime[j]` **早于或等于** `finishL`，我们可以直接在陆地结束后立刻上水上，结束时间为 `finishL + waterDuration[j]`。  
     - 否则要等到水上设施开放，结束时间为 `waterStartTime[j] + waterDuration[j]`。  
  2. 先玩水上：同理，只是把陆地和水上换位。  

- **取最小**：遍历完所有配对后，选出最早的结束时间。

> **类比**：把每个设施想成一本“游乐手册”，手册里写着“最早可以进去的时间”和“玩多久”。暴力解就是把所有手册两两摆在一起，逐一算出读完两本手册需要的最短时间。

这种方法一定能得到正确答案，因为它把**所有可能的组合**都算了一遍。  

**为什么正确**：题目只要求挑选 **恰好** 一个陆地和一个水上设施，并且顺序可以自由决定。遍历全部组合必然覆盖最优组合。

**复杂度**  
- 时间复杂度：`O(n * m)`（`n` 为陆地设施数量，`m` 为水上设施数量）。  
  - 如果 `n = m = 5·10⁴`，则需要 2.5 × 10⁹ 次计算，显然会超时。  
- 空间复杂度：`O(1)`（只用常数级的临时变量）。

> **大白话**：`O(n*m)` 就像把 5 万本书两两配对去比较，需要几千亿次比较，普通电脑根本跑不完。

---

#### 代码（Python）

```python
from typing import List

def brute_force(landStartTime: List[int], landDuration: List[int],
                waterStartTime: List[int], waterDuration: List[int]) -> int:
    INF = 10 ** 18
    ans = INF

    # ---------- 先玩陆地，再玩水上 ----------
    for sL, dL in zip(landStartTime, landDuration):
        finishL = sL + dL                     # 陆地结束时间
        for sW, dW in zip(waterStartTime, waterDuration):
            if sW <= finishL:                 # 水上已经开了，可以立刻上
                finish = finishL + dW
            else:                             # 需要等水上开放
                finish = sW + dW
            ans = min(ans, finish)

    # ---------- 先玩水上，再玩陆地 ----------
    for sW, dW in zip(waterStartTime, waterDuration):
        finishW = sW + dW                     # 水上结束时间
        for sL, dL in zip(landStartTime, landDuration):
            if sL <= finishW:
                finish = finishW + dL
            else:
                finish = sL + dL
            ans = min(ans, finish)

    return ans
```

> **注释**：每一行都写了中文解释，帮助理解每一步在干什么。

#### 复杂度

- **时间复杂度**：`O(n * m)` —— 两个循环套在一起，数量级是两类设施数量的乘积。  
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量，不会随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**每一次配对都要遍历全部另一类设施**。如果我们能在 **对另一类设施的查询** 上做到 **快速定位**（比如 `O(log m)`），整体时间就会大幅下降。

关键观察：

1. 对于固定的第一类设施（假设是陆地），我们只关心 **水上设施的开放时间** 与 **陆地结束时间** 的相对大小。  
2. 把所有水上设施 **按照开放时间 `start` 排序**，则可以用二分查找把水上设施划分成两块：  
   - **早到组**：`waterStartTime <= finishL` → 可以立刻上，结束时间为 `finishL + waterDuration`。  
   - **晚到组**：`waterStartTime > finishL` → 必须等，结束时间为 `waterStartTime + waterDuration`。  
3. 对这两块我们只需要 **最小的** 结束时间：  
   - 早到组只需要最小的 **持续时间** `minDuration`（因为 `finishL` 已经固定），答案是 `finishL + minDuration`。  
   - 晚到组只需要最小的 **结束时间** `start + duration`，答案是 `min(start+duration)`。  
4. 为了在 `O(1)` 时间得到这两个最小值，提前准备两个前缀/后缀数组：  
   - `prefixMinDur[i]` = 前 `i` 个（水上设施）中 **最短的 duration**。  
   - `suffixMinFinish[i]` = 从第 `i` 个到最后的 **最小 (start+duration)**。  
5. 对每个陆地设施，二分定位分界点 `idx`（最后一个满足 `start <= finishL` 的下标），然后用上面的前缀/后缀数组快速算出 **该陆地设施对应的最佳配对**。  
6. 同理，**把顺序换成水上先玩**，再跑一次同样的过程。  
7. 两次过程的最小值即为答案。

> **类比**：把水上设施想成排好队的公交车，车次有不同的发车时间（`start`）和行驶时长（`duration`）。我们已经坐上了一辆陆地“巴士”，想接下一辆公交。我们只需要知道在我们到站前已经发车的最短路程公交（前缀最小时长），以及我们到站后还能等到的最早到达终点的公交（后缀最小结束时间）。提前算好这些信息，就可以在 O(log m) 内直接挑选最优的公交。

**步骤细化**  

1. **排序**：把水上设施按 `start` 升序排列，得到 `w_start[i]`、`w_dur[i]`。  
2. **前缀最小时长** `pre_min_dur[i]`：  
   ```
   pre_min_dur[0] = w_dur[0]
   pre_min_dur[i] = min(pre_min_dur[i-1], w_dur[i])
   ```
3. **后缀最小结束时间** `suf_min_finish[i]`（`start+duration`）：  
   ```
   suf_min_finish[-1] = w_start[-1] + w_dur[-1]
   suf_min_finish[i] = min(suf_min_finish[i+1], w_start[i] + w_dur[i])
   ```
4. **遍历第一类设施**（这里以陆地为例）：  
   - `finish1 = land_start + land_dur`。  
   - 用 `bisect_right` 在 `w_start` 中找到 `idx = last index where w_start <= finish1`。  
   - 计算两种可能的完成时间：  
     - 若 `idx >= 0`（有早到组），`cand1 = finish1 + pre_min_dur[idx]`。  
     - 若 `idx + 1 < len(w_start)`（有晚到组），`cand2 = suf_min_finish[idx+1]`。  
   - 取 `min(cand1, cand2)` 作为该陆地设施的最佳配对结束时间，更新全局最小答案。  
5. **交换顺序**：把陆地和水上角色互换，重复步骤 1‑4。  
6. **返回答案**。

**复杂度分析**  

- 排序：`O(n log n + m log m)`。  
- 前缀/后缀预处理：`O(n + m)`（线性遍历）。  
- 主循环：对每个陆地设施一次二分查找 `O(log m)`，共 `O(n log m)`；再对每个水上设施一次二分 `O(log n)`，共 `O(m log n)`。  
- 整体时间：`O((n+m) log (n+m))`。  
- 额外空间：存排好序的数组和前缀/后缀数组，`O(n+m)`。

相比暴力的 `O(n*m)`，现在即使 `n=m=5·10⁴` 也只需要几百万次操作，轻松在 1 秒内跑完。

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def _prepare(second_start: List[int], second_dur: List[int]):
    """
    将第二类设施按 start 排序，并构造
    1) 前缀最小 duration
    2) 后缀最小 (start + duration)
    返回 (sorted_start, prefix_min_dur, suffix_min_finish)
    """
    # 按 start 排序，保持 start 与对应的 duration 对齐
    paired = sorted(zip(second_start, second_dur), key=lambda x: x[0])
    s = [p[0] for p in paired]          # 排好序的 start
    d = [p[1] for p in paired]          # 对应的 duration

    # 前缀最小 duration
    pre_min = [0] * len(d)
    cur = float('inf')
    for i, dur in enumerate(d):
        cur = min(cur, dur)
        pre_min[i] = cur

    # 后缀最小 (start + duration)
    suf_min = [0] * len(d)
    cur = float('inf')
    for i in range(len(d) - 1, -1, -1):
        cur = min(cur, s[i] + d[i])
        suf_min[i] = cur

    return s, pre_min, suf_min


def _min_finish(first_start: List[int], first_dur: List[int],
                second_start: List[int], second_dur: List[int]) -> int:
    """
    先玩 first（如陆地），再玩 second（如水上），返回最早可能的完成时间。
    """
    # 预处理第二类设施
    s2, pre_min_dur, suf_min_finish = _prepare(second_start, second_dur)

    INF = 10 ** 18
    best = INF

    for s1, d1 in zip(first_start, first_dur):
        finish1 = s1 + d1                     # 第一段结束时间

        # 二分找出所有 start <= finish1 的最后下标
        idx = bisect_right(s2, finish1) - 1   # -1 表示“没有早到的”

        # 方案一：在 finish1 立刻上第二段（需要早到组存在）
        if idx >= 0:
            cand = finish1 + pre_min_dur[idx]   # finish1 + 最短 duration
            best = min(best, cand)

        # 方案二：等到后面某个设施才开始（需要晚到组存在）
        if idx + 1 < len(s2):
            cand = suf_min_finish[idx + 1]       # 直接取最小的 (start+duration)
            best = min(best, cand)

    return best


def earliestFinishTime(landStartTime: List[int], landDuration: List[int],
                       waterStartTime: List[int], waterDuration: List[int]) -> int:
    """
    主函数：分别计算“陆地 → 水上”和“水上 → 陆地”的最早完成时间，取最小值。
    """
    # 陆地先玩
    ans1 = _min_finish(landStartTime, landDuration,
                       waterStartTime, waterDuration)

    # 水上先玩
    ans2 = _min_finish(waterStartTime, waterDuration,
                       landStartTime, landDuration)

    return min(ans1, ans2)
```

> **关键行解释**  
> - `paired = sorted(zip(...))`：把设施的开园时间和时长绑在一起，再按时间排好序。  
> - `pre_min[i]`：记录从左到右看到的最短游玩时长，类似“从左边的每本书里挑出最薄的那本”。  
> - `suf_min[i]`：记录从右到左看到的最早可达终点的时间，类似“从后面的公交车里挑出最早到站的那辆”。  
> - `bisect_right`：二分定位，时间复杂度 `O(log m)`。  
> - `finish1 + pre_min_dur[idx]`：先玩完第一段后，马上接上最短的第二段。  
> - `suf_min_finish[idx+1]`：等到后面那辆公交车直接把我们送到终点。

#### 复杂度

- **时间复杂度**：`O((n + m) log (n + m))`  
  - 排序占 `O(n log n + m log m)`，主循环的二分查找共 `n` 次（或 `m` 次），每次 `O(log m)`（或 `O(log n)`）。  
  - 与暴力的 `O(n*m)` 相比，下降了几个数量级。  
- **空间复杂度**：`O(n + m)`  
  - 需要额外存放排序后的数组以及前缀/后缀最小值数组。  

> **对比**：如果 `n = m = 5·10⁴`，最优解大约只会进行 `≈ 2·5·10⁴·log₂5·10⁴ ≈ 1.5·10⁶` 次比较，几乎是暴力解的 **千分之一**。

---

## 心得

- **核心技巧**：**排序 + 前缀/后缀最小值 + 二分查找**。  
  这套组合常用于“**先后顺序可变、需要最小化总耗时**”的场景。  
- **适用的类似题型**  
  1. “两个航班的最早到达时间”  
  2. “选择一件上衣和一条裤子，先后顺序任意，最小化总花费”  
  3. “两段路程的最早完成时间”  
- **一句话总结解题钥匙**：把第二类设施预处理成 **“任意时刻最好的选择”**，随后只需 **一次二分** 即可快速得到最佳配对。

---

## 反思

- **第一反应**：看到“各选一个、顺序可变”，自然想到**枚举所有组合**（暴力）。  
- **最容易踩的坑**  
  1. **忘记等候时间**：第二段设施的开始时间可能晚于第一段结束时间，需要 `max(finish1, start2)`。  
  2. **边界情况**：当所有第二段设施都早于或都晚于 `finish1` 时，前缀或后缀数组可能不存在对应的元素，需要额外判断。  
  3. **整数溢出**：`start + duration` 最大可达 `2·10⁵`，在 Python 中不成问题，但在其他语言要注意使用足够大的类型。  
- **下次遇到同类题**：第一步先**把一类设施按时间排序**，并**预处理出“从左到右的最小值”和“从右到左的最小值”**，这样后续的配对可以在对数时间内完成。