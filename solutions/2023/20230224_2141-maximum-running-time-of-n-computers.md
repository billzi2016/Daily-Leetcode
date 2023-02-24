# #2141. N 台电脑的最长运行时间 / Maximum Running Time of N Computers

> 难度：困难 · 标签：Array、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-running-time-of-n-computers/)

---

## 题目（英文原版）

**Description**

You have n computers. You are given the integer n and a 0-indexed integer array batteries where the ith battery can run a computer for batteries[i] minutes. You are interested in running all n computers simultaneously using the given batteries.
Initially, you can insert at most one battery into each computer. After that and at any integer time moment, you can remove a battery from a computer and insert another battery any number of times. The inserted battery can be a totally new battery or a battery from another computer. You may assume that the removing and inserting processes take no time.
Note that the batteries cannot be recharged.
Return the maximum number of minutes you can run all the n computers simultaneously.

**Examples**

**Example 1:**

```
Input: n = 2, batteries = [3,3,3]
Output: 4
Explanation: 
Initially, insert battery 0 into the first computer and battery 1 into the second computer.
After two minutes, remove battery 1 from the second computer and insert battery 2 instead. Note that battery 1 can still run for one minute.
At the end of the third minute, battery 0 is drained, and you need to remove it from the first computer and insert battery 1 instead.
By the end of the fourth minute, battery 1 is also drained, and the first computer is no longer running.
We can run the two computers simultaneously for at most 4 minutes, so we return 4.
```

**Example 2:**

```
Input: n = 2, batteries = [1,1,1,1]
Output: 2
Explanation: 
Initially, insert battery 0 into the first computer and battery 2 into the second computer. 
After one minute, battery 0 and battery 2 are drained so you need to remove them and insert battery 1 into the first computer and battery 3 into the second computer. 
After another minute, battery 1 and battery 3 are also drained so the first and second computers are no longer running.
We can run the two computers simultaneously for at most 2 minutes, so we return 2.
```

**Constraints**

- 1 <= n <= batteries.length <= 105
- 1 <= batteries[i] <= 109

---

## 题目（中文翻译）

你有 `n` 台电脑。给定整数 `n` 和一个 **0 索引** 整数数组 `batteries`，其中第 `i` 块电池可以为电脑提供 `batteries[i]` 分钟的电量。你希望使用这些电池让所有 `n` 台电脑同时运行。

最开始，你最多可以在每台电脑中插入一块电池。此后在任意整数时间点，你可以**移除**一台电脑中的电池并**插入**另一块电池，且此操作可以进行任意次数。插入的电池可以是全新的电池，也可以是从另一台电脑上取下的电池。可以假设移除和插入过程不消耗时间。

需要注意的是，电池不可充电。

返回能够让所有 `n` 台电脑同时运行的最长分钟数。

---

## 示例

### 示例 1

**输入**  
`n = 2, batteries = [3,3,3]`

**输出**  
`4`

**解释**  
最初，将电池 `0` 插入第一台电脑，电池 `1` 插入第二台电脑。  
两分钟后，从第二台电脑中取出电池 `1`，并插入电池 `2`（此时电池 `1` 仍有 1 分钟电量）。  
第三分钟结束时，电池 `0` 电量耗尽，需要将其从第一台电脑中取出并进行后续操作……  

### 示例 2

**输入**  
`n = 2, batteries = [1,1,1,1]`

**输出**  
`2`

**解释**  
最初，将电池 `0` 插入第一台电脑，电池 `2` 插入第二台电脑。  
一分钟后，电池 `0` 与电池 `2` 均耗尽，需要将它们取下并分别插入电池 `1` 和电池 `3`。  
再过一分钟，电池 `1` 与电池 `3` 也耗尽，此时两台电脑已经运行完毕……  

---

## 约束

