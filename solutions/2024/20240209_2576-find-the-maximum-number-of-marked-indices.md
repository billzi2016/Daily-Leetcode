# #2576. 找到标记下标的最大数量 / Find the Maximum Number of Marked Indices

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-number-of-marked-indices/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
Initially, all of the indices are unmarked. You are allowed to make this operation any number of times:
Return the maximum possible number of marked indices in nums using the above operation any number of times.

**Examples**

**Example 1:**

```
Input: nums = [3,5,2,4]
Output: 2
Explanation: In the first operation: pick i = 2 and j = 1, the operation is allowed because 2 * nums[2] <= nums[1]. Then mark index 2 and 1.
It can be shown that there's no other valid operation so the answer is 2.
```

**Example 2:**

```
Input: nums = [9,2,5,4]
Output: 4
Explanation: In the first operation: pick i = 3 and j = 0, the operation is allowed because 2 * nums[3] <= nums[0]. Then mark index 3 and 0.
In the second operation: pick i = 1 and j = 2, the operation is allowed because 2 * nums[1] <= nums[2]. Then mark index 1 and 2.
Since there is no other operation, the answer is 4.
```

**Example 3:**

```
Input: nums = [7,6,8]
Output: 0
Explanation: There is no valid operation to do, so the answer is 0.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个 **0 基**（0-indexed）的整数数组 `nums`。最初，所有下标（index）均未标记。你可以任意次数执行以下 **操作（operation）**：

1. 选择两个 **未标记** 的不同下标 `i` 和 `j`，使得 `2 * nums[i] <= nums[j]` 成立；
2. 将下标 `i` 和 `j` 都标记为已标记。

返回在可以无限次执行上述 **操作** 的情况下，数组 `nums` 中最多可以标记的下标数量。

---

### 示例

#### 示例 1  
**输入**  
```json
nums = [3,5,2,4]
```  
**输出**  
```
2
```  
**解释**  
第一次操作：选择 `i = 2`（`nums[2] = 2`）和 `j = 1`（`nums[1] = 5`），因为 `2 * nums[2] <= nums[1]` 成立。随后将下标 `2` 与 `1` 标记。可以证明不存在其他合法的操作，故答案为 `2`。

#### 示例 2  
**输入**  
```json
nums = [9,2,5,4]
```  
**输出**  
```
4
```  
**解释**  
第一次操作：选择 `i = 3`（`nums[3] = 4`）和 `j = 0`（`nums[0] = 9`），因为 `2 * nums[3] <= nums[0]` 成立，标记下标 `3` 与 `0`。  
第二次操作：选择 `i = 1`（`nums[1] = 2`）和 `j = 2`（`nums[2] = 5`），因为 `2 * nums[1] <= nums[2]` 成立，标记下标 `1` 与 `2`。  
此后已经没有可行的操作，答案为 `4`。

#### 示例 3  
**输入**  
```json
nums = [7,6,8]
```  
**输出**  
```
0
```  
**解释**  
不存在满足条件的操作，故答案为 `0`。

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每一次合法的操作都枚举出来**，只要满足  
`2 * nums[i] ≤ nums[j] (i ≠ j)`  
就把这两个下标标记（记作已使用），然后继续在剩下的下标中寻找下一对。  

可以把数组看成一堆“牌”，每次要找两张牌满足“左边的点数乘 2 不超过右边的点数”。  
暴力做法就是把所有牌两两比较，一旦找到一对就把它们从牌堆里剔除，继续比较。  

这种方法一定能得到合法的操作序列，因为我们没有遗漏任何可能的配对；  
但是它并不一定得到**最大**的标记数，因为我们随意挑选的第一对可能会把后面更有价值的配对“抢走”。  

#### 代码（Python）

```python
def max_marked_bruteforce(nums):
    n = len(nums)
    used = [False] * n          # 标记哪些下标已经被配对
    cnt = 0                     # 已标记的下标个数

    # 暴力枚举所有可能的 (i, j) 组合，顺序随意
    for i in range(n):
        if used[i]:
            continue
        for j in range(n):
            if i == j or used[j]:
                continue
            if 2 * nums[i] <= nums[j]:   # 满足题目条件
                used[i] = used[j] = True
                cnt += 2                 # 一次操作标记两个下标
                break                    # 跳出内层，去找下一个 i
    return cnt
