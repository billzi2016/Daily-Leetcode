# #1052. 脾气暴躁的书店老板 / Grumpy Bookstore Owner

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/grumpy-bookstore-owner/)

---

## 题目（英文原版）

**Description**

There is a bookstore owner that has a store open for n minutes. You are given an integer array customers of length n where customers[i] is the number of the customers that enter the store at the start of the ith minute and all those customers leave after the end of that minute.
During certain minutes, the bookstore owner is grumpy. You are given a binary array grumpy where grumpy[i] is 1 if the bookstore owner is grumpy during the ith minute, and is 0 otherwise.
When the bookstore owner is grumpy, the customers entering during that minute are not satisfied. Otherwise, they are satisfied.
The bookstore owner knows a secret technique to remain not grumpy for minutes consecutive minutes, but this technique can only be used once.
Return the maximum number of customers that can be satisfied throughout the day.

**Examples**

**Example 1:**

```
Input: customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3
Output: 16
Explanation:
The bookstore owner keeps themselves not grumpy for the last 3 minutes.
The maximum number of customers that can be satisfied = 1 + 1 + 1 + 1 + 7 + 5 = 16.
```

**Example 2:**

```
Input: customers = [1], grumpy = [0], minutes = 1
Output: 1
```

**Constraints**

- n == customers.length == grumpy.length
- 1 <= minutes <= n <= 2 * 104
- 0 <= customers[i] <= 1000
- grumpy[i] is either 0 or 1.

---

## 题目（中文翻译）

有一家书店在 **n** 分钟内营业。给定一个长度为 **n** 的整数数组（integer array）`customers`，其中 `customers[i]` 表示第 **i** 分钟开始时进入书店的顾客数量，这些顾客会在该分钟结束后离开。

在某些分钟，书店老板会情绪暴躁。给定一个二进制数组（binary array）`grumpy`，其中 `grumpy[i]` 为 `1` 表示第 **i** 分钟老板情绪暴躁，为 `0` 表示不暴躁。

当老板情绪暴躁时，该分钟进入的顾客会不满意；否则他们会满意。

老板掌握一种只能使用一次的 **秘密技巧（secret technique）**，可以让自己在 **minutes** 分钟内保持不暴躁（即连续的 **minutes** 分钟）。

返回一天结束时能够满意的顾客的最大可能数量。

---

### 示例

#### 示例 1
**输入**  
`customers = [1,0,1,2,1,1,7,5]`  
`grumpy = [0,1,0,1,0,1,0,1]`  
`minutes = 3`

**输出**  
`16`

**解释**  
书店老板在最后的 3 分钟内保持不暴躁。能够满意的顾客总数 = 1 + 1 + 1 + 1 + 7 + 5 = 16。

#### 示例 2
**输入**  
`customers = [1]`  
`grumpy = [0]`  
`minutes = 1`

**输出**  
`1`

---

### 约束条件
- `n == customers.length == grumpy.length`
- `1 <= minutes <= n <= 2 * 10^4`
- `0 <= customers[i] <= 1000`
- `grumpy[i]` 只能是 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们先把题目想成“一天里每分钟有多少顾客会满意”。  
- 如果第 `i` 分钟老板不生气（`grumpy[i] == 0`），不管有没有使用秘技，这些顾客一定满意。  
- 如果第 `i` 分钟老板生气（`grumpy[i] == 1`），只有在我们把秘技的“免生气”窗口覆盖到这分钟时，这些顾客才会变满意。  

暴力做法就是枚举所有可能的窗口起点 `start`（窗口长度固定为 `minutes`），  
计算在该窗口内 **把生气的分钟都变成不生气** 后，整个一天能让多少顾客满意，取最大值。

> 类比：想象我们有一本字典（哈希表），`grumpy` 就像是字典里标记的“红色单词”。  
> 我们一次只能把连续的 `minutes` 个红色单词涂成蓝色，使它们变成“正常”。  
> 暴力解就是把字典的每个可能的起始位置都尝试一次，看看涂完后能得到多少蓝色单词。

正确性：  
- 每一种合法的使用方式（即窗口的起点）我们都算了一遍，必然能找到最大值。  

时间/空间复杂度：  
- 枚举窗口起点 `O(n)`，每次遍历整个数组计算满意人数 `O(n)`，总计 `O(n²)`。  
  用大白话说，如果 `n = 10000`，程序大约要跑 1 亿次循环，可能会很慢。  
- 只使用了几个整数变量，空间是 `O(1)`（常数级），不随 `n` 增长。

#### 代码（Python）

