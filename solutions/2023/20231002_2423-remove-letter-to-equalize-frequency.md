# #2423. 删除字母以使频率相等 / Remove Letter To Equalize Frequency

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/remove-letter-to-equalize-frequency/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string word, consisting of lowercase English letters. You need to select one index and remove the letter at that index from word so that the frequency of every letter present in word is equal.
Return true if it is possible to remove one letter so that the frequency of all letters in word are equal, and false otherwise.
Note:

**Examples**

**Example 1:**

```
Input: word = "abcc"
Output: true
Explanation: Select index 3 and delete it: word becomes "abc" and each character has a frequency of 1.
```

**Example 2:**

```
Input: word = "aazz"
Output: false
Explanation: We must delete a character, so either the frequency of "a" is 1 and the frequency of "z" is 2, or vice versa. It is impossible to make all present letters have equal frequency.
```

**Constraints**

- 2 <= word.length <= 100
- word consists of lowercase English letters only.

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串 `word`，仅包含小写英文字母。要求你选择一个下标并删除该下标处的字符，使得 `word` 中所有出现的字母的出现次数（frequency）相等。若可以通过删除恰好一个字符实现上述目标，返回 `true`，否则返回 `false`。

**示例 1**

```text
Input: word = "abcc"
Output: true
Explanation: 删除下标为 3 的字符后，字符串变为 "abc"，此时每个字符的频率都是 1。
```

**示例 2**

```text
Input: word = "aazz"
Output: false
Explanation: 必须删除一个字符，删除后要么 "a" 的频率为 1、"z" 的频率为 2，要么相反，无法使所有出现的字母频率相等。
```

**约束条件**

- `2 <= word.length <= 100`
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串的每一个位置都尝试删掉一次，删掉后重新统计剩余字符的出现次数，看这些次数是否全部相同。

- **数据结构**：我们可以用一个长度为 26 的数组 `cnt[0..25]` 来记录每个字母的出现次数。数组就像一本**查字典**，下标是字母（`a`→0，`b`→1…），里面的数字是对应字母的“页码”，即出现次数。
- **为什么正确**：遍历所有可能的删除位置，必然会覆盖“真正能让频率相等的那一次”。只要有一次删掉后频率相等，就返回 `True`。
- **时间/空间复杂度**  
  - 对每一个字符（最多 `n` 次）我们都要重新遍历一次字符串来统计频率（`O(n)`），所以总体是 `O(n²)`。如果把 `n=100` 代进去，最多要做 10,000 次计数，虽然在本题的约束下还能接受，但显然不是最好的做法。  
  - 使用的额外空间只有一个长度为 26 的数组，记作 `O(1)`（常数空间），因为 26 与输入规模无关。

#### 代码（Python）

```python
def equal_frequency_bruteforce(word: str) -> bool:
    n = len(word)
    # 把字符转成 0~25 的整数，方便下标访问
    nums = [ord(c) - ord('a') for c in word]

    for i in range(n):                     # ⬅️ 逐个尝试删除位置 i
        cnt = [0] * 26                     # 重新统计频率，像一本新字典
        for j in range(n):
            if j == i:                     # 跳过被删除的字符
                continue
            cnt[nums[j]] += 1              # 对应字母的页码 +1

        # 过滤掉出现次数为 0 的字母，只保留真正出现的
        freqs = [c for c in cnt if c > 0]

        # 判断所有出现次数是否相等
        if len(set(freqs)) == 1:           # set 把相同的次数合并，只剩一种说明相等
            return True

    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n` 次外层循环，每次都要遍历 `n` 个字符统计频率。  
  - 大白话：如果字符串长 100，最坏情况下要做 10,000 次“数字游戏”，这在电脑眼里是“小事”，但在更大的数据规模下会变慢。

- **空间复杂度**：`O(1)`（常数）  
  - 只用了长度固定为 26 的数组 `cnt`，不随输入大小增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于每次删除后都要**重新遍历整个字符串**。其实我们只需要一次遍历就能得到所有字母的出现次数，然后再根据这些次数判断是否可以只删掉 **一个** 字母就让频率统一。

关键点：

1. **一次遍历得到每个字母的频率**  
   用长度为 26 的数组 `cnt` 记录每个字母出现了多少次。相当于把整本字典一次性填好。

2. **再统计“频率出现的次数”**  
   把 `cnt` 中非零的数字拿出来，统计每种出现次数出现了多少个字母。  
   用一个字典 `freq_cnt`，键是出现次数（比如 1、2、3…），值是拥有该次数的字母种类数。  
   这一步相当于把**字典的页码再做一次目录**——我们关心的是“有多少种字母的频率是 2”，而不是具体是哪几个字母。

