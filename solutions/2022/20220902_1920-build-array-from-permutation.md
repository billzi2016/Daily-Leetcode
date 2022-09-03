# #1920. 从排列构造数组 / Build Array from Permutation

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/build-array-from-permutation/)

---

## 题目（英文原版）

**Description**

Given a zero-based permutation nums (0-indexed), build an array ans of the same length where ans[i] = nums[nums[i]] for each 0 <= i < nums.length and return it.
A zero-based permutation nums is an array of distinct integers from 0 to nums.length - 1 (inclusive).
Follow-up: Can you solve it without using an extra space (i.e., O(1) memory)?

**Examples**

**Example 1:**

```
Input: nums = [0,2,1,5,3,4]
Output: [0,1,2,4,5,3]
Explanation: The array ans is built as follows: 
ans = [nums[nums[0]], nums[nums[1]], nums[nums[2]], nums[nums[3]], nums[nums[4]], nums[nums[5]]]
    = [nums[0], nums[2], nums[1], nums[5], nums[3], nums[4]]
    = [0,1,2,4,5,3]
```

**Example 2:**

```
Input: nums = [5,0,1,2,3,4]
Output: [4,5,0,1,2,3]
Explanation: The array ans is built as follows:
ans = [nums[nums[0]], nums[nums[1]], nums[nums[2]], nums[nums[3]], nums[nums[4]], nums[nums[5]]]
    = [nums[5], nums[0], nums[1], nums[2], nums[3], nums[4]]
    = [4,5,0,1,2,3]
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] < nums.length
- The elements in nums are distinct.

---

## 题目（中文翻译）

给定一个 **零基排列**（zero-based permutation）`nums`（下标从 0 开始），构造一个与其长度相同的数组 `ans`，使得 `ans[i] = nums[nums[i]]` 对于所有 `0 ≤ i < nums.length` 均成立，并返回该数组。  
**零基排列**是指由 `0` 到 `nums.length - 1`（含）之间的互不相同的整数构成的数组。

**示例 1**  
**示例 2**  
**约束条件**  
**进阶**：能否在不使用额外空间（即 O(1) 额外内存）的情况下完成该题？

---

### 示例

#### 示例 1
**输入**: `nums = [0,2,1,5,3,4]`  
**输出**: `[0,1,2,4,5,3]`  
**解释**: 构造 `ans` 的过程如下:  
```
ans = [nums[nums[0]], nums[nums[1]], nums[nums[2]],
       nums[nums[3]], nums[nums[4]], nums[nums[5]]]
    = [nums[0], nums[2], nums[1], nums[5], nums[3], nums[4]]
    = [0,1,2,4,5,3]
```

#### 示例 2
**输入**: `nums = [5,0,1,2,3,4]`  
**输出**: `[4,5,0,1,2,3]`  
**解释**: 构造 `ans` 的过程如下:  
```
ans = [nums[nums[0]], nums[nums[1]], nums[nums[2]],
       nums[nums[3]], nums[nums[4]], nums[nums[5]]]
    = [nums[5], nums[0], nums[1], nums[2], nums[3], nums[4]]
    = [4,5,0,1,2,3]
```

### 约束条件
- `1 <= nums.length <= 1000`
- `0 <= nums[i] < nums.length`
- `nums` 中的元素互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目要求 **对每个下标 i**，把 `ans[i]` 设成 `nums[ nums[i] ]`。  
最直接的想法就是：

1. 新建一个和 `nums` 长度相同的数组 `ans`（相当于准备了一张新的“纸”。）  
2. 按顺序遍历下标 `i = 0 … n‑1`，把 `ans[i] = nums[ nums[i] ]` 写进去。  

这里用到的唯一数据结构是 **数组**（在 Python 中就是 list），它就像一排编号的抽屉，`nums[i]` 表示第 `i` 抽屉里放的数字，而 `nums[ nums[i] ]` 就是先打开第 `i` 抽屉，看到里面的数字 `k`，再去打开第 `k` 抽屉，取出那里的数字。  

这种做法显然能得到正确答案，因为我们完全按照题目描述的 “先取一次，再取一次” 进行操作。  

**时间/空间复杂度**  
- **时间**：我们遍历一次数组，做 O(1) 的查找两次，所以是 **O(n)**（n 是数组长度）。可以把 O(n) 想象成“随数组长度线性增长”，比如长度是 10 时跑 10 步，长度是 100 时跑 100 步。  
- **空间**：额外新建了一个同样大小的数组 `ans`，所以是 **O(n)** 的额外空间。  

#### 代码（Python）  

```python
def buildArray(nums):
    """
    暴力解：新建 ans，直接按题意填值
    :param nums: List[int]，满足 0 <= nums[i] < len(nums) 且不重复
    :return: List[int]，ans[i] = nums[ nums[i] ]
    """
    n = len(nums)               # 数组长度
    ans = [0] * n               # 先准备好 n 个空位的答案数组
    for i in range(n):
        # 先取 nums[i]，再把这个结果当作下标去取 nums
        ans[i] = nums[ nums[i] ]   # 两次下标查找
    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 随着数组长度线性增长，遍历一次即可。  
