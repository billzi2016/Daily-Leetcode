# #1320. 使用双指敲击单词的最小距离 / Minimum Distance to Type a Word Using Two Fingers

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-distance-to-type-a-word-using-two-fingers/)

---

## 题目（英文原版）

**Description**

You have a keyboard layout as shown above in the X-Y plane, where each English uppercase letter is located at some coordinate.
Given the string word, return the minimum total distance to type such string using only two fingers.
The distance between coordinates (x1, y1) and (x2, y2) is |x1 - x2| + |y1 - y2|.
Note that the initial positions of your two fingers are considered free so do not count towards your total distance, also your two fingers do not have to start at the first letter or the first two letters.

**Examples**

**Example 1:**

```
Input: word = "CAKE"
Output: 3
Explanation: Using two fingers, one optimal way to type "CAKE" is: 
Finger 1 on letter 'C' -> cost = 0 
Finger 1 on letter 'A' -> cost = Distance from letter 'C' to letter 'A' = 2 
Finger 2 on letter 'K' -> cost = 0 
Finger 2 on letter 'E' -> cost = Distance from letter 'K' to letter 'E' = 1 
Total distance = 3
```

**Example 2:**

```
Input: word = "HAPPY"
Output: 6
Explanation: Using two fingers, one optimal way to type "HAPPY" is:
Finger 1 on letter 'H' -> cost = 0
Finger 1 on letter 'A' -> cost = Distance from letter 'H' to letter 'A' = 2
Finger 2 on letter 'P' -> cost = 0
Finger 2 on letter 'P' -> cost = Distance from letter 'P' to letter 'P' = 0
Finger 1 on letter 'Y' -> cost = Distance from letter 'A' to letter 'Y' = 4
Total distance = 6
```

**Constraints**

- 2 <= word.length <= 300
- word consists of uppercase English letters.

---

## 题目（中文翻译）

**描述**  
你在 X‑Y 平面上拥有如上图所示的键盘布局，每个大写英文字母都位于某个坐标。  
给定字符串 `word`，返回使用仅两根手指敲击该字符串的 **最小总距离**（minimum total distance）。  
两个坐标 `(x1, y1)` 与 `(x2, y2)` 之间的距离定义为 `|x1 - x2| + |y1 - y2|`。  
注意，两根手指的初始位置视为免费（不计入总距离），并且手指不一定要从第一个字母或前两个字母开始。

**示例 1**  
**示例 2**  

**约束条件**  

- `2 <= word.length <= 300`  
- `word` 只包含大写英文字母  

**示例**  

**示例 1**  
```
Input: word = "CAKE"
Output: 3
```
**解释**：使用两根手指，敲击 `"CAKE"` 的一种最优方式如下  
- 手指 1 按下字母 `'C'` → 花费 = 0  
- 手指 1 按下字母 `'A'` → 花费 = `'C'` 到 `'A'` 的距离 = 2  
- 手指 2 按下字母 `'K'` → 花费 = 0  
- 手指 2 按下字母 `'E'` → 花费 = `'K'` 到 `'E'` 的距离 = 1  
- **总距离 = 3**

**示例 2**  
```
Input: word = "HAPPY"
Output: 6
```
**解释**：使用两根手指，敲击 `"HAPPY"` 的一种最优方式如下  
- 手指 1 按下字母 `'H'` → 花费 = 0  
- 手指 1 按下字母 `'A'` → 花费 = `'H'` 到 `'A'` 的距离 = 2  
- 手指 2 按下字母 `'P'` → 花费 = 0  
- 手指 2 按下字母 `'P'` → 花费 = `'P'` 到 `'P'` 的距离 = 0  
- 手指 1 按下字母 `'Y'` → 花费 = `'A'` 到 `'Y'` 的距离 = 4  
- **总距离 = 6**   (后续示例已截断)

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**每一次敲字都决定用哪根手指**。  
假设我们从左到右依次处理 `word`，第 `i` 个字符可以交给**左指**或**右指**，于是会产生两条分支。  
把所有分支全部展开，就得到所有可能的指法序列，遍历它们并计算总距离，取最小值即可。

- **数据结构**：我们只需要记录两根手指当前所在的字母（或 `None` 表示还未放置）。这类似于查字典时的 **键‑值对**：键是手指编号（左/右），值是它所在的字符。  
- **正确性**：因为我们枚举了**所有**合法的指法分配，最优解一定会出现在枚举的集合里。  

> 这里的 “暴力” 就像把所有可能的钥匙都拿去尝试打开锁，肯定能找到那把对的钥匙，只是会花很多时间。

#### 代码（Python）

