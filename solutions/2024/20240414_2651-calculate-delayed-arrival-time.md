# #2651. 计算延迟到达时间 / Calculate Delayed Arrival Time

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/calculate-delayed-arrival-time/)

---

## 题目（英文原版）

**Description**

You are given a positive integer arrivalTime denoting the arrival time of a train in hours, and another positive integer delayedTime denoting the amount of delay in hours.
Return the time when the train will arrive at the station.
Note that the time in this problem is in 24-hours format.

**Examples**

**Example 1:**

```
Input: arrivalTime = 15, delayedTime = 5 
Output: 20 
Explanation: Arrival time of the train was 15:00 hours. It is delayed by 5 hours. Now it will reach at 15+5 = 20 (20:00 hours).
```

**Example 2:**

```
Input: arrivalTime = 13, delayedTime = 11
Output: 0
Explanation: Arrival time of the train was 13:00 hours. It is delayed by 11 hours. Now it will reach at 13+11=24 (Which is denoted by 00:00 in 24 hours format so return 0).
```

**Constraints**

- 1 <= arrivaltime < 24
- 1 <= delayedTime <= 24

---

## 题目（中文翻译）

给定一个正整数 `arrivalTime` 表示列车的原始到达时间（单位：小时），以及另一个正整数 `delayedTime` 表示延迟的时长（单位：小时）。  
返回列车实际到达车站的时间。  
注意，题目中的时间采用 **24 小时制（24-hours format）**。

**示例 1：**  
**示例 2：**  

**约束条件：**  

### 示例

#### 示例 1
**输入:** `arrivalTime = 15, delayedTime = 5`  
**输出:** `20`  
**解释:** 列车原计划在 15:00 到达，延迟了 5 小时，实际到达时间为 15 + 5 = 20（20:00）。

#### 示例 2
**输入:** `arrivalTime = 13, delayedTime = 11`  
**输出:** `0`  
**解释:** 列车原计划在 13:00 到达，延迟了 11 小时，实际到达时间为 13 + 11 = 24。24 在 24 小时制中表示 00:00，故返回 0。

### 约束条件
- `1 <= arrivalTime < 24`
- `1 <= delayedTime <= 24`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **到达时间** `arrivalTime` 和 **延迟时间** `delayedTime` 直接相加，得到一个 “原始” 的到达时刻。  
但是题目要求的时间是 **24 小时制**，也就是说如果相加的结果 ≥ 24，就要回到第二天的零点继续计数。  

> 类比：我们把一天看成一本有 24 页的日记本，`arrivalTime` 是已经写到的第几页，`delayedTime` 是要再往后写多少页。如果写完后超过第 24 页，就要从第 0 页（即新的一天）重新开始。

实现上，只需要把相加的结果对 24 取余（`% 24`），余数就是符合 24 小时制的答案。  

**为什么这样一定对？**  
- 任意正整数 `x`，`x % 24` 的取值范围是 `[0, 23]`，恰好对应一天中的每个小时。  
- 对 24 取余的本质是“把多余的整天（24 小时）去掉”，所以保留下来的就是当天的时间。

#### 代码（Python）

```python
def calculateDelayedArrivalTime(arrivalTime: int, delayedTime: int) -> int:
    """
    直接相加后取模，得到 24 小时制的到达时间
    """
    # 第一步：把两个小时数相加
    raw_time = arrivalTime + delayedTime          # 例如 13 + 11 = 24

    # 第二步：对 24 取余，去掉完整的整天
    result = raw_time % 24                         # 24 % 24 = 0

    return result
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做了常数次的加法和取模运算，跟输入大小无关。  
  > 大白话：不管你给多少小时，这段代码的运行时间都是一样快的。
- **空间复杂度**：`O(1)` — 只用了几条整数变量，额外占用的内存是常数级的。

---

### 2. 最优解

#### 思路  

从暴力解来看，唯一的“耗时”操作就是一次加法和一次取模，两者都是 **O(1)** 的基本算术操作。  
因此已经达到了理论上的最优时间复杂度，没有可以进一步优化的空间。  
这里把“最优解”写成一个完整的函数，只是把思路整理成更易读的形式：

1. **相加**：`arrivalTime + delayedTime` 得到原始时间。  
2. **取模**：`% 24` 把超过 24 的部分“抹掉”，得到 0~23 之间的结果。  

如果不想使用取模运算，也可以用 `if raw_time >= 24: raw_time -= 24`，效果相同，只是代码稍微长一点。  

#### 代码（Python）

```python
def calculateDelayedArrivalTime_opt(arrivalTime: int, delayedTime: int) -> int:
    """
    最优实现：直接使用取模完成 24 小时制的转换
    """
    # 计算相加后的时间
    total = arrivalTime + delayedTime   # 例如 15 + 5 = 20

    # 通过取模得到当天的时间（余数在 0~23 之间）
    return total % 24
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只有一次加法和一次取模，已经是最快的。  
- **空间复杂度**：`O(1)` — 只用了常数个变量。

---

## 心得

- **核心技巧**：**取模（Modulo）** 用来把超出周期的数值“折回”到合法范围。  
- **适用的题型**  
  1. **时间/日期循环**（如 12 小时制、7 天循环等）  
  2. **环形数组**（如轮询队列、环形缓冲区）  
  3. **数学周期问题**（如求余数、同余方程）  
- **解题钥匙**：**“把超出范围的整段（这里是 24 小时）去掉，用 `% 周期长度`”**。

## 反思

- **第一反应**：看到“时间相加后可能超过 24”，立刻想到 **取模**，因为它正是处理“循环”最常用的工具。  
- **最容易踩的坑**  
  - 忘记 **取模后可能得到 0**（表示午夜），而不是 24。  
  - `arrivalTime` 与 `delayedTime` 均为正整数，但如果有 **0** 的情况，需要确保仍然返回合法的 0~23。  
- **下次类似题的第一步**：先判断“是否有循环/周期”。如果有，**先算出原始值**，随后 **用 `% 周期长度`** 把结果规约到合法区间。