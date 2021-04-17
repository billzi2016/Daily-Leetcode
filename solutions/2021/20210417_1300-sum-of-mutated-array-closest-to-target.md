# #1300. 变异数组之和最接近目标 / Sum of Mutated Array Closest to Target

> 难度：中等 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/)

---

## 题目（英文原版）

**Description**

Given an integer array arr and a target value target, return the integer value such that when we change all the integers larger than value in the given array to be equal to value, the sum of the array gets as close as possible (in absolute difference) to target.
In case of a tie, return the minimum such integer.
Notice that the answer is not neccesarilly a number from arr.

**Examples**

**Example 1:**

```
Input: arr = [4,9,3], target = 10
Output: 3
Explanation: When using 3 arr converts to [3, 3, 3] which sums 9 and that's the optimal answer.
```

**Example 2:**

```
Input: arr = [2,3,5], target = 10
Output: 5
```

**Example 3:**

```
Input: arr = [60864,25176,27249,21296,20204], target = 56803
Output: 11361
```

**Constraints**

- 1 <= arr.length <= 104
- 1 <= arr[i], target <= 105

---

## 题目（中文翻译）

给定一个整数数组（integer array）`arr` 和一个目标值 `target`，返回一个整数 `value`，使得将数组中所有大于 `value` 的整数都改为 `value` 后，数组的和与 `target` 的绝对差（absolute difference）尽可能小。  
如果存在多个满足最小差距的 `value`，返回其中最小的整数。  
请注意，答案不一定是数组中的元素。

**示例 1**  
```text
Input: arr = [4,9,3], target = 10
Output: 3
Explanation: 当使用 3 时，arr 变为 [3, 3, 3]，其和为 9，这就是最优答案。
```

**示例 2**  
```text
Input: arr = [2,3,5], target = 10
Output: 5
```

**示例 3**  
```text
Input: arr = [60864,25176,27249,21296,20204], target = 56803
Output: 11361
```

**约束条件**

- `1 <= arr.length <= 10^4`
- `1 <= arr[i], target <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的取值都枚举一遍**，然后算出把数组中比这个取值大的元素全部改成该取值后得到的数组和，看看哪个和最接近 `target`。  

- **数据结构**：只需要普通的 Python 列表。遍历时把每个元素和当前枚举的 `value` 比较，如果大就取 `value`，否则保持原值。可以把这个过程想象成“给每个人发糖”，糖的数量就是 `value`，如果有人本来拥有的糖更多，就把多余的收回，只剩 `value`。  
- **正确性**：因为我们把**所有**可能的 `value`（从 `0` 到数组中最大元素）都试了一遍，必然能找到让和最接近 `target` 的那个 `value`。  
- **时间/空间复杂度**：  
  - 假设数组最大元素是 `M`，我们要枚举 `0 … M` 共 `M+1` 种取值。对每一种取值，都要遍历整个数组（长度 `n`），所以总共要做 `O(M·n)` 次基本操作。  
  - 这里的 `O(M·n)` 可以想象成“如果最大糖数是 1000，人数是 100，那么我们要做 100 000 次加法”。  
  - 只用到常数级的额外空间 `O(1)`（只保存几个计数器）。

#### 代码（Python）

```python
def findBestValue_bruteforce(arr, target):
    # 1. 先算出数组的最大值，决定枚举的上界
    max_val = max(arr)

    best_val = 0          # 当前找到的最优取值
    best_diff = float('inf')   # 最小的绝对差

    # 2. 枚举所有可能的 value
    for value in range(max_val + 1):
        cur_sum = 0
        # 3. 计算把大于 value 的元素都改成 value 后的数组和
        for num in arr:
            cur_sum += min(num, value)   # 如果 num > value，用 value 替代

        diff = abs(cur_sum - target)      # 与目标的距离
        # 4. 更新最优解（若距离相等，取更小的 value）
        if diff < best_diff or (diff == best_diff and value < best_val):
            best_diff = diff
            best_val = value

    return best_val
