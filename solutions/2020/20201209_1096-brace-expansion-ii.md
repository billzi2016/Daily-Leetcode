# #1096. Brace Expansion II / Brace Expansion II

> 难度：困难 · 标签：String、Backtracking、Stack、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/brace-expansion-ii/)

---

## 题目（英文原版）

**Description**

Under the grammar given below, strings can represent a set of lowercase words. Let R(expr) denote the set of words the expression represents.
The grammar can best be understood through simple examples:
Formally, the three rules for our grammar:
Given an expression representing a set of words under the given grammar, return the sorted list of words that the expression represents.

**Examples**

**Example 1:**

```
Input: expression = "{a,b}{c,{d,e}}"
Output: ["ac","ad","ae","bc","bd","be"]
```

**Example 2:**

```
Input: expression = "{{a,z},a{b,c},{ab,z}}"
Output: ["a","ab","ac","z"]
Explanation: Each distinct word is written only once in the final answer.
```

**Constraints**

- 1 <= expression.length <= 60
- expression[i] consists of '{', '}', ','or lowercase English letters.
- The given expression represents a set of words based on the grammar given in the description.

---

## 题目（中文翻译）

在下面给出的文法下，字符串可以表示一组小写单词。记 `R(expr)` 为表达式 `expr` 所表示的单词集合。

文法可以通过下面的简单例子来理解：

正式地，文法包含以下三条规则：

1. **连接（concatenation）**  
   若 `A` 和 `B` 均为合法表达式，则 `AB` 也是合法表达式，且  
   `R(AB) = { a + b │ a ∈ R(A), b ∈ R(B) }`，其中 “+” 表示字符串拼接。

2. **并集（union）**  
   若 `A` 和 `B` 均为合法表达式，则 `{A,B}` 也是合法表达式，且  
   `R({A,B}) = R(A) ∪ R(B)`。花括号内的多个子表达式之间用逗号分隔。

3. **字母（letter）**  
   任意单个小写英文字母 `c` 本身就是合法表达式，`R(c) = {c}`。

给定一个满足上述文法的表达式 `expression`，返回它所表示的所有单词的 **字典序**（lexicographically） 排序列表。

**示例 1**  
输入: `expression = "{a,b}{c,{d,e}}"`  
输出: `["ac","ad","ae","bc","bd","be"]`

**示例 2**  
输入: `expression = "{{a,z},a{b,c},{ab,z}}"`  
输出: `["a","ab","ac","z"]`  
**解释**: 每个不同的单词在最终答案中只出现一次。

**约束条件**  
- `1 <= expression.length <= 60`  
- `expression[i]` 只包含 `'{'`, `'}'`, `','` 或小写英文字母。  
- 给定的 `expression` 必然能根据上述文法表示出一个单词集合。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把表达式当成一棵树**，从左到右把每个字符都展开成所有可能的单词，然后把得到的单词全部放进一个列表，最后去重并排序。  
可以把它想象成下面的过程：

1. **遍历字符**。  
   - 遇到普通字母（`a~z`）时，直接把它当成一个“只含这一个字母”的集合。  
   - 遇到左花括号 `{` 时，找到对应的右花括号 `}`（注意可能有嵌套），把花括号内部看成一个**子表达式**，递归地把它展开成若干单词。  
   - 遇到逗号 `,` 时，表示“或”。我们把逗号左边得到的所有单词和逗号右边得到的所有单词 **合并（取并集）**。  

2. **把相邻的两个集合做笛卡尔积**（即所有可能的拼接），因为相邻的两个块表示要把它们**连接**起来。  

> 类比：  
> - **哈希表**就像字典，`key` 是单词，`value` 是出现次数。这里我们只需要 `key`（单词本身），所以可以直接用 `set` 去重。  
> - **笛卡尔积**可以想象成两堆水果，左边有苹果、香蕉，右边有红、绿，所有可能的组合就是 “苹果红、苹果绿、香蕉红、香蕉绿”。  

**为什么暴力法能得到正确答案**  
- 每一次我们都完整地把 **所有** 可能性枚举出来：字母直接给出，花括号内部递归展开，逗号做并集，拼接做笛卡尔积。只要不遗漏任何一步，最终集合里就包含了表达式能生成的所有单词。  

**时间/空间复杂度**（大白话）  
- 假设最终产生 `k` 个不同的单词，单词平均长度为 `L`。  
- 暴力遍历会 **把每一种可能都生成一次**，所以时间复杂度大约是 `O(k·L)`。但在最坏情况下，`k` 可能是指数级的（比如 `"{a,b}{c,d}{e,f}..."`），这就像把所有可能的组合都列出来，**时间会呈指数增长**。  
- 我们把所有单词放进一个集合，空间同样是 `O(k·L)`，因为每个单词都要存下来。  

