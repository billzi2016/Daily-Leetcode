# #2337. 移动棋子得到字符串 / Move Pieces to Obtain a String

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/move-pieces-to-obtain-a-string/)

---

## 题目（英文原版）

**Description**

You are given two strings start and target, both of length n. Each string consists only of the characters 'L', 'R', and '_' where:
Return true if it is possible to obtain the string target by moving the pieces of the string start any number of times. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: start = "_L__R__R_", target = "L______RR"
Output: true
Explanation: We can obtain the string target from start by doing the following moves:
- Move the first piece one step to the left, start becomes equal to "L___R__R_".
- Move the last piece one step to the right, start becomes equal to "L___R___R".
- Move the second piece three steps to the right, start becomes equal to "L______RR".
Since it is possible to get the string target from start, we return true.
```

**Example 2:**

```
Input: start = "R_L_", target = "__LR"
Output: false
Explanation: The 'R' piece in the string start can move one step to the right to obtain "_RL_".
After that, no pieces can move anymore, so it is impossible to obtain the string target from start.
```

**Example 3:**

```
Input: start = "_R", target = "R_"
Output: false
Explanation: The piece in the string start can move only to the right, so it is impossible to obtain the string target from start.
```

**Constraints**

- n == start.length == target.length
- 1 <= n <= 105
- start and target consist of the characters 'L', 'R', and '_'.

---

## 题目（中文翻译）

**题目描述**

给定两个长度均为 `n` 的字符串 `start` 和 `target`。每个字符串仅由字符 `'L'`、`'R'` 和 `'_'` 组成，其中：

- `'L'` 表示只能向左移动的棋子（piece）；
- `'R'` 表示只能向右移动的棋子；
- `'_'` 表示空位（empty cell）。

在一次移动中，你可以将任意一个棋子向其允许的方向移动一步，前提是该方向相邻的格子是空位 `'_'`。棋子可以进行任意次数的移动，但不能跨过其他棋子，也不能改变棋子的相对顺序。

如果可以通过若干次移动将 `start` 变换为 `target`，返回 `true`；否则返回 `false`。

---

**示例**

**示例 1**

```
Input: start = "_L__R__R_", target = "L______RR"
Output: true
Explanation: 我们可以按如下步骤得到 target：
- 将第一个棋子向左移动一步，`start` 变为 "L___R__R_"
- 将最后一个棋子向右移动一步，`start` 变为 "L___R___R"
- 将第二个棋子向右移动三步，`start` 变为 "L______RR"
```

**示例 2**

```
Input: start = "R_L_", target = "__LR"
Output: false
Explanation: `start` 中的 `'R'` 棋子只能向右移动一步得到 "_RL_"。此时没有棋子可以再移动，因此无法得到 `target`。
```

**示例 3**

```
Input: start = "_R", target = "R_"
Output: false
Explanation: `'R'` 棋子只能向右移动，无法将其移动到左侧，从而无法得到 `target`。
```

---

**约束条件**

- `n == start.length == target.length`
- `1 <= n <= 10^5`
- `start` 和 `target` 仅由字符 `'L'`、`'R'` 和 `'_'` 组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有合法的移动都模拟一遍**，看能不能恰好得到 `target`。  
- 每一次移动只能把字符 `'L'` 往左走一格，或者把字符 `'R'` 往右走一格，前提是目的格是 `'_'`（空位）。  
- 我们可以把字符串看成一排格子，`'_'` 就像一本字典的空白页，`'L'`、`'R'` 则是只能向特定方向“翻页”的棋子。  
- 暴力做法：遍历整个字符串，凡是看到可以移动的棋子就把它往对应方向移动一步，循环直到一次遍历中没有任何移动为止。最后把得到的字符串和 `target` 做比较，若相等则返回 `True`，否则 `False`。  

为什么这种方法能得到正确答案？  
只要我们一直把**所有**能够移动的棋子一步一步搬走，最终的状态一定是**所有棋子已经走到它们能走的最远位置**。如果在这个“最远”状态仍然和目标不一致，说明无论怎么移动都不可能匹配目标。  

**时间/空间分析（大白话）**  
- 每一次完整遍历字符串的时间是 `O(n)`（`n` 是字符串长度）。  
- 最坏情况下，一块棋子可能需要走 `n` 步才能到达最左/最右端，而我们每走一步都要重新遍历一次整个字符串。于是总的遍历次数可能是 `n` 次，导致整体时间复杂度是 `O(n²)`，也就是 **“平方级”**，在 `n=10⁵` 时会超时。  
- 只用了原字符串的副本和若干计数变量，空间是 `O(1)`（常数级），不随 `n` 增长。

#### 代码（Python）

```python
def canChange(start: str, target: str) -> bool:
    # 把字符串转成列表，方便原地修改
    s = list(start)
    n = len(s)

    while True:
        moved = False               # 本轮是否有棋子真的移动了
        i = 0
        while i < n:
            # 'L' 只能往左走，且左边必须是空位
            if s[i] == 'L' and i > 0 and s[i - 1] == '_':
                s[i - 1], s[i] = s[i], '_'   # 交换位置
                moved = True
                i -= 1        # 向左检查，防止同一块 L 再次移动
            # 'R' 只能往右走，且右边必须是空位
            elif s[i] == 'R' and i + 1 < n and s[i + 1] == '_':
                s[i + 1], s[i] = s[i], '_'   # 交换位置
                moved = True
                i += 1        # 跳过已经移动到的 R，避免重复判断
            i += 1

        if not moved:          # 本轮没有任何移动，说明已经“最远”
            break

    # 把列表再拼回字符串，与目标比较
    return ''.join(s) == target
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  想象一下有 `n` 只小动物，每只动物最多要走 `n` 步，每走一步我们都要重新检查整条路，这就是“平方级”耗时。
- **空间复杂度**：`O(1)`（不计输出字符串本身）  
  只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**反复遍历整条字符串**，而我们其实可以一次遍历就判断出答案。关键在于以下两个观察：

