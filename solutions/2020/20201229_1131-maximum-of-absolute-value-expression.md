# #1131. 绝对值表达式的最大值 / Maximum of Absolute Value Expression

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/maximum-of-absolute-value-expression/)

---

## 题目（英文原版）

**Description**

Given two arrays of integers with equal lengths, return the maximum value of:
|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|
where the maximum is taken over all 0 <= i, j < arr1.length.

**Examples**

**Example 1:**

```
Input: arr1 = [1,2,3,4], arr2 = [-1,4,5,6]
Output: 13
```

**Example 2:**

```
Input: arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]
Output: 20
```

**Constraints**

- 2 <= arr1.length == arr2.length <= 40000
- -10^6 <= arr1[i], arr2[i] <= 10^6

---

## 题目（中文翻译）

给定两个长度相等的整数数组 `arr1` 和 `arr2`，返回下式的最大值：

\[
|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|
\]

其中最大值在所有满足 `0 <= i, j < arr1.length` 的下标对 `(i, j)` 中取得。

---

### 示例 1  
### 示例 2  

---

### 约束条件
- `2 <= arr1.length == arr2.length <= 40000`
- `-10^6 <= arr1[i], arr2[i] <= 10^6`

---

### 示例

**示例 1**  
输入: `arr1 = [1,2,3,4], arr2 = [-1,4,5,6]`  
输出: `13`

**示例 2**  
输入: `arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]`  
输出: `20`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把所有可能的 i、j 都枚举一遍**，直接套公式算出  

\[
|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|
\]

然后取最大值。  

- **用到的数据结构**：两个普通的 Python 列表（`list`），相当于我们生活中排好顺序的数字牌。  
- **为什么一定对**：因为题目要求的是「所有 i、j 的最大值」，只要把所有组合都算一遍，必然不会漏掉最优解。  
- **复杂度大概是怎样的**：设数组长度为 `n`，我们需要两层循环，外层 `n` 次，内层也最多 `n` 次，所以总共要算 `n × n = n²` 次。  
  - `O(n²)` 里的 **O** 代表“数量级”，`n²` 表示如果 `n` 翻倍，运算次数会变成原来的 **四倍**（因为平方的关系）。  
  - 空间上我们只用到了常数个额外变量（最大值、当前值），所以是 **O(1)**，即“几乎不占额外空间”。  

#### 代码（Python）  

```python
from typing import List

def maxAbsValExpr_bruteforce(arr1: List[int], arr2: List[int]) -> int:
    n = len(arr1)
    ans = 0                       # 用来保存目前找到的最大值
    # 枚举所有 i
    for i in range(n):
        # 枚举所有 j（包括 i 本身，公式在 i=j 时为 0，不影响最大值）
        for j in range(n):
            # 计算当前 i、j 对应的表达式值
            cur = (abs(arr1[i] - arr1[j])   # 第一个绝对值
                   + abs(arr2[i] - arr2[j]) # 第二个绝对值
                   + abs(i - j))            # 第三个绝对值
            # 如果比当前最大值更大，就更新 ans
            if cur > ans:
                ans = cur
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 需要两层循环，`n` 可能高达 4 万，`n²` 会达到 1.6 × 10⁹，计算量太大，实际会超时。  
- **空间复杂度**：`O(1)` —— 只用了几个整型变量，不随 `n` 增长而增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于两层循环**，我们必须把 “比较所有 i、j 的差值” 这一步 **压缩到一次遍历**。  

**关键观察**：  
\[
|x| + |y| + |z| = \max_{\pm}\;(\pm x \pm y \pm z)
\]  

也就是说，绝对值的和等价于在 **8 种符号组合** 中挑最大的那一个。  
把题目中的  

\[
x = arr1[i] - arr1[j],\quad
y = arr2[i] - arr2[j],\quad
z = i - j
\]

代进去，就得到  

\[
\pm (arr1[i]-arr1[j]) \; \pm (arr2[i]-arr2[j]) \; \pm (i-j)
\]

把符号分配到每个 **i** 上，可以写成  

\[
\bigl(s_1\*arr1[i] + s_2\*arr2[i] + s_3\*i\bigr) \;-\;
\bigl(s_1\*arr1[j] + s_2\*arr2[j] + s_3\*j\bigr)
\]

其中 `s1、s2、s3` 每个只能是 `+1` 或 `-1`。  
对固定的 `(s1,s2,s3)`，上式只等于 “某个数组 `val[i]` 的最大值减去最小值”。  
所以 **只要遍历所有符号组合，记录对应的 `val[i]` 的最大/最小**，就能在 **一次遍历** 内求出答案。

**为什么只需要 4 种组合而不是 8 种？**  
把所有符号同时取反 `(s1,s2,s3) → (-s1,-s2,-s3)` 会得到相同的差值（因为 `max-min` 不变），因此只保留一半即可。  
常见的四种组合是：

| 组合 | 对应的 `val[i]` 表达式 |
|------|------------------------|
| (+,+,+) | `arr1[i] + arr2[i] + i` |
| (+,+,-) | `arr1[i] + arr2[i] - i` |
| (+,-,+) | `arr1[i] - arr2[i] + i` |
| (+,-,-) | `arr1[i] - arr2[i] - i` |

**步骤**  

1. 初始化四个 `max` 为 `-inf`，四个 `min` 为 `+inf`。  
2. 一次遍历数组下标 `i`（从 0 到 n‑1），计算上述四个 `val`。  
3. 同时更新对应的 `max`、`min`。  
4. 最后答案是四个 `(max - min)` 中的最大值。  

这样时间只是 **O(n)**，空间只需要常数级别的变量 **O(1)**，完全可以通过所有测试。

#### 代码（Python）  

```python
from typing import List

