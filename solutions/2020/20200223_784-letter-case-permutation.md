# #784. 字母大小写全排列 / Letter Case Permutation

> 难度：中等 · 标签：String、Backtracking、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/letter-case-permutation/)

---

## 题目（英文原版）

**Description**

Given a string s, you can transform every letter individually to be lowercase or uppercase to create another string.
Return a list of all possible strings we could create. Return the output in any order.

**Examples**

**Example 1:**

```
Input: s = "a1b2"
Output: ["a1b2","a1B2","A1b2","A1B2"]
```

**Example 2:**

```
Input: s = "3z4"
Output: ["3z4","3Z4"]
```

**Constraints**

- 1 <= s.length <= 12
- s consists of lowercase English letters, uppercase English letters, and digits.

---

## 题目（中文翻译）

给定一个字符串 `s`，你可以对其中的每个字母（letter）单独转换为小写或大写，从而生成另一条字符串。  
返回所有可能生成的字符串列表，输出顺序可以任意。

**示例 1**  
**输入**  
``` 
s = "a1b2"
```  
**输出**  
```json
["a1b2","a1B2","A1b2","A1B2"]
```

**示例 2**  
**输入**  
``` 
s = "3z4"
```  
**输出**  
```json
["3z4","3Z4"]
```

**约束条件**

- `1 <= s.length <= 12`
- `s` 仅由小写英文字母、大写英文字母和数字组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把每个字符逐个看一遍**，只要遇到字母，就有两种可能：保持原样（小写或大写），或者把它的大小写互换。  
我们可以把这个过程想象成**一次“选择树”**：  

- 树的根节点是空字符串  
- 每走到下一层，就往已经拼好的前缀后面 **加上** 当前字符的所有可能形式  
- 当走完所有字符后，就得到一个完整的结果  

这就是典型的**回溯（Backtracking）**思路。  
> 类比：把制作披萨的过程想成“先放面团 → 放酱 → 放配料”。每一步都有若干选择，所有选择的组合就是所有可能的披萨。  

因为题目长度最多只有 12，最多出现 12 个字母，所有组合数是 `2^k`（k 为字母个数），即最多 `2^12 = 4096`，完全在计算范围内，所以直接遍历全部组合即可得到正确答案。

#### 代码（Python）  
```python
from typing import List

def letterCasePermutation(s: str) -> List[str]:
    res = []                         # 用来保存所有合法的字符串

    def backtrack(idx: int, path: List[str]) -> None:
        """
        idx   : 当前处理到原字符串的下标
        path  : 已经拼好的字符列表（使用列表而不是字符串拼接，效率稍高）
        """
        if idx == len(s):            # 已经遍历完所有字符，得到一个完整答案
            res.append(''.join(path))
            return

        ch = s[idx]                  # 当前字符
        if ch.isdigit():             # 如果是数字，只有唯一一种写法
            path.append(ch)
            backtrack(idx + 1, path)
            path.pop()               # 回溯，撤销本次选择
        else:                        # 是字母，分别尝试小写和大写
            # 选小写
            path.append(ch.lower())
            backtrack(idx + 1, path)
            path.pop()

            # 选大写
            path.append(ch.upper())
            backtrack(idx + 1, path)
            path.pop()

    backtrack(0, [])
    return res
```

#### 复杂度  
- **时间复杂度：** `O(2^k * n)`  
  - 解释：`k` 是字母的个数，所有组合数是 `2^k`。每生成一个结果，需要把长度为 `n` 的字符列表拼成字符串，耗时 `O(n)`。所以整体是 `2^k` 种情况 × `n` 步操作。  
- **空间复杂度：** `O(n)`（递归栈 + 临时路径）  
  - 解释：递归深度最多 `n`（字符串长度），每层保存一个字符；结果列表本身不计入额外空间，因为它是题目要求的输出。

---  

### 2. 最优解  

#### 思路  
暴力解已经是最直接的枚举，**瓶颈**在于递归调用的函数开销以及每次拼接字符串的操作。  
我们可以把**“每个字母有两种状态”** 看成 **二进制位**，用整数的每一位来表示该字母是大写还是小写。  

具体步骤如下：

