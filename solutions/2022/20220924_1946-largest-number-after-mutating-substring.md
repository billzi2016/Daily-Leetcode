# #1946. **变换子串后的最大数** / Largest Number After Mutating Substring

> 难度：中等 · 标签：Array、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/largest-number-after-mutating-substring/)

---

## 题目（英文原版）

**Description**

You are given a string num, which represents a large integer. You are also given a 0-indexed integer array change of length 10 that maps each digit 0-9 to another digit. More formally, digit d maps to digit change[d].
You may choose to mutate a single substring of num. To mutate a substring, replace each digit num[i] with the digit it maps to in change (i.e. replace num[i] with change[num[i]]).
Return a string representing the largest possible integer after mutating (or choosing not to) a single substring of num.
A substring is a contiguous sequence of characters within the string.

**Examples**

**Example 1:**

```
Input: num = "132", change = [9,8,5,0,3,6,4,2,6,8]
Output: "832"
Explanation: Replace the substring "1":
- 1 maps to change[1] = 8.
Thus, "132" becomes "832".
"832" is the largest number that can be created, so return it.
```

**Example 2:**

```
Input: num = "021", change = [9,4,3,5,7,2,1,9,0,6]
Output: "934"
Explanation: Replace the substring "021":
- 0 maps to change[0] = 9.
- 2 maps to change[2] = 3.
- 1 maps to change[1] = 4.
Thus, "021" becomes "934".
"934" is the largest number that can be created, so return it.
```

**Example 3:**

```
Input: num = "5", change = [1,4,7,5,3,2,5,6,9,4]
Output: "5"
Explanation: "5" is already the largest number that can be created, so return it.
```

**Constraints**

- 1 <= num.length <= 105
- num consists of only digits 0-9.
- change.length == 10
- 0 <= change[d] <= 9

---

## 题目（中文翻译）

你得到一个字符串 `num`，它表示一个大整数。同时给定一个下标从 0 开始、长度为 10 的整数数组 `change`，用于将每个数字 0‑9 映射到另一个数字。更形式化地说，数字 `d` 映射为 `change[d]`。  

你可以选择对 `num` 的 **一个子串**（substring）进行变异。对子串进行变异的方式是，将子串中的每个字符 `num[i]` 替换为 `change[num[i]]`（即用映射后的数字替换）。  

返回一个字符串，表示在对 `num` 的 **单个子串**（或不进行任何操作）变异后能够得到的最大整数。  
子串是指字符串中连续的一段字符。

---

### 示例

#### 示例 1
```
Input: num = "132", change = [9,8,5,0,3,6,4,2,6,8]
Output: "832"
Explanation: 替换子串 "1"：
- 1 映射为 change[1] = 8。
因此，"132" 变为 "832"。
"832" 是可以得到的最大数字，返回它。
```

#### 示例 2
```
Input: num = "021", change = [9,4,3,5,7,2,1,9,0,6]
Output: "934"
Explanation: 替换子串 "021"：
- 0 映射为 change[0] = 9。
- 2 映射为 change[2] = 3。
- 1 映射为 change[1] = 4。
于是，"021" 变为 "934"。
"934" 是可以得到的最大数字，返回它。
```

#### 示例 3
```
Input: num = "5", change = [1,4,7,5,3,2,5,6,9,4]
Output: "5"
Explanation: "5" 已经是可以得到的最大数字，直接返回它。
```

---

### 约束条件

