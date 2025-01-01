# #3006. 在给定数组中寻找美丽下标 I / Find Beautiful Indices in the Given Array I

> 难度：中等 · 标签：Two Pointers、String、Binary Search、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s, a string a, a string b, and an integer k.
An index i is beautiful if:
Return the array that contains beautiful indices in sorted order from smallest to largest.

**Examples**

**Example 1:**

```
Input: s = "isawsquirrelnearmysquirrelhouseohmy", a = "my", b = "squirrel", k = 15
Output: [16,33]
Explanation: There are 2 beautiful indices: [16,33].
- The index 16 is beautiful as s[16..17] == "my" and there exists an index 4 with s[4..11] == "squirrel" and |16 - 4| <= 15.
- The index 33 is beautiful as s[33..34] == "my" and there exists an index 18 with s[18..25] == "squirrel" and |33 - 18| <= 15.
Thus we return [16,33] as the result.
```

**Example 2:**

```
Input: s = "abcd", a = "a", b = "a", k = 4
Output: [0]
Explanation: There is 1 beautiful index: [0].
- The index 0 is beautiful as s[0..0] == "a" and there exists an index 0 with s[0..0] == "a" and |0 - 0| <= 4.
Thus we return [0] as the result.
```

**Constraints**

- 1 <= k <= s.length <= 105
- 1 <= a.length, b.length <= 10
- s, a, and b contain only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**

给定一个 0 基索引的字符串 `s`、一个字符串 `a`、一个字符串 `b`，以及一个整数 `k`。  
下标 `i` 若满足以下条件则称为 **美丽下标（beautiful index）**：

* `s[i .. i+|a|-1] == a` （即从下标 `i` 开始的子串（substring）恰好等于 `a`），并且  
* 存在某个下标 `j` 使得 `s[j .. j+|b|-1] == b` 且 `|i - j| <= k`。

返回所有美丽下标构成的数组，按从小到大排序。

**示例**

*示例 1*

```
输入: s = "isawsquirrelnearmysquirrelhouseohmy", a = "my", b = "squirrel", k = 15
输出: [16,33]
解释:
- 下标 16 为美丽下标，因为 s[16..17] == "my"，且存在下标 4 使得 s[4..11] == "squirrel"，且 |16 - 4| = 12 ≤ 15。
- 下标 33 为美丽下标，因为 s[33..34] == "my"，且存在下标 18 使得 s[18..25] == "squirrel"，且 |33 - 18| = 15 ≤ 15。
因此返回 [16,33]。
```

*示例 2*

```
输入: s = "abcd", a = "a", b = "a", k = 4
输出: [0]
解释:
唯一的美丽下标为 0，因为 s[0..0] == "a"，且存在下标 0 使得 s[0..0] == "a"，且 |0 - 0| = 0 ≤ 4。
所以返回 [0]。
```

**约束条件**

- `1 <= k <= s.length <= 10^5`
- `1 <= a.length, b.length <= 10`
- `s、a、b` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 i、j 都枚举一遍**：

1. 先遍历 `s`，找出所有满足 `s[i … i+len(a)-1] == a` 的下标 `i`（记为集合 **A**）。  
2. 再遍历 `s`，找出所有满足 `s[j … j+len(b)-1] == b` 的下标 `j`（记为集合 **B**）。  
3. 对 **A** 中的每一个 `i`，遍历 **B** 中的每一个 `j`，检查 `|i - j| ≤ k` 是否成立。只要有一个满足条件的 `j`，`i` 就是 “beautiful”。

> **类比**：  
> - 把 `A` 想成“所有符合条件的苹果”，`B` 想成“所有符合条件的香蕉”。  
> - 暴力做法就是把每个苹果和每根香蕉都配对一次，看看它们的距离（下标差）是否在 `k` 以内。

**为什么正确**：只要遍历了 **所有** 可能的 `(i, j)` 配对，就一定能发现满足条件的配对，因而不会漏掉任何一个 beautiful index。

