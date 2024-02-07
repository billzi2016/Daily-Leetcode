# #2573. 寻找满足 LCP 矩阵的字符串 / Find the String with LCP

> 难度：困难 · 标签：Array、String、Dynamic Programming、Greedy、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-string-with-lcp/)

---

## 题目（英文原版）

**Description**

We define the lcp matrix of any 0-indexed string word of n lowercase English letters as an n x n grid such that:
Given an n x n matrix lcp, return the alphabetically smallest string word that corresponds to lcp. If there is no such string, return an empty string.
A string a is lexicographically smaller than a string b (of the same length) if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b. For example, "aabd" is lexicographically smaller than "aaca" because the first position they differ is at the third letter, and 'b' comes before 'c'.

**Examples**

**Example 1:**

```
Input: lcp = [[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]]
Output: "abab"
Explanation: lcp corresponds to any 4 letter string with two alternating letters. The lexicographically smallest of them is "abab".
```

**Example 2:**

```
Input: lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,1]]
Output: "aaaa"
Explanation: lcp corresponds to any 4 letter string with a single distinct letter. The lexicographically smallest of them is "aaaa".
```

**Example 3:**

```
Input: lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,3]]
Output: ""
Explanation: lcp[3][3] cannot be equal to 3 since word[3,...,3] consists of only a single letter; Thus, no answer exists.
```

**Constraints**

- 1 <= n == lcp.length == lcp[i].length <= 1000
- 0 <= lcp[i][j] <= n

---

## 题目（中文翻译）

我们将任意一个下标从 0 开始、由 **n** 个小写英文字母组成的字符串 **word** 的 **最长公共前缀（LCP）矩阵** 定义为一个 **n × n** 的网格，使得第 **i** 行第 **j** 列的值等于 **word[i…]** 与 **word[j…]** 的最长公共前缀长度。

给定一个 **n × n** 矩阵 **lcp**，返回与 **lcp** 对应的字典序（lexicographically）最小的字符串 **word**。如果不存在满足条件的字符串，返回空字符串 `""`。

**字典序**（lexicographically）比较：若两个等长字符串 **a** 与 **b** 在首次出现不同的字符位置，**a** 的该字符在字母表中出现得更早，则 **a** 的字典序小于 **b**。例如，`"aabd"` 的字典序小于 `"aaca"`，因为它们在第三个字符不同，`'b'` 在 `'c'` 之前。

### 示例

**示例 1**

```
Input: lcp = [[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]]
Output: "abab"
Explanation: 该 LCP 矩阵对应所有形如交替出现两种字母的 4 位字符串。字典序最小的是 `"abab"`。
```

**示例 2**

```
Input: lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,1]]
Output: "aaaa"
Explanation: 该 LCP 矩阵对应所有只含单一字符的 4 位字符串。字典序最小的是 `"aaaa"`。
```

**示例 3**

```
Input: lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,3]]
Output: ""
Explanation: `lcp[3][3]` 不可能等于 3，因为 `word[3…3]` 只包含一个字符；因此不存在满足条件的字符串。
```

### 约束条件

- `1 ≤ n == lcp.length == lcp[i].length ≤ 1000`
- `0 ≤ lcp[i][j] ≤ n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的字符串都列举出来，逐个验证它们是否能够产生给定的 `lcp` 矩阵**。  

- **枚举方式**：长度为 `n` 的字符串，每个位置可以放 `'a' … 'z'` 共 26 种字母。于是所有候选字符串的数量是 `26ⁿ`（相当于把 26 本字典的每一页都翻遍）。  
- **验证过程**：对每个候选字符串，按照下面的递推公式计算它自己的 LCP 矩阵  

```
if i == n or j == n:   dp[i][j] = 0
elif s[i] == s[j]:     dp[i][j] = 1 + dp[i+1][j+1]
else:                  dp[i][j] = 0
```

  然后把得到的矩阵和题目给出的 `lcp` 做逐格比较，完全相同则说明找到了合法的字符串。  

- **为什么能得到正确答案**：只要遍历了**所有**可能的字符串，就一定会碰到满足约束的那一个（如果存在的话），因此必然能得到答案或确认不存在。

#### 代码（Python）

```python
import itertools

def brute(lcp):
    n = len(lcp)

    # 递归计算字符串 s 的 LCP 矩阵，返回二维列表
    def build_lcp(s):
        dp = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if s[i] == s[j]:
                    dp[i][j] = 1 + (dp[i + 1][j + 1] if i + 1 < n and j + 1 < n else 0)
                else:
                    dp[i][j] = 0
        return dp

    # 逐个枚举所有长度为 n、只用 a~z 的字符串
    for chars in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=n):
        s = ''.join(chars)                     # 生成候选字符串
        if build_lcp(s) == lcp:                # 与目标矩阵逐格比较
            return s                          # 找到最小的（因为枚举顺序本身是字典序）
    return ""                                 # 没有合法答案
