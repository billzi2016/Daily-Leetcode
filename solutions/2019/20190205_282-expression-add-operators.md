# #282. 表达式添加运算符 / Expression Add Operators

> 难度：困难 · 标签：Math、String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/expression-add-operators/)

---

## 题目（英文原版）

**Description**

Given a string num that contains only digits and an integer target, return all possibilities to insert the binary operators '+', '-', and/or '*' between the digits of num so that the resultant expression evaluates to the target value.
Note that operands in the returned expressions should not contain leading zeros.
Note that a number can contain multiple digits.

**Examples**

**Example 1:**

```
Input: num = "123", target = 6
Output: ["1*2*3","1+2+3"]
Explanation: Both "1*2*3" and "1+2+3" evaluate to 6.
```

**Example 2:**

```
Input: num = "232", target = 8
Output: ["2*3+2","2+3*2"]
Explanation: Both "2*3+2" and "2+3*2" evaluate to 8.
```

**Example 3:**

```
Input: num = "3456237490", target = 9191
Output: []
Explanation: There are no expressions that can be created from "3456237490" to evaluate to 9191.
```

**Constraints**

- 1 <= num.length <= 10
- num consists of only digits.
- -231 <= target <= 231 - 1

---

## 题目（中文翻译）

给定一个仅包含数字的字符串 `num` 和一个整数 `target`，返回所有可能的方式，在 `num` 的数字之间插入二元运算符（binary operators）`'+'`、`'-'` 和/或 `'*'`，使得生成的表达式的计算结果等于 `target`。  
返回的表达式中，操作数（operands）不得含有前导零。  
注意，数字可以由多个字符组成。

**示例 1**  
**输入**: `num = "123", target = 6`  
**输出**: `["1*2*3","1+2+3"]`  
**解释**: `"1*2*3"` 和 `"1+2+3"` 的计算结果均为 6。

**示例 2**  
**输入**: `num = "232", target = 8`  
**输出**: `["2*3+2","2+3*2"]`  
**解释**: `"2*3+2"` 和 `"2+3*2"` 的计算结果均为 8。

**示例 3**  
**输入**: `num = "3456237490", target = 9191`  
**输出**: `[]`  
**解释**: 没有任何由 `"3456237490"` 生成的表达式能够得到 9191。

**约束条件**  
- `1 <= num.length <= 10`  
- `num` 仅由数字组成。  
- `-2^31 <= target <= 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `num` 中的每两个相邻数字之间**全部**尝试三种符号（`+`、`-`、`*`），或者不放符号（直接把它们拼成一个更大的整数）。  
这样就能得到所有可能的表达式，然后逐个算出它们的值，挑出等于 `target` 的就返回。

- **数据结构**：  
  - **列表** `res` 用来收集符合要求的表达式，像装东西的篮子。  
  - **字符串** `expr` 记录当前拼好的表达式，就像我们手里写的算式。  
  - **整数** `value` 记录算式的结果，等价于把算式交给“计算器”。  

- **为什么正确**：  
  只要把每个位置的三种符号（或不放）全部遍历一遍，就不会漏掉任何一种合法的写法。遍历结束后把每个算式的值和 `target` 比较，恰好相等的必然是答案。

- **时间/空间复杂度**（大白话）  
  - 对长度为 `n` 的字符串，`n‑1` 个缝隙每个都有 **4** 种选择（`+`、`-`、`*`、不放），所以可能的表达式数量是 `4^(n-1)`，这在最坏情况下会指数级增长。  
  - 对每个表达式我们要把它交给 Python 的 `eval`（或者自己写一个解释器）算一次，时间大约是 `O(n)`（因为算式里最多有 `n` 个数字）。  
  - 因此 **时间复杂度** 大约是 `O(4^(n-1) * n)`，也可以写成 `O(4^n)`，意思是随着数字位数增加，耗时会非常快。  
  - **空间复杂度** 只需要存放递归栈和临时字符串，最多 `O(n)`，即和输入长度成正比。

#### 代码（Python）

```python
from typing import List

