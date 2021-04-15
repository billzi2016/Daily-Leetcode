# #1298. 可以获得的最大糖果数 / Maximum Candies You Can Get from Boxes

> 难度：困难 · 标签：Array、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/maximum-candies-you-can-get-from-boxes/)

---

## 题目（英文原版）

**Description**

You have n boxes labeled from 0 to n - 1. You are given four arrays: status, candies, keys, and containedBoxes where:
You are given an integer array initialBoxes that contains the labels of the boxes you initially have. You can take all the candies in any open box and you can use the keys in it to open new boxes and you also can use the boxes you find in it.
Return the maximum number of candies you can get following the rules above.

**Examples**

**Example 1:**

```
Input: status = [1,0,1,0], candies = [7,5,4,100], keys = [[],[],[1],[]], containedBoxes = [[1,2],[3],[],[]], initialBoxes = [0]
Output: 16
Explanation: You will be initially given box 0. You will find 7 candies in it and boxes 1 and 2.
Box 1 is closed and you do not have a key for it so you will open box 2. You will find 4 candies and a key to box 1 in box 2.
In box 1, you will find 5 candies and box 3 but you will not find a key to box 3 so box 3 will remain closed.
Total number of candies collected = 7 + 4 + 5 = 16 candy.
```

**Example 2:**

```
Input: status = [1,0,0,0,0,0], candies = [1,1,1,1,1,1], keys = [[1,2,3,4,5],[],[],[],[],[]], containedBoxes = [[1,2,3,4,5],[],[],[],[],[]], initialBoxes = [0]
Output: 6
Explanation: You have initially box 0. Opening it you can find boxes 1,2,3,4 and 5 and their keys.
The total number of candies will be 6.
```

**Constraints**

- n == status.length == candies.length == keys.length == containedBoxes.length
- 1 <= n <= 1000
- status[i] is either 0 or 1.
- 1 <= candies[i] <= 1000
- 0 <= keys[i].length <= n
- 0 <= keys[i][j] < n
- All values of keys[i] are unique.
- 0 <= containedBoxes[i].length <= n
- 0 <= containedBoxes[i][j] < n
- All values of containedBoxes[i] are unique.
- Each box is contained in one box at most.
- 0 <= initialBoxes.length <= n
- 0 <= initialBoxes[i] < n

---

## 题目（中文翻译）

**描述**  
你有 `n` 个盒子，编号从 `0` 到 `n-1`。给定四个数组 `status`、`candies`、`keys` 和 `containedBoxes`，含义如下：

- `status[i]` 表示第 `i` 个盒子是否已打开，`1` 表示已打开，`0` 表示关闭。  
- `candies[i]` 表示第 `i` 个盒子中糖果的数量。  
- `keys[i]` 是一个整数数组，存放第 `i` 个盒子里可以获得的钥匙（keys），每把钥匙对应一个盒子的编号。  
- `containedBoxes[i]` 是一个整数数组，存放第 `i` 个盒子里可以获得的其他盒子（containedBoxes）的编号。

另外，给定一个整数数组 `initialBoxes`，其中存放你一开始拥有的盒子编号。  

你可以：

1. **打开**（open）任意已经打开的盒子，取走其中的所有糖果。  
2. 使用盒子里得到的钥匙（key）去打开对应的关闭盒子。  
3. 将在盒子里找到的其他盒子（containedBoxes）加入到你拥有的盒子集合中。

按照上述规则，返回你能够获得的**最大糖果数量**。

**示例 1**  
```text
Input: status = [1,0,1,0], candies = [7,5,4,100], keys = [[],[],[1],[]], containedBoxes = [[1,2],[3],[],[]], initialBoxes = [0]
Output: 16
Explanation: 初始你拥有盒子 0。打开后得到 7 颗糖果以及盒子 1 和 2。  
盒子 1 关闭且没有钥匙，所以只能打开盒子 2。打开盒子 2 后得到 4 颗糖果和一把打开盒子 1 的钥匙。  
使用钥匙打开盒子 1，得到 5 颗糖果。最终总糖果数为 7 + 4 + 5 = 16。
```

**示例 2**  
```text
Input: status = [1,0,0,0,0,0], candies = [1,1,1,1,1,1], keys = [[1,2,3,4,5],[],[],[],[],[]], containedBoxes = [[1,2,3,4,5],[],[],[],[],[]], initialBoxes = [0]
Output: 6
Explanation: 初始你拥有盒子 0。打开后可以得到盒子 1、2、3、4、5 以及它们的钥匙。  
所有盒子均可打开，糖果总数为 6。
```

