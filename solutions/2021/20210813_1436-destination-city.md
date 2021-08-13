# #1436. 目的地城市 / Destination City

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/destination-city/)

---

## 题目（英文原版）

**Description**

You are given the array paths, where paths[i] = [cityAi, cityBi] means there exists a direct path going from cityAi to cityBi. Return the destination city, that is, the city without any path outgoing to another city.
It is guaranteed that the graph of paths forms a line without any loop, therefore, there will be exactly one destination city.

**Examples**

**Example 1:**

```
Input: paths = [["London","New York"],["New York","Lima"],["Lima","Sao Paulo"]]
Output: "Sao Paulo" 
Explanation: Starting at "London" city you will reach "Sao Paulo" city which is the destination city. Your trip consist of: "London" -> "New York" -> "Lima" -> "Sao Paulo".
```

**Example 2:**

```
Input: paths = [["B","C"],["D","B"],["C","A"]]
Output: "A"
Explanation: All possible trips are: 
"D" -> "B" -> "C" -> "A". 
"B" -> "C" -> "A". 
"C" -> "A". 
"A". 
Clearly the destination city is "A".
```

**Example 3:**

```
Input: paths = [["A","Z"]]
Output: "Z"
```

**Constraints**

- 1 <= paths.length <= 100
- paths[i].length == 2
- 1 <= cityAi.length, cityBi.length <= 10
- cityAi != cityBi
- All strings consist of lowercase and uppercase English letters and the space character.

---

## 题目（中文翻译）

给定数组 `paths`，其中 `paths[i] = [cityAi, cityBi]` 表示存在一条直接路径从 `cityAi` 到 `cityBi`。返回 **目的地城市**（destination city），即没有任何出发路径指向其他城市的城市。  
题目保证 `paths` 构成一条不含环的直线形图，因此必然恰好存在一个目的地城市。

## 示例

### 示例 1
**输入**  
`paths = [["London","New York"],["New York","Lima"],["Lima","Sao Paulo"]]`

**输出**  
`"Sao Paulo"`

**解释**  
从 `"London"` 出发，你会依次到达 `"Sao Paulo"`，它就是目的地城市。整个行程为：  
`"London" -> "New York" -> "Lima" -> "Sao Paulo"`。

### 示例 2
**输入**  
`paths = [["B","C"],["D","B"],["C","A"]]`

**输出**  
`"A"`

**解释**  
所有可能的行程为：  
`"D" -> "B" -> "C" -> "A"`  
`"B" -> "C" -> "A"`  
`"C" -> "A"`  
`"A"`  
显然目的地城市是 `"A"`。

### 示例 3
**输入**  
`paths = [["A","Z"]]`

**输出**  
`"Z"`

## 约束条件
- `1 <= paths.length <= 100`
- `paths[i].length == 2`
- `1 <= cityAi.length, cityBi.length <= 10`
- `cityAi != cityBi`
- 所有字符串仅由大小写英文字母和空格组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们有若干条“一对一” 的直达路径 `paths[i] = [cityA, cityB]`，  
要求找出 **没有任何出发路径** 的城市，也就是 **终点城市**。  

最直接的想法是：

1. 把所有路径的 **起点**（`cityA`）和 **终点**（`cityB`）都列出来。  
2. 对每一个终点 `cityB`，检查它在所有起点中是否出现过。  
   - 若它从来没有作为起点出现，就说明没有从它出发的路径，它就是答案。  

这里我们把 **起点集合** 想象成一本“出发城市字典”，  
把每个城市的名字当作 **key**，只要在字典里能查到，就说明它还能继续前进。  
暴力做法就是对每个终点 **遍历整个字典** 去查找，这样会产生两层循环。

> **为什么一定会有答案？**  
> 题目保证路径形成一条 **不循环的链**（类似 “A → B → C → …”），  
> 所以链的最末端必然只有入度没有出度，即唯一的终点城市。

#### 代码（Python）

