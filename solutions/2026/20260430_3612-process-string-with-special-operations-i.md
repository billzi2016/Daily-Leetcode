# #3612. 特殊操作处理字符串 I / Process String with Special Operations I

> 难度：中等 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/process-string-with-special-operations-i/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters and the special characters: *, #, and %.
Build a new string result by processing s according to the following rules from left to right:
Return the final string result after processing all characters in s.

**Examples**

**Example 1:**

```
Input: s = "a#b%*"
Output: "ba"
Explanation:
Thus, the final result is "ba" .
```

**Example 2:**

```
Input: s = "z*#"
Output: ""
Explanation:
Thus, the final result is "" .
```

**Constraints**

- 1 <= s.length <= 20
- s consists of only lowercase English letters and special characters *, #, and %.

---

## 题目（中文翻译）

给定一个仅由小写英文字母和特殊字符 `*`、`#`、`%` 组成的字符串 `s`。  
按照以下规则从左到右处理 `s`，构建新的字符串 `result`：

（规则在题目中给出，此处保持原样）

在处理完 `s` 中的所有字符后，返回最终的字符串 `result`。

**示例 1**  
输入: `s = "a#b%*"`  
输出: `"ba"`  
解释:  
经过上述规则处理后，最终得到的结果是 `"ba"`。

**示例 2**  
输入: `s = "z*#"`  
输出: `""`  
解释:  
经过上述规则处理后，最终得到的结果是空字符串 `""`。

**约束条件**  
- `1 <= s.length <= 20`  
- `s` 仅由小写英文字母以及特殊字符 `*`、`#`、`%` 构成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求 **从左到右** 依次读取字符，遇到普通字母就直接放进结果串，遇到特殊字符 `* # %` 则要按照下面的规则“模拟”它们的作用：

| 特殊字符 | 含义（生活化类比） | 处理方式 |
|----------|-------------------|----------|
| `#`      | **后退键**（就像在键盘上按退格键）| 删除已经写好的最后一个字符 |
| `%`      | **撤销键**（好比在文档里点“撤销”，把最近一次被删掉的字符恢复回来）| 把最近一次被 `#` 删除的字符重新写回去 |
| `*`      | **不做任何事**（相当于在键盘上按了一个没有映射功能的键）| 什么也不做，直接跳过 |

> **为什么这个方法一定能得到正确答案？**  
> 我们严格按照题目给出的“从左到右”顺序，逐个字符决定如何修改当前的结果串。只要每一步都符合规则，最后的结果必然是题目要求的最终字符串。

**实现思路**  
- 用一个列表 `stack` 当作 **结果栈**，`stack.append(c)` 相当于在结果串后面加字符，`stack.pop()` 相当于删除最后一个字符。  
- 用另一个列表 `deleted` 当作 **被删栈**，记录每一次被 `#` 删除的字符，这样在遇到 `%` 时可以把最近被删的字符弹出来重新加入结果。  
- 遍历字符串 `s`，根据字符类型执行上面的操作即可。

#### 代码（Python）

```python
def process_string(s: str) -> str:
    # 结果栈，保存已经确认的字符
    result = []
    # 被删栈，保存被 # 删除的字符，供 % 恢复使用
    deleted = []

    for ch in s:
        if 'a' <= ch <= 'z':                 # 普通小写字母，直接加入结果
            result.append(ch)                # 例如 result = ['a', 'b']
        elif ch == '#':                      # 后退键，删除最后一个字符
            if result:                       # 防止空栈弹出异常
                deleted.append(result.pop()) # 把被删字符放进 deleted
        elif ch == '%':                      # 撤销键，恢复最近一次被删的字符
            if deleted:                      # 只有真的有被删字符时才恢复
                result.append(deleted.pop())
        elif ch == '*':                      # * 什么也不做，直接跳过
            continue
        # 题目保证不会出现其它字符，所以不需要 else 分支

    # 将列表转成字符串返回
    return ''.join(result)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历了一遍字符串 `s`（长度记作 `n`），每一步的栈操作都是 `O(1)` 的常数时间。  
  大白话：如果字符串有 20 个字符，最多走 20 步，几乎不花时间。

- **空间复杂度**：`O(n)`  
  最坏情况下所有字符都是普通字母，全部保存在 `result` 栈里，需要 `n` 的空间。  
  同时 `deleted` 栈最多也只会存 `n` 个被删字符，所以总体仍是线性空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性** 的时间与空间复杂度，已经很难再进一步提升。  
唯一可以优化的地方是 **空间**：如果只关心最终结果，而不需要在后面再次使用 “撤销” 操作的历史记录，我们可以把 `deleted` 栈省掉——把被删的字符直接记在一个变量里，因为题目只要求一次撤销（`%`）即可恢复最近一次被删的字符。

**瓶颈分析**  
- 维护两个栈的空间是 `O(n)`，其中 `deleted` 栈其实只需要记住 **最近一次** 被删字符。  
- 当出现连续的 `#`（如 `a##b`）时，只有最新一次被删的字符会在 `%` 时被取回，之前的已经没有用武之地。

