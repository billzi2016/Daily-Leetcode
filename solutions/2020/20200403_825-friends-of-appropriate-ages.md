# #825. 适龄好友请求 / Friends Of Appropriate Ages

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/friends-of-appropriate-ages/)

---

## 题目（英文原版）

**Description**

There are n persons on a social media website. You are given an integer array ages where ages[i] is the age of the ith person.
A Person x will not send a friend request to a person y (x != y) if any of the following conditions is true:
Otherwise, x will send a friend request to y.
Note that if x sends a request to y, y will not necessarily send a request to x. Also, a person will not send a friend request to themself.
Return the total number of friend requests made.

**Examples**

**Example 1:**

```
Input: ages = [16,16]
Output: 2
Explanation: 2 people friend request each other.
```

**Example 2:**

```
Input: ages = [16,17,18]
Output: 2
Explanation: Friend requests are made 17 -> 16, 18 -> 17.
```

**Example 3:**

```
Input: ages = [20,30,100,110,120]
Output: 3
Explanation: Friend requests are made 110 -> 100, 120 -> 110, 120 -> 100.
```

**Constraints**

- n == ages.length
- 1 <= n <= 2 * 104
- 1 <= ages[i] <= 120

---

## 题目（中文翻译）

有 n 位用户在一个社交媒体网站上。给定一个整数数组 `ages`，其中 `ages[i]` 表示第 i 位用户的年龄。

若满足以下任意条件，则用户 x（`x != y`）不会向用户 y 发送好友请求（friend request）：

- `ages[y] <= 0.5 * ages[x] + 7`
- `ages[y] > ages[x]`
- `ages[y] > 100` 且 `ages[x] < 100`

否则，x 将向 y 发送好友请求。需要注意的是：

- 若 x 向 y 发送请求，y 不一定会向 x 发送请求；
- 同一用户不会向自己发送请求。

返回所有发送的好友请求总数。

**示例 1**  
Input: `ages = [16,16]`  
Output: `2`  
Explanation: 两个人互相发送好友请求。

**示例 2**  
Input: `ages = [16,17,18]`  
Output: `2`  
Explanation: 发送的好友请求为 `17 -> 16`，`18 -> 17`。

**示例 3**  
Input: `ages = [20,30,100,110,120]`  
Output: `3`  
Explanation: 发送的好友请求为 `110 -> 100`，`120 -> 110`，`120 -> 100`。

**约束条件**

- `n == ages.length`
- `1 <= n <= 2 * 10^4`
- `1 <= ages[i] <= 120`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把每个人和每个人（除自己）都配对一次，检查题目给出的三个“不发送请求”的条件是否成立。如果这三个条件 **全部不成立**，说明可以发送请求，就把计数器加一。  

- **数据结构**：只需要用到普通的 Python 列表 `ages`，以及两个整数循环变量 `i`、`j`。可以把它想象成在 **朋友圈里逐个敲门**，看对方是否满足年龄要求。  
- **正确性**：因为我们枚举了所有可能的 (x, y) 有序对（x≠y），只要对每一对都严格按照题目规则判断，就一定不会漏掉也不会多算。  

#### 代码（Python）  

```python
from typing import List

def numFriendRequests_bruteforce(ages: List[int]) -> int:
    n = len(ages)
    ans = 0
    for i in range(n):                # x 的下标
        for j in range(n):            # y 的下标
            if i == j:                 # 不能和自己请求
                continue
            age_x, age_y = ages[i], ages[j]

            # 三个“不发送请求”的条件
            if age_y <= 0.5 * age_x + 7:      # 条件 1
                continue
            if age_y > age_x:                # 条件 2
                continue
            if age_y > 100 and age_x < 100:  # 条件 3
                continue

            # 以上条件都不满足，说明可以发送请求
            ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 这里的 `n²` 可以读作“**n 的平方**”，也就是如果人数是 1000，循环大概要执行 1,000,000 次。  
- **空间复杂度**：`O(1)`。  
  - 只用了常数个额外变量，和输入规模无关。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每个人都要和每个人比较一次**，导致 `n²` 次判断。  
观察题目条件可以发现：

1. 条件 `age_y > age_x` 说明 **只可能向比自己年龄不大的（≤）的人发送请求**。  
2. 条件 `age_y <= 0.5 * age_x + 7` 只和 **x 的年龄** 有关，决定了一个 **最小可接受的年龄下界**。  
3. 条件 `age_y > 100 且 age_x < 100` 只在 **一方年龄超过 100、另一方不超过 100** 时阻止请求。

把所有年龄排好序后，**对于每个年龄 a = ages[i]**，我们只需要找出在排好序的数组中满足：

```
0.5 * a + 7 < age ≤ a            (并且不出现 (age > 100 且 a < 100) 的情况)
```

的所有 **左侧** 元素的数量。  
这正好可以用 **双指针**（Two Pointers）来完成：

- `left` 指向当前窗口的最左边（第一个满足 `age > 0.5 * a + 7` 的位置）。  
- `right`（即 `i`）是当前遍历到的元素。  

当 `ages[left]` 过小不满足下界时，左指针不断右移，直到满足。  
此时窗口 `[left, i)` 中的所有元素（不包括 `i` 本身）都可以收到来自 `i` 的请求。  
窗口大小 = `i - left`，但如果窗口中有和 `i` 年龄相同的 **多个人**，每个人都可以向窗口内的其他人发送请求（包括同龄的），所以我们直接把 `i - left` 加到答案中即可。  

因为年龄上限只有 120，排序的复杂度 `O(n log n)` 已经足够快；双指针遍历一次数组，时间 `O(n)`，整体 `O(n log n)`。

> **类比**：把排好序的年龄看成排好队的学生，老师要检查每个学生能否向前面的同学递交作业。只要把队首（不符合条件的）学生踢出队列，剩下的就是可以接受的同学。

#### 代码（Python）  

```python
from typing import List

