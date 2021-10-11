# #1509. 三次操作后最大值与最小值的最小差值 / Minimum Difference Between Largest and Smallest Value in Three Moves

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
In one move, you can choose one element of nums and change it to any value.
Return the minimum difference between the largest and smallest value of nums after performing at most three moves.

**Examples**

**Example 1:**

```
Input: nums = [5,3,2,4]
Output: 0
Explanation: We can make at most 3 moves.
In the first move, change 2 to 3. nums becomes [5,3,3,4].
In the second move, change 4 to 3. nums becomes [5,3,3,3].
In the third move, change 5 to 3. nums becomes [3,3,3,3].
After performing 3 moves, the difference between the minimum and maximum is 3 - 3 = 0.
```

**Example 2:**

```
Input: nums = [1,5,0,10,14]
Output: 1
Explanation: We can make at most 3 moves.
In the first move, change 5 to 0. nums becomes [1,0,0,10,14].
In the second move, change 10 to 0. nums becomes [1,0,0,0,14].
In the third move, change 14 to 1. nums becomes [1,0,0,0,1].
After performing 3 moves, the difference between the minimum and maximum is 1 - 0 = 1.
It can be shown that there is no way to make the difference 0 in 3 moves.
```

**Example 3:**

```
Input: nums = [3,100,20]
Output: 0
Explanation: We can make at most 3 moves.
In the first move, change 100 to 7. nums becomes [3,7,20].
In the second move, change 20 to 7. nums becomes [3,7,7].
In the third move, change 3 to 7. nums becomes [7,7,7].
After performing 3 moves, the difference between the minimum and maximum is 7 - 7 = 0.
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`。  
一次操作中，你可以选择 `nums` 中的任意一个元素，并将其更改为任意值。  
返回在至多进行 **三次操作**（at most three moves）后，`nums` 的最大值与最小值之间的最小可能差值。

**示例**  

**示例 1**  
```
Input: nums = [5,3,2,4]
Output: 0
Explanation: 我们最多可以进行 3 次操作。
- 第一次操作，将 2 改为 3。数组变为 [5,3,3,4]。
- 第二次操作，将 4 改为 3。数组变为 [5,3,3,3]。
- 第三次操作，将 5 改为 3。数组变为 [3,3,3,3]。
完成 3 次操作后，最大值与最小值的差为 3 - 3 = 0。
```

**示例 2**  
```
Input: nums = [1,5,0,10,14]
Output: 1
Explanation: 我们最多可以进行 3 次操作。
- 第一次操作，将 5 改为 0。数组变为 [1,0,0,10,14]。
- 第二次操作，将 10 改为 0。数组变为 [1,0,0,0,14]。
- 第三次操作，将 14 改为 1。数组变为 [1,0,0,0,1]。
完成 3 次操作后，最大值与最小值的差为 1 - 0 = 1。
可以证明不存在更小的差值。
```

**示例 3**  
```
Input: nums = [3,100,20]
Output: 0
Explanation: 我们最多可以进行 3 次操作。
- 第一次操作，将 100 改为 7。数组变为 [3,7,20]。
- 第二次操作，将 20 改为 7。数组变为 [3,7,7]。
- 第三次操作，将 3 改为 7。数组变为 [7,7,7]。
完成 3 次操作后，最大值与最小值的差为 7 - 7 = 0。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把能改的至多 3 个数全部列举出来，尝试每一种改法，看最后的最大值与最小值差是多少，取最小的那一个**。  
这相当于下面两步：

1. **选取要改的下标**  
   - 可以改 0、1、2、3 个数。  
   - 对于每一种改动的个数，枚举所有可能的下标组合（组合数用 C(n,k) 表示），比如 n=5，改 2 个数就有 `C(5,2)=10` 种选法。  

2. **为选中的下标赋任意值**  
   - 只要把这些位置的数改成 **任意** 的整数，就能让它们不再影响最大/最小差值。最好的办法是把它们改成 **数组中剩下的数的最小值或最大值**，甚至直接改成同一个数。  
   - 为了穷举，我们可以把改动后的数设为 `-inf`（极小）或 `+inf`（极大），然后再重新计算剩余元素的最大最小值。  

这个思路一定能得到正确答案，因为我们把**所有可能的改动**都考虑到了。  

**为什么会对？**  
- 题目只限制改动次数（≤3），没有限制改成什么值。只要我们把要改的数改成一个“足够极端”的值，就等价于“把这些数从原数组中去掉”，因为它们不再决定最终的最大或最小。  
- 因此暴力枚举所有“去掉”最多 3 个元素的情况，就能得到最小可能的差值。  

**时间/空间复杂度**  
- 枚举 0~3 个下标的组合数是 `C(n,0)+C(n,1)+C(n,2)+C(n,3)`，在最坏情况下约等于 `O(n^3)`（因为 `C(n,3) = n·(n-1)·(n-2)/6`）。  
- 对每个组合，我们要遍历一次数组求最大最小，时间是 `O(n)`。  
- 综合下来是 **O(n^4)**，这在 n 可达 `10^5` 时根本跑不动。  
- 空间只用到常数级别的临时变量，**O(1)**。  

下面给出可以直接运行的暴力代码（仅作思路演示，实际提交会超时）。

#### 代码（Python）

```python
import itertools
from typing import List

