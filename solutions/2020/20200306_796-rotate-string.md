# #796. 旋转字符串 / Rotate String

> 难度：简单 · 标签：String、String Matching · [LeetCode 链接](https://leetcode.com/problems/rotate-string/)

---

## 题目（英文原版）

**Description**

Given two strings s and goal, return true if and only if s can become goal after some number of shifts on s.
A shift on s consists of moving the leftmost character of s to the rightmost position.

**Examples**

**Example 1:**

```
Input: s = "abcde", goal = "cdeab"
Output: true
```

**Example 2:**

```
Input: s = "abcde", goal = "abced"
Output: false
```

**Constraints**

- 1 <= s.length, goal.length <= 100
- s and goal consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `goal`，当且仅当通过对 `s` 进行若干次移位（shift）后能够得到 `goal` 时，返回 `true`。一次移位（shift）指的是将 `s` 最左侧的字符移动到最右侧的位置。

**示例 1:**  
**示例 2:**  
**约束条件:**

- `1 <= s.length, goal.length <= 100`
- `s` 和 `goal` 仅由小写英文字母组成。

**示例：**

**示例 1:**  
Input: s = "abcde", goal = "cdeab"  
Output: true  

**示例 2:**  
Input: s = "abcde", goal = "abced"  
Output: false

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把字符串 `s` 按照题目要求一次一次地“左移”，每次左移后比较一下得到的新字符串是否等于 `goal`。  
- **左移一次** 就相当于把最左边的字符摘下来，挂到最右边去。可以把它想象成把一列排好的小朋友从最前面挪到队伍尾部，顺序保持不变，只是循环了一圈。  
- 我们把这种操作循环做 `len(s)` 次（因为做 `len(s)` 次后会回到原来的字符串），每一次都用 `==` 检查是否已经和 `goal` 完全相同。只要有一次相等，就返回 `True`，否则全部尝试完返回 `False`。

这个方法之所以一定能得到答案，是因为题目限制只允许 **循环平移**（不允许插入、删除字符），而循环平移的所有可能只会出现 `len(s)` 种不同的排列。

#### 代码（Python）

```python
def rotateString_bruteforce(s: str, goal: str) -> bool:
    # 长度不同直接不可能相等
    if len(s) != len(goal):
        return False

    # 记录原始字符串，防止在循环中被改掉
    cur = s
    for _ in range(len(s)):
        # 检查当前排列是否已经等于 goal
        if cur == goal:
            return True
        # 把左边第一个字符移到右边，形成新的排列
        # 类似把队伍最前面的同学搬到队尾
        cur = cur[1:] + cur[0]   # 切片 + 拼接
    return False
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  解释：外层循环执行 `n` 次（`n = len(s)`），每一次比较 `cur == goal` 需要遍历两个长度为 `n` 的字符串，最坏情况是 `O(n)`，于是总共是 `n * n = n²`。如果把 `n` 想成 100，`n²` 就是 10,000 步，仍然可以接受，但不是最优的。

- **空间复杂度：** `O(n)`  
  解释：我们额外保存了一个和 `s` 长度相同的临时字符串 `cur`，因此需要线性空间。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每一次左移后都要重新遍历整个字符串来比较**。  
实际上，所有左移得到的字符串**都包含在**把 `s` 自己拼接一次得到的 `s + s` 中。  

举个例子：

```
s = "abcde"
s + s = "abcdeabcde"
```

如果把 `s` 循环左移两位，得到 `"cdeab"`，它正好是 `s+s` 的一个连续子串（从第 3 位开始，长度为 `len(s)`）。  
因此，**只要 `goal` 是 `s+s` 的子串**，并且两者长度相同，就说明可以通过若干次左移得到 `goal`。

关键点：

1. **拼接**：`s + s` 把所有可能的循环平移“摊开”成一条直线。  
2. **子串判断**：在这条直线上查找 `goal` 是否出现。Python 中的 `in` 操作符已经实现了高效的子串匹配（基于 `O(m+n)` 的算法，实际实现可能是 Boyer‑Moore、KMP 等），对我们来说直接使用即可。  
3. **长度相等**：如果 `s` 与 `goal` 长度不同，即使 `goal` 出现在 `s+s` 中，也不符合题意（因为只能循环平移，不能增删字符），所以先判断长度。

#### 代码（Python）

```python
def rotateString_optimal(s: str, goal: str) -> bool:
    # 长度不同直接返回 False
    if len(s) != len(goal):
        return False

    # 把 s 拼接一次，形成所有循环平移的“总集合”
    doubled = s + s          # 例: "abcde" -> "abcdeabcde"

    # 检查 goal 是否是 doubled 的子串
    # Python 的 in 已经帮我们做了高效的子串匹配
    return goal in doubled
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  解释：拼接 `s+s` 需要 `O(n)` 的时间，子串检查 `goal in doubled` 在最坏情况下也是线性时间（`n` 为字符串长度），所以整体是线性的。相比暴力的 `O(n²)`，这里的 “n” 只要几百次循环就能完成，速度快很多。

- **空间复杂度：** `O(n)`  
  解释：我们额外创建了 `doubled`，长度是原来字符串的两倍，即 `2n`，仍然是线性空间。  

---

## 心得

- **核心技巧**：把循环平移问题转化为“子串是否出现”。  
- **适用场景**：  
  1. 判断两个字符串是否是循环移位关系（本题）。  
  2. 判断一个字符串是否是另一个字符串的旋转（如 LeetCode 796 “Rotate String”）。  
  3. 判断环形数组是否存在某段连续子数组（可以把数组拼接两遍后做子数组查找）。  
- **解题钥匙**：**把所有可能的结果一次性列出来（拼接），再用“包含”检查**。

---

## 反思

- **第一反应**：直接模拟左移一次一次地比较，觉得最直观。  
- **最容易踩的坑**：  
  - 忘记先判断两个字符串长度是否相等，导致错误地返回 `True`（比如 `"a"` 与 `"aa"`）。  
  - 在暴力实现里，误把 `cur = cur[1:] + cur[0]` 写成 `cur = cur[0] + cur[1:]`，这样其实是右移，导致答案错误。  
- **下次遇到同类题**：第一步先思考“是否可以把所有可能的结果一次性展开”，如果可以，就尝试把问题转化为子串（或子数组）包含检查，这通常能把时间复杂度从平方级降到线性级。