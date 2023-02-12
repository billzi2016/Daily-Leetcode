# #2126. 摧毁小行星 / Destroying Asteroids

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/destroying-asteroids/)

---

## 题目（英文原版）

**Description**

You are given an integer mass, which represents the original mass of a planet. You are further given an integer array asteroids, where asteroids[i] is the mass of the ith asteroid.
You can arrange for the planet to collide with the asteroids in any arbitrary order. If the mass of the planet is greater than or equal to the mass of the asteroid, the asteroid is destroyed and the planet gains the mass of the asteroid. Otherwise, the planet is destroyed.
Return true if all asteroids can be destroyed. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: mass = 10, asteroids = [3,9,19,5,21]
Output: true
Explanation: One way to order the asteroids is [9,19,5,3,21]:
- The planet collides with the asteroid with a mass of 9. New planet mass: 10 + 9 = 19
- The planet collides with the asteroid with a mass of 19. New planet mass: 19 + 19 = 38
- The planet collides with the asteroid with a mass of 5. New planet mass: 38 + 5 = 43
- The planet collides with the asteroid with a mass of 3. New planet mass: 43 + 3 = 46
- The planet collides with the asteroid with a mass of 21. New planet mass: 46 + 21 = 67
All asteroids are destroyed.
```

**Example 2:**

```
Input: mass = 5, asteroids = [4,9,23,4]
Output: false
Explanation: 
The planet cannot ever gain enough mass to destroy the asteroid with a mass of 23.
After the planet destroys the other asteroids, it will have a mass of 5 + 4 + 9 + 4 = 22.
This is less than 23, so a collision would not destroy the last asteroid.
```

**Constraints**

- 1 <= mass <= 105
- 1 <= asteroids.length <= 105
- 1 <= asteroids[i] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个整数 `mass`，表示行星的初始质量。再给定一个整数数组 `asteroids`，其中 `asteroids[i]` 是第 `i` 颗小行星的质量。  
你可以让行星以任意顺序与这些小行星相撞。如果行星的质量 **大于等于** 小行星的质量，则该小行星被摧毁，行星的质量会增加该小行星的质量；否则行星会被摧毁。  
返回 `true` 表示可以摧毁所有小行星，否则返回 `false`。

**示例 1**  
```
Input: mass = 10, asteroids = [3,9,19,5,21]
Output: true
Explanation: 可以按顺序 [9,19,5,3,21] 碰撞小行星：
- 行星与质量为 9 的小行星相撞，新的行星质量为 10 + 9 = 19  
- 行星与质量为 19 的小行星相撞，新的行星质量为 19 + 19 = 38  
- 行星与质量为 5 的小行星相撞，新的行星质量为 38 + 5 = 43  
- 行星与质量为 3 的小行星相撞，新的行星质量为 43 + 3 = 46  
- 行星与质量为 21 的小行星相撞，新的行星质量为 46 + 21 = 67  
所有小行星均被摧毁，返回 true。
```

**示例 2**  
```
Input: mass = 5, asteroids = [4,9,23,4]
Output: false
Explanation: 行星永远无法获得足够的质量来摧毁质量为 23 的小行星。  
即使先摧毁其他小行星，行星的质量也只能达到 5 + 4 + 9 + 4 = 22，仍小于 23，最后一次碰撞会导致行星被摧毁。
```

**约束条件**  
- `1 <= mass <= 10^5`  
- `1 <= asteroids.length <= 10^5`  
- `1 <= asteroids[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有小行星的碰撞顺序都枚举一遍**，只要找到一种顺序让行星质量始终大于等于要碰撞的小行星，就返回 `True`，否则返回 `False`。  

- **使用的数据结构**：  
  - `list`（列表）保存小行星质量。  
  - `itertools.permutations` 可以把列表的所有排列（相当于把所有可能的“碰撞顺序”）一次一次生成。把它想象成“把所有可能的排队顺序全部写在纸上”，然后逐一检查哪一种可以让行星活下来。  

- **为什么正确**：  
  - 只要遍历了**所有**可能的顺序，就一定不会漏掉最优的那一种。因此只要有一种可行的排列，暴力搜索一定会找到。  

- **时间/空间复杂度**：  
  - 对长度为 `n` 的小行星数组，排列数是 `n!`（阶乘），也就是说时间复杂度是 `O(n!)`，这在实际运行时会非常慢。  
  - 额外空间只需要存放一次排列，`O(n)`。  

> **大白话**：  
> - `O(n!)` 就像把所有可能的钥匙都尝一遍才能打开门，钥匙越多，尝试的次数会指数级增长，根本不现实。  

#### 代码（Python）

```python
from itertools import permutations
from typing import List

def can_destroy_bruteforce(mass: int, asteroids: List[int]) -> bool:
    """
    暴力枚举所有碰撞顺序，判断是否存在一种可以全部摧毁小行星的顺序。
    """
    # 遍历所有排列（每一种可能的碰撞顺序）
    for order in permutations(asteroids):
        cur_mass = mass                 # 当前行星质量
        survived = True                 # 标记本次排列是否能成功
        for a in order:                 # 按当前排列依次碰撞
            if cur_mass >= a:           # 行星够重，摧毁小行星
                cur_mass += a
            else:                       # 行星被摧毁，直接终止本次排列
                survived = False
                break
        if survived:                    # 找到一种成功的排列，直接返回 True
            return True
    return False                        # 所有排列都失败，返回 False
```

#### 复杂度

- **时间复杂度**：`O(n!)`  
  - `n!` 是所有排列的数量，随着小行星个数的增多会呈指数级增长。  
- **空间复杂度**：`O(n)`  
  - 只保存当前排列和若干临时变量，额外空间与 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于选择“下一个要碰撞的小行星”**。如果我们每次都选**最小的**那颗还能被摧毁的小行星，行星的质量会尽可能快地增长，而不会因为一次“大碰撞”而提前失败。  

**为什么“最小的”是最好的选择？**  

1. **单调性**：如果当前行星质量 `mass` 小于某颗小行星 `a`，那么对所有质量更大的小行星 `b > a`，`mass < b` 仍然成立，行星必然会被摧毁。  
2. **贪心选择**：只要能摧毁当前最小的小行星，就把它的质量加到行星上，行星质量只会变大，后面的选择空间只会增大。  
3. **全局最优**：因为每一步我们都把行星质量提升到可能的最大（通过摧毁所有能摧毁的最小小行星），如果在某一步已经找不到可以摧毁的最小小行星，则说明**无论怎么排列，都不可能成功**。

**实现方式**：  
- 先把小行星数组按质量升序排列（相当于把“最小的”放在最前面）。这一步相当于先把所有小行星排好队。  
- 然后从左到右依次尝试碰撞：  
  - 若 `mass >= asteroid[i]`，行星成功摧毁该小行星，`mass += asteroid[i]`。  
  - 否则直接返回 `False`（因为后面的所有小行星质量更大，肯定也摧毁不了）。  

**类比**：把行星想象成一只吃掉糖果的怪兽，糖果的大小从小到大排好。怪兽只能吃掉比自己小或等于自己的糖果，吃完后会变得更大。只要从最小的糖果开始吃，怪兽的体型会一直增长，最坏的情况就是遇到一颗太大的糖果，说明无论怎么挑选，怪兽都吃不下。

#### 代码（Python）

```python
from typing import List

def can_destroy_greedy(mass: int, asteroids: List[int]) -> bool:
    """
    贪心解：先把小行星按质量升序排列，然后依次尝试摧毁。
    """
    # 1. 把小行星从小到大排好序（相当于排队）
    asteroids.sort()                     # O(n log n) 的排序

    # 2. 按顺序依次碰撞
    for a in asteroids:                  # O(n) 的遍历
        if mass >= a:                    # 能摧毁当前最小的小行星
            mass += a                    # 行星质量增长
        else:                            # 当前质量不足，后面的更大，必定失败
            return False
    return True                           # 所有小行星都被摧毁
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 主要来自排序，`n` 为小行星数量。排序后只需要一次线性遍历。相比暴力的 `O(n!)`，这已经是可接受的规模。  
- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（若语言内部实现返回新列表）。这里我们直接在原列表上排序，额外空间几乎可以忽略不计。

---

## 心得

- **核心技巧**：**贪心 + 排序** —— 每一步都选择当前能摧毁的最小小行星，保证行星质量的最快增长。  
- **适用的题型**：  
  1. “吃水果” 类题目（如 LeetCode 1746. Maximum Subarray Sum with One Deletion）  
  2. “资源收集” 类题目（如 LeetCode 1040. Moving Stones Until Consecutive）  
  3. 需要“从小到大逐步累加”才能通过的题目（如 LeetCode 2615. Sum of Distances）  
- **一句话总结解题钥匙**：**“把所有任务按难度从易到难排好序，逐个完成，遇到第一个无法完成的就直接失败”。**

---

## 反思

- **第一反应**：看到“任意顺序”就想到**枚举所有排列**，这是最直观但不可行的做法。  
- **最容易踩的坑**：  
  - 忽略了“如果最小的小行星都摧毁不了，后面的更大的一定也摧毁不了”。  
  - 没考虑到 **排序的时间复杂度**，直接使用 `sorted()`（返回新列表）会产生额外的 `O(n)` 空间。  
- **下次遇到同类题**：第一步就**思考是否存在单调性**（即“更大更难”），如果有，就**尝试把元素排序后用贪心**，而不是盲目枚举。