**约束条件**  

- `n == status.length == candies.length == keys.length == containedBoxes.length`  
- `1 <= n <= 1000`  
- `status[i]` 只能是 `0` 或 `1`。  
- `1 <= candies[i] <= 1000`  
- `0 <= keys[i].length <= n`  
- `0 <= keys[i][j] < n`，`keys[i]` 中的所有值互不相同。  
- `0 <= containedBoxes[i].length <= n`  
- `0 <= containedBoxes[i][j] < n`，`containedBoxes[i]` 中的所有值互不相同。  
- 每个盒子至多被放在一个其他盒子中。  
- `0 <= initialBoxes.length <= n`  
- `0 <= initialBoxes[i] < n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把所有可以拿到的盒子一次一次“翻开”，每翻开一次就把：

- **糖果**拿走  
- **钥匙**收进背包（相当于把钥匙加入一个“字典”，key 是盒子编号，value 是我们是否有钥匙，字典就像查字典一样，查一次能告诉我们这把钥匙是否已经在手）  
- **里面的盒子**放进我们手里（相当于把新盒子加入“待处理列表”）

因为我们一开始只能打开**已经打开的盒子**（`status[i] == 1`），所以每次循环要遍历**所有**我们手里的盒子，检查：

1. 这盒子是否已经打开过（避免重复计数）  
2. 我们手里是否有钥匙（或者本来就是打开状态）  

只要还有**新的**盒子可以打开，就继续循环。  
这就是最直接、最笨的想法——每轮都把所有盒子扫一遍，直到再也找不到可以打开的盒子为止。

**为什么一定能得到正确答案？**  
因为每一次循环我们都会把**所有**当前能打开的盒子都打开，且打开后会把它产生的钥匙和新盒子全部加入我们的手中。只要还有未打开且可达的盒子，必然会在后面的某一次循环里被发现并打开。循环结束时，所有可达的盒子都已经被打开，得到的糖果自然是最大值。

#### 代码（Python）

```python
from typing import List

def maxCandies_bruteforce(status: List[int],
                          candies: List[int],
                          keys: List[List[int]],
                          containedBoxes: List[List[int]],
                          initialBoxes: List[int]) -> int:
    n = len(status)
    # 拥有的盒子集合（包括一开始得到的以及后面打开的盒子）
    have = set(initialBoxes)
    # 已经打开过的盒子集合，防止重复计数
    opened = set()
    # 我们拥有的钥匙集合
    have_key = set(i for i, s in enumerate(status) if s == 1)  # 本来就打开的盒子视作拥有钥匙
    total_candies = 0

    # 只要本轮有新盒子被打开，就继续循环
    changed = True
    while changed:
        changed = False
        # 遍历所有我们手里的盒子
        for box in list(have):
            # 如果已经打开过，跳过
            if box in opened:
                continue
            # 判断是否可以打开：本来就是打开的或我们已经得到钥匙
            if status[box] == 1 or box in have_key:
                # 打开盒子
                opened.add(box)
                total_candies += candies[box]          # 拿走糖果
                have_key.update(keys[box])             # 收集钥匙
                have.update(containedBoxes[box])       # 收到新盒子
                changed = True                         # 本轮有进展
    return total_candies
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  在最坏情况下，每一次循环都要遍历所有 `n` 个盒子，而循环本身最多会进行 `n` 次（每次至少打开一个新盒子），于是总操作数大约是 `n * n`。用大白话说，就是如果盒子很多，程序会像“层层筛选”一样，逐次检查每一个盒子多次，耗时会随盒子数量的平方增长。

- **空间复杂度：** `O(n)`  
  主要是用来存放 `have、opened、have_key` 这几个集合，最多各放 `n` 个盒子编号。其它辅助变量都是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每轮都要把所有盒子扫一遍，即使大多数盒子已经确认无法打开。我们可以把“只在真正需要的时候才检查”这件事交给 **广度优先搜索（BFS）** 来完成：

1. **队列**（Queue）保存「当前手里可以立即打开的盒子」。  
2. **集合** `have` 保存我们已经得到的所有盒子（不管是否已打开）。  
3. **集合** `keys` 保存我们已经得到的钥匙。  
4. **集合** `visited`（或 `opened`）记录已经打开过的盒子，防止重复打开。

**步骤**  

