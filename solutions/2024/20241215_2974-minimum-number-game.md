# #2974. 最小数游戏 / Minimum Number Game

> 难度：简单 · 标签：Array、Sorting、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/minimum-number-game/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of even length and there is also an empty array arr. Alice and Bob decided to play a game where in every round Alice and Bob will do one move. The rules of the game are as follows:
Return the resulting array arr.

**Examples**

**Example 1:**

```
Input: nums = [5,4,2,3]
Output: [3,2,5,4]
Explanation: In round one, first Alice removes 2 and then Bob removes 3. Then in arr firstly Bob appends 3 and then Alice appends 2. So arr = [3,2].
At the begining of round two, nums = [5,4]. Now, first Alice removes 4 and then Bob removes 5. Then both append in arr which becomes [3,2,5,4].
```

**Example 2:**

```
Input: nums = [2,5]
Output: [5,2]
Explanation: In round one, first Alice removes 2 and then Bob removes 5. Then in arr firstly Bob appends and then Alice appends. So arr = [5,2].
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 100
- nums.length % 2 == 0

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始、长度为偶数的整数数组 `nums`，以及一个初始为空的数组 `arr`。Alice 和 Bob 决定进行如下游戏：每一轮两人各进行一次操作，顺序如下：

1. Alice 从 `nums` 中移除当前的最小元素（最小数，minimum number）。  
2. Bob 再从剩余的 `nums` 中移除当前的最小元素。  
3. 将 Bob 移除的元素 **先** 追加到 `arr`（append），随后将 Alice 移除的元素追加到 `arr`。

游戏持续进行，直至 `nums` 为空，返回最终得到的数组 `arr`。

**示例 1**  
```text
Input: nums = [5,4,2,3]
Output: [3,2,5,4]
Explanation: 第 1 轮，Alice 先移除 2，Bob 再移除 3。随后 Bob 先将 3 追加到 arr，Alice 再将 2 追加，得到 arr = [3,2]。  
第 2 轮，此时 nums = [5,4]，Alice 移除 4，Bob 移除 5，依次追加后 arr 变为 [3,2,5,4]。
```

**示例 2**  
```text
Input: nums = [2,5]
Output: [5,2]
Explanation: 第 1 轮，Alice 移除 2，Bob 移除 5。Bob 先追加 5，随后 Alice 追加 2，得到 arr = [5,2]。
```

**约束条件**  
- `2 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`  
- `nums.length` 为偶数 (`nums.length % 2 == 0`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目说 **每轮** 都要进行两次“删除”操作：  
1. **Alice** 先把 `nums` 中的最小值挑走。  
2. **Bob** 再把剩下的 `nums` 中的最小值挑走。  

随后 **Bob 先把自己挑走的数放进 `arr`，Alice 再把自己的数放进 `arr`**。  
整个过程一直进行到 `nums` 为空为止。

> **类比**：想象你有一堆纸条，上面写着数字。Alice 像老师先把最短的纸条收走，Bob 再把剩下的最短纸条收走。收走后，Bob 把自己的纸条先贴到黑板上，老师（Alice）再贴自己的。  

因为每次都要找 **当前最小的** 元素，最直接的做法就是 **遍历数组一次找最小值**，把它删掉（或标记为已使用），再遍历一次找第二小的。重复 `n/2` 轮即可得到答案。

这种方法的正确性来源于题目给出的规则：每轮只能删掉当前最小的两个数，且 Bob 的数先写入结果。只要我们每轮都严格遵循这两步，最终得到的 `arr` 必然是题目要求的。

#### 代码（Python）

```python
def minNumberGame_bruteforce(nums):
    # 为了不修改原数组，拷贝一份
    nums = nums[:]               # 复制列表，防止外部数据被破坏
    arr = []                     # 最终结果

    # 只要还有元素，就继续进行回合
    while nums:
        # ---------- Alice 选最小 ----------
        min_a = min(nums)        # O(len(nums))，遍历一次找最小
        nums.remove(min_a)       # 删除该元素，列表会自动收缩

        # ---------- Bob 选最小 ----------
        min_b = min(nums)        # 再次遍历找最小
        nums.remove(min_b)       # 删除

        # ---------- 按顺序写入结果 ----------
        arr.append(min_b)        # Bob 的数先放
        arr.append(min_a)        # 再放 Alice 的数

    return arr
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每轮要遍历一次数组找最小值（`O(k)`），删掉后数组长度减 2。总共大约 `n/2` 轮，求和得到 `n + (n‑2) + (n‑4) + … ≈ n²/2`，所以是二次时间。  
  - 大白话：如果数组有 100 个数，最差情况下大约要比较 5,000 次左右。

