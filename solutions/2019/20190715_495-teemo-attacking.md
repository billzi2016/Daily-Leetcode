# #495. 提莫攻击 / Teemo Attacking

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/teemo-attacking/)

---

## 题目（英文原版）

**Description**

Our hero Teemo is attacking an enemy Ashe with poison attacks! When Teemo attacks Ashe, Ashe gets poisoned for a exactly duration seconds. More formally, an attack at second t will mean Ashe is poisoned during the inclusive time interval [t, t + duration - 1]. If Teemo attacks again before the poison effect ends, the timer for it is reset, and the poison effect will end duration seconds after the new attack.
You are given a non-decreasing integer array timeSeries, where timeSeries[i] denotes that Teemo attacks Ashe at second timeSeries[i], and an integer duration.
Return the total number of seconds that Ashe is poisoned.

**Examples**

**Example 1:**

```
Input: timeSeries = [1,4], duration = 2
Output: 4
Explanation: Teemo's attacks on Ashe go as follows:
- At second 1, Teemo attacks, and Ashe is poisoned for seconds 1 and 2.
- At second 4, Teemo attacks, and Ashe is poisoned for seconds 4 and 5.
Ashe is poisoned for seconds 1, 2, 4, and 5, which is 4 seconds in total.
```

**Example 2:**

```
Input: timeSeries = [1,2], duration = 2
Output: 3
Explanation: Teemo's attacks on Ashe go as follows:
- At second 1, Teemo attacks, and Ashe is poisoned for seconds 1 and 2.
- At second 2 however, Teemo attacks again and resets the poison timer. Ashe is poisoned for seconds 2 and 3.
Ashe is poisoned for seconds 1, 2, and 3, which is 3 seconds in total.
```

**Constraints**

- 1 <= timeSeries.length <= 104
- 0 <= timeSeries[i], duration <= 107
- timeSeries is sorted in non-decreasing order.

---

## 题目（中文翻译）

**描述**  
我们的英雄提莫（Teemo）正在使用毒性攻击对敌方的艾希（Ashe）进行攻击！每当提莫在第 `t` 秒进行一次攻击时，艾希会在恰好 `duration` 秒内受到中毒。更正式地说，第 `t` 秒的攻击会导致艾希在 **包含的时间区间** `[t, t + duration - 1]` 内中毒。如果提莫在毒性效果结束之前再次攻击，则计时器会被重置，毒性效果将在新攻击后 `duration` 秒结束。

给定一个 **非递减** 整数数组 `timeSeries`（时间序列），其中 `timeSeries[i]` 表示提莫在第 `timeSeries[i]` 秒攻击艾希，以及一个整数 `duration`（持续时间）。返回艾希被中毒的 **总秒数**。

**示例 1**  
```text
Input: timeSeries = [1,4], duration = 2
Output: 4
Explanation: 提莫对艾希的攻击过程如下：
- 第 1 秒，提莫攻击，艾希在第 1、2 秒中毒。
- 第 4 秒，提莫攻击，艾希在第 4、5 秒中毒。
艾希在第 1、2、4、5 秒共计 4 秒中毒。
```

**示例 2**  
```text
Input: timeSeries = [1,2], duration = 2
Output: 3
Explanation: 提莫对艾希的攻击过程如下：
- 第 1 秒，提莫攻击，艾希在第 1、2 秒中毒。
- 第 2 秒提莫再次攻击，计时器被重置，艾希在第 2、3 秒中毒。
艾希在第 1、2、3 秒共计 3 秒中毒。
```

**约束条件**  
- `1 <= timeSeries.length <= 10^4`  
- `0 <= timeSeries[i], duration <= 10^7`  
- `timeSeries` 已按非递减顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一次中毒的每一秒** 都记下来，然后去重后计数。  
可以把「中毒的秒」想象成一本日历，Teemo 每攻击一次，就在日历上划出一段连续的日期（`duration` 天）。  
把所有划过的日期放进一个 **集合（set）**，集合天然会去掉重复的日期，最后集合的大小就是 Ashe 被毒的总秒数。

- **数据结构**：`set`（集合）  
  - 类比：就像查字典一样，字典里已经有的词不会再插入，自动去重。这里的「词」是「秒数」。
- **正确性**：因为集合里每个元素恰好代表了一秒钟是否被毒，只要把所有可能被毒的秒全部放进去，去重后剩下的就是实际被毒的秒数。

#### 代码（Python）

