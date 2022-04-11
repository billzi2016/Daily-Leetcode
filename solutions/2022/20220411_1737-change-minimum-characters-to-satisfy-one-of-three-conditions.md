# #1737. 更改最少字符以满足三种条件之一 / Change Minimum Characters to Satisfy One of Three Conditions

> 难度：中等 · 标签：Hash Table、String、Counting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/change-minimum-characters-to-satisfy-one-of-three-conditions/)

---

## 题目（英文原版）

**Description**

You are given two strings a and b that consist of lowercase letters. In one operation, you can change any character in a or b to any lowercase letter.
Your goal is to satisfy one of the following three conditions:
Return the minimum number of operations needed to achieve your goal.

**Examples**

**Example 1:**

```
Input: a = "aba", b = "caa"
Output: 2
Explanation: Consider the best way to make each condition true:
1) Change b to "ccc" in 2 operations, then every letter in a is less than every letter in b.
2) Change a to "bbb" and b to "aaa" in 3 operations, then every letter in b is less than every letter in a.
3) Change a to "aaa" and b to "aaa" in 2 operations, then a and b consist of one distinct letter.
The best way was done in 2 operations (either condition 1 or condition 3).
```

**Example 2:**

```
Input: a = "dabadd", b = "cda"
Output: 3
Explanation: The best way is to make condition 1 true by changing b to "eee".
```

**Constraints**

- 1 <= a.length, b.length <= 105
- a and b consist only of lowercase letters.

---

## 题目（中文翻译）

给定两个仅由小写字母 (lowercase letters) 组成的字符串 `a` 和 `b`。在一次操作 (operation) 中，你可以将 `a` 或 `b` 中的任意字符改成任意小写字母。  
你的目标是使下面三种条件之一成立，并返回实现目标所需的最少操作次数。

**满足以下任意一种条件：**

1. `a` 中的每个字母都严格小于 `b` 中的每个字母。  
2. `b` 中的每个字母都严格小于 `a` 中的每个字母。  
3. `a` 和 `b` 中所有字符都相同（即只包含一种字母）。

---

### 示例

#### 示例 1
```
Input: a = "aba", b = "caa"
Output: 2
Explanation: 考虑使每个条件成立的最佳方案：
1) 将 `b` 改为 "ccc"（2 次操作），此时 `a` 中的每个字母都小于 `b` 中的每个字母。
2) 将 `a` 改为 "bbb"，`b` 改为 "aaa"（共 3 次操作），此时 `b` 中的每个字母都小于 `a` 中的每个字母。
3) 将 `a` 改为 "aaa"，`b` 改为 "aaa"（2 次操作），此时 `a` 与 `b` 只包含同一种字母。
```

#### 示例 2
```
Input: a = "dabadd", b = "cda"
Output: 3
Explanation: 最佳做法是通过将 `b` 改为 "eee"（3 次操作）使条件 1 成立。
```

---

### 约束条件
- `1 <= a.length, b.length <= 10^5`
- `a` 和 `b` 仅由小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们要把两串字符 **a**、**b** 通过“改字符” 的方式，满足下面三条 **任意一条**：

1. a 中的每个字母都严格小于 b 中的每个字母。  
2. b 中的每个字母都严格小于 a 中的每个字母。  
3. a 与 b 最终都只剩下同一个字母（比如全都变成 `c`）。

> **类比**：把 `a`、`b` 想成两盒彩色弹珠，颜色用字母 `a~z` 表示。  
> - 条件 1 相当于把左盒的弹珠颜色都调暗（小），右盒的弹珠颜色都调亮（大），两盒之间没有交叉。  
> - 条件 3 则是把两盒弹珠全部换成同一种颜色。

最直接的办法是**枚举所有可能的目标**，然后逐个统计需要改动多少字符：

* 条件 3：枚举 26 个字母 `c`，把所有不等于 `c` 的字符改掉，统计次数。  
* 条件 1：枚举 “a 的最大字母” `p`（`p` 只能是 `'a'` 到 `'y'`），让 `b` 的最小字母是 `p+1`。  
  - 把 `a` 中 **比 `p` 大** 的字符全部改掉。  
  - 把 `b` 中 **比 `p+1` 小** 的字符全部改掉。  
* 条件 2：与条件 1 对称，只是把角色换一下。

每次枚举都要遍历整条字符串来统计“有多少字符不符合要求”，于是时间复杂度是：

