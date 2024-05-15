# #2696. 最小字符串长度（删除子串后） / Minimum String Length After Removing Substrings

> 难度：简单 · 标签：String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/minimum-string-length-after-removing-substrings/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting only of uppercase English letters.
You can apply some operations to this string where, in one operation, you can remove any occurrence of one of the substrings "AB" or "CD" from s.
Return the minimum possible length of the resulting string that you can obtain.
Note that the string concatenates after removing the substring and could produce new "AB" or "CD" substrings.

**Examples**

**Example 1:**

```
Input: s = "ABFCACDB"
Output: 2
Explanation: We can do the following operations:
- Remove the substring "ABFCACDB", so s = "FCACDB".
- Remove the substring "FCACDB", so s = "FCAB".
- Remove the substring "FCAB", so s = "FC".
So the resulting length of the string is 2.
It can be shown that it is the minimum length that we can obtain.
```

**Example 2:**

```
Input: s = "ACBBD"
Output: 5
Explanation: We cannot do any operations on the string so the length remains the same.
```

**Constraints**

- 1 <= s.length <= 100
- s consists only of uppercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅由大写英文字母组成的字符串 `s`。  
你可以对该字符串进行若干次操作，每次操作可以删除字符串中任意出现的子串（substring） `"AB"` 或 `"CD"`。  
返回通过上述操作后可以得到的最小可能长度。

**说明**  
删除子串后，字符串会重新连接，新的相邻字符可能会形成新的 `"AB"` 或 `"CD"` 子串，进而可以继续删除。

**示例 1**  
输入：`s = "ABFCACDB"`  
输出：`2`  
解释：我们可以按以下步骤进行操作：  
- 删除子串 `"AB"`，得到 `s = "FCACDB"`。  
- 删除子串 `"CD"`，得到 `s = "FCAB"`。  
- 删除子串 `"AB"`，得到 `s = "FC"`。  
最终字符串长度为 `2`，可以证明这是能够得到的最小长度。

**示例 2**  
输入：`s = "ACBBD"`  
输出：`5`  
解释：字符串中不存在 `"AB"` 或 `"CD"` 子串，无法进行任何操作，长度保持不变。

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由大写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**一次遍历整条字符串，找到所有出现的 “AB” 或 “CD”，把它们删掉**，然后把剩下的字符拼接成新串，再继续同样的过程，直到找不到可以删除的子串为止。  

- **使用的数据结构**：我们只需要一个普通的 Python `str`（相当于一行文字），以及在每次遍历时记录是否有删除发生的布尔变量。可以把 `str` 想象成一条纸带，手里拿着剪刀，遍历时一旦看到 “AB” 或 “CD” 就剪掉这两个字符，剩下的字符自动靠拢（就像把剪掉的纸片撕掉后，两边的纸会自然粘在一起）。
- **为什么正确**：题目允许**任意次**执行删除操作，只要还有 “AB” 或 “CD” 就可以继续。暴力遍历不断把所有能删的子串一次性清除，等到没有可删的子串时，得到的就是一种**合法的最终状态**。因为每一步都是真实可以执行的操作，最终长度一定是可达的。题目要求的是 **最小** 长度，而该过程一直删到不能再删，显然已经达到最小（如果还能删就说明还没有达到极限）。
- **时间/空间复杂度**：  
  - 每一次完整遍历需要 O(n) 的时间（n 为当前字符串长度），而每次删除至少会让长度减 2。最坏情况下，字符串长度从 100 逐步减到 0，需要进行约 50 次遍历，所以总体时间复杂度是 O(n²)。  
  - 只用了原来的字符串和几个临时变量，额外空间是 O(1)。

> **大白话解释**：  
> - O(n²) 就像在 100 本书里每本都要翻 100 次页，总共 10 000 次操作。对本题的规模（n ≤ 100）来说还能接受，但如果 n 达到几千甚至几万，就会变得很慢。

#### 代码（Python）

```python
def minLength_bruteforce(s: str) -> int:
    """
    暴力解：不断遍历字符串，删除所有出现的 "AB" 或 "CD"
    直到再也找不到为止，返回剩余字符的长度。
    """
    while True:                       # 循环直到没有任何删除发生
        i = 0
        new_chars = []                # 用列表收集本轮遍历后保留下来的字符
        removed = False               # 标记本轮是否删掉了子串

        while i < len(s):
            # 检查当前位置及下一位是否构成 "AB" 或 "CD"
            if i + 1 < len(s) and (s[i] == 'A' and s[i+1] == 'B' or
                                   s[i] == 'C' and s[i+1] == 'D'):
                # 找到可删除的子串，直接跳过这两个字符
                i += 2
                removed = True
            else:
                # 否则保留下当前字符
                new_chars.append(s[i])
                i += 1

        # 把列表转回字符串，准备进入下一轮
        s = ''.join(new_chars)

        if not removed:               # 本轮没有删掉任何东西，说明结束
            break

    return len(s)
```

#### 复杂度

- **时间复杂度**：O(n²)  
  - 解释：每次遍历是 O(n)，最多会进行约 n/2 次（因为每次至少删掉 2 个字符），所以总体是 n × n/2 ≈ n²。
