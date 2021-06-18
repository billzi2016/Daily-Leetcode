# #1370. 递增递减字符串 / Increasing Decreasing String

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/increasing-decreasing-string/)

---

## 题目（英文原版）

**Description**

You are given a string s. Reorder the string using the following algorithm:
If the smallest or largest character appears more than once, you may choose any occurrence to append to the result.
Return the resulting string after reordering s using this algorithm.

**Examples**

**Example 1:**

```
Input: s = "aaaabbbbcccc"
Output: "abccbaabccba"
Explanation: After steps 1, 2 and 3 of the first iteration, result = "abc"
After steps 4, 5 and 6 of the first iteration, result = "abccba"
First iteration is done. Now s = "aabbcc" and we go back to step 1
After steps 1, 2 and 3 of the second iteration, result = "abccbaabc"
After steps 4, 5 and 6 of the second iteration, result = "abccbaabccba"
```

**Example 2:**

```
Input: s = "rat"
Output: "art"
Explanation: The word "rat" becomes "art" after re-ordering it with the mentioned algorithm.
```

**Constraints**

- 1 <= s.length <= 500
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 **s**（string），请按照以下算法重新排列该字符串：

1. 从剩余字符中选取**字典序最小**（smallest）的字符，将其追加到结果字符串中并从 **s** 中移除。  
2. 继续选取字典序严格递增的字符（即比上一次选取的字符大的最小字符），依次追加并移除，直至不存在更大的字符。  
3. 然后从剩余字符中选取**字典序最大**（largest）的字符，将其追加到结果字符串中并从 **s** 中移除。  
4. 再选取字典序严格递减的字符（即比上一次选取的字符小的最大字符），依次追加并移除，直至不存在更小的字符。  
5. 重复步骤 1‑4，直至 **s** 为空。

> **注意**：如果当前的最小字符或最大字符出现多次，你可以任选其中一次加入结果。

返回按照上述算法重新排列后的字符串。

---

### 示例

#### 示例 1
**输入**  
``` 
s = "aaaabbbbcccc"
```  
**输出**  
```
"abccbaabccba"
```  
**解释**  
第一次迭代的步骤 1、2、3 后，`result = "abc"`。  
接着执行步骤 4、5、6，`result = "abccba"`。  
第一轮结束，此时 `s = "aabbcc"`，回到步骤 1。  
第二轮的步骤 1、2、3 后，`result = "abccbaabc"`。  
随后步骤 4、5、6 完成后，`result = "abccbaabccba"`。

#### 示例 2
**输入**  
``` 
s = "rat"
```  
**输出**  
```
"art"
```  
**解释**  
字符串 `"rat"` 经过上述算法重新排序后得到 `"art"`。

---

### 约束条件
- `1 <= s.length <= 500`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次一次地模拟题目描述的过程**：

1. 把剩下的字符全部取出来，按照字典序（`a` → `z`）排好序。  
2. 按顺序遍历排好序的字符，把每个字符的**第一个出现**依次加入答案，这对应 “从小到大取一次”。  
3. 再把剩下的字符按照逆序（`z` → `a`）排好序，依次把每个字符的**第一个出现**加入答案，这对应 “从大到小取一次”。  
4. 重复 1~3，直到所有字符都被取完。

> **类比**：把剩下的字符想象成一本散页的书，  
> - “从小到大取一次”相当于把书页按字母顺序排好，然后每种字母只抽走最左边那一页。  
> - “从大到小取一次”则是把书页倒着排，再抽走最左边那一页。  
> 这两步交替进行，直到书页全部抽完。

这种做法一定能得到题目要求的结果，因为我们严格遵循了题目给出的**“最小字符 → 最大字符 → 最小字符 → …”**的顺序。

#### 代码（Python）

```python
def sortString_bruteforce(s: str) -> str:
    # 记录剩余字符
    remain = list(s)          # 把字符串转成列表，方便删除
    ans = []                  # 最终答案

    while remain:             # 只要还有字符就继续
        # 1. 按字典序升序排列
        remain.sort()        # O(k log k)，k 为当前剩余字符数
        # 2. 从左到右遍历，只保留每种字符的第一个
        i = 0
        while i < len(remain):
            ans.append(remain[i])      # 把当前字符加入答案
            # 删除该字符的所有出现，只保留第一次（因为后面要逆序再取一次）
            ch = remain[i]
            # 删除已经取走的字符（只删一次）
            del remain[i]
            # 跳过同字符的后续出现，保持每种字符只取一次
            while i < len(remain) and remain[i] == ch:
                i += 1

        # 3. 按字典序降序排列
        remain.sort(reverse=True)
        # 4. 同样只取每种字符的第一个
        i = 0
        while i < len(remain):
            ans.append(remain[i])
            ch = remain[i]
            del remain[i]
            while i < len(remain) and remain[i] == ch:
                i += 1

    return ''.join(ans)
```

> **关键行注释**  
> - `remain.sort()`：把剩余字符排好序，像把书页重新整理。  
> - `while i < len(remain) …`：遍历排好序的列表，只把每种字符的**第一次出现**加入答案，并删除这一次，以免在本轮再次被取到。  

#### 复杂度

