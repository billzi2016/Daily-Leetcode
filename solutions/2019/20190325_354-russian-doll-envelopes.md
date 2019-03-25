# #354. 俄罗斯套娃信封 / Russian Doll Envelopes

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/russian-doll-envelopes/)

---

## 题目（英文原版）

**Description**

You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi] represents the width and the height of an envelope.
One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height.
Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
Note: You cannot rotate an envelope.

**Examples**

**Example 1:**

```
Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
Output: 3
Explanation: The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).
```

**Example 2:**

```
Input: envelopes = [[1,1],[1,1],[1,1]]
Output: 1
```

**Constraints**

- 1 <= envelopes.length <= 105
- envelopes[i].length == 2
- 1 <= wi, hi <= 105

---

## 题目（中文翻译）

你得到一个二维整数数组 `envelopes`，其中 `envelopes[i] = [wi, hi]` 表示第 `i` 个信封的宽度 `wi` 和高度 `hi`。  
只有当一个信封的宽度和高度都严格大于另一个信封的宽度和高度时，前者才能放入后者。  
返回你可以进行俄罗斯套娃的最大信封数量（即把一个信封放进另一个信封，依次嵌套的最大长度）。  
注意：信封不能旋转。

**示例 1**  
**输入**: `envelopes = [[5,4],[6,4],[6,7],[2,3]]`  
**输出**: `3`  
**解释**: 可以形成的最长套娃序列为 3 个信封：`[2,3] => [5,4] => [6,7]`。

**示例 2**  
**输入**: `envelopes = [[1,1],[1,1],[1,1]]`  
**输出**: `1`

**约束条件**  
- `1 <= envelopes.length <= 10^5`  
- `envelopes[i].length == 2`  
- `1 <= wi, hi <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的信封排列**，检查每一种排列是否满足“宽度和高度都严格递增”。  
可以把每个信封想象成一个盒子，只有当后面的盒子比前面的盒子“大”（宽高都更大）时，才能把前面的盒子塞进去。  
因此我们可以：

1. 对所有信封进行全排列（就像把所有盒子随意排个序）。  
2. 按顺序检查这条序列是否满足宽高严格递增。  
3. 记录最长的合法序列长度，即为答案。

> **数据结构**：这里用到的只是普通的 **列表**（list），相当于把信封装进一个装信件的信箱里，一个信封对应列表中的一个元素。

**为什么能得到正确答案**  
因为我们遍历了**所有**可能的顺序，只要有一种顺序可以让信封形成俄罗斯套娃，那么在枚举过程中一定会出现这条序列，进而记录到最大长度。

**时间/空间复杂度**  
- **时间复杂度**：全排列的数量是 `n!`（n 的阶乘），每条序列检查一次需要 O(n) 时间，所以总时间是 **O(n!·n)**，这在实际中几乎不可接受。  
  - 用大白话说，n=10 时，10! ≈ 3.6 百万，已经很大；n=20 时，20! 超过 2.4 × 10¹⁸，根本不可能跑完。
- **空间复杂度**：递归实现全排列时需要 O(n) 的调用栈空间，外加保存当前排列的列表，也是 O(n)。

#### 代码（Python）

```python
import itertools

def max_envelopes_brute(envelopes):
    """
    暴力枚举所有排列，找出最长的合法套娃序列。
    只适用于 n 很小的情况（比如 n <= 8）。
    """
    n = len(envelopes)
    best = 0

    # itertools.permutations 会生成所有排列
    for perm in itertools.permutations(envelopes):
        cnt = 1               # 当前序列至少可以放一个信封
        # 检查相邻信封是否满足宽高都严格递增
        for i in range(1, n):
            w1, h1 = perm[i - 1]
            w2, h2 = perm[i]
            if w2 > w1 and h2 > h1:
                cnt += 1
            else:
                # 一旦不满足，就从这里重新算起
                cnt = 1
        best = max(best, cnt)

    return best
