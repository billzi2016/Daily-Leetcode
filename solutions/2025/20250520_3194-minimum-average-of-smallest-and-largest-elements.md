# #3194. 最小的最大与最小元素的平均值 / Minimum Average of Smallest and Largest Elements

> 难度：简单 · 标签：Array、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-average-of-smallest-and-largest-elements/)

---

## 题目（英文原版）

**Description**

You have an array of floating point numbers averages which is initially empty. You are given an array nums of n integers where n is even.
You repeat the following procedure n / 2 times:
Return the minimum element in averages.

**Examples**

**Example 1:**

```
Input: nums = [7,8,3,4,15,13,4,1]
Output: 5.5
Explanation:
```

**Example 2:**

```
Input: nums = [1,9,8,3,10,5]
Output: 5.5
Explanation:
```

**Example 3:**

```
Input: nums = [1,2,3,7,8,9]
Output: 5.0
Explanation:
```

**Constraints**

- 2 <= n == nums.length <= 50
- n is even.
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

你有一个初始为空的浮点数数组 `averages`（array）。现在给定一个长度为 `n` 的整数数组 `nums`，其中 `n` 为偶数。  
你需要重复下面的过程 `n / 2` 次：

- （过程内容在原题中未给出，仅保留原句）  
- 返回 `averages` 中的最小元素。

**示例 1：**  
输入: `nums = [7,8,3,4,15,13,4,1]`  
输出: `5.5`  
说明:  

**示例 2：**  
输入: `nums = [1,9,8,3,10,5]`  
输出: `5.5`  
说明:  

**示例 3：**  
输入: `nums = [1,2,3,7,8,9]`  
输出: `5.0`  
说明:  

**约束条件：**  
- `2 <= n == nums.length <= 50`  
- `n` 为偶数。  
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步一步模拟题目描述的过程**：

1. 把 `averages` 初始化为空列表。  
2. 重复 `n/2` 次（`n` 为 `nums` 的长度）  
   - 在当前的 `nums` 中**找出最小值** `min_val`（相当于在字典里查最小的键）。  
   - 再**找出最大值** `max_val`（相当于在字典里查最大的键）。  
   - 计算它们的平均数 `(min_val + max_val) / 2`，放进 `averages`。  
   - 把这两个数从 `nums` 中删掉（相当于把这两本书从书架上搬走）。  

3. 循环结束后，`averages` 中已经存了所有 `n/2` 次的平均值，**返回最小的那个** 即可。

> **为什么正确**  
> 题目要求每一次都取当前剩余数组的最小和最大元素配对，求平均并保存。我们正是按这个规则一步步操作，最终得到的 `averages` 与题目要求完全一致。

> **时间/空间复杂度**  
> - 每一次找最小值和最大值都要遍历一次数组，时间是 `O(current_len)`。  
> - 第一次遍历 `n` 次，第二次遍历 `n-2` 次，……，总共大约 `n + (n-2) + … + 2 = O(n²)`。  
> - 我们在原地删除元素（用 `pop`），额外的存储只有 `averages`，大小为 `n/2`，所以空间是 `O(n)`（实际上是 `O(n/2)`，简化写 `O(n)`）。

#### 代码（Python）

