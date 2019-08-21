# #541. 反转字符串 II / Reverse String II

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/reverse-string-ii/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, reverse the first k characters for every 2k characters counting from the start of the string.
If there are fewer than k characters left, reverse all of them. If there are less than 2k but greater than or equal to k characters, then reverse the first k characters and leave the other as original.

**Examples**

**Example 1:**

```
Input: s = "abcdefg", k = 2
Output: "bacdfeg"
```

**Example 2:**

```
Input: s = "abcd", k = 2
Output: "bacd"
```

**Constraints**

- 1 <= s.length <= 104
- s consists of only lowercase English letters.
- 1 <= k <= 104

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，从字符串的起始位置开始，每 `2k` 个字符为一组，**反转**（reverse）该组中的前 `k` 个字符。  

- 如果剩余字符少于 `k`，则将剩余的所有字符全部反转。  
- 如果剩余字符不少于 `k` 但少于 `2k`，则仅反转前 `k` 个字符，后面的字符保持原样。  

**示例 1**  
输入: `s = "abcdefg", k = 2`  
输出: `"bacdfeg"`  

**示例 2**  
输入: `s = "abcd", k = 2`  
输出: `"bacd"`  

**约束条件**  

- `1 <= s.length <= 10^4`  
- `s` 仅由小写英文字母组成。  
- `1 <= k <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一次遍历** 把字符串按照「每 2k 个字符」划分成若干块，然后对每块的前 k 个字符做一次**整体翻转**，其余字符保持不变。

- **数据结构**：把 Python 的不可变字符串 `s` 先转成 **列表**（list），因为列表可以原地修改字符，类似于把一串珠子装进可打开的盒子里，想改哪个珠子就直接换。
- **翻转**：把列表的某段 `[l, r]` 用切片 `[::-1]` 或者双指针 `while l < r: swap` 来倒序，像把一段文字倒着读。
- **为什么正确**：题目只要求在每个「2k」的区间里把前 k 个字符逆序，而我们恰好按照这个规则对每个区间执行了相同的操作，所以结果必然满足要求。

#### 代码（Python）

```python
def reverseStr_brute(s: str, k: int) -> str:
    # 把字符串转成列表，列表是可变的，后面可以直接改字符
    chars = list(s)

    n = len(chars)
    # i 表示每个「2k」区间的起始位置
    i = 0
    while i < n:
        # 计算本区间需要翻转的左、右端点（左闭右闭）
        left = i
        right = min(i + k - 1, n - 1)   # 不能越界

        # 双指针翻转 left~right 区间
        while left < right:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1

        # 跳到下一个 2k 区间的起点
        i += 2 * k

    # 列表再拼回字符串返回
    return ''.join(chars)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  我们遍历整个字符串一次，每个字符最多被交换一次。`O(n)` 可以理解为“随着字符串长度 n 增大，运行时间大约线性增长”，比如长度是 10 时需要 10 步，长度是 100 时需要 100 步。
- **空间复杂度**：`O(n)`  
  额外用了一个字符列表来存放 `s`，这相当于再开了一份和原字符串等长的副本。  

---

### 2. 最优解

#### 思路  

从暴力解来看，已经是 **线性时间** 的了，唯一可以改进的地方是 **空间**：如果不想额外再占用 `O(n)` 的列表空间，可以直接在 **字符串切片** 上操作，然后一次性拼接结果。  
Python 的字符串切片会创建新的子串，但因为每段子串的长度总和仍然是 `n`，整体空间仍是 `O(n)`（这已经是不可避免的，因为返回值本身就是一个新字符串）。  
因此这里把「最优」定义为 **代码更简洁、常数因子更小**，使用切片一次性完成翻转，而不需要手写双指针。

核心步骤：

1. **按 2k 为步长遍历** 整个字符串，记录每段的起始下标 `i`。  
2. 对每段，**取前 k 个字符**（如果不足 k，就取全部），用 `[::-1]` 直接得到逆序字符串。  
3. 把这段逆序的子串 + **剩余未逆序的子串** 合在一起，累加到答案中。  

> **类比**：想象一条长绳子被每 2k 米打一个结，你只需要把每个结前面的 k 米绳子翻过去，后面的保持原样。用切片就相当于把绳子剪成小段，然后把需要翻的那段倒着拼回去。

#### 代码（Python）

```python
def reverseStr_optimal(s: str, k: int) -> str:
    n = len(s)
    res = []                     # 用列表收集每段处理后的子串，最后一次 join

    i = 0
    while i < n:
        # ① 需要逆序的子串：从 i 开始，长度最多 k（可能不足 k）
        part_to_reverse = s[i : i + k][::-1]   # 切片 + 逆序
        # ② 其余保持不变的子串：从 i+k 开始，最多再取 k 个字符
        part_remain = s[i + k : i + 2 * k]

        # 把两部分拼接后加入结果列表
        res.append(part_to_reverse + part_remain)

        # 跳到下一个 2k 区间
        i += 2 * k

    # 最后把所有块拼成完整字符串返回
    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个字符恰好被切片或拼接一次，整体仍是线性增长。相比双指针的写法，这里省去了每次交换的循环，常数因子更小。
- **空间复杂度**：`O(n)`  
  需要存放返回的完整字符串（不可避免），以及临时的列表 `res`，其总长度也是 `n`。

---

## 心得

- **核心技巧**：**按固定步长分块 + 局部逆序**（Two‑Pointer/切片）  
- **适用的题型**  
  1. “每 k 个字符翻转一次”类题目（如 *Reverse String II*、*Reverse Only Letters*）  
  2. “区间内做特定操作”类题目（如 *Rotate Array*, *Shuffle String*）  
- **一句话总结解题钥匙**：**把大问题拆成若干个相同大小的小区间，只在需要的区间里做逆序，其他保持原样**。

---

## 反思

- **第一反应**：看到“每 2k 个字符”就想到“循环跳步”，于是直接用 `while i < n: i += 2*k` 来遍历区间。  
- **最容易踩的坑**  
  - **边界条件**：最后剩余的字符可能不足 k，也可能在 k~2k 之间，需要分别处理。  
  - **下标越界**：切片时必须使用 `min` 或 Python 的自然截断特性，防止 `i+k` 超出字符串长度。  
- **下次类似题目第一步**：先**画出字符串的分块示意图**，明确每块需要的操作（翻转、保持），再决定是用**双指针**还是**切片**实现。