```python
def destCity_brute(paths):
    """
    暴力解：对每个终点城市，遍历所有起点城市检查是否出现。
    时间复杂度 O(n^2)，空间复杂度 O(n)（存放起点列表）。
    """
    # 把所有起点收集到列表中
    start_cities = [p[0] for p in paths]          # 起点集合

    # 遍历每一条路径的终点
    for _, dest in paths:                         # dest 为终点城市
        # 在所有起点中查找是否出现过
        found = False
        for s in start_cities:
            if s == dest:                          # 找到相同的起点
                found = True
                break
        if not found:                               # 终点没有出现在起点列表里
            return dest

    # 根据题目保证，这里永远不会执行到
    return ""
```

#### 复杂度

- **时间复杂度：`O(n²)`**  
  `n` 为路径条数。外层遍历每条路径一次，内层在所有起点中再遍历一次。  
  用大白话说，就是“如果有 10 条路径，需要检查 10×10=100 次”。

- **空间复杂度：`O(n)`**  
  只额外保存了所有起点城市的列表，最多保存 `n` 个字符串。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“对每个终点都要线性扫描所有起点”**。  
我们可以把 **“是否是起点”** 这件事的查询时间从 *O(n)* 降到 *O(1)*。

**哈希表（Python 中的 `set`）** 正好可以做到常数时间的“是否存在”查询。  
思路如下：

1. 把所有起点城市放进一个 **集合** `starts`。  
   - 集合类似“查字典”，`city in starts` 能在 **常数时间** 判定。  
2. 再遍历一次路径的终点 `cityB`，只要发现 `cityB` **不在** `starts` 中，就找到了终点城市。  

整个过程只需要 **两次遍历**，每次都是线性时间 `O(n)`，空间只多出一个集合 `O(n)`。

> **类比**：想象你在一个城市列表里找“唯一的没有出口的城市”。  
> 把所有有出口的城市写在一本“有出口城市手册”里（集合），  
> 然后把每个城市拿出来查手册，没查到的就是终点。

#### 代码（Python）

```python
def destCity(paths):
    """
    最优解：使用集合（哈希表）一次性记录所有起点城市，
    再遍历终点城市判断是否出现过。
    时间复杂度 O(n)，空间复杂度 O(n)。
    """
    # 1. 把所有起点放进集合，查找速度 O(1)
    starts = {p[0] for p in paths}   # 集合推导式，等价于 for 循环

    # 2. 找到不在起点集合中的终点
    for _, dest in paths:            # 只关心终点 cityB
        if dest not in starts:       # 若终点不在起点集合，说明没有出路
            return dest

    # 根据题目保证，这里永远不会执行到
    return ""
```

#### 复杂度

- **时间复杂度：`O(n)`**  
  第一次遍历收集起点，第二次遍历查找终点，都是线性次数。  
  用大白话说，就是“如果有 10 条路径，只需要检查 10+10=20 次”，比 100 次快很多。

- **空间复杂度：`O(n)`**  
  只多用了一个集合保存所有起点，最多存 `n` 个城市名称。

---

## 心得

- **核心技巧**：利用 **哈希表（集合）** 实现 “出现过吗？” 的快速判断。  
- **适用的题型**  
  1. “找出唯一出现一次的元素”——如 LeetCode 136（只出现一次的数字）  
  2. “找出没有出边的节点”——如 LeetCode 1971（寻找图中没有出度的节点）  
  3. “找出唯一的缺失/多余元素”——如 LeetCode 448（找到所有数组中缺失的数字）  
- **一句话总结**：**把所有“能继续前进的城市”记下来，剩下的就是终点。**

---

## 反思

- **第一反应**：把所有城市都列出来，然后手动比较起点和终点。  
- **最容易踩的坑**  
  - 忽略了路径可能只有一条的极端情况（仍然适用集合方法）。  
  - 把终点和起点都放进同一个集合，导致查询失效。  
- **下次遇到同类题**：第一步先思考“有没有可以一次性记录‘可以继续’的信息结构”，常常是集合或字典。这样就能把暴力的 O(n²) 降到 O(n)。