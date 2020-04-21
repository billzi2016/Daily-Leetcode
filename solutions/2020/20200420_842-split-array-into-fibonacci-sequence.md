# #842. 拆分数组为斐波那契序列 / Split Array into Fibonacci Sequence

> 难度：中等 · 标签：String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/split-array-into-fibonacci-sequence/)

---

## 题目（英文原版）

**Description**

You are given a string of digits num, such as "123456579". We can split it into a Fibonacci-like sequence [123, 456, 579].
Formally, a Fibonacci-like sequence is a list f of non-negative integers such that:
Note that when splitting the string into pieces, each piece must not have extra leading zeroes, except if the piece is the number 0 itself.
Return any Fibonacci-like sequence split from num, or return [] if it cannot be done.

**Examples**

**Example 1:**

```
Input: num = "1101111"
Output: [11,0,11,11]
Explanation: The output [110, 1, 111] would also be accepted.
```

**Example 2:**

```
Input: num = "112358130"
Output: []
Explanation: The task is impossible.
```

**Example 3:**

```
Input: num = "0123"
Output: []
Explanation: Leading zeroes are not allowed, so "01", "2", "3" is not valid.
```

**Constraints**

- 1 <= num.length <= 200
- num contains only digits.

---

## 题目（中文翻译）

给定一个仅包含数字的字符串 `num`，例如 `"123456579"`。我们可以将它拆分成一个斐波那契类似序列（Fibonacci-like sequence）`[123, 456, 579]`。  

形式上，斐波那契类似序列是一个非负整数列表 `f`，满足：

- 对所有 `i >= 2`，都有 `f[i] = f[i‑1] + f[i‑2]`。  

在将字符串拆分成若干片段时，**每个片段**不能有多余的前导零，唯一例外是该片段本身就是数字 `0`。  

返回任意一个能够从 `num` 拆分得到的斐波那契类似序列；如果无法完成拆分，则返回空列表 `[]`。

---

### 示例

**示例 1**  
```
Input: num = "1101111"
Output: [11,0,11,11]
Explanation: 输出 [110, 1, 111] 也会被接受。
```

**示例 2**  
```
Input: num = "112358130"
Output: []
Explanation: 任务无法完成。
```

**示例 3**  
```
Input: num = "0123"
Output: []
Explanation: 不允许出现前导零，因此 "01", "2", "3" 是无效的拆分方式。
```

---

### 约束条件

- `1 <= num.length <= 200`
- `num` 仅包含数字字符。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串 `num` 的每一种可能的切分方式都枚举出来，然后检查这些切分得到的序列是否满足 **斐波那契数列** 的定义。

- **枚举切分**  
  把 `num` 看成一串珠子，每一颗珠子上是一个数字字符。我们可以在任意两颗珠子之间插入“分隔符”，把整串变成若干段。比如 `"123456"` 插入两次分隔符可以得到 `[1, 23, 456]`、`[12, 3, 456]` 等等。  
  用程序实现时，最常见的做法是递归（或回溯）——从左到右尝试每一种可能的 “取多长的数字”，把它加入当前序列，再递归处理剩余的字符。

- **为什么一定能判断对错**  
  只要把所有合法的切分都遍历完，就一定会碰到所有可能的斐波那契序列（如果存在的话）。遍历的过程本身并不改变题目要求，只是把“所有可能”逐一展示出来，然后用一个**检查函数**判断当前序列是否满足 `f[i] = f[i-1] + f[i-2]`（且每个数 ≤ `2^31-1`，防止整数溢出）。

- **使用的数据结构**  
  - **列表 (`list`)**：像装珠子的盒子，依次存放已经确定好的数字。  
  - **字符串切片**：把 `num` 的一段字符转成整数，就像把一段珠子摘下来称重。  
  - **递归栈**：每一次尝试都相当于在“记事本”里写下一行“我现在取了多少位”，等到发现冲突再回到上一行继续尝试。

#### 代码（Python）

