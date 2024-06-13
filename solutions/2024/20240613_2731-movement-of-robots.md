# #2731. 机器人移动 / Movement of Robots

> 难度：中等 · 标签：Array、Brainteaser、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/movement-of-robots/)

---

## 题目（英文原版）

**Description**

Some robots are standing on an infinite number line with their initial coordinates given by a 0-indexed integer array nums and will start moving once given the command to move. The robots will move a unit distance each second.
You are given a string s denoting the direction in which robots will move on command. 'L' means the robot will move towards the left side or negative side of the number line, whereas 'R' means the robot will move towards the right side or positive side of the number line.
If two robots collide, they will start moving in opposite directions.
Return the sum of distances between all the pairs of robots d seconds after the command. Since the sum can be very large, return it modulo 109 + 7.
Note:

**Examples**

**Example 1:**

```
Input: nums = [-2,0,2], s = "RLL", d = 3
Output: 8
Explanation: 
After 1 second, the positions are [-1,-1,1]. Now, the robot at index 0 will move left, and the robot at index 1 will move right.
After 2 seconds, the positions are [-2,0,0]. Now, the robot at index 1 will move left, and the robot at index 2 will move right.
After 3 seconds, the positions are [-3,-1,1].
The distance between the robot at index 0 and 1 is abs(-3 - (-1)) = 2.
The distance between the robot at index 0 and 2 is abs(-3 - 1) = 4.
The distance between the robot at index 1 and 2 is abs(-1 - 1) = 2.
The sum of the pairs of all distances = 2 + 4 + 2 = 8.
```

**Example 2:**

```
Input: nums = [1,0], s = "RL", d = 2
Output: 5
Explanation: 
After 1 second, the positions are [2,-1].
After 2 seconds, the positions are [3,-2].
The distance between the two robots is abs(-2 - 3) = 5.
```

**Constraints**

- 2 <= nums.length <= 105
- -2 * 109 <= nums[i] <= 2 * 109
- 0 <= d <= 109
- nums.length == s.length
- s consists of 'L' and 'R' only
- nums[i] will be unique.

---

## 题目（中文翻译）

一些机器人站在无限数轴上，它们的初始坐标由下标从 **0** 开始的整数数组 `nums` 给出。收到指令后，机器人将开始移动，每秒移动 **1** 个单位距离。  
给定字符串 `s` 表示机器人在指令下的移动方向，`'L'` 表示机器人向数轴的左侧（负方向）移动，`'R'` 表示机器人向数轴的右侧（正方向）移动。  
如果两个机器人相撞，它们会开始向相反方向移动。  
返回指令执行 **d** 秒后，所有机器人对之间距离之和。由于答案可能非常大，请返回 **(答案 mod 10⁹ + 7)**。

**示例 1**  
```text
Input: nums = [-2,0,2], s = "RLL", d = 3
Output: 8
```
**解释**：  
- 第 1 秒后，位置变为 `[-1,-1,1]`。此时下标 `0` 的机器人向左移动，下标 `1` 的机器人向右移动。  
- 第 2 秒后，位置变为 `[-2,0,0]`。此时下标 `1` 的机器人向左移动，下标 `2` 的机器人向右移动。  
- 第 3 秒后，位置变为 `[-3,-1,1]`。  

所有机器人对的距离之和为 `8`。

**示例 2**  
```text
Input: nums = [1,0], s = "RL", d = 2
Output: 5
```
**解释**：  
- 第 1 秒后，位置变为 `[2,-1]`。  
- 第 2 秒后，位置变为 `[3,-2]`。  

两机器人之间的距离为 `abs(-2 - 3) = 5`。

**约束条件**  

- `2 <= nums.length <= 10⁵`  
- `-2 * 10⁹ <= nums[i] <= 2 * 10⁹`  
- `0 <= d <= 10⁹`  
- `nums.length == s.length`  
- `s` 只包含字符 `'L'` 和 `'R'`  
- `nums[i]` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **逐秒模拟** 机器人的运动过程：

1. 把每个机器人记下来，它当前所在的坐标 `pos[i]` 和它的前进方向 `dir[i]`（`L` 为 -1，`R` 为 +1）。  
2. 循环 `d` 次（每一次代表 1 秒）  
   - 所有机器人同时向各自的方向走一步：`pos[i] += dir[i]`。  
   - 检查是否有 **碰撞**：如果两台机器人恰好站在同一个坐标上，它们会 **互相调头**（方向取相反数）。  
3. 循环结束后，遍历所有 `(i, j)` 对，累加 `abs(pos[i] - pos[j])`，再取模。

