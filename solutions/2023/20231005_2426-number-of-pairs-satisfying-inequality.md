# #2426. **满足不等式的数对个数** / Number of Pairs Satisfying Inequality

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer、Binary Indexed Tree、Segment Tree、Merge Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/number-of-pairs-satisfying-inequality/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2, each of size n, and an integer diff. Find the number of pairs (i, j) such that:
Return the number of pairs that satisfy the conditions.

**Examples**

**Example 1:**

```
Input: nums1 = [3,2,5], nums2 = [2,2,1], diff = 1
Output: 3
Explanation:
There are 3 pairs that satisfy the conditions:
1. i = 0, j = 1: 3 - 2 <= 2 - 2 + 1. Since i < j and 1 <= 1, this pair satisfies the conditions.
2. i = 0, j = 2: 3 - 5 <= 2 - 1 + 1. Since i < j and -2 <= 2, this pair satisfies the conditions.
3. i = 1, j = 2: 2 - 5 <= 2 - 1 + 1. Since i < j and -3 <= 2, this pair satisfies the conditions.
Therefore, we return 3.
```

**Example 2:**

```
Input: nums1 = [3,-1], nums2 = [-2,2], diff = -1
Output: 0
Explanation:
Since there does not exist any pair that satisfies the conditions, we return 0.
```

**Constraints**

- n == nums1.length == nums2.length
- 2 <= n <= 105
- -104 <= nums1[i], nums2[i] <= 104
- -104 <= diff <= 104

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组 `nums1` 和 `nums2`（长度均为 `n`），以及一个整数 `diff`。请计算满足以下条件的索引对 `(i, j)` 的数量：

- `i < j`
- `nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff`

返回满足上述条件的数对个数。

---

### 示例

#### 示例 1
**输入**  
``` 
nums1 = [3,2,5], nums2 = [2,2,1], diff = 1
```  
**输出**  
```
3
```  
**解释**  
满足条件的数对共有 3 个：
1. `i = 0, j = 1`：`3 - 2 <= 2 - 2 + 1`，即 `1 <= 1`，满足条件。  
2. `i = 0, j = 2`：`3 - 5 <= 2 - 1 + 1`，即 `-2 <= 2`，满足条件。  
3. `i = 1, j = 2`：`2 - 5 <= 2 - 1 + 1`，即 `-3 <= 2`，满足条件。

#### 示例 2
**输入**  
``` 
nums1 = [3,-1], nums2 = [-2,2], diff = -1
```  
**输出**  
```
0
```  
**解释**  
不存在满足条件的数对，返回 `0`。

---

### 约束条件
- `n == nums1.length == nums2.length`
- `2 <= n <= 10^5`
- `-10^4 <= nums1[i], nums2[i] <= 10^4`
- `-10^4 <= diff <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有满足条件的 `(i, j)` 暴力枚举一遍：

1. 先遍历左指针 `i`（`0 ≤ i < n`）。  
2. 对每个 `i` 再遍历右指针 `j`（`i+1 ≤ j < n`），检查不等式  

   ```
   nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff
   ```

3. 若成立，就把答案加一。

> **类比**：把数组想成排好队的同学，暴力解就是让每个同学依次去和后面所有同学比较一次，看看谁符合条件。  

这个方法显然是 **正确** 的，因为它把所有可能的 `(i, j)` 都检查了一遍，符合条件的自然会被计数。

**时间复杂度**  
- 外层循环 `n` 次，内层循环最多 `n-1` 次，整体是 `O(n²)`。  
- 用大白话说，就是当 `n = 10⁵` 时，需要检查大约 `10¹⁰` 次，根本跑不完。

**空间复杂度**  
- 只用了常数级的额外变量（计数器），所以是 `O(1)`。

#### 代码（Python）

```python
def count_pairs_bruteforce(nums1, nums2, diff):
    n = len(nums1)
    ans = 0
    for i in range(n):                # 左指针 i
        for j in range(i + 1, n):      # 右指针 j，必须 i < j
            # 检查题目给出的不等式
            if nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff:
                ans += 1               # 条件满足，计数加一
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：`O(1)` —— 只用了计数器 `ans`，不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现瓶颈在于**每次都要遍历所有后面的元素**。  
要把时间降到 `O(n log n)`，必须在遍历时**快速统计**满足条件的后缀元素个数。

---

#### 2.1 重新整理不等式  

原始不等式：

```
nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff
```

把左边、右边都移项，得到：

