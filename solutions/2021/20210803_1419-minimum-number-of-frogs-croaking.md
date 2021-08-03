# #1419. 最少青蛙呱叫数量 / Minimum Number of Frogs Croaking

> 难度：中等 · 标签：String、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-frogs-croaking/)

---

## 题目（英文原版）

**Description**

You are given the string croakOfFrogs, which represents a combination of the string "croak" from different frogs, that is, multiple frogs can croak at the same time, so multiple "croak" are mixed.
Return the minimum number of different frogs to finish all the croaks in the given string.
A valid "croak" means a frog is printing five letters 'c', 'r', 'o', 'a', and 'k' sequentially. The frogs have to print all five letters to finish a croak. If the given string is not a combination of a valid "croak" return -1.

**Examples**

**Example 1:**

```
Input: croakOfFrogs = "croakcroak"
Output: 1 
Explanation: One frog yelling "croak" twice.
```

**Example 2:**

```
Input: croakOfFrogs = "crcoakroak"
Output: 2 
Explanation: The minimum number of frogs is two. 
The first frog could yell "crcoakroak".
The second frog could yell later "crcoakroak".
```

**Example 3:**

```
Input: croakOfFrogs = "croakcrook"
Output: -1
Explanation: The given string is an invalid combination of "croak" from different frogs.
```

**Constraints**

- 1 <= croakOfFrogs.length <= 105
- croakOfFrogs is either 'c', 'r', 'o', 'a', or 'k'.

---

## 题目（中文翻译）

给定字符串 `croakOfFrogs`，它表示若干只青蛙（frog）交叉发出的 `"croak"` 声音的组合，即多个青蛙可以同时呱叫，因而多个 `"croak"` 可能交错出现。  
返回能够完成字符串中所有呱叫所需的 **最小不同青蛙数量**。  

