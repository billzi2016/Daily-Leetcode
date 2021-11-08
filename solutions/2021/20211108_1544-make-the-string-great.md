# #1544. 使字符串变好 / Make The String Great

> 难度：简单 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/make-the-string-great/)

---

## 题目（英文原版）

**Description**

Given a string s of lower and upper case English letters.
A good string is a string which doesn't have two adjacent characters s[i] and s[i + 1] where:
To make the string good, you can choose two adjacent characters that make the string bad and remove them. You can keep doing this until the string becomes good.
Return the string after making it good. The answer is guaranteed to be unique under the given constraints.
Notice that an empty string is also good.

**Examples**

**Example 1:**

```
Input: s = "leEeetcode"
Output: "leetcode"
Explanation: In the first step, either you choose i = 1 or i = 2, both will result "leEeetcode" to be reduced to "leetcode".
```

**Example 2:**

```
Input: s = "abBAcC"
Output: ""
Explanation: We have many possible scenarios, and all lead to the same answer. For example:
"abBAcC" --> "aAcC" --> "cC" --> ""
"abBAcC" --> "abBA" --> "aA" --> ""
```

**Example 3:**

```
Input: s = "s"
Output: "s"
```

**Constraints**

- 1 <= s.length <= 100
- s contains only lower and upper case English letters.

---

## 题目（中文翻译）

给定一个仅包含英文字母大小写的字符串 `s`。  
**好字符串**（good string）指的是不存在相邻字符 `s[i]` 与 `s[i + 1]` 满足以下条件的字符串：  
- `s[i]` 是小写字母，`s[i + 1]` 是对应的大写字母，或  
- `s[i]` 是大写字母，`s[i + 1]` 是对应的小写字母。  

为了使字符串变好，你可以选择一对相邻的、使字符串变坏的字符并将它们删除。不断重复此操作，直至字符串成为好字符串。  
返回最终得到的好字符串。题目保证在给定约束下答案唯一。  
注意，空字符串也被视为好字符串。

**示例 1**  
**输入**: `s = "leEeetcode"`  
**输出**: `"leetcode"`  
**解释**: 第一步可以选择下标 `i = 1`（字符 `'e'` 与 `'E'`）或 `i = 2`（字符 `'E'` 与 `'e'`），两种选择都会把 `"leEeetcode"` 缩减为 `"leetcode"`。

**示例 2**  
**输入**: `s = "abBAcC"`  
**输出**: `""`  
**解释**: 有多种删除顺序，但最终结果相同。例如：  
`"abBAcC"` → `"aAcC"` → `"cC"` → `""`  
`"abBAcC"` → `"abBA"` → `"aA"` → `""`

**示例 3**  
**输入**: `s = "s"`  
**输出**: `"s"`

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由英文字母大小写组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把字符串当成一列字符，顺序检查相邻的两个字符**，只要出现「大小写相同但字母不同」的情况（比如 `'a'` 与 `'A'`、`'B'` 与 `'b'`），就把这两个字符一起删掉。删除后，前后字符会重新相邻，于是我们再从头（或从删除位置）继续检查，直到再也找不到这样的相邻对为止。

- **用到的数据结构**：只需要一个普通的 Python `list`（把字符串转成列表），因为列表可以在任意位置**删除**元素。可以把它想象成「一排磁铁」：相邻的两块磁铁如果是相反极性（大小写相反）就会相互吸走，剩下的磁铁继续往左、往右靠拢。
- **为什么正确**：题目说明「无论先删哪一对，最终得到的好字符串唯一」。因此只要我们不断把所有「相反大小写」的相邻对删掉，最后得到的必然是唯一的好字符串。
- **复杂度分析**：  
  - 每一次遍历我们最多检查 `n`（字符串长度）次；一旦发现一对需要删除，就要把列表中对应的两个元素删掉，这在 Python 列表里是 **O(n)** 的操作（因为后面的元素要整体左移）。最坏情况下会删掉 `n/2` 对，每删一次都要重新遍历。于是时间复杂度大约是 **O(n²)**。  
  - 空间上我们除了原字符串外，还需要一个列表保存字符，额外使用 **O(n)** 的空间。

> **大白话解释**：  
> - `O(n²)` 就像在一个 100 人的队伍里，你每检查完一次就让后面的人全部往前走一次，走完所有人要走 100 次，耗时会翻倍增长。

#### 代码（Python）

