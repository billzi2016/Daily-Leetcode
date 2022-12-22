# #2060. **检查是否存在能够被两个编码字符串表示的原始字符串** / Check if an Original String Exists Given Two Encoded Strings

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/check-if-an-original-string-exists-given-two-encoded-strings/)

---

## 题目（英文原版）

**Description**

An original string, consisting of lowercase English letters, can be encoded by the following steps:
For example, one way to encode an original string "abcdefghijklmnop" might be:
Given two encoded strings s1 and s2, consisting of lowercase English letters and digits 1-9 (inclusive), return true if there exists an original string that could be encoded as both s1 and s2. Otherwise, return false.
Note: The test cases are generated such that the number of consecutive digits in s1 and s2 does not exceed 3.

**Examples**

**Example 1:**

```
Input: s1 = "internationalization", s2 = "i18n"
Output: true
Explanation: It is possible that "internationalization" was the original string.
- "internationalization" 
  -> Split:       ["internationalization"]
  -> Do not replace any element
  -> Concatenate:  "internationalization", which is s1.
- "internationalization"
  -> Split:       ["i", "nternationalizatio", "n"]
  -> Replace:     ["i", "18",                 "n"]
  -> Concatenate:  "i18n", which is s2
```

**Example 2:**

```
Input: s1 = "l123e", s2 = "44"
Output: true
Explanation: It is possible that "leetcode" was the original string.
- "leetcode" 
  -> Split:      ["l", "e", "et", "cod", "e"]
  -> Replace:    ["l", "1", "2",  "3",   "e"]
  -> Concatenate: "l123e", which is s1.
- "leetcode" 
  -> Split:      ["leet", "code"]
  -> Replace:    ["4",    "4"]
  -> Concatenate: "44", which is s2.
```

**Example 3:**

```
Input: s1 = "a5b", s2 = "c5b"
Output: false
Explanation: It is impossible.
- The original string encoded as s1 must start with the letter 'a'.
- The original string encoded as s2 must start with the letter 'c'.
```

**Constraints**

- 1 <= s1.length, s2.length <= 40
- s1 and s2 consist of digits 1-9 (inclusive), and lowercase English letters only.
- The number of consecutive digits in s1 and s2 does not exceed 3.

---

## 题目（中文翻译）

一个只包含小写英文字母的原始字符串可以通过以下步骤进行编码：

（题目中会给出编码示例，例如将原始字符串 `"abcdefghijklmnop"` 编码的某种方式。）

给定两个编码字符串 `s1` 和 `s2`，它们仅由小写英文字母和数字 `1-9`（含）组成，返回 `true` 当且仅当存在一个原始字符串能够同时被编码为 `s1` 和 `s2`。否则返回 `false`。

> **注意**：测试用例保证 `s1` 和 `s2` 中连续数字的长度不超过 `3`。

### 示例

#### 示例 1

```text
Input: s1 = "internationalization", s2 = "i18n"
Output: true
```

**解释**：可能的原始字符串是 `"internationalization"`。  

- 对于 `s1`：  
  - **拆分**（split）为 `["internationalization"]`  
  - **不替换**（do not replace）任何元素  
  - **连接**（concatenate）后得到 `"internationalization"`，即 `s1`。  

- 对于 `s2`：  
  - **拆分** 为 `["i", "nternationalizatio", "n"]`  
  - **替换**（replace）为 `["i", "18", "n"]`  
  - **连接** 后得到 `"i18n"`，即 `s2`。

#### 示例 2

```text
Input: s1 = "l123e", s2 = "44"
Output: true
```

**解释**：可能的原始字符串是 `"leetcode"`。  

- 对于 `s1`：  
  - **拆分** 为 `["l", "e", "et", "cod", "e"]`  
  - **替换** 为 `["l", "1", "2", "3", "e"]`  
  - **连接** 后得到 `"l123e"`，即 `s1`。  

- 对于 `s2`：  
  - **拆分** 为 `["leet", "code"]`  
  - **替换** 为 `["4", "4"]`  
  - **连接** 后得到 `"44"`，即 `s2`。

#### 示例 3

```text
Input: s1 = "a5b", s2 = "c5b"
Output: false
```

**解释**：不存在满足条件的原始字符串。  

- 能编码为 `s1` 的原始字符串必须以字母 `'a'` 开头。  
- 能编码为 `s2` 的原始字符串必须以字母 `'c'` 开头。  
两者冲突，故返回 `false`。

### 约束条件

