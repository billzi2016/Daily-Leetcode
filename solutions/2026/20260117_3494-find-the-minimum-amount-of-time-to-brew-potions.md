# #3494. 寻找酿造药水的最小时间 / Find the Minimum Amount of Time to Brew Potions

> 难度：中等 · 标签：Array、Simulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays, skill and mana, of length n and m, respectively.
In a laboratory, n wizards must brew m potions in order. Each potion has a mana capacity mana[j] and must pass through all the wizards sequentially to be brewed properly. The time taken by the ith wizard on the jth potion is timeij = skill[i] * mana[j].
Since the brewing process is delicate, a potion must be passed to the next wizard immediately after the current wizard completes their work. This means the timing must be synchronized so that each wizard begins working on a potion exactly when it arrives. ​
Return the minimum amount of time required for the potions to be brewed properly.

**Examples**

**Example 1:**

```
Input: skill = [1,5,2,4], mana = [5,1,4,2]
Output: 110
Explanation:
As an example for why wizard 0 cannot start working on the 1 st potion before time t = 52 , consider the case where the wizards started preparing the 1 st potion at time t = 50 . At time t = 58 , wizard 2 is done with the 1 st potion, but wizard 3 will still be working on the 0 th potion till time t = 60 .
```

**Example 2:**

```
Input: skill = [1,1,1], mana = [1,1,1]
Output: 5
Explanation:
```

**Example 3:**

```
Input: skill = [1,2,3,4], mana = [1,2]
Output: 21
```

**Constraints**

- n == skill.length
- m == mana.length
- 1 <= n, m <= 5000
- 1 <= mana[i], skill[i] <= 5000

---

## 题目（中文翻译）

你得到两个整数数组，skill 和 mana，长度分别为 n 和 m。  
在实验室中，n 位巫师必须按顺序酿造 m 种药水。每种药水的法力容量为 mana[j]，并且必须依次经过所有巫师才能正确酿造。第 i 位巫师酿造第 j 种药水所需的时间为  

```
timeij = skill[i] * mana[j]
```

由于酿造过程十分精细，药水在当前巫师完成工作后必须立刻传递给下一位巫师。这意味着时间必须同步，使得每位巫师在药水到达的瞬间立即开始工作。  
返回所有药水能够正确酿造所需的最少总时间。

### 示例

#### 示例 1
``` 
Input: skill = [1,5,2,4], mana = [5,1,4,2]
Output: 110
Explanation:
例如，巫师 0 在时间 t = 52 之前不能开始酿造第 1 瓶药水。设想巫师们在时间 t = 50 开始准备第 1 瓶药水。  
在时间 t = 58，巫师 2 完成了第 1 瓶药水的酿造，但此时巫师 3 仍在酿造第 0 瓶药水，直到时间 t = 60 才完成。
```

#### 示例 2
``` 
Input: skill = [1,1,1], mana = [1,1,1]
Output: 5
Explanation:
（此处略去详细说明，仅展示结果。）
```

#### 示例 3
``` 
Input: skill = [1,2,3,4], mana = [1,2]
Output: 21
Explanation:
（此处略去详细说明，仅展示结果。）
```

### 约束条件
- n == skill.length
- m == mana.length
- 1 ≤ n, m ≤ 5000
- 1 ≤ mana[i], skill[i] ≤ 5000

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
我们把 **药水** 看成 **任务**，把 **巫师** 看成 **机器**。  
每个任务必须依次在 `0 → 1 → … → n‑1` 号机器上加工，  
第 `i` 台机器加工第 `j` 件任务的时间为  

```
time[i][j] = skill[i] * mana[j]
```

最直接的想法是：  

1. 按照题目顺序一个一个把药水送进实验室。  
2. 对于当前药水 `j`，遍历所有巫师 `i`，  
   - 先看它前一位巫师 `i‑1` 何时把药水 `j` 处理完（如果 `i==0` 则视为 0），  
   - 再看第 `i` 位巫师自己何时空闲（即上一瓶药水在它这里结束的时间），  
   - 两者取 **较大值**，因为药水必须等到两件事都准备好才能开始。  
   - 加上本次加工时间 `skill[i] * mana[j]`，得到第 `i` 位巫师在药水 `j` 上的结束时间。  

把每一步的结束时间都记录下来，最后第 `n‑1` 位巫师完成第 `m‑1` 瓶药水的时间，就是总耗时。

> **生活化类比**：  
> 想象有 `n` 条传送带，药水是装在小车里的货物。每条传送带上都有一个工人，工人的工作效率是 `skill[i]`，货物的重量是 `mana[j]`。工人处理一辆车需要的时间就是 “效率 × 重量”。车子只能在前一个工人完全处理完后才可以进入下一个工人手里。我们只要一步步记录每个工人什么时候空闲，什么时候可以接到下一辆车，就能算出所有车子全部出厂的时间。

