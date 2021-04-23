# #1307. 文字算术谜题 / Verbal Arithmetic Puzzle

> 难度：困难 · 标签：Array、Math、String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/verbal-arithmetic-puzzle/)

---

## 题目（英文原版）

**Description**

Given an equation, represented by words on the left side and the result on the right side.
You need to check if the equation is solvable under the following rules:
Return true if the equation is solvable, otherwise return false.

**Examples**

**Example 1:**

```
Input: words = ["SEND","MORE"], result = "MONEY"
Output: true
Explanation: Map 'S'-> 9, 'E'->5, 'N'->6, 'D'->7, 'M'->1, 'O'->0, 'R'->8, 'Y'->'2'
Such that: "SEND" + "MORE" = "MONEY" ,  9567 + 1085 = 10652
```

**Example 2:**

```
Input: words = ["SIX","SEVEN","SEVEN"], result = "TWENTY"
Output: true
Explanation: Map 'S'-> 6, 'I'->5, 'X'->0, 'E'->8, 'V'->7, 'N'->2, 'T'->1, 'W'->'3', 'Y'->4
Such that: "SIX" + "SEVEN" + "SEVEN" = "TWENTY" ,  650 + 68782 + 68782 = 138214
```

**Example 3:**

```
Input: words = ["LEET","CODE"], result = "POINT"
Output: false
Explanation: There is no possible mapping to satisfy the equation, so we return false.
Note that two different characters cannot map to the same digit.
```

**Constraints**

- 2 <= words.length <= 5
- 1 <= words[i].length, result.length <= 7
- words[i], result contain only uppercase English letters.
- The number of different characters used in the expression is at most 10.

---

## 题目（中文翻译）

给定一个等式（equation），左侧由若干单词（words）组成，右侧为结果单词（result）。  
需要判断在满足以下规则的前提下，该等式是否可以求解：  
- 每个不同的字母映射到 **唯一** 的数字 0~9。  
- 同一个字母在所有单词中映射的数字必须相同。  
- 首字符（即每个单词的最高位）不能映射为 0。  
- 将每个单词按字母映射得到的数字相加，必须等于结果单词对应的数字。  

如果存在满足条件的映射，返回 `true`，否则返回 `false`。

## 示例

### 示例 1  
**输入**：`words = ["SEND","MORE"]`, `result = "MONEY"`  
**输出**：`true`  
**解释**：映射关系为  
- `'S' → 9`，`'E' → 5`，`'N' → 6`，`'D' → 7`  
- `'M' → 1`，`'O' → 0`，`'R' → 8`，`'Y' → 2`  

于是 `"SEND" + "MORE" = "MONEY"`，即 `9567 + 1085 = 10652`。

### 示例 2  
**输入**：`words = ["SIX","SEVEN","SEVEN"]`, `result = "TWENTY"`  
**输出**：`true`  
**解释**：映射关系为  
- `'S' → 6`，`'I' → 5`，`'X' → 0`，`'E' → 8`，`'V' → 7`，`'N' → 2`  
- `'T' → 1`，`'W' → 3`，`'Y' → 4`  

于是 `"SIX" + "SEVEN" + "SEVEN" = "TWENTY"`，即 `650 + 68782 + 68782 = 138214`。

### 示例 3  
**输入**：`words = ["LEET","CODE"]`, `result = "POINT"`  
**输出**：`false`  
**解释**：不存在任何映射能够使等式成立，因此返回 `false`。  
注意，两个不同的字符不能映射到同一个数字。

## 约束条件

- `2 ≤ words.length ≤ 5`
- `1 ≤ words[i].length, result.length ≤ 7`
- `words[i]`、`result` 只包含大写英文字母
- 表达式中出现的不同字符总数不超过 10（因为数字 0~9 只有十个）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有出现的字母全部列出来**，然后把 `0~9` 这十个数字全部排列组合，尝试每一种映射是否能让等式成立。

- **数据结构**  
  - `letters`：保存所有不重复的字符，类似一本词典的“单词表”。  
  - `perm`：从 `0~9` 中挑选 `len(letters)` 个数字的全排列，类似把每个单词对应的页码排好顺序。  
  - `mapping`（字典）：把字符映射到数字，像查字典一样，`key` 是字母，`value` 是对应的数字。

- **为什么正确**  
  只要遍历了所有可能的映射，就一定会碰到真实可行的那一种（如果有的话）。只要把每个单词按映射的数字转成整数并相加，检查是否等于结果单词对应的整数即可。

