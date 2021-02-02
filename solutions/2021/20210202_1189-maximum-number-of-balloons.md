# #1189. **气球的最大数量** / Maximum Number of Balloons

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-balloons/)

---

## 题目（英文原版）

**Description**

Given a string text, you want to use the characters of text to form as many instances of the word "balloon" as possible.
You can use each character in text at most once. Return the maximum number of instances that can be formed.
Note: This question is the same as  2287: Rearrange Characters to Make Target String.

**Examples**

**Example 1:**

```
Input: text = "nlaebolko"
Output: 1
```

**Example 2:**

```
Input: text = "loonbalxballpoon"
Output: 2
```

**Example 3:**

```
Input: text = "leetcode"
Output: 0
```

**Constraints**

- 1 <= text.length <= 104
- text consists of lower case English letters only.

---

## 题目（中文翻译）

给定一个字符串 (string) `text`，你希望使用 `text` 中的字符尽可能多地组成单词 **"balloon"**。  
每个字符在 `text` 中最多只能使用一次。返回能够组成的 **"balloon"** 的最大实例数 (maximum number of instances)。

**示例 1**  
**示例 2**  
**示例 3**  
**说明**：此题与 2287: Rearrange Characters to Make Target String 完全相同。

**示例**

**示例 1**  
输入: `text = "nlaebolko"`  
输出: `1`

**示例 2**  
输入: `text = "loonbalxballpoon"`  
输出: `2`

**示例 3**  
输入: `text = "leetcode"`  
输出: `0`

**约束条件**

- `1 <= text.length <= 10^4`
- `text` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**一次一次地把“balloon”从字符串里取走**，看还能取多少次。  
可以把 `text` 当成一盒字母拼图，**每取走一个 “balloon”，就把对应的字母块从盒子里删掉**，直到盒子里再也拼不出完整的 “balloon”。  

实现步骤  

1. 把 `text` 转成一个列表（每个字符就是一个可以单独删除的块）。  
2. 只要列表里还能找到 **b、a、l、l、o、o、n** 这七块，就把它们一次性删掉，计数器 `cnt` 加一。  
3. 当任意一个字母找不到时，循环结束，`cnt` 就是答案。  

> **数据结构类比**：列表就像装字母的抽屉，`pop`/`remove` 相当于把抽屉里的某个字母拿走。  

这种做法之所以**正确**，是因为我们每次都严格按照 “balloon” 的顺序把所需字母删掉，且每个字母最多只用一次，符合题目要求。  

**时间/空间分析（大白话）**  

- 每取一次 “balloon”，我们要在列表里 **线性扫描** 7 次（找 b、a、l、l、o、o、n），每一次 `remove` 也要把后面的元素往前搬一次。  
- 最坏情况下，`text` 长度为 `n`，我们最多能取 `n/7` 次（每次用了 7 个字母），于是总的操作次数约为 `O(n * n/7) ≈ O(n²)`。  
- 只用了一个字符列表，额外空间是 `O(n)`（复制了一遍字符串）。  

#### 代码（Python）  

