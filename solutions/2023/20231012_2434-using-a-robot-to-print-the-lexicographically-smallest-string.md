# #2434. 使用机器人打印字典序最小的字符串 / Using a Robot to Print the Lexicographically Smallest String

> 难度：中等 · 标签：Hash Table、String、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string/)

---

## 题目（英文原版）

**Description**

You are given a string s and a robot that currently holds an empty string t. Apply one of the following operations until s and t are both empty:
Return the lexicographically smallest string that can be written on the paper.

**Examples**

**Example 1:**

```
Input: s = "zza"
Output: "azz"
Explanation: Let p denote the written string.
Initially p="", s="zza", t="".
Perform first operation three times p="", s="", t="zza".
Perform second operation three times p="azz", s="", t="".
```

**Example 2:**

```
Input: s = "bac"
Output: "abc"
Explanation: Let p denote the written string.
Perform first operation twice p="", s="c", t="ba". 
Perform second operation twice p="ab", s="c", t="". 
Perform first operation p="ab", s="", t="c". 
Perform second operation p="abc", s="", t="".
```

**Example 3:**

```
Input: s = "bdda"
Output: "addb"
Explanation: Let p denote the written string.
Initially p="", s="bdda", t="".
Perform first operation four times p="", s="", t="bdda".
Perform second operation four times p="addb", s="", t="".
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only English lowercase letters.

---

## 题目（中文翻译）

你得到一个字符串 `s`，以及一个当前持有空字符串 `t` 的机器人。不断对 `s` 和 `t` 施行以下两种操作中的任意一种，直至 `s` 与 `t` 均为空：

- 将 `s` 的首字符移动到 `t` 的末尾；
- 将 `t` 的末字符弹出并写在纸上形成字符串 `p`。

返回能够写在纸上得到的字典序（lexicographically）最小的字符串 `p`。

---

### 示例

#### 示例 1  
**输入**: `s = "zza"`  
**输出**: `"azz"`  
**解释**: 设 `p` 为写在纸上的字符串。  

初始时 `p = ""`，`s = "zza"`，`t = ""`。  
- 先执行第一种操作三次，得到 `p = ""`，`s = ""`，`t = "zza"`。  
- 再执行第二种操作三次，得到 `p = "azz"`，`s = ""`，`t = ""`。  

#### 示例 2  
**输入**: `s = "bac"`  
**输出**: `"abc"`  
**解释**: 设 `p` 为写在纸上的字符串。  

- 执行第一种操作两次，得到 `p = ""`，`s = "c"`，`t = "ba"`。  
- 执行第二种操作两次，得到 `p = "ab"`，`s = "c"`，`t = ""`。  
- 再执行第一种操作一次，得到 `p = "ab"`，`s = ""`，`t = "c"`。  
- 最后执行第二种操作一次，得到 `p = "abc"`，`s = ""`，`t = ""`。  

#### 示例 3  
**输入**: `s = "bdda"`  
**输出**: `"addb"`  
**解释**: 设 `p` 为写在纸上的字符串。  

初始时 `p = ""`，`s = "bdda"`，`t = ""`。  
- 先执行第一种操作四次，得到 `p = ""`，`s = ""`，`t = "bdda"`。  
- 再执行第二种操作四次，得到 `p = "addb"`，`s = ""`，`t = ""`。  

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s` 仅由英文小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的操作顺序枚举一遍，模拟机器人把字符写到纸上，最后取所有得到的字符串中字典序最小的那个。  

- **数据结构**：我们可以用两个列表（相当于栈）来分别保存 `s`（原始字符序列）和 `t`（机器人手里的临时字符串），再用一个字符串 `p` 记录写在纸上的字符。  
- **为什么正确**：因为题目只要求“所有合法的操作序列”里字典序最小的结果，枚举全部序列自然不会漏掉最优解。  
- **复杂度分析**：  
  - 每一次操作都有两种选择（把 `s` 的首字符压入 `t`，或把 `t` 的栈顶弹出写入 `p`），如果把 `s` 长度记为 `n`，则总的可能序列数是 **指数级** 的，大约是 `2^n`。这就像把每个字符都看成一次“是/否”决定。  
  - 因此时间复杂度是 **O(2ⁿ)**，对 `n = 10⁵` 完全不可行。  
  - 空间上我们只需要保存 `s`、`t`、`p`，所以是 **O(n)**，但这已经不是瓶颈。

