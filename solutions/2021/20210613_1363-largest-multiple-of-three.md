# #1363. 三的最大倍数 / Largest Multiple of Three

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/largest-multiple-of-three/)

---

## 题目（英文原版）

**Description**

Given an array of digits digits, return the largest multiple of three that can be formed by concatenating some of the given digits in any order. If there is no answer return an empty string.
Since the answer may not fit in an integer data type, return the answer as a string. Note that the returning answer must not contain unnecessary leading zeros.

**Examples**

**Example 1:**

```
Input: digits = [8,1,9]
Output: "981"
```

**Example 2:**

```
Input: digits = [8,6,7,1,0]
Output: "8760"
```

**Example 3:**

```
Input: digits = [1]
Output: ""
```

**Constraints**

- 1 <= digits.length <= 104
- 0 <= digits[i] <= 9

---

## 题目（中文翻译）

给定一个由数字（digits）组成的数组 `digits`，返回可以通过任意顺序拼接其中的部分数字而形成的**最大三的倍数**。如果不存在满足条件的答案，返回空字符串。  
由于答案可能超出整数数据类型的范围，需要以字符串形式返回。注意，返回的答案不能包含多余的前导零。

约束条件：

- `1 <= digits.length <= 10^4`
- `0 <= digits[i] <= 9`

示例 1:
```
Input: digits = [8,1,9]
Output: "981"
```

示例 2:
```
Input: digits = [8,6,7,1,0]
Output: "8760"
```

示例 3:
```
Input: digits = [1]
Output: ""
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把 **所有** 能够由给定数字组成的数都列举出来，挑出其中是 3 的倍数且最大的那一个。  
具体步骤如下：

1. **枚举子集**：从 `digits` 中挑选任意个数字（可以是 0 个、1 个、…、全部），这一步相当于把数字装进一个背包里。  
2. **枚举排列**：对每个子集，把选中的数字全部排个序（因为不同的排列会得到不同的整数）。  
3. **检查是否是 3 的倍数**：把排列好的数字拼成字符串，再把每位字符转成整数求和，判断 `sum % 3 == 0`。  
4. **记录最大值**：把满足条件的数按字典序（即数值大小）比较，保存最大的那个。

> **类比**：把哈希表想成一本字典，`key` 是单词，`value` 是页码；这里的「子集」就像把字典里任意几页撕下来，「排列」则是把撕下的页重新排顺序。

这种方法一定能得到正确答案，因为我们穷举了 **所有** 可能的组合和顺序，只要答案存在，就一定会被遍历到。

#### 代码（Python）  

```python
import itertools

def largestMultipleOfThree_bruteforce(digits):
    # 用集合去掉重复的结果，防止同一数字集合产生相同的字符串
    candidates = set()

    n = len(digits)
    # 1️⃣ 枚举子集：长度从 1 到 n（0 长度对应空串，不是合法答案）
    for r in range(1, n + 1):
        for subset in itertools.combinations(digits, r):
            # 2️⃣ 枚举排列：对当前子集全排列
            for perm in itertools.permutations(subset):
                # 把排列好的数字拼成字符串
                s = ''.join(map(str, perm))
                # 3️⃣ 判断是否是 3 的倍数
                digit_sum = sum(map(int, s))
                if digit_sum % 3 == 0:
                    # 去掉前导零（如 "000" → "0"），但保留单个 0
                    s = s.lstrip('0') or '0'
                    candidates.add(s)

    if not candidates:
        return ""                     # 没有合法答案

    # 4️⃣ 取最大（字符串比较在同等长度时等价于数值比较）
    return max(candidates, key=lambda x: (len(x), x))

# 示例
print(largestMultipleOfThree_bruteforce([8, 1, 9]))          # "981"
print(largestMultipleOfThree_bruteforce([8, 6, 7, 1, 0]))   # "8760"
print(largestMultipleOfThree_bruteforce([1]))               # ""
```

> **关键行中文注释**  
> - `itertools.combinations`：选出若干个数字的子集（不考虑顺序）。  
> - `itertools.permutations`：把子集里的数字全排列，得到所有可能的顺序。  
> - `s.lstrip('0') or '0'`：去掉不必要的前导零，只保留单个 0。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n!)`（极其庞大）  
  - 解释：子集数量是 `2^n`（每个数字保留或丢弃），每个子集内部需要遍历所有排列，最多是 `n!`，所以总体是指数级别的。  
