# #798. 最高得分的最小旋转 / Smallest Rotation with Highest Score

> 难度：困难 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/smallest-rotation-with-highest-score/)

---

## 题目（英文原版）

**Description**

You are given an array nums. You can rotate it by a non-negative integer k so that the array becomes [nums[k], nums[k + 1], ... nums[nums.length - 1], nums[0], nums[1], ..., nums[k-1]]. Afterward, any entries that are less than or equal to their index are worth one point.
Return the rotation index k that corresponds to the highest score we can achieve if we rotated nums by it. If there are multiple answers, return the smallest such index k.

**Examples**

**Example 1:**

```
Input: nums = [2,3,1,4,0]
Output: 3
Explanation: Scores for each k are listed below: 
k = 0,  nums = [2,3,1,4,0],    score 2
k = 1,  nums = [3,1,4,0,2],    score 3
k = 2,  nums = [1,4,0,2,3],    score 3
k = 3,  nums = [4,0,2,3,1],    score 4
k = 4,  nums = [0,2,3,1,4],    score 3
So we should choose k = 3, which has the highest score.
```

**Example 2:**

```
Input: nums = [1,3,0,2,4]
Output: 0
Explanation: nums will always have 3 points no matter how it shifts.
So we will choose the smallest k, which is 0.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] < nums.length

---

## 题目（中文翻译）

给定一个数组 `nums`。你可以通过一个非负整数 `k` 对其进行旋转，使得数组变为  

`[nums[k], nums[k + 1], … , nums[nums.length - 1], nums[0], nums[1], … , nums[k-1]]`。  

旋转完成后，任意 **值小于等于其下标** 的元素计 1 分。  

返回能够获得最高分数的旋转下标 `k`。如果存在多个下标能够得到相同的最高分数，返回最小的那个 `k`。

---

### 示例

#### 示例 1
```
输入: nums = [2,3,1,4,0]
输出: 3
解释: 各个 k 的得分如下:
k = 0, nums = [2,3,1,4,0],    score 2
k = 1, nums = [3,1,4,0,2],    score 3
k = 2, nums = [1,4,0,2,3],    score 3
k = 3, nums = [4,0,2,3,1],    score 4
k = 4, nums = [0,2,3,1,4],    score 3
因此应选择得分最高的 k = 3。
```

#### 示例 2
```
输入: nums = [1,3,0,2,4]
输出: 0
解释: 无论如何旋转，数组始终得到 3 分。
所以选择最小的 k，即 0。
```

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的旋转都枚举一遍**，每一次都把数组重新排好顺序，然后逐个检查每个位置 `i` 上的元素 `nums[i]` 是否满足 `nums[i] ≤ i`，满足就得 1 分，最后统计这次旋转得到的总分。  

- **数据结构**：只需要普通的 Python 列表（list），相当于我们平时用的「购物清单」；  
- **为什么正确**：因为题目要求的是「遍历所有合法的旋转 `k`」并找出分数最高的那个，枚举所有 `k`（从 `0` 到 `n-1`）自然能保证不漏掉任何一种可能。  

#### 代码（Python）

```python
from typing import List

def bestRotation_brute(nums: List[int]) -> int:
    n = len(nums)
    best_k = 0          # 当前分数最高的旋转下标
    best_score = -1     # 最高分，初始设为 -1 方便第一次比较

    # 枚举所有可能的旋转 k
    for k in range(n):
        # 把数组左旋 k 位，等价于切片 + 拼接
        rotated = nums[k:] + nums[:k]

        # 计算当前旋转的得分
        score = 0
        for i, val in enumerate(rotated):
            if val <= i:          # 满足题目条件得一分
                score += 1

        # 更新最佳答案（若分数相同，保留更小的 k）
        if score > best_score:
            best_score = score
            best_k = k

    return best_k
```

> **关键行解释**  
> - `rotated = nums[k:] + nums[:k]`：把数组左移 `k` 位，就像把排好队的学生从第 `k` 位开始重新排队，前面走到队尾。  
> - `if val <= i:`：判断「学生的编号」是否不大于「他在队列中的位置」。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 我们要遍历 `n` 种旋转，每种旋转内部又要遍历 `n` 个元素去计分。  
  - 用大白话说，就是「如果数组有 10,000 个元素，最坏情况下要做 100,000,000 次比较」，显然太慢了。

- **空间复杂度**：`O(n)`  
  - 需要额外的 `rotated` 列表保存每次旋转后的数组，长度为 `n`。  
  - 其余变量都是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每一次旋转都要重新遍历整个数组**。  
其实我们并不需要真的把数组转过去，只要**知道每个元素在多少个 `k` 下会得分**，就可以直接统计出所有 `k` 的总分。

---

#### 2.1 关键观察  

- 对于下标 `i`（原数组中的位置）和它的值 `nums[i]`，在旋转 `k` 后，它会出现在新下标  

  \[
  new\_idx = (i - k + n) \bmod n
  \]

- 该元素在旋转 `k` 时能得分的条件是  

  \[
  nums[i] \le new\_idx
  \]

- 把条件改写成「`k` 不在某个区间」更容易处理。  
  当 `new_idx` 小于 `nums[i]` 时，元素 **不给分**，这对应的 `k` 形成一个**不合法区间**。

- 通过一点代数变形可以得到「不合法区间」的起点和终点：

  \[
  \begin{aligned}
  nums[i] &> (i - k + n) \bmod n \\
  \Longrightarrow\; k &\in \bigl[(i - nums[i] + 1) ,\; i \bigr] \pmod n
  \end{aligned}
  \]

  换句话说，如果 `k` 落在区间 **`[start, end]`（循环取模）**，那么 `nums[i]` **不计分**；否则计 1 分。

- 于是**每个元素只会把一段 `k` 标记为「不加分」**，其余所有 `k` 都会得到 1 分。

---

#### 2.2 差分数组（前缀和）技巧  

我们可以使用「差分数组」来高效地把所有「不加分」的区间累加到每个 `k` 上：

1. 建立一个长度为 `n+1` 的差分数组 `diff`，初始全为 0。  
2. 对于每个元素 `i`，计算它的「不加分」区间 `[start, end]`（取模后可能会跨越数组尾部）。  
3. 在 `diff` 上做区间加 **-1**（因为这段区间要扣掉 1 分）：

   - 如果区间不跨界：`diff[start] -= 1; diff[end+1] += 1`。  
   - 如果跨界（比如 `[7, 2]` 在长度 10 的数组里），则分成两段 `[start, n-1]` 与 `[0, end]` 分别处理。

4. 完成所有元素的区间更新后，对 `diff` 做一次前缀和，得到每个 `k` 的 **总扣分**。  
5. 初始每个 `k` 的得分都是 `n`（因为每个元素默认都能得 1 分），最终得分 = `n + diff_prefix[k]`（`diff_prefix` 为前缀和结果）。  
6. 只要遍历一次找出最大得分对应的最小 `k` 即可。

> **类比**：差分数组就像在一条路上装设「增减灯」，每当有一段路需要「减 1 分」时，只在这段路的入口点关灯（-1），在出口点开灯（+1），最后走完整条路累计灯的状态，就得到每段路的真实「减分」值。

---

#### 代码（Python）

```python
from typing import List

