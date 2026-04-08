# #3587. 最小相邻交换次数使奇偶交替 / Minimum Adjacent Swaps to Alternate Parity

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-adjacent-swaps-to-alternate-parity/)

---

## 题目（英文原版）

**Description**

You are given an array nums of distinct integers.
In one operation, you can swap any two adjacent elements in the array.
An arrangement of the array is considered valid if the parity of adjacent elements alternates, meaning every pair of neighboring elements consists of one even and one odd number.
Return the minimum number of adjacent swaps required to transform nums into any valid arrangement.
If it is impossible to rearrange nums such that no two adjacent elements have the same parity, return -1.

**Examples**

**Example 1:**

```
Input: nums = [2,4,6,5,7]
Output: 3
Explanation:
Swapping 5 and 6, the array becomes [2,4,5,6,7]
Swapping 5 and 4, the array becomes [2,5,4,6,7]
Swapping 6 and 7, the array becomes [2,5,4,7,6] . The array is now a valid arrangement. Thus, the answer is 3.
```

**Example 2:**

```
Input: nums = [2,4,5,7]
Output: 1
Explanation:
By swapping 4 and 5, the array becomes [2,5,4,7] , which is a valid arrangement. Thus, the answer is 1.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 0
Explanation:
The array is already a valid arrangement. Thus, no operations are needed.
```

**Example 4:**

```
Input: nums = [4,5,6,8]
Output: -1
Explanation:
No valid arrangement is possible. Thus, the answer is -1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- All elements in nums are distinct.

---

## 题目（中文翻译）

给定一个由不同整数构成的数组 `nums`。  
一次操作可以交换数组中任意两个相邻元素（adjacent swaps）。  
如果相邻元素的奇偶性（parity）交替，即每一对相邻元素恰好由一个偶数和一个奇数组成，则该数组的排列被认为是有效的（valid arrangement）。  

请返回将 `nums` 通过相邻交换转变为任意有效排列所需的最小交换次数。  
如果无法重新排列使得任意相邻元素的奇偶性不同，返回 `-1`。

**示例 1**  
输入: `nums = [2,4,6,5,7]`  
输出: `3`  
解释:  
- 交换 `5` 与 `6`，数组变为 `[2,4,5,6,7]`  
- 交换 `5` 与 `4`，数组变为 `[2,5,4,6,7]`  
- 交换 `6` 与 `7`，数组变为 `[2,5,4,7,6]`，此时数组已是有效排列。因此答案为 `3`。

**示例 2**  
输入: `nums = [2,4,5,7]`  
输出: `1`  
解释: 交换 `4` 与 `5`，数组变为 `[2,5,4,7]`，已满足奇偶交替，是有效排列，故答案为 `1`。

**示例 3**  
输入: `nums = [1,2,3]`  
输出: `0`  
解释: 数组本身已经满足奇偶交替，无需操作。

**示例 4**  
输入: `nums = [4,5,6,8]`  
输出: `-1`  
解释: 无法得到任意有效排列，返回 `-1`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `nums` 中所有元素互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**先枚举所有合法的奇偶交替排列**，然后把原数组一步一步地“冒泡”成这个目标排列，记录需要的相邻交换次数，取最小值。  

- **合法排列**：数组的奇数、偶数交替出现。我们可以先把数组中的奇数取出来，偶数取出来，然后交替拼接。  
- **相邻交换**：把数组变成目标排列的过程就像冒泡排序一样：把一个元素往左或往右移动，只能一步一步和相邻的元素交换。把元素从位置 `i` 移到位置 `j`（`i>j`）至少要交换 `i‑j` 次，**因为每次只能和左边的一个元素换位**。  

把所有元素都对齐到目标位置后，累计的交换次数就是把原数组变成该目标排列的代价。遍历所有可能的目标排列，取最小的代价即为答案。  

> **类比**：把数组想象成一排学生，想让每个奇数学生站在偶数学生之间，只能让相邻的两个人互相让路，想把一个学生从第 5 位搬到第 2 位，必须让他先和第 4 位、再和第 3 位、最后和第 2 位的人分别让路一次，合计 3 次。  

如果奇数和偶数的数量相差大于 1，根本不可能交替排列，直接返回 `-1`。

#### 代码（Python）

```python
from itertools import permutations

