# #93. 恢复 IP 地址 / Restore IP Addresses

> 难度：中等 · 标签：String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/restore-ip-addresses/)

---

## 题目（英文原版）

**Description**

A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.
Given a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s. You are not allowed to reorder or remove any digits in s. You may return the valid IP addresses in any order.

**Examples**

**Example 1:**

```
Input: s = "25525511135"
Output: ["255.255.11.135","255.255.111.35"]
```

**Example 2:**

```
Input: s = "0000"
Output: ["0.0.0.0"]
```

**Example 3:**

```
Input: s = "101023"
Output: ["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]
```

**Constraints**

- 1 <= s.length <= 20
- s consists of digits only.

---

## 题目（中文翻译）

一个有效的 IP 地址 (IP address) 由恰好四个整数通过单个点 (dot) 分隔组成。每个整数的取值范围是 0 到 255（含），且不能有前导零。  
给定仅包含数字的字符串 `s`，返回所有可以通过在 `s` 中插入点而形成的有效 IP 地址。禁止重新排列或删除 `s` 中的任何数字。返回的有效 IP 地址顺序不限。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= s.length <= 20`  
- `s` 仅由数字组成。  

**示例**  

**示例 1:**  
```
Input: s = "25525511135"
Output: ["255.255.11.135","255.255.111.35"]
```

**示例 2:**  
```
Input: s = "0000"
Output: ["0.0.0.0"]
```

**示例 3:**  
```
Input: s = "101023"
Output: ["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切点全部枚举出来**，然后逐一检查每段是否满足 IP 地址的合法性。  
- 一个合法的 IP 由 **4 段** 组成，段之间用点 `.` 隔开。  
- 给定长度为 `n` 的字符串 `s`，我们只需要在 `s` 中挑选 **3 个位置** 作为切点，把字符串分成 4 段。  
- 对每一种切法，检查四段是否都在 `0~255` 且没有前导零（除了单独的 `"0"`）。  

这里用到的**数据结构**非常简单：只用到 **字符串切片**（`s[l:r]`）和 **列表**（收集合法的 IP）。  
可以把切点想象成 **在一根绳子上打结**，每打一个结就把绳子分成两段。我们要在绳子上打 **3** 个结，所有打法就是所有可能的切点组合。

为什么这个方法一定能找到所有答案？因为我们把 **所有** 可能的切点组合都尝试了一遍，只要某个组合对应的四段合法，就会被加入答案。

#### 代码（Python）

```python
def restore_ip_addresses_bruteforce(s: str):
    n = len(s)
    res = []

    # i、j、k 分别是第 1、2、3 个点左侧的字符个数（切点下标）
    for i in range(1, min(4, n - 2)):          # 第一段最多 3 位，且后面至少要留 3 位给剩下的段
        for j in range(i + 1, i + min(4, n - i - 1)):
            for k in range(j + 1, j + min(4, n - j)):
                # 把字符串切成四段
                seg1, seg2, seg3, seg4 = s[:i], s[i:j], s[j:k], s[k:]
                # 检查每段是否合法
                if all(is_valid(seg) for seg in (seg1, seg2, seg3, seg4)):
                    res.append(".".join([seg1, seg2, seg3, seg4]))
    return res


def is_valid(seg: str) -> bool:
    """判断一个子串是否能成为合法的 IP 段"""
    # 空串显然非法
    if not seg:
        return False
    # 不能有前导零，除非就是 "0"
    if seg[0] == '0' and len(seg) > 1:
        return False
    # 转成整数检查范围
    val = int(seg)
    return 0 <= val <= 255
```

> **关键行解释**  
> - `for i in range(1, min(4, n - 2))`：第一段长度只能是 1~3，且剩下的字符至少要能分成 3 段（每段最少 1 位）。  
> - `is_valid`：先判断是否有前导零，再把字符串转成整数检查是否在 `[0,255]`。  

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 我们用了三层循环，每层最多遍历 `3` 次（因为每段最长 3 位），所以总体是常数级的立方。  
  - 用大白话说，就是如果字符串长度是 12（最大可能形成合法 IP），我们最多检查 `3 * 3 * 3 = 27` 种切法，几乎可以忽略不计。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只用了若干个临时变量，和输入长度无关。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于我们对所有切点组合都枚举，即使很多组合在早期就已经可以判定为非法（例如某段已经大于 255，或者出现前导零）。我们可以在**构造 IP 段的过程中**就把非法分支剪掉，这就是 **回溯（Backtracking）** 的思想。

优化步骤：

1. **逐段尝试**：从左到右一次生成一个段。每次取 `1~3` 位字符作为当前段的候选。  
2. **提前剪枝**：  
   - 如果候选段以 `'0'` 开头且长度大于 1，直接舍弃（因为会产生前导零）。  
   - 把候选段转成整数后若 >255，也直接舍弃。  
3. **递归继续**：若当前段合法，就把它加入临时路径 `path`，递归处理剩余的字符串，并把已经形成的段数 `segment_count` 加 1。  
4. **终止条件**：  
   - 当已经得到 **4 段** 且字符串已经全部用完时，说明找到一个合法 IP，加入答案。  
   - 任何其他情况（段数已达 4 但还有字符未用完，或字符已用完但段数不足 4）都直接返回，不继续搜索。  

这样我们只会遍历**合法的分支**，极大减少不必要的检查。由于每一步最多尝试 3 种长度，且最多递归 4 层，实际运行时间非常快。

> **类比**：把生成 IP 看成在 **树形结构** 中找叶子。每层代表一段，每个节点代表一种取法（1、2、3 位），剪枝相当于在树上砍掉明显不通往答案的枝干。

#### 代码（Python）

```python
def restore_ip_addresses(s: str):
    """
    回溯法恢复所有合法的 IP 地址。
    """
    res = []
    path = []          # 当前已经确定的段，长度最多 4

    def backtrack(start: int):
        """
        start: 当前要从 s 的哪个下标开始切下一个段
        """
        # 已经取了 4 段但仍有剩余字符 → 歧路，直接返回
        if len(path) == 4:
            if start == len(s):          # 正好用完所有字符 → 合法答案
                res.append(".".join(path))
            return

        # 剩余字符不够或太多也可以提前返回（可选优化）
        # 例如还剩 2 段，却只剩 1 位字符 → 必然不合法
        remaining = 4 - len(path)        # 还需要几段
        # 每段最少 1 位，最多 3 位
        if len(s) - start < remaining or len(s) - start > remaining * 3:
            return

        # 取 1~3 位作为当前段的候选
        for length in range(1, 4):
            if start + length > len(s):   # 越界直接停止
                break
            seg = s[start:start + length]

            # 剪枝：前导零
            if seg[0] == '0' and length > 1:
                continue
            # 剪枝：数值超出 255
            if int(seg) > 255:
                continue

            # 选定当前段，进入下一层递归
            path.append(seg)
            backtrack(start + length)
            path.pop()                    # 恢复现场，尝试下一个候选

    backtrack(0)
    return res
```

> **关键行解释**  
> - `if len(path) == 4:`：已经凑够四段，只有在恰好用完字符串时才算成功。  
> - `if len(s) - start < remaining or len(s) - start > remaining * 3:`：提前判断剩余字符是否有可能恰好填满剩下的段，若不可能直接返回，进一步减少搜索。  
> - `if seg[0] == '0' and length > 1:`：剪掉所有会产生前导零的分支。  
> - `if int(seg) > 255:`：剪掉超过 255 的分支。  

#### 复杂度

- **时间复杂度**：`O(3^4)`（常数级）  
  - 每一层最多尝试 3 种长度，最多递归 4 层，所以最坏情况是 `3⁴ = 81` 次递归调用。  
  - 由于剪枝，大多数情况下会更少。用大白话说，这相当于只检查了几十种可能，几乎可以忽略不计。  
- **空间复杂度**：`O(4)`（递归栈 + 临时路径）  
  - 递归深度最多 4，`path` 最多保存 4 段字符串，都是常数级的额外空间。  

---

## 心得

- 这道题的核心技巧是 **回溯 + 剪枝**，尤其是对「前导零」和「数值范围」的提前判断。  
- 类似的技巧可以用在：  
  1. **电话号码字母组合**（Letter Combinations of a Phone Number）——逐位选择字符并剪枝。  
  2. **括号生成**（Generate Parentheses）——在递归树中剪掉不合法的括号序列。  
  3. **分割回文子串**（Palindrome Partitioning）——利用回溯生成所有合法的分割。  
- **一句话总结**：把「逐段构造」和「非法立即抛弃」结合起来，就能快速遍历所有合法 IP。  

---

## 反思

- **第一反应**：先想到枚举所有切点（暴力），因为只有 4 段，枚举看起来最直接。  
- **最容易踩的坑**：  
  - **前导零**：`"01"`、`"00"` 等必须排除。  
  - **数值范围**：`"256"`、`"999"` 等超过 255 的段不能接受。  
  - **边界情况**：长度小于 4 或大于 12 的字符串根本不可能组成合法 IP，需要提前返回。  
- **下次类似题的第一步**：先判断**是否有剪枝条件**（长度、取值范围、特殊字符），再决定是暴力枚举还是回溯搜索。这样可以避免无效的搜索，直接走向最优解。