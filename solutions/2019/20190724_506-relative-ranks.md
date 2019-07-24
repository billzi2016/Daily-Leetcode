# #506. 相对排名 / Relative Ranks

> 难度：简单 · 标签：Array、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/relative-ranks/)

---

## 题目（英文原版）

**Description**

You are given an integer array score of size n, where score[i] is the score of the ith athlete in a competition. All the scores are guaranteed to be unique.
The athletes are placed based on their scores, where the 1st place athlete has the highest score, the 2nd place athlete has the 2nd highest score, and so on. The placement of each athlete determines their rank:
Return an array answer of size n where answer[i] is the rank of the ith athlete.

**Examples**

**Example 1:**

```
Input: score = [5,4,3,2,1]
Output: ["Gold Medal","Silver Medal","Bronze Medal","4","5"]
Explanation: The placements are [1st, 2nd, 3rd, 4th, 5th].
```

**Example 2:**

```
Input: score = [10,3,8,9,4]
Output: ["Gold Medal","5","Bronze Medal","Silver Medal","4"]
Explanation: The placements are [1st, 5th, 3rd, 2nd, 4th].
```

**Constraints**

- n == score.length
- 1 <= n <= 104
- 0 <= score[i] <= 106
- All the values in score are unique.

---

## 题目（中文翻译）

你得到一个大小为 `n` 的整数数组 `score`，其中 `score[i]` 表示第 `i` 位运动员在比赛中的得分。所有得分均保证唯一。  
运动员根据得分进行排序，得分最高的运动员排名第 1 名，得分第二高的运动员排名第 2 名，依此类推。每位运动员的排名决定其奖励：

- 第 1 名获得 **Gold Medal**（金牌）  
- 第 2 名获得 **Silver Medal**（银牌）  
- 第 3 名获得 **Bronze Medal**（铜牌）  
- 其余名次直接用对应的序号字符串表示（例如 `"4"`、`"5"` …）

返回一个大小为 `n` 的字符串数组 `answer`，其中 `answer[i]` 为第 `i` 位运动员的排名表示。

---

### 示例

**示例 1**  
```text
Input: score = [5,4,3,2,1]
Output: ["Gold Medal","Silver Medal","Bronze Medal","4","5"]
Explanation: 排名顺序为 [第 1 名, 第 2 名, 第 3 名, 第 4 名, 第 5 名]。
```

**示例 2**  
```text
Input: score = [10,3,8,9,4]
Output: ["Gold Medal","5","Bronze Medal","Silver Medal","4"]
Explanation: 排名顺序为 [第 1 名, 第 5 名, 第 3 名, 第 2 名, 第 4 名]。
```

---

### 约束条件

- `n == score.length`
- `1 <= n <= 10^4`
- `0 <= score[i] <= 10^6`
- `score` 中的所有值均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个运动员，逐个和其他运动员的成绩比较**，看有多少人的成绩比他高。  
- 如果有 0 个人比他高，说明他是第 1 名；  
- 如果有 1 个人比他高，就是第 2 名；以此类推。  

这里用到的唯一数据结构是 **列表（数组）**，我们把 `score` 看成一排排选手的成绩单。  
把“比较多少次”想象成 **一次一次翻阅成绩单**，每翻一页就判断一次大小，类似在字典里查词——虽然慢，但最容易想到。

**为什么这个方法一定正确？**  
因为题目保证所有成绩互不相同，比较的结果唯一。只要我们数清了有多少人比当前选手分数高，就能准确知道他的名次。

#### 代码（Python）

