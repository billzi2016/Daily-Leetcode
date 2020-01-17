# #735. 小行星碰撞 / Asteroid Collision

> 难度：中等 · 标签：Array、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/asteroid-collision/)

---

## 题目（英文原版）

**Description**

We are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space.
For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.
Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

**Examples**

**Example 1:**

```
Input: asteroids = [5,10,-5]
Output: [5,10]
Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.
```

**Example 2:**

```
Input: asteroids = [8,-8]
Output: []
Explanation: The 8 and -8 collide exploding each other.
```

**Example 3:**

```
Input: asteroids = [10,2,-5]
Output: [10]
Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide resulting in 10.
```

**Constraints**

- 2 <= asteroids.length <= 104
- -1000 <= asteroids[i] <= 1000
- asteroids[i] != 0

---

## 题目（中文翻译）

我们给定一个整数数组 `asteroids`，表示一排小行星。数组中的下标对应它们在空间中的相对位置。  
对于每颗小行星，**绝对值**表示其大小，**符号**表示其运动方向（正数表示向右移动，负数表示向左移动）。所有小行星的速度相同。  

求所有碰撞结束后，小行星的最终状态。  
- 当两颗小行星相遇时，尺寸较小的会爆炸。  
- 若两颗小行星尺寸相同，则两者同时爆炸。  
- 同向运动的两颗小行星永远不会相遇。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `2 <= asteroids.length <= 10^4`  
- `-1000 <= asteroids[i] <= 1000`  
- `asteroids[i] != 0`

### 示例

**示例 1**  
```
Input: asteroids = [5,10,-5]
Output: [5,10]
Explanation: 10 和 -5 碰撞后只剩下 10。5 和 10 永远不会相撞。
```

**示例 2**  
```
Input: asteroids = [8,-8]
Output: []
Explanation: 8 与 -8 碰撞后相互爆炸，结果为空数组。
```

**示例 3**  
```
Input: asteroids = [10,2,-5]
Output: [10]
Explanation: 2 与 -5 碰撞后只剩下 -5。随后 10 与 -5 碰撞，剩下 10。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是模拟每一颗小行星的运动，**一次遍历**就把它们全部放进一个“宇宙”里，然后每次检查相邻的两颗小行星是否会相撞：

1. **相撞的条件**  
   - 前一颗向右（正数），后一颗向左（负数）。只有这两种方向相对而行时才会相遇。  
   - 其它组合（比如 `+ +`、`- -`、`- +`）永远不会相撞，因为它们要么同向、要么背向而行。

2. **相撞的结果**  
   - 比大小：绝对值大的小行星存活，另一颗爆炸。  
   - 大小相等：两颗都爆炸。

3. **模拟过程**  
   - 从左到右遍历数组，用一个列表 `res` 保存“当前宇宙”的状态。  
   - 对于每颗新来的小行星 `a`，不停地和 `res` 最后一颗（即最近的左侧小行星）比较，直到：
     * `res` 为空，或
     * `res` 最后的小行星向左（负数）——这意味着它们永远不会相遇，或者
     * `a` 存活下来（比对手大），或者
     * 两颗同归于尽（大小相等），此时把 `res` 的最后一颗弹出并且不把 `a` 加入。

   这段“不停比较”其实就是 **暴力** 的核心：每次新来一个小行星，都可能要和左边所有还在的右向小行星逐个碰撞。

**为什么正确**  
因为我们严格按照题目给出的“相同速度、相向而行即相撞”规则，逐步消除所有可能的碰撞，最终留下的就是所有不会再相遇的小行星。

**时间/空间复杂度**  
- 最坏情况下，每加入一颗小行星都要和之前的所有右向小行星碰撞一次。设 `n` 为小行星数量，时间复杂度是 `O(n²)`。  
  > 用大白话说，`O(n²)` 就像我们让每个人和前面所有人都握手，一共要握手 `n*(n-1)/2` 次，随着 `n` 增大，次数会呈“平方”增长，算起来会很慢。  
- 需要一个额外的列表保存当前状态，最坏情况下会存 `n` 颗小行星，空间复杂度是 `O(n)`。

#### 代码（Python）

```python
from typing import List

def asteroidCollision_bruteforce(asteroids: List[int]) -> List[int]:
    # 用列表模拟栈，存放已经确定不会再碰撞的小行星
    res: List[int] = []

    for a in asteroids:                     # 依次处理每颗小行星
        # 当出现“右向小行星 + 左向小行星”时，需要碰撞
        while res and res[-1] > 0 and a < 0:
            # 左向小行星 a 与栈顶右向小行星进行比较
            if abs(res[-1]) < abs(a):       # 栈顶小行星更小，爆炸
                res.pop()                  # 把它移除，继续比较下一个栈顶
                continue                   # 继续 while 循环，a 仍在待处理
            elif abs(res[-1]) == abs(a):   # 大小相同，两颗一起爆炸
                res.pop()                  # 移除栈顶
                break                      # a 也不放进结果，直接结束 while
            else:                           # 栈顶小行星更大，a 爆炸
                break                      # a 被消灭，结束 while

        else:
            # while 循环正常结束（没有 break），说明 a 没有被炸掉
            res.append(a)                  # 把 a 加入结果列表

    return res
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 这里的 `n` 是小行星的数量。因为每颗小行星最坏可能要和左侧所有已经保留的右向小行星比较一次，比较次数会随 `n` 的增长呈平方级别。

