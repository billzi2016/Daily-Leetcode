# #1471. 数组中最强的 k 个值 / The k Strongest Values in an Array

> 难度：中等 · 标签：Array、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/the-k-strongest-values-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr and an integer k.
A value arr[i] is said to be stronger than a value arr[j] if |arr[i] - m| > |arr[j] - m| where m is the centre of the array.
If |arr[i] - m| == |arr[j] - m|, then arr[i] is said to be stronger than arr[j] if arr[i] > arr[j].
Return a list of the strongest k values in the array. return the answer in any arbitrary order.
The centre is the middle value in an ordered integer list. More formally, if the length of the list is n, the centre is the element in position ((n - 1) / 2) in the sorted list (0-indexed).

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,4,5], k = 2
Output: [5,1]
Explanation: Centre is 3, the elements of the array sorted by the strongest are [5,1,4,2,3]. The strongest 2 elements are [5, 1]. [1, 5] is also accepted answer.
Please note that although |5 - 3| == |1 - 3| but 5 is stronger than 1 because 5 > 1.
```

**Example 2:**

```
Input: arr = [1,1,3,5,5], k = 2
Output: [5,5]
Explanation: Centre is 3, the elements of the array sorted by the strongest are [5,5,1,1,3]. The strongest 2 elements are [5, 5].
```

**Example 3:**

```
Input: arr = [6,7,11,7,6,8], k = 5
Output: [11,8,6,6,7]
Explanation: Centre is 7, the elements of the array sorted by the strongest are [11,8,6,6,7,7].
Any permutation of [11,8,6,6,7] is accepted.
```

**Constraints**

- 1 <= arr.length <= 105
- -105 <= arr[i] <= 105
- 1 <= k <= arr.length

---

## 题目（中文翻译）

给定一个整数数组 **arr** 和一个整数 **k**。  
如果对于数组的中心值 **m**（见下文定义），满足  

\[
|arr[i] - m| > |arr[j] - m|
\]

则称 **arr[i]** 比 **arr[j]** 更强（stronger）。  
当  

\[
|arr[i] - m| = |arr[j] - m|
\]

时，若 **arr[i] > arr[j]**，则仍认为 **arr[i]** 更强。

返回数组中最强的 **k** 个值，结果的顺序可以是任意的。

**中心（centre）** 的定义：先对数组进行升序排序得到已排序列表（sorted list）。设已排序列表的长度为 **n**，则中心是下标为 \(\frac{n-1}{2}\)（0‑索引）的元素。

---

## 示例

### 示例 1
**输入**  
```json
arr = [1,2,3,4,5], k = 2
```
**输出**  
```json
[5,1]
```
**解释**：中心是 3，按照强度从大到小排序后的数组为 \([5,1,4,2,3]\)。最强的 2 个元素是 \([5, 1]\)。\([1, 5]\) 也被视为合法答案。请注意，虽然 \(|5-3| = |1-3|\)，但 5 更强因为 5 > 1。

### 示例 2
**输入**  
```json
arr = [1,1,3,5,5], k = 2
```
**输出**  
```json
[5,5]
```
**解释**：中心是 3，排序后的强度序列为 \([5,5,1,1,3]\)。最强的 2 个元素是 \([5, 5]\)。

### 示例 3
**输入**  
```json
arr = [6,7,11,7,6,8], k = 5
```
**输出**  
```json
[11,8,6,6,7]
```
**解释**：中心是 7，排序后的强度序列为 \([11,8,6,6,7,7]\)。任意排列的 \([11,8,6,6,7]\) 均为正确答案。

---

## 约束条件

- \(1 \leq \text{arr.length} \leq 10^{5}\)
- \(-10^{5} \leq \text{arr}[i] \leq 10^{5}\)
- \(1 \leq k \leq \text{arr.length}\)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **先求出 centre**  
   - 把数组 `arr` 按从小到大排好序，记为 `sorted_arr`。  
   - centre 的定义是排好序后第 `((n-1)//2)` 个元素（0‑index），相当于“中间的那个人”。  

2. **计算每个数的“强度”**  
   - 强度由两层比较决定  
     1. 先看 `|arr[i] - centre|`（与 centre 的距离），距离越大越强。  
     2. 距离相同再比较数值本身，数值大的更强。  
   - 把每个元素和它的强度放在一起，形成 `(value, strength)` 的列表。  

3. **挑出最强的 k 个**  
   - 暴力的想法是：对剩下的所有元素 **一次遍历找到当前最大的强度**，把它加入答案，然后把它从列表中“删掉”。  
   - 这样重复 k 次，就得到最强的 k 个数。  

> **类比**：把 `arr` 看成一堆水果，centre 就是水果摊里“中等大小”的水果。我们要挑出“离中等大小最远，且更大的水果更抢手”。暴力做法相当于每挑一次，都要把所有水果重新排个序（线性扫描），找到那颗“最抢手”的水果。

#### 代码（Python）

```python
from typing import List

def k_strongest_bruteforce(arr: List[int], k: int) -> List[int]:
    n = len(arr)
    # 1️⃣ 排序得到 centre
    sorted_arr = sorted(arr)
    centre = sorted_arr[(n - 1) // 2]          # 中间的元素

    # 2️⃣ 计算每个数的强度，存成 (value, strength) 元组
    # strength 用一个二元组表示，先比较距离，再比较数值
    strengths = [(x, (abs(x - centre), x)) for x in arr]

    res = []                                    # 用来存答案
    for _ in range(k):                         # 重复 k 次
        # 3️⃣ 线性扫描找当前最强的元素
        max_idx = 0
        for i in range(1, len(strengths)):
            # 如果 strengths[i] 的二元组更大，就更新 max_idx
            if strengths[i][1] > strengths[max_idx][1]:
                max_idx = i
        # 把找到的最强值加入答案
        res.append(strengths[max_idx][0])
        # 把它从列表中删掉，后面的元素会左移
        strengths.pop(max_idx)

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n·k)`  
  - 每一次找最大都要遍历剩余的元素，最坏情况要遍历 `n`、`n‑1`、…、`n‑k+1` 次，近似 `n·k`。  
  - 用大白话说，就是“如果数组有 10 000 个数，而我们要找 5 000 个最强的，那大概要比对 5 000 万次”。  

- **空间复杂度**：`O(n)`  
  - 需要额外的列表 `strengths` 存每个元素的强度信息，大小和原数组一样。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈**在于每挑一个最强的数都要重新线性扫描一次，导致 `O(n·k)`。  
我们可以利用 **排序 + 双指针** 把这一步的代价压到 `O(k)`。

1. **先排序**  
   - 同样把数组排好序得到 `sorted_arr`，并求出 centre。  
   - 排序后，数组左侧的数离 centre 越远（距离大），右侧的数也同理。  

2. **双指针选最强**  
   - 设左指针 `l = 0`（指向最小的数），右指针 `r = n‑1`（指向最大的数）。  
   - 每一次比较 `sorted_arr[l]` 与 `sorted_arr[r]` 哪个更强：  
     - 先比较 `|sorted_arr[l] - centre|` 与 `|sorted_arr[r] - centre|`。  
     - 若距离相等，再比较数值本身（右边的数一定更大，因为数组已升序）。  
   - 把更强的那个放进答案，随后把对应的指针向中间收拢（`l += 1` 或 `r -= 1`）。  
   - 重复 `k` 次即可得到最强的 `k` 个数。  

> **类比**：想象把排好序的水果摆成一排，左边是最小的，右边是最大的。我们站在两端 simultaneously 看，谁离“中等大小”更远谁就先被挑走。每挑走一个，站在那一侧的手就往中间移动一步。这样只需要走 `k` 步就能把最抢手的 `k` 只水果挑完。

#### 代码（Python）

```python
from typing import List

def k_strongest(arr: List[int], k: int) -> List[int]:
    n = len(arr)
    # 1️⃣ 排序并求 centre
    arr.sort()                              # 原地排序，省空间
    centre = arr[(n - 1) // 2]

    # 2️⃣ 双指针从两端挑最强的 k 个
    l, r = 0, n - 1
    ans = []
    while len(ans) < k:
        # 计算两端元素与 centre 的距离
        left_dist = abs(arr[l] - centre)
        right_dist = abs(arr[r] - centre)

        # 如果右端更强（距离更大，或距离相同且值更大），挑右端
        if right_dist > left_dist or (right_dist == left_dist and arr[r] > arr[l]):
            ans.append(arr[r])
            r -= 1               # 右指针向左收拢
        else:
            ans.append(arr[l])
            l += 1               # 左指针向右收拢

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要花费在一次排序上，`n` 最高可达 `10⁵`，排序是 `O(n log n)`。  
  - 选出最强的 `k` 个只需要 `O(k)`（最多 `O(n)`），相对于排序可以忽略不计。  
  - 与暴力解相比，省去了每次 `O(n)` 的线性扫描，整体快了很多。  

- **空间复杂度**：`O(1)`（不计排序本身）  
  - 只用了常数个额外变量 `l, r, centre, ans`。  
  - 若把原数组视为需要额外空间，则是 `O(n)`（因为排序通常需要 `O(log n)` 递归栈），但相对于暴力的 `O(n)` 额外列表已经是最优的。  

---

## 心得  

- **核心技巧**：先排序后用“双指针”一次遍历挑选。  
- **适用场景**  
  1. 需要按照“与某个基准的距离”排序或挑选的题目（如 “最远的 k 个点”）。  
  2. “从两端选最值”类问题（如 “找出数组中最小的 k 个数” 的双指针写法）。  
- **一句话总结**：**排序后让左、右指针竞争，把离 centre 最远（且更大的）的一侧先收走，即可线性挑出最强的 k 个。**  

---

## 反思  

- **第一反应**：直接把所有元素按强度排序，然后切片前 `k`。这其实已经是最简洁的写法，但在面试里要解释时间复杂度，面试官会期待你再进一步说明可以只取 `k` 而不完整排序。  
- **最容易踩的坑**  
  - **centre 的下标**：要记得使用 `((n‑1)//2)`（整数除），否则在偶数长度时会选错位置。  
  - **距离相等时的比较**：一定要在 `right_dist == left_dist` 时再比较数值本身，否则会得到错误的强度顺序。  
  - **指针移动的条件写反**：左指针对应的是更小的数，右指针对应的是更大，记清楚谁往哪边走。  
- **下次思路**：遇到“强度”或“距离”类排序挑选，先想“**排序 + 双指针**”是否能把挑选过程降到线性，而不是一次次全局搜索。这样往往能从 `O(n·k)` 降到 `O(n log n)` 或更好。