def min_swaps_bruteforce(nums):
    n = len(nums)
    # 统计奇偶个数
    odd = [x for x in nums if x % 2]
    even = [x for x in nums if x % 2 == 0]

    # 若数量差距大于1，直接不可能
    if abs(len(odd) - len(even)) > 1:
        return -1

    # 生成所有合法的目标序列（最多两种）
    targets = []
    if len(even) >= len(odd):          # 偶数可以放在下标0
        pattern = []
        for i in range(n):
            pattern.append(even[i // 2] if i % 2 == 0 else odd[i // 2])
        targets.append(pattern)
    if len(odd) >= len(even):          # 奇数可以放在下标0
        pattern = []
        for i in range(n):
            pattern.append(odd[i // 2] if i % 2 == 0 else even[i // 2])
        targets.append(pattern)

    # 暴力计算把 nums 变成 target 需要的相邻交换次数
    def swaps_to_target(arr, target):
        arr = list(arr)           # 复制一份，防止修改原数组
        swaps = 0
        # 用最朴素的“冒泡”思想把每个位置上的元素搬到正确位置
        for i in range(n):
            if arr[i] == target[i]:
                continue
            # 在后面的数组里找到目标元素的位置 j
            j = i + 1
            while arr[j] != target[i]:
                j += 1
            # 将位置 j 的元素左移到 i，期间每次与左侧相邻元素交换
            while j > i:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]   # 相邻交换
                swaps += 1
                j -= 1
        return swaps

    ans = float('inf')
    for t in targets:
        ans = min(ans, swaps_to_target(nums, t))
    return ans
```

> **关键行解释**  
> - 第 7‑11 行：把奇数、偶数分别收集到两个列表，类似把字典里 “奇数” 这本书和 “偶数” 那本书分开放。  
> - 第 19‑28 行：根据奇偶数量，构造最多两种交替模式（先偶后奇，或先奇后偶）。  
> - 第 33‑49 行：**暴力搬运**——从左到右依次把当前元素换成目标元素，用最直接的相邻交换方式实现。每找到一次目标位置就把它“一步步左移”，计数即为交换次数。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 最坏情况下，每个位置都要在后面遍历一次找到目标元素（`O(n)`），随后再把它左移 `O(n)` 步，总共 `O(n²)`。  
  - 对于 `n = 10⁵` 这种大规模数据，这个方法会超时。  
- **空间复杂度**：`O(n)`  
  - 需要额外的列表保存奇数、偶数以及复制的数组，和原数组等长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于每次都要在数组里找目标元素并逐个交换**，这导致 `O(n²)` 的时间。  
实际上，我们并不需要真的去“搬动”元素，只要知道每个奇数（或偶数）最终应该站在哪个位置，就能直接算出需要多少次相邻交换。  

**关键观察**  

1. **相邻交换的代价**：把一个元素从下标 `i` 移到下标 `j`（`i>j`），最少需要 `i‑j` 次相邻交换。因为每次只能和左边的一个元素换位，最短路径就是一步一步往左走。  
2. **奇偶元素之间互不影响**：我们只关心奇数放在哪、偶数放在哪。奇数之间的相对顺序在最终排列里保持不变（因为所有奇数都是不同的），同理偶数也是。于是只要把**奇数的当前位置列表**和**目标奇数位置列表**对应配对，累加每对的距离之和，就是把所有奇数搬到正确位置所需的最少交换次数。偶数同理。  
3. **只需要两种目标模式**：  
   - 若数组长度 `n` 为偶数，奇数和偶数数量相等，两种交替模式（`even, odd, even, …` 或 `odd, even, odd, …`）都可能。我们分别计算代价，取最小。  
   - 若 `n` 为奇数，数量较多的那一类（奇数或偶数）必须出现在下标 `0` 位置，其余位置交替。只有一种可行模式。  

**实现步骤**  

1. 统计奇数、偶数个数 `oddCnt`、`evenCnt`。若 `abs(oddCnt - evenCnt) > 1`，直接返回 `-1`。  
2. 收集**奇数元素的下标** `oddPos`，以及**偶数元素的下标** `evenPos`（下标从 `0` 开始）。这相当于把奇数和偶数分别装进两个“小抽屉”。  
3. 编写一个函数 `cost(target_start_parity)`：  
   - 根据 `target_start_parity`（0 表示下标 0 放偶数，1 表示放奇数）生成**目标奇数下标列表** `targetOddPos`（即在交替序列中奇数应该出现的位置）和**目标偶数下标列表** `targetEvenPos`。  
   - 计算奇数搬运代价：`sum(|oddPos[i] - targetOddPos[i]|)`。同理偶数搬运代价。  
   - 两者相加即为该模式的总交换次数。  
4. 对所有可行的起始奇偶组合求最小代价，返回结果。  

> **类比**：把奇数学生的座位号记在一张纸上，把他们“应该坐”的座位号记在另一张纸上，只要把两张纸对应的数字配对，算出每对之间相差多少步，所有差值相加就是搬动所有学生的最少让路次数。  

#### 代码（Python）

```python
def minAdjSwaps(nums):
    n = len(nums)

    # 1️⃣ 统计奇偶个数
    odd_pos = []   # 奇数元素所在的下标
    even_pos = []  # 偶数元素所在的下标
    for i, v in enumerate(nums):
        if v % 2:          # v 是奇数
            odd_pos.append(i)
        else:              # v 是偶数
            even_pos.append(i)

    odd_cnt, even_cnt = len(odd_pos), len(even_pos)

    # 2️⃣ 不可能的情况
    if abs(odd_cnt - even_cnt) > 1:
        return -1

    # 3️⃣ 计算一种起始奇偶模式的代价
    def calc_cost(start_with_even: bool) -> int:
        """
        start_with_even == True  -> index 0 需要放偶数
        start_with_even == False -> index 0 需要放奇数
        """
        # 目标奇数/偶数下标（交替排列）
        target_odd = []
        target_even = []
        for idx in range(n):
            # idx%2==0 表示当前位置是“起始位置”，
            # 根据 start_with_even 决定它应该是奇数还是偶数
            if (idx % 2 == 0) == (not start_with_even):
                # 这里是奇数应该出现的位置
                target_odd.append(idx)
            else:
                target_even.append(idx)

        # 4️⃣ 计算搬运代价：对应下标的绝对差值之和
        #   由于奇数、偶数在原数组中相对顺序不变，直接一一配对即可
        cost = 0
        for cur, tgt in zip(odd_pos, target_odd):
            cost += abs(cur - tgt)
        for cur, tgt in zip(even_pos, target_even):
            cost += abs(cur - tgt)
        return cost

    # 5️⃣ 根据数组长度决定检查哪些模式
    if n % 2 == 0:          # 长度为偶数，两种模式都可能
        ans = min(
            calc_cost(start_with_even=True),   # 偶数在下标0
            calc_cost(start_with_even=False)   # 奇数在下标0
        )
    else:                   # 长度为奇数，数量多的那类必须在下标0
        if odd_cnt > even_cnt:
            ans = calc_cost(start_with_even=False)  # 奇数先
        else:
            ans = calc_cost(start_with_even=True)   # 偶数先
    return ans
```

> **关键行解释**  
> - 第 4‑9 行：遍历数组，把奇数、偶数的下标分别存进 `odd_pos`、`even_pos`，相当于给奇数和偶数各贴了“位置标签”。  
> - 第 15‑18 行：如果奇偶数量差距大于 1，根本无法交替，直接返回 `-1`。  
> - 第 22‑33 行：根据起始位置（偶数在第 0 位还是奇数在第 0 位）生成目标奇数、偶数下标列表。`target_odd`/`target_even` 就是“理想座位”。  
> - 第 38‑44 行：把原来的奇数下标 `odd_pos[i]` 与目标奇数下标 `target_odd[i]` 配对，累加它们的距离；偶数同理。因为相邻交换的最短路径就是距离本身，这一步已经得到了最少交换次数。  
> - 第 48‑55 行：根据数组长度是奇数还是偶数，挑选合法的起始模式并取最小代价。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组收集奇偶下标 `O(n)`，随后对每种模式再次线性遍历计算代价，常数倍的 `n`。相比暴力的 `O(n²)`，大幅提升。  
- **空间复杂度**：`O(n)`（最坏情况）  
  - 需要保存奇数下标列表和偶数下标列表，合计不超过 `n` 个整数。  

---

## 心得  

- **核心技巧**：把“相邻交换的最少次数”转化为“元素当前位置与目标位置的距离之和”。这是一种**贪心 + 计数**的思路。  
- **适用的题型**：  
  1. **最少相邻交换使数组有序**（如把所有 0 移到左侧）  
  2. **最少相邻交换实现特定排列**（如把所有负数放左边，正数放右边）  
  3. **交替字符/数字序列**（如字符串中 `a` 与 `b` 交替）  
- **一句话总结解题钥匙**：**只要知道每个元素该站在哪儿，答案就是它们“走路距离”的总和**。  

---

## 反思  

- **第一反应**：先想到枚举所有合法排列，然后用冒泡式的相邻交换模拟，直接写出可运行的代码。  
- **最容易踩的坑**：  
  - **数量不匹配**：奇数和偶数相差超过 1 时必须提前返回 `-1`，否则后面的计算会出现索引越界。  
  - **目标下标的生成**：起始位置决定奇数/偶数的目标下标，需要仔细判断 `idx % 2` 与 `start_with_even` 的对应关系，容易写反。  
  - **大数溢出**：在 Python 中不必担心，但在其他语言要注意使用 64 位整数保存累计的交换次数。  
- **下次遇到同类题的第一步**：先**统计类别数量**（奇/偶、0/1、负/正），判断是否可能实现交替或分块；随后**收集原位置列表**，直接用“距离之和”求最少相邻交换次数。