# #2122. 恢复原数组 / Recover the Original Array

> 难度：困难 · 标签：Array、Hash Table、Two Pointers、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/recover-the-original-array/)

---

## 题目（英文原版）

**Description**

Alice had a 0-indexed array arr consisting of n positive integers. She chose an arbitrary positive integer k and created two new 0-indexed integer arrays lower and higher in the following manner:
Unfortunately, Alice lost all three arrays. However, she remembers the integers that were present in the arrays lower and higher, but not the array each integer belonged to. Help Alice and recover the original array.
Given an array nums consisting of 2n integers, where exactly n of the integers were present in lower and the remaining in higher, return the original array arr. In case the answer is not unique, return any valid array.
Note: The test cases are generated such that there exists at least one valid array arr.

**Examples**

**Example 1:**

```
Input: nums = [2,10,6,4,8,12]
Output: [3,7,11]
Explanation:
If arr = [3,7,11] and k = 1, we get lower = [2,6,10] and higher = [4,8,12].
Combining lower and higher gives us [2,6,10,4,8,12], which is a permutation of nums.
Another valid possibility is that arr = [5,7,9] and k = 3. In that case, lower = [2,4,6] and higher = [8,10,12].
```

**Example 2:**

```
Input: nums = [1,1,3,3]
Output: [2,2]
Explanation:
If arr = [2,2] and k = 1, we get lower = [1,1] and higher = [3,3].
Combining lower and higher gives us [1,1,3,3], which is equal to nums.
Note that arr cannot be [1,3] because in that case, the only possible way to obtain [1,1,3,3] is with k = 0.
This is invalid since k must be positive.
```

**Example 3:**

```
Input: nums = [5,435]
Output: [220]
Explanation:
The only possible combination is arr = [220] and k = 215. Using them, we get lower = [5] and higher = [435].
```

**Constraints**

- 2 * n == nums.length
- 1 <= n <= 1000
- 1 <= nums[i] <= 109
- The test cases are generated such that there exists at least one valid array arr.

---

## 题目（中文翻译）

Alice 有一个下标从 **0** 开始的数组 `arr`，其中包含 `n` 个正整数。她任选一个正整数 `k`，并以如下方式创建了两个新的下标从 **0** 开始的整数数组 `lower` 和 `higher`：

（题目原文未给出具体构造方式，这里保留原描述）

不幸的是，Alice 丢失了这三个数组的全部内容。但她记得 `lower` 和 `higher` 中出现的所有整数，只是不记得每个整数属于哪个数组。请帮助 Alice 恢复原数组 `arr`。

给定一个长度为 `2n` 的整数数组 `nums`，其中恰好有 `n` 个整数来自 `lower`，其余 `n` 个来自 `higher`。返回原数组 `arr`。如果答案不唯一，返回任意一个合法的数组即可。

**注意**：测试用例保证至少存在一个合法的数组 `arr`。

## 示例

### 示例 1

**输入**  
```text
nums = [2,10,6,4,8,12]
```

**输出**  
```text
[3,7,11]
```

**解释**  
如果 `arr = [3,7,11]` 且 `k = 1`，则  
`lower = [2,6,10]`，`higher = [4,8,12]`。  
将 `lower` 与 `higher` 合并得到 `[2,6,10,4,8,12]`，它是 `nums` 的一个排列。

另一种合法情况是 `arr = [5,7,9]` 且 `k = 3`。此时 `lower = [2,4,6]`，`higher = [8,10,12]`。

---

### 示例 2

**输入**  
```text
nums = [1,1,3,3]
```

**输出**  
```text
[2,2]
```

**解释**  
如果 `arr = [2,2]` 且 `k = 1`，则 `lower = [1,1]`，`higher = [3,3]`。  
合并后得到 `[1,1,3,3]`，正好等于 `nums`。

需要注意的是，`arr` 不能取 `[1,3]`，因为在这种情况下唯一能够得到 `[1,1,3,3]` 的方式是 `k = 0`，而 `k` 必须为正整数。

---

### 示例 3

**输入**  
```text
nums = [5,435]
```

**输出**  
```text
[220]
```

**解释**  
唯一可能的组合是 `arr = [220]` 且 `k = 215`。使用它们得到 `lower = [5]`，`higher = [435]`。

## 约束

- `2 * n == nums.length`
- `1 <= n <= 1000`
- `1 <= nums[i] <= 10^9`
- 测试用例保证至少存在一个合法的数组 `arr`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `nums` 随意划分成两堆**，一堆当作 `lower`，另一堆当作 `higher`。  
然后检查这两堆是否能对应同一个正整数 `k`：

