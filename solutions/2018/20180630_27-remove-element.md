# #27. 删除元素 / Remove Element

> 难度：简单 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/remove-element/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.
Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:
Custom Judge:
The judge will test your solution with the following code:
If all assertions pass, then your solution will be accepted.

**Examples**

**Example 1:**

```
int[] nums = [...]; // Input array
int val = ...; // Value to remove
int[] expectedNums = [...]; // The expected answer with correct length.
                            // It is sorted with no values equaling val.

int k = removeElement(nums, val); // Calls your implementation

assert k == expectedNums.length;
sort(nums, 0, k); // Sort the first k elements of nums
for (int i = 0; i < actualLength; i++) {
    assert nums[i] == expectedNums[i];
}
```

**Example 2:**

```
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 2.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Example 3:**

```
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums containing 0, 0, 1, 3, and 4.
Note that the five elements can be returned in any order.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

**Constraints**

- 0 <= nums.length <= 100
- 0 <= nums[i] <= 50
- 0 <= val <= 100

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `val`，请 **原地**（in‑place）移除数组中所有等于 `val` 的元素。元素的顺序可以改变。随后返回数组中不等于 `val` 的元素个数 `k`。

为了通过评测，需要满足以下要求：

**自定义判题（Custom Judge）**  
评测程序会使用如下代码检验你的实现：

```java
int k = removeElement(nums, val); // 调用你的实现

assert k == expectedNums.length;
sort(nums, 0, k); // 对前 k 个元素进行排序
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

只要所有断言均通过，你的解法即被接受。

---

## 示例

### 示例 1

```java
int[] nums = [...];          // 输入数组
int val = ...;               // 待移除的值
int[] expectedNums = [...];  // 正确答案（已去除 val 并按长度截断），其中不含任何等于 val 的元素，且已排序。

int k = removeElement(nums, val); // 调用你的实现

assert k == expectedNums.length;
sort(nums, 0, k); // 对前 k 个元素进行排序
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

### 示例 2

**输入**: `nums = [3,2,2,3]`, `val = 3`  
**输出**: `2, nums = [2,2,_,_]`  

**解释**: 你的函数应返回 `k = 2`，且 `nums` 前两个位置的元素为 `2`。  
返回 `k` 之后数组剩余位置的内容不作要求（因此用下划线表示任意值）。

### 示例 3

**输入**: `nums = [0,1,2,2,3,0,4,2]`, `val = 2`  
**输出**: `5, nums = [0,1,4,0,3,_,_,_]`  

**解释**: 你的函数应返回 `k = 5`，且前五个元素分别为 `0, 1, 4, 0, 3`（顺序任意）。  
同样，`k` 之后的元素内容不影响结果（以下划线表示任意值）。

---

## 约束条件

- `0 <= nums.length <= 100`
- `0 <= nums[i] <= 50`
- `0 <= val <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历一遍数组，把所有等于 `val` 的元素直接删掉**，把后面的元素往前搬。  
可以把数组想象成一排座位，`val` 就是我们不想坐的那位客人。我们把不想要的客人请出去，然后把后面的客人往前挪，填补空位。

实现上有两种常见的写法：

1. **使用额外的列表**：把所有不等于 `val` 的元素收集到一个新列表，然后把新列表的内容复制回原数组。  
   - 这相当于把“不想要的客人”直接搬到别的房间，再把剩下的客人搬回原来的座位。  
2. **原地删除**：在遍历时每次遇到 `val` 就调用 `list.pop(i)`（或 `del nums[i]`），把该元素从列表中删掉，后面的元素会自动左移。  

这里我们采用第一种“额外列表”方式，因为它思路最清晰，适合作为暴力解的示例。

#### 代码（Python）

```python
def removeElement_brute(nums, val):
    """
    暴力解：使用额外列表收集所有非 val 元素，再复制回原数组
    """
    # 1️⃣ 收集：遍历原数组，把不是 val 的元素放进 new_list
    new_list = []                     # 新列表相当于“新座位”
    for x in nums:                    # 逐个检查每位客人
        if x != val:                  # 只保留不等于 val 的
            new_list.append(x)        # 把他放进新座位

    # 2️⃣ 复制回原数组：把 new_list 的内容写回 nums 前 k 位
    k = len(new_list)                 # k 是新数组的长度
    for i in range(k):                # 把新座位上的客人搬回原来的座位
        nums[i] = new_list[i]

    # 3️⃣ 返回新长度
    return k
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `n` 是数组长度。我们遍历了一遍原数组（`O(n)`），再遍历了一遍 `new_list`（最多也是 `n`），相加仍是线性时间。  
  大白话：如果数组有 1000 个数，程序大约会检查 2000 次（每个数检查一次，再写回一次），这在电脑眼里仍算“快”。

