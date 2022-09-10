# #1929. 数组拼接 / Concatenation of Array

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/concatenation-of-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums of length n, you want to create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for 0 <= i < n (0-indexed).
Specifically, ans is the concatenation of two nums arrays.
Return the array ans.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1]
Output: [1,2,1,1,2,1]
Explanation: The array ans is formed as follows:
- ans = [nums[0],nums[1],nums[2],nums[0],nums[1],nums[2]]
- ans = [1,2,1,1,2,1]
```

**Example 2:**

```
Input: nums = [1,3,2,1]
Output: [1,3,2,1,1,3,2,1]
Explanation: The array ans is formed as follows:
- ans = [nums[0],nums[1],nums[2],nums[3],nums[0],nums[1],nums[2],nums[3]]
- ans = [1,3,2,1,1,3,2,1]
```

**Constraints**

- n == nums.length
- 1 <= n <= 1000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，你需要创建一个长度为 `2n` 的数组 `ans`，使得在 `0 ≤ i < n`（0‑索引）时满足 `ans[i] == nums[i]` 且 `ans[i + n] == nums[i]`。  
换句话说，`ans` 是两个 `nums` 数组的拼接（concatenation）。返回数组 `ans`。

## 示例

### 示例 1
**输入:** `nums = [1,2,1]`  
**输出:** `[1,2,1,1,2,1]`  
**解释:**  
数组 `ans` 的构造过程如下：  
- `ans = [nums[0], nums[1], nums[2], nums[0], nums[1], nums[2]]`  
- `ans = [1,2,1,1,2,1]`

### 示例 2
**输入:** `nums = [1,3,2,1]`  
**输出:** `[1,3,2,1,1,3,2,1]`  
**解释:**  
数组 `ans` 的构造过程如下：  
- `ans = [nums[0], nums[1], nums[2], nums[3], nums[0], nums[1], nums[2], nums[3]]`  
- `ans = [1,3,2,1,1,3,2,1]`

## 约束条件
- `n == nums.length`
- `1 <= n <= 1000`
- `1 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把原数组的每个元素分别放到新数组的两个位置**：

- 先创建一个长度为 `2 * n`（`n` 是原数组长度）的空数组 `ans`，这里的空数组可以先全部填充为 `0`（或 `None`），相当于在纸上先画好 2n 个格子，准备写数字。
- 然后遍历原数组 `nums`（用 `for i in range(n)`），把 `nums[i]` 写进 `ans[i]`（左边的那一段），再把同样的值写进 `ans[i + n]`（右边的那一段）。  
  这一步可以想象成 **把一本书的章节复印两遍**，左边是原来的，右边是复制的。

为什么能得到正确答案？因为题目要求的正是“把 `nums` 连在自己后面”，而我们正是把每个元素在恰好的两个位置写上了。

#### 代码（Python）

```python
def getConcatenation(nums):
    n = len(nums)                     # 原数组长度
    ans = [0] * (2 * n)                # 先准备好 2n 个格子，全部用 0 填充

    for i in range(n):                # 遍历原数组的每个下标 i
        ans[i] = nums[i]              # 把 nums[i] 放到左边
        ans[i + n] = nums[i]          # 把同样的值放到右边（下标偏移 n）

    return ans
```

#### 复杂度

- **时间复杂度：O(n)**  
  我们只遍历一次原数组，`n` 次循环，每次做常数时间的赋值。  
  “O(n)” 可以理解为“工作量随输入规模线性增长”，如果 `n` 加倍，时间大概也会加倍。

- **空间复杂度：O(n)**  
  需要额外开辟一个长度为 `2n` 的数组 `ans`，这相当于再使用了和原数组同等规模的空间（常数因子 2 不影响大 O 表示）。  

---

### 2. 最优解

#### 思路  

从暴力解出发，我们已经达到了 **线性时间**，已经是最优的时间复杂度了（不可能比 `O(n)` 更快，因为必须把 `2n` 个元素写进去）。  
我们可以把实现方式写得更**简洁**，利用 Python 列表的“拼接”特性：

- `nums + nums` 直接把两个列表合并成一个新列表，内部实现本质上也是一次遍历把元素拷贝过去，只是写法更简洁。  
- 这相当于把两本完全相同的书直接放在一起，读者看到的就是两遍内容。

#### 代码（Python）

```python
def getConcatenation(nums):
    # 直接利用列表的 + 操作符把 nums 拼接到自身后面
    return nums + nums
```

> **提示**：如果你想手动控制内存（在极端大数据时），可以使用 `list.extend`：
> ```python
> ans = nums.copy()      # 先拷贝一份
> ans.extend(nums)       # 再把原数组追加进来
> return ans
> ```

#### 复杂度

- **时间复杂度：O(n)**  
  虽然代码只有一行，但底层仍然需要遍历 `nums` 两次（一次拷贝，一次追加），总共写入 `2n` 个元素，和暴力解的时间相同。

- **空间复杂度：O(n)**  
  同样需要新建一个长度为 `2n` 的列表，空间使用和暴力解一致。

---

## 心得

- **核心技巧**：数组（列表）复制与拼接。  
- **适用的题型**：  
  1. “把数组翻倍” 类似题目（如 `Duplicate Zeros`、`Merge Two Sorted Arrays` 的前半段）。  
  2. 需要把一个序列重复若干次的题目（如 `Repeat String`、`Generate Array`）。  
- **一句话总结解题钥匙**：**把原数组直接拼接到自身后面**，不必额外循环两遍，只要利用语言自带的拼接操作即可。

---

## 反思

- **第一反应**：看到“把数组连接两次”，自然想到先建一个大数组，然后把每个元素写两遍。  
- **最容易踩的坑**：  
  - 忘记创建足够大的结果数组，导致下标越界。  
  - 对空数组或极小 `n`（如 `n=1`）没有特殊处理，虽然本题约束 `n≥1`，但养成检查边界的好习惯。  
- **下次遇到同类题**：第一步先思考“是否可以直接使用语言提供的复制/拼接功能”，如果可以，就立刻写出一行代码；如果不行，再考虑手动循环实现。