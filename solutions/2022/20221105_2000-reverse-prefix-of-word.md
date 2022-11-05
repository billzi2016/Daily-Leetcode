# #2000. 单词前缀翻转 / Reverse Prefix of Word

> 难度：简单 · 标签：Two Pointers、String、Stack · [LeetCode 链接](https://leetcode.com/problems/reverse-prefix-of-word/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed string word and a character ch, reverse the segment of word that starts at index 0 and ends at the index of the first occurrence of ch (inclusive). If the character ch does not exist in word, do nothing.
Return the resulting string.

**Examples**

**Example 1:**

```
Input: word = "abcdefd", ch = "d"
Output: "dcbaefd"
Explanation: The first occurrence of "d" is at index 3. 
Reverse the part of word from 0 to 3 (inclusive), the resulting string is "dcbaefd".
```

**Example 2:**

```
Input: word = "xyxzxe", ch = "z"
Output: "zxyxxe"
Explanation: The first and only occurrence of "z" is at index 3.
Reverse the part of word from 0 to 3 (inclusive), the resulting string is "zxyxxe".
```

**Example 3:**

```
Input: word = "abcd", ch = "z"
Output: "abcd"
Explanation: "z" does not exist in word.
You should not do any reverse operation, the resulting string is "abcd".
```

**Constraints**

- 1 <= word.length <= 250
- word consists of lowercase English letters.
- ch is a lowercase English letter.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串 **word** 和一个字符 **ch**，将 **word** 中从下标 **0** 开始、一直到 **ch** 第一次出现位置（**inclusive**，即包含该字符）的子串（segment）进行反转。如果字符 **ch** 在 **word** 中不存在，则不进行任何操作。  
返回得到的字符串。

**示例 1**  
**输入**: `word = "abcdefd", ch = "d"`  
**输出**: `"dcbaefd"`  
**解释**: 第一次出现的 `"d"` 位于下标 **3**。将下标 **0** 到 **3**（**inclusive**）的子串反转后，得到的字符串为 `"dcbaefd"`。

**示例 2**  
**输入**: `word = "xyxzxe", ch = "z"`  
**输出**: `"zxyxxe"`  
**解释**: `"z"` 唯一且第一次出现的位置是下标 **3**。将下标 **0** 到 **3**（**inclusive**）的子串反转后，得到的字符串为 `"zxyxxe"`。

**示例 3**  
**输入**: `word = "abcd", ch = "z"`  
**输出**: `"abcd"`  
**解释**: 字符 `"z"` 不存在于 **word** 中。无需进行任何反转操作，结果字符串仍为 `"abcd"`。

**约束条件**  
- $1 \leq \text{word.length} \leq 250$
- **word** 仅由小写英文字母组成。
- **ch** 为小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：

1. **先找** `ch` 在字符串 `word` 中第一次出现的位置 `idx`。这一步相当于在一本字典里翻页，找到某个单词所在的页码——我们只需要一次线性遍历。  
2. **如果找到了**（`idx != -1`），把 `word` 前 `idx+1` 个字符整体反转，然后把剩下的部分拼接回来。  
3. **如果没有找到**，直接返回原字符串。

这里用到的 **数据结构** 只有 Python 的 `str`（不可变的字符序列）和 `list`（可变的字符数组）。把字符串切片得到的子串相当于把整本书的前几页摘出来，再把这些页的顺序倒过来（这就是“反转”），最后再把后面的页码接上。

为什么这样一定能得到正确答案？

- 题目要求只**翻转**从下标 `0` 到第一次出现 `ch` 的位置（包括该位置）的这段子串。我们正好把这段子串取出来、倒序、再拼回去，完全符合要求。  
- 若 `ch` 不存在，题目说“什么都不做”，我们直接返回原字符串即可。

#### 代码（Python）

```python
def reversePrefix(word: str, ch: str) -> str:
    # 1. 找到 ch 第一次出现的下标，-1 表示不存在
    idx = -1
    for i, c in enumerate(word):
        if c == ch:          # 找到啦
            idx = i
            break

    # 2. 若不存在直接返回原串
    if idx == -1:
        return word

    # 3. 把前 idx+1 个字符切片、翻转，然后拼接后面的部分
    #   word[:idx+1] 取前缀，[::-1] 表示倒序
    reversed_part = word[:idx + 1][::-1]
    #   word[idx+1:] 取剩余的后缀
    return reversed_part + word[idx + 1:]
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们最多遍历一次字符串（`n` 为 `word` 的长度），找到 `ch` 的位置；随后切片、翻转和拼接也是线性操作，所以整体是线性时间。  
- **空间复杂度**：`O(n)`  
  - 解释：因为 Python 的字符串是不可变的，`word[:idx+1][::-1]` 会生成一个新的子串，最坏情况下会复制整个字符串，所以需要额外 `n` 的空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n)` 的线性时间，已经很快了。不过我们可以把**额外的空间**降到 `O(1)`（不计输出字符串本身的空间），即**原地**完成翻转。思路如下：

1. **同样先找** `ch` 第一次出现的位置 `idx`。这一步仍然是一次线性扫描。  
2. **如果找到了**，我们把 `word` 转成字符列表 `lst`（列表是可变的），然后使用**双指针**在 `[0, idx]` 区间内交换字符：左指针 `l` 从 `0` 开始，右指针 `r` 从 `idx` 开始，循环把 `lst[l]` 与 `lst[r]` 互换后 `l+=1, r-=1`，直到 `l >= r`。  
   - 这里的双指针就像两个人从两端走向中间，手里各拿一本书的页码，互相交换位置，最后书的前缀就被倒过来了。  
3. **把列表再转回字符串**，返回结果。  

这样我们只用了常数级的额外变量（两个指针），不再产生和原字符串等长的临时子串，空间使用更经济。

#### 代码（Python）

```python
def reversePrefix(word: str, ch: str) -> str:
    # 1. 找到 ch 第一次出现的位置
    idx = -1
    for i, c in enumerate(word):
        if c == ch:
            idx = i
            break

    # 2. 若不存在直接返回原串
    if idx == -1:
        return word

    # 3. 将字符串转为列表，方便原地修改
    lst = list(word)

    # 4. 双指针在前缀 [0, idx] 区间内交换字符
    l, r = 0, idx
    while l < r:
        lst[l], lst[r] = lst[r], lst[l]   # 交换
        l += 1
        r -= 1

    # 5. 列表转回字符串返回
    return ''.join(lst)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：同样只遍历一次找位置 `idx`（最多 `n` 步），随后在前缀区间最多交换 `idx/2 ≤ n/2` 次，仍然是线性时间。相比暴力解唯一的区别是省去了切片复制的常数因子。  
- **空间复杂度**：`O(1)`（不计输出字符串）  
  - 解释：我们只用了常数个额外变量 `idx, l, r`，以及把原字符串转成列表的 `O(n)` 空间是必须的，因为 Python 字符串不可原地修改。但相较于暴力解创建的额外子串，这里不再额外占用与 `n` 同量级的临时字符串空间。

---

## 心得

- **核心技巧**：**双指针在区间内原地翻转**（常用于数组/字符串的局部逆序）。  
- **适用的题型**：  
  1. “翻转子串” 类题目，例如 LeetCode 541. Reverse String、557. Reverse Words in a String III。  
  2. “数组/链表的区间翻转” 类题目，如 203. Remove Linked List Elements（思路相似的区间操作）。  
- **一句话总结解题钥匙**：**先定位区间端点，再用双指针把区间内部的元素逐对交换**。

---

## 反思

- **第一反应**：直接想到“先找字符位置，再切片翻转”。这是一种最自然的做法，但会产生额外的字符串拷贝。  
- **最容易踩的坑**：  
  - 忘记处理 **字符不存在** 的情况，直接对 `-1` 位置做翻转会导致错误。  
  - 在原地翻转时，如果写成 `while l <= r` 会把中间字符交换两次，导致结果错误。  
- **下次遇到同类题**：第一步先**明确要翻转的区间端点**，然后**考虑是否可以用双指针原地交换**，这样能在保证正确性的同时尽量降低空间开销。