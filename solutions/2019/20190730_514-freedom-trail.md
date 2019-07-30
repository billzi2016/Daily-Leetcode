# #514. 自由之路 / Freedom Trail

> 难度：困难 · 标签：String、Dynamic Programming、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/freedom-trail/)

---

## 题目（英文原版）

**Description**

In the video game Fallout 4, the quest "Road to Freedom" requires players to reach a metal dial called the "Freedom Trail Ring" and use the dial to spell a specific keyword to open the door.
Given a string ring that represents the code engraved on the outer ring and another string key that represents the keyword that needs to be spelled, return the minimum number of steps to spell all the characters in the keyword.
Initially, the first character of the ring is aligned at the "12:00" direction. You should spell all the characters in key one by one by rotating ring clockwise or anticlockwise to make each character of the string key aligned at the "12:00" direction and then by pressing the center button.
At the stage of rotating the ring to spell the key character key[i]:

**Examples**

**Example 1:**

```
Input: ring = "godding", key = "gd"
Output: 4
Explanation:
For the first key character 'g', since it is already in place, we just need 1 step to spell this character. 
For the second key character 'd', we need to rotate the ring "godding" anticlockwise by two steps to make it become "ddinggo".
Also, we need 1 more step for spelling.
So the final output is 4.
```

**Example 2:**

```
Input: ring = "godding", key = "godding"
Output: 13
```

**Constraints**

- 1 <= ring.length, key.length <= 100
- ring and key consist of only lower case English letters.
- It is guaranteed that key could always be spelled by rotating ring.

---

## 题目（中文翻译）

**描述**  
在电子游戏《辐射4》中，任务 “Road to Freedom” 要求玩家转动一个名为 “Freedom Trail Ring” 的金属转盘，并通过转盘拼写出特定的关键字以打开门。  
给定一个字符串 `ring`（环），表示刻在外环上的代码；再给定一个字符串 `key`（钥匙），表示需要拼写的关键字，返回拼写完整关键字所需的最少步数。

最初，环的第一个字符位于 **12:00** 方向。你需要依次拼写 `key` 中的每个字符，方法是顺时针或逆时针旋转环，使得当前要拼写的字符对齐到 **12:00** 方向，然后按下中心按钮。每次旋转一步算作一步，按下按钮也算作一步。

在旋转环以拼写字符 `key[i]` 的过程中：

* 任选顺时针或逆时针方向，使得目标字符尽可能少步数到达 **12:00** 方向；
* 完成对齐后，按一次中心按钮。

---

### 示例

**示例 1**  
```
Input: ring = "godding", key = "gd"
Output: 4
Explanation:
对于第一个关键字字符 'g'，由于它已经在 **12:00** 位置，只需要 1 步（按下按钮）即可拼写该字符。  
对于第二个关键字字符 'd'，需要逆时针旋转环两步，使其变为 "ddinggo"。随后再按一次按钮。  
因此总步数为 4 步。
```

**示例 2**  
```
Input: ring = "godding", key = "godding"
Output: 13
```

---

### 约束条件
- $1 \leq \text{ring.length}, \text{key.length} \leq 100$
- `ring` 和 `key` 仅由小写英文字母组成。
- 保证可以通过旋转环拼写出 `key`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个转盘的每一次旋转都“枚举”出来，然后逐个检查能否得到目标关键字 `key`。  
可以把问题想成：

> 有一个圆形的字母环 `ring`，我们每一步可以把环顺时针或逆时针转任意格数（每格算一步），把想要的字母转到 12 点位置后按一次按钮（也算一步）。  
> 现在要一次写完 `key`，求最少的步数。

暴力解法的实现方式有两种：

1. **递归+全遍历**  
   对每个 `key[i]`，遍历环上所有出现该字符的位置 `pos`，计算从当前指针 `cur` 到 `pos` 的最短旋转步数（顺时针或逆时针），把这一步加上“按键”这一步，再递归求剩余字符的最小步数。  
   这相当于把每一步的所有可能都列举出来。

2. **宽度优先搜索（BFS）**  
   把状态定义为 `(i, cur)`——已经写完 `key` 前 `i` 个字符，且环指针现在指向 `cur`（即 `ring[cur]` 在 12 点）。  
   从初始状态 `(0, 0)` 开始，每次把所有可以转到的下一个字符的位置加入队列，层层展开，第一次碰到 `i == len(key)` 时的层数即为答案。

下面用递归的方式实现，因为它的代码更直观，虽然效率很低。

- **数据结构**：  
  - `ring` 和 `key` 都是普通的 Python `str`，我们只需要遍历字符。  
  - 为了快速找出某个字符在环中出现的所有位置，我们可以在递归里直接用 `for idx, ch in enumerate(ring)`，这相当于“查字典”，`idx` 就是“页码”，`ch` 是“单词”。  

- **为什么正确**：  
  递归会尝试 **所有** 可能的转动方式，最终必然会遍历到最优路径。因为我们对每一步都取最小值（`min`），所以返回的就是全局最小步数。

