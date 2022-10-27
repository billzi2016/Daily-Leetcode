# #1987. 唯一好子序列的数量 / Number of Unique Good Subsequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-unique-good-subsequences/)

---

## 题目（英文原版）

**Description**

You are given a binary string binary. A subsequence of binary is considered good if it is not empty and has no leading zeros (with the exception of "0").
Find the number of unique good subsequences of binary.
Return the number of unique good subsequences of binary. Since the answer may be very large, return it modulo 109 + 7.
A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: binary = "001"
Output: 2
Explanation: The good subsequences of binary are ["0", "0", "1"].
The unique good subsequences are "0" and "1".
```

**Example 2:**

```
Input: binary = "11"
Output: 2
Explanation: The good subsequences of binary are ["1", "1", "11"].
The unique good subsequences are "1" and "11".
```

**Example 3:**

```
Input: binary = "101"
Output: 5
Explanation: The good subsequences of binary are ["1", "0", "1", "10", "11", "101"]. 
The unique good subsequences are "0", "1", "10", "11", and "101".
```

**Constraints**

- 1 <= binary.length <= 105
- binary consists of only '0's and '1's.

---

## 题目（中文翻译）

给定一个二进制字符串 `binary`。如果一个子序列（subsequence）非空且没有前导零（唯一例外是字符串 `"0"`），则称其为 **好子序列**（good）。  
求 `binary` 中 **唯一** 好子序列的数量，并返回结果。由于答案可能非常大，请对 $10^9+7$ 取模后返回。

**子序列** 是指可以通过删除原序列中的若干（也可以不删除）字符而得到的序列，且剩余字符的相对顺序保持不变。

### 示例

**示例 1**  
```
Input: binary = "001"
Output: 2
Explanation: binary 的好子序列有 ["0", "0", "1"]。  
唯一的好子序列是 "0" 和 "1"。
```

**示例 2**  
```
Input: binary = "11"
Output: 2
Explanation: binary 的好子序列有 ["1", "1", "11"]。  
唯一的好子序列是 "1" 和 "11"。
```

**示例 3**  
```
Input: binary = "101"
Output: 5
Explanation: binary 的好子序列有 ["1", "0", "1", "10", "11", "101"]。  
唯一的好子序列是 "0", "1", "10", "11" 和 "101"。
```

### 约束条件

- $1 \le \text{binary.length} \le 10^5$
- `binary` 仅由字符 `'0'` 和 `'1'` 组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是**枚举所有子序列**，把每个子序列写成字符串后判断：

1. 不是空串。  
2. 不能出现「前导 0」——如果子序列的第一个字符是 `0`，只能是单独的 `"0"`。  

把所有满足条件的子序列放进集合 `set`，最后返回集合的大小（取模）。

> **数据结构类比**  
> - `set` 就像 **字典**，我们往里放东西，若已经存在就不会再增加。  
> - 枚举子序列相当于 **遍历所有可能的删除方案**，就像把一本书的每一页都可能被撕掉或留下，所有组合的数量是 `2^n`（`n` 为字符串长度）。

#### 代码（Python）

```python
from itertools import combinations

MOD = 10**9 + 7

def brute_force(binary: str) -> int:
    n = len(binary)
    good = set()                     # 用来去重的集合
    # 枚举子序列的长度（1~n）
    for l in range(1, n + 1):
        # 选出所有长度为 l 的下标组合
        for idxs in combinations(range(n), l):
            subseq = ''.join(binary[i] for i in idxs)   # 构造子序列字符串
            # 判断是否是“好”子序列
            if subseq[0] == '0' and subseq != '0':
                continue
            good.add(subseq)       # 自动去重
    return len(good) % MOD
