# #3106. 受约束操作后的字典序最小字符串 / Lexicographically Smallest String After Operations With Constraint

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-string-after-operations-with-constraint/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k.
Define a function distance(s1, s2) between two strings s1 and s2 of the same length n as:
For example, distance("ab", "cd") == 4, and distance("a", "z") == 1.
You can change any letter of s to any other lowercase English letter, any number of times.
Return a string denoting the lexicographically smallest string t you can get after some changes, such that distance(s, t) <= k.

**Examples**

**Example 1:**

```
Input: s = "zbbz", k = 3
Output: "aaaz"
Explanation:
Change s to "aaaz" . The distance between "zbbz" and "aaaz" is equal to k = 3 .
```

**Example 2:**

```
Input: s = "xaxcd", k = 4
Output: "aawcd"
Explanation:
The distance between "xaxcd" and "aawcd" is equal to k = 4.
```

**Example 3:**

```
Input: s = "lol", k = 0
Output: "lol"
Explanation:
It's impossible to change any character as k = 0 .
```

**Constraints**

- 1 <= s.length <= 100
- 0 <= k <= 2000
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s` 和一个整数 `k`。  
定义两个等长字符串 `s1`、`s2`（长度为 `n`）之间的函数 `distance(s1, s2)` 为：

- 对于每个位置 `i（0 ≤ i < n）`，记字符 `c1 = s1[i]`、`c2 = s2[i]`。  
- 设它们在字母表中的序号分别为 `pos(c1)`、`pos(c2)`（`a` 为 0，`b` 为 1，…，`z` 为 25）。  
- 该位置的距离为 `min(|pos(c1) - pos(c2)|, 26 - |pos(c1) - pos(c2)|)`。  
- `distance(s1, s2)` 为所有位置距离的总和。

例如，`distance("ab", "cd") == 4`，`distance("a", "z") == 1`。

你可以将 `s` 中的任意字符改成任意其他小写英文字母，次数不限。  
返回在若干次修改后得到的字典序最小字符串 `t`，要求满足 `distance(s, t) ≤ k`。

---

**示例**

**示例 1**  
```text
Input: s = "zbbz", k = 3
Output: "aaaz"
Explanation:
将 s 改为 "aaaz"。此时 "zbbz" 与 "aaaz" 的 distance 等于 k = 3。
```

**示例 2**  
```text
Input: s = "xaxcd", k = 4
Output: "aawcd"
Explanation:
"xaxcd" 与 "aawcd" 的 distance 等于 k = 4。
```

**示例 3**  
```text
Input: s = "lol", k = 0
Output: "lol"
Explanation:
因为 k = 0，无法进行任何字符的修改。
```

---

**约束条件**

- `1 ≤ s.length ≤ 100`
- `0 ≤ k ≤ 2000`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的目标字符串 t 都列举出来**，然后计算每个 t 与原字符串 s 的距离 `distance(s, t)`，挑选出满足 `distance ≤ k` 且字典序最小的那个。  

- **数据结构**：我们可以把每个候选字符串当作一个长度为 `n` 的字符数组。  
  - 类比：把所有可能的字符串想成一本巨大的“字典”，每一页（`t`）都是一种组合。  
- **为什么正确**：因为我们遍历了**全部**合法的 t，必然不会错过最小的那个。  
- **复杂度分析**：  
  - 每个位置有 26 种字母，字符串长度为 `n`，所以候选数量是 `26ⁿ`（指数级）。  
  - 对每个候选我们要遍历 `n` 个字符计算距离，时间是 `O(n)`。  
  - 综合下来时间是 `O(n·26ⁿ)`，空间只需要保存当前枚举的字符串 `O(n)`。  
  - 用大白话说，**当 n=5 时**候选数已经是 `≈ 1.2×10⁷`，远远超出普通电脑的计算能力。  

> 这就是为什么暴力解只能用来“验证思路”，而不是正式提交的答案。

#### 代码（Python）

```python
import itertools

def char_dist(c1: str, c2: str) -> int:
    """单个字符的循环距离，例如 'a' 与 'z' 的距离是 1"""
    diff = abs(ord(c1) - ord(c2))
    return min(diff, 26 - diff)          # 取顺时针或逆时针的较小值

def distance(s: str, t: str) -> int:
    """两个等长字符串的总距离"""
    return sum(char_dist(a, b) for a, b in zip(s, t))

def brute_force(s: str, k: int) -> str:
    n = len(s)
    best = None                           # 用来保存当前最小的合法字符串
    # itertools.product 会产生所有长度为 n 的字母组合
    for chars in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=n):
        t = ''.join(chars)
        if distance(s, t) <= k:           # 只关注满足约束的 t
            if best is None or t < best: # 字典序比较
                best = t
    return best if best is not None else s   # 若没有合法解，返回原串（题目保证一定有解）