**复杂度**  
- 找 `A`、`B` 的过程各是 O(|s|·|a|) / O(|s|·|b|)，但因为 `|a|、|b| ≤ 10`，可以视为 O(|s|)。  
- 核心的双层循环是 `|A| × |B|`，最坏情况下 `|A| ≈ |B| ≈ |s|`，于是时间复杂度 **O(n²)**（n = |s|）。  
- 只用了两个列表存下标，空间复杂度 **O(n)**。

> **大白话解释 O(n²)**：如果 `s` 长度是 10 000，那么暴力解要比较大约 1 亿 次（10 000 × 10 000），在电脑里跑会非常慢。

#### 代码（Python）

```python
def beautiful_indices_bruteforce(s: str, a: str, b: str, k: int):
    n = len(s)
    la, lb = len(a), len(b)

    # 1️⃣ 找出所有 a 出现的起始下标
    A = []
    for i in range(n - la + 1):
        if s[i:i + la] == a:          # 子串匹配
            A.append(i)

    # 2️⃣ 找出所有 b 出现的起始下标
    B = []
    for j in range(n - lb + 1):
        if s[j:j + lb] == b:
            B.append(j)

    # 3️⃣ 暴力检查每一对 (i, j)
    ans = []
    for i in A:                        # 遍历所有可能的 i
        beautiful = False
        for j in B:                    # 遍历所有可能的 j
            if abs(i - j) <= k:        # 距离满足 k
                beautiful = True
                break                  # 找到一个就可以停止内层循环
        if beautiful:
            ans.append(i)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - “n²” 表示如果字符串长度是 10 000，算法大约会执行 100 000 000 次比较，速度会很慢。
- **空间复杂度**：`O(n)`  
  - 只需要保存两个下标列表，最坏情况每个列表长度都接近 `n`。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于第 3 步：对每个 `i` 都要遍历全部 `j`。  
我们可以利用 **下标是有序的** 这一事实，把查找“距离在 k 以内的 j”变成 **区间查询**，从而把二重循环降到线性甚至对数级。

下面给出两种等价的实现思路，任选其一即可：

1. **二分查找（Binary Search）**  
   - `A`、`B` 本身已经是升序的（因为我们是从左到右扫描得到的）。  
   - 对每个 `i ∈ A`，在 `B` 中二分找出 **第一个 ≥ i‑k 的下标**。  
   - 只要这个下标对应的 `j` ≤ i + k，说明在 `[i‑k, i+k]` 区间内存在 `b`，`i` 就是 beautiful。  
   - 每次二分是 `O(log |B|)`，总时间 `O(|A|·log|B|) ≤ O(n·log n)`。

2. **双指针滑动窗口（Two Pointers）**  
   - 维护一个指针 `p` 指向 `B` 中的“左边界”。  
   - 随着 `i` 从左到右递增，`p` 只会向右移动（因为 `i‑k` 只会增大），所以整个过程是 **线性** 的。  
   - 对每个 `i`，只要检查 `B[p] ≤ i + k`（若 `p` 已经越界则不满足），即可判断是否 beautiful。  
   - 这一步的时间复杂度是 **O(n)**，空间仍是 `O(n)`。

下面用 **双指针** 方式实现，思路更直观，且无需额外的 `bisect` 模块。

> **类比**：  
> 想象 `A` 是一条跑道上的一批跑者，`B` 是另一批跑者。我们想知道每位 `A` 的跑者是否在 **k** 米的范围内有一位 `B` 的跑者。因为两批跑者都是按位置从左到右排好的，只需要让一只手指（指针）跟着 `B` 的跑者走，一遍扫描就能知道答案。

**关键步骤**：

1. **预处理**：一次遍历 `s`，分别记录所有 `a`、`b` 的出现位置，得到有序列表 `pos_a`、`pos_b`。  
2. **双指针遍历**：  
   - 初始化 `pb = 0`（指向 `pos_b` 的左端）。  
   - 对每个 `i`（遍历 `pos_a`）：  
     - 把 `pb` 向右移动，直到 `pos_b[pb] >= i - k`（保证窗口左边界不小于 `i - k`）。  
     - 检查当前 `pb` 是否仍在列表内且 `pos_b[pb] <= i + k`，若成立则把 `i` 加入答案。  
   - 由于 `pb` 只前进不后退，整体是 O(|s|)。

#### 代码（Python）

```python
def beautiful_indices(s: str, a: str, b: str, k: int):
    """
    返回所有 beautiful index，升序排列
    """
    n = len(s)
    la, lb = len(a), len(b)

    # ---------- 1. 预处理：找出所有 a、b 的起始下标 ----------
    pos_a = []          # a 出现的下标集合
    for i in range(n - la + 1):
        if s[i:i + la] == a:
            pos_a.append(i)

    pos_b = []          # b 出现的下标集合
    for i in range(n - lb + 1):
        if s[i:i + lb] == b:
            pos_b.append(i)

    # ---------- 2. 双指针滑动窗口 ----------
    ans = []
    pb = 0              # pos_b 的左指针，始终指向第一个 >= i - k 的位置

    for i in pos_a:                     # 按升序遍历所有可能的 i
        # 把 pb 推到满足 pos_b[pb] >= i - k 的位置
        while pb < len(pos_b) and pos_b[pb] < i - k:
            pb += 1

        # 此时若 pb 仍在范围内且 pos_b[pb] <= i + k，则 i 是 beautiful
        if pb < len(pos_b) and pos_b[pb] <= i + k:
            ans.append(i)

    return ans
