# #3152. **特殊数组 II** / Special Array II

> 难度：中等 · 标签：Array、Binary Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/special-array-ii/)

---

## 题目（英文原版）

**Description**

An array is considered special if every pair of its adjacent elements contains two numbers with different parity.
You are given an array of integer nums and a 2D integer matrix queries, where for queries[i] = [fromi, toi] your task is to check that subarray nums[fromi..toi] is special or not.
Return an array of booleans answer such that answer[i] is true if nums[fromi..toi] is special.

**Examples**

**Example 1:**

```
Input: nums = [3,4,1,2,6], queries = [[0,4]]
Output: [false]
Explanation:
The subarray is [3,4,1,2,6] . 2 and 6 are both even.
```

**Example 2:**

```
Input: nums = [4,3,1,6], queries = [[0,2],[2,3]]
Output: [false,true]
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- 1 <= queries.length <= 105
- queries[i].length == 2
- 0 <= queries[i][0] <= queries[i][1] <= nums.length - 1

---

## 题目（中文翻译）

如果一个数组的每一对相邻元素中的两个数字奇偶性（parity）不同，则该数组被视为特殊数组（special array）。

给定一个整数数组 `nums` 和一个二维整数矩阵 `queries`，对于 `queries[i] = [from_i, to_i]`，你的任务是检查子数组（subarray）`nums[from_i..to_i]` 是否为特殊数组。

返回一个布尔数组 `answer`，使得 `answer[i]` 为 `true` 当且仅当 `nums[from_i..to_i]` 为特殊数组。

---

### 示例

**示例 1**

> Input: `nums = [3,4,1,2,6]`, `queries = [[0,4]]`  
> Output: `[false]`  
> Explanation: 子数组为 `[3,4,1,2,6]`。其中 2 和 6 均为偶数。

**示例 2**

> Input: `nums = [4,3,1,6]`, `queries = [[0,2],[2,3]]`  
> Output: `[false,true]`  
> Explanation: 

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= queries[i][0] <= queries[i][1] <= nums.length - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**逐个检查**子数组 `nums[from .. to]` 中相邻的两个数是否奇偶不同。  
具体做法：

1. 取出子数组的所有元素（其实只要遍历下标 `from` 到 `to` 即可）。
2. 对每一对相邻元素 `nums[i]`、`nums[i+1]`（`i` 从 `from` 到 `to-1`），判断它们的奇偶性是否相同。  
   - 判断奇偶性可以用 `num % 2`：余数为 `0` 表示偶数，余数为 `1` 表示奇数。  
3. 只要出现一次 `nums[i]` 与 `nums[i+1]` 同奇同偶，就可以立刻返回 `False`（子数组不特殊）。遍历完都没有冲突，则返回 `True`。

> **类比**：把数组想成一排灯泡，奇数灯泡是红灯，偶数灯泡是蓝灯。我们要检查的就是“相邻的灯泡颜色是否交替”。暴力做法就是从左到右逐个查看每对灯泡的颜色。

**为什么正确**  
如果子数组里所有相邻的两数奇偶不同，那么按照题意它就是 *special*；只要有一对奇偶相同，就违背了“每一对相邻元素必须不同奇偶”的定义。遍历所有相邻对能够完整覆盖所有可能的冲突点，所以答案一定正确。

#### 代码（Python）

```python
def is_special_bruteforce(nums, queries):
    """
    暴力实现：对每个查询都线性扫描子数组
    返回一个布尔列表 answer，answer[i] 表示第 i 个查询的答案
    """
    answer = []
    for l, r in queries:               # 对每个查询
        ok = True                       # 先假设子数组是 special
        for i in range(l, r):          # 检查相邻元素对
            # (nums[i] % 2) 是奇偶标记，0=偶，1=奇
            if (nums[i] % 2) == (nums[i + 1] % 2):
                ok = False              # 发现奇偶相同，直接否定
                break                   # 可以提前结束本次循环
        answer.append(ok)
    return answer
