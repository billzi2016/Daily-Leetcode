# #1224. **最大相等频率** / Maximum Equal Frequency

> 难度：困难 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/maximum-equal-frequency/)

---

## 题目（英文原版）

**Description**

Given an array nums of positive integers, return the longest possible length of an array prefix of nums, such that it is possible to remove exactly one element from this prefix so that every number that has appeared in it will have the same number of occurrences.
If after removing one element there are no remaining elements, it's still considered that every appeared number has the same number of ocurrences (0).

**Examples**

**Example 1:**

```
Input: nums = [2,2,1,1,5,3,3,5]
Output: 7
Explanation: For the subarray [2,2,1,1,5,3,3] of length 7, if we remove nums[4] = 5, we will get [2,2,1,1,3,3], so that each number will appear exactly twice.
```

**Example 2:**

```
Input: nums = [1,1,1,2,2,2,3,3,3,4,4,4,5]
Output: 13
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个正整数数组 `nums`，返回 `nums` 的一个前缀（prefix）的最长可能长度，使得可以恰好删除该前缀中的 **一个** 元素后，前缀中出现的每个数字的出现次数（occurrences）都相同。  
如果在删除一个元素后前缀中不再剩余任何元素，也仍然视为所有出现的数字的出现次数相同（均为 0）。

**示例 1**  
Input: `nums = [2,2,1,1,5,3,3,5]`  
Output: `7`  
Explanation: 对于长度为 7 的子数组（subarray）`[2,2,1,1,5,3,3]`，如果删除 `nums[4] = 5`，得到 `[2,2,1,1,3,3]`，此时每个数字恰好出现两次。

**示例 2**  
Input: `nums = [1,1,1,2,2,2,3,3,3,4,4,4,5]`  
Output: `13`

**约束条件**  
- `2 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一种可能的前缀**，然后在这个前缀里**尝试删除每一个元素**，检查剩下的数字出现次数是否全部相同。

- **数据结构**  
  - `cnt`：一个哈希表（在 Python 中用 `dict`），把数字当作“单词”，出现次数当作“页码”。比如 `cnt[5] = 3` 就像在字典里查到单词 5 出现在第 3 页。  
  - `freq`：另一个哈希表，用来统计**出现次数本身**出现了多少次。比如 `freq[2] = 4` 表示有 4 个不同的数字，它们各自出现了 2 次。

- **为什么正确**  
  对每一个前缀 `nums[:i+1]`，我们把它的所有子数组（即删除一个位置后的数组）都遍历一遍，逐个比较它们的出现次数是否相等。如果有一种删除方式可以让所有出现次数相等，那么这个前缀就是合法的。因为我们检查了 **所有可能**，所以一定不会漏掉答案。

- **时间/空间复杂度**  

  - 枚举前缀需要 `O(n)`（`n` 为数组长度）。  
  - 对每个前缀再枚举要删除的元素，需要再遍历一次前缀，最坏情况是 `O(i)`，累计下来是 `O(1 + 2 + … + n) = O(n²)`。  
  - 哈希表里最多存放 `n` 个不同的数字和对应的出现次数，空间是 `O(n)`。  

  用大白话说，`O(n²)` 就像你在一条长长的队伍里，先让第一个人排队检查所有人，接着第二个人再检查所有人，…… 这样检查的次数会是 `1 + 2 + … + n`，等于 `n` 的平方量级，随着 `n` 增大会非常慢。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxEqualFreq_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 枚举前缀的长度 i+1
    for i in range(n):
        # 统计前缀里每个数字出现的次数
        cnt = defaultdict(int)
        for j in range(i + 1):
            cnt[nums[j]] += 1

        # 试着删除前缀里每一个位置的元素
        for remove_idx in range(i + 1):
            # 把要删除的元素次数减一（如果次数降到 0，就把它从字典里删掉）
            removed_val = nums[remove_idx]
            cnt[removed_val] -= 1
            if cnt[removed_val] == 0:
                del cnt[removed_val]

            # 检查剩余数字的出现次数是否全相等
            freqs = list(cnt.values())
            if len(set(freqs)) <= 1:          # 全部相等或只有一种数字
                ans = max(ans, i + 1)        # 更新答案

            # 恢复原来的计数，准备下一个 remove_idx
            cnt[removed_val] = cnt.get(removed_val, 0) + 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历 `n` 次，内层在最坏情况下要遍历前缀的所有元素，再遍历每个可能的删除位置，总共是二次方级别的工作量。

- **空间复杂度**：`O(n)`  
  解释：哈希表 `cnt` 最多保存 `n` 个不同的数字及其出现次数，随 `n` 增长线性增加。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**每次都重新统计整个前缀**。我们可以在一次遍历的过程中**动态维护**所需的信息，这样每个元素只处理一次，时间降到线性 `O(n)`。

核心思路：

1. **实时记录每个数字的出现次数** `cnt[x]`（哈希表）。  
2. **实时记录“出现次数出现了多少次”** `freq[f]`。例如，`freq[3] = 5` 表示有 5 个不同的数字，它们各自出现了 3 次。  
   - 这一步好比我们在统计“每页有多少单词”。  
3. 在遍历到第 `i` 个元素后，**我们只需要检查当前前缀是否满足题目条件**，不必再枚举删除哪个元素。  
   - 设 `maxFreq` 为当前所有数字的最大出现次数，`cntMax = freq[maxFreq]` 为出现 `maxFreq` 次的数字个数。  
   - 设 `total = i + 1` 为前缀长度，`distinct = len(cnt)` 为不同数字的种类数。

