# #2225. 零次或一次失利的玩家 / Find Players With Zero or One Losses

> 难度：中等 · 标签：Array、Hash Table、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/find-players-with-zero-or-one-losses/)

---

## 题目（英文原版）

**Description**

You are given an integer array matches where matches[i] = [winneri, loseri] indicates that the player winneri defeated player loseri in a match.
Return a list answer of size 2 where:
The values in the two lists should be returned in increasing order.
Note:

**Examples**

**Example 1:**

```
Input: matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]
Output: [[1,2,10],[4,5,7,8]]
Explanation:
Players 1, 2, and 10 have not lost any matches.
Players 4, 5, 7, and 8 each have lost one match.
Players 3, 6, and 9 each have lost two matches.
Thus, answer[0] = [1,2,10] and answer[1] = [4,5,7,8].
```

**Example 2:**

```
Input: matches = [[2,3],[1,3],[5,4],[6,4]]
Output: [[1,2,5,6],[]]
Explanation:
Players 1, 2, 5, and 6 have not lost any matches.
Players 3 and 4 each have lost two matches.
Thus, answer[0] = [1,2,5,6] and answer[1] = [].
```

**Constraints**

- 1 <= matches.length <= 105
- matches[i].length == 2
- 1 <= winneri, loseri <= 105
- winneri != loseri
- All matches[i] are unique.

---

## 题目（中文翻译）

给定一个整数数组 `matches`，其中 `matches[i] = [winner_i, loser_i]` 表示玩家 `winner_i` 在一场比赛中击败了玩家 `loser_i`。  
返回一个大小为 2 的列表 `answer`，其中：

- `answer[0]` 包含所有 **零次失利**（zero losses）的玩家编号，  
- `answer[1]` 包含所有 **恰好一次失利**（one loss）的玩家编号。  

两个子列表中的值必须 **升序**（in increasing order）返回。

---

### 示例

**示例 1**  
```text
Input: matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]
Output: [[1,2,10],[4,5,7,8]]
```
**解释**：  
- 玩家 1、2、10 没有输过任何比赛。  
- 玩家 4、5、7、8 各输掉了一场比赛。  
- 玩家 3、6、9 各输掉了两场比赛。  
因此 `answer[0] = [1,2,10]`，`answer[1] = [4,5,7,8]`。

**示例 2**  
```text
Input: matches = [[2,3],[1,3],[5,4],[6,4]]
Output: [[1,2,5,6],[]]
```
**解释**：  
- 玩家 1、2、5、6 没有输过任何比赛。  
- 玩家 3、4 各输掉了两场比赛。  
因此 `answer[0] = [1,2,5,6]`，`answer[1] = []`。

---

### 约束条件

- `1 <= matches.length <= 10^5`
- `matches[i].length == 2`
- `1 <= winner_i, loser_i <= 10^5`
- `winner_i != loser_i`
- 所有 `matches[i]` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有出现过的玩家收集起来，然后**逐个检查**这个玩家在 `matches` 里输掉了多少场。如果输的次数是 `0` 或 `1`，就把它放进对应的答案列表。

- **用到的数据结构**  
  - **列表（list）**：保存所有出现过的玩家编号，像是把所有选手的名字写在一本“参赛名单”上。  
  - **遍历**：对每个玩家都去 `matches` 里查一遍，类似于在比赛记录本里逐行搜索某个人的名字。

- **为什么正确**  
  对每个玩家都统计它到底输了几场，只要统计结果满足题目要求（0 场或 1 场），就一定是答案。因为我们没有遗漏任何出现过的玩家，也没有把不符合条件的玩家误加入。

- **时间/空间复杂度**  
  - 时间复杂度：设 `n = len(matches)`，玩家的总数最多是 `2n`（每场比赛产生两个玩家），所以我们会对每个玩家遍历全部 `n` 场比赛，时间是 `O( (2n) * n ) = O(n²)`。  
    大白话：如果比赛有 10,000 场，暴力解大概要比较 10,000 × 20,000 次——非常慢。  
  - 空间复杂度：我们只需要保存玩家列表和答案列表，最多存 `2n` 个整数，空间是 `O(n)`。

#### 代码（Python）

