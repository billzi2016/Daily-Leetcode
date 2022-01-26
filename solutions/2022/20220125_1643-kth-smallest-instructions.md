# #1643. 第 k 小的指令 / Kth Smallest Instructions

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-instructions/)

---

## 题目（英文原版）

**Description**

Bob is standing at cell (0, 0), and he wants to reach destination: (row, column). He can only travel right and down. You are going to help Bob by providing instructions for him to reach destination.
The instructions are represented as a string, where each character is either:
Multiple instructions will lead Bob to destination. For example, if destination is (2, 3), both "HHHVV" and "HVHVH" are valid instructions.
However, Bob is very picky. Bob has a lucky number k, and he wants the kth lexicographically smallest instructions that will lead him to destination. k is 1-indexed.
Given an integer array destination and an integer k, return the kth lexicographically smallest instructions that will take Bob to destination.

**Examples**

**Example 1:**

```
Input: destination = [2,3], k = 1
Output: "HHHVV"
Explanation: All the instructions that reach (2, 3) in lexicographic order are as follows:
["HHHVV", "HHVHV", "HHVVH", "HVHHV", "HVHVH", "HVVHH", "VHHHV", "VHHVH", "VHVHH", "VVHHH"].
```

**Example 2:**

```
Input: destination = [2,3], k = 2
Output: "HHVHV"
```

**Example 3:**

```
Input: destination = [2,3], k = 3
Output: "HHVVH"
```

**Constraints**

- destination.length == 2
- 1 <= row, column <= 15
- 1 <= k <= nCr(row + column, row), where nCr(a, b) denotes a choose b​​​​​.

---

## 题目（中文翻译）

Bob 站在单元格 (0, 0)，他想要到达目的地 (row, column)。他只能向右 (right) 和向下 (down) 移动。请你为 Bob 提供一段指令，使其能够到达目的地。  
指令用字符串表示，每个字符只能是：

- **'H'**：向右移动一次（horizontal）  
- **'V'**：向下移动一次（vertical）

多条指令都可以让 Bob 到达目的地。例如，若目的地是 (2, 3)，则 `"HHHVV"` 与 `"HVHVH"` 都是合法的指令。  

然而 Bob 非常挑剔。他有一个幸运数字 *k*，想要得到第 *k* 小的（按字典序）合法指令。*k* 使用 **1‑基索引**。  

给定整数数组 `destination` 和整数 `k`，返回第 *k* 小的、能够把 Bob 带到目的地的指令。

---

### 示例

**示例 1**  
```text
Input: destination = [2,3], k = 1
Output: "HHHVV"
Explanation: 所有能够到达 (2, 3) 的指令按字典序排列如下：
["HHHVV", "HHVHV", "HHVVH", "HVHHV", "HVHVH", "HVVHH", "VHHHV", "VHHVH", "VHVHH", "VVHHH"]。
```

**示例 2**  
```text
Input: destination = [2,3], k = 2
Output: "HHVHV"
Explanation: 按字典序第 2 小的合法指令是 "HHVHV"。
```

**示例 3**  
```text
Input: destination = [2,3], k = 3
Output: "HHVVH"
Explanation: 按字典序第 3 小的合法指令是 "HHVVH"。
```

---

### 约束条件

- `destination.length == 2`
- `1 <= row, column <= 15`
- `1 <= k <= nCr(row + column, row)`，其中 `nCr(a, b)` 表示组合数 “a 选 b”。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有** 能到达 `(row, column)` 的指令都列举出来，再按照字典序（lexicographic order）排序，最后取第 `k` 条。  

- **数据结构**：我们可以把指令看成只包含两种字符的字符串：`'H'` 表示向右走一步，`'V'` 表示向下走一步。  
- **怎么枚举**：从起点走到终点必须走 `row` 步向下（`V`）和 `column` 步向右（`H`），总共 `row + column` 步。只要把这 `row + column` 步中的 `row` 步标记为 `V`（其余标记为 `H`），每一种标记方式就是一种合法指令。  
  这相当于从 `row + column` 个位置中挑选出 `row` 个位置放 `V`，其余放 `H`，也就是组合数 `C(row+column, row)`。  
