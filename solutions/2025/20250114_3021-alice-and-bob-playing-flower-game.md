# #3021. Alice 与 Bob 的花园游戏 / Alice and Bob Playing Flower Game

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/alice-and-bob-playing-flower-game/)

---

## 题目（英文原版）

**Description**

Alice and Bob are playing a turn-based game on a circular field surrounded by flowers. The circle represents the field, and there are x flowers in the clockwise direction between Alice and Bob, and y flowers in the anti-clockwise direction between them.
The game proceeds as follows:
Given two integers, n and m, the task is to compute the number of possible pairs (x, y) that satisfy the conditions:
Return the number of possible pairs (x, y) that satisfy the conditions mentioned in the statement.

**Examples**

**Example 1:**

```
Input: n = 3, m = 2
Output: 3
Explanation: The following pairs satisfy conditions described in the statement: (1,2), (3,2), (2,1).
```

**Example 2:**

```
Input: n = 1, m = 1
Output: 0
Explanation: No pairs satisfy the conditions described in the statement.
```

**Constraints**

- 1 <= n, m <= 105

---

## 题目（中文翻译）

Alice 与 Bob 正在一个被花环绕的圆形场地上进行回合制游戏。圆圈代表场地，Alice 与 Bob 之间顺时针方向有 **x** 朵花，逆时针方向有 **y** 朵花。

游戏按照如下方式进行：

给定两个整数 **n** 和 **m**，求满足题目描述中条件的可能的配对 **(x, y)** 的数量。返回满足上述条件的配对数。

---

### 示例

#### 示例 1
**输入**: `n = 3, m = 2`  
**输出**: `3`  
**解释**: 符合题目条件的配对有 `(1,2)`, `(3,2)`, `(2,1)`。

#### 示例 2
**输入**: `n = 1, m = 1`  
**输出**: `0`  
**解释**: 没有配对满足题目条件。

---

### 约束条件
- `1 <= n, m <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的 `(x, y)` 都枚举一遍，逐个检查它们的奇偶性是否不同。  
- **数据结构**：只需要两个普通的 `for` 循环，不需要额外的数据结构。可以把它想象成在一张表格里逐格填数，表格的行代表 `x`，列代表 `y`，我们逐格查看格子里写的两个数是“奇数‑偶数”还是“偶数‑奇数”。  
- **正确性**：只要遍历了所有合法的 `x`（`1 … n`）和所有合法的 `y`（`1 … m`），并且把满足“奇偶不同”这一条件的组合计数，就一定不会漏掉也不会多计。  

#### 代码（Python）

```python
def countPairs_bruteforce(n: int, m: int) -> int:
    cnt = 0                         # 计数器，记录满足条件的组合数
    for x in range(1, n + 1):       # 枚举所有可能的 x
        for y in range(1, m + 1):   # 枚举所有可能的 y
            # 判断 x 与 y 的奇偶性是否不同
            if (x % 2) != (y % 2):  # %2 得到余数，0 表示偶数，1 表示奇数
                cnt += 1           # 满足条件，计数器加一
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - 这里的 `O` 记号可以理解为“随着 `n` 和 `m` 变大，程序运行时间大约会像 `n` 乘以 `m` 那样增长”。如果 `n = m = 10⁵`，则需要遍历 10⁵ × 10⁵ = 10¹⁰ 次，显然不可接受。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和 `n、m` 的大小无关，所占内存可以看作是常数级别。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正耗时的地方是两层循环**——每一次循环只做了一件事：判断奇偶性。  
我们可以把“奇偶性”这件事提前统计出来，**不必逐个检查**。  

1. **统计区间 `[1, n]` 中奇数和偶数的个数**  
   - 奇数的个数 = `(n + 1) // 2`  
     - 解释：如果 `n` 是奇数，前 `(n+1)/2` 个数都是奇数；如果 `n` 是偶数，前 `n/2` 个数是奇数，`(n+1)//2` 正好把这两种情况统一起来。  
   - 偶数的个数 = `n // 2`（整数除法直接把 `n` 除以 2，向下取整）。  

2. 同理，统计区间 `[1, m]` 中奇数和偶数的个数。  

3. **满足奇偶不同的配对有两种**  
   - `x` 为奇数，`y` 为偶数 → `odd_n * even_m` 种  
   - `x` 为偶数，`y` 为奇数 → `even_n * odd_m` 种  

4. 把两种情况相加，即为答案。  

> **类比**：想象有两箱球，一箱里装的是 “奇数球”，另一箱是 “偶数球”。我们要从两箱各挑一个球，使得挑出来的两个球颜色不同。只要知道每箱里球的数量，直接相乘就能得到挑法数，而不必把每个球都列出来。

#### 代码（Python）

```python
def countPairs(n: int, m: int) -> int:
    # 统计 1..n 中奇数、偶数的个数
    odd_n = (n + 1) // 2   # 奇数个数
    even_n = n // 2        # 偶数个数

    # 统计 1..m 中奇数、偶数的个数
    odd_m = (m + 1) // 2
    even_m = m // 2

    # 奇偶不同的配对 = (奇数 x 偶数) + (偶数 x 奇数)
    return odd_n * even_m + even_n * odd_m
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  - 只做了常数次的算术运算，和 `n、m` 的大小没有任何关系。相比暴力的 `O(n*m)`，这里的运行时间几乎是瞬间完成。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，同样是常数级别的内存。

---

## 心得  

- **核心技巧**：**利用整数除法快速统计区间内奇数/偶数的个数**，再用乘法组合计数。  
- **适用的题型**：  
  1. “在两个区间里选数，使得满足某种**属性不同**（奇偶、正负、模 k 等）” 的计数题。  
  2. “给定两个集合的大小，求满足**特定配对规则**的配对总数”。  
- **一句话总结解题钥匙**：**先把属性计数（奇数/偶数），再用乘法直接得到配对数**。

---

## 反思  

- **第一反应**：看到“不同奇偶”会立刻想到“枚举所有组合并判断”。  
- **最容易踩的坑**：  
  - 忘记把 `1` 也算进去（区间是闭区间 `[1, n]`、`[1, m]`）。  
  - 对奇数、偶数的计数公式写错，例如把 `odd = n // 2`（这只对偶数 `n` 正确）。  
- **下次遇到同类题的第一步**：**先把每个区间里满足单个属性的元素个数算出来**，再用组合公式（乘法原理）求答案。这样可以立刻把指数级的枚举压缩到常数时间。