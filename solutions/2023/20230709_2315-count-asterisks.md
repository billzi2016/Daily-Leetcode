# #2315. 统计星号 / Count Asterisks

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/count-asterisks/)

---

## 题目（英文原版）

**Description**

You are given a string s, where every two consecutive vertical bars '|' are grouped into a pair. In other words, the 1st and 2nd '|' make a pair, the 3rd and 4th '|' make a pair, and so forth.
Return the number of '*' in s, excluding the '*' between each pair of '|'.
Note that each '|' will belong to exactly one pair.

**Examples**

**Example 1:**

```
Input: s = "l|*e*et|c**o|*de|"
Output: 2
Explanation: The considered characters are underlined: "l|*e*et|c**o|*de|".
The characters between the first and second '|' are excluded from the answer.
Also, the characters between the third and fourth '|' are excluded from the answer.
There are 2 asterisks considered. Therefore, we return 2.
```

**Example 2:**

```
Input: s = "iamprogrammer"
Output: 0
Explanation: In this example, there are no asterisks in s. Therefore, we return 0.
```

**Example 3:**

```
Input: s = "yo|uar|e**|b|e***au|tifu|l"
Output: 5
Explanation: The considered characters are underlined: "yo|uar|e**|b|e***au|tifu|l". There are 5 asterisks considered. Therefore, we return 5.
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of lowercase English letters, vertical bars '|', and asterisks '*'.
- s contains an even number of vertical bars '|'.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s`，其中每两个相邻的竖线（`|`）会被视为一对。换句话说，第 1 个和第 2 个 `|` 形成一对，第 3 个和第 4 个 `|` 形成一对，依此类推。  
返回 `s` 中字符 `*` 的数量，但要排除位于每对 `|` 之间的 `*`。  
注意，每个 `|` 恰好属于唯一的一对。

**示例**  

*示例 1*  
```text
Input: s = "l|*e*et|c**o|*de|"
Output: 2
Explanation: 被计数的字符已下划线标出： "l|*e*et|c**o|*de|".  
第一个和第二个 `|` 之间的字符不计入答案，同理第三个和第四个 `|` 之间的字符也不计入。  
最终有 2 个 `*` 被计入，所以返回 2。
```

*示例 2*  
```text
Input: s = "iamprogrammer"
Output: 0
Explanation: 本例中 `s` 不包含任何 `*`，因此返回 0。
```

*示例 3*  
```text
Input: s = "yo|uar|e**|b|e***au|tifu|l"
Output: 5
Explanation: 被计数的字符已下划线标出： "yo|uar|e**|b|e***au|tifu|l".  
其中有 5 个 `*` 被计入，故返回 5。
```

**约束条件**  
- `1 <= s.length <= 1000`  
- `s` 仅由小写英文字母、竖线（`|`）和星号（`*`）组成。  
- `s` 中竖线（`|`）的数量为偶数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每遇到一个 `*`，就去检查它左边有多少个 `|`**。  
- 如果左侧出现的 `|` 数目是奇数，说明这个 `*` 位于一对 `|` 之间（因为第 1、3、5 … 个 `|` 是“打开”标记），此时不计数。  
- 如果左侧 `|` 的数量是偶数，则说明它不在任何 `|…|` 区间内，应该计入答案。

可以把 `|` 看成 **一本字典**，每翻开一页（出现一次 `|`），就进入或退出“保密区”。遍历到 `*` 时，只要查看当前已经翻开的页数是奇数还是偶数，就能判断它是否被隐藏。

**为什么正确**  
因为题目保证所有的 `|` 都成对出现，且配对顺序是按照出现顺序依次配对的。于是左侧 `|` 的奇偶性恰好对应“是否在一对 `|` 之间”。只要统计左侧 `|` 的个数，就能唯一确定 `*` 的状态。

**暴力实现**  
对每个 `*`，都向左遍历一次，统计 `|` 的数量。最坏情况下，字符串长度为 `n`，每个字符都可能是 `*`，于是会进行 `n` 次 `O(n)` 的遍历，总复杂度为 `O(n²)`。