```
(nums1[i] - nums2[i]) <= (nums1[j] - nums2[j]) + diff
```

令  

```
a[k] = nums1[k] - nums2[k]          # 对每个位置 k 计算一次差值
```

则条件可以写成：

```
a[i] <= a[j] + diff      (i < j)
```

进一步变形：

```
a[j] >= a[i] - diff
```

**解释**：当我们已经确定了左指针 `i`，只要在右边的下标 `j` 中找到 **“差值 a[j] 不小于 a[i] - diff”** 的个数，就把它们全部计入答案。

所以问题转化为：

> 对每个位置 `i`（从左到右），统计在 `i` 右侧出现的、**大于等于** `a[i] - diff` 的元素个数。

这正好是**“在一个动态变化的序列中，统计 ≥ 某个阈值的元素数量”**的经典场景——可以用**有序数据结构**（如平衡二叉树、线段树、Fenwick 树）实现。

---

#### 2.2 逆序遍历 + Fenwick 树（Binary Indexed Tree）

**逆序遍历的原因**  
如果我们从右往左遍历数组，当前遍历到的下标 `i` 右侧的所有元素已经被“放进”数据结构中了。这样在处理 `i` 时，只需要在已有的结构里**查询**满足 `a[j] >= a[i] - diff` 的数量即可。

**Fenwick 树的作用**  
Fenwick 树可以在 `O(log n)` 时间内完成两类操作：

1. **单点更新**：把某个数值的出现次数加 1（相当于把 `a[j]` 放进集合）。
2. **前缀和查询**：求 ≤ 某个值的元素个数。  

因为我们需要 **≥** 某个阈值的个数，可以把 “总数 - ≤阈值的个数” 计算出来。

**离散化（坐标压缩）**  
`a[i]` 的取值范围是 `[-2·10⁴, 2·10⁴]`（两数组相减），但 `n` 可达 `10⁵`，直接在这么大的范围上建树会浪费空间。  
做法是把所有会出现的数值映射到 `[1 … m]` 的紧凑序号：

- 把所有 `a[i]` 和 `a[i] - diff` 收集到一个列表里，排序去重；
- 用字典把原始值 → 压缩后的序号。

这样 Fenwick 树只需要大小 `m ≤ 2n`，非常省内存。

**步骤概览**

1. 计算数组 `a`（`a[i] = nums1[i] - nums2[i]`）。
2. 把 `a[i]` 与 `a[i] - diff` 全部放进 `vals`，离散化得到映射 `idx`。
3. 初始化 Fenwick 树 `bit`（大小为 `len(vals)`）。
4. **从右往左遍历** `i = n-1 … 0`  
   - 设 `need = a[i] - diff`。  
   - 用 `bisect_left` 在 `vals` 中找到 `need` 的压缩下标 `pos_need`。  
   - `cnt_ge = total_inserted - bit.query(pos_need - 1)` → 右侧满足 `≥ need` 的元素个数。  
   - 把 `cnt_ge` 加到答案 `ans`。  
   - 把当前的 `a[i]` 插入 Fenwick 树：`bit.update(idx[a[i]], 1)`。  
   - `total_inserted` 加 1（用于后面的 “总数” 计算）。
5. 返回 `ans`。

> **类比**：想象我们有一本“已收集的数字账本”，每次往账本里写入一个新数字（右侧的 `a[j]`），随后要快速查出账本里有多少数字 **不小于** 某个阈值（`a[i] - diff`）。Fenwick 树就是这本高效的账本。

---

#### 代码（Python）

