# #2156. 找到满足给定哈希值的子串 / Find Substring With Given Hash Value

> 难度：困难 · 标签：String、Sliding Window、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/find-substring-with-given-hash-value/)

---

## 题目（英文原版）

**Description**

The hash of a 0-indexed string s of length k, given integers p and m, is computed using the following function:
Where val(s[i]) represents the index of s[i] in the alphabet from val('a') = 1 to val('z') = 26.
You are given a string s and the integers power, modulo, k, and hashValue. Return sub, the first substring of s of length k such that hash(sub, power, modulo) == hashValue.
The test cases will be generated such that an answer always exists.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0
Output: "ee"
Explanation: The hash of "ee" can be computed to be hash("ee", 7, 20) = (5 * 1 + 5 * 7) mod 20 = 40 mod 20 = 0. 
"ee" is the first substring of length 2 with hashValue 0. Hence, we return "ee".
```

**Example 2:**

```
Input: s = "fbxzaad", power = 31, modulo = 100, k = 3, hashValue = 32
Output: "fbx"
Explanation: The hash of "fbx" can be computed to be hash("fbx", 31, 100) = (6 * 1 + 2 * 31 + 24 * 312) mod 100 = 23132 mod 100 = 32. 
The hash of "bxz" can be computed to be hash("bxz", 31, 100) = (2 * 1 + 24 * 31 + 26 * 312) mod 100 = 25732 mod 100 = 32. 
"fbx" is the first substring of length 3 with hashValue 32. Hence, we return "fbx".
Note that "bxz" also has a hash of 32 but it appears later than "fbx".
```

**Constraints**

- 1 <= k <= s.length <= 2 * 104
- 1 <= power, modulo <= 109
- 0 <= hashValue < modulo
- s consists of lowercase English letters only.
- The test cases are generated such that an answer always exists.

---

## 题目（中文翻译）

给定一个 **0 索引** 的字符串 `s`（长度为 `k`），以及整数 `p` 与 `m`，其哈希（hash）值通过下列函数计算：

> `hash(s, p, m) = ( val(s[0]) * p^0 + val(s[1]) * p^1 + … + val(s[k‑1]) * p^{k‑1} ) mod m`

其中 `val(s[i])` 表示字符 `s[i]` 在字母表中的序号，`val('a') = 1`，`val('z') = 26`。

现在给定字符串 `s`、整数 `power`、`modulo`、`k` 与 `hashValue`。返回 `sub`——`s` 中长度为 `k` 的**第一个**子串（substring），使得 `hash(sub, power, modulo) == hashValue`。

测试数据保证必然存在答案。

**子串（substring）** 是指字符串中连续的、非空的字符序列。

---

### 示例

#### 示例 1
**输入**  
``` 
s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0
```
**输出**  
```
"ee"
```
**解释**  
`"ee"` 的哈希值可以计算为  
`hash("ee", 7, 20) = (5 * 1 + 5 * 7) mod 20 = 40 mod 20 = 0`。  
`"ee"` 是长度为 2、哈希值为 0 的第一个子串，因此返回 `"ee"`。

#### 示例 2
**输入**  
``` 
s = "fbxzaad", power = 31, modulo = 100, k = 3, hashValue = 32
```
**输出**  
```
"fbx"
```
**解释**  
`"fbx"` 的哈希值为  
`hash("fbx", 31, 100) = (6 * 1 + 2 * 31 + 24 * 31^2) mod 100 = 23132 mod 100 = 32`。  
`"bxz"` 的哈希值为  
`hash("bxz", 31, 100) = (2 * 1 + 24 * 31 + 26 * 31^2) mod 100 = 25732 mod 100 = 32`。  
`"fbx"` 是长度为 3、哈希值为 32 的第一个子串。

---

### 约束条件
- `1 <= k <= s.length <= 2 * 10^4`
- `1 <= power, modulo <= 10^9`
- `0 <= hashValue < modulo`
- `s` 仅由小写英文字母组成
- 测试数据保证答案一定存在

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有长度为 `k` 的子串都枚举一遍，逐个计算它们的哈希值，然后挑出第一个等于 `hashValue` 的子串返回。  

- **枚举子串**：把原字符串 `s` 当成一排房子，从左到右依次挑出长度为 `k` 的连续房间（子串），这相当于滑动一个固定长度的窗口。
- **计算哈希**：根据题目给出的公式  
  \[
  \text{hash}(t) = \bigg(\sum_{i=0}^{k-1} \text{val}(t[i]) \times \text{power}^i\bigg) \bmod \text{modulo}
  \]  
  这里 `val('a') = 1, …, val('z') = 26`。  
  计算时可以把每个字符的数值乘上对应的幂次，再把所有结果相加后取模。  
- **为什么正确**：我们把每一种可能的子串都检查了一遍，只要出现满足条件的子串，就一定会被找出来，且因为是从左到右依次检查的，第一个找到的自然就是答案。

**时间/空间复杂度**  
- **时间**：枚举 `n‑k+1`（`n = len(s)`）个子串，每个子串内部要跑 `k` 次循环去算幂次和乘积，整体是 `O((n‑k+1) * k) ≈ O(n·k)`。如果 `n` 最高是 2·10⁴，`k` 也可能接近 `n`，最坏情况下相当于 `O(n²)`，这在实际运行时会明显慢下来。  
- **空间**：只需要常数级别的额外变量（如临时哈希值、幂次），所以是 `O(1)`。

> **大白话**：`O(n²)` 可以想象成“把一本 20000 页的书每页都要抄写 20000 次”，显然不现实。

#### 代码（Python）

```python
def subStrHash_bruteforce(s: str, power: int, modulo: int,
                         k: int, hashValue: int) -> str:
    n = len(s)

    # 预先把字符转成 1~26 的整数，后面会用到
    vals = [ord(ch) - ord('a') + 1 for ch in s]

    # 暴力遍历所有长度为 k 的子串
    for start in range(n - k + 1):
        cur_hash = 0          # 当前子串的哈希值
        cur_pow = 1          # power^i，i 从 0 开始
        # 计算子串 s[start : start + k] 的哈希
        for i in range(k):
            cur_hash = (cur_hash + vals[start + i] * cur_pow) % modulo
            cur_pow = (cur_pow * power) % modulo   # 为下一个字符准备 power^{i+1}
        if cur_hash == hashValue:   # 找到第一个满足条件的子串
            return s[start:start + k]

    # 题目保证一定有答案，这里不会执行到
    return ""
