# #1980. 寻找唯一的二进制字符串 / Find Unique Binary String

> 难度：中等 · 标签：Array、Hash Table、String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/find-unique-binary-string/)

---

## 题目（英文原版）

**Description**

Given an array of strings nums containing n unique binary strings each of length n, return a binary string of length n that does not appear in nums. If there are multiple answers, you may return any of them.

**Examples**

**Example 1:**

```
Input: nums = ["01","10"]
Output: "11"
Explanation: "11" does not appear in nums. "00" would also be correct.
```

**Example 2:**

```
Input: nums = ["00","01"]
Output: "11"
Explanation: "11" does not appear in nums. "10" would also be correct.
```

**Example 3:**

```
Input: nums = ["111","011","001"]
Output: "101"
Explanation: "101" does not appear in nums. "000", "010", "100", and "110" would also be correct.
```

**Constraints**

- n == nums.length
- 1 <= n <= 16
- nums[i].length == n
- nums[i] is either '0' or '1'.
- All the strings of nums are unique.

---

## 题目（中文翻译）

给定一个字符串数组 `nums`，其中包含 **n** 个互不相同的二进制字符串，每个字符串的长度均为 **n**。返回一个长度为 **n** 的二进制字符串，使其不出现在 `nums` 中。如果存在多个答案，你可以返回任意一个。

**示例 1**  
Input: `nums = ["01","10"]`  
Output: `"11"`  
Explanation: `"11"` **未** 出现在 `nums` 中。`"00"` 也是一个正确答案。

**示例 2**  
Input: `nums = ["00","01"]`  
Output: `"11"`  
Explanation: `"11"` **未** 出现在 `nums` 中。`"10"` 也是一个正确答案。

**示例 3**  
Input: `nums = ["111","011","001"]`  
Output: `"101"`  
Explanation: `"101"` **未** 出现在 `nums` 中。`"000"`、`"010"`、`"100"` 和 `"110"` 也都是正确答案。

**约束条件**  

- `n == nums.length`  
- `1 <= n <= 16`  
- `nums[i].length == n`  
- `nums[i]` 仅由字符 `'0'` 或 `'1'` 组成  
- `nums` 中的所有字符串互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的长度为 `n` 的二进制字符串都列举出来，然后在这些候选里挑一个不在 `nums` 中的返回。  
- **数据结构**：把 `nums` 放进一个 **哈希集合**（`set`），就像把字典装进抽屉，想找某个单词（这里是某个二进制串）是否存在，只需要直接打开抽屉查一次，时间几乎是 `O(1)`。  
- **正确性**：所有长度为 `n` 的二进制串一共有 `2^n` 个，而 `nums` 只包含 `n` 个（题目保证 `nums` 长度恰好等于 `n`），所以必然还有未被占用的串。只要我们遍历完所有 `2^n` 种可能，必定能找到一个不在集合里的。  

**时间复杂度**  
- 生成每个候选串需要 `O(n)`（因为要把数字转成二进制字符串，长度是 `n`）。  
- 候选总数是 `2^n`，所以整体时间是 `O(n·2^n)`。  
  用大白话说，就是“随 `n` 指数增长”，当 `n=16` 时，`2^16 = 65536`，在电脑上还能跑，但已经不是最优的做法。  

**空间复杂度**  
- 哈希集合存 `n` 条字符串，需要 `O(n·n)`（每条长度 `n`），简记为 `O(n²)`。  
- 递归或循环中临时生成的候选串最多只有一个，算作 `O(n)`，整体仍是 `O(n²)`（因为 `n` 很小，这个空间开销可以接受）。

#### 代码（Python）

```python
from typing import List

def findDifferentBinaryString(nums: List[str]) -> str:
    n = len(nums)                     # 二进制串的长度，也是数组的长度
    existing = set(nums)              # 把所有已出现的串放进哈希集合，查找 O(1)

    # 从 0 到 2^n-1 枚举所有可能的二进制数
    for mask in range(1 << n):        # 1 << n 等价于 2 的 n 次方
        # 把整数 mask 转成长度为 n 的二进制字符串，前面补零
        candidate = format(mask, f'0{n}b')
        if candidate not in existing:    # 哈希集合查询是否已经出现
            return candidate             # 找到第一个未出现的直接返回
    # 题目保证一定能找到，这行理论上不会执行
    return ""
```

#### 复杂度

