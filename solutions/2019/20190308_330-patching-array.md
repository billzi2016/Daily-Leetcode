# #330. **补丁数组** / Patching Array

> 难度：困难 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/patching-array/)

---

## 题目（英文原版）

**Description**

Given a sorted integer array nums and an integer n, add/patch elements to the array such that any number in the range [1, n] inclusive can be formed by the sum of some elements in the array.
Return the minimum number of patches required.

**Examples**

**Example 1:**

```
Input: nums = [1,3], n = 6
Output: 1
Explanation:
Combinations of nums are [1], [3], [1,3], which form possible sums of: 1, 3, 4.
Now if we add/patch 2 to nums, the combinations are: [1], [2], [3], [1,3], [2,3], [1,2,3].
Possible sums are 1, 2, 3, 4, 5, 6, which now covers the range [1, 6].
So we only need 1 patch.
```

**Example 2:**

```
Input: nums = [1,5,10], n = 20
Output: 2
Explanation: The two patches can be [2, 4].
```

**Example 3:**

```
Input: nums = [1,2,2], n = 5
Output: 0
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 104
- nums is sorted in ascending order.
- 1 <= n <= 231 - 1

---

## 题目（中文翻译）

给定一个已排序的整数数组 `nums` 和一个整数 `n`，向数组中添加（补丁）元素，使得区间 `[1, n]`（包括 1 和 n）内的每个数字都可以表示为数组中某些元素的和。返回所需的最少补丁数量。

**示例 1**

```text
Input: nums = [1,3], n = 6
Output: 1
```

**解释**  
`nums` 的组合有 `[1]`、`[3]`、`[1,3]`，能够形成的和为：`1, 3, 4`。  
如果我们向 `nums` 中补上 `2`，则组合为 `[1]`、`[2]`、`[3]`、`[1,3]`、`[2,3]`、`[1,2,3]`。  
可能的和为 `1, 2, 3, 4, 5, 6`，已覆盖区间 `[1, 6]`。  
因此只需要 1 个补丁。

**示例 2**

```text
Input: nums = [1,5,10], n = 20
Output: 2
```

**解释**  
可以补的两个元素为 `[2, 4]`。

**示例 3**

```text
Input: nums = [1,2,2], n = 5
Output: 0
```

**约束条件**

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^4`
- `nums` 按升序排序。
- `1 <= n <= 2^31 - 1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的子集**，看能不能把 `[1, n]` 中的每个整数都表示出来。  
- 我们可以把“能否组成某个数”看成 **背包问题**：  
  - 背包里有若干个物品（数组 `nums` 中的元素），每个物品只能使用一次。  
  - 背包容量从 `1` 到 `n`，我们要判断每个容量是否能恰好装满。  
- 为了判断哪些数已经可以被表示，我们用一个布尔数组 `can[i]`（类似字典的查表，`i` 就是“词”，`can[i]` 是“是否在词典里”）。  
- 接下来从 `1` 开始检查：  
  1. 如果 `can[i]` 为 `True`，说明已经能组成 `i`，继续检查 `i+1`。  
  2. 如果 `can[i]` 为 `False`，说明缺少某个数。我们**把 `i` 当成新的补丁**，把它加入 `nums`，并用同样的背包方式把它的贡献更新到 `can` 中。  
- 这样一直循环到 `i == n`，统计加入的补丁数量即可。

> 为什么这个方法一定能得到答案？  
> 因为每当我们发现最小的不可达数 `i` 时，把 `i` 加进去一定是**最保守的补丁**——它能立刻让 `i` 可达，同时也会帮助后面更大的数。这样不管后面再怎么补，都不会比我们直接补 `i` 用更少的次数。

#### 代码（Python）

```python
def minPatches(nums, n):
    # can[x] 表示是否能用已有元素凑出和为 x（0 <= x <= n）
    can = [False] * (n + 1)
    can[0] = True                     # 空集合的和为 0，始终可达

    # 用原数组的元素做一次“背包” DP
    for v in nums:
        # 为防止覆盖掉还未使用的状态，从后往前遍历
        for s in range(n, v - 1, -1):
            if can[s - v]:
                can[s] = True

    patches = 0          # 记录补丁数量
    i = 1                # 当前要检查的最小正整数

    while i <= n:
        if can[i]:               # 已经可以凑出 i，直接跳到下一个
            i += 1
            continue

        # i 不可达，需要补一个数 i
        patches += 1
        # 把 i 加入后，同样做一次背包 DP 更新 can[]
        for s in range(n, i - 1, -1):
            if can[s - i]:
                can[s] = True
        i += 1                    # 继续检查下一个

    return patches
```

> 关键行中文注释已写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n * (len(nums) + patches))`  
  - `n` 是要覆盖的最大数字，`len(nums)` 是原数组长度，`patches` 最坏情况下也可能接近 `log n`（实际更小）。  
  - 用大白话说，就是**每检查一个数字都要遍历一次 1~n 的区间**，所以会比较慢。  
- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n+1` 的布尔数组 `can` 来记录每个和是否可达，类似把所有可能的“词”都记在一本大字典里。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**对每个缺失的数都重新遍历一遍 `[1, n]`**，导致时间呈线性乘积。  
其实我们并不需要知道**每个具体的可达数**，只要知道**目前能覆盖的连续区间** `[1, miss)` 即可。  

**核心观察**（来源于数学归纳）  
> 假设我们已经能够用现有的数（包括已补的）凑出所有 `1 … miss-1`，  
> - 如果下一个数组元素 `num` **不大于 `miss`**，则把 `num` 加进来后，最大可达区间会扩展到 `miss + num - 1`。  
> - 如果 `num` **大于 `miss`**，说明 `miss` 本身无法凑出，这时最优的做法是**直接补上 `miss`**（因为 `miss` 是当前最小的缺口），补完后可达区间会翻倍到 `2*miss - 1`。  

这样每一次“扩展区间”都会**把左端点 `miss` 向右推**，而且每次操作（无论是使用数组元素还是补丁）都能让区间长度**至少翻倍**，所以总体只会进行 `O(log n)` 次操作。

> 类比：  
> - `miss` 就像**水桶的容量上限**，我们先往桶里倒已有的石子（数组元素），如果石子太大装不进去，就先往桶里倒恰好能装的最小石子（补丁 `miss`），这样桶的容量立刻翻倍。

**步骤**  
1. 初始化 `miss = 1`（表示我们还不能组成 `1`），`i = 0`（指向 `nums`），`patches = 0`。  
2. 当 `miss <= n` 时循环：  
   - 若 `i < len(nums)` 且 `nums[i] <= miss`，说明当前数组元素可以直接使用，`miss += nums[i]`，`i += 1`。  
   - 否则，需要补丁：`patches += 1`，`miss += miss`（相当于把 `miss` 本身加入数组）。  
3. 循环结束时，`patches` 即为最少补丁数。

#### 代码（Python）

```python
def minPatches(nums, n):
    miss = 1          # 当前最小的「未能覆盖」的正整数
    i = 0             # nums 的指针
    patches = 0       # 记录补丁数量

    # 当 miss 超过 n 时，说明 [1, n] 已经全覆盖
    while miss <= n:
        # 如果数组中还有元素且该元素不大于 miss，直接使用它
        if i < len(nums) and nums[i] <= miss:
            miss += nums[i]   # 区间右端点向右扩展
            i += 1
        else:
            # 否则补上 miss 本身，使可达区间翻倍
            patches += 1
            miss += miss       # 相当于把 miss 加入数组

    return patches
```

> 代码只用了几行，且每行都加了中文解释，直接运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(log n)`  
  - 每一次循环要么把 `miss` 翻倍，要么把数组指针向右移动一次。`miss` 最多翻倍到大于 `n`，所以循环次数不超过 `log₂ n`（大约 30 次，`n ≤ 2³¹-1`）。  
  - 用大白话说，就是**每一步都把要检查的范围砍掉一半**，所以非常快。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，不随输入规模增长，几乎不占内存。

---

## 心得  

- **核心技巧**：**贪心 + 前缀覆盖**。只维护当前能连续覆盖的最大区间 `[1, miss)`，每次都把最小缺口 `miss` 当成补丁，能让区间长度指数级增长。  
- **适用的题型**  
  1. **「最小补全」类**：如 LeetCode 330 *Patching Array*（本题）。  
  2. **「覆盖区间」类**：如 LeetCode 45 *Jump Game II*（最少跳步覆盖），LeetCode 56 *Merge Intervals*（合并区间）。  
  3. **「前缀和/前缀乘」类**：如 LeetCode 1005 *Maximize Sum Of Array After K Negations*（贪心选最小值补齐）。  
- **一句话总结**：  
  > 把“已能组成的连续区间”看成水桶的容量，每次补的都是恰好填满水桶的最小石子，让容量翻倍，步数最少。

---

## 反思  

- **第一反应**：看到“任意数的和”，自然联想到**子集求和**或**背包 DP**，于是写出暴力的 DP 解。  
- **最容易踩的坑**  
  1. **整数溢出**：`miss` 在翻倍时可能超过 Python 的整型范围（Python 自动大整数，安全），但在语言限制严格的情况下要用 64 位。  
  2. **边界条件**：`miss` 初始化为 `1`，而不是 `0`；如果数组首元素不是 `1`，必须先补 `1`。  
  3. **循环退出**：一定要用 `while miss <= n`，否则会在 `miss` 超过 `n` 时多补一次。  
- **下次遇到同类题**：  
  1. 先问自己：“我已经能连续覆盖到哪儿了？”  
  2. 判断下一个已有元素是否可以直接延伸覆盖；如果不行，就**补上当前缺口**。  

这样就能快速定位到贪心解法，避免笨重的 DP。祝你玩转算法！