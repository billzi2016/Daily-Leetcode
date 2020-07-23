# #936. 盖章序列 / Stamping The Sequence

> 难度：困难 · 标签：String、Stack、Greedy、Queue · [LeetCode 链接](https://leetcode.com/problems/stamping-the-sequence/)

---

## 题目（英文原版）

**Description**

You are given two strings stamp and target. Initially, there is a string s of length target.length with all s[i] == '?'.
In one turn, you can place stamp over s and replace every letter in the s with the corresponding letter from stamp.
We want to convert s to target using at most 10 * target.length turns.
Return an array of the index of the left-most letter being stamped at each turn. If we cannot obtain target from s within 10 * target.length turns, return an empty array.

**Examples**

**Example 1:**

```
Input: stamp = "abc", target = "ababc"
Output: [0,2]
Explanation: Initially s = "?????".
- Place stamp at index 0 to get "abc??".
- Place stamp at index 2 to get "ababc".
[1,0,2] would also be accepted as an answer, as well as some other answers.
```

**Example 2:**

```
Input: stamp = "abca", target = "aabcaca"
Output: [3,0,1]
Explanation: Initially s = "???????".
- Place stamp at index 3 to get "???abca".
- Place stamp at index 0 to get "abcabca".
- Place stamp at index 1 to get "aabcaca".
```

**Constraints**

- 1 <= stamp.length <= target.length <= 1000
- stamp and target consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 **stamp**（印章字符串）和 **target**（目标字符串）。最初，有一个长度为 `target.length` 的字符串 `s`，其中每个字符均为 `'?'`。

在一次操作中，你可以将 **stamp** 覆盖在 `s` 上，并将 `s` 中对应位置的字符全部替换为 **stamp** 中的字符。

我们希望在至多 `10 * target.length` 次操作内，将 `s` 转换为 **target**。返回一个整数数组，数组中的每个元素表示一次操作中 **stamp** 左端字符在 `s` 中的下标（即本次盖章的起始位置）。如果无法在限定次数内得到 **target**，返回空数组。

---

### 示例

**示例 1**  
输入: `stamp = "abc", target = "ababc"`  
输出: `[0,2]`  
解释: 初始时 `s = "?????"`。  
- 在下标 `0` 处盖章，得到 `"abc??"`。  
- 在下标 `2` 处盖章，得到 `"ababc"`。  

`[1,0,2]` 也被视为合法答案，此外还有其他可行的答案。

**示例 2**  
输入: `stamp = "abca", target = "aabcaca"`  
输出: `[3,0,1]`  
解释: 初始时 `s = "???????"`。  
- 在下标 `3` 处盖章，得到 `"???abca"`。  
- 在下标 `0` 处盖章，得到 `"abcabca"`。  
- 在下标 `1` 处盖章，得到 `"aabcaca"`。

---

### 约束条件

- `1 <= stamp.length <= target.length <= 1000`
- `stamp` 和 `target` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们可以把题目想成「把一张满是问号的纸（`s`）逐步贴上印章（`stamp`）」，每次贴印章时只能把对应位置的字符改成印章上的字母。  

最直接的想法是：**从左到右一次遍历 target，凡是能把 stamp 完全匹配（即对应位置的字符要么已经是目标字母，要么是 `?`）的窗口就直接贴一次**。  
- 数据结构：只需要一个可变的字符数组 `s`（把 `?` 当作占位符），以及一个 `list` 用来记录每一次贴印章的左端索引。  
- 正确性：只要我们每一次都把能够贴的窗口都贴上，最终 `s` 中的每个字符都会被对应的目标字符覆盖。因为题目保证最多 `10 * len(target)` 次操作足够，而我们的暴力过程只会在每次真的可以贴的时候才进行一次操作，不会出现非法覆盖。  

**为什么会停下来？**  
- 每贴一次，`s` 中至少会有一个 `?` 被替换成真实字符。  
- `s` 长度至多 `1000`，所以最多 `len(target)` 次贴印章就能把所有 `?` 消掉，远小于题目给的上限。  

#### 代码（Python）  

```python
def movesToStamp(stamp: str, target: str):
    m, n = len(stamp), len(target)
    s = list('?' * n)                 # 当前的字符串，用列表方便原地修改
    res = []                           # 记录每一次贴 stamp 的左端下标
    changed = True

    # 只要在一次遍历中还有可以贴的地方，就一直循环
    while changed:
        changed = False
        # 检查所有可能的窗口
        for i in range(n - m + 1):
            # 如果这个窗口已经全是 stamp 的字符，就不必再贴了
            if all(s[i + j] == stamp[j] or s[i + j] == '?' for j in range(m)):
                # 只在至少有一个 '?' 时才算一次真实的贴印章
                if any(s[i + j] == '?' for j in range(m)):
                    # 把窗口全部改成 stamp 的字符
                    for j in range(m):
                        s[i + j] = stamp[j]
                    res.append(i)               # 记录左端下标
                    changed = True
        # 若一次循环没有任何变化，说明再也找不到可以贴的窗口了
    # 最终检查是否全部匹配 target
    if ''.join(s) != target:
        return []                         # 无法完成
    # 题目要求返回的顺序是“从后往前贴”，所以要逆序
    return res[::-1]
```

**关键行中文注释**  
- `s = list('?' * n)`：把全部 `?` 放进可变数组，方便后面直接改字符。  
- `all(s[i + j] == stamp[j] or s[i + j] == '?' for j in range(m))`：检查窗口是否可以贴（已有字符要么相同，要么仍是 `?`）。  
- `any(s[i + j] == '?' for j in range(m))`：确保这次真的“进步”，否则会无限循环。  
- `res.append(i)`：记录本次贴 stamp 的左端位置。  

#### 复杂度  

- **时间复杂度：** `O(n * m)`（最坏情况下，每次循环遍历所有 `n-m+1` 窗口，每个窗口检查 `m` 个字符）。  
  - 用大白话说：如果 `target` 长 1000，`stamp` 长 500，最多要检查 `500 * 500 = 250,000` 次字符，比起 10 万次的上限仍然可以接受。  
- **空间复杂度：** `O(n)` 用来存放当前的字符数组 `s`，以及答案列表 `res`（最多 `n` 条记录）。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要遍历所有窗口**，即使很多窗口已经不可能再贴了。  
我们可以把过程 **倒着想**：  

> **从 `target` 开始，逐步把可以被 `stamp` 完全覆盖的子串全部变成 `?`，直到全变成 `?` 为止。**  

倒着做的好处是：  
1. 每次只关注 **一个窗口** 是否可以全部变成 `?`，而不必每轮遍历所有窗口。  
2. 当一个窗口被成功“消除”后，它会帮助相邻的窗口变得更容易消除（因为 `?` 可以当作通配符），这正好形成 **广度优先搜索** 的层层推进。  

具体步骤如下（核心数据结构：**队列 + 已访问集合**）  

1. **预处理每个窗口**（长度为 `m`）  
   - 记录该窗口中已经和 `stamp` 匹配的字符数量 `match`。  
   - 记录该窗口中不匹配的字符位置集合 `todo`（这些位置必须被其他窗口先变成 `?` 才能贴）。  
2. **初始化**  
   - 把所有 `todo` 为空的窗口（即一开始就可以直接贴的窗口）放入队列 `q`，并标记为已访问。  
   - 同时把这些窗口对应的所有字符位置标记为已“消除”（即 `?`），加入另一个集合 `filled`。  
3. **BFS 过程**  
   - 从队列中弹出一个窗口 `i`，把 `i` 加入答案列表 `ans`（因为倒着思考，这实际上是 **最后一次** 贴 `stamp` 的位置）。  
   - 对 `i` 所覆盖的每个字符位置 `pos`，如果 `pos` 之前还不是 `?`，把它设为 `?` 并遍历所有包含 `pos` 的窗口 `j`（这一步可以通过一个 **位置 → 窗口列表** 的映射提前构造）。  
   - 对每个受影响的窗口 `j`，把 `pos` 从 `todo[j]` 中移除，`match[j]` 加一。若此时 `todo[j]` 为空且 `j` 未被访问，则把 `j` 加入队列。  
4. **结束**  
   - 当所有字符都被标记为 `?`（`len(filled) == n`）时，说明我们成功倒推出一组合法的贴印章顺序。  
   - 由于我们是倒着记录的，需要把答案列表 `ans` 逆序返回。  

**关键概念解释**  
- **队列（Queue）**：像排队买票一样，先发现可以直接贴的窗口就先处理，后面受影响的窗口再依次进入队列。  
- **单调栈 / 贪心**：这里不需要栈，只用贪心的“只要窗口已经可以全部变成 `?` 就立即处理”。  
- **位置 → 窗口映射**：把每个字符位置关联到所有可能覆盖它的窗口，类似于“字典里查词”，可以在 O(1) 时间找到受影响的窗口。  

#### 代码（Python）  

```python
from collections import deque, defaultdict
from typing import List

def movesToStamp(stamp: str, target: str) -> List[int]:
    m, n = len(stamp), len(target)
    # 每个窗口的 match 数量和待消除的字符集合
    match = [0] * (n - m + 1)          # 已经匹配的字符数
    todo = [set() for _ in range(n - m + 1)]   # 需要先变成 '?' 的下标集合

    # 位置 -> 包含该位置的窗口列表
    pos_to_windows = defaultdict(list)

    # 预处理所有窗口
    for i in range(n - m + 1):
        for j in range(m):
            if stamp[j] == target[i + j]:
                match[i] += 1           # 已匹配
            else:
                todo[i].add(i + j)      # 这个位置必须先变成 '?'
        # 把窗口 i 的每个位置登记到映射表中
        for p in range(i, i + m):
            pos_to_windows[p].append(i)

    q = deque()                        # 队列保存“已经可以直接贴”的窗口下标
    visited = [False] * (n - m + 1)    # 防止同一个窗口入队多次
    ans = []                           # 逆向记录的答案

    # 初始化：所有 todo 为空的窗口直接入队
    for i in range(n - m + 1):
        if not todo[i]:
            q.append(i)
            visited[i] = True

    # 已经被变成 '?' 的字符集合
    filled = set()

    while q:
        i = q.popleft()
        ans.append(i)                  # 逆序记录：i 实际上是最后一次贴 stamp 的位置
        # 把窗口 i 覆盖的每个位置都标记为 '?'
        for p in range(i, i + m):
            if p in filled:
                continue               # 已经是 '?'，不必重复处理
            filled.add(p)
            # 所有受 p 影响的窗口
            for w in pos_to_windows[p]:
                if p in todo[w]:
                    todo[w].remove(p)  # 这个位置不再是阻碍
                    # 如果窗口 w 已经没有阻碍且未入队，则加入队列
                    if not todo[w] and not visited[w]:
                        q.append(w)
                        visited[w] = True

    # 检查是否所有字符都被消除
    if len(filled) != n:
        return []                      # 无法完成

    # 题目要求返回正向的贴印章顺序，需要逆序
    return ans[::-1]
```

**关键行中文注释**  
- `todo[i].add(i + j)`：把不匹配的位置记录下来，后面必须先把这些位置变成 `?` 才能贴。  
- `pos_to_windows[p].append(i)`：建立“字符位置 ↔ 能覆盖它的窗口”映射，方便后续快速定位受影响的窗口。  
- `if not todo[i]: q.append(i)`：一开始就把已经可以直接贴的窗口加入队列，相当于 BFS 的起点。  
- `filled.add(p)`：把位置 `p` 标记为已经被“消除”（变成 `?`），相当于在正向思考里已经完成了这一次 stamp。  
- `if not todo[w] and not visited[w]: q.append(w)`：当某个窗口的所有阻碍都被消除后，就可以在倒序步骤里把它当作一次合法的 stamp。  

#### 复杂度  

- **时间复杂度：** `O(n * m)`  
  - 预处理遍历每个窗口一次，需要 ` (n-m+1) * m ≈ n*m` 次比较。  
  - BFS 过程中每个字符位置最多被处理一次，每次处理会遍历所有包含该位置的窗口，总共仍然是 `O(n*m)`。  
  - 用大白话说：如果 `target` 长 1000、`stamp` 长 500，最多约 `500,000` 次基本操作，完全在 1 秒以内。  

- **空间复杂度：** `O(n * m)`（主要是 `todo` 中的集合和 `pos_to_windows` 的映射）  
  - `todo` 最坏情况每个窗口都保存 `m` 个位置，`pos_to_windows` 每个位置最多关联 `m` 个窗口，整体仍然是 `n*m` 级别。  
  - 再加上 `O(n)` 的队列、visited、filled 等额外空间，整体仍然是可接受的。  

---

## 心得  

- **核心技巧**：**逆向贪心 + BFS**（把“从全 `?` 到 target”倒着思考，逐步把可以直接消除的窗口加入队列）。  
- **适用的题型**  
  1. “把字符串逐步恢复/消除” 类题目，如 *"Reveal Cards In Increasing Order"*（逆向思考）  
  2. “区间覆盖” 类问题，如 *"Maximum Area of a Piece of Cake After Horizontal and Vertical Cuts"*（使用区间映射）  
  3. “使用局部操作全局转换” 类，如 *"Minimum Number of Flips to Make the Binary String Alternating"*（贪心+区间）  

- **一句话总结解题钥匙**：**把正向的“逐步构造”倒过来做，先把已经可以完成的局部块消除，再利用这些消除产生的 `?` 继续消除邻近块。**  

---

## 反思  

- **第一反应**：直接模拟正向的 stamp 过程，想一次遍历找所有能贴的位置。  
- **最容易踩的坑**  
  - 正向模拟容易陷入 **无限循环**：因为即使窗口可以贴，但如果全部字符已经是目标字母，继续贴没有意义，需要检测是否真的有 `?` 被改动。  
  - **边界条件**：`stamp` 与 `target` 长度相等时，只能在唯一位置尝试一次。  
  - **倒序实现的细节**：忘记把答案逆序返回，导致输出的顺序与题目要求不符。  
- **下次遇到同类题**，第一步应该问自己：“这道题能否从**终点倒推到起点**？”如果答案是肯定的，就先尝试构建逆向的“消除”模型，再用 BFS/贪心把所有可行的局部操作逐步加入答案。