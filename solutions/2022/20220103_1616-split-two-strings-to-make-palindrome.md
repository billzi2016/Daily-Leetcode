# #1616. 拆分两个字符串构成回文 / Split Two Strings to Make Palindrome

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/split-two-strings-to-make-palindrome/)

---

## 题目（英文原版）

**Description**

You are given two strings a and b of the same length. Choose an index and split both strings at the same index, splitting a into two strings: aprefix and asuffix where a = aprefix + asuffix, and splitting b into two strings: bprefix and bsuffix where b = bprefix + bsuffix. Check if aprefix + bsuffix or bprefix + asuffix forms a palindrome.
When you split a string s into sprefix and ssuffix, either ssuffix or sprefix is allowed to be empty. For example, if s = "abc", then "" + "abc", "a" + "bc", "ab" + "c" , and "abc" + "" are valid splits.
Return true if it is possible to form a palindrome string, otherwise return false.
Notice that x + y denotes the concatenation of strings x and y.

**Examples**

**Example 1:**

```
Input: a = "x", b = "y"
Output: true
Explaination: If either a or b are palindromes the answer is true since you can split in the following way:
aprefix = "", asuffix = "x"
bprefix = "", bsuffix = "y"
Then, aprefix + bsuffix = "" + "y" = "y", which is a palindrome.
```

**Example 2:**

```
Input: a = "xbdef", b = "xecab"
Output: false
```

**Example 3:**

```
Input: a = "ulacfd", b = "jizalu"
Output: true
Explaination: Split them at index 3:
aprefix = "ula", asuffix = "cfd"
bprefix = "jiz", bsuffix = "alu"
Then, aprefix + bsuffix = "ula" + "alu" = "ulaalu", which is a palindrome.
```

**Constraints**

- 1 <= a.length, b.length <= 105
- a.length == b.length
- a and b consist of lowercase English letters

---

## 题目（中文翻译）

给定两个长度相同的字符串 **a** 和 **b**。选择一个下标（index），在同一位置将两个字符串同时拆分，得到：

- **a** 拆分为前缀 **aprefix** 和后缀 **asuffix**，满足 `a = aprefix + asuffix`  
- **b** 拆分为前缀 **bprefix** 和后缀 **bsuffix**，满足 `b = bprefix + bsuffix`

判断 **aprefix + bsuffix** 或 **bprefix + asuffix** 是否能够组成一个回文（palindrome）。

拆分字符串 **s** 为 **sprefix** 和 **ssuffix** 时，**sprefix** 或 **ssuffix** 可以为空。例如，若 `s = "abc"`，则以下拆分均合法：

- `"" + "abc"`
- `"a" + "bc"`
- `"ab" + "c"`
- `"abc" + ""`

如果能够形成回文字符串则返回 `true`，否则返回 `false`。  
注意，`x + y` 表示字符串 **x** 与 **y** 的拼接（concatenation）。

---

### 示例

**示例 1**  
```
Input: a = "x", b = "y"
Output: true
Explaination: If either a or b are palindromes the answer is true since you can split in the following way:
aprefix = "", asuffix = "x"
bprefix = "", bsuffix = "y"
Then, aprefix + bsuffix = "" + "y" = "y", which is a palindrome.
```
**解释**：只要 **a** 或 **b** 本身是回文，就可以通过把两者全部放在后缀（或前缀）的位置得到回文。因此答案为 `true`。

**示例 2**  
```
Input: a = "xbdef", b = "xecab"
Output: false
```

**示例 3**  
```
Input: a = "ulacfd", b = "jizalu"
Output: true
Explaination: Split them at index 3:
aprefix = "ula", asuffix = "cfd"
bprefix = "jiz", bsuffix = "alu"
Then, aprefix + bsuffix = "ula" + "alu" = "ulaalu", which is a palindrome.
```
**解释**：在下标 3 处拆分后，`aprefix + bsuffix = "ulaalu"`，该字符串是回文，所以返回 `true`。

---

### 约束条件

- `1 <= a.length, b.length <= 10^5`
- `a.length == b.length`
- `a` 和 `b` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的 **分割点** 都枚举一遍，然后把两种拼接方式逐一检查是否是回文。

- **分割点**：因为 `a` 与 `b` 长度相同，设长度为 `n`，我们可以在 `0 … n`（含 `0` 与 `n`）这 `n+1` 个位置把两串同时切开。  
  - 例如 `i = 3` 时，`a` 被切成 `aprefix = a[0:3]`、`asuffix = a[3:]`；`b` 同理。  
- **拼接方式**：有两种可能  
  1. `aprefix + bsuffix`  
  2. `bprefix + asuffix`  

对每一种拼接，判断得到的字符串是否是回文。判断回文只需要把字符串从左往右、右往左各走一遍，看对应字符是否相等。

> **类比**：把两个长条的拼图板分别在同一根线上切开，然后把左边的拼图板和右边的另一块拼图板拼在一起，看看能否拼出一面“镜子对称”的图案（回文）。

只要找到了一个满足条件的分割点，就可以返回 `True`；如果所有分割点都不行，返回 `False`。

#### 代码（Python）