- **空间复杂度**：`O(1)`（不计输出数组 `arr`）  
  - 只用了常数级的额外变量 `min_a、min_b`，没有额外的和输入规模相关的存储。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每轮都要**线性扫描寻找最小值**。如果我们提前把所有数排好序，就不需要每次再找最小了——因为排好序后，最小的两个数一定是相邻的。

**关键观察**：

1. 把 `nums` 按 **升序** 排列。  
   - 排好序后，数组的前两个元素就是本轮 Alice 与 Bob 要挑走的最小数。  
2. 题目要求 **Bob 的数先写入 `arr`，再写 Alice 的数**。  
   - 所以对于排好序的每一对相邻元素 `(a[i], a[i+1])`，我们应该把 `a[i+1]`（Bob）放在前面，`a[i]`（Alice）放在后面。  

于是只要 **一次排序**（`O(n log n)`），再 **一次线性遍历**，把相邻两数顺序调换加入结果，即可得到最终数组。

> **类比**：把所有纸条先按照数字从小到大排成一列（像排队），然后每次让排在前面的两个人（Alice、Bob）依次把自己的纸条贴到黑板上——但因为 Bob 要先贴，所以我们把这对纸条的顺序调换一下再贴。

#### 代码（Python）

```python
def minNumberGame_optimal(nums):
    # 1. 先把所有数升序排列
    nums.sort()                 # O(n log n) 的排序

    arr = []                    # 用来存放答案

    # 2. 每次取相邻的两个数，调换顺序加入 arr
    #    i 指向 Alice 的数（较小的），i+1 指向 Bob 的数（稍大一点）
    for i in range(0, len(nums), 2):
        arr.append(nums[i + 1])   # 先放 Bob 的数
        arr.append(nums[i])       # 再放 Alice 的数

    return arr
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序是最耗时的步骤，时间复杂度是 `n log n`（对数 * n）。  
  - 大白话：如果有 100 个数，排序大约只需要几千次比较，远比暴力的几万次要快。

- **空间复杂度**：`O(1)`（不计输出数组）  
  - 只用了常数级的额外变量 `arr`（如果把结果直接写回原数组，也可以做到原地），没有额外的和 `n` 成正比的存储。

---

## 心得

- **核心技巧**：先排序，再把相邻元素调换顺序（**相邻交换**）。  
- **适用场景**：  
  1. 需要**每次取当前最小/最大**的两元素并按特定顺序输出的题目（例如 “Minimum Number Game”。）  
  2. 需要**把数组分成若干对**，且每对内部顺序要调换的题目（如 “Array Partition I/II”。）  
  3. **排序 + 直接映射** 的思路在很多 “按大小分组” 的题目里都有用。  

> **一句话总结**：先把所有数排好序，随后把相邻的两数换个位置加入答案——排序一次，解题即止。

---

## 反思

- **第一反应**：看到“一轮两次删除最小数”，自然想到**每次遍历找最小**，于是写出了暴力实现。  
- **最容易踩的坑**：  
  - **忘记 Bob 先写入**，导致结果顺序颠倒。  
  - **边界条件**：数组长度一定是偶数，但若不注意 `i+1` 越界会报错。  
  - **原地修改**时要注意 `sort()` 会改变原数组，若题目要求保留原数据需先拷贝。  
- **下次遇到类似题**：第一步先思考**是否可以一次性排序**，把“每轮取最小/最大”转化为“取相邻元素”。若能，就立刻走向 **排序 + 线性遍历** 的路线。