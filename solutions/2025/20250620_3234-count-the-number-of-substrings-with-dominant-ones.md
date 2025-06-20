# #3234. 统计主导 1 的子串数量 / Count the Number of Substrings With Dominant Ones

> 难度：中等 · 标签：String、Sliding Window、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-substrings-with-dominant-ones/)

---

## 题目（英文原版）

**Description**

You are given a binary string s.
Return the number of substrings with dominant ones.
A string has dominant ones if the number of ones in the string is greater than or equal to the square of the number of zeros in the string.

**Examples**

**Example 1:**

```
Input: s = "00011"
Output: 5
Explanation:
The substrings with dominant ones are shown in the table below.
```

**Example 2:**

```
Input: s = "101101"
Output: 16
Explanation:
The substrings with non-dominant ones are shown in the table below.
Since there are 21 substrings total and 5 of them have non-dominant ones, it follows that there are 16 substrings with dominant ones.
```

**Constraints**

- 1 <= s.length <= 4 * 104
- s consists only of characters '0' and '1'.

---

## 题目（中文翻译）

**描述**  
给定一个二进制字符串 `s`。  
返回具有主导 1 的子串（substring）的数量。  

如果一个字符串中 `1` 的数量 **大于等于** `0` 的数量的平方，则该字符串拥有主导 1。

**示例 1**  
```text
输入: s = "00011"
输出: 5
解释:
具有主导 1 的子串如下表所示。
```

**示例 2**  
```text
输入: s = "101101"
输出: 16
解释:
具有非主导 1 的子串如下表所示。由于所有子串共有 21 个，其中有 5 个不具备主导 1，因此剩余 16 个子串具备主导 1。
```

**约束条件**  

- $1 \leq s.\text{length} \leq 4 \times 10^{4}$
- $s$ 仅由字符 `'0'` 和 `'1'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **枚举所有子串**，然后检查它是否满足 “1 的个数 ≥ (0 的个数)²”。  

- **枚举子串**：把左边界 `l` 从 `0` 到 `n-1`，右边界 `r` 从 `l` 到 `n-1`，每一对 `(l, r)` 就对应一个子串 `s[l..r]`。  
- **统计 0/1**：在遍历子串的过程中，用两个计数器 `cnt0`、`cnt1` 分别记录出现的 `0` 和 `1` 的个数。  
- **判断支配性**：只要 `cnt1 >= cnt0 * cnt0`（注意是平方），就把答案加一。

> **类比**：把字符串想成一本书，子串就是从第 `l` 页翻到第 `r` 页的内容。我们要把每一种翻页方式都试一遍，看看这段文字里 “1” 的数量是否不少于 “0” 的平方。

> **为什么正确**：因为我们把**所有**可能的子串都检查了一遍，凡是满足条件的必然被计数，凡是不满足的必然被排除。

#### 代码（Python）

```python
def countDominant(s: str) -> int:
    n = len(s)
    ans = 0

    # 枚举左端点 l
    for l in range(n):
        cnt0 = cnt1 = 0               # 统计当前子串的 0、1 个数
        # 枚举右端点 r（逐步扩展子串）
        for r in range(l, n):
            if s[r] == '0':
                cnt0 += 1
            else:
                cnt1 += 1

            # 判断支配性：1 的个数 ≥ (0 的个数)²
            if cnt1 >= cnt0 * cnt0:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层最坏也要遍历 `n` 次，整体是 “n 的平方”。如果把 `n=10,000` 代入，约等于一亿次操作，普通电脑跑会比较慢。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数计数器，和字符串长度无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每个左端点都要遍历所有右端点**，导致 `O(n²)`。  
观察条件 `cnt1 >= cnt0²`，可以得到以下关键事实：

1. **0 的个数不能太多**  
   - 若 `cnt0 = z`，则至少需要 `cnt1 ≥ z²`。  
   - 整个子串长度 `len = cnt1 + z ≥ z² + z`。  
   - 当 `z` 超过 `√n`（`n` 为字符串长度）时，`z² + z > n`，根本不可能在长度为 `n` 的字符串里出现。  
   - **结论**：任意满足支配性的子串，内部的 `0` 最多只有 `√n` 个。

2. **把子串划分为 “0 的位置” 与 “0 之间的 1”**  
   - 记下所有 `0` 出现的下标，形成数组 `zero_pos`（类似字典里查词的“页码”，下标就是页码）。  
   - 对每个左端点 `l`，只需要看 **后面最多 `√n` 个零** 的位置，枚举这些零作为子串的**最右侧零**。  

3. **如何从“最右侧零”推出合法的右端点**  
   - 假设从左端点 `l` 往右数第 `k` 个零的位置是 `pos`（`k` 从 `1` 开始计数），此时子串里已经有 `k` 个零。  
   - 为了让 `1` 的数量满足 `cnt1 ≥ k²`，子串的最小长度必须是 `k² + k`（因为最少要 `k²` 个 `1` 再加 `k` 个 `0`）。  
   - 因此右端点 `r` 至少要满足 `r ≥ l + k² + k - 1`。  
   - 同时右端点必须不早于最右侧零 `pos`，否则零会超出子串。  
   - 综上，合法的最小右端点是 `need = max(pos, l + k² + k - 1)`。  
   - 只要 `need < n`，从 `need` 到字符串结尾的每个位置都是合法的右端点，贡献 `n - need` 个子串。

