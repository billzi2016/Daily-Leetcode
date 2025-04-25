# #3160. 统计球中不同颜色的数量 / Find the Number of Distinct Colors Among the Balls

> 难度：中等 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-distinct-colors-among-the-balls/)

---

## 题目（英文原版）

**Description**

You are given an integer limit and a 2D array queries of size n x 2.
There are limit + 1 balls with distinct labels in the range [0, limit]. Initially, all balls are uncolored. For every query in queries that is of the form [x, y], you mark ball x with the color y. After each query, you need to find the number of colors among the balls.
Return an array result of length n, where result[i] denotes the number of colors after ith query.
Note that when answering a query, lack of a color will not be considered as a color.

**Examples**

**Example 1:**

```
Input: limit = 4, queries = [[1,4],[2,5],[1,3],[3,4]]
Output: [1,2,2,3]
Explanation:
```

**Example 2:**

```
Input: limit = 4, queries = [[0,1],[1,2],[2,2],[3,4],[4,5]]
Output: [1,2,2,3,4]
Explanation:
```

**Constraints**

- 1 <= limit <= 109
- 1 <= n == queries.length <= 105
- queries[i].length == 2
- 0 <= queries[i][0] <= limit
- 1 <= queries[i][1] <= 109

---

## 题目（中文翻译）

给定一个整数 `limit（limit）` 和一个大小为 `n × 2` 的二维数组 `queries（queries）`。  
共有 `limit + 1` 个球，它们的标签唯一，范围为 `[0, limit]`。初始时，所有球都未着色。对于 `queries` 中的每个查询 `[x, y]`，将标签为 `x` 的球染上颜色 `y（color）`。在每次查询之后，需要统计当前所有球中出现的不同颜色的数量。

返回一个长度为 `n` 的数组 `result（result）`，其中 `result[i]` 表示第 `i` 次查询之后的不同颜色数量。  
注意：在回答查询时，**未出现的颜色不计入颜色数量**。

## 示例

### 示例 1
**输入**  
`limit = 4, queries = [[1,4],[2,5],[1,3],[3,4]]`

**输出**  
`[1,2,2,3]`

**解释**  
- 第一次查询后，球 1 被染成颜色 4，当前颜色集合为 `{4}`，数量为 1。  
- 第二次查询后，球 2 被染成颜色 5，颜色集合为 `{4,5}`，数量为 2。  
- 第三次查询后，球 1 的颜色被改为 3，颜色集合为 `{3,5}`，数量仍为 2。  
- 第四次查询后，球 3 被染成颜色 4，颜色集合为 `{3,4,5}`，数量为 3。

### 示例 2
**输入**  
`limit = 4, queries = [[0,1],[1,2],[2,2],[3,4],[4,5]]`

**输出**  
`[1,2,2,3,4]`

**解释**  
- 第一次查询后，颜色集合为 `{1}`，数量为 1。  
- 第二次查询后，颜色集合为 `{1,2}`，数量为 2。  
- 第三次查询后，球 2 的颜色仍为 2，颜色集合不变，数量仍为 2。  
- 第四次查询后，颜色集合为 `{1,2,4}`，数量为 3。  
- 第五次查询后，颜色集合为 `{1,2,4,5}`，数量为 4。

## 约束条件
- `1 <= limit <= 10^9`
- `1 <= n == queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= queries[i][0] <= limit`
- `1 <= queries[i][1] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
1. 用一个字典 `ball2color` 记录每个球当前的颜色（键是球的编号，值是颜色）。  
2. 每收到一条查询 `[x, y]`，把 `ball2color[x]` 更新为 `y`。  
3. **随后**遍历 `ball2color` 中所有已经上色的球，把它们的颜色放进一个集合 `set`（集合天然去重），集合的大小就是当前的不同颜色数。  

> **类比**：  
> - **哈希表**（这里的 `ball2color`）就像一本“球-颜色”字典，想查某个球的颜色只要翻到对应的页码就能立刻得到。  
> - **集合**（`set`）像是“颜色手册”，每次看到一种颜色就把它记进去，重复的颜色自然不会再占位置。  

**为什么正确**：  
- 每一次查询我们都把最新的颜色写进 `ball2color`，所以字典里始终保存的是“每个球最新的颜色”。  
- 把所有颜色收集到集合里再计数，恰好等于“当前出现的不同颜色数”。  

#### 代码（Python）  

```python
def distinctColors_bruteforce(limit: int, queries: list[list[int]]) -> list[int]:
    # ball2color: ball 编号 -> 颜色（只记录已经上色的球）
    ball2color: dict[int, int] = {}
    ans: list[int] = []

    for x, y in queries:
        # ① 把球 x 标记为颜色 y（覆盖旧颜色）
        ball2color[x] = y

        # ② 收集所有出现的颜色
        colors: set[int] = set()
        for col in ball2color.values():
            colors.add(col)          # 集合会自动去重

        # ③ 当前不同颜色的数量就是集合的大小
        ans.append(len(colors))

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（`n` 为查询数量）  
  - 每条查询我们都要遍历一次 `ball2color`（最坏情况下会有 `n` 个已上色的球），于是总操作数约为 `1 + 2 + … + n = n·(n+1)/2`，用大写的 **O(n²)** 表示。  
  - 用生活化的语言说，就是“随着查询次数的增加，花的时间会像平方一样快地增长”。  

