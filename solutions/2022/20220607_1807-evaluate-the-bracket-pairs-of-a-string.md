# #1807. 评估字符串中的括号对 / Evaluate the Bracket Pairs of a String

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/evaluate-the-bracket-pairs-of-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s that contains some bracket pairs, with each pair containing a non-empty key.
You know the values of a wide range of keys. This is represented by a 2D string array knowledge where each knowledge[i] = [keyi, valuei] indicates that key keyi has a value of valuei.
You are tasked to evaluate all of the bracket pairs. When you evaluate a bracket pair that contains some key keyi, you will:
Each key will appear at most once in your knowledge. There will not be any nested brackets in s.
Return the resulting string after evaluating all of the bracket pairs.

**Examples**

**Example 1:**

```
Input: s = "(name)is(age)yearsold", knowledge = [["name","bob"],["age","two"]]
Output: "bobistwoyearsold"
Explanation:
The key "name" has a value of "bob", so replace "(name)" with "bob".
The key "age" has a value of "two", so replace "(age)" with "two".
```

**Example 2:**

```
Input: s = "hi(name)", knowledge = [["a","b"]]
Output: "hi?"
Explanation: As you do not know the value of the key "name", replace "(name)" with "?".
```

**Example 3:**

```
Input: s = "(a)(a)(a)aaa", knowledge = [["a","yes"]]
Output: "yesyesyesaaa"
Explanation: The same key can appear multiple times.
The key "a" has a value of "yes", so replace all occurrences of "(a)" with "yes".
Notice that the "a"s not in a bracket pair are not evaluated.
```

**Constraints**

- 1 <= s.length <= 105
- 0 <= knowledge.length <= 105
- knowledge[i].length == 2
- 1 <= keyi.length, valuei.length <= 10
- s consists of lowercase English letters and round brackets '(' and ')'.
- Every open bracket '(' in s will have a corresponding close bracket ')'.
- The key in each bracket pair of s will be non-empty.
- There will not be any nested bracket pairs in s.
- keyi and valuei consist of lowercase English letters.
- Each keyi in knowledge is unique.

---

## 题目（中文翻译）

给定一个字符串 `s`，其中包含若干括号对（bracket pair），每个括号对内含一个非空的键（key）。  
已知大量键的取值，这些信息存放在一个二维字符串数组 `knowledge` 中，其中 `knowledge[i] = [key_i, value_i]` 表示键 `key_i` 对应的值为 `value_i`。  

你的任务是评估所有的括号对。当评估包含键 `key_i` 的括号对时，需要：

* 若 `knowledge` 中存在键 `key_i`，则用对应的 `value_i` 替换整个括号对 `(... )`；
* 若 `knowledge` 中不存在键 `key_i`，则用字符 `?` 替换整个括号对 `(... )`。

每个键在 `knowledge` 中至多出现一次。字符串 `s` 中不存在嵌套的括号。  

返回评估完所有括号对后的结果字符串。

---

### 示例

**示例 1**  
```text
Input: s = "(name)is(age)yearsold", knowledge = [["name","bob"],["age","two"]]
Output: "bobistwoyearsold"
```
**解释**  
键 `"name"` 的值为 `"bob"`，因此将 `"(name)"` 替换为 `"bob"`。  
键 `"age"` 的值为 `"two"`，因此将 `"(age)"` 替换为 `"two"`。

**示例 2**  
```text
Input: s = "hi(name)", knowledge = [["a","b"]]
Output: "hi?"
```
**解释**  
由于未知键 `"name"` 的取值，将 `"(name)"` 替换为 `"?"`。

**示例 3**  
```text
Input: s = "(a)(a)(a)aaa", knowledge = [["a","yes"]]
Output: "yesyesyesaaa"
```
**解释**  
同一个键可以出现多次。键 `"a"` 的值为 `"yes"`，因此将所有 `"(a)"` 替换为 `"yes"`。  
注意，不在括号对中的 `"a"` 不会被评估。

---

### 约束条件

