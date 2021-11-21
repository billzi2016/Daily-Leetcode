# #1560. 圆形跑道上访问次数最多的扇区 / Most Visited Sector in  a Circular Track

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/most-visited-sector-in-a-circular-track/)

---

## 题目（英文原版）

**Description**

Given an integer n and an integer array rounds. We have a circular track which consists of n sectors labeled from 1 to n. A marathon will be held on this track, the marathon consists of m rounds. The ith round starts at sector rounds[i - 1] and ends at sector rounds[i]. For example, round 1 starts at sector rounds[0] and ends at sector rounds[1]
Return an array of the most visited sectors sorted in ascending order.
Notice that you circulate the track in ascending order of sector numbers in the counter-clockwise direction (See the first example).

**Examples**

**Example 1:**

```
Input: n = 4, rounds = [1,3,1,2]
Output: [1,2]
Explanation: The marathon starts at sector 1. The order of the visited sectors is as follows:
1 --> 2 --> 3 (end of round 1) --> 4 --> 1 (end of round 2) --> 2 (end of round 3 and the marathon)
We can see that both sectors 1 and 2 are visited twice and they are the most visited sectors. Sectors 3 and 4 are visited only once.
```

**Example 2:**

```
Input: n = 2, rounds = [2,1,2,1,2,1,2,1,2]
Output: [2]
```

**Example 3:**

```
Input: n = 7, rounds = [1,3,5,7]
Output: [1,2,3,4,5,6,7]
```

**Constraints**

- 2 <= n <= 100
- 1 <= m <= 100
- rounds.length == m + 1
- 1 <= rounds[i] <= n
- rounds[i] != rounds[i + 1] for 0 <= i < m

---

## 题目（中文翻译）

给定整数 `n` 和整数数组 `rounds`。我们有一条圆形跑道（circular track），由编号从 `1` 到 `n` 的扇区（sector）组成。马拉松将在该跑道上进行，整个马拉松包含 `m` 圈（round）。第 `i` 圈从扇区 `rounds[i‑1]` 开始，在扇区 `rounds[i]` 结束。例如，第 `1` 圈从 `rounds[0]` 开始，在 `rounds[1]` 结束。

返回一个按升序排列的访问次数最多的扇区数组。

> **提示**：跑道的行进方向是扇区编号递增的逆时针方向（见第一个示例）。

### 示例

#### 示例 1
```text
Input: n = 4, rounds = [1,3,1,2]
Output: [1,2]
Explanation: 马拉松从扇区 1 开始。访问的扇区顺序如下：
1 --> 2 --> 3 (第 1 圈结束) --> 4 --> 1 (第 2 圈结束) --> 2 (第 3 圈结束且马拉松结束)
可以看到扇区 1 和扇区 2 各被访问了两次，成为访问次数最多的扇区。扇区 3 和扇区 4 只被访问一次。
```

#### 示例 2
```text
Input: n = 2, rounds = [2,1,2,1,2,1,2,1,2]
Output: [2]
```

#### 示例 3
```text
Input: n = 7, rounds = [1,3,5,7]
Output: [1,2,3,4,5,6,7]
```

### 约束条件
- `2 <= n <= 100`
- `1 <= m <= 100`
- `rounds.length == m + 1`
- `1 <= rounds[i] <= n`
- `rounds[i] != rounds[i + 1]` 对所有 `0 <= i < m` 成立

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把马拉松的每一步都“走一遍”，把每经过的赛道扇区记个分。  
- **用到的数据结构**：一个长度为 `n` 的数组 `cnt`，下标 `i`（0‑based）对应赛道扇区 `i+1`，记录该扇区被跑过的次数。可以把它想象成 **一本查字典**，词是扇区编号，页码是访问次数。  
- **遍历方式**：第 `i` 圈的起点是 `rounds[i]`，终点是 `rounds[i+1]`。从起点沿着“顺时针”（题目说逆时针，但编号是递增的）一步一步走到终点，每走到一个扇区，就把 `cnt[sector‑1] += 1`。因为是环形赛道，走到 `n` 后会回到 `1`，这可以用 **取模** 来实现：`sector = sector % n + 1`。  
- **正确性**：我们把所有可能出现的访问都完整记录下来，最后统计出现次数最多的扇区，自然就是答案。

#### 代码（Python）

