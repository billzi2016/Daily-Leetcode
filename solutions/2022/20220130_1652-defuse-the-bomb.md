# #1652. **拆弹** / Defuse the Bomb

> 难度：简单 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/defuse-the-bomb/)

---

## 题目（英文原版）

**Description**

You have a bomb to defuse, and your time is running out! Your informer will provide you with a circular array code of length of n and a key k.
To decrypt the code, you must replace every number. All the numbers are replaced simultaneously.
As code is circular, the next element of code[n-1] is code[0], and the previous element of code[0] is code[n-1].
Given the circular array code and an integer key k, return the decrypted code to defuse the bomb!

**Examples**

**Example 1:**

```
Input: code = [5,7,1,4], k = 3
Output: [12,10,16,13]
Explanation: Each number is replaced by the sum of the next 3 numbers. The decrypted code is [7+1+4, 1+4+5, 4+5+7, 5+7+1]. Notice that the numbers wrap around.
```

**Example 2:**

```
Input: code = [1,2,3,4], k = 0
Output: [0,0,0,0]
Explanation: When k is zero, the numbers are replaced by 0.
```

**Example 3:**

```
Input: code = [2,4,9,3], k = -2
Output: [12,5,6,13]
Explanation: The decrypted code is [3+9, 2+3, 4+2, 9+4]. Notice that the numbers wrap around again. If k is negative, the sum is of the previous numbers.
```

**Constraints**

- n == code.length
- 1 <= n <= 100
- 1 <= code[i] <= 100
- -(n - 1) <= k <= n - 1

---

## 题目（中文翻译）

你有一个需要拆除的炸弹，时间紧迫！情报员会提供给你一个长度为 `n` 的循环数组 `code` 和一个密钥 `k`。  
要解密该数组，你必须同时替换每一个数字。  

由于数组是循环的，`code[n‑1]` 的下一个元素是 `code[0]`，而 `code[0]` 的前一个元素是 `code[n‑1]`。  
给定循环数组 `code` 与整数 `k`，返回解密后的数组，以便成功拆弹！

---

### 示例

**示例 1**  
```text
Input:  code = [5,7,1,4], k = 3
Output: [12,10,16,13]
```
**解释**：每个数字都被其后面 `k = 3` 个数字的和所替代。解密后的数组为  
`[7+1+4, 1+4+5, 4+5+7, 5+7+1]`。注意数组会循环回到开头。

**示例 2**  
```text
Input:  code = [1,2,3,4], k = 0
Output: [0,0,0,0]
```
**解释**：当 `k` 为 `0` 时，所有数字都被 `0` 替代。

**示例 3**  
```text
Input:  code = [2,4,9,3], k = -2
Output: [12,5,6,13]
```
**解释**：解密后的数组为  
`[3+9, 2+3, 4+2, 9+4]`。同样会循环回到数组首部。当 `k` 为负数时，取的是前面 `|k|` 个数字的和。

---

### 约束条件

- `n == code.length`
- `1 <= n <= 100`
- `1 <= code[i] <= 100`
- `-(n - 1) <= k <= n - 1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**逐个元素**地去算它需要被替换成的和。  

- **数据结构**：我们只需要一个普通的 Python 列表 `code`，它本身就像一本 **顺序的字典**，下标（index）相当于词条，值相当于对应的解释。  
- **循环方式**：因为数组是 **环形** 的，最后一个元素的“下一个”是第一个元素，第一位的“上一个”是最后一个元素。这可以用 **取模运算**（`% n`）来实现——就像在圆形跑道上走，走到终点再回到起点。  
- **求和规则**：  
  - 当 `k > 0` 时，每个位置要把 **后面的 `k` 个数**（顺时针）相加。  
  - 当 `k < 0` 时，每个位置要把 **前面的 `|k|` 个数**（逆时针）相加。  
  - 当 `k == 0` 时，所有位置都替换成 `0`。  

只要对每个下标 `i`，循环 `|k|` 次取出对应的元素相加，就能得到答案。  

**为什么正确**：  
因为题目明确规定“每个数字同时被它左/右（取决于 k 的符号）`|k|` 个数字的和替换”。暴力循环正好按照这个规定去取数并相加，必然得到正确结果。  

**时间/空间复杂度**：  
- 外层遍历 `n` 次（数组长度），内层最多遍历 `|k|` 次（`k` 的绝对值），所以时间复杂度是 **O(n·|k|)**。在最坏情况下 `|k|` 可能接近 `n`，于是最坏时间是 **O(n²)**。  
- 只用了一个长度为 `n` 的结果数组，空间复杂度是 **O(n)**（不计输入本身）。  

> **大白话**：  
> - `O(n²)` 并不是说真的会出现 “n 的平方次方” 的数字，而是说如果 `n` 是 100，最坏会进行 10,000 次简单的加法——在电脑里这仍然很快，但如果 `n` 是 10⁵，就会慢到不行。  

#### 代码（Python）  

```python
from typing import List

