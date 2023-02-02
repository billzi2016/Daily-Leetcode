# #2115. 根据现有供应品寻找所有可制作的配方 / Find All Possible Recipes from Given Supplies

> 难度：中等 · 标签：Array、Hash Table、String、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/)

---

## 题目（英文原版）

**Description**

You have information about n different recipes. You are given a string array recipes and a 2D string array ingredients. The ith recipe has the name recipes[i], and you can create it if you have all the needed ingredients from ingredients[i]. A recipe can also be an ingredient for other recipes, i.e., ingredients[i] may contain a string that is in recipes.
You are also given a string array supplies containing all the ingredients that you initially have, and you have an infinite supply of all of them.
Return a list of all the recipes that you can create. You may return the answer in any order.
Note that two recipes may contain each other in their ingredients.

**Examples**

**Example 1:**

```
Input: recipes = ["bread"], ingredients = [["yeast","flour"]], supplies = ["yeast","flour","corn"]
Output: ["bread"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
```

**Example 2:**

```
Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
```

**Example 3:**

```
Input: recipes = ["bread","sandwich","burger"], ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich","burger"]
Explanation:
We can create "bread" since we have the ingredients "yeast" and "flour".
We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
We can create "burger" since we have the ingredient "meat" and can create the ingredients "bread" and "sandwich".
```

**Constraints**

- n == recipes.length == ingredients.length
- 1 <= n <= 100
- 1 <= ingredients[i].length, supplies.length <= 100
- 1 <= recipes[i].length, ingredients[i][j].length, supplies[k].length <= 10
- recipes[i], ingredients[i][j], and supplies[k] consist only of lowercase English letters.
- All the values of recipes and supplies combined are unique.
- Each ingredients[i] does not contain any duplicate values.

---

## 题目（中文翻译）

**描述**  
你拥有关于 `n` 种不同配方（recipes）的信息。给定一个字符串数组 `recipes` 和一个二维字符串数组 `ingredients`。第 `i` 种配方的名称为 `recipes[i]`，当且仅当你拥有 `ingredients[i]` 中的所有所需原料时才能制作该配方。配方本身也可以作为其他配方的原料，即 `ingredients[i]` 中可能出现 `recipes` 中的字符串。  

另外，给定一个字符串数组 `supplies`，其中包含你一开始拥有的所有原料，并且这些原料的供应是无限的。  

返回所有你能够制作的配方列表，答案的顺序任意即可。  
注意，两个配方之间可能互相包含对方的原料。

**示例 1**  
```text
Input: recipes = ["bread"], ingredients = [["yeast","flour"]], supplies = ["yeast","flour","corn"]
Output: ["bread"]
Explanation:
我们可以制作 "bread"，因为我们拥有原料 "yeast" 和 "flour"。
```

**示例 2**  
```text
Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich"]
Explanation:
我们可以制作 "bread"，因为我们拥有原料 "yeast" 和 "flour"。  
我们可以制作 "sandwich"，因为我们拥有原料 "meat"，并且可以先制作出原料 "bread"。
```

**示例 3**  
```text
Input: recipes = ["bread","sandwich","burger"], ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]], supplies = ["yeast","flour","meat"]
Output: ["bread","sandwich","burger"]
Explanation:
我们可以制作 "bread"，因为我们拥有原料 "yeast" 和 "flour"。  
我们可以制作 "sandwich"，因为我们拥有原料 "meat"，并且可以先制作出原料 "bread"。  
我们可以制作 "burger"，因为我们已经可以制作出原料 "sandwich"、"meat" 与 "bread"。
```

**约束条件**  
- `n == recipes.length == ingredients.length`  
- `1 <= n <= 100`  
- `1 <= ingredients[i].length, supplies.length <= 100`  
- `1 <= recipes[i].length, ingredients[i][j].length, supplies[k].length <= 10`  
- `recipes[i]、ingredients[i][j]、supplies[k]` 仅由小写英文字母组成。  
- 所有配方名称和供应品的取值集合互不重复。  
- 每个 `ingredients[i]` 中不含重复的原料。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把「我们已经拥有的材料」放进一个集合（把集合想象成厨房的储物柜，里面的每件东西都有名字），  
然后不停地遍历所有配方：

