# #2299. 强密码检查器 II / Strong Password Checker II

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/strong-password-checker-ii/)

---

## 题目（英文原版）

**Description**

A password is said to be strong if it satisfies all the following criteria:
Given a string password, return true if it is a strong password. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: password = "IloveLe3tcode!"
Output: true
Explanation: The password meets all the requirements. Therefore, we return true.
```

**Example 2:**

```
Input: password = "Me+You--IsMyDream"
Output: false
Explanation: The password does not contain a digit and also contains 2 of the same character in adjacent positions. Therefore, we return false.
```

**Example 3:**

```
Input: password = "1aB!"
Output: false
Explanation: The password does not meet the length requirement. Therefore, we return false.
```

**Constraints**

- 1 <= password.length <= 100
- password consists of letters, digits, and special characters: "!@#$%^&*()-+".

---

## 题目（中文翻译）

一个密码被认为是强密码，需要满足以下所有条件：

- 长度至少为 **8**。
- 至少包含一个小写字母（lowercase letter）。
- 至少包含一个大写字母（uppercase letter）。
- 至少包含一个数字（digit）。
- 至少包含一个特殊字符（special character），特殊字符集合为 `!@#$%^&*()-+`。
- 任意两个相邻字符**不能相同**。

给定一个字符串 `password`，如果它是强密码则返回 `true`，否则返回 `false`。

### 示例

#### 示例 1
**输入**  
``` 
password = "IloveLe3tcode!"
```  
**输出**  
```
true
```  
**解释**  
该密码满足所有要求，因此返回 `true`。

#### 示例 2
**输入**  
``` 
password = "Me+You--IsMyDream"
```  
**输出**  
```
false
```  
**解释**  
密码中不包含数字（digit），且存在两个相同字符在相邻位置（`--`），因此返回 `false`。

#### 示例 3
**输入**  
``` 
password = "1aB!"
```  
**输出**  
```
false
```  
**解释**  
密码长度未达到 8 位的要求，所以返回 `false`。

### 约束条件
- `1 <= password.length <= 100`
- `password` 仅由字母、数字以及特殊字符 `!@#$%^&*()-+` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把密码的每一条规则都 **逐条检查**，只要有一条不满足就返回 `False`，全部满足才返回 `True`。  
我们需要检查的内容有四个：

1. **长度**：密码长度必须 ≥ 8。  
2. **字符种类**：必须同时出现 **小写字母**、**大写字母**、**数字**、**特殊字符**（`!@#$%^&*()-+`）。  
3. **相邻字符**：密码里**不能出现两个相同的字符**相邻。  
4. **字符范围**：题目已经保证只会出现字母、数字和上述特殊字符，所以这里不必再额外判断。

实现时可以使用 **四个布尔变量**（`has_lower`, `has_upper`, `has_digit`, `has_special`）来记录是否已经看到对应的字符，就像在查字典时把「词」当作 `key`、出现次数当作 `value`，只不过这里的「value」是布尔值。遍历字符串一次，就能把四类信息全部收集完。

为什么这种做法一定正确？因为我们没有对密码做任何「修改」或「猜测」，只是在**原样检查**每一条要求。只要所有要求都满足，答案必然是 `True`；只要有一条不满足，答案必然是 `False`。

**时间/空间复杂度**  
- **时间复杂度**：我们只遍历一次字符串，时间随密码长度线性增长，用大写的 **O(n)** 表示（n 是密码的字符数）。可以把它想象成「每增加一个字符，就多检查一次」。
- **空间复杂度**：只用了常数个布尔变量和一个常量长度的特殊字符集合，用 **O(1)** 表示（不随 n 增长）。

#### 代码（Python）