- **时间复杂度**：`O(n² log n)`  
  - 每轮循环都要对剩余字符 `k`（逐渐递减）进行排序，排序的代价是 `O(k log k)`。  
  - 由于循环大约进行 `n / 1` 次（每轮至少取走 1 个字符），总体近似 `O(n² log n)`。  
  - **大白话**：如果字符串长 100，最坏情况下要做 100 次排序，每次排序都要花大约 `100 * log 100` 的时间，整体就会很慢。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表 `remain` 保存剩余字符，最多和原字符串等长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每轮都要排序**，而字符集只有 26 个小写英文字母。我们可以用**计数数组（哈希表）**一次性记录每个字符出现的次数，随后按照固定的顺序遍历计数数组，就不需要再排序。

1. **统计频次**：用长度为 26 的数组 `cnt[0..25]`，`cnt[i]` 表示字符 `chr(ord('a')+i)` 在原串中出现的次数。  
   - 类比：把每种字符的出现次数写在一张表格里，像字典的“词条 → 页码”。  
2. **循环取字符**：只要还有未取完的字符（`total > 0`），就做两遍遍历：
   - **从小到大**：`i` 从 `0` 到 `25`，如果 `cnt[i] > 0`，把对应字符加入答案并把 `cnt[i]` 减 1。  
   - **从大到小**：`i` 从 `25` 到 `0`，同理再取一次。  
   这样一次完整的“升序 → 降序”就完成了。  
3. 重复第 2 步，直到所有计数都变成 0（即 `total == 0`）。

**为什么正确**：  
- 每一次遍历都严格遵守“先最小后最大”的顺序。  
- 对每个字符我们只在它还有剩余次数时才取一次，正好对应题目里“如果最小/最大字符出现多次，可以任选一次”。  
- 当所有计数都耗尽时，说明所有字符都已经按要求被放入答案，过程结束。

#### 代码（Python）

```python
def sortString(s: str) -> str:
    # 1. 统计每个字符出现的次数
    cnt = [0] * 26                     # 26 个字母的计数表
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1   # 把对应位置的计数加一

    total = len(s)                     # 剩余未取的字符数
    ans = []                           # 用列表收集答案，效率更高

    while total > 0:                   # 只要还有字符就继续
        # 2. 从小到大遍历一次
        for i in range(26):            # i = 0 对应 'a', i = 25 对应 'z'
            if cnt[i] > 0:             # 该字符还有剩余
                ans.append(chr(ord('a') + i))
                cnt[i] -= 1
                total -= 1

        # 3. 从大到小遍历一次
        for i in range(25, -1, -1):    # 逆序遍历
            if cnt[i] > 0:
                ans.append(chr(ord('a') + i))
                cnt[i] -= 1
                total -= 1

    return ''.join(ans)                # 把列表拼成字符串返回
```

> **关键行注释**  
> - `cnt = [0] * 26`：创建一个长度为 26 的计数表，像一本只记录字母出现次数的小册子。  
> - `cnt[ord(ch) - ord('a')] += 1`：把字符转换成下标并计数。  
> - `for i in range(26)` / `for i in range(25, -1, -1)`：固定顺序遍历计数表，分别实现“从小到大取一次”和“从大到小取一次”。  
> - `total` 用来快速判断是否所有字符都已取完，避免每轮都遍历整个计数表来检查是否全为 0。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 统计频次遍历一次字符串，`O(n)`。  
  - 主循环中每次遍历计数表固定 26 次（常数），不随 `n` 增长。整体仍是线性 `O(n)`。  
  - **大白话**：不管字符串有多长，我们只需要一次“数数”，然后每轮最多看 26 个字母，速度非常快。

- **空间复杂度**：`O(1)`（常数级）  
  - 只用了长度为 26 的计数数组和几个常数变量，和字符串长度无关。  
  - **大白话**：不管输入有多大，额外占用的内存始终是固定的几百字节。

---

## 心得

- **核心技巧**：利用字符种类固定（只有 26 个小写字母），用**计数数组**代替排序，实现线性时间的字符重排。  
- **适用的题型**：  
  1. “字符计数”类题目，如 **"Sort Characters By Frequency"**（按频率排序字符）。  
  2. “固定顺序遍历”类题目，如 **"Rearrange String k Distance Apart"**（距离为 k 的重新排列）。  
  3. “区间/顺序统计”类题目，如 **"Find the Smallest Letter Greater Than Target"**（找大于目标的最小字符）。  
- **一句话总结**：**“当字符种类有限时，用计数表一次遍历搞定所有排序需求”。**

---

## 反思

- **第一反应**：看到“从小到大、从大到小交替”就想到**先排序再双指针**，但忘记字符集只有 26 种，导致想到的排序会重复做很多次。  
- **最容易踩的坑**：  
  - **边界条件**：当某个字符只剩一次时，升序和降序遍历都要检查它，否则会漏掉。  
  - **计数递减错误**：忘记在取字符后 `cnt[i] -= 1`，会导致无限循环。  
  - **输出格式**：答案要一次性拼接成字符串，不能在每次循环中直接 `print`。  
- **下次第一步**：先**统计字符频次**，看是否可以利用“字符种类有限”这一特性，决定是否需要排序。这样可以直接跳到最优思路，省去不必要的重复排序。