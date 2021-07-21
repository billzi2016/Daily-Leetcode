# #1405. 最长快乐字符串 / Longest Happy String

> 难度：中等 · 标签：String、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/longest-happy-string/)

---

## 题目（英文原版）

**Description**

A string s is called happy if it satisfies the following conditions:
Given three integers a, b, and c, return the longest possible happy string. If there are multiple longest happy strings, return any of them. If there is no such string, return the empty string "".
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: a = 1, b = 1, c = 7
Output: "ccaccbcc"
Explanation: "ccbccacc" would also be a correct answer.
```

**Example 2:**

```
Input: a = 7, b = 1, c = 0
Output: "aabaa"
Explanation: It is the only correct answer in this case.
```

**Constraints**

- 0 <= a, b, c <= 100
- a + b + c > 0

---

## 题目（中文翻译）

如果一个字符串 `s` 中 **不存在** 任意出现连续三个相同字符的子串（substring），则称 `s` 为**快乐字符串**（happy string）。

给定三个整数 `a`、`b`、`c`，分别表示字符 `'a'`、`'b'`、`'c'` 在结果中最多可以出现的次数，返回 **最长** 的快乐字符串。如果存在多个长度相同的最长快乐字符串，返回任意一个即可。如果不存在满足条件的字符串，返回空字符串 `""`。

**子串（substring）** 是字符串内部的一个连续字符序列。

---

## 示例

### 示例 1
**输入**  
```text
a = 1, b = 1, c = 7
```
**输出**  
```text
"ccaccbcc"
```
**解释**  
`"ccbccacc"` 也是一个正确答案。

### 示例 2
**输入**  
```text
a = 7, b = 1, c = 0
```
**输出**  
```text
"aabaa"
```
**解释**  
在此情况下这是唯一的正确答案。

---

## 约束条件

- `0 <= a, b, c <= 100`
- `a + b + c > 0`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的字符序列都枚举出来**，然后挑出满足“同一种字符连续出现不能超过 2 次”的序列，取最长的那个。  
- **数据结构**：我们可以用递归（回溯）来逐步往字符串后面添加字符。递归的参数包括当前已经拼好的字符串 `cur`，以及三个字符剩余的使用次数 `a、b、c`。  
- **生活化类比**：把递归想象成在玩拼字游戏，每次你手里有若干块字母卡（a、b、c），要把它们按规则放到一行纸上。每放一块，就把对应的卡数减一，继续放下一块，直到没有卡可以放为止。  
- **为什么正确**：回溯会遍历**所有**合法的放置顺序（只要我们在每一步都检查“连续三个相同字符”是否会被破坏），所以最后找到的最长字符串一定是答案。  

#### 代码（Python）  

```python
def longest_happy_string_bruteforce(a: int, b: int, c: int) -> str:
    # 用来记录目前找到的最长合法字符串
    best = ""

    def backtrack(cur: str, a_left: int, b_left: int, c_left: int):
        nonlocal best
        # 每进入一次递归，都尝试更新答案
        if len(cur) > len(best):
            best = cur

        # 如果已经没有字符可以继续放了，直接返回
        if a_left == 0 and b_left == 0 and c_left == 0:
            return

        # 依次尝试放 'a'、'b'、'c'
        for ch, left in (('a', a_left), ('b', b_left), ('c', c_left)):
            # 1️⃣ 剩余数量必须大于 0
            if left == 0:
                continue
            # 2️⃣ 检查加入后是否会出现 “连续三个相同字符”
            if len(cur) >= 2 and cur[-1] == cur[-2] == ch:
                continue      # 不能放，直接跳过

            # 递归进入下一层
            if ch == 'a':
                backtrack(cur + 'a', a_left - 1, b_left, c_left)
            elif ch == 'b':
                backtrack(cur + 'b', a_left, b_left - 1, c_left)
            else:  # ch == 'c'
                backtrack(cur + 'c', a_left, b_left, c_left - 1)

    backtrack("", a, b, c)
    return best
