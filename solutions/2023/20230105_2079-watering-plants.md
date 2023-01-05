# #2079. 浇水植物 / Watering Plants

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/watering-plants/)

---

## 题目（英文原版）

**Description**

You want to water n plants in your garden with a watering can. The plants are arranged in a row and are labeled from 0 to n - 1 from left to right where the ith plant is located at x = i. There is a river at x = -1 that you can refill your watering can at.
Each plant needs a specific amount of water. You will water the plants in the following way:
You are initially at the river (i.e., x = -1). It takes one step to move one unit on the x-axis.
Given a 0-indexed integer array plants of n integers, where plants[i] is the amount of water the ith plant needs, and an integer capacity representing the watering can capacity, return the number of steps needed to water all the plants.

**Examples**

**Example 1:**

```
Input: plants = [2,2,3,3], capacity = 5
Output: 14
Explanation: Start at the river with a full watering can:
- Walk to plant 0 (1 step) and water it. Watering can has 3 units of water.
- Walk to plant 1 (1 step) and water it. Watering can has 1 unit of water.
- Since you cannot completely water plant 2, walk back to the river to refill (2 steps).
- Walk to plant 2 (3 steps) and water it. Watering can has 2 units of water.
- Since you cannot completely water plant 3, walk back to the river to refill (3 steps).
- Walk to plant 3 (4 steps) and water it.
Steps needed = 1 + 1 + 2 + 3 + 3 + 4 = 14.
```

**Example 2:**

```
Input: plants = [1,1,1,4,2,3], capacity = 4
Output: 30
Explanation: Start at the river with a full watering can:
- Water plants 0, 1, and 2 (3 steps). Return to river (3 steps).
- Water plant 3 (4 steps). Return to river (4 steps).
- Water plant 4 (5 steps). Return to river (5 steps).
- Water plant 5 (6 steps).
Steps needed = 3 + 3 + 4 + 4 + 5 + 5 + 6 = 30.
```

**Example 3:**

```
Input: plants = [7,7,7,7,7,7,7], capacity = 8
Output: 49
Explanation: You have to refill before watering each plant.
Steps needed = 1 + 1 + 2 + 2 + 3 + 3 + 4 + 4 + 5 + 5 + 6 + 6 + 7 = 49.
```

**Constraints**

- n == plants.length
- 1 <= n <= 1000
- 1 <= plants[i] <= 106
- max(plants[i]) <= capacity <= 109

---

## 题目（中文翻译）

**描述**  
你想用一个浇水壶为花园中的 `n` 株植物浇水。植物按从左到右的顺序排成一行，编号为 `0` 到 `n - 1`，第 `i` 株植物位于 `x = i`。在 `x = -1` 处有一条河流，你可以在此给浇水壶补水。  
每株植物需要一定量的水。你将按照如下方式浇水：

- 初始时你在河边（即 `x = -1`）。在 `x` 轴上移动一单位需要一步。  
- 给定一个下标从 **0** 开始的整数数组 `plants`，其中 `plants[i]` 表示第 `i` 株植物需要的水量，以及一个整数 `capacity` 表示浇水壶的容量，返回浇完所有植物所需的步数。

**示例 1**  
```
Input: plants = [2,2,3,3], capacity = 5
Output: 14
```
**解释**：从河边带满水开始：

- 步行到植物 0（1 步）并浇水，壶中剩余 3 单位水。  
- 步行到植物 1（1 步）并浇水，壶中剩余 1 单位水。  
- 由于水不足以完整浇灌植物 2，返回河边补水（2 步）。  
- 步行到植物 2（3 步）并浇水……（后续过程同理）。

**示例 2**  
```
Input: plants = [1,1,1,4,2,3], capacity = 4
Output: 30
```
**解释**：从河边带满水开始：

- 浇灌植物 0、1、2（共 3 步），随后返回河边（3 步）。  
- 浇灌植物 3（4 步），返回河边（4 步）。  
- 浇灌植物 4（5 步），返回河边（5 步）。  
- 浇灌植物 5（6 步）。  

所需步数 = 3 + 3 + 4 + 4 + 5 + 5 + 6 = 30。

**示例 3**  
```
Input: plants = [7,7,7,7,7,7,7], capacity = 8
Output: 49
```
**解释**：每浇一株植物都必须先回河边补水。  

所需步数 = 1 + 1 + 2 + 2 + 3 + 3 + 4 + 4 + 5 + 5 + 6 + 6 + 7 = 49。

**约束条件**  

- `n == plants.length`  
- `1 <= n <= 1000`  
- `1 <= plants[i] <= 10^6`  
- `max(plants[i]) <= capacity <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是 **“一步步走”**：  
- 把自己想象成一个人在坐标轴上行走，左边的河流在 `x = -1`，第 `i` 株植物就在 `x = i`。  
- 每走一步（左或右）都记一次步数。  
- 手里装的水罐容量是 `capacity`，每次给植物浇水就把罐子里的水减掉对应的需求。  
- 当罐子里的水不足以满足当前植物的需求时，就 **一步一步** 往左走回河流 (`x = -1`)，把水罐补满，然后再一步一步走回去继续浇水。  

这就像我们在玩 “走格子” 的游戏：每走一格记一次分，水罐就像背包里的物品，装满后才可以继续前进。  

> **为什么这种方法一定能得到正确答案？**  
> 因为它严格按照题目描述的“每走一格算一步、遇到水不够就回河补满”来模拟，所有可能的走法都被完整地复制了，最终得到的步数就是题目要求的最少步数。

#### 代码（Python）

```python
def steps_brute(plants, capacity):
    # 当前位置，初始在河边 -1
    pos = -1
    # 罐子里剩余的水，初始装满
    water = capacity
    # 累计步数
    steps = 0

    for i, need in enumerate(plants):
        # 先走到第 i 株植物（一步一步走）
        while pos < i:          # 这里是逐格前进，模拟每一步
            pos += 1
            steps += 1

        # 如果罐子里的水不够浇当前植物，就回河补水
        if water < need:
            # 逐格返回河流
            while pos > -1:
                pos -= 1
                steps += 1
            water = capacity      # 在河边把水罐装满

            # 再一步一步走回第 i 株植物
            while pos < i:
                pos += 1
                steps += 1

        # 给第 i 株植物浇水
        water -= need

    return steps
