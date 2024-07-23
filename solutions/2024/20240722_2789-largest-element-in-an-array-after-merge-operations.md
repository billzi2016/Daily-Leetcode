# #2789. 合并操作后数组中的最大元素 / Largest Element in an Array after Merge Operations

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/largest-element-in-an-array-after-merge-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of positive integers.
You can do the following operation on the array any number of times:
Return the value of the largest element that you can possibly obtain in the final array.

**Examples**

**Example 1:**

```
Input: nums = [2,3,7,9,3]
Output: 21
Explanation: We can apply the following operations on the array:
- Choose i = 0. The resulting array will be nums = [5,7,9,3].
- Choose i = 1. The resulting array will be nums = [5,16,3].
- Choose i = 0. The resulting array will be nums = [21,3].
The largest element in the final array is 21. It can be shown that we cannot obtain a larger element.
```

**Example 2:**

```
Input: nums = [5,3,3]
Output: 11
Explanation: We can do the following operations on the array:
- Choose i = 1. The resulting array will be nums = [5,6].
- Choose i = 0. The resulting array will be nums = [11].
There is only one element in the final array, which is 11.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的数组 **nums (array)**，其中所有元素都是正整数。  
你可以对该数组执行以下 **操作 (operation)** 任意次数：

- 选择一个下标 **i**，将 **nums[i]** 与 **nums[i+1]** 合并为它们的和 **(nums[i] + nums[i+1])**，用该和替换原来的两个元素，数组长度因此减少 **1**。

返回在 **最终数组 (final array)** 中可能得到的 **最大元素 (largest element)** 的值。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [2,3,7,9,3]
```  
**输出**  
```
21
```  
**解释**  
我们可以按如下顺序执行操作：

- 选择 `i = 0`，得到 `nums = [5,7,9,3]`（`2+3=5`）。  
- 选择 `i = 1`，得到 `nums = [5,16,3]`（`7+9=16`）。  
- 选择 `i = 0`，得到 `nums = [21,3]`（`5+16=21`）。

此时 **最终数组** 中的 **最大元素** 为 **21**。可以证明无法得到更大的元素。

#### 示例 2
**输入**  
``` 
nums = [5,3,3]
```  
**输出**  
```
11
```  
**解释**  
执行以下操作：

- 选择 `i = 1`，得到 `nums = [5,6]`（`3+3=6`）。  
- 选择 `i = 0`，得到 `nums = [11]`（`5+6=11`）。

**最终数组** 只剩一个元素 **11**，即为最大元素。

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的合并顺序都穷举**，然后记录每一种顺序最终得到的数组里最大的数，取最大值即可。  

- **数据结构**：我们可以把当前的数组当成一条链表（或者 Python 的 `list`），每次“合并”就把相邻的两个节点删掉一个，用它们的和替代左边的节点。  
- **为什么能得到正确答案**：因为我们把**所有**合法的合并顺序都尝试了一遍，答案自然不会遗漏。  
- **复杂度分析**：  
  - 对于长度为 `n` 的数组，第一次可以选择 `n‑1` 种位置合并，第二次可以选择 `n‑2` 种，依此类推，总的尝试次数是 `(n‑1)!`（阶乘），这在实际中会非常非常大。  
  - 时间复杂度记作 `O((n‑1)!)`，意思是“随着 `n` 增大，耗时会像阶乘一样飞快增长”。  
  - 每一次递归都需要保存一份当前数组，最坏情况下会占用 `O(n)` 的额外空间（递归栈 + 复制的数组）。

#### 代码（Python）

```python
def max_after_merge_bruteforce(nums):
    """
    暴力递归搜索所有合法的合并顺序
    :param nums: List[int]
    :return: 最大可能出现的元素值
    """
    # 递归结束：数组里已经没有相邻可以合并的地方
    if len(nums) == 1:
        return nums[0]

    best = max(nums)                     # 只合并不到的情况下，当前数组的最大值
    n = len(nums)

    # 枚举所有可以合并的位置 i（0 <= i < n-1）
    for i in range(n - 1):
        # 合并的前提是左边元素 <= 右边元素（题目限制）
        if nums[i] <= nums[i + 1]:
            merged = nums[:i] + [nums[i] + nums[i + 1]] + nums[i + 2:]
            # 递归求子问题的答案
            best = max(best, max_after_merge_bruteforce(merged))

    return best
```

> **注意**：这段代码只用于说明思路，实际运行会在 `n ≈ 15` 时就卡死，远远达不到题目要求的 `10⁵` 规模。

#### 复杂度  

- **时间复杂度**：`O((n‑1)!)` —— 随着数组长度稍微增长，计算量就会呈阶乘级别爆炸。  
- **空间复杂度**：`O(n)` —— 递归栈的深度最多 `n`，每层会复制一份数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈在于大量的重复搜索**。我们需要找出合并操作的“规律”，把它转化为一次线性扫描就能得到答案的形式。

