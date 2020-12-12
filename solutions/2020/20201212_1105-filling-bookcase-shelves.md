# #1105. 装满书架 / Filling Bookcase Shelves

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/filling-bookcase-shelves/)

---

## 题目（英文原版）

**Description**

You are given an array books where books[i] = [thicknessi, heighti] indicates the thickness and height of the ith book. You are also given an integer shelfWidth.
We want to place these books in order onto bookcase shelves that have a total width shelfWidth.
We choose some of the books to place on this shelf such that the sum of their thickness is less than or equal to shelfWidth, then build another level of the shelf of the bookcase so that the total height of the bookcase has increased by the maximum height of the books we just put down. We repeat this process until there are no more books to place.
Note that at each step of the above process, the order of the books we place is the same order as the given sequence of books.
Return the minimum possible height that the total bookshelf can be after placing shelves in this manner.

**Examples**

**Example 1:**

```
Input: books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]], shelfWidth = 4
Output: 6
Explanation:
The sum of the heights of the 3 shelves is 1 + 3 + 2 = 6.
Notice that book number 2 does not have to be on the first shelf.
```

**Example 2:**

```
Input: books = [[1,3],[2,4],[3,2]], shelfWidth = 6
Output: 4
```

**Constraints**

- 1 <= books.length <= 1000
- 1 <= thicknessi <= shelfWidth <= 1000
- 1 <= heighti <= 1000

---

## 题目（中文翻译）

**题目描述**

给定一个数组 `books`，其中 `books[i] = [thickness_i, height_i]` 表示第 `i` 本书的厚度（thickness）和高度（height）。同时给定一个整数 `shelfWidth`，表示每层书架的总宽度。

我们需要按照书本在数组中的顺序，将这些书依次放到书架的层上。具体过程如下：

1. 选取若干连续的书放在当前层，要求这些书的厚度之和 `≤ shelfWidth`。  
2. 为书架再建一层，当前层的高度等于本层所有书的最高高度（即这些书的 `height` 的最大值），书架的总高度因此增加该层的高度。  
3. 重复上述步骤，直到所有书都被放置完。

**要求**  
返回按照上述方式放置所有书后，书架的最小可能总高度。

**示例**

> 示例 1  
> 输入: `books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]], shelfWidth = 4`  
> 输出: `6`  
> 解释:  
> 三层书架的高度之和为 `1 + 3 + 2 = 6`。  
> 注意，第 2 本书（下标为 1 的书）不必放在第一层。

> 示例 2  
> 输入: `books = [[1,3],[2,4],[3,2]], shelfWidth = 6`  
> 输出: `4`

**约束条件**

- `1 <= books.length <= 1000`
- `1 <= thickness_i <= shelfWidth <= 1000`
- `1 <= height_i <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每本书都尝试放到每一层可能的货架上**，然后穷举所有合法的摆放方式，取最小的总高度。  

- **数据结构**：我们可以用一个 `list` 来保存当前层的书（记录每本书的厚度和高度），用另一个 `list` 记录已经放好的层的总高度。  
- **生活化类比**：把书架想象成一排排的抽屉，每个抽屉的宽度固定为 `shelfWidth`。我们把书一个接一个往抽屉里塞，**只要抽屉还能装下当前这本书，就可以继续往里放**；否则就打开新抽屉继续装。  
- **为什么正确**：因为我们遍历了**所有**可能的“什么时候换新抽屉”的决策路径，所以一定能找到最小的总高度。  

**缺点**：  
- 书的数量 `n` 最多 1000，若每本书都有两种选择（放在当前层或新开一层），总的可能性是指数级的（大约 `2^(n-1)`），根本不可接受。

#### 代码（Python）

```python
from typing import List

def minHeightShelves_bruteforce(books: List[List[int]], shelfWidth: int) -> int:
    n = len(books)

    # dfs(idx, cur_width, cur_max_h, total_h)
    # idx: 正在处理第 idx 本书
    # cur_width: 当前层已经使用的宽度
    # cur_max_h: 当前层的最高书的高度
    # total_h: 已经确定的层的总高度（不包括当前层）
    def dfs(idx, cur_width, cur_max_h, total_h):
        # 所有书都放完了，返回总高度（把最后一层也算进去）
        if idx == n:
            return total_h + cur_max_h

        w, h = books[idx]          # 当前书的厚度和高度
        # 1) 把它放到当前层（前提是宽度够）
        ans = float('inf')
        if cur_width + w <= shelfWidth:
            ans = dfs(idx + 1,
                      cur_width + w,
                      max(cur_max_h, h),   # 当前层最高高度可能升高
                      total_h)

        # 2) 开新层放这本书
        # 把已经确定的层高度加上当前层的最高高度，然后重新开始新层
        ans = min(ans, dfs(idx + 1,
                           w,                 # 新层已经放了这本书，宽度是 w
                           h,                 # 新层最高高度就是这本书的高度
                           total_h + cur_max_h))   # 把旧层的高度记进 total_h

        return ans

    # 第一本书一定放在第一层，宽度为它的厚度，高度为它的高度
    first_w, first_h = books[0]
    return dfs(1, first_w, first_h, 0)
