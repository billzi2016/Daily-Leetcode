# #765. 情侣牵手 / Couples Holding Hands

> 难度：困难 · 标签：Greedy、Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/couples-holding-hands/)

---

## 题目（英文原版）

**Description**

There are n couples sitting in 2n seats arranged in a row and want to hold hands.
The people and seats are represented by an integer array row where row[i] is the ID of the person sitting in the ith seat. The couples are numbered in order, the first couple being (0, 1), the second couple being (2, 3), and so on with the last couple being (2n - 2, 2n - 1).
Return the minimum number of swaps so that every couple is sitting side by side. A swap consists of choosing any two people, then they stand up and switch seats.

**Examples**

**Example 1:**

```
Input: row = [0,2,1,3]
Output: 1
Explanation: We only need to swap the second (row[1]) and third (row[2]) person.
```

**Example 2:**

```
Input: row = [3,2,0,1]
Output: 0
Explanation: All couples are already seated side by side.
```

**Constraints**

- 2n == row.length
- 2 <= n <= 30
- n is even.
- 0 <= row[i] < 2n
- All the elements of row are unique.

---

## 题目（中文翻译）

**描述**  
有 `n` 对情侣坐在一排的 `2n` 个座位上，想要牵手。人和座位用整数数组 `row` 表示，`row[i]` 是坐在第 `i` 个座位上的人的 ID。情侣按顺序编号，第一对是 `(0, 1)`，第二对是 `(2, 3)`，依此类推，最后一对是 `(2n - 2, 2n - 1)`。

返回最少的交换次数，使得每对情侣都相邻坐。一次交换指选择任意两个人，让他们站起并交换座位。

**示例**

示例 1  
``` 
Input: row = [0,2,1,3]
Output: 1
Explanation: We only need to swap the second (row[1]) and third (row[2]) person.
```  
解释：只需要交换第二个人 (`row[1]`) 和第三个人 (`row[2]`) 即可。

示例 2  
``` 
Input: row = [3,2,0,1]
Output: 0
Explanation: All couples are already seated side by side.
```  
解释：所有情侣已经相邻坐好，不需要交换。

**约束条件**  
- `2n == row.length`  
- `2 <= n <= 30`  
- `n` 为偶数。  
- `0 <= row[i] < 2n`  
- `row` 中的元素各不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把每一对情侣都拉到相邻的位置」。  
我们可以从左到右扫描座位：

1. 当前位置 `i`（一定是偶数，因为我们每次检查一对相邻座位 `i,i+1`）。  
2. 看坐在 `i` 的人是谁 `a = row[i]`，他的另一半应该是 `a ^ 1`（因为情侣编号是 `(0,1) , (2,3) , …`，相邻的两个数字只差 1，且奇偶相反，用异或 1 可以直接得到配偶）。  
3. 如果 `row[i+1]` 正好是 `a ^ 1`，说明这对已经坐在一起，继续往后。  
4. 否则我们要把 `a ^ 1` 换到 `i+1` 位置。于是遍历后面的座位，找到配偶所在的下标 `j`，把 `row[i+1]` 与 `row[j]` 交换。一次交换后，这一对情侣就坐在一起了。

这个过程虽然「贪心」但每次都要在剩余的 `O(n)` 个位置里寻找配偶，所以总体是 `O(n²)`。

> **生活化类比**：  
> 把每个人想象成一本书，书的封面上写着编号。我们想让每本书的「上下册」（配偶）摆在相邻的书架格子里。先把左边的格子检查好，如果右边不是对应的下册，就去整排书里找那本下册，然后把它搬到右边的格子——这相当于「把书搬来搬去」的过程。

#### 代码（Python）

```python
def min_swaps_couples(row):
    """
    暴力/贪心实现
    """
    n = len(row) // 2                # 夫妻对的数量
    swaps = 0                         # 记录交换次数

    # 把每个人所在座位的下标保存下来，后面找配偶时可 O(1) 查表
    # pos[x] = 当前编号为 x 的人坐在的座位下标
    pos = {person: i for i, person in enumerate(row)}

    for i in range(0, len(row), 2):   # 只检查偶数下标 i, i+1 这一对座位
        a = row[i]                    # 左边的人的编号
        b = a ^ 1                     # a 的配偶编号（异或 1）

        if row[i + 1] == b:          # 已经是配偶，什么也不做
            continue

        # 配偶不在右边，需要把配偶搬到 i+1
        j = pos[b]                    # 配偶所在的座位下标
        # 交换 row[i+1] 与 row[j]
        row[i + 1], row[j] = row[j], row[i + 1]

        # 更新 pos 表（因为两个人位置互换了）
        pos[row[j]] = j
        pos[row[i + 1]] = i + 1

        swaps += 1                    # 完成一次交换
    return swaps
```

