# #2391. 收集垃圾的最少时间 / Minimum Amount of Time to Collect Garbage

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-amount-of-time-to-collect-garbage/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings garbage where garbage[i] represents the assortment of garbage at the ith house. garbage[i] consists only of the characters 'M', 'P' and 'G' representing one unit of metal, paper and glass garbage respectively. Picking up one unit of any type of garbage takes 1 minute.
You are also given a 0-indexed integer array travel where travel[i] is the number of minutes needed to go from house i to house i + 1.
There are three garbage trucks in the city, each responsible for picking up one type of garbage. Each garbage truck starts at house 0 and must visit each house in order; however, they do not need to visit every house.
Only one garbage truck may be used at any given moment. While one truck is driving or picking up garbage, the other two trucks cannot do anything.
Return the minimum number of minutes needed to pick up all the garbage.

**Examples**

**Example 1:**

```
Input: garbage = ["G","P","GP","GG"], travel = [2,4,3]
Output: 21
Explanation:
The paper garbage truck:
1. Travels from house 0 to house 1
2. Collects the paper garbage at house 1
3. Travels from house 1 to house 2
4. Collects the paper garbage at house 2
Altogether, it takes 8 minutes to pick up all the paper garbage.
The glass garbage truck:
1. Collects the glass garbage at house 0
2. Travels from house 0 to house 1
3. Travels from house 1 to house 2
4. Collects the glass garbage at house 2
5. Travels from house 2 to house 3
6. Collects the glass garbage at house 3
Altogether, it takes 13 minutes to pick up all the glass garbage.
Since there is no metal garbage, we do not need to consider the metal garbage truck.
Therefore, it takes a total of 8 + 13 = 21 minutes to collect all the garbage.
```

**Example 2:**

```
Input: garbage = ["MMM","PGM","GP"], travel = [3,10]
Output: 37
Explanation:
The metal garbage truck takes 7 minutes to pick up all the metal garbage.
The paper garbage truck takes 15 minutes to pick up all the paper garbage.
The glass garbage truck takes 15 minutes to pick up all the glass garbage.
It takes a total of 7 + 15 + 15 = 37 minutes to collect all the garbage.
```

**Constraints**

- 2 <= garbage.length <= 105
- garbage[i] consists of only the letters 'M', 'P', and 'G'.
- 1 <= garbage[i].length <= 10
- travel.length == garbage.length - 1
- 1 <= travel[i] <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 **0** 开始的字符串数组 **garbage**，其中 `garbage[i]` 表示第 `i` 栋房子里的垃圾种类。`garbage[i]` 仅由字符 **'M'**、**'P'**、**'G'** 组成，分别代表一单位的金属（Metal）、纸张（Paper）和玻璃（Glass）垃圾。捡起任意一种垃圾的 **1** 单位需要 **1** 分钟。

另给定一个下标从 **0** 开始的整数数组 **travel**，其中 `travel[i]` 表示从第 `i` 栋房子前往第 `i+1` 栋房子所需的分钟数。

城市里有 **3** 辆垃圾车，每辆负责收集一种垃圾。所有垃圾车都从第 **0** 栋房子出发，并且必须按顺序访问房子；但它们不必每栋房子都停留。**任意时刻只能有一辆垃圾车在工作**——当一辆垃圾车在行驶或捡垃圾时，另外两辆均不能进行任何操作。

返回收集完所有垃圾所需的最少总分钟数。

---

### 示例

**示例 1**  
```text
Input: garbage = ["G","P","GP","GG"], travel = [2,4,3]
Output: 21
Explanation:
纸张垃圾车（paper garbage truck）:
1. 从第 0 栋房子行驶到第 1 栋（耗时 2 分钟）
2. 捡起第 1 栋的纸张垃圾（耗时 1 分钟）
3. 从第 1 栋行驶到第 2 栋（耗时 4 分钟）
4. 捡起第 2 栋的纸张垃圾（耗时 1 分钟）
共计 8 分钟完成所有纸张垃圾的收集。

玻璃垃圾车（glass garbage truck）:
1. 捡起第 0 栋的玻璃垃圾（耗时 1 分钟）
2. 从第 0 栋行驶到第 1 栋（耗时 2 分钟）
3. 从第 1 栋行驶到第 2 栋（耗时 4 分钟）
4. 捡起第 2 栋的玻璃垃圾（耗时 1 分钟）
5. 从第 2 栋行驶到第 3 栋（耗时 3 分钟）
6. 捡起第 3 栋的玻璃垃圾（耗时 2 分钟）
共计 13 分钟完成所有玻璃垃圾的收集。

金属垃圾车（metal garbage truck）不需要出行，因为所有房子里都没有金属垃圾。

总时间 = 8 + 13 + 0 = **21** 分钟。
```

