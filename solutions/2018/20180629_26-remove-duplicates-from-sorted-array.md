# #26. 删除有序数组中的重复元素 / Remove Duplicates from Sorted Array

> 难度：简单 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.
Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:
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
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Example 3:**

```
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order.

---

## 题目（中文翻译）

**描述**  
给定一个按非递减顺序（non‑decreasing order）排序的整数数组 `nums`，请原地（in‑place）删除其中的重复元素，使得每个唯一元素仅出现一次。数组中元素的相对顺序必须保持不变。函数返回 `nums` 中唯一元素的个数 `k`。

**评判方式**  
题目采用自定义判题（Custom Judge）。判题代码大致如下：

```java
int[] nums = [...]; // 输入数组
int[] expectedNums = [...]; // 正确答案（长度已裁剪）

int k = removeDuplicates(nums); // 调用你的实现

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

只要所有断言都通过，即可通过判题。

**示例**

**示例 1**  
（代码片段略）

**示例 2**  
```text
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: 你的函数应返回 k = 2，且 `nums` 前两个位置分别为 1 和 2。返回 k 之后的元素可以任意（因此示例中用下划线表示）。
```

**示例 3**  
```text
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: 你的函数应返回 k = 5，且 `nums` 前五个位置分别为 0、1、2、3、4。返回 k 之后的元素可以任意（用下划线表示）。
```

**约束条件**  

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `nums` 已按非递减顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历整个位数组，把所有出现的数字都记录下来，只保留第一次出现的那个**。  
可以用一个「哈希表」来记住已经出现过的值，哈希表就像一本字典，**key** 是数字本身，**value** 可以随便设（这里我们只关心有没有这个 key）。  

具体步骤：

1. 从左到右依次看 `nums[i]`。  
2. 判断这个数字是否已经在哈希表里出现过  
   - 没出现过 → 把它加入哈希表，同时把它拷贝到结果数组的下一个位置。  
   - 出现过 → 什么都不做，直接跳到下一个元素。  
3. 最后返回结果数组的长度 `k`。

因为题目要求**原地**修改（in‑place），我们可以在原数组上直接写入唯一元素，只是为了阐明思路，这里先用额外的数组来演示「最笨」的办法。

> **为什么正确？**  
> 哈希表保证了每个数字只会被计数一次；遍历整个数组保证所有元素都被检查到；把第一次出现的数字依次写入前部，最终得到的序列正是去重后的结果。

#### 代码（Python）

```python
from typing import List

def removeDuplicates_brute(nums: List[int]) -> int:
    """
    暴力版：使用哈希表记录出现过的数字
    返回去重后数组的长度（前 k 位是唯一元素）
    """
    seen = set()               # 哈希表，记录已经出现的数字
    write = 0                  # 写指针，指向下一个要写入的位置

    for num in nums:           # 逐个遍历原数组
        if num not in seen:    # 只处理第一次出现的数字
            seen.add(num)      # 把它加入哈希表
            nums[write] = num  # 把唯一元素写到前面
            write += 1         # 写指针右移

    return write               # write 正好是唯一元素的个数
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `n` 是数组长度。我们只遍历了一遍，每次查找/插入哈希表平均是 `O(1)`，所以整体是线性时间。  
  （如果把「哈希表」换成「遍历已有元素」去判断是否重复，则会变成 `O(n²)`，因为每个元素都要和前面的所有元素比较一次。）
- **空间复杂度**：`O(n)`  
  需要额外的集合 `seen` 最多保存 `n` 个不同的数字，最坏情况下和原数组等大。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正的瓶颈不在时间**（已经是 `O(n)`），而在**空间**——题目要求**原地**去重，不能额外使用 `O(n)` 的哈希表。  

观察题目关键条件：

- 输入数组是**非递减有序**的。  
- 相同的数字一定会**挨在一起**（就像排队买票，排在同一个窗口的都是同一个人）。

利用有序这一点，我们可以用 **双指针**（Two Pointers）技巧：

1. **慢指针 `slow`**：指向已经确认唯一的元素的最后位置（即下一个唯一元素要写入的位置）。  
2. **快指针 `fast`**：遍历整个数组，寻找下一个**不同**于 `nums[slow]` 的元素。  

当 `nums[fast] != nums[slow]` 时，说明 `fast` 位置的元素是一个新的唯一值：

- `slow += 1`（把慢指针右移到下一个空位）  
- `nums[slow] = nums[fast]`（把新发现的唯一值写进去）

遍历结束后，`slow + 1` 就是去重后数组的长度 `k`。

> **类比**：把数组想象成一条装满盒子的传送带，盒子里可能有相同的玩具。我们让一个工人（慢指针）只把每种玩具的**第一个**搬到左边的展示台上，另一个工人（快指针）不停跑来跑去，找出下一个**新玩具**，交给前面的工人摆放。

#### 代码（Python）

```python
from typing import List

def removeDuplicates(nums: List[int]) -> int:
    """
    双指针原地去重（官方最优解）
    返回唯一元素的个数 k，前 k 位即为去重后的数组
    """
    if not nums:               # 防止空数组（虽然题目保证长度≥1）
        return 0

    slow = 0                    # 慢指针：指向已确认唯一元素的最后位置
    # fast 从下标 1 开始，因为下标 0 已经是第一个唯一元素
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:   # 发现新元素
            slow += 1                  # 慢指针右移到下一个空位
            nums[slow] = nums[fast]    # 把新元素写进去

    # slow 是下标，长度要加 1
    return slow + 1
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每次比较、赋值都是常数时间。与暴力解的时间相同，但**没有额外的哈希表**，更符合题目要求。

- **空间复杂度**：`O(1)`  
  只用了两个整数变量 `slow`、`fast`，不随输入规模增长，真正实现了**原地**操作。

---

## 心得

- **核心技巧**：**双指针**（Two Pointers）在有序数组上去重/筛选的经典应用。  
- **适用题型**：
  1. *删除有序数组中的特定元素*（LeetCode 27）  
  2. *合并两个有序数组*（LeetCode 88）  
  3. *有序数组的平方后排序*（LeetCode 977）  
- **一句话总结**：  
  “有序数组 → 相同元素相邻 → 用慢指针记录唯一位置，快指针寻找下一个不同的元素。”

---

## 反思

- **第一反应**：看到“已排序”“去重”，立刻想到“相邻相等的可以直接跳过”，于是想到哈希表或集合。  
- **最容易踩的坑**：
  - **边界条件**：空数组或长度为 1 的数组，需要单独处理，否则 `slow`/`fast` 的初始化会出错。  
  - **指针位置**：`slow` 必须指向已确认唯一元素的**最后位置**，返回时要 `slow + 1` 才是元素个数。  
  - **原地修改**：不要在遍历时删除元素（`pop`），那会导致索引错位，使用覆盖写入更安全。  
- **下次遇到同类题**：  
  “先确认数组是否有序，若有序就立刻考虑双指针；若无序，则先排序或使用哈希结构”。