```

#### 复杂度  

- **时间复杂度**：`O(M·n)`  
  - `M` 是数组中最大的元素。比如 `M=10⁵、n=10⁴` 时，最坏会有 `10⁹` 次循环，明显超时。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历整个数组**，而我们其实可以利用数学性质把计算 `sum(min(ai, x))` 的过程加速。

1. **观察单调性**  
   把函数 `f(x) = Σ min(ai, x)` 写出来会发现：  
   - 当 `x` 增大时，`min(ai, x)` 只会变大或保持不变，永远不会变小。  
   - 因此 `f(x)` 是一个 **单调不减** 的函数。  
   - 想象把 `x` 当作横坐标，`|f(x) - target|` 当作纵坐标，你会得到一条先下降后上升的“U”形曲线（**单峰**），最底部对应的 `x` 就是答案。

2. **把数组排序 + 前缀和**  
   - 把数组从小到大排序后，前面的元素一定会全部 **小于等于** 某个阈值 `x`，后面的元素则可能被裁剪为 `x`。  
   - 设 `arr` 已排序，`pref[i]` 为前 `i` 个元素的和（**前缀和**）。  
   - 对于任意 `x`，我们可以二分定位第一个大于 `x` 的位置 `idx`（类似在字典里查单词的首字母）。  
   - 那么  
     ```
     f(x) = pref[idx]               # 前 idx 个元素保持原样
          + (n - idx) * x           # 剩下的每个都被裁成 x
     ```
   - 这一步只需要 `O(log n)` 的时间（二分查找），而不是 `O(n)`。

3. **二分搜索最接近 target 的阈值**  
   - 因为 `f(x)` 单调递增，我们可以在 `[0, max(arr)]` 之间做二分搜索，找到**最左侧**的 `x` 使得 `f(x) >= target`。  
   - 设这个 `x` 为 `hi`，`lo = hi - 1`（若 `hi` 为 0，则 `lo = 0`）。这两个相邻的候选值必定把 `f` 分别压在 target 的左右两侧。  
   - 最后比较 `|f(lo) - target|` 与 `|f(hi) - target|`，取距离更小的那个；若相等返回较小的 `x`（即 `lo`）。

4. **为什么二分能工作**  
   - `f(x)` 单调递增 ⇒ `f(x) - target` 也是单调递增。  
   - 所以寻找 “第一个非负” 的位置恰好可以用二分。

> **类比**：把 `x` 想成水位，`arr` 是一排容器的高度。把容器里超过水位的水倒掉后，总水量就是 `f(x)`。水位升高，总水量只会不减。我们想让水量最接近目标 `target`，于是二分找最合适的水位。

#### 代码（Python）

```python
from bisect import bisect_right
from itertools import accumulate

def findBestValue(arr, target):
    """
    返回使得将所有大于 value 的元素都替换为 value 后的数组和
    与 target 的绝对差最小的 value（若有多个则返回最小的）。
    """
    n = len(arr)
    arr.sort()                               # 1. 排序，方便二分定位
    pref = [0] + list(accumulate(arr))       # 2. 前缀和，pref[i] = 前 i 个元素之和

    max_val = arr[-1]

    # --------- 辅助函数：计算 f(x) = Σ min(ai, x) ----------
    def calc(x: int) -> int:
        # idx = 第一个 > x 的位置（右侧插入点），等价于 bisect_right
        idx = bisect_right(arr, x)           # O(log n)
        # 前 idx 个保持原样，后面的都被裁成 x
        return pref[idx] + (n - idx) * x

    # --------- 二分搜索最左侧的 f(x) >= target ----------
    lo, hi = 0, max_val
    while lo < hi:
        mid = (lo + hi) // 2
        if calc(mid) < target:
            lo = mid + 1
        else:
            hi = mid

    # 此时 lo == hi 为第一个使得 sum >= target 的阈值
    cand_high = lo
    cand_low = max(0, cand_high - 1)          # 防止 lo 为 0 时出现负数

    # 计算两者的距离，选更好的
    diff_low = abs(calc(cand_low) - target)
    diff_high = abs(calc(cand_high) - target)

    if diff_low <= diff_high:                # 若相等返回更小的 value
        return cand_low
    else:
        return cand_high
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`（占主导）。  
  - 二分搜索的循环次数是 `log(max_val)`（最多约 17 次，因为 `max_val ≤ 10⁵`），每次调用 `calc` 里又有一次二分 `O(log n)`，整体仍然是 `O(log max_val · log n)`，远小于 `n log n`。  
  - 与暴力解的 `O(M·n)` 相比，提升了 **几个数量级**，即使 `n = 10⁴、M = 10⁵` 也能在毫秒级完成。

- **空间复杂度**：`O(n)`  
  - 需要额外存储排序后的数组和前缀和，各占 `n` 长度。  
  - 这比暴力解的 `O(1)` 多一点，但在本题的约束下（`n ≤ 10⁴`）完全可以接受。

---

## 心得

- **核心技巧**：利用 **单调性 + 二分搜索**，配合 **排序 + 前缀和** 快速求出 `Σ min(ai, x)`。  
- **适用场景**：  
  1. “把数组元素上限/下限限制后求和” 类问题（如 LeetCode 1300. **Sum of Mutated Array Closest to Target**）。  
  2. “给定阈值，统计满足某种条件的元素数量或和” 的查询（如 “找第 K 大的元素” 的二分变体）。  
  3. “单调函数求最接近目标值的自变量” （例如在**容量/费用**之间做平衡的二分）。  
- **一句话总结**：**先把问题转化为单调函数，再用二分定位最接近目标的阈值**，配合前缀和实现 O(1) 级的函数值计算。

---

## 反思

- **第一反应**：直接遍历所有可能的 `value`，写个双层循环，最直接但会超时。  
- **最容易踩的坑**：  
  - 忘记 `value` 可能不在原数组中，需要在 `[0, max(arr)]` 的完整区间搜索。  
  - 计算 `f(x)` 时若直接遍历数组会导致 `O(n·log(max))` 超时，必须用二分 + 前缀和把单次计算降到 `O(log n)`。  
  - 边界情况：当所有元素都小于目标 `target` 时，最优 `value` 可能是 `max(arr)`；当 `target` 极小，答案可能是 `0`（因为题目未限制 `value` 必须为正）。  
- **下次思路**：看到“把数组中大于某个阈值的元素都改成阈值”这类描述，立刻想到 **排序 + 前缀和** 能把 “对每个阈值求和” 变成 `O(log n)`，随后检查函数是否单调，从而使用二分或三分搜索定位最优阈值。