```
26 次 × (|a| + |b|)  ≈  O(26·n)   (n 为两串长度之和)
```

虽然系数不大，但对 10⁵ 长度的字符串来说仍然有点浪费——我们可以把 **统计过程提前准备**，让每次枚举只用 O(1) 时间。

#### 代码（Python）

```python
def minCharacters_bruteforce(a: str, b: str) -> int:
    # ---------- 辅助函数 ----------
    def changes_to_one_char(s: str, target: int) -> int:
        """把字符串 s 全部改成字符 target（0~25）需要多少次操作"""
        return sum(1 for ch in s if ord(ch) - 97 != target)

    # ---------- 条件 3 ----------
    best = float('inf')
    for c in range(26):                     # 枚举目标字母
        ops = changes_to_one_char(a, c) + changes_to_one_char(b, c)
        best = min(best, ops)

    # ---------- 条件 1 ----------
    for p in range(25):                     # a 的最大字母 p，b 的最小字母必须是 p+1
        ops_a = sum(1 for ch in a if ord(ch) - 97 > p)   # a 中比 p 大的要改
        ops_b = sum(1 for ch in b if ord(ch) - 97 < p + 1)  # b 中比 p+1 小的要改
        best = min(best, ops_a + ops_b)

    # ---------- 条件 2 ----------
    for p in range(25):                     # b 的最大字母 p，a 的最小字母必须是 p+1
        ops_b = sum(1 for ch in b if ord(ch) - 97 > p)
        ops_a = sum(1 for ch in a if ord(ch) - 97 < p + 1)
        best = min(best, ops_a + ops_b)

    return best
```

> **关键行注释**  
> - `ord(ch) - 97` 把字符 `'a'~'z'` 映射到整数 `0~25`，方便比较。  
> - `sum(1 for ...)` 是把每个不符合要求的字符计数，等价于 “需要改动一次”。

#### 复杂度

- **时间复杂度**：`O(26·(|a|+|b|))` ≈ `O(n)`，但实际常数是 26 × 2 ≈ 52，遍历两遍字符串 52 次。  
  - **大白话**：如果字符串总长是 100 000，程序会检查大约 5 200 000 次字符，算起来有点慢。
- **空间复杂度**：`O(1)`，只用了若干计数变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次枚举都要 **重新遍历** 整个字符串统计不符合的字符。  
我们可以在一开始就把每个字母在 `a`、`b` 中出现的次数统计出来，用 **哈希表**（这里用长度为 26 的数组）记住：

```
cntA[i] = a 中字符 i ('a'+i) 出现的次数
cntB[i] = b 中字符 i ('a'+i) 出现的次数
```

有了这两个计数数组，**前缀和**（prefix sum）可以帮助我们在 O(1) 时间内得到：

- “a 中所有字母 **≤ p** 的总数”
- “b 中所有字母 **≥ p** 的总数”

具体做法：

1. **构造前缀和** `preA[i] = Σ_{k=0..i} cntA[k]`（a 中 ≤ i 的字符数）。  
   同理 `preB[i] = Σ_{k=0..i} cntB[k]`（b 中 ≤ i 的字符数）。  
   再算一个 **后缀和** `sufB[i] = Σ_{k=i..25} cntB[k]`（b 中 ≥ i 的字符数），或直接用 `len(b) - preB[i-1]`。

2. **条件 1**（a < b）  
   设 `p` 为 a 的最大字母（0~24），则  
   - 需要改动的 a：`|a| - preA[p]`（所有 > p 的字符）  
   - 需要改动的 b：`preB[p]`（所有 < p+1 的字符）  
   只要遍历 `p = 0..24`，每次用前缀和直接算出两部分的改动数，取最小即可。

3. **条件 2**（b < a）与条件 1 对称，只是把 `a`、`b` 换位。遍历同样的 `p`。

4. **条件 3**（统一成同一字符）  
   对每个字母 `c`，把 `a`、`b` 中不是 `c` 的字符全部改掉。  
   这等价于 `|a| - cntA[c] + |b| - cntB[c]`，同样只需遍历 26 次。

整个过程只用了 **两次线性遍历**（一次统计出现次数，一次遍历 26 个字母），时间是 `O(|a| + |b| + 26)`，即 `O(n)`，而且 **常数非常小**。

> **类比**：把计数数组想成 26 格的小盒子，每格放的是对应字母的弹珠数。  
> 前缀和就是把左边所有盒子的弹珠都倒进一个大桶，瞬间知道“左边一共多少”。这样我们就不必每次都重新去数弹珠。