> **大白话**：`O(2ⁿ)` 就好比把一棵深度为 `n`、每层有两个分支的二叉树全部遍历，树的节点数会爆炸，根本跑不完。

#### 代码（Python）

```python
from itertools import product

def robot_print_bruteforce(s: str) -> str:
    # 这里仅作演示，实际 n 只能很小（比如 <= 6）才能跑完
    n = len(s)
    best = None

    # 用二进制序列表示每一步是“压栈”(0) 还是“出栈写纸”(1)
    # 需要保证每一步合法：压栈时 s 还有字符，出栈时 t 非空
    def dfs(i, s_remain, t_stack, cur):
        nonlocal best
        # 当 s、t 都为空时得到一个完整的答案
        if not s_remain and not t_stack:
            if best is None or cur < best:
                best = cur
            return
        # 1）把 s 的首字符压入 t
        if s_remain:
            dfs(i + 1, s_remain[1:], t_stack + s_remain[0], cur)
        # 2）把 t 栈顶弹出写到纸上
        if t_stack:
            dfs(i + 1, s_remain, t_stack[:-1], cur + t_stack[-1])

    dfs(0, s, "", "")
    return best

# 示例（仅能跑很短的字符串）
print(robot_print_bruteforce("bac"))   # -> "abc"
```

> 代码里每一行都有中文注释，实际使用时只能在 `n` 很小的情况下测试。

#### 复杂度

- **时间复杂度**：`O(2ⁿ)` —— 每个字符都有两种可能的操作，导致指数级的搜索空间。  
- **空间复杂度**：`O(n)` —— 递归栈深度最多 `2n`，加上保存 `s`、`t`、`p` 的临时字符串。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**搜索所有可能**是不可取的，真正的难点在于**何时把栈顶字符写到纸上**。只要我们能在每一步做出“贪心”选择，就能避免枚举。

**关键观察**：

1. **字典序的比较**  
   当我们准备把 `t` 栈顶字符写到纸上时，如果后面还有更小的字符（在 `s` 里还未出现），那么现在写会导致最终结果变大。只有当**栈顶字符不大于**剩余字符中最小的那个时，才安全写下。

2. **如何快速得到剩余字符的最小值**  
   - 统计 `s` 中每个字母出现的次数（相当于“字典”。key 是字符，value 是还剩多少个）。  
   - 当我们把 `s[0]` 推入栈 `t` 时，记得把对应计数减 1。  
   - 随时可以遍历 `'a'..'z'` 找到第一个计数 > 0 的字母，这就是**当前剩余字符的最小字母**。因为字母表只有 26 种，遍历成本是常数级。

3. **贪心过程**  
   - 依次把 `s` 的首字符推入栈 `t`（相当于机器人“取”字符）。  
   - 每次 **循环** 检查：如果栈不为空且 `t[-1] <= min_remain`，就把栈顶弹出写到答案 `p`。  
   - 当 `s` 已经空了，`min_remain` 变成一个“哨兵”字符（如 `'{'`），此时所有剩余字符都可以直接弹出。

**为什么贪心对**：

- 设想我们在某一步把栈顶字符 `c` 写到纸上，而后面还有更小的字符 `x (< c)` 仍在 `s` 中。无论后面怎么操作，`x` 必须先被压入栈再写出，必然导致 `c` 出现在 `x` 之前，字典序必然不如把 `c` 延后写的方案。因此**只要栈顶大于剩余最小字符，就不该写**。  
- 当 `c <= min_remain` 时，**无论后面怎么排**，`c` 已经是当前能够写的最小字符，立刻写不会破坏全局最小性。  

**类比**：把这过程想象成“排队买咖啡”。`s` 是排队的顾客，`t` 是临时等候的窗口。我们只在窗口最前面的顾客的咖啡种类不比后面还有的顾客更贵时才让他付款，这样整体花费（字典序）最小。