```python
def splitIntoFibonacci(num: str):
    MAX_INT = 2**31 - 1          # 题目限制的最大整数

    # 递归函数：从下标 start 开始尝试切出下一个数，当前序列保存在 path 中
    def backtrack(start: int, path: list) -> bool:
        # 递归结束条件：遍历完整个字符串且已经得到至少 3 个数
        if start == len(num) and len(path) >= 3:
            return True

        # 当前位置可以取 1~10 位（因为 2^31-1 只有 10 位），防止溢出
        for end in range(start + 1, min(len(num), start + 10) + 1):
            # 不能出现前导零（除非数字本身就是 "0"）
            if num[start] == '0' and end - start > 1:
                break

            cur = int(num[start:end])   # 把切片转成整数
            if cur > MAX_INT:           # 超出范围直接放弃
                break

            # 若已有前两个数，则必须满足斐波那契关系
            if len(path) >= 2:
                if cur < path[-1] + path[-2]:   # 还太小，继续往后取位数
                    continue
                if cur > path[-1] + path[-2]:   # 已经太大，后面的切法都不行
                    break

            # 选取当前数，进入下一层递归
            path.append(cur)
            if backtrack(end, path):   # 成功找到完整序列直接返回 True
                return True
            path.pop()                 # 回溯：撤销选择

        return False   # 所有切法都不行，返回 False

    ans = []
    backtrack(0, ans)
    return ans
```

> **关键行解释**  
> - `if num[start] == '0' and end - start > 1:` —— 防止出现 “01、001” 之类的前导零。  
> - `if len(path) >= 2:` —— 只有在已有前两个数时才检查斐波那契关系。  
> - `if cur < path[-1] + path[-2]: continue` —— 当前数字太小，说明我们取的位数不够，需要继续往右扩展。  
> - `if cur > path[-1] + path[-2]: break` —— 当前数字已经超过应有的和，后面再取更长的数字只会更大，直接剪枝。

#### 复杂度

- **时间复杂度：** `O(2^n)`（指数级）  
  解释：在最坏情况下，每个字符都可以决定是否“分割”，相当于在每个位置都有两种选择（分或不分），所以可能的切分方案数是 `2^(n-1)`。我们需要遍历这些方案来验证是否满足斐波那契条件，因此时间呈指数增长。  
  实际上因为整数大小的限制（最多 10 位）以及前导零的剪枝，真实运行会快很多，`n ≤ 200` 时仍然能在毫秒级通过。

- **空间复杂度：** `O(n)`  
  解释：递归深度最多等于字符串长度（每次最少取走 1 位），再加上保存当前序列的列表，最多占用 `O(n)` 的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **盲目递归**：我们把所有可能的切分都尝试了一遍，即使已经确定了前两个数后，后面的检查仍然是递归遍历。其实，一旦前两个数确定后，后面的数是唯一的——它们必须严格等于前两个数的和。于是我们可以把“后面的递归”改成 **一次性线性验证**，把搜索空间从指数级降到多项式级。

优化步骤：

1. **枚举前两个数的长度**  
   - 前两个数决定了整条斐波那契序列。我们只需要在 `num` 前面尝试所有合法的 `(i, j)`（`i` 为第一个数的结束位置，`j` 为第二个数的结束位置），共 `O(n^2)` 种组合。  
   - 每个数的长度仍然受 `2^31-1`（10 位）和前导零的限制。

2. **一次性生成后续序列**  
   - 已知 `a = num[0:i]`、`b = num[i:j]`，后面的每一项只能是 `a + b`。我们把这个和转成字符串 `c_str`，检查 `num` 从当前位置是否以 `c_str` 为前缀。若是，就把 `c` 加入答案并把指针移动到 `c_str` 之后，继续计算下一个和。  
   - 只要一次检查失败，就立刻放弃当前 `(i, j)`，不再递归回溯。

3. **提前剪枝**  
   - 如果在枚举 `i`、`j` 时，任意一个数已经超过 `2^31-1`，直接停止该分支。  
   - 当 `a + b` 超过 `2^31-1`，也不必继续，因为后面的数只会更大。

这样，整个算法的时间复杂度是 **`O(n^2)`**（两层循环枚举前两个数）乘以 **`O(n)`**（每次线性验证），即 **`O(n^3)`**，在 `n ≤ 200` 的范围内完全可接受，且常数非常小。