4. **全是 1 的子串**  
   - 当子串里 **没有零** 时，条件始终成立（因为 `0² = 0`）。  
   - 我们只需统计所有连续 `1` 组成的段的子串数，段长为 `len` 时贡献 `len * (len + 1) // 2`。

> **类比**：把零看成“障碍物”，我们只关心离左端点最近的若干个障碍物（不超过 `√n` 个）。一旦确定了最右边的障碍物，后面再往右加的都是 “安全区域”，因为再加入的字符只能是 `1`，只会让 `1` 的数量更多，条件仍然满足。

#### 代码（Python）

```python
import math

def countDominant(s: str) -> int:
    n = len(s)
    ans = 0

    # ---------- 1. 统计全部为 1 的子串 ----------
    i = 0
    while i < n:
        if s[i] == '1':
            j = i
            while j < n and s[j] == '1':
                j += 1
            length = j - i                 # 连续 1 的长度
            ans += length * (length + 1) // 2   # 子串个数公式
            i = j
        else:
            i += 1

    # ---------- 2. 预处理零的下标 ----------
    zero_pos = [idx for idx, ch in enumerate(s) if ch == '0']
    m = len(zero_pos)

    # ---------- 3. 枚举左端点 ----------
    B = int(math.sqrt(n)) + 1               # 最多多少个零需要枚举
    for l in range(n):
        # 在 zero_pos 中找到第一个 >= l 的零的下标位置
        # 使用二分搜索提高到 O(log n)（这里用 Python 的 bisect）
        import bisect
        start = bisect.bisect_left(zero_pos, l)

        # 枚举从左端点 l 开始看到的前 B 个零
        for k in range(1, B + 1):
            if start + k - 1 >= m:          # 已经没有这么多零了
                break
            pos = zero_pos[start + k - 1]   # 第 k 个零的位置（最右侧零）

            # 需要的最小右端点，使得 1 的数量 ≥ k²
            need_len = k * k + k            # 最短长度 = k² + k
            need_r = l + need_len - 1       # 对应的右端点下标
            need = max(pos, need_r)         # 必须同时满足两条要求

            if need < n:
                ans += n - need              # 从 need 到 n-1 都合法

    return ans
```

> **代码说明**  
- 第 1 部分统计全是 `1` 的子串，时间 `O(n)`。  
- 第 2 部分把所有 `0` 的下标存进列表，后面可以 **快速定位**。  
- 第 3 部分对每个左端点 `l`，只检查最多 `√n`（约 200）个零，整体时间 `O(n·√n)`。  
- 使用 `bisect_left` 在 `zero_pos` 中找第一个不小于 `l` 的零，保证每次枚举都是从正确位置开始。

#### 复杂度

- **时间复杂度**：`O(n·√n)`  
  - `√n` 大约是 200（因为 `n ≤ 4·10⁴`），所以最坏约 `8·10⁶` 次基本操作，能够在毫秒级通过。  
  - 与暴力的 `O(n²)`（约 `1.6·10⁹`）相比，快了 **两个数量级**。

- **空间复杂度**：`O(n)`（仅存 `zero_pos` 列表）  
  - 只用了线性额外空间，和输入长度同阶。  

---

## 心得

- **核心技巧**：利用条件 `ones ≥ zeros²` 推导出 “零的个数至多 √n”，从而把 **全局枚举** 转化为 **局部枚举**（每个左端点只看有限个零）。  
- **适用场景**：  
  1. 条件里出现 **平方 / 指数** 之类的函数，使得某类元素的数量被上界限制（如 “`sum ≥ count²`”）。  
  2. 需要统计满足某种不等式的子数组/子串时，可先 **限定关键元素的最大出现次数**，再枚举。  
  3. 类似的题目还有 “**Count Subarrays with Median K**” 中的 “限定奇数个数上界” 方案。  
- **一句话总结**：**把“稀有元素”数量压到 √n，枚举这些稀有元素而不是全部子串**，即可把二次暴力降到准线性。

---

## 反思

- **第一反应**：直接枚举所有子串，逐个计数。  
- **最容易踩的坑**：  
  - 忽略 **全 1 子串** 的特殊情况，导致答案少计。  
  - 计算 `need_len = k*k + k` 时忘记减一导致右端点越界。  
  - 对于 `0` 的位置搜索，如果用线性遍历会把时间复杂度拉回 `O(n·√n·√n)`，需要二分或指针移动保持 `O(1)` 逐步推进。  
- **下次类似题的第一步**：  
  - 先**分析不等式**，看是否能把某类字符的出现次数上界化（如 `≤ √n`），然后**只枚举这些关键字符**，其余字符随意扩展即可。