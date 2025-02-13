# #3069. **将元素分配到两个数组 I** / Distribute Elements Into Two Arrays I

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/distribute-elements-into-two-arrays-i/)

---

## 题目（英文原版）

**Description**

You are given a 1-indexed array of distinct integers nums of length n.
You need to distribute all the elements of nums between two arrays arr1 and arr2 using n operations. In the first operation, append nums[1] to arr1. In the second operation, append nums[2] to arr2. Afterwards, in the ith operation:
The array result is formed by concatenating the arrays arr1 and arr2. For example, if arr1 == [1,2,3] and arr2 == [4,5,6], then result = [1,2,3,4,5,6].
Return the array result.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3]
Output: [2,3,1]
Explanation: After the first 2 operations, arr1 = [2] and arr2 = [1].
In the 3rd operation, as the last element of arr1 is greater than the last element of arr2 (2 > 1), append nums[3] to arr1.
After 3 operations, arr1 = [2,3] and arr2 = [1].
Hence, the array result formed by concatenation is [2,3,1].
```

**Example 2:**

```
Input: nums = [5,4,3,8]
Output: [5,3,4,8]
Explanation: After the first 2 operations, arr1 = [5] and arr2 = [4].
In the 3rd operation, as the last element of arr1 is greater than the last element of arr2 (5 > 4), append nums[3] to arr1, hence arr1 becomes [5,3].
In the 4th operation, as the last element of arr2 is greater than the last element of arr1 (4 > 3), append nums[4] to arr2, hence arr2 becomes [4,8].
After 4 operations, arr1 = [5,3] and arr2 = [4,8].
Hence, the array result formed by concatenation is [5,3,4,8].
```

**Constraints**

- 3 <= n <= 50
- 1 <= nums[i] <= 100
- All elements in nums are distinct.

---

## 题目（中文翻译）

你得到一个下标从 1 开始、长度为 `n`、且元素互不相同的整数数组 `nums`。  
需要通过恰好 `n` 次操作把 `nums` 中的所有元素分配到两个数组 `arr1` 与 `arr2` 中。

- 第 1 次操作：将 `nums[1]` 追加到 `arr1`。  
- 第 2 次操作：将 `nums[2]` 追加到 `arr2`。  
- 第 `i` 次操作（`i ≥ 3`）的规则如下：

  1. 先将 `arr1` 与 `arr2` 按顺序拼接得到数组 `result`（即 `result = arr1 + arr2`，例如 `arr1 = [1,2,3]`、`arr2 = [4,5,6]` 时 `result = [1,2,3,4,5,6]`）。
  2. 若 `arr1` 的最后一个元素大于 `arr2` 的最后一个元素，则把 `nums[i]` 追加到 `arr1`；否则把 `nums[i]` 追加到 `arr2`。

返回最终得到的拼接数组 `result`。

---

### 示例

#### 示例 1
**输入**  
`nums = [2,1,3]`

**输出**  
`[2,3,1]`

**解释**  
前两次操作后，`arr1 = [2]`，`arr2 = [1]`。  
第 3 次操作时，`arr1` 的最后一个元素 2 大于 `arr2` 的最后一个元素 1，故把 `nums[3]` 追加到 `arr1`。  
此时 `arr1 = [2,3]`，`arr2 = [1]`。  
拼接得到的数组为 `[2,3,1]`。

#### 示例 2
**输入**  
`nums = [5,4,3,8]`

**输出**  
`[5,3,4,8]`

**解释**  
前两次操作后，`arr1 = [5]`，`arr2 = [4]`。  
第 3 次操作时，`arr1` 的最后一个元素 5 大于 `arr2` 的最后一个元素 4，故把 `nums[3]` 追加到 `arr1`，此时 `arr1 = [5,3]`。  
第 4 次操作时，`arr2` 的最后一个元素 4 大于 `arr1` 的最后一个元素 3，故把 `nums[4]` 追加到 `arr2`，此时 `arr2 = [4,8]`。  
最终拼接得到的数组为 `[5,3,4,8]`。

---

### 约束条件

- `3 <= n <= 50`
- `1 <= nums[i] <= 100`
- `nums` 中的所有元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目本身就描述了一套**顺序模拟**的规则：  
1️⃣ 第一次把 `nums[1]` 放进 `arr1`  
2️⃣ 第二次把 `nums[2]` 放进 `arr2`  
3️⃣ 从第 3 次开始，比较 `arr1` 的**最后一个元素**和 `arr2` 的**最后一个元素**  
   - 如果 `arr1` 最后一个 > `arr2` 最后一个，就把当前 `nums[i]` 放进 `arr1`  
   - 否则放进 `arr2`  

这就像 **排队**：我们每次只看两条队伍的“队尾”，决定把新来的小朋友加入哪条队。  
- **数组**（list）在 Python 里就像一个可随时在尾部添加元素的“背包”。  
- “最后一个元素”可以直接通过 `list[-1]` 取到，类似查字典里某个词的**解释**——直接定位，不需要遍历。

只要把规则一步步照着写，遍历一次 `nums`，就能得到 `arr1`、`arr2`，最后把两者拼接得到 `result`。  
**为什么正确？**  
因为题目规定的每一步操作唯一确定：我们不需要做任何“选择”，只要遵守比较规则，就一定得到唯一的 `arr1`、`arr2`，进而唯一的 `result`。

**时间/空间复杂度**  
- 我们遍历 `nums` 一次，`O(n)` 次比较和一次追加，**时间复杂度是 O(n)**。  
  - 这里的 `O(n)` 可以理解为：“如果 `nums` 长度是 10，最多做 10 次基本操作；如果是 1000，就最多做 1000 次”。  
- 使用了两个额外的列表 `arr1`、`arr2`（总长度仍是 `n`），**空间复杂度是 O(n)**。  

#### 代码（Python）

```python
def resultArray(nums):
    """
    按题目规则把 nums 分配到 arr1、arr2，最后返回 arr1+arr2
    """
    # 第一步、第二步直接放入对应的数组
    arr1 = [nums[0]]          # 第 1 次操作，放进 arr1
    arr2 = [nums[1]]          # 第 2 次操作，放进 arr2

    # 从第 3 个元素开始遍历（下标从 2 开始）
    for i in range(2, len(nums)):
        # 看 arr1、arr2 的最后一个元素大小
        if arr1[-1] > arr2[-1]:
            # arr1 尾巴更大，当前元素也放进 arr1
            arr1.append(nums[i])
        else:
            # 否则放进 arr2
            arr2.append(nums[i])

    # 最终结果是 arr1 与 arr2 的拼接
    return arr1 + arr2