```python
from functools import lru_cache

# 预先把键盘坐标写进表，方便查距离
pos = {
    'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (0, 3), 'E': (0, 4), 'F': (0, 5), 'G': (0, 6),
    'H': (1, 0), 'I': (1, 1), 'J': (1, 2), 'K': (1, 3), 'L': (1, 4), 'M': (1, 5), 'N': (1, 6),
    'O': (2, 0), 'P': (2, 1), 'Q': (2, 2), 'R': (2, 3), 'S': (2, 4), 'T': (2, 5), 'U': (2, 6),
    'V': (3, 0), 'W': (3, 1), 'X': (3, 2), 'Y': (3, 3), 'Z': (3, 4)
}

def manhattan(a: str, b: str) -> int:
    """返回两个字母之间的曼哈顿距离"""
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    return abs(x1 - x2) + abs(y1 - y2)

def minimumDistance_bruteforce(word: str) -> int:
    n = len(word)

    @lru_cache(None)                     # 记忆化，防止重复计算同样子问题
    def dfs(idx: int, left: str, right: str) -> int:
        """
        idx   : 正在处理的字符下标
        left  : 左手指当前所在的字母（None 表示还没放）
        right : 右手指当前所在的字母（None 表示还没放）
        返回从 idx 开始往后敲完所有字符的最小额外距离
        """
        if idx == n:                     # 已经全部敲完
            return 0

        cur = word[idx]                  # 本次要敲的字符

        # 把 cur 给左手指
        cost_left = (0 if left is None else manhattan(left, cur))
        # 递归求后面的最小距离，左手指位置变成 cur，右手指保持不变
        ans_left = cost_left + dfs(idx + 1, cur, right)

        # 把 cur 给右手指（对称）
        cost_right = (0 if right is None else manhattan(right, cur))
        ans_right = cost_right + dfs(idx + 1, left, cur)

        # 取两种选择的最小值
        return min(ans_left, ans_right)

    # 初始时两根手指都没有放置（free），从第 0 个字符开始
    return dfs(0, None, None)
```

> **运行示例**  
> ```python
> print(minimumDistance_bruteforce("CAKE"))   # 3
> print(minimumDistance_bruteforce("HAPPY"))  # 6
> ```

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。因为每个字符都有两种指派方式，`n` 越大，分支树的叶子数会呈指数增长。  
- **空间复杂度**：`O(n)`（递归栈深度），加上记忆化表的大小 `O(2^n)`（最坏情况会存下所有子问题），所以总体也是指数级的。

> **大白话**：想象有 20 个字符，暴力解相当于要尝试 2^20 ≈ 1,000,000 次，已经远远超过一秒能跑完的量级。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于“每一次都把两根手指的状态全部记下来”，导致状态数爆炸。  
实际上，**只需要关心一根手指的位置**，另一根手指的当前位置可以在后面再决定。  

> **核心观察**  
> 当我们处理到第 `i` 个字符时，**必然有一根手指刚刚敲完这个字符**（记作“活动指”。）  
> 另一根手指的位置在之前的某一次敲字时被确定，它可能停在任意 26 个字母中的一个。  
> 因此我们可以把 **“活动指的位置固定为 word[i]”**，只把 **“另一根手指停在哪个字母”** 作为状态。

这样状态数从 `O(2^n)` 降到了 `O(26 * n)`，即每处理一个字符，只需要遍历 26 种可能的另一根手指位置。

**状态定义**  
`dp[c]` = 已经敲完前 `i` 个字符，**另一根手指**（不是刚敲完 `word[i-1]` 的那根）停在字母 `c` 时的最小总距离。  
- `c` 取值范围是 `'A' … 'Z'`（共 26 个）。
- 当 `i = 1`（只敲完第一个字符）时，另一根手指还没使用，所有 `dp[c] = 0`（因为起始位置免费）。

**状态转移**  
设当前要敲的字符是 `cur = word[i]`，上一字符是 `prev = word[i-1]`。有两种情况：

1. **继续用同一根手指**（即活动指保持不变）  
   - 那么另一根手指的停留字母 `c` 不变，费用为 `dp[c] + distance(prev, cur)`。  
   - 这对应 “把 `cur` 交给刚才敲 `prev` 的那根手指”。

2. **换到另一根手指**（把 `cur` 给另一根手指）  
   - 这时 **上一根手指** 成为“另一根手指”，它停在 `prev`。  
   - 那么新的 `dp[cur]`（因为活动指现在是 `cur`，另一根手指停在 `prev`）的费用为 `dp[prev] + distance(c, cur)`，其中 `c` 是原来“另一根手指”所在的字母。  
   - 换句话说，**把 `cur` 交给另一根手指**，需要付出把这根手指从它原来的位置 `c` 移动到 `cur` 的代价。

把两种情况取最小，即得到新的 `dp`。遍历所有 `c`（26 个）即可完成一次转移。

**答案**  
遍历完所有字符后，所有 `dp[c]` 中的最小值即为答案，因为最后一次敲完的字符一定是活动指，另一根手指可以停在任意字母。

