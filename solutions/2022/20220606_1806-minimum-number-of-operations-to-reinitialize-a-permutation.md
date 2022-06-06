# #1806. Minimum Number of Operations to Reinitialize a Permutation / Minimum Number of Operations to Reinitialize a Permutation

> 难度：中等 · 标签：Array、Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-reinitialize-a-permutation/)

---

## 题目（英文原版）

**Description**

You are given an even integer n​​​​​​. You initially have a permutation perm of size n​​ where perm[i] == i​ (0-indexed)​​​​.
In one operation, you will create a new array arr, and for each i:
You will then assign arr​​​​ to perm.
Return the minimum non-zero number of operations you need to perform on perm to return the permutation to its initial value.

**Examples**

**Example 1:**

```
Input: n = 2
Output: 1
Explanation: perm = [0,1] initially.
After the 1st operation, perm = [0,1]
So it takes only 1 operation.
```

**Example 2:**

```
Input: n = 4
Output: 2
Explanation: perm = [0,1,2,3] initially.
After the 1st operation, perm = [0,2,1,3]
After the 2nd operation, perm = [0,1,2,3]
So it takes only 2 operations.
```

**Example 3:**

```
Input: n = 6
Output: 4
```

**Constraints**

- 2 <= n <= 1000
- n​​​​​​ is even.

---

## 题目（中文翻译）

给定一个偶数 `n`。最初你有一个大小为 `n` 的排列 `perm`，其中 `perm[i] == i`（**0-indexed**，即下标从 0 开始）。  

一次操作的过程如下：

1. 创建一个新数组 `arr`（array），对每个下标 `i`（`0 <= i < n`）执行：
   - 如果 `i` 为偶数，则 `arr[i] = perm[i / 2]`；
   - 如果 `i` 为奇数，则 `arr[i] = perm[n / 2 + (i - 1) / 2]`。
2. 将 `arr` 赋值给 `perm`（即 `perm = arr`）。

返回使 `perm` 恢复到初始状态（即 `perm[i] == i`）所需的最少 **非零** 操作次数。

---

### 示例

**示例 1**  
```text
Input: n = 2
Output: 1
Explanation: perm = [0,1] 初始时如此。
第一次操作后，perm = [0,1]。
因此只需要 1 次操作。
```

**示例 2**  
```text
Input: n = 4
Output: 2
Explanation: perm = [0,1,2,3] 初始时如此。
第一次操作后，perm = [0,2,1,3]。
第二次操作后，perm = [0,1,2,3]。
因此只需要 2 次操作。
```

**示例 3**  
```text
Input: n = 6
Output: 4
```

---

### 约束条件

- `2 <= n <= 1000`
- `n` 为偶数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心是“把一个固定的变换不停地作用在排列上，直到它又回到原来的样子”。  
我们可以把 **perm** 看成一排编号为 `0 … n-1` 的盒子，盒子里装着对应的数字。  
一次操作会把这些盒子重新排放，规则如下（这里把题目公式写成代码更直观）：

```text
如果 i 是偶数：   arr[i] = perm[i // 2]
如果 i 是奇数：   arr[i] = perm[n // 2 + (i - 1) // 2]
```

把 `arr` 再赋值回 `perm`，相当于把盒子里数字搬了一遍。  
因为 `n ≤ 1000` 且“操作次数不会超过 n”，我们可以**直接模拟**：  
1. 记录下最初的 `perm = [0, 1, 2, …, n-1]`。  
2. 按上面的规则算出 `arr`，把 `arr` 复制回 `perm`。  
3. 每完成一次操作，就检查 `perm` 是否已经和最初的数组相同。相同就返回已经做的次数。  

> **为什么这样一定能得到答案？**  
> 这一次次的变换实际上是把同一个“函数”不断复合。因为所有的排列都是有限的（最多 `n!` 种），必然会在某一步回到起点。题目已经保证了回到起点的次数不超过 `n`，所以直接模拟一定能在很短的时间内找到答案。

#### 代码（Python）

```python
def reinitializePermutation_bruteforce(n: int) -> int:
    # 初始排列：perm[i] == i
    perm = list(range(n))
    # 保存最初的排列，用来后面比较
    original = perm[:]

    def next_perm(p):
        """按照题目规则生成一次操作后的新排列"""
        arr = [0] * n
        for i in range(n):
            if i % 2 == 0:                # i 为偶数
                arr[i] = p[i // 2]
            else:                         # i 为奇数
                arr[i] = p[n // 2 + (i - 1) // 2]
        return arr

    steps = 0
    while True:
        steps += 1                     # 执行一次操作
        perm = next_perm(perm)         # 计算新排列
        if perm == original:           # 与最初的排列相同？
            return steps
```

#### 复杂度

