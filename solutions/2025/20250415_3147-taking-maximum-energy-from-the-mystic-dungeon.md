# #3147. 从神秘地下城获取最大能量 / Taking Maximum Energy From the Mystic Dungeon

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/)

---

## 题目（英文原版）

**Description**

In a mystic dungeon, n magicians are standing in a line. Each magician has an attribute that gives you energy. Some magicians can give you negative energy, which means taking energy from you.
You have been cursed in such a way that after absorbing energy from magician i, you will be instantly transported to magician (i + k). This process will be repeated until you reach the magician where (i + k) does not exist.
In other words, you will choose a starting point and then teleport with k jumps until you reach the end of the magicians' sequence, absorbing all the energy during the journey.
You are given an array energy and an integer k. Return the maximum possible energy you can gain.
Note that when you are reach a magician, you must take energy from them, whether it is negative or positive energy.

**Examples**

**Example 1:**

```
Input: energy = [5,2,-10,-5,1], k = 3
Output: 3
Explanation: We can gain a total energy of 3 by starting from magician 1 absorbing 2 + 1 = 3.
```

**Example 2:**

```
Input: energy = [-2,-3,-1], k = 2
Output: -1
Explanation: We can gain a total energy of -1 by starting from magician 2.
```

**Constraints**

- 1 <= energy.length <= 105
- -1000 <= energy[i] <= 1000
- 1 <= k <= energy.length - 1

---

## 题目（中文翻译）

在一条直线上有 `n` 位魔法师 (magician)。每位魔法师都有一个属性会给你能量 (energy)。有些魔法师会给你负能量，也就是从你这里扣除能量。  
你受到诅咒：在从第 `i` 位魔法师吸收能量后，你会立刻被传送到第 `i + k` 位魔法师。这个过程会一直重复，直到不存在第 `i + k` 位魔法师为止。  

换句话说，你可以任选一个起始位置，然后以步长 `k` 跳跃直到序列结束，在此过程中必须收集所有经过的能量。  
给定数组 `energy` 和整数 `k`，返回你能够获得的最大可能能量总和。  
注意：每当你到达一位魔法师时，都必须获取其能量，无论是正能量还是负能量。

**示例 1**  
**输入**: `energy = [5,2,-10,-5,1]`, `k = 3`  
**输出**: `3`  
**解释**: 从第 1 位魔法师开始，吸收的能量为 `2 + 1 = 3`，总和为 3。

**示例 2**  
**输入**: `energy = [-2,-3,-1]`, `k = 2`  
**输出**: `-1`  
**解释**: 从第 2 位魔法师开始，吸收的能量为 `-1`，总和为 -1。

**约束条件**  
- `1 <= energy.length <= 10^5`  
- `-1000 <= energy[i] <= 1000`  
- `1 <= k <= energy.length - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一个可能的起点**，然后按照题目给出的跳数 `k` 一直往后跳，累计经过的能量，最后取最大的累计值。

- **数据结构**：只需要一个普通的列表 `energy`，我们把它想象成一排排魔法师站成的队伍。遍历时用 **下标**（相当于给每个人贴了编号）来定位当前站在的魔法师。
- **为什么正确**：因为题目要求“任选一个起点”，只要把所有起点都尝试一遍，必然能找到最优的那一个。每一次的“跳”过程都是唯一的（只能往后跳 `k` 步），所以遍历所有起点即可覆盖全部可能的路径。
- **时间/空间复杂度**：  
  - 对每一个起点，我们最多会访问 `⌈n/k⌉` 次（因为每跳走 `k`，最多走完数组）。如果我们把所有起点都尝试一次，总的访问次数约为 `n/k + n/k + … ≈ n * (n/k) = O(n²/k)`，在最坏情况下（`k = 1`）就是 `O(n²)`。  
    - **大白话**：想象有 `n` 个人排成一行，`k=1` 时我们相当于从每个人出发都要走遍全部人，像在跑来跑去，步数会成平方级增长。  
  - 只用了常数级的额外空间（几个计数器），所以空间是 `O(1)`。

#### 代码（Python）

```python
def maxEnergy_bruteforce(energy, k):
    n = len(energy)
    best = -10**9                     # 记录全局最大能量，初始设一个很小的数
    for start in range(n):            # 枚举每一个起点
        cur = 0                        # 当前路径的累计能量
        i = start
        while i < n:                  # 按 k 跳到数组末尾
            cur += energy[i]          # 必须吸收当前魔法师的能量
            i += k                     # “瞬移”到下一个位置
        best = max(best, cur)         # 更新全局最大值
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（最坏情况 `k = 1` 时，每个起点都会遍历近 `n` 次）。  
  - **含义解释**：如果 `n = 10⁴`，暴力解大约要进行 `10⁸` 次循环，计算机会明显卡顿。
