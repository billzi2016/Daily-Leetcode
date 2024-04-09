# #2645. 使字符串有效的最少插入字符数 / Minimum Additions to Make Valid String

> 难度：中等 · 标签：String、Dynamic Programming、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-additions-to-make-valid-string/)

---

## 题目（英文原版）

**Description**

Given a string word to which you can insert letters "a", "b" or "c" anywhere and any number of times, return the minimum number of letters that must be inserted so that word becomes valid.
A string is called valid if it can be formed by concatenating the string "abc" several times.

**Examples**

**Example 1:**

```
Input: word = "b"
Output: 2
Explanation: Insert the letter "a" right before "b", and the letter "c" right next to "b" to obtain the valid string "abc".
```

**Example 2:**

```
Input: word = "aaa"
Output: 6
Explanation: Insert letters "b" and "c" next to each "a" to obtain the valid string "abcabcabc".
```

**Example 3:**

```
Input: word = "abc"
Output: 0
Explanation: word is already valid. No modifications are needed.
```

**Constraints**

- 1 <= word.length <= 50
- word consists of letters "a", "b" and "c" only.

---

## 题目（中文翻译）

给定一个字符串 `word`，你可以在任意位置插入任意次数的字符 **"a"、"b"** 或 **"c"**，返回必须插入的最少字符数，使得 `word` 变为**有效字符串（valid string）**。  
如果一个字符串可以通过多次**拼接（concatenating）**字符串 **"abc"** 而得到，则称其为**有效**。

#### 示例

**示例 1**  
**输入**: `word = "b"`  
**输出**: `2`  
**解释**: 在 `"b"` 前插入字符 `"a"`，在 `"b"` 后插入字符 `"c"`，得到有效字符串 `"abc"`。

**示例 2**  
**输入**: `word = "aaa"`  
**输出**: `6`  
**解释**: 在每个 `"a"` 后依次插入字符 `"b"` 和 `"c"`，得到有效字符串 `"abcabcabc"`。

**示例 3**  
**输入**: `word = "abc"`  
**输出**: `0`  
**解释**: `word` 本身已经是有效的，无需任何修改。

#### 约束条件

- `1 <= word.length <= 50`
- `word` 仅由字符 **"a"、"b"、"c"** 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把原字符串 `word` 和目标模式 `"abcabc…"` 对齐**，  
只要出现不匹配，就往 `word` 里插入缺少的字符。  

> **类比**：把 `"abc"` 想成一本字典，  
> - 词条（`key`）是 `"a"、"b"、"c"`，  
> - 页码（`value`）是它们在一个完整的 `"abc"` 循环中的位置 0、1、2。  
> 我们要把手里的单词（`word`）顺序对应到这本字典的页码上。  
> 当手里的字母和字典的当前页码不一致时，就“补一本缺失的页”（插入字符），  
> 然后继续往后翻页（移动指针）。  

暴力实现可以用 **递归+记忆化**（或直接的递归）来枚举所有可能的插入方式：

1. 维护两个指针  
   * `i`：指向 `word` 中当前要处理的字符  
   * `j`：指向模式串 `"abc"` 中当前要匹配的字符（`j∈{0,1,2}`）  
2. 若 `i` 已经到达 `word` 末尾，只需要把剩余的模式字符全部插入，返回插入数。  
3. 否则比较 `word[i]` 与 `pattern[j]`（`pattern = "abc"`）  
   * **相等** → 两指针都向前走，不需要插入。  
   * **不相等** → 必须在 `word` 前插入 `pattern[j]`，插入计数+1，只移动模式指针 `j`（因为我们刚刚“补上”了这个字符），`i` 仍然停在原位。  
4. 对所有递归分支取最小值，即为答案。  

这种做法会把每一步的“插还是不插”都列举一遍，最坏情况下会产生 **指数级** 的递归树（每个字符都可能导致一次插入），因此只能算是概念性的 **暴力解**，用来帮助我们理清问题的本质。

#### 代码（Python）

```python
def minInsertions_bruteforce(word: str) -> int:
    pattern = "abc"
    n = len(word)

    # 记忆化表，避免相同 (i, j) 重复计算
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(i: int, j: int) -> int:
        """
        i : 当前在 word 中的位置 (0~n)
        j : 当前在 pattern 中的位置 (0,1,2)
        返回把 word[i:] 变成合法串需要的最少插入数
        """
        # 1. word 已经遍历完，只剩 pattern 的后缀需要补齐
        if i == n:
            # 还差多少字符才能走完一个完整的 "abc"？
            # 例如 j==1 表示已经匹配到 "b"，还需要插入 "c"
            return (3 - j) % 3

        # 2. 取当前字符进行比较
        if word[i] == pattern[j]:
            # 匹配成功，两个指针都向前走
            return dfs(i + 1, (j + 1) % 3)
        else:
            # 不匹配，必须在 word 前面插入 pattern[j]
            # 插入一次后，模式指针向前走，word 指针不动
            return 1 + dfs(i, (j + 1) % 3)

    return dfs(0, 0)
```

> **关键行中文注释**  
> - `@lru_cache`：把已经算过的 `(i, j)` 结果存起来，防止重复递归（相当于“记忆化”）。  
> - `if i == n`：当遍历完原串时，只剩下把当前的 `"abc"` 循环写完整。  
> - `if word[i] == pattern[j]`：字符相等，直接匹配；否则插入缺失的字符并计数。

#### 复杂度  

