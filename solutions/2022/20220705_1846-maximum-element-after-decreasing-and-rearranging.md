# #1846. 最大元素在递减和重新排列后的值 / Maximum Element After Decreasing and Rearranging

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers arr. Perform some operations (possibly none) on arr so that it satisfies these conditions:
There are 2 types of operations that you can perform any number of times:
Return the maximum possible value of an element in arr after performing the operations to satisfy the conditions.

**Examples**

**Example 1:**

```
Input: arr = [2,2,1,2,1]
Output: 2
Explanation: 
We can satisfy the conditions by rearranging arr so it becomes [1,2,2,2,1].
The largest element in arr is 2.
```

**Example 2:**

```
Input: arr = [100,1,1000]
Output: 3
Explanation: 
One possible way to satisfy the conditions is by doing the following:
1. Rearrange arr so it becomes [1,100,1000].
2. Decrease the value of the second element to 2.
3. Decrease the value of the third element to 3.
Now arr = [1,2,3], which satisfies the conditions.
The largest element in arr is 3.
```

**Example 3:**

```
Input: arr = [1,2,3,4,5]
Output: 5
Explanation: The array already satisfies the conditions, and the largest element is 5.
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个只包含正整数的数组 `arr`。你可以对 `arr` 执行任意次数（包括 0 次）以下两类操作：

1. **重新排列**（rearrange）：任意调换数组中元素的顺序。  
2. **递减**（decrease）：将任意元素的值减小为任意正整数（但不能增大），即把 `arr[i]` 改为任意满足 `1 ≤ newVal ≤ arr[i]` 的整数。

在完成若干操作后，数组必须满足如下条件：

- 对于排序后的数组（下标从 0 开始），第 `i` 个位置的元素 `arr[i]` 必须 **不大于** `i + 1`，即 `arr[i] ≤ i + 1`。

在满足上述条件的前提下，求 **数组中可能出现的最大元素值的上限**（即所有可行方案中最大的 `arr[i]`），并返回该最大值。

**示例**  

*示例 1*  
```
Input: arr = [2,2,1,2,1]
Output: 2
Explanation: 
我们可以先重新排列，使数组变为 [1,2,2,2,1]。此时每个位置的元素均满足 ≤ i+1 的要求，数组中的最大元素为 2。
```

*示例 2*  
```
Input: arr = [100,1,1000]
Output: 3
Explanation: 
一种可行的操作序列如下：
1. 重新排列得到 [1,100,1000]；
2. 将第二个元素递减至 2；
3. 将第三个元素递减至 3。  
此时数组为 [1,2,3]，满足条件，最大元素为 3。
```

*示例 3*  
```
Input: arr = [1,2,3,4,5]
Output: 5
Explanation: 
原数组已经满足条件，最大元素为 5。
```

**约束条件**  

- `1 ≤ arr.length ≤ 10^5`
- `1 ≤ arr[i] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的操作都穷举一遍：

1. **排列**：把数组 `arr` 的元素随意换位（相当于把数组的下标和数值对应关系全部重新配对）。  
   - 类比：把一堆书随意摆放在书架上，每本书都可以放在任意位置，就像把「键」换成「值」的过程。  
2. **递减**：对每本书的厚度（即数值）任意减小，但不能减到 0（题目要求正整数）。  
   - 类比：把一本厚书的页数撕掉几页，只能撕掉，不能往回加页。

把所有排列和所有可能的递减组合列举出来，检查哪一种满足「第 i 本书的厚度 ≤ i+1」的条件，然后记录下其中的最大厚度。

**为什么这样一定能得到答案**  
因为我们把所有合法的「排列 + 递减」都尝试了一遍，只要有一种办法能得到更大的最大值，就一定会在枚举的过程中被发现。

**为什么不可取**  
- **排列数目**：长度为 `n` 的数组有 `n!`（阶乘）种排列，`n` 甚至只有 10 时 `10! = 3,628,800`，已经非常大；而 `n` 可达 `10^5`，根本不可能遍历。  
- **递减方式**：每个元素可以减到 `1` 到原值之间的任意整数，组合数更是指数级增长。  

