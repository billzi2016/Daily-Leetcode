# #899. 有序队列 / Orderly Queue

> 难度：困难 · 标签：Math、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/orderly-queue/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k. You can choose one of the first k letters of s and append it at the end of the string.
Return the lexicographically smallest string you could have after applying the mentioned step any number of moves.

**Examples**

**Example 1:**

```
Input: s = "cba", k = 1
Output: "acb"
Explanation: 
In the first move, we move the 1st character 'c' to the end, obtaining the string "bac".
In the second move, we move the 1st character 'b' to the end, obtaining the final result "acb".
```

**Example 2:**

```
Input: s = "baaca", k = 3
Output: "aaabc"
Explanation: 
In the first move, we move the 1st character 'b' to the end, obtaining the string "aacab".
In the second move, we move the 3rd character 'c' to the end, obtaining the final result "aaabc".
```

**Constraints**

- 1 <= k <= s.length <= 1000
- s consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。你可以从 `s` 的前 `k` 个字符中任选一个，将其移动到字符串的末尾（append）。可以无限次地重复上述操作。返回在任意次数操作后能够得到的字典序（lexicographically）最小的字符串。

示例 1:
```
Input: s = "cba", k = 1
Output: "acb"
Explanation: 
在第一次操作中，我们将第 1 个字符 'c' 移动到末尾，得到字符串 "bac"。  
在第二次操作中，我们将第 1 个字符 'b' 移动到末尾，得到最终结果 "acb"。
```

示例 2:
```
Input: s = "baaca", k = 3
Output: "aaabc"
Explanation: 
在第一次操作中，我们将第 1 个字符 'b' 移动到末尾，得到字符串 "aacab"。  
在第二次操作中，我们将第 3 个字符 'c' 移动到末尾，得到最终结果 "aaabc"。
```

约束条件：
- 1 <= k <= s.length <= 1000
- s 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的操作都枚举出来**，把每一次可以得到的字符串都放进集合里，最后取字典序最小的那个。

- **数据结构**：我们可以把每一次得到的字符串放进 `set`（集合），集合就像一本“已经出现过的单词本”，可以帮助我们避免把同一个字符串重复算进去。  
- **操作**：每一步我们只能把 **前 k** 个字符中的任意一个挑出来，放到字符串的末尾。于是我们可以对当前字符串的前 `k` 个位置循环尝试，把挑选的字符移到末尾，得到新的字符串，再继续往下走。  
- **正确性**：只要我们把**所有**合法的移动序列都遍历完，就一定会碰到字典序最小的那个，因为没有任何合法的字符串会被遗漏。  

> 这实际上是一棵**状态树**：根节点是原始字符串，子节点是一次合法移动后的字符串，子节点的子节点是再一次合法移动后的字符串……只要把这棵树遍历完（比如用深度优先搜索），就能得到全部可能的结果。

**为什么会慢**  
- 树的宽度是 `k`，深度最坏可以是 `n!`（因为我们可以把字符重新排列成任意顺序），所以搜索空间是 **指数级** 的。  
- 每生成一个新字符串都要复制一次（长度为 `n`），导致时间和空间都非常大。

#### 代码（Python）

```python
from collections import deque

def orderlyQueue_bruteforce(s: str, k: int) -> str:
    """
    暴力 BFS（广度优先搜索）实现
    把每一次合法的移动都加入队列，遍历所有可能的字符串
    """
    n = len(s)
    visited = set()          # 记录已经出现过的字符串，防止重复搜索
    q = deque([s])           # 待搜索的队列，初始只有原字符串
    visited.add(s)

    while q:
        cur = q.popleft()
        # 对前 k 个字符尝试移动到末尾
        for i in range(k):
            # 把第 i 个字符（0-index）取出来放到末尾
            nxt = cur[:i] + cur[i+1:] + cur[i]
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)

    # 所有能得到的字符串都在 visited 里，返回字典序最小的那个
    return min(visited)
```

> 关键行解释  
> - `visited = set()`：相当于一本“已经看过的单词本”，防止把同一个字符串反复处理。  
> - `for i in range(k):`：遍历前 `k` 个位置，模拟“挑选第 i 个字符并移动到末尾”。  
> - `nxt = cur[:i] + cur[i+1:] + cur[i]`：把第 `i` 个字符搬到字符串最后。  

#### 复杂度

- **时间复杂度**：`O(k * |S|)`，其中 `|S|` 是所有可能状态的数量。最坏情况下 `|S|` 接近 `n!`（全排列），因此是 **指数级** 的。  
- **空间复杂度**：`O(|S| * n)`，需要保存所有已访问的字符串，同样是指数级。