- `1 <= s1.length, s2.length <= 40`
- `s1` 和 `s2` 仅由数字 `1-9`（含）和小写英文字母组成。
- `s1` 和 `s2` 中连续数字的长度不超过 `3`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个编码字符串 **全部展开**，看是否能得到相同的原始字符串。  
- 编码里的字母不变，直接写出来。  
- 编码里的数字（比如 `"12"`）表示 **恰好 12 个任意小写字母**，相当于 12 个 “通配符”。  
  可以把它想成一本字典：数字是“页码”，页码对应的内容是 **任意** 的 12 个字母。  

展开后，两条展开的字符串如果相等，就说明存在这样一个原始字符串。  

**为什么正确**：  
如果真的有一个原始字符串能被同时编码成 `s1` 与 `s2`，那么把 `s1`、`s2` 按照规则展开出来的每一种可能的原始字符串集合必然会交集非空。只要我们把 **所有** 可能的展开枚举出来，检查交集是否为空即可得到答案。

**怎么实现**：  
- 对每个字符串做深度优先搜索（DFS）。  
- 当前指针指向字符 `c`  
  - 若 `c` 是字母，直接把它加入当前展开的结果。  
  - 若 `c` 是数字，读取完整的数字 `num`（题目保证连续数字不超过 3 位），随后递归 **在结果后面追加任意 `num` 个字母**（这里我们可以用 `'a'` 重复 `num` 次来占位，因为后面只比较是否相同，具体是哪 26 个字母并不影响）。  
- 当两个字符串都走完且展开的结果相同，返回 `True`。

**时间/空间复杂度**：  
- 对每个数字 `num`，我们都要把 **`26^num`** 种字母组合都尝试一次（因为每个位置可以是 26 种字母）。如果字符串里出现了长度为 `k` 的数字，时间会呈指数增长，最坏情况是 `O(26^{totalDigits})`。这在实际里是 **爆炸性的**，即使 `totalDigits` 只有 10，`26^{10}` 也远远超出可接受范围。  
- 空间上我们需要保存递归栈以及当前的展开字符串，最深递归层数是 `len(s)`（≤ 40），所以空间是 `O(len(s))`，这本身不算问题。

> **大白话**：  
> 暴力法就像把所有可能的钥匙（原始字符串）都做出来，放进一个大箱子里，然后去箱子里找有没有两把钥匙恰好对应 `s1` 与 `s2`。钥匙的种类太多，根本装不下。

#### 代码（Python）

```python
from typing import List

def expand_all(s: str) -> List[str]:
    """返回所有可能的展开字符串（仅用于演示，实际不可用）。"""
    res = []

    def dfs(idx: int, cur: List[str]):
        # idx：当前在 s 中的位置
        # cur：已经展开的字符列表
        if idx == len(s):
            res.append(''.join(cur))
            return

        if s[idx].isalpha():                     # 直接是字母
            cur.append(s[idx])
            dfs(idx + 1, cur)
            cur.pop()
        else:                                     # 开始读取一个数字
            j = idx
            while j < len(s) and s[j].isdigit():
                j += 1
            num = int(s[idx:j])                  # 这个数字表示多少个通配符
            # 用 'a' 占位，真正的字母可以是任意 26 种，这里只演示一种情况
            for _ in range(num):
                cur.append('a')
            dfs(j, cur)
            for _ in range(num):
                cur.pop()

    dfs(0, [])
    return res

def brute_force(s1: str, s2: str) -> bool:
    """暴力枚举所有展开，判断是否有交集。"""
    set1 = set(expand_all(s1))
    set2 = set(expand_all(s2))
    return not set1.isdisjoint(set2)   # 是否有公共元素
```

> 以上代码只用于说明思路，**在实际测评中会超时**。

#### 复杂度  

- **时间复杂度**：`O(26^{totalDigits})`（指数级），因为每个数字都要尝试 26 的幂次种可能。  
- **空间复杂度**：`O(26^{totalDigits})` 用于保存所有展开的字符串集合，同样是指数级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有可能的字母组合**。其实我们并不需要真的把字母写出来，只要比较两条编码在“长度”层面的匹配情况即可。  
关键观察：

