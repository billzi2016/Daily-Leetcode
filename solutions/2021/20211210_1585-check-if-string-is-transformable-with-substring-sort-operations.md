# #1585. 判断字符串是否可以通过子串排序操作转换 / Check If String Is Transformable With Substring Sort Operations

> 难度：困难 · 标签：String、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/check-if-string-is-transformable-with-substring-sort-operations/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, transform string s into string t using the following operation any number of times:
Return true if it is possible to transform s into t. Otherwise, return false.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "84532", t = "34852"
Output: true
Explanation: You can transform s into t using the following sort operations:
"84532" (from index 2 to 3) -> "84352"
"84352" (from index 0 to 2) -> "34852"
```

**Example 2:**

```
Input: s = "34521", t = "23415"
Output: true
Explanation: You can transform s into t using the following sort operations:
"34521" -> "23451"
"23451" -> "23415"
```

**Example 3:**

```
Input: s = "12345", t = "12435"
Output: false
```

**Constraints**

- s.length == t.length
- 1 <= s.length <= 105
- s and t consist of only digits.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，可以无限次使用以下操作将字符串 `s` 转换为字符串 `t`：  
选择 `s` 中的任意子串（substring），对该子串进行**升序排序**后替换原位置。  
如果可以将 `s` 转换为 `t`，返回 `true`；否则返回 `false`。

**子串（substring）** 是字符串中连续的一段字符序列。

### 示例

#### 示例 1
**输入**: `s = "84532", t = "34852"`  
**输出**: `true`  
**解释**: 可以通过以下排序操作将 `s` 转换为 `t`：  
1. 对下标 `[2, 3]` 的子串进行排序  
   `"84532"` → `"84352"`  
2. 对下标 `[0, 2]` 的子串进行排序  
   `"84352"` → `"34852"`

#### 示例 2
**输入**: `s = "34521", t = "23415"`  
**输出**: `true`  
**解释**: 可以通过以下排序操作将 `s` 转换为 `t`：  
1. `"34521"` → `"23451"`  
2. `"23451"` → `"23415"`

#### 示例 3
**输入**: `s = "12345", t = "12435"`  
**输出**: `false`

### 约束条件
- `s.length == t.length`
- `1 <= s.length <= 10^5`
- `s` 和 `t` 只包含数字字符。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的子串排序操作都枚举一遍**，看能不能把 `s` 变成 `t`。  
可以把每一次操作看成一次“状态转移”：  

* 当前状态 = 一个字符串（比如 `"84532"`）  
* 选一个子串 `[l, r]`（下标连续），把它 **升序排序**，得到新的字符串（比如把下标 2~3 的 `"53"` 排序成 `"35"`，得到 `"84352"`）  

把这些状态连成一张图，用 **宽度优先搜索（BFS）** 从起点 `s` 开始，一层层展开所有可能的下一步，直到找到 `t` 为止，或者所有状态都已经访问完仍未找到，说明不可达。

> **类比**：把每个字符串想象成一本书的页面，翻页的顺序只能是把相邻的几页重新排好顺序后放回去。我们想知道能不能通过一次次这样“重新排页”把原书变成目标书。

**为什么这种方法一定能得到正确答案？**  
因为 BFS 会遍历**所有**合法的操作序列（只要不超出题目给出的长度限制），只要有一种方式能够把 `s` 变成 `t`，必然会在搜索过程中遇到。

**为什么不推荐直接使用？**  
- 对每个字符串长度为 `n`，子串的选择有 `O(n²)` 种，排序子串本身是 `O(k log k)`（`k` 为子串长度）。  
- BFS 需要把每个产生的字符串都放进队列并去重，最坏情况下会产生 **指数级**（`2^n`、`n!`）的状态。  
- 当 `n` 甚至只有 10 时，状态数已经会爆炸，远远超出计算资源。

> **时间复杂度** 中的 `O(2ⁿ)`、`O(n!)` 并不是说真的会跑到 2 的 n 次方这么多，而是 **数量级** 超出了我们能接受的范围。  
> **空间复杂度** 同理，需要存储所有已经访问过的状态，也会指数级增长。

下面给出一个 **仅用于演示**（只能在 `n ≤ 8` 左右的小样例上跑）的实现，帮助大家直观感受暴力搜索的思路。

#### 代码（Python）

```python
from collections import deque

