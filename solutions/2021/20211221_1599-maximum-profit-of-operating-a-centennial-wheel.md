# #1599. 运营摩天轮的最大利润 / Maximum Profit of Operating a Centennial Wheel

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/maximum-profit-of-operating-a-centennial-wheel/)

---

## 题目（英文原版）

**Description**

You are the operator of a Centennial Wheel that has four gondolas, and each gondola has room for up to four people. You have the ability to rotate the gondolas counterclockwise, which costs you runningCost dollars.
You are given an array customers of length n where customers[i] is the number of new customers arriving just before the ith rotation (0-indexed). This means you must rotate the wheel i times before the customers[i] customers arrive. You cannot make customers wait if there is room in the gondola. Each customer pays boardingCost dollars when they board on the gondola closest to the ground and will exit once that gondola reaches the ground again.
You can stop the wheel at any time, including before serving all customers. If you decide to stop serving customers, all subsequent rotations are free in order to get all the customers down safely. Note that if there are currently more than four customers waiting at the wheel, only four will board the gondola, and the rest will wait for the next rotation.
Return the minimum number of rotations you need to perform to maximize your profit. If there is no scenario where the profit is positive, return -1.

**Examples**

**Example 1:**

```
Input: customers = [8,3], boardingCost = 5, runningCost = 6
Output: 3
Explanation: The numbers written on the gondolas are the number of people currently there.
1. 8 customers arrive, 4 board and 4 wait for the next gondola, the wheel rotates. Current profit is 4 * $5 - 1 * $6 = $14.
2. 3 customers arrive, the 4 waiting board the wheel and the other 3 wait, the wheel rotates. Current profit is 8 * $5 - 2 * $6 = $28.
3. The final 3 customers board the gondola, the wheel rotates. Current profit is 11 * $5 - 3 * $6 = $37.
The highest profit was $37 after rotating the wheel 3 times.
```

**Example 2:**

```
Input: customers = [10,9,6], boardingCost = 6, runningCost = 4
Output: 7
Explanation:
1. 10 customers arrive, 4 board and 6 wait for the next gondola, the wheel rotates. Current profit is 4 * $6 - 1 * $4 = $20.
2. 9 customers arrive, 4 board and 11 wait (2 originally waiting, 9 newly waiting), the wheel rotates. Current profit is 8 * $6 - 2 * $4 = $40.
3. The final 6 customers arrive, 4 board and 13 wait, the wheel rotates. Current profit is 12 * $6 - 3 * $4 = $60.
4. 4 board and 9 wait, the wheel rotates. Current profit is 16 * $6 - 4 * $4 = $80.
5. 4 board and 5 wait, the wheel rotates. Current profit is 20 * $6 - 5 * $4 = $100.
6. 4 board and 1 waits, the wheel rotates. Current profit is 24 * $6 - 6 * $4 = $120.
7. 1 boards, the wheel rotates. Current profit is 25 * $6 - 7 * $4 = $122.
The highest profit was $122 after rotating the wheel 7 times.
```

**Example 3:**

```
Input: customers = [3,4,0,5,1], boardingCost = 1, runningCost = 92
Output: -1
Explanation:
1. 3 customers arrive, 3 board and 0 wait, the wheel rotates. Current profit is 3 * $1 - 1 * $92 = -$89.
2. 4 customers arrive, 4 board and 0 wait, the wheel rotates. Current profit is 7 * $1 - 2 * $92 = -$177.
3. 0 customers arrive, 0 board and 0 wait, the wheel rotates. Current profit is 7 * $1 - 3 * $92 = -$269.
4. 5 customers arrive, 4 board and 1 waits, the wheel rotates. Current profit is 11 * $1 - 4 * $92 = -$357.
5. 1 customer arrives, 2 board and 0 wait, the wheel rotates. Current profit is 13 * $1 - 5 * $92 = -$447.
The profit was never positive, so return -1.
```

**Constraints**

