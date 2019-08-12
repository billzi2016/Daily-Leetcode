# #528. 随机挑选带权重的索引 / Random Pick with Weight

> 难度：中等 · 标签：Array、Math、Binary Search、Prefix Sum、Randomized · [LeetCode 链接](https://leetcode.com/problems/random-pick-with-weight/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers w where w[i] describes the weight of the ith index.
You need to implement the function pickIndex(), which randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it. The probability of picking an index i is w[i] / sum(w).

**Examples**

**Example 1:**

```
Input
["Solution","pickIndex"]
[[[1]],[]]
Output
[null,0]

Explanation
Solution solution = new Solution([1]);
solution.pickIndex(); // return 0. The only option is to return 0 since there is only one element in w.
```

**Example 2:**

```
Input
["Solution","pickIndex","pickIndex","pickIndex","pickIndex","pickIndex"]
[[[1,3]],[],[],[],[],[]]
Output
[null,1,1,1,1,0]

Explanation
Solution solution = new Solution([1, 3]);
solution.pickIndex(); // return 1. It is returning the second element (index = 1) that has a probability of 3/4.
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 0. It is returning the first element (index = 0) that has a probability of 1/4.

Since this is a randomization problem, multiple answers are allowed.
All of the following outputs can be considered correct:
[null,1,1,1,1,0]
[null,1,1,1,1,1]
[null,1,1,1,0,0]
[null,1,1,1,0,1]
[null,1,0,1,0,0]
......
and so on.
```

**Constraints**

- 1 <= w.length <= 104
- 1 <= w[i] <= 105
- pickIndex will be called at most 104 times.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的正整数数组 `w`，其中 `w[i]` 表示第 `i` 个下标的权重（weight）。  
请实现函数 `pickIndex()`，该函数在 `[0, w.length - 1]`（含两端）范围内随机返回一个下标。返回下标 `i` 的概率为 `w[i] / sum(w)`，其中 `sum(w)` 为数组中所有元素的和。

**示例 1**  
```text
Input
["Solution","pickIndex"]
[[[1]],[]]

Output
[null,0]

Explanation
Solution solution = new Solution([1]);
solution.pickIndex(); // 返回 0。因为 w 中只有一个元素，只能返回下标 0。
```

**示例 2**  
```text
Input
["Solution","pickIndex","pickIndex","pickIndex","pickIndex","pickIndex"]
[[[1,3]],[],[],[],[],[]]

Output
[null,1,1,1,1,0]

Explanation
Solution solution = new Solution([1, 3]);
solution.pickIndex(); // 返回 1。下标 1 的元素权重为 3，出现概率为 3/4。
solution.pickIndex(); // 返回 1
solution.pickIndex(); // 返回 1
solution.pickIndex(); // 返回 1
solution.pickIndex(); // 返回 0。下标 0 的元素权重为 1，出现概率为 1/4。

由于本题涉及随机性，允许多种答案。以下输出均视为正确：
[null,1,1,1,1,0]  
[null,1,1,1,1,1]  
[null,1,1,1,0,0]  
[null,1,1,1,0,1]  
[null,1,0,1,0,0]  
…… 等等。
```

**约束条件**  

- `1 <= w.length <= 10^4`
- `1 <= w[i] <= 10^5`
- `pickIndex` 最多被调用 `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次一次地“抽签”**，把每个下标的权重看成抽签的纸条数。  
具体步骤：

1. 把所有权重加起来得到总和 `total = sum(w)`。  
2. 用随机数 `rand = random.randint(1, total)`，相当于在 `1 … total` 这串连续的纸条里随便抽一张。  
3. 从下标 `0` 开始累加权重 `cur += w[i]`，当 `cur` 第一次 **大于等于** `rand` 时，当前的下标 `i` 就是抽中的结果。

> **类比**：把权重看成装满糖果的盒子，盒子 0 有 `w[0]` 颗糖，盒子 1 有 `w[1]` 颗糖……把所有盒子排成一条长队，随机挑一颗糖，糖所在的盒子下标就是答案。

这个方法一定能得到正确的概率，因为每个下标出现的次数正好等于它的权重，占总糖果数的比例就是 `w[i]/sum(w)`。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, w: List[int]):
        # 保存原始权重，后面会直接遍历
        self.w = w
        # 计算总权重，后面用于生成随机数的范围
        self.total = sum(w)

    def pickIndex(self) -> int:
        # 在 1~total 之间随机抽一个整数（包含两端）
        target = random.randint(1, self.total)
        cur = 0                     # 累计已经遍历过的权重
        for i, weight in enumerate(self.w):
            cur += weight           # 把当前下标的权重加入累计和
            if cur >= target:      # 第一次累计和 >= 目标值，就命中该下标
                return i
        # 理论上不会走到这里，因为 target 一定会在累计和中被命中
        return -1
```

> **关键行解释**  
> - `random.randint(1, self.total)`: 随机生成 **闭区间** `[1, total]`，确保每一张“糖”都有同等机会被抽到。  
> - `if cur >= target:`: 当累计的糖数已经覆盖到抽中的那颗糖时，即找到了对应的下标。

#### 复杂度

- **时间复杂度**：`O(n)` —— 这里的 `n` 是数组 `w` 的长度。每次 `pickIndex` 需要线性遍历一次，最坏情况下要走到最后一个元素。可以把 `O(n)` 想象成“随数组长度成正比增长”，数组越大，花的时间越多。  
- **空间复杂度**：`O(1)` —— 只用了常数级的额外变量（`cur`、`target`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要从头遍历**，如果 `pickIndex` 被调用很多次（题目允许最多 `10⁴` 次），这会导致大量的重复工作。  
我们可以把“累计权重”这一步 **提前一次性完成**，把数组转化成 **前缀和数组**（prefix sum）。这样：

1. **预处理**：一次遍历把 `w` 转成前缀和 `pre = [w[0], w[0]+w[1], …]`。  
   - `pre[i]` 表示下标 `0…i` 的权重总和。  
2. **抽签**：仍然在 `1 … total` 之间随机生成整数 `target`。  
3. **定位**：在前缀和数组中寻找第一个 **≥ target** 的位置。因为前缀和是 **单调递增** 的，完全可以使用 **二分查找**（binary search）在 `O(log n)` 时间内完成。

> **类比**：前缀和就像把所有糖果排好序并记录每一步的累计数量。抽到第 `k` 颗糖后，只需要在这张累计表里“快速定位”到底是哪盒糖（下标），这一步就像在有序的电话号码簿里用二分法找号码——非常快。

二分查找的核心是：每次比较中间位置的前缀和 `pre[mid]` 与目标 `target`，如果 `pre[mid] < target`，说明目标在右半边；否则在左半边（包括 `mid` 本身），最终收敛到最左侧满足条件的下标。

#### 代码（Python）

```python
import random
import bisect
from typing import List

class Solution:
    def __init__(self, w: List[int]):
        # 预处理：构造前缀和数组
        self.prefix = []
        cur = 0
        for weight in w:
            cur += weight          # 累计权重
            self.prefix.append(cur)  # 保存每一步的累计和
        self.total = cur           # 整体权重和，等于最后一个前缀和

    def pickIndex(self) -> int:
        # 随机抽取 1~total 之间的整数
        target = random.randint(1, self.total)
        # 使用二分查找定位第一个 prefix >= target 的下标
        # bisect_left 返回左侧插入点，即满足条件的最左下标
        idx = bisect.bisect_left(self.prefix, target)
        return idx
```

> **关键行解释**  
> - `self.prefix.append(cur)`: 把每一步的累计和存进列表，形成单调递增的序列。  
> - `bisect.bisect_left(self.prefix, target)`: Python 标准库的二分实现，时间复杂度是 `O(log n)`，直接返回满足 `prefix[idx] >= target` 的最左侧下标。

#### 复杂度

- **时间复杂度**：  
  - 构造前缀和 `O(n)`（只在初始化时执行一次）。  
  - 每次 `pickIndex` 使用二分查找 `O(log n)`。  
  与暴力解的 `O(n)` 相比，`log n` 只会随数组长度的 **对数** 增长，极大提升效率。  
- **空间复杂度**：`O(n)` —— 需要额外存储前缀和数组，长度与原数组相同。

---

## 心得

- **核心技巧**：前缀和 + 二分查找  
- **适用场景**：  
  1. “按照权重随机抽取” 类的问题（如随机抽奖、负载均衡）。  
  2. “区间求和” 或 “区间查询” 场景，需要快速定位累计值的下标。  
  3. “离散概率分布的采样” 以及 “分段函数求值”。  
- **一句话总结**：把一次遍历的线性累计变成一次性预处理，再用二分把查询从 `O(n)` 降到 `O(log n)`。

---

## 反思

- **第一反应**：直接模拟抽签，用循环累加寻找目标下标——最自然但效率低。  
- **最容易踩的坑**：  
  - 随机数的取值范围要是 **闭区间** `[1, total]`，否则会出现偏差。  
  - 前缀和数组可能会非常大（最大 `10⁴ * 10⁵ = 10⁹`），但仍在 Python 整数范围内，注意不要使用 `float` 造成精度问题。  
  - 二分查找时要返回 **左侧** 插入点，`bisect_left` 正好满足需求；若手写二分，需要注意循环退出条件，防止死循环。  
- **下次第一步**：先思考能否把“累计权重”一次性算好（前缀和），再考虑怎样快速定位（二分），而不是每次都重新遍历。这样能把时间复杂度从线性降到对数。