```

#### 复杂度

- **时间复杂度**：`O( q * n )`（最坏情况是每个查询的子数组长度接近 `n`，需要遍历 `n-1` 对相邻元素）。  
  用大白话说，就是“每个查询都要走一遍数组”，如果 `n = 10⁵`、`q = 10⁵`，那就要跑 **10⁵ × 10⁵ = 10⁰¹⁰** 步，根本不可能在一秒内完成。

- **空间复杂度**：`O(1)`（除了输入本身和返回的答案外，只用了常数级的临时变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个查询都要重新遍历子数组**。如果我们能在**预处理阶段**把“哪些相邻位置是奇偶相同”记录下来，查询时只需要**看一次**这些记录，就能判断子数组是否满足要求。

**关键观察**  
- 对于下标 `i (0 ≤ i < n-1)`，只关心 `nums[i]` 与 `nums[i+1]` 的奇偶是否相同。  
- 把这件事抽象成一个二进制数组 `bad`：  
  `bad[i] = 1` 表示 `nums[i]` 与 `nums[i+1]` 同奇偶（**坏**，会破坏 special），  
  `bad[i] = 0` 表示奇偶不同（**好**）。  

如果我们把 `bad` 再做一次**前缀和**（累加），得到 `pref`，其中  

```
pref[i] = bad[0] + bad[1] + ... + bad[i-1]   (i 从 0 到 n)
```

（这里让 `pref[0] = 0`，方便计算区间和）

那么对于任意查询 `[l, r]`：

- 子数组里所有相邻对对应的 `bad` 索引区间是 `[l, r-1]`（因为最后一个元素没有右边的相邻元素）。  
- 只要 `bad[l] + … + bad[r-1] == 0`，说明这段区间里没有“坏”对，子数组就是 special。  
- 用前缀和可以 **O(1)** 计算这个区间和：

```
sum_bad = pref[r] - pref[l]   # 注意 pref 的长度是 n，取到 r 即可
```

如果 `sum_bad == 0` → `True`，否则 `False`。

> **类比**：想象把数组的每一条相邻“桥”标记为“好桥”(0) 或“坏桥”(1)。我们提前统计好桥和坏桥的累计数量（前缀和），查询时只要看从 `l` 到 `r` 之间有多少坏桥——如果为零，说明这段路全是好桥，安全通行。

**为什么正确**  
- `bad[i]` 完全等价于“`nums[i]` 与 `nums[i+1]` 是否同奇偶”。  
- 前缀和的差 `pref[r] - pref[l]` 正好把区间 `[l, r-1]` 的 `bad` 值相加。  
- 区间和为零当且仅当区间内每个 `bad[i]` 都是 0，即每对相邻元素奇偶不同。  

因此答案一定与题意相符。

#### 代码（Python）

```python
def is_special_optimized(nums, queries):
    """
    最优实现：先预处理一个前缀和数组，然后每个查询 O(1) 判断
    返回布尔列表 answer
    """
    n = len(nums)

    # 1) 构造 bad 数组：bad[i] = 1 表示相邻 i,i+1 奇偶相同
    bad = [0] * (n - 1)          # 长度 n-1，因为最后一个元素没有右邻居
    for i in range(n - 1):
        if (nums[i] % 2) == (nums[i + 1] % 2):
            bad[i] = 1          # 记录“坏”位置

    # 2) 前缀和 pref，pref[0] = 0，pref[i] 表示 bad[0..i-1] 的和
    pref = [0] * (n)             # 长度 n，方便直接用下标 r
    for i in range(1, n):
        pref[i] = pref[i - 1] + bad[i - 1]

    # 3) 逐个查询，利用前缀和 O(1) 判定
    answer = []
    for l, r in queries:
        # 区间 [l, r] 对应的 bad 索引是 [l, r-1]，其和 = pref[r] - pref[l]
        if pref[r] - pref[l] == 0:
            answer.append(True)     # 没有坏对，子数组是 special
        else:
            answer.append(False)    # 至少有一个坏对，不是 special
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n + q)`  
  - 预处理遍历一次数组得到 `bad` 与前缀和，花 `O(n)`。  
  - 每个查询只做常数次算术运算，`O(1)`，共 `q` 次，累计 `O(q)`。  
  与暴力的 `O(n·q)` 相比，提升了 **指数级**（从 10⁰¹⁰ 级别降到 2·10⁵ 级别）。

- **空间复杂度**：`O(n)`  
  - 需要额外存 `bad`（长度 `n-1`）和 `pref`（长度 `n`），都是线性空间。  
  - 用大白话说，就是“我们把原数组再复制一遍用来记‘哪里坏了’”，这在 10⁵ 规模下完全可以接受。

---

## 心得

- **核心技巧**：把“相邻元素奇偶是否相同”抽象成一个**二进制标记数组**，再利用**前缀和**快速求区间和。  
- **适用的题型**  
  1. **区间是否满足某种“全部相同/全部不同”** 的判定（例如：区间内是否全是正数、全是相同字符等）。  
  2. **统计区间内不满足条件的次数**（如区间内出现多少次逆序对、多少次相邻相等等）。  
  3. **区间和为零/非零的判断**（如子数组是否为平衡括号序列的简化版）。  

- **一句话总结解题钥匙**：  
  “把局部冲突预先标记，再用前缀和把区间冲突数量压缩到 O(1) 查询”。  

---

## 反思

- **第一反应**：看到“相邻元素奇偶不同”，自然想到遍历检查——也就是暴力解。  
- **最容易踩的坑**  
  - **下标越界**：`bad` 长度是 `n-1`，在构造前缀和或查询时一定要注意不访问 `bad[n-1]`。  
  - **查询区间长度为 1**：此时没有相邻对，子数组一定是 special，前缀和公式 `pref[r] - pref[l]` 仍然返回 0，需保证实现不出现 `IndexError`。  
  - **奇偶判断的细节**：使用 `num % 2`，而不是 `num & 1`（后者同样可行，但对初学者解释可能更抽象）。  

- **下次遇到同类题**，第一步应该想到：  
  “**把每两个相邻元素的关系压缩成一个一维标记**，然后**用前缀和/差分数组**把区间查询转化为 O(1) 的求和”。这样就能快速从暴力到最优。