- **时间复杂度**：`O(n·2^n)`  
  解释：我们遍历 `2^n` 种可能，每次都要把整数转成长度为 `n` 的字符串（`O(n)`），所以乘起来就是 `O(n·2^n)`。  
- **空间复杂度**：`O(n²)`  
  解释：哈希集合里存 `n` 条长度为 `n` 的字符串，约等于 `n·n`，再加上常数级的临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举全部 2^n 种可能是多余的**。我们只需要 **构造** 一个必定不在 `nums` 中的串即可。  
- **瓶颈**：暴力解的时间随 `2^n` 指数增长，虽然 `n ≤ 16` 仍可接受，但不够“优雅”。  
- **关键观察**（来源于“对角线论证”）  
  把 `nums` 看成一个 `n × n` 的矩阵，每行是一条二进制串，第 `i` 行第 `i` 列的字符记为 `nums[i][i]`。如果我们把第 `i` 行第 `i` 列的字符 **取反**（`0→1`，`1→0`），得到的新字符记作 `ans[i]`，则得到的串 `ans` 与每一行的第 `i` 位必然不同。  
  换句话说，`ans` 与第 `i` 行的 **第 i 位** 不同，于是 `ans` 不可能完全等于第 `i` 行的整个字符串。因为 `nums` 里每一行都是唯一的，`ans` 与所有行都至少有一位不同，所以 `ans` 一定不在 `nums` 中。  

- **实现细节**  
  1. 直接遍历 `i = 0 … n-1`，读取 `nums[i][i]`（第 i 行第 i 列的字符）。  
  2. 若是 `'0'` 则改成 `'1'`，若是 `'1'` 则改成 `'0'`，把结果放进答案的第 i 位。  
  3. 最终把字符列表合并成字符串返回。  

- **类比**：想象有 `n` 本不同的字典，每本字典的第 `i` 页码（第 `i` 位）都不相同。如果我们把每本字典的第 `i` 页码都翻到相反的方向（奇数翻成偶数，偶数翻成奇数），得到的这本“新字典”必然没有出现在原来的任何一本里。

#### 代码（Python）

```python
from typing import List

def findDifferentBinaryString(nums: List[str]) -> str:
    n = len(nums)               # 同时是字符串长度和数组长度
    ans_chars = []              # 用来逐位收集答案字符

    for i in range(n):
        # 取第 i 行第 i 列的字符
        cur = nums[i][i]
        # 取反：'0' -> '1' , '1' -> '0'
        flipped = '1' if cur == '0' else '0'
        ans_chars.append(flipped)   # 把取反后的字符加入答案

    # 把字符列表拼成最终的二进制字符串
    return ''.join(ans_chars)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：只遍历一次数组，每次只做常数时间的字符比较和取反，整体随 `n` 线性增长。相较于暴力的 `O(n·2^n)`，快了指数级。  
- **空间复杂度**：`O(n)`  
  解释：我们只额外用了一个长度为 `n` 的字符列表来存答案（返回值本身也需要 `n` 长度），不随输入规模增长。

---

## 心得

- **核心技巧**：**对角线取反（Diagonal Complement）**，它利用了“鸽巢原理”和“对角线论证”来一次性构造出一个必不在集合中的元素。  
- **适用的题型**  
  1. “找一个不在给定集合中的二进制串”——本题。  
  2. “找一个不在给定集合中的排列/序列”——如 LeetCode 1961 “Check If String Is a Prefix of Array”。  
  3. “构造不冲突的标识符”——比如生成未使用的用户名、IP 地址等。  
- **一句话总结**：**把每行的第 i 位翻个面，得到的对角线串必然是全新的**。

---

## 反思

- **第一反应**：看到“长度为 n 的所有二进制串”，自然想到枚举全部 `2^n` 种可能，然后检查是否出现。  
- **最容易踩的坑**  
  1. **忘记把 `nums` 放进哈希集合**，导致每次线性查找导致 `O(n·2^n·n)`（更慢）。  
  2. **忽略 n=1 的极端情况**：对角线方法仍然有效，只会返回 `'1'`（如果输入是 `'0'`）或 `'0'`。  
  3. **误以为对角线取反只能产生一种答案**，其实只要任意一次取反即可，答案不唯一。  
- **下次遇到同类题**：第一步先思考 **“能不能不枚举，而直接构造一个必不相同的对象？”**，尤其留意是否可以利用索引位置的对应关系（对角线、位运算等）来实现。