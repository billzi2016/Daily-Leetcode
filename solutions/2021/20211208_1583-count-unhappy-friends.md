# #1583. 统计不开心的朋友 / Count Unhappy Friends

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-unhappy-friends/)

---

## 题目（英文原版）

**Description**

You are given a list of preferences for n friends, where n is always even.
For each person i, preferences[i] contains a list of friends sorted in the order of preference. In other words, a friend earlier in the list is more preferred than a friend later in the list. Friends in each list are denoted by integers from 0 to n-1.
All the friends are divided into pairs. The pairings are given in a list pairs, where pairs[i] = [xi, yi] denotes xi is paired with yi and yi is paired with xi.
However, this pairing may cause some of the friends to be unhappy. A friend x is unhappy if x is paired with y and there exists a friend u who is paired with v but:
Return the number of unhappy friends.

**Examples**

**Example 1:**

```
Input: n = 4, preferences = [[1, 2, 3], [3, 2, 0], [3, 1, 0], [1, 2, 0]], pairs = [[0, 1], [2, 3]]
Output: 2
Explanation:
Friend 1 is unhappy because:
- 1 is paired with 0 but prefers 3 over 0, and
- 3 prefers 1 over 2.
Friend 3 is unhappy because:
- 3 is paired with 2 but prefers 1 over 2, and
- 1 prefers 3 over 0.
Friends 0 and 2 are happy.
```

**Example 2:**

```
Input: n = 2, preferences = [[1], [0]], pairs = [[1, 0]]
Output: 0
Explanation: Both friends 0 and 1 are happy.
```

**Example 3:**

```
Input: n = 4, preferences = [[1, 3, 2], [2, 3, 0], [1, 3, 0], [0, 2, 1]], pairs = [[1, 3], [0, 2]]
Output: 4
```

**Constraints**

- 2 <= n <= 500
- n is even.
- preferences.length == n
- preferences[i].length == n - 1
- 0 <= preferences[i][j] <= n - 1
- preferences[i] does not contain i.
- All values in preferences[i] are unique.
- pairs.length == n/2
- pairs[i].length == 2
- xi != yi
- 0 <= xi, yi <= n - 1
- Each person is contained in exactly one pair.

---

## 题目（中文翻译）

你得到一个包含 **n** 位朋友偏好（preferences）的列表，**n** 总是偶数。  
对于每个人 **i**，`preferences[i]` 是一个按照偏好顺序排列的朋友列表——列表中更靠前的朋友比后面的更受偏爱。列表中的朋友用 **0** 到 **n‑1** 的整数表示。

所有朋友被划分为若干对。配对信息在列表 `pairs` 中给出，其中 `pairs[i] = [x_i, y_i]` 表示 **x_i** 与 **y_i** 配对，**y_i** 也与 **x_i** 配对。

然而，这样的配对可能会让部分朋友感到不开心。若朋友 **x** 与 **y** 配对，而存在另一对 **u**, **v** 满足：

- **x** 更倾向于 **u**（即在 `preferences[x]` 中 **u** 出现在 **y** 前面），且  
- **u** 也更倾向于 **x**（即在 `preferences[u]` 中 **x** 出现在 **v** 前面），  

则 **x** 为不开心的朋友（unhappy friend）。

请返回不开心的朋友的数量。

---

### 示例

**示例 1**

```
Input: n = 4, preferences = [[1, 2, 3], [3, 2, 0], [3, 1, 0], [1, 2, 0]], pairs = [[0, 1], [2, 3]]
Output: 2
Explanation:
朋友 1 不开心，因为：
- 1 与 0 配对，但他更倾向于 3 而不是 0；
- 3 更倾向于 1 而不是 2。
朋友 3 也不开心，因为：
- 3 与 2 配对，但他更倾向于 1 而不是 2；
- 1 更倾向于 3 而不是 0。
朋友 0 和 2 都是开心的。
```

**示例 2**

```
Input: n = 2, preferences = [[1], [0]], pairs = [[1, 0]]
Output: 0
Explanation: 朋友 0 和 1 都是开心的。
```

**示例 3**

```
Input: n = 4, preferences = [[1, 3, 2], [2, 3, 0], [1, 3, 0], [0, 2, 1]], pairs = [[1, 3], [0, 2]]
Output: 4
```

---

### 约束条件

- `2 <= n <= 500`
- `n` 为偶数
- `preferences.length == n`
- `preferences[i].length == n - 1`
- `0 <= preferences[i][j] <= n - 1`
- `preferences[i]` 中不包含 `i`
- `preferences[i]` 中的所有值互不相同
- `pairs.length == n / 2`
- `pairs[i].length == 2`
- `x_i != y_i`
- `0 <= x_i, y_i <= n - 1`
- 每个人恰好出现在一对中

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出 `n`（偶数）位朋友的偏好列表 `preferences[i]`，以及已经形成的配对 `pairs`。  
我们要判断 **某个人 x 是否不开心**，根据定义：