- **空间复杂度**：`O(n)`  
  需要额外的列表 `new_list` 来保存所有非 `val` 的元素，最坏情况下它会装下整个原数组。  
  大白话：相当于我们在原来的座位旁边额外准备了一排同样长的座位来临时存放客人。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现**最大的浪费在于额外的存储空间**（`O(n)` 的新列表）以及**两次遍历**。  
事实上，题目已经说明：

> “可以改变元素的顺序，返回前 k 个不等于 `val` 的元素即可，后面的内容随便。”

这暗示我们可以**原地（in‑place）完成**，不需要额外空间。  
核心技巧是**双指针（Two Pointers）**：

1. **慢指针 `i`**：指向当前已经确定好的、非 `val` 元素的下一个位置。相当于我们已经整理好的座位的“末尾”。  
2. **快指针 `j`**：遍历整个数组，寻找下一个不是 `val` 的元素。相当于我们在整排座位里走动，找出可以留下的客人。

当 `nums[j] != val` 时，把它搬到 `nums[i]` 的位置，然后 `i` 前进一步。  
如果 `nums[j] == val`，我们什么也不做，只让 `j` 前进，等以后有合适的元素再填补 `i` 位置。

因为可以**把要删除的元素直接覆盖掉**，所以不需要额外空间，且只遍历一次数组。

> **类比**：想象一条装满水果的传送带，传送带上有一些烂水果（值等于 `val`）。我们让两个工人站在传送带上：左边的工人负责把好水果装进箱子（`i`），右边的工人负责检查水果（`j`）。每当右边工人看到好水果，就把它交给左边工人装箱；看到烂水果就直接让它继续往前走，最终箱子里装的全是好水果。

#### 代码（Python）

```python
def removeElement(nums, val):
    """
    双指针原地删除：一次遍历、O(1) 额外空间
    """
    i = 0                     # 慢指针：下一个可以放置非 val 元素的位置
    for j in range(len(nums)):   # 快指针：遍历整个数组
        if nums[j] != val:        # 只关心不是 val 的元素
            nums[i] = nums[j]     # 把它搬到位置 i（可能是原位，也可能是前面腾出来的空位）
            i += 1                # i 前进一步，准备下一个位置
    return i                      # i 正好等于新数组的长度 k
```

> **关键行解释**  
> - `i = 0`：从数组开头开始准备填充。  
> - `if nums[j] != val:`：只在遇到“好水果”时才动手。  
> - `nums[i] = nums[j]`：把好水果搬到左边已经整理好的位置。  
> - `i += 1`：左边的“箱子”已经装满一个好水果，准备装下一个。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，`n` 为数组长度。相当于只检查每个客人一次，快得多。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（`i`, `j`），不随输入规模增长。相当于我们不需要额外的座位，只在原来的座位上搬动。

与暴力解对比：**时间相同但空间从 `O(n)` 降到 `O(1)`**，这正是最优解的关键提升。

---

## 心得

- **核心技巧**：双指针原地修改（Two‑Pointer In‑Place）。  
- **适用题型**：  
  1. 移除数组中满足条件的元素（如本题）。  
  2. 删除有序数组中的重复元素（LeetCode 26）。  
  3. 合并两个已排序数组到一个数组中（LeetCode 88 的变形）。  
- **一句话总结**：**把“要删除的”当作空位，用另一个指针把“留下的”填进去，遍历一次即可**。

---

## 反思

- **第一反应**：直接遍历、把不想要的元素删掉或新建列表保存剩余元素。  
- **最容易踩的坑**：  
  - 忘记返回新长度 `k`，导致判题时只检查前 `k` 个元素。  
  - 误以为必须保持原数组顺序，其实题目允许顺序改变，利用这一点可以更自由地搬移元素。  
  - 在原地删除时，如果在遍历时直接使用 `pop(i)`，会导致下标错位或遗漏元素。  
- **下次遇到同类题**：第一步先问自己“是否可以在原地、一次遍历完成？”如果答案是“可以”，就立刻想到双指针或快慢指针的思路。