# #2239. 寻找最接近零的数 / Find Closest Number to Zero

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/find-closest-number-to-zero/)

---

## 题目（英文原版）

**Description**

Given an integer array nums of size n, return the number with the value closest to 0 in nums. If there are multiple answers, return the number with the largest value.

**Examples**

**Example 1:**

```
Input: nums = [-4,-2,1,4,8]
Output: 1
Explanation:
The distance from -4 to 0 is |-4| = 4.
The distance from -2 to 0 is |-2| = 2.
The distance from 1 to 0 is |1| = 1.
The distance from 4 to 0 is |4| = 4.
The distance from 8 to 0 is |8| = 8.
Thus, the closest number to 0 in the array is 1.
```

**Example 2:**

```
Input: nums = [2,-1,1]
Output: 1
Explanation: 1 and -1 are both the closest numbers to 0, so 1 being larger is returned.
```

**Constraints**

- 1 <= n <= 1000
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个大小为 **n** 的整数数组（integer array）`nums`，返回数组中数值最接近 0 的数。如果存在多个答案，返回数值最大的那个。

**示例 1**  

**示例 2**  

**约束条件**  

- 1 ≤ n ≤ 1000  
- -10⁵ ≤ nums[i] ≤ 10⁵  

**示例**  

**示例 1:**  
```text
Input: nums = [-4,-2,1,4,8]
Output: 1
```
**解释:**  
- -4 到 0 的距离为 |-4| = 4。  
- -2 到 0 的距离为 |-2| = 2。  
- 1 到 0 的距离为 |1| = 1。  
- 4 到 0 的距离为 |4| = 4。  
- 8 到 0 的距离为 |8| = 8。  
因此，数组中最接近 0 的数是 **1**。

**示例 2:**  
```text
Input: nums = [2,-1,1]
Output: 1
```
**解释:**  
1 和 -1 与 0 的距离相同，故返回数值更大的 **1**。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组里每个数都和 0 的距离算出来，然后把**所有距离**两两比较，找出最小的那个。如果出现相同的最小距离，再挑选数值更大的那个。  

- **用到的数据结构**：普通的 Python 列表（list），相当于我们平常用的“一排装东西的盒子”。  
- **为什么正确**：因为我们把每一个数的距离都算出来并且两两比较，必然能找到距离最近且数值最大的那个。  
- **时间/空间复杂度**：  
  - **时间**：我们要对每个元素 `i` 再遍历所有元素 `j` 进行比较，形成两个循环，时间是 `n × n = n²`。用大白话说，就是如果数组有 10 个数，就要做 100 次比较；如果有 1000 个数，就要做 1 000 000 次比较。  
  - **空间**：只用了常数个额外变量（比如 `best`、`best_abs`），所以是 `O(1)`，也就是不随数组大小增长。

#### 代码（Python）

```python
def closest_to_zero_bruteforce(nums):
    """
    暴力解：两层循环，两两比较
    """
    n = len(nums)
    # 初始假设第一个数就是答案
    best = nums[0]
    best_abs = abs(best)

    for i in range(n):
        for j in range(i + 1, n):
            # 先算出两数各自到 0 的距离
            cur_i_abs = abs(nums[i])
            cur_j_abs = abs(nums[j])

            # 先比较距离的大小
            if cur_i_abs < cur_j_abs:
                # i 更接近 0，看看它是否比当前 best 更好
                if cur_i_abs < best_abs or (cur_i_abs == best_abs and nums[i] > best):
                    best, best_abs = nums[i], cur_i_abs
            else:
                # j 更接近 0，看看它是否比当前 best 更好
                if cur_j_abs < best_abs or (cur_j_abs == best_abs and nums[j] > best):
                    best, best_abs = nums[j], cur_j_abs

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 两层循环导致比较次数随 `n` 的平方增长，`n` 越大，耗时会急速增加。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈**在于我们不需要两两比较，只要一次遍历就能把每个数的距离和“当前最佳”进行比较即可。  

1. **遍历一次数组**：对每个元素 `x` 计算 `abs(x)`（即到 0 的距离）。  
2. **维护两个变量**：  
   - `best_abs` 保存当前最小的距离。  
   - `best` 保存对应的数值。  
3. **更新规则**：  
   - 如果 `abs(x) < best_abs`，说明 `x` 更靠近 0，直接把 `best` 换成 `x`。  
   - 如果 `abs(x) == best_abs`，说明距离相同，此时要返回**数值更大的**那个，所以只在 `x > best` 时才更新。  

这就是**单次扫描**的思路，类似于在找最大值时只走一遍数组，只是这里我们比较的是“绝对值”。  

**核心算法**：一次遍历（线性扫描） + 维护当前最优解。  

**类比**：把数组想象成一排学生站好，老师要找离教室门最近的学生。如果两个学生离门的距离相同，老师会选身高更高的（这里的“身高”对应数值大小）。老师只需要从左到右检查一次，不需要让每个学生互相比较。

#### 代码（Python）

```python
def closest_to_zero(nums):
    """
    最优解：一次遍历，实时维护距离最近且数值最大的答案
    """
    # 先把第一个元素设为初始答案
    best = nums[0]
    best_abs = abs(best)

    for x in nums[1:]:                     # 从第二个元素开始遍历
        cur_abs = abs(x)                    # 计算当前元素到 0 的距离

        # ① 距离更小 → 直接更新
        if cur_abs < best_abs:
            best, best_abs = x, cur_abs
        # ② 距离相同但数值更大 → 也要更新
        elif cur_abs == best_abs and x > best:
            best = x                       # 只需要更新数值，距离不变

    return best
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，`n` 增大时耗时线性增长。相比暴力的 `O(n²)`，速度提升非常明显。  
- **空间复杂度**：`O(1)` — 只用了几个临时变量，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：在遍历过程中**实时维护最优解**（这里是“最小绝对值且数值最大”），这是一种“贪心”思路。  
- **适用的题型**：  
  1. 找数组中绝对值最小的数（如本题）。  
  2. 在一串数字里找出现次数最多的元素（维护计数器）。  
  3. 在数组里找距离目标值最近的数（如二分搜索配合线性扫描的变体）。  
- **一句话总结**：一次遍历、比较并保存“更好”的候选，就是解这类“找最优”题目的钥匙。

---

## 反思

- **第一反应**：直接遍历数组，记录每个数到 0 的距离，遇到更小或相等且更大的数就更新。  
- **最容易踩的坑**：  
  - 忘记在距离相同的情况下返回**数值更大的**那个，导致答案错误。  
  - 忘记把第一个元素设为初始值，导致在全负数或全正数的情况下出现未初始化错误。  
- **下次类似题的第一步**：先确定“比较规则”（比如“距离更小”或“次数更多”），然后在一次遍历中实时维护满足规则的最佳候选。