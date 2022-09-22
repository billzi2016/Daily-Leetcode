# #1944. 队列中可见人数 / Number of Visible People in a Queue

> 难度：困难 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/number-of-visible-people-in-a-queue/)

---

## 题目（英文原版）

**Description**

There are n people standing in a queue, and they numbered from 0 to n - 1 in left to right order. You are given an array heights of distinct integers where heights[i] represents the height of the ith person.
A person can see another person to their right in the queue if everybody in between is shorter than both of them. More formally, the ith person can see the jth person if i < j and min(heights[i], heights[j]) > max(heights[i+1], heights[i+2], ..., heights[j-1]).
Return an array answer of length n where answer[i] is the number of people the ith person can see to their right in the queue.

**Examples**

**Example 1:**

```
Input: heights = [10,6,8,5,11,9]
Output: [3,1,2,1,1,0]
Explanation:
Person 0 can see person 1, 2, and 4.
Person 1 can see person 2.
Person 2 can see person 3 and 4.
Person 3 can see person 4.
Person 4 can see person 5.
Person 5 can see no one since nobody is to the right of them.
```

**Example 2:**

```
Input: heights = [5,1,2,3,10]
Output: [4,1,1,1,0]
```

**Constraints**

- n == heights.length
- 1 <= n <= 105
- 1 <= heights[i] <= 105
- All the values of heights are unique.

---

## 题目（中文翻译）

给定 `n` 个人站在一条队列（queue）中，编号从左到右依次为 `0` 到 `n-1`。你会得到一个由不同整数构成的数组（array）`heights`，其中 `heights[i]` 表示第 `i` 个人的身高。

如果两个人之间的所有人都比他们两人都矮，则左侧的这个人可以看到右侧的那个人。形式化地说，当 `i < j` 且  

`min(heights[i], heights[j]) > max(heights[i+1], heights[i+2], ..., heights[j-1])`  

时，第 `i` 个人可以看到第 `j` 个人。

返回一个长度为 `n` 的数组 `answer`，其中 `answer[i]` 表示第 `i` 个人能够看到的右侧人的数量。

示例 1:
Input: heights = [10,6,8,5,11,9]
Output: [3,1,2,1,1,0]
Explanation:
- 人 0 可以看到人 1、2 和 4。  
- 人 1 可以看到人 2。  
- 人 2 可以看到人 3 和 4。  
- 人 3 可以看到人 4。  
- 人 4 可以看到人 5。  
- 人 5 看不到任何人，因为其右侧没有人。

示例 2:
Input: heights = [5,1,2,3,10]
Output: [4,1,1,1,0]
Explanation:
- 人 0 可以看到右侧的 4 个人（1、2、3、4）。  
- 人 1 可以看到人 2。  
- 人 2 可以看到人 3。  
- 人 3 可以看到人 4。  
- 人 4 看不到任何人。

约束条件：
- `n == heights.length`
- `1 <= n <= 10^5`
- `1 <= heights[i] <= 10^5`
- `heights` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对于每一个人 i，向右依次检查后面的每一个人 j**，看他是否满足“中间所有人都比 i 和 j 短”。  
这可以一步一步地模拟：

1. 从 i+1 开始往右走，用一个变量 `max_between` 记录 i 与当前 j 之间的最高身高（即 `max(heights[i+1…j-1])`）。  
2. 当检查到 j 时，只要 `max_between < heights[i]` 并且 `max_between < heights[j]`（等价于 `min(heights[i], heights[j]) > max_between`），说明 i 能看到 j，计数器 `cnt` 加 1。  
3. 然后把 `heights[j]` 与 `max_between` 比较，更新 `max_between` 为两者的较大值，继续检查下一个 j。  

> **类比**：把身高看成“一堵墙”。站在 i 位置的你想往右看，只有当你和目标 j 之间的最高墙比你们两个都低时，你才能看到 j。我们每走一步，就把这段路上的最高墙记下来。

这个办法一定能得到正确答案，因为我们穷举了所有可能的 j，并且每次都严格按照题目定义检查可视条件。

#### 代码（Python）

```python
from typing import List

def canSeePersonsCount_bruteforce(heights: List[int]) -> List[int]:
    n = len(heights)
    ans = [0] * n                     # 最终答案，全部先设为 0
    for i in range(n):                # 对每一个人 i
        cnt = 0                        # i 能看到的人数计数器
        max_between = -1              # i 与当前 j 之间的最高身高，初始为 -1（因为身高都是正数）
        for j in range(i + 1, n):     # 向右检查每一个 j
            # 判断 i 是否能看到 j
            if max_between < heights[i] and max_between < heights[j]:
                cnt += 1               # 能看到，计数 +1
            # 更新 max_between 为 i 与 j 之间的最高身高
            max_between = max(max_between, heights[j])
        ans[i] = cnt                    # 把 i 的结果写入答案数组
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n²` 表示“如果有 10 个人，你大概要比较 10×10=100 次”。因为外层遍历 `n` 次，内层最坏情况下也要遍历 `n` 次（从 i+1 到末尾），所以总操作次数与 `n` 的平方成正比。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了常数个额外变量 `cnt`、`max_between`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