```

#### 复杂度

- **时间复杂度**：`O(n·k)`（最坏情况相当于 `O(n²)`），因为每个窗口内部都要重新算一次哈希。
- **空间复杂度**：`O(1)`，只用了几个整数变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复计算哈希是主要瓶颈**。  
如果我们能在移动窗口时 **只用常数时间更新哈希**，整体就能降到线性 `O(n)`。这正是**滚动哈希（Rolling Hash）**的核心思想。

**滚动哈希的关键点**  

1. **哈希的定义**  
   \[
   H = \big(\sum_{i=0}^{k-1} v_i \cdot p^i\big) \bmod m
   \]  
   其中 `v_i = val(sub[i])`，`p = power`，`m = modulo`。

2. **从右向左滑动窗口**  
   - 设当前窗口是 `s[i : i+k]`（左闭右开），其哈希记作 `H_i`。  
   - 当我们把窗口左移一位，变成 `s[i-1 : i-1+k]`，需要把最右侧的字符 `s[i+k-1]` **去掉**，并把新加入的左侧字符 `s[i-1]` **加入**。  
   - 为了方便去掉最右字符，我们把窗口的哈希写成 **从右到左** 的形式（即最低位对应窗口最右字符）：
     \[
     H_i = \big(v_{i} \cdot p^{k-1} + v_{i+1} \cdot p^{k-2} + \dots + v_{i+k-1} \cdot p^{0}\big) \bmod m
     \]  
     这样在左移窗口时，最右字符对应的系数是 `p^0 = 1`，直接可以减去。

3. **更新公式**  
   已知 `H_i`，求左移一位后的 `H_{i-1}`：
   - 先把最右字符的贡献去掉：`H_i - v_{i+k-1}`（因为它乘以 `p^0 = 1`）。  
   - 再把剩下的部分整体除以 `p`（在模运算里相当于乘以 `p^{-1}`），因为所有幂次都向右平移了一位。  
   - 最后把新左字符 `v_{i-1}` 加上 `v_{i-1} * p^{k-1}`。  
   公式写成代码更直观（全部在模 `m` 下）：

   ```python
   H_{i-1} = ( (H_i - v_{i+k-1}) * inv_p + v_{i-1} * p^{k-1} ) % m
   ```

   其中 `inv_p` 是 `p` 在模 `m` 下的**逆元**，即 `inv_p * p ≡ 1 (mod m)`。  
   由于 `m` 可能不是质数，直接求逆元比较麻烦。**更简洁的做法**是**不使用逆元**，而是直接从右往左一次性算出所有窗口的哈希：

   - 先计算最后一个窗口（最右侧的 `k` 个字符）的哈希 `cur`（按照题目给出的正向公式）。
   - 然后向左遍历，每一步把左侧新字符的贡献加入，同时把最右字符的旧贡献去掉（乘以 `p^{k}`），并对 `modulo` 取模。  
   - 这一步只需要预先算好 `p^{k-1}`（记作 `pow_k_1`），以及 `p^{k}`（记作 `pow_k`），都可以在 `O(log k)` 的快速幂或 `O(k)` 的线性循环中得到（这里 `k ≤ 2·10⁴`，线性就足够快）。

4. **实现细节**  
   - 为了避免负数取模，`(x - y) % m` 在 Python 中已经安全（会自动把负数转成正数的同余类）。  
   - 记录下满足哈希等于 `hashValue` 的所有窗口的起始位置，取最小的即可（因为我们是从右往左遍历，最后一次更新的满足条件的窗口就是“最左边的”）。

**整体思路**：  
- 先把字符映射成 1~26 的整数。  
- 计算 `power^{k-1}`（记作 `pow_k_1`）和 `power^{k}`（记作 `pow_k`）。  
- 从字符串最右侧开始，维护当前长度为 `k` 的窗口哈希 `cur`。  
- 每左移一步，使用公式快速更新 `cur`。  
- 若 `cur == hashValue`，记录当前窗口的左端索引。遍历结束后返回对应子串。

> **类比**：把滚动哈希想象成“流水线上的装配工”。每当一个新零件（字符）进来，老的零件（最右字符）被踢出去，整个产品的价值（哈希）只需要微调，而不是重新把所有零件重新计价。

#### 代码（Python）

```python
def subStrHash(s: str, power: int, modulo: int,
               k: int, hashValue: int) -> str:
    """
    返回第一个满足 hash(sub, power, modulo) == hashValue 的长度为 k 的子串
    """
    n = len(s)
    vals = [ord(ch) - ord('a') + 1 for ch in s]   # 字符转成 1~26

    # 预计算 power^{k-1} % modulo 和 power^{k} % modulo
    pow_k_1 = 1
    for _ in range(k - 1):
        pow_k_1 = (pow_k_1 * power) % modulo          # p^{k-1}
    pow_k = (pow_k_1 * power) % modulo                # p^{k}

    # 先算最右侧窗口的哈希（从左到右的普通定义）
    cur = 0
    cur_pow = 1
    for i in range(k):
        cur = (cur + vals[n - k + i] * cur_pow) % modulo
        cur_pow = (cur_pow * power) % modulo

    # 记录满足条件的最左起始位置，初始为最右窗口的起点
    best_start = n - k if cur == hashValue else -1

    # 从右往左依次把窗口左移一位
    # i 表示新窗口左端的索引（从 n-k-1 -> 0）
    for i in range(n - k - 1, -1, -1):
        # 把最右字符的贡献去掉（它乘以 p^0 = 1）
        cur = (cur - vals[i + k]) % modulo
        # 把剩余部分整体乘以 power（相当于幂次整体左移一位）
        cur = (cur * power) % modulo
        # 把新左字符加入，它对应的是 p^{k-1}
        cur = (cur + vals[i] * pow_k_1) % modulo

        # 若哈希相等，更新最左起始位置
        if cur == hashValue:
            best_start = i

    # 根据记录的最左起始位置切片返回子串
    return s[best_start:best_start + k]