```

#### 复杂度

- **时间复杂度**：O(n!·n)  
  - “n!” 表示所有排列的数量，乘以每条排列的线性检查时间。
- **空间复杂度**：O(n)  
  - 只需要保存当前排列和递归栈（或迭代生成器）的深度。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“枚举所有顺序”**，其实我们只需要关心 **宽度的顺序**，因为如果宽度已经排好序，剩下的只需要在高度上找最长严格递增的子序列（LIS，Longest Increasing Subsequence）。

**关键观察**：

1. **先按宽度升序排序**。如果宽度相同的信封直接放在一起会产生冲突，因为宽度相等时根本无法套娃。为了解决这个冲突，**把宽度相同的信封在高度上按 **降序** 排列**。这样在后面做 LIS 时，宽度相同的信封不会被错误地算进递增序列（因为高度是降序的，无法形成严格递增）。
2. 排序完毕后，问题化简为：**在高度序列中找最长严格递增子序列**。这正是经典的 LIS 问题。
3. LIS 可以用 **二分查找 + 贪心** 在 O(n log n) 时间完成。我们维护一个数组 `tails`，`tails[i]` 表示长度为 `i+1` 的递增子序列的最小可能结尾高度。遍历每个高度 `h`，在 `tails` 中二分定位第一个 ≥ `h` 的位置并替换；如果 `h` 大于所有 `tails`，则直接追加。

**类比**：把高度看成一列排好序的邮票编号，我们希望挑出尽可能多的邮票，使得编号严格递增。`tails` 就像是一个“邮票盒”，每个盒子里放的都是当前能得到的最小编号的邮票，这样后面遇到更大的编号时更容易继续往下拼。

**步骤**：

1. 按 `(w asc, h desc)` 排序。
2. 取排序后的高度列表 `heights`。
3. 用二分搜索维护 `tails`，得到 LIS 长度。

#### 代码（Python）

```python
from bisect import bisect_left

def max_envelopes(envelopes):
    """
    最优解：先排序，再在高度上做 LIS（二分搜索版）。
    时间复杂度 O(n log n)，空间复杂度 O(n)。
    """
    # 1. 按宽度升序、宽度相同的情况下高度降序排序
    #   - 宽度升序：保证后面的信封宽度一定不小于前面的
    #   - 高度降序：防止宽度相同的信封在 LIS 中被错误使用
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # 2. 只取高度构成序列
    heights = [h for _, h in envelopes]

    # 3. LIS（严格递增）——使用贪心 + 二分
    tails = []                     # tails[i] = 长度为 i+1 的递增子序列的最小结尾高度
    for h in heights:
        # 在 tails 中找到第一个 >= h 的位置
        idx = bisect_left(tails, h)
        if idx == len(tails):
            # h 大于所有已有的结尾，高度可以继续延长序列
            tails.append(h)
        else:
            # 用更小的高度替换，以便后面有更大的高度时还能接上去
            tails[idx] = h
    # tails 的长度就是 LIS 长度，也是最大套娃信封数
    return len(tails)
```

#### 复杂度

- **时间复杂度**：O(n log n)  
  - 排序需要 O(n log n)。遍历高度并二分搜索 `tails` 每次 O(log n)，共 n 次，仍是 O(n log n)。比暴力的阶乘时间快了几乎几个数量级。  
  - 用大白话说：如果有 10⁵ 个信封，log₂10⁵ ≈ 17，所以整体大约是 10⁵ × 17 次基本操作，完全可以在一秒内跑完。
- **空间复杂度**：O(n)  
  - 需要存放排好序的数组（原地排序）和 `tails`（最长可能是 n 长），所以是线性空间。

---

## 心得

- **核心技巧**：先排序再做 LIS（**先排序后做最长递增子序列**）。排序把二维约束转化为一维约束，LIS 用二分实现 O(n log n)。
- **适用的题型**：
  1. **最长递增子序列**（普通一维数组）。
  2. **桥梁问题**（两座城市的桥梁不能交叉，等价于先排序后 LIS）。
  3. **最大嵌套矩形/盒子**（类似本题，只是维度更多，需要先排序再多维 LIS）。
- **一句话总结**：**把二维套娃问题降维成一维递增序列，利用二分贪心得到 O(n log n) 的最优解**。

---

## 反思

- **第一反应**：直接想到遍历所有排列或递归搜索，想把每个信封都尝试放进去。
- **最容易踩的坑**：
  - **宽度相同的信封**：如果只按宽度升序排序，高度相同的信封会被错误计入 LIS，导致答案偏大。解决办法是宽度相同的情况下把高度 **降序** 排。
  - **严格递增 vs 非严格递增**：题目要求“都要更大”，所以在 LIS 中必须使用 **strict**（严格）递增；`bisect_left` 能帮我们实现这一点。
  - **边界情况**：所有信封尺寸相同、只有一个信封、或极大输入规模（10⁵）都需要算法在 O(n log n) 内完成。
- **下次遇到同类题**：第一步先 **思考能否把多维约束降到一维**（通过排序），随后在剩余维度上使用 **LIS / DP / 二分** 之类的高效子算法。这样往往能把看似指数级的搜索压到对数级。