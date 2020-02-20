# #781. 森林中的兔子 / Rabbits in Forest

> 难度：中等 · 标签：Array、Hash Table、Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/rabbits-in-forest/)

---

## 题目（英文原版）

**Description**

There is a forest with an unknown number of rabbits. We asked n rabbits "How many rabbits have the same color as you?" and collected the answers in an integer array answers where answers[i] is the answer of the ith rabbit.
Given the array answers, return the minimum number of rabbits that could be in the forest.

**Examples**

**Example 1:**

```
Input: answers = [1,1,2]
Output: 5
Explanation:
The two rabbits that answered "1" could both be the same color, say red.
The rabbit that answered "2" can't be red or the answers would be inconsistent.
Say the rabbit that answered "2" was blue.
Then there should be 2 other blue rabbits in the forest that didn't answer into the array.
The smallest possible number of rabbits in the forest is therefore 5: 3 that answered plus 2 that didn't.
```

**Example 2:**

```
Input: answers = [10,10,10]
Output: 11
```

**Constraints**

- 1 <= answers.length <= 1000
- 0 <= answers[i] < 1000

---

## 题目（中文翻译）

给定一片森林，其中兔子的数量未知。我们随机询问了 **n** 只兔子「和你颜色相同的兔子有多少只？」并将得到的答案收集到一个整数数组 **answers** 中，其中 `answers[i]` 表示第 **i** 只兔子的回答。  
给定数组 **answers**，返回森林中可能出现的 **最小** 兔子总数。

**示例 1**  
**输入**: `answers = [1,1,2]`  
**输出**: `5`  
**解释**:  
- 两只回答「1」的兔子可以是同一种颜色，例如红色。  
- 回答「2」的那只兔子不可能是红色，否则答案会矛盾。设它的颜色为蓝色。  
- 那么在森林中还应该还有另外 **2** 只同样颜色（蓝色）的兔子，但它们没有被问及，因而没有出现在数组中。  
- 因此森林中最少可能的兔子数量为 **5**：已回答的 **3** 只加上未回答的 **2** 只。

**示例 2**  
**输入**: `answers = [10,10,10]`  
**输出**: `11`  

**约束条件**  
- `1 <= answers.length <= 1000`  
- `0 <= answers[i] < 1000`   (答案均为非负整数)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每只兔子都当成“自己单独的一类”，**  
它说 “我有 `answers[i]` 只同颜色的兔子”，于是我们把它算进 `answers[i] + 1` 只兔子（自己 + 那些同颜色的）。  
把所有兔子这样算一遍，最后把这些数字全部相加，就是一种合法的森林规模——因为每只兔子的回答都被满足了。

- **用到的数据结构**：只需要遍历原数组，用一个整数 `total` 累加即可。  
  不需要哈希表、堆或其他高级结构，类似我们在超市里把每件商品的价格加到一起得到总价。

- **为什么这个方法一定正确**  
  因为我们把每只兔子所在的颜色组当成 **“至少有 `answers[i] + 1` 只兔子”**。  
  只要我们把每只兔子对应的最小可能数量都算进去，所有回答必然被满足，只是可能会 **“多算”** 一些兔子。

- **时间/空间复杂度的大白话**  
  - **时间**：我们只遍历一次 `answers`，所以时间是 “线性的”，记作 `O(n)`（n 是数组长度），意思是 **随兔子数量增长，耗时也按同样比例增长**。  
  - **空间**：只用了一个计数变量 `total`，不随输入大小增长，记作 `O(1)`，即 **常数空间**。

#### 代码（Python）

