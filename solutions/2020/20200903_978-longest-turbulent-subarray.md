# #978. 最长湍流子数组 / Longest Turbulent Subarray

> 难度：中等 · 标签：Array、Dynamic Programming、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-turbulent-subarray/)

---

## 题目（英文原版）

**Description**

Given an integer array arr, return the length of a maximum size turbulent subarray of arr.
A subarray is turbulent if the comparison sign flips between each adjacent pair of elements in the subarray.
More formally, a subarray [arr[i], arr[i + 1], ..., arr[j]] of arr is said to be turbulent if and only if:

**Examples**

**Example 1:**

```
Input: arr = [9,4,2,10,7,8,8,1,9]
Output: 5
Explanation: arr[1] > arr[2] < arr[3] > arr[4] < arr[5]
```

**Example 2:**

```
Input: arr = [4,8,12,16]
Output: 2
```

**Example 3:**

```
Input: arr = [100]
Output: 1
```

**Constraints**

- 1 <= arr.length <= 4 * 104
- 0 <= arr[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `arr`，返回 `arr` 中最长湍流子数组（turbulent subarray）的长度。

如果子数组（subarray）中相邻元素之间的比较符号在每一对相邻元素之间交替变化，则该子数组是湍流的。更形式化地说，子数组 `[arr[i], arr[i + 1], ..., arr[j]]` 当且仅当对所有 `k`（`i ≤ k < j`）满足以下两种情况之一时才是湍流的：

- 当 `(k - i)` 为偶数时 `arr[k] > arr[k + 1]`，且当 `(k - i)` 为奇数时 `arr[k] < arr[k + 1]`；
- 或者当 `(k - i)` 为偶数时 `arr[k] < arr[k + 1]`，且当 `(k - i)` 为奇数时 `arr[k] > arr[k + 1]`。

## 示例

### 示例 1
```
Input: arr = [9,4,2,10,7,8,8,1,9]
Output: 5
Explanation: arr[1] > arr[2] < arr[3] > arr[4] < arr[5]
```

### 示例 2
```
Input: arr = [4,8,12,16]
Output: 2
```

### 示例 3
```
Input: arr = [100]
Output: 1
```

## 约束条件

- `1 <= arr.length <= 4 * 10^4`
- `0 <= arr[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的子数组都枚举一遍，逐个判断它们是不是 **turbulent**（交替大小）：

1. **枚举子数组的起点 `i`**，再枚举终点 `j (i ≤ j)`。这相当于在数组里挑出一段连续的片段，就像我们在一串珠子里挑出一段连续的珠子。  
2. 对于每一个子数组 `[arr[i], …, arr[j]]`，从左到右检查相邻元素的比较符号（`>`、`<` 或 `=`）。如果出现了相等的情况直接判为不符合；如果比较符号在每一步都和前一步相反（`> < > < …` 或 `< > < > …`），则这段子数组是 **turbulent**。  
3. 只要找到符合条件的子数组，就记录它的长度，最后取最大的长度。

**为什么正确？**  
因为我们把「所有可能的子数组」都遍历了一遍，只要有符合要求的子数组，就一定会被检测到，记录的最大长度自然就是答案。

**复杂度大白话**：  
- 双层循环：外层跑 `n` 次，内层最坏也要跑 `n` 次，所以总共大概是 `n × n`，记作 **O(n²)**。把它想象成「如果你有 1000 件衣服，要把每件衣服和每另一件配对检查一次，需要大约 1000×1000 次比较」。
- 额外空间只用了几个计数器，和数组大小无关，记作 **O(1)**。

#### 代码（Python）

```python
def max_turbulent_bruteforce(arr):
    n = len(arr)
    ans = 1                     # 至少有一个元素时长度为 1

    # 遍历所有子数组的左端点 i
    for i in range(n):
        # cur_len 记录以 i 为左端点的当前子数组长度
        cur_len = 1
        # 记录上一次的比较符号：1 表示 >，-1 表示 <，0 表示 = 或尚未确定
        last_sign = 0

        # 遍历右端点 j (i+1 … n-1)
        for j in range(i + 1, n):
            # 计算 arr[j-1] 与 arr[j] 的比较符号
            if arr[j - 1] > arr[j]:
                cur_sign = 1
            elif arr[j - 1] < arr[j]:
                cur_sign = -1
            else:                # 相等，立刻终止这条子数组的检查
                break

            # 第一次比较时不需要翻转，只要记录符号即可
            if last_sign == 0 or cur_sign != last_sign:
                cur_len += 1          # 长度可以继续增长
                ans = max(ans, cur_len)
                last_sign = cur_sign  # 更新上一次的符号
            else:                     # 符号没有翻转，子数组不再 turbulent
                break

    return ans
```

#### 复杂度  

- **时间复杂度：O(n²)** — 需要两层循环，最坏情况下会检查每一对起止位置。  
- **空间复杂度：O(1)** — 只用了常数个变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于「每次都从头重新检查子数组」。实际上，只要我们在一次遍历中维护**当前符合 turbulent 条件的最长子数组的长度**，就不需要回头重新枚举。

关键观察：

1. **比较符号只可能是三种**：`>`、`<`、`=`。  
2. **只要出现 `=`，就必须把窗口（子数组）重新从下一个位置开始**，因为相等破坏了交替。  
3. 当比较符号在相邻两对之间**翻转**时（即 `>` 后跟 `<`，或 `<` 后跟 `>`），窗口可以继续向右扩展；否则（连续两个 `>` 或两个 `<`），窗口必须从**第二个元素**重新开始计数，因为从这里起才能重新尝试交替。

基于以上，我们可以使用 **滑动窗口**（双指针）：

- 用 `left` 记录当前窗口的左边界，用 `right` 从左到右遍历数组。  
- 维护 `prev_sign`（上一次比较的符号），当 `prev_sign == 0`（刚开始或遇到相等）时，把 `left = right - 1`，重新开始。  
- 当 `curr_sign` 与 `prev_sign` 不同且都不为 0 时，说明仍然是交替的，窗口可以继续扩展，更新答案。  
- 否则（符号相同或出现相等），把 `left = right - 1`，重新从 `right-1` 开始计数。

这样只遍历一次数组，时间 **O(n)**，空间 **O(1)**。

> **类比**：想象你在走一条山路，要求每一步要么上坡要么下坡，而且上坡下坡必须交替。如果两步都是上坡（或者下坡），你得回到上一次转折点重新开始计数；如果遇到平路（相等），只能从平路后面重新开始。

#### 代码（Python）

```python
def max_turbulent(arr):
    """
    返回最长 turbulent 子数组的长度，时间 O(n)，空间 O(1)。
    """
    n = len(arr)
    if n < 2:
        return n

    # left 为当前窗口的左边界（包含），right 为遍历指针
    left = 0
    ans = 1          # 至少有一个元素
    prev_sign = 0    # 前一次比较的符号，0 表示未定义或相等

    for right in range(1, n):
        # 计算 arr[right-1] 与 arr[right] 的比较符号
        if arr[right - 1] > arr[right]:
            cur_sign = 1
        elif arr[right - 1] < arr[right]:
            cur_sign = -1
        else:                # 相等，窗口必须重新开始
            cur_sign = 0

        if cur_sign == 0:            # 遇到相等，窗口只能从右边重新开始
            left = right
            prev_sign = 0
        elif prev_sign == 0:         # 第一次出现非零比较，窗口长度至少为 2
            prev_sign = cur_sign
            ans = max(ans, right - left + 1)
        elif cur_sign != prev_sign:  # 符号翻转，窗口继续扩张
            prev_sign = cur_sign
            ans = max(ans, right - left + 1)
        else:                         # 符号未翻转，窗口从 right-1 重新开始
            left = right - 1
            prev_sign = cur_sign
            ans = max(ans, right - left + 1)

    return ans
```

> **代码解释**（每行中文注释已在上方），核心在于：
> - `cur_sign` 用来判断当前两个元素的大小关系。  
> - `prev_sign` 记录上一次比较的关系，以便判断是否“翻转”。  
> - 根据 `cur_sign` 与 `prev_sign` 的组合，决定是否继续扩展窗口或重新定位左边界。

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次数组，每个元素的处理是常数时间。相比暴力的 O(n²)，快了很多，尤其在 `n` 达到 4·10⁴ 时差距非常明显。  
- **空间复杂度：O(1)** — 只用了几个整数变量，不随输入规模增长。

---

## 心得  

- **核心技巧**：利用**滑动窗口**实时维护“当前满足交替条件的最长子数组”。关键是把“比较符号翻转”抽象成一个状态 (`prev_sign`) 来驱动窗口的收缩与扩张。  
- **适用的题型**：  
  1. **最长上升/下降子数组**（需要单调性）  
  2. **最长子数组满足特定模式**（如交替奇偶、交替正负）  
  3. **带有“窗口失效条件”的子数组问题**（如最多 K 个不同字符、子数组和 ≤ target）  
- **一句话总结**：**“只要能用一次遍历把状态更新完，就能把 O(n²) 的暴力变成 O(n) 的滑动窗口。”**

---

## 反思  

- **第一反应**：看到“比较符号翻转”，立刻想到“枚举所有子数组检查”。这很自然，但容易忽视时间限制。  
- **最容易踩的坑**：  
  - **相等元素**：`=` 必须立刻终止当前窗口，否则会错误地把不满足条件的子数组计入长度。  
  - **窗口左边界的更新**：当出现连续相同符号（如 `> >`）时，左边界应该回退到 **第二个元素**（`right-1`），而不是直接跳到 `right`。  
  - **单元素数组**：答案应为 `1`，需要在代码开头处理 `n < 2` 的情况。  
- **下次类似题的第一步**：先把**比较符号**抽象成 `1 / -1 / 0`，判断“翻转”与“相等”两种失效条件，然后决定是用**滑动窗口**还是**DP**来一次遍历解决。