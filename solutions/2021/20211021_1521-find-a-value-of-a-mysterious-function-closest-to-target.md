# #1521. 寻找神秘函数值最接近目标的值 / Find a Value of a Mysterious Function Closest to Target

> 难度：困难 · 标签：Array、Binary Search、Bit Manipulation、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/)

---

## 题目（英文原版）

**Description**

Winston was given the above mysterious function func. He has an integer array arr and an integer target and he wants to find the values l and r that make the value |func(arr, l, r) - target| minimum possible.
Return the minimum possible value of |func(arr, l, r) - target|.
Notice that func should be called with the values l and r where 0 <= l, r < arr.length.

**Examples**

**Example 1:**

```
Input: arr = [9,12,3,7,15], target = 5
Output: 2
Explanation: Calling func with all the pairs of [l,r] = [[0,0],[1,1],[2,2],[3,3],[4,4],[0,1],[1,2],[2,3],[3,4],[0,2],[1,3],[2,4],[0,3],[1,4],[0,4]], Winston got the following results [9,12,3,7,15,8,0,3,7,0,0,3,0,0,0]. The value closest to 5 is 7 and 3, thus the minimum difference is 2.
```

**Example 2:**

```
Input: arr = [1000000,1000000,1000000], target = 1
Output: 999999
Explanation: Winston called the func with all possible values of [l,r] and he always got 1000000, thus the min difference is 999999.
```

**Example 3:**

```
Input: arr = [1,2,4,8,16], target = 0
Output: 0
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i] <= 106
- 0 <= target <= 107

---

## 题目（中文翻译）

**描述**  
Winston 获得了如上所示的神秘函数 `func`。给定整数数组 `arr` 和整数 `target`，他希望找到下标 `l` 与 `r`（满足 `0 ≤ l, r < arr.length`），使得  

\[
|\,\text{func}(arr, l, r) - target\,|
\]

的值尽可能小。返回该最小可能的绝对差值。

**示例**

**示例 1**  
```text
Input: arr = [9,12,3,7,15], target = 5
Output: 2
Explanation: 对所有可能的 \[l,r\] 对 \[[0,0],[1,1],[2,2],[3,3],[4,4],[0,1],[1,2],[2,3],[3,4],[0,2],[1,3],[2,4],[0,3],[1,4],[0,4]\] 调用 `func`，Winston 得到了结果 [9,12,3,7,15,8,0,3,7,0,0,3,0,0,0]。最接近 5 的值是 7 与 3，因而最小差值为 2。
```

**示例 2**  
```text
Input: arr = [1000000,1000000,1000000], target = 1
Output: 999999
Explanation: Winston 对所有可能的 \[l,r\] 调用了 `func`，始终得到 1000000，所以最小差值为 999999。
```

**示例 3**  
```text
Input: arr = [1,2,4,8,16], target = 0
Output: 0
```

**约束条件**  

- $1 \leq \text{arr.length} \leq 10^5$
- $1 \leq \text{arr}[i] \leq 10^6$
- $0 \leq \text{target} \leq 10^7$

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有合法的 `(l, r)` 都枚举一遍，计算 `func(arr, l, r)`，再和 `target` 比较，找出最小的绝对差。

- **`func` 是什么？**  
  题目没有直接给出函数的定义，但提示里说：“*If the **and** value of sub‑array arr[i…j] is ≥ the **and** value of sub‑array arr[i…j+1]*”。  
  这说明 `func(arr, l, r)` 就是 **子数组 `arr[l…r]` 的按位与（bitwise AND）**。  
  按位与可以想象成“把每个数的二进制位都对应起来，只要有 0，结果就会是 0”。  

- **为什么暴力一定能得到正确答案？**  
  只要把所有 `l`（左端点）和 `r`（右端点）组合遍历一遍，必然会碰到真正最接近 `target` 的子数组。  

- **时间/空间复杂度的大白话**  
  - 时间复杂度记作 **O(n²)**，这里的 `n` 是数组长度。  
    这相当于“把 `n` 张卡片两两配对”，配对的次数会随 `n` 的平方增长。  
    当 `n = 10⁵` 时，配对次数大约是 `10¹⁰`，电脑根本跑不完。  
  - 空间复杂度是 **O(1)**（不计输出），因为只用几个临时变量。  

#### 代码（Python）

```python
def brute_min_diff(arr, target):
    """
    暴力解：枚举所有子数组，求按位与后与 target 的最小差值。
    只适合非常小的输入，用来验证思路。
    """
    n = len(arr)
    best = float('inf')          # 当前找到的最小差值

    for l in range(n):           # 左端点
        cur_and = arr[l]         # 维护子数组 [l..r] 的 AND 值
        for r in range(l, n):    # 右端点
            if r > l:            # r 向右扩展时，按位与会继续 “压低”
                cur_and &= arr[r]
            diff = abs(cur_and - target)
            if diff < best:
                best = diff
    return best
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  需要遍历所有 `(l, r)`，相当于 `n·(n+1)/2` 次计算。  
- **空间复杂度：O(1)**  
  只用了常数个整数变量。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于**枚举所有子数组**。我们需要利用 **按位与的单调性** 来剪枝。  

**关键观察 1：**  
把子数组右端点从左向右扩展时，按位与只会 **保持不变或变小**（因为 `x & y ≤ x`）。  
可以把它想成“水往低处流”，一旦某一位变成 0，就再也回不来。