```

> **关键行中文注释**  
> - `used` 用来模拟“这张牌已经被取走”。  
> - 两层 `for` 循环把所有 `(i, j)` 组合都检查一遍，最坏情况是 `n·(n‑1)` 次比较。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  > “平方”意味着如果数组有 10 000 个元素，算法大概要做 100 000 000 次比较，随元素增多非常快变慢。  
- **空间复杂度**：`O(n)`  
  > 只用了一个和原数组等长的布尔数组 `used` 来记录标记情况。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于我们一次只看一对 `(i, j)`，并且随意挑选配对顺序。  
实际上，要想标记最多的下标，**配对策略本身必须是最优的**。  

观察条件 `2 * nums[i] ≤ nums[j]`，左边的数要尽可能小，右边的数要尽可能大，才能更容易满足不等式。  
这就引导我们想到 **先把数组从小到大排好序**，然后把“小的”配给“大的”。  

> **为什么要用最小的 k 个数和最大的 k 个数？**  
> 假设我们想完成 `k` 次操作（即标记 `2k` 个下标）。  
> - 若我们不使用最小的 `k` 个数中的某个数 `x`，而是用一个更大的数 `y`（`y ≥ x`），  
>   那么配对时左侧的数只会更大，满足 `2*y ≤ …` 的难度不降反升，**不会比使用 `x` 更好**。  
> - 同理，若我们不使用最大的 `k` 个数中的某个数 `z`，而是用一个更小的数 `w`（`w ≤ z`），  
>   右侧的数变小，同样会让不等式更难成立。  

所以，**若存在一种方式能完成 `k` 次操作，那么一定可以用最小的 `k` 个数配对最大的 `k` 个数来完成**。  

配对方式的细节：  
- 把最小的 `k` 个数从左到右记为 `small[0] … small[k‑1]`（已经排好序）。  
- 把最大的 `k` 个数从右到左记为 `big[0] … big[k‑1]`（即 `big[0]` 是第 `k` 大的数，`big[k‑1]` 是最大数）。  
- 为了让每一对都尽可能满足 `2 * small[i] ≤ big[i]`，**把 `small[i]` 与 `big[i]` 配对**（即最小的配最小的“大”，第二小的配第二小的“大”，依次类推）。  

于是检查某个 `k` 是否可行，只要遍历 `i = 0 … k‑1` 看是否都有 `2 * small[i] ≤ big[i]` 即可。  

因为 `k` 的取值范围是 `[0, n//2]`，我们可以 **二分搜索** 出最大的可行 `k`。  

整体步骤  

1. 对 `nums` 进行升序排序。  
2. 设左指针 `l = 0`（指向最小的数），右指针 `r = n // 2`（指向中间），二分搜索 `k`。  
3. 对每个中间值 `mid`（尝试的操作次数），取前 `mid` 个最小数 `nums[0:mid]` 与后 `mid` 个最大数 `nums[n-mid:]`，逐一比较  
   `2 * nums[i] ≤ nums[n-mid+i]`。  
   - 若全部成立，说明 `mid` 次操作可以完成，尝试更大的 `mid`（`l = mid + 1`）。  
   - 否则 `mid` 太大，尝试更小的 `mid`（`r = mid - 1`）。  
4. 最终得到的最大 `k` 即为答案的 **标记下标数 = 2 * k**。  

#### 代码（Python）

```python
def max_marked(nums):
    """
    返回能够标记的最大下标个数（即 2 * 最大可完成的操作次数）
    """
    n = len(nums)
    nums.sort()                     # 先排序，O(n log n)

    # 二分搜索能够完成的最大 k（操作次数）
    left, right = 0, n // 2          # 最多只能配对 n//2 对
    best = 0

    while left <= right:
        mid = (left + right) // 2    # 试图完成 mid 次操作
        ok = True

        # 检查最小的 mid 个数和最大的 mid 个数是否都能配对成功
        for i in range(mid):
            if 2 * nums[i] > nums[n - mid + i]:
                ok = False          # 只要有一对不满足，就说明 mid 太大
                break

        if ok:                       # mid 可行，尝试更大
            best = mid
            left = mid + 1
        else:                        # mid 不可行，缩小范围
            right = mid - 1

    return 2 * best                  # 每次操作标记两个下标
```

> **关键行中文注释**  
> - `nums.sort()`：把数组想象成排好序的牌堆，最小的在左，最大的在右。  
> - `n // 2`：最多只能配对一半的元素，因为每次需要两个人。  
> - `for i in range(mid):`：把左边第 `i` 小的牌和右边第 `i` 大的牌配对，检查 `2 * 小 ≤ 大`。  
> - `2 * best`：每完成一次合法配对，就标记两个下标。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)` 是主导成本。  
  - 二分搜索的循环最多 `log₂(n/2)` 次，每次检查至多 `mid ≤ n/2` 条配对，整体仍然是 `O(n log n)`。  
  - 与暴力的 `O(n²)` 相比，**即使 n = 10⁵ 也能在毫秒级跑完**。  

- **空间复杂度**：`O(1)`（不计排序时使用的原地排序）  
  - 只用了常数个额外变量 `left, right, mid, ok, best`，没有额外的数组。  

---

## 心得  

- **核心技巧**：**先排序 + 二分答案 + 直接配对检查**。  
- 这种“把最小的配给最大的” 的配对思想常出现在需要比较大小关系的贪心/二分题目中。  
- 类似题型（可以套用同样思路）  
  1. *Maximum Number of Pairs With Absolute Difference At Most K*（配对差值限制）  
  2. *Find the Longest Subsequence Such That Its Sum Is Divisible by K*（利用前缀和的二分）  
  3. *Maximum Number of Events That Can Be Attended*（按结束时间排序的贪心）  

- **一句话总结解题钥匙**：  
  > “把问题转化为‘能否在 k 次配对下全部满足条件’，然后二分搜索最大可行的 k”。  

---

## 反思  

- **第一反应**：看到 “2 * nums[i] ≤ nums[j]”，立刻想到把小的乘 2 与大的比较，于是想到排序后两端配对。  
- **最容易踩的坑**  
  1. **忘记每次配对都要标记两个下标**，直接返回 `k` 而不是 `2*k`。  
  2. **二分搜索的区间写错**：上界应该是 `n // 2`（因为每次需要两个人），否则会出现数组越界。  
  3. **配对顺序错误**：必须把第 `i` 小的数配第 `i` 大的数（而不是最小配最大、次小配次大），否则会漏掉可行配对。  
- **下次遇到同类题**：  
  1. 先判断“是否可以把问题抽象为‘在 k 次操作下全部满足某个单调判定条件’”。  
  2. 若是，立刻考虑 **二分答案** + **排序后两端配对**（或前缀/后缀技巧）来实现判定函数。