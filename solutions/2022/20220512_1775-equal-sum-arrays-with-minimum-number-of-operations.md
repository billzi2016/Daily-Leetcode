# #1775. 最小操作次数使两数组和相等 / Equal Sum Arrays With Minimum Number of Operations

> 难度：中等 · 标签：Array、Hash Table、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/equal-sum-arrays-with-minimum-number-of-operations/)

---

## 题目（英文原版）

**Description**

You are given two arrays of integers nums1 and nums2, possibly of different lengths. The values in the arrays are between 1 and 6, inclusive.
In one operation, you can change any integer's value in any of the arrays to any value between 1 and 6, inclusive.
Return the minimum number of operations required to make the sum of values in nums1 equal to the sum of values in nums2. Return -1​​​​​ if it is not possible to make the sum of the two arrays equal.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3,4,5,6], nums2 = [1,1,2,2,2,2]
Output: 3
Explanation: You can make the sums of nums1 and nums2 equal with 3 operations. All indices are 0-indexed.
- Change nums2[0] to 6. nums1 = [1,2,3,4,5,6], nums2 = [6,1,2,2,2,2].
- Change nums1[5] to 1. nums1 = [1,2,3,4,5,1], nums2 = [6,1,2,2,2,2].
- Change nums1[2] to 2. nums1 = [1,2,2,4,5,1], nums2 = [6,1,2,2,2,2].
```

**Example 2:**

```
Input: nums1 = [1,1,1,1,1,1,1], nums2 = [6]
Output: -1
Explanation: There is no way to decrease the sum of nums1 or to increase the sum of nums2 to make them equal.
```

**Example 3:**

```
Input: nums1 = [6,6], nums2 = [1]
Output: 3
Explanation: You can make the sums of nums1 and nums2 equal with 3 operations. All indices are 0-indexed. 
- Change nums1[0] to 2. nums1 = [2,6], nums2 = [1].
- Change nums1[1] to 2. nums1 = [2,2], nums2 = [1].
- Change nums2[0] to 4. nums1 = [2,2], nums2 = [4].
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 1 <= nums1[i], nums2[i] <= 6

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`（array），它们的长度可能不同，数组中的元素值均在 1 到 6（含）之间。  
在一次操作（operation）中，你可以将任意一个数组中的任意整数的值更改为 1 到 6（含）之间的任意值。  
返回使 `nums1` 的所有元素之和等于 `nums2` 的所有元素之和所需的最小操作次数。如果无法使两个数组的和相等，返回 `-1`。

**示例 1**  
**输入**: `nums1 = [1,2,3,4,5,6]`, `nums2 = [1,1,2,2,2,2]`  
**输出**: `3`  
**解释**: 只需 3 次操作即可使两数组的和相等（下标均为 0 起始）。  
- 将 `nums2[0]` 改为 6。此时 `nums1 = [1,2,3,4,5,6]`, `nums2 = [6,1,2,2,2,2]`。  
- 将 `nums1[5]` 改为 1。此时 `nums1 = [1,2,3,4,5,1]`, `nums2 = [6,1,2,2,2,2]`。  
- 将 `nums1[2]` 改为 2。此时 `nums1 = [1,2,2,4,5,1]`, `nums2 = [6,1,2,2,2,2]`。

**示例 2**  
**输入**: `nums1 = [1,1,1,1,1,1,1]`, `nums2 = [6]`  
**输出**: `-1`  
**解释**: 无法通过降低 `nums1` 的和或提升 `nums2` 的和来使两者相等。

**示例 3**  
**输入**: `nums1 = [6,6]`, `nums2 = [1]`  
**输出**: `3`  
**解释**: 只需 3 次操作即可使两数组的和相等（下标均为 0 起始）。  
- 将 `nums1[0]` 改为 2。此时 `nums1 = [2,6]`, `nums2 = [1]`。  
- 将 `nums1[1]` 改为 2。此时 `nums1 = [2,2]`, `nums2 = [1]`。  
- 将 `nums2[0]` 改为 4。此时 `nums1 = [2,2]`, `nums2 = [4]`。

**约束条件**  
- `1 <= nums1.length, nums2.length <= 10^5`  
- `1 <= nums1[i], nums2[i] <= 6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的修改方式**，直到两个数组的和相等。  
具体可以这样做：

1. 先算出 `sum1 = sum(nums1)`、`sum2 = sum(nums2)`。  
2. 若 `sum1 == sum2`，直接返回 `0`。  
3. 否则我们把两个数组合并成一个大列表 `all = nums1 + nums2`，每一次在 `all` 中挑选一个元素，把它改成 `1~6` 中的任意值，然后重新计算两个数组的和，判断是否相等。  
4. 把所有可能的改动次数从 `1`、`2`、`3` … 逐层 BFS（广度优先搜索），第一个找到相等的层数就是答案。

