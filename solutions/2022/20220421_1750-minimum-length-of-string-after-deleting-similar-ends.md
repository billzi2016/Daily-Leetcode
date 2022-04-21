# #1750. 删除相同两端字符后的字符串最小长度 / Minimum Length of String After Deleting Similar Ends

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/minimum-length-of-string-after-deleting-similar-ends/)

---

## 题目（英文原版）

**Description**

Given a string s consisting only of characters 'a', 'b', and 'c'. You are asked to apply the following algorithm on the string any number of times:
Return the minimum length of s after performing the above operation any number of times (possibly zero times).

**Examples**

**Example 1:**

```
Input: s = "ca"
Output: 2
Explanation: You can't remove any characters, so the string stays as is.
```

**Example 2:**

```
Input: s = "cabaabac"
Output: 0
Explanation: An optimal sequence of operations is:
- Take prefix = "c" and suffix = "c" and remove them, s = "abaaba".
- Take prefix = "a" and suffix = "a" and remove them, s = "baab".
- Take prefix = "b" and suffix = "b" and remove them, s = "aa".
- Take prefix = "a" and suffix = "a" and remove them, s = "".
```

**Example 3:**

```
Input: s = "aabccabba"
Output: 3
Explanation: An optimal sequence of operations is:
- Take prefix = "aa" and suffix = "a" and remove them, s = "bccabb".
- Take prefix = "b" and suffix = "bb" and remove them, s = "cca".
```

**Constraints**

- 1 <= s.length <= 105
- s only consists of characters 'a', 'b', and 'c'.

---

## 题目（中文翻译）

**题目描述**

给定一个仅由字符 `'a'`、`'b'`、`'c'` 组成的字符串 `s`。你可以对字符串执行以下操作任意次（可以为零次）：

1. 选择一个非空的前缀（prefix），要求前缀中的所有字符相同，记为字符 `ch`；
2. 选择一个非空的后缀（suffix），要求后缀中的所有字符也相同且字符为同一个 `ch`；
3. 同时删除这两个前缀和后缀。

返回在上述操作任意次数后，字符串 `s` 可能得到的最小长度。

**示例**

> 示例 1  
> 输入: `s = "ca"`  
> 输出: `2`  
> 解释: 你无法删除任何字符，字符串保持不变。

> 示例 2  
> 输入: `s = "cabaabac"`  
> 输出: `0`  
> 解释: 一种最优的操作序列如下:  
> - 取前缀 `"c"` 与后缀 `"c"` 删除，得到 `s = "abaaba"`。  
> - 取前缀 `"a"` 与后缀 `"a"` 删除，得到 `s = "baab"`。  
> - 取前缀 `"b"` 与后缀 `"b"` 删除，得到 `s = "aa"`。  
> - 取前缀 `"a"` 与后缀 `"a"` 删除，得到 `s = ""`（空串），长度为 `0`。

> 示例 3  
> 输入: `s = "aabccabba"`  
> 输出: `3`  
> 解释: 一种最优的操作序列如下:  
> - 取前缀 `"aa"` 与后缀 `"a"` 删除，得到 `s = "bccabb"`。  
> - 取前缀 `"b"` 与后缀 `"bb"` 删除，得到 `s = "cca"`。  
> 此时无法再进行合法的删除，剩余字符串长度为 `3`。

**约束条件**

- `1 <= s.length <= 10^5`
- `s` 只由字符 `'a'`、`'b'`、`'c'` 组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**不停地在字符串两端找相同的字符并把它们全部删掉**。  
具体步骤可以这样描述：

1. 从左边找出一段连续相同的字符（比如全部是 `'a'`），记作 `prefix`。  
2. 从右边找出一段连续相同的字符（比如全部是 `'a'`），记作 `suffix`。  
3. 如果 `prefix` 与 `suffix` 使用的字符相同（比如都是 `'a'`），就把这两段全部删掉，得到一个更短的字符串。  
4. 对得到的新字符串重复步骤 1~3，直到两端的字符不相同或字符串为空。

> **类比**：把字符串想象成一本书的书页，左端的连续相同字符就像书的前几页都是同一本章节的标题，右端的连续相同字符也是同样的标题。如果两端的标题相同，就把这几页全部撕掉；否则就不能再撕。

这种做法一定能得到合法的结果，因为每一步都遵守题目规定的“取相同字符的前缀和后缀并删除”。只要一直循环下去，最终要么删到空串，要么两端字符不同，无法再操作。

**为什么会慢**  
在每一次循环里，我们都要**遍历**整段字符串来找前缀和后缀，这会导致**重复扫描**已经被检查过的字符。例如字符串 `"aaaaabaaaaa"`，我们可能在第一轮扫描了左边的 5 个 `'a'`，右边的 5 个 `'a'`，随后又要在第二轮重新从头开始扫描，导致总体时间呈二次增长。

#### 代码（Python）

