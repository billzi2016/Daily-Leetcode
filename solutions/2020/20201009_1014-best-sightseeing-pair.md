# #1014. **最佳观光配对** / Best Sightseeing Pair

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/best-sightseeing-pair/)

---

## 题目（英文原版）

**Description**

You are given an integer array values where values[i] represents the value of the ith sightseeing spot. Two sightseeing spots i and j have a distance j - i between them.
The score of a pair (i < j) of sightseeing spots is values[i] + values[j] + i - j: the sum of the values of the sightseeing spots, minus the distance between them.
Return the maximum score of a pair of sightseeing spots.

**Examples**

**Example 1:**

```
Input: values = [8,1,5,2,6]
Output: 11
Explanation: i = 0, j = 2, values[i] + values[j] + i - j = 8 + 5 + 0 - 2 = 11
```

**Example 2:**

```
Input: values = [1,2]
Output: 2
```

**Constraints**

- 2 <= values.length <= 5 * 104
- 1 <= values[i] <= 1000

---

## 题目（中文翻译）

给定一个整数数组（integer array）`values`，其中 `values[i]` 表示第 `i` 个观光点的价值。两个观光点 `i` 和 `j` 之间的距离为 `j - i`。  
对于任意一对观光点 `(i < j)`，其得分（score）定义为  

```
values[i] + values[j] + i - j
```

即两个观光点价值之和减去它们之间的距离。  

返回任意一对观光点能够得到的最大得分。

---

### 示例

**示例 1**

```text
Input: values = [8,1,5,2,6]
Output: 11
Explanation: i = 0, j = 2, values[i] + values[j] + i - j = 8 + 5 + 0 - 2 = 11
```

**示例 2**

```text
Input: values = [1,2]
Output: 2
```

---

### 约束条件

- `2 <= values.length <= 5 * 10^4`
- `1 <= values[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的「景点对」都枚举一遍，逐个算出它们的分数  
`score = values[i] + values[j] + i - j ( i < j )`，最后取最大的那个。

- **用到的数据结构**：只需要一个普通的 Python 列表 `values`。我们会用两层 `for` 循环遍历下标 `i`、`j`，这跟在纸上把所有可能的两张卡片两两配对是一样的。
- **为什么正确**：因为我们真的把「所有」合法的 `(i, j)` 都算了一遍，必然不会漏掉最优的那一对，所以最大值一定会被找出来。
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(n²)**，因为外层循环跑 `n` 次，内层循环在最坏情况下也要跑 `n‑1` 次，整体是「平方级」的增长。可以把它想象成「把 n 张卡片全部两两配对」的工作量，会随卡片数的增加而快速膨胀。  
  - 空间复杂度是 **O(1)**，我们只用了几个整数变量来保存当前的最大分数，和输入规模无关。

#### 代码（Python）

```python
def maxScoreSightseeingPair_bruteforce(values):
    n = len(values)
    best = 0                     # 用来保存最大分数
    # 枚举所有 i < j 的组合
    for i in range(n):
        for j in range(i + 1, n):
            # 计算当前这对景点的得分
            score = values[i] + values[j] + i - j
            # 如果更大就更新 best
            if score > best:
                best = score
    return best