def bestRotation(nums: List[int]) -> int:
    n = len(nums)
    # diff[i] 表示第 i 位相对于前一位的增量，长度多留一个位置方便处理区间末端
    diff = [0] * (n + 1)

    for i, val in enumerate(nums):
        # 计算「不计分」区间的起点和终点（取模后可能跨界）
        # 区间为 (i - val + 1) ... i   （闭区间）
        start = (i - val + 1 + n) % n   # 加 n 防止负数
        end = i

        if start <= end:          # 区间没有跨越数组尾部
            diff[start] -= 1      # 区间入口 -1
            diff[end + 1] += 1    # 区间出口 +1（因为 diff 长度为 n+1，安全）
        else:                     # 跨界，拆成两段
            # 第1段：start ... n-1
            diff[start] -= 1
            diff[n] += 1           # 到数组末尾结束
            # 第2段：0 ... end
            diff[0] -= 1
            diff[end + 1] += 1

    # 前缀和得到每个 k 的累计「扣分」值
    max_score = -1
    best_k = 0
    cur = 0                     # 当前前缀和（累计扣分）
    for k in range(n):
        cur += diff[k]          # 加上第 k 位的增量
        # 初始每个 k 的得分是 n，实际得分 = n + cur（cur 可能是负数）
        score = n + cur
        if score > max_score:   # 只保留分数更大的情况，若相等则保持更小的 k
            max_score = score
            best_k = k

    return best_k
```

> **关键行解释**  
> - `start = (i - val + 1 + n) % n`：把「不计分」区间的左端点映射到 `[0, n-1]`，相当于把「学生需要站在队尾」的条件转成「旋转多少次会导致他站在不合格的位置」。  
> - `diff[start] -= 1` / `diff[end + 1] += 1`：在差分数组上做「区间减 1」的标记。  
> - `cur += diff[k]`：一步一步累计差分，得到第 `k` 次旋转到底扣了多少分。  
> - `score = n + cur`：因为每个元素默认能得 1 分，`n` 是上限，`cur`（负数）才是实际扣掉的分数。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组来构造差分区间，随后再遍历一次差分数组做前缀和。  
  - 与暴力解 `O(n²)` 相比，**大幅降低**，即使 `n = 10⁵` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 额外使用一个长度为 `n+1` 的差分数组。  
  - 这在题目限制下是完全可以接受的。

---

## 心得

- **核心技巧**：利用「差分数组 + 前缀和」把「每个元素对所有旋转的贡献」转化为区间加减操作，从而在 **线性时间** 内得到所有旋转的得分。  
- **适用场景**：  
  1. 「区间加减」类问题，例如 LeetCode 1852 *Maximum Digits Sum After Increment Operations*。  
  2. 「循环数组」里需要统计每个起点的贡献，如 798 *Smallest Rotation with Highest Score*（本题）和 1654 *Minimum Deletions to Make Array Balanced*（思路类似）。  
- **一句话总结**：**把「不计分」的旋转范围标记为区间减 1，前缀和即得每个旋转的真实得分**。

---

## 反思

- **第一反应**：看到「旋转」和「分数」两个关键词，我会先想到「枚举所有旋转」——这就是暴力解的出发点。  
- **最容易踩的坑**：  
  1. **取模后的区间跨界**：`start > end` 时需要拆成两段，否则会出现负向索引错误。  
  2. **差分数组的越界**：在 `diff[end+1]` 时要保证 `end+1 ≤ n`，所以差分数组长度要多开一个位置。  
  3. **初始得分的设定**：别忘了每个元素默认能得 1 分，最终得分是 `n + 累计差分`。  
- **下次类似题的第一步**：先思考「每个元素对所有可能答案的贡献」是否可以用 **区间** 表示，如果可以，就立刻尝试差分数组/前缀和来把区间操作压缩到 `O(n)`。