1. 对每个配方检查它的所有原料是否都已经在储物柜里。  
2. 如果全部都有，就「做出」这道菜，把这道菜的名字也放进储物柜（因为以后它可以作为别的配方的原料）。  
3. 再继续遍历，直到一次遍历中没有任何新菜被做出来为止。

> **为什么会对？**  
> 只要一个配方的所有原料已经在集合中，它一定是可做的；把它加入集合后，后面的配方就可能因为多了一个原料而变得可做。循环结束时，集合里包含的所有名字就是我们能做的所有配方。

> **数据结构**  
> - **集合（`set`）**：像字典查词一样，`O(1)` 能判断某个材料是否已经拥有。  
> - **列表（`list`）**：存放配方及其原料，方便遍历。

> **时间/空间复杂度（大白话）**  
> - 每次遍历要检查所有配方的所有原料，最坏情况是要遍历 `n`（配方数）次，每次检查 `m`（每个配方的原料数）个字。于是时间复杂度大约是 `O(n * n * m)`，可以简记为 `O(n²·m)`，也就是说如果配方很多、每个配方原料也多，速度会明显变慢。  
> - 只用了几个集合和列表，空间上和输入规模成正比，记作 `O(n + total_ingredients)`。

#### 代码（Python）

```python
from typing import List

def findAllRecipes(recipes: List[str],
                  ingredients: List[List[str]],
                  supplies: List[str]) -> List[str]:
    # 1️⃣ 把已有的材料放进「储物柜」——集合查询快
    have = set(supplies)          # 已经拥有的材料/配方
    n = len(recipes)
    # 2️⃣ 记录每个配方是否已经做过，防止重复加入
    made = [False] * n
    # 3️⃣ 循环尝试做配方，直到一次循环没有新配方产生
    progress = True
    while progress:
        progress = False
        for i in range(n):
            if made[i]:
                continue                     # 已经做好，跳过
            # 检查第 i 个配方的所有原料是否都在 have 中
            if all(ing in have for ing in ingredients[i]):
                # 所有原料都有，做出这道菜
                have.add(recipes[i])         # 把它也加入储物柜
                made[i] = True
                progress = True              # 本轮有进展，继续循环
    # 最后把所有做过的配方收集返回
    return [recipes[i] for i, ok in enumerate(made) if ok]
```

#### 复杂度  

- **时间复杂度**：`O(n²·m)`  
  - `n` 为配方数，`m` 为单个配方的原料数。最坏情况下每轮遍历 `n` 个配方，最多会进行 `n` 轮（每轮至少做出一个新配方），于是总操作次数约为 `n × n × m`。  
- **空间复杂度**：`O(n + total_ingredients)`  
  - `have` 集合最多存放所有配方和所有原料，`made` 数组存 `n` 个布尔值，都是线性空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于重复遍历所有配方**。  
我们可以把配方之间的「需要」关系看成一张有向图：

- **节点**：所有配方和原料（原料本身不需要再拆分）。
- **有向边**：如果配方 `B` 需要原料（或配方）`A`，就在 `A → B` 上建一条边，表示「有了 A，就可以少一个 B 的依赖」。

这样的问题恰好是 **拓扑排序**（Topological Sort）——  
从「已经拥有」的节点出发，逐层「消除」它们指向的配方的依赖计数（入度），入度降到 0 的配方就可以做了，随后把它当作新的原料继续传播。

**核心步骤**

1. **统计入度**：`indeg[recipe] = 该配方需要的原料数量`。  
2. **建立邻接表**：`graph[ingredient]` 列出所有因为该原料而受影响的配方。  
3. **初始化队列**：把所有 **初始材料**（`supplies`）放入队列。  
4. **BFS（广度优先）遍历**：  
   - 从队列弹出一个已拥有的材料 `x`。  
   - 查看 `graph[x]` 中的每个配方 `y`，把 `indeg[y]` 减 1（相当于「把 x 当作已满足的依赖」）。  
   - 当 `indeg[y]` 变成 0，说明所有依赖都已经准备好，`y` 可以做出来，加入结果列表并把 `y` 本身也放进队列（因为它以后可能是别的配方的原料）。  