```python
def maxNumberOfBalloons_bruteforce(text: str) -> int:
    # 把字符串转成列表，方便后面删除元素
    chars = list(text)
    cnt = 0                     # 记录成功拼出的 "balloon" 数量
    target = list("balloon")    # 需要的字母顺序

    while True:
        # 临时保存本次要删除的字符下标，防止在遍历时直接修改列表导致错位
        idx_to_remove = []
        for ch in target:       # 依次寻找 b a l l o o n
            try:
                # 找到第一个匹配的字符下标
                i = chars.index(ch)
                idx_to_remove.append(i)
                # 为了后面删除不影响前面的下标，暂时把该字符标记为 None
                chars[i] = None
            except ValueError:  # 没找到，说明已经拼不出完整的 balloon
                return cnt

        # 成功找到一整套，真正把标记的字符删除
        # 这里一次性删除比每次 pop 更快
        chars = [c for c in chars if c is not None]
        cnt += 1                # 完成一次拼接
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “n²” 代表如果字符串很长，暴力一次次删字符会导致大量的搬移操作，类似把一大堆纸张一张张撕掉，越撕越慢。  
- **空间复杂度**：`O(n)`  
  - 需要额外的列表来存放字符，和原字符串等长。  

---  

### 2. 最优解  

#### 思路  
从暴力解我们可以看到，**真正的耗时在不停地在列表里找字母并删除**。  
其实我们并不需要真的把字符一个个搬走，只要**统计每种字母出现的次数**，就能直接算出最多能拼出多少个 “balloon”。  

**关键点**  

1. 统计 `text` 中每个字母的出现次数。  
   - 这一步可以用 **哈希表**（Python 的 `dict` 或 `collections.Counter`）实现。  
   - 哈希表好比一本“字典”，把每个字母当成“单词”，对应的出现次数当成“页码”。查一次就能立刻知道这个字母有多少个。  

2. “balloon” 中每个字母需要的数量：  

| 字母 | 需要多少个 |
|------|------------|
| b    | 1          |
| a    | 1          |
| l    | 2          |
| o    | 2          |
| n    | 1          |

3. 对每种必需的字母，计算 **“手头有的数量 / 需要的数量”**（整数除法），得到这类字母能支持的最大 “balloon” 数。  
4. 最终答案是所有必需字母中**最小的那个**——因为一旦某个字母不够用了，整个单词就拼不完整了。  

> **为什么最小值是答案？**  
> 想象你在做手工拼图，每种形状的拼板都有一定数量。只能拼出完整图案的次数，取决于“最少的那种拼板”。  

**时间/空间分析（大白话）**  

- 只需要一次遍历字符串，**线性**地统计字母出现次数，时间是 `O(n)`（n 是字符串长度）。  
- 哈希表最多存 26 个小写字母，空间是 `O(1)`（常数级），因为字母种类固定。  

#### 代码（Python）  

```python
from collections import Counter

def maxNumberOfBalloons(text: str) -> int:
    # 1️⃣ 统计每个字符出现的次数
    freq = Counter(text)               # Counter 本质是 dict，key 是字符，value 是出现次数

    # 2️⃣ "balloon" 中各字符需要的数量
    need = {
        'b': 1,
        'a': 1,
        'l': 2,
        'o': 2,
        'n': 1,
    }

    # 3️⃣ 计算每种必需字符能支持的最大 balloon 数
    #    用一个很大的初始值，然后取最小值
    ans = float('inf')
    for ch, cnt in need.items():
        # 如果某字符根本不存在，freq[ch] 会返回 0，0 // cnt = 0，直接把答案变成 0
        ans = min(ans, freq.get(ch, 0) // cnt)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，`n` 代表字符串长度。比起暴力的 `n²`，这就像一次性把所有字母都数清楚，而不是一次次去找。  
- **空间复杂度**：`O(1)`  
  - 哈希表最多保存 26 条记录（所有小写字母），与 `n` 无关，属于常数级空间。  

---  

## 心得  

- **核心技巧**：**计数 + 取最小**（即 “每种必需资源的供给 / 需求，取最小值”）。  
- **适用场景**：  
  1. **重排字符构造目标字符串**（LeetCode 2287 – Rearrange Characters to Make Target String）。  
  2. **制作最大数量的汉堡/披萨**，每种配料有固定需求量。  
  3. **求最大完整套装数**，如“最多能配几套完整的玩具套装”。  
- **解题钥匙**：**先把资源（字符）统计清楚，再用最紧缺的那一种决定上限**。  

---  

## 反思  

- **第一反应**：看到“用字符拼单词”，自然想到“把字符一个个挑出来”，于是想到了暴力的“逐个删除”。  
- **最容易踩的坑**：  
  - 忘记 **'l'** 和 **'o'** 各需要出现两次，直接用 `freq['l'] // 1` 会把答案算得太大。  
  - 忽视字符可能根本不存在，直接除以需求会报错；使用 `freq.get(ch, 0)` 能安全返回 0。  
- **下次遇到同类题**：第一步就 **统计所有字符的出现次数**，然后 **根据目标词的每个字符需求量做整数除法**，最后取 **最小值**。这样可以直接从 `O(n²)` 跳到 `O(n)`。