# #3492. 船舶上可装载的最大集装箱数量 / Maximum Containers on a Ship

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/maximum-containers-on-a-ship/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n representing an n x n cargo deck on a ship. Each cell on the deck can hold one container with a weight of exactly w.
However, the total weight of all containers, if loaded onto the deck, must not exceed the ship's maximum weight capacity, maxWeight.
Return the maximum number of containers that can be loaded onto the ship.

**Examples**

**Example 1:**

```
Input: n = 2, w = 3, maxWeight = 15
Output: 4
Explanation:
The deck has 4 cells, and each container weighs 3. The total weight of loading all containers is 12, which does not exceed maxWeight .
```

**Example 2:**

```
Input: n = 3, w = 5, maxWeight = 20
Output: 4
Explanation:
The deck has 9 cells, and each container weighs 5. The maximum number of containers that can be loaded without exceeding maxWeight is 4.
```

**Constraints**

- 1 <= n <= 1000
- 1 <= w <= 1000
- 1 <= maxWeight <= 109

---

## 题目（中文翻译）

**描述**  
给定一个正整数 `n`，表示船上一个 `n × n` 的货舱（cargo deck）。货舱的每个格子只能放置一个重量恰好为 `w` 的集装箱（container）。然而，所有装载的集装箱的总重量不能超过船的最大承载重量 `maxWeight`。返回可以装载的最大集装箱数量。

**示例 1**  
**输入**: `n = 2, w = 3, maxWeight = 15`  
**输出**: `4`  
**解释**:  
货舱共有 4 个格子，每个集装箱重量为 3。装满所有格子时的总重量为 `12`，未超过 `maxWeight`。

**示例 2**  
**输入**: `n = 3, w = 5, maxWeight = 20`  
**输出**: `4`  
**解释**:  
货舱共有 9 个格子，每个集装箱重量为 5。为了不超过 `maxWeight`，最多只能装载 4 个集装箱。

**约束条件**  
- `1 ≤ n ≤ 1000`  
- `1 ≤ w ≤ 1000`  
- `1 ≤ maxWeight ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把甲板的每个格子都当成一个“座位”，依次把集装箱放进去，累计已经放了多少重量，只要总重量不超过 `maxWeight` 就继续放，超过了就停下来。  

- **用到的数据结构**：只需要一个整数变量 `cnt` 记录已经放了多少个集装箱，和一个整数变量 `total` 记录当前累计的重量。可以把它想象成在超市排队结账时，手里只拿着两张纸——一张记“已经买了几件”，另一张记“已经花了多少钱”。  
- **为什么正确**：因为我们是逐格检查，所有可能的格子都会被考虑到，只有当再放一个集装箱会导致总重量超过上限时才停止，所以得到的 `cnt` 必然是“最多能放的”数量。  

#### 代码（Python）

```python
def maxContainers_bruteforce(n: int, w: int, maxWeight: int) -> int:
    # 甲板一共有 n*n 格子
    total_cells = n * n

    cnt = 0          # 已经放了多少个集装箱
    total = 0        # 当前累计的总重量

    # 按顺序遍历每一个格子
    for _ in range(total_cells):
        # 如果再放一个集装箱会超过最大承重，就停止
        if total + w > maxWeight:
            break
        cnt += 1          # 放下一个集装箱
        total += w        # 累计重量

    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：甲板有 `n*n` 个格子，我们最多会遍历一次每个格子。比如 `n = 1000` 时，需要检查 1,000,000 次，算起来就是“平方级别”的工作量。  
- **空间复杂度**：`O(1)`  
  解释：只用了几个整数变量，和 `n` 的大小无关，算是“常数级别”的内存消耗。

---

### 2. 最优解

#### 思路  
从暴力解可以看出，真正的瓶颈在于我们**逐格遍历**，但其实不需要真的去遍历每个格子，因为每个格子的重量都是相同的 `w`，我们只要算出**最多能放多少个**就行。

1. 甲板最多能放的容器数量是 `n * n`（把每个格子都塞满）。  
2. 受重量限制，最多能放的容器数量是 `maxWeight // w`（整数除法得到在不超重的前提下最多能装多少个）。  
3. 两个限制同时作用，最终能放的数量就是二者的**最小值**：  

\[
\text{answer} = \min\bigl(n \times n,\; \bigl\lfloor\frac{\text{maxWeight}}{w}\bigr\rfloor\bigr)
\]

这一步只用了几次算术运算，时间复杂度是 **O(1)**，即常数时间。

#### 代码（Python）

```python
def maxContainers(n: int, w: int, maxWeight: int) -> int:
    """
    返回在不超过 maxWeight 的前提下，最多能放多少个集装箱。
    思路：取甲板格子数和重量限制下能放的数量的最小值。
    """
    # 甲板总格子数
    total_cells = n * n          # n 的平方，表示最多可以放多少个

    # 根据重量限制，最多能放的数量（整数除法，直接向下取整）
    max_by_weight = maxWeight // w

    # 两个上限取最小值，就是答案
    return min(total_cells, max_by_weight)
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  解释：只做了几次加减乘除和一次 `min`，不随 `n` 大小变化，算是“一瞬间就算完”。  
- **空间复杂度**：`O(1)`  
  解释：同样只用了常数个变量，和输入规模无关。

---

## 心得

- **核心技巧**：把约束条件转化为**取最小值**的问题。先算出每个约束下的上限，再取最小值即可。
- **适用的题型**：  
  1. “在预算/容量限制下，最多能买/装多少件商品”  
  2. “在时间/步数限制下，最多能完成多少次操作”  
  3. “在空间限制下，最多能放置多少元素”  
- **一句话总结**：**先算每个独立限制的上限，再取最小值**，往往能把遍历式的暴力解压缩到常数时间。

---

## 反思

- **第一反应**：看到“每个格子都能放一个重量相同的集装箱”，自然想到“把格子一个一个遍历”。  
- **最容易踩的坑**：  
  - 忘记对 `maxWeight` 进行整数除法，导致出现小数或浮点数错误。  
  - 忽略了 `n*n` 可能非常大（`n` 最大 1000 时是 1,000,000），如果直接用 `for i in range(n*n)`，在更大的约束下会超时。  
- **下次思路**：面对“数量 × 单位重量 ≤ 上限”这类线性约束时，第一步就考虑 **“上限除以单价”**，再与实际容量（格子数、库存等）取最小值。这样常常能直接得到 O(1) 的最优解。