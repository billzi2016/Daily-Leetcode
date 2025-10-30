# #3403. 从盒子中找出字典序最大的字符串 I / Find the Lexicographically Largest String From the Box I

> 难度：中等 · 标签：Two Pointers、String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-the-lexicographically-largest-string-from-the-box-i/)

---

## 题目（英文原版）

**Description**

You are given a string word, and an integer numFriends.
Alice is organizing a game for her numFriends friends. There are multiple rounds in the game, where in each round:
Find the lexicographically largest string from the box after all the rounds are finished.

**Examples**

**Example 1:**

```
Input: word = "dbca", numFriends = 2
Output: "dbc"
Explanation:
All possible splits are:
```

**Example 2:**

```
Input: word = "gggg", numFriends = 4
Output: "g"
Explanation:
The only possible split is: "g" , "g" , "g" , and "g" .
```

**Constraints**

- 1 <= word.length <= 5 * 103
- word consists only of lowercase English letters.
- 1 <= numFriends <= word.length

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `word` 和一个整数 `numFriends`。Alice 正在为她的 `numFriends` 位朋友组织一场游戏。游戏包含多轮，在每一轮中：  
- …（题目具体的每轮操作在原题中省略）  
在所有回合结束后，求盒子中**字典序（lexicographically）**最大的字符串。

**示例**

*示例 1*  
```
Input: word = "dbca", numFriends = 2
Output: "dbc"
Explanation:
所有可能的划分有：
```
（此处省略具体划分过程）

*示例 2*  
```
Input: word = "gggg", numFriends = 4
Output: "g"
Explanation:
唯一可能的划分是："g", "g", "g", 和 "g"。
```

**约束条件**  

- `1 <= word.length <= 5 * 10^3`
- `word` 仅由小写英文字母组成。
- `1 <= numFriends <= word.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
题目等价于：**在保持字符相对顺序不变的前提下，删掉 `numFriends‑1` 个字符，使剩下的字符串尽可能大（字典序最大）**。  
最直接的做法就是把所有可能的删法枚举出来，求出每种情况下剩下的字符串，然后取最大值。

- **枚举方式**：对每一种 “删哪 `numFriends‑1` 个位置” 的组合，拼接剩下的字符得到一个子串。  
- **数据结构类比**：我们可以把原字符串想象成一本书的每一页，删掉某几页后剩下的就是我们要的“新书”。枚举所有删页方案就像把所有可能的“目录”都列出来。  

为什么正确？因为我们把**所有**合法的删法都遍历了一遍，最大值自然就在其中。

#### 代码（Python）  
```python
import itertools

def largestString_bruteforce(word: str, numFriends: int) -> str:
    n = len(word)
    # 需要保留的字符个数
    keep = n - numFriends + 1

    best = ""                     # 用来记录目前找到的最大串
    # 从 0~n-1 的位置中挑选 keep 个不变的下标（相当于删除其余的）
    for idxs in itertools.combinations(range(n), keep):
        # 按下标顺序拼接字符，保持原来的相对顺序
        cur = "".join(word[i] for i in idxs)
        if cur > best:            # Python 的 > 已经是字典序比较
            best = cur
    return best