**示例 2**  
```text
Input: garbage = ["MMM","PGM","GP"], travel = [3,10]
Output: 37
Explanation:
金属垃圾车（metal garbage truck）需要 7 分钟收集完所有金属垃圾。  
纸张垃圾车（paper garbage truck）需要 15 分钟收集完所有纸张垃圾。  
玻璃垃圾车（glass garbage truck）需要 15 分钟收集完所有玻璃垃圾。  

总时间 = 7 + 15 + 15 = **37** 分钟。
```

---

### 约束条件
- `2 <= garbage.length <= 10^5`
- `garbage[i]` 只包含字符 `'M'`、`'P'`、`'G'`
- `1 <= garbage[i].length <= 10`
- `travel.length == garbage.length - 1`
- `1 <= travel[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把三辆垃圾车分别当成 **三个人**，让每个人从第 0 栋房子走到第 `n‑1` 栋房子。  
在走到每一栋房子时：

1. 检查这栋房子里有没有自己负责的垃圾（比如金属车负责 `'M'`）。  
2. 如果有，就把所有该类型的垃圾全部捡完（每捡一个单位花 1 分钟）。  
3. 然后继续向下一栋房子前进，前进的时间由 `travel` 数组给出。

这种做法把 **“只去有对应垃圾的房子”** 的优化完全忽略了——每辆车都会把所有房子都走一遍。  

- **数据结构**：我们只需要遍历数组，`list`（列表）本身就能满足需求。可以把 `travel` 看成一本 **路程字典**：键是“从第 i 栋到第 i+1 栋”，值是需要的分钟数。  
- **正确性**：因为每次我们都完整模拟了所有可能的行动（走路 + 捡垃圾），所以得到的时间一定是 **一种可行的方案**，即使它不是最优的。  

**时间复杂度**：  
- 对每一种垃圾（3 种）我们都遍历所有房子 `n` 次。  
- 在每次遇到目标垃圾时，又要重新累加从起点到当前房子的所有 `travel`（这一步是线性求和），最坏会出现 `1 + 2 + … + n = O(n²)` 次累加。  
- 因此整体是 **O(n²)**，这里的 `n²` 可以理解为“如果有 10,000 栋房子，计算时间大约是 100,000,000 次基本操作”，在实际数据范围（`10⁵`）下会超时。  

**空间复杂度**：  
- 只使用了常数个额外变量（计数器、累计时间），所以是 **O(1)**。

#### 代码（Python）

```python
def garbageCollection_bruteforce(garbage, travel):
    """
    暴力模拟三辆车全部走完所有房子
    :param garbage: List[str] 每栋房子的垃圾种类字符串
    :param travel:  List[int] i -> i+1 的行驶时间
    :return: int 最少需要的总时间（这里其实是一个可行的时间）
    """
    n = len(garbage)
    total_time = 0

    # 三种垃圾对应的字符
    types = ['M', 'P', 'G']

    for typ in types:                     # 对每一种垃圾车
        cur_time = 0                       # 这辆车花的时间
        for i in range(n):                 # 从第 0 栋遍历到最后一栋
            # 1. 捡垃圾：遍历当前房子里所有字符，计数属于 typ 的
            cur_time += garbage[i].count(typ)

            # 2. 前往下一栋（如果不是最后一栋）
            if i < n - 1:
                cur_time += travel[i]      # 直接加上 travel[i]，不管后面有没有该类型垃圾

        total_time += cur_time             # 累加三辆车的时间

    return total_time
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 这里的 `n²` 代表“如果房子数量是 10,000，最坏情况下要做大约 100,000,000 次累加”。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每辆车都走完了所有房子**。实际上，垃圾车只需要 **走到最后一次出现自己负责的垃圾的那栋房子**，之后再也不必继续前进。  

我们可以把问题拆成两部分：

1. **捡垃圾的时间**  
   - 每捡一个单位垃圾花 1 分钟。于是只要把所有字符串里出现的字符总数相加即可，**与车的行驶路线无关**。  