def addOperators_bruteforce(num: str, target: int) -> List[str]:
    n = len(num)
    res: List[str] = []

    # 递归枚举每个位置放哪种符号
    def dfs(pos: int, expr: str):
        """
        pos  : 已经处理到 num 的下标（左闭右开），
        expr : 当前已经拼好的表达式字符串
        """
        if pos == n:                     # 已经用了所有数字
            # 用 eval 直接算值（这里为了演示暴力法才用）
            try:
                if eval(expr) == target:
                    res.append(expr)
            except Exception:
                pass                  # 防止像 "01" 这种非法数字导致异常
            return

        # 当前位置可以取 1~n-pos 位数字（防止前导零）
        for i in range(pos + 1, n + 1):
            cur_str = num[pos:i]        # 当前切出的子串
            # 跳过前导零（比如 "01"、"00"），但单独的 "0" 是合法的
            if len(cur_str) > 1 and cur_str[0] == '0':
                continue

            if pos == 0:                # 第一个数字前面不能放符号
                dfs(i, cur_str)
            else:
                dfs(i, expr + '+' + cur_str)
                dfs(i, expr + '-' + cur_str)
                dfs(i, expr + '*' + cur_str)

    dfs(0, "")
    return res
```

#### 复杂度

- **时间复杂度**：`O(4^n)`（指数级），因为每个缝隙有 4 种选择，且每条分支都要算一次表达式。  
- **空间复杂度**：`O(n)`，递归栈的最大深度等于数字的个数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次都等到最后才算表达式的值”**。  
如果我们在递归的过程中**同步维护当前表达式的计算结果**，就能在生成完整表达式前就判断它是否有可能得到目标值，从而省掉大量无用的 `eval`。

关键难点是 **乘法的优先级**：  
`+`、`-` 是左结合，直接把当前值累加或累减就可以；  
但 `*` 必须先把前面的乘数 **和上一次的乘法结果** 合并，再加入累计值。  
举例：

```
表达式 1+2*3
从左到右：
  1   -> cur = 1, last = 1
  +2  -> cur = 1+2 = 3, last = 2
  *3  -> 乘法要把上一步的 +2 “撤销”，再乘以 3：
          cur = (3 - last) + last*3 = (3-2) + 2*3 = 1 + 6 = 7
          last = 2*3 = 6
```

于是我们在递归时维护三个信息：

| 信息 | 含义 | 为什么要记 |
|------|------|-------------|
| `expr` | 已经拼好的表达式字符串 | 最终要返回的答案 |
| `value`| 表达式到目前为止的**真实计算结果** | 直接和 `target` 比较 |
| `last` | 最近一次加入 `value` 的**那一块数字**（可能已经乘过） | 处理 `*` 时需要“撤销”它的影响 |

递归步骤：

1. 从当前位置 `pos` 开始，尝试取长度为 `1~n-pos` 的子串 `cur_str`，转成整数 `cur_val`。  
   - 若子串有前导零（长度>1 且首字符是 `0`），直接跳过，因为题目不允许。  
2. **第一块数字**（`pos == 0`）只能直接放进去，`value = cur_val`，`last = cur_val`。  
3. 对于后面的每块数字，分别尝试三种运算符：

   - **`+`**：`value' = value + cur_val`，`last' = cur_val`  
   - **`-`**：`value' = value - cur_val`，`last' = -cur_val`（把负号提前算进去，后面乘法统一处理）  
   - **`*`**：`value' = (value - last) + last * cur_val`，`last' = last * cur_val`  
     解释：先把之前的 `last` 从累计值里减掉（相当于“撤销”它），再把 `last * cur_val` 加回来，这正好实现了乘法的高优先级。

4. 递归进入下一个位置 `i`（子串右端），把新的 `expr、value、last` 传下去。  
5. 当 `pos == n`（已经用了全部数字）时，若 `value == target`，把 `expr` 加入答案列表。

这样每条递归路径只走一次，不需要在叶子节点再去重新解释表达式，时间大幅降低。

#### 代码（Python）

```python
from typing import List

