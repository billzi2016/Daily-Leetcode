# #3206. 交替分组 I / Alternating Groups I

> 难度：简单 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/alternating-groups-i/)

---

## 题目（英文原版）

**Description**

There is a circle of red and blue tiles. You are given an array of integers colors. The color of tile i is represented by colors[i]:
Every 3 contiguous tiles in the circle with alternating colors (the middle tile has a different color from its left and right tiles) is called an alternating group.
Return the number of alternating groups.
Note that since colors represents a circle, the first and the last tiles are considered to be next to each other.

**Examples**

**Example 1:**

```
Input: colors = [1,1,1]
Output: 0
Explanation:
```

**Example 2:**

```
Input: colors = [0,1,0,0,1]
Output: 3
Explanation:

Alternating groups:
```

**Constraints**

- 3 <= colors.length <= 100
- 0 <= colors[i] <= 1

---

## 题目（中文翻译）

存在一个由红色和蓝色瓦片组成的圆环。给定一个整数数组 `colors`，其中 `colors[i]` 表示第 i 块瓦片的颜色（0 表示蓝色，1 表示红色）。  
在圆环中，任意 **3 块相邻的瓦片**（即相邻的三个位置）若满足 **中间的瓦片颜色与左侧和右侧的瓦片颜色都不同**，则称这三块瓦片构成一个 **交替组（alternating group）**。  
返回圆环中交替组的数量。  
注意，由于 `colors` 表示的是一个圆环，数组的首尾视为相邻。

**示例 1**  
```
Input: colors = [1,1,1]
Output: 0
Explanation: 没有任何三块相邻的瓦片满足交替条件，因此结果为 0。
```

**示例 2**  
```
Input: colors = [0,1,0,0,1]
Output: 3
Explanation: 交替组如下：
- 下标 0、1、2 的瓦片 (0,1,0)
- 下标 1、2、3 的瓦片 (1,0,0) 不符合，因为中间瓦片与右侧相同
- 实际满足条件的三个交替组为：
  1) 下标 0、1、2 → (0,1,0)
  2) 下标 1、2、4 → (1,0,1)（这里利用了环的特性，4 与 0 相邻）
  3) 下标 2、4、0 → (0,1,0)
```

**约束条件**  
- `3 <= colors.length <= 100`  
- `0 <= colors[i] <= 1`   (仅包含两种颜色)

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把每一块瓷砖都当作“中间块”，把它左边和右边的两块也找出来，逐个比较**。  
- 数据结构：只需要原始的 `colors` 列表。把它想象成一条环形的项链，**下标** 就是挂在项链上的珠子编号。  
- 检查方法：对每一个下标 `i`，先把左边的下标算出来 `left = i‑1`，右边的下标算出来 `right = i+1`（因为是环形，超出两端时要回到另一端，用取模 `% n`）。随后比较三块的颜色：如果左块和右块颜色相同且和中间块不同，就算一个交替组。  
- 为什么正确：题目要求的正好是“中间块颜色不同于左右两块”，而在只有两种颜色（0 / 1）的情况下，左右块相同就一定和中间块相反，所以只要满足上面的条件就一定是合法的交替组。  

如果把 **找左边、找右边** 的过程写成两个循环（虽然每次只跑一次），整体时间复杂度就会是 `O(n²)`（外层遍历 `n` 次，内层每次最坏也要遍历 `n` 次去找左/右），这就是最笨的实现方式。

#### 代码（Python）  

```python
def countAlternatingGroups_bruteforce(colors):
    n = len(colors)
    cnt = 0

    # 对每一个位置 i 当作“中间块”
    for i in range(n):
        # 下面的两个 for 循环是“笨办法”——逐个往左、往右找最近的块
        # 实际上只会循环一次，但写成循环可以帮助初学者理解思路
        left_idx = None
        for step in range(1, n + 1):          # 最多走 n 步才能回到自己
            left = (i - step) % n
            left_idx = left
            break                            # 找到最近的左邻居就停

        right_idx = None
        for step in range(1, n + 1):
            right = (i + step) % n
            right_idx = right
            break                            # 找到最近的右邻居就停

        # 检查是否满足“左右相同且和中间不同”
        if colors[left_idx] == colors[right_idx] and colors[left_idx] != colors[i]:
            cnt += 1

    return cnt
```

