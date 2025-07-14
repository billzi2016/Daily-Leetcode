# #3266. **K 次乘法操作后的最终数组状态 II** / Final Array State After K Multiplication Operations II

> 难度：困难 · 标签：Array、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums, an integer k, and an integer multiplier.
You need to perform k operations on nums. In each operation:
After the k operations, apply modulo 109 + 7 to every value in nums.
Return an integer array denoting the final state of nums after performing all k operations and then applying the modulo.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,5,6], k = 5, multiplier = 2
Output: [8,4,6,5,6]
Explanation:
```

**Example 2:**

```
Input: nums = [100000,2000], k = 2, multiplier = 1000000
Output: [999999307,999999993]
Explanation:
```

**Constraints**

- 1 <= nums.length <= 104
- 1 <= nums[i] <= 109
- 1 <= k <= 109
- 1 <= multiplier <= 106

---

## 题目（中文翻译）

你被给定一个整数数组 `nums`、一个整数 `k`，以及一个整数 `multiplier`。  
需要对 `nums` 执行 `k` 次操作。每一次操作的具体规则如下：  

（题目原文中未给出每次操作的细节，此处保留原样）

在完成全部 `k` 次操作后，对 `nums` 中的每个值取模 `10^9 + 7`。  
返回一个整数数组，表示在执行完所有 `k` 次操作并随后取模后的 `nums` 最终状态。

### 示例

**示例 1**  
```text
输入: nums = [2,1,3,5,6], k = 5, multiplier = 2
输出: [8,4,6,5,6]
解释:
```

**示例 2**  
```text
输入: nums = [100000,2000], k = 2, multiplier = 1000000
输出: [999999307,999999993]
解释:
```

### 约束条件

- `1 <= nums.length <= 10^4`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`
- `1 <= multiplier <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把题目说的“每一次操作”**真的一次一次地执行**。  
操作的描述是：

1. 在当前数组 `nums` 中找出最小的那个数（最小值），记作 `x`。  
2. 用给定的 `multiplier` 把它乘一下，得到 `x·multiplier`。  
3. 用新的值替换掉原来的最小值。  

这一步可以用 **最小堆（priority queue）** 来实现，堆就像一个随时可以拿到“字典里最前面那一页”的工具：  
- 堆顶（`heap[0]`）总是当前最小的元素，取出来的时间是 `O(log n)`。  
- 把新值放回堆里同样是 `O(log n)`。

我们把上面的三步循环 `k` 次，最后把每个数取模 `10^9+7` 即可。

> **为什么这一定是对的？**  
> 题目只说“每一次都对当前最小的数乘以 multiplier”，而我们正是严格按照这个规则一步一步走，所以答案一定和题目要求一致。

> **时间/空间复杂度的大白话**  
> - `O(k log n)`：想象有 `k` 次“取最小 + 放回” 的操作，每一次都要在 `log n`（约等于把 `n` 本书排好顺序后找第 1 本的时间）里完成。  
> - `O(n)`：我们只需要保存 `n` 个数和它们在堆里的位置，额外的空间和原数组大小是同一个量级。

#### 代码（Python）

```python
import heapq

MOD = 10 ** 9 + 7

def finalArray_bruteforce(nums, k, multiplier):
    """
    暴力模拟：每一次都找最小值乘以 multiplier
    适用于 k 较小的情况（比如 k <= 10^5）
    """
    n = len(nums)
    # 用 (value, index) 的元组保存堆，这样最后还能把结果放回原来的下标位置
    heap = [(val, i) for i, val in enumerate(nums)]
    heapq.heapify(heap)               # O(n) 建堆

    for _ in range(k):                # 循环 k 次
        val, idx = heapq.heappop(heap)   # 取出当前最小的数（O(log n)）
        val = val * multiplier           # 乘以 multiplier
        heapq.heappush(heap, (val, idx)) # 放回堆中（O(log n)）

    # 把堆里的值写回原数组，并统一取模
    res = [0] * n
    while heap:
        val, idx = heapq.heappop(heap)
        res[idx] = val % MOD
    return res
