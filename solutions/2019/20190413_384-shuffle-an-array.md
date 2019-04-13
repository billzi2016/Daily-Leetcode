# #384. 打乱数组 / Shuffle an Array

> 难度：中等 · 标签：Array、Math、Design、Randomized · [LeetCode 链接](https://leetcode.com/problems/shuffle-an-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, design an algorithm to randomly shuffle the array. All permutations of the array should be equally likely as a result of the shuffling.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
Output
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

Explanation
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // Shuffle the array [1,2,3] and return its result.
                       // Any permutation of [1,2,3] must be equally likely to be returned.
                       // Example: return [3, 1, 2]
solution.reset();      // Resets the array back to its original configuration [1,2,3]. Return [1, 2, 3]
solution.shuffle();    // Returns the random shuffling of array [1,2,3]. Example: return [1, 3, 2]
```

**Constraints**

- 1 <= nums.length <= 50
- -106 <= nums[i] <= 106
- All the elements of nums are unique.
- At most 104 calls in total will be made to reset and shuffle.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，设计一种算法来 **随机打乱（shuffle）** 该数组。打乱后，数组的所有排列（permutations）出现的概率应当相等。

实现 `Solution` 类，使其能够：

- `reset()`：将数组恢复到最初的状态并返回该数组。
- `shuffle()`：返回数组的一个随机排列。

**示例 1**

```text
Input
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]

Output
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]
```

**解释**

```java
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // 随机打乱数组 [1,2,3] 并返回结果。
                       // 任意排列 [1,2,3] 的出现概率必须相等。
                       // 示例返回 [3, 1, 2]。
solution.reset();      // 将数组恢复到初始状态 [1,2,3]，返回 [1, 2, 3]。
solution.shuffle();    // 再次返回数组的随机打乱结果，例如返回 [1, 3, 2]。
```

**约束条件**

- `1 <= nums.length <= 50`
- `-10^6 <= nums[i] <= 10^6`
- `nums` 中的所有元素互不相同。
- `reset` 和 `shuffle` 的调用总次数不超过 `10^4`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的排列都列出来**，然后随机挑选其中一个返回。  
- **数据结构**：我们可以用 Python 的 `list` 来存放一个排列，用 `list of list`（即列表的列表）来存放所有排列。  
- **生活化类比**：把数组想成一副牌，所有可能的洗牌方式就像把这副牌全部摆成一排排的“花样”。我们先把所有花样写在纸上（即生成全部排列），再闭上眼睛随机抽一张。  
- **正确性**：因为我们把**所有**合法的排列都列了出来，随后用等概率的方式抽取，所以每一种排列出现的概率都是相同的，满足题目要求。  

#### 代码（Python）  

```python
import random
import itertools
from copy import deepcopy

class Solution:
    def __init__(self, nums):
        # 保存原始数组的副本，后面 reset 要用
        self.original = deepcopy(nums)

    def reset(self):
        """返回最初的数组"""
        return deepcopy(self.original)

    def shuffle(self):
        """
        暴力做法：先生成所有排列，然后随机挑一个返回。
        这里使用 itertools.permutations 来一次性得到所有排列。
        """
        # 1️⃣ 生成所有排列（每个排列是一个 tuple）
        all_perms = list(itertools.permutations(self.original))
        # 2️⃣ 随机选一个下标
        idx = random.randint(0, len(all_perms) - 1)
        # 3️⃣ 把 tuple 转成 list 再返回
        return list(all_perms[idx])
