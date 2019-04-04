# #374. 猜数字（更高或更低） / Guess Number Higher or Lower

> 难度：简单 · 标签：Binary Search、Interactive · [LeetCode 链接](https://leetcode.com/problems/guess-number-higher-or-lower/)

---

## 题目（英文原版）

**Description**

We are playing the Guess Game. The game is as follows:
I pick a number from 1 to n. You have to guess which number I picked.
Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.
You call a pre-defined API int guess(int num), which returns three possible results:
Return the number that I picked.

**Examples**

**Example 1:**

```
Input: n = 10, pick = 6
Output: 6
```

**Example 2:**

```
Input: n = 1, pick = 1
Output: 1
```

**Example 3:**

```
Input: n = 2, pick = 1
Output: 1
```

**Constraints**

- 1 <= n <= 231 - 1
- 1 <= pick <= n

---

## 题目（中文翻译）

我们在进行猜数字游戏（Guess Game），规则如下：

- 我会从 `1` 到 `n` 之间（包含两端）选取一个整数。
- 你需要猜出我选的具体数字。
- 每次猜错后，我会告诉你我选的数字是比你猜的更高（higher）还是更低（lower）。
- 你需要调用预先定义好的 API `int guess(int num)`，该函数会返回三种可能的结果：
  - 返回 `-1` 表示我选的数字比 `num` 小（lower）。
  - 返回 `1` 表示我选的数字比 `num` 大（higher）。
  - 返回 `0` 表示 `num` 正好就是我选的数字。

**示例**

```text
示例 1:
Input: n = 10, pick = 6
Output: 6
```

```text
示例 2:
Input: n = 1, pick = 1
Output: 1
```

```text
示例 3:
Input: n = 2, pick = 1
Output: 1
```

**约束条件**

- `1 <= n <= 2^31 - 1`
- `1 <= pick <= n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**从 1 开始一点点尝试**，每猜一次就调用一次 `guess(num)`，  
如果返回值是 `0`（表示猜对了），立刻结束；否则根据返回的提示继续往下猜。  
这就好比在一排盒子里找钥匙，**顺序打开每个盒子**，直到找到为止。  

- **使用的数据结构**：这里只需要一个普通的整数变量 `i`，顺序递增即可。  
- **正确性**：因为题目保证答案一定在 `[1, n]` 之间，遍历所有可能的数字必然能找到正确答案。  
- **时间/空间复杂度**：最坏情况下要尝试所有 `n` 个数字，时间复杂度是 **O(n)**；只使用了常数个变量，空间复杂度是 **O(1)**。  

> **大白话解释**：`O(n)` 可以理解为“随 `n` 的增大，工作量几乎线性增长”。如果 `n` 是 1000，需要大约 1000 次猜测；如果 `n` 是 1 000 000，则需要约 1 000 000 次猜测，显然会慢。

#### 代码（Python）  

```python
# -------------------------------------------------
# 下面的代码仅用于本地模拟，真实提交时只需要实现 guessNumber()
# -------------------------------------------------
def guess(num: int) -> int:
    """
    模拟 LeetCode 提供的 API。
    - 返回 -1 表示 pick > num（答案更大）
    - 返回  1 表示 pick < num（答案更小）
    - 返回  0 表示 num 正好就是答案
    """
    if num < PICK:      # PICK 为全局的正确答案
        return -1
    if num > PICK:
        return 1
    return 0


def guessNumber_brute_force(n: int) -> int:
    """
    暴力解：从 1 到 n 逐个尝试
    """
    for i in range(1, n + 1):          # 依次尝试每一个可能的数字
        res = guess(i)                 # 调用 API 获得提示
        if res == 0:                   # 0 表示猜对了
            return i                   # 直接返回答案
    # 按题意这里一定能返回，不会走到下面
    return -1
```

#### 复杂度  

- **时间复杂度：O(n)** — 需要最多尝试 `n` 次，`n` 越大，耗时线性增长。  
- **空间复杂度：O(1)** — 只用了常数个变量（循环计数器 `i` 和返回值 `res`），不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次只能排除一个数字**，如果 `n` 很大会非常慢。  
观察题目：  

- 我们每次猜一个数后，`guess(num)` 会告诉我们答案是**更大**还是**更小**。  
- 这正好把搜索空间 **二分** 成两半：如果答案更大，就可以把左边全部舍弃；如果更小，就把右边全部舍弃。  

这就是**二分查找（Binary Search）**的核心思想。  
实现时维护两个指针 `left`、`right`，表示当前仍可能包含答案的闭区间 `[left, right]`。  
每轮取区间中点 `mid = left + (right - left) // 2`（这样写可以避免 `left + right` 可能产生的整数溢出），  

- `guess(mid) == 0` → 找到答案，直接返回。  
- `guess(mid) == -1` → 说明答案在 `mid` 右侧，更新 `left = mid + 1`。  
- `guess(mid) == 1` → 说明答案在 `mid` 左侧，更新 `right = mid - 1`。  

循环在 `left <= right` 时继续，必然在 `log₂ n` 次迭代内收敛到唯一答案。  

> **类比**：想象你在一本有序的字典里找某个单词，直接翻到中间的页码查看；如果单词在后半部，就把前半部撕掉，只在后半部继续二分查找。每一步都把剩余范围砍掉一半，效率大大提升。

#### 代码（Python）  

```python
def guessNumber_binary_search(n: int) -> int:
    """
    二分查找版本
    """
    left, right = 1, n               # 初始搜索区间是 [1, n]
    while left <= right:             # 只要区间还有可能包含答案就继续
        mid = left + (right - left) // 2   # 防止 left+right 溢出
        res = guess(mid)             # 调用 API 获取提示

        if res == 0:                  # 正好猜中
            return mid
        elif res == -1:               # 答案比 mid 大，排除左半边（含 mid）
            left = mid + 1
        else:                         # res == 1，答案比 mid 小，排除右半边（含 mid）
            right = mid - 1
    # 按题意这里永远不会到达，因为一定会在循环内部返回
    return -1
```

#### 复杂度  

- **时间复杂度：O(log n)** — 每次都把搜索区间大小减半，`n` 翻倍只会多一次循环。相较于暴力的 O(n)，对大 `n` 提升数十倍甚至上百倍。  
- **空间复杂度：O(1)** — 只使用了常数个变量（`left`, `right`, `mid`, `res`），不随 `n` 增长。

---

## 心得  

- **核心技巧**：二分搜索（Binary Search）。  
- **适用的题型**：  
  1. 在有序或单调的数值范围内寻找目标（如 `Sqrt(x)`、`First Bad Version`）。  
  2. 求满足某种单调条件的最小/最大值（如 “最小的满足条件的数组长度”。）  
  3. 任何可以把“更大/更小”信息用于排除半边的交互式题目。  
- **一句话总结**：把搜索空间每次砍掉一半，利用对数级的缩小速度快速定位答案。

---

## 反思  

- **拿到题目第一反应**：直接从 1 开始线性枚举——最直观但效率最低。  
- **最容易踩的坑**：  
  - **整数溢出**：`mid = (left + right) // 2` 在某些语言会因为 `left + right` 超出整数上限而出错，改写为 `left + (right - left) // 2` 更安全。  
  - **区间边界**：一定要使用闭区间 `[left, right]` 并在更新时正确处理 `mid` 本身（`mid+1`、`mid-1`），否则可能出现死循环。  
  - **交互 API 的返回值**：记清楚 `-1` 表示答案更大，`1` 表示答案更小，别弄混了。  
- **下次遇到同类题，第一步该想到**：**“能否二分？”**——先判断搜索空间是否是单调的或可以通过比较得到方向信息，若可以，就立刻尝试二分搜索。