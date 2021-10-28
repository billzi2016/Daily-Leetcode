# #1529. 最小后缀翻转次数 / Minimum Suffix Flips

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-suffix-flips/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed binary string target of length n. You have another binary string s of length n that is initially set to all zeros. You want to make s equal to target.
In one operation, you can pick an index i where 0 <= i < n and flip all bits in the inclusive range [i, n - 1]. Flip means changing '0' to '1' and '1' to '0'.
Return the minimum number of operations needed to make s equal to target.

**Examples**

**Example 1:**

```
Input: target = "10111"
Output: 3
Explanation: Initially, s = "00000".
Choose index i = 2: "00000" -> "00111"
Choose index i = 0: "00111" -> "11000"
Choose index i = 1: "11000" -> "10111"
We need at least 3 flip operations to form target.
```

**Example 2:**

```
Input: target = "101"
Output: 3
Explanation: Initially, s = "000".
Choose index i = 0: "000" -> "111"
Choose index i = 1: "111" -> "100"
Choose index i = 2: "100" -> "101"
We need at least 3 flip operations to form target.
```

**Example 3:**

```
Input: target = "00000"
Output: 0
Explanation: We do not need any operations since the initial s already equals target.
```

**Constraints**

- n == target.length
- 1 <= n <= 105
- target[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始、长度为 `n` 的二进制字符串 `target`。再给你另一个同样长度为 `n`、初始全部为 `'0'` 的二进制字符串 `s`，你希望通过一系列操作使 `s` 与 `target` 相等。  

一次操作可以 **选择** 一个下标 `i`（`0 ≤ i < n`），并 **翻转**（flip）区间 `[i, n‑1]` 内的所有位。翻转指将 `'0'` 变为 `'1'`，`'1'` 变为 `'0'`。  

返回将 `s` 变成 `target` 所需的 **最少** 操作次数。

---

### 示例

**示例 1**

```
Input: target = "10111"
Output: 3
```

**解释**：初始时 `s = "00000"`。  
1. 选择 `i = 2`：`"00000"` → `"00111"`  
2. 选择 `i = 0`：`"00111"` → `"11000"`  
3. 选择 `i = 1`：`"11000"` → `"10111"`  

至少需要 3 次翻转才能得到 `target`。

---

**示例 2**

```
Input: target = "101"
Output: 3
```

**解释**：初始时 `s = "000"`。  
1. 选择 `i = 0`：`"000"` → `"111"`  
2. 选择 `i = 1`：`"111"` → `"100"`  
3. 选择 `i = 2`：`"100"` → `"101"`  

至少需要 3 次翻转才能得到 `target`。

---

**示例 3**

```
Input: target = "00000"
Output: 0
```

**解释**：初始的 `s` 已经等于 `target`，不需要任何操作。

---

### 约束条件

- `n == target.length`
- `1 ≤ n ≤ 10^5`
- `target[i]` 只能是 `'0'` 或 `'1'`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**一步步模拟**题目描述的操作：  

1. 先把 `s` 初始化为全 `0` 的字符串。  
2. 从左到右检查每一个位置 `i`（`0 ≤ i < n`）。  
3. 如果此时 `s[i]` 与 `target[i]` 不同，就把区间 `[i, n‑1]` 的所有位全部翻转。  
4. 重复直到遍历完所有位置。  

> **数据结构类比**：  
> - `s` 可以看成一本笔记本，每一页写着 `0` 或 `1`。  
> - “翻转区间” 就像把笔记本从第 `i` 页往后的所有页都涂黑（`0→1`）或擦白（`1→0`）。  

这种做法显然能得到一个合法的答案，因为每次我们都把左边已经匹配好的位固定住，后面的位再继续纠正。  

#### 代码（Python）  

```python
def minFlips_brute(target: str) -> int:
    n = len(target)
    # 把 s 用 list 方便原地修改
    s = ['0'] * n
    flips = 0                     # 记录操作次数

    for i in range(n):
        if s[i] != target[i]:    # 当前位置不相同，需要翻转
            flips += 1
            # 把 i .. n-1 的每一位都取反
            for j in range(i, n):
                s[j] = '1' if s[j] == '0' else '0'
            # 调试时可以打印中间状态
            # print(f'flip at {i}: {"".join(s)}')
    return flips
```

- 第 4 行创建一个可变的字符数组来模拟 `s`。  
- 第 8‑9 行判断当前位是否已经和目标相同。  
- 第 11‑13 行是 **核心**：对 `[i, n‑1]` 区间逐个取反，时间开销是 `O(n-i)`。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 最坏情况下每次都要翻转几乎整条后缀，例如 `target = "111...1"`，第一位不匹配会翻转 `n` 次，第二位再翻 `n‑1` 次，依此类推，整体大约是 `n + (n‑1) + … + 1 = n·(n+1)/2`，即二次方级别。  
  - 用大白话说，就是**每次都要重新检查很多已经处理过的字符**，所以会慢。  

- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n` 的数组来保存当前的 `s`，其余变量都是常数级别。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈**是每次翻转时都要遍历后面的所有字符。  
实际上我们并不需要真的去修改每个字符，只要知道**当前位到底被翻转了多少次**（奇数次还是偶数次）就能判断它的真实值。

**关键观察**  

- 翻转操作只会影响**它左边的所有位置**，右边的位在以后仍然可能被再次翻转。  
- 对于位置 `i`，我们只关心**截至 i‑1 为止已经执行了多少次翻转**。如果翻转次数是奇数，`s[i]` 实际上已经被反转了一次；如果是偶数，则仍是初始的 `0`。  

于是可以使用一个**“翻转奇偶标记”** `flip`（取值 `0` 或 `1`）来记录到目前为止的翻转次数的奇偶性：

1. 初始化 `flip = 0`（表示还没有翻转，`s` 仍然全是 `0`）。  
2. 从左到右遍历 `target`：  
   - 真实的当前位应为 `flip`（因为原始是 `0`，翻转奇数次变成 `1`，偶数次仍是 `0`）。  
   - 若 `flip` 与 `target[i]` 不同，说明此时的位不匹配，需要在 `i` 位置再做一次翻转。  
   - 翻转一次后，`flip` 取反（`flip ^= 1`），因为之后的所有位都会被再翻转一次。  
3. 最终的翻转次数即为答案。  

> **类比**：  
> 把 `flip` 想象成灯泡开关的“状态”。最开始灯泡是关的（`0`），每次我们把开关向右推一次（在位置 `i` 进行翻转），后面的灯泡都会随之改变状态。我们只需要记住开关现在是开还是关，而不必去逐个点亮每盏灯。  

#### 代码（Python）  

```python
def minFlips(target: str) -> int:
    flip = 0          # 记录截至当前下标已经翻转了奇数次(1)还是偶数次(0)
    ans = 0           # 统计需要的翻转次数

    for ch in target:               # 依次遍历每个字符
        # 当前真实的位 = 原始 0 翻转 flip 次后的值，即 flip 本身
        if int(ch) != flip:         # 如果不相等，说明需要再翻一次
            ans += 1                # 增加一次操作计数
            flip ^= 1               # flip 取反，后面的位都被再翻转一次
    return ans
```

- 第 2 行的 `flip` 初始为 `0`（相当于“没有翻转”）。  
- 第 5 行把字符直接转成整数，便于比较（`'0'→0`, `'1'→1`）。  
- 第 7‑9 行是核心：**不需要真的去改后面的字符**，只要更新 `flip` 即可。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，每一步都是 **常数时间** 的比较与位运算。相比暴力的 `O(n²)`，快了很多。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量 (`flip`, `ans`)；不依赖额外与输入规模相关的存储。  

---

## 心得  

- **核心技巧**：**利用翻转次数的奇偶性来“懒惰”地维护状态**，即**贪心 + 前缀翻转标记**。  
- 这种技巧常出现在需要对**后缀或前缀统一操作**的题目中，例如：  
  1. **“Bulb Switcher IV”**（同样是后缀翻转）  
  2. **“Minimum Number of Steps to Make Two Strings Equal”**（利用前缀翻转）  
  3. **“Flip Binary String to Make All Zeros”**（前缀翻转）  
- **一句话总结**：只要记录“已经翻转了多少次（奇偶）”，就能在 O(1) 空间内得到每个位置的真实值，从而得到最少操作次数。  

---

## 反思  

- **第一反应**：看到“翻转区间”就想“一次一次地真的去翻”，于是写出 O(n²) 的模拟代码。  
- **最容易踩的坑**：  
  - 忘记 **只需要关注奇偶**，导致不必要的数组拷贝或循环。  
  - 边界情况：全是 `0` 的字符串应返回 `0`（因为 `flip` 永远保持 `0`），如果不处理好会误计一次。  
- **下次遇到类似题**：第一步先思考“**翻转的影响是全局还是局部**”，如果是全局（后缀/前缀），就尝试用一个**标记位**记录累计的翻转次数，而不是逐个修改。这样往往能把时间复杂度从二次降到线性。