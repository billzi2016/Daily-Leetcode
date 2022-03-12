# #1700. 学生无法进餐的数量 / Number of Students Unable to Eat Lunch

> 难度：简单 · 标签：Array、Stack、Queue、Simulation · [LeetCode 链接](https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/)

---

## 题目（英文原版）

**Description**

The school cafeteria offers circular and square sandwiches at lunch break, referred to by numbers 0 and 1 respectively. All students stand in a queue. Each student either prefers square or circular sandwiches.
The number of sandwiches in the cafeteria is equal to the number of students. The sandwiches are placed in a stack. At each step:
This continues until none of the queue students want to take the top sandwich and are thus unable to eat.
You are given two integer arrays students and sandwiches where sandwiches[i] is the type of the i​​​​​​th sandwich in the stack (i = 0 is the top of the stack) and students[j] is the preference of the j​​​​​​th student in the initial queue (j = 0 is the front of the queue). Return the number of students that are unable to eat.

**Examples**

**Example 1:**

```
Input: students = [1,1,0,0], sandwiches = [0,1,0,1]
Output: 0 
Explanation:
- Front student leaves the top sandwich and returns to the end of the line making students = [1,0,0,1].
- Front student leaves the top sandwich and returns to the end of the line making students = [0,0,1,1].
- Front student takes the top sandwich and leaves the line making students = [0,1,1] and sandwiches = [1,0,1].
- Front student leaves the top sandwich and returns to the end of the line making students = [1,1,0].
- Front student takes the top sandwich and leaves the line making students = [1,0] and sandwiches = [0,1].
- Front student leaves the top sandwich and returns to the end of the line making students = [0,1].
- Front student takes the top sandwich and leaves the line making students = [1] and sandwiches = [1].
- Front student takes the top sandwich and leaves the line making students = [] and sandwiches = [].
Hence all students are able to eat.
```

**Example 2:**

```
Input: students = [1,1,1,0,0,1], sandwiches = [1,0,0,0,1,1]
Output: 3
```

**Constraints**

- 1 <= students.length, sandwiches.length <= 100
- students.length == sandwiches.length
- sandwiches[i] is 0 or 1.
- students[i] is 0 or 1.

---

## 题目（中文翻译）

学校食堂在午休时提供圆形和方形三明治，分别用数字 **0**（circular sandwich）和 **1**（square sandwich）表示。所有学生排成一个队列，每个学生都有自己偏好的三明治类型。  
食堂里三明治的数量与学生人数相同，三明治按堆叠顺序摆放。每一次操作如下：

1. 观察队首的学生 `students[0]` 与堆顶的三明治 `sandwiches[0]`。  
2. **如果** 两者类型相同，学生拿走该三明治并离开队列，三明治也从堆中移除。  
3. **否则**，学生不拿三明治，直接走到队列的末尾。  

上述过程会一直进行，直到出现以下情况：**没有任何学生想要当前堆顶的三明治**，此时剩余的学生都无法进餐。  

给定两个整数数组 `students` 和 `sandwiches`，其中 `sandwiches[i]` 表示第 `i` 个三明治的类型（`i = 0` 为堆顶），`students[j]` 表示第 `j` 位学生的偏好（`j = 0` 为队首），返回无法进餐的学生人数。

**示例 1**  
```
Input: students = [1,1,0,0], sandwiches = [0,1,0,1]
Output: 0
Explanation:
- 队首学生（偏好 1）不想要堆顶三明治 0，走到队尾 → students = [1,0,0,1]
- 队首学生（偏好 1）仍不想要堆顶三明治 0，走到队尾 → students = [0,0,1,1]
- 队首学生（偏好 0）拿走堆顶三明治 0，离开队列 → students = [0,1,1], sandwiches = [1,0,1]
- 队首学生（偏好 0）拿走堆顶三明治 1（不匹配），走到队尾 → students = [1,1,0]
- 队首学生（偏好 1）拿走堆顶三明治 1，离开队列 → students = [1,0], sandwiches = [0,1]
- 队首学生（偏好 1）不想要堆顶三明治 0，走到队尾 → students = [0,1]
- 队首学生（偏好 0）拿走堆顶三明治 0，离开队列 → students = [1], sandwiches = [1]
- 队首学生（偏好 1）拿走最后的三明治 1，离开队列 → students = [], sandwiches = []
所有学生都吃到了三明治，返回 0。
```