#### 代码（Python）

```python
def braceExpansionII_bruteforce(expression: str):
    """
    暴力版：直接递归展开所有可能的单词，最后去重并排序。
    """
    n = len(expression)

    # ---------- 辅助函数 ----------
    def parse(i: int):
        """
        从下标 i 开始解析，返回 (得到的单词集合, 解析结束后下一个未处理的下标)
        """
        cur_set = set([''])          # 当前块的笛卡尔积初始值是空串
        while i < n and expression[i] != '}':
            if expression[i].isalpha():                     # 单个字母
                # 把每个已有的字符串后面加上这个字母
                cur_set = {s + expression[i] for s in cur_set}
                i += 1
            elif expression[i] == '{':                     # 子表达式
                sub_set, i = parse(i + 1)                  # 递归得到子集合
                # 把子集合和当前集合做笛卡尔积
                cur_set = {s + t for s in cur_set for t in sub_set}
            elif expression[i] == ',':                     # “或”运算
                # 把当前块的结果保存下来，准备解析下一个块
                union_set.update(cur_set)                 # union_set 在外层定义
                cur_set = set([''])                       # 重新开始新的块
                i += 1
        return cur_set, i + 1 if i < n and expression[i] == '}' else i

    # ---------- 主流程 ----------
    union_set = set()          # 用来收集被逗号分隔的所有块（并集）
    final_set, _ = parse(0)    # 从下标 0 开始解析整个表达式
    union_set.update(final_set)   # 把最后一个块也并进来

    # 把集合转成列表、排序、返回
    return sorted(union_set)
```

> 关键行解释  
> - `cur_set = set([''])`：相当于在做乘法时的“单位元”，空串和后面的字母拼接不会改变字母本身。  
> - `{s + expression[i] for s in cur_set}`：把每个已有的字符串后面加上当前字母，实现“拼接”。  
> - `union_set.update(cur_set)`：逗号左边的结果需要和右边的结果合并（取并集）。  

#### 复杂度  

- **时间复杂度**：`O(k·L)`，其中 `k` 为所有可能单词的数量，`L` 为单词平均长度。最坏情况下 `k` 可能是指数级（比如每层都有 2 种选择），所以实际运行时间会非常慢。  
- **空间复杂度**：`O(k·L)`，因为要把所有生成的单词都保存到集合里。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每一次都把所有子集合完整地复制一遍**（尤其是笛卡尔积的实现），导致大量中间结果的重复创建。我们可以通过**一次遍历、分层返回**的方式，直接在递归过程中把 **并集**（逗号）和 **乘积**（相邻块）组合起来，避免不必要的拷贝。

从暴力解出发的改进步骤：

1. **用指针一次遍历**  
   - 维护一个全局指针 `idx`，指向当前要解析的字符。这样我们不需要每次都切片字符串，省去 `O(n)` 的复制开销。  

2. **递归返回集合**  
   - 定义函数 `parse()`，它从当前 `idx` 开始解析，**遇到右花括号 `}` 时结束**，返回 **该子表达式能产生的所有单词集合**。  
   - 递归的返回值本身已经是 **去重** 的 `set`，所以后面不必再额外去重。  

3. **处理三种基本情况**（每一步都只做一次集合运算）  
   - **字母**：返回 `{letter}`。  
   - **逗号**：在同一层的不同子表达式之间做 **并集**（`union`），因为逗号表示“任选其一”。  
   - **相邻块**：在同一层的两个块之间做 **笛卡尔积**（`product`），因为它们需要 **拼接**。  

4. **利用 Python 的集合推导式一次完成笛卡尔积**  
   - `new_set = {a + b for a in left for b in right}`，这一步只遍历一次左集合和右集合的所有组合，时间上是最优的。  

5. **最终结果排序**  
   - 题目要求返回 **字典序**（即排序）且不含重复元素，直接对最终集合 `sorted()` 即可。  

> 类比帮助理解  
> - 想象有 **几层盒子**：最里层是字母，里面装的就是单个字母的集合。  
> - 当两个盒子 **并排** 放在一起（相邻），我们需要把左盒子里的每个字母 **贴在** 右盒子里的每个字母后面，得到所有可能的拼接——这就是笛卡尔积。  
> - 当盒子之间有 **分隔符（逗号）**，我们只需要把它们的内容 **放进同一个大盒子**，即取并集。  