- `1 <= s.length <= 10^5`
- `0 <= knowledge.length <= 10^5`
- `knowledge[i].length == 2`
- `1 <= key_i.length, value_i.length <= 10`
- `s` 仅由小写英文字母和圆括号 `'('`、`')'` 组成
- 每个左括号 `'('` 在 `s` 中都有对应的右括号 `')'`
- 每个括号对中的键非空
- `s` 中不存在嵌套的括号对
- `key_i` 与 `value_i` 仅由小写英文字母组成
- `knowledge` 中的每个 `key_i` 唯一

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把字符串 `s` 按顺序扫一遍，遇到左括号 `'('` 就往后找对应的右括号 `')'`，把两者之间的子串当作 **key**。  
随后在 `knowledge` 里逐个比较，找到匹配的 `[key, value]`，如果找到了就用 `value` 替换掉整个 `"(key)"`，找不到则替换成 `'?'`。  

- **用到的数据结构**：  
  - `knowledge` 本身是一个二维列表，像一本 **查字典**，`key` 就是词，`value` 是对应的页码。我们在暴力解里会把它当成一本**顺序的字典**，每次都从头到尾线性查找。  
  - 结果字符串可以用 Python 的 `list`（字符数组）来临时保存，最后 `join` 成最终答案。  

- **为什么正确**：  
  - 题目保证每个左括号都有右括号且没有嵌套，按左到右的顺序一次处理每个完整的 `"(key)"` 就能覆盖所有需要替换的地方。  
  - 即使同一个 `key` 出现多次，只要每次都查找 `knowledge`，都能得到相同的 `value`（或 `'?'`），所以最终字符串必然符合题意。  

- **复杂度分析（大白话）**：  
  - 假设 `s` 长度为 `n`，`knowledge` 中有 `m` 条记录。  
  - 对于每个括号对，我们都要在 `knowledge` 里 **顺序** 查找一次，最坏情况要比较 `m` 次。  
  - 所以时间复杂度是 **O(n·m)**，如果 `m` 很大（比如 10⁵），这会非常慢。  
  - 空间上我们只额外用了一个结果数组，大小和 `s` 相同，故 **O(n)** 的空间。  

#### 代码（Python）  
```python
def evaluate_brackets_brute(s: str, knowledge: list[list[str]]) -> str:
    # 把 knowledge 变成普通的 list，后面会线性遍历它
    # 这里不使用 dict，保持“暴力”本色
    n = len(s)
    i = 0                     # 主指针，遍历 s
    res = []                  # 用列表收集最终字符，最后 join

    while i < n:
        if s[i] == '(':       # 发现左括号，准备找右括号
            j = i + 1
            # 向右找第一个 ')'，因为题目保证一定能找到
            while j < n and s[j] != ')':
                j += 1
            # s[i+1:j] 就是 key（不包括括号本身）
            key = s[i + 1:j]

            # 暴力查找 knowledge，模拟“顺序字典”
            value = '?'        # 默认找不到
            for k, v in knowledge:
                if k == key:   # 找到对应的 value
                    value = v
                    break

            # 把找到的 value（或 '?'）加入结果
            res.append(value)

            i = j + 1          # 跳过整个 "(key)"，继续向后
        else:
            # 普通字符直接加入结果
            res.append(s[i])
            i += 1

    return ''.join(res)
```

#### 复杂度  
- **时间复杂度**：`O(n·m)`  
  - 解释：`n` 是字符串长度，`m` 是 knowledge 条数。每找到一对括号，就要在 `knowledge` 里遍历一次，最坏情况是 `n/2` 对括号 → 大约 `n·m` 次比较。  
- **空间复杂度**：`O(n)`  
  - 只用了一个和原字符串等长的列表来拼接答案，额外的哈希表或递归栈都没有。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看出，**瓶颈** 出在每次都要线性遍历 `knowledge` 来找对应的 `value`。这一步完全可以用 **哈希表（字典）** 把查询时间降到常数 `O(1)`。  

优化步骤如下：  