- n == customers.length
- 1 <= n <= 105
- 0 <= customers[i] <= 50
- 1 <= boardingCost, runningCost <= 100

---

## 题目（中文翻译）

你是拥有四个舱位（gondola）的摩天轮的运营者，每个舱位最多可容纳四人。你可以逆时针旋转舱位，每转一次需要支付 `runningCost` 美元。

给定长度为 `n` 的数组 `customers`，其中 `customers[i]` 表示在第 `i` 次旋转（下标从 0 开始）之前到达的新顾客数量。这意味着在第 `i` 次旋转之前必须先进行 `i` 次旋转，之后才会有 `customers[i]` 位顾客到达。只要舱位还有空位，你不能让顾客等待。每位顾客在登上最靠近地面的舱位时支付 `boardingCost` 美元，并在该舱位再次到达地面时下车。

你可以在任意时刻停止旋转，包括在未服务完所有顾客之前。如果决定停止服务，则后续的所有旋转都是免费的，以确保所有顾客安全下车。注意，如果当前等待的顾客数量超过四人，则只有四人能够登上舱位，其余顾客需等待下一次旋转。

返回为使利润最大化所需执行的最少旋转次数。如果不存在利润为正的情况，返回 `-1`。

### 示例

#### 示例 1
```text
Input: customers = [8,3], boardingCost = 5, runningCost = 6
Output: 3
Explanation: 圆盘上数字表示当前舱位中的人数。
1. 8 位顾客到达，4 人登舱，剩余 4 人等待下一舱，轮子旋转一次。当前利润为 4 × $5 - 1 × $6 = $14。
2. 3 位顾客到达，之前等待的 4 人登舱，另外 3 人继续等待，轮子再次旋转。当前利润为 8 × $5 - 2 × $6 = $28。
3. 3 位等待的顾客登舱，轮子再旋转一次后结束。此时累计利润最高，所需最少旋转次数为 3。
```

#### 示例 2
```text
Input: customers = [10,9,6], boardingCost = 6, runningCost = 4
Output: 7
Explanation:
1. 10 位顾客到达，4 人登舱，6 人等待，轮子旋转一次。当前利润为 4 × $6 - 1 × $4 = $20。
2. 9 位顾客到达，之前等待的 6 人加上新到的 9 人中有 4 人登舱，剩余 11 人等待，轮子旋转一次。当前利润为 8 × $6 - 2 × $4 = $40。
3. 最后 6 位顾客到达，4 人登舱，剩余顾客继续等待，随后继续旋转，直至累计利润达到最大值。此时最少需要 7 次旋转。
```

#### 示例 3
```text
Input: customers = [3,4,0,5,1], boardingCost = 1, runningCost = 92
Output: -1
Explanation:
1. 3 位顾客到达，全部登舱，轮子旋转一次。当前利润为 3 × $1 - 1 × $92 = -$89。
2. 4 位顾客到达，全部登舱，轮子再旋转一次。当前利润为 7 × $1 - 2 × $92 = -$177。
3. 0 位顾客到达，轮子继续旋转。累计利润仍为负数，后续无论如何操作都无法使利润转正，故返回 -1。
```