1. **相对顺序永远不会改变**  
   - `'L'` 只能往左，`'R'` 只能往右，它们之间的相对顺序（先出现的在左边，后出现的在右边）在任何合法移动后保持不变。  
   - 因此如果把所有 `'_'` 删除，只剩下字符序列 `L`/`R`，这两个序列在 `start` 和 `target` 必须完全相同。  
   - 类比：把字符串看成一本字典，`'L'`、`'R'` 就是词条，只能往左或往右翻页，翻页不会让词条的顺序乱掉。

2. **每个棋子移动的方向受限**  
   - 对于 `'L'`：它只能左移，所以在 `start` 中出现的位置 **必须不小于**（即在右边）它在 `target` 中出现的位置。换句话说，`start` 的 `'L'` 不能出现在目标 `'L'` 的左边。  
   - 对于 `'R'`：只能右移，所以在 `start` 中出现的位置 **必须不大于**（即在左边）它在 `target` 中出现的位置。  

基于上述两点，我们可以使用 **双指针**（两个指针分别在 `start`、`target` 上移动）一次遍历完成检查：

1. 跳过所有 `'_'`，让指针指向下一个实际的棋子。  
2. 比较两个指针指向的字符是否相同（都是 `'L'` 或都是 `'R'`），若不同直接返回 `False`。  
3. 若相同，再根据字符类型检查位置约束：  
   - `'L'`：`i_start >= i_target` 必须成立。  
   - `'R'`：`i_start <= i_target` 必须成立。  
4. 两个指针各自向后继续寻找下一个棋子，直到遍历完所有字符。  
5. 最后如果两个指针都到达字符串末尾，则说明所有约束都满足，返回 `True`。

这一步只遍历一次字符串，时间是线性的 `O(n)`，空间只用了几个指针变量 `O(1)`。

#### 代码（Python）

```python
def canChange(start: str, target: str) -> bool:
    n = len(start)
    i = j = 0          # i 遍历 start，j 遍历 target

    while i < n or j < n:
        # 跳过 '_'，找到下一个真实的棋子
        while i < n and start[i] == '_':
            i += 1
        while j < n and target[j] == '_':
            j += 1

        # 两边都遍历完了，说明剩下的都是 '_'，直接结束
        if i == n and j == n:
            return True
        # 只剩下一个字符串还有棋子，说明数量不匹配
        if (i == n) != (j == n):
            return False

        # 此时 start[i] 与 target[j] 必须是同一种棋子
        if start[i] != target[j]:
            return False

        # 检查移动方向的约束
        if start[i] == 'L' and i < j:   # L 只能左移，i 必须在右边
            return False
        if start[i] == 'R' and i > j:   # R 只能右移，i 必须在左边
            return False

        # 都满足，继续向后找下一个棋子
        i += 1
        j += 1

    return True
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了两遍字符串（一次同步，两次各自跳过 '_'），所以时间随 `n` 成线性增长。相比暴力的 `O(n²)`，速度快了几个数量级。
- **空间复杂度**：`O(1)` — 只用了常数个整数指针和临时变量，和输入规模无关。

---

## 心得

- **核心技巧**：**相对顺序不变 + 方向约束**，用双指针一次遍历即可判断。  
- **适用的题型**：  
  1. “移动棋子”类题目（如 LeetCode 778 `Swim in Rising Water` 中的单调栈思路）  
  2. “只允许单方向移动” 的字符串变换（如 `Swap Adjacent in LR String`、`Minimum Moves to Make Array Complementary`）  
  3. “保持相对顺序” 的数组/字符串匹配（如 `Is Subsequence`）  
- **一句话总结**：**先确认顺序相同，再检查每个棋子是否还能往合法方向到达目标位置**。

---

## 反思

- **第一反应**：先想“把所有可能的移动都枚举”，于是跑出了暴力 BFS/模拟的想法。  
- **最容易踩的坑**：  
  - 忽略了 `'L'` 只能左移、`'R'` 只能右移的方向限制，导致错误地认为只要字符种类相同就一定可达。  
  - 边界情况：全部是 `'_'`，或者某一侧多出一个 `'L'`/`'R'`，都需要在指针遍历结束时统一检查。  
- **下次遇到同类题**：第一步先问自己**“棋子能否调换顺序？”**，如果答案是不能，就把两个字符串的“有效字符序列”对齐，用双指针检查**位置是否满足单向移动的约束**。这样往往能在 `O(n)` 时间内得到答案。