**数据结构类比**：  
- 把每一次“把一个数改成别的数”看成在一张巨大的**状态图**里走一步。  
- BFS 就像在城市的地图上层层展开，离起点最近的地方先探索。

**为什么能得到正确答案**：  
因为 BFS 会遍历所有 **最少步数** 的可能性，先到达的就是最小操作次数。

**时间/空间复杂度**：  
- 每一步我们都要遍历所有元素并尝试 6 种新值，最坏情况下会产生指数级的状态数。  
- 对长度为 `n`、`m`（均 ≤ 10⁵）的数组，暴力搜索根本不可行。  
- 用大白话说，时间复杂度大约是 `O(6^{(n+m)})`，几乎等同于 **无限大**，空间也会随状态数爆炸。

#### 代码（Python）

```python
from collections import deque

def min_operations_bruteforce(nums1, nums2):
    sum1, sum2 = sum(nums1), sum(nums2)
    if sum1 == sum2:
        return 0

    # 把两个数组拼成一个列表，记住每个位置属于哪边
    all_nums = nums1 + nums2
    belong = [1] * len(nums1) + [2] * len(nums2)   # 1 表示在 nums1，2 表示在 nums2

    # BFS：状态 = (当前和差 diff, 已经改动的次数, 当前数组)
    start = (sum1 - sum2, 0, tuple(all_nums))
    q = deque([start])
    visited = {start[2]}          # 防止重复状态

    while q:
        diff, steps, cur = q.popleft()
        if diff == 0:                     # 两边和相等
            return steps
        # 尝试把每个位置改成 1~6 的任意值
        for i, val in enumerate(cur):
            for new_val in range(1, 7):
                if new_val == val:
                    continue
                # 计算新的 diff
                if belong[i] == 1:   # 改动的是 nums1
                    new_diff = diff - (new_val - val)
                else:                # 改动的是 nums2
                    new_diff = diff + (new_val - val)
                new_state = list(cur)
                new_state[i] = new_val
                new_state_t = tuple(new_state)
                if new_state_t not in visited:
                    visited.add(new_state_t)
                    q.append((new_diff, steps + 1, new_state_t))
    return -1
```

> **注意**：上面的代码仅用于说明思路，实际运行会在几秒钟内因状态爆炸而超时或内存爆炸。

#### 复杂度  

- **时间复杂度**：`O(6^{(n+m)})`（指数级），因为每一步都有 6 种可能，且会遍历所有元素。  
- **空间复杂度**：`O(6^{(n+m)})`，需要保存所有已经访问过的状态。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**每次都枚举所有元素的所有新值**。  
实际上，我们只需要关心 **每一次操作能让差距（两个数组的和之差）最大程度地缩小**，而不必真的去尝试所有具体的数值。

**关键观察**  

1. 设 `sum1 > sum2`（若相反，直接把两数组调换角色）。我们只能**减小 `sum1`** 或**增大 `sum2`**，因为只要让差距变小就行。  
2. 对于 `nums1` 中的一个元素 `x`，它能**降低** `sum1` 的最大幅度是 `x - 1`（把它改成最小的 1）。  
   对于 `nums2` 中的一个元素 `y`，它能**提升** `sum2` 的最大幅度是 `6 - y`（把它改成最大的 6）。  
3. 每一次操作的“贡献”就是上面两种可能中的 **最大值**。我们希望每一步都选出 **贡献最大的** 元素来操作——**贪心**。  

**为什么贪心是对的**  

- 每一步我们都尽可能把差距削减最多。假设有两步操作 A、B，若把贡献大的先做，差距会更快变为 0；把贡献小的先做，只会让后面的操作需要更多次数。  
- 这类似“把硬币面值从大到小找零”，先用面值大的硬币可以最少硬币数得到目标金额。  

**实现细节**  

1. 计算 `diff = abs(sum1 - sum2)`，如果 `diff == 0` 直接返回 `0`。  
2. 统计两个数组中**每种“单次最大贡献”**出现的次数。因为数值只在 `[1,6]`，贡献只能是 `0~5`（`6-1`）。  
   - 对 `nums1`（假设 `sum1 > sum2`），贡献 `c = x - 1`，`c` 的取值范围是 `0~5`。  
   - 对 `nums2`，贡献 `c = 6 - y`，同样 `0~5`。  
   用一个长度为 `6` 的数组 `cnt[0..5]` 累计每种贡献的出现次数。  
