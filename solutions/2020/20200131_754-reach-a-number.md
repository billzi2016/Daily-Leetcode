# #754. 到达指定数字 / Reach a Number

> 难度：中等 · 标签：Math、Binary Search · [LeetCode 链接](https://leetcode.com/problems/reach-a-number/)

---

## 题目（英文原版）

**Description**

You are standing at position 0 on an infinite number line. There is a destination at position target.
You can make some number of moves numMoves so that:
Given the integer target, return the minimum number of moves required (i.e., the minimum numMoves) to reach the destination.

**Examples**

**Example 1:**

```
Input: target = 2
Output: 3
Explanation:
On the 1st move, we step from 0 to 1 (1 step).
On the 2nd move, we step from 1 to -1 (2 steps).
On the 3rd move, we step from -1 to 2 (3 steps).
```

**Example 2:**

```
Input: target = 3
Output: 2
Explanation:
On the 1st move, we step from 0 to 1 (1 step).
On the 2nd move, we step from 1 to 3 (2 steps).
```

**Constraints**

- -109 <= target <= 109
- target != 0

---

## 题目（中文翻译）

你站在无限数轴的 0 位置，目标位于位置 `target`。  
你可以进行若干次移动 `numMoves`，每一次移动的步长依次为 1、2、3、…，即第 `i` 次移动你必须走恰好 `i` 步（可以向左也可以向右）。  
给定整数 `target`，返回到达目标所需的最少移动次数（即最小的 `numMoves`）。

## 示例

### 示例 1
**输入:** `target = 2`  
**输出:** `3`  
**解释:**  
- 第 1 次移动，从 0 步进到 1（走 1 步）。  
- 第 2 次移动，从 1 步进到 -1（走 2 步，方向左）。  
- 第 3 次移动，从 -1 步进到 2（走 3 步，方向右）。

### 示例 2
**输入:** `target = 3`  
**输出:** `2`  
**解释:**  
- 第 1 次移动，从 0 步进到 1（走 1 步）。  
- 第 2 次移动，从 1 步进到 3（走 2 步，方向右）。

## 约束条件
- `-10^9 <= target <= 10^9`
- `target != 0`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**一步步模拟所有可能的移动**，直到走到目标位置 `target`。  
- 每一步的步长是递增的：第 1 步走 `+1`（或 `-1`），第 2 步走 `+2`（或 `-2`），第 3 步走 `+3`（或 `-3`）……  
- 对于每一步，我们可以选择“向左”或“向右”。这就像在走迷宫，每走一步都要决定是往左拐还是往右拐。  
- 用 **回溯**（DFS）或 **队列 BFS** 把所有可能的方向组合枚举出来，只要有一种组合的累计位置等于 `target`，对应的步数就是答案。

> **为什么这个方法一定能找到答案？**  
> 因为我们把**所有**合法的走法都遍历了一遍，必然会碰到最少步数的那条路径。

> **时间/空间复杂度大概是怎样的？**  
> 第 k 步有 2ⁿ 种方向组合，遍历到第 k 步的时间是 O(2ᵏ)。目标可能很大（|target| ≤ 10⁹），所以需要的步数可能上百，2¹⁰⁰ 的数量已经天文级别，根本不可接受。  
> 空间上我们要保存递归栈或 BFS 队列，最坏情况下也是 O(2ᵏ)。

#### 代码（Python）
```python
from collections import deque

def reach_number_brute(target: int) -> int:
    # BFS：每一层对应一步数，先到达 target 的层数即为最小步数
    target = abs(target)          # 由于左右对称，只考虑正数即可
    q = deque([(0, 0)])           # (当前位置, 已走步数)
    visited = set([0])            # 防止同一个位置重复入队

    while q:
        pos, steps = q.popleft()
        nxt_step = steps + 1      # 第 steps+1 步的步长

        # 两个可能的方向
        for nxt in (pos + nxt_step, pos - nxt_step):
            if nxt == target:     # 找到目标，返回步数+1
                return steps + 1
            if nxt not in visited and -target <= nxt <= target * 2:
                visited.add(nxt)
                q.append((nxt, steps + 1))

    # 理论上不会走到这里
    return -1
```
> **关键行解释**  
> - `target = abs(target)`: 目标的正负对称，只处理正数即可。  
> - `visited` 防止同一个位置被重复加入队列，避免无限扩张。  
> - `-target <= nxt <= target*2` 简单剪枝：走得太远已经没有意义。

#### 复杂度
- **时间复杂度**：O(2ᵏ)（k 为答案步数），实际会因为剪枝稍好，但仍然是指数级增长。  
- **空间复杂度**：O(2ᵏ) 用于存储 BFS 队列和 visited 集合。  

---

### 2. 最优解

#### 思路  
从暴力解可以看出**枚举方向是最慢的环节**。我们需要找到一种**只关心步数本身**的数学规律，而不是每一步的方向。

**关键观察 1：累计步长的和**  
第 k 步走的距离是 `1 + 2 + … + k = k·(k+1)/2`，记作 `S(k)`。如果我们把所有步都向同一个方向（全正），最终位置就是 `S(k)`。

**关键观察 2：可以把某些步改为向左**  
把第 i 步的方向改为左，则相当于在总和 `S(k)` 上**减去 2·i**（因为原来是 +i，现在是 -i，差值是 2i）。  
所以，任意一步的方向组合产生的最终位置一定形如：

```
final = S(k) - 2 * (sum of some selected step indices)
```

换句话说，**只要能够让 S(k) 与 target 同号且差值是偶数，就一定可以通过翻转若干步的方向得到 target**。

**关键观察 3：最小的 k 满足两个条件**  
1. `S(k) >= target`（总距离至少要覆盖目标）  
2. `S(k) - target` 为偶数（差值能被 2 整除，才能通过翻转实现）

因此算法可以这么写：

1. 把 `target` 取绝对值，利用对称性。  
2. 从 `k = 1` 开始累加步长，直到 `S(k) >= target`。  
3. 检查 `diff = S(k) - target` 是否为偶数。  
   - 若是，返回 `k`。  
   - 若否，继续增加 `k`（即再走一步），并再次检查。  
   - 这里有一个小技巧：当 `diff` 为奇数时，往往只需要再走 **1 步**（如果 `k+1` 为奇数）或 **2 步**（如果 `k+1` 为偶数）即可让差值变偶。  

**为什么这一步就能得到最小步数？**  
因为我们是从最小的 `k` 开始递增，只要当前 `k` 满足上述两个条件，就已经是最少的步数。后面的 `k` 只会更大，显然不是最优。

**需要的核心工具**  
- **等差数列求和公式** `S(k) = k*(k+1)//2`（一次算完）  
- **取模判断奇偶** `diff % 2 == 0`（判断是否为偶数）  

#### 代码（Python）
```python
def reach_number(target: int) -> int:
    """
    返回从 0 出发走到 target 所需的最少步数。
    思路：累加等差数列直到满足
          1) 累加和 >= target
          2) 累加和与 target 同号且差值为偶数
    """
    target = abs(target)                 # 只考虑正数，负数对称

    k = 0                                # 已走步数
    total = 0                            # S(k) = 1+2+...+k

    while True:
        k += 1
        total += k                       # 直接累加，等价于 S(k)

        if total >= target and (total - target) % 2 == 0:
            return k                     # 条件同时满足，k 即答案
```

> **关键行解释**  
> - `target = abs(target)`: 负数目标只需要把方向整体翻转，等价于正数。  
> - `total += k`: 用循环累加避免一次性乘除的溢出担忧（Python 本身不溢出，但更直观）。  
> - `if total >= target and (total - target) % 2 == 0:`：一次检查两个必要条件，满足即返回最小 `k`。

#### 复杂度
- **时间复杂度**：O(k)，其中 `k` 为答案步数。由于 `S(k) ≈ k²/2`，要使 `S(k) ≥ |target|`，大约需要 `k ≈ √(2·|target|)`。所以时间复杂度是 **O(√|target|)**，对 10⁹ 的目标也只需要几万次循环，极快。  
- **空间复杂度**：O(1) 只用几个整数变量，常数级空间。

---

## 心得

- **核心技巧**：把「向左/向右」的选择转化为「把总和减去偶数」的等价关系，利用等差数列求和和奇偶性判断快速定位最小步数。  
- **适用的题型**：  
  1. “Reach a Number” 系列（如 LeetCode 754）  
  2. “Minimum Number of Moves to Reach a Destination” 类的步长递增问题  
  3. “Find Minimum Operations to Reach a Target” 需要把累计值调到指定数的题目（常见于数学/二分搜索标签）  
- **一句话总结解题钥匙**：**“先让总距离够大，再让差值变成偶数”。**

---

## 反思

- **第一反应**：看到递增步长就想到“累加”，于是尝试暴力搜索所有方向。  
- **最容易踩的坑**：  
  - 忽略了负数目标的对称性，导致实现时要处理正负两套逻辑。  
  - 没注意到差值必须为偶数的条件，直接返回 `k` 会在某些情况下得到错误答案（例如 target=2 时 k=2 不行，需要 k=3）。  
  - 在循环中忘记更新 `total`，导致无限循环。  
- **下次遇到同类题的第一步**：先**写出累计步长的闭式表达式**，再**分析奇偶性或可达性条件**，最后**只在步数上二分或线性搜索**，而不是在方向上枚举。