- x 与 y 配对  
- 存在另一对 (u, v) 使得  
  - x 更喜欢 u 而不是自己的配偶 y  
  - u 也更喜欢 x 而不是自己的配偶 v  

如果满足上述条件，x 就是不开心的。

最直接的想法就是 **枚举**：  

1. 先把配对关系存到字典 `partner[x] = y`，这样可以 O(1) 直接得到任意人的配偶。  
2. 对每个朋友 `x`（共 n 人）  
   - 遍历 `preferences[x]`，找到所有 **比配偶 y 更喜欢的朋友** `u`（这些朋友排在 `y` 前面）。  
   - 对每个这样得到的 `u`，检查 `u` 是否也更喜欢 `x` 而不是 `u` 的配偶 `partner[u]`。  
   - 若有一次满足，就把 `x` 记为不开心，直接结束对 `x` 的搜索。  

这套流程里最关键的判断是“某人更喜欢谁”。因为偏好列表是**有序**的，我们可以直接遍历列表，遇到配偶 `y` 时停止；遍历到的所有元素就是“更喜欢的朋友”。  

> **类比**：  
> - `partner` 字典就像一本“配对簿”，告诉我们每个人的“另一半”。  
> - `preferences[i]` 像是 **个人的“爱好排行榜”**，越靠前越喜欢。  

只要把上述步骤实现出来，就能得到答案。  

**为什么正确**：  
- 我们对每个人都检查了**所有**可能导致不开心的情况（所有比当前配偶更喜欢的人），并且对每个候选人 `u` 都检查了 `u` 是否也更喜欢 `x`。只要出现一次符合条件，就符合题目定义的“不开心”。  

#### 代码（Python）

```python
def unhappyFriends(n, preferences, pairs):
    # 1. 建立配对映射，partner[x] = y 表示 x 的配偶是 y
    partner = {}
    for a, b in pairs:
        partner[a] = b
        partner[b] = a

    unhappy = set()                     # 用集合去重，防止同一个人被计入两次

    # 2. 对每个人 x 检查是否不开心
    for x in range(n):
        y = partner[x]                  # x 的配偶
        # 依次遍历 x 的偏好列表，直到遇到配偶 y 为止
        for u in preferences[x]:
            if u == y:                  # 已经到了配偶，后面的都不比配偶更喜欢
                break
            # u 是 x 更喜欢的朋友，检查 u 是否也更喜欢 x
            v = partner[u]              # u 的配偶
            # 在 u 的偏好列表里，x 是否排在 v 前面？
            # 只要遍历到 x 就说明 u 更喜欢 x
            for w in preferences[u]:
                if w == x:              # u 更喜欢 x
                    unhappy.add(x)      # x 不开心
                    break
                if w == v:              # 已经到了 u 的配偶，后面不再更喜欢
                    break
            if x in unhappy:            # 已经确认 x 不开心，直接结束对 x 的检查
                break

    return len(unhappy)
```

> **关键注释**  
> - `partner` 相当于**哈希表**（字典），像查字典一样 O(1) 找到配偶。  
> - 两层 `for` 循环分别遍历 **x 更喜欢的朋友** 与 **这些朋友是否更喜欢 x**。  

#### 复杂度

- **时间复杂度**：  
  对每个人 `x`，我们最坏要遍历整个偏好列表（长度 `n‑1`），在内部又可能遍历另一位 `u` 的完整偏好列表。  
  因此最坏情况是 `O(n * (n-1) * (n-1)) ≈ O(n³)`。  
  > **大白话**：如果有 100 个人，最坏要做 100×99×99 ≈ 1,000,000 次比较，算是“很慢”。  

- **空间复杂度**：  
  只用了 `partner`（大小 `n`）和一个 `set`（最多 `n`），所以是 `O(n)` 的额外空间。  

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在 **频繁遍历偏好列表**：每次判断 `u` 是否更喜欢 `x` 时，都要线性扫描 `preferences[u]`。  
我们可以把“谁更喜欢谁”的判断 **提前预处理**，把它降到 **O(1)**。

**核心技巧：**  
- 对每个人 `i`，建立一个 **排名表 `rank[i][j]`**，表示 `i` 在自己的偏好列表中把 `j` 排在第几位（数值越小越喜欢）。  
- 有了 `rank`，比较 “`i` 更喜欢 `a` 还是 `b`” 只需要比较两个整数：`rank[i][a] < rank[i][b]`。

构建 `rank` 的步骤：

```text
for i in 0 .. n-1:
    for position, friend in enumerate(preferences[i]):
        rank[i][friend] = position
```

这样 `rank` 的大小是 `n × n`（最多 500×500 = 250,000），在题目限制下完全可以接受。

有了 `rank`，判断不开心的过程可以直接遍历 **所有配对**，再遍历 **配对中每个人的所有可能更喜欢的对象**（不需要再去遍历对方的列表）：