一个有效的 `"croak"` 必须按顺序依次输出字符 `'c'`、`'r'`、`'o'`、`'a'`、`'k'`，青蛙必须完整输出这五个字母才能算作一次完整的呱叫。  
如果给定的字符串不能拆分为若干个有效的 `"croak"`，返回 `-1`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= croakOfFrogs.length <= 10^5`  
- `croakOfFrogs` 只包含字符 `'c'`、`'r'`、`'o'`、`'a'` 或 `'k'`  

### 示例

#### 示例 1
**输入**  
``` 
croakOfFrogs = "croakcroak"
```  
**输出**  
```
1
```  
**解释**  
一只青蛙连续呱叫两次 `"croak"`。

#### 示例 2
**输入**  
``` 
croakOfFrogs = "crcoakroak"
```  
**输出**  
```
2
```  
**解释**  
最少需要两只青蛙。  
第一只青蛙可以发出 `"crcoakroak"`。  
第二只青蛙随后可以发出 `"crcoakroak"`。

#### 示例 3
**输入**  
``` 
croakOfFrogs = "croakcrook"
```  
**输出**  
```
-1
```  
**解释**  
给定的字符串不是若干只青蛙合法 `"croak"` 的组合。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每只青蛙想象成一条**流水线**，它们分别在按照 `"c → r → o → a → k"` 的顺序发声。  
遍历字符串 `croakOfFrogs`，对每个字符：

1. 从已经在“发声”中的青蛙里找一只**正好需要这个字符**的青蛙，让它继续往后走一步。  
2. 如果没有青蛙正好需要这个字符，则新开辟一只青蛙，让它从 `c` 开始。  
3. 当青蛙完成 `'k'` 时，说明它已经完整喊完一次 `"croak"`，可以把它从“进行中”的列表中移除（相当于这只青蛙可以休息，后面若再需要可以重新使用）。

这相当于**逐个匹配**，每次都要遍历当前所有正在喊的青蛙，找到合适的那只。  
如果遍历结束后还有青蛙停在中间状态（没有完整喊完），或者在匹配过程中出现不可能的字符（比如出现 `'r'` 但没有青蛙已经喊过 `'c'`），则说明输入非法，返回 `-1`。  

> **类比**：想象你在图书馆排队借书，书的借阅顺序是 `c → r → o → a → k`。每个人手里只能拿一本书，必须按照顺序拿完。如果来的人手里拿的书不符合顺序，就得新开一个借书窗口。暴力解就是每来一个人，就去所有窗口里找能接收这本书的窗口，找到就让他继续，找不到就开新窗口。

#### 代码（Python）  

```python
def minNumberOfFrogs_bruteforce(croakOfFrogs: str) -> int:
    # 每只青蛙当前停留的字符位置，用列表保存
    # 0 代表还没有开始，1~5 代表已经读到的字符下标（c=1, r=2, o=3, a=4, k=5）
    frogs = []                     # 正在发声的青蛙状态
    max_frogs = 0                  # 同时出现的最大青蛙数
    order = "croak"                # 正确顺序

    for ch in croakOfFrogs:
        # 尝试在已有青蛙中找到可以接收当前字符的青蛙
        placed = False
        for i in range(len(frogs)):
            # 若该青蛙已经在等下一个字符，且下一个字符正好是 ch
            if frogs[i] < 5 and order[frogs[i]] == ch:
                frogs[i] += 1      # 青蛙前进一步
                placed = True
                # 如果已经完成一次 croak，移除该青蛙（它可以休息）
                if frogs[i] == 5:
                    frogs.pop(i)
                break

        # 没有找到合适的青蛙，需要新开一只
        if not placed:
            if ch != 'c':          # 第一个字符必须是 c，否则非法
                return -1
            frogs.append(1)        # 这只青蛙已经读到了 'c'（位置 1）
            max_frogs = max(max_frogs, len(frogs))

    # 循环结束后，若还有未完成的青蛙，说明字符串不合法
    if frogs:                      # 仍有未完成的 croak
        return -1
    return max_frogs
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`，其中 `n` 是字符串长度，`m` 是同时出现的青蛙数（最坏情况 `m≈n`），所以最坏情况是 `O(n²)`。可以把 `O(n²)` 想象成“每读一个字符，都要去检查所有已经在喊的青蛙”。  
- **空间复杂度**：`O(m)`，最多同时存放 `m` 只青蛙的状态，最坏 `O(n)`。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有正在喊的青蛙**，这导致二次循环。  
观察可以发现：

1. 所有青蛙的状态只会出现在 `"c r o a k"` 五个阶段之一。  
2. 当我们看到字符 `'c'` 时，必然是 **新开一只青蛙**（或者有已经完成的青蛙再次开始），因为 `'c'` 是序列的第一个字符。  
3. 当看到字符 `'r'`、`'o'`、`'a'`、`'k'` 时，只需要检查**前一个字符的计数是否大于当前字符的计数**，即是否有青蛙已经走到前一步并在等待这个字符。  

因此我们可以用 **5 个计数器**（或哈希表）来记录每个字母当前出现的次数：

- `cnt['c']`：已经出现但还未匹配到 `'r'` 的 `'c'` 数量  
- `cnt['r']`：已经匹配到 `'r'`，但还未匹配到 `'o'` 的数量  
- … 依此类推

遍历字符串时：

- 对每个字符 `ch`，把对应计数 `cnt[ch]` 加 1。  
- 检查合法性：如果 `ch` 不是 `'c'`，则必须满足 `cnt[ch] ≤ cnt[prev]`（`prev` 为前一个字符），否则说明出现了“缺少前置字符”，返回 `-1`。  
- 当字符是 `'k'` 时，表示一只青蛙完整喊完一次，此时我们可以把这条完整的路径从计数中移除，即把 `cnt['c']`、`cnt['r']`、`cnt['o']`、`cnt['a']`、`cnt['k']` 都各减 1（因为它们已经配对完成）。这一步相当于把一只正在使用的青蛙释放回“空闲池”。  

在遍历的过程中，**当前正在发声的青蛙数**等于所有未完成的字符之和 `cnt['c']+cnt['r']+cnt['o']+cnt['a']`（不包括已经完成的 `'k'`，因为 `'k'` 已经把青蛙归还）。我们只要记录遍历过程中出现的最大值，即为所需的最小青蛙数。  

> **类比**：把每只青蛙看成一条流水线的“卡车”，卡车在每个站点（c → r → o → a → k）都有一个计数器记录有多少卡车在该站等候。新来的卡车只能在站点 `c` 进入，后面的站点只能在前一个站点已经有卡车的情况下进入。`k` 站点的卡车离开后，卡车数量回到空闲池，可供后续使用。  

#### 代码（Python）  

```python
def minNumberOfFrogs(croakOfFrogs: str) -> int:
    # 统计每个字符出现的次数
    cnt = {ch: 0 for ch in "croak"}
    order = "croak"
    max_frogs = 0          # 同时出现的最大青蛙数

    for ch in croakOfFrogs:
        if ch not in cnt:          # 非法字符（题目保证不会出现，但防御式写法）
            return -1
        cnt[ch] += 1               # 当前字符出现一次

        # 检查合法性：除 'c' 外，当前字符的数量不能超过前一个字符的数量
        if ch != 'c':
            prev = order[order.index(ch) - 1]
            if cnt[ch] > cnt[prev]:
                return -1

        # 当完成一次完整的 "croak"（看到 'k'）时，所有计数都减 1
        if ch == 'k':
            # 完成一次 croak，四个前置字符各减 1
            for c in "croa":
                cnt[c] -= 1
            cnt['k'] -= 1          # k 本身也要减，表示这只青蛙已归还

        # 当前正在发声的青蛙数 = 未完成的字符总数
        # （cnt['k'] 已经是已经完成的，不计入）
        current = cnt['c'] + cnt['r'] + cnt['o'] + cnt['a']
        max_frogs = max(max_frogs, current)

    # 循环结束后，若还有未完成的字符，则非法
    if any(cnt[ch] != 0 for ch in "croa"):
        return -1
    return max_frogs
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串，每个字符的处理都是 `O(1)` 的常数操作。相较于暴力的 `O(n²)`，大幅提升。可以把它想成“每读一个字符，只需要检查它自己和前一个字符的计数”。  
- **空间复杂度**：`O(1)`，只用到固定的 5 个计数器（哈希表），与输入规模无关。  

