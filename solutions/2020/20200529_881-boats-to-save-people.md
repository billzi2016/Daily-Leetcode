# #881. 救生艇 / Boats to Save People

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/boats-to-save-people/)

---

## 题目（英文原版）

**Description**

You are given an array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry a maximum weight of limit. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.
Return the minimum number of boats to carry every given person.

**Examples**

**Example 1:**

```
Input: people = [1,2], limit = 3
Output: 1
Explanation: 1 boat (1, 2)
```

**Example 2:**

```
Input: people = [3,2,2,1], limit = 3
Output: 3
Explanation: 3 boats (1, 2), (2) and (3)
```

**Example 3:**

```
Input: people = [3,5,3,4], limit = 5
Output: 4
Explanation: 4 boats (3), (3), (4), (5)
```

**Constraints**

- 1 <= people.length <= 5 * 104
- 1 <= people[i] <= limit <= 3 * 104

---

## 题目（中文翻译）

你被给定一个数组 **people**，其中 `people[i]` 表示第 *i* 个人的体重（weight），还有无限数量的船（boat），每艘船的最大承载重量为 **limit**。每艘船最多同时容纳两个人，前提是这些人的体重之和不超过 **limit**。返回运送所有给定人员所需的最少船只数量。

### 示例

#### 示例 1
**输入**  
`people = [1,2]`, `limit = 3`  

**输出**  
`1`  

**解释**  
1 艘船 (1, 2)

#### 示例 2
**输入**  
`people = [3,2,2,1]`, `limit = 3`  

**输出**  
`3`  

**解释**  
3 艘船 (1, 2)、(2) 和 (3)

#### 示例 3
**输入**  
`people = [3,5,3,4]`, `limit = 5`  

**输出**  
`4`  

**解释**  
4 艘船 (3)、(3)、(4) 和 (5)

### 约束条件
- `1 <= people.length <= 5 * 10^4`
- `1 <= people[i] <= limit <= 3 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每个人都尝试和其它所有人配对**，看能否在同一艘船上。具体步骤如下：

1. **遍历**数组 `people`，对每个未被安排的人 `i`，尝试找一个还未安排的、重量和 `people[i]` 加起来 ≤ `limit` 的人 `j`。  
2. 找到这样的一对后，计数 `boats += 1`，把这两个人标记为“已上船”。  
3. 如果找不到合适的伙伴，只能单独一人上船，同样计数 `boats += 1`。  
4. 重复上述过程，直到所有人都被标记为已上船。

> **类比**：把 `people` 看成一排排的行李箱，船是装箱的箱子，每个箱子最多只能放两个行李，且总重量不能超过上限。我们把每个行李箱一个个拿出来，找能一起装进同一个箱子的另一件行李。  

**为什么这种方法一定能得到答案？**  
因为我们穷举了所有可能的配对方式（只要有人还能配，就一定配），最终每个人都会被安排进某艘船。只不过这种“穷举”方式会产生大量重复检查，效率很低。

#### 代码（Python）  

```python
from typing import List

def num_rescue_boats_bruteforce(people: List[int], limit: int) -> int:
    n = len(people)
    used = [False] * n               # 标记每个人是否已经上船
    boats = 0

    for i in range(n):
        if used[i]:                   # 已经安排好的直接跳过
            continue
        # 先假设 i 只能单独上船
        used[i] = True
        boats += 1

        # 再尝试找一个伙伴 j，使得 weight_i + weight_j ≤ limit
        for j in range(i + 1, n):
            if not used[j] and people[i] + people[j] <= limit:
                used[j] = True        # 找到配对，标记 j 已上船
                break                 # 每艘船最多两个人，配对成功后直接退出内层循环
    return boats