#### 代码（Python）

```python
def robot_with_string(s: str) -> str:
    """
    贪心 + 栈 + 计数
    1. cnt[c] 记录 s 中字符 c 还剩多少个
    2. 按顺序把 s 的字符压入栈 t
    3. 每次检查栈顶是否 <= 剩余字符的最小字母，若是则弹出写入答案
    """
    # 1. 统计每个字符出现次数
    cnt = [0] * 26                     # cnt[0] 对应 'a', cnt[25] 对应 'z'
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    stack = []                         # 机器人手里的临时字符串 t
    ans = []                           # 最终写在纸上的字符列表

    # 辅助函数：返回当前剩余字符的最小字母（如果没有则返回 '{'，ASCII 在 'z' 之后）
    def current_min():
        for i in range(26):
            if cnt[i] > 0:
                return chr(ord('a') + i)
        return '{'                     # 哨兵，大于所有小写字母

    # 2. 依次处理 s
    for ch in s:
        # 把 ch 推入栈
        stack.append(ch)
        # 该字符已经被取走，计数减 1
        cnt[ord(ch) - ord('a')] -= 1

        # 3. 只要栈顶字符 <= 剩余最小字符，就弹出写入答案
        while stack and stack[-1] <= current_min():
            ans.append(stack.pop())

    # s 处理完后，stack 里可能还有字符（此时 current_min() == '{'），全部弹出
    while stack:
        ans.append(stack.pop())

    return ''.join(ans)


# ------------------- 示例 -------------------
print(robot_with_string("zza"))   # "azz"
print(robot_with_string("bac"))   # "abc"
print(robot_with_string("bdda"))  # "addb"
```

> **关键行中文注释**  
> - `cnt = [0] * 26`：把字母表当成 26 格的“字典”，每格存剩余个数。  
> - `while stack and stack[-1] <= current_min():`：只要栈顶不大于后面最小的字母，就可以放心写下。  
> - `return '{'`：`'{'` 的 ASCII 码比 `'z'` 大，充当“无穷大”，确保剩余为空时栈里的字符都会弹出。

#### 复杂度

- **时间复杂度**：`O(n * 26)` → 实际是 `O(n)`  
  - 每个字符只会被压栈一次、弹栈一次。  
  - `current_min()` 最多遍历 26 次（字母表常数），所以整体线性。  
  - 与暴力解的指数级相比，`O(n)` 意味着即使 `n = 10⁵` 也能在毫秒级完成。  

- **空间复杂度**：`O(n)`  
  - 最坏情况下所有字符都先压入栈，栈的大小等于 `n`。  
  - 计数数组只有 26 个整数，算作常数空间。

---

## 心得

- **核心技巧**：**贪心 + 最小剩余字符**（即“只在栈顶不大于剩余最小字符时写出”。）  
- **适用的题型**  
  1. **单调栈 + 前缀最小/最大**：如 “最小字典序的子序列”“删除字符使字符串字典序最小”。  
  2. **字符压入/弹出模拟**：比如 “栈排序”“使用队列/栈模拟特定输出序列”。  
  3. **Greedy + 计数**：如 “最小字典序的排列”“按字母频率构造字符串”。  
- **一句话总结**：**只在“当前可写的字符已是全局最小”时才写，剩下的交给后面处理**。

---

## 反思

- **第一反应**：把所有操作顺序枚举，写出暴力递归/回溯。  
- **最容易踩的坑**  
  1. **忘记更新计数**：在把字符压入栈后必须把对应的剩余计数减 1，否则 `current_min()` 会误判。  
  2. **边界条件**：当 `s` 已经遍历完，`current_min()` 必须返回一个大于 `'z'` 的哨兵，否则循环会卡在 `while`。  
  3. **字符比较**：直接比较字符 `'a' <= ch <= 'z'` 在 Python 中是合法的，但要确保不是把字符的 ASCII 码当成整数比较。  
- **下次类似题的第一步**：先**统计剩余信息**（如字符频次、最小值），再决定**何时输出**，把“是否输出”转化为一个**可局部判断的贪心条件**。这样往往能把指数级搜索压缩到线性时间。