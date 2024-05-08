# #2682. 找出循环游戏的输家 / Find the Losers of the Circular Game

> 难度：简单 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-losers-of-the-circular-game/)

---

## 题目（英文原版）

**Description**

There are n friends that are playing a game. The friends are sitting in a circle and are numbered from 1 to n in clockwise order. More formally, moving clockwise from the ith friend brings you to the (i+1)th friend for 1 <= i < n, and moving clockwise from the nth friend brings you to the 1st friend.
The rules of the game are as follows:
1st friend receives the ball.
In other words, on the ith turn, the friend holding the ball should pass it to the friend who is i * k steps away from them in the clockwise direction.
The game is finished when some friend receives the ball for the second time.
The losers of the game are friends who did not receive the ball in the entire game.
Given the number of friends, n, and an integer k, return the array answer, which contains the losers of the game in the ascending order.

**Examples**

**Example 1:**

```
Input: n = 5, k = 2
Output: [4,5]
Explanation: The game goes as follows:
1) Start at 1st friend and pass the ball to the friend who is 2 steps away from them - 3rd friend.
2) 3rd friend passes the ball to the friend who is 4 steps away from them - 2nd friend.
3) 2nd friend passes the ball to the friend who is 6 steps away from them  - 3rd friend.
4) The game ends as 3rd friend receives the ball for the second time.
```

**Example 2:**

```
Input: n = 4, k = 4
Output: [2,3,4]
Explanation: The game goes as follows:
1) Start at the 1st friend and pass the ball to the friend who is 4 steps away from them - 1st friend.
2) The game ends as 1st friend receives the ball for the second time.
```

**Constraints**

- 1 <= k <= n <= 50

---

## 题目（中文翻译）

**题目描述**  
有 `n` 位朋友在玩一个游戏。朋友们按顺时针顺序围成一个圆圈，编号为 `1` 到 `n`。更正式地说，顺时针从第 `i` 位朋友移动会到第 `i+1` 位朋友（`1 ≤ i < n`），而顺时针从第 `n` 位朋友移动会回到第 `1` 位朋友。  

游戏规则如下：  
1. 第 `1` 位朋友先收到球。  
2. 在第 `i` 轮时，持球的朋友需要把球传给顺时针方向上距离他 **`i * k`** 步的朋友。  
3. 当某位朋友第二次收到球时，游戏结束。  

在整个游戏过程中 **没有收到过球的朋友** 被视为输家（losers）。  
给定朋友的数量 `n` 和整数 `k`，返回一个数组 `answer`，其中按升序排列所有输家的编号。

**示例 1**  
```
输入: n = 5, k = 2
输出: [4,5]
解释: 游戏过程如下:
1) 从第 1 位朋友开始，将球传给顺时针方向上距离 2 步的朋友 → 第 3 位朋友。
2) 第 3 位朋友将球传给顺时针方向上距离 4 步的朋友 → 第 2 位朋友。
3) 第 2 位朋友将球传给顺时针方向上距离 6 步的朋友 → 第 3 位朋友。
4) 第 3 位朋友再次收到球，游戏结束。
未曾收到球的朋友是第 4 位和第 5 位，因此输出 [4,5]。
```

**示例 2**  
```
输入: n = 4, k = 4
输出: [2,3,4]
解释: 游戏过程如下:
1) 从第 1 位朋友开始，将球传给顺时针方向上距离 4 步的朋友 → 第 1 位朋友（因为环形结构）。
2) 第 1 位朋友再次收到球，游戏结束。
未曾收到球的朋友是第 2、3、4 位，所以输出 [2,3,4]。
```

**约束条件**  
- `1 ≤ k ≤ n ≤ 50`   (所有数值均为整数)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把朋友们想象成坐在圆桌上的座位，编号从 **1** 到 **n**，顺时针方向依次相邻。  
游戏的过程其实就是：

1. 从第 1 位朋友手里拿球。  
2. 第 `i` 次传球时，当前持球者要把球传给 **顺时针走 `i·k` 步** 的朋友。  
3. 当某个人第二次收到球时，游戏结束。

所以最直接的做法就是 **一步步模拟** 这个过程，直到出现第二次接球的玩家为止。  
在模拟的过程中，用一个哈希表（在 Python 中用 `set`）记录已经接过球的朋友编号——  
`set` 就像一本“字典”，把朋友编号（key）映射到“已经出现过”这个状态（value），查询和插入都只需要 O(1) 的时间。

当游戏结束后，所有 **不在已接球集合** 中的朋友就是输家，按升序返回即可。

> **为什么正确？**  
> 我们严格按照题目描述的规则一步步执行，没有遗漏任何一次传球，也没有提前结束。只要出现第二次接球，就恰好是游戏规定的终止条件。于是记录下的所有接球者就是完整的“获胜者”，其余的自然是“输家”。  

