# #2745. 构造最长的新字符串 / Construct the Longest New String

> 难度：中等 · 标签：Math、Dynamic Programming、Greedy、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/construct-the-longest-new-string/)

---

## 题目（英文原版）

**Description**

You are given three integers x, y, and z.
You have x strings equal to "AA", y strings equal to "BB", and z strings equal to "AB". You want to choose some (possibly all or none) of these strings and concatenate them in some order to form a new string. This new string must not contain "AAA" or "BBB" as a substring.
Return the maximum possible length of the new string.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: x = 2, y = 5, z = 1
Output: 12
Explanation: We can concatenate the strings "BB", "AA", "BB", "AA", "BB", and "AB" in that order. Then, our new string is "BBAABBAABBAB". 
That string has length 12, and we can show that it is impossible to construct a string of longer length.
```

**Example 2:**

```
Input: x = 3, y = 2, z = 2
Output: 14
Explanation: We can concatenate the strings "AB", "AB", "AA", "BB", "AA", "BB", and "AA" in that order. Then, our new string is "ABABAABBAABBAA". 
That string has length 14, and we can show that it is impossible to construct a string of longer length.
```

**Constraints**

- 1 <= x, y, z <= 50

---

## 题目（中文翻译）

给定三个整数 `x`、`y` 和 `z`。  
你拥有 `x` 个字符串为 `"AA"`、`y` 个字符串为 `"BB"`、以及 `z` 个字符串为 `"AB"`。你可以选择其中的任意若干（可以全部也可以一个也不选）并以任意顺序将它们**拼接（concatenate）**起来，形成一个新的**字符串（string）**。该新字符串**不能**包含 `"AAA"` 或 `"BBB"` 作为**子串（substring）**。  

返回能够构造的新字符串的**最大可能长度**。  

**子串**是指字符串中连续的、非空的字符序列。  

## 示例  

### 示例 1  
**输入**: `x = 2, y = 5, z = 1`  
**输出**: `12`  
**解释**: 我们可以按顺序拼接 `"BB"`, `"AA"`, `"BB"`, `"AA"`, `"BB"` 和 `"AB"`，得到的新字符串为 `"BBAABBAABBAB"`。  
该字符串长度为 12，且可以证明不存在更长的合法字符串。

### 示例 2  
**输入**: `x = 3, y = 2, z = 2`  
**输出**: `14`  
**解释**: 我们可以按顺序拼接 `"AB"`, `"AB"`, `"AA"`, `"BB"`, `"AA"`, `"BB"` 和 `"AA"`，得到的新字符串为 `"ABABAABBAABBAA"`。  
该字符串长度为 14，且可以证明不存在更长的合法字符串。

## 约束条件  

- `1 <= x, y, z <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 能选的字符串列出来，然后枚举：

1. 先决定每种字符串要选多少（`0 ~ x` 个 `"AA"`、`0 ~ y` 个 `"BB"`、`0 ~ z` 个 `"AB"`）。  
2. 把选中的这些小块全部排列组合，得到若干完整的长字符串。  
3. 检查每个长字符串里是否出现了 `"AAA"` 或 `"BBB"`，如果没有就记下它的长度，最后取最大值。

> **类比**：把每块小字符串想成一张纸条，我们要把纸条排成一行。枚举所有排法就像把所有纸条的所有可能摆放方式都列出来，显然会非常多。

**为什么这个方法能得到正确答案**  
因为它遍历了「所有合法的」拼接方式——只要我们把每一种可能都试一遍，最大长度自然会被发现。

**时间/空间复杂度**  
- 选取数量的枚举本身是 `O((x+1)*(y+1)*(z+1))`，最多约 `51³ ≈ 1.3e5`（对 50 的上限已经算是可接受的）。  
- 但是**排列**的步奏是致命的：选了 `k` 块后，要遍历 `k!` 种顺序。最坏情况下 `k = x + y + z ≤ 150`，`150!` 远远超出计算能力。  
- 因此整体时间复杂度是 **指数级**（`O(k!)`），空间上只需要保存当前排列，`O(k)`。

> **大白话**：  
> - `O(n²)` 表示“把 n 个东西两两比较”大约需要 n×n 次操作。  
> - `O(k!)` 表示“把 k 个东西全排列”，操作次数会像 1·2·3·…·k 那样飞快增长，几分钟内就算不可能算完。

#### 代码（Python）

```python
import itertools

def brute(x: int, y: int, z: int) -> int:
    # 所有可选的小块
    blocks = ["AA"] * x + ["BB"] * y + ["AB"] * z
    n = len(blocks)
    best = 0

    # 枚举使用的子集（用二进制表示是否取第 i 块）
    for mask in range(1 << n):
        chosen = [blocks[i] for i in range(n) if mask >> i & 1]
        # 对子集内部所有排列进行尝试
        for perm in itertools.permutations(chosen):
            s = "".join(perm)
            if "AAA" not in s and "BBB" not in s:
                best = max(best, len(s))
    return best
```

> 这段代码只能在极小的 `x, y, z`（比如 ≤ 4）时跑得完，已经超出了题目限制。

#### 复杂度

- **时间复杂度**：`O(2^{x+y+z} * (x+y+z)!)` → 指数级，实际不可用。  
- **空间复杂度**：`O(x + y + z)` → 只保存当前的排列。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**枚举所有排列是最慢的环节**。我们要找出一种不需要排列、只用计数就能得到答案的思路。

下面一步步推导：

1. **“AB” 块的特性**  
   - `"AB"` 本身已经是交替的 `"A"`、`"B"`，不会产生 `"AAA"` 或 `"BBB"`。  
   - 把若干 `"AB"` 串在一起得到 `"ABABAB…"`，仍然安全。  
   - 重要结论（题目提示已经证明）：**在最优解里一定会使用所有的 `z` 个 `"AB"`**。因为它们既不增加冲突，又能贡献 2 的长度。