```

#### 复杂度

- **时间复杂度**：`O(k log n)`  
  解释：每一次操作都要“弹出最小 + 插入新值”，各需要 `log n` 的时间，循环 `k` 次就乘起来。

- **空间复杂度**：`O(n)`  
  解释：我们只在堆里保存 `n` 个 `(value, index)`，没有额外的与 `k` 成正比的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **`k` 可能非常大（最高 10^9）**，逐步模拟会超时。  
我们需要找出 **何时可以一次性算完很多次操作**，而不是一步一步走。

---

#### 2.1 观察：什么时候会“卡住”？

设当前数组的最小值为 `mn`，最大值为 `mx`。  
如果 `mn * multiplier > mx`，说明：

- 把 `mn` 乘上 `multiplier` 以后，它会立刻变成**所有数中最大的**。  
- 接下来一次操作会把**第二小的**数乘上 `multiplier`，它同样会变成最大，以此类推。

于是，**从此刻起每一次操作都只会把当前最小的数乘一次，然后把它“踢”到最大的位置**。  
这和把数组看成一个**循环队列**是一样的：  
```
最小 → 乘 → 变成最大 → 放到队尾
```

所以在满足 `mn * multiplier > mx` 以后，后面的操作可以 **按轮回（round‑robin）** 计算：

- 每进行 `n` 次操作，所有 `n` 个元素各被乘一次。  
- 剩余的 `k % n` 次，只需要把当前最小的 `k % n` 个再乘一次。

---

#### 2.2 何时能进入“循环”阶段？

我们可以先 **用堆模拟**，但只模拟到 **第一次出现 `mn * multiplier > mx`** 为止。  
因为每一次乘法都让最小的数变大，**最小值会快速追上最大值**，这一步最多需要 `O(n·log max / log multiplier)` 次，远小于 `k`（`n ≤ 10^4`，`multiplier ≥ 1`）。

---

#### 2.3 具体步骤

1. **准备堆**  
   - 把 `(value, index)` 放进最小堆，记住每个位置的下标，以便最后把答案写回原数组。  
   - 同时维护 `cur_max`（当前最大值），初始时可以直接遍历一次 `nums` 得到。

2. **模拟到进入循环**  
   - 当 `k > 0` 且 `heap[0].value * multiplier <= cur_max` 时，执行一次普通的堆操作（同暴力解）。  
   - 每次乘完后，更新 `cur_max = max(cur_max, new_value)`。  
   - 这一步最多 O(n log n) 次，足够快。

3. **进入循环阶段**（如果还有剩余 `k`）  
   - 此时 `mn * multiplier > cur_max` 已经成立，**后面的每一次乘法都会把最小元素送到最大位置**。  
   - 设 `remain = k`（此时的 `k` 已经是未处理的次数）。  
   - 每个元素都要再乘 `extra = remain // n` 次：`value = value * multiplier^extra`（用快速幂 `pow` 取模）。  
   - 余下的 `rem = remain % n` 次，只对当前最小的 `rem` 个再乘一次。  
   - 为了找这 `rem` 个最小的，我们可以直接 **弹出 `rem` 次堆**，每弹出一次再乘一次并放回堆（`rem < n`，开销可以接受）。

4. **取模并输出**  
   - 所有乘法都已经在取模 `MOD = 10^9+7` 的环境下完成，最后把 `res[idx]` 按下标顺序返回。

---

#### 2.4 核心算法/数据结构的零基础解释  

| 名称 | 类比 | 作用 |
|------|------|------|
| **最小堆（priority queue）** | 像一本随时可以翻到“最前面那一页”的字典，字典里总是把最小的词排在最前面。| 快速得到当前数组的最小元素（`O(1)` 取堆顶）并在 `O(log n)` 时间内把新元素放回。|
| **快速幂 `pow(a, b, MOD)`** | 把“一次乘 `a`”看成“把 `a` 的纸条折叠一次”。折叠 `b` 次可以一次性算出来，而不是逐次相乘。| 计算 `a^b mod MOD`，时间是 `O(log b)`，即使 `b` 很大也很快。|
| **循环（round‑robin）** | 想象有 `n` 个人排队，每次轮到最前面的人做事后，直接站到队尾。| 当最小数乘后一定比所有人都大时，操作就会变成这样循环，每个人被乘的次数只与轮数有关。|

---

#### 代码（Python）

