# #2834. 找出美丽数组的最小可能和 / Find the Minimum Possible Sum of a Beautiful Array

> 难度：中等 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-possible-sum-of-a-beautiful-array/)

---

## 题目（英文原版）

**Description**

You are given positive integers n and target.
An array nums is beautiful if it meets the following conditions:
Return the minimum possible sum that a beautiful array could have modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 2, target = 3
Output: 4
Explanation: We can see that nums = [1,3] is beautiful.
- The array nums has length n = 2.
- The array nums consists of pairwise distinct positive integers.
- There doesn't exist two distinct indices, i and j, with nums[i] + nums[j] == 3.
It can be proven that 4 is the minimum possible sum that a beautiful array could have.
```

**Example 2:**

```
Input: n = 3, target = 3
Output: 8
Explanation: We can see that nums = [1,3,4] is beautiful.
- The array nums has length n = 3.
- The array nums consists of pairwise distinct positive integers.
- There doesn't exist two distinct indices, i and j, with nums[i] + nums[j] == 3.
It can be proven that 8 is the minimum possible sum that a beautiful array could have.
```

**Example 3:**

```
Input: n = 1, target = 1
Output: 1
Explanation: We can see, that nums = [1] is beautiful.
```

**Constraints**

- 1 <= n <= 109
- 1 <= target <= 109

---

## 题目（中文翻译）

给定正整数 `n` 和 `target`。  
如果数组 `nums` 满足以下条件，则称其为 **美丽数组**（beautiful array）：

（题目原文中未列出具体条件，这里保持原样）

返回一个美丽数组可能拥有的 **最小和**（minimum possible sum），并对 `10^9 + 7` 取模。

---

### 示例

**示例 1**  
**输入**: `n = 2, target = 3`  
**输出**: `4`  
**解释**: 我们可以看到数组 `nums = [1,3]` 是美丽的。  
- 数组 `nums` 的长度为 `n = 2`。  
- `nums` 由两两不同的正整数构成。  
- 不存在两个不同的下标 `i` 和 `j` 使得 `nums[i] + nums[j] == 3`。  
可以证明，`4` 是美丽数组可能拥有的最小和。

**示例 2**  
**输入**: `n = 3, target = 3`  
**输出**: `8`  
**解释**: 我们可以看到数组 `nums = [1,3,4]` 是美丽的。  
- 数组 `nums` 的长度为 `n = 3`。  
- `nums` 由两两不同的正整数构成。  
- 不存在两个不同的下标 `i` 和 `j` 使得 `nums[i] + nums[j] == 3`。  
可以证明，`8` 是美丽数组可能拥有的最小和。

**示例 3**  
**输入**: `n = 1, target = 1`  
**输出**: `1`  
**解释**: 我们可以看到数组 `nums = [1]` 是美丽的。

---

### 约束条件

- `1 <= n <= 10^9`  
- `1 <= target <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从小到大依次尝试加入数字**，只要满足下面两个条件就把它放进数组 `nums`：

1. 该数字是正整数且之前没有出现（相当于“字典里没有这个词”，这里的字典是已经选过的数字集合）。  
2. 选了它以后，**不会出现两数之和等于 `target`**。这等价于：如果已经选过 `target - x`，那么 `x` 不能再选。可以把 “已选的数字” 想成一本查字典的笔记本，`target - x` 就是字典里对应的另一页，如果那一页已经写了，`x` 这页就不能写。

只要满足这两个条件，就把数字加入 `nums`，直到数组长度达到 `n` 为止。

> **为什么正确**  
> 由于我们始终挑最小的可用数字，得到的数组一定是“最小和”。如果把某个更大的数字换成更小的合法数字，和会更小，所以贪心的选择不会错。

> **时间/空间复杂度**  
> - **时间**：我们可能需要检查从 `1` 到很大的数（最坏情况是 `O(n + target)`），每检查一次都要在已选集合里查找 complement，使用哈希表可以在 `O(1)` 完成。整体是 **线性** 的 `O(n + target)`。  
> - **空间**：需要保存已经选的数字，最坏保存 `n` 个，空间是 **`O(n)`**。

> **大白话解释**  
> - `O(n)` 就是“随 `n` 增长的速度”。比如 `n` 增加一倍，时间大约也增加一倍。  
> - `O(n²)`（这里没有出现）则是“随 `n` 增长的速度是 `n` 的平方”，比如 `n=1000` 时要耗费大约 `1,000,000` 次操作，明显太慢。

#### 代码（Python）

```python
def min_beautiful_sum_bruteforce(n: int, target: int) -> int:
    MOD = 10 ** 9 + 7
    chosen = set()          # 已经选过的数字
    cur = 1                  # 当前尝试的数字
    total = 0                # 当前数组的和

    while len(chosen) < n:
        # 1) 不能和已有的数字形成 target
        if (target - cur) in chosen:
            cur += 1
            continue

        # 2) 必须是正整数且未出现过
        chosen.add(cur)
        total = (total + cur) % MOD
        cur += 1

    return total
```

> **关键行中文注释**  
> - `chosen` 相当于“字典”，记录已经写下的数字。  
> - `if (target - cur) in chosen:` 检查“另一页”是否已经写过，若是则跳过当前数字。  

