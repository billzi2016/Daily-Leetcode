# #2160. 拆分四位数字后的最小和 / Minimum Sum of Four Digit Number After Splitting Digits

> 难度：简单 · 标签：Math、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/)

---

## 题目（英文原版）

**Description**

You are given a positive integer num consisting of exactly four digits. Split num into two new integers new1 and new2 by using the digits found in num. Leading zeros are allowed in new1 and new2, and all the digits found in num must be used.
Return the minimum possible sum of new1 and new2.

**Examples**

**Example 1:**

```
Input: num = 2932
Output: 52
Explanation: Some possible pairs [new1, new2] are [29, 23], [223, 9], etc.
The minimum sum can be obtained by the pair [29, 23]: 29 + 23 = 52.
```

**Example 2:**

```
Input: num = 4009
Output: 13
Explanation: Some possible pairs [new1, new2] are [0, 49], [490, 0], etc. 
The minimum sum can be obtained by the pair [4, 9]: 4 + 9 = 13.
```

**Constraints**

- 1000 <= num <= 9999

---

## 题目（中文翻译）

给定一个恰好由四位数组成的正整数 `num`。使用 `num` 中的数位，将其拆分为两个新整数 `new1` 和 `new2`。`new1`、`new2` 允许出现前导零（leading zeros），且必须使用 `num` 中的全部数位。返回 `new1` 与 `new2` 的最小可能的和。

**示例 1**  
**输入:** `num = 2932`  
**输出:** `52`  
**解释:** 一些可能的配对 `[new1, new2]` 包括 `[29, 23]`、`[223, 9]` 等。最小的和可以由配对 `[29, 23]` 得到：`29 + 23 = 52`。

**示例 2**  
**输入:** `num = 4009`  
**输出:** `13`  
**解释:** 一些可能的配对 `[new1, new2]` 包括 `[0, 49]`、`[490, 0]` 等。最小的和可以由配对 `[4, 9]` 得到：`4 + 9 = 13`。

**约束条件**  
- `1000 <= num <= 9999`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目要求把四位整数的四个数字重新组合成 **两个整数** `new1`、`new2`（可以有前导零），使 `new1 + new2` 最小。  
最直接的想法是**把所有可能的拆分方式都枚举一遍**，算出它们的和，取最小值。

- **数据结构**：我们可以把四个数字放进一个列表 `digits`，再用 **全排列**（Permutation）得到这四个数字的所有排列顺序。全排列就像把四张不同颜色的卡片全部排成一行，所有可能的排法都列出来。  
- 对每一种排列 `[a, b, c, d]`，我们可以把前两位当作 `new1`，后两位当作 `new2`（也可以把它们交叉组合，只要遍历所有分配方式即可）。因为题目只要求 **使用全部数字**，不要求每个数的位数相同，枚举所有分配即可覆盖所有情况。  

**为什么正确**：只要遍历了 **所有合法的拆分**，其中必然会包含最优解，取最小值自然得到答案。

#### 代码（Python）  

```python
import itertools

def minimumSum_bruteforce(num: int) -> int:
    # 把四位整数拆成单个字符，再转成 int，得到数字列表
    digits = [int(ch) for ch in str(num)]          # 例: 2932 -> [2,9,3,2]

    best = float('inf')                            # 用一个很大的数保存当前最小和

    # 对四个数字的所有排列进行遍历（全排列）
    for perm in itertools.permutations(digits):
        # 这里我们把前两位组成 new1，后两位组成 new2
        # 例如 perm = (2,9,3,2) -> new1 = 29, new2 = 32
        new1 = perm[0] * 10 + perm[1]              # 十位 * 10 + 个位
        new2 = perm[2] * 10 + perm[3]
        cur_sum = new1 + new2
        # 更新最小值
        if cur_sum < best:
            best = cur_sum

    return best
```

#### 复杂度  
- **时间复杂度**：`O(4! ) = O(24)`，因为只有 4 个数字，排列数固定为 24，常数级别的时间。可以把它想象成**只需要检查 24 种可能**，几乎瞬间完成。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（列表、临时整数），不随输入规模增长。

---

### 2. 最优解  

#### 思路  
暴力解已经够快（只要 24 种组合），但我们可以用 **数学上的贪心** 思想直接得到最小和，省去枚举。

**观察 1**：  
把四个数字分别记为 `a ≤ b ≤ c ≤ d`（从小到大排序）。  
若我们把 `a`、`b` 放在十位，`c`、`d` 放在个位，得到的两个数是  

```
new1 = 10 * a + c
new2 = 10 * b + d
sum  = (10*a + c) + (10*b + d) = 10*(a+b) + (c+d)
```

**观察 2**：  
十位的权值是 10，远大于个位的权值 1。要让总和最小，**十位上应该放最小的数字**，而个位上放稍大的数字即可。  

**推导**：  
- 把最小的两个数字分别放到十位（各自成为一个两位数的十位），这能让十位的贡献尽可能小。  
- 剩下的两个数字自然放到个位。  

这样得到的和正是上式 `10*(a+b) + (c+d)`，已经是全局最小。  

**为什么不会出现更小的组合**：  
假设我们把某个更大的数字 `x` 放到十位，而把更小的数字 `y` 放到个位（`x > y`）。则十位的贡献会多 `10*(x-y)`，而个位只会少 `(x-y)`，整体多 `9*(x-y) > 0`，显然更大。因此把最小的两个数字放十位是唯一的最优策略。  

#### 代码（Python）  

```python
def minimumSum(num: int) -> int:
    # 把四位整数拆成单个字符，再转成 int，得到数字列表
    digits = [int(ch) for ch in str(num)]          # 例: 4009 -> [4,0,0,9]

    # 将四个数字从小到大排序
    digits.sort()                                   # 现在 digits = [0,0,4,9]

    # 取最小的两个作为十位，剩下的两个作为个位
    a, b, c, d = digits                             # a≤b≤c≤d

    # 组成两个两位数
    new1 = a * 10 + c
    new2 = b * 10 + d

    return new1 + new2
```

#### 复杂度  
- **时间复杂度**：`O(1)`（常数时间）。排序四个元素的时间可以视作常数，因为元素数量固定。  
- **空间复杂度**：`O(1)`，只用了几个整数变量。

> 与暴力解相比，最优解省去了枚举的步骤，思路更直接，也更符合面试中展示**贪心思考**的要求。

---

## 心得  

- **核心技巧**：**贪心 + 位权比较**。先把位值大的位置（十位）分配最小的数字，再把剩余的放在位值小的位置。  
- **适用的题型**：  
  1. 需要把若干数字重新组合成若干整数，使和或差最小/最大（如 LeetCode 2160 “Minimum Sum of Four Digit Number After Splitting Digits”）。  
  2. 把数字分配到不同位数的“最小/最大数”类问题（如把数字排成最小数/最大数）。  
  3. 需要利用位权大小进行贪心选择的组合优化题。  
- **解题钥匙**：**先比较位权的大小，再把最小的数字放到位权最大的位上**。

---

## 反思  

- **第一反应**：看到“把四位数拆成两个数求最小和”，本能想到**全排列枚举**，因为最安全、最直接。  
- **最容易踩的坑**：  
  - 忽略**前导零**的合法性，误以为每个数必须是两位数，从而错过更小的组合。  
  - 没有注意到十位的权值是个位的 10 倍，导致贪心思路不成立。  
- **下次遇到类似题**：第一步先**思考位权的影响**，判断是否可以用“把最小数字放在最高位”这种贪心策略直接得到答案，再决定是否需要枚举或动态规划。