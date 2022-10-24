# #1982. **根据子集和找数组** / Find Array Given Subset Sums

> 难度：困难 · 标签：Array、Divide and Conquer · [LeetCode 链接](https://leetcode.com/problems/find-array-given-subset-sums/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the length of an unknown array that you are trying to recover. You are also given an array sums containing the values of all 2n subset sums of the unknown array (in no particular order).
Return the array ans of length n representing the unknown array. If multiple answers exist, return any of them.
An array sub is a subset of an array arr if sub can be obtained from arr by deleting some (possibly zero or all) elements of arr. The sum of the elements in sub is one possible subset sum of arr. The sum of an empty array is considered to be 0.
Note: Test cases are generated such that there will always be at least one correct answer.

**Examples**

**Example 1:**

```
Input: n = 3, sums = [-3,-2,-1,0,0,1,2,3]
Output: [1,2,-3]
Explanation: [1,2,-3] is able to achieve the given subset sums:
- []: sum is 0
- [1]: sum is 1
- [2]: sum is 2
- [1,2]: sum is 3
- [-3]: sum is -3
- [1,-3]: sum is -2
- [2,-3]: sum is -1
- [1,2,-3]: sum is 0
Note that any permutation of [1,2,-3] and also any permutation of [-1,-2,3] will also be accepted.
```

**Example 2:**

```
Input: n = 2, sums = [0,0,0,0]
Output: [0,0]
Explanation: The only correct answer is [0,0].
```

**Example 3:**

```
Input: n = 4, sums = [0,0,5,5,4,-1,4,9,9,-1,4,3,4,8,3,8]
Output: [0,-1,4,5]
Explanation: [0,-1,4,5] is able to achieve the given subset sums.
```

**Constraints**

- 1 <= n <= 15
- sums.length == 2n
- -104 <= sums[i] <= 104

---

## 题目（中文翻译）

你得到一个整数 `n`，表示一个未知数组的长度，你需要恢复该数组。同时，给定一个数组 `sums`，其中包含未知数组所有 `2^n` 个子集和（subset sum）的取值，顺序任意。  

返回长度为 `n` 的数组 `ans`，即未知数组的一个可能取值。如果存在多个答案，返回任意一个即可。

> **子集（subarray）**：如果一个数组 `sub` 能通过删除原数组 `arr` 中的若干（可能为零或全部）元素得到，则称 `sub` 为 `arr` 的子集。`sub` 中所有元素的和即为 `arr` 的一个子集和（subset sum）。空数组的和定义为 `0`。  

**注意**：测试数据保证至少存在一个正确答案。

### 示例

#### 示例 1  
**输入**: `n = 3, sums = [-3,-2,-1,0,0,1,2,3]`  
**输出**: `[1,2,-3]`  
**解释**: `[1,2,-3]` 能产生给出的所有子集和：

- `[]`：和为 `0`
- `[1]`：和为 `1`
- `[2]`：和为 `2`
- `[1,2]`：和为 `3`
- `[-3]`：和为 `-3`
- `[1,-3]`：和为 `-2`
- `[2,-3]`：和为 `-1`
- `[1,2,-3]`：和为 `0`

任意 `[1,2,-3]` 的排列，或 `[-1,-2,3]` 的任意排列，都视为合法答案。

#### 示例 2  
**输入**: `n = 2, sums = [0,0,0,0]`  
**输出**: `[0,0]`  
**解释**: 唯一正确的答案是 `[0,0]`。

#### 示例 3  
**输入**: `n = 4, sums = [0,0,5,5,4,-1,4,9,9,-1,4,3,4,8,3,8]`  
**输出**: `[0,-1,4,5]`  
**解释**: `[0,-1,4,5]` 能产生给出的所有子集和。

### 约束条件
- `1 <= n <= 15`
- `sums.length == 2^n`
- `-10^4 <= sums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的数组都枚举出来**，然后检查它们的子集和集合是否和题目给出的 `sums` 完全相同。

- **枚举数组**：长度为 `n`，每个位置的取值范围是 `[-10⁴, 10⁴]`（题目限制），这相当于把一个 20 001 进制的数写成 `n` 位。即使 `n=5`，可能的组合也已经是 `20001⁵ ≈ 3.2×10²⁰`，根本不可行。
- **验证子集和**：对于每个候选数组，计算它的全部 `2ⁿ` 个子集和（可以用位运算枚举子集），再把得到的列表与 `sums` 做比较。

> **为什么这个方法一定能得到答案？**  
> 因为题目保证 `sums` 正好是某个真实数组的全部子集和。只要我们把所有可能的数组都穷举出来，必然会碰到这个真实数组，检查时自然会通过。

> **时间/空间复杂度**  
> - **时间**：枚举每个数组需要 `O((range)ⁿ)`，每次验证又要 `O(2ⁿ)`，整体是 **指数级**，即 `O((range)ⁿ·2ⁿ)`。用大白话说，就是“天文数字”，即使最小的 `n=5` 也会耗时多年。  
> - **空间**：只需要存放一个候选数组和它的子集和，空间是 `O(2ⁿ)`（用于保存子集和的临时列表），即最多几千个整数，算是“小”。

显然，这种“暴力”根本不可用，只能作为思考的起点：**我们必须利用 `sums` 本身提供的结构信息**，而不是盲目枚举。

#### 代码（Python）

```python
import itertools

def brute_force_find_array(n: int, sums: list[int]) -> list[int]:
    # 这里仅作演示，实际运行会超时
    lo, hi = -10_000, 10_000
    # 枚举所有可能的数组（极其慢）
    for cand in itertools.product(range(lo, hi + 1), repeat=n):
        # 计算 cand 的所有子集和
        subset_sums = []
        for mask in range(1 << n):               # 0 .. 2^n-1
            s = 0
            for i in range(n):
                if mask >> i & 1:                # 第 i 位为 1，说明选了第 i 个元素
                    s += cand[i]
            subset_sums.append(s)
        # 检查是否与给出的 sums 完全相同（忽略顺序）
        if sorted(subset_sums) == sorted(sums):
            return list(cand)
    return []   # 题目保证一定有解，这行永远不被执行
```

#### 复杂度

- **时间复杂度**：`O((2·10⁴+1)ⁿ · 2ⁿ)`，指数级，实际不可接受。  
- **空间复杂度**：`O(2ⁿ)`，用于存放一次子集和的临时数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**我们并不需要枚举所有可能的数组**，只要利用 `sums` 本身的“层次结构”。  
关键观察如下：

1. **最大子集和**  
   把所有子集和从小到大排好序，最后一个元素一定是 **所有元素之和**（把每个数都选进来的子集）。记作 `total = max(sums)`。

2. **把数组拆成两部分**  
   假设我们已经知道了数组的最后一个元素 `x`（正数或负数），那么其余 `n‑1` 个元素组成的子集和集合记为 `A`。  
   加上 `x` 后的子集和集合记为 `B`。显然  
   `sums = A ∪ (A + x)`，其中 `A + x` 表示把 `A` 中每个和都加上 `x`。  
   这意味着：**如果我们把 `sums` 按照是否包含 `x` 分成两组，就能得到 `A`**，而 `A` 正是 **去掉一个元素后的子集和集合**。

3. **如何得到 `x`？**  
   - `total`（最大和）一定是 `sum(all elements)`。  
   - `second_max`（倒数第二大的和）一定是 `total - min_element`，因为把最小的那个数从完整集合里去掉，得到的子集和恰好是第二大。  
   - 于是 `x = total - second_max` 可能是 **最小的元素**，也可能是 **最大的元素的相反数**（因为我们并不知道正负号）。  

   为了兼容正负两种情况，我们尝试两种候选 `x`：`candidate = total - second_max` 与 `-candidate`。

4. **递归恢复**  
   - 把 `sums` 按照是否包含 `candidate` 分成两组 `group0`（不含）和 `group1`（含），具体做法是：从最小的和开始，用一个计数器（类似“多重集合”）匹配。  
   - 若分组成功且 `group0` 与 `group1` 的大小均为 `2^{n‑1}`，则 `group0` 正好是去掉 `candidate` 后的子集和集合。  
   - 对 `group0` 递归求解，得到长度为 `n‑1` 的子数组 `rest`。  
   - 最终答案为 `rest + [candidate]`（顺序随意）。

5. **为什么递归一定能结束？**  
   每次递归把问题规模从 `n` 降到 `n‑1`，且 `n ≤ 15`，递归深度最多 15，完全可接受。

> **核心数据结构：多重集合（Counter）**  
> 在 Python 中用 `collections.Counter` 实现，它类似于字典，记录每个数出现了多少次。可以把它想象成“装有很多相同标签的小球的盒子”，取出一个球就相当于把对应的计数减 1。

> **类比**：把 `sums` 看成一本“账本”，每一行记了一次购物的总花费。我们要找出哪一件商品的价格是 `x`，只要把所有含有这件商品的记录（把 `x` 加进去）和不含它的记录配对，就能把这件商品从账本里“剔除”，得到只剩下其余商品的账本。递归继续，最后把所有商品的价格都找出来。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def recover_array(n: int, sums: List[int]) -> List[int]:
    """
    主入口：返回任意一个满足条件的原数组（顺序任意）
    """
    sums.sort()                     # 先排序，便于后面分组
    return _helper(n, sums)

def _helper(k: int, sums: List[int]) -> List[int]:
    """
    递归函数，已知当前子问题的长度为 k，子集和集合为 sums（已排好序）。
    返回对应的长度为 k 的原数组（顺序任意）。
    """
    if k == 0:                      # 空数组的子集和只有一个 0
        return []

    # 1. 取出最大和（全部元素之和）
    total = sums[-1]                # 最大值
    # 2. 取出次大和，利用它推断候选元素
    second_max = sums[-2]

    # candidate 可能是最小元素，也可能是最大元素的相反数
    cand = total - second_max

    # 尝试两种符号（cand 与 -cand）
    for x in (cand, -cand):
        # 用 Counter 记录所有子集和的出现次数
        cnt = Counter(sums)
        group0 = []                 # 不含 x 的子集和
        group1 = []                 # 含 x 的子集和

        # 按照从小到大的顺序配对
        for s in sums:
            if cnt[s] == 0:         # 已经被配对过，跳过
                continue
            # s 属于 group0（不含 x）
            group0.append(s)
            cnt[s] -= 1
            # 对应的 s + x 必须在 group1 中
            t = s + x
            if cnt[t] == 0:         # 配对失败，说明 x 取值不对
                break
            group1.append(t)
            cnt[t] -= 1
        else:
            # 成功配对完所有元素，说明 x 正确
            # 递归求解剩余的 k-1 个数
            rest = _helper(k - 1, group0)
            return rest + [x]      # 把当前找到的元素加到答案里

    # 按题目保证一定有解，这行理论上不会执行
    raise ValueError("No valid reconstruction found")
```

**关键注释说明**  

- `cnt = Counter(sums)` 把所有子集和放进“多重集合”，相当于把账本里的每张票据放进一个可以计数的盒子。  
- 循环中 `if cnt[s] == 0: continue` 表示这张票据已经被配对使用过，直接跳过。  
- `t = s + x` 表示如果我们把候选元素 `x` 加进子集，那么对应的总和应该是 `s + x`。我们在盒子里找这张票据并把它标记为已使用。  
- `else:` 与 `for` 配合使用：只有在循环 **没有** 因 `break` 而提前退出时，才会执行 `else` 块，说明配对成功。  

#### 复杂度

- **时间复杂度**  
  每一层递归都要遍历一次当前的 `sums`（长度 `2^k`），并进行常数次的计数操作。递归深度为 `n`，所以总时间是  
  \[
  O\!\left(\sum_{k=0}^{n-1} 2^{k}\right)=O(2^{n})
  \]  
  用大白话说，就是“最多需要检查所有子集和一次”，对 `n≤15` 来说最多只有 `2^{15}=32768` 次，完全够快。  

- **空间复杂度**  
  递归栈深度为 `n`，每层保存一个大小为 `2^{k}` 的列表（`group0`），但所有层加起来仍然是 `O(2^{n})`（因为每层的列表互不重叠）。再加上 `Counter` 的额外存储，也都是 `O(2^{n})`。对本题的限制，这只是一小段内存（几万整数）。

> 与暴力解相比，时间从 **指数的指数** 降到了 **普通的指数**，效率提升了天壤之别。

---

## 心得

- **核心技巧**：利用子集和集合的“加/不加”结构，把原数组逐个“摘除”。关键是把 `sums` 按是否包含某个候选元素划分为两组，这一步用多重集合（Counter）实现配对。  
- **适用的题型**  
  1. **Recover Array From Subset Sums**（本题）  
  2. **Find Array Given XOR of Subsets**（使用异或代替加法的类似思路）  
  3. **Split Array Into Two Subsets With Given Difference**（需要把集合划分成两部分的题目）  
- **一句话总结解题钥匙**：**最大子集和告诉我们整体和，剩下的子集和可以两两配对得到候选元素，递归把数组一点点剥离**。

---

## 反思

- **第一反应**：看到“所有子集和”，立刻想到“枚举所有数组”。这是一种**盲目搜索**的思路，虽然直观但完全不可行。  
- **最容易踩的坑**  
  1. **负数的处理**：`candidate` 可能是正数也可能是负数，需要尝试两种符号。  
  2. **多重集合配对**：如果直接用 `list.remove`，在出现相同数值多次时会出错。必须用 `Counter` 或手动计数。  
  3. **边界条件**：当 `n=0`（空数组）或所有元素都为 `0` 时，`sums` 只有全 0，递归终止条件要写对。  
- **下次遇到同类题**：**第一步**先看最大、次大的子集和，利用它们推断可能的“当前元素”，随后用 **配对分组 + 递归** 的思路逐层剥离。这样可以把指数搜索压缩到可接受的规模。