- **空间复杂度**：O(1)（不计返回值的字符数组）  
  - 解释：只用了几个指针和一个临时列表，列表的大小始终不超过原字符串长度。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次遍历都要从头扫描**，即使大多数字符已经确定不会再被删除，也要重新检查。我们可以把**“已经确定不会再被删的字符”**提前锁定，这正是 **栈**（后进先出）的天然特性。

**关键观察**：

1. 删除的子串长度固定为 2，且只能是 “AB” 或 “CD”。  
2. 当我们从左到右逐字符处理时，只有**当前字符和栈顶字符**可能组成可删除的子串。  
3. 一旦栈顶的字符与新来的字符不能形成 “AB” 或 “CD”，这个栈顶字符就永远不可能再被删掉（因为后面的字符只能在它右侧出现，无法再把它和左侧的字符配对）。于是它可以安全地留在栈中。

**由此得到的算法**：

- 初始化一个空栈 `stack`（用 Python 列表实现）。  
- 依次遍历字符串的每个字符 `c`：
  - 如果栈不为空且栈顶 `top` 与 `c` 形成 “AB” 或 “CD”，则弹出栈顶（相当于把这两个字符一起删掉），**不把 `c` 入栈**。  
  - 否则，把 `c` 推入栈中。  
- 遍历结束后，栈中剩下的字符就是 **无法再进一步删除的字符**，栈的长度即为答案。

**为什么这个过程等价于暴力的“反复删”**：

- 栈的弹出操作对应一次 “AB”/“CD” 删除。  
- 由于我们是 **即时** 判断能否删除（而不是等整条字符串遍历完后再统一删除），所以每一次弹出都保证了后面的字符已经看到并决定是否配对。  
- 这正好模拟了暴力解中“先删左边的子串，再让右边字符靠拢”的过程，只是把“靠拢”这一步用栈的结构自然完成。

**类比**：想象一列火车车厢，每当新的车厢进入时，检查它与前面最后一节车厢是否能“碰撞消失”（AB 或 CD），如果可以，两节车厢直接消失；否则，这节车厢就永久停在列车末端，后面的车厢只能在它后面排队。

#### 代码（Python）

```python
def minLength_optimal(s: str) -> int:
    """
    栈解法：一次遍历完成所有可能的删除，返回最终栈的大小即最小长度。
    """
    stack = []                     # 用列表当作栈，stack[-1] 为栈顶

    for c in s:                    # 从左到右逐字符处理
        if stack:
            top = stack[-1]        # 取出当前栈顶字符
            # 检查是否构成可删除的子串 "AB" 或 "CD"
            if (top == 'A' and c == 'B') or (top == 'C' and c == 'D'):
                stack.pop()       # 弹出栈顶，等价于把 top 和 c 同时删除
                continue          # 当前字符已被消除，无需入栈
        # 不能删除的情况，直接把当前字符压入栈中
        stack.append(c)

    return len(stack)              # 栈中剩余字符的个数即最小可能长度
```

#### 复杂度

- **时间复杂度**：O(n)  
  - 解释：每个字符最多被压入栈一次，又可能被弹出一次，总操作次数和字符串长度成正比。相比暴力的 O(n²)，这里是线性时间，哪怕 n 达到几万也能轻松跑完。
- **空间复杂度**：O(n)（最坏情况下栈会存下全部字符）  
  - 解释：如果字符串里根本没有 “AB” 或 “CD”，栈会保存所有字符，此时占用的额外空间就是原字符串长度的大小。

---

## 心得

- **核心技巧**：**利用栈实现一次遍历的“消除”**。这是一种常见的“配对消除”思路，适用于所有只涉及相邻字符删除的题目。
- **相似题型**（可再练习）：
  1. **LeetCode 1047. Remove All Adjacent Duplicates In String** – 删除相邻相同字符。
  2. **LeetCode 1657. Determine if Two Strings Are Close**（部分思路）或 **LeetCode 1003. Check If Word Is Valid After Substitutions** – 使用栈检查特定模式的消除。
  3. **LeetCode 1455. Check If a Word Occurs As a Prefix of Any Word in a Sentence**（思路类似的字符匹配）。
- **一句话总结**：**把“左边的字符 + 当前字符”看成一次可能的消除，栈自然完成“左边记忆 + 立即配对”。**

---

## 反思

- **第一反应**：看到“可以删除子串 AB 或 CD”，立刻想到暴力遍历并不断删，甚至想尝试递归或回溯搜索所有删除顺序。
- **最容易踩的坑**：
  - **忘记“删除后字符串会收缩”**：若只在一次遍历中删掉出现的子串，却不再继续检查新产生的子串，会得到错误的结果。  
  - **边界条件**：空字符串或只剩一个字符时，栈操作仍需安全（不能弹出空栈）。  
  - **误把“AB”和“BA”混淆**：只有严格的顺序 “A” 紧跟 “B” 才能删，顺序反了不行。
- **下次遇到同类题**，第一步应该先问自己：**“是否只涉及相邻字符的配对删除？”** 如果答案是肯定的，立刻考虑 **栈** 或 **双指针** 的线性解法，而不是直接写暴力的循环。