# #2217. 固定长度回文数 / Find Palindrome With Fixed Length

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/find-palindrome-with-fixed-length/)

---

## 题目（英文原版）

**Description**

Given an integer array queries and a positive integer intLength, return an array answer where answer[i] is either the queries[i]th smallest positive palindrome of length intLength or -1 if no such palindrome exists.
A palindrome is a number that reads the same backwards and forwards. Palindromes cannot have leading zeros.

**Examples**

**Example 1:**

```
Input: queries = [1,2,3,4,5,90], intLength = 3
Output: [101,111,121,131,141,999]
Explanation:
The first few palindromes of length 3 are:
101, 111, 121, 131, 141, 151, 161, 171, 181, 191, 202, ...
The 90th palindrome of length 3 is 999.
```

**Example 2:**

```
Input: queries = [2,4,6], intLength = 4
Output: [1111,1331,1551]
Explanation:
The first six palindromes of length 4 are:
1001, 1111, 1221, 1331, 1441, and 1551.
```

**Constraints**

- 1 <= queries.length <= 5 * 104
- 1 <= queries[i] <= 109
- 1 <= intLength <= 15

---

## 题目（中文翻译）

给定一个整数数组（integer array）`queries` 和一个正整数（positive integer）`intLength`，返回一个数组 `answer`，其中 `answer[i]` 为第 `queries[i]` 小的 **长度为** `intLength` 的正回文数（palindrome），如果不存在这样的回文数则返回 `-1`。

**回文数（palindrome）** 是指正向和反向读都相同的数字。回文数不能有前导零（leading zeros）。

## 示例

### 示例 1
**输入**  
`queries = [1,2,3,4,5,90]`, `intLength = 3`

**输出**  
`[101,111,121,131,141,999]`

**解释**  
长度为 3 的前几个回文数为：  
101, 111, 121, 131, 141, 151, 161, 171, 181, 191, 202, …  
第 90 小的长度为 3 的回文数是 999。

### 示例 2
**输入**  
`queries = [2,4,6]`, `intLength = 4`

**输出**  
`[1111,1331,1551]`

**解释**  
长度为 4 的前六个回文数为：  
1001, 1111, 1221, 1331, 1441, 1551。

## 约束

- `1 <= queries.length <= 5 * 10^4`
- `1 <= queries[i] <= 10^9`
- `1 <= intLength <= 15`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有满足长度 `intLength` 的正整数都枚举出来，检查它们是不是回文数**，把符合条件的按从小到大的顺序存进一个数组，然后直接用下标取第 `queries[i]`‑个。  

- **用到的数据结构**：  
  - **列表（list）**：像装东西的箱子，依次把找到的回文数放进去，后面要取第 k 个时，只要取列表的第 k‑1 个元素就行。  
  - **字符串**：把整数转成字符串，利用“正读和反读相同”这个特性来判断是否是回文。把数字想成一本书的文字，正读相当于从左往右读，反读相当于从右往左读，两个读法相同说明这本书是回文的。  

- **为什么正确**：  
  我们把**所有**满足长度要求的数都检查了一遍，凡是回文的都会被加入列表，列表自然就是“从小到大第 1、2、3 … 个回文数”。因此直接取第 k 个就一定是第 k 小的回文数。  

- **时间/空间复杂度**（大白话解释）：  
  - 假设我们需要查到第 `maxK = max(queries)` 个回文数。  
  - 为了得到 `maxK` 个回文数，我们可能要遍历 **大约 `maxK` 个整数**（实际可能会多一点，因为不是每个整数都是回文）。每检查一个整数，就要把它转成字符串、把字符串倒着写一遍再比较，这个过程的耗时和数字的位数（`intLength`）成正比。  
  - 所以时间复杂度大约是 **O(maxK × intLength)**，如果 `maxK` 很大（比如上限 10⁹），这根本不可接受。  
  - 我们把找到的回文数全部存进列表，需要 **O(maxK)** 的额外空间。  

#### 代码（Python）  

```python
def kth_palindrome_bruteforce(queries, intLength):
    """
    暴力解：遍历所有整数，挑出长度为 intLength 的回文数
    返回一个答案列表，答案[i] 为第 queries[i] 小的回文数，若不存在则为 -1
    """
    # 先算出需要的最大序号，避免遍历太多不必要的数字
    max_k = max(queries)
    ans = [-1] * len(queries)          # 预先准备答案列表
    palins = []                         # 用来保存找到的回文数

    # 生成最小的 intLength 位正整数（不能有前导零）
    start = 10 ** (intLength - 1)
    # 结束时直接到 10**intLength - 1（所有 intLength 位数的上界）
    end = 10 ** intLength

    for num in range(start, end):
        s = str(num)                    # 把整数变成字符串，方便回文检测
        if s == s[::-1]:                # 字符串正读和反读相同 → 回文
            palins.append(num)
            if len(palins) >= max_k:    # 已经找够最大的查询序号，可以提前结束
                break

    # 把找到的回文数映射回每个查询
    for idx, q in enumerate(queries):
        if 1 <= q <= len(palins):       # q 在合法范围内
            ans[idx] = palins[q - 1]    # 第 q 小对应列表下标 q-1
        else:
            ans[idx] = -1               # 超出范围，返回 -1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(maxK × intLength)`  
  - 解释：如果要找第 `maxK` 小的回文，需要检查大约 `maxK` 个整数，每次检查的工作量与位数 `intLength` 成正比。  
- **空间复杂度**：`O(maxK)`  
  - 解释：我们把找到的回文数全部保存到了列表里，列表的长度最多是 `maxK`。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“逐个枚举、逐个检查”**，这一步用了 `O(maxK)` 的时间。其实我们可以直接**算出第 k 小回文长啥样**，不必遍历。关键在于回文数的构造规律：

