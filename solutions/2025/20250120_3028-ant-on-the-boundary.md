# #3028. 边界上的蚂蚁 / Ant on the Boundary

> 难度：简单 · 标签：Array、Simulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/ant-on-the-boundary/)

---

## 题目（英文原版）

**Description**

An ant is on a boundary. It sometimes goes left and sometimes right.
You are given an array of non-zero integers nums. The ant starts reading nums from the first element of it to its end. At each step, it moves according to the value of the current element:
Return the number of times the ant returns to the boundary.
Notes:

**Examples**

**Example 1:**

```
Input: nums = [2,3,-5]
Output: 1
Explanation: After the first step, the ant is 2 steps to the right of the boundary.
After the second step, the ant is 5 steps to the right of the boundary.
After the third step, the ant is on the boundary.
So the answer is 1.
```

**Example 2:**

```
Input: nums = [3,2,-3,-4]
Output: 0
Explanation: After the first step, the ant is 3 steps to the right of the boundary.
After the second step, the ant is 5 steps to the right of the boundary.
After the third step, the ant is 2 steps to the right of the boundary.
After the fourth step, the ant is 2 steps to the left of the boundary.
The ant never returned to the boundary, so the answer is 0.
```

**Constraints**

- 1 <= nums.length <= 100
- -10 <= nums[i] <= 10
- nums[i] != 0

---

## 题目（中文翻译）

**描述**  
一只蚂蚁位于边界（boundary）上，它有时向左移动，有时向右移动。  
给定一个 **非零整数数组（array of non-zero integers）** `nums`。蚂蚁从 `nums` 的第一个元素开始依次读取到末尾。每一步，它按照当前元素的值移动相应的距离（正数表示向右，负数表示向左）。  
返回蚂蚁返回到边界（boundary）的次数。

**示例 1**  
```text
Input: nums = [2,3,-5]
Output: 1
Explanation: 第一步后，蚂蚁在边界的右侧 2 步处。  
After the first step, the ant is 2 steps to the right of the boundary.  
第二步后，蚂蚁在边界的右侧 5 步处。  
After the second step, the ant is 5 steps to the right of the boundary.  
第三步后，蚂蚁回到边界上。  
After the third step, the ant is on the boundary.  
因此答案为 1。  
So the answer is 1.
```

**示例 2**  
```text
Input: nums = [3,2,-3,-4]
Output: 0
Explanation: 第一步后，蚂蚁在边界的右侧 3 步处。  
After the first step, the ant is 3 steps to the right of the boundary.  
第二步后，蚂蚁在边界的右侧 5 步处。  
After the second step, the ant is 5 steps to the right of the boundary.  
第三步后，蚂蚁在边界的右侧 2 步处。  
After the third step, the ant is 2 steps to the right of the boundary.  
第四步后，蚂蚁在边界的左侧 2 步处。  
After the fourth step, the ant is 2 steps to the left of the boundary.  
蚂蚁从未返回到边界，答案为 0。  
The ant never returned to the boundary, so the answer is 0.
```

**约束条件**  
- `1 <= nums.length <= 100`  
- `-10 <= nums[i] <= 10`  
- `nums[i] != 0`   (数组中不存在零)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把蚂蚁在“边界”左侧记为负数，右侧记为正数。  
- **当前位置** 用一个变量 `pos` 表示，初始值 `0`（就在边界上）。  
- 依次读取 `nums`，每读到一个数就把它加到 `pos` 上（左走是负，右走是正）。  
- **每走一步** 检查一次 `pos` 是否恰好等于 `0`，如果是，就说明蚂蚁回到了边界，计数器 `ans` 加一。

> 类比：`pos` 就像一本字典的页码，`nums[i]` 是一次向前或向后翻页的步数。每翻完一页就看一下是否回到了第 0 页（边界）。

这种做法一定能得到正确答案，因为它完整地模拟了题目描述的“每一步都移动并检查是否在边界”。

#### 代码（Python）

```python
def ant_on_boundary(nums):
    """
    返回蚂蚁在遍历完 nums 过程中回到边界的次数
    """
    pos = 0          # 当前距离边界的距离，0 表示正好在边界上
    ans = 0          # 计数器，记录回到边界的次数

    for step, move in enumerate(nums, 1):   # step 为第几步（仅用于调试说明）
        pos += move                         # 按当前元素移动
        # 检查是否恰好回到边界
        if pos == 0:
            ans += 1
            # 如果想观察过程，可以打印：
            # print(f"第 {step} 步后回到边界，累计位置 {pos}")

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  只遍历了一遍数组，`n` 为 `nums` 的长度。这里的 `O(n)` 可以理解为“随着数组变长，运行时间大约会线性增长”。  
- **空间复杂度：** `O(1)`  
  只用了几个固定大小的变量（`pos`、`ans`），和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**唯一的瓶颈** 是没有——它已经是线性遍历一次，无法再更快了。  
不过我们可以把思路用**前缀和**的概念重新表述，帮助大家在以后遇到类似“累计值等于某个目标” 的题目时快速定位。

- **前缀和**：`prefix[i]` 表示前 `i` 个元素的累计和。这里我们只需要一个变量 `pos` 来维护当前前缀和。
- 当 `pos == 0` 时，说明当前前缀和恰好等于初始值（0），即“回到了边界”。  
- 因此 **最优解** 与直觉解本质上相同，只是把“模拟”换成了“前缀和”，便于迁移到更复杂的场景（比如统计所有出现次数等）。

> 类比：把每一步的累计距离想成“水位”。只要水位恰好回到零，就算一次“潮汐”。我们只需要一根尺子（`pos`）随时记录水位即可。

#### 代码（Python）

```python
def ant_on_boundary(nums):
    """
    使用前缀和思想的最优实现
    """
    pos = 0          # 当前前缀和，也就是蚂蚁相对边界的位置
    ans = 0

    for move in nums:
        pos += move   # 更新前缀和
        if pos == 0:  # 前缀和为 0 表示回到了边界
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)` —— 只需要一次遍历。和暴力解相同，但在思路上已经是最简洁、最通用的形式。  
- **空间复杂度：** `O(1)` —— 只使用常数个额外变量。

---

## 心得

- 这道题考察的核心技巧是 **前缀和（累计和）**，以及 **在遍历过程中即时判断条件**。
- 类似技巧常出现在：
  1. “子数组和为 K” 类题（LeetCode 560 Subarray Sum Equals K）  
  2. “最长连续 1 子数组” 需要累计计数  
  3. “判断数组是否能分成若干段，每段和相等”  
- **解题钥匙**：把“每一步的位移”累加成一个变量，遇到目标值（这里是 0）就计数。

## 反思

- **第一反应**：把题目想成“模拟蚂蚁走路”，直接用一个变量记录位置。  
- **最容易踩的坑**：  
  - 忘记把 **第一次回到边界**（即在遍历完第 `i` 步后）也计入答案。  
  - 对负数移动的方向搞混，导致 `pos` 加错符号。  
- **下次遇到同类题**：第一步先想“有没有可以累计的量”，把它抽象成前缀和或累计计数，然后在遍历中即时检查是否满足目标条件。