- **复杂度分析（大白话）**  
  - 假设一共有 `k` 个不同的字母（`k ≤ 10`），则需要遍历 `10! / (10‑k)!` 种排列。  
  - 这相当于**指数级**的尝试，最坏情况下接近 `10! ≈ 3.6 百万`，在电脑上虽然还能跑完，但随着 `k` 越大，时间会急剧增长。  
  - 空间上我们只需要保存字母列表和当前的映射，大约 `O(k)`，即几乎不占内存。

#### 代码（Python）

```python
import itertools
from typing import List

def is_solvable_bruteforce(words: List[str], result: str) -> bool:
    # 1️⃣ 收集所有出现的不同字符
    letters = set(''.join(words) + result)          # 类似把所有字母放进一个集合
    if len(letters) > 10:                           # 超过 10 个字符根本不可能映射到 0~9
        return False
    letters = list(letters)

    # 2️⃣ 预先记录每个单词的首字符，防止出现首位为 0 的非法情况
    first_chars = {w[0] for w in words + [result]}

    # 3️⃣ 对 0~9 的全排列进行尝试（只取前 k 位）
    for perm in itertools.permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))          # 把字母映射到数字

        # 4️⃣ 首位不能为 0，直接剪枝
        if any(mapping[ch] == 0 for ch in first_chars):
            continue

        # 5️⃣ 把每个单词转换成对应的整数
        def word_to_num(word: str) -> int:
            num = 0
            for ch in word:
                num = num * 10 + mapping[ch]        # 把每个字符的数字“拼”在一起
            return num

        total = sum(word_to_num(w) for w in words)
        target = word_to_num(result)

        # 6️⃣ 检查等式是否成立
        if total == target:
            return True

    return False
```

#### 复杂度

- **时间复杂度**：`O(P * L)`，其中 `P = 10! / (10‑k)!` 为全排列的数量，`L` 为所有单词字符总数（最多 `5 * 7 = 35`）。  
  用大白话说，就是“尝试所有可能的映射，每一次都要把单词拼成数字”，所以随 `k` 增大，时间会急速增长。

- **空间复杂度**：`O(k)`，只存放字母列表和当前的映射，最多十个元素，几乎不占内存。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**一次性把所有字母都决定**，这会产生大量不必要的尝试。实际上，加法是**从右往左**（最低位到最高位）逐位进行的，每一列的和只会受到当前列的数字以及前一列的进位影响。我们可以利用这个特性，**按列递归地尝试赋值**，并在每一步进行剪枝（提前判断当前列是否已经不可能满足等式），从而大幅减少搜索空间。

核心要点：

1. **列式加法**  
   把所有单词右对齐（不足的左侧补 0），从最右边的列开始往左遍历。每一列会涉及若干个字母（加数的对应位）以及结果字母。

2. **进位 (carry)**  
   加完当前列后会产生一个进位 `carry`，它会影响左边一列的求和。递归的状态需要记住当前列的索引 `col` 和进位 `carry`。

3. **回溯 + 剪枝**  
   - 对当前列未被映射的字母尝试所有可能的数字（0~9 中未被使用的）。  
   - **首位不能为 0**：如果某个字母是任何单词的首字符（包括结果），它在最高位出现时不能映射为 0。  
   - **列求和值校验**：在所有涉及的字母都已经有映射后，检查 `(sum_of_digits + carry) % 10` 是否等于结果位的映射值；若不等则直接剪枝。

4. **结束条件**  
   当遍历完所有列（即 `col == max_len`）时，若进位为 0，则说明找到合法映射。

下面一步步展示如何把这些想法写成代码。

#### 代码（Python）