def minDifference_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # 最多改 3 次，枚举改 0、1、2、3 个元素的所有下标组合
    best = float('inf')
    for k in range(0, min(3, n) + 1):          # k 表示要改的元素个数
        for idxs in itertools.combinations(range(n), k):
            # 把选中的位置设为极端值，使它们不影响 max/min
            # 这里直接把它们设为 None，后面统计时跳过
            tmp = [nums[i] for i in range(n) if i not in idxs]
            if not tmp:                        # 全部被改掉了，差值为 0
                return 0
            cur_diff = max(tmp) - min(tmp)
            best = min(best, cur_diff)
    return best

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    print(minDifference_bruteforce([5, 3, 2, 4]))          # 0
    print(minDifference_bruteforce([1, 5, 0, 10, 14]))    # 1
    print(minDifference_bruteforce([3, 100, 20]))        # 0
```

> **关键注释**  
> - `itertools.combinations` 用来生成所有「选中下标」的组合，就像把一堆水果挑出来装进篮子。  
> - 把选中的位置直接从数组里剔除（`if i not in idxs`），等价于把它们改成「不影响」最大最小的值。  

#### 复杂度  

- **时间复杂度**：`O(n^4)`  
  - `C(n,3)` 约等于 `n³/6`，每个组合又要遍历一次数组 `O(n)`，所以总体是 `O(n⁴)`。  
  - 用大白话说，就是如果数组有 10 万个元素，算法要做 **10⁴⁰** 次操作，根本不可能在一秒内跑完。  

- **空间复杂度**：`O(1)`（不计递归栈和 itertools 生成的迭代器本身）  
  - 只用了几个临时变量，和数组大小无关。  

---

### 2. 最优解  

#### 思路  

从暴力解我们得到的“**把最多 3 个元素从数组中‘去掉’**”的等价关系入手。  
真正的难点在于**怎样快速找出去掉哪几个元素可以让剩余部分的最大值与最小值差最小**。  

**观察 1：**  
- 把一个数改成极小或极大后，它只会影响 **最小值** 或 **最大值**，不会同时影响两者。  
- 因此，最优的改动一定是：**把最小的几个数或最大的几个数改掉**（或者两者各一点），而不会去掉中间的数。  

**观察 2：**  
- 改动次数上限是 3。于是我们只需要考虑以下四种“去除方案”：

| 方案 | 去掉最小的多少个 | 去掉最大的多少个 |
|------|----------------|-------------------|
| 0    | 0              | 3 |
| 1    | 1              | 2 |
| 2    | 2              | 1 |
| 3    | 3              | 0 |

- 其余的元素保持不变，差值就是 **剩余数组的最大值 - 最小值**。  

**如何快速得到这些值？**  
- 先把数组**从小到大排序**。排序后，第 `i` 小的元素就是 `sorted[i]`，第 `j` 大的元素就是 `sorted[n-1-j]`。  
- 对每种方案，直接取对应的下标即可得到差值。  

**整体步骤**  

1. **如果数组长度 ≤ 4**，直接把所有数改成同一个值，差值必为 0。  
2. 对数组进行**升序排序**（时间 `O(n log n)`）。  
3. 枚举 `i = 0..3`，其中 `i` 表示去掉最小的 `i` 个数，`3-i` 表示去掉最大的 `3-i` 个数。  
4. 计算 `current = sorted[n-1-(3-i)] - sorted[i]`，更新答案的最小值。  

**为什么只需要这四种情况？**  
- 设想我们把最小的 `a` 个数和最大的 `b` 个数改掉，且 `a+b ≤ 3`。  
- 若 `a > 3` 或 `b > 3`，显然超过了改动上限。  
- 如果 `a+b < 3`，我们可以再随意改掉任意一个中间元素（对差值没有影响），所以最优解一定落在 `a+b = 3` 的情况上。  
- 因此只需枚举 `a = 0,1,2,3`（对应 `b = 3-a`），共四种可能。  

**类比**：把数组想成一排排书，想让最高和最低的书之间的高度差最小，只能把最左边几本（最小值）或最右边几本（最大值）搬走，最多搬走三本。搬走中间的书并不能让两端的高度更接近。  

#### 代码（Python）

```python
from typing import List

