# #332. 重建行程 / Reconstruct Itinerary

> 难度：困难 · 标签：Depth-First Search、Graph、Eulerian Circuit · [LeetCode 链接](https://leetcode.com/problems/reconstruct-itinerary/)

---

## 题目（英文原版）

**Description**

You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.
All of the tickets belong to a man who departs from "JFK", thus, the itinerary must begin with "JFK". If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.
You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.

**Examples**

**Example 1:**

```
Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
Output: ["JFK","MUC","LHR","SFO","SJC"]
```

**Example 2:**

```
Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
Explanation: Another possible reconstruction is ["JFK","SFO","ATL","JFK","ATL","SFO"] but it is larger in lexical order.
```

**Constraints**

- 1 <= tickets.length <= 300
- tickets[i].length == 2
- fromi.length == 3
- toi.length == 3
- fromi and toi consist of uppercase English letters.
- fromi != toi

---

## 题目（中文翻译）

给定一组航空机票，其中 `tickets[i] = [from_i, to_i]` 表示一段航班的出发机场和到达机场。请按照顺序重建完整的行程并返回它。

所有机票均属于同一个旅客，该旅客从 **"JFK"** 出发，因此行程必须以 **"JFK"** 为起点。若存在多个合法的行程，则返回按整体字符串的字典序（lexical order）最小的那条。

可以假设所有机票至少能构成一条有效的行程。必须恰好使用每张机票一次且仅使用一次。

## 示例

### 示例 1
**输入**  
```json
tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
```
**输出**  
```json
["JFK","MUC","LHR","SFO","SJC"]
```

### 示例 2
**输入**  
```json
tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
```
**输出**  
```json
["JFK","ATL","JFK","SFO","ATL","SFO"]
```
**解释**  
另一种可能的重建结果是 `["JFK","SFO","ATL","JFK","ATL","SFO"]`，但它的字典序更大。

## 约束条件
- `1 <= tickets.length <= 300`
- `tickets[i].length == 2`
- `from_i.length == 3`
- `to_i.length == 3`
- `from_i` 与 `to_i` 仅由大写英文字母组成
- `from_i != to_i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有机票看成一条条有向边**，从 `"JFK"` 开始深度优先遍历（DFS），把每一次走的路径记录下来，只要恰好用了所有机票，就得到一条合法的行程。  
如果遍历过程中出现死路（没有可用的下一张机票），就回溯，尝试另一条路——这就是典型的「穷举所有可能」的回溯法。

> **类比**：想象你手里有一堆拼图块（机票），每块都有「左边」和「右边」两个字（出发机场、到达机场）。从 `"JFK"` 开始，你把左边对应的块放在桌子上，然后找一块左边等于当前右边的块继续拼，直到所有块都被用完。如果中途找不到合适的块，就把刚才放的块拿掉（回溯），重新尝试别的块。

**为什么正确**  
回溯会尝试所有可能的「使用顺序」，只要存在至少一条能够恰好使用全部机票的路径，回溯一定会找到它。  

**时间/空间复杂度**  
- **时间**：每张机票都有两种「使用」或「不使用」的状态，最坏情况下需要遍历所有排列。若有 `n` 张机票，排列数是 `n!`（阶乘），因此时间复杂度是 **O(n!)**。这在 `n ≤ 300` 时是不可接受的——想象 10 张票就已经是 3,628,800 种可能了。  
- **空间**：递归栈的深度最多 `n`，再加上保存当前路径的列表，也是 **O(n)**。

#### 代码（Python）

```python
from collections import defaultdict
from copy import deepcopy

def find_itinerary_bruteforce(tickets):
    # 建立邻接表：每个出发机场对应所有可能的到达机场列表
    graph = defaultdict(list)
    for a, b in tickets:
        graph[a].append(b)
    # 为了后面能够按字典序遍历，把每条边按字典序排序
    for src in graph:
        graph[src].sort()

    n = len(tickets)
    route = ["JFK"]                     # 当前已走的路径，只保存机场序列
    used = [False] * n                  # 标记第 i 张票是否已经使用

    def dfs():
        # 当路径长度等于票数+1，说明恰好用了所有票
        if len(route) == n + 1:
            return True

        cur = route[-1]                 # 当前所在的机场
        # 枚举所有从 cur 出发的票（按照字典序已经排好序）
        for i, (src, dst) in enumerate(tickets):
            if not used[i] and src == cur:
                used[i] = True
                route.append(dst)
                if dfs():                # 继续往下走
                    return True
                # 回溯
                used[i] = False
                route.pop()
        return False

    dfs()
    return route
```

> 代码要点：
> - `graph` 用来把「同一个出发机场的所有目的地」收集在一起，类似于“字典查词典”，`src` 是键（key），`dst` 则是对应的值（value）。  
> - `used` 数组记录每张票是否已经用了，防止重复使用。  
> - `dfs` 递归尝试每一种可能的下一站，失败后回溯（撤销选择）。

#### 复杂度

- **时间复杂度**：**O(n!)** —— 解释：`n!` 表示“n 的阶乘”，就是 `1 × 2 × 3 × … × n`，随着 `n` 增大，增长速度非常快，几乎不可能在合理时间内跑完。
- **空间复杂度**：**O(n)** —— 只需要保存递归栈和当前路径，最多 `n` 层。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复搜索**：很多分支在走到某一步后会发现已经走不通，却已经花掉了大量时间去尝试。我们需要一种只遍历一次、一次性把所有边「用掉」的算法。

本题的本质是 **在有向图中寻找欧拉路径（Eulerian Path）**：  
- 每张机票是一条有向边，机场是节点。  
- 要使用 **所有** 边恰好一次，且必须从 `"JFK"` 开始。  
- 当图满足欧拉路径的条件时，**Hierholzer 算法** 能在 **线性时间 O(E)**（E 为边数）构造出这条路径。

**Hierholzer 算法简述**（适合初学者）：

1. **从起点出发**（这里固定为 `"JFK"`），沿着任意可走的边一直前进，直到走不动（没有未使用的出边）。把走过的节点记录下来，形成一个「环」或「路径」。
2. 可能出现「环」里还有未走过的出边，此时**把这个环中还有未使用边的节点当作新起点**，再从那里进行同样的深度优先搜索，把新走的路径插入到原来的环中。
3. 重复第 2 步，直到所有边都被使用完。最终得到的路径即为欧拉路径。

> **类比**：把所有机票想成一条条「绳子」连在一起，你从 `"JFK"` 开始拉绳子，尽可能往前拉，直到绳子打了结（没有可继续的绳子）。如果这条绳子中间还有未用的绳子，你把手移到那个结点，再继续往前拉，把新拉出来的部分「塞进」原来的绳子里。最后，所有绳子都连成一条长长的链子，这条链子就是我们的行程。

**字典序最小** 的要求：  
- 在遍历每个节点的出边时，**必须先走字典序最小的那条**。  
- 为了让 `pop()` 能直接取到最小的目的地，我们把每个邻接列表 **逆序排序**，然后使用 **栈**（后进先出）取元素。这样每次弹出的都是当前字典序最小的未使用航班。

#### 代码（Python）

```python
from collections import defaultdict

def find_itinerary(tickets):
    """
    使用 Hierholzer 算法求欧拉路径（字典序最小）。
    """
    # 1. 建图：每个出发机场对应一个目的地列表
    graph = defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)

    # 2. 对每个出发机场的目的地列表进行逆序排序
    #    这样在后面 pop() 时，能得到字典序最小的机场
    for src in graph:
        graph[src].sort(reverse=True)

    route = []            # 最终的行程（逆序存放）

    def dfs(node):
        """
        深度优先遍历：不断取出当前节点的最小未使用目的地，
        递归访问，等所有出边用完后把节点加入 route。
        """
        # 当还有未使用的出边时，持续前进
        while graph[node]:
            # 取出字典序最小的目的地（因为是逆序，所以 pop() 取到最小）
            next_node = graph[node].pop()
            dfs(next_node)          # 继续往下走
        route.append(node)          # 所有出边走完后，才把当前机场加入结果

    dfs("JFK")                       # 必须从 JFK 起飞
    # dfs 结束后 route 中的顺序是反的，需要反转回来
    return route[::-1]