**示例 2**  
```
Input: students = [1,1,1,0,0,1], sandwiches = [1,0,0,0,1,1]
Output: 3
```

**约束条件**

- `1 <= students.length, sandwiches.length <= 100`
- `students.length == sandwiches.length`
- `sandwiches[i]` 为 `0` 或 `1`
- `students[i]` 为 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**严格按照题目描述**去模拟整个排队和发三明治的过程。  

- 用 **队列**（在 Python 中可以用 `collections.deque`）来保存学生的喜好顺序，队首对应排在最前面的学生。  
- 用 **栈**（这里用列表的下标）来保存三明治的顺序，`sandwiches[0]` 是最上面的那块。  
- 每一次取出栈顶三明治，检查队首学生是否喜欢它：  
  - 如果喜欢，就把学生出队（吃掉三明治），栈指针向后移动一位。  
  - 如果不喜欢，就把学生移动到队尾，继续检查下一个学生。  
- 为了防止出现“所有学生都不喜欢当前三明治，却一直循环检查”的死循环，需要记录本轮 **已经检查过的学生数**。如果在一次完整的循环（检查了队列中所有学生）里没有人吃掉栈顶三明治，说明剩下的学生都不可能吃到任何三明治，直接结束。

> 类比：队列像是排队买咖啡的顾客，三明治栈像是咖啡机里只能按顺序取出的咖啡杯。顾客若不喜欢当前咖啡，就只能让他回到队尾继续等。

这个方法一定能得到正确答案，因为它完全复现了题目中“每一步都要么吃，要么让学生回到队尾”的规则。

#### 代码（Python）  

```python
from collections import deque
from typing import List

def countStudents(students: List[int], sandwiches: List[int]) -> int:
    # 用 deque 维护学生队列，左侧是队首
    q = deque(students)
    # 用下标指向当前要发的三明治，0 表示栈顶
    idx = 0
    # 记录连续检查但没有人吃掉三明治的学生数
    checked = 0

    while q and idx < len(sandwiches):
        # 队首学生的喜好
        pref = q[0]
        # 当前三明治的类型
        sand = sandwiches[idx]

        if pref == sand:
            # 学生吃掉三明治，出队，指向下一块三明治
            q.popleft()
            idx += 1
            # 吃掉后，重新计数，因为已经有人成功吃了
            checked = 0
        else:
            # 学生不喜欢，移到队尾
            q.rotate(-1)   # 相当于 pop 左侧再 append 右侧
            # 本轮检查的学生数加 1
            checked += 1

        # 如果一轮检查了所有学生仍然没有人吃掉当前三明治
        # 说明剩下的学生全部不喜欢这块三明治，直接结束
        if checked == len(q):
            break

    # 队列中剩余的学生就是无法吃到三明治的人数
    return len(q)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（最坏情况）  
  - `n` 为学生/三明治的数量。  
  - 当所有学生都不喜欢当前三明治时，需要把整个队列循环一遍（`O(n)`），而这种情况最坏会发生 `n` 次，所以总体是 `O(n * n)`。  
  - 用大白话说，就是“每个人可能要检查每块三明治一次”。  

- **空间复杂度**：`O(n)`  
  - 需要一个队列保存所有学生的喜好，额外使用的空间与输入规模成正比。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的卡点**在于我们不停地把不喜欢当前三明治的学生转到队尾，导致大量无用的循环。  
实际上，我们不必真的模拟每一次“转圈”，只要知道**还有多少学生喜欢 0，多少学生喜欢 1**就够了。  

关键观察：

1. 三明治的顺序是固定的，我们只能按照这个顺序依次发出。  
2. 当栈顶三明治的类型为 `t` 时，只要还有学生**偏好是 `t`**，一定可以让其中的一个学生吃掉这块三明治（不管他现在在队列的哪个位置），因为循环转移最终会把这个学生带到队首。  
3. 只要某种类型的三明治出现，而对应的学生偏好已经为 0，说明**剩下的所有学生都不喜欢这块以及后面的所有三明治**，因为后面的三明治只能是 0 或 1，而我们已经没有对应偏好的学生了。此时直接返回剩余学生数即可。

因此算法步骤：

- 先遍历 `students`，统计喜欢圆形（0）和方形（1）三明治的学生人数，记作 `cnt0`、`cnt1`。这一步相当于把学生信息压缩成两个计数器，类似把“字典”想象成 **查字典**：键是喜好，值是人数。  
- 再依次遍历 `sandwiches`（即栈的顺序）：
  - 若当前三明治是 0 且 `cnt0 > 0`，则让一个喜欢 0 的学生吃掉，`cnt0 -= 1`。  
  - 若当前三明治是 1 且 `cnt1 > 0`，则让一个喜欢 1 的学生吃掉，`cnt1 -= 1`。  
  - 否则（对应计数为 0），说明没有学生能吃这块三明治，直接返回 `cnt0 + cnt1`（即剩余学生数）。  
- 循环结束后，所有三明治都被吃掉，返回 0。

这一步只需要一次遍历，时间线性，空间只用了两个整数。

#### 代码（Python）  

```python
from typing import List