### 约束条件
- `n == customers.length`
- `1 <= n <= 10^5`
- `0 <= customers[i] <= 50`
- `1 <= boardingCost, runningCost <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题本质上是**模拟**：  
- 每转动一次，最多让 4 个人上车（因为每个舱位只能坐 4 人）。  
- 上车的乘客会付 `boardingCost`，转动一次需要花 `runningCost`。  
- 新的顾客会在第 `i` 次转动 **之前** 到达。  

我们可以把“等待的顾客数”当作一个**计数器**，每轮：

1. 把 `customers[i]`（如果还有 i）加入等待队列。  
2. 从等待队列中取走 `min(waiting, 4)` 个人上车，记作 `board`。  
3. 更新利润 `profit += board * boardingCost - runningCost`。  
4. 记录下 **当前轮数**（从 1 开始计）以及 **最高利润** 和 **第一次出现最高利润的轮数**。  

如果所有 `customers` 已经全部到达，但还有人等待，我们就继续“空转”——只取走最多 4 人，直到等待数为 0 为止。

**为什么正确？**  
每一次转动的行为都是唯一决定的：  
- 等待人数只能增不能减（只能被上车的那部分减）。  
- 费用和收入都是线性累加的。  
因此只要按顺序一步步执行，就一定得到真实的利润曲线。  

**暴力写法的缺点**  
如果我们想“尝试在每一轮停下来”，最直接的做法是：  
- 对每个可能的停转轮数 `k`，重新从头算一遍利润。  
- 这相当于在每次循环里再次遍历前面的所有转动，时间会变成 **O(R²)**（`R` 为实际需要转动的次数），在最坏情况下会超时。

#### 代码（Python）

```python
def minOperationsMaxProfit_bruteforce(customers, boardingCost, runningCost):
    # 所有可能的转动次数上限：把所有人全部上车后再多转几次让剩余的人走完
    total_people = sum(customers)
    max_rotations = (total_people + 3) // 4 + len(customers)   # 一个保守的上界

    best_profit = float('-inf')
    best_rot = -1

    # 对每一个可能的停转轮数 k 重新计算利润
    for k in range(1, max_rotations + 1):
        waiting = 0          # 当前等待的人数
        profit = 0           # 累计利润

        for i in range(k):
            # 第 i 次转动前（i 从 0 开始），如果还有新客到达则加入等待
            if i < len(customers):
                waiting += customers[i]

            # 本轮上车人数，最多 4 人
            board = min(waiting, 4)
            waiting -= board

            # 收入 - 成本
            profit += board * boardingCost - runningCost

        # 记录最大利润以及第一次出现的转动次数
        if profit > best_profit:
            best_profit = profit
            best_rot = k

    return best_rot if best_profit > 0 else -1
```

> **关键行中文注释**  
> - `waiting += customers[i]`：把新来的顾客加入“等车队”。  
> - `board = min(waiting, 4)`：每轮只能坐 4 人，取最少的那个。  
> - `profit += board * boardingCost - runningCost`：本轮的净赚。  

#### 复杂度  

- **时间复杂度**：`O(R²)`，其中 `R` 为实际需要的转动次数（最坏约为 1.3 × 10⁶），因为外层遍历每个可能的停转点，内层重新模拟全部转动。用大白话说，就是“每次都从头重新算”。  
- **空间复杂度**：`O(1)`，只用了几个整数计数器，不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**每一次转动的利润都是可以累加的**，不需要每次都重新从头算。只要我们在一次遍历中**实时维护**：

1. `waiting` —— 当前还有多少人等着上车。  
2. `profit` —— 到目前为止累计的净利润。  
3. `maxProfit` 与 `answerRot` —— 记录出现最高利润时的轮数（第一次出现）。  

遍历的顺序：

| 步骤 | 说明 |
|------|------|
| **①** | 把本轮（第 `i` 次）到达的新客加入 `waiting`（如果 `i` 仍在 `customers` 范围内）。 |
| **②** | 让 `min(waiting, 4)` 人上车，`waiting` 减去上车人数。 |
| **③** | 计算本轮的利润变化 `board * boardingCost - runningCost` 并累加到 `profit`。 |
| **④** | 如果 `profit` 超过历史最高值，更新 `maxProfit` 与 `answerRot = currentTurn`。 |
| **⑤** | 当所有 `customers` 都已经到达且 `waiting == 0` 时，模拟结束。否则继续“空转”——只执行步骤 ②~④，直到 `waiting` 为 0。 |

**瓶颈在哪里？**  
暴力解的瓶颈是**重复计算**。只要把累计的 `profit` 保留下来，每转动一次只做 **O(1)** 的工作，就能得到完整的利润曲线。  

**核心算法**：一次线性**模拟**（simulation），时间与实际转动次数成正比。因为每轮最多处理 4 人，转动次数上限约为 `sum(customers)/4 + n`，在题目约束下最多约 **1.3 × 10⁶**，完全可以在一秒内跑完。  

**类比**：把转动过程想象成在收银台排队结账：  
- “等待人数” 就是排队的人数。  
- 每次只能叫 4 个人进去付钱（上车），然后收钱并扣掉转动成本。  
- 我们只需要记下每一次收完钱后的累计盈亏，就能随时知道哪一刻是最赚钱的。

#### 代码（Python）

```python
def minOperationsMaxProfit(customers, boardingCost, runningCost):
    """
    返回在利润最大时所需的最少转动次数；若最大利润 ≤ 0，返回 -1。
    """
    waiting = 0          # 当前等待上车的人数
    profit = 0           # 累计利润
    maxProfit = float('-inf')
    answerRot = -1       # 记录第一次出现 maxProfit 的转动次数
    turn = 0             # 已经转动的次数（从 1 开始计数）

    i = 0                # customers 数组的指针
    n = len(customers)

    # 只要还有新客未到达 或者 还有人等待，就继续转动
    while i < n or waiting > 0:
        # 1️⃣ 新客到达（如果还有的话）
        if i < n:
            waiting += customers[i]
            i += 1

        # 2️⃣ 本轮上车人数（最多 4 人）
        board = min(waiting, 4)
        waiting -= board

        # 3️⃣ 本轮产生的利润：收入 - 成本
        profit += board * boardingCost - runningCost
        turn += 1  # 本轮已经完成，转动次数加 1

        # 4️⃣ 更新最大利润及对应的转动次数
        if profit > maxProfit:
            maxProfit = profit
            answerRot = turn

    # 如果最高利润仍然不大于 0，按照题目要求返回 -1
    return answerRot if maxProfit > 0 else -1
