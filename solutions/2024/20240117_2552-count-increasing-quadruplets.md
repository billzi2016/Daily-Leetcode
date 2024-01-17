# #2552. 计数递增四元组 / Count Increasing Quadruplets

> 难度：困难 · 标签：Array、Dynamic Programming、Binary Indexed Tree、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-increasing-quadruplets/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums of size n containing all numbers from 1 to n, return the number of increasing quadruplets.
A quadruplet (i, j, k, l) is increasing if:

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,4,5]
Output: 2
Explanation: 
- When i = 0, j = 1, k = 2, and l = 3, nums[i] < nums[k] < nums[j] < nums[l].
- When i = 0, j = 1, k = 2, and l = 4, nums[i] < nums[k] < nums[j] < nums[l]. 
There are no other quadruplets, so we return 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 0
Explanation: There exists only one quadruplet with i = 0, j = 1, k = 2, l = 3, but since nums[j] < nums[k], we return 0.
```

**Constraints**

- 4 <= nums.length <= 4000
- 1 <= nums[i] <= nums.length
- All the integers of nums are unique. nums is a permutation.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`，且其中恰好包含从 `1` 到 `n` 的所有整数（即 `nums` 是一个全排列），请返回满足以下条件的递增四元组的数量。

四元组 `(i, j, k, l)` 若满足下列全部条件则称为递增四元组：  

- `0 ≤ i < j < k < l < n`  
- `nums[i] < nums[k] < nums[j] < nums[l]`

**示例**  

> 示例 1  
> ```text
> 输入: nums = [1,3,2,4,5]
> 输出: 2
> 解释:
> - 当 i = 0, j = 1, k = 2, l = 3 时，满足 nums[i] < nums[k] < nums[j] < nums[l]。  
> - 当 i = 0, j = 1, k = 2, l = 4 时，满足 nums[i] < nums[k] < nums[j] < nums[l]。  
> 除此之外不存在其他满足条件的四元组，故返回 2。
> ```
> 示例 2  
> ```text
> 输入: nums = [1,2,3,4]
> 输出: 0
> 解释: 唯一可能的四元组为 i = 0, j = 1, k = 2, l = 3，但此时 nums[j] < nums[k]，不满足递增条件，所以返回 0。
> ```

**约束条件**  

- `4 <= nums.length <= 4000`  
- `1 <= nums[i] <= nums.length`  
- `nums` 中的所有整数互不相同，`nums` 是一个排列。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求找所有满足  

```
i < j < k < l
nums[i] < nums[k] < nums[j] < nums[l]
```

的四元组。  
最直接的想法就是把四个下标全部枚举一遍：  

1. 用四层循环，分别遍历 `i、j、k、l`（注意要保持下标顺序 `i<j<k<l`）。  
2. 每找到一组下标，就检查对应的四个数是否满足递增关系。  

> **数据结构类比**  
> 这里其实只需要数组本身，不需要额外的数据结构。可以把四层循环想象成“在一条直线上挑四个人”，逐个检查他们的身高是否满足 **小‑中‑大‑更大** 的顺序。

只要把所有可能的四元组都检查一遍，就一定不会漏掉答案，正确性显而易见。  

#### 代码（Python）  

```python
def countIncreasingQuadruplets(nums):
    n = len(nums)
    ans = 0
    # 四层循环，枚举所有 i < j < k < l
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            for k in range(j + 1, n - 1):
                # 先检查 nums[i] < nums[k] < nums[j] 的中间关系
                if not (nums[i] < nums[k] < nums[j]):
                    continue          # 若不满足，后面的 l 也不可能成立
                for l in range(k + 1, n):
                    # 最后检查 nums[j] < nums[l]
                    if nums[j] < nums[l]:
                        ans += 1
    return ans
```

> **关键行注释**  
> - 第 4‑7 行：四层循环确保下标顺序 `i < j < k < l`。  
> - 第 9 行：提前筛掉不满足 `nums[i] < nums[k] < nums[j]` 的中间两层，省一点点时间。  
> - 第 12 行：只有当 `nums[j] < nums[l]` 时，才算一个合法四元组。

#### 复杂度  

