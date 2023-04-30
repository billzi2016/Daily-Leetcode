# #2224. 转换时间所需的最少操作次数 / Minimum Number of Operations to Convert Time

> 难度：简单 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-convert-time/)

---

## 题目（英文原版）

**Description**

You are given two strings current and correct representing two 24-hour times.
24-hour times are formatted as "HH:MM", where HH is between 00 and 23, and MM is between 00 and 59. The earliest 24-hour time is 00:00, and the latest is 23:59.
In one operation you can increase the time current by 1, 5, 15, or 60 minutes. You can perform this operation any number of times.
Return the minimum number of operations needed to convert current to correct.

**Examples**

**Example 1:**

```
Input: current = "02:30", correct = "04:35"
Output: 3
Explanation:
We can convert current to correct in 3 operations as follows:
- Add 60 minutes to current. current becomes "03:30".
- Add 60 minutes to current. current becomes "04:30".
- Add 5 minutes to current. current becomes "04:35".
It can be proven that it is not possible to convert current to correct in fewer than 3 operations.
```

**Example 2:**

```
Input: current = "11:00", correct = "11:01"
Output: 1
Explanation: We only have to add one minute to current, so the minimum number of operations needed is 1.
```

**Constraints**

- current and correct are in the format "HH:MM"
- current <= correct

---

## 题目（中文翻译）

给定两个字符串 `current` 和 `correct`，分别表示两个 **24 小时制时间（24-hour times）**。  
24 小时制时间的格式为 `"HH:MM"`，其中 `HH` 的取值范围是 `00` 到 `23`，`MM` 的取值范围是 `00` 到 `59`。最早的时间是 `00:00`，最晚的时间是 `23:59`。

一次操作可以将时间 `current` 增加 **1、5、15 或 60 分钟（minutes）**，该操作可以执行任意次数。  
返回将 `current` 转换为 `correct` 所需的最少操作次数。

## 示例

### 示例 1
**输入**  
`current = "02:30", correct = "04:35"`

**输出**  
`3`

**解释**  
我们可以通过 3 次操作将 `current` 转换为 `correct`，过程如下：  
- 给 `current` 加 `60` 分钟，得到 `"03:30"`。  
- 再加 `60` 分钟，得到 `"04:30"`。  
- 最后加 `5` 分钟，得到 `"04:35"`。  
可以证明，少于 3 次操作无法完成转换。

### 示例 2
**输入**  
`current = "11:00", correct = "11:01"`

**输出**  
`1`

**解释**  
只需要给 `current` 加 `1` 分钟，最少操作次数为 `1`。

## 约束条件
- `current` 与 `correct` 的格式均为 `"HH:MM"`。  
- `current <= correct`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：先把两个时间都转换成「从 00:00 开始经过的分钟数」  
（比如 `"02:30"` → 2 × 60 + 30 = 150 分钟），再算出它们的差值 `diff`（`correct - current`）。

然后我们一次只使用 **最小的操作**——加 **1 分钟**，循环 `diff` 次，把 `current` 推进到 `correct`。  
这相当于把「把时间往后推」这件事拆成最细的颗粒（每次 1 分钟），一步步完成。

> **类比**：把时间想成一本书的页码，`diff` 就是要翻的页数。暴力解法就是“一页一页地翻”，虽然能到达目标，但显然很慢。

只要 `diff` 不为负（题目保证 `current ≤ correct`），循环 `diff` 次就一定能把时间对齐，所以方法是 **正确** 的。

#### 代码（Python）

```python
def convertToMinutes(t: str) -> int:
    """把 \"HH:MM\" 转成从 00:00 开始的总分钟数"""
    h, m = map(int, t.split(":"))
    return h * 60 + m

def minOperations_bruteforce(current: str, correct: str) -> int:
    # 1. 把时间转成分钟
    cur = convertToMinutes(current)
    tar = convertToMinutes(correct)

    # 2. 计算需要前进的分钟数
    diff = tar - cur          # 题目保证 diff >= 0

    # 3. 暴力模拟：每次只加 1 分钟
    ops = 0
    while diff > 0:           # 只要还有差距，就继续加 1 分钟
        diff -= 1             # 前进 1 分钟
        ops += 1              # 记录一次操作
    return ops
```

