# #2578. 最小和拆分 / Split With Minimum Sum

> 难度：简单 · 标签：Math、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/split-with-minimum-sum/)

---

## 题目（英文原版）

**Description**

Given a positive integer num, split it into two non-negative integers num1 and num2 such that:
Return the minimum possible sum of num1 and num2.
Notes:

**Examples**

**Example 1:**

```
Input: num = 4325
Output: 59
Explanation: We can split 4325 so that num1 is 24 and num2 is 35, giving a sum of 59. We can prove that 59 is indeed the minimal possible sum.
```

**Example 2:**

```
Input: num = 687
Output: 75
Explanation: We can split 687 so that num1 is 68 and num2 is 7, which would give an optimal sum of 75.
```

**Constraints**

- 10 <= num <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个正整数（positive integer）`num`，将其拆分为两个非负整数（non‑negative integer）`num1` 和 `num2`，满足：  
返回 `num1` 与 `num2` 的最小可能和（sum）。

**示例**  

**示例 1**  
输入: `num = 4325`  
输出: `59`  
解释: 我们可以将 4325 拆分，使得 `num1` 为 24，`num2` 为 35，得到的和为 59。可以证明 59 确实是最小的可能和。

**示例 2**  
输入: `num = 687`  
输出: `75`  
解释: 我们可以将 687 拆分，使得 `num1` 为 68，`num2` 为 7，得到的最优和为 75。

**约束条件**  
- `10 <= num <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把所有数字的每一种可能的分配方式都尝试一遍**，然后把得到的两个整数相加，取最小的和。  

- **数据结构**：  
  - 把整数 `num` 拆成一个字符数组（相当于把数字拆成一堆“砖块”），例如 `4325 → ['4','3','2','5']`。  
  - 用 **集合 / 子集** 来决定每块砖放进哪个箱子（`num1` 还是 `num2`），这可以用二进制掩码或 `itertools.combinations` 来实现。  
  - 对于每个箱子内部的砖块，需要把它们排成一个具体的顺序，这相当于**全排列**，可以用 `itertools.permutations`（把砖块排成一行，就像排队买票）。  

- **为什么正确**：  
  - 我们把**所有**可能的分配和排列都枚举了，必然会覆盖最优的那一种。只要在遍历过程中记录最小的 `num1 + num2`，最终得到的就是答案。  

- **时间/空间复杂度**（大白话）  
  - 假设 `n` 是 `num` 的位数（最多 10 位）。  
  - 对每一种把位划分到两个箱子的方式，有 `2^n` 种（每位可以去左边或右边）。  
  - 对每个箱子内部，需要把选中的位全排列，最坏情况下是 `n!` 种。  
  - 因此时间复杂度是 **指数级**：`O(2^n * n!)`，对 10 位数已经是几万甚至上百万次运算，远远超出“一秒能跑完”的要求。  
  - 空间上只需要存放当前的排列和几个临时变量，属于 **O(n)**，即几乎不占内存。  

#### 代码（Python）  

```python
import itertools

def split_min_sum_bruteforce(num: int) -> int:
    # 把整数拆成字符列表，方便后面取每一位
    digits = list(str(num))                 # 例如 4325 -> ['4','3','2','5']
    n = len(digits)

    best = float('inf')                     # 用来记录最小的和

    # 用二进制掩码遍历所有把每一位放进 num1(0) 还是 num2(1) 的方式
    for mask in range(1 << n):              # 0 ~ 2^n-1
        group1 = []                          # 放进 num1 的位
        group2 = []                          # 放进 num2 的位
        for i in range(n):
            if mask & (1 << i):              # 第 i 位放进 group2
                group2.append(digits[i])
            else:                            # 第 i 位放进 group1
                group1.append(digits[i])

        # 如果某一组为空，也算合法（题目允许非负整数）
        # 对每组分别枚举所有排列，计算对应的整数
        for perm1 in itertools.permutations(group1):
            num1 = int(''.join(perm1)) if perm1 else 0
            for perm2 in itertools.permutations(group2):
                num2 = int(''.join(perm2)) if perm2 else 0
                best = min(best, num1 + num2)   # 维护最小和

    return best
```

> 这段代码可以直接跑通，但仅适合位数非常少的测试（比如 4 位以内），否则会超时。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n!)`  
  - `2^n` 表示所有可能的“左/右”分配，`n!` 表示每组内部的全排列。对 10 位数来说大约是 10!·2^10 ≈ 3.7×10^9 次，显然不可接受。  
