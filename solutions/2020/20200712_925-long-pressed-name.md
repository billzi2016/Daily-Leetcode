# #925. 长按键名 / Long Pressed Name

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/long-pressed-name/)

---

## 题目（英文原版）

**Description**

Your friend is typing his name into a keyboard. Sometimes, when typing a character c, the key might get long pressed, and the character will be typed 1 or more times.
You examine the typed characters of the keyboard. Return True if it is possible that it was your friends name, with some characters (possibly none) being long pressed.

**Examples**

**Example 1:**

```
Input: name = "alex", typed = "aaleex"
Output: true
Explanation: 'a' and 'e' in 'alex' were long pressed.
```

**Example 2:**

```
Input: name = "saeed", typed = "ssaaedd"
Output: false
Explanation: 'e' must have been pressed twice, but it was not in the typed output.
```

**Constraints**

- 1 <= name.length, typed.length <= 1000
- name and typed consist of only lowercase English letters.

---

## 题目（中文翻译）

你的朋友正在键盘上输入他的名字。有时，当输入一个字符 **c** 时，键会被长按，导致该字符会被输入 **1** 次或多次。  
给定键盘上实际输入的字符序列 **typed**，如果它有可能是朋友的名字 **name**，且其中的某些字符（也可能没有）是被长按产生的，则返回 `True`。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= name.length, typed.length <= 1000`
- `name` 和 `typed` 仅由小写英文字母组成。

### 示例

**示例 1**  
```
Input: name = "alex", typed = "aaleex"
Output: true
Explanation: 'a' 和 'e' 在 "alex" 中被长按。
```

**示例 2**  
```
Input: name = "saeed", typed = "ssaaedd"
Output: false
Explanation: 'e' 必须被按两次，但在输出的 typed 中并没有出现两次。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **name** 的每个字符都和 **typed** 的字符逐一对应，检查是否满足「按键可能被长按」的规则。  
我们可以把 **typed** 当成「原始字符序列」+「每个字符的额外重复」：

1. 从左到右遍历 **name**，对每个字符 `c`，在 **typed** 中找出连续出现的 `c` 的区间（可能只有 1 次，也可能多次）。  
2. 检查 **typed** 中对应的这段字符是否 **至少** 包含了 **name** 中的这一个 `c`（即出现次数 ≥ 1）。  
3. 若出现次数满足，继续检查下一个字符；否则返回 `False`。  

> **类比**：把 **typed** 想象成一本字典，里面记录了每个字母出现的「页码」——我们只需要确保每个字母在字典里出现的次数不小于原本应该出现的次数。

**为什么正确**：  
- 如果 **typed** 能够由 **name** 通过「某些字符被长按」得到，那么每个 **name** 中的字符在 **typed** 中出现的次数一定 **不小于** 1，且必须保持顺序不变。  
- 反之，如果我们在 **typed** 中找到的对应字符次数都满足 ≥1 且顺序一致，那么必然可以把多余的重复解释为长按。

**时间/空间分析**：  
- 我们对 **name** 的每个字符都要在 **typed** 中扫描一次，最坏情况下会遍历 **typed** 的全部字符（长度记为 `m`），因此时间复杂度是 `O(m)`。  
- 只使用了几个指针变量，额外空间为 `O(1)`（常数级）。

> **大白话**：`O(m)` 就像说「最多要看一遍 typed」；`O(1)` 就是「只需要几根手指指着位置，不需要额外的大箱子装东西」。

#### 代码（Python）

```python
def isLongPressedName(name: str, typed: str) -> bool:
    i, j = 0, 0               # i 指向 name，j 指向 typed
    while i < len(name) and j < len(typed):
        if name[i] == typed[j]:          # 同字符，正常匹配
            i += 1
            j += 1
        elif j > 0 and typed[j] == typed[j - 1]:
            # 当前 typed 的字符和它左边的字符相同，说明是长按产生的冗余字符
            j += 1
        else:
            # 不匹配且不是长按的冗余字符，直接失败
            return False

    # 检查 name 是否已经全部匹配完
    if i != len(name):
        return False

    # typed 可能还有剩余的长按字符，需要全部是前一个字符的重复
    while j < len(typed):
        if typed[j] != typed[j - 1]:
            return False
        j += 1

    return True
```

- `i, j` 分别是 **name**、**typed** 的指针。  
- 当两个字符相等时，两个指针都向前走。  
- 当不相等时，若 `typed[j]` 与它左边的字符相同，说明是「长按」产生的额外字符，只让 `j` 前进。  
- 其他情况直接返回 `False`。