```python
def makeGood_bruteforce(s: str) -> str:
    # 把字符串转成列表，方便原地删除
    chars = list(s)
    i = 0                      # 当前检查的下标
    while i < len(chars) - 1:  # 只要还有相邻的两个字符
        a, b = chars[i], chars[i + 1]
        # 判断是否是同字母不同大小写
        if a != b and a.lower() == b.lower():
            # 删除这两个字符，列表会自动左移
            del chars[i:i + 2]
            # 删除后，前面的字符可能又和新的相邻字符构成“坏对”，
            # 所以把指针左移一步（但不能小于0），重新检查
            i = max(i - 1, 0)
        else:
            i += 1               # 当前对没问题，继续向右检查
    return ''.join(chars)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每次删除都可能导致后面的字符整体移动，最坏会进行 `n/2` 次删除，每次遍历 `O(n)`，所以是二次方级别。
- **空间复杂度**：`O(n)`  
  - 需要额外的列表保存字符，长度与原字符串相同。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次删除都要把后面的字符整体搬迁**，导致重复遍历。我们可以把“搬迁”这一步省掉，改用 **栈**（后进先出）来模拟字符的“相邻关系”。

**关键观察**：

- 当我们从左到右遍历字符串时，**栈顶**始终保存**当前已处理好的字符序列的最后一个字符**。  
- 如果当前字符 `c` 与栈顶字符 `top` 互为大小写（即 `c != top` 且 `c.lower() == top.lower()`），那么这两个字符会相互抵消（根据题意直接删除），我们只需要把栈顶弹出，不必真的在原串里做删除操作。  
- 否则，`c` 不能和前面的字符抵消，就把它 **压入栈**，成为新的“最后一个字符”。  

这样 **每个字符只会被压栈一次、弹栈一次**，整个过程只需要一次线性扫描，省去了频繁的移动操作。

**为什么用栈**：  
想象一列磁铁从左到右依次放下，每放一块磁铁，它只会和左边最近的那块磁铁（即栈顶）产生相互作用。如果相互抵消，两块磁铁都消失；如果不抵消，它就稳稳地站在最右端，等待后面的磁铁来检查。

**实现细节**：

1. 初始化空列表 `stack = []`（在 Python 中列表本身就可以当栈用，`append` 入栈、`pop` 出栈）。  
2. 遍历字符串 `s` 中的每个字符 `ch`：  
   - 若 `stack` 非空且 `ch` 与 `stack[-1]` 互为大小写，则 `stack.pop()`（抵消）。  
   - 否则 `stack.append(ch)`（保留下来）。  
3. 最后把栈中的字符拼成字符串返回。

#### 代码（Python）

```python
def makeGood(s: str) -> str:
    """
    使用栈一次遍历完成字符抵消
    """
    stack = []                     # 空栈，用列表模拟
    for ch in s:                   # 从左到右依次处理每个字符
        if stack and ch != stack[-1] and ch.lower() == stack[-1].lower():
            # 栈顶字符和当前字符是同字母不同大小写，互相抵消
            stack.pop()           # 弹出栈顶，相当于把这两个字符都删掉
        else:
            stack.append(ch)       # 不能抵消，保留下来
    return ''.join(stack)          # 把栈中的字符拼成结果字符串
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，每个字符最多压栈一次、弹栈一次，线性时间。相比暴力的 `O(n²)`，快了很多。
- **空间复杂度**：`O(n)`  
  - 最坏情况下没有任何抵消，所有字符都会留在栈里，需要额外 `n` 的空间。

---

## 心得

- **核心技巧**：**栈模拟相邻消除**。利用栈的“后进先出”特性，只需要关注当前字符与最近的未消除字符的关系，就能一次遍历完成所有消除操作。  
- **适用的题型**：  
  1. **相邻字符消除**（如 LeetCode 1047 `Remove All Adjacent Duplicates In String`）。  
  2. **括号匹配**（如 LeetCode 20 `Valid Parentheses`）。  
  3. **单调栈**处理区间问题（如直方图最大矩形）。  
- **一句话总结解题钥匙**：**“只要能把“最近的未处理元素”拿出来比较，就可以用栈一次搞定”。**

---

## 反思

- **第一反应**：看到“相邻字符删除”就想到**遍历并直接删**，于是写出了暴力的双指针/列表删除方案。  
- **最容易踩的坑**：  
  - **大小写判断**：必须同时满足 `c != top`（保证不是同样的字符）以及 `c.lower() == top.lower()`（保证字母相同）。仅比较 `c != top` 会误删相同大小写的字符。  
  - **空字符串**：题目保证返回的空字符串也是合法答案，代码要能正确返回 `''`。  
  - **删除顺序不影响结果**：虽然题目说顺序不影响，但实现时仍需保证每次比较的是“最近的未消除字符”，否则会出现错误的抵消顺序。  
- **下次遇到同类题**：第一步就思考**“是否可以把相邻关系压进栈，仅比较栈顶”**，把暴力的多次遍历和删除转换成一次线性扫描的栈操作。这样往往能直接得到最优解。