1. **字母只能和字母比较**，如果出现不相同的字母直接返回 `False`。  
2. **数字代表的是“占位的长度”**，它们可以和字母、也可以和另一个数字比较，只要最终的“长度”相等。  
3. 当我们在两条字符串的当前位置分别看到  
   - **字母 vs 字母** → 必须相等，指针都向前走 1 步。  
   - **字母 vs 数字** → 把数字“消耗”掉对应的长度（`min(1, num)`），数字剩余的长度仍然可以继续和后面的字符匹配。  
   - **数字 vs 字母** → 同上，方向相反。  
   - **数字 vs 数字** → 两个数字都可以“相互抵消”。比如 `3` 与 `5`，我们可以把两者都向前消耗 `min(3,5)=3`，剩下的 `0` 与 `2`，继续比较。  

于是我们只需要在 **指针位置 + 剩余未匹配的“通配符长度”** 上递归搜索。  

我们用下面的状态来记忆化（DP）：

```
dfs(i, j, diff)
i   : s1 当前处理到的下标（0 … len(s1)）
j   : s2 当前处理到的下标（0 … len(s2)）
diff: s1 还剩多少“未匹配的字符”，正数表示 s1 多出 diff 个字符，负数表示 s2 多出 -diff 个字符
```

- 当 `diff == 0` 时，两条字符串的已处理部分长度相等，接下来要比较的是 `s1[i]` 与 `s2[j]`。  
- 当 `diff > 0` 时，说明 **s1 里还有 `diff` 个通配符字符** 等待和 `s2` 的后续字符匹配（即 s1 的数字比 s2 的数字大或 s1 的字母已经匹配到了 s2 的数字）。这时我们只看 `s2[j]`：  
  - 若 `s2[j]` 是字母，则消耗掉 1 个 `diff`，指针 `j` 前进 1。  
  - 若 `s2[j]` 是数字 `num`，则把 `num` 与 `diff` 抵消：`newDiff = diff - num`，`j` 前进到数字后面。  
- `diff < 0` 的情况对称，只看 `s1[i]`。

递归的终止条件：

- 两个指针都走到字符串末尾且 `diff == 0` → 成功返回 `True`。  
- 只要有一个指针走完但 `diff` 不为 0，说明长度不匹配，返回 `False`。  
- 在比较字母时发现不相等，直接返回 `False`。

因为每次递归都 **至少前进一位**（或者把 `diff` 减少），状态空间是有限的。我们用 `@lru_cache`（或字典）记忆化，避免重复计算。

**为什么是最优**：  
- 只遍历 **指针位置**（最多 40）和 **diff 的可能取值**。`diff` 的绝对值最大不会超过所有数字之和，而每个数字最多 3 位（最大 999），且字符串长度 ≤ 40，所以 `diff` 的范围在 `[-4000, 4000]` 之内，实际更小。  
- 因此时间复杂度是 `O(L1 * L2 * D)`，在本题的约束下约几千次操作，足够快。  
- 空间只保存记忆化表，大小同样是 `O(L1 * L2 * D)`，远小于暴力的指数级。

#### 代码（Python）

```python
from functools import lru_cache
from typing import Tuple

def possible(s1: str, s2: str) -> bool:
    """判断是否存在一个原始字符串，使得它可以被编码成 s1 与 s2。"""

    # ---------- 辅助函数 ----------
    def next_token(st: str, idx: int) -> Tuple[bool, int, int]:
        """
        读取从 idx 开始的下一个“记号”。
        返回 (is_number, value, next_idx)
        - is_number 为 True 表示是数字，value 为该数字本身
        - is_number 为 False 表示是字母，value 为该字母的 ASCII 码（仅用于比较）
        """
        if idx >= len(st):
            return (False, -1, idx)       # 结束标记，调用方会自行处理

        ch = st[idx]
        if ch.isdigit():
            j = idx
            while j < len(st) and st[j].isdigit():
                j += 1
            num = int(st[idx:j])
            return (True, num, j)          # 是数字
        else:
            return (False, ord(ch), idx + 1)   # 是字母

    # ---------- 主递归 ----------
    @lru_cache(maxsize=None)
    def dfs(i: int, j: int, diff: int) -> bool:
        """
        i, j   : 当前在 s1、s2 的下标
        diff   : s1 剩余未匹配的字符数（正数）或 s2 剩余未匹配的字符数（负数）
        """
        # 终止条件
        if i == len(s1) and j == len(s2):
            return diff == 0          # 两边都用完且长度相等
        if diff == 0:
            # 两边都需要取新的记号进行比较
            if i == len(s1) or j == len(s2):
                return False          # 其中一方已结束，另一方还有字符

            is_num1, val1, ni = next_token(s1, i)
            is_num2, val2, nj = next_token(s2, j)

            if not is_num1 and not is_num2:          # 字母 vs 字母
                if val1 != val2:
                    return False
                return dfs(ni, nj, 0)

            if is_num1 and not is_num2:              # 数字 vs 字母
                # 把数字的长度消耗掉 1（对应的字母）
                return dfs(ni, nj, val1 - 1)

            if not is_num1 and is_num2:              # 字母 vs 数字
                return dfs(ni, nj, -(val2 - 1))

            # 两个都是数字
            # 把两者相互抵消，diff 可能为正、负或 0
            new_diff = val1 - val2
            return dfs(ni, nj, new_diff)

        # diff != 0 时，只需要把较大的那一方的记号与 diff 抵消
        if diff > 0:
            # s1 多出 diff 个字符，需要和 s2 的下一个记号匹配
            if j == len(s2):
                return False
            is_num2, val2, nj = next_token(s2, j)
            if not is_num2:
                # 用掉一个字符
                return dfs(i, nj, diff - 1)
            else:
                # 把数字 val2 与 diff 抵消
                return dfs(i, nj, diff - val2)
        else:  # diff < 0，s2 多出 -diff 个字符，需要和 s1 的下一个记号匹配
            if i == len(s1):
                return False
            is_num1, val1, ni = next_token(s1, i)
            if not is_num1:
                return dfs(ni, j, diff + 1)      # diff 为负，+1 表示消掉一个字符
            else:
                return dfs(ni, j, diff + val1)

    return dfs(0, 0, 0)
```

