# #1717. 移除子串的最大得分 / Maximum Score From Removing Substrings

> 难度：中等 · 标签：String、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-score-from-removing-substrings/)

---

## 题目（英文原版）

**Description**

You are given a string s and two integers x and y. You can perform two types of operations any number of times.
Return the maximum points you can gain after applying the above operations on s.

**Examples**

**Example 1:**

```
Input: s = "cdbcbbaaabab", x = 4, y = 5
Output: 19
Explanation:
- Remove the "ba" underlined in "cdbcbbaaabab". Now, s = "cdbcbbaaab" and 5 points are added to the score.
- Remove the "ab" underlined in "cdbcbbaaab". Now, s = "cdbcbbaa" and 4 points are added to the score.
- Remove the "ba" underlined in "cdbcbbaa". Now, s = "cdbcba" and 5 points are added to the score.
- Remove the "ba" underlined in "cdbcba". Now, s = "cdbc" and 5 points are added to the score.
Total score = 5 + 4 + 5 + 5 = 19.
```

**Example 2:**

```
Input: s = "aabbaaxybbaabb", x = 5, y = 4
Output: 20
```

**Constraints**

- 1 <= s.length <= 105
- 1 <= x, y <= 104
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串（string）`s` 和两个整数（integer）`x`、`y`。你可以任意次数地执行以下两种操作：

1. 删除子串（substring）`"ab"`，并获得 `x` 分。
2. 删除子串（substring）`"ba"`，并获得 `y` 分。

返回在对 `s` 进行上述操作后能够获得的最大分数（points）。

**示例 1**  

**输入**  
``` 
s = "cdbcbbaaabab", x = 4, y = 5
```  

**输出**  
```
19
```  

**解释**  
- 删除 `cdbcbbaaabab` 中下划线标出的 **"ba"**，此时 `s = "cdbcbbaaab"`，得分增加 `5` 分。  
- 删除 `cdbcbbaaab` 中下划线标出的 **"ab"**，此时 `s = "cdbcbbaa"`，得分增加 `4` 分。  
- 删除 `cdbcbbaa` 中下划线标出的 **"ba"**，此时 `s = "cdbcba"`，得分增加 `5` 分。  
- 删除 `cdbcba` 中下划线标出的 **"ba"**，此时 `s = "cdbc"`，得分增加 `5` 分。  
- 删除 `cdbc` 中下划线标出的 **"ab"**（不存在），因此停止。  
（已截断）

**示例 2**  

**输入**  
``` 
s = "aabbaaxybbaabb", x = 5, y = 4
```  

**输出**  
```
20
```  

（此示例暂无解释）

**约束条件**  
- `1 <= s.length <= 10^5`  
- `1 <= x, y <= 10^4`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **不停地在字符串里找** 可以被删除的子串 `"ab"` 或 `"ba"`，每找到一次就把它删除、累计对应的分数，然后把得到的新字符串继续往下查。  
- **数据结构**：只需要一个普通的 Python `str`，因为我们每次都要把子串切掉。可以把它想象成 **剪纸**：把一段纸（子串）剪掉，剩下的纸继续剪。
- **为什么正确**：只要把所有出现的合法子串都删掉，最终的得分一定是一次合法操作序列的总和。暴力搜索遍历了所有可能的删除顺序（虽然实际实现时只会走一种顺序），只要每一步都合法，最后的得分一定是可达的。
- **时间/空间复杂度**：  
  - 每次搜索子串都要遍历整条字符串，最坏情况要 **O(n)**。删掉一个子串后，字符串长度会变短，但最坏情况下我们可能要删 **O(n)** 次（每次只删掉两个字符），于是总时间是 **O(n × n) = O(n²)**。  
  - 只使用了原始字符串本身和临时的切片，空间复杂度是 **O(1)**（不计输入本身）。

> **大白话**：  
> - `O(n²)` 就好比你在一条长队里找两个人站在一起，每找一次都要从头排队数过去，排队的次数和人数都乘起来，工作量会“爆炸”。

#### 代码（Python）