```python
def strongPasswordCheckerII(password: str) -> bool:
    # 1. 长度检查
    if len(password) < 8:
        return False

    # 2. 初始化四个标记，分别记录是否出现过小写、大写、数字、特殊字符
    has_lower = has_upper = has_digit = has_special = False

    # 3. 把合法的特殊字符放进集合，集合查询像查字典一样 O(1)
    specials = set('!@#$%^&*()-+')

    # 4. 遍历每个字符，同时检查相邻字符是否相同
    for i, ch in enumerate(password):
        # 检查相邻字符是否相同
        if i > 0 and ch == password[i - 1]:
            return False   # 只要发现相邻相同立刻返回 False

        # 根据字符的 Unicode 范围更新对应的标记
        if 'a' <= ch <= 'z':
            has_lower = True
        elif 'A' <= ch <= 'Z':
            has_upper = True
        elif '0' <= ch <= '9':
            has_digit = True
        elif ch in specials:
            has_special = True
        # 题目保证字符只能是上述四类，所以这里不需要 else

    # 5. 最后检查四个标记是否全为 True
    return has_lower and has_upper and has_digit and has_special
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着密码长度 n 增长，检查次数线性增加。  
- **空间复杂度**：`O(1)` — 只用了常数个变量和一个固定大小的集合。

---

### 2. 最优解

#### 思路  

在本题中，**暴力解已经是最优解**，因为我们只能对每个字符做一次检查，无法再把时间降低到 `O(log n)` 或 `O(1)`（必须看完整个密码才能判断是否满足所有条件）。  
不过可以把「暴力」的实现写得更**简洁、易读**，并强调**一次遍历**的思想，这也是本题的核心优化点：

- **瓶颈**：如果把每条规则分别写成多个循环，会导致多次遍历同一个字符串，时间会变成 `O(4n) ≈ O(n)`，虽然在大 O 记号里仍是线性，但实际常数更大。一次遍历即可把所有信息收集完，最省时。
- **优化**：把所有检查合并到同一个 `for` 循环里，利用 **布尔变量 + 集合** 完成所有标记。这样代码既快又简洁。

下面给出更「最优」的实现（与上面的思路相同，只是代码更紧凑）。

#### 代码（Python）

```python
def strongPasswordCheckerII(password: str) -> bool:
    # 长度必须 ≥ 8
    if len(password) < 8:
        return False

    specials = set('!@#$%^&*()-+')          # 特殊字符集合，查询快
    has_lower = has_upper = has_digit = has_special = False

    for i, ch in enumerate(password):
        # 相邻字符相同直接返回 False
        if i > 0 and ch == password[i - 1]:
            return False

        # 更新四类标记
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in specials:
            has_special = True
        # 其他字符不会出现（题目已限定）

    # 四个标记全为 True 才算强密码
    return has_lower and has_upper and has_digit and has_special
```

> **小技巧**：`str.islower()`、`str.isupper()`、`str.isdigit()` 是 Python 内置的字符分类函数，使用它们可以让代码更直观。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串。与暴力解的时间相同，但常数更小，因为没有额外的循环或重复检查。
- **空间复杂度**：`O(1)` — 只用了固定数量的变量和一个大小固定的集合。

---

## 心得

- **核心技巧**：一次遍历（**单遍扫描**）结合**布尔标记**和**集合查询**，在检查多条规则时既不遗漏也不重复工作。
- **适用的题型**  
  1. **密码强度检查**（本题）  
  2. **字符串合法性校验**（如检查是否只含字母数字下划线）  
  3. **字符分类统计**（如统计字符串中出现的不同字符种类）  
- **一句话总结解题钥匙**：  
  > “把所有条件的检查压缩到一次遍历，用布尔变量记录出现情况，遇到违规立即返回”。  

---

## 反思

- **第一反应**：看到“长度、四类字符、相邻相同”这几个条件，马上想到遍历字符串并用标记记录。
- **最容易踩的坑**  
  - **相邻相同的判断**：容易忘记在遍历时把当前字符和前一个字符比较。  
  - **特殊字符集合**：如果手写判断条件容易遗漏或写错，使用集合或字符串 `in` 检查更安全。  
  - **长度边界**：密码长度恰好是 8 时仍然合法，需要使用 `>= 8` 而不是 `> 8`。  
- **下次遇到同类题的第一步**：  
  > “先把所有约束列成清单，判断哪些可以在同一次遍历中完成，并准备好对应的标记或集合”。