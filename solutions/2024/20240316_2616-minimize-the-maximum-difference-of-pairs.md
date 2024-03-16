# #2616. 最小化配对的最大差值 / Minimize the Maximum Difference of Pairs

> 难度：中等 · 标签：Array、Binary Search、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer p. Find p pairs of indices of nums such that the maximum difference amongst all the pairs is minimized. Also, ensure no index appears more than once amongst the p pairs.
Note that for a pair of elements at the index i and j, the difference of this pair is |nums[i] - nums[j]|, where |x| represents the absolute value of x.
Return the minimum maximum difference among all p pairs. We define the maximum of an empty set to be zero.

**Examples**

**Example 1:**

```
Input: nums = [10,1,2,7,1,3], p = 2
Output: 1
Explanation: The first pair is formed from the indices 1 and 4, and the second pair is formed from the indices 2 and 5. 
The maximum difference is max(|nums[1] - nums[4]|, |nums[2] - nums[5]|) = max(0, 1) = 1. Therefore, we return 1.
```

**Example 2:**

```
Input: nums = [4,2,1,2], p = 1
Output: 0
Explanation: Let the indices 1 and 3 form a pair. The difference of that pair is |2 - 2| = 0, which is the minimum we can attain.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109
- 0 <= p <= (nums.length)/2

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 **0** 开始的整数数组 `nums` 和一个整数 `p`。请找出 `p` 对下标，使得所有配对（pair）之间的最大差值（maximum difference）最小，并且在这 `p` 对配对中，同一个下标不能出现超过一次。  

对于下标为 `i` 和 `j` 的两个元素，它们的差值定义为 `|nums[i] - nums[j]|`，其中 `|x|` 表示 **绝对值**（absolute value）。  

返回所有 `p` 对配对中的最小的最大差值。如果配对集合为空，则最大值定义为 `0`。  

**示例**  

*示例 1*  
```
输入: nums = [10,1,2,7,1,3], p = 2
输出: 1
解释: 第一对配对选取下标 1 和 4，第二对配对选取下标 2 和 5。  
最大差值为 max(|nums[1] - nums[4]|, |nums[2] - nums[5]|) = max(0, 1) = 1。因此返回 1。
```

*示例 2*  
```
输入: nums = [4,2,1,2], p = 1
输出: 0
解释: 选择下标 1 和 3 组成一对。该配对的差值为 |2 - 2| = 0，这是可以得到的最小值。
```

**约束条件**  

- `1 <= nums.length <= 10^5`  
- `0 <= nums[i] <= 10^9`  
- `0 <= p <= nums.length / 2`   (整数除法)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的配对方式**，然后在每一种配对方案里找出最大的差值，最后取所有方案中的最小值。

- **枚举配对**：把数组的下标看成“人”，我们要把 `2·p` 个人两两配对，使得没有人被重复使用。可以把配对看成把下标划分成 `p` 对，每对里有两个下标。
- **计算差值**：对于每一对 `(i, j)`，差值就是 `|nums[i] - nums[j]|`。对该配对方案的所有差值取最大值。
- **取最小**：遍历所有配对方案，保留最大的差值最小的那一个。

> **类比**：想象你有 `2p` 张卡片，每张卡片上写着一个数字。你要把它们两两配成 `p` 对，目标是让“最糟糕的一对”（差值最大的那对）的差距尽可能小。

**为什么能得到正确答案**：因为我们穷举了**所有合法的配对方式**，所以必然会包含最优的那一种。只要把每一种方案的“最大差值”算出来，再在这些最大差值中取最小，就得到了题目要求的答案。

**为什么不实际使用**：  
- **组合数爆炸**：`n` 最多 `10⁵`，即使 `p = n/2`，配对方式的数量是 `(2p)! / (2ⁿ·p!)`，天文数字，根本不可能在电脑上跑完。  
- **时间复杂度**：如果硬凑一个实现，最坏情况下要遍历所有配对，时间复杂度约为 `O( (2p)! )`，对任何稍大的输入都会超时。

#### 代码（Python）

```python
import itertools
from math import inf

def brute_min_max_diff(nums, p):
    n = len(nums)
    # 先取出所有下标
    indices = list(range(n))
    best = inf

    # 生成所有可能的 p 对（这里仅用于演示，实际不可用）
    # 先选出 2p 个下标，再在这 2p 个下标中两两配对
    for chosen in itertools.combinations(indices, 2 * p):
        # 对 chosen 按顺序两两配对（不一定是最优配对方式，只是示例）
        # 为了穷举所有配对，需要再对 chosen 的全排列做配对，这里省略
        # ...
        pass

    return best
