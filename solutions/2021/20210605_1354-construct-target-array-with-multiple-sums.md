# #1354. 构造目标数组的多次求和 / Construct Target Array With Multiple Sums

> 难度：困难 · 标签：Array、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/construct-target-array-with-multiple-sums/)

---

## 题目（英文原版）

**Description**

You are given an array target of n integers. From a starting array arr consisting of n 1's, you may perform the following procedure :
Return true if it is possible to construct the target array from arr, otherwise, return false.

**Examples**

**Example 1:**

```
Input: target = [9,3,5]
Output: true
Explanation: Start with arr = [1, 1, 1] 
[1, 1, 1], sum = 3 choose index 1
[1, 3, 1], sum = 5 choose index 2
[1, 3, 5], sum = 9 choose index 0
[9, 3, 5] Done
```

**Example 2:**

```
Input: target = [1,1,1,2]
Output: false
Explanation: Impossible to create target array from [1,1,1,1].
```

**Example 3:**

```
Input: target = [8,5]
Output: true
```

**Constraints**

- n == target.length
- 1 <= n <= 5 * 104
- 1 <= target[i] <= 109

---

## 题目（中文翻译）

你得到一个包含 **n** 个整数的数组 `target`。从一个全部由 **1** 组成的初始数组 `arr`（长度为 **n**）出发，你可以反复执行以下操作：

- 计算当前数组 `arr` 的所有元素之和 `sum`。
- 选择任意下标 `i`，将 `arr[i]` 替换为 `sum`。

如果能够通过若干次上述操作将 `arr` 变为 `target`，返回 `true`；否则返回 `false`。

---

### 示例

**示例 1**

```
Input: target = [9,3,5]
Output: true
Explanation: 
从 arr = [1, 1, 1] 开始
[1, 1, 1]，sum = 3，选择下标 1
[1, 3, 1]，sum = 5，选择下标 2
[1, 3, 5]，sum = 9，选择下标 0
得到 [9, 3, 5]，完成
```

**示例 2**

```
Input: target = [1,1,1,2]
Output: false
Explanation: 无法从 [1,1,1,1] 构造出目标数组。
```

**示例 3**

```
Input: target = [8,5]
Output: true
```

---

### 约束条件

- `n == target.length`
- `1 <= n <= 5 * 10^4`
- `1 <= target[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**正向模拟**：  
- 从初始数组 `arr = [1, 1, …, 1]`（长度 `n`）出发。  
- 每一步遍历所有下标 `i`，把当前数组的 **总和** 加到 `arr[i]` 上，得到新的数组。  
- 重复上述过程，直到数组恰好等于 `target`，或者出现了无法再匹配的情况。  

这里用到的唯一数据结构就是普通的 **列表**（Python 中的 `list`），它就像一排排盒子，盒子里装的是数字。  
- “遍历所有下标”就像把手伸进每个盒子，检查或修改里面的东西。  

**为什么会对？**  
因为题目说每一次只能把 **当前所有元素的和** 加到某一个位置上，而我们正是把所有可能的加法路径都尝试一遍，所以如果真的能得到 `target`，必定会在某一步出现完全相同的数组。

**时间/空间复杂度**  
- **时间复杂度**：设数组长度为 `n`，目标数组的最大值为 `M`（`M ≤ 10⁹`）。每一次加法都会让某个元素至少增长 `1`，而总和从 `n`（全是 1）增长到 `sum(target)`。最坏情况下，需要 **`O(sum(target))`** 次操作，而 `sum(target)` 可能是 `n·M`，即 **`O(n·M)`**。这在实际数据（`n ≤ 5·10⁴, M ≤ 10⁹`）下根本不可接受。  
- **空间复杂度**：只用了原数组和若干临时变量，**`O(n)`**（保存当前数组的空间）。  

> 大白话：`O(n·M)` 就像说我们要走 **n** 条路，每条路上要走 **M** 步，步数多到天荒地老，根本走不完。

#### 代码（Python）  

```python
def isPossible_bruteforce(target):
    n = len(target)
    arr = [1] * n                 # 初始全是 1
    total = n                     # 当前数组的总和

    # 为了避免死循环，设置一个上限（实际根本跑不完）
    max_steps = sum(target) * 2  

    for _ in range(max_steps):
        if arr == target:         # 已经和目标一样，成功
            return True
        # 尝试把 total 加到每一个位置，看能否一步到位
        for i in range(n):
            new_arr = arr.copy()
            new_arr[i] += total   # 把当前总和加到第 i 位
            if all(new_arr[j] <= target[j] for j in range(n)):
                # 只保留不超过目标的状态继续搜索
                arr = new_arr
                total = sum(arr)
                break
    return False                  # 超出步数上限仍未匹配，视为不可能