def maxAbsValExpr_opt(arr1: List[int], arr2: List[int]) -> int:
    # 四种线性组合的当前最大值、最小值
    max1 = max2 = max3 = max4 = -10**18   # 足够小的初始值
    min1 = min2 = min3 = min4 = 10**18    # 足够大的初始值

    for i, (a, b) in enumerate(zip(arr1, arr2)):
        # 计算四个表达式的值
        v1 = a + b + i      # (+,+,+)
        v2 = a + b - i      # (+,+,-)
        v3 = a - b + i      # (+,-,+)
        v4 = a - b - i      # (+,-,-)

        # 更新最大/最小
        if v1 > max1: max1 = v1
        if v1 < min1: min1 = v1

        if v2 > max2: max2 = v2
        if v2 < min2: min2 = v2

        if v3 > max3: max3 = v3
        if v3 < min3: min3 = v3

        if v4 > max4: max4 = v4
        if v4 < min4: min4 = v4

    # 四种组合对应的差值
    diff1 = max1 - min1
    diff2 = max2 - min2
    diff3 = max3 - min3
    diff4 = max4 - min4

    # 取最大值即为答案
    return max(diff1, diff2, diff3, diff4)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 最大 4 万，轻松通过。  
- **空间复杂度**：`O(1)` —— 只用了若干整型变量，和 `n` 无关。  

---  

## 心得  

- **核心技巧**：把 **绝对值的和** 转化为 **符号枚举**，再利用 “最大值减最小值” 的思想一次遍历求解。  
- **适用的题型**：  
  1. 同时出现多个绝对值的表达式（如 `|A[i]-A[j]| + |B[i]-B[j]|`）。  
  2. 需要求 “两点之间的曼哈顿距离最大值” 之类的几何/坐标问题。  
- **一句话总结解题钥匙**：**把每个绝对值拆成正负两种可能，用线性组合把原式化为“某个数的最大值减最小值”。**  

## 反思  

- **第一反应**：直接写两层循环，算出所有组合的值。  
- **最容易踩的坑**：  
  - 忘记考虑 `i=j` 的情况（虽然值为 0，不影响最大值，但代码里要避免除零错误等）。  
  - 符号组合写错导致得到的 `val[i]` 与公式不匹配。  
  - 使用 Python 的 `int` 时不必担心溢出，但在其他语言要注意范围。  
- **下次遇到同类题**：第一步先**把所有绝对值拆成 ± 的形式**，看能否写成 “`某个线性表达式的最大值 - 最小值`”，如果可以，就立刻转向一次遍历的 O(n) 思路。