#### 代码（Python）

```python
def minCharacters(a: str, b: str) -> int:
    # ---------- 1. 统计每个字母出现次数 ----------
    cntA = [0] * 26
    cntB = [0] * 26
    for ch in a:
        cntA[ord(ch) - 97] += 1
    for ch in b:
        cntB[ord(ch) - 97] += 1

    # ---------- 2. 前缀和 ----------
    preA = [0] * 26          # preA[i] = a 中字母 <= i 的数量
    preB = [0] * 26
    preA[0] = cntA[0]
    preB[0] = cntB[0]
    for i in range(1, 26):
        preA[i] = preA[i - 1] + cntA[i]
        preB[i] = preB[i - 1] + cntB[i]

    lenA, lenB = len(a), len(b)
    ans = float('inf')

    # ---------- 3. 条件 1：a 中所有字母 < b 中所有字母 ----------
    for p in range(25):          # p 代表 a 的最大字母，取值 0~24（对应 'a'~'y')
        # a 中需要改动的字符：全部 > p 的字符
        change_a = lenA - preA[p]
        # b 中需要改动的字符：全部 < p+1 的字符，即 <= p 的字符
        change_b = preB[p]
        ans = min(ans, change_a + change_b)

    # ---------- 4. 条件 2：b 中所有字母 < a 中所有字母 ----------
    for p in range(25):
        change_b = lenB - preB[p]          # b 中 > p 的字符要改
        change_a = preA[p]                 # a 中 < p+1 的字符要改（即 <= p）
        ans = min(ans, change_a + change_b)

    # ---------- 5. 条件 3：两串统一成同一字符 ----------
    for c in range(26):
        change = (lenA - cntA[c]) + (lenB - cntB[c])
        ans = min(ans, change)

    return ans
```

> **关键行解释**  
> - `cntA[ord(ch) - 97] += 1`：把字符映射到 0~25，计数。  
> - `preA[i] = preA[i-1] + cntA[i]`：构造前缀和，累计左边所有字母的出现次数。  
> - `lenA - preA[p]`：`lenA` 是 a 的总长度，减去左边（≤p）的弹珠数，就是需要改动的“右边”弹珠数。  
> - `preB[p]`：左边（≤p）的弹珠数，就是 b 中不满足 “≥ p+1” 的字符数。  

#### 复杂度

- **时间复杂度**：`O(|a| + |b| + 26)` ≈ `O(n)`。  
  - 只遍历两遍字符串（统计出现次数），随后遍历 26 次字母，几乎是线性时间。  
  - **对比**：相比暴力解的 52 次全遍历，常数从 52 降到约 30（统计 + 前缀），速度提升明显。

- **空间复杂度**：`O(26)` → `O(1)`。  
  - 使用固定大小的 26 长度数组存计数和前缀和，和输入规模无关。

---

## 心得

- **核心技巧**：把字符出现次数统计下来，再利用前缀和在 *常数时间* 里得到 “≤ 某字母” 或 “≥ 某字母” 的字符数量。  
- **适用的题型**  
  1. 需要比较两个字符串的字母大小关系（如 “Make Two Strings Equal” 类题）。  
  2. 需要把字符统一到某个范围或某个特定字符的最小修改次数（如 “Minimum Deletions to Make Character Frequencies Unique”）。  
- **一句话总结**：**先把信息压缩到 26 个计数，再用前缀和快速求区间统计**，就能把看似 “遍历每次都要全遍历” 的暴力转成线性时间。

---

## 反思

- **第一反应**：看到“改字符”就想到逐字符遍历、枚举目标字母——这自然是暴力思路。  
- **最容易踩的坑**  
  - 忘记 **严格** 小于/大于 的限制，导致把 `'z'` 当作可以成为 “a 的最大字母” 而出现越界。  
  - 条件 3 要让 **两串** 同时变成同一个字母，而不是各自单独统一。  
  - 前缀和的边界处理：`p` 只能取到 `'y'`（索引 24），因为要保证 `p+1` 仍在 `'z'` 范围内。  
- **下次遇到类似题**：第一步先 **统计字母频率**，思考是否可以用 **前缀/后缀和** 把 “大于 / 小于” 的计数变成 O(1) 查询，再再去遍历所有可能的分界点。这样可以把很多 “每次都遍历全串” 的暴力方案优化到线性时间。