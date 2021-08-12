# #1433. 检查一个字符串能否打败另一个字符串 / Check If a String Can Break Another String

> 难度：中等 · 标签：String、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/check-if-a-string-can-break-another-string/)

---

## 题目（英文原版）

**Description**

Given two strings: s1 and s2 with the same size, check if some permutation of string s1 can break some permutation of string s2 or vice-versa. In other words s2 can break s1 or vice-versa.
A string x can break string y (both of size n) if x[i] >= y[i] (in alphabetical order) for all i between 0 and n-1.

**Examples**

**Example 1:**

```
Input: s1 = "abc", s2 = "xya"
Output: true
Explanation: "ayx" is a permutation of s2="xya" which can break to string "abc" which is a permutation of s1="abc".
```

**Example 2:**

```
Input: s1 = "abe", s2 = "acd"
Output: false 
Explanation: All permutations for s1="abe" are: "abe", "aeb", "bae", "bea", "eab" and "eba" and all permutation for s2="acd" are: "acd", "adc", "cad", "cda", "dac" and "dca". However, there is not any permutation from s1 which can break some permutation from s2 and vice-versa.
```

**Example 3:**

```
Input: s1 = "leetcodee", s2 = "interview"
Output: true
```

**Constraints**

- s1.length == n
- s2.length == n
- 1 <= n <= 10^5
- All strings consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个等长的字符串 `s1` 和 `s2`，判断是否存在 `s1` 的某个排列（permutation）能够 **打败**（break）`s2` 的某个排列，或 `s2` 的某个排列能够 **打败**（break）`s1` 的某个排列。  
换句话说，`s2` 能打败 `s1`，或 `s1` 能打败 `s2`。

如果两个长度均为 `n` 的字符串 `x` 与 `y` 满足 `x[i] >= y[i]`（按字母序比较）对所有 `0 ≤ i ≤ n‑1` 成立，则称 `x` 能打败（break）`y`。

---

### 示例

**示例 1**  
Input: `s1 = "abc"`, `s2 = "xya"`  
Output: `true`  
**解释**：`"ayx"` 是 `s2="xya"` 的一种排列（permutation），它能够打败字符串 `"abc"`，而 `"abc"` 正是 `s1="abc"` 的一种排列（permutation）。

**示例 2**  
Input: `s1 = "abe"`, `s2 = "acd"`  
Output: `false`  
**解释**：`s1="abe"` 的所有排列为 `"abe"`, `"aeb"`, `"bae"`, `"bea"`, `"eab"` 和 `"eba"`；`s2="acd"` 的所有排列为 `"acd"`, `"adc"`, `"cad"`, `"cda"`, `"dac"` 和 `"dca"`。然而，没有任意一个 `s1` 的排列能够打败 `s2` 的某个排列，反之亦然。

**示例 3**  
Input: `s1 = "leetcodee"`, `s2 = "interview"`  
Output: `true`

---

### 约束条件

- `s1.length == n`
- `s2.length == n`
- `1 <= n <= 10^5`
- 所有字符串仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两条字符串的所有排列全部枚举出来，然后两两比较：

1. 先把 `s1` 的所有可能排列列成一个列表（就像把一本书的所有章节顺序都换一种排法）。
2. 再把 `s2` 的所有可能排列也列出来。
3. 对每一对排列 `(p1, p2)`，检查对应位置的字符是否满足 `p1[i] >= p2[i]`（即 `p1` 能 “break” `p2`），或者相反的方向 `p2[i] >= p1[i]`。

> **类比**：把每个排列想象成一本词典的不同装订顺序，想要找出一种装订方式，使得在同一页码上，左边的词（字符）总是字典序不小于右边的词。

这个方法 **一定正确**，因为我们把所有可能的排列都穷举了，只要存在满足条件的组合，就一定会被检查到。

但是穷举所有排列的代价非常大：

- 长度为 `n` 的字符串有 `n!`（阶乘）种不同的排列。  
- 对每一对排列我们还要比较 `n` 次字符。

所以时间复杂度是 **O(n! × n!)**（更准确地说是 O((n!)²·n)），即使 `n = 10`，`10! = 3,628,800`，已经远远超过机器的计算能力。

#### 代码（Python）

```python
import itertools

def can_break_brute(s1: str, s2: str) -> bool:
    """
    暴力枚举所有排列并两两比较
    """
    # 生成所有排列，itertools.permutations 返回的是元组，需要 join 成字符串
    perms1 = {''.join(p) for p in itertools.permutations(s1)}
    perms2 = {''.join(p) for p in itertools.permutations(s2)}

    # 检查任意一对排列是否满足 “break” 条件
    for p1 in perms1:
        for p2 in perms2:
            # p1 break p2 ?
            if all(c1 >= c2 for c1, c2 in zip(p1, p2)):
                return True
            # p2 break p1 ?
            if all(c2 >= c1 for c1, c2 in zip(p1, p2)):
                return True
    return False

# 示例（仅用于小规模测试，实际 n 较大时会超时）
print(can_break_brute("abc", "xya"))   # True
print(can_break_brute("abe", "acd"))   # False
```

> **注意**：上面的代码只能在 `n` 很小（比如 ≤ 8）时跑得完，真正的 LeetCode 数据规模可以达到 `10⁵`，因此必须寻找更快的办法。