```

> **注意**：上述代码仅为“思路演示”，真正的暴力实现需要更复杂的递归/回溯来枚举配对，代码量大且运行时间极其慢，**不建议在实际面试或竞赛中使用**。

#### 复杂度

- **时间复杂度**：`O( (2p)! )`（阶乘级别）——即使 `p=10`，也已经是 `≈3.6e6` 次操作，`p=20` 更是天文数字。  
- **空间复杂度**：`O(p)` 用于保存当前配对的递归栈或临时数组。

> **大白话**：`O(n²)` 代表“时间随输入大小的平方增长”。这里的暴力解甚至比 `O(n²)` 更糟，几乎是 **“指数级”** 增长，输入稍大就会卡死。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举配对是最耗时的环节**。我们需要找到一种**快速判断**在给定的“最大差值上限 `limit`”的情况下，是否能组成至少 `p` 对。若能，则说明答案 **不大于** `limit`，否则答案 **大于** `limit`。这正好符合**二分查找**的思路。

**核心步骤**：

1. **先排序**  
   把 `nums` 按升序排好。排序后，相邻的两个数差值最小，配对时倾向于把相邻的数配在一起，这样更容易让差值 ≤ `limit`。  
   > 类比：把一堆不同长度的木棍排成从短到长的顺序，想要挑出差距最小的两根木棍，自然就从相邻的开始找。

2. **二分答案**  
   - `low = 0`（最小可能的最大差值）  
   - `high = max(nums) - min(nums)`（最坏情况下需要配最远的两个数）  
   - 在 `[low, high]` 区间做二分，取中点 `mid` 作为当前的“差值上限”。  

3. **贪心判断**：在已排序的数组中，**一次遍历**尝试配对  
   - 使用指针 `i` 从左到右。  
   - 若 `nums[i+1] - nums[i] <= mid`，说明这两个数可以组成一对，计数 `cnt += 1`，并把 `i` 向前跳两格（因为这两个下标已经被占用）。  
   - 否则，`i` 只向前跳一格，尝试把 `nums[i]` 与下一个数配。  
   - 结束遍历后，若 `cnt >= p`，说明在 `mid` 这个上限下可以配出至少 `p` 对，**答案可以更小**；否则需要更大的上限。  

   这一步的 **贪心** 是有理论依据的：  
   - 已排序后，若两个相邻数的差值已经 ≤ `mid`，把它们配在一起永远不会比把它们分别配给更远的数得到更差的结果。  
   - 因此，**最左侧** 能配对的相邻元素一定是最优选择，后面的配对不受影响。

4. **收敛**  
   当二分结束时，`low`（或 `high`）即为最小的“可以配出 `p` 对的最大差值”。这就是题目要求的答案。

#### 代码（Python）

```python
from typing import List

def minimize_maximum_difference(nums: List[int], p: int) -> int:
    """
    核心思路：
    1. 先把数组排序，方便后面只看相邻元素的差值。
    2. 对答案进行二分搜索，利用贪心在 O(n) 时间内判断
       “在当前上限 limit 下能否配出至少 p 对”。
    """
    nums.sort()                     # 1️⃣ 排序，O(n log n)

    # 2️⃣ 二分搜索答案的范围
    low, high = 0, nums[-1] - nums[0]    # 最小可能为 0，最大可能为全局差值

    # 判定函数：给定 limit，能否配出 >= p 对？
    def can_form(limit: int) -> bool:
        cnt = 0          # 已经配好的对数
        i = 0
        n = len(nums)
        while i + 1 < n:                # 必须保证有 i+1 这个元素
            # 若相邻两个数差值不超过 limit，就配对
            if nums[i + 1] - nums[i] <= limit:
                cnt += 1
                i += 2                  # 这两个下标都已经用掉，跳过
            else:
                i += 1                  # 不能配，尝试把 nums[i] 与下一个元素配
        return cnt >= p                 # 是否满足需求

    # 标准的二分模板（左闭右闭）
    while low < high:
        mid = (low + high) // 2          # 取中间值作为当前的差值上限
        if can_form(mid):                # 能配够 p 对 → 说明答案 ≤ mid
            high = mid
        else:                            # 配不够 → 需要更大的上限
            low = mid + 1

    return low                           # 最小的可行上限
```

#### 复杂度

- **时间复杂度**：  
  - 排序 `O(n log n)`（`n = len(nums)`）  
  - 二分搜索的轮数是 `log2(maxDiff)`，其中 `maxDiff = max(nums) - min(nums)` ≤ `10⁹`，所以最多约 `30` 次。每次二分里调用 `can_form`，线性遍历一次数组 `O(n)`。  
  - 总体为 `O(n log n + n log maxDiff)`，在最坏情况下约等于 `O(n log n)`（因为 `log maxDiff` 常数很小）。  
  - **大白话**：先把数排好序要花 `n` 乘以 “对数” 的时间（比普通的线性遍历稍微慢一点），之后每次检查“能不能配对”只需要一次线性扫描，检查的次数最多 30 次，整体还是非常快。

- **空间复杂度**：`O(1)`（不计排序本身的原地改动，只使用常数个额外变量）。  
  - **解释**：我们只用了几个整数指针和计数器，和输入规模无关。

---

## 心得

- **核心技巧**：先**排序** → 用**二分答案** + **贪心配对** 判定可行性。  
- **适用的题型**（类似思路）  
  1. *Divide Array in Sets of K Consecutive Numbers*（需要先排序，再用贪心/哈希配对）  
  2. *Find the Minimum Number of Moves to Make All Elements Equal*（二分答案 + 可行性判定）  
  3. *Split Array Largest Sum*（同样是二分答案，判定是否能在给定阈值下分成 ≤ m 段）  

- **一句话总结解题钥匙**：**把问题转化为“在给定上限下能否完成目标”，用二分搜索找最小上限，配对过程用排序后相邻贪心完成**。

---

## 反思

- **第一反应**：看到“最大差值最小化”，自然想到**先把数组排好序**，因为排序后相邻差最小。随后想到**二分答案**，因为答案是一个数值范围且满足“可行 → 更大仍可行”的单调性。  
- **最容易踩的坑**  
  1. **边界条件**：`p = 0` 时答案应为 `0`（空集最大值定义为 0），实现时二分仍能返回 `0`，但要确认 `can_form` 能正确返回 `True`。  
  2. **相邻配对的跳步**：配对成功后一定要 `i += 2`，否则会重复使用同一个下标。  
  3. **整数溢出/范围**：`high = nums[-1] - nums[0]` 可能为 `0`，二分循环仍能正常结束。  
- **下次遇到同类题**：第一步先判断**是否存在单调的“可行性”**（即答案增大时可行性不减），如果有，立即考虑**二分答案 + 线性/贪心判定**的框架。这样往往能把复杂度从指数级降到 `O(n log n)`。