```python
import heapq

MOD = 10 ** 9 + 7

def finalArray(nums, k, multiplier):
    """
    最优解：先用堆模拟到最小数乘后超过最大数的时刻，
    再利用轮转的性质一次性算完剩余的乘法。
    """
    n = len(nums)
    # 结果数组，随时更新对应下标的值（已取模）
    res = list(nums)

    # ---------- 1. 建堆 & 维护当前最大值 ----------
    heap = [(val, idx) for idx, val in enumerate(nums)]
    heapq.heapify(heap)                # O(n)
    cur_max = max(nums)

    # ---------- 2. 逐步模拟，直到进入“循环” ----------
    while k > 0:
        mn, idx = heap[0]               # 直接看堆顶（最小值），O(1)
        # 如果乘一次后仍然 <= 当前最大值，就继续普通模拟
        if mn * multiplier <= cur_max:
            mn, idx = heapq.heappop(heap)   # 弹出最小元素，O(log n)
            mn = mn * multiplier
            res[idx] = mn % MOD             # 更新答案（先取模，后面仍可继续乘）
            heapq.heappush(heap, (mn, idx)) # 放回堆，O(log n)

            # 更新最大值
            if mn > cur_max:
                cur_max = mn
            k -= 1
        else:
            # 已经进入循环阶段，退出模拟
            break

    # ---------- 3. 循环阶段的批量处理 ----------
    if k > 0:   # 仍有未完成的操作
        # 每个元素都再乘 extra 次
        extra = k // n
        if extra:
            mul_extra = pow(multiplier, extra, MOD)   # multiplier^extra % MOD
            # 把堆里每个元素都乘 extra 次
            new_heap = []
            while heap:
                val, idx = heapq.heappop(heap)
                val = (val % MOD) * mul_extra % MOD
                res[idx] = val
                new_heap.append((val, idx))
            heap = new_heap
            heapq.heapify(heap)   # 重新建堆，O(n)

        # 剩余的 rem 次只针对当前最小的 rem 个
        rem = k % n
        for _ in range(rem):
            val, idx = heapq.heappop(heap)   # 取当前最小
            val = (val % MOD) * multiplier % MOD
            res[idx] = val
            heapq.heappush(heap, (val, idx))

    # ---------- 4. 统一取模返回 ----------
    return [x % MOD for x in res]
```

**代码要点说明（中文注释已在代码中）**：

- 第 1 步把原数组放进堆并记录全局最大值 `cur_max`。  
- 第 2 步是**安全的暴力模拟**，但只会进行到“最小数乘一次已经超过最大数”这一步；这一步的次数在最坏情况下也只会是几千次（因为每次乘法都让最小值指数级增长）。  
- 第 3 步利用**轮转**的规律一次性算完剩余的乘法：  
  - `extra = k // n` 表示每个元素还能完整地多乘多少次。  
  - `pow(multiplier, extra, MOD)` 用快速幂一次算出 `multiplier^extra (mod MOD)`，避免循环乘法。  
  - 剩下的 `rem = k % n` 次只需要对当前最小的 `rem` 个再乘一次，用堆直接弹出即可。  
- 第 4 步统一对答案取模，得到题目要求的最终数组。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 初始建堆 `O(n)`。  
  - 模拟到进入循环的过程最多 `O(n log n)`（每次弹出/插入 `log n`，次数受 `log(max)/log(multiplier)` 限制）。  
  - 循环阶段只做一次遍历 `O(n)`（计算 `extra`）和最多 `O(n log n)`（对 `rem < n` 次弹出/插入）。  
  - 与 `k` 的大小无关，适用于 `k` 达到 `10^9` 的极端情况。

- **空间复杂度**：`O(n)`  
  - 需要保存堆、结果数组以及若干临时变量，全部都是与 `n` 成线性关系的。

---

## 心得

- **核心技巧**：**把“每次取最小再乘” 的过程分为两段**——  
  1. 先用堆模拟，等到最小值乘一次就已经大于最大值。  
  2. 进入“循环”阶段后，用 **轮转 + 快速幂** 一次性算完剩余的乘法。  

- **该技巧适用的题型**  
  1. “每次对当前最小/最大元素做相同操作” 且操作会让它们的相对顺序**最终固定**的题目（例如 “K 次最小乘法”）。  
  2. “操作次数极大，需要找规律或周期” 的模拟类题目（如 “数组的循环左移 / 右移” 以及 “乘法循环”）。  

- **一句话总结解题钥匙**：  
  > 当一次操作把最小值直接跳到最大位置时，后面的过程就变成 **轮流乘**，可以用 **批量乘**（快速幂）一次性完成。

---

## 反思

- **第一反应**：直接写一个循环，使用最小堆一步一步模拟。  
- **最容易踩的坑**  
  1. **忘记取模**：乘法会很快溢出 64 位整数，必须在每一步或最终统一取模。  
  2. **循环阶段的判断错误**：必须判断 “`mn * multiplier > cur_max`” **在乘之前**，否则会少算一次或多算一次。  
  3. **边界条件**：`k` 可能本来就已经在进入循环之前就用完，这时不需要进入批量处理；代码要在 `while k>0` 循环后检查 `k` 是否为 0。  

- **下次遇到同类题，第一步该想到**  
  > **先找出“什么时候状态会进入稳定循环”**（比如最小值乘一次就超过最大值），把问题划分为“有限次精细模拟 + 大批量一次性处理”。这样即使 `k` 超大，也能在 `O(n log n)` 内解决。