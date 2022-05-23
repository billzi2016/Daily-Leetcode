# #1790. 检查一次字符交换是否能使字符串相等 / Check if One String Swap Can Make Strings Equal

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/check-if-one-string-swap-can-make-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given two strings s1 and s2 of equal length. A string swap is an operation where you choose two indices in a string (not necessarily different) and swap the characters at these indices.
Return true if it is possible to make both strings equal by performing at most one string swap on exactly one of the strings. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: s1 = "bank", s2 = "kanb"
Output: true
Explanation: For example, swap the first character with the last character of s2 to make "bank".
```

**Example 2:**

```
Input: s1 = "attack", s2 = "defend"
Output: false
Explanation: It is impossible to make them equal with one string swap.
```

**Example 3:**

```
Input: s1 = "kelb", s2 = "kelb"
Output: true
Explanation: The two strings are already equal, so no string swap operation is required.
```

**Constraints**

- 1 <= s1.length, s2.length <= 100
- s1.length == s2.length
- s1 and s2 consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个等长的字符串 `s1` 和 `s2`。**字符串交换（string swap）**是一种操作，即在一个字符串中选择两个下标（可以相同），并交换这两个下标处的字符。

如果可以通过对其中一个字符串最多进行一次 **字符串交换（string swap）** 使得两个字符串相等，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入:** `s1 = "bank", s2 = "kanb"`  
**输出:** `true`  
**解释:** 例如，对 `s2` 的第一个字符和最后一个字符进行交换，可得到 `"bank"`。

### 示例 2
**输入:** `s1 = "attack", s2 = "defend"`  
**输出:** `false`  
**解释:** 无法仅通过一次字符串交换使它们相等。

### 示例 3
**输入:** `s1 = "kelb", s2 = "kelb"`  
**输出:** `true`  
**解释:** 两个字符串已经相等，不需要进行任何字符串交换操作。

## 约束条件

- `1 <= s1.length, s2.length <= 100`
- `s1.length == s2.length`
- `s1` 和 `s2` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的交换都试一遍**，只要出现一次能够让两串相等，就返回 `True`，否则返回 `False`。

- **数据结构**：我们只需要遍历字符串，最常用的结构是 **列表**（因为列表可以原地修改字符），可以把 `s2` 转成列表后进行交换。
- **生活化类比**：把字符串想象成一排排的字母卡片，暴力解相当于把每两张卡片（包括同一张卡片自己和自己交换）都尝试换位，看能否把两排卡片排成完全一样的样子。
- **正确性**：因为我们枚举了 **所有** 可能的（包括不交换的情况），只要有一种能够使 `s1` 与 `s2` 完全相同，就一定会在遍历过程中被发现。
- **时间/空间复杂度**：  
  - 外层遍历 `i`（长度 `n`），内层遍历 `j`（长度 `n`），所以总共要检查 `n × n` 次。用大白话说，就是如果字符串有 10 个字符，就要尝试 100 次；字符多了，次数就会呈 **平方增长**，记作 **O(n²)**。  
  - 我们只使用了一个长度为 `n` 的字符列表来临时交换，空间开销随输入线性增长，记作 **O(n)**。

#### 代码（Python）

```python
def are_equal_by_one_swap_bruteforce(s1: str, s2: str) -> bool:
    # 长度相等是题目保证，这里不再检查
    n = len(s1)
    # 直接把 s2 转成列表，方便原地交换字符
    s2_list = list(s2)

    # 第一次检查：不做任何交换的情况
    if s1 == s2:
        return True

    # 枚举所有 i、j（可以相同）的位置进行一次交换
    for i in range(n):
        for j in range(n):
            # 交换前先把字符换回来，防止上一次循环留下痕迹
            s2_list = list(s2)          # 重新拷贝一次，保持 O(1) 代码可读性
            s2_list[i], s2_list[j] = s2_list[j], s2_list[i]  # 交换

            # 检查交换后是否相等
            if ''.join(s2_list) == s1:
                return True
    # 所有可能都尝试完了，仍未相等
    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：如果字符串长度是 `n`，我们要尝试 `n` × `n` 次交换，每次比较两个字符串的相等性也是 `O(n)`，但在 Python 中 `==` 已经做了优化，这里只计遍历次数即可，整体仍是平方级别。