**代码要点解释（配合中文注释）**  

1. `next_token`：把字符串划分为 “单个字母” 或 “完整数字”。这相当于把原始编码分割成 **最小单元**，类似把句子切成单词。  
2. `dfs(i, j, diff)`：记忆化递归函数。`diff` 表示当前两条已处理部分的长度差。  
3. 当 `diff == 0` 时，两边长度相等，直接比较下一个记号。  
4. 当 `diff > 0`（或 `< 0`）时，只需要让 **另一边的记号** 消耗掉这些多余的字符。  
5. 递归的每一步都 **把指针向前移动**（至少移动 1），或 **把 diff 减少**，因此不会出现无限循环。  
6. `@lru_cache` 自动把 `(i, j, diff)` 的结果缓存，防止同一状态重复计算。

#### 复杂度  

- **时间复杂度**：`O(L1 * L2 * D)`  
  - `L1, L2 ≤ 40` 为两个字符串的长度。  
  - `D` 为 `diff` 可能的取值范围，最坏不超过所有数字之和（每个数字 ≤ 999，最多 40 个），实际远小于 4000。  
  - 在本题约束下，最多几千次递归调用，几乎是常数级别。  
  - 与暴力的指数级 `26^{totalDigits}` 相比，**快了几个数量级**。  

- **空间复杂度**：`O(L1 * L2 * D)` 用于记忆化表 + 递归栈（深度 ≤ L1+L2），同样在几千个状态以内，完全可以接受。

---

## 心得  

- **核心技巧**：把“数字代表的通配符长度”抽象为 **剩余未匹配的字符数**（`diff`），用 **记忆化递归 / 动态规划** 在指针 + 差值空间中搜索。  
- **适用的题型**  
  1. 两个包含通配符（`*`、`?`、数字等）描述的字符串是否可能相等的题目。  
  2. “两个正则表达式能否匹配同一个字符串” 类似的匹配问题。  
  3. “带有回退/跳过指令的路径是否能同步” 之类的 DP/状态机问题。  

- **一句话总结解题钥匙**：  
  > 把数字视作“长度”，只比较 **长度差** 而不是具体字母，用 DP 记忆化遍历所有可能的差值状态。

---

## 反思  

- **第一反应**：看到数字就想到“把它展开成所有可能的字母组合”，于是想到暴力搜索。  
- **最容易踩的坑**  
  - **数字的切分**：连续的数字必须一次性读取为完整的整数（题目保证不超过三位），否则会把 `12` 错误地当成 `1` 和 `2` 两个独立的通配符。  
  - **diff 的符号**：正负代表的是哪一边多出字符，写反了会导致递归方向错误。  
  - **递归终止条件**：忘记在 `diff != 0` 时仍需要检查是否已经到达字符串末尾，会产生错误的 `True`。  
- **下次类似题的第一步**：  
  把所有“可变长度的通配符”抽象为 **剩余长度差**，构建 **指针 + 差值** 的状态空间，再用记忆化递归/DP 检查是否能走到 “两指针都到头且差值为 0”。