# #2379. 最少重新着色使连续黑块数达到 K / Minimum Recolors to Get K Consecutive Black Blocks

> 难度：简单 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string blocks of length n, where blocks[i] is either 'W' or 'B', representing the color of the ith block. The characters 'W' and 'B' denote the colors white and black, respectively.
You are also given an integer k, which is the desired number of consecutive black blocks.
In one operation, you can recolor a white block such that it becomes a black block.
Return the minimum number of operations needed such that there is at least one occurrence of k consecutive black blocks.

**Examples**

**Example 1:**

```
Input: blocks = "WBBWWBBWBW", k = 7
Output: 3
Explanation:
One way to achieve 7 consecutive black blocks is to recolor the 0th, 3rd, and 4th blocks
so that blocks = "BBBBBBBWBW". 
It can be shown that there is no way to achieve 7 consecutive black blocks in less than 3 operations.
Therefore, we return 3.
```

**Example 2:**

```
Input: blocks = "WBWBBBW", k = 2
Output: 0
Explanation:
No changes need to be made, since 2 consecutive black blocks already exist.
Therefore, we return 0.
```

**Constraints**

- n == blocks.length
- 1 <= n <= 100
- blocks[i] is either 'W' or 'B'.
- 1 <= k <= n

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n`、下标从 0 开始的字符串 `blocks`，其中 `blocks[i]` 为 `'W'` 或 `'B'`，分别表示第 `i` 块的颜色为白色（white）或黑色（black）。  
另给定一个整数 `k`，表示希望得到的连续黑块（black blocks）的数量。  
在一次操作中，你可以把一块白色块重新着色为黑色块。  
返回至少出现一次 `k` 个连续黑块所需的最少操作次数。

**示例 1**  
```
Input: blocks = "WBBWWBBWBW", k = 7
Output: 3
Explanation:
一种实现 7 个连续黑块的方法是把第 0、3、4 块重新着色为黑色，使得
blocks = "BBBBBBBWBW"。  
可以证明，少于 3 次操作无法得到 7 个连续黑块。因此返回 3。
```

**示例 2**  
```
Input: blocks = "WBWBBBW", k = 2
Output: 0
Explanation:
已经存在 2 个连续的黑块，不需要任何修改。因此返回 0。
```

**约束条件**  
- `n == blocks.length`
- `1 <= n <= 100`
- `blocks[i]` 只能是 `'W'` 或 `'B'`
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有长度为 `k` 的连续子串都枚举一遍**，看每个子串里有多少个 `'W'`（白块），因为只有白块需要染成黑块。  
- **数据结构**：只需要遍历字符串，用一个整数 `cnt` 记录当前子串里 `'W'` 的个数。可以把它想象成在一本字典里查词：字典的“键”是子串的起始位置，值就是这段子串里需要改颜色的次数。  
- **正确性**：如果我们把某个子串全部变成黑色，那么恰好需要把子串里所有的白块染成黑块，次数就是白块的数量。遍历所有可能的子串后，最小的白块数就是最少需要的操作次数。  

#### 代码（Python）

```python
def minRecolorBlocks_bruteforce(blocks: str, k: int) -> int:
    n = len(blocks)
    min_ops = float('inf')                     # 记录最小操作次数，初始设为无穷大
    # 枚举所有长度为 k 的窗口的左端点 i
    for i in range(n - k + 1):
        # 统计窗口 [i, i+k) 内有多少个 'W'
        ops = 0
        for j in range(i, i + k):
            if blocks[j] == 'W':               # 遇到白块就需要一次染色
                ops += 1
        # 更新全局最小值
        min_ops = min(min_ops, ops)
    return min_ops
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  对每个起始位置（最多 `n` 个）都要遍历 `k` 长度的子串。可以把 `O(n * k)` 想象成“把一本 100 页的书，每页再读 10 行”，总共要读 1000 行。  
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量，和输入大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新统计窗口内的 `'W'`**，这导致 `k` 重复计算。  
我们可以利用 **滑动窗口（Sliding Window）** 的思想，把窗口向右移动时，只关注**进入窗口和离开窗口的两个字符**，这样就能在 `O(1)` 时间内更新计数，整体只需 `O(n)`。

1. **初始化**：先把前 `k` 个字符的 `'W'` 数目算出来，记为 `curr`。  
2. **滑动窗口**：窗口左端从 `0` 移到 `n-k`。每次右移一步，  
   - 如果左侧离开的字符是 `'W'`，`curr` 减 1（因为窗口里少了一个白块）。  
   - 如果新加入的右侧字符是 `'W'`，`curr` 加 1（因为窗口里多了一个白块）。  
3. 每一步都把 `curr` 和全局最小值 `ans` 比较，保留更小的那个。  
4. 最后 `ans` 即为答案。  

**类比**：想象你在看一条长跑道，上面有若干块白色的石头（需要搬走）和黑色的石头（已经是目标）。你一次只能看到长度为 `k` 的窗口。刚开始数一下窗口里白石头的数量，之后每往前走一步，只需要检查刚离开窗口的那块石头和刚进入窗口的那块石头，省去重新数整个窗口的麻烦。

#### 代码（Python）

```python
def minRecolorBlocks(blocks: str, k: int) -> int:
    n = len(blocks)
    # 1. 统计第一个窗口 [0, k) 内的白块数
    curr = sum(1 for i in range(k) if blocks[i] == 'W')
    ans = curr                                 # 初始化答案为第一个窗口的结果

    # 2. 窗口左端从 1 开始滑动到 n-k
    for left in range(1, n - k + 1):
        # 离开窗口的字符下标是 left-1
        if blocks[left - 1] == 'W':
            curr -= 1                           # 少了一个白块
        # 新进入窗口的字符下标是 left + k - 1
        if blocks[left + k - 1] == 'W':
            curr += 1                           # 多了一个白块
        ans = min(ans, curr)                    # 保留最小值

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了一遍字符串，像是“把一本 100 页的书一次性读完”，每页只看一次。相比暴力解的 `O(n·k)`，快了很多，尤其当 `k` 接近 `n` 时差距尤为明显。  
- **空间复杂度**：`O(1)`  
  只用了几个整数变量，额外空间常数级。

---

## 心得

- **核心技巧**：**滑动窗口**——在需要统计“固定长度子数组/子串的某种属性”时，利用窗口的移动只更新增删的元素，避免重复计数。  
- **适用题型**：  
  1. “最少翻转使子串全部相同”类（如本题、LeetCode 1658 Minimum Operations to Reduce X to Zero 的变体）。  
  2. “最长满足条件的子数组/子串”类（如 1003. 检查子数组是否连续、3. 最长无重复子串）。  
  3. “窗口内元素之和/乘积达到目标”类（如 209. 长度最小的子数组）。  
- **一句话总结解题钥匙**：**把“大块问题”拆成“相邻小块的增量变化”，用窗口一次滑动解决**。

---

## 反思

- **第一反应**：看到“在长度为 k 的连续块里，把所有白块改成黑块”，立刻想到枚举所有子串并统计白块数。  
- **最容易踩的坑**：  
  - **边界处理**：窗口右端的下标是 `left + k - 1`，容易写成 `left + k` 导致越界。  
  - **k = n** 的特殊情况：此时只需要统计整串的白块数，滑动窗口的循环体不应执行。  
  - **初始化错误**：忘记把第一个窗口的白块数计入答案，会导致返回错误的最小值。  
- **下次遇到同类题**：第一步先**判断是否可以用固定长度滑动窗口**，如果是，立刻写出窗口的初始化和增删更新公式，再在此基础上求最值。这样可以把时间从 `O(n·k)` 降到 `O(n)`。