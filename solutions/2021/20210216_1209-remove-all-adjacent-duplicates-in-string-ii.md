# #1209. 删除字符串中的所有相邻重复字符 II / Remove All Adjacent Duplicates in String II

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k, a k duplicate removal consists of choosing k adjacent and equal letters from s and removing them, causing the left and the right side of the deleted substring to concatenate together.
We repeatedly make k duplicate removals on s until we no longer can.
Return the final string after all such duplicate removals have been made. It is guaranteed that the answer is unique.

**Examples**

**Example 1:**

```
Input: s = "abcd", k = 2
Output: "abcd"
Explanation: There's nothing to delete.
```

**Example 2:**

```
Input: s = "deeedbbcccbdaa", k = 3
Output: "aa"
Explanation: 
First delete "eee" and "ccc", get "ddbbbdaa"
Then delete "bbb", get "dddaa"
Finally delete "ddd", get "aa"
```

**Example 3:**

```
Input: s = "pbbcggttciiippooaais", k = 2
Output: "ps"
```

**Constraints**

- 1 <= s.length <= 105
- 2 <= k <= 104
- s only contains lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，**k 重复删除**（k duplicate removal）指的是从 `s` 中选取 `k` 个相邻且相同的字符并将其移除，移除后左侧和右侧的子串会**连接**（concatenate）在一起。  
我们对 `s` 反复执行 **k 重复删除**，直到无法再进行为止。  
返回完成所有删除操作后的最终字符串。题目保证答案唯一。

## 示例

### 示例 1
**输入**: `s = "abcd", k = 2`  
**输出**: `"abcd"`  
**解释**: 没有可以删除的字符。

### 示例 2
**输入**: `s = "deeedbbcccbdaa", k = 3`  
**输出**: `"aa"`  
**解释**:  
- 首先删除 `"eee"` 和 `"ccc"`，得到 `"ddbbbdaa"`  
- 然后删除 `"bbb"`，得到 `"dddaa"`  
- 最后删除 `"ddd"`，得到 `"aa"`

### 示例 3
**输入**: `s = "pbbcggttciiippooaais", k = 2`  
**输出**: `"ps"`  

## 约束条件
- `1 <= s.length <= 10^5`
- `2 <= k <= 10^4`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次遍历整条字符串**，寻找连续出现 `k` 次的相同字符并把它们删掉，然后把左侧和右侧拼接起来，再继续搜索。可以把这一步看成：

1. 从左到右扫描，记录当前字符出现了几次（`cnt`）。
2. 当 `cnt == k` 时，把这 `k` 个字符从字符串中删除。
3. 删除后，指针需要往左退 `k` 步，因为左边可能刚好形成新的 `k` 连续相同字符（比如 `"aaabbb"` 删除 `bbb` 后，左边的 `aaa` 仍然需要检查）。
4. 重复上述过程，直到遍历完整个字符串且没有再出现可以删除的 `k` 连续字符。

> **生活化类比**：想象你在一本笔记本上划线找相同的单词，找到 `k` 个相邻相同的单词后直接用橡皮擦掉，然后把前后两页的纸粘在一起继续找。每次擦完都要把手指往回退一点，防止漏掉新出现的相同单词。

**为什么正确**：只要我们每次都把出现的 `k` 连续字符全部删掉，最终的字符串一定是“没有任何 `k` 连续相同字符的最短形态”。因为每一次删除都不会影响已经检查过的左侧字符（左侧已经不含 `k` 连续相同字符），只会把右侧字符搬到左侧来再次检查，这正是题目要求的“重复进行，直到无法再删”。

**时间/空间复杂度**：

- **时间**：最坏情况下每删掉一次 `k` 个字符，都要把指针往左退 `k` 步并重新遍历。设字符串长度为 `n`，每个字符可能被“访问”多次，最坏会达到 `O(n * k)`，在 `k` 接近 `n` 时接近 `O(n²)`。  
  - 大白话：如果你把每个字符都当作一次“检查”，但每次删掉后又要回头重新检查，那就像在跑步时每走一步都要倒退再跑一次，跑的路程会变成原来的平方级别。

- **空间**：只用了几个计数变量，额外空间是 `O(1)`（不计原字符串本身）。

#### 代码（Python）

```python
def removeDuplicates_bruteforce(s: str, k: int) -> str:
    # 把字符串转成列表，方便原地删除
    lst = list(s)
    i = 0                      # 当前检查的位置
    while i < len(lst):
        # 统计从 i 开始连续相同字符的数量
        cnt = 1
        while i + cnt < len(lst) and lst[i + cnt] == lst[i]:
            cnt += 1

        if cnt >= k:            # 找到至少 k 个相同字符
            # 删除前 k 个（因为只要恰好 k 连续就能删，剩下的继续检查）
            del lst[i:i + k]
            # 删除后需要把指针往左退 k 步，防止左侧新形成 k 连续
            i = max(i - k, 0)
        else:
            # 当前字符不够 k 个，直接跳到下一个位置
            i += 1
    return ''.join(lst)
```

#### 复杂度

