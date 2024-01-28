# #2564. 子串异或查询 / Substring XOR Queries

> 难度：中等 · 标签：Array、Hash Table、String、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/substring-xor-queries/)

---

## 题目（英文原版）

**Description**

You are given a binary string s, and a 2D integer array queries where queries[i] = [firsti, secondi].
For the ith query, find the shortest substring of s whose decimal value, val, yields secondi when bitwise XORed with firsti. In other words, val ^ firsti == secondi.
The answer to the ith query is the endpoints (0-indexed) of the substring [lefti, righti] or [-1, -1] if no such substring exists. If there are multiple answers, choose the one with the minimum lefti.
Return an array ans where ans[i] = [lefti, righti] is the answer to the ith query.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "101101", queries = [[0,5],[1,2]]
Output: [[0,2],[2,3]]
Explanation: For the first query the substring in range [0,2] is "101" which has a decimal value of 5, and 5 ^ 0 = 5, hence the answer to the first query is [0,2]. In the second query, the substring in range [2,3] is "11", and has a decimal value of 3, and 3 ^ 1 = 2. So, [2,3] is returned for the second query.
```

**Example 2:**

```
Input: s = "0101", queries = [[12,8]]
Output: [[-1,-1]]
Explanation: In this example there is no substring that answers the query, hence [-1,-1] is returned.
```

**Example 3:**

```
Input: s = "1", queries = [[4,5]]
Output: [[0,0]]
Explanation: For this example, the substring in range [0,0] has a decimal value of 1, and 1 ^ 4 = 5. So, the answer is [0,0].
```

**Constraints**

- 1 <= s.length <= 104
- s[i] is either '0' or '1'.
- 1 <= queries.length <= 105
- 0 <= firsti, secondi <= 109

---

## 题目（中文翻译）

You are given a binary string `s`, and a 2D integer array `queries` where `queries[i] = [first_i, second_i]`.  
For the *i*‑th query, find the shortest **substring**（子串） of `s` whose decimal value, `val`, yields `second_i` when bitwise XOR（异或）ed with `first_i`. In other words, `val ^ first_i == second_i`.  
The answer to the *i*‑th query is the endpoints (0‑indexed) of the substring `[left_i, right_i]` or `[-1, -1]` if no such substring exists. If there are multiple answers, choose the one with the minimum `left_i`.  
Return an array `ans` where `ans[i] = [left_i, right_i]` is the answer to the *i*‑th query.  
A **substring**（子串） is a contiguous non‑empty sequence of characters within a string.

**Example 1:**  
**Input:** `s = "101101"`, `queries = [[0,5],[1,2]]`  
**Output:** `[[0,2],[2,3]]`  
**Explanation:**  
- For the first query the substring in range `[0,2]` is `"101"` which has a decimal value of `5`, and `5 ^ 0 = 5`, hence the answer to the first query is `[0,2]`.  
- In the second query, the substring in range `[2,3]` is `"11"`, which has a decimal value of `3`, and `3 ^ 1 = 2`. So `[2,3]` is returned for the second query.

**Example 2:**  
**Input:** `s = "0101"`, `queries = [[12,8]]`  
**Output:** `[[-1,-1]]`  
**Explanation:** In this example there is no substring that satisfies the query, therefore `[-1,-1]` is returned.

**Example 3:**  
**Input:** `s = "1"`, `queries = [[4,5]]`  
**Output:** `[[0,0]]`  
**Explanation:** For this example, the substring in range `[0,0]` has a decimal value of `1`, and `1 ^ 4 = 5`. So the answer is `[0,0]`.

**Constraints:**
- `1 <= s.length <= 10^4`
- `s[i]` is either `'0'` or `'1'`.
- `1 <= queries.length <= 10^5`
- `0 <= first_i, second_i <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **对每个查询**，把字符串 `s` 的所有可能子串都枚举出来，算出它们对应的十进制值 `val`，检查  
`val ^ first == second` 是否成立。  

- **数据结构**：我们只需要一个普通的整数变量来保存当前子串的十进制值，遍历时不断左移并加上新位。  
  - 把二进制字符看成 **“灯泡”**，左边的灯泡亮了以后，右边再亮一个灯泡，相当于把已有的数字左移一位（乘以 2）再加上新灯泡的状态（0 或 1）。  
- **正确性**：因为我们把 **所有** 子串都检查了一遍，只要存在满足条件的子串，必定能在枚举过程中被发现。若有多个符合的子串，按照题目要求返回左端点最小的那一个，只需要在遍历时记录下最早出现的即可。

#### 代码（Python）