- `1 <= n <= batteries.length <= 10^5`
- `1 <= batteries[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟每一分钟**的电池使用过程：

1. **把电池装进电脑**：一开始每台电脑装一块电池（如果电池比电脑多，就随便挑几块）。
2. **每分钟循环**  
   - 所有装在电脑里的电池都耗掉 1 分钟的电量。  
   - 检查哪些电脑的电池已经耗尽，立刻把剩余的、还能用的电池（可能是别的电脑刚换下来的）装进去。  
   - 如果此时已经没有足够的电池可以供所有 `n` 台电脑使用，说明运行已经结束，返回已经跑的分钟数。

> **类比**：想象 `n` 辆车在赛道上跑，车上装的油箱就是电池。每跑 1 公里油箱就少一点，油箱空了就得马上把别的油箱装上去。暴力模拟就是把每公里的油耗都算一遍。

这个思路一定能得到答案，因为我们把**每一分钟**的所有可能换电操作都穷举了——只要还有足够的电池，总能找到一种换法让所有电脑继续跑。

但是**时间会爆炸**：

- 假设 `batteries` 总容量为 `S`（所有电池的分钟数之和），最长可能运行时间也不超过 `S // n`。如果 `S` 很大（如 `10^14`），逐分钟模拟就要循环 `10^14` 次，根本不可接受。

#### 代码（Python）

```python
def maxRunTime_bruteforce(n: int, batteries: list[int]) -> int:
    # 把电池按剩余时间从大到小排序，方便取出“最大的”电池
    batteries = sorted(batteries, reverse=True)

    # 初始时每台电脑装一块电池（如果电池不够则直接返回 0）
    if len(batteries) < n:
        return 0
    running = batteries[:n]          # 正在使用的电池剩余时间
    spare = batteries[n:]            # 备用电池

    minutes = 0
    while True:
        # 所有正在使用的电池都减 1 分钟
        running = [t - 1 for t in running]
        minutes += 1

        # 收集已经耗尽的电脑
        exhausted_idx = [i for i, t in enumerate(running) if t == 0]

        # 如果有电脑没电且没有备用电池可以补上，结束
        if len(exhausted_idx) > len(spare):
            return minutes - 1   # 前一分钟是最后一次成功运行

        # 用备用电池给这些电脑重新装电池
        for i in exhausted_idx:
            # 取出一块容量最大的备用电池
            running[i] = spare.pop()   # spare 已经是从大到小的，pop() 取最小的，这里不影响正确性
        # 为了保持 spare 仍然有序（仅用于演示），重新排序
        spare.sort(reverse=True)
```

> 代码仅用于说明思路，实际运行会超时。

#### 复杂度  

- **时间复杂度**：`O(T * n)`，其中 `T` 是实际运行的分钟数（最坏可达 `Σ batteries[i] / n`），相当于**指数级**。用大白话说，就是“如果电池总容量是 100 万分钟，程序要跑 100 万次循环”，远远超出 1 秒的限制。  
- **空间复杂度**：`O(n)` 用来存放正在运行的电池和备用电池。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：**我们不需要真的去逐分钟模拟**，只要能够**判断**在给定的运行时间 `t` 下，是否能让所有电脑同时工作 `t` 分钟，就可以用**二分查找**找出最大的 `t`。

**关键观察**  

- 在 `t` 分钟内，每台电脑至少需要 `t` 分钟的电量。  
- 只要把所有电池的容量加起来，检查**总电量是否不少于 `n * t`**，并且**每块电池最多只能提供 `t` 分钟**（因为一块电池如果超过 `t`，多余的时间也只能供其他电脑使用，等价于只取 `min(battery, t)`）。

因此，判断 `t` 是否可行的过程是：

1. 对每块电池 `b`，它最多能贡献 `min(b, t)` 分钟（超过 `t` 的部分在 `t` 分钟内只能用于一台电脑，剩余的时间无法再利用）。  
2. 把所有这些贡献相加，记为 `total`。  
3. 如果 `total >= n * t`，说明电池总量足够支撑 `n` 台电脑跑 `t` 分钟；否则不可行。

这一步只需要遍历一次电池数组，时间 `O(m)`（`m = len(batteries)`），空间 `O(1)`。

**二分搜索**  

- **搜索范围**：最少可以跑 `0` 分钟，最多不可能超过所有电池总容量除以电脑数，即 `sum(batteries) // n`。  
- 采用**左闭右闭**区间 `[low, high]`，每次取中点 `mid`，用上面的检查函数判断可行性：  
  - 可行 → 说明可以更久，`low = mid + 1`（尝试更大的 `mid`）。  
  - 不可行 → 说明太久了，`high = mid - 1`。  