```

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  解释：每个字符可以「保留」或「删除」两种状态，共有 `2^n` 种子序列；把下标转成字符串要遍历子序列本身，最坏是 `O(n)`。  
- **空间复杂度**：`O(2^n * n)`  
  需要把所有不同的子序列放进集合，最坏情况下几乎每个子序列都是不同的。

> 这已经远远超出题目限制（`n ≤ 10^5`），只能作为思路的出发点，下面我们要把它压缩到线性时间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子序列**。  
观察可以发现：

* **只要把一个已经是“好”子序列的字符串再拼上一个字符，它仍然是好子序列**（前提是原串的首字符已经是 `1`，否则会产生前导 `0`）。  
* 因此我们只需要记录**已经出现过的好子序列的数量**，而不必把它们一个个列举出来。  

把“好子序列”分成两类：

| 类别 | 说明 |
|------|------|
| **A** | 以 `1` 为首的好子序列（长度可以是 1，也可以很长） |
| **B** | 单独的 `"0"`（唯一合法的以 `0` 开头的子序列） |

设  

* `cnt1` – 当前已经出现的 **A 类** 子序列的数量（只计数，不计 `"0"`）。  
* `has0` – 是否已经出现过字符 `'0'`（从而把 `"0"` 加入答案）。  

每遍历到一个字符 `c`，会产生两类**新子序列**：

1. **单字符子序列**  
   * `c == '1'` → `"1"`（一定是好子序列）  
   * `c == '0'` → `"0"`（只有第一次出现时才算新）  

2. **把 `c` 加到所有已经是 **A 类** 的子序列后面**  
   这些子序列仍然以 `1` 为首，仍属于 **A 类**。  

如果我们把「所有已有的 A 类子序列」记作集合 `S`，则本轮可以产生的子序列集合是  

```
new_set = S ∪ {c}   （c 为单字符，视情况加入）
```

然而，**相同字符在不同位置产生的子序列会重复**。  
例如 `"101"` 中第二个 `'1'` 再把 `S` 中的 `"1"` 加上 `'1'`，得到的 `"11"` 已经在第一次 `'1'` 时产生过。  

要消除这种重复，只需要**记住上一次出现同一字符时产生的全部子序列数量**。  
设  

* `prev[0]` – 上一次处理字符 `'0'` 时「`cnt1 + (是否产生单字符 `'0'`）`」的值  
* `prev[1]` – 上一次处理字符 `'1'` 时「`cnt1 + 1`」的值  

则本轮 **真正新增的子序列数** 为  

```
candidate = cnt1 + base                # base = 1 (单字符) 或 0
new = candidate - prev[c]              # 去掉已经出现过的那部分
```

其中  

* `base = 1`                     → 当 `c == '1'`  
* `base = 1`                     → 当 `c == '0'` 且 `has0` 仍为 False（第一次出现）  
* `base = 0`                     → 当 `c == '0'` 且已经出现过 `"0"`  

`new` 可能为负（只有一种特殊情况：再次遍历 `'0'` 时 `base` 由 1 变成 0，导致 `candidate` 比 `prev[0]` 小 1），**负数代表本轮不产生任何新子序列**，我们把它当作 0。

把 `new` 加到 `cnt1`（除去单独的 `"0"` 那一项）后，就得到了新的 **A 类** 子序列数量。  
同时要把 `prev[c]` 更新为本轮的 `candidate`，为以后再次出现同字符做准备。

整个过程只需要一次遍历，时间 `O(n)`，空间 `O(1)`。

> **关键数据结构解释**  
> - `cnt1` → “以 1 开头的好子序列集合的大小”。可以想象成 **一本只记录以 1 开头的词典**，我们只记词的数量，不记具体内容。  
> - `prev` → “上一次出现该字符时，能产生的子序列数量”。相当于 **记住上一次查字典时的页码**，下次再查时只看页码的变化，就能知道新增了多少词。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numberOfUniqueGoodSubsequences(binary: str) -> int:
    """
    线性时间 O(n) 只使用常数额外空间。
    cnt1   : 以 '1' 为首的好子序列数量（不含单独的 "0"）
    has0   : 是否已经把单独的 "0" 加入答案
    prev   : prev[0] / prev[1] 记录上一次出现对应字符时
             (cnt1 当时 + 是否产生单字符) 的值
    """
    cnt1 = 0                 # A 类子序列的数量
    has0 = False             # 是否已经出现过 "0"
    prev = [0, 0]            # 上一次出现 0/1 时的 candidate

    for ch in binary:
        c = int(ch)          # 0 或 1

        # base 表示本轮是否还能产生单字符子序列
        if c == 1:
            base = 1                     # "1" 总是新子序列
        else:  # c == 0
            base = 0 if has0 else 1      # 第一次出现 0 才算新

        # candidate = 所有可能产生的子序列数量（不去重）
        candidate = cnt1 + base

        # 实际新增的子序列数（去掉上一次相同字符已经产生的那部分）
        new = candidate - prev[c]
        if new < 0:          # 只会在第二次出现 0 时出现 -1，视为 0
            new = 0

        # 把真正新增且以 1 为首的子序列计入 cnt1
        if c == 1:
            cnt1 = (cnt1 + new) % MOD          # 所有 new 都以 1 开头
        else:  # c == 0
            # new 里可能包含单独的 "0"，它不算在 cnt1 中
            add_to_cnt1 = new - base           # 去掉单字符 "0"
            if add_to_cnt1 < 0:
                add_to_cnt1 = 0
            cnt1 = (cnt1 + add_to_cnt1) % MOD
            has0 = True                         # 以后不再产生单字符 "0"

        # 为以后出现相同字符做准备
        prev[c] = candidate

    # 最终答案 = 以 1 开头的子序列 + （可能的单独 "0"）
    ans = cnt1 + (1 if has0 else 0)
    return ans % MOD
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，每一步做常数次整数运算。  
- **空间复杂度**：`O(1)`  
  只使用几个整数变量，与输入长度无关。

> 与暴力解对比：  
> - 暴力解需要 `2^n` 次遍历，根本不可行。  
> - 最优解把“所有子序列”压缩成 **几个计数**，实现线性时间。

---

## 心得

- **核心技巧**：**利用已有好子序列的数量直接计算新增子序列**，并用**上一次出现同字符时的计数**去重。  
- **适用的题型**  
  1. **计数不同子序列**（如 LeetCode 940 `Distinct Subsequences II`）。  
  2. **涉及前导字符限制的子序列计数**（本题、以及 “统计不以 `0` 开头的子序列” 等变形）。  
  3. **需要在遍历时“记住上一次状态”来消除重复**的动态规划问题。  

> **解题钥匙**：**“把子序列的集合抽象为‘数量’，用上一次出现的状态去除重复”。**

---

## 反思

- **第一反应**：直接枚举子序列 → 很快意识到 `2^n` 的爆炸。  
- **最容易踩的坑**  
  1. **前导 0 的特殊处理**：忘记把 `"0"` 单独计数，或者把以 `0` 开头的长子序列错误计入。  
  2. **去重时的负数**：`candidate - prev[c]` 可能为负，必须把它当作 0 处理，否则会出现莫名其妙的负贡献。  
  3. **取模时的顺序**：在做 “减去上一次计数” 之前一定要使用完整的整数值，否则模运算会把真实的正差变成大数。  

- **下次类似题的第一步**：  
  **先把“所有合法子序列的数量”写成一个递推式**，再思考“相同字符会导致哪些重复”，用“上一次出现时的计数”把重复剔除。这样往往能在一次遍历里完成计数。