2. **行驶的时间**  
   - 对于每一种垃圾类型，找出 **最右侧（下标最大的）** 那栋房子里出现该类型垃圾的下标 `last[typ]`。  
   - 只需要把车从第 0 栋走到 `last[typ]`，期间的行驶时间即为从 `travel[0]` 到 `travel[last[typ]-1]` 的累计和。  
   - 为了快速求区间和，先把 `travel` 做一次 **前缀和**：`pref[i] = travel[0] + … + travel[i-1]`（`pref[0]=0`）。这样从第 0 栋到第 `k` 栋的行驶时间就是 `pref[k]`，查询是 O(1)。  

**核心算法**：一次遍历找出每种垃圾的最右出现位置 + 前缀和求区间和。  

**类比**：  
- 想象三位快递员分别负责 **金属、纸张、玻璃**。他们只需要跑到自己最后一次送货的地点，然后返回办公室（这里返回不算时间）。如果你把所有街道的距离先算好（前缀和），每个人只需要看自己最远的那条街道距离即可。

#### 代码（Python）

```python
def garbageCollection(garbage, travel):
    """
    最优解：一次遍历 + 前缀和
    :param garbage: List[str] 每栋房子的垃圾种类字符串
    :param travel:  List[int] i -> i+1 的行驶时间
    :return: int 最少需要的总时间
    """
    n = len(garbage)

    # 1. 统计所有垃圾的总数量（捡垃圾的时间）
    total_pick = sum(len(g) for g in garbage)   # 每个字符都是 1 分钟

    # 2. 前缀和：pref[i] 表示从第 0 栋到第 i 栋（不含 i）需要的行驶时间
    pref = [0] * (n)           # 长度 n，pref[0]=0
    for i in range(1, n):
        pref[i] = pref[i-1] + travel[i-1]

    # 3. 找到每种垃圾的最右出现位置
    last = {'M': -1, 'P': -1, 'G': -1}
    for idx, g in enumerate(garbage):
        for ch in set(g):          # 用 set 去重，防止同一栋里多次计数
            last[ch] = idx        # 更新为更大的下标

    # 4. 累加每辆车的行驶时间
    total_travel = 0
    for typ in ['M', 'P', 'G']:
        if last[typ] != -1:                 # 该类型垃圾至少出现一次
            total_travel += pref[last[typ]]  # 从 0 到最右出现的那栋的累计行驶时间

    return total_pick + total_travel
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了 `garbage` 一次（`n`），再遍历一次 `travel` 生成前缀和（`n-1`），所有操作都是常数时间的。  
  - 与暴力解的 `O(n²)` 相比，**把时间从“平方级”降到了线性级**，即如果有 100,000 栋房子，只需要大约 200,000 次基本操作，完全可以在一秒内跑完。  

- **空间复杂度**：`O(1)`（不计输出）  
  - 使用了固定大小的字典 `last`、前缀和数组 `pref`（长度 `n`，但这属于输入规模同级的必需空间），额外的辅助变量都是常数个。  

---

## 心得  

- **核心技巧**：**只走到最后一次需要的地点 + 前缀和快速求区间和**。  
- **适用的题型**  
  1. “**最右出现位置**” 类问题，如 “Minimum Time to Collect All Apples” 等。  
  2. 需要多次求 **区间累计和** 的场景，前缀和是常用利器。  
- **一句话总结解题钥匙**：  
  > “别让车白跑——找出每种垃圾最远的房子，然后用前缀和一次算出行驶时间”。  

---

## 反思  

- **第一反应**：把三辆车都让它们走完整条街道，直接把所有 `travel` 累加，感觉最安全。  
- **最容易踩的坑**  
  - 忘记 **只计数一次** 行驶时间：每种垃圾只需要走到它的最右出现位置，而不是每次出现都重新累加。  
  - 处理 **空类型**（某种垃圾根本不存在）时，需要判断 `last[typ] == -1`，否则会错误地把 `pref[-1]` 当作最后一栋的距离。  
  - 对 `travel` 的前缀和索引容易出错：`pref[i]` 表示到第 `i` 栋的累计时间（不包括第 `i` 到 `i+1` 的路段），所以取值时要用 `last[typ]` 而不是 `last[typ] - 1`。  

- **下次遇到同类题**，第一步应该问自己：  
  1. “每个子任务（比如每种垃圾）最远需要到哪儿？”  
  2. “是否可以把重复的区间求和预处理一次（前缀和）？”  

这样就能迅速从暴力思路跳到最优解。