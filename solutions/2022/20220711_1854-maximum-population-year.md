# #1854. 最大人口年份 / Maximum Population Year

> 难度：简单 · 标签：Array、Counting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-population-year/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array logs where each logs[i] = [birthi, deathi] indicates the birth and death years of the ith person.
The population of some year x is the number of people alive during that year. The ith person is counted in year x's population if x is in the inclusive range [birthi, deathi - 1]. Note that the person is not counted in the year that they die.
Return the earliest year with the maximum population.

**Examples**

**Example 1:**

```
Input: logs = [[1993,1999],[2000,2010]]
Output: 1993
Explanation: The maximum population is 1, and 1993 is the earliest year with this population.
```

**Example 2:**

```
Input: logs = [[1950,1961],[1960,1971],[1970,1981]]
Output: 1960
Explanation: 
The maximum population is 2, and it had happened in years 1960 and 1970.
The earlier year between them is 1960.
```

**Constraints**

- 1 <= logs.length <= 100
- 1950 <= birthi < deathi <= 2050

---

## 题目（中文翻译）

给定一个二维整数数组 `logs`，其中 `logs[i] = [birth_i, death_i]` 表示第 `i` 个人的出生年份和死亡年份。  
某一年 `x` 的人口（population）指的是在该年仍然存活的人的数量。若年份 `x` 落在 **闭区间** `[birth_i, death_i - 1]`（即 `birth_i ≤ x ≤ death_i - 1`）内，则第 `i` 个人会被计入年份 `x` 的人口。注意，死亡当年不计入人口。  

返回人口最多的最早年份。

## 示例

### 示例 1
**输入**: `logs = [[1993,1999],[2000,2010]]`  
**输出**: `1993`  
**解释**: 最大人口为 `1`，而 `1993` 是出现该人口的最早年份。

### 示例 2
**输入**: `logs = [[1950,1961],[1960,1971],[1970,1981]]`  
**输出**: `1960`  
**解释**:  
最大人口为 `2`，该人口出现在 `1960` 年和 `1970` 年。两者中较早的年份是 `1960`。

## 约束条件
- `1 <= logs.length <= 100`
- `1950 <= birth_i < death_i <= 2050`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一年都枚举一遍**，然后统计在该年还活着的人有多少。  
- **数据结构**：我们只需要一个普通的 `list`（数组）来保存 `logs`，再用一个整数计数器 `cnt` 来统计某一年的人数。  
- **生活化类比**：把年份想成一排排的教室，`logs[i]` 表示第 `i` 个人从出生教室走进学校，到死亡教室离开。我们要逐个教室（年份）走过去，看看有多少同学正在教室里。  

**为什么正确**：  
题目要求“在某一年 `x`，所有满足 `birth_i ≤ x < death_i` 的人都算在该年的总人口”。如果我们真的遍历每一年，并逐条检查每个人是否满足这个不等式，显然能得到每一年真实的在世人数。

#### 代码（Python）

```python
from typing import List

def maximumPopulation(logs: List[List[int]]) -> int:
    # 题目中年份范围是 1950 ~ 2050（闭区间），所以我们可以直接遍历这段区间
    earliest = 1950
    latest   = 2050

    max_pop = -1          # 记录出现过的最大人口数
    ans_year = earliest   # 记录对应的最早年份

    # 逐年检查
    for year in range(earliest, latest + 1):
        cnt = 0  # 当前 year 的在世人数

        # 检查每一条日志
        for birth, death in logs:
            # 人在 [birth, death) 区间内，即 birth <= year < death
            if birth <= year < death:
                cnt += 1

        # 更新最大值和对应的最早年份
        if cnt > max_pop:          # 出现更大的值就直接更新
            max_pop = cnt
            ans_year = year
        # 如果相等，题目要求最早的年份，不需要额外处理，因为我们是从小到大遍历的

    return ans_year
```

#### 复杂度

- **时间复杂度**：`O(Y * N)`，其中 `Y = 2050 - 1950 + 1 = 101` 是年份的总数，`N = len(logs)` 是人数。  
  用大白话说，就是**每一年都要遍历所有人**，如果有 100 个人，101 年，就要算 10,100 次。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（计数器、答案），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每一年都遍历所有人”**。我们可以把“每个人对哪些年份有贡献”提前算好，随后只需要一次遍历就能得到每一年的在世人数。这里用到的核心技巧是 **前缀和（差分数组）**，它的思想类似于“在某个起点加 1，在结束点减 1”，随后把所有的增减累加起来，就得到每个位置的真实值。

