# #2390. 去除字符串中的星号 / Removing Stars From a String

> 难度：中等 · 标签：String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/removing-stars-from-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s, which contains stars *.
In one operation, you can:
Return the string after all stars have been removed.
Note:

**Examples**

**Example 1:**

```
Input: s = "leet**cod*e"
Output: "lecoe"
Explanation: Performing the removals from left to right:
- The closest character to the 1st star is 't' in "leet**cod*e". s becomes "lee*cod*e".
- The closest character to the 2nd star is 'e' in "lee*cod*e". s becomes "lecod*e".
- The closest character to the 3rd star is 'd' in "lecod*e". s becomes "lecoe".
There are no more stars, so we return "lecoe".
```

**Example 2:**

```
Input: s = "erase*****"
Output: ""
Explanation: The entire string is removed, so we return an empty string.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters and stars *.
- The operation above can be performed on s.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅包含小写英文字母和星号（*）的字符串 `s`。  
在一次操作中，你可以将星号（*）及其左侧最近的一个非星号字符一起删除。  
请在所有星号（*）都被删除后，返回剩余的字符串。

**示例 1**  
输入: `s = "leet**cod*e"`  
输出: `"lecoe"`  
**解释**：按照从左到右的顺序依次执行删除操作：
- 第一个星号左侧最近的字符是 `"t"`，删除后得到 `"lee*cod*e"`。  
- 第二个星号左侧最近的字符是 `"e"`，删除后得到 `"lecod*e"`。  
- 第三个星号左侧最近的字符是 `"d"`，删除后得到 `"lecoe"`。  
此时已不存在星号，返回 `"lecoe"`。

**示例 2**  
输入: `s = "erase*****"`  
输出: `""`  
**解释**：所有字符都被星号（*）及其左侧字符删除，最终得到空字符串。

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母和星号（*）组成。  
- 可以对 `s` 执行上述操作直至所有星号被删除。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次遍历字符串，遇到 `*` 就把它左边最近的字符和自己一起删掉**。  
因为 Python 的字符串是不可变的，我们可以把每一次删掉的操作都转成“重新拼接”一个新字符串：

1. 从左到右扫描 `s`。  
2. 遇到普通字母就直接往结果里加。  
3. 遇到 `*` 时，把已经得到的结果 **倒着找第一个字符**（这就是最近的左侧字符），把它删掉，同时也不把 `*` 加进去。  

这相当于每次都要 **遍历已经得到的结果一次** 来找要删掉的字符，所以时间会比较慢。

> 类比：把结果当成一本已经写好的书，遇到星号就要把书的最后一页翻出来检查并删除——每次都要从头翻到最后。

这种做法当然是**正确的**，因为我们始终遵循题目“左侧最近字符被星号抵消”的规则，只是实现方式不够高效。

#### 代码（Python）

```python
def removeStars_bruteforce(s: str) -> str:
    # 保存已经处理好的字符（类似一本书的已写内容）
    res = []                     # list 便于后面拼接
    for ch in s:
        if ch != '*':
            # 普通字符直接放进去
            res.append(ch)
        else:
            # 碰到星号，要把左侧最近的字符删掉
            # 这里用 while 循环倒着找第一个非 '*' 的字符
            # 实际上因为我们已经把 '*' 前面的字符都放进了 res，
            # 所以直接 pop 最后一个字符即可
            if res:              # 防止空列表 pop 报错（虽然题目保证一定有可删字符）
                res.pop()
            # 星号本身不加入结果
    # 把列表转回字符串
    return ''.join(res)
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  - 每遇到一个 `*`，我们都要在已经得到的结果里找并删除最近的字符，这一步在最坏情况下是遍历已处理字符的长度。若有 `k` 个星号，整体操作大约是 `1 + 2 + … + k ≈ k²/2`，所以是二次时间。  
  - 用大白话说，就是“如果字符串里有 10,000 个星号，程序大概要跑 100,000,000 步”，会明显慢。

- **空间复杂度：** `O(n)`  
  - 我们额外用了一个列表 `res` 来保存中间结果，最坏情况下会和原字符串等长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于每次删除左侧最近字符时都要遍历已有结果**。  
如果我们能把“最近的字符”随时拿到手，而不必遍历，那就可以把时间降到线性。

这正是 **栈（stack）** 的用武之地：

- 栈是一种 **后进先出（LIFO）** 的结构，最靠近栈顶的元素正好是“左侧最近、还未被删除的字符”。  
- 当遍历到普通字母时，把它 **压入栈**（相当于记下来）。  
- 当遍历到 `*` 时，**弹出栈顶**（把最近的字符删掉），并且不把 `*` 放进去。  

整个过程只需要一次遍历，每个字符最多压入一次、弹出一次，时间是 `O(n)`。

> 类比：想象一根棍子上依次贴了字母标签，星号出现时我们直接把棍子最上面的标签撕掉——不需要再往下找。

#### 代码（Python）

```python
def removeStars(s: str) -> str:
    """
    使用栈一次遍历完成所有星号的消除
    """
    stack = []                     # 用列表充当栈
    for ch in s:
        if ch == '*':
            # 星号出现，弹出栈顶（最近的字符）
            if stack:              # 题目保证一定有可弹元素，这里防御性检查
                stack.pop()
        else:
            # 普通字符压入栈中
            stack.append(ch)
    # 栈里剩下的字符本身就是答案，按顺序拼成字符串
    return ''.join(stack)
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 只遍历一次字符串，每个字符的压栈或弹栈操作都是 `O(1)`，所以整体是线性时间。  
  - 与暴力解相比，时间从二次下降到一次遍历，处理 10⁵ 长度的字符串也毫秒级。

- **空间复杂度：** `O(n)`  
  - 最坏情况下（没有星号）所有字符都要压进栈，使用的额外空间和原字符串等长。  
  - 这已经是最优的，因为最终答案本身就需要保存这些字符。

---

## 心得

- **核心技巧**：利用栈实现“最近元素删除”。  
- **适用题型**：  
  1. **括号匹配**（如 LeetCode 20 Valid Parentheses）  
  2. **删除相邻相同字符**（如 LeetCode 1047 Remove All Adjacent Duplicates In String）  
  3. **单调栈求最近更大/更小元素**（如 LeetCode 496 Next Greater Element I）  
- **解题钥匙**：**“左侧最近、未被处理的字符 → 栈顶”**，遇到需要“撤销”或“配对”的操作时，第一反应就是考虑栈。

---

## 反思

- **第一反应**：看到星号会把左边的字符删掉，想到“一遍遍扫描、每次删掉”——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略了星号可能连续出现，导致一次弹栈不够，需要对每个 `*` 都弹一次。  
  - 边界情况：全是星号的字符串，最终答案为空字符串，代码要能正确返回 `""`。  
- **下次类似题的第一步**：**识别“最近元素被删除/配对”**的模式，立刻想到 **栈**（或者双指针）来做到 `O(1)` 的最近元素获取。