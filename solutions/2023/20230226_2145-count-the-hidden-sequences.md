# #2145. 统计隐藏序列 / Count the Hidden Sequences

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-the-hidden-sequences/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of n integers differences, which describes the differences between each pair of consecutive integers of a hidden sequence of length (n + 1). More formally, call the hidden sequence hidden, then we have that differences[i] = hidden[i + 1] - hidden[i].
You are further given two integers lower and upper that describe the inclusive range of values [lower, upper] that the hidden sequence can contain.
Return the number of possible hidden sequences there are. If there are no possible sequences, return 0.

**Examples**

**Example 1:**

```
Input: differences = [1,-3,4], lower = 1, upper = 6
Output: 2
Explanation: The possible hidden sequences are:
- [3, 4, 1, 5]
- [4, 5, 2, 6]
Thus, we return 2.
```

**Example 2:**

```
Input: differences = [3,-4,5,1,-2], lower = -4, upper = 5
Output: 4
Explanation: The possible hidden sequences are:
- [-3, 0, -4, 1, 2, 0]
- [-2, 1, -3, 2, 3, 1]
- [-1, 2, -2, 3, 4, 2]
- [0, 3, -1, 4, 5, 3]
Thus, we return 4.
```

**Example 3:**

```
Input: differences = [4,-7,2], lower = 3, upper = 6
Output: 0
Explanation: There are no possible hidden sequences. Thus, we return 0.
```

**Constraints**

- n == differences.length
- 1 <= n <= 105
- -105 <= differences[i] <= 105
- -105 <= lower <= upper <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的长度为 `n` 的整数数组 `differences`，它描述了一个长度为 `n + 1` 的隐藏序列（hidden sequence）中相邻整数之间的差值。更形式化地，记隐藏序列为 `hidden`，则有  

```
differences[i] = hidden[i + 1] - hidden[i]
```  

另外，给定两个整数 `lower` 与 `upper`，它们定义了隐藏序列中所有元素必须落在的闭区间 `[lower, upper]`。  
求可能的隐藏序列的个数。如果不存在合法序列，返回 `0`。

**示例**  

*示例 1*  
```
Input: differences = [1,-3,4], lower = 1, upper = 6
Output: 2
Explanation: 可能的隐藏序列为：
- [3, 4, 1, 5]
- [4, 5, 2, 6]
因此返回 2。
```

*示例 2*  
```
Input: differences = [3,-4,5,1,-2], lower = -4, upper = 5
Output: 4
Explanation: 可能的隐藏序列为：
- [-3, 0, -4, 1, 2, 0]
- [-2, 1, -3, 2, 3, 1]
- [-1, 2, -2, 3, 4, 2]
- [0, 3, -1, 4, 5, 3]
因此返回 4。
```

*示例 3*  
```
Input: differences = [4,-7,2], lower = 3, upper = 6
Output: 0
Explanation: 不存在满足条件的隐藏序列，返回 0。
```