```

> **关键行中文注释**  
> - `itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=n)`：相当于把 26 本字典的每一页都翻遍，生成所有可能的组合。  
> - `build_lcp(s)`：用“如果两个字符相同就往后看一格”这种递推，像在纸上手工算 LCP 那样。  

#### 复杂度  

- **时间复杂度**：`O(26ⁿ · n²)`  
  - `26ⁿ` 是所有可能字符串的数量，`n²` 是每次验证时要算的 LCP 矩阵大小。  
  - 用大白话说，就是“先把所有 26ⁿ 本书都翻完，再把每本书的每一页（n²格）都核对一遍”。  
- **空间复杂度**：`O(n²)`  
  - 只需要保存一个 `n × n` 的临时矩阵，和枚举时的 `O(n)` 字符串。

> 这显然在 `n ≤ 1000` 时根本不可行，只能当作“思考起点”。  

---  

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **“枚举所有可能的字符”**——这一步的搜索空间太大。  
其实我们并不需要去尝试每一种字符，只要弄清 **哪些位置的字符必须相同**，再把它们分配最小的字母即可。  

**核心步骤**：

1. **从 LCP 矩阵推出相等关系**  
   - 对任意 `i, j`，如果 `lcp[i][j] > 0`，说明下标 `i` 和 `j` 处的字符一定相同（因为它们的最长公共前缀至少有 1 个字符）。  
   - 这是一条 **等式约束**，可以用 **并查集（Union‑Find）** 把这些下标归到同一个集合。  
   - 并查集就像是“查字典”，每个下标是单词，集合的根节点是词典页码，`union(a,b)` 就是把两个单词放到同一页。

2. **检查基本合法性**  
   - 对角线 `lcp[i][i]` 必须等于剩余长度 `n‑i`（因为一个后缀和它自己最长公共前缀就是整个后缀）。  
   - 任意 `lcp[i][j]` 不能超过 `min(n‑i, n‑j)`。  
   - 这两条如果不满足，直接返回空串。

3. **给每个集合分配字母**  
   - 把所有集合按照 **最小下标** 从小到大排序。因为字典序要求“最左边的字符尽可能小”。  
   - 按顺序依次给集合分配 `'a'、'b'、'c' …`。如果集合数量超过 26（英文字母数），说明根本无法用不同字母来区分，返回空串。

4. **构造字符串并二次验证**  
   - 根据每个位置所在集合的字母，得到候选字符串 `word`。  
   - 再用上面递推公式 **重新计算** 这条字符串的 LCP 矩阵 `calc`，与题目给出的 `lcp` 完全相等才算合法。  
   - 之所以要二次验证，是因为仅仅利用 `lcp[i][j] > 0` 合并集合只能保证“首字符相等”，而更长的公共前缀还可能产生 **不一致**（例如示例 3），只有完整的矩阵对比才能捕捉这些细节。

**为什么快**：

- **并查集**的 `union`/`find` 操作几乎是 `O(α(n))`（α 为极慢增长的反阿克曼函数），对所有 `i,j`（共 `n²` 对）遍历一次即可，整体是 **`O(n²)`**。  
- 重新计算 LCP 也只需要一次 `O(n²)` 的 DP。  
- 与暴力的 `26ⁿ` 成指数级差距相比，`n ≤ 1000` 时 `n² = 10⁶` 完全可接受。

下面把每一步细化并配上代码。

#### 代码（Python）

```python
from typing import List

# ---------- 并查集（Union‑Find） ----------
class DSU:
    def __init__(self, n: int):
        self.par = list(range(n))          # 父节点数组，初始每个下标自成一组
        self.sz = [1] * n                  # 组的大小，可选

    def find(self, x: int) -> int:
        # 路径压缩：把查到的每个节点直接挂到根上，加速后续查询
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按大小合并，保持树尽量平衡
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.par[rb] = ra
        self.sz[ra] += self.sz[rb]

