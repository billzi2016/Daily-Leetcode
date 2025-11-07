# #3412. 字符串的镜像得分 / Find Mirror Score of a String

> 难度：中等 · 标签：Hash Table、String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-mirror-score-of-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s.
We define the mirror of a letter in the English alphabet as its corresponding letter when the alphabet is reversed. For example, the mirror of 'a' is 'z', and the mirror of 'y' is 'b'.
Initially, all characters in the string s are unmarked.
You start with a score of 0, and you perform the following process on the string s:
Return the total score at the end of the process.

**Examples**

**Example 1:**

```
Input: s = "aczzx"
Output: 5
Explanation:
```

**Example 2:**

```
Input: s = "abcdef"
Output: 0
Explanation:
For each index i , there is no index j that satisfies the conditions.
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`。  
我们将英文字母的**镜像 (mirror)** 定义为当字母表反转时对应的字母。例如，`'a'` 的镜像是 `'z'`，`'y'` 的镜像是 `'b'`。  
最初，字符串 `s` 中的所有字符均未标记。  
你从得分 `0` 开始，对字符串 `s` 执行如下过程：  
（题目原文未给出具体过程，保持原样）  
返回过程结束时的总得分。

示例 1:
```
Input: s = "aczzx"
Output: 5
Explanation:
```

示例 2:
```
Input: s = "abcdef"
Output: 0
Explanation:
对于每个索引 i，不存在满足条件的索引 j。
```

约束条件：
- 1 <= s.length <= 10^5
- s 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从左到右遍历字符串**，对每一个位置 `i`，在它右侧找第一个还没有被标记（未配对）的字符 `j`，满足 `s[j]` 是 `s[i]` 的“镜像”。  
如果找到了，就把这两个位置标记为已使用，分数加上它们的距离 `j‑i`；如果找不到，就把 `i` 标记为已使用（相当于它永远配不成）。  

> **哈希表 / 字典的类比**：可以把“已标记的下标”想象成一本记录本，键是下标，值是“是否已经配对”。我们每次查找都要遍历后面的所有字符，类似在字典里线性搜索。

这种做法一定能得到题目要求的分数，因为我们严格按照题目描述的“顺序配对”来操作。唯一的缺点是 **每次都要从 i+1 开始遍历，最坏情况会检查 `n` 次**，导致时间复杂度很高。

#### 代码（Python）