**约束条件**  
- `n == differences.length`  
- `1 <= n <= 10^5`  
- `-10^5 <= differences[i] <= 10^5`  
- `-10^5 <= lower <= upper <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
把隐藏序列的第一个数记为 `x`。  
- 已知 `differences[i] = hidden[i+1] - hidden[i]`，所以只要把 `x` 代进去，就可以**一步步往后推**出整个序列：  

```
hidden[0] = x
hidden[1] = x + differences[0]
hidden[2] = x + differences[0] + differences[1]
...
```

把上面的过程想象成 **“把字典里查到的词义依次累加”**：  
- `x` 相当于字典的起始页码，`differences` 是每一步要翻的页数，累加后得到每一页的实际位置。  

暴力做法就是把所有可能的 `x`（即所有在 `[lower, upper]` 区间的整数）都尝试一遍，  
每一次都生成完整的序列并检查 **所有元素是否仍然在 `[lower, upper]` 之间**。  
只要全部满足，就把计数器加一。

**为什么正确？**  
因为题目要求的是 **所有满足约束的隐藏序列的个数**，枚举每一个可能的首元素 `x`，并且对每个 `x` 完全确定后面的数，正好遍历了所有合法序列。

**时间/空间复杂度**  
- `upper - lower + 1` 可能有上万甚至上百万个取值，遍历每个 `x` 都要 O(n) 生成序列，**总时间复杂度是 O((upper‑lower+1)·n)**。  
  用大白话说，就是“先把每一个可能的起点都试一遍，再把每条路走完整”。  
- 只需要保存当前生成的序列（或者直接逐个检查），**额外空间是 O(1)**（不计输出计数器）。

显然，这种方法在 `n` 达到 10⁵、`upper‑lower` 也很大的情况下会超时。

---

#### 代码（Python）

```python
def count_hidden_sequences_bruteforce(differences, lower, upper):
    n = len(differences)
    ans = 0

    # 把所有可能的起点 x 枚举一遍
    for x in range(lower, upper + 1):
        cur = x          # 当前 hidden[i] 的值
        ok = True        # 标记这条序列是否一直在范围内

        # 根据 differences 推导后面的每个元素
        for d in differences:
            cur += d      # hidden[i+1] = hidden[i] + differences[i]
            if cur < lower or cur > upper:   # 超出范围立刻放弃
                ok = False
                break

        if ok:           # 全部元素都在范围内
            ans += 1

    return ans
```

> 代码中每一行都写了中文注释，直接可以运行（只要 `differences` 长度不太大，否则会超时）。

#### 复杂度  

- **时间复杂度**：`O((upper - lower + 1) * n)`。  
  直观解释：先遍历所有可能的起点（`upper‑lower+1` 次），每次再走完整条长度为 `n` 的路。  
- **空间复杂度**：`O(1)`。只用了几个整数变量，不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈**在于我们把每一个可能的起点 `x` 都重新走了一遍。  
其实，**所有序列的相对形状是固定的**，只和 `differences` 有关；  
不同的 `x` 只会把整个序列**整体平移**（上下平移），不会改变各元素之间的相对距离。

**关键观察**  

1. 设 `pref[i]` 为从第 0 项到第 i‑1 项的累计差值（前缀和），  
   `pref[0] = 0`，`pref[i] = differences[0] + … + differences[i‑1]`。  

   那么完整的隐藏序列可以写成  

   ```
   hidden[i] = x + pref[i]   (0 ≤ i ≤ n)
   ```

   这里的 `x` 仍是我们要选的首元素。

2. 把 `pref` 看成一个 **“相对坐标”** 的数组。  
   只要知道 `pref` 中的最小值 `minPref` 和最大值 `maxPref`，就能得到序列中 **最小元素** 与 **最大元素** 的相对距离：

   ```
   range = maxPref - minPref   # 序列中最大值和最小值的差距
   ```

   这一步不需要真正生成完整的序列，只要在一次遍历中维护最小、最大前缀和即可。  
   （可以把 `pref` 想象成一条爬山路线，`minPref` 是最低谷，`maxPref` 是最高峰，`range` 就是山谷到山顶的高度差。）

3. 现在把序列整体平移 `x`，要让所有元素落在 `[lower, upper]` 区间，需要满足：

   ```
   lower ≤ x + minPref   （最小元素不低于 lower）
   x + maxPref ≤ upper   （最大元素不超过 upper）
   ```

   两式合在一起得到 `x` 的合法取值范围：

   ```
   lower - minPref ≤ x ≤ upper - maxPref
   ```

   于是合法的整数 `x` 的个数就是：

   ```
   count = max(0, (upper - maxPref) - (lower - minPref) + 1)
   ```

   如果 `upper - maxPref` 小于 `lower - minPref`，说明根本找不到满足条件的 `x`，答案为 0。

4. **进一步简化**：  
   令 `totalRange = upper - lower + 1`（给定区间的长度），  
   `seqRange = maxPref - minPref`（隐藏序列内部的跨度）。  
   那么答案等价于：

   ```
   answer = max(0, totalRange - seqRange)
   ```

   直观解释：我们有一段长度为 `totalRange` 的“容器”，要放进长度为 `seqRange` 的“棒子”。  
   棒子可以平移的方式数就是容器长度减去棒子长度（如果容器太小装不下，答案为 0）。

**算法步骤**（一次遍历）  

1. 初始化 `cur = 0`（当前前缀和），`minPref = 0`，`maxPref = 0`。  
2. 依次遍历 `differences`：  
   - `cur += d`  
   - 更新 `minPref = min(minPref, cur)`，`maxPref = max(maxPref, cur)`。  
3. 计算 `seqRange = maxPref - minPref`。  
4. 计算 `totalRange = upper - lower + 1`。  
5. 返回 `max(0, totalRange - seqRange)`。

整个过程只需要 **O(n)** 的时间和 **O(1)** 的额外空间。

#### 代码（Python）

```python
def count_hidden_sequences(differences, lower, upper):
    """
    返回满足条件的 hidden 序列个数
    思路：利用前缀和得到序列的相对最值，再计算首元素 x 的合法取值范围
    """
    cur = 0            # 当前的前缀和 pref[i]
    min_pref = 0       # 前缀和的最小值
    max_pref = 0       # 前缀和的最大值

    # 一次遍历求出所有前缀和的极值
    for d in differences:
        cur += d
        if cur < min_pref:
            min_pref = cur
        if cur > max_pref:
            max_pref = cur

    seq_range = max_pref - min_pref          # 序列内部的跨度
    total_range = upper - lower + 1          # 给定区间的长度

    # 合法的首元素 x 的个数 = total_range - seq_range（若为负则为 0）
    return max(0, total_range - seq_range)