> **类比**：想象一条直线的跑道，机器人像小球一样每秒滚动一步，遇到同一位置的两个小球就会弹开、换方向。我们把每秒的运动过程完整写下来，就是最笨的办法。

**为什么正确**  
因为我们真的按照题目描述的每一步去执行了，所有的碰撞、调头、移动都一一对应，所以最终得到的距离一定是题目要求的。

**时间/空间分析**  

- 每秒我们要遍历所有机器人一次，碰撞检测最坏情况下需要两两比较（`O(n²)`），即 **`O(d·n²)`**。  
- 再算一次所有配对的距离，需要 `O(n²)`。  
- 空间只存了 `pos`、`dir` 两个长度为 `n` 的数组，**`O(n)`**。

> **大白话**：  
> - `O(d·n²)` 就像你有 10 万个机器人（`n=10⁵`），要跑 10⁹ 秒（`d=10⁹`），每秒还要把每两个机器人配对检查一次，根本不可能在电脑里跑完。  
> - `O(n²)` 的意思是“把所有机器人两两配对”，如果机器人有 10 万个，配对数就是 5 000 000 000，已经太大了。

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute_force(nums, s, d):
    n = len(nums)
    # 当前位置
    pos = nums[:]
    # 方向：L -> -1, R -> +1
    dir_ = [-1 if c == 'L' else 1 for c in s]

    for _ in range(d):                     # 每秒一次
        # 先让所有机器人同时移动一步
        for i in range(n):
            pos[i] += dir_[i]

        # 检测碰撞：把坐标相同的机器人成对调头
        # 最朴素的做法是两层循环比较
        for i in range(n):
            for j in range(i + 1, n):
                if pos[i] == pos[j]:       # 碰到同一点
                    dir_[i] *= -1          # 方向相反
                    dir_[j] *= -1

    # 计算所有配对的距离和
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            ans = (ans + abs(pos[i] - pos[j])) % MOD
    return ans
```

> 这段代码可以直接跑通小规模的测试（比如 `n ≤ 10`、`d ≤ 10`），但对正式数据会 **超时**。

#### 复杂度

- **时间复杂度**：`O(d·n²)` —— 每秒要两层循环比较所有机器人，`d` 可能高达 `10⁹`，根本不可行。  
- **空间复杂度**：`O(n)` —— 只用了两个长度为 `n` 的数组保存位置和方向。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：

1. **逐秒模拟**：`d` 可能非常大（`10⁹`），不可能真的跑这么多秒。  
2. **碰撞处理**：每秒都要两两比较位置，`O(n²)` 的代价太高。

**关键观察**（提示已经给出）：

> 如果把“碰撞后调头”这件事**忽略**，让每个机器人只按照自己的原始方向一直走 `d` 步，得到的 **最终坐标** 与真实情况是**完全相同**的。

**为什么**？  
想象两台机器人在同一点相遇后互相换方向继续走。换方向后，它们的后续轨迹其实**相当于**把这两台机器人的“身份”互换了。  
- 原来机器人 A 向右、B 向左，碰撞后 A 向左、B 向右。  
- 如果我们把 A、B 的身份互换（把 A 当成 B、B 当成 A），那么它们继续走 **不需要调头**，仍然是“向右的机器人走右、向左的机器人走左”。  
- 由于我们只关心 **所有机器人最终所在的坐标集合**（而不是哪台机器人到底是哪台），所以可以直接让每台机器人“直线前进”，不必模拟调头。

于是，**忽略碰撞**，每台机器人 `i` 的最终坐标：

```
final[i] = nums[i] + d   (if s[i] == 'R')
final[i] = nums[i] - d   (if s[i] == 'L')
```

得到 `final` 数组后，题目要求 **所有配对的距离之和**：

```
Σ_{i<j} |final[i] - final[j]|
```

这正是**求一组数的绝对差之和**，常用的技巧是：

1. 把 `final` **排序**。设排序后为 `a[0] ≤ a[1] ≤ … ≤ a[n-1]`。  
2. 用**前缀和**（prefix sum）快速累计每个元素与左边所有元素的差：

   对于位置 `i`（从左到右），它与左侧 `i` 个元素的距离和是：

   ```
   a[i] * i - prefix[i-1]
   ```

   其中 `prefix[i-1] = a[0] + a[1] + … + a[i-1]`。  
3. 把上面的值累加到答案中，即得到全部配对的绝对差之和。

**为什么排序后可以这么算？**  
因为在有序序列中，任意两数的差 `a[j] - a[i] (j>i)` 都是正的，`|a[j] - a[i]| = a[j] - a[i]`。于是把所有差展开：

```
Σ_{j>i} (a[j] - a[i])
= Σ_{j} a[j] * (j) - Σ_{i} a[i] * (n-1-i)
```

前缀和的形式正是对上述公式的逐步累加，实现上更直观。

**完整流程**：

1. 计算每台机器人 `d` 秒后的坐标（忽略碰撞）。  
2. 将这些坐标放入数组 `pos`，并 **排序**。  
3. 维护一个变量 `pre`（已遍历元素的前缀和），以及答案 `ans`。  
4. 从左到右遍历排序后的 `pos`，对第 `i` 个元素（0‑based）：

   ```
   ans += pos[i] * i - pre
   ans %= MOD
   pre += pos[i]
   pre %= MOD   # 防止整数溢出（Python 本身不溢出，但取模保持统一）
   ```

5. 返回 `ans`。

**复杂度**  

- 排序 `O(n log n)`。  
- 单次遍历 `O(n)`。  
- 只用了几个长度为 `n` 的数组，空间 `O(n)`（如果直接在原数组上排序，甚至可以是 `O(1)` 额外空间）。

> 与暴力解相比，时间从天文数字的 `O(d·n²)` 降到了 `O(n log n)`，在 `n ≤ 10⁵` 时轻松跑完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def movement_of_robots(nums, s, d):
    """
    计算 d 秒后所有机器人配对距离之和（模 1e9+7）
    思路：忽略碰撞，直接算每台机器人的最终坐标，随后用排序 + 前缀和求绝对差之和。
    """
    n = len(nums)

    # 1️⃣ 计算每台机器人在 d 秒后的坐标（不考虑碰撞）
    #    R -> 向右走 d 步，L -> 向左走 d 步
    final_pos = [0] * n
    for i in range(n):
        if s[i] == 'R':
            final_pos[i] = nums[i] + d
        else:               # 'L'
            final_pos[i] = nums[i] - d

    # 2️⃣ 对坐标排序，后面使用前缀和
    final_pos.sort()

    # 3️⃣ 前缀和遍历，累计配对距离
    ans = 0          # 最终答案
    pre = 0          # 已遍历元素的坐标和（前缀和）
    for i, x in enumerate(final_pos):
        # 对于当前元素 x，它与左侧 i 个元素的距离之和是：
        # x * i - pre
        ans = (ans + (x % MOD) * i - pre) % MOD
        # 更新前缀和（取模防止数字过大）
        pre = (pre + x) % MOD

    return ans
```