def numFriendRequests(ages: List[int]) -> int:
    # 1. 排序，方便使用双指针
    ages.sort()
    n = len(ages)
    ans = 0
    left = 0                     # 窗口左边界

    for right in range(n):       # right 代表当前的 x（发送请求的人）
        age_x = ages[right]

        # 2. 把左指针右移，直到满足最小年龄下界
        #    只要 ages[left] <= 0.5 * age_x + 7，就不行，需要继续右移
        while left < right and ages[left] <= 0.5 * age_x + 7:
            left += 1

        # 3. 此时 (left, right) 之间的所有年龄都满足：
        #    ages[left] > 0.5*age_x + 7 且 ages[left] ≤ age_x
        #    但我们还要排除 “age_y > 100 且 age_x < 100” 的情况
        #    观察可得：只要 age_x < 100，窗口里所有年龄 ≤ age_x 都 ≤ 100，
        #    因此该条件自然满足；若 age_x ≥ 100，则条件 3 永远不阻止。
        #    所以不需要额外判断。

        # 4. 统计合法的 y（左闭右开区间），并累加
        #    注意：如果 left == right，说明没有符合条件的 y，此时 i-left 为 0。
        ans += right - left   # 不包括自己 (right)

    return ans
```

> **代码说明**  
- `ages.sort()`：把年龄从小到大排好序，类似把学生按身高排队。  
- `while ages[left] <= 0.5 * age_x + 7:`：左指针不断左移，直到窗口左端的年龄 **大于** “半年龄加 7”。这一步是 **过滤掉太小的朋友**。  
- `ans += right - left`：窗口大小即为满足条件的 y 的数量。因为 `right` 本身是 x，不能算在内，所以直接用差值。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `n log n` 来自排序（比如 20,000 人排序大约需要 20,000 × log₂20,000 ≈ 300,000 次比较），双指针遍历只要 `O(n)`，相当于 **线性**。相比暴力的 `n²`，提升非常明显。  
- **空间复杂度**：`O(1)`（不计排序本身的原地修改）  
  - 只用了几个整数指针 `left、right、ans`，不随输入规模增长。

---  

## 心得  

- **核心技巧**：利用 **排序 + 双指针** 把“年龄区间”转化为一个滑动窗口，快速统计符合条件的配对数。  
- **适用的类似题型**：  
  1. **“两个数组的相对大小”**（如 LeetCode 1122 `Relative Sort Array`）——需要在有序序列中找满足区间的元素。  
  2. **“区间内的数对”**（如 LeetCode 974 `Subarray Sums Divisible by K`）——使用前缀和+哈希或双指针。  
  3. **“满足距离约束的配对”**（如 LeetCode 881 `Boats to Save People`）——同样用双指针在排序后寻找合法区间。  
- **一句话总结解题钥匙**：**先把数据排好序，再用滑动窗口一次遍历把所有合法区间统计完**。

---  

## 反思  

- **第一反应**：看到“年龄条件”立刻想到**逐个比较**，于是写出暴力双循环的实现。  
- **最容易踩的坑**：  
  1. **条件的顺序**——忘记先判断 “太小” 再判断 “太大”，导致错误计数。  
  2. **自我请求**——忘记排除 `i == j`，会多算 `n` 次。  
  3. **年龄 >100 且 <100 的特殊规则**——如果不仔细推敲，容易遗漏或多写条件。  
- **下次遇到同类题**：第一步先**思考是否可以把“满足某区间的元素”转化为“在有序数组中找左、右边界”。如果可以，立刻考虑**排序 + 双指针**（或计数 + 前缀和）来把 `O(n²)` 降到 `O(n log n)` 或 `O(n)`。