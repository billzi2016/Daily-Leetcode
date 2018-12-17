# #205. 同构字符串 / Isomorphic Strings

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/isomorphic-strings/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, determine if they are isomorphic.
Two strings s and t are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.

**Examples**

**Example 1:**

```
Input: s = "egg", t = "add"
Output: true
Explanation:
The strings s and t can be made identical by:
```

**Example 2:**

```
Input: s = "foo", t = "bar"
Output: false
Explanation:
The strings s and t can not be made identical as 'o' needs to be mapped to both 'a' and 'r' .
```

**Example 3:**

```
Input: s = "paper", t = "title"
Output: true
```

**Constraints**

- 1 <= s.length <= 5 * 104
- t.length == s.length
- s and t consist of any valid ascii character.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，判断它们是否是同构的。  
如果可以通过替换 `s` 中的字符得到 `t`，则称这两个字符串是同构的。  

- 所有出现的同一个字符必须被替换成同一个字符，且替换后字符的顺序保持不变。  
- 不同的字符不能映射到同一个字符，但字符可以映射到它自身。

### 示例

**示例 1**  
```
Input: s = "egg", t = "add"
Output: true
Explanation:
可以将字符串 s 中的字符映射为：
'e' → 'a', 'g' → 'd'，从而得到与 t 完全相同的字符串。
```

**示例 2**  
```
Input: s = "foo", t = "bar"
Output: false
Explanation:
字符 'o' 需要同时映射到 'a' 和 'r'，这违反了不同字符不能映射到同一字符的规则，因此无法使两个字符串相同。
```

**示例 3**  
```
Input: s = "paper", t = "title"
Output: true
```

### 约束条件

- `1 <= s.length <= 5 * 10^4`
- `t.length == s.length`
- `s` 和 `t` 由任意有效的 ASCII 字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**只要两个字符串在相同位置的字符出现“模式”相同，它们就是同构的**。  
具体做法：

1. 从左到右遍历下标 `i`（0 ≤ i < n），对每个 `i` 再遍历一次下标 `j`（i+1 ≤ j < n）。
2. 检查两种情况  
   * 若 `s[i] == s[j]`，则要求 `t[i] == t[j]`（相同字符在 `s` 中出现的地方，`t` 中也必须是相同字符）。  
   * 若 `s[i] != s[j]`，则要求 `t[i] != t[j]`（不同字符在 `s` 中出现的地方，`t` 中也必须保持不同）。  
3. 只要出现一次不满足，上面两条规则就说明两串不可能是同构，直接返回 `False`。遍历完都没有冲突则返回 `True`。

> **类比**：把字符串想成一排排的颜色球，暴力解就是把每两个球配对检查——如果两个球颜色相同，那么它们在另一排里的对应球颜色也必须相同；如果颜色不同，另一排的对应球也必须不同。  

这种方法**一定正确**，因为它把“相等关系”在两个字符串之间逐一对应检查完了。

#### 代码（Python）

```python
def isIsomorphic_bruteforce(s: str, t: str) -> bool:
    n = len(s)
    # 两层循环检查每一对位置 i、j
    for i in range(n):
        for j in range(i + 1, n):
            # s 中相等 → t 中必须相等
            if s[i] == s[j] and t[i] != t[j]:
                return False
            # s 中不等 → t 中必须不等
            if s[i] != s[j] and t[i] == t[j]:
                return False
    return True
```

> 关键行解释  
> - `for i in range(n):`：遍历第一个位置。  
> - `for j in range(i + 1, n):`：遍历它后面的所有位置，形成所有 **两两配对**。  
> - `if s[i] == s[j] and t[i] != t[j]:`：检测“相等‑不相等”冲突。  
> - `if s[i] != s[j] and t[i] == t[j]:`：检测“不同‑相等”冲突。

#### 复杂度

- **时间复杂度：** `O(n²)`。  
  *解释*：外层遍历 `n` 次，内层平均遍历约 `n/2` 次，乘起来就是 `n * n/2 ≈ n²`，也就是**平方级**的工作量。对 5 × 10⁴ 长度的字符串来说会非常慢。

- **空间复杂度：** `O(1)`。  
  只用了常数级的额外变量（`i、j、n`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正需要检查的其实只有每个字符第一次出现时的映射关系**，不必把每对位置都比较。  
