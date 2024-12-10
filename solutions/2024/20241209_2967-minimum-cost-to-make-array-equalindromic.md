# #2967. **使数组等价回文的最小成本** / Minimum Cost to Make Array Equalindromic

> 难度：中等 · 标签：Array、Math、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-make-array-equalindromic/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums having length n.
You are allowed to perform a special move any number of times (including zero) on nums. In one special move you perform the following steps in order:
A palindromic number is a positive integer that remains the same when its digits are reversed. For example, 121, 2552 and 65756 are palindromic numbers whereas 24, 46, 235 are not palindromic numbers.
An array is considered equalindromic if all the elements in the array are equal to an integer y, where y is a palindromic number less than 109.
Return an integer denoting the minimum possible total cost to make nums equalindromic by performing any number of special moves.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: 6
Explanation: We can make the array equalindromic by changing all elements to 3 which is a palindromic number. The cost of changing the array to [3,3,3,3,3] using 4 special moves is given by |1 - 3| + |2 - 3| + |4 - 3| + |5 - 3| = 6.
It can be shown that changing all elements to any palindromic number other than 3 cannot be achieved at a lower cost.
```

**Example 2:**

```
Input: nums = [10,12,13,14,15]
Output: 11
Explanation: We can make the array equalindromic by changing all elements to 11 which is a palindromic number. The cost of changing the array to [11,11,11,11,11] using 5 special moves is given by |10 - 11| + |12 - 11| + |13 - 11| + |14 - 11| + |15 - 11| = 11.
It can be shown that changing all elements to any palindromic number other than 11 cannot be achieved at a lower cost.
```

**Example 3:**

```
Input: nums = [22,33,22,33,22]
Output: 22
Explanation: We can make the array equalindromic by changing all elements to 22 which is a palindromic number. The cost of changing the array to [22,22,22,22,22] using 2 special moves is given by |33 - 22| + |33 - 22| = 22.
It can be shown that changing all elements to any palindromic number other than 22 cannot be achieved at a lower cost.
```

**Constraints**

- 1 <= n <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`。  
你可以对 `nums` 任意次数（包括零次）执行一种特殊操作（**special move**）。一次特殊操作按以下顺序进行：

1. 选取一个整数 `y`，其中 `y` 为 **palindromic number（回文数）**，且 `y < 10^9`。  
2. 将数组中的若干元素（可以是全部或部分）修改为 `y`。  
3. 对每个被修改的元素 `x`，产生的代价为 `|x - y|`（绝对值）。

**回文数**是指正整数在其数字顺序反转后仍保持不变的数，例如 `121、2552、65756` 是回文数，而 `24、46、235` 不是。  
如果数组的所有元素都等于同一个回文数 `y`，则称该数组为 **equalindromic（等价回文）**。

返回通过执行任意次数的特殊操作，使 `nums` 变为等价回文所需的**最小可能总代价**。

---

### 示例

**示例 1**

```text
Input: nums = [1,2,3,4,5]
Output: 6
Explanation: 我们可以将所有元素改为 3（回文数），得到数组 [3,3,3,3,3]。  
使用 4 次特殊操作的总代价为 |1-3| + |2-3| + |4-3| + |5-3| = 6。  
可以证明，除 3 之外的任何回文数都无法得到更低的代价。
```

**示例 2**

```text
Input: nums = [10,12,13,14,15]
Output: 11
Explanation: 将所有元素改为 11（回文数），得到数组 [11,11,11,11,11]。  
总代价为 |10-11| + |12-11| + |13-11| + |14-11| + |15-11| = 11。  
可以证明，除 11 之外的任何回文数都无法得到更低的代价。
```

**示例 3**

```text
Input: nums = [22,33,22,33,22]
Output: 22
Explanation: 将所有元素改为 22（回文数），得到数组 [22,22,22,22,22]。  
使用 2 次特殊操作的总代价为 |33-22| + |33-22| = 22。  
可以证明，除 22 之外的任何回文数都无法得到更低的代价。
```

---

### 约束

