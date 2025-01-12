# #3019. 键位更换次数 / Number of Changing Keys

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/number-of-changing-keys/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s typed by a user. Changing a key is defined as using a key different from the last used key. For example, s = "ab" has a change of a key while s = "bBBb" does not have any.
Return the number of times the user had to change the key.
Note: Modifiers like shift or caps lock won't be counted in changing the key that is if a user typed the letter 'a' and then the letter 'A' then it will not be considered as a changing of key.

**Examples**

**Example 1:**

```
Input: s = "aAbBcC"
Output: 2
Explanation: 
From s[0] = 'a' to s[1] = 'A', there is no change of key as caps lock or shift is not counted.
From s[1] = 'A' to s[2] = 'b', there is a change of key.
From s[2] = 'b' to s[3] = 'B', there is no change of key as caps lock or shift is not counted.
From s[3] = 'B' to s[4] = 'c', there is a change of key.
From s[4] = 'c' to s[5] = 'C', there is no change of key as caps lock or shift is not counted.
```

**Example 2:**

```
Input: s = "AaAaAaaA"
Output: 0
Explanation: There is no change of key since only the letters 'a' and 'A' are pressed which does not require change of key.
```

**Constraints**

- 1 <= s.length <= 100
- s consists of only upper case and lower case English letters.

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串 `s`，表示用户的输入。**更换键**（changing a key）定义为使用的键与上一次使用的键不同。例如，`s = "ab"` 中存在键的更换，而 `s = "bBBb"` 中不存在键的更换。  
返回用户必须更换键的次数。

**注意**：Shift、Caps Lock 等修饰键不计入键的更换。也就是说，如果用户先输入字符 `'a'`，随后输入字符 `'A'`，这不算作键的更换。

### 示例

**示例 1**

```
Input: s = "aAbBcC"
Output: 2
Explanation: 
从 s[0] = 'a' 到 s[1] = 'A'，没有键的更换，因为 Caps Lock 或 Shift 不计入。
从 s[1] = 'A' 到 s[2] = 'b'，发生键的更换。
从 s[2] = 'b' 到 s[3] = 'B'，没有键的更换，因为 Caps Lock 或 Shift 不计入。
从 s[3] = 'B' 到 s[4] = 'c'，发生键的更换。
从 s[4] = 'c' 到 s[5] = 'C'，没有键的更换。
```

**示例 2**

```
Input: s = "AaAaAaaA"
Output: 0
Explanation: 没有键的更换，因为只按了 `'a'` 与 `'A'`，这不需要更换键。
```

### 约束

- `1 <= s.length <= 100`
- `s` 仅由大小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐字符扫描**这段输入的键盘记录 `s`，把每个字符都统一成同一种形式（这里用全部小写），然后把相邻两个字符进行比较：

- 如果 **当前字符**（已转成小写）和 **上一个字符**（已转成小写）不相同，就说明用户换了一把键（不管是大小写，只要字母本身不同就算换键）。
- 如果相同，则说明仍在使用同一把键。

这就好比我们在看一本 **字典**（哈希表的类比），字典里每个单词只对应一个“根本形态”。把所有字母都映射到它们的小写形态，就相当于把大小写视作同一个“词”。然后我们只需要顺序检查相邻两个词是否相同即可。

> **为什么正确**  
> 题目说明：**仅当键盘实际使用的字母不同** 时才算一次换键；大小写只是一种修饰键（Shift / CapsLock），不算换键。把所有字母转成小写后，大小写差异被消除，比较得到的结果恰好对应题目所需的“是否换键”。

#### 代码（Python）

```python
def numberOfKeyChanges(s: str) -> int:
    """
    直觉解：遍历字符串，统计相邻字符（转为小写后）不相同的次数。
    """
    # 先把整个字符串全部转成小写，后面比较就不需要再考虑大小写了
    lower_s = s.lower()

    changes = 0                 # 用来计数换键的次数
    # 从下标 1 开始遍历，和前一个字符比较
    for i in range(1, len(lower_s)):
        # 如果当前字符和前一个字符不相同，说明换键
        if lower_s[i] != lower_s[i - 1]:
            changes += 1
    return changes
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了一遍字符串，`n` 是字符串长度。这里的 `O(n)` 可以想象成“走完这条路只需要一次脚步”，不管路有多长，步数正好等于路长。
- **空间复杂度**：`O(n)` —— 额外创建了 `lower_s`，它的长度和原字符串相同。若把这一步改成 **原地** 转小写（使用 `s[i].lower()`），则可以降到 `O(1)`（只用常数级的额外空间）。

---

### 2. 最优解

#### 思路  

在上述直觉解中，**最大的开销** 是创建了一个新的全小写字符串 `lower_s`（占用了额外的 `O(n)` 空间）。其实我们完全可以在遍历的同时把每个字符临时转成小写，而不需要额外的存储，这样就达到了 **最优的空间使用**。

优化步骤：

1. **不创建新字符串**：直接在循环里使用 `s[i].lower()` 获得当前字符的小写形式，`s[i-1].lower()` 获得前一个字符的小写形式。
2. 其余逻辑保持不变：只要两次转小写的结果不同，就计数一次换键。

这样做的核心技巧是**“在使用时即时转换”**，类似于在阅读一本书时，只在需要时把生词翻译成熟词，而不是一次性把整本书都翻译好。

#### 代码（Python）

```python
def numberOfKeyChanges(s: str) -> int:
    """
    最优解：一次遍历，边遍历边把字符转成小写，省去额外的 O(n) 空间。
    """
    if not s:                     # 防御式写法，虽然题目保证长度 ≥ 1
        return 0

    changes = 0
    # 先把第一个字符转成小写，保存为上一个字符的状态
    prev = s[0].lower()

    for ch in s[1:]:              # 从第二个字符开始遍历
        cur = ch.lower()          # 当前字符的小写形式
        if cur != prev:           # 与上一个字符不同 → 换键
            changes += 1
        prev = cur                # 更新“上一个字符”
    return changes
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然只遍历一次字符串，和暴力解一样快。  
- **空间复杂度**：`O(1)` —— 只用了几个额外的变量 (`changes`, `prev`, `cur`)，与字符串长度无关。相比于暴力解省掉了 `O(n)` 的额外存储。

---

## 心得

- **核心技巧**：把大小写统一（`lower()`）后，统计相邻字符是否相同。  
- **适用的题型**：  
  1. **字符归一化后计数**（如统计不同的字母种类、连续相同字符的次数）。  
  2. **相邻元素比较**（如 LeetCode 1578 “Minimum Deletion Size”、面试常见的 “删除相邻相同字符”）。  
  3. **一次遍历求解**（如求字符串中出现的 “转折点”）。
- **一句话总结解题钥匙**：**先把字母统一到同一种形态，再一次遍历比较相邻是否相同**。

## 反思

- **第一反应**：把字符串全部转成小写，然后数相邻不同的次数。  
- **最容易踩的坑**：忘记把大小写统一，导致把 `'a'` 与 `'A'` 当成不同键而多计数；或者在统计时把首字符也算进去（实际上换键是从第二个字符开始判断的）。  
- **下次类似题的第一步**：**确定是否需要归一化（如大小写、空格、特殊符号）**，再决定遍历方式。这样可以避免因表面差异而产生错误计数。