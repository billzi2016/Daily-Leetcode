# #1047. 删除字符串中的所有相邻重复字符 / Remove All Adjacent Duplicates In String

> 难度：简单 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters. A duplicate removal consists of choosing two adjacent and equal letters and removing them.
We repeatedly make duplicate removals on s until we no longer can.
Return the final string after all such duplicate removals have been made. It can be proven that the answer is unique.

**Examples**

**Example 1:**

```
Input: s = "abbaca"
Output: "ca"
Explanation: 
For example, in "abbaca" we could remove "bb" since the letters are adjacent and equal, and this is the only possible move.  The result of this move is that the string is "aaca", of which only "aa" is possible, so the final string is "ca".
```

**Example 2:**

```
Input: s = "azxxzy"
Output: "ay"
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`。**重复移除（duplicate removal）** 指的是选择两个相邻且相同的字符并将它们删除。  
我们对 `s` 反复执行重复移除，直到无法再进行任何操作。  
返回完成所有重复移除后的最终字符串。可以证明答案唯一。

示例 1:  
输入: `s = "abbaca"`  
输出: `"ca"`  
解释:  
在 `"abbaca"` 中可以移除 `"bb"`（因为这两个字符相邻且相等），这是唯一可以进行的操作。此操作后字符串变为 `"aaca"`，其中只能再移除 `"aa"`，最终得到的字符串是 `"ca"`。

示例 2:  
输入: `s = "azxxzy"`  
输出: `"ay"`  

约束条件：  
- `1 <= s.length <= 10^5`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**一次遍历字符串，找到相邻且相同的两个字符就把它们删掉**，然后把剩下的字符重新拼成新字符串，再继续这个过程，直到再也找不到相邻相同的字符为止。

- **使用的数据结构**：我们只需要一个普通的 Python `list`（或者直接用字符串）来保存当前的字符序列。可以把它想象成一块可编辑的纸，随时在上面删除两个相邻的字母。
- **为什么正确**：题目要求“不断地”进行相邻相同字符的删除，只要我们每一步都把所有可以删除的相邻相同字符删掉，最终得到的字符串一定是题目要求的唯一答案。因为每一次删除都不影响已经确定不能再删的部分，只会让后面的字符更靠近，从而可能产生新的可删对。
- **时间/空间复杂度**：  
  - 每一次遍历我们都要检查整个字符串，最坏情况下每次只能删掉一对字符，字符串长度 `n` 需要 `n/2` 次遍历才能结束，时间复杂度约为 `O(n²)`。  
  - 只用到了原始字符串和临时的几个变量，空间复杂度是 `O(1)`（不计返回结果的空间）。

#### 代码（Python）

```python
def removeDuplicates_brute(s: str) -> str:
    # 把字符串转换成列表，方便原地删除
    chars = list(s)
    while True:
        i = 0
        changed = False          # 本轮遍历是否删掉了字符
        # 从左到右检查相邻字符
        while i < len(chars) - 1:
            if chars[i] == chars[i + 1]:
                # 删除这两个相邻相同的字符
                del chars[i:i + 2]
                changed = True
                # 删除后，前面的字符已经和后面的靠近，
                # 继续检查当前位置（不需要 i += 1）
            else:
                i += 1
        if not changed:          # 本轮没有任何删除，说明结束
            break
    return ''.join(chars)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 想象 `n = 1000`，每次只能删掉最左边的一对字符，需要遍历约 1000 次，每次遍历又要检查 `≈1000` 个字符，总共接近 `10⁶` 次比较，这就是平方级别的耗时。
- **空间复杂度**：`O(1)`（不计返回值）  
  - 只用了原始字符列表和几个指针变量，额外占用的内存不随 `n` 增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次删除后都要重新从头遍历**，导致大量重复检查。我们可以把“已处理好且不可能再产生相邻相同字符的部分”保存起来，这样后面再来新字符时，只需要和最近的一个字符比较即可。

这正是**栈（Stack）**的典型用法：

1. 从左到右遍历字符串的每个字符 `c`。  
2. 查看栈顶（即最近保留下来的字符）是否和 `c` 相同。  
   - 若相同，则说明出现了相邻相同的两字符，直接 **弹出栈顶**（相当于把这对字符一起删掉），不把 `c` 放进栈。  
   - 若不同，则把 `c` **压入栈**，因为它暂时没有相邻相同的伙伴。  
3. 遍历结束后，栈中从底到顶的字符就是最终的字符串。

- **为什么正确**：栈始终保持“已经确定不会再和后面的字符形成相邻相同对”的序列。每当遇到相同字符时，立即消除这对字符，这等价于题目中“立即删除”。因为我们是从左到右一次性处理，每次删除后新出现的相邻字符恰好是栈顶与当前字符的比较结果，所以不会遗漏任何一步。  
- **类比**：把栈想象成一条**流水线**，每个新来的字母要先和“前面最后一个留下的字母”检查是否相同，若相同就一起被“机器”吞掉，若不同就继续排在队伍后面等待后面的字母来检查。

#### 代码（Python）

```python
def removeDuplicates(s: str) -> str:
    stack = []                     # 用列表实现栈，栈底在左侧，栈顶在右侧
    for ch in s:                  # 依次处理每个字符
        if stack and stack[-1] == ch:
            # 栈顶字符与当前字符相同，弹出栈顶，实现“相邻相同字符删除”
            stack.pop()
        else:
            # 不相同，保留当前字符，压入栈顶
            stack.append(ch)
    # 栈中剩余的字符顺序即为答案
    return ''.join(stack)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个字符至多进栈一次、出栈一次，总操作次数不超过 `2n`，即线性时间。与暴力解的 `O(n²)` 相比，速度提升了好几个数量级（例如 `n=10⁵` 时，`O(n²)` 已不可接受，而 `O(n)` 仍在毫秒级）。
- **空间复杂度**：`O(n)`  
  - 最坏情况下（没有任何相邻相同字符）所有字符都会留在栈里，需要 `n` 的额外空间。这里的空间是用来保存答案的，属于必需的。

---

## 心得

- **核心技巧**：利用栈（或等价的“模拟栈的列表”）一次遍历完成所有相邻相同字符的消除。
- **适用的题型**：  
  1. “删除相邻相同字符”系列，如 *Remove All Adjacent Duplicates In String II*（需要删除 `k` 个相同字符）。  
  2. “括号匹配”“表达式求值”等需要**配对**或**回溯**的字符串处理题。  
  3. “逆波兰表达式求值”这类需要**后进先出**的场景。
- **一句话总结**：**相邻相同就立即消除，用栈把“已确定安全”的字符保存下来**。

## 反思

- **第一反应**：看到“相邻相同字符删除”，立刻想到遍历并每次删掉，忽略了重复遍历的代价。  
- **最容易踩的坑**：  
  - 忘记在相同字符出现时**不把当前字符再压栈**，导致错误的重复计数。  
  - 对空字符串或全部字符相同的极端情况没有考虑，可能出现索引错误。  
- **下次类似题的第一步**：先判断**是否可以用栈一次遍历完成**——把“已经处理好的部分”保存在栈里，只和最新元素比较，避免二次遍历。