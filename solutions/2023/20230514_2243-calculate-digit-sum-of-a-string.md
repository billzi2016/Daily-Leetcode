# #2243. 计算字符串的数字和 / Calculate Digit Sum of a String

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/calculate-digit-sum-of-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of digits and an integer k.
A round can be completed if the length of s is greater than k. In one round, do the following:
Return s after all rounds have been completed.

**Examples**

**Example 1:**

```
Input: s = "11111222223", k = 3
Output: "135"
Explanation: 
- For the first round, we divide s into groups of size 3: "111", "112", "222", and "23".
  ​​​​​Then we calculate the digit sum of each group: 1 + 1 + 1 = 3, 1 + 1 + 2 = 4, 2 + 2 + 2 = 6, and 2 + 3 = 5. 
  So, s becomes "3" + "4" + "6" + "5" = "3465" after the first round.
- For the second round, we divide s into "346" and "5".
  Then we calculate the digit sum of each group: 3 + 4 + 6 = 13, 5 = 5. 
  So, s becomes "13" + "5" = "135" after second round. 
Now, s.length <= k, so we return "135" as the answer.
```

**Example 2:**

```
Input: s = "00000000", k = 3
Output: "000"
Explanation: 
We divide s into "000", "000", and "00".
Then we calculate the digit sum of each group: 0 + 0 + 0 = 0, 0 + 0 + 0 = 0, and 0 + 0 = 0. 
s becomes "0" + "0" + "0" = "000", whose length is equal to k, so we return "000".
```

**Constraints**

- 1 <= s.length <= 100
- 2 <= k <= 100
- s consists of digits only.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅包含数字字符的字符串 `s` 和一个整数 `k`。  
只要 `s` 的长度大于 `k`，就可以进行一轮操作。每一轮的操作如下：

1. 将 `s` 按照大小为 `k` 的连续子串（subarray）划分，最后一个子串可能不足 `k`。  
2. 对每个子串，计算其所有数字的和（digit sum），并将该和转换为十进制字符串。  
3. 将所有得到的字符串按顺序连接，形成新的 `s`。

当 `s` 的长度不再大于 `k` 时，结束所有轮次，返回最终的 `s`。

**示例 1**  
```
Input: s = "11111222223", k = 3
Output: "135"
Explanation:
- 第 1 轮：将 s 划分为 "111", "112", "222", "23"。
  计算每组的数字和得到 3、4、6、5，拼接后 s 变为 "3465"。
- 第 2 轮：将 s 划分为 "346", "5"。
  计算数字和得到 13、5，拼接后 s 变为 "135"。
此时 s 的长度等于 k，结束并返回 "135"。
```

**示例 2**  
```
Input: s = "00000000", k = 3
Output: "000"
Explanation:
将 s 划分为 "000", "000", "00"。
每组的数字和均为 0，拼接后得到 "000"。此时长度等于 k，返回 "000"。
```

**约束条件**  

- `1 <= s.length <= 100`
- `2 <= k <= 100`
- `s` 仅由数字字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一步一步模拟题目描述的过程**：

1. 只要当前字符串 `s` 的长度大于 `k`，就进入一轮循环。  
2. 把 `s` 按照 **每 `k` 位一组** 切分（最后一组可能不足 `k` 位）。  
3. 对每一组，计算组内所有字符对应的数字之和（把字符 `'0'~'9'` 当成数字），得到一个新的数字。  
4. 把每一组得到的数字依次拼接成新的字符串 `s`，进入下一轮。

> **类比**：把 `s` 看成一串数字珠子，`k` 是一次可以抓住的珠子数量。每抓一把，就把这把珠子称重（求和），把称重的结果写下来，形成新的一串珠子。只要珠子太长（>k），就继续抓。

**为什么一定会得到正确答案**  
题目说“在每一轮里把字符串分组、求每组的数字和、再拼接”，我们的模拟**完全照搬**了这一步骤，且循环终止条件（长度 ≤ k）与题目一致，所以必然得到题目要求的最终字符串。

**复杂度分析（大白话）**  
- 每一轮我们要遍历一次当前字符串，时间随字符串长度线性增长。  
- 最坏情况下 `k = 2`，每轮长度大约会减半（因为每两位会合并成一个数），所以最多会有 `log₂(100) ≈ 7` 轮。  
- 因此总体时间复杂度是 **O(n log n)**，这里的 `n` 是原始字符串长度（≤ 100），在实际数据里几乎是瞬间完成。  
- 我们只用到了几个临时变量和一个新建的字符串，额外空间随字符串长度线性增长，**空间复杂度 O(n)**。

#### 代码（Python）