```

> 代码中每一步都有中文注释，直接可以在 LeetCode 上提交。

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历一次 `differences`，每个元素做常数次加减比较。  
  与暴力解相比，省去了对每个可能起点的重复遍历，速度提升了 `upper‑lower+1` 倍（在最坏情况下可达 10⁵ 倍）。
- **空间复杂度**：`O(1)`。只用了几个整数变量，不随 `n` 增长。

---

## 心得  

- **核心技巧**：把“差分数组”转化为前缀和，从而得到序列的相对位置；再用**整体平移**的思想把约束转化为首元素的取值区间。  
- **适用的题型**  
  1. “根据相邻差值恢复序列并判断范围” 类题（如 LeetCode 2134 – Minimum Swaps to Group All 1's II）。  
  2. “在给定区间内放置一个长度固定的区间” 的计数问题（比如把一根绳子放进箱子）。  
  3. 需要利用 **前缀和的最值** 来判断整体波动幅度的题目（如最大子数组和、最小子数组长度等）。  
- **一句话总结解题钥匙**：*“先算出序列内部的最小/最大相对位置，再看整个区间能把它平移多少次”。*

---

## 反思  

- **第一反应**：直接枚举首元素 `x`，把序列逐个生成——这在小数据时能跑通，却忽视了规模的限制。  
- **最容易踩的坑**  
  - 忘记把 `pref[0] = 0` 计入最值，导致 `seq_range` 少算一次。  
  - 在计算答案时忘记加 `+1`（因为区间是闭区间），会少算一个合法起点。  
  - 当 `seq_range` 大于 `total_range` 时直接返回负数，而不是 `0`。  
- **下次遇到同类题**：第一步先思考“**相对位置** 是否固定”，若是则尝试用前缀和或差分把绝对值的自由度抽离出来，再把约束转化为**首元素的取值范围**。这样往往能把 O(n·range) 的暴力降到 O(n)。