```python
def maxScore_bruteforce(s: str, x: int, y: int) -> int:
    score = 0
    # 为了让代码更易懂，用 while 循环不停地尝试删除
    while True:
        changed = False               # 本轮是否真的删掉了子串
        # 先尝试删除得分更高的子串，这样可以保证至少不比最优差太多
        high, low = ("ab", x), ("ba", y) if x >= y else ("ba", y), ("ab", x)

        # 删除所有 high 类型的子串
        i = 0
        while i < len(s) - 1:
            if s[i:i+2] == high[0]:
                s = s[:i] + s[i+2:]   # 把 i、i+1 两个字符剪掉
                score += high[1]
                changed = True
                # 删除后 i 位置的字符已经是新字符，继续从同一个位置检查
            else:
                i += 1

        # 再删除 low 类型的子串
        i = 0
        while i < len(s) - 1:
            if s[i:i+2] == low[0]:
                s = s[:i] + s[i+2:]
                score += low[1]
                changed = True
            else:
                i += 1

        if not changed:               # 本轮没有任何删除，说明已经无法继续
            break
    return score
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每次遍历整个字符串（`O(n)`），最坏要删 `n/2` 次，所以乘起来是 `n × n`。
- **空间复杂度**：`O(1)` —— 只用了常数级的额外变量（`score、i、changed`），字符串本身在原地改写。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要 **从头遍历** 整条字符串，导致二次方的时间。  
观察题目可以发现：

1. 两种子串 `"ab"` 与 `"ba"` 互不重叠（它们的字符顺序不同），一次删除只能影响相邻的两个字符。  
2. **先删分值更高的子串总是不会让后面的得分变少**。因为删除高分子串后，只会让相邻字符更靠近，最多会产生新的低分子串，绝不会把已经存在的高分子串“吞掉”。  
3. 只需要 **一次线性扫描** 来把所有高分子串删掉，再一次线性扫描删低分子串。  
   - 线性扫描可以用 **栈**（stack）来实现：遍历字符，把它压入栈；每压入一个字符后检查栈顶的两个字符是否构成我们要删除的子串。如果是，就弹出这两个字符（相当于把子串删掉），并累计分数。

**实现细节**（以 `x >= y` 为例，先删 `"ab"`）：

- 第一次遍历：目标子串是 `"ab"`，分值 `x`。  
  - 用一个栈 `stack1` 保存已经处理好的字符。  
  - 当读取到字符 `c` 时，若 `stack1` 非空且 `stack1[-1] + c == "ab"`，则弹出栈顶字符（即把 `"ab"` 删除），`score += x`；否则把 `c` 压入栈。  
- 此时栈 `stack1` 中剩下的字符已经不含 `"ab"`，但可能出现 `"ba"`。把 `stack1` 的内容转成字符串（或直接在第二次遍历时继续使用栈），再用相同的方式、目标子串改为 `"ba"`、分值 `y`，得到最终得分。

如果 `y > x`，只需要把顺序换一下：先删 `"ba"`（高分），再删 `"ab"`（低分）。

> **类比**：  
> 想象有一条生产线，产品在上面移动。我们在生产线的两端放了“检测器”。当检测器发现相邻的两个部件能组成高价值的组合时，就立即把它们“抓走”。这样整个生产线只需要一次前进，就完成了所有高价值的抓取，随后再一次前进处理剩下的低价值组合。

#### 代码（Python）

```python
def maxScore(s: str, x: int, y: int) -> int:
    """
    贪心 + 栈的线性解法
    先删分值更高的子串，再删另一种子串
    """
    # 统一把「先删」的子串记为 first, 其得分为 first_val
    if x >= y:
        first, first_val = "ab", x
        second, second_val = "ba", y
    else:
        first, first_val = "ba", y
        second, second_val = "ab", x

    # ---------- 第一次遍历：删除 first ----------
    stack = []               # 用列表模拟栈，stack[-1] 是栈顶
    score = 0
    for ch in s:
        # 检查栈顶 + 当前字符 是否恰好是我们要删除的子串
        if stack and stack[-1] + ch == first:
            stack.pop()      # 弹出栈顶字符，等价于把两个字符一起删掉
            score += first_val
        else:
            stack.append(ch) # 否则把当前字符压入栈，等待后面的匹配

    # ---------- 第二次遍历：删除 second ----------
    # 此时 stack 中不含 first 子串，但可能含 second 子串
    # 再用一个新栈继续处理
    new_stack = []
    for ch in stack:          # 直接遍历残留的字符序列
        if new_stack and new_stack[-1] + ch == second:
            new_stack.pop()
            score += second_val
        else:
            new_stack.append(ch)

    return score
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 两次线性遍历，每次只做常数次栈操作。相当于只走了一遍字符串，远比 `O(n²)` 快。  
- **空间复杂度**：`O(n)` —— 最坏情况下栈会保存全部字符（比如没有任何匹配子串时），所以需要线性额外空间。  

> 与暴力解对比：时间从“每次都从头找” 的 `O(n²)` 降到了“一次遍历就搞定” 的 `O(n)`，在长度 10⁵ 的输入下差距相当于 **秒级** vs **几分钟**。

---

## 心得

- **核心技巧**：**先删高分子串、后删低分子串** 的贪心思路 + **栈模拟相邻字符消除**。  
- **适用的题型**：  
  1. “删除指定相邻字符并计分” 类问题（如 LeetCode 1658 `Maximum Total Score From Stacking` 的变形）。  
  2. “相邻字符抵消” 类问题（如 LeetCode 1047 `Remove All Adjacent Duplicates In String`）。  
  3. “字符串消除后再处理” 的双阶段贪心（如 LeetCode 1544 `Make The String Great`）。  
- **一句话总结**：**把价值大的“先吃”，用栈一次扫完，再处理剩下的价值小的**，是这类“相邻子串消除”问题的钥匙。

---

## 反思

- **第一反应**：看到可以无限次删除子串，立刻想到“遍历找、删掉、再找”，于是写出了暴力的循环。  
- **最容易踩的坑**：  
  - **先后顺序**：如果不先处理高分子串，可能会把本来可以得到的高分子串“埋”在低分子串里，导致得分下降。  
  - **边界字符**：栈顶检查时必须确保栈非空，否则会越界。  
  - **字符串长度大**：暴力 `O(n²)` 在 10⁵ 长度下会超时，需要及时想到线性栈方案。  
- **下次遇到同类题**：第一步先 **比较两种操作的得分**，确定“先删哪一种”。随后 **用栈一次遍历把这种子串全部消掉**，再对剩余字符做第二遍遍历处理另一种子串。这样就能保证时间线性、得分最大。