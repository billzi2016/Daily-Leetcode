# #1046. 最后一块石头的重量 / Last Stone Weight

> 难度：简单 · 标签：Array、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/last-stone-weight/)

---

## 题目（英文原版）

**Description**

You are given an array of integers stones where stones[i] is the weight of the ith stone.
We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:
At the end of the game, there is at most one stone left.
Return the weight of the last remaining stone. If there are no stones left, return 0.

**Examples**

**Example 1:**

```
Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation: 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.
```

**Example 2:**

```
Input: stones = [1]
Output: 1
```

**Constraints**

- 1 <= stones.length <= 30
- 1 <= stones[i] <= 1000

---

## 题目（中文翻译）

你将得到一个整数数组 `stones`，其中 `stones[i]` 表示第 `i` 块石头的重量。  
我们在玩一个游戏，每回合选择最重的两块石头并将它们撞击（smash）在一起。  
设这两块石头的重量分别为 `x` 和 `y`，且 `x <= y`。撞击的结果如下：

- 若 `x == y`，则这两块石头都被销毁；
- 否则，重量为 `y - x` 的石头会留下，其余石头保持不变。

游戏结束时至多会剩下一块石头。返回最后剩余石头的重量；如果所有石头都被销毁，返回 `0`。

## 示例

### 示例 1

**输入**  
``` 
stones = [2,7,4,1,8,1]
```  

**输出**  
```
1
```  

**解释**  
我们先把重量为 `7` 和 `8` 的两块石头撞击，得到 `1`，数组变为 `[2,4,1,1,1]`；  
接着撞击 `2` 和 `4`，得到 `2`，数组变为 `[2,1,1,1]`；  
再撞击 `2` 和 `1`，得到 `1`，数组变为 `[1,1,1]`；  
然后撞击 `1` 和 `1`，得到 `0`，数组变为 `[1]`，这就是最后剩下的石头的重量。

### 示例 2

**输入**  
``` 
stones = [1]
```  

**输出**  
```
1
```  

## 约束条件

- `1 <= stones.length <= 30`
- `1 <= stones[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **每一次都把所有石头排序，取出最大的两个**，按照题目规则把它们撞碎后把新产生的石头（如果有的话）再放回去，重复这个过程直到只剩下 0 或 1 块石头。  

- **用到的数据结构**：  
  - `list`（数组）存放石头的重量。  
  - `sort`（排序）相当于把石头从轻到重排好，**就像把一本字典的单词按字母顺序排好**，我们只需要直接取最后两个（最重的）就行。  

- **为什么正确**：  
  - 题目每一步都要求“选出当前最重的两块石头”。把所有石头排序后，数组最后两个元素恰好是这两块。  
  - 计算撞击后的新重量（`y - x`），如果不为 0，就把它再放回数组中继续后面的轮次。这样完全模拟了题目描述的过程，最终得到的剩余重量一定是唯一正确的答案。  

- **复杂度分析（大白话）**：  
  - `sort` 的时间代价大约是 **n log n**（比如 30 块石头排序一次，大概相当于把 30 张卡片按大小重新排好，需要的比较次数随 `log` 增长）。  
  - 最坏情况下我们可能要进行 **n‑1 次**（每次至少消掉一块石头），所以总体时间是 **O(n² log n)**，因为每次都要重新排序。  
  - 空间上我们只用原来的数组，外加常数级的临时变量，**O(1)**（不计输入本身的空间）。  

#### 代码（Python）

```python
from typing import List

def lastStoneWeight_bruteforce(stones: List[int]) -> int:
    """
    暴力解：每轮都排序，取最大的两块石头撞击
    """
    while len(stones) > 1:                # 只要还有两块以上的石头就继续
        stones.sort()                     # 把石头从小到大排好
        y = stones.pop()                  # 取出最重的石头 y（相当于字典里最后一页）
        x = stones.pop()                  # 再取出次重的石头 x
        if y != x:                         # 如果两块重量不相同，剩下的重量是 y - x
            stones.append(y - x)           # 把新石头放回数组，准备下一轮
        # 若 y == x，撞击后直接消失，不需要再放回
    return stones[0] if stones else 0      # 最后可能剩一块，也可能全消失
