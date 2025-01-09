# #3014. 键入单词的最少按键次数 I / Minimum Number of Pushes to Type Word I

> 难度：简单 · 标签：Math、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-i/)

---

## 题目（英文原版）

**Description**

You are given a string word containing distinct lowercase English letters.
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
Input: word = "xycdefghij"
Output: 12
Explanation: The remapped keypad given in the image provides the minimum cost.
"x" -> one push on key 2
"y" -> two pushes on key 2
"c" -> one push on key 3
"d" -> two pushes on key 3
"e" -> one push on key 4
"f" -> one push on key 5
"g" -> one push on key 6
"h" -> one push on key 7
"i" -> one push on key 8
"j" -> one push on key 9
Total cost is 1 + 2 + 1 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = 12.
It can be shown that no other mapping can provide a lower cost.
```

**Constraints**

- 1 <= word.length <= 26
- word consists of lowercase English letters.
- All letters in word are distinct.

---

## 题目（中文翻译）

给定一个只包含不同小写英文字母的字符串 `word`。  
电话键盘（telephone keypad）上的按键 2~9 各对应一组不同的小写字母，按同一个键多次即可得到该组中的不同字母。例如，键 2 映射到 `["a","b","c"]`，输入 `"a"` 需要按一次键 2，输入 `"b"` 需要按两次键 2，输入 `"c"` 需要按三次键 2。  

可以将键 2~9 重新映射为任意不相交的字母集合，每个字母必须恰好映射到一个键，且每个键可以映射任意数量的字母。求在重新映射后，输入字符串 `word` 所需的最小按键次数。  

返回重新映射键盘后，输入 `word` 所需的最少按键次数。  

下面给出一种电话键盘的映射示例（注意键 1、`*`、`#`、0 不映射任何字母）。

**示例 1**  
**示例 2**  

**约束条件**

- `1 <= word.length <= 26`
- `word` 仅由小写英文字母组成
- `word` 中的所有字母均互不相同  

**示例**

**示例 1**  
```
Input: word = "abcde"
Output: 5
Explanation: 如图所示的重新映射键盘能够达到最小代价。
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
Input: word = "xycdefghij"
Output: 12
Explanation: 如图所示的重新映射键盘能够达到最小代价。
"x" → 在键 2 上按一次  
"y" → 在键 2 上按两次  
"c" → 在键 3 上按一次  
"d" → 在键 3 上按两次  
"e" → 在键 4 上按一次  
"f" → 在键 5 上按一次  
"g" → 在键 6 上按一次  
"h" → 在键 7 上按一次  
"i" → 在键 8 上按一次  
"j" → 在键 9 上按一次  
总费用为 1 + 2 + 1 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = 12。  
（后续内容已截断）  
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每个字母** 随意分配到 **键 2~9** 上的某个位置，然后逐个算出打字的次数，取最小值。  
- **键盘** 可以看成 8 把抽屉（键 2~9），每把抽屉里可以放任意数量的字母。  
- **抽屉里的第 k 个字母** 需要按键 k 次才能输入（类似把字典的第 k 页翻到手指要点几次）。  

暴力做法就是遍历 **所有可能的分配方式**，计算每种方式的总按键次数，最后取最小值。  

> **为什么它是对的？**  
> 因为我们枚举了所有合法的映射，必然会包括最优的那一种，所以最小值一定是正确答案。  

> **复杂度分析**  
> - 设单词长度为 `n`（`1 ≤ n ≤ 26`），每个字母可以放到 8 把抽屉的任意位置。  
> - 把 `n` 个字母排成顺序再决定每个字母所在的抽屉，等价于把 `n` 个元素分配到 8 类，**组合数是 8ⁿ**。  
> - 因此时间复杂度是 **O(8ⁿ)**，指数级增长，几乎不可能在合理时间内跑完。  
> - 只需要保存当前的最小值，空间复杂度是 **O(1)**。  

显然，这种“全枚举”只适合极小的 `n`，在本题的最坏情况下（`n=26`）根本不可行。  

#### 代码（Python）  

```python
import itertools

def minPushes_bruteforce(word: str) -> int:
    # 所有字母
    letters = list(word)
    n = len(letters)
    best = float('inf')

    # 把 8 把键编号为 0~7，键 i 上的第 k 个字母需要按 (k+1) 次
    # 为了暴力遍历，这里把每个字母映射为 (key_index, position_on_key)
    # 位置从 0 开始计数，实际按键次数 = position + 1
    for assign in itertools.product(range(8), repeat=n):
        # 统计每把键上已经放了多少字母
        cnt_on_key = [0] * 8
        total = 0
        for idx, key in enumerate(assign):
            pos = cnt_on_key[key]          # 这把键已经有多少字母
            total += pos + 1               # 本字母需要按 (pos+1) 次
            cnt_on_key[key] += 1
        best = min(best, total)

    return best
