# #2201. 可提取的文物计数 / Count Artifacts That Can Be Extracted

> 难度：中等 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-artifacts-that-can-be-extracted/)

---

## 题目（英文原版）

**Description**

There is an n x n 0-indexed grid with some artifacts buried in it. You are given the integer n and a 0-indexed 2D integer array artifacts describing the positions of the rectangular artifacts where artifacts[i] = [r1i, c1i, r2i, c2i] denotes that the ith artifact is buried in the subgrid where:
You will excavate some cells of the grid and remove all the mud from them. If the cell has a part of an artifact buried underneath, it will be uncovered. If all the parts of an artifact are uncovered, you can extract it.
Given a 0-indexed 2D integer array dig where dig[i] = [ri, ci] indicates that you will excavate the cell (ri, ci), return the number of artifacts that you can extract.
The test cases are generated such that:

**Examples**

**Example 1:**

```
Input: n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1]]
Output: 1
Explanation: 
The different colors represent different artifacts. Excavated cells are labeled with a 'D' in the grid.
There is 1 artifact that can be extracted, namely the red artifact.
The blue artifact has one part in cell (1,1) which remains uncovered, so we cannot extract it.
Thus, we return 1.
```

**Example 2:**

```
Input: n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1],[1,1]]
Output: 2
Explanation: Both the red and blue artifacts have all parts uncovered (labeled with a 'D') and can be extracted, so we return 2.
```

**Constraints**

- 1 <= n <= 1000
- 1 <= artifacts.length, dig.length <= min(n2, 105)
- artifacts[i].length == 4
- dig[i].length == 2
- 0 <= r1i, c1i, r2i, c2i, ri, ci <= n - 1
- r1i <= r2i
- c1i <= c2i
- No two artifacts will overlap.
- The number of cells covered by an artifact is at most 4.
- The entries of dig are unique.

---

## 题目（中文翻译）

**题目描述**  
有一个 $n \times n$ 的 0 索引网格（grid），其中埋有若干文物（artifact）。给定整数 `n` 和一个 0 索引二维整数数组 `artifacts`，用于描述矩形文物的位置，其中 `artifacts[i] = [r1_i, c1_i, r2_i, c2_i]` 表示第 `i` 件文物埋在子网格（subgrid） `r1_i .. r2_i` 行、`c1_i .. c2_i` 列（均为闭区间）中。

你将挖掘网格中的若干单元格，并把这些单元格中的泥土全部清除。如果该单元格下方有文物的一部分，则该部分会被揭露。**当且仅当文物的所有部分全部被揭露时，你才能将其提取出来。**

给定一个 0 索引二维整数数组 `dig`，其中 `dig[i] = [r_i, c_i]` 表示你将挖掘单元格 `(r_i, c_i)`。返回你能够提取的文物数量。

**示例**

```text
示例 1:
Input: n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1]]
Output: 1
Explanation: 
不同颜色代表不同的文物。被挖掘的单元格在网格中用字符 'D' 标记。
可以提取 1 件文物，即红色文物。
蓝色文物在单元格 (1,1) 还有未被揭露的部分，因此无法提取。
因此返回 1。
```

```text
示例 2:
Input: n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1],[1,1]]
Output: 2
Explanation: 红色和蓝色文物的所有部分均已被揭露（标记为 'D'），均可提取，故返回 2。
```

**约束条件**
- $1 \le n \le 1000$
- $1 \le \text{artifacts.length}, \text{dig.length} \le \min(n^2, 10^5)$
- `artifacts[i].length == 4`
- `dig[i].length == 2`
- $0 \le r1_i, c1_i, r2_i, c2_i, r_i, c_i \le n - 1$
- $r1_i \le r2_i$
- $c1_i \le c2_i$
- 任意两件文物不会重叠。
- 单件文物覆盖的单元格数最多为 4。
- `dig` 中的条目互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每件文物**，把它所在的矩形里所有格子一个一个列举出来，然后**逐个去检查**这些格子是否在 `dig` 数组里出现过。  
- **数据结构**：  
  - `artifacts[i] = [r1, c1, r2, c2]` 描述的是一个子矩形，左上角 `(r1, c1)`、右下角 `(r2, c2)`。  
  - `dig` 是我们挖掘的格子列表。可以把它想象成一本“挖掘日志”，每一行记录了我们在第几行第几列挖了一个洞。  
- **为什么正确**：只要文物的每一个格子都在日志里出现，说明它全部被挖开，根本就可以直接取走。反之，只要有一个格子没有被记录，就说明还有泥土盖着，这件文物不能提取。  
- **时间/空间分析（大白话）**：  
  - 暴力做法对每件文物的每个格子，都要在 `dig` 列表里**线性遍历**一次寻找匹配。  
  - 假设有 `A` 件文物，每件文物最多覆盖 `4` 个格子（题目已给出），`dig` 长度为 `D`。  
  - 那么总的比较次数大约是 `A * 4 * D`，这在最坏情况下相当于 `O(A·D)`，如果 `A`、`D` 都是上限（≈10⁵），就会非常慢。  
  - 空间上只用了原始输入的存储，没有额外的数组，空间复杂度是 `O(1)`（不计输入）。

#### 代码（Python）

