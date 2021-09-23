# #1486. **数组中的 XOR 操作** / XOR Operation in an Array

> 难度：简单 · 标签：Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/xor-operation-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an integer start.
Define an array nums where nums[i] = start + 2 * i (0-indexed) and n == nums.length.
Return the bitwise XOR of all elements of nums.

**Examples**

**Example 1:**

```
Input: n = 5, start = 0
Output: 8
Explanation: Array nums is equal to [0, 2, 4, 6, 8] where (0 ^ 2 ^ 4 ^ 6 ^ 8) = 8.
Where "^" corresponds to bitwise XOR operator.
```

**Example 2:**

```
Input: n = 4, start = 3
Output: 8
Explanation: Array nums is equal to [3, 5, 7, 9] where (3 ^ 5 ^ 7 ^ 9) = 8.
```

**Constraints**

- 1 <= n <= 1000
- 0 <= start <= 1000
- n == nums.length

---

## 题目（中文翻译）

给定整数 `n` 和整数 `start`。  
定义一个数组 `nums`，其中 `nums[i] = start + 2 * i`（下标从 0 开始），且 `n == nums.length`。  
返回数组 `nums` 中所有元素的位运算 XOR（bitwise XOR）的结果。

**示例 1**  
**输入**: `n = 5, start = 0`  
**输出**: `8`  
**解释**: 数组 `nums` 为 `[0, 2, 4, 6, 8]`，其中 `(0 ^ 2 ^ 4 ^ 6 ^ 8) = 8`。  
这里的 "`^`" 表示位运算 XOR（bitwise XOR）运算符。

**示例 2**  
**输入**: `n = 4, start = 3`  
**输出**: `8`  
**解释**: 数组 `nums` 为 `[3, 5, 7, 9]`，其中 `(3 ^ 5 ^ 7 ^ 9) = 8`。

**约束条件**  
- `1 <= n <= 1000`  
- `0 <= start <= 1000`  
- `n == nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把数组直接算出来**，再把所有元素逐个做异或（XOR）运算。

- **数据结构**：只需要一个普通的 Python `list`，把 `nums[i] = start + 2*i` 按照公式填进去。  
  - 这里的 “list” 就像我们平时用的**购物清单**，把每件商品（数组元素）一个个写进去，后面再逐个处理。
- **为什么正确**：题目已经明确说“返回 `nums` 中所有元素的异或”。我们把 `nums` 完整地构造出来后，依次把每个数用 `^`（位异或）连接，最终得到的结果必然就是题目要求的答案。
- **复杂度分析**：  
  - **时间**：我们要遍历 `n` 次来生成数组，又要遍历 `n` 次来做异或，整体是 `O(n)`，在这里可以直接写成 `O(n)`，意思是**时间随 `n` 成线性增长**。比如 `n=1000` 时需要大约 1000 步。  
  - **空间**：我们额外创建了一个长度为 `n` 的数组，空间占用是 `O(n)`，即**需要和元素个数一样多的额外记忆**。

#### 代码（Python）

```python
def xorOperation_bruteforce(n: int, start: int) -> int:
    # 1. 生成数组 nums
    nums = [start + 2 * i for i in range(n)]   # 像写购物清单一样把每个元素放进列表

    # 2. 对所有元素做异或
    ans = 0                                     # 异或的“中性元”是 0，0 ^ x = x
    for num in nums:
        ans ^= num                               # ^ 是位异或运算符
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着 `n` 的增大，运行时间线性增长。
- **空间复杂度**：`O(n)` — 需要存储 `n` 个整数的额外列表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**显式地把整个数组保存下来**，其实我们并不需要真的把数组列出来，只要知道每个元素的规律，就可以直接算出最终的异或结果。

1. **观察规律**  
   - `nums[i] = start + 2*i`，也就是说每个数都是 `start` 再加上一个偶数（`2*i`）。  
   - 偶数乘以 2 相当于把二进制左移一位（`x << 1`），所以  
     ```
     start + 2*i = (start//2 + i) << 1   （当 start 为偶数时）
     ```
   - 当 `start` 为奇数时，`start = 2*k + 1`，于是  
     ```
     start + 2*i = (k + i) << 1  + 1   （每个数都是“左移后再加 1”）
     ```