1. **先统计字母的位置**，记下它们在原串中的下标 `letter_idx`（例如 `"a1b2"` → `[0, 2]`）。  
2. 设字母个数为 `k`，则 `0 … (1 << k) - 1`（即 `0` 到 `2^k‑1`）的每一个整数，都对应一种大小写组合。  
3. 对每个整数 `mask`：  
   - 把原字符串转换成列表 `tmp = list(s)`，便于原地修改字符。  
   - 对第 `i` 个字母（`i` 从 `0` 开始），检查 `mask` 第 `i` 位是 `0` 还是 `1`：  
     - `0` → 用 **小写**（`tmp[letter_idx[i]] = s[letter_idx[i]].lower()`）  
     - `1` → 用 **大写**（`tmp[letter_idx[i]] = s[letter_idx[i]].upper()`）  
   - 将 `tmp` 合并成字符串加入答案。  

这样我们 **一次遍历** 完成所有组合，不需要递归，也不需要在每一步都创建临时字符串，只在生成答案时一次性拼接。

> 类比：把每个字母想成一个灯泡，灯泡可以开（大写）或关（小写）。`mask` 就是一串开关的状态码，遍历所有可能的开关组合，就能得到所有灯泡的点亮方式。

#### 代码（Python）  
```python
from typing import List

def letterCasePermutation(s: str) -> List[str]:
    # 1. 记录所有字母在原串中的下标
    letter_idx = [i for i, ch in enumerate(s) if ch.isalpha()]
    k = len(letter_idx)                     # 字母的数量

    total = 1 << k                          # 2^k 种组合
    ans: List[str] = []

    for mask in range(total):               # 依次枚举 0 … 2^k-1
        tmp = list(s)                       # 将字符串转为可修改的列表

        for i in range(k):                  # 逐个处理第 i 个字母
            pos = letter_idx[i]             # 该字母在原串中的位置
            if (mask >> i) & 1:             # mask 第 i 位是 1 → 选大写
                tmp[pos] = s[pos].upper()
            else:                           # 第 i 位是 0 → 选小写
                tmp[pos] = s[pos].lower()

        ans.append(''.join(tmp))            # 把列表拼成字符串加入结果

    return ans
```

#### 复杂度  
- **时间复杂度：** `O(2^k * n)`（与暴力解相同的量级）  
  - 解释：仍然需要遍历 `2^k` 种组合，每种组合要遍历所有 `k` 个字母并最终拼接 `n` 长度的字符串。相较于递归，这里常数因子更小，实际运行更快。  
- **空间复杂度：** `O(n)`  
  - 解释：只使用了一个长度为 `n` 的临时列表 `tmp`，以及记录字母下标的数组 `letter_idx`（最多 `n` 长），不随组合数增长。

---  

## 心得  

- **核心技巧**：把“每个字母有两种状态”抽象成二进制位，用 **位运算** 或 **回溯** 完全枚举所有组合。  
- **适用的题型**：  
  1. “所有子集” 类问题（如 LeetCode 78 Subsets）  
  2. “所有排列/组合” 中带有二元选择的情形（如 LeetCode 784 Letter Case Permutation 本题）  
  3. “二进制位枚举” 的状态压缩 DP（如 LeetCode 698 Partition to K Equal Sum Subsets）  
- **一句话总结解题钥匙**：**把每个可变的字符映射到一位二进制，遍历所有位模式即可得到全部可能**。

---  

## 反思  

- **第一反应**：看到“每个字母可以变大小写”，立刻想到“每个字母有两种选择”，于是想到回溯/DFS。  
- **最容易踩的坑**：  
  - 忘记对数字保持原样，只对字母进行大小写转换。  
  - 在递归实现里，`path.pop()` 写错位置导致路径没有正确回退，出现重复或缺失的结果。  
  - 位运算实现时，`mask >> i` 的顺序必须对应 `letter_idx` 的顺序，顺序错了会得到错误的大小写组合。  
- **下次遇到同类题**：**先判断“可变元素的数量”，如果 ≤ 20 左右，就可以直接用 **位掩码枚举** 或 **回溯** 完全搜索；先写出“每个位置的两种状态”，再决定使用递归还是位运算实现。