```

**代码要点注释**：

- `pow_k_1`、`pow_k`：分别是 `power^{k-1}` 与 `power^{k}` 的模值，后面更新哈希时会用到。
- 初始 `cur`：直接按照题目给出的正向公式算出最右窗口的哈希，**不需要逆元**。
- 更新过程三步：
  1. `cur = (cur - vals[i + k]) % modulo` 去掉最右字符（乘以 `p^0`）。
  2. `cur = (cur * power) % modulo` 把所有剩余字符的幂次左移一位（等价于除以 `p`，但乘 `power` 更安全）。
  3. `cur = (cur + vals[i] * pow_k_1) % modulo` 把新左字符加入，乘以 `p^{k-1}`。
- 因为我们是从右往左遍历，**最后一次更新的满足条件的窗口就是起始位置最小的**，直接保存 `best_start` 即可。

#### 复杂度

- **时间复杂度**：`O(n)`。只遍历一次字符串，每次窗口移动只做常数次算术运算。相比暴力的 `O(n·k)`，快了一个数量级。
- **空间复杂度**：`O(1)`（不计输出子串本身）。只用了几个整数变量和一个长度为 `n` 的整数列表（字符值），字符值列表可以视作原字符串的直接映射，额外空间仍是常数级。

---

## 心得

- **核心技巧**：滚动哈希（Rolling Hash）+ 逆向滑动窗口。  
- **适用的题型**：
  1. “寻找满足特定哈希值的子串” 类题（如本题、LeetCode 1016 *子串的最大和* 的变形）。
  2. “判断两个字符串是否相等（或相似）”的 Rabin‑Karp 字符串匹配算法。
  3. “最长不重复子串”等需要快速比较子串的场景，也常用滚动哈希配合二分搜索。
- **一句话总结解题钥匙**：**把每次窗口移动的代价压到 O(1)，只在哈希值上做增量更新**。

---

## 反思

- **第一反应**：看到“hash”二字就想到 “直接遍历、每次重新算”。这会导致超时，是最常见的误区。
- **最容易踩的坑**：
  1. **幂次顺序**：题目定义的哈希是左端字符乘 `p^0`，右端字符乘 `p^{k-1}`，如果写反了会导致所有答案错误。建议先在纸上写小例子验证。
  2. **模运算的负数**：`(a - b) % m` 在 Python 中是安全的，但在其他语言可能需要手动加 `m` 防止负数。
  3. **大数溢出**：`power`、`modulo` 均可达 `10^9`，直接相乘可能超过 64 位整数范围，使用 Python 的大整数即可，若在 C++/Java 中要注意使用 `long long` 或 `BigInteger`。
- **下次遇到同类题的第一步**：**先把哈希公式写清楚，再思考如何把窗口左移或右移时的增量变化**，通常可以直接得到滚动哈希的更新公式，从而实现线性时间解法。