```python
from typing import List

def is_solvable(words: List[str], result: str) -> bool:
    # ---------- 预处理 ----------
    # 1. 收集所有不同字符
    chars = set(''.join(words) + result)
    if len(chars) > 10:                     # 超过 10 个字符不可能映射到 0~9
        return False
    chars = list(chars)

    # 2. 记录每个字符是否出现在某个单词的首位（不能映射成 0）
    leading = set()
    for w in words + [result]:
        leading.add(w[0])

    # 3. 把所有单词右对齐，方便按列访问
    max_len = max(map(len, words + [result]))
    # 逆序存放，方便从低位到高位遍历
    rev_words = [w[::-1] for w in words]
    rev_result = result[::-1]

    # ---------- 回溯主体 ----------
    assign = {}                 # 当前字母 -> 数字 的映射
    used = [False] * 10         # 哪些数字已经被使用

    def dfs(col: int, carry: int) -> bool:
        """尝试第 col 列（从 0 开始），carry 为前一列的进位"""
        if col == max_len:                 # 已经处理完所有列
            return carry == 0              # 进位必须为 0 才合法

        # ------- 收集本列涉及的字符 -------
        add_chars = []                      # 加数所在列的字符
        for w in rev_words:
            if col < len(w):
                add_chars.append(w[col])
        result_char = rev_result[col] if col < len(rev_result) else None

        # ------- 递归尝试赋值 -------
        # 先把已经有映射的字符算进 sum，未映射的放到待处理列表
        sum_val = carry
        pending = []                        # 需要在本层决定的字符
        for ch in add_chars:
            if ch in assign:
                sum_val += assign[ch]
            else:
                pending.append(ch)

        # 结果字符也可能未映射
        need_result = result_char not in assign if result_char else True

        # 为 pending 中的字符尝试所有未使用的数字
        def try_assign(idx: int) -> bool:
            """给 pending[idx] 赋值并继续递归"""
            if idx == len(pending):
                # 所有加数本列已确定，尝试确定结果位
                digit = sum_val % 10
                if result_char is None:          # 结果没有对应位，等价于 0
                    if digit != 0:
                        return False
                    # 进位进入下一列
                    return dfs(col + 1, sum_val // 10)

                # 结果位已经有映射
                if result_char in assign:
                    if assign[result_char] != digit:
                        return False
                    return dfs(col + 1, sum_val // 10)

                # 结果位未映射，尝试把 digit 分配给它
                if used[digit]:
                    return False
                if digit == 0 and result_char in leading:
                    return False
                # 做映射
                assign[result_char] = digit
                used[digit] = True
                ok = dfs(col + 1, sum_val // 10)
                # 回溯
                del assign[result_char]
                used[digit] = False
                return ok

            # 为 pending[idx] 选一个未使用的数字
            ch = pending[idx]
            for d in range(10):
                if used[d]:
                    continue
                if d == 0 and ch in leading:
                    continue          # 首位不能是 0
                # 做映射
                assign[ch] = d
                used[d] = True
                if try_assign(idx + 1):
                    return True
                # 回溯
                del assign[ch]
                used[d] = False
            return False

        return try_assign(0)

    return dfs(0, 0)
```

> **代码要点注释（中文）**  
> - `rev_words` / `rev_result`：把单词逆序，这样下标 `col` 就对应“从右往左第几位”。  
> - `leading`：保存所有出现过的首字符，用来在给字符赋 0 时进行检查。  
> - `dfs(col, carry)`：递归函数，**列** 为单位进行搜索。  
> - `pending`：本列中尚未确定数字的加数字符，需要在本层尝试所有可能。  
> - `try_assign`：对 `pending` 里的字符逐个尝试，全部确定后检查当前列的 **和** 是否能匹配结果位的数字。  
> - **剪枝**：  
>   1. 已经使用的数字不再尝试。  
>   2. 首位字符不允许取 0。  
>   3. 当结果位已有映射且不等于 `sum % 10` 时直接返回 `False`。  

#### 复杂度

- **时间复杂度**：最坏情况下仍然是 `O(10! )`，因为我们可能要遍历所有合法的映射。但由于**按列逐位剪枝**，实际搜索的分支大幅削减，平均情况远低于全排列。可以把它理解为“在每一步都提前排除大量不可能的情况”，所以在题目给出的限制（最多 10 个字符，单词长度 ≤ 7）下，运行速度几乎是瞬间返回。

- **空间复杂度**：`O(k)`（`k ≤ 10`）用于保存映射 `assign`、已使用数字 `used`，以及递归栈深度 `max_len ≤ 7`，整体非常小。

---

## 心得

- **核心技巧**：**按列回溯（列式加法）** + **进位剪枝**。  
- **适用的题型**  
  1. “Cryptarithmetic” 类的字母数字替换加法（如 `SEND + MORE = MONEY`）。  
  2. 需要满足进位约束的多位数加法或减法问题。  
  3. 其他有限域求解问题（如字母映射到颜色、状态等）可以借鉴列式约束的思想。

- **一句话总结解题钥匙**：**把全局一次性决定的暴力搜索，转化为逐位、逐进位的局部决策，利用进位信息及时剪枝。**

---

## 反思

- **第一反应**：看到“字母 → 数字”的映射，马上想到全排列遍历——最直观但容易超时。  
- **最容易踩的坑**  
  1. **首位为 0**：任何单词的最高位字符不能映射为 0，需要提前记录并在赋值时排除。  
  2. **进位处理**：忘记在最高位结束后检查进位是否为 0，会产生错误的“看似满足”结果。  
  3. **字符数量 > 10**：直接返回 `False`，否则会在排列时出现索引错误。  

- **下次遇到同类题**，第一步应该想到**“把等式按位拆开，利用进位递归搜索”**，而不是一次性遍历所有映射。这样可以在搜索树的每一层就把不可能的分支剔除，大幅提升效率。