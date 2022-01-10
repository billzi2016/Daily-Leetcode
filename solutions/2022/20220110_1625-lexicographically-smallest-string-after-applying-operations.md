# #1625. 应用操作后字典序最小的字符串 / Lexicographically Smallest String After Applying Operations

> 难度：中等 · 标签：String、Depth-First Search、Breadth-First Search、Enumeration · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-string-after-applying-operations/)

---

## 题目（英文原版）

**Description**

You are given a string s of even length consisting of digits from 0 to 9, and two integers a and b.
You can apply either of the following two operations any number of times and in any order on s:
Return the lexicographically smallest string you can obtain by applying the above operations any number of times on s.
A string a is lexicographically smaller than a string b (of the same length) if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b. For example, "0158" is lexicographically smaller than "0190" because the first position they differ is at the third letter, and '5' comes before '9'.

**Examples**

**Example 1:**

```
Input: s = "5525", a = 9, b = 2
Output: "2050"
Explanation: We can apply the following operations:
Start:  "5525"
Rotate: "2555"
Add:    "2454"
Add:    "2353"
Rotate: "5323"
Add:    "5222"
Add:    "5121"
Rotate: "2151"
Add:    "2050"​​​​​
There is no way to obtain a string that is lexicographically smaller than "2050".
```

**Example 2:**

```
Input: s = "74", a = 5, b = 1
Output: "24"
Explanation: We can apply the following operations:
Start:  "74"
Rotate: "47"
​​​​​​​Add:    "42"
​​​​​​​Rotate: "24"​​​​​​​​​​​​
There is no way to obtain a string that is lexicographically smaller than "24".
```

**Example 3:**

```
Input: s = "0011", a = 4, b = 2
Output: "0011"
Explanation: There are no sequence of operations that will give us a lexicographically smaller string than "0011".
```

**Constraints**

- 2 <= s.length <= 100
- s.length is even.
- s consists of digits from 0 to 9 only.
- 1 <= a <= 9
- 1 <= b <= s.length - 1

---

## 题目（中文翻译）

给定一个长度为偶数、只包含字符 `'0'` 到 `'9'` 的字符串 `s`，以及两个整数 `a` 和 `b`。  
你可以对 `s` 任意次、任意顺序地执行以下两种操作中的任意一种：

1. **加法操作**：将下标为奇数的位置（0‑索引）的每个数字加上 `a`，若结果大于 `9` 则取模 `10`。即 `digit = (digit + a) % 10`。
2. **旋转操作**：将字符串整体向右旋转 `b` 位，即把后 `b` 个字符移动到字符串前面。

返回在对 `s` 执行上述操作任意次数后能够得到的 **字典序最小字符串（lexicographically smallest string）**。  

**字典序**的定义：若两个等长字符串在首次出现不同的字符位置上，前者的字符在字母表（这里指 `'0'`‑`'9'` 的顺序）中出现得更早，则前者的字典序更小。  
例如 `"0158"` 的字典序小于 `"0190"`，因为它们在第三个字符处不同，`'5'` 在 `'9'` 之前。

---

### 示例

**示例 1**  
```text
Input: s = "5525", a = 9, b = 2
Output: "2050"
Explanation:
我们可以按以下顺序执行操作：
```
- Start:  `"5525"`
- Rotate: `"2555"`
- Add:    `"2454"`
- Add:    `"2353"`
- Rotate: `"5323"`
- Add:    `"5222"`
- Add:    `"5121"`
- Rotate: `"2151"`
- Add:    `"2050"`

没有办法得到字典序更小的字符串。

---

**示例 2**  
```text
Input: s = "74", a = 5, b = 1
Output: "24"
Explanation:
执行过程如下：
```
- Start:  `"74"`
- Rotate: `"47"`
- Add:    `"42"`
- Rotate: `"24"`

已经是字典序最小的可能结果。

---

**示例 3**  
```text
Input: s = "0011", a = 4, b = 2
Output: "0011"
Explanation:
不存在任何操作序列能够得到字典序更小的字符串。
```

---

### 约束条件

