# #80. 从有序数组中删除重复项 II / Remove Duplicates from Sorted Array II

> 难度：中等 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.
Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.
Return k after placing the final result in the first k slots of nums.
Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.
Custom Judge:
The judge will test your solution with the following code:
If all assertions pass, then your solution will be accepted.

**Examples**

**Example 1:**

```
int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

**Example 2:**

```
Input: nums = [1,1,1,2,2,3]
Output: 5, nums = [1,1,2,2,3,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Example 3:**

```
Input: nums = [0,0,1,1,1,1,2,3,3]
Output: 7, nums = [0,0,1,1,2,3,3,_,_]
Explanation: Your function should return k = 7, with the first seven elements of nums being 0, 0, 1, 1, 2, 3 and 3 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- -104 <= nums[i] <= 104
- nums is sorted in non-decreasing order.

---

## 题目（中文翻译）

给定一个按 **非递减顺序**（non-decreasing order）排序的整数数组 `nums`，请 **就地**（in-place）删除部分重复元素，使得每个唯一元素至多出现两次。数组中元素的 **相对顺序**（relative order）必须保持不变。  

由于某些语言无法改变数组的长度，你必须把处理后的结果放在数组 `nums` 的前部。更形式化地说，如果删除重复后数组中有 `k` 个元素，则 `nums` 的前 `k` 个位置应存放最终结果，`k` 之后的内容可以任意。  

返回 `k`，即最终有效元素的数量。  

要求：

- 不得为另一个数组分配额外空间，必须使用 **O(1)** 额外内存 **就地**（in-place）修改输入数组。  

### 自定义判题器  
判题器会使用以下代码测试你的实现：  

```java
// 如果所有断言都通过，则你的解答会被接受
int[] nums = [...];               // 输入数组
int[] expectedNums = [...];       // 正确答案（包含正确的长度）

int k = removeDuplicates(nums);  // 调用你的实现

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

### 示例  

#### 示例 1  
```java
int[] nums = [...]; // 输入数组
int[] expectedNums = [...]; // 期望的答案（包含正确的长度）

int k = removeDuplicates(nums); // 调用你的实现

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

#### 示例 2  
**输入**：`nums = [1,1,1,2,2,3]`  
**输出**：`5, nums = [1,1,2,2,3,_]`  
**解释**：函数应返回 `k = 5`，并且 `nums` 前五个元素分别为 `1, 1, 2, 2, 3`。`k` 之后的内容可以任意（因此这里用下划线表示）。

#### 示例 3  
**输入**：`nums = [0,0,1,1,1,1,2,3,3]`  
**输出**：`7, nums = [0,0,1,1,2,3,3,_,_]`  
**解释**：函数应返回 `k = 7`，并且 `nums` 前七个元素分别为 `0, 0, 1, 1, 2, 3, 3`。`k` 之后的内容可以任意（用下划线表示）。

### 约束条件  

- `1 <= nums.length <= 3 * 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` 按 **非递减顺序**（non-decreasing order）排序。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目要求在 **已排序** 的数组 `nums` 中，最多保留每个不同数字出现两次，并且要 **原地** 修改数组。  
最直接的想法是：  
1. 先遍历整个数组，统计每个数字出现了几次（可以用 Python 的 `dict`，相当于把字典想象成 **查字典**：单词是 `key`，对应的页码是 `value`）。  
2. 再遍历 `nums`，把出现次数 ≤ 2 的元素依次写回数组的前面。  

因为我们先把所有出现次数记录下来，再把合法的元素挑出来，所以一定能得到正确答案。  

**为什么正确**  
- 统计阶段得到每个数字的真实出现次数。  
- 只把出现次数不超过两次的元素写回，恰好满足 “每个唯一元素最多出现两次”。  

**时间/空间复杂度**  
- 第一次遍历统计次数是 `O(n)`，第二次遍历写回也是 `O(n)`，所以总时间是 `O(2n) ≈ O(n)`。  
- 需要一个哈希表保存每个不同数字的计数，最坏情况下每个元素都不相同，需要 `O(n)` 的额外空间。  

> **大白话**：如果数组有 10 万个元素，暴力解大概会跑两遍 10 万次的循环，时间还行；但它会额外开出一张“字典表”，大小和原数组差不多，这在要求 **O(1) 额外空间** 时是不被允许的。

#### 代码（Python）  

```python
from typing import List

def removeDuplicates_bruteforce(nums: List[int]) -> int:
    """
    暴力解：先统计每个数字出现次数，再把合法的元素写回数组前部
    """
    # 1️⃣ 统计出现次数，像查字典一样，key 是数字，value 是出现次数
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1          # get 如果找不到就返回 0

    # 2️⃣ 重新写回合法元素
    write = 0                                   # 写指针，指向下一个要写的位置
    for x in nums:
        if count[x] <= 2:                       # 只保留出现次数 ≤ 2 的元素
            nums[write] = x
            write += 1
            count[x] -= 1                       # 已写入一次后，出现次数减 1
            # 这样同一个数字最多会写两次
    return write                                # 前 write 个元素就是答案
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历了两遍数组，`n` 是数组长度。  
- **空间复杂度**：`O(n)` —— 需要一个哈希表保存每个不同数字的计数，最坏情况下和原数组等大。  

---

### 2. 最优解  

#### 思路  
暴力解的 **瓶颈** 在于额外的哈希表。因为数组本身已经是 **非递减有序** 的，我们可以直接利用这个特性，**不需要额外空间**。  

**核心想法：双指针**  
- **慢指针 `slow`**：指向已处理好的、满足“每个元素出现不超过两次”的子数组的最后一个位置。最终 `slow + 1` 就是答案的长度 `k`。  
- **快指针 `fast`**：遍历原数组，寻找可以加入子数组的元素。  

由于每个数字最多出现两次，我们只需要检查 **当前元素 `nums[fast]` 与子数组中倒数第三个元素 `nums[slow-1]` 的关系**：  
- 如果 `nums[fast]` 与 `nums[slow-1]` 不同，说明即使已经出现两次（因为 `slow` 已经指向了前面两次），再出现一次也不会超过两次，可以安全写入。  
- 具体来说：当 `slow < 1`（子数组长度不足 2）时，直接写入；否则检查 `nums[fast] != nums[slow-1]`。  

**一步步推导**  
1. 初始化 `slow = 0`（子数组已放置第一个元素），`fast` 从下标 1 开始。  
2. 对每个 `fast`：  
   - 如果 `slow < 1`（子数组只有 0/1 个元素）或 `nums[fast] != nums[slow-1]`，则说明 `nums[fast]` 可以加入。  
   - 把 `nums[fast]` 复制到 `nums[slow+1]`，`slow += 1`。  
3. 循环结束后，`slow + 1` 就是最终长度 `k`。  

**为什么正确**  
- `nums[slow-1]` 正好是当前子数组中 **倒数第二个** 元素（因为子数组长度 ≥ 2 时 `slow-1` 为倒数第二）。  
- 当 `nums[fast]` 与倒数第二个元素相同，说明已经有两个相同的数在子数组末尾，再加入会导致出现三次，违反要求。  
- 当它们不同，说明即使子数组末尾已经有两个相同的数（可能是别的值），当前数是新的或是第一次/第二次出现，安全加入。  

**类比**：想象你在排队买票，规则是每个人最多只能买两张票。`slow` 记录已经批准的票的最后一张位置，`fast` 负责检查下一个想买票的人。如果这个人已经买了两张（即前面已经有两个相同的名字），就让他等下次再来；否则批准并把他的票加入队列。

#### 代码（Python）  

```python
from typing import List

def removeDuplicates(nums: List[int]) -> int:
    """
    双指针解法：在已排序数组上原地保留每个元素至多出现两次
    """
    if not nums:                     # 空数组直接返回 0
        return 0

    # slow 指向已整理好的子数组的最后一个位置
    slow = 0                         # 已经确认的子数组长度为 slow+1

    # fast 从第二个元素开始遍历（下标 1）
    for fast in range(1, len(nums)):
        # 当子数组长度小于 2 时，直接放入；否则比较 nums[fast] 与 nums[slow-1]
        if slow < 1 or nums[fast] != nums[slow-1]:
            slow += 1                 # 把新元素放到子数组的下一个位置
            nums[slow] = nums[fast]   # 复制元素
        # 若相等且 slow>=1，则说明已经有两个相同的数，跳过此元素

    # 子数组长度 = slow + 1
    return slow + 1
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 为数组长度。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`slow`, `fast`），不随 `n` 增长。  

> 与暴力解对比：时间相同，但空间从 `O(n)` 降到了 `O(1)`，完全符合题目 “原地 O(1) 额外空间” 的要求。

---

## 心得  

- **核心技巧**：**双指针（慢指针/快指针）**，利用已排序的特性，只看「倒数第二个」元素就能判断是否可以加入。  
- **适用的题型**：  
  1. “删除有序数组中的重复元素” 系列（如 **Remove Duplicates from Sorted Array I**，只能保留一次）。  
  2. “有序数组中删除满足某种计数限制的元素” 如 “删除有序数组中的所有出现超过 k 次的元素”。  
  3. “滑动窗口” 类问题（比如 “最长子数组满足和 ≤ K”），也常用双指针。  
- **一句话总结**：**利用有序性，只比较当前元素与子数组中倒数第二个元素，就能在 O(1) 额外空间下完成去重**。

---

## 反思  

- **第一反应**：想到统计出现次数的哈希表，然后再筛选。虽然直观，却忽略了题目已经给出的有序信息。  
- **最容易踩的坑**：  
  - **边界条件**：数组长度为 0 或 1 时，需要单独处理，否则 `slow-1` 会越界。  
  - **判断条件**：必须比较 `nums[fast]` 与 `nums[slow-1]`（倒数第二个），而不是倒数第一个，否则会错误允许第三个相同元素。  
- **下次遇到同类题**，第一步应该先问自己：“数组有没有排序？如果有，能否只看前面几个元素的关系来决定是否保留当前元素？” 这通常能直接指向双指针或滑动窗口的最优思路。