# #1282. 按所属分组大小分组人员 / Group the People Given the Group Size They Belong To

> 难度：中等 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/group-the-people-given-the-group-size-they-belong-to/)

---

## 题目（英文原版）

**Description**

There are n people that are split into some unknown number of groups. Each person is labeled with a unique ID from 0 to n - 1.
You are given an integer array groupSizes, where groupSizes[i] is the size of the group that person i is in. For example, if groupSizes[1] = 3, then person 1 must be in a group of size 3.
Return a list of groups such that each person i is in a group of size groupSizes[i].
Each person should appear in exactly one group, and every person must be in a group. If there are multiple answers, return any of them. It is guaranteed that there will be at least one valid solution for the given input.

**Examples**

**Example 1:**

```
Input: groupSizes = [3,3,3,3,3,1,3]
Output: [[5],[0,1,2],[3,4,6]]
Explanation: 
The first group is [5]. The size is 1, and groupSizes[5] = 1.
The second group is [0,1,2]. The size is 3, and groupSizes[0] = groupSizes[1] = groupSizes[2] = 3.
The third group is [3,4,6]. The size is 3, and groupSizes[3] = groupSizes[4] = groupSizes[6] = 3.
Other possible solutions are [[2,1,6],[5],[0,4,3]] and [[5],[0,6,2],[4,3,1]].
```

**Example 2:**

```
Input: groupSizes = [2,1,3,3,3,2]
Output: [[1],[0,5],[2,3,4]]
```

**Constraints**

- groupSizes.length == n
- 1 <= n <= 500
- 1 <= groupSizes[i] <= n

---

## 题目（中文翻译）

**描述**  
有 `n` 个人被划分到若干未知数量的组中，每个人都有一个唯一 ID（unique ID），范围是 `0` 到 `n‑1`。  
给定一个整数数组 `groupSizes`，其中 `groupSizes[i]` 表示编号为 `i` 的人所在组的大小。例如，若 `groupSizes[1] = 3`，则编号为 `1` 的人必须在一个大小为 `3` 的组里。  

返回一个 **分组列表**（list of groups），使得每个人 `i` 所在的组大小恰好等于 `groupSizes[i]`。  
- 每个人必须恰好出现在一个组中，且所有人都必须被分配。  
- 若存在多个合法答案，返回任意一个即可。  
- 题目保证对于给定输入一定至少存在一个有效解。

**示例 1**  
**输入**: `groupSizes = [3,3,3,3,3,1,3]`  
**输出**: `[[5],[0,1,2],[3,4,6]]`  
**解释**:  
- 第一个组是 `[5]`，大小为 `1`，且 `groupSizes[5] = 1`。  
- 第二个组是 `[0,1,2]`，大小为 `3`，并且 `groupSizes[0] = groupSizes[1] = groupSizes[2] = 3`。  
- 第三个组是 `[3,4,6]`，大小为 `3`，且 `groupSizes[3] = groupSizes[4] = groupSizes[6] = 3`。  
其他合法的答案例如 `[[2,1,6],[5],[0,4,3]]`、`[[5],[...]]`（此处省略）等。

**示例 2**  
**输入**: `groupSizes = [2,1,3,3,3,2]`  
**输出**: `[[1],[0,5],[2,3,4]]`  