```

> **关键行解释**  
> - `itertools.permutations(self.original)`：把数组的所有排列一次性生成出来。  
> - `random.randint(0, len(all_perms) - 1)`：在这些排列里等概率抽取一个。  

#### 复杂度  

- **时间复杂度**：`O(n! )`  
  - 生成全部排列的代价是 n 的阶乘（n!），因为排列的个数就是 n!。  
  - 对于 n=3，排列数是 6；但 n=10 时已经是 3,628,800，明显不可接受。  
- **空间复杂度**：`O(n! )`  
  - 需要把所有排列都存到内存里，同样是 n! 级别的空间。  

> **大白话**：`O(n!)` 就像“把所有可能的排队顺序都写下来”，人数越多，写的纸就会指数级增长，根本写不完。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**提前生成所有排列**，这既耗时又耗内存。  
我们只需要**一次遍历**就能把数组随机打乱，这就是**Fisher‑Yates 洗牌算法**（也叫 Knuth 洗牌）。  

核心思想：  
1. 从左到右遍历数组的每个位置 `i`（从 0 开始）。  
2. 在当前位置 `i` 之后（包括自己）的区间 `[i, n-1]` 中**随机挑选一个下标 `j`**。  
3. 把 `i` 和 `j` 两个位置的元素**互换**。  

这样做的好处是：  
- 第一步决定第 0 位的最终元素，它在所有 `n` 个位置中等概率出现。  
- 第二步决定第 1 位的最终元素，它在剩下的 `n-1` 个位置中等概率出现，……  
- 最后一步只剩下一个位置，不需要再换。  

因为每一步的随机选择都是等概率的，**所有排列出现的概率相同**，满足题目要求。

**生活化类比**：想象有一堆不同颜色的球排成一行，你从左到右依次抽取“剩下的球里随便挑一个”，把抽到的球放到当前的位置上，抽完后球的顺序就是一次公平的随机洗牌。

#### 代码（Python）  

```python
import random
from copy import deepcopy

class Solution:
    def __init__(self, nums):
        # 保存一份原始数组的拷贝，reset 时直接返回它
        self.original = deepcopy(nums)

    def reset(self):
        """恢复到最初的数组"""
        return deepcopy(self.original)

    def shuffle(self):
        """
        Fisher‑Yates 洗牌（Knuth Shuffle）。
        思路：从左到右遍历，每次把当前位置 i 与 i~n-1 区间内随机选的下标 j 互换。
        这样所有排列出现的概率都是 1/n!。
        """
        # 先拷贝一份数组，这样不改动原始数据
        arr = deepcopy(self.original)
        n = len(arr)

        for i in range(n):
            # 在 i ~ n-1 之间随机选一个下标
            j = random.randint(i, n - 1)
            # 交换位置 i 和 j 的元素
            arr[i], arr[j] = arr[j], arr[i]

        return arr
```

> **关键行解释**  
> - `random.randint(i, n - 1)`：保证只在当前未确定的位置里抽取，等概率。  
> - `arr[i], arr[j] = arr[j], arr[i]`：Python 的“一行交换”，把两个位置的数互换。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，`n` 次随机数生成和交换，线性时间。  
- **空间复杂度**：`O(n)`（如果算返回的新数组）  
  - 需要额外拷贝一份数组来避免修改 `original`，这占用 `n` 个元素的空间。  
  - 若在原地修改（不需要保持 `original`），空间可以降到 `O(1)`。  

> 与暴力解相比：时间从“指数级”降到了“线性”，空间也从“指数级”降到了“线性”。  

---

## 心得  

- **核心技巧**：Fisher‑Yates 洗牌——一次遍历、在未确定区间随机挑选并交换，保证每个排列等概率。  
- **适用的题型**：  
  1. 需要在 **O(1)** 额外空间内随机抽样的题目（如「随机从数组中抽取 k 个不重复元素」）。  
  2. **随机重排** 类的问题（如「打乱链表」的思路可以借鉴）。  
  3. 需要 **均匀抽样** 的概率统计题（如「抽签」模拟）。  
- **一句话总结**：**一次遍历、随机交换，就是公平洗牌的钥匙**。  

---

## 反思  

- **第一反应**：先把所有排列列出来再抽，想到的最直观但不够高效。  
- **最容易踩的坑**：  
  - **使用已经打乱的数组继续 shuffle**：如果在 `shuffle` 中直接在 `self.original` 上操作，会导致后续 `reset` 失效，或多次 shuffle 结果不均匀。  
  - **随机区间写错**：必须在 `[i, n-1]` 之间随机，而不是 `[0, n-1]`，否则会破坏已经确定好的前缀，导致排列概率不均。  
  - **忘记拷贝原数组**：`reset` 必须返回最初的顺序，直接返回内部数组会因为 shuffle 后被修改而出错。  
- **下次类似题的第一步**：先思考**是否真的需要生成所有组合**，如果只是要“随机且均匀”，就考虑 **Fisher‑Yates** 这类“一次遍历” 的原地算法。