```
> 关键点说明  
> - `itertools.combinations` 会返回所有长度为 `keep` 的下标组合。  
> - `cur > best` 用来比较两个字符串的字典序，等价于“哪个更大”。  

#### 复杂度  
- **时间复杂度**：`O(C(n, keep) * n)`，其中 `C(n, keep)` 是组合数，表示所有可能的下标组合数。  
  - 直观上可以理解为“要把所有可能的删法都尝试一次”，当 `n` 为 5000 时根本不可行。  
- **空间复杂度**：`O(n)`，主要是保存临时的字符串 `cur`（最坏需要 `keep ≤ n` 长度）。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**枚举所有组合**，这会导致指数级的时间。  
实际上我们只需要得到字典序最大的 **长度为 `L = n - numFriends + 1` 的子序列**（保持相对顺序），这可以用**贪心 + 单调栈**一次遍历完成。

**关键观察**  
- 为了让结果尽可能大，**越靠前的字符越重要**。  
- 当我们在遍历字符串时，如果当前字符 `c` 比栈顶字符更大，并且我们还有“删掉字符的余地”，那么把栈顶弹出，让 `c` 站到更前面，这样整体字典序会提升。  
- “删掉字符的余地” = 还能删除的字符数 `k = numFriends - 1`（因为最终要保留 `L` 个字符）。  

**算法步骤（单调栈）**  
1. 设 `k = numFriends - 1` 为还能删除的字符数，`stack = []` 保存已经决定的字符。  
2. 从左到右遍历 `word` 的每个字符 `ch`：  
   - 当 `stack` 非空且 `k > 0` 且 `stack[-1] < ch` 时，弹出栈顶（相当于“删掉”这个字符），`k -= 1`。  
   - 将 `ch` 压入栈。  
3. 循环结束后，栈中可能比目标长度 `L` 长。只需要取栈的前 `L` 个字符即为答案。  

**为什么正确**（零基础解释）  
- **单调栈的作用**：它始终保持栈内字符从左到右 **非递增**（即从大到小）。当出现更大的字符 `ch` 时，我们把左边比它小的字符都踢出去，因为把大字符提前放到左边会让整体字典序更大。  
- **删字符的上限**：我们只能删 `k` 次，防止把后面必须保留的字符全部删光。每删一次就把 `k` 减 1，等 `k` 用完后就只能把后面的字符直接放进去，保证最终长度不小于 `L`。  
- **截断到 `L`**：即使我们在遍历结束后还有多余的字符（因为没有机会再删），只要把最左边的 `L` 个字符留下，已经是字典序最大的了，因为左边的字符已经尽可能大，右边的多余字符对前面的顺序没有影响。  

**类比**：把字符想象成一排小球，球的大小对应字母的字典序。我们手里有一根可以弹出小球的棍子（删字符的次数）。从左到右扫过每个球时，如果发现更大的球，就把之前的“小球”弹掉，让大球往前走。最后留下的前 `L` 个球，就是字典序最大的排列。

#### 代码（Python）  
```python
def largestString(word: str, numFriends: int) -> str:
    """
    返回字典序最大的子序列，长度为 len(word) - numFriends + 1
    """
    n = len(word)
    keep = n - numFriends + 1          # 最终需要保留的字符数
    k = numFriends - 1                 # 最多可以删除的字符数

    stack = []                         # 单调栈，保存已经决定的字符
    for ch in word:
        # 只要还有删字符的机会，且栈顶字符比当前字符小，就弹出栈顶
        while k > 0 and stack and stack[-1] < ch:
            stack.pop()
            k -= 1
        stack.append(ch)

    # 栈可能比目标长度长，只取前 keep 个字符
    result = "".join(stack[:keep])
    return result
```
> 关键行中文注释  
> - `k = numFriends - 1`：相当于“我们可以把多少个字符踢出盒子”。  
> - `while k > 0 and stack and stack[-1] < ch:`：只要还有踢人的机会，且左边的字符更“小”，就把它踢掉，让更大的字符靠前。  
> - `stack[:keep]`：把多余的“后备字符”丢掉，只保留需要的前 `keep` 个。  

#### 复杂度  
- **时间复杂度**：`O(n)`，每个字符最多进栈一次、出栈一次。  
  - 与暴力解的 `O(C(n, L) * n)` 相比，线性时间在 `n ≤ 5000` 的限制下毫无压力。  
- **空间复杂度**：`O(n)`，最坏情况下栈会存放所有字符（例如字符单调不下降时）。  

---

## 心得  

- **核心技巧**：**单调栈（贪心）** 用来在保持相对顺序的前提下，删除一定数量的字符以获得字典序最大的子序列。  
- **适用的题型**（类似思路）：  
  1. “删除 K 个字符得到字典序最大的字符串”（LeetCode 402 / 1081 变形）。  
  2. “构造字典序最小的子序列”——同样用单调栈，只是弹出条件改为 `stack[-1] > ch`。  
  3. “单调栈求最大矩形/下一个更大元素”等需要维护单调性的场景。  
- **一句话总结解题钥匙**：**“把左边的‘小’字符踢走，让更大的字符尽可能往左”**。

---

## 反思  

- **第一反应**：看到“字典序最大 + 删除固定数量的字符”，立刻想到枚举所有组合（暴力），随后想到“怎么一次遍历就搞定？”  
- **最容易踩的坑**：  
  - **删除次数控制错误**：一定要把可删除的次数设为 `numFriends‑1`，否则最终长度会不对。  
  - **截断长度**：栈可能比目标长度长，忘记 `stack[:keep]` 会得到错误的答案。  
  - **特殊字符**：全部相同字符时，循环不会弹出，最终需要截断，否则会返回过长的字符串。  
- **下次类似题的第一步**：**先把需求转化为“保留多少字符 / 删除多少字符”，再想单调栈或贪心的“一次遍历”方案**。这样可以快速从暴力思路跳到最优实现。