def minDifference(nums: List[int]) -> int:
    n = len(nums)
    # 长度不超过 4 时，全部改成同一个数即可，差值为 0
    if n <= 4:
        return 0

    # 1. 排序，时间 O(n log n)
    nums.sort()                     # 升序

    # 2. 枚举去掉 i 个最小值，3-i 个最大值的四种情况
    ans = float('inf')
    for i in range(4):              # i = 0,1,2,3
        # 剩余数组的最小值是 nums[i]
        # 剩余数组的最大值是 nums[n-1-(3-i)]
        cur_diff = nums[n - 1 - (3 - i)] - nums[i]
        ans = min(ans, cur_diff)

    return ans

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    print(minDifference([5, 3, 2, 4]))          # 0
    print(minDifference([1, 5, 0, 10, 14]))    # 1
    print(minDifference([3, 100, 20]))        # 0
```

> **关键注释**  
> - `nums.sort()`：把数组排好序，就像把一堆弹珠从小到大排成一行，后面只需要看两头就能知道最大/最小。  
> - `nums[n - 1 - (3 - i)]`：`3-i` 表示要去掉的最大元素个数，`n-1-(3-i)` 正好是“剩下的最大元素”的下标。  
> - 循环只跑 4 次，时间几乎可以忽略不计。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要耗时在排序，`n` 最多 `10⁵`，`log n` 约为 17，完全可以在一秒内完成。  
  - 与暴力解的 `O(n⁴)` 相比，快了 **指数级**（从 10⁴⁰ 降到 10⁶ 左右）。  

- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（Python 的 Timsort 会额外使用少量临时空间），但都不随 `n` 的指数增长。  

---

## 心得  

- **核心技巧**：**把“最多 K 次改动”转化为“从数组两端去掉最多 K 个元素”**，并利用排序后直接取下标的方式求解。  
- **适用的题型**  
  1. “删除最多 K 个元素后，使数组的范围（max‑min）最小”——如本题、LeetCode 1509 *Minimum Difference Between Largest and Smallest Value in Three Moves*（本题）。  
  2. “在 K 次操作后，使数组的中位数/均值最大/最小”——思路类似，常用排序 + 双指针。  
  3. “删除 K 条边后，图的直径最小”——在一维（排序）情形下的对应思路。  
- **一句话总结**：**把可改动的次数当成“可以抹去”两端的元素数量，排序后只需检查四种端点组合即可**。  

---

## 反思  

- **第一反应**：看到“最多三次改动”，立刻想到枚举所有改动方式（暴力），但很快意识到数组长度可达 10⁵，枚举不可行。  
- **最容易踩的坑**  
  - 忘记处理 `len(nums) ≤ 4` 的特殊情况，会导致访问越界。  
  - 在计算差值时写错下标，例如 `nums[n-1-(3-i)]` 写成 `nums[n-(3-i)]`，会少算一个元素。  
  - 把“改成任意值”误认为只能改成数组中已有的值，实际上可以直接把它们视作被“移除”。  
- **下次遇到同类题**：第一步先**思考是否可以把有限次的改动等价为“去掉”几端的元素**，如果能，就立刻排序并枚举端点的组合，而不是盲目枚举所有改动。