- `1 <= n <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的回文数都枚举一遍**，然后把数组里的每个元素都改成这个回文数，算出总花费，最后取最小的那一个。  

- **回文数**可以类比成“正着读和倒着读都一样的单词”，比如 121、1331。  
- **枚举**相当于把一本字典从头到尾翻遍，字典的每一页（`key`）就是一个回文数，页码（`value`）就是我们要把数组全部改成的目标值 `y`。  
- 对每个 `y`，我们把数组里每个元素 `nums[i]` 与 `y` 的差的绝对值相加，`|nums[i] - y|` 就像是把第 `i` 本书从第 `nums[i]` 章节搬到第 `y` 章节需要的“搬运距离”。  

只要遍历了**所有**回文数，就一定能找到最小的总花费，所以方法是 **正确的**。

#### 代码（Python）

```python
def is_palindrome(x: int) -> bool:
    """判断整数 x 是否是回文数（正着倒着读一样）"""
    s = str(x)
    return s == s[::-1]

def minCost_bruteforce(nums):
    n = len(nums)
    # 题目说 y 必须是 < 10^9 的回文数
    max_val = 10 ** 9
    best = float('inf')
    # 从 1 开始枚举所有回文数（这里用最朴素的方式：逐个检查）
    for y in range(1, max_val):
        if not is_palindrome(y):
            continue
        # 计算把所有元素改成 y 的总费用
        cost = sum(abs(v - y) for v in nums)
        best = min(best, cost)
    return best
```

> **提示**：上述代码在真实数据上根本跑不完（`10^9` 次循环），只是一种“思路演示”。

#### 复杂度  

- **时间复杂度**：`O(P * n)`，其中 `P` 是回文数的个数。`P` 接近 `10^9`，所以这相当于 **十亿乘以数组长度**，在 1 秒内根本不可能完成。可以把 `O(P * n)` 想象成“要把所有学生（`n`）送到每一座城市（`P`）去”。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有回文数**。实际上我们并不需要遍历每一个回文数，只要找到离“最佳目标”最近的两个回文数即可。

**关键观察 1：**  
对任意整数 `y`，把所有 `nums[i]` 改成 `y` 的总费用是  
\[
\text{cost}(y)=\sum_{i=1}^{n} |\,\text{nums}[i] - y\,|
\]  
这是一条**绝对值求和函数**，它在 **中位数**（median）处取得最小值。  
> 类比：把一堆人排成一条直线，让大家都走到同一个位置，最省力的集合点就是中间的那个人站的位置（如果人数是偶数，可以任选中间两个位置中的任意一个）。

**关键观察 2：**  
目标 `y` 必须是回文数。于是我们只需要在**中位数 `m` 的左右两侧**找最近的回文数，分别记为 `p_low ≤ m ≤ p_high`（如果不存在，则只取一侧），计算这两个候选值的费用，取最小即可。

**如何快速得到最近的回文数？**  

给定整数 `x`（这里是中位数 `m`），我们可以：

1. 把 `x` 的左半部分（包括中间位）复制到右半，得到一个回文数 `cand`。  
   - 例如 `x = 12345` → 左半 `123` → 镜像得到 `12321`。  
2. 为了覆盖进位/借位的情况，还要把左半 **加 1** 再镜像，得到 `cand_up`，以及 **减 1** 再镜像，得到 `cand_down`。  
   - 继续上例：左半 `123` 加 1 → `124` → 镜像 `12421`；左半 `123` 减 1 → `122` → 镜像 `12221`。  

这三个（或两三个）候选数中，**离 `x` 最近的回文数**一定在其中。因为只改变了最左侧的“核心”部分，右侧被强制对称，已经覆盖了所有可能的最近回文。

**步骤概览**  

1. **排序**数组，得到中位数 `m`（如果 `n` 为偶数，随便取下标 `n//2` 即可）。  
2. **构造候选回文数**：  
   - `mirror(m)` → `p0`  
   - `mirror(m+1)` → `p_up`（如果 `m+1` 超过 `10^9`，直接忽略）  
   - `mirror(m-1)` → `p_down`（如果 `m-1` 小于 `1`，直接忽略）  
3. 把这些候选数中 **合法的回文数**（`1 ≤ p < 10^9`）放进列表 `cands`，再分别计算 `cost(p)`。  
4. 返回最小的费用。

**为什么只需要检查这几个人？**  
因为在绝对值求和函数里，离中位数更远的数只会让费用更大，而回文的“形状”只会在左半段的微调（+1、-1）时产生最近的回文。再往外走一步（+2、-2）得到的回文必然比 `+1` 或 `-1` 更远。

