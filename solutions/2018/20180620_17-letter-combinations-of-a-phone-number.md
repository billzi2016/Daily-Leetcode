# #17. 电话号码的字母组合 / Letter Combinations of a Phone Number

> 难度：中等 · 标签：Hash Table、String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

---

## 题目（英文原版）

**Description**

Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.
A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

**Examples**

**Example 1:**

```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**Example 2:**

```
Input: digits = ""
Output: []
```

**Example 3:**

```
Input: digits = "2"
Output: ["a","b","c"]
```

**Constraints**

- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].

---

## 题目（中文翻译）

给定一个只包含字符 `'2'` 到 `'9'`（含）的字符串 `digits`，返回该数字可能表示的所有字母组合（letter combinations）。答案的顺序可以任意。

数字到字母的映射（mapping）如下（类似电话键盘上的按键），注意 `1` 不映射到任何字母：

- `2` → `"abc"`
- `3` → `"def"`
- `4` → `"ghi"`
- `5` → `"jkl"`
- `6` → `"mno"`
- `7` → `"pqrs"`
- `8` → `"tuv"`
- `9` → `"wxyz"`

**示例**

**示例 1**  
Input: `digits = "23"`  
Output: `["ad","ae","af","bd","be","bf","cd","ce","cf"]`

**示例 2**  
Input: `digits = ""`  
Output: `[]`

**示例 3**  
Input: `digits = "2"`  
Output: `["a","b","c"]`

**约束条件**

- `0 <= digits.length <= 4`
- `digits[i]` 为范围 `['2', '9']` 内的字符。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把每个数字对应的字母集合都列出来，然后把这些集合**两两拼接**，再和下一个集合拼接，直到把所有数字的字母都拼完。  
可以把它想象成**“字母的笛卡尔积”**——就像在超市里挑选衣服，先挑上衣（第一位的字母），再挑裤子（第二位的字母），每一种上衣都可以和每一种裤子组合，最后得到所有可能的套装。

实现时我们可以使用 **递归**（深度优先搜索）或者 **循环**（逐层累加）。这里用递归来写：

1. 建立一个哈希表 `digit2char`，把数字 `'2'~'9'` 映射到对应的字母字符串。哈希表就像一本**字典**，键（key）是数字，值（value）是它对应的字母集合。  
2. 设一个递归函数 `backtrack(idx, path)`，  
   - `idx` 表示当前正在处理第几位数字（从左到右），  
   - `path` 保存已经拼好的字母前缀（相当于已经挑好的衣服）。  
3. 当 `idx == len(digits)` 时，说明已经处理完所有数字，把 `path` 加入答案列表。  
4. 否则，取出 `digits[idx]` 对应的所有字母，遍历每个字母，把它加到 `path` 里继续递归。

**为什么一定能得到所有组合？**  
递归的每一层都枚举当前数字的每一个可能字母，且每条递归路径恰好走过所有数字的每一层，所以每一种可能的字母序列都会被遍历一次，且不会漏掉。

#### 代码（Python）

```python
from typing import List

