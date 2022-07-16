# #1860. 增量内存泄漏 / Incremental Memory Leak

> 难度：中等 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/incremental-memory-leak/)

---

## 题目（英文原版）

**Description**

You are given two integers memory1 and memory2 representing the available memory in bits on two memory sticks. There is currently a faulty program running that consumes an increasing amount of memory every second.
At the ith second (starting from 1), i bits of memory are allocated to the stick with more available memory (or from the first memory stick if both have the same available memory). If neither stick has at least i bits of available memory, the program crashes.
Return an array containing [crashTime, memory1crash, memory2crash], where crashTime is the time (in seconds) when the program crashed and memory1crash and memory2crash are the available bits of memory in the first and second sticks respectively.

**Examples**

**Example 1:**

```
Input: memory1 = 2, memory2 = 2
Output: [3,1,0]
Explanation: The memory is allocated as follows:
- At the 1st second, 1 bit of memory is allocated to stick 1. The first stick now has 1 bit of available memory.
- At the 2nd second, 2 bits of memory are allocated to stick 2. The second stick now has 0 bits of available memory.
- At the 3rd second, the program crashes. The sticks have 1 and 0 bits available respectively.
```

**Example 2:**

```
Input: memory1 = 8, memory2 = 11
Output: [6,0,4]
Explanation: The memory is allocated as follows:
- At the 1st second, 1 bit of memory is allocated to stick 2. The second stick now has 10 bit of available memory.
- At the 2nd second, 2 bits of memory are allocated to stick 2. The second stick now has 8 bits of available memory.
- At the 3rd second, 3 bits of memory are allocated to stick 1. The first stick now has 5 bits of available memory.
- At the 4th second, 4 bits of memory are allocated to stick 2. The second stick now has 4 bits of available memory.
- At the 5th second, 5 bits of memory are allocated to stick 1. The first stick now has 0 bits of available memory.
- At the 6th second, the program crashes. The sticks have 0 and 4 bits available respectively.
```

**Constraints**

- 0 <= memory1, memory2 <= 231 - 1

---

## 题目（中文翻译）

你得到两个整数 `memory1` 和 `memory2`，它们分别表示两根内存条上可用的内存（单位：比特）。当前有一个有缺陷的程序在运行，该程序每秒会消耗递增数量的内存。  

在第 `i` 秒（从 1 开始计数）时，程序会把 `i` 比特的内存分配给 **可用内存更多的** 那根内存条（如果两根内存条的可用内存相同，则分配给第一根内存条）。如果两根内存条都没有至少 `i` 比特的可用内存，程序会崩溃。  

返回一个数组 `[crashTime, memory1Crash, memory2Crash]`，其中  
- `crashTime` 为程序崩溃的时间（秒），  
- `memory1Crash` 为崩溃时第一根内存条剩余的可用内存（比特），  
- `memory2Crash` 为崩溃时第二根内存条剩余的可用内存（比特）。  

## 示例  

### 示例 1  
**输入**: `memory1 = 2, memory2 = 2`  
**输出**: `[3,1,0]`  
**解释**: 内存的分配过程如下:  
- 第 1 秒，分配 1 比特到内存条 1。此时第一根内存条剩余 1 比特可用内存。  
- 第 2 秒，分配 2 比特到内存条 2。此时第二根内存条剩余 0 比特可用内存。  
- 第 3 秒，程序崩溃。两根内存条的剩余可用内存分别为 1 比特和 0 比特。  

### 示例 2  
**输入**: `memory1 = 8, memory2 = 11`  
**输出**: `[6,0,4]`  
**解释**: 内存的分配过程如下:  
- 第 1 秒，分配 1 比特到内存条 2。此时第二根内存条剩余 10 比特可用内存。  
- 第 2 秒，分配 2 比特到内存条 2。此时第二根内存条剩余 8 比特可用内存。  
- 第 3 秒，分配 3 比特到内存条 1。此时第一根内存条剩余 5 比特可用内存。  
- 第 4 秒，分配 4 比特到内存条 2。此时第二根内存条剩余 4 比特可用内存。  
- 第 5 秒，分配 5 比特到内存条 1。此时第一根内存条剩余 0 比特可用内存。  
- 第 6 秒，程序崩溃。两根内存条的剩余可用内存分别为 0 比特和 4 比特。  

