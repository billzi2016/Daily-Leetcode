# #2751. 机器人碰撞 / Robot Collisions

> 难度：困难 · 标签：Array、Stack、Sorting、Simulation · [LeetCode 链接](https://leetcode.com/problems/robot-collisions/)

---

## 题目（英文原版）

**Description**

There are n 1-indexed robots, each having a position on a line, health, and movement direction.
You are given 0-indexed integer arrays positions, healths, and a string directions (directions[i] is either 'L' for left or 'R' for right). All integers in positions are unique.
All robots start moving on the line simultaneously at the same speed in their given directions. If two robots ever share the same position while moving, they will collide.
If two robots collide, the robot with lower health is removed from the line, and the health of the other robot decreases by one. The surviving robot continues in the same direction it was going. If both robots have the same health, they are both removed from the line.
Your task is to determine the health of the robots that survive the collisions, in the same order that the robots were given, i.e. final health of robot 1 (if survived), final health of robot 2 (if survived), and so on. If there are no survivors, return an empty array.
Return an array containing the health of the remaining robots (in the order they were given in the input), after no further collisions can occur.
Note: The positions may be unsorted.

**Examples**

**Example 1:**

```
Input: positions = [5,4,3,2,1], healths = [2,17,9,15,10], directions = "RRRRR"
Output: [2,17,9,15,10]
Explanation: No collision occurs in this example, since all robots are moving in the same direction. So, the health of the robots in order from the first robot is returned, [2, 17, 9, 15, 10].
```

**Example 2:**

```
Input: positions = [3,5,2,6], healths = [10,10,15,12], directions = "RLRL"
Output: [14]
Explanation: There are 2 collisions in this example. Firstly, robot 1 and robot 2 will collide, and since both have the same health, they will be removed from the line. Next, robot 3 and robot 4 will collide and since robot 4's health is smaller, it gets removed, and robot 3's health becomes 15 - 1 = 14. Only robot 3 remains, so we return [14].
```

**Example 3:**

```
Input: positions = [1,2,5,6], healths = [10,10,11,11], directions = "RLRL"
Output: []
Explanation: Robot 1 and robot 2 will collide and since both have the same health, they are both removed. Robot 3 and 4 will collide and since both have the same health, they are both removed. So, we return an empty array, [].
```

**Constraints**

- 1 <= positions.length == healths.length == directions.length == n <= 105
- 1 <= positions[i], healths[i] <= 109
- directions[i] == 'L' or directions[i] == 'R'
- All values in positions are distinct

---

## 题目（中文翻译）

**题目描述**

有 `n` 个编号为 1 起始的机器人，每个机器人位于数轴上的某个位置，拥有一定的生命值（health），并且具有移动方向。  
给定 **0 起始索引** 的整数数组 `positions`、`healths`，以及字符串 `directions`（`directions[i]` 为 `'L'` 表示左移，`'R'` 表示右移）。`positions` 中的所有整数互不相同。

所有机器人同时以相同的速度沿各自的方向开始移动。若在移动过程中出现两个机器人位于同一位置，则它们会发生碰撞（collision）。

- 碰撞时，生命值较低的机器人会被从数轴上移除，另一机器人的生命值会减 1。存活的机器人继续保持原来的移动方向。
- 若两机器人生命值相同，则两者同时被移除。

请你返回 **按照原始输入顺序**（即机器人 1、机器人 2 …）的存活机器人最终的生命值。如果没有机器人存活，返回空数组。

> 注意：`positions` 可能未按升序排列。

**返回值**  
一个数组，包含在所有可能的碰撞结束后仍然存活的机器人生命值，顺序与输入中机器人编号相同。

---

## 示例

### 示例 1
> **输入**  
> `positions = [5,4,3,2,1]`  
> `healths = [2,17,9,15,10]`  
> `directions = "RRRRR"`  

> **输出**  
> `[2,17,9,15,10]`  

> **解释**  
> 所有机器人均向右移动，方向相同，因而不存在碰撞。返回原始的生命值序列 `[2, 17, 9, 15, 10]`。

### 示例 2
> **输入**  
> `positions = [3,5,2,6]`  
> `healths = [10,10,15,12]`  
> `directions = "RLRL"`  

> **输出**  
> `[14]`  

> **解释**  
> 发生了两次碰撞。  
> 1. 机器人 1（位置 3，向右）与机器人 2（位置 5，向左）相遇，双方生命值相等，都被移除。  
> 2. 机器人 3（位置 2，向右）与机器人 4（位置 6，向左）相遇，机器人 4 的生命值较小，被移除，机器人 3 的生命值下降为 `15 - 1 = 14`。  
> 最终仅剩机器人 3，返回 `[14]`。

### 示例 3
> **输入**  
> `positions = [1,2,5,6]`  
> `healths = [10,10,11,11]`  
> `directions = "RLRL"`  

> **输出**  
> `[]`  

> **解释**  
> - 机器人 1 与机器人 2 碰撞，生命值相同，均被移除。  
> - 机器人 3 与机器人 4 碰撞，生命值相同，亦均被移除。  
> 所有机器人均被消除，返回空数组 `[]`。

---

## 约束条件

- `1 <= positions.length == healths.length == directions.length == n <= 10^5`
- `1 <= positions[i], healths[i] <= 10^9`
- `directions[i]` 为 `'L'` 或 `'R'`
- `positions` 中的所有值互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有机器人一次一次地“跑”下来**，看哪两个会在同一时刻占到同一个位置，然后按照题目规则立即处理碰撞。  

1. **把机器人按照位置排序**（因为位置是唯一的），这样我们可以从左到右依次观察它们的运动。  
2. 对每一对相邻的机器人，判断它们的方向是否相向（左机器人向右、右机器人向左）。只有相向的机器人才会相遇。  
3. 计算它们相遇的时间：  
   - 两个机器人速度相同，距离是 `pos2 - pos1`，相遇时间就是 `distance / (speed+speed) = distance / 2`（速度都是 1，实际不需要算，只要记住相向就一定会相撞）。  
4. 当相撞时，比较健康值（`health`），把血量更低的机器人删掉，另一只血量减 1。如果血量相等，两只都删掉。  
5. 删除后，**继续从头重新检查**，因为一次碰撞会导致后面的机器人位置、相邻关系全部变化。  

这相当于**不停地在数组里找相邻的“R…L”**，每次处理完后再从头扫描，直到再也找不到可以碰撞的对。

> **类比**：想象一排小车在直线道路上跑，只有迎面相遇的小车会相撞。我们把所有小车排成一列，手动检查每一对相邻的迎面车，碰撞后把受损的小车踢出队伍，再重新排队检查——这就是暴力模拟的过程。

**为什么它是正确的？**  
- 每一次我们都按照真实的运动规则（相向必相撞、血量更低者死亡、存活者血量减 1）来处理，且在所有可能的碰撞都被逐个执行后，剩下的机器人已经不可能再相遇，所以最终结果一定是题目要求的“所有碰撞结束后的健康值”。

**时间/空间复杂度**  
- 每次碰撞我们可能要**从头重新遍历**整个数组，最坏情况是每次只消除一只机器人，导致 **O(n) 次完整遍历**。每次遍历本身是 O(n)，于是总时间是 **O(n²)**。  
- 只使用了原数组和若干临时变量，额外空间是 **O(1)**（不计输入输出本身）。

> **大白话**：如果有 10,000 辆车，每次只能处理掉一辆，那我们得重新检查 10,000 次，每次又要走一遍 10,000 辆车，10,000 × 10,000 = 100,000,000 步，明显太慢了。

#### 代码（Python）

```python
def robotCollisions_bruteforce(positions, healths, directions):
    # 把机器人信息合在一起，方便后面操作
    robots = [
        {"pos": p, "hp": h, "dir": d, "idx": i}
        for i, (p, h, d) in enumerate(zip(positions, healths, directions))
    ]

    # 先按位置排序，左边的 robot 在前
    robots.sort(key=lambda r: r["pos"])

    changed = True                      # 是否有碰撞发生
    while changed:
        changed = False
        i = 0
        while i < len(robots) - 1:      # 只看相邻的两只机器人
            a, b = robots[i], robots[i + 1]
            # 只有 a 向右、b 向左才会相撞
            if a["dir"] == 'R' and b["dir"] == 'L':
                # 处理碰撞
                if a["hp"] > b["hp"]:
                    a["hp"] -= 1        # a 存活，血量减 1
                    del robots[i + 1]   # b 被消除
                elif a["hp"] < b["hp"]:
                    b["hp"] -= 1
                    del robots[i]       # a 被消除，i 指向下一个位置
                else:                    # 血量相等，两只都死
                    del robots[i + 1]
                    del robots[i]
                changed = True          # 发生了碰撞，需要重新扫描
                break                    # 立刻跳出 while，重新从头开始
            else:
                i += 1

    # 把剩余机器人的血量恢复成原始顺序
    ans = [0] * len(positions)
    for r in robots:
        ans[r["idx"]] = r["hp"]
    # 过滤掉没有存活的（血量为 0 的位置）
    return [hp for hp in ans if hp != 0]
```

> **关键注释**  
> - `robots.sort(key=lambda r: r["pos"])`：把机器人排成一列，好比把小车排好队。  
> - `if a["dir"] == 'R' and b["dir"] == 'L'`：只有面对面的两辆车会相撞。  
> - `del robots[i]` / `del robots[i+1]`：把撞坏的车从队列里踢出去。  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每一次碰撞都可能导致一次完整的 `while` 循环遍历，最坏情况下会进行 `n` 次遍历，每次遍历检查 `n` 个机器人。  
  - 用大白话说，就是“每次只消掉一只机器人，得重新走遍所有机器人 n 次”。  

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只用了常数个临时变量和一个用于排序的原地列表。  

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次碰撞后都要**从头重新扫描**，导致二次遍历。  
我们需要一种一次遍历就能把所有相向的碰撞“压平”。这里可以借助 **栈（stack）**，把“向右走的机器人”暂时放进去，等到出现向左走的机器人时，直接和栈顶的右走机器人比较——这正好对应了“最近的相向机器人必先相撞”。

**核心观察**  

1. 把机器人**按位置从左到右排序**。这样左边的机器人永远先出现，右边的机器人永远后出现。  
2. 只要方向是 `'R'`（向右），它**只能和后面出现的 `'L'`（向左）机器人相撞**，因为前面的机器人已经在它左侧，且已经决定了自己的命运。  
3. 当我们遍历到一个向左走的机器人 `L` 时，**栈顶一定是最近的、仍然存活的向右走的机器人 `R`**（如果栈里还有 `R`）。这两者必然是**最近的相向对**，先碰撞是必然的。  
4. 碰撞规则可以直接在栈上实现：  
   - 如果 `L` 的血量更大，`R` 死，`L` 的血量减 1，继续与栈中下一个 `R` 比较（因为 `L` 仍然活着，可能还要继续碰撞）。  
   - 如果血量相等，两者都死，直接弹出栈顶 `R`，`L` 也不再入栈。  
   - 如果 `R` 的血量更大，`L` 死，`R` 的血量减 1，`L` 不入栈。  

5. 处理完所有机器人后，**栈里剩下的**要么是向右的（`R`），要么是向左的（`L`）但已经不可能再碰撞（因为左边已经没有 `R` 了）。这两类机器人都是最终存活的。  

**为什么只需要一次遍历？**  
- 每个机器人只会 **进栈一次**（方向为 `R`）或 **与栈顶比较若干次**（方向为 `L`），比较过程会把血量为 0 的机器人弹出，**不会再回头检查**。这正是栈的“后进先出”特性，让我们一次完成所有相向碰撞的“配对”。  

**类比**：  
- 把向右走的机器人想象成**排队的冲锋队员**，他们站在栈里等待对面来袭的敌人（向左走的机器人）。当敌人出现时，最前面的冲锋队员（栈顶）先上前格斗，输的一方立刻倒下，胜者血量减 1，继续面对下一个敌人。整个过程只需要 **一次排队和一次战斗**，不必每次都重新点名检查。

#### 代码（Python）

```python
def robotCollisions(positions, healths, directions):
    """
    返回所有存活机器人的最终血量，顺序与原输入保持一致。
    思路：先按位置排序，然后用栈模拟相向碰撞。
    """
    n = len(positions)

    # 1) 把每个机器人打包，记住原始下标，方便最后恢复顺序
    robots = [
        (positions[i], healths[i], directions[i], i)   # (pos, hp, dir, original_index)
        for i in range(n)
    ]
    # 2) 按位置从左到右排序
    robots.sort(key=lambda x: x[0])

    # 栈中存放仍然存活的机器人信息： [ [hp, dir, idx] , ... ]
    stack = []

    for pos, hp, d, idx in robots:
        if d == 'R':
            # 向右的机器人先入栈，等待后面的左向机器人来碰撞
            stack.append([hp, d, idx])
        else:   # d == 'L'，向左的机器人需要和栈顶的右向机器人碰撞
            cur_hp = hp
            while cur_hp > 0 and stack and stack[-1][1] == 'R':
                top_hp, _, top_idx = stack[-1]

                if top_hp < cur_hp:
                    # 栈顶右向机器人血量更少，先死，左向机器人血量减 1
                    cur_hp -= 1
                    stack.pop()                # 右向机器人出栈
                elif top_hp == cur_hp:
                    # 两者血量相等，互相抵消，都死
                    stack.pop()
                    cur_hp = 0                 # 左向机器人也死
                    break
                else:  # top_hp > cur_hp
                    # 右向机器人更强，左向机器人死，右向机器人血量减 1
                    stack[-1][0] -= 1
                    cur_hp = 0                 # 左向机器人死亡，结束循环
                    break

            # 若左向机器人仍然存活（没有右向机器人可以碰撞或已把所有右向机器人击退），
            # 它会继续向左移动，后面再也不可能和左边的机器人相撞，
            # 所以直接把它加入栈中（方向仍是 L，方便后面统一收集）。
            if cur_hp > 0:
                stack.append([cur_hp, 'L', idx])

    # 3) 栈中剩下的机器人全部是最终存活的，按照原始下标恢复顺序
    survivors = sorted(stack, key=lambda x: x[2])   # 按原始下标升序
    return [hp for hp, _, _ in survivors]
```

> **代码要点注释**  
> - `robots.sort(key=lambda x: x[0])`：把机器人排成“一条直线”，左边先处理。  
> - `stack.append([hp, d, idx])`：把向右的机器人暂存，等左向来袭时配对。  
> - `while cur_hp > 0 and stack and stack[-1][1] == 'R'`：只和最近的、仍然向右的机器人碰撞。  
> - `stack.pop()`：右向机器人血量更低，直接从栈里踢出去。  
> - `stack[-1][0] -= 1`：右向机器人血量大于左向，它存活但血量减 1。  
> - `if cur_hp > 0: stack.append([cur_hp, 'L', idx])`：左向机器人若全胜，则加入栈，后面再也不会与其他机器人碰撞（因为后面只会出现更右侧的机器人）。  
> - 最后 `sorted(..., key=lambda x: x[2])` 把存活机器人按原来的下标排序，得到答案顺序。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，遍历一次栈的操作每个机器人最多进栈一次、出栈一次，整体是线性的 `O(n)`。  
  - 与暴力的 `O(n²)` 相比，**只多了一次排序**，大大提升效率。  
  - 用大白话讲：把 100,000 辆车先排好队（花 100,000·log2(100,000)≈1.7M 步），之后每辆车只检查一次，整体快了几个数量级。

- **空间复杂度**：`O(n)`  
  - 需要额外的数组 `robots`（存放排序后的信息）以及栈，最坏情况下所有机器人都可能进入栈中，空间与输入规模同量级。  
  - 这已经是最优的，因为我们必须保存每个机器人的健康信息以便最终返回。

---

## 心得

- **核心技巧**：**单调栈 + 按位置排序** 用来一次性解决“相向碰撞”这类**最近配对**问题。  
- **适用的题型**（类似思路）  
  1. **LeetCode 2741 – Robot Collisions**（本题）  
  2. **LeetCode 735 – Asteroid Collision**（小行星相撞）  
  3. **LeetCode 2255 – Count Prefixes of a Given String**（使用栈处理前缀匹配）  
- **一句话总结**：**把向右的机器人压栈，向左的机器人从栈顶“逐个拔枪”消灭最左侧的右向机器人，整个过程只需一次遍历**。

---

## 反思

- **第一反应**：看到“相向移动的机器人会相撞”，立刻想到**模拟每一步**，于是想到暴力的“每次碰撞后重新遍历”。  
- **最容易踩的坑**  
  - **位置未排序**：直接按输入顺序处理会导致左边的右向机器人先被错误地忽略。  
  - **血量递减时机**：只有在两者都存活的情况下才减 1，忘记这点会导致结果偏小。  
  - **左向机器人全胜后仍需入栈**：否则后面出现更左侧的左向机器人会错过配对。  
  - **返回顺序**：题目要求**保持原始下标顺序**，忘记恢复顺序会导致答案不匹配。  
- **下次类似题目**的第一步**：先把对象按**“空间位置”**排序，再考虑**“最近的相向配对”**，看看能否用栈或单调结构一次完成配对。这样可以迅速从 O(n²) 的暴力思路跳到 O(n log n)。