> **关键行中文注释**  
> - `b = a ^ 1`：利用二进制异或，快速得到配偶编号。  
> - `pos = {person: i for i, person in enumerate(row)}`：相当于「字典查词典」，把人名映射到座位，后面找配偶时不需要遍历整个数组。  
> - `row[i + 1], row[j] = row[j], row[i + 1]`：一次 Python 式的「换座位」操作。

#### 复杂度  

- **时间复杂度：`O(n²)`**  
  - 外层循环遍历 `n` 对座位，最坏情况下每次都要在剩余的 `≈ n` 个位置里寻找配偶，形成 `n × n` 的搜索。  
  - 用大白话说，就是「你要把 30 对情侣全部排好，第一对可能要找 30 个人，第二对找 29 个人，……」于是总共要检查大约 `30×30/2 ≈ 450` 次。

- **空间复杂度：`O(n)`**  
  - 额外使用了一个字典 `pos` 保存每个人的座位，下标 `i` 与编号 `person` 的映射关系。除了输入数组之外，只需要线性额外空间。

---

### 2. 最优解

#### 思路  

上面的暴力解每次都要**线性搜索配偶**，这就是瓶颈。  
我们注意到：

- 座位是成对出现的（`[0,1] , [2,3] , …`），每对座位可以看成 **一张两人沙发**（couch）。  
- 每个人的配偶要么已经坐在同一张沙发上，要么坐在 **另一张沙发** 上。  
- 如果配偶不在同一张沙发，我们可以在这两张沙发之间画一条**无向边**，表示「这两张沙发里的人需要互相调换位置」。

把所有沙发看成图的 **节点**，配偶跨沙发的关系看成 **边**，则：

- 每条边把两个节点连在一起。  
- **一个连通块（connected component）** 表示若干张沙发相互交叉，需要通过交换才能把每对情侣都坐在同一张沙发。  
- 在一个连通块里，若有 `k` 张沙发（即 `k` 对座位），只要把其中的 `k-1` 条边「断开」就可以让每对情侣都坐好。换句话说，**每个连通块需要的最少交换次数 = 节点数 - 1**。

整个问题的答案就是所有连通块的需求之和：

```
total_swaps = Σ (size_of_component - 1) = total_couples - number_of_components
```

这正好可以用 **并查集（Union‑Find）** 高效实现：

1. 初始化 `n` 个集合，每个集合对应一张沙发（下标 `i // 2`）。  
2. 遍历座位数组 `row`，每次取一对相邻座位 `(i,i+1)`，它们所在的沙发编号分别是 `c1 = i // 2` 和 `c2 = i // 2`（其实是同一张沙发），但我们关心的是**这两个人的配偶分别坐在哪张沙发**。  
   - 设左边人的编号是 `a = row[i]`，配偶是 `a ^ 1`。我们在数组中找配偶的座位下标 `pos[a ^ 1]`，其所在的沙发是 `c2 = pos[a ^ 1] // 2`。  
   - 把 `c1` 与 `c2` 合并（union）。  
3. 完成遍历后，用并查集统计有多少不同的根（即连通块数）。  
4. 用公式 `answer = n - components` 得到最小交换次数。

> **类比**：  
> 把每张沙发想象成一个小岛，岛上已经有两个人。若两个人的配偶在不同的小岛上，就在这两座小岛之间搭一座桥。所有的桥形成若干连通的「桥群」。要让每对情侣住在同一座岛上，只需要把每个桥群里多余的桥拆掉——每拆掉一座桥就相当于一次「换座位」的操作。拆掉 `桥群大小-1` 座桥，就能把每座岛上只留下本该住在一起的情侣。

#### 代码（Python）