## 约束条件  
- `0 <= memory1, memory2 <= 2^31 - 1`   (即 32 位有符号整数的最大值)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**一步一步模拟**题目描述的过程：

1. 从第 `i = 1` 秒开始，依次递增 `i`。
2. 每一次都比较两根内存条剩余的可用空间（`memory1`、`memory2`），把 `i` 位（bits）分配给**剩余空间更大的那根**；如果相等则默认分配给第一根。
3. 如果两根内存条的剩余空间都 **小于 i**，说明程序已经崩溃，记录下当前的秒数 `i`（即崩溃时间）以及两根内存条此时的剩余空间，返回结果。

> **类比**：把每根内存条想成一本字典，字典里还有多少页可以翻就对应剩余的内存。每秒我们要翻 `i` 页，先找那本还有最多未翻页的字典去翻。如果两本字典的未翻页数相同，就固定选第一本。

**为什么正确**：  
题目明确规定每秒必须把 `i` 位分配给“剩余空间更多的那根”。只要我们严格按照这个规则去执行，就一定会得到和题目要求完全一致的分配过程。程序崩溃的唯一条件是**两根内存条都不够 `i` 位**，这正是我们在循环中检测的地方。

**时间/空间复杂度**（大白话）：

- **时间复杂度**：每秒我们只做几次常数时间的比较和减法，循环的次数等于程序崩溃的秒数 `t`。最坏情况下 `t` 可能会很大（比如两根内存条各有 `10^9` 位），所以我们把它记作 **O(t)**。如果把 `t` 用输入规模（总内存 `S = memory1 + memory2`）来表示，`t` 的上界大约是 `√(2S)`（因为 1+2+…+t ≈ t²/2），所以暴力解的时间复杂度可以粗略写成 **O(√S)**，但在代码层面我们仍然是“每秒一次”。

- **空间复杂度**：只用了几个整数变量来保存当前的秒数和两根内存条的剩余空间，**O(1)**，即常数级别的额外空间。

#### 代码（Python）

```python
def memoryLeak(memory1: int, memory2: int):
    """
    暴力模拟每秒的内存分配过程
    返回 [崩溃时间, memory1剩余, memory2剩余]
    """
    i = 1                     # 当前是第 i 秒
    while True:
        # 两根内存条都不足 i 位，程序崩溃
        if memory1 < i and memory2 < i:
            return [i, memory1, memory2]

        # 决定把 i 位分配给哪根内存条
        if memory1 >= memory2:        # memory1 更大或相等，分配给 memory1
            memory1 -= i
        else:                         # memory2 更大，分配给 memory2
            memory2 -= i

        i += 1                        # 进入下一秒
```

#### 复杂度

- **时间复杂度**：`O(t)`，其中 `t` 为程序崩溃的秒数。直观上可以理解为“我们需要跑多少秒才会停”。  
- **空间复杂度**：`O(1)`，只用了固定数量的整数变量。

---

### 2. 最优解

#### 思路  

暴力解已经是**最直接的模拟**，但我们可以利用数学上的上界来避免不必要的循环，使代码更简洁且更容易分析。

1. **上界分析**  
   - 每秒分配的位数形成等差数列 `1, 2, 3, …, t`，其前 `t` 项和为 `S_t = t·(t+1)/2`。  
   - 当程序仍在运行时，已分配的总位数一定不超过两根内存条的总可用位数 `total = memory1 + memory2`。  
   - 因此 `t·(t+1)/2 ≤ total`，解这个不等式可以得到 `t ≤ √(2·total)`（略去常数项）。这说明 **程序最多只会运行到大约 √(2·total) 秒**。

