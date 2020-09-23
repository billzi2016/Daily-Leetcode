# #997. 寻找镇上的法官 / Find the Town Judge

> 难度：简单 · 标签：Array、Hash Table、Graph · [LeetCode 链接](https://leetcode.com/problems/find-the-town-judge/)

---

## 题目（英文原版）

**Description**

In a town, there are n people labeled from 1 to n. There is a rumor that one of these people is secretly the town judge.
If the town judge exists, then:
You are given an array trust where trust[i] = [ai, bi] representing that the person labeled ai trusts the person labeled bi. If a trust relationship does not exist in trust array, then such a trust relationship does not exist.
Return the label of the town judge if the town judge exists and can be identified, or return -1 otherwise.

**Examples**

**Example 1:**

```
Input: n = 2, trust = [[1,2]]
Output: 2
```

**Example 2:**

```
Input: n = 3, trust = [[1,3],[2,3]]
Output: 3
```

**Example 3:**

```
Input: n = 3, trust = [[1,3],[2,3],[3,1]]
Output: -1
```

**Constraints**

- 1 <= n <= 1000
- 0 <= trust.length <= 104
- trust[i].length == 2
- All the pairs of trust are unique.
- ai != bi
- 1 <= ai, bi <= n

---

## 题目（中文翻译）

在一个镇子里，有 `n` 个人，编号为 `1` 到 `n`。传闻其中有一个人暗中是镇上的法官。  
如果镇上的法官存在，则：

- 法官**不信任**任何人（即在 `trust` 数组中没有以法官为第一元素的记录）。
- 所有除法官之外的其他人**都信任**法官（即每个其他人都有一条 `[ai, bi]`，其中 `bi` 为法官的编号）。

给定一个二维数组 `trust`，其中 `trust[i] = [ai, bi]` 表示编号为 `ai` 的人信任编号为 `bi` 的人。如果 `trust` 数组中不存在某对关系，则表示该信任关系不存在。  
返回镇上法官的编号；如果不存在满足条件的法官，或无法唯一确定，则返回 `-1`。

### 示例

**示例 1**  
输入: `n = 2, trust = [[1,2]]`  
输出: `2`

**示例 2**  
输入: `n = 3, trust = [[1,3],[2,3]]`  
输出: `3`

**示例 3**  
输入: `n = 3, trust = [[1,3],[2,3],[3,1]]`  
输出: `-1`

### 约束条件

- `1 <= n <= 1000`
- `0 <= trust.length <= 10^4`
- `trust[i].length == 2`
- 所有信任对均唯一。
- `ai != bi`
- `1 <= ai, bi <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把每个人都当成可能的“法官”，然后逐一检查是否满足题目给出的两条条件  

1. **不相信任何人**：这个人不能出现在 `trust` 数组的左边（即 `ai`）。  
2. **被所有其他人信任**：除了自己以外的 `n‑1` 个人，都必须出现在 `trust` 数组的右边（即 `bi`）。

我们可以用两层循环来完成检查：

- 外层遍历每个候选人 `candidate`（从 1 到 n）。  
- 内层遍历 `trust` 数组，统计 `candidate` 是否出现在左边、右边，进而判断是否满足上面的两个条件。

如果某个人通过了检查，就直接返回他的编号；如果所有人都不符合，则返回 `-1`。

> **数据结构类比**：`trust` 就像一本“谁信任谁”的小册子，左边是“信任的人”，右边是“被信任的人”。我们要逐页翻，看每个人是否从未在左边出现，却在右边出现了 `n‑1` 次。

#### 代码（Python）

```python
from typing import List

def findJudge_brute(n: int, trust: List[List[int]]) -> int:
    # 暴力枚举每一个可能的法官 candidate
    for candidate in range(1, n + 1):
        trusts_someone = False   # candidate 是否相信别人
        trusted_by_cnt = 0       # 被多少人信任

        # 遍历所有信任关系
        for a, b in trust:
            if a == candidate:               # candidate 出现在左边 → 他相信别人
                trusts_someone = True
            if b == candidate:               # candidate 出现在右边 → 被某人信任
                trusted_by_cnt += 1

        # 判断是否满足法官的两个条件
        if not trusts_someone and trusted_by_cnt == n - 1:
            return candidate   # 找到法官，直接返回

    return -1  # 没有符合条件的人
```

#### 复杂度

- **时间复杂度**：`O(n * m)`，其中 `n` 是人数，`m = len(trust)` 是信任关系的条数。因为我们对每个候选人都要遍历一遍全部关系。  
  - **大白话**：如果有 1000 个人、10000 条关系，最坏情况下要检查 1000 × 10000 = 1,000 万次，算起来有点慢。

- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（计数器、布尔值），不随输入规模增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次检查都要遍历完整的 `trust` 列表**，导致 `O(n·m)`。我们可以把遍历的工作一次性完成，用**计数**的方式直接得到每个人的“信任出度”和“被信任入度”。  

- 对每个人 `i`，维护一个整数 `score[i]`：  
  - 当 `i` **相信** `j` 时，`score[i]` 减 1（因为法官不能相信任何人）。  
  - 当 `i` **被** `j` **信任** 时，`score[i]` 加 1（因为法官必须被所有其他人信任）。  

这样遍历完 `trust` 只需要 **一次**（`O(m)`），最后只要找出 `score[i] == n-1` 的人即可——  
- `+ (n-1)` 表示被 `n-1` 个人信任。  
- `- 0` 表示没有相信任何人。  

> **数据结构类比**：把每个人想象成一个天平的砝码，左边放“相信别人的负重”，右边放“被别人信任的正重”。法官的天平最终只剩下右边的正重 `n-1`，左边为空。

#### 代码（Python）

```python
from typing import List

def findJudge(n: int, trust: List[List[int]]) -> int:
    # 用一个长度为 n+1 的数组记录每个人的得分（下标 0 不使用，直接对应编号）
    score = [0] * (n + 1)

    # 只遍历一次 trust 列表
    for a, b in trust:
        score[a] -= 1   # a 相信别人，得分减一
        score[b] += 1   # b 被别人信任，得分加一

    # 检查是否存在得分恰好为 n-1 的人
    for person in range(1, n + 1):
        if score[person] == n - 1:
            return person

    return -1  # 没有满足条件的法官
```

#### 复杂度

- **时间复杂度**：`O(n + m)`。  
  - 第一次遍历 `trust` 用 `O(m)`，第二次遍历人数数组用 `O(n)`。这在最坏情况下仍然远小于暴力的 `O(n·m)`。  
  - **大白话**：如果 `n=1000`、`m=10000`，只需要大约 11000 次操作，几乎瞬间完成。

- **空间复杂度**：`O(n)`。我们用了一个长度为 `n+1` 的数组 `score`，随着人数线性增长。相比于暴力的 `O(1)`，这里稍多一点，但在本题的约束（n ≤ 1000）下完全可以接受。

---

## 心得

- **核心技巧**：**计数差分**（入度 - 出度）——把“相信”和“被信任”这两件事用加减同一个数组统一记录，最后只看哪个人的得分恰好是 `n‑1`。  
- **适用的题型**：  
  1. **找出图中唯一的“中心节点”**（如 LeetCode 997 Find the Town Judge、LeetCode 2050 Parallel Courses III）。  
  2. **统计入度/出度判断环或路径**（如 LeetCode 207 Course Schedule）。  
  3. **投票、推荐系统的“得票最高者”**（如 LeetCode 1512 Number of Good Pairs）。  
- **一句话总结**：把“谁信任谁”转化为“每个人的得分”，得分最高且恰为 `n‑1` 的就是法官。

---

## 反思

- **第一反应**：看到“每个人不信任任何人、被所有人信任”，立刻想到枚举检查——这就是暴力解。  
- **最容易踩的坑**：  
  - `n = 1` 且 `trust = []` 时，唯一的居民本身就是法官，需要额外判断。  
  - 输入中可能出现 **自环**（`ai == bi`）的非法情况，题目已保证不存在，但实际面试时最好防御性检查。  
  - 当 `trust` 为空且 `n > 1` 时，显然没有法官，也要返回 `-1`。  
- **下次思路**：遇到“所有人都指向同一个人”或“每个人的进出度都有特殊要求”时，第一步就想到 **用入度/出度计数数组**，把关系压缩成 O(n) 的信息，再做一次线性扫描即可。