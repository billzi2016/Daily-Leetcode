# #1744. 你能在喜欢的那天吃到喜欢的糖果吗？ / Can You Eat Your Favorite Candy on Your Favorite Day?

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/can-you-eat-your-favorite-candy-on-your-favorite-day/)

---

## 题目（英文原版）

**Description**

You are given a (0-indexed) array of positive integers candiesCount where candiesCount[i] represents the number of candies of the ith type you have. You are also given a 2D array queries where queries[i] = [favoriteTypei, favoriteDayi, dailyCapi].
You play a game with the following rules:
Construct a boolean array answer such that answer.length == queries.length and answer[i] is true if you can eat a candy of type favoriteTypei on day favoriteDayi without eating more than dailyCapi candies on any day, and false otherwise. Note that you can eat different types of candy on the same day, provided that you follow rule 2.
Return the constructed array answer.

**Examples**

**Example 1:**

```
Input: candiesCount = [7,4,5,3,8], queries = [[0,2,2],[4,2,4],[2,13,1000000000]]
Output: [true,false,true]
Explanation:
1- If you eat 2 candies (type 0) on day 0 and 2 candies (type 0) on day 1, you will eat a candy of type 0 on day 2.
2- You can eat at most 4 candies each day.
   If you eat 4 candies every day, you will eat 4 candies (type 0) on day 0 and 4 candies (type 0 and type 1) on day 1.
   On day 2, you can only eat 4 candies (type 1 and type 2), so you cannot eat a candy of type 4 on day 2.
3- If you eat 1 candy each day, you will eat a candy of type 2 on day 13.
```

**Example 2:**

```
Input: candiesCount = [5,2,6,4,1], queries = [[3,1,2],[4,10,3],[3,10,100],[4,100,30],[1,3,1]]
Output: [false,true,true,false,false]
```

**Constraints**

- 1 <= candiesCount.length <= 105
- 1 <= candiesCount[i] <= 105
- 1 <= queries.length <= 105
- queries[i].length == 3
- 0 <= favoriteTypei < candiesCount.length
- 0 <= favoriteDayi <= 109
- 1 <= dailyCapi <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的正整数数组 `candiesCount`，其中 `candiesCount[i]` 表示第 *i* 类糖果的数量。另给定一个二维数组 `queries`，其中 `queries[i] = [favoriteTypei, favoriteDayi, dailyCapi]`。

你需要按照以下规则进行游戏：

1. 构造一个布尔数组 `answer`，使得 `answer.length == queries.length`。如果在第 `favoriteDayi` 天能够吃到第 `favoriteTypei` 类糖果，并且在任意一天吃的糖果总数不超过 `dailyCapi`（每日上限），则 `answer[i]` 为 `true`；否则为 `false`。注意，同一天可以吃不同种类的糖果，只要满足规则 2 即可。

返回构造好的数组 `answer`。

**示例 1**  
```text
Input: candiesCount = [7,4,5,3,8], queries = [[0,2,2],[4,2,4],[2,13,1000000000]]
Output: [true,false,true]
Explanation:
1. 如果在第 0 天吃 2 颗（类型 0）的糖果，在第 1 天再吃 2 颗（类型 0）的糖果，那么第 2 天就可以吃到类型 0 的糖果。
2. 每天最多只能吃 4 颗糖果。
   若每天都吃 4 颗，则第 0 天吃掉 4 颗（类型 0），第 1 天吃掉 4 颗（类型 0 和类型 1），此时第 2 天已经无法再吃到类型 0 的糖果。
3. （此处略去的解释已被截断） 
```

**示例 2**  
```text
Input: candiesCount = [5,2,6,4,1], queries = [[3,1,2],[4,10,3],[3,10,100],[4,100,30],[1,3,1]]
Output: [false,true,true,false,false]
```