- **空间复杂度**：`O(2^n * n)`  
  - 解释：我们把所有合法的字符串放进 `candidates` 集合，最坏情况下可能有指数个不同的候选答案。  

> 对于 `n` 只有几位的情况还能跑得动，但 `n` 达到 10⁴ 时根本不可行，这也是我们要寻找更优解的动机。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举全部子集和排列是最大瓶颈**。我们需要利用数学性质和贪心策略，直接在原数组上“裁剪”一些数字，使得剩下的数字拼成的最大数满足“能被 3 整除”。核心思路如下：

1. **3 的倍数判定**  
   - 一个整数能被 3 整除 ⇔ 它所有数字之和能被 3 整除。  
   - 因此，只要我们保证剩余数字的总和 `sum % 3 == 0`，最终拼出的数一定是 3 的倍数。  

2. **把数字按大小计数**  
   - 由于答案只要求“最大”，我们不必真的去排列所有数字，只要把它们 **从大到小** 输出即可。  
   - 用一个长度为 10 的计数数组 `cnt[0..9]` 记录每个数字出现的次数（相当于把数字装进 10 个格子的小抽屉）。  

3. **根据余数决定删掉哪些数字**  
   - 设 `total = sum(digits)`，`rem = total % 3`（余数只能是 0、1、2）。  
   - **如果 `rem == 0`**：已经满足条件，直接输出全部数字。  
   - **如果 `rem == 1`**：有两种办法让余数变为 0  
        a. 删除 **最小的一个** 余数为 1 的数字（如 1、4、7 中最小的）。  
        b. 若不存在余数为 1 的数字，删除 **两个** 余数为 2 的数字（如 2、5、8 中最小的两个）。  
   - **如果 `rem == 2`**：对称处理  
        a. 删除 **最小的一个** 余数为 2 的数字。  
        b. 若不存在余数为 2 的数字，删除 **两个** 余数为 1 的数字。  

   这一步是 **贪心**：我们总是尽量删掉 **最小** 的数字，因为删掉大的数字会让最终答案变小。  

4. **构造答案**  
   - 按数字从 9 到 0 的顺序，把计数数组中对应的数字加入结果字符串。  
   - 需要特别处理 **全是 0** 的情况：如果结果全部是 `'0'`，返回单个 `'0'` 而不是 `"000..."`。  

5. **如果删除后没有数字剩下**，返回空串 `""`（说明无法构成任何 3 的倍数）。  

> **类比**：想象你有一堆不同面值的硬币，要凑出总额能被 3 整除的最大金额。先把所有硬币都拿出来（总和可能不是 3 的倍数），如果多了 1 元，就把面值最小、余数为 1 的硬币扔掉；如果没有，就扔掉两枚面值最小、余数为 2 的硬币。最后把剩下的硬币从大到小排成一列，就是答案。  

#### 代码（Python）  

