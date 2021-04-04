# #1286. 组合迭代器 / Iterator for Combination

> 难度：中等 · 标签：String、Backtracking、Design、Iterator · [LeetCode 链接](https://leetcode.com/problems/iterator-for-combination/)

---

## 题目（英文原版）

**Description**

Design the CombinationIterator class:

**Examples**

**Example 1:**

```
Input
["CombinationIterator", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[["abc", 2], [], [], [], [], [], []]
Output
[null, "ab", true, "ac", true, "bc", false]

Explanation
CombinationIterator itr = new CombinationIterator("abc", 2);
itr.next();    // return "ab"
itr.hasNext(); // return True
itr.next();    // return "ac"
itr.hasNext(); // return True
itr.next();    // return "bc"
itr.hasNext(); // return False
```

**Constraints**

- 1 <= combinationLength <= characters.length <= 15
- All the characters of characters are unique.
- At most 104 calls will be made to next and hasNext.
- It is guaranteed that all calls of the function next are valid.

---

## 题目（中文翻译）

设计一个 `CombinationIterator` 类，使其能够按字典序（lexicographic order）遍历给定字符串 `characters` 中所有长度为 `combinationLength` 的组合（combination）。

- 构造函数 `CombinationIterator(characters, combinationLength)` 初始化迭代器，其中 `characters` 只包含唯一的字符，且已按升序排列。
- 方法 `next()` 返回字典序中的下一个组合字符串。
- 方法 `hasNext()` 返回布尔值，表示是否仍有未遍历的组合。

**示例**

```json
Input
["CombinationIterator", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[["abc", 2], [], [], [], [], [], []]
Output
[null, "ab", true, "ac", true, "bc", false]
```

**解释**
```java
CombinationIterator itr = new CombinationIterator("abc", 2);
itr.next();    // 返回 "ab"
itr.hasNext(); // 返回 True
itr.next();    // 返回 "ac"
itr.hasNext(); // 返回 True
itr.next();    // 返回 "bc"
itr.hasNext(); // 返回 False
```

**约束条件**
- `1 <= combinationLength <= characters.length <= 15`
- `characters` 中的所有字符互不相同，并已按升序排列。
- 最多调用 `next` 和 `hasNext` 共计 `10^4` 次。
- 保证对 `next` 的所有调用都是合法的（即在调用 `next` 前一定会返回 `true` 的 `hasNext`）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次性把所有合法的组合全部列出来**，然后让迭代器只负责在这份列表上移动指针。  

- **数据结构**：用一个 Python `list` 保存所有组合字符串。  
  - `list` 就像一本已经排好序的“组合词典”，每个元素（词）就是一个合法的组合。  
- **生成组合**：使用 **回溯（Backtracking）**，从左到右依次挑选字符，直到挑够 `combinationLength` 个。  
  - 回溯过程可以类比为“走迷宫”：每走一步就记下当前的路径（已挑选的字符），如果走不下去就退回（回溯）重新尝试别的路。  
- **正确性**：回溯会遍历 **所有** 长度为 `combinationLength` 的子序列（因为字符不重复且保持原顺序），恰好对应题目要求的组合集合。把它们存进列表后，`next()` 只要返回当前指针指向的元素并把指针右移，`hasNext()` 判断指针是否已经越界即可。  

#### 代码（Python）  

```python
from typing import List

class CombinationIterator:
    """
    暴力版：一次性生成全部组合，存进列表。
    """

    def __init__(self, characters: str, combinationLength: int):
        self.combos: List[str] = []          # 保存所有合法组合
        self.idx: int = 0                    # 当前指针，指向下一个要返回的组合

        # ---------- 回溯生成组合 ----------
        def backtrack(start: int, path: List[str]) -> None:
            # 如果已经挑满了，拼成字符串加入结果
            if len(path) == combinationLength:
                self.combos.append(''.join(path))
                return
            # 从 start 开始尝试每一个后续字符
            for i in range(start, len(characters)):
                # 选入字符 i
                path.append(characters[i])
                # 继续向后搜索
                backtrack(i + 1, path)
                # 退回，尝试下一个字符
                path.pop()

        backtrack(0, [])
        # 组合本身已经是字典序，无需再排序

    def next(self) -> str:
        """返回当前指针指向的组合，并把指针右移一位"""
        result = self.combos[self.idx]
        self.idx += 1
        return result

    def hasNext(self) -> bool:
        """只要指针还没有超过列表长度，就还有下一个组合"""
        return self.idx < len(self.combos)
```

#### 复杂度  

- **时间复杂度**  
  - 初始化时需要遍历所有合法组合。组合数为 `C(n, k) = n! / (k!·(n‑k)!)`（`n = len(characters)`），每个组合拼接字符串的代价是 `O(k)`，所以总体是 **`O(C(n,k)·k)`**。  
  - `next()` 与 `hasNext()` 均为 **`O(1)`**（只读列表、移动指针）。  

- **空间复杂度**  
  - 需要把所有组合都保存下来，空间是 **`O(C(n,k)·k)`**。  
  - 额外的递归栈深度最多 `k`，可以忽略不计。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **初始化时一次性生成所有组合并占用大量内存**。如果只需要按顺序访问组合，我们完全可以 **“按需生成”**，每次 `next()` 只计算下一个组合，而不必把所有组合都存起来。  

关键点：

1. **组合的字典序等价于**：  
   用一组递增的索引 `i0 < i1 < … < i(k‑1)` 表示当前组合在原字符序列中的位置。  
   例如 `"abcde"`、`k=3`，索引 `[0,1,2]` → `"abc"`，索引 `[0,1,3]` → `"abd"`，依此类推。

2. **如何得到下一个索引序列**  
   - 从右往左找第一个可以“向右移动”的位置。  
   - 设当前位置是 `pos`，它的最大可取值是 `n‑k+pos`（因为右边还要留出足够的空间给后面的元素）。  
   - 把 `pos` 加 1，然后把它右边的所有位置依次设为紧跟在前面的最小合法值（即 `pos+1, pos+2, …`）。  
   - 这正是 **“字典序的下一个组合”** 的生成方法，时间只和 `k` 成正比。

3. **数据结构**  
   - 用一个长度为 `k` 的列表 `indices` 保存当前组合对应的字符下标。  
   - `indices` 本身就像一把 **“指针钥匙”**，每次 `next()` 用它在原字符串上取字符形成答案。  
   - `hasNext` 只要判断 `indices` 是否已经走到最后一种组合即可（即 `indices[0] == n‑k` 且其余递增到极限）。

这样，我们在 **初始化** 时只需要把 `indices = [0,1,…,k‑1]`（即第一个组合）准备好，后面的组合在每次 `next()` 时动态生成，空间只剩 `O(k)`，时间每次 `O(k)`，整体非常高效。

#### 代码（Python）  

```python
class CombinationIterator:
    """
    最优解：仅保存当前组合的索引数组，按需生成下一个组合。
    """

    def __init__(self, characters: str, combinationLength: int):
        self.chars = characters               # 原字符序列，保持不变
        self.n = len(characters)              # 总字符数
        self.k = combinationLength            # 组合长度

        # 初始组合对应的索引：0,1,2,...,k-1
        self.indices = list(range(self.k))

        # 是否还有下一个组合的标记。初始化时一定有（题目保证调用合法）
        self._has_next = True if self.k <= self.n else False

    def _next_combination(self) -> None:
        """
        根据当前 self.indices，生成字典序的下一个组合索引。
        若已经是最后一种组合，则把 _has_next 设为 False。
        """
        # 从右往左寻找可以“向右移动”的位置
        i = self.k - 1
        while i >= 0 and self.indices[i] == self.n - self.k + i:
            i -= 1

        if i < 0:                     # 已经没有可移动的位子，说明已经是最后一个组合
            self._has_next = False
            return

        # 把找到的位子右移一格
        self.indices[i] += 1
        # 右边的位子重新紧贴在左边位子的后面，形成最小的字典序
        for j in range(i + 1, self.k):
            self.indices[j] = self.indices[j - 1] + 1

    def next(self) -> str:
        """返回当前组合对应的字符串，并准备好下一个组合"""
        # 依据当前索引数组构造答案
        ans = ''.join(self.chars[i] for i in self.indices)

        # 为后续调用准备下一个组合（如果还有的话）
        self._next_combination()
        return ans

    def hasNext(self) -> bool:
        """只要还有未遍历完的组合，就返回 True"""
        return self._has_next
```

#### 复杂度  

- **时间复杂度**  
  - `next()`：遍历 `k` 个索引取字符 → **`O(k)`**；随后再进行一次右向扫描并可能更新最多 `k` 个位置，仍是 **`O(k)`**。  
  - `hasNext()`：仅返回布尔值 → **`O(1)`**。  
  - 与暴力解相比，**不再需要一次性遍历 `C(n,k)` 组合**，而是“按需”产生，整体更快且更省内存。

- **空间复杂度**  
  - 只保存 `indices`（长度 `k`）以及几个整数 → **`O(k)`**。  
  - 与暴力解的 `O(C(n,k)·k)` 相比，下降到了线性空间。  

---

## 心得  

- **核心技巧**：利用**组合的字典序特性**，用一组递增的索引直接生成下一个组合，避免预先枚举全部结果。  
- **适用场景**：  
  1. **组合/子集迭代器**（如 LeetCode 1286 `Iterator for Combination`）。  
  2. **排列迭代器**（下一个排列的生成，同样基于索引或数组的原地修改）。  
  3. **位掩码枚举**（当 `n ≤ 20` 时，用二进制位表示子集并按顺序遍历）。  
- **一句话总结**：  
  *“把组合看成一把递增的指针钥匙，指针每次右移一步，就是字典序的下一个答案。”*

---

## 反思  

- **第一反应**：直接把所有组合一次性生成，存进列表——最自然、最不容易出错的办法。  
- **最容易踩的坑**  
  - **边界条件**：当 `combinationLength == len(characters)` 时，只有唯一一个组合；当 `combinationLength == 1` 时，需要确保右移逻辑仍然正确。  
  - **指针越界**：在 `_next_combination` 中忘记判断 `i < 0` 会导致索引访问负数，引发错误。  
  - **返回值顺序**：题目要求字典序，需要保证初始索引是 `[0,1,…]`，并且右移后重新紧凑排列。  
- **下次遇到同类题**，第一步应该先思考 **“是否可以用索引/位掩码直接按序产生下一个结果，而不是一次性全部列出？”**，这样往往能把时间和空间复杂度都压到最优。