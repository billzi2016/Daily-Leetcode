# #799. 香槟塔 / Champagne Tower

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/champagne-tower/)

---

## 题目（英文原版）

**Description**

We stack glasses in a pyramid, where the first row has 1 glass, the second row has 2 glasses, and so on until the 100th row.  Each glass holds one cup of champagne.
Then, some champagne is poured into the first glass at the top.  When the topmost glass is full, any excess liquid poured will fall equally to the glass immediately to the left and right of it.  When those glasses become full, any excess champagne will fall equally to the left and right of those glasses, and so on.  (A glass at the bottom row has its excess champagne fall on the floor.)
For example, after one cup of champagne is poured, the top most glass is full.  After two cups of champagne are poured, the two glasses on the second row are half full.  After three cups of champagne are poured, those two cups become full - there are 3 full glasses total now.  After four cups of champagne are poured, the third row has the middle glass half full, and the two outside glasses are a quarter full, as pictured below.
Now after pouring some non-negative integer cups of champagne, return how full the jth glass in the ith row is (both i and j are 0-indexed.)

**Examples**

**Example 1:**

```
Input: poured = 1, query_row = 1, query_glass = 1
Output: 0.00000
Explanation: We poured 1 cup of champange to the top glass of the tower (which is indexed as (0, 0)). There will be no excess liquid so all the glasses under the top glass will remain empty.
```

**Example 2:**

```
Input: poured = 2, query_row = 1, query_glass = 1
Output: 0.50000
Explanation: We poured 2 cups of champange to the top glass of the tower (which is indexed as (0, 0)). There is one cup of excess liquid. The glass indexed as (1, 0) and the glass indexed as (1, 1) will share the excess liquid equally, and each will get half cup of champange.
```

**Example 3:**

```
Input: poured = 100000009, query_row = 33, query_glass = 17
Output: 1.00000
```

**Constraints**

- 0 <= poured <= 109
- 0 <= query_glass <= query_row < 100

---

## 题目（中文翻译）

我们把玻璃杯（glass）按金字塔形堆叠，第一层有 1 个杯子，第二层有 2 个杯子，依此类推，直到第 100 层。每个杯子容量为 1 杯香槟。  
随后，将一定量的香槟倒入最上层的第一个杯子。当顶部的杯子被装满后，任何多余的液体会等量流向它左侧和右侧的两个杯子。当这些杯子也被装满后，剩余的香槟同样会等量流向它们左右两侧的杯子，依此类推。（底层的杯子如果有多余的香槟，则会流到地面上。）  

例如，倒入 1 杯香槟后，最上面的杯子恰好装满。倒入 2 杯香槟后，第二层的两个杯子各装满一半。倒入 3 杯香槟后，这两个杯子也被装满——此时共有 3 个满杯。倒入 4 杯香槟后，第三层的中间杯子装满一半，左右两侧的杯子各装满四分之一，如下图所示。  

现在，给定倒入的香槟杯数（非负整数），返回第 `i` 行第 `j` 个杯子（`i`、`j` 均为 0 索引）的填充程度。

### 示例

#### 示例 1
``` 
Input: poured = 1, query_row = 1, query_glass = 1
Output: 0.00000
Explanation: 我们向塔顶的杯子 (0, 0) 倒入 1 杯香槟。没有多余的液体，所以顶层以下的所有杯子都保持为空。
```

#### 示例 2
``` 
Input: poured = 2, query_row = 1, query_glass = 1
Output: 0.50000
Explanation: 我们向塔顶的杯子 (0, 0) 倒入 2 杯香槟。产生了 1 杯的多余液体。索引为 (1, 0) 和 (1, 1) 的两个杯子平分这部分液体，各得到半杯香槟。
```

#### 示例 3
``` 
Input: poured = 100000009, query_row = 33, query_glass = 17
Output: 1.00000
```