#### 复杂度

- **时间复杂度**：`O(m)`（`m = len(typed)`）——最多遍历一次 `typed`。  
- **空间复杂度**：`O(1)`——只用了常数个变量。

---

### 2. 最优解

#### 思路  

其实上面的「暴力」已经是最优的线性时间解法，只是我们可以用更简洁的 **双指针** 思路一步到位，避免额外的「遍历完后再检查」过程。  

**瓶颈**：  
- 在暴力思路里，我们先把两串对齐，再在结尾处做一次额外的检查。  
- 如果在遍历过程中就能判断所有情况，就可以更直接、更易懂。

**优化步骤**  

1. 同时用两个指针 `i`（指向 `name`）和 `j`（指向 `typed`）。  
2. 当 `name[i] == typed[j]` 时，说明这是一段合法匹配，两个指针都向前走。  
3. 当不相等时，只要 `typed[j]` 与前一个字符相同（`typed[j] == typed[j-1]`），就把它视作长按的冗余字符，**只让 `j` 前进**。  
4. 只要出现「不相等且不是冗余字符」的情况，立即返回 `False`。  
5. 循环结束后，若 `i` 已经走完 `name`（`i == len(name)`），则说明所有字符都得到匹配。此时 `typed` 可能还有剩余字符，只要这些剩余字符全是前一个字符的重复即可（这一步在循环内部已经隐含处理，因为只要出现不等就会提前返回）。

这样，整个过程只需一次遍历，代码更紧凑。

**核心数据结构**：**双指针**。  
- **双指针** 就像两个人手拉手在两条不同的路上走，一起比较当前看到的东西是否相同，必要时让其中一个人快一点，另一个保持原位。

#### 代码（Python）

```python
def isLongPressedName(name: str, typed: str) -> bool:
    i = j = 0                     # 同时从两串的开头出发

    while j < len(typed):
        # 情况 1：字符相等，正常匹配，两指针都前进
        if i < len(name) and name[i] == typed[j]:
            i += 1
            j += 1
        # 情况 2：当前 typed 的字符是前一个字符的重复（长按），只让 j 前进
        elif j > 0 and typed[j] == typed[j - 1]:
            j += 1
        else:
            # 既不匹配，也不是长按产生的冗余字符，直接失败
            return False

    # 循环结束后，只有 i 必须走完 name，j 已经遍历完 typed
    return i == len(name)
```

- `i < len(name)` 的检查防止指针越界。  
- `j > 0 and typed[j] == typed[j-1]` 捕捉「长按」的冗余字符。  
- 最后只要 `i` 正好等于 `len(name)`，说明所有原字符都匹配成功。

#### 复杂度

- **时间复杂度**：`O(m)`（`m = len(typed)`），只遍历一次 `typed`。  
  > 与前面的暴力解相比，省去了结尾的二次遍历，真正做到“一次遍历搞定”。  
- **空间复杂度**：`O(1)`，只用了几个整数指针。

---

## 心得

- **核心技巧**：**双指针** 在两个有序序列（这里是字符串）上同步比较，并利用「当前字符等于前一个字符」的特性识别冗余（长按）字符。  
- **适用题型**：  
  1. 判断两个字符串是否为「同构」或「变形」关系（如 *Backspace String Compare*）。  
  2. 判断两个有序数组是否相同，允许出现重复元素（如 *Remove Duplicates from Sorted Array* 的变体）。  
- **一句话总结**：只要把「长按」看成「前一个字符的额外复制」，用双指针同步扫描即可轻松验证。

---

## 反思

- **第一反应**：把 `typed` 当成 `name` 的每个字符后面加上一堆重复的「长按」字符，想把两串逐个对应比较。  
- **最容易踩的坑**：  
  - 忘记检查 `typed` 末尾可能还有的长按字符。  
  - 当 `name` 已经遍历完，但 `typed` 仍有字符时，需要确保这些字符全是前一个字符的重复，否则应该返回 `False`。  
  - 边界条件，如 `name` 长度为 1，或 `typed` 与 `name` 完全相同（没有长按）时也要返回 `True`。  
- **下次遇到同类题**：第一步先想到「双指针」同步遍历，同时利用「当前字符等于前一个字符」来捕获冗余或多余的元素。这样可以在一次遍历中完成判断，避免额外的后处理。