- 把所有 **初始拥有且已经打开** 的盒子放入队列。  
- 当队列不为空时，弹出一个盒子 `b`：  
  - 累加糖果 `candies[b]`。  
  - 把 `keys[b]` 中的钥匙加入 `keys` 集合。  
  - 把 `containedBoxes[b]` 中的盒子加入 `have` 集合。  
  - **检查**：对于我们新得到的每个盒子 `x`，如果  
    - `status[x] == 1`（本来就是打开的） **或**  
    - `x` 已经在 `keys` 集合里（我们已经拥有钥匙），  
    那么把 `x` 放进队列继续 BFS。  
- 由于每个盒子最多只会进入队列一次，整个过程只遍历一次所有 **盒子、钥匙、内部盒子** 的关系，时间就是 **线性** 的。

> **核心数据结构解释**  
> - **队列**：像排队买票一样，先打开的盒子先处理，保证我们一步步“向外扩散”。  
> - **集合（哈希表）**：查找某个盒子是否在手里、是否有钥匙，时间是 **O(1)**，相当于在字典里查词，只要把词（盒子编号）递进去，马上就能得到答案。

#### 代码（Python）

```python
from collections import deque
from typing import List

def maxCandies(status: List[int],
              candies: List[int],
              keys: List[List[int]],
              containedBoxes: List[List[int]],
              initialBoxes: List[int]) -> int:
    n = len(status)

    # 手里已有的盒子（包括初始盒子以及后面拿到的）
    have = set(initialBoxes)

    # 已经拥有的钥匙（本来打开的盒子视为已经有钥匙）
    have_key = {i for i, s in enumerate(status) if s == 1}

    # 已经打开过的盒子，防止重复计数
    opened = set()

    # 队列：当前可以立刻打开的盒子
    q = deque()

    # 把一开始就可以打开的盒子全部加入队列
    for b in initialBoxes:
        if status[b] == 1:          # 已经打开
            q.append(b)
            opened.add(b)

    total = 0

    while q:
        box = q.popleft()
        total += candies[box]               # 收集糖果

        # 收到的钥匙
        for k in keys[box]:
            if k not in have_key:
                have_key.add(k)
                # 如果我们已经拿到这个盒子且还未打开，就可以马上打开它
                if k in have and k not in opened:
                    q.append(k)
                    opened.add(k)

        # 收到的盒子
        for nb in containedBoxes[box]:
            if nb not in have:
                have.add(nb)
                # 判断是否可以立刻打开：本来是打开的或我们已有钥匙
                if status[nb] == 1 or nb in have_key:
                    if nb not in opened:
                        q.append(nb)
                        opened.add(nb)

    return total
```

#### 复杂度

- **时间复杂度：** `O(N + E)`，其中  
  - `N` 为盒子数量（最多 1000），  
  - `E` 为所有钥匙和内部盒子的总数（每个盒子最多 `n` 条边），最坏情况仍是 `O(N²)`，但在实际数据中 **每条边只会被处理一次**，所以比暴力解的 `O(N²)`（每轮全遍历）更快。用大白话说，就是我们只走一次“所有的通道”，不必反复在同一条路上来回跑。

- **空间复杂度：** `O(N)`  
  需要保存 `have、have_key、opened` 三个集合以及队列，规模都不会超过盒子数量 `N`。

---

## 心得

- **核心技巧**：**BFS + 哈希集合**，把“能立刻打开的盒子”当作图的前向层，用队列逐层扩展，确保每个盒子只被处理一次。  
- **适用场景**：  
  1. **钥匙/门** 类问题（如 LeetCode 1298 “Maximum Number of Candies You Can Get from Boxes” 本题）。  
  2. **资源获取** 类问题（如 “Keys and Rooms” 841、 “Unlock the Safe” 1635）。  
  3. **图的可达性** 问题，只要有“是否拥有”这种判断条件，都可以用相同思路。  
- **一句话总结**：**只把“当前能打开的盒子”放进队列，逐层扩散，所有可达盒子自然全部被打开，糖果自然最大**。

---

## 反思

- **第一反应**：先把所有盒子一次遍历，重复检查，直到没有新盒子可打开。  
- **最容易踩的坑**：  
  - 忘记 **去重**（同一个盒子或钥匙可能在不同盒子里出现多次），导致无限循环或重复计糖。  
  - 只检查 **初始盒子**，没有在拿到新钥匙后重新检查手中已有但尚未打开的盒子。  
  - 边界条件：`initialBoxes` 可能为空，或者所有盒子一开始都是关闭的。  
- **下次遇到同类题**：第一步先思考 **“哪些东西是我们已经拥有的，哪些是我们可以立即使用的”**，把可立即使用的放进 **队列**，随后 **“拿到新资源后立刻检查手里已有的未使用资源”**，这一步往往是突破口。