def addOperators(num: str, target: int) -> List[str]:
    n = len(num)
    ans: List[str] = []

    def dfs(pos: int, expr: str, value: int, last: int):
        """
        pos   : 当前要处理的起始下标（左闭右开）
        expr  : 已经拼好的表达式（最终要返回的形式）
        value : expr 目前的计算结果（已经考虑了所有运算符的优先级）
        last  : expr 最后加入的那一块数值（可能已经乘过），用于后续的乘法撤销
        """
        if pos == n:                 # 用完所有字符
            if value == target:
                ans.append(expr)
            return

        for i in range(pos + 1, n + 1):
            cur_str = num[pos:i]
            # 跳过前导零
            if len(cur_str) > 1 and cur_str[0] == '0':
                continue
            cur_val = int(cur_str)

            if pos == 0:              # 第一个数字只能直接放
                dfs(i, cur_str, cur_val, cur_val)
            else:
                # 加号
                dfs(i, expr + '+' + cur_str, value + cur_val, cur_val)

                # 减号
                dfs(i, expr + '-' + cur_str, value - cur_val, -cur_val)

                # 乘号，注意乘法的优先级
                # 先把之前的 last 从累计值里减掉，再加上 last*cur_val
                dfs(i,
                    expr + '*' + cur_str,
                    (value - last) + last * cur_val,
                    last * cur_val)

    dfs(0, "", 0, 0)
    return ans
```

> **代码要点解释**  
> 1. `for i in range(pos+1, n+1)` 用来切出 **所有可能长度** 的数字块。  
> 2. `if len(cur_str) > 1 and cur_str[0] == '0': continue` 负责**剔除前导零**。  
> 3. `last` 在加/减时直接取正负号，这样在乘法时只需要把 `last` 乘上新的数字即可，代码更简洁。  
> 4. 递归深度最多 `n`（≤10），所以栈空间是安全的。

#### 复杂度

- **时间复杂度**：`O(3^{n-1})`（每个缝隙最多 3 种运算符，乘号不产生额外分支），比暴力的 `4^{n-1}` 少一个分支，而且在递归过程中已经把表达式的值算好了，不需要再遍历整个字符串去 `eval`。  
  - 用大白话说，就是当 `n=10` 时，大约只有 `3^9 ≈ 19683` 条路径，完全可以在毫秒级跑完。  
- **空间复杂度**：`O(n)`，递归栈深度等于数字个数（≤10），再加上保存答案的列表（答案本身的大小不计入额外空间）。

---

## 心得

- **核心技巧**：**回溯（Backtracking） + 同步维护表达式的累计值与最近的操作数**，从而在构造表达式的过程中即时判断是否可能得到目标值。  
- **适用的题型**  
  1. “把字符串插入运算符使结果为目标值” 系列（如 LeetCode 282 `Expression Add Operators`、411 `Minimum Unique Word Abbreviation` 的思路类似）。  
  2. “在数字序列中插入 `+`/`-` 使和为目标” 如 494 `Target Sum`（只需维护累计和，不需要乘法撤销）。  
  3. “生成所有合法括号/路径” 这类需要 **枚举所有可能**、并在递归时剪枝的组合问题。  
- **一句话总结解题钥匙**：**“在递归的每一步同步更新‘当前值’与‘上一次的数’，乘法时把上一次的贡献撤销再重新乘”。**

---

## 反思

- **第一反应**：看到“所有可能的表达式”，第一时间想到“枚举 + 计算”。于是想到暴力遍历所有符号组合。  
- **最容易踩的坑**  
  1. **前导零**：像 `"05"`、`"00"` 这类子串在题目中是不合法的，需要在切子串时立即过滤。  
  2. **乘法的优先级**：直接把 `value * cur` 加进去会导致运算顺序错误，必须用 `value - last + last * cur` 的技巧。  
  3. **整数范围**：虽然 Python 的整数不会溢出，但在有些语言需要注意 32 位整数的上下界。  
- **下次遇到同类题**：**先把“状态”写清楚**——递归的参数里需要哪些信息才能在一步步构造时即时得到正确的累计结果。然后再考虑如何利用这些状态来**剪枝**或**快速判断**是否还有可能得到目标。这样可以把“暴力枚举”直接升级为“高效回溯”。