#### 代码（Python）

```python
def median(nums):
    """返回已排序数组的中位数（下标 n//2）"""
    n = len(nums)
    nums.sort()
    return nums[n // 2]                     # n 为偶数时任选左中位

def make_palindrome(x: int) -> int:
    """
    根据整数 x 生成以 x 的左半部分为核心的回文数。
    例如 x = 12345 -> 12321
    """
    s = str(x)
    l = len(s)
    # 前半（如果长度为奇数，包含中间那位）
    half = s[: (l + 1) // 2]
    # 把 half 反转后拼到右边（去掉中间位的重复）
    rev = half[::-1]
    if l % 2 == 1:          # 奇数长度需要去掉最中间的那位
        rev = rev[1:]
    return int(half + rev)

def nearest_palindromes(m: int):
    """返回离 m 最近的两个合法回文数（左侧、右侧），如果不存在返回空列表"""
    candidates = set()
    # 中心回文
    p0 = make_palindrome(m)
    candidates.add(p0)

    # m+1 的回文（向上寻找最近的）
    if m + 1 < 10 ** 9:
        candidates.add(make_palindrome(m + 1))

    # m-1 的回文（向下寻找最近的）
    if m - 1 >= 1:
        candidates.add(make_palindrome(m - 1))

    # 过滤非法值（必须是回文且 < 1e9）
    res = []
    for p in candidates:
        if 1 <= p < 10 ** 9 and str(p) == str(p)[::-1]:
            res.append(p)
    return res

def minCost_optimal(nums):
    """最优解：只检查中位数左右最近的回文数"""
    m = median(nums)                     # O(n log n) 排序得到中位数
    cand_vals = nearest_palindromes(m)   # O(log10 m) 构造回文（最多 3 个）

    best = float('inf')
    for y in cand_vals:
        cost = sum(abs(v - y) for v in nums)   # O(n) 计算费用
        best = min(best, cost)
    return best
```

> **关键注释**  
> - `make_palindrome` 把左半“核心”复制过去，时间只跟数字位数有关，最多 10 位（因为 `nums[i] ≤ 10^9`），所以可以视作 **O(1)**。  
> - `nearest_palindromes` 只产生至多 3 个回文数，常数级操作。  
> - 整体时间复杂度受排序支配，为 `O(n log n)`，空间只用了排序的数组（原地）和若干常数变量，**O(1)** 额外空间。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 解释：先对数组排序（像把学生按身高排好队）需要 `n log n` 次比较；之后只遍历一次数组计算费用（`O(n)`），但 `n log n` 已经是主导。相比暴力的 `O(P·n)`，这里的 `log` 只比线性慢一点点，完全可以接受。  
- **空间复杂度**：`O(1)`（不计入输入数组本身）  
  - 只用了几个整数变量和最多 3 个回文候选值，和数组长度无关。

---

## 心得

- **核心技巧**：**中位数最小化绝对值求和** + **利用回文数的结构快速生成最近的回文**。  
- **适用的题型**  
  1. “把数组所有元素改成同一个数，使费用最小”——如 **最小移动成本**、**最小绝对差** 类问题。  
  2. “目标值有额外约束（回文、质数、特定模）”——需要在最优区间（如中位数附近）搜索最近满足约束的数。  
- **一句话总结解题钥匙**：先找**理论最优点**（中位数），再在**约束空间**里向左右“靠拢”找到最近的合法点。

---

## 反思

- **第一反应**：直接遍历所有回文数，算费用——想到“枚举”但忽略了搜索空间太大。  
- **最容易踩的坑**  
  - 忘记 **回文数必须是正整数且 `< 10^9`**，导致生成的候选数可能越界。  
  - 在奇数位数时生成回文时多复制了中间位，需要去掉一次，否则会得到长度错误的数。  
  - 当数组长度为偶数时，任选左中位或右中位都可以，但如果只取左中位而不考虑右侧的最近回文，可能会漏掉更优解。  
- **下次类似题的第一步**：先**确定无约束时的最优目标**（如中位数或均值），再**围绕这个目标在满足约束的集合里寻找最近的可行解**。这样既能保证解的质量，又能把搜索范围压到常数级。