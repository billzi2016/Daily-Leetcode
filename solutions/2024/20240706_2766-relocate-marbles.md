# #2766. 移动弹珠 / Relocate Marbles

> 难度：中等 · 标签：Array、Hash Table、Sorting、Simulation · [LeetCode 链接](https://leetcode.com/problems/relocate-marbles/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums representing the initial positions of some marbles. You are also given two 0-indexed integer arrays moveFrom and moveTo of equal length.
Throughout moveFrom.length steps, you will change the positions of the marbles. On the ith step, you will move all marbles at position moveFrom[i] to position moveTo[i].
After completing all the steps, return the sorted list of occupied positions.
Notes:

**Examples**

**Example 1:**

```
Input: nums = [1,6,7,8], moveFrom = [1,7,2], moveTo = [2,9,5]
Output: [5,6,8,9]
Explanation: Initially, the marbles are at positions 1,6,7,8.
At the i = 0th step, we move the marbles at position 1 to position 2. Then, positions 2,6,7,8 are occupied.
At the i = 1st step, we move the marbles at position 7 to position 9. Then, positions 2,6,8,9 are occupied.
At the i = 2nd step, we move the marbles at position 2 to position 5. Then, positions 5,6,8,9 are occupied.
At the end, the final positions containing at least one marbles are [5,6,8,9].
```

**Example 2:**

```
Input: nums = [1,1,3,3], moveFrom = [1,3], moveTo = [2,2]
Output: [2]
Explanation: Initially, the marbles are at positions [1,1,3,3].
At the i = 0th step, we move all the marbles at position 1 to position 2. Then, the marbles are at positions [2,2,3,3].
At the i = 1st step, we move all the marbles at position 3 to position 2. Then, the marbles are at positions [2,2,2,2].
Since 2 is the only occupied position, we return [2].
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= moveFrom.length <= 105
- moveFrom.length == moveTo.length
- 1 <= nums[i], moveFrom[i], moveTo[i] <= 109
- The test cases are generated such that there is at least a marble in moveFrom[i] at the moment we want to apply the ith move.

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`，表示若干弹珠的初始位置。另给定两个等长的下标从 **0** 开始的整数数组 `moveFrom` 和 `moveTo`。  
在 `moveFrom.length` 步操作中，你需要依次改变弹珠的位置。第 `i` 步时，将所有位于位置 `moveFrom[i]` 的弹珠移动到位置 `moveTo[i]`。  
完成所有步骤后，返回所有被占据位置的升序排列列表。

**示例 1**  
```text
Input: nums = [1,6,7,8], moveFrom = [1,7,2], moveTo = [2,9,5]
Output: [5,6,8,9]
Explanation: 初始时，弹珠位于位置 1、6、7、8。  
第 0 步，将位置 1 的弹珠全部移动到位置 2，得到占据位置 2、6、7、8。  
第 1 步，将位置 7 的弹珠全部移动到位置 9，得到占据位置 2、6、8、9。  
第 2 步，将位置 2 的弹珠全部移动到位置 5，最终占据位置 5、6、8、9。  
返回升序排列的结果 `[5,6,8,9]`。  
```

**示例 2**  
```text
Input: nums = [1,1,3,3], moveFrom = [1,3], moveTo = [2,2]
Output: [2]
Explanation: 初始时，弹珠位于位置 [1,1,3,3]。  
第 0 步，将所有位于位置 1 的弹珠移动到位置 2，得到位置 [2,2,3,3]。  
第 1 步，将所有位于位置 3 的弹珠移动到位置 2，得到位置 [2,2,2,2]。  
此时只有位置 2 被占据，返回 `[2]`。  
```

**约束条件**
- `1 <= nums.length <= 10^5`
- `1 <= moveFrom.length <= 10^5`
- `moveFrom.length == moveTo.length`
- `1 <= nums[i], moveFrom[i], moveTo[i] <= 10^9`
- 测试数据保证在执行第 `i` 步移动时，至少有一个弹珠位于 `moveFrom[i]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**模拟每一步的移动**，把所有弹珠的位置存到一个普通的 Python `list`（或 `array`）里。  
- 每次要把 `moveFrom[i]` 上的所有弹珠搬到 `moveTo[i]`，我们就在列表中遍历所有元素，把等于 `moveFrom[i]` 的下标改成 `moveTo[i]`。  
- 这类似于把弹珠摆成一排，老师喊“把所有在 5 号位置的弹珠搬到 9 号位置”，我们只能一个一个检查，看到 5 就换成 9。

> **为什么这样是对的？**  
> 只要按照题目顺序逐步执行，每一步都把对应位置的弹珠全部搬走，最终得到的列表自然就是题目要求的“所有占据的坐标”。  

> **时间/空间复杂度**  
> - 假设弹珠数 `n = len(nums)`，移动指令数 `m = len(moveFrom)`。  
> - 对每一条指令我们都要遍历整个列表（最坏情况要检查 `n` 个位置），所以总共要做 `m × n` 次比较/赋值。  
> - 用大白话说，`O(n²)` 就像“如果你有 1000 颗弹珠，还要跑 1000 次检查，那就相当于要做 100 万 次操作”。  

#### 代码（Python）

```python
def relocateMarbles_bruteforce(nums, moveFrom, moveTo):
    # 把弹珠位置复制到一个列表，后面会直接改动它
    positions = list(nums)                     # O(n) 的空间

    for f, t in zip(moveFrom, moveTo):         # 逐条指令处理
        # 暴力遍历所有弹珠，找到要搬走的弹珠并改成新位置
        for i in range(len(positions)):
            if positions[i] == f:              # 发现一颗在 f 位置的弹珠
                positions[i] = t               # 把它搬到 t

    # 题目要求返回 **已排序** 的占位坐标（去重后）
    return sorted(set(positions))              # set 去重，sorted 排序
```

#### 复杂度

- **时间复杂度**：`O(n * m)`  
  解释：每条指令都要遍历 `n` 颗弹珠，最坏情况下 `n`≈`m`，所以大约是 `n²` 级别的操作。  
- **空间复杂度**：`O(n)`  
  解释：只用了一个和原始弹珠数等大的列表以及最后去重的 `set`，额外空间与输入规模线性相关。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都要遍历全部弹珠**。其实我们只关心**每个坐标是否被占据**，而不在乎同一坐标上有多少颗弹珠。  
- 当我们把所有在 `moveFrom[i]` 的弹珠搬走时，这个坐标 **一定会变空**（因为题目保证此时一定有弹珠），于是可以直接把它从“占据集合”里删掉。  
- 同时，无论原来有没有弹珠，`moveTo[i]` 位置在搬完后必然被占据，只需要把它加入集合即可。

这正好可以用 **哈希集合（`set`）** 来实现：  
- `set` 在 Python 中底层是哈希表，查找、插入、删除的平均时间都是 **O(1)**，就像在一本大字典里找词条——找得快、直接改。  
- 过程如下：  
  1. 把所有初始弹珠位置放进 `occupied` 集合（自动去重）。  
  2. 按顺序遍历 `moveFrom / moveTo`：  
     - `occupied.discard(f)` → 把出发坐标删掉（如果已经不在集合里，`discard` 也不会报错）。  
     - `occupied.add(t)` → 把目标坐标加入。  
  3. 最后把集合转成列表并排序返回。

> **为什么只用集合就够了？**  
> 因为题目保证在每一步执行前，`moveFrom[i]` 必定有弹珠在该位置；搬走所有弹珠后，这个位置一定空；而我们只记录“是否有人在”，不需要记录具体数量。

> **核心数据结构**：**哈希集合（set）**  
> - 类比：就像一本词典，词是坐标，词条在不在字典里代表该坐标是否被占。查找、增加、删除都非常快。

#### 代码（Python）

```python
def relocateMarbles(nums, moveFrom, moveTo):
    """
    最优实现：使用集合（哈希表）模拟占位情况
    """
    # 1️⃣ 把初始弹珠位置放进集合，自动去重
    occupied = set(nums)               # O(n) 空间

    # 2️⃣ 按顺序处理每一次搬运
    for f, t in zip(moveFrom, moveTo):
        # 把出发位置的占位删除（题目保证一定存在）
        occupied.discard(f)            # discard 不会因为不存在而报错
        # 把目标位置加入占位集合
        occupied.add(t)

    # 3️⃣ 返回排序后的列表
    return sorted(occupied)            # O(k log k)，k 为最终不同坐标数
```

#### 复杂度

- **时间复杂度**：`O(n + m + k log k)`  
  - `O(n)` 用于把初始弹珠放进集合。  
  - `O(m)` 逐条指令进行 `discard`/`add`，每次都是常数时间。  
  - `k` 是最终不同坐标的数量（`k ≤ n + m`），排序需要 `O(k log k)`。  
  与暴力解相比，**不再有 `n × m` 的乘法级别**，在数据规模最大（10⁵）时能轻松通过。

- **空间复杂度**：`O(n + m)`（实际上只需要 `O(k)`）  
  - 集合中最多存放所有出现过的坐标，最多不超过 `n + m` 个。  
  - 与输入规模线性相关，远小于暴力解的 `O(n)` 列表（但同样是线性的，只是常数更小）。

---

## 心得

- **核心技巧**：**使用哈希集合维护“是否被占据”**，而不是维护每颗弹珠的具体位置。  
- **适用的题型**  
  1. 需要在大量“加入/删除/查询”操作后输出 **唯一元素集合**（如 “First Unique Number”）。  
  2. “移动”或“合并”操作只关心 **状态是否存在**，不关心计数（如 “Merge Similar Items”）。  
- **解题钥匙**：**把“数量”降维成“是否”，用 `set` 实现 O(1) 的增删查**。

---

## 反思

- **第一反应**：看到“把所有在某位置的弹珠搬走”，立刻想到遍历整个数组去改值——这就是暴力思路。  
- **最容易踩的坑**  
  - **重复坐标**：初始 `nums` 可能有相同位置的多颗弹珠，直接用 `list` 会导致后面重复删除/添加，需要去重。  
  - **移动顺序**：一定要按给定的顺序逐条执行，不能一次性把所有 `moveFrom` → `moveTo` 直接映射。  
  - **集合操作**：使用 `remove` 而不是 `discard` 可能在某些指令已经把位置清空后抛异常。  
- **下次思考类似题**：先问自己“我到底需要**计数**还是**是否存在**”。如果只要存在，立刻考虑用 `set`（哈希表）来压缩状态，避免遍历全部元素。