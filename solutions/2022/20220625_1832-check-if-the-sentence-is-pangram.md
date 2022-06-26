# #1832. 检查句子是否为全字母句 / Check if the Sentence Is Pangram

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/check-if-the-sentence-is-pangram/)

---

## 题目（英文原版）

**Description**

A pangram is a sentence where every letter of the English alphabet appears at least once.
Given a string sentence containing only lowercase English letters, return true if sentence is a pangram, or false otherwise.

**Examples**

**Example 1:**

```
Input: sentence = "thequickbrownfoxjumpsoverthelazydog"
Output: true
Explanation: sentence contains at least one of every letter of the English alphabet.
```

**Example 2:**

```
Input: sentence = "leetcode"
Output: false
```

**Constraints**

- 1 <= sentence.length <= 1000
- sentence consists of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
pangram（全字母句）是指每个英文字母表中的字母至少出现一次的句子。  
给定一个仅包含 lowercase English letters（小写英文字母）的字符串 `sentence`，如果 `sentence` 是 pangram（全字母句），返回 `true`，否则返回 `false`。

**示例 1**  

**输入**  
``` 
sentence = "thequickbrownfoxjumpsoverthelazydog"
```  
**输出**  
```
true
```  
**解释**  
`sentence` 至少包含英文字母表的每个字母各一次。

**示例 2**  

**输入**  
``` 
sentence = "leetcode"
```  
**输出**  
```
false
```  

**约束条件**  
- `1 <= sentence.length <= 1000`  
- `sentence` 仅由 lowercase English letters（小写英文字母）组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把句子里出现的每个字母记下来**，最后看记下来的字母数量是否已经达到 26（英文字母的个数）。  
这里可以使用**哈希表**（在 Python 中直接用 `set`），它的工作方式很像查字典：  
- **key** 就是字母本身（比如 `'a'`），  
- **value**（这里我们不需要）可以想象成字典里对应的页码。  
因为 `set` 会自动去重，只要把每个出现的字符“塞”进去，最后 `set` 的长度就是不同字母的个数。

这个方法**一定正确**：只要句子里出现了所有 26 个字母，`set` 的大小就会是 26；如果缺少任何一个字母，大小就会小于 26。

**时间复杂度**：我们需要遍历一次字符串，长度记作 `n`，每个字符的插入操作在哈希表里是 **O(1)** 的均摊时间，所以总共是 **O(n)**。  
**空间复杂度**：最多会存 26 个不同的字符，常数级别的空间，用 **O(1)** 表示（因为 26 是固定的，不会随 `n` 增长）。

#### 代码（Python）

```python
def checkIfPangram(sentence: str) -> bool:
    # 用集合记录已经出现过的字符
    seen = set()                     # 空集合，相当于“空字典”
    for ch in sentence:              # 遍历句子中的每个字符
        seen.add(ch)                 # 把字符加入集合，重复的会自动去重
        # 只要集合已经装满 26 个字母，就可以提前返回 True
        if len(seen) == 26:          # 集合大小等于字母表长度
            return True
    # 循环结束后如果集合不满 26，说明缺字母
    return False
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 线性遍历一次字符串，`n` 是句子的长度。  
- **空间复杂度**：`O(1)` —— 最多只会存 26 个字符，属于常数空间。

---

### 2. 最优解

#### 思路  

虽然上面的集合解已经是 **线性时间、常数空间**，在实际面试里还有一种更“低配”的做法——**位运算**（bitmask）。  
它的核心思想是：

1. 把 26 个字母映射到 26 个二进制位（第 0 位对应 `'a'`，第 1 位对应 `'b'` …… 第 25 位对应 `'z'`）。  
2. 用一个整数 `mask` 记录哪些字母出现过。把对应位设为 1 即表示该字母已出现。  
3. 遍历完字符串后，检查 `mask` 是否已经全部为 1（即 `mask == (1 << 26) - 1`），若是则是全字母句子。

为什么这样更好？

- **空间更省**：只用一个整数（在 Python 中整数大小不受限），相当于只占用了 4~8 个字节。  
- **速度更快**：位运算是 CPU 的原生指令，几乎不需要额外的函数调用或哈希计算。  

下面一步步解释关键操作：

| 操作 | 解释 |
|------|------|
| `ord(ch) - ord('a')` | 把字符 `'a'~'z'` 转换为 0~25 的索引。就像把字母映射到数组下标。 |
| `1 << idx` | 把数字 1 左移 `idx` 位，得到只有第 `idx` 位为 1 的二进制数。 |
| `mask |= 1 << idx` | 用 **或** 操作把第 `idx` 位设为 1，表示该字母出现过。 |
| `full = (1 << 26) - 1` | 26 位全为 1 的二进制数，等价于十进制的 `67108863`。 |

如果遍历完后 `mask == full`，说明每一位都被设过 1，即所有字母都出现过。

#### 代码（Python）

```python
def checkIfPangram(sentence: str) -> bool:
    mask = 0                     # 用 0 表示“还没有出现任何字母”
    for ch in sentence:          # 逐字符遍历
        idx = ord(ch) - ord('a') # 把字符转成 0~25 的索引
        mask |= 1 << idx         # 把对应的位设为 1
        # 只要 mask 已经等于全部 1，就可以提前返回 True
        if mask == (1 << 26) - 1:
            return True
    # 循环结束后仍未全满，说明缺字母
    return False
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然只遍历一次字符串。位运算的常数因子比集合更小。  
- **空间复杂度**：`O(1)` —— 只用了一个整数来记录状态，真正的常数空间。

---

## 心得

- 这道题考察的核心技巧是 **集合去重** 与 **位掩码（bitmask）** 的使用。  
- 同类技巧常出现在以下题目中：  
  1. **判断数组是否包含所有数字 0~9**（类似全数字题）  
  2. **找出缺失的字母**（如 LeetCode 268. Missing Number）  
  3. **统计出现过的字符种类**（如 统计字符串中不同字符的个数）  
- **一句话总结解题钥匙**：把“出现过的东西”映射到**唯一标识**（集合的 key 或位的下标），遍历一次即可完成检查。

## 反思

- **第一反应**：把每个字符记下来，最后数数有没有 26 个不同的字母。  
- **最容易踩的坑**：  
  - 忘记字符串只包含小写字母，若出现大写需要先 `lower()`。  
  - 直接用 `len(set(sentence)) == 26` 也是可行的，但要注意 **提前返回** 可以省时间。  
- **下次类似题的第一步**：先把“出现过的元素”映射到一个**固定大小的标记结构**（集合、数组、位掩码），再检查标记是否已经全部被激活。