```python
from bisect import bisect_left

class FenwickTree:
    """Fenwick 树（Binary Indexed Tree），实现前缀和查询和单点增量"""
    def __init__(self, size: int):
        self.n = size
        self.bit = [0] * (size + 1)          # 1-indexed，便于实现

    def update(self, idx: int, delta: int):
        """把 idx 位置的值加 delta（这里 delta 永远是 1）"""
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx               # lowbit，向上遍历

    def query(self, idx: int) -> int:
        """返回前缀和：1 .. idx 位置的累计值"""
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx               # lowbit，向下遍历
        return s

def count_pairs(nums1, nums2, diff):
    """
    主函数：返回满足
        nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff   (i < j)
    的 (i, j) 对数
    """
    n = len(nums1)

    # 1️⃣ 计算 a[i] = nums1[i] - nums2[i]
    a = [nums1[i] - nums2[i] for i in range(n)]

    # 2️⃣ 离散化：收集所有 a[i] 与 a[i] - diff
    vals = list(set(a + [x - diff for x in a]))
    vals.sort()                               # 排序后得到有序坐标轴
    # 把原始值映射到 1 .. m（Fenwick 树使用 1-indexed）
    comp = {v: i + 1 for i, v in enumerate(vals)}   # +1 为了配合 Fenwick

    # 3️⃣ 初始化 Fenwick 树
    bit = FenwickTree(len(vals))
    total = 0          # 已经插入到树中的元素数量（即右侧元素的个数）
    ans = 0

    # 4️⃣ 逆序遍历
    for i in range(n - 1, -1, -1):
        need = a[i] - diff                     # 我们需要的下界
        # 在离散化后的坐标轴中找到 need 的位置（左侧第一个 >= need）
        pos = bisect_left(vals, need) + 1      # +1 转成 Fenwick 的下标
        # 前缀和 query(pos-1) 得到 ≤ need-1 的元素个数
        # 所以 ≥ need 的元素数 = total - ≤(need-1)
        cnt_ge = total - bit.query(pos - 1)
        ans += cnt_ge

        # 把当前的 a[i] 加入 Fenwick，供左侧的 i-1 使用
        bit.update(comp[a[i]], 1)
        total += 1

    return ans
```

**代码要点注释**

| 行号 | 关键含义 |
|------|----------|
| 7‑14 | Fenwick 树的实现，`update` 用来把新出现的 `a[j]` 加进去，`query` 用来求「前缀和」即「≤ 某值」的个数。 |
| 22‑27 | 把每个位置的 `nums1 - nums2` 预先算好，得到数组 `a`。 |
| 30‑33 | 为了在树上使用离散化的下标，先把所有可能出现的数（`a[i]` 与 `a[i]-diff`）收集、排序、去重。 |
| 38‑41 | `comp` 把原始数映射到 1‑based 的索引，Fenwick 只能处理正整数下标。 |
| 45‑57 | 逆序遍历：  
  - `need = a[i] - diff` 是当前左指针需要的阈值。  
  - `bisect_left` 在有序的 `vals` 中定位 `need`，得到 **≥ need** 的第一个位置。  
  - `total - bit.query(pos-1)` 计算右侧已有元素中 **≥ need** 的数量。  
  - 把当前 `a[i]` 加入树中，`total` 同时递增。 |
| 60 | 最后返回累计的答案。 |

---

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 离散化排序 `O(n log n)`。  
  - 逆序遍历中每次 `query` 与 `update` 都是 `O(log n)`，共 `n` 次。  
  - 与暴力的 `O(n²)` 相比，提升了数量级，能够轻松处理 `n = 10⁵` 的数据。

- **空间复杂度**：`O(n)`  
  - 需要存放 `a`、离散化后的坐标数组 `vals`，以及 Fenwick 树本身，都是线性规模。  

---

## 心得  

- **核心技巧**：把原始不等式化简为 `a[i] <= a[j] + diff`，进而转化为 “在右侧统计 ≥ 某阈值的元素数量”。  
- **适用场景**：  
  1. **“前缀/后缀满足阈值”** 类的问题（如 LeetCode 1248 – Count Number of Nice Subarrays）。  
  2. **“逆序遍历 + 统计满足条件的后缀”**（如 327. Count of Range Sum）。  
  3. **需要快速求 “≥ / ≤ 某值的元素个数”** 的场景，常用 Fenwick 树或线段树实现。  

> **解题钥匙**：**把不等式整理成单调形式 → 用有序结构快速计数**。

---

## 反思  

- **第一反应**：看到 `i < j` 与不等式，立刻想到“遍历所有对”。但这会超时，于是要寻找**单调/前缀**的特征。  
- **最容易踩的坑**  
  1. **离散化忘记加入 `a[i] - diff`**：查询阈值可能不在原始 `a` 中，导致坐标映射错误。  
  2. **Fenwick 树下标从 1 开始**，若直接使用 `0` 会导致查询错误。  
  3. **边界条件**：当 `need` 小于所有离散化值时，`bisect_left` 返回 `0`，此时 `pos-1` 为 `0`，`query(0)` 必须返回 `0`（Fenwick 实现自然满足）。  
- **下次类似题的第一步**：**先把不等式整理成 “左侧值 ≤ 右侧值 + 常数” 的形式**，检查是否可以用**单调性 + 逆序遍历 + 有序统计结构**来降低复杂度。