- **复杂度分析（大白话）**  
  - 假设环长为 `n`，关键字长为 `m`。  
  - 对每个关键字字符，我们都要遍历环上全部 `n` 个位置（最坏情况每个字符都出现 `n` 次），递归深度是 `m`。  
  - 所以总的计算量大约是 `O(n^m)`，这就像在每一步都有 `n` 条路要选，走 `m` 步，组合数会爆炸。  
  - 空间上只用了递归栈，深度为 `m`，即 `O(m)`。

#### 代码（Python）

```python
def findRotateSteps(ring: str, cur: int, target: str) -> int:
    """
    计算从当前指针 cur（环上某个位置）转到下一个字符 target
    所需的最少旋转步数（不包括按键那一步）
    """
    n = len(ring)
    # 顺时针距离
    clockwise = (target - cur) % n
    # 逆时针距离
    anticlockwise = (cur - target) % n
    return min(clockwise, anticlockwise)


def dfs(ring: str, key: str, i: int, cur: int, memo: dict) -> int:
    """
    递归求解：已经写完 key[0..i-1]，当前指针在 cur，返回写完剩余字符的最小步数
    使用 memo 记忆化搜索避免重复计算
    """
    if i == len(key):                 # 所有字符都写完了
        return 0
    if (i, cur) in memo:              # 已经算过了，直接返回
        return memo[(i, cur)]

    min_steps = float('inf')
    # 环上所有可能的目标字符位置
    for nxt, ch in enumerate(ring):
        if ch == key[i]:
            # 先转到 nxt，再按键（+1），再递归处理后面的字符
            steps = findRotateSteps(ring, cur, nxt) + 1 + dfs(ring, key, i + 1, nxt, memo)
            min_steps = min(min_steps, steps)

    memo[(i, cur)] = min_steps
    return min_steps


def findRotateSteps_bruteforce(ring: str, key: str) -> int:
    """
    暴力递归实现，返回最少步数
    """
    memo = {}
    return dfs(ring, key, 0, 0, memo)
```

#### 复杂度

- **时间复杂度**：`O(n^m)`（极端情况下会指数爆炸），这里的 `n = len(ring)`，`m = len(key)`。  
  用大白话说，就是“每写一个字母，你可能要尝试环上所有位置”，而关键字有 `m` 位，就像在树上每层都有 `n` 个分支，深度是 `m`，总节点数会非常大。

- **空间复杂度**：`O(m)`（递归栈深度）+ 记忆化表的大小 `O(m·n)`（最坏情况每个 `(i,cur)` 都会被存），整体是 `O(m·n)`。  

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于：  

1. **重复计算**——同一个 `(i, cur)` 状态会被递归很多次。  
2. **枚举所有环上位置**——每一步都遍历 `n` 次，导致指数级复杂度。

要优化，核心在于 **动态规划 + 预处理**：

1. **预处理字符位置**  
   把每个字母在环中出现的所有下标保存下来。比如 `pos['g'] = [0, 6]`（因为 `ring="godding"`）。  
   这相当于把“查字典”变成一次性把所有“页码”记下来，后面查询时只需要遍历对应的列表，而不是遍历整个环。

2. **状态定义**  
   设 `dp[i][j]` 为：写完 `key` 的前 `i` 个字符后，指针停在环的下标 `j`（`ring[j]` 对应 `key[i-1]`）时的最小步数。  
   - `i` 范围是 `1..m`（`m = len(key)`）。  
   - `j` 只取 **当前字符在环中出现的位置**，而不是全部 `0..n-1`，这样可以大幅削减状态数。

3. **状态转移**  
   要得到 `dp[i][cur]`（`cur` 是第 `i` 个字符 `key[i-1]` 在环中的一个出现位置），我们需要枚举前一步可能停留的所有位置 `prev`（对应 `key[i-2]` 的出现位置），并加上从 `prev` 转到 `cur` 的最短旋转步数：

   \[
   dp[i][cur] = \min_{prev} \bigl( dp[i-1][prev] + \text{dist}(prev, cur) + 1 \bigr)
   \]

   其中 `dist(prev, cur) = min(|prev - cur|, n - |prev - cur|)` 是顺时针或逆时针的最短距离，`+1` 是按键的那一步。

4. **初始状态**  
   写第一个字符 `key[0]` 时，指针起点在 `0`（环的第一个字符）。所以：

   \[
   dp[1][pos] = \text{dist}(0, pos) + 1
   \]

   对所有 `pos` 属于 `pos[key[0]]` 计算即可。

5. **答案**  
   最后一个字符写完后，指针可以停在任意对应位置，取最小值：

   \[
   answer = \min_{pos \in pos[key[m-1]]} dp[m][pos]
   \]

