# #1051. 身高检查器 / Height Checker

> 难度：简单 · 标签：Array、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/height-checker/)

---

## 题目（英文原版）

**Description**

A school is trying to take an annual photo of all the students. The students are asked to stand in a single file line in non-decreasing order by height. Let this ordering be represented by the integer array expected where expected[i] is the expected height of the ith student in line.
You are given an integer array heights representing the current order that the students are standing in. Each heights[i] is the height of the ith student in line (0-indexed).
Return the number of indices where heights[i] != expected[i].

**Examples**

**Example 1:**

```
Input: heights = [1,1,4,2,1,3]
Output: 3
Explanation: 
heights:  [1,1,4,2,1,3]
expected: [1,1,1,2,3,4]
Indices 2, 4, and 5 do not match.
```

**Example 2:**

```
Input: heights = [5,1,2,3,4]
Output: 5
Explanation:
heights:  [5,1,2,3,4]
expected: [1,2,3,4,5]
All indices do not match.
```

**Example 3:**

```
Input: heights = [1,2,3,4,5]
Output: 0
Explanation:
heights:  [1,2,3,4,5]
expected: [1,2,3,4,5]
All indices match.
```

**Constraints**

- 1 <= heights.length <= 100
- 1 <= heights[i] <= 100

---

## 题目（中文翻译）

学校每年都会为所有学生拍摄合照，要求学生按身高的非递减顺序排成一列。将这种理想的排队方式记作整数数组 `expected`，其中 `expected[i]` 表示第 `i` 位学生应该站的位置的身高。  
现在给定一个整数数组 `heights`，表示学生当前的站位顺序，其中 `heights[i]` 是第 `i` 位学生的实际身高（下标从 0 开始）。  
请返回 `heights[i] != expected[i]` 的下标数量。

## 示例

### 示例 1
**输入**: `heights = [1,1,4,2,1,3]`  
**输出**: `3`  
**解释**:  
```
heights:  [1,1,4,2,1,3]
expected: [1,1,1,2,3,4]
```
下标 2、4、5 处的身高不匹配。

### 示例 2
**输入**: `heights = [5,1,2,3,4]`  
**输出**: `5`  
**解释**:  
```
heights:  [5,1,2,3,4]
expected: [1,2,3,4,5]
```
所有下标的身高均不匹配。

### 示例 3
**输入**: `heights = [1,2,3,4,5]`  
**输出**: `0`  
**解释**:  
```
heights:  [1,2,3,4,5]
expected: [1,2,3,4,5]
```
所有下标的身高都匹配。

## 约束条件
- `1 <= heights.length <= 100`
- `1 <= heights[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是先把学生的身高排成“应该出现的顺序”，再把这个正确顺序和原来的 `heights` 逐位比较，统计不相同的下标个数。

- **数据结构**：我们需要两个数组  
  1. `heights`：原始顺序（题目已给出）。  
  2. `expected`：把 `heights` 复制后**排序**得到的数组。  
  排序可以看成把一堆乱糟糟的书本放进书架，按照高度（从小到大）依次摆好。  

- **为什么正确**：如果把所有学生按身高从低到高排好（即 `expected`），那么只有当原来的位置已经是这个顺序时，`heights[i]` 才会等于 `expected[i]`。不相等的下标正是需要“重新站位”的学生。

- **复杂度分析**：  
  - 排序一步的时间复杂度是 `O(n log n)`（这里 `n` 是学生人数），因为常用的排序算法（如 Python 内置的 Timsort）在最坏情况下会进行 `log n` 轮比较，每轮处理 `n` 个元素。  
  - 再遍历比较一次是 `O(n)`。  
  - 所以总时间是 `O(n log n + n) = O(n log n)`，在这里我们称之为“n 乘以对数 n”，意思是随着学生人数增加，耗时会比线性增长（`O(n)`）稍快一些。  
  - 额外空间我们用了一个和 `heights` 同大小的副本 `expected`，占用 `O(n)` 的空间。

#### 代码（Python）

```python
def heightChecker(heights):
    # 1. 复制一份原数组，准备排序得到正确顺序
    expected = sorted(heights)          # 排序后得到应该的顺序
    # 2. 逐位比较，统计不相等的下标个数
    diff_cnt = 0
    for i in range(len(heights)):
        if heights[i] != expected[i]:   # 如果当前位置的身高不对
            diff_cnt += 1               # 计数加一
    return diff_cnt
