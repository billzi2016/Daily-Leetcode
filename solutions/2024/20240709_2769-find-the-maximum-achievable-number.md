# #2769. **找到可达的最大数字** / Find the Maximum Achievable Number

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-achievable-number/)

---

## 题目（英文原版）

**Description**

Given two integers, num and t. A number x is achievable if it can become equal to num after applying the following operation at most t times:
Return the maximum possible value of x.

**Examples**

**Example 1:**

```
Input: num = 4, t = 1
Output: 6
Explanation:
Apply the following operation once to make the maximum achievable number equal to num :
```

**Example 2:**

```
Input: num = 3, t = 2
Output: 7
Explanation:
Apply the following operation twice to make the maximum achievable number equal to num :
```

**Constraints**

- 1 <= num, t <= 50

---

## 题目（中文翻译）

给定两个整数 `num` 和 `t`。如果一个数字 `x` 能在至多 `t` 次以下操作后变为 `num`，则称 `x` 为 *可达的*。  
返回所有可达的数字中可能的最大值。

**示例 1**

```text
Input: num = 4, t = 1
Output: 6
Explanation:
对一次操作后，使得最大的可达数字等于 num：
```

**示例 2**

```text
Input: num = 3, t = 2
Output: 7
Explanation:
对两次操作后，使得最大的可达数字等于 num：
```

**约束条件**

- `1 <= num, t <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给了两个整数 `num` 和 `t`，我们要找一个整数 `x`，使得 **最多** 进行 `t` 次下面的操作后，`x` 能和 `num` 相等。

> **操作**：一次操作把 `x` 减 1、把 `num` 加 1。  
> 想象成把 1 块糖从 `x` 那里“转移”到 `num` 那里，糖的总数不变，只是从左边搬到右边。

所以如果我们用了 `k` 次操作（`0 ≤ k ≤ t`）：

```
x  ->  x - k
num -> num + k
```

要让两者相等，只需要 `x - k == num + k`，也就是  

```
x - num = 2 * k
```

因为 `k` 只能是整数，`x` 必须满足 `x = num + 2*k`，并且 `k ≤ t`。  
暴力的做法就是遍历所有可能的 `k`（0…t），把对应的 `x` 记下来，取最大的那个。

> **为什么正确**：我们把所有合法的「转移次数」都枚举了一遍，找到了所有可以让 `x` 与 `num` 在 `t` 步内相等的 `x`，最大值自然就是答案。

#### 代码（Python）

```python
def maximum_achievable(num: int, t: int) -> int:
    # max_x 用来保存最大的可行 x，初始设为最小可能值
    max_x = num          # 至少可以取 num 本身（k = 0）
    for k in range(1, t + 1):          # 枚举使用的操作次数 1~t
        x = num + 2 * k                # 根据等式 x = num + 2*k 计算对应的 x
        max_x = max(max_x, x)          # 取最大值
    return max_x
```

- 第 3 行：`max_x` 先设为 `num`，因为不操作时 `x = num` 也是合法的。  
- 第 4‑5 行：遍历所有可能的操作次数 `k`。  
- 第 6 行：根据推导的公式直接算出对应的 `x`。  
- 第 7 行：更新答案为最大的 `x`。  

#### 复杂度

- **时间复杂度**：`O(t)`。我们只循环了 `t` 次，`t` 最多 50，几乎可以忽略不计。  
- **空间复杂度**：`O(1)`。只用了常数个变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，答案总是形如 `num + 2*k`，而 `k` 的上限是 `t`。  
于是我们只需要让 `k` 取到最大的可能值 `t`，就能直接得到最大 `x`：

```
x_max = num + 2 * t
```

这一步不需要循环，直接算式即可。

> **瓶颈在哪里**：暴力解里我们遍历 `k = 1…t`，虽然 `t` 很小，但在算法思考中我们总是想把「遍历」去掉，得到 **常数时间** 的解法。  
> **核心技巧**：把「每次操作把 1 从 x 移到 num」转化为等式 `x - num = 2*k`，再把 `k` 取最大值 `t`。

#### 代码（Python）

```python
def maximum_achievable(num: int, t: int) -> int:
    """
    直接使用公式：最大可达数 = num + 2 * t
    """
    return num + 2 * t
```

- 第 4 行：一行代码完成全部计算，既简洁又高效。

#### 复杂度

- **时间复杂度**：`O(1)`——只做一次加法和一次乘法，和 `t` 大小无关。  
- **空间复杂度**：`O(1)`——只使用了常数级别的变量。

---

## 心得

- **核心技巧**：把“每次把 1 从 x 移到 num”抽象为等式 `x - num = 2*k`，利用等差关系直接求最大值。  
- **适用题型**：  
  1. 需要在固定次数的“转移”或“加减”操作后，使两个数相等的题目。  
  2. 只涉及线性关系（如 `a + b = const`）且操作次数受限的数学题。  
- **一句话总结**：**把操作转化为等式，令次数取上界，公式直接给出答案。**

---

## 反思

- **第一反应**：看到“最多 t 次操作”会先想到枚举次数 `k`，写个循环。  
- **最容易踩的坑**：忘记 `x` 必须 **不小于** `num`（因为只能把 `x` 减），或者把等式写成 `x + num = 2*k`，导致答案错误。  
- **下次思路**：遇到“把值从一个变量转移到另一个变量”这种描述时，马上写出 **守恒量**（总和不变）和 **转移次数** 的等式，看看能否直接求解。