这样，我们只遍历一次表达式（`O(n)`），而集合的合并次数恰好等于产生的单词数 `k`，整体时间是 `O(k·L)`，但没有额外的指数级复制，实际运行非常快。

#### 代码（Python）

```python
def braceExpansionII(expression: str):
    """
    最优解：一次遍历 + 递归返回集合，时间 O(k·L)，空间 O(k·L)。
    """
    n = len(expression)
    idx = 0                     # 全局指针，使用闭包方式在内部函数中修改

    def parse() -> set:
        """
        解析从当前 idx 开始的子表达式，遇到 '}' 时返回。
        返回值是该子表达式能产生的所有单词集合（已经去重）。
        """
        nonlocal idx
        cur_set = set([''])    # 当前块的乘积结果，初始是空串（单位元）

        while idx < n and expression[idx] != '}':
            ch = expression[idx]

            if ch.isalpha():                     # 1️⃣ 单个字母
                # 把字母加入到当前乘积结果中
                cur_set = {s + ch for s in cur_set}
                idx += 1

            elif ch == '{':                      # 2️⃣ 子表达式
                idx += 1          # 跳过左花括号
                sub_set = parse()               # 递归得到子集合
                # 把子集合和当前乘积做笛卡尔积
                cur_set = {s + t for s in cur_set for t in sub_set}

            elif ch == ',':                      # 3️⃣ 逗号 → 并集
                # 把已经得到的块加入全局并集
                result.update(cur_set)
                cur_set = set([''])              # 重新开始下一个块
                idx += 1

        # 当 while 结束时，idx 要么指向 '}'，要么已经到字符串末尾
        return cur_set

    result = set()               # 用来收集同一层被逗号分隔的所有块（并集）
    final_set = parse()         # 解析整个表达式
    result.update(final_set)    # 把最后一个块也并进来

    return sorted(result)       # 按字典序返回列表
```

> 关键行解释  
> - `cur_set = set([''])`：相当于乘法的 “1”，空串与后面的字母拼接不会改变字母本身。  
> - `cur_set = {s + ch for s in cur_set}`：把当前块里的每个已有前缀都加上这个字母，实现“拼接”。  
> - `sub_set = parse()`：递归解析花括号内部，返回的是 **已经去重** 的集合。  
> - `cur_set = {s + t for s in cur_set for t in sub_set}`：一次性完成左集合和右集合的所有拼接，避免多余的拷贝。  
> - `result.update(cur_set)`：遇到逗号时，把当前块的所有单词加入全局并集，然后清空 `cur_set` 为下一个块做准备。  

#### 复杂度  

- **时间复杂度**：`O(k·L)`  
  - `k` 为最终不同单词的数量，`L` 为单词平均长度。我们只遍历表达式一次 (`O(n)`，`n ≤ 60`)，其余的工作都是在生成每个单词的过程中完成的，没有额外的指数级复制。  
  - 与暴力解相比，**省掉了大量中间集合的重复拷贝**，所以在实际测试里会快很多。  

- **空间复杂度**：`O(k·L)`  
  - 需要保存所有不同的单词（集合 `result`），以及递归栈的深度（最坏 `O(n)`，但 `n ≤ 60` 可以忽略不计）。  

---

## 心得  

- **核心技巧**：**递归解析 + 集合的并集/笛卡尔积**。  
- **适用的题型**（类似思路可复用）：  
  1. `LeetCode 1087. Brace Expansion`（只涉及并集，没有嵌套）  
  2. `LeetCode 44. Wildcard Matching`（需要把通配符展开成所有可能的匹配）  
  3. `LeetCode 212. Word Search II`（把字典的前缀树与搜索结合）  

- **一句话总结解题钥匙**：**把表达式看成“并集”和“乘积”的交替出现，用递归一次解析出每层的集合，再用集合的并集/笛卡尔积完成合并**。  

---

## 反思  

- **第一反应**：看到 `{`、`}`、`,` 立刻想到“把它们拆成子表达式，然后枚举所有组合”。  
- **最容易踩的坑**：  
  1. **逗号的作用范围**：逗号只在当前花括号层级有效，不能跨层级。忘记这一点会导致错误的并集。  
  2. **空串的初始化**：在做乘积时必须以空串 `''` 作为起始元素，否则第一个块的结果会丢失。  
  3. **重复单词**：不同分支可能产生相同单词，必须用 `set` 去重后再排序。  

- **下次遇到同类题**，第一步应该想到：**“把整个表达式拆成若干块，每块要么是并集（逗号），要么是乘积（相邻）”，递归返回集合并在相邻块之间做笛卡尔积、在逗号之间做并集**。这样思路清晰、实现也更简洁。