#### 复杂度  

- **时间复杂度**：`O((n!)²·n)` —— 解释：`n!` 是排列数，两个集合各有 `n!` 种，遍历所有配对需要 `(n!)²` 次，每次比较 `n` 个字符。这个数量在实际中几乎是不可接受的。
- **空间复杂度**：`O(n!·n)` —— 需要把所有排列存进集合里，最坏情况下需要存 `n!` 条长度为 `n` 的字符串。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们把所有排列都列出来。实际上我们并不需要真的去排列，只要比较 **字符的相对大小** 即可。关键观察如下：

1. **排序会把字符从小到大排列**。如果我们把 `s1` 和 `s2` 各自排序得到 `a`、`b`，那么任意一个排列的字符序列在对应位置上一定不会比排好序的序列更“小”。换句话说，**最小的可能排列就是排序后的序列**，最大的可能排列也是排序后的序列（只不过是从大到小，但我们只关心相对大小）。
2. 因此，只要检查两条排好序的序列之间的大小关系，就能判断是否存在满足条件的排列：
   - 如果对所有 `i`，`a[i] >= b[i]` 成立，则 **`a`（即 `s1` 的某个排列）可以 break `b`（`s2` 的某个排列）**。
   - 同理，如果对所有 `i`，`b[i] >= a[i]` 成立，则 `s2` 可以 break `s1`。
3. 如果两者都不成立，则不存在任何排列能满足 “break” 条件。

> **类比**：把两堆字母想象成两列排好序的盒子。只要左边每个盒子的字母不小于右边对应盒子的字母（或者反过来），我们就能把左列的盒子搬到右列上方，保持每个位置的字母不小于对应的。因为盒子已经按大小排好序，搬动时不需要再去打乱顺序。

**核心技巧**：**排序 + 贪心比较**。排序把问题从 “所有排列” 降维到 “只比较一次”。这正是本题的“Greedy（贪心）”标签所在。

#### 代码（Python）

```python
def check_if_can_break(s1: str, s2: str) -> bool:
    """
    最优解：先排序，再用一次遍历比较大小
    """
    # 将两个字符串转成列表并排序，得到从小到大的字符序列
    a = sorted(s1)          # a[i] 表示 s1 排序后第 i 小的字符
    b = sorted(s2)          # b[i] 表示 s2 排序后第 i 小的字符

    # 检查 a 是否可以 break b
    can_a_break_b = all(c1 >= c2 for c1, c2 in zip(a, b))
    # 检查 b 是否可以 break a
    can_b_break_a = all(c2 >= c1 for c1, c2 in zip(a, b))

    # 只要有一种情况成立，就返回 True
    return can_a_break_b or can_b_break_a

# ---- 示例 ----
print(check_if_can_break("abc", "xya"))        # True
print(check_if_can_break("abe", "acd"))        # False
print(check_if_can_break("leetcodee", "interview"))  # True
```

> **关键行解释**  
> - `sorted(s1)`：把字符串的字符按字母顺序排好，等价于把字典装进了从小到大的抽屉。  
> - `all(c1 >= c2 for c1, c2 in zip(a, b))`：一次遍历把对应位置的字符做比较，`all` 会在发现不满足的情况时立即返回 `False`，这就是 **贪心**——只要有一次违背就不可能整体满足。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `sorted` 的时间是 `O(n log n)`（因为要把 `n` 个字符排序），后面的遍历是 `O(n)`，整体受排序主导。  
  - 与暴力解的 `O((n!)²·n)` 相比，已经从“天文数字”降到“几乎线性”，在 `n = 10⁵` 时也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 排序会产生两个新列表，各占 `n` 个字符的空间。除了这两个列表，算法本身使用常数级额外空间。

---

## 心得

- **核心技巧**：先排序再一次遍历比较大小（贪心 + 排序）。
- **适用的题型**：  
  1. “两个数组/字符串能否逐位比较大小” 如 LeetCode 1652. Defuse the Bomb（数组逐位比较）  
  2. “能否把一个序列重新排列，使得满足某种单调关系” 如 1124. Longest Well‑Performing Interval（单调栈）  
  3. “字符或数字的排列是否满足某种相对大小” 如 1640. Check Array Formation Through Concatenation（排序后比较）
- **一句话总结**：**把所有可能的排列压缩到“排好序的唯一形态”，再用一次贪心比较即可**。

---

## 反思

- **第一反应**：直接想到穷举所有排列，因为题目提到了“任意排列”。这会让人不自觉地走向暴力搜索。
- **最容易踩的坑**：  
  - 忽略了 **字符串长度相同** 的前提，直接比较不同长度会出错。  
  - 只检查 `s1` 排序后是否能 break `s2`，忘记了 “或 vice‑versa”。两种方向都必须验证。  
  - 对字符比较的大小理解错误（比如把 `'a'` 当作数字 0 而不是 ASCII 码），导致 `>=` 条件写反。
- **下次思路**：遇到“任意排列”+“逐位比较”这种描述时，第一步就想到 **先排序**，因为排序是把所有排列压缩到唯一的有序形态，随后再做 **一次遍历的贪心检查**。这样可以立刻把复杂度从指数级降到 `O(n log n)`。