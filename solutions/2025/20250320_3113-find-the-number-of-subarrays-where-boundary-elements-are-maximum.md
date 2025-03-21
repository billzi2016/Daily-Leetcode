# #3113. 找出边界元素为最大值的子数组数量 / Find the Number of Subarrays Where Boundary Elements Are Maximum

> 难度：困难 · 标签：Array、Binary Search、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums.
Return the number of subarrays of nums, where the first and the last elements of the subarray are equal to the largest element in the subarray.

**Examples**

**Example 1:**

```
Input: nums = [1,4,3,3,2]
Output: 6
Explanation:
There are 6 subarrays which have the first and the last elements equal to the largest element of the subarray:
Hence, we return 6.
```

**Example 2:**

```
Input: nums = [3,3,3]
Output: 6
Explanation:
There are 6 subarrays which have the first and the last elements equal to the largest element of the subarray:
Hence, we return 6.
```

**Example 3:**

```
Input: nums = [1]
Output: 1
Explanation:
There is a single subarray of nums which is [ 1 ] , with its largest element 1. The first element is 1 and the last element is also 1.
Hence, we return 1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个正整数数组 `nums`。  
返回 `nums` 中满足以下条件的子数组（subarray）数量：子数组的第一个元素和最后一个元素均等于该子数组中的最大元素。

**示例 1**  
**输入**: `nums = [1,4,3,3,2]`  
**输出**: `6`  
**解释**:  
共有 6 个子数组的首尾元素都等于该子数组的最大元素，满足条件的子数组分别是  
`[4]`, `[4,3]`, `[4,3,3]`, `[4,3,3,2]`, `[3,3]`, `[3,3,2]`。  
因此返回 `6`。

**示例 2**  
**输入**: `nums = [3,3,3]`  
**输出**: `6`  
**解释**:  
所有可能的子数组均满足条件，具体为  
`[3]`, `[3]`, `[3]`, `[3,3]`, `[3,3]`, `[3,3,3]`。  
所以返回 `6`。

**示例 3**  
**输入**: `nums = [1]`  
**输出**: `1`  
**解释**:  
唯一的子数组是 `[1]`，其最大元素为 `1`，首尾元素均为 `1`。  
因此返回 `1`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有 **子数组**（连续的区间）枚举出来，逐个判断：

1. 取出子数组 `nums[l : r+1]`（左闭右闭区间），记录它的最大值 `mx`。  
2. 检查子数组的第一个元素 `nums[l]` 与最后一个元素 `nums[r]` 是否都等于 `mx`。  
3. 如果相等，就把答案加一。

> **数据结构类比**  
> - **数组** 就像我们日常的“一排盒子”，可以随意取出任意连续的一段。  
> - **子数组** 就是从这排盒子里挑出连续的几盒。  
> - **最大值** 好比把这几盒里最高的那件商品挑出来比较。

只要把所有可能的 `(l, r)` 组合遍历完，就一定不会漏掉任何合法子数组，所以这个方法**一定正确**。

#### 代码（Python）

```python
from typing import List

def count_subarrays_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 枚举所有左端点 l
    for l in range(n):
        cur_max = nums[l]               # 当前子数组的最大值，先设为第一个元素
        # 枚举所有右端点 r（r 必须 >= l）
        for r in range(l, n):
            # 更新子数组 [l, r] 的最大值
            cur_max = max(cur_max, nums[r])

            # 检查子数组首尾是否等于最大值
            if nums[l] == cur_max and nums[r] == cur_max:
                ans += 1
    return ans
