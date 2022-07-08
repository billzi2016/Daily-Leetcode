# #1849. 将字符串拆分为递减的连续数值 / Splitting a String Into Descending Consecutive Values

> 难度：中等 · 标签：String、Backtracking、Enumeration · [LeetCode 链接](https://leetcode.com/problems/splitting-a-string-into-descending-consecutive-values/)

---

## 题目（英文原版）

**Description**

You are given a string s that consists of only digits.
Check if we can split s into two or more non-empty substrings such that the numerical values of the substrings are in descending order and the difference between numerical values of every two adjacent substrings is equal to 1.
Return true if it is possible to split s​​​​​​ as described above, or false otherwise.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "1234"
Output: false
Explanation: There is no valid way to split s.
```

**Example 2:**

```
Input: s = "050043"
Output: true
Explanation: s can be split into ["05", "004", "3"] with numerical values [5,4,3].
The values are in descending order with adjacent values differing by 1.
```

**Example 3:**

```
Input: s = "9080701"
Output: false
Explanation: There is no valid way to split s.
```

**Constraints**

- 1 <= s.length <= 20
- s only consists of digits.

---

## 题目（中文翻译）

你得到一个仅由数字组成的字符串 `s`。  
判断是否可以把 `s` 拆分成两个或更多的非空子串（substring），使得这些子串对应的数值严格递减，并且任意相邻两个子串的数值之差恰好等于 1。  
如果可以按上述方式拆分，返回 `true`；否则返回 `false`。  

**子串** 是字符串中连续的字符序列。

### 示例

**示例 1**  
**输入**: `s = "1234"`  
**输出**: `false`  
**解释**: 没有任何合法的拆分方式。

**示例 2**  
**输入**: `s = "050043"`  
**输出**: `true`  
**解释**: `s` 可以拆分为 `["05", "004", "3"]`，对应的数值为 `[5, 4, 3]`。  
这些数值递减且相邻数值之差均为 1。

**示例 3**  
**输入**: `s = "9080701"`  
**输出**: `false`  
**解释**: 没有任何合法的拆分方式。

### 约束条件

- `1 <= s.length <= 20`
- `s` 只包含数字字符。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的切分方式都列出来」，然后逐个检查它们的数值是否满足：

1. 每一段都是非空的连续子串。  
2. 各段对应的整数严格递减，且相邻两段的差恰好为 `1`。  

这类似于「把一根绳子剪成若干段」的过程：我们从左到右，每隔一个位置就可以决定「剪」还是「不剪」。把所有「剪」的位置的组合枚举出来，就相当于把所有可能的切分方式列举完了。

**用到的数据结构**  

- **递归（回溯）**：把「在当前位置要不要剪」的二选一过程用函数调用的方式实现。递归相当于「在树形结构上深度优先搜索」每一种切分方案。  
- **列表**：暂时保存已经切好的子串（或者对应的整数），方便在递归返回时回溯（撤销上一步的切分）。  
- **整数转换**：把子串 `sub` 转成整数 `int(sub)`，这一步就像「查字典」——把字符串（词）映射到它对应的数值（页码）。

**为什么这个方法一定能得到正确答案**  

因为我们把 **所有** 合法的切分方式都尝试了一遍，只要有一种满足「递减且相邻差 1」的切分，就会在遍历的某个节点返回 `True`。如果遍历结束仍未找到，则说明不存在满足条件的切分，返回 `False`。

**时间/空间复杂度的大白话解释**  

- **时间复杂度**：长度为 `n` 的字符串有 `2^(n-1)` 种切分方式（每个位置要不要剪，除最后一个位置外），最坏情况下我们都要检查一次，所以时间复杂度是 **指数级** `O(2^n)`。把 `2^n` 想象成「每增加一个字符，可能的切分方式就会翻倍」。
- **空间复杂度**：递归深度最多为 `n`（每个字符都单独成段），再加上保存当前切分的列表，空间复杂度是 **线性** `O(n)`。

#### 代码（Python）

```python
def splitString(s: str) -> bool:
    """
    暴力回溯：尝试所有切分方式，只要有一种满足
    “递减且相邻差 1”，就返回 True。
    """

    n = len(s)

    # dfs(pos, prev) 表示从位置 pos 开始继续切分，
    # prev 为前一个子串对应的整数（如果 prev 为 None，说明还没有切出第一段）
    def dfs(pos: int, prev: int) -> bool:
        # 已经划到字符串末尾，说明切分成功且至少有两段
        if pos == n:
            return prev is not None  # 至少切出过一次

        # 从当前位置往后尝试每一种可能的子串长度
        for end in range(pos + 1, n + 1):
            cur_str = s[pos:end]          # 当前子串
            cur_val = int(cur_str)        # 把子串转成整数

            # 如果已经有前一个数，必须满足递减且相差 1
            if prev is not None and not (prev - cur_val == 1):
                continue  # 不满足条件，直接尝试更长的子串

            # 递归检查后面的部分
            if dfs(end, cur_val):
                return True

        # 所有可能都不行，返回 False
        return False

    # 初始时没有前一个数，用 None 作为占位
    return dfs(0, None)
```

#### 复杂度

- **时间复杂度**：`O(2^n)` — 解释：每个字符后面都有「剪」或「不剪」两种选择，所有组合共 `2^(n-1)` 种，最坏情况下都要遍历一次。
- **空间复杂度**：`O(n)` — 解释：递归调用栈的深度最多等于字符串长度 `n`，再加上保存当前子串的列表（实际在代码里用函数参数实现），所以用的额外空间随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

虽然题目只要求 `n ≤ 20`，暴力解已经足够快，但我们仍可以 **在枚举的过程中做剪枝**，把搜索空间显著压缩，使算法在更大的输入下也能保持高效。

**慢在哪里？**  
暴力解每次尝试子串时，都会把它转成整数并检查「前后差是否为 1」。如果前一个数已经很大，而当前子串很长，`int(cur_str)` 可能会非常大，且我们仍会继续往下递归，导致大量不必要的搜索。

**优化思路**  

1. **利用前一个数的大小限制当前子串的长度**  
   - 已知 `prev`（前一个数），下一个数必须是 `prev - 1`。所以我们只需要尝试能得到 `prev-1` 的子串，而不必尝试更长的子串。  
   - 具体做法是：把目标值 `target = prev - 1` 当作字符串 `target_str = str(target)`，然后只检查 `s[pos:pos+len(target_str)]` 是否等于 `target_str`（要考虑前导零的情况）。如果相等，就直接递归；否则直接返回 `False`。  

2. **特殊处理首段**  
   - 首段没有前驱数，我们可以枚举它的长度（从 1 到 `n-1`），得到 `first = int(s[:len])`，随后把目标值设为 `first - 1` 开始递归。  

3. **前导零的容忍**  
   - 题目允许子串有前导零，只要它们对应的整数满足递减条件即可。例如 `"05"` → `5`，`"004"` → `4`。所以在比较时只需要比较整数值，而不是直接比较子串是否相同。

**核心算法：受限递归 + 字符串匹配**  
把「枚举所有切分」改成「每一步只尝试唯一可能的下一段」，相当于把搜索树的分支数从 `O(2^n)` 降到了 `O(n)`（最多尝试 `n` 种首段长度）。

**类比**  
想象你在玩「数数递减」的游戏：老师先说一个数 `10`，你只能接 `9`，接下来只能接 `8`……每一步只能说唯一的下一个数，根本不需要去考虑别的选项。我们把这种「只能说唯一答案」的规则搬到了字符串切分上。

#### 代码（Python）

```python
def splitString(s: str) -> bool:
    """
    优化版回溯：每一步只尝试唯一可能的下一段（prev-1），
    大幅降低搜索分支。
    """

    n = len(s)

    # 递归函数：从位置 pos 开始，期待的下一个整数是 target
    def dfs(pos: int, target: int) -> bool:
        # 已经到达字符串末尾，说明成功切分
        if pos == n:
            return True

        # 目标整数转成字符串（可能有前导零的情况）
        target_str = str(target)

        # 如果剩余字符不足以容纳 target_str，直接失败
        if pos + len(target_str) > n:
            return False

        # 取出对应长度的子串
        cur_sub = s[pos:pos + len(target_str)]

        # 把子串转成整数比较
        if int(cur_sub) != target:
            return False

        # 递归检查后面的部分，目标值继续减 1
        return dfs(pos + len(target_str), target - 1)

    # 枚举第一段的长度（至少保留一个字符给后面）
    for first_len in range(1, n):
        first_val = int(s[:first_len])          # 第一个整数
        # 从下一个位置开始，期待的下一个数是 first_val-1
        if dfs(first_len, first_val - 1):
            return True

    return False
```

#### 复杂度

- **时间复杂度**：`O(n^2)`（实际更接近 `O(n)`）  
  - 解释：我们枚举首段的长度 `O(n)`，每次递归只会检查一次对应的子串，子串比较的代价最多是 `O(n)`（因为要截取字符串），所以整体是 `O(n^2)`。在实际运行时，由于每一步只有唯一分支，常数非常小，远快于指数级暴力。
- **空间复杂度**：`O(n)`  
  - 解释：递归深度最多等于切分的段数，最坏情况是每段长度为 1，深度为 `n`，因此使用的栈空间随 `n` 线性增长。

---

## 心得

- **核心技巧**：利用「相邻数差为 1」的强约束，把每一步的选择压缩到唯一可能的长度，从而把指数搜索降到线性搜索。  
- **适用的题型**  
  1. **连续递减/递增数列的切分**（如 LeetCode 1849 `Splitting a String Into Descending Consecutive Values`）。  
  2. **按照固定差值递增/递减的数列检查**（如检查是否能把数字序列分成等差数列）。  
  3. **字符串匹配+数值约束** 的组合问题（比如「把数字字符串划分成等差数列」）。
- **一句话总结解题钥匙**：**把“只能往下走一步”的约束转化为唯一的子串长度**，让搜索从「全图遍历」变成「顺着唯一路径前进」。

---

## 反思

- **第一反应**：看到「两两相邻差 1」立刻想到「回溯」——把所有切法枚举出来检查。  
- **最容易踩的坑**  
  - **前导零**：子串可以有前导零，但 `int('001') == 1`，所以比较时要转成整数，而不是直接比较子串字符。  
  - **必须切成两段以上**：如果只切出一段（整个字符串本身），答案应为 `False`。在实现时要确保递归结束时已经切出了至少一段。  
  - **目标值为负数**：当 `prev` 为 `0` 时，`prev-1` 为 `-1`，此时必然失败，需要在递归入口提前返回。  
- **下次遇到同类题**：第一步先思考「相邻元素之间有没有固定的数学关系」——如果有，就尝试把这种关系转化为 **唯一的下一步**，从而把搜索空间压到最小。这样往往能从暴力的「枚举所有」直接跳到「按规则唯一推进」。