> **复杂度直观解释**  
> - `O(n²)` 这种写法可以想象成“把 n 张纸两两比较”，即每一次操作都可能遍历整个集合。  
> - `O(n)` 则像“只走一遍路”，每个朋友最多只被访问一次。

#### 代码（Python）

```python
def circularGameLosers(n: int, k: int) -> list[int]:
    # 已经接过球的朋友集合，类似“查字典”
    visited = set()
    # 第一次持球的是第 1 位
    cur = 1
    visited.add(cur)          # 记录 1 已经接过球

    step = 1                  # 第几次传球（从 1 开始计数）
    while True:
        # 计算下一位朋友的编号
        # (cur - 1) 把编号转成 0 开始的下标，方便取模
        nxt = (cur - 1 + step * k) % n + 1

        # 如果 nxt 已经在 visited 中，说明第二次接球，游戏结束
        if nxt in visited:
            break

        visited.add(nxt)      # 否则记录 nxt 已经接过球
        cur = nxt             # 球交给 nxt
        step += 1             # 进入下一轮传球

    # 所有没有出现在 visited 中的编号就是输家，升序返回
    losers = [i for i in range(1, n + 1) if i not in visited]
    return losers
```

#### 复杂度

- **时间复杂度**：`O(n)` — 最坏情况下每个朋友最多只会被访问一次（因为游戏在所有人都接过球或出现重复时必然结束），所以时间随人数线性增长。  
- **空间复杂度**：`O(n)` — 需要用 `set` 存放已经接球的朋友编号，最坏会保存全部 `n` 个人的编号。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性模拟**，在本题的约束（`n ≤ 50`）下已经足够快。  
如果把 “暴力” 理解成 **每次都遍历整个数组去找下一个人**，那显然会是 `O(n²)`。  
我们可以把 **查找下一个人的过程** 用 **取模运算**（`% n`）直接算出来，避免任何遍历，从而把时间降到 `O(n)`。  

关键点：

1. **取模运算**：因为朋友坐成环，编号超出 `n` 时需要回到开头。`(cur-1 + step*k) % n + 1` 正好把“顺时针走 step·k 步”映射到 1~n 的合法编号。  
2. **哈希表（集合）**：记录已经出现过的编号，查询是否重复只需要 O(1)。这一步相当于把 “已经接过球的朋友列表” 从线性搜索改成常数时间查找。  
3. **终止条件**：只要出现第二次接球就结束，保证不会出现无限循环。

这样，整体思路仍然是 **模拟**，但所有操作都是常数时间，已是最优的线性解法。

> **类比**：想象你在一条环形跑道上跑步，每跑 `step*k` 米就记录一次位置。如果你每次都用地图全走一遍去找自己现在在哪，那会很慢；而直接用手表算出“我现在在第几格”就快多了。

#### 代码（Python）

```python
def circularGameLosers(n: int, k: int) -> list[int]:
    visited = set()               # 已接球的朋友集合
    cur = 1                       # 从 1 号朋友开始
    visited.add(cur)

    step = 1                      # 第几次传球
    while True:
        # 直接算出下一个朋友的编号（取模保证环形）
        nxt = (cur - 1 + step * k) % n + 1

        if nxt in visited:        # 已经出现过 → 游戏结束
            break

        visited.add(nxt)          # 记录新出现的朋友
        cur = nxt                 # 球交给 nxt
        step += 1                 # 进入下一轮

    # 输出未出现过的编号，升序
    return [i for i in range(1, n + 1) if i not in visited]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每轮传球只做常数次算术和集合查询，最多进行 `n` 轮（因为最多有 `n` 个人接球）。相较于 “每次遍历数组找下一个人” 的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(n)` — 需要保存所有已经接球的编号，最坏保存 `n` 个元素。

---

## 心得

- **核心技巧**：**取模运算 + 哈希集合** 用来在环形结构中快速定位下一个元素并判断是否重复。  
- **适用的题型**：  
  1. 环形游戏/约瑟夫环（Josephus）类问题。  
  2. “循环数组”里寻找下一个满足条件的元素（如循环右移、循环跳步等）。  
  3. “检测循环” 类问题（比如判断链表是否有环的思路类似）。  
- **一句话总结**：**“环上前进一步，用模算位置，用集合记历史，一旦重复即停”。**

## 反思

- **第一反应**：直接把游戏过程写成循环，每次把球传给下一个人，直到出现重复。  
- **最容易踩的坑**：  
  - **取模位置错误**：忘记把编号转成 0‑based 再取模，导致越界或错位。  
  - **忘记记录第一次出现的朋友**：只检查第二次出现会导致提前结束。  
  - **边界条件**：`k = n` 或 `k = 1` 时，球可能立即回到自己，需要保证循环能够正确结束。  
- **下次遇到同类题**：第一步先 **明确“环形”结构**，把“走几步”转成 **`(cur-1 + 步数) % n + 1`**，然后用 **集合** 检测是否已访问，保证 O(1) 判断。这样就能快速写出正确且高效的模拟代码。