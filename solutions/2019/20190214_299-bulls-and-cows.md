# #299. 猜数字（Bulls and Cows） / Bulls and Cows

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/bulls-and-cows/)

---

## 题目（英文原版）

**Description**

You are playing the Bulls and Cows game with your friend.
You write down a secret number and ask your friend to guess what the number is. When your friend makes a guess, you provide a hint with the following info:
Given the secret number secret and your friend's guess guess, return the hint for your friend's guess.
The hint should be formatted as "xAyB", where x is the number of bulls and y is the number of cows. Note that both secret and guess may contain duplicate digits.

**Examples**

**Example 1:**

```
Input: secret = "1807", guess = "7810"
Output: "1A3B"
Explanation: Bulls are connected with a '|' and cows are underlined:
"1807"
  |
"7810"
```

**Example 2:**

```
Input: secret = "1123", guess = "0111"
Output: "1A1B"
Explanation: Bulls are connected with a '|' and cows are underlined:
"1123"        "1123"
  |      or     |
"0111"        "0111"
Note that only one of the two unmatched 1s is counted as a cow since the non-bull digits can only be rearranged to allow one 1 to be a bull.
```

**Constraints**

- 1 <= secret.length, guess.length <= 1000
- secret.length == guess.length
- secret and guess consist of digits only.

---

## 题目（中文翻译）

你正在和朋友玩 **Bulls and Cows**（猜数字）游戏。  
你先写下一个 **secret**（秘密）数字，让朋友来猜这个数字。当朋友给出一次 **guess**（猜测）时，你需要根据以下规则给出提示：

- **bulls**（公牛）指的是位置和数字都完全相同的字符数量。  
- **cows**（奶牛）指的是数字正确但位置错误的字符数量。  

返回的提示必须遵循 `"xAyB"` 的格式，其中 `x` 表示 **bulls** 的数量，`y` 表示 **cows** 的数量。请注意，`secret` 和 `guess` 中可能包含重复的数字。

---

## 示例

### 示例 1
**输入**  
`secret = "1807", guess = "7810"`

**输出**  
`"1A3B"`

**解释**  
公牛（bulls）用竖线 `|` 标记，奶牛（cows）用下划线标记：

```
"1807"
  |
"7810"
```

### 示例 2
**输入**  
`secret = "1123", guess = "0111"`

**输出**  
`"1A1B"`

**解释**  
公牛（bulls）用竖线 `|` 标记，奶牛（cows）用下划线标记：

```
"1123"        "1123"
  |      or     |
"0111"        "0111"
```

注意：只有一个未匹配的 `1` 被计为奶牛（cow），因为非公牛的数字只能重新排列以形成一个 `1` 为公牛（bull）。

---

## 约束条件

- `1 <= secret.length, guess.length <= 1000`
- `secret.length == guess.length`
- `secret` 和 `guess` 仅由数字字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把每一位都拿出来比较：

1. **先找 “bull”(A)**：遍历 `secret` 与 `guess` 的每个下标 `i`，如果 `secret[i] == guess[i]`，说明这位是 **bull**，计数 `bulls` 加一。  
2. **再找 “cow”(B)**：把所有 **非 bull** 的字符收集起来（比如用两个列表 `s_remain`、`g_remain`），然后在 `g_remain` 中每找一个字符在 `s_remain` 里出现过，就算作 **cow**，并把对应的字符从 `s_remain` 中删掉，防止重复计数。

> **类比**：把 `secret` 想成一本字典，`guess` 想成一本待查的手册。先把两本书对应页码完全相同的章节划出来（bull），剩下的章节再在另一册里找有没有相同的词（cow），找到就算作匹配。

这种做法一定能得到正确答案，因为我们把所有可能的匹配都枚举了一遍，只是效率不高。

#### 代码（Python）
```python
def getHint_bruteforce(secret: str, guess: str) -> str:
    n = len(secret)
    bulls = 0                     # 记录 A 的数量
    s_remain = []                 # secret 中非 bull 的字符
    g_remain = []                 # guess 中非 bull 的字符

    # 第一步：找出所有的 bull
    for i in range(n):
        if secret[i] == guess[i]:
            bulls += 1
        else:
            s_remain.append(secret[i])
            g_remain.append(guess[i])

    # 第二步：在剩余字符里找 cow（注意要防止重复计数）
    cows = 0
    for ch in g_remain:           # 逐个检查 guess 的剩余字符
        if ch in s_remain:        # 如果 secret 里还有相同的字符
            cows += 1
            s_remain.remove(ch)   # 删除一次，避免同一个字符被多算

    return f"{bulls}A{cows}B"
```