1. **预处理**：把 `knowledge` 转成 Python 的 `dict`，相当于把“顺序的字典”变成**查字典**，`key` → `value`。这一步只需要遍历一次 `knowledge`，时间 `O(m)`，空间 `O(m)`（存放所有键值对）。  
2. **一次遍历 s**：仍然用双指针 `i`（主指针）和 `j`（寻找右括号），每遇到左括号就往后找右括号得到 `key`。  
3. **直接查询**：用 `dict.get(key, '?')` 在常数时间内得到对应的 `value`，若不存在则返回 `'?'`。  
4. **构造答案**：把得到的 `value`（或 `'?'`）加入结果列表，继续扫描。  

整个过程只遍历 `s` 一遍，没有额外的嵌套循环，时间复杂度降为 **O(n + m)**。  

> **为什么不会漏掉重复的 key**  
> 题目保证同一个 `key` 可能出现多次，但在 `knowledge` 中只会出现一次。字典天然支持“同一个键多次查询”，每次都返回同一个 `value`，因此不需要额外处理。  

#### 代码（Python）  
```python
def evaluate_brackets(s: str, knowledge: list[list[str]]) -> str:
    """
    最优实现：利用哈希表把查找时间压到 O(1)。
    """
    # 1. 把 knowledge 转成 dict，等价于 “查字典”
    kv_map = {k: v for k, v in knowledge}   # O(m) 时间、O(m) 空间

    n = len(s)
    i = 0
    res = []                # 用列表收集字符，最后一次性 join

    while i < n:
        if s[i] == '(':
            # 2. 找到对应的 ')'
            j = i + 1
            while j < n and s[j] != ')':
                j += 1
            # 提取 key（不包括 '(' 与 ')'）
            key = s[i + 1:j]

            # 3. 哈希表查询，若不存在返回 '?'
            value = kv_map.get(key, '?')
            res.append(value)

            i = j + 1        # 跳过整个 "(key)"
        else:
            # 普通字符直接加入
            res.append(s[i])
            i += 1

    return ''.join(res)     # O(n) 合并
```

#### 复杂度  
- **时间复杂度**：`O(n + m)`  
  - `n` 为字符串长度，`m` 为 knowledge 条数。  
  - 预处理 `knowledge` 用 `O(m)`，遍历 `s` 用 `O(n)`，两者相加即为总时间。相比暴力的 `O(n·m)`，这里把“每次查找”从线性降到了常数。  
- **空间复杂度**：`O(m + n)`  
  - `kv_map` 需要存 `m` 条键值对，结果列表 `res` 长度最多为 `n`（最坏情况所有字符都是普通字符），所以总空间是两者之和。  

---

## 心得  

- **核心技巧**：使用哈希表（字典）把多次查询的复杂度从线性 `O(m)` 降到常数 `O(1)`。  
- **适用的题型**：  
  1. “把字符串中的占位符替换成对应值”——如 LeetCode 1840 *Maximum Building Height* 中的高度映射。  
  2. “根据键值对对数组或字符串进行批量替换”——如 2085 *Count Common Words With One Occurrence*。  
  3. “字符频次统计后快速查询”——如 2420 *Find All Good Indices* 中的前缀/后缀计数。  
- **一句话总结解题钥匙**：**先把所有已知映射装进字典，再一次遍历原始数据完成替换**。  

---

## 反思  

- **第一反应**：看到括号里是“键”，想到先把键对应的值准备好，然后再把字符串逐段替换。  
- **最容易踩的坑**：  
  - 忘记处理 **不存在的键**，导致直接访问字典时报错。使用 `dict.get(key, '?')` 可以安全返回默认值。  
  - 没有正确跳过已经处理的 `"(key)"`，导致进入死循环或重复字符。记得在处理完括号后把指针移动到右括号的下一个位置。  
  - 题目保证没有嵌套括号，但如果误以为会有，需要额外的栈来匹配，这会增加不必要的复杂度。  
- **下次遇到同类题**：第一步先思考“是否可以把所有已知信息预处理成哈希表”，如果可以，就直接用 O(1) 查询，否则才考虑更复杂的数据结构（如前缀和、单调栈等）。