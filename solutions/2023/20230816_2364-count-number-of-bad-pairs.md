# #2364. 统计坏对的数量 / Count Number of Bad Pairs

> 难度：中等 · 标签：Array、Hash Table、Math、Counting · [LeetCode 链接](https://leetcode.com/problems/count-number-of-bad-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. A pair of indices (i, j) is a bad pair if i < j and j - i != nums[j] - nums[i].
Return the total number of bad pairs in nums.

**Examples**

**Example 1:**

```
Input: nums = [4,1,3,3]
Output: 5
Explanation: The pair (0, 1) is a bad pair since 1 - 0 != 1 - 4.
The pair (0, 2) is a bad pair since 2 - 0 != 3 - 4, 2 != -1.
The pair (0, 3) is a bad pair since 3 - 0 != 3 - 4, 3 != -1.
The pair (1, 2) is a bad pair since 2 - 1 != 3 - 1, 1 != 2.
The pair (2, 3) is a bad pair since 3 - 2 != 3 - 3, 1 != 0.
There are a total of 5 bad pairs, so we return 5.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: 0
Explanation: There are no bad pairs.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个 **0 索引**（0-indexed）的整数数组 `nums`。如果一对索引 `(i, j)` 满足 `i < j` 且 `j - i != nums[j] - nums[i]`，则称其为 **坏对**（bad pair）。返回数组 `nums` 中坏对的总数。

**示例 1**  
**输入**: `nums = [4,1,3,3]`  
**输出**: `5`  
**解释**:  
- 对 `(0, 1)` 是坏对，因为 `1 - 0 != 1 - 4`。  
- 对 `(0, 2)` 是坏对，因为 `2 - 0 != 3 - 4`，即 `2 != -1`。  
- 对 `(0, 3)` 是坏对，因为 `3 - 0 != 3 - 4`，即 `3 != -1`。  
- 对 `(1, 2)` 是坏对，因为 `2 - 1 != 3 - 1`，即 `1 != 2`。  
- 对 `(2, 3)` 是坏对，因为 `3 - 2 != 3 - 3`，即 `1 != 0`。  
共有 5 个坏对，返回 `5`。

**示例 2**  
**输入**: `nums = [1,2,3,4,5]`  
**输出**: `0`  
**解释**: 没有坏对。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把所有满足 `i < j` 的下标对枚举一遍，逐个判断它们是否满足  
```
j - i != nums[j] - nums[i]
```  
如果不相等，就把这对记为 **坏对**，最后把计数器加起来返回。  

- **使用的数据结构**：只需要一个普通的 Python 列表 `nums`，以及两个整型变量 `cnt`（记录坏对数量）和 `n`（数组长度）。  
- **生活化类比**：把数组想成排好队的同学，每个人都有一个编号（下标 `i`）和一个身高（`nums[i]`）。我们要检查每一对前后同学，看看“站位距离”和“身高差”是否相等，不相等就算“坏配”。这就像老师让你两两比较，最笨的办法就是每个人都去和后面所有人聊一次。  

**为什么正确**：因为我们把 **所有** 可能的 `(i, j)`（满足 `i<j`）都检查了一遍，漏掉的情况不存在，所以计数必然是准确的。  

#### 代码（Python）  
```python
def countBadPairs(nums):
    n = len(nums)          # 数组长度
    cnt = 0                # 坏对计数器
    # 两层循环遍历所有 i < j 的组合
    for i in range(n):
        for j in range(i + 1, n):
            # 判断条件：距离 != 值的差
            if (j - i) != (nums[j] - nums[i]):
                cnt += 1    # 发现坏对，计数加一
    return cnt
```

#### 复杂度  
- **时间复杂度**：`O(n²)`。  
  - 解释：外层循环跑 `n` 次，内层平均跑 `n/2` 次，整体约等于 `n * n/2`，所以是二次方级别。对 10⁵ 长度的数组来说，`n²` 已经是 **10¹⁰** 级别，根本跑不完。  
- **空间复杂度**：`O(1)`。  
  - 解释：只用了常数个额外变量（`cnt、n、i、j`），和输入规模无关。

---  

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现最慢的地方在于 **两层循环**——每次都要比较 `j - i` 与 `nums[j] - nums[i]`。  
我们可以把判断式子变形，看看能否把比较的成本降到 **O(1)**，然后再用哈希表把所有配对的计数一次性完成。

1. **变形等价**  
   ```
   j - i != nums[j] - nums[i]
   ⇔  (j - i) - (nums[j] - nums[i]) != 0
   ⇔  (j - nums[j]) - (i - nums[i]) != 0
   ⇔  nums[i] - i != nums[j] - j
   ```
   最后一行说明：**只要两个位置的 “值减下标” 不相等，就一定是坏对**。  
   换句话说，**好对**（不是坏对）的条件是 `nums[i] - i == nums[j] - j`。

2. **把问题反过来**：先算出 **好对的数量**，再用总对数减去好对数得到坏对数。  
   - 总对数（所有 `i<j`） = `n * (n-1) / 2`（等差数列求和，组合数 C(n,2)）。
   - 好对数 = 同一个 `nums[k] - k` 值出现的次数两两组合的数量。

3. **如何快速统计相同的 `nums[i] - i`**  
   - 把每个下标 `i` 对应的 `key = nums[i] - i` 放进 **哈希表**（Python 中的 `dict`）。  
   - 哈希表的 **key** 就是 “值减下标”，**value** 记录这个 key 出现了多少次。  
   - 当遍历到第 `i` 个元素时，如果该 key 已经出现了 `c` 次，那么它可以和之前的 `c` 个位置组成 **好对**，计数器 `good` 加 `c`，随后把该 key 的计数加一。

4. **一步到位的遍历**  
   ```text
   good = 0
   for each i:
       key = nums[i] - i
       good += count[key]   # 之前出现的相同 key 能组成多少好对
       count[key] += 1
   ```
   这样只用了 **一次遍历**，时间是线性的。

5. **最终答案**  
   ```
   total = n * (n-1) // 2
   bad   = total - good
   ```

**核心概念解释**  

- **哈希表（HashMap）**：可以把它想象成一本“查字典”。字典里每个单词（key）对应一个页码（value），我们只需要 O(1) 时间就能快速找到对应的页码。这里的 key 是 `nums[i] - i`，value 是出现次数。  
- **组合数 C(k,2) = k*(k-1)/2**：如果同一个 key 出现了 `k` 次，那么这 `k` 个位置两两配对，一共有 `k` 选 `2` 种配法，等价于 `k*(k-1)/2`。我们在遍历时用累计方式（`good += count[key]`）实现的其实就是在实时累加这些组合数。

#### 代码（Python）  
```python
def countBadPairs(nums):
    """
    统计数组中「坏对」的数量。
    思路：先统计「好对」(nums[i] - i 相等) 的数量，再用总对数减去好对数。
    """
    n = len(nums)
    total_pairs = n * (n - 1) // 2   # 所有 i<j 的组合数

    cnt = {}        # 哈希表：key = nums[i] - i, value = 出现次数
    good = 0        # 好对（满足 nums[i]-i == nums[j]-j）的计数

    for i, v in enumerate(nums):
        key = v - i               # 计算 nums[i] - i
        # 之前出现过相同 key 的位置可以和当前 i 组成好对
        good += cnt.get(key, 0)   # cnt.get(key,0) 等价于 dict.get(key, default)
        # 更新哈希表中该 key 的出现次数
        cnt[key] = cnt.get(key, 0) + 1

    bad = total_pairs - good       # 坏对 = 总对 - 好对
    return bad
```

#### 复杂度  
- **时间复杂度**：`O(n)`。  
  - 解释：只遍历一次数组，哈希表的插入和查询都是常数时间（平均 O(1)），所以整体是线性级别。相比暴力的 `O(n²)`，速度提升了 **指数级**。  
- **空间复杂度**：`O(n)`（最坏情况）。  
  - 解释：如果每个 `nums[i] - i` 都不相同，哈希表需要存 `n` 条记录；如果很多相同，则会更少。总的额外空间随输入规模线性增长。

---  

## 心得  

- **核心技巧**：把 “不等式” 通过代数变形转成 “相等” 的判定，然后利用 **哈希表** 统计相同值的出现次数，再用 **组合计数** 求解。  
- **适用的题型**  
  1. “统计满足某种相等关系的下标对”——如 LeetCode 2420 *Count Subarrays With Fixed Ratio*（利用哈希表统计前缀和/前缀乘积）。  
  2. “先求好对/满足条件的对数，再用总数减去”——如 1512 *Number of Good Pairs*。  
  3. “把数组下标和数值组合成新的表达式，再统计相同值”——如 1665 *Minimum Initial Energy to Finish Tasks*（把 `deadline - duration` 之类的转化）。  

- **一句话总结**：  
  **把“坏对”反向计数为“好对”，用 `nums[i]-i` 的哈希计数一次遍历搞定。**  

---  

## 反思  

- **第一反应**：看到两个下标差与数值差不相等，立刻想到双层循环枚举。  
- **最容易踩的坑**  
  1. **整数溢出**：在某些语言里 `n*(n-1)` 可能超过 32 位整数范围，需要使用 64 位或 Python 的大整数。  
  2. **负数 key**：`nums[i] - i` 可能为负数，哈希表要能接受负数键（Python 没问题）。  
  3. **边界条件**：数组长度为 1 时，总对数为 0，直接返回 0；实现时要防止除以 2 时出现浮点数，使用整数除 `//`。  

- **下次类似题的第一步**：  
  **把“i 与 j 的关系”用代数式子化简，看能否转化为“相等”判定，然后考虑哈希表计数**。这样往往能把二次枚举降到线性时间。