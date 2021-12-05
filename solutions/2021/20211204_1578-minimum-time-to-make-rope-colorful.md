# #1578. 使绳子彩色的最小时间 / Minimum Time to Make Rope Colorful

> 难度：中等 · 标签：Array、String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-make-rope-colorful/)

---

## 题目（英文原版）

**Description**

Alice has n balloons arranged on a rope. You are given a 0-indexed string colors where colors[i] is the color of the ith balloon.
Alice wants the rope to be colorful. She does not want two consecutive balloons to be of the same color, so she asks Bob for help. Bob can remove some balloons from the rope to make it colorful. You are given a 0-indexed integer array neededTime where neededTime[i] is the time (in seconds) that Bob needs to remove the ith balloon from the rope.
Return the minimum time Bob needs to make the rope colorful.

**Examples**

**Example 1:**

```
Input: colors = "abaac", neededTime = [1,2,3,4,5]
Output: 3
Explanation: In the above image, 'a' is blue, 'b' is red, and 'c' is green.
Bob can remove the blue balloon at index 2. This takes 3 seconds.
There are no longer two consecutive balloons of the same color. Total time = 3.
```

**Example 2:**

```
Input: colors = "abc", neededTime = [1,2,3]
Output: 0
Explanation: The rope is already colorful. Bob does not need to remove any balloons from the rope.
```

**Example 3:**

```
Input: colors = "aabaa", neededTime = [1,2,3,4,1]
Output: 2
Explanation: Bob will remove the balloons at indices 0 and 4. Each balloons takes 1 second to remove.
There are no longer two consecutive balloons of the same color. Total time = 1 + 1 = 2.
```

**Constraints**

- n == colors.length == neededTime.length
- 1 <= n <= 105
- 1 <= neededTime[i] <= 104
- colors contains only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
Alice 在一根绳子上排列了 `n` 个气球。给定一个下标从 **0** 开始的字符串 `colors`，其中 `colors[i]` 表示第 `i` 个气球的颜色。  
Alice 希望绳子呈现彩色，即**相邻的两个气球颜色不能相同**，于是她请 Bob 帮忙。Bob 可以从绳子上移除若干气球来实现这一目标。给定一个下标从 **0** 开始的整数数组 `neededTime`，其中 `neededTime[i]` 表示 Bob 移除第 `i` 个气球所需的时间（秒）。  
请返回 Bob 使绳子彩色所需的**最少时间**。

**示例**  

*示例 1*  
```
Input: colors = "abaac", neededTime = [1,2,3,4,5]
Output: 3
Explanation: 如上图所示，'a' 为蓝色，'b' 为红色，'c' 为绿色。  
Bob 可以移除下标为 2 的蓝色气球，耗时 3 秒。此后不存在相邻颜色相同的气球。总时间 = 3。
```

*示例 2*  
```
Input: colors = "abc", neededTime = [1,2,3]
Output: 0
Explanation: 绳子已经是彩色的，Bob 不需要移除任何气球。
```

*示例 3*  
```
Input: colors = "aabaa", neededTime = [1,2,3,4,1]
Output: 2
Explanation: Bob 移除下标 0 和 4 的气球，每个气球耗时 1 秒。  
此后不存在相邻颜色相同的气球。总时间 = 1 + 1 = 2。
```

**约束条件**  
- `n == colors.length == neededTime.length`
- `1 <= n <= 10^5`
- `1 <= neededTime[i] <= 10^4`
- `colors` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步** 把绳子检查一遍，只要发现相邻的两个气球颜色相同，就把其中 **耗时更少** 的那个气球删掉。  
删掉以后，绳子会短一些，后面的气球会向前“搬家”，于是需要 **重新从头开始** 检查，直到整根绳子里没有相邻相同的颜色为止。

- **使用的数据结构**：  
  - `list`（列表）保存颜色字符，类似于我们手里的一串气球。  
  - `list` 保存对应的删除时间，像是每个气球的“标签”。  
  - 这里可以把 `list` 想象成 **字典**（查字典的过程），只不过我们用下标来定位每个气球。

- **为什么正确**：  
  - 每一次我们都把一对相同颜色的气球中 **更便宜** 的那个删掉。  
  - 只要还有相邻相同的颜色，就继续删，最终必然得到“没有相邻相同颜色”的绳子。  
  - 因为每一次删的都是当前最便宜的选项，整个过程不会错过更优解。

- **时间/空间复杂度**：  
  - 每删掉一个气球，都要把后面的所有气球往前搬一次，相当于一次 **O(n)** 的移动。  
  - 最坏情况是所有气球颜色都相同，需要删掉 `n‑1` 次，所以总时间是 **O(n²)**。  
  - 只用了原来的两个列表，额外空间是 **O(1)**（不计输入本身）。

> 大白话解释：如果把绳子想象成排队的学生，两个相邻的同学穿同样的衣服就要让其中一个离开。离开后，后面的同学要往前挤一个位置，这个“挤位子”过程要花时间。最坏情况下，每次都要挤一次，挤 `n` 次，挤 `n` 次——于是时间是 `n × n`。

