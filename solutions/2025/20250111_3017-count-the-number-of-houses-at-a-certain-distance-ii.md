# #3017. 统计特定距离的房屋对数 II / Count the Number of Houses at a Certain Distance II

> 难度：困难 · 标签：Graph、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-houses-at-a-certain-distance-ii/)

---

## 题目（英文原版）

**Description**

You are given three positive integers n, x, and y.
In a city, there exist houses numbered 1 to n connected by n streets. There is a street connecting the house numbered i with the house numbered i + 1 for all 1 <= i <= n - 1 . An additional street connects the house numbered x with the house numbered y.
For each k, such that 1 <= k <= n, you need to find the number of pairs of houses (house1, house2) such that the minimum number of streets that need to be traveled to reach house2 from house1 is k.
Return a 1-indexed array result of length n where result[k] represents the total number of pairs of houses such that the minimum streets required to reach one house from the other is k.
Note that x and y can be equal.

**Examples**

**Example 1:**

```
Input: n = 3, x = 1, y = 3
Output: [6,0,0]
Explanation: Let's look at each pair of houses:
- For the pair (1, 2), we can go from house 1 to house 2 directly.
- For the pair (2, 1), we can go from house 2 to house 1 directly.
- For the pair (1, 3), we can go from house 1 to house 3 directly.
- For the pair (3, 1), we can go from house 3 to house 1 directly.
- For the pair (2, 3), we can go from house 2 to house 3 directly.
- For the pair (3, 2), we can go from house 3 to house 2 directly.
```

**Example 2:**

```
Input: n = 5, x = 2, y = 4
Output: [10,8,2,0,0]
Explanation: For each distance k the pairs are:
- For k == 1, the pairs are (1, 2), (2, 1), (2, 3), (3, 2), (2, 4), (4, 2), (3, 4), (4, 3), (4, 5), and (5, 4).
- For k == 2, the pairs are (1, 3), (3, 1), (1, 4), (4, 1), (2, 5), (5, 2), (3, 5), and (5, 3).
- For k == 3, the pairs are (1, 5), and (5, 1).
- For k == 4 and k == 5, there are no pairs.
```

**Example 3:**

```
Input: n = 4, x = 1, y = 1
Output: [6,4,2,0]
Explanation: For each distance k the pairs are:
- For k == 1, the pairs are (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), and (4, 3).
- For k == 2, the pairs are (1, 3), (3, 1), (2, 4), and (4, 2).
- For k == 3, the pairs are (1, 4), and (4, 1).
- For k == 4, there are no pairs.
```

**Constraints**

- 2 <= n <= 105
- 1 <= x, y <= n

---

## 题目（中文翻译）

你得到三个正整数 `n`、`x` 和 `y`。  
在一座城市中，有编号为 `1` 到 `n` 的房屋（houses），它们通过 `n` 条街道（streets）相连。对所有 `1 <= i <= n - 1`，都有一条街道连接编号为 `i` 的房屋和编号为 `i + 1` 的房屋。除此之外，还有一条额外的街道连接编号为 `x` 的房屋和编号为 `y` 的房屋。

对于每个满足 `1 <= k <= n` 的整数 `k`，求出满足**从 house1 到 house2 所需经过的最少街道数恰好为 `k`**的有序房屋对 `(house1, house2)` 的数量。  
返回一个 **1-indexed** 长度为 `n` 的数组 `result`，其中 `result[k]` 表示满足上述条件的房屋对数。  
注意，`x` 与 `y` 可能相等。

**约束条件**

- `2 <= n <= 10^5`
- `1 <= x, y <= n`

---

### 示例