```

> **关键行中文注释**  
> - `waiting += customers[i]`：把第 `i` 轮新来的顾客加入等车队。  
> - `board = min(waiting, 4)`：每转动一次只能让 4 个人上车。  
> - `profit += board * boardingCost - runningCost`：本轮净赚（收入减去转动成本）。  
> - `if profit > maxProfit:`：只要当前累计利润超过历史最高，就记录此时的转动次数。  

#### 复杂度  

- **时间复杂度**：`O(R)`，`R` 为实际转动次数（≈ `sum(customers)/4 + n`），在最坏情况下约 1.3 × 10⁶，属于线性时间。可以用大白话说成“每转动一次只做几件事”，所以整体跑得很快。  
- **空间复杂度**：`O(1)`，只用了常数个整数变量，和输入规模无关。

---

## 心得  

- **核心技巧**：一次遍历的**累计模拟**（把每一步的结果保留下来，而不是每次都重新计算）。  
- **适用题型**：  
  1. “出租车接客”“公交车上下客”类的**排队/等待**模拟（如 LeetCode 1700. Number of Students Unable to Eat Lunch）。  
  2. “生产线”或“机器加工”每轮产生固定收益/固定成本的**利润最大化**问题。  
- **一句话总结**：**累计利润 + 只在利润刷新时记录转数**，就是这道题的解题钥匙。  

---

## 反思  

- **第一反应**：看到“每转动一次上车人数最多 4，收入/成本固定”，立刻想到**模拟**。  
- **最容易踩的坑**：  
  - 忘记在所有顾客到达后仍需继续转动直到 `waiting == 0`（否则会少算最后几轮的利润）。  
  - 把“利润为 0”误判为“有正收益”，题目要求返回 `-1` 当最大利润**不大于 0**。  
  - 边界条件：`customers` 可能全是 `0`，此时应直接返回 `-1`。  
- **下次遇到同类题**，第一步应该想到**“用一个变量记录累计状态（等待人数、累计利润）”，然后在每一步更新并检查是否刷新最佳”。这样可以把复杂的枚举过程化简为一次线性遍历。