**关键观察 2：**  
对固定的左端点 `i`，随着右端点 `j` 逐渐右移，`AND(i…j)` 的取值序列最多会改变 **log₂(max(arr))** 次。  
原因是每次 AND 只能把 1 位变成 0，`arr[i] ≤ 10⁶ < 2²⁰`，所以至多 20 次变化。  

**利用观察 2**，我们不必记录每一个 `j`，只记录 **每一次 AND 值变化时对应的最右端点**。  
这样对所有左端点累计的不同 AND 值总数是 `O(n·log max)`，远小于 `n²`。

**实现技巧——滚动集合（Rolling Set）**  

我们从左到右遍历数组，维护一个集合 `cur`，其中保存的是**以当前下标 `i` 为右端点的所有不同子数组 AND 值**。  
- 当我们把 `arr[i]` 加进来时，所有以前的子数组都要再和 `arr[i]` 做一次 AND（因为右端点向右延伸了）。  
- 同时，`arr[i]` 本身也可以作为长度为 1 的新子数组加入集合。  
- 由于很多 AND 结果会相同，我们在更新时把相同的值合并（只保留一次），这样集合的大小始终保持在 `log max` 级别。

在每一步更新完 `cur` 后，遍历集合中的每个 AND 值，直接计算 `|val - target|` 并更新全局最小答案。  

**为什么这样是最优的？**  
- 每个数组元素只会参与 **O(log max)** 次 AND 计算。  
- 整体时间是 `O(n·log max)`（约 `n·20`），在 `n = 10⁵` 时完全可以接受。  
- 只用了几个临时列表，空间是 `O(log max)`。

#### 代码（Python）

```python
def min_diff_and(arr, target):
    """
    最优解：利用 AND 的单调性和“每个左端点的 AND 变化次数有限” 的性质。
    时间复杂度 O(n * log MAX)   （MAX 为 arr 中的最大值，≤ 10⁶，log₂MAX ≤ 20）
    空间复杂度 O(log MAX)
    """
    INF = 10 ** 18
    answer = INF                     # 当前找到的最小差值
    cur = []                         # 以当前位置为右端点的所有不同 AND 值，按出现顺序保存

    for x in arr:                    # 从左到右遍历
        # 第一步：把新元素加入已有子数组的 AND 结果中
        nxt = [x]                     # 以 x 为单独子数组的 AND 值
        for v in cur:                # 逐个与之前的 AND 值做与运算
            nxt.append(v & x)

        # 第二步：合并重复的 AND 值，保持集合小（因为 AND 只能下降）
        # 这里利用“相邻相同的会被压掉”的特性，只保留不重复的值
        cur = []
        for v in nxt:
            if not cur or cur[-1] != v:   # 去重
                cur.append(v)

        # 第三步：更新答案
        for v in cur:
            diff = abs(v - target)
            if diff < answer:
                answer = diff
                # 早停：如果已经达到 0，无法再更好
                if answer == 0:
                    return 0

    return answer
```

> **代码解释（每行中文注释）**  
> - `cur` 保存“以当前遍历位置为右端点的所有不同子数组 AND”。  
> - `nxt = [x]` 把仅包含当前元素的子数组加入集合。  
> - 对 `cur` 中的每个旧值 `v`，计算 `v & x`，得到右端点向右扩展后新的 AND。  
> - 通过 `if not cur or cur[-1] != v` 去除相邻相同的结果，保证集合大小始终 ≤ `log MAX`。  
> - 最后遍历 `cur`，把每个 AND 与 `target` 的差值拿出来比较，维护全局最小。

#### 复杂度  

- **时间复杂度：O(n · log MAX)**  
  - `n` 为数组长度（最多 10⁵）。  
  - `log MAX` ≈ 20，因为 `MAX ≤ 10⁶ < 2²⁰`。  
  - 换句话说，程序大约只会做 `2 × 10⁶` 次 AND 运算和比较，跑得非常快。  
  - 与暴力的 O(n²) 相比，提升了数量级（从 10¹⁰ 降到 10⁶）。

- **空间复杂度：O(log MAX)**  
  - `cur` 最多保存 20 左右的整数，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：利用 **按位与的单调下降特性** 与 **“每个左端点的 AND 值变化次数有限”**，把原本 O(n²) 的枚举压缩到 O(n log MAX)。  
- **适用场景**（类似题目）  
  1. **子数组按位与/或的所有可能值**（如 LeetCode 898. Bitwise ORs of Subarrays）。  
  2. **子数组最小/最大 GCD**（GCD 也有类似的单调性）。  
  3. **子数组最小/最大值的离散化计数**（利用单调栈或单调队列）。  
- **一句话总结**：  
  “把子数组的 AND 看成只会‘掉位’的水流，利用每条水流最多掉多少位来限制状态数，枚举即可”。  

---

## 反思  

- **第一反应**：直接想到暴力枚举所有 `(l, r)`，因为这能保证正确。  
- **最容易踩的坑**  
  - **去重不彻底**：在更新 `cur` 时如果只用 `set` 会打乱顺序，失去单调性，导致集合大小不受控制。  
  - **忘记把单元素子数组加入**：否则会漏掉长度为 1 的情况。  
  - **边界值**：`target` 可能为 0，答案可能恰好为 0，需要提前返回以提升效率。  
- **下次遇到同类题**，第一步应该问自己：  
  “这个子数组运算（AND、OR、GCD…）有没有单调/递减/递增的性质？”  
  若有，就尝试 **状态压缩 + 滚动集合** 的思路，而不是盲目枚举。