- **空间复杂度**：`O(n)`  
  - 最多会记录 `n` 条 `ball → color` 的映射，和集合里最多 `n` 种颜色，都是线性空间。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历所有已上色的球来统计颜色**。  
我们其实可以在 **更新颜色的同时**，直接维护每种颜色当前出现了多少个球，这样就不需要再遍历了。

**核心数据结构**  

1. `ball2color`（哈希表）：记录每个球最新的颜色。  
2. `color_cnt`（哈希表）：记录每种颜色当前被多少个球使用。  
   - 键：颜色  
   - 值：使用该颜色的球的数量  

**更新步骤**（对每条查询 `[x, y]`）  

1. **如果球 x 之前已经有颜色**（`old = ball2color.get(x)`）  
   - 把 `color_cnt[old]` 减 1。  
   - 若减后等于 0，说明这种颜色已经不再出现，直接把它从 `color_cnt` 中删掉。  
2. **把新颜色写进去**  
   - `ball2color[x] = y`  
   - 把 `color_cnt[y]` 加 1（如果之前不存在就创建并设为 1）。  
3. 当前不同颜色的数量就是 `len(color_cnt)`，直接加入答案。  

> **类比**：  
> - `color_cnt` 像是一张“颜色库存表”，每种颜色对应的数字告诉我们还有多少件商品在仓库里。只要库存为 0，就把这行删掉，表格的行数就是我们想要的“在库的不同颜色种类”。  

这样每条查询只涉及 **常数次** 哈希表的查找/插入/删除，时间复杂度降到 `O(1)`，整体 `O(n)`。

#### 代码（Python）  

```python
def distinctColors(limit: int, queries: list[list[int]]) -> list[int]:
    """
    返回每次查询后，不同颜色的数量。
    只使用哈希表，能够处理 limit 达到 1e9、queries 长度 1e5 的情况。
    """
    ball2color: dict[int, int] = {}   # 球 -> 当前颜色
    color_cnt: dict[int, int] = {}    # 颜色 -> 使用该颜色的球的数量
    ans: list[int] = []

    for x, y in queries:
        # ---------- 1. 处理旧颜色 ----------
        old = ball2color.get(x)       # 可能是 None（表示球之前未上色）
        if old is not None:
            # 旧颜色的计数减 1
            color_cnt[old] -= 1
            if color_cnt[old] == 0:   # 没有球再用该颜色，删除键以保持统计正确
                del color_cnt[old]

        # ---------- 2. 写入新颜色 ----------
        ball2color[x] = y
        color_cnt[y] = color_cnt.get(y, 0) + 1   # 若不存在则默认 0 再加 1

        # ---------- 3. 当前不同颜色数量 ----------
        ans.append(len(color_cnt))

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每条查询只做了几次哈希表的 `get / set / del`，这些操作在平均情况下都是 **常数时间**，所以总耗时随查询数线性增长。  
  - 与暴力解的 `O(n²)` 相比，提升了一个量级：原来查询 10⁵ 次会花上 **约 5·10⁹** 次基本操作，而现在只需要 **约 10⁵** 次。  

- **空间复杂度**：`O(n)`  
  - 最多会记录 `n` 条球‑颜色映射和 `n` 条颜色‑计数（实际颜色种类不可能超过查询数），仍然是线性空间。  

---  

## 心得  

- **核心技巧**：**双哈希表维护“对象 → 属性”和“属性 → 出现次数”**，从而在每次更新时即时得到不同属性的种类数。  
- **适用的题型**（类似思路）  
  1. **统计数组中不同元素的个数，且支持增删改**（如 LeetCode 1690. Majority Element）。  
  2. **滑动窗口内不重复字符的最长子串**（使用字符 → 计数 哈希表）。  
  3. **在线查询区间不同值的数量**（可以用离线 + BIT/线段树 + 哈希表实现）。  
- **一句话总结**：**“把‘出现次数’也记下来，就能在 O(1) 内知道还有多少种颜色”。**  

---  

## 反思  

- **拿到题目第一反应**：先用字典记录每个球的颜色，然后每次遍历一遍取集合计数——最直接的“暴力”实现。  
- **最容易踩的坑**  
  1. **忘记删除计数为 0 的颜色**，导致 `len(color_cnt)` 包含已经不存在的颜色，答案偏大。  
  2. **没有区分“未上色”和“颜色为 0”**（题目颜色都是正数），所以 `ball2color.get(x)` 返回 `None` 时要特别判断。  
  3. **空间泄漏**：如果只把计数减 1而不删除键，哈希表会一直增长，虽然不影响正确性，但会浪费内存。  
- **下次遇到同类题**，第一步应该想到：**“我需要快速知道每种属性的出现次数”，于是直接准备一个计数哈希表来同步维护。**