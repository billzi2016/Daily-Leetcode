# #1674. 使数组互补的最少操作次数 / Minimum Moves to Make Array Complementary

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-make-array-complementary/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of even length n and an integer limit. In one move, you can replace any integer from nums with another integer between 1 and limit, inclusive.
The array nums is complementary if for all indices i (0-indexed), nums[i] + nums[n - 1 - i] equals the same number. For example, the array [1,2,3,4] is complementary because for all indices i, nums[i] + nums[n - 1 - i] = 5.
Return the minimum number of moves required to make nums complementary.

**Examples**

**Example 1:**

```
Input: nums = [1,2,4,3], limit = 4
Output: 1
Explanation: In 1 move, you can change nums to [1,2,2,3] (underlined elements are changed).
nums[0] + nums[3] = 1 + 3 = 4.
nums[1] + nums[2] = 2 + 2 = 4.
nums[2] + nums[1] = 2 + 2 = 4.
nums[3] + nums[0] = 3 + 1 = 4.
Therefore, nums[i] + nums[n-1-i] = 4 for every i, so nums is complementary.
```

**Example 2:**

```
Input: nums = [1,2,2,1], limit = 2
Output: 2
Explanation: In 2 moves, you can change nums to [2,2,2,2]. You cannot change any number to 3 since 3 > limit.
```

**Example 3:**

```
Input: nums = [1,2,1,2], limit = 2
Output: 0
Explanation: nums is already complementary.
```

**Constraints**

- n == nums.length
- 2 <= n <= 105
- 1 <= nums[i] <= limit <= 105
- n is even.

---

## 题目（中文翻译）

给定一个长度为偶数 `n` 的整数数组 `nums` 和一个整数 `limit`。一次操作（move）指将 `nums` 中的任意一个整数替换为 `[1, limit]` 区间内的任意整数（包含端点）。

如果对于所有下标 `i`（0 起始），都有  

`nums[i] + nums[n - 1 - i]`  

等于同一个数，则称数组 `nums` 为 **互补**（complementary）。例如数组 `[1,2,3,4]` 是互补的，因为对所有下标 `i`，都有 `nums[i] + nums[n - 1 - i] = 5`。

返回使 `nums` 变为互补所需的最少操作次数。

## 示例

### 示例 1
**输入**  
`nums = [1,2,4,3], limit = 4`  

**输出**  
`1`  

**解释**  
只需一次操作即可将 `nums` 改为 `[1,2,2,3]`（下划线部分为被修改的元素）。  

- `nums[0] + nums[3] = 1 + 3 = 4`  
- `nums[1] + nums[2] = 2 + 2 = 4`  
- `nums[2] + nums[1] = 2 + 2 = 4`  
- `nums[3] + nums[0] = 3 + 1 = 4`  

因此对于每个 `i`，`nums[i] + nums[n-1-i] = 4`，`nums` 为互补数组。

### 示例 2
**输入**  
`nums = [1,2,2,1], limit = 2`  

**输出**  
`2`  

**解释**  
通过两次操作可以将 `nums` 改为 `[2,2,2,2]`。由于 `limit = 2`，无法将任何元素改为 `3`（因为 `3 > limit`）。

### 示例 3
**输入**  
`nums = [1,2,1,2], limit = 2`  

**输出**  
`0`  

**解释**  
`nums` 已经是互补的，无需任何操作。

## 约束条件

- `n == nums.length`
- `2 <= n <= 10^5`
- `1 <= nums[i] <= limit <= 10^5`
- `n` 为偶数

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把数组 `nums` 变成「互补」的：  
对于每个下标 `i`，都有 `nums[i] + nums[n-1-i]` **等于同一个数**（记作 `target`）。  
最直接的想法是：

1. 枚举所有可能的 `target`（合法的和范围是 `2 … 2*limit`，因为每个数最小是 `1`，最大是 `limit`）。  
2. 对每一对 `(i, n-1-i)`，分别判断要把它们的和变成 `target` 需要 **0、1 或 2 次** 替换。  
   - 如果当前和已经等于 `target`，不需要操作。  
   - 否则看能否只改动一个数使和等于 `target`（只要 `target - other` 落在 `[1, limit]`）。  
   - 否则只能改动两个数。  
3. 把所有对的操作次数加起来，取最小值。

**数据结构**：只需要遍历数组，用普通的 `list` 保存每对的值。  
可以把「查字典」的过程想象成：我们要把每对的「当前和」对应到「需要的改动次数」，这一步就像在字典里查找键值一样。

**为什么正确**：我们穷举了所有合法的 `target`，并且对每个 `target` 都精确计算了最少的改动次数，最终取最小值自然就是答案。

