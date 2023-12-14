# #2512. 奖励前 K 名学生 / Reward Top K Students

> 难度：中等 · 标签：Array、Hash Table、String、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/reward-top-k-students/)

---

## 题目（英文原版）

**Description**

You are given two string arrays positive_feedback and negative_feedback, containing the words denoting positive and negative feedback, respectively. Note that no word is both positive and negative.
Initially every student has 0 points. Each positive word in a feedback report increases the points of a student by 3, whereas each negative word decreases the points by 1.
You are given n feedback reports, represented by a 0-indexed string array report and a 0-indexed integer array student_id, where student_id[i] represents the ID of the student who has received the feedback report report[i]. The ID of each student is unique.
Given an integer k, return the top k students after ranking them in non-increasing order by their points. In case more than one student has the same points, the one with the lower ID ranks higher.

**Examples**

**Example 1:**

```
Input: positive_feedback = ["smart","brilliant","studious"], negative_feedback = ["not"], report = ["this student is studious","the student is smart"], student_id = [1,2], k = 2
Output: [1,2]
Explanation: 
Both the students have 1 positive feedback and 3 points but since student 1 has a lower ID he ranks higher.
```

**Example 2:**

```
Input: positive_feedback = ["smart","brilliant","studious"], negative_feedback = ["not"], report = ["this student is not studious","the student is smart"], student_id = [1,2], k = 2
Output: [2,1]
Explanation: 
- The student with ID 1 has 1 positive feedback and 1 negative feedback, so he has 3-1=2 points. 
- The student with ID 2 has 1 positive feedback, so he has 3 points. 
Since student 2 has more points, [2,1] is returned.
```

**Constraints**

- 1 <= positive_feedback.length, negative_feedback.length <= 104
- 1 <= positive_feedback[i].length, negative_feedback[j].length <= 100
- Both positive_feedback[i] and negative_feedback[j] consists of lowercase English letters.
- No word is present in both positive_feedback and negative_feedback.
- n == report.length == student_id.length
- 1 <= n <= 104
- report[i] consists of lowercase English letters and spaces ' '.
- There is a single space between consecutive words of report[i].
- 1 <= report[i].length <= 100
- 1 <= student_id[i] <= 109
- All the values of student_id[i] are unique.
- 1 <= k <= n

---

## 题目（中文翻译）

你将得到两个字符串数组 `positive_feedback` 和 `negative_feedback`，分别包含表示积极反馈和消极反馈的词语。请注意，没有词语会同时出现在两者中。  
最初每位学生的分数为 0。每出现一次积极词语（positive word）会使学生的分数增加 3 分，而每出现一次消极词语（negative word）会使学生的分数减少 1 分。  

现在有 `n` 条反馈报告，由下标从 0 开始的字符串数组 `report` 和下标从 0 开始的整数数组 `student_id` 表示，其中 `student_id[i]` 为收到第 `i` 条反馈报告 `report[i]` 的学生的 ID。每个学生的 ID 均唯一。  

给定整数 `k`，请在按照分数非递增（从高到低）排序后返回前 `k` 名学生的 ID 列表。如果出现分数相同的情况，ID 较小的学生排名更靠前。

**示例 1**  
**示例 2**  
**约束条件**  

示例  
**示例 1:**  
```text
Input: positive_feedback = ["smart","brilliant","studious"], negative_feedback = ["not"], report = ["this student is studious","the student is smart"], student_id = [1,2], k = 2
Output: [1,2]
Explanation:  
两位学生各收到 1 条积极反馈，得到 3 分。由于学生 1 的 ID 更小，他排名更靠前。
```

**示例 2:**  
```text
Input: positive_feedback = ["smart","brilliant","studious"], negative_feedback = ["not"], report = ["this student is not studious","the student is smart"], student_id = [1,2], k = 2
Output: [2,1]
Explanation:  
- 学生 1 收到 1 条积极反馈和 1 条消极反馈，得分为 3-1=2 分。  
- 学生 2 收到 1 条积极反馈，得分为 3 分。  
由于学生 2 的得分更高，他排名第一。
```