**为什么这个方法一定能得到正确答案？**  
因为我们严格遵守了题目给出的唯一约束：

- 药水必须按顺序经过所有巫师，且不能出现“提前”或“等候”之外的调度。  
- 每个巫师只能在自己空闲且药水已经从前一个巫师那里到达时才开始工作。  

只要每一步都取 `max(前一巫师结束时间, 本巫师空闲时间)`，就恰好模拟了真实的流水线运行过程，所以答案必然正确。

**时间/空间复杂度**  

- **时间**：外层遍历 `m` 瓶药水，内层遍历 `n` 位巫师，还要在每一次内部循环里**再遍历一次**所有已经处理过的药水去找本巫师的空闲时间（如果不使用额外记忆的话），这会导致 **O(n·m²)** 的时间。  
  - `O(n·m²)` 可以理解为：如果 `n = m = 5000`，最坏情况下要做约 `5 000 × 5 000² = 125 亿` 次基本运算，显然会超时。  

- **空间**：只需要保存每位巫师的最新空闲时间，`O(n)` 的额外空间。

#### 代码（Python）  

```python
# 暴力实现：每次都遍历所有已经完成的药水来找巫师的空闲时间
def min_time_bruteforce(skill, mana):
    n, m = len(skill), len(mana)
    # f[i][j] 表示第 i 位巫师完成第 j 瓶药水的时间（这里全用二维列表存，直观但浪费空间）
    f = [[0] * m for _ in range(n)]

    # 第 0 位巫师的完成时间可以直接累加
    for j in range(m):
        prev = f[0][j - 1] if j > 0 else 0          # 前一瓶药水在这位巫师的结束时间
        f[0][j] = prev + skill[0] * mana[j]        # 直接加工

    # 其余巫师
    for i in range(1, n):
        for j in range(m):
            # 前一位巫师处理完这瓶药水的时间
            from_prev_wizard = f[i - 1][j]
            # 本巫师自己上一次处理的药水结束时间
            self_free = f[i][j - 1] if j > 0 else 0
            start = max(from_prev_wizard, self_free)   # 必须等两件事都准备好
            f[i][j] = start + skill[i] * mana[j]

    # 最后一个巫师处理完最后一瓶药水的时间即为答案
    return f[n - 1][m - 1]
```

> 代码里每一行都有中文注释，帮助你对照思路。  
> 这里使用了二维数组 `f`，直观但会占用 `O(n·m)` 的空间，实际运行时会非常慢。

#### 复杂度  

- **时间复杂度**：`O(n·m²)`  
  - “平方”意味着如果你把任务数想成排队的车子，巫师每次都要回头去检查所有已经离开的车子，这会让时间呈二次增长。  

- **空间复杂度**：`O(n·m)`（存所有中间结束时间）  
  - 实际上只需要上一行的信息就可以，后面会进一步压缩到 `O(n)`。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要去“翻看”所有已经处理完的药水来找本巫师的空闲时间。  
实际上我们只需要 **每位巫师最近一次的空闲时间**，不必记住所有历史记录。  

设 `free[i]` 为第 `i` 位巫师在 **上一瓶药水** 完成后立即空闲的时间（即该巫师的“下班时间”）。  
处理第 `j` 瓶药水（容量 `x = mana[j]`）的步骤：

1. **从第 0 位巫师开始**：  
   - `now = free[0]`（第 0 位巫师已经空闲的时间）  
2. **依次遍历其余巫师**（`i = 1 … n-1`）：  
   - 前一位巫师完成这瓶药水的时间是 `now + skill[i-1] * x`（因为 `now` 表示前一位巫师刚开始加工的时间）。  
   - 本位巫师自己可能还在忙上一瓶药水，空闲时间是 `free[i]`。  
   - 所以本位巫师真正的 **开始时间** 必须是两者的最大值：  

     ```
     now = max(now + skill[i-1] * x, free[i])
     ```

   - 完成时间则是 `now + skill[i] * x`，但我们暂时只更新 `now` 为开始时间，待循环结束后再统一计算。

3. **循环结束后**，第 `n‑1` 位巫师的完成时间即为  

   ```
   finish = now + skill[n-1] * x
   ```

   这就是本瓶药水的 **最终完成时间**，也应该写回 `free[n-1]`。

4. **更新其余巫师的 free 值**  
   - 为了让下一瓶药水的模拟继续使用，只需要把每位巫师的空闲时间往前推一个步骤。  
   - 观察可以得到：

     ```
     free[i] = finish - sum_{k=i+1}^{n-1} skill[k] * x
     ```

   - 直接使用逆向更新的方式更方便：

     ```
     for i = n-2 … 0:
         free[i] = free[i+1] - skill[i+1] * x
     ```

   - 这样，`free` 数组始终保持“上一瓶药水结束后，各巫师的空闲时间”。  

