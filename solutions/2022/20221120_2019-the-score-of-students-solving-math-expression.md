# #2019. 学生解答数学表达式的得分 / The Score of Students Solving Math Expression

> 难度：困难 · 标签：Array、Math、String、Dynamic Programming、Stack、Memoization · [LeetCode 链接](https://leetcode.com/problems/the-score-of-students-solving-math-expression/)

---

## 题目（英文原版）

**Description**

You are given a string s that contains digits 0-9, addition symbols '+', and multiplication symbols '*' only, representing a valid math expression of single digit numbers (e.g., 3+5*2). This expression was given to n elementary school students. The students were instructed to get the answer of the expression by following this order of operations:
You are given an integer array answers of length n, which are the submitted answers of the students in no particular order. You are asked to grade the answers, by following these rules:
Return the sum of the points of the students.

**Examples**

**Example 1:**

```
Input: s = "7+3*1*2", answers = [20,13,42]
Output: 7
Explanation: As illustrated above, the correct answer of the expression is 13, therefore one student is rewarded 5 points: [20,13,42]
A student might have applied the operators in this wrong order: ((7+3)*1)*2 = 20. Therefore one student is rewarded 2 points: [20,13,42]
The points for the students are: [2,5,0]. The sum of the points is 2+5+0=7.
```

**Example 2:**

```
Input: s = "3+5*2", answers = [13,0,10,13,13,16,16]
Output: 19
Explanation: The correct answer of the expression is 13, therefore three students are rewarded 5 points each: [13,0,10,13,13,16,16]
A student might have applied the operators in this wrong order: ((3+5)*2 = 16. Therefore two students are rewarded 2 points: [13,0,10,13,13,16,16]
The points for the students are: [5,0,0,5,5,2,2]. The sum of the points is 5+0+0+5+5+2+2=19.
```

**Example 3:**

```
Input: s = "6+0*1", answers = [12,9,6,4,8,6]
Output: 10
Explanation: The correct answer of the expression is 6.
If a student had incorrectly done (6+0)*1, the answer would also be 6.
By the rules of grading, the students will still be rewarded 5 points (as they got the correct answer), not 2 points.
The points for the students are: [0,0,5,0,0,5]. The sum of the points is 10.
```

**Constraints**

- 3 <= s.length <= 31
- s represents a valid expression that contains only digits 0-9, '+', and '*' only.
- All the integer operands in the expression are in the inclusive range [0, 9].
- 1 <= The count of all operators ('+' and '*') in the math expression <= 15
- Test data are generated such that the correct answer of the expression is in the range of [0, 1000].
- n == answers.length
- 1 <= n <= 104
- 0 <= answers[i] <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个仅包含数字 `0-9`、加号 `'+'` 和乘号 `'*'` 的字符串 `s`，它表示一个合法的单数字数学表达式（例如 `3+5*2`）。这道表达式被交给 `n` 名小学生，要求他们按如下运算顺序求得答案：

1. 先进行所有的乘法（`*`），再进行加法（`+`），即遵循标准的运算优先级。  
2. 若学生使用了错误的运算顺序（即对运算符任意加括号），则得到的可能是 **错误答案**。

现在给定长度为 `n` 的整数数组 `answers`，其中存放了学生提交的答案，顺序任意。请按照以下规则为每位学生打分，并返回所有学生得分的总和。

- 若学生的答案等于表达式的 **正确答案**，奖励 **5 分**。  
- 否则，若学生的答案等于 **某一种错误的括号化**（即对运算符任意加括号后得到的结果），奖励 **2 分**。  
- 其他情况得 **0 分**。  

> 注意：如果某个错误的括号化恰好得到与正确答案相同的数值，则仍按“正确答案”计 5 分，而不是 2 分。

**示例**

示例 1  
```text
Input: s = "7+3*1*2", answers = [20,13,42]
Output: 7
Explanation: 正确答案为 13，因而得到 5 分的学生有 1 人（答案 13）。  
错误的运算顺序如 ((7+3)*1)*2 = 20，对应得到 2 分的学生有 1 人（答案 20）。  
各学生得分分别为 [2,5,0]，总分为 2+5+0 = 7。
```

示例 2  
```text
Input: s = "3+5*2", answers = [13,0,10,13,13,16,16]
Output: 19
Explanation: 正确答案为 13，三位学生得到 5 分（答案 13）。  
错误的运算顺序如 ((3+5)*2) = 16，得到 2 分的学生有两位（答案 16）。  
各学生得分为 [5,0,0,5,5,2,2]，总分为 5+0+0+5+5+2+2 = 19。
```

示例 3  
```text
Input: s = "6+0*1", answers = [12,9,6,4,8,6]
Output: 10
Explanation: 正确答案为 6。  
即使错误的括号化 (6+0)*1 也等于 6，但仍按正确答案计 5 分。  
各学生得分为 [0,0,5,0,0,5]，总分为 10。
```

**约束条件**
- `3 <= s.length <= 31`
- `s` 为仅包含数字 `0-9`、`'+'` 与 `'*'` 的合法表达式
- 表达式中所有整数操作数均在 `[0, 9]` 范围内
- 表达式中运算符（`'+'` 与 `'*'`）的总数满足 `1 <= count <= 15`
- 测试数据保证表达式的正确答案在 `[0, 1000]` 之间
- `n == answers.length`
- `1 <= n <= 10^4`
- `0 <= answers[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求我们判断每个学生的答案属于哪一种情况：

1. **完全正确**：使用普通的运算顺序（乘法先于加法）得到的答案。  
2. **运算顺序错误但仍能得到的结果**：如果把表达式任意加括号（即随意决定先算哪一步），得到的结果恰好等于学生的答案。  
3. 其它情况：得 0 分。

> **类比**：把表达式想成一串珠子，珠子之间有两种“绳子”——`+` 与 `*`。  
> - 按照教材的顺序（`*` 先算）把所有绳子都剪开，最后只剩下几个珠子相加，这就是**标准答案**。  
> - 但如果我们随意先剪哪根绳子（先算哪个子表达式），所有可能的剪法对应的最终珠子数就是**所有可能的答案**。

**暴力做法**：  
1. 先把表达式按字符拆成数字列表 `nums` 与运算符列表 `ops`（例如 `"3+5*2"` → `nums=[3,5,2]`，`ops=['+','*']`）。  
2. 用递归枚举所有合法的加括号方式。对每一种划分，递归求左子表达式的所有可能值 `L`，右子表达式的所有可能值 `R`，然后把 `L` 与 `R` 用当前运算符算一次，所有结果放进一个集合 `res`。  
3. 递归的终止条件是子表达式只剩一个数字，直接返回 `{该数字}`。  
4. 这样得到的集合 `all_vals` 就是**所有可能的答案**。  
5. 再单独用一次普通的运算顺序算出**正确答案** `true_val`（可以直接用 `eval`，也可以手动实现）。  
6. 最后遍历 `answers`，根据是否等于 `true_val`（5 分）或是否在 `all_vals` 中（2 分）累计总分。

> **为什么正确**：递归把每一种合法的二叉树结构（即一种加括号方式）都枚举了一遍，且每棵树的计算结果都被加入集合，因而 `all_vals` 包含了**所有**可能的结果。

**时间/空间复杂度**  
- 对长度为 `m`（运算符个数 ≤ 15）的表达式，所有不同的划分数大约是 Catalan 数 `C_m`，它的增长速度是指数级的（约 `4^m / (m^{1.5})`）。所以最坏情况下时间复杂度是 **指数级**，记作 `O(2^m)`（大白话：随着运算符增多，计算时间会飞快增长，像翻倍一样）。  
- 递归的调用栈深度最多 `m`，每层都保存一个集合，集合里最多存 `O(答案范围)`（这里 ≤ 1000）个整数，所以空间复杂度是 **指数级**（与时间相同的量级），但因为答案被限制在 0~1000，实际占用的内存不会太大。

---

#### 代码（Python）

```python
from typing import List, Set

def evaluate_standard(s: str) -> int:
    """
    按照乘法优先、加法后置的正常顺序计算表达式的值。
    思路：先把表达式按 '+' 切块，每块内部只含 '*', 直接把乘积算出来，
    再把所有块相加。
    """
    total = 0
    # 按加号分段，例如 "7+3*1*2" -> ["7", "3*1*2"]
    for term in s.split('+'):
        prod = 1
        # 每段内部只有乘号，例如 "3*1*2"
        for num in term.split('*'):
            prod *= int(num)          # 把字符转成整数后相乘
        total += prod                # 把每段的乘积相加
    return total


def all_possible_vals(nums: List[int], ops: List[str],
                      l: int, r: int,
                      memo: dict) -> Set[int]:
    """
    递归枚举 nums[l..r]（以及对应的 ops）所有可能的计算结果。
    使用 memo[(l,r)] 缓存子区间的结果，避免重复计算。
    """
    if (l, r) in memo:
        return memo[(l, r)]

    # 子区间只剩一个数字，直接返回该数字的集合
    if l == r:
        memo[(l, r)] = {nums[l]}
        return memo[(l, r)]

    res = set()
    # 在每一个运算符位置划分左右子表达式
    for i in range(l, r):
        left_vals = all_possible_vals(nums, ops, l, i, memo)
        right_vals = all_possible_vals(nums, ops, i + 1, r, memo)
        op = ops[i]                     # 第 i 个运算符对应的符号

        # 把左、右两边的所有可能值两两组合
        for a in left_vals:
            for b in right_vals:
                if op == '+':
                    res.add(a + b)
                else:                  # op == '*'
                    res.add(a * b)

    memo[(l, r)] = res
    return res


def score_of_students(s: str, answers: List[int]) -> int:
    # 1️⃣ 计算标准答案
    true_val = evaluate_standard(s)

    # 2️⃣ 把表达式拆成数字和运算符列表
    nums = [int(ch) for ch in s if ch.isdigit()]          # 只保留数字字符
    ops  = [ch for ch in s if ch in '+*']                  # 只保留运算符

    # 3️⃣ 暴力枚举所有可能的结果（带记忆化）
    memo = {}
    all_vals = all_possible_vals(nums, ops, 0, len(nums) - 1, memo)

    # 4️⃣ 计算总分
    total = 0
    for ans in answers:
        if ans == true_val:
            total += 5            # 完全正确
        elif ans in all_vals:
            total += 2            # 只算错顺序但仍得到的答案
        # else: 得 0 分，不需要额外处理
    return total
```

#### 复杂度

- **时间复杂度**：`O(2^m)`（指数级），因为递归会遍历所有可能的二叉树划分。  
- **空间复杂度**：`O(2^m)`，递归栈和记忆化表会保存每个子区间的所有可能结果。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复计算**：同一个子表达式会被多次求值。  
我们可以把“子表达式的所有可能结果”记下来（**记忆化**），这样每个子区间只计算一次，时间从指数级降到多项式级。

具体步骤：

1. **拆分表达式**  
   与暴力解相同，得到数字列表 `nums`（长度 ≤ 16）和运算符列表 `ops`（长度 ≤ 15）。

2. **记忆化递归 / 动态规划**  
   - 用字典 `memo[(l, r)]` 保存区间 `[l, r]`（包括第 `l` 到第 `r` 个数字）所有可能的计算结果。  
   - 对每个区间 `[l, r]`，枚举中间的运算符位置 `i`（`l ≤ i < r`），把区间划分为左子区间 `[l, i]` 与右子区间 `[i+1, r]`。  
   - 递归得到左、右两边的结果集合 `L`、`R`（已经被缓存），再把 `L` 与 `R` 按当前运算符合并，得到该划分的所有可能值。  
   - 把所有划分得到的值放进集合 `res`，最后存入 `memo[(l, r)]`。

   由于每个区间只会被计算一次，**时间复杂度** 为 `O(m^3)`（`m` 为数字个数），这在 `m ≤ 16` 时几乎可以忽略不计。  
   - 为什么是 `O(m^3)`？  
     - 区间数量是 `O(m^2)`（所有左、右端点组合）。  
     - 对每个区间，我们遍历 `O(m)` 个划分点。  
     - 合并左右集合的大小受答案范围限制（≤ 1000），可以视作常数。  

3. **计算标准答案**  
   使用一次线性扫描即可得到乘法先算的结果（见下文实现），时间 `O(m)`。

4. **评分**  
   - 把所有可能的结果放进一个 `set` `all_vals`（记忆化已经得到）。  
   - 遍历 `answers`，如果等于标准答案 `true_val` 加 5 分；否则如果在 `all_vals` 中加 2 分。

5. **进一步的剪枝（可选）**  
   - 题目保证答案 ≤ 1000，计算时可以把大于 1000 的中间结果直接丢弃，防止集合膨胀。  
   - 由于运算符只有 `+` 与 `*`，结果永不为负数，直接使用整数集合即可。

> **核心技巧**：**区间 DP + 记忆化**，把“所有可能的子结果”缓存下来，避免重复枚举。

---

#### 代码（Python）

```python
from typing import List, Set

def evaluate_standard(s: str) -> int:
    """普通运算顺序（* 先算）得到的唯一答案。"""
    total = 0
    for term in s.split('+'):          # 按加号分块
        prod = 1
        for num in term.split('*'):    # 每块内部只含乘号
            prod *= int(num)
        total += prod
    return total


def compute_all_vals(nums: List[int], ops: List[str]) -> Set[int]:
    """
    动态规划（记忆化递归）求所有可能的结果。
    只保留 0~1000 之间的值，防止集合无限增长。
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(l: int, r: int) -> frozenset:
        # 区间只剩一个数字
        if l == r:
            return frozenset({nums[l]})

        results = set()
        # 在每一个运算符处划分左右子区间
        for i in range(l, r):
            left  = dfs(l, i)
            right = dfs(i + 1, r)
            op = ops[i]

            for a in left:
                for b in right:
                    val = a + b if op == '+' else a * b
                    # 题目限制答案 ≤ 1000，超过的直接丢弃
                    if 0 <= val <= 1000:
                        results.add(val)

        return frozenset(results)      # 用不可变集合便于 lru_cache 缓存

    return set(dfs(0, len(nums) - 1))


def score_of_students(s: str, answers: List[int]) -> int:
    # 1️⃣ 正确答案（乘法优先）
    true_val = evaluate_standard(s)

    # 2️⃣ 拆分数字和运算符
    nums = [int(ch) for ch in s if ch.isdigit()]
    ops  = [ch for ch in s if ch in '+*']

    # 3️⃣ 所有可能的答案（记忆化 DP）
    all_vals = compute_all_vals(nums, ops)

    # 4️⃣ 计分
    total = 0
    for ans in answers:
        if ans == true_val:
            total += 5
        elif ans in all_vals:
            total += 2
    return total
```

#### 复杂度

- **时间复杂度**：`O(m^3)`，其中 `m` 为数字个数（最多 16），实际运行时间极快。  
  - 与暴力解相比，指数级的 `O(2^m)` 降到了多项式级的 `O(m^3)`，即“把原本要翻几百页的手稿压缩成几页”。  
- **空间复杂度**：`O(m^2)` 用于记忆化表（保存每个子区间的结果集合），每个集合大小受答案上限 1000 限制，实际占用内存很小。

---

## 心得

- **核心技巧**：**区间动态规划 + 记忆化**（也叫“不同括号的计算”），可以在指数级搜索空间里高效地枚举所有可能的结果。  
- **适用的题型**  
  1. LeetCode 241 *Different Ways to Add Parentheses*（相同思路，只是运算符种类不同）。  
  2. LeetCode 877 *Stone Game*（区间 DP 用于子区间的最优解）。  
  3. 任意需要**枚举所有子表达式结果**的题目（如带括号的布尔表达式求值）。  
- **一句话总结解题钥匙**：把“大树的所有枝干”记下来，只在每个子树上算一次，避免重复劳动。

---

## 反思

- **第一反应**：直接写一个递归把所有括号方式全部枚举，感觉实现起来最直接。  
- **最容易踩的坑**  
  - **重复计算**：没有记忆化会导致指数级爆炸。  
  - **答案范围**：如果不限制中间结果的大小，集合会无限增长，导致内存超限。  
  - **运算符优先级**：标准答案必须严格按照 `*` 先算，否则会把本该 5 分的错算成 2 分。  
- **下次类似题的第一步**：先把表达式拆成数字与运算符列表，思考是否可以用 **区间 DP**（记忆化递归）来把所有子区间的结果缓存起来，再再利用这些子结果组合得到全局答案。这样既安全又高效。