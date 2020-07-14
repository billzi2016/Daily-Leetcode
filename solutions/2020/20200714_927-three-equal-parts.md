# #927. 三等分 / Three Equal Parts

> 难度：困难 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/three-equal-parts/)

---

## 题目（英文原版）

**Description**

You are given an array arr which consists of only zeros and ones, divide the array into three non-empty parts such that all of these parts represent the same binary value.
If it is possible, return any [i, j] with i + 1 < j, such that:
If it is not possible, return [-1, -1].
Note that the entire part is used when considering what binary value it represents. For example, [1,1,0] represents 6 in decimal, not 3. Also, leading zeros are allowed, so [0,1,1] and [1,1] represent the same value.

**Examples**

**Example 1:**

```
Input: arr = [1,0,1,0,1]
Output: [0,3]
```

**Example 2:**

```
Input: arr = [1,1,0,1,1]
Output: [-1,-1]
```

**Example 3:**

```
Input: arr = [1,1,0,0,1]
Output: [0,2]
```

**Constraints**

- 3 <= arr.length <= 3 * 104
- arr[i] is 0 or 1

---

## 题目（中文翻译）

给定一个只包含 `0` 和 `1` 的数组 `arr`（array），将其划分为三个非空部分（non‑empty parts），使得这三个部分表示相同的二进制值（binary value）。  
如果能够实现，返回任意满足 `i + 1 < j` 的 `[i, j]`；否则返回 `[-1, -1]`。  

注意，判断二进制值时必须使用完整的部分。例如，`[1,1,0]` 在十进制（decimal）中等于 `6`，而不是 `3`。前导零（leading zeros）是允许的，因此 `[0,1,1]` 与 `[1,1]` 表示相同的值。

**示例 1**  
输入: `arr = [1,0,1,0,1]`  
输出: `[0,3]`

**示例 2**  
输入: `arr = [1,1,0,1,1]`  
输出: `[-1,-1]`

**示例 3**  
输入: `arr = [1,1,0,0,1]`  
输出: `[0,2]`

**约束条件**  

- `3 <= arr.length <= 3 * 10^4`
- `arr[i]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的切分点全部枚举一遍，然后把每一段看成二进制数，比较它们是否相等。

- **枚举切分点**  
  数组长度记为 `n`，我们要找两个下标 `i、j`（满足 `i+1 < j`），把数组划分成  
  `arr[0 … i]`、`arr[i+1 … j-1]`、`arr[j … n‑1]` 三段。  
  所有合法的 `(i, j)` 组合大约有 `C(n,2) ≈ n²/2` 种。

- **把子数组转成整数**  
  二进制数可以直接用 Python 的 `int(''.join(map(str, sub)), 2)` 把子数组转成十进制。  
  为了让 “前导零” 不影响比较，我们在转化前先把子数组左边的 `0` 去掉（如果全是 `0`，则值为 `0`）。

- **比较三段的值**  
  如果三段的整数相同，就找到了答案，直接返回对应的 `(i, j)`；遍历结束仍未找到，则返回 `[-1, -1]`。

> **生活化类比**：  
> 把数组想成一串灯泡（亮=1，灭=0），我们要把它切成三段，使每段灯泡的“亮灯模式”完全相同。最笨的办法就是把每一种切法都试一遍，再把每段的亮灯模式写下来比较。

- **为什么一定正确**  
  因为我们把 **所有** 可能的切法都检查了一遍，只要有合法答案必定会在检查过程中被发现。

#### 代码（Python）

```python
def threeEqualParts_bruteforce(arr):
    n = len(arr)

    # 把子数组转成整数（去掉左边的 0）
    def value(sub):
        # 去掉前导零
        k = 0
        while k < len(sub) and sub[k] == 0:
            k += 1
        # 全是 0 的情况
        if k == len(sub):
            return 0
        # 把剩余的二进制位转成十进制整数
        return int(''.join(map(str, sub[k:])), 2)

    # 枚举所有 (i, j)
    for i in range(n - 2):            # 第一个段至少要有一个元素
        for j in range(i + 2, n):    # 第二个段也至少要有一个元素
            left  = arr[:i + 1]
            mid   = arr[i + 1:j]
            right = arr[j:]

            if value(left) == value(mid) == value(right):
                return [i, j]

    return [-1, -1]
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层两个循环枚举 `i、j`，组合数约为 `n²/2`。  
  - 每次都要把三段数组转成整数，最坏情况下每段长度是 `O(n)`，所以整体是 `O(n³)`。  
  - 用大白话说，就是如果数组有 1000 个元素，程序大概要跑 1000³ = 10⁹ 次基本操作，明显会超时。

- **空间复杂度**：`O(1)`（不计返回值）  
  - 只用了常数个临时变量，没有额外的随输入规模增长的容器。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有切点**（`O(n²)`）以及 **每次都重新计算子数组的二进制值**（`O(n)`），导致总共 `O(n³)`。  
我们需要找到只遍历一次数组就能判断是否可以切分的办法。

关键观察如下：

1. **只关心 `1` 的分布**  
   二进制数的大小完全由 `1` 的位置决定，前导零可以随意补。  
   因此我们先统计数组里一共有多少个 `1`，记为 `total_ones`。