> 代码中 `x % MOD`、`pre % MOD` 是为了防止在极端情况下整数非常大（`nums[i]` 可能到 `2·10⁹`，`d` 也到 `10⁹`），虽然 Python 的整数不溢出，但取模可以保持数值在 64 位范围，和题目要求保持一致。

---

## 心得

- **核心技巧**：**忽略碰撞的等价性 + 排序 + 前缀和求绝对差之和**。  
- 该技巧适用于很多“**所有配对的距离之和**”或“**所有配对的绝对差之和**”的题目，例如  
  1. LeetCode 1688 *Count of Matching Subsequences*（变形后用前缀和统计）  
  2. LeetCode 1498 *Number of Subsequences That Satisfy the Given Sum Condition*（同样先排序再前缀和）  
  3. LeetCode 1657 *Determine if Two Strings Are Close*（利用排序与前缀和的思路）  
- **一句话总结解题钥匙**：  
  “把碰撞看成机器人身份的互换，先算出每台机器人的‘理想位置’，再用排序 + 前缀和快速求所有配对的绝对距离。”

---

## 反思

- **第一反应**：看到“碰撞后调头”，会本能想到**逐秒模拟**，但很快发现 `d` 可能高达 `10⁹`，模拟根本不现实。  
- **最容易踩的坑**  
  1. **忽略碰撞的等价性**：需要清晰说明为什么最终坐标不受调头影响，否则会产生错误的实现。  
  2. **负数与大数取模**：`x * i - pre` 可能为负数，取模时要使用 `(value % MOD + MOD) % MOD` 或直接在 Python 中使用 `% MOD`（Python 已经保证非负）。  
  3. **整数溢出**（在 C++/Java 中会出现）：在 Python 中虽不溢出，但仍需在每一步取模保持数值规模。  
- **下次遇到同类题**，第一步应该思考**是否可以把动态过程（碰撞、调头、移动）抽象成一个等价的静态结果**，如“忽略碰撞后的位置不变”。如果可以，就先把问题简化到**求配对距离/和**，再利用**排序 + 前缀和**等常用技巧完成高效计算。