1. 设 `lower[i] = a_i - k`，`higher[i] = a_i + k`（`a_i` 是原数组 `arr` 的第 `i` 个元素）。  
2. 那么 `higher[i] - lower[i] = 2k`，也就是说每一对上下数的差必须相同且为偶数。  
3. 如果我们把两堆数分别排好序，只要对应位置的差都相等且为正偶数，就能推出 `k = diff/2`，再把 `lower[i] + k` 放回去得到 `arr`。

把所有可能的划分全部枚举出来，就是 **指数级** 的搜索（`C(2n, n)` 种划分），每一种划分再做一次差值检查。  

> **类比**：想象你有一盒混合了“左鞋”和“右鞋”的鞋子，却不知道哪只属于左脚、哪只属于右脚。暴力做法就是把所有鞋子随意分成两堆，然后检查每一左鞋和对应右鞋的大小差是否相同。显然，这种“随意分堆”会产生天文数字的组合，根本不可行。

> **为什么正确**：如果真的存在一种划分满足所有差值相等，那么这恰好就是题目要求的 `lower`、`higher` 与 `k`。  
> **为什么慢**：枚举所有划分的时间是 `O( C(2n, n) )`，对 `n≤1000` 完全不可接受。

#### 代码（Python）

```python
from itertools import combinations
from collections import Counter
from typing import List

def recoverArray_bruteforce(nums: List[int]) -> List[int]:
    m = len(nums)                     # m = 2n
    n = m // 2
    # 1. 所有可能的下标组合，选出 n 个数作为 lower
    for lower_idx in combinations(range(m), n):
        lower = [nums[i] for i in lower_idx]
        higher = [nums[i] for i in range(m) if i not in lower_idx]

        lower.sort()
        higher.sort()
        # 2. 检查对应差值是否相同且为正偶数
        diff = higher[0] - lower[0]
        if diff <= 0 or diff % 2:        # 必须是正偶数
            continue
        ok = True
        for l, h in zip(lower, higher):
            if h - l != diff:
                ok = False
                break
        if ok:                           # 找到合法解
            k = diff // 2
            return [l + k for l in lower]   # arr = lower + k
    return []   # 题目保证一定有解，这行永远不会到达
```

> **关键行中文注释**  
> - `combinations(range(m), n)`: 枚举所有可能的 “下标集合”，把对应的数当作 `lower`。  
> - `diff % 2`: 检查差值是否为偶数（因为 `higher - lower = 2k`）。  
> - `return [l + k for l in lower]`: 由 `lower = a - k` 逆推得到原数组 `a = lower + k`。

#### 复杂度  

- **时间复杂度**：`O( C(2n, n) * n )`，指数级，实际不可运行。  
  - `C(2n, n)` 表示从 `2n` 个数中挑 `n` 个的组合数，随 `n` 增大非常快。  
- **空间复杂度**：`O(n)`，主要是保存一次 `lower`、`higher` 的临时列表。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，真正的难点在于 **如何快速找出 `k`**，而不是枚举所有的下标划分。  
下面一步步推导出一种只枚举 `k` 的方法：

1. **最小值一定是 `lower` 中的一个**  
   对于每个原数 `a_i`，都有 `a_i - k < a_i + k`，所以在整个 `nums` 里，最小的数必然是某个 `lower[i]`（记作 `L_min`）。  

2. **利用 `L_min` 计算候选的 `k`**  
   假设 `L_min = a_x - k`，而它对应的 `higher` 为 `H = a_x + k`。  
   那么 `H - L_min = 2k` ⇒ `k = (H - L_min) / 2`。  
   因此，只要把 `L_min` 与数组中 **其他任意一个数** 当作可能的 `higher`，就能算出一个候选 `k`（前提是差值为正偶数，且 `k>0`）。

3. **对每个候选 `k` 进行“贪心配对”**  
   - 把 `nums` 按升序放进一个计数器 `cnt`（相当于字典，键是数值，值是出现次数）。  
   - 从小到大遍历 `nums`，若当前数 `x` 还有剩余（`cnt[x] > 0`），我们认为它是 `lower`。  
   - 对应的 `higher` 必须是 `x + 2k`（因为 `higher = (a - k) + 2k = a + k = lower + 2k`）。  
   - 检查 `cnt[x + 2k]` 是否大于 0，若是则配对成功，分别把两者的计数减 1，并把原数 `a = x + k` 加入答案。  
   - 若在配对过程中找不到对应的 `higher`，说明这个 `k` 不合法，直接放弃。

4. **找到合法 `k` 即可返回答案**  
   题目保证至少有一种合法的 `arr`，所以遍历完所有候选 `k`（最多 `2n-1` 种）一定能得到答案。

