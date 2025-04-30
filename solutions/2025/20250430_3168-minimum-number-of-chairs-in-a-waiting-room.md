# #3168. 等待室所需的最少座位数 / Minimum Number of Chairs in a Waiting Room

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-chairs-in-a-waiting-room/)

---

## 题目（英文原版）

**Description**

You are given a string s. Simulate events at each second i:
Return the minimum number of chairs needed so that a chair is available for every person who enters the waiting room given that it is initially empty.

**Examples**

**Example 1:**

```
Input: s = "EEEEEEE"
Output: 7
Explanation:
After each second, a person enters the waiting room and no person leaves it. Therefore, a minimum of 7 chairs is needed.
```

**Example 2:**

```
Input: s = "ELELEEL"
Output: 2
Explanation:
Let's consider that there are 2 chairs in the waiting room. The table below shows the state of the waiting room at each second.
```

**Example 3:**

```
Input: s = "ELEELEELLL"
Output: 3
Explanation:
Let's consider that there are 3 chairs in the waiting room. The table below shows the state of the waiting room at each second.
```

**Constraints**

- 1 <= s.length <= 50
- s consists only of the letters 'E' and 'L'.
- s represents a valid sequence of entries and exits.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅由字符 `'E'`（Enter，进入）和 `'L'`（Leave，离开）组成的字符串 `s`，模拟每秒 `i`（从第 0 秒开始）发生的事件：

- 若 `s[i]` 为 `'E'`，则有一名新顾客进入等待室（waiting room）。
- 若 `s[i]` 为 `'L'`，则有一名已经在等待室中的顾客离开。

假设一开始等待室为空，求 **最少的座位（chair）数**，使得在整个过程的每一秒钟，进入的每位顾客都能立即坐到一把空座位上。

---

**示例**

**示例 1**  
```
输入: s = "EEEEEEE"
输出: 7
解释:
每一秒都有新顾客进入，且没有人离开。因此需要至少 7 把座位（chair）。
```

**示例 2**  
```
输入: s = "ELELEEL"
输出: 2
解释:
假设等待室里有 2 把座位（chair）。下表展示了每秒的状态（E 表示进入，L 表示离开）：

| 秒数 | 事件 | 在座位上的人数 |
|------|------|----------------|
| 0    | E    | 1              |
| 1    | L    | 0              |
| 2    | E    | 1              |
| 3    | L    | 0              |
| 4    | E    | 1              |
| 5    | E    | 2              |
| 6    | L    | 1              |

整个过程最多同时有 2 人在等待室内，因此 2 把座位（chair）足够。
```

**示例 3**  
```
输入: s = "ELEELEELLL"
输出: 3
解释:
假设等待室里有 3 把座位（chair）。下表展示了每秒的状态：

| 秒数 | 事件 | 在座位上的人数 |
|------|------|----------------|
| 0    | E    | 1 |
| 1    | L    | 0 |
| 2    | E    | 1 |
| 3    | E    | 2 |
| 4    | L    | 1 |
| 5    | E    | 2 |
| 6    | E    | 3 |
| 7    | L    | 2 |
| 8    | L    | 1 |
| 9    | L    | 0 |

最多同时有 3 人在等待室内，所以需要 3 把座位（chair）。
```

---

**约束条件**

- `1 <= s.length <= 50`
- `s` 只包含字符 `'E'` 和 `'L'`.
- `s` 表示一个合法的进入/离开序列（即在任意时刻离开的顾客数不超过已进入的顾客数）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每一秒**我们都重新算一次现在房间里有多少人。  
具体做法：

1. 从左到右遍历字符串 `s`，第 `i` 位表示第 `i` 秒发生的事件。  
2. 对于第 `i` 秒，**再次**遍历 `s[0..i]`，把所有 `'E'`（Enter，进入）计为 +1，所有 `'L'`（Leave，离开）计为 -1，得到此时房间里的人数。  
3. 把每秒得到的人数保存下来，最后取最大值，就是需要的最少椅子数。

> **类比**：想象你在图书馆查找一本书，每次都要把目录从头到尾翻一遍，看看这本书在第几页出现。这里我们每秒都“重新翻目录”，所以会很慢。

**为什么正确**  
因为题目要求的是“任意时刻房间里最多有多少人”。只要我们能够得到每一秒的实际人数，取最大值自然就是答案。即使我们每秒都重新计数，只要计数方式不出错，答案一定正确。

