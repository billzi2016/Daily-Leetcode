# #821. 字符的最短距离 / Shortest Distance to a Character

> 难度：简单 · 标签：Array、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/shortest-distance-to-a-character/)

---

## 题目（英文原版）

**Description**

Given a string s and a character c that occurs in s, return an array of integers answer where answer.length == s.length and answer[i] is the distance from index i to the closest occurrence of character c in s.
The distance between two indices i and j is abs(i - j), where abs is the absolute value function.

**Examples**

**Example 1:**

```
Input: s = "loveleetcode", c = "e"
Output: [3,2,1,0,1,0,0,1,2,2,1,0]
Explanation: The character 'e' appears at indices 3, 5, 6, and 11 (0-indexed).
The closest occurrence of 'e' for index 0 is at index 3, so the distance is abs(0 - 3) = 3.
The closest occurrence of 'e' for index 1 is at index 3, so the distance is abs(1 - 3) = 2.
For index 4, there is a tie between the 'e' at index 3 and the 'e' at index 5, but the distance is still the same: abs(4 - 3) == abs(4 - 5) = 1.
The closest occurrence of 'e' for index 8 is at index 6, so the distance is abs(8 - 6) = 2.
```

**Example 2:**

```
Input: s = "aaab", c = "b"
Output: [3,2,1,0]
```

**Constraints**

- 1 <= s.length <= 104
- s[i] and c are lowercase English letters.
- It is guaranteed that c occurs at least once in s.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个在 `s` 中出现的字符 `c`，返回一个整数数组 `answer`，其中 `answer.length == s.length`，且 `answer[i]` 表示下标 `i` 到最近一次出现字符 `c` 的距离。  
两个下标 `i` 和 `j` 之间的距离定义为 `abs(i - j)`，其中 `abs` 为绝对值函数。

**示例 1:**  
**示例 2:**  
**约束条件:**

**示例**

**示例 1:**  
```text
Input: s = "loveleetcode", c = "e"
Output: [3,2,1,0,1,0,0,1,2,2,1,0]
```
**解释:** 字符 `'e'` 出现在下标 3、5、6 和 11（从 0 开始计数）。  
下标 0 最近的 `'e'` 在下标 3，距离为 `abs(0 - 3) = 3`。  
下标 1 最近的 `'e'` 在下标 3，距离为 `abs(1 - 3) = 2`。  
对于下标 4，虽然下标 3 和下标 5 处的 `'e'` 距离相同，但距离仍为 `abs(4 - 3) == abs(4 - 5) = 1`。  
下标 8 最近的 `'e'` 在下标 6，距离为 `abs(8 - 6) = 2`。

**示例 2:**  
```text
Input: s = "aaab", c = "b"
Output: [3,2,1,0]
```

**约束条件**
- `1 <= s.length <= 10^4`
- `s[i]` 和 `c` 为小写英文字母。
- 保证字符 `c` 至少在 `s` 中出现一次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个位置 `i`，把字符串里所有出现字符 `c` 的下标都找出来，算出 `|i - pos|` 的最小值**。  
这相当于把每个位置都和所有 “目标字符” 进行一次比较，就像在找字典里所有含有某个字根的词，然后挑出最接近的那一本。  

- **用到的数据结构**：  
  - `list`（列表）来存放所有出现字符 `c` 的下标。列表就像一排排的抽屉，依次放下标。  
- **为什么正确**：  
  - 对于位置 `i`，真正的最近距离一定是它和某个 `c` 的下标之间的绝对差值的最小值。我们把所有可能的下标都遍历一遍，必然能得到这个最小值。  

- **时间/空间复杂度的大白话**：  
  - 假设字符串长度是 `n`，字符 `c` 出现了 `k` 次。  
  - 对每个 `i`（共 `n` 次），我们都要遍历这 `k` 个下标，最坏情况下 `k` 接近 `n`，于是总的比较次数大约是 `n × n`，也就是 **`O(n²)`**。可以把它想象成在一个 `n × n` 的棋盘上走遍每一个格子。  
  - 额外的空间只用来存放 `k` 个下标，最多 `O(n)`，即 **`O(n)`** 的额外空间。

#### 代码（Python）

