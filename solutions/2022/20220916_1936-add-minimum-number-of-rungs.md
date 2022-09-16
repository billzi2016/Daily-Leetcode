# #1936. **添加最少数量的梯级** / Add Minimum Number of Rungs

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/add-minimum-number-of-rungs/)

---

## 题目（英文原版）

**Description**

You are given a strictly increasing integer array rungs that represents the height of rungs on a ladder. You are currently on the floor at height 0, and you want to reach the last rung.
You are also given an integer dist. You can only climb to the next highest rung if the distance between where you are currently at (the floor or on a rung) and the next rung is at most dist. You are able to insert rungs at any positive integer height if a rung is not already there.
Return the minimum number of rungs that must be added to the ladder in order for you to climb to the last rung.

**Examples**

**Example 1:**

```
Input: rungs = [1,3,5,10], dist = 2
Output: 2
Explanation:
You currently cannot reach the last rung.
Add rungs at heights 7 and 8 to climb this ladder. 
The ladder will now have rungs at [1,3,5,7,8,10].
```

**Example 2:**

```
Input: rungs = [3,6,8,10], dist = 3
Output: 0
Explanation:
This ladder can be climbed without adding additional rungs.
```

**Example 3:**

```
Input: rungs = [3,4,6,7], dist = 2
Output: 1
Explanation:
You currently cannot reach the first rung from the ground.
Add a rung at height 1 to climb this ladder.
The ladder will now have rungs at [1,3,4,6,7].
```

**Constraints**

- 1 <= rungs.length <= 105
- 1 <= rungs[i] <= 109
- 1 <= dist <= 109
- rungs is strictly increasing.

---

## 题目（中文翻译）

给定一个严格递增的整数数组 `rungs`，表示梯子上每根横档（rung）的高度。你当前站在地面（高度为 0），目标是到达最后一根横档。

同时给定一个整数 `dist`。只有当你所在位置（地面或某根横档）与下一根横档之间的距离不超过 `dist` 时，才能爬到该横档。你可以在任意正整数高度插入新的横档，只要该高度原本没有横档。

返回必须添加的最少横档数量，使得你能够爬到最后一根横档。

**示例 1**  
**输入**: `rungs = [1,3,5,10]`, `dist = 2`  
**输出**: `2`  
**解释**:  
你目前无法到达最后一根横档。  
在高度 7 和 8 处各添加一根横档后，即可爬完这把梯子。  
此时梯子上的横档为 `[1,3,5,7,8,10]`。

**示例 2**  
**输入**: `rungs = [3,6,8,10]`, `dist = 3`  
**输出**: `0`  
**解释**:  
这把梯子可以在不添加任何横档的情况下直接爬完。

**示例 3**  
**输入**: `rungs = [3,4,6,7]`, `dist = 2`  
**输出**: `1`  
**解释**:  
你当前无法从地面到达第一根横档。  
在高度 1 处添加一根横档后，即可爬完这把梯子。  
此时梯子上的横档为 `[1,3,4,6,7]`。

**约束条件**  

- `1 <= rungs.length <= 10^5`
- `1 <= rungs[i] <= 10^9`
- `1 <= dist <= 10^9`
- `rungs` 严格递增。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们从地面（高度 `0`）开始，依次看每根梯子之间的距离。如果当前的距离 **≤ dist**，说明可以直接跳过去，不需要做任何事。  
如果距离大于 `dist`，按照最直观的想法就是 **一步一步** 往上加梯子，直到两点之间的距离不再超过 `dist` 为止。  

- **使用的数据结构**：只需要遍历一次数组 `rungs`，不需要额外的数据结构。  
- **生活化类比**：把每根梯子想成楼梯的台阶，`dist` 是我们一次能跨的最大步数。如果两步之间相差太远，我们只能在中间“踩”几个临时的台阶（即插入新的梯子）。  
- **为什么正确**：每次我们都把当前能够到达的最高点往前推进，若无法直接到达下一个目标，就在两者之间插入最靠近目标的梯子（即距离 `dist` 的位置）。这样保证了每一次插入都是必须的，最终得到的插入数量是最小的。  

#### 代码（Python）