**观察 1：合并的唯一限制是左边的数必须 ≤ 右边的数**。  
合并后得到的新数 `a+b` 一定比右边的数 `b` 大（因为 `a` 为正），所以**合并后这个新数几乎总是可以继续向左合并**，只要左边的原始数不大于它。

**观察 2：如果我们从右往左遍历数组**，维护一个“当前可以合并得到的总和 `cur`”。  
- 初始时 `cur = nums[-1]`（最右边的元素只能自己形成一个段）。  
- 向左看第 `i` 个元素 `nums[i]`：  
  - **如果 `nums[i] <= cur`**，说明它可以和右边的段合并，新的段和变成 `cur + nums[i]`。  
  - **否则**，它太大，根本合不进右边的段，这时候右边的段已经“封闭”，它的和 `cur` 就是一个**候选的最大值**，我们把 `cur` 与全局最大值比较后，重新把 `cur` 设为 `nums[i]`，开启一个新的段。

这样我们把整个数组划分成若干**不可再向左合并的段**，每个段的和就是一次“最终可能出现的最大元素”。答案就是这些段和的最大值。

**为什么这样是最优的？**  
- 每一次合并只会让左边的数变大（因为加上了右边的正数），所以**只要左边的原始数不超过已经合并好的右段和，就一定能合并**。  
- 只要出现 `nums[i] > cur`，左边的这个数永远不可能和右边的任何元素合并（因为右边的所有元素在合并后形成的数只会更大），所以我们必须把它留在独立的段里。  
- 这正是**贪心**的思路：每次都尽可能把左边的数合进右边的段，除非根本做不到。

**核心算法**：一次线性扫描（O(n)），只使用常数个变量（O(1) 空间）。

#### 代码（Python）

```python
def largest_element_after_merge(nums):
    """
    贪心 + 单次遍历求最大可能出现的元素
    :param nums: List[int]，正整数数组
    :return: int，最大的可达元素值
    """
    # 从右往左维护当前可以合并成的段的和
    cur = nums[-1]          # 最右边的元素先形成一个段
    ans = cur                # 当前已知的最大段和

    # 逆序遍历除了最后一个元素之外的所有位置
    for i in range(len(nums) - 2, -1, -1):
        if nums[i] <= cur:
            # 可以合并：把左边的数加入当前段
            cur += nums[i]
        else:
            # 不能合并：当前段已经封闭，更新答案
            ans = max(ans, cur)
            # 重新开启新段，以当前元素为起点
            cur = nums[i]

    # 循环结束后，最后一个段仍未比较，需要再更新一次
    ans = max(ans, cur)
    return ans
```

> **关键行解释**  
> - `if nums[i] <= cur:` ← 判断左边的数能否“塞进”右边已经合并好的段。  
> - `cur += nums[i]` ← 合并成功后，段的总和变大。  
> - `ans = max(ans, cur)` ← 每当出现合并阻塞，说明一个完整的段已经形成，更新全局最大值。  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，所谓 `O(n)` 就是“工作量随元素个数线性增长”，比如 `n=10000` 时大约需要走一万步，完全可接受。  
- **空间复杂度**：`O(1)` —— 只用了几个整型变量 (`cur`, `ans`)，不随 `n` 增长。  

---

## 心得  

- **核心技巧**：**从右往左的贪心合并**，利用“左 ≤ 右”这个限制，把数组划分成若干不可再向左合并的段，最大段和即为答案。  
- **适用题型**：  
  1. “只能在满足某个局部条件时合并相邻元素”的数组题（如本题）。  
  2. “把数组划分成若干段，使每段满足单调或大小关系，求某种极值”的问题（如 “分割数组的最大子段和”）。  
- **一句话总结**：**只要左边的数不大于右边已经合并好的总和，就一定能合并——所以从右向左不断累加，遇阻就记录最大**。

---

## 反思  

- **第一反应**：看到“可以任意次数合并”，自然想到**暴力搜索所有顺序**，但很快发现 `n` 可能高达 `10⁵`，这显然不可行。  
- **最容易踩的坑**：  
  - 忘记**合并的前提条件** `nums[i] <= nums[i+1]`，直接把所有相邻数都相加会得到总和 `24`（错误答案）。  
  - 处理边界时漏掉了最后一个段的比较，需要在循环结束后再 `max` 一次。  
- **下次类似题目第一步**：**先写出合并的局部条件，尝试从一端（通常是右端）把条件转化为“能否继续累加”，看能否用一次线性扫描完成**。这样往往能迅速发现贪心或单调栈/双指针的切入点。