**时间/空间复杂度**  
- 时间复杂度：`O(n! * something)`，在实际中会因为 `n!` 超出计算能力而直接超时。  
- 空间复杂度：`O(n)`（保存一次排列的空间），但由于时间已经不可接受，空间也不值得讨论。

> **大白话解释**：`O(n!)` 就像让 20 个人排队，所有可能的排法有 20!（≈2.4×10¹⁸）种，你根本不可能一个一个试完。

#### 代码（Python）

下面的代码只是演示“暴力”思路，**只能在 n ≤ 8 的极小数据上跑通**，请不要在正式提交时使用。

```python
import itertools

def max_element_bruteforce(arr):
    """
    暴力枚举所有排列 + 所有递减方式（这里递减直接取最小可能的 1）
    只用于教学演示，复杂度极高，实际不可用。
    """
    best = 0
    # 1) 枚举所有排列
    for perm in itertools.permutations(arr):
        # 2) 对每个位置 i，尝试把该数递减到 1~perm[i] 之间的任意值
        # 为了简化，只取递减到 i+1（满足条件的最大可能值）或更小的 1
        ok = True
        cur_max = 0
        for i, val in enumerate(perm):
            # 需要满足 arr[i] <= i+1，最多只能递减到 i+1
            allowed = min(val, i + 1)
            if allowed < 1:          # 递减后变成非正数，非法
                ok = False
                break
            cur_max = max(cur_max, allowed)
        if ok:
            best = max(best, cur_max)
    return best

# 示例（只能跑很小的数组）
print(max_element_bruteforce([2, 2, 1, 2, 1]))   # 2
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`（遍历所有排列，每个排列线性检查），在实际中几乎不可运行。  
- **空间复杂度**：`O(n)`（保存一次排列），与时间复杂度相比不重要。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**排列**其实不需要穷举：只要把数组 **从小到大排序**，我们就已经得到一种“最有利”的顺序。  
原因：

- 递减只能让数变小，**把大数放在后面**（对应更大的下标）能够让它们有更大的“容忍度”。  
- 这和把一本厚书放在靠后的位置（第 i+1 本书）更容易满足「厚度 ≤ i+1」的要求是一致的。

**核心瓶颈**：在排好序之后，仍然需要决定每个位置到底要把原来的数递减到多少。  
观察一下排好序的数组 `a[0] ≤ a[1] ≤ … ≤ a[n-1]`：

- 对第 `0` 本书（下标 0），它的最大允许厚度是 `1`（因为 `i+1 = 1`），只要原数 `a[0] ≥ 1`（必然成立），我们就可以把它调到 **1**。  
- 对第 `1` 本书，最大允许厚度是 `2`，但如果原数 `a[1]` 本来只有 `1`，我们只能把它调到 `1`（不能强行变成 `2`），于是此时**最大值仍是 1**。  
- 对第 `2` 本书，最大允许厚度是 `3`，如果 `a[2] ≥ 3`，我们就可以把它调到 `3`，否则只能调到 `a[2]`。

可以发现，一个**递增的目标值** `cur`（代表当前已经能够达到的最大厚度）在遍历数组时只会 **最多加 1**。  
具体的更新规则：

```
cur = 0                     # 目前已成功构造的最大厚度（初始为 0）
for each value a in sorted(arr):
    # 我们希望把当前这本书的厚度设为 cur+1（比之前的最大厚度大 1）
    # 但它不能超过原来的厚度 a，故实际能设的最大值是 min(a, cur+1)
    cur = min(a, cur + 1)
```

遍历完所有元素后，`cur` 就是**可以得到的最大元素值**。

**为什么这一步是最优的**  

