# #2383. 最少训练时间以赢得比赛 / Minimum Hours of Training to Win a Competition

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-hours-of-training-to-win-a-competition/)

---

## 题目（英文原版）

**Description**

You are entering a competition, and are given two positive integers initialEnergy and initialExperience denoting your initial energy and initial experience respectively.
You are also given two 0-indexed integer arrays energy and experience, both of length n.
You will face n opponents in order. The energy and experience of the ith opponent is denoted by energy[i] and experience[i] respectively. When you face an opponent, you need to have both strictly greater experience and energy to defeat them and move to the next opponent if available.
Defeating the ith opponent increases your experience by experience[i], but decreases your energy by energy[i].
Before starting the competition, you can train for some number of hours. After each hour of training, you can either choose to increase your initial experience by one, or increase your initial energy by one.
Return the minimum number of training hours required to defeat all n opponents.

**Examples**

**Example 1:**

```
Input: initialEnergy = 5, initialExperience = 3, energy = [1,4,3,2], experience = [2,6,3,1]
Output: 8
Explanation: You can increase your energy to 11 after 6 hours of training, and your experience to 5 after 2 hours of training.
You face the opponents in the following order:
- You have more energy and experience than the 0th opponent so you win.
  Your energy becomes 11 - 1 = 10, and your experience becomes 5 + 2 = 7.
- You have more energy and experience than the 1st opponent so you win.
  Your energy becomes 10 - 4 = 6, and your experience becomes 7 + 6 = 13.
- You have more energy and experience than the 2nd opponent so you win.
  Your energy becomes 6 - 3 = 3, and your experience becomes 13 + 3 = 16.
- You have more energy and experience than the 3rd opponent so you win.
  Your energy becomes 3 - 2 = 1, and your experience becomes 16 + 1 = 17.
You did a total of 6 + 2 = 8 hours of training before the competition, so we return 8.
It can be proven that no smaller answer exists.
```

**Example 2:**

```
Input: initialEnergy = 2, initialExperience = 4, energy = [1], experience = [3]
Output: 0
Explanation: You do not need any additional energy or experience to win the competition, so we return 0.
```

**Constraints**

- n == energy.length == experience.length
- 1 <= n <= 100
- 1 <= initialEnergy, initialExperience, energy[i], experience[i] <= 100

---

## 题目（中文翻译）

你将参加一场比赛，给定两个正整数 `initialEnergy`（初始能量） 和 `initialExperience`（初始经验），分别表示你的初始能量和初始经验。  
同时给定两个下标从 **0** 开始的整数数组 `energy` 和 `experience`，长度均为 `n`。

你需要按顺序面对 `n` 个对手（opponent）。第 `i` 位对手的能量和经验分别为 `energy[i]` 和 `experience[i]`。  
当你面对一位对手时，**必须**同时拥有 **严格大于** 对手的经验和能量才能击败他并继续（如果还有后续对手）。  

- 击败第 `i` 位对手后，你的经验会增加 `experience[i]`，但能量会减少 `energy[i]`。  

在比赛开始前，你可以进行若干小时的训练。每训练 **1 小时**，可以选择将 **初始经验** 增加 **1**，或将 **初始能量** 增加 **1**。  

返回为了击败所有 `n` 位对手，所需的 **最少训练小时数**。

---

### 示例

**示例 1**

```
Input: initialEnergy = 5, initialExperience = 3, energy = [1,4,3,2], experience = [2,6,3,1]
Output: 8
Explanation: 你可以在训练 6 小时后将能量提升至 11，在训练 2 小时后将经验提升至 5。
接下来按顺序面对对手：
- 你的能量和经验均大于第 0 位对手，获胜。此时能量变为 11 - 1 = 10，经验变为 5 + 2 = 7。
- 你的能量仍大于第 1 位对手，但经验（7）不大于其经验（6），因此需要先训练提升经验……
（后续过程省略）
```

**示例 2**

```
Input: initialEnergy = 2, initialExperience = 4, energy = [1], experience = [3]
Output: 0
Explanation: 你无需额外的能量或经验即可赢得比赛，因此返回 0。
```

---

### 约束条件

- `n == energy.length == experience.length`
- `1 <= n <= 100`
- `1 <= initialEnergy, initialExperience, energy[i], experience[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是 **“一次一次地训练”**，把训练过程模拟出来。  
我们可以把每一次训练看成一次“加一”操作：  
- 把经验值 `experience` 加 1，或者  
- 把能量值 `energy` 加 1。  

每训练完一次，就去尝试按顺序挑战对手。如果在某个对手面前，**经验或能量不够**（必须 **严格大于** 对手的对应值），就继续训练，直到两者都满足为止。  

> **类比**：  
> 想象你在玩一款 RPG 游戏，需要先升级（训练）角色的属性，才能打败一波怪物。每升级一次属性，只能提升一点点，直到属性足够大才能继续前进。  

这种方法一定能得到答案，因为我们不断增加属性，最终必然可以大到把所有对手都打败。  

#### 代码（Python）  

```python
def minNumberOfHours_bruteforce(initialEnergy, initialExperience, energy, experience):
    # 当前的能量和经验，复制一份防止修改原始输入
    cur_energy = initialEnergy
    cur_exp = initialExperience
    hours = 0                     # 训练的总小时数

    n = len(energy)

    # 只要还有对手没打完，就一直循环
    i = 0
    while i < n:
        # 若当前能量或经验不足以击败第 i 个对手，则训练
        if cur_energy <= energy[i] or cur_exp <= experience[i]:
            # 训练策略：先把不足的属性补足
            if cur_energy <= energy[i]:
                # 能量需要比对手多 1
                need = energy[i] - cur_energy + 1
                cur_energy += need
                hours += need
            if cur_exp <= experience[i]:
                # 经验需要比对手多 1
                need = experience[i] - cur_exp + 1
                cur_exp += need
                hours += need
            # 训练完后，重新检查同一个对手
            continue

        # 能量和经验都足够，正式击败对手
        cur_energy -= energy[i]          # 能量消耗
        cur_exp += experience[i]         # 经验提升
        i += 1                           # 进入下一个对手

    return hours