1. **回文数的左半边决定全部**  
   - 设长度为 `L`，把它分成左半边和右半边。  
   - 例如 `L = 5` → `abcba`，左半边是 `abc`（包含中间的那个 `c`），右半边是 `ba`，完全是左半边的镜像。  
   - 如果 `L = 6` → `abccba`，左半边是 `abc`（不含中间），右半边是 `cba`。  

2. **左半边的取值范围**  
   - 左半边的位数是 `half = ceil(L / 2)`（向上取整），记作 `half_len`。  
   - 左半边的第一位 **不能是 0**（否则整体会出现前导零），所以最小的左半边是 `10^{half_len-1}`，最大的左半边是 `10^{half_len} - 1`。  
   - 因此 **长度为 `L` 的回文数一共有**  

     \[
     \text{cnt} = 9 \times 10^{\;half\_len-1}
     \]

     种（因为第一位有 9 种（1‑9），其余 `half_len-1` 位各有 10 种）。  

3. **从序号直接得到左半边**  
   - 第 `k` 小的回文对应的左半边是：  

     \[
     \text{firstHalf} = 10^{\;half\_len-1} + (k-1)
     \]

     （把最小的左半边往后数 `k-1` 步）。  

4. **把左半边翻转拼接得到完整回文**  
   - 把 `firstHalf` 转成字符串 `s`。  
   - 若 `L` 为奇数，去掉 `s` 最后一个字符再反转（因为中间那位不需要重复），拼接得到回文。  
   - 若 `L` 为偶数，直接把 `s` 完全反转拼接。  

5. **不存在的情况**  
   - 如果 `k > cnt`，说明该长度根本没有第 `k` 小的回文，直接返回 `-1`。  

**总结**：对每个查询，只需要 **常数时间**（几次算幂、几次字符串拼接）就能得到答案，整个算法是 **O(|queries|)** 的线性时间，空间只用常数级别的额外变量。  

#### 代码（Python）  

```python
def kth_palindrome_optimal(queries, intLength):
    """
    最优解：利用回文数的构造规律，直接计算第 k 小的回文
    """
    half_len = (intLength + 1) // 2          # 左半边的位数，向上取整
    start = 10 ** (half_len - 1)             # 左半边最小值（第一位不能为 0）
    total = 9 * start                        # 该长度所有回文的数量

    ans = []
    for k in queries:
        if k > total:                        # 超出范围 → -1
            ans.append(-1)
            continue

        # 第 k 小对应的左半边
        first_half = start + (k - 1)
        s = str(first_half)

        # 根据长度奇偶决定拼接方式
        if intLength % 2 == 0:               # 偶数长度：全翻转
            pal = s + s[::-1]
        else:                                # 奇数长度：去掉中间字符再翻转
            pal = s + s[-2::-1]              # s[-2::-1] = 从倒数第二个字符开始逆序

        ans.append(int(pal))                 # 转回整数加入答案
    return ans
```

**代码要点注释**  

- `half_len = (intLength + 1) // 2`：整数除法实现向上取整。比如 `5 → 3`，`4 → 2`。  
- `start = 10 ** (half_len - 1)`：左半边最小可能是 `100…0`（第一位 1，后面全 0），保证没有前导零。  
- `total = 9 * start`：因为左半边第一位有 9 种（1‑9），其余位各有 10 种，等价于 `9 × 10^{half_len-1}`。  
- `first_half = start + (k - 1)`：把最小左半边往后数 `k-1` 步得到第 `k` 小。  
- `s + s[::-1]` / `s + s[-2::-1]`：把左半边拼上它的镜像，奇数长度时把中间那位（`s[-1]`）去掉再翻转。  

#### 复杂度  

- **时间复杂度**：`O(|queries|)`  
  - 解释：对每个查询只做了常数次算数运算和一次长度至多 15（题目上限）的字符串拼接，和查询的数量呈线性关系。相比暴力的 `O(maxK)`，快了好几数量级。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 解释：除了保存答案的列表外，只用了几个整数和临时字符串，大小不随输入规模增长。  

---

## 心得  

- **核心技巧**：**利用回文数左半边唯一决定整体的特性**，把“第 k 小”转化为对左半边的直接计数。  
- **该技巧适用的题型**（类似思路）  
  1. **构造指定长度的回文数**（如本题）。  
  2. **生成回文数序列或求第 N 大回文数**（如 “Find the K-th Smallest Palindrome” 系列）。  
  3. **数字翻转类题目**（如 “Reverse Integer”）中，需要把数字的前半段/后半段分别处理。  
- **一句话总结解题钥匙**：  
  > “回文数的左半边是唯一自由变量，先算出左半边的起始值，再加上序号偏移，即可直接得到第 k 小回文。”  

---

## 反思  

- **拿到题目第一反应**：先想“枚举所有数字，然后判断回文”，这是一种最直观的暴力思路。  
- **最容易踩的坑**  
  - **前导零**：左半边的第一位不能为 0，必须从 `10^{half_len-1}` 开始计数。  
  - **奇偶长度的区别**：奇数长度时中间的数字不应重复，否则会多出一位。  
  - **查询超界**：`k` 可能大于该长度所有回文的数量，需要提前返回 `-1`，否则会产生错误的拼接结果。  
- **下次遇到同类题，第一步该想到**：  
  - “这个结构（回文、对称、镜像）是否可以用**一半的信息**完整描述？”  
  - 若答案是“可以”，就尝试 **把‘第 k 小’转化为‘左半边的第 k 小’**，再直接构造答案。