```python
def addRungs_bruteforce(rungs, dist):
    """
    暴力版：一步一步在两根梯子之间插入新梯子
    """
    added = 0               # 已经插入的梯子数量
    prev = 0                # 当前所在的高度，起点是地面 0

    for h in rungs:         # 依次遍历每根已有的梯子
        # 两点之间的距离
        gap = h - prev

        # 当 gap 大于 dist 时，需要插入梯子
        while gap > dist:
            # 在当前高度往上走 dist 的位置插入一根新梯子
            prev += dist
            added += 1
            gap = h - prev   # 更新剩余的距离

        # 此时 gap ≤ dist，直接跳到下一根梯子
        prev = h

    return added
```

#### 复杂度  

- **时间复杂度**：`O(total_added + n)`  
  其中 `n` 为原数组长度，`total_added` 为实际需要插入的梯子数量。最坏情况下如果 `dist = 1`，而相邻梯子相差很大，可能会出现 **O(∑gap)** 的循环次数，等价于 `O(max_height)`，在极端数据下会非常慢。  
- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量 `added`、`prev`、`gap`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的“慢点”在于 **逐步插入** 的 `while` 循环——我们一次只能前进 `dist`，却可能需要重复很多次。  
其实我们只关心 **需要插入多少根**，不必真的模拟每一次插入。  

观察两个相邻高度 `prev`（上一次站立的位置）和 `h`（下一根已有的梯子）之间的距离 `gap = h - prev`：

- 如果 `gap ≤ dist`，直接跳过去，不需要插入。  
- 如果 `gap > dist`，我们可以在 `prev` 与 `h` 之间均匀放置新梯子，使得每段距离都 ≤ dist。  
  设需要插入 `k` 根新梯子，则会把原来的 `gap` 分成 `k+1` 段，每段的最大长度为 `ceil(gap / (k+1))`。  
  为了让每段 ≤ dist，只要满足 `gap ≤ (k+1) * dist`，即 `k ≥ (gap-1)//dist`。  
  因此最少需要的插入数量为  

\[
k = \left\lfloor \frac{gap-1}{dist} \right\rfloor
\]

这一步只用一次整数除法即可得到答案，无需循环。

- **核心算法**：**贪心 + 整除**。每一次都把「需要的最少插入数」直接算出来，保证全局最优。  
- **类比**：把两根梯子之间的距离想成一根绳子，我们只能每次抓住最多 `dist` 长度的段落。要把绳子全部抓完，只要知道绳子总长 `gap`，每次最多抓 `dist`，自然就能算出最少需要抓几次（即插几根梯子）。

#### 代码（Python）

```python
def addRungs(rungs, dist):
    """
    最优解：一次性计算每段需要插入的梯子数量
    """
    added = 0          # 统计总共需要插入的梯子数
    prev = 0           # 当前所在的高度，起点是地面 0

    for h in rungs:
        gap = h - prev                 # 两点之间的距离
        # (gap - 1) // dist 正好等于需要插入的最少梯子数
        added += (gap - 1) // dist
        prev = h                       # 跳到下一根已有的梯子

    return added
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次数组，针对每根梯子做一次常数时间的整数除法。相较于暴力版的 `while` 循环，这里不受 `gap` 大小的影响。  
- **空间复杂度**：`O(1)`  
  只使用了常数个变量。

---

## 心得

- **核心技巧**：**贪心 + 整数除法**，即把「需要插入的数量」直接用公式 `(gap-1)//dist` 计算出来。  
- **适用的题型**：  
  1. **最小补全/插入问题**（如 “Minimum Number of Refills”）。  
  2. **区间划分问题**（如 “Divide Array in Sets of K Consecutive Numbers” 中的计数）。  
  3. **步长限制的爬楼梯/跳跃问题**（如 “Frog Jump” 的变形）。  
- **一句话总结解题钥匙**：**把“逐步模拟”转化为“一次算出需要的次数”，利用整除直接得到最小插入数**。

---

## 反思

- **第一反应**：看到“只能跨距离 ≤ dist”，立刻想到逐段检查、必要时一步步插入新梯子。  
- **最容易踩的坑**：  
  - 忽略了起点是 **0**，导致第一段距离算错。  
  - 使用 `gap // dist` 而不是 `(gap-1)//dist`，会在恰好等于 `dist` 的情况下多加一根梯子。  
  - 对大数（`rungs[i]`、`dist` 可达 `10^9`）使用循环会超时。  
- **下次遇到同类题**：第一步就思考 **“每段距离需要多少次跳/插”**，尝试用 **除法/取余** 把循环次数压缩到 O(1)。这样既能保证正确性，又能得到最优的时间复杂度。