- **为什么正确**：每一种合法的标记方式都恰好对应一条只走右或下、恰好走满 `row` 步下、`column` 步右的路径，且不存在重复或遗漏。  
- **时间/空间**：  
  - 枚举组合的过程本身是 `C(row+column, row)` 次，每次产生一个长度为 `row+column` 的字符串。  
  - 排序需要把所有字符串放进列表再排序，时间大约是 `O(N log N)`（`N = C(row+column, row)`），空间也是 `O(N·(row+column))` 用来保存所有字符串。  
  - 用大白话讲，假设 `row=15, column=15`，则 `N = C(30,15) ≈ 155M`，显然直接把 1.5 亿条 30 长度的字符串全部存下来是不可能的——这就是暴力解的致命瓶颈。  

#### 代码（Python）  

```python
import itertools
from math import comb

def kthInstruction_bruteforce(destination, k):
    row, col = destination
    total_len = row + col                     # 指令总长度
    # 生成所有在 total_len 位中挑选 row 位放 V 的组合
    all_instr = []
    for v_pos in itertools.combinations(range(total_len), row):
        # 把选中的位置设为 V，其余设为 H
        s = ['H'] * total_len
        for idx in v_pos:
            s[idx] = 'V'
        all_instr.append(''.join(s))

    # 按字典序排序
    all_instr.sort()
    # k 是 1-indexed
    return all_instr[k - 1]

# 示例
print(kthInstruction_bruteforce([2, 3], 3))   # -> "HHVVH"
```

> **关键行中文注释**  
> - `itertools.combinations(range(total_len), row)`：相当于在 `total_len` 张卡片里挑 `row` 张放 “V”。  
> - `s = ['H'] * total_len`：先把所有位置都设成 “H”。  
> - `all_instr.sort()`：把所有指令按照字典序从小到大排好。

#### 复杂度  

- **时间复杂度**：`O(C(row+col, row) * (row+col) + C(row+col, row) log C(row+col, row))`  
  - 前半部分是生成每条指令（每条长度 `row+col`），后半部分是排序。  
  - 对于最大输入 `row = col = 15`，约等于 `O(1.5e8 * 30)`，远远超时。  
- **空间复杂度**：`O(C(row+col, row) * (row+col))`，需要把所有指令都存下来，同样不可接受。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **“枚举所有指令”** 是最慢的环节。我们其实不需要把所有指令都写出来，只要知道第 `k` 条指令的每一个字符应该是 `'H'` 还是 `'V'` 即可。  

**核心观察**：  
- 所有合法指令在字典序下，先出现的都是以 `'H'` 开头的（因为 `'H'` 的 ASCII 小于 `'V'`）。  
- 假设我们已经确定前缀 `prefix`，现在要决定第 `i` 位是 `'H'` 还是 `'V'`。  
  - 如果把第 `i` 位设为 `'H'`，则剩下的路径必须在 `(remaining_row, remaining_col-1)` 之间完成。  
  - 在这种情况下，**后面所有可能的指令数量**恰好是组合数 `C(remaining_row + remaining_col - 1, remaining_row)`（从剩余的格子里挑出所有下走的步数）。  

利用上述计数，我们可以**一步步构造**答案：  

1. 初始化 `row = destination[0]`、`col = destination[1]`，`k` 为 1‑indexed。  
2. 当 `row > 0` 且 `col > 0` 时：  
   - 计算如果现在放 `'H'`，后面还能有多少种合法指令：`cnt = C(row + col - 1, row)`（因为此时只剩下 `col-1` 步右和 `row` 步下）。  
   - 若 `k <= cnt`，说明第 `k` 条指令一定以 `'H'` 开头，选 `'H'` 并把 `col -= 1`。  
   - 否则，第 `k` 条指令不在所有以 `'H'` 开头的指令里，而在以 `'V'` 开头的那一部分。此时把 `k -= cnt`（跳过前面 `cnt` 条），选 `'V'` 并把 `row -= 1`。  
3. 当 `row == 0` 时，只能把剩下的 `col` 步全写成 `'H'`；当 `col == 0` 时，只能全写成 `'V'`。  
4. 把所有选的字符拼接成最终答案。  

**为什么正确**：  
- 组合数 `C(a, b)` 正好统计了在剩余格子中挑选下走步数的所有可能指令数。  
- 通过比较 `k` 与 `cnt`，我们等价于在已排序的序列中“跳过”前 `cnt` 条指令，从而定位到第 `k` 条所在的分支。  
- 这一步步逼近的过程保证了每一步都选到了字典序中对应位置的字符，最终得到的完整字符串正是第 `k` 小的。  