```python
def findRelativeRanks(score):
    n = len(score)                     # 运动员总人数
    answer = [""] * n                  # 用来存放最终的名次字符串

    for i in range(n):                 # 遍历每个运动员 i
        # 统计有多少分数比 score[i] 大
        higher = 0
        for j in range(n):
            if score[j] > score[i]:
                higher += 1

        # 根据 higher 的值决定名次的文字
        if higher == 0:
            answer[i] = "Gold Medal"
        elif higher == 1:
            answer[i] = "Silver Medal"
        elif higher == 2:
            answer[i] = "Bronze Medal"
        else:
            # 第 higher+1 名，用数字字符串表示
            answer[i] = str(higher + 1)

    return answer
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  解释：外层循环跑 `n` 次，内层循环也跑 `n` 次，两个循环相乘就是 `n × n`，也就是 **平方级**。如果 `n` 是 10 000，运算次数大约是 1 亿次，可能会比较慢。  
- **空间复杂度：** `O(n)`  
  解释：我们额外开辟了一个长度为 `n` 的 `answer` 列表来存放结果，除此之外没有其他随 `n` 增长的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每个选手都要遍历全部选手一次**，导致 `O(n²)`。  
我们注意到，只要把成绩 **从大到小排好序**，名次就自然出现了：排第一的就是金牌，第二的银牌，第三的铜牌，之后直接用数字表示。

实现思路分两步：

1. **记录原始下标**  
   为了在排好序后还能把名次写回到原来的位置，需要把每个成绩和它在原数组中的下标配对。可以把 `(score[i], i)` 放进一个列表。

2. **排序 + 填写答案**  
   - 按成绩从大到小排序（`sorted(..., reverse=True)`），得到一个按名次顺序的列表。  
   - 依次遍历排好序的列表，根据当前是第几名，填入对应的字符串（前 3 名特殊文字，其余用数字）。  
   - 因为我们保存了原下标 `i`，所以可以直接把结果写到 `answer[i]` 中。

如果你熟悉 **堆（优先队列）**，也可以把所有成绩放进最大堆，一次弹出最大的元素来决定名次。这里用排序更直观，时间复杂度同样是 `O(n log n)`。

#### 代码（Python）

```python
def findRelativeRanks(score):
    n = len(score)
    answer = [""] * n                         # 最终答案

    # 1) 把成绩和原下标配对，例如 (10, 0) 表示成绩 10 在下标 0 处
    indexed_scores = [(s, i) for i, s in enumerate(score)]

    # 2) 按成绩从大到小排序，sorted 返回新的列表
    #    reverse=True 表示降序
    indexed_scores.sort(key=lambda x: x[0], reverse=True)

    # 3) 根据排好的顺序依次写入名次
    for rank, (s, i) in enumerate(indexed_scores, start=1):
        if rank == 1:
            answer[i] = "Gold Medal"
        elif rank == 2:
            answer[i] = "Silver Medal"
        elif rank == 3:
            answer[i] = "Bronze Medal"
        else:
            answer[i] = str(rank)   # 第 4、5…名直接用数字

    return answer
```

#### 复杂度  

- **时间复杂度：** `O(n log n)`  
  解释：排序是这道题的主耗时步骤，排序算法的复杂度是 `n log n`（对数级），远快于 `n²`。遍历一次排好序的列表只要 `O(n)`，不影响总体复杂度。  

- **空间复杂度：** `O(n)`  
  解释：我们额外用了 `indexed_scores`（长度 `n`）和 `answer`（长度 `n`），总共是线性空间。Python 的排序本身也会使用 `O(n)` 的临时空间。

---

## 心得

- **核心技巧**：**排序 + 记录原下标**（或使用最大堆）。  
- **适用的题型**：  
  1. “按成绩/分数/高度排名” 类问题（如《排队叫号》）。  
  2. “把原数组的元素按某种顺序重新映射到新数组” （如《按字母顺序重排字符串》）。  
  3. “找第 K 大/小元素” 系列题目（可用堆或快速选择）。  
- **一句话总结解题钥匙**：**先把想要的顺序排好，再把结果“倒回”原位置**。

---

## 反思

- **第一反应**：看到“最高分”“第几名”，自然想到“比较大小”。于是先想到逐个遍历比较，得到暴力解。  
- **最容易踩的坑**：  
  - 忘记把 **原下标** 保存下来，导致排好序后不知道该把名次写到哪儿。  
  - 前三名的文字写错（顺序必须是 Gold → Silver → Bronze）。  
  - 当只有 1、2、3 名时，仍然要返回对应的文字，而不是数字。  
- **下次遇到同类题**，第一步应该问自己：“**这道题的核心是要得到一个有序的排列**吗？如果是，先把数据排序（或用堆）并保留原位置索引”。这样就能直接跳到最优思路，避免不必要的 `O(n²)` 暴力。