> **类比**：把 `nums` 想象成一堆“左脚鞋”和“右脚鞋”。我们先确定最小的左脚鞋 `L_min`，然后尝试把它和每一只可能的右脚鞋配对，算出鞋子的“宽度差” `2k`。接下来，我们用这个宽度差去“快速匹配”剩下的鞋子——只要左脚鞋 `x` 能找到正好大 `2k` 的右脚鞋，就配对成功。这样每次只需要一次线性扫描，无需枚举所有可能的左/右划分。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def recoverArray(nums: List[int]) -> List[int]:
    """
    返回原数组 arr，使得存在正整数 k，使得
    lower[i] = arr[i] - k, higher[i] = arr[i] + k,
    且 lower 与 higher 合在一起恰好是 nums（顺序任意）。
    """
    nums.sort()                       # 先排序，便于从小到大遍历
    n = len(nums) // 2                # 原数组长度
    smallest = nums[0]                # 必然是某个 lower

    # 枚举所有可能的 higher（对应 same original element）
    for j in range(1, len(nums)):
        diff = nums[j] - smallest
        if diff <= 0 or diff % 2:      # 必须是正偶数，才能得到整数 k
            continue
        k = diff // 2                  # 候选的正整数 k
        if k == 0:                     # k 必须为正
            continue

        cnt = Counter(nums)           # 计数器，类似“字典查词典”
        arr = []                       # 用来存放恢复出的原数组

        # 贪心配对：从小到大尝试把每个数当作 lower
        for x in nums:
            if cnt[x] == 0:            # 已经被配对完毕
                continue
            cnt[x] -= 1                # 把 x 当作 lower，用掉一次
            higher = x + 2 * k         # 对应的 higher 必须是 x + 2k
            if cnt[higher] == 0:       # 找不到匹配的 higher → 失败
                break
            cnt[higher] -= 1           # 配对成功，higher 也用掉一次
            arr.append(x + k)          # 原数 a = lower + k
        else:
            # 循环正常结束，说明所有数都成功配对
            if len(arr) == n:
                return arr             # 找到合法答案，直接返回

    # 根据题目保证，这里永远不会被执行
    return []
```

> **关键行中文注释**  
> - `nums.sort()`: 先把所有数排好序，最小的数一定是 `lower`。  
> - `if diff % 2`: 只保留能够得到整数 `k` 的候选（差值必须是偶数）。  
> - `cnt = Counter(nums)`: 把所有数放进“计数器”，相当于在字典里查“这本书还有几页”。  
> - `higher = x + 2 * k`: 根据 `higher = lower + 2k` 推导得到对应的上层数。  
> - `arr.append(x + k)`: 把配对成功的 `lower` 恢复成原数 `a = lower + k`。  

#### 复杂度  

- **时间复杂度**：`O(m²)`，其中 `m = 2n ≤ 2000`。  
  - 外层循环最多枚举 `m-1` 个候选 `k`（每个 `higher` 与最小值配对一次）。  
  - 内层配对遍历一次排序后的数组，时间为 `O(m)`。  
  - 所以总体 `O(m·m) = O(m²)`。在本题的约束 (`m ≤ 2000`) 下完全可接受。  
  - 与暴力解的指数级不同，这里只需要 **几千次** 操作。

- **空间复杂度**：`O(m)`。  
  - 主要是存放排序后的数组和计数器 `Counter`（最多保存 `m` 个不同的数）。  

---

## 心得  

- **核心技巧**：**利用最小值确定候选 `k`，再用贪心配对**。  
- **该技巧适用的题型**：  
  1. **配对差值相同的数组**（如 “两个数的差是固定值” 的配对题）。  
  2. **把一组数拆成两堆，使得每堆的某种线性关系相同**（例如 “把数组拆成等差数列的上、下半部分”。）  
- **一句话总结解题钥匙**：  
  > *“最小的数一定是左边（lower），把它和每个可能的右边（higher）算出 k，随后用一次线性扫描把所有数配对——只要配对成功，原数组就找到了。”*  

---

## 反思  

- **第一反应**：直接把 `nums` 随意划分成两堆检查差值——想到暴力搜索。  
- **最容易踩的坑**：  
  - 忘记 `k` 必须是 **正整数**，导致 `k = 0` 的非法解被误认为有效。  
  - 差值必须是 **偶数**，否则无法得到整数 `k`。  
  - 配对时要使用计数器而不是一次性删除列表，否则会因为重复元素而出错。  
- **下次遇到同类题**，第一步应该：  
  > *“先定位必然属于某一侧的极值（最小或最大），据此枚举可能的参数（这里是 `k`），再用一次线性/计数器配对验证。”*