#### 示例 1
```
Input: n = 3, x = 1, y = 3
Output: [6,0,0]
```
**解释**：逐一查看每一对房屋：
- 对于对 `(1, 2)`，可以直接从房屋 1 到房屋 2。
- 对于对 `(2, 1)`，可以直接从房屋 2 到房屋 1。
- 对于对 `(1, 3)`，可以直接从房屋 1 到房屋 3。
- 对于对 `(3, 1)`，可以直接从房屋 3 到房屋 1。
- 对于对 `(2, 3)`，可以从房屋 2 到房屋 3…（后文省略）

#### 示例 2
```
Input: n = 5, x = 2, y = 4
Output: [10,8,2,0,0]
```
**解释**：每个距离 `k` 对应的房屋对如下：
- `k == 1` 时，房屋对有  
  `(1, 2)`, `(2, 1)`, `(2, 3)`, `(3, 2)`, `(2, 4)`, `(4, 2)`, `(3, 4)`, `(4, 3)`, `(4, 5)`, `(5, 4)`。
- `k == 2` 时，房屋对有  
  `(1, 3)`, `(3, 1)`, `(1, 4)`, `(4, 1)`, `(2, 5)`, `(5, 2)`, `(3, 5)`, `(5, 3)`。
- `k == 3` 时，房屋对有  
  `(1, 5)`, `(5, 1)`。
- `k == 4`、`k == 5` 时，没有房屋对。

#### 示例 3
```
Input: n = 4, x = 1, y = 1
Output: [6,4,2,0]
```
**解释**：每个距离 `k` 对应的房屋对如下：
- `k == 1` 时，房屋对有  
  `(1, 2)`, `(2, 1)`, `(2, 3)`, `(3, 2)`, `(3, 4)`, `(4, 3)`。
- `k == 2` 时，房屋对有  
  `(1, 3)`, `(3, 1)`, `(2, 4)`, `(4, 2)`。
- `k == 3` 时，房屋对有  
  `(1, 4)`, `(4, 1)`。
- `k == 4` 时，没有房屋对。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这是一道 **求所有有序房屋对的最短路径长度** 的题目。  
城市的道路其实就是一条长度为 `n‑1` 的直线（`1—2—3—…—n`），  
再加上一条“快捷通道”把编号为 `x` 的房子和编号为 `y` 的房子直接相连。

> **类比**：如果把每个房子看成字典里的词，普通道路就是词之间的顺序关系，  
> 快捷通道就像在字典里额外加了一个“同义词”条目，查词时可以直接跳过去。

最直接的想法是 **枚举所有有序对** `(i, j)`（`1 ≤ i, j ≤ n`，`i ≠ j`），
分别计算它们之间的最短距离，然后把得到的距离统计到答案数组里。

最短距离有三条可能的路线：

1. 直接走直线：`|i - j|`  
2. 先走到 `x`，再走快捷通道到 `y`，最后走到 `j`：`|i - x| + 1 + |j - y|`  
3. 先走到 `y`，再走快捷通道到 `x`，最后走到 `j`：`|i - y| + 1 + |j - x|`

取这三条路径的最小值就是两房子之间的最短街道数。

#### 代码（Python）

```python
def countPairs_bruteforce(n: int, x: int, y: int):
    # 结果使用 1-indexed，result[k] 表示距离恰好为 k 的有序对数
    result = [0] * (n + 1)          # 0 号位暂时不用

    for i in range(1, n + 1):      # 枚举左端点
        for j in range(1, n + 1):  # 枚举右端点（有序对，所以不排除 i==j）
            if i == j:
                continue           # 同一个房子距离为 0，不计入答案

            # 三条可能的路径长度
            direct = abs(i - j)
            via_xy = abs(i - x) + 1 + abs(j - y)
            via_yx = abs(i - y) + 1 + abs(j - x)

            dist = min(direct, via_xy, via_yx)   # 取最小值
            result[dist] += 1                    # 统计到对应距离

    return result[1:]   # 去掉下标 0，返回长度为 n 的列表
```