**约束条件**  
- `groupSizes.length == n`  
- `1 <= n <= 500`  
- `1 <= groupSizes[i] <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个人都单独放进一个组**，然后检查每个人所在的组大小是否等于 `groupSizes[i]`。如果不相等，就把两个人合并，合并后再检查。一直这样尝试所有可能的组合，直到找到一个满足所有人要求的分配。

- **使用的数据结构**  
  - **列表 `groups`**：存放所有已经形成的组，每个组本身也是一个列表。可以把它想象成「装小盒子的盒子」，每个小盒子里装的是一堆人的编号。  
  - **遍历**：我们会对 `groups` 中的每一个小盒子逐个检查，类似于在超市里一个货架一个货架地找商品。

- **为什么这个方法能得到正确答案**  
  - 暴力搜索会尝试 **所有** 可能的组合方式（虽然实际实现中会因为剪枝而不是真的遍历全部），只要有解，就一定能在搜索的某一步碰到它。  

- **时间/空间复杂度分析（大白话版）**  
  - 假设有 `n` 个人。最坏情况下我们会尝试把每个人和其他每个人配对，也就是 **“每个人和每个人都比一次”**，这相当于 `n × n` 次比较，记作 **O(n²)**。  
  - 空间上我们需要保存所有的组，最坏情况下每个人都单独成组，需要 `n` 个小列表，空间复杂度是 **O(n)**（线性空间）。

#### 代码（Python）

```python
from itertools import combinations
from copy import deepcopy

def group_the_people_bruteforce(groupSizes):
    n = len(groupSizes)
    # 初始时把每个人都单独放进一个组
    groups = [[i] for i in range(n)]

    # 递归尝试合并组
    def dfs(cur_groups):
        # 检查是否所有组都满足要求
        ok = True
        for g in cur_groups:
            sz = groupSizes[g[0]]          # 组里任意一个人的期望大小
            if len(g) != sz:                # 组的实际大小不等于期望大小
                ok = False
                break
        if ok:
            return cur_groups               # 找到合法答案

        # 找到第一个不满足的组，尝试把它和后面的组合并
        for i in range(len(cur_groups)):
            if len(cur_groups[i]) != groupSizes[cur_groups[i][0]]:
                for j in range(i + 1, len(cur_groups)):
                    # 合并后检查是否仍有可能满足（不超过期望大小）
                    merged = cur_groups[i] + cur_groups[j]
                    if len(merged) <= groupSizes[merged[0]]:
                        # 复制一份当前状态，防止递归时相互影响
                        new_groups = deepcopy(cur_groups)
                        # 删除原来的两个组，加入合并后的组
                        new_groups.pop(j)
                        new_groups.pop(i)
                        new_groups.append(merged)
                        ans = dfs(new_groups)
                        if ans:                # 只要找到一个合法答案就返回
                            return ans
                # 如果没有任何合并方式可以让第 i 组合法，则此分支必定失败
                return None
        return None

    return dfs(groups)

