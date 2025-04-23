# #3158. 出现两次的数字的异或 / Find the XOR of Numbers Which Appear Twice

> 难度：简单 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-the-xor-of-numbers-which-appear-twice/)

---

## 题目（英文原版）

**Description**

You are given an array nums, where each number in the array appears either once or twice.
Return the bitwise XOR of all the numbers that appear twice in the array, or 0 if no number appears twice.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,3]
Output: 1
Explanation:
The only number that appears twice in nums is 1.
```

**Example 2:**

```
Input: nums = [1,2,3]
Output: 0
Explanation:
No number appears twice in nums .
```

**Example 3:**

```
Input: nums = [1,2,2,1]
Output: 3
Explanation:
Numbers 1 and 2 appeared twice. 1 XOR 2 == 3 .
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= 50
- Each number in nums appears either once or twice.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其中每个数字要么出现一次，要么出现两次。  
返回所有出现两次的数字的按位异或（bitwise XOR）结果；如果没有数字出现两次，则返回 `0`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 50`
- `nums` 中的每个数字要么出现一次，要么出现两次。

**示例**

**示例 1:**  
```
Input: nums = [1,2,1,3]
Output: 1
Explanation:
唯一出现两次的数字是 1。
```

**示例 2:**  
```
Input: nums = [1,2,3]
Output: 0
Explanation:
没有数字出现两次。
```

**示例 3:**  
```
Input: nums = [1,2,2,1]
Output: 3
Explanation:
数字 1 和 2 都出现了两次。1 XOR 2 == 3 。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把数组里每个数都去“数一遍”，看它出现了几次：

1. 取出数组中的第 `i` 个元素 `nums[i]`。  
2. 再遍历一遍整个数组，统计 `nums[i]` 出现了多少次。  
3. 如果出现 **恰好两次**，就把它加入答案的 XOR 中。  

这里用到的唯一数据结构是 **普通的列表**（数组本身），没有额外的空间需求。  
把它想象成我们在超市里手动点数每件商品的数量——虽然慢，但一定能得到正确的结果。

> 为什么能对每个数都完整遍历就一定对？  
> 因为题目保证每个数最多出现两次，只要我们把出现次数算清楚，就能判断它是否是“出现两次的数”，进而做 XOR。

#### 代码（Python）

```python
def xor_of_twice(nums):
    """返回所有出现两次的数的 XOR，若没有则返回 0"""
    ans = 0                     # 最终的异或结果，初始为 0（因为 0 与任何数异或不改变它）
    n = len(nums)

    for i in range(n):          # 把每个位置的数都检查一遍
        cnt = 0                  # 统计 nums[i] 出现的次数
        for j in range(n):      # 再遍历一次整个数组计数
            if nums[j] == nums[i]:
                cnt += 1
        # 如果恰好出现两次，就把它加入异或
        if cnt == 2:
            ans ^= nums[i]      # ^ 是 Python 中的位异或运算符
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - “n²” 可以想象成“每个人都要和所有人握手”。这里 `n` 最多只有 50，虽然慢，但仍在可接受范围内。  
- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量（`ans、cnt、i、j`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个数都要再遍历一次**，导致整体是 `n²`。我们可以把“数出现几次”这一步提前做好，做到 **一次遍历** 就得到所有信息。

思路如下：

1. **使用集合（Set）记录已经出现一次的数**。  
   - 集合像一本**字典**，把已经看到的单次出现的数字记下来，查找和插入的速度都是 `O(1)`（想象在字典里查词的速度）。  
2. 再遍历数组 `nums`：  
   - 如果当前数 **不在集合**，说明是第一次出现，加入集合。  
   - 如果当前数 **已经在集合**，说明这是第二次出现（题目保证不会出现三次），这时把它 **XOR 到答案**，并把它从集合中移除（这样后面再碰到同一个数就不会重复计入）。  

这样只需要 **一次遍历**，时间从 `O(n²)` 降到 `O(n)`，额外的集合最多存 `n` 个元素，空间是 `O(n)`。  

因为题目中数值范围只有 `1~50`，我们甚至可以用长度为 `51` 的计数数组（类似“记事本”）把空间降到 `O(1)`，但这里先用集合让概念更直观。

#### 代码（Python）

```python
def xor_of_twice(nums):
    """一次遍历求出现两次的数的 XOR，若没有则返回 0"""
    seen_once = set()   # 用来记录出现过一次的数，相当于“字典的钥匙”
    ans = 0

    for x in nums:      # 只遍历一次数组
        if x not in seen_once:          # 第一次出现
            seen_once.add(x)            # 把它记下来
        else:                            # 第二次出现
            ans ^= x                     # 把它加入异或结果
            seen_once.remove(x)         # 已经处理完，移除避免以后重复计入

    return ans
```

> **关键点解释**  
> - `set` 的 `add`、`remove`、`in` 操作在 Python 中都是 **常数时间**（O(1)），相当于在字典里快速查找/写入。  
> - `ans ^= x` 表示把当前找到的第二次出现的数与答案进行位异或，异或的性质保证相同的数只会保留一次。

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次数组，想象成“一次全员点名”。相比暴力的 `n²`，速度提升显著。  
- **空间复杂度：** `O(n)`（最坏情况集合里会有 `n/2` 个只出现一次的数）  
  - 这里的空间是线性的，但因为 `n ≤ 50`，实际占用也很小。若使用计数数组，则可以降到 `O(1)`（固定大小 51 的列表）。

---

## 心得

- **核心技巧**：利用 **集合（哈希表）** 记录已经出现一次的元素，从而在一次遍历中找出出现两次的元素并直接进行 XOR。  
- **适用的题型**：  
  1. “找出只出现一次的数”（LeetCode 136）——使用异或或集合。  
  2. “找出所有出现两次的数”或“出现三次的数”——同样可以用哈希表计数。  
- **解题钥匙**：**把“出现次数统计”提前做，只要一次遍历就能得到答案**。

---

## 反思

- **第一反应**：看到“出现一次或两次”，本能想到**计数**，于是想先遍历统计每个数出现的次数。  
- **最容易踩的坑**：  
  - 忘记 **只对出现两次的数做 XOR**，而是把所有数都异或，容易得到错误答案。  
  - 在集合中没有把第二次出现的数移除，导致后面如果出现第三次（虽然题目不允许）会再次被计入。  
- **下次类似题的第一步**：先思考**有没有可以在一次遍历中完成计数的结构**（集合、哈希表或固定大小计数数组），再决定是用计数还是直接在遍历时完成所需的运算（如 XOR）。