```python
def check_palindrome(s: str) -> bool:
    """判断字符串 s 是否是回文（左右对应字符相同）"""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def splitTwoStrings_bruteforce(a: str, b: str) -> bool:
    n = len(a)
    # i 表示切分位置，范围是 0 ~ n（两端的空串也算合法切分）
    for i in range(n + 1):
        # 前缀 / 后缀
        aprefix, asuffix = a[:i], a[i:]
        bprefix, bsuffix = b[:i], b[i:]

        # 方式 1：aprefix + bsuffix
        if check_palindrome(aprefix + bsuffix):
            return True
        # 方式 2：bprefix + asuffix
        if check_palindrome(bprefix + asuffix):
            return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层枚举 `n+1` 个切分点，内层每次检查回文最坏要遍历整条拼接后的字符串（长度 `n`），所以大约是 `n * n` 次字符比较。  
  - **大白话**：如果 `n = 10⁵`，暴力解相当于要比较 `10⁵ × 10⁵ = 10¹⁰` 次字符，显然会超时。

- **空间复杂度**：`O(n)`  
  - 需要临时拼接两个子串生成新的字符串（最坏长度 `n`），以及递归栈（`check_palindrome` 用循环，不会额外占用栈空间）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要把整条字符串重新拼接并完整遍历**。  
观察题目可以发现，**只要从两端开始比较字符**，不匹配的地方一定是我们“切换”拼接的边界。  

设我们想要检查 `aprefix + bsuffix` 能否成为回文。把它写成两段：

```
a[0] a[1] … a[i-1] | b[i] b[i+1] … b[n-1]
```

从左端 (`a[0]`) 与右端 (`b[n-1]`) 开始比较：

- 如果 `a[left] == b[right]`，说明这对字符已经匹配，继续向里收敛 (`left += 1, right -= 1`)。
- 当出现不相等时，**只能把剩下的子串全交给同一原始字符串**，否则再换一次拼接会导致再次不匹配。  
  也就是说，出现第一次不匹配后，剩下的区间要么全部来自 `a`（检查 `a[left … right]` 是否本身是回文），要么全部来自 `b`（检查 `b[left … right]` 是否本身是回文）。

如果这两种检查任意一种成立，就可以在该不匹配位置“切换”拼接，得到回文。  
同理，还要检查另一种拼接方式 `bprefix + asuffix`，只需要把 `a`、`b` 的角色调换即可。

因此，只需要 **一次双指针遍历**（`O(n)`）并在第一次不匹配时做两次局部回文检查（每次最多遍历剩余区间），总体仍是线性时间。

> **类比**：把两根绳子分别从左、右两头往中间拉，如果一直能对应上颜色，那说明可以一直拼在一起；一旦颜色不对，就只能把后面的整段绳子换成单独的、自己能自洽的那根绳子（检查它自身是否是回文）。

#### 代码（Python）

```python
def is_pal_sub(s: str, l: int, r: int) -> bool:
    """检查 s[l:r+1]（闭区间）是否是回文，使用双指针"""
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True


def check_one_way(s1: str, s2: str) -> bool:
    """
    检查是否可以通过  s1 前缀 + s2 后缀  构造回文。
    这里 s1 对应 a，s2 对应 b（或相反）。
    """
    i, j = 0, len(s1) - 1
    # 从两端同时比较 s1[i] 与 s2[j]
    while i < j and s1[i] == s2[j]:
        i += 1
        j -= 1

    # 如果已经走完或只剩一个字符，必然是回文
    if i >= j:
        return True

    # 第一次不匹配后，有两种可能：
    # 1. 剩下的全部由 s1 组成（检查 s1[i..j] 是否回文）
    # 2. 剩下的全部由 s2 组成（检查 s2[i..j] 是否回文）
    return is_pal_sub(s1, i, j) or is_pal_sub(s2, i, j)


def splitTwoStrings_optimal(a: str, b: str) -> bool:
    """
    主函数：只要两种拼接方式任意一种可行，即返回 True。
    """
    return check_one_way(a, b) or check_one_way(b, a)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 主循环最多遍历一次完整的字符串长度 `n`（双指针收敛），  
  - 最多会在一次不匹配后再各检查一次子串的回文性，子串长度最多是 `n`，但这两次检查是 **互斥的**（只会执行其中一次），整体仍是线性级别。  
  - **对比**：相比暴力的 `n²`，我们把“每次都重新拼接检查”改成“一次遍历加一次局部检查”，快了几个数量级。

- **空间复杂度**：`O(1)`  
  - 只使用了若干整数指针，没有额外的与 `n` 成比例的容器。

---

## 心得

- **核心技巧**：**双指针 + 局部回文检查**。先把两串从外向内比较，冲突出现的第一点即是「只能换一次拼接」的切入口。  
- **适用的题型**  
  1. “拼接后回文” 类问题（如 LeetCode 1960 Split Two Strings to Make Palindrome）。  
  2. “只允许一次修改/删除后回文” 题目（如 680 Valid Palindrome II）。  
  3. “两个字符串交叉拼接检查回文” 的变形（如 1121. Divide Array Into Increasing Sequences 的思路相似——都利用一次扫描定位冲突点）。  

- **一句话总结**：  
  *“从两端同步比较，第一处不匹配决定只能把剩余部分交给同一字符串，检查它本身是否回文即可。”*

---

## 反思

- **第一反应**：直接遍历所有切分点（暴力），因为思路最直观。  
- **最容易踩的坑**  
  - 忽略空串的合法切分（`i = 0` 或 `i = n`）。  
  - 只检查 `aprefix + bsuffix`，忘记对称的 `bprefix + asuffix`。  
  - 在局部回文检查时使用 `s[i:j]`（左闭右开）导致漏掉最后一个字符；应使用闭区间或统一的切片方式。  
- **下次类似题目**，第一步应该：  
  *“用双指针从外向内比较两串对应字符，定位第一处冲突，再只在冲突区间做一次回文验证。”*