- `2 <= s.length <= 100`
- `s.length` 为偶数
- `s` 仅由 `'0'` 到 `'9'` 组成
- `1 <= a <= 9`
- `1 <= b <= s.length - 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们把字符串 `s` 看成一个**状态**，每一次操作（加 `a` 或右移 `b`）都会把它变成另一个状态。  
最直接的想法就是**把所有可能出现的状态都枚举出来**，最后挑出字典序最小的那个。  

- **加 `a`**：只会影响下标为奇数的位置（从 0 开始计数），比如 `"5525"` → 在奇数位加 `9` → `"5(5+9)2(5+9)"`，每个数字超过 `9` 要取模 `10`，相当于 **在 0~9 的十个数字里循环**。可以把它想象成“把字典里的第 5 条目往后数 9 步，若超过第 10 条就回到第 1 条”。  
- **右移 `b`**：把整个字符串整体往右搬 `b` 位，超出的部分从左边补回来。就像把一排书往右搬，搬不下的书会从左边重新排进来。  

如果我们把每个状态都记下来（比如放进一个 `set`），并且 **不重复处理已经见过的状态**，那么最终我们会遍历到 **所有** 能到达的字符串。遍历结束后，只要在这些字符串里找最小的即可。

> 为什么这样一定能得到答案？  
> 因为题目允许任意次数、任意顺序地使用两种操作，而我们的遍历正好模拟了所有可能的操作序列，只要不遗漏任何状态，就不会错过字典序最小的那个。

> 复杂度怎么说？  
> - 长度为 `n`（`n ≤ 100`）的字符串，右移 `b` 的效果只会产生 `n / gcd(n, b)` 种不同的排列。  
> - 对每一种排列，奇数位的加法最多只会产生 10 种不同的数字（因为 `mod 10` 循环）。  
> - 因此状态总数 ≤ `10 * 10 * n`（题目提示），最多几千个，完全可以在几毫秒内遍历完。  

#### 代码（Python）

```python
from collections import deque

def lexicographically_smallest_string(s: str, a: int, b: int) -> str:
    n = len(s)
    # 用集合记录已经访问过的字符串，防止无限循环
    visited = set()
    # BFS 用队列，先把起始字符串放进去
    q = deque([s])
    visited.add(s)

    best = s                         # 当前找到的最小答案

    while q:
        cur = q.popleft()
        # 更新最小答案
        if cur < best:
            best = cur

        # ---------- 操作 1：在奇数下标加 a ----------
        # 这里用列表更容易修改单个字符
        lst = list(cur)
        for i in range(1, n, 2):          # 只遍历奇数下标
            # (原数字 + a) % 10 → 加完后再转成字符
            lst[i] = str((int(lst[i]) + a) % 10)
        added = ''.join(lst)
        if added not in visited:
            visited.add(added)
            q.append(added)

        # ---------- 操作 2：右移 b 位 ----------
        rotated = cur[-b:] + cur[:-b]     # 把后 b 位搬到前面
        if rotated not in visited:
            visited.add(rotated)
            q.append(rotated)

    return best
```

> 关键行注释  
> - `visited` 像 **查字典** 一样快速判断一个字符串是否已经出现过。  
> - `cur[-b:] + cur[:-b]` 把后 `b` 位搬到前面，等价于右移。  
> - BFS（广度优先搜索）保证我们一次一次地遍历所有可能的状态，而不需要递归深度太大。

#### 复杂度  

- **时间复杂度**：`O(10 * 10 * n)` → 实际上就是 **状态数 × 每个状态的常数操作**。  
  - `n` 为字符串长度，最多 100；`10*10*n` 约等于 `1e5`，在计算机里几乎是瞬间完成。  
- **空间复杂度**：`O(10 * 10 * n)` → 需要把所有已经访问的状态存进集合，最坏也只会保存几千个长度为 `n` 的字符串。

---

### 2. 最优解  

#### 思路  

上面的“暴力”其实已经是 **最优** 的做法，因为题目本身的搜索空间非常小。  
我们可以把“暴力”细化为 **状态空间搜索**（BFS/DFS），并结合下面两点进行**剪枝**，使实现更简洁：

1. **加法的循环性**  
   对同一个位置的数字，连续加 `a` 最多只会产生 10 种不同的结果（因为是 `mod 10`），再继续加会回到已经出现的数字。因此我们不必对同一个状态无限次加 `a`，只要把已经出现的状态记下来即可。

2. **右移的周期性**  
   把字符串右移 `b` 位若干次后会回到原来的排列。具体回到原点的次数是 `n / gcd(n, b)`（`gcd` 为最大公约数）。这意味着右移只会产生 **有限且可预测** 的排列数。

基于这两个性质，我们只要 **遍历所有可能的排列 + 对每个排列尝试 0~9 次加法**，就能得到完整的可达集合。实现时最常见的做法是：

- 用 **BFS**（队列）从初始字符串开始，依次生成两种新状态并加入队列（如果未出现过）。  
- 由于每次操作的结果都被 `visited` 集合过滤掉，整个搜索过程只会遍历一次每个唯一状态。  

这就是 LeetCode 官方推荐的 **最优解**，时间和空间均为 `O(10 * n)`（常数 10 来自加法的循环），在本题约等于 `O(n)`。

#### 代码（Python）

```python
from collections import deque
from math import gcd

