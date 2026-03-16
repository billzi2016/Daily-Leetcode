# #3561. 相邻字符删除后的结果字符串 / Resulting String After Adjacent Removals

> 难度：中等 · 标签：String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/resulting-string-after-adjacent-removals/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters.
You must repeatedly perform the following operation while the string s has at least two consecutive characters:
Return the resulting string after no more operations can be performed.
Note: Consider the alphabet as circular, thus 'a' and 'z' are consecutive.

**Examples**

**Example 1:**

```
Input: s = "abc"
Output: "c"
Explanation:
```

**Example 2:**

```
Input: s = "adcb"
Output: ""
Explanation:
```

**Example 3:**

```
Input: s = "zadb"
Output: "db"
Explanation:
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串（string） `s`。  
当字符串 `s` 至少存在一对相邻字符时，你必须重复执行以下操作，直至无法再进行任何操作为止。  
返回无法再进行操作时的结果字符串。  

**注意**：字母表视为循环的，即 `'a'` 与 `'z'` 被视为相邻字符。

### 示例

**示例 1**  
Input: `s = "abc"`  
Output: `"c"`  
解释：

**示例 2**  
Input: `s = "adcb"`  
Output: `""`  
解释：

**示例 3**  
Input: `s = "zadb"`  
Output: `"db"`  
解释：

### 约束条件

- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**一次遍历整个字符串，找到任意一对相邻且字母顺序相差 1（`a` 与 `z` 也算相邻）的字符，直接把这两个字符删掉**，然后把剩下的字符重新拼接成新字符串，再继续上述过程，直到整段字符串里已经没有相邻的“相邻字符”了。

- **用到的数据结构**：只需要普通的 Python 字符串（或列表）来保存当前的字符序列。可以把它想象成一行排好的字母，手动把相邻的两块“相邻字母”剪掉，就像在纸上用橡皮擦掉相邻的两个字母一样。
- **为什么正确**：题目要求**反复**执行“相邻字符消除”操作，只要我们每一次都找到了一个合法的相邻对并把它们删掉，剩下的字符顺序不变，后续的消除仍然可以在新的字符串上继续进行。只要没有可删的相邻对，说明已经达到了题目要求的最终状态。
- **时间/空间复杂度**：  
  - 每一次遍历我们都要检查全部字符（最坏 `O(n)`），而每一次成功删除会让字符串长度减少 2。最坏情况下，可能需要进行 `n/2` 次遍历（每次只删掉最左边的一对），于是总体时间是 `O(n²)`。  
  - 只用了原字符串本身或临时的几个额外变量，空间是 `O(1)`（不计返回结果的存储）。

> **大白话**：`O(n²)` 就像你在一条长长的队伍里，反复从头到尾找一对可以一起离开的兄弟，两个人走后你又得从头再找一次。每找一次都要走完整条队伍，次数又跟队伍长度成正比，所以总工作量是“队伍长度 × 队伍长度”。

#### 代码（Python）

```python
def remove_adjacent_bruteforce(s: str) -> str:
    # 把字符串转成列表，方便原地删除
    chars = list(s)

    # 循环直到一次遍历也没有删除任何字符
    while True:
        i = 0               # 当前检查的下标
        deleted = False     # 本轮是否删掉了字符

        # 从左到右检查相邻字符
        while i < len(chars) - 1:
            cur = chars[i]
            nxt = chars[i + 1]

            # 判断两字符是否相邻（考虑 a 与 z 的环形相邻）
            diff = abs(ord(cur) - ord(nxt))
            if diff == 1 or diff == 25:   # 25 = |ord('a')-ord('z')|
                # 删除这两个字符
                del chars[i:i + 2]
                deleted = True
                # 删除后，左侧的字符已经和新的右侧相邻，i 不需要加 1
                continue
            i += 1

        # 如果本轮没有任何删除，说明已经是最终结果
        if not deleted:
            break

    return ''.join(chars)
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每一次遍历 `O(n)`，最坏会进行 `O(n)` 次遍历。  
- **空间复杂度**：`O(1)`（不计返回的结果字符串）。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每次删除后都要重新从头遍历**，导致大量重复检查。  
其实我们只需要一次线性扫描就能完成所有删除：  

