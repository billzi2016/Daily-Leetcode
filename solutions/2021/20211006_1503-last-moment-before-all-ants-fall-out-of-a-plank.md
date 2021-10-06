# #1503. 所有蚂蚁掉出木板前的最后时刻 / Last Moment Before All Ants Fall Out of a Plank

> 难度：中等 · 标签：Array、Brainteaser、Simulation · [LeetCode 链接](https://leetcode.com/problems/last-moment-before-all-ants-fall-out-of-a-plank/)

---

## 题目（英文原版）

**Description**

We have a wooden plank of the length n units. Some ants are walking on the plank, each ant moves with a speed of 1 unit per second. Some of the ants move to the left, the other move to the right.
When two ants moving in two different directions meet at some point, they change their directions and continue moving again. Assume changing directions does not take any additional time.
When an ant reaches one end of the plank at a time t, it falls out of the plank immediately.
Given an integer n and two integer arrays left and right, the positions of the ants moving to the left and the right, return the moment when the last ant(s) fall out of the plank.

**Examples**

**Example 1:**

```
Input: n = 4, left = [4,3], right = [0,1]
Output: 4
Explanation: In the image above:
-The ant at index 0 is named A and going to the right.
-The ant at index 1 is named B and going to the right.
-The ant at index 3 is named C and going to the left.
-The ant at index 4 is named D and going to the left.
The last moment when an ant was on the plank is t = 4 seconds. After that, it falls immediately out of the plank. (i.e., We can say that at t = 4.0000000001, there are no ants on the plank).
```

**Example 2:**

```
Input: n = 7, left = [], right = [0,1,2,3,4,5,6,7]
Output: 7
Explanation: All ants are going to the right, the ant at index 0 needs 7 seconds to fall.
```

**Example 3:**

```
Input: n = 7, left = [0,1,2,3,4,5,6,7], right = []
Output: 7
Explanation: All ants are going to the left, the ant at index 7 needs 7 seconds to fall.
```

**Constraints**

- 1 <= n <= 104
- 0 <= left.length <= n + 1
- 0 <= left[i] <= n
- 0 <= right.length <= n + 1
- 0 <= right[i] <= n
- 1 <= left.length + right.length <= n + 1
- All values of left and right are unique, and each value can appear only in one of the two arrays.

---

## 题目（中文翻译）

我们有一块长度为 `n` 单位的木板（plank）。若干只蚂蚁在木板上行走，每只蚂蚁的速度为每秒 1 单位。部分蚂蚁向左移动，另一部分向右移动。  
当两只方向相反的蚂蚁在某一点相遇时，它们会互相转向并继续移动，转向不消耗额外时间。  
当蚂蚁在时间 `t` 到达木板的某一端时，会立即从木板上掉落。  

给定整数 `n` 和两个整数数组 `left`、`right`，分别表示向左移动和向右移动的蚂蚁所在的位置，返回最后一只（或多只）蚂蚁掉落木板的时刻。

### 示例 1
```text
Input: n = 4, left = [4,3], right = [0,1]
Output: 4
Explanation: 如上图所示：
- 索引 0 处的蚂蚁记为 A，向右移动。
- 索引 1 处的蚂蚁记为 B，向右移动。
- 索引 3 处的蚂蚁记为 C，向左移动。
- 索引 4 处的蚂蚁记为 D，向左移动。
最后一只蚂蚁仍在木板上的时刻是 `t = 4` 秒，随后它立即掉落。
```

### 示例 2
```text
Input: n = 7, left = [], right = [0,1,2,3,4,5,6,7]
Output: 7
Explanation: 所有蚂蚁均向右移动，索引 0 处的蚂蚁需要 7 秒才能掉落。
```

### 示例 3
```text
Input: n = 7, left = [0,1,2,3,4,5,6,7], right = []
Output: 7
Explanation: 所有蚂蚁均向左移动，索引 7 处的蚂蚁需要 7 秒才能掉落。
```

### 约束条件
- `1 <= n <= 10^4`
- `0 <= left.length <= n + 1`
- `0 <= left[i] <= n`
- `0 <= right.length <= n + 1`
- `0 <= right[i] <= n`
- `1 <= left.length + right.length <= n + 1`
- `left` 与 `right` 中的所有值均唯一，且每个值只能出现在其中一个数组中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每只蚂蚁当成一个会走动的“小人”，把木板看成一条长度为 `n` 的数轴。  
- **数据结构**：用两个列表 `left_pos`、`right_pos` 分别保存向左、向右的蚂蚁当前位置。  
- **模拟过程**：每秒钟把所有蚂蚁的位置都往它们的方向移动 `1`。  
- **碰撞处理**：如果某时刻有两只蚂蚁恰好站在同一个位置（相向而行），它们会互相“调换方向”。这相当于把两只蚂蚁的 **方向标记** 互换。  
- **掉落**：当蚂蚁的坐标小于 `0` 或大于 `n` 时，它就直接从木板上掉下来，从列表中移除。  

只要一直模拟到列表为空，记录下最后一次掉落的时间，就是答案。

> **为什么这样一定能得到正确答案？**  
> 因为我们严格按照题目描述的「每秒移动 1 单位、相遇后立即调头、到达端点即掉落」来执行，没有遗漏任何一步。只要时间足够长，所有蚂蚁必然会掉落。

#### 代码（Python）

```python
def get_last_moment_bruteforce(n: int, left: list[int], right: list[int]) -> int:
    # left: 向左走的蚂蚁初始位置
    # right: 向右走的蚂蚁初始位置
    # 用字典记录每只蚂蚁的方向，True 表示向右，False 表示向左
    ants = {pos: False for pos in left}          # 向左 -> False
    ants.update({pos: True for pos in right})    # 向右 -> True

    time = 0
    while ants:               # 只要还有蚂蚁在木板上就继续
        time += 1

        # 1. 先把所有蚂蚁移动 1 步，生成新的位置字典
        new_ants = {}
        for pos, to_right in ants.items():
            new_pos = pos + 1 if to_right else pos - 1
            # 2. 如果已经走出木板，就直接丢弃（掉落）
            if 0 <= new_pos <= n:
                # 3. 记录下新位置，如果已有蚂蚁占据，说明相遇，需要调头
                if new_pos in new_ants:
                    # 两只相遇：把各自的方向翻转
                    new_ants[new_pos] = not new_ants[new_pos]
                else:
                    new_ants[new_pos] = to_right
        ants = new_ants
    return time
```

> **关键注释**  
> - `ants` 用 `pos -> direction` 保存当前每个位置的蚂蚁方向。  
> - 移动后若出现同一 `new_pos`，说明两只相向而行，此时把已经记录的方向取反（等价于两只调头）。  
> - 循环结束时 `time` 正好是最后一只蚂蚁掉下的时刻。

#### 复杂度

- **时间复杂度**：`O(T * m)`，其中 `m = len(left)+len(right)` 是蚂蚁数量，`T` 是最大掉落时间（不超过 `n`），所以最坏情况约为 `O(n * m)`。  
  > 大白话：如果木板长 10 000，蚂蚁也有 10 000，只要每秒都遍历一次，最多要跑 10 000 秒，整体大概是 1 亿次操作，已经接近上限。  
- **空间复杂度**：`O(m)`，只需要保存当前每只蚂蚁的位置和方向。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**瓶颈**在于每秒都要遍历所有蚂蚁并处理碰撞。  
仔细想想，**两只相向而行的蚂蚁相遇后调头**，其实和**它们互相穿过、方向不变**是等价的。  
> **类比**：两个人在走廊里相向而行，碰面后各自转身继续走，等价于他们不转身、直接从对方身上“穿过去”。  
> 因为蚂蚁本身没有身份区分（只关心“还有多少时间在木板上”），我们完全可以把“调头”看作“继续直走”。  

于是**每只蚂蚁只需要看它离自己朝向的那端有多远**，它到底会在多久掉落，根本不受其它蚂蚁的影响。  
- 向左走的蚂蚁：距离左端的距离就是 `position`（因为左端坐标是 `0`）。  
- 向右走的蚂蚁：距离右端的距离就是 `n - position`（因为右端坐标是 `n`）。  

所有蚂蚁掉落的时间就是这些距离的**最大值**。  

#### 代码（Python）

```python
def get_last_moment_optimal(n: int, left: list[int], right: list[int]) -> int:
    """
    计算最后一只蚂蚁掉下木板的时刻。
    思路：碰撞等价于“穿过”，只需取每只蚂蚁到它所朝向端点的距离的最大值。
    """
    # 对于向左走的蚂蚁，掉落时间 = 当前位置到左端的距离
    max_left = max(left) if left else 0          # 只需要最大位置，因为距离 = 位置本身
    # 对于向右走的蚂蚁，掉落时间 = 右端坐标 - 当前位置
    max_right = max((n - pos) for pos in right) if right else 0

    # 最后掉落的时刻是两者的最大值
    return max(max_left, max_right)
```

> **关键注释**  
> - `max(left)` 直接给出向左蚂蚁中离左端最远的那只的距离（因为距离就是它的坐标）。  
> - 对向右蚂蚁，用列表推导式算出每只蚂蚁到右端的距离，再取最大。  
> - 若某个方向没有蚂蚁，直接视为 `0`（不会影响最大值的比较）。

#### 复杂度

- **时间复杂度**：`O(L + R)`，只遍历一次左侧列表和一次右侧列表。  
  > 与暴力解相比，省掉了 “每秒模拟” 的 `n` 倍因子，真正只和蚂蚁数量线性相关。  
- **空间复杂度**：`O(1)`，只用常数级别的几个变量。

---

## 心得

- **核心技巧**：把“相向相遇后调头”转化为“相向相遇后直接穿过”。这是一种**等价变换**，常用于蚂蚁、球弹碰等“无身份”问题。  
- **适用题型**：  
  1. “Ants on a Plank” 系列（如 LeetCode 1490）。  
  2. “Collision of balls in a line” 之类的“一维弹性碰撞”问题。  
  3. “Minimum time for all people to exit a corridor” 这类只关心最远距离的题。  
- **一句话总结**：**把碰撞视作穿过，答案就是所有蚂蚁到自己朝向端点的最大距离。**

---

## 反思

- **第一反应**：先想到逐秒模拟，因为“每秒走 1 步”这个描述非常直观。  
- **最容易踩的坑**：  
  - 忘记把 **左端坐标是 0，右端坐标是 n** 区分清楚，导致距离公式写错。  
  - 没考虑空数组的情况（全部向同一方向），直接 `max([])` 会报错。  
  - 在暴力模拟时，忘记在相遇后把两只蚂蚁的方向都翻转，只翻转了一只，导致结果偏差。  
- **下次思路**：看到“一维运动、相向相遇、速度相同”时，立刻检查是否可以使用“等价穿过”或“把碰撞抽象掉”的技巧，先求 **每只对象到端点的时间**，再取最大值。这样往往能直接得到最优解。