# #2683. 相邻位异或 / Neighboring Bitwise XOR

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/neighboring-bitwise-xor/)

---

## 题目（英文原版）

**Description**

A 0-indexed array derived with length n is derived by computing the bitwise XOR (⊕) of adjacent values in a binary array original of length n.
Specifically, for each index i in the range [0, n - 1]:
Given an array derived, your task is to determine whether there exists a valid binary array original that could have formed derived.
Return true if such an array exists or false otherwise.

**Examples**

**Example 1:**

```
Input: derived = [1,1,0]
Output: true
Explanation: A valid original array that gives derived is [0,1,0].
derived[0] = original[0] ⊕ original[1] = 0 ⊕ 1 = 1 
derived[1] = original[1] ⊕ original[2] = 1 ⊕ 0 = 1
derived[2] = original[2] ⊕ original[0] = 0 ⊕ 0 = 0
```

**Example 2:**

```
Input: derived = [1,1]
Output: true
Explanation: A valid original array that gives derived is [0,1].
derived[0] = original[0] ⊕ original[1] = 1
derived[1] = original[1] ⊕ original[0] = 1
```

**Example 3:**

```
Input: derived = [1,0]
Output: false
Explanation: There is no valid original array that gives derived.
```

**Constraints**

- n == derived.length
- 1 <= n <= 105
- The values in derived are either 0's or 1's

---

## 题目（中文翻译）

给定一个 **0 索引 (0-indexed)** 的数组 `derived`，其长度为 `n`。`derived` 是通过对长度相同的 **二进制数组 (binary array)** `original` 中相邻元素进行 **按位异或 (bitwise XOR)** (⊕) 计算得到的。具体地，对于每个 **索引 (index)** `i`，满足 `0 ≤ i ≤ n‑1`：

```
derived[i] = original[i] ⊕ original[(i + 1) mod n]
```

换言之，`derived` 的第 `i` 个元素等于 `original` 中第 `i` 个元素与其后一个元素（循环到数组开头）的异或结果。

**任务**：判断是否存在至少一个满足上述关系的合法 **二进制数组 (binary array)** `original`。若存在返回 `true`，否则返回 `false`。

---

### 示例

**示例 1**

```
Input: derived = [1,1,0]
Output: true
Explanation: 一个满足条件的 original 为 [0,1,0]。
derived[0] = original[0] ⊕ original[1] = 0 ⊕ 1 = 1
derived[1] = original[1] ⊕ original[2] = 1 ⊕ 0 = 1
derived[2] = original[2] ⊕ original[0] = 0 ⊕ 0 = 0
```

**示例 2**

```
Input: derived = [1,1]
Output: true
Explanation: 一个满足条件的 original 为 [0,1]。
derived[0] = original[0] ⊕ original[1] = 1
derived[1] = original[1] ⊕ original[0] = 1
```

**示例 3**

```
Input: derived = [1,0]
Output: false
Explanation: 不存在满足条件的 original。
```

---

### 约束条件

- `n == derived.length`
- `1 <= n <= 10^5`
- `derived` 中的元素仅为 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有可能的原始数组** `original` 都枚举一遍，然后逐个检查它们生成的 `derived` 是否和题目给出的相同。

- **数据结构**：我们只需要一个普通的 Python 列表来存放 `original`，把它看成一串 0/1。  
  - 可以把列表想象成 **一本字典**，每一页（下标）上写的就是一个二进制数字（0 或 1）。  
- **验证过程**：遍历 `original`，按照题目定义 `derived[i] = original[i] XOR original[(i+1) % n]`（注意最后一个元素要和第一个“环”起来），得到一个新数组 `tmp`，再和输入的 `derived` 做逐位比较。  
- **正确性**：只要我们把 **所有** 2ⁿ 种可能的 `original` 都尝试一遍，必定能找到一条满足条件的（如果存在的话），否则全部尝试完后返回 `False`。

#### 代码（Python）

```python
from itertools import product
from typing import List

def possible_bruteforce(derived: List[int]) -> bool:
    n = len(derived)
    # 用 product 生成 0/1 的所有组合，等价于二进制枚举 0 ~ 2^n-1
    for original in product([0, 1], repeat=n):
        ok = True
        # 检查每一个相邻位置的异或是否等于 derived[i]
        for i in range(n):
            nxt = (i + 1) % n               # 环形相邻下标
            if (original[i] ^ original[nxt]) != derived[i]:
                ok = False                  # 只要有一个不相等，就可以提前放弃
                break
        if ok:                             # 全部匹配成功
            return True
    return False                          # 没有一种组合满足
```