```

> **关键行中文注释**已经写在代码里，帮助你快速定位每一步的作用。

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - `n` 是人数。外层遍历 `n` 次，内层最坏情况下要再遍历一次剩余的 `n‑1` 人，所以整体是平方级别。  
  - 用大白话说，就是如果有 1000 个人，程序大概要做 1000×1000＝**100 万次**比较，人数一多，耗时就会暴涨。

- **空间复杂度：** `O(n)`  
  - 需要一个长度为 `n` 的布尔数组 `used` 来记录每个人是否已经上船。除此之外只用了常数级的临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于不停地在剩余的人里找配对**，导致大量重复检查。  
我们需要一种**一次遍历就能把配对关系确定下来**的方法。这里的关键技巧是**贪心 + 双指针**，思路如下：

1. **先把所有人的体重从小到大排序**。  
   - 排序后，最轻的和最重的两个人的组合最有可能“刚好”装进一艘船（因为最重的人已经占用了大部分容量，只有最轻的人才可能与之配合）。  
2. 设两个指针：`left` 指向最轻的未安排的人，`right` 指向最重的未安排的人。  
3. 每次尝试让 **最重的那个人** 上船：  
   - 如果 `people[left] + people[right] ≤ limit`，说明最重的可以和最轻的配对，两人一起上船，`left` 向右移动一位。  
   - 否则，最重的只能单独上船，`left` 不动。  
   - **无论是否配对**，`right` 都向左移动一位（因为这艘船已经用掉了最重的那个人）。  
4. 每进行一次上述操作，就使用了一艘船，计数 `boats += 1`。  
5. 当 `left > right` 时，所有人都已经安排完毕，返回 `boats`。

> **类比**：把人排成一列，从最轻的站左边，最重的站右边。每次把最右边的“胖子”送上船，如果左边的“瘦子”还能跟他一起坐，就让瘦子也上船；否则胖子只能独自上船。然后把胖子从队伍里移除，继续处理剩下的人。

**为什么贪心是最优的？**  
- 对于最重的那个人，**只有最轻的那个人** 能最大程度地降低总重量。如果连最轻的都装不下，那么这位最重的**不可能**和任何其他人配对（因为其他人都更重）。所以让最重的单独上船是唯一的最优选择。  
- 如果最轻的可以和最重的配对，那么这对配对一定不会影响后面更轻的人的配对，因为后面的人都不比最轻更轻，且船的容量已经被最大化利用。  

因此，这种每次都把“最重 + 最轻（如果可行）”的策略必然得到最少的船数。

#### 代码（Python）  

```python
from typing import List

def num_rescue_boats(people: List[int], limit: int) -> int:
    # 1. 先排序，O(n log n) 的时间开销
    people.sort()
    
    left, right = 0, len(people) - 1   # left 指向最轻，right 指向最重
    boats = 0

    while left <= right:               # 只要还有未安排的人，就继续
        # 每轮必定使用一艘船，装下最重的那个人
        boats += 1
        # 如果最轻的 + 最重的 ≤ limit，则可以一起上船
        if people[left] + people[right] <= limit:
            left += 1                   # 最轻的也被安排走了
        # 不管能否配对，最重的那个人一定已经上船
        right -= 1                      # 最重的离开队列

    return boats
```

> 代码中每一行都有中文注释，帮助你一步步跟上算法的思路。

#### 复杂度  

- **时间复杂度：** `O(n log n)`  
  - 主要耗时在排序阶段（`n log n`），之后的双指针遍历只需线性 `O(n)`，不影响整体复杂度。  
  - 用通俗的话说，如果有 10 万个人，排序大约需要 **10 万 × log₂10万 ≈ 10 万 × 17 ≈ 170 万** 次比较，比暴力的 `10万² = 1,0000,0000`（一亿次）要少很多。

- **空间复杂度：** `O(1)`（不计排序本身的原地改动）  
  - 除了几个指针变量和计数器外，只用了常数级的额外空间。  
  - 如果使用语言内部的排序会产生 `O(n)` 的临时空间，但这在 Python 中是实现细节，概念上我们只需要常数额外空间。

---

## 心得  

- **核心技巧**：**贪心 + 双指针**，先排序后两端配对。  
- **适用的题型**（类似思路）：  
  1. “最大化装箱”类问题，如 *Assign Cookies*（分配饼干）  
  2. “两数之和 ≤ target” 类的配对问题，如 *Two Sum Less Than K*（求小于 K 的两数最大和）  
  3. “最少区间覆盖” 类的贪心，如 *Jump Game II*（跳跃游戏 II）  

- **一句话总结**：**让最重的人先上船，若还能容纳最轻的人就一起上，否则只能单独上**——这一步一步把“最难安排的”先解决，剩下的自然更容易。

---

## 反思  

- **第一反应**：看到“每艘船最多两个人，重量有上限”，会想到把人两两配对，最自然的就是穷举或枚举。  
- **最容易踩的坑**：  
  - **忘记排序**：没有排序直接双指针会导致错误配对。  
  - **边界条件**：当所有人重量都等于 `limit`，每个人都只能单独上船，循环条件 `left <= right` 必须写对，否则会少算一次。  
  - **溢出/类型**：本题限制 `weight ≤ 3·10⁴`，使用 Python 的整数不会溢出，但在其他语言要注意可能的整数溢出。  

- **下次遇到同类题**，**第一步**先思考是否可以把“最极端的元素”（最大/最小）先固定，然后用 **双指针** 或 **贪心** 逐步消除极端元素，这往往能把复杂度从指数级/平方级降低到 `O(n log n)` 或 `O(n)`。