**复杂度**：  
- 外层遍历所有可能的 `target`，数量是 `2*limit-1`，约为 `O(limit)`。  
- 内层遍历数组的前半段（因为每对只算一次），数量是 `n/2`，即 `O(n)`。  
- 因此总时间是 `O(limit * n)`，在最坏情况下 `limit` 和 `n` 都可达 `10^5`，会产生 `10^10` 次操作，明显超时。  
- 空间只用了常数级的几个变量，`O(1)`。

#### 代码（Python）

```python
from typing import List

def minMoves_bruteforce(nums: List[int], limit: int) -> int:
    n = len(nums)
    # 所有可能的目标和，从 2 到 2*limit（因为每个数最小 1，最大 limit）
    best = float('inf')
    for target in range(2, 2 * limit + 1):
        moves = 0
        # 只遍历前半段，每对只算一次
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            cur_sum = a + b
            if cur_sum == target:                 # 已经等于 target，0 次操作
                continue
            # 看能否只改动一个数，使和等于 target
            # 改动 a：需要 new_a = target - b，检查 new_a 是否在合法范围 [1, limit]
            # 改动 b：需要 new_b = target - a，同理
            if 1 <= target - a <= limit or 1 <= target - b <= limit:
                moves += 1                        # 只需要 1 次操作
            else:
                moves += 2                        # 必须改动两个数
        best = min(best, moves)
    return best
```

#### 复杂度

- **时间复杂度**：`O(limit * n)`。  
  - `limit` 代表「目标和的种类」，`n` 代表「数组长度的一半」。  
  - 想象成「先挑 10 万种口味，再对每种口味检查 5 万个人」，显然太慢。

- **空间复杂度**：`O(1)`。  
  - 只用了几个计数器，没有额外的数组或哈希表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每个可能的 target 都重新遍历所有对**。  
我们需要把「每对对不同 target 的影响」一次性统计出来，随后再快速求出每个 target 的总改动次数。

关键观察：

1. 对于一对 `(a, b)`（`a = nums[i]`，`b = nums[n-1-i]`），
   - 若我们把目标和 `target` 设为 `a + b`，只需要 **0** 次改动。
   - 若 `target` 落在区间 `[min(a, b) + 1, max(a, b) + limit]`，只需要 **1** 次改动。  
     解释：只改动较小的那个数，使它变成 `target - larger`（只要在 `[1, limit]` 范围），或者只改动较大的那个数，使它变成 `target - smaller`。这两个区间合并正好是上述范围。
   - 其他所有 `target`（即 `< min(a,b)+1` 或 `> max(a,b)+limit`）需要 **2** 次改动。

2. 把「需要 2 次改动」视为基线（所有 target 默认都要 2 次），然后用**差分数组（difference array）**记录「从 2 次降到 1 次」和「从 1 次降到 0 次」的区间。

   - 对每对 `(a,b)`：
     - `sum_ab = a + b` → 这一个点的改动次数要减 2（从 2 次降到 0 次）。
     - 区间 `[low, high] = [min(a,b)+1, max(a,b)+limit]` → 对这整个区间的改动次数要再减 1（从 2 次降到 1 次）。
   - 用差分数组 `diff`（长度 `2*limit + 2`）来累计这些「-1」或「-2」的操作。最后对 `diff` 做前缀和，即可得到每个 `target` 对应的「总改动次数」。

3. 实现细节（一步步推导）：

   - 初始化 `diff` 为全 `0`。我们把「所有 target 默认需要 2 次」这一步放在后面：最终答案 = `2 * (n/2) + prefix_sum[target]`，因为每对默认 2 次，总共 `n/2` 对。
   - 对每对：
     1. `sum_ab = a + b`  
        - `diff[sum_ab] -= 2`（在 `sum_ab` 位置减 2，后面的前缀和会把它加进去）。
        - `diff[sum_ab + 1] += 2`（在下一个位置恢复回去，形成「只在 sum_ab 这一个点」的区间）。
     2. `low = min(a, b) + 1`  
        `high = max(a, b) + limit`  
        - `diff[low] -= 1`（从 low 开始减 1）  
        - `diff[high + 1] += 1`（在 high 之后恢复）。
   - 完成所有对后，对 `diff` 进行一次前缀和，得到 `change[target]`（相对 2 次的偏移）。  
     实际的改动次数 = `2 * pairs + change[target]`。

4. 最后遍历所有合法的 `target`（`2 … 2*limit`），取最小的改动次数即为答案。

**核心算法**：差分数组 + 前缀和。  
- 差分数组可以把「在区间 [L,R] 内整体加（或减）一个值」的操作压缩成 **O(1)** 的两次更新。  
- 前缀和把这些局部更新「展开」成每个位置的真实值。