def letter_combinations_bruteforce(digits: str) -> List[str]:
    # 1. 建立数字到字母的映射表（哈希表），类似查字典
    digit2char = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    # 特殊情况：空字符串直接返回空列表
    if not digits:
        return []

    ans: List[str] = []          # 用来收集所有合法组合

    # 2. 深度优先搜索（回溯）函数
    def backtrack(idx: int, path: List[str]) -> None:
        """
        idx   : 当前处理到 digits 的第 idx 位
        path  : 已经选好的字母，使用列表便于后续 pop
        """
        # 3. 递归终止条件——所有数字都已经处理完
        if idx == len(digits):
            ans.append(''.join(path))   # 把列表转成字符串加入答案
            return

        # 4. 取出当前数字对应的所有字母，逐个尝试
        possible_chars = digit2char[digits[idx]]
        for ch in possible_chars:
            path.append(ch)          # 选一个字母
            backtrack(idx + 1, path) # 继续往后处理
            path.pop()               # 恢复现场，尝试下一个字母

    # 从第 0 位开始搜索
    backtrack(0, [])
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(3^n * 4^m)`  
  - 这里 `n` 是只对应 3 个字母的数字（2,3,4,5,6,8），`m` 是对应 4 个字母的数字（7,9）。每个数字都要遍历它所有的字母，所以总的组合数等于 `3^n * 4^m`，每个组合生成时需要 `O(L)`（L 为 digits 长度）的拼接操作，整体仍是指数级。用大白话说，就是“随着数字个数增加，组合数会飞速增长”，这也是暴力解慢的根本原因。  
- **空间复杂度：** `O(L)`（递归栈深度）+ `O(3^n * 4^m * L)`（存放答案）  
  - 递归最多会深入 `L` 层，每层保存一个字符，所以需要 `L` 的栈空间。答案本身需要把所有组合都保存下来，这部分空间不可避免。

---

### 2. 最优解

#### 思路  

在上面的暴力解中，**瓶颈**并不在于枚举方式本身（回溯已经是最自然的枚举），而是**每次递归都要创建/复制字符串**，以及**使用列表 `path` 再 `join`** 的开销。我们可以：

1. **直接在递归过程中构造完整的字符串**，不必每次都 `join`。Python 的字符串是不可变的，频繁拼接会产生很多临时对象。使用列表 `path` 再 `join` 已经是常用的优化手段，这里已经比较好。  
2. **利用迭代方式**，把所有字母集合一次性地做笛卡尔积。Python 的 `itertools.product` 能一次性生成所有组合，但这相当于把递归的过程交给库实现，时间复杂度仍是指数级，只是实现更简洁。  
3. **剪枝**：在本题里并没有可以提前剪掉的分支，因为每个字母都是合法的。于是**最优解**其实就是**回溯（深度优先搜索）**，只需要写得简洁、避免不必要的拷贝。

下面给出一种**更简洁的回溯实现**，把 `path` 当成字符串直接传递（因为每层只加一个字符，Python 会创建新字符串，但代码更直观；在实际运行时性能与列表+`join` 差别不大，且题目规模 `digits <= 4` 并不会成为瓶颈）。

> **关键点**：  
> - **哈希表**（字典）用来快速查找每个数字对应的字母集合，像查字典一样 O(1)。  
> - **回溯**（Backtracking）是一种**深度优先搜索**的技巧：沿着一条可能的路径一直往下走，走不通就“回头”尝试别的分支。这里每条路径对应一种字母组合。  

#### 代码（Python）

```python
from typing import List

def letter_combinations_optimal(digits: str) -> List[str]:
    # 1. 数字到字母的映射，使用字典（哈希表）实现 O(1) 查找
    digit2char = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    if not digits:                # 空输入直接返回空列表
        return []

    res: List[str] = []           # 用来存放最终答案

    # 2. 回溯函数，使用字符串 path 直接累计当前组合
    def dfs(idx: int, path: str) -> None:
        """
        idx  : 当前处理到 digits 的第 idx 位
        path : 已经拼好的字母串（当前组合的前缀）
        """
        # 3. 完成所有位的拼接，得到一个完整组合
        if idx == len(digits):
            res.append(path)
            return

        # 4. 取出当前数字对应的所有字母，逐个尝试
        for ch in digit2char[digits[idx]]:
            dfs(idx + 1, path + ch)   # 递归进入下一层，路径加上新字母

    # 从第 0 位开始搜索
    dfs(0, "")
    return res
```

#### 复杂度  

- **时间复杂度：** `O(3^n * 4^m)`  
  - 与暴力解的时间复杂度相同，因为我们仍然要遍历所有可能的字母组合。这里的“最优”指的是 **实现最简洁、代码最易懂且常数因子更小**，而不是指数级的降低。  
- **空间复杂度：** `O(L)`（递归栈）+ `O(3^n * 4^m * L)`（存放答案）  
  - 与暴力解相同，只是递归时使用字符串 `path` 而不是列表，栈深度仍是 `L`（digits 长度），答案占用的空间不可避免。

---

## 心得

- **核心技巧**：回溯（深度优先搜索）+ 哈希表快速映射。  
- **适用的题型**：  
  1. **全排列**（Permutations）——需要枚举所有可能的顺序。  
  2. **子集生成**（Subsets）——枚举集合的所有子集。  
  3. **组合总和**（Combination Sum）——在给定数字集合中找出所有满足条件的组合。  
- **一句话总结**：**“把每一位的所有选择都遍历一遍，用回溯把路径记录下来，就是答案。”**

---

## 反思

- **第一反应**：看到“数字对应字母”，立刻想到把每个数字映射成字母集合，然后把这些集合做笛卡尔积。  
- **最容易踩的坑**：  
  - 忘记处理空字符串 `""`，直接返回空列表会导致后续递归出错。  
  - 递归终止条件写错（比如用了 `>=` 而不是 `==`），会产生多余的空组合。  
  - 对数字 `'7'` 和 `'9'` 对应 4 个字母的情况忘记计数，导致复杂度估计错误。  
- **下次遇到同类题**：第一步先 **写出数字→字母的映射表**，然后 **决定是用递归回溯还是迭代笛卡尔积**（取决于个人习惯），最后 **确保递归终止条件和边界（空输入）都处理好**。