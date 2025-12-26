# #3468. 找出复制数组的数量 / Find the Number of Copy Arrays

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-copy-arrays/)

---

## 题目（英文原版）

**Description**

You are given an array original of length n and a 2D array bounds of length n x 2, where bounds[i] = [ui, vi].
You need to find the number of possible arrays copy of length n such that:
Return the number of such arrays.

**Examples**

**Example 1:**

```
Input: original = [1,2,3,4], bounds = [[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation:
The possible arrays are:
```

**Example 2:**

```
Input: original = [1,2,3,4], bounds = [[1,10],[2,9],[3,8],[4,7]]
Output: 4
Explanation:
The possible arrays are:
```

**Example 3:**

```
Input: original = [1,2,1,2], bounds = [[1,1],[2,3],[3,3],[2,3]]
Output: 0
Explanation:
No array is possible.
```

**Constraints**

- 2 <= n == original.length <= 105
- 1 <= original[i] <= 109
- bounds.length == n
- bounds[i].length == 2
- 1 <= bounds[i][0] <= bounds[i][1] <= 109

---

## 题目（中文翻译）

你被给定一个长度为 `n` 的数组 `original`，以及一个大小为 `n × 2` 的二维数组 `bounds`，其中 `bounds[i] = [u_i, v_i]`。  
你需要统计满足特定条件的长度为 `n` 的可能数组 `copy` 的个数。  
返回满足条件的数组数量。

**示例 1**  
Input: `original = [1,2,3,4]`, `bounds = [[1,2],[2,3],[3,4],[4,5]]`  
Output: `2`  
Explanation:  
可能的数组如下：

**示例 2**  
Input: `original = [1,2,3,4]`, `bounds = [[1,10],[2,9],[3,8],[4,7]]`  
Output: `4`  
Explanation:  
可能的数组如下：

**示例 3**  
Input: `original = [1,2,1,2]`, `bounds = [[1,1],[2,3],[3,3],[2,3]]`  
Output: `0`  
Explanation:  
不存在满足条件的数组。

**约束条件**  
- `2 ≤ n == original.length ≤ 10^5`  
- `1 ≤ original[i] ≤ 10^9`  
- `bounds.length == n`  
- `bounds[i].length == 2`  
- `1 ≤ bounds[i][0] ≤ bounds[i][1] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求找出所有 **copy** 数组，使得  

* `copy[i]` 位于给定的区间 `bounds[i] = [u_i, v_i]` 中  
* `copy` 必须是 **original** 整体平移得到的数组，即存在一个整数 `k` 使得  
  `copy[i] = original[i] + k` 对所有 `i` 都成立  

最直接的做法是 **枚举** 所有可能的 `k`，把它代入每个位置检查是否满足对应的区间。  
如果 `k` 合法，就算作一种可行的 `copy`，最后把合法的 `k` 数目返回。

> **数据结构类比**  
> 把 `k` 想成一把 **调色板**，把原数组的每个颜色值（`original[i]`）往右平移 `k` 步，就得到新的颜色 `copy[i]`。每个位置都有自己的 “颜色容器” `bounds[i]`，只有调色板的平移量落在所有容器的交集里，才算合法。

#### 代码（Python）

```python
def numberOfCopyArrays(original, bounds):
    # 先把所有可能的 k 取出来（这里用 -10^9 ~ 10^9 只是示意，实际会超时）
    MIN_K, MAX_K = -10**9, 10**9
    ans = 0
    for k in range(MIN_K, MAX_K + 1):
        ok = True
        for a, (u, v) in zip(original, bounds):
            if not (u <= a + k <= v):   # copy[i] = a + k 必须落在区间内
                ok = False
                break
        if ok:
            ans += 1
    return ans