```

> **注意**：上述代码只能在 `n` 极小（比如 `n≤5`）时跑得完，**仅作思路展示**，实际提交会超时。

#### 复杂度  

- **时间复杂度**：`O(8ⁿ)`，指数级增长，`n` 增大几乎立即失去可行性。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们把每个字母的具体位置都枚举了。  
实际上，**字母出现的次数** 决定了它应该放在键盘的哪个“层”。  

本题的特殊条件：  

1. 单词里所有字母 **互不相同**，即每个字母只出现一次。  
2. 我们拥有 **8 把键**（2~9），每把键的第 1、2、3… 个字母对应的按键次数分别是 1、2、3…  

因此，要让总按键次数最小，只需要把**按键次数最少的“位子”**分配给**字母**，不必关心具体是哪把键。  
可以把所有可能的位子想成一个从小到大的序列：

```
1 次  → 8 个位置（每把键的第 1 个字母）
2 次  → 8 个位置（每把键的第 2 个字母）
3 次  → 8 个位置
...
```

把单词的字母数 `n` 按这个序列依次取位子，累加对应的次数即可。  

> **核心概念：贪心**  
> 把“成本最小的资源”先分配给“需求”，这里的资源是“按键次数”，需求是每个字母（出现一次）。因为每个字母的需求相同（都只需要一次），把最便宜的位子先用完，剩下的再用更贵的位子，显然能得到全局最优。

**实现步骤**  

1. 计算单词长度 `n`。  
2. 对 `i` 从 `0` 到 `n-1`（遍历每个字母），它在排序好的位子序列中的下标是 `i`。  
3. 该字母对应的按键次数 = `i // 8 + 1`（整除 8 表示它在第几层，层号+1 即为按键次数）。  
4. 把所有次数加起来，即为答案。  

> 如果题目没有“字母互不相同”这一限制，只需要先统计每个字母出现的频率，然后把频率从大到小排序，再按同样的位子序列乘以频率求和即可——思路完全相同，只是多了一步排序。

#### 代码（Python）  

```python
def minPushes(word: str) -> int:
    """
    返回在最佳映射下输入 word 所需的最小按键次数。
    思路：把 8 把键的第 1、2、3… 个位置视为成本 1、2、3… 的资源，
          按成本从低到高依次分配给字母（每个字母出现一次）。
    """
    n = len(word)                # 单词中不同字母的数量
    total = 0
    for i in range(n):
        pushes = i // 8 + 1      # 第 i 个字母对应的按键次数
        total += pushes
    return total
```

> **关键行解释**  
> - `i // 8 + 1`：`i // 8` 表示第几层（从 0 开始），加 1 得到实际需要的按键次数。  
> - 由于 `i` 从 0 开始递增，前 8 个字母 (`i = 0~7`) 都得到 `1` 次，接下来的 8 个得到 `2` 次，依此类推。

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次单词，`n ≤ 26`，几乎瞬间完成。  
- **空间复杂度**：`O(1)`，只用了几个整数变量。  

相比暴力的指数级时间，这里是线性时间，毫秒级即可运行。

---

## 心得  

- **核心技巧**：**贪心分配**——把“成本最低的资源”先用完。  
- **适用题型**  
  1. **键盘打字类**（如本题、`Minimum Number of Pushes to Type Word II`）。  
  2. **按权重分配资源**（如 `Maximum Sum of Selected Elements`、`Assign Cookies`）。  
  3. **分层计数**（如 `Minimum Number of Moves to Seat Everyone`）。  
- **一句话总结**：把所有可能的“按键次数”从小到大排好序，依次给字母配位子，即是最小总耗时。  

---

## 反思  

- **第一反应**：想到要把每个字母映射到键盘上，先尝试全枚举所有映射。  
- **最容易踩的坑**  
  1. **忽略键的数量**：键盘只有 8 把键（2~9），不能随意假设有无限键。  
  2. **忘记字母互不相同**：若误以为字母可以重复出现，需要先统计频率再排序。  
  3. **边界条件**：当 `word` 长度恰好是 8、16、24 等时，`i // 8 + 1` 正好切换层次，代码仍需保持正确。  
- **下次类似题的第一步**：先问自己“资源（键位）有多少层、每层的容量是多少”，再把需求（字母出现次数）按从大到小（或相同）配到最便宜的层上。这样可以快速定位贪心或排序的方向，避免盲目枚举。