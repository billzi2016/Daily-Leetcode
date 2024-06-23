# #2742. 给墙面涂漆 / Painting the Walls

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/painting-the-walls/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays, cost and time, of size n representing the costs and the time taken to paint n different walls respectively. There are two painters available:
Return the minimum amount of money required to paint the n walls.

**Examples**

**Example 1:**

```
Input: cost = [1,2,3,2], time = [1,2,3,2]
Output: 3
Explanation: The walls at index 0 and 1 will be painted by the paid painter, and it will take 3 units of time; meanwhile, the free painter will paint the walls at index 2 and 3, free of cost in 2 units of time. Thus, the total cost is 1 + 2 = 3.
```

**Example 2:**

```
Input: cost = [2,3,4,2], time = [1,1,1,1]
Output: 4
Explanation: The walls at index 0 and 3 will be painted by the paid painter, and it will take 2 units of time; meanwhile, the free painter will paint the walls at index 1 and 2, free of cost in 2 units of time. Thus, the total cost is 2 + 2 = 4.
```

**Constraints**

- 1 <= cost.length <= 500
- cost.length == time.length
- 1 <= cost[i] <= 106
- 1 <= time[i] <= 500

---

## 题目（中文翻译）

你得到两个下标从 0 开始的整数数组 **cost** 和 **time**，长度均为 n，分别表示涂 n 面不同墙壁的费用和所需时间。有两名涂漆工人：

- **付费涂漆工**：涂每面墙都会产生对应的 **cost[i]**，并且需要 **time[i]** 单位时间。
- **免费涂漆工**：涂墙不产生费用，但也需要时间（具体规则见示例）。

返回涂完所有 n 面墙所需的最小花费。

---

### 示例

**示例 1**  
```
Input: cost = [1,2,3,2], time = [1,2,3,2]
Output: 3
Explanation: 索引 0 和 1 的墙由付费涂漆工完成，耗时 1 + 2 = 3 单位时间；与此同时，免费涂漆工涂完索引 2 和 3 的墙，耗时 2 单位时间且不产生费用。因此总费用为 1 + 2 = 3。
```

**示例 2**  
```
Input: cost = [2,3,4,2], time = [1,1,1,1]
Output: 4
Explanation: 索引 0 和 3 的墙由付费涂漆工完成，耗时 1 + 1 = 2 单位时间；免费涂漆工涂完索引 1 和 2 的墙，耗时 2 单位时间且不产生费用。因此总费用为 2 + 2 = 4。
```

---

### 约束条件
- $1 \leq \text{cost.length} \leq 500$
- $\text{cost.length} = \text{time.length}$
- $1 \leq \text{cost}[i] \leq 10^6$
- $1 \leq \text{time}[i] \leq 500$

---

**⚠️ 题目描述不完整或存在歧义**  

目前给出的信息（示例、约束、提示）不足以唯一确定问题的正式要求。例如：

- 示例 1 中，“免费画家在 2 单位时间内完成第 2、3 墙”的描述与 `time = [1,2,3,2]` 不吻合。  
- 提示 “Paid painters will be used for a maximum of N/2 units of time” 与示例中的数值也不匹配。  
- 若仅要求 “把所有墙都画完，付费画家的总时间 ≤ 总时间的一半”，则空集合（不付费）即可得到最小费用 0，这与示例答案冲突。  

为了避免给出错误的解法，建议先确认以下关键点：

1. **约束条件**  
   - 是否要求两位画家的工作时间 **都不超过** 某个上限（例如总时间的一半）？  
   - 还是要求付费画家的工作时间 **不超过** 免费画家的工作时间，或 **至少** 达到某个阈值？

2. **目标函数**  
   - 仅最小化付费画家的费用，还是在费用最小的前提下还要最小化整体完成时间（makespan）？

3. **示例解释**  
   - 示例 1 中免费画家的耗时为何为 2 而不是 3+2=5？  
   - 示例 2 与示例 1 的费用计算依据是什么？

4. **提示中的 “N/2”**  
   - 这里的 `N` 是指墙的数量，还是所有墙的总时间 `sum(time)`？

请补充或澄清上述细节后，我会基于完整的题意给出 **直觉解（暴力）**、**最优解（动态规划）**、复杂度分析以及解题心得等完整文档。