- **时间复杂度**：`O(n⁴)`  
  四层循环，每层最多遍历 `n` 次，乘起来就是 `n⁴`。  
  这里的 `O(n⁴)` 可以想象成“把 n 本书排成 4 行，每行都要选一本”，组合数会非常大。  

- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量（计数器 `ans`），不随 `n` 增长。

> 对于 `n ≤ 4000`，`n⁴` 的操作数已经是 **数万亿** 级别，根本跑不完，必须寻找更快的办法。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于四层循环**。  
我们需要把枚举的层数压到 **两层**，其余的计数通过**前缀/后缀统计**一次性得到。  

观察不等式  

```
i < j < k < l
nums[i] < nums[k] < nums[j] < nums[l]
```

如果我们 **先固定中间的两个下标 `j` 与 `k`**（满足 `j < k`），  
那么剩下的 `i` 与 `l` 完全独立：

* `i` 必须在 `j` 的左侧，且 `nums[i] < nums[k]`。  
  → 只要知道在位置 `j` 左边，有多少个数 **小于 `nums[k]`**，记为 `leftLess`.

* `l` 必须在 `k` 的右侧，且 `nums[l] > nums[j]`。  
  → 只要知道在位置 `k` 右边，有多少个数 **大于 `nums[j]`**，记为 `rightGreater`.

对于这一次固定的 `(j, k)`，合法四元组的数量就是  

```
leftLess  *  rightGreater
```

因为任意一个符合条件的 `i` 可以和任意一个符合条件的 `l` 配对。  

所以整体思路是：

1. **遍历所有可能的 `j`（从左到右）**。  
2. 对每个 `j`，准备两张表：  
   - `leftPrefix[v]`：在 `j` 左侧，值 ≤ `v` 的元素个数（相当于前缀和）。  
   - `rightSuffix[pos]`：在某个位置 `pos` 右侧，值 > `nums[j]` 的元素个数（后缀统计）。  
3. 再遍历 `k`（`j+1 … n-2`），利用上面的两张表直接得到  
   `leftLess = leftPrefix[ nums[k] - 1 ]`（比 `nums[k]` 小的数）  
   `rightGreater = rightSuffix[ k+1 ]`（在 `k` 右边比 `nums[j]` 大的数）  
   把乘积加到答案中。

> **核心数据结构解释**  
> - **前缀计数数组** `leftPrefix`：想象把左边的数字排成一本字典，`leftPrefix[x]` 就是“字典里第 `x` 页之前（含第 `x` 页）有多少单词”。查询“比某个值小的元素有多少”只需要一次数组下标访问，时间是 `O(1)`。  
> - **后缀计数数组** `rightSuffix`：把右边的数字倒着排，同理可以一次遍历得到“从当前位置往右，有多少个数大于 `nums[j]`”。  

因为 `nums` 是 **1 … n 的全排列**，值的范围正好是 `1 … n`，可以直接用大小为 `n+1` 的数组来存前缀计数，避免使用哈希表或平衡树。

#### 代码（Python）  

```python
def countIncreasingQuadruplets(nums):
    """
    O(n^2) 时间、O(n) 额外空间
    """
    n = len(nums)
    ans = 0

    # left_cnt[v] 表示当前 j 左侧，值等于 v 的出现次数（0/1，因为是排列）
    left_cnt = [0] * (n + 1)          # 只需要 O(n) 的空间
    # left_prefix[v] = sum_{t <= v} left_cnt[t]
    left_prefix = [0] * (n + 1)

    # j 从左到右遍历（最左的 j 必须留出 i、k、l 四个位置）
    for j in range(1, n - 2):
        # -------------------------------------------------
        # 1）更新左侧计数（把 nums[j-1] 加入左侧）
        v = nums[j - 1]
        left_cnt[v] = 1                # 这一次循环结束后，v 已经在左侧
        # 重新构造前缀和（因为 n ≤ 4000，O(n) 重建是可以接受的）
        cur = 0
        for x in range(1, n + 1):
            cur += left_cnt[x]
            left_prefix[x] = cur
        # -------------------------------------------------
        # 2）构造右侧 “大于 nums[j]” 的后缀计数
        # right_gt[pos] = 在位置 pos（含）之后，值 > nums[j] 的个数
        right_gt = [0] * n
        cnt = 0
        for pos in range(n - 1, j, -1):          # 从最右向左扫到 j+1
            if nums[pos] > nums[j]:
                cnt += 1
            right_gt[pos] = cnt                 # pos 右侧（含 pos）的符合条件的数量
        # -------------------------------------------------
        # 3）枚举 k 并累加答案
        for k in range(j + 1, n - 1):
            # 左侧满足 nums[i] < nums[k] 的 i 个数
            left_less = left_prefix[nums[k] - 1]    # 前缀和查询，O(1)
            # 右侧满足 nums[l] > nums[j] 的 l 个数
            right_greater = right_gt[k + 1]         # 后缀查询，O(1)
            ans += left_less * right_greater
        # -------------------------------------------------
    return ans
```