#### 复杂度

- **时间复杂度**：`O(n + target)` —— 需要逐个检查直到找到 `n` 个合法数，最坏情况下要走到 `target` 左右的数。  
- **空间复杂度**：`O(n)` —— 需要存储已选的 `n` 个数字。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐个尝试**，当 `n` 可达 `10⁹` 时根本不可行。  
观察贪心过程可以发现一种**规律**：

| 目标 `target` | 小于 `target` 的合法数字 | 被阻塞的数字 |
|---------------|------------------------|------------|
| `target = 7`  | `1, 2, 3`              | `6, 5, 4`  |
| `target = 8`  | `1, 2, 3, 4`           | `7, 6, 5`  |

- 对每一对 `(a, target‑a)`（其中 `a < target‑a`），我们只能选其中一个，**贪心总是选更小的 `a`**。  
- 因此**所有小于 `target` 且不大于 `target//2` 的正整数**（记作 `k = target // 2`）必然会被选进数组。  
- 这 `k` 个数的和是 `k·(k+1)/2`（等差数列求和公式）。

剩下的数字只能从 **`target` 开始往后** 取，因为 `k+1 … target‑1` 正好是已经被前面小数的 complement，不能再用。  

于是得到完整的数学公式：

1. **如果 `n ≤ k`**（不需要用到 `target` 及其之后的数）  
   \[
   \text{答案} = 1 + 2 + \dots + n = \frac{n(n+1)}{2}
   \]

2. **如果 `n > k`**  
   - 已选的 `k` 个小数和：`sum_small = k·(k+1)//2`  
   - 还需要 `m = n - k` 个数，从 `target` 开始的等差数列：  
     \[
     \text{extra} = m·target + \frac{m(m-1)}{2}
     \]
   - 最终答案：`sum_small + extra`

所有运算只涉及常数次加减乘除，**时间 O(1)，空间 O(1)**，即使 `n = 10⁹` 也能瞬间算出。

> **核心概念解释**  
> - **等差数列**：比如 `5,6,7,8`，每项与前一项的差相同（这里是 `1`），求和可以用 “首项 + 末项” × 项数 ÷ 2。  
> - **整数除法 `//`**：在 Python 中表示向下取整，例如 `7 // 2 = 3`。  
> - **模运算**：题目要求答案对 `10⁹+7` 取余，防止整数溢出，直接在每一步取模即可。

#### 代码（Python）

```python
def min_beautiful_sum(n: int, target: int) -> int:
    MOD = 10 ** 9 + 7

    k = target // 2                     # 能直接取的最小正整数的个数
    if n <= k:                          # 只需要前 n 个自然数
        ans = n * (n + 1) // 2
        return ans % MOD

    # n > k，需要把 k 个小数和剩下的 m 个 >= target 的数都加进来
    sum_small = k * (k + 1) // 2        # 1 + 2 + ... + k
    m = n - k                           # 还缺多少个数
    # 等差数列：target, target+1, ..., target+m-1
    extra = m * target + m * (m - 1) // 2

    ans = (sum_small + extra) % MOD
    return ans
```

> **关键行中文注释**  
> - `k = target // 2`：相当于“把目标数分成两半，左边的数全部可以直接用”。  
> - `if n <= k:`：如果要的个数不超过左半边，直接算前 `n` 个自然数的和。  
> - `extra = m * target + m * (m - 1) // 2`：先把每个数的基准 `target` 加进去（`m` 次），再加上等差递增的 `0,1,2,…` 部分。

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做常数次算术运算。  
- **空间复杂度**：`O(1)` —— 只使用几个整数变量。

与暴力解相比，时间从可能的 `O(n + target)` 降到了 **常数时间**，能够轻松处理 `n`、`target` 高达 `10⁹` 的极端数据。

---

## 心得

- **核心技巧**：把“不能出现两数之和等于 `target`”转化为“每对 `(a, target‑a)` 只能选一个”，然后利用**贪心选最小的**得到一个明确的数列结构。  
- **适用的题型**  
  1. “禁止出现某种配对关系” 的构造题（例如 **“数组中不出现和为 `k` 的两数”**）。  
  2. 需要 **最小/最大和** 且约束为“互斥配对”的问题（如 **“不允许出现相邻两数差为 1”** 的变体）。  
- **一句话总结解题钥匙**：**把配对限制化为“每对只能取一个”，贪心取最小的，然后用等差数列公式一次算完**。

---

## 反思

- **第一反应**：先写一个逐个检查的暴力程序，确认思路是否正确。  
- **最容易踩的坑**  
  - 忽略 `target` 为奇数/偶数时 `target//2` 的差异，导致漏算或多算了 `target/2`。  
  - 边界情况 `target = 1`（此时 `k = 0`），需要从 `1` 开始直接取数。  
  - 在大数求和时忘记取模，导致 Python 整数虽然不会溢出，但提交会超时/内存。  
- **下次类似题的第一步**：先**找出“互斥配对”**，确定每对只能保留一个，然后**计算可以直接取的最小集合的大小**，再用等差数列或组合数学一次性求和。