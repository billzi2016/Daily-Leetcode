# #2295. 替换数组中的元素 / Replace Elements in an Array

> 难度：中等 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/replace-elements-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums that consists of n distinct positive integers. Apply m operations to this array, where in the ith operation you replace the number operations[i][0] with operations[i][1].
It is guaranteed that in the ith operation:
Return the array obtained after applying all the operations.

**Examples**

**Example 1:**

```
Input: nums = [1,2,4,6], operations = [[1,3],[4,7],[6,1]]
Output: [3,2,7,1]
Explanation: We perform the following operations on nums:
- Replace the number 1 with 3. nums becomes [3,2,4,6].
- Replace the number 4 with 7. nums becomes [3,2,7,6].
- Replace the number 6 with 1. nums becomes [3,2,7,1].
We return the final array [3,2,7,1].
```

**Example 2:**

```
Input: nums = [1,2], operations = [[1,3],[2,1],[3,2]]
Output: [2,1]
Explanation: We perform the following operations to nums:
- Replace the number 1 with 3. nums becomes [3,2].
- Replace the number 2 with 1. nums becomes [3,1].
- Replace the number 3 with 2. nums becomes [2,1].
We return the array [2,1].
```

**Constraints**

- n == nums.length
- m == operations.length
- 1 <= n, m <= 105
- All the values of nums are distinct.
- operations[i].length == 2
- 1 <= nums[i], operations[i][0], operations[i][1] <= 106
- operations[i][0] will exist in nums when applying the ith operation.
- operations[i][1] will not exist in nums when applying the ith operation.

---

## 题目（中文翻译）

你被给定一个下标从 0 开始的数组 `nums`，其中包含 `n` 个互不相同的正整数。对该数组执行 `m` 次操作，第 `i` 次操作将数字 `operations[i][0]` 替换为 `operations[i][1]`。保证在第 `i` 次操作时：

- `operations[i][0]` 必定在当前数组中存在；
- `operations[i][1]` 在当前数组中不存在。

返回完成所有操作后得到的数组。

**示例 1：**

```
Input: nums = [1,2,4,6], operations = [[1,3],[4,7],[6,1]]
Output: [3,2,7,1]
Explanation: 我们对 `nums` 依次执行以下操作：
- 用 3 替换数字 1，`nums` 变为 [3,2,4,6]。
- 用 7 替换数字 4，`nums` 变为 [3,2,7,6]。
- 用 1 替换数字 6，`nums` 变为 [3,2,7,1]。
返回最终数组 [3,2,7,1]。
```

**示例 2：**

```
Input: nums = [1,2], operations = [[1,3],[2,1],[3,2]]
Output: [2,1]
Explanation: 我们对 `nums` 依次执行以下操作：
- 用 3 替换数字 1，`nums` 变为 [3,2]。
- 用 1 替换数字 2，`nums` 变为 [3,1]。
- 用 2 替换数字 3，`nums` 变为 [2,1]。
返回数组 [2,1]。
```

**约束条件：**

- `n == nums.length`
- `m == operations.length`
- `1 <= n, m <= 10^5`
- `nums` 中的所有值互不相同。
- `operations[i].length == 2`
- `1 <= nums[i], operations[i][0], operations[i][1] <= 10^6`
- 在执行第 `i` 次操作时，`operations[i][0]` 必定存在于 `nums` 中。
- 在执行第 `i` 次操作时，`operations[i][1]` 必定不存在于 `nums` 中。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次的替换操作都 **逐个遍历** 整个数组，找到要被替换的数字后再改成新值。  
可以把数组想象成一排 **书架**，每本书都有唯一的编号（数组的数值）。  
一次操作就像让你在整排书中 **找一本指定编号的书**，把它换成另一种编号的书。  
如果每次都从左到右找，这就像在一本厚厚的字典里逐页查找——很慢，但思路最直白。

**为什么正确**：  
- 题目保证在第 *i* 次操作时，`operations[i][0]` 必定在当前数组里出现。  
- 只要我们真的把它找到了并改成 `operations[i][1]`，数组的状态就和题目要求的一致。  
- 重复执行所有操作后，最终数组自然就是答案。

#### 代码（Python）