```

> **代码要点解释**  
> - `while pb < len(pos_b) and pos_b[pb] < i - k:` 这行保证窗口左边界不小于 `i - k`，相当于把不可能的 `j` “踢出”窗口。  
> - `if pb < len(pos_b) and pos_b[pb] <= i + k:` 判断窗口右边界是否仍在合法范围内。若成立，说明在 `[i-k, i+k]` 区间里至少有一个 `b`，于是 `i` 被加入答案。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 预处理遍历 `s` 两次得到 `pos_a`、`pos_b`（各 O(n)）。  
  - 双指针遍历时 `pb` 只会向右移动至 `len(pos_b)`，所以整体也是线性。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **指数级**（比如 n=10⁵ 时，暴力解大约 10¹⁰ 次操作，而本解只有几万次）。
- **空间复杂度**：`O(n)`  
  - 需要保存两个下标列表，最坏情况每个列表长度接近 `n`。  
  - 额外的变量只有常数个，符合题目对空间的要求。

---

## 心得

- **核心技巧**：利用**有序下标 + 双指针（或二分）**把“在区间内是否存在元素”的问题从笛卡尔积降到线性/对数时间。  
- **适用的题型**  
  1. “在两组位置之间满足距离 ≤ k 的配对”——如 *Find Beautiful Indices in the Given Array II*。  
  2. “区间内是否出现某字符/子串”——如 *Maximum Number of Vowels in a Substring of Given Length*（滑动窗口）。  
  3. “在有序数组中找最近的满足条件的元素”——如 *Find Smallest Letter Greater Than Target*（二分搜索）。  
- **一句话总结**：**把离散的匹配位置视作有序序列，用指针/二分快速定位区间内的最近元素，即可将暴力 O(n²) 降到 O(n)。**

---

## 反思

- **第一反应**：看到“存在下标 j 满足 |i‑j| ≤ k”，立刻想到**枚举所有 i、j**，这就是暴力解。  
- **最容易踩的坑**  
  - **边界条件**：`i‑k` 可能小于 0，`i+k` 可能大于 `len(s)-1`，但因为我们只比较下标本身（不访问字符），不需要额外裁剪，只要在比较时使用原始下标即可。  
  - **子串长度**：`a`、`b` 长度不同，记得在遍历时用 `n - len + 1` 防止越界。  
  - **重复下标**：如果 `a` 与 `b` 相同，`i` 本身也可能是 `j`，代码已经自然兼容。  
- **下次遇到同类题**：  
  1. 先**把所有满足子串匹配的下标收集成有序列表**。  
  2. 再**思考如何在有序列表上做区间查询**（双指针/二分/滑动窗口）。  
  3. 只要能把“每个 i 检查所有 j”转化为“在有序序列中快速定位最近的 j”，时间复杂度就能大幅提升。