```python
class UnionFind:
    """并查集（带路径压缩的写法）"""
    def __init__(self, n):
        self.parent = list(range(n))   # 每个节点的根初始化为自己
        self.rank = [0] * n            # 用于按秩合并，保持树的高度低

    def find(self, x):
        # 递归找根并压缩路径
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 将两棵树合并成一棵
        rx, ry = self.find(x), self.find(y)
        if rx == ry:          # 已经在同一个集合里，没必要再合并
            return False
        # 按秩合并：高度小的挂到高度大的下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def min_swaps_couples_opt(row):
    """
    并查集最优解
    """
    n = len(row) // 2                     # 夫妻对数量，也等于沙发数
    uf = UnionFind(n)

    # 记录每个人当前坐在哪个座位，便于 O(1) 找配偶位置
    pos = {person: i for i, person in enumerate(row)}

    for i in range(0, len(row), 2):       # 只看每对相邻座位
        a = row[i]                         # 左边的人的编号
        b = a ^ 1                          # a 的配偶编号

        # 配偶所在的座位下标以及对应的沙发编号
        j = pos[b]                         # 配偶所在的座位
        couch_a = i // 2                   # a 所在的沙发（即第 i//2 张沙发）
        couch_b = j // 2                   # 配偶所在的沙发

        uf.union(couch_a, couch_b)         # 把这两张沙发连到同一个集合

    # 统计有多少不同的根，即有多少连通块
    components = len({uf.find(i) for i in range(n)})

    # 最少交换次数 = 总沙发数 - 连通块数
    return n - components
```

> **关键行解释**  
> - `a ^ 1`：异或 1 快速得到配偶。  
> - `couch_a = i // 2`：把座位下标映射到「沙发编号」——每两个座位是一张沙发。  
> - `uf.union(couch_a, couch_b)`：把两张沙发放进同一个连通块，表示它们之间有配偶跨坐的需求。  
> - `components = len({uf.find(i) for i in range(n)})`：遍历所有沙发，统计最终有多少不同的根（即多少独立的块）。

#### 复杂度  

- **时间复杂度：`O(n α(n)) ≈ O(n)`**  
  - `n` 为情侣对数（最多 30），我们遍历一次数组做 `n` 次 `union` 与 `find`。  
  - 并查集的 `find`/`union` 近似常数时间，实际复杂度是 α(n)（反阿克曼函数），对于 30 这种小规模几乎可以视作 O(1)。  
  - 与暴力解的 `O(n²)` 相比，**速度提升了一个数量级**。

- **空间复杂度：`O(n)`**  
  - 需要保存并查集的 `parent`、`rank` 数组以及 `pos` 字典，各占线性空间。  
  - 只使用了与输入规模同阶的额外空间。

---

## 心得

- **核心技巧**：把「配偶跨座」的关系抽象为图的连通块，利用并查集快速统计块的数量，从而得到最少交换次数。  
- **适用的题型**  
  1. **“把相邻元素配对”** 的问题，如 *Friends Of Appropriate Ages*（配对年龄）  
  2. **“交换使每组成员相邻”** 的问题，如 *Minimum Swaps to Make Strings Equal*（通过交换使字符串相等）  
  3. **“把元素分到同一集合”** 的图论题，如 *Redundant Connection*（找多余的边）  
- **一句话总结解题钥匙**：**把每对座位当作节点，配偶跨坐形成连边，用并查集合并节点，答案是 “节点数 – 连通块数”。**

---

## 反思

- **第一反应**：看到“每对情侣要坐在一起”，立刻想到“遍历每对座位，如果配偶不在右边就把他搬过来”。这就是暴力贪心的思路。  
- **最容易踩的坑**  
  1. **配偶编号的计算**：一定要记住 `partner = person ^ 1`，否则会出现 `partner = person + 1`（仅对偶数有效）导致错误。  
  2. **下标与沙发编号的映射**：座位是 `2n` 长，沙发编号是 `i // 2`，混用容易出错。  
  3. **并查集的路径压缩**：如果只实现了普通 `find`，在最坏情况下仍可能出现近似线性时间。  
- **下次遇到同类题**：第一步先**把“跨组关系”抽象成图**（节点＝组，边＝跨组的配对），判断是否可以用 **并查集 / BFS / DFS** 统计连通块，从而把“最少操作次数 = 总组数 – 连通块数” 这种公式直接套上去。这样就能立刻跳出暴力搜索的思维框架。