```python
def findPoisonedDuration(timeSeries, duration):
    # 用集合保存所有被毒的秒
    poisoned = set()

    for t in timeSeries:                     # 遍历每一次攻击的时间
        # 攻击在 t 时刻，毒持续 duration 秒，包含 t 本身
        for sec in range(t, t + duration):   # 把这段时间的每一秒都加入集合
            poisoned.add(sec)                # 集合会自动去重

    # 集合的大小就是总的中毒秒数
    return len(poisoned)
```

#### 复杂度  

- **时间复杂度**：`O(n * duration)`  
  - `n` 是攻击次数，`duration` 是每次毒持续的秒数。我们在每次攻击时都要遍历 `duration` 个秒，最坏情况下会这么多次循环。  
  - 大白话：如果有 100 次攻击，每次毒 10 秒，就要循环 1000 次。
- **空间复杂度**：`O(T)`，`T` 为所有被毒的不同秒数的个数（最多不超过 `n * duration`）。集合要把每个秒都存下来。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **逐秒枚举**——当 `duration` 很大时会导致大量无意义的循环。  
其实我们只需要关注 **每两次攻击之间的间隔**，因为：

- 如果两次攻击的间隔 `gap = timeSeries[i+1] - timeSeries[i]` 大于等于 `duration`，说明第一次的毒效已经结束，第二次重新开始计时。此时这一次攻击贡献了完整的 `duration` 秒。
- 如果 `gap` 小于 `duration`，说明第二次攻击在第一次毒效还没结束时到来，毒效会被 **重置**，这一次攻击只贡献了 `gap` 秒（因为前面的 `gap` 秒已经被算进了上一次的毒时长）。

于是我们只需遍历一次数组，累计每次攻击实际贡献的秒数：

```
total = 0
for i from 0 to n-2:
    total += min(duration, timeSeries[i+1] - timeSeries[i])
total += duration          # 最后一次攻击一定完整贡献 duration 秒
```

核心概念：

- **最小值 `min`**：取两者较小的那一个，自动处理“是否重叠”的情况。
- **单次遍历**：只看相邻两次攻击，省掉了逐秒枚举。

#### 代码（Python）

```python
def findPoisonedDuration(timeSeries, duration):
    """
    :type timeSeries: List[int]  # 攻击的时间点，已升序
    :type duration: int          # 毒持续的秒数
    :rtype: int                  # 总的中毒秒数
    """
    if not timeSeries:               # 防止空列表（虽然题目保证非空）
        return 0

    total = 0                         # 累计被毒的总秒数

    # 遍历相邻的攻击时间
    for i in range(len(timeSeries) - 1):
        gap = timeSeries[i + 1] - timeSeries[i]   # 两次攻击的时间间隔
        # 这一次攻击实际贡献的秒数 = min(duration, gap)
        total += min(duration, gap)

    # 最后一次攻击一定完整贡献 duration 秒
    total += duration

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次 `timeSeries`（`n` 为攻击次数）。  
  - 大白话：如果有 10⁴ 次攻击，只会循环 10⁴ 次，远比逐秒枚举快。
- **空间复杂度**：`O(1)`，只用了几个额外的变量，不随输入规模增长。

---

## 心得

- **核心技巧**：利用相邻元素的间隔与固定长度 `duration` 取最小值，直接计算每段不重叠的贡献。  
- **适用的题型**  
  1. **区间合并计时**：如「汽车行驶时长」等，需要合并或截断重叠区间。  
  2. **累计不重复时间**：如「视频播放累计观看时长」等。  
  3. **滑动窗口的长度限制**：类似「最长子数组不超过 K」的思路。  
- **一句话总结**：把「每次攻击的实际贡献」看成 `min(duration, 两次攻击的间隔)`，一次遍历即可得总时长。

---

## 反思

- **第一反应**：直接把每秒都记下来，用集合去重，想到「模拟」但没考虑效率。  
- **最容易踩的坑**  
  - **漏算最后一次攻击**：循环只到倒数第二个元素，需要单独加上 `duration`。  
  - **相邻攻击时间相同**（`gap = 0`）：此时 `min(duration, 0) = 0`，不会重复计数。  
  - **duration 为 0**：直接返回 0，代码中 `total += duration` 仍然成立。  
- **下次遇到同类题**：第一步先判断「是否有重叠」——用相邻元素的差值与固定长度比较，决定是否需要合并或截断。这样就能立刻从 O(n·duration) 降到 O(n)。