```

> 代码可以直接运行，但仅适用于 `n` 很小的测试（比如 `n ≤ 4`），否则会卡死。

#### 复杂度

- **时间复杂度**：`O(n·26ⁿ)` —— 随着字符串长度指数级增长，几乎不可接受。  
- **空间复杂度**：`O(n)` —— 只保存当前枚举的字符串和常数级的辅助变量。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈在于“枚举所有可能”**。我们注意到：

1. **距离是可加的**：`distance(s, t) = Σ distance(s[i], t[i])`。每个字符的贡献是独立的，只要累计的总和不超过 `k` 即可。  
2. **想要字典序最小**，我们应该**尽可能把左侧字符改成 `'a'`**（因为 `'a'` 是字母表里最小的）。  
3. **剩余的 k 只会在后面的字符上消耗**，所以只要当前字符的改动消耗不超过剩余的 `k`，我们就可以把它定下来，然后把剩余的 `k` 交给后面的字符继续处理。  

于是可以采用**贪心**策略：

- 从左到右遍历每个位置 `i`。  
- 对字母表 `'a' … 'z'` 按顺序尝试：  
  - 计算把 `s[i]` 改成该字母需要的距离 `need = char_dist(s[i], ch)`。  
  - 若 `need ≤ remaining_k`，则把 `t[i] = ch`，并把 `remaining_k -= need`，**立刻确定该字符**，跳到下一个位置。  
- 当 `remaining_k` 用完或遍历完所有字符时，得到的 `t` 已经是字典序最小的合法答案。  

> 为什么这个贪心是正确的？  
> - **局部最优 → 全局最优**：在当前位置，选最小的能够满足约束的字符，不会影响后面字符的可行性，因为后面最多还能使用剩余的 `k`（它是非负的）。  
> - **不存在更好选择**：如果我们在某位置选了更大的字母 `ch'`（`ch' > ch`），则必然导致整个字符串字典序更大，且不会为后面节省任何 `k`（因为两者的 `need` 都已经 ≤ 剩余 `k`），所以不会得到更小的答案。  

#### 代码（Python）

```python
def char_dist(c1: str, c2: str) -> int:
    """单字符循环距离，'a' 与 'z' 的距离是 1"""
    diff = abs(ord(c1) - ord(c2))
    return min(diff, 26 - diff)

def smallestString(s: str, k: int) -> str:
    """
    贪心求字典序最小且 distance(s, t) <= k 的字符串 t
    """
    s_list = list(s)                # 方便按位修改
    n = len(s_list)
    remaining = k                    # 剩余可以消耗的距离

    for i in range(n):
        # 从 'a' 到 'z' 逐个尝试，找到第一个可以接受的字符
        for ch in map(chr, range(ord('a'), ord('z') + 1)):
            need = char_dist(s_list[i], ch)   # 把 s[i] 改成 ch 需要的距离
            if need <= remaining:              # 只要不超出剩余预算就可以使用
                s_list[i] = ch                 # 确定该位置的字符
                remaining -= need             # 更新剩余预算
                break                          # 结束本轮循环，进入下一个位置
        # 如果所有字符都不可用（理论上不会出现，因为可以一直选原字符），则保持原字符

    return ''.join(s_list)
```

> 关键行的中文注释已经写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n·26)` → 简化为 `O(n)`，因为 26 是常数。  
  - 直观解释：我们只遍历一次字符串（`n` 次），每次最多检查 26 个字母，整体时间随字符串长度线性增长。  
- **空间复杂度**：`O(n)`，用于存放结果字符串（Python 中的列表/字符串本身就占 `n` 个字符的空间）。

> 与暴力解相比，时间从指数级降到了线性级，几乎可以在毫秒级处理长度 100 的输入。

---

## 心得

- **核心技巧**：**贪心 + 循环距离**。先把左侧尽可能变成 `'a'`，只要不超出预算 `k`。  
- **适用场景**：  
  1. 需要在**有限预算**下让字符串尽可能“小”（字典序）的问题。  
  2. 每个位置的代价是**独立且非负**的优化问题（如把数字数组改成尽可能小的序列，代价为绝对差）。  
  3. 类似的 LeetCode 题目：  
     - *1547. Minimum Cost to Cut a Stick*（贪心分段）  
     - *1640. Check Array Formation Through Concatenation*（逐段检查）  
- **一句话总结**：**左侧先抢，剩余预算后面再花——这就是字典序最小的贪心钥匙。**

---

## 反思

- **第一反应**：看到“字典序最小”和“距离上限”，本能想到“从左到右尽可能改成最小字符”。  
- **最容易踩的坑**：  
  - **循环距离的计算**：忘记取最小的顺时针或逆时针步数，会导致错误的 `need`。  
  - **预算更新错误**：把 `k` 更新成 `k - need` 时忘记使用剩余的 `k`，导致后面的字符被错误限制。  
  - **特殊情况**：`k = 0` 时只能保持原字符，代码仍然要正常运行。  
- **下次思路**：遇到“在预算内让序列尽可能小”这类题，第一步就**考虑贪心从左到右**，验证“当前最小可行选择不影响后续可行性”后再实现。