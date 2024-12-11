# #2970. 统计不可移除子数组的数量 I / Count the Number of Incremovable Subarrays I

> 难度：简单 · 标签：Array、Two Pointers、Binary Search、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-incremovable-subarrays-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers nums.
A subarray of nums is called incremovable if nums becomes strictly increasing on removing the subarray. For example, the subarray [3, 4] is an incremovable subarray of [5, 3, 4, 6, 7] because removing this subarray changes the array [5, 3, 4, 6, 7] to [5, 6, 7] which is strictly increasing.
Return the total number of incremovable subarrays of nums.
Note that an empty array is considered strictly increasing.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 10
Explanation: The 10 incremovable subarrays are: [1], [2], [3], [4], [1,2], [2,3], [3,4], [1,2,3], [2,3,4], and [1,2,3,4], because on removing any one of these subarrays nums becomes strictly increasing. Note that you cannot select an empty subarray.
```

**Example 2:**

```
Input: nums = [6,5,7,8]
Output: 7
Explanation: The 7 incremovable subarrays are: [5], [6], [5,7], [6,5], [5,7,8], [6,5,7] and [6,5,7,8].
It can be shown that there are only 7 incremovable subarrays in nums.
```

**Example 3:**

```
Input: nums = [8,7,6,6]
Output: 3
Explanation: The 3 incremovable subarrays are: [8,7,6], [7,6,6], and [8,7,6,6]. Note that [8,7] is not an incremovable subarray because after removing [8,7] nums becomes [6,6], which is sorted in ascending order but not strictly increasing.
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个下标从 0 开始的正整数数组 `nums`。  
如果在删除某个子数组（subarray）后，`nums` 变为 **严格递增（strictly increasing）**，则该子数组称为 *incremovable* 子数组。例如，子数组 `[3, 4]` 是数组 `[5, 3, 4, 6, 7]` 的 *incremovable* 子数组，因为删除该子数组后数组变为 `[5, 6, 7]`，而 `[5, 6, 7]` 是严格递增的。  

返回 `nums` 中 *incremovable* 子数组的总数。  
注意，**空数组（empty array）** 被视为严格递增。  
子数组是数组中连续的、非空的元素序列。

**示例 1**  
**输入**: `nums = [1,2,3,4]`  
**输出**: `10`  
**解释**: 这 10 个 *incremovable* 子数组为: `[1]`, `[2]`, `[3]`, `[4]`, `[1,2]`, `[2,3]`, `[3,4]`, `[1,2,3]`, `[2,3,4]` 和 `[1,2,3,4]`。删除其中任意一个子数组后，`nums` 都会变为严格递增。注意不能选择空子数组。

**示例 2**  
**输入**: `nums = [6,5,7,8]`  
**输出**: `7`  
**解释**: 这 7 个 *incremovable* 子数组为: `[5]`, `[6]`, `[5,7]`, `[6,5]`, `[5,7,8]`, `[6,5,7]` 和 `[6,5,7,8]`。可以证明 `nums` 中只有这 7 个 *incremovable* 子数组。

**示例 3**  
**输入**: `nums = [8,7,6,6]`  
**输出**: `3`  
**解释**: 这 3 个 *incremovable* 子数组为: `[8,7,6]`, `[7,6,6]` 和 `[8,7,6,6]`。注意 `[8,7]` 不是 *incremovable* 子数组，因为删除 `[8,7]` 后 `nums` 变为 `[6,6]`，虽然是升序排列，但不是严格递增。

**约束条件**  
- `1 <= nums.length <= 50`  
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子数组**，把它们一个个删掉，检查剩下的数组是否严格递增。

- **子数组**：数组里连续的一段，比如 `[2,3,4]` 是 `[1,2,3,4]` 的子数组。  
- **严格递增**：相邻两个数必须满足 `前 < 后`，不能相等。  
- **检查递增**：把子数组 `[l … r]` 删除后，得到的新数组是 `nums[0 … l‑1] + nums[r+1 … n‑1]`。我们只要遍历一次这个新数组，判断每一对相邻数是否满足 `前 < 后` 即可。