```

#### 复杂度  

- **时间复杂度**：最坏情况会遍历所有合法的排列。因为每一步最多有 3 种选择，深度最多是 `a+b+c`，所以时间复杂度是 `O(3^{a+b+c})`，这在 `a,b,c ≤ 100` 时是不可接受的（指数级爆炸）。  
- **空间复杂度**：递归栈的深度最多为 `a+b+c`，即 `O(a+b+c)`，再加上保存 `best` 的字符串也需要同样的空间。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“每一步都要尝试所有字符”**，导致指数级的搜索。  
观察题目可以发现：  
1. **只要当前字符不是已经连续出现了两次，就可以继续放**。  
2. 为了让字符串尽可能长，我们**应该优先使用剩余数量最多的字符**，因为它更容易被卡在后面导致无法继续。  

于是可以采用 **贪心 + 最大堆（优先队列）** 的思路：  

- **最大堆**：把每种字符及其剩余次数放入堆，堆顶永远是**当前剩余次数最多的字符**。堆的概念类似“字典”，字典里每个词都有对应的页码，页码最大的词最先被取出。  
- **每一步**：弹出堆顶字符 `first`。  
  - 如果把 `first` 加到结果后会导致出现“三个相同字符”，则不能直接使用。此时再弹出第二多的字符 `second`，使用 `second`（一定不会违反规则，因为它和前两个字符不同），使用完后把 `second` 的剩余次数重新放回堆。  
  - 如果 `first` 可以直接使用，就把它加入结果，使用一次后如果还有剩余就再放回堆。  
- **结束条件**：堆为空或堆里只剩下一个字符且已经连续出现两次，说明再也不能添加字符，结束。  

这样每一步只检查最多两个字符，时间大幅降低到线性。  

**关键点解释**  
- **为什么要检查“连续两个相同字符”**：因为只要前面已经有两个相同字符，若再放同样的字符就会违反“不能出现连续三个”。  
- **为什么使用堆**：堆能在 `O(log 3) ≈ O(1)` 的时间内得到当前最大剩余次数的字符，保证每一步都“贪心地”使用最充足的字符。  

#### 代码（Python）  

```python
import heapq

def longest_happy_string(a: int, b: int, c: int) -> str:
    # 构造最大堆，Python 的 heapq 是最小堆，用负数实现最大堆
    max_heap = []
    for cnt, ch in ((a, 'a'), (b, 'b'), (c, 'c')):
        if cnt > 0:
            heapq.heappush(max_heap, (-cnt, ch))   # (-cnt) 越大（负数越小）表示剩余越多

    result = []          # 用列表收集字符，最后 join 成字符串，效率更高

    while max_heap:
        cnt1, ch1 = heapq.heappop(max_heap)   # 取出剩余最多的字符
        # 判断把 ch1 加进去会不会形成 “xxx”
        if len(result) >= 2 and result[-1] == result[-2] == ch1:
            # 需要使用次多的字符
            if not max_heap:                  # 堆里已经没有别的字符，说明结束
                break
            cnt2, ch2 = heapq.heappop(max_heap)   # 取第二多的字符
            result.append(ch2)                # 必然安全，因为 ch2 != ch1
            cnt2 += 1                          # 使用一次，cnt 是负数，+1 相当于 -1
            if cnt2 < 0:                       # 仍有剩余，放回堆
                heapq.heappush(max_heap, (cnt2, ch2))
            # 把第一次弹出的字符重新放回堆，稍后还能用
            heapq.heappush(max_heap, (cnt1, ch1))
        else:
            # 可以直接使用 ch1
            result.append(ch1)
            cnt1 += 1                          # 使用一次
            if cnt1 < 0:                       # 还有剩余，继续放回堆
                heapq.heappush(max_heap, (cnt1, ch1))

    return ''.join(result)
```

#### 复杂度  

- **时间复杂度**：每次循环最多弹出两次堆，堆的大小始终不超过 3（因为只有 a、b、c 三种字符），所以每次 `push/pop` 的代价是 `O(log 3) = O(1)`。循环次数等于最终字符串的长度 `N = a+b+c`（最多 300），因此整体时间是 **O(N)**，即线性时间。  
- **空间复杂度**：堆里最多存 3 条记录，结果字符串需要 `O(N)` 的空间来保存答案，所以 **O(N)**（主要是输出本身的空间）。

---

## 心得  

- **核心技巧**：**贪心 + 最大堆**，始终优先使用剩余最多且不违反约束的字符。  
- **适用的题型**：  
  1. “构造最长/最短满足特定约束的序列”——如 *"Construct String with Substring Constraints"*。  
  2. “按出现频率组织字符”——如 *"Rearrange String k Distance Apart"*（需要把相同字符间隔 k）。  
  3. “使用优先队列控制资源消耗”——如 *"Task Scheduler"*（把任务按频率调度）。  
- **一句话总结**：**每一步都选“最多还能用、且不让规则崩溃”的字符**，就是解这类构造类贪心题的钥匙。

---

## 反思  

- **第一反应**：看到“不能出现三个相同字符”，立刻想到“限制连续次数”，于是尝试回溯枚举所有可能。  
- **最容易踩的坑**：  
  - 忘记检查 **前两个字符** 是否相同，只检查最后一个会导致错误。  
  - 当堆里只剩下一个字符且已经连续出现两次时，仍继续循环会产生无限循环或错误的输出。  
  - 计数使用负数实现最大堆时，`cnt += 1`（而不是 `cnt -= 1`）容易混淆。  
- **下次第一步**：先判断“**是否可以用贪心**”。如果约束是“局部连续次数有限”，往往可以用**最大堆/计数排序**来每一步挑最有余量的字符。这样思路更清晰，避免一开始就陷入指数级搜索。