#### 复杂度

- **时间复杂度**：`O(diff)`  
  这里的 `diff` 是两时间之间的分钟差。例如相差 120 分钟时，需要循环 120 次。  
  用大白话说，就是「执行的次数和要加的分钟数成正比」。
- **空间复杂度**：`O(1)`  
  只用了常数个整数变量，不会随输入规模增长而占用更多内存。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次只加 1 分钟**，如果差距很大（比如相差几百分钟），就要循环几百次，效率低下。  
其实我们可以一次使用 **更大的加法**：题目允许一次加 **1、5、15、60** 分钟。  
显然，加大的步长能让我们更快抵达目标。

**贪心（Greedy）** 的核心思想是：**每一步都尽可能使用最大的可用步长**。  
因为所有步长都是 **彼此的倍数**（60 是 15 的 4 倍，15 是 5 的 3 倍，5 是 1 的 5 倍），
使用更大的步长不会导致后面出现「凑不出」的情况——剩下的差值总能被更小的步长补齐。

实现上，只要把 `diff` 按照 60、15、5、1 的顺序除以对应的步长，得到每种操作需要的次数即可：

1. `cnt60 = diff // 60`，剩余 `diff %= 60`
2. `cnt15 = diff // 15`，剩余 `diff %= 15`
3. `cnt5  = diff // 5`，剩余 `diff %= 5`
4. `cnt1  = diff`（此时 `diff < 5`）

把四个计数相加就是最少的操作次数。

> **类比**：把时间看成装满的水箱，想把水箱从 150 L 加到 275 L。我们有 60 L、15 L、5 L、1 L 四种容量的水桶。贪心的做法就是先用最大的大桶装水，装满后再用次大的，直到装满目标容量。因为大桶容量都是小桶容量的整数倍，永远不会出现「装不满」的尴尬。

#### 代码（Python）

```python
def convertToMinutes(t: str) -> int:
    """把 \"HH:MM\" 转成总分钟数"""
    h, m = map(int, t.split(":"))
    return h * 60 + m

def minOperations_greedy(current: str, correct: str) -> int:
    # 1. 转成分钟并计算差值
    diff = convertToMinutes(correct) - convertToMinutes(current)

    # 2. 按照 60、15、5、1 的顺序贪心使用
    ops = 0
    for step in (60, 15, 5, 1):          # 依次遍历四种步长
        cnt = diff // step               # 能用多少个该步长
        ops += cnt                       # 累计操作次数
        diff %= step                     # 剩余的分钟数
    return ops
```

#### 复杂度

- **时间复杂度**：`O(1)`  
  只进行固定次数的除法/取模（4 次），不随输入大小变化。  
  与暴力解相比，从「和差值成正比」提升到「常数时间」。
- **空间复杂度**：`O(1)`  
  只用了若干整数变量，内存占用固定。

---

## 心得

- **核心技巧**：**贪心**——每一步都选最大可用的操作，使得总步数最少。  
- **适用的题型**：  
  1. “换硬币”类问题（最少硬币数）  
  2. “最少加法”或“最少减法”类的数值转换（如把一个数变成另一个数，只能加固定的几种值）  
  3. “装箱”或“装水”类的容量分配问题
- **一句话总结解题钥匙**：**把差值一次性拆成最大步长的整数倍**。

---

## 反思

- **第一反应**：把时间转成分钟，算出差值，然后想办法把差值「拆」成若干次加法。  
- **最容易踩的坑**：  
  - 忽略了题目保证 `current ≤ correct`，如果不检查会出现负差导致错误。  
  - 没注意到步长之间是整数倍关系，随意使用非贪心策略（比如先用很多 5 分钟再用 60）可能导致操作数增多。  
- **下次类似题的第一步**：先把所有“量”统一到同一单位（这里是分钟），再检查是否可以使用 **贪心**（即是否存在“步长互为倍数”或“局部最优即全局最优”的结构）。