整个过程对每瓶药水只遍历一次 `n` 位巫师，时间 **O(n·m)**，空间只需 `O(n)`。

> **核心概念解释**  
> - **max**：表示两件事谁慢等谁。比如你在排队买咖啡，只有当咖啡机空闲且你手里已经拿到咖啡券时才能开始点单，这里取两者的最大值。  
> - **前缀和 / 逆向更新**：我们不想每次都把所有 `skill * x` 累加，可以从后往前把已经算好的总时间减去当前巫师的加工时间，得到前一位巫师的空闲时间。类似于在数轴上往左走一步，走的距离就是当前巫师的加工时长。  

#### 代码（Python）  

```python
def min_time_optimal(skill, mana):
    """
    skill : List[int]   # 巫师的效率
    mana  : List[int]   # 药水的容量
    返回值为所有药水全部酿造完毕的最小时间
    """
    n = len(skill)
    # free[i] 表示第 i 位巫师在“上一瓶药水”完成后空闲的时间
    free = [0] * n          # 初始时所有巫师都在时间 0 时空闲

    for x in mana:          # 逐瓶药水处理
        # 第 0 位巫师直接在自己的空闲时间开始
        now = free[0]

        # 依次让后面的巫师接手
        for i in range(1, n):
            # 前一位巫师加工完这瓶药水的时间
            finish_prev = now + skill[i - 1] * x
            # 本位巫师自己的空闲时间
            now = max(finish_prev, free[i])   # 必须等两件事都准备好

        # 第 n-1 位巫师的完成时间
        finish = now + skill[n - 1] * x
        free[n - 1] = finish                # 更新最后一位的空闲时间

        # 逆向更新其余巫师的空闲时间
        for i in range(n - 2, -1, -1):
            free[i] = free[i + 1] - skill[i + 1] * x

    # 所有药水结束后，最后一位巫师的空闲时间即为答案
    return free[-1]
```

> 关键行中文解释：  
> - `now = free[0]`      # 第 0 位巫师从自己空闲的时间开始工作。  
> - `finish_prev = now + skill[i-1] * x` # 前一位巫师加工完当前药水的时间。  
> - `now = max(finish_prev, free[i])`  # 本位巫师只能在两者都准备好后才开始。  
> - `finish = now + skill[n-1] * x`   # 最后一位巫师的完成时间。  
> - `free[i] = free[i+1] - skill[i+1] * x` # 逆向推导每位巫师的空闲时间。  

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 这里的 `n·m` 就是把每瓶药水“走”一遍所有巫师的总次数。  
  - 与暴力解的 `O(n·m²)` 相比，省掉了每瓶药水内部的二次遍历，跑得快几百倍。  

- **空间复杂度**：`O(n)`  
  - 只需要保存 `free` 数组，大小等于巫师数量。  
  - 与暴力解的 `O(n·m)`（甚至 `O(n·m²)`）相比，节省了大量内存。

---

## 心得  

- **核心技巧**：使用 **每台机器的最早空闲时间**（`free`）配合 **max** 来同步流水线，再通过 **逆向差分**（`free[i] = free[i+1] - …`）快速更新。  
- **适用题型**（类似思路）  
  1. **流水线排程**（Flow Shop Scheduling）——如 LeetCode 1977 “Minimum Time to Complete Trips”。  
  2. **生产线同步**——比如 “Parallel Courses III” 中的最长路径/拓扑排序。  
  3. **多机加工**——如 “Minimum Time to Finish All Jobs” 这类需要记录机器空闲时间的题目。  
- **一句话总结**：  
  > “只要记录每个巫师上一次结束的时间，用 `max` 把前后两道工序同步，逆向差分即可得到下一轮的起始时间。”

---

## 反思  

- **第一反应**：看到 `skill[i] * mana[j]`，本能想到两层循环直接相乘求和，以为只能 O(n·m²)。  
- **最容易踩的坑**  
  - **边界条件**：`free[0]` 初始为 `0`，否则会多加一个无意义的等待。  
  - **整数溢出**：在 Python 中不怕，但在 C++/Java 需要用 `long long`。  
  - **逆向更新公式写错**：`free[i] = free[i+1] - skill[i+1] * x`，如果把 `+` 写成 `-` 或者忘记乘以当前 `x`，答案会偏大。  
- **下次类似题的第一步**：  
  - **先把每台机器的空闲时间列出来**（`free`），然后用 `max(prev_finish, free[i])` 同步，最后再想怎么在 O(1) 时间内更新 `free`。  

祝你玩得开心，算法之路一步一个脚印！