因为题目要求 **子数组不能为空**，所以 `l ≤ r` 必须成立。

> **类比**：把数组想成一本书的章节序号。我们要把连续的几页撕掉（子数组），然后看剩下的章节编号是否仍然是递增的。暴力做法就是把所有可能的撕页方式都尝试一次，看看哪种方式撕完后仍然满足递增。

**为什么一定能得到答案**  
暴力枚举不会漏掉任何一种子数组，也不会误判，因为我们对每一种情况都做了完整的递增检查。

**复杂度分析**  
- 枚举子数组有 `O(n²)` 种（`n` 是数组长度）。  
- 对每一种子数组，要遍历剩余的元素检查递增，最坏也只需要 `O(n)`（其实只需遍历一次即可），于是总体是 `O(n³)`。  
- 这里我们可以把检查递增的过程合并到枚举里，使每次检查只走一次剩余数组，得到 **`O(n²)`** 的时间复杂度。  
- 只用了常数级的额外空间，**`O(1)`**。

> **大白话**：  
> - `O(n²)` 就像你在课堂上让 `n` 个学生两两握手，一共要握手 `n × n` 次（但其实只握一次手），所以时间随 `n` 的平方增长。  
> - `O(1)` 表示我们只用了一张纸记下几个指针，不会因为学生人数增多而占用更多内存。

#### 代码（Python）

```python
from typing import List

def count_incremovable_subarrays_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 遍历所有左端点 l
    for l in range(n):
        # 遍历所有右端点 r（保证子数组非空）
        for r in range(l, n):
            # 检查删除 nums[l..r] 后的数组是否严格递增
            prev = None          # 记录前一个保留下来的数
            ok = True

            # 先遍历左侧保留下来的部分
            for i in range(l):
                if prev is not None and not (prev < nums[i]):
                    ok = False
                    break
                prev = nums[i]

            # 再遍历右侧保留下来的部分（如果前面已经失败可以直接跳过）
            if ok:
                for i in range(r + 1, n):
                    if prev is not None and not (prev < nums[i]):
                        ok = False
                        break
                    prev = nums[i]

            if ok:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 两层循环枚举子数组，内部检查递增只遍历一次剩余元素。  
- **空间复杂度**：`O(1)`  
  - 只使用了几个整数指针 `l、r、prev`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“枚举所有子数组”**——`n` 可能达到 50，`n² = 2500` 虽然不大，但在面试里我们仍然想展示更高效的思路。  
我们把注意力放在 **“左侧”和“右侧”各自是否已经是递增的**，以及 **“左侧最后一个数”和“右侧第一个数”之间的关系**。

1. **预处理前缀递增**  
   `pre[i] = True` 表示子数组 `nums[0…i]` 已经严格递增。  
   只要 `pre[i‑1]` 为 `True` 且 `nums[i‑1] < nums[i]`，`pre[i]` 才为 `True`。  
   这相当于把左边 “已经排好序” 的信息存下来，后面查时 O(1)。

2. **预处理后缀递增**  
   `suf[i] = True` 表示子数组 `nums[i…n‑1]` 已经严格递增，方式类似，只是从右往左遍历。

3. **双指针扫描**  
   - 固定左端点 `l`（子数组的左边界）。  
   - 我们想找到 **最小的右端点 `r`**（`r ≥ l`），使得删掉 `nums[l…r]` 后剩余数组递增。  
   - 条件分三部分：
     1. `l == 0` 或者 `pre[l‑1]` 为 `True`（左侧已经递增）。
     2. `r == n‑1` 或者 `suf[r+1]` 为 `True`（右侧已经递增）。
     3. 如果两侧都存在元素，则 `nums[l‑1] < nums[r+1]`（左侧最后一个数必须小于右侧第一个数）。
   - 当 `l` 向右移动时，`r` 永远不会左移（因为左侧变短，只会让条件更容易满足），于是可以 **一次遍历** 完成全部计数，时间 `O(n)`。

4. **计数**  
   对于固定的 `l`，只要找到了最小的合法 `r`，那么 **所有 `r' ≥ r`**（一直删到更右）同样合法，因为右侧的递增前缀只会变短，且 `nums[l‑1] < nums[r'+1]` 仍然成立（`r'+1` 更靠右，数值更大或不存在）。  
   因此本次贡献的子数组数目是 `n - r`（从 `r` 到 `n‑1` 都可以）。把每次的贡献累加即得答案。