- **空间复杂度**：**O(n)** — 需要额外的同等大小数组 `ans` 来存放结果。  

---  

### 2. 最优解  

#### 思路  
暴力解的 **时间** 已经是最优的 O(n)，唯一可以改进的地方是 **空间**：能否在原数组 `nums` 上直接改写，使得不需要额外的数组（即 O(1) 额外空间）？

关键难点在于：如果我们直接把 `nums[i]` 改成 `nums[ nums[i] ]`，后面的计算可能会使用已经被改过的值，导致错误。  
想法是 **把旧值和新值同时保存下来**，这样在遍历时仍然可以取到原始的 `nums[i]`。  

一种常见的技巧是 **“编码”**（encoding）两个数到同一个位置：

- 假设 `old = nums[i]`（原始值），`new = nums[ old ]`（我们真正想写进去的值）。  
- 因为 `new` 和 `old` 都在 `[0, n-1]` 范围内，我们可以利用 **整数的进位** 把它们合在一起：  
  ```
  nums[i] = old + n * new
  ```
  这里 `n` 是数组长度，乘以 `n` 后保证 `new` 的信息不会和 `old` 混淆。  
- 当所有位置都完成 “编码” 后，再遍历一次把每个位置除以 `n`，只保留新值：
  ```
  nums[i] = nums[i] // n
  ```

**类比**：把两个小盒子（old、new）装进一个大盒子（nums[i]），先把大盒子装好（old + n*new），最后打开大盒子只取出 new（除以 n）。

这样我们只用了原数组本身，不需要额外的 O(n) 空间，空间复杂度降到 **O(1)**。

#### 代码（Python）  

```python
def buildArray(nums):
    """
    最优解：原地 O(1) 额外空间
    思路：利用编码技巧把旧值和新值存到同一个位置
    """
    n = len(nums)

    # 第一次遍历：把新值编码进 nums[i]，保留旧值供后续使用
    for i in range(n):
        old = nums[i]                # 还没被修改的原始值
        new = nums[old]              # 我们真正想写进去的值
        nums[i] = old + n * new      # 编码：low 位保存 old，high 位保存 new

    # 第二次遍历：把编码后的数恢复为只包含新值
    for i in range(n):
        nums[i] = nums[i] // n       # 取高位即新值

    return nums   # 直接返回原数组即可
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 仍然只遍历两次数组，常数因子略大但数量级相同。  
- **空间复杂度**：**O(1)** — 只用了常数个额外变量（`n`, `old`, `new`），没有额外随 `n` 增长的数组。  

---

## 心得  

- **核心技巧**：在不额外空间的情况下，利用「编码」把旧值和新值存到同一个位置（也叫「原地哈希」或「在数组里做标记」）。  
- **适用题型**：  
  1. 需要在原数组上做一次“映射”或“置换”，如 *数组的置换、原地翻转*。  
  2. 需要标记已访问或已处理的元素，却又不能额外开数组，如 *寻找环、原地计数*。  
- **一句话总结**：**把两件事压进同一个格子，用整数的进位来分层，既不丢信息，又不占新空间。**  

## 反思  

- **第一反应**：直接新建一个数组复制结果——最自然的实现，却忘了题目还有「O(1) 额外空间」的进阶要求。  
- **最容易踩的坑**：  
  - 直接覆盖 `nums[i]` 会破坏后面需要的原始值。  
  - 编码时要确保乘的基数 `n` 足够大，防止新旧值混淆（这里因为所有值 < n，`n` 正好满足条件）。  
  - 记得第二遍遍历把结果取出来，否则返回的仍是编码后的混合数。  
- **下次遇到同类题**：第一步先思考「能否把旧信息和新信息一起存」——如果能，就尝试「编码」或「标记」技巧；如果不能，才考虑额外空间的暴力实现。