约束条件  
- `1 <= positive_feedback.length, negative_feedback.length <= 10^4`  
- `1 <= positive_feedback[i].length, negative_feedback[j].length <= 100`  
- `positive_feedback[i]` 和 `negative_feedback[j]` 均由小写英文字母组成。  
- 没有词语同时出现在 `positive_feedback` 和 `negative_feedback` 中。  
- `n == report.length == student_id.length`  
- `1 <= n <= 10^4`  
- `report[i]` 只包含小写英文字母和空格 `' '`。  
- `report[i]` 中相邻单词之间只有一个空格。  
- `1 <= report[i].length <= 100`  
- `1 <= student_id[i] <= 10^9`  
- 所有 `student_id[i]` 均唯一。  
- `1 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**逐条处理每份报告**，把报告里的每个单词都和正向词表、负向词表进行比较：

1. 把 `positive_feedback`、`negative_feedback` 两个列表直接当作普通的 Python 列表保存。  
   - 这相当于我们在生活中**翻字典**：要找一个词是否是正向词，就在正向词的“字典”里逐个查找。  
2. 对于第 `i` 份报告 `report[i]`，先把它用空格拆成单词列表。  
3. 对每个单词：  
   - 如果在正向词列表里，给对应的学生 `+3` 分；  
   - 如果在负向词列表里，给对应的学生 `-1` 分。  
4. 用一个 `dict`（哈希表）记录每个学生的累计分数，键是 `student_id[i]`，值是分数。  
5. 最后把所有学生按照**分数从高到低**排序，分数相同则**ID 更小的排前面**，取前 `k` 个即可。

> **为什么能得到正确答案？**  
> 只要我们把每份报告里出现的正/负词都统计出来，并且严格按照题目给的加减分规则累加，最终得到的每个学生的总分必然是题目要求的分数。排序只是一种“展示”手段，不会改变分数本身。

> **复杂度大白话**  
> - `O(n * m)` 里的 `n` 是报告的条数，`m` 是每条报告的单词数。  
> - `O(p)` 是正向词表的长度，`O(q)` 是负向词表的长度。因为我们每次都要在列表里**线性查找**（像在一本厚厚的词典里逐页翻），所以总体时间是 `O(n * m * (p+q))`。  
> - 空间上只多用了一个 `dict` 保存学生分数，大小和学生人数成正比，即 `O(n)`。

#### 代码（Python）  
```python
def topStudents_bruteforce(positive_feedback, negative_feedback,
                          report, student_id, k):
    # 1. 用列表保存正负词（暴力解每次线性查找）
    pos = positive_feedback          # 正向词列表
    neg = negative_feedback          # 负向词列表

    # 2. 用字典记录每个学生的总分，键是学生 ID，值是分数
    scores = {}                      # 哈希表，像查字典一样 O(1) 存取

    # 3. 逐条处理报告
    for idx, txt in enumerate(report):
        sid = student_id[idx]        # 当前报告对应的学生 ID
        # 把报告按空格切成单词
        words = txt.split()          # 例：["this","student","is","studious"]
        # 初始化该学生的分数（如果之前没有出现过）
        if sid not in scores:
            scores[sid] = 0

        # 4. 对每个单词检查正负词表（这里是线性遍历列表）
        for w in words:
            if w in pos:             # 正向词 → +3 分
                scores[sid] += 3
            elif w in neg:           # 负向词 → -1 分
                scores[sid] -= 1

    # 5. 把所有学生按照「分数高 → ID 低」的顺序排序
    #   sorted 返回列表，key 用元组 ( -score, id ) 实现多重排序
    ordered = sorted(scores.items(),
                     key=lambda x: (-x[1], x[0]))

    # 6. 取前 k 个学生的 ID
    return [sid for sid, _ in ordered[:k]]
```

#### 复杂度  
- **时间复杂度**：`O(n * m * (p + q))`  
  - 解释：对每条报告（`n` 条），我们遍历其中的每个单词（平均 `m` 个），并在正负词列表里做线性查找（分别是 `p`、`q` 长度）。  
  - 用生活中的比喻：就像有 `n` 本书，每本书有 `m` 页，每翻一页都要在两本厚厚的词典里找一次对应的词。  
- **空间复杂度**：`O(n)`  
  - 只用了一个字典保存每个学生的分数，最多有 `n` 个学生（因为 `student_id` 唯一）。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于对正负词的查找**。每次都在列表里线性遍历，等价于在一本厚厚的词典里逐页翻，时间开销大。我们可以把正负词提前放进**哈希集合（set）**，这样查询的时间复杂度就从 `O(p)`、`O(q)` 降到 **O(1)**，即“只要看一下键是否在集合里”，和在字典里直接查找一样快。

接下来还有两种常见的“取前 K”方式：

1. **全排序**：先把所有学生的 `(score, id)` 放进列表，直接 `sort`，时间 `O(n log n)`。实现简单，代码直观。  
2. **最小堆（Priority Queue）**：维护一个大小为 `k` 的最小堆，遍历学生时把当前学生放进去，如果堆的大小超过 `k` 就弹出堆顶（最小的那个），这样堆里始终保留分数最高的 `k` 个学生。时间 `O(n log k)`，空间 `O(k)`，在 `k` 远小于 `n` 时更快。

这里我们展示 **两步走** 的最优实现：  
- 第一步用 **哈希集合** 把正负词的查找降到 O(1)。  
- 第二步用 **全排序**（代码更简洁），如果想进一步提升可以改成最小堆。

> **核心概念解释**  
> - **哈希集合（set）**：类似生活中的“快速查找表”。把所有正向词放进一个盒子，想知道某个单词是否是正向词，只需要把它扔进去检查是否已经在盒子里，几乎是瞬间就能得到答案。  
> - **最小堆**：想象有一个只能装 `k` 本书的书架，每次放新书进去，如果书架已经满了，就把 **最薄** 的那本书扔掉，保证书架里永远是 **最厚**（分数最高）的 `k` 本书。堆的实现正是用来快速找出最薄那本书（堆顶）的数据结构。

#### 代码（Python）  
```python
import heapq
from typing import List