```python
def minLength_bruteforce(s: str) -> int:
    # 只要还能删，就一直循环
    while True:
        n = len(s)
        if n == 0:                     # 空串直接返回 0
            return 0

        # 找左端连续相同字符的长度
        left = 0
        while left < n and s[left] == s[0]:
            left += 1

        # 找右端连续相同字符的长度
        right = 0
        while right < n and s[n - 1 - right] == s[-1]:
            right += 1

        # 两端字符相同且长度都大于 0，才能删
        if left > 0 and right > 0 and s[0] == s[-1]:
            # 删除左端和右端（注意可能会出现 left+right > n 的情况）
            cut = min(left, right)          # 只能删掉两端都存在的那部分
            s = s[cut:n - cut]              # 重新构造剩余的子串
        else:
            # 不能再删除，返回当前长度
            return len(s)
```

#### 复杂度

- **时间复杂度：**`O(n²)`  
  解释：最坏情况下，每一次循环都要遍历整个字符串（`O(n)`），而循环的次数也可能是 `O(n)`（比如每次只删掉 1 个字符），于是总共是 `n × n`，即二次方。  
- **空间复杂度：**`O(1)`（不计返回值）  
  只使用了常数个指针变量，没有额外的随输入规模增长的存储。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于每次都从头遍历整段字符串。实际上，我们只需要 **一次遍历** 就能把所有可以删掉的字符跳过去。  

观察题目提示：

> 如果两端字符不同，操作结束；否则，只能把两端**相同字符的全部**删除。

这意味着：  
- 当左端字符 `s[l]` 与右端字符 `s[r]` 相等时，**左边所有连续的 `s[l]` 必然会被删掉**，右边所有连续的 `s[r]` 也会被删掉。  
- 删除后，指针直接跳到下一个不相同的字符位置继续判断即可。

于是我们可以用 **双指针**（两个指针分别指向左、右）一次遍历完成：

1. 初始化 `l = 0, r = len(s) - 1`。  
2. 当 `l < r` 且 `s[l] == s[r]` 时：  
   - 记下当前字符 `c = s[l]`。  
   - 把左指针向右移动，跳过所有连续的 `c`（`while l <= r and s[l] == c: l += 1`）。  
   - 把右指针向左移动，跳过所有连续的 `c`（`while l <= r and s[r] == c: r -= 1`）。  
3. 循环结束后，`l` 与 `r` 之间剩下的子串（如果有）就是 **再也无法删除的部分**，其长度即为答案。

> **类比**：把字符串想象成一根绳子，两个人站在两端，只有当两端手里拿的颜色相同（比如都是红色）时，两个人才能一起把手里所有相同颜色的绳段一起剪掉。剪完后，两人继续往中间走，检查新的颜色是否相同，直到颜色不同为止。

#### 代码（Python）

```python
def minLength(s: str) -> int:
    l, r = 0, len(s) - 1          # 左右指针初始指向字符串两端

    while l < r and s[l] == s[r]:
        cur = s[l]                # 当前两端相同的字符

        # 左指针跳过所有连续的 cur
        while l <= r and s[l] == cur:
            l += 1

        # 右指针跳过所有连续的 cur
        while l <= r and s[r] == cur:
            r -= 1

    # 循环结束，l..r（含）之间的字符无法再被删除
    return r - l + 1 if l <= r else 0
```

#### 复杂度

- **时间复杂度：**`O(n)`  
  解释：每个字符最多被左指针或右指针访问一次，整个过程只做一次线性扫描。相比暴力的二次方，这就是“快了一倍”，在 10⁵ 长度的限制下完全可以接受。  
- **空间复杂度：**`O(1)`  
  只用了几个整数指针，没有额外随输入增长的存储。

---

## 心得

- **核心技巧**：双指针一次遍历，利用“相同字符两端全部删除”这一规则，跳过连续相同的块。  
- **适用题型**  
  1. “删除相同字符的前后缀”类题（如 LeetCode 1750 `Minimum Length of String After Deleting Similar Ends`）。  
  2. 两端匹配删除或收缩的字符串题（如 “删除回文子串” 变形）。  
  3. 需要一次遍历解决的“左右收敛”问题（如 “判断回文” 的双指针实现）。  
- **一句话总结**：只要两端字符相同，就一次性把两端所有相同字符都剔除，循环即可得到最短长度。

---

## 反思

- **第一反应**：看到“从两端删相同字符”，立刻想到“循环检查两端是否相同”。  
- **最容易踩的坑**  
  - **边界条件**：当字符串只剩一个字符或已经空时，需要直接返回长度（1 或 0），否则指针移动会越界。  
  - **删除长度不等**：左端和右端相同字符的数量可能不同，但题目要求删除**两端全部**相同字符，所以要把左、右各自的连续块全部跳过，而不是只删掉较短的那一边。  
  - **指针交叉**：在跳过字符时要检查 `l <= r`，防止指针已经相遇或交叉导致无限循环。  
- **下次遇到同类题**：第一步就想到“用双指针从两端向中间收敛”，并在相等时一次性跳过连续相同块，这样可以把时间复杂度直接压到 `O(n)`。