- **时间复杂度**：`O(3^n)`（指数级），因为每个字符都可能导致一次插入，递归树会呈指数增长。  
  实际上加了记忆化后，状态只有 `n * 3` 种，时间降到 `O(n·3)`，但这已经不再是“最原始的暴力”。  
- **空间复杂度**：`O(n·3)` 用于递归栈和记忆化表，最坏情况下等于 `O(n)`。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出：**唯一需要考虑的自由度是**  
> “当前 `word[i]` 与模式 `pattern[j]` 是否相等”。  

如果相等，直接向前匹配；如果不等，我们 **只能** 在 `word` 前面插入缺失的 `pattern[j]`，因为题目不允许删除或替换字符。  

因此，整个过程可以 **一次遍历** 完成，不需要回溯或记忆化——这正是 **贪心** 思想的体现：

1. 设 `i` 为遍历 `word` 的指针，`j` 为模式指针（取值 0、1、2，分别对应 `'a'、'b'、'c'`）。  
2. 当 `i < len(word)`：  
   * 若 `word[i] == pattern[j]` → 匹配成功，`i += 1, j = (j + 1) % 3`。  
   * 否则 → 必须插入 `pattern[j]`，计数 `ans += 1`，仅让 `j` 前进 `j = (j + 1) % 3`（因为我们已经“补上”了这个字符），`i` 仍停留在原位，等待后面真正的字符来匹配下一个模式位置。  
3. 循环结束后，`i` 已经指向 `word` 末尾，但 `j` 可能还停在 `'a'`、`'b'` 或 `'c'` 的中间位置。此时需要把剩余的模式字符补齐，插入数为 `(3 - j) % 3`。  

这就是 **线性贪心**：每一次都做“当前最合理的插入”，因为唯一的选择只有“插还是不插”。插入后不影响后面的匹配顺序，保证全局最优。

> **类比**：把 `"abc"` 看成一条跑道，跑道上有三个站点 A、B、C 循环。  
> 你手里拿着一串标签（`word`），要把它们依次放到跑道上。  
> - 如果手中标签恰好是当前站点的颜色，就直接放下，跑到下一个站点。  
> - 否则只能在跑道上先补一个对应颜色的标签（插入），再继续检查手中的标签。  
> 这样跑完所有手中标签后，跑道自然会停在某个站点，剩余的空位再补完即可。

#### 代码（Python）

```python
def minInsertions(word: str) -> int:
    """
    贪心线性扫描 O(n) 解法
    """
    pattern = "abc"
    ans = 0          # 记录需要插入的字符数
    j = 0            # 模式指针，0->'a', 1->'b', 2->'c'

    for ch in word:          # 逐字符遍历 word
        if ch == pattern[j]:
            # 匹配成功，两个指针都向前走
            j = (j + 1) % 3
        else:
            # 不匹配，需要在前面插入 pattern[j]
            ans += 1
            # 插入后，模式指针前进，当前字符仍待匹配
            j = (j + 1) % 3
            # 这里不移动 word 的指针，因为 ch 仍然需要与下一个模式字符比较

    # 循环结束后，可能还剩下未完成的 "abc" 部分
    ans += (3 - j) % 3
    return ans
```

> **关键行中文注释**  
> - `for ch in word:`：一次遍历原串。  
> - `if ch == pattern[j]:`：相等则直接匹配。  
> - `else:`：不相等时插入缺失字符并计数。  
> - `ans += (3 - j) % 3`：把最后一个不完整的 `"abc"` 补齐。

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串，`n = len(word)`。  
  > **含义**：即使 `word` 长达 50（题目上限），最多也只会执行 50 次循环，几乎瞬间得到答案。  
- **空间复杂度**：`O(1)`，只使用了若干个整数变量，和字符串长度无关。  
  > 与暴力解相比，省去了递归栈和记忆化表，真正做到“常数空间”。

---

## 心得  

- **核心技巧**：**贪心 + 循环匹配**。  
  把目标模式看成无限循环的 `"abc"`，始终让指针保持在正确的相位上，一旦出现不匹配就立即插入缺失字符。  
- **适用的题型**（类似思路）  
  1. *“删除最少字符使字符串成为某固定模式的重复”*（如 `abab…`、`xyzxyz…`）。  
  2. *“最少插入使字符串成为回文”*（也可以用双指针贪心或 DP）。  
  3. *“最少插入使字符串满足特定顺序约束”*（如 `a…b…c` 的相对顺序）。  
- **一句话总结解题钥匙**：  
  **“把目标模式当作循环跑道，遇到不匹配就立即补齐当前跑道站点”。**

---

## 反思  

- **第一反应**：把问题抽象为“把 `word` 对齐到无限长的 `'abc'` 序列”，想到可以用指针同步遍历。  
- **最容易踩的坑**  
  1. **忘记处理尾部残余**：遍历完 `word` 后，模式指针可能停在 `'a'` 或 `'b'`，需要再补齐剩余的字符。  
  2. **插入后指针错误**：插入字符后只能让模式指针前进，**不能**把 `word` 指针也向前走，否则会漏掉当前字符的匹配机会。  
  3. **边界情况**：空串（虽然题目最短为 1）和全是同一字符的情况，都能通过上述公式统一处理。  
- **下次遇到同类题**，第一步应该问自己：  
  *“是否可以把目标结构看成一个固定循环/顺序？”*  
  若答案是“是”，则尝试用 **指针同步 + 必要时立即补齐** 的贪心方式求解。