4. **合法前缀的三种情形**（把删除的那一次“想象”为把某个数字的出现次数减 1）：

   1. **全部出现一次**：`maxFreq == 1`  
      只要所有数字都只出现一次，随便删除一个，剩下的仍然全是 1 次。  
   2. **只剩一种数字的出现次数为 1**：`freq[1] == 1` 且 `maxFreq * cntMax == total - 1`  
      也就是说，有一个数字只出现一次，其他所有数字的出现次数相同（等于 `maxFreq`），把唯一的那一次删掉后，所有数字的出现次数就相等了。  
   3. **只有一种数字的出现次数比其他多 1**：`cntMax == 1` 且 `(maxFreq - 1) * (freq[maxFreq - 1] + 1) == total - 1`  
      这里只有一个数字出现了 `maxFreq` 次，其他数字都出现了 `maxFreq-1` 次。把这个出现次数最多的数字删掉一次后，所有数字的出现次数就都变成 `maxFreq-1`。

   只要上述任意一种成立，当前前缀就可以通过**删除恰好一个元素**让所有出现次数相等，我们就把答案更新为 `total`。

5. **为什么只需要这三种**  
   - 删除一次只能让 **一种** 数字的出现次数减少 1。  
   - 为了让所有数字的出现次数相同，原本只能有两种不同的频率：`x` 和 `x+1`（或者 `x` 和 `1`）。  
   - 这三种情况正好覆盖了所有可能的组合。

6. **实现细节**  
   - 每处理一个新数字 `num`，先把它原来的频率 `old = cnt[num]` 从 `freq[old]` 中减去，再把 `cnt[num]` 加 1，新的频率 `new = old + 1` 加到 `freq[new]` 中。  
   - 同时维护 `maxFreq`（如果 `new > maxFreq` 就更新）。  
   - 检查合法性时只看 `maxFreq`、`freq[maxFreq]`、`freq[maxFreq-1]`、`freq[1]` 四个数，常数时间。

这样整个数组只遍历一次，时间是 `O(n)`，空间是哈希表的大小 `O(n)`（最坏情况下所有数字都不相同）。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxEqualFreq(nums: List[int]) -> int:
    # cnt[x]   : x 在前缀中出现了多少次
    cnt = defaultdict(int)
    # freq[f]  : 有多少个不同的数字，它们的出现次数恰好是 f
    freq = defaultdict(int)

    maxFreq = 0          # 当前所有数字的最大出现次数
    answer = 0

    for i, num in enumerate(nums):
        # 1. 把旧的出现次数从 freq 中减去
        old = cnt[num]
        if old > 0:
            freq[old] -= 1

        # 2. 更新 cnt 与 freq
        cnt[num] += 1
        new = cnt[num]
        freq[new] += 1

        # 3. 更新 maxFreq
        maxFreq = max(maxFreq, new)

        total = i + 1                 # 前缀长度
        # ---------- 检查三种合法情况 ----------
        # 情形 1：所有出现次数都是 1
        if maxFreq == 1:
            answer = total
            continue

        # 情形 2：出现次数为 1 的数字恰好只有一个，且其它数字出现次数相同
        # 这里的等式等价于：total - 1 == maxFreq * cnt[maxFreq] 且 freq[1] == 1
        if freq[1] == 1 and maxFreq * freq[maxFreq] == total - 1:
            answer = total
            continue

        # 情形 3：只有一种数字出现次数为 maxFreq，其他都是 maxFreq-1
        # 等价条件：cnt[maxFreq] == 1 且 (maxFreq-1)*(freq[maxFreq-1]+1) == total-1
        if freq[maxFreq] == 1 and (maxFreq - 1) * (freq[maxFreq - 1] + 1) == total - 1:
            answer = total
            continue

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：数组只遍历一次，每个元素的计数更新、`maxFreq` 更新以及合法性检查都是常数时间操作。相比暴力的二次方，这就像一次排队检查，不会因为人数多而指数增长。

- **空间复杂度**：`O(n)`  
  解释：`cnt` 和 `freq` 两个哈希表最多各保存 `n` 条记录（最坏情况每个数字都不相同），随输入规模线性增长。

---

## 心得

- **核心技巧**：**使用两个哈希表同步维护“数字出现次数”和“出现次数出现的频率”，并通过枚举有限的几种频率分布情况来判定合法前缀**。  
- **适用的题型**：  
  1. **“前缀合法性”** 类似题目，如 *Maximum Frequency of an Element After Deleting One Element*。  
  2. **“出现次数相等”** 的变体，如 *Equal Frequency*（LeetCode 1224）。  
  3. **“统计频率的频率”** 的问题，如 *Frequency of the Most Frequent Element*（LeetCode 1838）。  
- **一句话总结解题钥匙**：**把“出现多少次”也当成普通的数来统计，只要把频率的分布控制在两种（或一种）可能的形态，就能在 O(n) 内判断是否可以只删一次让所有次数相等。**

---

## 反思

- **第一反应**：看到“删除一个元素后所有出现次数相同”，我立刻想到**枚举前缀 + 枚举删除位置**的暴力思路。  
- **最容易踩的坑**  
  1. **忘记考虑空前缀**：删除后可能剩下 0 个元素，仍然算合法。  
  2. **频率为 0 的情况**：在维护 `freq` 时要小心把 `freq[0]` 排除，否则会误判。  
  3. **更新 `maxFreq`**：删除元素不会让 `maxFreq` 下降，但在本题我们只做“添加”操作，所以只需要在 `new > maxFreq` 时更新即可。  
- **下次遇到同类题**，第一步应该**先思考如何在一次遍历中实时维护“数字出现次数”和“出现次数出现的次数”，把问题转化为检查几种频率分布是否满足条件**，而不是直接枚举。这样思路更清晰，也更容易写出 O(n) 的解法。