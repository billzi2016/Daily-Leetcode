# #2105. 浇水植物 II / Watering Plants II

> 难度：中等 · 标签：Array、Two Pointers、Simulation · [LeetCode 链接](https://leetcode.com/problems/watering-plants-ii/)

---

## 题目（英文原版）

**Description**

Alice and Bob want to water n plants in their garden. The plants are arranged in a row and are labeled from 0 to n - 1 from left to right where the ith plant is located at x = i.
Each plant needs a specific amount of water. Alice and Bob have a watering can each, initially full. They water the plants in the following way:
Given a 0-indexed integer array plants of n integers, where plants[i] is the amount of water the ith plant needs, and two integers capacityA and capacityB representing the capacities of Alice's and Bob's watering cans respectively, return the number of times they have to refill to water all the plants.

**Examples**

**Example 1:**

```
Input: plants = [2,2,3,3], capacityA = 5, capacityB = 5
Output: 1
Explanation:
- Initially, Alice and Bob have 5 units of water each in their watering cans.
- Alice waters plant 0, Bob waters plant 3.
- Alice and Bob now have 3 units and 2 units of water respectively.
- Alice has enough water for plant 1, so she waters it. Bob does not have enough water for plant 2, so he refills his can then waters it.
So, the total number of times they have to refill to water all the plants is 0 + 0 + 1 + 0 = 1.
```

**Example 2:**

```
Input: plants = [2,2,3,3], capacityA = 3, capacityB = 4
Output: 2
Explanation:
- Initially, Alice and Bob have 3 units and 4 units of water in their watering cans respectively.
- Alice waters plant 0, Bob waters plant 3.
- Alice and Bob now have 1 unit of water each, and need to water plants 1 and 2 respectively.
- Since neither of them have enough water for their current plants, they refill their cans and then water the plants.
So, the total number of times they have to refill to water all the plants is 0 + 1 + 1 + 0 = 2.
```

**Example 3:**

```
Input: plants = [5], capacityA = 10, capacityB = 8
Output: 0
Explanation:
- There is only one plant.
- Alice's watering can has 10 units of water, whereas Bob's can has 8 units. Since Alice has more water in her can, she waters this plant.
So, the total number of times they have to refill is 0.
```

**Constraints**

- n == plants.length
- 1 <= n <= 105
- 1 <= plants[i] <= 106
- max(plants[i]) <= capacityA, capacityB <= 109

---

## 题目（中文翻译）

Alice 和 Bob 想要给花园里的 **n** 株植物浇水。植物沿一条直线排列，编号从左到右依次为 **0** 到 **n‑1**，其中第 **i** 株植物位于 **x = i**。  
每株植物需要的水量各不相同。Alice 和 Bob 各自拥有一个装满水的浇水壶。两人按如下方式浇水：

给定一个 **0** 起始索引的整数数组 **plants**（长度为 **n**），其中 **plants[i]** 表示第 **i** 株植物需要的水量；再给定两个整数 **capacityA** 与 **capacityB**，分别表示 Alice 和 Bob 的浇水壶容量。返回为浇完所有植物所需的 **加水次数**（即重新装满浇水壶的次数）。

---

## 示例

### 示例 1  
**Input:** `plants = [2,2,3,3]`, `capacityA = 5`, `capacityB = 5`  
**Output:** `1`  
**Explanation:**  
- 初始时，Alice 和 Bob 的浇水壶各有 **5** 单位的水。  
- Alice 浇第 **0** 株植物，Bob 浇第 **3** 株植物。  
- 此时 Alice 剩余 **3** 单位水，Bob 剩余 **2** 单位水。  
- Alice 的水足够浇第 **1** 株植物，于是浇了它。Bob 的水不足以浇第 **2** 株植物，遂 **重新装满** 浇水壶后再浇第 **2** 株植物。  
- 只发生了一次加水。

### 示例 2  
**Input:** `plants = [2,2,3,3]`, `capacityA = 3`, `capacityB = 4`  
**Output:** `2`  
**Explanation:**  
- 初始时，Alice 的浇水壶有 **3** 单位水，Bob 的有 **4** 单位水。  
- Alice 浇第 **0** 株植物，Bob 浇第 **3** 株植物。  
- 两人此时各剩 **1** 单位水，需要分别浇第 **1**、**2** 株植物。  
- 由于两人都没有足够的水，Alice 先 **重新装满**，随后 Bob 也 **重新装满**。  
- 共计两次加水。

### 示例 3  
**Input:** `plants = [5]`, `capacityA = 10`, `capacityB = 8`  
**Output:** `0`  
**Explanation:**  
- 只剩一株植物。  
- Alice 的浇水壶有 **10** 单位水，Bob 的有 **8** 单位水。因为 Alice 的水更多，她直接浇了这株植物。  
- 整个过程没有任何一次加水，故返回 **0**。

---

## 约束条件

- `n == plants.length`
- `1 <= n <= 10^5`
- `1 <= plants[i] <= 10^6`
- `max(plants[i]) <= capacityA, capacityB <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一步一步地模拟** 两个人浇水的全过程：

1. **指针**  
   - `l` 指向 Alice 正在浇的最左边的植物下标（从 `0` 开始）。  
   - `r` 指向 Bob 正在浇的最右边的植物下标（从 `n‑1` 开始）。  
   这两个指针就像两个人在一条直线的两端走向中间，彼此互不干扰。

2. **水罐容量**  
   - `remainA` 保存 Alice 当前水罐里剩余的水量。  
   - `remainB` 保存 Bob 当前水罐里剩余的水量。  
   把水罐想象成 **字典**，`key` 是“剩余水量”，`value` 是“还能浇多少”。  
   当 `remainX < plants[i]`（`X` 为 A 或 B）时，就需要 **“查字典”**，发现水不够，于是 **重新装满**（`remainX = capacityX`），并把 “补水次数” 加一。

3. **浇水过程**  
   - 当 `l < r` 时，Alice 负责 `plants[l]`，Bob 负责 `plants[r]`。  
   - 当 `l == r`（两人来到同一株植物）时，**水量较多的那个人先浇**，如果两人水量相同，任选其一即可。  

4. **结束条件**  
   当 `l > r` 时，所有植物已经被浇完，模拟结束。

> **为什么这个方法一定对？**  
> 我们完全按照题目描述的规则一步一步执行：先检查水够不够，不够就补水，然后消耗对应的水量。只要不漏掉任何一步，最终的 “补水次数” 与真实过程完全一致。

#### 代码（Python）

```python
def wateringPlants(plants, capacityA, capacityB):
    n = len(plants)
    l, r = 0, n - 1                 # 两端的指针
    remainA, remainB = capacityA, capacityB   # 初始各自的水量
    refill = 0                       # 记录补水次数

    while l <= r:                    # 只要还有未浇的植物
        if l == r:                    # 两人碰到同一株
            # 谁的水多谁浇；如果相等随便挑一个
            if remainA >= remainB:
                need = plants[l]
                if remainA < need:   # 不够就补水
                    remainA = capacityA
                    refill += 1
                remainA -= need
            else:
                need = plants[r]
                if remainB < need:
                    remainB = capacityB
                    refill += 1
                remainB -= need
            break                     # 已经浇完最后一株，退出

        # ----- Alice 浇左边的植物 -----
        needA = plants[l]
        if remainA < needA:           # 水不够，需要补水
            remainA = capacityA
            refill += 1
        remainA -= needA
        l += 1                        # 向右移动指针

        # ----- Bob 浇右边的植物 -----
        needB = plants[r]
        if remainB < needB:
            remainB = capacityB
            refill += 1
        remainB -= needB
        r -= 1                        # 向左移动指针

    return refill
```

> 代码里每一行都加了中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度：** `O(n)`  
  “`n` 次循环” 就是遍历每株植物一次。这里的 `O(n)` 并不是说运行时间真的是 `n` 毫秒，而是说 **随着植物数量线性增长，运行时间也会线性增长**。比如 `n` 从 `10` 变到 `100`，大概会慢 `10` 倍。

- **空间复杂度：** `O(1)`  
  只用了常数个变量（指针、剩余水量、计数器），不随 `n` 增长而增大。

---

### 2. 最优解

#### 思路  

暴力解已经是 **一次遍历**，看起来已经很快了。  
真正的“优化点”在于 **不需要额外的循环或数据结构**，只要把两端的指针和水量的更新写得更简洁，就可以把代码压到最短、最易懂，同时仍保持 `O(n)` 与 `O(1)` 的复杂度。

**慢在哪里？**  
- 在 `l == r`（两人碰到同一株）时，我们用了两套几乎相同的代码（分别判断 Alice、Bob），导致代码重复。

**一步步推导优化思路**  

1. **统一处理同一株的情况**  
   当 `l == r` 时，只需要判断 **当前水量更大的那个人** 是否足够。如果不够，直接一次性补满（计数+1），然后结束。这样把原来两套代码合并成一套。

2. **把“检查‑补水‑消耗”抽象成一个小函数**  
   这样可以在左侧和右侧都复用，避免重复代码。函数的核心就是：

   ```python
   def water(need, remain, capacity):
       if remain < need:          # 不够就补水
           remain = capacity
           refill += 1
       remain -= need
       return remain
   ```

3. **使用 **双指针** 的经典写法**  
   - `while l < r:` 只处理 **两端不同** 的情况。  
   - 循环结束后，若 `l == r` 再单独处理一次即可。

4. **核心数据结构**：只需要 **两个指针**、**两个整数**（剩余水量）以及 **一个计数器**。没有额外的数组、栈或哈希表。

> **类比**：想象两个人在走廊的两头走向中间，走到同一个房间时，谁的背包里水多谁先进去。我们只需要记录两个人各自背包里还有多少水，以及他们各自走了多少步——这就是 **双指针**。

#### 代码（Python）

```python
def wateringPlants(plants, capacityA, capacityB):
    n = len(plants)
    l, r = 0, n - 1                 # 左、右指针
    remainA, remainB = capacityA, capacityB
    refill = 0

    # 辅助函数：负责一次浇水（检查‑补水‑消耗）
    def water(need, remain, capacity):
        nonlocal refill
        if remain < need:           # 水不够，需要补水
            remain = capacity
            refill += 1
        remain -= need
        return remain

    # 先处理两端不相同的植物
    while l < r:
        remainA = water(plants[l], remainA, capacityA)
        remainB = water(plants[r], remainB, capacityB)
        l += 1
        r -= 1

    # 如果指针相遇，只剩下一株植物
    if l == r:
        # 谁的水多谁先浇（如果相等，随便挑 Alice）
        if remainA >= remainB:
            remainA = water(plants[l], remainA, capacityA)
        else:
            remainB = water(plants[r], remainB, capacityB)

    return refill
```

> 代码里把 “检查‑补水‑消耗” 抽成了 `water` 函数，逻辑更清晰，重复更少。

#### 复杂度

- **时间复杂度：** `O(n)`  
  仍然只遍历一次所有植物。相较于“暴力解”，我们去掉了重复的 `if l == r` 分支，使常数因子更小，实际运行会更快。

- **空间复杂度：** `O(1)`  
  只使用了固定数量的变量（指针、剩余水量、计数器），不随 `n` 增长。

---

## 心得

- **核心技巧**：**双指针 + 模拟**。  
  双指针让我们可以一次遍历同时处理左侧和右侧的元素，模拟则是严格按照题目规则一步步执行。

- **适用的题型**  
  1. `Planting Flowers`, `Two Sum II - Input array is sorted`（双指针在有序数组中找配对）  
  2. `Queue Reconstruction by Height`（从两端模拟）  
  3. `Boats to Save People`（从两端尽量配对，统计次数）

- **一句话总结解题钥匙**：  
  **把“从左到右”和“从右到左”合在一次循环里，用指针相向而行，遇到同一点时比较谁的资源更多再决定**。

---

## 反思

- **第一反应**：看到“两个角色从两端向中间”立刻想到 **双指针**，于是把整个过程写成 “左指针走、右指针走” 的循环。

- **最容易踩的坑**  
  1. **指针相遇时的处理**：忘记只让水量较多的一方浇最后一株，会导致多计一次补水。  
  2. **补水后忘记把水量恢复到容量**：如果只加了计数而没有把 `remain` 设回 `capacity`，后面的消耗会出错。  
  3. **边界条件**：`n = 1` 时，只有 Alice 或 Bob 浇水，必须提前判断指针是否已经相等。

- **下次类似题的第一步**：  
  先判断是否可以 **用双指针一次遍历**（即两端同时处理），再考虑 **相遇点的特殊规则**，最后把“检查‑补水‑消耗”抽象成一个小函数，避免重复代码。