#### 代码（Python）

```python
from typing import List

# 键盘坐标，同上面的定义
pos = {
    'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (0, 3), 'E': (0, 4), 'F': (0, 5), 'G': (0, 6),
    'H': (1, 0), 'I': (1, 1), 'J': (1, 2), 'K': (1, 3), 'L': (1, 4), 'M': (1, 5), 'N': (1, 6),
    'O': (2, 0), 'P': (2, 1), 'Q': (2, 2), 'R': (2, 3), 'S': (2, 4), 'T': (2, 5), 'U': (2, 6),
    'V': (3, 0), 'W': (3, 1), 'X': (3, 2), 'Y': (3, 3), 'Z': (3, 4)
}

def manhattan(a: str, b: str) -> int:
    """返回两个字母之间的曼哈顿距离"""
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    return abs(x1 - x2) + abs(y1 - y2)

def minimumDistance(word: str) -> int:
    """
    dp[c] 表示：已经敲完到当前位置，另一根手指停在字符 c 时的最小总距离。
    初始时另一根手指还没使用，所有 dp[c] = 0（免费放置）。
    """
    INF = 10 ** 9                     # 一个足够大的数，表示“不可能的情况”
    dp = [0] * 26                     # 26 个字母对应的最小费用
    # 只要把字符映射到 0~25 的下标，后面就可以用列表快速访问
    def idx(ch: str) -> int:
        return ord(ch) - ord('A')

    # 逐字符遍历，从第二个字符开始考虑转移
    for i in range(1, len(word)):
        cur = word[i]                 # 当前要敲的字符
        prev = word[i - 1]            # 前一个字符
        cur_i = idx(cur)
        prev_i = idx(prev)

        new_dp = [INF] * 26           # 本轮转移后得到的 dp 表

        # 情况 1：继续用同一根手指（活动指不换）
        # 对所有可能的另一根手指位置 c，费用 = dp[c] + dist(prev, cur)
        move_same = manhattan(prev, cur)
        for c in range(26):
            if dp[c] + move_same < new_dp[c]:
                new_dp[c] = dp[c] + move_same

        # 情况 2：换到另一根手指
        # 这时“另一根手指”会停在 prev，活动指是 cur。
        # 对所有原来的另一根手指位置 c，需要把它移动到 cur。
        for c in range(26):
            # 把 cur 交给另一根手指，需要把原来在 c 的手指移动到 cur
            cost = dp[c] + manhattan(chr(c + ord('A')), cur)
            # 新的“另一根手指”位置是 prev（因为原来的活动指变成了另一根）
            if cost < new_dp[prev_i]:
                new_dp[prev_i] = cost

        dp = new_dp                    # 进入下一轮

    # 最后答案是所有 dp[c] 中的最小值
    return min(dp)
```

> **运行示例**  
> ```python
> print(minimumDistance("CAKE"))   # 3
> print(minimumDistance("HAPPY"))  # 6
> ```

#### 复杂度  

- **时间复杂度**：`O(26 * n)` → `O(n)`（因为 26 是常数）。  
  对每个字符我们遍历 26 种可能的另一根手指位置，整体线性随字符串长度增长。  
- **空间复杂度**：`O(26)` → `O(1)`（常数空间）。只保存当前的 `dp` 数组和一个临时 `new_dp`。

> 与暴力解相比，时间从指数级骤降到线性级，几乎可以在毫秒级完成最长 300 字符的输入。

---

## 心得  

- **核心技巧**：**把“两个手指”压缩成“一根手指活动 + 另一根手指位置”**，利用 **状态压缩** 的动态规划。  
- **适用的题型**  
  1. **两个角色交替行动** 的问题（例如 “两个机器人收集水果”）。  
  2. **只关心一个变量的历史**，另一个变量可以用“状态索引”代替（例如 “键盘敲击最小移动距离”）。  
- **一句话总结解题钥匙**：**只保存必要的信息——活动指的字符必定是当前字符，另一根指的位置用 26 种可能枚举即可**。

---

## 反思  

- **第一反应**：看到“两个手指”和“曼哈顿距离”，第一时间想把每个字符的指派列举出来，导致想到暴力搜索。  
- **最容易踩的坑**  
  - **忘记起始位置免费**：一开始把第一字符的距离算成了非零，会把答案整体偏大。  
  - **状态转移写反**：把“另一根手指位置”写成“当前手指位置”，会导致转移公式不对。  
  - **边界条件**：字符串长度为 2 时，只有一次换手指的机会，需要确保 DP 初始化能覆盖这种最小规模。  
- **下次类似题的第一步**：先问自己 **“当前一步一定是谁在动？”**，把不动的那一方抽象成一个有限集合的状态，然后再设计 DP。这样可以迅速从指数爆炸的暴力思路转向线性 DP。