```

> 代码里每一步都有中文注释，帮助阅读。

#### 复杂度  

- **时间复杂度**：`O(R * n)`，其中 `R` 是 `k` 的取值范围（本题可达 `2·10^9`），显然不可接受。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外空间。

> **大白话解释**：  
> 这里的 `O(R·n)` 就像把所有可能的调色板一次又一次搬到每个画框里去检查，画框很多、调色板也很多，根本搬不过来。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**唯一需要关心的其实是平移量 `k`**，而不是整条 `copy`。  
对每一个位置 `i`，`k` 必须满足：

```
u_i ≤ original[i] + k ≤ v_i
⇔ u_i - original[i] ≤ k ≤ v_i - original[i]
```

所以每个位置都会给 `k` 限定一个 **区间**，所有位置的约束必须同时成立，  
这等价于把这些区间 **取交集**。  
交集得到的最终区间 `[L, R]`（如果交集为空则没有合法 `k`）里每一个整数 `k` 都对应唯一的一条合法 `copy`。

**核心步骤**  

1. 初始化合法区间为 `[-∞, +∞]`（实际可以用题目给的数值范围代替）。  
2. 遍历数组 `i = 0 … n-1`  
   * 计算当前位置对 `k` 的限制 `left = u_i - original[i]`、`right = v_i - original[i]`  
   * 用 `L = max(L, left)`、`R = min(R, right)` 把区间收紧  
3. 循环结束后  
   * 若 `L > R` → 交集为空，答案为 `0`  
   * 否则答案为 `R - L + 1`（区间中整数的个数）

> **类比**：把每个位置的 “颜色容器” 先平移到以 `k` 为坐标的轴上，所有容器的重叠部分就是合法的调色板位置。我们只要把这些容器一个接一个“压”到一起，最后剩下的就是可以放调色板的区域。

#### 代码（Python）

```python
def numberOfCopyArrays(original, bounds):
    """
    返回满足 copy[i] = original[i] + k 且 copy[i] ∈ bounds[i] 的不同 k 的个数
    """
    # 题目保证 1 ≤ original[i], u_i, v_i ≤ 10^9，故可以用这些上下界来初始化
    INF = 10**18                      # 足够大的正无穷
    L, R = -INF, INF                 # 当前合法 k 的区间

    for a, (u, v) in zip(original, bounds):
        # 对第 i 位，k 必须落在 [u - a, v - a] 之间
        left  = u - a
        right = v - a
        # 与已有区间取交集
        L = max(L, left)
        R = min(R, right)

    # 若交集为空，说明不存在合法的 k
    if L > R:
        return 0
    # 区间两端都是整数，答案就是区间长度 + 1
    return R - L + 1
```

> 关键行均加了中文注释，帮助初学者快速定位思路。

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  > 大白话：我们只需要一次“压盒子”，不需要搬来搬去检查每个可能的 `k`，所以快很多。  
- **空间复杂度**：`O(1)`，只用了几个整数保存当前区间。

---

## 心得

- **核心技巧**：把“每个位置的约束转化为对同一个未知量 `k` 的区间限制”，然后求所有区间的交集。  
- **适用题型**：  
  1. “所有元素整体平移 / 整体乘以同一个系数” 的约束类题目（如 *Maximum Value of an Ordered Subsequence*）。  
  2. 多个线性不等式只涉及同一个未知数的求解（如 *Find the Minimum Possible Integer*）。  
- **解题钥匙**：**统一变量 + 区间交集**。

---

## 反思

- **第一反应**：看到 `copy[0] 唯一决定其余`，立刻想到整体平移或整体乘法的模型。  
- **最容易踩的坑**：  
  - 忘记 `k` 必须是整数，最后返回的是区间长度 `+1` 而不是长度本身。  
  - 忽略了负数情况（本题数值均为正，但写通用代码时要把 `-INF`/`+INF` 处理好）。  
- **下次类似题的第一步**：先把每个位置的约束写成对同一个未知量的区间，然后求交集。这样往往能直接得到 `O(n)` 的最优解。