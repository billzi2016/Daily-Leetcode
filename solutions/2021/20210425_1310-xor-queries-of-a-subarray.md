# #1310. 子数组的 XOR 查询 / XOR Queries of a Subarray

> 难度：中等 · 标签：Array、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/xor-queries-of-a-subarray/)

---

## 题目（英文原版）

**Description**

You are given an array arr of positive integers. You are also given the array queries where queries[i] = [lefti, righti].
For each query i compute the XOR of elements from lefti to righti (that is, arr[lefti] XOR arr[lefti + 1] XOR ... XOR arr[righti] ).
Return an array answer where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]
Output: [2,7,14,8] 
Explanation: 
The binary representation of the elements in the array are:
1 = 0001 
3 = 0011 
4 = 0100 
8 = 1000 
The XOR values for queries are:
[0,1] = 1 xor 3 = 2 
[1,2] = 3 xor 4 = 7 
[0,3] = 1 xor 3 xor 4 xor 8 = 14 
[3,3] = 8
```

**Example 2:**

```
Input: arr = [4,8,2,10], queries = [[2,3],[1,3],[0,0],[0,3]]
Output: [8,0,4,4]
```

**Constraints**

- 1 <= arr.length, queries.length <= 3 * 104
- 1 <= arr[i] <= 109
- queries[i].length == 2
- 0 <= lefti <= righti < arr.length

---

## 题目（中文翻译）

给定一个正整数数组 `arr`。同时给定查询数组 `queries`，其中 `queries[i] = [left_i, right_i]`。  
对于每个查询 `i`，计算下标从 `left_i` 到 `right_i` 的元素的异或（XOR），即  

`arr[left_i] XOR arr[left_i + 1] XOR … XOR arr[right_i]`  

返回数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的结果。

---

### 示例 1
**输入**  
```text
arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]
```
**输出**  
```text
[2,7,14,8]
```
**解释**  
数组中元素的二进制表示为：  
```
1 = 0001
3 = 0011
4 = 0100
8 = 1000
```
各查询的 XOR 值为：  
- `[0,1]` : `1 XOR 3 = 2`  
- `[1,2]` : `3 XOR 4 = 7`  
- `[0,3]` : `1 XOR 3 XOR 4 XOR 8 = 14`  
- `[3,3]` : `8`

---

### 示例 2
**输入**  
```text
arr = [4,8,2,10], queries = [[2,3],[1,3],[0,0],[0,3]]
```
**输出**  
```text
[8,0,4,4]
```

---

### 约束条件
- `1 <= arr.length, queries.length <= 3 * 10^4`
- `1 <= arr[i] <= 10^9`
- `queries[i].length == 2`
- `0 <= left_i <= right_i < arr.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个查询的区间元素一个一个取出来做异或**（XOR）。  
可以把数组想象成一本书，每个位置是一本小册子，查询 `[l, r]` 就是把第 `l` 本到第 `r` 本的内容全部放进计算器里依次“^”一下，得到答案。

- **使用的数据结构**：仅仅是原始的列表 `arr`，以及一个用于保存答案的列表 `ans`。  
  （这里没有额外的“哈希表”或“前缀和”之类的结构，全部靠遍历。）

- **为什么正确**：XOR 运算满足**结合律**和**交换律**，即不管我们先算哪两个数，最终的结果都是一样的。所以只要把区间内所有数依次异或，得到的就是查询的答案。

- **时间/空间复杂度**：  
  - 对每个查询，我们都要遍历一次区间 `[l, r]`，最坏情况下区间长度是 `n`（数组长度）。  
  - 如果有 `m` 条查询，整体时间就是 `O(m * n)`。  
  - 这里的 `O` 符号可以理解为“数量级”。比如 `n = 10⁴`，`m = 10⁴`，则最多要做 `10⁸` 次异或运算，跑起来会比较慢。  
  - 只用了原数组和答案数组，额外空间是 `O(1)`（不算返回的答案）。

#### 代码（Python）