- **空间复杂度**：`O(n)`  
  - 只需要存放当前的位列表、两组临时数组以及少量临时变量，随 `n` 线性增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到**瓶颈在于枚举所有排列**。其实我们并不需要考虑所有顺序，只要让两个数的最高位尽可能小、位数尽可能均衡，就能得到最小的和。  

1. **把所有数字从小到大排好序**（像把字典里的词按字母顺序排好，最前面的就是最小的词）。  
2. **交叉分配**：把排好序的数字依次交替放进 `num1` 和 `num2`。  
   - 第 1、3、5… 位放进 `num1`，第 2、4、6… 位放进 `num2`。  
   - 这样做的直观解释：  
     - 先把最小的数字放进 `num1`，再把第二小的放进 `num2`，保证两边的首位都是尽可能小的。  
     - 接下来再把第三小的放进 `num1`（它会成为 `num1` 的第二位），这样两数的位数差不会超过 1，避免出现一个数非常长、另一个数很短导致和变大。  
3. 最后把两个数字从字符列表拼成整数即可。  

**为什么这样是最优的？**  

- **位数均衡**：如果两数的位数相差超过 1，必然会导致较长的那个数在高位有更大的十的幂次，从而使和增大。交叉分配天然保证位数差 ≤ 1。  
- **高位最小**：因为我们是从最小的数字开始分配的，两个数的最高位都是当前未使用的最小数字，任何其他分配方式都会让其中至少一个数的最高位更大，进而使总和变大。  
- 形式化证明可以用“交换论证”：若存在两位 `a<b`，且 `a` 放在较高位的 `num1`、`b` 放在较低位的 `num2`，交换这两位会让和更小。通过不断交换，最终会得到**升序交叉**的分配。  

#### 代码（Python）  

```python
def split_min_sum_greedy(num: int) -> int:
    # 1. 把整数的每一位取出来并排序，得到从小到大的字符列表
    digits = sorted(str(num))               # 例如 4325 -> ['2','3','4','5']

    # 2. 交叉放进两个列表，模拟构造两个数
    num1_digits, num2_digits = [], []
    for i, d in enumerate(digits):
        if i % 2 == 0:                       # 偶数下标放进 num1
            num1_digits.append(d)
        else:                                # 奇数下标放进 num2
            num2_digits.append(d)

    # 3. 把字符列表拼成整数（空列表视为 0）
    num1 = int(''.join(num1_digits)) if num1_digits else 0
    num2 = int(''.join(num2_digits)) if num2_digits else 0

    return num1 + num2
```

> 代码仅用了 `sorted`、列表拼接和一次遍历，运行速度在毫秒级。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `sorted` 对 `n` 位数字进行排序，需要 `n log n` 的时间。`n` 最多是 10，几乎可以视作常数。  
  - 之后的遍历和拼接都是线性 `O(n)`，不影响整体阶。相较于暴力的指数级，这已经是“瞬间完成”。  

- **空间复杂度**：`O(n)`  
  - 需要额外存放排好序的字符数组以及两个结果列表，都是与位数成正比的空间。  

---  

## 心得  

- **核心技巧**：**贪心 + 排序 + 交叉分配**，即把所有元素按从小到大的顺序排列后，交替放进两个容器，使得两边的“重量”（位数）尽可能均衡。  
- **适用的题型**：  
  1. 把数字拆成两个数，使和/差/乘积最小（如 LeetCode 2160 “Minimum Sum of Four Digit Number After Splitting Digits”）。  
  2. 把字符或数字分成两组，使两组的数值或长度尽量相近（如 “Rearrange Array Elements to Maximize Minimum Difference” 的思路）。  
- **一句话总结**：**把所有数字升序排列后交叉填入两数，既保证高位最小，又让位数均衡，从而得到最小和。**  

---  

## 反思  

- **第一反应**：看到“把整数拆成两部分求最小和”，第一时间会想到“遍历所有可能的切分”。这自然导向暴力搜索。  
- **最容易踩的坑**：  
  - 忘记对数字的每一位进行排序，直接按原顺序交叉会得到错误答案（例如 `num = 1002`）。  
  - 当位数为奇数时，需要让较长的那一边仍然保持最小的高位，否则会产生多余的十的幂次。  
  - 题目允许 `num1` 或 `num2` 为 0，注意空列表时要返回 0 而不是报错。  
- **下次类似题的第一步**：先**把原始元素排序**，思考**如何均匀地把最小的元素分配到不同的组**，通常交叉或轮流分配就是最直接的贪心策略。