```python
def replaceElements(nums, operations):
    """
    暴力解：对每一次操作都遍历 nums 找到要替换的数，然后直接改值。
    """
    for old, new in operations:          # 逐条操作
        for idx in range(len(nums)):     # 在数组里逐个检查
            if nums[idx] == old:         # 找到要替换的元素
                nums[idx] = new          # 直接改成新值
                break                    # 已完成本次替换，退出内层循环
    return nums
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 这里的 `m` 是操作次数，`n` 是数组长度。每一次操作都要遍历整个数组（最坏情况），所以时间随两者的乘积增长。  
  - 用生活化的说法：如果你有 10 本书要换 10 次，每次都要把书全部翻一遍找目标，那总共要翻 100 次。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（循环计数器），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要 **线性搜索** 目标数字。  
如果我们能够在 **常数时间** 内直接定位到某个数字在数组中的位置，就可以把每次操作的代价从 `O(n)` 降到 `O(1)`。

**核心技巧：哈希表（字典）存储 “数字 → 位置”。**  
- 想象我们有一本 **索引卡片**，每张卡片记录了某本书的编号（数字）和它在书架上的位置（下标）。  
- 用 Python 的 `dict` 就相当于这本卡片本，查询、插入、删除的时间都是 `O(1)`。  

**优化步骤**  

1. **初始化**：遍历一次 `nums`，把每个数及其下标放进哈希表 `pos`。  
   - 这一步是 `O(n)`，只做一次。  

2. **处理每条操作** `[old, new]`：  
   - 通过 `pos[old]` 直接得到 `old` 在数组中的下标 `idx`（常数时间）。  
   - 把 `nums[idx]` 改成 `new`。  
   - 更新哈希表：删除键 `old`，插入键 `new` 并指向同一个下标 `idx`。  
   - 这样后续如果还有操作涉及 `new`，我们仍然可以快速定位。  

3. **返回**最终的 `nums` 即可。

**为什么仍然正确**：  
- 哈希表始终保持 “当前数组里每个数 → 它的下标” 的映射。  
- 每次替换后我们同步更新映射，确保后面的操作看到的都是最新的数组状态。  

#### 代码（Python）

```python
def replaceElements(nums, operations):
    """
    最优解：利用哈希表记录每个数所在的下标，实现 O(1) 替换。
    """
    # 1. 建立数字 → 下标 的映射（一次遍历）
    pos = {num: idx for idx, num in enumerate(nums)}   # dict 相当于“索引卡片”

    # 2. 逐条执行操作
    for old, new in operations:
        idx = pos[old]          # 直接拿到 old 的位置（O(1)）
        nums[idx] = new        # 替换数组中的值

        # 同步更新哈希表
        del pos[old]           # old 已经不在数组里，删掉它的映射
        pos[new] = idx         # new 出现在同一个位置，加入映射

    return nums
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 初始化哈希表 `O(n)`，每条操作只做常数次字典查询/更新 `O(1)`，共 `m` 条，所以总共是 `O(n + m)`。  
  - 与暴力解相比，时间从 “每次都翻整排书” 降到了 “直接看索引卡片”，大幅提升。

- **空间复杂度**：`O(n)`  
  - 额外的哈希表需要存储 `n` 条键值对（每个数组元素对应一个下标），因此随输入规模线性增长。  
  - 用生活化的说法：我们需要准备和书本数量相同的索引卡片。

---

## 心得  

- **核心技巧**：使用哈希表（字典）维护 “值 → 位置” 的映射，实现 O(1) 查找与更新。  
- **适用场景**：  
  1. **数组元素位置快速定位**（如 “把数组里的某个数改成别的数”）。  
  2. **元素唯一且需要频繁查询/更新**（如 “数组去重后查询位置”）。  
  3. **类似题目**：LeetCode 1704 *“返回数组中相邻元素的距离”*、LeetCode 1389 *“按既定顺序排列数组”*。  
- **一句话总结**：**把“在数组里找位置”这件事交给哈希表，让每次替换都只花常数时间**。

---

## 反思  

- **第一反应**：直接遍历数组寻找要替换的元素，写出最朴素的实现。  
- **最容易踩的坑**：  
  - 忘记在替换后同步更新哈希表，导致后续操作仍然使用旧的映射。  
  - 没有考虑 **“新值不在数组中”** 的保证，若题目放宽约束，需要先检查或处理冲突。  
- **下次遇到同类题**：第一步先思考 **“我需要怎样快速定位元素？”**，如果是唯一值，立刻构建哈希表；如果有重复，可能需要 **集合 + 列表** 或 **多值映射**。