> 简单来说，随着字符串长度稍微增大（比如 10~12），这套办法就会“爆炸”，在实际面试或竞赛中根本不可用。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们把所有可能的排列都枚举了。其实我们并不需要这么多，只要弄清楚在不同的 `k` 下我们到底能实现哪些排列即可。

1. **k = 1 的情况**  
   - 我们每次只能把**第一个字符**移动到末尾。  
   - 这相当于在原字符串上做**循环左移**：`"abc"` → `"bca"` → `"cab"` → `"abc"` ……  
   - 所以所有能够得到的字符串**恰好是所有旋转（循环移位）**。  
   - 因此只要遍历 `n` 次（每次左移一位），找出字典序最小的那一次即可。  
   - 这一步的时间是 `O(n^2)`（每次比较/生成长度为 `n` 的字符串），空间 `O(1)`（只保存最小的那一个）。

2. **k ≥ 2 的情况**  
   - 当 `k ≥ 2` 时，操作的自由度大大提升。我们可以把 **前两个字符** 进行任意调换：  
     - 把第二个字符移动到末尾，然后再把原来的第一个字符移动到末尾，这相当于把前两个字符交换位置。  
   - 通过不断交换相邻字符，我们可以实现**任意的相邻交换**，这正是**冒泡排序**的核心操作。  
   - 既然任意相邻交换都可以完成，那么我们就可以把整个字符串**随意排列**，最终只要把字符按字典序排序即可得到最小字符串。  
   - 排序可以使用 Python 内置的 `sorted`，时间 `O(n log n)`，空间 `O(n)`（存放排好序的字符列表）。

> 用生活化的类比：  
> - 当只能把第一件衣服挂到衣柜最末尾（k=1）时，你只能把衣服顺序“循环搬动”。  
> - 当你可以把前两件衣服随意调换（k≥2）时，就相当于拥有了**任意换位**的能力，所有衣服都能按字母顺序挂好。

#### 代码（Python）

```python
def orderlyQueue(s: str, k: int) -> str:
    """
    最优解：
    - k == 1  -> 枚举所有循环左移，取最小
    - k >= 2  -> 直接对字符排序
    """
    if k == 1:
        # 只需要检查所有 n 次循环左移
        candidates = [s[i:] + s[:i] for i in range(len(s))]
        return min(candidates)          # 字典序最小的那个
    else:
        # k >= 2 时任意排列都可以实现，直接排序即可
        return ''.join(sorted(s))
```

> 关键行解释  
> - `if k == 1:`：单独处理只能左移的情况。  
> - `candidates = [s[i:] + s[:i] for i in range(len(s))]`：生成所有旋转字符串（把前 `i` 个字符搬到后面）。  
> - `return ''.join(sorted(s))`：把字符按字母顺序重新排好，得到全局最小的字符串。

#### 复杂度

- **时间复杂度**  
  - `k == 1`：`O(n^2)` —— 需要生成 `n` 个长度为 `n` 的子串并比较字典序。  
  - `k >= 2`：`O(n log n)` —— 只做一次排序，快得多。  
- **空间复杂度**  
  - `k == 1`：`O(n)` —— 只保存当前最小的字符串（列表 `candidates` 在 Python 中会暂时占 `O(n)`，但可以改写成单遍遍历降低到 `O(1)`）。  
  - `k >= 2`：`O(n)` —— 排序后得到的字符列表。

> 与暴力解相比，最优解把指数级的搜索空间压缩到了线性或对数级别，瞬间可以处理 `s.length = 1000` 的极限输入。

---

## 心得

- **核心技巧**：根据 `k` 的取值把问题分成两类——**循环移位**（k=1）和**任意排列**（k≥2）。  
- **适用的题型**  
  1. “只允许移动首字符” 的旋转类问题（如 LeetCode 796 Rotate String）。  
  2. “k≥2 能实现任意相邻交换” 的排列类问题（如 LeetCode 1156 Swap For Longest Repeated Character Substring 的思路）。  
- **一句话总结**：`k==1` → 检查所有旋转；`k>=2` → 直接把字符排好序。

---

## 反思

- **第一反应**：看到“把前 k 个字符中的任意一个移到末尾”，自然会想到**枚举所有可能的移动序列**。  
- **最容易踩的坑**  
  - 忽略了 `k >= 2` 时可以实现**相邻交换**的事实，导致误以为仍需枚举。  
  - 对 `k==1` 的实现如果直接用 `while` 循环不断左移，需要注意循环次数恰好是 `n`，否则会陷入无限循环。  
- **下次遇到同类题**：先判断**操作的自由度**（能否实现相邻交换），如果可以，就考虑**排序**或**贪心**；如果只能循环移动，则只需要**遍历所有旋转**。这样可以快速定位最优思路，避免暴力搜索的陷阱。