```

> 关键点注释已在代码中，用中文解释每一步的意义。

#### 复杂度  

- **时间复杂度**：`O(total_training_hours × n)`  
  这里的 `total_training_hours` 是最终答案的大小。因为每训练一次就会重新检查当前对手，最坏情况下会在每个对手前进行多次训练，导致时间随训练小时数线性增长。  
  用大白话说，就是“训练多少小时，代码就跑多少遍”。在题目限制（属性值 ≤ 100）下仍然可以接受，但当数值变大时会变慢。  

- **空间复杂度**：`O(1)`  
  只使用了常数级的额外变量（当前能量、经验、计数器），不随输入规模增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次只训练一次，然后又要重新从头检查**。  
其实我们完全可以**一次性把不足的属性补齐**，不必一步一步地“慢慢训练”。  

对每个对手，分别考虑能量和经验的两种情况：

1. **能量不足**  
   - 规则要求：**必须严格大于** 对手的能量 `energy[i]`。  
   - 若 `cur_energy <= energy[i]`，我们直接把能量提升到 `energy[i] + 1`，所需的训练小时数就是 `energy[i] - cur_energy + 1`。  
   - 这样一次训练就能保证当前对手可以被击败，后面不需要再为同一个对手多次训练。

2. **经验不足**  
   - 同理，若 `cur_exp <= experience[i]`，我们把经验提升到 `experience[i] + 1`，所需的训练小时数是 `experience[i] - cur_exp + 1`。  
   - 经验提升后，**要记得把当前经验设为提升后的值**（即 `experience[i] + 1`），因为后面会继续累加对手的经验。

完成必要的训练后，**直接进行战斗**：  
- 能量减去 `energy[i]`（因为对手会消耗我们的能量）  
- 经验加上 `experience[i]`（因为击败对手会提升我们的经验）  

把上述过程对所有对手顺序执行，累计的训练小时数即为答案。  

> **类比**：  
> 想象你在排队买咖啡，需要先检查自己的钱包里是否有足够的钱。如果不够，你一次性把钱补足到“刚好够买当前咖啡的金额”，而不是每次只加一块钱。这样排队速度会快很多。  

#### 代码（Python）  

```python
def minNumberOfHours(initialEnergy, initialExperience, energy, experience):
    """
    贪心算法：一次性把不足的能量/经验补齐
    时间复杂度 O(n) ，空间复杂度 O(1)
    """
    cur_energy = initialEnergy          # 当前剩余能量
    cur_exp = initialExperience         # 当前经验值
    hours = 0                           # 训练总时长

    for e, exp in zip(energy, experience):
        # ---------- 处理能量 ----------
        if cur_energy <= e:                     # 能量不够，需要训练
            need = e - cur_energy + 1           # 提升到 > e 所需的最小值
            cur_energy += need
            hours += need

        # ---------- 处理经验 ----------
        if cur_exp <= exp:                      # 经验不够，需要训练
            need = exp - cur_exp + 1            # 提升到 > exp 的最小值
            cur_exp += need
            hours += need

        # ---------- 战斗 ----------
        cur_energy -= e          # 能量被消耗
        cur_exp += exp           # 经验获得提升

    return hours
```

> 代码每一步都有中文注释，帮助初学者快速抓住关键点。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次对手列表，对每个对手做 **常数次** 的判断和加减操作。  
  与暴力解相比，**从“训练小时数 × n”降到了“n”，快了好几个数量级**。  

- **空间复杂度**：`O(1)`  
  只用几个整数变量记录当前能量、经验和累计的训练时间，和输入规模无关。

---

## 心得  

- **核心技巧**：**贪心**——在每一步都让属性**恰好满足**“严格大于”对手的要求，避免多余的训练。  
- **适用的题型**：  
  1. “最小增量使序列满足条件” 类题（如 LeetCode 1642 `Minimum Number of Operations to Make Array Sorted`）。  
  2. “资源分配与需求匹配” 的贪心题（如 LeetCode 1353 `Maximum Number of Events That Can Be Attended`）。  
- **解题钥匙**：**一次性把不足的属性补齐**，而不是一步步慢慢增加。  

---

## 反思  

- **第一反应**：先把训练过程写成循环，一次一次地增加属性，直到能打败当前对手。  
- **最容易踩的坑**：  
  - 忘记 “严格大于” 的要求，只满足 “≥” 会导致后面对手仍然无法击败。  
  - 经验提升后忘记把当前经验更新为提升后的值，导致后面的比较仍然使用旧的经验。  
  - 能量在每场战斗后要 **减去** 对手的能量消耗，不能忘记这一步。  
- **下次思路**：看到 “每个阶段都必须大于某个阈值” 时，立刻想到 **一次性补齐**（贪心），而不是逐步逼近。这样可以把时间复杂度从 **O(训练小时数 × n)** 降到 **O(n)**。