3. 从最大的贡献 `5` 开始，尽可能多地使用这些贡献来抵消 `diff`：  
   - `need = diff // contribution`（向下取整）是仅用这种贡献可以完全覆盖的次数。  
   - 实际可用次数是 `min(need, cnt[contribution])`。  
   - 用完后更新 `diff -= used * contribution`，并累计操作次数 `ops += used`。  
   - 若 `diff` 仍然大于 `0`，继续用下一小的贡献。  
4. 最后如果 `diff > 0`，说明即使把所有元素都改成极端值仍然不足以平衡，两数组长度差距导致不可达，返回 `-1`。  
5. 否则返回累计的 `ops`。

**为什么只需要计数**  

- 题目限制数值在 `1~6`，所以每个元素的最大贡献只有 `5` 种可能（`1~5`），用计数数组即可在 **O(n+m)** 时间统计完毕。  
- 这避免了使用堆或平衡树的 `log` 开销，直接线性遍历即可。

#### 代码（Python）

```python
def min_operations(nums1, nums2):
    """
    贪心 + 计数实现
    """
    sum1, sum2 = sum(nums1), sum(nums2)
    # 已经相等
    if sum1 == sum2:
        return 0

    # 保证 sum1 为较大的那个，这样统一思考「减小 sum1」或「增大 sum2」
    if sum1 < sum2:
        nums1, nums2 = nums2, nums1   # 交换
        sum1, sum2 = sum2, sum1

    diff = sum1 - sum2                 # 需要消除的差距（正数）

    # cnt[i] 表示「一次操作能改变 i 的差距」的元素个数，i 范围 0~5
    cnt = [0] * 6

    # 对较大的数组（现在是 nums1）统计「把元素变成 1」能减少的量
    for x in nums1:
        cnt[x - 1] += 1                # 最大可减小的幅度 = x-1

    # 对较小的数组（现在是 nums2）统计「把元素变成 6」能增加的量
    for y in nums2:
        cnt[6 - y] += 1                # 最大可增加的幅度 = 6-y

    ops = 0
    # 从最大贡献 5 开始往下尝试
    for change in range(5, 0, -1):      # 0 的贡献没有意义，直接跳过
        if diff <= 0:                  # 已经消除完差距
            break
        if cnt[change] == 0:
            continue
        # 需要多少次这种贡献才能把 diff 消完（向上取整）
        need = (diff + change - 1) // change
        use = min(need, cnt[change])
        diff -= use * change
        ops += use

    # 如果 diff 仍然大于 0，说明所有元素都已经调到极端仍不足
    return -1 if diff > 0 else ops
```

> **代码说明**  
> - 第 1–9 行：先把 `sum1` 设为较大的和，统一后面的计算。  
> - 第 12–18 行：`cnt[i]` 统计每个元素**一次操作能带来的最大差距改变**。  
> - 第 21–30 行：从最大的可能改变（5）往下使用，尽量一次削减最多的 `diff`。  
> - 第 33 行：若所有贡献用完仍有剩余，返回 `-1`。

#### 复杂度  

- **时间复杂度**：`O(n + m)`（线性遍历两数组一次，再遍历常数长度的 `cnt`），即使数组长达 `10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(1)`，只用了固定大小的计数数组 `cnt[6]`，与输入规模无关。

---

## 心得

- **核心技巧**：**贪心 + 计数**。先把差距最大的“可改动幅度”一次性使用，保证最少操作次数。  
- **适用的题型**  
  1. “最小操作次数使数组和相等”类（如本题、LeetCode 1775）。  
  2. “把数组元素改成目标范围内的任意值”类（如把数组变为全 0、或使两数组差值 ≤ k）。  
  3. “使用最少硬币凑齐金额”这类 **最大贡献优先** 的问题。  
- **一句话总结解题钥匙**：**把每一步的“收益”最大化，就能最少步数达成目标**。

---

## 反思

- **第一反应**：看到 “可以把任意数改成 1~6”，立刻想到把大的数变小、把小的数变大，随后尝试 BFS 暴力搜索。  
- **最容易踩的坑**  
  - 忽略了数组长度差导致的不可达情况（例如 `nums1` 长度远大于 `nums2`，即使全部调到极端也无法平衡）。  
  - 没有把 `sum1` 与 `sum2` 先做大小排序，导致后续代码要分两种情况写两遍。  
  - 在贪心实现时忘记对 `change = 0`（没有贡献）直接跳过，会导致死循环。  
- **下次遇到同类题**：  
  1. 先算出两数组的和差 `diff`，确认是“增大小的、减小大的”。  
  2. 统计每个元素**一次操作能带来的最大改变**，用计数或优先队列。  
  3. 从最大改变开始逐步消除 `diff`，若用尽所有改变仍未抵消，直接返回 `-1`。