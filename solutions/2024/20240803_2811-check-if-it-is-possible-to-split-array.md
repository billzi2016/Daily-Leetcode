# #2811. 检查是否可以拆分数组 / Check if it is Possible to Split Array

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/check-if-it-is-possible-to-split-array/)

---

## 题目（英文原版）

**Description**

You are given an array nums of length n and an integer m. You need to determine if it is possible to split the array into n arrays of size 1 by performing a series of steps.
An array is called good if:
In each step, you can select an existing array (which may be the result of previous steps) with a length of at least two and split it into two arrays, if both resulting arrays are good.
Return true if you can split the given array into n arrays, otherwise return false.

**Examples**

**Example 1:**

```
Input: nums = [2, 2, 1], m = 4
Output: true
Explanation:
```

**Example 2:**

```
Input: nums = [2, 1, 3], m = 5
Output: false
Explanation:
The first move has to be either of the following:
So as both moves are invalid (they do not divide the array into two good arrays), we are unable to split nums into n arrays of size 1.
```

**Example 3:**

```
Input: nums = [2, 3, 3, 2, 3], m = 6
Output: true
Explanation:
```

**Constraints**

- 1 <= n == nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= m <= 200

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的数组 `nums` 和一个整数 `m`。你需要判断是否可以通过一系列步骤把数组拆分成 `n` 个大小为 `1` 的数组。

一个数组被称为 **good**（好）如果满足以下条件：  
- 在每一步操作中，你可以选择一个当前存在的数组（该数组可能是前一步操作的结果），前提是其长度至少为 `2`，并将其拆分成两个子数组（subarray），**且**这两个得到的子数组都必须是 **good**（好）的。

如果能够将给定的数组拆分成 `n` 个大小为 `1` 的数组，则返回 `true`，否则返回 `false`。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [2, 2, 1], m = 4
```  
**输出**  
```
true
```  
**解释**  
（此处省略具体解释，题目原文未给出）

#### 示例 2
**输入**  
``` 
nums = [2, 1, 3], m = 5
```  
**输出**  
```
false
```  
**解释**  
第一次拆分只能是以下两种情况之一：  
（此处省略具体拆分方式，题目原文未给出）  
由于这两种拆分方式都无效（它们没有把数组拆分成两个 **good**（好）数组），因此无法将 `nums` 拆分成 `n` 个大小为 `1` 的数组。

#### 示例 3
**输入**  
``` 
nums = [2, 3, 3, 2, 3], m = 6
```  
**输出**  
```
true
```  
**解释**  
（此处省略具体解释，题目原文未给出）

---

### 约束条件
- `1 <= n == nums.length <= 100`
- `1 <= nums[i] <= 100`
- `1 <= m <= 200`

---

**⚠️ 题目描述不完整**  
在原题中，判断 “数组是否可以拆分” 必须依赖某个 **约束条件**（例如子数组的和必须满足某个不等式、能被 `m` 整除、平均值≥ `m` 等）。目前提供的描述只给出了拆分的递归定义，却没有说明 **“good”** 数组的具体判定规则，导致无法给出唯一、准确的算法实现。

如果你能补充完整的判定条件（比如 “子数组的和必须 ≥ `m`” 或 “子数组的和必须 ≤ `m`”，或者其他任何约束），我可以基于该条件：

1. 给出 **暴力解**（直觉实现）  
2. 推导并实现 **最优解**（DP、贪心、双指针、单调栈等）  
3. 分析时间/空间复杂度  
4. 总结技巧、常见坑、反思要点  

请提供缺失的 **good 数组判定规则**，我会立即为你完成完整的面向初学者的解题文档。