```

> **关键行中文注释**  
> - `cur_max = max(cur_max, nums[r])`：随右端点扩大，实时维护子数组的最大值。  
> - `if nums[l] == cur_max and nums[r] == cur_max:`：判断首尾是否同时等于最大值。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环遍历 `n` 次，内层循环最坏也会遍历 `n` 次，所以大约要做 `n × n` 次比较。  
  - 对于 `n = 10⁵` 这样的大数据，这种“平方级”算法会非常慢（相当于把 10⁵ 的数字排成 10⁵ 行，每行 10⁵ 列，遍历整个表格）。
- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（`ans、cur_max、l、r`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都要重新遍历子数组来找最大值，这导致了 `O(n²)` 的时间。  
要把时间降到线性（`O(n)`），我们需要 **一次遍历** 就把每个位置能贡献的合法子数组数算出来。核心思路如下：

1. **把问题转化为“以 i 为右端点的合法子数组有多少”。**  
   - 如果我们能快速得到每个 `i` 的答案，所有 `i` 的答案相加就是最终结果。

2. **定位“左边界”**  
   - 对于右端点 `i`，如果左端点 `l` 所在位置的元素 **小于** `nums[i]`，那么 `nums[i]` 就不可能是子数组 `[l, i]` 的最大值（因为左边已经有更大的数了）。  
   - 因此，合法子数组的左端点必须 **在最近的比 `nums[i]` 小的元素的右侧**。记这个最近的更小元素位置为 `prevLess[i]`，则左端点 `l` 必须满足 `l > prevLess[i]`。  

   - **如何快速求 `prevLess[i]`？**  
     使用 **单调递增栈**（Monotonic Stack）。栈里保存 **严格递增** 的元素下标。当我们遍历到 `i` 时，弹出所有 `nums[stack.top] >= nums[i]` 的下标，栈顶（如果还有）就是最近的更小元素。整个过程是 `O(n)` 的。

3. **在合法区间内计数“相同值的出现次数”。**  
   - 子数组 `[l, i]` 要满足首尾都是 **最大值**，而最大值正好是 `nums[i]`（因为左端点不可能有更大的数）。于是左端点 `l` 必须是 **值等于 `nums[i]` 的位置**。  
   - 因此，在区间 `(prevLess[i], i]`（左开右闭）里，所有 **值等于 `nums[i]` 的位置** 都可以作为合法的左端点。  

   - 为了在 **O(1)** 时间内得到这些位置的个数，我们维护一个 **滑动窗口计数器** `cnt[value]`，它记录当前窗口 `[L, i]`（`L = prevLess[i] + 1`）内每个数值出现了多少次。  
     - 当窗口左边界 `L` 向右移动时，删掉离开的元素对应的计数。  
     - 当我们处理位置 `i` 时，`cnt[nums[i]]` 正好是 **在 `[L, i-1]` 中值等于 `nums[i]` 的个数**。  
     - 再加上长度为 1 的子数组 `[i, i]` 本身，一共 `cnt[nums[i]] + 1` 个合法子数组以 `i` 为右端点。

4. **把每个位置的贡献累加** 即得到答案。

> **类比**  
> - **单调栈** 好比“排队的保安”。当一个更高的数字来时，所有比它矮的保安都被“赶走”，剩下的保安正好是递增的，最前面的保安就是最近的更矮的数字。  
> - **滑动窗口计数** 像是“超市收银台”。我们只关心当前正在结账的这批顾客（窗口内），当有人离开（左指针右移），我们把他买的商品数量从统计里减掉。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def count_subarrays_opt(nums: List[int]) -> int:
    n = len(nums)
    # 1️⃣ 先用单调递增栈求每个位置左边最近的更小元素下标
    prev_less = [-1] * n          # 若左侧没有更小元素，记为 -1
    stack = []                    # 栈中保存下标，且对应的值严格递增

    for i, val in enumerate(nums):
        # 弹出所有 >= 当前值的下标，使栈保持严格递增
        while stack and nums[stack[-1]] >= val:
            stack.pop()
        # 此时栈顶（如果存在）就是最近的更小元素
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)           # 当前下标压入栈中

    # 2️⃣ 滑动窗口计数 + 累计答案
    cnt = defaultdict(int)       # 统计窗口内每个数值出现次数
    ans = 0
    left = 0                      # 窗口左端点，随 i 前进而可能跳跃

    for i, val in enumerate(nums):
        # 窗口左端点必须是 prev_less[i] + 1
        new_left = prev_less[i] + 1
        # 把左指针从 old left 移到 new_left，删除离开的元素计数
        while left < new_left:
            cnt[nums[left]] -= 1
            left += 1

        # 此时 cnt[val] 代表在 [new_left, i-1] 中值等于 val 的个数
        ans += cnt[val] + 1      # +1 是长度为 1 的子数组 [i,i]

        # 把当前位置加入窗口，供后续 i 使用
        cnt[val] += 1

    return ans
```

> **关键行中文注释**  
> - `while stack and nums[stack[-1]] >= val:`：弹出所有不比当前值小的元素，保证栈里始终是递增的。  
> - `prev_less[i] = stack[-1] if stack else -1`：记录最近的更小元素位置。  
> - `while left < new_left: cnt[nums[left]] -= 1; left += 1`：滑动窗口左边界向右收缩，实时维护计数。  
> - `ans += cnt[val] + 1`：`cnt[val]` 是之前出现的相同值的个数，加上单元素子数组。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 求 `prev_less` 的单调栈遍历一次，每个下标最多进栈、出栈一次。  
  - 主循环里左指针 `left` 只会整体向右移动 `n` 步，计数字典的增删都是 `O(1)`。  
  - 所以整体是线性时间，远快于暴力的 `O(n²)`。

- **空间复杂度**：`O(n)`  
  - `prev_less`、单调栈、计数字典均可能存储至多 `n` 条信息。  
  - 对于 `n = 10⁵` 完全可以接受。

---

## 心得

- **核心技巧**：**单调栈** + **滑动窗口计数**。  
  - 单调栈帮助我们在一次遍历中找到“左侧最近的更小元素”，从而界定每个右端点的合法左端点范围。  
  - 滑动窗口计数在这个范围内快速统计“值相同出现了多少次”，直接得到以当前元素为右端点的合法子数组数量。

- **适用的题型**（可以套用相同思路）  
  1. **“每个元素左侧最近更大/更小”** 的统计题，如 “Daily Temperatures”、 “Sum of Subarray Minimums”。  
  2. **“子数组的最大/最小值必须出现在子数组两端”** 的计数题，例如本题、或“子数组最大值恰好出现一次”。  
  3. **“在限定区间内计数相同值出现次数”** 的题目，如 “Count Subarrays With Median K”。

- **一句话总结解题钥匙**  
  > 把“以 i 为右端点的合法子数组”拆成 **左边界 = 最近更小元素右侧** 与 **左端点必须是同值位置**，用单调栈锁定左边界，用滑动窗口计数快速求同值个数。

---

## 反思

- **拿到题目第一反应**：先想“枚举所有子数组”，这自然是最直观的暴力思路。  
- **最容易踩的坑**  
  1. **左边界的定义**：必须是“最近的更小元素的右侧”，而不是“最近的更大”。弄错会导致计数错误。  
  2. **窗口收缩时忘记更新计数**：左指针左移后对应的元素计数必须减一，否则会把已经不在窗口里的相同值算进去。  
  3. **单元素子数组**：每个位置本身也是合法子数组，记得在 `cnt[val]` 基础上加 `1`。  

- **下次遇到同类题，第一步该想到**  
  > “先把每个位置的合法左边界用单调栈算出来”，随后再在该区间里做**快速计数**（滑动窗口、哈希计数或二分查找），避免再次出现二次遍历的暴力情况。