- `cur+1` 是“下一个可能的更大值”。如果当前的原数 `a` 连这个值都达不到（`a < cur+1`），我们只能把它调到 `a`，`cur` 不会增长。  
- 如果 `a` 足够大（`a ≥ cur+1`），我们立刻把它调到 `cur+1`，这样 **每一步都尽可能让最大值增长 1**，不会浪费任何“大数”。  
- 由于我们是 **从小到大** 处理，任何后面的数都不可能帮助前面的位子再增长，因为前面的位子已经被最小的数“锁住”了。  

因此，这个贪心过程得到的 `cur` 是全局最优的。

#### 代码（Python）

```python
def maximumElementAfterDecreasingAndRearranging(arr):
    """
    贪心 + 排序
    思路：
        1. 将数组升序排列，确保“小数”在前，“大数”在后。
        2. 用 cur 记录当前已经能够实现的最大值。
        3. 对每个数 a，尝试把它调到 cur+1（比已有最大值大 1），
           受限于原数大小，只能取 min(a, cur+1)。
        4. 循环结束后 cur 即为答案。
    时间复杂度：O(n log n)   （排序）
    空间复杂度：O(1)  （原地排序或额外 O(n) 的临时列表）
    """
    arr.sort()                     # 1. 升序排列
    cur = 0                        # 已经成功构造的最大厚度
    for a in arr:                  # 2. 逐个处理
        # 期望把当前元素调到 cur+1，但不能超过它本身的大小
        cur = min(a, cur + 1)      # 3. 贪心更新
    return cur                     # 4. 最终的最大可能值


# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(maximumElementAfterDecreasingAndRearranging([2, 2, 1, 2, 1]))  # 2
    print(maximumElementAfterDecreasingAndRearranging([100, 1, 1000]))   # 3
    print(maximumElementAfterDecreasingAndRearranging([1, 2, 3, 4, 5])) # 5
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `n log n`（常规比较排序的代价），随后一次线性遍历 `O(n)`，两者相加仍是 `O(n log n)`。  
  - 与暴力解的 `O(n!)` 相比，`n log n` 在 `n = 10^5` 时也只需几毫秒到几百毫秒，完全可以接受。

- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（Python 的 `list.sort()` 可能使用额外的临时空间），但都远低于暴力解的 `O(n)` 并且不随指数增长。

> **大白话**：`O(n log n)` 就像把 100,000 本书先排好序（花点时间），然后一次过检查每本书能否放在对应位置，整个过程只需要“几次翻页”，不会像暴力那样“把每本书搬来搬去无止境”。  

---

## 心得

- **核心技巧**：**先排序、后贪心**——把“小的先放前面”，再让每个位置尽可能“递增 1”。  
- **适用场景**：  
  1. 需要 **“每个位置的值 ≤ 位置编号”**（或类似的上界）且只能 **递减**的题目。  
  2. “最大化可达的序号/层数”这类 **从 1 开始递增** 的构造问题。  
  3. 类似的 LeetCode 题目还有  
     - *"Maximum Length of Pair Chain"*（用贪心排序构造最长链）  
     - *"Can Make Palindrome from Substring"*（先排序后贪心配对）  

- **一句话总结**：**把数组升序后，让每个元素尽可能取 “前一个元素+1” 的值，受原数限制的最小值即为答案**。

---

## 反思

- **第一反应**：直接想遍历所有排列和递减方式（暴力），因为题目说“可以任意重新排列并递减”。  
- **最容易踩的坑**  
  1. **忘记排序**：直接按原顺序贪心会导致大数被提前使用，失去后面位置的“容忍度”。  
  2. **漏掉下界**：递减后数值必须保持正整数，`min(a, cur+1)` 中的 `cur+1` 必须从 1 开始，否则会得到 0。  
  3. **特殊情况**：数组全是 `1` 时，答案只能是 `1`（因为后面的 `cur+1` 会被 `min(1, cur+1)` 卡住）。  

- **下次思路**：一看到“可以重新排列 + 只能递减”，第一步就**考虑排序**，随后检查“每个位置的上限”是否随下标线性增长，从而尝试 **“贪心让值尽可能增长 1”** 的思路。这样可以快速跳过暴力的陷阱，直达最优解。