> **关键行中文注释**  
> - `for i in range(n)`: 把每块都当作中间块遍历。  
> - `left = (i - step) % n`: 环形下标，超出左端会回到右端。  
> - `if colors[left_idx] == colors[right_idx] and colors[left_idx] != colors[i]`: 正是题目定义的交替组判定。  

#### 复杂度  

- **时间复杂度：`O(n²)`**  
  - 外层循环 `n` 次，内层寻找左/右邻居的循环最坏也要走 `n` 步（虽然实际只走一步），所以乘起来是 `n × n`。  
  - 对于本题的最大规模 `n ≤ 100`，`100 × 100 = 10,000` 次操作仍然可以接受，但显然有更好的办法。  

- **空间复杂度：`O(1)`**  
  - 只用了几个额外的整数变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈在于“寻找左邻居、右邻居”这一步**。  
实际上因为题目已经给出了 **每块的颜色**，左邻居就是下标 `i‑1`（环形取模），右邻居就是下标 `i+1`（同样环形取模），不需要任何循环去找。  

因此，只要一次遍历数组，**直接读取相邻下标的颜色**，就能在 `O(n)` 的时间内完成计数。  

核心技巧：**利用取模实现环形数组的邻接访问**。  
- `left = (i - 1) % n` 把 “左边超出” 的情况自动映射到数组最后。  
- `right = (i + 1) % n` 把 “右边超出” 的情况自动映射到数组开头。  

判断条件仍然是 `colors[left] == colors[right] != colors[i]`。  
这一步只需要常数时间，整体只需遍历一次 `n` 个位置，即可得到答案。

> 类比：把环形项链想象成 **一条闭合的跑道**，跑步时只需要看左手和右手的颜色，根本不必去“跑遍整个跑道”去找邻居。

#### 代码（Python）  

```python
def countAlternatingGroups(colors):
    """
    返回交替组的数量。
    思路：一次遍历，直接取左、右相邻下标（取模实现环形），检查
          colors[left] == colors[right] != colors[i]。
    """
    n = len(colors)
    cnt = 0

    for i in range(n):
        left = (i - 1) % n          # 环形左邻居
        right = (i + 1) % n         # 环形右邻居

        # 判断：左块和右块相同且都和中间块不同
        if colors[left] == colors[right] and colors[left] != colors[i]:
            cnt += 1

    return cnt
```

> **关键行中文注释**  
> - `left = (i - 1) % n`、`right = (i + 1) % n`：一行代码搞定环形邻接。  
> - `if colors[left] == colors[right] and colors[left] != colors[i]`：正是题目中“中间块颜色不同于左右两块”的判定。  

#### 复杂度  

- **时间复杂度：`O(n)`** — 只遍历一次数组，`n` 是数组长度。对比暴力的 `O(n²)`，快了 **n 倍**。  
- **空间复杂度：`O(1)`** — 只用了几个整数变量，和输入大小无关。  

---  

## 心得  

- **核心技巧**：环形数组的邻接访问（取模） + 一次遍历即可完成判定。  
- **适用的题型**  
  1. “环形滑动窗口” 类题，例如 LeetCode 1343 *Number of Sub-arrays With Bounded Maximum*（环形变体）。  
  2. “相邻元素关系” 类题，如判断数组中是否存在相邻相等/不相等的模式。  
  3. “固定长度子数组判定” 类，如 LeetCode 643 *Maximum Average Subarray I*（固定窗口长度）。  

- **一句话总结解题钥匙**：**把环形看成普通数组，使用取模直接定位左右邻居，一遍遍历即可。**  

---  

## 反思  

- **第一反应**：看到“圆形”“相邻三块”，立刻想到要把数组首尾相连，检查每个位置的左、右邻居。  
- **最容易踩的坑**  
  1. **边界取模写错**：`(i-1) % n` 在 Python 中已经是正数，但在某些语言需要额外处理负数取模。  
  2. **忘记环形**：只检查 `i` 到 `i+2` 的普通子数组会漏掉跨越数组末尾的情况。  
  3. **颜色只有 0/1** 的前提：如果颜色种类更多，左块和右块相同不一定意味着和中间块相反，需要更一般的判定。  

- **下次遇到同类题的第一步**：先确认是否是 **环形**，然后 **用取模把左/右邻居写出来**，再依据题目条件写判断式。这样即可快速得到 `O(n)` 的最优解。