> **类比**：  
> 想象你在排队买票，左边已经排好序的队伍是 `pre`，右边已经排好序的队伍是 `suf`。我们想把中间一段人请出去，让剩下的两边仍然保持递增的身高顺序。只要左边最后一个人的身高 < 右边第一个人的身高，就可以把中间的任意连续人请走。双指针就像把两只手分别指向左边和右边，左手往右移动时，右手只需要向右“追赶”，不必回头。

#### 代码（Python）

```python
from typing import List

def count_incremovable_subarrays_opt(nums: List[int]) -> int:
    n = len(nums)

    # 1️⃣ 前缀递增标记
    pre = [False] * n          # pre[i] 为 True 表示 nums[0..i] 严格递增
    pre[0] = True
    for i in range(1, n):
        pre[i] = pre[i - 1] and (nums[i - 1] < nums[i])

    # 2️⃣ 后缀递增标记
    suf = [False] * n          # suf[i] 为 True 表示 nums[i..n-1] 严格递增
    suf[-1] = True
    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] and (nums[i] < nums[i + 1])

    ans = 0
    r = 0                       # 右指针，表示当前找到的最小合法右端点

    # 3️⃣ 枚举左端点 l
    for l in range(n):
        # 保证 r 至少不小于 l（子数组非空）
        if r < l:
            r = l

        # 向右移动 r，直到满足所有条件
        while r < n:
            left_ok = (l == 0) or pre[l - 1]               # 左侧递增
            right_ok = (r == n - 1) or suf[r + 1]          # 右侧递增
            cross_ok = (l == 0) or (r == n - 1) or (nums[l - 1] < nums[r + 1])
            if left_ok and right_ok and cross_ok:
                break          # 已经找到最小的合法 r
            r += 1               # 继续往右找

        # 若 r 超出数组，说明后面已经没有合法子数组
        if r == n:
            break

        # 对当前的 l，所有 r' ≥ r 都合法，贡献 n - r 个子数组
        ans += n - r

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 前缀、后缀各一次遍历 `O(n)`。  
  - 双指针整体只向右移动最多 `n` 步，故总共线性。相比暴力的 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(n)`  
  - 需要两个布尔数组 `pre`、`suf` 各 `n` 长度。若把它们压缩成整数标记，也仍是线性空间。

---

## 心得

- **核心技巧**：利用前缀/后缀递增信息把“是否递增”这件事降到 `O(1)` 查询，再配合双指针一次遍历得到所有合法子数组。
- **适用场景**  
  1. **删除子数组后保持某种单调性**（如本题、LeetCode 1574 “Shortest Subarray to be Removed to Make Array Sorted”）。  
  2. **在数组两端保留递增/递减序列**的计数或判断问题。  
- **一句话总结**：**先把左、右两边的“已经排好序”信息存下来，再用两根指针一次遍历找最左/最右的可删区间**。

---

## 反思

- **第一反应**：直接把所有子数组枚举一遍，写个检查函数，这样能确保正确。  
- **最容易踩的坑**  
  - **空子数组**不计入答案，必须保证 `l ≤ r`。  
  - **边界条件**：当左侧或右侧不存在元素时（`l==0` 或 `r==n-1`），跨界比较 `nums[l-1] < nums[r+1]` 不应执行。  
  - **严格递增** vs **非严格递增**：相等的元素会让子数组失效，注意 `<=` 与 `<` 的区别。  
- **下次类似题**：第一步先**判断两端是否已经满足单调性**（前缀/后缀），然后再思考**如何用指针/二分快速定位满足交叉条件的区间**。这样就能从暴力的 “枚举全部” 跳到线性的 “一次扫描”。