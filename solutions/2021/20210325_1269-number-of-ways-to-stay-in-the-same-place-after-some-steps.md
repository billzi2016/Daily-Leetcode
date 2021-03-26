# #1269. 若干步后仍在原点的方式数 / Number of Ways to Stay in the Same Place After Some Steps

> 难度：困难 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/)

---

## 题目（英文原版）

**Description**

You have a pointer at index 0 in an array of size arrLen. At each step, you can move 1 position to the left, 1 position to the right in the array, or stay in the same place (The pointer should not be placed outside the array at any time).
Given two integers steps and arrLen, return the number of ways such that your pointer is still at index 0 after exactly steps steps. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: steps = 3, arrLen = 2
Output: 4
Explanation: There are 4 differents ways to stay at index 0 after 3 steps.
Right, Left, Stay
Stay, Right, Left
Right, Stay, Left
Stay, Stay, Stay
```

**Example 2:**

```
Input: steps = 2, arrLen = 4
Output: 2
Explanation: There are 2 differents ways to stay at index 0 after 2 steps
Right, Left
Stay, Stay
```

**Example 3:**

```
Input: steps = 4, arrLen = 2
Output: 8
```

**Constraints**

- 1 <= steps <= 500
- 1 <= arrLen <= 106

---

## 题目（中文翻译）

你有一个指针位于长度为 `arrLen` 的数组的下标 `0` 处。每一步，你可以向左移动 1 个位置、向右移动 1 个位置，或者保持不动（指针在任意时刻都不能越界到数组外）。  
给定两个整数 `steps` 和 `arrLen`，返回恰好走完 `steps` 步后指针仍然位于下标 `0` 的所有可能方式数。由于答案可能非常大，请返回 **10⁹ + 7** 取模后的结果。

## 示例

### 示例 1
```
Input: steps = 3, arrLen = 2
Output: 4
Explanation: 有 4 种不同的方式在 3 步后仍停留在下标 0。
Right, Left, Stay
Stay, Right, Left
Right, Stay, Left
Stay, Stay, Stay
```

### 示例 2
```
Input: steps = 2, arrLen = 4
Output: 2
Explanation: 有 2 种不同的方式在 2 步后仍停留在下标 0。
Right, Left
Stay, Stay
```

### 示例 3
```
Input: steps = 4, arrLen = 2
Output: 8
```

## 约束条件
- `1 <= steps <= 500`
- `1 <= arrLen <= 10⁶`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的走法枚举出来，然后统计其中恰好在 `steps` 步后回到下标 `0` 的数量。  
可以把每一步的选择看成一次“投掷”，有三种结果：

1. **左移**  → 指针 `pos-1`
2. **右移**  → 指针 `pos+1`
3. **原地不动** → 指针 `pos`

于是整个走法相当于一棵 **3‑叉树**，树的深度等于 `steps`，每条根到叶的路径就是一种走法。  
在遍历的过程中，只要发现指针跑到数组边界之外（`pos < 0` 或 `pos >= arrLen`），就立刻剪枝，因为这条路径不合法。

> **类比**：想象你在一条只能前后走的走廊里，每一步可以往左、往右或者站着不动。要统计恰好 `steps` 步后回到入口的所有走法，就像把所有可能的行走路线画出来，然后挑出以入口结束的那几条。

**为什么正确**  
暴力枚举会把**所有**合法的走法都遍历一次，只有满足「恰好 `steps` 步且最终位置是 `0`」的路径会被计数，因此答案一定是正确的。

**时间/空间复杂度**  
- 时间复杂度：每一步有 3 种选择，深度为 `steps`，所以总的搜索树节点数是 `3^steps`，即 **指数级**。  
  - 大白话：如果 `steps = 10`，大约要检查 3