1. **从左到右读字符**，把已经“确认不会再被删除”的字符放进一个栈（可以用 Python 列表实现）。  
2. 当读到新字符 `c` 时，检查栈顶的字符 `top` 是否和 `c` 是相邻字母（包括 `a` 与 `z`）。  
   - **如果相邻**：说明这两个字符可以立刻消除，于是把栈顶弹出（`pop`），并且**不把 `c` 放进栈**。这一步相当于把这对相邻字符直接“擦掉”。  
   - **如果不相邻**：则把 `c` 推入栈中（`push`），因为它暂时没有可以消除的伙伴。  
3. 整个过程结束后，栈里留下的字符顺序正好就是**无法再消除的最终字符串**。  

为什么一次遍历就够了？  
- 栈顶始终保存的是**最近的、还未被配对的字符**。如果它和当前字符不相邻，说明无论后面再出现什么字符，都不可能把这两个字符配对（因为配对只能在相邻位置），所以它可以安全地留在栈里。  
- 当栈顶与当前字符相邻时，它们立刻配对消除，后面的字符会再次和新的栈顶比较，这正好模拟了“连续消除”的过程。

**核心数据结构：栈**（在 Python 中用 `list` 实现）。  
- 栈就像一个**“后进先出”的盒子**，我们把字符一个接一个放进去，遇到可以消除的情况就把最近放进去的字符（栈顶）拿出来，正好符合题目“相邻消除”的要求。  

**相邻判断**：  
两个小写字母 `x`、`y` 相邻当且仅当它们的 ASCII 码差的绝对值是 `1`，或者它们是 `a` 与 `z`（因为字母是循环的）。可以用下面的条件表达：

```python
diff = abs(ord(x) - ord(y))
if diff == 1 or diff == 25:   # 25 = |ord('a') - ord('z')|
    # 相邻
```

#### 代码（Python）

```python
def resulting_string(s: str) -> str:
    """
    使用栈一次遍历完成所有相邻字符的消除。
    """
    stack = []  # 用列表模拟栈

    for ch in s:
        if stack:
            top = stack[-1]                     # 取栈顶元素（最近的未匹配字符）
            diff = abs(ord(top) - ord(ch))
            # 判断 top 与 ch 是否相邻（包括 a 与 z）
            if diff == 1 or diff == 25:
                stack.pop()                     # 两字符相邻，直接消除
                continue                        # 当前字符已被消除，不入栈
        # 若没有相邻配对，或栈为空，则把当前字符压入栈
        stack.append(ch)

    # 栈中剩余的字符顺序即为最终答案
    return ''.join(stack)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，每个字符至多进栈一次、出栈一次。  
- **空间复杂度**：`O(n)` —— 最坏情况下没有任何字符可以配对，所有字符都保存在栈中。  

> 与暴力解相比，时间从 “每次都要重新扫描整条队伍” 降到了 “一次走完所有人”，快了几个数量级。

---

## 心得  

- **核心技巧**：**栈 + 相邻判断**，利用栈的后进先出特性一次遍历完成“相邻消除”。  
- **适用的题型**：  
  1. “相邻字符消除”类（如 LeetCode 1047 Remove All Adjacent Duplicates of Size K）。  
  2. “括号匹配 / 有效字符序列”类（如 Valid Parentheses）。  
  3. “单调栈”或“最近更大/更小元素”类问题（如 Next Greater Element）。  
- **解题钥匙**：**把“相邻消除”抽象成“栈顶与当前元素是否匹配”，匹配则弹栈，不匹配则压栈**。

---

## 反思  

- **第一反应**：看到“反复删除相邻字符”，自然想到**循环遍历 + 删除**，这就是暴力思路。  
- **最容易踩的坑**：  
  - **环形相邻**：忘记 `a` 与 `z` 也是相邻，导致判断条件出错。  
  - **删除后索引移动**：暴力实现时要小心在删除后继续检查新的相邻对，容易出现越界或遗漏。  
  - **大输入**：直接使用 `str.replace` 或频繁的字符串拼接会导致 `O(n²)` 超时。  
- **下次类似题目第一步**：**先思考是否可以用栈模拟“配对/消除”过程**，如果可以，立刻尝试写出“一次遍历”的方案。这样往往能直接得到最优解。