def find_lex_smallest(s: str, a: int, b: int) -> str:
    n = len(s)
    visited = set([s])
    q = deque([s])
    ans = s                     # 当前最小答案

    # 右移的周期，只会出现 n / gcd(n, b) 种不同的排列
    rotate_cycle = n // gcd(n, b)

    while q:
        cur = q.popleft()
        if cur < ans:
            ans = cur

        # ---------- 1. 加 a ----------
        # 对奇数位加 a，形成新状态
        lst = list(cur)
        for i in range(1, n, 2):
            lst[i] = str((int(lst[i]) + a) % 10)
        added = ''.join(lst)
        if added not in visited:
            visited.add(added)
            q.append(added)

        # ---------- 2. 右移 b ----------
        # 只需要右移一次，因为后续的右移会在 BFS 中自然出现
        rotated = cur[-b:] + cur[:-b]
        if rotated not in visited:
            visited.add(rotated)
            q.append(rotated)

    return ans
```

> 关键点解释  
> - `rotate_cycle = n // gcd(n, b)` 用来说明右移的**最大不同排列数**，虽然代码里不直接用它来限制循环，但它帮助我们理解为什么 BFS 不会无限增长。  
> - `visited` 相当于“已经查过的字典”，保证每个状态只入队一次。  
> - 每次取出一个状态后，立刻比较字典序，保持 `ans` 为当前最小值。

#### 复杂度  

- **时间复杂度**：`O(10 * n)` → 每个不同的排列（最多 `n` 种）只会尝试 10 次加法，整体线性可接受。  
- **空间复杂度**：`O(10 * n)` → 需要保存所有已访问的状态，数量同上。

---

## 心得  

- **核心技巧**：**状态空间搜索 + 循环剪枝**。  
- **适用场景**：  
  1. 字符串/数组的有限变换（如旋转、翻转、加法）且每种变换的取值范围有限。  
  2. 需要找最小/最大字典序或数值结果的题目。  
  3. 类似的 LeetCode 题目还有  
     - “**Minimum Number of Moves to Seat Everyone**” （利用 BFS 找最小操作次数）  
     - “**Open the Lock**” （密码锁的状态搜索）  

- **一句话总结**：  
  *把所有可达状态都枚举出来，利用集合去重，再在这些状态中挑最小的——这就是本题的解题钥匙。*

---

## 反思  

- **第一反应**：看到“任意次数、任意顺序的两种操作”，自然想到**图遍历**（把每个字符串当成图的节点）。  
- **最容易踩的坑**：  
  - 忘记对 **奇数位**（下标 1,3,5,…）而不是偶数位加 `a`。  
  - 加法后没有对 `10` 取模，导致数字超过 `'9'` 报错。  
  - 没有使用 `visited` 集合，导致 BFS 无限循环（状态重复入队）。  
- **下次类似题的第一步**：  
  *先判断每种操作的循环周期（比如 `mod 10`、旋转周期），再决定用 BFS/DFS 并配合“已访问集合”来遍历所有唯一状态。*