```python
def substringXorQueries_bruteforce(s: str, queries):
    n = len(s)
    ans = []

    for first, second in queries:
        target = first ^ second               # 我们希望子串的十进制值等于 target
        best = (-1, -1)                       # 先记成不存在

        # 枚举所有子串
        for left in range(n):
            val = 0
            for right in range(left, n):
                # 把 s[right] 加到二进制数的末尾
                val = (val << 1) + (s[right] == '1')
                if val == target:            # 找到匹配
                    best = (left, right)     # 只要第一次找到，就是左端点最小的
                    break                    # 当前 left 已经找到最短子串，跳出内层循环
            if best[0] != -1:                 # 已经找到答案，直接结束外层循环
                break

        ans.append([best[0], best[1]])

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(q * n²)`  
  - `q` 是查询数量，`n` 是字符串长度。对每个查询我们要遍历所有 `O(n²)` 个子串。  
  - 用大白话说，就是如果 `s` 长 10 000，`q` 是 100 000，最坏情况要做 10⁴×10⁴×10⁵ 次循环，根本跑不完。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用常数级的变量存当前子串的值，没有额外的存储。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每个查询都要重新遍历全部子串。我们可以把“所有子串的十进制值”提前算好，保存到哈希表（字典）里，这样每个查询只需要一次 **O(1)** 的查找。

**关键观察 1：**  
`first`、`second` 的取值上限是 `10⁹`，而 `10⁹ < 2³⁰`。这说明 **只要子串的长度不超过 30 位，它的十进制值就一定 ≤ 2³⁰‑1 ≤ 10⁹**。长度更长的子串对应的数一定会超出查询范围，根本不可能是答案。

**关键观察 2：**  
我们只需要记录 **“最左端点最小的子串”**。遍历 `s` 时，如果同一个十进制值出现多次，只保留第一次出现的左端点（以及对应的右端点），后面的就可以忽略。

**实现步骤**

1. **预处理**  
   - 对每个起点 `i`（0 ≤ i < n），最多向右扩展 30 位，累计二进制数 `val`。  
   - 把 `val` 作为键，`(i, j)`（左、右端点）作为值，存进字典 `best_pos`。如果 `val` 已经在字典里，直接跳过，因为已经有更左的起点。  
   - 这一步的复杂度是 `O(n * 30)`，因为每个起点最多检查 30 次。

2. **回答查询**  
   - 对每个 `[first, second]`，计算 `target = first ^ second`。  
   - 在 `best_pos` 中查找 `target`：若存在，直接返回对应的端点；否则返回 `[-1, -1]`。  

这样每个查询只需要一次哈希查找，时间几乎是常数。

#### 代码（Python）

```python
def substringXorQueries(s: str, queries):
    n = len(s)
    best_pos = {}                     # val -> (left, right)

    # ---------- 预处理所有长度 ≤ 30 的子串 ----------
    for left in range(n):
        val = 0
        # 只需要向右看最多 30 位
        for right in range(left, min(n, left + 30)):
            # 左移一位并加上当前字符是否为 '1'
            val = (val << 1) + (s[right] == '1')
            # 只记录第一次出现的位置（左端点最小）
            if val not in best_pos:
                best_pos[val] = (left, right)

    # ---------- 逐个查询 ----------
    ans = []
    for first, second in queries:
        target = first ^ second        # 需要的子串十进制值
        if target in best_pos:
            l, r = best_pos[target]
            ans.append([l, r])
        else:
            ans.append([-1, -1])

    return ans
```

> **注释要点**  
> - `s[right] == '1'` 在 Python 中会得到 `True/False`，在算数运算时会被自动转成 `1/0`，非常方便。  
> - `min(n, left + 30)` 确保不会越界。  
> - 字典的 `in` 操作是 **哈希表**，可以类比成 **“查字典”**：键是单词（这里是十进制值），值是对应的页码（子串左右端点）。

#### 复杂度  

- **时间复杂度**：`O(n * 30 + q)` → 简写为 `O(n + q)`（因为 30 是常数）。  
  - 预处理遍历 `n` 次，每次最多 30 步；查询只做一次哈希查找。相比暴力的 `O(q * n²)`，快了几个数量级。  
- **空间复杂度**：`O(n * 30)` → 实际上最多存 `n * 30` 条记录，但每条记录只是一对整数，最多约 `3·10⁵` 条（因为 `n ≤ 10⁴`），远小于 `10⁹`。  
  - 用大白话说，就是我们只需要把 **所有“短子串”** 的信息记下来，空间开销在几百 KB 级别，完全可以接受。

---

## 心得

- **核心技巧**：利用数值上限（`≤ 10⁹`）限制子串长度，只预处理长度不超过 30 的子串；再用哈希表一次性保存最左出现位置，实现 **“查询 O(1)”**。  
- **适用场景**  
  1. “子串/子数组值在一定范围内” 的问题（如 **Maximum XOR of Two Numbers in an Array** 中的位数限制）。  
  2. 需要对大量查询做**离线预处理** 的场景（如 **Range Sum Queries**、**Palindrome Queries**）。  
- **一句话总结**：**把“所有可能的答案”提前算好、用哈希表记住最左位置，查询时直接查表即可**。

---

## 反思

- **第一反应**：看到“子串的十进制值”和“XOR”就想逐个枚举子串，检查 `val ^ first == second`。  
- **最容易踩的坑**  
  - 忘记 **子串长度上限**，导致预处理的时间和空间爆炸。  
  - 计算十进制值时没有及时截断，可能会产生非常大的整数，影响性能。  
  - 对同一 `val` 保存了更右的子串，导致答案不满足 “左端点最小”。  
- **下次类似题的第一步**：先思考 **数值范围** 是否能把搜索空间压到常数级（比如位数、和的上限），再决定是否可以 **离线预处理** 并使用哈希表/字典快速查询。