```

> 这段代码仅用于说明暴力思路，**在实际测试会超时**。

#### 复杂度  

- **时间复杂度**：`O(n·M)`（极其庞大，几乎不可能在 1 秒内跑完）。  
- **空间复杂度**：`O(n)`（保存当前数组的空间）。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出：**正向模拟太慢**，因为每一步都要遍历所有元素并且总和不断增大。  
我们需要 **倒着想**——从 `target` 逆向回到全是 `1` 的初始数组。

**关键观察**  

1. **总和只会增大**  
   - 每一次操作是把当前数组的总和 `S` 加到某个位置 `i`，于是新的总和变成 `S + S = 2S`。  
   - 因此 **从前往后** 总和是单调递增的。  

2. **最大元素一定是最后一步产生的**  
   - 在一次操作里，只有被选中的位置会变大，而它会变成 “原来的值 + 之前的总和”。  
   - 所以在 `target` 中最大的那个数，一定是 **上一次** 操作后得到的。  

3. **逆向恢复**  
   - 设当前数组为 `target`，总和为 `total = sum(target)`。  
   - 取出最大的元素 `mx`（用最大堆或直接遍历），记 `rest = total - mx` 为除它之外的其他元素之和。  
   - 在上一步，这个 `mx` 是 **`previous_value + rest`**，而 `previous_value` 必须是 **正数**（至少是 `1`）。  
   - 所以 **`previous_value = mx % rest`**（因为可能在同一个位置多次被加上 `rest`）。  
   - 把 `mx` 替换成 `previous_value`，更新总和 `total = previous_value + rest`，继续循环。  

4. **特殊情况**  
   - 当数组长度为 `1` 时，只要 `target[0] == 1` 就可以，否则不可能。  
   - 当 `rest == 1` 时，`previous_value` 必然是 `1`（因为任何数减去若干个 `1` 最终会变成 `1`），此时直接返回 `True`。  

**为什么要用最大堆（Priority Queue）**  
- 每一步我们都需要 **最快** 找到当前最大的元素。  
- 堆是一种专门用来 **快速取最大（或最小）** 的数据结构，取最大只需要 `O(log n)`，而普通遍历则是 `O(n)`。  
- 类比：堆就像一个 **“随时可以拿到最高分的学生名单”**，不必每次都把所有学生的成绩都重新排一遍。

**算法步骤**  

1. 把 `target` 放进 **最大堆**（Python 用 `heapq` 实现最小堆，取负数转为最大堆）。  
2. 计算总和 `total = sum(target)`。  
3. 循环：  
   - 取出堆顶最大值 `mx`。  
   - 计算 `rest = total - mx`。  
   - 如果 `mx == 1` 或 `rest == 1`，返回 `True`（已经可以回到全 1）。  
   - 如果 `rest == 0` 或 `mx < rest`，返回 `False`（不可能）。  
   - 计算 `prev = mx % rest`（如果 `prev == 0`，说明上一轮应该是 `rest`，但 `rest` 为 0 时已在上一步排除）。  
   - 如果 `prev == 0`，说明 `mx` 正好是 `rest` 的倍数，但 `prev` 必须至少是 `1`，否则返回 `False`。  
   - 把 `prev` 放回堆中，更新 `total = prev + rest`。  
4. 循环结束时若堆中全是 `1`，返回 `True`。  

#### 代码（Python）  

```python
import heapq