**暴力解的瓶颈**在于：对每个人都要重新向右扫描，导致大量重复工作。  
实际上，当我们从右向左遍历时，可以把“已经看到的更矮的人”保存下来，后面的更高的人只需要一次性把它们弹出，**不必再逐个检查**。这正是**单调栈（Monotonic Stack）**的典型用法。

**核心想法**：

1. 从数组最右侧开始往左遍历。右侧已经处理完的元素会保存在一个栈 `stk` 中，栈里保存的是**身高递减**的序列（栈顶是最近、且最高的那个人）。  
   - 为什么要递减？因为如果栈中出现了一个比前面更高的身高，它必然会挡住更矮的身高对左侧人的视线，后者就不需要再保留了。  
2. 对于当前位置 `i`，栈顶到栈底的所有元素（即比 `heights[i]` 短的）都是 `i` 能看到的人。我们把它们全部弹出，计数器 `cnt` 加上弹出的次数。  
3. 弹完后，如果栈仍然非空，栈顶的那个人比 `heights[i]` 高，`i` 仍然可以看到 **这个更高的人**（因为它比 `i` 高，且中间没有更高的阻挡），所以 `cnt` 再加 1。  
4. 最后把 `heights[i]` 压入栈中，继续向左处理下一个人。

> **类比**：想象你站在右边的山顶往左看，山峰高度依次记录在栈里。每次往左走一步，你把比自己低的山峰“摘下来”，因为它们已经被你看到并且不会再影响更左边的视线。若还有更高的山峰在前面，你还能再看到它一个。

**一步步推导**：

- **一步**：从右往左遍历，这样右边的答案已经确定，可以直接利用。  
- **二步**：使用栈保存“右侧仍然可见的身高”。栈保持递减顺序，保证栈顶永远是最近且最高的可见人。  
- **三步**：弹出所有比当前身高低的元素，这些就是当前人能看到的“矮人”。  
- **四步**：如果弹完后栈仍有元素，说明还有一个更高的人在右侧，当前人还能看到它（因为更高的人不被更矮的人挡住），计数再加 1。  

这样每个元素只会被压入栈一次、弹出栈一次，整体线性时间。

#### 代码（Python）

```python
from typing import List

def canSeePersonsCount(heights: List[int]) -> List[int]:
    n = len(heights)
    ans = [0] * n                # 最终答案
    stk: List[int] = []          # 单调递减栈，保存身高（也可以只保存下标）

    # 从右往左遍历
    for i in range(n - 1, -1, -1):
        cnt = 0                  # 当前人 i 能看到的人数

        # 弹出所有比 heights[i] 短的元素，它们都是 i 能看到的
        while stk and stk[-1] < heights[i]:
            stk.pop()
            cnt += 1

        # 若栈非空，栈顶是第一个比 heights[i] 高的人，i 也能看到它
        if stk:
            cnt += 1

        ans[i] = cnt              # 写入答案
        stk.append(heights[i])    # 把当前人压入栈，供左侧的人使用

    return ans
```

> **代码要点**  
> - `while stk and stk[-1] < heights[i]`：只要栈顶比当前人矮，就把它弹掉，因为它已经被当前人“看到”，以后更左边的人不需要再考虑它。  
> - `if stk:`：弹完后如果还有人，说明栈顶比当前人高，当前人还能看到这个更高的人（只看一次）。  
> - 栈中保存的始终是从当前位置向右最近的、**身高递减**的序列。

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个身高只会进栈一次、出栈一次，合计最多 `2n` 次基本操作。  
  > 类比：如果有 1000 个人，你最多只会“放进背包”1000 次、再“拿出背包”1000 次，整体操作次数与人数成线性关系。

- **空间复杂度**：`O(n)`（最坏情况下栈里会存全部元素）  
  需要额外的栈来保存右侧未被更高身高挡住的人数，最坏情况下栈的大小等于 `n`。

---

## 心得

- **核心技巧**：单调栈（Monotonic Stack）——利用栈的递减/递增特性，能够在一次遍历中完成“最近更大/更小”这类查询。  
- **适用题型**  
  1. **下一个更大元素**（Next Greater Element）  
  2. **柱状图中最大的矩形面积**（Largest Rectangle in Histogram）  
  3. **滑动窗口最大值**（Sliding Window Maximum）  
- **一句话总结**：  
  “从右往左，用单调递减栈把右侧比自己矮的人一次性弹掉，剩下的第一个更高的人就是还能看到的最后一个”。  

---

## 反思

- **第一反应**：直接写两层循环，逐个比较，想到了暴力 `O(n²)` 的做法。  
- **最容易踩的坑**  
  1. **忘记计数更高的那个人**：只弹出矮的人会漏掉“第一个更高的”。  
  2. **栈的递减顺序写反**：如果栈里是递增的，弹出条件会写错，导致错误答案。  
  3. **边界条件**：最后一个人右侧没有人，答案必须是 0，代码中需要正确处理空栈的情况。  
- **下次遇到同类题**：第一步先问自己“是否可以把问题倒着思考（从右往左）并利用单调栈来维护‘当前可见的候选集合’”。如果答案是肯定的，就立刻尝试构造单调栈的进出规则。