```python
def mirror_score_bruteforce(s: str) -> int:
    n = len(s)
    used = [False] * n                 # 标记每个下标是否已经配对
    def mirror(ch: str) -> str:
        # a<->z, b<->y, ... 通过字母表反转得到镜像字符
        return chr(ord('a') + (25 - (ord(ch) - ord('a'))))

    score = 0
    for i in range(n):
        if used[i]:
            continue                    # 已经配对过，直接跳过
        mir = mirror(s[i])
        # 在 i 右侧寻找第一个未使用且是镜像的字符
        j = i + 1
        while j < n:
            if not used[j] and s[j] == mir:
                break
            j += 1
        if j < n:                       # 找到了配对
            score += j - i              # 距离加到分数
            used[i] = used[j] = True    # 两个位置都标记为已使用
        else:
            used[i] = True               # 找不到配对，只标记为已使用

    return score
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  想象 `n` 是 10,000。最坏情况下，每个字符都要向后遍历几乎整个字符串，等价于 **“n 次 n”** 的操作。  
- **空间复杂度**：`O(n)`  
  需要一个长度为 `n` 的布尔数组 `used` 来记录哪些位置已经配对。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要往后线性搜索**。如果我们能够在 **看到字符时立刻知道它最近的镜像位置**，就可以把搜索的时间降到常数级。

关键观察：

1. **镜像是一对固定的字符**。比如 `'a'` 的镜像一定是 `'z'`，`'c'` 的镜像一定是 `'x'`，不随位置变化。  
2. 当我们从左到右遍历字符串时，**如果当前字符的镜像已经出现过且还未被配对**，我们就可以立刻完成配对。  
3. 为了快速找到“最近的、尚未配对的镜像位置”，我们可以为每个字母维护一个 **栈**（后进先出）。栈里只存放 **尚未配对的下标**。  
   - 当看到字符 `ch` 时，检查 **它的镜像字符对应的栈** 是否非空。  
   - 若非空，栈顶就是最近的、尚未配对的镜像下标 `j`。我们弹出它，得分 `i - j`。  
   - 若空，则把当前下标 `i` 压入 **`ch` 自己的栈**，等待以后可能出现的镜像来配对。

> **栈的类比**：想象每个字母都有一个“小盒子”，盒子里放的是还没有找到“镜子伙伴”的位置。后来的位置先放进去，先出来配对——这正好符合 “最近的未配对位置优先配对” 的需求。

这样，**每个字符只会被压栈一次、弹栈一次**，整个过程是线性的。

#### 代码（Python）

```python
def mirror_score_optimal(s: str) -> int:
    n = len(s)

    # 计算字母的镜像，例如 mirror['a'] == 'z'
    mirror = {chr(ord('a') + i): chr(ord('a') + (25 - i)) for i in range(26)}

    # 为每个字母准备一个栈（用 list 实现），下标从 0 到 25 对应 a~z
    stacks = [[] for _ in range(26)]

    def idx(ch: str) -> int:
        """把字符映射到 0~25 的整数索引，方便取对应的栈"""
        return ord(ch) - ord('a')

    score = 0
    for i, ch in enumerate(s):
        mir = mirror[ch]                     # 当前字符的镜像字符
        mir_idx = idx(mir)                   # 镜像字符对应的栈编号

        if stacks[mir_idx]:                  # 镜像栈非空 → 能配对
            j = stacks[mir_idx].pop()        # 取出最近的未配对镜像位置
            score += i - j                   # 距离加分
        else:
            # 没有可配对的镜像，把自己压进去，等待以后出现镜像
            stacks[idx(ch)].append(i)

    return score
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每个字符只做 **一次压栈** 或 **一次弹栈**，相当于 “n 次常数操作”。相比暴力的 `n²`，大幅提升。  
- **空间复杂度**：`O(n)`（最坏情况所有字符都压在各自的栈里）  
  实际上只需要 26 个栈的指针，额外的存储是所有下标的总和，和输入长度同阶。

> **与暴力解对比**：时间从 “每次遍历剩余部分” 降到 “一次遍历全程”，空间略增（需要额外的栈），但仍然是线性可接受的。

---

## 心得

- **核心技巧**：利用 **“每个字符对应的镜像是固定的”**，结合 **栈** 实现 “最近未配对位置”的快速匹配。  
- **适用场景**：  
  1. **配对类问题**，如“括号匹配”“相同字符配对”。  
  2. **单调栈/最近未处理元素** 的场景，例如 “每日温度” / “柱状图最大矩形”。  
  3. **字符映射配对**，如 “字符相互映射的最短距离求和”。  
- **一句话总结解题钥匙**：**“把每个字母的未配对位置装进自己的小盒子，遇到镜像时立刻打开对应盒子取出最近的下标配对”。**

---

## 反思

- **第一反应**：直接写两层循环去找每个字符右侧的镜像，忽视了可以利用字符之间的固定映射关系。  
- **最容易踩的坑**：  
  - **忘记把已配对的下标从栈中弹出**，导致同一个位置被重复使用。  
  - **镜像计算错误**（比如写成 `chr(ord('a') + (ord(ch) - ord('a')))`），要确保是 “字母表反转”。  
  - **边界情况**：全部相同字符或全没有镜像的字符串，算法仍需正常返回 0。  
- **下次遇到同类题**：第一步先思考 **“是否可以在一次遍历中完成配对？”**，如果答案是 “可以”，就尝试 **“使用栈/哈希表记录未完成的元素”。**这样往往能把二次循环的暴力思路优化到线性时间。