6. **复杂度分析**  
   - 每个字符的出现次数记作 `k`（最坏情况是 `n`），总的状态转移次数大约是 `∑_{i=2}^{m} (cnt(key[i-2]) * cnt(key[i-1]))`，在最坏情况下是 `O(m·n²)`，但实际因为字母种类只有 26，平均每个字母出现次数约为 `n/26`，所以实际运行很快（LeetCode 官方给出的时间限制足够）。  
   - 空间只需要保存上一轮的 DP（两层），即 `O(n)`。

下面给出完整实现，并在关键行加入中文注释。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def findRotateSteps_opt(ring: str, key: str) -> int:
    n = len(ring)               # 环的长度
    m = len(key)                # 关键字长度

    # 1️⃣ 预处理：记录每个字符在 ring 中出现的所有下标
    # pos['a'] = [2, 5, 9]  这就像把字典的“页码”一次性写好，后面查找更快
    pos: defaultdict[str, List[int]] = defaultdict(list)
    for idx, ch in enumerate(ring):
        pos[ch].append(idx)

    # 2️⃣ DP 数组：只保存上一层和当前层，降低空间
    # prev_dp[j] 表示写完 key 的前 i-1 个字符后，指针在下标 j 时的最小步数
    prev_dp = {0: 0}            # 初始时指针在 0，已经写了 0 个字符，步数 0

    # 逐个处理 key 中的字符
    for i, ch in enumerate(key):
        cur_dp = {}             # 当前字符写完后的新状态
        # 对于每个可能的目标位置 cur（该字符在 ring 中的出现位置）
        for cur in pos[ch]:
            # 在所有可能的前一个位置 prev 中挑最小的转动成本
            best = float('inf')
            for prev in prev_dp:
                # 环上两点的最短距离
                diff = abs(cur - prev)
                step = min(diff, n - diff)   # 顺时针或逆时针取最小
                # prev_dp[prev] 是前面已经花的步数，+ step 为旋转，+1 为按键
                best = min(best, prev_dp[prev] + step + 1)
            cur_dp[cur] = best   # 记录写到第 i+1 个字符后，指针停在 cur 的最小步数
        prev_dp = cur_dp          # 进入下一轮

    # 3️⃣ 最终答案：写完所有字符后，指针可以停在任意合法位置，取最小值
    return min(prev_dp.values())
```

#### 复杂度

- **时间复杂度**：`O(m * n * avg_occurrence)`  
  - `m = len(key)`，`n = len(ring)`。  
  - `avg_occurrence` 是每个字符在环中出现的平均次数，最坏情况下是 `n`（所有字符相同），此时复杂度退化为 `O(m·n²)`。  
  - 但因为字母只有 26 种，实际 `avg_occurrence ≈ n/26`，在题目限制（`n ≤ 100`）下运行毫秒级。

- **空间复杂度**：`O(n)`  
  - 只保存两层 DP（前一轮和当前轮）以及字符位置表 `pos`（最多 `n` 个下标），因此空间与环的长度线性相关。

---

## 心得

- **核心技巧**：  
  把“环上旋转的最短距离”抽象为 `min(|i-j|, n-|i-j|)`，并使用 **动态规划** 在每一步只保留**可能的指针位置**（即当前字符出现的下标），从而避免指数级搜索。

- **适用的题型**  
  1. **环形/循环结构的最短路径**（如 LeetCode 514 "Freedom Trail"、LeetCode 847 "Shortest Path Visiting All Nodes" 中的环形状态压缩）。  
  2. **需要在两个序列之间匹配并考虑位移成本**（如 LeetCode 1155 "Number of Dice Rolls With Target Sum" 中的状态转移）。  
  3. **字符匹配+移动代价**（如 LeetCode 1190 "Reverse Substrings Again?" 中的最小翻转次数）。

- **一句话总结解题钥匙**：  
  **“把每一步的所有合法位置都列出来，用 DP 记录最小累计代价，再用环的最短距离公式快速算转动步数”。**

---

## 反思

- **第一反应**：看到“转盘”“顺时针/逆时针”“最少步数”，自然想到**枚举所有旋转方式**（即暴力搜索），但很快会发现状态爆炸。

- **最容易踩的坑**  
  1. **环的距离计算错误**：一定要取 `min(diff, n - diff)`，否则会把顺时针和逆时针的距离算成同一个方向，导致答案偏大。  
  2. **忘记把按键这一步计入**：每写完一个字符，除了转动的步数，还要加 `1` 步的“按下按钮”。  
  3. **字符出现多次的处理**：同一个字符在环中可能出现多次，必须把所有位置都考虑进 DP，否则会错过更优的路径。  
  4. **边界条件**：`key` 长度为 `1` 时，只需要一次转动和一次按键；`ring` 长度为 `1` 时，转动步数永远是 `0`，只加按键步数。

- **下次遇到类似题的第一步**：  
  **先把“状态”明确下来**——这里是“已经写完多少字符 + 当前指针所在位置”。然后检查是否可以用**记忆化/动态规划**把状态数压缩到可接受的范围（例如只保留出现字符的下标），再再考虑**转动距离的快速计算公式**。这样就能快速从暴力搜索跳到最优 DP。