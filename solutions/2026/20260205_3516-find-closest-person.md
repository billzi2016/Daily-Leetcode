# #3516. 寻找最近的人 / Find Closest Person

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/find-closest-person/)

---

## 题目（英文原版）

**Description**

You are given three integers x, y, and z, representing the positions of three people on a number line:
Both Person 1 and Person 2 move toward Person 3 at the same speed.
Determine which person reaches Person 3 first:
Return the result accordingly.

**Examples**

**Example 1:**

```
Input: x = 2, y = 7, z = 4
Output: 1
Explanation:
Since Person 1 reaches Person 3 first, the output is 1.
```

**Example 2:**

```
Input: x = 2, y = 5, z = 6
Output: 2
Explanation:
Since Person 2 reaches Person 3 first, the output is 2.
```

**Example 3:**

```
Input: x = 1, y = 5, z = 3
Output: 0
Explanation:
Since both Person 1 and Person 2 reach Person 3 at the same time, the output is 0.
```

**Constraints**

- 1 <= x, y, z <= 100

---

## 题目（中文翻译）

**题目描述**  
给定三个整数 `x`、`y` 和 `z`，它们分别表示三个人在数轴 (number line) 上的位置。  
人物 1 和人物 2 以相同的速度向人物 3 移动。  
请判断哪一个人物先到达人物 3，返回对应的结果。

**返回值约定**  
- 返回 `1`：人物 1 先到达人物 3。  
- 返回 `2`：人物 2 先到达人物 3。  
- 返回 `0`：人物 1 与人物 2 同时到达人物 3。

**示例**  

示例 1:  
```
Input: x = 2, y = 7, z = 4
Output: 1
Explanation:
Since Person 1 reaches Person 3 first, the output is 1.
```
**解释**：人物 1 距离人物 3 最近，先到达，所以输出 `1`。

示例 2:  
```
Input: x = 2, y = 5, z = 6
Output: 2
Explanation:
Since Person 2 reaches Person 3 first, the output is 2.
```
**解释**：人物 2 距离人物 3 最近，先到达，所以输出 `2`。

示例 3:  
```
Input: x = 1, y = 5, z = 3
Output: 0
Explanation:
Since both Person 1 and Person 2 reach Person 3 at the same time, the output is 0.
```
**解释**：人物 1 与人物 2 同时到达人物 3，返回 `0`。

**约束条件**  
- `1 <= x, y, z <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
这道题的本质是比较 **两个人到第三个人的距离**，谁的距离更短，谁就先到达。  
- **距离** 可以用绝对值 `|a - b|` 表示，等价于在数轴上两点之间的步数。  
- 把「距离」想象成「走路的步数」，如果你站在位置 `x`，目标在 `z`，走到目标需要走 `|x - z|` 步。  
- 计算 `d1 = |x - z|`（人 1 到人 3 的距离）和 `d2 = |y - z|`（人 2 到人 3 的距离），比较 `d1` 与 `d2`：  
  - `d1 < d2` → 人 1 更近，返回 `1`  
  - `d1 > d2` → 人 2 更近，返回 `2`  
  - `d1 == d2` → 两人同时到达，返回 `0`

这个思路直接、最笨，因为它不做任何「优化」——只把题目描述的比较过程完整写出来。它一定正确，因为在同速前进的前提下，走的路程少的必定先到。

#### 代码（Python）

```python
def findClosestPerson(x: int, y: int, z: int) -> int:
    """
    计算两个人到第三个人的距离并比较
    :param x: 人 1 的位置
    :param y: 人 2 的位置
    :param z: 人 3 的位置
    :return: 1、2 或 0
    """
    # 计算绝对距离，abs 相当于“数轴上走的步数”
    d1 = abs(x - z)   # 人 1 到 人 3 的步数
    d2 = abs(y - z)   # 人 2 到 人 3 的步数

    if d1 < d2:
        return 1      # 人 1 更近
    elif d1 > d2:
        return 2      # 人 2 更近
    else:
        return 0      # 距离相同，齐头并进
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做了几次算术运算和一次比较，常数时间。  
  *大白话：不管输入数字有多大，程序跑的时间几乎不变。*
- **空间复杂度**：`O(1)` — 只用了几个整数变量，额外占用的内存不随输入规模增长。  

---

### 2. 最优解

#### 思路  
从暴力解可以看到，整个过程已经只用了 **常数时间**，没有任何可以进一步削减的「循环」或「递归」开销。  
因此 **最优解** 与暴力解是同一个实现：直接比较两段距离。  
这里强调「最优」的意义在于帮助大家认识到：

1. **先判断是否已经是 O(1) 的解**：如果是，说明已经达到了时间上的极限。  
2. **不需要额外的数据结构**：哈希表、数组、栈等都没有出现，因为题目本身只需要两次取差并比较。  

如果把「距离」比作「两个人各自走的路程」，我们只需要「量一下尺子」就能知道谁更短，而不必「走遍整条路」去验证。

#### 代码（Python）

```python
def findClosestPerson(x: int, y: int, z: int) -> int:
    """
    最优解：直接比较两段距离，时间、空间均为常数级别。
    """
    d1 = abs(x - z)
    d2 = abs(y - z)

    # 只要比较一次大小即可得到答案
    if d1 < d2:
        return 1
    if d1 > d2:
        return 2
    return 0
```

#### 复杂度

- **时间复杂度**：`O(1)` — 与暴力解相同，已经是最好的。  
- **空间复杂度**：`O(1)` — 同样只用了固定几个整数变量。

---

## 心得

- **核心技巧**：**距离比较**（使用绝对值）。  
- **适用的题型**：  
  1. “谁离目标更近”类问题（如 LeetCode 1791. Find Center of Star Graph）。  
  2. “谁先到达”类问题（如 1657. Determine if Two Strings Are Close）。  
  3. “最近的点”或“最近的数”比较（如 475. Heaters 中的最近暖气片）。  
- **一句话总结解题钥匙**：**把“谁先到”转化为“谁的距离更短”，用绝对值直接比较**。

## 反思

- **第一反应**：看到“同速移动”，自然想到“距离决定先后”。  
- **最容易踩的坑**：  
  - 忽略了负数或位置顺序导致的距离方向错误，使用 `abs` 能避免。  
  - 没考虑相等情况，返回值需要明确为 `0`。  
- **下次遇到同类题**：第一步先 **把“时间”或“先后”转换为“距离”或“步数”，再做比较**。这样往往能直接得到 O(1) 的最优解。