- **时间复杂度**：`O(n * k)`，其中 `k` 是答案（最多 `n`），所以最坏情况是 `O(n²)`。  
  大白话：每次操作都要遍历 `n` 个位置，最多做 `n` 次，所以相当于“遍历 `n` 次 `n` 个盒子”，这就是 `n` 乘 `n`。
- **空间复杂度**：`O(n)`，我们需要保存当前的 `perm`、临时的 `arr` 以及最初的 `original`，都和 `n` 成正比。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每一步都要遍历整个数组**。其实我们并不需要关心所有位置的变化，只要弄清 **每个下标是怎么迁移的**，就能直接算出“多少次操作后会回到原位”。  

观察规则可以发现：

- `i = 0` 和 `i = n‑1` 永远不动（因为它们对应的公式里只会取到自己）。
- 对于其他下标（记作 `i`），一次操作后它会移动到 **`new_i = (2 * i) % (n - 1)`**。  

**推导过程**（不必记住，只要明白结论）：

1. 当 `i` 为偶数时，`i = 2 * t`，新位置是 `arr[2*t] = perm[t]` → 下标 `t = i/2`。  
2. 当 `i` 为奇数时，`i = 2 * t + 1`，新位置是 `arr[2*t+1] = perm[n/2 + t]` → 下标 `n/2 + t = (i + n) / 2`。  
3. 统一写成模运算可以得到 `new_i = (2 * i) % (n - 1)`（对 `i = 0`、`i = n‑1` 这两个特殊点除外，它们会映射到自己）。

于是，**一次操作等价于把每个下标乘以 2（模 `n‑1`）**。  
把这个过程重复 `k` 次，就是把 `i` 乘以 `2^k`（仍然取模 `n‑1`）：

```
i  →  2*i (mod n-1)  →  2^2*i (mod n-1)  → … →  2^k*i (mod n-1)
```

要让所有 `i`（除 0、n‑1 之外）回到原位，必须满足：

```
2^k ≡ 1 (mod n-1)
```

这正是 **“2 在模 n‑1 下的乘法阶”**（multiplicative order）。  
所以答案就是最小的正整数 `k` 使得 `2^k % (n-1) == 1`。

**如何求这个 k？**  
直接把 `2` 连乘，记下每一步的模值，直到再次出现 `1`。因为题目已保证答案 ≤ `n`，循环最多 `n` 次即可。

#### 代码（Python）

```python
def reinitializePermutation_optimal(n: int) -> int:
    """
    计算最小的 k，使得 (2^k) % (n-1) == 1
    这正是排列恢复到初始状态所需的操作次数。
    """
    target = n - 1          # 模数
    cur = 2 % target        # 第一次操作后下标 1 会变成 2%target
    k = 1                   # 已经做了 1 次操作

    # 循环直到 cur 再次回到 1
    while cur != 1:
        cur = (cur * 2) % target   # 再乘一次 2，取模
        k += 1

    return k
```

> **代码要点注释**  
> - `target = n - 1` 是因为除了 `0`、`n-1`，其它下标的循环是模 `n-1` 的。  
> - `cur` 保存当前的 `2^k % target`，从 `k = 1` 开始。  
> - 循环里每一步都相当于“再做一次操作”，所以 `k` 同时也是操作次数。  

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k` 是答案。根据提示，`k ≤ n`，所以最坏是 `O(n)`。  
  与暴力解相比，我们只做了 **常数级别的工作**（一次乘法和一次取模），不必遍历整个数组。
- **空间复杂度**：`O(1)`，只用了几个整数变量，和 `n` 大小无关。

---

## 心得

- **核心技巧**：把“数组变换”抽象成 **下标的数学映射**，进而用 **模运算** 与 **乘法阶**（multiplicative order）求解。  
- **适用场景**：  
  1. 需要求某个固定置换重复若干次后恢复原状的问题（如 “Permutation Power” 类题）。  
  2. 任何涉及“循环移位”或“按固定规则重新排列”的题目（比如 “Cyclic Rotation” 、 “Shuffle the Array”）。  
- **一句话总结**：**把数组操作看成下标的乘法映射，答案就是 2 在模 (n‑1) 下的最小循环次数。**

---

## 反思

- **第一反应**：看到“每次操作都把数组重新排布”，自然想到直接**模拟**，因为 n 只有 1000。  
- **最容易踩的坑**：  
  - 忘记 `0` 与 `n-1` 永远不动，导致在求模时出现除零或错误的循环。  
  - 误把 “`arr[i] = perm[perm[i]]`” 当成题目规则，实际规则是上文的奇偶分支。  
  - 在求最小 `k` 时，如果直接写 `while (2**k) % (n-1) != 1`，会产生大整数溢出或效率低下。使用循环乘法并即时取模才安全。  
- **下次遇到同类题**：第一步先**把操作写成下标映射公式**，判断是否可以用 **模运算** 或 **循环节** 来直接求解；如果不行，再考虑**完整模拟**。这样可以在最坏情况下快速定位最优解的方向。