2. **把所有 `"AB"` 串起来**  
   - 拼成 `ABAB…AB`（共 `2·z` 个字符）。  
   - 这条基准链已经交替出现 `A`、`B`，唯一的 “空位” 是 **在每个字符的左侧或右侧**，我们可以在这些空位插入 `"AA"` 或 `"BB"`，只要不让同一种字符连续出现 3 次。

3. **怎样插入 `"AA"` 与 `"BB"`**  
   - 观察基准链 `ABAB…AB`，每出现一次 **B**，它的左边是 **A**，右边（如果不是结尾）也是 **A**。  
   - 若我们在 **B** 的左侧插入 `"AA"`，会得到 `...AA B ...` → `A A B`，最多出现两连 `A`，安全。  
   - 同理，在 **A** 的左侧插入 `"BB"` 也是安全的。  
   - 关键是：**每个 “B” 最多只能插入一块 `"AA"`，每个 “A” 最多只能插入一块 `"BB"`**。  
   - `"AB"` 链里一共有 `z` 个 `B`（以及 `z` 个 `A`），所以我们最多能插入 `z` 块 `"AA"` 和 `z` 块 `"BB"`。但这并不是限制，因为我们还有额外的 `"AA"`、`"BB"` 可以直接放在字符串的 **开头** 或 **结尾**。

4. **交替使用 `"AA"` 与 `"BB"`**  
   - 为了避免出现 `AAA` 或 `BBB`，最安全的做法是 **交替** 使用 `"AA"` 与 `"BB"`：  
     ```
     AA BB AA BB …   或   BB AA BB AA …
     ```  
   - 只要我们把两者配对使用，任意多对都不会产生冲突。  
   - 能配对的对数受限于较少的那种块的数量：`pairs = min(x, y)`。

5. **处理剩余的块**  
   - 配对完后，可能还有多余的 `"AA"`（如果 `x > y`）或多余的 `"BB"`（如果 `y > x`）。  
   - 这时可以把 **一块** 多余的块放在整个字符串的最前面或最后面：  
     - 例如 `AA` + `ABAB…` + `BB`，仍然不会出现三个相同字符。  
   - 只能放 **一块**，因为放两块会在同侧产生 `AAAA` 或 `BBBB`（违反规则）。

6. **总结得到公式**  

| 使用的块数 | 长度贡献 |
|-----------|----------|
| 所有 `AB` (`z` 个) | `2·z` |
| 成对的 `AA` 与 `BB` (`pairs = min(x, y)`) | 每对 4 长度 → `4·pairs` |
| 可能的额外块（如果 `x ≠ y`） | 2 长度 |

所以答案为  

\[
\text{ans} = 2·z + 4·\min(x, y) + 
\begin{cases}
2 & (x \neq y)\\
0 & (x = y)
\end{cases}
\]

等价写成更直观的形式：

```python
ans = 2 * z                     # 所有 AB
ans += 2 * (2 * min(x, y))      # 配对的 AA 与 BB
if x > y:
    ans += 2                    # 额外的一个 AA
elif y > x:
    ans += 2                    # 额外的一个 BB
```

> 这就是 **贪心** 思路：先把所有 “安全” 的块用完（AB），再尽可能多地交替使用 AA/BB，最后在两端补上一块多余的块。

#### 代码（Python）

```python
def longestString(x: int, y: int, z: int) -> int:
    """
    返回在不出现 'AAA' 或 'BBB' 的前提下，能够构造的最长字符串的长度。
    思路：贪心 + 简单计数
    """
    # 1. 使用所有的 "AB"
    ans = 2 * z                     # 每个 AB 长度为 2

    # 2. 交替使用 AA 与 BB，能配对的数量是两者的最小值
    pairs = min(x, y)               # 配对的次数
    ans += 4 * pairs                # 每对贡献 4（AA+BB 各 2）

    # 3. 处理剩余的块：只能在最前或最后再放一块
    if x > y:
        ans += 2                    # 额外的一个 AA
    elif y > x:
        ans += 2                    # 额外的一个 BB

    return ans
```

> 代码仅用了几行整数运算，几乎可以在 **O(1)** 时间内算出答案。

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做常数次算术操作。相比暴力的指数级，快得多。  
- **空间复杂度**：`O(1)` —— 只用几个整数变量。

---

## 心得

- **核心技巧**：**贪心计数**——先利用所有“安全”块（`AB`），再尽可能交替使用会产生冲突的块（`AA`、`BB`），最后在两端补上多余的块。  
- **适用的题型**  
  1. 需要避免连续相同字符的排列问题（如 “避免 AAA/BBB”）。  
  2. 资源（块）可以任意组合，只要满足局部约束的“最大化长度/数量”类问题。  
  3. 类似的 LeetCode 题目：`Longest Happy String`、`Maximum Length of a Concatenated String with Unique Characters`。  
- **一句话总结解题钥匙**：**把所有不产生冲突的块先用完，再交替使用会产生冲突的块，剩余的只能放在两端**。

---

## 反思

- **第一反应**：直接想枚举所有排列，没意识到这会爆炸。  
- **最容易踩的坑**  
  - 忽视了 **所有 `AB` 必然全部使用** 的证明，导致思考时会把它当成可选项，从而多走不必要的分支。  
  - 在插入 `AA`、`BB` 时没有仔细考虑“连续三个相同字符”的边界，容易误把两块同类放在一起。  
- **下次类似题目第一步**：先**找出“永远安全”可以全部使用的元素**（这里是 `AB`），再**考虑如何在它们之间交替安排有冲突的元素**。这样往往能把问题从指数级压到常数级。