5. 最终队列为空时，所有被加入结果的配方即为可做的配方。

> **为什么快？**  
> 每条边只会被访问一次（从原料指向配方），不需要重复扫描整个配方列表。时间正比于「配方数 + 边数」，即 `O(N + E)`，在最坏情况下也只比输入规模大常数倍。

> **类比**  
> 想象每个配方是一座工厂，需要若干原料才能启动。我们先把所有已经有的原料装进运输车（队列），车子跑到每个工厂把对应的需求「减掉」一件。某座工厂的需求全部被满足时，它就可以开工（加入结果），并且生产出自己的产品（也变成一种原料，继续装进车子），帮助后面的工厂启动。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def findAllRecipes(recipes: List[str],
                  ingredients: List[List[str]],
                  supplies: List[str]) -> List[str]:
    # 1️⃣ 建立图：ingredient -> [recipes that need it]
    graph = defaultdict(list)        # 邻接表
    indeg = {}                        # 入度：每个配方还缺多少原料

    for r, ing_list in zip(recipes, ingredients):
        indeg[r] = len(ing_list)      # 需要的原料数量
        for ing in ing_list:
            graph[ing].append(r)      # ing 供应后会帮助 r

    # 2️⃣ 队列里先放所有我们已经拥有的材料
    q = deque(supplies)
    result = []

    # 3️⃣ BFS 拓扑排序
    while q:
        cur = q.popleft()             # 已有的材料或已做好的配方
        # 看看哪些配方因为有了 cur 而少一个依赖
        for nxt in graph[cur]:
            indeg[nxt] -= 1            # 依赖计数减 1
            if indeg[nxt] == 0:       # 所有原料齐了，可以做了
                result.append(nxt)    # 记录答案
                q.append(nxt)         # 这道菜本身也可以作为别的配方的原料

    return result
```

#### 复杂度  

- **时间复杂度**：`O(N + E)`  
  - `N` 为配方总数（`len(recipes)`），`E` 为所有「配方‑原料」关系的总数（即所有 `ingredients[i]` 长度之和）。每个原料只会遍历一次，每条边只会导致一次 `indeg` 减法，整体线性。相比暴力解的 `O(n²·m)`，在配方很多时快很多。  
- **空间复杂度**：`O(N + E)`  
  - `graph` 保存每条边，`indeg` 保存每个配方的计数，队列最多装 `N + supplies` 个元素，都是线性空间。

---

## 心得  

- **核心技巧**：把「配方‑原料」关系抽象成有向图，利用 **拓扑排序（Kahn 算法）** 逐层消除依赖。  
- **适用场景**：  
  1. 课程安排（Course Schedule）——判断能否完成所有课程。  
  2. 任务调度（Task Schedule with Prerequisites）——先完成前置任务后才能进行后续任务。  
  3. 生产线配方、软件包依赖解析等需要先解决前置条件的场景。  
- **一句话总结**：**把“先有材料才能做菜”转化为“先有前置节点才能访问后继节点”，用拓扑排序一次遍历搞定**。

---

## 反思  

- **拿到题目第一反应**：把已有材料放进集合，循环检查配方是否可做——就是暴力的「一次遍历 + 重复」思路。  
- **最容易踩的坑**  
  - **循环依赖**：两道配方相互需要对方时，入度永远不会降到 0，必须通过拓扑排序自然剔除。  
  - **原料不在任何配方里**：它们只出现在 `supplies`，仍需加入队列，否则后面的图遍历会遗漏。  
  - **重复加入**：一旦配方完成后就不应再重复加入结果，否则会产生错误的计数。  
- **下次遇到同类题**：第一步先思考「是否可以把关系建成有向图并统计入度」，如果可以，就直接走拓扑排序路线；如果图结构不明显，再回退到集合+循环的暴力模拟。