def isPossible(target):
    """
    判断能否从全 1 的数组通过题目规定的操作得到 target
    """
    if len(target) == 1:               # 只有一个元素时，只有 target[0]==1 才可能
        return target[0] == 1

    # Python 的 heapq 是最小堆，取负数实现最大堆
    max_heap = [-x for x in target]    # 负数越小，原数越大
    heapq.heapify(max_heap)            # O(n) 建堆
    total = sum(target)                # 当前数组的总和

    while True:
        mx = -heapq.heappop(max_heap)   # 取出最大值，恢复正数
        rest = total - mx               # 其余元素的和

        # 1. 已经全部恢复成 1
        if mx == 1 or rest == 1:
            return True

        # 2. 不可能的情况
        if rest == 0 or mx < rest:     # mx 必须大于 rest，且 rest 不能为 0
            return False

        # 3. 计算上一步该位置的真实值
        prev = mx % rest                # 取模得到“之前的值”
        if prev == 0:                   # 如果恰好整除，说明上一轮该位置应该是 rest
            prev = rest

        # 4. 若 prev 仍然不合法，直接失败
        if prev == mx:                  # 没有变化，说明卡死在循环
            return False

        # 5. 把恢复后的值放回堆，更新总和
        heapq.heappush(max_heap, -prev)
        total = prev + rest             # 新的总和

```

> 关键注释已用中文标明每一步的意义，代码可以直接复制运行。

#### 复杂度  

- **时间复杂度**：`O( n log n * log(max(target)) )`  
  - 每一次循环我们弹出/插入堆的代价是 `O(log n)`。  
  - 循环次数大致等于 **每个元素被“削减”到 1 的次数**，最多是 `log_{2}(max(target))`（因为每次至少会把最大值减小到它的 **模**，相当于除以至少 2 的数量级）。  
  - 因此整体是 `O(n log n * log max)`，在题目限制下（`n ≤ 5·10⁴, max ≤ 10⁹`）完全可接受。  

- **空间复杂度**：`O(n)`  
  - 需要保存堆和几个整数，和原数组大小同阶。  

> 与暴力解相比，时间从天文数字的 `O(n·M)` 降到了几乎线性的 `O(n log n)`，快得多。

---

## 心得  

- **核心技巧**：**逆向思考 + 最大堆**。先从目标倒着“减”，把每一步的最大元素恢复成它之前的样子。  
- **适用的题型**  
  1. “从初始状态逐步扩大” → 需要逆向回到初始状态的题目（如 “把数组变成全 1”）。  
  2. “每一步都把整体信息（总和、最小值）加到某个位置” → 典型的 **Priority Queue** 应用。  
  3. “需要频繁取最大/最小并更新” → 如 “K 次取最大元素的和”、 “有序数组的动态更新”。  
- **一句话总结解题钥匙**：  
  > **“把最大的那一步逆向拆回去，用堆把最大值快速找出来”**。  

---

## 反思  

- **第一反应**：直接正向模拟，想一步步把 `1` 加大到目标。  
- **最容易踩的坑**  
  - 忽略 **`rest == 1`** 的特殊情况，导致循环卡在大数上。  
  - `mx % rest` 为 `0` 时没有正确处理，应该把它视作 `rest`（因为上一步可能正好是 `rest` 本身）。  
  - 当数组长度为 `1` 时忘记单独判断。  
- **下次遇到同类题**，第一步应该问自己：  
  > “这一步的操作是把整体信息（比如总和）加到某个位置吗？如果是，能不能从目标倒着把它‘减’回去？”  

这样就能快速定位到 **逆向 + 堆** 的思路，避免盲目正向暴力搜索。