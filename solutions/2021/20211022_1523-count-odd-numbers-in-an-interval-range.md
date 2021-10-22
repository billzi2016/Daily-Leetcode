# #1523. 区间范围内奇数的个数 / Count Odd Numbers in an Interval Range

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/count-odd-numbers-in-an-interval-range/)

---

## 题目（英文原版）

**Description**

Given two non-negative integers low and high. Return the count of odd numbers between low and high (inclusive).

**Examples**

**Example 1:**

```
Input: low = 3, high = 7
Output: 3
Explanation: The odd numbers between 3 and 7 are [3,5,7].
```

**Example 2:**

```
Input: low = 8, high = 10
Output: 1
Explanation: The odd numbers between 8 and 10 are [9].
```

**Constraints**

- 0 <= low <= high <= 10^9

---

## 题目（中文翻译）

**描述**  
给定两个非负整数 `low` 和 `high`。返回 `low` 与 `high`（含）之间奇数（odd number）的个数。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1:**  
```
Input: low = 3, high = 7
Output: 3
Explanation: The odd numbers between 3 and 7 are [3,5,7].
```

**示例 2:**  
```
Input: low = 8, high = 10
Output: 1
Explanation: The odd numbers between 8 and 10 are [9].
```

**约束条件**  
- `0 <= low <= high <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 **low 到 high** 之间的每一个整数都遍历一遍，判断它是奇数还是偶数，奇数就计数。  
- 用到的数据结构：**循环 + 计数器**。可以把计数器想象成一个装有“计数珠”的盒子，每遇到一个奇数，就往盒子里再放一颗珠子。  
- 为什么正确：只要把区间内的所有数都检查一遍，肯定不会漏掉任何奇数，也不会把偶数算进去。  

#### 代码（Python）  

```python
def countOdds_bruteforce(low: int, high: int) -> int:
    """
    暴力遍历 low~high，每遇到奇数计数一次
    """
    cnt = 0                     # 计数器，初始为 0
    for num in range(low, high + 1):   # 包含 high，使用 range 左闭右开，需要 +1
        if num % 2 == 1:        # 判断奇数：余数为 1
            cnt += 1            # 碰到奇数，计数器加 1
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = high - low + 1`，意思是「随区间长度线性增长」，区间越大，跑的时间就越长。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（计数器 `cnt`），不随输入规模增长。  



---  

### 2. 最优解  

#### 思路  

从暴力解来看，**瓶颈** 在于我们把每个数都遍历了一遍。实际上，只要知道区间的长度和区间两端的奇偶性，就能直接算出奇数的个数，而不必逐个检查。  

观察规律：  

1. **区间长度是偶数**  
   - 例如 `[3, 8]`，长度 `8-3+1 = 6`（偶数）。  
   - 偶数长度的区间里，奇数和偶数必然各占一半。  
   - 所以奇数个数 = 长度 / 2。  

2. **区间长度是奇数**  
   - 例如 `[3, 7]`，长度 `7-3+1 = 5`（奇数）。  
   - 此时奇数的个数取决于区间两端的奇偶性：  
     - 若 **low** 与 **high** 同为奇数，则奇数会比偶数多 1。  
     - 若两端中只有一个是奇数（另一个是偶数），奇数与偶数数量相等。  
   - 简单写成：`odd = length // 2 + (low % 2 == 1 or high % 2 == 1)`。  
   - 这里 `low % 2 == 1` 判断 low 是否为奇数，`or` 表示只要有一个奇数就多加 1。  

把两种情况合并，用整数除法 `//`（向下取整）即可得到 **O(1)** 的公式：  

```
total = high - low + 1                # 区间长度
odd = total // 2                      # 先算出“最少的奇数数目”
if total % 2 == 1:                    # 如果长度是奇数
    odd += 1 if low % 2 == 1 else 0   # 只在 low 为奇数时再加 1
```

也可以写得更简洁：  

```
odd = (high + 1) // 2 - low // 2
```

解释：`(high + 1) // 2` 表示 **0~high** 之间奇数的个数，`low // 2` 表示 **0~low-1** 之间奇数的个数，两者相减即得到 **low~high** 之间的奇数个数。  

#### 代码（Python）  

```python
def countOdds_optimal(low: int, high: int) -> int:
    """
    O(1) 公式求解：区间内奇数的个数 = (high + 1)//2 - low//2
    """
    # (high + 1)//2 统计 0~high 之间奇数的数量
    # low//2       统计 0~low-1 之间奇数的数量
    return (high + 1) // 2 - low // 2
```

#### 复杂度  

- **时间复杂度**：`O(1)`，只做了几次算术运算，和输入规模无关。  
- **空间复杂度**：`O(1)`，只用了常数个变量。  

相比暴力解，时间几乎瞬间完成，即使 `high` 达到 `10^9` 也毫无压力。  



## 心得  

- **核心技巧**：利用「前缀计数」的思想，把「区间统计」转化为「两个前缀的差」。  
- **适用的题型**：  
  1. 统计区间内偶数/奇数个数（本题）。  
  2. 统计区间内满足某种取模条件的数目（如能被 3 整除的个数）。  
  3. 统计区间内满足不等式的整数个数（如 `a <= x <= b` 且 `x` 为平方数）。  
- **解题钥匙**：**先把大区间拆成两个小的「从 0 开始」的区间，再用差值抵消重叠部分**。  

## 反思  

- **第一反应**：直接写循环遍历，想到「遍历」这个最自然的办法。  
- **最容易踩的坑**：  
  - 忘记 `range` 是左闭右开，需要 `high + 1` 才能把 `high` 包括进去。  
  - 在使用公式 `(high + 1)//2 - low//2` 时，如果把 `low` 当成闭区间端点直接除以 2，会少算一个奇数。  
  - 边界值 `low = 0`、`high = 0` 或者 `low = high` 时，仍要保证公式成立。  
- **下次遇到同类题**：第一步先思考「能不能把区间统计转化为前缀计数的差」——如果可以，就直接写 O(1) 公式；如果不行，再考虑双指针或循环。