> **关键行中文注释**  
> - 第 9‑11 行：`left_cnt` 记录当前 `j` 左边已经出现过的数字（因为是排列，只会出现一次）。  
> - 第 13‑17 行：把 `left_cnt` 转换成前缀和 `left_prefix`，以后查询“比某个值小的元素有多少”只需要一次数组下标。  
> - 第 22‑27 行：从右向左遍历，累计 **大于 `nums[j]`** 的元素个数，得到 `right_gt[pos]`。  
> - 第 31‑35 行：固定 `j` 与 `k`，利用前缀/后缀表直接得到 `left_less` 与 `right_greater`，乘积即为该 `(j,k)` 对贡献的四元组数。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历所有可能的 `j`（约 `n` 次）。  
  - 对每个 `j`：  
    * 重建左侧前缀和需要 `O(n)`（`n` ≤ 4000，完全可接受）。  
    * 右侧后缀扫描同样是 `O(n)`。  
    * 再遍历所有 `k`（最多 `n` 次）并在 `O(1)` 内完成计数。  
  - 综合下来是 `≈ 3 * n * n = O(n²)`。  
  - 对比暴力的 `O(n⁴)`，`n = 4000` 时 `n² ≈ 1.6×10⁷`，可以在一秒左右跑完。  

- **空间复杂度**：`O(n)`  
  - 只用了几张长度为 `n+1` 的数组（`left_cnt`, `left_prefix`, `right_gt`），随 `n` 线性增长。  
  - 没有使用递归或额外的二维矩阵，内存占用非常小。

> **与暴力解对比**：  
> - 暴力解每多一层循环，就把时间指数级提升一次；  
> - 最优解把两层循环压到 `O(n²)`，并且每一次计数都是 `O(1)`，实现了“把四个人的选法拆成两段独立计数，再相乘”的思路。

---  

## 心得  

- **核心技巧**：**固定中间两位，利用前缀/后缀计数把剩余两位的选择转化为乘法**。  
- **适用题型**：  
  1. “计数四元组/三元组”且下标有顺序限制的题目（如 *Count Special Quadruplets*）。  
  2. 需要在数组中找满足 **a < c < b < d** 之类不完全递增关系的组合。  
  3. 任何可以把整体拆成 “左侧/右侧” 两块独立统计的排列计数问题。  
- **一句话总结解题钥匙**：**先固定中间的关键位置，用一次前缀统计和一次后缀统计把两端的合法元素数量算出来，再相乘求和**。

---  

## 反思  

- **第一反应**：看到四个下标的严格顺序，直接想到多层循环枚举，没意识到可以把中间的两个下标先固定。  
- **最容易踩的坑**：  
  - **下标越界**：在计算 `right_gt[k+1]` 时要保证 `k+1` 不超过数组长度。  
  - **前缀和查询**：`left_prefix[nums[k]-1]` 必须先判断 `nums[k]` 是否为 `1`（此时查询 `0`，前缀数组要有第 `0` 位的默认 `0`）。  
  - **重复计数**：一定要保证 `i` 在 `j` 左侧、`l` 在 `k` 右侧，否则会把不合法的四元组算进去。  
- **下次遇到同类题**：第一步先**思考能否固定中间的一个或两个关键下标**，然后检查两侧是否可以用**前缀/后缀计数**或**BIT / 哈希表**一次性求出符合条件的元素个数。这样就能把枚举层数从四层降到两层，时间立刻得到指数级提升。