### 约束条件
- `0 <= poured <= 10^9`
- `0 <= query_glass <= query_row < 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **一杯一杯地倒**，每倒一杯就让酒从上往下“滴流”一次。  
可以把整个塔想象成一张二维表，每个格子代表一只酒杯。  

* **倒酒**：把 1 加到最上面的杯子 `(0,0)`。  
* **流动**：从上往下遍历每一行，若某个杯子里的酒量 `> 1`（已经装满），则把多余的 `excess = amount - 1` 平分给左下角和右下角的两个杯子。  
* **重复**：把上述过程重复 `poured` 次（即倒了多少杯，就执行多少次）。

> **类比**：这就像在厨房里手动把一大勺糖倒进一个金字塔形的容器，每次只倒一小勺，然后等糖自然流向下层的两个小碗。  

这个方法**一定能得到正确答案**，因为我们严格模拟了题目描述的每一步：  
1. 只在顶层倒酒。  
2. 只有当杯子装满后才会把多余的酒向下分配。  
3. 分配是均匀的（左、右各一半）。  

只要把所有倒入的酒都走完，最终每个杯子里的量就和题目要求一致。

#### 代码（Python）

```python
def champagneTower_bruteforce(poured: int, query_row: int, query_glass: int) -> float:
    # ① 建立 101 行的塔（题目最多到第 99 行，多建一行防止越界）
    tower = [[0.0] * (i + 1) for i in range(101)]

    # ② 一杯一杯倒
    for _ in range(poured):
        tower[0][0] += 1.0                 # 把 1 杯酒倒进最顶层

        # ③ 从上到下把溢出的酒往下传
        for r in range(100):               # 只需要遍历到第 100 行（第 99 行是最后可能会溢出的行）
            for c in range(r + 1):
                if tower[r][c] > 1.0:       # 这只杯子已经装满
                    excess = tower[r][c] - 1.0   # 多余的酒
                    tower[r][c] = 1.0            # 保留满杯的 1
                    # 把多余的均分给左下和右下的两只杯子
                    tower[r + 1][c]     += excess / 2.0
                    tower[r + 1][c + 1] += excess / 2.0

    # ④ 直接返回查询的那只杯子的酒量（已保证在 0~1 之间）
    return tower[query_row][query_glass]
```

> **关键行中文注释**已经写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(poured × rows²)`  
  - `poured` 是倒的杯数，最多 `10⁹`，而每一次都要遍历至第 `100` 行（`rows ≈ 100`），所以最坏情况下是 `10⁹ × 10⁴`，几乎不可接受。  
  - 用大白话说，就是“倒多少杯就要跑多少遍”，如果倒了很多杯，程序会卡死。

- **空间复杂度**：`O(rows²)` ≈ `O(100²)` ≈ `10⁴`  
  - 只用了一个 101×101 的二维数组来存放每只杯子的酒量，大小是固定的，和 `poured` 没关系。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于“每倒一杯都要重新遍历整个塔”。  
实际上，**酒的流动只和总倒入量有关**，不需要逐杯模拟。  

我们可以一次性把所有酒倒进去，然后一次遍历塔，**把每只杯子里多余的酒一次性向下分配**。  
这正是**动态规划（DP）**的思想：  
- `dp[i][j]` 表示第 `i` 行第 `j` 列的杯子**最终**会收到多少酒（可能超过 1，表示有溢出）。  
- 初始时只有顶杯收到 `poured` 杯：`dp[0][0] = poured`。  
- 对每只杯子 `dp[i][j]`：  
  - 若 `dp[i][j] > 1`，说明有 `excess = dp[i][j] - 1` 需要向下流。  
  - 这 `excess` 均分给左下 `(i+1, j)` 与右下 `(i+1, j+1)`。  
  - 若 `dp[i][j] ≤ 1`，则没有溢出，直接保留。  

遍历顺序必须是**从上到下、从左到右**，因为下层的酒量依赖上层的溢出。  

> **类比**：想象把一大桶水一次性倒进金字塔形的容器，水会顺着重力“自动”往下渗。我们只需要一次性算出每层会渗出多少，而不必每滴水都单独跟踪。