2. **直接模拟到上界**  
   - 基于上面的上界，我们可以在 `while` 循环里直接判断“当前秒数 i 是否已经超过上界”，如果超过则一定已经崩溃（因为前面的等式已经不可能成立），直接返回。  
   - 实际上，这一步并不是必须的，因为前面的 “两根内存都不足 i 位” 条件已经足够终止循环；但写出上界可以帮助我们**提前了解循环次数的最大可能**，从而说明算法是 **O(√total)**，这已经是最优的时间复杂度（因为必须逐秒检查每一次是否还能分配）。

3. **核心技巧 – 前缀和的上界**  
   - 这里使用的“前缀和上界”思路在很多需要**逐步递增消耗资源**的问题里都适用，例如 “把糖果分给孩子们”，“递增的燃油消耗”等。  
   - 关键是把**累计消耗**（等差数列的和）和**资源总量**进行比较，从而得到循环的最大次数。

> **类比**：把两根内存条看成两块油罐，总油量是 `total`。每秒汽车要消耗 `i` 升油，消耗量逐秒递增。我们可以先算出最多能跑多少秒（油罐里油足够支撑的最大秒数），再按秒模拟实际消耗。

#### 代码（Python）

```python
def memoryLeak(memory1: int, memory2: int):
    """
    最优解：同样是模拟，但在分析层面给出循环次数的上界 √(2·total)。
    时间复杂度 O(√total)，空间复杂度 O(1)。
    """
    i = 1                               # 第 i 秒
    total = memory1 + memory2            # 两根内存的总位数（用于上界估算）

    # 只要 i 满足 i*(i+1)/2 <= total，理论上仍有可能继续分配
    while i * (i + 1) // 2 <= total:
        if memory1 >= memory2:           # memory1 更大或相等，分配给 memory1
            if memory1 < i:              # 实际检查：memory1 不够 i 位，程序崩溃
                break
            memory1 -= i
        else:                            # memory2 更大，分配给 memory2
            if memory2 < i:              # 实际检查：memory2 不够 i 位，程序崩溃
                break
            memory2 -= i
        i += 1                           # 进入下一秒

    # 循环结束时 i 已经是 **崩溃的秒数**（因为上面已经检查过不足的情况）
    return [i, memory1, memory2]
```

> **注释解释**  
> - `i * (i + 1) // 2` 是等差数列前 `i` 项的和，代表“如果一直跑到第 `i` 秒，累计需要的内存”。  
> - 循环的 `while` 条件保证我们只在**理论上还能满足**的范围内继续模拟，实际每一步仍然要检查对应内存条是否真的够 `i` 位。

#### 复杂度

- **时间复杂度**：`O(√total)`，其中 `total = memory1 + memory2`。因为循环次数至多是 `√(2·total)`，可以想象成“我们最多只需要跑到 sqrt(两根内存总和) 的秒数”。这已经是最优的，因为我们必须逐秒检查每一次是否还能分配，无法跳过任何秒。
- **空间复杂度**：`O(1)`，只用了常数个整数变量。

---

## 心得

- **核心技巧**：把“递增消耗”转化为等差数列的前缀和，与资源总量比较得到循环上界。  
- **适用场景**：  
  1. **分配递增资源**（如 “Increasing Subtraction” 系列、递增的糖果分配等）。  
  2. **逐秒/逐步递增的消耗**（如 “Fuel Consumption” 类题目、递增的时间窗口等）。  
  3. **需要判断何时资源耗尽** 的情形（如 “Maximum Number of Weeks for a Project”）。
- **一句话总结**：**“把递增的需求累加成等差和，和总资源比较，就能直接得出最多能进行多少轮”**。

---

## 反思

- **第一反应**：看到“每秒 i 位，分配给剩余空间更多的那根”，立刻想到**直接模拟**，因为逻辑非常直观。
- **最容易踩的坑**：  
  - 忘记在两根内存相等时要默认给第一根，导致答案偏差。  
  - 边界条件：当 `memory1` 或 `memory2` 为 `0` 时，程序应立即检查是否还能分配 `i = 1`。  
  - 计算前缀和时使用整数除法 `//` 防止出现浮点数误差。
- **下次遇到同类题**，第一步应该想到：**“这是一段递增的消耗序列，先求出它的前缀和上界，再按规则逐步模拟”**。这样既保证正确性，又能在复杂度上做出合理的分析。