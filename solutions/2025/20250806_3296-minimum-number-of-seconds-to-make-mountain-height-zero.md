# #3296. 山的高度归零的最少秒数 / Minimum Number of Seconds to Make Mountain Height Zero

> 难度：中等 · 标签：Array、Math、Binary Search、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-seconds-to-make-mountain-height-zero/)

---

## 题目（英文原版）

**Description**

You are given an integer mountainHeight denoting the height of a mountain.
You are also given an integer array workerTimes representing the work time of workers in seconds.
The workers work simultaneously to reduce the height of the mountain. For worker i:
Return an integer representing the minimum number of seconds required for the workers to make the height of the mountain 0.

**Examples**

**Example 1:**

```
Input: mountainHeight = 4, workerTimes = [2,1,1]
Output: 3
Explanation:
One way the height of the mountain can be reduced to 0 is:
Since they work simultaneously, the minimum time needed is max(2, 3, 1) = 3 seconds.
```

**Example 2:**

```
Input: mountainHeight = 10, workerTimes = [3,2,2,4]
Output: 12
Explanation:
The number of seconds needed is max(9, 12, 12, 12) = 12 seconds.
```

**Example 3:**

```
Input: mountainHeight = 5, workerTimes = [1]
Output: 15
Explanation:
There is only one worker in this example, so the answer is workerTimes[0] + workerTimes[0] * 2 + workerTimes[0] * 3 + workerTimes[0] * 4 + workerTimes[0] * 5 = 15 .
```

**Constraints**

- 1 <= mountainHeight <= 105
- 1 <= workerTimes.length <= 104
- 1 <= workerTimes[i] <= 106

---

## 题目（中文翻译）

给定一个整数 `mountainHeight` 表示山的高度。  
再给定一个整数数组 `workerTimes`，其中 `workerTimes[i]` 表示第 `i` 位工人的工作时间（单位：秒）。  

所有工人同时工作，用来把山的高度降为 0。第 `i` 位工人若需要降低 `k` 个单位的高度，则他需要的时间为  

```
workerTimes[i] * (1 + 2 + … + k) = workerTimes[i] * k * (k + 1) / 2
```

即第 1 个单位耗时 `workerTimes[i]` 秒，第 2 个单位耗时 `2 * workerTimes[i]` 秒，依此类推。  

你需要把 `mountainHeight` 分配给各工人（每位工人可以负责任意非负整数个高度），使得所有工人完成各自任务所需的时间的 **最大值** 最小。  

返回一个整数，表示使山的高度降为 0 所需的最少秒数。

---

## 示例

### 示例 1  
**输入**: `mountainHeight = 4, workerTimes = [2,1,1]`  
**输出**: `3`  
**解释**:  
一种可能的分配方式是：  
- 工人 0 负责 1 个单位 → 时间 = `2 * 1 = 2`  
- 工人 1 负责 2 个单位 → 时间 = `1 * (1+2) = 3`  
- 工人 2 负责 1 个单位 → 时间 = `1 * 1 = 1`  

所有工人同时工作，总耗时为 `max(2, 3, 1) = 3` 秒，已达到最小可能值。

### 示例 2  
**输入**: `mountainHeight = 10, workerTimes = [3,2,2,4]`  
**输出**: `12`  
**解释**:  
一种可能的分配方式是：  
- 工人 0 负责 2 个单位 → 时间 = `3 * (1+2) = 9`  
- 工人 1 负责 3 个单位 → 时间 = `2 * (1+2+3) = 12`  
- 工人 2 负责 3 个单位 → 时间 = `2 * (1+2+3) = 12`  
- 工人 3 负责 2 个单位 → 时间 = `4 * (1+2) = 12`  

最大时间为 `max(9, 12, 12, 12) = 12` 秒，已是最小值。

### 示例 3  
**输入**: `mountainHeight = 5, workerTimes = [1]`  
**输出**: `15`  
**解释**:  
只有一名工人，他需要负责全部 5 个单位，高度归零的时间为  

```
1 * (1+2+3+4+5) = 15
```

---