瓶颈在于 **大量的重复比较**（`i、j` 成对遍历），而我们只需要一次遍历就能捕获所有冲突。

**核心思路**：使用 **哈希表（字典）** 同时记录两种映射  

1. `s → t` 的映射：`char_s` 对应的 `char_t` 必须唯一。  
2. `t → s` 的映射：防止两个不同的 `char_s` 映射到同一个 `char_t`（即 “一对多” 的冲突）。  

> **类比**：把 `s` 看成“老师”，`t` 看成“学生”。老师只能对应唯一的学生，学生也只能对应唯一的老师。我们用两本“通讯录”分别记录老师→学生、学生→老师的对应关系，只要出现冲突就立刻说“不同构”。

遍历两串的每个下标 `i`：

- 如果 `s[i]` 已经出现过，却对应的 `t[i]` 与之前记录的不一致 → 冲突，返回 `False`。  
- 同理，如果 `t[i]` 已经出现过，却对应的 `s[i]` 与之前记录的不一致 → 冲突，返回 `False`。  
- 否则把这对字符加入两个字典。

遍历结束仍未发现冲突，即可返回 `True`。

#### 代码（Python）

```python
def isIsomorphic(s: str, t: str) -> bool:
    # 两个字典分别记录正向和反向映射
    s_to_t = {}   # key: s 的字符, value: 对应的 t 的字符
    t_to_s = {}   # key: t 的字符, value: 对应的 s 的字符

    for ch_s, ch_t in zip(s, t):          # 同时遍历两个字符串
        # 正向映射冲突检测
        if ch_s in s_to_t:
            if s_to_t[ch_s] != ch_t:      # 已记录的映射不相等
                return False
        else:
            s_to_t[ch_s] = ch_t            # 建立新的映射

        # 反向映射冲突检测（防止不同的 s 映射到同一个 t）
        if ch_t in t_to_s:
            if t_to_s[ch_t] != ch_s:      # 已记录的映射不相等
                return False
        else:
            t_to_s[ch_t] = ch_s            # 建立新的映射

    return True
```

> 关键行解释  
> - `for ch_s, ch_t in zip(s, t):`：一次遍历同步取出对应字符。  
> - `if ch_s in s_to_t:`：判断 `s` 中的字符是否已经建立映射。  
> - `if s_to_t[ch_s] != ch_t:`：若映射不一致，说明出现冲突。  
> - 同理的 `t_to_s` 检查确保 **双向唯一**。

#### 复杂度

- **时间复杂度：** `O(n)`。  
  *解释*：只遍历一次长度为 `n` 的字符串，每一步的字典查询/插入都是 **常数时间**（哈希表的平均复杂度），所以整体是线性级别，远快于 `O(n²)`。

- **空间复杂度：** `O(k)`，其中 `k` 为不同字符的种类数（最多不超过字符集大小）。  
  对于 ASCII 字符，`k ≤ 128`，可以视作常数空间；在最坏情况下（所有字符都不相同）会占用 `O(n)` 的额外空间来存储映射表。

---

## 心得

- **核心技巧**：使用哈希表记录双向映射，保证“一对一”对应关系。  
- **适用的题型**  
  1. **判断两个序列是否同构**（如 `Isomorphic Strings`）。  
  2. **判断两个数组的相对顺序是否相同**（如“相同的排列”问题）。  
  3. **字符替换合法性检测**（如“Word Pattern”）。  
- **解题钥匙**：**“把关系抽象成映射表，检查是否出现冲突”**。

---

## 反思

- **第一反应**：看到“字符可以被替换”，自然想到“把每个字符映射成另一个字符”。于是想到用字典记录映射。  
- **最容易踩的坑**  
  - 只检查 `s → t` 而忘记 `t → s`，会出现两个不同字符映射到同一字符的错误情况（如 `s = "ab", t = "cc"`）。  
  - 忽视输入可能包含任意 ASCII 字符，需要使用通用的哈希表而不是仅限 `'a'‑'z'`。  
- **下次第一步**：**先确认“一对一”映射的必要性**，然后决定是否需要双向哈希表来完整约束映射关系。