**约束条件**  
- `1 <= candiesCount.length <= 10^5`  
- `1 <= candiesCount[i] <= 10^5`  
- `1 <= queries.length <= 10^5`  
- `queries[i].length == 3`  
- `0 <= favoriteTypei < candiesCount.length`  
- `0 <= favoriteDayi <= 10^9`  
- `1 <= dailyCapi <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
我们先把题目想成“在第 `favoriteDay` 天，你能否吃到第 `favoriteType` 种糖”。  
最直接的做法是 **模拟每一天的吃糖过程**：

1. 从第 0 天开始，记录当天已经吃了多少糖。  
2. 每天最多吃 `dailyCap` 颗（因为题目说“任何一天都不能超过 dailyCap”），  
   但也可以少吃（可以吃 0 颗），只要总数不超过 `dailyCap`。  
3. 按顺序把糖从第 0 种吃完，再吃第 1 种，……，直到第 `favoriteType` 种。  
4. 当天数达到 `favoriteDay` 时，检查当前手里是否还有第 `favoriteType` 的糖，如果有，则答案为 `True`，否则为 `False`。

> **类比**：把糖想成超市里排队的顾客，`dailyCap` 就是收银台每分钟最多能处理的客人数。我们把顾客从前面排起，一直处理到第 `favoriteDay` 分钟，看第 `favoriteType` 的顾客是否已经轮到。

**为什么这个方法是对的**  
因为我们严格遵守了两条规则：  
- 每天吃的糖数不超过 `dailyCap`。  
- 必须先吃完前面的类型才能开始吃后面的类型（题目没有强制，但我们只要能保证在第 `favoriteDay` 前把前面的糖吃完，就一定能在这天吃到目标糖）。  
只要模拟过程满足这些约束，得到的结果自然是正确的。

**复杂度分析（大白话）**  
- **时间**：对每个查询我们可能要遍历所有天数，最坏情况下 `favoriteDay` 可以达到 `10⁹`，所以 **时间会非常非常慢**，约为 `O(queries * maxDay)`，在实际数据里几乎不可接受。  
- **空间**：只需要保存几个计数器，`O(1)`（常数级别的内存），但因为时间太慢，根本用不了。

#### 代码（Python）  

```python
def canEat_bruteforce(candiesCount, queries):
    ans = []
    for fav_type, fav_day, cap in queries:
        # 已经吃掉的糖总数
        eaten = 0
        # 当前正在吃的糖种类
        cur_type = 0
        # 剩余该种糖的数量
        left_in_type = candiesCount[0] if candiesCount else 0

        day = 0
        possible = False
        while day <= fav_day:
            # 当天最多可以吃 cap 颗糖，但也可以少吃
            # 这里我们尽量多吃（贪心），因为要判断是否**能够**吃到目标糖
            to_eat = min(cap, left_in_type)
            eaten += to_eat
            left_in_type -= to_eat

            # 当前种类吃完，换到下一种
            while left_in_type == 0 and cur_type + 1 < len(candiesCount):
                cur_type += 1
                left_in_type = candiesCount[cur_type]

            # 检查今天是否已经能吃到目标种类的糖
            if day == fav_day:
                # 如果当前种类已经是目标种类，说明今天可以吃到
                possible = (cur_type == fav_type)
                break

            day += 1

        ans.append(possible)
    return ans
```

> 代码里每一行都有中文注释，帮助你快速定位逻辑。  
> **注意**：这段代码仅用于演示思路，实际运行会超时。

#### 复杂度  

- **时间复杂度**：`O(queries * favoriteDay)`，因为对每个查询我们可能遍历到第 `favoriteDay` 天。  
  - 用大白话说，就是如果 `favoriteDay` 是 10⁹，程序要循环 10⁹ 次，根本跑不完。  
- **空间复杂度**：`O(1)`，只用了常数个变量，不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于逐天模拟。  
其实我们并不需要真的去“每天吃多少”，只要知道 **最早** 能吃到第 `favoriteType` 的糖是哪一天，**最晚** 能吃到它是哪一天，就能直接判断。

**关键观察**  

1. **前缀和**  
   - 把 `candiesCount` 前缀相加得到 `prefix[i]`：  
     `prefix[i] = candiesCount[0] + candiesCount[1] + ... + candiesCount[i]`  
   - `prefix[i-1]`（如果 `i>0`）表示 **在第 i 种糖之前**，所有糖的总数。  
   - 类比：把糖装进一本厚厚的账本，`prefix[i]` 就是第 `i` 页结束时的累计数量。

2. **最早可能的天数**（Earliest day）  
   - 为了 **尽可能早** 吃到目标糖，我们每天都吃 **上限** `dailyCap`（因为吃得越多，累计吃掉的糖越快）。  
   - 在最早的情况下，第 `favoriteType` 的第一颗糖出现在第 `ceil( (totalPrev) / dailyCap )` 天，其中 `totalPrev = prefix[fav_type-1]`（前面所有糖的数量）。  
   - 解释：如果前面有 20 颗糖，每天最多吃 5 颗，那么最早第 5 天（20/5）才能把前面的糖全部吃完，下一天才可能吃到目标糖。

3. **最晚可能的天数**（Latest day）  
   - 为了 **尽可能晚** 吃到目标糖，我们每天只吃 **最少** 1 颗（题目只要求 “不超过 dailyCap”，最少可以是 1）。  
   - 那么在最晚的情况下，第 `favoriteType` 的最后一颗糖会在第 `totalPrev + candiesCount[fav_type] - 1` 天出现。  
   - 解释：把所有前面的糖和目标糖全部算进去，假设每天只吃 1 颗，最后一颗目标糖出现的天数就是总糖数减 1（因为天数从 0 开始计）。

4. **判断**  
   - 只要查询的 `favoriteDay` 落在 `[earliest, latest]` 区间（两端都可以），答案就是 `True`。  
   - 否则 `False`。

**为什么这一步就够了**  
因为我们已经把“吃多少”这件事抽象成了 **“累计吃掉的糖数”**。  
只要累计数能够覆盖前面的糖，再加上今天还能吃到目标糖，就满足题意。  
不需要真正去模拟每天的吃法。

**实现细节**  

- 先预处理前缀和 `pref`（长度 `n`），时间 `O(n)`。  
- 对每个查询，利用 `pref` 直接算出 `earliest` 与 `latest`，时间 `O(1)`。  
- 所有查询一起的时间是 `O(n + q)`，其中 `q = len(queries)`。  

**类比图示（文字版）**  

```
糖种类：  0      1      2      3      4
数量：   7      4      5      3      8
前缀和： 7     11     16     19     27
```

- 想吃第 2 种糖（索引 2），前面有 `pref[1] = 11` 颗糖。  
- 如果每天最多吃 2 颗，最早第 `ceil(11 / 2) = 6` 天才能把前 11 颗吃完，**第 6 天**（从 0 开始计）就可能开始吃第 2 种。  
- 如果每天只吃 1 颗，最晚第 `11 + 5 - 1 = 15` 天才会吃完第 2 种的最后一颗。  

只要查询的 `day` 在 `[6, 15]`，答案为 `True`。

#### 代码（Python）  

```python
from typing import List