```python
def shortestToChar_brute(s: str, c: str) -> list[int]:
    # 1️⃣ 先把所有字符 c 的位置收集到一个列表里
    positions = []                     # 这里相当于“抽屉”，把每个出现的下标放进去
    for idx, ch in enumerate(s):
        if ch == c:
            positions.append(idx)

    # 2️⃣ 对每个位置 i，遍历所有 c 的位置，找最小距离
    answer = []                         # 用来存放最终答案
    for i in range(len(s)):
        min_dist = float('inf')         # 初始设为无限大，后面会被更小的距离替代
        for pos in positions:          # 把每个“抽屉”里的下标都拿出来比较
            dist = abs(i - pos)         # 绝对值就是两下标之间的距离
            if dist < min_dist:
                min_dist = dist
        answer.append(min_dist)         # 把该位置的最近距离加入答案
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 想象成在一个 `n × n` 的方格里每格都走一遍，随着字符串变长，耗时会快速增长。  
- **空间复杂度**：`O(n)` —— 只用了一个列表保存所有 `c` 的下标，最坏情况下会存 `n` 个数字。

---

### 2. 最优解

#### 思路  

暴力解慢的地方在于**每次都要遍历所有 `c` 的位置**。我们可以把“所有 `c` 的位置”这件事做两遍预处理，**把最近的距离提前算好**，这样查询时只需要 `O(1)`。

核心想法是 **两次线性扫描**（Two Pass）：

1. **从左往右**：记录最近的 `c` 出现位置 `prev`，对每个下标 `i`，如果 `s[i]==c` 就把 `prev=i`，否则答案 `ans[i]=i-prev`（如果左边还没有出现 `c`，则设 `prev=-∞`，这里用一个很大的负数代替）。这样得到的 `ans[i]` 是**左侧最近的 `c`**的距离。
2. **从右往左**：同理记录最近的 `c` 出现位置 `next`，对每个下标 `i`，如果 `s[i]==c` 就把 `next=i`，否则把 `ans[i]=min(ans[i], next-i)`，取左侧和右侧距离的最小值。

这就像**把字符 `c` 当成灯塔**，从左边点亮左侧的灯光，从右边再点亮右侧的灯光，最后每个位置取两盏灯光的最近距离。

- **核心算法/数据结构**：  
  - **两次遍历**（Two Pass）+ **数组**（list）保存答案。数组在这里相当于一排排的信箱，每个信箱里先放左侧灯塔的距离，再和右侧灯塔的距离比较取最小。  
- **为什么正确**：  
  - 对任意位置 `i`，最近的 `c` 要么在左边，要么在右边（或者恰好是 `i` 本身）。左到右的扫描保证我们知道左边最近的 `c`，右到左的扫描保证我们知道右边最近的 `c`，两者取最小即为全局最近距离。

#### 代码（Python）

```python
def shortestToChar(s: str, c: str) -> list[int]:
    n = len(s)
    answer = [0] * n                     # 先准备好长度为 n 的数组，默认全 0

    # ---------- 第一次遍历：左 → 右 ----------
    prev = -10**9                         # 一个很小的数，表示“左边还没有出现 c”
    for i in range(n):
        if s[i] == c:
            prev = i                     # 碰到 c，更新最近的左侧位置
        answer[i] = i - prev             # 与最近的左侧 c 的距离
        # 如果 prev 仍是负无穷，则 i - prev 会是一个很大的正数，后面会被右侧距离覆盖

    # ---------- 第二次遍历：右 → 左 ----------
    nxt = 10**9                           # 一个很大的数，表示“右边还没有出现 c”
    for i in range(n - 1, -1, -1):
        if s[i] == c:
            nxt = i                     # 碰到 c，更新最近的右侧位置
        # 取左侧距离和右侧距离的最小值
        answer[i] = min(answer[i], nxt - i)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了两遍字符串，每遍都是一次线性扫描。可以想象成在跑道上来回跑两次，跑完后每个位置的答案已经算好。  
- **空间复杂度**：`O(n)` —— 需要一个长度为 `n` 的数组来保存答案，除此之外只用了几个整数变量，属于**原地**（不额外开辟大块空间）使用。  

与暴力解相比，时间从 **`O(n²)`** 降到了 **`O(n)`**，在 `n` 达到 10⁴ 时差距非常明显。

---

## 心得

- **核心技巧**：**双向扫描（Two Pass）**，先记录左侧最近信息，再记录右侧最近信息，最后取最小。  
- **适用的题型**：  
  1. *Shortest Distance to a Character*（本题）  
  2. *Find Nearest Right/Left 1*（在二进制数组中找最近的 1）  
  3. *Candy*（左右约束的分配问题，也常用双向扫描）  
- **一句话总结解题钥匙**：**“把全局最近距离拆成左侧最近 + 右侧最近，分别线性预处理，再取最小”。**

---

## 反思

- **第一反应**：直接想遍历所有 `c` 的位置求最小距离，结果是暴力 `O(n²)`。  
- **最容易踩的坑**：  
  - 忘记处理左侧或右侧还没有出现 `c` 的情况（需要用一个足够大的负数/正数占位）。  
  - 直接在第一次遍历时把答案写死，导致右侧更近的 `c` 没有被考虑。  
- **下次遇到同类题**：**第一步想到“左右最近”**，判断能否用两遍线性扫描分别收集左侧/右侧信息，再合并。这样往往能把时间从平方级降到线性级。