```python
def mostVisited(n: int, rounds: list[int]) -> list[int]:
    # cnt[i] 记录编号为 i+1 的扇区被访问的次数
    cnt = [0] * n

    # 按照 rounds 的每一段模拟跑步
    for i in range(len(rounds) - 1):
        start = rounds[i]          # 本段的起点
        end = rounds[i + 1]        # 本段的终点

        cur = start                # 从起点开始
        while True:
            cnt[cur - 1] += 1      # 访问一次
            if cur == end:         # 到达终点，结束本段
                break
            # 向下一个扇区移动，环形赛道要回到 1
            cur = cur % n + 1

    # 找到最大的访问次数
    max_visits = max(cnt)

    # 所有访问次数等于 max_visits 的扇区按升序返回（下标 + 1）
    return [i + 1 for i, v in enumerate(cnt) if v == max_visits]
```

#### 复杂度  

- **时间复杂度**：`O(total_steps)`，其中 `total_steps` 是所有圈数跑过的格子总数。最坏情况下每一圈都要跑 `n` 步，`m ≤ 100`，所以 `O(n·m)`，在本题的约束下最多约 `10⁴`，完全可接受。  
- **空间复杂度**：`O(n)`，我们只用了一个长度为 `n` 的计数数组来记录每个扇区的访问次数。

---

### 2. 最优解

#### 思路  
暴力解的“慢”点在于我们把每一步都显式地走了一遍。其实我们只需要知道 **哪几个扇区的访问次数是最高**，不必记录每一次访问。

观察题目可以发现：

1. 马拉松是 **顺时针**（编号递增）环形跑的。  
2. 除了 **起点** 和 **终点** 之外，所有其他扇区在完整的循环中被访问的次数是相同的。  
3. 唯一会多访问一次的，是**从第一段的起点 `rounds[0]` 到最后一段的终点 `rounds[-1]` 之间的扇区**（包括这两个端点）。因为马拉松结束时正好停在 `rounds[-1]`，所以这段路比其它路多跑了一次。

换句话说，**出现次数最多的扇区** 就是从 `rounds[0]` 开始、顺时针走到 `rounds[-1]` 的所有扇区。  
这条路可能会跨过 “n → 1” 的边界：

- 若 `start ≤ end`，则直接是 `[start, start+1, …, end]`。  
- 若 `start > end`（比如从 4 跑到 2，赛道是 1‑2‑3‑4），则路经两段：`[start … n]` 加上 `[1 … end]`。

只要把这两个区间拼在一起，就得到所有**最常被访问的扇区**，并且天然是升序的（因为我们按编号递增的顺序输出）。

**为什么不需要计数？**  
想象每个扇区都有一个 “底层计数”，所有扇区在完整的环形跑完后都会被加上一样的基数（比如跑了 `k` 圈）。唯一的区别是上面提到的那段路会额外多加一次。于是 **最大计数** 必然出现在这段路上，其他扇区的计数都比它少或相等（如果整条赛道只跑了一圈，则所有扇区计数相同，答案就是全部扇区）。

#### 代码（Python）

```python
def mostVisited(n: int, rounds: list[int]) -> list[int]:
    start = rounds[0]          # 马拉松的起点
    end = rounds[-1]           # 最后一段的终点

    if start <= end:
        # 起点在前，直接输出 start~end
        return list(range(start, end + 1))
    else:
        # 跨越了 n -> 1，需要两段拼接
        # 先把 start~n 加入结果，再把 1~end 加入
        return list(range(start, n + 1)) + list(range(1, end + 1))
```

#### 复杂度  

- **时间复杂度**：`O(k)`，其中 `k` 是答案数组的长度，最多 `n`，即 `O(n)`。相比暴力的 `O(n·m)`，省去了遍历每一步的过程。  
- **空间复杂度**：`O(k)` 用于存放返回结果，最坏也是 `O(n)`，和暴力的计数数组相当，但没有额外的 `O(n)` 辅助空间。

---

## 心得

- **核心技巧**：利用环形赛道的“每圈均匀”特性，只关注起点到终点这段“多走一次”的区间。  
- **适用的题型**：  
  1. “环形数组/循环赛道”类的计数最高问题（如 *Circular Array Maximum Visits*）。  
  2. “整体均匀，只差一段” 的统计题（如 *Maximum Number of Coins You Can Obtain* 中的前缀/后缀差分思路）。  
- **一句话总结**：**最常访问的扇区就是从第一段起点顺时针走到最后一段终点的那段路**。

---

## 反思

- **第一反应**：把马拉松每一步都写出来，逐个计数——这是最安全的直觉解。  
- **最容易踩的坑**：  
  - 忘记环形赛道的回环（`n → 1`），导致索引越界。  
  - 把起点和终点都算进来还是只算一次要弄清楚（题目要求“访问次数最多”，起点和终点都算在内）。  
  - 当 `start > end` 时需要分两段输出，否则会得到错误的倒序。  
- **下次遇到同类题**：第一步先思考“是否所有位置的计数基本相同，只有某段会多一次”，如果是，就直接定位这段而不是全遍历。