```python
def digArtifacts_bruteforce(n, artifacts, dig):
    # 暴力：对每件文物的每个格子，都在 dig 列表里线性查找
    answer = 0

    for a in artifacts:
        r1, c1, r2, c2 = a
        all_dug = True                     # 假设这件文物全部被挖开

        # 枚举文物占据的每一个格子
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                found = False               # 这个格子是否在 dig 里出现
                for dr, dc in dig:          # 线性遍历 dig
                    if dr == r and dc == c:
                        found = True
                        break
                if not found:               # 只要有一个格子没被挖开，就退出
                    all_dug = False
                    break
            if not all_dug:
                break

        if all_dug:                         # 该文物全部被挖开，计数加一
            answer += 1

    return answer
```

#### 复杂度

- **时间复杂度**：`O(A·D)`（A 为文物数量，D 为挖掘次数），因为每检查一个格子都要遍历整个 `dig` 列表。  
  - 大白话：如果文物有 10 万件，挖掘次数也有 10 万次，程序要做 10⁴⁰ 次比较，根本跑不完。
- **空间复杂度**：`O(1)`（不计输入），只用了常数个临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次检查格子时，都要遍历整个 `dig` 列表寻找匹配。我们需要一种**快速判断**“某个格子是否已经被挖掘” 的办法。

**关键点**：  
- `dig` 中的每个坐标都是唯一的（题目已保证），我们可以把所有挖掘过的格子放进 **哈希表**（在 Python 中就是 `set`），这样“是否存在” 的查询可以在 **常数时间 O(1)** 完成。  
- 哈希表可以类比为“字典”，`key` 是格子坐标 `(r, c)`，`value`（这里我们只关心键是否在集合里）相当于页码。查找一个词在字典里是否有对应的页码，只需要一次快速定位。

**步骤**：

1. **构建集合** `dug = {(ri, ci) for each dig[i]}`，把所有挖掘坐标一次性放进去。  
2. 对每件文物，枚举它占据的格子（每件最多 4 格），检查这些格子是否全部在 `dug` 集合里。  
   - 如果全部在，说明这件文物可以提取，计数加一。  
   - 否则继续检查下一件文物。  

由于每件文物最多只有 4 个格子，整个过程的时间复杂度仅与文物数量成正比。

#### 代码（Python）

```python
def digArtifacts(n, artifacts, dig):
    """
    最优解：使用哈希集合快速判断格子是否被挖掘
    :param n: grid 的尺寸（实际不需要在算法里使用）
    :param artifacts: List[List[int]]，每件文物的左上、右下坐标
    :param dig: List[List[int]]，挖掘的坐标列表
    :return: 可提取的文物数量
    """
    # 1. 把所有挖掘的格子放进集合，查询 O(1)
    dug = set()
    for r, c in dig:
        dug.add((r, c))          # (r, c) 这个坐标已经被挖开

    answer = 0

    # 2. 检查每件文物的每个格子是否都在 dug 中
    for r1, c1, r2, c2 in artifacts:
        all_dug = True
        # 文物面积最多 4，直接双层循环即可
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if (r, c) not in dug:   # O(1) 判断
                    all_dug = False
                    break
            if not all_dug:
                break

        if all_dug:
            answer += 1

    return answer
```

#### 复杂度

- **时间复杂度**：`O(A + D)`  
  - `O(D)` 用来把 `dig` 坐标放进集合。  
  - `O(A * 4)`（即 `O(A)`） 用来检查每件文物的格子，因为每件文物最多 4 个格子。  
  - 与暴力解相比，省掉了 `·D` 的乘法因子，速度提升几个数量级。  
- **空间复杂度**：`O(D)`  
  - 需要额外存储所有挖掘格子的集合，最坏情况是把整个网格（最多 10⁵ 个格子）都放进去。  
  - 大白话：相当于把我们挖过的每个洞记在一本小本子里，查找时只需要翻到对应页码，省时省力。

---

## 心得

- **核心技巧**：使用哈希集合（`set`）实现“是否被挖掘” 的 **常数时间查询**。  
- **适用场景**：  
  1. “在若干坐标中快速判断是否出现”——例如 LeetCode 1903 *Largest Odd Number in String*（判断字符是否出现）  
  2. “元素唯一且查询频繁”——例如 1460 *Make Two Arrays Equal by Reversing Subarrays*（需要快速判断元素是否在集合中）  
  3. “空间坐标或键值的快速存在性检查”——例如 2003 *Smallest Missing Genetic Value in Each Subtree*（使用集合记录基因值）  
- **一句话总结**：**把所有已知信息预先放进哈希表，后续查询即可 O(1) 完成**，是“避免重复遍历”的万能钥匙。

---

## 反思

- **第一反应**：直接对每件文物的每个格子遍历 `dig`，把所有可能的格子都检查一遍。  
- **最容易踩的坑**：  
  - 忘记 **去重**：如果不把 `dig` 放进集合，而是每次线性搜索，时间会爆炸。  
  - **边界条件**：文物的矩形可能只占一个格子（`r1==r2` 且 `c1==c2`），循环仍需正常执行。  
  - **坐标存储**：使用 `(r, c)` 这种二元组作为键时，必须保证两者顺序一致，否则会出现 “找不到”。  
- **下次类似题的第一步**：先思考 **“我要快速判断某个元素是否出现”** 吗？如果是，立刻把所有出现的元素放进 **哈希集合 / 哈希表**，后续所有判断都可以 O(1) 完成。这样往往能把原本的 O(N·M) 降到 O(N+M)。