2. **把问题转化为 “连续整数的异或”**  
   - 对于一段连续整数 `a, a+1, …, b`，它们的异或可以用 **前缀异或** 快速算出：  
     ```
     xor_range(a, b) = prefix(b) ^ prefix(a-1)
     ```
     其中 `prefix(x)` 表示 `0 ^ 1 ^ 2 ^ … ^ x`。  
     `prefix(x)` 有非常简洁的周期性（每 4 个数循环一次）：
     ```
     x % 4 == 0 → prefix = x
     x % 4 == 1 → prefix = 1
     x % 4 == 2 → prefix = x + 1
     x % 4 == 3 → prefix = 0
     ```
   - 这一步相当于**把一大串数压缩成四种可能的结果**，所以时间从 `O(n)` 降到 `O(1)`。

3. **根据 start 的奇偶性分别处理**  
   - **start 为偶数**  
     ```
     let s = start // 2
     ans = (xor_range(s, s + n - 1)) << 1
     ```
     把 `s … s+n-1` 的异或算出来后左移一位（乘 2），得到最终答案。
   - **start 为奇数**  
     ```
     let s = start // 2          # 这里的除法自动向下取整，等价于 (start-1)//2
     ans = (xor_range(s, s + n - 1)) << 1
     if n % 2 == 1:               # 1 出现了 n 次，奇数次会留下一个 1
         ans ^= 1
     ```
     多出来的 `+1`（因为每个数都是奇数）会在异或时相互抵消，只有当出现奇数次时才会留下一个 `1`。

4. **核心算法**：  
   - **前缀异或的四周期性质**（只需要几行 `if` 判断）。  
   - **位运算**：左移 `<< 1` 相当于把所有数乘以 2，异或运算 `^` 按位比较不同。

#### 代码（Python）

```python
def xorOperation(n: int, start: int) -> int:
    """
    O(1) 时间、O(1) 空间求解。
    思路：把原数组转化为「连续整数的异或」+ 可能的额外 1。
    """

    # ---------- 辅助函数：前缀异或 ----------
    def prefix_xor(x: int) -> int:
        """返回 0 ^ 1 ^ 2 ^ ... ^ x 的结果，利用 4 周期性质"""
        r = x % 4
        if r == 0:   # 0,4,8,...
            return x
        if r == 1:   # 1,5,9,...
            return 1
        if r == 2:   # 2,6,10,...
            return x + 1
        # r == 3
        return 0

    # ---------- 计算连续区间的异或 ----------
    def xor_range(l: int, r: int) -> int:
        """返回 l ^ (l+1) ^ ... ^ r 的结果"""
        return prefix_xor(r) ^ prefix_xor(l - 1)

    # ---------- 根据 start 的奇偶性分别处理 ----------
    base = start // 2                     # 取整除 2，相当于把偶数部分去掉
    cur = xor_range(base, base + n - 1)   # 连续整数的异或
    ans = cur << 1                        # 左移一位 = 乘以 2

    # 如果 start 本身是奇数，每个数都多了一个 1
    if start % 2 == 1 and n % 2 == 1:     # 1 出现奇数次才会留下
        ans ^= 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只用了常数次算术和位运算，不会随 `n` 增大而变慢。相比暴力的 `O(n)`，快了好几个数量级。  
- **空间复杂度**：`O(1)` — 只用了若干个整数变量，额外空间恒定不变。

---

## 心得

- **核心技巧**：**前缀异或的 4 周期规律** + **把「等差数列」转化为「连续整数」** 再利用位运算。  
- **适用的题型**：  
  1. “XOR of All Numbers from 1 to n” 这类求连续区间异或的题目。  
  2. “XOR of an Arithmetic Sequence” （等差数列的异或）  
  3. “Find Missing Number” 中利用异或抵消的思想。  
- **一句话总结**：把数组的生成规则拆解成“左移 + 可能的 1”，再用前缀异或一次算出答案。

---

## 反思

- **第一反应**：直接把数组列出来，循环异或——最自然的暴力实现。  
- **最容易踩的坑**：  
  - 忘记 `start` 为奇数时，每个数都多了一个 `1`，导致结果偏差。  
  - 前缀异或的四周期写错，导致 `xor_range` 计算错误。  
  - 边界情况：`n = 1` 时，只有一个元素，需要确保 `xor_range` 能正确处理 `l == r`。  
- **下次类似题的第一步**：**先观察数列的生成规律，尝试把它映射到已知的“连续整数异或”或“前缀异或”模型**，再决定是否需要使用位移、奇偶性等技巧。