```

> **注意**：上述代码在 `n=20` 左右就已经会超时，主要是因为它尝试了所有可能的换层方式。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级），因为每本书都有「放在当前层」或「开新层」两种选择。  
  - 大白话：如果有 30 本书，理论上要检查 `2^30 ≈ 10⁹` 种摆法，根本不可能在电脑里跑完。  
- **空间复杂度**：`O(n)`，递归栈的深度最多 `n`，每层只保存几个整数。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到**换层的决策**是唯一的瓶颈：我们每次只需要知道**从第 i 本书开始，最小的总高度是多少**。这正好符合**动态规划（DP）**的思路——把大问题拆成子问题，子问题之间有重叠。

**核心想法**：

1. **定义 dp[i]**  
   `dp[i]` 表示 **把第 i 本书到最后一本书全部放好后，书架的最小总高度**（下标从 0 开始）。我们的目标是 `dp[0]`。  

2. **状态转移**  
   考虑第 i 本书作为当前层的**第一本**，往后可以把连续的几本书都放到同一层，只要它们的厚度和不超过 `shelfWidth`。  
   - 设 `j` 为当前层的最后一本书的下标（`j ≥ i`），则第 `i…j` 本书共用一层。  
   - 这层的高度 = 这几本书的 **最大高度**（因为层高由最高的书决定）。  
   - 该层左侧已经放好的书的最小高度 = `dp[j+1]`（因为第 `j+1` 本书开始的子问题）。  
   - 因此 `dp[i] = min_{j} ( maxHeight(i..j) + dp[j+1] )`，其中 `sumWidth(i..j) ≤ shelfWidth`。  

3. **如何高效求转移**  
   - 我们从左到右遍历 `i`（从后往前计算），在内部用一个循环扩展 `j`，同时维护两件事：  
     - **累计宽度** `curWidth`：逐本加上厚度，一旦超过 `shelfWidth` 就停止扩展。  
     - **当前层最大高度** `curMaxHeight`：在遍历过程中实时取 `max(curMaxHeight, books[j][1])`。  
   - 这样每次求 `dp[i]` 的时间是 `O(k)`，其中 `k` 是从 `i` 开始向后能放的最多书本数，最坏情况 `k = n`，整体是 `O(n²)`。  

4. **边界**  
   - 当 `i == n`（已经放完所有书）时，`dp[n] = 0`（没有高度需要再加）。  

5. **类比帮助理解**  
   想象你在装箱子，每次决定“这次装多少件”。`dp[i]` 就是“从第 i 件开始，剩下的最小装箱费用”。我们尝试把第 i 件和后面几件一起装进同一个箱子（只要不超重），记录这箱子的最高费用，然后加上装完后面的最小费用。最终取最小的组合。

#### 代码（Python）

```python
from typing import List

def minHeightShelves(books: List[List[int]], shelfWidth: int) -> int:
    n = len(books)
    # dp[i] 表示把 books[i:] 放好后，书架的最小总高度
    dp = [0] * (n + 1)          # dp[n] = 0 已经放完

    # 从后往前算 dp
    for i in range(n - 1, -1, -1):
        cur_width = 0           # 当前层已使用的宽度
        cur_max_h = 0           # 当前层的最高书的高度
        best = float('inf')     # 在所有可能的 j 中取最小

        # 把第 i 本书当作本层的第一本，尝试往后放更多书
        j = i
        while j < n and cur_width + books[j][0] <= shelfWidth:
            cur_width += books[j][0]                 # 累加厚度
            cur_max_h = max(cur_max_h, books[j][1])  # 更新层最高
            # 本层高度 + 之后的最小高度
            best = min(best, cur_max_h + dp[j + 1])
            j += 1

        dp[i] = best

    return dp[0]
```

> **关键行中文注释**  
> - `cur_width += books[j][0]` # 把第 j 本书的厚度加进当前层  
> - `cur_max_h = max(cur_max_h, books[j][1])` # 当前层的最高书可能升高  
> - `best = min(best, cur_max_h + dp[j + 1])` # 本层高度 + 之后子问题的最小高度  

#### 复杂度  

- **时间复杂度**：`O(n²)`（平方级）  
  - 大白话：如果有 1000 本书，最坏要比较约 `1000 × 1000 / 2 ≈ 5×10⁵` 次，这在电脑里几毫秒就能完成。  
  - 与暴力 `O(2ⁿ)` 相比，**从指数级降到了多项式级**，大幅提升。  

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n+1` 的数组 `dp`，再加上一些常数级的临时变量。  

---

## 心得  

- **核心技巧**：**动态规划 + 前缀遍历**，把“把第 i 本书往后放多少本”这一决策抽象成子问题 `dp[i]`。  
- **适用的题型**：  
  1. **分段装箱**（如「分割数组的最大和」）  
  2. **线性顺序的最优分段**（如「把单词排版到行」）  
  3. **带宽限制的序列划分**（如「最小化路径代价」）  
- **一句话总结**：**把“从第 i 本书开始的最小高度”记下来，逐本向前回溯，尝试把后面的书一次性放进同一层**，就能得到最优解。

---

## 反思  

- **第一反应**：看到“顺序放置、宽度限制、层高取最大”，第一时间会想到“枚举每层放几本”。这直接指向 DP 的状态转移。  
- **最容易踩的坑**：  
  - **宽度累加时忘记判断上限**，导致无限循环或错误的层划分。  
  - **层高取最大**时忘记更新 `cur_max_h`，导致层高始终是第一本书的高度。  
  - **边界条件**：`dp[n] = 0` 必不可少，忘了会导致最后一层高度被多加一次。  
- **下次遇到同类题**：第一步先**明确子问题**（比如“从第 i 开始的最小代价”），再**枚举当前决策的范围**（在宽度/重量/行数限制下尽量往后扩展），用 DP 把递归转成自底向上的迭代。这样思路清晰，代码也容易写对。