2. **每段必须拥有相同数量的 `1`**  
   - 如果 `total_ones` 不是 `3` 的倍数，则不可能把 `1` 平均分到三段，直接返回 `[-1, -1]`。  
   - 特殊情况：`total_ones == 0`，整个数组全是 `0`，任意切分都满足要求，返回 `[0, n‑2]`（最左边的合法切法）。

3. **确定每段的起始位置**  
   当 `total_ones` 能被 `3` 整除时，每段必须恰好包含 `k = total_ones / 3` 个 `1`。  
   我们一次遍历数组，记录下第 1 段第一个 `1` 的下标 `first1`、第 2 段第一个 `1` 的下标 `second1`、第 3 段第一个 `1` 的下标 `third1`。

4. **把三段的“形状”对齐比较**  
   从这三个起始位置开始，同时向右比较对应的元素是否相等。  
   - 如果在比较过程中出现不相等，则说明无法得到相同的二进制值。  
   - 当比较到数组末尾（即 `third1` 越界）时，说明后三段的 “有效位” 完全相同。  

   此时我们还必须保证 **每段后面可以补足足够的零**，因为切分后每段的末尾可能会出现不同数量的前导零。  
   实际上，只要把第三段的剩余长度 `suffix_len = n - third1` 看作 “模式”，前两段的末尾也必须至少有这么多字符（全是 `0`），否则无法对齐。

5. **算出最终的切分下标**  
   - 第一段结束位置 `i = first1 + suffix_len - 1`（因为第一段要覆盖它对应的模式）。  
   - 第二段结束位置 `j = second1 + suffix_len`（第二段的结束位置是模式的最后一个字符的下一个索引）。  
   返回 `[i, j]` 即可。

> **类比**：  
> 想象三根相同的绳子上分别挂了若干颗灯（`1`）和空位（`0`），我们要把原来的一根长绳子切成三段，使得每段灯的排列完全相同。只要先数出灯的总数，平均分配到每段，然后把三段的灯“对齐”检查是否一致，就能一次遍历搞定。

#### 代码（Python）

```python
def threeEqualParts(arr):
    n = len(arr)

    # 1️⃣ 统计 1 的总数
    total_ones = sum(arr)
    # 全是 0 的特殊情况
    if total_ones == 0:
        return [0, n - 2]          # 任意合法切法，这里选最左

    # 2️⃣ 必须能被 3 整除，否则不可能
    if total_ones % 3 != 0:
        return [-1, -1]

    k = total_ones // 3            # 每段应该拥有的 1 的个数

    # 3️⃣ 找到每段的第一个 1 的下标
    first1 = second1 = third1 = -1
    cnt = 0
    for idx, bit in enumerate(arr):
        if bit == 1:
            cnt += 1
            if cnt == 1:
                first1 = idx
            elif cnt == k + 1:
                second1 = idx
            elif cnt == 2 * k + 1:
                third1 = idx
                break               # 找到第三段的起点即可

    # 4️⃣ 同时比较三个子数组的每一位
    #   只要有一位不相同，就说明无法等价
    while third1 < n:
        if arr[first1] != arr[second1] or arr[first1] != arr[third1]:
            return [-1, -1]
        first1 += 1
        second1 += 1
        third1 += 1

    # 5️⃣ 计算切分下标
    #    第一个子数组的结束位置是 first1 - 1（因为循环已经把它推进到模式末尾）
    i = first1 - 1
    #    第二个子数组的结束位置是 second1（此时 second1 指向模式的最后一个元素的下一个位置）
    j = second1
    return [i, j]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历数组一次（统计 `1`、找起始位置）和一次对齐比较，整体线性。  
  - 与暴力解相比，从 `n³` 降到了 `n`，即使 `n` 达到 `3·10⁴` 也能轻松在毫秒级完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，额外空间不随输入规模增长。

---

## 心得

- **核心技巧**：把问题从“比较整段二进制值”转化为“比较 `1` 的分布和后缀模式”。  
- **适用的题型**  
  1. 把数组/字符串划分成若干等价片段（如 “Split Array into Three Equal Parts”）。  
  2. 需要在二进制或字符序列中保持相同“模式”时（如 “Find All Anagrams in a String” 的滑动窗口思路）。  
  3. 只关心特定字符出现次数的分割问题（如 “Partition Array into Three Parts With Equal Sum”）。  
- **一句话总结解题钥匙**：**先把整体的约束（总 1 的个数）化简，再用一次遍历对齐并验证局部模式**。

---

## 反思

- **第一反应**：直接枚举切点并把子数组转成整数，觉得最直观。  
- **最容易踩的坑**  
  - 忘记处理全 `0` 的特殊情况，会误判返回 `[-1,-1]`。  
  - 对齐比较时没有考虑后缀的零，需要保证前两段能够补足第三段后面的零。  
  - 在计算返回下标时容易把“已经移动过的指针”误当作切分位置，导致 off‑by‑one 错误。  
- **下次类似题目的第一步**：  
  **先统计全局信息（如总和、总个数），判断是否有可能再继续**，这样可以在一开始就排除大多数不可能的情况，避免盲目枚举。