1. 同样先把配对映射 `partner` 建好。  
2. 对每对 `(x, y)`：  
   - 对 `x`，遍历 `preferences[x]` 中 **排在 `y` 前面的所有朋友 `u`**（因为这些才是 `x` 更喜欢的）。  
   - 对每个 `u`，检查 `rank[u][x] < rank[u][partner[u]]`，即 `u` 是否也更喜欢 `x` 而不是自己的配偶。  
   - 若条件成立，则 `x` 不开心。  
   - 同理处理 `y`（因为配对是对称的），或者在遍历所有人时自然会覆盖。  

由于每对配对只检查一次，每个人只遍历一次自己的 **更喜欢的前缀**，整体时间降到 **`O(n²)`**。

> **类比**：  
> - `rank` 像是 **“朋友的名次表”**，把每个人的“爱好排行榜”压缩成一个可以快速查表的矩阵。  
> - 以后想知道 “我更喜欢 A 还是 B”，直接看两个人的分数（排名），不必再翻书（遍历列表）。  

#### 代码（Python）

```python
def unhappyFriends(n, preferences, pairs):
    # 1. partner[i] = i 的配偶
    partner = [0] * n
    for a, b in pairs:
        partner[a] = b
        partner[b] = a

    # 2. 构造 rank 矩阵，rank[i][j] = i 对 j 的偏好顺序（越小越喜欢）
    rank = [[0] * n for _ in range(n)]
    for i in range(n):
        for pos, friend in enumerate(preferences[i]):
            rank[i][friend] = pos

    unhappy = set()

    # 3. 对每个人 x 检查是否不开心
    for x in range(n):
        y = partner[x]                     # x 的配偶
        # 只遍历 x 更喜欢的朋友（出现在配偶 y 前面的所有人）
        for u in preferences[x]:
            if u == y:                     # 已经到了配偶，后面的都不再更喜欢
                break
            # u 是否也更喜欢 x 而不是自己的配偶？
            v = partner[u]                 # u 的配偶
            if rank[u][x] < rank[u][v]:   # u 对 x 的排名更靠前
                unhappy.add(x)            # x 不开心
                break                     # 找到一次即可结束对 x 的检查

    return len(unhappy)
```

> **关键注释**  
> - `rank[u][x] < rank[u][v]`：如果 `u` 对 `x` 的排名比对自己的配偶 `v` 更靠前，说明 `u` 更喜欢 `x`。  
> - 只遍历到配偶 `y` 为止，避免无意义的比较，进一步降低常数。  

#### 复杂度

- **时间复杂度**：  
  - 构建 `partner`：`O(n)`  
  - 构建 `rank`：遍历 `n` 个列表，每个长度 `n‑1`，共 `O(n²)`。  
  - 主循环：对每个人遍历其 **更喜欢配偶的前缀**，最坏情况仍是遍历 `O(n²)` 次（因为每条偏好最多被遍历一次）。  
  - 合计 `O(n²)`，在 `n ≤ 500` 时非常快。  
  > **大白话**：如果有 500 个人，只需要大约 500×500 = 250,000 次比较，几乎瞬间完成。

- **空间复杂度**：  
  - `partner` 长度 `n` → `O(n)`  
  - `rank` 矩阵 `n × n` → `O(n²)`（最多 250,000 个整数，完全可接受）  
  - 其它如 `unhappy` 集合最多 `O(n)`。  

---

## 心得

- **核心技巧**：利用 **排名矩阵 `rank`** 把“谁更喜欢谁”的比较从线性搜索降为常数时间。  
- **适用题型**  
  1. **配对/婚姻稳定性** 类题目（如《求稳定婚姻配对》）。  
  2. **基于偏好顺序的比较**（比如《找出互相喜欢的情侣》）。  
  3. 任何需要频繁比较两个元素在同一有序列表中的相对位置的场景。  
- **一句话总结**：先把“谁排在前面”预处理成表，后面的比较就像查字典一样快。

---

## 反思

- **第一反应**：直接把题目描述翻译成“遍历所有可能的组合”，于是写出了暴力的三层循环。  
- **最容易踩的坑**  
  - 忘记只遍历“比配偶更喜欢的朋友”，导致不必要的 `O(n³)`。  
  - 在判断 `u` 是否更喜欢 `x` 时，仍然使用线性扫描而不是 O(1) 比较。  
  - 边界：`preferences[i]` 长度是 `n‑1`，配偶一定在列表中，遍历时要记得在遇到配偶时 `break`，否则会把配偶后面的不相关朋友也算进来。  
- **下次思路**：  
  1. 先把**配对关系**和**偏好顺序**抽象成可以 O(1) 访问的结构（哈希表、矩阵）。  
  2. 再思考“瓶颈在哪”，是否有重复的线性搜索可以预处理。  
  3. 把每一步的 **“我在找什么”** 用图或表的形式写下来，帮助发现可以提前计算的子问题。