```python
def minimum_average_bruteforce(nums):
    """
    暴力模拟：每次线性扫描找最小/最大，配对求平均。
    """
    nums = nums[:]                     # 复制一份，防止修改原数组
    averages = []                      # 用来保存每一次的平均值

    # 需要配对 n/2 次
    for _ in range(len(nums) // 2):
        # 找最小值及其下标
        min_val = min(nums)
        min_idx = nums.index(min_val)

        # 找最大值及其下标
        max_val = max(nums)
        max_idx = nums.index(max_val)

        # 计算平均数并加入列表
        averages.append((min_val + max_val) / 2)

        # 为了不影响后面的索引，先删除下标大的那个
        # （否则删除前面的会导致后面的下标变化）
        if min_idx > max_idx:
            nums.pop(min_idx)
            nums.pop(max_idx)
        else:
            nums.pop(max_idx)
            nums.pop(min_idx)

    # 返回所有平均值中的最小值
    return min(averages)
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 直观理解就是“每次都要把整条队伍从头到尾检查一次”，随着 `n` 增大，工作量呈二次增长。  
- **空间复杂度**：`O(n)` —— 需要额外的 `averages` 列表保存 `n/2` 个平均值，另外还有复制的 `nums`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历整个数组去找最小/最大**。如果我们事先把数组**排好序**，最小和最大就天然出现在两端，**不需要再遍历**。

1. **先排序**：`nums.sort()`，时间 `O(n log n)`（排序算法的常规复杂度）。  
2. 使用**双指针**：  
   - `left` 指向最左边（最小），`right` 指向最右边（最大）。  
   - 每一次把 `nums[left]` 与 `nums[right]` 配对，计算平均数。  
   - 移动指针 `left += 1, right -= 1`，继续配对下一个最小/最大。  
3. 在配对的过程中**实时记录最小的平均值**，不必再把所有平均值存进列表，省去额外空间。  

> **为什么这样就对了**  
> 排序后，数组的顺序已经是从小到大。第 `i` 小的元素必然和第 `i` 大的元素配对（即 `nums[i]` 与 `nums[n-1-i]`），这正好满足“每一步取当前最小和最大”。因为我们一次性把所有配对都算完，**结果与逐步删除的过程完全等价**。

> **核心数据结构**  
> - **排序**：把一堆乱糟糟的数字排成有序的队列，类似把书按照字母顺序摆好，查找最前/最后一本书就变得非常快。  
> - **双指针**：两个手指分别从队列的两端向中间走，每走一步就完成一次配对。  

> **时间/空间复杂度**  
> - 排序 `O(n log n)`，配对只需要一次线性遍历 `O(n)`，整体仍是 `O(n log n)`。  
> - 只使用常数级额外变量（指针、最小平均值），空间是 `O(1)`。

#### 代码（Python）

```python
def minimum_average(nums):
    """
    最优解：先排序，再用双指针配对，直接追踪最小平均值。
    """
    nums.sort()                       # O(n log n) 的排序
    left, right = 0, len(nums) - 1    # 双指针分别指向最小和最大
    min_avg = float('inf')            # 初始设为正无穷，方便取最小

    while left < right:               # 只需要配对 n/2 次
        avg = (nums[left] + nums[right]) / 2   # 计算当前配对的平均值
        if avg < min_avg:                         # 更新最小平均值
            min_avg = avg
        left += 1                     # 左指针向右移动
        right -= 1                    # 右指针向左移动

    return min_avg
```

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 主要耗时在排序，配对过程是线性 `O(n)`，不影响总体阶数。相对于暴力解的 `O(n²)`，速度提升明显。  
- **空间复杂度**：`O(1)` —— 只用了几个整数和一个浮点数变量，未额外占用与输入规模相关的空间。

---

## 心得

- **核心技巧**：先排序，再用双指针从两端配对，能够把“每次都要找最值”的操作降到 `O(1)`，整体复杂度受限于排序 `O(n log n)`。  
- **适用的题型**  
  1. “配对求和/平均最小值” 类似题目，如 **Minimum Sum of Two Numbers**（求配对后最小的和）。  
  2. “两数之和最接近目标” 类似题目，如 **Two Sum Less Than K**（使用双指针）。  
  3. “数组两端配对” 的变形，如 **Maximum Distance Between Two Arrays**（同样用排序 + 双指针）。  
- **一句话总结**：**把数组排好序，最小和最大自然在两端，双指针一次遍历即可完成全部配对**。

---

## 反思

- **第一反应**：直接把题目描述的“取最小、取最大、求平均”写成循环，没想到可以先排序。  
- **最容易踩的坑**  
  - 忘记把 `left`、`right` 的移动条件写成 `left < right`（否则会在中间重复配对）。  
  - 计算平均数时要使用浮点除法 `/`，否则在 Python 整除 `//` 会丢失小数。  
  - 边界：数组长度一定是偶数，若忘记这一点，`left == right` 时不应再配对。  
- **下次类似题的第一步**：**先思考是否可以通过排序把“最值”直接定位**，如果可以，就立刻用双指针或滑动窗口把线性遍历变成常数时间的配对。