```

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 想象每次都要把 30 张卡片重新排好，排一次是 `n log n`，最多要排 `n` 次，整体就是 `n * n log n`。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个临时变量，额外占用的内存可以忽略不计。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每轮都要重新排序**。我们其实只需要**快速取出当前最大的两块石头**，不必把全部石头重新排好。  

**优先队列（堆）** 正好能帮我们做到这点：  
- 堆是一棵满足“父节点 ≥ 子节点”（大根堆）或 “父节点 ≤ 子节点”（小根堆）性质的二叉树。  
- 在 **大根堆** 中，根节点始终是最大的元素，**取出最大值的时间是 O(log n)**，而不是 O(n)。  

实现细节（Python 中的 `heapq` 默认是小根堆）：

1. 为了让 `heapq` 当“大根堆”用，我们把所有石头的重量取相反数（负数），这样“最小的负数”对应的原始重量最大。  
2. 把所有负数放进堆，调用 `heapify` 一次即可完成 **O(n)** 的建堆。  
3. 循环：  
   - `heappop` 两次得到最大的两块石头（其实是最小的两个负数），记为 `y`、`x`（取相反数恢复正数）。  
   - 如果 `y != x`，把 `y - x` 再取相反数放回堆中。  
4. 循环结束后，堆里可能还有一块石头（负数），返回其相反数；若堆空返回 0。  

这样每次操作只需要 **O(log n)**，整个过程最多进行 `n‑1` 次，时间复杂度降到 **O(n log n)**，空间仍然是 **O(n)**（存放堆本身）。  

> **类比**：想象有一个装满不同重量的石头的背包，我们每次只需要找出最重的两块并拿走。用堆相当于在背包里装了一个“自动称重的天平”，每次只要轻轻一拉，就能直接把最重的两块石头递给我们，而不必把所有石头都搬出来重新称一遍。  

#### 代码（Python）

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    """
    最优解：使用大根堆（通过存负数的方式实现）快速取出最大两块石头
    """
    # 1. 把所有石头的重量取负数，放进列表
    max_heap = [-w for w in stones]   # 负数越大（接近 0），原始重量越小
    heapq.heapify(max_heap)           # O(n) 建堆，得到“大根堆”

    # 2. 循环直到堆里剩不到两块石头
    while len(max_heap) > 1:
        y = -heapq.heappop(max_heap)   # 取出最重的石头 y（恢复正数）
        x = -heapq.heappop(max_heap)   # 再取出次重的石头 x
        if y != x:                     # 只要两块重量不相等，就会产生新石头
            heapq.heappush(max_heap, -(y - x))  # 把新石头的负数放回堆

    # 3. 处理剩余结果
    return -max_heap[0] if max_heap else 0   # 如果堆非空，取负数恢复正数
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 建堆一次 `O(n)`，随后每次取出两块石头和可能的插入操作都是 `O(log n)`，最多进行 `n‑1` 次，整体是 `n log n`。与暴力解相比，从“每轮都重新排”降到了“每轮只动几次”。  
- **空间复杂度**：`O(n)`  
  - 堆里最多存放所有石头的负数，需要与输入大小同量级的额外空间。  

---  

## 心得  

- **核心技巧**：使用**堆（优先队列）** 在动态集合中快速取出最大（或最小）元素。  
- **适用的题型**：  
  1. “合并最小/最大成本” 类题，如 **合并石头的最小成本**（LC 1000），**最小生成树** 中的 Prim 算法。  
  2. “寻找第 K 大/小元素” 如 **Kth Largest Element in an Array**（LC 215）。  
  3. “滑动窗口最大值” 等需要维护窗口内极值的题目。  
- **一句话总结解题钥匙**：**把“每次都要找最大” 的需求交给堆，让它替你省去一次次的全排序**。  

---  

## 反思  

- **第一反应**：看到“每回合选出最大两块石头”，立刻想到**排序**，因为排序后直接取最后两个最方便。  
- **最容易踩的坑**：  
  - 忘记把堆中的负数恢复成正数返回，导致答案是负的。  
  - 当两块石头重量相等时，撞击后会产生 0，需要 **不把 0 放回堆**，否则会多出无意义的“石头”。  
  - 边界情况：只有一块石头或全部石头都相同消光，代码必须能返回 0 或该唯一石头的重量。  
- **下次遇到同类题的第一步**：先判断“是否需要频繁获取集合中的极值”。如果是，就立即考虑 **堆**（或双指针、单调队列等对应的数据结构），而不是直接排序或遍历。