**为什么只需要遍历到查询的行**？  
因为题目只关心第 `query_row` 行的某只杯子，行以下的酒量对答案没有影响。于是我们可以在遍历到 `query_row` 时停止，进一步省时。

#### 代码（Python）

```python
def champagneTower(poured: int, query_row: int, query_glass: int) -> float:
    """
    动态规划一次性模拟所有酒的流动。
    返回第 query_row 行第 query_glass 列的酒量（0~1 之间的浮点数）。
    """
    # ① 创建一个足够大的 DP 表（只需要 query_row + 2 行即可，防止越界）
    dp = [[0.0] * (i + 1) for i in range(query_row + 2)]

    # ② 顶部一次性倒入全部酒
    dp[0][0] = float(poured)

    # ③ 从上到下遍历，向下分配溢出
    for i in range(query_row + 1):          # 只遍历到 query_row 行（含）
        for j in range(i + 1):
            if dp[i][j] > 1.0:              # 有溢出
                excess = dp[i][j] - 1.0     # 多余的酒
                dp[i][j] = 1.0              # 该杯子最多装满 1 杯
                # 均分给左下、右下两杯
                dp[i + 1][j]     += excess / 2.0
                dp[i + 1][j + 1] += excess / 2.0
            # 如果 dp[i][j] ≤ 1，直接保留，不会向下流

    # ④ 结果可能大于 1（因为我们只在遍历时把 >1 的情况截为 1），
    #    但查询的杯子已经在遍历结束时被裁剪过，直接返回即可
    return min(1.0, dp[query_row][query_glass])
```

> 代码中每一步都有中文注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(query_row²)`  
  - 只遍历到第 `query_row` 行，每行最多 `i+1` 个杯子，总操作数约为 `1 + 2 + … + (query_row+1) = O(query_row²)`。  
  - 对于最大 `query_row = 99`，最多只有约 `5,000` 次循环，几乎瞬间完成。  
  - 用大白话说，就是“只跑一次塔，跑的行数不超过 100”，所以非常快。

- **空间复杂度**：`O(query_row²)`（同样是二维表的大小）  
  - 只需要存储到第 `query_row+1` 行的数据，最多约 `5,000` 个浮点数，几乎不占内存。  

与暴力解相比，**时间从 `poured × rows²` 降到了 `rows²`**，把原本可能的 `10⁹` 次循环砍掉，瞬间变成了常数级别。

---

## 心得  

- **核心技巧**：一次性把所有酒倒入顶层，再用**自上而下的动态规划**把溢出均分到下层。  
- **适用的题型**：  
  1. **金字塔/三角形分配** 类问题（如 LeetCode 1199 “Minimum Total Cost to Hire K Workers” 中的 DP 递推）。  
  2. **水流/雨水分配** 类题目（如 LeetCode 404 “Sum of Left Leaves” 的递归分配思路）。  
  3. **层级累计**（例如 LeetCode 746 “Min Cost Climbing Stairs” 的 DP 递推）。  
- **一句话总结解题钥匙**：**“把所有资源一次性放进顶点，然后自上而下把多余的均分下去”。**

---

## 反思  

- **第一反应**：把酒一杯一杯倒，模拟每一次的流动。虽然思路直接，但忽略了 `poured` 可能非常大。  
- **最容易踩的坑**：  
  - **边界**：第 `query_row` 行的右侧杯子在数组中是 `j = query_row`，必须保证 DP 表有足够的列（`i+1` 列）。  
  - **溢出裁剪**：`dp[i][j]` 可能大于 `1`，返回时必须 `min(1, value)`，否则答案会超过 1。  
  - **精度**：使用浮点数时要注意 `0.999999` 与 `1.0` 的比较，`min` 可以直接解决。  
- **下次类似题的第一步**：先思考 **“一次性把所有资源放进去，然后一次遍历把多余的向下/向右分配”**，这往往能把暴力的多次循环压缩成一次 DP。