# 示例
print(group_the_people_bruteforce([3,3,3,3,3,1,3]))
```

> **注意**：上述代码仅用于演示“暴力思路”，在 `n` 较大（如 100）时会非常慢，实际使用请参考下面的最优解。

#### 复杂度

- **时间复杂度**：`O(n²)`（每个人可能和其他每个人配对检查）  
  > 这里的 `n²` 可以理解为“如果你有 100 个人，最多会进行 10,000 次配对尝试”。  
- **空间复杂度**：`O(n)`（保存所有人的编号）  
  > 只需要把每个人的 ID 存下来，最多和人数成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于不停地尝试把组合并，导致大量不必要的搜索。实际上，题目已经告诉我们每个人的 **期望组大小**，我们只需要把 **相同期望大小的人成为一类**，然后在每一类内部**按需划分**即可。

1. **把相同 `groupSize` 的人放进同一个桶**  
   - 想象有若干个抽屉（桶），抽屉的编号就是“期望的组大小”。  
   - 当我们遍历 `groupSizes` 时，把人的 ID 放进对应抽屉里。这个过程类似于“把单词放进字典的对应页码”，字典的 **key** 是组大小，**value** 是这个大小下的所有人。

2. **在每个抽屉里切分成若干完整的组**  
   - 抽屉里的人数一定是 `groupSize` 的整数倍（题目保证有解），所以我们只要 **每满 `groupSize` 个人就形成一个完整的组**。  
   - 这一步可以一次遍历抽屉列表，用 **切片** 或 **弹出** 的方式把前 `groupSize` 个人取出来，放进答案中。

3. **贪心**（Greedy）  
   - “每满 `groupSize` 就立刻成组” 是一种 **贪心** 做法，因为我们永远不会因为提前成组而导致后面无法完成。  
   - 直观解释：如果你已经有 3 个人都说自己想要 3 人的团队，那么无论后面再出现多少人想要 3 人的团队，这 3 个人已经可以幸福地在一起了，等不及再等下去。

> **关键点**：只需要一次遍历 `groupSizes`（O(n)），并在每个桶内部再次遍历（总体也是 O(n)），因此整体线性时间即可完成。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def group_the_people(groupSizes: List[int]) -> List[List[int]]:
    """
    1. 用哈希表（defaultdict）把相同 groupSize 的人放进同一个桶
    2. 每当桶里的人数达到 groupSize，就取出这些人组成一个完整的组
    """
    # step1：建立 bucket，key = 需要的组大小，value = 该大小下的人的编号列表
    buckets = defaultdict(list)          # 类比：字典的 key 是“页码”，value 是“本页的单词”

    for person_id, size in enumerate(groupSizes):
        buckets[size].append(person_id)   # 把人放进对应的抽屉

    answer = []                           # 最终返回的所有组

    # step2：遍历每个抽屉，按 size 把人划分成完整的组
    for size, people in buckets.items():
        # people 可能很多，需要每 size 个人切成一组
        # 采用 while 循环弹出前 size 个人
        while people:
            # 取出前 size 个人，形成一个新组
            group = people[:size]        # 切片得到一个新列表
            answer.append(group)         # 加入答案
            # 删除已经使用的这些人，准备处理剩下的
            del people[:size]            # 原地删除，保持列表短小

    return answer

# 示例
if __name__ == "__main__":
    print(group_the_people([3,3,3,3,3,1,3]))   # [[5], [0,1,2], [3,4,6]] 或其他合法解
    print(group_the_people([2,1,3,3,3,2]))     # [[1], [0,5], [2,3,4]]
```

> **代码要点注释**  
> - `defaultdict(list)`：如果某个组大小第一次出现，字典会自动创建一个空列表，省去 `if size not in buckets` 的判断。  
> - `enumerate(groupSizes)` 同时得到人的编号 `person_id`（相当于身份证号）和他想要的组大小 `size`。  
> - `while people:` 循环确保把同一抽屉里的所有人全部划分完。  
> - `del people[:size]` 是一种 **原地删除** 的技巧，避免每次都创建新列表，节省空间。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历了一遍输入数组（把人放进桶），再遍历每个桶一次，总操作次数不超过 `2n`。  
  - 与暴力解的 `O(n²)` 相比，线性时间就像“把 100 本书一次性全部搬走”，而不是“一本一本搬”。

- **空间复杂度**：`O(n)`  
  - 需要额外的哈希表存放每个人的编号，总数正好是 `n`，与输入规模相同。  
  - 与暴力解的空间相同，但没有额外的递归栈或深拷贝，使用更少的临时内存。

---

## 心得

- **核心技巧**：利用**哈希表（字典）进行分桶 + 贪心切分**。  
- **适用的题型**  
  1. “按属性分组” 类题目，如 *将数组分成相同长度的子数组*。  
  2. “按频次/计数分配” 类题目，如 *分配任务到工作机器*（每台机器负载相同）。  
  3. “分桶 + 切片” 类题目，如 *把字符串按字符出现次数划分*。  
- **一句话总结解题钥匙**：**把相同需求的元素先聚在一起，再一次性按需求大小切割**。

---

## 反思

- **第一反应**：看到每个人都有“想要的组大小”，自然想到“先把相同大小的人放一起”。  
- **最容易踩的坑**  
  - 忽略 **“每个抽屉里的人数一定是 size 的倍数”** 这一点，导致在切分时出现剩余人数不足的情况。  
  - 在实现时忘记 **原地删除** 已经组成的组，导致同一批人被重复使用。  
- **下次遇到同类题**：**先建立“需求 → 元素列表”的映射（哈希表），再按需求大小一次性划分**，这一步几乎是所有“分组”题的通用模板。