## 约束条件
- `1 <= mountainHeight <= 10^5`
- `1 <= workerTimes.length <= 10^4`
- `1 <= workerTimes[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把时间从 1 秒开始一点点往后推**，每推进一秒，就让所有工人按照他们的工作规律各自削减山的高度，直到累计削减的总高度 ≥ `mountainHeight` 为止。  

- **工人的工作规律**  
  第 1 单位高度需要 `workerTimes[i]` 秒，  
  第 2 单位高度需要 `2 * workerTimes[i]` 秒，  
  第 3 单位高度需要 `3 * workerTimes[i]` 秒，……  
  也就是说，第 `k` 次削减（第 `k` 块高度）耗时 `k * workerTimes[i]`。  

- **用到的数据结构**  
  只需要一个普通的整数数组 `workerTimes`，不需要额外的数据结构。  
  可以把它想象成 **一排工人的“秒表”**，每个人的秒表上记录的是他完成第 k 块高度所需的时间。

- **为什么正确**  
  由于我们是**按时间顺序**、**同步**地模拟每一秒钟里所有工人的工作情况，必然会得到最早能把山削到 0 的那一秒。  

- **复杂度大白话**  
  假设答案是 `T` 秒（也就是最终要返回的最小秒数），我们会循环 `T` 次，每次遍历全部 `n` 位工人来更新他们的进度。  
  用大写的 **O** 记号写就是 `O(T·n)`。  
  如果 `T` 很大（比如几万甚至几百万），这段代码会非常慢。  

#### 代码（Python）

```python
def minSeconds_bruteforce(mountainHeight: int, workerTimes: list[int]) -> int:
    # 已经削减的总高度
    removed = 0
    # 当前已经过去的秒数
    seconds = 0
    # 每个工人已经完成了多少块（第几块）高度，初始为 0
    progress = [0] * len(workerTimes)

    # 循环直到山被削平
    while removed < mountainHeight:
        seconds += 1                         # 时间前进一步
        for i, t in enumerate(workerTimes):
            # 如果这秒正好是第 (progress[i] + 1) 块高度完成的时刻
            # 那么 progress[i] + 1 表示这位工人已经完成了多少块
            # 完成第 k 块需要 k * t 秒，累计起来正好等于 seconds
            # 换句话说：seconds % t == 0 并且
            # seconds // t == progress[i] + 1
            # 为了代码简洁，直接用累加的方式判断
            if seconds == (progress[i] + 1) * t:
                progress[i] += 1            # 这位工人完成了下一块
                removed += 1                # 山的高度整体下降 1
                if removed >= mountainHeight:
                    break                   # 已经够了，直接退出

    return seconds
```

> **关键行中文注释**已经写在代码里，帮助初学者快速定位每一步的意义。

#### 复杂度

- **时间复杂度**：`O(T·n)`  
  这里的 `T` 是答案（最小秒数），`n` 是工人数。  
  用大白话说，就是“每秒要检查所有工人一次”，如果答案是几千秒，循环几千次，每次遍历十个工人，就是几万次操作。

- **空间复杂度**：`O(n)`  
  只用了一个长度为 `n` 的 `progress` 数组来记录每个工人的进度，除此之外几乎不占额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于逐秒模拟**，我们其实不需要知道每一秒到底发生了什么，只要判断 “在 `T` 秒之内，所有工人合计最多能削掉多少高度” 即可。如果这个累计高度 ≥ `mountainHeight`，说明 `T` 秒足够；否则 `T` 太小，需要更久。

因此可以把 **答案的范围**（最小秒数）当成 **单调函数** 来二分查找：

1. **单调性**  
   给定时间 `T`，所有工人在 `T` 秒内能削的总高度 `f(T)` 是 **不下降** 的——时间越长，削的高度只会更多或相同。  
   所以 `f(T) >= mountainHeight` 成立的最小 `T` 正好是我们要的答案。

2. **如何快速计算 `f(T)`**  
   对于第 `i` 位工人，已知 `workerTimes[i] = w`。  
   第 `k` 块高度需要 `k * w` 秒，总共需要的时间是  

   ```
   w * (1 + 2 + … + k) = w * k * (k + 1) / 2
   ```

   我们要求最大整数 `k` 使得 `w * k * (k + 1) / 2 ≤ T`。  
   这是一元二次不等式，解出来：

   ```
   k = floor( ( -1 + sqrt(1 + 8*T / w) ) / 2 )
   ```

   这个公式直接给出该工人在 `T` 秒内能完成的块数（即削掉的高度）。  
   计算一次 `sqrt`，时间是常数级。

3. **二分搜索的边界**  
   - **左边界** `lo = 0`（显然 0 秒削不掉任何高度）。  
   - **右边界** `hi` 需要足够大，使得一定能完成。  
     最坏的情况是只有最慢的工人 `w_max`，而山高 `H`。  
     这位工人单独完成所有高度需要的时间是  

     ```
     w_max * (1 + 2 + … + H) = w_max * H * (H + 1) / 2
     ```

     所以取 `hi = w_max * H * (H + 1) // 2` 作为上界，必然足够。

4. **二分的实现**  
   标准的 “左闭右闭” 二分模板：  
   ```
   while lo < hi:
       mid = (lo + hi) // 2
       if enough(mid):   # f(mid) >= mountainHeight
           hi = mid
       else:
           lo = mid + 1
   return lo
   ```

