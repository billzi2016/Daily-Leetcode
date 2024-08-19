# #2833. 离原点最远的点 / Furthest Point From Origin

> 难度：简单 · 标签：String、Counting · [LeetCode 链接](https://leetcode.com/problems/furthest-point-from-origin/)

---

## 题目（英文原版）

**Description**

You are given a string moves of length n consisting only of characters 'L', 'R', and '_'. The string represents your movement on a number line starting from the origin 0.
In the ith move, you can choose one of the following directions:
Return the distance from the origin of the furthest point you can get to after n moves.

**Examples**

**Example 1:**

```
Input: moves = "L_RL__R"
Output: 3
Explanation: The furthest point we can reach from the origin 0 is point -3 through the following sequence of moves "LLRLLLR".
```

**Example 2:**

```
Input: moves = "_R__LL_"
Output: 5
Explanation: The furthest point we can reach from the origin 0 is point -5 through the following sequence of moves "LRLLLLL".
```

**Example 3:**

```
Input: moves = "_______"
Output: 7
Explanation: The furthest point we can reach from the origin 0 is point 7 through the following sequence of moves "RRRRRRR".
```

**Constraints**

- 1 <= moves.length == n <= 50
- moves consists only of characters 'L', 'R' and '_'.

---

## 题目（中文翻译）

你得到一个长度为 `n` 的字符串 `moves`，仅由字符 `'L'`、`'R'` 和 `'_'` 组成。该字符串描述了你在数轴（number line）上从原点 `0` 开始的移动。

在第 `i` 次移动时，你可以从以下方向中任选其一进行选择：

返回在完成 `n` 次移动后，你能够到达的最远点到原点的距离。

---

### 示例

#### 示例 1
**输入:** `moves = "L_RL__R"`  
**输出:** `3`  
**解释:** 通过以下移动序列 `"LLRLLLR"`，我们可以从原点 `0` 到达最远的点 `-3`，其距离为 `3`。

#### 示例 2
**输入:** `moves = "_R__LL_"`  
**输出:** `5`  
**解释:** 通过以下移动序列 `"LRLLLLL"`，我们可以从原点 `0` 到达最远的点 `-5`，其距离为 `5`。

#### 示例 3
**输入:** `moves = "_______"`  
**输出:** `7`  
**解释:** 通过以下移动序列 `"RRRRRRR"`，我们可以从原点 `0` 到达最远的点 `7`，其距离为 `7`。

---

### 约束条件
- `1 <= moves.length == n <= 50`
- `moves` 仅由字符 `'L'`、`'R'` 和 `'_'` 组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把下划线 `'_'` 当成“可以自行决定向左还是向右”的自由开关。  
- **遍历所有可能**：对每一个 `'_'`，我们都有两种选择（左 `L` 或右 `R`），于是所有可能的走法就是把这些二选一组合起来，形成 `2^{cnt_}` 种不同的完整指令串。  
- **模拟走法**：把每一种完整指令串从原点 `0` 按顺序执行，记录最终所在的位置 `pos`，取其绝对值 `|pos|`（因为题目要“最远离原点的距离”，方向不重要，只看距离）。  
- **取最大**：所有走法中最大的 `|pos|` 就是答案。

> **类比**：把 `'_'` 想成一本词典里缺的页码，你可以随意填上“左”或“右”。要找出最远的点，就得把每一种填法都尝试一次，就像把所有可能的钥匙都试一遍，看看哪把能打开最远的门。

这种方法一定能得到正确答案，因为我们穷举了**所有**合法的走法。

#### 代码（Python）

```python
from itertools import product

def furthest_distance_bruteforce(moves: str) -> int:
    # 统计下划线出现的位置
    underscore_idx = [i for i, ch in enumerate(moves) if ch == '_']
    k = len(underscore_idx)                     # 下划线的个数

    # 如果没有下划线，直接模拟一次即可
    if k == 0:
        pos = 0
        for ch in moves:
            pos += 1 if ch == 'R' else -1      # R → +1，L → -1
        return abs(pos)

    max_dist = 0
    # product 会生成所有 0/1 的组合，0 代表填 L，1 代表填 R
    for combo in product((0, 1), repeat=k):
        # 把原字符串转成列表，方便修改
        cur = list(moves)
        for idx, fill in zip(underscore_idx, combo):
            cur[idx] = 'R' if fill else 'L'    # 填入 L 或 R

        # 模拟走完所有步数
        pos = 0
        for ch in cur:
            pos += 1 if ch == 'R' else -1
        max_dist = max(max_dist, abs(pos))

    return max_dist
```

> 关键行解释  
> - `product((0, 1), repeat=k)`：相当于把 `k` 个下划线每个都抛一次硬币，得到所有可能的填法。  
> - `pos += 1 if ch == 'R' else -1`：左走记为 `-1`，右走记为 `+1`，把移动累加到当前位置。

#### 复杂度  

- **时间复杂度**：`O(2^{cnt_} * n)`  
  - `2^{cnt_}` 是所有可能的填法数（指数级），每种填法需要遍历长度为 `n` 的字符串来模拟移动。  
  - 大白话：如果下划线有 10 个，需要尝试 1024 种走法；如果有 20 个，就要尝试超过一百万种，明显会很慢。

- **空间复杂度**：`O(n)`  
  - 主要是保存临时的字符列表 `cur`（长度 `n`）以及递归/迭代产生的组合。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正耗时的地方是**枚举每一种填法**。其实我们不需要把每个 `'_'` 单独考虑，因为所有 `'_'` 的贡献只在于它们的**方向总和**——每向左一次就 `-1`，向右一次就 `+1`。  

1. **把已确定的步数先算出来**  
   - 已有的 `L` 都是 `-1`，`R` 都是 `+1`。  
   - 设 `base = (#R) - (#L)`，这就是在不使用下划线时最终的位置（可以是负数）。

2. **下划线的自由度**  
   - 有 `k = cnt_` 个下划线，每个可以是 `+1`（右）或 `-1`（左）。  
   - 把它们全都选成右，则总贡献是 `+k`；全都选成左，则总贡献是 `-k`。  
   - 所以最终位置的可能取值只有 **两种极端**：`base + k` 或 `base - k`。  
   - 其他混合填法（比如一半左、一半右）会让位置落在这两者之间，绝对值必然不大于这两个极端。

3. **取最大绝对值**  
   - `ans = max(|base + k|, |base - k|)`。  
   - 这一步相当于“把所有下划线都往同一个方向走”，因为这样才能把偏离原点的距离拉到最大。  

> **类比**：想象你站在原点，左边有若干负向的石子（`L`），右边有正向的石子（`R`），而下划线是可以随意搬动的石子。要让自己离原点最远，只需要把所有可以搬动的石子全部搬到已有石子较多的一侧，形成最大的“力矩”。  

#### 代码（Python）

```python
def furthest_distance_optimal(moves: str) -> int:
    cnt_L = moves.count('L')
    cnt_R = moves.count('R')
    cnt_ = moves.count('_')

    base = cnt_R - cnt_L          # 已确定的左/右步数之差
    # 两种极端情况：全部填 R 或全部填 L
    far1 = abs(base + cnt_)       # 全部填成 R
    far2 = abs(base - cnt_)       # 全部填成 L

    return max(far1, far2)
```

> 关键行解释  
> - `moves.count('L')`、`moves.count('R')`、`moves.count('_')`：一次遍历即可统计三类字符的数量。  
> - `base = cnt_R - cnt_L`：左走记为 `-1`，右走记为 `+1`，两者相减得到当前的净位移。  
> - `abs(base + cnt_)` 与 `abs(base - cnt_)`：分别对应把所有下划线都当成右走或左走的情况。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需一次遍历统计字符个数，常数级的几次算术运算。  
  - 与暴力解的指数级相比，快得多——即使 `n=50` 也只需几微秒。

- **空间复杂度**：`O(1)`  
  - 只用几个整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：把可变的下划线视为“可自由取值的 +1/-1”，利用**线性代数的极值原则**（在一维情况下，最大绝对值必出现在所有自由变量取同号的极端）。  
- **适用题型**：  
  1. “把所有 `?` 替换成 `a` 或 `b`，求最大/最小某个计数”——如 `Maximum Score After Splitting a String`。  
  2. “给定固定步数和可调步数，求最远距离”——如 “Maximum Distance Between Two Cities” 类似的路径问题。  
- **一句话总结**：**把所有可自由决定的步统一向同一方向，就能让距离最大**。

---

## 反思

- **第一反应**：看到下划线会想到“遍历所有可能”，于是想到暴力搜索。  
- **最容易踩的坑**：  
  - 忽视了 **混合填法** 并不会产生更大的距离，导致不必要的复杂度。  
  - 计算绝对值时忘记比较两种极端情况（全左或全右），只算了其中一种会得到错误答案。  
- **下次类似题的第一步**：先把 **确定的部分** 计数，求出“基准位移”，再思考 **可自由调节的部分** 能在数轴上怎样拉伸这条基准线——往往答案就是把自由部分全部推向同一方向。