> **关键注释**  
> - `abs(i - x)`：从 `i` 到 `x` 需要经过多少条普通街道。  
> - `+ 1`：表示那条额外的快捷通道本身算作一条街道。  
> - `result[dist] += 1`：因为是有序对，`(i, j)` 与 `(j, i)` 会分别被统计。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  需要遍历所有 `n × n` 对房子（实际上是 `n·(n‑1)`，数量级相同），每对做常数次计算。  
  “`O(n²)`” 可以想象成在一个 `n` 行 `n` 列的表格里逐格检查，随着 `n` 增大，工作量会呈二次增长，`n=10⁵` 时根本不可接受。

- **空间复杂度**：`O(n)`  
  只需要存放答案数组 `result`（长度 `n+1`），其余都是常数级别的临时变量。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历所有 `n²` 对**。  
我们要利用题目给出的 **结构化信息** 来一次性算出所有距离的统计。

---

#### 2.1 先算“没有快捷通道”时的基准答案  

如果城市只有普通直线道路，那么两房子之间的最短距离就是它们的编号差 `|i‑j|`。  
对每个可能的距离 `d (1 ≤ d ≤ n‑1)`，有：

- 左端点可以取 `1 … n‑d`（共 `n‑d` 种），右端点只能是左端点右边恰好 `d` 的房子。  
- 因为是**有序对**，左端点在前、右端点在后两种顺序都算，所以数量是 `2·(n‑d)`。

于是我们可以直接得到一个 **基准数组** `base[d] = 2·(n‑d)`（`d` 从 `1` 到 `n`，`base[n]=0`）。

> **类比**：把所有房子排成一排，距离 `d` 的配对就像在这排中挑出相隔 `d` 的相邻两个人，左边的人可以站在第 `1` 位到第 `n‑d` 位，右边的人自然被决定了。因为我们区分先后顺序，所以每种站法算两次。

---

#### 2.2 哪些对会因为快捷通道而 “走更短”？

只要一对房子 **跨过** 快捷通道的两端（即左端点在 `x` 左侧，右端点在 `y` 右侧），走 `x—y` 这条边就能省掉若干条普通街道。  

设 `x ≤ y`（若 `x > y` 先交换），记左端点为 `i`，右端点为 `j`（`i < j`）：

- **直接走直线** 的距离是 `j - i`。
- **走快捷通道** 的距离（只考虑 `i ≤ x`、`j ≥ y` 的情况）为  
  `distVia = (x - i) + 1 + (j - y) = (j) + (x - i - y + 1)`  

  这里 `x - i - y + 1` 是一个 **常数**（对固定的 `i`），所以 `distVia` 随 `j` 线性增长，且每向右走一步，距离也 +1。

**何时会更短？**  
比较 `distVia` 与 `j - i`：

```
(j) + (x - i - y + 1)  <  j - i
=>  x - i - y + 1  <  -i
=>  x - y + 1  <  0
=>  y > x + 1
```

只要 `y` 与 `x` 之间间隔至少两条普通街道（`y ≥ x+2`），**所有**满足 `i ≤ x` 且 `j ≥ y` 的配对都会因为快捷通道而走更短。  
如果 `y = x+1`，两端相邻，快捷通道等价于普通街道，距离不会变短。

> **结论**：  
> - 当 `i ≤ x` 且 `j ≥ y`（跨过两端）时，最短距离一定是 `distVia`（如果 `y > x+1`）。  
> - 其他情况（两端在同一侧或 `i` 在 `x` 与 `y` 之间）**不会**因为快捷通道而缩短距离。

因此我们只需要统计 **跨区间的有序对**，把它们原本算到 `base[j-i]` 的计数搬到 `distVia` 对应的距离上。

---

#### 2.3 用前缀和（差分数组）一次性完成搬移  

对固定的左端点 `i`（`i ≤ x`），右端点的合法区间是 `[y, n]`。  
对每个 `j`：

- 原始距离 `d₁ = j - i`（在 `base` 中已经计数）。
- 新的最短距离 `d₂ = j + offset`，其中 `offset = x - i - y + 1`（常数）。

