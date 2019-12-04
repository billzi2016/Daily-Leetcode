# #682. Baseball Game / Baseball Game

> 难度：简单 · 标签：Array、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/baseball-game/)

---

## 题目（英文原版）

**Description**

You are keeping the scores for a baseball game with strange rules. At the beginning of the game, you start with an empty record.
You are given a list of strings operations, where operations[i] is the ith operation you must apply to the record and is one of the following:
Return the sum of all the scores on the record after applying all the operations.
The test cases are generated such that the answer and all intermediate calculations fit in a 32-bit integer and that all operations are valid.

**Examples**

**Example 1:**

```
Input: ops = ["5","2","C","D","+"]
Output: 30
Explanation:
"5" - Add 5 to the record, record is now [5].
"2" - Add 2 to the record, record is now [5, 2].
"C" - Invalidate and remove the previous score, record is now [5].
"D" - Add 2 * 5 = 10 to the record, record is now [5, 10].
"+" - Add 5 + 10 = 15 to the record, record is now [5, 10, 15].
The total sum is 5 + 10 + 15 = 30.
```

**Example 2:**

```
Input: ops = ["5","-2","4","C","D","9","+","+"]
Output: 27
Explanation:
"5" - Add 5 to the record, record is now [5].
"-2" - Add -2 to the record, record is now [5, -2].
"4" - Add 4 to the record, record is now [5, -2, 4].
"C" - Invalidate and remove the previous score, record is now [5, -2].
"D" - Add 2 * -2 = -4 to the record, record is now [5, -2, -4].
"9" - Add 9 to the record, record is now [5, -2, -4, 9].
"+" - Add -4 + 9 = 5 to the record, record is now [5, -2, -4, 9, 5].
"+" - Add 9 + 5 = 14 to the record, record is now [5, -2, -4, 9, 5, 14].
The total sum is 5 + -2 + -4 + 9 + 5 + 14 = 27.
```

**Example 3:**

```
Input: ops = ["1","C"]
Output: 0
Explanation:
"1" - Add 1 to the record, record is now [1].
"C" - Invalidate and remove the previous score, record is now [].
Since the record is empty, the total sum is 0.
```

**Constraints**

- 1 <= operations.length <= 1000
- operations[i] is "C", "D", "+", or a string representing an integer in the range [-3 * 104, 3 * 104].
- For operation "+", there will always be at least two previous scores on the record.
- For operations "C" and "D", there will always be at least one previous score on the record.

---

## 题目（中文翻译）

你正在为一场规则特殊的棒球比赛记录分数。比赛开始时，记录（record）为空。  
给定一个字符串数组 `operations`，其中 `operations[i]` 表示第 i 个需要对记录执行的操作，可能是以下四种之一：

* **整数**（如 `"5"`、`"-2"`）——将该整数加入记录。  
* `"C"` —— **作废（Invalidate）** 前一次得分，即从记录中移除最近的一个分数。  
* `"D"` —— 将前一次得分的 **两倍** 加入记录。  
* `"+"` —— 将前两次得分的 **和** 加入记录。

在执行完所有操作后，返回记录中所有分数的总和。

题目保证所有答案和中间计算均能放入 32 位整数，且所有操作均合法。

---

## 示例

### 示例 1  
**输入**: `ops = ["5","2","C","D","+"]`  
**输出**: `30`  
**解释**:
- `"5"` —— 将 5 加入记录，记录变为 `[5]`。  
- `"2"` —— 将 2 加入记录，记录变为 `[5, 2]`。  
- `"C"` —— 作废并移除前一次得分，记录变为 `[5]`。  
- `"D"` —— 将 `2 * 5 = 10` 加入记录，记录变为 `[5, 10]`。  
- `"+"` —— 将 `5 + 10 = 15` 加入记录，记录变为 `[5, 10, 15]`。  
总和为 `5 + 10 + 15 = 30`。

### 示例 2  
**输入**: `ops = ["5","-2","4","C","D","9","+","+"]`  
**输出**: `27`  
**解释**:
- `"5"` —— 记录 `[5]`。  
- `"-2"` —— 记录 `[5, -2]`。  
- `"4"` —— 记录 `[5, -2, 4]`。  
- `"C"` —— 作废前一次得分，记录 `[5, -2]`。  
- `"D"` —— 加入 `2 * -2 = -4`，记录 `[5, -2, -4]`。  
- `"9"` —— 记录 `[5, -2, -4, 9]`。  
- `"+"` —— 加入 `-4 + 9 = 5`，记录 `[5, -2, -4, 9, 5]`。  
- `"+"` —— 加入 `9 + 5 = 14`，记录 `[5, -2, -4, 9, 5, 14]`。  
总和为 `5 + -2 + -4 + 9 + 5 + 14 = 27`。

### 示例 3  
**输入**: `ops = ["1","C"]`  
**输出**: `0`  
**解释**:
- `"1"` —— 记录 `[1]`。  
- `"C"` —— 作废并移除前一次得分，记录 `[]`。  
记录为空时，总和为 `0`。

---

## 约束条件

- `1 <= operations.length <= 1000`  
- `operations[i]` 为 `"C"`、`"D"`、`"+"`，或表示区间 `[-3 * 10^4, 3 * 10^4]` 的整数字符串。  
- 对于操作 `"+"`，记录中必定至少有前两个分数。  
- 对于操作 `"C"` 和 `"D"`，记录中必定至少有一个分数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每一次操作都完整地在一张纸上记下来**，等全部操作结束后再把纸上的数字全部相加。  
这里的“纸”可以用 Python 的 `list` 来模拟，它本质上就是一个**可变长的数组**，我们把它当作“记录”：