```python
def findWinners_bruteforce(matches):
    # 1. 收集所有出现过的玩家
    players = set()                     # 用 set 自动去重
    for w, l in matches:
        players.add(w)
        players.add(l)

    zero_loss = []      # 输 0 场的玩家
    one_loss = []       # 输 1 场的玩家

    # 2. 对每个玩家统计输的场数（遍历整张比赛表）
    for p in players:
        loss_cnt = 0
        for _, loser in matches:        # 逐行检查是否是输家
            if loser == p:
                loss_cnt += 1
        # 3. 根据统计结果放入对应列表
        if loss_cnt == 0:
            zero_loss.append(p)
        elif loss_cnt == 1:
            one_loss.append(p)

    # 4. 题目要求升序返回
    zero_loss.sort()
    one_loss.sort()
    return [zero_loss, one_loss]
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每个玩家都要遍历全部 `n` 场比赛，随着比赛数量的增加，耗时会呈二次方增长。  
- **空间复杂度**：`O(n)` —— 只存放玩家集合和两个答案列表，和比赛场数线性相关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每个玩家都要遍历整张比赛表**，这导致了二次时间。我们可以把“统计输的次数”这一步提前完成，只遍历一次 `matches`，把每个玩家输的次数直接记下来。  

实现思路：

1. **一次遍历**所有比赛，用**哈希表（字典）**记录每个玩家的“输的次数”。  
   - 哈希表就像一本“选手字典”，`key` 是选手编号，`value` 是它已经输掉的场数。查找或更新 `key` 的时间几乎是 **O(1)**，所以整体只需要 `O(n)`。
2. 同时把所有出现过的玩家（无论赢或输）放进一个 **集合**，确保不遗漏任何选手。  
3. 遍历这个集合，把输的次数为 `0` 的放进 `answer[0]`，为 `1` 的放进 `answer[1]`。  
4. 最后对两个答案列表排序后返回。

**关键概念解释**  

- **哈希表（字典）**：想象成一本“电话簿”，我们可以用选手的编号快速找到对应的记录（输的次数），不需要逐行搜索。  
- **集合（set）**：类似于“唯一的名单”，可以自动去掉重复的玩家编号。  

**为什么是最优**  

- 只遍历一次 `matches`，时间 `O(n)`。  
- 之后只遍历一次玩家集合，玩家数至多 `2n`，仍然是线性时间。  
- 空间使用两个线性结构（字典 + 集合），都是 `O(n)`，已经是不可再压缩的下界，因为我们必须至少保存每个出现过的玩家的信息。

#### 代码（Python）

```python
def findWinners(matches):
    """
    :type matches: List[List[int]]
    :rtype: List[List[int]]
    """
    loss_cnt = {}          # key: player, value: loss times
    players = set()        # 所有出现过的玩家（赢的也算）

    # 只遍历一次 matches
    for winner, loser in matches:
        players.add(winner)
        players.add(loser)

        # loser 输一次，计数加一
        loss_cnt[loser] = loss_cnt.get(loser, 0) + 1
        # winner 可能之前没有输过，确保在字典里有条目（这里不强制写也行）
        if winner not in loss_cnt:
            loss_cnt[winner] = loss_cnt.get(winner, 0)

    zero_loss = []   # 输 0 场的玩家
    one_loss  = []   # 输 1 场的玩家

    # 根据 loss_cnt 把玩家分配到对应列表
    for p in players:
        cnt = loss_cnt.get(p, 0)   # 若字典里没有，说明从未输过
        if cnt == 0:
            zero_loss.append(p)
        elif cnt == 1:
            one_loss.append(p)

    # 题目要求升序
    zero_loss.sort()
    one_loss.sort()
    return [zero_loss, one_loss]
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次 `matches`（`n` 条记录）以及一次玩家集合（最多 `2n` 条），两次线性遍历。相较于暴力解的 `O(n²)`，大幅提升。  
- **空间复杂度**：`O(n)` —— 需要保存每个出现过的玩家的输次数（字典）以及所有玩家的集合，和比赛数量成线性关系。

---

## 心得

- **核心技巧**：利用**哈希表统计频次**（这里是输的次数），一次遍历即可完成计数。  
- **适用的题型**  
  1. “统计出现次数”类题目，如 *“找出只出现一次的数字”*（LeetCode 136）。  
  2. “根据出现频率分类”类题目，如 *“找出出现两次的字符”*（LeetCode 438）。  
- **解题钥匙**：**先把统计工作做好，再一次性遍历结果**，避免在每个元素上重复遍历原始数据。

---

## 反思

- **第一反应**：看到“输的次数”这个关键词，立刻想到要**计数**，于是想到了字典/哈希表。  
- **最容易踩的坑**  
  - **遗漏只赢不输的玩家**：仅统计输的次数会让只赢不输的玩家在字典里不存在，需要额外的 `players` 集合来捕获所有出现过的选手。  
  - **排序要求**：答案必须升序返回，忘记排序会导致答案不匹配。  
- **下次类似题的第一步**：先明确**统计的对象是什么**（出现次数、输赢次数等），决定使用 **哈希表** 还是 **数组计数**，然后一次遍历完成统计。