#### 代码（Python）

```python
def splitIntoFibonacci(num: str):
    MAX_INT = 2**31 - 1
    n = len(num)

    # 枚举第一个数的结束位置 i（不含），第二个数的结束位置 j（不含）
    for i in range(1, min(10, n) + 1):                # 第一个数最多 10 位
        # 前导零检查
        if num[0] == '0' and i > 1:
            break
        a = int(num[:i])
        if a > MAX_INT:
            break

        for j in range(i + 1, min(i + 10, n) + 1):    # 第二个数最多 10 位
            if num[i] == '0' and j - i > 1:          # 不能有前导零
                break
            b = int(num[i:j])
            if b > MAX_INT:
                break

            seq = [a, b]          # 当前尝试的斐波那契序列
            k = j                 # 下一段要匹配的起始下标

            # 依次生成后面的数，直到字符串用完或匹配失败
            while k < n:
                nxt = seq[-1] + seq[-2]
                if nxt > MAX_INT:               # 超出整数范围直接终止
                    break
                nxt_str = str(nxt)
                if not num.startswith(nxt_str, k):  # 前缀不匹配
                    break
                # 匹配成功，加入序列并移动指针
                seq.append(nxt)
                k += len(nxt_str)

            # 如果恰好用了完所有字符且序列长度 ≥ 3，则成功返回
            if k == n and len(seq) >= 3:
                return seq

    # 没有任何合法划分
    return []
```

> **关键行解释**  
> - `for i in range(1, min(10, n) + 1):` —— 第一个数最多 10 位（因为 `2^31-1` 是 10 位）。  
> - `if num[0] == '0' and i > 1: break` —— 防止 “01、001” 之类的前导零。  
> - `while k < n:` 循环里我们 **不再递归**，而是一次性生成下一个和并检查前缀，极大降低搜索空间。  
> - `if k == n and len(seq) >= 3:` —— 用光了整个字符串且序列长度不少于 3，说明找到了合法答案。

#### 复杂度

- **时间复杂度：** `O(n^3)`（在最坏情况下）  
  - 两层枚举前两个数：`O(n^2)`。  
  - 对每一组 `(i, j)`，最多遍历剩余字符一次：`O(n)`。  
  相比暴力解的指数级，这已经是线性多项式时间，`n ≤ 200` 时运行毫秒即可。

- **空间复杂度：** `O(1)`（不计答案列表）  
  只用了常数级的额外变量 `a, b, nxt, k` 等；答案本身 `seq` 只在找到合法解时返回，不算额外空间。

---

## 心得

- **核心技巧**：**先枚举前两项，后续唯一确定**。这是一种典型的“**确定前缀，线性验证后缀**”的思路，常用于需要满足递推关系的字符串划分题。  
- **适用的题型**（类似思路）  
  1. “**分割回文串**” – 枚举前缀是否为回文，后续递归。  
  2. “**按位相加得到目标**” – 先确定前几位，后面唯一决定。  
  3. “**等差数列划分**” – 枚举前两项，后面必须是前两项之差。  
- **一句话总结解题钥匙**：**“先锁定决定性的前两项，剩下的只能唯一推导”**。

---

## 反思

- **第一反应**：看到“斐波那契”立刻想到递归或回溯——把每一段都当作候选数，然后检查相邻三项的关系。  
- **最容易踩的坑**  
  1. **前导零**：`"0"` 本身合法，`"01"`、`"00"` 都不合法，需要在取子串时及时剪枝。  
  2. **整数溢出**：题目限制每个数 ≤ `2^31-1`，如果不检查会导致 Python 虽然不溢出但违背题意。  
  3. **长度剪枝**：单纯的指数回溯会在 `num` 长度 200 时超时，必须利用“前两项决定后续”来降低复杂度。  
- **下次遇到同类题**：第一步先 **固定几个关键的前缀（通常是前 1~2 项）**，判断它们是否合法后，再 **用线性或贪心方式验证剩余部分**，而不是盲目递归全部切分。这样能把搜索空间从指数级压到多项式级。