def can_transform_bruteforce(s: str, t: str) -> bool:
    """
    暴力 BFS 实现，仅适用于长度很小的情况（如 n ≤ 8）。
    每一步：枚举所有子串 [l, r]，对其进行升序排序，得到新字符串。
    """
    if s == t:
        return True

    n = len(s)
    # 用集合记录已经访问过的字符串，防止无限循环
    visited = {s}
    q = deque([s])

    while q:
        cur = q.popleft()
        # 枚举所有子串
        for l in range(n):
            for r in range(l, n):
                # 取子串并排序
                sub = ''.join(sorted(cur[l:r+1]))
                nxt = cur[:l] + sub + cur[r+1:]
                if nxt == t:          # 找到目标
                    return True
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
    # BFS 结束仍未找到
    return False


# ------------------- 示例 -------------------
print(can_transform_bruteforce("84532", "34852"))  # True
print(can_transform_bruteforce("34521", "23415"))  # True
print(can_transform_bruteforce("12345", "12435"))  # False
```

> **关键注释**  
> - `visited` 像一本“查字典”，记录每个已经出现的字符串（key），避免重复搜索。  
> - `sorted(cur[l:r+1])` 把子串升序排列，正是题目允许的操作。  
> - 双层 `for` 循环遍历所有 **连续** 子串 `[l, r]`，相当于把每一次“翻页”都尝试一次。

#### 复杂度

- **时间复杂度**：`O( C * n² * n log n )`（`C` 为实际遍历的状态数），在最坏情况下是指数级 `O(2ⁿ)`，因为状态会呈指数增长。  
  > 大白话：随着字符串长度稍微长一点，搜索的时间会“炸裂”，很快就跑不完。
- **空间复杂度**：`O(C * n)`，需要把所有已经访问的字符串都存下来，同样是指数级的空间消耗。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈在于状态的爆炸**：我们不需要真的去枚举所有子串，只要判断是否 **能够** 把字符移动到目标位置即可。  

**观察 1：**  
一次子串升序排序只能把 **更小的字符** 移到左边，把 **更大的字符** 移到右边。也就是说，**相对顺序** 会被“局部化”地变成非递减的。

**观察 2：**  
如果我们从左到右一次决定 `t` 中的每个字符应该取自 `s` 的哪一个位置，那么只要在取到该字符之前，没有**更小的字符**仍然停留在它左边，就一定可以通过若干次子串排序把它拉到这里。  

> 类比：想象一排小球，每个小球上写着数字。我们只能把一段连续的小球 **重新排成从小到大的顺序**。如果我们想把一个数字 `5` 拉到最左边，必须确保它左边没有 `1~4` 的小球，因为排序只会把这些更小的数字 **推到左边**，而不会让它们“让路”给 `5`。

**关键结论**  
遍历目标字符串 `t`，对每个字符 `d`：

1. 在原字符串 `s` 中找出 **最左边还未使用** 的 `d`（记为下标 `pos`）。  
2. 检查所有比 `d` 小的字符（`0 … d-1`）中，是否还有未使用的、且位置 **在 `pos` 左侧** 的。如果有，说明这些更小的字符卡在 `d` 前面，无法让 `d` 前移——**转化失败**。  
3. 否则，使用这个 `pos`（把它标记为已用），继续处理下一个目标字符。

实现细节：

- 为每个数字 `0‑9` 建立一个 **队列（deque）**，把它在 `s` 中出现的下标依次放进去。队列的左端始终是当前最左边未使用的下标，弹出时用 `popleft()`。  
- 在处理 `t[i] = d` 时，只需要检查 **10 个队列** 中 **比 `d` 小的** 那些的首元素是否小于 `pos`。这一步是 `O(10)`，即常数时间。  

整个过程遍历 `t` 一遍，时间 `O(n)`，空间存储下标的总数也是 `O(n)`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def can_transform(s: str, t: str) -> bool:
    """
    贪心 + 队列（deque）实现。
    思路：从左到右匹配 t 中的字符，保证在取到当前字符之前
          没有更小的字符停在它左边。
    """
    if len(s) != len(t):
        return False

    # 1. 为每个数字 0~9 建立一个队列，存放它们在 s 中出现的下标（从左到右）
    pos: List[deque] = [deque() for _ in range(10)]
    for idx, ch in enumerate(s):
        digit = int(ch)                # 把字符转成整数，方便比较大小
        pos[digit].append(idx)         # 把下标加入对应的队列

    # 2. 依次遍历目标字符串 t
    for ch in t:
        d = int(ch)                    # 目标字符的数字值

        # 2.1 如果 s 中已经没有未使用的 d，说明无法匹配
        if not pos[d]:
            return False

        # 2.2 取出最左边的 d 的位置
        cur_idx = pos[d].popleft()

        # 2.3 检查所有更小的数字，它们的最左下标是否在 cur_idx 左侧
        for smaller in range(d):       # 0 ~ d-1
            if pos[smaller] and pos[smaller][0] < cur_idx:
                # 存在更小的字符卡在左边，d 无法前移
                return False

        # 如果检查通过，说明 cur_idx 这个 d 可以被“拉到”当前的位置
        # 继续匹配下一个字符
    return True


# ------------------- 示例 -------------------
print(can_transform("84532", "34852"))  # True
print(can_transform("34521", "23415"))  # True
print(can_transform("12345", "12435"))  # False
```