---

## 心得  

- **核心技巧**：使用 **计数器 + 前后字符约束** 来模拟多个并行的有序序列，常见于“多线程/多任务交叉出现的序列验证”。  
- **适用的题型**  
  1. **Valid Parentheses with Multiple Types**（如 `()[]{}` 的交叉验证）  
  2. **Number of Active Projects**（项目启动/结束日志，需要实时统计并发数）  
  3. **Check if a String Is a Valid Sequence of Operations**（例如 `"ABAB"` 之类的状态机验证）  
- **一句话总结**：**把每只青蛙的进度抽象成五个计数器，最大并发计数即答案**。  

---

## 反思  

- **第一反应**：把每只青蛙当成对象，逐个匹配，写成模拟的循环（即暴力思路）。  
- **最容易踩的坑**  
  - 忽略了字符出现的顺序约束，只统计总频率会导致错误（如 `"rcoak"`）。  
  - 在遇到 `'k'` 时没有及时把青蛙归还，导致并发数被高估。  
  - 结束后没有检查是否还有未完成的 `"croa"`，会把非法输入误判为合法。  
- **下次遇到同类题**：第一步先 **判断是否可以用“每个阶段的计数”来描述**，如果可以，就直接用 **计数器 + 前后约束** 的思路求解，避免逐个对象的模拟。