```python
def xorQueries_bruteforce(arr, queries):
    """
    暴力解：对每个查询区间直接遍历求异或
    :param arr: List[int]，原始数组
    :param queries: List[List[int]]，每个子数组是 [left, right]
    :return: List[int]，每个查询的答案
    """
    ans = []                     # 用来存放每个查询的结果
    for left, right in queries: # 逐条处理查询
        cur = 0                  # 当前区间的异或值，0 与任何数异或都等于它本身
        for i in range(left, right + 1):
            cur ^= arr[i]        # ^= 是 “cur = cur ^ arr[i]”
        ans.append(cur)          # 把本次查询的结果放进答案列表
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - `m` 是查询数量，`n` 是数组长度。  
  - 直观来说，就是“每条查询都要走一遍数组”。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了常数个额外变量 `cur`、`ans`（答案数组本身必须返回）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于每条查询都要重复遍历区间**。如果我们能够**把区间的异或结果预先算好**，查询时只需要 O(1) 时间取值，就能大幅加速。

**关键技巧：前缀异或（Prefix XOR）**。  
前缀和是把数组从左到右累计求和，前缀异或则是把它们累计求 XOR。  
我们可以把前缀异或想象成一本“异或字典”，第 `i` 页记录的是 `arr[0] ^ arr[1] ^ ... ^ arr[i]` 的结果。

- 记 `pre[i]` 为前 `i`（含）个元素的异或，`pre[-1]` 定义为 `0`（空集合的异或为 0）。
- 那么区间 `[l, r]` 的异或可以用前缀异或快速得到：

```
arr[l] ^ arr[l+1] ^ ... ^ arr[r]
= pre[r] ^ pre[l-1]
```

**为什么成立？**  
把 `pre[r]` 展开：`arr[0] ^ arr[1] ^ ... ^ arr[l-1] ^ arr[l] ^ ... ^ arr[r]`。  
再把 `pre[l-1]`（`arr[0] ^ ... ^ arr[l-1]`）与它异或，公共部分（左侧的 `arr[0] ... arr[l-1]`）会出现两次，而 `x ^ x = 0`，于是它们全部消掉，只剩下 `[l, r]` 的部分。  
这正是 **XOR 的消消乐特性**：`x ^ x = 0`，`0 ^ y = y`。

**步骤**：

1. **预处理**：一次遍历算出 `pre` 数组，时间 `O(n)`，空间 `O(n)`（存 `pre`）。
2. **回答查询**：对每条 `[l, r]`，直接返回 `pre[r] ^ pre[l-1]`（如果 `l==0`，`pre[l-1]` 用 `0` 代替），时间 `O(1)`。

整体时间是 `O(n + m)`，空间 `O(n)`。

#### 代码（Python）

```python
def xorQueries_prefix(arr, queries):
    """
    前缀异或解法：预处理前缀异或数组，查询时 O(1) 时间取值
    :param arr: List[int]
    :param queries: List[List[int]]
    :return: List[int]
    """
    n = len(arr)
    # step1：构造前缀异或数组，pre[i] 表示 arr[0] ^ ... ^ arr[i]
    pre = [0] * n
    cur = 0                     # 当前累计的异或值
    for i in range(n):
        cur ^= arr[i]           # 把第 i 个元素加入异或
        pre[i] = cur            # 保存到前缀数组

    # step2：逐条查询，利用 pre[r] ^ pre[l-1]（l 为 0 时使用 0）
    ans = []
    for left, right in queries:
        if left == 0:
            ans.append(pre[right])                # 区间从头开始，直接取 pre[right]
        else:
            ans.append(pre[right] ^ pre[left-1])  # 前缀消消乐
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `n` 次遍历生成前缀异或，`m` 次查询每次都是常数时间。  
  - 与暴力解的 `O(m·n)` 相比，提升了几个数量级，尤其当 `n`、`m` 都接近上限 `3·10⁴` 时，差距非常明显。

- **空间复杂度**：`O(n)`  
  - 需要额外保存一个长度为 `n` 的前缀数组 `pre`。  
  - 如果一定要把空间降到 `O(1)`，可以把前缀值直接存在原数组里（破坏原数组），但对初学者来说保持原数组不变更易理解。

---

## 心得

- **核心技巧**：**前缀异或 + 消消乐性质**（`x ^ x = 0`）。  
- **适用的题型**（类似技巧）：
  1. 区间异或查询（本题）。
  2. 区间求和查询（使用前缀和）。
  3. 子数组异或为零的计数（利用前缀异或的出现次数）。
- **解题钥匙**：把“重复计算的部分”提前算好，用**一次预处理**换取**多次快速查询**。

---

## 反思

- **第一反应**：看到“区间 XOR”，立刻想到遍历区间求异或——这就是暴力思路。  
- **最容易踩的坑**：
  - 忘记 `pre[-1]`（即左边界为 0 时）应该是 `0`，导致下标越界或错误结果。  
  - 对于大数（`arr[i] ≤ 10⁹`）直接使用 Python 的 `int` 没问题，但在某些语言需要注意整数溢出。  
  - 忘记异或的**交换律**和**结合律**，以为顺序会影响结果，实际是无关的。
- **下次类似题目**：第一步先问自己“有没有可以一次性累计的前缀结构”，如果答案是“有”，就立刻构造前缀数组；如果没有，再考虑更高级的数据结构（线段树、树状数组）或暴力。