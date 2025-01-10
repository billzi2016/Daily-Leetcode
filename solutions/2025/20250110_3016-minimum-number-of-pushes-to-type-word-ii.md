# #3016. 键入单词的最少按键次数 II / Minimum Number of Pushes to Type Word II

> 难度：中等 · 标签：Hash Table、String、Greedy、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/)

---

## 题目（英文原版）

**Description**

You are given a string word containing lowercase English letters.
Telephone keypads have keys mapped with distinct collections of lowercase English letters, which can be used to form words by pushing them. For example, the key 2 is mapped with ["a","b","c"], we need to push the key one time to type "a", two times to type "b", and three times to type "c" .
It is allowed to remap the keys numbered 2 to 9 to distinct collections of letters. The keys can be remapped to any amount of letters, but each letter must be mapped to exactly one key. You need to find the minimum number of times the keys will be pushed to type the string word.
Return the minimum number of pushes needed to type word after remapping the keys.
An example mapping of letters to keys on a telephone keypad is given below. Note that 1, *, #, and 0 do not map to any letters.

**Examples**

**Example 1:**

```
Input: word = "abcde"
Output: 5
Explanation: The remapped keypad given in the image provides the minimum cost.
"a" -> one push on key 2
"b" -> one push on key 3
"c" -> one push on key 4
"d" -> one push on key 5
"e" -> one push on key 6
Total cost is 1 + 1 + 1 + 1 + 1 = 5.
It can be shown that no other mapping can provide a lower cost.
```

**Example 2:**

```
Input: word = "xyzxyzxyzxyz"
Output: 12
Explanation: The remapped keypad given in the image provides the minimum cost.
"x" -> one push on key 2
"y" -> one push on key 3
"z" -> one push on key 4
Total cost is 1 * 4 + 1 * 4 + 1 * 4 = 12
It can be shown that no other mapping can provide a lower cost.
Note that the key 9 is not mapped to any letter: it is not necessary to map letters to every key, but to map all the letters.
```

**Example 3:**

```
Input: word = "aabbccddeeffgghhiiiiii"
Output: 24
Explanation: The remapped keypad given in the image provides the minimum cost.
"a" -> one push on key 2
"b" -> one push on key 3
"c" -> one push on key 4
"d" -> one push on key 5
"e" -> one push on key 6
"f" -> one push on key 7
"g" -> one push on key 8
"h" -> two pushes on key 9
"i" -> one push on key 9
Total cost is 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 2 * 2 + 6 * 1 = 24.
It can be shown that no other mapping can provide a lower cost.
```

**Constraints**

- 1 <= word.length <= 105
- word consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个只包含小写英文字母的字符串 `word`。  
电话键盘（keypad）上的键 2~9 各自映射到若干不相交的字母集合，用户通过按键（push）若干次来输入对应的字母。例如，键 2 映射到 `["a","b","c"]`，输入 `"a"` 需要按一次该键，输入 `"b"` 需要按两次，输入 `"c"` 需要按三次。

现在可以 **重新映射（remap）** 键 2~9 到任意数量的字母，要求每个字母恰好映射到唯一的一个键。求在一次最佳的重新映射后，输入字符串 `word` 所需的最少按键次数，并返回该最小值。

下面给出了电话键盘的一个示例映射（注意键 1、`*`、`#`、0 不映射任何字母）。

---

### 示例

**示例 1**

```
Input: word = "abcde"
Output: 5
Explanation: 如图所示的重新映射能够得到最小费用。
"a" → 在键 2 上按一次
"b" → 在键 3 上按一次
"c" → 在键 4 上按一次
"d" → 在键 5 上按一次
"e" → 在键 6 上按一次
总费用为 1 + 1 + 1 + 1 + 1 = 5。
可以证明没有其他映射能够得到更低的费用。
```

**示例 2**

```
Input: word = "xyzxyzxyzxyz"
Output: 12
Explanation: 如图所示的重新映射能够得到最小费用。
"x" → 在键 2 上按一次
"y" → 在键 3 上按一次
"z" → 在键 4 上按一次
总费用为 1 * 4 + 1 * 4 + 1 * 4 = 12
可以证明没有其他映射能够得到更低的费用。
注意键 9 未映射到任何字母：并非所有键都必须映射字母，
```