```python
def digit_sum_string(s: str, k: int) -> str:
    """
    按题目要求模拟多轮分组求和，直至长度 <= k
    :param s: 只包含数字字符的字符串
    :param k: 每组的最大长度
    :return: 最终得到的字符串
    """
    # 只要长度大于 k，就继续做一轮
    while len(s) > k:
        groups = []                     # 用来存放每一组的求和结果（字符串形式）
        # i 以步长 k 遍历，切片得到每一组
        for i in range(0, len(s), k):
            part = s[i:i + k]           # 当前组，可能不足 k 位
            # 把字符转成整数并求和，sum(...) 本身就是 O(组长) 的遍历
            total = sum(int(ch) for ch in part)
            groups.append(str(total))   # 把求和结果转回字符，准备拼接
        # 把所有组的结果拼成新的 s，进入下一轮
        s = ''.join(groups)
    return s
```

#### 复杂度

- **时间复杂度**：`O(n log n)`（`n` 为初始字符串长度）。  
  - 直观理解：每轮遍历一次当前字符串，轮数最多是 `log_k(n)`，所以总工作量约为 `n + n/k + n/k² + … ≤ n·log_k(n)`。  
- **空间复杂度**：`O(n)`。  
  - 需要额外的列表 `groups` 和拼接后的新字符串，最大长度不超过原始字符串长度。

---

### 2. 最优解

#### 思路  

暴力解已经非常接近题目的真实要求，**瓶颈**只在于我们每轮都重新创建列表和新字符串。实际上我们可以在 **同一次遍历中直接构造新字符串**，省掉额外的列表，从而把空间使用降到 **O(1)**（不计输出本身的空间）。

优化步骤：

1. **一次遍历完成分组求和**：用两个指针  
   - `i` 标记当前遍历的位置（从 `0` 开始）。  
   - `cnt` 记录已经累计了多少位（不超过 `k`）。  
   当 `cnt` 达到 `k` 或遍历到字符串末尾时，说明一组结束，立即把累计的和写入结果字符串。  
2. **循环结束后直接返回**：如果本轮结束后长度仍 > k，继续下一轮（同样的过程），直到满足终止条件。  
3. **原地修改**：我们只用一个变量 `new_s` 保存本轮的结果，然后把 `s` 替换为 `new_s`，循环继续。这样除了存放 `s` 本身外，只需要常数个临时变量。

> **类比**：想象我们在流水线上加工珠子。以前我们把每一把珠子装进篮子再去称重，篮子就是额外的列表。现在我们把称重的结果直接写在纸上，省掉篮子——纸上写的就是新字符串。

**复杂度**  
- **时间**：每轮仍然需要遍历一次当前字符串，轮数仍是 `log_k(n)`，所以 **O(n log n)**（与暴力解相同的数量级）。  
- **空间**：只用了常数个额外变量，**O(1)**（不计返回值本身），比暴力的 `O(n)` 更省内存。

#### 代码（Python）

```python
def digit_sum_string_opt(s: str, k: int) -> str:
    """
    更省空间的实现：在一次遍历中直接构造新字符串。
    """
    while len(s) > k:
        new_s = []          # 用列表收集字符，最后一次性 join，避免字符串频繁拼接
        total = 0           # 当前组的数字和
        cnt = 0             # 当前组已经累计了多少位

        for ch in s:
            total += int(ch)    # 累加当前字符对应的数字
            cnt += 1
            # 当累计到 k 位，或者已经是最后一个字符时，结束本组
            if cnt == k:
                new_s.append(str(total))
                total = 0
                cnt = 0
        # 循环结束后可能还有剩余不足 k 位的字符
        if cnt:                 # cnt>0 表示还有未写入的组
            new_s.append(str(total))

        s = ''.join(new_s)      # 把本轮的结果变成新的 s，进入下一轮
    return s
```

#### 复杂度

- **时间复杂度**：`O(n log n)`，与直觉解相同，只是常数因子更小。  
- **空间复杂度**：`O(1)`（不计最终返回的字符串），因为我们只使用了几个整型变量和一次性拼接的临时列表。

---

## 心得

- **核心技巧**：**模拟 + 分组求和**。关键在于把“每 `k` 位一组”这一步实现得既直观又高效。  
- **适用场景**：  
  1. **分组统计**：如 LeetCode 1132 *"Reporting the Number of Subarrays With Minimum Sum"*（分组累加）。  
  2. **分段压缩**：如 2244 *"Minimum Rounds to Complete All Tasks"*（把任务分批处理）。  
  3. **迭代聚合**：如 1658 *"Minimum Operations to Reduce X to Zero"*（不断合并区间）。  
- **一句话总结解题钥匙**：**把大问题拆成“小组”，每组只做一次简单的求和，循环直到满足结束条件**。

---

## 反思

- **第一反应**：看到“把字符串每 k 位分组，求每组的数字和”，立刻想到 **直接模拟**，因为数据规模非常小（≤ 100）。  
- **最容易踩的坑**：  
  - **最后一组可能不足 k 位**，必须单独处理，否则会丢失字符。  
  - **把字符转成整数**时要用 `int(ch)`，不能直接相加字符。  
  - 循环终止条件必须是 **长度 ≤ k**，而不是 “等于 k”。  
- **下次遇到同类题**，第一步应想到：**“是否可以一次遍历完成分组操作？”**，如果可以，就立刻写出类似的 **指针+计数** 模板，避免不必要的额外容器。