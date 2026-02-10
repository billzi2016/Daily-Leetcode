# #3522. 执行指令后计算得分 / Calculate Score After Performing Instructions

> 难度：中等 · 标签：Array、Hash Table、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/calculate-score-after-performing-instructions/)

---

## 题目（英文原版）

**Description**

You are given two arrays, instructions and values, both of size n.
You need to simulate a process based on the following rules:
The process ends when you either:
Return your score at the end of the process.

**Examples**

**Example 1:**

```
Input: instructions = ["jump","add","add","jump","add","jump"], values = [2,1,3,1,-2,-3]
Output: 1
Explanation:
Simulate the process starting at instruction 0:
```

**Example 2:**

```
Input: instructions = ["jump","add","add"], values = [3,1,1]
Output: 0
Explanation:
Simulate the process starting at instruction 0:
```

**Example 3:**

```
Input: instructions = ["jump"], values = [0]
Output: 0
Explanation:
Simulate the process starting at instruction 0:
```

**Constraints**

- n == instructions.length == values.length
- 1 <= n <= 105
- instructions[i] is either "add" or "jump".
- -105 <= values[i] <= 105

---

## 题目（中文翻译）

给定两个大小为 `n` 的数组，指令数组（`instructions`）和数值数组（`values`）。  
你需要按照以下规则模拟一个过程：  

- 从下标 `0` 开始执行指令。  
- 若当前指令为 `"add"`，则将对应的 `values[i]` 加到得分（score）上，然后将指针 `i` 向右移动一位（`i += 1`）。  
- 若当前指令为 `"jump"`，则将指针 `i` 按 `values[i]` 的大小进行跳转（`i += values[i]`），得分不变。  
- 当指针 `i` 超出数组范围（`i < 0` 或 `i >= n`）时，过程结束。  

返回过程结束时的得分。

**示例 1**  
输入: `instructions = ["jump","add","add","jump","add","jump"]`, `values = [2,1,3,1,-2,-3]`  
输出: `1`  
**解释:**  
从指令 `0` 开始模拟过程：

**示例 2**  
输入: `instructions = ["jump","add","add"]`, `values = [3,1,1]`  
输出: `0`  
**解释:**  
从指令 `0` 开始模拟过程：

**示例 3**  
输入: `instructions = ["jump"]`, `values = [0]`  
输出: `0`  
**解释:**  
从指令 `0` 开始模拟过程：

**约束条件**  
- `n == instructions.length == values.length`  
- `1 <= n <= 10^5`  
- `instructions[i]` 仅为 `"add"` 或 `"jump"`  
- `-10^5 <= values[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目让我们 **模拟** 一段指令序列的执行过程。  
- 有两个数组 `instructions`（只会是 `"add"` 或 `"jump"`）和 `values`（对应的整数），长度相同记为 `n`。  
- 从下标 `0` 开始执行：  
  - 若指令是 `"add"`，把 `values[i]` 加到 **得分** 上，然后走到下一条指令 `i+1`。  
  - 若指令是 `"jump"`，直接把指针移动到 `i + values[i]`（**不改变得分**）。  
- 当指针 **跑出数组**（`i < 0` 或 `i >= n`）或者 **再次来到已经执行过的下标** 时，整个过程结束，返回当前得分。  

最直接的想法就是：**一步一步走**，每走一步都检查当前下标是否已经访问过。  
- 为了判断“是否已经访问”，我们可以把已经走过的下标存进一个普通的 Python `list`，每次判断时遍历整个列表看有没有相同的下标。  
- 这就像我们在生活中查字典：字典的 “key” 是单词， “value” 是页码。这里的 “list” 就是一本**没有索引**的字典，我们只能顺着翻页找。

这种做法一定能得到正确答案，因为我们严格按照题目规则一步一步模拟，直到满足结束条件。  

#### 代码（Python）

```python
def calculateScore(instructions, values):
    n = len(instructions)
    i = 0                     # 当前指针
    score = 0                 # 最终得分
    visited = []              # 已经执行过的下标，类似“无索引的字典”

    while 0 <= i < n:
        # 线性扫描 visited，判断是否已经到过 i
        if i in visited:      # O(len(visited))，最坏会是 O(n)
            break             # 再次来到同一条指令，结束

        visited.append(i)     # 记录这条指令已经执行过

        if instructions[i] == "add":
            score += values[i]    # 加分
            i += 1                # 移动到下一条指令
        else:                     # "jump"
            i += values[i]        # 直接跳转，不加分

    return score
