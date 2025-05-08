# #3178. K 秒后持球的孩子编号 / Find the Child Who Has the Ball After K Seconds

> 难度：简单 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-child-who-has-the-ball-after-k-seconds/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and k. There are n children numbered from 0 to n - 1 standing in a queue in order from left to right.
Initially, child 0 holds a ball and the direction of passing the ball is towards the right direction. After each second, the child holding the ball passes it to the child next to them. Once the ball reaches either end of the line, i.e. child 0 or child n - 1, the direction of passing is reversed.
Return the number of the child who receives the ball after k seconds.
Note: This question is the same as  2582: Pass the Pillow.

**Examples**

**Example 1:**

```
Input: n = 3, k = 5
Output: 1
Explanation:
```

**Example 2:**

```
Input: n = 5, k = 6
Output: 2
Explanation:
```

**Example 3:**

```
Input: n = 4, k = 2
Output: 2
Explanation:
```

**Constraints**

- 2 <= n <= 50
- 1 <= k <= 50

---

## 题目（中文翻译）

你得到两个正整数 `n` 和 `k`。有 `n` 个孩子，编号从 `0` 到 `n‑1`，从左到右依次站成一条队列（queue）。最初，孩子 `0` 手里拿着球（ball），传球的方向指向右侧。每过一秒，持球的孩子会把球传给相邻的下一个孩子。当球到达队列的任一端，即孩子 `0` 或孩子 `n‑1` 时，传球方向会反向。

返回经过 `k` 秒后接到球的孩子编号。

## 示例

### 示例 1
**输入**: `n = 3, k = 5`  
**输出**: `1`  
**解释**:

（此处省略具体过程的文字说明）

### 示例 2
**输入**: `n = 5, k = 6`  
**输出**: `2`  
**解释**:

（此处省略具体过程的文字说明）

### 示例 3
**输入**: `n = 4, k = 2`  
**输出**: `2`  
**解释**:

（此处省略具体过程的文字说明）

## 约束条件

- `2 <= n <= 50`
- `1 <= k <= 50`

> 注意：本题与 2582 题 **Pass the Pillow** 完全相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **模拟** 球的传递过程：

1. 用一个整数 `pos` 记录当前球所在的孩子编号，初始为 `0`（孩子 0 持球）。  
2. 用一个整数 `dir` 记录传递方向，`+1` 表示向右，`-1` 表示向左，初始为 `+1`。  
3. 每秒钟做一次下面的操作  
   * `pos += dir`（把球传给相邻的孩子）  
   * 检查是否到了两端：如果 `pos == 0` 或 `pos == n-1`，说明要掉头，`dir = -dir`。  
4. 重复步骤 3 共 `k` 次，最后的 `pos` 就是答案。

> **类比**：把孩子们想成排成一列的座位，`dir` 就像手里拿的“指示棒”，指向左或右，碰到墙壁（两端）就把棒子反过来。

只要把上述过程写成代码，就能得到正确答案，因为我们把每一秒的状态都完整地执行了一遍。

#### 代码（Python）

```python
def childAfterKSeconds_bruteforce(n: int, k: int) -> int:
    # 当前球所在的孩子编号
    pos = 0
    # 传递方向，+1 向右，-1 向左
    direction = 1

    for _ in range(k):                     # 重复 k 次，每次代表 1 秒
        pos += direction                    # 把球传给相邻的孩子
        # 碰到左端或右端，需要掉头
        if pos == 0 or pos == n - 1:
            direction = -direction         # 方向取反

    return pos
```

#### 复杂度

- **时间复杂度**：`O(k)`  
  需要循环 `k` 次，每次只做常数操作。  
  > 大白话：如果 `k` 是 10，程序会跑 10 步；如果 `k` 是 1 000 000，程序会跑 1 000 000 步。  

- **空间复杂度**：`O(1)`  
  只用了几个整数变量，和 `n、k` 的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每秒都要循环一次，当 `k` 很大时会很慢。  
观察球的运动轨迹可以发现规律：

```
n = 5 时的传递顺序（从第 0 秒开始）：
0 → 1 → 2 → 3 → 4 → 3 → 2 → 1 → 0 → 1 → 2 → …
```

可以看到：

* 球从左端走到右端需要 `n-1` 秒，随后再走回左端又需要 `n-1` 秒。  
* 完成一次“来回”总共用了 `2 * (n-1)` 秒，且状态完全回到最初（球又在 0 号孩子手里，方向向右）。

因此，**时间是周期性的**，周期长度 `cycle = 2 * (n - 1)`。  
只要把 `k` 取模这个周期，就等价于只模拟 `k % cycle` 秒：

```
k_effective = k % (2 * (n - 1))
```

剩下的步骤和暴力解完全相同，只是循环次数大幅减少（最多 `2*(n-1)-1`，而 `n ≤ 50`，所以最多 98 次）。

> **类比**：想象一条跑道，跑者每跑完一圈回到起点后，后面的动作跟第一圈一模一样。我们只需要关心“跑了多少圈的余数”。

#### 代码（Python）

```python
def childAfterKSeconds_optimal(n: int, k: int) -> int:
    # 计算有效的秒数（去掉完整的来回周期）
    cycle = 2 * (n - 1)               # 一次来回的总秒数
    k = k % cycle                     # 只需要模拟剩余的这段时间

    pos = 0
    direction = 1

    for _ in range(k):
        pos += direction
        if pos == 0 or pos == n - 1:
            direction = -direction

    return pos
```

#### 复杂度

- **时间复杂度**：`O(min(k, 2*(n-1)))` → 实际上是 `O(n)`（因为 `n ≤ 50`，常数很小）。  
  > 与暴力解相比，最多只循环 98 次，几乎可以忽略不计。  

- **空间复杂度**：`O(1)`  
  仍然只使用常数级别的额外变量。

---

## 心得

- **核心技巧**：**周期性（模运算）**  
  通过发现系统状态会在固定步数后重复，从而把大 `k` 转化为小 `k`。  

- **适用题型**  
  1. “传递球/枕头”类的来回运动（LeetCode 2582 Pass the Pillow）。  
  2. 环形数组的旋转或遍历（如轮流发牌、约瑟夫环）。  
  3. 任意在有限状态机中出现循环的模拟题。

- **解题钥匙**：**找出循环周期 → 用 `%` 把步数压缩**  

---

## 反思

- **第一反应**：直接写循环模拟，觉得代码最直观。  
- **最容易踩的坑**  
  * 忘记在到达两端时立即掉头，导致方向错误。  
  * 对 `k` 正好是周期倍数的情况处理不当（此时应该返回 `0`），如果不做模运算会多走完整个周期。  
  * 边界条件：`n = 2` 时周期是 `2`，代码仍然成立，但要确认 `pos` 不会越界。  

- **下次类似题的第一步**：先画出小规模的运动序列，观察是否出现**重复模式**；若有，立刻计算周期并使用取模来缩短模拟。