把 `i` 固定后，`d₁` 与 `d₂` 随 `j` 都是 **等差数列**，所以它们在距离轴上形成 **连续的区间**：

```
d₁ ∈ [y - i , n - i]
d₂ ∈ [y + offset , n + offset]
```

我们只要把区间 `[y - i , n - i]` 对应的计数 **减 1**（因为这部分不再是最短距离），
再把区间 `[y + offset , n + offset]` 对应的计数 **加 1**。

对所有满足 `i ≤ x` 的左端点重复上述操作，即可得到最终答案。

**如何高效地“区间加/减 1”**？

- 使用 **差分数组**（difference array）`diff`，对区间 `[L, R]` 执行 `diff[L] += 1, diff[R+1] -= 1`，随后一次前缀和即可得到每个距离的增量。  
- 同理，对 “减 1” 的区间也用差分数组 `sub`（或者直接在 `base` 上做前缀差分）。

整个过程只遍历一次 `i = 1 … n`，每次做 **常数次**的差分操作，时间 `O(n)`，空间 `O(n)`。

---

#### 2.4 完整算法步骤

1. **保证 `x ≤ y`**（若不满足则交换）。  
2. **初始化基准答案** `ans[d] = 2·(n‑d)`（`d = 1 … n`），`ans[0]` 暂时不使用。  
3. **准备两个差分数组**  
   - `add`：记录 “因为快捷通道而新增的计数”。  
   - `sub`：记录 “因为快捷通道而要删除的计数”。（也可以直接在 `ans` 上做前缀差分，这里为了思路清晰分开写）  
4. **遍历左端点 `i = 1 … n`**  
   - 若 `i > x` 且 `i < y`，仍然会跨过两端（只要右端点 `j ≥ y`），此时 `offset = i - x + 1 - y`。  
   - 若 `i ≤ x`，`offset = x - i - y + 1`。  
   - 若 `i ≥ y`，左端点在右侧，**不可能跨过两端**，直接 `continue`。  
   - 设右端点合法区间 `[L, R] = [y, n]`（因为 `j` 必须大于 `i`，但 `y` 本身已经 ≥ `i+1`，所以直接取 `[y, n]`）。  
   - 计算 **要减的区间** `subL = L - i`, `subR = R - i`（直接距离）。  
   - 计算 **要加的区间** `addL = L + offset`, `addR = R + offset`（走快捷通道的距离）。  
   - 把区间截到合法范围 `[1, n]`（因为答案数组只到 `n`）。  
   - 对 `sub` 做差分 `sub[subL] -= 1, sub[subR+1] += 1`。  
   - 对 `add` 做差分 `add[addL] += 1, add[addR+1] -= 1`。  
5. **把差分数组转成真实增量**（一次前缀和）。  
6. **把基准答案 `ans` 与增量相加**，得到最终答案。  
7. **返回** `ans[1:]`（去掉下标 0），即长度为 `n` 的 1‑indexed 结果。

---

#### 代码（Python）

