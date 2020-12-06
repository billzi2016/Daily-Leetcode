# #1093. 大样本统计 / Statistics from a Large Sample

> 难度：中等 · 标签：Array、Math、Probability and Statistics · [LeetCode 链接](https://leetcode.com/problems/statistics-from-a-large-sample/)

---

## 题目（英文原版）

**Description**

You are given a large sample of integers in the range [0, 255]. Since the sample is so large, it is represented by an array count where count[k] is the number of times that k appears in the sample.
Calculate the following statistics:
Return the statistics of the sample as an array of floating-point numbers [minimum, maximum, mean, median, mode]. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: count = [0,1,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: [1.00000,3.00000,2.37500,2.50000,3.00000]
Explanation: The sample represented by count is [1,2,2,2,3,3,3,3].
The minimum and maximum are 1 and 3 respectively.
The mean is (1+2+2+2+3+3+3+3) / 8 = 19 / 8 = 2.375.
Since the size of the sample is even, the median is the average of the two middle elements 2 and 3, which is 2.5.
The mode is 3 as it appears the most in the sample.
```

**Example 2:**

```
Input: count = [0,4,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: [1.00000,4.00000,2.18182,2.00000,1.00000]
Explanation: The sample represented by count is [1,1,1,1,2,2,2,3,3,4,4].
The minimum and maximum are 1 and 4 respectively.
The mean is (1+1+1+1+2+2+2+3+3+4+4) / 11 = 24 / 11 = 2.18181818... (for display purposes, the output shows the rounded number 2.18182).
Since the size of the sample is odd, the median is the middle element 2.
The mode is 1 as it appears the most in the sample.
```

**Constraints**

- count.length == 256
- 0 <= count[i] <= 109
- 1 <= sum(count) <= 109
- The mode of the sample that count represents is unique.

---

## 题目（中文翻译）

你得到一个取值范围在 `[0, 255]` 的整数的大样本。由于样本规模庞大，它用一个数组 **count**（计数数组）来表示，其中 `count[k]` 是数值 `k` 在样本中出现的次数。

计算以下统计量：

- 最小值 `minimum`
- 最大值 `maximum`
- 均值 `mean`
- 中位数 `median`
- 众数 `mode`（样本的众数唯一）

返回一个浮点数数组 `[minimum, maximum, mean, median, mode]`。只要答案的误差在 `10⁻⁵` 以内即视为正确。

## 示例

### 示例 1
```text
Input: count = [0,1,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
... (已截断)
```

### 示例 2
```text
Input: count = [0,4,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
... (已截断)
```

## 约束条件
- `count.length == 256`
- `0 <= count[i] <= 10^9`
- `1 <= sum(count) <= 10^9`
- 样本的众数唯一（即 **mode** 唯一）

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个样本“展开”成一个普通的数组，然后直接用 Python 的内置函数求最小值、最大值、均值、中位数和众数。  

- **展开样本**：`count[k]` 表示数值 `k` 在样本中出现了多少次。把每个 `k` 按出现次数复制到一个列表里，就得到完整的样本。  
- **最小值 / 最大值**：直接调用 `min()` / `max()`，就像在字典里查找最小或最大的键。  
- **均值**：把所有数相加再除以样本大小 `total = sum(count)`。  
- **中位数**：先把列表排序（其实已经是升序），然后看样本大小是奇数还是偶数，取中间的一个或两个数的平均值。  
- **众数**：遍历一次，找出现次数最多的 `k`，这相当于在“查字典”，`k` 是词，`count[k]` 是页码，页码最大的词就是众数。  

> **为什么正确**  
> 因为我们把原始的计数信息完整地恢复成了原始样本的每一个元素，所有统计量都是在真正的数据上直接计算的，必然得到正确答案。

> **时间/空间分析（大白话）**  
> - **时间**：我们必须把每个出现的数字都复制一遍，假设样本总量是 `N`，那么复制、求和、排序等操作都要遍历 `N` 次，时间复杂度是 **O(N)**。如果 `N` 很大（题目允许高达 `10⁹`），这会非常慢，甚至根本跑不完。  
> - **空间**：需要一个长度为 `N` 的列表来存放所有数字，空间复杂度是 **O(N)**。对大样本来说，这根本不可能装进内存。  

#### 代码（Python）

```python
def sample_stats_bruteforce(count):
    # 1️⃣ 把计数展开成完整的样本列表
    sample = []
    for value, freq in enumerate(count):
        # freq 次把 value 加进列表
        sample.extend([value] * freq)   # 关键行：复制 value

    total = len(sample)                 # 样本总数 N
    # 2️⃣ 最小值、最大值
    minimum = min(sample)
    maximum = max(sample)

    # 3️⃣ 均值（平均数）
    mean = sum(sample) / total

    # 4️⃣ 中位数
    sample.sort()                       # 已经是升序，但这里写清楚思路
    if total % 2 == 1:                  # 样本大小是奇数
        median = float(sample[total // 2])
    else:                               # 样本大小是偶数
        median = (sample[total // 2 - 1] + sample[total // 2]) / 2.0

    # 5️⃣ 众数（出现次数最多的数）
    mode = max(range(256), key=lambda k: count[k])   # 在字典里找最大页码

    return [float(minimum), float(maximum), mean, median, float(mode)]
```

#### 复杂度  

- **时间复杂度**：`O(N)`（`N = sum(count)`），因为需要把每个出现的元素都复制一次。  
- **空间复杂度**：`O(N)`，需要额外的列表保存完整的样本。

> **含义解释**：  
> - `O(N)` 表示运行时间会随样本大小线性增长。  
> - 对于 `N = 10⁹`，这相当于要处理十亿次循环，远远超出常规机器的计算能力。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **“展开样本”** 这一步：  
- 复制十亿个数字既慢，又会把内存撑爆。  
- 其实我们不需要把每个元素都显式列出来，只要知道 **每个数出现了多少次**（这正是 `count` 提供的信息）就能直接算出所有统计量。

**核心思路**：一次遍历 `count`，累计必要的信息。  

1. **最小值 & 最大值**  
   - 从左到右找第一个 `count[i] > 0` → `minimum = i`。  
   - 从右到左找第一个 `count[i] > 0` → `maximum = i`。  
   - 这相当于在字典里顺序查找，最左/最右的非空键。

2. **均值（Mean）**  
   - 累加 `value * frequency` 得到所有数的总和 `total_sum`。  
   - 用 `total_sum / total_cnt`（`total_cnt = sum(count)`）得到均值。  
   - 只需要一次遍历，时间 O(256)，空间 O(1)。

3. **众数（Mode）**  
   - 在遍历时记录出现次数最多的 `value`，因为题目保证唯一。  

4. **中位数（Median）**  
   - 中位数是 **第 (total_cnt+1)//2** 个数（奇数）或 **第 total_cnt//2** 与 **第 total_cnt//2 + 1** 个数的平均（偶数）。  
   - 我们可以写一个 **帮助函数 `find_kth(k)`**，它顺序累加 `count`（类似前缀和），当累计的样本数第一次 **≥ k** 时，当前的 `value` 就是第 `k` 小的数。  
   - 只需要 **O(256)** 的时间，不需要展开数组。  

> **类比**：想象 `count` 是一本“分布表”，每一页记录某个数字出现了多少次。要找第 `k` 小的数字，就像从第一页翻起，累计页码，翻到累计页码 ≥ `k` 那一页，就是答案。  

#### 代码（Python）

```python
def sample_stats(count):
    """
    统计最小值、最大值、均值、中位数、众数。
    只遍历一次 count（长度固定 256），时间 O(256)，空间 O(1)。
    """
    total_cnt = sum(count)          # 样本总数 N
    # ---------- 1️⃣ 求最小值、最大值、均值、众数 ----------
    minimum = None
    maximum = None
    total_sum = 0                   # 所有数的加权和
    mode = None
    mode_cnt = -1

    for value, freq in enumerate(count):
        if freq == 0:
            continue
        # 最小值：第一次出现的 value
        if minimum is None:
            minimum = value
        # 最大值：每次出现都更新，遍历结束后自然是最大的
        maximum = value

        total_sum += value * freq    # 累加加权和

        # 记录出现次数最多的 value → 众数
        if freq > mode_cnt:
            mode_cnt = freq
            mode = value

    mean = total_sum / total_cnt    # 均值

    # ---------- 2️⃣ 辅助函数：找第 k 小的数 ----------
    def find_kth(k: int) -> int:
        """返回样本中第 k 小的数（k 从 1 开始计数）"""
        cum = 0                     # 累计出现次数（前缀和）
        for value, freq in enumerate(count):
            cum += freq
            if cum >= k:            # 第一次累计不小于 k 的位置
                return value
        # 理论上不会走到这里，因为 k <= total_cnt
        return -1

    # ---------- 3️⃣ 计算中位数 ----------
    if total_cnt % 2 == 1:          # 样本大小是奇数
        median = float(find_kth(total_cnt // 2 + 1))
    else:                           # 样本大小是偶数
        left = find_kth(total_cnt // 2)          # 第 N/2 小
        right = find_kth(total_cnt // 2 + 1)     # 第 N/2+1 小
        median = (left + right) / 2.0

    # ---------- 4️⃣ 返回结果 ----------
    return [
        float(minimum),   # minimum
        float(maximum),   # maximum
        mean,             # mean
        median,           # median
        float(mode)       # mode
    ]
```

#### 复杂度  

- **时间复杂度**：`O(256)`，即 **O(1)**（因为 256 是常数），因为我们只遍历一次长度固定的 `count`，以及两次（最多）调用 `find_kth`，每次也是一次线性遍历。  
  - 与暴力解的 `O(N)`（`N` 可能是十亿）相比，快了 **几千万倍**，几乎瞬间完成。  
- **空间复杂度**：`O(1)`，只用了若干个整数变量，未随样本规模增长。

> **含义解释**：  
> - `O(1)` 表示不管样本有多大，程序占用的额外内存几乎不变。  
> - 这正是我们利用 **计数数组** 这个“压缩”信息的好处。

---

## 心得  

- **核心技巧**：利用 **计数数组 + 前缀和** 在不展开样本的前提下直接定位第 k 小的元素。  
- **适用的题型**：  
  1. “频率直方图”类问题，例如 LeetCode 645 *Set Mismatch*（需要找缺失与重复数字）。  
  2. “分位数/中位数”在大数据流中求解，例如 295 *Find Median from Data Stream*（使用两个堆的思路）。  
  3. 任何给出 **值域固定且频次已知** 的统计题目。  
- **一句话总结**：  
  > “把计数数组当作‘压缩的原始数据’，用累计计数直接定位第 k 小的数，既省时又省空间。”

---

## 反思  

- **第一反应**：把 `count` 展开成完整数组再用常规方法求统计量。  
- **最容易踩的坑**：  
  - 忘记样本总数可能非常大，导致内存溢出或超时。  
  - 中位数的索引计算错误（奇偶数的区别）。  
  - `find_kth` 中累计时没有考虑 `k` 从 1 开始，导致返回错误的值。  
- **下次类似题的第一步**：  
  - 先检查输入是否已经是 **计数/频次** 形式，思考能否 **直接在计数上做前缀和**，而不是先展开。这样往往能把时间从 `O(N)` 降到 `O(值域大小)`。