**示例 3**

```
Input: word = "aabbccddeeffgghhiiiiii"
Output: 24
Explanation: 如图所示的重新映射能够得到最小费用。
"a" → 在键 2 上按一次
"b" → 在键 3 上按一次
"c" → 在键 4 上按一次
"d" → 在键 5 上按一次
"e" → 在键 6 上按一次
"f" → 在键 7 上按一次
"g" → 在键 8 上按一次
"h" → 在键 9 上按两次
"i" → 在键 9 上按一次
总费用为 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + … = 24
（后续省略的计算过程同理）
```

---

### 约束

- `1 <= word.length <= 10^5`
- `word` 只由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把 26 个字母全部列举所有可能的键位分配**，然后逐个计算敲键次数，取最小值。

- **键位**：电话上可用的键只有 2~9 共 8 个。每个键可以放任意个字母，只要同一个字母只出现一次。
- **敲键次数**：如果某个键上有 `k` 个字母，排在第 `i`（从 1 开始）的位置，则敲这个字母需要 `i` 次。  
  > 类比查字典：键号相当于“书本”，键上的字母顺序相当于“页码”。要找第 3 页的内容，需要翻 3 次页。

**暴力做法**：

1. 生成所有把 26 个字母划分到 8 条键的方式（每种方式都是一个**集合划分**）。  
2. 对每种划分，遍历 `word`，统计每个字母出现的次数，再根据它所在键的位置算出总敲键次数。  
3. 取所有划分中的最小值。

**为什么一定能得到答案**：因为我们枚举了**所有合法的映射**，最优的那一个必然在枚举集合里。

**时间/空间分析**：

- 26 个字母要划分到 8 条键，组合数是 **Stirling 数** `S(26,8)`，大约是 `10^15` 级别，根本不可能在电脑里跑完。  
- 即使我们只枚举一次，就要把所有划分存进内存，空间也会天文数字。

> 大白话：  
> - `O(n²)` 里 `n` 表示问题规模，这里规模是 26，`n²` 已经是 676，远远不够描述实际的 `10^15`。  
> - 实际上暴力解的时间复杂度是 **指数级**，随字母数指数增长，根本不可接受。

#### 代码（Python）

下面的代码仅作演示，**不能在真实数据上运行**（会卡死），请不要把它提交。

```python
import itertools
from collections import Counter

def brute_min_pushes(word: str) -> int:
    # 统计每个字母出现次数
    cnt = Counter(word)               # {'a': 3, 'b': 2, ...}
    letters = list(cnt.keys())        # 最多 26 个

    min_cost = float('inf')
    # 所有把 letters 划分到 8 条键的方式（组合数爆炸！）
    for groups in itertools.product(range(8), repeat=len(letters)):
        # groups[i] 表示第 i 个字母被放到哪一条键（0~7）
        # 检查每条键上的字母顺序随意，这里默认按字母出现顺序排列
        key_to_letters = [[] for _ in range(8)]
        for letter, key in zip(letters, groups):
            key_to_letters[key].append(letter)

        # 计算敲键次数
        cost = 0
        for key_letters in key_to_letters:
            for pos, ch in enumerate(key_letters, start=1):  # 第几次敲
                cost += cnt[ch] * pos
        min_cost = min(min_cost, cost)

    return min_cost
```

#### 复杂度

- 时间复杂度：`O(8^L)`（`L` 为不同字母个数，最坏 26），指数级，实际不可用。  
- 空间复杂度：`O(L)` 用来保存一次划分，极小，但整体算法受时间限制。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于 **枚举所有映射**。我们需要一种不枚举、直接得到最优映射的方法。

观察键位的特性：

1. **每条键的敲击次数是递增的**：同一键上第 1 个字母只需 1 次，第 2 个需要 2 次……  
2. **我们拥有 8 条键**，所以一次可以让 **最多 8 个字母只需 1 次**，再多的字母至少要 2 次，以此类推。  