```

> 代码要点解释  
> 1. **`defaultdict(list)`**：类似于“查字典”，键是出发机场，值是所有可能的到达机场列表。  
> 2. **逆序排序 + `pop()`**：把列表排成 `['SFO', 'LHR', 'MUC']`（大到小），`pop()` 会弹出最右边的 `'MUC'`，即字典序最小的。这样既保持 **O(1)** 的取出时间，又满足“字典序最小”。  
> 3. **递归 `dfs`**：每进入一个节点，就尽可能把它所有的出边「用掉」——这正是 Hierholzer 的核心：**先把子路径全部走完，再把当前节点加入答案**。  
> 4. **`route[::-1]`**：因为我们是在「回溯」时把节点加入 `route`，所以顺序是倒的，需要再翻转一次得到正确的行程。

#### 复杂度

- **时间复杂度**：**O(E log E)**（这里 `E = n` 为机票数量）。  
  - 构建图的遍历是 O(E)。  
  - 对每个邻接列表排序，最坏情况下每个列表长度为 `O(E)`，整体排序成本是 `O(E log E)`（实际因为总票数 ≤ 300，影响不大）。  
  - DFS 过程中每条边只被 `pop()` 一次，时间是 O(E)。  
  - 与暴力解的 `O(n!)` 相比，线性或近线性时间是完全可以接受的。

- **空间复杂度**：**O(V + E)**，其中 `V` 为机场数。  
  - `graph` 保存所有边，需要 O(E) 空间。  
  - 递归栈深度最多为 `E`，`route` 也需要存 `E+1` 个机场。  

---

## 心得

- **核心技巧**：把「使用所有机票一次」转化为「在有向图中寻找欧拉路径」，并用 **Hierholzer 算法**（深度优先遍历 + 逆序栈）一次性完成。  
- **适用的题型**  
  1. “重新排列行程” 系列（如本题）。  
  2. “给定一组单词，找出所有可能的排列，使得每两个相邻单词的首尾相连” —— 也是欧拉路径的变形。  
  3. “在城市间找一条遍历所有道路恰好一次的路线”——经典的 **Eulerian Trail**（欧拉路）问题。  
- **一句话总结解题钥匙**：  
  *“把所有票看成图的边，用一次遍历把每条边都‘消掉’，并且每次都选字典序最小的下一站。”*

---

## 反思

- **拿到题目第一反应**：先想到回溯穷举，试图把所有票的使用顺序列举出来。  
- **最容易踩的坑**  
  1. **字典序**：如果不对邻接列表进行逆序排序或直接 `pop(0)`（O(n)），会导致时间超限。  
  2. **多条相同出发机场的票**：必须把每条票都视为独立的边，不能只保留一个目的地。  
  3. **环路的插入**：忘记在回溯阶段把节点加入结果，导致得到的路径是倒序或不完整。  
- **下次遇到同类题，第一步该想到**：  
  “这是一条要走完所有边的路径吗？如果是，就考虑欧拉路径/Hierholzer，而不是普通的 DFS/回溯。”  

祝你在算法的旅途中一路顺风！ 🚀