#### 代码（Python）

```python
def countAsterisks_bruteforce(s: str) -> int:
    ans = 0                       # 最终答案
    n = len(s)
    for i, ch in enumerate(s):   # 逐个字符检查
        if ch != '*':             # 只关心 '*'
            continue
        # 向左数有多少个 '|'
        bar_cnt = 0
        j = i - 1
        while j >= 0:
            if s[j] == '|':
                bar_cnt += 1      # 发现一个 '|'
            j -= 1
        # bar_cnt 为奇数说明在 '|...|' 之间，忽略
        if bar_cnt % 2 == 0:      # 偶数 → 不在保密区
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n` 是字符串长度。想象一下，你要对每颗星星（`*`）都去“回头数一遍”左边的竖线，最坏情况下会做 `n` 次 `n` 步的工作，等价于 `n × n`。

- **空间复杂度**：`O(1)`  
  只用了几个整数计数器，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新向左遍历**，导致大量重复计数。实际上，我们只需要一次遍历，就能知道自己当前是否位于 `|...|` 区间：

1. 维护一个布尔变量 `in_bar`（是否在竖线之间）。初始为 `False`，表示我们在普通区域。  
2. 从左到右逐字符扫描：  
   - 遇到 `'|'` 时，翻转 `in_bar`（`True` ↔ `False`），因为每出现一次竖线，就要么进入保密区，要么离开保密区。  
   - 当 `in_bar == False` 且字符是 `'*'` 时，说明此星星不在任何 `|...|` 区间内，计数 `+1`。  
3. 扫描结束后，`ans` 就是答案。

这里的 `in_bar` 类似 **灯的开关**：每次碰到竖线，就把灯的状态切换；灯亮时（`in_bar=True`）我们不计数，灯灭时（`in_bar=False`）我们才计数。

#### 代码（Python）

```python
def countAsterisks(s: str) -> int:
    ans = 0            # 统计满足条件的 '*'
    in_bar = False     # 当前是否位于一对 '|' 之间

    for ch in s:       # 单次线性遍历
        if ch == '|':
            # 碰到竖线就切换状态：进入或离开保密区
            in_bar = not in_bar
        elif ch == '*' and not in_bar:
            # 只在不在保密区时计数
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，想象成走一次路，路程和字符数一样长。相比暴力的 `O(n²)`，这就像把“回头数”这件事省掉了，只需要“一路向前”。

- **空间复杂度**：`O(1)`  
  只用了 `ans` 与 `in_bar` 两个变量，常数级别的额外空间。

---

## 心得

- **核心技巧**：使用**状态机**（布尔变量）在一次遍历中记录“是否在特定区间”。  
- **适用的题型**：  
  1. “统计不在某对括号/引号之间的字符”——如 LeetCode 2110 *Number of Smooth Descent Periods of a Stock*（不完全相同但思路类似的区间标记）。  
  2. “删除/忽略被特定标记包围的子串”——如 1209 *Remove All Adjacent Duplicates in String*（需要标记是否在可删除区域）。  
  3. “配对符号的奇偶性判定”——如 331 *Verify Preorder Serialization of a Binary Tree*（利用栈/计数判断合法性）。  
- **一句话总结**：**把“在不在保密区”抽象成一个开关，遍历时随 `'|'` 翻转，它就帮你自动过滤掉不该计数的 `*`**。

---

## 反思

- **第一反应**：看到“成对的竖线”和“排除区间”，立刻想到“奇偶性”或“栈”。因为配对本质上就是“每出现一次就进入，第二次就退出”。  
- **最容易踩的坑**：  
  - 忘记 **翻转** 状态而是直接把 `in_bar` 设为 `True`（会导致后面的 `|` 永远保持在保密区）。  
  - 边界情况：字符串开头或结尾就是 `|`，仍然需要翻转状态，否则会误计数。  
- **下次第一步**：**先把“是否在目标区间”抽象成一个布尔变量**，再在一次遍历中根据特定字符（这里是 `'|'`）切换它的值，随后根据该状态决定是否计数或处理当前字符。这样既简洁又高效。