#### 复杂度
- **时间复杂度**：`O(n²)`  
  解释：外层遍历一次得到 `O(n)`，而 `list.remove` 需要在列表中线性查找，最坏情况是 `O(n)`，两者相乘就是 `O(n²)`。可以把它想象成在一条长队里找人，每找一次都要从头到尾遍历一次队伍。
- **空间复杂度**：`O(n)`  
  需要额外的两个列表来保存非 bull 的字符，最坏情况下会存 `n` 个字符。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **第二步的线性搜索和删除**。我们可以用**计数**来把“在列表里找有没有相同的字符”这件事降到 `O(1)`。

1. **遍历一次字符串**（一次遍历完成两件事）  
   - 如果当前位置相同，直接计入 `bulls`。  
   - 否则，把 `secret[i]` 与 `guess[i]` 各自的数字计数放进两个长度为 10 的数组 `cnt_secret`、`cnt_guess`（因为只有 `'0'~'9'` 十种可能）。  

2. **计算 cows**  
   - 对每个数字 `d`（0~9），`cnt_secret[d]` 表示 secret 中该数字出现但不是 bull 的次数，`cnt_guess[d]` 同理。  
   - 两者的最小值 `min(cnt_secret[d], cnt_guess[d])` 就是该数字可以组成的 cow 数量（因为每对匹配只能使用一次）。把所有数字的最小值加起来，就是总的 `cows`。

> **类比**：把十个小盒子想成“零钱盒”，每个盒子专门放一种面额的硬币。我们把 secret 中的未匹配硬币倒进对应的盒子，同理把 guess 的硬币倒进另一套盒子。最后，两套盒子里相同面额的硬币能配对的数量，就是 cow 的数量。

这样只需要 **一次遍历**（`O(n)`）加上 **常数大小的十次遍历**（`O(10)`），整体时间是线性的，空间只需要两个长度为 10 的数组（`O(1)`）。

#### 代码（Python）
```python
def getHint(secret: str, guess: str) -> str:
    bulls = 0                     # A 的计数
    # 只需要 10 个位置，分别统计 0~9 的出现次数（排除已经是 bull 的情况）
    cnt_secret = [0] * 10
    cnt_guess  = [0] * 10

    for s, g in zip(secret, guess):
        if s == g:                # 完全匹配 → bull
            bulls += 1
        else:
            # ord('0') = 48，转成 0~9 的整数索引
            cnt_secret[ord(s) - ord('0')] += 1
            cnt_guess[ord(g) - ord('0')]  += 1

    # 计算 cows：对每个数字取出现次数的最小值
    cows = 0
    for d in range(10):
        cows += min(cnt_secret[d], cnt_guess[d])

    return f"{bulls}A{cows}B"
```

#### 复杂度
- **时间复杂度**：`O(n)` — 只遍历一次字符串，`n` 是字符串长度。想象成一次走遍整个游戏板，所有信息一次性收集完毕。
- **空间复杂度**：`O(1)` — 只用了固定大小（10）的两个数组，和字符串长度无关。相当于只准备了十个小盒子，无论游戏板多大，盒子数量始终不变。

---

## 心得

- **核心技巧**：**计数（哈希表/数组）+ 一次遍历**，把“在剩余字符里找匹配”转化为“对应数字出现次数的最小值”。  
- **适用题型**：  
  1. **字母异位词判断**（LeetCode 242）——使用字符计数判断两串是否由相同字符组成。  
  2. **找出数组中出现次数超过 ⌊n/3⌋ 的元素**（LeetCode 229）——利用计数或投票法。  
  3. **字母计数类的子串匹配**（如滑动窗口求最小覆盖子串）——同样依赖计数数组/字典。  
- **一句话总结解题钥匙**：**把“能匹配多少次”转化为“每种字符出现次数的最小值”。**

---

## 反思

- **第一反应**：直接逐位比较，遇到不相同的就去别的位找匹配（暴力双循环）。  
- **最容易踩的坑**：  
  - **重复数字的计数**：如果不把已经算作 bull 的位置排除，会导致 cow 计数多算。  
  - **边界条件**：长度为 1 的字符串或全部相同的数字，需要确保计数数组不越界。  
- **下次遇到同类题**：第一步先 **划分出确定匹配的部分（bull）**，然后 **用计数或哈希结构处理剩余的“可能匹配”**，避免 O(n²) 的搜索。