```

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 排序是主要耗时，`n` 为学生人数。  
- **空间复杂度**：`O(n)` —— 需要额外的数组 `expected` 来存放排序后的结果。

---

### 2. 最优解

#### 思路  

虽然 `O(n log n)` 已经够快（`n ≤ 100`），但我们可以利用题目给出的**取值范围**（身高在 1~100）把时间进一步降到线性 `O(n)`。思路如下：

1. **瓶颈**：排序的 `log n` 部分是多余的，因为我们知道身高的取值只有 100 种。  
2. **计数排序**：把每一种身高出现的次数记下来（相当于在字典里查“这个词出现了几次”，这里词就是身高），再按照身高从小到大“重新走一遍”，即可得到有序序列，而不需要比较大小。  
3. **实现细节**  
   - 创建长度为 101（下标 0~100，0 不会用到）的计数数组 `cnt`，`cnt[h]` 表示身高为 `h` 的学生有多少人。  
   - 第一次遍历 `heights`，把每个身高的计数加一。  
   - 第二次遍历 `heights`（原数组的顺序），用一个指针 `cur_h` 表示“当前应该出现的身高”。  
     - 如果 `cnt[cur_h]` 为 0，说明这种身高已经全部用完，`cur_h` 向右移动（即身高增大）。  
     - 否则，比较 `heights[i]` 与 `cur_h`：不相等则计数+1；无论相不相等，都把 `cnt[cur_h]` 减一（表示用了一个该身高的名额）。  
4. **类比**：把计数数组想象成一本“身高目录”，每一页（下标）写着该身高的剩余学生数。我们从最小的页码开始，逐页检查并对应原来的学生站位。

这样我们只遍历了两遍 `heights`，没有任何 `log` 操作，时间降到了 `O(n)`，空间只用了常数（101）大小的额外数组，即 `O(1)`（相对于输入规模是常数）。

#### 代码（Python）

```python
def heightChecker(heights):
    # 1. 计数数组，索引代表身高，值代表出现次数
    cnt = [0] * 101               # 因为身高范围是 1~100，0 位置不使用
    for h in heights:            # 第一次遍历：统计每个身高出现几次
        cnt[h] += 1

    diff_cnt = 0                  # 记录不匹配的下标数量
    cur_h = 1                     # 当前应该出现的最小身高（从 1 开始）

    # 2. 再次遍历原数组，按计数顺序“模拟”排好序的序列
    for h in heights:
        # 找到下一个还有剩余学生的身高
        while cnt[cur_h] == 0:   # 当前身高已经用完，往右找
            cur_h += 1

        # 此时 cur_h 就是期望的身高
        if h != cur_h:           # 原位置的身高与期望不一致
            diff_cnt += 1

        cnt[cur_h] -= 1          # 用掉一个 cur_h 身高的名额
    return diff_cnt
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 两次线性遍历，`n` 为学生人数。  
- **空间复杂度**：`O(1)` —— 计数数组大小固定为 101（常数），不随 `n` 增长。

---

## 心得

- **核心技巧**：利用**计数排序**（Counting Sort）把排序过程的 `log n` 降到 `O(1)`，前提是元素取值范围有限且不大。  
- **适用的题型**：  
  1. 需要对取值范围在 `[1, K]`（`K` 较小）的整数数组进行排序或统计，如 “排序数组的出现次数”。  
  2. “找出数组中与排好序后不一致的元素数量” 类似的比较题。  
- **一句话总结**：**把“排序”转化为“计数”，再按计数顺序逐个比对**，即可在 O(n) 时间内完成。

---

## 反思

- **第一反应**：直接把数组排序后逐位比较，想到使用 Python 的 `sorted`。  
- **最容易踩的坑**：  
  - 忘记复制一份再排序，导致原数组被修改，后续比较出错。  
  - 对计数排序不熟悉时，容易在寻找下一个非零计数的循环中出现死循环（忘记 `cur_h` 边界）。  
  - 忽视身高的取值范围（1~100），如果取值更大，计数数组会占用过多空间，需要回退到普通排序。  
- **下次类似题的第一步**：先检查“数值范围是否有限且小”，如果是，立刻考虑计数排序或桶排序；否则使用常规排序。