- 普通整数（如 `"5"`、`"-2"`） → 把对应的整数直接 `append` 到列表末尾。  
- `"C"` → 把最近一次记录（列表最后一个元素）删掉，用 `pop()`。这就像把桌子最上面的一盘菜吃掉一样。  
- `"D"` → 取最近一次记录的两倍，再 `append`。相当于在桌子最上面再放一盘与上一盘重量相同的两倍的菜。  
- `"+"` → 取最近两次记录的和，再 `append`。这好比把最近两盘菜的重量相加，作为新的一盘放上去。

只要按顺序遍历 `ops`，把每一步都照着上面的规则执行，就能得到最终的记录。最后把列表里所有数字求和即可。

> **为什么正确？**  
> 题目给出的每一种操作都有唯一的、确定的含义；我们把这些含义逐条实现，并且**严格按照出现的顺序**执行，保证了记录的状态始终和题目描述一致。于是最终求得的和必然是正确的。

#### 代码（Python）

```python
def calPoints(ops):
    """
    :type ops: List[str]
    :rtype: int
    """
    record = []                     # 用列表充当“记录本”，相当于一摞牌
    for op in ops:                  # 依次处理每个操作
        if op == "C":               # 失效前一次得分
            record.pop()            # 把最后一张牌拿走
        elif op == "D":             # 本次得分是前一次的两倍
            record.append(2 * record[-1])
        elif op == "+":             # 本次得分是前两次得分之和
            record.append(record[-1] + record[-2])
        else:                       # 普通整数得分
            record.append(int(op))
    return sum(record)              # 把所有得分加起来
```

#### 复杂度  

- **时间复杂度：O(n)** — `n` 为 `ops` 的长度。我们只遍历一次 `ops`，每一步的 `append`、`pop`、取索引等操作都是 **O(1)**，所以整体是线性时间。  
- **空间复杂度：O(n)** — 最坏情况下所有操作都是普通整数，需要把每个得分都保存下来，列表的长度最多会达到 `n`，所以需要线性额外空间。

---

### 2. 最优解

#### 思路  

其实上面的“暴力”解已经是最优的了，因为每个操作本身只能在 **常数时间** 完成，必须遍历一次才能看到所有指令。  
唯一可以进一步**解释清楚**的地方是：我们为何使用**栈（stack）** 这种数据结构，而不是普通的数组或其他结构。

- **栈的特性**：只能在一端（栈顶）进行插入和删除，正好对应题目中“最近一次得分”这种**后进先出**的需求。  
- 使用栈可以让代码的意图更明确：`pop()` 表示“撤销最近一次得分”，`[-1]`、`[-2]` 表示“栈顶的一个或两个元素”。  

因此，最优解就是**用栈** 完整地模拟整个游戏过程，时间、空间复杂度都保持在 O(n)。下面给出更具可读性的实现，并在关键位置加上生活化的类比说明。

#### 代码（Python）

```python
def calPoints(ops):
    """
    使用栈（list）模拟棒球记分规则
    :type ops: List[str]
    :rtype: int
    """
    stack = []                       # 栈：相当于一摞放在桌子上的牌
    for token in ops:
        if token == "C":              # “撤销”最近一张牌
            stack.pop()               # 把栈顶的牌拿走
        elif token == "D":            # “双倍”最近一张牌的分数
            stack.append(2 * stack[-1])   # 在栈顶再放一张分数是原来两倍的牌
        elif token == "+":            # “合计”最近两张牌的分数
            stack.append(stack[-1] + stack[-2])   # 把最近两张牌分数相加，放成新的一张牌
        else:                         # 普通整数得分
            stack.append(int(token))  # 把这张牌直接放进栈
    return sum(stack)                 # 把栈里的所有牌的分数加起来
```

#### 复杂度  

- **时间复杂度：O(n)** — 每个操作只做一次栈的 `push`、`pop` 或读取，都是常数时间。遍历一次 `ops` 即可。  
- **空间复杂度：O(n)** — 栈中最多会保存所有合法得分，最坏情况下与 `ops` 长度相同。

与暴力解相比，**时间和空间都没有增加**，而且代码语义更贴合题目描述，易于阅读和维护。

---

## 心得

- 这道题考察的核心技巧是**栈的模拟**（stack simulation），即在顺序处理指令的过程中，用栈来保存“最近一次”或“最近两次”的状态。
- 该技巧适用的题型包括  
  1. **有效的括号**（Valid Parentheses）——用栈匹配左、右括号。  
  2. **每日温度**（Daily Temperatures）——单调栈求最近更高温度。  
  3. **最小栈**（Min Stack）——在栈中维护额外信息，实现 O(1) 取最小值。
- **一句话总结解题钥匙**：**“把‘最近一次’的东西放在栈顶，所有需要撤销或查询最近记录的操作，都可以在 O(1) 时间内完成”。**

---

## 反思

- **第一反应**：看到 “C、D、+” 这种只能作用在最近一次或最近两次得分的指令，就想到“后进先出”，自然联想到栈。  
- **最容易踩的坑**  
  - 忽略了 **负数** 的情况，直接使用 `int(token)` 时要确保能正确解析。  
  - 对于 `"+"` 必须保证栈里已有至少两条记录，否则会越界（题目已保证，但实现时仍要小心）。  
  - 在 `"C"`、`"D"`、`"+"` 的顺序上出错，导致取错了栈顶元素。  
- **下次遇到同类题**：第一步先判断**是否涉及“最近”或“前缀”**的操作，如果是，立刻考虑使用**栈**（或队列、单调栈）来保存历史状态。这样可以把复杂的回溯或重复遍历问题化简为常数时间的栈操作。