5. **核心概念解释**  
   - **二分搜索**：像在排好序的书架上找一本书，只需要每次把搜索区间缩小一半，时间是对数级的。这里我们把“时间长短”当成排好序的“坐标”。  
   - **平方根（sqrt）**：在公式里出现的 `sqrt`，相当于我们在求一个 “正方形的边长”。Python 的 `math.isqrt`（整数平方根）可以避免浮点误差。  

#### 代码（Python）

```python
import math
from typing import List

def minSeconds(mountainHeight: int, workerTimes: List[int]) -> int:
    """
    二分答案 + 公式求每个工人在给定时间内能削掉的高度
    """
    # ---------- 1. 确定二分的搜索区间 ----------
    max_w = max(workerTimes)                         # 最慢的工人
    # 最坏情况下只有这一个工人独自完成所有高度的时间上界
    hi = max_w * mountainHeight * (mountainHeight + 1) // 2
    lo = 0                                            # 0 秒显然不够

    # ---------- 2. 判断函数 ----------
    def enough(seconds: int) -> bool:
        """在 seconds 秒内，所有工人合计能削掉的高度是否 >= mountainHeight"""
        total = 0
        for w in workerTimes:
            # 计算 k，使得 w * k * (k+1) / 2 <= seconds
            # 为了避免浮点数，先算 8*seconds // w
            # 注意这里使用整数除法，防止溢出
            # 公式推导：k = floor( (-1 + sqrt(1 + 8*seconds / w)) / 2 )
            # 为了保持整数运算，先算 disc = 1 + 8*seconds // w
            disc = 1 + (8 * seconds) // w
            k = (int(math.isqrt(disc)) - 1) // 2   # isqrt 返回整数平方根
            total += k
            # 提前退出：如果已经够了，就不必继续累加
            if total >= mountainHeight:
                return True
        return total >= mountainHeight

    # ---------- 3. 二分搜索 ----------
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid          # 可能还能更小，继续左侧区间
        else:
            lo = mid + 1      # 右侧区间才有可能满足

    return lo
```

> **代码要点**  
> - `math.isqrt` 是整数平方根，避免了浮点数误差。  
> - 在 `enough` 函数里，**提前返回** 可以在累计高度已经够时立刻结束循环，提升常数因子。  
> - 二分的上界 `hi` 使用最慢工人的最坏时间，保证一定覆盖答案。

#### 复杂度

- **时间复杂度**：`O(n · log answer)`  
  - `log answer` 来自二分的迭代次数（答案的二进制位数），通常不超过 60（因为 `answer` ≤ `10^6 * 10^5 * 10^5 / 2` 仍在 64 位整数范围）。  
  - 每一次二分判断需要遍历所有 `n` 位工人，计算一次平方根，都是常数时间。  
  - 与暴力解的 `O(T·n)` 相比，**把 `T`（可能上万甚至上百万）压缩到对数级**，快了几个数量级。

- **空间复杂度**：`O(1)`（不计输入数组）  
  只用了几个整数变量和循环计数器，没有额外的随 `n` 增长的容器。

---

## 心得

- **核心技巧**：把“能否在 `T` 秒内完成”抽象成单调函数，然后用 **二分搜索** 在时间轴上定位最小可行的 `T`。  
- **适用的题型**  
  1. “在给定资源下，最小/最大时间/容量”类问题（如*分配机器加工任务*、*吃饭速度*、*装水罐*）。  
  2. “满足某个累计条件的最小/最大整数”类问题（如*最小下载时间*、*最大可容纳人数*）。  
  3. 需要 **利用公式快速求单个元素贡献** 的二分题（如*求最少天数让所有机器生产一定数量*）。  
- **一句话总结解题钥匙**：**把“是否足够”变成 O(1)（或 O(n)）的判定函数，随后在答案空间上二分**。

---

## 反思

- **第一反应**：看到工人的工作时间呈等差递增，想到 **等差数列求和**，于是尝试逐秒模拟。  
- **最容易踩的坑**  
  - **溢出**：`w * H * (H+1) / 2` 可能超过 32 位整数，需要使用 64 位（Python 自动大整数，但在其他语言要注意）。  
  - **整数除法的顺序**：在求判定公式时，`8*seconds // w` 必须先除后乘，否则会出现精度或除零错误。  
  - **平方根的精度**：使用浮点 `math.sqrt` 可能出现向下取整错误，建议用 `math.isqrt`（整数平方根）保证正确性。  
- **下次类似题的第一步**：**先思考“单调性”**——如果增加资源（时间、机器、容量）会不会让目标更容易达成？如果是，就立刻考虑二分搜索。随后**把每个元素的贡献用闭式公式算出来**，避免逐步模拟。