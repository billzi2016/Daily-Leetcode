# #739. 每日温度 / Daily Temperatures

> 难度：中等 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/daily-temperatures/)

---

## 题目（英文原版）

**Description**

Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

**Examples**

**Example 1:**

```
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

**Example 2:**

```
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
```

**Example 3:**

```
Input: temperatures = [30,60,90]
Output: [1,1,0]
```

**Constraints**

- 1 <= temperatures.length <= 105
- 30 <= temperatures[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组（array）`temperatures`，其中 `temperatures[i]` 表示第 `i` 天的气温，返回一个数组（array）`answer`，使得 `answer[i]` 为第 `i` 天之后需要等待的天数，才能出现更高的气温。如果之后不存在更高的气温，则 `answer[i]` 为 `0`。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**

- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

**示例**

示例 1:  
输入: `temperatures = [73,74,75,71,69,72,76,73]`  
输出: `[1,1,4,2,1,1,0,0]`

示例 2:  
输入: `temperatures = [30,40,50,60]`  
输出: `[1,1,1,0]`

示例 3:  
输入: `temperatures = [30,60,90]`  
输出: `[1,1,0]`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一天 i，往后逐个检查后面的温度，直到找到比 `temperatures[i]` 更高的那一天**，记录下相隔的天数。如果遍历到数组末尾都没有更高的温度，就把答案设为 0。  

- **使用的数据结构**：只需要原数组 `temperatures` 和一个同长度的答案数组 `answer`。这就像我们在生活中翻看一本日记本：从今天往后翻，每翻一页就相当于检查一天的温度。  
- **为什么正确**：因为我们真的把“以后每一天”都检查了一遍，只要找到第一个更高的温度，那个天数就是答案；如果没有找到，说明以后再也不会更热，答案自然是 0。  

**时间/空间复杂度**：  
- 对第 `i` 天，我们最坏要检查 `n‑i‑1` 天（`n` 为总天数），于是所有天数的检查次数是 `n-1 + n-2 + … + 1 = n·(n‑1)/2`，大约是 `n²/2`，所以时间复杂度记作 **O(n²)**。这里的 O(n²) 可以想象成“如果有 10,000 天，最坏情况下要做大约 100,000,000 次比较”。  
- 只用了额外的答案数组，长度为 `n`，所以空间复杂度是 **O(n)**。  

#### 代码（Python）  

```python
def dailyTemperatures_brute(temperatures):
    n = len(temperatures)                 # 天数
    answer = [0] * n                      # 初始化答案，全为 0

    for i in range(n):                    # 从第 0 天遍历到第 n-1 天
        # 从 i+1 开始往后找第一个更大的温度
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i        # 记录相隔的天数
                break                    # 找到后立刻退出内层循环
        # 如果内部循环跑完都没 break，answer[i] 本来就是 0
    return answer
```

#### 复杂度  

- **时间复杂度**：O(n²) —— 两层循环，外层 n 次，内层最坏也要遍历 n 次，整体是“平方级”。  
- **空间复杂度**：O(n) —— 只额外用了一个长度为 n 的答案数组。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**主要的瓶颈在于每一天都要向后遍历很多次**。如果我们能够在遍历一次数组的过程中，直接知道“最近的更高温度”在哪儿，就能把时间降到线性 O(n)。  

**单调栈（Monotonic Stack）** 正好能帮我们做到这一点。  

1. **单调栈的概念**：把栈想成一个“只会递增（或递减）的纸牌堆”。这里我们维护一个 **递减栈**，栈里存放的是“**温度还没有找到更高天气的下标**”。  
   - 栈顶的温度永远是**当前还没有被“暖化”的最高温度**。  
   - 当我们遍历到新的一天 `i`，如果 `temperatures[i]` **大于**栈顶对应的温度，说明今天把栈顶那一天“暖了”。于是弹出栈顶下标 `prev`，`i - prev` 就是 `prev` 的答案。  
   - 继续比较，可能一次新温度会把栈里多个较低温度都暖化掉。  
2. **遍历顺序**：从左到右一次遍历所有天数。每遇到一个温度，就尝试把栈中所有比它小的温度“清空”。清空完后，把当前下标压进栈，表示它还在等待更高的天气。  
3. **为什么是单调递减**：因为一旦出现更高的温度，所有比它低的天数的答案已经确定，栈中只会保留温度**从栈底到栈顶递减**的下标，这样后面新来的更高温度才能一次性弹出所有需要解答的天数。  

**类比**：想象一条排队的顾客，每个人都想等比自己更热的天气。队列里的人温度从前到后是递减的。当出现更热的天气时，队首（最早且最冷的）的人可以立刻离开，记录等待天数；随后可能还有人也可以离开，直到队列里没有比当前温度更冷的顾客为止。  

#### 代码（Python）  

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n               # 最终答案，默认全 0
    stack = []                     # 单调递减栈，存放下标

    for i, cur_temp in enumerate(temperatures):
        # 当当前温度高于栈顶下标对应的温度时，弹出栈顶
        while stack and cur_temp > temperatures[stack[-1]]:
            prev_index = stack.pop()           # 弹出需要解答的下标
            answer[prev_index] = i - prev_index  # 等待的天数
        # 当前下标加入栈中，等待以后更高的温度
        stack.append(i)

    # 栈中剩余的下标对应的天数已经是 0（默认值），不需要额外处理
    return answer
```

#### 复杂度  

- **时间复杂度**：O(n) —— 每个下标最多被压栈一次、弹出一次，整个过程线性扫描。  
- **空间复杂度**：O(n) —— 最坏情况下栈里会保存所有下标（比如温度单调递减时），因此需要额外 O(n) 的空间。  

---  

## 心得  

- **核心技巧**：**单调栈**（Monotonic Stack），利用栈的 “后进先出” 特性一次性找出每个元素右侧第一个更大的值。  
- **适用的类似题型**：  
  1. **739. 每日温度**（本题）  
  2. **901. 股票价格跨度**（求每一天向前最近不低于当前价格的天数）  
  3. **84. 柱状图中最大的矩形**（利用单调栈快速求左右边界）  
- **一句话总结**：把“找右侧第一个更大”转化为“栈顶弹出直到不再更大”，一次遍历即可搞定。  

## 反思  

- **第一反应**：看到“每一天之后的更高温度”，立刻想到“双层循环”逐个比较。  
- **最容易踩的坑**：  
  - 忘记在循环结束后把答案数组默认的 0 保留下来（即没有更热的天数）。  
  - 栈的单调性写反了：如果写成递增栈，弹出的条件会错，导致答案全是 0。  
  - 边界条件：数组长度为 1 时，答案应为 `[0]`，代码必须能正确返回。  
- **下次类似题的第一步**：先判断“是否在寻找右侧（或左侧）第一个满足某种关系的元素”。如果是，立刻考虑 **单调栈**（递增或递减取决于关系）来一次遍历完成。