def topStudents_optimal(positive_feedback: List[str],
                        negative_feedback: List[str],
                        report: List[str],
                        student_id: List[int],
                        k: int) -> List[int]:
    # 1. 把正负词放进哈希集合，查询时间 O(1)
    pos_set = set(positive_feedback)   # 正向词集合
    neg_set = set(negative_feedback)   # 负向词集合

    # 2. 统计每个学生的分数
    scores = {}                         # 学生 ID -> 分数
    for idx, txt in enumerate(report):
        sid = student_id[idx]
        # 若该学生尚未出现，初始化分数为 0
        scores.setdefault(sid, 0)

        # 把报告拆成单词，遍历统计
        for w in txt.split():
            if w in pos_set:            # 正向词 → +3
                scores[sid] += 3
            elif w in neg_set:          # 负向词 → -1
                scores[sid] -= 1

    # 3. 取前 k 名 —— 方法一：全排序（代码更直观）
    #    按「分数高 → ID 低」排序，利用元组 (-score, id) 实现
    ordered = sorted(scores.items(),
                     key=lambda x: (-x[1], x[0]))
    top_k = [sid for sid, _ in ordered[:k]]
    return top_k

    # 4. 取前 k 名 —— 方法二：最小堆（如果 k << n 时更快）
    #    heap 里存 (score, -id) 使得堆顶是「最小分数、ID 最大」的学生
    # heap = []
    # for sid, sc in scores.items():
    #     heapq.heappush(heap, (sc, -sid))   # 负号让 ID 越大越「小」在堆里
    #     if len(heap) > k:
    #         heapq.heappop(heap)           # 弹出最小的那位
    # # 堆中剩下的就是 top k，取出后再按要求排序
    # top_k = [ -sid for sc, sid in sorted(heap, key=lambda x: (-x[0], x[1])) ]
    # return top_k
```

#### 复杂度  
- **时间复杂度**：`O(n * m + n log n)`（全排序版）  
  - `O(n * m)`：遍历所有报告的每个单词并在哈希集合中 O(1) 判断正负。  
  - `O(n log n)`：对 `n` 个学生进行一次排序。  
  - 与暴力解相比，省去了 `p+q` 的线性查找，速度提升明显。  
- **空间复杂度**：`O(p + q + n)`  
  - `O(p + q)` 用于存放正负词集合；`O(n)` 用于保存每个学生的分数。  

如果改用最小堆，则时间会变成 `O(n * m + n log k)`，空间 `O(p + q + k)`，在 `k` 远小于 `n` 时更具优势。

---

## 心得  

- **核心技巧**：  
  1. **哈希集合**（set）实现 O(1) 的词汇查找。  
  2. **多关键字排序**：先按分数降序，再按 ID 升序，用元组 `(-score, id)` 一行搞定。  
  3. **堆（可选）**：在需要「只保留前 k」且 `k` 较小的场景下，使用最小堆把时间复杂度压到 `O(n log k)`。

- **适用的题型**（类似思路）  
  1. “统计词频并返回出现次数最多的前 K 个单词”。  
  2. “根据成绩排序并取前 K 名学生”。  
  3. “在大量日志中筛选出现次数最高的前 K 条关键字”。

- **一句话总结解题钥匙**：**先把需要频繁查询的集合做成哈希结构，再用合适的排序或堆把 “前 K” 挖出来**。

---

## 反思  

- **拿到题目第一反应**：先把每份报告的单词一个个对照正负词表，直接累加分数——这就是暴力思路。  
- **最容易踩的坑**  
  1. **正负词查找使用列表**导致时间超限。  
  2. **报告里可能出现重复单词**，每出现一次都要计分，不能去重。  
  3. **排序时忘记“分数相同 ID 小的排前面”**，导致结果顺序错误。  
  4. **学生 ID 可能非常大**（ up to 1e9），不要把它当作数组下标使用。  

- **下次遇到同类题，第一步该想到**：**把所有需要快速判断的元素（词、编号等）放进哈希集合或哈希映射**，这样后面的遍历就能做到 O(1) 查询，避免不必要的线性搜索。