#### 代码（Python）

```python
def minCost_bruteforce(colors: str, neededTime: list[int]) -> int:
    # 把字符串转成列表，方便删除操作
    colors = list(colors)
    neededTime = list(neededTime)

    total = 0                     # 累计已经花掉的时间
    i = 0                         # 当前检查的位置

    while i < len(colors) - 1:    # 只要还有后面一个气球
        if colors[i] == colors[i + 1]:          # 相邻颜色相同
            # 删除耗时更少的那个
            if neededTime[i] <= neededTime[i + 1]:
                total += neededTime[i]          # 加上删除的时间
                del colors[i]                   # 删除颜色
                del neededTime[i]               # 同时删除对应的时间
            else:
                total += neededTime[i + 1]
                del colors[i + 1]
                del neededTime[i + 1]
            # 删除后，需要从头重新检查，因为搬位可能产生新的相邻相同
            i = 0
        else:
            i += 1                # 颜色不同，继续向后检查

    return total
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：最坏情况下每删一次都要把后面的元素整体左移，左移的代价是 `O(n)`，而要删 `n‑1` 次，所以是 `n × n`。
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只在原列表上原地删除，没有额外的大数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每次只处理一对相同颜色的气球，而实际上如果有一串 **连续相同颜色的气球**（比如 `"aaa"`），我们一次就可以决定要保留哪一个，删掉其余的。

**关键观察**：

- 对于一段连续相同颜色的子串（记作一个 “组”），要让绳子变得“彩色”，**必须**删除除 **一个** 气球以外的全部气球。  
- 为了 **最小化删除时间**，我们应该 **保留耗时最大的那个气球**，因为把它留下可以省掉最大的时间。于是该组需要删除的时间就是 **组内所有时间之和 - 组内最大时间**。

因此只要一次遍历，把相同颜色的连续块划分出来，累计它们的时间总和和最大值，最后把 **总和 - 最大值** 加到答案中即可。

**核心算法/数据结构**：

- **一次线性扫描**（双指针思路）  
  - `i` 指向当前组的起始位置，`j` 向右移动直到颜色变化为止。  
- **组内统计**：  
  - `group_sum` 保存该组所有 `neededTime` 的累计和。  
  - `group_max` 保存该组最大的 `neededTime`。  
  - 这两个数相减就是该组需要付出的最小删除时间。

**类比**：  
把每个颜色相同的气球看作“一堆相同颜色的球”。我们要挑出这堆里“最贵的球”留下，其他的全部卖掉（删除），卖掉的总价就是我们要付出的时间。

#### 代码（Python）

```python
def minCost(colors: str, neededTime: list[int]) -> int:
    """
    贪心 + 一次遍历
    对每个连续相同颜色的子串，只保留耗时最大的气球，其余全部删除。
    """
    n = len(colors)
    ans = 0                     # 最终答案
    i = 0                       # 当前组的起始下标

    while i < n:
        # 统计以 i 为起点、颜色相同的连续子串
        group_sum = neededTime[i]   # 该组时间之和
        group_max = neededTime[i]   # 该组的最大时间
        j = i + 1
        while j < n and colors[j] == colors[i]:
            group_sum += neededTime[j]
            group_max = max(group_max, neededTime[j])
            j += 1

        # 该组需要删除的时间 = 总和 - 最大值
        ans += group_sum - group_max

        # 继续处理下一个组
        i = j

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，每个字符进入循环一次，常数操作（加、比较）不影响数量级。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量来记录当前组的统计信息，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：在同一颜色的连续块中，只保留耗时最大的气球，其余全部删除（**贪心**）。  
- **适用的题型**：  
  1. “把相邻相同元素合并或删除” 类问题（如 LeetCode 1658 *"Minimum Operations to Reduce X to Zero"* 中的类似思路）。  
  2. “同类物品中保留最贵/最值的一个” 类问题（如 1647 *"Minimum Deletions to Make Character Frequencies Unique"*）。  
  3. “区间划分后对每段做统计” 的动态规划或贪心题目（如 1220 *"Count Vowel Permutation"* 的分段统计）。  
- **一句话总结**：**“同色相邻必删，删时保留最贵”。**

---

## 反思

- **拿到题目第一反应**：先想到逐对比较、一次删一个，结果是 **暴力 O(n²)** 的思路。  
- **最容易踩的坑**：  
  - 忘记 **同一组可能有超过两个** 相同颜色的气球，需要一次性处理整组。  
  - 没有正确维护 **组内最大时间**，导致错误地把最大值也算进删除时间。  
  - 边界条件：整个字符串只有一种颜色，或所有颜色都不相同，都必须能正确返回 `0`。  
- **下次遇到同类题的第一步**：先 **划分连续相同的子串**，思考在每个子串内部“保留哪个、删除哪些”，再决定整体的最小代价。这样常能直接得到 **线性贪心** 解法。