**步骤**：

1. **准备一个差分数组** `diff`，长度覆盖所有可能的年份（这里用 1950~2050 共 101 年，再多留一个位方便做 “结束点 -1”。）  
   - `diff[y]` 表示在年份 `y` 人口的**增量**。  
2. **遍历每一条日志** `[birth, death)`：  
   - 在 `birth` 那一年人口要 **+1**（这个人出生了）。  
   - 在 `death` 那一年人口要 **-1**（这个人已经不算在该年了，因为死亡年份不计入）。  
   - 这一步相当于在 `diff` 上做一次 “区间加一”。  
3. **把差分数组转成前缀和**：从最小年份往后累加，得到每一年真实的在世人数。  
4. **遍历一次前缀和数组**，记录最大人口以及最早出现的年份。  

**类比**：  
想象一条河流，`diff` 是在每个河口放的闸门。有人出生时在对应的闸门打开 (+1)，死亡时在对应闸门关闭 (-1)。水流（人口）沿河向下流动，累计所有闸门的开关状态，就得到每段河道的水量（该年的在世人数）。

#### 代码（Python）

```python
from typing import List

def maximumPopulation(logs: List[List[int]]) -> int:
    # 题目约束的年份范围
    START = 1950
    END   = 2050          # 包含 END 本身

    # 差分数组，长度多留一个位置防止越界
    diff = [0] * (END - START + 2)   # 0 ~ 101（共 102 个格子）

    # 1. 把每个人的出生、死亡对 diff 做增减操作
    for birth, death in logs:
        diff[birth - START] += 1      # 出生年份人口 +1
        diff[death - START] -= 1      # 死亡年份人口 -1（死亡年不算）

    # 2. 前缀和 + 同时找最大值
    max_pop = -1
    ans_year = START
    cur = 0          # 当前年份的人口累计值

    for i in range(0, END - START + 1):   # 只遍历到 END（含）
        cur += diff[i]        # 前缀和：累加到当前年份
        year = START + i      # 把下标转换回真实年份

        if cur > max_pop:     # 发现更大的人口数
            max_pop = cur
            ans_year = year
        # 若相等，因我们是从小到大遍历，不会更新 ans_year，保持最早年份

    return ans_year
```

#### 复杂度

- **时间复杂度**：`O(N + Y)`，其中 `N` 是人数，`Y = 101` 是年份数。  
  - 只遍历一次 `logs`（`O(N)`）来做差分，随后一次线性遍历 `diff`（`O(Y)`）得到前缀和。  
  - 用大白话说，就是**先把每个人的“出生+1、死亡-1”记下来，只做两件事**，再顺序走一遍所有年份，整体比暴力快很多。  
- **空间复杂度**：`O(Y)`，需要一个大小约为 102 的差分数组来存增量。相较于输入规模，这仍然是常数级别的额外空间（因为年份范围固定），但比 `O(1)` 多一点。

---

## 心得

- **核心技巧**：差分数组 + 前缀和（也叫区间计数或扫描线思想）。  
- **适用题型**：  
  1. “区间人数/活动最多的时间点”类（如 **Meeting Rooms II**、**Maximum Guests**）。  
  2. “区间加一，求最终数组”类（如 **Car Pooling**、**Range Addition**）。  
  3. “统计每个坐标出现次数”类（如 **Number of Boomerangs** 的离散化思路）。  
- **一句话总结解题钥匙**：**把“每个人在每一年都算一次”转化为“在出生年加一、死亡年减一”，再一次累加得到所有年份的人口**。

---

## 反思

- **第一反应**：看到“每一年都要统计在世人数”，自然想到两层循环直接遍历。  
- **最容易踩的坑**：  
  - **死亡年份不计入**：必须在 `death` 那一年做 `-1`，而不是 `death-1`。  
  - **年份偏移**：数组下标从 `0` 开始，需要把真实年份减去 `START`（1950）才能对应到 `diff` 的位置。  
  - **边界处理**：差分数组要比实际年份多留一个位置，以防在 `death` 为最大小年时出现越界。  
- **下次类似题的第一步**：先判断是否可以把 “区间计数” 用差分数组表示，若可以，则直接转化为 **一次加、一减 + 前缀和**，避免多余的嵌套遍历。