# ---------- 主函数 ----------
def findTheString(lcp: List[List[int]]) -> str:
    n = len(lcp)

    # 1. 基础合法性检查
    for i in range(n):
        # 对角线必须等于后缀长度
        if lcp[i][i] != n - i:
            return ""
        for j in range(n):
            # 任何格子都不能超过各自后缀的长度
            if lcp[i][j] > min(n - i, n - j):
                return ""

    # 2. 用并查集合并“首字符相等”的下标
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):          # 只看上三角，省一半
            if lcp[i][j] > 0:              # 说明 word[i] == word[j]
                dsu.union(i, j)

    # 3. 收集每个集合的成员以及最小下标
    groups = {}                            # root -> [成员列表]
    for idx in range(n):
        root = dsu.find(idx)
        groups.setdefault(root, []).append(idx)

    # 4. 按最小下标排序，给每组分配字母
    sorted_groups = sorted(groups.values(), key=lambda lst: min(lst))
    if len(sorted_groups) > 26:            # 超过 26 种字母无法分配
        return ""

    char_of_root = {}                      # root -> 分配的字符
    for i, members in enumerate(sorted_groups):
        ch = chr(ord('a') + i)             # 第 i 组得到第 i 个字母
        root = dsu.find(members[0])
        char_of_root[root] = ch

    # 5. 根据分配结果生成字符串
    word = [''] * n
    for i in range(n):
        root = dsu.find(i)
        word[i] = char_of_root[root]
    word = ''.join(word)

    # 6. 重新计算 LCP 矩阵并与输入比较（完整验证）
    calc = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if word[i] == word[j]:
                calc[i][j] = 1 + (calc[i + 1][j + 1] if i + 1 < n and j + 1 < n else 0)
            else:
                calc[i][j] = 0

    if calc == lcp:
        return word
    return ""                               # 矩阵不匹配，说明原矩阵不合法

# ---------- 示例 ----------
if __name__ == "__main__":
    examples = [
        ([[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]], "abab"),
        ([[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,1]], "aaaa"),
        ([[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,3]], ""),
    ]
    for mat, ans in examples:
        print(findTheString(mat), "==", ans)
```

> **代码要点中文注释**  
> - `DSU` 类：把“下标”当成字典里的单词，用 `find` 找到它所在的“页码”。  
> - 第 1 步的对角线检查相当于确认每本书的“封面页数”是否正确。  
> - 第 2 步只看上三角 (`j > i`) 是因为 `lcp` 对称，省一半比较。  
> - 第 4 步把“最左边的页”排在前面，保证字典序最小。  
> - 第 6 步的 `calc` 就是“用新写好的单词重新翻页，看看每页的公共前缀长度是否和原来的一模一样”。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层 `for i,j` 循环遍历矩阵（`n²` 次）进行合法性检查与并查集合并。  
  - 再一次 `O(n²)` 的 DP 用来重新计算 LCP。  
  - 相比暴力的指数级时间，`n = 1000` 时大约只需要几百万次基本操作，完全在 1 秒以内。  

- **空间复杂度**：`O(n²)`  
  - 需要存储输入矩阵（题目已经给出）以及重新计算的 `calc` 矩阵。  
  - 并查集只占 `O(n)`，整体仍是 `O(n²)`。  

> 与暴力的 `O(26ⁿ·n²)` 相比，`O(n²)` 是线性的提升，真正可以在机器上跑通。

---  

## 心得  

- **核心技巧**：**利用 LCP 矩阵的“首字符相等”信息构造等价类（并查集），再按最左下标分配最小字母**。  
- **适用场景**：  
  1. **相等约束类字符串题**（例如 LeetCode 1625 “Lexicographically Smallest String After Swaps”）。  
  2. **需要从矩阵/表格推导出字符关系的题**（例如 “Construct the String from its Pairwise Distance Matrix”。）  
  3. **任何出现 “某些位置必须相同” 的离散约束，都可以尝试并查集**。  

- **一句话总结解题钥匙**：  
  *“把 LCP 矩阵转化为‘哪些位置必须共用同一个字母’，先把这些位置聚成组，再把组按出现顺序分配最小的字母”。*  

---  

## 反思  

- **第一反应**：看到 LCP 矩阵，就想到“最长公共前缀”是逐字符比较的结果，先想把矩阵直接逆向构造字符串，结果一开始想遍历所有字符组合（暴力）。  
- **最容易踩的坑**：  
  - **对角线不符合 `n‑i`**：容易忽略，导致后面所有检查都失效。  
  - **仅靠 `lcp[i][j] > 0` 合并可能不够**：需要最终的完整矩阵校验，否则会出现示例 3 那种“局部看起来合法，整体冲突”的情况。  
  - **字母种类不足**：若等价类数量超过 26，需要及时返回空串，防止后面出现 IndexError。  
- **下次类似题的第一步**：  
  *先把“相等关系”抽象出来，用并查集或图的连通分量把相等的下标聚在一起，再检查是否还能满足全部约束*。这样可以把搜索空间从指数级压缩到多项式级。