```python
def largestMultipleOfThree(digits):
    """
    返回可以由 digits 组成的、最大的 3 的倍数（字符串形式）。
    思路：计数 + 贪心删数 + 从大到小输出
    """
    # 1️⃣ 计数每个数字出现次数
    cnt = [0] * 10               # cnt[i] 表示数字 i 出现了多少次
    total = 0                    # 所有数字的和
    for d in digits:
        cnt[d] += 1
        total += d

    # 2️⃣ 根据余数决定删除哪些数字
    rem = total % 3
    if rem == 1:
        # 先尝试删除一个余数为 1 的最小数字
        if not _remove_one(cnt, [1, 4, 7]):
            # 若不存在余数为 1 的数字，删除两个余数为 2 的最小数字
            _remove_two(cnt, [2, 5, 8])
    elif rem == 2:
        # 对称处理
        if not _remove_one(cnt, [2, 5, 8]):
            _remove_two(cnt, [1, 4, 7])
    # 若 rem == 0，直接进入下一步

    # 3️⃣ 把剩余数字从大到小拼成答案
    res_parts = []
    for digit in range(9, -1, -1):
        if cnt[digit]:
            res_parts.append(str(digit) * cnt[digit])
    ans = ''.join(res_parts)

    # 4️⃣ 处理全 0 或空串的特殊情况
    if not ans:                # 没有任何数字留下
        return ""
    if ans[0] == '0':          # 最高位是 0，说明全是 0
        return "0"
    return ans


def _remove_one(cnt, candidates):
    """
    尝试删除 candidates 中**最小**的一个数字。
    返回 True 表示成功删除，False 表示 candidates 都不存在。
    """
    for d in sorted(candidates):   # 从小到大遍历
        if cnt[d] > 0:
            cnt[d] -= 1
            return True
    return False


def _remove_two(cnt, candidates):
    """
    删除 candidates 中**最小的两个**数字（可能是同一个数字两次）。
    """
    need = 2
    for d in sorted(candidates):
        while cnt[d] > 0 and need > 0:
            cnt[d] -= 1
            need -= 1
        if need == 0:
            break
    # 题目保证在调用此函数前一定有足够的数字可以删除
    return

# ------------------- 测试 -------------------
print(largestMultipleOfThree([8, 1, 9]))          # "981"
print(largestMultipleOfThree([8, 6, 7, 1, 0]))   # "8760"
print(largestMultipleOfThree([1]))               # ""
print(largestMultipleOfThree([0,0,0]))           # "0"
```

> **代码关键行解释**  
> - `cnt = [0] * 10`：把 0~9 十个抽屉准备好，像字典的 “key”。  
> - `rem = total % 3`：求总和除以 3 的余数，决定要删几颗“硬币”。  
> - `_remove_one` / `_remove_two`：分别负责删“一颗”或“二颗”最小的目标数字。  
> - `for digit in range(9, -1, -1)`：从 9 往 0 倒着取，直接得到最大排列。  

#### 复杂度  

- **时间复杂度**：`O(n + 10)` ≈ `O(n)`  
  - 解释：遍历一次数组统计计数是 `O(n)`，其余操作（求余数、删数、输出）只涉及常数大小的 10 个数字。  
- **空间复杂度**：`O(1)`（常数空间）  
  - 解释：只用了长度为 10 的计数数组和若干常数级的临时变量，与输入规模无关。  

> 与暴力解相比，时间从指数级降到线性，几乎可以处理题目给出的上限 `10⁴`，甚至更大。

---  

## 心得  

- **核心技巧**：利用“数字和能被 3 整除 ⇔ 余数为 0” 的数学性质，结合**计数 + 贪心删除最小数字**，直接得到最大可行答案。  
- **适用的题型**  
  1. “把数组中的数字拼成满足某个模数条件的最大数”——如 **Largest Multiple of Five**（模 5）等。  
  2. “在保留尽可能多元素的前提下，使总和满足某个约束”——如 **Subset Sum with Modulo**。  
  3. “在给定数字集合中，删除最少元素使其满足特定性质”——如 **Make Array Divisible by K**。  
- **一句话总结解题钥匙**：**先把所有数字按出现次数统计，再根据总和的余数贪心删掉最小的“破坏者”，最后倒序输出即得最大答案**。  

---  

## 反思  

- **拿到题目第一反应**：想到“枚举所有子集和排列”，因为这样最保险可以覆盖所有可能。  
- **最容易踩的坑**  
  1. **前导零**：答案不能出现多余的 `0`，需要在最终字符串里去掉多余的前导零，只保留单个 `0`。  
  2. **删除策略的顺序**：必须先尝试删除**最少**且**最小**的数字；若直接删两个大数字会导致答案不是最大。  
  3. **全是 0 的情况**：如果最终只剩下 `0`，返回 `"0"` 而不是空串或 `"000"`。  
- **下次遇到同类题的第一步**：**先计算整体的模数余数**，再决定是**删除 1 个还是 2 个**最小的“对应余数”数字；这一步往往可以把问题的搜索空间直接压到常数级。