**类比**：想象你在一本笔记本的每一页写下「这页需要额外的改动次数」。如果你要把第 `L` 到第 `R` 页的数都减 1，你只需要在第 `L` 页写「-1」，在第 `R+1` 页写「+1」来「抵消」后面的影响，最后把所有页的数累加起来就得到每页的实际值。

#### 代码（Python）

```python
from typing import List

def minMoves(nums: List[int], limit: int) -> int:
    n = len(nums)
    pairs = n // 2                      # 需要考虑的配对数量
    max_sum = 2 * limit                 # 目标和的最大可能值
    # diff 长度比 max_sum 多 2，防止在 high+1 越界
    diff = [0] * (max_sum + 2)

    for i in range(pairs):
        a, b = nums[i], nums[n - 1 - i]
        low = min(a, b) + 1                 # 只需要 1 次改动的左边界
        high = max(a, b) + limit            # 只需要 1 次改动的右边界
        s = a + b                           # 只需要 0 次改动的目标和

        # 区间 [low, high] 里每个 target 只需要 1 次改动（比默认的 2 次少 1）
        diff[low] -= 1
        diff[high + 1] += 1

        # 只在 s 这一个点上，改动次数还能再少 1（从 1 次降到 0 次），
        # 因此整体上再减 1（相当于在 s 位置再减 1）
        diff[s] -= 1
        diff[s + 1] += 1

    # 前缀和得到每个 target 的「相对于 2 次的偏移」
    best = float('inf')
    cur = 0
    for target in range(2, max_sum + 1):
        cur += diff[target]          # 累计到当前 target
        moves = cur + 2 * pairs      # 基础 2 次 * 对数 + 累计的偏移
        best = min(best, moves)

    return best
```

**代码要点解释**：

- `pairs = n // 2`：因为数组长度是偶数，只需要处理前半段，每个元素都有唯一的「镜像」伙伴。
- `diff[low] -= 1` / `diff[high + 1] += 1`：在区间 `[low, high]` 内把默认的 2 次改动降为 1 次（即「减 1」），使用差分实现 O(1) 更新。
- `diff[s] -= 1` / `diff[s + 1] += 1`：在恰好等于当前和 `s` 的位置，再把改动次数从 1 次降到 0 次（再「减 1」），同样用差分。
- `cur += diff[target]`：遍历所有可能的目标和时，实时维护前缀和，即当前 `target` 的累计偏移。
- `moves = cur + 2 * pairs`：`2 * pairs` 是所有对默认需要的 2 次改动，加上累计的「减」的次数，就是实际需要的最少改动数。

#### 复杂度

- **时间复杂度**：`O(n + limit)`  
  - 遍历数组一次得到所有差分更新：`O(n)`。  
  - 再遍历所有可能的目标和（`2 … 2*limit`）一次，做前缀和并取最小值：`O(limit)`。  
  - 与暴力解的 `O(limit * n)` 相比，省掉了乘法，实际只是线性两次遍历，能够轻松通过 10⁵ 规模的数据。

- **空间复杂度**：`O(limit)`  
  - 额外使用了一个长度约为 `2*limit` 的差分数组。  
  - 这相当于「存一张 2*limit 长的记事本」，在本题的约束下（limit ≤ 10⁵）完全可接受。

---

## 心得

- **核心技巧**：利用差分数组把「每对对所有可能 target 的改动次数」一次性统计，再通过前缀和快速得到每个 target 的总改动数。  
- **适用题型**  
  1. 「最小操作使数组满足某种和/差约束」——如 *“Minimum Moves to Make Array Complementary”*（本题）。  
  2. 「区间加减」类题目——如 *“Difference Array”*、*“Range Addition”*（LeetCode 370）。  
  3. 「前缀和 + 区间统计」——如 *“Maximum Number of Points Inside a Square”*（LeetCode 1478）等。  
- **一句话总结**：**把每对的“0/1/2 次改动”转化为区间增减，用差分数组一次遍历完成所有目标和的统计**。

---

## 反思

- **第一反应**：直接枚举所有可能的目标和，然后对每对独立计算改动次数——这就是暴力思路。  
- **最容易踩的坑**  
  - **边界**：`target` 的合法范围是 `[2, 2*limit]`，别忘了把 `limit` 本身也算进去。  
  - **差分数组越界**：在对 `high+1` 做 `+1` 更新时，需要保证数组长度足够（常加 2）。  
  - **整数溢出**：虽然 Python 没有整型溢出，但在其他语言需要注意 `2*limit` 可能超过 32 位整数范围。  
- **下次遇到同类题**：先思考「每个局部（如每对）对所有全局候选值的影响是否可以用区间表示」，如果可以，就立刻考虑差分数组或前缀和来“一次性”累计。这样往往能把原本的 `O(N·M)` 降到 `O(N+M)`。