- `1 <= num.length <= 10^5`
- `num` 仅由字符 `0`‑`9` 组成
- `change.length == 10`
- `0 <= change[d] <= 9` (对所有 `0 <= d <= 9`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子串**，把子串里的每个字符都按照 `change` 表进行替换，得到一个新的数字字符串，然后比较大小，取最大的那个。

- **数据结构**：  
  - `num` 本身是一个字符串，遍历时可以把它当成字符数组（列表）来使用。  
  - `change` 是长度为 10 的数组，类似于一本**查字典**：把原来的数字（key）对应到新的数字（value）。  

- **为什么正确**：  
  我们把所有合法的“变异方案”都枚举一遍，必然会包括最优的那一种。只要把每种方案产生的字符串和当前最大值比较，就一定能得到全局最大。

- **时间/空间复杂度**：  
  - 枚举子串需要两层循环：外层选起始位置 `i`（0~n‑1），内层选结束位置 `j`（i~n‑1），总共大约 `n·(n+1)/2 ≈ O(n²)` 次。  
  - 对每个子串我们要遍历一次子串内部的字符进行替换，最坏情况下子串长度也是 `O(n)`，所以整体时间是 `O(n³)`，不过我们可以在内部直接在原字符串上做一次复制并修改，时间仍然是 `O(n²)`（因为每次只遍历一次子串），这已经足够说明暴力解的低效。  
  - 额外空间只需要保存一个复制的字符串，大小为 `O(n)`。

> **大白话解释**：  
> `O(n²)` 就是“如果你有 1000 个数字，最差情况下要比较 1000×1000=1 000 000 次”。当 `n` 达到 10⁵ 时，这个数字会变成 10¹⁰，根本跑不完。

#### 代码（Python）

```python
def largestNumber_bruteforce(num: str, change: list[int]) -> str:
    n = len(num)
    best = num                     # 先把原始字符串当作答案
    # 枚举子串的左端点
    for i in range(n):
        # 枚举子串的右端点（包含 i 本身）
        for j in range(i, n):
            # 把 num 复制一份，准备在子串 [i, j] 上改写
            cur = list(num)
            # 对子串内的每个字符进行映射
            for k in range(i, j + 1):
                cur[k] = str(change[int(cur[k])])
            cur_str = "".join(cur)
            # 与当前最好的结果比较，取大的
            if cur_str > best:
                best = cur_str
    return best
```

- 第 4 行把原始字符串保存为当前最优解。  
- 第 7‑8 行是两层循环，枚举所有子串。  
- 第 11‑13 行把子串里的每个字符按照 `change` 替换。  
- 第 15‑16 行比较大小，`>` 对字符串直接按字典序比较，等价于数值大小比较（因为长度相同且都是数字）。

#### 复杂度

- **时间复杂度**：`O(n²)`（两层循环枚举子串，每次内部遍历子串的字符）。  
  - 含义：如果 `num` 长度是 10⁴，程序大约要执行 10⁸ 次基本操作，已经很慢了；长度是 10⁵ 时更是不可接受。

- **空间复杂度**：`O(n)`，因为我们需要复制 `num` 成列表 `cur`，大小随输入长度线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**唯一的瓶颈**是我们尝试了所有可能的子串。实际上，只要**一次连续的替换**就能得到最大的结果，且我们不需要尝试每一种起止位置。关键观察如下：

1. **只有当映射后的数字大于原数字时，才值得替换**。如果 `change[d] < d`，把它改成更小的数只会让整体变小，永远不会是最优方案。  
2. **一旦开始替换，应该一直替换下去，直到出现“映射后不再增大”**的情况。原因是：
   - 替换的子串是连续的，若在已经开始的子串里出现 `change[d] == d`（不变）或者 `change[d] > d`（仍然变大），继续往后替换不会降低已经得到的前缀值。  
   - 只有当 `change[d] < d` 时，继续往后替换才会让数值下降，这时必须立刻停止，因为后面的字符再怎么好也抵消不了已经变小的这位。  

基于以上两点，我们可以 **一次线性扫描** 完成：

- 从左到右遍历 `num`。  
- **状态机**：  
  - `started = False` 表示当前是否已经进入了“正在变大的子串”。  
  - 当 `started` 为 `False` 时，若 `change[d] > d`，则从这里开始变换，设 `started = True`。  
  - 当 `started` 为 `True` 时，若 `change[d] >= d`（仍然不小于），继续替换；否则（`change[d] < d`）立刻结束变换，后面的字符保持原样，且再也不会重新开始（因为已经错过了更靠前的高位）。  

- **为什么只会出现一次**：  
  - 题目要求只能变异**一个**子串。若我们在某个位置停止后继续往后再找另一个更大的子串，那前面的停止点已经导致该位变小，整体数值必然不如一次性在更靠前的位开始并一直到更靠后的位置的方案。  

这样只需一次遍历即可得到答案。

#### 代码（Python）

```python
def largestNumber(num: str, change: list[int]) -> str:
    # 将字符串转成列表，方便原地修改
    digits = list(num)
    started = False               # 是否已经进入“变大”阶段

    for i, ch in enumerate(digits):
        d = int(ch)                # 原始数字
        nd = change[d]             # 映射后的数字

        if not started:
            # 还没有开始变换：只有映射后更大才值得启动
            if nd > d:
                digits[i] = str(nd)
                started = True
        else:
            # 已经在变换区间：只要不让数字变小就继续改
            if nd >= d:
                digits[i] = str(nd)
            else:
                # 一旦出现变小，立即结束后面的所有改动
                break

    return "".join(digits)
```

- 第 2 行把输入字符串拆成列表，便于就地修改。  
- 第 4‑5 行用 `started` 记录是否已经进入变换区间。  
- 第 8‑12 行处理“未开始”时的情况：只有当映射后更大才启动。  
- 第 14‑20 行处理“已经开始”时的情况：只要映射后不小于原数就继续改，否则 `break` 停止遍历。  
- 第 22 行把列表重新拼成字符串返回。

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次字符串。  
  - 含义：如果 `num` 长度是 10⁵，只需要执行大约 10⁵ 次基本操作，毫秒级就能跑完。

- **空间复杂度**：`O(n)`（存放字符列表），如果把输入视为可写的原地修改，也可以说是 `O(1)` 额外空间，因为只用了常数级的变量 `started`、`d`、`nd`。

---

## 心得

- **核心技巧**：**一次线性扫描 + 状态机**，利用“只在映射后更大的时候才开始并持续更大”这一贪心性质。  
- **适用的题型**：  
  1. 只能进行一次连续操作，使整体数值最大（如 “Maximum Subarray with One Swap” 类似思路）。  
  2. 需要把子串全部替换为更大的字符或数字的题目（如 “Lexicographically Smallest String After Operations”）。  
- **一句话总结**：**只要映射后不让当前位变小，就一直往后改；一旦变小，立刻停手**。

---

## 反思

- **第一反应**：直接想遍历所有子串，写出暴力枚举的代码。  
- **最容易踩的坑**：  
  - 忘记**只能改一次子串**，导致在遍历过程中多次启动/结束。  
  - 对 `change[d] == d` 的处理不当：它既不需要启动，也可以作为已经启动后的“安全”字符继续保留。  
  - 边界情况：整个字符串都不需要改动（如示例 3），要确保代码返回原始 `num`。  
- **下次遇到同类题**：第一步先**思考何时值得“开始”操作**（映射后更大），随后**判断何时必须“停止”**（映射后更小），把过程抽象成 **“开始 → 继续 → 停止”** 的状态机，直接线性扫描即可。