- **空间复杂度**：`O(1)`，只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一次跳的过程都是固定的**：从位置 `i` 开始，下一步一定是 `i + k`，再下一步是 `i + 2k` …… 这是一条**等差数列**的下标。  

我们可以把 **从 `i` 开始的总能量** 记为 `dp[i]`（动态规划的常用记号），则显然有：

```
dp[i] = energy[i] + dp[i + k]   （如果 i + k 超出数组范围，则 dp[i + k] = 0）
```

也就是说，**从 `i` 开始的能量等于当前位置的能量加上从 `i + k` 开始的能量**。这是一条递推关系，**只要我们已经算出 `dp[i + k]`，就能立刻得到 `dp[i]`**。

因此我们可以 **逆序遍历**数组（从右往左），保证在计算 `dp[i]` 时，`dp[i + k]` 已经被求出。整个过程只需要一次遍历，时间是线性的。

> **类比**：想象每个魔法师手里都有一张“通往后面魔法师的票”，票上写着从他那里继续跳下去能得到的总能量。我们从最右边的魔法师开始贴票（因为他后面没有人，票上写的就是自己的能量），然后向左依次贴，贴完后每个人手里的票就是从他出发能得到的最大能量。

**实现细节**：

1. 创建一个与 `energy` 同长度的数组 `dp`（可以直接在原数组上改写，省空间）。
2. 从下标 `n-1` 到 `0` 逆序遍历：
   - 若 `i + k` 超出范围，`dp[i] = energy[i]`（只能拿到自己的能量）。
   - 否则 `dp[i] = energy[i] + dp[i + k]`。
3. 遍历结束后，答案就是 `dp` 中的最大值。

**复杂度分析**：

- **时间**：只遍历一次 `n`，每个位置做 O(1) 的加法，故 `O(n)`。相比暴力的 `O(n²)`，快了几个数量级。
- **空间**：如果直接在原数组上改写，只需要 `O(1)` 额外空间；若另建 `dp` 数组，则是 `O(n)`，但仍然是线性的。

#### 代码（Python）

```python
def maxEnergy_optimal(energy, k):
    """
    返回在任意起点、每次跳 k 步的情况下能够获得的最大能量。
    """
    n = len(energy)
    # dp[i] 表示从 i 开始（包括 i）能获得的总能量
    # 为了节约空间，直接在 energy 上改写成 dp
    dp = energy[:]                     # 复制一份，保持原数组不变（可省略）

    # 逆序遍历，保证 dp[i + k] 已经算好
    for i in range(n - 1, -1, -1):
        nxt = i + k                    # 下一跳的位置
        if nxt < n:                    # 还能跳到下一个魔法师
            dp[i] = dp[i] + dp[nxt]    # 当前能量 + 从 nxt 开始的最优能量
        # else: dp[i] 本身已经是只取自己能量的情况，无需修改

    # 最终答案是所有 dp[i] 中的最大值
    return max(dp)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，哪怕 `n = 10⁵` 也能在毫秒级完成。  
  - **含义解释**：如果 `n = 100,000`，我们只做 100,000 次加法，比暴力的 10,000,000,000 次（`n²`）少了 5 位数的量级。
- **空间复杂度**：`O(1)`（如果在原数组上原地修改）或 `O(n)`（若额外创建 `dp` 数组）。在本实现里用了 `O(n)` 的临时数组，只是为了代码更直观。

---

## 心得

- **核心技巧**：**递推式 + 逆序 DP**（从后往前算），把“后面的子问题已知”这一点利用起来，避免重复计算。
- **适用题型**：
  1. “从当前位置跳固定步长，求最大/最小累计值”——例如 **“跳石子游戏”**（固定步长的爬楼梯变体）。
  2. “每个位置只能向右走固定距离，求最优路径”——如 **“最小代价跳跃”**（每次跳 `k` 步的最小费用）。
  3. “按固定间隔取子序列求和最大值”——比如 **“分段求和最大化”**（按模 `k` 分组）。
- **一句话总结解题钥匙**：**把从 i 开始的答案表达为自身加上已知的 i+k 的答案，逆序填表即可**。

---

## 反思

- **第一反应**：看到“每次固定跳 k 步”，自然想到**遍历所有起点**，直接模拟跳的过程（就是暴力解）。
- **最容易踩的坑**：
  1. **下标越界**：在递推时一定要先判断 `i + k` 是否在数组范围内，否则会抛异常。
  2. **负数能量**：即使所有能量都是负的，答案仍然是**最大（即最不负）的单个能量**，不能默认答案是非负。
  3. **空间优化**：很多人会直接开一个 `dp` 数组而忘记可以**在原数组上原地修改**，导致不必要的额外空间。
- **下次遇到同类题**，第一步应该想到**“把当前状态和后面的状态关联起来”，写出递推式，然后考虑逆序或前序 DP 的遍历顺序**，这一步往往能把指数级的暴力直接压缩到线性。