把这个过程倒着想：**如果把出现次数最多的字母放在“最省力”的位置**，整体敲键次数就会最小。  
这正是典型的 **贪心** 思想：局部最优（把高频字母放在低次数位置）→全局最优。

实现步骤：

1. **统计每个字母在 `word` 中出现的频率**。这一步只需要一次遍历，`O(|word|)`。  
2. **把频率从大到小排序**。字母只有 26 种，排序成本几乎可以忽略（`O(26 log 26)`）。  
3. 按顺序遍历排好序的频率列表，**第 `i` 个字母的敲击次数为 `i // 8 + 1`**。  
   - `i // 8` 表示已经分配了多少整套 8 个键（每套键对应一次额外的敲击），  
   - 加 1 是因为最少要敲一次。  
4. 把 **频率 × 敲击次数** 累加，就是最小的总敲键次数。

> 类比：把 26 本不同的书（频率高的书更常被借）放进 8 条书架。每条书架的第一层可以直接拿到（只需一次），第二层需要先翻一次（两次），……我们当然把最常被借的书放在最容易拿的层。

#### 代码（Python）

```python
from collections import Counter

def minPushes(word: str) -> int:
    """
    返回重新映射键盘后，敲出 word 所需的最少次数。
    思路：贪心——把出现频率高的字母放在“敲一次”位置，依次类推。
    """
    # 1. 统计每个字母出现的次数
    freq = Counter(word)                # 例如 {'a': 5, 'b': 2, ...}

    # 2. 把频率从大到小排好序（只要 26 个数，开销很小）
    counts = sorted(freq.values(), reverse=True)

    total = 0
    for i, c in enumerate(counts):
        # 第 i 个字母对应的敲击次数 = 已经用了多少整套 8 键 + 1
        pushes = i // 8 + 1
        total += c * pushes              # 频率 × 敲击次数

    return total
```

**关键行解释**：

- `i // 8 + 1`：整数除法 `//` 把下标 `i` 按每 8 个一组分块；第一组（`i=0~7`）得到 `1` 次敲击，第二组得到 `2` 次，依此类推。
- `c * pushes`：如果字母 `c` 出现了 10 次，而它被放在需要 2 次敲击的位置，那么这 10 次一共需要 `10 * 2 = 20` 次敲键。

#### 复杂度

- 时间复杂度：`O(|word| + 26 log 26)` → 实际上就是 `O(|word|)`，因为 `|word|`（最多 10⁵）远大于 26。  
  - 大白话：我们只遍历一次字符串（线性），再做一次极小的排序，整体快得像闪电。  
- 空间复杂度：`O(1)`（只用到 26 个计数器和几个临时变量），与输入大小无关。

---

## 心得

- **核心技巧**：**贪心 + 频率排序**。把“最常出现的东西”放到“最省力的位置”。  
- **适用的题型**  
  1. **键盘/遥控器映射类**（如 LeetCode 1160 “Find Words That Can Be Formed by Characters”）。  
  2. **任务调度/机器分配**，需要把高权重任务分配到低成本机器。  
  3. **压缩编码**（如 Huffman 编码的思路），也是把高频放在短码上。  
- **一句话总结解题钥匙**：**把频率最高的字母排在最前面的 8 个位置，随后依次往后排**。

---

## 反思

- **第一反应**：想到把所有字母随意分配到键上，枚举所有可能。  
- **最容易踩的坑**  
  - 忘记每条键可以放 **任意数量** 的字母，只要不重复；所以不必把所有 26 个字母平均分到 8 条键。  
  - 边界：`word` 只有一种字母时，只需要一次敲击；`word` 包含所有 26 个字母时，后面的字母会被分配到第 4 次甚至第 5 次敲击，需要正确使用 `i // 8 + 1`。  
- **下次遇到同类题**：第一步立刻想到 **统计频率 → 按频率排序 → 用最小的“成本”分配**，而不是去枚举或做复杂的 DP。这样可以迅速把问题转化为“把大数放在小系数上”的贪心模型。