- 循环结束后，`high` 就是最大可行的运行时间。

> **类比**：把所有电池看成一大桶水，`t` 分钟相当于每台电脑每天要喝 `t` 升。我们先猜一个 `t`，检查这桶水够不够喂 `n` 台电脑 `t` 天。如果够，就往更大的 `t` 猜；如果不够，就往小的 `t` 猜。二分搜索就像把猜的范围不断对半砍，快速收敛到最大可能的 `t`。

#### 代码（Python）

```python
def maxRunTime(n: int, batteries: list[int]) -> int:
    """
    返回 n 台电脑能够同时运行的最长分钟数
    思路：二分搜索 + 贪心检查（每块电池最多贡献 min(battery, t) 分钟）
    """
    # 1. 计算搜索上界：总电量除以电脑数
    total_power = sum(batteries)
    high = total_power // n          # 最大可能的运行时间
    low = 0                          # 最小可能是 0

    # 2. 二分搜索
    while low <= high:
        mid = (low + high) // 2      # 试探的运行时间

        # 计算在时间 mid 下所有电池能提供的总分钟数
        # 每块电池最多只能贡献 mid 分钟
        can_supply = 0
        for b in batteries:
            can_supply += min(b, mid)
            # 早停：如果已经够了，就不必继续累加
            if can_supply >= n * mid:
                break

        if can_supply >= n * mid:   # mid 可行，尝试更大
            low = mid + 1
        else:                       # mid 不可行，减小范围
            high = mid - 1

    # 循环结束时 high 是最后一个可行的值
    return high
```

**关键行中文注释**  

- `high = total_power // n`：总电量除以电脑数，是一个不可能被超过的上限。  
- `can_supply += min(b, mid)`：每块电池最多只能在 `mid` 分钟内贡献 `mid` 分钟的电量，超过的部分在这段时间里无法再被利用。  
- `if can_supply >= n * mid: break`：一旦累计的可用电量已经满足 `n` 台电脑 `mid` 分钟的需求，就可以提前退出循环，提升效率。  

#### 复杂度  

- **时间复杂度**：`O(m log (S/n))`  
  - `m = len(batteries)`（最多 `10^5`）是遍历电池的成本。  
  - `log (S/n)` 是二分搜索的迭代次数，`S` 为所有电池容量之和，最多约 `log(10^14) ≈ 47`，可以视作常数。  
  - 用大白话说，就是**遍历一次数组大约 50 次**，在 1 秒内完全可以完成。  
- **空间复杂度**：`O(1)`，只使用了常数级的额外变量。

---

## 心得

- **核心技巧**：**二分答案 + 贪心检查**。先把“能否做到”转化为一个**单调判定问题**（时间越长越难实现），再用二分快速定位最大可行值。  
- **适用题型**  
  1. “最大化最小值”类问题，如**分配工作、分配木块、最大化最小距离**等。  
  2. 需要判断“在给定资源和时间下是否可行”的问题，如**装配线调度、船运最大载重**等。  
- **一句话总结**：**把“能否跑 t 分钟”抽象成“所有电池贡献的有效时间是否 ≥ n·t”，二分搜索即得最优答案。**

---

## 反思

- **第一反应**：看到“可以随时换电池”，会想到**模拟换电**，于是想到逐分钟遍历。  
- **最容易踩的坑**  
  - **忽略每块电池的上限**：在检查 `t` 可行性时必须使用 `min(battery, t)`，否则会把单块电池的超额时间错误地算进去，导致答案偏大。  
  - **搜索上界选错**：直接用 `max(batteries)` 可能会低估上界，因为多块电池可以一起供电，正确的上界是 `sum(batteries)//n`。  
  - **整数溢出**（在某些语言中）：`n * t` 可能超出 32 位整数范围，使用 64 位或 Python 的大整数即可。  
- **下次遇到同类题**：第一步立刻**把问题转化为“是否能满足需求”**的判定函数，检查单调性后直接套二分搜索，而不是去模拟细节。这样既能避免时间爆炸，也能让代码结构更清晰。