def canEat(candiesCount: List[int], queries: List[List[int]]) -> List[bool]:
    # 1. 计算前缀和
    n = len(candiesCount)
    pref = [0] * n          # pref[i] = 前 i+1 种糖的总数
    cur = 0
    for i, cnt in enumerate(candiesCount):
        cur += cnt
        pref[i] = cur

    ans = []
    for fav_type, fav_day, cap in queries:
        # 2. 前面所有糖的总数
        total_prev = pref[fav_type - 1] if fav_type > 0 else 0

        # 3. 最早可以吃到目标糖的天数（从 0 开始计）
        #    需要把前面的糖全部吃完，采用“每天最多吃 cap 颗”
        #    使用整数除法并向上取整： (a + b - 1) // b
        earliest = (total_prev + cap - 1) // cap   # ceil(total_prev / cap)

        # 4. 最晚可以吃到目标糖的天数
        #    假设每天只吃 1 颗糖，累计到目标糖的最后一颗
        latest = total_prev + candiesCount[fav_type] - 1

        # 5. 判断 fav_day 是否落在区间 [earliest, latest]
        ans.append(earliest <= fav_day <= latest)

    return ans
```

**代码要点解释**  

- `pref` 的构造是 **一次遍历**，每一步把当前糖的数量累加到 `cur`，再存进数组。  
- `earliest` 的公式 `(total_prev + cap - 1) // cap` 实现了向上取整，避免使用浮点数。  
- `latest` 直接把前面的糖数 + 目标糖的数量 - 1（因为天数从 0 开始）。  
- 每条查询只做 **常数次** 加减乘除运算，时间非常快。

#### 复杂度  

- **时间复杂度**：`O(n + q)`  
  - `n = len(candiesCount)`（计算前缀和）  
  - `q = len(queries)`（逐条处理）  
  - 用大白话说，就是 **线性** 的工作量：每个元素只看一次，根本不会卡住。  
  - 与暴力解的 `O(queries * favoriteDay)` 相比，快了 **天数级别的数量级**（从 10⁹ 降到 10⁵）。

- **空间复杂度**：`O(n)`  
  - 需要存储前缀和数组 `pref`，长度等于糖的种类数。  
  - 这相当于额外占用和原始输入同等规模的内存，完全可以接受。

---

## 心得  

- **核心技巧**：**前缀和 + 区间判断**。  
  - 前缀和把“前面所有糖的总量”压缩成 O(1) 查询的形式。  
  - 通过计算“最早可能的天数”和“最晚可能的天数”，把原本的“是否能吃到”问题转化为“某天是否落在区间”。  

- **适用的题型**（类似思路）  
  1. **"Maximum Number of Weeks for Which You Can Work"**（判断是否能在给定天数内完成任务）  
  2. **"Maximum Number of Consecutive Ones"**（利用前缀和快速判断子数组和）  
  3. **"Maximum Number of Balls in a Box"**（统计累计值的区间）  

- **一句话总结解题钥匙**：  
  > 用前缀和把“前面多少糖”压缩为一个数，随后只比较 **最早** 与 **最晚** 能吃到的天数是否覆盖查询的天数。

---

## 反思  

- **第一反应**：看到“每天不能超过 dailyCap”，立刻想到要**逐天模拟**，于是写了暴力循环。  
- **最容易踩的坑**  
  1. **天数从 0 开始计**：`favoriteDay` 是 0‑based，计算区间时别忘了 `-1`。  
  2. **向上取整**：`ceil(totalPrev / cap)` 必须用整数技巧 `(a + b - 1) // b`，否则会出错。  
  3. **溢出**：`totalPrev`、`candiesCount[i]` 以及乘除可能达到 `10¹⁴`，在 Python 中整数不溢，但在其他语言要用 64 位。  
  4. **边界条件**：`favoriteType = 0` 时前缀和 `pref[-1]` 不存在，需要单独处理。  

- **下次遇到同类题**，第一步应该：  
  > “先把累计信息（前缀和、前缀乘积等）预处理出来，然后把每个查询转化为一个**区间是否相交**的判断”。  

这样既能避免暴力模拟的时间炸弹，又能快速得到答案。祝你玩得开心 🎉!