**关键数据结构**：  
- **组合数（binomial coefficient）**：在 Python 3.8+ 中可以直接用 `math.comb(n, r)` 计算。它的含义类似于“从 `n` 本书里挑 `r` 本”。这里我们把它当作“从剩余格子里挑出下走的步数”。  

#### 代码（Python）  

```python
from math import comb

def kthInstruction(destination, k):
    """
    返回第 k 小（字典序）的合法指令字符串。
    参数：
        destination: [row, col]，目标格子坐标
        k: 1-indexed
    """
    row, col = destination
    ans = []                     # 用列表收集字符，最后 join 成字符串

    # 当仍有上下左右两种选择时循环
    while row > 0 and col > 0:
        # 如果此时走 'H'（右），剩下的格子数是 row + col - 1，
        # 需要在其中安排 row 步向下
        cnt = comb(row + col - 1, row)   # 以 'H' 为当前字符的所有合法指令数量

        if k <= cnt:
            # 第 k 条指令在所有以 'H' 开头的指令里
            ans.append('H')
            col -= 1                     # 右走一步，列数减一
        else:
            # 第 k 条指令不在以 'H' 开头的那部分，而在以 'V' 开头的部分
            ans.append('V')
            k -= cnt                     # 跳过前面 cnt 条指令
            row -= 1                     # 下走一步，行数减一

    # 走完上面的循环后，要么 row 为 0，要么 col 为 0
    # 剩下的全部只能用唯一的字符填满
    ans.extend(['H'] * col)   # 只剩右走
    ans.extend(['V'] * row)   # 只剩下走

    return ''.join(ans)

# ------------------- 示例 -------------------
print(kthInstruction([2, 3], 1))  # "HHHVV"
print(kthInstruction([2, 3], 2))  # "HHVHV"
print(kthInstruction([2, 3], 3))  # "HHVVH"
```

> **代码要点中文注释**  
> - `comb(row + col - 1, row)`：在剩余的 `row+col-1` 步里挑出 `row` 步向下的组合数，等价于“以 H 为当前字符的指令有多少”。  
> - `if k <= cnt:`：如果 k 落在这部分，说明答案的当前字符就是 `'H'`。  
> - `k -= cnt`：如果不在 `'H'` 那部分，就把前面的 `cnt` 条指令“剔除”，把 k 向后移动。  

#### 复杂度  

- **时间复杂度**：`O(row + col)`  
  - 循环最多执行 `row + col` 次（每一步都确定一个字符），每次只做常数时间的组合数查询。  
  - 对于最大输入 `30` 步，几乎可以忽略不计。  
- **空间复杂度**：`O(row + col)`（存储答案的字符列表）。  
  - 与暴力解的 `O(N·(row+col))` 相比，省了几乎所有额外空间。  

---

## 心得  

- **核心技巧**：**利用组合数计数并逐位构造字典序第 k 小的序列**。  
- **适用的题型**（类似思路）：  
  1. **K-th Smallest Perfect Square**（在有序集合中找第 k 小）  
  2. **K-th Smallest Number in Lexicographical Order**（LC 440）  
  3. **K-th Permutation Sequence**（LC 60）——都是在“有序的组合/排列”中定位第 k 项。  
- **一句话总结解题钥匙**：**把“枚举所有可能”转化为“在已排序的序列里跳过多少条”，用组合数快速计数**。  

---

## 反思  

- **第一反应**：看到“字典序第 k 小”，立刻想到**二分/计数**而不是直接枚举。  
- **最容易踩的坑**：  
  - **组合数溢出**：`row+col` 最多 30，`C(30,15)` 仍在 64 位整数范围内，但如果约束更大，需要使用大数或取模。  
  - **k 是 1‑indexed**：容易忘记在比较 `k <= cnt` 时不要把 `k` 先减一。  
  - **边界情况**：当 `row == 0` 或 `col == 0` 时只能填充唯一字符，别忘了把剩余字符一次性写完。  
- **下次类似题的第一步**：先**确定计数公式**（这里是组合数），再**逐位比较 k 与计数值**，把答案一步步“锁定”。