```

#### 复杂度

- **时间复杂度**：O(n²)  
  - 「平方级」的意思是如果把数组长度从 10 增加到 100，运算次数会从约 100 次涨到约 10 000 次，增长非常快。
- **空间复杂度**：O(1)  
  - 只用了常数个额外变量，不会随 `n` 增大而增加内存。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，分数公式可以拆成两部分：

```
values[i] + values[j] + i - j
= (values[i] + i) + (values[j] - j)
```

- 前面的 `(values[i] + i)` 只和左边的景点 `i` 有关，右边的 `j` 完全不影响它。  
- 后面的 `(values[j] - j)` 只和右边的景点 `j` 有关，左边的 `i` 完全不影响它。

**关键观察**：当我们从左到右遍历数组时，若已经知道「左侧所有位置的 `values[i] + i` 的最大值」`max_left`，那么对于当前的 `j`，最佳配对的得分立刻可以算出来：

```
candidate = max_left + (values[j] - j)
```

于是我们只需要一次遍历：

1. 初始化 `max_left = values[0] + 0`（第一个位置只能作为左侧点）。
2. 从 `j = 1` 开始：
   - 用 `max_left` 计算当前配对的得分 `candidate`，并更新全局最大 `ans`。
   - 再把 `values[j] + j` 与 `max_left` 比较，保留更大的值，供后面的 `j` 使用。

这就是**动态规划**的思想：`max_left` 实际上是「以当前位置为右端点时，左侧能够贡献的最优值」的前缀最值。我们只需要 **O(1)** 的额外空间，就能在 **O(n)** 的时间内完成。

> **类比**：把 `values[i] + i` 想成「左边的最高山峰」，`values[j] - j` 想成「右边的最低谷」。我们在遍历时随时记录左边的最高山峰，这样每到一个谷时，只要把山峰高度加上谷的高度，就得到这对山谷的「视野分数」。

#### 代码（Python）

```python
def maxScoreSightseeingPair(values):
    """
    一遍遍历求最大分数
    时间复杂度：O(n)
    空间复杂度：O(1)
    """
    n = len(values)
    # 第 0 位只能作为左侧点，先算出它的 (value + index)
    max_left = values[0] + 0
    ans = 0  # 用来保存全局最大分数

    # 从第 1 位开始，把它当作右侧点 j
    for j in range(1, n):
        # 右侧点贡献的 part 是 values[j] - j
        right_part = values[j] - j
        # 组合左侧的最优 max_left 与右侧的 part，得到当前配对的分数
        candidate = max_left + right_part
        # 更新全局最大分数
        if candidate > ans:
            ans = candidate

        # 更新左侧的最优值，为后面的 j 做准备
        # 这里相当于把当前点也当成左侧点，看看它的 (value + index) 是否更大
        left_candidate = values[j] + j
        if left_candidate > max_left:
            max_left = left_candidate

    return ans
```

#### 复杂度

- **时间复杂度**：O(n) — 只遍历一次数组，线性增长。相比暴力的 O(n²)，即使把 `n` 扩大 10 倍，运算次数也只会增加 10 倍，而不是 100 倍。
- **空间复杂度**：O(1) — 只用了常数个变量 `max_left、ans、j`，不随输入规模变化。

---

## 心得

- **核心技巧**：把原式拆解成两部分，使左侧信息可以提前累计（前缀最大），右侧信息在遍历时即时使用。相当于「一次遍历求前缀最值」的思路。
- **适用的题型**  
  1. **两数之和类的最大化**：如 `Maximum Sum of a Pair With Absolute Difference Less Than K`（需要前缀最大/最小）。  
  2. **带距离惩罚的最优配对**：如 `Maximum Score of a Pair With Distance Penalty`。  
  3. **单调栈/单调队列的滑动窗口最大值**（思路相似：维护窗口内的最优值）。
- **一句话总结**：把「左边的贡献」和「右边的贡献」分离，用前缀最大一次遍历即可得到全局最优。

---

## 反思

- **第一反应**：看到 `values[i] + values[j] + i - j`，自然会想到「两层循环枚举所有对」——这就是暴力解的雏形。
- **最容易踩的坑**  
  - **下标顺序**：一定要保证 `i < j`，否则公式会变成 `i - j` 为正数，意义不对。  
  - **初始化**：`max_left` 必须从第 `0` 位开始，否则会把不存在的左侧点计入。  
  - **负数情况**：虽然题目保证 `values[i] ≥ 1`，但 `i - j` 会是负数，必须在代码里用 `values[j] - j`（而不是 `j - values[j]`）保持符号正确。
- **下次思考路径**：看到「值 + 下标」或「值 - 下标」的组合时，第一步就尝试把式子拆分成「左侧只依赖 i」+「右侧只依赖 j」的形式，看看能否用「前缀最值」或「单调结构」在一次遍历中完成。这样往往能把 O(n²) 降到 O(n)。