> **关键行解释**  
> - `product([0, 1], repeat=n)`：相当于把 0/1 放进 **字典**，遍历所有可能的“词条”。  
> - `original[i] ^ original[nxt]`：`^` 是 Python 中的位异或运算，等价于 “如果两个数不同则得到 1”。  

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n)`  
  - 2ⁿ 来自所有可能的原始数组（每个位置 0/1 两种选择），每种组合要遍历 n 次检查。  
  - 用大白话说，就是“指数级增长”，当 n 只要稍微大一点（比如 20），运行时间就会爆炸。  
- **空间复杂度**：`O(n)`  
  - 只存放当前枚举的 `original`（长度 n）以及常数级的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们把所有 2ⁿ 种可能都列举出来。实际上，题目给出的等式蕴含了更深的数学性质，利用 **异或的可交换、可结合** 特性可以一次遍历就得到答案。

**关键观察**：

1. 题目定义  
   \[
   derived[i] = original[i] \oplus original[(i+1) \bmod n]
   \]
   （这里的 `⊕` 表示位异或）

2. 把所有 `derived[i]` **全部异或**（记作 `X = derived[0] ⊕ derived[1] ⊕ … ⊕ derived[n-1]`），代入上式：

   \[
   \begin{aligned}
   X &= \bigoplus_{i=0}^{n-1} \bigl(original[i] \oplus original[(i+1)\bmod n]\bigr)\\
     &= \bigl(\bigoplus_{i=0}^{n-1} original[i]\bigr) \oplus
        \bigl(\bigoplus_{i=0}^{n-1} original[(i+1)\bmod n]\bigr)
   \end{aligned}
   \]

   注意右边第二个大括号里，索引 `(i+1) mod n` 其实把 **所有原始元素** 又遍历了一遍，只是顺序不同而已。于是每个 `original[k]` 在两个大括号里各出现一次，**异或两次会相互抵消**（因为 `a ⊕ a = 0`），于是得到：

   \[
   X = 0
   \]

   这说明 **若原始数组存在**，`derived` 的所有元素的异或一定是 0。**这是一条必要条件**。

3. 这条条件同时也是 **充分条件**。  
   - 任选一个起始值 `original[0]`（可以设为 0），利用等式 `original[i+1] = original[i] ⊕ derived[i]` 逐步推算出整个 `original`。  
   - 推算 n 步后会回到 `original[0]`，此时得到的 `original[0]` 实际上是 `original[0] ⊕ X`。如果 `X = 0`，两者相等，说明推算过程没有矛盾，构造出的 `original` 就合法。  
   - 因此 **只要 `X = 0`，就一定能找到一个满足条件的原始数组**。

4. 特殊情况 `n = 1`：  
   - 只有 `derived[0] = original[0] ⊕ original[0] = 0`，同样满足 “所有元素异或为 0”。  

**结论**：`derived` 能否由某个二进制数组生成，仅取决于 **`derived` 所有元素的异或是否为 0**。

> **类比**：把 `derived` 看成一本**账本**，每一页记的是相邻两天的“收入差”。如果把所有页的差额加在一起（异或相当于“相消”），结果必须是 0，才说明这本账本是自洽的。

#### 代码（Python）

```python
from typing import List

def possible_optimal(derived: List[int]) -> bool:
    """
    判断是否存在原始二进制数组，使得
    derived[i] = original[i] XOR original[(i+1) % n]
    """
    xor_sum = 0                     # 用来累计 derived 的异或和
    for val in derived:
        xor_sum ^= val              # ^ 是异或运算
    # 若 xor_sum 为 0，说明条件满足；否则不可能构造出 original
    return xor_sum == 0
```

> **关键行解释**  
> - `xor_sum ^= val`：把当前元素与累计结果做异或，相当于“把这页的差额和前面的相消”。  
> - 最后只判断 `xor_sum == 0`，一次遍历即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要遍历一次 `derived`，每一步都是常数时间的异或。相当于“线性增长”，即使 `n = 10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(1)`  
  - 只使用了一个整数 `xor_sum` 来存放中间结果，和输入规模无关。

---

## 心得

- **核心技巧**：利用异或的 **自反性**（`a ⊕ a = 0`）和 **交换结合律**，把看似需要构造的过程化简为“所有元素的异或是否为 0”。  
- **适用的题型**  
  1. 环形或循环关系下的二进制约束（如 “环形相邻异或”）  
  2. 需要判断是否存在满足某种“配对消除”条件的数组（如 “相邻差的异或为 0”）  
  3. 只关心整体奇偶性或整体异或的题目（如 “数组的异或和为 0”）  
- **一句话总结**：**只要把所有 `derived` 元素异或一次，结果为 0 就一定能找到原始数组**。

---

## 反思

- **第一反应**：立刻想到枚举所有可能的原始数组，因为题目只说“是否存在”，看起来要把所有情况都试遍。  
- **最容易踩的坑**  
  - 忘记 **环形** 的特性，导致把最后一个位置写成 `original[n-1] XOR original[n]`（数组越界）而不是 `original[n-1] XOR original[0]`。  
  - 只检查了 `derived` 的总和或计数，而不是 **异或**，导致错误的判断。  
- **下次类似题的第一步**：先思考 **“整体约束”**（比如所有元素的异或、奇偶性、和）是否能直接给出答案，而不是急于构造具体解。这样往往能把指数级的搜索压缩到线性时间。