3. **只会出现两种特殊的频率分布**（因为只能删掉一个字符）  
   - **情况 A**：所有字母频率已经相同，只是某个字母出现了 **1 次**（比如 `aabbc` → 频率 `{2,2,1}`），删掉这个只出现一次的字母后，剩下的字母频率就全部相同。  
   - **情况 B**：出现次数最多的那类字母，只比其他字母多 **1 次**（比如 `aaabbbcc` → 频率 `{3,3,2}`），删掉一次出现次数最多的字母的一个实例后，所有频率统一。  
   - **特殊情况**：整个字符串只有一种字母（比如 `aaaa`），删掉任意一个后仍只有一种字母，频率自然相同。

   只要满足上面任意一种，就返回 `True`，否则 `False`。

4. **为什么只会出现这几种**  
   因为我们只能删除 **一个** 字符，频率的改变幅度只能是 **-1**（对应删掉的那个字母），所以最终的频率集合最多只能有两种不同的数值（原来的频率和减一后的频率），这就限制了可能的分布形态。

#### 代码（Python）

```python
def equal_frequency(word: str) -> bool:
    # 1. 统计每个字母出现多少次
    cnt = [0] * 26
    for ch in word:
        cnt[ord(ch) - ord('a')] += 1

    # 2. 统计“出现次数”本身出现了几次
    freq_cnt = {}
    for c in cnt:
        if c == 0:               # 没出现的字母不算
            continue
        freq_cnt[c] = freq_cnt.get(c, 0) + 1

    # 3. 只可能有两种不同的出现次数（或者只有一种）
    if len(freq_cnt) == 1:
        # 只有一种频率
        # a) 所有字母频率相同且只有一种字母 → 删除任意一个都可以
        # b) 所有字母频率相同且出现次数为 1 → 删除这唯一的字母后仍保持相同
        # 只要出现次数为 1 或者频率为 1，都可以删掉一个字母得到统一
        freq = next(iter(freq_cnt))
        # 只要出现的字母种类为 1（全同字符）或者频率为 1（每个字符只出现一次）
        return freq == 1 or list(freq_cnt.values())[0] == 1

    if len(freq_cnt) == 2:
        # 取出两种频率以及它们对应的字母种类数
        (f1, c1), (f2, c2) = freq_cnt.items()
        # 让 f1 总是较小的那个，方便后面判断
        if f1 > f2:
            f1, f2 = f2, f1
            c1, c2 = c2, c1

        # 情况 A：较小的频率是 1，且只出现一次（只出现一次的字母可以直接删掉）
        if f1 == 1 and c1 == 1:
            return True

        # 情况 B：较大的频率比小的频率大 1，且较大的频率只对应一种字母
        # 例如 {2:3, 3:1} → 删除频率为 3 的那个字母的一个实例后，所有频率变成 2
        if f2 - f1 == 1 and c2 == 1:
            return True

    # 其他任何分布都无法只删一个字符统一频率
    return False
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串统计字母出现次数（`n`），再遍历长度为 26 的数组统计频率出现次数，都是线性或常数时间。  
  - 与暴力解相比，省掉了 `n` 次的重复统计，速度提升明显。

- **空间复杂度**：`O(1)`（常数）  
  - 使用的额外空间只有两个长度固定为 26 的数组/字典，和输入规模无关。

---

## 心得

- **核心技巧**：利用**频率的频率**（即统计每个出现次数出现了多少个字母）来把问题从“遍历每个字符”压缩到“遍历最多 26 种字母”。  
- **适用题型**：  
  1. **“删除一个字符后使所有字符出现次数相同”**（本题）。  
  2. **“检查字符串是否可以通过一次修改满足某种计数约束”**（例如 LeetCode 2420 “Find All Good Indices” 中的计数类思路）。  
  3. **“找出出现次数最多的字符”**（常见的字符统计类题目）。
- **一句话总结**：**把“每个字母出现了多少次”再一次计数，得到的两层统计能快速判断唯一的删字符是否能让所有频率统一**。

---

## 反思

- **第一反应**：直接暴力尝试每个位置的删除，写出可运行的代码。  
- **最容易踩的坑**：  
  - 忽略了只有一种字符的特殊情况（如 `"aaaa"`），容易误判为 `False`。  
  - 在判断两种频率时，忘记把较大的频率对应的字母种类数必须为 `1`，导致错误接受了像 `{2:2, 3:2}` 这种不可能只删一次字符的情况。  
- **下次思路**：一看到“只允许删除/修改一次”这类限制，就先**统计整体的频率分布**，看看能否通过一次微调（+1 / -1）把分布统一，而不是直接遍历每个位置。这样思路更清晰，代码也更高效。