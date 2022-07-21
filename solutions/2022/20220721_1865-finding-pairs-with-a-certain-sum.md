# #1865. 寻找满足特定和的数对 / Finding Pairs With a Certain Sum

> 难度：中等 · 标签：Array、Hash Table、Design · [LeetCode 链接](https://leetcode.com/problems/finding-pairs-with-a-certain-sum/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2. You are tasked to implement a data structure that supports queries of two types:
Implement the FindSumPairs class:

**Examples**

**Example 1:**

```
Input
["FindSumPairs", "count", "add", "count", "count", "add", "add", "count"]
[[[1, 1, 2, 2, 2, 3], [1, 4, 5, 2, 5, 4]], [7], [3, 2], [8], [4], [0, 1], [1, 1], [7]]
Output
[null, 8, null, 2, 1, null, null, 11]

Explanation
FindSumPairs findSumPairs = new FindSumPairs([1, 1, 2, 2, 2, 3], [1, 4, 5, 2, 5, 4]);
findSumPairs.count(7);  // return 8; pairs (2,2), (3,2), (4,2), (2,4), (3,4), (4,4) make 2 + 5 and pairs (5,1), (5,5) make 3 + 4
findSumPairs.add(3, 2); // now nums2 = [1,4,5,4,5,4]
findSumPairs.count(8);  // return 2; pairs (5,2), (5,4) make 3 + 5
findSumPairs.count(4);  // return 1; pair (5,0) makes 3 + 1
findSumPairs.add(0, 1); // now nums2 = [2,4,5,4,5,4]
findSumPairs.add(1, 1); // now nums2 = [2,5,5,4,5,4]
findSumPairs.count(7);  // return 11; pairs (2,1), (2,2), (2,4), (3,1), (3,2), (3,4), (4,1), (4,2), (4,4) make 2 + 5 and pairs (5,3), (5,5) make 3 + 4
```

**Constraints**

- 1 <= nums1.length <= 1000
- 1 <= nums2.length <= 105
- 1 <= nums1[i] <= 109
- 1 <= nums2[i] <= 105
- 0 <= index < nums2.length
- 1 <= val <= 105
- 1 <= tot <= 109
- At most 1000 calls are made to add and count each.

---

## 题目（中文翻译）

**描述**  
给定两个整数数组 `nums1` 和 `nums2`。请实现一个数据结构，支持以下两类查询：

- `add(index, val)`：将 `nums2[index]` 增加 `val`（`val` 为正整数）。
- `count(tot)`：返回满足 `nums1[i] + nums2[j] == tot` 的数对 `(i, j)` 的数量，其中 `i` 是 `nums1` 的下标，`j` 是 `nums2` 的下标。

实现 `FindSumPairs` 类，使上述操作的时间复杂度尽可能低。

**示例**  
```text
输入
["FindSumPairs", "count", "add", "count", "count", "add", "add", "count"]
[[[1, 1, 2, 2, 2, 3], [1, 4, 5, 2, 5, 4]], [7], [3, 2], [8], [4], [0, 1], [1, 1], [7]]
输出
[null, 8, null, 2, 1, null, null, 11]
```

**解释**  
```java
FindSumPairs findSumPairs = new FindSumPairs([1, 1, 2, 2, 2, 3], [1, 4, 5, 2, 5, 4]);
findSumPairs.count(7);  // 返回 8；满足的数对有 (2,2), (3,2), (4,2), (2,4), (3,4), (4,4) 等
findSumPairs.add(3, 2); // 将 nums2[3] 增加 2，数组变为 [1, 4, 5, 4, 5, 4]
findSumPairs.count(8);  // 返回 2
findSumPairs.count(4);  // 返回 1
findSumPairs.add(0, 1); // 将 nums2[0] 增加 1，数组变为 [2, 4, 5, 4, 5, 4]
findSumPairs.add(1, 1); // 将 nums2[1] 增加 1，数组变为 [2, 5, 5, 4, 5, 4]
findSumPairs.count(7);  // 返回 11
```

**约束条件**  

- `1 <= nums1.length <= 1000`
- `1 <= nums2.length <= 10^5`
- `1 <= nums1[i] <= 10^9`
- `1 <= nums2[i] <= 10^5`
- `0 <= index < nums2.length`
- `1 <= val <= 10^5`
- `1 <= tot <= 10^9`
- `add` 与 `count` 的调用次数各不超过 `1000` 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：每次有人调用 `count(tot)`，我们就把 `nums1` 和 `nums2` 中的所有元素两两配对，看看有多少对满足 `nums1[i] + nums2[j] == tot`。  
- **用到的数据结构**：仅仅是两个普通的 Python 列表（`list`），不需要额外的容器。可以把它想象成我们在厨房里把两盘水果（一个装 `nums1`，一个装 `nums2`）全部摆出来，然后手动数一遍所有可能的“水果 + 水果”组合。  
- **为什么正确**：因为我们枚举了所有可能的 `(i, j)`，只要有一对满足等式，就一定会被统计进去。  

#### 代码（Python）  
```python
class FindSumPairs:
    def __init__(self, nums1, nums2):
        # 直接保存原始数组，后面 add 需要改动 nums2
        self.nums1 = nums1
        self.nums2 = nums2

    def count(self, tot: int) -> int:
        """暴力枚举所有 (i, j) 并计数"""
        ans = 0
        for a in self.nums1:          # 遍历 nums1 的每个元素
            for b in self.nums2:      # 遍历 nums2 的每个元素
                if a + b == tot:      # 检查是否满足目标和
                    ans += 1
        return ans

    def add(self, index: int, val: int) -> None:
        """直接把 nums2[index] 加上 val"""
        self.nums2[index] += val
```

#### 复杂度  
- **时间复杂度**：`O(len(nums1) * len(nums2))`。  
  - 这里的 `O` 只是一种“数量级”的说法，实际意义是：如果 `nums1` 长 1 000、`nums2` 长 100 000，那么一次 `count` 需要检查 **1 000 × 100 000 = 100 000 000** 次，加起来会非常慢。  
- **空间复杂度**：`O(1)`（不计输入数组本身的空间），因为我们没有使用额外的容器。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，慢的根源在于每次 `count` 都要遍历 **整个** `nums2`。  
- **关键观察**：`nums1` 的长度最多只有 1 000，而 `nums2` 可以长达 100 000。也就是说 `nums1` 相对“很小”。  
- **优化思路**：如果我们能够**快速**知道 `nums2` 中有多少个特定的数值，就可以把遍历 `nums2` 的工作提前做一次，随后每次 `count` 只需要遍历 `nums1`（小数组）即可。  

这正是**哈希表**（在 Python 中用 `dict`）的用武之地。我们把 `nums2` 中每个数值出现的次数记录下来，形成「数值 → 出现次数」的映射。可以把它想象成一本**查字典**：词是「数值」，页码是「出现次数」。

- **`add` 操作**：只会改变 `nums2` 中一个位置的数值。我们把旧值的计数减 1，新增值的计数加 1，哈希表随时保持最新。这样 `add` 的时间是 `O(1)`。  
- **`count` 操作**：遍历 `nums1`（最多 1 000 次），对每个 `x`，我们需要的配对数是 `tot - x` 在 `nums2` 中出现了多少次，只要在哈希表里查一次即可，时间是 `O(1)`。于是 `count` 的总体复杂度是 `O(len(nums1))`。  

**完整流程**  
1. 初始化时，遍历一次 `nums2`，把每个元素的出现次数放进哈希表 `cnt2`。  
2. `add(index, val)`  
   - 记下旧值 `old = nums2[index]`。  
   - 在 `cnt2` 中把 `old` 的计数减 1（若计数降到 0 可以删掉键，保持表小）。  
   - 更新数组 `nums2[index] += val` 得到新值 `new = nums2[index]`。  
   - 在 `cnt2` 中把 `new` 的计数加 1。  
3. `count(tot)`  
   - 初始化答案 `ans = 0`。  
   - 对每个 `x` 在 `nums1` 中：  
     - 目标配对值 `need = tot - x`。  
     - 从 `cnt2` 里取出 `need` 的出现次数（若不存在则为 0），累加到 `ans`。  
   - 返回 `ans`。  

#### 代码（Python）  
```python
class FindSumPairs:
    def __init__(self, nums1, nums2):
        """
        初始化时记录 nums2 中每个数值的出现次数。
        - self.nums1 : 直接保存，不会被修改
        - self.nums2 : 需要在 add 时修改
        - self.cnt2  : 哈希表，key = 数值，value = 出现次数
        """
        self.nums1 = nums1
        self.nums2 = nums2
        self.cnt2 = {}
        for v in nums2:                     # 一次遍历，把出现次数统计到哈希表
            self.cnt2[v] = self.cnt2.get(v, 0) + 1

    def add(self, index: int, val: int) -> None:
        """
        把 nums2[index] 加上 val，并同步更新哈希表 cnt2。
        """
        old = self.nums2[index]              # 旧值
        # 1) 把旧值的计数减 1
        self.cnt2[old] -= 1
        if self.cnt2[old] == 0:              # 计数为 0 时可以删掉，保持表更小
            del self.cnt2[old]

        # 2) 更新数组中的实际值
        self.nums2[index] += val
        new = self.nums2[index]              # 新值

        # 3) 把新值的计数加 1
        self.cnt2[new] = self.cnt2.get(new, 0) + 1

    def count(self, tot: int) -> int:
        """
        统计满足 nums1[i] + nums2[j] == tot 的配对数。
        只遍历 nums1（长度 ≤ 1000），每个元素在哈希表中 O(1) 查找。
        """
        ans = 0
        for x in self.nums1:                 # 对每个 nums1 中的数
            need = tot - x                   # 需要的配对数值
            ans += self.cnt2.get(need, 0)    # 哈希表里出现多少次，就加多少
        return ans
```

#### 复杂度  
- **时间复杂度**  
  - `add`：`O(1)` —— 只做常数次哈希表的增删查。  
  - `count`：`O(len(nums1))`，最多 `O(1000)`，即每次查询只需要遍历小数组一次。  
  与暴力解相比，查询速度提升了 **近 100 000 倍**（因为不再遍历长数组）。  

- **空间复杂度**：`O(distinct(nums2))`，即哈希表中保存的不同数值的个数。最坏情况下每个元素都不相同，需要 `O(len(nums2))` 的额外空间（约 100 000），但这仍然是线性可接受的。  

---

## 心得  

- **核心技巧**：利用**哈希表记录频次**，把“在大数组里找某个数出现多少次”这个操作提前做一次，随后每次查询只需要遍历小数组。  
- **适用的题型**  
  1. “两数组求和计数”类（如 LeetCode 1672. **最接近的两数之和** 的变体）。  
  2. “动态更新后再查询”类（如 LeetCode 1791. **找出数组的中位数**，需要维护频次结构）。  
  3. “多次查询、单次预处理”类（如 频率统计、子数组求和计数等）。  
- **一句话总结解题钥匙**：**把大数组压缩成「数值 → 出现次数」的哈希表，查询时只遍历小数组并在哈希表里 O(1) 取值**。

---

## 反思  

- **第一反应**：直接想遍历两遍数组（暴力），因为最直观的思路是“把所有可能都枚举”。  
- **最容易踩的坑**  
  - **忘记在 `add` 时同步哈希表**，导致查询得到的计数不正确。  
  - **计数为 0 时不删键**，虽然不影响正确性，但会让哈希表变大，影响空间和潜在的查找效率。  
  - **整数范围大**（`tot` 可达 1e9），不能使用数组下标直接存频次，必须使用哈希表。  
- **下次遇到同类题**：第一步就要问自己  
  1. 哪个数组更小？  
  2. 是否可以把大数组“压缩”为频次表？  
  3. 更新操作会不会破坏频次表？如果会，需要在更新时同步维护。  

这样一步步思考，就能快速从暴力到最优的转变。