- **空间复杂度**：`O(n)`  
  - 解释：我们需要额外的字符列表保存 `s2`，列表的大小正好是字符串的长度 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈**在于我们把所有位置的组合都枚举了一遍，而实际上只需要关注 **两串不同的字符所在的位置**。

1. **先找出不相等的下标**  
   - 逐位比较 `s1[i]` 与 `s2[i]`，把不相等的下标记录下来。  
   - 如果不相等的下标数量不是 **0** 或 **2**，说明不可能只通过一次交换就相等（因为一次交换最多只能影响两个位置）。

2. **0 个不相等**  
   - 两串本来就相等，直接返回 `True`（不需要交换）。

3. **恰好 2 个不相等**  
   - 设这两个下标为 `i`、`j`，则要想通过一次交换让两串相等，需要满足：  
     ```
     s1[i] == s2[j]  且  s1[j] == s2[i]
     ```  
   - 这相当于把 `s2` 中的两个字符调换后，恰好对应 `s1` 的字符。  
   - 用生活化的类比：我们在两条相同长度的字母链上只发现了两块颜色不对的拼图，只要把这两块互换，就能拼成完全一样的图案。

4. **其它情况**（不等于 0、2）直接返回 `False`。

**核心数据结构**：这里只用到了 **列表**（或直接使用字符串索引）来遍历，**不需要哈希表**。如果想更形象地解释哈希表的作用，可类比为“字典”，但本题不必使用。

#### 代码（Python）

```python
def are_equal_by_one_swap(s1: str, s2: str) -> bool:
    """
    判断是否只通过一次字符交换（可以在任意一个字符串里）就能让两串相等。
    思路：只关注不相等的下标，数量必须是 0 或 2。
    """
    # 记录不相等的下标
    diff = []                       # diff 类似“不同的地方清单”

    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            diff.append(i)          # 把位置 i 加进清单
            # 提前剪枝：如果已经超过 2 个不同位置，直接返回 False
            if len(diff) > 2:
                return False

    # 情况 1：完全相同
    if not diff:                     # diff 为空列表，相当于 len(diff) == 0
        return True

    # 情况 2：恰好两个不同位置
    if len(diff) == 2:
        i, j = diff[0], diff[1]
        # 检查交叉相等条件
        return s1[i] == s2[j] and s1[j] == s2[i]

    # 其它情况（只有 1 个不同位置）不可能只用一次交换解决
    return False
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：我们只遍历一次字符串（长度为 `n`），每一步只做常数时间的比较和列表操作。相比暴力的 `O(n²)`，这里是线性增长，字符多了，耗时也只会线性增长。
- **空间复杂度**：`O(1)`（不计返回值）  
  - 解释：我们只用了一个长度最多为 2 的列表 `diff`，占用的空间与输入规模无关，视作常数空间。

---

## 心得

- **核心技巧**：**只关注不相等的位置并利用交叉匹配**。一次交换只能影响两个字符，所以不相等的地方必须恰好是 0（已相等）或 2（正好可以通过交换修复）。
- **适用的题型**  
  1. *“检查能否通过一次交换使数组相等”*（如 LeetCode 1650）  
  2. *“检查两个字符串是否只差一个字符位置的置换”*（如 变位词的特殊版）  
  3. *“判断是否只需一次修改即可使两个序列相同”*（如一次翻转、一次翻转子数组等）
- **一句话总结**：**一次交换只能纠正恰好两处错误，先定位错误再交叉匹配即可**。

---

## 反思

- **第一反应**：看到“最多一次交换”，自然会想到“枚举所有可能的交换”。这导致了暴力解的出现。
- **最容易踩的坑**  
  1. **忘记** “不需要交换也算成功”。如果两串本来相等，答案应为 `True`。  
  2. **误判** 只有 1 个不相等位置时仍返回 `True`（实际上无法通过一次交换解决）。  
  3. **边界条件**：字符串长度为 1 时，只会出现 0 或 1 个不同位置，需要正确处理。
- **下次遇到同类题的第一步**：**先统计不相等的下标数量**，根据数量判断是否还有可能在限定次数的操作内完成。这样可以立即排除大多数不可能的情况，避免不必要的枚举。