```

> 关键行的中文注释已经写在代码里，直接复制粘贴即可运行。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每一步都要在 `visited` 中线性查找 (`i in visited`)。最坏情况下会遍历 `0 … n‑1`，所以总时间是 `1 + 2 + … + n = O(n²)`。  
  - 用大白话说，就是“每走一步都要把已经走过的所有路程重新翻一遍”，所以会变慢。  

- **空间复杂度**：`O(n)`  
  - 需要保存最多 `n` 个已经访问过的下标。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出 **瓶颈** 在于判断“是否已经访问”时的线性扫描。  
如果我们能把 **查询** 的时间从 `O(n)` 降到 `O(1)`，整体就会从 `O(n²)` 降到 `O(n)`。

在 Python 中，有两种常用的 “常数时间查询” 结构：

1. **集合（`set`）**  
   - 把已经访问过的下标放进集合，查询 `i in visited_set` 的时间复杂度是 `O(1)`（哈希表的查找）。  
   - 哈希表可以类比为 **查字典**：我们直接看单词对应的页码，不需要从头翻到尾。  

2. **布尔数组**（长度为 `n` 的 `list`）  
   - 用 `visited[i] = True` 标记，下标 `i` 是否已经访问。查询同样是 `O(1)`。  
   - 这相当于在每一页上贴上“已读”贴纸，直接看贴纸就知道。  

这里我们选用 **布尔数组**，因为下标范围已经知道是 `0 … n‑1`，空间正好是 `n`，实现最简洁。

整体思路：

1. 初始化指针 `i = 0`、得分 `score = 0`、布尔数组 `visited = [False] * n`。  
2. 只要指针在合法范围且对应位置未被访问过，就继续执行：  
   - 把 `visited[i]` 设为 `True`（标记为已访问）。  
   - 根据指令类型更新 `score` 与 `i`：  
     - `"add"` → `score += values[i]; i += 1`  
     - `"jump"` → `i += values[i]`（不改分）  
3. 循环结束后返回 `score`。  

这样每一步的操作都是 **常数时间**，整个过程最多走 `n` 步（因为一旦访问了 `n` 条指令就一定会结束），所以总时间是 `O(n)`。

#### 代码（Python）

```python
def calculateScore(instructions, values):
    n = len(instructions)
    i = 0                 # 当前指针，从第 0 条指令开始
    score = 0
    visited = [False] * n   # 布尔数组，类似“已读”贴纸

    while 0 <= i < n and not visited[i]:
        visited[i] = True    # 标记第 i 条指令已经执行过

        if instructions[i] == "add":
            score += values[i]   # 累加得分
            i += 1               # 移动到下一条指令
        else:                     # "jump"
            i += values[i]       # 按值跳转，不加分

    return score
```

> 每一行都配有中文注释，帮助你快速对照实现细节。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每条指令最多被访问一次，且每次操作都是常数时间。相比暴力解的 `O(n²)`，快了很多。  

- **空间复杂度**：`O(n)`  
  - 需要额外的布尔数组来记录是否访问过，同样是线性空间。  
  - 若使用 `set` 也会是 `O(n)`，只不过常数因子略大一些。  

---

## 心得  

- **核心技巧**：使用 **哈希表 / 布尔数组** 实现“已访问”快速查询，避免在模拟过程中出现重复遍历。  
- **适用的题型**：  
  1. “循环检测” 类题目（如环形链表、数组跳跃游戏中的环检测）。  
  2. “路径遍历” 需要防止无限循环的模拟题（如“机器人在网格中移动”）。  
  3. “状态记录” 类的 DP/搜索题目（如“跳棋游戏”中记录已经到达的格子）。  
- **一句话总结**：**“先把已经做过的事记下来，用 O(1) 查找防止走回头路”。**

---

## 反思  

- **第一反应**：直接把题目描述翻译成一步一步的循环，手动维护指针和分数。  
- **最容易踩的坑**：  
  - **越界**：`jump` 可能让指针直接跑出数组，需要在循环条件里检查 `0 ≤ i < n`。  
  - **自循环**：`jump` 的值为 `0` 时会一直停在同一条指令，需要及时检测“已访问”。  
  - **负数跳转**：`values[i]` 可能是负数，导致指针向左移动，同样要做好越界判断。  
- **下次遇到同类题**，第一步应该想到：**“是否会出现重复访问？”** → 用集合或布尔数组记录访问状态，保证模拟过程在 O(n) 内结束。