```python
def countPairs(n: int, x: int, y: int):
    """
    返回长度为 n 的列表 result，result[k-1] 表示最短距离恰好为 k 的有序房屋对数。
    时间复杂度 O(n)，空间复杂度 O(n)。
    """
    # 1. 保证 x <= y，方便统一讨论
    if x > y:
        x, y = y, x

    # 2. 基准答案（没有快捷通道时的计数）
    ans = [0] * (n + 1)               # ans[0] 暂时不使用
    for d in range(1, n + 1):
        ans[d] = 2 * (n - d)           # 2·(n‑d) 对应距离 d

    # 3. 差分数组，分别记录“加”和“减”
    add = [0] * (n + 2)                # 加的差分
    sub = [0] * (n + 2)                # 减的差分

    # 4. 枚举左端点 i
    for i in range(1, n + 1):
        # 只关心能够跨过两端的情况
        if i >= y:                     # 左端点已经在右侧，无法跨过
            continue

        # 右端点必须在 y 右边（因为 j > i，且要跨过 y）
        L, R = y, n                    # 右端点的合法区间

        # 计算 offset，使得走快捷通道的距离 = j + offset
        if i <= x:                     # i 在 x 左侧
            offset = x - i - y + 1
        else:                          # x < i < y
            offset = i - x + 1 - y

        # ----- 直接距离的区间（需要减 1） -----
        subL = L - i
        subR = R - i
        # 直接距离一定在 [1, n]，但仍做一次安全截断
        subL = max(subL, 1)
        subR = min(subR, n)
        if subL <= subR:
            sub[subL]     -= 1
            sub[subR + 1] += 1

        # ----- 走快捷通道的距离区间（需要加 1） -----
        addL = L + offset
        addR = R + offset
        addL = max(addL, 1)
        addR = min(addR, n)
        if addL <= addR:
            add[addL]     += 1
            add[addR + 1] -= 1

    # 5. 把差分数组转成实际增量
    cur = 0
    for d in range(1, n + 1):
        cur += add[d]
        ans[d] += cur                     # 加上因快捷通道产生的新增计数

    cur = 0
    for d in range(1, n + 1):
        cur += sub[d]
        ans[d] += cur                     # 减去被快捷通道取代的计数

    # 6. 返回 1-indexed 结果（去掉下标 0）
    return ans[1:]
```

> **代码要点解释**  
> - `offset` 为一个只跟左端点 `i` 相关的常数，代表“走快捷通道后相比直接距离整体向左（或向右）平移了多少”。  
> - `add` 与 `sub` 分别是 “把这段距离的计数加 1” 与 “把这段距离的计数减 1”。使用差分后，只需要 **O(1)** 时间更新整个区间。  
> - 最后两次前缀和把差分恢复为每个具体距离的增量，然后统一加到基准答案 `ans` 上。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次左端点 `i`（`n` 次），每次做常数次差分操作，再进行两次长度为 `n` 的前缀和。  
  与 `n` 成线性关系，即使 `n = 10⁵` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  需要存放基准答案 `ans`、两个差分数组 `add`、`sub`，均为长度 `n+2` 的列表。  

---

## 心得

- **核心技巧**：  
  1. **先算基准**（没有额外边时的答案），再只处理会被“快捷通道”影响的配对。  
  2. **区间差分 + 前缀和**：把大量“把某段距离的计数 +1 / -1”压缩成 O(1) 操作。  

- **适用的题型**（类似思路）  
  1. “在一维数组/序列上加一条跨区间的特殊边”导致距离变化的题目。  
  2. “统计所有满足某种区间关系的配对数量”，如 “子数组和为 k” 的计数可用前缀和+哈希表。  

- **一句话总结解题钥匙**：  
  “先算全局通用的答案，再用差分技巧把少数被特殊结构改变的配对‘搬家’”。  

---

## 反思

- **拿到题目第一反应**：  
  直接想到两层循环遍历所有房子对，算最短路径——也就是暴力解。  

- **最容易踩的坑**  
  1. **忘记有序对**：`(i, j)` 与 `(j, i)` 必须分别计数，两倍的计数常被遗漏。  
  2. **边界条件**：`x == y` 时快捷通道退化为自环，实际上不改变任何距离；代码里要能自然处理（本算法通过 `offset` 自动得到 0 区间，等价于不变）。  
  3. **区间截断**：差分更新时要把区间限制在 `[1, n]`，否则会产生数组越界或错误的计数。  

- **下次遇到同类题的第一步**：  
  “先写出没有特殊边/约束的通用答案”，然后再思考**哪些配对会被特殊结构影响**，用**区间差分**或**前缀和**把这些配对的计数迁移过去。这样即可把二次循环降到线性时间。