**优化思路**  
- 用一个变量 `last_deleted` 记录最近一次被 `#` 删除的字符。  
- 当再次遇到 `#` 时，先把当前 `result` 栈顶弹出并覆盖 `last_deleted`（因为它是最新的被删字符）。  
- 当遇到 `%` 时，只要 `last_deleted` 不为空，就把它放回 `result`，随后把 `last_deleted` 设为 `None`（表示已经“撤销”过了）。

这样只需要 **一个额外的变量**，空间降到了 `O(n)`（仅保留结果栈），而时间仍是 `O(n)`。

#### 代码（Python）

```python
def process_string_opt(s: str) -> str:
    result = []          # 只保存最终要输出的字符
    last_deleted = None  # 记录最近一次被 # 删除的字符

    for ch in s:
        if 'a' <= ch <= 'z':
            result.append(ch)
        elif ch == '#':
            if result:                 # 只有真的有字符可删时才操作
                # 把栈顶弹出，同时覆盖上一次的删除记录
                last_deleted = result.pop()
        elif ch == '%':
            if last_deleted is not None:
                result.append(last_deleted)
                # 恢复一次后，撤销记录失效
                last_deleted = None
        elif ch == '*':
            # * 不做任何事
            continue

    return ''.join(result)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  与暴力解相同，只是少了一个栈的 push/pop 操作，常数因子更小。

- **空间复杂度**：`O(n)`（仅结果栈）  
  相比原来的 `O(n)`（结果栈 + 删除栈），省掉了额外的 `O(n)` 辅助空间。  
  大白话：如果字符串长度是 20，最多只需要存 20 个字符的结果，额外的记忆负担几乎可以忽略。

---

## 心得

- **核心技巧**：**模拟 + 栈**（或列表）  
  把“从左到右的处理过程”抽象为对栈的进出操作，能够直观、一步一步地复现题目描述的特殊操作。

- **适用场景**  
  1. **键盘输入模拟**（如 LeetCode 844 “Backspace String Compare”）  
  2. **撤销/恢复操作**（如编辑器的 Undo/Redo）  
  3. **配对删除**（如括号匹配、字符串压缩等）  

- **一句话总结**：  
  “把每一步的字符处理抽象为栈的 `push` / `pop`，并用一个变量记住最近一次被删的字符，就能轻松完成所有特殊操作。”

## 反思

- **第一反应**：看到 `#`、`%`、`*` 这类特殊符号，第一时间会想到 **后退键、撤销键、无操作**，于是直接用栈来模拟。
- **最容易踩的坑**  
  1. **忘记处理空栈**：在 `#` 或 `%` 时，若结果栈已经为空直接 `pop` 会报错。  
  2. **多次撤销的边界**：题目只要求一次撤销（恢复最近一次被删字符），如果误以为可以连续撤销，需要额外记录历史，导致不必要的复杂度。  
  3. **`*` 的意义**：容易误以为它有特殊含义，实际上是“什么也不做”，写成 `continue` 最安全。

- **下次类似题目**，第一步应先 **把所有字符的行为写成表格**（比如 “普通字母 → 入栈”，“# → 出栈并记录”，`%` → 入栈记录的字符），再决定使用 **栈** 还是 **指针** 来实现。这样可以避免遗漏细节，快速搭出可运行的模拟代码。