- **空间复杂度**：`O(n)`  
  > 需要额外的列表 `res` 来存放最终状态，最坏情况下所有小行星都保留下来，长度为 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要从头遍历**左侧所有右向小行星。其实我们只需要关注**最近的可能相撞对象**——即栈顶的右向小行星。因为：

- 如果栈顶是左向（负数）或者空，说明左侧没有可以相撞的右向小行星，后面的更左边的右向小行星更不可能相撞（它们之间已经被左向小行星“隔开”）。
- 只有栈顶是右向（正数）时，才会与新来的左向小行星产生冲突。冲突后，要么栈顶被炸掉，要么新小行星被炸掉，或者两者同归于尽。**一旦栈顶处理完毕，后面的右向小行星自然不需要再检查**。

这正好对应**单调栈**的思路：我们维护一个**只保留可能会相撞的小行星**的栈（这里的栈其实就是前面代码里的 `res`），每加入一个新小行星，只和栈顶比较，必要时弹出栈顶继续比较，直到不再有冲突为止。

具体步骤：

1. 初始化空栈 `stack`。
2. 遍历 `asteroids` 中的每个小行星 `a`：
   - 当 `stack` 不为空且 `stack[-1] > 0`（右向）且 `a < 0`（左向）时，说明即将碰撞，需要比较大小。
   - **三种情况**：
     - `abs(a) > stack[-1]` → 栈顶右向小行星被炸，弹出栈顶，继续与新的栈顶比较（因为 `a` 仍然在）。
     - `abs(a) == stack[-1]` → 两颗同归于尽，弹出栈顶，`a` 也不入栈，结束当前循环。
     - `abs(a) < stack[-1]` → `a` 被炸，直接结束循环，不入栈。
   - 如果上面的 `while` 循环正常结束（没有因为 `a` 被炸而 `break`），说明 `a` 没有再相撞的对象，直接把 `a` 入栈。
3. 循环结束后，栈中从左到右的顺序即为最终的宇宙状态。

**核心数据结构：栈（list）**  
- 栈像“一摞盘子”，只能在最上面（栈顶）放进或拿出东西。这里用它来记录**左侧仍然活着、且方向向右的小行星**，因为只有它们可能和后面来的左向小行星碰撞。

**为什么是最优**  
- 每颗小行星最多进栈一次、出栈一次，整个过程只遍历一次数组，时间复杂度是 `O(n)`，大幅降低了暴力解的平方级别开销。

#### 代码（Python）

```python
from typing import List

def asteroidCollision(asteroids: List[int]) -> List[int]:
    """
    使用栈一次遍历完成碰撞模拟，时间 O(n)，空间 O(n)。
    """
    stack: List[int] = []                     # 栈中保存当前存活的小行星

    for a in asteroids:                       # 逐个处理
        # 只要栈顶是向右的（>0）且当前小行星向左（<0），就可能碰撞
        while stack and stack[-1] > 0 and a < 0:
            # 栈顶右向小行星的大小
            top = stack[-1]

            if abs(a) > top:                  # a 更大，栈顶被炸
                stack.pop()                   # 弹出栈顶，继续比较下一个栈顶
                continue                      # a 仍在，继续 while 循环

            elif abs(a) == top:               # 大小相等，两颗同归于尽
                stack.pop()                   # 弹出栈顶
                break                         # a 也不入栈，直接结束 while

            else:                              # 栈顶更大，a 被炸
                break                         # a 不入栈，结束 while

        else:
            # while 正常结束（没有 break），说明 a 没有被炸
            stack.append(a)                   # 把 a 放进栈中

    return stack
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  > 每颗小行星至多进栈一次、出栈一次，整个过程只遍历一次数组。相比暴力的 `O(n²)`，即使 `n` 达到 10⁴，运行时间也几乎是瞬间完成。

- **空间复杂度**：`O(n)`  
  > 最坏情况下所有小行星都朝同一方向，根本不会相撞，栈会保存全部 `n` 颗小行星。

---

## 心得

- **核心技巧**：利用栈一次遍历模拟“相向而行的碰撞”。栈帮助我们只关注最近的可能相撞对象，避免了重复比较。
- **适用题型**  
  1. **括号匹配**（如 “Valid Parentheses”）——栈用于记录左括号，遇到右括号时配对。  
  2. **每日温度**（“Daily Temperatures”）——单调栈记录温度，找到下一个更高的温度。  
  3. **柱状图中最大的矩形**（“Largest Rectangle in Histogram”）——单调栈维护递增的柱高，快速计算面积。
- **一句话总结**：**“只保留最近的可能相撞对象，用栈把它们‘压在一起’，碰撞就能在 O(1) 时间内决定。”**

## 反思

- **第一反应**：看到“相向而行、同速、相撞”会想到**两两比较**，于是直接写了双层循环的暴力模拟。
- **最容易踩的坑**  
  1. **方向判断错误**：只有“右向 + 左向”才会相撞，别忘了排除 `- +`、`+ +`、`- -`。  
  2. **同归于尽的处理**：大小相等时，两颗都要消失，记得弹出栈顶并且不把当前小行星入栈。  
  3. **边界条件**：全正或全负的数组直接返回原数组，栈的 `while` 条件要写得严谨，防止空栈访问。  
- **下次遇到类似题**：第一步先**把问题抽象为“只有最近的左侧元素会影响当前元素”**，如果成立，就立刻考虑**单调栈**或**双指针**来做到线性遍历。这样可以快速从暴力思路跳到最优解。