def countStudents(students: List[int], sandwiches: List[int]) -> int:
    # 统计学生对 0（圆形）和 1（方形）的偏好人数
    cnt = [0, 0]          # cnt[0] = 喜欢 0 的人数，cnt[1] = 喜欢 1 的人数
    for s in students:
        cnt[s] += 1

    # 按照三明治的顺序依次尝试发放
    for sand in sandwiches:
        if cnt[sand] > 0:        # 还有人喜欢当前这块三明治
            cnt[sand] -= 1      # 让其中一个学生吃掉
        else:
            # 没有人喜欢这块三明治，后面的也无法被吃
            return cnt[0] + cnt[1]

    # 所有三明治都被吃完，没人剩下
    return 0
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历两遍数组（一次统计，一次发放），每一步都是常数时间。  
  - 与暴力解相比，省掉了大量的“转圈”操作，真正的运行时间大幅下降。  

- **空间复杂度**：`O(1)`  
  - 只用了一个长度为 2 的计数数组，空间使用不随 `n` 增长。  

---  

## 心得  

- 这道题核心考察**统计与模拟的取舍**：先想到模拟很自然，但要发现可以用**计数**代替完整的队列操作。  
- 类似技巧常用于**“只关心数量而不关心顺序”**的题目，例如：  
  1. `Number of Steps to Reduce a Number to Zero`（统计奇偶）  
  2. `Assign Cookies`（用计数匹配需求）  
  3. `Find the Difference of Two Arrays`（计数差异）  
- **解题钥匙**：先判断“是否真的需要完整模拟”，若只关心“还有多少人满足条件”，用计数即可。  

---  

## 反思  

- **第一反应**：看到“队列”和“栈”就想直接用 `deque`+循环模拟。  
- **最容易踩的坑**：  
  - 忘记在暴力模拟中加入“检查整队仍无人吃掉” 的退出条件，会导致无限循环。  
  - 计数法需要注意边界：当三明治种类不匹配时，要一次性返回剩余学生总数，而不是继续循环。  
- **下次遇到同类题**：第一步先问自己“我真的需要保留每个人的具体位置吗？”如果答案是否定的，就立刻转向**计数/哈希表**的思路。