**代码要点解读**

| 行号 | 关键代码 | 中文注释（帮助理解） |
|------|----------|-------------------|
| 5‑7 | `pos = [deque() for _ in range(10)]` | 为 0‑9 共十个数字准备十条“排队通道”。 |
| 8‑10| `pos[digit].append(idx)` | 把每个字符出现的下标依次放进对应的通道，左边的下标先进。 |
| 14‑16| `if not pos[d]: return False` | 没有剩余的目标字符 → 无法完成转换。 |
| 19   | `cur_idx = pos[d].popleft()` | 取出 **最左** 的 `d`，因为只有它最有可能被移动到最前面。 |
| 22‑25| `for smaller in range(d): ...` | 检查所有比 `d` 小的数字的最左下标是否在 `cur_idx` 左侧。 |
| 27   | `return False` | 发现更小的字符卡在左边，说明 `d` 不能前移，直接判负。 |
| 31   | `return True` | 全部匹配成功，说明可以通过若干子串排序得到 `t`。 |

#### 复杂度

- **时间复杂度**：`O(n * 10) = O(n)`  
  - 只遍历一次目标字符串 `t`（长度 `n`）。  
  - 每一步最多检查 10 个队列的首元素（常数 10），所以整体是线性。  
  - 与暴力解的指数级相比，几乎是“瞬间完成”。  

- **空间复杂度**：`O(n)`  
  - 需要把 `s` 中每个字符的下标存进对应的队列，总共恰好 `n` 个下标。  
  - 除此之外只使用了常数级的额外变量。

> **对比**：  
> - 暴力解需要 `O(2ⁿ)`（甚至更高）时间和空间，根本不可行。  
> - 最优解只用 `O(n)`，即使 `n = 10⁵` 也能在毫秒级跑完。

---

## 心得  

- **核心技巧**：**贪心 + 位置队列**  
  - 关键是“最左边的字符先用”，并且**保证没有更小的字符阻塞**。  
- **适用场景**（类似题目）  
  1. **LeetCode 1650. Low‑est Common Ancestor of a Binary Tree**（不直接相关，但需要“从左到右的贪心”思路）。  
  2. **LeetCode 1730. Shortest Path to Get All Keys**（使用状态队列进行 BFS，但仍需判断可达性）。  
  3. **LeetCode 2399. Check Distances Between Same Letters**（利用下标队列检查约束）。  
- **一句话总结解题钥匙**：**“左边只能出现更小的字符，先把每个字符的最左位置取出来，确保没有更小字符挡路即可”。**

---

## 反思  

- **第一反应**：看到“子串排序”，第一时间会想到“暴力枚举所有子串”。这在概念上是自然的，但很快会发现搜索空间爆炸。  
- **最容易踩的坑**  
  1. **忘记检查更小字符的阻塞**：仅判断 `s` 中是否还有对应字符是不够的，需要比较相对位置。  
  2. **下标越界 / 队列空**：在取 `pos[d].popleft()` 前一定要确认队列非空。  
  3. **字符是数字而非字母**：记得把字符 `'0'~'9'` 转成整数 `0~9`，否则比较会出错。  
- **下次遇到同类题**，第一步应该问自己：“**这个操作会改变相对顺序吗？如果只能让更小的东西往左走，那么在把目标字符拉到当前位置前，需要确保左侧没有更小的未使用字符**”。有了这个视角，就能迅速构造出类似的贪心/队列解法。