def decrypt(code: List[int], k: int) -> List[int]:
    n = len(code)                 # 数组长度
    if k == 0:                    # k 为 0 时全部置 0，直接返回
        return [0] * n

    res = [0] * n                 # 用来存放答案
    step = abs(k)                 # 需要取多少个相邻元素

    for i in range(n):           # 对每个位置 i
        total = 0
        for j in range(1, step + 1):
            # 根据 k 的符号决定往左还是往右取元素
            if k > 0:            # 向右（顺时针）取
                idx = (i + j) % n
            else:                # 向左（逆时针）取
                idx = (i - j) % n
            total += code[idx]   # 累加
        res[i] = total            # 写入结果
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n·|k|)`  
  - 如果 `k` 接近 `n`，相当于 `O(n²)`，意思是每个位置都要遍历几乎整个数组。  
- **空间复杂度**：`O(n)`  
  - 只用了一个和输入等长的列表来存放答案。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每个位置都重新遍历 `|k|` 次**，导致大量重复计算。  
比如 `k = 3` 时，位置 0 需要 `code[1] + code[2] + code[3]`，位置 1 需要 `code[2] + code[3] + code[4]`（下标环绕）。可以看到 **相邻两个窗口的和只差一个进、一个出**，这正是**滑动窗口**（Sliding Window）技巧的典型场景。  

**滑动窗口的核心**：  
- 维护一个“窗口”里当前的元素和。  
- 当窗口向右平移一步时，只需要 **减去离开的元素**，**加上新进来的元素**，即可得到新的窗口和，**O(1)** 时间完成更新。  

因为数组是环形的，我们可以把原数组 **复制一遍**（即拼接 `code + code`），这样在不使用取模的情况下也能直接取到跨界的元素。  

实现步骤如下（以 `k > 0` 为例，`k < 0` 类似，只是窗口向左移动）：  

1. **特判** `k == 0` → 全部返回 `0`。  
2. 复制数组：`extended = code + code`，长度变成 `2n`。  
3. 初始化窗口和为前 `k` 个元素的和（对应下标 0 的答案）。  
4. 从 `i = 0` 到 `n-1`：  
   - `res[i] = window_sum`（当前窗口和即为位置 i 的答案）。  
   - 滑动窗口：`window_sum += extended[i + k + 1] - extended[i + 1]`（把窗口右边再往右移一位，左边去掉一个元素）。  
5. 如果 `k < 0`，只需把上述过程的方向反过来：把窗口放在左侧，或者等价地把 `code` 逆序后再用同样的右滑窗口。这里我们直接在 **负方向** 上滑动，同样使用取模即可。  

**复杂度分析**：  
- 只遍历了数组一次（`O(n)`），每次窗口更新是常数时间。  
- 额外空间只用了一个长度为 `n` 的答案数组和一个长度为 `2n` 的临时复制（复制可以看作 O(n)），总体 **O(n)**。  

#### 代码（Python）  

```python
from typing import List

def decrypt(code: List[int], k: int) -> List[int]:
    n = len(code)
    if k == 0:                     # k 为 0，直接返回全 0
        return [0] * n

    # 为了避免取模带来的额外判断，先把数组拼接一次，形成环形的“直线”
    extended = code + code         # 长度 2n

    res = [0] * n

    if k > 0:                      # 向右（顺时针）取 k 个数
        # 初始窗口：code[1] .. code[k]
        window_sum = sum(extended[1:k+1])
        for i in range(n):
            res[i] = window_sum                # 当前窗口和即答案
            # 窗口整体右移一位：
            #   - 移出 extended[i+1]（窗口左端）
            #   - 移入 extended[i+k+1]（窗口右端）
            window_sum += extended[i + k + 1] - extended[i + 1]
    else:                          # k < 0，向左（逆时针）取 |k| 个数
        step = -k                   # 取绝对值
        # 初始窗口：code[n-step] .. code[n-1]（即左侧 step 个数）
        window_sum = sum(extended[n-step:n])
        for i in range(n):
            res[i] = window_sum
            # 窗口整体左移一位（等价于右移 n-1 步），这里直接用取模计算：
            #   - 移出 extended[i + n]（窗口右端）
            #   - 移入 extended[i + n - step]（窗口左端）
            window_sum += extended[i + n - step] - extended[i + n]
    return res
```

> **代码说明**  
> - `extended[i + k + 1]` 与 `extended[i + 1]` 只在 `i` 在 `[0, n-1]` 范围内使用，索引始终合法。  
> - 当 `k < 0` 时，我们把窗口放在左侧，用同样的 **滑动** 思路，只是进出元素的方向相反。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，窗口更新是常数时间。相比暴力的 `O(n·|k|)`，速度提升了数倍，尤其在 `|k|` 接近 `n` 时差别明显。  
- **空间复杂度**：`O(n)`  
  - 额外使用了一个长度为 `2n` 的 `extended` 列表（仍然是线性空间），以及结果列表 `res`。  

---  

## 心得  

- **核心技巧**：**滑动窗口**（Sliding Window）——在求“固定长度子数组的和”时，利用“进一减一”实现 O(1) 更新。  
- **适用的题型**（类似思路）：  
  1. LeetCode 209. Minimum Size Subarray Sum（最小长度子数组和）  
  2. LeetCode 239. Sliding Window Maximum（滑动窗口最大值）  
  3. LeetCode 3. Longest Substring Without Repeating Characters（最长无重复子串）  
- **一句话总结**：**把每一次重复的遍历“合并”进窗口的移动，只保留一次遍历**，就是解锁 O(n) 的钥匙。  

## 反思  

- **第一反应**：看到“每个元素都要被相邻 `k` 个数的和替换”，立刻想到 **遍历每个位置、再遍历 `|k|` 次** 的直接实现。  
- **最容易踩的坑**：  
  - **环形索引**：忘记使用取模或数组复制会导致 IndexError。  
  - **k 的符号**：正负方向不同，需要分别处理，否则会把前面的数算成后面的数。  
  - **k = 0** 的特殊情况：直接返回全 0，防止窗口大小为 0 时出现除零或空窗口错误。  
- **下次遇到同类题**：第一步先判断是否可以把“每次都重新求和”转化为“窗口移动”——只要是 **固定长度的子数组求和**（或固定窗口的其他统计量），就尝试滑动窗口。