#### 代码（Python）

```python
def minChairs_bruteforce(s: str) -> int:
    # 用来记录所有秒的在座人数
    people_counts = []

    # i 表示第 i 秒（下标从 0 开始）
    for i in range(len(s)):
        cur = 0  # 当前秒的在座人数
        # 再次遍历从第 0 秒到第 i 秒的所有事件
        for j in range(i + 1):
            if s[j] == 'E':      # 有人进入
                cur += 1
            else:                # 'L'，有人离开
                cur -= 1
        people_counts.append(cur)   # 记录第 i 秒的人数

    # 房间里最高峰的人数，就是最少需要的椅子数
    return max(people_counts)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n` 是字符串长度。因为外层遍历 `n` 次，内层每次最多再遍历 `n` 次（实际是 `1 + 2 + … + n = n·(n+1)/2`），所以总体是二次方的工作量。  
  用大白话说，就是如果有 10 秒，需要检查 1+2+…+10=55 次；如果有 50 秒，需要检查 1275 次，随 `n` 增大，检查次数会“蹭蹭”增长。

- **空间复杂度**：`O(n)`  
  只用了一个列表 `people_counts` 保存每秒的人数，长度等于 `n`。其余变量都是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每秒都重新遍历之前的所有字符**，导致二次方时间。  
其实我们不需要每次重新计数，只要在遍历一次字符串的过程中，实时维护当前房间里的人数即可。

核心思路：

1. 用一个变量 `cur` 表示“当前房间里的人数”。  
2. 从左到右扫描字符串：  
   - 遇到 `'E'`，`cur += 1`（有人进来）。  
   - 遇到 `'L'`，`cur -= 1`（有人离开）。  
3. 同时维护另一个变量 `ans`，它始终保存遍历过程中出现的 **最大** `cur`。  
4. 扫描结束后，`ans` 就是房间里人数的最高峰，也是最少需要的椅子数。

> **类比**：想象你在看一条河的水位变化，河流的水位随时间上下波动。你只需要带一个水位计，每秒读一次当前水位，并记下最高的那一次。这样只需要一次走遍河岸，而不必每秒都回头再测一次。

**为什么正确**  
因为 `cur` 精确地表示了 **从起点到当前秒** 所有进入与离开的净效果，即此刻房间里真实的人数。遍历时记录的最大 `cur` 就是所有时刻的最大人数，恰好对应题目要求的最少椅子数。

#### 代码（Python）

```python
def minChairs(s: str) -> int:
    cur = 0   # 当前房间里的人数
    ans = 0   # 迄今为止的最高人数（即需要的最少椅子数）

    for ch in s:               # 逐字符遍历
        if ch == 'E':          # 有人进入
            cur += 1
        else:                  # 'L'，有人离开
            cur -= 1

        # 更新最高人数
        if cur > ans:
            ans = cur

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，每个字符做 O(1) 的加减和比较。用大白话说，字符多少，就需要多少次“看一眼”，不会出现重复检查，效率线性增长。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量，和字符串长度无关，常数级别的额外空间。

---

## 心得

- **核心技巧**：一次遍历（**前缀和**） + 维护**最大前缀和**。  
- 该技巧常用于**统计过程中的峰值**，例如  
  1. “汽车停车场需要的最少车位数” (`'I'` 入场、`'O'` 出场)  
  2. “股票买卖中的最大持仓量”  
  3. “括号序列的最大深度” (`'('` 增、`')'` 减)  
- **解题钥匙**：**只要能把每一步的“当前状态”算出来，并实时记录最大值，就不必回头重算**。

## 反思

- **第一反应**：看到只有 `'E'`、`'L'` 两种字符，立刻想到“进出计数”。  
- **最容易踩的坑**  
  - 忘记初始化 `ans` 为 0（如果全是 `'L'`，但题目保证序列合法，仍需防止负数）。  
  - 把 `'L'` 当成 +1，导致计数方向错误。  
  - 忽视“合法序列”意味着在任何前缀中 `'L'` 的数量不会超过 `'E'` 的数量，保证 `cur` 永不为负。  
- **下次思路**：看到“每秒都有增或减的事件，需要最高峰”，第一步就想到**维护当前值并取最大**，即“一遍遍历 + 前缀和”。