```

> **关键行中文注释**  
> - `while pos < i:`  模拟“向右走”到达目标植物。  
> - `while pos > -1:`  模拟“向左走”回到河边。  
> - `water = capacity`  在河边把水罐重新装满。

#### 复杂度  

- **时间复杂度：** `O(total_steps)`。  
  - 这里的 `total_steps` 是实际走的格子数，最坏情况下等价于答案本身（可能达到 `O(n·capacity)`），远大于 `n`。  
  - 用大白话说，就是“每走一步都要循环一次”，如果答案是几千步，代码就会循环几千次，甚至更大。  
- **空间复杂度：** `O(1)`。只用了常数个变量来记录位置、剩余水量和步数。

---

### 2. 最优解  

#### 思路  

虽然上面的“逐格走”能得到正确答案，但 **步数本身已经是题目要返回的结果**，我们不需要真的去“一格一格”数，而只需要**直接算出每一次往返的距离**。  

从暴力解可以看到，真正消耗步数的只有两类动作：

1. **从当前位置直接走到下一株植物**，距离就是 `i - cur`（`cur` 为上一次结束时的坐标）。  
2. **当水不够时，需要回河 (`x = -1`) 再回来**，这一次往返的距离是 `2 * (i + 1)`：  
   - 从第 `i` 株植物回到河需要 `i + 1` 步（因为河在 `-1`），  
   - 再从河走到第 `i` 株植物又要 `i + 1` 步。  

因此，我们可以在一次遍历 `plants` 的过程中，**只记录当前位置**（其实始终是 `i`），**只在水不够时加上一次往返的距离**，不必真的“走回去”。  

核心思路可以类比为 **“把每一次往返的路程提前算好”**，就像在旅行前先算好往返机票的费用，而不是每到一个机场再去排队买票。

#### 代码（Python）

```python
def steps_optimal(plants, capacity):
    steps = 0          # 累计步数
    water = capacity   # 罐子里剩余的水，初始装满

    for i, need in enumerate(plants):
        # 走到第 i 株植物的步数，直接加上距离 (i - (i-1)) = 1
        # 其实每次向右走一步，所以可以统一累加 1
        steps += 1

        # 如果罐子里的水不够浇这株植物
        if water < need:
            # 回河再回来，一次往返的距离是 2 * (i + 1)
            steps += 2 * i   # 已经走了 i 步到达植物，这里加上回河再回来的额外步数
            water = capacity  # 在河边重新装满

        # 给第 i 株植物浇水
        water -= need

    return steps
```

> **关键行中文注释**  
> - `steps += 1`  每处理一株植物，必然向右移动一步（从 `i-1` 到 `i`）。  
> - `steps += 2 * i` 当水不够时，**额外** 加上一次往返的距离：`i` 步回河 + `i` 步再回来。  
> - `water = capacity` 在河边把水罐重新装满。

> **为什么 `steps += 2 * i` 而不是 `2 * (i+1)`？**  
> 因为在进入本轮循环时已经算过一次向右走到第 `i` 株植物的步（`steps += 1`），所以往返只需要再加上 “回到河再走回来的” 距离，即 `i` 步回去 + `i` 步回来 = `2*i`。

#### 复杂度  

- **时间复杂度：** `O(n)`。只遍历一次数组，常数时间完成每一步的计算。  
  - 与暴力解相比，省去了 “每走一步都循环一次” 的开销，答案的大小不再影响运行时间。  
- **空间复杂度：** `O(1)`。只用了几个整数变量。

---

## 心得  

- **核心技巧**：**把“模拟过程”中的每一次往返距离直接算出来**，而不是逐格移动。  
- **适用的题型**：  
  1. **需要往返补给的模拟题**（如 LeetCode 1749 *“Warehouse Keeper”* 类似思路）。  
  2. **在一维坐标系上来回移动的贪心题**（如 1656 *“Design an Ordered Stream”* 中的下标跳转）。  
  3. **需要累计距离但不必真的走路的题**（如 1498 *“Number of Subsequences That Satisfy the Given Sum Condition”* 的双指针累计）。  
- **一句话总结解题钥匙**：**把“走路”抽象成“距离”，只在必要时加上往返的距离即可**。

---

## 反思  

- **第一反应**：看到“走一步算一步”，直接写了逐格循环的模拟代码。  
- **最容易踩的坑**：  
  - 忘记在 “回河再回来” 时把已经算过的那一步去掉，导致往返距离多加了 `+2`。  
  - 没有处理 **最后一株植物** 后不需要再回河的情况（本题不需要返回河，直接结束）。  
- **下次遇到同类题**，第一步应该想到：**先把每一次“往返”抽象为固定的距离公式，再累加**，而不是一步步模拟。这样既直观又高效。