- **时间复杂度**：`O(n * k)`，在最坏情况下约等于 `O(n²)`。  
  - 含义：如果 `n=10⁴，k=10⁴`，理论上可能要检查 100 000 000 次，跑得很慢。

- **空间复杂度**：`O(1)`（不计原字符串本身），只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**频繁的左退和重新遍历是性能瓶颈**。我们需要一种数据结构，让我们在 **一次线性遍历** 时就能知道当前字符已经连续出现了多少次，并在达到 `k` 时立刻把它们“弹出”。这正是 **栈（stack）** 的用武之地。

**关键观察**：

- 当我们从左到右扫描字符时，只有 **相邻相同** 的字符才会相互影响。  
- 栈顶保存的是**最近出现的字符以及它已经连续出现的次数**。  
- 若栈顶字符与当前字符相同，则把次数加一；否则把新字符及次数 `1` 入栈。  
- 当次数恰好等于 `k` 时，说明已经形成了 `k` 连续相同字符，直接把栈顶弹出（相当于一次性删除这 `k` 个字符），不需要再回退检查左侧，因为左侧的状态已经在栈里保存好。

**为什么只需要一次遍历**：每个字符只会被 **压入** 栈一次、**弹出**（最多一次），所以整体是 `O(n)`。

**数据结构细化**：

- 栈的每个元素是一个二元组 `(char, count)`，类似 **字典里查词** 的“键值对”。  
  - `char`：字符本身。  
  - `count`：该字符在当前连续块中出现的次数。  

**类比**：想象你在排队买票，每个人手里都有一张票（字符）和他们已经排了几次（计数）。当同一个人连续排了 `k` 次，你直接把这 `k` 个人送走（弹出），不必再让后面的人回头检查。

#### 代码（Python）

```python
def removeDuplicates(s: str, k: int) -> str:
    """
    使用栈一次遍历完成删除。
    栈中每个元素为 (字符, 当前连续计数)。
    """
    stack = []                     # 空栈，准备存放 (char, cnt)

    for ch in s:                   # 从左到右遍历每个字符
        if stack and stack[-1][0] == ch:
            # 栈顶字符与当前字符相同，计数加一
            prev_char, prev_cnt = stack.pop()
            new_cnt = prev_cnt + 1
            if new_cnt < k:
                # 计数未达到 k，重新压回栈
                stack.append((ch, new_cnt))
            # 若 new_cnt == k，则直接不压回，相当于把这 k 个字符删除
        else:
            # 栈为空或栈顶字符不同，计数从 1 开始
            stack.append((ch, 1))

    # 把栈中剩余的字符展开成结果字符串
    result = []
    for ch, cnt in stack:
        result.append(ch * cnt)    # 同一个字符可能出现多次，例如 ('a',3) => "aaa"
    return ''.join(result)
```

> **关键行解释**  
> - `if stack and stack[-1][0] == ch:` 判断当前字符是否能与栈顶合并。  
> - `new_cnt = prev_cnt + 1` 计算新的连续次数。  
> - `if new_cnt < k: stack.append((ch, new_cnt))` 只有次数不足 `k` 时才保留下来；恰好 `k` 时直接丢弃，实现“一次性删除”。  

#### 复杂度

- **时间复杂度**：`O(n)`，每个字符最多压入一次、弹出一次。  
  - 含义：即使字符串长达 100 000，算法只会走 100 000 步，速度非常快。

- **空间复杂度**：`O(n)`，最坏情况下栈会保存所有字符（比如 `k` 很大，根本不触发删除）。  
  - 含义：需要额外的存储空间与原字符串等长，但这在题目限制下是可以接受的。

---

## 心得

- **核心技巧**：**使用栈保存字符及其连续计数**，在计数达到 `k` 时一次性弹出，实现线性时间删除。  
- **适用的题型**：  
  1. “Remove All Adjacent Duplicates in String” (LeetCode 1047) —— 只需要删除相邻两个相同字符（`k = 2`）。  
  2. “Simplify Path” (LeetCode 71) —— 用栈处理路径层级。  
  3. “Longest Valid Parentheses” (LeetCode 32) —— 用栈匹配括号，类似的“配对后弹出”思想。  
- **一句话总结解题钥匙**：**把“相邻相同的计数”交给栈来维护，遇到 `k` 就立刻把整块弹走**。

---

## 反思

- **第一反应**：看到“相邻 k 个相同字符就删除”，自然会想到遍历并直接删除——这就是暴力思路。  
- **最容易踩的坑**：  
  - **左侧回溯遗漏**：删除后左边可能出现新的 `k` 连续，需要回退检查，容易忘记导致错误结果。  
  - **计数溢出**：如果使用普通 `int` 累加而不及时弹出，计数会超过 `k`，导致错误的删除时机。  
  - **空栈访问**：在栈为空时直接访问 `stack[-1]` 会报错，需要先判断栈是否为空。  
- **下次遇到同类题的第一步**：**把“连续相同/配对”抽象成“栈的 push/pop”过程，先想象每个字符对应的计数是否能直接在栈里维护**。这样就能快速跳过回溯的思考，直接写出线性时间的解法。