```

#### 复杂度  

- **时间复杂度：** `O(n)` — 只遍历一次数组，n 越大，操作次数线性增长。  
- **空间复杂度：** `O(n)` — 需要两个额外列表来保存全部元素，最坏情况下它们合在一起占 `n` 个位置。

---

### 2. 最优解

#### 思路  

对这道题而言，**暴力模拟本身已经是最优**，因为每一步的决定只能通过一次比较得到，无法再省掉这一步。  
不过我们仍然可以从“慢在哪里”来思考：  
- 如果有人尝试在每一步都遍历整个 `arr1`、`arr2` 去找最大/最小值，时间会变成 `O(n²)`，这就是**瓶颈**。  
- 关键在于**只需要关注最后一个元素**，不必遍历整个子数组。  

因此，最优解的核心技巧是**“只看尾巴”**（即 `list[-1]`），这是一种**常数时间的查询**。  

下面的实现与上面的暴力解在代码上几乎相同，但我们明确指出它已经是 **时间 O(n)、空间 O(n)** 的最优方案。

#### 代码（Python）

```python
def resultArray(nums):
    """
    最优实现：只比较两个子数组的最后一个元素，时间 O(n)，空间 O(n)
    """
    # 初始化两个子数组
    arr1 = [nums[0]]
    arr2 = [nums[1]]

    # 从第 3 个元素开始逐个处理
    for x in nums[2:]:
        # 只比较 arr1、arr2 的最后一个元素
        if arr1[-1] > arr2[-1]:
            arr1.append(x)   # 放进 arr1
        else:
            arr2.append(x)   # 放进 arr2

    # 拼接返回
    return arr1 + arr2
```

#### 复杂度  

- **时间复杂度：** `O(n)` — 每个元素只做一次比较和一次追加。  
  - 与暴力解相比，没有任何额外的循环，已经是最快的线性时间。  
- **空间复杂度：** `O(n)` — 需要存放 `arr1`、`arr2` 两个列表，总元素数等于原数组长度。  

---

## 心得

- **核心技巧**：在需要“比较子数组的状态”时，**只保留必要的信息**（这里是子数组的最后一个元素），避免全遍历。  
- **适用的题型**：  
  1. “把序列分配到两条队列/栈，依据队尾/栈顶比较” —— 如 LeetCode *Distribute Elements Into Two Arrays II*。  
  2. “按规则把元素放入若干组，只关心每组的最新元素” —— 如 “分配糖果” 类问题。  
- **解题钥匙**：**“只关注局部最新状态”**，而不是整个子结构。

---

## 反思

- **第一反应**：看到“第 i 次操作要比较 arr1、arr2 的最后一个元素”，立刻想到用两个列表逐步模拟。  
- **最容易踩的坑**：  
  - 忘记 **1‑indexed** 的描述，导致把 `nums[0]`、`nums[1]` 当成第 0、1 步。  
  - 当 `n == 2`（虽然题目最小 n 为 3）时，需要先判断是否有第二步；本题约束已排除这种情况。  
  - 对空列表使用 `list[-1]` 会报错，必须保证 `arr1`、`arr2` 已经有元素再比较。  
- **下次遇到同类题**，第一步应该：**明确每一步只需要哪些“局部信息”，把它们保存下来，避免全遍历**。这样往往能直接得到 O(n) 的线性解。