```python
def maxSatisfied_brute(customers, grumpy, minutes):
    n = len(customers)
    # 先算出不需要任何秘技时已经满意的顾客数
    base = 0
    for i in range(n):
        if grumpy[i] == 0:          # 老板本来不生气
            base += customers[i]

    best = base                     # 最终答案的初始值

    # 枚举窗口左端点 start，窗口长度固定为 minutes
    for start in range(n - minutes + 1):
        extra = 0                   # 这一次使用窗口能额外让多少不满意的顾客满意
        for j in range(start, start + minutes):
            if grumpy[j] == 1:      # 只有原本生气的分钟才会产生额外收益
                extra += customers[j]
        best = max(best, base + extra)

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 这里的 `n²` 表示“数组长度的平方”。如果 `n` 是 20000，时间大约是 400 000 000 步，远超 1 秒的限制。  
- **空间复杂度**：`O(1)` —— 只用了常量个整数变量，不会随 `n` 增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次窗口都重新遍历 `minutes` 长度的区间**，导致 `O(n·minutes)`，最坏情况下等价于 `O(n²)`。  
观察可以发现：

- 已经满意的顾客（`grumpy[i] == 0`）**不受窗口位置影响**，它们的贡献是固定的 `base`（同上）。  
- 只有窗口覆盖的 **生气的分钟**（`grumpy[i] == 1`）才会产生“额外满意” 的增益。  
- 因此我们只需要在所有长度为 `minutes` 的窗口里，**快速求出窗口内部 `grumpy[i] == 1` 的顾客总数**，取最大值即可。

这正是**滑动窗口**的典型应用：  
1. 先算出窗口 `[0, minutes-1]` 内的增益 `window_gain`。  
2. 窗口向右滑动一格时，左边界离开窗口，右边界进入窗口。  
   - 如果左边界的 `grumpy` 为 1，则减去对应的 `customers`（因为这部分不再受秘技保护）。  
   - 如果右边界的 `grumpy` 为 1，则加上对应的 `customers`（新加入的生气分钟被覆盖）。  
3. 每一步更新 `max_gain = max(max_gain, window_gain)`。  

这样只遍历一次数组，时间降到 `O(n)`。

> 类比：想象一根长度固定的扫帚在地上来回拖动，地上散落的“脏点”对应 `grumpy[i]==1` 的顾客。  
> 我们每次只需要关注扫帚覆盖的区域里有多少脏点被扫掉，而不是每次重新数全场。扫帚每向前一步，只要把左边离开的脏点减掉，右边进来的脏点加上，就得到新的结果。

#### 代码（Python）

```python
def maxSatisfied(customers, grumpy, minutes):
    n = len(customers)

    # 1️⃣ 计算原本不生气时已经满意的顾客数（固定不变）
    base = 0
    for i in range(n):
        if grumpy[i] == 0:
            base += customers[i]

    # 2️⃣ 计算第一个窗口 [0, minutes-1] 内，使用秘技能额外满意的顾客数
    window_gain = 0
    for i in range(minutes):
        if grumpy[i] == 1:          # 只有生气的分钟才算增益
            window_gain += customers[i]

    max_gain = window_gain          # 记录出现过的最大增益

    # 3️⃣ 滑动窗口：窗口左端点从 1 移动到 n-minutes
    for left in range(1, n - minutes + 1):
        # 移出窗口的左边界
        if grumpy[left - 1] == 1:
            window_gain -= customers[left - 1]

        # 新进入窗口的右边界
        right = left + minutes - 1
        if grumpy[right] == 1:
            window_gain += customers[right]

        # 更新最大增益
        if window_gain > max_gain:
            max_gain = window_gain

    # 4️⃣ 最终答案 = 原本满意的 + 最佳增益
    return base + max_gain
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历数组两遍（一次算 `base`，一次滑动窗口），即使 `n = 20000` 也只需要约 4 万次操作，几乎瞬间完成。  
- **空间复杂度**：`O(1)` —— 只用几个整数变量，额外内存不随 `n` 增长。

---

## 心得  

- **核心技巧**：滑动窗口（Sliding Window）。  
- **适用的题型**：  
  1. “最大子数组和”类问题（如 LeetCode 209. 长度最小子数组）。  
  2. “固定长度窗口内的最大/最小值”类（如 LeetCode 239. 滑动窗口最大值）。  
  3. “在数组中找最长满足条件的子串”类（如 LeetCode 424. 替换后的最长重复字符）。  
- **一句话总结**：把“一次性全部枚举”换成“窗口只移动一步，增减局部”，即可把二次方降到线性。

---

## 反思  

- **第一反应**：看到“只能使用一次、长度固定”，第一想法就是枚举所有起点，写出暴力解。  
- **最容易踩的坑**：  
  - 忘记把本来就满意的顾客（`grumpy[i]==0`）计入最终答案，只算了窗口增益。  
  - 边界处理不严谨：窗口右端点的索引 `right = left + minutes - 1` 必须在数组范围内，否则会越界。  
  - `minutes` 可能等于 `n`，此时窗口只能放在唯一位置，需要代码能兼容这种情况。  
- **下次遇到同类题**：第一步先**把“固定不变的部分”剥离出来**（这里是 `base`），再**思考如何在 O(1) 时间内更新“可变窗口”的价值**，滑动窗口往往是最直接的思路。