```python
def min_rabbits_bruteforce(answers):
    """
    暴力思路：每只兔子单独算一个最小的颜色组
    """
    total = 0                     # 用来累计最少的兔子总数
    for a in answers:             # 逐个读取每只兔子的回答
        total += a + 1            # a 只同颜色的 + 自己 = a+1 只
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，n 越大，时间线性增长。  
- **空间复杂度**：`O(1)` —— 只用了一个整数变量 `total`，不随输入大小变化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**我们把每只兔子的 “最小颜色组大小” 都累加了**，导致同一种颜色的兔子被多算了。  
要想 **最小化** 森林的总兔子数，需要把 **相同颜色的兔子合并**，而合并的原则来源于回答本身：

1. **回答的含义**  
   - 如果一只兔子说 `a`，说明 **它所在的颜色组里恰好有 `a+1` 只兔子**（自己 + `a` 只同颜色的）。  
   - 这意味着，同一种颜色的兔子最多只能出现 `a+1` 次，否则就会出现 “超过了回答所暗示的上限”。

2. **把相同回答的兔子分组**  
   - 统计每个不同回答 `a` 出现了多少次，记作 `cnt[a]`。  
   - 对于回答 `a`，每组最多容纳 `a+1` 只兔子。  
   - 如果 `cnt[a]` 正好是 `a+1` 的整数倍，我们只需要 `cnt[a] / (a+1)` 组。  
   - 否则，还会剩下一部分兔子（不足 `a+1` 只），它们仍然需要完整的一组，因为颜色组必须是完整的 `a+1` 只。  
   - 因此 **组数 = ceil(cnt[a] / (a+1))**，可以用整数除法 `((cnt[a] + a) // (a+1))` 来实现。

3. **把每组的大小加起来**  
   - 每组的大小固定是 `a+1`，所以该回答贡献的兔子总数是  
     `组数 * (a+1)`。

把所有不同的回答都这样算一遍，就得到 **满足所有回答的最小森林规模**。

> **类比**：想象每种颜色是一辆巴士，巴士最多只能坐 `a+1` 位乘客。如果有 7 位乘客说 “我所在的巴士只能坐 4 人”，我们需要 **2 辆巴士**（`ceil(7/4)=2`），每辆 4 人，总共 8 位座位，刚好能容纳这 7 位乘客，同时还有 1 位空座位（对应森林里未被调查到的兔子）。

#### 代码（Python）

```python
from collections import Counter
import math

def minNumberOfRabbits(answers):
    """
    最优解：统计相同回答，按组装配计算最小总数
    """
    cnt = Counter(answers)          # 统计每个回答出现的次数
    total = 0                       # 最终答案

    for a, freq in cnt.items():     # 遍历每种不同的回答 a
        group_size = a + 1          # 同颜色的最大组容量
        # 需要的组数 = 向上取整 (freq / group_size)
        groups = (freq + group_size - 1) // group_size   # 等价于 math.ceil
        total += groups * group_size   # 每组都有 group_size 只兔子
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)` ——  
  - 统计次数 `Counter` 只遍历一次数组。  
  - 再遍历不同的回答（最多 1000 种），与 `n` 同阶。  
  - 所以整体仍是线性时间，随兔子数量线性增长。

- **空间复杂度**：`O(m)` ——  
  - `m` 是不同回答的种类数，最坏情况下等于 `n`（每只兔子回答不同），但受限制 `answers[i] < 1000`，所以最多 1000 种。  
  - 用来存哈希表的空间随种类数增长，属于 **线性空间**。

---

## 心得

- **核心技巧**：**把“相同答案的兔子”视为同一颜色的候选成员，用“每组最多 a+1 只” 的限制来分组**。这是一种 **计数 + 向上取整** 的贪心思路。
- **适用的题型**  
  1. “人数分组” 类问题，如 “根据每个人的报数，求最少的团队数”。  
  2. “容量上限” 类问题，例如 “每个箱子最多装 k 件物品，求最少箱子数”。  
  3. “统计出现次数后分块” 的题目，如 “将相同频率的字符压缩到固定长度的块”。
- **一句话总结解题钥匙**：**“先统计，再把每种回答按最大容纳量向上取整分组”。**

---

## 反思

- **第一反应**：看到“多少只同颜色的兔子”，立刻想到 **把相同颜色的兔子聚在一起**，于是想到计数。
- **最容易踩的坑**  
  - 忽略了 **向上取整**：如果只用整数除法会少算一组，导致答案偏小。  
  - 没考虑 **回答为 0 的情况**：此时每只兔子自己是一组，`group_size = 1`，代码仍然要能处理。  
  - 误以为所有兔子可以直接放在同一组，导致答案错误。
- **下次遇到同类题**，第一步应该 **统计每种限制出现的次数**，然后 **根据每种限制的最大容量向上取整求组数**，最后把组数乘以容量求和。这样可以快速得到最小的整体规模。